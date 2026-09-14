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
- **Public endpoints are explicit.** Only this short allowlist works without a token: `/meta`, `/setup/status`, `/setup`, `/auth/login`, `/auth/refresh`, `/auth/sso/providers`, `/actuator/health`. Everything else needs a Bearer token.

## Hardened HTTP responses

- **Security headers** on every response, including **HSTS** (forces HTTPS), a strict **Content-Security-Policy** and **`Referrer-Policy: no-referrer`**.
- **Stable, localized JSON errors with no stack traces.** The server resolves errors from message bundles based on the client's `Accept-Language` and always returns the same shape. Internal paths, class names and stack traces never reach clients.
- **Regex-escaped search input.** Search terms are escaped before they reach the query layer, so a crafted term can't become an injected or expensive regular expression.

## File uploads and object storage

- **Content type and size are validated** on upload, so clients can't slip in disallowed or oversized files (limits are ENV-driven).
- **Randomized S3 object keys.** Stored objects can't be guessed or enumerated by name.
- **Presigned downloads.** Attachments are served through short-lived presigned URLs instead of a public bucket, so access is scoped and time-limited.

## Encryption at rest for integration secrets

Git access tokens and other integration secrets are **encrypted with AES-GCM** before they reach the database, using the key in **`HINATA_GIT_TOKEN_SECRET`**. Secrets are **write-only in the admin API** and never returned. Change the default key in production. Rotating it re-encrypts stored tokens.

## OWASP Top 10 mapping

| OWASP Top 10 (2021) | How Hinata addresses it |
| --- | --- |
| A01 Broken Access Control | `ADMIN`-gated admin routes, explicit public allowlist, team and project visibility, tokens revocable per session |
| A02 Cryptographic Failures | JWT HS512, BCrypt 12 passwords, AES-GCM encryption of integration secrets at rest, TLS everywhere (operator) |
| A03 Injection | Regex-escaped search, parameterized Mongo access, uploads validated for content type and size |
| A04 Insecure Design | Refresh tokens rejected for API use, write-only secrets, auth callbacks via deep link, authorization state stored in MongoDB |
| A05 Security Misconfiguration | Hardened headers (HSTS/CSP/no-referrer), API docs UI off by default in prod, trusted proxy allowlist, stable errors without stack traces |
| A06 Vulnerable Components | Actively maintained Spring Boot 4 / Java 21 base. Keep images updated (operator) |
| A07 Identification & Auth Failures | Password minimums, database-backed login lockout, strict `/auth/**` rate limiting, TOTP 2FA, revocable sessions |
| A08 Software & Data Integrity | Git webhooks with verified signatures, a commit ledger that applies each commit only once (see [Git integration](/en/git-integration.html)) |
| A09 Logging & Monitoring | `/actuator/health` for probes. Errors are logged on the server without leaking internals to clients |
| A10 SSRF | Integrations run through the server with fixed provider endpoints instead of client-supplied URLs |

## Hardening checklist for operators

!!! danger "Do these before going live"

    - **Change `HINATA_JWT_SECRET`** to a fresh 64-char secret (`openssl rand -base64 64`).
    - **Change every default password:** `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` and the TLS keystore and truststore passwords (`HINATA_MONGO_TLS_*_PASSWORD`, default `changeit`).
    - **Change `HINATA_GIT_TOKEN_SECRET`** so integration tokens are encrypted with your own key.

!!! tip "Then tighten the perimeter"

    - **TLS everywhere:** terminate HTTPS at your reverse proxy and use TLS between services. Run MongoDB with X.509 client auth in production (see [MongoDB & X.509](/en/database.html)).
    - **Set `HINATA_TRUSTED_PROXIES`** to your proxy's CIDR so rate limiting and lockout see the real client IP.
    - **Disable the docs UI in prod:** keep `HINATA_DOCS_ENABLED=false` so the Scalar API docs UI is not exposed.
    - **Scope CORS:** set `HINATA_CORS_ALLOWED_ORIGINS` to exactly your web app origin(s), nothing broader.
    - **Keep images updated:** pull new `ghcr.io/hinata-platform` images regularly for security fixes. See [Backups & upgrades](/en/backups.html).
    - **Keep the server clock in sync** (NTP). Token expiry and SAML SSO depend on it.

## Where to go next

- **[Authentication](/en/authentication.html):** the credential system, 2FA and session revocation.
- **[Single sign-on](/en/sso.html):** hand authentication off to your IdP.
- **[Configuration reference](/en/configuration.html):** every environment variable in one place.
- **[Reverse proxy & TLS](/en/reverse-proxy.html):** trusted proxies and TLS termination.
