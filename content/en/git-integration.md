---
title: Git integration
description: Connect Hinata projects to GitHub, GitLab and Bitbucket for dev info, smart commits and automation.
---

# Git integration

Connect a Hinata project to **one or more** repositories on **GitHub, GitLab or
Bitbucket**. Branches, commits, pull or merge requests and CI builds that reference an
issue key then show up right on that issue.

On top of that you get:

- **Smart commits**: act on an issue straight from a commit message.
- **Status automation**: Git events move issues through your workflow.

The server runs a real OAuth flow with the provider and registers a signed webhook. An
event is only recorded after its signature matches the secret stored when the repo was
connected.

!!! info "How work gets linked to an issue"
    Hinata links by **issue key**, the readable id like `ASTA-42` (regex
    `[A-Z][A-Z0-9]+-\d+`). A branch is linked by the key in its **name**, a commit by the
    keys in its **message**, and a PR/MR by its **title or source branch**. A commit is
    *never* linked just because it sits on an issue's branch.

## What you get on an issue

Each issue in a connected project shows a development info panel built from verified
webhook events:

| Surface | Source event | Notes |
| --- | --- | --- |
| **Branches** | `push` with a new ref / `create` | Name, base (the repo's default branch), provider and repo |
| **Commits** | `push` | SHA, first line of the message, timestamp, verified flag. Newest first (capped) |
| **Pull / merge requests** | `pull_request` / Merge Request / `pullrequest:*` | Number, title, state (`OPEN`, `DRAFT`, `MERGED`, `CLOSED`), source/target branch, comment count |
| **CI builds** | `workflow_run` / Pipeline | Workflow name, branch and status (`pending`, `running`, `passing`, `failing`) |

You can act on a linked PR/MR right from the issue:

```text
POST /api/v1/issues/{key}/dev-info/prs/{number}/merge   → merge it
POST /api/v1/issues/{key}/dev-info/prs/{number}/ready    → mark ready for review
GET  /api/v1/issues/{key}/dev-info                        → read the panel
```

- Reading dev info or acting on a PR: **project membership**.
- Changing a project's connection: **project lead or admin**.

## Operator setup (one-time, platform-wide)

You set up Git integration **once for the whole platform**. Register **one OAuth app
per provider** and give the server its credentials. After that, every project lead can
connect repos.

### 1. Provide OAuth app credentials

Register an OAuth app (GitHub, GitLab) or OAuth consumer (Bitbucket) with each provider.
Give Hinata the client id and secret in one of two ways:

- in the app's **Admin area → Git integration** (stored in MongoDB, applied without a restart)
- via environment variables

**The database overrides the environment.** Secrets are **write-only** in the admin API
and are never returned.

| Variable | Purpose |
| --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` / `HINATA_GIT_GITHUB_CLIENT_SECRET` | GitHub OAuth app credentials |
| `HINATA_GIT_GITLAB_CLIENT_ID` / `HINATA_GIT_GITLAB_CLIENT_SECRET` | GitLab OAuth app credentials |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` / `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Bitbucket OAuth consumer credentials |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Public API base for the OAuth callback **and** webhook registration. Falls back to `HINATA_BASE_URL` + `/api/v1` |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM key that encrypts stored access tokens and webhook secrets at rest. **Change the default in production** |

### 2. Set the public API base

The OAuth callback and the webhooks must be reachable **from the provider**, so Hinata
needs to know its public API base. Set `HINATA_GIT_WEBHOOK_BASE_URL`:

```properties
HINATA_GIT_WEBHOOK_BASE_URL=https://api.track.example.com/api/v1
```

If you leave it blank, Hinata uses `HINATA_BASE_URL` + `/api/v1`.

### 3. Register the OAuth callback

At each provider, set this callback URL in the OAuth app:

```text
<public-api-base>/git/oauth/callback
```

With the base above that is
`https://api.track.example.com/api/v1/git/oauth/callback`.

!!! warning "Change the token encryption secret"
    `HINATA_GIT_TOKEN_SECRET` is the AES-GCM key for every stored access token and
    per-connection webhook secret **at rest**. Use a random value in production, never
    the shipped default. If it changes, stored tokens can no longer be decrypted and
    affected repos must be reconnected.

## The OAuth flow (server-brokered)

The server brokers a three-legged OAuth flow, so the app never holds the provider's
client secret. An unguessable, short-lived `state` (stored in MongoDB with a **15-minute
TTL**) ties the browser round trip back to the project:

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

The callback is **public** because the provider redirects the browser there without a
bearer token. Its security rests entirely on the unguessable `state`. It returns a small
HTML page telling the user to close the tab and return to Hinata.

### Self-managed servers (Enterprise / Data Center)

Self-hosted **GitHub Enterprise**, **GitLab** (self-managed) and **Bitbucket Data
Center** skip OAuth. Connect them with a repo URL and a **personal access token**:

```text
POST /api/v1/projects/{id}/git/connect-token
{ "repoUrl": "https://git.example.com/team/app.git", "token": "<personal-access-token>" }
```

The token is stored AES-GCM-encrypted like an OAuth token. Webhook registration and
linking rules are the same.

## Webhooks

On connect the server registers a hook for `push`, branch `create`, PR/MR and CI events.
It points at a **public** receiver and is signed with a **per-project secret** generated
at connect time. Every delivery is verified before anything is recorded:

| Provider | Endpoint | Verification |
| --- | --- | --- |
| **GitHub** | `POST /api/v1/git/webhooks/github` | HMAC-SHA256 over the raw body (`X-Hub-Signature-256`) |
| **GitLab** | `POST /api/v1/git/webhooks/gitlab` | token compare (`X-Gitlab-Token`) |
| **Bitbucket** | `POST /api/v1/git/webhooks/bitbucket` | shared secret in the URL query (`?secret=…`) |

The receiver finds the project and the connected repo from the repository in the
payload. It verifies **that connection's** secret and only then links the event to issue
keys.

- Unknown repository: ignored without error, with a `200`.
- Known repository with a bad signature: rejected as unauthorized.

## Linking rules

- **Branch**: by the issue key in the **branch name**.
- **Commit**: only by the issue keys in the **commit message**. It is *never* linked just
  because it sits on an issue's branch.
- **PR / MR**: by the issue keys in its **title or source branch**.
- A key only links to an **existing** issue in **this repo's project**. Keys pointing at
  a missing issue or an issue in another project are ignored.

!!! note "Exactly-once side effects"
    Providers redeliver webhooks, and a commit is listed again when a feature branch is
    merged into the default branch. So a commit's **side effects** (smart commits and the
    commit-pushed transition) run **exactly once**, guarded by a small ledger
    (`git_processed_commits`). Without it, every redelivery would post comments and log
    work again.

    The panel itself is idempotent: the same SHA or PR number is updated, not duplicated.

## Automation

Automation is set **per project**, against **that project's own workflow states**. It
maps Git events to state transitions:

| Trigger | Rule |
| --- | --- |
| **Branch created** (a `create`, or a `push` that introduces a new ref) | move the referenced issue (e.g. → *In Progress*) |
| **Commit pushed** referencing the key (on any branch) | move the referenced issue |
| **PR / MR opened** (opened / reopened / ready-for-review) | move the referenced issue (e.g. → *In Review*) |
| **PR / MR merged** | move the referenced issue (e.g. → *Done*) |

!!! tip "Forward only"
    Automation only moves an issue **forward** in the workflow. A late commit can't drag
    an *In Review* or *Done* issue back to *In Progress*, and a transition that is already
    satisfied does nothing. Configure the rules with
    `PATCH /api/v1/projects/{id}/git/automation`.

## Smart commits

Enable smart commits in the project's automation settings. Trailers in a commit message
then act directly on the referenced issue:

| Trailer | Effect |
| --- | --- |
| `ASTA-42 #comment shipped it` | adds a comment to `ASTA-42` |
| `ASTA-42 #time 2h 30m` | logs `2h 30m` of work on `ASTA-42` |
| `ASTA-42 #done` (any other `#word`) | transitions `ASTA-42` to the matching workflow state |

```text
ASTA-42 #comment fixed the null pointer on empty search #time 45m #in-review
```

That commit adds a comment, logs 45 minutes and moves `ASTA-42` to *In Review*. An
unknown `#word` (no matching state) or a key without an existing issue is skipped without
error. The rest of the message still applies.

## Multiple repositories per project

A project can connect **several** repositories, for example an app repo and a server
repo owned by the same team.

- **Shared across the project**: the automation rules and the **branch template**
  (default `{key}-{summary}`, suggests a branch name from an issue).
- **Per repository**: its own access **token**, its own **webhook** and signing secret,
  and its own **default branch**.

Only work pushed to a **connected** repo shows up on the project's issues. Manage extra
repos alongside the primary one. Disconnect and resync can target a single repo by id:

```text
POST   /api/v1/projects/{id}/git/connect         → add a repo (OAuth)
POST   /api/v1/projects/{id}/git/connect-token   → add a self-managed repo (PAT)
POST   /api/v1/projects/{id}/git/resync?repoId=… → re-pull state for one repo
DELETE /api/v1/projects/{id}/git?repoId=…        → disconnect one repo (omit repoId for all)
PATCH  /api/v1/projects/{id}/git/branch-template → set the shared branch template
```

## Security

- **Encryption at rest**: access tokens and webhook secrets are **AES-GCM-encrypted**
  with `HINATA_GIT_TOKEN_SECRET` and **never returned** by the API (write-only in the
  admin area).
- **Signature-verified ingestion**: a webhook event is only recorded if its signature
  (HMAC, token or query secret) matches the stored per-project secret. Unknown repos are
  ignored, bad signatures rejected.
- **Least privilege**: reading dev info or acting on a PR requires project membership.
  Connecting, disconnecting or changing automation requires project lead or admin.
- **Bounded state**: commits and builds per issue are capped and trimmed, so a busy repo
  can't grow the panel without limit.

## Related pages

- [Projects & teams](/en/projects-teams.html): issue keys, workflows and membership.
- [Issues & hierarchy](/en/issues.html): where the dev info panel appears.
- [Admin area](/en/admin-area.html): where OAuth credentials live at runtime.
- [Configuration reference](/en/configuration.html): the full `HINATA_GIT_*` set.
