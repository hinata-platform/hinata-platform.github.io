---
title: Grundkonzepte
description: Das Vokabular von Hinata — Organisationen, Projekte und Keys, Workflow-Status, Vorgänge und Hierarchie, Sprints, Teams, Rollen, Anhänge und die Wissensdatenbank.
---

# Grundkonzepte

Diese Seite ist ein Glossar der Ideen, aus denen Hinata aufgebaut ist. Lies sie einmal, und der Rest der Dokumentation — und die App selbst — liest sich sehr viel leichter. Die Konzepte sind grob von außen nach innen gruppiert: zuerst die Organisation, dann die Projekte, dann die Arbeit darin.

## Organisation

Die **Organisation** ist der Container auf oberster Ebene für alles auf einem Hinata-Server — ihren Namen, ihr Branding und die Personen darin. Du erstellst sie beim ersten Start im [Einrichtungsassistenten](/de/setup-wizard.html) (oder legst sie per `HINATA_SETUP_ORGANIZATION_NAME` an). Ein Server hostet eine einzelne Organisation; mehrere unabhängige Organisationen zu betreiben bedeutet, mehrere Server zu betreiben, was das Modell [eine App, selbst gehostete Server](/de/self-hosted-app.html) sauber unterstützt.

## Nutzer & Rollen

Ein **Nutzer** ist eine Person mit einem Konto. Die Authentifizierung kann über lokale Zugangsdaten oder [SSO](/de/sso.html) erfolgen. Die Rollen sind bewusst einfach:

- **ADMIN** — voller Zugriff, einschließlich des Adminbereichs (`/api/v1/admin/**` ist nur für ADMIN): Servereinstellungen, Nutzer, SSO, Git-OAuth-Apps, E-Mail-Ingest und App-weite Flags.
- **Reguläre Nutzer** — alle anderen. Was sie sehen können, wird nicht durch eine globale Rolle bestimmt, sondern durch **Team-Mitgliedschaft und Projektzugriff pro Mitglied** (siehe unten).

!!! info "Sichtbarkeit ist team-gesteuert"
    Jenseits der ADMIN-Rolle verwendet Hinata keine breite Rollenhierarchie. Die Reichweite eines Nutzers über die Plattform hinweg wird davon entschieden, welche Projekte ihm seine Team-Mitgliedschaften gewähren. Siehe [Teams](/de/projects-teams.html).

## Projekte & Projekt-Keys

Ein **Projekt** ist ein Arbeitsbereich für einen Arbeitsstrom — mit eigenen Vorgängen, eigenem Workflow, Labels, Board und Mitgliedern. Jedes Projekt hat einen kurzen, großgeschriebenen **Projekt-Key**, der jeder Vorgangsnummer vorangestellt wird, um einen menschenlesbaren, stabilen Bezeichner zu bilden:

```text
ASTA-42      →  project key "ASTA", issue #42
WEB-1007     →  project key "WEB",  issue #1007
```

Vorgangsnummern sind innerhalb eines Projekts fortlaufend, sodass `ASTA-42` für immer eindeutig ist, in URLs erscheint und das ist, worauf sich Git-[Smart-Commits](/de/git-integration.html) in Branch- und Commit-Nachrichtentext beziehen.

## Workflow-Status

Ein **Workflow-Status** ist eine Spalte im Prozess eines Projekts — wo sich ein Vorgang in seinem Lebenszyklus *befindet* (zum Beispiel *To Do → In Progress → In Review → Done*). Status werden **pro Projekt** definiert und sind farbig: Jeder ist ein `{id, name, hue}`-Datensatz, namensbasiert, und wird in den [Projekteinstellungen](/de/project-settings.html) mit einem Entwurfs- + Speicherleisten-Editor bearbeitet. Das Umbenennen eines Status kaskadiert serverseitig über das gesamte Projekt, sodass bestehende Vorgänge mitgehen.

Board-Spalten bilden auf Workflow-Status ab; Automatisierung (aus Git-Ereignissen) bewegt Vorgänge **vorwärts** durch diese Status, niemals rückwärts.

## Labels

**Labels** sind wiederverwendbare, farbige Tags, die auf ein Projekt beschränkt sind — dieselbe `{id, name, hue}`-Form wie Workflow-Status. Sie klassifizieren Vorgänge (zum Beispiel *backend*, *needs-design*, *customer*) unabhängig von Typ oder Status und werden in den Projekteinstellungen verwaltet. Weil Labels projektbezogen und namensbasiert sind, aktualisiert das Umbenennen eines Labels jeden Vorgang, der es trägt.

## Vorgänge

Ein **Vorgang** ist die atomare Arbeitseinheit — eine Aufgabe, ein Bug, eine Story, ein Feature, ein Epic oder eine Unteraufgabe. Jeder Vorgang trägt:

- einen **Typ** (siehe Hierarchie unten) und eine **Priorität**;
- **Tags/Labels**, **Kommentare** und **[Anhänge](/de/issues.html)** (gespeichert in S3/MinIO);
- **Abhängigkeiten** zu anderen Vorgängen;
- einen **Workflow-Status**, einen **Bearbeiter** und optionale **Start-/Fälligkeitsdaten** sowie **Story Points**.

### Die Vorgangshierarchie

Hinata verwendet eine Jira-artige **dreistufige Hierarchie**:

```text
Epic
 └─ Story / Task / Bug / Feature
     └─ Sub-task
```

- **Epic** — ein großer Arbeitsblock, der viele Vorgänge umspannt.
- **Story / Task / Bug / Feature** — die mittlere Ebene, die alltäglichen Vorgangstypen.
- **Sub-task** — ein kleiner Teil eines einzelnen übergeordneten Vorgangs.

Die App unterstützt dies mit einer Breadcrumb, einer Auswahl für den übergeordneten Vorgang sowie Panels für Kind- / Unteraufgaben, dazu Validierung und kaskadierendes Löschen, damit der Baum konsistent bleibt. Boards können Vorgänge in **Swimlanes** gruppieren nach none / epic / assignee / subtask, mit Epic-Filterung. Mehr dazu unter [Vorgänge & Hierarchie](/de/issues.html).

## Sprints & Backlog

Ein **Sprint** ist ein zeitlich begrenztes Arbeitspaket, das du *planst → startest → abschließt*, mit einer Kapazität und Story Points sowie einem **Burndown**-Bericht. Der **Backlog** ist schlicht die Menge der Vorgänge, die **keinem Sprint zugewiesen** sind — dein Pool anstehender Arbeit. Beim Planen ziehst du Vorgänge aus dem Backlog in einen Sprint. Die Ansichten [Boards & Sprints](/de/boards-sprints.html) bieten einen Board- / Backlog- / Timeline-Umschalter, einen Personenfilter und einen Sprint-Header.

## Teams & Projektzugriff

Ein **Team** ist eine Gruppe von Personen, und es ist der Mechanismus, der die **Sichtbarkeit** über die gesamte Plattform hinweg steuert. Jedes Team gewährt seinen Mitgliedern Zugriff auf bestimmte Projekte; ein Mitglied sieht nur die Projekte, die sein Team-Zugriff erlaubt. Das bedeutet:

- jemanden zu einem Team mit Zugriff auf *Projekt X* hinzuzufügen, macht *Projekt X* für ihn sichtbar;
- eine Person außerhalb jedes Teams, das ein Projekt gewährt, sieht dieses Projekt schlicht nie.

Der Projektzugriff pro Mitglied steuert die app-weite Sichtbarkeit. Siehe [Projekte & Teams](/de/projects-teams.html) für das vollständige Modell.

## Anhänge

**Anhänge** sind an einen Vorgang gebundene Dateien, gespeichert in **S3/MinIO** statt in der Datenbank. Sie verwenden zufällige Objekt-Keys und **vorsignierte Downloads** (die Bytes laufen nie über eine langlebige öffentliche URL), atomares push/pull am Vorgangsdokument und **Live-SSE**, sodass Ergänzungen und Entfernungen für alle, die den Vorgang betrachten, sofort erscheinen. Größen- und Typlimits werden über die Umgebungskonfiguration gesteuert. Die Oberfläche ist ein Drag-and-Drop-Raster mit einer Glas-Lightbox. Details unter [Objektspeicher](/de/storage.html) und [Vorgänge](/de/issues.html).

## Wissensdatenbank

Die **Wissensdatenbank** ist ein Confluence-artiger Bereich hierarchischer **Markdown-Artikel**, entweder global oder auf ein Projekt beschränkt, mit Team-/Projekt-Zugriffssteuerung. Artikel unterstützen **Smart Links**, die zu echten Vorgängen und Personen auflösen, und teilen dieselbe Markdown-Symbolleiste wie der Rest der App. Sie ist vollständig backend-gestützt über `/api/v1/articles`. Siehe [Wissensdatenbank](/de/knowledge-base.html).

## Weitere Bausteine

Ein paar weitere Begriffe, die dir quer durch die Dokumentation begegnen:

- **Workflow-Automatisierung** — Git-Ereignisse (Branch erstellt, Commit gepusht, PR/MR geöffnet/gemergt) bewegen Vorgänge vorwärts durch Workflow-Status. Siehe [Git-Integration](/de/git-integration.html).
- **Smart-Commits** — Trailer in einer Commit-Nachricht, die auf einen Vorgang wirken (`ASTA-42 #comment shipped`, `#time 2h 30m` oder jedes `#word`, um ihn zu überführen).
- **Zeiterfassung** — Arbeitsposten, die gegen Vorgänge mit Aktivitätstypen protokolliert und in wöchentliche Stundenzettel aufsummiert werden. Siehe [Gantt & Zeiterfassung](/de/timeline.html).
- **Benachrichtigungen** — In-App- und E-Mail-Hinweise sowie Push über das [Connect Gateway](/de/connect-gateway.html).
- **Die Befehlspalette** — die ⌘K-Liquid-Glass-[Suche](/de/search.html) und Befehlsoberfläche.

!!! tip "Nächster Schritt"
    Jetzt, wo das Vokabular steht, siehe die [Architektur](/de/architecture.html) dafür, wie sich diese Konzepte über die Leitung bewegen, oder springe in den [Schnellstart](/de/quick-start.html), um sie live zu sehen.
