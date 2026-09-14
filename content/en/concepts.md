---
title: Core concepts
description: The key terms in Hinata, from the organization to the knowledge base.
---

# Core concepts

This page explains the terms Hinata is built on. It goes from the outside in: organization, projects, then the work inside them.

## Organization

The **organization** is the top-level container on a Hinata server. It has a name, branding and the people in it.

- You create it on first run in the [setup wizard](/en/setup-wizard.html), or with `HINATA_SETUP_ORGANIZATION_NAME`.
- A server hosts exactly one organization.
- For several organizations, run several servers. The [one-app, self-hosted-servers](/en/self-hosted-app.html) model supports that.

## Users & roles

A **user** is a person with an account. Sign-in uses local credentials or [SSO](/en/sso.html). There are only two roles:

- **ADMIN:** full access, including the Admin area (`/api/v1/admin/**` is ADMIN-only). That covers server settings, users, SSO, Git OAuth apps, e-mail ingest and app-level flags.
- **Regular users:** everyone else. What they see depends on **team membership and per-member project access** (below).

!!! info "Visibility is team-driven"
    Apart from ADMIN, there is no role hierarchy. A user's teams decide which projects they see. See [Teams](/en/projects-teams.html).

## Projects & project keys

A **project** is a workspace with its own issues, workflow, labels, board and members.

Each project has a short uppercase **project key**. It prefixes every issue number:

```text
ASTA-42      →  project key "ASTA", issue #42
WEB-1007     →  project key "WEB",  issue #1007
```

Numbers count up per project, so `ASTA-42` stays unambiguous forever. The key appears in URLs, and Git [smart commits](/en/git-integration.html) reference it in branch names and commit messages.

## Workflow states

A **workflow state** shows where an issue is in the process, for example *To Do → In Progress → In Review → Done*.

- States are defined **per project** and have a color.
- Each state is a `{id, name, hue}` record, keyed by name.
- You edit them in [Project settings](/en/project-settings.html). Changes start as a draft and are applied from a save bar.
- Renaming a state updates it across the whole project on the server. Existing issues follow along.

Board columns map to workflow states. Automation from Git events only moves issues **forward**, never back.

## Labels

**Labels** are colored tags per project, with the same `{id, name, hue}` shape as states. They classify issues independently of type and state, for example *backend*, *needs-design* or *customer*.

You manage them in Project settings. Renaming a label updates every issue that carries it.

## Issues

An **issue** is the smallest unit of work: a task, bug, story, feature, epic or sub-task. Every issue has:

- a **type** (see the hierarchy) and a **priority**
- **tags/labels**, **comments** and **[attachments](/en/issues.html)** (stored in S3/MinIO)
- **dependencies** on other issues
- a **workflow state**, an **assignee**, and optional **start/due dates** and **story points**

### The issue hierarchy

Hinata uses a Jira-style **three-level hierarchy**:

```text
Epic
 └─ Story / Task / Bug / Feature
     └─ Sub-task
```

- **Epic:** a large body of work spanning many issues.
- **Story / Task / Bug / Feature:** the middle level with the everyday types.
- **Sub-task:** a small piece of one parent issue.

The app gives you a breadcrumb, a parent picker, and panels for children and sub-tasks. Validation and cascade delete keep the tree consistent. Boards group issues into **swimlanes** by none / epic / assignee / subtask and filter by epic. More in [Issues & hierarchy](/en/issues.html).

## Sprints & backlog

A **sprint** is a time-boxed batch of work. You *plan → start → complete* it. It has a capacity, story points and a **burndown** report.

The **backlog** is every issue **not assigned to a sprint**. When planning, you pull issues from there into a sprint.

The [Boards & sprints](/en/boards-sprints.html) views have a Board / Backlog / Timeline switcher, a people filter and a sprint header.

## Teams & project access

A **team** is a group of people. Teams control **visibility** across the whole platform. Each team grants its members access to specific projects.

- Add someone to a team with access to *Project X*, and they see *Project X*.
- Someone in no team with access to a project never sees it.

See [Projects & teams](/en/projects-teams.html) for the full model.

## Attachments

**Attachments** are files on an issue. They live in **S3/MinIO**, not in the database.

- Object keys are random.
- Downloads use **presigned URLs**, never a long-lived public URL.
- Adding and removing is atomic on the issue document.
- With **live SSE**, everyone viewing the issue sees changes instantly.
- Size and type limits are set through environment variables.

The UI has a drag-and-drop grid and a lightbox. Details in [Object storage](/en/storage.html) and [Issues](/en/issues.html).

## Knowledge base

The **knowledge base** is a space of hierarchical **Markdown articles**, similar to Confluence.

- Articles are global or belong to a project.
- Access is controlled by team and project.
- **Smart links** resolve to real issues and people.
- The Markdown toolbar is the same as in the rest of the app.
- Data is stored in the backend via `/api/v1/articles`.

See [Knowledge base](/en/knowledge-base.html).

## Other building blocks

- **Workflow automation:** Git events (branch created, commit pushed, PR/MR opened or merged) move issues forward. See [Git integration](/en/git-integration.html).
- **Smart commits:** trailers in a commit message that act on an issue, e.g. `ASTA-42 #comment shipped`, `#time 2h 30m`, or any `#word` to transition it.
- **Time tracking:** log work with activity types against issues, rolled up into weekly timesheets. See [Gantt & time tracking](/en/timeline.html).
- **Notifications:** in the app, by e-mail, and as push via the [Connect gateway](/en/connect-gateway.html).
- **The command palette:** [search](/en/search.html) and commands with ⌘K.

!!! tip "Next step"
    The [Architecture](/en/architecture.html) shows how this data moves between app and server. To see it live, jump into the [Quick start](/en/quick-start.html).
