---
title: Download
description: Get the Hinata app for Android, iOS, macOS, Windows, Linux or the web — where each build comes from, what it can do on that platform, and what you need before you sign in.
---

# Download Hinata

Hinata is a client for **your own server**, so installing the app is only half of
it: the first thing it asks for is a server URL. If nobody has set one up for you
yet, start with [Self-hosting](/en/self-hosting.html) — it takes a Docker Compose
file and a few minutes.

The app is one Flutter codebase compiled six ways. The same screens, the same
data, the same shortcuts, wherever you open it.

## Get the app

<ul class="plat-grid">
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg><strong>Android</strong></span>
  <span class="plat-status live">Available</span>
  <p>Phone and tablet, with push notifications and the full offline-friendly navigation.</p>
  <span class="plat-actions">
    <a href="https://play.google.com/store/apps/details?id=com.ahmadre.hinata"><img class="b-play" src="/assets/img/badges/google-play.png" alt="Get it on Google Play"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg><strong>iOS</strong></span>
  <span class="plat-status soon">In review</span>
  <p>The iPhone and iPad build is with App Review. The listing below is live already — it serves the Mac app until iOS is approved.</p>
  <span class="plat-actions">
    <a class="plat-link" href="https://apps.apple.com/us/app/hinata/id6781889251">View the listing</a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/></svg><strong>macOS</strong></span>
  <span class="plat-status live">Available</span>
  <p>A native desktop client, notarised and distributed through the Mac App Store.</p>
  <span class="plat-actions">
    <a href="https://apps.apple.com/us/app/hinata/id6781889251"><img class="b-apple" src="/assets/img/badges/mac-app-store.svg" alt="Download on the Mac App Store"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg><strong>Windows</strong></span>
  <span class="plat-status live">Available</span>
  <p>Packaged as an MSIX, with push delivered over Windows Push Notification Services.</p>
  <span class="plat-actions">
    <a href="https://apps.microsoft.com/detail/9N5NVNPKBBLR"><img class="b-ms" src="/assets/img/badges/microsoft-store.svg" alt="Get it from Microsoft"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg><strong>Linux</strong></span>
  <span class="plat-status soon">In review</span>
  <p>A native GTK 3 client, uploaded to the store as a strictly confined snap for amd64 and arm64 — but no revision is on a channel yet, so there is nothing to install and no store page to link. <code>snap info hinata</code> is the check; it errors while none is published. Until one is, the Flatpak and AppImage recipes in the repository build the same app.</p>
  <span class="plat-actions">
    <a class="plat-link" href="/en/clients.html#hinata-on-linux">What the status is</a>
    <a class="plat-link" href="https://github.com/hinata-platform/hinata-app/tree/main/packaging/linux">Build it yourself</a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg><strong>Web</strong></span>
  <span class="plat-status live">Included</span>
  <p>Nothing to install. Your server ships the web app itself — open its address and sign in.</p>
  <span class="plat-actions">
    <a class="plat-link" href="/en/self-hosting.html">How to host it</a>
  </span>
</li>
</ul>

!!! info "One app, many servers"
    A published Hinata app has **no server address compiled into it**. The same
    build from the same store connects to your company's server, your club's
    server and a local test instance — each with its own saved session. See
    [The apps](/en/clients.html) for the Server Manager that keeps them apart.

## What each platform can do

Almost everything is identical everywhere. These are the differences worth
knowing before you choose where to work, and each one has a reason rather than a
roadmap entry.

| | Android | iOS | macOS | Windows | Linux | Web |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| Boards, sprints, issues, Gantt, reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Push notifications | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| In-app & e-mail notifications | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Take a photo with the camera | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Attach files you already have | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Record a voice comment | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Stay signed in across restarts | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| `hinata://` deep links | ✅ | ✅ | ✅ | ✅ | ✅ | — |

⚠️ means it works once the system provides something the app cannot ship itself.
On Linux, staying signed in needs a keyring (GNOME Keyring, KWallet — anything
implementing the Secret Service), and voice comments need the GStreamer plugin
packages to play and PulseAudio plus FFmpeg to record. The app names the missing
piece instead of failing quietly. [The apps](/en/clients.html#hinata-on-linux)
has the detail and the package lists.

!!! note "Why Linux has no push"
    Push on mobile and Windows is relayed through the
    [Hinata Connect gateway](/en/connect-gateway.html) to FCM and WNS. A Linux
    desktop has no equivalent service to register a token with — so notifications
    arrive in the app and by e-mail instead. Your notification settings stay
    editable there anyway: the preferences belong to your **account**, not to the
    machine you happen to be sitting at, and they still govern your phone.

## After you install

1. **Enter your server URL.** The app checks it answers before it continues, so
   you can never end up half-connected to something that is not a Hinata server.
2. **Sign in** with your credentials, or through whatever
   [single sign-on](/en/sso.html) your operator configured.
3. That is it — the workspace is the same one you will find on every other
   device.

!!! tip "Told to update?"
    When a server requires a newer client than you have, the app says so and
    offers a button straight to the right place for your platform. Operators set
    those links per platform in the admin area, so the button goes to the store
    you actually installed from.

New to Hinata? The [User guide](/en/guide-start.html) walks through the app
screen by screen.
