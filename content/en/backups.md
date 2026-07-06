---
title: Backups & upgrades
description: Operate a Hinata stack over time — back up MongoDB, MinIO and your secrets, restore safely, and upgrade or roll back the server and app without touching the data services.
---

# Backups & upgrades

Standing a Hinata stack up is a one-time job; keeping it healthy is the ongoing
one. Three things carry all your state — **MongoDB** (all data), **MinIO/S3**
(attachments and avatars) and your **secrets** (`.env`, the Mongo keyfile and the
X.509 PKI). Back up all three, and know how to bump image tags without recreating
the data services. This page covers exactly that.

!!! danger "The three things that will ruin your day if lost"
    - **`HINATA_JWT_SECRET`** — lose it and every issued token becomes invalid;
      **all users are logged out** and must sign in again.
    - **The Mongo keyfile + X.509 PKI** (`deploy/mongo-keyfile`, `deploy/x509/prod`)
      — lose them and the replica set can't authenticate members and the server
      can't connect. **Auth breaks.** These are not regenerable to match existing
      data.
    - **`MONGO_ROOT_PASSWORD` / `MINIO_ROOT_PASSWORD`** — lose them and you can't
      administer the databases you just restored.

    A database backup without these secrets is only half a backup.

## What to back up

| What | Where it lives | How |
| --- | --- | --- |
| All application data | MongoDB replica set | `mongodump` (below) |
| Attachments & avatars | MinIO/S3 bucket (`HINATA_S3_BUCKET`, default `hinata`) | `mc mirror` / bucket sync |
| Secrets & config | `.env` | copy to a secret store |
| Cluster auth keyfile | `deploy/mongo-keyfile` | copy (mode `400`) |
| MongoDB TLS/X.509 PKI | `deploy/x509/prod/` | copy the whole directory |

## Backing up MongoDB

Production runs a replica set with **TLS + X.509**, so `mongodump` must speak TLS
and authenticate. The simplest reliable approach is to run it **inside** a Mongo
container with the SCRAM root account (the same credentials the healthcheck and
`init-prod-user.sh` use), dumping to a mounted path.

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

This streams a single compressed-friendly archive to the host. Adjust the
container name to match your project (`docker compose ps` shows it — the compose
project is named `hinata`).

!!! tip "Dumping against a live replica set is safe"
    `mongodump` reads a consistent snapshot without stopping the server, so you
    can run it on a schedule against the running primary. There's no need to take
    the stack offline for a backup.

## Backing up MinIO / S3

Attachments and avatars live in the S3 bucket, not in MongoDB — Mongo only stores
the object keys. Back up the bucket separately with the MinIO client `mc`:

```bash
# Configure an alias for your MinIO once (use your MINIO_ROOT_USER / _PASSWORD)
mc alias set hinata http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# Mirror the bucket to a local backup directory (incremental)
mc mirror --overwrite --remove hinata/hinata ./backups/minio/hinata
```

For off-site durability, mirror to another S3 target (e.g. a second MinIO or a
cloud bucket) instead of a local path. See [Object storage (S3/MinIO)](/en/storage.html).

## Backing up secrets & PKI

These are small, static and irreplaceable — copy them somewhere safe (a secrets
manager, an encrypted vault):

```bash
# From the server repo root
tar czf backups/hinata-secrets-$(date +%F).tar.gz \
  .env \
  deploy/mongo-keyfile \
  deploy/x509/prod
```

!!! warning "Store secrets separately from data dumps"
    Keep the secrets archive in a different, access-controlled location from your
    MongoDB/MinIO dumps. Anyone with `.env` + the PKI + a data dump has your whole
    platform. Encrypt at rest and restrict who can read it.

## A recommended cron backup

Put the three backups behind one script and schedule it. This keeps 14 daily
snapshots and prunes older ones:

```bash
#!/usr/bin/env bash
# /opt/hinata/backup.sh — run daily via cron
set -euo pipefail
cd /opt/hinata/hinata-server
DEST="/opt/hinata/backups/$(date +%F)"
mkdir -p "$DEST/minio"

# 1) MongoDB (TLS + SCRAM root inside the container)
docker exec hinata-mongo1-1 sh -c '
  mongodump --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin --db hinata --archive' \
  > "$DEST/hinata.archive"

# 2) Attachments bucket
mc mirror --overwrite --remove hinata/hinata "$DEST/minio/hinata"

# 3) Secrets & PKI
tar czf "$DEST/secrets.tar.gz" .env deploy/mongo-keyfile deploy/x509/prod

# Retain the last 14 days
find /opt/hinata/backups -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
```

```cron
# Daily at 03:30
30 3 * * * /opt/hinata/backup.sh >> /var/log/hinata-backup.log 2>&1
```

## Restoring

The high-level order is: **restore secrets → bring up Mongo + MinIO → restore
data → start the server + app**.

```bash
# 1) Restore secrets & PKI into the repo (so the cluster can authenticate)
tar xzf backups/hinata-secrets-YYYY-MM-DD.tar.gz

# 2) Bring up ONLY the data services
docker compose up -d mongo1 mongo2 mongo-arbiter minio

# 3) Restore MongoDB from the archive
docker exec -i hinata-mongo1-1 sh -c '
  mongorestore --host mongo1 \
    --tls --tlsCAFile /etc/mongo/certs/ca.crt \
    --tlsCertificateKeyFile /etc/mongo/certs/server.pem \
    -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
    --authenticationDatabase admin \
    --drop --archive' < backups/hinata-YYYY-MM-DD.archive

# 4) Restore the attachments bucket
mc mirror --overwrite ./backups/minio/hinata hinata/hinata

# 5) Start the application
docker compose up -d hinata-server hinata-app
```

!!! note "Restore onto matching PKI"
    Because the X.509 subject DN is registered as a Mongo user, restore your data
    onto the **same** PKI you backed up (or re-register the DN with
    `./deploy/x509/init-prod-user.sh`). Restoring data with a mismatched
    certificate leaves the server unable to authenticate.

## Upgrading

Upgrades are just an image-tag bump. The server and app are pulled from GHCR; the
data services (Mongo, MinIO) stay exactly as they are.

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
    A production redeploy touches **only** `hinata-server` and `hinata-app`. Keep
    the MongoDB replica set and MinIO **online** — do not run a full
    `docker compose up` that recreates every service, and never pass a
    prune/down-and-up that could wipe the `mongo*-data` or `minio-data` volumes.
    Use `--no-deps` so Compose doesn't restart Mongo/MinIO as dependencies.

!!! tip "Take a backup right before upgrading"
    Run your backup script first. A fresh MongoDB dump plus the current `.env`
    lets you roll back instantly if a new tag misbehaves.

### Rolling back

Rollback is the same operation with the previous tag:

```bash
# Set HINATA_SERVER_TAG / HINATA_APP_TAG back to the last known-good release, then:
docker compose pull hinata-server hinata-app
docker compose up -d --no-deps hinata-server hinata-app
```

Because you pin explicit tags rather than relying on `latest`, a known-good
version is always one edit away.

## Health checks

After any upgrade or restore, confirm the server is up before declaring victory:

```bash
# Local (inside the host)
curl -s http://127.0.0.1:3356/actuator/health
# → {"status":"UP"}

# Through the proxy
curl -s https://api.track.example.com/actuator/health
```

`/actuator/health` is a public endpoint (no token) and is ideal for orchestrator
liveness/readiness probes. A `DOWN` status usually points at MongoDB or MinIO
connectivity — check that the data services are running and that your PKI and
credentials match.

## Next steps

- [Production deployment](/en/deployment.html) — the full stack and deploy flow
- [Configuration reference](/en/configuration.html) — every environment variable
- [MongoDB & X.509](/en/database.html) — the replica set and PKI in depth
- [Object storage (S3/MinIO)](/en/storage.html) — buckets, keys and presigned downloads
