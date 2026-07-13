---
title: Produktiv-Deployment
description: Ein vollständiger, geordneter Durchlauf für das produktive Deployment von Hinata mit Docker Compose, X.509-MongoDB, TLS und sicherem Update-Ablauf.
---

# Produktiv-Deployment

Dies ist der vollständige Produktiv-Durchlauf — jeder Schritt, in Reihenfolge, vom
sauberen Host bis zur laufenden, geprüften Instanz hinter deinem Reverse Proxy. Er
nutzt das `prod`-Profil: ein MongoDB-Replica-Set mit TLS und
X.509-Client-Authentifizierung.

Falls noch nicht geschehen, lies zuerst den
[Überblick zum Selbstbetrieb](/de/self-hosting.html) für das große Ganze. Für die
Bedeutung jeder hier erwähnten Einstellung halte die
[Konfigurationsreferenz](/de/configuration.html) daneben offen.

## Voraussetzungen

- Ein Linux-Host mit **Docker Engine** und dem **Docker-Compose-Plugin**
  (`docker compose`, v2).
- `openssl`, `keytool` (aus einem JRE/JDK) und eine POSIX-Shell für die
  Hilfsskripte in `deploy/`.
- Zwei DNS-Namen, die du kontrollierst — einen für die API und einen für die
  Web-App. Auf dieser Seite verwenden wir `api.track.example.com` (API) und
  `track.example.com` (Web).
- Einen Reverse Proxy, der HTTPS terminiert (Nginx, Caddy, Traefik, ein
  NAS-Reverse-Proxy …). Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).
- Ein SMTP-Relay für ausgehende Mail. Siehe [E-Mail & SMTP](/de/email.html).

## 1. Das Server-Repository holen

```bash
git clone https://github.com/hinata-platform/hinata-server.git
cd hinata-server
```

Spätere Updates sind ein `git pull` in diesem Verzeichnis — die Images selbst
werden von GHCR gezogen, du baust also nie auf dem Host.

## 2. Deine .env anlegen

```bash
cp .env.example .env
```

`.env.example` ist vollständig kommentiert; jeder Wert kann auch als schlichte
Umgebungsvariable am Container gesetzt werden. Wir füllen sie in den nächsten
Schritten aus.

## 3. Secrets erzeugen

```bash
./deploy/generate-secrets.sh
```

Dieses Skript:

- erzeugt `deploy/mongo-keyfile` (das Internal-Auth-Keyfile des Replica Sets),
  falls noch nicht vorhanden, und
- gibt vorgeschlagene Zufallswerte für `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD`
  und `MINIO_ROOT_PASSWORD` aus.

Kopiere die ausgegebenen Werte in deine `.env`.

!!! warning "Das JWT-Secret ist in Produktion erforderlich"
    `HINATA_JWT_SECRET` muss ein zufälliger String mit **mindestens 64 Zeichen**
    sein (HS512). Der Server startet im prod-Profil ohne dieses Secret nicht. Falls
    du den Generator nicht verwendet hast, erzeuge eines mit:

    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```

    Das Rotieren dieses Secrets macht jedes ausgegebene Token ungültig — alle
    Nutzer müssen sich neu anmelden.

## 4. Die MongoDB-X.509-PKI erzeugen

Produktions-Mongo nutzt TLS plus X.509-Client-Authentifizierung — das
Gold-Standard-Setup — es gibt also kein Datenbank-Passwort im Connection-String.
Erzeuge die Zertifizierungsstelle, das Server-Zertifikat und das
Client-Zertifikat der Anwendung:

```bash
./deploy/x509/generate-certs.sh prod
```

Dies schreibt unter `deploy/x509/prod/`: die CA (`ca.crt`/`ca.key`), das
mongod-Server-Zertifikat (`server.pem`), den JVM-Keystore der App
(`hinata-app.p12`), den Truststore (`truststore.p12`), das Replica-Set-`keyfile`
und `app-subject-dn.txt` — den Subject-DN des Client-Zertifikats, der zum
Mongo-Benutzernamen wird.

Die Keystore- und Truststore-Passwörter sind standardmäßig `changeit`. Ändere sie
und setze die passenden Werte in `.env`:

```properties
HINATA_MONGO_TLS_KEYSTORE_PASSWORD=change-me-keystore
HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD=change-me-truststore
```

!!! tip
    Führe den Zertifikatsgenerator **vor** dem Setzen der Passwörter aus, wenn du
    den Standard willst — oder exportiere `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` /
    `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD`, bevor du ihn ausführst, damit die
    PKCS#12-Dateien von Anfang an mit deinen gewählten Passwörtern gebaut werden.
    Volle Details auf der Seite [MongoDB & X.509](/de/database.html).

## 5. Eine realistische .env

Hier eine repräsentative Produktions-`.env`. Platzhalter lauten `change-me…`;
Secrets sind so gezeigt, als kämen sie vom Generator (deine werden abweichen).
Passe die Hosts an deine an.

```properties
# Profil
SPRING_PROFILES_ACTIVE=prod

# Öffentliche URLs
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com

# Image-Tags (statt latest eine Version pinnen für reproduzierbare Deployments)
HINATA_SERVER_TAG={{version}}
HINATA_APP_TAG={{version}}

# JWT — aus ./deploy/generate-secrets.sh
HINATA_JWT_SECRET=Kf3mS0pQ9xR2vN7wY1bZ8cH4dJ6gL5aT0eU3iO2rW9kP1sX4nC7mB6vD8fA2hQ0

# MongoDB-SCRAM-Root (nur Admin/intern — die App nutzt X.509)
MONGO_ROOT_USERNAME=hinata
MONGO_ROOT_PASSWORD=9f1c7a4e2b6d8039a5c1e7f2b4d6a8c0
HINATA_MONGO_TLS_KEYSTORE_PASSWORD=change-me-keystore
HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD=change-me-truststore

# Reverse Proxy — CIDR, aus dem der Proxy den Container erreicht (siehe Schritt 8)
HINATA_TRUSTED_PROXIES=172.16.0.0/12

# SMTP — ein echtes Relay, damit Mail zugestellt wird
HINATA_SMTP_HOST=smtp.example.com
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.com
HINATA_SMTP_PASSWORD=change-me-smtp
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=hinata@example.com

# Objektspeicher — mitgeliefertes MinIO (setze stattdessen COMPOSE_PROFILES=
# und HINATA_STORAGE_* / HINATA_S3_* / HINATA_AZURE_* für AWS S3, GCS oder
# Azure; siehe die Objektspeicher-Seite)
COMPOSE_PROFILES=local-storage
MINIO_ROOT_USER=hinata
MINIO_ROOT_PASSWORD=3b8e0d5f7a2c9146e0b3d7f1a5c8e2b4
HINATA_S3_BUCKET=hinata

# App-Integration
HINATA_PRIVACY_POLICY_URL=https://example.com/privacy
HINATA_APP_MIN_VERSION={{version}}
HINATA_CORS_ALLOWED_ORIGINS=https://track.example.com
HINATA_DOCS_ENABLED=false

# Push + Deep-Links — Standard-Gateway; nur überschreiben für ein eigenes
HINATA_GATEWAY_BASE_URL=https://connect.hinata.ahmadre.com

# Erststart (leer lassen, um den In-App-Assistenten zu nutzen)
HINATA_SETUP_AUTO_COMPLETE=false

# Demo-Seed — NIEMALS in Produktion aktivieren
HINATA_DEMO_SEED=false
HINATA_DEMO_RESET=false

# Rate-Limiting / Brute-Force
HINATA_RATE_LIMIT_ENABLED=true
HINATA_RATE_LIMIT_API=300
HINATA_RATE_LIMIT_AUTH=10
HINATA_MAX_LOGIN_FAILURES=5
HINATA_LOGIN_BLOCK_MINUTES=15

# Veröffentlichte Host-Ports (der Reverse Proxy leitet hierher weiter)
HINATA_PORT=3356
HINATA_APP_PORT=3456
```

!!! warning "Ändere jeden Standardwert"
    Die mitgelieferte `.env.example` enthält Entwicklungs-Defaults
    (`MONGO_ROOT_PASSWORD=hinata-dev-secret`, `changeit`-Keystore-Passwörter, ein
    leeres JWT-Secret). Jeder davon in Produktion unverändert gelassen ist eine
    ernste Lücke. Erzeuge für alle echte Secrets.

## 6. Den Stack starten

Starte zuerst MongoDB, damit das Replica Set initiieren kann und du den
X.509-Nutzer registrieren kannst, und starte dann den Rest.

```bash
# Datenbank-Knoten starten
docker compose up -d mongo1 mongo2 mongo-arbiter

# Das Client-Zertifikat der App als $external-Mongo-Nutzer registrieren
./deploy/x509/init-prod-user.sh

# Alles starten (Server + MinIO)
docker compose up -d
```

Um die Flutter-Web-App ebenfalls von diesem Host zu servieren, füge das
App-Overlay hinzu:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

`init-prod-user.sh` liest den Subject-DN aus
`deploy/x509/prod/app-subject-dn.txt` und legt einen passenden
`$external`-Nutzer mit `readWrite` und `dbAdmin` auf der `hinata`-Datenbank an,
unter Verwendung des SCRAM-Root-Kontos aus `.env`. Führe es einmal aus, sobald das
Replica Set gesund ist.

## 7. Health prüfen

Der Server stellt einen Health-Endpunkt bereit, den auch der `HEALTHCHECK` des
Containers abfragt:

```bash
curl -fsS https://api.track.example.com/actuator/health
# {"status":"UP"}
```

Lokal, bevor der Proxy verdrahtet ist, erreiche den veröffentlichten Port direkt:

```bash
curl -fsS http://localhost:3356/actuator/health
```

Schau in die Logs, wenn es nicht `UP` ist:

```bash
docker compose logs -f hinata-server
```

Ein häufiger Erststart-Fehler ist die Mongo-Auth — bei
X.509-Authentifizierungsfehlern wurde der `$external`-Nutzer nicht registriert
(führe `./deploy/x509/init-prod-user.sh` erneut aus) oder das Keystore-Passwort in
`.env` passt nicht zu dem, mit dem `hinata-app.p12` gebaut wurde.

## 8. DNS, Reverse Proxy und Ports

Der Server veröffentlicht zwei Host-Ports; dein Reverse Proxy terminiert TLS und
leitet an sie weiter:

| Öffentlicher Name | Zweck | Leitet an Host-Port | Env-Variable |
| --- | --- | --- | --- |
| `api.track.example.com` | REST-API + SSE | `3356` | `HINATA_PORT` |
| `track.example.com` | Flutter-Web-App | `3456` | `HINATA_APP_PORT` |

Zeige beide DNS-Einträge auf den Proxy, stelle Zertifikate aus und proxye jeden
Hostnamen auf seinen Port. Eine minimale Nginx-Skizze (vollständige Konfiguration
unter [Reverse Proxy & TLS](/de/reverse-proxy.html)):

```nginx
location / {
    proxy_pass http://127.0.0.1:3356;   # api.track.example.com → Server
    proxy_set_header Host              $host;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;                # SSE-Streaming erhalten
}
```

Zwei Einstellungen müssen mit deinem Proxy übereinstimmen, damit das Deployment
korrekt und sicher ist:

- **CORS** — `HINATA_CORS_ALLOWED_ORIGINS` muss die Browser-Origin der Web-App
  aufführen (`https://track.example.com`). Der gehostete Web-Client ruft die API
  cross-origin auf, eine fehlende Origin zeigt sich also als blockierte Anfragen im
  Browser.
- **Trusted Proxies** — `HINATA_TRUSTED_PROXIES` ist der CIDR, aus dem der Proxy
  den Container erreicht. Nur von diesen Adressen vertraut der Server
  `X-Forwarded-For`, sodass Rate-Limiting und Logging die echte Client-IP sehen.
  Leer bedeutet niemandem vertrauen; zu weit gesetzt erlaubt Clients, ihre IP zu
  fälschen.

!!! tip "Halte SSE durch den Proxy am Leben"
    Live-Updates nutzen Server-Sent Events. Deaktiviere Response-Buffering an der
    API-Location (`proxy_buffering off;` in Nginx), sonst erhalten Clients Updates
    nicht zeitnah.

## 9. Erststart

Ist der Stack gesund, öffne `https://track.example.com` (oder richte eine native
App auf `https://api.track.example.com`) und schließe den Setup-Assistenten ab, um
die Organisation und den ersten Admin anzulegen. Um dies stattdessen zu
automatisieren — praktisch für Infrastructure-as-Code — setze die
`HINATA_SETUP_*`-Variablen; siehe [Setup & Erststart](/de/setup-wizard.html).

## Aktualisieren und neu ausrollen

Updates sind nur ein neuer Image-Tag. Setze den Tag, ziehe ihn und erzeuge nur
App und Server neu — niemals die Datendienste.

```bash
# Das neue Release in .env pinnen
HINATA_SERVER_TAG=2.3.0
HINATA_APP_TAG=2.3.0

# Die neuen Images ziehen und nur Server + App neu erzeugen
docker compose pull hinata-server
docker compose up -d hinata-server
# falls du auch die Web-App servierst:
docker compose -f docker-compose.yml -f docker-compose.app.yml pull hinata-app
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d hinata-app
```

!!! danger "Ein Redeploy darf nur App + Server aktualisieren — niemals Mongo oder MinIO neu erzeugen"
    Deine Vorgänge, Anhänge und Nutzer liegen in den Docker-Volumes `mongo1-data`,
    `mongo2-data` und `minio-data`. Das Neuerzeugen oder Entfernen der Datenbank-
    oder Storage-Dienste (etwa ein vollständiges `down -v` oder ein Stack-Redeploy,
    der Volumes prunt) **zerstört diese Daten**. Ziele beim Update explizit auf die
    Dienste `hinata-server` und `hinata-app`, wie oben. Erstelle vor jeder Änderung,
    die die Datendienste berührt, ein Backup — siehe
    [Backups & Upgrades](/de/backups.html).

!!! tip "Tags pinnen für reproduzierbare Deployments"
    `latest` ist bequem, verschiebt sich aber unter dir. Pinne `HINATA_SERVER_TAG`
    und `HINATA_APP_TAG` auf eine bestimmte Version (z. B. `{{version}}`), sodass jeder
    Host denselben, bekannten Build ausführt und Rollbacks eine einzeilige
    Tag-Änderung sind.

## Wie es weitergeht

- [Konfigurationsreferenz](/de/configuration.html) — jede Einstellung erklärt.
- [MongoDB & X.509](/de/database.html) — die PKI im Detail, plus Betrieb.
- [Reverse Proxy & TLS](/de/reverse-proxy.html) — vollständige Proxy-Konfigurationen.
- [Backups & Upgrades](/de/backups.html) — Daten über Updates hinweg schützen.
