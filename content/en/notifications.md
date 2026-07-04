---
title: Notifications
description: Stay in the loop with in-app, e-mail and push notifications — each user tunes exactly what they receive with a per-event notification matrix.
---

# Notifications

Hinata keeps people informed without drowning them. Notifications arrive through three channels, and every user decides exactly which events reach them and where.

## Channels

- **In-app** — a live notification centre inside the app, updated as things happen.
- **E-mail** — delivered through your server's [SMTP relay](/en/email.html). Actionable e-mails (an assignment, a mention) carry a deep link that opens the exact issue in the app.
- **Push** — mobile push notifications delivered through the [Hinata Connect gateway](/en/connect-gateway.html), so a published app can notify users of any self-hosted server without each server owning Firebase credentials.

!!! info "E-mail needs a real relay"
    In-app notifications work out of the box. For e-mail to actually be delivered — including verification and password-reset links — the server needs a real SMTP relay configured. See [E-mail & SMTP](/en/email.html).

## What triggers a notification

Typical events include:

- **Assignment** — an issue is assigned to you.
- **Mentions** — someone `@`-mentions you in a description or comment.
- **Comments** — new activity on an issue you're involved with.
- **Status changes** — an issue you follow moves through the workflow.
- **Sprint events** — sprint start/complete and related planning changes.
- **Invites** — you're invited to the workspace or a team.
- **Security** — sign-ins and account-security events (always on — you can't silence these).

## The notification matrix

In **Settings → Notifications**, each user gets a matrix: a row per event type, a column per channel. Two master switches turn e-mail and push on or off wholesale, and the matrix fine-tunes the rest. Turn off comment e-mails but keep mention e-mails; get push for assignments but not for digests — whatever fits how you work.

!!! tip "Set it once, forget it"
    Encourage new team members to spend thirty seconds on their matrix during onboarding. Well-tuned notifications are the difference between a tool people trust and one they mute entirely.

Security-related notifications are locked on by design, so account-safety events always reach you.

## Next steps

- Configure delivery: [E-mail & SMTP](/en/email.html) and the [Connect gateway](/en/connect-gateway.html).
- Manage your own preferences under [Account & settings](/en/authentication.html).
