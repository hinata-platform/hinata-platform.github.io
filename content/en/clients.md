---
title: The apps
description: How the Hinata app for Android, iOS, Web, macOS, Windows and Linux connects, signs in and manages several servers.
---

# The apps

Hinata has a single Flutter client for **Android**, **iOS**, the **web**,
**macOS**, **Windows** and **Linux**. There is no separate mobile and desktop
app. The same screens, the same state and the same networking layer adapt to the
platform.

This page covers connecting, the version gate, signing in, multiple servers and
running on Linux.

![Hinata on mobile](/assets/img/shot-mobile-dashboard.png)
*One app from one Flutter codebase for six platforms.*

## One codebase, six platforms

The client uses Flutter, bloc/cubit for state, go_router for routing and i18next
for localization. Every network call goes through one `ApiClient` built on
**dio** (automatic token refresh, `Accept-Language` header). A new feature lands
everywhere at once.

- **Responsive:** breakpoints derived from the golden ratio instead of fixed
  pixel widths. The same UI fits a phone, a tablet, a desktop window and a
  browser tab.
- **Localized:** UI in **English** and **German** (i18next). Error messages are
  translated **by the server**. The client sends the user's language via
  `Accept-Language`, and the server returns the finished message.
- **Light and dark:** a navy navigation rail, a warm paper workspace and the
  honey amber accent `#D9A032`, which looks the same in both modes. Glass
  surfaces appear on the mobile nav, the ⌘K palette and the attachment lightbox.
- **Native on the desktop:** real native builds rather than a browser in a
  frame. macOS, Windows (packaged as MSIX) and Linux as a **GTK 3**
  application. Details under [Hinata on Linux](#hinata-on-linux).

## How it works: from launch to workspace

Every fresh launch runs in this order:

| Step | What happens |
| --- | --- |
| **Connect** | On first start the app asks for your **server URL** and only continues once the server answers at `/api/v1/meta`. |
| **Version gate** | The app compares its version with the server's minimum (`HINATA_APP_MIN_VERSION`, exposed as `minAppVersion`) and forces an update when the client is too old. |
| **Setup wizard** | A brand-new server is set up directly in the app (organization name and first admin), unless it was bootstrapped with `HINATA_SETUP_*`. |
| **Onboarding** | A one-time illustrated tour of the key features. |
| **Sign in** | Local credentials, or **SSO** (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP). |

### Connect

A native app first asks for a server URL. It probes `/api/v1/meta` and only
continues once the server responds. That way you never end up connected to a
host that isn't a Hinata server.

Previously used servers appear as shortcuts below the URL field. After a brief
outage, reconnecting takes one tap.

!!! info "Native apps have no built-in server URL"
    A published native app has no server address compiled into it. That is how
    one app can serve every Hinata operator. Only the **web** build may default
    to its own origin (via `kIsWeb`), because it is already served from a known
    host. See [Multi-server](#multi-server-one-app-many-servers).

### Version gate

On every start the app reads the minimum client version from the server. If the
installed app is older, it shows an **update-required** screen instead of the
workspace.

Operators set the value with `HINATA_APP_MIN_VERSION` or override it live in the
[Admin area](/en/admin-area.html) → Platform. The database value wins. This
lets you move every client onto a new build as soon as a breaking change ships,
with no client-side coordination.

### Setup wizard

Point the app at a freshly deployed server and it walks you through first-run
setup: your organization name and the first administrator account.

To skip the wizard, set `HINATA_SETUP_AUTO_COMPLETE=true` together with
`HINATA_SETUP_ORGANIZATION_NAME` and the admin credentials. See
[Setup & first run](/en/setup-wizard.html).

### Sign in

You sign in with:

- **Local credentials:** username or e-mail and password. Self-registration,
  e-mail verification, forgot password and optional admin approval are
  controlled by feature flags (see [Authentication](/en/authentication.html)).
- **SSO:** OpenID Connect, OAuth 2.0, SAML 2.0 or LDAP, configured in the Admin
  area. The app is reopened through the `hinata://auth-callback` deep link. See
  [Single sign-on](/en/sso.html).

If two-factor authentication (TOTP) is enabled on the account, a one-time code
is requested after the password.

## Multi-server: one app, many servers

One Hinata app can talk to any number of independent servers. You switch between
them without signing out of the others.

- Add each server once, and the app remembers it.
- Switch freely from the switcher. Each server keeps its own session.
- Access tokens only work for the server that issued them. Switching never moves
  credentials between instances.

### The Server Manager

The **Server Manager** (in the glass design) is where you manage saved servers.
On open it probes all of them **in parallel**. Each row shows a live status with
a pulsing dot and a real ping in milliseconds. It changes from *checking…* to
*online* (with latency) or *offline*.

From the manager you can:

- **Add** a server. A **connection test** runs before saving, so a wrong or
  unreachable URL is caught right away.
- **Edit** a server's name or URL.
- **Delete** a server you no longer use.
- **Switch** to any online server with a tap.

!!! tip "Self-hosted or cloud, side by side"
    Each row has a badge, so you can spot your own self-hosted instance at a
    glance. Because tokens are scoped per server, keeping a work server and a
    personal one in the same app is safe.

## Where to get the app

| You want to… | Use |
| --- | --- |
| **Just use a server in the browser** | The hosted **web app**. An operator serves it at `https://track.example.com` (the `docker-compose.app.yml` overlay). Nothing to install. |
| **Run the client yourself from source** | Clone [hinata-app](https://github.com/hinata-platform/hinata-app), `flutter pub get`, `flutter run`. GPL-3.0. |
| **Ship a branded app to the stores** | Build your own **custom** client, see [Branding & custom clients](/en/self-hosted-app.html). |

The store builds carry no built-in server URL. You bring your own server, and
one published app serves every operator through the
[Hinata Connect gateway](/en/connect-gateway.html).

The gateway also relays push notifications: to FCM for Android, iOS and macOS,
and to WNS for Windows. Linux has no such service, so the Linux build gets no
push. Notifications reach you in the app and by e-mail instead.

Linux gets the app from the **Snap Store**: `snap install hinata` installs a
strictly confined snap for amd64 and arm64 from
[snapcraft.io/hinata](https://snapcraft.io/hinata). The **Flatpak** manifest and
the **AppImage** script are in the repository for building it yourself.

!!! note "Open source, GPL-3.0"
    The app is licensed **GPL-3.0**. You are free to build it, modify it and
    ship your own branded client. The
    [custom-client guide](/en/self-hosted-app.html) lists what to change.

## Hinata on Linux

Linux is a full target. The app is a native **GTK 3** application with the
binary `hinata` and the application id `com.ahmadre.hinata`, built from the same
Flutter codebase as the phone and web versions. Sign-in, SSO, multi-server,
boards, attachments, printing and PDF export work as everywhere else.

### Installing it

| Format | What you get |
| --- | --- |
| **Snap** | The channel Hinata ships Linux through. `sudo snap install hinata` on any distribution with snapd, for x86-64 and ARM64, strictly confined. Two permissions need connecting by hand (see below). |
| **Flatpak** | Build and install it yourself with `flatpak-builder` from the manifest in `packaging/linux/flatpak/`. It is on no hosted Flatpak remote and not on Flathub. |
| **AppImage** | One portable file you build yourself: `packaging/linux/appimage/build-appimage.sh` turns a release bundle into it, then `chmod +x` and run. It is published nowhere. CI attaches it to a workflow run, not to a release. It links against your system's GTK, GStreamer and libsecret on purpose, so it keeps your desktop theme and your distribution's codecs. |
| **From source** | `flutter build linux --release` produces a relocatable bundle (the `hinata` binary plus `data/` and `lib/`) that you can install wherever you like. |

!!! info "Two permissions need one click"
    Snap runs the app under strict confinement. Two interfaces are not
    connected automatically, because a store makes you grant that access
    deliberately:

    ```bash
    sudo snap connect hinata:password-manager-service   # stay signed in
    sudo snap connect hinata:audio-record               # record a voice comment
    ```

    Without the first, the app runs but cannot keep your session in the
    keyring, so every restart lands on the sign-in screen. Without the second,
    the microphone button does nothing. The app names the missing permission.
    The same toggles are in Ubuntu's App Center under the app's Permissions.

    For the current status, check `snap info hinata`. It lists the channels
    that carry a revision and which build sits on each. **stable** (what a bare
    `snap install hinata` reads) carries the released version for both
    architectures. **edge** carries the build from the last tag. It is ahead of
    stable and less settled: `snap install hinata --edge`.

All three recipes live in `packaging/linux/` in
[hinata-app](https://github.com/hinata-platform/hinata-app). They install the
same desktop entry, icon and AppStream metainfo.

- The Flatpak and the AppImage package a bundle built beforehand.
  `flatpak-builder` runs its modules with no network, so the Flatpak needs a
  finished bundle.
- The snap runs the Flutter build itself. A snapcraft build step has network,
  and the Flutter engine artefacts and pdfium are fetched during the build.

The AppImage and the raw bundle are built on a pinned `ubuntu-22.04` runner,
which sets their glibc floor on purpose. A Flutter bundle is dynamically linked
against the glibc it was built with, and glibc is only forward-compatible. Built
on a newer runner, the binary would not start on older distributions. The snap
needs no pin, because its libc comes from its `core24` base.

!!! note "Not on Flathub"
    Hinata is not offered on Flathub. On Linux the app comes through the Snap
    Store. The Flatpak manifest and the AppImage script are for building it
    yourself.

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

The desktop entry registers the `x-scheme-handler/hinata` scheme. The app runs
as a **single-instance** GTK application. Launching `hinata` a second time hands
its arguments to the running copy instead of opening another window.

That is what makes `hinata://auth-callback` work. An SSO return, an invitation or
a password-reset link arrives in your window, whether the app was already open
or the link launched it.

### What differs on Linux

Two things are not available on Linux. A few more depend on programs your
distribution may not have installed.

| Area | On Linux | Why |
| --- | --- | --- |
| **Push notifications** | Not available. Notifications arrive **in the app** and **by e-mail**. | `firebase_messaging` has no Linux implementation, and there is no desktop push service to register a token with. Nothing plays the role of FCM on mobile or WNS on Windows. |
| **Camera capture** | The *take a photo* entry is not offered. Attaching an image or file you already have works normally. | No camera implementation exists for Linux. An entry that could only show an error dialog is left out. |
| **Staying signed in** | Needs a keyring, see the callout below. | Session tokens are written through the freedesktop Secret Service. |
| **Voice comments** | Playback needs the GStreamer plugin packages, recording needs `pulseaudio-utils` and `ffmpeg`. | `just_audio` ships no Linux implementation, so playback runs through a GStreamer plugin written for this app. The recorder produces AAC, which is why `gstreamer1.0-libav` is required. |
| **Attachment file picker** | Uses `zenity`, `qarma` or `kdialog`. If none is installed, the app names the ones you can install. | The Flutter file picker has no native Linux backend and drives one of those dialogs. |
| **Downloads** | An attachment is saved straight into your Downloads folder, and a toast names the file. | Linux has no share sheet to hand the file to, so the app tells you where it went. |

Your **notification settings stay visible and editable** on Linux, even though
push never fires there. They belong to your account and also control your phone.

!!! warning "Staying signed in needs a keyring"
    Hinata keeps your session tokens in the system keyring through the
    freedesktop **Secret Service**: GNOME Keyring, KWallet or anything else that
    implements it. A minimal window manager, a container or an SSH session into
    a desktop whose keyring was never unlocked has nowhere to store them.

    Sign-in still works, but your session only lasts until you close the app.
    The app tells you so right away.

    ```bash
    sudo apt install gnome-keyring     # Debian / Ubuntu
    sudo dnf install gnome-keyring     # Fedora
    ```

Everything in the table works on a normal desktop install. On a slim system (a
container, a bare window manager) this is the full list:

```bash
sudo apt install \
  gnome-keyring zenity \
  pulseaudio-utils ffmpeg \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-libav
```

!!! tip "The packaged builds bring most of that with them"
    The Flatpak runtime already contains GTK, `zenity`, FFmpeg and the GStreamer
    plugins. A Flatpak install only needs a keyring on the host.

    The snap brings FFmpeg, PulseAudio's recording tools and the extra GStreamer
    plugins itself, and picks files through the desktop portal instead of
    `zenity`. Two of its permissions reach the keyring and the microphone, so
    they do not connect on their own:

    ```bash
    sudo snap connect hinata:password-manager-service   # stay signed in
    sudo snap connect hinata:audio-record               # record voice comments
    ```

## Where to go next

- [Branding & custom clients](/en/self-hosted-app.html): runtime branding, or ship your own client.
- [Authentication](/en/authentication.html): local accounts, registration, 2FA.
- [Single sign-on](/en/sso.html): connect an identity provider.
- [Setup & first run](/en/setup-wizard.html): configure a fresh server.
