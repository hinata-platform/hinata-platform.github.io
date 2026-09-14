---
title: FAQ & troubleshooting
description: Answers to common questions about Hinata and concrete fixes for the usual problems.
---

# FAQ & troubleshooting

Common questions from self-hosters, and fixes for the problems that come up in
practice. The linked pages go deeper.

## Frequently asked questions

### Is Hinata really free, with no limits?

Yes. Hinata is **open source under the GPL-3.0 license**. There are **no user, team
or board limits**, and there never will be. There is no paid tier, no per-seat
billing and no locked feature. The whole platform is the code in the two
repositories.

### Do I need Firebase for push notifications?

**No.** Mobile push and universal (deep) links run through the central
[Hinata Connect gateway](/en/connect-gateway.html), a hosted service. The app's push
credentials live there, so you configure **nothing** for push. You only need
Firebase if you ship your **own** client with its own store listing and run your own
gateway.

### Can I use my own domain and branding?

**Yes.** Everything already runs under your domain (`track.example.com` for the web
app, `api.track.example.com` for the API). The app picks up your organization's name
and logo from your server at runtime.

You can also build your own client: your own package id, app name, icons, splash
and accent color, pointed at the gateway. See
[Branding & custom clients](/en/self-hosted-app.html). Native apps have no built-in
server URL. Users save servers and switch between them, so one app can serve many
instances.

### Which databases and storage does Hinata use?

- **MongoDB** is the system of record. Production runs a **replica set** (2 data
  nodes + 1 arbiter) with TLS and X.509 client authentication. See
  [MongoDB & X.509](/en/database.html).
- **S3-compatible object storage** holds attachments and avatars, with randomized
  object keys and presigned downloads. The stack ships **MinIO**, and any
  S3-compatible store works. See [Object storage](/en/storage.html).

There is no separate SQL database and no message broker. Live updates use SSE.

### Does SSO work with my identity provider?

Very likely. Hinata supports **OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP**. You
configure it at runtime in the Admin area (stored in MongoDB, no restart). That
covers Keycloak, Authentik, Azure AD, Google, Synology SSO and anything that speaks
those protocols. See [Single sign-on (SSO)](/en/sso.html).

### Do configuration changes need a restart?

Mostly not. Runtime settings (SSO, e-mail ingest, push, Git OAuth apps, app
settings) are **stored in MongoDB and managed from the Admin area**. **The database
overrides the environment.** Changes apply on the next request. Only bootstrap
variables like `HINATA_JWT_SECRET` need a redeploy. See
[Architecture → Runtime settings](/en/architecture.html).

## Troubleshooting

Symptom, usual cause and fix at a glance. Details follow below.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| **App won't connect to the server** | Wrong base URL, blocked CORS, or a TLS problem | `HINATA_BASE_URL` must be the public API URL and reachable over HTTPS. Add the web app's origin to `HINATA_CORS_ALLOWED_ORIGINS`. Check that the certificate is valid. |
| **App stuck in a forced-update loop** | `HINATA_APP_MIN_VERSION` is higher than the client's version | Lower `HINATA_APP_MIN_VERSION` to a version at or below your installed clients (or update the clients). Also editable in Admin → App, which overrides the env. |
| **E-mails never arrive** | No real SMTP relay, wrong sender address, or missing web base URL | Set a real `HINATA_SMTP_*` relay (Mailpit is dev only). Set `HINATA_MAIL_FROM` to an address your relay may send as. Set `HINATA_WEB_BASE_URL` so links in mail point at the right host. |
| **SSE / live updates don't work** | The reverse proxy is buffering the stream | Disable response buffering for the stream path (e.g. `proxy_buffering off;` on nginx) so events arrive right away. |
| **Rate-limited too aggressively / wrong client IP** | Every request looks like it comes from the proxy | Set `HINATA_TRUSTED_PROXIES` to the proxy's CIDR. The server then reads the real client IP from `X-Forwarded-For` and limits per user, not per proxy. |
| **MongoDB won't start** | Replica set not initialized, keyfile or PKI wrong | Initialize the replica set and make sure the Mongo **keyfile** exists (`./deploy/generate-secrets.sh`). For prod, generate the X.509 PKI and register the client user. |
| **Everyone logged out after a redeploy** | `HINATA_JWT_SECRET` changed | Keep `HINATA_JWT_SECRET` **stable** across deployments. Changing it invalidates every issued token. Generate it once and store it safely. |
| **Git webhooks never arrive** | Webhook base URL not public, callback not registered | Set `HINATA_GIT_WEBHOOK_BASE_URL` to a **public** API base and register `<public-api-base>/git/oauth/callback` at the provider. The webhook is registered automatically on connect. |

### App won't connect to the server

Check in order:

1. **`HINATA_BASE_URL`** is the public API URL (e.g.
   `https://api.track.example.com`) and reachable from the device.
2. **CORS**: web builds call the API cross-origin. Their origin (e.g.
   `https://track.example.com`) must be listed in `HINATA_CORS_ALLOWED_ORIGINS`.
3. **TLS**: the certificate must be valid for the API host. A self-signed or
   mismatched cert fails without an error message in some clients.

See [Reverse proxy & TLS](/en/reverse-proxy.html) and
[Configuration reference](/en/configuration.html).

### Forced-update loop

On start, the app compares its version with the server's minimum and forces an
update if it is lower. Lower `HINATA_APP_MIN_VERSION` to a version at or below what
your users have installed. Or edit it in **Admin → App**, which overrides the
environment.

### E-mails not delivered

Verification, password reset and notification mail needs a **real SMTP relay**.
Mailpit only catches mail in development.

- Set `HINATA_SMTP_HOST`, `_PORT`, `_USERNAME`, `_PASSWORD`, `_AUTH` and
  `_STARTTLS`.
- Set `HINATA_MAIL_FROM` to an address your relay is authorized to send as. A
  mismatched `From` identity often gets mail rejected without notice.
- Set `HINATA_WEB_BASE_URL` so the links inside those e-mails point at your web app.

See [E-mail & SMTP](/en/email.html).

### Live updates / SSE not working

[Attachments and other live features](/en/api.html#live-updates-with-server-sent-events)
stream over Server-Sent Events. A buffering reverse proxy holds the events until the
connection closes. Turn buffering off for the stream path, on nginx with
`proxy_buffering off;`. See [Reverse proxy & TLS](/en/reverse-proxy.html).

### Rate-limited, or the wrong client IP is logged

Rate limiting keys on the client IP. Behind a proxy, every request appears to come
from the proxy. Set `HINATA_TRUSTED_PROXIES` to the proxy's CIDR, and the server
reads the real client IP from `X-Forwarded-For`. Empty means trust none, which is
only right without a proxy.

### MongoDB won't start

The replica set needs a shared **keyfile** for internal auth, and in production
**X.509** for the app connection. Check:

- The keyfile was generated (`./deploy/generate-secrets.sh`).
- The replica set is initialized.
- Prod only: the PKI was generated (`./deploy/x509/generate-certs.sh prod`) and the
  client user registered (`./deploy/x509/init-prod-user.sh`).

See [MongoDB & X.509](/en/database.html).

### Login loops after a redeploy

JWTs are signed with `HINATA_JWT_SECRET`. If that value changes, every previously
issued token becomes invalid and clients land back at login. Generate the secret
**once** (`openssl rand -base64 64 | tr -d '\n'`) and keep it stable in your `.env`
or secret store.

### Git webhooks not arriving

Push, PR and CI events need a publicly reachable webhook receiver and a registered
OAuth callback.

- Set `HINATA_GIT_WEBHOOK_BASE_URL` to a **public** API base (it falls back to
  `HINATA_BASE_URL` + `/api/v1`).
- Register `<public-api-base>/git/oauth/callback` at each provider.

The per-project webhook is registered automatically when you connect a repository.
See [Git integration](/en/git-integration.html).

## Where to go next

- [Configuration reference](/en/configuration.html): every environment variable in one place.
- [Reverse proxy & TLS](/en/reverse-proxy.html): CORS, SSE buffering and trusted proxies.
- [E-mail & SMTP](/en/email.html): delivering verification and notification mail.
- [Self-hosting overview](/en/self-hosting.html): the big picture and a config checklist.
