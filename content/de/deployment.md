---
title: Produktiv-Deployment
description: Hinata Schritt für Schritt produktiv betreiben, mit Docker Compose, X.509-MongoDB, TLS und sicheren Updates.
---

# Produktiv-Deployment

Diese Anleitung führt vom leeren Host bis zur laufenden, geprüften Instanz hinter
deinem Reverse Proxy. Sie nutzt das `prod`-Profil: ein MongoDB-Replica-Set mit TLS
und X.509-Client-Authentifizierung.

Lies vorher den [Überblick zum Selbstbetrieb](/de/self-hosting.html). Was jede
Einstellung bedeutet, steht in der [Konfigurationsreferenz](/de/configuration.html).

## Voraussetzungen

- Ein Linux-Host mit **Docker Engine** und dem **Docker-Compose-Plugin**
  (`docker compose`, v2).
- `openssl`, `keytool` (aus einem JRE/JDK) und eine POSIX-Shell für die Skripte in
  `deploy/`.
- Zwei DNS-Namen: einer für die API, einer für die Web-App. Diese Seite nutzt
  `api.track.example.com` (API) und `track.example.com` (Web).
- Ein Reverse Proxy, der HTTPS terminiert (Nginx, Caddy, Traefik, der Reverse Proxy
  eines NAS …). Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).
- Ein SMTP-Relay für ausgehende Mail. Siehe [E-Mail & SMTP](/de/email.html).

## 1. Das Server-Repository holen

```bash
git clone https://github.com/hinata-platform/hinata-server.git
cd hinata-server
```

Spätere Updates holst du mit `git pull` in diesem Verzeichnis. Die Images kommen
fertig von GHCR, auf dem Host wird nie gebaut.

## 2. Deine .env anlegen

```bash
cp .env.example .env
```

`.env.example` ist vollständig kommentiert. Jeder Wert geht auch als normale
Umgebungsvariable am Container.

## 3. Secrets erzeugen

```bash
./deploy/generate-secrets.sh
```

Das Skript:

- erzeugt `deploy/mongo-keyfile` (das Keyfile für die interne Authentifizierung des
  Replica Sets), falls es noch fehlt.
- gibt Zufallswerte für `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD` und
  `MINIO_ROOT_PASSWORD` aus.

Kopiere die Werte in deine `.env`.

!!! warning "Das JWT-Secret ist in Produktion erforderlich"
    `HINATA_JWT_SECRET` muss ein zufälliger String mit **mindestens 64 Zeichen**
    sein (HS512). Im prod-Profil startet der Server ohne ihn nicht. Ohne Generator
    erzeugst du ihn so:

    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```

    Wer das Secret rotiert, macht alle ausgegebenen Tokens ungültig. Alle Nutzer
    müssen sich dann neu anmelden.

## 4. Die MongoDB-X.509-PKI erzeugen

MongoDB nutzt in Produktion TLS und X.509-Client-Authentifizierung. Im
Connection-String steht deshalb kein Passwort. Erzeuge CA, Server-Zertifikat und
Client-Zertifikat der App:

```bash
./deploy/x509/generate-certs.sh prod
```

Unter `deploy/x509/prod/` entstehen:

- die CA (`ca.crt`/`ca.key`)
- das mongod-Server-Zertifikat (`server.pem`)
- der JVM-Keystore der App (`hinata-app.p12`)
- der Truststore (`truststore.p12`)
- das `keyfile` des Replica Sets
- `app-subject-dn.txt`: der Subject-DN des Client-Zertifikats, er wird zum
  Mongo-Benutzernamen

Keystore und Truststore haben standardmäßig das Passwort `changeit`. Ändere es und
trage die passenden Werte in `.env` ein:

```properties
HINATA_MONGO_TLS_KEYSTORE_PASSWORD=change-me-keystore
HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD=change-me-truststore
```

!!! tip
    Exportiere `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` und
    `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` **vor** dem Zertifikatsgenerator. Dann
    entstehen die PKCS#12-Dateien gleich mit deinen Passwörtern. Startest du ihn
    vorher, bleibt der Standard. Details auf der Seite
    [MongoDB & X.509](/de/database.html).

## 5. Eine realistische .env

Eine typische Produktions-`.env`. Platzhalter heißen `change-me…`. Die Secrets sehen
aus wie vom Generator, deine sind andere. Passe die Hosts an.

```properties
# Profil
SPRING_PROFILES_ACTIVE=prod

# Öffentliche URLs
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com

# Image-Tags (statt latest eine Version pinnen für reproduzierbare Deployments)
HINATA_SERVER_TAG={{version}}
HINATA_APP_TAG={{version}}

# JWT: aus ./deploy/generate-secrets.sh
HINATA_JWT_SECRET=Kf3mS0pQ9xR2vN7wY1bZ8cH4dJ6gL5aT0eU3iO2rW9kP1sX4nC7mB6vD8fA2hQ0

# MongoDB-SCRAM-Root (nur Admin/intern, die App nutzt X.509)
MONGO_ROOT_USERNAME=hinata
MONGO_ROOT_PASSWORD=9f1c7a4e2b6d8039a5c1e7f2b4d6a8c0
HINATA_MONGO_TLS_KEYSTORE_PASSWORD=change-me-keystore
HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD=change-me-truststore

# Reverse Proxy: CIDR, aus dem der Proxy den Container erreicht (siehe Schritt 8)
HINATA_TRUSTED_PROXIES=172.16.0.0/12

# SMTP: ein echtes Relay, damit Mail zugestellt wird
HINATA_SMTP_HOST=smtp.example.com
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.com
HINATA_SMTP_PASSWORD=change-me-smtp
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=hinata@example.com

# Objektspeicher: mitgeliefertes MinIO (setze stattdessen COMPOSE_PROFILES=
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

# Push + Deep-Links: Standard-Gateway; nur überschreiben für ein eigenes
HINATA_GATEWAY_BASE_URL=https://connect.hinata.ahmadre.com

# Erststart (leer lassen, um den In-App-Assistenten zu nutzen)
HINATA_SETUP_AUTO_COMPLETE=false

# Demo-Seed: NIEMALS in Produktion aktivieren
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
    `.env.example` enthält Standardwerte für die Entwicklung:
    `MONGO_ROOT_PASSWORD=hinata-dev-secret`, `changeit` als Keystore-Passwort und
    ein leeres JWT-Secret. Jeder davon ist in Produktion eine ernste Lücke. Erzeuge
    überall echte Secrets.

## 6. Den Stack starten

Starte zuerst MongoDB. So kann das Replica Set initialisieren und du registrierst
den X.509-Nutzer. Danach startest du den Rest.

```bash
# Datenbank-Knoten starten
docker compose up -d mongo1 mongo2 mongo-arbiter

# Das Client-Zertifikat der App als $external-Mongo-Nutzer registrieren
./deploy/x509/init-prod-user.sh

# Alles starten (Server + MinIO)
docker compose up -d
```

Soll dieser Host auch die Flutter-Web-App ausliefern, nimm das App-Overlay dazu:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

`init-prod-user.sh` liest den Subject-DN aus `deploy/x509/prod/app-subject-dn.txt`.
Mit dem SCRAM-Root-Konto aus `.env` legt es einen passenden `$external`-Nutzer mit
`readWrite` und `dbAdmin` auf der Datenbank `hinata` an. Führe es einmal aus, sobald
das Replica Set gesund ist.

## 7. Health prüfen

Diesen Endpunkt fragt auch der `HEALTHCHECK` des Containers ab:

```bash
curl -fsS https://api.track.example.com/actuator/health
# {"status":"UP"}
```

Solange der Proxy noch fehlt, prüfst du den Port direkt:

```bash
curl -fsS http://localhost:3356/actuator/health
```

Ist der Status nicht `UP`, schau in die Logs:

```bash
docker compose logs -f hinata-server
```

Beim ersten Start scheitert oft die Mongo-Authentifizierung. Bei X.509-Fehlern gibt
es zwei übliche Ursachen:

- Der `$external`-Nutzer wurde nicht registriert. Führe
  `./deploy/x509/init-prod-user.sh` erneut aus.
- Das Keystore-Passwort in `.env` passt nicht zu dem, mit dem `hinata-app.p12`
  gebaut wurde.

## 8. DNS, Reverse Proxy und Ports

Der Server veröffentlicht zwei Host-Ports. Dein Reverse Proxy terminiert TLS und
leitet dorthin weiter:

| Öffentlicher Name | Zweck | Leitet an Host-Port | Env-Variable |
| --- | --- | --- | --- |
| `api.track.example.com` | REST-API + SSE | `3356` | `HINATA_PORT` |
| `track.example.com` | Flutter-Web-App | `3456` | `HINATA_APP_PORT` |

Richte beide DNS-Einträge auf den Proxy, stelle Zertifikate aus und leite jeden
Hostnamen auf seinen Port. Eine minimale Nginx-Skizze (vollständig unter
[Reverse Proxy & TLS](/de/reverse-proxy.html)):

```nginx
location / {
    proxy_pass http://127.0.0.1:3356;   # api.track.example.com → Server
    proxy_set_header Host              $host;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;                # SSE-Streaming erhalten
}
```

Zwei Einstellungen müssen zu deinem Proxy passen:

- **CORS**: `HINATA_CORS_ALLOWED_ORIGINS` muss die Origin der Web-App enthalten
  (`https://track.example.com`). Der Web-Client ruft die API cross-origin auf. Fehlt
  die Origin, blockiert der Browser die Anfragen.
- **Trusted Proxies**: `HINATA_TRUSTED_PROXIES` ist der CIDR, aus dem der Proxy den
  Container erreicht. Nur Adressen daraus glaubt der Server `X-Forwarded-For`. So
  sehen Rate-Limiting und Logs die echte Client-IP. Leer heißt, niemandem zu
  vertrauen. Ist der Bereich zu weit, können Clients ihre IP fälschen.

!!! tip "Halte SSE durch den Proxy am Leben"
    Live-Updates nutzen Server-Sent Events. Schalte das Response-Buffering an der
    API-Location ab (`proxy_buffering off;` in Nginx), sonst kommen Updates
    verspätet an.

## 9. Erststart

Ist der Stack gesund, öffne `https://track.example.com` (oder richte eine native App
auf `https://api.track.example.com`). Der Setup-Assistent legt die Organisation und
den ersten Admin an. Automatisieren kannst du das, etwa für Infrastructure as Code,
über die `HINATA_SETUP_*`-Variablen. Siehe [Setup & Erststart](/de/setup-wizard.html).

## Aktualisieren und neu ausrollen

Ein Update ist ein neuer Image-Tag. Setze den Tag, zieh die Images und erzeuge nur
App und Server neu. Die Datendienste fasst du nicht an.

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

!!! danger "Ein Redeploy aktualisiert nur App und Server, niemals Mongo oder MinIO"
    Vorgänge, Anhänge und Nutzer liegen in den Docker-Volumes `mongo1-data`,
    `mongo2-data` und `minio-data`. Werden Datenbank oder Speicher neu erzeugt oder
    entfernt (etwa per `down -v` oder durch ein Stack-Redeploy, das Volumes
    löscht), sind **diese Daten zerstört**. Nenne beim Update deshalb ausdrücklich
    die Dienste `hinata-server` und `hinata-app`, wie oben. Mach vor jeder Änderung
    an den Datendiensten ein Backup. Siehe [Backups & Upgrades](/de/backups.html).

!!! tip "Tags pinnen für reproduzierbare Deployments"
    `latest` ist bequem, ändert sich aber ohne dein Zutun. Pinne
    `HINATA_SERVER_TAG` und `HINATA_APP_TAG` auf eine feste Version (z. B.
    `{{version}}`). Dann läuft auf jedem Host derselbe bekannte Build, und ein
    Rollback ist eine geänderte Zeile.

## Wie es weitergeht

- [Konfigurationsreferenz](/de/configuration.html): jede Einstellung erklärt.
- [MongoDB & X.509](/de/database.html): die PKI im Detail und der Betrieb.
- [Reverse Proxy & TLS](/de/reverse-proxy.html): vollständige Proxy-Konfigurationen.
- [Backups & Upgrades](/de/backups.html): Daten über Updates hinweg schützen.
