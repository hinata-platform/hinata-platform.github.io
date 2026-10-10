---
title: Backups & upgrades
description: Back up MongoDB, the file bucket and your secrets, restore them, and upgrade or roll back the server and app without touching the data services.
---

# Backups & upgrades

All your state lives in three places. Back up all three:

- **MongoDB:** all data
- **Object storage (SeaweedFS or your S3 provider):** attachments and avatars
- **Secrets:** `.env`, the Mongo keyfile and the X.509 PKI

Upgrades only bump image tags. The data services are never recreated.

!!! danger "Secrets you must never lose"

    - **`HINATA_JWT_SECRET`:** without it every issued token becomes invalid. **All users are logged out** and must sign in again.
    - **The Mongo keyfile and X.509 PKI** (`deploy/mongo-keyfile`, `deploy/x509/prod`): without them the replica set can't authenticate its members and the server can't connect. **Auth breaks.** You cannot regenerate them to match existing data.
    - **`MONGO_ROOT_PASSWORD`:** without it you can't administer the database you just restored.
    - **`SEAWEEDFS_SSE_KEK`:** every object in the bundled SeaweedFS is encrypted under it. Without it the files on the data volume can't be read. Keep a copy apart from the server and from the data.

    A database backup without these secrets is only half a backup.

## What to back up

| What | Where it lives | How |
| --- | --- | --- |
| All application data | MongoDB replica set | `mongodump` (below) |
| Attachments & avatars | Bucket `HINATA_S3_BUCKET` (default `hinata`) in SeaweedFS or your S3 provider | `rclone sync` (below) |
| Secrets & config | `.env` | copy to a secret store |
| Cluster auth keyfile | `deploy/mongo-keyfile` | copy (mode `400`) |
| MongoDB TLS/X.509 PKI | `deploy/x509/prod/` | copy the whole directory |

## Backing up MongoDB

Production uses **TLS + X.509**, so `mongodump` must speak TLS and authenticate. The simplest way is to run it **inside** a Mongo container with the SCRAM root account, the same credentials the healthcheck and `init-prod-user.sh` use.

```bash
# Dump the 'hinata' database from the primary, over TLS, into ./backups on the host
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

This streams a single archive that compresses well to the host. Adjust the container name: `docker compose ps` shows it, and the compose project is named `hinata`.

!!! tip "Dumping against a live replica set is safe"
    `mongodump` reads a consistent snapshot while the server runs. You can schedule it against the primary without taking the stack offline.

## Backing up the bucket

Attachments and avatars live in the bucket. MongoDB only stores the object keys. The bundled SeaweedFS publishes no port, so a copy runs as a short-lived [rclone](https://rclone.org) container on the stack network (`hinata_hinata` with the default project name):

```bash
# From the server repo root, so the keys come from .env
set -a; . ./.env; set +a
docker run --rm --network hinata_hinata \
  -v "$PWD/backups/files:/files" \
  -e RCLONE_CONFIG_SRC_TYPE=s3 -e RCLONE_CONFIG_SRC_PROVIDER=SeaweedFS \
  -e RCLONE_CONFIG_SRC_ENDPOINT=http://seaweedfs:8333 \
  -e RCLONE_CONFIG_SRC_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
  -e RCLONE_CONFIG_SRC_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
  rclone/rclone:1.71 sync src:hinata /files --checksum --transfers 8
```

`sync` is incremental: only what changed moves. With an external provider, use its endpoint and keys instead, or the provider's own replication.

!!! warning "The copy is not encrypted"
    SeaweedFS decrypts the files when it hands them out, so the directory holds them in the clear. Encrypt it before it leaves the host, for example with restic as below, and keep it as private as the database dump.

!!! tip "A key that can only read"
    The SeaweedFS start script knows an optional third identity for backups. It may read and list the bucket and nothing else, so a backup job can never change what it copies. Set `SEAWEEDFS_BACKUP_ACCESS_KEY` and `SEAWEEDFS_BACKUP_SECRET_KEY` in `.env`. The stock `docker-compose.yml` does not pass them to the container, so add them in `docker-compose.override.yml` and recreate `seaweedfs`:

    ```yaml
    services:
      seaweedfs:
        environment:
          SEAWEEDFS_BACKUP_ACCESS_KEY: ${SEAWEEDFS_BACKUP_ACCESS_KEY}
          SEAWEEDFS_BACKUP_SECRET_KEY: ${SEAWEEDFS_BACKUP_SECRET_KEY}
    ```

    Then use these keys in the `rclone` call instead of the server's.

## Backing up secrets & PKI

These files are small and irreplaceable. Keep them somewhere safe, such as a secrets manager or an encrypted vault:

```bash
# From the server repo root
tar czf backups/hinata-secrets-$(date +%F).tar.gz \
  .env \
  deploy/mongo-keyfile \
  deploy/x509/prod
```

!!! warning "Store secrets separately from data dumps"
    Keep the secrets archive in a different, access-controlled place from your MongoDB dump and file copy. Anyone with `.env`, the PKI and a data dump has your whole platform. Encrypt it at rest and restrict who can read it.

## A recommended cron backup

One script for all three backups. It keeps 14 daily snapshots and prunes older ones:

```bash
#!/usr/bin/env bash
# /opt/hinata/backup.sh: run daily via cron
set -euo pipefail
cd /opt/hinata/hinata-server
DEST="/opt/hinata/backups/$(date +%F)"
mkdir -p "$DEST/files"

# 1) MongoDB (TLS + SCRAM root inside the container)
docker exec hinata-mongo1-1 sh -c '
  mongodump --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin --db hinata --archive' \
  > "$DEST/hinata.archive"

# 2) Attachments bucket (bundled SeaweedFS, over the stack network)
set -a; . ./.env; set +a
docker run --rm --network hinata_hinata -v "$DEST/files:/files" \
  -e RCLONE_CONFIG_SRC_TYPE=s3 -e RCLONE_CONFIG_SRC_PROVIDER=SeaweedFS \
  -e RCLONE_CONFIG_SRC_ENDPOINT=http://seaweedfs:8333 \
  -e RCLONE_CONFIG_SRC_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
  -e RCLONE_CONFIG_SRC_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
  rclone/rclone:1.71 sync src:hinata /files --checksum --quiet

# 3) Secrets & PKI
tar czf "$DEST/secrets.tar.gz" .env deploy/mongo-keyfile deploy/x509/prod

# Retain the last 14 days
find /opt/hinata/backups -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
```

```cron
# Daily at 03:30
30 3 * * * /opt/hinata/backup.sh >> /var/log/hinata-backup.log 2>&1
```

## Off-site with restic

A copy on the same host does not survive the loss of that host. The server repository ships a more complete example in `deploy/backup/`: `backup.sh` for the nightly run and `restore-test.sh` to prove the backup works. The approach, which you can adapt to your own setup:

- **The database** is dumped with `mongodump --archive --gzip` and streamed straight into [restic](https://restic.net), never written to disk. The dump runs over TLS as an X.509 user that may only read the database.
- **The files** are copied by rclone with the read-only SeaweedFS identity into a staging directory that only root can read. It stays between runs, so only changes move. restic then backs up that directory.
- **restic encrypts everything** before it leaves the host. The repository lives on another machine behind a REST server in append-only mode: this host can add snapshots but cannot change or delete one. Retention runs on the backup machine.
- **A run fails loudly.** A failing dump fails the whole run instead of leaving an empty snapshot behind, and every run writes its outcome to a log.

`restore-test.sh` checks the latest snapshots without touching the running stack. It restores the database into a throwaway MongoDB on a throwaway network and sets its collection and document counts beside the live ones. It restores the files into a throwaway directory and compares count and bytes with the staged copy. It prints counts only and removes everything temporary afterwards. Run it regularly, not only when you need the backup.

## Restoring

The order: **restore secrets → start Mongo and SeaweedFS → restore data → start the server and app**.

```bash
# 1) Restore secrets & PKI into the repo (so the cluster can authenticate)
tar xzf backups/hinata-secrets-YYYY-MM-DD.tar.gz

# 2) Bring up ONLY the data services, and let the setup job create the bucket
docker compose up -d mongo1 mongo2 mongo-arbiter seaweedfs
docker compose run --rm seaweedfs-setup

# 3) Restore MongoDB from the archive
docker exec -i hinata-mongo1-1 sh -c '
  mongorestore --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin \
    --drop --archive' < backups/hinata-YYYY-MM-DD.archive

# 4) Restore the attachments bucket (written encrypted again on the way in)
set -a; . ./.env; set +a
docker run --rm --network hinata_hinata -v "$PWD/backups/files:/files:ro" \
  -e RCLONE_CONFIG_DST_TYPE=s3 -e RCLONE_CONFIG_DST_PROVIDER=SeaweedFS \
  -e RCLONE_CONFIG_DST_ENDPOINT=http://seaweedfs:8333 \
  -e RCLONE_CONFIG_DST_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
  -e RCLONE_CONFIG_DST_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
  -e RCLONE_CONFIG_DST_SERVER_SIDE_ENCRYPTION=AES256 \
  rclone/rclone:1.71 copy /files dst:hinata --transfers 8

# 5) Start the application
docker compose up -d hinata-server hinata-app
```

!!! note "Restore onto matching PKI"
    The X.509 subject DN is registered as a Mongo user. Restore onto the **same** PKI you backed up, or re-register the DN with `./deploy/x509/init-prod-user.sh`. Otherwise the server can't authenticate.

## Upgrading

An upgrade is just an image tag bump. The server and app come from GHCR, and the data services (Mongo, SeaweedFS) stay as they are.

```bash
# 1) Pin the versions you want (in .env)
#    HINATA_SERVER_TAG={{version}}
#    HINATA_APP_TAG={{version}}

# 2) Pull the new images
docker compose pull hinata-server hinata-app

# 3) Recreate ONLY the app and server
docker compose up -d --no-deps hinata-server hinata-app
```

!!! danger "Never recreate or prune the data services on an upgrade"
    A production redeploy touches **only** `hinata-server` and `hinata-app`. The MongoDB replica set and SeaweedFS stay **online**.

    - Don't run a full `docker compose up` that recreates every service.
    - Never run a prune or down and up that could wipe the `mongo*-data` or `seaweedfs-data` volumes.
    - Use `--no-deps` so Compose doesn't restart Mongo and SeaweedFS as dependencies.

!!! tip "Take a backup right before upgrading"
    Run your backup script first. With a fresh MongoDB dump and the current `.env` you can roll back right away if a new tag misbehaves.

### Rolling back

The same steps with the previous tag:

```bash
# Set HINATA_SERVER_TAG / HINATA_APP_TAG back to the last known-good release, then:
docker compose pull hinata-server hinata-app
docker compose up -d --no-deps hinata-server hinata-app
```

With explicit tags instead of `latest`, a working version is always one edit away.

## Health checks

After every upgrade or restore, check that the server is up:

```bash
# Local (inside the host)
curl -s http://127.0.0.1:3356/actuator/health
# → {"status":"UP"}

# Through the proxy
curl -s https://api.track.example.com/actuator/health
```

`/actuator/health` needs no token and works well for orchestrator liveness and readiness probes. `DOWN` usually means MongoDB or the object store can't be reached. Check that the data services are running and that your PKI and credentials match.

## Next steps

- [Production deployment](/en/deployment.html): the full stack and deploy flow
- [Configuration reference](/en/configuration.html): every environment variable
- [MongoDB & X.509](/en/database.html): the replica set and PKI in depth
- [Object storage](/en/storage.html): SeaweedFS, other providers and moving from MinIO
