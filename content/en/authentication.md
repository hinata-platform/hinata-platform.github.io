---
title: Authentication
description: How users sign in to Hinata, with passwords, self-registration, email verification, password reset, admin approval, 2FA and sessions.
---

# Authentication

Hinata ships a complete local authentication system:

- username/password login
- optional self-registration with email verification
- forgot password, with a deep link into the app
- optional admin approval of new accounts
- time-based two-factor authentication

You toggle every mode at runtime from the Admin area, with no restart or redeploy.

For federated login (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP) see [Single sign-on](/en/sso.html). Hardening and the threat model are covered in the [Security model](/en/security.html).


![Hinata account settings](/assets/img/shot-settings.png)
*Account settings with profile, security, 2FA, sessions and notifications.*

## Local credentials

Users sign in with a username (or email) and password. Passwords are hashed with **BCrypt (strength 12)** and never stored or logged in the clear. On success the server issues a short-lived **JWT access token** and a **refresh token**. The app stores both per server and refreshes them automatically.

Password rules enforced by the server:

- **Minimum 10 characters.** Length is the strongest lever against brute force.
- Hashed with BCrypt strength 12, so each verification is deliberately slow.

!!! tip "Length over complexity"
    Hinata requires length instead of lots of special-character rules. A 10+ character passphrase is stronger and easier to remember. Encourage your users to use a password manager.

## Feature flags: AuthPolicy

Three flags control local authentication. They live in an **AuthPolicy** stored in MongoDB and are editable from **Admin → Users / App**. The database value overrides the environment default and takes effect **without a restart**.

| Flag | What it controls | Typical default |
| --- | --- | --- |
| `localAuthEnabled` | Whether username/password login is allowed at all. Turn it **off** to force SSO only. | `true` |
| `registrationEnabled` | Whether visitors can self-register from the app. Off means admins create every account. | depends on deployment |
| `requireAdminApproval` | Whether a newly registered (and email-verified) account must be approved by an admin before it can sign in. | `false` |

The app reads the effective policy from the public `/api/v1/meta` endpoint on launch and adapts the login screen. With registration off, the register link is hidden. With local auth off, the password form is hidden.

!!! info "SSO-only deployments"
    Set `localAuthEnabled = false` once your SSO provider is configured and every user has a federated identity. The password form disappears and only the SSO buttons remain. You can always turn it back on to recover access.

## Self-registration and email verification

When `registrationEnabled` is on, the app shows a **Create account** flow:

1. The visitor submits a display name, username, email and password (checked against the password rules above).
2. The server creates the account as **unverified** and emails a verification link.
3. The link opens the app (deep link) or the web build and confirms the email with the server.
4. If `requireAdminApproval` is on, the account then waits as **pending** until an admin approves it under **Admin → Users**. Otherwise the user can sign in right after verifying.

!!! warning "Email must actually work"
    Verification, approval and password reset all depend on outbound mail. Configure `HINATA_SMTP_*` and `HINATA_MAIL_FROM` before enabling self-registration, and confirm delivery. See [E-mail & SMTP](/en/email.html). In development the stack ships Mailpit, so you can read every message locally.

### Optional admin approval

With `requireAdminApproval = true`, verified accounts land in a pending list. Admins approve or reject them under **Admin → Users**. This is the recommended setup for an open registration form on a public network: anyone can request access, and a person decides.

## Forgot password

The reset flow runs in the app and reveals nothing about which addresses exist:

1. On the login screen the user taps **Forgot password?** and enters their email.
2. The server always responds the same way and never confirms whether an address is registered. If the account exists, it emails a reset link.
3. The link carries a single-use token and opens the app through the **`hinata://` deep link** (or an **HTTPS universal link** to `https://track.example.com` on platforms configured for it). The app renders the reset screen itself. The backend serves no password HTML.
4. The user sets a new password (again at least 10 characters) and the token is consumed.

!!! info "Why a deep link?"
    With the reset screen inside the app, there is no server-rendered password page to harden, theme and localize separately. The email only hands a token back to the client you already trust. On native platforms the app registers the `hinata://auth-callback` / reset scheme. On the web build the universal link opens the same route.

## Two-factor authentication (TOTP)

Hinata supports **time-based one-time passwords (TOTP)**: the six-digit codes from Google Authenticator, 1Password, Aegis and similar apps.

### Enabling 2FA

From **Settings** (the `/settings` account screen) a user opens the two-factor section:

1. The server generates a TOTP secret and returns an `otpauth://` provisioning URI, shown as a QR code.
2. The user scans it with their authenticator app.
3. They enter a current 6-digit code, which activates 2FA on the account.

### The login 2FA challenge

With TOTP enabled, login takes two steps:

1. The user submits username and password. If the credentials are valid, the server responds with a **2FA challenge** instead of tokens.
2. The app asks for the current 6-digit code. Only after a correct code does the server issue the access and refresh tokens.

!!! tip "Keep a recovery path"
    Treat the authenticator device as a credential. If a user loses it, an admin can reset the account's second factor from the Admin area so the user can re-enrol.

## Sessions

Every successful login creates a record in a **`sessions` collection** in MongoDB. The issued JWT carries a **session id (`sid`) claim** that ties the token to that record. That makes tokens individually revocable: signing out or revoking a session invalidates its `sid`. A leaked token can be killed without rotating the global signing secret.

### Session management

From **Settings** users see their active sessions (device / client, last activity) and can **revoke** any of them, for example after signing in on a shared machine. A revoked session's tokens are rejected immediately.

!!! note "Refresh tokens are for refresh only"
    Access and refresh tokens are distinct. A refresh token is accepted **only** at the refresh endpoint to mint a new access token. The rest of the API rejects it. See the [Security model](/en/security.html) for the full token design.

## Account, privacy and avatar

The same `/settings` screen is where users manage their own account:

- **Profile**: display name and details.
- **Email change**: the new address is verified again.
- **Notification matrix**: in-app and e-mail preferences per category.
- **Avatar upload**: a profile picture stored in S3/MinIO. Uploaded via the account API, served through a private-bucket proxy, capped and re-encoded server-side. Users can upload or remove it at any time.
- **GDPR export & delete**: users can **export** their personal data and **delete** their account themselves. That covers data portability and the right to erasure without an admin ticket.

!!! info "GDPR by design"
    Hinata is self-hosted, so the data never leaves your infrastructure. With export and delete built into the app, you can answer access and erasure requests directly.

## Where to go next

- **[Single sign-on](/en/sso.html)**: replace or complement local login with OIDC, OAuth 2.0, SAML 2.0 or LDAP.
- **[Security model](/en/security.html)**: JWT design, rate limiting, login lockout, headers and the OWASP mapping.
- **[Admin area](/en/admin-area.html)**: where the AuthPolicy flags, user approval and app settings live.
