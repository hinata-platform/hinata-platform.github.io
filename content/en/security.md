---
title: Security model
description: How Hinata hardens the platform, mapped to the OWASP Top 10, with a checklist for operators.
---

# Security model

Hinata is built to run on the public internet. This page lists the security controls, their environment variables and an **operator checklist**, all mapped to the **OWASP Top 10**.

Registration, 2FA and sessions from the user's side: [Authentication](/en/authentication.html). Federated login: [Single sign-on](/en/sso.html).

## Tokens and passwords

- **Stateless JWT, HS512.** Access tokens are short-lived, and a separate **refresh token** issues new ones. The **refresh token is rejected for normal API access** and only works at the refresh endpoint. A stolen access token expires quickly, and a stolen refresh token can't read data.
- **Revocable sessions.** Each token carries a session id (`sid`) tied to a record in the `sessions` collection. You can revoke single sessions without rotating the signing secret. See [Authentication → Sessions](/en/authentication.html).
- **BCrypt strength 12** for password hashing, with a **10-character minimum** length. Length and a deliberately slow hash protect against brute force.

!!! danger "Change the JWT secret before you expose the server"
    `HINATA_JWT_SECRET` is the HS512 signing key and must be a real secret of **at least 64 characters** in production. Generate one with:
    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```
    Anyone who knows this secret can forge tokens for any user. Never use the default.

## Login lockout and rate limiting

Two independent layers protect logins and the API.

**Database-backed login blocking.** Failed logins are counted, and the account or identifier is locked after a threshold. The counter lives in MongoDB, so the block **survives restarts** and works across multiple server instances.

| Variable | Default | Purpose |
| --- | --- | --- |
| `HINATA_MAX_LOGIN_FAILURES` | `5` | Failed attempts before the identifier is blocked |
| `HINATA_LOGIN_BLOCK_MINUTES` | `15` | How long the block lasts |

**Per-IP rate limiting** (via **bucket4j**) caps requests per client IP. `/auth/**` gets a **stricter budget** against password spraying and account enumeration.

| Variable | Default | Purpose |
| --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | `true` | Master switch for rate limiting |
| `HINATA_RATE_LIMIT_API` | `300` | Requests per minute for general API |
| `HINATA_RATE_LIMIT_AUTH` | `10` | Requests per minute for `/auth/**` (strict. The public SSO provider lookup counts against the API budget) |

!!! warning "Rate limiting needs the real client IP"
    Behind a reverse proxy, every request otherwise seems to come from the proxy. Set `HINATA_TRUSTED_PROXIES` to the CIDR(s) of your load balancer or proxy, and `X-Forwarded-For` is only honoured from them. If it is empty, Hinata trusts no forwarded header. That is safe, but every client looks like the proxy. See [Reverse proxy & TLS](/en/reverse-proxy.html).

## Authorization

- **Role-gated admin surface.** Every route under **`/api/v1/admin/**` requires the `ADMIN` role**. A normal token can't reach admin functions.
- **Tenant and project visibility.** Team membership decides project visibility across the app: a user only sees projects their team grants (see [Projects & teams](/en/projects-teams.html)).
- **No back door for admins.** The `ADMIN` role only opens the admin area. An admin sees projects, teams, issues, boards, knowledge base pages, search hits and time entries only through their own membership, like everyone else.
- **Organization duties have their own role.** The settings for time tracking, approvals, absences, holidays and billing need the `ORG_ADMIN` role. Everyone else gets a 403 there, admins included. See [Organization](/en/organization.html).
- **Roles you cannot give yourself.** An admin cannot make themselves an organization admin, another admin has to do it. This is a transparency measure, not a hard barrier, because a second admin account would still get around it. That is why every grant is recorded, and that cannot be switched off. The last organization admin cannot be removed, deactivated or deleted. Every organization admin is told when someone joins or leaves the role. The same holds for the moderation role (`MODERATOR`). Whether someone moderates is checked on the stored account, not on the token: a role taken away takes effect at once.
- **No account takeover by admins.** When an admin changes a person's sign-in address, the person gets a message at their old address. For one day after that, no password reset reaches them, neither from the admin area nor from the public "forgot password" page, which quietly sends nothing during that time.
- **A separate audit log.** **Admin area → Audit** only shows platform records: sign-ins, accounts, configuration and integrations. Records about working time, timesheets and absences are in the log on the Organization page. Records about absences are only shown there to whoever keeps absences. Organization admins decide which of these events are recorded. Admins cannot change that, and the platform's master switch does not turn them off. Records about issues and pages appear for admins without their details, so without issue keys and page ids. Changes to the admin and organization admin roles, and any change of a sign-in address by an admin, are always recorded and cannot be switched off.
- **Knowledge base protected by roles.** A page can be read by whoever sees its project, by the Team-Admins of its team, or by members the team opened it to. Pages with neither project nor team are read only by their author. Search only returns what the caller can reach. Only someone with authority over a page's current place can move it somewhere else, and only its author can make it private.
- **Public endpoints are explicit.** Everything that works without a token is listed under [What is reachable without signing in](#what-is-reachable-without-signing-in). Everything else needs a Bearer token.

## What is reachable without signing in

The content of an instance reaches only its members. That is also what keeps an instance legally a hosting service rather than an online platform. Without a token, the server therefore answers only these:

| What for | Routes |
| --- | --- |
| Signing in, joining and getting back in | `POST /api/v1/auth/login`, `/2fa`, `/refresh`, `/register`, `/verify-email`, `/resend-verification`, `/reset/request`, `/reset/accept`, `/invite/accept`, `/sso/exchange`; `GET /api/v1/auth/invite/info`, `/sso/providers`, `/sso/start/{id}` |
| Links from mails and calendar subscriptions, each with its own secret | `GET /api/v1/me/email-change/confirm`, `GET` and `POST /api/v1/me/password-reset/confirm`, `GET /api/v1/me/export.pdf`, `GET /api/v1/shifts/feed/{token}.ics` |
| What the app learns about a server before signing in: name, logo, contact for reports | `GET /api/v1/meta`, `GET /api/v1/meta/logo` |
| The house rules and the form for reports from people without an account (DSA Art. 14 and 16) | `GET /api/v1/public/rules`, `GET` and `POST /api/v1/public/report` |
| Profile pictures for mails and pushes | `GET /api/v1/users/{id}/avatar` |
| The first start of a new server, refused afterwards | `GET /api/v1/setup/status`, `POST /api/v1/setup` |
| Git providers; a webhook counts only with the signature of a connected repository | `GET /api/v1/git/oauth/callback`, `POST /api/v1/git/webhooks/github`, `/gitlab`, `/bitbucket` |
| OAuth for AI clients connecting to `/mcp` | `GET /.well-known/oauth-authorization-server`, `GET /.well-known/oauth-protected-resource` and `…/mcp`, `POST /oauth/register`, `GET /oauth/authorize`, `POST /oauth/token` |
| Hinata Connect checking that the server controls its domain | `GET /.well-known/hinata-connect-challenge` |
| Liveness for the container runtime, status only | `GET /actuator/health` and below |
| The description of the API, off with `HINATA_DOCS_ENABLED=false` | `GET /v3/api-docs`, `/docs`, `/docs/scalar.js`, `/webjars/**` |
| Error responses | `/error` |
| Redirects to and from an identity provider | `/oauth2/authorization/{id}`, `/login/oauth2/code/{id}`, `/saml2/authenticate/{id}`, `/login/saml2/sso/{id}`, `/logout` (only a redirect; a token is no session) |

A test in the server (`UnauthenticatedSurfaceTest`) reads this from the running server on every build: every route of every handler mapping, the filters of every security chain, every servlet and every servlet filter. When a route without sign-in appears, in whatever way, the test fails until somebody has reviewed it and listed it here. What these routes take is bounded, for example the name of a dynamically registered OAuth client to 100 characters and at most ten redirect addresses.

### Reports without an account

The report form at `/api/v1/public/report` is a page of the server, without JavaScript. So that it can be used neither to send spam nor to wear the server down:

- Every form carries a single-use token bound to a hash of the IP address. It counts after 3 seconds at the earliest and 2 hours at the latest, and sending uses it up. A hidden field catches bots.
- Only the same origin may send it (`Sec-Fetch-Site`, else `Origin`), otherwise 403.
- The limits live in the database: 10 reports an hour per address, 3 a day per email address, 100 an hour in all. When a limit is reached, the page shows the instance's contact instead of an error.
- The server never fetches the address given. When it points to content of this instance, the report attaches to exactly that content, and moderation only sees it once a second person releases it. The page never says whether the content exists.
- The receipt repeats nothing of what was entered and names no internal ids.

Behind a reverse proxy the limits per address need `HINATA_TRUSTED_PROXIES`, see [Reverse proxy & TLS](/en/reverse-proxy.html).

## Hardened HTTP responses

- **Security headers** on every response, including **HSTS** (forces HTTPS), a strict **Content-Security-Policy** and **`Referrer-Policy: no-referrer`**.
- **Stable, localized JSON errors with no stack traces.** The server resolves errors from message bundles based on the client's `Accept-Language` and always returns the same shape. Internal paths, class names and stack traces never reach clients.
- **Regex-escaped search input.** Search terms are escaped before they reach the query layer, so a crafted term can't become an injected or expensive regular expression.

## Texts and links

- **Links lead only to the web, to mail or into the app.** When a text is saved, a link in it keeps only targets with `http`, `https` or `mailto` and paths of the app that start with exactly one `/`. Anything else, such as `javascript:`, `data:` or `//foreign.host`, loses its link and keeps its words. That holds for every way into a text, Markdown from MCP and from mail included. A one-time migration did the same for every text stored before.
- **Outside a browser the apps follow only addresses with a scheme.** A relative path means nothing there, and Windows would open it as a path on the disk, `//host` as a network share.
- **The automatic text check** refuses clear violations when a text is saved, on every way in. It runs in the server, without any outside service. See [Admin area](/en/admin-area.html).

## File uploads and object storage

- **Content type and size are validated** on upload, so clients can't slip in disallowed or oversized files (limits are ENV-driven).
- **Randomized S3 object keys.** Stored objects can't be guessed or enumerated by name.
- **Presigned downloads.** Attachments are served through short-lived presigned URLs instead of a public bucket, so access is scoped and time-limited.

## Encryption at rest for integration secrets

Git access tokens and other integration secrets are **encrypted with AES-GCM** before they reach the database, using the key in **`HINATA_GIT_TOKEN_SECRET`**. Secrets are **write-only in the admin API** and never returned. Change the default key in production. Rotating it re-encrypts stored tokens.

## OWASP Top 10 mapping

| OWASP Top 10 (2021) | How Hinata addresses it |
| --- | --- |
| A01 Broken Access Control | `ADMIN`-gated admin routes, `ORG_ADMIN`-gated organization routes, no content rights from platform roles, explicit public allowlist, team and project visibility, tokens revocable per session |
| A02 Cryptographic Failures | JWT HS512, BCrypt 12 passwords, AES-GCM encryption of integration secrets at rest, TLS everywhere (operator) |
| A03 Injection | Regex-escaped search, parameterized Mongo access, uploads validated for content type and size |
| A04 Insecure Design | Refresh tokens rejected for API use, write-only secrets, auth callbacks via deep link, authorization state stored in MongoDB |
| A05 Security Misconfiguration | Hardened headers (HSTS/CSP/no-referrer), API docs UI off by default in prod, trusted proxy allowlist, stable errors without stack traces |
| A06 Vulnerable Components | Actively maintained Spring Boot 4 / Java 21 base. Keep images updated (operator) |
| A07 Identification & Auth Failures | Password minimums, database-backed login lockout, strict `/auth/**` rate limiting, TOTP 2FA, revocable sessions |
| A08 Software & Data Integrity | Git webhooks with verified signatures, a commit ledger that applies each commit only once (see [Git integration](/en/git-integration.html)) |
| A09 Logging & Monitoring | `/actuator/health` for probes. Errors are logged on the server without leaking internals to clients |
| A10 SSRF | Integrations run through the server with fixed provider endpoints instead of client-supplied URLs, and a logo set by URL is fetched only from public addresses on port 80 or 443, with every redirect checked again |

## Hardening checklist for operators

!!! danger "Do these before going live"

    - **Change `HINATA_JWT_SECRET`** to a fresh 64-char secret (`openssl rand -base64 64`).
    - **Change every default password:** `MONGO_ROOT_PASSWORD`, `HINATA_S3_SECRET_KEY`, the `SEAWEEDFS_*` secrets and the TLS keystore and truststore passwords (`HINATA_MONGO_TLS_*_PASSWORD`, default `changeit`).
    - **Change `HINATA_GIT_TOKEN_SECRET`** so integration tokens are encrypted with your own key.

!!! tip "Then tighten the perimeter"

    - **TLS everywhere:** terminate HTTPS at your reverse proxy and use TLS between services. Run MongoDB with X.509 client auth in production (see [MongoDB & X.509](/en/database.html)).
    - **Set `HINATA_TRUSTED_PROXIES`** to your proxy's CIDR so rate limiting and lockout see the real client IP.
    - **Disable the docs UI in prod:** keep `HINATA_DOCS_ENABLED=false` so the Scalar API docs UI is not exposed.
    - **Scope CORS:** set `HINATA_CORS_ALLOWED_ORIGINS` to exactly your web app origin(s), nothing broader.
    - **Don't trust a request because of where it comes from:** when a logo is set by URL, the server downloads it itself. It refuses addresses on its own machine and in private networks, but it reaches every public address on port 80 or 443, including your own reverse proxy and internal services with a public IPv4 or IPv6 address. So put a login in front of every service that lets requests in only because of where they come from, such as your server's IP or your internal network.
    - **Keep images updated:** pull new `ghcr.io/hinata-platform` images regularly for security fixes. See [Backups & upgrades](/en/backups.html).
    - **Keep the server clock in sync** (NTP). Token expiry and SAML SSO depend on it.

## Where to go next

- **[Authentication](/en/authentication.html):** the credential system, 2FA and session revocation.
- **[Single sign-on](/en/sso.html):** hand authentication off to your IdP.
- **[Configuration reference](/en/configuration.html):** every environment variable in one place.
- **[Reverse proxy & TLS](/en/reverse-proxy.html):** trusted proxies and TLS termination.
