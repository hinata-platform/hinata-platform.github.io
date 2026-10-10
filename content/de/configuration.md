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

## Objektspeicher (S3 / SeaweedFS / GCS / Azure)

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_STORAGE_PROVIDER` | Backend: `s3` (SeaweedFS, AWS S3, GCS per Interop, R2, Spaces, …) oder `azure` (Azure Blob Storage) | `s3` | Nein |
| `COMPOSE_PROFILES` | `local-storage` betreibt das mitgelieferte SeaweedFS. Leer bei externem Speicher | `local-storage` | Nein |
| `HINATA_S3_ENDPOINT` | S3-Endpunkt, mit dem der Server spricht | `http://seaweedfs:8333` (in Compose) | Externes S3 |
| `HINATA_S3_ACCESS_KEY` | S3 Access Key. Das mitgelieferte SeaweedFS richtet aus diesem und dem Secret Key die Identität des Servers ein | `hinata` | Bei S3 |
| `HINATA_S3_SECRET_KEY` | S3 Secret Key | *(aus `generate-secrets.sh`)* | Bei S3 |
| `HINATA_S3_BUCKET` | Bucket (S3) oder Container (Azure) für Anhänge und Avatare | `hinata` | Nein |
| `HINATA_S3_REGION` | Region des Buckets (AWS und Anbieter mit Regionen) | `us-east-1` | Externes S3 |
| `HINATA_S3_ADDRESSING_STYLE` | Adressierung der S3-URLs: `auto`, `virtual-host` oder `path`. Der mitgelieferte Speicher braucht `path`, externe meist `auto` | `path` (in Compose), `auto` (Standard des Servers) | Nein |
| `HINATA_S3_SSE` | Serverseitige Verschlüsselung, die für jedes geschriebene oder kopierte Objekt verlangt wird: `AES256` (SSE-S3) oder leer. Jeder andere Wert hält den Server beim Start an | `AES256` (in `.env.example`) | Mit mitgeliefertem SeaweedFS |
| `HINATA_AZURE_CONNECTION_STRING` | Connection String des Azure-Speicherkontos (bei `provider=azure`) | *(leer)* | Azure |
| `SEAWEEDFS_ADMIN_ACCESS_KEY` / `SEAWEEDFS_ADMIN_SECRET_KEY` | Admin-Identität des mitgelieferten SeaweedFS. Nur der Job `seaweedfs-setup` nutzt sie | `hinata-admin` / *(erzeugt)* | Mit mitgeliefertem SeaweedFS |
| `SEAWEEDFS_SSE_KEK` | Schlüssel, der jedes Objekt im mitgelieferten SeaweedFS verschlüsselt (64 Hex-Zeichen). **Bewahre eine Kopie getrennt vom Server auf.** Ohne ihn lässt sich nichts Gespeichertes mehr lesen | *(erzeugt)* | Mit mitgeliefertem SeaweedFS |
| `SEAWEEDFS_JWT_VOLUME_WRITE` / `_VOLUME_READ` / `_FILER_WRITE` / `_FILER_READ` | Schlüssel, die Anfragen zwischen den Teilen von SeaweedFS signieren | *(erzeugt)* | Mit mitgeliefertem SeaweedFS |
| `SEAWEEDFS_BACKUP_ACCESS_KEY` / `SEAWEEDFS_BACKUP_SECRET_KEY` | Optionale Nur-Lese-Identität für Backups. Die mitgelieferte Compose-Datei reicht sie nicht an den Container weiter, siehe [Backups & Upgrades](/de/backups.html) | *(leer)* | Nein |

SeaweedFS startet nicht, solange einer seiner Schlüssel fehlt. `./deploy/generate-secrets.sh`
gibt für jedes Geheimnis einen frischen Wert aus. Das mitgelieferte SeaweedFS, die
Einrichtung je Anbieter (AWS, GCS, Azure, R2, …) und den Umzug von MinIO beschreibt
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
| `HINATA_RATE_LIMIT_REFRESH` | Budget für das Erneuern eines Zugangstokens (Anfragen / Minute). Eigenes Budget, weil das Vorzeigen eines Tokens, das dieser Server signiert hat, kein Rateversuch auf ein Passwort ist — und weil sich alle Clients hinter einer Adresse das Anmelde-Budget teilen | `60` | Nein |
| `HINATA_RATE_LIMIT_SSO` | Budget für die beiden Weiterleitungen einer Single-Sign-on-Anmeldung (Anfragen / Minute). Eigenes Budget, weil ein ganzes Büro hinter einer Adresse sich darüber anmeldet, die Callback-Adresse aber jeder erreicht | `60` | Nein |
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

Organisationsadmins pflegen Feiertagskalender auf der Seite [Organisation](/de/organization.html). Ein Kalender folgt den gesetzlichen Feiertagen einer Region, die der Server selbst kennt, oder liest eine Kalenderadresse, zum Beispiel einen Feiertagskalender von Google, Apple oder Outlook. Beide füllen jedes Jahr von selbst, siehe [Feiertage](/de/organization.html#feiertage). Welche Region die Organisation zu Beginn bekommt, stellen Admins unter **Adminbereich → Allgemein → Feiertage der Plattform** ein; ohne Angabe gilt das Land der Zeitzone des Servers. Ist der Kalender-Import eingeschaltet, können Personen außerdem ihre eigenen Kalender abonnieren und Termine als Zeiteinträge übernehmen (siehe [Zeit erfassen](/de/guide-time.html#deine-eigenen-kalender)). Jede dieser Adressen ruft der Server selbst ab. Mit einer privaten oder Loopback-Adresse verbindet er sich nie, egal was in den Listen unten steht. Die Arbeitszeiten plant jede Person in ihren Einstellungen, die Abwesenheiten in der Zeiterfassung. Das alles setzt die erweiterte Zeiterfassung voraus (`HINATA_TIME_TRACKING_ADVANCED_ENABLED`). Siehe [Zeit erfassen](/de/guide-time.html).

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_HOLIDAYS_AUTO_FILL` | Füllt jede Nacht und bei jedem Start das laufende und das nächste Jahr jedes Feiertagskalenders mit Region oder Kalenderadresse, jedes Jahr nur einmal. Mit `false` werden Kalenderadressen nur noch auf Knopfdruck gelesen; ein Kalender mit Region füllt sich beim Speichern trotzdem | `true` | Nein |
| `HINATA_ICS_SECRET` | Schlüssel, mit dem gespeicherte Kalenderadressen verschlüsselt werden (AES-256-GCM), sowohl Feiertagsquellen als auch persönliche Kalender-Abos. Base64 von mindestens 32 Bytes. Erzeugen: `openssl rand -base64 32`. Ohne ihn, oder mit einem kürzeren oder ungültigen Wert, speichert der Server keine Kalenderadresse: Feiertage lassen sich nur von Hand eintragen, und niemand kann einen Kalender abonnieren. **Einmal gesetzt, nie mehr ändern** | *(leer)* | Für Kalenderadressen |
| `HINATA_ICS_ALLOWED_HOSTS` | Kommagetrennte Hosts, von denen Kalender abgerufen werden dürfen: ein Hostname oder `*.example.org` für dessen Subdomains. Leer heißt jeder öffentliche Host | *(leer)* | Nein |
| `HINATA_ICS_DENIED_HOSTS` | Kommagetrennte Hosts, von denen nie abgerufen wird, in derselben Schreibweise. Wird vor der Erlaubnisliste geprüft | *(leer)* | Nein |
| `HINATA_TIME_TRACKING_ICS_IMPORT_ENABLED` | Erlaubt Personen, ihre eigenen Kalender zu abonnieren und Termine als Einträge zu übernehmen. Setzt die erweiterte Zeiterfassung und `HINATA_ICS_SECRET` voraus. Der Schalter **Kalender-Import** unter **Organisation → Zeiterfassung** hat Vorrang vor diesem Wert | `false` | Nein |
| `HINATA_AVAILABILITY_DEFAULT_WEEKDAY_MINUTES` | Geplante Minuten je Wochentag, beginnend mit Montag, für alle, die keine eigenen Stunden festgelegt haben | `480,480,480,480,480,0,0` | Nein |
| `HINATA_TIME_TRACKING_ABSENCE_MANAGEMENT_ENABLED` | Schaltet die Abwesenheitsverwaltung ein: Arten, Ansprüche, Konten, Anträge und Krankmeldungen. Setzt die erweiterte Zeiterfassung voraus. Der Schalter unter **Organisation → Zeiterfassung** hat Vorrang vor diesem Wert | `false` | Nein |
| `HINATA_TIME_TRACKING_ABSENCE_CALENDAR_VISIBILITY` | Der Team-Abwesenheitskalender: `OFF`, `BUSY_ONLY` (nur, dass jemand abwesend ist) oder `TYPE` (die Art, Krankheit nie). Wirkt nur mit eingeschalteter Abwesenheitsverwaltung. Die Auswahl unter **Organisation → Zeiterfassung** hat Vorrang vor diesem Wert | `OFF` | Nein |
| `HINATA_TIME_TRACKING_WORKLOAD_REPORTS_ENABLED` | Schaltet den Auslastungsbericht unter **Zeiterfassung → Berichte** ein: Kapazität gegen gebuchte Zeit je Person, nur für Organisationsadmins und Projektleitungen. Setzt die erweiterte Zeiterfassung voraus. Der Schalter unter **Organisation → Zeiterfassung** hat Vorrang vor diesem Wert. Siehe [Datenschutz der Zeiterfassung](/de/time-tracking-privacy.html) | `false` | Nein |
| `HINATA_TIME_TRACKING_BILLING_ENABLED` | Schaltet die Abrechnung ein: Stundensätze, Abrechnungsberichte und Rechnungen, nur für Organisationsadmins und Projektleitungen. Setzt die erweiterte Zeiterfassung voraus. Der Schalter unter **Organisation → Zeiterfassung** hat Vorrang vor diesem Wert | `false` | Nein |
| `HINATA_TIME_TRACKING_CURRENCY` | Die eine Währung aller Beträge (ISO 4217). Das Feld unter **Organisation → Zeiterfassung** hat Vorrang vor diesem Wert | `EUR` | Nein |
| `HINATA_TIME_TRACKING_INVOICE_PREFIX` | Womit jede Rechnungsnummer beginnt, vor Jahr und laufender Nummer (`INV-2026-00001`). Großbuchstaben und Ziffern, höchstens 10. Ein neuer Präfix beginnt einen neuen Nummernkreis | `INV` | Nein |
| `HINATA_RATE_LIMIT_TIME_OFF_REQUESTS_PER_DAY` | Abwesenheitsanträge und Krankmeldungen je Person und Tag. Ein Tag statt einer Minute, weil ein Antrag eine bewusste Handlung ist und ein Minutenbudget eine Schleife trotzdem durchließe | `50` | Nein |

!!! info "Wer die Abwesenheiten führt"
    Ohne weiteres Zutun führen sie die Organisationsadmins. Unter **Organisation → Zeiterfassung** lassen sich daneben einzelne Personen als **Abwesenheitsverwaltung** benennen. Sie pflegen Arten, teilen Ansprüche zu, buchen Korrekturen und entscheiden Anträge, ohne sonst Adminrechte zu haben. Der Weg dorthin steht in ihren eigenen Einstellungen. Die Liste ist bewusst leer voreingestellt: Wer in ihr steht, sieht Krankheitstage als Krankheitstage (Art. 9 DSGVO), und der engere Kreis ist die richtige Vorgabe. Sobald jemand benannt ist, sehen Organisationsadmins bei einer Krankheit nur noch, dass die Person abwesend ist, aber nicht, warum. Ohne benannte Personen führen die Organisationsadmins die Abwesenheiten weiter selbst.

!!! info "Das Limit sperrt keine Krankmeldung"
    Eine Krankmeldung zählt auf dasselbe Tagesbudget, wird davon aber nie abgewiesen: § 5 EFZG kennt eine Anzeige, keine Erlaubnis. Erreicht jemand die Grenze, werden nur weitere **Anträge** abgelehnt.

!!! danger "`HINATA_ICS_SECRET` nie wechseln"
    Eine Kalenderadresse, die mit einem `HINATA_ICS_SECRET` verschlüsselt wurde, lässt sich mit einem anderen nicht lesen. Jede Adresse ist außerdem an den Datensatz gebunden, in dem sie steht, und lässt sich nicht in einen anderen kopieren. Ändert sich der Schlüssel, wird jede gespeicherte Adresse unlesbar: Feiertagsimporte scheitern, bis ein Organisationsadmin die Adresse neu einträgt, und die Abos aller Personen melden „Die gespeicherte Adresse lässt sich nicht mehr lesen“, bis sie ihre Adresse erneut einfügen. Bereits importierte Feiertage und schon übernommene Einträge bleiben. Bewahre den Schlüssel bei deinen anderen Geheimnissen auf und sichere ihn.

### Wie Kalender abgerufen werden

Eine Kalenderadresse tippt eine Person ein. Der Server behandelt deshalb jeden Abruf so, als hätte irgendwer im Internet die Adresse gewählt:

- **Nur `https`**, auf Port 443 oder 8443. Eine Adresse mit `webcal://` wird als `https` gelesen. Kein Benutzername und kein Passwort in der Adresse.
- **Der Host muss ein Name sein**, nie eine IP-Adresse. Jede Adresse, zu der er sich auflöst, muss im öffentlichen Internet liegen, sonst wird der Host abgelehnt. Der Server verbindet sich nur mit den geprüften Adressen, eine zweite DNS-Antwort kann ihn also nicht nach innen lenken.
- **Keine Weiterleitungen.** Eine Weiterleitung gilt als Fehler, auch auf denselben Host.
- **Zehn Sekunden** für Namensauflösung, Verbindung und Download zusammen, und höchstens **2 MB** je Kalender. Höchstens vier Abrufe laufen gleichzeitig.
- Die Adresse steht nie in einem Log, einer API-Antwort oder im Audit-Log. Personen sehen nur den Host.

Abos werden jede halbe Stunde gelesen, außer sie wurden in den letzten 25 Minuten schon gelesen. Unveränderte Kalender werden mit `If-None-Match` / `If-Modified-Since` abgefragt und kosten daher wenig. Personen können einen Kalender auch von Hand aktualisieren, höchstens einmal pro Minute. Nach fünf Fehlversuchen in Folge wird ein Abo pausiert, bis die Person es fortsetzt. Der Server behält die Termine jeder Person von 30 Tagen zurück bis 90 Tage voraus, höchstens 5.000 je Abo, und jede Person kann bis zu 10 Abos haben. Ist die erweiterte Zeiterfassung oder der Kalender-Import aus, wird nichts abgerufen.

## Projektvorlagen und relative Fristen

Ein Projekt lässt sich kopieren, als Vorlage kennzeichnen und mit einem Termin versehen, an dem die Fristen seiner Vorgänge hängen. Ist das ausgeschaltet, verhalten sich Projekte genau wie bisher, und die Wege zum Kopieren gibt es nicht. Siehe [Projektvorlagen](/de/project-templates.html).

| Variable | Zweck | Standard / Beispiel | Erforderlich |
| --- | --- | --- | --- |
| `HINATA_PROJECT_TEMPLATES_ENABLED` | Schaltet Projektvorlagen und relative Fristen ein: Projekt kopieren, als Vorlage kennzeichnen, Projekt aus einer Vorlage anlegen und eine Frist als Versatz zum Termin des Projekts pflegen. Der Schalter unter **Adminbereich → Plattform** hat Vorrang vor diesem Wert | `false` | Nein |
| `HINATA_PROJECT_TEMPLATES_DEFAULT_BASIS` | Worin neue relative Fristen zählen, solange weder die Organisation noch das Projekt etwas anderes festlegt: `CALENDAR` (Kalendertage) oder `WORKING` (Werktage). Organisationsadmins wählen den Standard auf der Seite [Organisation](/de/organization.html), jedes Projekt kann davon abweichen. Bestehende Fristen behalten ihre Zählweise | `CALENDAR` | Nein |

!!! info "Werktage brauchen einen Feiertagskalender"
    Eine Frist, die in Werktagen rechnet, überspringt immer Wochenenden. Feiertage überspringt sie nur, wenn am Projekt ein Feiertagskalender gewählt ist. Ohne einen solchen Kalender zählt sie Feiertage wie gewöhnliche Werktage.

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
- IMAP-Abruf für **E-Mail → Ticket** ([E-Mail zu Vorgang](/de/email-to-ticket.html)).
  Mails leiten Administratoren nur in Projekte, in denen sie selbst Mitglied sind
- **Push** über das Gateway
- OAuth-Zugangsdaten der **Git-Integration** (die `HINATA_GIT_*`-Werte oben)
- **Plattform-Einstellungen** unter Admin → Plattform: `minVersion`, die
  Datenschutz-URL, wie sich Menschen anmelden (`localAuthEnabled`,
  `registrationEnabled`, `requireAdminApproval`) und was die Plattform anbietet

Zeiterfassung, Abwesenheiten, Feiertage und der Standard für relative Fristen
liegen ebenfalls in MongoDB. Sie gehören aber nicht zum Adminbereich, sondern
zur Seite [Organisation](/de/organization.html), die Organisationsadmins
bearbeiten.

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
