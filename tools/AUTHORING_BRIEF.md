# Hinata Docs — Authoring Brief (single source of truth)

You are writing pages for the **official Hinata documentation site** (Liquid Glass
static site). Read this whole brief before writing. Facts here are authoritative;
if you need deeper detail, read the actual repos:

- Server: `/Users/rebar/Documents/Dev/Hivora/hinata-server` (Spring Boot 4, Java 21)
- App:    `/Users/rebar/Documents/Dev/Hivora/hinata-app` (Flutter)

> ⚠️ Do NOT expose internal/private infrastructure in the docs. Genericize every
> host to placeholders: use `track.example.com` (web app) and
> `api.track.example.com` (API). Never reference real internal servers, real
> customer domains, private repos, or secrets. The `.env.example` in the server
> repo uses `track.asta.hn` as a shipped default — you may mention it neutrally,
> but prefer the `example.com` placeholders in prose.

---

## 1. Markdown conventions (MANDATORY — the build depends on these)

Every page is a Markdown file with YAML-ish front matter, then a single `#` H1:

```markdown
---
title: Quick start
description: Get a Hinata server and app running in minutes with Docker Compose.
---

# Quick start

Intro paragraph (1–3 sentences, sets context).

## First section  (## and ### appear in the right-hand "On this page" TOC)
```

- **Front matter**: `title` and `description` (one sentence, ~120–160 chars, used
  for SEO/OpenGraph and search). Keep the `title` short; it should match the nav
  title. Do NOT put quotes issues — plain text.
- **H1**: exactly one `#` H1 = the page title. Body sections use `##` / `###`.
- **Admonitions** (styled as Liquid-Glass callouts). Syntax — `!!! type "Optional Title"`
  then an indented (4 spaces) body. Supported `type`: `note`, `info`, `tip`,
  `warning`, `danger`. Use them generously for Info/Warning/Tip as the user asked.

  ```markdown
  !!! warning "Change this in production"
      The default `HINATA_JWT_SECRET` is empty — generate a real 64-char secret.

  !!! tip
      You can set every value as a plain environment variable instead of `.env`.
  ```

- **Code blocks**: always fenced with a language (` ```bash `, ` ```yaml `,
  ` ```json `, ` ```properties `, ` ```dart `, ` ```text `, ` ```nginx `,
  ` ```dockerfile `). Copy buttons are added automatically. Show real, runnable
  snippets and configs — the user explicitly wants concrete code/config.
- **Tables**: standard Markdown tables for env vars, endpoints, comparisons.
- **Internal links**: link to other doc pages with root-absolute paths for the
  SAME language. In English pages link like `[Configuration](/en/configuration.html)`
  and the intro as `[Introduction](/en/)`. In German pages use `/de/...` and `/de/`.
  A full slug list is in section 7.
- **External links**: repos are
  `https://github.com/hinata-platform/hinata-app` and
  `https://github.com/hinata-platform/hinata-server`.
- Keep a warm, expert, encouraging tone. Explain *why*, not just *how*. Prefer
  short paragraphs, lots of concrete examples, and callouts.

### Bilingual requirement
For every assigned slug you write BOTH `content/en/<slug>.md` AND
`content/de/<slug>.md`. Write English first, then a faithful, natural German
translation with the SAME structure/headings/code. German tone: professional
"du" is fine (matches the product). Keep code/identifiers/env-var names unchanged;
translate prose and callout text. German front-matter `title` should match the
German nav title (section 7).

---

## 2. What Hinata is

Hinata is an **independent, open-source, self-hosted project & issue tracker** — a
modern alternative to hosted trackers. It is a **white-label** platform: operators
run their own server and can ship their own branded client. Licensed **GPL-3.0**.
Current platform version: **2.2.0**. No user, team or board limits, ever.

Two repositories:
- **hinata-server** — Spring Boot 4, Java 21, MongoDB (replica set), S3-compatible
  object storage (MinIO), SMTP mail. Publishes a Docker image to GHCR.
- **hinata-app** — a single Flutter codebase targeting **Android, iOS, Web and
  macOS**. State via bloc/cubit, routing via go_router, i18n via i18next (en + de),
  networking via dio (auto token refresh, `Accept-Language`). Charts via fl_chart.

**Design language**: navy navigation rail, warm-paper workspace, honey-amber accent
`#D9A032` that reads the same in light and dark, with liquid-glass surfaces on the
mobile nav, the ⌘K palette and the attachment lightbox.

## 3. Architecture

- App (Flutter) → `ApiClient` (dio, token refresh, `Accept-Language`) → REST
  `/api/v1` on the server. Server pushes live updates via **Server-Sent Events (SSE)**.
- Server persists to **MongoDB** (production = replica set: 2 data nodes + 1
  arbiter, TLS + X.509 client auth). Attachments live in **S3/MinIO** (presigned
  downloads, randomized object keys). Mail via **SMTP** (Mailpit in dev).
- **Hinata Connect gateway**: a central push-relay + universal-link relay so a
  single published white-label app can serve many servers; self-hosters need NO
  Firebase. The server registers itself with the gateway on boot. Default gateway
  URL: `https://connect.hinata.ahmadre.com` (override with `HINATA_GATEWAY_BASE_URL`).
- Runtime settings (SSO, e-mail ingest, push, git OAuth apps) are stored in MongoDB
  and managed from the app's Admin area; **DB overrides env** and changes apply
  **without a restart**. Secrets are write-only in the admin API (never echoed back).
- Localized errors: resolved server-side from `messages.properties` (en, default)
  and `messages_de.properties`, keyed by the client's `Accept-Language` header.

## 4. Environment variables (from server `.env.example`)

Active profile `SPRING_PROFILES_ACTIVE`: `dev` (local TLS/X.509 standalone) or
`prod` (replica set). Key variables:

| Variable | Purpose |
| --- | --- |
| `HINATA_BASE_URL` | Public API base URL (JWT issuer, SSO redirects), e.g. `https://api.track.example.com` |
| `HINATA_WEB_BASE_URL` | Flutter-web base URL; email deep links point here (blank ⇒ base URL) |
| `HINATA_SERVER_TAG` / `HINATA_APP_TAG` | Container image tags pulled from `ghcr.io/hinata-platform` (default `latest`) |
| `HINATA_JWT_SECRET` | **HS512 secret, ≥ 64 chars, required in prod.** Generate: `openssl rand -base64 64 \| tr -d '\n'` |
| `MONGO_ROOT_USERNAME` / `MONGO_ROOT_PASSWORD` | SCRAM root (internal/admin); the app uses X.509, not a password |
| `HINATA_MONGODB_URI` | Mongo connection string (dev). In prod it is X.509 and set in compose |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` / `..._TRUSTSTORE_PASSWORD` | Mongo TLS keystore/truststore passwords (default `changeit` — change it) |
| `HINATA_TRUSTED_PROXIES` | CIDRs of reverse proxies allowed to set `X-Forwarded-For`. Empty = trust none |
| `HINATA_SMTP_HOST/PORT/USERNAME/PASSWORD/AUTH/STARTTLS` | Outbound mail (Mailpit in dev, real relay in prod) |
| `HINATA_MAIL_FROM` | From address for outbound mail |
| `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` | MinIO credentials |
| `HINATA_S3_BUCKET` | Bucket name (default `hinata`); dev also uses `HINATA_S3_ACCESS_KEY/SECRET_KEY` |
| `HINATA_PRIVACY_POLICY_URL` | Privacy policy shown in the app (required for store releases) |
| `HINATA_APP_MIN_VERSION` | Minimum app version; older clients are force-updated |
| `HINATA_CORS_ALLOWED_ORIGINS` | Comma-separated browser origins allowed for CORS (the hosted web app calls cross-origin) |
| `HINATA_DOCS_ENABLED` | Expose the Scalar API-docs UI (default `false` in prod) |
| `HINATA_GATEWAY_BASE_URL` | Hinata Connect gateway URL (push + universal links); default `https://connect.hinata.ahmadre.com` |
| `HINATA_GATEWAY_BOOTSTRAP_SECRET` | Optional, if your gateway gates registration |
| `HINATA_SETUP_AUTO_COMPLETE` | Skip the in-app first-run wizard; with `HINATA_SETUP_ORGANIZATION_NAME`, `HINATA_SETUP_ADMIN_EMAIL/USERNAME/PASSWORD/DISPLAY_NAME` |
| `HINATA_DEMO_SEED` / `HINATA_DEMO_RESET` | Seed a realistic English demo workspace (dev only; seeder is `@Profile("!prod")`, skipped in prod). Login `rebar` / `hinata-demo-2026` |
| `HINATA_RATE_LIMIT_ENABLED` / `..._API` (300) / `..._AUTH` (10) | Rate limiting (requests/min) |
| `HINATA_MAX_LOGIN_FAILURES` (5) / `HINATA_LOGIN_BLOCK_MINUTES` (15) | Brute-force lockout |
| `HINATA_PORT` (3356) / `HINATA_APP_PORT` (3456) | Published host ports the reverse proxy forwards to |
| `HINATA_GIT_GITHUB_CLIENT_ID/_SECRET` | GitHub OAuth app credentials |
| `HINATA_GIT_GITLAB_CLIENT_ID/_SECRET` | GitLab OAuth app credentials |
| `HINATA_GIT_BITBUCKET_CLIENT_ID/_SECRET` | Bitbucket OAuth consumer credentials |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Public API base for OAuth callback + webhook registration (falls back to `HINATA_BASE_URL` + `/api/v1`) |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM key that encrypts stored access tokens at rest (change default in prod) |

## 5. Quick start (production)

```bash
cp .env.example .env
./deploy/generate-secrets.sh   # creates the Mongo keyfile + prints secrets for .env
docker compose up -d
```

Brings up the server, a MongoDB **replica set (2 data nodes + 1 arbiter)**, MinIO
and Mailpit. Point the app at `HINATA_BASE_URL` and complete the in-app setup
wizard (or set `HINATA_SETUP_AUTO_COMPLETE=true`). MongoDB PKI for prod:
`./deploy/x509/generate-certs.sh prod` then `./deploy/x509/init-prod-user.sh`.

Local dev:
```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./mvnw spring-boot:run
```
Mailpit UI `http://localhost:8025`, MinIO console `http://localhost:9001`. Tests: `./mvnw verify`.

## 6. Feature facts (be thorough & accurate)

- **Dashboard**: today's focus, completion, team ranking, weekly tracker.
- **Projects & teams**: per-project workflows, issue numbering/keys (e.g. `ASTA-42`),
  reusable project labels, project members. **Teams**: per-member project access
  gates app-wide visibility (a member only sees projects their team grants).
- **Issues**: types, priorities, tags/labels, comments, attachments (S3),
  dependencies. **Hierarchy** is Jira-style 3-level: **Epic → Story/Task/Bug/Feature
  → Sub-task**. Board can group into swimlanes by none/epic/assignee/subtask, with
  epic filtering; breadcrumb + parent picker + child/sub-task panels.
- **Labels & workflow states**: colored, `{id, name, hue}`, name-keyed, editable in
  Project Settings with a draft + save-bar editor; server rename cascade.
- **Agile boards**: columns mapped to workflow states, WIP limits, backlog (=
  no-sprint issues). Views: **Board / Backlog / Timeline** switcher, people filter,
  sprint header, glass filter popup.
- **Sprints**: plan / start / complete, capacity & story points, burndown report.
- **Gantt / Timeline**: read model — start/due dates, dependencies, progress.
- **Time tracking**: work items with activity types + weekly timesheets.
- **Reports**: burndown, velocity, cycle time; distributions by state/priority/
  assignee; created vs. resolved. Export to PDF (pdf + printing).
- **Knowledge base**: Confluence-style hierarchical Markdown articles, global or
  per project, team/project access control, smart links that resolve real
  issues/people, shared markdown toolbar. Backend-backed (`/api/v1/articles`).
- **Attachments**: S3/MinIO + presigned URLs, atomic push/pull, **live SSE** add/
  remove, drag-drop grid + glass lightbox, ENV-driven size/type limits.
- **Notifications**: in-app + e-mail (SMTP); push via the Connect gateway.
- **Global search / command palette**: ⌘K liquid-glass search/command palette;
  triggers, recents, responsive sheet.
- **Account / settings** (`/settings`): profile, e-mail change, 2FA (TOTP),
  sessions, notification matrix, GDPR export/delete, avatar upload (S3-backed).
- **Auth**: local credentials; self-registration + email verification;
  forgot-password (deep link); optional admin approval. Feature flags:
  `localAuthEnabled`, `registrationEnabled`, `requireAdminApproval` (via AuthPolicy,
  editable in admin). Login 2FA challenge when TOTP enabled.
- **Admin → App settings**: `minVersion`, privacy URL, feature flags editable in
  the Admin area (DB overrides env `hinata.app.*`).

## 6b. Git integration (full detail — from server README)

Connect each project to one OR MORE repos on GitHub, GitLab or Bitbucket. The
server brokers a real OAuth flow, registers a signed webhook, and turns push /
PR / CI events into per-issue development info (branches, commits, PR/MRs, build
status) — plus smart commits and status automation. Nothing is emulated; an event
only lands when its signature verifies.

**Operator setup (one-time, platform-wide)**: register ONE OAuth app per provider,
give the server its credentials in Admin → Git integration (Mongo, DB overrides
env, secrets write-only) or via env. Set a public API base
`HINATA_GIT_WEBHOOK_BASE_URL` (e.g. `https://api.track.example.com/api/v1`);
falls back to `HINATA_BASE_URL` + `/api/v1`. Register this OAuth callback at each
provider: `<public-api-base>/git/oauth/callback`.

**OAuth flow (server-brokered)**: App → `POST /projects/{id}/git/oauth/start` →
server returns authorize URL + session state (Mongo, TTL 15m) → user consents in
browser → provider hits `GET /git/oauth/callback?code&state` (public) → server
exchanges code→token (stored AES-GCM) → app polls
`GET /git/oauth/session/{state}` → AUTHORIZED → owners → repos → connect (registers
webhook). Self-managed GitHub Enterprise / GitLab / Bitbucket Data Center skip
OAuth: `POST /projects/{id}/git/connect-token` with repo URL + personal access token.

**Webhooks** (per-project secret, signature-verified):
| Provider | Endpoint | Verification |
| --- | --- | --- |
| GitHub | `POST /git/webhooks/github` | HMAC-SHA256 over raw body (`X-Hub-Signature-256`) |
| GitLab | `POST /git/webhooks/gitlab` | token compare (`X-Gitlab-Token`) |
| Bitbucket | `POST /git/webhooks/bitbucket` | shared secret in URL (`?secret=…`) |

Linking: branch by the key in its name, commit by key(s) in its message, PR/MR by
its title or source branch. A commit is never linked just because it rides on an
issue's branch. Side effects (smart commits + commit-pushed transition) are applied
**exactly once**, guarded by a `git_processed_commits` ledger (providers redeliver
webhooks; merges re-list commits).

**Automation** (per project, against that project's workflow states): branch created
→ move (e.g. In Progress); commit pushed referencing the key → move; PR/MR opened →
move (In Review); PR/MR merged → move (Done). Automation only moves issues FORWARD,
never backward. **Smart commits**: trailers in a commit message act on the issue —
`ASTA-42 #comment shipped` adds a comment, `#time 2h 30m` logs work, any other
`#word` transitions the issue. Tokens/secrets AES-GCM-encrypted at rest, never
returned. A project can connect several repos; automation rules + branch template
are shared project-wide, each repo keeps its own token/webhook/default branch.

## 6c. SSO

Runtime-configured (Admin area, stored in Mongo, no restart): **OpenID Connect,
OAuth 2.0, SAML 2.0, LDAP** — e.g. Synology SSO, Keycloak, Authentik, Azure AD,
Google. SSO returns to the app via the `hinata://auth-callback` deep link. The
OAuth2 authorization-request state is stored in Mongo (not cookie/session) so it
works behind proxies/tunnels. Public endpoint: `/auth/sso/providers`.

## 6d. Security model

Stateless **JWT (HS512)**, short-lived access + refresh tokens (refresh rejected
for API access). **BCrypt** (strength 12), min 10-char passwords. DB-backed login
blocking (survives restarts) + **bucket4j** rate limiting per client IP (strict on
`/auth/**`). `/api/v1/admin/**` requires `ADMIN`. Hardened headers (HSTS, CSP,
no-referrer), localized stable JSON errors without stack traces, regex-escaped
search input. Content-type & size-validated uploads with randomized S3 keys,
presigned downloads. Secrets write-only in the admin API. Mapped to OWASP Top 10.

## 6e. E-mail → ticket (IMAP)

IMAP polling turns inbound mail into issues. Runtime-configured in the Admin area
(stored in Mongo, no restart).

## 6f. Hinata Connect gateway

Central push-relay + universal-link relay (`connect.hinata.ahmadre.com`) so ONE
white-label app serves many servers. The server registers itself on boot; per-server
FCM/firebase-admin lives in the gateway, not each server — self-hosters need no
Firebase. The app handles universal links `/l/<code>`. Override with
`HINATA_GATEWAY_BASE_URL` to run your own gateway.

## 6g. Multi-server & white-label

Native apps must NEVER bake in a server URL (web build may default via `kIsWeb`).
Users save multiple servers and switch between them; tokens are scoped per server.
A liquid-glass Server Manager shows live probe status/ping and lets you add/edit/
delete/switch servers, with a connection test on add. White-label = build your own
branded client: package id (e.g. `com.yourorg.yourapp`), app name, icons/splash,
accent, and point it at the gateway. Deep links: Android App Links + iOS Universal
Links for `https://track.example.com` (assetlinks.json / AASA served by the web
image; iOS needs the Associated Domains capability).

## 6h. API

REST under `/api/v1`. Public endpoints (no token):
`/meta`, `/setup/status`, `/setup`, `/auth/login`, `/auth/refresh`,
`/auth/sso/providers`, `/actuator/health`. Everything else needs a Bearer token.
Attachment changes stream over SSE at
`/api/v1/issues/{issueId}/attachments/stream`. Optional Scalar API-docs UI gated
by `HINATA_DOCS_ENABLED` (off in prod).

## 7. Page catalog (slug → EN title / DE title)

overview: index (Introduction / Einführung), architecture (Architecture / Architektur),
concepts (Core concepts / Grundkonzepte).
getting-started: quick-start (Quick start / Schnellstart), requirements (Requirements / Voraussetzungen).
self-hosting: self-hosting (Overview / Überblick), deployment (Production deployment / Produktiv-Deployment),
configuration (Configuration reference / Konfigurationsreferenz), database (MongoDB & X.509 / MongoDB & X.509),
storage (Object storage (S3/MinIO) / Objektspeicher (S3/MinIO)), email (E-mail & SMTP / E-Mail & SMTP),
reverse-proxy (Reverse proxy & TLS / Reverse Proxy & TLS), setup-wizard (Setup & first run / Setup & Erststart),
backups (Backups & upgrades / Backups & Upgrades).
features: features (Feature tour / Feature-Tour), projects-teams (Projects & teams / Projekte & Teams),
issues (Issues & hierarchy / Vorgänge & Hierarchie), boards-sprints (Boards & sprints / Boards & Sprints),
timeline (Gantt & time tracking / Gantt & Zeiterfassung), reports (Reports & dashboard / Berichte & Dashboard),
knowledge-base (Knowledge base / Wissensdatenbank), notifications (Notifications / Benachrichtigungen),
search (Search & palette / Suche & Palette).
security: authentication (Authentication / Authentifizierung), sso (Single sign-on (SSO) / Single Sign-on (SSO)),
security (Security model / Sicherheitsmodell).
integrations: git-integration (Git integration / Git-Integration),
email-to-ticket (E-mail to ticket / E-Mail zu Vorgang), connect-gateway (Hinata Connect gateway / Hinata Connect Gateway).
apps: clients (The apps / Die Apps), white-label (White-label & branding / White-Label & Branding).
administration: admin-area (Admin area / Adminbereich), project-settings (Project settings / Projekteinstellungen).
reference: api (API reference / API-Referenz), development (Development / Entwicklung),
contributing (Contributing / Mitwirken), faq (FAQ & troubleshooting / FAQ & Fehlerbehebung).
```
