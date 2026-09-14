---
title: Reverse Proxy & TLS
description: Betreibe Web-App und API hinter nginx, Caddy oder Traefik mit HTTPS, SSE und Trusted-Proxy-Headern.
---

# Reverse Proxy & TLS

Hinata stellt auf dem Host zwei reine HTTP-Dienste bereit:

- die **Web-App** auf `HINATA_APP_PORT` (Standard `3456`)
- die **API** auf `HINATA_PORT` (Standard `3356`)

In Produktion legst du diese Ports nie direkt offen. Ein Reverse Proxy terminiert TLS und leitet die Anfragen an die Container weiter.

Empfohlen sind zwei Subdomains:

| Subdomain | Zweck | Weiterleitung an |
| --- | --- | --- |
| `track.example.com` | Flutter-Web-App | `host:3456` (`HINATA_APP_PORT`) |
| `api.track.example.com` | REST-API + SSE | `host:3356` (`HINATA_PORT`) |

!!! info "Warum zwei Subdomains"
    Die Web-App ruft die API cross-origin auf. Mit getrennten Hostnamen bleibt
    CORS explizit, du kannst beides getrennt skalieren oder cachen, und es passt
    zu den Vorgaben aus `.env.example` (`HINATA_BASE_URL` / `HINATA_WEB_BASE_URL`).

Unten findest du fertige Konfigurationen für **nginx**, **Caddy** und
**Traefik**.

## Vorab: drei Einstellungen, die zusammenpassen müssen

Setze diese Werte am Hinata-**Server**-Container, egal welchen Proxy du nutzt
(siehe [Konfigurationsreferenz](/de/configuration.html)):

```properties
# Öffentliche URLs, die der Server bekannt gibt (JWT-Issuer, E-Mail-Deeplinks, SSO-Redirects)
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com

# Browser-Origins, die die API cross-origin aufrufen dürfen: MUSS die Web-App enthalten
HINATA_CORS_ALLOWED_ORIGINS=https://track.example.com

# CIDR(s) deines Reverse Proxy, damit der Server X-Forwarded-* von ihm vertraut
HINATA_TRUSTED_PROXIES=172.16.0.0/12
```

!!! danger "HINATA_TRUSTED_PROXIES korrekt setzen, sonst kein Rate-Limiting pro Client"
    Hinata liest die echte Client-IP aus `X-Forwarded-For` **nur**, wenn der
    direkte Gegenpart in `HINATA_TRUSTED_PROXIES` liegt. Ist der Wert leer, wird
    niemandem vertraut, und alle Anfragen scheinen vom Proxy zu kommen.

    Rate-Limiting (`HINATA_RATE_LIMIT_*`) und die Login-Sperre gegen Brute Force
    hängen an der Client-IP. Ein falscher Wert heißt deshalb **ein gemeinsamer
    Zähler für das ganze Internet**. Entweder werden alle gemeinsam gedrosselt,
    oder ein gefälschter `X-Forwarded-For` umgeht das Limit.

    Trag die Adresse des Proxy ein, **wie der Container sie sieht** (meist das
    Docker-Bridge-Subnetz, z. B. `172.16.0.0/12`). Nicht die öffentliche IP.

    Die Adresse steht in den Serverlogs, oder du fragst das Netzwerk ab:

    ```bash
    docker network inspect hinata_hinata \
      --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
    ```

!!! tip "HSTS ist bereits erledigt"
    Der Server sendet selbst `Strict-Transport-Security`, CSP und
    `Referrer-Policy`. HSTS musst du im Proxy **nicht** ergänzen. TLS und die
    Zertifikatserneuerung übernimmt der Proxy.

## nginx + Let's Encrypt (certbot)

Hol zuerst Zertifikate für beide Hostnamen. Dann nutzt du die Server-Blöcke unten.

### Zertifikate holen

```bash
sudo certbot certonly --nginx \
  -d track.example.com \
  -d api.track.example.com
```

Certbot richtet den Erneuerungs-Timer selbst ein. Testen kannst du ihn mit
`sudo certbot renew --dry-run`.

### Server-Blöcke

```nginx
# --- Alles von HTTP auf HTTPS umleiten --------------------------------------
server {
    listen 80;
    listen [::]:80;
    server_name track.example.com api.track.example.com;
    return 301 https://$host$request_uri;
}

# --- Web-App: track.example.com  →  host:3456 -------------------------------
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name track.example.com;

    ssl_certificate     /etc/letsencrypt/live/track.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/track.example.com/privkey.pem;

    # Flutter-Web kann große canvaskit/wasm-Assets ausliefern
    client_max_body_size 25m;

    location / {
        proxy_pass http://127.0.0.1:3456;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;
    }
}

# --- API: api.track.example.com  →  host:3356 -------------------------------
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name api.track.example.com;

    ssl_certificate     /etc/letsencrypt/live/api.track.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.track.example.com/privkey.pem;

    # Anhänge werden hierhin hochgeladen: an dein ENV-Attachment-Limit anpassen
    client_max_body_size 50m;

    location / {
        proxy_pass http://127.0.0.1:3356;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;
    }

    # --- Server-Sent Events (Live-Attachment-Sync) --------------------------
    # SSE-Verbindungen bleiben offen; Pufferung deaktivieren und lange
    # Read-Timeouts nutzen, sonst kommen Events nur schubweise oder brechen ab.
    location ~ ^/api/v1/.*/stream$ {
        proxy_pass http://127.0.0.1:3356;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Upgrade-Handling (für SSE harmlos, für WebSocket bereit)
        proxy_set_header Connection        "";
        proxy_set_header Upgrade           $http_upgrade;

        proxy_buffering    off;   # jedes Event sofort durchreichen
        proxy_cache        off;
        chunked_transfer_encoding off;
        proxy_read_timeout 3600s; # Stream bis zu einer Stunde idle offen halten
        proxy_send_timeout 3600s;
    }
}
```

!!! warning "Den Stream nicht puffern"
    Der häufigste SSE-Fehler ist ein Proxy, der die Antwort puffert. Mit
    `proxy_buffering off` und einem langen `proxy_read_timeout` in der
    `/stream`-Location kommen Anhang-Updates in Echtzeit an. Mit der
    Standardpufferung „hängen“ Events, bis die Verbindung schließt.

## Caddy (automatisches HTTPS)

Caddy macht am wenigsten Arbeit. Es holt und erneuert die Let's-Encrypt-Zertifikate
selbst, ohne certbot und Timer. Das ist die komplette `Caddyfile`:

```caddy
track.example.com {
    reverse_proxy 127.0.0.1:3456
}

api.track.example.com {
    # SSE-/Streaming-Endpunkte: ohne Pufferung durchreichen
    @stream path_regexp stream ^/api/v1/.*/stream$
    reverse_proxy @stream 127.0.0.1:3356 {
        flush_interval -1
    }

    reverse_proxy 127.0.0.1:3356
}
```

!!! tip "Caddy macht das Richtige von allein"
    Caddy setzt `X-Forwarded-For`, `X-Forwarded-Proto` und `X-Forwarded-Host`
    automatisch. `flush_interval -1` schaltet die Pufferung ab, damit SSE sofort
    fließt. WebSocket-Upgrades gehen ohne Zusatzkonfiguration durch. Achte nur
    darauf, dass `HINATA_TRUSTED_PROXIES` die Adresse abdeckt, von der Caddy den
    Container erreicht.

Für ein echtes Deployment auf Port 80/443 braucht Caddy eine gültige E-Mail für
ACME. Beide DNS-Einträge müssen auf den Host zeigen:

```caddy
{
    email admin@example.com
}
```

## Traefik (Labels)

Läuft Traefik bei dir schon als Docker-Ingress, setzt du Labels an die Services
`hinata-app` und `hinata-server`. Eine eigene Konfigurationsdatei brauchst du
nicht. Das Beispiel nimmt einen `websecure`-Entrypoint auf `:443` und einen
Resolver namens `le` an:

```yaml
services:
  hinata-server:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.hinata-api.rule=Host(`api.track.example.com`)"
      - "traefik.http.routers.hinata-api.entrypoints=websecure"
      - "traefik.http.routers.hinata-api.tls.certresolver=le"
      - "traefik.http.services.hinata-api.loadbalancer.server.port=8080"

  hinata-app:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.hinata-web.rule=Host(`track.example.com`)"
      - "traefik.http.routers.hinata-web.entrypoints=websecure"
      - "traefik.http.routers.hinata-web.tls.certresolver=le"
      - "traefik.http.services.hinata-web.loadbalancer.server.port=80"
```

!!! note "Traefik und SSE"
    Traefik puffert Antworten standardmäßig nicht. Der SSE-Endpunkt für Anhänge
    funktioniert also sofort. Setze `HINATA_TRUSTED_PROXIES` auf das CIDR von
    Traefiks Container oder Netzwerk. Traefik reicht `X-Forwarded-For` weiter,
    und Hinata beachtet es nur von einem vertrauten Gegenpart.

## Überprüfen, ob es funktioniert

```bash
# API über den Proxy erreichbar und gesund
curl -s https://api.track.example.com/actuator/health
# → {"status":"UP"}

# Öffentliche Metadaten (kein Token nötig)
curl -s https://api.track.example.com/api/v1/meta

# Web-App liefert HTML
curl -sI https://track.example.com | head -n 1
```

Prüf auch, ob echte Client-IPs geloggt werden. Ruf dazu von einem anderen
Rechner einen Endpunkt auf und schau in die Serverlogs. Dort sollte **deine** IP
stehen, nicht das Docker-Gateway. Steht dort die Adresse des Proxy, ist
`HINATA_TRUSTED_PROXIES` falsch.

## Nächste Schritte

- [Konfigurationsreferenz](/de/configuration.html): jede Umgebungsvariable
- [Produktiv-Deployment](/de/deployment.html): der komplette Docker-Compose-Stack
- [Setup & Erststart](/de/setup-wizard.html): erste Organisation und Admin anlegen
- [Backups & Upgrades](/de/backups.html): den Stack langfristig betreiben
