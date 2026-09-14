---
title: MongoDB & X.509
description: How Hinata runs MongoDB in production, as a replica set with TLS and X.509, plus the scripts that generate every certificate.
---

# MongoDB & X.509

Hinata stores everything in **MongoDB**: projects, issues, comments, knowledge base articles and runtime settings. In production it runs as a **replica set** with **TLS encryption** and **X.509 client authentication**.

!!! info
    All commands live in the server repo under `deploy/`. They are plain `openssl` and `mongosh` scripts you can read before running them.

## Why a replica set

- **Multi-document transactions.** Some operations must be all or nothing, for example completing a sprint and moving its issues. MongoDB only offers transactions on a replica set, never on a standalone node.
- **High availability.** Two data nodes and an arbiter survive losing one data node. The other one is elected primary, and the server keeps serving.

!!! note "SSE is handled in the app, not by Mongo"
    Live attachment updates use in-process Server-Sent Events, not Mongo change streams. SSE does not need the replica set.

## Production topology

The production `docker-compose.yml` starts three MongoDB containers on a private Docker network:

| Container | Role | Data | Votes |
| --- | --- | --- | --- |
| `mongo1` | Data node (priority 2, preferred primary) | yes (`mongo1-data` volume) | yes |
| `mongo2` | Data node (priority 1) | yes (`mongo2-data` volume) | yes |
| `mongo-arbiter` | Arbiter, election tie-breaker only | **none** | yes |

The arbiter holds no data. It only gives elections an odd number of voters without a third full copy. Every node runs the same command:

```yaml
command: >-
  mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongo/keyfile
  --tlsMode requireTLS
  --tlsCertificateKeyFile /etc/mongo/certs/server.pem
  --tlsCAFile /etc/mongo/certs/ca.crt
```

Two independent authentication layers:

- **`--keyFile`:** a shared secret the members use to authenticate *to each other* (internal cluster auth, SCRAM).
- **`--tlsMode requireTLS` + `--tlsCAFile`:** every *client* connection needs TLS **and** a certificate signed by the cluster's CA. This enables X.509 client authentication.

The first time `mongo1` becomes healthy, its healthcheck runs `rs.initiate(...)` with the three members if the set is not configured yet. You never run it by hand.

## Two ways the app authenticates: SCRAM root vs. app X.509

- **`MONGO_ROOT_USERNAME` / `MONGO_ROOT_PASSWORD`:** a classic SCRAM root account created by the Mongo image (`MONGO_INITDB_ROOT_*`). It is *administrative only*: it initiates the replica set and registers the X.509 user. The Hinata server never uses it.
- **The application X.509 user:** the server authenticates with a **client certificate**, no password. Its username *is* the certificate's subject DN, and it lives in the special `$external` authentication database.

That is why the connection string has no password:

```text
mongodb://mongo1:27017,mongo2:27017/hinata?replicaSet=rs0&tls=true&authMechanism=MONGODB-X509&authSource=$external
```

`docker-compose.yml` sets it as `HINATA_MONGODB_URI` on the server container. The server's certificate comes from the JVM keystore in `HINATA_MONGO_TLS_KEYSTORE`. It validates the cluster with the truststore in `HINATA_MONGO_TLS_TRUSTSTORE`.

## Generating the keyfile and PKI

Run the three scripts in this order on a fresh production host.

### 1. Replica-set keyfile and suggested secrets

```bash
cp .env.example .env
./deploy/generate-secrets.sh
```

`generate-secrets.sh` creates `deploy/mongo-keyfile` (`openssl rand -base64 756`, mode `400`) if it is missing. It never overwrites an existing one. It also prints values for `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD` and `MINIO_ROOT_PASSWORD` to copy into your `.env`.

### 2. The X.509 certificate authority and certificates

```bash
./deploy/x509/generate-certs.sh prod
```

This builds a self-contained PKI under `deploy/x509/prod/`:

| File | What it is |
| --- | --- |
| `ca.crt` / `ca.key` | The private certificate authority (4096-bit RSA, valid 10 years) |
| `server.pem` | The `mongod` TLS cert + key. Its SAN covers `mongo1`, `mongo2`, `mongo-arbiter` |
| `hinata-app.p12` | JVM **keystore**: the app's client certificate + key |
| `truststore.p12` | JVM **truststore**: just the CA |
| `app-subject-dn.txt` | The client cert's subject DN, which is the Mongo `$external` username |
| `keyfile` | A replica set internal auth keyfile (prod only) |

The app certificate deliberately uses a different Organizational Unit (`OU=Hinata Application`) than the server and member certificate. That way `mongod` treats it as a normal X.509 **user**, not a cluster member.

!!! warning "Do not regenerate the CA on a live cluster"
    `generate-certs.sh` only overwrites an existing CA with `--force`. A new CA instantly invalidates every certificate the running cluster trusts. Only use `--force` on a fresh setup.

### 3. Register the X.509 user

Bring up the data nodes, then create the `$external` user that matches the app certificate's DN:

```bash
docker compose up -d mongo1 mongo2 mongo-arbiter
./deploy/x509/init-prod-user.sh
docker compose up -d hinata-server
```

`init-prod-user.sh` connects over TLS as the SCRAM root account from your `.env`. It runs `createUser` in `$external` with the DN from `app-subject-dn.txt` and grants `readWrite` and `dbAdmin` on the `hinata` database. It is idempotent: if the user already exists, it says so and moves on.

## The dev database (standalone, still TLS + X.509)

Locally, `docker-compose.dev.yml` starts a single `mongod`, **not** a replica set. Security stays the same: `requireTLS`, `--auth` and X.509-only client access. One command sets it up:

```bash
./deploy/x509/setup-dev.sh
SPRING_PROFILES_ACTIVE=dev ./gradlew bootRun
```

`setup-dev.sh` generates the dev PKI (`deploy/x509/dev/`), starts the dev Mongo, creates the `$external` X.509 user via the localhost exception and checks that X.509 login works. `application-dev.yml` already uses this connection, so you don't set `HINATA_MONGODB_URI` yourself.

!!! note "Dev binds to loopback only"
    The dev Mongo publishes `127.0.0.1:27017`, never `0.0.0.0`. It is not reachable from the network.

## Keystore and truststore passwords

The JVM keystore and truststore are PKCS#12 files protected by passwords you choose:

| Variable | Protects | Default |
| --- | --- | --- |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | `hinata-app.p12` (client cert + key) | `changeit` |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | `truststore.p12` (the CA) | `changeit` |

`generate-certs.sh` reads both variables when it builds the `.p12` files. Export your own passwords **before** generating the certificates:

```bash
export HINATA_MONGO_TLS_KEYSTORE_PASSWORD='a-long-random-value'
export HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD='another-long-random-value'
./deploy/x509/generate-certs.sh prod
```

Then set the same values in `.env` so the server can open the stores at runtime.

!!! danger "Change every default before you go live"
    `changeit`, `hinata-dev-secret` and the sample `MONGO_ROOT_PASSWORD` in `.env.example` are for development only. For any internet-facing deployment, generate fresh secrets with `./deploy/generate-secrets.sh` and set real keystore passwords.

## Data persistence and operational safety

- **Named volumes.** The data nodes write to `mongo1-data` and `mongo2-data`. Your data survives container restarts, image upgrades and `docker compose up` re-creations. `docker compose down -v` removes those volumes and destroys the database. Don't.
- **Never expose Mongo publicly.** The ports stay on the internal `hinata` Docker network, and the default compose does not publish `27017` to the host in production. Only the server (behind your reverse proxy) should reach the database.
- **The arbiter is not a backup.** It stores no data. Backups come from `mongodump` or volume snapshots, see [Backups & upgrades](/en/backups.html).

Next: [Object storage (S3/MinIO)](/en/storage.html), [E-mail & SMTP](/en/email.html) and [Reverse proxy & TLS](/en/reverse-proxy.html). Every environment variable is listed in the [Configuration reference](/en/configuration.html).
