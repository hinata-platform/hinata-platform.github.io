---
title: Tracking your time
description: Log work against an issue, pick the right activity type, read spent versus estimate, fill your weekly timesheet fast, and see where your hours end up.
---

# Tracking your time

Time tracking in Hinata is deliberately small. You log a duration against the
issue you were working on, you say what kind of work it was, and that is the
whole ritual. Everything else — your timesheet, the focus-time chart on your
home screen, the effort breakdown in reports — is built from those entries. No
second tool, no separate spreadsheet, nothing to reconcile at the end of the
month.

That also means the numbers are only as good as the logging. This page is about
making the logging cheap enough that you actually do it.

## Log time on an issue

Open the issue you worked on and find the **Timeline** card — it holds the start
and due dates, the spent-versus-estimate line, and the most recent work entries.
On a wide window it sits in the right-hand column under Details; on a phone it is
further down the page. In the top-right corner of that card is **Log time**.

Tap it and a small glass sheet slides up with four things to fill in:

| Field | What to put in it |
| --- | --- |
| **Hours** / **Minutes** | How long you worked. Two separate boxes; they start at `1` and `0`, so a plain hour is one tap away. |
| **Activity type** | What kind of work it was — Development, Testing, Documentation, Design, Meeting or Support. |
| **Date** | The day the work happened. Defaults to today. |
| **Note (optional)** | A sentence about what you actually did. |

Press **Save** and the entry is recorded immediately. The issue's spent total
goes up, the entry appears in the list at the bottom of the Timeline card, and
your timesheet for that week gains the minutes.

!!! tip "The two-box duration is faster than it looks"
    Leave **Hours** at `1` and type `30` into **Minutes** for an hour and a half.
    For a 20-minute job, clear **Hours** to `0` and put `20` in **Minutes**. The
    boxes only accept digits, so there is no format to remember and nothing to
    get wrong.

### What you can and cannot enter

- **A single entry must be at least one minute and at most 24 hours.** If you
  genuinely worked a marathon session across midnight, log it as two entries on
  the two days it belongs to — which is more accurate anyway.
- **You can back-date up to a year.** The date picker opens on today and lets you
  go back 365 days.
- **You cannot log time in the future.** Today is the last selectable day. Time
  tracking records what happened, not what you intend to happen; that is what
  the [start and due dates](/en/guide-timeline.html) are for.
- **Entries add up.** Logging twice against the same issue on the same day is
  perfectly normal and gives you two lines instead of one bigger one.

### The entry list

Underneath the spent line, the Timeline card lists the most recent entries on
that issue — the eight newest, each as *duration · activity type* with the date
on the right. These are everyone's entries, not just yours, which is exactly
what you want when you are trying to work out why a task that was supposed to
take a day has eaten three.

## Pick the right activity type

The six activity types are fixed, and they are fixed on purpose. A short, shared
list means that six months from now "Testing" still means the same thing to
everyone, and the numbers can actually be added together.

- **Development** — writing and changing the thing itself.
- **Testing** — verifying it, manually or by building tests.
- **Documentation** — writing it down, in the [knowledge base](/en/guide-knowledge.html) or anywhere else.
- **Design** — deciding what it should look like or how it should behave.
- **Meeting** — time spent with other people, about this issue.
- **Support** — helping someone else use or unblock the thing.

The type is what makes the **Time per activity** report meaningful. A team that
discovers it spent more hours in meetings about a feature than building it has
learned something useful — but only if everyone logs meetings as meetings.

!!! note "Your language, one underlying value"
    The activity names are translated in the app — a German colleague sees
    *Entwicklung*, *Testen*, *Dokumentation*. Underneath it is one shared value,
    so a report reads the same regardless of which language each person logged
    in.

## Estimate, spent, and the difference between them

The Timeline card carries one line that quietly does a lot of work:

```text
Spent 3h 30m of 8h
```

The first number is the sum of every work entry on this issue, from everybody.
The second is the issue's **time estimate** — the original guess at how long the
whole job would take. Watching the first number approach the second is the
earliest honest warning you get that something is going sideways.

Where an issue carries a time estimate, it shows up in two more places:

- **On a board card**, as a small timer chip with the time spent so far — so you
  can see effort piling up without opening anything.
- **On the [Timeline view](/en/guide-timeline.html)**, as the filled portion
  inside the issue's bar. A bar that is visually full but has days left on the
  calendar is telling you the estimate was optimistic.

!!! note "An estimate is not a story point"
    The **Estimate** picker you meet during sprint planning — the deck of
    Fibonacci cards — sets **story points**, a relative size used for planning
    and velocity. That is a different field from the time estimate, and it is
    the one most teams use day to day. If nobody has set a time estimate on an
    issue, the spent line simply reads `Spent 3h 30m of —`, and that is fine.
    Your logged time is still counted everywhere else.

## The weekly timesheet

**Timesheet** in the sidebar is the week-at-a-glance view of everything that has
been logged. On a phone it lives behind the **More** tab.

![The Hinata timesheet, showing one week and its navigation](/assets/img/shot-timesheet.png)
*The Timesheet page. The week you are looking at sits in the top-right corner with an arrow on either side; when nothing has been logged in that week, the card says so rather than showing an empty grid.*

### Reading a row

The timesheet is a grid. Each **row** is one person working on one project, and
the columns are:

- **Member** — who logged the time.
- **Project** — the project key the work belongs to, derived from the issue.
- **One column per day**, Monday through Sunday. A day with no entries shows a
  dash rather than a zero, so the days you actually worked stand out.
- **Total** — the row's sum for the week.

If you worked on three projects this week, you get three rows. That split is the
point: it answers "where did my week go?" without anyone having to tag anything
manually.

### Moving between weeks

The week range sits in the top-right of the page with a chevron on either side.
The arrows step one week back or forward. Weeks always start on Monday, so the
grid lines up with how most people talk about a week, and a Sunday session lands
at the end of the week it belonged to rather than the start of the next one.

### Whose time you can see

Your timesheet shows **your own** work. Administrators see everyone's rows,
which is what makes the page useful for a team lead reviewing a week. Nobody
else can browse your hours from here.

!!! note "Empty is not broken"
    "No work items recorded in this week" means exactly that — nothing was
    logged in the week you are looking at. Step back a week with the left arrow
    before assuming something is wrong.

## Filling a week quickly

The trick to a timesheet that reflects reality is never to fill it in as a
timesheet. Log as you go, from the issue you were just working on, and the week
assembles itself.

**Log at the moment you stop, not at the end of the day.** You are already on
the issue. The sheet takes four taps.

**Back-date the whole of yesterday from one sitting.** If you did lose a day,
open each issue you touched, log against it and change the **Date** to
yesterday. You are reconstructing from the issues themselves, which is far more
accurate than reconstructing from memory.

**Let your commits do it.** If your project is connected to a Git repository and
smart commits are switched on, a trailer in the commit message logs the work
without you leaving your editor:

```text
MOB-42 #time 2h 30m
```

Durations understand `w`, `d`, `h` and `m`, and follow the usual convention that
a day is 8 hours and a week is 5 days — so `1d 4h` means twelve hours. Whether
this is available depends on whether an administrator has connected your project
to a repository; see [Git integration](/en/git-integration.html).

!!! warning "Time from a commit is not a timesheet entry"
    A `#time` trailer raises the **Spent** total on the issue, but it does not
    create a work entry with a date and an activity type. It therefore does not
    appear on your timesheet, in your focus-time chart, or in the Time per
    activity report. If those numbers matter to you or to your team, log the
    work in the app as well as — or instead of — in the commit.

## Correcting an entry

Be a little careful here, because this is the one part of time tracking that is
not yet forgiving.

!!! warning "A saved entry cannot be edited in the app"
    There is no edit or delete control on a work entry. Check the duration, the
    date and the issue before you press **Save**.

What to do when it goes wrong anyway:

- **You logged too little.** Log the difference as a second entry. Entries on the
  same issue and day add together, so two entries of 1h and 30m read exactly the
  same as one entry of 1h 30m.
- **You logged too much, or against the wrong issue.** Ask an administrator to
  remove the entry for you — deletion exists on the server, it simply has no
  button in the app yet — and then log it again correctly.
- **You picked the wrong activity type.** In practice this is rarely worth
  unpicking. It shifts a few minutes between two bars on one 30-day report. Get
  the next one right.

## Where your logged time ends up

Every entry you save feeds five different places, which is the argument for
logging even the small stuff.

**The issue itself.** The spent total is recomputed from all its entries, so it
is always the true sum rather than a running counter that can drift.

**Focus time on your home screen.** The bar chart on the [dashboard](/en/guide-reports.html)
shows your own logged minutes for the last seven days, with today's bar
highlighted in amber. Switch it to **Month** and it re-buckets into the last five
calendar weeks. This chart only ever counts *your* entries — it is a personal
mirror, not a team scoreboard.

**Your weekly timesheet**, as described above.

**The Time per activity report.** In [Reports](/en/guide-reports.html), one card
breaks the last 30 days of a project's logged time down by activity type, as
durations rather than counts. This is the team-level view of everything everyone
logged.

**Your weekly summary.** The weekly digest includes a "focused" figure — the
total you tracked over the week — alongside what you closed. See
[Staying informed](/en/guide-notifications.html).

## Habits that make the numbers worth keeping

- **Round gently, don't fabricate.** 25 minutes logged as 30 is fine. Two hours
  logged as a whole day is not, and it will quietly poison every estimate the
  team makes afterwards.
- **Log the meetings.** They are the hours most often left out and the hours most
  worth seeing.
- **Log against the piece you actually worked on.** If the work belongs to a
  [sub-task](/en/guide-issues.html), log it on the sub-task. Spent time stays on
  the issue it was logged against — it does not roll up to the parent — so the
  issue you choose is the issue that will carry the number forever.
- **Don't log against an epic.** An epic is a container. Time logged there is
  time you can no longer attribute to anything specific, and it will never
  appear against the work that actually consumed it.
- **Nobody is grading you on hours.** Focus time is on your own dashboard, and
  the team ranking counts issues resolved — not minutes logged. Log honestly;
  nothing in Hinata rewards inflation.

!!! info "Logging time is quiet"
    Saving a work entry does not notify the people watching the issue. Time
    tracking ticks up constantly and would drown every other notification, so it
    is deliberately left out. If the hours are news — the job turned out to be
    three times the size — say so in a [comment](/en/guide-collaboration.html).

## Next steps

- Set the dates that time is measured against on the [Timeline](/en/guide-timeline.html).
- See what your hours turn into on the [dashboard and in reports](/en/guide-reports.html).
- Learn how issues and sub-tasks fit together in [Working with issues](/en/guide-issues.html).
