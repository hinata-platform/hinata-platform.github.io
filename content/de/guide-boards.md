---
title: Boards & Sprints
description: Arbeit über ein Board bewegen, auf das Wesentliche filtern, in Swimlanes aufteilen und einen Sprint von der Planung bis zum Abschluss führen.
---

# Boards & Sprints

Ein Board ist die Arbeit deines Teams, sichtbar ausgelegt. Jede Spalte ist ein Schritt in eurem Prozess, jede Karte ein Vorgang — und eine Karte zu verschieben heißt: „Das hier ist weiter.“ Alles andere auf dieser Seite — Filter, Swimlanes, Limits, Sprints — sorgt dafür, dass dieses eine Bild auch mit achtzig Karten noch lesbar bleibt statt nur mit acht.

Du musst vorher nichts einrichten. Wenn für dein Projekt schon ein Board existiert, öffne es und fang an, Karten zu bewegen.

## Ein Board öffnen

Wähle **Board** in der Seitenleiste. Du siehst eine Liste aller Boards, die du sehen darfst, über alle Projekte hinweg; ein Menü oben grenzt sie auf ein Projekt ein. Tippe ein Board an, um es zu öffnen.

Ist die Liste leer, legst du mit **Neues Board** eines an. Drei Dinge werden gefragt:

- **Board-Typ** — **Kanban** oder **Scrum**. In der App gibt es kein Bedienelement, um den Typ eines Boards nachträglich zu wechseln — hier lohnt also ein kurzer Moment: siehe [Kanban oder Scrum](#kanban-oder-scrum) weiter unten.
- **Board-Name** — wie euer Team das Board nennt, nicht wie das Projekt heißt.
- **Projekte** — eines oder mehrere. Ein Board über mehrere Projekte fasst gleichwertige Spalten zu einer Wand zusammen, sodass zwei Teams nebeneinander arbeiten können, ohne ihr eigenes Projekt zu verlassen.

!!! tip "Ein Projekt kann mehrere Boards haben"
    Boards sind Ansichten, keine Behälter. Derselbe Vorgang kann auf einem Team-Board, einem Release-Board und einem persönlichen Board auftauchen, ohne kopiert zu werden. Nichts gehört *zu* einem Board — Vorgänge gehören zu Projekten.

## Spalten sind eure Workflow-Status

Die Spalten, die du siehst, sind nicht allgemein. Jede bildet einen oder mehrere **Workflow-Status** deines Projekts ab — die benannten Schritte, die ein Vorgang durchläuft, etwa *To Do*, *In Arbeit*, *Im Review*, *Erledigt*. Der farbige Punkt neben dem Spaltennamen ist die Farbe dieses Status, und es ist dieselbe Farbe auf der Karte, im Vorgang und in den Berichten.

Genau deshalb ist das Verschieben einer Karte eine echte Änderung und kein Aufräumen: Die Karte landet im Status der Spalte, und jede andere Ansicht in Hinata ist sofort derselben Meinung.

Das Abzeichen rechts in der Spaltenüberschrift zählt die Karten darin.

!!! note "Wer bestimmt, wie die Spalten heißen"
    Die Status selbst liegen in den Projekteinstellungen, und eine Projektleitung kann sie umbenennen, umfärben und umsortieren. Die Doku dazu steht unter [Projekteinstellungen](/de/project-settings.html). Wenn eine Spalte auf deinem Board unglücklich heißt, wird das dort behoben — nicht auf dem Board.

### Was als Karte erscheint — und was nicht

Boards nutzen dieselbe dreistufige Hierarchie wie der Rest von Hinata — siehe [Mit Vorgängen arbeiten](/de/guide-issues.html):

- **Stories, Tasks, Bugs und Features** sind immer Karten.
- **Epics** nie. Ein Epic ist ein Behälter für andere Arbeit; als Karte auf der Wand würde es doppelt zählen. Epics erscheinen stattdessen als Swimlane-Überschrift und als Filter.
- **Sub-Tasks** sind standardmäßig ausgeblendet, weil sie zu ihrem übergeordneten Vorgang gehören. Gruppierst du das Board nach Sub-Task, erscheinen sie darunter.

### Was eine Karte verrät, ohne geöffnet zu werden

Eine Karte ist bewusst dicht — sie soll aus drei Metern Entfernung die Frage „muss ich das anklicken?“ beantworten:

- Ein **farbiger Streifen** oben, in der Statusfarbe des Vorgangs.
- Das **Typ-Symbol** und der **Vorgangsschlüssel** (`HIN-42`) in der ersten Zeile, rechts der **Prioritätspfeil**.
- Der **Titel**, bis zu drei Zeilen.
- Bis zu drei **Stichwörter**, in ihren eigenen Farben.
- Die bisher **aufgewendete Zeit**, falls der Vorgang eine Schätzung trägt; das **Fälligkeitsdatum**, das rot wird, sobald es vorbei ist; und der **Avatar der zugewiesenen Person**.
- Hat der Vorgang Sub-Tasks, findest du unten eine Leiste, die du aufklappen kannst — inklusive Fortschritt, ohne das Board zu verlassen.

## Einen Vorgang über das Board bewegen

Am Rechner **ziehst du die Karte** in die gewünschte Spalte. Die Zielspalte hebt sich an und leuchtet bernsteinfarben, während du darüber schwebst, die Karte hinterlässt eine Lücke an ihrem alten Platz und setzt sich beim Loslassen an ihrem neuen Ort ab. Ziehst du an den Bildschirmrand, scrollt die Wand mit — eine Spalte, die gerade nicht sichtbar ist, bleibt also mitten im Ziehen erreichbar.

Auf Handy und Tablet lassen sich Karten **nicht** ziehen — mit dem Finger sind Kartendrag und Board-Scrollen dieselbe Geste, und eine von beiden muss gewinnen. Tippe stattdessen die Karte an, öffne den Vorgang und ändere den Status dort. Das Ergebnis ist identisch.

Ein Verschieben ändert genau eine Sache: den Status des Vorgangs. Zuweisung, Sprint, Termine, Story Points und alles andere bleiben, wie sie waren. Gespeichert wird im Moment des Loslassens — es gibt keinen Bestätigungsschritt und nichts nachträglich zu sichern — und die Änderung landet mit deinem Namen in der Historie des Vorgangs. Alle anderen bekommen sie mit, sobald ihr Board das nächste Mal lädt.

### Wenn eine Spalte eine Karte ablehnt

Auf einem Board über mehrere Projekte kann eine Spalte einen Status aus Projekt A und einen aus Projekt B halten — aber nicht zwingend einen aus Projekt C. Ziehst du eine C-Karte darauf, umrandet sich die Spalte rot statt bernsteinfarben, der Drop wird abgelehnt, solange die Karte noch in der Luft ist, und eine Meldung nennt dir das Projekt, das hier keinen Status hat.

Das ist Absicht. Die Alternative wäre, den Drop anzunehmen und dann zu scheitern — und dich rätseln zu lassen, was du falsch gemacht hast. Eine Ablehnung, die du mitten im Ziehen siehst, ist eine, auf die du reagieren kannst.

### Einen Vorgang genau dort anlegen, wo er hingehört

Am Fuß jeder Spalte sitzt ein Direkteingabefeld — **Aufgabe hinzufügen**. Titel tippen, Enter drücken, fertig: Der Vorgang entsteht bereits im Projekt und im Status dieser Spalte. Steht die Spalte in einer Epic-Swimlane, erbt er das Epic; in einer Personen-Lane die Person; auf einem Sprint-Board den Sprint.

Das ist deutlich schneller als das vollständige Formular — und es sorgt dafür, dass ein Gedanke aus dem Daily auch im Daily notiert wird.

## Kanban oder Scrum

Beide Board-Typen teilen dieselben Karten, dieselben Filter und dieselben Swimlanes. Sie unterscheiden sich darin, wie sie mit Zeit umgehen.

| | Kanban | Scrum |
| --- | --- | --- |
| Form der Arbeit | Kontinuierlicher Fluss | Feste Zeitfenster (Sprints) |
| Ansichten | **Board** und **Timeline** | **Planung**, **Aktiver Sprint** und **Auswertung** |
| Wo Ungestartetes wartet | In der ersten Spalte | Im Backlog, im Tab „Planung“ |
| Schätzung | Optional | Story Points, pro Sprint |

Auf einem **Kanban**-Board bietet der Umschalter neben dem Board-Namen **Board** und **Timeline** an. Board ist die Wand, die du schon kennst; Timeline legt dieselben Vorgänge auf einen Kalender — siehe [Timeline & Abhängigkeiten](/de/guide-timeline.html).

Auf einem **Scrum**-Board ersetzen die drei Tabs diesen Umschalter vollständig, und das Backlog liegt im Tab „Planung“ statt in einer eigenen Ansicht. Der Rest dieser Seite führt dich hindurch.

## Das Board eingrenzen

Ein Board mit zweihundert Karten ist eine Wand, kein Bild. Drei Bedienelemente über den Spalten schneiden es zurecht, und sie greifen ineinander.

### Die Personenleiste

Die überlappenden Avatare oben rechts sind alle, die auf diesem Board Arbeit haben. Klick auf einen, um nur dessen Karten zu sehen; klick auf einen zweiten, um ihn hinzuzunehmen; noch ein Klick entfernt ihn wieder. Ausgewählte Avatare bleiben hell, die übrigen werden blass — du siehst also immer auf einen Blick, ob ein Filter aktiv ist.

Das ist dieselbe Einstellung wie die Facette „Zugewiesen“ im Filter-Popup — die Leiste ist schlicht die Abkürzung für das, wonach am häufigsten gefiltert wird.

### Das Filter-Popup

**Filter** öffnet ein Glaspanel mit acht Facetten:

**Status · Typ · Priorität · Zugewiesen · Sprint · Autor · Stichwort · Epic**

Jede Facette ist eine durchsuchbare Mehrfachauswahl. Wie sie zusammenwirken, lohnt sich zu merken — genau das macht den Filter brauchbar statt fummelig:

> Auswahlen **innerhalb** einer Facette sind ein ODER. Facetten **untereinander** sind ein UND.

*Bug* und *Story* unter Typ, dazu *Ana* unter Zugewiesen, ergibt also „Bugs oder Stories, die Ana zugewiesen sind“. Nichts in einer Facette auszuwählen heißt: Diese Facette filtert gar nicht.

Die Sprint-Facette enthält den Eintrag **Kein Sprint** — so siehst du Backlog-Einträge zwischen dem Rest. Die Schaltfläche trägt ein bernsteinfarbenes Abzeichen mit der Zahl der aktiven Kriterien, und **Zurücksetzen** räumt mit einem Klick alles ab.

!!! tip "Der Filter gehört dir, nicht dem Board"
    Filtern ändert, was *du* siehst. Es verschiebt, versteckt oder verändert für niemanden sonst etwas und wird auch nicht am Board gespeichert — filtere also unbesorgt.

### Swimlanes

**Gruppieren nach** teilt die Wand in waagerechte Lanes, von denen jede den vollständigen Spaltensatz trägt. Es ist das wirksamste Mittel, ein volles Board lesbar zu machen — welche Gruppierung hilft, hängt an deiner Frage.

| Gruppieren nach | Du bekommst | Nimm es, wenn |
| --- | --- | --- |
| **Keine** | Ein flaches Board | Standard — weniger als ~40 Karten |
| **Epic** | Eine Lane pro Epic, dazu *Kein Epic* | Du sehen willst, wie ein großes Vorhaben als Ganzes vorankommt |
| **Zugewiesene Person** | Eine Lane pro Person, dazu *Nicht zugewiesen* | Ihr ein Daily haltet oder prüfen wollt, ob die Last fair verteilt ist |
| **Sub-Task** | Eine Lane pro übergeordnetem Vorgang, dessen Sub-Tasks als Karten, dazu *Eigenständig* | Ein paar große Themen parallel laufen und du das Klein-Klein brauchst |
| **Projekt** | Eine Lane pro Projekt | Nur auf einem Board über mehrere Projekte |

Jede Lane lässt sich einklappen — du kannst also die vier Epics wegfalten, über die ihr gerade nicht sprecht, und das fünfte offen lassen.

!!! tip "Epic-Swimlanes plus Epic-Filter"
    Gruppiere nach **Epic** und filtere dann auf ein einzelnes Epic: Das ganze Board wird zum Board dieses einen Epics — Spalten, Karten und alles. Das ist der sauberste Weg für ein fokussiertes Review, ohne dafür ein eigenes Board anzulegen.

## WIP-Limits

Eine Spalte kann ein **WIP-Limit** tragen (Work in Progress): die größte Zahl an Karten, die gleichzeitig darin liegen sollte. Ist eines gesetzt, liest sich das Zählabzeichen als `3/5` statt `3`. Wird es überschritten, färben sich Abzeichen und Hintergrund rot.

Hinata hindert dich nicht daran, ein WIP-Limit zu überschreiten — mit Absicht. Das Limit ist ein Gesprächsanlass, kein Schloss: Der Sinn eines roten Abzeichens in *Im Review* ist, dass jemand bemerkt, dass nichts reviewt wird, nicht dass die siebte Karte an der Tür abgewiesen wird.

Limits werden je Spalte unter **Board-Optionen → Spalten** gesetzt, zusammen mit dem Spaltennamen und den enthaltenen Status. Dafür musst du das Board besitzen, eines seiner Projekte leiten, ein Team mit Zugriff leiten oder Administrator sein.

## Das Backlog

Das Backlog ist einfacher, als es klingt: Es sind **alle Vorgänge der Board-Projekte, die in keinem Sprint sind**, nach Priorität sortiert. Nichts legt einen Vorgang dort ab — ein Vorgang ist genau so lange im Backlog, wie kein Sprint ihn beansprucht.

Dort warten Ideen. Ein Bug, der dienstags gemeldet wird, liegt im Backlog, bis eine Sprint-Planung entscheidet, ob er in die nächsten zwei Wochen gehört. Auf einem Scrum-Board findest du ihn unten im Tab **Planung**, seitenweise, mit eigenem Suchfeld.

!!! note "Kanban-Boards haben kein Backlog-Tab"
    Ein Flussboard hat keine Zeitfenster, außerhalb derer man sein könnte — das Konzept greift dort nicht. Ungestartete Arbeit liegt schlicht in der ersten Spalte.

## Einen Sprint fahren

Ein Sprint ist ein festes Zeitfenster — meist ein bis vier Wochen — mit einem vereinbarten Arbeitsumfang. Hinata bildet den ganzen Zyklus ab: planen, starten, durcharbeiten, abschließen. Alles passiert in den drei Tabs eines Scrum-Boards.

![Der Planungs-Tab eines Hinata-Boards](/assets/img/shot-board.png)
*Der Tab „Planung“: Sprint 24 ist aktiv, läuft vom 18. Juli bis 1. August, und sein Kapazitätsbalken ist rot — 44 committete Story Points gegen eine Kapazität von 40. Jede Zeile zeigt Typ, Schlüssel, Titel, Priorität, Story Points und zugewiesene Person.*

### 1. Den Sprint planen

Wähle im Tab **Planung** die Schaltfläche **Sprint erstellen**. Der Dialog fragt nach:

- **Sprint-Name** — vorbelegt mit der nächsten Nummer (*Sprint 24*, *Sprint 25* …), frei änderbar.
- **Sprint-Ziel** — optional, und es lohnt sich. Ein Satz zum Ergebnis, das der Sprint liefern soll; er steht dann zwei Wochen lang in der Sprint-Kopfzeile und erinnert alle daran, worauf ihr euch geeinigt habt.
- **Dauer** — eine bis vier Wochen. Das Enddatum ergibt sich automatisch aus dem Startdatum.
- **Startdatum** — wann das Zeitfenster beginnt. Es ist vorbelegt: morgen beim ersten Sprint, danach kurz nach dem Enddatum des vorherigen Sprints.

Der neue Sprint erscheint als leerer Container über dem Backlog.

### 2. Ihn aus dem Backlog füllen

Zieh Vorgänge aus dem Backlog in den Sprint-Container. Auf dem Handy hakst du stattdessen die Kreise der gewünschten Zeilen an — unten erscheint eine Leiste mit der Anzahl und der Aktion **Verschieben nach…**.

Auf demselben Weg verschiebst du Vorgänge auch *zwischen* geplanten Sprints — so wird aus „das ist eigentlich ein Nächster-Sprint-Problem“ eine Handlung statt einer Diskussion.

### 3. Mit Story Points schätzen

Tippe auf einer Sprint-Zeile den Punktebereich an, um den Schätzdialog zu öffnen. Es ist ein Planning-Poker-Kartenraster auf der Fibonacci-Skala — **1, 2, 3, 5, 8, 13, 21** — plus einer Möglichkeit, die Schätzung wieder zu löschen.

Story Points messen relativen Aufwand, keine Stunden. Eine 5 ist spürbar größer als eine 3 und ungefähr halb so groß wie eine 13; mehr ist nicht vereinbart. Ihr Wert liegt in der Summe — und dafür gibt es die zwei Anzeigen in der Sprint-Kopfzeile:

- **Punkte-Töpfe** — drei Pillen, die zeigen, wie sich die committeten Punkte auf offen, in Arbeit und erledigt verteilen. Während des Sprints willst du zusehen, wie der grüne wächst.
- **Kapazität** — committete Punkte gegen die Kapazität des Teams, als `44 / 40 pts` mit Balken darunter. Bei Überschreitung werden beide rot, wie im Screenshot oben.

!!! note "Kapazität ist optional"
    Ein Sprint ohne Kapazitätswert zeigt seine committeten Punkte allein, ohne Balken — ein Balken, der immer voll ist, sagt nichts. Die Kapazität wird über die API oder ein Admin-Werkzeug gesetzt, nicht im Erstellen-Dialog. Nutzt dein Team sie nicht, siehst du sie einfach nicht.

### 4. Ihn starten

Sieht der Umfang gut aus, drück **Sprint starten** am Sprint-Container. Die Schaltfläche bleibt deaktiviert, solange der Sprint leer ist — da gibt es nichts zu starten.

Der Dialog zeigt, worauf du dich festlegst: Anzahl der Vorgänge, committete Story Points und eine Warnung, falls das über der Kapazität liegt. Bestätige Ziel und Enddatum, und der Sprint ist **Aktiv**.

Ein Sprintstart benachrichtigt alle Mitglieder der Board-Projekte — niemand muss also gesondert erfahren, dass das Zeitfenster begonnen hat.

### 5. Ihn durcharbeiten

Der Tab **Aktiver Sprint** ist eine ganz normale Board-Wand, begrenzt auf den Sprint. Gleiches Ziehen, gleiche Filter, gleiche Swimlanes — dazu eine Glas-Kopfzeile mit bernsteinfarbenem **Aktiv**-Abzeichen, Sprint-Name und -Ziel sowie einem Tageszähler `Tag 4/14` mit Fortschrittsbalken.

Dieser Zähler ist still das Nützlichste am Tab. „Wir sind an Tag 11 von 14, und die Hälfte der Punkte ist noch offen“ ist ein Gespräch, das du an Tag 11 führen willst, nicht an Tag 14.

### 6. Ihn abschließen

Drück **Sprint abschließen**, wenn das Zeitfenster endet. Der Dialog bilanziert:

- **Abgeschlossen** — wie viele Vorgänge fertig wurden, wie viele Punkte das waren, und der Prozentsatz.
- **Nicht abgeschlossen** — wie viele Vorgänge und Punkte noch offen sind.
- **Wohin die offene Arbeit geht** — wähle einen anderen geplanten Sprint, in den sie übernommen wird, oder **Backlog**, um sie zurück in den Pool zu geben.

Bestätige, und drei Dinge passieren. Der Sprint wird archiviert. Fertige Arbeit bleibt ihm zugerechnet, damit Historie und Zahlen ehrlich bleiben. Jeder offene Vorgang wandert an das gewählte Ziel, wird in seiner Historie als Sprint-Wechsel festgehalten, und seine Beobachter werden benachrichtigt.

!!! warning "Ein Sprintabschluss verschiebt die Arbeit anderer Leute"
    Offene Vorgänge wechseln wirklich den Sprint — das ist kein Etikett. Wer einen davon beobachtet, wird informiert, und der Wechsel steht in der Historie des Vorgangs. Triff die Wahl bewusst und sag dem Team, wie du entschieden hast.

!!! tip "An einer Sprintgrenze geht nie etwas verloren"
    Es gibt keine Möglichkeit, einen Sprint abzuschließen und offene Vorgänge darin stranden zu lassen. Jeder einzelne bekommt ausdrücklich ein neues Zuhause — genau das erspart der nächsten Planung eine archäologische Ausgrabung.

## Die Zahlen des Sprints lesen

Der Tab **Auswertung** macht aus dem laufenden Sprint vier Diagramme:

- **Sprint-Burndown** — eine gestrichelte *Richtlinie* von den committeten Punkten hinunter auf null, dagegen eine durchgezogene *Ist*-Linie bis heute. Der Abstand zwischen beiden ist die Geschichte.
- **Velocity** — committete gegen erledigte Punkte für diesen und frühere Sprints, mit Durchschnitt.
- **Arbeitsverteilung nach Bearbeiter** — wo der geschätzte Aufwand liegt.
- **Umfangsänderungen** — die Netto-Punkte, die seit Sprintstart dazugekommen oder weggefallen sind. So wird aus „wir haben ständig etwas nachgeschoben“ ein Gefühl weniger und eine Zahl mehr.

Für Trends über viele Sprints, Durchlaufzeit und Exporte geht es weiter zu [Berichte & Dashboard](/de/guide-reports.html).

## Auf dem Handy

Alles oben Beschriebene funktioniert auf dem Handy; das Layout faltet sich nur zusammen.

![Ein Hinata-Sprint-Board auf dem Handy](/assets/img/shot-mobile-board.png)
*Derselbe Tab „Planung“ auf dem Handy: Ansichtsumschalter und Filter schrumpfen zu Symbolen, die Sprint-Kopfzeile stapelt Vorgangszahl, Punkte-Töpfe und Kapazitätsbalken untereinander, und „Sprint abschließen“ nimmt die volle Breite ein.*

Die Unterschiede, die du kennen solltest:

- Der Umschalter Board/Timeline und die Tabs Planung/Aktiver Sprint/Auswertung werden zu reinen Symbolschaltflächen — genau wie **Filter**.
- Karten lassen sich nicht ziehen. Einen Status änderst du, indem du den Vorgang öffnest; in einen Sprint verschiebst du Vorgänge, indem du sie auswählst und **Verschieben nach…** nutzt.
- Die Board-Wand scrollt seitwärts spaltenweise, sodass eine Spalte immer sauber im Bild landet.

Mehr zum Arbeiten auf kleinen Bildschirmen steht unter [Auf dem Handy](/de/guide-mobile.html).

## Das Board pflegen

Jedes Board in der Board-Liste trägt eine **⋮**-Schaltfläche — das sind die **Board-Optionen**, ebenso auf der Boards-Seite eines Projekts. Dahinter liegen die Verwaltungsaktionen:

- **Board umbenennen** — neuer Name, sonst ändert sich nichts.
- **Projekte** — ändern, welche Projekte das Board umfasst. Gleichwertige Status der gewählten Projekte werden automatisch zu gemeinsamen Spalten zusammengefasst.
- **Spalten** — Spalten von Hand benennen, festlegen, welcher Status in welche gehört, sie umsortieren und WIP-Limits setzen. Die automatische Zusammenführung rät gut, aber zwei Projekte können denselben Schritt unterschiedlich nennen; hier korrigierst du das.
- **Board löschen** — entfernt das Board. Die Vorgänge darauf bleiben unangetastet: Sie gehören ihren Projekten, nicht dem Board.

Dafür musst du das Board besitzen, eines seiner Projekte leiten, ein Team mit Zugriff leiten oder Administrator sein. Siehst du das Menü nicht, bist du in keiner dieser Rollen — das ist normal und nichts, was du selbst reparieren müsstest.

!!! warning "Jeder Status braucht eine Spalte"
    Bearbeitest du Spalten von Hand, achte darauf, dass jeder Workflow-Status in genau einer landet. Ein Status ohne Spalte bedeutet, dass seine Vorgänge stillschweigend nicht auf der Wand erscheinen. Der Editor warnt dich davor, bevor er speichern lässt.

## Wie es weitergeht

- **[Mit Vorgängen arbeiten](/de/guide-issues.html)** — was auf den Karten steht und wie Epics, Stories und Sub-Tasks zusammenhängen.
- **[Timeline & Abhängigkeiten](/de/guide-timeline.html)** — dieselbe Arbeit auf einem Kalender, samt der Verknüpfungen dazwischen.
- **[Zeit erfassen](/de/guide-time.html)** — Aufwand auf die Vorgänge buchen, die du bewegst.
- **[Berichte & Dashboard](/de/guide-reports.html)** — Velocity, Durchlaufzeit und die Zahlen hinter mehreren Sprints.
