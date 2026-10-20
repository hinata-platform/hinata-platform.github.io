---
title: Time tracking: privacy & law
description: What time tracking stores, on which legal basis, and which policy enables which evaluation. With checklists for works agreements, DPIA and the record of processing.
---

# Time tracking: privacy & law

Working time is personal data. Whoever records it could also use it to watch people.

This page is for you as the operator of a Hinata instance, and for everyone preparing the rollout with you: works or staff council, data protection officer and HR. It explains what the module stores, which legal bases you can rely on, which setting allows which evaluation of people, and how the people concerned use their rights in the app.

The legal framework here is German and EU law, because that is where co-determination and working-time recording are most tightly regulated. Statute names stay in German so they match the sources.

!!! warning "Not legal advice"
    This page gives orientation and working material. It does not replace advice. More [at the end of the page](#not-legal-advice). As of 11 October 2026.

## Who is responsible

Hinata is self-hosted. The controller under Art. 4(7) GDPR for everything on an instance is its operator, usually the employer. The publisher of the app sees no time data (see the [privacy policy](/en/privacy-policy.html)).

The works agreement, the data protection impact assessment and the record of processing activities are therefore your documents. Hinata provides the settings and the functions for data subject rights. You decide which of them run.

Every policy that makes a statement about a person possible is off out of the box. After an upgrade, time tracking stays as it was until someone deliberately switches something on. Organization admins set the policies on the [Organization](/en/organization.html) page under **Time tracking**. If one stays unset, the value from the server's environment applies. Every policy with its default is in [Time tracking administration](/en/admin-time-tracking.html#policy-matrix).

## Purpose and data categories

The module records working time. It serves statutory recording duties and project steering. When switched on, it also serves timesheet approval, absence planning and billing. For that it stores:

| Category | Content | Note |
| --- | --- | --- |
| Time entries | Day, duration, optional start and end time, project, issue, activity type, description, tags, billable yes/no, source (app, timer, smart commit, calendar), `createdAt`, `updatedAt`, `updatedBy` | The core. Without start and end an entry is just a duration on a day. |
| Running timer | Start time and the details for the later entry | At most one per person. It becomes an entry when stopped, and ends by itself after a full day. |
| Submissions and approvals | Period, status (submitted, approved, rejected, withdrawn), who decided when, notes | Only with timesheet approvals switched on. |
| Correction requests and requests for older days | Affected entry or span, reason, answer with note, timestamps | Kept in their own collection. The audit log repeats them (`TIME_CORRECTION_REQUESTED`, `TIME_BACKFILL_REQUESTED`, `TIME_CORRECTION_ANSWERED`). |
| Days opened for a person | Span, who opened them, expiry, a message if there is one | Close again by themselves after two weeks and are recorded in the audit log (`TIME_BACKFILL_GRANTED`, `TIME_BACKFILL_REVOKED`). |
| Shared entries | Who offered a copy of an entry to whom, a snapshot of day, duration, times and issue, status, the copy if accepted | The entry stays the sender's. Accepting files a copy in the recipient's own record. The audit log records offering, accepting and revoking (`TIME_ENTRY_SHARED`, `TIME_SHARE_ACCEPTED`, `TIME_SHARE_REVOKED`). |
| Personal timer preferences | For example pomodoro lengths and breaks | Stored on the account, only relevant to the person. |
| Acknowledgement of the privacy notice | Timestamp (`timePrivacyAcknowledgedAt`) | Proof that the person was informed. Not consent. |
| Working hours | Planned minutes per weekday, the day they apply from, the chosen holiday calendar, who set them and when | Planning data. When an organization admin changes them for someone else, the audit log records it (`AVAILABILITY_SCHEDULE_CHANGED`). |
| Absences | Type (vacation, sick, other), first and last day, half day, optional note | Planning data. An absence never stops anyone from recording time. When an organization admin changes one for someone else, the audit log records it without the note (`AVAILABILITY_TIME_OFF_CHANGED`). |
| Absence balances | Per type and year: entitlement, grants, bookings and corrections, each with the day it takes effect, the reason and who acted | Planning data. The journal is the source: no balance is stored, and every figure on every screen is computed from it. A correction's reason lives **only** on the journal line. |
| Employment dates used for the calculation | Joining and leaving date, optional note | There only to work out entitlements (§§ 4, 5 and 7 (4) BUrlG). Only absence keepers read and write them. Deleted with the account. |
| Absence requests | Type, span, the share the first and last day count for, the frozen number of days, status, optional note, the people who could decide it as worked out at submission, an optional stand-in, and the history of every step with its time and who acted | The request is the document and the absence is its result. A decision's reason lives **only** here, never in the audit log. The log records the type, the span and the amount (`TIME_OFF_REQUEST_SUBMITTED`, `_APPROVED`, `_REJECTED`, `_WITHDRAWN`, `_CANCELLED`). |
| Sick reports | Span, half day, type | A notification and not a request: no approver, no status, no required field and **no certificate**. The log records only that a report was made and for which span (`TIME_OFF_SICK_REPORTED`). |
| Notices before leave lapses | Who was told when, for which type and year, how many days remained and when they lapse | Evidence for a lapse. Never deleted (`TIME_OFF_EXPIRY_NOTICE_SENT`). |
| Calendar subscriptions | Name, colour, the calendar's address encrypted with AES-256-GCM and bound to the record, its host, status and last error, the takeover rule, timestamps | Only with the calendar import on. Only the owner sees them. The address is never shown again, not even to the owner, and never appears in a log, a response or an export. The audit log records adding and removing one with the host only (`TIME_CALENDAR_SUBSCRIPTION_CREATED`, `_DELETED`). |
| Calendar events | Per occurrence from 30 days back to 90 days ahead: start, end, time zone, title and location (each cut at 200 characters), all-day, free or busy, tentative or confirmed | A cache, replaced on every read, and shown **only** to the person who subscribed. They appear in no report, no inbox and nobody else's export. Only an event the person takes over becomes data others can see, as an ordinary entry with the source *calendar*. |
| Rates | Hourly rates and labour cost rates per team, project, person, person in a project or issue, each with the span it applies to and who wrote it | Only with billing on. Rates are never overwritten: a change is a new rate from a date on. A labour cost rate for a person can reveal pay. |
| Invoices and credit notes | Number, recipient, lines with description, minutes, rate and amount as issued, the entries a line was built from | A booking record. Never deleted (§ 147 AO, § 257 HGB). |
| Timer copies on the device | Timer state for system surfaces: start, mode and phase, no description by default | Stays on the device. See [Timer outside the app](#timer-outside-the-app). |

!!! danger "A reason stays with the thing it is about, not in the log"
    When somebody corrects a balance, Hinata asks for a reason. It writes that reason on the journal line, **not** into the audit log. The same holds for **rejecting a request**: the sentence sits on the request and goes when it does. That is deliberate: a reason can name an illness or a recognised disability (§ 208 SGB IX), which is data under Art. 9 GDPR. In the audit log it would outlive the deletion of the account, survive the module being switched off, and be readable by everyone who sees the log. The audit log records **that** somebody corrected or decided, for which type, which span and by how much.

!!! info "Who reads these log records"
    Records about working time, timesheets and absences are in the log on the [Organization](/en/organization.html) page. Administrators do not see them under **Admin area → Audit**. Records about absences, meaning requests, sick reports and balances, are only shown there to whoever keeps absences: the named absence keepers or, while nobody is named, the organization admins. Which of these events are recorded is up to the organization admins, not the administrators.

!!! info "Why the acknowledgement is not consent"
    In an employment relationship consent is rarely free, because the employee depends on the employer. The duty to record working time does not depend on consent anyway. Acknowledging the notice only proves that the information under Art. 13 GDPR was given. Not acknowledging it costs nobody a right and grants none.

## Recipients and periods

### Recipients

- The person themselves always sees their own data.
- Organization admins see hours, person and project key for everyone. Issue titles and descriptions only for projects they belong to.
- Leads see single entries only with `leadsSeeMemberEntries`. Otherwise they see totals.
- Other project members see on an issue only day, duration and activity.
- Absence keepers see absences and balances of everyone, sickness included.
- Customers receive invoices, if billing is on.
- Processors: hosting, mail relay, and for push notifications the [Hinata Connect gateway](/en/connect-gateway.html) with Firebase Cloud Messaging and Apple Push Notification service.

### Periods

- Time entries: never deleted until you set **Delete entries after**, then at least 24 months.
- Sickness details: coarsened after 12 months. Closed absence requests: deleted after 36 months. Leave journal: kept unless you set at least 3 years.
- Notices before leave lapses, invoices and credit notes: never deleted.
- Audit log: 365 days.

The full table is under [Retention](/en/admin-time-tracking.html#retention).

## Legal bases

### Data protection law

- **Art. 6(1)(b) GDPR:** performance of the employment contract, for instance when pay or overtime compensation depends on recorded time.
- **Art. 6(1)(c) GDPR:** compliance with a legal obligation, here the duty to record working time (see below).
- **Art. 6(1)(f) GDPR:** legitimate interests, for instance project steering or billing customers. This needs a documented balancing test. People can object under Art. 21 GDPR.
- **Art. 88 GDPR in conjunction with § 26 Abs. 4 BDSG:** works and service agreements and collective bargaining agreements can be more specific rules for employee data. That only holds if they meet Art. 88(2) GDPR, meaning they contain suitable and specific measures to protect employees.
- **Art. 9(2)(b) GDPR in conjunction with § 22 Abs. 1 Nr. 1 lit. b BDSG:** for sick days, which are health data. See [Health data](#health-data).

!!! warning "§ 26 Abs. 1 S. 1 BDSG no longer carries the processing"
    On 30 March 2023 the CJEU ruled (C-34/21) that national employee data protection rules which do not meet Art. 88(2) GDPR must be disregarded, unless they are a legal basis under Art. 6(3) GDPR themselves. In its judgment of 8 May 2025 (8 AZR 209/21) the Federal Labour Court (BAG) concluded that § 26 Abs. 1 BDSG must remain unapplied. So base the processing on Art. 6(1) GDPR and, where one exists, on a collective agreement.

### Duty to record working time

- **CJEU, judgment of 14 May 2019, C-55/18 *CCOO*:** member states must require employers to set up an objective, reliable and accessible system that measures each worker's daily working time.
- **BAG, order of 13 September 2022, 1 ABR 22/21:** in Germany this duty already follows from § 3 Abs. 2 Nr. 1 ArbSchG, read in line with EU law. The start and end of daily working time, including overtime, must be recorded. The works council cannot force the employer to introduce an electronic system. It does have a say in how the system works.
- **§ 16 Abs. 2 ArbZG:** working time beyond eight hours on a working day must be recorded, and the records kept for at least two years. The provision sets no deadline for recording.
- **§ 9 ArbZG:** prohibits work on Sundays and public holidays, with the exceptions of §§ 10 to 13 ArbZG. It prohibits the work, not its record. Hinata therefore never blocks an entry on a holiday.
- **§ 17 Abs. 1 MiLoG:** for marginal employment (§ 8 Abs. 1 SGB IV) and in the sectors listed in § 2a SchwarzArbG (among them construction, hospitality, passenger transport, logistics, building cleaning, meat processing and security services), the start, end and duration of daily working time must be recorded. This has to happen by the end of the **seventh calendar day** after the working day. The records must be kept for at least two years. Breaches are fined under § 21 Abs. 1 Nr. 8 MiLoG.

!!! note "Outlook: draft bill of 18 June 2026 (not passed)"
    A draft bill (Referentenentwurf) of the Federal Ministry of Labour (BMAS) amending the ArbZG, dated 18 June 2026, foresees among other things recording working time as a rule on the day the work is done. It has **not been passed**. This is the state at the time of writing. Until a law is passed, the rules above apply.

### Co-determination

In every case the assessment is for the works parties. These provisions can be relevant:

- **§ 87 Abs. 1 Nr. 6 BetrVG:** introducing and using technical devices designed to monitor behaviour or performance. Under the BAG's settled case law it is enough that a device is objectively suitable for monitoring. Nobody has to intend to monitor. This is the central provision for the whole module.
- **§ 87 Abs. 1 Nr. 1 BetrVG:** rules of conduct in the workplace, for instance required fields or how detailed descriptions must be.
- **§ 87 Abs. 1 Nr. 2 BetrVG:** start and end of daily working time and breaks, and their distribution over the week, for instance in working hours and holiday calendars.
- **§ 87 Abs. 1 Nr. 3 BetrVG:** temporary shortening or extension of working time, for instance where reports and targets point to overtime.
- **§ 87 Abs. 1 Nr. 5 BetrVG:** holiday principles, the holiday schedule and fixing an individual's holiday. See [Absences](#absences-the-law-of-their-own).
- **§ 87 Abs. 1 Nr. 7 BetrVG:** health protection, for instance the working-time hints on rest periods.
- **Public sector:** here staff representation law applies. For federal authorities that is § 80 Abs. 1 Nr. 21 BPersVG, in the federal states the respective state staff representation act (LPVG).

### Tax and commercial law

Issued invoices and credit notes are booking records. § 147 AO and § 257 HGB require them to be kept. Hinata never deletes them, and the entries an invoice names are excluded from deletion and from changes until a credit note releases them.

### Data protection impact assessment

The [DPIA "must list" of the German Data Protection Conference (DSK)](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf) lists under no. 8 the extensive processing of data about employees' behaviour that can be used to assess their work in a way that has legal consequences for them or otherwise significantly affects them.

The more evaluations of people you switch on, the more likely you need a DPIA under Art. 35 GDPR. Check it with the [DPIA checklist](#dpia-checklist) and write down the result. Do that even if you conclude that no DPIA is needed.

## Policy matrix

The full matrix, with effect, visibility, co-determination note and default of every policy, is in [Time tracking administration](/en/admin-time-tracking.html#policy-matrix). Use it as the annex to your agreement. These four principles apply to all of it:

1. **Hinata never prevents the recording of working time actually performed.** Holidays, weekends, company shutdowns and absences are marked, not locked. Basis: BAG 13.09.2022, 1 ABR 22/21 and CJEU 14.05.2019, C-55/18 (CCOO); § 16 (2) ArbZG requires recording working time beyond the working-day hours, which by the prevailing reading covers all work on Sundays and public holidays. § 9 ArbZG prohibits work on public holidays, not its documentation.
2. **Only the past is ever locked, never the present or the future.** The lock date is an integrity tool for closed periods (Art. 32 GDPR; retention under § 16 (2) ArbZG / § 17 MiLoG, two years), not a steering instrument.
3. **Every immutability has a documented way back.** Lock date, approval and invoice: by correction request, reopening or credit note, always with a reason in the audit log. Without a way back the lock collides with Art. 16 GDPR: working time is personal data, and inaccurate data must be rectified without undue delay.
4. **Late recording is never refused, at most made visible.** Catching up is possible up to the policy `maxDaysBack` (default 365 days), and beyond that through the exception route. The deadline of § 17 (1) MiLoG (seven calendar days in the sectors of § 2a SchwarzArbG and for marginal employment, fined under § 21 MiLoG) remains an organisational duty of the operator; Hinata supports it with the self-hint and does not enforce it.

!!! note "What the audit log records by default"
    Actions on someone else's data are in the audit log out of the box: deleting or changing another person's entry, an entry created for someone else (`TIME_ENTRY_CREATED_FOR`, for instance by smart commit), changes to the lock date, reopened spans, days opened for a person, correction requests, decisions on timesheets and absences and every run of automatic deletion. That protects the people concerned, because it records what happens to their data. When they work is not in it: the timer events and `TIME_ENTRY_CREATED` are off by default.

## What Hinata deliberately does not do

- No activity tracking: no screenshots, no keystrokes, no app or website logging.
- No idle detection. A running timer does not watch whether someone is at the keyboard.
- No rankings and no comparison scores between people.
- No team reminders. A reminder only ever goes to the person who set the target.
- No booking ban on holidays, weekends or outside working hours.
- No lock date in the future.
- No automatic submission of timesheets, no sanction, and no evaluation of who recorded late.
- The reason for every freeze is visible to the person: why the day is closed, who can open it and how to ask. Every refusal names the reason, the holder and the way back.

## Time reports, exports and shared links

The time reports under **Time tracking → Reports** open no new view of people. They read what the policies already allow.

- **Totals** per project, activity, tag, issue or period include one's own entries and every entry of the projects one can see. Every member already sees on the issue that time was booked on it. A total names nobody.
- **People** are named in a report only on one's own entries and, with `leadsSeeMemberEntries`, on the members of the projects one leads. The same rule applies to the list of entries and to every export.
- **Organization admins** see hours, person and project key for everyone. Issue titles, issue keys, descriptions and project names they only see for projects they are a member of, and for their own entries. The description search only searches entries they may read.
- All of this is written into the database query. Nothing is read first and filtered out afterwards.

Whoever **shares** a saved report passes on a link, not their view. Whoever opens the link has to be signed in and gets the report with what they may see themselves. Hinata keeps only a hash of the link, and the person who created it can revoke it at any time.

A **scheduled report by mail** goes to a list of up to 50 active accounts. Each person gets it with their own view, without an attachment and with a link into the app. Whoever schedules a report only gets it if they are on the list themselves. The log of the sending counts reports, not people.

Every **export** of a report is in the audit log (`TIME_REPORT_EXPORTED`) with format, number of rows and a fingerprint of the filters. Names and search terms are not in it. A **CSV import** writes only entries that pass the same checks as a typed entry, so never into a locked or submitted period. When an organization admin imports for another person, that is in the audit log (`TIME_ENTRIES_IMPORTED`).

## Works agreement checklist

An agreement on time tracking with Hinata should settle at least these points:

- **Subject and scope:** which instance, which employees, which modules. Attach the [policy matrix](/en/admin-time-tracking.html#policy-matrix) with an "our value" column.
- **Purposes:** list them exhaustively, for instance recording duties, project steering, absence planning and billing. Regulate or exclude any other use explicitly, especially monitoring of behaviour or performance.
- **Data categories and required fields:** whether project, issue, description or tag are required. How detailed descriptions should be and what does not belong in them, such as health details like "doctor's appointment".
- **Visibility:** who sees whose entries (the person, leads only with `leadsSeeMemberEntries`, organization admins) and who gets that role. On issues, other members see only day, duration and activity.
- **Approvals:** whether timesheets are submitted, in which rhythm, who approves and what happens on rejection and reopening.
- **Evaluations and notifications:** workload reports, absence reports, budget alerts and target reminders, each on or off, with recipients and thresholds. Also whether reports may be shared and sent regularly by mail, and to whom.
- **Timers and audit events:** whether start and end times are recorded and whether the timer events may be switched on in the audit log (default: off).
- **Timer outside the app:** which system surfaces are offered, described as functions (see [below](#timer-outside-the-app)).
- **Corrections and locks:** lock date, handling of correction requests, reopened spans and days opened for individuals, late recording (`maxDaysBack`, `lateEntryHintDays`).
- **Absences:** see the separate [absence checklist](#holiday-co-determination).
- **Billing:** whether labour cost rates are stored and who sees them.
- **Calendar import:** voluntary, own calendar only, handling of private appointments.
- **Retention and deletion:** concrete values for `entryPurgeMonths`, `descriptionPurgeMonths` and the absence periods, and how approved periods are handled.
- **Exports and interfaces:** who pulls CSV or report exports and where they go. Access through the API and MCP has the same rights as the app. Name it anyway.
- **Transparency:** the text of the privacy notice (built-in template or your own) and training for leads and organization admins.
- **Changes:** before a new Hinata version or policy switches on a new evaluation of people, the employee representatives are informed and involved again. Changes to the policies are recorded in the audit log.
- **Oversight:** the employee representatives can see settings and audit log, and the experience is reviewed after a fixed period.
- **Consequences of breaches:** for instance, data evaluated against the agreement may not be used.
- **Term, termination and continuing effect.**

## DPIA checklist

- **Write down the threshold assessment:** DSK must list no. 8 and the criteria from WP 248 rev. 01, among them systematic monitoring, vulnerable data subjects and evaluation or scoring. The more rows of the [policy matrix](/en/admin-time-tracking.html#policy-matrix) are switched on, the more likely a DPIA is needed.
- **Systematic description** (Art. 35(7)(a) GDPR): data categories, data flows (app, server, mail, push, exports, MCP), switched-on policies with their values, and recipients.
- **Necessity and proportionality** (point b): for each switched-on policy, name the purpose and explain why a less intrusive means is not enough, for instance project totals instead of individual bookings. Data minimisation: keep required fields to a minimum and use start and end times only where needed.
- **Risks to the people concerned** (point c): monitoring of performance and behaviour, profiles from timer times, conclusions from descriptions and calendar appointments (health, private life), sick days and absence rates, labour cost rates, exports outside the system, wrongly assigned roles, retention too long or too short.
- **Measures** (point d): defaults off, the "Who sees my time data?" panel, retention periods, lock date with recorded exceptions, the [security model](/en/security.html) (TLS, roles, rate limits), encrypted [backups](/en/backups.html) and training.
- **People involved:** ask the data protection officer for advice (Art. 35(2)), involve the employee representatives, and ask the people concerned where appropriate (Art. 35(9)).
- **Assess the residual risk:** if a high risk remains, you must consult the supervisory authority first (Art. 36 GDPR).
- **Review:** whenever a policy changes and with new Hinata versions that bring new evaluations (Art. 35(11)).

## Template: record of processing activities (Art. 30 GDPR)

The "Suggestion" column contains wording for a typical instance. You fill in the last column for your organization.

| Field | Suggestion for Hinata | Your entry |
| --- | --- | --- |
| Controller (Art. 30(1)(a)) | Name and contact details of the operator, representative if any | … |
| Data protection officer | Contact details | … |
| Name of the processing | Working and project time recording, absence planning and billing with Hinata | … |
| Purposes (point b) | Meeting recording duties (§ 3 Abs. 2 Nr. 1 ArbSchG, § 16 Abs. 2 ArbZG, § 17 MiLoG where applicable); project steering; timesheet approval where applicable; holiday and absence planning where applicable; billing customers where applicable | … |
| Legal bases | Art. 6(1)(b), (c) and (f) GDPR; for sick days Art. 9(2)(b) GDPR in conjunction with § 22 Abs. 1 Nr. 1 lit. b BDSG; works or service agreement under Art. 88 GDPR in conjunction with § 26 Abs. 4 BDSG where one exists | … |
| Categories of data subjects (point c) | Employees; apprentices, temporary agency workers, freelancers with an account where applicable | … |
| Categories of personal data (point c) | Account master data; time entries (day, duration, optional start and end, project, issue, activity type, description, tags, billable, source, change data); running timer; submissions and approvals with notes; correction requests, requests for older days and answers; days opened for the person; shared entries; timer preferences; time the privacy notice was acknowledged; working hours; absences, absence balances, absence requests, sick reports (type and days only), employment dates, notices before leave lapses; with the calendar import on, calendar subscriptions (address encrypted) and the events read from them; with billing on, rates and invoices | … |
| Storage (MongoDB collections) | `work_items`, `running_timers`, `timesheet_approvals`, `time_correction_requests`, `time_backfill_grants`, `time_entry_shares`, `time_tags`, `saved_reports`, `time_imports`, `time_marks`, `time_departed_users`, `time_retention_runs`, `project_time_settings`, `working_schedules`, `holiday_calendars`, `holidays`, `time_off`, `time_off_types`, `time_off_entitlements`, `time_off_ledger`, `time_off_employment`, `time_off_requests`, `time_off_notices`, `time_off_proposals`, `time_off_year_runs`, `time_off_retention_runs`, `calendar_subscriptions`, `calendar_events`, `billing_rates`, `invoices`, `invoice_sequences` | … |
| Recipients (point d) | The person; organization admins; absence keepers; leads only with the policy switched on; other project members only day, duration and activity on issues; customers through invoices; payroll through exports where applicable; hosting and mail providers as processors | … |
| Transfers to third countries (point e) | None, if server, storage and mail relay run in the EU. Push notifications go through the [Hinata Connect gateway](/en/connect-gateway.html), Firebase Cloud Messaging (Google) and Apple Push Notification service; assess them under the EU-US Data Privacy Framework or standard contractual clauses. With the calendar import on, the server fetches each subscribed calendar from the provider the person chose (for example Google, Microsoft or Apple) | … |
| Erasure periods (point f) | `entryPurgeMonths` (never, or 24 months after the entry's day at the earliest); `descriptionPurgeMonths` for deleted accounts; sickness details 12 months, closed requests 36 months, leave journal kept or at least 3 years; invoices and notices before leave lapses never; audit log 365 days | … |
| Technical and organizational measures (point g, Art. 32) | Reference to the [security model](/en/security.html): TLS, role-based rights, lock date, audit log, rate limits, backups; policy values as annexed | … |
| DPIA | carried out yes/no, date, result of the threshold assessment | … |
| Last review | Date and occasion (for example a new policy switched on) | … |

## Data subject rights in Hinata

### Information (Art. 12 to 14 GDPR)

The first time someone opens the module, the privacy notice appears once as a sheet. Acknowledging it closes the sheet and stores the time (`timePrivacyAcknowledgedAt`). That proves the information was given. It is not consent. After that the notice stays available under **Settings → Time tracking → Privacy**.

The **"Who sees my time data?"** panel is there too. Hinata computes it from the policies that are active right now. Nobody maintains it by hand. If you switch on `leadsSeeMemberEntries`, for example, the panel says at once that leads see the entries. So it can never be out of date. The panel also says what other members see on an issue: how much time was booked, but not who booked it and not the description.

The built-in template exists in nine languages. Under **Organization → Time tracking → Privacy and retention** you can replace it with your own text in the **Privacy notice** field, for instance with a reference to your works agreement. If the field stays empty, the template applies. Your instance's own privacy policy must cover the module as well, see [Your instance's privacy policy](/en/admin-time-tracking.html#your-instances-privacy-policy).

### Access and data portability (Art. 15 and 20 GDPR)

The account's data export also contains the time data: time entries, the running timer, submissions, correction requests and requests for older days with their answers, days opened for the person, shared entries, timer preferences, the time the notice was acknowledged, the person's working hours and absences, their absence balances with every journal line and its reason, their absence requests with every note and every decision's reason, and their calendar subscriptions with the events read from them. A subscription appears there with its host, never with its address, because the address is a key to someone else's service and an export is a file that travels. The reason a rejection gave belongs there in particular: it is deliberately in no log, so this export is where the person it is about receives it in full (Art. 15 GDPR).

It comes as JSON via `GET /api/v1/me/export` and as a PDF report whose link arrives by e-mail. Very long histories are shortened there, and a note in the export then points to the CSV export.

You get your own entries as CSV in the app under **Settings → Time tracking**, or directly through the API:

```bash
curl -H "Authorization: Bearer $HINATA_TOKEN" \
  -o my-time.csv \
  "https://api.track.example.com/api/v1/time/export.csv?from=2026-01-01&to=2026-06-30"
```

The file is UTF-8 with a BOM, so Excel shows umlauts correctly. Cells that start with a formula character are neutralised so no spreadsheet runs them. The export is streamed, covers up to 100,000 rows and is rate-limited per person. When many exports run at the same time, Hinata asks you to try again shortly. The export contains only the entries of the person who requests it.

### Rectification (Art. 16 GDPR)

You edit your own entries yourself. If a day lies before the lock date, inside a submitted period or on an invoice, it is frozen. The app says why, who can open it and how to ask. Then **Request a correction** sends a reason to whoever can lift the freeze. For the lock date that is the organization admins, for a submitted period the project leads or approvers. You can ask once a day per entry.

They answer with a note. The answer arrives as a notification, and you find it on the entry and in its history. The answer itself changes nothing yet. You can only change the entry once the day is actually open again. There are four ways to get there:

- For a submitted period, the project lead reopens the submission.
- For the lock date, an organization admin opens the day for you alone, straight from the request with **Open the days**. The opening lasts two weeks. You read their reason as the answer, and it is recorded in the audit log.
- If a span should be open for everyone again, an organization admin adds an exception to the lock date, with a reason in the audit log.
- For an invoiced entry, a credit note on the invoice releases it.

In an entry's history, a project lead reads only the requests about submissions in their projects, because only those are addressed to them. Requests about the lock date stay between you and the organization admins.

### Erasure and storage limitation (Art. 17 and Art. 5(1)(e) GDPR)

When an account is deleted, Hinata removes the account, a running timer, submissions that are not yet approved, the person's requests, the days opened for them, their working hours, absences and employment dates, and the absence requests nobody ever decided. Decided ones stay, pseudonymised, like approved submissions and bookings: they are the record of who was granted what. After that, their name no longer appears in the history of entries, and Hinata no longer shows the text of their correction requests there to anyone.

Calendar subscriptions and their events go too. Entries a person took over from a calendar stay like every other entry. Deleting a single subscription removes its events at once, and pasting a new address removes the events of the old one. Switching the calendar import off stops all fetching and hides the events, but deletes nothing.

Approved submissions stay, because they are a business record. Time entries stay too, with the user id as a pseudonym, because the hours are part of the project's record.

!!! note "Pseudonymous is not anonymous"
    As long as a user id can be linked to a person, the entries remain personal data (Art. 4(5) GDPR). That is what the periods below are for.

You set retention under **Organization → Time tracking → Privacy and retention**:

- **Clear descriptions after** (`descriptionPurgeMonths`) empties the descriptions on deleted people's entries and the notes on their timesheets after N months. The hours and the decisions stay.
- **Delete entries after** (`entryPurgeMonths`) deletes entries older than N months, for everyone. Hinata never deletes entries inside a submitted or approved period, nor entries on an invoice. Allowed values are 0 for never or at least 24 months. A smaller value from the server's environment counts as 24.
- The absence periods (**Coarsen sickness after**, **Delete closed requests after**, **Delete the leave journal after**) are listed under [Retention](/en/admin-time-tracking.html#retention).

Deletion runs at night in batches. Even with several server instances it runs only once. A run has a fixed time budget. If it does not finish within it, the next run continues where it stopped. Every run is recorded in the audit log with its counters (`TIME_RETENTION_RUN`, `TIME_OFF_RETENTION_RUN`), including one that stops with an error.

!!! warning "The default is 0: nothing is deleted automatically"
    Both entry periods are `0` out of the box. Hinata deletes no entry until you consciously choose a period. This is deliberate: a deletion cannot be undone, and the right period depends on your organization.

Why 24 months is a good starting point: § 16 Abs. 2 ArbZG and § 17 Abs. 1 MiLoG both require records to be kept for at least two years. You may not delete sooner, which is why Hinata accepts no smaller value.

After that, storage limitation applies: data you no longer need for any purpose must be deleted. Invoices follow their own periods (§ 147 AO, § 257 HGB).

!!! tip "A buffer for late records"
    Hinata counts the months from the entry's day. § 17 MiLoG counts the two years from the point that is relevant for the record. If people in your organization often record late, plan a few months of buffer.

### Objection (Art. 21 GDPR)

An objection is possible where the processing rests on legitimate interests (Art. 6(1)(f) GDPR), for instance project steering or billing. Hinata has no objection button. The operator assesses the objection and, if it succeeds, switches the evaluation off or limits it, for instance by turning off workload reports. Recording working time to meet a legal duty (Art. 6(1)(c) GDPR) is not open to objection.

### No automated decisions (Art. 22 GDPR)

Budget alerts, budget notes while recording, target reminders, working-time hints and late-entry hints are only hints. A budget's usage is always the sum of the whole project and never names a person. Hinata does not lock anyone out, cut anything or rate anyone automatically. Leave after a long illness never lapses automatically either: Hinata only proposes it, and a person decides. Whatever someone concludes from a hint is a human decision.

## Working-time self-hints (ArbZG)

With **Working-time hints** (`arbzgHintsEnabled`, default: off), Hinata shows a person on their own entries where they hit limits of the German Working Hours Act. Hinata only calculates this for the person themselves and for at most 31 days. There are four hints:

- The day total is over 10 hours, the daily maximum under [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html).
- There are fewer than 11 hours of rest between the end of one working day and the start of the next ([§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html)). This needs entries with start and end times.
- There are entries on a Sunday ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).
- There are entries on a public holiday of the calendar the person follows ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).

The hints are not stored, not passed to leads or organization admins and not combined across people. They help the person themselves. They do not prove that your working hours comply with the ArbZG, and they are no verdict. The law has exceptions, for Sunday work for instance, that Hinata cannot know about.

## Late recording: what is possible and what you must organize

Hinata never refuses a late record just because it is late. § 16 Abs. 2 ArbZG sets no deadline, and the duty to record stays until the time is recorded. A late record is better than none. In C-55/18 the CJEU requires that daily working time can actually be measured.

Recording a whole month at the end of the month is possible and allowed. So is catching up over several months. Where a sector deadline applies, the operator makes sure of it through the organization. The software at most makes lateness visible, and only to the person concerned.

With `lateEntryHintDays` you can switch on a hint (default: empty, so no hint). When a value is set, an entry recorded later shows "recorded N days after the working day". Only the person sees it, and it is in no report.

The threshold is configurable and not fixed at seven days. The seven-day rule in § 17 MiLoG only applies to certain sectors and marginal employment, and the draft bill of 18 June 2026 could make same-day recording the rule. Where the MiLoG applies, `7` is the obvious value.

`maxDaysBack` (default: 365) guards against typos, so that 2025 instead of 2026 does not slip through. The date picker does not offer older days, and Hinata refuses to save them. Both show the way out:

1. The person asks, with a reason, for the days to be opened. That works right at the message, in the date picker, or under **Settings → Time tracking → Ask for older days**. The request is recorded.
2. An organization admin opens the days for that person under **Organization → Time tracking → Correction requests** with **Open the days**. The opening lasts two weeks and applies to that person only. The opening is recorded in the audit log, and if the organization admin writes a message, the person reads it as the answer. An opening can be closed sooner under **Days opened for people**.
3. The person records the time.

!!! danger "Meeting the MiLoG deadline remains your duty"
    Hinata helps, but it enforces nothing. Where § 17 MiLoG applies, you have to make sure through your organization that start, end and duration are recorded within seven calendar days. That takes clear responsibilities, reminders in the team and a rule for absences such as illness or holidays. The responsibility stays with the employer, even when employees record the time themselves.

## Absences: the law of their own

### Holiday co-determination

Absence management and the team absence calendar fall under **§ 87 Abs. 1 Nr. 5 BetrVG**: general holiday principles, the holiday schedule and, in a dispute, the timing of an individual's holiday. That applies in addition to no. 6. Settle at least:

- whether absence management and the team calendar are switched on, and at which level (`absenceCalendarVisibility`);
- the absence types, which need approval, and who decides;
- who keeps absences (`absenceManagers`) and so sees sick days;
- whether sick days are entered here at all, or whether *other* is enough for planning;
- carry-over, lapse and the notices before leave lapses (`expiryNotice`);
- whether the absence report and the absence rate per person are used (`absenceReportsEnabled`, `absenceRateEnabled`);
- the absence periods (`timeOffRetention`).

### Notice duty, lapse and limitation

- **Leave only lapses after a timely notice.** BAG, judgment of 19 February 2019, 9 AZR 541/15, following CJEU 6 November 2018, C-684/16 *Max-Planck* and C-619/16 *Kreuziger*. Hinata sends that notice once a year on a fixed day (default 1 October) and some weeks before each deadline (default 6). The notices are never deleted.
- **Limitation starts only with the notice.** BAG, judgment of 20 December 2022, 9 AZR 266/20. That is why the leave journal is kept, or at least three years (§§ 195, 199 BGB).
- **Long-term sickness: lapse after 15 months.** Leave that could not be taken because of illness lapses fifteen months after the end of its leave year (CJEU 22 November 2011, C-214/10 *KHS*; BAG, judgment of 20 December 2022, 9 AZR 245/19). Whether someone really could not work all that time is a finding about a person. Hinata only proposes the lapse. An absence keeper confirms or dismisses it, with a reason.

### Health data

A sick day says something about a person's health, which Art. 9 GDPR protects specially. The legal basis is Art. 9(2)(b) GDPR in conjunction with § 22 Abs. 1 Nr. 1 lit. b BDSG.

- Hinata stores no reason and no diagnosis, only the type and the days.
- There is nowhere to upload a certificate. Since 2023 an employer retrieves the electronic certificate of incapacity (eAU) from the health insurer under § 109 SGB IV.
- No notification about an absence names its type: not in the bell, not in the mail, not on a lock screen.
- If you name absence keepers, only they see sickness as sickness. Organization admins then only see that someone is away. If nobody is named, organization admins keep absences and see them in full.
- After 12 months a sick day is coarsened to "away (other)" by default.

!!! warning "Only sickness is hidden, not every sensitive type"
    A sick report reaches whoever decides as *other*. No other type works that way: somebody deciding a request reads the name of the type, so a type you add yourself (*parental leave*, *rehabilitation*, time off under § 208 SGB IX) says something about the person. Two roads are open: give the type no approval, and nobody decides it, or give it a name that says nothing. Settle that before you extend the catalogue.

!!! info "Who learns that leave got shorter"
    When sickness falls on approved leave, Hinata books the overlapping days back and shortens the leave (§ 9 BUrlG). The people who decided it learn **that** the leave got shorter, never why. The reason would otherwise be a health fact finding its way to a manager through a planning notice.

### What Hinata does not do with absences

- No payroll. Hinata computes days, never holiday pay or any other amount.
- No sickness rate per person, unless you switch on its own policy (`absenceRateEnabled`), and then only for absence keepers.
- No automatic lapse after illness.
- No certificate, no reason, no diagnosis.

## Shift planning

When the [shift planning](/en/shifts.html) module is on, Hinata records who is signed up for which shift and when. That is a history of who worked or helped when, so it is personal data.

- **Co-determination.** In companies shift plans touch § 87(1) no. 2 and 3 BetrVG, and evaluations of staffing no. 6. Public bodies fall under the federal or state staff representation law, associations under neither. Cover the module in your works or service agreement before you switch it on.
- **Retention.** Assignments are deleted twelve months after their shift ended, every night at 03:55. Set the period with `HINATA_SHIFTS_RETENTION_MONTHS`. The counts of a past shift stay; the names behind them do not.
- **Names for members only.** Only members of the project see who is on a shift. Lists carry figures, not names; names appear only in the detail of a shift or an event. There are no rankings and no evaluations per person.
- **Absences only for those who see them.** If absence management is on as well, Hinata points out an entered absence when someone signs up, but only to people who can see that absence anyway. Planners learn nothing about other people's absences this way.
- **Offline copy.** For "My shifts" the app keeps a small copy of the person's own shifts on the device, without anyone else's names. It is deleted on sign-out and when the module is switched off.
- **Access.** The access report under Art. 15 GDPR includes the person's own assignments and planner rights.
- **Calendar subscription.** Whoever subscribes to their shifts in their own calendar hands them to the calendar provider they choose; with Google and Microsoft, their servers store them. The address is shown only once and stored as a hash, never in plain text. See [Shifts in your own calendar](/en/shifts.html#shifts-in-your-own-calendar).

## Timer outside the app

Since this release the timer can reach the person outside the app window:

- **End of an interval:** a system notification when a countdown or a Pomodoro interval ends. On Android, iOS, macOS and Windows it is planned ahead, so it also arrives with the app closed. On Linux and in the browser it comes while the app runs in the background.
- **Running timer:** on Android a quiet ongoing notification whose clock the system runs (on Android 16 and later as a Live Update with a status bar chip that shows only the time, optionally held by a foreground service in the reliability mode, which collects nothing), the home screen widget and a Quick Settings tile. On iPhone and iPad a Live Activity (lock screen, Dynamic Island, StandBy) and the timer widget on the home and lock screen. In an installed web app a badge on the app icon.
- **Tab title:** in the browser, if the person wants it, the running time in the tab title. Only the time.
- **Desktop:** the running timer in the menu bar on a Mac and in the notification area on Windows and Linux. Work and breaks look the same there. On a Mac also the timer widget on the desktop and in Notification Center, with the same record as on the iPhone, in an extension in the App Sandbox without network access.

Controls, alarms and app shortcuts follow in later releases.

- **Device-local.** The surfaces collect nothing and send nothing to the employer (one exception, with a switch of its own: the Live Activity in the background, see below). There is no telemetry, and surface events are not audited. Stopping the timer from a notification calls the same route as the button in the app, and the server cannot tell them apart.
- **Generic texts.** A notification says that an interval is over, never what it was for. It disappears by itself where the system allows that (Android after ten minutes, Linux after a timeout, the browser on its own). On iOS and macOS the system keeps it in the notification centre until the person clears it.
- **No description by default.** A locked Android screen shows only the app name. Details on the unlocked screen and on the lock screen are two separate switches, both off.
- **They expire.** Local copies end by themselves at the latest 24 hours after the start, and vanish on sign out and with the account. The widgets keep one record without any id: start, end, whether it is a break, and when the copy expires. They go back to idle at that moment without the app and without the network, at the latest an hour after the end of a countdown or a Pomodoro phase. A Live Activity is started, changed and ended only by the running app. iOS ends it after eight hours at the latest, and the app ends an expired one the next time it starts.
- **One by one.** Everything is off until the person confirms the card **Timer outside the app** once. After that each surface can be switched off on its own under **Settings → Time tracking**. The panel **Who sees my time data?** lists what is active on this device, and **Delete now** removes the local copies at once.

Recommendation: list the surfaces in the works agreement checklist, as functions of the co-determined system.

**Devices owned or managed by the employer.** On a managed device, device management can see installed apps and in some setups their stored data. Settle in the agreement that device management is not used to read time data. With the defaults the local copies hold no description.

**Updating the Live Activity in the background.** With the switch **Update in the background** (iPhone and iPad only, off by default, per device) the Live Activity follows the timer while the app is closed: a phase change or a stop on another device reaches the lock screen. This is the one case in which the state of the timer leaves the server, so:

- **End-to-end encrypted.** For every activity the iPhone makes its own 256-bit key and registers it, with the activity's push token, at the server over TLS. The server encrypts every state with AES-256-GCM. The plaintext holds only the mode, the phase, the finished intervals, the start, the end of the stretch and whether it ended, never a description, project, issue or tag. Only the widget on the iPhone decrypts it. The [Hinata Connect gateway](/en/connect-gateway.html), Google Firebase Cloud Messaging and Apple Push Notification service see ciphertext, the token and when it was sent. Those times stay metadata with the processors.
- **Short-lived.** Token and key live as long as the activity: the server deletes them at its end, when the push service reports the token as invalid, when the switch goes off, and at the latest four hours after the longest possible end. The server keeps the key encrypted (with `HINATA_ICS_SECRET`); without that secret it accepts no registration.
- **No monitoring.** No delivery log, no statistics, no field on the user, no audit entry. The gateway logs no content.
- **Deleted with the account.** Deleting an account removes every device token of the person, including the ones for ordinary push notifications.

Add the feature to your record of processing. Sub-processors are the Hinata Connect gateway, Google Firebase Cloud Messaging and Apple Push Notification service. Assess the third-country transfer under the EU-US Data Privacy Framework or standard contractual clauses.

**Actions without opening the app.** **Stop** and **Take a break** or **Resume** in the notification, the buttons on the timer widget (on iPhone and iPad also **Start**), the buttons of the Live Activity and, on Android, the Quick Settings tile work without the app opening. They call the same routes as the buttons in the app. On a locked device iOS asks for Face ID or the passcode first; Android does nothing and asks the person to unlock and try again. If the sign-in has expired, the app renews it in the background just as it does when it opens. If the server refuses, nothing happens, and the app catches up the next time it opens.

**Alarms (iPhone and iPad with iOS 26 and later).** An alarm breaks through silent mode and Focus. That is why the switch **Ring as an alarm** is off by default, not part of the setup, and stands on its own in the settings with that said; iOS asks as well. The system keeps the alarm outside the app for as long as it exists. It gets only what a lock screen would show anyway: the title at the end of the interval, the same one for every countdown (“Interval”) while it counts down, the button words, the times and one word for the widget (countdown, work or break). Never a description, project, issue, tag or an ID of the timer. Nothing goes to the server for it, and Hinata collects nothing. Passing the alarm on to a paired Apple Watch is the system's own behaviour. Signing out and **Delete now** remove every alarm; restarting the app removes none. Since only the person switches the alarm on, the time tracking settings stay their own; an alarm set by someone else would need a fresh co-determination assessment (§ 87(1) nos. 2 and 6 BetrVG).

**Siri, Shortcuts and controls.** Everything happens on the device. Siri, the Shortcuts app, search, Control Center and the Action button only hand the action to the app, which calls the same routes as the buttons in the app; the server cannot tell them apart. For the project parameter the app keeps a list of your visible projects in the storage only the app and its widget share: the ID and the name of each, at most 200, removed when you sign out and with **Delete now**. **Timer status** reads the widgets' record and says the time and the phase, never the description. Actions from a locked device need Face ID or the passcode. Hinata collects nothing here and has no telemetry. The phrases Siri listens for are fixed in the app and processed by Apple when it is installed; what you say to Siri, Apple processes under its own Siri terms, and Hinata only receives the action.

**Alarms (planned).** Alarms through Apple's AlarmKit (iOS and iPadOS 26) break through silent mode. That is why they are an explicit opt-in for each person.

**App shortcuts (planned).** Apple evaluates the spoken phrases of app shortcuts on its side, without telling Hinata who said what. Hinata only receives the resulting action.

## Not legal advice

This page is a careful orientation, but it is not legal advice. The law on working-time recording is changing right now. What applies to your organization depends on sector, collective agreements, groups of employees and your own agreements.

Software on its own is never "legally compliant". Processing only becomes lawful through the decisions you make with it. The works or service agreement, the data protection impact assessment and the record of processing activities are the operator's tasks. Get expert advice for the rollout, for instance from your data protection officer and an employment lawyer.

As of 11 October 2026.

## Sources

- [General Data Protection Regulation (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679), Art. 4, 5, 6, 9, 12 to 22, 30, 32, 35, 36 and 88
- [§ 22 BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__22.html), [§ 26 BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__26.html)
- [CJEU, judgment of 30 March 2023, C-34/21](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62021CJ0034)
- [BAG, judgment of 8 May 2025, 8 AZR 209/21](https://www.bundesarbeitsgericht.de/entscheidung/8-azr-209-21/)
- [CJEU, judgment of 14 May 2019, C-55/18 *CCOO*](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62018CJ0055)
- [BAG, order of 13 September 2022, 1 ABR 22/21](https://www.bundesarbeitsgericht.de/entscheidung/1-abr-22-21/)
- [CJEU, judgments of 6 November 2018, C-684/16 *Max-Planck*](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62016CJ0684) and [C-619/16 *Kreuziger*](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62016CJ0619)
- [BAG, judgment of 19 February 2019, 9 AZR 541/15](https://www.bundesarbeitsgericht.de/entscheidung/9-azr-541-15/)
- [CJEU, judgment of 22 November 2011, C-214/10 *KHS*](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62010CJ0214)
- [BAG, judgment of 20 December 2022, 9 AZR 266/20](https://www.bundesarbeitsgericht.de/entscheidung/9-azr-266-20/) and [9 AZR 245/19](https://www.bundesarbeitsgericht.de/entscheidung/9-azr-245-19/)
- [§ 3 ArbSchG](https://www.gesetze-im-internet.de/arbschg/__3.html)
- [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html), [§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html), [§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html), [§ 16 ArbZG](https://www.gesetze-im-internet.de/arbzg/__16.html)
- [§ 17 MiLoG](https://www.gesetze-im-internet.de/milog/__17.html), [§ 21 MiLoG](https://www.gesetze-im-internet.de/milog/__21.html)
- [§ 2a SchwarzArbG](https://www.gesetze-im-internet.de/schwarzarbg_2004/__2a.html), [§ 8 SGB IV](https://www.gesetze-im-internet.de/sgb_4/__8.html), [§ 109 SGB IV](https://www.gesetze-im-internet.de/sgb_4/__109.html)
- [BUrlG](https://www.gesetze-im-internet.de/burlg/), [§ 195 BGB](https://www.gesetze-im-internet.de/bgb/__195.html), [§ 199 BGB](https://www.gesetze-im-internet.de/bgb/__199.html)
- [§ 147 AO](https://www.gesetze-im-internet.de/ao_1977/__147.html), [§ 257 HGB](https://www.gesetze-im-internet.de/hgb/__257.html)
- [§ 87 BetrVG](https://www.gesetze-im-internet.de/betrvg/__87.html), [§ 80 BPersVG](https://www.gesetze-im-internet.de/bpersvg_2021/__80.html)
- [BMAS: Arbeitszeitgesetz](https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/arbeitszeitgesetz.html) (the draft bill of 18 June 2026 is not published there)
- [DSK: list of processing operations requiring a DPIA (version 1.1, German)](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf)

## Next steps

- How people record time is described in [Tracking your time](/en/guide-time.html).
- Every policy with its default: [Time tracking administration](/en/admin-time-tracking.html).
- The technical safeguards are described in the [security model](/en/security.html).
