---
title: Gantt & Zeiterfassung
description: Der Plan als Timeline mit Abhängigkeiten und Fortschritt, dazu Zeiterfassung mit Tätigkeitsarten und Stundenzettel.
---

# Gantt & Zeiterfassung

Zwei Funktionen beantworten zwei Fragen: *Wann ist es fertig?* und *Wohin ist die Zeit geflossen?*

- Die **Timeline** (Gantt) macht aus Start- und Fälligkeitsdaten einen Plan.
- Die **Zeiterfassung** hält den tatsächlichen Aufwand fest und liefert die Zahlen für die [Berichte](/de/reports.html).

![Hinata Gantt-Timeline](/assets/img/shot-gantt.png)
*Die Timeline mit Daten, Abhängigkeiten und Fortschritt.*

## Die Timeline

Die Timeline wird aus deinen Vorgängen aufgebaut. Jeder Vorgang mit Daten erscheint als Balken vom **Startdatum** bis zum **Fälligkeitsdatum**. So erkennst du Überschneidungen, Lücken und den kritischen Pfad auf einen Blick.

- **Abhängigkeiten**: Verknüpfungen zwischen Vorgängen sind als Linien gezeichnet. Verzögert sich ein Vorgang, siehst du, was dahinter nach hinten rutscht.
- **Fortschritt**: Jeder Balken zeigt, wie weit sein Vorgang ist. So siehst du sofort, ob der Plan hält.
- **Gruppierung**: Du kannst einem Projekt, einem Epic oder einer zugewiesenen Person entlang der Timeline folgen.

!!! info "Daten treiben die Timeline"
    Ein Balken erscheint erst, wenn ein Vorgang ein **Start-** und/oder **Fälligkeitsdatum** hat. Du setzt sie in der Detailansicht des Vorgangs (siehe [Vorgänge](/de/issues.html)). Die Timeline aktualisiert sich sofort.

!!! tip "Plane auf dem Board, prüfe auf der Timeline"
    Auf dem [Board](/de/boards-sprints.html) legst du fest, *was* in einen Sprint kommt. Auf der Timeline prüfst du, *wann* alles passieren muss und ob die Abhängigkeiten zusammenpassen.

## Zeiterfassung

Die Timeline zeigt den Plan, die Zeiterfassung die Wirklichkeit. Alle, die an einem Vorgang arbeiten, können ihren Aufwand erfassen.

### Arbeit erfassen

Öffne einen Vorgang und wähle **Zeit erfassen**. Ein Arbeitseintrag enthält:

- **Dauer**: Stunden und Minuten.
- **Tätigkeitsart**: **Entwicklung, Testen, Dokumentation, Design, Meeting** oder **Support**. So lässt sich der Aufwand nach Art der Arbeit auswerten.
- **Datum**: wann die Arbeit stattfand (jeder Tag bis heute).
- **Notiz**: optional, was du gemacht hast.

Jeder Vorgang zeigt **aufgewendet vs. Schätzung**. So fällt sofort auf, wenn etwas den Rahmen sprengt.

!!! tip "Zeit direkt aus einem Commit erfassen"
    Mit aktiver [Git-Integration](/de/git-integration.html) erfasst ein Smart Commit Arbeit, ohne dass du deinen Editor verlässt: `MOB-42 #time 2h 30m` legt an `MOB-42` einen Arbeitseintrag über 2½ Stunden an.

### Wöchentlicher Stundenzettel

Arbeitseinträge ergeben einen **wöchentlichen Stundenzettel**: eine Zeile je Person und Projekt, eine Spalte je Tag. Damit prüfst du schnell eine Woche, findest Lücken und meldest Zeit ohne Tabellenkalkulation.

## Wohin die Zahlen fließen

Erfasste Zeit und Schätzungen fließen in die Liefermetriken: Kapazitätsplanung bei [Sprints](/de/boards-sprints.html) sowie Auswertungen zu Zykluszeit und Aufwand in den [Berichten](/de/reports.html).

## Nächste Schritte

- Setze Daten und Abhängigkeiten an deinen [Vorgängen](/de/issues.html).
- Lies die Liefermetriken in [Berichte & Dashboard](/de/reports.html).
- Automatisiere die Zeiterfassung mit [Smart Commits](/de/git-integration.html).
