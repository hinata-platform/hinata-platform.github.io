---
title: Boards & Sprints
description: Karten über ein Board bewegen, filtern, in Swimlanes teilen und Sprints planen und abschließen.
---

# Boards & Sprints

Ein Board zeigt die Arbeit deines Teams. Jede Spalte ist ein Schritt in eurem Prozess, jede Karte ein Vorgang. Verschiebst du eine Karte, ist der Vorgang einen Schritt weiter.

Einrichten musst du nichts. Gibt es für dein Projekt schon ein Board, öffne es und leg los.

## Ein Board öffnen

Wähle **Board** in der Seitenleiste. Du siehst alle Boards, die du sehen darfst, über alle Projekte. Das Menü oben grenzt auf ein Projekt ein. Tippe ein Board an, um es zu öffnen.

Ist die Liste leer, legst du mit **Neues Board** eines an.

![Der Dialog „Neues Board“](/assets/img/shot-board-new-dialog.png)
*Der Dialog „Neues Board“ mit Typ, „Board-Name“ und „Projekte“. „Erstellen“ bleibt grau, bis das Board einen Namen hat.*

Beim Anlegen wichtig:

- **Typ:** Kanban oder Scrum. Nachträglich umstellen kannst du das in der App nicht. Lies vorher [Kanban oder Scrum](#kanban-oder-scrum).
- **Name:** so, wie euer Team das Board nennt. Er muss nicht wie das Projekt heißen.
- **Projekte:** Wählst du mehrere, werden ihre gleichwertigen Spalten zu einer Wand zusammengefasst. Zwei Teams arbeiten dann nebeneinander, jedes in seinem Projekt.

!!! tip "Ein Projekt kann mehrere Boards haben"
    Boards sind Ansichten. Derselbe Vorgang kann auf mehreren Boards erscheinen, ohne kopiert zu werden. Vorgänge gehören zu Projekten, nicht zu Boards.

## Spalten sind eure Workflow-Status

Jede Spalte steht für einen oder mehrere **Workflowstatus** deines Projekts, etwa *To Do*, *In Arbeit*, *Im Review*, *Erledigt*. Der farbige Punkt neben dem Spaltennamen ist die Farbe des Status. Dieselbe Farbe siehst du auf der Karte, im Vorgang und in Berichten.

Verschiebst du eine Karte, bekommt der Vorgang den Status der Spalte. Alle anderen Ansichten in Hinata zeigen das sofort.

Das Abzeichen rechts in der Spaltenüberschrift zählt die Karten.

!!! note "Wer bestimmt, wie die Spalten heißen"
    Die Status liegen in den [Projekteinstellungen](/de/project-settings.html). Eine Projektleitung kann sie dort umbenennen, umfärben und umsortieren. Heißt eine Spalte unglücklich, wird das dort geändert, nicht auf dem Board.

### Was als Karte erscheint

Boards nutzen dieselbe dreistufige Hierarchie wie der Rest von Hinata (siehe [Mit Vorgängen arbeiten](/de/guide-issues.html)):

- **Stories, Tasks, Bugs und Features** sind immer Karten.
- **Epics** nie. Ein Epic enthält andere Arbeit und würde sonst doppelt zählen. Epics erscheinen als Überschrift einer Swimlane und als Filter.
- **Sub-Tasks** sind standardmäßig ausgeblendet. Gruppierst du nach Sub-Task, erscheinen sie unter ihrem Vorgang.

### Was eine Karte verrät, ohne geöffnet zu werden

Auf jeder Karte stehen Statusstreifen, Typsymbol, Vorgangsschlüssel, Prioritätspfeil, Titel, Stichwörter und der Avatar der zugewiesenen Person. Gut zu wissen:

- Das **Fälligkeitsdatum** wird rot, sobald es vorbei ist.
- Die **aufgewendete Zeit** erscheint nur, wenn der Vorgang eine Schätzung hat. Fehlt sie, hat niemand geschätzt. Gearbeitet wurde vielleicht trotzdem.
- Die **Leiste mit Sub-Tasks** unten klappt direkt auf der Karte auf. So siehst du den Fortschritt, ohne das Board zu verlassen.

## Einen Vorgang über das Board bewegen

Am Rechner ziehst du die Karte in die gewünschte Spalte. Die Zielspalte hebt sich und leuchtet bernsteinfarben. Am alten Platz bleibt eine Lücke, bis du loslässt. Ziehst du an den Bildschirmrand, scrollt die Wand mit.

Auf Handy und Tablet kannst du Karten nicht ziehen, weil Ziehen und Scrollen dieselbe Geste wären. Öffne stattdessen den Vorgang und ändere dort den Status. Das Ergebnis ist dasselbe.

Beim Verschieben ändert sich nur der Status. Zuweisung, Sprint, Termine, Story Points und alles andere bleiben. Gespeichert wird beim Loslassen, ohne Bestätigung. Die Änderung steht mit deinem Namen in der Historie des Vorgangs. Andere sehen sie, sobald ihr Board neu lädt.

### Wenn eine Spalte eine Karte ablehnt

Auf einem Board mit mehreren Projekten kann eine Spalte Status aus Projekt A und B enthalten, aber keinen aus Projekt C. Ziehst du eine Karte aus C darauf, wird die Spalte rot umrandet. Der Drop wird schon beim Ziehen abgelehnt, und eine Meldung nennt das Projekt, das hier keinen Status hat.

### Einen Vorgang genau dort anlegen, wo er hingehört

![Das Direkteingabefeld am Fuß einer Board-Spalte](/assets/img/shot-board-quick-create.png)
*„Aufgabe hinzufügen“ am Fuß der Spalte „Open“, aufgeklappt mit getipptem Titel und Chips für Typ, Fälligkeit und zugewiesene Person.*

Tippe unten in einer Spalte auf **Aufgabe hinzufügen**, gib einen Titel ein und drücke Enter. Der Vorgang entsteht im Projekt und im Status dieser Spalte.

Er übernimmt auch, worin die Spalte liegt: das Epic der Swimlane, die Person der Lane oder den Sprint des Boards. Das geht viel schneller als das vollständige Formular.

## Kanban oder Scrum

Beide Typen haben dieselben Karten, Filter und Swimlanes. Sie unterscheiden sich im Umgang mit Zeit.

| | Kanban | Scrum |
| --- | --- | --- |
| Form der Arbeit | Kontinuierlicher Fluss | Feste Zeitfenster (Sprints) |
| Ansichten | **Board** und **Timeline** | **Planung**, **Aktiver Sprint** und **Auswertung** |
| Wo Ungestartetes wartet | In der ersten Spalte | Im Backlog, im Tab „Planung“ |
| Schätzung | Optional | Story Points, pro Sprint |

Bei Kanban schaltest du neben dem Board-Namen zwischen **Board** und **Timeline** um. Timeline zeigt dieselben Vorgänge auf einem Kalender, siehe [Timeline & Abhängigkeiten](/de/guide-timeline.html).

Bei Scrum gibt es statt des Umschalters drei Tabs. Das Backlog liegt im Tab „Planung“.

## Das Board eingrenzen

Drei Bedienelemente über den Spalten machen ein volles Board übersichtlich. Sie wirken zusammen.

### Die Personenleiste

Die Avatare oben rechts sind alle, die auf diesem Board Arbeit haben.

- Klick auf einen Avatar: nur dessen Karten.
- Klick auf einen weiteren: kommt dazu.
- Nochmal klicken: wieder weg.

Das ist dieselbe Einstellung wie die Facette „Zugewiesen“ im Filter.

### Der Filter

**Filter** öffnet ein Panel mit acht Facetten:

**Status · Typ · Priorität · Zugewiesen · Sprint · Autor · Stichwort · Epic**

![Das Filter-Popup des Boards mit zwei ausgewählten Personen](/assets/img/shot-board-filter.png)
*Zwei Personen unter „Zugewiesen“ gewählt: „2 aktiv“, und die Wand zeigt nur noch ihre Karten.*

In jeder Facette kannst du suchen und mehrere Einträge wählen. Die Regel:

> Auswahlen **innerhalb** einer Facette sind ein ODER. Facetten **untereinander** sind ein UND.

Beispiel: *Bug* und *Story* unter Typ plus *Ana* unter Zugewiesen ergibt „Bugs oder Stories, die Ana zugewiesen sind“. Eine Facette ohne Auswahl filtert nicht.

Die Facette Sprint hat den Eintrag **Kein Sprint**. Damit siehst du Einträge aus dem Backlog.

!!! tip "Der Filter gehört dir, nicht dem Board"
    Filtern ändert nur, was *du* siehst. Für andere ändert sich nichts, und am Board wird nichts gespeichert.

### Swimlanes

**Gruppieren nach** teilt die Wand in waagerechte Lanes. Jede Lane hat alle Spalten.

![Das Menü „Gruppieren nach“ auf einem Board](/assets/img/shot-board-group-by.png)
*Das Menü „Gruppieren nach“. „Projekt“ erscheint nur auf einem Board mit mehreren Projekten.*

| Gruppieren nach | Du bekommst | Nimm es, wenn |
| --- | --- | --- |
| **Keine** | Ein flaches Board | Standard, weniger als ~40 Karten |
| **Epic** | Eine Lane pro Epic, dazu *Kein Epic* | Du den Fortschritt eines großen Vorhabens sehen willst |
| **Zugewiesene Person** | Eine Lane pro Person, dazu *Nicht zugewiesen* | Ihr ein Daily haltet oder die Last prüfen wollt |
| **Sub-Task** | Eine Lane pro übergeordnetem Vorgang, dessen Sub-Tasks als Karten, dazu *Eigenständig* | Mehrere große Themen parallel laufen und du Details brauchst |
| **Projekt** | Eine Lane pro Projekt | Nur auf einem Board über mehrere Projekte |

Jede Lane lässt sich einklappen.

!!! tip "Epic-Swimlanes plus Epic-Filter"
    Gruppiere nach **Epic** und filtere auf ein Epic. Dann zeigt das ganze Board nur dieses Epic. Praktisch für ein Review, ohne ein eigenes Board anzulegen.

## WIP-Limits

Eine Spalte kann ein **WIP-Limit** (Work in Progress) haben: die maximale Zahl an Karten darin. Dann zeigt das Abzeichen `3/5` statt `3`. Wird das Limit überschritten, färben sich Abzeichen und Hintergrund rot.

Hinata blockiert keine weiteren Karten. Das rote Abzeichen soll zeigen, dass sich Arbeit staut.

![Der Spalten-Editor eines Boards](/assets/img/shot-board-columns.png)
*„Board-Optionen → Spalten“: pro Spalte ein Ziehgriff, die Status als Chips, das Feld „Max.“ für das WIP-Limit und eine Schaltfläche zum Entfernen.*

Limits setzen darf, wer das Board besitzt, eines seiner Projekte leitet, ein Team mit Zugriff leitet oder Administrator ist.

## Das Backlog

Das Backlog sind **alle Vorgänge der Projekte des Boards, die in keinem Sprint sind**, sortiert nach Priorität. Ein Vorgang bleibt dort, bis ein Sprint ihn aufnimmt.

Bei Scrum findest du es unten im Tab **Planung**, seitenweise geladen und mit eigenem Suchfeld.

!!! note "Kanban hat kein Backlog"
    Ohne Zeitfenster gibt es kein „außerhalb“. Ungestartete Arbeit liegt in der ersten Spalte.

## Einen Sprint fahren

Ein Sprint ist ein festes Zeitfenster, meist ein bis vier Wochen, mit vereinbarter Arbeit. Du planst, startest, arbeitest und schließt ab, alles in den drei Tabs eines Scrum-Boards.

![Der Planungs-Tab eines Hinata-Boards](/assets/img/shot-board.png)
*Der Tab „Planung“: Sprint 24 hat 42 Story Points bei einer Kapazität von 40, der Balken ist rot.*

### 1. Den Sprint planen

Wähle im Tab **Planung** die Schaltfläche **Sprint erstellen**. Der Dialog fragt:

- **Sprint-Name:** vorbelegt mit der nächsten Nummer (*Sprint 24*, *Sprint 25* …), frei änderbar.
- **Sprint-Ziel:** optional. Ein Satz zum gewünschten Ergebnis. Er steht während des Sprints in der Kopfzeile.
- **Dauer:** eine bis vier Wochen. Das Enddatum wird aus dem Startdatum berechnet.
- **Startdatum:** vorbelegt. Beim ersten Sprint morgen, danach kurz nach dem Ende des vorherigen Sprints.

Der neue Sprint erscheint als leerer Container über dem Backlog.

### 2. Ihn aus dem Backlog füllen

Zieh Vorgänge aus dem Backlog in den Sprint. Auf dem Handy hakst du die Kreise der Zeilen an. Unten erscheint dann eine Leiste mit der Anzahl und **Verschieben nach…**.

So verschiebst du Vorgänge auch zwischen geplanten Sprints.

### 3. Mit Story Points schätzen

Tippe in einer Zeile des Sprints auf den Punktebereich. Der Schätzdialog öffnet sich.

![Der Schätzdialog](/assets/img/shot-board-estimate.png)
*„Schätzen“ für HIN-4: Werte 1, 2, 3, 5, 8, 13, 21, die letzte Karte (ein Strich) löscht die Schätzung.*

Schlüssel und Titel oben im Dialog zeigen, welchen Vorgang du gerade schätzt.

Story Points messen relativen Aufwand, keine Stunden. Eine 5 ist spürbar größer als eine 3 und etwa halb so groß wie eine 13. Wichtig ist die Summe. Die Kopfzeile des Sprints zeigt sie zweimal:

- **Punktetöpfe:** drei Pillen für offen, in Arbeit und erledigt.
- **Kapazität:** committete Punkte gegen die Kapazität des Teams, etwa `42 / 40 pts`, mit Balken. Bei Überschreitung wird beides rot.

!!! note "Kapazität ist optional"
    Ohne Kapazitätswert siehst du nur die committeten Punkte, ohne Balken. Die Kapazität wird über die API oder ein Werkzeug für Admins gesetzt, nicht im Dialog zum Erstellen.

### 4. Ihn starten

Drück **Sprint starten** am Sprint. Solange der Sprint leer ist, bleibt die Schaltfläche deaktiviert.

Der Dialog zeigt Anzahl der Vorgänge, committete Story Points und eine Warnung, falls die Kapazität überschritten ist. Bestätige Ziel und Enddatum. Der Sprint ist dann **Aktiv**.

Alle Mitglieder der Projekte des Boards werden benachrichtigt.

### 5. Ihn durcharbeiten

Der Tab **Aktiver Sprint** ist eine normale Wand, begrenzt auf den Sprint. Ziehen, Filter und Swimlanes funktionieren wie gewohnt.

Die Kopfzeile zeigt das bernsteinfarbene Abzeichen **Aktiv**, Name und Ziel des Sprints und einen Tageszähler wie `Tag 8/15` mit Fortschrittsbalken. So merkst du früh, wenn noch viele Punkte offen sind.

### 6. Ihn abschließen

Drück **Sprint abschließen**, wenn das Zeitfenster endet.

![Der Dialog „Sprint abschließen“](/assets/img/shot-board-complete-sprint.png)
*„Sprint 24 abschließen“: fünf erledigte, zwölf offene Vorgänge und darunter das Ziel für die offenen, etwa __Sprint 25__ oder „Backlog“.*

Im Dialog wählst du, wohin offene Vorgänge gehen. Zur Wahl stehen alle geplanten Sprints und darunter „Backlog“. Gibt es keinen geplanten Sprint, bleibt nur „Backlog“.

Nach dem Bestätigen:

- Der Sprint wird archiviert.
- Erledigte Arbeit bleibt ihm zugerechnet. Historie und Zahlen stimmen also.
- Jeder offene Vorgang wandert zum gewählten Ziel. Der Sprintwechsel steht in seiner Historie, und seine Beobachter werden benachrichtigt.

!!! warning "Ein Sprintabschluss verschiebt die Arbeit anderer Leute"
    Offene Vorgänge wechseln wirklich den Sprint. Beobachter werden informiert, und der Wechsel steht in der Historie. Entscheide bewusst und sag dem Team Bescheid.

!!! tip "An einer Sprintgrenze geht nie etwas verloren"
    Du kannst keinen Sprint abschließen, ohne jedem offenen Vorgang ein neues Ziel zu geben.

## Die Zahlen des Sprints lesen

Der Tab **Auswertung** zeigt vier Diagramme:

- **Sprint-Burndown:** eine gestrichelte *Richtlinie* von den committeten Punkten bis null und eine durchgezogene *Ist*-Linie bis heute.
- **Velocity:** committete und erledigte Punkte für diesen und frühere Sprints, mit Durchschnitt.
- **Arbeitsverteilung nach Bearbeiter:** wo der geschätzte Aufwand liegt.
- **Umfangsänderungen:** Punkte, die seit Sprintstart netto dazukamen oder wegfielen.

Trends über viele Sprints, Durchlaufzeit und Exporte findest du unter [Berichte & Dashboard](/de/guide-reports.html).

## Auf dem Handy

Alles funktioniert auch auf dem Handy, nur kompakter.

![Der Planungs-Tab eines Hinata-Boards auf dem Handy](/assets/img/shot-mobile-board.png)
*Der Tab „Planung“ auf dem Handy: Umschalter und Filter als Symbole, die Kopfzeile des Sprints untereinander gestapelt.*

Die Unterschiede:

- Der Umschalter Board/Timeline, die Tabs Planung/Aktiver Sprint/Auswertung und **Filter** sind reine Symbolschaltflächen.
- Karten lassen sich nicht ziehen. Den Status änderst du im Vorgang. In einen Sprint verschiebst du Vorgänge, indem du sie auswählst und **Verschieben nach…** nutzt.
- Die Wand scrollt seitwärts Spalte für Spalte, sodass immer eine Spalte sauber im Bild steht.

Mehr unter [Auf dem Handy](/de/guide-mobile.html).

## Das Board pflegen

Die Schaltfläche **⋮** an jedem Board in der Liste öffnet die **Board-Optionen**. Du findest sie auch auf der Boards-Seite eines Projekts.

- **Board umbenennen:** nur der Name ändert sich.
- **Projekte:** festlegen, welche Projekte das Board umfasst. Gleichwertige Status werden automatisch zu gemeinsamen Spalten.
- **Spalten:** der Editor [von oben](#wip-limits). Nennen zwei Projekte denselben Schritt unterschiedlich, korrigierst du die Zuordnung hier.
- **Board löschen:** entfernt das Board. Die Vorgänge bleiben, denn sie gehören zu ihren Projekten.

Dafür musst du das Board besitzen, eines seiner Projekte leiten, ein Team mit Zugriff leiten oder Administrator sein. Siehst du das Menü nicht, hast du keine dieser Rollen.

!!! warning "Jeder Status braucht eine Spalte"
    Jeder Workflowstatus muss in genau einer Spalte liegen. Ein Status ohne Spalte heißt: Seine Vorgänge fehlen auf der Wand. Der Editor warnt dich davor, bevor du speicherst.

## Wie es weitergeht

- **[Mit Vorgängen arbeiten](/de/guide-issues.html):** was auf den Karten steht und wie Epics, Stories und Sub-Tasks zusammenhängen.
- **[Timeline & Abhängigkeiten](/de/guide-timeline.html):** dieselbe Arbeit auf einem Kalender, mit Verknüpfungen.
- **[Zeit erfassen](/de/guide-time.html):** Aufwand auf Vorgänge buchen.
- **[Berichte & Dashboard](/de/guide-reports.html):** Velocity, Durchlaufzeit und Zahlen über mehrere Sprints.
