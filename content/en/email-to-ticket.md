---
title: E-mail to ticket
description: Turn inbound e-mail into issues via IMAP, configured in the admin area with no restart.
---

# E-mail to ticket

Hinata can watch a mailbox and turn every unread message into an issue. Point a
support or intake address at an IMAP mailbox. Each new mail becomes an issue in
the project you choose:

- Subject becomes the title.
- Body becomes the description.
- Sender is recorded as the reporter.

This is the **inbound** part. Outbound mail (verification, password reset,
notifications) is covered in [E-mail & SMTP](/en/email.html).

!!! info "Runtime-configured, no restart"
    You configure e-mail ingestion in the **Admin area**. The settings live in
    **MongoDB**. Turning it on, changing the mailbox or switching the target
    project applies **without restarting the server**, because the poller reads
    the settings on every cycle.

## How it works

The server polls the mailbox on a schedule. When ingestion is enabled and a host
and default project are set, each cycle does this:

1. Connect over IMAP or IMAPS.
2. Scan the chosen folder for **unseen** messages.
3. Create an issue from each message.
4. Mark the message **seen** so it's never imported twice.

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

If a poll fails (mailbox unreachable, bad credentials), the error is logged and
the next cycle tries again. No mail is lost, because unread messages get picked
up on the next successful poll.

## What gets created

Each message becomes one issue in the selected **default project**:

| Issue field | Comes from |
| --- | --- |
| **Title** | The e-mail **subject** (or `(no subject)` if empty), truncated to a safe length |
| **Description** | A short header naming the sender, then the plain-text body. If there's no plain part, the HTML part is converted to text |
| **Type** | **Task** |
| **Reporter** | The sender's e-mail address |
| **Author** | The sender, if their address belongs to an active Hinata account. They then get notified about every change, like any watcher. If nobody owns the address, the issue has no author. The description header still names the sender |

!!! note "An author who is not a project member"
    Being the author grants no access. Only project members can open the issue.
    An author outside the project still gets e-mail and push notices, but without
    a link, since it would only lead to a "not a member" error. Add them to the
    project if they should follow it.

It's a normal issue. It starts in the project's default workflow state and shows
up on the board and backlog. You can assign, label, link and comment on it. If
the project is connected to Git, it picks up development info once someone
references its key.

!!! tip "Pick a dedicated intake project"
    Send inbound mail to its own project, for example a *Support Inbox*. Someone
    triages each new issue there: assigns it, sets type and priority, or moves it
    to the right project. That keeps unfiltered mail off your active boards.

## Configuring it

Open **Admin area → E-mail ingest** and enter the mailbox details:

| Setting | Default | Meaning |
| --- | --- | --- |
| **Enabled** | `false` | Master switch for the poller |
| **Host** | (empty) | IMAP server hostname |
| **Port** | `993` | IMAP port |
| **SSL** | `true` | Use IMAPS (implicit TLS). The standard port for it is `993` |
| **Username** | (empty) | Mailbox login |
| **Password** | (empty) | Mailbox password. Write-only, never returned by the API |
| **Folder** | `INBOX` | Which folder to scan |
| **Default project** | (empty) | The project that receives the issues |
| **Poll interval** | `60` s | Minimum seconds between mailbox scans |

Ingestion stays idle until **Enabled** is on **and** both **host** and **default
project** are set. A half-finished configuration does nothing.

!!! warning "Use a dedicated mailbox"
    Every **unseen** message in the folder is imported and marked seen. Use a
    mailbox that exists only for this. In a shared inbox, ordinary unread mail
    would turn into issues and get marked as read.

## How it complements outbound SMTP

The two directions are independent and configured separately:

- **Inbound (this page):** IMAP polling, configured in the admin area (MongoDB).
  Turns received mail into issues.
- **Outbound ([E-mail & SMTP](/en/email.html)):** the SMTP relay Hinata uses to
  *send* verification, password reset and notification mail.

You can use either one alone. A status page might only send, an intake address
might only receive. Most production setups use both: SMTP for mail to users, and
ingestion for support requests.

## Related pages

- [E-mail & SMTP](/en/email.html): outbound mail setup.
- [Admin area](/en/admin-area.html): where you configure ingestion.
- [Projects & teams](/en/projects-teams.html): choosing and triaging the intake project.
- [Notifications](/en/notifications.html): how people learn about new issues.
