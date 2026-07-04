---
title: E-mail to ticket
description: Turn inbound e-mail into Hinata issues with IMAP polling, configured entirely at runtime from the admin area — no restart required.
---

# E-mail to ticket

Hinata can watch a mailbox and turn every incoming message into an issue. Point a
support or intake address at an IMAP mailbox, and each unread mail becomes a new issue
in the project you choose — subject as the title, body as the description, sender
recorded as the reporter. It is the **inbound** half of Hinata's mail story; the
**outbound** half (verification, password reset, notifications) is covered on the
[E-mail & SMTP](/en/email.html) page.

!!! info "Runtime-configured, no restart"
    E-mail ingestion is configured from the app's **Admin area**, and the settings live
    in **MongoDB**. Turning it on, changing the mailbox or switching the target project
    all apply **without restarting the server** — the poller reads the current settings
    on every cycle.

## How it works

The server runs a scheduled poller. On each cycle it reads the current ingest settings
and, when ingestion is enabled and a host and default project are configured, connects
to the mailbox over IMAP (or IMAPS), scans the chosen folder for **unseen** messages,
creates an issue from each one, and marks the message as **seen** so it is never
imported twice.

```text
scheduled poll (respects your poll interval)
        │
        ▼
enabled? host + default project set?  ── no ──▶ do nothing
        │ yes
        ▼
connect IMAP/IMAPS → open folder (READ_WRITE)
        │
        ▼
search UNSEEN messages
        │
        ▼
for each: create issue in the default project, then flag it SEEN
```

If a poll fails (mailbox unreachable, bad credentials), the error is logged and the
next cycle simply tries again — a transient outage never loses mail, because unread
messages are picked up on the following successful poll.

## What gets created

Each imported message becomes one issue in the **default project** you selected:

| Issue field | Comes from |
| --- | --- |
| **Title** | The e-mail **subject** (or `(no subject)` if empty), truncated to a safe length |
| **Description** | A short header noting who it was created from, then the message's plain-text body (the HTML part is stripped to text if no plain part exists) |
| **Type** | **Task** |
| **Reporter** | The sender's e-mail address is recorded on the issue |

Because it is a normal issue, everything else in Hinata applies immediately: it lands in
the project's default workflow state, appears on the board and backlog, can be assigned,
labelled, linked and commented on, and — if the project is connected to Git — can pick
up development info once someone references its key.

!!! tip "Pick a dedicated intake project"
    Point ingestion at a project that exists to receive raw inbound mail (for example a
    *Support Inbox*). A person triages each new issue — assigning it, setting type and
    priority, or moving it into the right project — rather than having unfiltered mail
    land in an active delivery board.

## Configuring it

Open the **Admin area → E-mail ingest** and provide the mailbox details. The available
settings and their defaults:

| Setting | Default | Meaning |
| --- | --- | --- |
| **Enabled** | `false` | Master switch for the poller |
| **Host** | — | IMAP server hostname |
| **Port** | `993` | IMAP port |
| **SSL** | `true` | Use IMAPS (implicit TLS); the standard port for it is `993` |
| **Username** | — | Mailbox login |
| **Password** | — | Mailbox password (write-only — never echoed back by the API) |
| **Folder** | `INBOX` | Which folder to scan |
| **Default project** | — | The project that receives the created issues |
| **Poll interval** | `60` s | Minimum seconds between mailbox scans |

Ingestion stays idle until **Enabled** is on **and** both a **host** and a **default
project** are set — so a half-finished configuration never does anything unexpected.

!!! warning "Use a dedicated mailbox"
    Every **unseen** message in the chosen folder is imported and then marked seen. Point
    ingestion at a mailbox that exists only for this purpose, not a shared human inbox —
    otherwise ordinary unread mail would be turned into issues and flagged as read.

## How it complements outbound SMTP

The two directions are independent and configured separately:

- **Inbound (this page)** — IMAP polling, configured in the admin area (MongoDB), turns
  received mail *into* issues.
- **Outbound — [E-mail & SMTP](/en/email.html)** — the SMTP relay Hinata uses to *send*
  verification, password-reset and notification mail.

You can run either without the other. A read-only status page might only send outbound
mail; an intake address might only ingest. Most production deployments run both: SMTP so
users get their mail, and ingestion so support requests become tracked issues.

## Related pages

- [E-mail & SMTP](/en/email.html) — outbound mail configuration.
- [Admin area](/en/admin-area.html) — where ingestion is configured at runtime.
- [Projects & teams](/en/projects-teams.html) — choosing and triaging the intake project.
- [Notifications](/en/notifications.html) — how people are told about new issues.
