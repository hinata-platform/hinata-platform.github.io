---
title: Schnellstart
description: Hinata-Server und App mit Docker Compose in wenigen Minuten starten, mit drei Befehlen, einem JWT-Secret und dem Einrichtungsassistenten.
---

# Schnellstart

Mit Docker brauchst du etwa drei Befehle für Server, Datenbank, Objektspeicher und Mail-Catcher. Danach verbindest du die App und durchläufst einen kurzen Einrichtungsassistenten.

!!! note "Voraussetzungen"
    Ein Host mit **Docker Engine + Docker Compose v2** und dem ausgecheckten Repository. Mehr braucht der Schnellstart nicht. Dimensionierung und Netzwerk stehen unter [Voraussetzungen](/de/requirements.html).

## Die drei Befehle

Im Wurzelverzeichnis des [hinata-server](https://github.com/hinata-platform/hinata-server)-Repositorys:

```bash
cp .env.example .env
./deploy/generate-secrets.sh   # creates the Mongo keyfile + prints secrets for .env
docker compose up -d
```

1. **`cp .env.example .env`** legt deine Konfigurationsdatei aus der Vorlage an. Jede Einstellung ist eine Umgebungsvariable. Alle stehen in der [Konfigurationsreferenz](/de/configuration.html).
2. **`./deploy/generate-secrets.sh`** erzeugt das **Keyfile** für das MongoDB-Replikatset (nötig für die interne Cluster-Authentifizierung) und gibt starke Zufallswerte für `.env` aus. Führe es vor dem ersten `up` aus.
3. **`docker compose up -d`** lädt die Images von `ghcr.io/hinata-platform` und startet den Stack im Hintergrund.

## Was hochfährt

`docker compose up -d` startet den kompletten Stack für die Entwicklung:

| Container | Rolle |
| --- | --- |
| **server** | Die Spring-Boot-API unter `/api/v1` (standardmäßig Host-Port `3356`). |
| **MongoDB replica set** | 2 Datenknoten + 1 Arbiter, das führende System. |
| **MinIO** | S3-kompatibler Objektspeicher für Anhänge und Avatare. |
| **Mailpit** | Lokaler Mail-Catcher. Zeigt ausgehende E-Mails ohne echtes Relay. |

Warte ein paar Sekunden und prüfe dann den Server:

```bash
curl -s http://localhost:3356/api/v1/actuator/health
# {"status":"UP"}
```

!!! info "Praktische lokale Oberflächen"
    Mailpit liegt unter `http://localhost:8025`, die MinIO-Konsole unter `http://localhost:9001`. Damit prüfst du vor dem Produktivbetrieb, ob Mail und Uploads funktionieren.

## Das JWT-Secret setzen (Pflicht)

Hinata signiert seine zustandslosen Access- und Refresh-Tokens mit einem **HS512**-Secret. Die Vorlage lässt es **leer**, und im Produktivbetrieb lehnt der Server leere oder schwache Werte ab. Erzeuge ein echtes Secret mit mindestens 64 Zeichen:

```bash
openssl rand -base64 64 | tr -d '\n'
```

Füge die Ausgabe in `.env` ein:

```properties
HINATA_JWT_SECRET=PASTE_YOUR_64_CHAR_SECRET_HERE
```

!!! danger "Keine Standardwerte ausliefern"
    `HINATA_JWT_SECRET` ist standardmäßig **leer**. `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` und das Passwort für TLS-Keystore und Truststore (`changeit`) in der Vorlage sind **Platzhalter**. Setze vor jedem öffentlich erreichbaren Deployment ein echtes JWT-Secret und ersetze alle Standardpasswörter. `./deploy/generate-secrets.sh` gibt dafür starke Werte aus.

Nach Änderungen an `.env` erstellst du den Server neu, damit er die Umgebung übernimmt:

```bash
docker compose up -d
```

## Die App auf deinen Server ausrichten

Genutzt wird Hinata über die [App](/de/clients.html). Sie kann mit mehreren Servern arbeiten und hat keine fest eingebaute URL. Du sagst ihr also, wo dein Server liegt.

Setze deine öffentliche API-Basis in `.env`. Dann werden Tokens für den richtigen Host ausgestellt, und Links in E-Mails führen zu deinem Server:

```properties
HINATA_BASE_URL=https://api.track.example.com
```

Öffne dann in der App den **Server-Manager**, füge deinen Server hinzu (mit Live-Verbindungstest) und wechsle zu ihm. Im Web-Build rufst du einfach die Web-App auf, die neben der API ausgeliefert wird. Lokal auf derselben Maschine funktioniert `http://localhost:3356`.

!!! tip "Lokale und produktive Hosts"
    Dieser Schnellstart nutzt `localhost`. Sollen andere Geräte zugreifen, brauchst du öffentliches DNS und TLS vor dem Server, denn die App erwartet `https://` für gespeicherte Server. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Den Einrichtungsassistenten durchlaufen

Beim ersten Start gibt es noch keine Organisation und keinen Admin. Öffne die App mit deinem neuen Server und durchlaufe den **Einrichtungsassistenten in der App**: Organisation benennen, erstes ADMIN-Konto anlegen. Danach kannst du Projekte anlegen, Leute einladen und loslegen.

Für CI oder skriptgesteuerte Installationen überspringst du den Assistenten:

```properties
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-please
HINATA_SETUP_ADMIN_DISPLAY_NAME=Admin
```

Details und eine Anleitung mit Screenshots findest du unter [Setup & Erststart](/de/setup-wizard.html).

## Du betreibst jetzt Hinata

Server, Datenbank, Speicher, Mail und ein Admin-Konto laufen. Als Nächstes machst du den Stack fit für die Produktion.

## Nächste Schritte

- **[Produktiv-Deployment](/de/deployment.html):** Replikatset mit X.509-Zertifikaten und GHCR-Image-Tags.
- **[Konfigurationsreferenz](/de/configuration.html):** jede Umgebungsvariable mit Zweck und Standardwert.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html):** Proxy davorschalten, TLS terminieren und an die Ports `3356`/`3456` weiterleiten.
- **[Voraussetzungen](/de/requirements.html):** Dimensionierung, Netzwerk und was du für ein echtes Deployment brauchst.
