---
title: E-mail & SMTP
description: Configure outbound mail for assignment, verification and password-reset e-mails, with Mailpit in dev and a real SMTP relay in production.
---

# E-mail & SMTP

Hinata sends e-mail over **SMTP**:

- notifications when an issue is assigned to you
- e-mail verification for new accounts
- password-reset links

In local development **Mailpit** captures these, and you read them in a browser. In production you need a **real SMTP relay** so they reach people's inboxes.

!!! info "Inbound mail is a separate feature"
    This page covers *outbound* mail. Turning incoming e-mail into issues (IMAP polling) is configured in the Admin area, see [E-mail to ticket](/en/email-to-ticket.html).

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
| `HINATA_WEB_BASE_URL` | Where e-mail links point (the Flutter web app) | *(falls back to base URL)* |

Every value is a plain environment variable. Set them in `.env` or directly on the container.

## Development: Mailpit

The dev stack (`docker-compose.dev.yml`) includes Mailpit. It accepts mail on `localhost:1025` and shows every message in a web UI:

```bash
docker compose -f docker-compose.dev.yml up -d   # includes Mailpit
```

Open **`http://localhost:8025`** to read whatever Hinata sends. Mailpit needs no credentials or STARTTLS and accepts every message. The default `HINATA_SMTP_HOST` is `mailpit` (`mailpit`/`1025` in the compose network), so local mail works without any config.

!!! warning "Mailpit never delivers"
    Mailpit only *displays* mail and does not forward it to real inboxes. If verification or reset e-mails don't arrive in production, a real relay was almost always never configured and Hinata is still talking to a dev mail catcher.

## Production: a real SMTP relay

Point Hinata at an SMTP relay you run yourself or subscribe to. A typical STARTTLS setup on port 587:

```properties
HINATA_SMTP_HOST=smtp.example.org
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.org
HINATA_SMTP_PASSWORD=your-smtp-password
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=Hinata <hinata@example.org>
```

That covers almost every relay: your provider's SMTP, a transactional mail service or your own Postfix. If the relay requires a login (almost always true for hosted relays), set `HINATA_SMTP_AUTH=true` and provide credentials.

!!! danger "MAIL_FROM often must match an authenticated identity"
    Many relays reject a message whose `From` address is not an identity you are authenticated and authorized to send as (SPF/DKIM alignment). If mail is dropped without notice or bounced with "sender not allowed", set `HINATA_MAIL_FROM` to a verified sender or domain on your relay. This is the most common outbound mail problem.

## Deep links: where the e-mails point

Links in Hinata's e-mails ("open this issue", "verify your address", "reset your password") must open your **Flutter web app**, not the API. `HINATA_WEB_BASE_URL` sets that target:

```properties
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com
```

If `HINATA_WEB_BASE_URL` is blank, links fall back to `HINATA_BASE_URL`. When web app and API run on separate hosts (the common case), users would land on the API domain. So **set `HINATA_WEB_BASE_URL` explicitly** to your web app's public URL.

!!! tip "Reset and verification happen in the app"
    Both flows run through these deep links in the app. The server renders no HTML pages of its own for them. Only a correct `HINATA_WEB_BASE_URL` makes the links land on a working screen.

## Testing your configuration

1. Set the SMTP variables and restart the server.
2. Trigger a real message, for example a password reset or assigning an issue to a teammate with notifications enabled.
3. Confirm delivery in the inbox or your relay's outbound log. In dev, watch Mailpit at `http://localhost:8025`.
4. If nothing arrives:
   - Compare `HINATA_MAIL_FROM` with your relay's allowed senders.
   - Check the port and STARTTLS pairing (587 with STARTTLS, or 465 for implicit TLS).
   - Set `HINATA_SMTP_AUTH=true` when credentials are required.

For all variables see the [Configuration reference](/en/configuration.html). For inbound mail-to-issue see [E-mail to ticket](/en/email-to-ticket.html).
