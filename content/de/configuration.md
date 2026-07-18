---
title: Konfigurationsreferenz
description: Die maßgebliche Referenz für jede Hinata-Umgebungsvariable, gruppiert nach Bereich, sowie wie Laufzeiteinstellungen aus der Datenbank die Umgebung überschreiben.
---

# Konfigurationsreferenz

Dies ist die vollständige Referenz zur Konfiguration eines Hinata-Servers. Jede
Einstellung ist eine Umgebungsvariable — gelesen aus `.env` (über Docker Compose)
oder direkt am Container gesetzt. Nachfolgend sind sie nach Bereich gruppiert, mit
Zweck, einem Standardwert oder Beispiel und ob die Variable erforderlich ist.

Eine zweite Klasse von Einstellungen — SSO, E-Mail-Ingest, Push, Git-OAuth-Apps —
liegt in der Datenbank und wird aus dem Adminbereich der App verwaltet. Der letzte
Abschnitt erklärt, wie die beiden zusammenhängen.

!!! tip "Alles kann eine einfache Umgebungsvariable sein"
    `.env` ist nur ein bequemes Laden für Compose. Jeder Wert hier kann ebenso als
    Umgebungsvariable am Container durch deinen Orchestrator gesetzt werden. Namen und
    Semantik sind identisch.

## Kern / URLs

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `SPRING_PROFILES_ACTIVE` | Aktives Profil: `prod` (Replikatset, X.509) oder `dev` (eigenständig) | `prod` | Ja |
| `HINATA_BASE_URL` | Öffentliche API-Basis-URL — JWT-Aussteller und SSO-Redirect-Basis | `https://api.track.example.com` | Ja |
| `HINATA_WEB_BASE_URL` | Flutter-Web-Basis-URL; E-Mail-Deep-Links zeigen hierher. Leer ⇒ fällt auf die Basis-URL zurück | `https://track.example.com` | Nein |

## Container-Images

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_SERVER_TAG` | Tag von `ghcr.io/hinata-platform/hinata-server`, das ausgeführt wird | `latest` (z. B. `{{version}}` pinnen) | Nein |
| `HINATA_APP_TAG` | Tag von `ghcr.io/hinata-platform/hinata-app` (Web-App-Overlay) | `latest` (z. B. `{{version}}` pinnen) | Nein |

!!! tip
    Pinne beide Tags im Produktivbetrieb auf eine bestimmte Version, damit jeder Host
    denselben Build ausführt und Rollbacks eine einzeilige Änderung sind.

## Sicherheit / JWT

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_JWT_SECRET` | HS512-Signaturschlüssel, **≥ 64 Zeichen**. Erzeugen: `openssl rand -base64 64 \| tr -d '\n'` | *(leer)* | **Ja (prod)** |

!!! warning
    Der Server startet im `prod`-Profil nicht ohne ein gültiges
    `HINATA_JWT_SECRET`. Eine Rotation macht alle bestehenden Tokens ungültig.

## MongoDB

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `MONGO_ROOT_USERNAME` | SCRAM-Root-Benutzername (nur intern/administrativ; die App authentifiziert sich mit X.509) | `hinata` | Ja |
| `MONGO_ROOT_PASSWORD` | SCRAM-Root-Passwort | `hinata-dev-secret` (ändere es) | **Ja (prod)** |
| `HINATA_MONGODB_URI` | Mongo-Verbindungszeichenkette. In Prod ist sie in `docker-compose.yml` auf die X.509-URI gesetzt; setze sie nur für Dev / externes Mongo explizit | *(in Compose gesetzt)* | Nein (prod) |
| `HINATA_MONGO_TLS_ENABLED` | TLS für die Mongo-Verbindung aktivieren | `true` (prod, in Compose) | Nein |
| `HINATA_MONGO_TLS_KEYSTORE` | Pfad zum PKCS#12-Client-Keystore der App im Container | `/etc/hinata/x509/hinata-app.p12` | Nein (prod, in Compose) |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | Passwort für den Client-Keystore | `changeit` (ändere es) | **Ja (prod)** |
| `HINATA_MONGO_TLS_TRUSTSTORE` | Pfad zum CA-Truststore im Container | `/etc/hinata/x509/truststore.p12` | Nein (prod, in Compose) |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | Passwort für den Truststore | `changeit` (ändere es) | **Ja (prod)** |

Siehe [MongoDB & X.509](/de/database.html) dafür, wie die PKI erzeugt und der
`$external`-Benutzer registriert wird.

## Reverse Proxies

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_TRUSTED_PROXIES` | Kommagetrennte CIDRs von Reverse Proxies, die `X-Forwarded-For` setzen dürfen. Leer = keinem vertrauen | `172.16.0.0/12` | Empfohlen |

!!! warning
    Setze dies auf genau den Adressbereich, aus dem dein Proxy den Container erreicht.
    Leer bedeutet, dass der Server weitergeleitete Header ignoriert (Rate Limiting /
    Logging sehen die Proxy-IP); zu weit gefasst erlaubt Clients, ihre Quell-IP zu fälschen.

## SMTP (ausgehende Mail)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_SMTP_HOST` | SMTP-Relay-Host | `smtp.example.com` (`mailpit` in Dev) | Ja (für Mail) |
| `HINATA_SMTP_PORT` | SMTP-Port | `587` (`1025` für Mailpit) | Ja (für Mail) |
| `HINATA_SMTP_USERNAME` | SMTP-Auth-Benutzername | *(leer)* | Wenn Auth |
| `HINATA_SMTP_PASSWORD` | SMTP-Auth-Passwort | *(leer)* | Wenn Auth |
| `HINATA_SMTP_AUTH` | SMTP-Authentifizierung aktivieren | `true` (`false` in Dev) | Nein |
| `HINATA_SMTP_STARTTLS` | STARTTLS aktivieren | `true` (`false` in Dev) | Nein |
| `HINATA_MAIL_FROM` | Absenderadresse ausgehender Mail | `hinata@example.com` | Ja (für Mail) |

Deep-Link-E-Mails (Verifizierung, Passwort-Reset, Zuweisungsbenachrichtigungen) werden
nur mit einem echten Relay zugestellt. Siehe [E-Mail & SMTP](/de/email.html).

## Objektspeicher (S3 / MinIO / GCS / Azure)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_STORAGE_PROVIDER` | Backend: `s3` (MinIO, AWS S3, GCS-Interop, R2, Spaces, …) oder `azure` (Azure Blob Storage) | `s3` | Nein |
| `COMPOSE_PROFILES` | `local-storage` betreibt das mitgelieferte MinIO; leer bei externem Speicher | `local-storage` | Nein |
| `MINIO_ROOT_USER` | MinIO-Root-Benutzer (in Compose auch als S3-Access-Key verwendet) | `hinata` | Mit mitgeliefertem MinIO |
| `MINIO_ROOT_PASSWORD` | MinIO-Root-Passwort (in Compose auch als S3-Secret-Key) | `hinata-dev-secret` (ändere es) | **Mit mitgeliefertem MinIO (prod)** |
| `HINATA_S3_ENDPOINT` | S3-Endpunkt, mit dem der Server spricht | `http://minio:9000` (in Compose) | Externes S3 |
| `HINATA_S3_ACCESS_KEY` | S3-Access-Key (Dev / externes S3) | `hinata` | Dev / extern |
| `HINATA_S3_SECRET_KEY` | S3-Secret-Key (Dev / externes S3) | `hinata-dev-secret` | Dev / extern |
| `HINATA_S3_BUCKET` | Bucket (S3) / Container (Azure) für Anhänge und Avatare | `hinata` | Nein |
| `HINATA_S3_REGION` | Bucket-Region (AWS und regionssensible Anbieter) | `us-east-1` | Externes S3 |
| `HINATA_S3_ADDRESSING_STYLE` | S3-URL-Adressierung: `auto`, `virtual-host` oder `path` | `auto` | Nein |
| `HINATA_AZURE_CONNECTION_STRING` | Connection String des Azure-Speicherkontos (bei `provider=azure`) | — | Azure |

Im Produktiv-Compose fallen `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` automatisch auf
`MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` zurück. Siehe
[Objektspeicher](/de/storage.html) für die Einrichtung je Anbieter (AWS, GCS, Azure, R2, …).

## App-Integration

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_PRIVACY_POLICY_URL` | In der App angezeigte URL der Datenschutzerklärung (erforderlich für Store-Releases) | `https://example.com/privacy` | Empfohlen |
| `HINATA_APP_MIN_VERSION` | Mindest-App-Version; ältere Clients werden zum Update gezwungen | `1.0.0` | Nein |
| `HINATA_CORS_ALLOWED_ORIGINS` | Kommagetrennte Browser-Origins, die für CORS erlaubt sind (die Web-App ruft cross-origin auf) | `https://track.example.com` | **Ja (Web)** |
| `HINATA_DOCS_ENABLED` | Die Scalar-API-Docs-Oberfläche freigeben | `false` | Nein |

## Hinata Connect Gateway

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Push- + Universal-Link-Gateway-URL. Standard ist das gehostete Gateway; überschreibe dies nur, wenn du deine eigene gebrandete App mit eigenem Gateway ausrollst | `https://connect.hinata.ahmadre.com` | Nein |

Siehe [Hinata Connect Gateway](/de/connect-gateway.html).

## Setup (erster Start)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_SETUP_AUTO_COMPLETE` | Den In-App-Erststart-Assistenten überspringen | `false` | Nein |
| `HINATA_SETUP_ORGANIZATION_NAME` | Organisationsname (mit Auto-Complete) | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_EMAIL` | E-Mail des ersten Admins | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_USERNAME` | Benutzername des ersten Admins | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_PASSWORD` | Passwort des ersten Admins | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_DISPLAY_NAME` | Anzeigename des ersten Admins | *(leer)* | Bei Auto-Complete |

Siehe [Setup & Erststart](/de/setup-wizard.html).

## Demo-Seed (nur Dev)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_DEMO_SEED` | Einen realistischen englischen Demo-Workspace anlegen. Login `rebar` / `hinata-demo-2026`. Unter `prod` übersprungen (Seeder ist `@Profile("!prod")`) | `false` | Nein |
| `HINATA_DEMO_RESET` | Den Workspace bei jedem Start löschen und neu anlegen. Erfordert `HINATA_DEMO_SEED=true` | `false` | Nein |

!!! danger "Aktiviere den Demo-Seed niemals im Produktivbetrieb"
    Er erstellt einen Admin mit bekanntem Passwort und Wegwerfdaten. Der Seeder wird
    unter dem `prod`-Profil herauskompiliert, halte `HINATA_DEMO_SEED=false` im
    Produktivbetrieb dennoch unabhängig davon.

## Rate Limiting / Brute Force

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | Rate Limiting pro IP aktivieren (bucket4j) | `true` | Nein |
| `HINATA_RATE_LIMIT_API` | Allgemeines API-Budget (Anfragen / Minute) | `300` | Nein |
| `HINATA_RATE_LIMIT_AUTH` | Budget für Auth-Endpunkte (Anfragen / Minute) | `10` | Nein |
| `HINATA_MAX_LOGIN_FAILURES` | Fehlgeschlagene Logins, bevor ein Konto blockiert wird | `5` | Nein |
| `HINATA_LOGIN_BLOCK_MINUTES` | Wie lange ein blockiertes Konto gesperrt bleibt (Minuten) | `15` | Nein |

Login-Blockierung ist datenbankgestützt und übersteht daher Neustarts. Siehe das
[Sicherheitsmodell](/de/security.html).

## Ports

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_PORT` | Veröffentlichter Host-Port für die API (Container `8080`); der Reverse Proxy leitet hierher weiter | `3356` | Nein |
| `HINATA_APP_PORT` | Veröffentlichter Host-Port für die Web-App (Container `80`) | `3456` | Nein |

## Git-Integration

Plattformweite OAuth-Zugangsdaten zum Verbinden von Projekten mit GitHub / GitLab /
Bitbucket. Diese können auch zur Laufzeit unter Admin → Git-Integration gesetzt werden
(was die Umgebung überschreibt). Siehe [Git-Integration](/de/git-integration.html).

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` | GitHub-OAuth-App-Client-ID | *(leer)* | Wenn GitHub |
| `HINATA_GIT_GITHUB_CLIENT_SECRET` | GitHub-OAuth-App-Client-Secret | *(leer)* | Wenn GitHub |
| `HINATA_GIT_GITLAB_CLIENT_ID` | GitLab-OAuth-App-Client-ID | *(leer)* | Wenn GitLab |
| `HINATA_GIT_GITLAB_CLIENT_SECRET` | GitLab-OAuth-App-Client-Secret | *(leer)* | Wenn GitLab |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` | Bitbucket-OAuth-Consumer-Key | *(leer)* | Wenn Bitbucket |
| `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Bitbucket-OAuth-Consumer-Secret | *(leer)* | Wenn Bitbucket |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Öffentliche API-Basis für den OAuth-Callback und die Webhook-Registrierung. Fällt auf `HINATA_BASE_URL` + `/api/v1` zurück | `https://api.track.example.com/api/v1` | Nein |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM-Schlüssel, der gespeicherte Access-Tokens im Ruhezustand verschlüsselt — **ändere den Standard im Produktivbetrieb** | *(Standard; ändere es)* | Empfohlen |

## Laufzeiteinstellungen (DB) vs. Umgebung

Hinata hat zwei Konfigurationsebenen, und es ist wichtig zu wissen, welche wo liegt.

**Umgebungsvariablen (diese Seite)** werden beim Start gelesen. Sie decken
Infrastruktur und Secrets ab: URLs, das JWT-Secret, Datenbank- und Speicherverbindung,
TLS, SMTP-Transport, Ports, CORS, vertrauenswürdige Proxies, Rate Limits. Eine zu
ändern bedeutet, `.env` zu bearbeiten und den Container neu zu starten.

**Laufzeiteinstellungen** sind in MongoDB gespeichert und werden aus dem
**Adminbereich** der App bearbeitet, während der Server läuft. Sie decken
Integrationen ab, die du betrieblich anpasst:

- **SSO**-Anbieter — OpenID Connect, OAuth 2.0, SAML 2.0, LDAP
  ([SSO](/de/sso.html)).
- **E-Mail → Ticket** IMAP-Ingestion ([E-Mail zu Vorgang](/de/email-to-ticket.html)).
- **Push**-Konfiguration über das Gateway.
- **Git-Integration** OAuth-App-Zugangsdaten (die `HINATA_GIT_*`-Werte oben).
- **App-Einstellungen** — `minVersion`, Datenschutz-URL und Feature-Flags
  (`localAuthEnabled`, `registrationEnabled`, `requireAdminApproval`), bearbeitbar
  unter Admin → App.

Drei Regeln bestimmen die beiden Ebenen:

1. **DB überschreibt Umgebung.** Wo eine Einstellung in beiden existiert — insbesondere
   Git-OAuth-Zugangsdaten und die App-Einstellungen (`hinata.app.*`) — gewinnt der in der
   Datenbank gespeicherte Wert. Umgebungswerte fungieren als anfänglicher Standard /
   Fallback.
2. **Änderungen greifen ohne Neustart.** Das Bearbeiten einer Laufzeiteinstellung im
   Adminbereich wird sofort wirksam; du deployst nicht neu.
3. **Secrets sind nur schreibbar.** Secret-Felder in der Admin-API (OAuth-Secrets,
   Tokens, Passwörter) werden nach dem Speichern nie zurückgegeben — du kannst sie setzen
   oder ersetzen, aber nicht lesen.

!!! info "Faustregel"
    Wenn es eine Verbindungszeichenkette, ein Transport-Secret oder etwas ist, das der
    Prozess braucht, bevor er eine Anfrage bedienen kann, ist es eine
    **Umgebungsvariable**. Wenn es eine Integration ist, die du auf einem laufenden
    System neu konfigurieren würdest, ist es eine **Laufzeiteinstellung** im Adminbereich.
