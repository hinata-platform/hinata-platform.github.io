---
title: Staying informed
description: How Hinata tells you about changes through the bell, e-mail and push, and how to tune it.
---

# Staying informed

Hinata reports events through the bell, e-mail and push. You decide, event by event, what may interrupt you.

## What Hinata notifies you about

These ten events are also the rows in your settings.

| Event | It fires when |
| --- | --- |
| **Mentions & replies** | Someone `@`-mentions you in a description or a comment, or replies to a comment of yours |
| **Issue assigned to you** | You are added as an assignee |
| **Comments on my issues** | Someone comments on an issue you created or watch |
| **Status changes** | An issue you are involved with moves to another column |
| **Watched issues** | Any change at all to an issue you subscribed to |
| **New issues from e-mail** | An incoming e-mail becomes an issue in a project you are part of |
| **Sprints & deadlines** | A sprint starts or completes, or a due date is coming up |
| **Team & project invites** | You are added to a team or a project |
| **Weekly digest** | Your Monday summary of the week |
| **Security alerts** | A new sign-in, a password change, an e-mail change |

Good to know:

- **Assignees and reporters do not need to watch.** Changes reach them through "Status changes". "Watched issues" is for issues nobody is assigned to that you still want to follow.
- **Due dates remind you once.** Every morning the server looks two days ahead and reminds the assignees of unresolved issues. There is one reminder per due date. If the date moves, a new one follows.
- **You never hear about your own actions.** The bell shows what other people did.
- **Nobody hears about work they cannot see.** When sending, Hinata checks that each recipient still reaches the project the issue is in *now*. Someone removed from a project gets no more e-mails about it.

!!! note "New issues from e-mail depend on your server"
    This event only exists if your operator has connected a mailbox to a project. See [E-mail to ticket](/en/email-to-ticket.html).

## The bell and the notification centre

The bell sits in the top bar on every screen. A dot shows that something is unread.

![The notification preview open under the bell with five entries](/assets/img/shot-notification-bell.png)
*The five most recent notices under the bell, unread ones on an amber tint.*

"Mark all read" is in the top right, "View all notifications" at the bottom. The full centre groups notices into **Today**, **Yesterday**, **This week**, **This month** and **Earlier**, and loads more as you scroll.

![The Hinata notification centre](/assets/img/shot-notifications.png)
*In the centre every row explains in one sentence what happened.*

- **Tap** a row to open its destination, such as the comment that mentions you, and mark it read.
- **Swipe right** to flip it between read and unread.
- **Swipe left** to delete your copy. Nothing changes on the issue.

!!! tip "Unread as a to-do list"
    Mark a notice unread again to come back to it later. The dot on the bell stays until you have dealt with it.

## Three channels, and which ones you control

| Channel | Where it shows | Can you turn it off? |
| --- | --- | --- |
| **In-app** | The bell and the notification centre | No, it is always recorded |
| **E-mail** | Your inbox | Yes, per event |
| **Push** | Your phone's or desktop's system notifications | Yes, per event |

The bell always records everything. Your settings only decide whether something also *interrupts* you.

- **E-mail** needs an outbound mail server set up by your operator.
- **Push** works on Android, iOS, macOS and Windows, not on Linux or in the browser. See [Download](/en/download.html).

!!! note "The push switch stays usable everywhere"
    The setting belongs to your **account**. You can change it on Linux or in a browser, and it applies to your phone. The app just notes that this device has no push service.

## Tune what reaches you

Open **Settings → Notifications**.

![The notification matrix in settings with the two master switches above the per-event grid](/assets/img/shot-notification-matrix.png)
*The master switches at the top, then one row per event with "Email" and "Push".*

The masters **E-mail notifications** and **Push notifications** turn a channel off completely. Your per-event choices are kept. A notice is delivered only when the master *and* the cell are on.

![The same notification settings on a phone, one card per event](/assets/img/shot-mobile-notification-matrix.png)
*On a phone each event becomes its own card.*

Defaults for a new account:

| Event | E-mail | Push |
| --- | :---: | :---: |
| Mentions & replies | on | on |
| Issue assigned to you | on | on |
| Comments on my issues | on | off |
| Status changes | off | on |
| Watched issues | on | on |
| New issues from e-mail | off | on |
| Sprints & deadlines | on | on |
| Team & project invites | on | off |
| Weekly digest | on | off |
| Security alerts | locked on | locked on |

Security alerts cannot be switched off. Their row shows a padlock instead of a switch.

!!! tip "Spend two minutes once"
    Turn off the two or three rows you know you will never act on. Then every notice means something.

## Watch an issue to opt in

1. Open the issue.
2. Tap **⋯** in the top bar.
3. Choose **Watch**.

![The watch panel open on an issue, showing the toggle and the watcher list](/assets/img/shot-issue-watch-panel.png)
*The panel with the toggle, your status and "Watchers of this issue".*

A toast confirms it: *You are now watching this issue.* The toggle then reads "Stop watching". A line such as "You already get notifications as the reporter." tells you whether you were covered anyway.

Everything you watch is listed under **Watched** in the sidebar (behind **More** on a phone).

![The Watched issues page](/assets/img/shot-watched.png)
*One row per subscription with state, priority, assignee and due date.*

Before you watch anything, the page tells you how to fill it.

!!! info "Why watched issues do not flood your inbox"
    The bell and push report every change right away. Mail is bundled: after about five minutes without edits you get **one** mail listing all changes, and after half an hour at the latest.

    Assignees and reporters get their mail immediately, even if they also watch.

## Your weekly summary

Every Monday morning Hinata sums up your week: what the team and you closed, your focus time and what is next. It arrives in the bell and, if the "Weekly digest" e-mail is on, as a mail too. Both open the same page. If there is nothing to report, no digest is sent.

![The weekly summary page](/assets/img/shot-weekly-summary.png)
*The weekly summary with key figures, sprint progress and your upcoming to-dos.*

- **Header**: the week, issues the team completed, your own closed count and your focus time.
- **The week behind**: completed, created and focus time tiles plus the active sprint's progress.
- **Top contributors and completed highlights**: who moved what, and a sample of finished work.
- **Your upcoming to-dos**: your open issues ordered by urgency. An **overdue** count sits at the top and overdue items are red. Tap a row to open the issue.

Turn it off in the **Weekly digest** row of your settings.

!!! tip "Read it before your Monday meeting"
    It shows what landed last week and what is at risk this week.

## When something does not arrive

The most common causes are at the top.

1. **Check the master switch.** A silenced channel silences every event, and the app says so at the switch.
2. **Check the event's row.** Comments and status changes are off for one channel each by default.
3. **Check that you are involved.** You hear about issues as assignee, reporter or watcher. Being in the project is not enough.
4. **For push: check your device's permission.** The app asks once at first sign-in. If you declined, allow it in the system settings. Check [Download](/en/download.html) to see whether your platform supports push.
5. **For e-mail: ask your operator.** Without a working outbound mail server, no setting helps.

!!! warning "Deleting a notification does not undo anything"
    You only delete your copy. If the issue should stop bothering you, stop watching it or hand it to someone else.

## Next steps

- [Comments & attachments](/en/guide-collaboration.html): how to write mentions, the biggest source of notifications.
- [Working with issues](/en/guide-issues.html): assignees, reporters and the ⋯ menu.
- [Your account](/en/guide-account.html): the rest of the settings screen.
- [Reports & dashboard](/en/guide-reports.html): the numbers behind the weekly summary, whenever you want them.
