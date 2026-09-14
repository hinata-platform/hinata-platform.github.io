---
title: Objektspeicher (S3, GCS, Azure)
description: Hinata legt Anhänge und Avatare in MinIO, einem S3-kompatiblen Anbieter oder Azure Blob Storage ab, mit presignten Downloads und zufälligen Schlüsseln.
---

# Objektspeicher (S3, GCS, Azure)

Anhänge und Avatare liegen im **Objektspeicher**, nicht in MongoDB. `HINATA_STORAGE_PROVIDER` wählt eines von zwei Backends:

- **`s3`** (Standard): jeder S3-kompatible Speicher, also das **mitgelieferte MinIO**, **AWS S3**, **Google Cloud Storage** (über die S3-kompatible XML-API), **Cloudflare R2**, **DigitalOcean Spaces**, Backblaze B2, Wasabi, Ceph, ein verwaltetes MinIO, …
- **`azure`**: **Azure Blob Storage** über die eigene API von Azure (Azure spricht kein S3).

## MinIO im Standard-Stack

Die `docker-compose.yml` für die Produktion startet MinIO neben dem Server. Der Container hängt am Compose-**Profil `local-storage`**, das standardmäßig aktiv ist (`COMPOSE_PROFILES=local-storage` in `.env.example`):

```yaml
minio:
  image: minio/minio:latest
  profiles: [local-storage]
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: ${MINIO_ROOT_USER:-}
    MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-}
  volumes:
    - minio-data:/data
```

Der Server erreicht MinIO über das interne Docker-Netzwerk und nutzt die Root-Zugangsdaten von MinIO als S3-Schlüssel:

```yaml
HINATA_S3_ENDPOINT: ${HINATA_S3_ENDPOINT:-http://minio:9000}
HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-${MINIO_ROOT_USER:-}}
HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-${MINIO_ROOT_PASSWORD:-}}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
```

In `.env` setzt du nur vier Werte:

```properties
COMPOSE_PROFILES=local-storage
MINIO_ROOT_USER=hinata
MINIO_ROOT_PASSWORD=change-me-to-a-long-random-value
HINATA_S3_BUCKET=hinata
```

Die **Weboberfläche** von MinIO läuft auf Port `9001`, die **S3-API** auf `9000`. Lokal (`docker-compose.dev.yml`) sind beide auf Loopback erreichbar, unter `http://localhost:9001` (Konsole) und `http://localhost:9000` (API), mit den Dev-Schlüsseln `hinata` / `hinata-dev-secret`.

!!! warning "Ändere das MinIO-Passwort vor der Produktion"
    `hinata-dev-secret` ist nur für die Entwicklung. Setze in jedem echten Deployment ein langes, zufälliges `MINIO_ROOT_PASSWORD` (z. B. aus `./deploy/generate-secrets.sh`). Veröffentliche die MinIO-Ports nie im Internet, nur der Server muss sie erreichen.

## Der Bucket wird für dich erstellt

Beim ersten Upload prüft der Server, ob `HINATA_S3_BUCKET` existiert, und ruft sonst `makeBucket` auf. Der Bucket bleibt **privat**, nichts wird öffentlich lesbar. Jeder Download läuft über den Server (siehe unten), nie direkt aus dem Bucket.

!!! tip
    Du kannst den Bucket auch selbst anlegen, etwa um vorher eine Lifecycle-Regel oder Bucket-Policy zu setzen. Nimm dann den Standardnamen `hinata` oder setze `HINATA_S3_BUCKET` auf deinen Namen. Ein vorhandener Bucket wird einfach mitgenutzt.

## Presigned Downloads und zufällig erzeugte Schlüssel

- **Zufällige Objektschlüssel.** Jeder Anhang liegt unter einer zufälligen UUID (optional mit Präfix wie `media/` oder `avatars/`), nie unter dem Dateinamen vom Nutzer. Schlüssel lassen sich nicht erraten, und der Originalname taucht im Bucket nicht auf.
- **Kurzlebige presignte Downloads.** Fordert ein Client einen Anhang an, gibt der Server eine **presignte GET-URL** zurück. Sie gilt **10 Minuten** und setzt `Content-Disposition: attachment`, damit Dateien heruntergeladen statt im Browser angezeigt werden.

Die S3-Zugangsdaten bleiben so auf dem Server. Clients sehen nur zeitlich begrenzte URLs, und der Bucket muss nie öffentlich sein.

## Anhänge in Echtzeit (SSE)

Änderungen an Anhängen gehen per **Server-Sent Events** sofort an alle, die den Vorgang geöffnet haben:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

Lädt jemand Dateien hoch oder entfernt sie, sehen alle das Raster ohne Polling aktualisiert, auch bei mehreren Dateien auf einmal. Der Stream läuft im Prozess jeder Serverinstanz. Für ein Deployment im Cluster bräuchtest du davor einen gemeinsamen Broker.

## Größen- und Content-Type-Limits

Die Standardwerte:

| Einstellung | Env / Property | Standard |
| --- | --- | --- |
| Maximale Größe einer einzelnen Datei | `HINATA_STORAGE_MAX_UPLOAD_MB` | `25` MB |
| Maximale Anzahl Dateien pro Anfrage | `hinata.storage.max-files-per-request` | `10` |
| Maximale Gesamtgröße einer Anfrage | `HINATA_STORAGE_MAX_REQUEST_MB` | `100` MB |

Erlaubt sind nur Content-Types aus einer festen Liste: PNG, JPEG, GIF, WebP, PDF, reiner Text, CSV, ZIP, JSON und Word- und Excel-Dokumente im OOXML-Format. Außerdem:

- **`image/svg+xml` ist bewusst ausgeschlossen.** SVG kann JavaScript enthalten (Risiko für Stored XSS).
- **Prüfung der Magic Bytes.** Bei Binärtypen vergleicht der Server die ersten Bytes mit dem angegebenen Content-Type. Eine Datei kann sich also nicht als PNG ausgeben.
- Ein abgelehnter Upload liefert einen stabilen, lokalisierten Fehler (`error.storage.fileTooLarge`, `error.storage.fileTypeNotAllowed`, `error.storage.contentMismatch`).

!!! note "Zwei Größenobergrenzen arbeiten zusammen"
    Die Multipart-Limits von Spring (`max-file-size` / `max-request-size`, aus denselben MB-Werten) sind die äußere Grenze. Die App prüft zusätzlich Dateianzahl und Gesamtgröße. Für größere Uploads erhöhst du alle Werte gemeinsam.

## Einen externen Anbieter statt MinIO verwenden

Leere das Compose-Profil in `.env`, um das mitgelieferte MinIO abzuschalten:

```properties
COMPOSE_PROFILES=
```

Konfiguriere dann einen der Anbieter unten. Die Variablen `MINIO_ROOT_*` kannst du entfernen.

### AWS S3

```properties
HINATA_S3_ENDPOINT=https://s3.eu-central-1.amazonaws.com
HINATA_S3_ACCESS_KEY=AKIA...
HINATA_S3_SECRET_KEY=your-secret-access-key
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_REGION=eu-central-1
```

### Google Cloud Storage

GCS spricht S3 über seine **interoperable XML-API**. Erzeuge **HMAC-Schlüssel** in der Cloud Console unter *Cloud Storage → Einstellungen → Interoperabilität* (empfohlen für ein Dienstkonto) und trage den Interop-Endpunkt ein:

```properties
HINATA_S3_ENDPOINT=https://storage.googleapis.com
HINATA_S3_ACCESS_KEY=GOOG1E...          # HMAC Access-ID
HINATA_S3_SECRET_KEY=your-hmac-secret
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_ADDRESSING_STYLE=path
```

### Azure Blob Storage

Azure hat keine S3-API, deshalb spricht Hinata direkt mit Azure. Stelle den Provider um und gib den **Connection String** des Speicherkontos an (Portal → Speicherkonto → *Zugriffsschlüssel*). Er muss den Kontoschlüssel enthalten, weil presignte Downloads als SAS-URLs ausgestellt werden:

```properties
HINATA_STORAGE_PROVIDER=azure
HINATA_AZURE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
HINATA_S3_BUCKET=hinata   # wird als Name des Blob-Containers verwendet
```

### Andere S3-kompatible Anbieter

Cloudflare R2, DigitalOcean Spaces, Backblaze B2, Wasabi, Ceph, Hetzner, ein verwaltetes MinIO, … funktionieren mit denselben Variablen `HINATA_S3_*`. Endpunkt, Schlüssel und Region stehen im Dashboard des Anbieters.

Hinweise:

- **`HINATA_S3_REGION`** ist standardmäßig `us-east-1`. Setze die Region deines Buckets bei AWS und bei Anbietern, die sie brauchen.
- **`HINATA_S3_ADDRESSING_STYLE`** (Standard `auto`) steuert die Adressierung der S3-URLs. `auto` wählt Virtual Host Style für AWS und Path Style für alle anderen, das passt fast immer. Verlangt dein Anbieter etwas anderes, setze `path` oder `virtual-host`.
- Nutze HTTPS für jeden Endpunkt, der über das Netzwerk geht.
- Die Zugangsdaten brauchen `PutObject`, `GetObject`, `DeleteObject`, `ListBucket` und `CreateBucket` (Letzteres nur, wenn du den Bucket nicht selbst anlegst). Bei Azure gelten die entsprechenden Rechte, auch der Container wird automatisch angelegt.
- Ohne Konfiguration (leerer Access Key oder leerer Connection String bei `provider=azure`) antworten die Endpunkte für Anhänge und Avatare mit `error.storage.notConfigured`. Der Rest von Hinata funktioniert, nur Uploads gehen nicht.
- **Ein Anbieterwechsel verschiebt keine vorhandenen Objekte.** Hat die Instanz schon Daten, kopiere zuerst den Bucket (`mc mirror`, `aws s3 sync`, `azcopy`).

!!! tip "Halte Buckets privat"
    Halte den Bucket bei jedem Anbieter **privat**. Hinata gibt immer kurzlebige presignte URLs aus und braucht nie öffentlichen Lesezugriff. Der würde nur die Angriffsfläche vergrößern.

Alle Variablen stehen in der [Konfigurationsreferenz](/de/configuration.html), die Datenbank unter [MongoDB & X.509](/de/database.html).
