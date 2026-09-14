---
title: Development
description: Set up the server (Spring Boot, Java 21) and app (Flutter) locally, run tests, and learn the layout and CI.
---

# Development

This gets server and app running on your machine. Hinata has two repositories.
Set up the server first, since that's what the app talks to.

- **Server**: [`github.com/hinata-platform/hinata-server`](https://github.com/hinata-platform/hinata-server)
- **App**: [`github.com/hinata-platform/hinata-app`](https://github.com/hinata-platform/hinata-app)

## Server (Spring Boot, Java 21)

### Prerequisites

- **JDK 21** (CI uses Temurin).
- **Docker** with Compose, for the local infrastructure.
- No global Gradle. The repo ships the Gradle Wrapper (`./gradlew`).

### 1. Start the infrastructure

A dedicated Compose file starts only the services the server needs: a MongoDB
replica set, Mailpit (a local SMTP catcher) and MinIO (S3-compatible storage).
You run the server itself from your IDE or the wrapper.

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
```

| Service | URL | What it is |
| --- | --- | --- |
| **Mailpit** | `http://localhost:8025` | Catches all outbound mail. Read verification, reset and notification e-mails here. |
| **MinIO console** | `http://localhost:9001` | Shows the bucket with attachments and avatars. |
| **MongoDB** | `localhost:27017` | Replica set `rs0`, reached with `directConnection=true`. |

### 2. Run the server

Point the server at the local Mongo and MinIO and start it:

```bash
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

!!! tip "Seed a realistic demo workspace"
    With `HINATA_DEMO_SEED=true` you get an English demo workspace with projects,
    issues, sprints and a knowledge base. First-run setup is done, and you're
    logged in as `rebar` / `hinata-demo-2026`. The seeder is annotated
    `@Profile("!prod")` and is compiled out of production builds entirely.

### 3. Run the tests

One command, the same one CI runs:

```bash
./gradlew build
```

!!! info "Dev vs prod profiles"
    Locally you use the `dev` Spring profile (standalone Mongo). Production uses
    `prod` (a replica set with TLS and X.509). You almost never need that
    locally. If you do, see [MongoDB & X.509](/en/database.html).

## App (Flutter)

### Prerequisites

- The **Flutter toolchain** on the stable channel, same as CI. Run
  `flutter doctor` and fix what it flags for your target platforms.
- You only need SDKs for the platforms you build.
- **Android:** Android Studio / SDK.
- **iOS and macOS:** Xcode.
- **Windows:** Visual Studio with the *Desktop development with C++* workload.
- **Web:** nothing extra.

### Run it

```bash
flutter pub get
flutter run
```

`flutter run` uses the connected device. To pick a target:

```bash
flutter run -d chrome    # web
flutter run -d macos     # macOS desktop
flutter run -d windows   # Windows desktop
flutter devices          # list attached devices/emulators
```

On first launch the app asks for your **server URL**. Use your local server:

- Desktop / web / iOS simulator: `http://localhost:8080`
- Android emulator: `http://10.0.2.2:8080` (the emulator's alias for your host)

### Quality gate

The same checks CI runs:

```bash
flutter analyze && flutter test
```

### Internationalization (i18n)

**Every user-facing string must be translated.** The app ships English and
German. Strings live in i18next JSON under `assets/i18n/{en,de}/` and are read
through the localization layer, never hardcoded in a widget.

!!! warning "Every new string needs en + de"
    New UI text needs the key in **both** `assets/i18n/en/` **and**
    `assets/i18n/de/`. Resolve it via the translation function. A missing key
    silently renders the raw key string. This is required for every PR that
    touches the UI, see [Contributing](/en/contributing.html).

## Project layout

The app is organized **feature-first**. Each feature owns its screens and state.
Shared code lives under `core/`. Data flows in one direction:

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

A screen never talks to `dio` directly:

1. The screen dispatches to a **bloc/cubit**.
2. The bloc calls a method on **`HinataRepository`**.
3. The repository uses the **`ApiClient`**.

Only the `ApiClient` handles the Bearer token, automatic refresh and the
`Accept-Language` header. Live changes arrive over **SSE** and update the
relevant bloc.

## CI/CD

Both repositories use **GitHub Actions**.

**Server** (`ci.yml`):

- Every push and pull request runs `./gradlew build`.
- Pushes to `main` and version tags (`v*`) **publish a Docker image to the
  GitHub Container Registry (GHCR)** under `ghcr.io/hinata-platform`. Tagged
  `latest` on `main`, and with the semantic version on tags.

**App** (`ci.yml`):

- Every push and pull request runs `flutter analyze` and `flutter test`, and
  builds the web release.
- Pushes to `main` and `v*` tags publish the Flutter **web** image to GHCR.
- A separate release workflow builds the mobile apps for the stores.

!!! note "The image tags you deploy"
    Operators pull the GHCR images by tag via `HINATA_SERVER_TAG` and
    `HINATA_APP_TAG` in the deployment `.env` (default `latest`). See
    [Production deployment](/en/deployment.html).

## Where to go next

- [Contributing](/en/contributing.html): conventions, i18n rules, commit style and PRs.
- [API reference](/en/api.html): the REST API and how to enable the Scalar docs UI locally.
- [Architecture](/en/architecture.html): how app, server and infrastructure fit together.
- [Configuration reference](/en/configuration.html): every environment variable.
