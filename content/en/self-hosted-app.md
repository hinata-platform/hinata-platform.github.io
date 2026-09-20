---
title: Branding & custom clients
description: Runtime branding from your server, and how to build your own Hinata client if you want one.
---

# Branding & custom clients

Hinata follows the **one app, self-hosted servers** model you know from
Rocket.Chat or Nextcloud. You run your own server, and the published Hinata app
connects to it.

- The native app has **no baked-in server URL**. Users bring their own server.
- Branding (organization name and logo) comes from the server at runtime via
  `/api/v1/meta`.
- Push and universal links work for every instance through the
  [Hinata Connect gateway](/en/connect-gateway.html).

So most operators never need to build anything. If you still want your own
client under your own store listing, you are free to build and publish one. This
page shows how.

!!! note "Open source, GPL-3.0"
    The client is licensed **GPL-3.0**. You may rebrand, modify and distribute
    it, provided you honor the license. Above all, make your corresponding source
    available to your users under the same terms.

## The zero-build option: the hosted web app

First check whether you need a native app at all. The server repository ships
`docker-compose.app.yml`, an overlay that serves the compiled Flutter **web**
client as static files at your own domain, e.g. `https://track.example.com`.

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

Users get a branded URL in the browser with **nothing to install and nothing to
build**. The web build talks to the API it is configured for. Many operators run
only this and let mobile users use the published apps. You only need a custom
native build for your own store presence, icon and name.

## What you change

A custom client is a fork of [hinata-app](https://github.com/hinata-platform/hinata-app)
with a handful of identity values swapped. There are five things to change.

| # | What | Where |
| --- | --- | --- |
| 1 | **Package / bundle id** | `com.yourorg.yourapp`: Android `applicationId` + `namespace`, iOS/macOS `PRODUCT_BUNDLE_IDENTIFIER`, Windows `msix_config.identity_name` + `publisher`, Linux `APPLICATION_ID` + `BINARY_NAME` in `linux/CMakeLists.txt` |
| 2 | **App display name** | Android `android:label`, iOS/macOS display name, Windows `msix_config.display_name`, Linux `Name=` in the desktop entry |
| 3 | **Icons & splash** | `assets/branding/` + `flutter_launcher_icons` / `flutter_native_splash`; Linux takes a 512×512 PNG from `packaging/linux/` |
| 4 | **Accent color** | the honey amber `#D9A032` accent token in the theme |
| 5 | **Gateway** | point at the Hinata Connect gateway (or your own) |

### 1. Package and bundle id

Pick a reverse-DNS identifier you own, e.g. `com.yourorg.yourapp`, and set it
everywhere.

```kotlin
// android/app/build.gradle.kts
android {
    namespace = "com.yourorg.yourapp"
    defaultConfig {
        applicationId = "com.yourorg.yourapp"
    }
}
```

On iOS and macOS, set `PRODUCT_BUNDLE_IDENTIFIER` in the Xcode project (Runner
target). The id is permanent once published to a store, so choose carefully.

On Windows, **Partner Center assigns** `identity_name`, `publisher` and
`publisher_display_name` for the `msix_config` block in `pubspec.yaml` (Product
management → Product identity). Copy them character-exact, or the Store rejects
the package.

On Linux, the GTK application id and the binary name live in
`linux/CMakeLists.txt`:

```cmake
# linux/CMakeLists.txt
set(BINARY_NAME "yourapp")
set(APPLICATION_ID "com.yourorg.yourapp")
```

The application id appears in more places. AppStream and the desktop shells tie
these files together by that one string:

- the basename of the desktop entry (`com.yourorg.yourapp.desktop`) and the
  `StartupWMClass` inside it
- the `<id>` of the AppStream metainfo
- the Flatpak `app-id`
- the bus name in the snap's `dbus` slot

Miss one and the shell shows your app with a generic icon, or the store listing
never matches what is installed.

The binary name appears in `Exec=` in the desktop entry, `<provides><binary>` in
the metainfo, and the `command:` of the Flatpak and the snap.

!!! note "Why the Linux packaging files sit outside `linux/`"
    In hinata-app the desktop entry, the icon, the AppStream metainfo and the
    snap, Flatpak and AppImage recipes live in `packaging/linux/`.
    `flutter create --platforms=linux .` rewrites everything under `linux/` and
    would overwrite hand-maintained files. One shared directory also means
    every format (Flatpak, AppImage, a distro package, a plain `install`) ships
    the identical files.

### 2. App display name

Set the name shown under the icon:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<application android:label="Your App Name" ... >
```

On iOS/macOS set the display name in the Runner target's Info settings. On
Windows set `msix_config.display_name` in `pubspec.yaml`.

On Linux the visible name is `Name=` in the desktop entry, alongside
`GenericName` and `Comment`. All three take localized variants
(`Comment[de]=…`), so the launcher shows German text to a German user. Set
`<name>` and `<summary>` in the AppStream metainfo to match. GNOME Software and
KDE Discover show those on the listing.

### 3. Icons & splash

Put your artwork (app icon, adaptive foreground, splash) into `assets/branding/`
and regenerate the native assets with the tooling already wired into
`pubspec.yaml`:

```bash
dart run flutter_launcher_icons        # regenerate app icons (android/ios/web/macos)
dart run flutter_native_splash:create  # regenerate splash screens
```

The `flutter_launcher_icons` and `flutter_native_splash` blocks in `pubspec.yaml`
control the source images and background colors (defaults: light `#F4F3EF`, dark
`#131119`). Edit them to your brand, then run the generators again.

Windows takes its tile and taskbar icon from `msix_config.logo_path`. Point it
at a **rounded** variant of your icon. Windows applies no mask, so a full-bleed
square icon shows as a hard square on the tile.

Linux is the target the generators skip. `flutter_launcher_icons` writes the
Android, iOS, web and macOS assets only. The Linux icon is a plain **512×512
PNG** you install yourself, named after the application id. In hinata-app that is
`packaging/linux/icons/hicolor/512x512/apps/com.ahmadre.hinata.png`.

Use the same rounded artwork you gave Windows, because GNOME and KDE do not mask
app icons either. There is no splash screen on Linux. The GTK window appears
when the app is ready.

### 4. Accent color

The honey amber accent is a color token in the theme
(`lib/core/theme/app_colors.dart`, `accent = Color(0xFFD9A032)`). Change it to
your brand color. The token is used app-wide, so one edit re-tints buttons,
highlights and active states. Pick a hue with enough contrast for **both** light
and dark mode.

### 5. Point at a gateway

Push notifications and universal links are relayed through the
[Hinata Connect gateway](/en/connect-gateway.html), so self-hosters need no
Firebase project of their own.

A branded app you publish yourself owns its own push credentials and link
domain. You then run your own gateway and point your server at it with
`HINATA_GATEWAY_BASE_URL`.

## Deep links & universal links

To make `https://track.example.com/...` links open your app instead of a browser
tab, serve two association files and declare the capability in the app.

- **Android App Links:** an `assetlinks.json` served at
  `https://track.example.com/.well-known/assetlinks.json`, listing your
  `package_name` and the **SHA-256 fingerprints of your release signing key**.
- **iOS Universal Links:** an `apple-app-site-association` (AASA) file served at
  `https://track.example.com/.well-known/apple-app-site-association`, listing your
  `appID` (`TEAMID.com.yourorg.yourapp`) and the URL paths to capture.

The **web image** serves both files once the web app runs at your domain.
Example `assetlinks.json`:

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

!!! warning "Use your release key's SHA-256"
    Android verifies App Links against the fingerprint of the key that **signed
    the installed APK/AAB**. List your Play release (upload) signing key's
    SHA-256 in `assetlinks.json`, or links silently fall back to the browser.
    You can list several fingerprints (debug, upload, Play-managed) side by
    side.

!!! info "iOS needs the Associated Domains capability"
    Universal Links only work if the app declares the domain in its
    **Associated Domains** entitlement (`applinks:track.example.com`) and that
    capability is enabled in the provisioning profile. Without it, iOS never
    fetches your AASA file.

### Linux: your own URL scheme

Linux has no counterpart to App Links or Universal Links. `assetlinks.json` and
the AASA file are Android and Apple mechanisms, and nothing in freedesktop
answers to them. An `https://track.example.com/...` link therefore opens in the
browser, and the page offers the route into the app from there.

A custom scheme works well, though. The desktop entry claims the scheme, and the
client is a **single-instance** GTK application. An SSO callback, an invite or a
password reset opens in the window the user is already signed in to, without
starting a second copy.

```ini
# com.yourorg.yourapp.desktop
Exec=yourapp %u
MimeType=x-scheme-handler/yourscheme;
```

A rebranded client needs its **own** scheme. `hinata://` belongs to the
published app. If two installed apps claim one scheme, it is a coin toss which
one gets the link. Change it everywhere it is claimed:

- the Android intent filter
- `CFBundleURLSchemes` on iOS and macOS
- the `MimeType=` line above
- the client code that matches an incoming URI

Register and verify the handler after installing the desktop entry:

```bash
update-desktop-database ~/.local/share/applications
xdg-mime default com.yourorg.yourapp.desktop x-scheme-handler/yourscheme
xdg-mime query default x-scheme-handler/yourscheme

xdg-open 'yourscheme://verify-email?token=test'   # once with the app running,
                                                  # once with it closed
```

!!! tip "Test both entrances"
    A warm start hands the URI to the running instance over D-Bus. A cold start
    passes it in as a process argument before any plugin is registered. These
    are different code paths, so try the link with the app open and with it
    closed.

## Store releases need a privacy policy

Apple's App Store, Google Play and the Microsoft Store all require a reachable
**privacy policy** URL for review, and you need one for GDPR/DSGVO compliance
anyway. Hinata shows this URL in the app from the server setting
`HINATA_PRIVACY_POLICY_URL` (also editable live in the
[Admin area](/en/admin-area.html) → Platform). Set it before you submit.

An AppImage or your own Flatpak remote goes through no review. Stores do:

- The **Snap Store** reviews what a strictly confined snap asks for, by hand
  where a request is privileged.
- **Flathub** generates its listing from your AppStream metainfo. That file then
  needs a name, a summary, a description, the licence, an OARS content rating and
  at least one screenshot at a stable, hosted URL.

Hinata itself is not offered on Flathub. On Linux it ships through the Snap
Store.

!!! tip "Accessibility is part of compliance"
    The UI is built with accessibility in mind: scalable text, semantic widgets
    and sufficient contrast. Keep that in mind when you choose your accent color
    and any custom copy.

## Branding checklist

Work top to bottom. Each step is independent.

1. **Fork** [hinata-app](https://github.com/hinata-platform/hinata-app) and honor GPL-3.0.
2. Set the **package/bundle id** (`com.yourorg.yourapp`) on Android, iOS and macOS,
   the **MSIX identity** from Partner Center on Windows, and `APPLICATION_ID` +
   `BINARY_NAME` in `linux/CMakeLists.txt`. Then rename the Linux desktop entry,
   the metainfo `<id>`, the Flatpak `app-id` and the snap's `dbus` slot `name` to
   match. The snap's own `name:` is a separate, store-wide identifier you
   register at snapcraft.io.
3. Set the **app display name** on every platform, including `Name=` in the Linux
   desktop entry and `<name>` in the metainfo.
4. Replace the artwork in `assets/branding/` and run the icon and splash
   generators. Point `msix_config.logo_path` at a rounded icon for Windows, and
   install the same rounded icon as a 512×512 PNG under `packaging/linux/icons/…`.
5. Change the **accent color** token in the theme and check light **and** dark mode.
6. Choose your **gateway**: the default, or your own via `HINATA_GATEWAY_BASE_URL`.
7. Serve `assetlinks.json` and AASA at `https://track.example.com/.well-known/`
   (the web image does this) and list your **release key SHA-256**.
8. Enable the **Associated Domains** capability for iOS Universal Links, and claim
   your own `x-scheme-handler/` scheme in the Linux desktop entry.
9. Set **`HINATA_PRIVACY_POLICY_URL`** on the server.
10. Build, sign and submit to the stores.

## Where to go next

- [The apps](/en/clients.html): how the client connects, gates versions and manages servers.
- [Hinata Connect gateway](/en/connect-gateway.html): relay for push and universal links.
- [Configuration reference](/en/configuration.html): every server setting.
