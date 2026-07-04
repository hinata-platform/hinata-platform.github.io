---
title: Quick start
description: Get a Hinata server and app running in minutes with Docker Compose — three commands, a JWT secret, and the in-app setup wizard.
---

# Quick start

This is the fastest path from nothing to a running Hinata stack. If you have Docker, you are about three commands away from a live server, database, object storage and a mail catcher — then you point the app at it and complete a short setup wizard.

!!! note "Prerequisites (one line)"
    A host with **Docker Engine + Docker Compose v2** and this repo checked out. That's it for the quick start. For sizing and network detail, see [Requirements](/en/requirements.html).

## The three commands

From the root of the [hinata-server](https://github.com/hinata-platform/hinata-server) repository:

```bash
cp .env.example .env
./deploy/generate-secrets.sh   # creates the Mongo keyfile + prints secrets for .env
docker compose up -d
```

What each step does:

1. **`cp .env.example .env`** — creates your local configuration file from the shipped template. Every setting is an environment variable; `.env` is where you fill in the ones that matter for your deployment. The full list lives in the [Configuration reference](/en/configuration.html).
2. **`./deploy/generate-secrets.sh`** — generates the MongoDB replica-set **keyfile** (required for internal cluster auth) and prints strong random secrets for you to paste into `.env`. Run it before the first `up`.
3. **`docker compose up -d`** — pulls the images from `ghcr.io/hinata-platform` and starts the stack in the background.

## What comes up

`docker compose up -d` brings the whole development-style stack online:

| Container | Role |
| --- | --- |
| **server** | The Spring Boot API at `/api/v1` (host port `3356` by default). |
| **MongoDB replica set** | 2 data nodes + 1 arbiter — the system of record. |
| **MinIO** | S3-compatible object storage for attachments and avatars. |
| **Mailpit** | A local mail catcher so you can see outbound e-mail without a real relay. |

Give it a few seconds, then check the server is healthy:

```bash
curl -s http://localhost:3356/api/v1/actuator/health
# {"status":"UP"}
```

!!! info "Handy local UIs"
    Mailpit's inbox is at `http://localhost:8025` and the MinIO console at `http://localhost:9001`. Both are great for confirming that mail and uploads are working before you go to production.

## Set the JWT secret — this is a MUST

Hinata signs its stateless access and refresh tokens with an **HS512** secret. The template ships this **empty**, and in production the server will not accept an empty or weak value. Generate a real one (at least 64 characters):

```bash
openssl rand -base64 64 | tr -d '\n'
```

Paste the output into `.env`:

```properties
HINATA_JWT_SECRET=PASTE_YOUR_64_CHAR_SECRET_HERE
```

!!! danger "Do not ship defaults"
    The default `HINATA_JWT_SECRET` is **empty**, and the template's `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` and the TLS keystore/truststore password (`changeit`) are **placeholders**. Before any internet-facing deployment, set a real JWT secret and replace every default password. `./deploy/generate-secrets.sh` prints strong values for exactly this reason.

After changing `.env`, recreate the server so it picks up the new environment:

```bash
docker compose up -d
```

## Point the app at your server

The server is only half the stack — the [app](/en/clients.html) is how people use it. The app is multi-server: it never hardcodes a URL, so you tell it where your server is.

Set your public API base in `.env` so tokens are issued for the right host and e-mail deep links point home:

```properties
HINATA_BASE_URL=https://api.track.example.com
```

Then, in the app, open the **Server Manager**, add your server (it runs a live connection test), and switch to it. On the web build you can simply visit the web app served alongside the API. For a local test, `http://localhost:3356` works from the same machine.

!!! tip "Local vs. production hosts"
    In this quick start we use `localhost`. For anything reachable from other devices you'll want public DNS and TLS in front of the server — the app expects `https://` for saved servers. See [Reverse proxy & TLS](/en/reverse-proxy.html).

## Complete the setup wizard

On first run the server has no organization or admin yet. Open the app against your new server and complete the **in-app setup wizard**: name your organization and create the first ADMIN account. From that moment you can create projects, invite people and start working.

Prefer a hands-off boot (for CI or scripted installs)? Skip the wizard entirely:

```properties
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-please
HINATA_SETUP_ADMIN_DISPLAY_NAME=Admin
```

For the mechanics and a screenshot-by-screenshot walkthrough, see [Setup & first run](/en/setup-wizard.html).

## You're running Hinata

That's a live stack: server, database, storage, mail, and an admin account. From here, the sensible next steps are all about making it production-grade.

## Next steps

- **[Production deployment](/en/deployment.html)** — the real replica-set path with X.509 certificates and GHCR image tags.
- **[Configuration reference](/en/configuration.html)** — every environment variable, what it does and its default.
- **[Reverse proxy & TLS](/en/reverse-proxy.html)** — put a proxy in front, terminate TLS, and forward to ports `3356`/`3456`.
- **[Requirements](/en/requirements.html)** — host sizing, network and the pieces you'll want for a real deployment.
