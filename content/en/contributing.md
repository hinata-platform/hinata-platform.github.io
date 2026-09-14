---
title: Contributing
description: How to contribute to Hinata, with the repositories, conventions, translations, commits and bug reports.
---

# Contributing

Hinata is **open source under the GPL-3.0 license**. Contributions are welcome: bug reports, translations, docs and code.

You do not need to be an expert. A clear bug report, a typo fix or a better German string already helps.

## The two repositories

Server and client each have their own issues and pull requests.

| Repository | What it is | Link |
| --- | --- | --- |
| **hinata-server** | Spring Boot 4 / Java 21 REST API, MongoDB, S3/MinIO, SMTP. | [github.com/hinata-platform/hinata-server](https://github.com/hinata-platform/hinata-server) |
| **hinata-app** | The Flutter client for Android, iOS, Web, macOS, Windows and Linux from one codebase. | [github.com/hinata-platform/hinata-app](https://github.com/hinata-platform/hinata-app) |

Open your issue or PR in the repository that owns the code you change. If a change touches both (say, a new endpoint plus its UI), open two PRs and link them to each other.

## Getting set up

The full guide is on the [Development](/en/development.html) page: JDK 21 and Compose for the server, the Flutter toolchain for the app. In short:

```bash
# Server
docker compose -f docker-compose.dev.yml up -d
./gradlew bootRun

# App
flutter pub get
flutter run
```

Before you open a PR, run the same checks CI runs:

```bash
./gradlew build                   # server
flutter analyze && flutter test   # app
```

## Coding conventions

- **Match the surrounding code.** Follow the style of the file and do not reformat unrelated lines.
- **Server:** idiomatic Spring Boot. Controllers stay thin, business rules live in services, data access in repositories. Keep authorization checks and localized error keys where the existing code puts them.
- **App:** the feature-first, one-directional flow from [Development](/en/development.html). Screens dispatch to a **bloc/cubit**, which calls **`HinataRepository`**, which uses the **`ApiClient`**. Never call `dio` from a widget.
- **Icons:** **Lucide icons only** (`lucide_icons_flutter`), never Material or Cupertino.
- **Small PRs.** One logical change per PR is far easier to review than a large mixed diff.

### Translations are required

The app ships in **English and German**. Every user-facing string needs a key in **both** languages and goes through the localization layer. Strings hardcoded in a widget are not accepted.

!!! warning "Every new string needs an en and de key"
    Add the key to `assets/i18n/en/` **and** `assets/i18n/de/` and render it via the translation function. PRs with a bare string or without the German key will be sent back. A missing key shows users the raw key name.

Don't speak German? Add the German key anyway. A rough translation is far better than a missing key, and someone can refine it later. See [Development → Internationalization](/en/development.html).

## Commits and pull requests

- Write commit messages in the imperative, using **neutral terms from Hinata itself**. Describe *what the feature does*, e.g. "add issue linking". Don't name another product's UI.
- Keep the subject line short. Put the *why* in the body when it isn't obvious.
- The PR description says what changed, why, and how you verified it. Link the issue. For visible changes, a screenshot helps a lot.
- Request review only once CI is green (build, analyze, tests).

## Reporting issues

A good issue includes:

- **What you expected** and **what actually happened**.
- **Steps to reproduce**, as short and precise as possible.
- **Environment:** server image tag or app version, platform (Android, iOS, web, macOS, Windows, Linux) and anything relevant about your deployment (reverse proxy, SSO provider).
- **On Linux, also:** distribution, desktop session (GNOME or Plasma, X11 or Wayland) and how you installed the app (snap, Flatpak, AppImage or your own `flutter build linux`). The file picker, keyring and audio tools come from the system, so these facts are often half the bug report.
- **Logs or error messages**, but **redact secrets** first (tokens, passwords, connection strings).

Check the [FAQ & troubleshooting](/en/faq.html) first. Many "bugs" are known configuration issues (CORS, proxy buffering, mail relay, trusted proxies).

!!! danger "Never include secrets in a public issue"
    Do not paste real JWT secrets, database passwords, OAuth client secrets or access tokens into an issue, PR or screenshot. If a secret was exposed, rotate it.

## License

By contributing, you agree that your contributions are licensed under the project's **GPL-3.0** license, like the rest of Hinata. See the `LICENSE` file in each repository.

## Where to go next

- [Development](/en/development.html): local setup, project layout and CI.
- [API reference](/en/api.html): the REST surface you may be extending.
- [FAQ & troubleshooting](/en/faq.html): common issues and their fixes.
