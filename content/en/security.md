---
title: Security model
description: Hinata's hardening story mapped to the OWASP Top 10 — JWT design, BCrypt, login lockout, rate limiting, hardened headers, safe uploads and encryption at rest.
---

# Security model

Hinata is built to be exposed to the public internet. This page documents the platform's hardening — the concrete controls, the environment variables that tune them, and an **operator checklist** for a safe production deployment. Everything below is mapped to the **OWASP Top 10** so you can reason about coverage.

For the user-facing side of authentication (registration, 2FA, sessions) see [Authentication](/en/authentication.html), and for federated login see [Single sign-on](/en/sso.html).

## Tokens and passwords

- **Stateless JWT, HS512.** Access tokens are short-lived; a separate **refresh token** mints new access tokens. Crucially, a **refresh token is rejected for normal API access** — it is accepted only at the refresh endpoint. A stolen access token expires quickly; a stolen refresh token cannot be used to read data.
- **Revocable sessions.** Each token carries a session id (`sid`) tied to a record in the `sessions` collection, so individual sessions can be revoked without rotating the signing secret. See [Authentication → Sessions](/en/authentication.html).
- **BCrypt strength 12** for password hashing, with a **10-character minimum** password length. Length plus a deliberately slow hash is the core defence against credential brute force.

!!! danger "Change the JWT secret before you expose the server"
    `HINATA_JWT_SECRET` is the HS512 signing key and must be a real secret of **at least 64 characters** in production. Generate one with:
    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```
    Anyone who knows this secret can forge tokens for any user. Never ship the default.

## Login lockout and rate limiting

Two independent layers protect the credential and API surface.

**Database-backed login blocking** counts failed logins and locks the account/identifier after a threshold. Because the counter lives in MongoDB, the block **survives restarts** and works across multiple server instances.

| Variable | Default | Purpose |
| --- | --- | --- |
| `HINATA_MAX_LOGIN_FAILURES` | `5` | Failed attempts before the identifier is blocked |
| `HINATA_LOGIN_BLOCK_MINUTES` | `15` | How long the block lasts |

**Per-IP rate limiting** (via **bucket4j**) caps request volume per client IP, with a **stricter budget on `/auth/**`** to blunt password spraying and enumeration.

| Variable | Default | Purpose |
| --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | `true` | Master switch for rate limiting |
| `HINATA_RATE_LIMIT_API` | `300` | Requests per minute for general API |
| `HINATA_RATE_LIMIT_AUTH` | `10` | Requests per minute for `/auth/**` (strict) |

!!! warning "Rate limiting needs the real client IP"
    Behind a reverse proxy every request appears to come from the proxy unless you tell Hinata which proxies to trust. Set `HINATA_TRUSTED_PROXIES` to the CIDR(s) of your load balancer/proxy so `X-Forwarded-For` is honoured only from them. Leave it empty and Hinata trusts no forwarded header — safe, but every client looks like the proxy. See [Reverse proxy & TLS](/en/reverse-proxy.html).

## Authorization

- **Role-gated admin surface.** Every route under **`/api/v1/admin/**` requires the `ADMIN` role**; a normal token cannot reach admin functions.
- **Tenant/project visibility.** Team membership gates project visibility app-wide — a user only sees projects their team grants (see [Projects & teams](/en/projects-teams.html)).
- **Public endpoints are explicit.** Only a small allowlist is reachable without a token: `/meta`, `/setup/status`, `/setup`, `/auth/login`, `/auth/refresh`, `/auth/sso/providers`, `/actuator/health`. Everything else demands a Bearer token.

## Hardened HTTP responses

- **Security headers** on every response: **HSTS** (force HTTPS), a restrictive **Content-Security-Policy**, and **`Referrer-Policy: no-referrer`**, among others.
- **Stable, localized JSON errors with no stack traces.** Errors are resolved server-side from message bundles by the client's `Accept-Language` and returned in a consistent shape — no internal paths, class names or stack traces leak to clients.
- **Regex-escaped search input.** User-supplied search terms are escaped before they reach the query layer, so a crafted term cannot become an injected/expensive regular expression.

## File uploads and object storage

- **Content-type and size validated** on upload, so clients cannot smuggle disallowed or oversized files (limits are ENV-driven).
- **Randomized S3 object keys**, so stored objects are not guessable or enumerable by name.
- **Presigned downloads** — attachments are served through short-lived presigned URLs rather than a public bucket, so access is scoped and time-boxed.

## Encryption at rest for integration secrets

Git access tokens and other integration secrets are **encrypted with AES-GCM** before they touch the database, using the key in **`HINATA_GIT_TOKEN_SECRET`**. Secrets are **write-only in the admin API** — you can set them, but they are never returned. Change the default key in production; rotating it re-keys stored tokens.

## OWASP Top 10 mapping

| OWASP Top 10 (2021) | How Hinata addresses it |
| --- | --- |
| A01 Broken Access Control | `ADMIN`-gated admin routes, explicit public allowlist, team/project visibility gating, per-session revocable tokens |
| A02 Cryptographic Failures | JWT HS512, BCrypt-12 passwords, AES-GCM encryption of integration secrets at rest, TLS everywhere (operator) |
| A03 Injection | Regex-escaped search, parameterized Mongo access, content-type/size-validated uploads |
| A04 Insecure Design | Refresh tokens rejected for API use, write-only secrets, deep-link auth callbacks, Mongo-stored authorization state |
| A05 Security Misconfiguration | Hardened headers (HSTS/CSP/no-referrer), API-docs UI off by default in prod, trusted-proxy allowlist, stable errors without stack traces |
| A06 Vulnerable Components | Actively maintained Spring Boot 4 / Java 21 base; keep images updated (operator) |
| A07 Identification & Auth Failures | Password minimums, DB-backed login lockout, strict `/auth/**` rate limiting, TOTP 2FA, revocable sessions |
| A08 Software & Data Integrity | Signature-verified Git webhooks, single-apply commit ledger (see [Git integration](/en/git-integration.html)) |
| A09 Logging & Monitoring | `/actuator/health` for probes; errors logged server-side without leaking internals to clients |
| A10 SSRF | Server-brokered integrations with fixed provider endpoints rather than client-supplied URLs |

## Hardening checklist for operators

!!! danger "Do these before going live"
    - **Change `HINATA_JWT_SECRET`** to a fresh 64-char secret (`openssl rand -base64 64`).
    - **Change every default password** — `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD`, and the TLS keystore/truststore passwords (`HINATA_MONGO_TLS_*_PASSWORD`, default `changeit`).
    - **Change `HINATA_GIT_TOKEN_SECRET`** so integration tokens are encrypted with your own key.

!!! tip "Then tighten the perimeter"
    - **TLS everywhere** — terminate HTTPS at your reverse proxy and use TLS between services; run MongoDB with X.509 client auth in production (see [MongoDB & X.509](/en/database.html)).
    - **Set `HINATA_TRUSTED_PROXIES`** to your proxy's CIDR so rate limiting and lockout see the real client IP.
    - **Disable the docs UI in prod** — keep `HINATA_DOCS_ENABLED=false` so the Scalar API-docs UI is not exposed.
    - **Scope CORS** — set `HINATA_CORS_ALLOWED_ORIGINS` to exactly your web app origin(s), nothing broader.
    - **Keep images updated** — pull new `ghcr.io/hinata-platform` images regularly for security fixes; see [Backups & upgrades](/en/backups.html).
    - **Keep the server clock in sync** (NTP) — required for correct token expiry and SAML SSO.

## Where to go next

- **[Authentication](/en/authentication.html)** — the credential system, 2FA and session revocation.
- **[Single sign-on](/en/sso.html)** — delegate authentication to your IdP.
- **[Configuration reference](/en/configuration.html)** — every environment variable in one place.
- **[Reverse proxy & TLS](/en/reverse-proxy.html)** — trusted proxies and TLS termination.
