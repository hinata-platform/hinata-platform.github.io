---
title: Architecture
description: How Hinata fits together — Flutter app, dio ApiClient, REST /api/v1, Spring Boot, MongoDB replica set, S3/MinIO, SMTP, SSE and the Connect gateway.
---

# Architecture

Hinata is two deployable units — a Flutter client and a Spring Boot server — talking over a versioned REST API, backed by MongoDB and S3-compatible storage. This page explains how the pieces fit, how a request flows, and where runtime configuration lives.

## The components

At a glance, from client to storage:

```text
┌──────────────────────────────────────────────────────────────┐
│  Client — hinata-app (Flutter)                                │
│  Android · iOS · Web · macOS · one codebase                   │
│                                                                │
│   UI (bloc/cubit, go_router)                                  │
│        │                                                       │
│   ApiClient (dio)                                             │
│    · attaches Bearer access token                             │
│    · sends Accept-Language (en / de)                          │
│    · auto-refreshes on 401, retries once                      │
└───────────────┬────────────────────────────────┬─────────────┘
                │ HTTPS  REST /api/v1             │ SSE (live)
                ▼                                 ▼
┌──────────────────────────────────────────────────────────────┐
│  Server — hinata-server (Spring Boot 4, Java 21)              │
│                                                                │
│   Controllers → Services → Repositories                       │
│   JWT auth · rate limiting · localized errors                 │
│   Runtime settings loaded from MongoDB (override env)         │
└───┬────────────────┬───────────────────┬──────────────┬───────┘
    │                │                   │              │
    ▼                ▼                   ▼              ▼
┌────────┐    ┌────────────┐      ┌────────────┐  ┌──────────┐
│MongoDB │    │  S3/MinIO  │      │    SMTP    │  │  Hinata  │
│replica │    │attachments │      │  outbound  │  │ Connect  │
│  set   │    │ presigned  │      │   e-mail   │  │ gateway  │
└────────┘    └────────────┘      └────────────┘  └──────────┘
```

- **App (Flutter)** — a single codebase for Android, iOS, Web and macOS. State is managed with bloc/cubit, routing with go_router, localization with i18next (English + German), and networking through **dio** inside an `ApiClient`. Charts are drawn with fl_chart.
- **Server (Spring Boot 4, Java 21)** — exposes the REST API under `/api/v1`, holds all business logic and authorization, and streams live updates.
- **MongoDB** — the system of record. Production runs a **replica set** (2 data nodes + 1 arbiter) with TLS and X.509 client authentication.
- **S3 / MinIO** — object storage for attachments and avatars, with randomized object keys and presigned downloads.
- **SMTP** — outbound mail (verification, notifications, password reset). Mailpit stands in during development.
- **Hinata Connect gateway** — a central push-relay and universal-link relay so a single published white-label app can serve many servers.

## The app → server path

Every network call from the app goes through a single `ApiClient` built on **dio**. That client is where cross-cutting concerns live, so individual screens never think about tokens or headers:

- It attaches the current **Bearer access token** to authenticated requests.
- It sends an **`Accept-Language`** header (`en` or `de`) so the server can localize error messages.
- On a `401`, it transparently calls the refresh endpoint, swaps in a fresh access token and **retries the original request once**. If refresh fails, it clears the session and routes to login.

The server exposes a stable, versioned surface at **`/api/v1`**. See the [API reference](/en/api.html) for the full endpoint list.

!!! info "Multi-server by design"
    The native app never bakes in a server URL. Users save one or more servers and switch between them, and access tokens are scoped **per server**. The web build may default to its own origin. This is what makes the same published app usable against any Hinata server — see [White-label & branding](/en/white-label.html).

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

This indirection is what lets one published, white-label app serve an unlimited number of independent Hinata servers. See [Hinata Connect gateway](/en/connect-gateway.html) for the full design.

## Where to go next

- [Core concepts](/en/concepts.html) — the vocabulary the API and UI are built on.
- [Self-hosting overview](/en/self-hosting.html) — how these components map onto containers you deploy.
- [Security model](/en/security.html) — the guarantees behind the request path above.
