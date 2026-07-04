---
title: Feature-Tour
description: Eine geführte Tour durch alles, was Hinata kann — Dashboard, Projekte, Vorgänge, Boards, Sprints, Gantt, Zeiterfassung, Wissensdatenbank, Benachrichtigungen, Suche, Git und SSO.
---

# Feature-Tour

Hinata ist eine vollständige agile Projektmanagement-Suite an einem Ort: Arbeit planen, Sprints fahren, Zeit erfassen, Dokumentation schreiben und alle auf demselben Stand halten — von einem einzigen selbst-gehosteten Server und einer plattformübergreifenden App aus. Diese Seite ist die Landkarte. Jeder Bereich bekommt eine kurze Tour und einen Link zu seiner ausführlichen Anleitung.

!!! tip "Neu bei Hinata?"
    Wenn du einfach nur einen Stack zum Laufen bringen willst, beginne mit dem [Schnellstart](/de/quick-start.html). Wenn du zuerst die Begriffe verstehen möchtest — Organisationen, Projekte, Vorgänge, Sprints, Teams — lies die [Grundkonzepte](/de/concepts.html).


![Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Eine Plattform: Dashboard, Boards, Sprints, Gantt, Berichte, Wissensdatenbank und mehr.*

## Die Feature-Landkarte

| Bereich | Was er tut | Anleitung |
| --- | --- | --- |
| **Dashboard & Berichte** | Dein Fokus für heute, Fertigstellung und Team-Ranking, dazu Burndown-, Velocity-, Zykluszeit- und Verteilungsdiagramme, die du als PDF exportieren kannst. | [Berichte & Dashboard](/de/reports.html) |
| **Projekte & Teams** | Projekte mit eigenen Keys (`ASTA-42`), Workflows und farbigen Labels; Teams, die Mitgliedern projektbezogenen Zugriff gewähren und bestimmen, was jede Person überhaupt sieht. | [Projekte & Teams](/de/projects-teams.html) |
| **Vorgänge & Hierarchie** | Der zentrale Arbeitsgegenstand — Typen, Prioritäten, Labels, Markdown-Beschreibungen, Kommentare, Anhänge und Abhängigkeiten — in einer dreistufigen Epic → Story → Sub-Task-Hierarchie. | [Vorgänge & Hierarchie](/de/issues.html) |
| **Boards & Sprints** | Ein agiles Board mit Spalten, die auf deine Workflow-Zustände abgebildet sind, WIP-Limits, Swimlanes und einem Backlog; Sprints planen, starten und abschließen mit Kapazität und Burndown. | [Boards & Sprints](/de/boards-sprints.html) |
| **Gantt & Zeiterfassung** | Eine Timeline-Ansicht von Start-/Fälligkeitsdaten und Abhängigkeiten, dazu Arbeitszeiterfassung mit Aktivitätstypen und wöchentlichen Timesheets. | [Gantt & Zeiterfassung](/de/timeline.html) |
| **Wissensdatenbank** | Confluence-artige hierarchische Markdown-Artikel, global oder pro Projekt, mit Smart-Links, die echte Vorgänge und Personen auflösen. | [Wissensdatenbank](/de/knowledge-base.html) |
| **Benachrichtigungen** | In-App- und E-Mail-Benachrichtigungen, dazu mobiler Push über das Hinata Connect Gateway — kein eigenes Firebase-Projekt nötig. | [Benachrichtigungen](/de/notifications.html) |
| **Suche & Palette** | Eine ⌘K-Liquid-Glass-Befehlspalette, um überallhin zu springen, Befehle auszuführen und zuletzt geöffnete Elemente wieder aufzurufen, mit einem responsiven Sheet auf dem Handy. | [Suche & Palette](/de/search.html) |
| **Git-Integration** | Verbinde Projekte mit GitHub, GitLab oder Bitbucket für echte Entwicklungsinfos, Smart Commits und Workflow-Automatisierung über signierte Webhooks. | [Git-Integration](/de/git-integration.html) |
| **Single Sign-on** | OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP, zur Laufzeit im Adminbereich konfiguriert, ohne Neustart. | [SSO](/de/sso.html) |

## Dashboard & Berichte

Das Dashboard ist der Ort, an dem jede Person landet: der Fokus für heute, eine Fertigstellungs-Ansicht, ein Wochen-Tracker und ein freundliches Team-Ranking. Über die persönliche Ansicht hinaus bringt Hinata eine vollständige Berichts-Suite mit — Burndown und Velocity für Sprints, Zykluszeit, Erstellt-vs.-Gelöst und Verteilungen nach Zustand, Priorität oder Bearbeiter. Jeder Bericht lässt sich als PDF exportieren, sodass du ein Sprint-Review direkt in eine Präsentation übernehmen kannst. Mehr dazu unter [Berichte & Dashboard](/de/reports.html).

## Projekte & Teams

Alles in Hinata lebt in einem **Projekt**. Ein Projekt hat einen kurzen **Key** (wie `ASTA`), der zum Präfix jeder Vorgangsnummer wird (`ASTA-42`), einen eigenen Satz **Workflow-Zustände** und eine Palette wiederverwendbarer **farbiger Labels**. **Teams** steuern, wer was sieht: Ein Team gewährt seinen Mitgliedern Zugriff auf bestimmte Projekte, und dieser Zugriff regelt die app-weite Sichtbarkeit — eine Person sieht immer nur die Projekte, die ein Team ihr gewährt. Siehe [Projekte & Teams](/de/projects-teams.html).

## Vorgänge & Hierarchie

Der **Vorgang** ist das Atom der Arbeit. Jeder hat einen Typ (**Epic, Story, Task, Bug, Feature** oder **Sub-Task**), eine Priorität, Labels, eine Markdown-Beschreibung, Kommentare, Anhänge und Abhängigkeiten. Vorgänge verschachteln sich in einer Jira-artigen dreistufigen Hierarchie — **Epic → Story/Task/Bug/Feature → Sub-Task** — mit Breadcrumb, Parent-Auswahl sowie Panels für untergeordnete Vorgänge und Sub-Tasks direkt am Vorgang. Anhänge strömen live über Server-Sent Events herein, und Vorgangs-Keys verlinken direkt in deine Git-Historie. Siehe [Vorgänge & Hierarchie](/de/issues.html).

## Boards & Sprints

Das **Board** verwandelt die Vorgänge eines Projekts in ein agiles Drag-and-Drop-Board, dessen Spalten auf deine Workflow-Zustände abgebildet sind, mit optionalen WIP-Limits und Swimlanes gruppiert nach Epic, Bearbeiter oder Sub-Task. Ein **Board- / Backlog- / Timeline**-Umschalter lässt dich dieselbe Arbeit auf drei Arten planen und visualisieren, und der Backlog hält alles, was noch nicht in einen Sprint gezogen wurde. **Sprints** durchlaufen den vertrauten Zyklus planen → starten → abschließen mit Kapazität und Story Points und speisen den Burndown-Bericht. Siehe [Boards & Sprints](/de/boards-sprints.html).

## Gantt & Zeiterfassung

Die **Gantt-Timeline** ist ein Read-Model über die Start- und Fälligkeitsdaten, Abhängigkeiten und den Fortschritt deiner Vorgänge — eine schnelle Möglichkeit, die Form einer Lieferung zu sehen und wo der kritische Pfad verläuft. Die **Zeiterfassung** lässt Personen Arbeit an Vorgängen mit Aktivitätstypen erfassen, aufsummiert zu wöchentlichen Timesheets für Berichte und Kapazitätsplanung. Siehe [Gantt & Zeiterfassung](/de/timeline.html).

## Wissensdatenbank

Die **Wissensdatenbank** ist ein Confluence-artiger Raum für Dokumentation: hierarchische Markdown-Artikel, die global oder auf ein Projekt beschränkt sein können, mit derselben Team-/Projekt-Zugriffskontrolle wie der Rest der App. Smart-Links lösen echte Vorgänge und Personen beim Tippen auf, sodass deine Dokumentation mit Live-Daten verdrahtet bleibt, statt zu veralten. Siehe [Wissensdatenbank](/de/knowledge-base.html).

## Benachrichtigungen

Hinata hält alle auf dem Laufenden — mit In-App-Benachrichtigungen, E-Mail (über deinen SMTP-Relay) und mobilem Push. Push wird über das [Hinata Connect Gateway](/de/connect-gateway.html) weitergeleitet, was bedeutet, dass eine einzige veröffentlichte App viele Server bedienen kann und Selbst-Hoster kein eigenes Firebase-Projekt brauchen. Jede Person stellt in den [Kontoeinstellungen](/de/authentication.html) über eine Benachrichtigungsmatrix ein, was sie erhält. Siehe [Benachrichtigungen](/de/notifications.html).

## Suche & Palette

Drücke überall **⌘K** (oder **Strg+K**), um die Liquid-Glass-Befehlspalette zu öffnen. Sie sucht über Projekte, Vorgänge, Personen und Artikel hinweg, zeigt zuletzt geöffnete Elemente und bietet Schnellbefehle — alles in einem responsiven Sheet, das auch auf dem Handy hervorragend funktioniert. Siehe [Suche & Palette](/de/search.html).

## Git-Integration

Verbinde jedes Projekt mit einem oder mehreren Repositories auf **GitHub, GitLab oder Bitbucket**. Hinata vermittelt einen echten OAuth-Flow, registriert einen signierten Webhook und verwandelt Push-, Pull-Request- und CI-Ereignisse in vorgangsbezogene Entwicklungsinfos — Branches, Commits, PR/MRs und Build-Status. Ergänze **Smart Commits** (`ASTA-42 #comment shipped`, `#time 2h`) und Workflow-Automatisierung, die Vorgänge vorwärts bewegt, während die Arbeit voranschreitet. Siehe [Git-Integration](/de/git-integration.html).

## Single Sign-on

Bring deinen eigenen Identity-Provider mit. Hinata unterstützt **OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP** — Keycloak, Authentik, Azure AD, Google, Synology SSO und mehr — alles zur Laufzeit im Adminbereich konfiguriert, ohne Neustart. Siehe [SSO](/de/sso.html).

## Wie es weitergeht

- **[Projekte & Teams](/de/projects-teams.html)** — richte dein erstes Projekt ein und steuere, wer es sieht.
- **[Vorgänge & Hierarchie](/de/issues.html)** — der Arbeitsgegenstand von A bis Z.
- **[Boards & Sprints](/de/boards-sprints.html)** — fahre einen agilen Sprint von der Planung bis zum Review.
- **[Grundkonzepte](/de/concepts.html)** — das Vokabular, das alles zusammenhält.
