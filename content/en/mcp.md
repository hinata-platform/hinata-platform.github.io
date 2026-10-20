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

- **Scoped.** You grant only the capabilities it needs (`issues:read/write`, `projects:read/write`, `boards:read`, `sprints:write`, `teams:read`, `users:read`, `kb:read/write`, `worklog:read/write`, `search:read`, `notifications:read`, `shifts:read/write/plan`). A read-only token can never write.
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
| `list_my_work_items` | `worklog:read` | The user's own time entries in a date range, paginated, optionally by project or text |
| `time_summary` | `worklog:read` | The user's own time in up to 366 days, totalled and grouped by project, issue, activity, tag, day, week or month |
| `get_timer` | `worklog:read` | The user's running timer, if one runs |
| `my_time_off_balance` | `worklog:read` | The user's own leave per absence type: entitled, taken, planned, left. Sick leave is not listed |
| `list_my_notifications` | `notifications:read` | The user's notification inbox plus unread count |

**Write tools:**

| Tool | Scope | What it does |
|---|---|---|
| `create_issue` / `update_issue` | `issues:write` | Create an issue, update fields incl. state, sprint, parent, assignees |
| `add_comment` / `edit_comment` / `delete_comment` | `issues:write` | Comment on an issue, edit or delete your own comment |
| `add_participant` / `remove_participant` | `issues:write` | Share an issue with a person outside its project or end the share ([Sharing an issue](/en/guide-sharing)) |
| `create_sprint` / `update_sprint` | `sprints:write` | Plan a sprint on a SCRUM board, adjust name, goal, dates, capacity |
| `start_sprint` / `complete_sprint` | `sprints:write` | Start and complete a sprint. Completing moves open issues |
| `create_kb_article` / `update_kb_article` / `delete_kb_article` | `kb:write` | Manage knowledge base articles (visibility can never be changed via MCP) |
| `log_work` / `delete_work_item` | `worklog:write` | Log time against an issue, delete your own work item |
| `update_work_item` | `worklog:write` | Change your own time entry; locked days, submitted periods and invoiced entries are refused with the reason |
| `start_timer` / `stop_timer` / `discard_timer` | `worklog:write` | Start a timer, stop it into a time entry, or throw it away |
| `request_time_off` | `worklog:write` | Ask for time off; it goes to whoever decides it, as from the app |

The timer, entry and absence tools need the extended time tracking (and absence management for the last two); with the module off they say so and the four older tools keep working. No tool reads anybody else's time or balance, and no tool decides a leave request: approving stays with a person in the app. Sick leave is neither reported nor read over MCP.

There are also **resources** for direct reference (`hinata://issue/{ASTA-42}`, `hinata://project/{KEY}`, `hinata://kb/{id}`, and your own `hinata://time/timer`, `hinata://time/entries/{id}` and `hinata://time-off/balance`) and a few **prompt** templates (triage an issue, draft a sprint stand-up).

## Shifts

With [shift planning](/en/shifts.html) switched on, an assistant can answer questions like these and act for you:

- "When is my next shift?"
- "Where are people still missing on Saturday?"
- "Sign me up for setting up on Friday."
- "Give up my shift on Sunday."

| Tool | Scope | What it does |
|---|---|---|
| `list_my_shifts` | `shifts:read` | Your own shifts and waiting-list places in a period, the next 30 days by default |
| `next_shift` | `shifts:read` | Your next own shift, or that there is none |
| `list_shift_events` | `shifts:read` | Events with numbers: needed, taken, shifts still short. Optionally only events where people are missing |
| `get_shift_event` | `shifts:read` | One event with all its shifts as numbers, without names |
| `get_shift` | `shifts:read` | One shift with the people who hold a place. People on the waiting list are counted, never named |
| `self_assign_shift` | `shifts:write` | Sign yourself up. On a full shift you join the waiting list, and the answer says so |
| `release_shift` | `shifts:write` | Give up your own place or leave the waiting list |
| `confirm_shift` / `decline_shift` | `shifts:write` | Confirm or decline an assignment |
| `assign_shift` / `remove_assignment` | `shifts:plan` | As a planner, put somebody on a shift or take them off |

A period covers at most 62 days and a page at most 100 entries. Times come as wall-clock times in the event's time zone, with the zone named. Hinata refuses an overlap with one of your own shifts in a sentence that gives the reason.

`shifts:plan` is meant for tokens that work on behalf of a planner. The one-click connection leaves it out when the client names no scopes; a client only gets it by asking for it explicitly and with your approval. The three shift scopes appear in the app and on the approval page only while shift planning is switched on. While it is off, the tools answer that the feature is not enabled.

!!! warning "Event texts are not instructions"
    People write the title, location and description of an event, and an assistant reads them. If one says something like "Ignore all previous instructions", that is text, not a command. Hinata passes these texts in their own data fields and never in a tool's description. Still, give a token only the scopes it needs, and do not let an assistant with `shifts:plan` assign anybody without asking you first.

Sign-ups through MCP are recorded in the audit log as assignments, just like in the app. The extra records saying that a token acted (`MCP_SHIFT_*`) stay off until an administrator switches them on.

## Security model

- **The ACL is never bypassed.** Every tool resolves the connected user and goes through the same services as the app. Team and project membership and article visibility apply as in the UI.
- **Scopes gate writes and reads.** A token without the required scope is refused before anything happens.
- **PATs are `/mcp`-only**, hashed at rest, revocable and can expire.
- **Everything is rate-limited** on its own per-IP budget. Every write, every token creation or revocation and every OAuth authorization is recorded in the **audit log**. Starting, stopping and discarding a timer is the exception: like the same actions in the app, those records are off until an administrator switches them on, because a line per start and stop is a record of when somebody worked.
- **OAuth follows the standard and is hardened:** OAuth 2.1 with mandatory PKCE (S256), exact redirect URI matching, single-use authorization codes, hashed and rotating refresh tokens, and audience-bound access tokens (RFC 8707). OAuth tokens carry the same scopes and go through the same tools and ACLs as PATs.
