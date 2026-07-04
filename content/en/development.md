---
title: Development
description: Set up a local development environment for the Hinata server (Spring Boot / Java 21) and app (Flutter), run tests, and understand the project layout and CI.
---

# Development

This page gets you from a fresh clone to a running server and app on your own
machine. Hinata is two repositories — a **Spring Boot** server and a **Flutter**
client — and each has a short, predictable dev loop. Work through the server first
(it is what the app talks to), then the app.

- **Server**: [`github.com/hinata-platform/hinata-server`](https://github.com/hinata-platform/hinata-server)
- **App**: [`github.com/hinata-platform/hinata-app`](https://github.com/hinata-platform/hinata-app)

## Server (Spring Boot, Java 21)

### Prerequisites

- **JDK 21** (Temurin is what CI uses).
- **Docker** with Compose, for the local infrastructure.
- No global Maven needed — the repo ships the Maven Wrapper (`./mvnw`).

### 1. Start the infrastructure

A dedicated Compose file brings up only the backing services the server needs —
a MongoDB replica set, Mailpit (a local SMTP catcher) and MinIO (S3-compatible
storage) — so you can run the server itself from your IDE or the wrapper:

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
```

| Service | URL | What it is |
| --- | --- | --- |
| **Mailpit** | `http://localhost:8025` | Catches all outbound mail — open it to read verification / reset / notification e-mails. |
| **MinIO console** | `http://localhost:9001` | Browse the object storage bucket that holds attachments and avatars. |
| **MongoDB** | `localhost:27017` | Replica set `rs0`, reached with `directConnection=true`. |

### 2. Run the server

Point the server at the local Mongo and MinIO and start it with the wrapper:

```bash
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./mvnw spring-boot:run
```

!!! tip "Seed a realistic demo workspace"
    Add `HINATA_DEMO_SEED=true` to populate a full English demo workspace (projects,
    issues, sprints, a knowledge base) so you have something to click through.
    It also completes first-run setup and logs in as `rebar` / `hinata-demo-2026`.
    The seeder is annotated `@Profile("!prod")`, so it is compiled out of production
    builds entirely — it is a dev-only convenience.

### 3. Run the tests

The quality gate is a single command — the same one CI runs:

```bash
./mvnw verify
```

!!! info "Dev vs prod profiles"
    Local development uses the `dev` Spring profile (standalone Mongo). Production
    uses `prod` (a TLS + X.509 replica set). You almost never need the prod profile
    on your machine; see [MongoDB & X.509](/en/database.html) if you want to
    reproduce it.

## App (Flutter)

### Prerequisites

- The **Flutter toolchain** (stable channel — the same channel CI builds with).
  Run `flutter doctor` and resolve anything it flags for your target platforms.
- Platform SDKs only for the targets you build: Android Studio / SDK for Android,
  Xcode for iOS and macOS. Web needs nothing extra.

### Run it

```bash
flutter pub get
flutter run
```

`flutter run` targets whatever device is connected. To pick a target explicitly:

```bash
flutter run -d chrome    # web
flutter run -d macos     # macOS desktop
flutter devices          # list attached devices/emulators
```

On first launch the app asks for your **server URL**. Point it at your local
server:

- Desktop / web / iOS simulator: `http://localhost:8080`
- Android emulator: `http://10.0.2.2:8080` (the emulator's alias for your host)

### Quality gate

The same checks CI runs, locally:

```bash
flutter analyze && flutter test
```

### Internationalization (i18n)

Hinata is multilingual, and **every user-facing string must be translated** — the
app ships English and German. Strings live in i18next JSON under
`assets/i18n/{en,de}/` and are read through the localization layer (never hardcoded
in a widget).

!!! warning "Every new string needs en + de"
    When you add UI text, add the key to **both** `assets/i18n/en/` **and**
    `assets/i18n/de/` and resolve it via the translation function. A missing key
    silently renders the raw key string. This is a hard requirement for any PR that
    touches the UI — see [Contributing](/en/contributing.html).

## Project layout

The app follows a **feature-first** structure. Each feature owns its screens and
state; shared plumbing lives under `core/`. Data flows in one direction:

```text
Features (screens/widgets)
    │
    ▼
Bloc / Cubit            state management
    │
    ▼
HinataRepository        domain-facing data access
    │
    ▼
ApiClient (dio)         REST /api/v1, token refresh, Accept-Language
    │
    ▼
Hinata Server           Spring Boot, /api/v1  ──SSE──▶ back to Bloc
```

```text
lib/
  core/        theme, responsive system, i18n, api, models, blocs,
               router, storage, widgets
  features/    connect, setup, onboarding, auth, shell, dashboard,
               projects, issues, board, sprint, gantt, timesheet,
               reports, knowledge, search, notifications, settings, admin
packages/
  liquid_glass_widgets/   vendored glass surfaces (full control)
```

A screen never talks to `dio` directly: it dispatches to a **bloc/cubit**, which
calls a method on **`HinataRepository`**, which uses the **`ApiClient`**. That
single client is where the Bearer token, automatic refresh and the
`Accept-Language` header are handled once for the whole app. Live changes arrive
back over **SSE** and update the relevant bloc.

## CI/CD

Both repositories use **GitHub Actions**.

- **Server** (`ci.yml`): on every push and pull request, runs `./mvnw verify`.
  On pushes to `main` and on version (`v*`) tags, it builds and **publishes a Docker
  image to the GitHub Container Registry (GHCR)** under `ghcr.io/hinata-platform`,
  tagged `latest` on `main` and with the semantic version on tags.
- **App** (`ci.yml`): on every push and pull request, runs `flutter analyze` and
  `flutter test`, and builds the web release. On pushes to `main` and `v*` tags it
  publishes the compiled Flutter **web** image to GHCR. A separate release workflow
  handles store builds for the mobile apps.

!!! note "The image tags you deploy"
    Operators pull those GHCR images by tag — `HINATA_SERVER_TAG` and
    `HINATA_APP_TAG` in the deployment `.env` (default `latest`). See
    [Production deployment](/en/deployment.html).

## Where to go next

- [Contributing](/en/contributing.html) — conventions, i18n rules, commit style and how to open a PR.
- [API reference](/en/api.html) — the REST surface, and how to enable the Scalar docs UI locally.
- [Architecture](/en/architecture.html) — how the app, server and infrastructure fit together.
- [Configuration reference](/en/configuration.html) — every environment variable.
