---
title: Introduction
description: Hinata is an open-source, self-hosted, white-label project and issue tracker — no user, team or board limits, ever. Meet the platform.
---

# Hinata

Hinata is an **independent, open-source, self-hosted project & issue tracker** — a modern alternative to hosted trackers that you run entirely on your own infrastructure. It is a **white-label** platform: operators run their own server and can ship their own branded client. Licensed under **GPL-3.0**, current platform version **2.2.0**.

No user limits. No team limits. No board limits. Ever. What you self-host is yours.

!!! tip "Two ways in"
    New here? Jump straight to the [Quick start](/en/quick-start.html) to get a stack running in three commands. Ready to run it for real? Head to [Self-hosting](/en/self-hosting.html) for the production path.

## What is Hinata?

Hinata is a full agile project-management suite: projects and teams, issues with a real Epic → Story → Sub-task hierarchy, agile boards, sprints, a Gantt timeline, time tracking, reports, and a Confluence-style knowledge base. It is built to feel modern and fast, and to be operated by a single team on a single server — or scaled out behind a reverse proxy for an entire organization.

Two things make it different from most self-hosted trackers:

- **It ships a real cross-platform app.** Not just a web UI — a single Flutter codebase compiled for Android, iOS, Web and macOS, with live updates over Server-Sent Events, offline-friendly navigation, and a ⌘K command palette.
- **It is white-label by design.** The server is decoupled from the client. You can point the published app at your own server, save and switch between multiple servers, or build and publish your own branded client with your package id, name, icons and accent color.

!!! info "Design language"
    Hinata wears a navy navigation rail, a warm-paper workspace, and a honey-amber accent (`#D9A032`) that reads the same in light and dark. Liquid-glass surfaces appear on the mobile navigation, the ⌘K palette and the attachment lightbox. It is meant to be a joy to look at every day.

## Who it's for

- **Self-hosters & privacy-first teams** who want their project data on hardware they control, under a copyleft license, with no seat-based pricing.
- **Agencies and product studios** who want to ship a branded tracker to their own clients — same engine, your brand.
- **Operators & platform teams** who need real infrastructure controls: MongoDB replica sets, S3 object storage, SMTP, SSO, rate limiting and an audited security model.
- **Developers** who value an approachable, well-documented codebase (Spring Boot 4 + Flutter) they can read, extend and contribute to.

## The two repositories

Hinata is split into two open-source repositories:

| Repository | What it is | Stack |
| --- | --- | --- |
| [hinata-server](https://github.com/hinata-platform/hinata-server) | The backend API, business logic and data layer. Publishes a Docker image to GHCR. | Spring Boot 4, Java 21, MongoDB (replica set), S3/MinIO, SMTP |
| [hinata-app](https://github.com/hinata-platform/hinata-app) | The client for every platform, from one codebase. | Flutter, bloc/cubit, go_router, dio, i18next (en + de), fl_chart |

The app talks to the server over a versioned REST API at `/api/v1`. See [Architecture](/en/architecture.html) for how the pieces fit together.

## Platforms

One Flutter codebase, four targets:

- **Android** — phones and tablets, App Links for `https://track.example.com`.
- **iOS** — iPhone and iPad, Universal Links via Associated Domains.
- **Web** — a full-featured Flutter-web build served by the web container.
- **macOS** — a native desktop client.

## What's inside

A tour of the platform, each with a deeper page:

- **[Projects & teams](/en/projects-teams.html)** — per-project workflows and issue keys (like `ASTA-42`), reusable colored labels, and teams whose per-member project access gates what each person can even see.
- **[Issues & hierarchy](/en/issues.html)** — types, priorities, tags, comments, attachments and dependencies, with a Jira-style three-level hierarchy: **Epic → Story/Task/Bug/Feature → Sub-task**.
- **[Boards & sprints](/en/boards-sprints.html)** — agile boards with columns mapped to workflow states, WIP limits and a backlog, plus a Board / Backlog / Timeline switcher and full sprint planning with burndown.
- **[Gantt & time tracking](/en/timeline.html)** — a timeline read model with start/due dates and dependencies, and work items with activity types and weekly timesheets.
- **[Reports & dashboard](/en/reports.html)** — burndown, velocity, cycle time, distributions and created-vs-resolved, exportable to PDF, plus a focus dashboard.
- **[Knowledge base](/en/knowledge-base.html)** — hierarchical Markdown articles, global or per project, with smart links that resolve real issues and people.
- **[Notifications](/en/notifications.html)** — in-app and e-mail, plus push delivered through the Hinata Connect gateway.
- **[Search & palette](/en/search.html)** — a ⌘K liquid-glass command palette with triggers, recents and a responsive sheet.
- **[Git integration](/en/git-integration.html)** — connect projects to GitHub, GitLab or Bitbucket for real development info, smart commits and workflow automation.
- **[Single sign-on](/en/sso.html)** — OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP, configured at runtime with no restart.

Want the full walkthrough? Read the [Feature tour](/en/features.html).

## Why self-host Hinata

!!! note "The short version"
    You own the server, the data and the brand. It's GPL-3.0, so it stays open. There are no seat limits or paywalled features, and everything from SSO to push works without handing your data to a third party.

- **Your data, your rules.** Everything lives in your MongoDB and your S3 bucket. Attachments use randomized object keys and presigned downloads.
- **No Firebase required.** Push notifications and universal links are relayed through the [Hinata Connect gateway](/en/connect-gateway.html), so a single published app can serve many servers and self-hosters need no Firebase project of their own.
- **Runtime configuration.** SSO, e-mail ingest, push and Git OAuth apps are stored in MongoDB and managed from the Admin area — the database overrides the environment, and changes apply **without a restart**.
- **Serious security.** Stateless JWT (HS512), BCrypt password hashing, database-backed login blocking, per-IP rate limiting, hardened HTTP headers and a model mapped to the OWASP Top 10. See the [Security model](/en/security.html).

## Get started

<div class="cta-row">

Two clear paths, depending on what you need next:

</div>

- **[Get started →](/en/quick-start.html)** — the fastest path to a running server and app, in three commands with Docker Compose.
- **[Self-host it →](/en/self-hosting.html)** — the production path: deployment, configuration, database, storage, mail and reverse proxy.

!!! tip "Prefer to understand the moving parts first?"
    Read [Architecture](/en/architecture.html) for the data-flow picture and [Core concepts](/en/concepts.html) for the vocabulary — organizations, projects, issues, sprints, teams and more.
