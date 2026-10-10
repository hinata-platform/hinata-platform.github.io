---
title: Backups & Upgrades
description: Sichere MongoDB, den Datei-Bucket und deine Secrets, stelle sie wieder her und aktualisiere Server und App, ohne die Datendienste anzufassen.
---

# Backups & Upgrades

Dein gesamter Zustand steckt in drei Dingen. Sichere alle drei:

- **MongoDB:** alle Daten
- **Objektspeicher (SeaweedFS oder dein S3-Anbieter):** Anhänge und Avatare
- **Secrets:** `.env`, das Mongo-Keyfile und die X.509-PKI

Upgrades heben nur Image-Tags an. Die Datendienste werden dabei nicht neu erstellt.

!!! danger "Diese Secrets darfst du nie verlieren"

    - **`HINATA_JWT_SECRET`:** Ohne es wird jedes ausgestellte Token ungültig. **Alle Benutzer werden abgemeldet** und müssen sich neu anmelden.
    - **Mongo-Keyfile und X.509-PKI** (`deploy/mongo-keyfile`, `deploy/x509/prod`): Ohne sie können sich die Mitglieder des Replica Sets nicht anmelden, und der Server kann sich nicht verbinden. **Die Authentifizierung bricht.** Passend zu bestehenden Daten lassen sie sich nicht neu erzeugen.
    - **`MONGO_ROOT_PASSWORD`:** Ohne es kannst du die wiederhergestellte Datenbank nicht verwalten.
    - **`SEAWEEDFS_SSE_KEK`:** Jedes Objekt im mitgelieferten SeaweedFS ist unter diesem Schlüssel verschlüsselt. Ohne ihn lassen sich die Dateien auf dem Datenvolume nicht lesen. Bewahre eine Kopie getrennt vom Server und von den Daten auf.

    Ein Datenbank-Backup ohne diese Secrets ist nur ein halbes Backup.

## Was zu sichern ist

| Was | Wo es liegt | Wie |
| --- | --- | --- |
| Alle Anwendungsdaten | MongoDB-Replica-Set | `mongodump` (unten) |
| Anhänge & Avatare | Bucket `HINATA_S3_BUCKET` (Standard `hinata`) in SeaweedFS oder bei deinem S3-Anbieter | `rclone sync` (unten) |
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

## Den Bucket sichern

Anhänge und Avatare liegen im Bucket, MongoDB speichert nur die Objektschlüssel. Das mitgelieferte SeaweedFS veröffentlicht keinen Port. Eine Kopie läuft deshalb als kurzlebiger [rclone](https://rclone.org)-Container im Netzwerk des Stacks (`hinata_hinata` beim Standard-Projektnamen):

```bash
# Aus dem Wurzelverzeichnis des Server-Repos, damit die Schlüssel aus .env kommen
set -a; . ./.env; set +a
docker run --rm --network hinata_hinata \
  -v "$PWD/backups/files:/files" \
  -e RCLONE_CONFIG_SRC_TYPE=s3 -e RCLONE_CONFIG_SRC_PROVIDER=SeaweedFS \
  -e RCLONE_CONFIG_SRC_ENDPOINT=http://seaweedfs:8333 \
  -e RCLONE_CONFIG_SRC_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
  -e RCLONE_CONFIG_SRC_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
  rclone/rclone:1.71 sync src:hinata /files --checksum --transfers 8
```

`sync` arbeitet inkrementell: Es wird nur kopiert, was sich geändert hat. Bei einem externen Anbieter nimmst du stattdessen dessen Endpunkt und Schlüssel, oder seine eigene Replikation.

!!! warning "Die Kopie ist nicht verschlüsselt"
    SeaweedFS entschlüsselt die Dateien, wenn es sie herausgibt. Im Verzeichnis liegen sie also im Klartext. Verschlüssele es, bevor es den Host verlässt, zum Beispiel mit restic wie unten, und halte es so privat wie den Datenbank-Dump.

!!! tip "Ein Schlüssel, der nur lesen darf"
    Das Startskript von SeaweedFS kennt eine optionale dritte Identität für Backups. Sie darf den Bucket lesen und auflisten, sonst nichts. So kann ein Backup-Job nie verändern, was er kopiert. Setze `SEAWEEDFS_BACKUP_ACCESS_KEY` und `SEAWEEDFS_BACKUP_SECRET_KEY` in `.env`. Die mitgelieferte `docker-compose.yml` reicht sie nicht an den Container weiter. Ergänze sie deshalb in der `docker-compose.override.yml` und erzeuge `seaweedfs` neu:

    ```yaml
    services:
      seaweedfs:
        environment:
          SEAWEEDFS_BACKUP_ACCESS_KEY: ${SEAWEEDFS_BACKUP_ACCESS_KEY}
          SEAWEEDFS_BACKUP_SECRET_KEY: ${SEAWEEDFS_BACKUP_SECRET_KEY}
    ```

    Nutze dann diese Schlüssel im `rclone`-Aufruf statt der des Servers.

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
    Lege das Secrets-Archiv an einen anderen, geschützten Ort als den MongoDB-Dump und die Dateikopie. Wer `.env`, PKI und einen Datendump hat, hat deine ganze Plattform. Verschlüssele das Archiv und beschränke, wer es lesen darf.

## Ein empfohlenes Cron-Backup

Ein Skript für alle drei Backups. Es behält 14 tägliche Snapshots und löscht ältere:

```bash
#!/usr/bin/env bash
# /opt/hinata/backup.sh: täglich per Cron ausführen
set -euo pipefail
cd /opt/hinata/hinata-server
DEST="/opt/hinata/backups/$(date +%F)"
mkdir -p "$DEST/files"

# 1) MongoDB (TLS + SCRAM-Root im Container)
docker exec hinata-mongo1-1 sh -c '
  mongodump --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin --db hinata --archive' \
  > "$DEST/hinata.archive"

# 2) Anhänge-Bucket (mitgeliefertes SeaweedFS, über das Netzwerk des Stacks)
set -a; . ./.env; set +a
docker run --rm --network hinata_hinata -v "$DEST/files:/files" \
  -e RCLONE_CONFIG_SRC_TYPE=s3 -e RCLONE_CONFIG_SRC_PROVIDER=SeaweedFS \
  -e RCLONE_CONFIG_SRC_ENDPOINT=http://seaweedfs:8333 \
  -e RCLONE_CONFIG_SRC_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
  -e RCLONE_CONFIG_SRC_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
  rclone/rclone:1.71 sync src:hinata /files --checksum --quiet

# 3) Secrets & PKI
tar czf "$DEST/secrets.tar.gz" .env deploy/mongo-keyfile deploy/x509/prod

# Die letzten 14 Tage behalten
find /opt/hinata/backups -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
```

```cron
# Täglich um 03:30
30 3 * * * /opt/hinata/backup.sh >> /var/log/hinata-backup.log 2>&1
```

## Außer Haus mit restic

Eine Kopie auf demselben Host übersteht den Verlust dieses Hosts nicht. Das Server-Repo bringt in `deploy/backup/` ein vollständigeres Beispiel mit: `backup.sh` für den nächtlichen Lauf und `restore-test.sh`, das zeigt, dass sich das Backup zurückspielen lässt. Der Ansatz, den du an deine Umgebung anpassen kannst:

- **Die Datenbank** wird mit `mongodump --archive --gzip` gesichert und direkt in [restic](https://restic.net) gestreamt, ohne je auf der Platte zu landen. Der Dump läuft über TLS als X.509-Benutzer, der die Datenbank nur lesen darf.
- **Die Dateien** kopiert rclone mit der Nur-Lese-Identität von SeaweedFS in ein Staging-Verzeichnis, das nur root lesen kann. Es bleibt zwischen den Läufen erhalten, so wandern nur Änderungen. restic sichert danach dieses Verzeichnis.
- **restic verschlüsselt alles**, bevor es den Host verlässt. Das Repository liegt auf einer anderen Maschine hinter einem REST-Server im Append-only-Modus: Dieser Host kann Snapshots hinzufügen, aber keinen ändern oder löschen. Die Aufbewahrung regelt die Backup-Maschine.
- **Ein Fehler fällt auf.** Scheitert der Dump, scheitert der ganze Lauf, statt einen leeren Snapshot zu hinterlassen. Jeder Lauf schreibt sein Ergebnis in ein Log.

`restore-test.sh` prüft die neuesten Snapshots, ohne den laufenden Stack anzufassen. Es spielt die Datenbank in eine Wegwerf-MongoDB in einem Wegwerf-Netzwerk zurück und stellt die Zahl der Collections und Dokumente neben die des Live-Systems. Die Dateien stellt es in ein Wegwerf-Verzeichnis wieder her und vergleicht Anzahl und Bytes mit der Staging-Kopie. Es gibt nur Zahlen aus und räumt danach alles Temporäre weg. Lass es regelmäßig laufen, nicht erst, wenn du das Backup brauchst.

## Wiederherstellen

Reihenfolge: **Secrets wiederherstellen → Mongo und SeaweedFS starten → Daten wiederherstellen → Server und App starten**.

```bash
# 1) Secrets & PKI ins Repo zurückspielen (damit sich der Cluster authentifizieren kann)
tar xzf backups/hinata-secrets-YYYY-MM-DD.tar.gz

# 2) NUR die Datendienste hochfahren und den Bucket vom Setup-Job anlegen lassen
docker compose up -d mongo1 mongo2 mongo-arbiter seaweedfs
docker compose run --rm seaweedfs-setup

# 3) MongoDB aus dem Archiv wiederherstellen
docker exec -i hinata-mongo1-1 sh -c '
  mongorestore --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin \
    --drop --archive' < backups/hinata-YYYY-MM-DD.archive

# 4) Den Anhänge-Bucket wiederherstellen (beim Schreiben wieder verschlüsselt)
set -a; . ./.env; set +a
docker run --rm --network hinata_hinata -v "$PWD/backups/files:/files:ro" \
  -e RCLONE_CONFIG_DST_TYPE=s3 -e RCLONE_CONFIG_DST_PROVIDER=SeaweedFS \
  -e RCLONE_CONFIG_DST_ENDPOINT=http://seaweedfs:8333 \
  -e RCLONE_CONFIG_DST_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
  -e RCLONE_CONFIG_DST_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
  -e RCLONE_CONFIG_DST_SERVER_SIDE_ENCRYPTION=AES256 \
  rclone/rclone:1.71 copy /files dst:hinata --transfers 8

# 5) Die Anwendung starten
docker compose up -d hinata-server hinata-app
```

!!! note "Auf passende PKI wiederherstellen"
    Der X.509-Subject-DN ist als Mongo-Benutzer registriert. Stelle deshalb auf **derselben** PKI wieder her, die du gesichert hast, oder registriere den DN neu mit `./deploy/x509/init-prod-user.sh`. Sonst kann sich der Server nicht anmelden.

## Upgrade

Ein Upgrade hebt nur den Image-Tag an. Server und App kommen von GHCR, die Datendienste (Mongo, SeaweedFS) bleiben unverändert.

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
    Ein Redeploy in der Produktion berührt **nur** `hinata-server` und `hinata-app`. Das MongoDB-Replica-Set und SeaweedFS bleiben **online**.

    - Kein vollständiges `docker compose up`, das jeden Dienst neu erstellt.
    - Nie prune oder down und up, das die Volumes `mongo*-data` oder `seaweedfs-data` löschen könnte.
    - Nutze `--no-deps`, damit Compose Mongo und SeaweedFS nicht als Abhängigkeiten neu startet.

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

`/actuator/health` braucht kein Token und eignet sich für Liveness- und Readiness-Probes eines Orchestrators. `DOWN` heißt meist, dass MongoDB oder der Objektspeicher nicht erreichbar sind. Prüfe dann, ob die Datendienste laufen und ob PKI und Zugangsdaten zusammenpassen.

## Nächste Schritte

- [Produktiv-Deployment](/de/deployment.html): der vollständige Stack und der Ablauf beim Deploy
- [Konfigurationsreferenz](/de/configuration.html): jede Umgebungsvariable
- [MongoDB & X.509](/de/database.html): Replica Set und PKI im Detail
- [Objektspeicher](/de/storage.html): SeaweedFS, andere Anbieter und der Umzug von MinIO
