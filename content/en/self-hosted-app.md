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
| 1 | **Package / bundle id** | `com.yourorg.yourapp` — Android `applicationId` + `namespace`, iOS/macOS `PRODUCT_BUNDLE_IDENTIFIER` |
| 2 | **App display name** | Android `android:label`, iOS/macOS display name |
| 3 | **Icons & splash** | `assets/branding/` + `flutter_launcher_icons` / `flutter_native_splash` |
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

### 2 — App display name

Set the visible name shown under the icon:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<application android:label="Your App Name" ... >
```

On iOS/macOS set the display name in the Runner target's Info settings.

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

### 4 — Accent color

The signature honey-amber accent lives as a color token in the theme
(`lib/core/theme/app_colors.dart`, `accent = Color(0xFFD9A032)`). Change it to
your brand color; the token is consumed app-wide, so a single edit re-tints
buttons, highlights and active states. Pick a hue with enough contrast to read in
**both** light and dark mode.

### 5 — Point at a gateway

Push notifications and universal links are relayed through the
[Hinata Connect gateway](/en/connect-gateway.html), so self-hosters need no
Firebase project of their own. Your branded app registers against a gateway; use
the default public gateway or run your own and set `HINATA_GATEWAY_BASE_URL` on
your server. The server registers itself with the gateway on boot.

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

## Store releases need a privacy policy

Both Apple's App Store and Google Play require a reachable **privacy policy** URL
for review, and you need one for GDPR/DSGVO compliance anyway. Hinata surfaces
this URL in the app from the server setting `HINATA_PRIVACY_POLICY_URL` (also
editable live in the [Admin area](/en/admin-area.html) → App settings). Set it
before you submit.

!!! tip "Accessibility is part of compliance"
    The UI is built to be accessibility-minded — scalable text, semantic widgets
    and sufficient contrast. Keep that in mind when you choose your accent color
    and any custom copy.

## Branding checklist

Work top to bottom; each step is independent.

1. **Fork** [hinata-app](https://github.com/hinata-platform/hinata-app) and honor GPL-3.0.
2. Set the **package/bundle id** (`com.yourorg.yourapp`) on Android, iOS and macOS.
3. Set the **app display name** on every platform.
4. Replace the artwork in `assets/branding/` and run the icon + splash generators.
5. Change the **accent color** token in the theme; verify light **and** dark mode.
6. Decide your **gateway** — default, or your own via `HINATA_GATEWAY_BASE_URL`.
7. Serve `assetlinks.json` + AASA at `https://track.example.com/.well-known/`
   (the web image does this) and list your **release key SHA-256**.
8. Enable the **Associated Domains** capability for iOS Universal Links.
9. Set **`HINATA_PRIVACY_POLICY_URL`** on the server.
10. Build, sign and submit to the stores.

## Where to go next

- [The apps](/en/clients.html) — how the client connects, gates versions and manages servers.
- [Hinata Connect gateway](/en/connect-gateway.html) — push + universal-link relay.
- [Configuration reference](/en/configuration.html) — every server setting.
