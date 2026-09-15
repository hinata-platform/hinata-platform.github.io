---
title: Time tracking: privacy & law
description: What time tracking stores, on which legal basis, and which policy enables which evaluation. With checklists for works agreements, DPIA and the record of processing.
---

# Time tracking: privacy & law

Working time is personal data. Whoever records it could also use it to watch people.

This page is for you as the operator of a Hinata instance, and for everyone preparing the rollout with you: works or staff council, data protection officer and HR. It explains what the module stores, which legal bases you can rely on, which setting allows which evaluation of people, and how the people concerned use their rights in the app.

The legal framework here is German and EU law, because that is where co-determination and working-time recording are most tightly regulated. Statute names stay in German so they match the sources.

!!! warning "Not legal advice"
    This page gives orientation and working material. It does not replace advice. More [at the end of the page](#not-legal-advice).

## Who is responsible

Hinata is self-hosted. The controller under Art. 4(7) GDPR for everything on an instance is its operator, usually the employer. The publisher of the app sees no time data (see the [privacy policy](/en/privacy-policy.html)).

The works agreement, the data protection impact assessment and the record of processing activities are therefore your documents. Hinata provides the settings and the functions for data subject rights. You decide which of them run.

Every policy that makes a statement about a person possible is off out of the box. After an upgrade, time tracking stays as it was until someone deliberately switches something on. You find the policies in the [Admin area](/en/admin-area.html) under **Time tracking**. If you leave one unset, the value from the server's environment applies.

## Purpose and data categories

The module records working time. It serves statutory recording duties and project steering. When switched on, it also serves timesheet approval and billing. For that it stores:

| Category | Content | Note |
| --- | --- | --- |
| Time entries | Day, duration, optional start and end time, project, issue, activity type, description, tags, billable yes/no, source (app, timer, smart commit, calendar), `createdAt`, `updatedAt`, `updatedBy` | The core. Without start and end an entry is just a duration on a day. |
| Running timer | Start time and the details for the later entry | At most one per person. It becomes an entry when stopped. |
| Submissions and approvals | Period, status (submitted, approved, rejected, withdrawn), who decided when, notes | Only with timesheet approvals switched on. |
| Correction requests and requests for older days | Affected entry or span, reason, answer with note, timestamps | Kept in their own collection. The audit log repeats them (`TIME_CORRECTION_REQUESTED`, `TIME_BACKFILL_REQUESTED`, `TIME_CORRECTION_ANSWERED`). |
| Days opened for a person | Span, who opened them, expiry, a message if there is one | Close again by themselves after two weeks and are recorded in the audit log (`TIME_BACKFILL_GRANTED`, `TIME_BACKFILL_REVOKED`). |
| Personal timer preferences | For example pomodoro lengths and breaks | Stored on the account, only relevant to the person. |
| Acknowledgement of the privacy notice | Timestamp (`timePrivacyAcknowledgedAt`) | Proof that the person was informed. Not consent. |
| Working hours | Planned minutes per weekday, the day they apply from, the chosen holiday calendar, who set them and when | Planning data. When an administrator changes them for someone else, the audit log records it (`AVAILABILITY_SCHEDULE_CHANGED`). |
| Absences | Type (vacation, sick, other), first and last day, half day, optional note | Planning data. An absence never stops anyone from recording time. When an administrator changes one for someone else, the audit log records it without the note (`AVAILABILITY_TIME_OFF_CHANGED`). |

!!! warning "A sick day is health data"
    The absence type *sick* says something about a person's health, which Art. 9 GDPR protects specially. Hinata stores no reason and no diagnosis, only the type and the days. Settle in the agreement whether sick days are entered here at all, or whether *other* is enough for planning.

!!! info "Why the acknowledgement is not consent"
    In an employment relationship consent is rarely free, because the employee depends on the employer. The duty to record working time does not depend on consent anyway. Acknowledging the notice only proves that the information under Art. 13 GDPR was given. Not acknowledging it costs nobody a right and grants none.

## Legal bases

### Data protection law

- **Art. 6(1)(b) GDPR:** performance of the employment contract, for instance when pay or overtime compensation depends on recorded time.
- **Art. 6(1)(c) GDPR:** compliance with a legal obligation, here the duty to record working time (see below).
- **Art. 6(1)(f) GDPR:** legitimate interests, for instance project steering or billing customers. This needs a documented balancing test. People can object under Art. 21 GDPR.
- **Art. 88 GDPR in conjunction with § 26 Abs. 4 BDSG:** works and service agreements and collective bargaining agreements can be more specific rules for employee data. That only holds if they meet Art. 88(2) GDPR, meaning they contain suitable and specific measures to protect employees.

!!! warning "§ 26 Abs. 1 S. 1 BDSG no longer carries the processing"
    On 30 March 2023 the CJEU ruled (C-34/21) that national employee data protection rules which do not meet Art. 88(2) GDPR must be disregarded, unless they are a legal basis under Art. 6(3) GDPR themselves. In its judgment of 8 May 2025 (8 AZR 209/21) the Federal Labour Court (BAG) concluded that § 26 Abs. 1 BDSG must remain unapplied. So base the processing on Art. 6(1) GDPR and, where one exists, on a collective agreement.

### Duty to record working time

- **CJEU, judgment of 14 May 2019, C-55/18 *CCOO*:** member states must require employers to set up an objective, reliable and accessible system that measures each worker's daily working time.
- **BAG, order of 13 September 2022, 1 ABR 22/21:** in Germany this duty already follows from § 3 Abs. 2 Nr. 1 ArbSchG, read in line with EU law. The start and end of daily working time, including overtime, must be recorded. The works council cannot force the employer to introduce an electronic system. It does have a say in how the system works.
- **§ 16 Abs. 2 ArbZG:** working time beyond eight hours on a working day must be recorded, and the records kept for at least two years. The provision sets no deadline for recording.
- **§ 17 Abs. 1 MiLoG:** for marginal employment (§ 8 Abs. 1 SGB IV) and in the sectors listed in § 2a SchwarzArbG (among them construction, hospitality, passenger transport, logistics, building cleaning, meat processing and security services), the start, end and duration of daily working time must be recorded. This has to happen by the end of the **seventh calendar day** after the working day. The records must be kept for at least two years. Breaches are fined under § 21 Abs. 1 Nr. 8 MiLoG.
- **Draft bill (Referentenentwurf) of the Federal Ministry of Labour (BMAS) amending the ArbZG, dated 18 June 2026:** among other things it foresees recording working time as a rule on the day the work is done. The draft has **not been adopted**. Until a law is passed, the rules above apply.

### Co-determination

- **§ 87 Abs. 1 Nr. 6 BetrVG:** the works council has a say when technical devices designed to monitor behaviour or performance are introduced and used. Under the BAG's settled case law it is enough that a device is objectively suitable for monitoring. Nobody has to intend to monitor.
- **Public sector:** here staff representation law applies. For federal authorities that is § 80 Abs. 1 Nr. 21 BPersVG, in the federal states the respective state staff representation act (LPVG).

### Data protection impact assessment

The [DPIA "must list" of the German Data Protection Conference (DSK)](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf) lists under no. 8 the extensive processing of data about employees' behaviour that can be used to assess their work in a way that has legal consequences for them or otherwise significantly affects them.

The more evaluations of people you switch on, the more likely you need a DPIA under Art. 35 GDPR. Check it with the [DPIA checklist](#dpia-checklist) and write down the result. Do that even if you conclude that no DPIA is needed.

## Policy matrix

The table shows, for each policy, which evaluation of people it makes possible. You can use it as an annex to the works agreement. Add the value you chose next to it, and why.

For every policy, the assessment under § 87 BetrVG is for the parties to the works agreement. The co-determination column names what to consider beyond that.

| Policy | Default | Which evaluation of people it enables | Co-determination |
| --- | --- | --- | --- |
| **Extended time tracking** (`advancedEnabled`) | off | The module itself: timers with start and end time, submissions, correction requests and every policy below. Only with it do the start and end of a person's work become data. | This is the introduction of a technical device that is objectively suitable for monitoring (§ 87 Abs. 1 Nr. 6 BetrVG, or staff representation law in the public sector). Agree it with the works or staff council before switching it on. |
| **Leads see members' entries** (`leadsSeeMemberEntries`) | off | Off: leads never see who booked what. On issues they see only day, duration and activity, like every other member, and they do not change other people's entries. Reports are per project. On: leads see members' entries, an entry's history, the entries behind a submission, and in the timesheet the rows of members of projects they lead. They may then change those entries too. They also see which days those members are away, if the member recorded time themselves on an issue of one of their projects in the last twelve months: vacation or other, never a note, a sick day only as other, never the planned hours, and nothing they could change. | Supervisors can then read individual bookings. That is the key question of any agreement. |
| **Timesheet approvals** (`approvalsEnabled`) with **Approval period** | off, monthly rhythm | People submit a period. A lead or admin approves or rejects it with a note. Approving means reading the person's entries, so it needs the policy above. The rhythm decides how closely things are checked. | Settle the rhythm, the approvers and how rejections are handled. |
| **Workload reports** (`workloadReportsEnabled`) | off | Booked time against capacity per person. That is a direct comparison between people. | Settle purpose, recipients and limits of use explicitly. |
| **Budget alerts** (`alertsEnabled`) | off | Leads get a message when a project passes a threshold of booked time. This is per project, but in small projects it can be traced to individuals. | Settle thresholds and recipients. |
| **Target reminders** (`targetRemindersEnabled`) | off | A person is reminded when their own booked time falls short of the target. The message goes only to them. | Nobody else gets a report. How the target is set still belongs in the agreement. |
| **Working-time hints** (`arbzgHintsEnabled`) | off | Hints under §§ 3, 5 and 9 ArbZG on a person's own entries, for that person only. Nothing is stored or passed on. See [Working-time self-hints](#working-time-self-hints-arbzg). | Only the general assessment (see above). |
| `lateEntryHintDays` | empty, so no hint | An entry shows "recorded N days after the working day". Only the person sees it, and it appears in no report. See [Late recording](#late-recording-what-is-possible-and-what-you-must-organise). | Only the general assessment (see above). |
| **Locked before** (`lockBefore`) and **Reopened spans** | no lock date | Entries before a cutoff day are frozen for everyone. A project can set its own, earlier lock date. An exception opens a named span for everyone, and its reason is in the audit log. On request the administrators can also open days for one person only, for two weeks. Requests and reasons can allow conclusions about individuals. | Settle who reads requests and exceptions and how long they are kept. |
| `maxDaysBack` | 365 days | Guards against typos. Older days are refused, and the message points to the administrators, who can open the days for that person. The request and the opening are recorded with their reasons. | Only the general assessment (see above). |
| **Retention** (`retention`) | 0 and 0, so no automatic deletion | Decides how far back anything can be evaluated at all. Hinata deletes entries never, or after 24 months at the earliest. | Retention periods belong in the agreement and the record of processing. |
| **Calendar import** (`icsImportEnabled`) | off | People subscribe to their own calendar and turn appointments into entries. Appointment titles and times become time data. | Settle voluntariness and how private appointments are handled. |
| **Billing** (`billingEnabled`) | off | Rates, labour costs, billing and profitability reports and invoices. Leads and admins see them. Labour cost rates can reveal individual pay. | Settle who sees cost rates. |
| Audit events `TIME_ENTRY_CREATED`, `TIME_TIMER_STARTED`, `TIME_TIMER_STOPPED`, `TIME_TIMER_DISCARDED` | off | A complete log of when each person created entries and started or stopped timers, which means the start and end of their work. Because such a log is objectively suitable for monitoring, these events are off by default. | Switch on only with an explicit rule. |

!!! note "What the audit log always records"
    Actions on someone else's data are always in the audit log: deleting another person's entry, an entry created for someone else (`TIME_ENTRY_CREATED_FOR`, for instance by smart commit), changes to the lock date, reopened spans, days opened for a person, correction requests and every run of automatic deletion. That protects the people concerned, because it records what happens to their data. When they work is not in it.

## Works agreement checklist

An agreement on time tracking with Hinata should settle at least these points:

- **Subject and scope:** which instance, which employees, which modules. Attach the chosen values. The simplest way is the [policy matrix](#policy-matrix) with an "our value" column.
- **Purposes:** list them exhaustively, for instance recording duties, project steering and billing. Regulate or exclude any other use explicitly, especially monitoring of behaviour or performance.
- **Data categories and required fields:** whether project, issue, description or tag are required. How detailed descriptions should be and what does not belong in them, such as health details like "doctor's appointment".
- **Visibility:** who sees whose entries (the person, leads only with `leadsSeeMemberEntries`, the administrators) and who gets admin rights. On issues, other members see only day, duration and activity.
- **Approvals:** whether timesheets are submitted, in which rhythm, who approves and what happens on rejection and reopening.
- **Evaluations and notifications:** workload reports, budget alerts and target reminders, each on or off, with recipients and thresholds.
- **Timers and audit events:** whether start and end times are recorded and whether the timer events may be switched on in the audit log (default: off).
- **Corrections and locks:** lock date, handling of correction requests, reopened spans and days opened for individuals, late recording (`maxDaysBack`, `lateEntryHintDays`).
- **Billing:** whether labour cost rates are stored and who sees them.
- **Calendar import:** voluntary, own calendar only, handling of private appointments.
- **Retention and deletion:** concrete values for `entryPurgeMonths` and `descriptionPurgeMonths`, and how approved periods are handled.
- **Exports and interfaces:** who pulls CSV or report exports and where they go. Access through the API has the same rights as the app. Name it anyway.
- **Transparency:** the text of the privacy notice (built-in template or your own) and training for leads and administrators.
- **Changes:** before a new Hinata version or policy switches on a new evaluation of people, the employee representatives are informed and involved again. Changes to the policies are recorded in the audit log.
- **Oversight:** the employee representatives can see settings and audit log, and the experience is reviewed after a fixed period.
- **Consequences of breaches:** for instance, data evaluated against the agreement may not be used.
- **Term, termination and continuing effect.**

## DPIA checklist

- **Write down the threshold assessment:** DSK must list no. 8 and the criteria from WP 248 rev. 01, among them systematic monitoring, vulnerable data subjects and evaluation or scoring. The more rows of the [policy matrix](#policy-matrix) are switched on, the more likely a DPIA is needed.
- **Systematic description** (Art. 35(7)(a) GDPR): data categories, data flows (app, server, mail, push, exports), switched-on policies with their values, and recipients.
- **Necessity and proportionality** (point b): for each switched-on policy, name the purpose and explain why a less intrusive means is not enough, for instance project totals instead of individual bookings. Data minimisation: keep required fields to a minimum and use start and end times only where needed.
- **Risks to the people concerned** (point c): monitoring of performance and behaviour, profiles from timer times, conclusions from descriptions and calendar appointments (health, private life), labour cost rates, exports outside the system, wrongly assigned roles, retention too long or too short.
- **Measures** (point d): defaults off, the "Who sees my time data?" panel, retention periods, lock date with recorded exceptions, the [security model](/en/security.html) (TLS, roles, rate limits), encrypted [backups](/en/backups.html) and training.
- **People involved:** ask the data protection officer for advice (Art. 35(2)), involve the employee representatives, and ask the people concerned where appropriate (Art. 35(9)).
- **Assess the residual risk:** if a high risk remains, you must consult the supervisory authority first (Art. 36 GDPR).
- **Review:** whenever a policy changes and with new Hinata versions that bring new evaluations (Art. 35(11)).

## Template: record of processing activities (Art. 30 GDPR)

The "Suggestion" column contains wording for a typical instance. You fill in the last column for your organisation.

| Field | Suggestion for Hinata | Your entry |
| --- | --- | --- |
| Controller (Art. 30(1)(a)) | Name and contact details of the operator, representative if any | … |
| Data protection officer | Contact details | … |
| Name of the processing | Working and project time recording with Hinata | … |
| Purposes (point b) | Meeting recording duties (§ 3 Abs. 2 Nr. 1 ArbSchG, § 16 Abs. 2 ArbZG, § 17 MiLoG where applicable); project steering; timesheet approval where applicable; billing customers where applicable | … |
| Legal bases | Art. 6(1)(b), (c) and (f) GDPR; works or service agreement under Art. 88 GDPR in conjunction with § 26 Abs. 4 BDSG where one exists | … |
| Categories of data subjects (point c) | Employees; apprentices, temporary agency workers, freelancers with an account where applicable | … |
| Categories of personal data (point c) | Account master data; time entries (day, duration, optional start and end, project, issue, activity type, description, tags, billable, source, change data); running timer; submissions and approvals with notes; correction requests, requests for older days and answers; days opened for the person; timer preferences; time the privacy notice was acknowledged | … |
| Recipients (point d) | The person; administrators; leads only with the policy switched on; other project members only day, duration and activity on issues; payroll or customers through exports where applicable; hosting and mail providers as processors | … |
| Transfers to third countries (point e) | None, if server, storage and mail relay run in the EU. Push notifications go through the [Hinata Connect gateway](/en/connect-gateway.html) and Firebase Cloud Messaging | … |
| Erasure periods (point f) | `entryPurgeMonths` (never, or 24 months after the entry's day at the earliest), `descriptionPurgeMonths` for deleted accounts; entries in submitted or approved periods handled separately | … |
| Technical and organisational measures (point g, Art. 32) | Reference to the [security model](/en/security.html): TLS, role-based rights, lock date, audit log, rate limits, backups; policy values as annexed | … |
| DPIA | carried out yes/no, date, result of the threshold assessment | … |
| Last review | Date and occasion (for example a new policy switched on) | … |

## Data subject rights in Hinata

### Information (Art. 12 to 14 GDPR)

The first time someone opens the module, the privacy notice appears once as a sheet. Acknowledging it closes the sheet and stores the time (`timePrivacyAcknowledgedAt`). That proves the information was given. It is not consent. After that the notice stays available under **Settings → Time tracking → Privacy**.

The **"Who sees my time data?"** panel is there too. Hinata computes it from the policies that are active right now. Nobody maintains it by hand. If you switch on `leadsSeeMemberEntries`, for example, the panel says at once that leads see the entries. So it can never be out of date. The panel also says what other members see on an issue: how much time was booked, but not who booked it and not the description.

The built-in template exists in nine languages. Under **Administration → Time tracking → Privacy and retention** you can replace it with your own text in the **Privacy notice** field, for instance with a reference to your works agreement. If the field stays empty, the template applies.

### Access and data portability (Art. 15 and 20 GDPR)

The account's data export also contains the time data: time entries, the running timer, submissions, correction requests and requests for older days with their answers, days opened for the person, timer preferences, the time the notice was acknowledged, and the person's working hours and absences.

It comes as JSON via `GET /api/v1/me/export` and as a PDF report whose link arrives by e-mail. Very long histories are shortened there, and a note in the export then points to the CSV export.

You get your own entries as CSV in the app under **Settings → Time tracking**, or directly through the API:

```bash
curl -H "Authorization: Bearer $HINATA_TOKEN" \
  -o my-time.csv \
  "https://api.track.example.com/api/v1/time/export.csv?from=2026-01-01&to=2026-06-30"
```

The file is UTF-8 with a BOM, so Excel shows umlauts correctly. Cells that start with a formula character are neutralised so no spreadsheet runs them. The export is streamed, covers up to 100,000 rows and is rate-limited per person. When many exports run at the same time, Hinata asks you to try again shortly. The export contains only the entries of the person who requests it.

### Rectification (Art. 16 GDPR)

You edit your own entries yourself. If a day lies before the lock date or inside a submitted period, it is frozen. Then **Request a correction** sends a reason to whoever can lift the freeze. For the lock date that is the administrators, for a submitted period the project leads or approvers. You can ask once a day per entry.

They answer with a note. The answer arrives as a notification, and you find it on the entry and in its history. The answer itself changes nothing yet. You can only change the entry once the day is actually open again. There are three ways to get there:

- For a submitted period, the project lead reopens the submission.
- For the lock date, the administrators open the day for you alone, straight from the request with **Open the days**. The opening lasts two weeks. You read their reason as the answer, and it is recorded in the audit log.
- If a span should be open for everyone again, the administrators add an exception to the lock date, with a reason in the audit log.

In an entry's history, a project lead reads only the requests about submissions in their projects, because only those are addressed to them. Requests about the lock date stay between you and the administrators.

### Erasure and storage limitation (Art. 17 and Art. 5(1)(e) GDPR)

When an account is deleted, Hinata removes the account, a running timer, submissions that are not yet approved, the person's requests, the days opened for them, and their working hours and absences. After that, their name no longer appears in the history of entries, and Hinata no longer shows the text of their correction requests there to anyone.

Approved submissions stay, because they are a business record. Time entries stay too, with the user id as a pseudonym, because the hours are part of the project's record.

!!! note "Pseudonymous is not anonymous"
    As long as a user id can be linked to a person, the entries remain personal data (Art. 4(5) GDPR). That is what the periods below are for.

You set retention under **Administration → Time tracking → Privacy and retention**:

- **Clear descriptions after** (`descriptionPurgeMonths`) empties the descriptions on deleted people's entries and the notes on their timesheets after N months. The hours and the decisions stay.
- **Delete entries after** (`entryPurgeMonths`) deletes entries older than N months, for everyone. Hinata never deletes entries inside a submitted or approved period. Allowed values are 0 for never or at least 24 months. A smaller value from the server's environment counts as 24.

Deletion runs at night in batches. Even with several server instances it runs only once. A run has a fixed time budget. If it does not finish within it, the next run continues where it stopped. Every run is recorded in the audit log with its counters (`TIME_RETENTION_RUN`), including one that stops with an error.

!!! warning "The default is 0: nothing is deleted automatically"
    Both periods are `0` out of the box. Hinata deletes nothing until you consciously choose a period. This is deliberate: a deletion cannot be undone, and the right period depends on your organisation.

Why 24 months is a good starting point: § 16 Abs. 2 ArbZG and § 17 Abs. 1 MiLoG both require records to be kept for at least two years. You may not delete sooner, which is why Hinata accepts no smaller value.

After that, storage limitation applies: data you no longer need for any purpose must be deleted. Check other retention duties separately, for instance for billed services.

!!! tip "A buffer for late records"
    Hinata counts the months from the entry's day. § 17 MiLoG counts the two years from the point that is relevant for the record. If people in your organisation often record late, plan a few months of buffer.

### No automated decisions (Art. 22 GDPR)

Budget alerts, target reminders, working-time hints and late-entry hints are only hints. Hinata does not lock anyone out, cut anything or rate anyone automatically. Whatever someone concludes from a hint is a human decision.

## Working-time self-hints (ArbZG)

With **Working-time hints** (`arbzgHintsEnabled`, default: off), Hinata shows a person on their own entries where they hit limits of the German Working Hours Act. Hinata only calculates this for the person themselves and for at most 31 days. There are four hints:

- The day total is over 10 hours, the daily maximum under [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html).
- There are fewer than 11 hours of rest between the end of one working day and the start of the next ([§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html)). This needs entries with start and end times.
- There are entries on a Sunday ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).
- There are entries on a public holiday of the calendar the person follows ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).

The hints are not stored, not passed to leads or administrators and not combined across people. They help the person themselves. They do not prove that your working hours comply with the ArbZG, and they are no verdict. The law has exceptions, for Sunday work for instance, that Hinata cannot know about.

## Late recording: what is possible and what you must organise

Hinata never refuses a late record just because it is late. § 16 Abs. 2 ArbZG sets no deadline, and the duty to record stays until the time is recorded. A late record is better than none. In C-55/18 the CJEU requires that daily working time can actually be measured.

With `lateEntryHintDays` you can switch on a hint (default: empty, so no hint). When a value is set, an entry recorded later shows "recorded N days after the working day". Only the person sees it, and it is in no report.

The threshold is configurable and not fixed at seven days. The seven-day rule in § 17 MiLoG only applies to certain sectors and marginal employment, and the draft bill of 18 June 2026 could make same-day recording the rule. Where the MiLoG applies, `7` is the obvious value.

`maxDaysBack` (default: 365) guards against typos, so that 2025 instead of 2026 does not slip through. The date picker does not offer older days, and Hinata refuses to save them. Both show the way out:

1. The person asks, with a reason, for the days to be opened. That works right at the message, in the date picker, or under **Settings → Time tracking → Ask for older days**. The request is recorded.
2. An administrator opens the days for that person under **Administration → Time tracking → Correction requests** with **Open the days**. The opening lasts two weeks and applies to that person only. The opening is recorded in the audit log, and if the administrator writes a message, the person reads it as the answer. An opening can be closed sooner under **Days opened for people**.
3. The person records the time.

!!! danger "Meeting the MiLoG deadline remains your duty"
    Hinata helps, but it enforces nothing. Where § 17 MiLoG applies, you have to make sure through your organisation that start, end and duration are recorded within seven calendar days. That takes clear responsibilities, reminders in the team and a rule for absences such as illness or holidays. The responsibility stays with the employer, even when employees record the time themselves.

## Not legal advice

This page is a careful orientation, but it is not legal advice. The law on working-time recording is changing right now. What applies to your organisation depends on sector, collective agreements, groups of employees and your own agreements.

Software on its own is never "legally compliant". Processing only becomes lawful through the decisions you make with it. The works or service agreement, the data protection impact assessment and the record of processing activities are the operator's tasks. Get expert advice for the rollout, for instance from your data protection officer and an employment lawyer.

## Sources

- [General Data Protection Regulation (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679), Art. 4, 5, 6, 12 to 22, 30, 35, 36 and 88
- [§ 26 BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__26.html)
- [CJEU, judgment of 30 March 2023, C-34/21](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62021CJ0034)
- [BAG, judgment of 8 May 2025, 8 AZR 209/21](https://www.bundesarbeitsgericht.de/entscheidung/8-azr-209-21/)
- [CJEU, judgment of 14 May 2019, C-55/18 *CCOO*](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62018CJ0055)
- [BAG, order of 13 September 2022, 1 ABR 22/21](https://www.bundesarbeitsgericht.de/entscheidung/1-abr-22-21/)
- [§ 3 ArbSchG](https://www.gesetze-im-internet.de/arbschg/__3.html)
- [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html), [§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html), [§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html), [§ 16 ArbZG](https://www.gesetze-im-internet.de/arbzg/__16.html)
- [§ 17 MiLoG](https://www.gesetze-im-internet.de/milog/__17.html), [§ 21 MiLoG](https://www.gesetze-im-internet.de/milog/__21.html)
- [§ 2a SchwarzArbG](https://www.gesetze-im-internet.de/schwarzarbg_2004/__2a.html), [§ 8 SGB IV](https://www.gesetze-im-internet.de/sgb_4/__8.html)
- [§ 87 BetrVG](https://www.gesetze-im-internet.de/betrvg/__87.html), [§ 80 BPersVG](https://www.gesetze-im-internet.de/bpersvg_2021/__80.html)
- [BMAS: Arbeitszeitgesetz](https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/arbeitszeitgesetz.html) (the draft bill of 18 June 2026 is not published there)
- [DSK: list of processing operations requiring a DPIA (version 1.1, German)](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf)

## Next steps

- How people record time is described in [Tracking your time](/en/guide-time.html).
- You set the policies in the [Admin area](/en/admin-area.html).
- The technical safeguards are described in the [security model](/en/security.html).
