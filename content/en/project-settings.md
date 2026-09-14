---
title: Project settings
description: Per-project configuration with colored labels and workflow states, draft and save bar, members, team access, the project key and Git connections.
---

# Project settings

The [Admin area](/en/admin-area.html) configures the whole instance. **Project settings** configure a single project: labels, workflow, visibility and connected repositories. The project's lead edits them.

## Labels & workflow states

At the heart of a project's configuration are two lists of colored, named items: **labels** and **workflow states**. Both share the same shape:

```json
{ "id": "…", "name": "In Progress", "hue": 210 }
```

- **`name`**: what you see, and how issues reference the item. Labels and states are **name-keyed**. An issue records the *name*, so states and labels line up by name across the project.
- **`hue`**: the color, stored as a hue on the shared **ProjectPalette**. Every project gets its own consistent coloring instead of a fixed global set.

**Workflow states** are the columns of your [board](/en/boards-sprints.html), e.g. *To Do → In Progress → In Review → Done*. **Labels** are reusable tags you attach to issues from a multi-select picker.

### Draft and save bar

Editing labels and states doesn't save on every keystroke. You edit a **draft**: add, rename, recolor, reorder. While you have unsaved changes, a **save bar** appears where you commit or discard them all at once. A half-finished rename never ripples through the project.

!!! info "Renaming a state cascades"
    Issues reference states and labels by name, so a rename triggers a **server-side rename cascade** that updates existing issues to the new name. Nothing is orphaned. A **boot migration** keeps older data consistent with the current shape.

!!! tip "Colors are per project"
    Hues live on the project's palette, so two projects can use the same state names with different colors without clashing. Pick hues that stay legible in both light and dark mode.

## Members & team access

This is also where you control **who can see and work in the project**. There are two ways:

- **Members:** people added directly to the project.
- **Teams:** Hinata's [teams](/en/projects-teams.html) grant project access per member.

A person only sees a project that their team or a direct membership grants. The check applies app-wide. Restrict a project here and it disappears from the boards, search and reports of anyone without access.

## Project key

Every project has a short **key** (e.g. `ASTA`) that prefixes its issue numbers (`ASTA-42`). Smart commits, branch names and PR titles use it to link work to an issue. See [Git integration](/en/git-integration.html).

## Git connections

A project can connect **one or more repositories** on GitHub, GitLab or Bitbucket from its settings.

- Prerequisite: the operator has registered the OAuth apps in the [Admin area](/en/admin-area.html).
- A project lead adds repositories here and configures automation rules and the branch template (both shared project-wide).
- Each connected repo keeps its own token, webhook and default branch.

Full detail is in [Git integration](/en/git-integration.html).

## How changes propagate

- **Labels and states** save as a batch from the draft when you commit the save bar. The server cascades renames to existing issues.
- **Access changes** take effect immediately. Removing a member or a team's grant hides the project from them across the app.
- **Git connections** register their webhook on connect, so development info shows up on issues right away.

## Where to go next

- [Projects & teams](/en/projects-teams.html): teams, membership and visibility.
- [Boards & sprints](/en/boards-sprints.html): how workflow states become board columns.
- [Git integration](/en/git-integration.html): connect a project's repositories.
