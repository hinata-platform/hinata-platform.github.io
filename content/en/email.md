---
title: E-mail & SMTP
description: Configure outbound mail so Hinata can deliver assignment, verification and password-reset e-mails — Mailpit in dev, a real SMTP relay in production.
---

# E-mail & SMTP

Hinata sends transactional e-mail over **SMTP**: issue-assignment notifications,
e-mail verification for new accounts, and password-reset links. In local
development these are captured by **Mailpit** so you can read them in a browser; in
production you point Hinata at a **real SMTP relay** so those messages actually
reach people's inboxes.

!!! info "Inbound mail is a separate feature"
    This page is about *outbound* mail. Turning incoming e-mail into issues
    (IMAP polling) is configured in the Admin area and documented on its own page:
    [E-mail to ticket](/en/email-to-ticket.html).

## Configuration variables

| Variable | Purpose | Dev default |
| --- | --- | --- |
| `HINATA_SMTP_HOST` | SMTP server hostname | `mailpit` |
| `HINATA_SMTP_PORT` | SMTP port | `1025` |
| `HINATA_SMTP_USERNAME` | SMTP auth username | *(empty)* |
| `HINATA_SMTP_PASSWORD` | SMTP auth password | *(empty)* |
| `HINATA_SMTP_AUTH` | Enable SMTP authentication | `false` |
| `HINATA_SMTP_STARTTLS` | Upgrade the connection with STARTTLS | `false` |
| `HINATA_MAIL_FROM` | From address on outgoing mail | `hinata@localhost` |
| `HINATA_WEB_BASE_URL` | Where e-mail deep links point (the Flutter web app) | *(falls back to base URL)* |

Every value is a plain environment variable — set them in `.env` or directly on the
container.

## Development: Mailpit

The dev stack (`docker-compose.dev.yml`) includes Mailpit, which accepts mail on
`localhost:1025` and shows every message in a web UI:

```bash
docker compose -f docker-compose.dev.yml up -d   # includes Mailpit
```

Open **`http://localhost:8025`** to read whatever Hinata sends. No credentials, no
STARTTLS — Mailpit swallows everything, which is exactly what you want while
developing. Because the default `HINATA_SMTP_HOST` is `mailpit` (and `mailpit`/`1025`
in the compose network), you don't have to configure anything for local mail to work.

!!! warning "Mailpit never delivers"
    Mailpit is a trap that *displays* mail; it does not forward it to real inboxes.
    If verification or reset e-mails aren't arriving in production, the cause is
    almost always that a real relay was never configured and Hinata is still talking
    to a dev mail catcher.

## Production: a real SMTP relay

For a production server, point Hinata at an SMTP relay you control or subscribe to.
A typical STARTTLS configuration on port 587:

```properties
HINATA_SMTP_HOST=smtp.example.org
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.org
HINATA_SMTP_PASSWORD=your-smtp-password
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=Hinata <hinata@example.org>
```

That covers the vast majority of relays — provider SMTP, a transactional-mail
service, or your own Postfix. Set `HINATA_SMTP_AUTH=true` and provide credentials
whenever the relay requires a login (almost always the case for a hosted relay).

!!! danger "MAIL_FROM often must match an authenticated identity"
    Many relays reject a message whose `From` address is not an identity you're
    authenticated and authorized to send as (SPF/DKIM alignment). If mail is
    silently dropped or bounced with a "sender not allowed" error, make
    `HINATA_MAIL_FROM` match a verified sender/domain on your relay — this is the
    single most common outbound-mail gotcha.

## Deep links: where the e-mails point

The links inside Hinata's e-mails — "open this issue", "verify your address", "reset
your password" — must open your **Flutter web app**, not the API. That target is
`HINATA_WEB_BASE_URL`:

```properties
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com
```

If `HINATA_WEB_BASE_URL` is blank, deep links fall back to `HINATA_BASE_URL`. On a
split host/API deployment (the common case) that would send users to the API domain,
so **set `HINATA_WEB_BASE_URL` explicitly** to your web app's public URL.

!!! tip "Reset and verification links are backend-free"
    Password reset and verification happen through the app via these deep links —
    the server does not render its own HTML pages for them. Getting
    `HINATA_WEB_BASE_URL` right is what makes those flows land on a working screen.

## Testing your configuration

1. Set the SMTP variables and restart the server.
2. Trigger a real message — for example request a password reset, or assign an issue
   to a teammate with notifications enabled.
3. Confirm delivery (check the inbox, or your relay's outbound log). In dev, watch
   Mailpit at `http://localhost:8025`.
4. If nothing arrives: re-check `HINATA_MAIL_FROM` against your relay's allowed
   senders, confirm the port/STARTTLS pairing (587 + STARTTLS, or 465 for implicit
   TLS), and make sure `HINATA_SMTP_AUTH=true` when credentials are required.

For the full variable catalogue see the
[Configuration reference](/en/configuration.html); for inbound mail-to-issue see
[E-mail to ticket](/en/email-to-ticket.html).
