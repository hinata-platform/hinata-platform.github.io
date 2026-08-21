---
title: Branding & custom clients
description: One published client app for self-hosted Hinata servers — runtime branding from your server, and how to build your own client (package id, name, icons, splash, accent, deep links) if you want one. Practical, step-by-step, GPL-3.0.
---

# Branding & custom clients

Hinata follows the **one app, self-hosted servers** model you know from
Rocket.Chat or Nextcloud: you run your own server instance, and the single
published Hinata app connects to it. The native app carries **no baked-in
server URL** — users bring their own server, and branding (organization name
and logo) comes from the server at runtime via `/api/v1/meta`. Push and
universal links work for every instance through the
[Hinata Connect gateway](/en/connect-gateway.html), so most operators never
need to build anything. If you *do* want a client of your own under your own
store listing, you are equally free to build and publish one — this page is
the practical guide to doing exactly that.

!!! note "Open source, GPL-3.0"
    The client is licensed **GPL-3.0**. You may rebrand, modify and distribute it,
    provided you honor the license — chiefly, make your corresponding source
    available to your users under the same terms.

## The zero-build option: the hosted web app

Before you build anything, consider whether you even need a native app. The
server repository ships `docker-compose.app.yml`, an overlay that serves the
compiled Flutter **web** client as static files at your own domain, e.g.
`https://track.example.com`.

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

This gives users a branded URL in the browser with **nothing to install and
nothing to build**. The web build points at whatever API it is configured for,
so many operators run only this and let mobile users reach them through the
published apps. Reach for a custom native build when you specifically need your
own store presence, icon and name.

## What you change

A custom client is a fork of [hinata-app](https://github.com/hinata-platform/hinata-app)
with a handful of identity values swapped. There are five things to change.

| # | What | Where |
| --- | --- | --- |
| 1 | **Package / bundle id** | `com.yourorg.yourapp` — Android `applicationId` + `namespace`, iOS/macOS `PRODUCT_BUNDLE_IDENTIFIER`, Windows `msix_config.identity_name` + `publisher`, Linux `APPLICATION_ID` + `BINARY_NAME` in `linux/CMakeLists.txt` |
| 2 | **App display name** | Android `android:label`, iOS/macOS display name, Windows `msix_config.display_name`, Linux `Name=` in the desktop entry |
| 3 | **Icons & splash** | `assets/branding/` + `flutter_launcher_icons` / `flutter_native_splash`; Linux takes a 512×512 PNG from `packaging/linux/` |
| 4 | **Accent color** | the honey-amber `#D9A032` accent token in the theme |
| 5 | **Gateway** | point at the Hinata Connect gateway (or your own) |

### 1 — Package / bundle id

Pick a reverse-DNS identifier you own, e.g. `com.yourorg.yourapp`, and set it
everywhere:

```kotlin
// android/app/build.gradle.kts
android {
    namespace = "com.yourorg.yourapp"
    defaultConfig {
        applicationId = "com.yourorg.yourapp"
    }
}
```

For iOS and macOS, set `PRODUCT_BUNDLE_IDENTIFIER` in the Xcode project (Runner
target). This id is permanent once published to a store — choose carefully.

Windows identifies an MSIX package differently: `identity_name`, `publisher` and
`publisher_display_name` in the `msix_config` block of `pubspec.yaml` are
**assigned to you by Partner Center** (Product management → Product identity).
Copy them character-exact — the Store rejects the package on any mismatch.

Linux keeps its identity in `linux/CMakeLists.txt` — the GTK application id, and
the name of the binary that lands in the bundle:

```cmake
# linux/CMakeLists.txt
set(BINARY_NAME "yourapp")
set(APPLICATION_ID "com.yourorg.yourapp")
```

The application id reaches further than the process, though. It is also the
basename of the desktop entry (`com.yourorg.yourapp.desktop`), the
`StartupWMClass` inside it, the `<id>` of the AppStream metainfo, the Flatpak
`app-id` and the bus name in the snap's `dbus` slot — AppStream and the desktop
shells tie those files together by that one string. Leave a single occurrence behind and the shell shows your app with a
generic icon, or the store listing never matches what is installed. The binary
name travels too: `Exec=` in the desktop entry, `<provides><binary>` in the
metainfo, and the `command:` of the Flatpak and of the snap.

!!! note "Why the Linux packaging files sit outside `linux/`"
    In hinata-app the desktop entry, the icon, the AppStream metainfo and the
    snap, Flatpak and AppImage recipes live in `packaging/linux/`, not in
    `linux/`.
    `flutter create --platforms=linux .` rewrites everything under `linux/`, and
    hand-maintained packaging inputs have no business in the blast radius of a
    regenerate. Keeping them in one directory also means every format —
    Flatpak, AppImage, a distro package, a plain `install` — ships the identical
    files.

### 2 — App display name

Set the visible name shown under the icon:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<application android:label="Your App Name" ... >
```

On iOS/macOS set the display name in the Runner target's Info settings; on Windows
set `msix_config.display_name` in `pubspec.yaml`.

On Linux the visible name is `Name=` in the desktop entry, alongside
`GenericName` and `Comment` — all three take localized variants
(`Comment[de]=…`), which is how the launcher shows a German user German text.
Set `<name>` and `<summary>` in the AppStream metainfo to match: those are what
GNOME Software and KDE Discover put on the listing.

### 3 — Icons & splash

Drop your artwork into `assets/branding/` (app icon, adaptive foreground,
splash) and regenerate the native assets with the tooling already wired into
`pubspec.yaml`:

```bash
dart run flutter_launcher_icons        # regenerate app icons (android/ios/web/macos)
dart run flutter_native_splash:create  # regenerate splash screens
```

The `flutter_launcher_icons` and `flutter_native_splash` blocks in `pubspec.yaml`
control the source images and background colors (light `#F4F3EF`, dark `#131119`
by default) — edit them to your brand, then re-run the generators.

Windows takes its tile and taskbar icon from `msix_config.logo_path` instead.
Point it at a **rounded** variant of your icon: Windows applies no mask of its
own, so a full-bleed square icon shows as a hard square on the tile.

Linux is the target the generators skip. `flutter_launcher_icons` writes the
Android, iOS, web and macOS assets; the Linux icon is a plain **512×512 PNG**
you install yourself, named after the application id — in hinata-app that is
`packaging/linux/icons/hicolor/512x512/apps/com.ahmadre.hinata.png`. Use the
same rounded artwork you gave Windows: neither GNOME nor KDE masks app icons
either, so a full-bleed square reads as a hard square there too. There is no
splash screen to generate — the GTK window appears when the app is ready.

### 4 — Accent color

The signature honey-amber accent lives as a color token in the theme
(`lib/core/theme/app_colors.dart`, `accent = Color(0xFFD9A032)`). Change it to
your brand color; the token is consumed app-wide, so a single edit re-tints
buttons, highlights and active states. Pick a hue with enough contrast to read in
**both** light and dark mode.

### 5 — Point at a gateway

Push notifications and universal links are relayed through the
[Hinata Connect gateway](/en/connect-gateway.html), so self-hosters need no
Firebase project of their own. A branded app you publish yourself owns its own
push credentials and link domain, so you run your own gateway and point your
server at it with `HINATA_GATEWAY_BASE_URL`.

## Deep links & universal links

To make `https://track.example.com/...` links open your app instead of a browser
tab, you serve two association files and declare the capability in the app.

- **Android App Links** — an `assetlinks.json` served at
  `https://track.example.com/.well-known/assetlinks.json`, listing your
  `package_name` and the **SHA-256 fingerprints of your release signing key**.
- **iOS Universal Links** — an `apple-app-site-association` (AASA) file served at
  `https://track.example.com/.well-known/apple-app-site-association`, listing your
  `appID` (`TEAMID.com.yourorg.yourapp`) and the URL paths to capture.

Both files are served by the **web image**, so hosting them is automatic once the
web app runs at your domain. Example `assetlinks.json`:

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.yourorg.yourapp",
      "sha256_cert_fingerprints": [
        "AA:BB:CC:...:release-signing-key-sha256"
      ]
    }
  }
]
```

!!! warning "Use your release key's SHA-256, not the debug key"
    Android verifies App Links against the fingerprint of the key that **signed
    the installed APK/AAB**. List your Play release (upload) signing key's SHA-256
    in `assetlinks.json`, or links will silently fall back to the browser. You can
    list several fingerprints (debug, upload, Play-managed) side by side.

!!! info "iOS needs the Associated Domains capability"
    Universal Links only work if the app declares the domain in its
    **Associated Domains** entitlement (`applinks:track.example.com`) and that
    capability is enabled in the provisioning profile. Without it, iOS never
    fetches your AASA file.

### Linux: your own URL scheme

Linux has no counterpart to App Links or Universal Links — `assetlinks.json` and
the AASA file are Android and Apple mechanisms, and nothing in freedesktop
answers to them. An `https://track.example.com/...` link therefore opens in the
browser, and the page offers the route into the app from there.

The custom scheme is what does work, and it works well: the desktop entry claims
the scheme, and the client is a **single-instance** GTK application, so an SSO
callback, an invite or a password reset opens in the window the user is already
signed in to instead of starting a second copy.

```ini
# com.yourorg.yourapp.desktop
Exec=yourapp %u
MimeType=x-scheme-handler/yourscheme;
```

A rebranded client needs its **own** scheme. `hinata://` belongs to the
published app, and two installed apps claiming one scheme is a coin toss over
which of them the desktop hands the link to. Change it everywhere it is claimed
— the Android intent filter, `CFBundleURLSchemes` on iOS and macOS, the
`MimeType=` line above — and in the client code that matches an incoming URI.

Register and verify the handler after installing the desktop entry:

```bash
update-desktop-database ~/.local/share/applications
xdg-mime default com.yourorg.yourapp.desktop x-scheme-handler/yourscheme
xdg-mime query default x-scheme-handler/yourscheme

xdg-open 'yourscheme://verify-email?token=test'   # once with the app running,
                                                  # once with it closed
```

!!! tip "Test both entrances"
    A warm start hands the URI to the running instance over D-Bus; a cold start
    passes it in as a process argument before any plugin is registered. They are
    genuinely different code paths, so try the link with the app open and with
    it closed.

## Store releases need a privacy policy

Apple's App Store, Google Play and the Microsoft Store all require a reachable
**privacy policy** URL for review, and you need one for GDPR/DSGVO compliance
anyway. Hinata surfaces this URL in the app from the server setting
`HINATA_PRIVACY_POLICY_URL` (also editable live in the
[Admin area](/en/admin-area.html) → App settings). Set it before you submit.

Linux has no gatekeeper of that kind — an AppImage or your own Flatpak remote
answers to nobody. A store does. The **Snap Store** reviews what a strictly
confined snap asks for, by hand where a request is privileged, and Flathub
generates its listing from your AppStream metainfo, so that file needs a name, a
summary, a description, the licence, an OARS content rating and at least one
screenshot at a stable, hosted URL.

Hinata itself ships Linux through the Snap Store and not through Flathub, whose
[submission requirements](https://docs.flathub.org/docs/for-app-authors/requirements)
exclude applications whose content was produced with an LLM. If your fork keeps
Hinata's screens and copy, that applies to it too.

!!! tip "Accessibility is part of compliance"
    The UI is built to be accessibility-minded — scalable text, semantic widgets
    and sufficient contrast. Keep that in mind when you choose your accent color
    and any custom copy.

## Branding checklist

Work top to bottom; each step is independent.

1. **Fork** [hinata-app](https://github.com/hinata-platform/hinata-app) and honor GPL-3.0.
2. Set the **package/bundle id** (`com.yourorg.yourapp`) on Android, iOS and macOS,
   the **MSIX identity** from Partner Center on Windows, and `APPLICATION_ID` +
   `BINARY_NAME` in `linux/CMakeLists.txt` — then rename the Linux desktop entry,
   the metainfo `<id>`, the Flatpak `app-id` and the snap's `dbus` slot `name` to
   match it. The snap's own `name:` is a separate, store-wide identifier you
   register at snapcraft.io.
3. Set the **app display name** on every platform, including `Name=` in the Linux
   desktop entry and `<name>` in the metainfo.
4. Replace the artwork in `assets/branding/` and run the icon + splash generators;
   point `msix_config.logo_path` at a rounded icon for Windows, and install the same
   rounded icon as a 512×512 PNG under `packaging/linux/icons/…`.
5. Change the **accent color** token in the theme; verify light **and** dark mode.
6. Decide your **gateway** — default, or your own via `HINATA_GATEWAY_BASE_URL`.
7. Serve `assetlinks.json` + AASA at `https://track.example.com/.well-known/`
   (the web image does this) and list your **release key SHA-256**.
8. Enable the **Associated Domains** capability for iOS Universal Links, and claim
   your own `x-scheme-handler/` scheme in the Linux desktop entry.
9. Set **`HINATA_PRIVACY_POLICY_URL`** on the server.
10. Build, sign and submit to the stores.

## Where to go next

- [The apps](/en/clients.html) — how the client connects, gates versions and manages servers.
- [Hinata Connect gateway](/en/connect-gateway.html) — push + universal-link relay.
- [Configuration reference](/en/configuration.html) — every server setting.
