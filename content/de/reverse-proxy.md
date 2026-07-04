---
title: Reverse Proxy & TLS
description: Betreibe die Hinata-Web-App und die API hinter nginx, Caddy oder Traefik mit HTTPS, korrektem SSE/WebSocket-Durchreichen und Trusted-Proxy-Headern.
---

# Reverse Proxy & TLS

Hinata veröffentlicht auf dem Host zwei reine HTTP-Dienste: die **Web-App** auf
`HINATA_APP_PORT` (Standard `3456`) und die **API** auf `HINATA_PORT` (Standard
`3356`). In Produktion legst du diese Ports niemals direkt offen — du betreibst
einen Reverse Proxy, der TLS terminiert, saubere Subdomains ausliefert und die
Anfragen an die Container weiterreicht.

Das empfohlene Setup nutzt zwei Subdomains:

| Subdomain | Zweck | Weiterleitung an |
| --- | --- | --- |
| `track.example.com` | Flutter-Web-App | `host:3456` (`HINATA_APP_PORT`) |
| `api.track.example.com` | REST-API + SSE | `host:3356` (`HINATA_PORT`) |

!!! info "Warum zwei Subdomains"
    Der Web-Build ruft die API cross-origin auf. Web-App und API auf eigene
    Hostnamen zu trennen hält CORS explizit, erlaubt unabhängiges Skalieren bzw.
    Caching und entspricht den Vorgaben aus `.env.example`
    (`HINATA_BASE_URL` / `HINATA_WEB_BASE_URL`).

Diese Seite liefert dir vollständige, funktionierende Konfigurationen für
**nginx**, **Caddy** und **Traefik** sowie die drei serverseitigen
Einstellungen, die zu deinem Proxy passen müssen: Trusted Proxies, CORS und
Streaming.

## Vorab: drei Einstellungen, die zusammenpassen müssen

Egal welchen Proxy du wählst, setze diese Werte am Hinata-**Server**-Container
(siehe [Konfigurationsreferenz](/de/configuration.html)):

```properties
# Öffentliche URLs, die der Server bekannt gibt (JWT-Issuer, E-Mail-Deeplinks, SSO-Redirects)
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com

# Browser-Origins, die die API cross-origin aufrufen dürfen — MUSS die Web-App enthalten
HINATA_CORS_ALLOWED_ORIGINS=https://track.example.com

# CIDR(s) deines Reverse Proxy, damit der Server X-Forwarded-* von ihm vertraut
HINATA_TRUSTED_PROXIES=172.16.0.0/12
```

!!! danger "HINATA_TRUSTED_PROXIES korrekt setzen — sonst kein Rate-Limiting pro Client"
    Hinata liest die echte Client-IP aus `X-Forwarded-For` **nur**, wenn der
    direkte Gegenpart innerhalb von `HINATA_TRUSTED_PROXIES` liegt. Leer =
    niemandem vertrauen, also scheinen alle Anfragen vom Proxy zu kommen. Da
    Rate-Limiting (`HINATA_RATE_LIMIT_*`) und die Brute-Force-Login-Sperre auf
    die Client-IP schlüsseln, bedeutet ein falscher Wert **einen gemeinsamen
    Zähler für das ganze Internet**: Entweder werden alle zusammen gedrosselt,
    oder ein gefälschter `X-Forwarded-For` umgeht das Limit. Setze den Wert auf
    die Adresse des Proxy **so, wie der Container sie sieht** (meist das
    Docker-Bridge-Subnetz, z. B. `172.16.0.0/12`), nicht auf die öffentliche IP
    des Proxy.

    Die Peer-Adresse findest du in den Serverlogs oder über das Netzwerk:

    ```bash
    docker network inspect hinata_hinata \
      --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
    ```

!!! tip "HSTS ist bereits erledigt"
    Der Server sendet `Strict-Transport-Security` (plus CSP und
    `Referrer-Policy`) in seinen eigenen Antworten, du musst HSTS also **nicht**
    im Proxy hinzufügen. Überlasse dem Proxy aber die TLS-Terminierung und die
    Zertifikatserneuerung.

## nginx + Let's Encrypt (certbot)

Eine bewährte Wahl. Hole zuerst Zertifikate für beide Hostnamen, nutze dann die
Server-Blöcke unten.

### Zertifikate holen

```bash
sudo certbot certonly --nginx \
  -d track.example.com \
  -d api.track.example.com
```

Certbot richtet den Erneuerungs-Timer automatisch ein; teste ihn mit
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

    # Anhänge werden hierhin hochgeladen — an dein ENV-Attachment-Limit anpassen
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
    Der häufigste SSE-Fehler ist ein Proxy, der die Antwort puffert.
    `proxy_buffering off` plus ein langes `proxy_read_timeout` in der
    `/stream`-Location sorgen dafür, dass Live-Attachment-Updates in Echtzeit
    ankommen. Bleibt die Standard-Pufferung an, wirken Events „hängend“, bis die
    Verbindung schließt.

## Caddy (automatisches HTTPS)

Caddy ist die aufwandsärmste Variante: Zeig es auf deine zwei Hostnamen, und es
holt und erneuert Let's-Encrypt-Zertifikate für dich — kein certbot, keine
Timer. Das ist die gesamte `Caddyfile`:

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
    automatisch, und `flush_interval -1` deaktiviert die Antwort-Pufferung, sodass
    SSE sofort fließt. WebSocket-Upgrades werden transparent durchgereicht — ohne
    Zusatzkonfiguration. Stell nur sicher, dass `HINATA_TRUSTED_PROXIES` die
    Adresse abdeckt, von der aus Caddy den Container erreicht.

Für ein echtes Deployment hinter Port 80/443 hinterlege eine gültige E-Mail für
ACME und stell sicher, dass beide DNS-Einträge auf den Host zeigen:

```caddy
{
    email admin@example.com
}
```

## Traefik (Labels)

Wenn du Traefik bereits als Docker-Ingress betreibst, füge Labels an die
Services `hinata-app` und `hinata-server` hinzu statt einer separaten
Konfigurationsdatei. Angenommen ein `websecure`-Entrypoint auf `:443` und ein
Resolver namens `le`:

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
    Traefik streamt Antworten standardmäßig ohne Pufferung, der Attachment-SSE-
    Endpunkt funktioniert also sofort. Wenn du über Traefik routest, setze
    `HINATA_TRUSTED_PROXIES` auf Traefiks Container-/Netzwerk-CIDR — Traefik
    reicht `X-Forwarded-For` weiter, und Hinata berücksichtigt es nur von einem
    vertrauten Peer.

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

Um zu bestätigen, dass echte Client-IPs geloggt werden (nicht die Proxy-Adresse),
beobachte die Serverlogs, während du einen Endpunkt von einem anderen Rechner
ansprichst — die geloggte IP sollte **deine** sein, nicht das Docker-Gateway.
Zeigt sie die Adresse des Proxy, ist `HINATA_TRUSTED_PROXIES` falsch.

## Nächste Schritte

- [Konfigurationsreferenz](/de/configuration.html) — jede Umgebungsvariable
- [Produktiv-Deployment](/de/deployment.html) — der komplette Docker-Compose-Stack
- [Setup & Erststart](/de/setup-wizard.html) — erste Organisation und Admin anlegen
- [Backups & Upgrades](/de/backups.html) — den Stack über die Zeit betreiben
