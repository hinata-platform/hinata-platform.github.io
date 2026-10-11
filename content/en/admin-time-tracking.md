---
title: Time tracking administration
description: Switch on extended time tracking, absence management and billing, and set every policy with its effect, visibility, co-determination note and default.
---

# Time tracking administration

This page is for organization admins and operators. It covers the three module switches, every time tracking policy with its default, retention, holidays, billing and the MCP tools.

Why each setting matters legally is on [Time tracking: privacy & law](/en/time-tracking-privacy.html). How people record time is in [Tracking your time](/en/guide-time.html).

!!! info "Feature flag"
    Extended time tracking only appears when it is switched on. Organization admins switch it under **Organization → Time tracking**. Administrators see under **Admin area → Platform → Platform behaviour** whether it is on. The default comes from `HINATA_TIME_TRACKING_ADVANCED_ENABLED` (`false`). A change takes effect without a restart.

## Who sets what

- **Organization admins** (`ORG_ADMIN`) set the module switches and all policies on the [Organization](/en/organization.html) page under **Time tracking**.
- **Administrators** (`ADMIN`) choose the holiday region under **Admin area → General**. In **Admin area → Platform** they only see whether extended time tracking is on. If they are organization admins too, the row leads them there.
- **The server's environment** gives the defaults (`HINATA_TIME_TRACKING_*`). Every policy may stay empty. It then shows **Env default**, and the environment decides. A stored value wins. **Use env default** clears it again.
- Every change to the policies and the lock date is in the audit log (`TIME_POLICY_CHANGED`, `TIME_LOCK_CHANGED`).

## The modules

### Extended time tracking

- Switch **Extended time tracking** (`advancedEnabled`), default off.
- Brings timers, the calendar view, approvals, availability, reports and billing.
- Off: the plain timesheet stays exactly as it is, and the module's endpoints do not exist for the apps. Switching it off hides the module and deletes nothing.
- Environment: `HINATA_TIME_TRACKING_ADVANCED_ENABLED=false`. The app reads the client flag `advanced_time_tracking`.

### Absence management

- Switch **Absence management** (`absenceManagementEnabled`), default off. Client flag `absence_management`.
- Brings absence types, yearly entitlements, balances, requests and sick reports.
- Needs extended time tracking, because every day it counts comes from working patterns, holiday calendars and capacity. While extended time tracking is off, the switch keeps its position and has no effect.
- Switching it off loses no data. Types, entitlements, bookings and requests stay. Absences keep shaping capacity.
- Environment: `HINATA_TIME_TRACKING_ABSENCE_MANAGEMENT_ENABLED=false`.

### Billing

- Switch **Billing** (`billingEnabled`), default off. Client flag `billing`. Needs extended time tracking.
- Brings rates with a history, labour costs, billing and profitability reports, invoices and credit notes. Leads and organization admins see them. **Manage rates** opens the rates.
- All amounts are in one currency (`currency`, default `EUR`). Invoice numbers look like `INV-2026-00001`. The prefix comes only from `HINATA_TIME_TRACKING_INVOICE_PREFIX`.
- Issuing an invoice freezes it and the entries it names. The way back is a credit note (`INVOICE_CREDITED` in the audit log). It releases the entries for correction.
- Issued invoices and credit notes are never deleted (§ 147 AO, § 257 HGB). A project that has one cannot be deleted.

## Four principles

These four rules hold for every policy below. You can quote them in the agreement.

1. **Hinata never prevents the recording of working time actually performed.** Holidays, weekends, company shutdowns and absences are marked, not locked. Basis: BAG 13.09.2022, 1 ABR 22/21 and CJEU 14.05.2019, C-55/18 (CCOO); § 16 (2) ArbZG requires recording working time beyond the working-day hours, which by the prevailing reading covers all work on Sundays and public holidays. § 9 ArbZG prohibits work on public holidays, not its documentation.
2. **Only the past is ever locked, never the present or the future.** The lock date is an integrity tool for closed periods (Art. 32 GDPR; retention under § 16 (2) ArbZG / § 17 MiLoG, two years), not a steering instrument.
3. **Every immutability has a documented way back.** Lock date, approval and invoice: by correction request, reopening or credit note, always with a reason in the audit log. Without a way back the lock collides with Art. 16 GDPR: working time is personal data, and inaccurate data must be rectified without undue delay.
4. **Late recording is never refused, at most made visible.** Catching up is possible up to the policy `maxDaysBack` (default 365 days), and beyond that through the exception route. The deadline of § 17 (1) MiLoG (seven calendar days in the sectors of § 2a SchwarzArbG and for marginal employment, fined under § 21 MiLoG) remains an organisational duty of the operator; Hinata supports it with the self-hint and does not enforce it.

## Policy matrix

Every policy of the time tracking settings, with its default from the code. Use the table as an annex to the works or service agreement. Add a column with your value and the reason.

In every row the assessment under § 87 BetrVG is for the works parties. The column names what to look at. "No. 6" means § 87 (1) no. 6 BetrVG. In the public sector the state staff representation act (LPVG) applies, for federal bodies § 80 (1) no. 21 BPersVG.

| Policy | Effect | Who sees what | Co-determination | Default |
| --- | --- | --- | --- | --- |
| **Extended time tracking** (`advancedEnabled`) | The module: timers with start and end, calendar, approvals, availability, reports, billing. Only with it do start and end of someone's work become data. | Depends on the rows below. | Introducing a technical device that is objectively suited to monitoring (no. 6). Agree it before switching on. | off |
| **Absence management** (`absenceManagementEnabled`) | Absence types, entitlements, balances, requests, sick reports. Needs extended time tracking. | Each person their own. Absence keepers everybody's. | § 87 (1) no. 5 BetrVG (holiday principles, holiday schedule), in addition to no. 6. | off |
| **Who keeps absences** (`absenceManagers`) | Named people keep types, entitlements and balances and decide requests. | They see a sick day as sickness. Once someone is named, organization admins only see "away". | Who receives health data (Art. 9 GDPR) belongs in the agreement. | empty: organization admins keep absences |
| **Team absence calendar** (`absenceCalendarVisibility`) | Colleagues see each other's absences: `OFF`, only that someone is away (`BUSY_ONLY`), or the type (`TYPE`). Only with absence management. | Sickness only ever as away. Leads see capacity as a sum, for groups of three or more. | A holiday schedule (§ 87 (1) no. 5 BetrVG). | `OFF` |
| **Project, Issue, Description, Tag required** (`requiredFields`) | Project, issue, description or tag must be on an entry. | No change. | Content of the record (no. 6). Rules of conduct can touch no. 1. | all off |
| **Locked before** (`lockBefore`) with **Reopened spans** (`lockExceptions`) | Entries before the day are frozen for everyone, admins included. The date can never be in the future. A reopened span opens named days for everyone, with a reason. | Everyone sees the span and its reason. | Settle who reads requests and exceptions. | no lock date, no spans |
| **Record up to** (`maxDaysBack`) | Typo guard. An older day is refused and shows the way out: a request, then an organization admin opens the days for that person for two weeks. | Request and opening are in the audit log. | Part of the system (no. 6). | 365 days |
| **Hint for late entries after** (`lateEntryHintDays`) | Marks an entry recorded more than N days after its working day. Blocks nothing. | Only the person. In no report. | Part of the system (no. 6). | empty: no hint |
| **Rounding** (`rounding`) | Rounds reported durations to a step. Stored minutes never change. | No change. | Settle it where reports feed pay (no. 6). | no rounding, step 15 minutes |
| **Restrict tags** (`limitTagAccess`) | Only organization admins create new tags. | No change. | Part of the system (no. 6). | off |
| **Billable by default** (`defaultBillable`) | New entries start out billable. | No change. | Part of the system (no. 6). | off |
| **Calendar import** (`icsImportEnabled`) | People subscribe to their own calendar and turn appointments into entries. Needs `HINATA_ICS_SECRET`. | Subscriptions and events only for their owner. A taken over appointment becomes a normal entry. | Settle voluntariness and private appointments. | off |
| **Leads see members' entries** (`leadsSeeMemberEntries`) | Leads see the single entries, history and timesheet rows of their project members and may change those entries. | Off: leads see project totals only. On: they also see which days those members are away (vacation or other, sickness only as other, never a note), if the member booked time on one of their projects in the last twelve months. | Supervisors read individual bookings. The core question of any agreement (no. 6). | off |
| **Timesheet approvals** (`approvalsEnabled`) with **Approval period** (`approvalPeriod`) | People submit a period. A lead or organization admin approves or rejects it with a note. Needs the row above. | The approver reads the entries of the period. | Settle rhythm, approvers and rejections (no. 6). | off, monthly, week starts Monday |
| **Workload reports** (`workloadReportsEnabled`) | Booked time against capacity, per person. | Organization admins and project leads. A lead only for their own projects. | A direct comparison between people (no. 6). Settle purpose and limits. | off |
| **Report "absences and balances"** (`absenceReportsEnabled`) | Figures on absences and balances. Only with absence management. | Everyone their own. Keepers everybody's. Leads sums over three or more people, without sickness, and only if they see members' entries. | No. 5 and no. 6. | off |
| **Absence rate per person** (`absenceRateEnabled`) | The share of days away per person in that report. | Absence keepers only, never leads. | Conduct and health data: its own decision (no. 6). | off |
| **Budget alerts** (`alertsEnabled`) | Leads get a message at 80 % (unless the project sets another share) and at 100 % of budget or estimates. Assignees get one when their issue reaches its estimate. | The message names project or issue and sums, never a person. In small projects it can still point to someone. | Settle thresholds and recipients (no. 6). | off |
| **Target reminders** (`targetRemindersEnabled`) with **Suggested daily target** (`suggestedDailyTargetMinutes`) and **Suggested weekly target** (`suggestedWeeklyTargetMinutes`) | Reminds a person when their own time falls short of their own target. Organization admins can only suggest a target. | Only the person. Not audited. | Whether and which target is suggested belongs in the agreement. | off, no suggestion |
| **Working-time hints** (`arbzgHintsEnabled`) | Hints under §§ 3, 5 and 9 ArbZG on one's own entries. | Only the person. Not stored. | Health protection can touch no. 7. Part of the system (no. 6). | off |
| **Billing** (`billingEnabled`) with **Currency** (`currency`) | Rates, labour costs, reports, invoices. Needs extended time tracking. | Leads and organization admins. Labour cost rates can reveal pay. | Settle who sees cost rates (no. 6). | off, `EUR` |
| **Retention** (`retention`) | **Delete entries after** (`entryPurgeMonths`) for everyone. **Clear descriptions after** (`descriptionPurgeMonths`) for deleted accounts. | Decides how far back anything can be evaluated. | Periods belong in the agreement and the record of processing. | 0 and 0: nothing is deleted |
| **Absence retention** (`timeOffRetention`) | Coarsens sickness, deletes closed requests, optionally deletes the leave journal. | As in absence management. | Periods belong in the agreement. | 12 months, 36 months, journal kept |
| **Notices before leave lapses** (`expiryNotice`) | A yearly notice on a fixed day, and one some weeks before each deadline. Without a timely notice no leave lapses. | The person concerned. The sending is in the audit log. | Part of the holiday principles (no. 5). | 1 October, 6 weeks before |
| **Privacy notice** (`privacyNotice`) | The text shown before first use and under **Settings → Time tracking**. | Everyone. | Name the text in the agreement. | empty: built-in template |
| **Holidays of the platform** (`region`) | The region whose holidays the organization gets, filled every year. Set by administrators. | Everyone. Holidays are marked, never locked. | Distribution of working time can touch no. 2. | automatic, from the time zone |
| Audit events `TIME_ENTRY_CREATED`, `TIME_TIMER_STARTED`, `TIME_TIMER_STOPPED`, `TIME_TIMER_DISCARDED` and `MCP_TIMER_STARTED`, `MCP_TIMER_STOPPED`, `MCP_TIMER_DISCARDED` | A complete log of when each person created entries and started or stopped timers, that is when they worked. | The `TIME_` events: organization admins, in the organization's log. The `MCP_` events: administrators, under **Admin area → Audit log**. | Switch on only with an explicit rule (no. 6). | off |
| Timer outside the app: system notification at the end of an interval and the running timer on Android (since this release); menu bar and tray, Live Activity, widgets, controls, alarms (planned) | A function: the person's own timer on the person's own device. Device-local. Collects nothing and sends nothing to the employer. | The person, and whoever looks at their screen. | Part of the co-determined time-tracking system; describe it as a function in the works/service agreement; the assessment under § 87 (1) no. 6 BetrVG is for the works parties. | off until the person confirms it once |

!!! note "What the server records about timer actions"
    Where the timer audit events are switched on, the audit log stores IP address and user agent with each record, as with every audit record. A timer started from a system surface reaches the server like one started in the app. The server cannot tell them apart.

## Retention

Deletion runs at night, once even with several server instances. Every run is in the audit log (`TIME_RETENTION_RUN`, `TIME_OFF_RETENTION_RUN`).

| Data | Setting | Default | Rule |
| --- | --- | --- | --- |
| Time entries | **Delete entries after** (`entryPurgeMonths`) | 0, never | Otherwise at least 24 months. Never inside a submitted or approved period, never on an invoice. |
| Descriptions of deleted accounts | **Clear descriptions after** (`descriptionPurgeMonths`) | 0, never | The hours stay. |
| Sickness details | **Coarsen sickness after** (`sickDetailPurgeMonths`) | 12 months | A sick day then reads "away (other)", without its note. Day and balance stay. |
| Closed requests | **Delete closed requests after** (`requestPurgeMonths`) | 36 months | Refused, withdrawn and cancelled ones. Approved requests stay as evidence. |
| Leave journal | **Delete the leave journal after** (`ledgerPurgeYears`) | 0, kept | Otherwise at least 3 years (§§ 195, 199 BGB). |
| Notices before leave lapses | none | never deleted | The audit sweep keeps them too. A lapse rests on them. |
| Invoices and credit notes | none | never deleted | § 147 AO, § 257 HGB. |
| Audit log | server setting `audit.retentionDays` | 365 days | Except the notices before leave lapses. |
| Reminder marks | none | 90 days | They hold no content. |
| Calendar events | none | 30 days back to 90 days ahead | Replaced on every fetch. |

!!! warning "Nothing is deleted until you choose a period"
    Entry retention is `0` out of the box. § 16 (2) ArbZG and § 17 (1) MiLoG ask for two years, so 24 months is a common choice. After that, storage limitation applies (Art. 5 (1) (e) GDPR).

## Holidays

- Administrators choose the region under **Admin area → General → Holidays of the platform**. **Automatic, from the time zone** is the default. **None** creates no calendar.
- From the region the server makes a holiday calendar and fills this year and the next, every year, without an import (`HINATA_HOLIDAYS_AUTO_FILL=true`).
- Organization admins can rename the calendar, edit its days, give it another source or delete it. See [Holidays](/en/organization.html#holidays).
- A holiday is a mark. Everyone can still record time on it (principle 1).

## Your instance's privacy policy

- Your own privacy policy has to cover the time tracking module. Link it under **Admin area → Platform → App releases → Privacy policy URL** (`privacyPolicyUrl`, env `HINATA_PRIVACY_POLICY_URL`).
- Hinata ships a privacy notice for the module in nine languages. Organization admins replace it in the **Privacy notice** field (`privacyNotice`). Empty means the built-in text in the reader's language.
- You may use the built-in text as a template for your own policy. Check it against your setup: it describes the defaults, and the panel **Who sees my time data?** shows what is switched on.

## MCP

AI clients can run the person's own timer, list and change their own entries, sum their own time, read their own leave balance and ask for time off. They never read anybody else's time, and they never decide a request. The timer audit events over MCP (`MCP_TIMER_*`) are off by default, like those in the app. Details on the [MCP server](/en/mcp.html) page.

## Next steps

- Legal background and checklists: [Time tracking: privacy & law](/en/time-tracking-privacy.html).
- Roles and the Organization page: [Organization](/en/organization.html).
- Environment variables: [Configuration reference](/en/configuration.html).
