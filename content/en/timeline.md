---
title: Gantt & time tracking
description: Your plan on a timeline with dependencies and progress, plus time tracking with activity types and weekly timesheets.
---

# Gantt & time tracking

Two features answer two questions: *when will it land?* and *where did the time go?*

- The **timeline** (Gantt) turns start and due dates into a plan.
- **Time tracking** records the effort actually spent and feeds the [reports](/en/reports.html).

![Hinata Gantt timeline](/assets/img/shot-gantt.png)
*The timeline with dates, dependencies and progress.*

## The timeline

The timeline is built from your issues. Every issue with dates appears as a bar from its **start date** to its **due date**. You see overlaps, gaps and the critical path at a glance.

- **Dependencies**: links between issues are drawn as connectors. When one issue slips, you see what gets pushed back behind it.
- **Progress**: each bar shows how far along its issue is, so you see right away whether the plan is on track.
- **Grouping**: you can follow a project, an epic or an assignee down the timeline.

!!! info "Dates drive the timeline"
    A bar only appears once an issue has a **start** and/or **due** date. Set them on the issue detail view (see [Issues](/en/issues.html)). The timeline updates immediately.

!!! tip "Plan on the board, verify on the timeline"
    Use the [board](/en/boards-sprints.html) to decide *what* goes into a sprint. Use the timeline to check *when* it all has to happen and whether the dependencies line up.

## Time tracking

The timeline shows the plan, time tracking shows what really happened. Anyone working on an issue can log their effort.

### Logging work

Open an issue and choose **Log time**. A work item holds:

- **Duration**: hours and minutes.
- **Activity type**: **Development, Testing, Documentation, Design, Meeting** or **Support**, so effort can be analysed by kind of work.
- **Date**: when the work happened (any day up to today).
- **Note**: optional, what you did.

Each issue shows **spent vs. estimate**, so you notice right away when something is running over.

!!! tip "Log time straight from a commit"
    With [Git integration](/en/git-integration.html) enabled, a smart commit logs work without leaving your editor: `MOB-42 #time 2h 30m` adds a 2½ hour work item to `MOB-42`.

### Weekly timesheets

Work items roll up into a **weekly timesheet**: one row per person and project, one column per day. Use it to review a week, spot gaps and report time without spreadsheets.

## Where the numbers go

Logged time and estimates feed the delivery metrics: capacity planning on [sprints](/en/boards-sprints.html), and cycle time and effort analysis in [Reports](/en/reports.html).

## Next steps

- Set dates and dependencies on your [issues](/en/issues.html).
- Read the delivery metrics in [Reports & dashboard](/en/reports.html).
- Automate time logging with [smart commits](/en/git-integration.html).
