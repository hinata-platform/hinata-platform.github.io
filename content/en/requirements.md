---
title: Requirements
description: What you need to self-host Hinata and to build it from source.
---

# Requirements

Hinata runs well on a single modest server and scales up from there. This page lists what the host, the components, the clients and development need.

## Host requirements

The server and its dependencies ship as containers. The host mainly needs a container runtime and enough headroom for the JVM, MongoDB and MinIO.

| Resource | Minimum | Recommended |
| --- | --- | --- |
| **CPU** | 2 cores (x86_64 or arm64) | 4+ cores |
| **RAM** | 4 GB | 8 GB+ (the JVM and a 3-member replica set use the most) |
| **Disk** | 20 GB SSD | 50 GB+ SSD, growing with attachments and database size |
| **OS** | Any Linux with a modern kernel | A stable server distro you patch regularly |

- **Docker Engine + Docker Compose v2** are the only hard software prerequisites. The Compose files use v2 syntax (`docker compose`, not the legacy `docker-compose`).
- **Architecture**: images are published for **x86_64** and **arm64**. Apple Silicon, AWS Graviton and Raspberry Pi class arm64 boxes all work.

!!! note "Attachments drive disk growth"
    The database stays lean. What grows is object storage: attachments and avatars live in S3/MinIO. Size the volume behind MinIO (or your external bucket) for how much your teams will upload over time.

## Component requirements

A production stack consists of these services:

| Component | What it needs | Notes |
| --- | --- | --- |
| **Server (Spring Boot)** | JVM runtime (in the image), the env from `.env` | Publishes the API. Host port `3356` by default |
| **MongoDB** | A **replica set** (2 data nodes + 1 arbiter) in prod, with TLS + X.509 | Runtime settings and all data live here |
| **S3 / MinIO** | An S3-compatible bucket (default name `hinata`) + credentials | Attachments, avatars, presigned downloads |
| **SMTP relay** | A real outbound mail relay in prod (Mailpit in dev) | Verification, notifications, password reset |
| **Reverse proxy** | Terminates TLS, forwards to the server and app ports | Public DNS + certificate, see below |
| **Hinata Connect gateway** | *Optional*: the hosted gateway, or your own | Push notifications + universal links |

### Network

- **Public DNS + TLS.** Beyond a local test you need public DNS names and TLS. Terminate TLS at a [reverse proxy](/en/reverse-proxy.html) and forward to Hinata over the internal ports. Typical names are `api.track.example.com` (API) and `track.example.com` (web app).
- **Internal ports.** By default the server publishes **`3356`** and the web/app container **`3456`** (`HINATA_PORT` / `HINATA_APP_PORT`). Your proxy forwards to these. Don't expose them directly to the internet.
- **Trusted proxies.** Set `HINATA_TRUSTED_PROXIES` to the CIDRs of your reverse proxies. `X-Forwarded-For` is honored only from them. Empty means trust none.
- **CORS.** The hosted web app calls the API cross-origin. List your browser origins in `HINATA_CORS_ALLOWED_ORIGINS`.

!!! warning "Terminate TLS in front, always"
    The internal ports (`3356`/`3456`) speak plain HTTP and belong behind a TLS-terminating proxy. Never expose them directly. The app requires `https://` for saved production servers.

### MongoDB replica set

Production Hinata needs a **replica set**, not a standalone MongoDB. It is required for the transactional guarantees Hinata relies on, and it allows safe rolling operation.

The shipped Compose brings up **2 data nodes + 1 arbiter** with **TLS and X.509 client authentication**. The app authenticates with an X.509 certificate. The SCRAM root password is reserved for internal and admin use.

- Generate the cluster keyfile: `./deploy/generate-secrets.sh`
- Generate the production PKI: `./deploy/x509/generate-certs.sh prod`, then create the X.509 user with `./deploy/x509/init-prod-user.sh`.

Full detail lives in [MongoDB & X.509](/en/database.html).

### Object storage

Hinata needs an object store:

- **Bundled MinIO** is the easy default: bucket `HINATA_S3_BUCKET` (default `hinata`), configured with `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`. In dev, `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` are also used.
- **External S3-compatible provider**: AWS S3, Google Cloud Storage, Cloudflare R2, DigitalOcean Spaces, …
- **Azure Blob Storage**: `HINATA_STORAGE_PROVIDER=azure`.

See [Object storage](/en/storage.html).

### SMTP

For e-mail verification, notifications and password reset, configure an outbound **SMTP relay** with `HINATA_SMTP_HOST/PORT/USERNAME/PASSWORD/AUTH/STARTTLS` and a sensible `HINATA_MAIL_FROM`. In development, **Mailpit** captures everything at `http://localhost:8025`, so nothing leaves the machine. See [E-mail & SMTP](/en/email.html).

### Hinata Connect gateway (optional)

Push notifications and universal links flow through the hosted **Connect gateway**. With it you need **no Firebase project of your own**. You can also run without push, or ship your own branded app with your own gateway and set `HINATA_GATEWAY_BASE_URL`. See [Hinata Connect gateway](/en/connect-gateway.html).

## Client requirements

The [app](/en/clients.html) runs on:

- **Android** and **iOS** phones and tablets,
- **Web** (any modern browser),
- **macOS**,
- **Windows**,
- **Linux** as a native GTK 3 build. The quickest way is `sudo snap install hinata` from the Snap Store (x86-64 and ARM64). The Flatpak and AppImage recipes build the same app. [The apps](/en/clients.html#hinata-on-linux) lists the two permissions the snap needs connected by hand.

The app works with multiple servers. Users only need the URL of a running server, with no further setup.

### What a Linux desktop needs

The Linux client uses the system's GTK, GStreamer and libsecret. That is why it follows your theme and uses the codecs your distribution installed. In return it expects an ordinary desktop. A stock GNOME or Plasma install already has everything. The list matters for containers, minimal window managers and stripped-down images.

| Package (Debian/Ubuntu names) | Needed for | Without it |
| --- | --- | --- |
| `libgtk-3-0` | the app itself | it does not start |
| `libsecret-1-0` plus a keyring (GNOME Keyring, KWallet or anything speaking the Secret Service) | staying signed in across restarts | the session ends when the app closes (the app tells the user) |
| `zenity`, `qarma` or `kdialog` | the file picker for attachments | the picker names which of the three to install |
| `pulseaudio-utils` and `ffmpeg` | recording a voice comment | the recorder does not start |
| `gstreamer1.0-plugins-base/good/bad` and `gstreamer1.0-libav` | playing a voice comment | playback fails with the missing package named |

`gstreamer1.0-libav` is required too. Voice comments are recorded as AAC on every platform, and libav carries the decoder. Without it a voice bubble loads but won't play.

!!! note "The packaged builds bring nearly all of this with them"

    - **Flatpak**: the Freedesktop runtime already carries GTK, zenity, GStreamer including libav, libsecret and FFmpeg. The package builds PulseAudio's recording tools in itself.
    - **Snap**: it sits on the GNOME platform snap and stages `gstreamer1.0-plugins-bad`, `gstreamer1.0-libav`, `pulseaudio-utils` and `ffmpeg` into the package. It picks files through the desktop portal, so it needs no `zenity`.

    In both cases the keyring comes from the host, because it belongs to the user's login session, not to the sandbox. Under the snap it needs `snap connect hinata:password-manager-service`, and recording needs `snap connect hinata:audio-record`.

!!! info "Two things Linux does not do"

    - There are **no push notifications**. `firebase_messaging` has no Linux implementation and there is no desktop push service to register with. Notifications arrive in the app and by e-mail.
    - There is **no webcam capture**. No camera implementation exists for Linux, so the app does not offer "take a photo" at all. Attaching existing files works as everywhere else.

## Development requirements

Building from source needs the toolchains behind each repo:

- **[hinata-server](https://github.com/hinata-platform/hinata-server)**: **JDK 21** and the bundled Gradle wrapper (`./gradlew`). Bring up the dev dependencies (Mongo replica set, Mailpit, MinIO), then run the server:

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

Run the test suite with `./gradlew build`.

- **[hinata-app](https://github.com/hinata-platform/hinata-app)**: a **Flutter** SDK plus the native toolchain of every target you build. That means the Android SDK, Xcode for iOS and macOS, Visual Studio with the desktop C++ workload for Windows, and the GTK development packages for Linux. State via bloc/cubit, routing via go_router, i18n via i18next.

### Building the Linux desktop target

The Linux build compiles against system libraries. Install their headers first, on Debian or Ubuntu:

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

What the packages are for:

- `libgtk-3-dev`: the embedder, including the GTK printing support behind print and PDF export.
- `libsecret-1-dev`: secure token storage, which keeps a session alive.
- GStreamer headers: audio playback for voice comments.

You also need a **Rust** toolchain ([rustup](https://rustup.rs)). The clipboard and drag and drop plugin is a Rust crate compiled from source on Linux.

The result is a relocatable `build/linux/<arch>/release/bundle/` directory with the `hinata` binary next to `data/` and `lib/`. The Flatpak and AppImage recipes in `packaging/linux/` package exactly that.

!!! note "Build Linux on the oldest distribution you intend to support"
    A Flutter bundle is dynamically linked against the glibc of the machine that built it. glibc is only forward compatible: a binary built on a new distribution won't start on an older one. Hinata's CI pins `ubuntu-22.04` for its Linux job for that reason, so the bundle's glibc floor is chosen on purpose.

!!! tip "Just want it running?"
    You don't need JDK or Flutter to *operate* Hinata. The [Quick start](/en/quick-start.html) pulls prebuilt images. The toolchains are only for building from source or contributing. See [Development](/en/development.html) and [Contributing](/en/contributing.html).

## Next steps

- [Quick start](/en/quick-start.html): three commands to a running stack.
- [Production deployment](/en/deployment.html): the full production path.
- [Reverse proxy & TLS](/en/reverse-proxy.html): public DNS, certificates and forwarding.
