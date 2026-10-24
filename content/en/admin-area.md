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
    is also restricted to admins on the server. Other users never see it,
    organization admins included.

!!! note "Admins run the platform, not the projects"
    The `ADMIN` role gives no view into other people's work. An admin only
    sees the projects, teams, issues, boards, pages, search hits and time
    entries they are a member of. Working time, approvals, absences, holidays,
    time tags, lock exceptions and billing are no longer here. They live on the
    [Organization](/en/organization.html) page and belong to organization
    admins.

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

- **General**, **Platform**, **Security** and **Moderation**
- **Authentication**, **E-mail** and **Git integration**
- **Audit log** and **Users**

### Holidays of the platform

Under **General**, next to time zone and language, you choose the region whose statutory holidays the organization gets, for example Germany or Bavaria. **Automatic** takes the country of the time zone, **None** creates no calendar. The server makes a holiday calendar from the region and fills it every year on its own. When you change the region, that calendar follows it. What the organization makes of it is up to the organization, see [Holidays](/en/organization.html#holidays).

### Users

Manage the people on your instance:

- **approve** pending registrations
- **enable** or disable accounts
- assign **roles**: **Admin** (`ADMIN`), **Organization admin**
  (`ORG_ADMIN`) and **Moderation** (`MODERATOR`). The three are independent,
  so a person can hold one, several or none. Select several people to make
  them organization admins, or to take the role away, in one go. You hand out
  moderation in the person's panel.
- change a person's **sign-in address**

A few rules apply to the roles. You cannot make yourself an organization
admin, another administrator has to do that. This is a transparency measure,
not a hard barrier: with a second administrator account the role could still
be granted. That is why every grant is recorded in the audit log, which cannot
be switched off, and every organization admin is notified. The last organization admin
cannot be removed, deactivated or deleted. When someone joins the role or
leaves it, every organization admin gets a notification. The same holds for
moderation: not to yourself, the last person with the role stays, every grant
is in the audit log, and everyone who moderates hears about it.

When you change a person's sign-in address, they are told at their old
address. For one day after that, no password reset reaches them, neither from
the admin area nor from the public "forgot password" page. That page then
quietly sends nothing. That way nobody can quietly take over an account through the new
address.

After the update to a version with organization admins, every existing admin
is also an organization admin once, so nothing stops working. This is
recorded for each person in the audit log, and each of them gets a
notification. If you want the
roles apart, separate them here on purpose. See
[Organization](/en/organization.html).

With the update to a version with moderation, every existing admin also
becomes a moderator once, so that reports reach somebody from the start. That
too is recorded for each person in the audit log. The notification suggests
handing the role to people who do not run the platform.

When self-registration with admin approval is on (see below), new sign-ups wait
here until an admin lets them in.

### Platform

Three cards: what clients your server accepts, how people sign in, and what this
platform offers.

- **Minimum version** (`minVersion`): the
  [version gate](/en/clients.html#version-gate). Older clients are forced to
  update. Overrides `HINATA_APP_MIN_VERSION`.
- **Privacy policy URL**: the link the app shows. Required for App Store and
  Play releases and for GDPR. Overrides `HINATA_PRIVACY_POLICY_URL`.
- **Sign-in**: local authentication, self-registration and admin approval.
  While self-registration lets people in without approval, a warning under the
  switches says what that means (see **Who comes in** below).
- **Platform behaviour**: several people on one issue, replying to an issue by
  e-mail, and **project templates** (copying a project, the template marker and
  deadlines kept as an offset from the project's event date). Left off, projects
  behave exactly as they do today. That switch has three positions, because
  empty means `HINATA_PROJECT_TEMPLATES_ENABLED` decides. See
  [Project templates](/en/project-templates.html). Whether deadlines count
  calendar days or working days is up to organization admins.
- **Shift planning**: events with shifts that people sign up for. This switch
  has three positions too, and empty means `HINATA_SHIFTS_ENABLED` decides.
  Shift planning needs a MongoDB replica set. On a server without one, the row
  shows the note **Needs a MongoDB replica set** instead of the switch. See
  [Shift planning](/en/shifts.html).
- **Extended time tracking**: here you only see whether it is on. It is set up
  on the [Organization](/en/organization.html) page. If you are an
  organization admin too, the row takes you there. Every switch and policy is
  explained in [Time tracking administration](/en/admin-time-tracking.html).

!!! tip "These override the environment"
    Anything under Platform wins over the matching `hinata.app.*`
    environment variable. Env values are only the starting point for a fresh
    instance.

### Moderation

When a way in lets people in without anybody deciding, the section starts
with **Who comes in**: self-registration without approval, or an SSO provider
that creates active accounts at the first sign-in. Whoever has such an account
reads organization-wide pages and the directory. Under the Digital Services Act
that content then counts as public, and the instance has the duties of an
online platform. **Switch approval on** closes every way listed and saves.
Hinata closes them itself when it is updated to this version and on every new
instance, and tells every admin. Opening one again takes an explicit
confirmation on save. Every change is recorded in the audit log.

If requests come through a proxy the server does not trust, a warning above the
cards says so for a day: every client then counts as the proxy's address. Set
`HINATA_TRUSTED_PROXIES`, see [Reverse proxy & TLS](/en/reverse-proxy.html).

Then five cards:

- **Who moderates**: everyone with the moderation role. They review reported
  content and decide on it, see only what was reported, and have no access to
  the admin area. When only one person moderates, the card says two are
  better, so that nobody decides on a report about themselves.
- **Contact for reports**: operator, email address and a link to the imprint.
  This is how people reach whoever runs the instance. The app stores require a
  published contact, the Digital Services Act a point of contact (Art. 11 and
  12). Without signing in, the contact is in `/api/v1/meta`. While the email
  address is missing, the card shows a warning. An address in
  `HINATA_MODERATION_CONTACT_EMAIL` applies as long as none is entered here.
- **File types**: one switch per group, namely images, PDF, Office
  documents, text and spreadsheets, ZIP and voice messages. Files of a group
  that is switched off can no longer be attached, put into texts or sent. The
  switches only narrow the server's safe list. SVG or programs can never be
  allowed here. Avatars and the logo are exempt. More on this under
  [Object storage](/en/storage.html).
- **House rules**: what everybody agrees to before writing. **Standard** is
  built in, in nine languages, and names your contact. **Own text** takes
  Markdown, **Address** a page of your own (https). Whatever you choose, the
  server adds **How we moderate**: how to report, that a person reviews every
  report, whether texts are checked, what happens next and how long records are
  kept. Every saved change makes a new version that never changes again, so
  every agreement and every decision points to the words it was given. A new
  version does not ask anybody again; **Ask everybody to agree again** does.
  Until a person agrees, they get no new access token and no AI client gets
  their consent. Anybody can read the rules without an account at
  `/api/v1/public/rules`, any earlier version with `?version=N`.
- **Automatic text check**: which texts the server refuses when they are
  saved, and whether it sends unclear cases to moderation. More on this just
  below.

The automatic text check compares texts with word lists when they are saved:
issues, comments, knowledge pages, name, position and pronouns in a profile,
usernames and the names of AI clients. That holds on every way in, in the app,
over MCP, from mail and from Git. None of it leaves the server. Code, logs and
technical terms such as `kill -9` set nothing off. The card has:

- **Refuse clear violations**, on. Threats, hate speech and the like are not
  saved. The writer sees which word it was and keeps the draft.
- **Send unclear cases to moderation**, off, also after the update. When it is
  on, the text is saved and moderation gets a report without a reporter, only
  for new finds from the built-in lists. The system then checks your members'
  texts itself. Depending on your organisation that first needs the consent of
  your staff representatives, in Germany under § 87(1) no. 6 BetrVG or the
  law on staff representation in the public sector, and a data protection
  impact assessment under Art. 35 GDPR. That is why the server asks once more
  when it is turned on.
- **Own terms** are always refused, however they are spelled. They never send
  anything to moderation, or any mention of a name or of the works council
  could be routed there.
- **Exceptions** are words that are harmless for you, such as technical terms.
  Content that endangers children stays blocked all the same. Both lists take
  up to 500 terms of 60 characters each.
- **Try a text** shows what the server would do with a text, with the saved
  settings. The text is neither stored nor counted.

The built-in lists cover German and English. For other languages only your own
terms work. The text check does not look at images and attachments; reports
cover those. **How we moderate** names your own terms and whether unclear cases
go to moderation. Every change of the switches and lists is in the audit log. A
refused mail becomes no issue and gets no reply. Its connection under
**E-mail** counts how many there were.

### Authentication & SSO

Set how people sign in:

- turn **local authentication**, **self-registration** and **admin approval**
  on or off
- register **SSO providers**: OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP
  (Synology SSO, Keycloak, Authentik, Azure AD, Google, …)
- per provider, **New accounts need approval**: the first sign-in waits like a
  registration. Or name **Allowed email domains**: only those come in straight
  away, everyone else waits. With neither, the provider lets in whoever it
  knows, and a warning under its switches says so.

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
Mongo and applies without a restart. You can only route mail into projects
you are a member of. See
[E-mail to ticket](/en/email-to-ticket.html).

### Audit log

Shows the platform's records: sign-ins, accounts, configuration and
integrations.

- Records about working time, timesheets and absences, sick reports included,
  are not shown here. They are only on the log of the
  [Organization](/en/organization.html) page. Organization admins decide which
  of them are recorded. You cannot change those switches, and the audit log's
  master switch does not silence them.
- Records about issues and pages appear without their details, so without
  issue keys and without page ids.
- Changes to the admin and organization admin roles, and any change of a
  sign-in address by an administrator, are always recorded. You cannot switch
  that off.

## Where to go next

- [Single sign-on](/en/sso.html): connect an identity provider.
- [Git integration](/en/git-integration.html): OAuth apps and per-project repos.
- [E-mail to ticket](/en/email-to-ticket.html): turn inbound mail into issues.
- [Authentication](/en/authentication.html): accounts, registration and 2FA.
- [Organization](/en/organization.html): time tracking, absences and deadlines for the whole organization.
