---
title: Overview
description: What you run to self-host Hinata, the Compose files, profiles, and a checklist of every setting.
---

# Self-hosting Hinata

You run Hinata on your own infrastructure, with no seat, board or user limits.
This page shows what Hinata is made of and what to configure before going live.
Each item links to a page with the concrete steps.

Just want a running instance fast? Use the [Quick start](/en/quick-start.html).

## What you run

Hinata runs as a small set of containers with Docker Compose. Two images are
published to the GitHub Container Registry under `ghcr.io/hinata-platform`. The
rest are stock upstream images.

| Component | Image | Role |
| --- | --- | --- |
| **Server (API)** | `ghcr.io/hinata-platform/hinata-server` | Spring Boot 4 / Java 21 REST API under `/api/v1`, SSE live updates, JWT auth |
| **Web app** | `ghcr.io/hinata-platform/hinata-app` | The compiled Flutter web client, served as static files |
| **MongoDB** | `mongo:8.0` | Primary data store. A **replica set** (2 data nodes + 1 arbiter) in production |
| **Object storage** | `minio/minio` | S3-compatible store for attachments and avatars (presigned downloads) |
| **Mail** | your SMTP relay (`axllent/mailpit` in dev) | Outbound e-mail: verification, password reset, notifications |

- The server is stateless. All data lives in MongoDB and MinIO, so you can scale
  or redeploy it freely.
- Live updates reach clients over **Server-Sent Events (SSE)**. No message broker
  needed.

!!! info "You do not need Firebase"
    Push and universal links go through the hosted
    [Hinata Connect gateway](/en/connect-gateway.html). The app's push
    credentials live there, not in your deployment. You run and configure
    nothing for push.

## The two Compose files

The server repository ships two stack files. The API stack is the base. The app
is an optional overlay on top.

| File | What it brings up |
| --- | --- |
| `docker-compose.yml` | **The full backend stack**: server, MongoDB replica set (`mongo1`, `mongo2`, `mongo-arbiter`) and MinIO. This is the base. |
| `docker-compose.app.yml` | **An overlay with the Flutter web app** (`hinata-app`) on `HINATA_APP_PORT`. Use it to serve the web client from the same host. |

Bring up the API stack alone:

```bash
docker compose up -d
```

Bring up the API stack **and** the web app together:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

!!! tip "You may not need to self-host the web app"
    The native apps can save several servers, and the web build points at the
    configured API. So some operators run only the API stack and users connect
    from the published apps. Host the web app yourself if you want a branded
    `https://track.example.com` in the browser.

For local development there's also `docker-compose.dev.yml`. It starts only
Mongo, MinIO and Mailpit, and you run the server from your IDE. See
[Development](/en/development.html).

## Profiles: dev vs prod

The Spring profile in `SPRING_PROFILES_ACTIVE` sets the behavior:

- **`prod`:** MongoDB is a TLS replica set with **X.509 client authentication**
  (no password in the connection string). This is what `docker-compose.yml` uses
  and what you deploy. The demo seeder is compiled out (`@Profile("!prod")`).
- **`dev`:** MongoDB runs standalone (still TLS + X.509) for a single developer
  on `localhost`. Used with `docker-compose.dev.yml` when running the server from
  source.

!!! warning "Never run the demo seeder in production"
    `HINATA_DEMO_SEED=true` creates an English demo workspace (login `rebar` /
    `hinata-demo-2026`) for screenshots and click-throughs.

    Under the prod profile, `@Profile("!prod")` makes the seeder **always skip,
    regardless of the flag**. Don't rely on that alone. Set
    `HINATA_DEMO_SEED=false` in every production `.env`. Otherwise an admin with a
    known password and throwaway data end up in your real database.

## Configuration checklist

Work through these before you expose the instance:

| Area | What to set | Page |
| --- | --- | --- |
| **Domain & TLS** | Public hostnames and a reverse proxy terminating HTTPS, forwarding to `HINATA_PORT` (API) and `HINATA_APP_PORT` (web) | [Reverse proxy & TLS](/en/reverse-proxy.html) |
| **JWT secret** | `HINATA_JWT_SECRET`: a random HS512 secret of ≥ 64 chars (required in prod) | [Production deployment](/en/deployment.html) |
| **MongoDB X.509** | Generate the PKI, register the client cert as the `$external` user | [MongoDB & X.509](/en/database.html) |
| **Object storage** | MinIO credentials and bucket, or an external S3 | [Object storage](/en/storage.html) |
| **SMTP** | A real mail relay so verification, reset and notification mail gets delivered | [E-mail & SMTP](/en/email.html) |
| **CORS** | `HINATA_CORS_ALLOWED_ORIGINS`: browser origins allowed to call the API | [Configuration reference](/en/configuration.html) |
| **Trusted proxies** | `HINATA_TRUSTED_PROXIES`: CIDRs of proxies allowed to set `X-Forwarded-For` | [Reverse proxy & TLS](/en/reverse-proxy.html) |
| **Gateway** | Usually the default. Override `HINATA_GATEWAY_BASE_URL` only to run your own | [Hinata Connect gateway](/en/connect-gateway.html) |
| **First run** | Complete the in-app setup wizard, or automate it with `HINATA_SETUP_*` | [Setup & first run](/en/setup-wizard.html) |

Every environment variable, grouped with defaults and whether it's required, is
in the [Configuration reference](/en/configuration.html).

## Where to go next

- [Production deployment](/en/deployment.html): every step in order, from
  secrets, PKI and image tags through `up -d`, health checks and DNS to updates.
- [Configuration reference](/en/configuration.html): every setting, and the
  difference between env vars and runtime (database) settings.
- [MongoDB & X.509](/en/database.html), [Object storage](/en/storage.html),
  [E-mail & SMTP](/en/email.html), [Reverse proxy & TLS](/en/reverse-proxy.html):
  the detailed pages per subsystem.
- [Backups & upgrades](/en/backups.html): keeping data safe across redeploys.
