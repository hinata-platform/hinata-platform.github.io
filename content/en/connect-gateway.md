---
title: Hinata Connect gateway
description: One central, hosted relay for push and universal links, so the published app can serve every self-hosted Hinata server with no Firebase for operators.
---

# Hinata Connect gateway

Push notifications and universal links are tied to a **published app's** platform credentials (Firebase/FCM, Windows Push Notification Services, Apple and Google app-site associations). A self-hosted server can't own those for an app it didn't publish to the stores.

The **Hinata Connect gateway** is one small, central relay. With it, a single published app can serve *any* Hinata server, and self-hosters need **no Firebase at all**.

## What it does

The gateway is a shared, **hosted** service (default `https://connect.hinata.ahmadre.com`), run and secured by the app publisher. It relays two things:

1. **Push notifications:** the app's push credentials live in the gateway. It forwards notifications from any connected server to the right devices, via **FCM** for Android, iOS and macOS and via **WNS** for the Windows build, which Firebase does not support.
2. **Universal and app links:** the gateway owns the verified link domain. Invite, verification and password-reset links from *any* self-hosted server open the installed app on the correct backend.

```text
  Self-hosted server A ─┐
  Self-hosted server B ─┼── connects ──▶  Hinata Connect gateway  ──push──▶  📱 published app
  Self-hosted server C ─┘                    (hosted service)        ──link──▶  correct backend
```

Once your server is connected to the gateway, push and universal links work. The platform credentials live in the gateway, never in your deployment.

## Why it exists (one app, many servers)

The published app can [point at any self-hosted server](/en/self-hosted-app.html), so it can't bake in per-server push credentials. The gateway makes "one app, many servers" possible and keeps operators out of Firebase entirely.

!!! tip "Nothing to run for the common case"
    With the standard app and the default gateway, you operate no push infrastructure. Notifications flow once your instance is connected. This is the recommended path for most self-hosters.

## Configuration

| Variable | Purpose |
| --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Gateway URL. Defaults to the shared hosted gateway. Override it only to point at your own (see below). |

Universal links are relayed as `https://<gateway>/l/<code>`. The app decodes the code, switches to the originating server and opens the target. That is how an invite from *your* server opens the app on *your* backend.

## Running your own gateway

If you ship your **own** branded app to the stores, you own its push credentials and link domain. Then you run your own gateway and point your server at it with `HINATA_GATEWAY_BASE_URL`. This is an advanced path that goes with a full [custom client build](/en/self-hosted-app.html). The relay works the same way as the hosted gateway.

## Next steps

- Ship your own client: [Branding & custom clients](/en/self-hosted-app.html).
- Configure delivery channels: [Notifications](/en/notifications.html).
- Review link handling: [The apps](/en/clients.html).
