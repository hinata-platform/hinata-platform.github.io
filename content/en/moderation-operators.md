---
title: Moderation for operators
description: For administrators and operators. What the Digital Services Act asks of a Hinata server, what Hinata does for each duty, the yearly figures, privacy notices, codetermination, retention and reporting to the police.
---

# Moderation for operators

Whoever runs a Hinata server offers a hosting service under the Digital Services Act (DSA), and in some cases an online platform. This page says which duties follow, what Hinata does for each of them and what is left to you. It is no legal advice. Where your case is unclear, ask whoever advises your organization.

How moderators work day to day is on [Moderation](/en/moderation.html). The settings are under [Admin area › Moderation](/en/admin-area.html#moderation).

## Hosting service or online platform

A Hinata server stores what its members write and upload, at their request. That makes it a **hosting service** (Art. 3(g)(iii) DSA).

It becomes an **online platform** when it also disseminates that content to the public (Art. 3(i) and (k)). Where people need an account to read, content only counts as public when anybody who asks gets in automatically, without a person deciding who is admitted (recital 14). In Hinata that happens in two ways:

- self-registration without approval,
- an SSO provider that creates active accounts at the first sign-in, without approval and without a list of allowed email domains.

An online platform has further duties (Art. 20 to 28), among them a complaint system, out-of-court dispute settlement and its own transparency figures.

**What the update changed:** when Hinata is updated to a version with moderation, and on every new instance, it closes each of these ways in by switching approval on, and tells every administrator. Opening one again takes an explicit confirmation on save. While one is open, **Admin area › Moderation** starts with **Who comes in** and says what it means.

## Instances inside a company or club

An instance only for your own staff or members, where an administrator decides who comes in, is a closed group. Its content is not public, so it is no online platform. Whether the DSA applies to a tool that only serves your own people at all is not settled. Hinata gives you what a hosting service needs either way, so you do not have to answer that question first.

## Public bodies

Micro and small enterprises are exempt from the yearly figures (Art. 15(2)) and, as online platforms, from most platform duties (Art. 19). Under the Commission's recommendation on the definition of SMEs (2003/361/EC, Annex, Art. 3(4)), an enterprise is no SME when public bodies control 25 % or more of its capital or voting rights. Public bodies themselves, such as administrations, universities or a students' union as a body under public law, therefore never get these exemptions:

- they publish the yearly figures (Art. 15),
- if their instance is an online platform, they have all of its duties (Art. 20 to 28), Art. 19 does not lift them.

## Your duties and what Hinata does

| Duty | DSA | In Hinata |
| --- | --- | --- |
| A point of contact for authorities | Art. 11 | **Admin area › Moderation › Contact for reports**. Name the languages you answer in, in your imprint or your house rules. |
| A point of contact for the people who use the service | Art. 12 | The same contact. The app shows it under **Settings › Help and contact** and on the sign-in screen, and `/api/v1/meta` publishes it without signing in. |
| A legal representative in the EU | Art. 13 | Only for providers outside the EU. |
| Terms that say how you moderate | Art. 14 | The **house rules**, in versions that never change again, with **How we moderate** added by the server. Everybody agrees before writing. |
| Yearly figures | Art. 15 | [Yearly figures](#yearly-figures) in the Commission's template, ready to download. |
| Notice and action | Art. 16 | **Report …** on every piece of content and every profile, the form for people without an account, a confirmation of good faith, a receipt, and the outcome for whoever reported. |
| A statement of reasons | Art. 17 | Every removal and every suspension sends the person responsible a statement, in the app and by email. |
| Reporting suspected offences against life or safety | Art. 18 | The plan for moderators, the note **Law enforcement told**, and [reporting to the police](#reporting-to-the-police). |

Hinata also offers what Art. 20 asks of online platforms on every instance: an appeal within six months, decided by somebody who did not decide the first time.

## Your imprint

A digital service offered in Germany for business purposes needs an imprint (§ 5 DDG). Enter the address of your organization's imprint under **Admin area › Moderation › Contact for reports**. The app then links it under **Settings › Help and contact**, and the house rules name it. Hinata does not write the imprint for you.

The imprint of the provider of the app is a different one, see [Imprint](/en/impressum.html).

## Building blocks for your privacy notice

You are the controller for everything moderation processes on your server. The app's privacy policy says so too. Your privacy notice should cover:

- **What is processed:** reports (reason, text, who reported, when), cases (a copy of the reported content, the decision, the statement, the history), the quarantine of removed content, blocks, agreements to the house rules (version and time) and the counters for the yearly figures, which hold no names.
- **Legal bases:** Art. 6(1)(c) GDPR together with Art. 16 to 18 DSA for reports, statements and notifications, and Art. 6(1)(f) GDPR for a safe place to work together and for enforcing the house rules. Public bodies cannot rely on point (f) for their tasks (Art. 6(1), second subparagraph) and use point (e) with the law that gives them the task.
- **The protection of whoever reported:** the reported person does not learn who reported. Informing them would defeat the purpose of the report, which is why the duty to inform does not apply (Art. 14(5)(b) GDPR). In Germany § 29 BDSG also protects what must stay secret for the sake of a third person, in an access request as well. Who reported something about children stays covered always.
- **Retention:** as set under [Retention and backups](#retention-and-backups).
- **The automatic text check:** it runs on your server, and nothing leaves it. While **Send unclear cases to moderation** is on, the server reads every member's texts and reports what it finds without anybody having reported it. That is systematic monitoring: carry out a data protection impact assessment first (Art. 35 GDPR).

## Codetermination

In a company with a works council, moderation and above all the automatic text check can count as technical equipment suited to monitoring the behaviour or performance of employees (§ 87(1) no. 6 BetrVG). Then the works council has to agree first, best in a works agreement. In the public sector the law on staff representation of the federation or of your Land applies. Hinata asks once more before **Send unclear cases to moderation** goes on, for this reason.

## Retention and backups

Under **Admin area › Moderation › Retention and figures** you choose whether done cases are kept for 6 or 12 months. Every night Hinata deletes what has run out: the case, its reports and the quarantine. A decision without an action is kept 30 days, a case where law enforcement was told 12 months at least, and moderators can keep a case longer when an authority needs it. Details are on [Moderation](/en/moderation.html#retention).

Your backups outlast this. A snapshot keeps what it holds until your backup retention removes it, and restic in append-only mode cannot delete single cases. Say so in your privacy notice, and keep the backup retention short. When you restore an older backup, the next nightly run deletes again what has run out in the meantime, because every case carries its own deletion date. See [Backups & upgrades](/en/backups.html).

## Behind a reverse proxy

The form for reports without an account limits how many reports one address may send. Behind a reverse proxy the server only sees the proxy's address unless you set `HINATA_TRUSTED_PROXIES`, and then a single limit holds everybody back at once. **Admin area › Moderation** warns for a day when requests come through a proxy the server does not trust. See [Reverse proxy & TLS](/en/reverse-proxy.html).

## Yearly figures

**Admin area › Moderation › Retention and figures › Download figures for …** gives you a ZIP with one CSV file per part of the Commission's template (Implementing Regulation (EU) 2024/2835, Annex I): parts 1 to 8 and 11. Parts 9 and 10 concern very large platforms only. Earlier years are there to choose from as soon as they have figures.

- **The period is the calendar year.** Publish the report at the latest two months after it ends, so by the end of February (Art. 2(3) of the Implementing Regulation). The files are machine-readable as the Regulation asks: CSV after RFC 4180, in UTF-8.
- **Counted when it happens.** Every report, decision and appeal counts at the moment it happens. A done case is deleted after some months, so the figures could not be read from the cases at the end of the year.
- **No names, no content, no rankings.** The files hold numbers, dates and the names the template itself defines.
- **Blank or zero.** A cell stays blank when it cannot apply on a Hinata server, for example a demotion, which Hinata never does. A zero means it could have happened but did not.

Hinata fills in part 1 with the name of the service (Hinata and your organization), the provider (the operator under **Contact for reports**) and the dates. Before you publish, check the figures and add what Hinata cannot know:

- **Part 3**, orders from authorities of the member states (Art. 9 and 10). Hinata does not record them.
- **Part 11**, the qualitative information in your own words, for example how many people moderate and how they are trained.
- What was dealt with outside Hinata, for example a report that came in by letter.

### Where Hinata's reasons stand in the template

The template has its own categories. Hinata puts each of its eight reasons in one category and one sub-category, so that the sub-categories add up to their category. Where the template has no sub-category for a reason, it stands under *Not captured by any other sub-category*, with a description.

| Reason in Hinata | Reports (part 4) | Measures under the law (part 5) | Measures under the house rules (part 6) |
| --- | --- | --- | --- |
| Harassment, insults or hate | Cyber violence › Cyber harassment | the same | the same |
| Threat or violence | Violence › Incitement to violence and hatred | the same | the same |
| Endangering children | Protection of minors › Child sexual abuse material | the same | the same |
| Private data without consent | Data protection and privacy violations › Missing processing ground | the same | the same |
| Spam, fraud or malware | Scams and fraud › Other: *Spam, phishing and malicious files* | the same | the same |
| Sexual content | Category not specified by the notifier | Cyber violence › Non-consensual image sharing | Other violation of terms and conditions › Adult sexual material |
| Infringement of the law | Category not specified by the notifier | Intellectual property infringements › Other: *Copyright or another right of others* | the same as part 5 |
| Something else | Category not specified by the notifier | only in the total | Other violation of terms and conditions › Other: *Other breaches of the house rules* |

Texts the text check refuses count in part 6 as measures by automated means, under the reason the check found. Refused uploads count there as *Files of a type the instance does not accept*.

## Matching images against known abuse material

Hinata does not compare images with known depictions of child sexual abuse, and it has no connection to a service that does. On a closed instance a person reviews every reported image. If your instance is half open, with many people nobody knows, you can apply for such a service yourself:

- **[Image Intercept](https://www.iwf.org.uk/our-technology/image-intercept)** of the Internet Watch Foundation: free for smaller eligible companies, up to one million checks a month. You register your interest, and the IWF checks whether you are eligible. It matches with PhotoDNA and cryptographic hashes and may only be used to detect, block and remove known material.
- **[Arachnid Shield](https://projectarachnid.com/en/)** of the Canadian Centre for Child Protection: an API without cost for providers, with an API key after signing up. Services with many uploads can apply for a local list of hashes instead.

Either way you build the connection yourself or have it built. The images, or their hashes, go to the service, so check it under data protection law first: a processing agreement, the transfer to the United Kingdom or Canada, and a data protection impact assessment. A match is handled like a report about children: remove, note, report, see the plan in [Moderation](/en/moderation.html#when-life-or-children-are-in-danger).

## Reporting to the police

When a hosting service learns of information that gives rise to a suspicion that a criminal offence involving a threat to the life or safety of a person has taken place, is taking place or is likely to take place, it informs the law enforcement or judicial authorities of the member state concerned at once (Art. 18 DSA). The DSA names the sexual abuse of children among the examples (recital 56).

In Germany the Federal Criminal Police Office (BKA) receives these reports centrally (§ 13 DDG):

1. **Register before you need it.** Access to the BKA's portal at `https://u-entrance.bka.de` is requested by email to `U-Entrance@bka.bund.de`, with the personal address of the person responsible or a neutral address of the team. The BKA confirms the access by email.
2. **The portal takes no emergency calls.** When somebody is in danger right now, call 110.
3. **What a report contains:** whether there is a danger, the area (terrorism, hate crime, sexual offences against children, or other), the account or profile, your case number, a description and the time in UTC.
4. **For depictions of the abuse of children, give the location and the case, never the material.** Nobody forwards it. The content stays in the quarantine, where the police can secure it, and **Law enforcement told** keeps the case long enough for that.

Outside Germany, ask the police of your country or your Digital Services Coordinator where such reports go.
