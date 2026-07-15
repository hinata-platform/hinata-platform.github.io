---
title: Architecture
description: How Hinata fits together — Flutter app, dio ApiClient, REST /api/v1, Spring Boot, MongoDB replica set, S3/MinIO, SMTP, SSE and the Connect gateway.
---

# Architecture

Hinata is two deployable units — a Flutter client and a Spring Boot server — talking over a versioned REST API, backed by MongoDB and S3-compatible storage. This page explains how the pieces fit, how a request flows, and where runtime configuration lives.

## The components

At a glance, from client to storage:

<div class="arch" role="img" aria-label="Architecture: the Flutter app talks to the Spring Boot server over REST and SSE; the server is backed by MongoDB, S3/MinIO, SMTP and the Hinata Connect gateway."><div class="arch-node glass"><div class="arch-node-top"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg></span><span class="arch-txt"><strong>Client — hinata-app</strong><em>Flutter · one codebase</em></span><span class="arch-tag">Android · iOS · Web · macOS</span></div><div class="arch-sub"><span class="arch-pill">UI · bloc/cubit · go_router</span><span class="arch-pill">ApiClient · dio · Bearer token · Accept-Language · auto-refresh</span></div></div><div class="arch-link"><span class="arch-vline"></span><span class="arch-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span><span class="arch-link-labels"><span>HTTPS · REST <code>/api/v1</code></span><span>SSE · live updates</span></span></div><div class="arch-node glass"><div class="arch-node-top"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="8" x="2" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/></svg></span><span class="arch-txt"><strong>Server — hinata-server</strong><em>Spring Boot 4 · Java 21</em></span></div><div class="arch-sub"><span class="arch-pill">Controllers → Services → Repositories</span><span class="arch-pill">JWT auth · rate limiting · localized errors</span><span class="arch-pill">Runtime settings from MongoDB (override env)</span></div></div><div class="arch-link"><span class="arch-vline"></span><span class="arch-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span></div><div class="arch-stores"><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg></span><strong>MongoDB</strong><em>Replica set · X.509</em></div><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg></span><strong>S3 / MinIO</strong><em>Attachments · presigned</em></div><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg></span><strong>SMTP</strong><em>Outbound e-mail</em></div><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/><path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/><circle cx="12" cy="12" r="2"/><path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/><path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"/></svg></span><strong>Connect</strong><em>Push · universal links</em></div></div></div>

- **App (Flutter)** — a single codebase for Android, iOS, Web and macOS. State is managed with bloc/cubit, routing with go_router, localization with i18next (English + German), and networking through **dio** inside an `ApiClient`. Charts are drawn with fl_chart.
- **Server (Spring Boot 4, Java 21)** — exposes the REST API under `/api/v1`, holds all business logic and authorization, and streams live updates.
- **MongoDB** — the system of record. Production runs a **replica set** (2 data nodes + 1 arbiter) with TLS and X.509 client authentication.
- **S3 / MinIO** — object storage for attachments and avatars, with randomized object keys and presigned downloads.
- **SMTP** — outbound mail (verification, notifications, password reset). Mailpit stands in during development.
- **Hinata Connect gateway** — a central push-relay and universal-link relay so the single published app can serve many self-hosted servers.

## The app → server path

Every network call from the app goes through a single `ApiClient` built on **dio**. That client is where cross-cutting concerns live, so individual screens never think about tokens or headers:

- It attaches the current **Bearer access token** to authenticated requests.
- It sends an **`Accept-Language`** header (`en` or `de`) so the server can localize error messages.
- On a `401`, it transparently calls the refresh endpoint, swaps in a fresh access token and **retries the original request once**. If refresh fails, it clears the session and routes to login.

The server exposes a stable, versioned surface at **`/api/v1`**. See the [API reference](/en/api.html) for the full endpoint list.

!!! info "Multi-server by design"
    The native app never bakes in a server URL. Users save one or more servers and switch between them, and access tokens are scoped **per server**. The web build may default to its own origin. This is what makes the same published app usable against any Hinata server — see [Branding & custom clients](/en/self-hosted-app.html).

## Live updates with SSE

Instead of polling, the server pushes changes to connected clients over **Server-Sent Events (SSE)**. The clearest example is attachments: when a file is added to or removed from an issue, every open client streaming that issue receives the change immediately at:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

SSE is a one-way, long-lived HTTP stream, which keeps live sync cheap and proxy-friendly — no WebSocket upgrade required. Make sure your [reverse proxy](/en/reverse-proxy.html) does not buffer these responses.

## Request lifecycle & token refresh

A typical authenticated request:

1. **App** issues a request through `ApiClient`; dio attaches the Bearer access token and `Accept-Language`.
2. **Server** authenticates the JWT (HS512), enforces per-IP rate limits, and checks authorization (for example, `/api/v1/admin/**` requires the `ADMIN` role).
3. **Controller → Service → Repository** — the service layer applies business rules and reads/writes MongoDB; attachment bytes go to S3/MinIO.
4. **Response** is a stable, localized JSON body — success payload, or an error resolved from `messages.properties` in the client's language, without stack traces.

Access tokens are deliberately **short-lived**; refresh tokens are longer-lived but are **rejected for API access** — they can only mint new access tokens. When an access token expires mid-session, the refresh dance is invisible to the user:

```text
App ──GET /issues (expired access token)──▶ Server
App ◀──────────── 401 Unauthorized ────────── Server
App ──POST /auth/refresh (refresh token)──▶ Server
App ◀──────── new access token ───────────── Server
App ──GET /issues (retried, new token)────▶ Server
App ◀──────────────── 200 OK ─────────────── Server
```

See [Authentication](/en/authentication.html) for the full token model.

## Runtime settings in MongoDB

A defining trait of Hinata: most operational configuration is **stored in MongoDB and managed from the app's Admin area**, not frozen into environment variables at boot. This covers SSO providers, e-mail ingest (IMAP), push, Git OAuth apps and app-level settings like the minimum client version.

Two rules follow from this:

- **The database overrides the environment.** Environment variables such as `hinata.app.*` are defaults; a value set in the Admin area wins.
- **Changes apply without a restart.** Update an SSO provider or a feature flag and it takes effect on the next request — no redeploy, no container restart.

!!! tip "Secrets are write-only"
    In the admin API, secrets (OAuth client secrets, tokens, passwords) are **write-only** — you can set them, but they are never echoed back. Stored Git access tokens are additionally AES-GCM-encrypted at rest.

This is why bootstrapping only needs a handful of environment variables (see [Configuration reference](/en/configuration.html)); everything else is configured live once the server is up.

## Localized errors

Error messages are resolved **server-side** from resource bundles — `messages.properties` (English, the default) and `messages_de.properties` (German) — keyed by the client's `Accept-Language` header. The app sends the user's language, and the server returns a stable, machine-readable error whose human message is already in the right language. No translation logic lives in the client.

## The Connect gateway

Push notifications and universal links are relayed through the **Hinata Connect gateway** rather than baked into each server:

- The server **registers itself with the gateway on boot**.
- Per-server Firebase/FCM credentials live in the gateway, not in each server, so **self-hosters need no Firebase project**.
- The app handles universal links of the form `/l/<code>` via the gateway.
- Override the gateway with `HINATA_GATEWAY_BASE_URL` to run your own.

This indirection is what lets the one published app serve an unlimited number of independent, self-hosted Hinata servers. See [Hinata Connect gateway](/en/connect-gateway.html) for the full design.

## Where to go next

- [Core concepts](/en/concepts.html) — the vocabulary the API and UI are built on.
- [Self-hosting overview](/en/self-hosting.html) — how these components map onto containers you deploy.
- [Security model](/en/security.html) — the guarantees behind the request path above.
