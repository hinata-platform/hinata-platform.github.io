---
title: Finding things
description: Use the command palette to jump to any issue, project, article or person in two keystrokes, and the issue list to build the exact set of work you need to see.
---

# Finding things

There are two very different questions you ask a tracker. The first is *"where is that one thing?"* — a ticket someone mentioned in a meeting, the runbook you wrote last spring, a colleague's name. The second is *"what does all the work of a certain shape look like?"* — every open bug in two projects, everything due this week, everything nobody has picked up.

Hinata answers the first with the **command palette**, and the second with the **Issues** list. Learning which one to reach for is most of the skill.

## Open the palette from anywhere

Press **⌘K** on a Mac, **Ctrl+K** on Windows and Linux. Both combinations work on every platform — the hint printed on screen simply names the key your keyboard actually has.

You can also click the **Search or jump to…** field in the top bar. It looks like a text field but behaves like a button: clicking it opens the same palette. On a phone the field becomes a magnifier icon in the top bar, and the palette slides down as a full-screen sheet instead of floating in the middle of the window.

The palette opens *over* whatever you were doing. Nothing you have half-typed is lost, nothing scrolls away behind it. Press **Esc**, or click the dimmed background, and you are exactly where you were.

!!! tip "It works while you are deep in something"
    The shortcut is registered by the app itself, not by any particular screen. Reading an issue, dragging a card, in the middle of a comment — ⌘K still opens. The one exception is when another dialog is already on top; the palette will not stack a second window over it.

![The command palette open over the dashboard, showing grouped results for the query "board"](/assets/img/shot-search.png)
*One query, everything at once: the scope chips carry a count each (9 commands, 57 issues, 3 projects, 6 people), matches are highlighted wherever they occur, and every row shows what tells it apart — an issue its key and status, a sprint its goal, an article its space and age. One row is always selected, so __Enter__ opens it. The bar along the bottom names the only three keys you need.*

## What it searches

Start typing and results arrive grouped, always in the same order, so your eye learns where to look:

| Group | What matches |
| --- | --- |
| **Commands** | Actions and destinations inside the app — see [It is also a command bar](#it-is-also-a-command-bar) |
| **Issues** | The title, the issue key (`HIN-42`), and labels — plus words from the description |
| **Projects** | The project name and its key, plus the project description |
| **People** | Display name, username and job title |
| **Boards & Sprints** | Board names, sprint names and sprint goals |
| **Knowledge** | Article titles and labels, plus the text inside the article |

Two kinds of matching run at once, and it is worth knowing the difference because it explains results that would otherwise look inconsistent. **Partial matches** work on the short fields — typing `len` finds *Lena*, `HIN-2` finds `HIN-241`, half a project name finds the project. **Whole words** are additionally matched inside the long fields: descriptions and article bodies. So a fragment of a word will find a title but not a sentence buried in a description; type the whole word for that.

In the default **All** view each group shows up to five results. Pick a single group and you get up to twenty-four.

## Narrow it to one kind of thing

The row of chips under the search field — **All**, **Commands**, **Issues**, **Projects**, **People**, **Boards & Sprints**, **Knowledge** — restricts the search to one category.

![The palette with the Knowledge scope picked and nothing typed](/assets/img/shot-search-scope-knowledge.png)
*Each chip carries the number of items of that kind that exist: 57 issues, 3 projects, 6 people, 4 boards, 8 articles. With __Knowledge__ picked and the field still empty, the palette browses instead of searching — the most recently touched articles, each with the space it lives in and how long ago it changed.*

Click a chip, or press **Tab** to walk forward through them and **Shift+Tab** to walk back. Your query stays in the field while you switch, so you can type once and then flick between "did I mean the issue or the article?".

!!! tip "An empty query in a scope is a browse list"
    It is the fastest way back to whatever the team was working on this morning without knowing a single word of its title.

## The keyboard is the point

| Key | Does |
| --- | --- |
| **↑ / ↓** | Move through results, across group boundaries |
| **↵ Enter** | Open the selected result, or run the selected command |
| **Tab / Shift+Tab** | Move to the next / previous scope chip |
| **Esc** | Close the palette |

The best match is already selected when results land, so the common case is: press ⌘K, type four characters, press Enter. Moving the mouse over a row selects it too, which means you can start on the keyboard and finish with a click without the highlight jumping around.

## Read the results before you open them

Each row carries enough context to answer "is this the one?" without opening anything, and the shape of a row tells you what kind of thing it is:

- **An issue** shows its type glyph, its key in a monospaced face, a coloured status dot with the status name, and the assignee's avatar on the right. Three tickets with nearly identical titles are told apart by their status and their owner, right there in the list.
- **A project** shows a coloured hexagon with the project key, how many issues are open and how many are done, and the faces of its members.
- **A person** shows their avatar and their job title.
- **A board or sprint** shows its name and, for a sprint, its goal — which is usually more recognisable than the sprint number.
- **An article** shows which space it lives in and how long ago it was updated, so a stale duplicate is obvious before you read it.

## Recent searches

Open the palette with an empty field and it shows the last six terms you actually used.

![The palette showing recent searches with an empty query](/assets/img/shot-search-recents.png)
*Under __Recent searches__, most recent first, with __Clear__ on the right. A term is recorded when you open one of its results, not while you type — so the list holds the searches that led somewhere.*

Clicking one puts it back in the field and runs it again; it does not jump straight to a result, because a search you repeat is usually a search you want to look through again. Recents are stored on the device you are using, so your phone and your laptop remember different things.

## It is also a command bar

The palette is not only a search box. Type what you want to *do* and it offers to do it:

- **Go to Dashboard**, **Projects**, **Issues**, **Board**, **Timeline**, **Reports**, **Knowledge** — the whole navigation, without aiming at the sidebar.
- **Create new issue** — takes you to the board, where every column carries an **Add issue** composer at its foot.
- **Toggle light / dark appearance** — flips the theme. This one deliberately leaves the palette open, so you can look at the result and flip back if you dislike it.

Commands are matched on your own device and appear instantly, before results come back from the server. You do not have to type the label exactly: *"dark"*, *"theme"* and *"appearance"* all find the theme switch.

## Where the answers come from

Everything the palette shows comes from your own server. There is no external index, nothing is sent anywhere else, and the results are as fresh as the data — an issue someone renamed a minute ago is findable under its new title.

The app waits a fraction of a second after your last keystroke before asking, and throws away answers that a newer keystroke has already made obsolete. That is why results settle a beat after you stop typing rather than flickering through every intermediate word, and why a slow connection never leaves you looking at the results for `car` when you have typed `carbon`.

Commands are the exception: they are matched on your device, so they appear the instant you type, even before the server has replied.

## When nothing comes back

If the palette says it has no matches, work through this in order:

1. **Is a scope chip still active?** A chip you pressed earlier stays pressed. Press **All** to widen again.
2. **Is it a fragment of a long word?** Fragments match titles, keys and labels — not the text inside descriptions and articles. Try the whole word.
3. **Is it archived?** Prefix the query with `archived`.
4. **Is it in a project you can reach?** Access to projects comes from your project membership and from your teams. If a colleague can see something you cannot, that is the reason — ask them to add you, or see [Projects and teams](/en/guide-projects.html).

## The palette on a phone

On a phone the palette takes the whole screen, sliding down from the top, with the field at the top under your thumb and the keyboard already up. The scope chips scroll sideways, results fill the rest, and the keyboard-hint footer is dropped because there is no keyboard to hint at. Everything else — scopes, recents, the archive keyword, commands — behaves exactly as it does on a desktop. More about the phone layout in [On your phone](/en/guide-mobile.html).

## Six things people actually look for

**"Someone mentioned HIN-42 and I need to read it."**
Type the key. Case does not matter, and you do not need all of it — `hin-4` already narrows the list. Press Enter on the top hit.

**"I remember a phrase from the description, not the title."**
Type the phrase as whole words. Descriptions and article bodies are searched too, so *"certificate rotation"* finds the ticket whose title says nothing of the sort. If nothing comes back, drop to the single most distinctive word — long-field matching is word-by-word, not fragment-by-fragment.

**"I want everything in one project."**
Search the project by name, press Enter on it, and you land on the Issues list already filtered to that project. From there use **Filter** and **Group by** to carve it up.

**"Nobody has picked this up, have they?"**
Open **Issues**, then **Filter → Assignee → Unassigned**. Add **Status** if you only care about work that has already started. This is the query that finds the things quietly rotting at the bottom of a backlog.

**"What did I touch last week?"**
**Filter → Assignee → you**, **Sort → Last modified (new)**, **Time range → Last 7 days**. Group by project if you work across several and want the answer split by area.

**"It was deleted — or was it?"**
Nothing you archive is really gone. Type `archived` followed by what you are looking for — `archived login bug` — and the palette searches the archive instead of the live workspace, across archived issues and archived projects. Type `archived` on its own to see the most recently archived items. The German word `archiviert` works the same way, whichever language your app is set to.

!!! note "Archived issues carry a badge"
    Results from the archive are marked, so you never mistake an archived ticket for a live one. Restoring it is done from the issue itself — see [Working with issues](/en/guide-issues.html).

## Issue keys are addresses

Every issue has a short, permanent key: the project's key, a dash, and a number — `HIN-42`. It is the thing to paste into a chat message, a commit message or a document, because it is short enough to read aloud and unique across the whole server.

On the web app you can go straight to `…/browse/HIN-42` and land on that issue. In the desktop and mobile apps, typing the key into the palette does the same job in fewer keystrokes.

Keys survive a move. If an issue is moved to another project it is renumbered — but the old key keeps working, in the palette, in `browse` links, and in every article or issue that already referenced it. A link you wrote a year ago does not rot because someone reorganised the projects.

!!! tip "Click the key to copy a link"
    On an open issue, clicking its key copies a shareable link to the clipboard — a copy icon appears as you hover, and the key confirms once it is done. That link resolves both ways: it opens the issue inside the app where the app is installed, and in the browser where it is not.

## When you need a list, not a jump

The **Issues** page is the other half of finding things. It shows every issue in every project you have access to, newest activity first, and pages more in as you scroll. Four controls shape it.

![The Issues list with its Group by, Sort, Filter and Time range controls above the table](/assets/img/shot-issues.png)
*The Issues page: 57 issues across every project you can see, the four view controls above the table, and Export on the right. The __Search or jump to…__ field with its ⌘K badge sits in the top bar on every screen.*

### Reading a row

Each row is one issue: its **key**, the **title** with a glyph for its type, its **status**, its **priority**, its **assignee**, and its **due date**. Two of those columns are doing more work than they look:

- **Due** speaks in relative terms while that is useful and in dates once it is not — *3d overdue* and *Today* in red, then *Tomorrow*, then *5d* for anything inside the coming week, then a plain date. You can scan a hundred rows for trouble without reading a single calendar date.
- **Title** carries a small counter when the issue has sub-tasks — `0/1`, `3/4` — so a parent that looks finished but is not says so before you open it.

Clicking anywhere on a row opens the issue.

### Shaping the list

**Filter** opens a popover with five facets — **Status**, **Priority**, **Assignee**, **Project** and **Type** — plus an **Archived** switch. Within one facet the choices are alternatives: picking *Bug* and *Task* shows both. Between facets they add up: *Bug* plus *In Progress* plus *Lena* shows only Lena's in-progress bugs.

![The Filter popover with the Assignee facet open](/assets/img/shot-issues-filter.png)
*One choice in __Status__ and one in __Assignee__: each facet chip carries its own count, the footer reads __2 active__, and the page header counts what survived — 3 of 11 issues. Long facets get a search field of their own, and __Clear all__ in the footer empties every facet at once.*

**Group by** breaks the list into labelled sections. Grouping by assignee before a stand-up turns the list into a per-person agenda; grouping by project turns it into a portfolio view.

![The Group by menu open above the issue list](/assets/img/shot-issues-groupby.png)
*One dropdown rather than a row of controls, with a tick on the grouping in force. The button reads __Group by__ while it is __None__ and takes the grouping's own name once you pick one.*

**Sort** orders the whole result set, not just the rows you have scrolled to: newest first, oldest first, or by last modified in either direction. The default is most recently touched first.

**Time range** narrows by date. It reads dates the way you would: an issue with a start *and* a due date matches when its span overlaps the window, an issue with only one of the two matches when that date falls inside it, and an issue with neither falls back to when it was last touched, so unscheduled work still surfaces.

![The Time range menu open above the issue list](/assets/img/shot-issues-timerange.png)
*Overdue and today at the top, rolling windows in the middle, __Custom range…__ at the foot — that last row opens a calendar where you pick the window yourself. Like __Group by__, the button renames itself to whichever preset is active.*

!!! note "Filters last for the visit, not forever"
    There are no saved views yet. What you set up stays until you leave the page, and the list opens unfiltered next time. For a view you need every day, keep the link — see below — or build it as a [board](/en/guide-boards.html), which does remember its configuration.

## Filters that arrive with a link

Some links carry a filter with them. The tiles on your dashboard are the clearest example: clicking **Today's tasks** opens the Issues list already narrowed to what is due by today, and the number you clicked matches the number of rows you get. Clicking through a project card does the same for that project.

In the web app the address bar carries that scope, so a link you copy from it opens for a colleague filtered the way it was for you.

## Taking the results with you

**Export** writes the complete filtered set, not just the rows you have scrolled into view — the app pages through the whole result on the server first.

![The Export menu open on the Issues toolbar](/assets/img/shot-issues-export.png)
*Three formats behind the __Export__ pill on the right of the toolbar: __Export as PDF__ is a printable table carrying your organisation's name and logo, __Export as CSV__ is for a spreadsheet, __Export as JSON__ for anything that needs to read it back.*

The file lands in your Downloads folder, and the app tells you the file name it used.

## Navigating by hierarchy instead of searching

Some things are easier to walk to than to search for. Work in Hinata nests three levels deep — an **epic** holds stories, tasks, bugs and features, and each of those can hold **sub-tasks** — and every level is navigable:

- Every issue shows a **breadcrumb** above its title. The ancestors are clickable, so one hop takes you from a sub-task to its parent and another to the epic that frames both.
- A parent lists its **child issues** and its **sub-tasks** in panels of their own, with a progress count. If you know the epic, you never need to search for anything inside it.
- On a board, **Group by → Epic** turns the columns into swimlanes, one per epic. It is the fastest way to see a whole initiative at once, including the parts of it nobody is working on.

When you do need to attach something to a parent, the epic and parent pickers open with **recent epics** and **recent issues** already listed — the thing you want is usually one of the last few you touched.

## Looking for a person

People results match on display name, username and job title, so *"Vogt"*, *"lvogt"* and *"Designer"* all find the same colleague. It is a quick way to check who holds a role you only know by description.

To see a person's *work* rather than their profile, go the other way round: open **Issues**, filter by **Assignee**, and group by project or status. The board's **People** filter does the same thing for a single board, which is what most stand-ups actually need.

!!! note "Opening a person needs admin rights"
    A person result leads to the user-management screen, which only administrators can open. Everyone can find people; not everyone can open the directory entry.

## Link once, search less

The best search is the one you never have to run. Whenever you write a description, a comment or an article, type **@** and pick the issue, article or person you mean. What lands in the text is a live link: it shows the issue's real title and status, it opens the issue when clicked, and it feeds the panels that connect things together — **Linked issues** at the foot of an article, **Documented in** on the issue itself.

Typing `HIN-42` as plain characters gives you none of that. It is readable, and someone can paste it into the palette, but the two things stay strangers. One extra keystroke turns a mention into a connection, and it pays back every time somebody else goes looking. See [Writing documentation](/en/guide-knowledge.html) for what those links do once they exist.

## Finding things elsewhere

Search does not only live in the palette:

- The **board** has its own filter, with facets the global list does not need — sprint, author, label and epic — plus a people filter for narrowing to one or two colleagues. See [Boards and sprints](/en/guide-boards.html).
- The **knowledge base** has a search field over the top of its own space grid, matching article titles, space names and labels. See [Writing documentation](/en/guide-knowledge.html).
- **Watched** collects the issues you asked to follow, which is often the shortest path back to work in progress. See [Staying informed](/en/guide-notifications.html).
- Inside an issue, the **@** menu searches issues, articles and people so you can link one to another while you write.

!!! tip "The rule of thumb"
    If you can name the thing, use ⌘K. If you can only describe it — *open, mine, overdue* — use the Issues list. If you need it again tomorrow, make it a board.

## Next steps

- Learn what you can do with what you found in [Working with issues](/en/guide-issues.html).
- Shape the same work visually in [Boards and sprints](/en/guide-boards.html).
- Write the runbook the palette will find next time in [Writing documentation](/en/guide-knowledge.html).
