---
title: Quick start
description: Get a Hinata server and app running in minutes with Docker Compose, using three commands, a JWT secret and the in-app setup wizard.
---

# Quick start

With Docker, you are about three commands away from a running server, database, object storage and mail catcher. Then you point the app at it and complete a short setup wizard.

!!! note "Prerequisites"
    A host with **Docker Engine + Docker Compose v2** and this repo checked out. That's all the quick start needs. For sizing and network detail, see [Requirements](/en/requirements.html).

## The three commands

From the root of the [hinata-server](https://github.com/hinata-platform/hinata-server) repository:

```bash
cp .env.example .env
./deploy/generate-secrets.sh   # creates the Mongo keyfile + prints secrets for .env
docker compose up -d
```

1. **`cp .env.example .env`** creates your config file from the template. Every setting is an environment variable. The full list is in the [Configuration reference](/en/configuration.html).
2. **`./deploy/generate-secrets.sh`** generates the MongoDB replica-set **keyfile** (required for internal cluster auth) and prints strong random secrets for `.env`. Run it before the first `up`.
3. **`docker compose up -d`** pulls the images from `ghcr.io/hinata-platform` and starts the stack in the background.

## What comes up

`docker compose up -d` starts the whole development-style stack:

| Container | Role |
| --- | --- |
| **server** | The Spring Boot API at `/api/v1` (host port `3356` by default). |
| **MongoDB replica set** | 2 data nodes + 1 arbiter, the system of record. |
| **MinIO** | S3-compatible object storage for attachments and avatars. |
| **Mailpit** | Local mail catcher. Shows outbound e-mail without a real relay. |

Wait a few seconds, then check the server:

```bash
curl -s http://localhost:3356/api/v1/actuator/health
# {"status":"UP"}
```

!!! info "Handy local UIs"
    Mailpit's inbox is at `http://localhost:8025` and the MinIO console at `http://localhost:9001`. Use them to confirm mail and uploads work before you go to production.

## Set the JWT secret (required)

Hinata signs its stateless access and refresh tokens with an **HS512** secret. The template ships it **empty**, and in production the server rejects an empty or weak value. Generate a real one with at least 64 characters:

```bash
openssl rand -base64 64 | tr -d '\n'
```

Paste the output into `.env`:

```properties
HINATA_JWT_SECRET=PASTE_YOUR_64_CHAR_SECRET_HERE
```

!!! danger "Do not ship defaults"
    The default `HINATA_JWT_SECRET` is **empty**. The template's `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` and the TLS keystore/truststore password (`changeit`) are **placeholders**. Before any internet-facing deployment, set a real JWT secret and replace every default password. `./deploy/generate-secrets.sh` prints strong values for this.

After changing `.env`, recreate the server so it picks up the new environment:

```bash
docker compose up -d
```

## Point the app at your server

People use Hinata through the [app](/en/clients.html). It works with multiple servers and never hardcodes a URL, so you tell it where your server is.

Set your public API base in `.env`. Tokens are then issued for the right host, and e-mail links lead to your server:

```properties
HINATA_BASE_URL=https://api.track.example.com
```

Then open the **Server Manager** in the app, add your server (it runs a live connection test) and switch to it. On the web build, just open the web app served alongside the API. For a local test, `http://localhost:3356` works from the same machine.

!!! tip "Local vs. production hosts"
    This quick start uses `localhost`. For access from other devices you need public DNS and TLS in front of the server, because the app expects `https://` for saved servers. See [Reverse proxy & TLS](/en/reverse-proxy.html).

## Complete the setup wizard

On first run the server has no organization or admin yet. Open the app against your new server and complete the **in-app setup wizard**: name your organization and create the first ADMIN account. After that you can create projects, invite people and start working.

For CI or scripted installs, skip the wizard:

```properties
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-please
HINATA_SETUP_ADMIN_DISPLAY_NAME=Admin
```

For details and a walkthrough with screenshots, see [Setup & first run](/en/setup-wizard.html).

## You're running Hinata

Server, database, storage, mail and an admin account are running. Next, make the stack production-grade.

## Next steps

- **[Production deployment](/en/deployment.html):** replica set with X.509 certificates and GHCR image tags.
- **[Configuration reference](/en/configuration.html):** every environment variable, what it does and its default.
- **[Reverse proxy & TLS](/en/reverse-proxy.html):** put a proxy in front, terminate TLS and forward to ports `3356`/`3456`.
- **[Requirements](/en/requirements.html):** host sizing, network and what a real deployment needs.
