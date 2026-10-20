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

## Object storage (S3 / SeaweedFS / GCS / Azure)

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_STORAGE_PROVIDER` | Backend: `s3` (SeaweedFS, AWS S3, GCS interop, R2, Spaces, …) or `azure` (Azure Blob Storage) | `s3` | No |
| `COMPOSE_PROFILES` | `local-storage` runs the bundled SeaweedFS. Empty when using an external store | `local-storage` | No |
| `HINATA_S3_ENDPOINT` | S3 endpoint the server talks to | `http://seaweedfs:8333` (in compose) | External S3 |
| `HINATA_S3_ACCESS_KEY` | S3 access key. The bundled SeaweedFS sets up the server's identity from this key and the secret key | `hinata` | For S3 |
| `HINATA_S3_SECRET_KEY` | S3 secret key | *(from `generate-secrets.sh`)* | For S3 |
| `HINATA_S3_BUCKET` | Bucket (S3) or container (Azure) for attachments and avatars | `hinata` | No |
| `HINATA_S3_REGION` | Bucket region (AWS and region-aware providers) | `us-east-1` | External S3 |
| `HINATA_S3_ADDRESSING_STYLE` | S3 URL addressing: `auto`, `virtual-host` or `path`. The bundled store needs `path`, external stores usually `auto` | `path` (in compose), `auto` (server default) | No |
| `HINATA_S3_SSE` | Server-side encryption asked for on every object written or copied: `AES256` (SSE-S3) or empty. Any other value stops the server at startup | `AES256` (in `.env.example`) | With bundled SeaweedFS |
| `HINATA_AZURE_CONNECTION_STRING` | Azure storage account connection string (with `provider=azure`) | *(empty)* | Azure |
| `SEAWEEDFS_ADMIN_ACCESS_KEY` / `SEAWEEDFS_ADMIN_SECRET_KEY` | Admin identity of the bundled SeaweedFS. Only the `seaweedfs-setup` job uses it | `hinata-admin` / *(generated)* | With bundled SeaweedFS |
| `SEAWEEDFS_SSE_KEK` | Key that encrypts every object in the bundled SeaweedFS (64 hex characters). **Keep a copy apart from the server.** Without it nothing stored can be read again | *(generated)* | With bundled SeaweedFS |
| `SEAWEEDFS_JWT_VOLUME_WRITE` / `_VOLUME_READ` / `_FILER_WRITE` / `_FILER_READ` | Keys that sign requests between the parts of SeaweedFS | *(generated)* | With bundled SeaweedFS |
| `SEAWEEDFS_BACKUP_ACCESS_KEY` / `SEAWEEDFS_BACKUP_SECRET_KEY` | Optional read-only identity for backups. Not passed to the container by the stock compose file, see [Backups & upgrades](/en/backups.html) | *(empty)* | No |

SeaweedFS refuses to start while any of its keys is missing. `./deploy/generate-secrets.sh`
prints a fresh value for every secret. See [Object storage](/en/storage.html) for the
bundled store, setup per provider (AWS, GCS, Azure, R2, …) and moving from MinIO.

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
| `HINATA_RATE_LIMIT_REFRESH` | Budget for exchanging a refresh token (requests / minute). Its own, because presenting a token this server signed is not a guess at a password, and every client behind one address shares the sign-in budget | `60` | No |
| `HINATA_RATE_LIMIT_SSO` | Budget for the two redirects of a single sign-on (requests / minute). Its own, because a whole office behind one address signs in through it while the callback is reachable by anybody | `60` | No |
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

## Calendars, holidays and working hours

Organization admins keep holiday calendars on the [Organization](/en/organization.html) page. A calendar follows the statutory holidays of a region, which the server knows itself, or reads a calendar address, for example a public holiday calendar from Google, Apple or Outlook. Both fill every year on their own, see [Holidays](/en/organization.html#holidays). Which region the organization starts with is set by admins under **Admin area → General → Holidays of the platform**; without a choice the country of the server's time zone applies. With the calendar import on, people can also subscribe to their own calendars and take appointments over as time entries (see [Tracking your time](/en/guide-time.html#your-own-calendars)). The server fetches every one of these addresses itself. It never connects to a private or loopback address, whatever the lists below say. People plan their own working hours in their settings, and their absences in time tracking. All of it needs extended time tracking (`HINATA_TIME_TRACKING_ADVANCED_ENABLED`). See [Tracking your time](/en/guide-time.html).

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_HOLIDAYS_AUTO_FILL` | Every night and at every start, fills the current and the next year of each holiday calendar with a region or a calendar address, each year only once. With `false` calendar addresses are only read on request; a calendar with a region still fills when it is saved | `true` | No |
| `HINATA_ICS_SECRET` | Key that stored calendar addresses are encrypted with (AES-256-GCM), both holiday feeds and personal calendar subscriptions. Base64 of at least 32 bytes. Generate: `openssl rand -base64 32`. Without it, or with a shorter or invalid value, the server refuses to store a calendar address: holidays can only be entered by hand and nobody can subscribe to a calendar. **Never change it once set** | *(empty)* | For calendar addresses |
| `HINATA_ICS_ALLOWED_HOSTS` | Comma-separated hosts calendars may be fetched from: a host name or `*.example.org` for its subdomains. Empty means any public host | *(empty)* | No |
| `HINATA_ICS_DENIED_HOSTS` | Comma-separated hosts calendars are never fetched from, in the same notation. Checked before the allow list | *(empty)* | No |
| `HINATA_TIME_TRACKING_ICS_IMPORT_ENABLED` | Lets people subscribe to their own calendars and take appointments over as entries. Needs extended time tracking and `HINATA_ICS_SECRET`. The switch **Calendar import** under **Organization → Time tracking** takes precedence over this value | `false` | No |
| `HINATA_AVAILABILITY_DEFAULT_WEEKDAY_MINUTES` | Planned minutes per weekday, Monday first, for everyone who has not set their own hours | `480,480,480,480,480,0,0` | No |
| `HINATA_TIME_TRACKING_ABSENCE_MANAGEMENT_ENABLED` | Turns absence management on: types, entitlements, balances, requests and sick reports. Needs extended time tracking. The switch under **Organization → Time tracking** takes precedence over this value | `false` | No |
| `HINATA_TIME_TRACKING_ABSENCE_CALENDAR_VISIBILITY` | The team absence calendar: `OFF`, `BUSY_ONLY` (only that somebody is away) or `TYPE` (the type, never sickness). Only in force with absence management on. The choice under **Organization → Time tracking** takes precedence over this value | `OFF` | No |
| `HINATA_TIME_TRACKING_WORKLOAD_REPORTS_ENABLED` | Switches on the workload report under **Time tracking → Reports**: capacity against booked time per person, for organization admins and project leads only. Needs extended time tracking. The switch under **Organization → Time tracking** takes precedence over this value. See [Time tracking privacy](/en/time-tracking-privacy.html) | `false` | No |
| `HINATA_TIME_TRACKING_BILLING_ENABLED` | Switches billing on: hourly rates, billing reports and invoices, for organization admins and project leads only. Requires extended time tracking. The switch under **Organization → Time tracking** takes precedence over this value | `false` | No |
| `HINATA_TIME_TRACKING_CURRENCY` | The one currency of every amount (ISO 4217). The field under **Organization → Time tracking** takes precedence over this value | `EUR` | No |
| `HINATA_TIME_TRACKING_INVOICE_PREFIX` | What every invoice number starts with, before the year and the running number (`INV-2026-00001`). Capital letters and digits, at most 10. A new prefix starts a new sequence | `INV` | No |
| `HINATA_RATE_LIMIT_TIME_OFF_REQUESTS_PER_DAY` | Absence requests and sick reports per person per day. A day rather than a minute, because filing leave is a deliberate act and a per-minute budget would let a loop through anyway | `50` | No |

!!! info "Who keeps absences"
    Organization admins do, unless you say otherwise. Under **Organization → Time tracking** you can also name individual people as **absence keepers**. They keep types, grant entitlements, book corrections and decide requests without holding any other admin right. Their way in is in their own settings. The list is deliberately empty by default: whoever is on it sees sick days as sick days (Art. 9 GDPR), and the narrower circle is the right default. Once someone is named, organization admins only see that a person is away when they are sick, not why. With nobody named, organization admins keep absences themselves as before.

!!! info "The limit never blocks a sick report"
    A sick report is counted against the same daily budget but is never refused by it: § 5 EFZG knows a notification, not a permission. Reaching the limit only refuses further **requests**.

!!! danger "Never rotate `HINATA_ICS_SECRET`"
    A calendar address encrypted with one `HINATA_ICS_SECRET` cannot be read with another. Each address is also bound to the record it is stored in, so it cannot be copied into another one. If the key changes, every stored address becomes unreadable: holiday imports fail until an organization admin enters the address again, and every person's subscriptions fail with "The saved address can no longer be read" until they paste their address again. Holidays already imported and entries already taken over stay. Keep the key with your other secrets and back it up.

### How calendars are fetched

A calendar address is typed by a person, so the server treats every fetch as if anybody on the internet had chosen the address:

- **Only `https`**, on port 443 or 8443. A `webcal://` address is read as `https`. No user name or password in the address.
- **The host must be a name**, never an IP address. Every address it resolves to must be on the public internet, otherwise the host is refused. The server connects only to the addresses it checked, so a second DNS answer cannot point it inward.
- **No redirects.** A redirect is reported as an error, even to the same host.
- **Ten seconds** for lookup, connection and download together, and at most **2 MB** per calendar. At most four fetches run at once.
- The address never appears in a log, an API response or the audit log. People see only the host.

Subscriptions are read every half hour, skipping any read in the last 25 minutes. Unchanged calendars are asked for with `If-None-Match` / `If-Modified-Since`, so they cost little. People can also refresh one by hand, once a minute at most. After five failed reads in a row a subscription is paused until its owner resumes it. The server keeps each person's events from 30 days back to 90 days ahead, at most 5,000 per subscription, and each person can have up to 10 subscriptions. With extended time tracking or the calendar import off, nothing is fetched.

## Project templates and relative deadlines

A project can be copied, marked as a template and given an event date that its issues' deadlines hang on. With this off, projects behave exactly as they do today and there is no way to copy one. See [Project templates](/en/project-templates.html).

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_PROJECT_TEMPLATES_ENABLED` | Turns project templates and relative deadlines on: copy a project, mark one as a template, create a project from a template, and keep a deadline as an offset from the project's event date. The switch under **Admin area → Platform** takes precedence over this value | `false` | No |
| `HINATA_PROJECT_TEMPLATES_DEFAULT_BASIS` | What new relative deadlines count in while neither the organization nor the project sets its own: `CALENDAR` (calendar days) or `WORKING` (working days). Organization admins choose the default on the [Organization](/en/organization.html) page, and each project can differ from it. Existing deadlines keep their basis | `CALENDAR` | No |

!!! info "Working days need a holiday calendar"
    A deadline that counts in working days always skips weekends. It only skips public holidays when the project has a holiday calendar selected. Without one it counts a holiday like any other working day.

## Shift planning

Events with shifts that people sign up for. With this off, the app has no "Shifts" entry and the server answers every request to the module with 404. See [Shift planning](/en/shifts.html).

| Variable | Purpose | Default / example | Required |
| --- | --- | --- | --- |
| `HINATA_SHIFTS_ENABLED` | Turns shift planning on. The switch under **Admin area → Platform** takes precedence over this value. Only takes effect with transactions (`HINATA_MONGO_TRANSACTIONS=true`, which means a replica set); without them the module stays off and the server says so in the log at startup | `false` | No |

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
- IMAP ingestion for **E-mail → ticket** ([E-mail to ticket](/en/email-to-ticket.html)).
  Administrators can only route mail into projects they are a member of
- **Push** configuration via the gateway
- OAuth app credentials for **Git integration** (the `HINATA_GIT_*` values above)
- **Platform settings** under Admin → Platform: `minVersion`, the privacy URL,
  how people sign in (`localAuthEnabled`, `registrationEnabled`,
  `requireAdminApproval`) and what the platform offers

Time tracking, absences, holidays and the default for relative deadlines are
stored in MongoDB too. They are not part of the Admin area, though, but of the
[Organization](/en/organization.html) page, which organization admins edit.

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
