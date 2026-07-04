---
title: Schnellstart
description: Bringe einen Hinata-Server und die App in Minuten mit Docker Compose zum Laufen — drei Befehle, ein JWT-Secret und der In-App-Einrichtungsassistent.
---

# Schnellstart

Dies ist der schnellste Weg von null zu einem laufenden Hinata-Stack. Wenn du Docker hast, bist du nur etwa drei Befehle von einem laufenden Server, einer Datenbank, Objektspeicher und einem Mail-Catcher entfernt — anschließend richtest du die App darauf aus und durchläufst einen kurzen Einrichtungsassistenten.

!!! note "Voraussetzungen (in einer Zeile)"
    Ein Host mit **Docker Engine + Docker Compose v2** und diesem ausgecheckten Repository. Mehr braucht der Schnellstart nicht. Für Dimensionierung und Netzwerkdetails siehe [Voraussetzungen](/de/requirements.html).

## Die drei Befehle

Aus dem Wurzelverzeichnis des [hinata-server](https://github.com/hinata-platform/hinata-server)-Repositorys:

```bash
cp .env.example .env
./deploy/generate-secrets.sh   # creates the Mongo keyfile + prints secrets for .env
docker compose up -d
```

Was jeder Schritt tut:

1. **`cp .env.example .env`** — erstellt deine lokale Konfigurationsdatei aus der mitgelieferten Vorlage. Jede Einstellung ist eine Umgebungsvariable; in `.env` trägst du die für dein Deployment relevanten Werte ein. Die vollständige Liste findest du in der [Konfigurationsreferenz](/de/configuration.html).
2. **`./deploy/generate-secrets.sh`** — erzeugt das MongoDB-Replikatset-**Keyfile** (erforderlich für die interne Cluster-Authentifizierung) und gibt starke, zufällige Secrets aus, die du in `.env` einfügst. Führe es vor dem ersten `up` aus.
3. **`docker compose up -d`** — lädt die Images von `ghcr.io/hinata-platform` und startet den Stack im Hintergrund.

## Was hochfährt

`docker compose up -d` bringt den kompletten Stack im Entwicklungsstil online:

| Container | Rolle |
| --- | --- |
| **server** | Die Spring-Boot-API unter `/api/v1` (Host-Port `3356` standardmäßig). |
| **MongoDB replica set** | 2 Datenknoten + 1 Arbiter — das führende System. |
| **MinIO** | S3-kompatibler Objektspeicher für Anhänge und Avatare. |
| **Mailpit** | Ein lokaler Mail-Catcher, damit du ausgehende E-Mails ohne echtes Relay sehen kannst. |

Gib ihm ein paar Sekunden und prüfe dann, ob der Server gesund ist:

```bash
curl -s http://localhost:3356/api/v1/actuator/health
# {"status":"UP"}
```

!!! info "Praktische lokale Oberflächen"
    Der Posteingang von Mailpit liegt unter `http://localhost:8025` und die MinIO-Konsole unter `http://localhost:9001`. Beide eignen sich hervorragend, um vor dem Produktivbetrieb zu bestätigen, dass Mail und Uploads funktionieren.

## Das JWT-Secret setzen — das ist ein MUSS

Hinata signiert seine zustandslosen Access- und Refresh-Tokens mit einem **HS512**-Secret. Die Vorlage liefert dieses **leer** aus, und im Produktivbetrieb akzeptiert der Server keinen leeren oder schwachen Wert. Erzeuge einen echten (mindestens 64 Zeichen):

```bash
openssl rand -base64 64 | tr -d '\n'
```

Füge die Ausgabe in `.env` ein:

```properties
HINATA_JWT_SECRET=PASTE_YOUR_64_CHAR_SECRET_HERE
```

!!! danger "Keine Standardwerte ausliefern"
    Der Standardwert für `HINATA_JWT_SECRET` ist **leer**, und die `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` sowie das TLS-Keystore-/Truststore-Passwort (`changeit`) der Vorlage sind **Platzhalter**. Setze vor jedem ins Internet gerichteten Deployment ein echtes JWT-Secret und ersetze jedes Standardpasswort. `./deploy/generate-secrets.sh` gibt genau dafür starke Werte aus.

Nachdem du `.env` geändert hast, erstelle den Server neu, damit er die neue Umgebung übernimmt:

```bash
docker compose up -d
```

## Die App auf deinen Server ausrichten

Der Server ist nur die halbe Miete — die [App](/de/clients.html) ist die Art, wie Menschen ihn nutzen. Die App ist mehrserverfähig: Sie kodiert nie eine URL fest, du gibst ihr also an, wo dein Server liegt.

Setze deine öffentliche API-Basis in `.env`, damit Tokens für den richtigen Host ausgestellt werden und E-Mail-Deep-Links nach Hause zeigen:

```properties
HINATA_BASE_URL=https://api.track.example.com
```

Öffne dann in der App den **Server-Manager**, füge deinen Server hinzu (dabei wird ein Live-Verbindungstest ausgeführt) und wechsle zu ihm. Im Web-Build kannst du einfach die neben der API ausgelieferte Web-App aufrufen. Für einen lokalen Test funktioniert `http://localhost:3356` von derselben Maschine.

!!! tip "Lokale vs. produktive Hosts"
    In diesem Schnellstart verwenden wir `localhost`. Für alles, was von anderen Geräten erreichbar sein soll, brauchst du öffentliches DNS und TLS vor dem Server — die App erwartet `https://` für gespeicherte Server. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Den Einrichtungsassistenten durchlaufen

Beim ersten Start hat der Server noch keine Organisation und keinen Administrator. Öffne die App gegen deinen neuen Server und durchlaufe den **In-App-Einrichtungsassistenten**: Benenne deine Organisation und lege das erste ADMIN-Konto an. Ab diesem Moment kannst du Projekte anlegen, Personen einladen und mit der Arbeit beginnen.

Du bevorzugst einen unbeaufsichtigten Start (für CI oder skriptgesteuerte Installationen)? Überspringe den Assistenten vollständig:

```properties
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-please
HINATA_SETUP_ADMIN_DISPLAY_NAME=Admin
```

Für die Mechanik und eine Schritt-für-Schritt-Anleitung mit Screenshots siehe [Setup & Erststart](/de/setup-wizard.html).

## Du betreibst jetzt Hinata

Das ist ein laufender Stack: Server, Datenbank, Speicher, Mail und ein Admin-Konto. Von hier aus geht es in den sinnvollen nächsten Schritten darum, ihn produktionsreif zu machen.

## Nächste Schritte

- **[Produktiv-Deployment](/de/deployment.html)** — der echte Replikatset-Weg mit X.509-Zertifikaten und GHCR-Image-Tags.
- **[Konfigurationsreferenz](/de/configuration.html)** — jede Umgebungsvariable, was sie tut und ihr Standardwert.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html)** — einen Proxy davorschalten, TLS terminieren und an die Ports `3356`/`3456` weiterleiten.
- **[Voraussetzungen](/de/requirements.html)** — Host-Dimensionierung, Netzwerk und die Bausteine, die du für ein echtes Deployment brauchst.
