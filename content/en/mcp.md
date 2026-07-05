---
title: MCP server (AI)
description: Connect Claude, Cursor and other AI clients to Hinata over the Model Context Protocol. Scoped Personal Access Tokens, an embedded /mcp endpoint, and tools that act as the connected user within their permissions.
---

# MCP server (AI)

Hinata speaks the **Model Context Protocol (MCP)** — the open standard AI clients
use to reach external systems. Point Claude (desktop, web or Claude Code), Cursor
or any spec-compliant client at your Hinata instance and it can search and create
issues, read and write the knowledge base, and log work — **always within the
exact permissions of the connected user**. Your project data becomes something a
developer or PM can drive straight from their AI workflow.

!!! info "Where it lives"
    The MCP server is **embedded in the Hinata backend** — no sidecar, no second
    deployment. It is served at **`/mcp`** on the same host as the API and
    inherits the platform's access control unchanged: every tool call runs
    through the same service layer (team/project membership, article visibility)
    a normal request does.

## How it authenticates — Personal Access Tokens

An AI client connects with a **Personal Access Token (PAT)** you create in the
app. A PAT is:

- **Scoped** — you grant it a least-privilege subset of capabilities
  (`issues:read`, `issues:write`, `projects:read`, `kb:read`, `kb:write`,
  `worklog:write`, `search:read`). A read-only token can never write.
- **Revocable** — revoke it any time; the next request from that token is
  rejected immediately.
- **Hashed at rest** — only a SHA-256 hash is stored. The plaintext is shown
  **once**, at creation, and never again.
- **Confined to `/mcp`** — a PAT authenticates the MCP endpoint and nothing else.
  Presenting it to the regular REST API is rejected, so a scoped token can never
  become unrestricted account access.

!!! warning "Copy the token when you create it"
    The full token (prefixed `hn_pat_…`) is displayed only at creation. Store it
    in your client's config right away — you cannot retrieve it later, only
    revoke it and create a new one.

## Create a token

In the app, open **Account → Access tokens**, choose **New token**, give it a
name (e.g. *Claude Desktop*), select the scopes it needs and an optional expiry,
then copy the generated token.

!!! info "Feature flag"
    Access tokens appear only when the MCP feature is enabled. Admins toggle it —
    and cap how many tokens each user may hold — under **Admin area → MCP**.

## Connect a client

Add Hinata as a remote MCP server, using your token as a bearer credential. For
**Claude Code**:

```bash
claude mcp add --transport http hinata https://YOUR-HINATA-HOST/mcp \
  --header "Authorization: Bearer hn_pat_your_token_here"
```

Any client that supports remote MCP over Streamable HTTP works the same way —
point it at `https://YOUR-HINATA-HOST/mcp` and send the token as an
`Authorization: Bearer` header.

## What the AI can do

The server exposes a curated, fixed set of tools — never a generic "call any
endpoint" surface, and never admin, auth or setup operations.

| Tool | Scope | What it does |
|---|---|---|
| `search_issues` | `issues:read` | Filter issues by project, state, assignee, sprint, type or text |
| `list_my_issues` | `issues:read` | Issues assigned to the connected user |
| `get_issue` | `issues:read` | One issue by id or readable id (e.g. `ASTA-42`) |
| `get_issue_hierarchy` | `issues:read` | An issue's epic/parent and sub-tasks |
| `list_projects` / `get_project` | `projects:read` | Projects visible to the user |
| `search` | `search:read` | Global search across issues, projects, people, boards, docs |
| `read_kb_article` | `kb:read` | A knowledge-base article, respecting its visibility |
| `create_issue` | `issues:write` | Create an issue |
| `update_issue` | `issues:write` | Update fields on an issue |
| `add_comment` | `issues:write` | Comment on an issue |
| `create_kb_article` | `kb:write` | Create a knowledge-base article |
| `log_work` | `worklog:write` | Log time against an issue |

It also publishes **resources** (`hinata://issue/{ASTA-42}`,
`hinata://project/{KEY}`, `hinata://kb/{id}`) for direct reference, and a couple
of **prompt** templates (triage an issue, draft a sprint stand-up).

## Security model

- **The ACL is never bypassed.** Every tool resolves the connected user and
  delegates through the same services the app uses, so team/project membership
  and article visibility apply exactly as in the UI.
- **Scopes gate writes** (and reads). A token missing the required scope is
  refused before anything happens.
- **PATs are `/mcp`-only**, hashed at rest, revocable, and optionally expiring.
- **Everything is rate-limited** on its own per-IP budget, and every write plus
  every token creation/revocation is recorded in the **audit log**.

!!! info "On the roadmap"
    A future release adds a full **OAuth 2.1** flow (dynamic client registration)
    so Claude's one-click "Connect" button can link to Hinata without pasting a
    token. PATs remain the simplest path for Claude Code, Cursor and scripts.
