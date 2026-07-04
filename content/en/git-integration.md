---
title: Git integration
description: Connect Hinata projects to real GitHub, GitLab and Bitbucket repositories for per-issue dev info, smart commits and workflow automation.
---

# Git integration

Connect each Hinata project to **one or more** repositories on **GitHub, GitLab or
Bitbucket** and your issues grow a live development timeline: the branches, commits,
pull/merge requests and CI builds that reference an issue key show up right on that
issue. On top of that you get **smart commits** (act on an issue straight from a
commit message) and **status automation** (let real Git events move issues through
your workflow).

Everything here is **real** — there is nothing emulated or faked. The server brokers
an actual OAuth flow with the provider, registers a signed webhook, and only records
an event after its signature verifies against the secret stored when the repo was
connected.

!!! info "How work gets linked to an issue"
    Hinata links by **issue key** — the human-readable id like `ASTA-42` (the regex
    is `[A-Z][A-Z0-9]+-\d+`). A branch is linked by the key in its **name**, a commit
    by the key(s) in its **message**, and a PR/MR by its **title or source branch**.
    A commit is *never* linked to an issue merely because it rides on that issue's
    branch — only the keys in its own message count.

## What you get on an issue

Once a project is connected, each issue exposes a development-info panel built from
verified webhook events:

| Surface | Source event | Notes |
| --- | --- | --- |
| **Branches** | `push` with a new ref / `create` | Name, base (the repo's default branch), provider and repo |
| **Commits** | `push` | SHA, first line of the message, timestamp, verified flag; newest first (capped) |
| **Pull / merge requests** | `pull_request` / Merge Request / `pullrequest:*` | Number, title, state (`OPEN`, `DRAFT`, `MERGED`, `CLOSED`), source/target branch, comment count |
| **CI builds** | `workflow_run` / Pipeline | Workflow name, branch and status (`pending`, `running`, `passing`, `failing`) |

You can also **act** on a linked PR/MR from the issue without leaving Hinata:

```text
POST /api/v1/issues/{key}/dev-info/prs/{number}/merge   → merge it
POST /api/v1/issues/{key}/dev-info/prs/{number}/ready    → mark ready for review
GET  /api/v1/issues/{key}/dev-info                        → read the panel
```

Reading dev-info or acting on a PR requires **project membership**; changing a
project's connection requires being a **project lead or admin**.

## Operator setup (one-time, platform-wide)

Git integration is configured **once per platform**, not per project. You register
**one OAuth app per provider** and give the server its credentials, then every
project lead can connect repos through it.

### 1. Provide OAuth app credentials

Register an OAuth app (GitHub / GitLab) or OAuth consumer (Bitbucket) with each
provider you want to support, then give Hinata the client id + secret — either in the
app's **Admin area → Git integration** (stored in MongoDB, applied without a restart)
or via environment variables. As everywhere in Hinata, **the database overrides the
environment**, and secrets are **write-only** in the admin API — they are never echoed
back.

| Variable | Purpose |
| --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` / `HINATA_GIT_GITHUB_CLIENT_SECRET` | GitHub OAuth app credentials |
| `HINATA_GIT_GITLAB_CLIENT_ID` / `HINATA_GIT_GITLAB_CLIENT_SECRET` | GitLab OAuth app credentials |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` / `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Bitbucket OAuth consumer credentials |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Public API base for the OAuth callback **and** webhook registration; falls back to `HINATA_BASE_URL` + `/api/v1` |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM key that encrypts stored access tokens and webhook secrets at rest — **change the default in production** |

### 2. Set the public API base

Both the OAuth callback and the webhooks must be reachable **from the provider**, so
Hinata needs to know its own public API base. Set `HINATA_GIT_WEBHOOK_BASE_URL` to it,
for example:

```properties
HINATA_GIT_WEBHOOK_BASE_URL=https://api.track.example.com/api/v1
```

If you leave it blank, Hinata derives it from `HINATA_BASE_URL` + `/api/v1`.

### 3. Register the OAuth callback

At each provider, set the OAuth app's authorization callback URL to the server's
public callback:

```text
<public-api-base>/git/oauth/callback
```

With the base above that is
`https://api.track.example.com/api/v1/git/oauth/callback`.

!!! warning "Change the token-encryption secret"
    `HINATA_GIT_TOKEN_SECRET` is the AES-GCM key that encrypts every stored access
    token and per-connection webhook secret **at rest**. Ship a real, random value in
    production — never the shipped default. If it changes, previously stored tokens can
    no longer be decrypted and affected repos must be reconnected.

## The OAuth flow (server-brokered)

Connecting a repo runs a real three-legged OAuth flow, brokered by the server so the
app never holds the provider client secret. The unguessable, short-lived `state`
(stored in MongoDB with a **15-minute TTL**) ties the browser round-trip back to the
project:

```text
App   POST /projects/{id}/git/oauth/start   (provider)
        │
        ▼
Server  builds provider authorize URL, stores session state (Mongo, TTL 15m)
        │  returns { authorizeUrl, state }
        ▼
User    opens the authorize URL in a browser and consents
        │
        ▼
Provider  GET /git/oauth/callback?code&state   (public, no bearer token)
        │
        ▼
Server  exchanges code → access token, stores it AES-GCM-encrypted
        │  marks the session AUTHORIZED
        ▼
App     polls GET /git/oauth/session/{state}  → AUTHORIZED
        │
        ▼
App     GET  /projects/{id}/git/owners        → pick an owner/org
        App  GET  /projects/{id}/git/repos     → pick a repository
        App  POST /projects/{id}/git/connect   → connect (registers the webhook)
```

The callback endpoint is **public** — the provider redirects the user's browser to it
with no bearer token — so its security rests entirely on the unguessable `state`. It
returns a small HTML page telling the user they can close the tab and return to Hinata.

### Self-managed servers (Enterprise / Data Center)

Self-hosted **GitHub Enterprise**, **GitLab** (self-managed) and **Bitbucket Data
Center** instances skip the OAuth dance entirely. Connect them with a repo URL and a
**personal access token** instead:

```text
POST /api/v1/projects/{id}/git/connect-token
{ "repoUrl": "https://git.example.com/team/app.git", "token": "<personal-access-token>" }
```

The token is stored AES-GCM-encrypted just like an OAuth token, and the same webhook
registration and linking rules apply.

## Webhooks

On connect the server registers a hook (for `push`, branch `create`, PR/MR and CI
events) that points at a **public**, signature-verified receiver, signed with a
**per-project secret** generated at connect time. Every inbound delivery is verified
before anything is recorded:

| Provider | Endpoint | Verification |
| --- | --- | --- |
| **GitHub** | `POST /api/v1/git/webhooks/github` | HMAC-SHA256 over the raw body (`X-Hub-Signature-256`) |
| **GitLab** | `POST /api/v1/git/webhooks/gitlab` | token compare (`X-Gitlab-Token`) |
| **Bitbucket** | `POST /api/v1/git/webhooks/bitbucket` | shared secret in the URL query (`?secret=…`) |

The receiver finds the project (and the exact connected repo) by the repository in the
payload, verifies **that connection's** secret, and only then links the event to issue
keys. An unknown repository is silently ignored with a `200`; a known repository whose
signature does not verify is rejected as unauthorized.

## Linking rules

The rules are deliberately strict so your issues stay honest:

- **Branch** → linked by the issue key in the **branch name**.
- **Commit** → linked by the issue key(s) in the **commit message** only. It is *never*
  linked just because it sits on an issue's branch.
- **PR / MR** → linked by the issue key(s) in its **title or source branch**.
- A key only links to a **real** issue that belongs to **this repo's project** — a key
  pointing at a nonexistent issue, or an issue in another project, is ignored.

!!! note "Exactly-once side effects"
    Providers redeliver webhooks, and the same commit is re-listed whenever a feature
    branch is merged into the default branch. So a commit's **side effects** — smart
    commits and the commit-pushed transition — are applied **exactly once**, guarded by
    a small ledger (`git_processed_commits`). Without it, every redelivery would re-post
    each comment and re-log each worklog. (Recording a branch/commit/PR into the panel
    is itself idempotent — the same SHA or PR number is upserted, not duplicated.)

## Automation

Automation is configured **per project**, against **that project's own workflow
states**, and wires real Git events to state transitions:

| Trigger | Rule |
| --- | --- |
| **Branch created** (a `create`, or a `push` that introduces a new ref) | move the referenced issue (e.g. → *In Progress*) |
| **Commit pushed** referencing the key (on any branch) | move the referenced issue |
| **PR / MR opened** (opened / reopened / ready-for-review) | move the referenced issue (e.g. → *In Review*) |
| **PR / MR merged** | move the referenced issue (e.g. → *Done*) |

!!! tip "Forward-only, so it never fights you"
    Automation only ever moves an issue **forward** in the workflow, never backward. A
    late commit can't drag an *In Review* or *Done* issue back to *In Progress*, and a
    transition that is already satisfied is a no-op. Configure the rules with
    `PATCH /api/v1/projects/{id}/git/automation`.

## Smart commits

Trailers in a commit message act directly on the referenced issue. Smart commits must
be enabled in the project's automation settings; then, for an issue key in the message:

| Trailer | Effect |
| --- | --- |
| `ASTA-42 #comment shipped it` | adds a comment to `ASTA-42` |
| `ASTA-42 #time 2h 30m` | logs `2h 30m` of work on `ASTA-42` |
| `ASTA-42 #done` (any other `#word`) | transitions `ASTA-42` to the matching workflow state |

```text
ASTA-42 #comment fixed the null pointer on empty search #time 45m #in-review
```

That single commit adds a comment, logs 45 minutes and moves `ASTA-42` to *In Review*.
An unknown `#word` (no matching state) or a key pointing at no real issue is quietly
skipped — the rest of the message still applies.

## Multiple repositories per project

A project can connect **several** repositories — for example an app repo and a server
repo tracked by the same team. What is **shared project-wide** versus **per-repo**:

- **Shared across the project**: the automation rules and the **branch template**
  (default `{key}-{summary}`, used to suggest a branch name from an issue).
- **Per repository**: its own access **token**, its own **webhook** and signing secret,
  and its own **default branch**.

Only work pushed to a **connected** repo surfaces on the project's issues. Manage the
extra repos alongside the primary one; disconnecting or resyncing can target a single
repo by id:

```text
POST   /api/v1/projects/{id}/git/connect         → add a repo (OAuth)
POST   /api/v1/projects/{id}/git/connect-token   → add a self-managed repo (PAT)
POST   /api/v1/projects/{id}/git/resync?repoId=… → re-pull state for one repo
DELETE /api/v1/projects/{id}/git?repoId=…        → disconnect one repo (omit repoId for all)
PATCH  /api/v1/projects/{id}/git/branch-template → set the shared branch template
```

## Security

- **Encryption at rest**: access tokens and per-connection webhook secrets are
  **AES-GCM-encrypted** with `HINATA_GIT_TOKEN_SECRET` and are **never returned** by the
  API (secrets are write-only in the admin surface).
- **Signature-verified ingestion**: no webhook event is recorded unless its signature
  (HMAC / token / query secret) verifies against the stored per-project secret. Unknown
  repos are ignored; bad signatures are rejected.
- **Least privilege**: reading dev-info or acting on a PR requires project membership;
  connecting, disconnecting or changing automation requires being a project lead or
  admin.
- **Bounded state**: commits and builds per issue are capped and trimmed, so a busy
  repo can't grow an unbounded panel.

## Related pages

- [Projects & teams](/en/projects-teams.html) — issue keys, workflows and membership.
- [Issues & hierarchy](/en/issues.html) — where the dev-info panel appears.
- [Admin area](/en/admin-area.html) — where OAuth app credentials live at runtime.
- [Configuration reference](/en/configuration.html) — the full `HINATA_GIT_*` set.
