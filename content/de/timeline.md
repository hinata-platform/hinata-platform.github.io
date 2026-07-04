---
title: Gantt & Zeiterfassung
description: Sieh deinen Plan auf einer Gantt-Timeline mit Abhängigkeiten und Fortschritt und erfasse den tatsächlichen Aufwand mit aktivitätstypisierten Arbeitseinträgen und wöchentlichen Timesheets.
---

# Gantt & Zeiterfassung

Zwei Funktionen beantworten die beiden Fragen, die sich jedes Team stellt: *Wann ist es fertig?* und *Wohin ist die Zeit geflossen?* Die **Gantt-Timeline** verwandelt Start- und Fälligkeitsdaten in einen visuellen Plan; die **Zeiterfassung** hält den tatsächlich aufgewendeten Aufwand fest und speist die [Berichte](/de/reports.html).


![Hinata Gantt-Timeline](/assets/img/shot-gantt.png)
*Die Gantt-Timeline — Start-/Fälligkeitsdaten, Abhängigkeiten und Fortschritt im Plan.*

## Die Gantt-/Timeline-Ansicht

Die Timeline ist ein aus deinen Vorgängen aufgebautes Lesemodell. Jeder Vorgang mit Daten erscheint als Balken, der von seinem **Startdatum** bis zu seinem **Fälligkeitsdatum** reicht, auf einem Kalender positioniert, sodass du Überschneidungen, Lücken und den kritischen Pfad auf einen Blick erkennst.

- **Abhängigkeiten** — Verknüpfungen zwischen Vorgängen werden als Verbinder gezeichnet, sodass ein Verzug stromaufwärts sichtbar alles stromabwärts nach hinten schiebt.
- **Fortschritt** — jeder Balken spiegelt wider, wie weit sein Vorgang fortgeschritten ist, und gibt so sofort Auskunft darüber, ob der Plan im Zeitrahmen liegt.
- **Gruppierung** — die Arbeit ist so organisiert, dass du einem Projekt, einem Epic oder einer zugewiesenen Person entlang der Timeline folgen kannst.

!!! info "Daten treiben die Timeline"
    Ein Balken erscheint erst, wenn ein Vorgang ein **Start-** und/oder **Fälligkeitsdatum** hat. Setze sie in der Vorgangs-Detailansicht (siehe [Vorgänge](/de/issues.html)); die Timeline aktualisiert sich sofort.

!!! tip "Plane auf dem Board, verifiziere auf der Timeline"
    Nutze das [Board](/de/boards-sprints.html), um zu organisieren, *was* in einem Sprint ist, und die Timeline, um zu prüfen, *wann* alles passieren muss und ob die Abhängigkeiten zusammenpassen.

## Zeiterfassung

Wo es bei der Timeline um den Plan geht, geht es bei der Zeiterfassung um die Realität. Jeder, der an einem Vorgang arbeitet, kann den aufgewendeten Aufwand erfassen.

### Arbeit erfassen

Öffne einen Vorgang und wähle **Zeit erfassen**. Ein Arbeitseintrag erfasst:

- **Dauer** — Stunden und Minuten.
- **Aktivitätstyp** — einer von **Development, Testing, Documentation, Design, Meeting** oder **Support**, sodass der Aufwand nach Art der Arbeit analysiert werden kann.
- **Datum** — wann die Arbeit stattfand (jeder Tag bis heute).
- **Notiz** — eine optionale Beschreibung dessen, was du getan hast.

Jeder Vorgang zeigt **aufgewendet vs. Schätzung**, sodass offensichtlich ist, wenn etwas den Rahmen sprengt.

!!! tip "Zeit direkt aus einem Commit erfassen"
    Mit aktivierter [Git-Integration](/de/git-integration.html) erfasst ein Smart-Commit-Trailer Arbeit, ohne dass du deinen Editor verlässt: `MOB-42 #time 2h 30m` fügt `MOB-42` einen 2½-stündigen Arbeitseintrag hinzu.

### Wöchentliche Timesheets

Arbeitseinträge werden zu einem **wöchentlichen Timesheet** zusammengefasst — ein Raster pro Person und pro Tag mit erfasstem Aufwand nach Aktivität. Es ist der schnelle Weg, eine Woche zu überprüfen, Lücken zu erkennen und Zeit ohne Tabellenkalkulationen zu melden.

## Wohin die Zahlen fließen

Erfasste Zeit und Schätzungen treiben die Liefermetriken: Kapazitätsplanung bei [Sprints](/de/boards-sprints.html) sowie Zykluszeit- und Aufwandsanalyse in den [Berichten](/de/reports.html).

## Nächste Schritte

- Setze Daten und Abhängigkeiten an deinen [Vorgängen](/de/issues.html).
- Lies die Liefermetriken in [Berichte & Dashboard](/de/reports.html).
- Automatisiere die Zeiterfassung mit [Smart Commits](/de/git-integration.html).
