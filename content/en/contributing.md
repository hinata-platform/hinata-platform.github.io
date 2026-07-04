---
title: Contributing
description: How to contribute to Hinata — the two repositories, coding conventions, the i18n requirement, commit style, and how to report issues or open a pull request.
---

# Contributing

Hinata is **open source under the GPL-3.0 license**, and contributions are very
welcome — bug reports, translations, docs, and code all move the project forward.
This page explains where the code lives, how to get set up, and the conventions
that keep pull requests easy to review and merge.

You do not need to be an expert to help. A clear bug report, a fix for a typo, or a
small improvement to a German string is a genuinely useful contribution.

## The two repositories

Hinata is split into a server and a client, each with its own issue tracker and
pull requests:

| Repository | What it is | Link |
| --- | --- | --- |
| **hinata-server** | Spring Boot 4 / Java 21 REST API, MongoDB, S3/MinIO, SMTP. | [github.com/hinata-platform/hinata-server](https://github.com/hinata-platform/hinata-server) |
| **hinata-app** | The Flutter client — Android, iOS, Web, macOS from one codebase. | [github.com/hinata-platform/hinata-app](https://github.com/hinata-platform/hinata-app) |

Open your issue or pull request against the repository that owns the code you are
changing. A change that spans both (a new endpoint plus its UI) is two coordinated
PRs — mention each in the other so a reviewer can follow the thread.

## Getting set up

The fastest way to a running dev environment is the [Development](/en/development.html)
page — it covers JDK 21 and the Compose infrastructure for the server, and the
Flutter toolchain for the app, plus the exact commands. In short:

```bash
# Server
docker compose -f docker-compose.dev.yml up -d
./mvnw spring-boot:run

# App
flutter pub get
flutter run
```

Before you open a PR, make sure the quality gates pass locally — they are the same
checks CI runs:

```bash
./mvnw verify              # server
flutter analyze && flutter test   # app
```

## Coding conventions

- **Match the surrounding code.** Follow the style already in the file you are
  editing; do not reformat unrelated lines.
- **Server** — idiomatic Spring Boot: controllers stay thin, business rules live in
  services, data access in repositories. Keep authorization checks and localized
  error keys where the existing code puts them.
- **App** — the feature-first, one-directional flow described in
  [Development](/en/development.html): screens dispatch to a **bloc/cubit**, which
  calls **`HinataRepository`**, which uses the **`ApiClient`**. Do not call `dio`
  from a widget.
- **Icons** — the app uses **Lucide icons only** (`lucide_icons_flutter`), never
  Material or Cupertino icon sets.
- **Keep changes focused.** One logical change per PR is far easier to review than a
  large mixed diff.

### The i18n requirement (non-negotiable)

The app is multilingual and ships **English and German**. Every user-facing string
must exist as a key in **both** languages and be resolved through the localization
layer — never hardcoded in a widget.

!!! warning "Every new UI string needs an en + de key"
    When you add text, add the key to **both** `assets/i18n/en/` **and**
    `assets/i18n/de/` and render it via the translation function. A PR that
    introduces a bare string, or adds an English key without its German counterpart,
    will be asked to fix it. A missing key silently renders the raw key name to
    users.

If you do not speak German, still add the German key — a best-effort translation
that a reviewer or a native speaker can refine is far better than a missing key. See
[Development → Internationalization](/en/development.html).

## Commit and pull-request style

- Write commit messages in the imperative mood and describe the change in
  **neutral, product-owned terms** — describe *what the feature does*, e.g.
  "add issue linking", rather than naming another product's UI.
- Keep the subject line short; use the body to explain the *why* when it is not
  obvious.
- In the PR description, say what changed and why, and how you verified it. Link the
  issue it addresses. If the change is visible in the UI, a screenshot helps a lot.
- Make sure CI is green (build, analyze, tests) before requesting review.

## Reporting issues

A good bug report saves everyone time. When you open an issue, include:

- **What you expected** and **what actually happened**.
- **Steps to reproduce** — the smaller and more precise, the better.
- **Environment** — server image tag / app version, platform (Android, iOS, web,
  macOS), and anything relevant about your deployment (reverse proxy, SSO provider).
- Relevant **logs or error messages** — but **redact secrets** (tokens, passwords,
  connection strings) before pasting.

Check the [FAQ & troubleshooting](/en/faq.html) first — many "bugs" are
configuration issues with a known fix (CORS, proxy buffering, mail relay, trusted
proxies).

!!! danger "Never include secrets in a public issue"
    Do not paste real JWT secrets, database passwords, OAuth client secrets or
    access tokens into an issue, PR or screenshot. If a secret has been exposed,
    rotate it.

## License

By contributing, you agree that your contributions are licensed under the project's
**GPL-3.0** license, the same terms as the rest of Hinata. See the `LICENSE` file in
each repository.

## Where to go next

- [Development](/en/development.html) — full local setup, project layout and CI.
- [API reference](/en/api.html) — the REST surface you may be extending.
- [FAQ & troubleshooting](/en/faq.html) — common issues and their fixes.
