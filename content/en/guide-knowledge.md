---
title: Writing documentation
description: Write knowledge base articles, organize them and link them to issues and people.
---

# Writing documentation

Issues describe work that is happening. Documentation describes how things *are*: runbooks, decisions, onboarding pages.

That is what the **knowledge base** is for. It's a wiki: pages nest inside pages, anyone who can read a page can edit it, and articles link to the issues and people they are about.

## Spaces, articles and sub-pages

- A **space** is a shelf, such as *Engineering*, *Product*, *Design* or *Operations*. It has a name, an icon, a colour and a one-line description.
- An **article** is a page in a space.
- Any article can have **sub-pages**, as deep as you like. For example, a handbook at the top and its chapters beneath it.

![The knowledge base home: search, a card per space, and the most recently updated articles](/assets/img/shot-knowledge.png)
*The knowledge base home.*

Each card shows a space's colour, description and article count. Below, **Recently updated** lists the latest changes with space and author.

### Creating a space

Click the **New space** tile, enter a name and description, and pick an icon and colour.

![The New space dialog with a name and description filled in](/assets/img/shot-kb-new-space.png)
*The New space dialog.*

**Create space** only becomes active once there is a name. The space then appears on the grid right away.

Prefer a few broad spaces, such as one per team or discipline. One per project rarely fits, because topics outlive projects.

!!! warning "A space can only be deleted while it is empty"
    **Delete space** is only offered on a space with no articles. Move or delete its pages first.

## Write an article

Press **New article**, on the home screen or in the article view next to **All spaces**.

![The article editor on a new page, with a title typed and the body still empty](/assets/img/shot-kb-new-article.png)
*The editor on a new page.*

- **Title** above the toolbar. It becomes the heading, the row in the tree and what people search for. *"Release checklist"* is findable, *"Notes"* is not.
- **Space picker** next to it. You can change it at any time.
- **Button on the right:** **Publish** on new pages, **Save** when editing.

There is no draft state.

!!! tip "Start it as a sub-page"
    Hover the parent in the tree and press the **+** (**Add sub-page**). The article is created in the right place.

## A first page, start to finish

1. Open **Knowledge** in the sidebar and press **New article**.
2. Title it for the question it answers: *"How to roll a release"*, not *"Release"*.
3. Pick the space from the dropdown next to the title.
4. Write the body with **Heading 2** per stage, a **numbered list** for the steps and a **Warning** panel for what can go wrong.
5. Type **@** and pick the related ticket.
6. Press **Publish**.

The page is now searchable by title and text, shows up in **Recently updated**, and the issue lists it under **Documented in**.

## The editor

You write with formatting applied as you go, with no markup and no preview. The toolbar:

| Group | Buttons |
| --- | --- |
| **History** | Undo, Redo |
| **Text style** | A dropdown: Body text, Heading 1 to 3, Quote, Bullet list, Numbered list, Task list, Code block |
| **Formatting** | Bold, Italic, Underline, Strikethrough, Inline code, Link |
| **Alignment** | Left, Centre, Right, Justify |
| **Blocks** | Info panel, Warning, Note, Tip, Divider |
| **Insert** | Insert image, Mention / link (@) |

![The Text style dropdown open over the article editor](/assets/img/shot-kb-text-style.png)
*The Text style dropdown with nine styles.*

- **Text style** is a dropdown because a line can only have one style. A tick marks the current one. If a selection spans several, it reads **Mixed**.
- **Coloured panels** (Info, Warning, Note, Tip) make important points stand out.
- **Task lists** have real checkboxes and are meant for checklists. If items need owners and dates, use [issues](/en/guide-issues.html).
- **Code blocks** carry a language and are coloured to match.

!!! tip "Select text and the tools come to you"
    Highlight text and a small toolbar appears above it with the most common formatting and the link editor. You type the address right above the selected words.

### Keyboard shortcuts

| Shortcut | Does |
| --- | --- |
| **⌘B / Ctrl+B** | Bold |
| **⌘I / Ctrl+I** | Italic |
| **⌘U / Ctrl+U** | Underline |
| **⌘Z / Ctrl+Z** | Undo |
| **⇧⌘Z / Ctrl+Y** | Redo |

There is no shortcut for coloured panels or **@**. You just type **@**.

### Links, images and dividers

- **Links** come from the toolbar or the selection toolbar. **Remove link** takes one off. Unsafe addresses are rejected.
- **Images** are uploaded with the image button and land at the cursor. Resize with the corner handles and add a caption below. PNG, JPEG, GIF and WebP are accepted. SVG is not, because it can carry code. The size limit is set by whoever runs the server, see [Object storage](/en/storage.html).
- **Dividers** are best used sparingly. Headings also feed the outline.

!!! warning "Saving an empty page over a full one is blocked"
    If loading goes wrong, the editor won't save an empty body over existing content, and tells you why.

## Smart links with @

Type **@** in the text or press the **@** button at the end of the toolbar. Pick a suggestion and it becomes a *chip*, a real link.

![The Mention / link picker open over the article editor](/assets/img/shot-kb-mention-picker.png)
*The picker for issues, articles and people.*

The list narrows as you type. Each row shows an icon for its kind and the issue key or space. In the example, `ok` finds four issues, two articles and Amara Okafor.

- **Issue:** shows type, key and current title, and opens on click. Hover (desktop) or long-press (phone) to see status, priority and assignee.
- **Article:** shows the page's icon and title.
- **Person:** shows avatar and first name, even if their job title changes.

If the target disappears, the chip turns red.

!!! warning "Typing HIN-42 by hand is just text"
    Only chips inserted with **@** are links. Typed text opens nothing and doesn't appear in **Linked issues**.

## Documentation that knows what it describes

Chips work in both directions, automatically:

- **Linked issues** at the foot of an article lists every issue it mentions, with current status.
- **Documented in** on an issue lists every article that links to it.

![An issue chip in an article body with its hover preview open](/assets/img/shot-kb-chip-preview.png)
*An issue's preview card.*

The preview card shows status, title, assignee, priority and label, with **Open issue** at the bottom.

![An article with its space tree on the left, the body in the centre, and contributors and details on the right](/assets/img/shot-knowledge-article.png)
*The article view.*

## Finding your way around an article

Three columns. Fold away the side columns with the toggles on their inner edges.

- **Left:** space picker and page tree. The current article is highlighted.
- **Middle:** space chip, title, author, last update, labels and body. **Edit** and delete sit next to the byline.
- **Right:** **On this page** (outline, only with more than one heading), **Contributors**, **Related articles** (pages this one links to) and **Details** (created, space, status).

## Writing on a phone

- The **toolbar scrolls sideways**, with Undo and Redo first.
- The **page tree lives in a drawer**, so the article gets the full width.
- **Long-press a chip** for its preview card.

See [On your phone](/en/guide-mobile.html).

## Reorganising: drag, nest, move

- **Drag a page onto another** to nest it. Sub-pages move with it.
- **Drop it on the root zone** at the top of the tree to move it to the top level.
- **Different space:** open the page, press **Edit** and change the space in the header.

Hovering a row shows **+** (**Add sub-page**) and the menu.

![The row menu of a page in the knowledge tree](/assets/img/shot-kb-tree-menu.png)
*The menu of a page in the tree.*

- **Move to top level** takes the page out of its parent without dragging.
- **Delete** removes the page. If it has sub-pages, the entry reads **Delete (move sub-pages first)** and does nothing.

!!! warning "Deleting is permanent, and parents are protected"
    **Delete** asks for confirmation and names the article. There is no undo and no wastebasket. Pages with sub-pages can only be deleted once those are moved.

## Who can see and change what

| Scope | Who can see it |
| --- | --- |
| **Global** | Everyone with an account on your server |
| **Project** | Everyone who has access to that project |
| **Team** | Members of that team |

- Articles written in the app are **global**.
- Project and team scoped articles come from integrations. If you can't see the project or team, you can't see its pages either, not in search and not in lists.
- Administrators see everything.

Project access: [Projects and teams](/en/guide-projects.html).

!!! warning "Anyone who can read a page can edit or delete it"
    There are no per-article permissions and no read-only mode. Only parent pages with sub-pages are protected from deletion.

## Searching the knowledge base

- **Search field on the knowledge home:** article titles, space names and labels.
- **⌘K palette:** also the text inside articles, plus everything else in Hinata. See [Finding things](/en/guide-search.html).

Labels appear as chips under the title, and both searches match them. A label like `runbook` brings up a whole category. The editor has no label field yet, so labels usually come from whatever created the article.

## What belongs here, and what belongs in an issue

| Write an article when… | Write an issue when… |
| --- | --- |
| It stays true after the work is done | It is done at some point, and then it is over |
| The reader is someone who arrives later | The reader is someone doing it now |
| It describes how a thing works | It describes a change to be made |
| Nobody needs to be assigned to it | Somebody needs to own it and finish it |

Rule of thumb: if the page needs a *status*, it's an issue. If it needs a *last reviewed* date, it's an article.

## Keeping a page current

The byline, **Contributors** and **Details** show the author, last update and creation date. There is no revision history. So:

- **Edit selectively** instead of replacing the whole text.
- **When a page is outdated**, say so at the top and link the page that replaces it, instead of deleting it.

If **Recently updated** hasn't moved in months, the documentation has probably fallen behind.

## Habits that keep a knowledge base alive

- **One page, one subject.** Otherwise split it into a page and a sub-page.
- **Link the issue instead of retelling it.** An `@` chip stays current.
- **Write the warning first**, in a coloured panel near the top.
- **Fix what you notice.** You can edit any page you can read.
- **Use real headings.** They build *On this page*.

## Next steps

- Attach documentation to the work it describes in [Working with issues](/en/guide-issues.html).
- Learn the fastest ways back to a page in [Finding things](/en/guide-search.html).
- See how project and team access is granted in [Projects and teams](/en/guide-projects.html).
