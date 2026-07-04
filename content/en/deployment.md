---
title: Production deployment
description: A complete, ordered walkthrough for deploying Hinata to production with Docker Compose, X.509 MongoDB, TLS, and a safe update flow.
---

# Production deployment

This is the full production walkthrough — every step, in order, from a clean host
to a running, health-checked instance behind your reverse proxy. It uses the
`prod` profile: a MongoDB replica set with TLS and X.509 client authentication.

If you have not yet, read the [self-hosting overview](/en/self-hosting.html) first
for the big picture. For the meaning of every setting mentioned here, keep the
[Configuration reference](/en/configuration.html) open alongside.

## Prerequisites

- A Linux host with **Docker Engine** and the **Docker Compose plugin**
  (`docker compose`, v2).
- `openssl`, `keytool` (from a JRE/JDK) and a POSIX shell to run the helper
  scripts in `deploy/`.
- Two DNS names you control — one for the API and one for the web app. Throughout
  this page we use `api.track.example.com` (API) and `track.example.com` (web).
- A reverse proxy terminating HTTPS (Nginx, Caddy, Traefik, a NAS reverse proxy,
  …). See [Reverse proxy & TLS](/en/reverse-proxy.html).
- An SMTP relay for outbound mail. See [E-mail & SMTP](/en/email.html).

## 1. Get the server repository

```bash
git clone https://github.com/hinata-platform/hinata-server.git
cd hinata-server
```

Updates later are `git pull` in this directory — the images themselves are pulled
from GHCR, so you never build on the host.

## 2. Create your .env

```bash
cp .env.example .env
```

`.env.example` is fully commented; every value can also be supplied as a plain
environment variable on the container. We fill it in over the next steps.

## 3. Generate secrets

```bash
./deploy/generate-secrets.sh
```

This script:

- creates `deploy/mongo-keyfile` (the replica set's internal-auth keyfile) if it
  does not already exist, and
- prints suggested random values for `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD`
  and `MINIO_ROOT_PASSWORD`.

Copy the printed values into your `.env`.

!!! warning "The JWT secret is required in production"
    `HINATA_JWT_SECRET` must be a random string of **at least 64 characters**
    (HS512). The server refuses to start in prod without it. If you did not use the
    generator, produce one with:

    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```

    Rotating this secret invalidates every issued token — all users must log in
    again.

## 4. Generate the MongoDB X.509 PKI

Production Mongo uses TLS plus X.509 client authentication — the gold-standard
setup — so there is no database password in the connection string. Generate the
certificate authority, server certificate and the application's client
certificate:

```bash
./deploy/x509/generate-certs.sh prod
```

This writes, under `deploy/x509/prod/`: the CA (`ca.crt`/`ca.key`), the mongod
server cert (`server.pem`), the app's JVM keystore (`hinata-app.p12`), the
truststore (`truststore.p12`), the replica-set `keyfile`, and
`app-subject-dn.txt` — the client certificate's subject DN, which becomes the
Mongo username.

The keystore and truststore passwords default to `changeit`. Change them, and set
the matching values in `.env`:

```properties
HINATA_MONGO_TLS_KEYSTORE_PASSWORD=change-me-keystore
HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD=change-me-truststore
```

!!! tip
    Run the certificate generator **before** the passwords are set if you want the
    default, or export `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` /
    `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` before running it so the PKCS#12 files
    are built with your chosen passwords from the start. Full detail on the
    [MongoDB & X.509](/en/database.html) page.

## 5. A realistic .env

Here is a representative production `.env`. Placeholders read `change-me…`;
secrets are shown as if produced by the generator (yours will differ). Adjust
hosts to your own.

```properties
# Profile
SPRING_PROFILES_ACTIVE=prod

# Public URLs
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com

# Image tags (pin a release instead of latest for reproducible deploys)
HINATA_SERVER_TAG=2.2.0
HINATA_APP_TAG=2.2.0

# JWT — from ./deploy/generate-secrets.sh
HINATA_JWT_SECRET=Kf3mS0pQ9xR2vN7wY1bZ8cH4dJ6gL5aT0eU3iO2rW9kP1sX4nC7mB6vD8fA2hQ0

# MongoDB SCRAM root (admin/internal only — the app uses X.509)
MONGO_ROOT_USERNAME=hinata
MONGO_ROOT_PASSWORD=9f1c7a4e2b6d8039a5c1e7f2b4d6a8c0
HINATA_MONGO_TLS_KEYSTORE_PASSWORD=change-me-keystore
HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD=change-me-truststore

# Reverse proxy — CIDR the proxy reaches the container from (see step 8)
HINATA_TRUSTED_PROXIES=172.16.0.0/12

# SMTP — a real relay so mail is delivered
HINATA_SMTP_HOST=smtp.example.com
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.com
HINATA_SMTP_PASSWORD=change-me-smtp
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=hinata@example.com

# Object storage (MinIO)
MINIO_ROOT_USER=hinata
MINIO_ROOT_PASSWORD=3b8e0d5f7a2c9146e0b3d7f1a5c8e2b4
HINATA_S3_BUCKET=hinata

# App integration
HINATA_PRIVACY_POLICY_URL=https://example.com/privacy
HINATA_APP_MIN_VERSION=2.2.0
HINATA_CORS_ALLOWED_ORIGINS=https://track.example.com
HINATA_DOCS_ENABLED=false

# Push + deep links — default gateway; override only to run your own
HINATA_GATEWAY_BASE_URL=https://connect.hinata.ahmadre.com

# First run (leave blank to use the in-app wizard)
HINATA_SETUP_AUTO_COMPLETE=false

# Demo seed — NEVER enable in production
HINATA_DEMO_SEED=false
HINATA_DEMO_RESET=false

# Rate limiting / brute force
HINATA_RATE_LIMIT_ENABLED=true
HINATA_RATE_LIMIT_API=300
HINATA_RATE_LIMIT_AUTH=10
HINATA_MAX_LOGIN_FAILURES=5
HINATA_LOGIN_BLOCK_MINUTES=15

# Published host ports (the reverse proxy forwards to these)
HINATA_PORT=3356
HINATA_APP_PORT=3456
```

!!! warning "Change every default"
    The stock `.env.example` ships development-grade defaults
    (`MONGO_ROOT_PASSWORD=hinata-dev-secret`, `changeit` keystore passwords, an
    empty JWT secret). Any of these left unchanged in production is a serious hole.
    Generate real secrets for all of them.

## 6. Bring up the stack

Start MongoDB first so the replica set can initiate and you can register the X.509
user, then start the rest.

```bash
# Start the database nodes
docker compose up -d mongo1 mongo2 mongo-arbiter

# Register the app's X.509 certificate as the $external Mongo user
./deploy/x509/init-prod-user.sh

# Start everything (server + MinIO)
docker compose up -d
```

To also serve the Flutter web app from this host, include the app overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

`init-prod-user.sh` reads the subject DN from `deploy/x509/prod/app-subject-dn.txt`
and creates a matching `$external` user with `readWrite` and `dbAdmin` on the
`hinata` database, using the SCRAM root account from `.env`. Run it once, after the
replica set is healthy.

## 7. Verify health

The server exposes a health endpoint that the container's own `HEALTHCHECK` also
polls:

```bash
curl -fsS https://api.track.example.com/actuator/health
# {"status":"UP"}
```

Locally, before the proxy is wired up, hit the published port directly:

```bash
curl -fsS http://localhost:3356/actuator/health
```

Watch the logs if it is not `UP`:

```bash
docker compose logs -f hinata-server
```

A common first-boot failure is Mongo auth — if you see X.509 authentication
errors, the `$external` user was not registered (re-run
`./deploy/x509/init-prod-user.sh`) or the keystore password in `.env` does not
match the one used to build `hinata-app.p12`.

## 8. DNS, reverse proxy and ports

The server publishes two host ports; your reverse proxy terminates TLS and
forwards to them:

| Public name | Purpose | Forwards to host port | Env var |
| --- | --- | --- | --- |
| `api.track.example.com` | REST API + SSE | `3356` | `HINATA_PORT` |
| `track.example.com` | Flutter web app | `3456` | `HINATA_APP_PORT` |

Point both DNS records at the proxy, issue certificates, and proxy each hostname
to its port. A minimal Nginx sketch (full config on
[Reverse proxy & TLS](/en/reverse-proxy.html)):

```nginx
location / {
    proxy_pass http://127.0.0.1:3356;   # api.track.example.com → server
    proxy_set_header Host              $host;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;                # keep SSE streaming
}
```

Two settings must agree with your proxy for the deployment to be correct and
secure:

- **CORS** — `HINATA_CORS_ALLOWED_ORIGINS` must list the web app's browser origin
  (`https://track.example.com`). The hosted web client calls the API cross-origin,
  so a missing origin here shows up as blocked requests in the browser.
- **Trusted proxies** — `HINATA_TRUSTED_PROXIES` is the CIDR the proxy reaches the
  container from. Only from those addresses does the server trust
  `X-Forwarded-For`, so rate limiting and logging see the real client IP. Empty
  means trust nobody; setting it too wide lets clients spoof their IP.

!!! tip "Keep SSE alive through the proxy"
    Live updates use Server-Sent Events. Disable response buffering on the API
    location (`proxy_buffering off;` in Nginx) or clients will not receive updates
    promptly.

## 9. First run

With the stack healthy, open `https://track.example.com` (or point a native app at
`https://api.track.example.com`) and complete the setup wizard to create the
organization and the first admin. To automate this instead — handy for
infrastructure-as-code — set the `HINATA_SETUP_*` variables; see
[Setup & first run](/en/setup-wizard.html).

## Updating and redeploying

Updates are just a new image tag. Set the tag, pull, and recreate only the app and
server — never the data services.

```bash
# Pin the new release in .env
HINATA_SERVER_TAG=2.3.0
HINATA_APP_TAG=2.3.0

# Pull the new images and recreate only server + app
docker compose pull hinata-server
docker compose up -d hinata-server
# if you serve the web app too:
docker compose -f docker-compose.yml -f docker-compose.app.yml pull hinata-app
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d hinata-app
```

!!! danger "A redeploy must update only app + server — never recreate Mongo or MinIO"
    Your issues, attachments and users live in the `mongo1-data`, `mongo2-data`
    and `minio-data` Docker volumes. Recreating or removing the database or storage
    services (for example a full `down -v`, or a stack redeploy that prunes volumes)
    **destroys that data**. When updating, target the `hinata-server` and
    `hinata-app` services explicitly, as above. Take a backup before any change
    that touches the data services — see [Backups & upgrades](/en/backups.html).

!!! tip "Pin tags for reproducible deploys"
    `latest` is convenient but moves under you. Pin `HINATA_SERVER_TAG` and
    `HINATA_APP_TAG` to a specific version (e.g. `2.2.0`) so every host runs the
    same, known build and rollbacks are a one-line tag change.

## Where to go next

- [Configuration reference](/en/configuration.html) — every setting explained.
- [MongoDB & X.509](/en/database.html) — the PKI in depth, plus operations.
- [Reverse proxy & TLS](/en/reverse-proxy.html) — full proxy configs.
- [Backups & upgrades](/en/backups.html) — protecting data across updates.
