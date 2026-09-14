---
title: API reference
description: Getting started with the Hinata REST API under /api/v1, with Bearer tokens, public endpoints, SSE streams and the Scalar docs UI.
---

# API reference

Hinata exposes a stable, versioned REST API under **`/api/v1`**. The app uses this
same API for everything, from projects and issues to boards, sprints and the
knowledge base. So your own scripts and integrations can do anything the client can.

This page is an **orientation**. It covers the rules that apply everywhere. The
full, always current endpoint list is in the
[Scalar docs UI](#exploring-the-full-surface).

## Base URL and versioning

All endpoints live under the `/api/v1` prefix on your server's public API host:

```text
https://api.track.example.com/api/v1
```

`v1` is the contract version. Breaking changes would ship under a new prefix, so you
can pin to `v1` safely. In the app you configure this base per server. In your own
clients, append the paths below to `https://api.track.example.com/api/v1`.

## Authentication model

Hinata uses **stateless JWTs (HS512)** with two kinds of token:

| Token | Lifetime | What it is for |
| --- | --- | --- |
| **Access token** | Short-lived | The Bearer credential you send on every authenticated request. |
| **Refresh token** | Longer-lived | Used **only** to mint a new access token via `/auth/refresh`. |

Put the access token in the `Authorization` header:

```text
Authorization: Bearer <access-token>
```

!!! warning "Refresh tokens are rejected for API access"
    A refresh token can **only** be exchanged for a new access token at
    `/auth/refresh`. No other endpoint accepts it as a Bearer credential. Send it as
    `Authorization: Bearer …` to, say, `/issues` and the request is rejected. Always
    call authenticated endpoints with a fresh **access** token.

When an access token expires, exchange your refresh token for a new one instead of
logging in again:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"refreshToken":"<refresh-token>"}'
```

The app does this automatically. Its `ApiClient` catches a `401`, calls
`/auth/refresh`, swaps in the new access token and retries the original request
once. See [Authentication](/en/authentication.html) for the full token model.

### Localized errors with Accept-Language

Send an **`Accept-Language`** header (`en` or `de`) and you get error messages in
that language. The server resolves them from resource bundles, so the client needs
no translation logic:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept-Language: de'
```

Errors are stable, machine-readable JSON with a human `message` already in the
requested language. They never include stack traces.

## Public endpoints (no token)

These endpoints work **without** a Bearer token. The app needs them before anyone
has signed in: to discover the server, check setup status and log in.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/meta` | Server metadata: minimum app version, privacy URL, auth feature flags. |
| `GET` | `/setup/status` | Whether first-run setup has been completed. |
| `POST` | `/setup` | Complete first-run setup (organization + first admin). |
| `POST` | `/auth/login` | Exchange credentials for access + refresh tokens. |
| `POST` | `/auth/refresh` | Exchange a refresh token for a new access token. |
| `GET` | `/auth/sso/providers` | List the configured SSO providers (OIDC, OAuth2, SAML, LDAP). |
| `GET` | `/actuator/health` | Liveness/health probe for load balancers and uptime checks. |

!!! note "Everything else needs a Bearer token"
    Any path not in the table above requires a valid **access** token. Admin routes
    under `/api/v1/admin/**` additionally require the `ADMIN` role.

## Log in, then call the API

The everyday flow: `POST /auth/login` to get tokens, then send the access token as a
Bearer credential on every following call.

**1. Log in** and receive an access token and a refresh token:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -H 'Accept-Language: en' \
  -d '{"usernameOrEmail":"rebar","password":"your-password"}'
```

The response contains the tokens (field names may include `accessToken` and
`refreshToken`) plus the signed-in user. Copy the **access token**.

**2. Call an authenticated endpoint** with that token as a Bearer credential:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>'
```

!!! tip "Capture the token in one step"
    With `jq` you can log in and keep the access token in a shell variable:

    ```bash
    TOKEN=$(curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
      -H 'Content-Type: application/json' \
      -d '{"usernameOrEmail":"rebar","password":"your-password"}' \
      | jq -r '.accessToken')

    curl -sS https://api.track.example.com/api/v1/projects \
      -H "Authorization: Bearer $TOKEN"
    ```

If TOTP two-factor is enabled for the account, `/auth/login` returns a 2FA challenge
instead of tokens. Complete the challenge to receive them. See
[Authentication](/en/authentication.html).

## Live updates with Server-Sent Events

Some resources push changes to connected clients over **Server-Sent Events (SSE)**,
so you don't have to poll. **Attachments** are the clearest example: when a file is
added to or removed from an issue, every client streaming that issue is notified
immediately at:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

Open the stream with `curl`. The `-N` flag disables buffering so events print as
they arrive:

```bash
curl -N https://api.track.example.com/api/v1/issues/ASTA-42/attachments/stream \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept: text/event-stream'
```

The connection stays open and emits an event each time the issue's attachments
change. SSE is a one-way, long-lived HTTP stream with no WebSocket upgrade.

!!! warning "Disable proxy buffering for SSE"
    A reverse proxy that buffers responses holds SSE events back until the
    connection closes, which looks like "live updates don't work." Turn buffering
    off for the stream path (for example `proxy_buffering off;` on nginx). See
    [Reverse proxy & TLS](/en/reverse-proxy.html) and the
    [FAQ](/en/faq.html).

## Rate limiting

The API is rate-limited **per client IP** with bucket4j. Authentication routes get a
strict budget against brute force:

| Scope | Default limit | Environment variable |
| --- | --- | --- |
| General API | **300** requests/minute | `HINATA_RATE_LIMIT_API` |
| `/auth/**` | **10** requests/minute | `HINATA_RATE_LIMIT_AUTH` |

`GET /auth/sso/providers` is the one exception and counts against the general
budget. The sign-in screen calls it on every visit to decide which SSO buttons to
draw, and it exposes nothing an attacker could guess at.

`HINATA_RATE_LIMIT_ENABLED` toggles rate limiting (on by default). Repeated failed
logins also trigger a **database-backed lockout** that survives restarts:

- `HINATA_MAX_LOGIN_FAILURES`, default 5
- `HINATA_LOGIN_BLOCK_MINUTES`, default 15

!!! tip "Behind a reverse proxy, set trusted proxies"
    Rate limiting keys on the client IP. If your server sits behind a proxy and
    `HINATA_TRUSTED_PROXIES` is not set to the proxy's CIDR, every request appears
    to come from the proxy and shares one bucket. See
    [Reverse proxy & TLS](/en/reverse-proxy.html).

## Exploring the full surface

The complete, always current endpoint list is served by an interactive **Scalar
API docs UI**, gated by the `HINATA_DOCS_ENABLED` flag. It is **off by default in
production**, so your API surface is not published to everyone. While developing, it
is the best way to browse every route, schema and parameter.

Enable it locally before you start the server:

```bash
HINATA_DOCS_ENABLED=true ./gradlew bootRun
```

Or in a `.env` / compose environment:

```properties
HINATA_DOCS_ENABLED=true
```

Then open the docs UI in your browser at your server's base URL.

!!! danger "Do not expose the docs UI in production"
    The Scalar UI describes every endpoint and schema. Leave
    `HINATA_DOCS_ENABLED=false` on internet-facing deployments. Enable it only on
    trusted, local dev servers.

## Where to go next

- [Authentication](/en/authentication.html): the full token lifecycle, 2FA and SSO login.
- [Single sign-on (SSO)](/en/sso.html): OIDC / OAuth2 / SAML / LDAP and `/auth/sso/providers`.
- [Git integration](/en/git-integration.html): OAuth flow and signed webhook endpoints.
- [Development](/en/development.html): run the server from source to explore the API with the docs UI.
