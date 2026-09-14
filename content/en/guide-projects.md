---
title: Projects & teams
description: What a project is, what the HIN-42 key means, and how teams decide which projects you can see.
---

# Projects & teams

Every issue belongs to a **project**. Which projects you can see depends on whether a **team** grants them to you or someone added you directly.

## What a project is

A project holds one area of work: a product, a service or an internal initiative. It has its own issues, its own board, its own columns and its own labels. Projects never get in each other's way.

Every project has:

- **An issue key**, the prefix on every issue in it.
- **Workflow states**, the columns an issue moves through.
- **Labels**, reusable coloured tags.
- **Members**, and one or more **leads**.
- **A board**, a backlog, a timeline and reports, all scoped to it.

### The issue key

When a project is created it gets a short uppercase key, such as `HIN`, `MOB` or `INF`. Its issues are then numbered `HIN-1`, `HIN-2`, `HIN-3` and so on. An issue keeps that name for good.

How to use the key:

- Type `HIN-42` into the search palette to jump straight to the issue.
- Write `HIN-42` in a chat and everyone knows what you mean.
- Put `HIN-42` in a branch name or commit message. If the project is connected to a repository, the work links back to the issue.

Numbers are handed out in order and **never reused**. Even after archiving, deleting or moving `HIN-42`, the `42` does not come back. That makes a key safe to write into documents.

!!! tip "Say it out loud before you commit to it"
    You type the key constantly, in commits, branches and conversations. `HIN` is easy, `PLATFORM2024` is not. Short wins.

!!! note "A key can change later, and it takes its issues with it"
    If the key changes, every issue gets the new prefix and keeps its number: `HIN-42` becomes `PLAT-42`. Old links stop working, so change it early if you can.

### Workflow states, labels and members

- **Workflow states** are the board's columns and the possible status values. New projects start with *Backlog → Open → In Progress → In Review → Done*, with *Done* marked as finished. A lead can change all of it later.
- **Labels** are coloured tags defined once per project and available on every issue in it, such as `design`, `performance`, `security`, `good-first-issue`. Because nobody types them freehand, they stay tidy and searchable.
- **Members** work in the project. They appear in assignee pickers, the board's people filter and reports. Members marked as **lead** may change the project's configuration.

## Browsing your projects

**Projects** in the navigation rail lists every project you can see.

![The Projects overview](/assets/img/shot-projects.png)
*The Projects page, with one card per project.*

The Active / Archived switch sits above the cards, New project at the top right.

Click a card to open the project's **issue list**. The **Settings** button on the card only appears if you are allowed to use it.

### What a card tells you at a glance

- **Square glyph:** the project's picture or, without one, its key in a mono typeface.
- **Line under the name:** key and project lead, such as `HIN · lead admin`.
- **Members** and **States:** how many people work here and how many columns the workflow has.
- **Bar:** how much of the work is resolved.
- **Faces:** the members, with `+2` when not all fit.
- **Tag count:** how many labels the project defines.

### Active and archived

The switch flips between **Active** and **Archived**. The line under the page title shows the count, such as *"3 active · 0 archived"*.

Archived projects are read-only and disappear from the active list. Issues, comments, attachments and history stay findable and readable. Nothing is deleted, and you can bring a project back at any time. This fits finished, cancelled or dormant projects.

### Creating a project

Click **New project** at the top right.

![The New project dialog](/assets/img/shot-project-new.png)
*The key fills in from the name as you type, here BP from "Billing & Plans".*

You also set a description, lead and colour. The line at the bottom names the workflow the project starts with.

You can overwrite the suggested key. It must:

- be uppercase and start with a letter,
- be two to ten characters of letters and digits,
- be unique across the whole server. Otherwise you see *"That key is already taken."* before you can save.

You edit the workflow and labels later in project settings.

## Teams, and why you can't see everything

**You do not automatically see every project on the server.** A colleague may see six projects where you see two. That is not a bug. Project access has to be granted.

### The rule, in three lines

You can see a project if **any one** of these is true:

1. You are a **member of that project** directly.
2. A **team you're on grants** you that project.
3. You are a **platform administrator**, who sees everything.

The server checks this on every request. A project you cannot access therefore also stays out of your issue list, search, reports, board filters and notifications. There is no extra sharing step: being granted access is the access.

### What a team is

A team is a group of people plus a set of projects. Anyone on the team can work in the team's projects. Take a project off the team, and everyone who reached it only through that team loses it.

![A team's overview](/assets/img/shot-team.png)
*A team page with headline counts, projects and recent activity.*

**Teams** in the rail lists the teams you belong to. Each card shows the key, member count, a few faces and how many projects the team grants. On teams you are on yourself, it shows your role: **Admin** or **Member**.

The top of a team page has Add members and Add project. Below are four tabs:

- **Overview:** counts for members, Team-Admins and projects, the granted projects and recent activity.
- **Members:** who is on the team, with role and reachable projects.
- **Projects:** the granted projects. Attach an existing one or create a new one for the team here.
- **Settings:** the team's name, key, colour and icon, a summary of what each role can do, and the danger zone.

### Two roles

| Role | What it can do |
| --- | --- |
| **Team-Admin** | Full control of this team: members, projects, settings. The same rights as a platform administrator, but scoped to this one team. Always sees every project the team owns. |
| **Member** | Works on the projects they're granted. Cannot change the team's membership or its settings. |

### Three levels of project access

When you add someone to a team, you set their role and project access together.

![Step two of Add members](/assets/img/shot-team-add-members.png)
*Step 2, Access: role and project access on one screen.*

Back returns to the People step. Add 1 saves the person, role and access in one go.

- **All projects:** includes projects attached to the team later.
- **Specific projects:** only the projects you tick.
- **No projects yet:** the person is on the team but sees no projects. Useful when you want to sort out access later.

**Team-Admins are the exception:** they always see every project their team owns, whatever the setting says.

### The projects a team owns

The team's **Projects** tab is where you grant projects.

![Adding a project to a team](/assets/img/shot-team-add-project.png)
*Attach existing lists every project the team does not have yet.*

- Each row shows key, name and lead with a tick box. The button counts along, such as **Attach 1**.
- **Create new** creates a project that belongs to the team from day one.

If you remove a project from a team, members lose the access this team gave them. The app tells you before you confirm. Anyone who also reaches the project directly or through another team keeps it. Hinata checks every route.

### "I'm sure this project exists, but I can't find it"

Then you are missing access. You have three options:

- Ask to be **added to the project** as a member.
- Ask to be **added to a team** that grants it.
- If you are already on that team, ask a Team-Admin to widen your *Specific projects* access to include it.

Team-Admins of that team, leads of the project and platform administrators can do this. The change works immediately, no need to sign in again.

!!! warning "Removing access removes it everywhere, at once"
    Taking someone off a team or detaching a project from a team removes everything that grant allowed: the project, its boards, its issues and the notifications about them. The person also stops watching issues they can no longer reach. The work itself is untouched.

!!! note "Deleting a team never deletes its projects"
    Members lose the access the team granted. Projects, boards and issues stay in the workspace. The confirmation says so too.

## An example that makes it click

Three projects: **Hinata Platform** (`HIN`), **Mobile App** (`MOB`) and **Infrastructure** (`INF`). And two teams:

- **Core Platform** grants `HIN` and `INF`.
- **Design & Mobile** grants `MOB`.

Four people:

- **Nora** is a Member of Core Platform with *All projects*. She sees `HIN` and `INF`.
- **Sam** is a Member of Design & Mobile and sees only `MOB`. `HIN` does not appear anywhere for them, not in search, reports or board filters.
- **Ida** is a Team-Admin of Core Platform. She sees `HIN` and `INF` regardless of any access setting. She also leads `INF`, so that is the only card that shows her a Settings button.
- **Ruben** is a Member of Design & Mobile *and* a direct member of `HIN`, because he designs one screen in it. He sees `MOB` through his team and `HIN` through direct membership.

After the initial setup, none of this needs an administrator. Team-Admins grant projects, project leads configure them.

!!! tip "Team grant or direct membership?"
    A **team grant** fits when a whole group needs a project. It stays correct as people join and leave. **Direct membership** fits individuals, such as one designer, one contractor or someone from another department. Mixing both is normal. Access is the union of everything that applies.

## What a project lead can change

A project's **Settings** belong to its **leads** and platform administrators. Regular members never see this page, which is why the Settings button is missing on their card. Leads do not need the admin area for any of this.

![Project settings](/assets/img/shot-project-settings.png)
*Project settings for Hinata Platform.*

General and Leads & members are on the left, Labels, Archive and the Danger zone on the right.

### General

The **picture** (or key glyph), **name**, **key**, **description** and an **accent colour** that tints the project across the app.

Under the key field you see live how issues will be named, such as *"Issues read like HIN-42"*.

### Leads & members

- **Star a member to make them a project lead.**
- A project always needs at least one lead. You cannot save without one.
- **Add members** searches everyone on the server. Newly added people are notified.

### Labels

Type a name, pick a colour, press **Add**. You can rename, recolour or remove labels later. A rename applies to every issue already carrying the label.

### Workflow states

The columns an issue moves through, in order. You can add, rename, drag to reorder and remove states.

- The **Resolved** toggle marks a state as *finished*. Burndown charts, progress rings and struck-through sub-tasks rely on it.
- A project needs **at least two states and at least one resolved state**. The editor won't let you go below that.

![Removing a workflow state that still holds issues](/assets/img/shot-workflow-state-migrate.png)
*"Status still has issues" counts them and offers the remaining states as a destination.*

Migrate & remove stays inactive until you pick one.

!!! warning "Nothing gets stranded"
    A state cannot be removed while issues are in it. You can also move those issues yourself beforehand.

### Saving

Settings are a draft. As soon as you change something, a bar appears at the bottom with **Unsaved changes**, **Discard** and **Save changes**. Nothing reaches the project or anyone else's screen until you save.

If something is invalid, the bar says *"Fix required fields to save"*.

### Archiving

The **Archive** card has one switch: *Project is active*. Turn it off and the project moves to the Archived tab and becomes read-only. It stays complete and readable until someone turns it back on.

When a project ends, this is almost always the right step.

### Deleting

The **Danger zone** at the bottom has one button: **Delete project**. This is the only truly irreversible action.

![The delete-project confirmation](/assets/img/shot-project-delete.png)
*The confirmation shows what will be lost and asks what happens to the issues.*

- It lists the real counts: boards and sprints, the teams the project will be detached from, and wiki articles.
- You can delete the issues or move them to another project.
- Delete stays inactive until you type the project's name.
- A board shared with other projects survives and only loses this one.

!!! warning "Archive instead, unless it was a mistake"
    Deleting is for a project that should never have existed. For one that simply ended, **archive it**. It can be turned back on.

## Who can do what

| Action | Who |
| --- | --- |
| Work in a project: create issues, comment, log time, move cards | Any member of the project |
| See a project at all | Direct members, people a team grants it to, platform administrators |
| Change a project's name, key, labels, workflow, members | Project leads and platform administrators |
| Archive or delete a project | Project leads and platform administrators |
| Add or remove team members, set their role and access | Team-Admins and platform administrators |
| Attach or detach a team's projects | Team-Admins and platform administrators |
| Change a team's name, key, colour or icon | Team-Admins and platform administrators |
| Everything else: users, sign-in, e-mail, integrations | Platform administrators, in the admin area |

For anything in the last row, contact whoever runs the server. The [Admin area](/en/admin-area.html) page describes what lives there.

## Where to go next

- **[Working with issues](/en/guide-issues.html):** how to write good issues.
- **[Boards & sprints](/en/guide-boards.html):** the workflow states as columns you drag cards across.
- **[Finding things](/en/guide-search.html):** search every project you can see, or filter down to one.
- **[Reports & dashboard](/en/guide-reports.html):** where resolved states and progress turn into charts.
- **[Getting started](/en/guide-start.html):** back to the start.
