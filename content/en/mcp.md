---
title: MCP server (AI)
description: Connect Claude, Cursor and other AI clients to Hinata over the Model Context Protocol, always within the connected user's permissions.
---

# MCP server (AI)

Hinata speaks the **Model Context Protocol (MCP)**, the open standard for AI clients. Connect Claude (desktop, web or Claude Code), Cursor or any other spec-compliant client.

The client can then search and create issues, read and write the knowledge base, and log work. **It always has exactly the permissions of the connected user.**

!!! info "Where it lives"
    The MCP server is **built into the Hinata backend**, with no sidecar and no second deployment. It is served at **`/mcp`** on the same host as the API. Every tool call runs through the same service layer as a normal request, with the same rules for team and project membership and article visibility.

## How it authenticates: Personal Access Tokens

An AI client connects with a **Personal Access Token (PAT)** you create in the app. A PAT is:

- **Scoped.** You grant only the capabilities it needs (`issues:read/write`, `projects:read/write`, `boards:read`, `sprints:write`, `teams:read`, `users:read`, `kb:read/write`, `worklog:read/write`, `search:read`, `notifications:read`). A read-only token can never write.
- **Revocable.** Any time. The next request with that token is rejected immediately.
- **Hashed at rest.** Only a SHA-256 hash is stored. You see the plaintext **once**, at creation.
- **Confined to `/mcp`.** The regular REST API rejects PATs, so a scoped token can never become full account access.

!!! warning "Copy the token when you create it"
    The full token (prefixed `hn_pat_…`) is shown only at creation. Put it in your client's config right away. Later you can only revoke it and create a new one.

## Create a token

1. In the app, open **Account → Access tokens**.
2. Choose **New token** and give it a name (e.g. *Claude Desktop*).
3. Select the scopes it needs and an optional expiry.
4. Copy the generated token.

!!! info "Feature flag"
    Access tokens appear only when the MCP feature is enabled. Admins turn it on under **Admin area → MCP** and cap how many tokens each user may hold.

## Connect a client

There are two ways to connect, depending on the client.

### One-click connect (OAuth 2.1)

For **Claude.ai** and **Claude Desktop**, add Hinata as a custom connector with the MCP URL `https://YOUR-HINATA-HOST/mcp` and press **Connect**.

Hinata is a full **OAuth 2.1 authorization server**:

- The client discovers the server through metadata (RFC 9728 / RFC 8414).
- It registers itself (Dynamic Client Registration).
- A browser opens. You **sign in to Hinata as usual (password, 2FA or SSO) and approve the requested scopes**.

There is no token to copy. Access runs on a short-lived token with a rotating refresh token, both revocable.

!!! info "OAuth needs HTTPS"
    Your server must be reachable over **HTTPS** at a public URL (its `base-url`). OAuth is on by default. Admins can turn it off, or turn off open client registration, under **Admin area → MCP**.

### Bearer token (PAT)

For **Claude Code**, **Cursor** and scripts, use a Personal Access Token:

```bash
claude mcp add --transport http hinata https://YOUR-HINATA-HOST/mcp \
  --header "Authorization: Bearer hn_pat_your_token_here"
```

Any client that supports remote MCP over Streamable HTTP works the same way: point it at `https://YOUR-HINATA-HOST/mcp` and send the token as an `Authorization: Bearer` header.

## What the AI can do

The server offers a fixed, curated set of tools. There is no way to call arbitrary endpoints, and no admin, auth or setup operations.

Every tool carries the MCP annotations `readOnlyHint` and `destructiveHint`. Clients like Claude use them to tell read tools apart from writes and deletions.

**Read tools:**

| Tool | Scope | What it does |
|---|---|---|
| `search_issues` | `issues:read` | Filter issues by project, state, assignee, sprint, backlog, type or text |
| `list_my_issues` | `issues:read` | Issues assigned to the connected user |
| `get_issue` | `issues:read` | One issue by id or readable id (e.g. `ASTA-42`) |
| `get_issue_hierarchy` | `issues:read` | An issue's epic or parent and sub-tasks |
| `list_comments` | `issues:read` | An issue's comments, paginated |
| `list_attachments` | `issues:read` | An issue's attachment metadata (name, type, size) |
| `get_dev_info` | `issues:read` | Linked branches, commits, pull requests and builds of an issue |
| `list_projects` / `get_project` | `projects:read` | Projects visible to the user, incl. workflow states and labels |
| `list_project_members` | `projects:read` | A project's members, to resolve people to assignee ids |
| `get_project_metrics` | `projects:read` | Issue counts: total, resolved, open, per workflow state |
| `copy_project` | `projects:write` | Copy a project with its plan; needs [project templates](/en/project-templates.html) |
| `set_issue_deadline` | `issues:write` | Keep a deadline as an offset from the project's date; needs project templates |
| `list_boards` / `get_board` | `boards:read` | Agile boards the user can open, with columns, WIP limits and active sprint |
| `list_sprints` | `boards:read` | A board's sprints, incl. archived on request |
| `get_sprint_report` | `boards:read` | Sprint insights: burndown, velocity, scope changes, assignee load |
| `list_teams` / `get_team` | `teams:read` | The user's teams, incl. members and their roles |
| `search_users` | `users:read` | Directory search by name, username or title |
| `get_me` | `users:read` | The connected user's own profile |
| `search` | `search:read` | Global search across issues, projects, people, boards, docs |
| `read_kb_article` | `kb:read` | A knowledge base article's content, respecting its visibility |
| `list_kb_articles` | `kb:read` | Visible knowledge base articles, by project or space |
| `list_work_items` | `worklog:read` | The logged time on an issue |
| `my_timesheet` | `worklog:read` | The user's own logged time in a date range |
| `list_my_notifications` | `notifications:read` | The user's notification inbox plus unread count |

**Write tools:**

| Tool | Scope | What it does |
|---|---|---|
| `create_issue` / `update_issue` | `issues:write` | Create an issue, update fields incl. state, sprint, parent, assignees |
| `add_comment` / `edit_comment` / `delete_comment` | `issues:write` | Comment on an issue, edit or delete your own comment |
| `create_sprint` / `update_sprint` | `sprints:write` | Plan a sprint on a SCRUM board, adjust name, goal, dates, capacity |
| `start_sprint` / `complete_sprint` | `sprints:write` | Start and complete a sprint. Completing moves open issues |
| `create_kb_article` / `update_kb_article` / `delete_kb_article` | `kb:write` | Manage knowledge base articles (visibility can never be changed via MCP) |
| `log_work` / `delete_work_item` | `worklog:write` | Log time against an issue, delete your own work item |

There are also **resources** for direct reference (`hinata://issue/{ASTA-42}`, `hinata://project/{KEY}`, `hinata://kb/{id}`) and a few **prompt** templates (triage an issue, draft a sprint stand-up).

## Security model

- **The ACL is never bypassed.** Every tool resolves the connected user and goes through the same services as the app. Team and project membership and article visibility apply as in the UI.
- **Scopes gate writes and reads.** A token without the required scope is refused before anything happens.
- **PATs are `/mcp`-only**, hashed at rest, revocable and can expire.
- **Everything is rate-limited** on its own per-IP budget. Every write, every token creation or revocation and every OAuth authorization is recorded in the **audit log**.
- **OAuth follows the standard and is hardened:** OAuth 2.1 with mandatory PKCE (S256), exact redirect URI matching, single-use authorization codes, hashed and rotating refresh tokens, and audience-bound access tokens (RFC 8707). OAuth tokens carry the same scopes and go through the same tools and ACLs as PATs.
