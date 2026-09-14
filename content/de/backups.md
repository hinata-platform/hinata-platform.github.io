---
title: Backups & Upgrades
description: Sichere MongoDB, MinIO und deine Secrets, stelle sie wieder her und aktualisiere Server und App, ohne die Datendienste anzufassen.
---

# Backups & Upgrades

Dein gesamter Zustand steckt in drei Dingen. Sichere alle drei:

- **MongoDB:** alle Daten
- **MinIO/S3:** Anhänge und Avatare
- **Secrets:** `.env`, das Mongo-Keyfile und die X.509-PKI

Upgrades heben nur Image-Tags an. Die Datendienste werden dabei nicht neu erstellt.

!!! danger "Diese Secrets darfst du nie verlieren"

    - **`HINATA_JWT_SECRET`:** Ohne es wird jedes ausgestellte Token ungültig. **Alle Benutzer werden abgemeldet** und müssen sich neu anmelden.
    - **Mongo-Keyfile und X.509-PKI** (`deploy/mongo-keyfile`, `deploy/x509/prod`): Ohne sie können sich die Mitglieder des Replica Sets nicht anmelden, und der Server kann sich nicht verbinden. **Die Authentifizierung bricht.** Passend zu bestehenden Daten lassen sie sich nicht neu erzeugen.
    - **`MONGO_ROOT_PASSWORD` / `MINIO_ROOT_PASSWORD`:** Ohne sie kannst du die wiederhergestellten Datenbanken nicht verwalten.

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

Die Produktion nutzt **TLS + X.509**, also muss `mongodump` TLS sprechen und sich anmelden. Am einfachsten läuft es **im** Mongo-Container mit dem SCRAM-Root-Konto, denselben Zugangsdaten wie beim Healthcheck und bei `init-prod-user.sh`.

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

Das schreibt ein einzelnes, gut komprimierbares Archiv auf den Host. Passe den Containernamen an. `docker compose ps` zeigt ihn, das Compose-Projekt heißt `hinata`.

!!! tip "Ein Dump gegen ein laufendes Replica Set ist sicher"
    `mongodump` liest einen konsistenten Snapshot im laufenden Betrieb. Du kannst es nach Zeitplan gegen den Primary ausführen, ohne den Stack zu stoppen.

## MinIO / S3 sichern

Anhänge und Avatare liegen im S3-Bucket, MongoDB speichert nur die Objektschlüssel. Sichere den Bucket mit dem MinIO-Client `mc`:

```bash
# Einmalig einen Alias für dein MinIO konfigurieren (nutze deine MINIO_ROOT_USER / _PASSWORD)
mc alias set hinata http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# Den Bucket in ein lokales Backup-Verzeichnis spiegeln (inkrementell)
mc mirror --overwrite --remove hinata/hinata ./backups/minio/hinata
```

Für eine Kopie außer Haus spiegelst du auf ein anderes S3-Ziel, etwa ein zweites MinIO oder einen Bucket in der Cloud. Siehe [Objektspeicher (S3/MinIO)](/de/storage.html).

## Secrets & PKI sichern

Diese Dateien sind klein und unersetzlich. Lege sie an einen sicheren Ort, etwa einen Secrets-Manager oder einen verschlüsselten Tresor:

```bash
# Vom Wurzelverzeichnis des Server-Repos
tar czf backups/hinata-secrets-$(date +%F).tar.gz \
  .env \
  deploy/mongo-keyfile \
  deploy/x509/prod
```

!!! warning "Secrets getrennt von Daten-Dumps aufbewahren"
    Lege das Secrets-Archiv an einen anderen, geschützten Ort als die Dumps von MongoDB und MinIO. Wer `.env`, PKI und einen Datendump hat, hat deine ganze Plattform. Verschlüssele das Archiv und beschränke, wer es lesen darf.

## Ein empfohlenes Cron-Backup

Ein Skript für alle drei Backups. Es behält 14 tägliche Snapshots und löscht ältere:

```bash
#!/usr/bin/env bash
# /opt/hinata/backup.sh: täglich per Cron ausführen
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

Reihenfolge: **Secrets wiederherstellen → Mongo und MinIO starten → Daten wiederherstellen → Server und App starten**.

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
    Der X.509-Subject-DN ist als Mongo-Benutzer registriert. Stelle deshalb auf **derselben** PKI wieder her, die du gesichert hast, oder registriere den DN neu mit `./deploy/x509/init-prod-user.sh`. Sonst kann sich der Server nicht anmelden.

## Upgrade

Ein Upgrade hebt nur den Image-Tag an. Server und App kommen von GHCR, die Datendienste (Mongo, MinIO) bleiben unverändert.

```bash
# 1) Die gewünschten Versionen festpinnen (in .env)
#    HINATA_SERVER_TAG={{version}}
#    HINATA_APP_TAG={{version}}

# 2) Die neuen Images ziehen
docker compose pull hinata-server hinata-app

# 3) NUR App und Server neu erstellen
docker compose up -d --no-deps hinata-server hinata-app
```

!!! danger "Bei einem Upgrade niemals die Datendienste neu erstellen oder prunen"
    Ein Redeploy in der Produktion berührt **nur** `hinata-server` und `hinata-app`. Das MongoDB-Replica-Set und MinIO bleiben **online**.

    - Kein vollständiges `docker compose up`, das jeden Dienst neu erstellt.
    - Nie prune oder down und up, das die Volumes `mongo*-data` oder `minio-data` löschen könnte.
    - Nutze `--no-deps`, damit Compose Mongo und MinIO nicht als Abhängigkeiten neu startet.

!!! tip "Direkt vor dem Upgrade ein Backup ziehen"
    Führe zuerst dein Backup-Skript aus. Mit frischem MongoDB-Dump und aktueller `.env` rollst du sofort zurück, falls ein neuer Tag Probleme macht.

### Zurückrollen

Derselbe Ablauf mit dem vorherigen Tag:

```bash
# HINATA_SERVER_TAG / HINATA_APP_TAG zurück auf das letzte funktionierende Release setzen, dann:
docker compose pull hinata-server hinata-app
docker compose up -d --no-deps hinata-server hinata-app
```

Mit festen Tags statt `latest` ist eine funktionierende Version immer nur eine Änderung entfernt.

## Health-Checks

Prüfe nach jedem Upgrade und jeder Wiederherstellung, ob der Server läuft:

```bash
# Lokal (auf dem Host)
curl -s http://127.0.0.1:3356/actuator/health
# → {"status":"UP"}

# Über den Proxy
curl -s https://api.track.example.com/actuator/health
```

`/actuator/health` braucht kein Token und eignet sich für Liveness- und Readiness-Probes eines Orchestrators. `DOWN` heißt meist, dass MongoDB oder MinIO nicht erreichbar sind. Prüfe dann, ob die Datendienste laufen und ob PKI und Zugangsdaten zusammenpassen.

## Nächste Schritte

- [Produktiv-Deployment](/de/deployment.html): der vollständige Stack und der Ablauf beim Deploy
- [Konfigurationsreferenz](/de/configuration.html): jede Umgebungsvariable
- [MongoDB & X.509](/de/database.html): Replica Set und PKI im Detail
- [Objektspeicher (S3/MinIO)](/de/storage.html): Buckets, Schlüssel und presignte Downloads
