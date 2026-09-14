---
title: Grundkonzepte
description: Die wichtigsten Begriffe in Hinata, von der Organisation bis zur Wissensdatenbank.
---

# Grundkonzepte

Diese Seite erklärt die Begriffe, auf denen Hinata aufbaut. Sie geht von außen nach innen: Organisation, Projekte, dann die Arbeit darin.

## Organisation

Die **Organisation** ist der oberste Container auf einem Hinata-Server. Sie hat einen Namen, ein Branding und die Personen darin.

- Du legst sie beim ersten Start im [Einrichtungsassistenten](/de/setup-wizard.html) an, oder über `HINATA_SETUP_ORGANIZATION_NAME`.
- Ein Server hostet genau eine Organisation.
- Für mehrere Organisationen betreibst du mehrere Server. Das Modell [eine App, selbst gehostete Server](/de/self-hosted-app.html) unterstützt das.

## Nutzer & Rollen

Ein **Nutzer** ist eine Person mit Konto. Die Anmeldung läuft über lokale Zugangsdaten oder [SSO](/de/sso.html). Es gibt nur zwei Rollen:

- **ADMIN:** voller Zugriff, auch auf den Adminbereich (`/api/v1/admin/**` ist nur für ADMIN). Dazu gehören Servereinstellungen, Nutzer, SSO, Git-OAuth-Apps, E-Mail-Ingest und appweite Flags.
- **Reguläre Nutzer:** alle anderen. Was sie sehen, hängt an ihrer **Teammitgliedschaft und dem Projektzugriff pro Mitglied** (siehe unten).

!!! info "Sichtbarkeit hängt am Team"
    Außer ADMIN gibt es keine Rollenhierarchie. Welche Projekte ein Nutzer sieht, bestimmen seine Teams. Siehe [Teams](/de/projects-teams.html).

## Projekte & Projekt-Keys

Ein **Projekt** ist ein Arbeitsbereich mit eigenen Vorgängen, Workflow, Labels, Board und Mitgliedern.

Jedes Projekt hat einen kurzen **Projekt-Key** in Großbuchstaben. Er steht vor jeder Vorgangsnummer:

```text
ASTA-42      →  project key "ASTA", issue #42
WEB-1007     →  project key "WEB",  issue #1007
```

Die Nummern zählen pro Projekt hoch. `ASTA-42` ist damit dauerhaft eindeutig. Der Schlüssel steht in URLs, und Git-[Smart-Commits](/de/git-integration.html) beziehen sich in Branchnamen und Commit-Nachrichten darauf.

## Workflow-Status

Ein **Workflow-Status** zeigt, wo ein Vorgang im Prozess steht, zum Beispiel *To Do → In Progress → In Review → Done*.

- Status gelten **pro Projekt** und haben eine Farbe.
- Jeder Status ist ein `{id, name, hue}`-Datensatz und wird über den Namen zugeordnet.
- Du bearbeitest sie in den [Projekteinstellungen](/de/project-settings.html). Änderungen landen erst als Entwurf und werden über eine Speicherleiste übernommen.
- Benennst du einen Status um, ändert der Server ihn im ganzen Projekt. Bestehende Vorgänge ziehen mit.

Board-Spalten gehören zu Workflow-Status. Automatisierung aus Git-Ereignissen bewegt Vorgänge nur **vorwärts**, nie zurück.

## Labels

**Labels** sind farbige Tags pro Projekt, mit derselben `{id, name, hue}`-Form wie Status. Sie ordnen Vorgänge unabhängig von Typ und Status ein, zum Beispiel *backend*, *needs-design* oder *customer*.

Du verwaltest sie in den Projekteinstellungen. Benennst du ein Label um, ändert sich jeder Vorgang, der es trägt.

## Vorgänge

Ein **Vorgang** ist die kleinste Arbeitseinheit: Aufgabe, Bug, Story, Feature, Epic oder Unteraufgabe. Jeder Vorgang hat:

- einen **Typ** (siehe Hierarchie) und eine **Priorität**
- **Tags/Labels**, **Kommentare** und **[Anhänge](/de/issues.html)** (gespeichert in S3/MinIO)
- **Abhängigkeiten** zu anderen Vorgängen
- einen **Workflow-Status**, einen **Bearbeiter**, optional **Start- und Fälligkeitsdatum** und **Story Points**

### Die Vorgangshierarchie

Hinata nutzt eine **dreistufige Hierarchie** wie in Jira:

```text
Epic
 └─ Story / Task / Bug / Feature
     └─ Sub-task
```

- **Epic:** ein großer Arbeitsblock über viele Vorgänge.
- **Story / Task / Bug / Feature:** die mittlere Ebene mit den alltäglichen Typen.
- **Sub-task:** ein kleiner Teil eines übergeordneten Vorgangs.

In der App helfen dir eine Breadcrumb, eine Auswahl für den übergeordneten Vorgang und Panels für Kinder und Unteraufgaben. Validierung und kaskadierendes Löschen halten den Baum konsistent. Boards gruppieren Vorgänge in **Swimlanes** nach none / epic / assignee / subtask und filtern nach Epic. Mehr unter [Vorgänge & Hierarchie](/de/issues.html).

## Sprints & Backlog

Ein **Sprint** ist ein zeitlich begrenztes Arbeitspaket. Du *planst → startest → schließt ab*. Er hat eine Kapazität, Story Points und einen **Burndown**-Bericht.

Der **Backlog** sind alle Vorgänge **ohne Sprint**. Beim Planen ziehst du Vorgänge von dort in einen Sprint.

Die Ansichten unter [Boards & Sprints](/de/boards-sprints.html) haben einen Umschalter für Board / Backlog / Timeline, einen Personenfilter und einen Sprint-Header.

## Teams & Projektzugriff

Ein **Team** ist eine Gruppe von Personen. Teams steuern die **Sichtbarkeit** in der ganzen Plattform. Jedes Team gibt seinen Mitgliedern Zugriff auf bestimmte Projekte.

- Kommt jemand in ein Team mit Zugriff auf *Projekt X*, sieht er *Projekt X*.
- Wer in keinem Team mit Zugriff auf ein Projekt ist, sieht es nie.

Das vollständige Modell steht unter [Projekte & Teams](/de/projects-teams.html).

## Anhänge

**Anhänge** sind Dateien an einem Vorgang. Sie liegen in **S3/MinIO**, nicht in der Datenbank.

- Objekt-Keys sind zufällig.
- Downloads laufen über **vorsignierte URLs**, nie über eine dauerhaft öffentliche URL.
- Hinzufügen und Entfernen passiert atomar am Vorgangsdokument.
- Per **Live-SSE** sehen alle, die den Vorgang offen haben, Änderungen sofort.
- Größen- und Typlimits stellst du über Umgebungsvariablen ein.

In der Oberfläche gibt es ein Raster mit Drag and Drop und eine Lightbox. Details unter [Objektspeicher](/de/storage.html) und [Vorgänge](/de/issues.html).

## Wissensdatenbank

Die **Wissensdatenbank** ist ein Bereich mit hierarchischen **Markdown-Artikeln**, ähnlich wie Confluence.

- Artikel sind global oder gehören zu einem Projekt.
- Der Zugriff läuft über Teams und Projekte.
- **Smart Links** verweisen auf echte Vorgänge und Personen.
- Die Markdown-Symbolleiste ist dieselbe wie im Rest der App.
- Die Daten liegen im Backend unter `/api/v1/articles`.

Siehe [Wissensdatenbank](/de/knowledge-base.html).

## Weitere Bausteine

- **Workflow-Automatisierung:** Git-Ereignisse (Branch erstellt, Commit gepusht, PR/MR geöffnet oder gemergt) bewegen Vorgänge vorwärts. Siehe [Git-Integration](/de/git-integration.html).
- **Smart-Commits:** Angaben in der Commit-Nachricht, die auf einen Vorgang wirken, z. B. `ASTA-42 #comment shipped`, `#time 2h 30m` oder ein beliebiges `#word` für einen Statuswechsel.
- **Zeiterfassung:** Arbeitszeit mit Aktivitätstyp an Vorgängen buchen, zusammengefasst in Wochenstundenzetteln. Siehe [Gantt & Zeiterfassung](/de/timeline.html).
- **Benachrichtigungen:** in der App, per E-Mail und als Push über das [Connect Gateway](/de/connect-gateway.html).
- **Die Befehlspalette:** [Suche](/de/search.html) und Befehle über ⌘K.

!!! tip "Nächster Schritt"
    Wie diese Daten zwischen App und Server fließen, zeigt die [Architektur](/de/architecture.html). Live ausprobieren kannst du alles im [Schnellstart](/de/quick-start.html).
