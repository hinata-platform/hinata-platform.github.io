---
title: MongoDB & X.509
description: How Hinata runs MongoDB — a production replica set with TLS and X.509 client authentication, plus the PKI scripts that generate every certificate.
---

# MongoDB & X.509

Hinata stores everything — projects, issues, comments, knowledge-base articles,
runtime settings — in **MongoDB**. In production it runs as a **replica set** with
**TLS encryption** and **X.509 client authentication**, the MongoDB "gold standard"
for a self-hosted cluster. This page explains why, how the topology is laid out,
and exactly what the deploy scripts in the server repo do so you can reproduce and
trust the setup.

!!! info
    All of the commands below live in the server repo under `deploy/`. They are
    plain `openssl`/`mongosh` scripts — nothing magic — so you can read them before
    you run them.

## Why a replica set

A single `mongod` is enough to *store* data, but Hinata deliberately targets a
replica set in production for two reasons:

- **Multi-document transactions.** Operations that must be all-or-nothing — for
  example completing a sprint and moving its issues — use MongoDB transactions.
  MongoDB only offers transactions on a replica set, never on a standalone node.
- **High availability.** With two data-bearing nodes and an arbiter, the cluster
  survives losing one data node: the surviving node is elected primary and the
  server keeps serving.

!!! note "SSE is handled in the app, not by Mongo"
    Hinata's live attachment updates use in-process Server-Sent Events, not Mongo
    change streams, so the SSE feature itself does not depend on the replica set.
    The replica set is about transactions and availability.

## Production topology

The production `docker-compose.yml` brings up three MongoDB containers on a private
Docker network:

| Container | Role | Data | Votes |
| --- | --- | --- | --- |
| `mongo1` | Data node (priority 2 — preferred primary) | yes (`mongo1-data` volume) | yes |
| `mongo2` | Data node (priority 1) | yes (`mongo2-data` volume) | yes |
| `mongo-arbiter` | Arbiter — election tie-breaker only | **none** | yes |

The arbiter holds no data; it exists purely so elections have an odd number of
voters without paying for a third full copy. Every node runs with the same command:

```yaml
command: >-
  mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongo/keyfile
  --tlsMode requireTLS
  --tlsCertificateKeyFile /etc/mongo/certs/server.pem
  --tlsCAFile /etc/mongo/certs/ca.crt
```

Two independent authentication layers are in play here:

- **`--keyFile`** — a shared secret that the replica-set members use to authenticate
  *to each other* (internal cluster auth, SCRAM).
- **`--tlsMode requireTLS` + `--tlsCAFile`** — every *client* connection must use TLS
  **and** present a certificate signed by the cluster's CA. That is what enables
  X.509 client authentication.

The replica set is initiated automatically the first time `mongo1` becomes healthy —
its Docker healthcheck runs `rs.initiate(...)` with the three members if the set is
not already configured, so you never have to run it by hand.

## Two ways the app authenticates: SCRAM root vs. app X.509

There are two distinct MongoDB identities, and it is important not to confuse them:

- **`MONGO_ROOT_USERNAME` / `MONGO_ROOT_PASSWORD`** — a classic SCRAM root account
  created by the Mongo image (`MONGO_INITDB_ROOT_*`). It is *administrative only*:
  it initiates the replica set and registers the X.509 user. The Hinata server never
  uses it.
- **The application X.509 user** — the server authenticates with a **client
  certificate**, not a password. Its username *is* the certificate's subject DN, and
  it lives in the special `$external` authentication database.

That is why the production connection string carries no password at all:

```text
mongodb://mongo1:27017,mongo2:27017/hinata?replicaSet=rs0&tls=true&authMechanism=MONGODB-X509&authSource=$external
```

This URI is set for you in `docker-compose.yml` (as `HINATA_MONGODB_URI` on the
server container). The certificate the server presents comes from the JVM keystore
configured with `HINATA_MONGO_TLS_KEYSTORE`, and it validates the cluster with the
truststore in `HINATA_MONGO_TLS_TRUSTSTORE`.

## Generating the keyfile and PKI

Three scripts produce everything. Run them in this order for a fresh production host.

### 1. Replica-set keyfile and suggested secrets

```bash
cp .env.example .env
./deploy/generate-secrets.sh
```

`generate-secrets.sh` creates `deploy/mongo-keyfile` (`openssl rand -base64 756`,
mode `400`) if it does not already exist — it refuses to overwrite an existing one —
and prints ready-to-paste values for `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD` and
`MINIO_ROOT_PASSWORD`. Copy those into your `.env`.

### 2. The X.509 certificate authority and certificates

```bash
./deploy/x509/generate-certs.sh prod
```

This builds a self-contained PKI under `deploy/x509/prod/`:

| File | What it is |
| --- | --- |
| `ca.crt` / `ca.key` | The private certificate authority (4096-bit RSA, valid 10 years) |
| `server.pem` | The `mongod` TLS cert + key; its SAN covers `mongo1`, `mongo2`, `mongo-arbiter` |
| `hinata-app.p12` | JVM **keystore** — the app's client certificate + key |
| `truststore.p12` | JVM **truststore** — just the CA |
| `app-subject-dn.txt` | The client cert's subject DN = the Mongo `$external` username |
| `keyfile` | A replica-set internal-auth keyfile (prod only) |

The application certificate is deliberately issued with a different
Organizational Unit (`OU=Hinata Application`) than the server/member certificate, so
`mongod` treats it as a normal X.509 **user** rather than a cluster member.

!!! warning "Do not regenerate the CA on a live cluster"
    `generate-certs.sh` refuses to overwrite an existing CA unless you pass
    `--force`, because replacing the CA would instantly invalidate every certificate
    the running cluster already trusts. Only use `--force` on a fresh setup.

### 3. Register the X.509 user

Bring the data nodes up, then create the `$external` user that maps to the app
certificate's DN:

```bash
docker compose up -d mongo1 mongo2 mongo-arbiter
./deploy/x509/init-prod-user.sh
docker compose up -d hinata-server
```

`init-prod-user.sh` connects as the SCRAM root account (from your `.env`) over TLS
and runs `createUser` in `$external` with the DN from `app-subject-dn.txt`, granting
`readWrite` and `dbAdmin` on the `hinata` database. It is idempotent — if the user
already exists it says so and moves on.

## The dev database (standalone, still TLS + X.509)

Local development does **not** run a replica set. `docker-compose.dev.yml` starts a
single standalone `mongod` — but it keeps the same security posture: `requireTLS`,
`--auth`, and X.509-only client access. One command sets it all up:

```bash
./deploy/x509/setup-dev.sh
SPRING_PROFILES_ACTIVE=dev ./gradlew bootRun
```

`setup-dev.sh` generates the dev PKI (`deploy/x509/dev/`), starts the dev Mongo,
creates the `$external` X.509 user via the localhost exception, and verifies that
X.509 login works. `application-dev.yml` already points at the TLS/X.509 connection,
so you don't set `HINATA_MONGODB_URI` yourself.

!!! note "Dev binds to loopback only"
    The dev Mongo publishes `127.0.0.1:27017` — never `0.0.0.0` — so a development
    database is never reachable from the network.

## Keystore and truststore passwords

The JVM keystore and truststore are PKCS#12 files protected by passwords you control:

| Variable | Protects | Default |
| --- | --- | --- |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | `hinata-app.p12` (client cert + key) | `changeit` |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | `truststore.p12` (the CA) | `changeit` |

`generate-certs.sh` reads these two variables when it builds the `.p12` files, so if
you want non-default passwords, export them **before** generating the certificates:

```bash
export HINATA_MONGO_TLS_KEYSTORE_PASSWORD='a-long-random-value'
export HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD='another-long-random-value'
./deploy/x509/generate-certs.sh prod
```

Then set the same values in `.env` so the server can open the stores at runtime.

!!! danger "Change every default before you go live"
    `changeit`, `hinata-dev-secret`, and the sample `MONGO_ROOT_PASSWORD` in
    `.env.example` are development conveniences. Generate fresh secrets with
    `./deploy/generate-secrets.sh` and set real keystore passwords for any
    internet-facing deployment.

## Data persistence and operational safety

- **Named volumes.** Each data node writes to a named Docker volume
  (`mongo1-data`, `mongo2-data`), so your data survives container restarts,
  image upgrades and `docker compose up` re-creations. Removing those volumes
  (`docker compose down -v`) destroys the database — don't.
- **Never expose Mongo publicly.** The replica-set ports stay on the internal
  `hinata` Docker network. Nothing in the default compose publishes `27017` to the
  host in production. Only the server (behind your reverse proxy) should reach the
  database.
- **The arbiter is not a backup.** It stores no data. Real backups come from
  `mongodump`/volume snapshots — see [Backups & upgrades](/en/backups.html).

For the surrounding stack — object storage, mail, and the reverse proxy — see
[Object storage (S3/MinIO)](/en/storage.html),
[E-mail & SMTP](/en/email.html), and
[Reverse proxy & TLS](/en/reverse-proxy.html). Every environment variable is
catalogued in the [Configuration reference](/en/configuration.html).
