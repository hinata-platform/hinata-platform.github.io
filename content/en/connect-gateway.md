---
title: Hinata Connect gateway
description: One central relay for mobile push and universal links, so a single published white-label app can serve every self-hosted Hinata server — with no Firebase for operators.
---

# Hinata Connect gateway

Mobile push notifications and universal links have an awkward requirement: they're tied to a **published app's** platform credentials (Firebase/FCM, Apple/Google app-site associations). A self-hosted server can't own those for an app it didn't publish to the stores. The **Hinata Connect gateway** solves this with one small, central relay so that a single published app can serve *any* Hinata server — and self-hosters need **no Firebase at all**.

## What it does

The gateway is a shared, central service (default `https://connect.hinata.ahmadre.com`) that relays two things:

1. **Push notifications** — it holds the published app's FCM credentials and forwards push messages from any registered server to the right devices.
2. **Universal / app links** — it owns the verified link domain, so invite, verification and password-reset links from *any* self-hosted server open the installed app on the correct backend.

```text
  Self-hosted server A ─┐
  Self-hosted server B ─┼──registers on boot──▶  Hinata Connect gateway  ──push──▶  📱 published app
  Self-hosted server C ─┘                         (owns FCM + link domain)   ──/l/<code>──▶  deep link
```

Your server **registers itself with the gateway on boot**. From then on, push and universal-link relaying just work — the FCM keys and the app-site-association files live in the gateway, never in your deployment.

## Why it exists (white-label)

Because one published, [white-label](/en/white-label.html) app can point at many servers, it can't bake in per-server push credentials. The gateway is the shared piece that makes "one app, many servers" possible while keeping operators out of the Firebase business entirely.

!!! tip "Nothing to configure for the common case"
    If you use the standard app and the default gateway, there is no push setup: your server registers on boot and notifications flow. This is the recommended path for most self-hosters.

## Configuration

| Variable | Purpose |
| --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Gateway URL. Defaults to the shared gateway; override to point at your own. |
| `HINATA_GATEWAY_BOOTSTRAP_SECRET` | Optional — only if your gateway gates registration behind a bootstrap secret. |

Universal links are relayed as `https://<gateway>/l/<code>`, where `<code>` encodes the originating server, the in-app path and a token. The app decodes it locally, switches to the correct server and routes to the target — which is how an invite from *your* server opens the app pointed at *your* backend.

## Running your own gateway

If you ship your **own** branded app to the stores, you'll own its FCM credentials and link domain — so you run your own gateway and point your server at it with `HINATA_GATEWAY_BASE_URL`. This is an advanced path that goes hand-in-hand with a full [white-label build](/en/white-label.html); the mechanics of registration and relaying are identical to the shared gateway.

!!! warning "Self-registration hardening"
    A gateway that accepts open registration should be protected in production (e.g. a bootstrap secret) so only your servers can register. Use `HINATA_GATEWAY_BOOTSTRAP_SECRET` when you run your own.

## Next steps

- Ship your own client in [White-label & branding](/en/white-label.html).
- Configure delivery channels in [Notifications](/en/notifications.html).
- Review link handling in [The apps](/en/clients.html).
