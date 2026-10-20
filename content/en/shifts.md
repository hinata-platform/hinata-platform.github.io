---
title: Shift planning
description: Plan events with shifts that people sign up for. A module of its own that an administrator switches on.
---

# Shift planning

A trade fair stand needs two people every morning and three every afternoon for three days. A club's summer party needs help at the bar, the grill and the till. A public office's workshop has to be staffed every Saturday. Each time it comes down to the same question: who is where and when, and where is someone still missing?

That is what shift planning is for. A project plans **events**, and an event has **shifts** with a start, an end and the number of people needed. Members sign up for open shifts, and whoever plans sees at a glance where places are still free.

!!! info "It has to be switched on"
    Shift planning is a module of its own and is off on a fresh instance. An administrator turns it on under **Admin area → Platform**. While it is off, Hinata behaves exactly as it always has.

## Switching it on

Under **Admin area → Platform** there is a switch called **Shift planning**. It has three positions: on, off and empty. Empty means the environment variable `HINATA_SHIFTS_ENABLED` decides, and that is `false` out of the box. See the [configuration reference](/en/configuration.html#shift-planning).

Saving is enough, no restart needed. The app then shows **Shifts** in the **Plan** group of the navigation, right after time tracking. On a phone it sits in the **More** sheet. Other devices pick up the change once they read the server's settings again, at the latest the next time the app starts.

Switch the module off again and the entry disappears. A link to a shifts page then leads to the "not found" page, and the server answers every request to the module with 404. Stored data is kept.

## Requirement: a replica set

Signing up for a shift gives you a place. Exactly one person gets the last place, even when two tap at the same moment, and nobody can be signed up in two places at the same time. The server guarantees both with MongoDB transactions, and transactions only exist in a **replica set**.

- The production setup from [Deployment](/en/deployment.html) runs as a replica set with transactions switched on (`HINATA_MONGO_TRANSACTIONS`, `true` by default in the `prod` profile). Nothing else to do there.
- If your server runs a single MongoDB without a replica set, shift planning stays off, whatever the switch or the environment says. The server logs a warning with the reason at startup, and the admin area shows the note **Needs a MongoDB replica set** instead of the switch.

How to set up a replica set is described under [MongoDB & X.509](/en/database.html).

## For helpers

Under **Shifts** there are three views: **Mine**, **Calendar** and **Events**. On a phone you switch between them with the pill under the title; on a wide window all three sit side by side in the page head.

### My shifts

At the top is your **next shift** as a card of its own: day and time in large type, how long until it starts, until when it runs, where it takes place and who you share it with. Your other shifts follow, sorted by day. At the end the page shows up to three **open shifts in your projects** from the next two weeks that still need people, and a way to all events.

Every shift shows its staffing as a small hexagon with a figure beside it, such as `2 / 3`. A triangle means someone is still missing, a tick that there are enough people, a lock that the shift is full. If a shift has an upper limit that differs from the number needed, it is shown too: `4 / 3 · max. 5`. A screen reader reads it as a whole sentence, for example "Staffing 2 of 3, 1 more person needed".

Without a connection the page shows what was last loaded. Only your own shifts with times, titles and figures are kept for that, no names of other people. It is deleted when you sign out and when the administration switches the module off.

### Signing up

Under **Events** you see the events of every project you are a member of, or of one project through the project pill. Each event shows how many places are taken and how many shifts still need people. Tapping it opens the event with its shifts, sorted by day. The filter **Understaffed only** hides everything that is already staffed.

A free shift shows **Sign up**. One tap is enough, and you are confirmed straight away. A full shift says so in words, such as "Full, 5 of 5", instead of showing a grey button. If the event head says "Only the organisers assign people", nobody signs up there themselves; the planners assign people.

Tapping a shift opens its sheet: time and length, place, who is signed up and how many places are free. It also leads to the event.

If you already have another shift at the same time, Hinata refuses the sign-up and tells you why. If you are entered as absent on that day, the sign-up still works, but Hinata points it out.

### Confirming and declining

When a planner assigns you to a shift, it appears as **Assigned** in your list and waits for your answer. **Confirm** accepts it. **Decline** (in the sheet or on the next-shift card) frees the place again so the planners can assign someone else.

### Giving up a shift

If you cannot take a confirmed shift after all, open it and choose **Give up**. Hinata asks once, then your place is free again and others can sign up. You can sign up again later as long as there is room.

### Times and time zones

Every event has its own time zone. Hinata shows times as they apply on site. If your device is set to a different time zone, the shift carries a note such as "Times in Europe/Berlin".

## What shift planning is

- **Events inside a project.** An event has a place, a time span and its own time zone. The project's members can see it, nobody else.
- **Shifts with a target and a limit.** Each shift says how many people it needs and, if you like, how many may come at most. Several people in one shift is the normal case, not the exception.
- **Signing up instead of passing lists around.** Helpers put themselves into an open shift. Planners can also assign people directly.
- **Conflicts before they happen.** If two shifts of the same person overlap, the server turns the second one down.
- **For any organization.** A company at a trade fair, a club at its summer party, a public office with on-call duty, an organizer with lots of helpers: the module only knows events, shifts and people.

## What it is not

- **Not time tracking.** A shift records no working time, and the module does not depend on [extended time tracking](/en/time-tracking-advanced.html). Volunteers and outside helpers need no time account to sign up.
- **Not issues.** Shifts do not appear on boards, in sprints or in the issue reports, and they do not count as issues.
- **Not an automatic roster.** Hinata does not hand out people by itself and has no qualifications per shift. Swapping between two people is not a step of its own: one gives the shift up, the other signs up.
- **No two-way sync.** Nothing is synchronized with Google or Microsoft, and appointments from other calendars do not become shifts.

## When something does not work

**Instead of the switch it says "Needs a MongoDB replica set".** The server runs without transactions. Set up a replica set, set `HINATA_MONGO_TRANSACTIONS=true` and restart the server.

**The switch is on, but the app has no "Shifts" entry.** The app has not read the server's settings again yet. Close it and open it again.

**A link to a shift shows "not found".** The module is off on this server, or the link belongs to another server.
