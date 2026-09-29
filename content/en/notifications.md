---
title: Notifications
description: In-app, e-mail and push notifications, tuned per event by each user.
---

# Notifications

Hinata keeps people informed through three channels. Each user decides which events reach them and where.

## Channels

- **In-app**: a notification centre inside the app that updates as things happen.
- **E-mail**: sent through your server's [SMTP relay](/en/email.html). E-mails you can act on (an assignment, a mention) carry a deep link that opens the exact issue in the app.
- **Push**: on Android, iOS, macOS and Windows, delivered through the [Hinata Connect gateway](/en/connect-gateway.html). That way a published app can notify users of any self-hosted server without each server owning Firebase credentials.

!!! info "E-mail needs a real relay"
    In-app notifications work out of the box. For e-mail to actually arrive, including verification and password reset links, the server needs a real SMTP relay configured. See [E-mail & SMTP](/en/email.html).

## What triggers a notification

Typical events:

- **Assignment**: an issue is assigned to you.
- **Mentions**: someone `@`-mentions you in a description or comment.
- **Comments**: new activity on an issue you're involved with.
- **Status changes**: an issue you follow moves through the workflow.
- **Sprint events**: a sprint starts or completes, and related planning changes.
- **Invites**: you're invited to the workspace or a team.
- **Security**: sign-ins and account security events. These are always on and cannot be silenced.

## The notification matrix

In **Settings → Notifications** each user gets a matrix: one row per event type, one column per channel.

- Two master switches turn e-mail and push on or off completely.
- The matrix handles the rest. For example: comment e-mails off, mention e-mails on. Or push for assignments but not for digests.
- **Notification times** set when e-mail and push may arrive: **Always**, or **Custom** on chosen weekdays between **From** and **Until** in the person's time zone. Without a choice of their own, the organisation decides through the day count on the organisation page: with working days everybody gets "Custom" with the working days where they live and 9:00 to 17:00, otherwise "Always". Outside those times the bell shows everything at once, while e-mail and push wait and go out when the next window begins, as one summary e-mail and one push (a job checks every five minutes). Security messages and important notices, such as expiring leave, always arrive. After the update everyone gets one note in the bell.

!!! tip "Set it once, forget it"
    Ask new team members to spend thirty seconds on their matrix during onboarding. People trust a tool with well-tuned notifications. Otherwise they tend to mute it entirely.

Security notifications are locked on, so account security events always reach you.

## Next steps

- Configure delivery: [E-mail & SMTP](/en/email.html) and the [Connect gateway](/en/connect-gateway.html).
- Manage your own preferences under [Account & settings](/en/authentication.html).
