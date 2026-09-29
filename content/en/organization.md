---
title: Organization
description: The organization admin role and the Organization page with working time, approvals, absences, holidays, billing and deadlines.
---

# Organization

Hinata has two roles for work that goes beyond a single project. **Administrators** run the platform. **Organization admins** look after working time, absences and billing for the whole organization. The two roles are independent. A person can hold one of them, both or neither.

## Two roles

| Role | What it is for | Where it works |
| --- | --- | --- |
| **Administrator** (`ADMIN`) | Accounts, sign-in and SSO, server settings, e-mail, Git and the audit log | [Admin area](/en/admin-area.html) |
| **Organization admin** (`ORG_ADMIN`) | Working time with extended time tracking, timesheet approvals, absences, holiday calendars, time tags, lock exceptions, billing and the default for relative deadlines | **Organization** page in the app |

You assign both roles in **Admin area → Users**. Organization admins have no access to the admin area.

### Rules for the organization admin role

- As an administrator you cannot make yourself an organization admin. Another administrator has to do it. This rule is there for transparency, it is not a hard barrier: someone with a second administrator account can still grant themselves the role that way. That is why every grant is recorded in the audit log and every organization admin gets a notification.
- The last organization admin cannot be removed, deactivated or deleted. Appoint someone else first.
- When someone joins the role or leaves it, every organization admin gets a notification.
- Every change to the admin and organization admin roles goes into the audit log. You cannot switch that off.

!!! info "Neither role opens other people's projects"
    An administrator only sees the projects, teams, issues, boards, knowledge base pages, search hits and time entries they are a member of, just like everyone else. Running the platform is not a reason to read other people's work. Organization admins also only see project content through their own membership. They do see every time entry, because approvals, corrections and billing need that. How far that goes is explained below under [Reports and exports](#reports-and-exports).

## The Organization page

As an organization admin you find an **Organization** row in your **Settings**. Nobody else sees it. It holds everything that applies to the whole organization:

- **Time tracking**: extended time tracking and its policies, such as rounding, the lock date, timesheet approvals, the privacy notice and retention. See [Time tracking privacy](/en/time-tracking-privacy.html).
- **Absences**: absence management with types, entitlements and balances, plus the people who may help keep them.
- **Holidays**: the holiday calendars, kept by hand or imported from a calendar address.
- **Time tags**, **lock exceptions** and days opened for single people.
- **Billing**: rates, costs and invoices.
- **Day count**: whether the organization counts in calendar days or working days, for new relative deadlines and as the default for notification times.
- **Log**: the audit log records about working time, timesheets and absences. Administrators do not see them. More under [The organization's log](#the-organizations-log).

There are day-to-day duties too: organization admins decide timesheets and absence requests when nobody else is there to do it, open locked days on request and may import entries for other people.

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

On a new install, the first person the [setup wizard](/en/setup-wizard.html) creates gets both roles.

## Where to go next

- [Tracking your time](/en/guide-time.html): working hours, absences and reports from a user's point of view.
- [Time tracking privacy](/en/time-tracking-privacy.html): the policies in detail.
- [Admin area](/en/admin-area.html): what administrators manage.
