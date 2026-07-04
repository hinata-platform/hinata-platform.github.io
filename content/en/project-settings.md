---
title: Project settings
description: Per-project configuration in Hinata — colored labels and workflow states, the draft + save-bar editor, members and team access, the project key, and Git connections.
---

# Project settings

Where the [Admin area](/en/admin-area.html) configures the whole instance,
**Project settings** configure a single project: its labels, its workflow, who
can see it, and which repositories it tracks. Everything here is scoped to one
project and edited by that project's lead.

## Labels & workflow states

The heart of a project's configuration is two lists of colored, named items —
**labels** and **workflow states**. Both share the same shape:

```json
{ "id": "…", "name": "In Progress", "hue": 210 }
```

- **`name`** — what you see, and how issues reference the item. Labels and states
  are **name-keyed**: an issue records the *name*, so states and labels line up by
  name across the project.
- **`hue`** — a color, stored as a hue on the shared **ProjectPalette**, so every
  project gets its own consistent, per-project coloring rather than a fixed
  global set.

**Workflow states** are the columns your [board](/en/boards-sprints.html) maps to
— e.g. *To Do → In Progress → In Review → Done*. **Labels** are the reusable
tags you attach to issues from a multi-select picker.

### The draft + save-bar editor

Editing labels and states doesn't save on every keystroke. You edit a **draft** —
add, rename, recolor, reorder — and a **save bar** appears while you have unsaved
changes, letting you commit them all at once or discard them. This keeps a
half-finished rename from immediately rippling through the project.

!!! info "Renaming a state cascades"
    Because issues reference states and labels by name, renaming one triggers a
    **server-side rename cascade**: existing issues are updated to the new name so
    nothing is orphaned. A **boot migration** keeps older data consistent with the
    current shape as the platform evolves. You rename once; the project catches up.

!!! tip "Colors are per project"
    Hues live on the project's palette, so two projects can use the same state
    names with different colors without clashing. Pick hues that stay legible in
    both light and dark mode.

## Members & team access

Project settings is also where you control **who can see and work in the
project**. Visibility is gated two ways:

- **Members** — the people directly added to the project.
- **Teams** — Hinata's [teams](/en/projects-teams.html) grant project access per
  member. A person only sees a project their team (or direct membership) grants;
  this access check gates the project's visibility app-wide, so restricting a
  project here removes it from the boards, search and reports of anyone without
  access.

## Project key

Every project has a short **key** (e.g. `ASTA`) that prefixes its issue numbers
(`ASTA-42`). The key is what smart commits, branch names and PR titles reference
to link work back to an issue — see [Git integration](/en/git-integration.html).

## Git connections

A project can connect **one or more repositories** on GitHub, GitLab or
Bitbucket from its settings. Once the operator has registered the OAuth apps in
the [Admin area](/en/admin-area.html), a project lead adds repositories here,
configures automation rules and the branch template (shared project-wide), and
each connected repo keeps its own token, webhook and default branch. Full detail
is in [Git integration](/en/git-integration.html).

## How changes propagate

- **Labels/states** save as a batch from the draft when you commit the save bar;
  renames cascade to existing issues server-side.
- **Access changes** take effect immediately — removing a member or a team's
  grant hides the project from them across the app.
- **Git connections** register their webhook on connect, so development info
  starts flowing onto issues right away.

## Where to go next

- [Projects & teams](/en/projects-teams.html) — teams, membership and visibility.
- [Boards & sprints](/en/boards-sprints.html) — how workflow states become board columns.
- [Git integration](/en/git-integration.html) — connect a project's repositories.
