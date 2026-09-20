---
title: Admin area
description: Manage users, app settings, SSO, Git and mail-to-ticket on a running server.
---

# Admin area

In the **Admin area** you configure most of Hinata directly in the app. Settings
are stored in MongoDB, **override the environment** and apply **without a
restart**.

!!! info "Who can access it"
    Only users with the **`ADMIN`** role. Every endpoint under `/api/v1/admin/**`
    is also restricted to admins on the server. Other users never see it.

![Hinata admin area](/assets/img/shot-admin.png)
*Users, app settings, SSO, Git and mail-to-ticket in one place.*

## How runtime configuration works

To start, a server only needs a few environment variables: a JWT secret, the
database connection and a mail relay. SSO providers, e-mail ingest, Git OAuth
apps and app settings are set up in the Admin area and stored in MongoDB. The
rules:

- **DB overrides env.** Environment values such as `hinata.app.*` are only
  *defaults*. A value you set in the Admin area wins.
- **No restart required.** Changes to a provider or flag apply from the next
  request, with no redeploy or container restart.
- **Secrets are write-only.** You can **set** OAuth client secrets, tokens and
  passwords, but the admin API never returns them. Stored Git tokens are also
  encrypted at rest with AES-GCM.

## The sections

The Admin area has three groups:

- **General**, **App** and **Security**
- **Authentication**, **E-mail** and **Git integration**
- **Audit log** and **Users**

### Users

Manage the people on your instance:

- **approve** pending registrations
- **enable** or disable accounts
- assign **roles**, including `ADMIN`

When self-registration with admin approval is on (see below), new sign-ups wait
here until an admin lets them in.

### App settings

Control how clients behave against your server:

- **Minimum version** (`minVersion`): the
  [version gate](/en/clients.html#version-gate). Older clients are forced to
  update. Overrides `HINATA_APP_MIN_VERSION`.
- **Privacy policy URL**: the link the app shows. Required for App Store and
  Play releases and for GDPR. Overrides `HINATA_PRIVACY_POLICY_URL`.
- **Feature flags**: turn platform features on or off. This includes the sign-in
  flags `localAuthEnabled`, `registrationEnabled` and `requireAdminApproval`,
  plus any `name → enabled` flags you add.
- **Project templates**: turns on copying a project, the template marker and
  deadlines kept as an offset from the project's event date. Left off, projects
  behave exactly as they do today. The switch has three positions, because
  empty means `HINATA_PROJECT_TEMPLATES_ENABLED` decides. See
  [Project templates](/en/project-templates.html).

!!! tip "These override the environment"
    Anything under App settings wins over the matching `hinata.app.*`
    environment variable. Env values are only the starting point for a fresh
    instance.

### Authentication & SSO

Set how people sign in:

- turn **local authentication**, **self-registration** and **admin approval**
  on or off
- register **SSO providers**: OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP
  (Synology SSO, Keycloak, Authentik, Azure AD, Google, …)

Providers are stored in Mongo and apply immediately. See
[Authentication](/en/authentication.html) and [Single sign-on](/en/sso.html).

### Git integration

Register **one OAuth app per provider** (GitHub, GitLab, Bitbucket) so projects
can connect their repositories. You enter:

- the client id and secret
- the public API base URL for the OAuth callback and webhooks
- optionally, a secret for encrypting tokens

You set this up once for the whole platform. Projects then connect individual
repos in their own settings. See [Git integration](/en/git-integration.html).

### E-mail (mail-to-ticket)

Set up **IMAP polling** so inbound e-mail becomes issues. This is also stored in
Mongo and applies without a restart. See
[E-mail to ticket](/en/email-to-ticket.html).

### Audit log

Shows administrative and security-relevant actions on the instance.

## Where to go next

- [Single sign-on](/en/sso.html): connect an identity provider.
- [Git integration](/en/git-integration.html): OAuth apps and per-project repos.
- [E-mail to ticket](/en/email-to-ticket.html): turn inbound mail into issues.
- [Authentication](/en/authentication.html): accounts, registration and 2FA.
