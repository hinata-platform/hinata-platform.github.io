---
title: The apps
description: One Flutter codebase for Android, iOS, Web and macOS — how the client connects, gates versions, signs in, and manages multiple servers from a liquid-glass Server Manager.
---

# The apps

Hinata ships a single Flutter client that runs from **one codebase** on
**Android, iOS, Web and macOS**. There is no separate mobile app and desktop
app to keep in sync — the same screens, the same state, the same networking
layer adapt to whatever they run on. This page explains how the app connects to
your server, how it decides whether it is up to date, how you sign in, and how a
single app talks to many servers at once.


![Hinata on mobile](/assets/img/shot-mobile-dashboard.png)
*One Flutter codebase — Android, iOS, Web and macOS from a single app.*

## One codebase, four platforms

The client is built with Flutter. State is managed with bloc/cubit, routing with
go_router, localization with i18next, and every network call goes through a
single `ApiClient` built on **dio** (automatic token refresh, `Accept-Language`
header). Because there is only one codebase, a feature lands everywhere at once.

- **Responsive by design.** Layout adapts through golden-ratio-derived
  breakpoints rather than fixed pixel widths, so the same UI reflows cleanly from
  a phone to a tablet to a desktop window to a browser tab.
- **Localized.** The UI ships in **English** and **German** (i18next), and error
  messages are localized **by the server** through the `Accept-Language` header —
  the client sends the user's language, the server returns the message already
  translated.
- **Light & dark.** A navy navigation rail, a warm-paper workspace and the
  signature honey-amber accent `#D9A032` that reads identically in light and dark
  mode, with liquid-glass surfaces on the mobile nav, the ⌘K palette and the
  attachment lightbox.

## How it works: from launch to workspace

Every fresh launch walks a short, predictable path before you land in your
workspace.

| Step | What happens |
| --- | --- |
| **Connect** | On first start the app asks for your **server URL** and only continues once the server answers at `/api/v1/meta`. |
| **Version gate** | The app compares its own version with the server's minimum (`HINATA_APP_MIN_VERSION`, exposed as `minAppVersion`) and forces an update when the client is too old. |
| **Setup wizard** | A brand-new server is configured directly in the app — organization name and first admin — unless it was bootstrapped with `HINATA_SETUP_*`. |
| **Onboarding** | A one-time illustrated tour of the key features. |
| **Sign in** | Local credentials, or **SSO** (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP). |

### Connect

The very first thing a native app asks for is a server URL. It probes
`/api/v1/meta` and refuses to continue until the server responds, so you can
never end up "connected" to a host that isn't a Hinata server. Previously used
servers appear as one-tap shortcuts beneath the URL field, which makes
re-connecting after a server was briefly unreachable a single tap.

!!! info "Native apps never bake in a server URL"
    A published native app has no server address compiled into it. This is what
    lets one app serve every Hinata operator. Only the **web** build may default
    to its own origin (via `kIsWeb`), because it is already served from a known
    host. See [Multi-server](#multi-server-one-app-many-servers) below.

### Version gate

On every start the app reads the server's advertised minimum client version. If
the installed app is older, it shows an **update-required** screen instead of the
workspace. Operators control this value with the `HINATA_APP_MIN_VERSION`
environment variable, or override it live in the
[Admin area](/en/admin-area.html) → App settings (the database value wins). This
means you can force every client onto a new build the moment a breaking change
ships — no client-side coordination required.

### Setup wizard

Point the app at a freshly deployed server and it walks you through first-run
setup in the UI: your organization name and the first administrator account. If
you would rather bootstrap unattended, set `HINATA_SETUP_AUTO_COMPLETE=true`
together with `HINATA_SETUP_ORGANIZATION_NAME` and the admin credentials, and the
wizard is skipped. See [Setup & first run](/en/setup-wizard.html).

### Sign in

Once a server is set up, you authenticate with either:

- **Local credentials** — username/e-mail and password. Self-registration,
  e-mail verification, forgot-password and optional admin approval are all
  supported and toggled by feature flags (see [Authentication](/en/authentication.html)).
- **SSO** — OpenID Connect, OAuth 2.0, SAML 2.0 or LDAP, configured by the
  operator in the Admin area. SSO returns to the app through the
  `hinata://auth-callback` deep link. See [Single sign-on](/en/sso.html).

When two-factor authentication (TOTP) is enabled on an account, sign-in adds a
one-time-code challenge after the password step.

## Multi-server: one app, many servers

A single Hinata app can talk to any number of independent servers, and switch
between them without signing out of the others.

- **Save multiple servers.** Add each server once; the app remembers them.
- **Switch freely.** Move between servers from the switcher; each keeps its own
  session.
- **Per-server scoped tokens.** Access tokens are scoped to the server that
  issued them — switching servers never leaks credentials across instances.

### The Server Manager

The liquid-glass **Server Manager** is where you administer your saved servers.
It probes every saved server **in parallel** on open, so each row shows a live
status — a pulsing dot and a real ping in milliseconds — and flips from
*checking…* to *online* (with latency) or *offline* as results land.

From the manager you can:

- **Add** a server — the app runs a **connection test** before saving, so an
  unreachable or wrong URL is caught immediately.
- **Edit** a saved server's name or URL.
- **Delete** a server you no longer use.
- **Switch** to any online server with a tap.

!!! tip "Self-hosted or cloud, side by side"
    Each row is badged so you can tell your own self-hosted instance apart from
    others at a glance. Because tokens are scoped per server, keeping a work
    server and a personal server in the same app is completely safe.

## Where to get the app

There are three ways to run the client, depending on who you are.

| You want to… | Use |
| --- | --- |
| **Just use a server in the browser** | The hosted **web app** — an operator serves it at `https://track.example.com` (the `docker-compose.app.yml` overlay). Nothing to install. |
| **Run the client yourself from source** | Clone [hinata-app](https://github.com/hinata-platform/hinata-app), `flutter pub get`, `flutter run`. GPL-3.0. |
| **Ship a branded app to the stores** | Build your own **white-label** client — see [White-label & branding](/en/white-label.html). |

The published store builds are white-label apps: because native apps carry no
baked-in server URL, one published app can serve every operator through the
[Hinata Connect gateway](/en/connect-gateway.html).

!!! note "Open source, GPL-3.0"
    The app is licensed **GPL-3.0**. You are free to build it, modify it and
    ship your own branded client — see the [white-label guide](/en/white-label.html)
    for exactly what to change.

## Where to go next

- [White-label & branding](/en/white-label.html) — ship your own branded client.
- [Authentication](/en/authentication.html) — local accounts, registration, 2FA.
- [Single sign-on](/en/sso.html) — connect an identity provider.
- [Setup & first run](/en/setup-wizard.html) — configuring a fresh server.
