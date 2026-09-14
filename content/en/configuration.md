---
title: Configuration reference
description: Every Hinata environment variable by area, and how database settings override them.
---

# Configuration reference

Every setting of a Hinata server is an environment variable. Set it in `.env`
(for Docker Compose) or directly on the container. The tables list each area with
the purpose, a default or example, and whether the variable is required.

SSO, inbound e-mail, push and the Git OAuth apps live in the database instead.
You manage them in the app's Admin area. The last section explains how the two
fit together.

!!! tip "You do not need `.env`"
    `.env` is just a convenient way to load values for Compose. Your orchestrator
    can set any of them as environment variables on the container, with the same
    names and meaning.

## Core / URLs

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `SPRING_PROFILES_ACTIVE` | Active profile: `prod` (replica set, X.509) or `dev` (standalone) | `prod` | Yes |
| `HINATA_BASE_URL` | Public API base URL. Used as JWT issuer and SSO redirect base | `https://api.track.example.com` | Yes |
| `HINATA_WEB_BASE_URL` | Base URL of the Flutter web app. E-mail deep links point here. Blank ⇒ falls back to the base URL | `https://track.example.com` | No |

## Container images

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_SERVER_TAG` | Tag of `ghcr.io/hinata-platform/hinata-server` to run | `latest` (pin e.g. `{{version}}`) | No |
| `HINATA_APP_TAG` | Tag of `ghcr.io/hinata-platform/hinata-app` (web app overlay) | `latest` (pin e.g. `{{version}}`) | No |

!!! tip
    Pin both tags to a specific version in production. Every host then runs the
    same build, and a rollback is a one-line change.

## Security / JWT

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_JWT_SECRET` | HS512 signing secret, **≥ 64 chars**. Generate: `openssl rand -base64 64 \| tr -d '\n'` | *(empty)* | **Yes (prod)** |

!!! warning
    In the `prod` profile the server will not start without a valid
    `HINATA_JWT_SECRET`. Rotating it invalidates all existing tokens.

## MongoDB

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `MONGO_ROOT_USERNAME` | SCRAM root username (internal admin use only, the app authenticates with X.509) | `hinata` | Yes |
| `MONGO_ROOT_PASSWORD` | SCRAM root password | `hinata-dev-secret` (change it) | **Yes (prod)** |
| `HINATA_MONGODB_URI` | Mongo connection string. In prod the X.509 URI is set in `docker-compose.yml`. Only set it yourself for dev or external Mongo | *(set in compose)* | No (prod) |
| `HINATA_MONGO_TLS_ENABLED` | Enable TLS for the Mongo connection | `true` (prod, in compose) | No |
| `HINATA_MONGO_TLS_KEYSTORE` | Path to the app's PKCS#12 client keystore in the container | `/etc/hinata/x509/hinata-app.p12` | No (prod, in compose) |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | Password for the client keystore | `changeit` (change it) | **Yes (prod)** |
| `HINATA_MONGO_TLS_TRUSTSTORE` | Path to the CA truststore in the container | `/etc/hinata/x509/truststore.p12` | No (prod, in compose) |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | Password for the truststore | `changeit` (change it) | **Yes (prod)** |

See [MongoDB & X.509](/en/database.html) for how to generate the PKI and register
the `$external` user.

## Reverse proxies

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_TRUSTED_PROXIES` | Comma-separated CIDRs of reverse proxies allowed to set `X-Forwarded-For`. Empty = trust none | `172.16.0.0/12` | Recommended |

!!! warning
    Set this to exactly the address range your proxy reaches the container from.

    - Empty: the server ignores forwarded headers. Rate limiting and logs only
      see the proxy IP.
    - Too wide: clients can spoof their source IP.

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

E-mails with deep links (verification, password reset, assignment notifications)
are only delivered with a real relay. See [E-mail & SMTP](/en/email.html).

## Object storage (S3 / MinIO / GCS / Azure)

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_STORAGE_PROVIDER` | Backend: `s3` (MinIO, AWS S3, GCS interop, R2, Spaces, …) or `azure` (Azure Blob Storage) | `s3` | No |
| `COMPOSE_PROFILES` | `local-storage` runs the bundled MinIO. Empty when using an external store | `local-storage` | No |
| `MINIO_ROOT_USER` | MinIO root user (also used as the S3 access key in compose) | `hinata` | With bundled MinIO |
| `MINIO_ROOT_PASSWORD` | MinIO root password (also the S3 secret key in compose) | `hinata-dev-secret` (change it) | **With bundled MinIO (prod)** |
| `HINATA_S3_ENDPOINT` | S3 endpoint the server talks to | `http://minio:9000` (in compose) | External S3 |
| `HINATA_S3_ACCESS_KEY` | S3 access key (dev / external S3) | `hinata` | Dev / external |
| `HINATA_S3_SECRET_KEY` | S3 secret key (dev / external S3) | `hinata-dev-secret` | Dev / external |
| `HINATA_S3_BUCKET` | Bucket (S3) or container (Azure) for attachments and avatars | `hinata` | No |
| `HINATA_S3_REGION` | Bucket region (AWS and region-aware providers) | `us-east-1` | External S3 |
| `HINATA_S3_ADDRESSING_STYLE` | S3 URL addressing: `auto`, `virtual-host` or `path` | `auto` | No |
| `HINATA_AZURE_CONNECTION_STRING` | Azure storage account connection string (with `provider=azure`) | *(empty)* | Azure |

In production compose, `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` fall back
to `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` automatically. See
[Object storage](/en/storage.html) for setup per provider (AWS, GCS, Azure, R2, …).

## App integration

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_PRIVACY_POLICY_URL` | Privacy policy URL shown in the app (required for store releases) | `https://example.com/privacy` | Recommended |
| `HINATA_APP_MIN_VERSION` | Minimum app version. Older clients are forced to update | `1.0.0` | No |
| `HINATA_CORS_ALLOWED_ORIGINS` | Comma-separated browser origins allowed for CORS (the web app calls cross-origin) | `https://track.example.com` | **Yes (web)** |
| `HINATA_DOCS_ENABLED` | Expose the Scalar API docs UI | `false` | No |

## Hinata Connect gateway

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Gateway URL for push and universal links. Defaults to the hosted gateway. Only override it when you ship your own branded app with your own gateway | `https://connect.hinata.ahmadre.com` | No |

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
    It creates an admin with a known password and throwaway data. The seeder is
    compiled out under the `prod` profile. Keep `HINATA_DEMO_SEED=false` in
    production anyway.

## Rate limiting / brute force

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | Enable per-IP rate limiting (bucket4j) | `true` | No |
| `HINATA_RATE_LIMIT_API` | General API budget (requests / minute) | `300` | No |
| `HINATA_RATE_LIMIT_AUTH` | Auth endpoints budget (requests / minute) | `10` | No |
| `HINATA_MAX_LOGIN_FAILURES` | Failed logins before an account is blocked | `5` | No |
| `HINATA_LOGIN_BLOCK_MINUTES` | How long a blocked account stays locked (minutes) | `15` | No |

Login blocking is stored in the database, so it survives restarts. See the
[Security model](/en/security.html).

## Ports

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_PORT` | Published host port for the API (container `8080`). The reverse proxy forwards here | `3356` | No |
| `HINATA_APP_PORT` | Published host port for the web app (container `80`) | `3456` | No |

## Git integration

Platform-wide OAuth credentials for connecting projects to GitHub, GitLab or
Bitbucket. You can also set them at runtime in Admin → Git integration, which
overrides env. See [Git integration](/en/git-integration.html).

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` | GitHub OAuth app client ID | *(empty)* | If GitHub |
| `HINATA_GIT_GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret | *(empty)* | If GitHub |
| `HINATA_GIT_GITLAB_CLIENT_ID` | GitLab OAuth app client ID | *(empty)* | If GitLab |
| `HINATA_GIT_GITLAB_CLIENT_SECRET` | GitLab OAuth app client secret | *(empty)* | If GitLab |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` | Bitbucket OAuth consumer key | *(empty)* | If Bitbucket |
| `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Bitbucket OAuth consumer secret | *(empty)* | If Bitbucket |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Public API base for the OAuth callback and webhook registration. Falls back to `HINATA_BASE_URL` + `/api/v1` | `https://api.track.example.com/api/v1` | No |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM key that encrypts stored access tokens at rest. **Change the default in production** | *(default; change it)* | Recommended |

## Runtime (DB) settings vs environment

Hinata has two configuration planes.

Environment variables (this page) are read at startup. They cover infrastructure
and secrets: URLs, the JWT secret, database and storage connection, TLS, SMTP
transport, ports, CORS, trusted proxies and rate limits. To change one, edit
`.env` and restart the container.

Runtime settings are stored in MongoDB. You edit them in the app's **Admin area**
while the server runs:

- **SSO** providers: OpenID Connect, OAuth 2.0, SAML 2.0, LDAP
  ([SSO](/en/sso.html))
- IMAP ingestion for **E-mail → ticket** ([E-mail to ticket](/en/email-to-ticket.html))
- **Push** configuration via the gateway
- OAuth app credentials for **Git integration** (the `HINATA_GIT_*` values above)
- **App settings** under Admin → App: `minVersion`, privacy URL and feature flags
  (`localAuthEnabled`, `registrationEnabled`, `requireAdminApproval`)

Three rules apply:

1. **DB overrides env.** If a setting exists in both, the database value wins.
   This mainly affects Git OAuth credentials and the app settings
   (`hinata.app.*`). Env values are only the initial default and fallback.
2. **No restart needed.** Changes in the Admin area apply immediately, without a
   redeploy.
3. **Secrets are write-only.** The admin API never returns OAuth secrets, tokens
   or passwords after they are saved. You can set or replace them, but not read
   them.

!!! info "Rule of thumb"
    If it is a connection string, a transport secret or something the process
    needs before it can serve a request, it is an **environment variable**. If it
    is an integration you would change on a live system, it is a **runtime
    setting** in the Admin area.
