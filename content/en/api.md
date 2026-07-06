---
title: API reference
description: Orientation for the Hinata REST API under /api/v1 — the Bearer token auth model, public endpoints, live SSE streams, and the Scalar docs UI.
---

# API reference

Hinata exposes a stable, versioned REST API under **`/api/v1`**. Every feature you
see in the app — projects, issues, boards, sprints, the knowledge base — is driven
by this same surface, so anything the client can do, your own scripts and
integrations can do too. This page is an **orientation**, not an exhaustive dump of
every endpoint: it covers the auth model, the handful of public endpoints, how live
updates stream over SSE, and how to explore the complete surface interactively.

!!! info "This is a map, not the territory"
    The API is large and evolves with the platform. Rather than duplicate every
    route here (and drift out of date), this page teaches you the rules that apply
    everywhere, then points you at the [Scalar docs UI](#exploring-the-full-surface)
    for the full, always-accurate endpoint list.

## Base URL and versioning

All endpoints live under the `/api/v1` prefix on your server's public API host:

```text
https://api.track.example.com/api/v1
```

The `v1` segment is the contract version. Breaking changes would ship under a new
prefix, so you can pin to `v1` safely. In the app this base is what you configure
per server; in your own clients, treat `https://api.track.example.com/api/v1` as the
root and append the paths below.

## Authentication model

Hinata uses **stateless JWTs (HS512)**. There are two kinds of token, and the
distinction matters:

| Token | Lifetime | What it is for |
| --- | --- | --- |
| **Access token** | Short-lived | The Bearer credential you send on every authenticated request. |
| **Refresh token** | Longer-lived | Used **only** to mint a new access token via `/auth/refresh`. |

You authenticate a request by putting the access token in the `Authorization`
header:

```text
Authorization: Bearer <access-token>
```

!!! warning "Refresh tokens are rejected for API access"
    A refresh token can **only** be exchanged for a new access token at
    `/auth/refresh` — it is not accepted as a Bearer credential on any other
    endpoint. If you send a refresh token as `Authorization: Bearer …` to, say,
    `/issues`, the request is rejected. Always call an authenticated endpoint with a
    fresh **access** token.

When an access token expires, exchange your refresh token for a new one rather than
logging in again:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"refreshToken":"<refresh-token>"}'
```

The app does this transparently: its `ApiClient` catches a `401`, calls
`/auth/refresh`, swaps in the new access token and retries the original request
once. See [Authentication](/en/authentication.html) for the full token model.

### Localized errors with Accept-Language

Send an **`Accept-Language`** header (`en` or `de`) and the server localizes error
messages for you — they are resolved server-side from resource bundles keyed by that
header. A German client gets German error text without any translation logic in the
client:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept-Language: de'
```

Errors are stable, machine-readable JSON with a human `message` already in the
requested language, and never include stack traces.

## Public endpoints (no token)

A small set of endpoints is reachable **without** a Bearer token — everything the
app needs before a user has signed in (discovering the server, checking setup
status, logging in). Everything else requires authentication.

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

The everyday flow: `POST /auth/login` to get tokens, then send the returned access
token as a Bearer credential on subsequent calls.

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
    With `jq` you can log in and stash the access token for reuse in a shell:

    ```bash
    TOKEN=$(curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
      -H 'Content-Type: application/json' \
      -d '{"usernameOrEmail":"rebar","password":"your-password"}' \
      | jq -r '.accessToken')

    curl -sS https://api.track.example.com/api/v1/projects \
      -H "Authorization: Bearer $TOKEN"
    ```

If TOTP two-factor is enabled for the account, `/auth/login` returns a 2FA
challenge instead of tokens; complete the challenge to receive them. See
[Authentication](/en/authentication.html).

## Live updates with Server-Sent Events

Some resources push changes to connected clients over **Server-Sent Events (SSE)**
instead of requiring you to poll. The clearest example is **attachments**: when a
file is added to or removed from an issue, every client streaming that issue is
notified immediately at:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

Open the stream with `curl` (the `-N` flag disables buffering so events print as
they arrive):

```bash
curl -N https://api.track.example.com/api/v1/issues/ASTA-42/attachments/stream \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept: text/event-stream'
```

The connection stays open and emits an event each time the issue's attachments
change. SSE is a one-way, long-lived HTTP stream — no WebSocket upgrade required.

!!! warning "Disable proxy buffering for SSE"
    A reverse proxy that buffers responses will hold SSE events back until the
    connection closes, which looks like "live updates don't work." Turn buffering
    off for the stream path (for example `proxy_buffering off;` on nginx). See
    [Reverse proxy & TLS](/en/reverse-proxy.html) and the
    [FAQ](/en/faq.html).

## Rate limiting

The API is rate-limited **per client IP** using bucket4j, with a strict budget on
authentication routes to blunt brute-force attempts:

| Scope | Default limit | Environment variable |
| --- | --- | --- |
| General API | **300** requests/minute | `HINATA_RATE_LIMIT_API` |
| `/auth/**` | **10** requests/minute | `HINATA_RATE_LIMIT_AUTH` |

Rate limiting is toggled by `HINATA_RATE_LIMIT_ENABLED` (on by default). Repeated
failed logins additionally trigger a **database-backed lockout**
(`HINATA_MAX_LOGIN_FAILURES`, default 5; `HINATA_LOGIN_BLOCK_MINUTES`, default 15)
that survives restarts.

!!! tip "Behind a reverse proxy, set trusted proxies"
    Rate limiting keys on the client IP. If your server sits behind a proxy and you
    have not set `HINATA_TRUSTED_PROXIES` to the proxy's CIDR, every request appears
    to come from the proxy and shares one bucket. See
    [Reverse proxy & TLS](/en/reverse-proxy.html).

## Exploring the full surface

The complete, always-accurate endpoint list is served by an interactive **Scalar
API-docs UI**, gated by the `HINATA_DOCS_ENABLED` flag. It is **off by default in
production** so you never leak your full API surface to the public — but it is the
best way to browse every route, schema and parameter while developing.

Enable it locally by setting the flag before you start the server:

```bash
HINATA_DOCS_ENABLED=true ./gradlew bootRun
```

Or in a `.env` / compose environment:

```properties
HINATA_DOCS_ENABLED=true
```

Then open the docs UI in your browser at your server's base URL. Because it exposes
the whole surface, **leave `HINATA_DOCS_ENABLED=false` in production** and use it
only on a dev instance.

!!! danger "Do not expose the docs UI in production"
    The Scalar UI describes every endpoint and schema. Keep it disabled on
    internet-facing deployments; enable it only on trusted, local dev servers.

## Where to go next

- [Authentication](/en/authentication.html) — the full token lifecycle, 2FA and SSO login.
- [Single sign-on (SSO)](/en/sso.html) — OIDC / OAuth2 / SAML / LDAP and `/auth/sso/providers`.
- [Git integration](/en/git-integration.html) — OAuth flow and signed webhook endpoints.
- [Development](/en/development.html) — run the server from source to explore the API with the docs UI.
