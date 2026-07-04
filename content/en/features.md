---
title: Feature tour
description: A guided tour of everything Hinata does — dashboard, projects, issues, boards, sprints, Gantt, time tracking, knowledge base, notifications, search, Git and SSO.
---

# Feature tour

Hinata is a full agile project-management suite in one place: plan work, run sprints, track time, write documentation and keep everyone in sync — from a single self-hosted server and a cross-platform app. This page is the map. Each area gets a one-paragraph tour and a link to its detailed guide.

!!! tip "New to Hinata?"
    If you just want to get a stack running, start with the [Quick start](/en/quick-start.html). If you want to understand the vocabulary first — organizations, projects, issues, sprints, teams — read [Core concepts](/en/concepts.html).


![Hinata dashboard](/assets/img/shot-dashboard.png)
*One platform: dashboard, boards, sprints, Gantt, reports, knowledge base and more.*

## The feature map

| Area | What it does | Guide |
| --- | --- | --- |
| **Dashboard & reports** | Your focus for today, completion and team ranking, plus burndown, velocity, cycle-time and distribution charts you can export to PDF. | [Reports & dashboard](/en/reports.html) |
| **Projects & teams** | Projects with their own keys (`ASTA-42`), workflows and colored labels; teams that grant per-member project access and decide what each person can even see. | [Projects & teams](/en/projects-teams.html) |
| **Issues & hierarchy** | The core work item — types, priorities, labels, Markdown descriptions, comments, attachments and dependencies — in a three-level Epic → Story → Sub-task hierarchy. | [Issues & hierarchy](/en/issues.html) |
| **Boards & sprints** | An agile board with columns mapped to your workflow states, WIP limits, swimlanes and a backlog; plan, start and complete sprints with capacity and burndown. | [Boards & sprints](/en/boards-sprints.html) |
| **Gantt & time tracking** | A timeline view of start/due dates and dependencies, plus work logging with activity types and weekly timesheets. | [Gantt & time tracking](/en/timeline.html) |
| **Knowledge base** | Confluence-style hierarchical Markdown articles, global or per project, with smart links that resolve real issues and people. | [Knowledge base](/en/knowledge-base.html) |
| **Notifications** | In-app and e-mail notifications, plus mobile push delivered through the Hinata Connect gateway — no Firebase project of your own required. | [Notifications](/en/notifications.html) |
| **Search & palette** | A ⌘K liquid-glass command palette to jump anywhere, run commands and reopen recent items, with a responsive sheet on mobile. | [Search & palette](/en/search.html) |
| **Git integration** | Connect projects to GitHub, GitLab or Bitbucket for real development info, smart commits and workflow automation driven by signed webhooks. | [Git integration](/en/git-integration.html) |
| **Single sign-on** | OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP, configured at runtime from the Admin area with no restart. | [SSO](/en/sso.html) |

## Dashboard & reports

The dashboard is where each person lands: today's focus, a completion view, a weekly tracker and a friendly team ranking. Beyond the personal view, Hinata ships a full reporting suite — burndown and velocity for sprints, cycle time, created-vs-resolved, and distributions by state, priority or assignee. Every report can be exported to PDF, so you can drop a sprint review straight into a slide deck. Read more in [Reports & dashboard](/en/reports.html).

## Projects & teams

Everything in Hinata lives inside a **project**. A project has a short **key** (like `ASTA`) that becomes the prefix for every issue number (`ASTA-42`), its own set of **workflow states**, and a palette of reusable **colored labels**. **Teams** are how you control who sees what: a team grants its members access to specific projects, and that access gates app-wide visibility — a person only ever sees the projects a team grants them. See [Projects & teams](/en/projects-teams.html).

## Issues & hierarchy

The **issue** is the atom of work. Each one has a type (**Epic, Story, Task, Bug, Feature** or **Sub-task**), a priority, labels, a Markdown description, comments, attachments and dependencies. Issues nest into a Jira-style three-level hierarchy — **Epic → Story/Task/Bug/Feature → Sub-task** — with a breadcrumb, a parent picker, and child and sub-task panels right on the issue. Attachments stream in live over Server-Sent Events, and issue keys link straight into your Git history. See [Issues & hierarchy](/en/issues.html).

## Boards & sprints

The **board** turns a project's issues into a drag-and-drop agile board whose columns map to your workflow states, with optional WIP limits and swimlanes grouped by epic, assignee or sub-task. A **Board / Backlog / Timeline** switcher lets you plan and visualize the same work three ways, and the backlog holds everything not yet pulled into a sprint. **Sprints** run the familiar plan → start → complete cycle with capacity and story points, and feed the burndown report. See [Boards & sprints](/en/boards-sprints.html).

## Gantt & time tracking

The **Gantt timeline** is a read model over your issues' start and due dates, dependencies and progress — a quick way to see the shape of a delivery and where the critical path runs. **Time tracking** lets people log work against issues with activity types, rolled up into weekly timesheets for reporting and capacity planning. See [Gantt & time tracking](/en/timeline.html).

## Knowledge base

The **knowledge base** is a Confluence-style space for documentation: hierarchical Markdown articles that can be global or scoped to a project, with the same team/project access control as the rest of the app. Smart links resolve real issues and people as you type, so your docs stay wired to live data instead of going stale. See [Knowledge base](/en/knowledge-base.html).

## Notifications

Hinata keeps everyone in the loop with in-app notifications, e-mail (over your SMTP relay) and mobile push. Push is relayed through the [Hinata Connect gateway](/en/connect-gateway.html), which means a single published app can serve many servers and self-hosters don't need a Firebase project of their own. Each person tunes what they receive from a notification matrix in [account settings](/en/authentication.html). See [Notifications](/en/notifications.html).

## Search & palette

Press **⌘K** (or **Ctrl+K**) anywhere to open the liquid-glass command palette. It searches across projects, issues, people and articles, surfaces recent items, and exposes quick commands — all in a responsive sheet that works just as well on a phone. See [Search & palette](/en/search.html).

## Git integration

Connect each project to one or more repositories on **GitHub, GitLab or Bitbucket**. Hinata brokers a real OAuth flow, registers a signed webhook, and turns push, pull-request and CI events into per-issue development information — branches, commits, PR/MRs and build status. Layer on **smart commits** (`ASTA-42 #comment shipped`, `#time 2h`) and workflow automation that moves issues forward as work progresses. See [Git integration](/en/git-integration.html).

## Single sign-on

Bring your own identity provider. Hinata supports **OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP** — Keycloak, Authentik, Azure AD, Google, Synology SSO and more — all configured at runtime from the Admin area, with no restart. See [SSO](/en/sso.html).

## Where to go next

- **[Projects & teams](/en/projects-teams.html)** — set up your first project and control who sees it.
- **[Issues & hierarchy](/en/issues.html)** — the work item, end to end.
- **[Boards & sprints](/en/boards-sprints.html)** — run an agile sprint from planning to review.
- **[Core concepts](/en/concepts.html)** — the vocabulary that ties it all together.
