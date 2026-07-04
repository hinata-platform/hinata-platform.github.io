---
title: Boards & Sprints
description: Steuere deine Arbeit auf einem agilen Board — Spalten, die auf Workflow-Zustände abgebildet sind, WIP-Limits, Swimlanes und Filter — und führe Sprints von der Planung über den Start bis zum Abschluss mit Burndown.
---

# Boards & Sprints

Das Board ist der Ort, an dem die Vorgänge eines Projekts zu einem lebendigen, beweglichen Abbild der Arbeit werden. Hinata gibt jedem Projekt ein agiles Board, dessen Spalten deine eigenen [Workflow-Zustände](/de/project-settings.html) sind, plus vollständige Sprint-Planung, wenn du in Timeboxen arbeiten möchtest. Diese Seite führt durch beides.

!!! info "Zwei Arten von Board"
    Ein Board ist entweder **Kanban** — ein Board mit kontinuierlichem Fluss — oder **Scrum** — ein Board rund um Sprints mit den Tabs Planung, Aktiver Sprint und Insights. Beide teilen dieselben Karten, Filter und Swimlanes; sie unterscheiden sich darin, wie sie die Zeit organisieren. Wähle das Board, das zur Arbeitsweise deines Teams passt.


![Hinata Agile Board](/assets/img/shot-board.png)
*Sprint-Planung — Kapazität, Story Points und der aktive Sprint auf einen Blick.*

## Das Board

Jede **Spalte** ist einem oder mehreren Workflow-Zuständen zugeordnet und zeigt einen farbigen Punkt, den Spaltennamen und ein Zähler-Badge. Karten sind deine Vorgänge. Epics erscheinen nie als Karten — sie fungieren stattdessen als Swimlane-Überschriften und Filter — und Sub-Tasks erscheinen nur dann als Karten, wenn du nach Sub-Task gruppierst.

### Vorgänge verschieben

Auf dem Desktop **ziehst du eine Karte** von einer Spalte in eine andere, um ihren Workflow-Zustand zu ändern — beim Ablegen wird der Vorgang auf den ersten Zustand dieser Spalte gesetzt, und die Zielspalte leuchtet beim Überfahren in Amber auf. Auf Smartphones und Tablets sind Karten **nur antippbar**: Öffne den Vorgang und ändere seinen Zustand über das Detail-Sheet. In beiden Fällen aktualisiert sich das Board live.

### WIP-Limits

Eine Spalte kann ein **Work-in-Progress-Limit (WIP-Limit)** tragen. Wenn gesetzt, zeigt das Zähler-Badge `3/5` (aktuell / Limit) an; wenn eine Spalte ihr Limit überschreitet, wird das Badge rot, sodass eine Überlastung unmöglich zu übersehen ist.

!!! note "WIP-Limits werden serverseitig konfiguriert"
    Das Board zeigt WIP-Limits an, bearbeitet sie aber nicht in der App — sie sind Teil der Spaltenkonfiguration. Siehe [Projekteinstellungen](/de/project-settings.html) für die Einrichtung von Workflow und Spalten.

### Ansichten

Ein Kanban-Board bietet einen **Board / Timeline**-Umschalter — dieselben Vorgänge als Fluss-Board oder als [Timeline](/de/timeline.html). Auf dem Desktop ist dies ein segmentierter Umschalter; auf dem Smartphone klappt er zu einem kompakten Umschalter zusammen. **Backlog** ist ein Scrum-Konzept und erscheint daher als eigener Tab auf Scrum-Boards statt im Kanban-Umschalter.

### Filtern

Öffne das **Filter**-Popup (ein Liquid-Glass-Popover mit einem Badge, das die aktiven Kriterien zählt), um das Board einzugrenzen. Du kannst filtern nach:

**Status · Bearbeiter · Priorität · Typ · Epic · Sprint · Autor · Label**

Filter kombinieren sich als **UND über Facetten hinweg, ODER innerhalb einer Facette** — zum Beispiel "Bug ODER Story", die außerdem "Ana zugewiesen" sind. Die Facette Sprint enthält eine Option **Kein Sprint** für Backlog-Elemente. Ein **Personen**-Streifen mit Bearbeiter-Avataren sitzt über dem Board als schneller Kurzweg in die Facette Bearbeiter, und **Alles zurücksetzen** setzt alles zurück.

### Swimlanes

Nutze **Gruppieren nach**, um das Board in horizontale Swimlanes aufzuteilen:

| Gruppieren nach | Lanes | Auffang-Lane |
| --- | --- | --- |
| **Keine** | Ein einzelnes flaches Board | — |
| **Epic** | Eine Lane pro Epic | *Kein Epic* |
| **Bearbeiter** | Eine Lane pro Person | *Nicht zugewiesen* |
| **Sub-Task** | Arbeitselemente mit ihren Sub-Tasks gruppieren | *Eigenständig* |

Kombiniert mit dem **Epic**-Filter erlauben dir Swimlanes, das ganze Board auf ein einzelnes Epic und seinen Baum herunterzuzoomen — eine saubere Art, ein epic-fokussiertes Standup abzuhalten.

### Der Backlog

Der **Backlog** ist schlicht jeder Vorgang im Projekt, dem **kein Sprint** zugewiesen ist, sortiert nach Priorität. Er ist dein Sammelbereich: Alles, was aufgeworfen, aber noch nicht in eine Timebox eingeplant wurde, lebt hier, bis du es in einen Sprint ziehst.

## Einen Sprint durchführen

Scrum-Boards organisieren die Arbeit in Sprints über drei Tabs — **Planung**, **Aktiver Sprint** und **Insights**. Hier ist der vollständige Zyklus Planen → Starten → Abschließen.

### 1. Planen

Wähle im Tab **Planung** die Option **Sprint erstellen**. Ein Dialog erlaubt dir zu setzen:

- **Sprint-Name** — vorausgefüllt als `Sprint 3` (die nächste Nummer), bearbeitbar.
- **Sprint-Ziel** — optional; das Ergebnis, das der Sprint liefern soll.
- **Dauer** — 1 bis 4 Wochen (Standard 2), was das Enddatum automatisch aus dem Startdatum berechnet.
- **Startdatum** — wann die Timebox beginnt.

Nach dem Erstellen des Sprints ziehst du Vorgänge aus dem **Backlog** in den Sprint-Container (oder wählst auf Touch mehrere aus und nutzt **Verschieben nach…**). Schätze jeden Vorgang mit **Story Points** über einen Planning-Poker-Dialog auf der Fibonacci-Skala. Während du planst, zeigt eine **Kapazitätsleiste** `committed / capacity pts` an und wird rot, wenn du dich übernimmst, und Punkt-Buckets zeigen, wie sich die zugesagten Punkte auf To-do, In Bearbeitung und Erledigt aufteilen.

### 2. Starten

Wenn der Umfang stimmig aussieht, drücke **Sprint starten** auf dem Sprint-Container (deaktiviert, solange der Container leer ist). Der Start-Dialog fixiert den Umfang und zeigt, was du zusagst — Anzahl der Vorgänge und zugesagte Story Points, mit einer Warnung **über Kapazität**, wenn du das Ziel überschritten hast. Bestätige Ziel und Dauer, und der Sprint wird **Aktiv**.

Der Tab **Aktiver Sprint** zeigt nun das laufende Board mit einer Sprint-Kopfzeile: ein amberfarbenes **Aktiv**-Badge, den Sprint-Namen und das Ziel sowie eine Tagesfortschrittsleiste, die `Tag 4/14` anzeigt.

### 3. Abschließen

Wenn die Timebox endet, drücke **Sprint abschließen**. Der Abschluss-Dialog überprüft das Ergebnis:

- **Abgeschlossen** — erledigte Story Points, mit einem Prozentsatz.
- **Nicht abgeschlossen** — noch offene Punkte.
- **Wohin unfertige Arbeit geht** — wähle ein Ziel für offene Vorgänge: **übertrage sie** in einen anderen geplanten Sprint oder **gib sie in den Backlog zurück**.

Bestätige, und der Sprint wird geschlossen, wobei seine unfertigen Vorgänge genau dort neu untergebracht werden, wo du es gewählt hast.

!!! tip "An Sprint-Grenzen geht nichts verloren"
    Der Abschluss eines Sprints löscht niemals Arbeit. Jeder offene Vorgang wird explizit verschoben — in den nächsten Sprint oder zurück in den Backlog — sodass dein Plan von einer Timebox zur nächsten ehrlich bleibt.

## Insights & Burndown

Der Tab **Insights** verwandelt einen Sprint in Diagramme:

- **Sprint-Burndown** — eine gestrichelte *Richtlinie* (der ideale Pfad von den zugesagten Punkten auf null) gegen eine durchgezogene *Ist*-Linie, die bis heute gezeichnet wird. Die y-Achse beginnt bei den zu Sprint-Beginn zugesagten Punkten.
- **Velocity** — zugesagte vs. erledigte Punkte, plus ein Durchschnitt über Sprints hinweg.
- **Arbeitsaufteilung nach Bearbeiter** und **Umfangsänderungen** — netto seit Sprint-Beginn hinzugefügte oder entfernte Punkte.

Für sprintübergreifende Auswertungen — Velocity-Trends, Zykluszeit, Verteilungen und PDF-Export — siehe [Berichte & Dashboard](/de/reports.html).

## Verwandte Seiten

- **[Vorgänge & Hierarchie](/de/issues.html)** — die Karten auf deinem Board und wie sie sich verschachteln.
- **[Projekteinstellungen](/de/project-settings.html)** — definiere die Workflow-Zustände, auf die deine Spalten abgebildet werden.
- **[Gantt & Zeiterfassung](/de/timeline.html)** — die Timeline-Ansicht und das Erfassen von Arbeit.
- **[Berichte & Dashboard](/de/reports.html)** — Velocity, Burndown-Historie und Exporte.
