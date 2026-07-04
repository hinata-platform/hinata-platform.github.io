---
title: Configuration reference
description: The definitive reference for every Hinata environment variable, grouped by area, plus how runtime database settings override env.
---

# Configuration reference

This is the complete reference for configuring a Hinata server. Every setting is
an environment variable — read from `.env` (via Docker Compose) or supplied
directly on the container. Below they are grouped by area, with purpose, a default
or example, and whether the variable is required.

A second class of settings — SSO, e-mail ingest, push, Git OAuth apps — lives in
the database and is managed from the app's Admin area. The final section explains
how the two relate.

!!! tip "Everything can be a plain environment variable"
    `.env` is just convenient loading for Compose. Any value here can equally be
    set as an environment variable on the container by your orchestrator. Names and
    semantics are identical.

## Core / URLs

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `SPRING_PROFILES_ACTIVE` | Active profile: `prod` (replica set, X.509) or `dev` (standalone) | `prod` | Yes |
| `HINATA_BASE_URL` | Public API base URL — JWT issuer and SSO redirect base | `https://api.track.example.com` | Yes |
| `HINATA_WEB_BASE_URL` | Flutter-web base URL; e-mail deep links point here. Blank ⇒ falls back to the base URL | `https://track.example.com` | No |

## Container images

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_SERVER_TAG` | Tag of `ghcr.io/hinata-platform/hinata-server` to run | `latest` (pin e.g. `2.2.0`) | No |
| `HINATA_APP_TAG` | Tag of `ghcr.io/hinata-platform/hinata-app` (web app overlay) | `latest` (pin e.g. `2.2.0`) | No |

!!! tip
    Pin both tags to a specific version in production so every host runs the same
    build and rollbacks are a one-line change.

## Security / JWT

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_JWT_SECRET` | HS512 signing secret, **≥ 64 chars**. Generate: `openssl rand -base64 64 \| tr -d '\n'` | *(empty)* | **Yes (prod)** |

!!! warning
    The server will not start in the `prod` profile without a valid
    `HINATA_JWT_SECRET`. Rotating it invalidates all existing tokens.

## MongoDB

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `MONGO_ROOT_USERNAME` | SCRAM root username (internal/admin only; the app authenticates with X.509) | `hinata` | Yes |
| `MONGO_ROOT_PASSWORD` | SCRAM root password | `hinata-dev-secret` (change it) | **Yes (prod)** |
| `HINATA_MONGODB_URI` | Mongo connection string. In prod it is set to the X.509 URI in `docker-compose.yml`; set explicitly only for dev / external Mongo | *(set in compose)* | No (prod) |
| `HINATA_MONGO_TLS_ENABLED` | Enable TLS for the Mongo connection | `true` (prod, in compose) | No |
| `HINATA_MONGO_TLS_KEYSTORE` | Path to the app's PKCS#12 client keystore in the container | `/etc/hinata/x509/hinata-app.p12` | No (prod, in compose) |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | Password for the client keystore | `changeit` (change it) | **Yes (prod)** |
| `HINATA_MONGO_TLS_TRUSTSTORE` | Path to the CA truststore in the container | `/etc/hinata/x509/truststore.p12` | No (prod, in compose) |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | Password for the truststore | `changeit` (change it) | **Yes (prod)** |

See [MongoDB & X.509](/en/database.html) for how the PKI is generated and the
`$external` user registered.

## Reverse proxies

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_TRUSTED_PROXIES` | Comma-separated CIDRs of reverse proxies allowed to set `X-Forwarded-For`. Empty = trust none | `172.16.0.0/12` | Recommended |

!!! warning
    Set this to exactly the address range your proxy reaches the container from.
    Empty means the server ignores forwarded headers (rate limiting / logging see
    the proxy IP); too wide lets clients spoof their source IP.

## SMTP (outbound mail)

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_SMTP_HOST` | SMTP relay host | `smtp.example.com` (`mailpit` in dev) | Yes (for mail) |
| `HINATA_SMTP_PORT` | SMTP port | `587` (`1025` for Mailpit) | Yes (for mail) |
| `HINATA_SMTP_USERNAME` | SMTP auth username | *(empty)* | If auth |
| `HINATA_SMTP_PASSWORD` | SMTP auth password | *(empty)* | If auth |
| `HINATA_SMTP_AUTH` | Enable SMTP authentication | `true` (`false` in dev) | No |
| `HINATA_SMTP_STARTTLS` | Enable STARTTLS | `true` (`false` in dev) | No |
| `HINATA_MAIL_FROM` | From address on outbound mail | `hinata@example.com` | Yes (for mail) |

Deep-link e-mails (verification, password reset, assignment notifications) are
only delivered with a real relay. See [E-mail & SMTP](/en/email.html).

## S3 / MinIO (object storage)

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `MINIO_ROOT_USER` | MinIO root user (also used as the S3 access key in compose) | `hinata` | Yes |
| `MINIO_ROOT_PASSWORD` | MinIO root password (also the S3 secret key in compose) | `hinata-dev-secret` (change it) | **Yes (prod)** |
| `HINATA_S3_ENDPOINT` | S3 endpoint the server talks to | `http://minio:9000` (in compose) | No (prod, in compose) |
| `HINATA_S3_ACCESS_KEY` | S3 access key (dev / external S3) | `hinata` | Dev / external |
| `HINATA_S3_SECRET_KEY` | S3 secret key (dev / external S3) | `hinata-dev-secret` | Dev / external |
| `HINATA_S3_BUCKET` | Bucket for attachments and avatars | `hinata` | No |

In production compose, `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` are wired to
`MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` automatically. See
[Object storage](/en/storage.html).

## App integration

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_PRIVACY_POLICY_URL` | Privacy policy URL shown in the app (required for store releases) | `https://example.com/privacy` | Recommended |
| `HINATA_APP_MIN_VERSION` | Minimum app version; older clients are force-updated | `1.0.0` | No |
| `HINATA_CORS_ALLOWED_ORIGINS` | Comma-separated browser origins allowed for CORS (the web app calls cross-origin) | `https://track.example.com` | **Yes (web)** |
| `HINATA_DOCS_ENABLED` | Expose the Scalar API-docs UI | `false` | No |

## Hinata Connect gateway

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Push + universal-link gateway URL. The server registers on boot; override only to run your own gateway | `https://connect.hinata.ahmadre.com` | No |
| `HINATA_GATEWAY_BOOTSTRAP_SECRET` | Bootstrap secret, only if your gateway gates registration | *(empty)* | No |

See [Hinata Connect gateway](/en/connect-gateway.html).

## Setup (first run)

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_SETUP_AUTO_COMPLETE` | Skip the in-app first-run wizard | `false` | No |
| `HINATA_SETUP_ORGANIZATION_NAME` | Organization name (with auto-complete) | *(empty)* | If auto-complete |
| `HINATA_SETUP_ADMIN_EMAIL` | First admin e-mail | *(empty)* | If auto-complete |
| `HINATA_SETUP_ADMIN_USERNAME` | First admin username | *(empty)* | If auto-complete |
| `HINATA_SETUP_ADMIN_PASSWORD` | First admin password | *(empty)* | If auto-complete |
| `HINATA_SETUP_ADMIN_DISPLAY_NAME` | First admin display name | *(empty)* | If auto-complete |

See [Setup & first run](/en/setup-wizard.html).

## Demo seed (dev only)

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_DEMO_SEED` | Seed a realistic English demo workspace. Login `rebar` / `hinata-demo-2026`. Skipped under `prod` (seeder is `@Profile("!prod")`) | `false` | No |
| `HINATA_DEMO_RESET` | Wipe and re-seed the workspace on every boot. Requires `HINATA_DEMO_SEED=true` | `false` | No |

!!! danger "Never enable the demo seed in production"
    It creates a known-password admin and throwaway data. The seeder is compiled
    out under the `prod` profile, but keep `HINATA_DEMO_SEED=false` in production
    regardless.

## Rate limiting / brute force

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | Enable per-IP rate limiting (bucket4j) | `true` | No |
| `HINATA_RATE_LIMIT_API` | General API budget (requests / minute) | `300` | No |
| `HINATA_RATE_LIMIT_AUTH` | Auth endpoints budget (requests / minute) | `10` | No |
| `HINATA_MAX_LOGIN_FAILURES` | Failed logins before an account is blocked | `5` | No |
| `HINATA_LOGIN_BLOCK_MINUTES` | How long a blocked account stays locked (minutes) | `15` | No |

Login blocking is database-backed, so it survives restarts. See the
[Security model](/en/security.html).

## Ports

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_PORT` | Published host port for the API (container `8080`); the reverse proxy forwards here | `3356` | No |
| `HINATA_APP_PORT` | Published host port for the web app (container `80`) | `3456` | No |

## Git integration

Platform-wide OAuth credentials for connecting projects to GitHub / GitLab /
Bitbucket. These can also be set at runtime in Admin → Git integration (which
overrides env). See [Git integration](/en/git-integration.html).

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` | GitHub OAuth app client ID | *(empty)* | If GitHub |
| `HINATA_GIT_GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret | *(empty)* | If GitHub |
| `HINATA_GIT_GITLAB_CLIENT_ID` | GitLab OAuth app client ID | *(empty)* | If GitLab |
| `HINATA_GIT_GITLAB_CLIENT_SECRET` | GitLab OAuth app client secret | *(empty)* | If GitLab |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` | Bitbucket OAuth consumer key | *(empty)* | If Bitbucket |
| `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Bitbucket OAuth consumer secret | *(empty)* | If Bitbucket |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Public API base for the OAuth callback and webhook registration. Falls back to `HINATA_BASE_URL` + `/api/v1` | `https://api.track.example.com/api/v1` | No |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM key encrypting stored access tokens at rest — **change the default in production** | *(default; change it)* | Recommended |

## Runtime (DB) settings vs environment

Hinata has two configuration planes, and it is important to know which lives where.

**Environment variables (this page)** are read at startup. They cover
infrastructure and secrets: URLs, the JWT secret, database and storage connection,
TLS, SMTP transport, ports, CORS, trusted proxies, rate limits. Changing one means
editing `.env` and restarting the container.

**Runtime settings** are stored in MongoDB and edited from the app's **Admin
area** while the server runs. They cover integrations you tune operationally:

- **SSO** providers — OpenID Connect, OAuth 2.0, SAML 2.0, LDAP
  ([SSO](/en/sso.html)).
- **E-mail → ticket** IMAP ingestion ([E-mail to ticket](/en/email-to-ticket.html)).
- **Push** configuration via the gateway.
- **Git integration** OAuth app credentials (the `HINATA_GIT_*` values above).
- **App settings** — `minVersion`, privacy URL and feature flags
  (`localAuthEnabled`, `registrationEnabled`, `requireAdminApproval`), editable
  under Admin → App.

Three rules govern the two planes:

1. **DB overrides env.** Where a setting exists in both — notably Git OAuth
   credentials and the app settings (`hinata.app.*`) — the value stored in the
   database wins. Env values act as the initial default / fallback.
2. **Changes apply without a restart.** Editing a runtime setting in the Admin area
   takes effect immediately; you do not redeploy.
3. **Secrets are write-only.** Secret fields in the admin API (OAuth secrets,
   tokens, passwords) are never echoed back after being saved — you can set or
   replace them, but not read them.

!!! info "Rule of thumb"
    If it is a connection string, a transport secret, or something the process
    needs before it can serve a request, it is an **environment variable**. If it
    is an integration you would reconfigure on a live system, it is a **runtime
    setting** in the Admin area.
