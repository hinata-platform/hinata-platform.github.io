---
title: Knowledge base
description: A built-in, Confluence-style wiki with nested Markdown articles, global or per project.
---

# Knowledge base

Runbooks, onboarding guides, architecture decisions, meeting notes and product specs do not fit into an issue. That is what the **knowledge base** is for: a built-in, Confluence-style wiki right next to your work.

![Hinata knowledge base](/assets/img/shot-knowledge.png)
*Spaces and nested Markdown articles next to your work.*

## Articles

You write articles in **Markdown**, with the same editor and toolbar as issue descriptions: headings, lists, code blocks, tables, callouts and images. Articles nest into a **hierarchy**: a space, its sections and the pages inside them.

- **Global articles:** documentation for the whole workspace, readable by everyone with access. For example a company handbook, engineering standards or incident playbooks.
- **Per-project articles:** documentation for a single project, right next to its board and issues.

!!! info "Backed by real data"
    The knowledge base is a full backend feature (`/api/v1/articles`). Articles are stored and versioned in your database and served through the API like everything else. That makes them searchable, access-controlled and always current.

## Smart links

As you write, **smart links** resolve references live:

- Mention an issue like `MOB-42` and it becomes a link showing its current title and state.
- Mention a person and it links to their profile.

A runbook that references `INF-7` always shows the current issue.

## Access control

Articles follow the same [team and project visibility](/en/projects-teams.html) as the rest of Hinata:

- A per-project space is visible to anyone who can see that project.
- Global spaces follow workspace access.

There is nothing extra to configure.

!!! tip "Link docs and delivery both ways"
    Reference an article from an issue comment and the issue from the article. That keeps the knowledge base alive.

## Next steps

- [Issues](/en/issues.html): the references smart links resolve.
- [Projects & teams](/en/projects-teams.html): who sees which articles.
- [Command palette](/en/search.html): find anything fast.
