---
title: Organization
description: The organization admin role and the Organization page with working time, approvals, absences, holidays, billing and deadlines.
---

# Organization

Hinata has three roles for work that goes beyond a single project. **Administrators** run the platform. **Organization admins** look after working time, absences and billing for the whole organization. **Moderators** review reported content and decide on it. The three roles are independent. A person can hold one of them, several or none.

## Three roles

| Role | What it is for | Where it works |
| --- | --- | --- |
| **Administrator** (`ADMIN`) | Accounts, sign-in and SSO, server settings, e-mail, Git and the audit log | [Admin area](/en/admin-area.html) |
| **Organization admin** (`ORG_ADMIN`) | Working time with extended time tracking, timesheet approvals, absences, holiday calendars, time tags, lock exceptions, billing and the default for relative deadlines | **Organization** page in the app |
| **Moderation** (`MODERATOR`) | Reviewing reported content and people and deciding on them, with reasons sent to everyone involved | **Moderation** page in the app |

You assign all roles in **Admin area → Users**. Organization admins and moderators have no access to the admin area.

### Rules for the organization admin role

- As an administrator you cannot make yourself an organization admin. Another administrator has to do it. This rule is there for transparency, it is not a hard barrier: someone with a second administrator account can still grant themselves the role that way. That is why every grant is recorded in the audit log and every organization admin gets a notification.
- The last organization admin cannot be removed, deactivated or deleted. Appoint someone else first.
- When someone joins the role or leaves it, every organization admin gets a notification.
- Every change to the admin and organization admin roles goes into the audit log. You cannot switch that off.

### Rules for the moderation role

- Nobody gives themselves the role, as with organization admins. Every grant is in the audit log, and everyone who moderates gets a notification.
- The last person with the role cannot be removed, deactivated or deleted. Appoint someone else first.
- At least two are good, so that nobody decides on a report about themselves.

!!! info "None of these roles opens other people's projects"
    An administrator only sees the projects, teams, issues, boards, knowledge base pages, search hits and time entries they are a member of, just like everyone else. Running the platform is not a reason to read other people's work. Organization admins also only see project content through their own membership. They do see every time entry, because approvals, corrections and billing need that. How far that goes is explained below under [Reports and exports](#reports-and-exports). Moderators see only what was reported, with the least context needed.

## The Organization page

As an organization admin you find an **Organization** row in your **Settings**. Nobody else sees it. It holds everything that applies to the whole organization:

- **Time tracking**: extended time tracking and its policies, such as rounding, the lock date, timesheet approvals, the calendar import, the privacy notice and retention. See [Time tracking privacy](/en/time-tracking-privacy.html).
- **Absences**: absence management with types, entitlements and balances, plus the people who may help keep them.
- **Holidays**: the holiday calendars. A calendar follows a region, comes from a calendar address or is kept by hand. More under [Holidays](#holidays).
- **Time tags**, **lock exceptions** and days opened for single people.
- **Billing**: rates, costs and invoices.
- **Day count**: whether the organization counts in calendar days or working days, for new relative deadlines and as the default for notification times.
- **Log**: the audit log records about working time, timesheets and absences. Administrators do not see them. More under [The organization's log](#the-organizations-log).

There are day-to-day duties too: organization admins decide timesheets and absence requests when nobody else is there to do it, open locked days on request and may import entries for other people.

## Holidays

Every holiday calendar gets its days from one of three sources:

- **Region**: the statutory holidays of a country or a state, such as Bavaria or Berlin. The server knows the rules itself and needs no outside connection for them. Every new year is added on its own.
- **Calendar address**: a public holiday calendar from Google, Apple or Outlook. Here too the server reads every new year on its own, as soon as the address contains it.
- **By hand**: you enter every day yourself.

Every night and at every start the server fills the current and the next year, each year only once. If you delete or change single days afterwards, they stay that way. To have a year back the way its source has it, use the restore or import button on the calendar's card.

On a new server the platform creates the first calendar itself: **Public holidays** for the region in the platform settings, or, without one, for the country of the server's time zone. It carries the label **Set by the platform** and is the default calendar while there is no other. You can rename it, change days, add more calendars or delete it. Once you give it another source it is entirely yours and no longer follows the platform settings. A deleted calendar does not come back; only a new region in the platform settings creates one again.

## Calendar import

Under **Time tracking** the switch **Calendar import** decides whether people may subscribe to their own calendars and turn appointments into entries. It is off by default and only works with extended time tracking. Until you choose, the server's value `HINATA_TIME_TRACKING_ICS_IMPORT_ENABLED` applies. How it looks for people is in [Tracking your time](/en/guide-time.html#your-own-calendars).

- **On:** everybody finds **Calendar subscriptions** under **Settings → Time tracking**. A subscription, its address, its events and its errors are visible to its owner only. You see neither the addresses nor the events, only the entries people take over, like any other entry.
- **Off:** the calendars show no events, nothing is fetched, and the server answers requests about subscriptions as if they did not exist. What people stored stays until they delete it or their account is deleted, and it is back when you switch the import on again.

The server needs `HINATA_ICS_SECRET` for this. Without it nobody can save a subscription, and the app says that the server needs `HINATA_ICS_SECRET` to be set. Ask whoever runs the server (see [Configuration](/en/configuration.html)). Adding and removing a subscription is recorded in the audit log, with the calendar's host and never its address.

Calendar appointments can say a lot about a person. Settle in the works agreement that the import is voluntary and how private appointments are handled, see [Time tracking privacy](/en/time-tracking-privacy.html).

## Sick reports

Under **Absences** you can name people who help keep absences. Once you have named them, only they see sickness as sickness. Organization admins then only see that someone is away, not why. If nobody is named, organization admins look after absences themselves and see them in full.

## The organization's log

The log on the Organization page shows records about working time, timesheets and absences. Records about absences, meaning requests, sick reports and balances, are only shown to whoever keeps absences. That is the named absence keepers or, while nobody is named, the organization admins.

As an organization admin you decide for each event whether it is recorded (through the API `PUT /api/v1/org/settings` with `auditEvents`). Administrators cannot change these switches, and the platform's master switch for the audit log does not silence these records either.

## Reports and exports

Time reports, exports, grouped summaries and timesheet approvals show you hours, person and project key for everyone. Issue titles, issue keys, descriptions and project names you only see for projects you are a member of, and for your own entries. The description search only searches entries you may read.

## Default for relative deadlines

With [project templates](/en/project-templates.html) on, a deadline can be an offset from the project's event date, such as "4 weeks before". Under **Day count** you choose whether the organization counts in **calendar days** or **working days**. It applies to such deadlines and also as the default for [notification times](/en/guide-notifications.html#when-things-reach-you): with working days, everybody without a choice of their own gets e-mail and push only on working days from 9:00 to 17:00, with calendar days at any time. Until you choose, the server default applies, which is calendar days (see `HINATA_PROJECT_TEMPLATES_DEFAULT_BASIS` in the [configuration reference](/en/configuration.html#project-templates-and-relative-deadlines)).

Each project can differ: when it is created, when it is copied, or later in its settings under **Deadlines count in**.

The setting only preselects what a new deadline starts with. Existing deadlines keep their own basis and do not move.

## After the update

So that nothing stops working, every existing administrator also becomes an organization admin once during the update. Everything works as it did before. The hand-over is recorded for each person in the audit log, and each person gets a notification. If you want the roles apart, separate them afterwards in **Admin area → Users**. That is a deliberate step.

With the update to a version with moderation, every existing administrator also becomes a moderator once, so that reports reach somebody from the start. That too is recorded for each person in the audit log, and the notification suggests handing the role on.

On a new install, the first person the [setup wizard](/en/setup-wizard.html) creates gets all three roles.

## Where to go next

- [Tracking your time](/en/guide-time.html): working hours, absences and reports from a user's point of view.
- [Time tracking privacy](/en/time-tracking-privacy.html): the policies in detail.
- [Admin area](/en/admin-area.html): what administrators manage.
