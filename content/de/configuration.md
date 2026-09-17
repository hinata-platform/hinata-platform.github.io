---
title: Konfigurationsreferenz
description: Alle Umgebungsvariablen von Hinata nach Bereich und wie Einstellungen aus der Datenbank sie überschreiben.
---

# Konfigurationsreferenz

Jede Einstellung eines Hinata-Servers ist eine Umgebungsvariable. Du setzt sie in
`.env` (für Docker Compose) oder direkt am Container. Die Tabellen zeigen je
Bereich den Zweck, einen Standardwert oder ein Beispiel und ob die Variable
Pflicht ist.

SSO, eingehende E-Mails, Push und die OAuth-Apps für Git liegen dagegen in der
Datenbank. Du verwaltest sie im Adminbereich der App. Wie beides zusammenhängt,
steht im letzten Abschnitt.

!!! tip "Alles geht auch ohne `.env`"
    `.env` ist nur ein bequemer Weg für Compose. Jeden Wert kannst du genauso über
    deinen Orchestrator als Umgebungsvariable am Container setzen, mit denselben
    Namen und derselben Bedeutung.

## Kern / URLs

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `SPRING_PROFILES_ACTIVE` | Aktives Profil: `prod` (Replikatset, X.509) oder `dev` (eigenständig) | `prod` | Ja |
| `HINATA_BASE_URL` | Öffentliche Basis-URL der API. Dient als JWT-Aussteller und als Basis für SSO-Redirects | `https://api.track.example.com` | Ja |
| `HINATA_WEB_BASE_URL` | Basis-URL der Flutter-Web-App. E-Mail-Deep-Links zeigen hierher. Leer ⇒ fällt auf die Basis-URL zurück | `https://track.example.com` | Nein |

## Container-Images

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_SERVER_TAG` | Tag von `ghcr.io/hinata-platform/hinata-server`, das ausgeführt wird | `latest` (z. B. `{{version}}` pinnen) | Nein |
| `HINATA_APP_TAG` | Tag von `ghcr.io/hinata-platform/hinata-app` (Web-App als Overlay) | `latest` (z. B. `{{version}}` pinnen) | Nein |

!!! tip
    Pinne im Produktivbetrieb beide Tags auf eine feste Version. Dann läuft auf
    jedem Host derselbe Build, und ein Rollback ist eine einzeilige Änderung.

## Sicherheit / JWT

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_JWT_SECRET` | Signaturschlüssel für HS512, **≥ 64 Zeichen**. Erzeugen: `openssl rand -base64 64 \| tr -d '\n'` | *(leer)* | **Ja (prod)** |

!!! warning
    Im `prod`-Profil startet der Server nicht ohne gültiges `HINATA_JWT_SECRET`.
    Eine Rotation macht alle bestehenden Tokens ungültig.

## MongoDB

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `MONGO_ROOT_USERNAME` | SCRAM-Root-Benutzername (nur intern für die Administration, die App authentifiziert sich per X.509) | `hinata` | Ja |
| `MONGO_ROOT_PASSWORD` | SCRAM-Root-Passwort | `hinata-dev-secret` (ändere es) | **Ja (prod)** |
| `HINATA_MONGODB_URI` | Verbindungszeichenkette für Mongo. In Prod steht die X.509-URI in `docker-compose.yml`. Nur für Dev oder externes Mongo selbst setzen | *(in Compose gesetzt)* | Nein (prod) |
| `HINATA_MONGO_TLS_ENABLED` | TLS für die Verbindung zu Mongo aktivieren | `true` (prod, in Compose) | Nein |
| `HINATA_MONGO_TLS_KEYSTORE` | Pfad zum PKCS#12-Client-Keystore der App im Container | `/etc/hinata/x509/hinata-app.p12` | Nein (prod, in Compose) |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | Passwort für den Client-Keystore | `changeit` (ändere es) | **Ja (prod)** |
| `HINATA_MONGO_TLS_TRUSTSTORE` | Pfad zum CA-Truststore im Container | `/etc/hinata/x509/truststore.p12` | Nein (prod, in Compose) |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | Passwort für den Truststore | `changeit` (ändere es) | **Ja (prod)** |

Wie du die PKI erzeugst und den `$external`-Benutzer registrierst, steht unter
[MongoDB & X.509](/de/database.html).

## Reverse Proxies

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_TRUSTED_PROXIES` | Kommagetrennte CIDRs der Reverse Proxies, die `X-Forwarded-For` setzen dürfen. Leer = keinem vertrauen | `172.16.0.0/12` | Empfohlen |

!!! warning
    Setze hier genau den Adressbereich, aus dem dein Proxy den Container erreicht.

    - Leer: Der Server ignoriert weitergeleitete Header. Rate Limiting und Logs
      sehen nur die IP des Proxys.
    - Zu weit: Clients können ihre Quell-IP fälschen.

## SMTP (ausgehende Mail)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_SMTP_HOST` | Host des SMTP-Relays | `smtp.example.com` (`mailpit` in Dev) | Ja (für Mail) |
| `HINATA_SMTP_PORT` | SMTP-Port | `587` (`1025` für Mailpit) | Ja (für Mail) |
| `HINATA_SMTP_USERNAME` | Benutzername für SMTP-Auth | *(leer)* | Wenn Auth |
| `HINATA_SMTP_PASSWORD` | Passwort für SMTP-Auth | *(leer)* | Wenn Auth |
| `HINATA_SMTP_AUTH` | SMTP-Authentifizierung aktivieren | `true` (`false` in Dev) | Nein |
| `HINATA_SMTP_STARTTLS` | STARTTLS aktivieren | `true` (`false` in Dev) | Nein |
| `HINATA_MAIL_FROM` | Absenderadresse ausgehender Mails | `hinata@example.com` | Ja (für Mail) |

E-Mails mit Deep Links (Verifizierung, Passwort zurücksetzen,
Zuweisungsbenachrichtigungen) kommen nur mit einem echten Relay an. Siehe
[E-Mail & SMTP](/de/email.html).

## Objektspeicher (S3 / MinIO / GCS / Azure)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_STORAGE_PROVIDER` | Backend: `s3` (MinIO, AWS S3, GCS per Interop, R2, Spaces, …) oder `azure` (Azure Blob Storage) | `s3` | Nein |
| `COMPOSE_PROFILES` | `local-storage` betreibt das mitgelieferte MinIO. Leer bei externem Speicher | `local-storage` | Nein |
| `MINIO_ROOT_USER` | MinIO-Root-Benutzer (in Compose auch als S3 Access Key genutzt) | `hinata` | Mit mitgeliefertem MinIO |
| `MINIO_ROOT_PASSWORD` | MinIO-Root-Passwort (in Compose auch als S3 Secret Key genutzt) | `hinata-dev-secret` (ändere es) | **Mit mitgeliefertem MinIO (prod)** |
| `HINATA_S3_ENDPOINT` | S3-Endpunkt, mit dem der Server spricht | `http://minio:9000` (in Compose) | Externes S3 |
| `HINATA_S3_ACCESS_KEY` | S3 Access Key (Dev / externes S3) | `hinata` | Dev / extern |
| `HINATA_S3_SECRET_KEY` | S3 Secret Key (Dev / externes S3) | `hinata-dev-secret` | Dev / extern |
| `HINATA_S3_BUCKET` | Bucket (S3) oder Container (Azure) für Anhänge und Avatare | `hinata` | Nein |
| `HINATA_S3_REGION` | Region des Buckets (AWS und Anbieter mit Regionen) | `us-east-1` | Externes S3 |
| `HINATA_S3_ADDRESSING_STYLE` | Adressierung der S3-URLs: `auto`, `virtual-host` oder `path` | `auto` | Nein |
| `HINATA_AZURE_CONNECTION_STRING` | Connection String des Azure-Speicherkontos (bei `provider=azure`) | *(leer)* | Azure |

Im Compose für den Produktivbetrieb fallen `HINATA_S3_ACCESS_KEY` /
`HINATA_S3_SECRET_KEY` automatisch auf `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`
zurück. Die Einrichtung je Anbieter (AWS, GCS, Azure, R2, …) steht unter
[Objektspeicher](/de/storage.html).

## App-Integration

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_PRIVACY_POLICY_URL` | URL der Datenschutzerklärung in der App (Pflicht für Store-Releases) | `https://example.com/privacy` | Empfohlen |
| `HINATA_APP_MIN_VERSION` | Mindestversion der App. Ältere Clients müssen updaten | `1.0.0` | Nein |
| `HINATA_CORS_ALLOWED_ORIGINS` | Kommagetrennte Browser-Origins, die per CORS zugreifen dürfen (die Web-App ruft von einer anderen Origin auf) | `https://track.example.com` | **Ja (Web)** |
| `HINATA_DOCS_ENABLED` | Die API-Dokumentation mit Scalar freigeben | `false` | Nein |

## Hinata Connect Gateway

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_GATEWAY_BASE_URL` | URL des Gateways für Push und Universal Links. Standard ist das gehostete Gateway. Nur ändern, wenn du eine eigene App unter deiner Marke mit eigenem Gateway ausrollst | `https://connect.hinata.ahmadre.com` | Nein |

Siehe [Hinata Connect Gateway](/de/connect-gateway.html).

## Setup (erster Start)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_SETUP_AUTO_COMPLETE` | Den Einrichtungsassistenten beim ersten Start überspringen | `false` | Nein |
| `HINATA_SETUP_ORGANIZATION_NAME` | Organisationsname (mit Auto-Complete) | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_EMAIL` | E-Mail des ersten Admins | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_USERNAME` | Benutzername des ersten Admins | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_PASSWORD` | Passwort des ersten Admins | *(leer)* | Bei Auto-Complete |
| `HINATA_SETUP_ADMIN_DISPLAY_NAME` | Anzeigename des ersten Admins | *(leer)* | Bei Auto-Complete |

Siehe [Setup & Erststart](/de/setup-wizard.html).

## Demo-Seed (nur Dev)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_DEMO_SEED` | Legt einen realistischen Workspace mit englischen Demodaten an. Login `rebar` / `hinata-demo-2026`. Unter `prod` übersprungen (Seeder ist `@Profile("!prod")`) | `false` | Nein |
| `HINATA_DEMO_RESET` | Löscht den Workspace bei jedem Start und legt ihn neu an. Erfordert `HINATA_DEMO_SEED=true` | `false` | Nein |

!!! danger "Demo-Seed nie im Produktivbetrieb aktivieren"
    Er legt einen Admin mit bekanntem Passwort und Wegwerfdaten an. Unter dem
    `prod`-Profil ist der Seeder herauskompiliert. Setze im Produktivbetrieb
    trotzdem immer `HINATA_DEMO_SEED=false`.

## Rate Limiting / Brute Force

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | Rate Limiting pro IP aktivieren (bucket4j) | `true` | Nein |
| `HINATA_RATE_LIMIT_API` | Allgemeines API-Budget (Anfragen / Minute) | `300` | Nein |
| `HINATA_RATE_LIMIT_AUTH` | Budget für Auth-Endpunkte (Anfragen / Minute) | `10` | Nein |
| `HINATA_MAX_LOGIN_FAILURES` | Fehlgeschlagene Logins, bevor ein Konto blockiert wird | `5` | Nein |
| `HINATA_LOGIN_BLOCK_MINUTES` | Wie lange ein blockiertes Konto gesperrt bleibt (Minuten) | `15` | Nein |

Die Login-Sperre liegt in der Datenbank und übersteht deshalb Neustarts. Siehe
das [Sicherheitsmodell](/de/security.html).

## Ports

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_PORT` | Veröffentlichter Host-Port der API (Container `8080`). Der Reverse Proxy leitet hierher weiter | `3356` | Nein |
| `HINATA_APP_PORT` | Veröffentlichter Host-Port der Web-App (Container `80`) | `3456` | Nein |

## Git-Integration

Plattformweite OAuth-Zugangsdaten, um Projekte mit GitHub, GitLab oder Bitbucket
zu verbinden. Du kannst sie auch zur Laufzeit unter Admin → Git-Integration
setzen. Diese Werte überschreiben die Umgebung. Siehe
[Git-Integration](/de/git-integration.html).

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` | Client-ID der GitHub-OAuth-App | *(leer)* | Wenn GitHub |
| `HINATA_GIT_GITHUB_CLIENT_SECRET` | Client-Secret der GitHub-OAuth-App | *(leer)* | Wenn GitHub |
| `HINATA_GIT_GITLAB_CLIENT_ID` | Client-ID der GitLab-OAuth-App | *(leer)* | Wenn GitLab |
| `HINATA_GIT_GITLAB_CLIENT_SECRET` | Client-Secret der GitLab-OAuth-App | *(leer)* | Wenn GitLab |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` | Consumer Key für Bitbucket OAuth | *(leer)* | Wenn Bitbucket |
| `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Consumer Secret für Bitbucket OAuth | *(leer)* | Wenn Bitbucket |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Öffentliche Basis der API für OAuth-Callback und Webhook-Registrierung. Fällt auf `HINATA_BASE_URL` + `/api/v1` zurück | `https://api.track.example.com/api/v1` | Nein |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM-Schlüssel, der gespeicherte Access Tokens verschlüsselt. **Im Produktivbetrieb den Standard ändern** | *(Standard; ändere es)* | Empfohlen |

## Kalender, Feiertage und Arbeitszeiten

Die Administration pflegt Feiertagskalender im Adminbereich und kann ein Jahr Feiertage aus einer Kalenderadresse importieren, zum Beispiel aus einem Feiertagskalender von Google, Apple oder Outlook. Diese Adresse ruft der Server selbst ab. Mit einer privaten oder Loopback-Adresse verbindet er sich nie, egal was in den Listen unten steht. Arbeitszeiten und Abwesenheiten plant jede Person in ihren Einstellungen. Das alles setzt die erweiterte Zeiterfassung voraus (`HINATA_TIME_TRACKING_ADVANCED_ENABLED`). Siehe [Zeit erfassen](/de/guide-time.html).

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_ICS_SECRET` | Schlüssel, mit dem gespeicherte Kalenderadressen verschlüsselt werden. Base64 von mindestens 32 Bytes. Erzeugen: `openssl rand -base64 32`. Ohne ihn speichert der Server keine Kalenderadresse, und Feiertage lassen sich nur von Hand eintragen | *(leer)* | Für Kalenderadressen |
| `HINATA_ICS_ALLOWED_HOSTS` | Kommagetrennte Hosts, von denen Kalender abgerufen werden dürfen: ein Hostname oder `*.example.org` für dessen Subdomains. Leer heißt jeder öffentliche Host | *(leer)* | Nein |
| `HINATA_ICS_DENIED_HOSTS` | Kommagetrennte Hosts, von denen nie abgerufen wird, in derselben Schreibweise. Wird vor der Erlaubnisliste geprüft | *(leer)* | Nein |
| `HINATA_AVAILABILITY_DEFAULT_WEEKDAY_MINUTES` | Geplante Minuten je Wochentag, beginnend mit Montag, für alle, die keine eigenen Stunden festgelegt haben | `480,480,480,480,480,0,0` | Nein |
| `HINATA_TIME_TRACKING_ABSENCE_MANAGEMENT_ENABLED` | Schaltet die Abwesenheitsverwaltung ein: Arten, Ansprüche und Konten. Setzt die erweiterte Zeiterfassung voraus. Der Schalter unter **Adminbereich → Zeiterfassung** hat Vorrang vor diesem Wert | `false` | Nein |

!!! info "Wer die Abwesenheiten führt"
    Ohne weiteres Zutun führt sie die Administration. Unter **Adminbereich → Zeiterfassung** lassen sich daneben einzelne Personen als **Abwesenheitsverwaltung** benennen — sie pflegen Arten, teilen Ansprüche zu und buchen Korrekturen, ohne sonst Administrationsrechte zu haben. Der Weg dorthin steht in ihren eigenen Einstellungen, nicht im Adminbereich. Die Liste ist bewusst leer voreingestellt: Wer in ihr steht, sieht Krankheitstage als Krankheitstage (Art. 9 DSGVO), und der engere Kreis ist die richtige Vorgabe.

!!! warning "Den Schlüssel aufbewahren"
    Eine Kalenderadresse, die mit einem `HINATA_ICS_SECRET` verschlüsselt wurde, lässt sich mit einem anderen nicht lesen. Ändert sich der Schlüssel, scheitern Importe aus gespeicherten Adressen, bis die Administration die Adresse neu einträgt. Bereits importierte Feiertage bleiben.

## Laufzeiteinstellungen (DB) vs. Umgebung

Hinata hat zwei Konfigurationsebenen.

Umgebungsvariablen (diese Seite) liest der Server beim Start. Sie betreffen
Infrastruktur und Secrets: URLs, JWT-Secret, Verbindung zu Datenbank und
Speicher, TLS, SMTP, Ports, CORS, vertrauenswürdige Proxies und Rate Limits. Für
eine Änderung bearbeitest du `.env` und startest den Container neu.

Laufzeiteinstellungen liegen in MongoDB. Du bearbeitest sie im **Adminbereich**
der App, während der Server läuft:

- **SSO**-Anbieter: OpenID Connect, OAuth 2.0, SAML 2.0, LDAP
  ([SSO](/de/sso.html))
- IMAP-Abruf für **E-Mail → Ticket** ([E-Mail zu Vorgang](/de/email-to-ticket.html))
- **Push** über das Gateway
- OAuth-Zugangsdaten der **Git-Integration** (die `HINATA_GIT_*`-Werte oben)
- **App-Einstellungen** unter Admin → App: `minVersion`, Datenschutz-URL und
  Feature-Flags (`localAuthEnabled`, `registrationEnabled`,
  `requireAdminApproval`)

Dafür gelten drei Regeln:

1. **DB überschreibt Umgebung.** Gibt es eine Einstellung in beiden, gewinnt der
   Wert aus der Datenbank. Das betrifft vor allem die OAuth-Zugangsdaten für Git
   und die App-Einstellungen (`hinata.app.*`). Umgebungswerte sind nur Startwert
   und Rückfall.
2. **Kein Neustart nötig.** Änderungen im Adminbereich wirken sofort, ohne neues
   Deployment.
3. **Secrets sind nur schreibbar.** OAuth-Secrets, Tokens und Passwörter gibt die
   Admin-API nach dem Speichern nie zurück. Du kannst sie setzen oder ersetzen,
   aber nicht lesen.

!!! info "Faustregel"
    Ist es eine Verbindungszeichenkette, ein Transport-Secret oder etwas, das der
    Prozess vor der ersten Anfrage braucht, ist es eine **Umgebungsvariable**.
    Ist es eine Integration, die du im laufenden Betrieb änderst, ist es eine
    **Laufzeiteinstellung** im Adminbereich.
