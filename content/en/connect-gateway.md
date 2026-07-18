---
title: Hinata Connect gateway
description: One central, hosted relay for mobile push and universal links, so the single published app can serve every self-hosted Hinata server — with no Firebase for operators.
---

# Hinata Connect gateway

Mobile push notifications and universal links have an awkward requirement: they're tied to a **published app's** platform credentials (Firebase/FCM, Apple/Google app-site associations). A self-hosted server can't own those for an app it didn't publish to the stores. The **Hinata Connect gateway** solves this with one small, central relay so that a single published app can serve *any* Hinata server — and self-hosters need **no Firebase at all**.

## What it does

The gateway is a shared, **hosted** service (default `https://connect.hinata.ahmadre.com`), operated and secured by the app publisher, that relays two things:

1. **Push notifications** — the published app's push credentials live in the gateway, so it can forward notifications from any connected server to the right devices.
2. **Universal / app links** — it owns the verified link domain, so invite, verification and password-reset links from *any* self-hosted server open the installed app on the correct backend.

```text
  Self-hosted server A ─┐
  Self-hosted server B ─┼── connects ──▶  Hinata Connect gateway  ──push──▶  📱 published app
  Self-hosted server C ─┘                    (hosted service)        ──link──▶  correct backend
```

Once your server is connected to the gateway, push and universal-link relaying just work — the platform credentials live in the gateway, never in your deployment.

## Why it exists (one app, many servers)

Because the one published app can [point at any self-hosted server](/en/self-hosted-app.html), it can't bake in per-server push credentials. The gateway is the shared piece that makes "one app, many servers" possible while keeping operators out of the Firebase business entirely.

!!! tip "Nothing to run for the common case"
    If you use the standard app and the default gateway, there is no push infrastructure to operate: the gateway is a hosted service, and notifications flow once your instance is connected. This is the recommended path for most self-hosters.

## Configuration

| Variable | Purpose |
| --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Gateway URL. Defaults to the shared hosted gateway; override it only to point at your own (see below). |

Universal links are relayed as `https://<gateway>/l/<code>`; the app decodes the code, switches to the originating server and routes to the target — which is how an invite from *your* server opens the app pointed at *your* backend.

## Running your own gateway

If you ship your **own** branded app to the stores, you'll own its push credentials and link domain — so you run your own gateway and point your server at it with `HINATA_GATEWAY_BASE_URL`. This is an advanced path that goes hand-in-hand with a full [custom client build](/en/self-hosted-app.html); the shape of the relay is the same as the hosted gateway.

## Next steps

- Ship your own client in [Branding & custom clients](/en/self-hosted-app.html).
- Configure delivery channels in [Notifications](/en/notifications.html).
- Review link handling in [The apps](/en/clients.html).
