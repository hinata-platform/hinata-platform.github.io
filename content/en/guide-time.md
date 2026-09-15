---
title: Tracking your time
description: Log work on issues, correct entries and review your weekly timesheet.
---

# Tracking your time

You log a duration on an issue and pick the kind of work. Your timesheet, the focus time on your home screen and the effort breakdown in reports are built from those entries.

## Log time on an issue

1. Open the issue and find the **Timeline** card. On a wide window it sits on the right under Details, on a phone further down.
2. Tap **Log time** in the top right corner of the card.
3. Enter the duration and press **Save**.

![The Log time sheet](/assets/img/shot-time-log.png)
*The filled in sheet with 1 hour 30 minutes and activity type Testing.*

Only the duration is required, the note is optional. After saving, the issue's spent total goes up, the entry appears on the card and your timesheet counts it.

!!! tip "Type a duration fast"
    **Hours** starts at `1`, **Minutes** at `0`. For an hour and a half, type `30` into **Minutes**. For 20 minutes, set **Hours** to `0` and **Minutes** to `20`. The boxes only accept digits.

![The Log time sheet on a phone](/assets/img/shot-mobile-time-log.png)
*On a phone the sheet slides up from the bottom and Hours and Minutes stay side by side.*

### What you can and cannot enter

- An entry is at least one minute and at most 24 hours. Split work across midnight over the two days.
- You can back-date up to a year, but you cannot log time in the future. Plans belong in [start and due dates](/en/guide-timeline.html).
- Several entries on the same issue and day are normal and add up.

![The date picker in the Log time sheet](/assets/img/shot-time-date.png)
*The picker opens on today, greys out the future and goes back 365 days.*

### The entry list

![The Timeline card of an issue with its work entries](/assets/img/shot-time-entries.png)
*The Timeline card with the spent line and the eight newest entries.*

Each row shows duration · activity type, with the date on the right. The list holds everyone's entries.

- On other people's entries you only see duration and activity type.
- Name and note show on your own entries. Project leads see them too and can correct entries.

!!! note "Why a colleague's entry has no name on it"
    A name and a day on every entry would create a record of who worked how long on which day. That kind of reading of employee data has to be introduced deliberately, with a works agreement where one applies. An operator policy that opens it up to project leads is planned. Until then the rule is the same for everyone.

**All entries (24)** below the list opens the whole history with the total logged so far. More entries load as you scroll.

## Pick the right activity type

There are six fixed activity types, so they mean the same to everyone and the numbers add up.

![The Activity type menu](/assets/img/shot-time-activity.png)
*The Activity type menu with six entries and no "other".*

- **Development**: writing and changing the thing itself.
- **Testing**: verifying it, manually or by building tests.
- **Documentation**: writing it down, in the [knowledge base](/en/guide-knowledge.html) or anywhere else.
- **Design**: deciding what it should look like or how it should behave.
- **Meeting**: time with other people about this issue.
- **Support**: helping someone else use the thing or get unblocked.

The type powers the **Time per activity** report, which is only accurate if everyone logs meetings as meetings. In the German app the types read *Entwicklung*, *Testen* and so on. Underneath is the same value, so reports count across languages.

## Estimate, spent, and the difference between them

The **Timeline** card shows a line like `Spent 9h 30m of 10h` (see [the entry list](#the-entry-list)).

- The first number is the sum of every entry on the issue, from everybody.
- The second is the **time estimate**, the original guess for the whole job.

When the first number gets close to the second, things are getting tight. A time estimate also shows:

- **On a board card** as a small timer chip with the time spent so far.
- **On the [Timeline view](/en/guide-timeline.html)** as the filled part of the bar. A full bar with days left means the estimate was optimistic.

!!! note "An estimate is not a story point"
    **Estimate** in sprint planning (the deck of Fibonacci cards) sets **story points**, a relative size for planning and velocity. That is a different field from the time estimate, and it is the one most teams use day to day. Without a time estimate the line reads `Spent 9h 30m of —`. Your logged time still counts everywhere.

## The weekly timesheet

**Timesheet** is in the sidebar, behind **More** on a phone.

![The Hinata timesheet, showing one week and its navigation](/assets/img/shot-timesheet.png)
*One week on the timesheet, with a row per person per project.*

### Reading a row

- Each row is one person on one project. The project comes from the issue.
- The columns run Monday to Sunday and end in **Total**.
- A day with no entries shows a dash instead of a zero.

### Moving between weeks

- The week sits in the top right. The arrows next to it step one week back or forward.
- Weeks start on Monday, so Sunday work lands at the end of its own week.
- **Today** in the page header jumps to the current week and reloads it. It is only active when you are looking at another week.

### Whose time you can see

- You only see **your own** work. The server refuses requests for somebody else's hours.
- Administrators see every row. They get a searchable filter for the person and one for the project.

Time on an issue that has since moved, or whose project is gone, is still yours. It shows under **Unassigned**.

!!! note "Empty is not broken"
    "No work items recorded in this week" only covers the week on screen. Step back with the left arrow before assuming something is wrong.

## Filling a week quickly

- **Log when you stop.** You are already on the issue, and the sheet takes four taps.
- **Forgot yesterday?** Open the issues you touched, log there and set the **Date** to yesterday.
- **Log from a commit.** If your project is connected to a Git repository and smart commits are on, this line in the message is enough:

```text
MOB-42 #time 2h 30m
```

Durations understand `w`, `d`, `h` and `m`. A day is 8 hours and a week is 5 days, so `1d 4h` means twelve hours. An administrator connects the repository, see [Git integration](/en/git-integration.html).

The entry belongs to **the author of the commit**, matched by the author e-mail. It shows on their timesheet, in their focus time and in the Time per activity report. It is dated the day the commit was authored, in that person's time zone. Its note holds the short sha and the commit subject. Without an explicit activity type it counts as **Development**.

!!! note "A commit only logs time for an account it can recognise"
    The address has to match an active Hinata account, and that person has to be a member of the project. Otherwise the line is skipped, noted in the server log and no time is logged, not even for whoever connected the repository. If your commits are missing, check `git config user.email` first.

## Correcting an entry

Every entry on the card and in the **All entries** sheet has a menu on the right.

- **Edit** reopens the sheet with the current values. After **Save** the **Spent** total is recomputed. The date rules still apply.
- **Delete** asks first, naming the duration and day, and cannot be undone. **Spent** drops by exactly that amount.

### Whose entries you may change

- **Your own**, always. You can edit and delete them.
- **Somebody else's**, if you lead the project or are an administrator. You may delete them but not edit them, so nothing appears under a name that the person did not log. Ask them to log it again. Every removal goes to the audit log with both names.

!!! tip "Logged too little?"
    Log the missing time as a second entry. Entries on the same issue and day add up. Editing is for a duration that is plainly wrong.

Entries labelled **Smart commits (pre-2.0)** come from older versions that booked time straight from commits with `#time`. They carry no name but still count. Only a lead or an administrator can remove them.

## Working hours, absences and holidays

When your administrators have switched on extended time tracking, your **Settings** have a section **Working hours and absences**. It is for planning only. You can record time on every day, holidays and days you are away included.

- **Planned hours** are your hours per weekday. Until you set your own, the default of the server applies. A change applies from the date you pick, so earlier weeks keep the hours they had. This is also where you pick the holiday calendar you follow.
- **Absences** are vacation, sick days or other time away, for a single day or a span. A single day can be half a day. The note is optional. Only you and the administrators see it.
- **Holidays** come from the calendars your administrators keep in the Admin area under **Holidays**. They enter days by hand or import a year from a calendar address.

What changes on screen:

- The entry list and the calendar mark holidays, absences and days without planned hours. The marking is quiet on purpose, because it is not a lock. A day that really cannot be changed shows a padlock.
- Your own timesheet shows **Your capacity**: your planned hours in the period, less holidays and absences, next to what you booked. Only you see it.
- With working-time hints on, an entry on a holiday gets a hint, just like an entry on a Sunday.

## Where your logged time ends up

1. **The issue**: the spent total is recomputed from all entries, so it is always the true sum.
2. **Focus time on the [dashboard](/en/guide-reports.html)**: your minutes for the last seven days, today in amber. **Month** shows the last five calendar weeks. It only counts *your* entries.
3. **Your weekly timesheet**, as described above.
4. **The Time per activity report** in [Reports](/en/guide-reports.html): a project's time from the last 30 days by activity type, as durations.
5. **Your weekly summary**: the focus time you tracked over the week, next to what you closed. See [Staying informed](/en/guide-notifications.html).

## Habits that make the numbers worth keeping

- **Round gently.** 25 minutes logged as 30 is fine. Two hours logged as a whole day skews every later estimate.
- **Log the meetings.** They are the hours most often left out.
- **Log on the piece you worked on.** Work on a [sub-task](/en/guide-issues.html) goes on the sub-task. Spent time does not roll up to the parent.
- **Don't log on an epic.** Time logged there cannot be tied to specific work.
- **Nobody grades you on hours.** Focus time is only on your own dashboard, and the team ranking counts resolved issues.

!!! info "Logging time sends no notifications"
    People watching the issue are not notified of new entries. If the job turned out much bigger, say so in a [comment](/en/guide-collaboration.html).

## Next steps

- Set the dates that time is measured against on the [Timeline](/en/guide-timeline.html).
- See what your hours turn into on the [dashboard and in reports](/en/guide-reports.html).
- Learn how issues and sub-tasks fit together in [Working with issues](/en/guide-issues.html).
