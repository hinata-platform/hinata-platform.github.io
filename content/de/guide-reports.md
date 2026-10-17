---
title: Berichte & Dashboard
description: So liest du Dashboard und Berichte und exportierst sie.
---

# Berichte & Dashboard

- Das **Dashboard** ist persönlich und zeigt, was du als Nächstes tust.
- **Berichte** zeigen allen, wie ein Projekt läuft.

Beide brauchen keine zusätzlichen Eingaben und sind nur so genau wie deine
Vorgänge.

## Dein Dashboard

Öffne **Home** in der Seitenleiste. Oben stehen dein Name, das Datum und, wenn
ein Sprint läuft, der aktuelle Sprinttag.

![Das Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Das Dashboard.*

### Die Karte zum aktiven Sprint

Läuft auf einem Scrum-Board ein Sprint, zeigt die große dunkle Karte:

- Name und Ziel des Sprints
- Chips für den Sprinttag, erledigte von committeten Story Points und fertige
  von allen Vorgängen
- einen Ring mit dem Fortschritt in Prozent
- Avatare aller, die im Sprint Vorgänge zugewiesen haben

**Zum Board** öffnet das Board. Ohne Sprint zeigt die Karte eine
Kanban-Übersicht, deren Fortschritt erledigte Vorgänge statt Punkte zählt. Ohne
Board bietet sie an, einen Sprint zu planen.

!!! tip "Board anheften"
    Standardmäßig nimmt die Karte den ersten laufenden Sprint aus deinen
    Projekten. Über **Anpassen** heftest du ein festes Board an.

### Die vier Kennzahlen

Ein Tipp auf eine Kachel öffnet die Vorgangsliste, gefiltert auf genau diese
Vorgänge.

| Kachel | Was gezählt wird |
| --- | --- |
| **Heutige Aufgaben** | *Deine* offenen Vorgänge, heute fällig oder überfällig, nach Priorität. |
| **In Arbeit** | Alle begonnenen Vorgänge im Bereich, die nicht fertig und nicht im Backlog sind. |
| **Backlog** | Alle Vorgänge im Bereich in Backlog oder Open. |
| **Erledigt** | Alle Vorgänge im Bereich in einem Abschlussstatus deines Projekts. |

!!! warning "Nur die erste Kachel betrifft dich"
    Die anderen drei zählen die Arbeit des ganzen Teams in allen Projekten des
    Dashboards.

### Fokus heute

Die Liste zeigt die ersten fünf Vorgänge aus **Heutige Aufgaben**, höchste
Priorität zuerst. Jede Zeile hat Typ, Titel, Schlüssel und in Rot die
Überfälligkeit. Der dünne Balken rechts zeigt die aufgewendete Zeit gegen die
Schätzung, falls es eine gibt.

Ein Tipp öffnet den Vorgang über dem Dashboard. **Alle Issues →** öffnet die
ganze Liste. Ist nichts fällig, zeigt Hinata einen kurzen Hinweis.

### Projektfortschritt

Der Donut zeigt in der Mitte den gelösten Anteil aller Projekte im Bereich. Die
Legende teilt in **Erledigt**, **In Arbeit** und **Backlog**, die Gesamtzahl steht
in der Ecke. Ist das Backlog der größte Teil, kommt mehr herein, als fertig wird.

### Fokuszeit

Nur deine erfassten Stunden: sieben Balken für die letzten sieben Tage (heute in
Bernstein) und oben die Summe. **Woche** / **Monat** zeigt die letzten fünf
Kalenderwochen. Ohne Einträge steht dort `0,0 Std`. Zeit aus Git-Commits zählt
nicht mit. Siehe [Zeit erfassen](/de/guide-time.html).

### Team-Ranking und Git-Aktivität

- **Team-Ranking**: die zehn Personen mit den meisten gelösten Vorgängen der
  letzten 30 Tage. Augenzwinkernd gemeint, Stunden zählen hier bewusst nicht.
- **Git-Aktivität**: neue Commits, Pull Requests und Merges aus den verbundenen
  Repositories. Nur sichtbar, wenn die
  [Git-Integration](/de/git-integration.html) eingerichtet ist.

### Anpassen

**Anpassen** oben rechts startet den Bearbeitungsmodus.

![Das Dashboard im Bearbeitungsmodus](/assets/img/shot-dashboard-customize.png)
*Der Bearbeitungsmodus.*

- Über den Kacheln stehen die Felder „Hero-Board“, „Dashboard-Daten“ und
  „Team-Ranking“.
- „Hero-Board“ wählt das Board für die große Karte. Standard ist „Automatisch
  (aktiver Sprint)“.
- „Dashboard-Daten“ legt fest, welche Projekte Kennzahlen, Donut und „Fokus
  heute“ zählen.
- Das Augensymbol auf einer Kachel blendet sie aus.

![Die Auswahl für das Hero-Board](/assets/img/shot-dashboard-hero-board-picker.png)
*„Hero-Board“ listet alle Boards, die du erreichst.*

**Fertig** speichert. Das Layout gilt für dein Konto, also auch auf dem Handy.
Ohne **Fertig** gehen die Änderungen verloren.

## Berichte

Öffne **Berichte** in der Seitenleiste, auf dem Handy unter **Mehr**. Die Seite zeigt immer **ein Projekt**. Die Projektkapsel oben öffnet eine Suche über alle Projekte, die du über dein Team erreichst. Daneben wählst du **30 Tage** oder **90 Tage**.

Ist das erweiterte Time-Tracking eingeschaltet, ist dieselbe Übersicht der erste Reiter **Projekt** der Zeitberichte. Daneben stehen **Budgets** und die Zeitberichte selbst, alle mit einem gemeinsamen Filter. Siehe [Erweitertes Time-Tracking](/de/time-tracking-advanced.html).

![Die Berichteseite mit Kennzahlen und Verlauf](/assets/img/shot-reports.png)
*Kennzahlen, Verlauf und Budget eines Projekts.*

### Kennzahlen

Vier Kacheln oben: die heute **offenen** Vorgänge, die im Zeitraum **neu** angelegten, die im Zeitraum **erledigten** und, mit dem erweiterten Time-Tracking, die im Zeitraum **erfasste** Zeit.

### Wie entwickeln sich die offenen Aufgaben?

- **Honigfläche**: offene Vorgänge an jedem Tag des Zeitraums, rückwärts berechnet ab der heutigen Zahl.
- **Gestrichelte Linie**: gerader Weg vom Startwert auf null. Sie dient nur als Maßstab.

!!! tip "Was die Form bedeutet"

    - **Flach:** Es wird so viel fertig, wie hereinkommt.
    - **Steigend:** Es kommt mehr herein, als fertig wird. Schneller arbeiten
      löst das nicht.
    - **Abfall kurz vor Schluss:** Vorgänge lagen in Review oder QA und wurden
      gesammelt geschlossen. Wo es hing, bleibt verborgen.
    - **Genau auf der Linie:** Werde misstrauisch. Echte Arbeit ist
      unregelmäßig.

### Wie füllt sich das Budget?

Hat das Projekt ein Zeitbudget, steht hier seine Röhre mit Prognose. **Verlauf** öffnet die Kurve der erfassten Stunden. Siehe [Budgets](/de/time-tracking-advanced.html#budgets).

### Wo stehen die Aufgaben? Wie dringend ist die Arbeit?

![Verteilungen weiter unten auf der Berichteseite](/assets/img/shot-reports-breakdowns.png)
*Status, Priorität, Personen und Tätigkeiten.*

Status erscheinen als Gläser, die sich in der Statusfarbe füllen, eigene Status wie *In Parking* eingeschlossen. Ein Stau in einem Status vor dem Abschluss zeigt einen Engpass. Bei der Priorität achte auf den Anteil: Ist fast alles dringend, ist eine Triage fällig.

### Wer arbeitet woran? Wofür geht die Zeit?

Vorgänge ohne Verantwortlichen stehen unter **Niemand zugewiesen**. Diese Zeile solltest du im Blick behalten. Die Zeit je Tätigkeit zählt nur [Zeiteinträge](/de/guide-time.html) im Zeitraum, keine Zeit aus Git-Commits.

!!! warning "Anzahl ist nicht Aufwand"
    Alle Verteilungen zählen Vorgänge. Zwölf kleine Bugs wiegen hier mehr als
    eine dreiwöchige Migration. Nutze die Diagramme, um Muster zu finden, und
    kläre die Gründe im Gespräch.

### Budgets

![Der Reiter Budgets mit Sprint und Projekten](/assets/img/shot-reports-budgets.png)
*Budgets, das vollste zuerst.*

Mit dem erweiterten Time-Tracking listet der Reiter **Budgets** alle Budgets, die du sehen darfst, das vollste zuerst. Oben stehen die laufenden Sprints mit Budget. Jede Projektkarte zeigt Zeitbudget mit Prognose, die Schätzungen und, wenn du es sehen darfst, das Geldbudget.

### Sprint-Burndown und Velocity leben auf dem Board

Sprintkennzahlen stehen im Tab **Auswertung** des Boards, neben Planung und
Aktiver Sprint: Sprint-Burndown, Velocity über abgeschlossene Sprints, Ø
Velocity, Umfangsänderungen und Arbeitsverteilung nach Bearbeiter. Siehe
[Boards & Sprints](/de/guide-boards.html).

## Diagramme richtig lesen

- **Zeitraum prüfen.** Verlauf und Zeit pro Tätigkeit zeigen den gewählten
  Zeitraum, das Team-Ranking 30 Tage, die Verteilungen den gesamten Zeitraum. Deshalb können sie sich
  scheinbar widersprechen.
- **Workflow prüfen.** Liegt alles in einem vagen *In Progress*, zeigt kein
  Bericht Details. Das änderst du in den
  [Projekteinstellungen](/de/guide-projects.html).
- **Auf Lücken achten.** Fehlende Balken sagen so viel wie hohe.
- **Zahlen erklären.** „Vierzehn Vorgänge sind In Review, weil eine Person jedes
  Review macht“ hilft mehr als die Zahl allein.

## Einen Bericht exportieren

**Exportieren** oben rechts. Jeder Export umfasst nur das angezeigte Projekt.

![Das Exportmenü auf der Berichteseite](/assets/img/shot-reports-export-menu.png)
*Das Exportmenü.*

- **Als PDF exportieren**: druckbares A4-Dokument mit Name und Logo deiner
  Organisation, Projektname, Erstellungszeitpunkt, Gesamtzahl, Burndown, allen
  Verteilungen als Tabelle (auch Zeit pro Tätigkeit) und Seitenzahlen. Es kommt
  über den Dialog zum Teilen oder Speichern und heißt etwa
  `hinata-report-Website-Relaunch-2026-08-20.pdf`.
- **Als CSV exportieren** und **Als JSON exportieren**: dieselben Zahlen als
  Daten. Im Browser als Download, in den Apps für Desktop und Handy in der
  Zwischenablage, bestätigt durch einen Toast.

!!! tip "Kurz vor dem Termin exportieren"
    Jeder Export ist eine Momentaufnahme mit aufgedruckter Erstellungszeit.

!!! note "Berichte zeigen, was du sehen darfst"
    Es gelten dieselben Sichtbarkeitsregeln wie im Rest der App. Siehe
    [Projekte & Teams](/de/guide-projects.html).

## Nächste Schritte

- Halte [Vorgänge](/de/guide-issues.html) im richtigen Status und gib ihnen Verantwortliche.
- [Erfasse deine Zeit](/de/guide-time.html) für genaue Aufwandszahlen.
- Sprintkennzahlen findest du im Tab Auswertung unter [Boards & Sprints](/de/guide-boards.html).
