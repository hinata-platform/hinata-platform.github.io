---
title: Backups & Upgrades
description: Betreibe einen Hinata-Stack über die Zeit — sichere MongoDB, MinIO und deine Secrets, stelle sie sicher wieder her und aktualisiere oder rolle Server und App zurück, ohne die Datendienste anzufassen.
---

# Backups & Upgrades

Einen Hinata-Stack aufzusetzen ist eine einmalige Aufgabe; ihn gesund zu halten
ist die fortlaufende. Drei Dinge tragen deinen gesamten Zustand — **MongoDB**
(alle Daten), **MinIO/S3** (Anhänge und Avatare) und deine **Secrets** (`.env`,
das Mongo-Keyfile und die X.509-PKI). Sichere alle drei und wisse, wie du
Image-Tags anhebst, ohne die Datendienste neu zu erstellen. Genau darum geht es
auf dieser Seite.

!!! danger "Die drei Dinge, die dir den Tag ruinieren, wenn sie verloren gehen"
    - **`HINATA_JWT_SECRET`** — verlierst du es, wird jedes ausgestellte Token
      ungültig; **alle Benutzer werden ausgeloggt** und müssen sich erneut
      anmelden.
    - **Das Mongo-Keyfile + die X.509-PKI** (`deploy/mongo-keyfile`, `deploy/x509/prod`)
      — verlierst du sie, kann sich das Replica Set nicht mehr gegenseitig
      authentifizieren und der Server kann sich nicht verbinden. **Die
      Authentifizierung bricht.** Diese lassen sich nicht so neu erzeugen, dass
      sie zu den bestehenden Daten passen.
    - **`MONGO_ROOT_PASSWORD` / `MINIO_ROOT_PASSWORD`** — verlierst du sie, kannst
      du die gerade wiederhergestellten Datenbanken nicht administrieren.

    Ein Datenbank-Backup ohne diese Secrets ist nur ein halbes Backup.

## Was zu sichern ist

| Was | Wo es liegt | Wie |
| --- | --- | --- |
| Alle Anwendungsdaten | MongoDB-Replica-Set | `mongodump` (unten) |
| Anhänge & Avatare | MinIO/S3-Bucket (`HINATA_S3_BUCKET`, Standard `hinata`) | `mc mirror` / Bucket-Sync |
| Secrets & Konfiguration | `.env` | in einen Secret-Store kopieren |
| Cluster-Auth-Keyfile | `deploy/mongo-keyfile` | kopieren (Modus `400`) |
| MongoDB-TLS/X.509-PKI | `deploy/x509/prod/` | das ganze Verzeichnis kopieren |

## MongoDB sichern

Die Produktion läuft als Replica Set mit **TLS + X.509**, daher muss `mongodump`
TLS sprechen und sich authentifizieren. Der einfachste zuverlässige Ansatz ist,
es **innerhalb** eines Mongo-Containers mit dem SCRAM-Root-Konto auszuführen (die
gleichen Zugangsdaten, die der Healthcheck und `init-prod-user.sh` verwenden) und
in einen gemounteten Pfad zu dumpen.

```bash
# Die 'hinata'-Datenbank vom Primary über TLS nach ./backups auf dem Host dumpen
docker exec hinata-mongo1-1 sh -c '
  mongodump \
    --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin \
    --db hinata \
    --archive' > "backups/hinata-$(date +%F).archive"
```

Das streamt ein einzelnes, gut komprimierbares Archiv auf den Host. Passe den
Container-Namen an dein Projekt an (`docker compose ps` zeigt ihn — das
Compose-Projekt heißt `hinata`).

!!! tip "Ein Dump gegen ein laufendes Replica Set ist sicher"
    `mongodump` liest einen konsistenten Snapshot, ohne den Server zu stoppen, du
    kannst es also nach Zeitplan gegen den laufenden Primary ausführen. Es gibt
    keinen Grund, den Stack für ein Backup offline zu nehmen.

## MinIO / S3 sichern

Anhänge und Avatare liegen im S3-Bucket, nicht in MongoDB — Mongo speichert nur
die Objekt-Keys. Sichere den Bucket separat mit dem MinIO-Client `mc`:

```bash
# Einmalig einen Alias für dein MinIO konfigurieren (nutze deine MINIO_ROOT_USER / _PASSWORD)
mc alias set hinata http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# Den Bucket in ein lokales Backup-Verzeichnis spiegeln (inkrementell)
mc mirror --overwrite --remove hinata/hinata ./backups/minio/hinata
```

Für Offsite-Beständigkeit spiegele auf ein anderes S3-Ziel (z. B. ein zweites
MinIO oder einen Cloud-Bucket) statt auf einen lokalen Pfad. Siehe
[Objektspeicher (S3/MinIO)](/de/storage.html).

## Secrets & PKI sichern

Diese sind klein, statisch und unersetzlich — kopiere sie an einen sicheren Ort
(einen Secrets-Manager, einen verschlüsselten Tresor):

```bash
# Vom Wurzelverzeichnis des Server-Repos
tar czf backups/hinata-secrets-$(date +%F).tar.gz \
  .env \
  deploy/mongo-keyfile \
  deploy/x509/prod
```

!!! warning "Secrets getrennt von Daten-Dumps aufbewahren"
    Halte das Secrets-Archiv an einem anderen, zugriffsgeschützten Ort als deine
    MongoDB-/MinIO-Dumps. Wer `.env` + die PKI + einen Daten-Dump hat, hat deine
    gesamte Plattform. Verschlüssele im Ruhezustand und beschränke, wer es lesen
    darf.

## Ein empfohlenes Cron-Backup

Fasse die drei Backups hinter einem Skript zusammen und plane es ein. Dieses
behält 14 tägliche Snapshots und entfernt ältere:

```bash
#!/usr/bin/env bash
# /opt/hinata/backup.sh — täglich per Cron ausführen
set -euo pipefail
cd /opt/hinata/hinata-server
DEST="/opt/hinata/backups/$(date +%F)"
mkdir -p "$DEST/minio"

# 1) MongoDB (TLS + SCRAM-Root im Container)
docker exec hinata-mongo1-1 sh -c '
  mongodump --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin --db hinata --archive' \
  > "$DEST/hinata.archive"

# 2) Anhänge-Bucket
mc mirror --overwrite --remove hinata/hinata "$DEST/minio/hinata"

# 3) Secrets & PKI
tar czf "$DEST/secrets.tar.gz" .env deploy/mongo-keyfile deploy/x509/prod

# Die letzten 14 Tage behalten
find /opt/hinata/backups -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
```

```cron
# Täglich um 03:30
30 3 * * * /opt/hinata/backup.sh >> /var/log/hinata-backup.log 2>&1
```

## Wiederherstellen

Die Reihenfolge auf hoher Ebene ist: **Secrets wiederherstellen → Mongo + MinIO
hochfahren → Daten wiederherstellen → Server + App starten**.

```bash
# 1) Secrets & PKI ins Repo zurückspielen (damit sich der Cluster authentifizieren kann)
tar xzf backups/hinata-secrets-YYYY-MM-DD.tar.gz

# 2) NUR die Datendienste hochfahren
docker compose up -d mongo1 mongo2 mongo-arbiter minio

# 3) MongoDB aus dem Archiv wiederherstellen
docker exec -i hinata-mongo1-1 sh -c '
  mongorestore --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin \
    --drop --archive' < backups/hinata-YYYY-MM-DD.archive

# 4) Den Anhänge-Bucket wiederherstellen
mc mirror --overwrite ./backups/minio/hinata hinata/hinata

# 5) Die Anwendung starten
docker compose up -d hinata-server hinata-app
```

!!! note "Auf passende PKI wiederherstellen"
    Weil der X.509-Subject-DN als Mongo-Benutzer registriert ist, stelle deine
    Daten auf **derselben** PKI wieder her, die du gesichert hast (oder registriere
    den DN neu mit `./deploy/x509/init-prod-user.sh`). Daten mit einem nicht
    passenden Zertifikat wiederherzustellen lässt den Server ohne Möglichkeit zur
    Authentifizierung zurück.

## Upgrade

Ein Upgrade ist nur ein Anheben des Image-Tags. Server und App werden von GHCR
gezogen; die Datendienste (Mongo, MinIO) bleiben exakt, wie sie sind.

```bash
# 1) Die gewünschten Versionen festpinnen (in .env)
#    HINATA_SERVER_TAG=2.2.0
#    HINATA_APP_TAG=2.2.0

# 2) Die neuen Images ziehen
docker compose pull hinata-server hinata-app

# 3) NUR App und Server neu erstellen
docker compose up -d --no-deps hinata-server hinata-app
```

!!! danger "Bei einem Upgrade niemals die Datendienste neu erstellen oder prunen"
    Ein Produktiv-Redeploy berührt **nur** `hinata-server` und `hinata-app`. Halte
    das MongoDB-Replica-Set und MinIO **online** — führe kein vollständiges
    `docker compose up` aus, das jeden Dienst neu erstellt, und übergib niemals ein
    prune/down-and-up, das die Volumes `mongo*-data` oder `minio-data` löschen
    könnte. Nutze `--no-deps`, damit Compose Mongo/MinIO nicht als Abhängigkeiten
    neu startet.

!!! tip "Direkt vor dem Upgrade ein Backup ziehen"
    Führe zuerst dein Backup-Skript aus. Ein frischer MongoDB-Dump plus die
    aktuelle `.env` erlaubt dir, sofort zurückzurollen, falls sich ein neuer Tag
    danebenbenimmt.

### Zurückrollen

Rollback ist derselbe Vorgang mit dem vorherigen Tag:

```bash
# HINATA_SERVER_TAG / HINATA_APP_TAG zurück auf das letzte funktionierende Release setzen, dann:
docker compose pull hinata-server hinata-app
docker compose up -d --no-deps hinata-server hinata-app
```

Weil du explizite Tags festpinnst, statt dich auf `latest` zu verlassen, ist eine
bekannt-gute Version immer nur eine Änderung entfernt.

## Health-Checks

Bestätige nach jedem Upgrade oder jeder Wiederherstellung, dass der Server läuft,
bevor du den Sieg verkündest:

```bash
# Lokal (auf dem Host)
curl -s http://127.0.0.1:3356/actuator/health
# → {"status":"UP"}

# Über den Proxy
curl -s https://api.track.example.com/actuator/health
```

`/actuator/health` ist ein öffentlicher Endpunkt (kein Token) und ideal für
Liveness-/Readiness-Probes eines Orchestrators. Ein `DOWN`-Status deutet meist auf
die MongoDB- oder MinIO-Konnektivität hin — prüfe, dass die Datendienste laufen und
dass deine PKI und deine Zugangsdaten zusammenpassen.

## Nächste Schritte

- [Produktiv-Deployment](/de/deployment.html) — der vollständige Stack und der Deploy-Ablauf
- [Konfigurationsreferenz](/de/configuration.html) — jede Umgebungsvariable
- [MongoDB & X.509](/de/database.html) — das Replica Set und die PKI im Detail
- [Objektspeicher (S3/MinIO)](/de/storage.html) — Buckets, Keys und presignte Downloads
