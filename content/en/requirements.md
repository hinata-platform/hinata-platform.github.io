---
title: Requirements
description: What you need to self-host Hinata — host sizing, Docker Engine + Compose v2, network and TLS, MongoDB replica set, S3/MinIO, SMTP, and dev prerequisites.
---

# Requirements

Hinata runs comfortably on a single modest server and scales up from there. This page lists what the host needs, what each component expects, and what you'll want for building from source.

## Host requirements

The server and its dependencies ship as containers, so the host mainly needs a container runtime and enough headroom to run the JVM, MongoDB and MinIO side by side.

| Resource | Minimum | Recommended |
| --- | --- | --- |
| **CPU** | 2 cores (x86_64 or arm64) | 4+ cores |
| **RAM** | 4 GB | 8 GB+ (the JVM + a 3-member replica set are the main consumers) |
| **Disk** | 20 GB SSD | 50 GB+ SSD, growing with attachments and database size |
| **OS** | Any Linux with a modern kernel | A stable server distro you patch regularly |

- **Docker Engine + Docker Compose v2** are the only hard software prerequisites. The Compose files use v2 syntax (`docker compose`, not the legacy `docker-compose`).
- **Architecture**: images are published for **x86_64** and **arm64**, so Apple Silicon, AWS Graviton and Raspberry Pi-class arm64 boxes all work.

!!! note "Attachments drive disk growth"
    The database itself stays lean; the variable is object storage. Attachments and avatars live in S3/MinIO, so size the volume behind MinIO (or your external bucket) for how much your teams will upload over time.

## Component requirements

A production Hinata stack is a handful of cooperating services. Here's what each one needs.

| Component | What it needs | Notes |
| --- | --- | --- |
| **Server (Spring Boot)** | JVM runtime (in the image), the env from `.env` | Publishes the API; host port `3356` by default |
| **MongoDB** | A **replica set** (2 data nodes + 1 arbiter) in prod, with TLS + X.509 | Runtime settings and all data live here |
| **S3 / MinIO** | An S3-compatible bucket (default name `hinata`) + credentials | Attachments, avatars; presigned downloads |
| **SMTP relay** | A real outbound mail relay in prod (Mailpit in dev) | Verification, notifications, password reset |
| **Reverse proxy** | Terminates TLS, forwards to the server/app ports | Public DNS + certificate; see below |
| **Hinata Connect gateway** | *Optional* — the hosted gateway, or your own | Push notifications + universal links |

### Network

- **Public DNS + TLS.** For anything beyond a local test you need public DNS names and TLS. Terminate TLS at a [reverse proxy](/en/reverse-proxy.html) and forward to Hinata over the internal ports. Typical names are `api.track.example.com` (API) and `track.example.com` (web app).
- **Internal ports.** The server publishes **`3356`** and the web/app container **`3456`** by default (`HINATA_PORT` / `HINATA_APP_PORT`). These are the ports your proxy forwards to; they should not be exposed directly to the internet.
- **Trusted proxies.** Set `HINATA_TRUSTED_PROXIES` to the CIDRs of your reverse proxies so `X-Forwarded-For` is honored only from them. Empty means trust none.
- **CORS.** The hosted web app calls the API cross-origin, so list your browser origins in `HINATA_CORS_ALLOWED_ORIGINS`.

!!! warning "Terminate TLS in front, always"
    The internal ports (`3356`/`3456`) speak plain HTTP and are meant to sit behind a TLS-terminating proxy. Never expose them directly. The app requires `https://` for saved production servers.

### MongoDB replica set

Production Hinata expects a **replica set**, not a standalone MongoDB, for two reasons: it's required for the transactional guarantees Hinata relies on, and it enables safe rolling operation. The shipped Compose brings up **2 data nodes + 1 arbiter** with **TLS and X.509 client authentication**. The app authenticates to MongoDB with an X.509 certificate — not the SCRAM root password, which is reserved for internal/admin use.

- Generate the cluster keyfile with `./deploy/generate-secrets.sh`.
- Generate the production PKI with `./deploy/x509/generate-certs.sh prod`, then create the X.509 user with `./deploy/x509/init-prod-user.sh`.

Full detail lives in [MongoDB & X.509](/en/database.html).

### Object storage

Hinata needs an object store. The bundled MinIO is the easy default (bucket `HINATA_S3_BUCKET`, default `hinata`), configured with `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`; in dev, `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` are also used. You can point Hinata at any external S3-compatible provider (AWS S3, Google Cloud Storage, Cloudflare R2, DigitalOcean Spaces, …) or at Azure Blob Storage (`HINATA_STORAGE_PROVIDER=azure`) instead. See [Object storage](/en/storage.html).

### SMTP

For real mail — e-mail verification, notifications and password reset — configure an outbound **SMTP relay** with `HINATA_SMTP_HOST/PORT/USERNAME/PASSWORD/AUTH/STARTTLS` and a sensible `HINATA_MAIL_FROM`. In development, **Mailpit** captures everything at `http://localhost:8025` so nothing leaves the machine. See [E-mail & SMTP](/en/email.html).

### Hinata Connect gateway (optional)

Push notifications and universal links flow through the **Connect gateway**, a hosted service. Using it means self-hosters need **no Firebase project of their own**. It's optional; you can run without push, or ship your own branded app with your own gateway and set `HINATA_GATEWAY_BASE_URL`. See [Hinata Connect gateway](/en/connect-gateway.html).

## Client requirements

The [app](/en/clients.html) runs on:

- **Android** and **iOS** phones/tablets,
- **Web** (any modern browser),
- **macOS** desktop,
- **Windows** desktop,
- **Linux** desktop — a native GTK 3 build, installed as a Flatpak, as an AppImage, or from a bundle you built yourself.

Because the app is multi-server, users just need the URL of a running server; no per-user install configuration is required.

### What a Linux desktop needs

The Linux client links against the system's GTK, GStreamer and libsecret instead of bundling its own copies — that is why it wears your theme and plays with the codecs your distribution installed. The other side of that trade is that it expects an ordinary desktop underneath. Everything below is already there on a stock GNOME or Plasma install; the list matters for containers, minimal window managers and stripped-down images.

| Package (Debian/Ubuntu names) | Needed for | Without it |
| --- | --- | --- |
| `libgtk-3-0` | the app itself | it does not start |
| `libsecret-1-0` plus a keyring (GNOME Keyring, KWallet — anything speaking the Secret Service) | staying signed in across restarts | the session lives only until the app closes, and the app tells the user so |
| `zenity`, `qarma` or `kdialog` | the file picker for attachments | the picker names which of the three to install |
| `pulseaudio-utils` and `ffmpeg` | recording a voice comment | the recorder does not start |
| `gstreamer1.0-plugins-base/good/bad` and `gstreamer1.0-libav` | playing a voice comment | playback fails with the missing package named |

`gstreamer1.0-libav` is the one that looks optional and is not: voice comments are recorded as AAC on every platform, and libav carries the decoder for it. Without it a voice bubble loads and then refuses to play.

!!! note "The Flatpak brings nearly all of this with it"
    The Flatpak sits on the Freedesktop runtime, which already carries GTK, zenity, GStreamer including libav, libsecret and FFmpeg, and it builds PulseAudio's recording tools into the package itself. The keyring is the piece that still comes from the host — it belongs to the user's login session, not to the sandbox.

!!! info "Two things Linux does not do"
    There are **no push notifications**: `firebase_messaging` has no Linux implementation and there is no desktop push service to register with, so notifications arrive in the app and by e-mail. And there is **no webcam capture** — no camera implementation exists for Linux, so the app does not offer "take a photo" at all rather than failing when it is tapped. Attaching files that already exist works exactly as everywhere else.

## Development requirements

Building from source (rather than pulling images) needs the toolchains behind each repo:

- **[hinata-server](https://github.com/hinata-platform/hinata-server)** — **JDK 21** and the bundled Gradle wrapper (`./gradlew`). Bring up the dev dependencies with `docker compose -f docker-compose.dev.yml up -d` (Mongo replica set, Mailpit, MinIO), then run the server:

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

Run the test suite with `./gradlew build`.

- **[hinata-app](https://github.com/hinata-platform/hinata-app)** — a **Flutter** SDK plus the native toolchain of every target you build: the Android SDK, Xcode for iOS and macOS, Visual Studio with the desktop C++ workload for Windows, and the GTK development packages for Linux. State via bloc/cubit, routing via go_router, i18n via i18next.

### Building the Linux desktop target

The Linux build compiles against system libraries instead of bundling them, so install their headers first — on Debian or Ubuntu:

```bash
sudo apt install \
  clang cmake ninja-build pkg-config \
  libgtk-3-dev liblzma-dev libsecret-1-dev libjsoncpp-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

Then build it like any other target:

```bash
flutter config --enable-linux-desktop
flutter build linux --release
```

Every package earns its place: `libgtk-3-dev` is the embedder and brings the GTK printing support behind print and PDF export, `libsecret-1-dev` backs the secure token storage that keeps a session alive, and the GStreamer headers build the audio playback voice comments need. A **Rust** toolchain ([rustup](https://rustup.rs)) is required too — the rich clipboard and drag-and-drop plugin is a Rust crate compiled from source on Linux rather than shipped prebuilt.

The result is a relocatable `build/linux/<arch>/release/bundle/` directory — the `hinata` binary next to `data/` and `lib/` — which is exactly what the Flatpak and AppImage recipes in `packaging/linux/` package.

!!! note "Build Linux on the oldest distribution you intend to support"
    A Flutter bundle is dynamically linked against the glibc of the machine that built it, and glibc is only forward compatible — a binary built on a brand-new distribution refuses to start on an older one. Hinata's CI pins `ubuntu-22.04` for its Linux job for exactly that reason, so the bundle's glibc floor is a decision rather than an accident.

!!! tip "Just want it running?"
    You don't need JDK or Flutter to *operate* Hinata — the [Quick start](/en/quick-start.html) pulls prebuilt images. The development toolchains are only for building from source or contributing. See [Development](/en/development.html) and [Contributing](/en/contributing.html).

## Next steps

- [Quick start](/en/quick-start.html) — three commands to a running stack.
- [Production deployment](/en/deployment.html) — the full production path.
- [Reverse proxy & TLS](/en/reverse-proxy.html) — public DNS, certificates and forwarding.
