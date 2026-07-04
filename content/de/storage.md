---
title: Objektspeicher (S3/MinIO)
description: Hinata bewahrt Anhänge und Avatare in S3-kompatiblem Objektspeicher auf — MinIO im Standard-Stack oder jeder externe S3-Anbieter — mit presigned Downloads und zufällig erzeugten Schlüsseln.
---

# Objektspeicher (S3/MinIO)

Vorgangsanhänge und Benutzer-Avatare werden nicht in MongoDB gespeichert — sie leben in
**S3-kompatiblem Objektspeicher**. Der Standard-Docker-Stack liefert **MinIO** aus, aber der
Server kommuniziert mit dem Speicher über die Standard-S3-API, sodass du ihn ohne Codeänderung
auf AWS S3 oder jeden anderen S3-kompatiblen Anbieter richten kannst. Diese Seite behandelt die
Standardeinrichtung, wie Downloads sicher bleiben und wie du einen externen Bucket einbindest.

## MinIO im Standard-Stack

Die produktive `docker-compose.yml` betreibt einen MinIO-Container neben dem Server:

```yaml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: ${MINIO_ROOT_USER:?set in .env}
    MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:?set in .env}
  volumes:
    - minio-data:/data
```

Der Server verbindet sich über das interne Docker-Netzwerk mit ihm und verwendet die
MinIO-Root-Zugangsdaten als seine S3-Access-/Secret-Keys wieder:

```yaml
HINATA_S3_ENDPOINT: http://minio:9000
HINATA_S3_ACCESS_KEY: ${MINIO_ROOT_USER}
HINATA_S3_SECRET_KEY: ${MINIO_ROOT_PASSWORD}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
```

Im Standard-Stack setzt du also nur drei Dinge in `.env`:

```properties
MINIO_ROOT_USER=hinata
MINIO_ROOT_PASSWORD=change-me-to-a-long-random-value
HINATA_S3_BUCKET=hinata
```

Die MinIO-**Weboberfläche** ist auf Port `9001` verfügbar und die **S3-API** auf `9000`.
In der lokalen Entwicklung (`docker-compose.dev.yml`) werden beide auf Loopback veröffentlicht —
`http://localhost:9001` (Konsole) und `http://localhost:9000` (API) — mit den Dev-Schlüsseln
`hinata` / `hinata-dev-secret`.

!!! warning "Ändere das MinIO-Passwort vor der Produktion"
    `hinata-dev-secret` ist ein Entwicklungsstandard. Setze ein langes, zufälliges
    `MINIO_ROOT_PASSWORD` (z. B. aus `./deploy/generate-secrets.sh`) für jedes reale
    Deployment und veröffentliche die MinIO-Ports niemals im öffentlichen Internet — nur der
    Server muss sie erreichen.

## Der Bucket wird für dich erstellt

Du musst den Bucket nicht vorab anlegen. Beim ersten Upload prüft der Server, ob
`HINATA_S3_BUCKET` existiert, und ruft `makeBucket` auf, falls nicht. Der Bucket bleibt
**privat** — nichts wird jemals öffentlich lesbar gemacht. Jeder Download wird vom Server
vermittelt (siehe unten), sodass Objekte nie direkt aus dem Bucket ausgeliefert werden.

!!! tip
    Wenn du den Bucket lieber selbst anlegst (zum Beispiel, um vorab eine Lifecycle-Regel
    oder eine Bucket-Policy zu setzen), tue dies mit dem Standardnamen `hinata` oder setze
    `HINATA_S3_BUCKET` auf den von dir erstellten Namen. Der Server verwendet einen
    vorhandenen Bucket gerne wieder.

## Presigned Downloads und zufällig erzeugte Schlüssel

Zwei Design-Entscheidungen halten den Objektspeicher standardmäßig sicher:

- **Zufällig erzeugte Objektschlüssel.** Ein vom Nutzer angegebener Dateiname wird nie zum
  Objektschlüssel. Der Server speichert jeden Anhang unter einer zufälligen UUID (optional
  hinter einem Präfix wie `media/` oder `avatars/`), sodass ein Bucket-Schlüssel nicht
  erraten werden kann und der ursprüngliche Dateiname nie das Bucket-Layout berührt.
- **Presigned, kurzlebige Downloads.** Wenn ein Client einen Anhang anfordert, gibt der
  Server eine **presigned GET-URL** zurück, die **10 Minuten** gültig ist und einen
  `Content-Disposition: attachment`-Header trägt (sodass Dateien heruntergeladen statt inline
  gerendert werden). Der Bucket selbst muss nie öffentlich sein.

Das bedeutet, dass die S3-Zugangsdaten vollständig serverseitig bleiben; Clients sehen immer nur
zeitlich begrenzte URLs.

## Live-Anhang-Ereignisse (SSE)

Anhang-Änderungen werden allen, die einen Vorgang betrachten, in Echtzeit über
**Server-Sent Events** gepusht:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

Wenn jemand eine Datei hochlädt oder entfernt — oder mehrere auf einmal ablegt — sieht jeder
offene Betrachter das Raster live aktualisiert, ohne Polling. Der Stream läuft in-process pro
Server-Instanz; für ein geclustertes Deployment würdest du ihn mit einem gemeinsamen Broker
vorschalten.

## Größen- und Content-Type-Limits

Uploads werden auf mehreren Achsen validiert. Die Standardwerte:

| Einstellung | Env / Property | Standard |
| --- | --- | --- |
| Maximale Größe einer einzelnen Datei | `HINATA_STORAGE_MAX_UPLOAD_MB` | `25` MB |
| Maximale Anzahl Dateien pro Anfrage | `hinata.storage.max-files-per-request` | `10` |
| Maximale Gesamtgröße einer Anfrage | `HINATA_STORAGE_MAX_REQUEST_MB` | `100` MB |

Erlaubte Content-Types sind eine explizite Allow-List — PNG, JPEG, GIF, WebP, PDF, reiner
Text, CSV, ZIP, JSON und die OOXML-Word-/Excel-Dokumente. Ein paar wichtige Schutzmaßnahmen:

- **`image/svg+xml` ist absichtlich ausgeschlossen**, weil SVG JavaScript einbetten kann
  (ein Stored-XSS-Risiko).
- **Magic-Byte-Verifizierung.** Bei Binärtypen prüft der Server die führenden Bytes der Datei
  gegen den deklarierten Content-Type, sodass sich eine Datei nicht etwa als PNG ausgeben kann.
- Ein abgelehnter Upload gibt einen lokalisierten, stabilen Fehler zurück
  (`error.storage.fileTooLarge`, `error.storage.fileTypeNotAllowed`,
  `error.storage.contentMismatch`).

!!! note "Zwei Größenobergrenzen arbeiten zusammen"
    Springs Multipart-Limits (`max-file-size` / `max-request-size`, gesteuert von denselben
    MB-Werten) sind die äußere Schutzschicht; die App erzwingt dann obendrauf die Dateianzahl
    und die aggregierte Größe. Erhöhe sie alle gemeinsam, wenn du größere Uploads brauchst.

## Externes / AWS S3 statt MinIO verwenden

Um AWS S3 oder einen anderen S3-kompatiblen Anbieter (Cloudflare R2, Backblaze B2, Wasabi,
Ceph, ein verwaltetes MinIO, …) zu verwenden, richte dieselben vier Variablen darauf und lasse
den mitgelieferten MinIO-Container weg:

```properties
HINATA_S3_ENDPOINT=https://s3.eu-central-1.amazonaws.com
HINATA_S3_ACCESS_KEY=AKIA...
HINATA_S3_SECRET_KEY=your-secret-access-key
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_REGION=eu-central-1
```

Hinweise:

- **`HINATA_S3_REGION`** ist standardmäßig `us-east-1`; setze es bei AWS und Anbietern, denen
  es wichtig ist, auf die Region deines Buckets.
- Für einen Nicht-AWS-Anbieter ist `HINATA_S3_ENDPOINT` dessen S3-Endpunkt-URL (z. B. dein
  R2- oder Backblaze-Endpunkt). Verwende HTTPS für alles, was das Netzwerk überquert.
- Die Zugangsdaten brauchen Berechtigung für `PutObject`, `GetObject`, `DeleteObject`,
  `ListBucket` und (sofern du den Bucket nicht vorab anlegst) `CreateBucket`.
- Wenn der Speicher unkonfiguriert bleibt (leerer Access-Key), antworten die Anhang- und
  Avatar-Endpunkte mit `error.storage.notConfigured` — der Rest von Hinata funktioniert
  weiterhin, du kannst nur keine Dateien hochladen.

!!! tip "Halte Buckets privat"
    Welchen Anbieter du auch verwendest, halte den Bucket **privat**. Hinata braucht nie
    öffentlichen Lesezugriff: Es gibt immer kurzlebige presigned URLs aus, sodass öffentlicher
    Zugriff nur deine Angriffsfläche vergrößern würde.

Siehe die [Konfigurationsreferenz](/de/configuration.html) für die vollständige Variablenliste
und [MongoDB & X.509](/de/database.html) für die Datenbankseite des Stacks.
