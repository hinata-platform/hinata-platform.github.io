---
title: Überblick
description: Die Landkarte für den Selbstbetrieb von Hinata — was du betreibst, die Compose-Dateien, Profile und eine Checkliste aller Einstellungen.
---

# Hinata selbst hosten

Hinata ist dafür gemacht, von dir betrieben zu werden — auf deiner eigenen
Infrastruktur, ohne Beschränkung bei Nutzern, Boards oder Teams. Diese Seite ist
die Landkarte: aus welchen Teilen ein laufendes Hinata besteht, wie sie
zusammenspielen und eine Checkliste all dessen, was du vor dem Go-live
konfigurierst. Jeder Punkt verweist auf eine eigene Seite mit den konkreten
Schritten.

Wenn du nur den schnellsten Weg zu einer laufenden Instanz willst, beginne mit dem
[Schnellstart](/de/quick-start.html). Diese Seite ist das große Ganze, das
Produktiv-Betreiber zuerst lesen sollten.

## Was du betreibst

Ein produktives Hinata-Deployment ist ein kleiner Satz Container, orchestriert von
Docker Compose. Zwei Images werden im GitHub Container Registry unter
`ghcr.io/hinata-platform` veröffentlicht; der Rest sind gängige Upstream-Images.

| Komponente | Image | Rolle |
| --- | --- | --- |
| **Server (API)** | `ghcr.io/hinata-platform/hinata-server` | Spring-Boot-4-/Java-21-REST-API unter `/api/v1`, SSE-Live-Updates, JWT-Auth |
| **Web-App** | `ghcr.io/hinata-platform/hinata-app` | Der kompilierte Flutter-Web-Client, als statische Dateien ausgeliefert |
| **MongoDB** | `mongo:8.0` | Primärer Datenspeicher — in Produktion ein **Replica Set** (2 Datenknoten + 1 Arbiter) |
| **Objektspeicher** | `minio/minio` | S3-kompatibler Speicher für Anhänge und Avatare (Presigned Downloads) |
| **Mail** | dein SMTP-Relay (`axllent/mailpit` in Dev) | Ausgehende E-Mail: Verifizierung, Passwort-Reset, Benachrichtigungen |

Der Server ist zustandslos — der gesamte Zustand liegt in MongoDB und MinIO —
sodass du ihn frei skalierst oder neu ausrollst. Live-Updates erreichen Clients
über **Server-Sent Events (SSE)**, ein zusätzlicher Message-Broker ist also nicht
nötig.

!!! info "Du brauchst kein Firebase"
    Mobile Push und universelle (Deep-)Links laufen über das zentrale
    [Hinata Connect Gateway](/de/connect-gateway.html). Dein Server registriert
    sich beim Start selbst am Gateway; die Push-Credentials der veröffentlichten App
    liegen im Gateway, nicht in deinem Deployment. Für Push konfigurieren
    Selbst-Hoster nichts.

## Die zwei Compose-Dateien

Das Server-Repository liefert zwei kombinierbare Stack-Dateien. Betrachte den
API-Stack als Basis und die App als Overlay, das du darüberlegst.

| Datei | Was sie startet |
| --- | --- |
| `docker-compose.yml` | **Der vollständige Backend-Stack**: der Server, das MongoDB-Replica-Set (`mongo1`, `mongo2`, `mongo-arbiter`) und MinIO. Das ist die Basis. |
| `docker-compose.app.yml` | **Ein Overlay, das die Flutter-Web-App hinzufügt** (`hinata-app`), ausgeliefert auf `HINATA_APP_PORT`. Lege es über die Basis, um den Web-Client vom selben Host zu servieren. |

Nur den API-Stack starten:

```bash
docker compose up -d
```

Den API-Stack **und** die Web-App zusammen starten, indem du beide Dateien
übergibst:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

!!! tip "Du musst die Web-App nicht zwingend selbst hosten"
    Da native Apps mehrere Server speichern und zwischen ihnen wechseln können und
    der Web-Build auf die konfigurierte API zeigt, betreiben manche Betreiber nur
    den API-Stack und lassen Nutzer ihn über die veröffentlichten Apps erreichen.
    Hoste die Web-App selbst, wenn du ein gebrandetes `https://track.example.com` im
    Browser willst.

Es gibt außerdem eine dritte Datei für die lokale Entwicklung,
`docker-compose.dev.yml`, die nur die Infrastruktur (Mongo, MinIO, Mailpit)
startet, damit du den Server aus deiner IDE laufen lassen kannst. Siehe
[Entwicklung](/de/development.html).

## Profile: dev vs prod

Der Server wählt sein Verhalten anhand des Spring-Profils in
`SPRING_PROFILES_ACTIVE`:

- **`prod`** — MongoDB ist ein TLS-Replica-Set mit **X.509-Client-Authentifizierung**
  (kein Passwort im Connection-String). Das nutzt `docker-compose.yml` und das
  rollst du aus. Der Demo-Seeder ist herauskompiliert (`@Profile("!prod")`).
- **`dev`** — MongoDB läuft standalone (weiterhin TLS + X.509) für eine einzelne
  Entwicklerin auf `localhost`. Wird mit `docker-compose.dev.yml` verwendet, wenn
  der Server aus dem Quellcode läuft.

!!! warning "Führe den Demo-Seeder niemals in Produktion aus"
    `HINATA_DEMO_SEED=true` füllt einen realistischen englischen Demo-Workspace
    (Login `rebar` / `hinata-demo-2026`) für Screenshots und Klick-Durchläufe. Der
    Seeder ist mit `@Profile("!prod")` annotiert, wird also **unter dem prod-Profil
    unabhängig vom Flag komplett übersprungen** — verlasse dich aber niemals darauf
    als einzigen Schutz. Lass `HINATA_DEMO_SEED=false` in jeder Produktions-`.env`.
    Eine Live-Instanz zu seeden würde einen Admin mit bekanntem Passwort und
    Wegwerf-Daten in deiner echten Datenbank anlegen.

## Konfigurations-Checkliste

Arbeite diese durch, bevor du die Instanz freigibst. Jeder Punkt verweist auf die
Seite mit den konkreten Befehlen und Dateiinhalten.

| Bereich | Was zu setzen ist | Seite |
| --- | --- | --- |
| **Domain & TLS** | Öffentliche Hostnamen, ein Reverse Proxy, der HTTPS terminiert und an `HINATA_PORT` (API) und `HINATA_APP_PORT` (Web) weiterleitet | [Reverse Proxy & TLS](/de/reverse-proxy.html) |
| **JWT-Secret** | `HINATA_JWT_SECRET` — ein zufälliges HS512-Secret mit ≥ 64 Zeichen (in prod erforderlich) | [Produktiv-Deployment](/de/deployment.html) |
| **MongoDB X.509** | PKI erzeugen, das Client-Zertifikat als `$external`-Nutzer registrieren | [MongoDB & X.509](/de/database.html) |
| **Objektspeicher** | MinIO-Zugangsdaten und Bucket, oder auf ein externes S3 zeigen | [Objektspeicher](/de/storage.html) |
| **SMTP** | Ein echtes Mail-Relay, damit Verifizierungs-/Reset-/Benachrichtigungs-Mails zugestellt werden | [E-Mail & SMTP](/de/email.html) |
| **CORS** | `HINATA_CORS_ALLOWED_ORIGINS` — die Browser-Origins, die die API aufrufen dürfen | [Konfigurationsreferenz](/de/configuration.html) |
| **Trusted Proxies** | `HINATA_TRUSTED_PROXIES` — CIDRs der Proxys, die `X-Forwarded-For` setzen dürfen | [Reverse Proxy & TLS](/de/reverse-proxy.html) |
| **Gateway** | Meist der Standard; `HINATA_GATEWAY_BASE_URL` nur überschreiben, um ein eigenes zu betreiben | [Hinata Connect Gateway](/de/connect-gateway.html) |
| **Erststart** | Den In-App-Setup-Assistenten abschließen oder mit `HINATA_SETUP_*` automatisieren | [Setup & Erststart](/de/setup-wizard.html) |

Die vollständige Liste jeder Umgebungsvariablen — gruppiert, mit Defaults und
Angabe, ob erforderlich — findest du in der
[Konfigurationsreferenz](/de/configuration.html).

## Wie es weitergeht

- [Produktiv-Deployment](/de/deployment.html) — der vollständige, geordnete
  Durchlauf: Secrets, PKI, Image-Tags, `up -d`, Health-Checks, DNS und der
  Update-Ablauf.
- [Konfigurationsreferenz](/de/configuration.html) — jede Einstellung und der
  Unterschied zwischen Env-Variablen und Laufzeit-(Datenbank-)Einstellungen.
- [MongoDB & X.509](/de/database.html), [Objektspeicher](/de/storage.html),
  [E-Mail & SMTP](/de/email.html), [Reverse Proxy & TLS](/de/reverse-proxy.html) —
  die ausführlichen Seiten je Teilsystem.
- [Backups & Upgrades](/de/backups.html) — Daten über Redeploys hinweg sichern.
