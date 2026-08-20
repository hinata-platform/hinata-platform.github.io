---
title: The apps
description: One Flutter codebase for Android, iOS, Web, macOS, Windows and Linux — how the client connects, gates versions, signs in, and manages multiple servers from a liquid-glass Server Manager.
---

# The apps

Hinata ships a single Flutter client that runs from **one codebase** on
**Android**, **iOS**, the **web**, and all three desktops — **macOS**,
**Windows** and **Linux**. There is no separate mobile app and desktop app to
keep in sync — the same screens, the same state, the same networking layer adapt
to whatever they run on. This page explains how the app connects to your server,
how it decides whether it is up to date, how you sign in, how a single app talks
to many servers at once, and what is worth knowing if you run it on Linux.


![Hinata on mobile](/assets/img/shot-mobile-dashboard.png)
*One Flutter codebase — Android, iOS, Web, macOS, Windows and Linux from a single app.*

## One codebase, six platforms

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
- **Native on the desktop.** The three desktop targets are real native builds,
  not a browser in a frame: macOS, Windows (packaged as an MSIX) and Linux as a
  **GTK 3** application. See [Hinata on Linux](#hinata-on-linux) for what that
  means in practice.

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
| **Ship a branded app to the stores** | Build your own **custom** client — see [Branding & custom clients](/en/self-hosted-app.html). |

The published store builds follow the bring-your-own-server model: because
native apps carry no baked-in server URL, one published app can serve every
operator through the
[Hinata Connect gateway](/en/connect-gateway.html). That gateway also relays
push notifications — to FCM for Android, iOS and macOS, and to WNS for Windows.
Linux has no such service to relay to, so the Linux build receives no push at
all; notifications reach you in the app and by e-mail instead.

On Linux there is no store lane to go through: the same build ships as a
**Flatpak** and as an **AppImage**, both produced from one bundle.

!!! note "Open source, GPL-3.0"
    The app is licensed **GPL-3.0**. You are free to build it, modify it and
    ship your own branded client — see the [custom-client guide](/en/self-hosted-app.html)
    for exactly what to change.

## Hinata on Linux

Linux is a full target, not a compatibility layer. The app builds as a native
**GTK 3** desktop application — one binary, `hinata`, with the application id
`com.ahmadre.hinata` — from exactly the same Flutter codebase as the phone and
the browser build. Sign-in, SSO, multi-server, boards, attachments, printing and
PDF export behave the way they do everywhere else.

### Installing it

| Format | What you get |
| --- | --- |
| **Flatpak** | The sandboxed desktop package. Build and install it from the manifest in `packaging/linux/flatpak/` with `flatpak-builder`; it is not currently published on a hosted Flatpak remote. |
| **AppImage** | One portable file: download it, `chmod +x`, run it. It links against your system's GTK, GStreamer and libsecret on purpose, so it keeps your desktop theme and your distribution's codecs instead of freezing its own copies. |
| **From source** | `flutter build linux --release` produces a relocatable bundle (the `hinata` binary plus `data/` and `lib/`) that you can install wherever you like. |

Both packages are built from the **same bundle**, and both recipes live in
`packaging/linux/` in
[hinata-app](https://github.com/hinata-platform/hinata-app). Release builds are
made on a pinned `ubuntu-22.04` runner, which makes the bundle's glibc floor a
decision rather than an accident: a Flutter bundle is dynamically linked against
the glibc it was built on, and glibc is only forward-compatible, so building on
a newer runner would quietly produce a binary that refuses to start on older
distributions.

To build it yourself on Debian or Ubuntu:

```bash
sudo apt install \
  clang cmake ninja-build pkg-config \
  libgtk-3-dev liblzma-dev libsecret-1-dev libjsoncpp-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

flutter config --enable-linux-desktop
flutter build linux --release
```

### Deep links land in the window you started from

The desktop entry registers the `x-scheme-handler/hinata` scheme, and the app
runs as a **single-instance** GTK application: launching `hinata` a second time
hands its arguments to the copy that is already running instead of opening a
rival window. That is what makes `hinata://auth-callback` work — an SSO return,
an invitation or a password-reset link arrives in the window you started from,
whether the app was already open or the link is what launched it.

### What differs on Linux

Two things are genuinely not available on Linux, and a few more lean on programs
your distribution may or may not have installed. The honest list:

| Area | On Linux | Why |
| --- | --- | --- |
| **Push notifications** | Not available. Notifications arrive **in the app** and **by e-mail**. | `firebase_messaging` has no Linux implementation, and there is no desktop push service to register a token with — nothing plays the role FCM plays on mobile or WNS on Windows. |
| **Camera capture** | The *take a photo* entry is not offered at all. Attaching an image or file you already have works normally. | No camera implementation exists for Linux. Leaving the entry out beats a button whose only possible outcome is an error dialog. |
| **Staying signed in** | Needs a keyring — see the callout below. | Session tokens are written through the freedesktop Secret Service. |
| **Voice comments** | Playback needs the GStreamer plugin packages, recording needs `pulseaudio-utils` and `ffmpeg`. | `just_audio` ships no Linux implementation, so playback runs through a GStreamer plugin written for this app. The recorder produces AAC, which is why `gstreamer1.0-libav` is required and not optional. |
| **Attachment file picker** | Uses `zenity`, `qarma` or `kdialog`. If none of them is installed, the app names the ones you can install instead of opening nothing. | The Flutter file picker has no native Linux backend; it drives one of those dialogs. |
| **Downloads** | An attachment is saved straight into your Downloads folder and a toast names the file. | There is no share sheet on Linux to hand the file to, so the app tells you where it went. |

Your **notification settings stay visible and editable** on a Linux desktop even
though push never fires there. The preference belongs to your account, not to
the machine you happen to be sitting at — hiding it on Linux would take away the
switch that governs your phone.

!!! warning "Staying signed in needs a keyring"
    Hinata keeps your session tokens in the system keyring through the
    freedesktop **Secret Service** — GNOME Keyring, KWallet or anything else that
    implements it. A minimal window manager, a container, or an SSH session into
    a desktop whose keyring was never unlocked has nothing to store them in.
    Sign-in still works and your session lasts until you close the app, and the
    app says so at the time rather than letting you discover it at the next
    launch.

    ```bash
    sudo apt install gnome-keyring     # Debian / Ubuntu
    sudo dnf install gnome-keyring     # Fedora
    ```

Everything in the table above works on a normal desktop install. If you are on a
slim system — a container, a bare window manager — this is the whole list:

```bash
sudo apt install \
  gnome-keyring zenity \
  pulseaudio-utils ffmpeg \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-libav
```

!!! tip "The Flatpak brings most of that with it"
    The Flatpak runtime already contains GTK, `zenity`, FFmpeg and the GStreamer
    plugins, so a Flatpak install only needs a keyring on the host to keep you
    signed in.

## Where to go next

- [Branding & custom clients](/en/self-hosted-app.html) — runtime branding, or ship your own client.
- [Authentication](/en/authentication.html) — local accounts, registration, 2FA.
- [Single sign-on](/en/sso.html) — connect an identity provider.
- [Setup & first run](/en/setup-wizard.html) — configuring a fresh server.
