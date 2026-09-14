---
title: Reports & dashboard
description: How to read your dashboard and reports, and how to export them.
---

# Reports & dashboard

- The **dashboard** is personal and shows what to do next.
- **Reports** show everyone how a project is going.

Neither needs extra input, and both are only as accurate as your issues.

## Your dashboard

Open **Home** in the sidebar. At the top you see your name, the date and, if a
sprint is running, which day of it you are on.

![The Hinata dashboard](/assets/img/shot-dashboard.png)
*The dashboard.*

### The active-sprint card

When a Scrum board has a sprint running, the large dark card shows:

- the sprint's name and goal
- chips for the sprint day, story points completed out of committed, and issues
  finished out of all issues
- a ring with the progress as a percentage
- avatars of everyone with issues assigned in the sprint

**To board** opens the board. Without a sprint, the card shows a Kanban overview
whose progress counts finished issues instead of points. Without a board, it
offers to plan a sprint.

!!! tip "Pin a board"
    By default the card picks the first running sprint among your projects. Use
    **Customize** to pin a fixed board.

### The four key figures

Tapping a tile opens the Issues list filtered to exactly those issues.

| Tile | What it counts |
| --- | --- |
| **Today's tasks** | *Your* open issues due today or overdue, ordered by priority. |
| **In Progress** | Every started issue in scope that is not done and not in the backlog. |
| **Backlog** | Every issue in scope in Backlog or Open. |
| **Done** | Every issue in scope in one of your project's resolved states. |

!!! warning "Only the first tile is about you"
    The other three count the whole team's work across every project on the
    dashboard.

### Today's focus

The list shows the first five issues from **Today's tasks**, highest priority
first. Each row has the type, title, key and, in red, how overdue it is. The thin
bar on the right is time spent against the estimate, if there is one.

Tap a row to open the issue over the dashboard. **All issues →** opens the full
list. If nothing is due, Hinata shows a short note.

### Project progress

The donut shows the percentage resolved across every project in scope. The
legend splits it into **Done**, **In Progress** and **Backlog**, with the total
count in the corner. If Backlog is the biggest slice, more is coming in than
going out.

### Focus time

Only your logged hours: seven bars for the last seven days (today's in amber)
and the total at the top. **Week** / **Month** shows the last five calendar
weeks. It reads `0.0 h` until work is logged. Time from Git commits is not
included. See [Tracking your time](/en/guide-time.html).

### Team ranking and Git activity

- **Team ranking**: the ten people who resolved the most issues in the last 30
  days. It is meant light-heartedly and deliberately ignores hours.
- **Git activity**: recent commits, pull requests and merges from connected
  repositories. Only shown once [Git integration](/en/git-integration.html) is
  set up.

### Customize

**Customize** in the top-right starts edit mode.

![The dashboard in edit mode](/assets/img/shot-dashboard-customize.png)
*Edit mode.*

- The fields "Hero board", "Dashboard data" and "Team ranking" appear above the
  cards.
- "Hero board" picks the board for the large card. The default is "Automatic
  (active sprint)".
- "Dashboard data" sets which projects the key figures, donut and Today's focus
  count.
- The eye button on a card hides it.

![The hero board picker](/assets/img/shot-dashboard-hero-board-picker.png)
*"Hero board" lists every board you can reach.*

**Done** saves. The layout belongs to your account, so it also applies on your
phone. Without **Done**, your changes are lost.

## Reports

Open **Reports** in the sidebar, or under **More** on a phone. A report always
shows **one project**. The picker under the heading only lists projects your
team access grants you.

![The project picker on the reports page](/assets/img/shot-reports-project-picker.png)
*The project picker.*

### Burndown · last 30 days

![The reports page with burndown, total and states](/assets/img/shot-reports.png)
*Burndown, total issues and states.*

- **Amber line**: open issues on each of the last 30 days, reconstructed
  backwards from today's count.
- **Dashed line**: a straight path from the starting value to zero. It is only a
  reference.
- **Count in the top-right**: today's figure. It is the only measured value.

!!! tip "What the shape means"

    - **Flat:** work gets done as fast as it comes in.
    - **Climbing:** more comes in than gets done. Working faster will not fix
      it.
    - **A drop near the end:** issues sat in review or QA and were closed
      together. Where the delay was stays hidden.
    - **Exactly on the line:** be suspicious. Real work is uneven.

### Total issues

Every issue that has ever existed in the project, resolved or not. Use it as the
scale: 7 issues *In Review* out of 53 is a lot, out of 5,000 it barely matters.

### Issues by state

One bar per state of your project, longest first, in the state's colour and with
the count. Custom states such as *In Parking* or *Signed off* appear too. A
pile-up in one state before done points to a bottleneck.

### Issues by priority

![Priority, assignee and activity further down the reports page](/assets/img/shot-reports-breakdowns.png)
*Priority, assignee and time per activity.*

Look at the proportion. If nearly everything is urgent, it is time for a triage
pass.

### Issues by assignee

Issues nobody owns are collected under **unassigned**. Keep an eye on that row.

!!! warning "Counting issues is not measuring effort"
    Every distribution counts issues. Twelve tiny bugs outweigh one three-week
    migration here. Use the charts to spot patterns, and talk to people to find
    the reasons.

### Time per activity (30 days)

Everyone's logged time on this project over the last 30 days, per activity type.
Only [time entries](/en/guide-time.html) count, not time from Git commits.

### Sprint burndown and velocity live on the board

Sprint metrics are on the board's **Insights** tab, next to Planning and Active
sprint: sprint burndown, velocity across finished sprints, average velocity,
scope changes and work breakdown by assignee. See
[Boards & sprints](/en/guide-boards.html).

## Reading the charts correctly

- **Check the time window.** The burndown, time per activity and team ranking
  cover 30 days, the distributions all time. That is why they can seem to
  disagree.
- **Check your workflow.** If everything sits in one vague *In Progress*, no
  report can show detail. Change that in the
  [project settings](/en/guide-projects.html).
- **Look for gaps.** Missing bars say as much as tall ones.
- **Explain your numbers.** "Fourteen issues are In Review because one person
  does every review" helps more than the number alone.

## Exporting a report

**Export** in the top-right. Each export covers only the project on screen.

![The export menu on the reports page](/assets/img/shot-reports-export-menu.png)
*The export menu.*

- **Export as PDF**: a printable A4 document with your organisation's name and
  logo, the project name, a generated-at timestamp, the total count, the
  burndown, every breakdown as a table (including time per activity) and page
  numbers. It arrives through the share or save dialog, named like
  `hinata-report-Website-Relaunch-2026-08-20.pdf`.
- **Export as CSV** and **Export as JSON**: the same numbers as data. The web
  app downloads them. The desktop and mobile apps copy them to your clipboard
  and confirm with a toast.

!!! tip "Export right before you present"
    Every export is a snapshot with its generation time printed on it.

!!! note "Reports show what you can see"
    The same visibility rules apply as in the rest of the app. See
    [Projects & teams](/en/guide-projects.html).

## Next steps

- Keep [issues](/en/guide-issues.html) in accurate states and give them owners.
- [Track your time](/en/guide-time.html) for accurate effort numbers.
- Get sprint metrics from the Insights tab in [Boards & sprints](/en/guide-boards.html).
