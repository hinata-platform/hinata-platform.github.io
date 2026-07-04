---
title: FAQ & troubleshooting
description: Answers to common questions about Hinata — cost, Firebase, branding, databases, SSO — plus a troubleshooting table with concrete fixes for the usual problems.
---

# FAQ & troubleshooting

The questions self-hosters ask most, and a troubleshooting table for the problems
that actually come up in practice — each with the concrete setting or command that
fixes it. If your issue is not here, the per-subsystem pages linked throughout go
deeper.

## Frequently asked questions

### Is Hinata really free, with no limits?

Yes. Hinata is **open source under the GPL-3.0 license**, and there are **no user,
team or board limits — ever**. You run it on your own infrastructure and add as many
people, projects, teams and boards as you like. There is no paid tier, no seat count
and no feature gate; the whole platform is the code in the two repositories.

### Do I need Firebase for push notifications?

**No.** Mobile push and universal (deep) links are relayed through the central
[Hinata Connect gateway](/en/connect-gateway.html). Your server registers itself with
the gateway on boot, and the published app's push credentials live in the gateway —
not in your deployment. Self-hosters configure **nothing** for push. (You only touch
Firebase if you build and ship your **own** white-label app with its own store
presence and run your own gateway.)

### Can I use my own domain and branding?

**Yes — Hinata is white-label by design.** You already serve everything under your
own domain (`track.example.com` for the web app, `api.track.example.com` for the
API). Beyond that you can build your own branded client: your own package id, app
name, icons and splash, accent color, pointed at the gateway. See
[White-label & branding](/en/white-label.html). Native apps never bake in a server
URL — users save and switch between servers — so one branded app can serve many
instances.

### Which databases and storage does Hinata use?

- **MongoDB** is the system of record. Production runs a **replica set** (2 data
  nodes + 1 arbiter) with TLS and X.509 client authentication — see
  [MongoDB & X.509](/en/database.html).
- **S3-compatible object storage** holds attachments and avatars, with randomized
  object keys and presigned downloads. The stack ships **MinIO**, but any
  S3-compatible store works — see [Object storage](/en/storage.html).

There is no separate SQL database and no message broker; live updates use SSE.

### Does SSO work with my identity provider?

Very likely. Hinata supports **OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP**,
configured at runtime in the Admin area (stored in MongoDB, no restart). That covers
the common providers — Keycloak, Authentik, Azure AD, Google, Synology SSO and
anything speaking those protocols. See [Single sign-on (SSO)](/en/sso.html).

### Do configuration changes need a restart?

Most don't. Runtime settings (SSO, e-mail ingest, push, Git OAuth apps, app-level
settings) are **stored in MongoDB and managed from the Admin area**, and **the
database overrides the environment**. Changes apply on the next request. Only the
bootstrap environment variables (like `HINATA_JWT_SECRET`) require a redeploy. See
[Architecture → Runtime settings](/en/architecture.html).

## Troubleshooting

Each row names the symptom, its usual cause, and the concrete fix.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| **App won't connect to the server** | Wrong base URL, blocked CORS, or a TLS problem | Verify `HINATA_BASE_URL` is the public API URL and reachable over HTTPS; add the web app's origin to `HINATA_CORS_ALLOWED_ORIGINS`; confirm the certificate is valid. |
| **App stuck in a forced-update loop** | `HINATA_APP_MIN_VERSION` is higher than the client's version | Lower `HINATA_APP_MIN_VERSION` to a version at or below your installed clients (or update the clients). It is also editable in Admin → App, which overrides the env. |
| **E-mails never arrive** | No real SMTP relay, wrong sender identity, or missing web base URL | Set a real `HINATA_SMTP_*` relay (Mailpit is dev-only); set `HINATA_MAIL_FROM` to an address your relay is allowed to send as; set `HINATA_WEB_BASE_URL` so deep links in mail point at the right host. |
| **SSE / live updates don't work** | The reverse proxy is buffering the stream | Disable response buffering for the stream path (e.g. `proxy_buffering off;` on nginx) so events are flushed as they occur. |
| **Rate-limited too aggressively / wrong client IP** | Every request looks like it comes from the proxy | Set `HINATA_TRUSTED_PROXIES` to the proxy's CIDR so the server reads the real client IP from `X-Forwarded-For` and rate-limits per user, not per proxy. |
| **MongoDB won't start** | Replica set not initialized, keyfile/PKI wrong | Ensure the replica set is initialized and the Mongo **keyfile** exists (`./deploy/generate-secrets.sh`); for prod, generate the X.509 PKI and register the client user. |
| **Everyone logged out after a redeploy** | `HINATA_JWT_SECRET` changed | Keep `HINATA_JWT_SECRET` **stable** across deployments — changing it invalidates every issued token. Generate it once and store it safely. |
| **Git webhooks never arrive** | Webhook base URL not public, callback not registered | Set `HINATA_GIT_WEBHOOK_BASE_URL` to a **public** API base and register `<public-api-base>/git/oauth/callback` at the provider; the webhook is registered automatically on connect. |

### App won't connect to the server

The app talks to the API at `HINATA_BASE_URL`, and browser (web) builds are subject
to CORS. Three things to check, in order:

1. **`HINATA_BASE_URL`** is the public API URL (e.g. `https://api.track.example.com`)
   and actually reachable from the device.
2. **CORS** — for the web client, the browser origin (e.g.
   `https://track.example.com`) must be listed in `HINATA_CORS_ALLOWED_ORIGINS`,
   which the hosted web app calls cross-origin.
3. **TLS** — the certificate must be valid for the API host; a self-signed or
   mismatched cert will fail silently in some clients.

See [Reverse proxy & TLS](/en/reverse-proxy.html) and
[Configuration reference](/en/configuration.html).

### Forced-update loop

On every start the app compares its version with the server's minimum and forces an
update when it is lower. If you set `HINATA_APP_MIN_VERSION` above what your users
actually have installed, they get stuck. Lower it to a version at or below your
fleet — or edit it in **Admin → App**, whose value overrides the environment.

### E-mails not delivered

Verification, password-reset and notification mail only leaves the server through a
**real SMTP relay** — Mailpit is a dev-only catcher. Configure `HINATA_SMTP_HOST`,
`_PORT`, `_USERNAME`, `_PASSWORD`, `_AUTH` and `_STARTTLS`, and set
`HINATA_MAIL_FROM` to an address your relay is authorized to send as (a mismatched
`From` identity is a common cause of silent rejects). Set `HINATA_WEB_BASE_URL` so
the deep links inside those e-mails point at your web app. See
[E-mail & SMTP](/en/email.html).

### Live updates / SSE not working

[Attachments and other live features](/en/api.html#live-updates-with-server-sent-events)
stream over Server-Sent Events. A reverse proxy that buffers responses will hold the
events until the connection closes, which looks exactly like "live sync is broken."
Turn buffering off for the stream path — on nginx, `proxy_buffering off;`. See
[Reverse proxy & TLS](/en/reverse-proxy.html).

### Rate-limited, or the wrong client IP is logged

Rate limiting keys on the client IP. Behind a proxy, every request appears to come
from the proxy's address unless you tell the server which proxies to trust. Set
`HINATA_TRUSTED_PROXIES` to the proxy's CIDR so the server reads the real client IP
from `X-Forwarded-For`. Empty means trust none — correct when there is no proxy,
wrong when there is one.

### MongoDB won't start

MongoDB runs as a replica set, which needs a shared **keyfile** for internal auth,
and in production **X.509** for the app connection. If it won't come up, confirm the
keyfile was generated (`./deploy/generate-secrets.sh`), the replica set is
initialized, and — for prod — that the PKI was generated
(`./deploy/x509/generate-certs.sh prod`) and the client user registered
(`./deploy/x509/init-prod-user.sh`). See [MongoDB & X.509](/en/database.html).

### Login loops after a redeploy

JWTs are signed with `HINATA_JWT_SECRET`. If that value changes between deploys,
every previously issued token becomes invalid and clients are bounced back to login.
Generate the secret **once** (`openssl rand -base64 64 | tr -d '\n'`) and keep it
stable in your `.env` / secret store across every redeploy.

### Git webhooks not arriving

For push / PR / CI events to reach your server, the webhook receiver must be
publicly reachable and the OAuth callback registered at the provider. Set
`HINATA_GIT_WEBHOOK_BASE_URL` to a **public** API base (it falls back to
`HINATA_BASE_URL` + `/api/v1`), and register `<public-api-base>/git/oauth/callback`
at each provider. The per-project webhook is registered automatically when you
connect a repository. See [Git integration](/en/git-integration.html).

## Where to go next

- [Configuration reference](/en/configuration.html) — every environment variable in one place.
- [Reverse proxy & TLS](/en/reverse-proxy.html) — CORS, SSE buffering and trusted proxies.
- [E-mail & SMTP](/en/email.html) — delivering verification and notification mail.
- [Self-hosting overview](/en/self-hosting.html) — the big picture and a config checklist.
