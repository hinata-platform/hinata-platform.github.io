---
title: Core concepts
description: The vocabulary of Hinata — organizations, projects and keys, workflow states, issues and hierarchy, sprints, teams, roles, attachments and the knowledge base.
---

# Core concepts

This page is a glossary of the ideas Hinata is built from. Read it once and the rest of the docs — and the app itself — will read much more easily. Concepts are grouped roughly from the outside in: organization first, then projects, then the work inside them.

## Organization

The **organization** is the top-level container for everything on a Hinata server — its name, branding and the people in it. You create it during the [setup wizard](/en/setup-wizard.html) on first run (or seed it with `HINATA_SETUP_ORGANIZATION_NAME`). A server hosts a single organization; running several independent organizations means running several servers, which the [one-app, self-hosted-servers](/en/self-hosted-app.html) model supports cleanly.

## Users & roles

A **user** is a person with an account. Authentication can be local credentials or [SSO](/en/sso.html). Roles are deliberately simple:

- **ADMIN** — full access, including the Admin area (`/api/v1/admin/**` is ADMIN-only): server settings, users, SSO, Git OAuth apps, e-mail ingest and app-level flags.
- **Regular users** — everyone else. What they can see is governed not by a global role but by **team membership and per-member project access** (below).

!!! info "Visibility is team-driven"
    Beyond the ADMIN role, Hinata does not use a broad role hierarchy. A user's reach across the platform is decided by which projects their team memberships grant them. See [Teams](/en/projects-teams.html).

## Projects & project keys

A **project** is a workspace for a stream of work — its own issues, workflow, labels, board and members. Each project has a short, uppercase **project key** that prefixes every issue number to make a human-readable, stable identifier:

```text
ASTA-42      →  project key "ASTA", issue #42
WEB-1007     →  project key "WEB",  issue #1007
```

Issue numbers are sequential within a project, so `ASTA-42` is unambiguous forever, appears in URLs, and is what Git [smart commits](/en/git-integration.html) reference in branch and commit-message text.

## Workflow states

A **workflow state** is a column in a project's process — where an issue *is* in its lifecycle (for example *To Do → In Progress → In Review → Done*). States are defined **per project** and are colored: each is a `{id, name, hue}` record, name-keyed, and edited in [Project settings](/en/project-settings.html) with a draft + save-bar editor. Renaming a state cascades across the project on the server so existing issues follow along.

Board columns map onto workflow states; automation (from Git events) moves issues **forward** through these states, never backward.

## Labels

**Labels** are reusable, colored tags scoped to a project — the same `{id, name, hue}` shape as workflow states. They classify issues (for example *backend*, *needs-design*, *customer*) independently of type or state, and are managed in Project settings. Because labels are project-scoped and name-keyed, renaming one updates every issue that carries it.

## Issues

An **issue** is the atomic unit of work — a task, bug, story, feature, epic or sub-task. Every issue carries:

- a **type** (see the hierarchy below) and a **priority**;
- **tags/labels**, **comments** and **[attachments](/en/issues.html)** (stored in S3/MinIO);
- **dependencies** on other issues;
- a **workflow state**, an **assignee**, and optional **start/due dates** and **story points**.

### The issue hierarchy

Hinata uses a Jira-style **three-level hierarchy**:

```text
Epic
 └─ Story / Task / Bug / Feature
     └─ Sub-task
```

- **Epic** — a large body of work spanning many issues.
- **Story / Task / Bug / Feature** — the mid level, the everyday issue types.
- **Sub-task** — a small piece of a single parent issue.

The app supports this with a breadcrumb, a parent picker, and child / sub-task panels, plus validation and cascade delete so the tree stays consistent. Boards can group issues into **swimlanes** by none / epic / assignee / subtask, with epic filtering. Read more in [Issues & hierarchy](/en/issues.html).

## Sprints & backlog

A **sprint** is a time-boxed batch of work you *plan → start → complete*, with a capacity and story points and a **burndown** report. The **backlog** is simply the set of issues **not assigned to any sprint** — your pool of upcoming work. You pull issues from the backlog into a sprint when planning. The [Boards & sprints](/en/boards-sprints.html) views offer a Board / Backlog / Timeline switcher, a people filter and a sprint header.

## Teams & project access

A **team** is a group of people, and it is the mechanism that controls **visibility** across the whole platform. Each team grants its members access to specific projects; a member only sees the projects their team access allows. This means:

- adding someone to a team with access to *Project X* makes *Project X* visible to them;
- a person outside any team granting a project simply never sees that project.

Per-member project access gates app-wide visibility. See [Projects & teams](/en/projects-teams.html) for the full model.

## Attachments

**Attachments** are files bound to an issue, stored in **S3/MinIO** rather than the database. They use randomized object keys and **presigned downloads** (the bytes never route through a long-lived public URL), atomic push/pull on the issue document, and **live SSE** so additions and removals appear instantly for everyone viewing the issue. Size and type limits are driven by environment configuration. The UI is a drag-drop grid with a glass lightbox. Details in [Object storage](/en/storage.html) and [Issues](/en/issues.html).

## Knowledge base

The **knowledge base** is a Confluence-style space of hierarchical **Markdown articles**, either global or scoped to a project, with team/project access control. Articles support **smart links** that resolve to real issues and people, and share the same Markdown toolbar as the rest of the app. It is fully backend-backed via `/api/v1/articles`. See [Knowledge base](/en/knowledge-base.html).

## Other building blocks

A few more terms you'll meet across the docs:

- **Workflow automation** — Git events (branch created, commit pushed, PR/MR opened/merged) move issues forward through workflow states. See [Git integration](/en/git-integration.html).
- **Smart commits** — trailers in a commit message that act on an issue (`ASTA-42 #comment shipped`, `#time 2h 30m`, or any `#word` to transition it).
- **Time tracking** — work items logged against issues with activity types, rolled up into weekly timesheets. See [Gantt & time tracking](/en/timeline.html).
- **Notifications** — in-app and e-mail alerts, plus push via the [Connect gateway](/en/connect-gateway.html).
- **The command palette** — the ⌘K liquid-glass [search](/en/search.html) and command surface.

!!! tip "Next step"
    Now that the vocabulary is in place, see the [Architecture](/en/architecture.html) for how these concepts move over the wire, or jump into the [Quick start](/en/quick-start.html) to see them live.
