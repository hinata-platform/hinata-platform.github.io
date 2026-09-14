---
title: Überblick
description: Was du für Hinata selbst betreibst, die Compose-Dateien, Profile und eine Checkliste aller Einstellungen.
---

# Hinata selbst hosten

Du betreibst Hinata auf deiner eigenen Infrastruktur, ohne Limits bei Nutzern,
Boards oder Teams. Diese Seite zeigt, aus welchen Teilen Hinata besteht und was
du vor dem Go-live einstellst. Jeder Punkt verweist auf eine Seite mit den
konkreten Schritten.

Nur schnell eine Instanz starten? Dann nimm den [Schnellstart](/de/quick-start.html).

## Was du betreibst

Hinata läuft als kleiner Satz Container mit Docker Compose. Zwei Images liegen in
der GitHub Container Registry unter `ghcr.io/hinata-platform`. Der Rest sind
gängige Upstream-Images.

| Komponente | Image | Rolle |
| --- | --- | --- |
| **Server (API)** | `ghcr.io/hinata-platform/hinata-server` | REST-API mit Spring Boot 4 und Java 21 unter `/api/v1`, SSE-Live-Updates, JWT-Auth |
| **Web-App** | `ghcr.io/hinata-platform/hinata-app` | Der kompilierte Flutter-Web-Client als statische Dateien |
| **MongoDB** | `mongo:8.0` | Hauptdatenspeicher. In Produktion ein **Replica Set** (2 Datenknoten + 1 Arbiter) |
| **Objektspeicher** | `minio/minio` | S3-kompatibler Speicher für Anhänge und Avatare (Presigned Downloads) |
| **Mail** | dein SMTP-Relay (`axllent/mailpit` in Dev) | Ausgehende E-Mail: Verifizierung, Passwort-Reset, Benachrichtigungen |

- Der Server ist zustandslos. Alle Daten liegen in MongoDB und MinIO. Du kannst ihn
  also frei skalieren oder neu ausrollen.
- Live-Updates kommen per **Server-Sent Events (SSE)**. Einen Message Broker
  brauchst du nicht.

!!! info "Du brauchst kein Firebase"
    Push und Universal Links laufen über das gehostete
    [Hinata Connect Gateway](/de/connect-gateway.html). Die Push-Zugangsdaten der
    App liegen dort, nicht bei dir. Für Push musst du nichts betreiben und nichts
    einstellen.

## Die zwei Compose-Dateien

Das Server-Repository enthält zwei Stack-Dateien. Der API-Stack ist die Basis, die
App legst du optional darüber.

| Datei | Was sie startet |
| --- | --- |
| `docker-compose.yml` | **Der vollständige Backend-Stack**: Server, MongoDB Replica Set (`mongo1`, `mongo2`, `mongo-arbiter`) und MinIO. Das ist die Basis. |
| `docker-compose.app.yml` | **Ein Overlay mit der Flutter-Web-App** (`hinata-app`) auf `HINATA_APP_PORT`. Damit lieferst du den Web-Client vom selben Host aus. |

Nur den API-Stack starten:

```bash
docker compose up -d
```

API-Stack **und** Web-App zusammen starten:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

!!! tip "Du musst die Web-App nicht zwingend selbst hosten"
    Die nativen Apps speichern mehrere Server, und der Web-Build zeigt auf die
    eingestellte API. Manche Betreiber starten daher nur den API-Stack, und die
    Nutzer verbinden sich über die Apps aus den Stores. Hoste die Web-App selbst,
    wenn du eine eigene Adresse wie `https://track.example.com` im Browser willst.

Für die lokale Entwicklung gibt es noch `docker-compose.dev.yml`. Sie startet nur
Mongo, MinIO und Mailpit, den Server startest du aus der IDE. Siehe
[Entwicklung](/de/development.html).

## Profile: dev vs prod

Das Spring-Profil in `SPRING_PROFILES_ACTIVE` bestimmt das Verhalten:

- **`prod`:** MongoDB ist ein Replica Set mit TLS und **X.509-Clientauthentifizierung**
  (kein Passwort im Connection String). Das nutzt `docker-compose.yml`, und das
  rollst du aus. Der Demo-Seeder ist nicht enthalten (`@Profile("!prod")`).
- **`dev`:** MongoDB läuft standalone (weiterhin TLS + X.509) für eine Person auf
  `localhost`. Gedacht für `docker-compose.dev.yml`, wenn der Server aus dem
  Quellcode läuft.

!!! warning "Führe den Demo-Seeder niemals in Produktion aus"
    `HINATA_DEMO_SEED=true` legt einen englischen Demo-Workspace an (Login `rebar`
    / `hinata-demo-2026`), gedacht für Screenshots und zum Durchklicken.

    Unter dem Profil `prod` wird der Seeder wegen `@Profile("!prod")` **immer
    übersprungen, egal was das Flag sagt**. Verlass dich trotzdem nicht allein
    darauf. Setze in jeder Produktions-`.env` `HINATA_DEMO_SEED=false`. Sonst
    landen ein Admin mit bekanntem Passwort und Testdaten in deiner echten
    Datenbank.

## Konfigurations-Checkliste

Geh diese Punkte durch, bevor du die Instanz freigibst:

| Bereich | Was zu setzen ist | Seite |
| --- | --- | --- |
| **Domain & TLS** | Öffentliche Hostnamen und ein Reverse Proxy, der HTTPS terminiert und an `HINATA_PORT` (API) und `HINATA_APP_PORT` (Web) weiterleitet | [Reverse Proxy & TLS](/de/reverse-proxy.html) |
| **JWT-Secret** | `HINATA_JWT_SECRET`: ein zufälliges HS512-Secret mit ≥ 64 Zeichen (in prod Pflicht) | [Produktiv-Deployment](/de/deployment.html) |
| **MongoDB X.509** | PKI erzeugen, Clientzertifikat als `$external`-Nutzer registrieren | [MongoDB & X.509](/de/database.html) |
| **Objektspeicher** | MinIO-Zugangsdaten und Bucket, oder ein externes S3 | [Objektspeicher](/de/storage.html) |
| **SMTP** | Ein echtes Mail-Relay, damit Mails zu Verifizierung, Passwort-Reset und Benachrichtigungen ankommen | [E-Mail & SMTP](/de/email.html) |
| **CORS** | `HINATA_CORS_ALLOWED_ORIGINS`: Browser-Origins, die die API aufrufen dürfen | [Konfigurationsreferenz](/de/configuration.html) |
| **Trusted Proxies** | `HINATA_TRUSTED_PROXIES`: CIDRs der Proxys, die `X-Forwarded-For` setzen dürfen | [Reverse Proxy & TLS](/de/reverse-proxy.html) |
| **Gateway** | Meist der Standard. `HINATA_GATEWAY_BASE_URL` nur für ein eigenes Gateway ändern | [Hinata Connect Gateway](/de/connect-gateway.html) |
| **Erststart** | Den Setup-Assistenten in der App abschließen oder mit `HINATA_SETUP_*` automatisieren | [Setup & Erststart](/de/setup-wizard.html) |

Alle Umgebungsvariablen mit Gruppen, Standardwerten und Pflichtangabe stehen in
der [Konfigurationsreferenz](/de/configuration.html).

## Wie es weitergeht

- [Produktiv-Deployment](/de/deployment.html): alle Schritte der Reihe nach, von
  Secrets, PKI und Image-Tags über `up -d`, Health-Checks und DNS bis zu Updates.
- [Konfigurationsreferenz](/de/configuration.html): jede Einstellung und der
  Unterschied zwischen Umgebungsvariablen und Einstellungen in der Datenbank.
- [MongoDB & X.509](/de/database.html), [Objektspeicher](/de/storage.html),
  [E-Mail & SMTP](/de/email.html), [Reverse Proxy & TLS](/de/reverse-proxy.html):
  die Detailseiten je Teilsystem.
- [Backups & Upgrades](/de/backups.html): Daten über Redeploys hinweg sichern.
