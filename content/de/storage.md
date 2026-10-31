---
title: Objektspeicher (S3, GCS, Azure)
description: Hinata legt Anhänge und Avatare im mitgelieferten SeaweedFS, einem S3-kompatiblen Anbieter oder Azure Blob Storage ab, mit presignten Downloads und zufälligen Schlüsseln.
---

# Objektspeicher (S3, GCS, Azure)

Anhänge und Avatare liegen im **Objektspeicher**, nicht in MongoDB. `HINATA_STORAGE_PROVIDER` wählt eines von zwei Backends:

- **`s3`** (Standard): jeder S3-kompatible Speicher, also das **mitgelieferte SeaweedFS**, **AWS S3**, **Google Cloud Storage** (über die S3-kompatible XML-API), **Cloudflare R2**, **DigitalOcean Spaces**, Backblaze B2, Wasabi, Ceph, ein verwaltetes MinIO, …
- **`azure`**: **Azure Blob Storage** über die eigene API von Azure (Azure spricht kein S3).

## SeaweedFS im Standard-Stack

Die `docker-compose.yml` für die Produktion startet [SeaweedFS](https://github.com/seaweedfs/seaweedfs) (Apache-2.0, fest auf `4.48`) neben dem Server. Frühere Versionen brachten MinIO mit. MinIO veröffentlicht keine Community-Container-Images mehr, deshalb ist der Stack auf SeaweedFS umgestiegen. Hinata selbst hängt an keinem von beiden: Es spricht einfaches S3, und alle anderen S3-Anbieter und Azure funktionieren weiter (siehe [Einen externen Anbieter verwenden](#einen-externen-anbieter-verwenden)). Läuft bei dir noch das mitgelieferte MinIO, lies [Von MinIO zu SeaweedFS umziehen](#von-minio-zu-seaweedfs-umziehen).

Beide Speicherdienste hängen am Compose-**Profil `local-storage`**, das standardmäßig aktiv ist (`COMPOSE_PROFILES=local-storage` in `.env.example`):

- **`seaweedfs`** betreibt den Speicher. Sein Startskript (`deploy/seaweedfs/entrypoint.sh`) startet nicht, solange ein Zugangsschlüssel oder Key fehlt.
- **`seaweedfs-setup`** läuft einmal, legt den Bucket an, macht SSE-S3-Verschlüsselung zum Standard des Buckets und beendet sich.

```yaml
seaweedfs:
  image: chrislusf/seaweedfs:4.48
  profiles: [local-storage]
  entrypoint: ["/bin/sh", "/opt/hinata/entrypoint.sh"]
  environment:
    HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
    HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-}
    HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-}
    SEAWEEDFS_ADMIN_ACCESS_KEY: ${SEAWEEDFS_ADMIN_ACCESS_KEY:-}
    SEAWEEDFS_ADMIN_SECRET_KEY: ${SEAWEEDFS_ADMIN_SECRET_KEY:-}
    WEED_S3_SSE_KEK: ${SEAWEEDFS_SSE_KEK:-}
    WEED_JWT_SIGNING_KEY: ${SEAWEEDFS_JWT_VOLUME_WRITE:-}
    WEED_JWT_SIGNING_READ_KEY: ${SEAWEEDFS_JWT_VOLUME_READ:-}
    WEED_JWT_FILER_SIGNING_KEY: ${SEAWEEDFS_JWT_FILER_WRITE:-}
    WEED_JWT_FILER_SIGNING_READ_KEY: ${SEAWEEDFS_JWT_FILER_READ:-}
  volumes:
    - seaweedfs-data:/data
    - ./deploy/seaweedfs:/opt/hinata:ro
```

Was die mitgelieferte Konfiguration tut:

- **Ohne Zugangsdaten geht nichts.** Es gibt zwei Identitäten: `hinata`, die der Server nutzt und die nur ihren einen Bucket anfassen darf, und `admin`, die nur der Setup-Job nutzt.
- **Objekte werden verschlüsselt gespeichert**, mit SSE-S3 unter `SEAWEEDFS_SSE_KEK`. Der Schlüssel steht in der Umgebung, nie auf dem Datenvolume.
- **Anfragen zwischen den Teilen von SeaweedFS sind signiert**, mit den vier Schlüsseln `SEAWEEDFS_JWT_*`.
- **Nichts wird veröffentlicht.** Nur der Server erreicht den S3-Port (`8333`), über das Netzwerk des Stacks. Eine Weboberfläche gibt es nicht.

Der Server spricht mit diesen Standardwerten aus der Compose-Datei mit ihm:

```yaml
HINATA_S3_ENDPOINT: ${HINATA_S3_ENDPOINT:-http://seaweedfs:8333}
HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-}
HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
HINATA_S3_ADDRESSING_STYLE: ${HINATA_S3_ADDRESSING_STYLE:-path}
HINATA_S3_SSE: ${HINATA_S3_SSE:-}
```

In `.env` setzt du die Schlüssel. `./deploy/generate-secrets.sh` gibt für jedes Geheimnis einen frischen Wert aus:

```properties
COMPOSE_PROFILES=local-storage
HINATA_S3_ACCESS_KEY=hinata
HINATA_S3_SECRET_KEY=change-me
HINATA_S3_SSE=AES256
HINATA_S3_BUCKET=hinata
SEAWEEDFS_ADMIN_ACCESS_KEY=hinata-admin
SEAWEEDFS_ADMIN_SECRET_KEY=change-me
SEAWEEDFS_SSE_KEK=change-me-64-hex-chars
SEAWEEDFS_JWT_VOLUME_WRITE=change-me
SEAWEEDFS_JWT_VOLUME_READ=change-me
SEAWEEDFS_JWT_FILER_WRITE=change-me
SEAWEEDFS_JWT_FILER_READ=change-me
```

!!! danger "Bewahre `SEAWEEDFS_SSE_KEK` getrennt vom Server auf"
    Jedes gespeicherte Objekt ist unter diesem Schlüssel verschlüsselt. Ohne ihn lässt sich keines mehr lesen, und eine Kopie des Datenvolumes allein hilft dann nicht. Lege ihn zu deinen anderen Geheimnissen, an einen anderen Ort als die Daten (siehe [Backups & Upgrades](/de/backups.html)). Ersetze ihn nicht in einer Installation, die schon Dateien hat: Was gespeichert ist, bleibt unter dem alten Schlüssel verschlüsselt.

!!! warning "Lass `-s3.encryptVolumeData` aus"
    SeaweedFS hat einen zweiten Schalter für Verschlüsselung, `-s3.encryptVolumeData`. In Version 4.48 verträgt er sich nicht mit SSE-S3: Die Kopie eines SSE-S3-Objekts wird unlesbar ([seaweedfs/seaweedfs#11646](https://github.com/seaweedfs/seaweedfs/issues/11646)), und die Standardverschlüsselung des Buckets wird übergangen ([seaweedfs/seaweedfs#11647](https://github.com/seaweedfs/seaweedfs/issues/11647)). Hinata kopiert Objekte, zum Beispiel wenn du einen Vorgang mit Anhängen klonst. Deshalb lässt die mitgelieferte Konfiguration den Schalter aus und setzt auf SSE-S3.

Lokal (`docker-compose.dev.yml`) läuft dasselbe SeaweedFS mit festen Dev-Schlüsseln und veröffentlicht nur seine S3-API auf Loopback, unter `http://localhost:8333`. Auch hier braucht es das Profil und einmal den Setup-Job:

```bash
COMPOSE_PROFILES=local-storage docker compose -f docker-compose.dev.yml up -d
COMPOSE_PROFILES=local-storage docker compose -f docker-compose.dev.yml run --rm seaweedfs-setup
```

Die Dev-Schlüssel sind `hinata` / `hinata-dev-secret-0123456789abcdef`. Sie sind nur für deinen Rechner gedacht. Siehe [Entwicklung](/de/development.html).

## Der Bucket wird für dich erstellt

Beim ersten Upload prüft der Server, ob `HINATA_S3_BUCKET` existiert, und ruft sonst `makeBucket` auf. Beim mitgelieferten SeaweedFS hat der Job `seaweedfs-setup` ihn schon angelegt. Der Bucket bleibt **privat**, nichts wird öffentlich lesbar. Jeder Download läuft über den Server (siehe unten), nie direkt aus dem Bucket.

!!! tip
    Du kannst den Bucket auch selbst anlegen, etwa um vorher eine Lifecycle-Regel oder Bucket-Policy zu setzen. Nimm dann den Standardnamen `hinata` oder setze `HINATA_S3_BUCKET` auf deinen Namen. Ein vorhandener Bucket wird einfach mitgenutzt.

## Serverseitige Verschlüsselung

Mit `HINATA_S3_SSE=AES256` verlangt der Server für jedes Objekt, das er schreibt, SSE-S3. Beim Kopieren verlangt er es noch einmal, denn eine Kopie ist ein neues Objekt. Lass die Variable leer bei einem Speicher, der selbst verschlüsselt oder den Header nicht kennt. Jeder andere Wert hält den Server beim Start an, damit ein Tippfehler keine Dateien unverschlüsselt lässt.

Beim mitgelieferten SeaweedFS setzt du sie auf `AES256`. Der Bucket-Standard aus dem Setup-Job deckt auch Objekte ab, die ohne den Header geschrieben werden. So hängt keine Datei an nur einem der beiden.

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

Jedes Byte, das jemand hochlädt, läuft vor dem Speichern durch dieselbe Prüfung: Anhänge, Bilder in Texten, Sprachnachrichten, Avatare, das Logo und die Anhänge eingehender E-Mails. Was die Prüfung ablehnt, wird nicht gespeichert.

- **Der Inhalt entscheidet, nicht der angegebene Typ.** Der Server liest die ersten Bytes und vergleicht sie mit dem angegebenen Content-Type. Ein Programm, das sich als PDF ausgibt, wird abgelehnt. Bei Anhängen von E-Mails zählt nur der Inhalt.
- **Eine feste Liste je Art.** Anhänge dürfen PNG, JPEG, GIF, WebP, PDF, reiner Text, CSV, ZIP, JSON und Word- und Excel-Dokumente im OOXML-Format sein. Bilder in Texten sind PNG, JPEG, GIF oder WebP, Sprachnachrichten M4A, AAC, MP3, WebM, Ogg oder WAV, Avatare und das Logo PNG, JPEG, GIF oder BMP.
- **`image/svg+xml` ist bewusst ausgeschlossen.** SVG kann JavaScript enthalten (Risiko für Stored XSS).
- **Größe je Art.** Anhänge und Bilder in Texten bis `HINATA_STORAGE_MAX_UPLOAD_MB`, Sprachnachrichten bis 16 MB, Avatare bis 12 MB und das Logo bis 8 MB. Wie viele Pixel ein Bild hat, liest der Server aus seinem Kopf, bevor er es öffnet. So kann eine kleine Datei nicht ein riesiges Bild vortäuschen.
- **Dateinamen** sind höchstens 200 Zeichen lang und enthalten weder Steuerzeichen noch `/` oder `\`.
- **Namen, die ein System ausführt, werden abgelehnt**, für jede Art und unabhängig vom Inhalt: Programme, Skripte, Verknüpfungen und Webseiten wie `.exe`, `.bat`, `.ps1`, `.js`, `.lnk`, `.html` oder `.svg`. Ein Download wird so nie zu einem davon.
- **Text wird gelesen, bevor er bleibt.** Eine Text-, CSV- oder JSON-Datei liest der Server bis zu ihren ersten 8 KB. Die Bytes eines Programms lehnt er ab, ebenso einen Anfang, den ein Browser oder der Desktop ausführen würde: HTML, SVG, XML oder ein Skript.
- Ein abgelehnter Upload antwortet mit `422` und einem lokalisierten Satz. In `details` stehen `code: upload.refused` und der Grund: `type`, `signature`, `size`, `image`, `metadata`, `fileName`, `empty`, `disabled` oder `unreadable`. Jede Ablehnung zählt in die Jahreszahlen der Moderation.

Unter **Adminbereich › Moderation › Dateitypen** schaltest du ganze Gruppen ab: Bilder, PDF, Office-Dokumente, Text und Tabellen, ZIP und Sprachnachrichten. Das schränkt die Liste nur ein. Erweitern lässt sie sich nicht, SVG oder Programme kann also niemand erlauben. Avatare und das Logo bleiben davon unberührt.

Was ein Bild zeigt, prüft der Server nicht. Gemeldete Bilder prüft ein Mensch.

### Metadaten von Bildern

Ein Bild, das jemand in eine Beschreibung, einen Kommentar oder einen Artikel einfügt, sehen alle, die den Text lesen. Ein Foto vom Handy trägt in seinen EXIF-Daten oft den Ort, an dem es aufgenommen wurde. Deshalb entfernt der Server aus eingebetteten Bildern vor dem Speichern EXIF, XMP und IPTC samt GPS-Position, dazu Kommentare und Textblöcke. Er schneidet nur diese Blöcke heraus und kodiert das Bild nicht neu, Qualität und Animation (GIF, WebP) bleiben also erhalten. Ein JPEG, das laut EXIF gedreht angezeigt werden soll, behält genau das und sonst nichts, in einem kleinen EXIF-Block, damit es richtig herum steht. Neu kodiert wird auch dieses nicht, die Vorschau dreht der Server selbst. Ein Bild, dessen Blöcke sich nicht sicher lesen lassen, lehnt er ab.

**Anhänge bleiben, wie sie hochgeladen wurden.** Wer ein Foto bewusst als Datei anhängt, bekommt es mit allen Metadaten zurück. Avatare, das Logo und Vorschaubilder kodiert der Server ohnehin neu, sie tragen keine Metadaten.

### Bilder aus anderen Quellen

Beim Speichern eines Textes geht der Server jedes Bild darin durch:

- **Externe Bilder** (`http`, `https`) bleiben in Beschreibungen und Kommentaren von Vorgängen Bilder, die App lädt sie aber nie selbst. Erst wenn die lesende Person zustimmt („Einmal laden“ oder ein vertrauenswürdiger Absender, siehe [E-Mail zu Vorgang](/de/email-to-ticket.html#externe-bilder)), holt der Server das Bild und reicht es weiter. Der fremde Server sieht so nur den Server, nie die Adresse der lesenden Person. Der Server lädt nur Bilder, die im Text dieses Vorgangs stehen, nur über `http`/`https` auf den Ports 80 und 443, nie von internen Adressen, höchstens 8 MB, und nur PNG, JPEG, GIF oder WebP. In Wissensartikeln werden externe Bilder weiter zu einem Link mit dem Text „Externes Bild“. Apps, die die neue Darstellung noch nicht kennen, bekommen ebenfalls diesen Link.
- **`data:`-Bilder** laufen durch dieselbe Prüfung wie ein Upload und landen im Medienspeicher, höchstens 20 je Speichern und jedes mit bis zu 25 Megapixeln. Lehnt die Prüfung eines ab, steht an seiner Stelle „Bild nicht übernommen“. Ihr Vorschaubild entsteht, wenn es zum ersten Mal jemand ansieht.
- Bilder dieses Servers bleiben, wie sie sind. Jede andere Quelle wird ebenfalls zu „Bild nicht übernommen“.

Ein Text fasst höchstens 200 Bilder. Wer einen mit mehr speichert, bekommt eine Ablehnung, die das sagt.

!!! note "Zwei Größenobergrenzen arbeiten zusammen"
    Die Multipart-Limits von Spring (`max-file-size` / `max-request-size`, aus denselben MB-Werten) sind die äußere Grenze. Die App prüft zusätzlich Dateianzahl und Gesamtgröße. Für größere Uploads erhöhst du alle Werte gemeinsam.

## Quarantäne entfernter Inhalte

Entfernt die Moderation eine Datei oder ein Bild, kopiert der Server es im Speicher nach `quarantine/<fall>/` und löscht das Original erst danach. Ein Bild, das andere Texte noch zeigen, bleibt an seiner Stelle. Entfernte Texte und die Fassungen einer entfernten Seite kommen in die Datenbank. Die Quarantäne ist, was Moderierende im Fall sehen und was ein erfolgreicher Widerspruch zurückholt. Sonst kommt niemand daran. Endet die Aufbewahrung des Falls, löscht der Server die Quarantäne mit ihm, außer die Strafverfolgung wurde informiert. Siehe [Moderation](/de/moderation.html#aufbewahrung).

Die Kopie entsteht im Speicher selbst und läuft nie über den Server. Jeder der Anbieter unten kann das. Bei SeaweedFS bleibt `-s3.encryptVolumeData` aus, wie oben beschrieben.

## Einen externen Anbieter verwenden

Leere das Compose-Profil in `.env`, um das mitgelieferte SeaweedFS abzuschalten:

```properties
COMPOSE_PROFILES=
```

Konfiguriere dann einen der Anbieter unten. Die Variablen `SEAWEEDFS_*` brauchst du nicht mehr. Die Compose-Datei setzt `HINATA_S3_ADDRESSING_STYLE` für den mitgelieferten Speicher auf `path`. Setze den Wert für einen externen Anbieter deshalb auf `auto`, außer dein Anbieter verlangt etwas anderes.

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
- **`HINATA_S3_ADDRESSING_STYLE`** steuert die Adressierung der S3-URLs. Der Server selbst nimmt standardmäßig `auto`, die Compose-Datei setzt `path`. `auto` wählt Virtual Host Style für AWS und Path Style für alle anderen, das passt fast immer. Verlangt dein Anbieter etwas anderes, setze `path` oder `virtual-host`.
- Nutze HTTPS für jeden Endpunkt, der über das Netzwerk geht.
- Die Zugangsdaten brauchen `PutObject`, `GetObject`, `DeleteObject`, `ListBucket` und `CreateBucket` (Letzteres nur, wenn du den Bucket nicht selbst anlegst). Bei Azure gelten die entsprechenden Rechte, auch der Container wird automatisch angelegt.
- Ohne Konfiguration (leerer Access Key oder leerer Connection String bei `provider=azure`) antworten die Endpunkte für Anhänge und Avatare mit `error.storage.notConfigured`. Der Rest von Hinata funktioniert, nur Uploads gehen nicht.
- **Ein Anbieterwechsel verschiebt keine vorhandenen Objekte.** Hat die Instanz schon Daten, kopiere zuerst den Bucket (`rclone sync`, `aws s3 sync`, `azcopy`). Die Objektschlüssel bleiben gleich, in der Datenbank ändert sich also nichts.

!!! tip "Halte Buckets privat"
    Halte den Bucket bei jedem Anbieter **privat**. Hinata gibt immer kurzlebige presignte URLs aus und braucht nie öffentlichen Lesezugriff. Der würde nur die Angriffsfläche vergrößern.

## Von MinIO zu SeaweedFS umziehen

Eine Installation, auf der noch das mitgelieferte MinIO läuft, zieht ihre Dateien einmal um. Der Ablauf: SeaweedFS neben MinIO starten, jedes Objekt mit [rclone](https://rclone.org) kopieren, vergleichen, den Server auf SeaweedFS umstellen und MinIO erst stilllegen, wenn du das Ergebnis geprüft hast. MinIO bleibt bis zum Schluss unangetastet, du kannst also jederzeit zurück.

1. **Erst sichern.** Ziehe einen Datenbank-Dump und eine Kopie des Buckets, wie unter [Backups & Upgrades](/de/backups.html) beschrieben.
2. **MinIO weiterlaufen lassen.** Die neue `docker-compose.yml` hat keinen Dienst `minio` mehr. Übernimm deine bisherige Definition in die `docker-compose.override.yml`, damit Compose ihn weiter verwaltet, mit demselben Volume, damit die Daten bleiben, wo sie sind:

    ```yaml
    services:
      minio:
        image: minio/minio:<der Tag, den du heute nutzt>
        command: server /data
        environment:
          MINIO_ROOT_USER: ${MINIO_ROOT_USER}
          MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
        volumes:
          - minio-data:/data
        networks: [hinata]
    volumes:
      minio-data:
    ```

3. **Trage die SeaweedFS-Geheimnisse** in `.env` ein: Führe `./deploy/generate-secrets.sh` aus, übernimm die Werte `SEAWEEDFS_*` und ein neues `HINATA_S3_SECRET_KEY`, setze `HINATA_S3_ACCESS_KEY=hinata` und `HINATA_S3_SSE=AES256`, und lege eine Kopie von `SEAWEEDFS_SSE_KEK` an einen anderen Ort. `MINIO_ROOT_*` behältst du vorerst. Erzeuge `hinata-server` noch nicht neu. Er liest weiter aus MinIO, mit den Einstellungen, mit denen er gestartet wurde.
4. **Starte SeaweedFS** und führe den Setup-Job aus:

    ```bash
    docker compose up -d seaweedfs
    docker compose run --rm seaweedfs-setup
    ```

5. **Kopiere jedes Objekt**, beim Schreiben verschlüsselt. rclone läuft im Netzwerk des Stacks (`hinata_hinata` beim Standard-Projektnamen) und wird nur über Umgebungsvariablen eingerichtet, so landet kein Schlüssel in einer Datei oder in deiner Shell-Historie:

    ```bash
    set -a; . ./.env; set +a
    rclone() {
      docker run --rm --network hinata_hinata \
        -e RCLONE_CONFIG_SRC_TYPE=s3 -e RCLONE_CONFIG_SRC_PROVIDER=Minio \
        -e RCLONE_CONFIG_SRC_ENDPOINT=http://minio:9000 \
        -e RCLONE_CONFIG_SRC_ACCESS_KEY_ID="$MINIO_ROOT_USER" \
        -e RCLONE_CONFIG_SRC_SECRET_ACCESS_KEY="$MINIO_ROOT_PASSWORD" \
        -e RCLONE_CONFIG_DST_TYPE=s3 -e RCLONE_CONFIG_DST_PROVIDER=SeaweedFS \
        -e RCLONE_CONFIG_DST_ENDPOINT=http://seaweedfs:8333 \
        -e RCLONE_CONFIG_DST_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
        -e RCLONE_CONFIG_DST_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
        -e RCLONE_CONFIG_DST_SERVER_SIDE_ENCRYPTION=AES256 \
        rclone/rclone:1.71 "$@"
    }
    rclone sync src:hinata dst:hinata --checksum --transfers 8
    ```

    Das kannst du beliebig oft wiederholen. Kopiert wird nur, was sich geändert hat.

6. **Vergleiche.** Die Zahl der Objekte muss gleich sein, und die Prüfung darf keine Unterschiede melden:

    ```bash
    rclone size src:hinata
    rclone size dst:hinata
    rclone check src:hinata dst:hinata --one-way --size-only
    ```

7. **Stelle um.** Führe direkt davor noch einmal `sync` aus, damit auch die Uploads aus der Zwischenzeit mitkommen. Erzeuge dann nur den Server neu. Überschreibt `.env` den `HINATA_S3_ENDPOINT` nicht, zeigen ihn die Compose-Standardwerte auf `http://seaweedfs:8333` mit Path-Adressierung:

    ```bash
    docker compose up -d --no-deps --force-recreate hinata-server
    ```

    Öffne in der App ein paar Anhänge und Avatare. Stimmt etwas nicht, stelle den Server zurück auf MinIO (`HINATA_S3_ENDPOINT=http://minio:9000` und die alten Schlüssel) und erzeuge ihn genauso neu. MinIO hat noch alles.

8. **Lege MinIO still**, wenn du zufrieden bist: Halte seinen Container mit `docker compose rm -sf minio` an und entferne ihn, lösche dann den Dienst `minio` und das Volume aus der `docker-compose.override.yml` und die Zeilen `MINIO_ROOT_*` aus `.env`. Das Volume selbst bleibt, bis du es bewusst löschst (`docker volume rm hinata_minio-data`). Tu das erst, wenn der Server eine Weile auf SeaweedFS gelaufen ist und ein Backup des neuen Buckets existiert.

Die Objektschlüssel bleiben gleich, in der Datenbank ändert sich also nichts.

Alle Variablen stehen in der [Konfigurationsreferenz](/de/configuration.html), die Datenbank unter [MongoDB & X.509](/de/database.html).
