---
title: Overview
description: The map of self-hosting Hinata — what you run, the Compose files, profiles, and a checklist of everything to configure.
---

# Self-hosting Hinata

Hinata is designed to be run by you, on your own infrastructure, with no seats,
board or user limits. This page is the map: what pieces make up a running
Hinata, how they fit together, and a checklist of everything you configure before
going live. Each item links to a focused page with the concrete steps.

If you just want the fastest path to a running instance, start with the
[Quick start](/en/quick-start.html). This page is the bigger picture that
production operators should read first.

## What you run

A production Hinata deployment is a small set of containers orchestrated by
Docker Compose. Two images are published to the GitHub Container Registry under
`ghcr.io/hinata-platform`; the rest are stock upstream images.

| Component | Image | Role |
| --- | --- | --- |
| **Server (API)** | `ghcr.io/hinata-platform/hinata-server` | Spring Boot 4 / Java 21 REST API under `/api/v1`, SSE live updates, JWT auth |
| **Web app** | `ghcr.io/hinata-platform/hinata-app` | The compiled Flutter web client, served as static files |
| **MongoDB** | `mongo:8.0` | Primary data store — a **replica set** (2 data nodes + 1 arbiter) in production |
| **Object storage** | `minio/minio` | S3-compatible store for attachments and avatars (presigned downloads) |
| **Mail** | your SMTP relay (`axllent/mailpit` in dev) | Outbound e-mail: verification, password reset, notifications |

The server is stateless — all state lives in MongoDB and MinIO — so you scale or
redeploy it freely. Live updates reach clients over **Server-Sent Events (SSE)**,
so no extra message broker is required.

!!! info "You do not need Firebase"
    Mobile push and universal (deep) links are relayed through the central
    [Hinata Connect gateway](/en/connect-gateway.html), a hosted service. The
    published app's push credentials live in the gateway, not in your deployment,
    so self-hosters run no push infrastructure and configure nothing for push.

## The two Compose files

The server repository ships two composable stack files. Think of the API stack as
the base, and the app as an overlay you layer on top.

| File | What it brings up |
| --- | --- |
| `docker-compose.yml` | **The full backend stack**: the server, the MongoDB replica set (`mongo1`, `mongo2`, `mongo-arbiter`) and MinIO. This is the base. |
| `docker-compose.app.yml` | **An overlay that adds the Flutter web app** (`hinata-app`), served on `HINATA_APP_PORT`. Layer it on top of the base to serve the web client from the same host. |

Bring up the API stack alone:

```bash
docker compose up -d
```

Bring up the API stack **and** the web app together by passing both files:

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

!!! tip "You may not need to self-host the web app"
    Because native apps let a user save and switch between servers, and the web
    build points at whatever API it is configured for, some operators run only the
    API stack and let users reach it from the published apps. Serve the web app
    yourself when you want a branded `https://track.example.com` in the browser.

There is also a third file for local development, `docker-compose.dev.yml`, which
starts only the infrastructure (Mongo, MinIO, Mailpit) so you can run the server
from your IDE. See [Development](/en/development.html).

## Profiles: dev vs prod

The server chooses its behavior from the Spring profile in
`SPRING_PROFILES_ACTIVE`:

- **`prod`** — MongoDB is a TLS replica set with **X.509 client authentication**
  (no password in the connection string). This is what `docker-compose.yml` uses
  and what you deploy. The demo seeder is compiled out (`@Profile("!prod")`).
- **`dev`** — MongoDB runs standalone (still TLS + X.509) for a single developer
  on `localhost`. Used with `docker-compose.dev.yml` when running the server from
  source.

!!! warning "Never run the demo seeder in production"
    `HINATA_DEMO_SEED=true` populates a realistic English demo workspace (login
    `rebar` / `hinata-demo-2026`) for screenshots and click-throughs. The seeder is
    annotated `@Profile("!prod")`, so it is **skipped entirely under the prod
    profile regardless of the flag** — but never rely on that as your only guard.
    Leave `HINATA_DEMO_SEED=false` in every production `.env`. Seeding a live
    instance would create a known-password admin and throwaway data in your real
    database.

## Configuration checklist

Work through these before you expose the instance. Each links to the page with the
concrete commands and file contents.

| Area | What to set | Page |
| --- | --- | --- |
| **Domain & TLS** | Public hostnames, a reverse proxy terminating HTTPS, forwarding to `HINATA_PORT` (API) and `HINATA_APP_PORT` (web) | [Reverse proxy & TLS](/en/reverse-proxy.html) |
| **JWT secret** | `HINATA_JWT_SECRET` — a random ≥ 64-char HS512 secret (required in prod) | [Production deployment](/en/deployment.html) |
| **MongoDB X.509** | Generate the PKI, register the client cert as the `$external` user | [MongoDB & X.509](/en/database.html) |
| **Object storage** | MinIO credentials and bucket, or point at an external S3 | [Object storage](/en/storage.html) |
| **SMTP** | A real mail relay so verification / reset / notification mail is delivered | [E-mail & SMTP](/en/email.html) |
| **CORS** | `HINATA_CORS_ALLOWED_ORIGINS` — the browser origins allowed to call the API | [Configuration reference](/en/configuration.html) |
| **Trusted proxies** | `HINATA_TRUSTED_PROXIES` — CIDRs of proxies allowed to set `X-Forwarded-For` | [Reverse proxy & TLS](/en/reverse-proxy.html) |
| **Gateway** | Usually the default; override `HINATA_GATEWAY_BASE_URL` only to run your own | [Hinata Connect gateway](/en/connect-gateway.html) |
| **First run** | Complete the in-app setup wizard, or automate it with `HINATA_SETUP_*` | [Setup & first run](/en/setup-wizard.html) |

For the exhaustive list of every environment variable — grouped, with defaults and
whether each is required — see the [Configuration reference](/en/configuration.html).

## Where to go next

- [Production deployment](/en/deployment.html) — the full, ordered walkthrough:
  secrets, PKI, image tags, `up -d`, health checks, DNS and the update flow.
- [Configuration reference](/en/configuration.html) — every setting, and the
  difference between env vars and runtime (database) settings.
- [MongoDB & X.509](/en/database.html), [Object storage](/en/storage.html),
  [E-mail & SMTP](/en/email.html), [Reverse proxy & TLS](/en/reverse-proxy.html) —
  the detailed per-subsystem pages.
- [Backups & upgrades](/en/backups.html) — keeping data safe across redeploys.
