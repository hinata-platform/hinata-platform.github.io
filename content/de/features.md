---
title: Feature-Tour
description: Ein Rundgang durch alle Bereiche von Hinata, vom Dashboard bis zu Git und SSO.
---

# Feature-Tour

Hinata bündelt agiles Projektmanagement an einem Ort: Arbeit planen, Sprints fahren, Zeit erfassen und Dokumentation schreiben. Alles läuft auf einem selbst gehosteten Server mit einer App für alle Plattformen. Hier bekommt jeder Bereich eine kurze Übersicht und einen Link zur ausführlichen Anleitung.

!!! tip "Neu bei Hinata?"
    Für einen laufenden Stack beginne mit dem [Schnellstart](/de/quick-start.html). Die Begriffe (Organisationen, Projekte, Vorgänge, Sprints, Teams) erklären die [Grundkonzepte](/de/concepts.html).


![Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Eine Plattform für Dashboard, Boards, Sprints, Gantt, Berichte, Wissensdatenbank und mehr.*

## Alle Bereiche im Überblick

| Bereich | Was er tut | Anleitung |
| --- | --- | --- |
| **Dashboard & Berichte** | Fokus für heute, Fertigstellung und Rangliste im Team. Dazu Diagramme zu Burndown, Velocity, Zykluszeit und Verteilung, als PDF exportierbar. | [Berichte & Dashboard](/de/reports.html) |
| **Projekte & Teams** | Projekte mit eigenen Keys (`ASTA-42`), Workflows und farbigen Labels. Teams geben Mitgliedern Zugriff auf Projekte und bestimmen, was jede Person überhaupt sieht. | [Projekte & Teams](/de/projects-teams.html) |
| **Vorgänge & Hierarchie** | Typen, Prioritäten, Labels, Markdown, Kommentare, Anhänge und Abhängigkeiten in der Hierarchie Epic → Story → Sub-Task. | [Vorgänge & Hierarchie](/de/issues.html) |
| **Boards & Sprints** | Agiles Board mit Spalten pro Workflow-Zustand, WIP-Limits, Swimlanes und Backlog. Sprints mit Kapazität und Burndown planen, starten und abschließen. | [Boards & Sprints](/de/boards-sprints.html) |
| **Gantt & Zeiterfassung** | Timeline mit Start- und Fälligkeitsdaten und Abhängigkeiten. Dazu Zeiterfassung mit Aktivitätstypen und wöchentlichen Timesheets. | [Gantt & Zeiterfassung](/de/timeline.html) |
| **Wissensdatenbank** | Hierarchische Markdown-Artikel wie in Confluence, global oder pro Projekt, mit Smart Links auf echte Vorgänge und Personen. | [Wissensdatenbank](/de/knowledge-base.html) |
| **Benachrichtigungen** | In der App, per E-Mail und per Push über das Hinata Connect Gateway. Ein eigenes Firebase-Projekt ist nicht nötig. | [Benachrichtigungen](/de/notifications.html) |
| **Suche & Palette** | Befehlspalette im Liquid-Glass-Stil (⌘K) zum Springen, für Befehle und zuletzt geöffnete Elemente. Auf dem Handy als Sheet. | [Suche & Palette](/de/search.html) |
| **Sprachen** | Neun vollständige Übersetzungen: Englisch, Deutsch, Französisch, Spanisch, Russisch, Chinesisch, Japanisch, Hindi und Arabisch. Arabisch durchgehend von rechts nach links. | [Sprachen](/de/features.html#sprachen) |
| **Git-Integration** | Projekte mit GitHub, GitLab oder Bitbucket verbinden, für Entwicklungsinfos, Smart Commits und Automatisierung über signierte Webhooks. | [Git-Integration](/de/git-integration.html) |
| **Single Sign-on** | OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP, zur Laufzeit im Adminbereich eingerichtet, ohne Neustart. | [SSO](/de/sso.html) |

## Dashboard & Berichte

Auf dem Dashboard landet jede Person. Es zeigt den Fokus für heute, die Fertigstellung, eine Wochenübersicht und eine Rangliste im Team.

Dazu kommen Berichte: Burndown und Velocity für Sprints, Zykluszeit, Erstellt vs. Gelöst sowie Verteilungen nach Zustand, Priorität oder Bearbeiter. Jeder Bericht lässt sich als PDF exportieren, etwa für ein Sprint-Review. Mehr unter [Berichte & Dashboard](/de/reports.html).

## Projekte & Teams

Alles in Hinata liegt in einem **Projekt**. Jedes Projekt hat einen kurzen **Key** (z. B. `ASTA`) als Präfix für Vorgangsnummern (`ASTA-42`), eigene **Workflow-Zustände** und wiederverwendbare **farbige Labels**.

**Teams** regeln, wer was sieht. Ein Team gibt seinen Mitgliedern Zugriff auf bestimmte Projekte. Eine Person sieht in der ganzen App nur die Projekte, die ein Team ihr freigibt. Siehe [Projekte & Teams](/de/projects-teams.html).

## Vorgänge & Hierarchie

Jeder **Vorgang** hat einen Typ (**Epic, Story, Task, Bug, Feature** oder **Sub-Task**), eine Priorität, Labels, eine Markdown-Beschreibung, Kommentare, Anhänge und Abhängigkeiten.

Die Hierarchie hat drei Ebenen wie in Jira: **Epic → Story/Task/Bug/Feature → Sub-Task**. Am Vorgang findest du Breadcrumb, Auswahl des übergeordneten Elements und Panels für untergeordnete Vorgänge und Sub-Tasks. Anhänge kommen live per Server-Sent Events, und Vorgangs-Keys verlinken in deine Git-Historie. Siehe [Vorgänge & Hierarchie](/de/issues.html).

## Boards & Sprints

Das **Board** zeigt die Vorgänge eines Projekts in Spalten nach Workflow-Zustand, per Drag & Drop. WIP-Limits und Swimlanes (nach Epic, Bearbeiter oder Sub-Task) sind optional.

- Der Umschalter **Board / Backlog / Timeline** zeigt dieselbe Arbeit auf drei Arten.
- Der Backlog enthält alles, was noch in keinem Sprint ist.
- **Sprints** laufen durch planen → starten → abschließen, mit Kapazität und Story Points, und speisen den Burndown-Bericht.

Siehe [Boards & Sprints](/de/boards-sprints.html).

## Gantt & Zeiterfassung

Die **Gantt-Timeline** ist eine Leseansicht (Read-Model) über Start- und Fälligkeitsdaten, Abhängigkeiten und Fortschritt deiner Vorgänge. So erkennst du den Ablauf einer Lieferung und den kritischen Pfad.

Mit der **Zeiterfassung** buchen Personen Arbeit mit Aktivitätstypen auf Vorgänge. Daraus entstehen wöchentliche Timesheets für Berichte und Kapazitätsplanung. Siehe [Gantt & Zeiterfassung](/de/timeline.html).

## Wissensdatenbank

Die **Wissensdatenbank** ist ein Bereich für Dokumentation wie Confluence. Sie enthält hierarchische Markdown-Artikel, global oder pro Projekt, mit derselben Zugriffskontrolle über Teams und Projekte wie der Rest der App. Smart Links lösen Vorgänge und Personen beim Tippen auf, damit Dokumente aktuell bleiben. Siehe [Wissensdatenbank](/de/knowledge-base.html).

## Benachrichtigungen

Hinata benachrichtigt in der App, per E-Mail (über dein SMTP-Relay) und per Push auf Android, iOS, macOS und Windows.

- Push läuft über das [Hinata Connect Gateway](/de/connect-gateway.html). Eine veröffentlichte App kann so viele Server bedienen, und du brauchst kein eigenes Firebase-Projekt.
- Unter Linux gibt es keinen Push-Dienst für die App. Dort kommen Benachrichtigungen in der App und per E-Mail an. Die Push-Einstellung des Kontos gilt weiter für das Handy derselben Person.

Jede Person wählt in den [Kontoeinstellungen](/de/authentication.html) über eine Benachrichtigungsmatrix, was sie erhält. Siehe [Benachrichtigungen](/de/notifications.html).

## Suche & Palette

Drücke überall **⌘K** (oder **Strg+K**) für die Befehlspalette im Liquid-Glass-Stil. Sie durchsucht Projekte, Vorgänge, Personen und Artikel, zeigt zuletzt geöffnete Elemente und bietet Schnellbefehle. Auf dem Handy erscheint sie als Sheet. Siehe [Suche & Palette](/de/search.html).

## Sprachen

Hinata gibt es in **neun Sprachen**. Jede ist vollständig übersetzt.

| | Sprache | In eigener Schreibweise | Code |
| --- | --- | --- | --- |
| 🇬🇧 | Englisch | English (UK) | `en` |
| 🇩🇪 | Deutsch | Deutsch | `de` |
| 🇫🇷 | Französisch | Français | `fr` |
| 🇪🇸 | Spanisch | Español | `es` |
| 🇷🇺 | Russisch | Русский | `ru` |
| 🇨🇳 | Chinesisch (vereinfacht) | 简体中文 | `zh` |
| 🇯🇵 | Japanisch | 日本語 | `ja` |
| 🇮🇳 | Hindi | हिन्दी | `hi` |
| 🇸🇦 | Arabisch | العربية | `ar` |

Deine Sprache wählst du unter **Aussehen & App** in [deinem Konto](/de/guide-account.html). Die Oberfläche wechselt sofort. Auch der Server schreibt E-Mails und Fehlermeldungen in dieser Sprache.

**Arabisch läuft von rechts nach links**, und die App folgt dem: Menüs, Listen, Navigation und die Pfeile auf den Schaltflächen.

!!! note "Zu den Flaggen"
    Die Flaggen dienen nur der schnellen Orientierung. Eine Flagge steht für ein Land. Spanisch wird aber nicht nur in Spanien gesprochen und Arabisch in mehr als zwanzig Ländern.

## Git-Integration

Verbinde ein Projekt mit einem oder mehreren Repositories auf **GitHub, GitLab oder Bitbucket**. Hinata nutzt einen echten OAuth-Flow und registriert einen signierten Webhook. Aus Push-, Pull-Request- und CI-Ereignissen werden Entwicklungsinfos am Vorgang: Branches, Commits, PR/MRs und Build-Status.

Dazu kommen **Smart Commits** (`ASTA-42 #comment shipped`, `#time 2h`) und eine Automatisierung, die Vorgänge mit dem Fortschritt vorwärts bewegt. Siehe [Git-Integration](/de/git-integration.html).

## Single Sign-on

Nutze deinen eigenen Identity Provider. Hinata unterstützt **OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP**, zum Beispiel mit Keycloak, Authentik, Azure AD, Google, Synology SSO und weiteren. Du richtest alles zur Laufzeit im Adminbereich ein, ohne Neustart. Siehe [SSO](/de/sso.html).

## Wie es weitergeht

- **[Projekte & Teams](/de/projects-teams.html)**: das erste Projekt einrichten und festlegen, wer es sieht.
- **[Vorgänge & Hierarchie](/de/issues.html)**: alles über Vorgänge.
- **[Boards & Sprints](/de/boards-sprints.html)**: einen agilen Sprint von der Planung bis zum Review.
- **[Grundkonzepte](/de/concepts.html)**: die wichtigsten Begriffe.
