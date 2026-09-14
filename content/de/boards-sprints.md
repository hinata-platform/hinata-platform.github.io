---
title: Boards & Sprints
description: Arbeite auf einem agilen Board mit Spalten, WIP-Limits, Swimlanes und Filtern, und führe Sprints mit Burndown.
---

# Boards & Sprints

Jedes Projekt hat ein agiles Board. Seine Spalten sind deine eigenen [Workflow-Zustände](/de/project-settings.html). Wenn du in Timeboxen arbeitest, planst du dazu Sprints.

!!! info "Zwei Arten von Board"
    **Kanban** ist ein Board mit kontinuierlichem Fluss. **Scrum** baut auf Sprints auf und hat die Tabs Planung, Aktiver Sprint und Insights. Karten, Filter und Swimlanes sind bei beiden gleich.


![Hinata Agile Board](/assets/img/shot-board.png)
*Sprintplanung mit Kapazität, Story Points und aktivem Sprint.*

## Das Board

Jede **Spalte** gehört zu einem oder mehreren Workflow-Zuständen. Sie zeigt einen farbigen Punkt, ihren Namen und ein Zähler-Badge.

- Karten sind deine Vorgänge.
- Epics sind nie Karten. Sie dienen als Swimlane-Überschriften und Filter.
- Sub-Tasks erscheinen nur als Karten, wenn du nach Sub-Task gruppierst.

### Vorgänge verschieben

- **Desktop:** Zieh eine Karte in eine andere Spalte. Der Vorgang bekommt den ersten Zustand dieser Spalte. Die Zielspalte leuchtet dabei in Amber.
- **Smartphone und Tablet:** Karten sind **nur antippbar**. Öffne den Vorgang und ändere den Zustand im Detail-Sheet.

Das Board aktualisiert sich in beiden Fällen live.

### WIP-Limits

Eine Spalte kann ein **Work-in-Progress-Limit (WIP-Limit)** haben. Das Badge zeigt dann `3/5` (aktuell / Limit). Liegt die Spalte über dem Limit, wird das Badge rot.

!!! note "WIP-Limits werden serverseitig konfiguriert"
    Die App zeigt WIP-Limits nur an. Sie gehören zur Spaltenkonfiguration, siehe [Projekteinstellungen](/de/project-settings.html).

### Ansichten

Ein Kanban-Board hat einen **Board / Timeline**-Umschalter. Er zeigt dieselben Vorgänge als Board oder als [Timeline](/de/timeline.html). Auf dem Desktop ist das ein segmentierter Umschalter, auf dem Smartphone ein kompakter.

Der **Backlog** gehört zu Scrum und ist dort ein eigener Tab.

### Filtern

Öffne das **Filter**-Popup, um das Board einzugrenzen. Ein Badge zählt die aktiven Kriterien. Filtern kannst du nach:

**Status · Bearbeiter · Priorität · Typ · Epic · Sprint · Autor · Label**

- Zwischen Facetten gilt **UND**, innerhalb einer Facette **ODER**. Beispiel: „Bug ODER Story“, die außerdem „Ana zugewiesen“ sind.
- Die Facette Sprint hat die Option **Kein Sprint** für Backlog-Elemente.
- Der **Personen**-Streifen mit Avataren über dem Board filtert schnell nach Bearbeiter.
- **Alles zurücksetzen** entfernt alle Filter.

### Swimlanes

Mit **Gruppieren nach** teilst du das Board in horizontale Swimlanes:

| Gruppieren nach | Lanes | Auffang-Lane |
| --- | --- | --- |
| **Keine** | Ein einzelnes flaches Board | (keine) |
| **Epic** | Eine Lane pro Epic | *Kein Epic* |
| **Bearbeiter** | Eine Lane pro Person | *Nicht zugewiesen* |
| **Sub-Task** | Arbeitselemente mit ihren Sub-Tasks gruppieren | *Eigenständig* |

Zusammen mit dem **Epic**-Filter zeigt das Board nur ein Epic und seinen Baum. Das passt gut für ein Standup zu einem Epic.

### Der Backlog

Der **Backlog** enthält alle Vorgänge des Projekts **ohne Sprint**, sortiert nach Priorität. Hier liegt alles, bis du es in einen Sprint ziehst.

## Einen Sprint durchführen

Scrum-Boards haben drei Tabs: **Planung**, **Aktiver Sprint** und **Insights**. Ein Sprint läuft in drei Schritten.

### 1. Planen

Wähle im Tab **Planung** die Option **Sprint erstellen** und setze:

- **Sprint-Name:** vorausgefüllt mit der nächsten Nummer, z. B. `Sprint 3`. Änderbar.
- **Sprint-Ziel:** optional. Was der Sprint liefern soll.
- **Dauer:** 1 bis 4 Wochen (Standard 2). Das Enddatum wird aus dem Startdatum berechnet.
- **Startdatum:** wann die Timebox beginnt.

Danach füllst du den Sprint:

- Zieh Vorgänge aus dem **Backlog** in den Sprint. Auf Touchgeräten wählst du mehrere aus und nutzt **Verschieben nach…**.
- Schätze Vorgänge mit **Story Points** per Planning Poker auf der Fibonacci-Skala.
- Die **Kapazitätsleiste** zeigt `committed / capacity pts` und wird rot, wenn du dich übernimmst.
- Punkt-Buckets zeigen, wie sich die Punkte auf To-do, In Bearbeitung und Erledigt verteilen.

### 2. Starten

Drück **Sprint starten** am Sprint. Der Knopf ist deaktiviert, solange der Sprint leer ist.

Der Dialog fixiert den Umfang und zeigt die Anzahl der Vorgänge und die zugesagten Story Points. Liegst du über dem Ziel, erscheint eine Warnung **über Kapazität**. Bestätige Ziel und Dauer, dann ist der Sprint **Aktiv**.

Der Tab **Aktiver Sprint** zeigt jetzt das laufende Board. Oben stehen ein amberfarbenes **Aktiv**-Badge, Name und Ziel des Sprints und eine Fortschrittsleiste wie `Tag 4/14`.

### 3. Abschließen

Drück am Ende **Sprint abschließen**. Der Dialog zeigt:

- **Abgeschlossen:** erledigte Story Points mit Prozentsatz.
- **Nicht abgeschlossen:** noch offene Punkte.
- **Wohin unfertige Arbeit geht:** offene Vorgänge **überträgst du** in einen anderen geplanten Sprint oder **gibst sie in den Backlog zurück**.

Nach dem Bestätigen wird der Sprint geschlossen. Die offenen Vorgänge landen dort, wo du es gewählt hast.

!!! tip "An Sprint-Grenzen geht nichts verloren"
    Ein Sprintabschluss löscht keine Arbeit. Jeder offene Vorgang wird in den nächsten Sprint oder in den Backlog verschoben.

## Insights & Burndown

Der Tab **Insights** zeigt den Sprint als Diagramme:

- **Sprint-Burndown:** eine gestrichelte *Richtlinie* (idealer Verlauf von den zugesagten Punkten auf null) und eine durchgezogene *Ist*-Linie bis heute. Die y-Achse beginnt bei den Punkten zu Sprintbeginn.
- **Velocity:** zugesagte und erledigte Punkte, dazu ein Durchschnitt über mehrere Sprints.
- **Arbeitsaufteilung nach Bearbeiter** und **Umfangsänderungen:** seit Sprintbeginn netto hinzugefügte oder entfernte Punkte.

Velocity-Trends, Zykluszeit, Verteilungen und PDF-Export über mehrere Sprints findest du unter [Berichte & Dashboard](/de/reports.html).

## Verwandte Seiten

- **[Vorgänge & Hierarchie](/de/issues.html):** die Karten auf deinem Board und wie sie sich verschachteln.
- **[Projekteinstellungen](/de/project-settings.html):** die Workflow-Zustände hinter deinen Spalten.
- **[Gantt & Zeiterfassung](/de/timeline.html):** die Timeline und das Erfassen von Arbeit.
- **[Berichte & Dashboard](/de/reports.html):** Velocity, Burndown-Verlauf und Exporte.
