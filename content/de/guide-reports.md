---
title: Berichte & Dashboard
description: Dein Dashboard lesen — Fokus, aktiver Sprint, Fortschritt, Fokuszeit — dann die Berichte, was jedes Diagramm ehrlich aussagt und wie du exportierst.
---

# Berichte & Dashboard

Zwei Bildschirme machen aus der Arbeit, die du ohnehin schon erfasst, etwas
Lesbares. Das **Dashboard** ist persönlich und beantwortet *Was mache ich als
Nächstes?*; es ist der Bildschirm, auf dem du jeden Morgen landest. **Berichte**
ist geteilt und beantwortet *Wie läuft dieses Projekt eigentlich?*

Keiner von beiden verlangt zusätzliche Eingaben. Beide sind nur so ehrlich wie
die Vorgänge darunter — und genau darum geht es auf dieser Seite.

## Dein Dashboard

**Home** in der Seitenleiste. Es öffnet mit deinem Namen, dem heutigen Datum und
— wenn ein Sprint läuft — mit dem Sprint-Tag, an dem du gerade stehst.

![Das Hinata-Dashboard mit der Karte zum aktiven Sprint, der Fokusliste, Kennzahlen, Projektfortschritt und Fokuszeit](/assets/img/shot-dashboard.png)
*Das Dashboard. Die dunkle Karte oben ist der laufende Sprint; die vier kleinen Kacheln rechts sind Zählungen, die sich anklicken lassen; Donut und Balkendiagramm darunter fassen das Projekt und deine eigene Woche zusammen.*

### Die Karte zum aktiven Sprint

Die große dunkle Karte ist das Board, das gerade für dich zählt. Läuft auf einem
Scrum-Board ein Sprint, bekommst du den Sprint: seinen Namen, darunter sein Ziel
und drei Chips: den Tag, an dem du im Kalender des Sprints stehst, die
abgeschlossenen Story Points von den committeten und die fertigen Vorgänge von
denen im Sprint.

Der Ring rechts erzählt dieselbe Geschichte als einzelne Prozentzahl, und die
Reihe Avatare zeigt, wer in diesem Sprint Vorgänge zugewiesen hat. **Zum Board**
bringt dich direkt dorthin.

Läuft kein Sprint, fällt die Karte auf eine Kanban-Übersicht eines Boards zurück,
deren Fortschritt sich aus abgeschlossenen Vorgängen statt aus Punkten speist.
Hast du überhaupt kein Board, bietet sie an, einen Sprint zu planen.

!!! tip "Hefte das Board an, das dich interessiert"
    Standardmäßig nimmt die Karte den ersten laufenden Sprint, den sie in deinen
    Projekten findet. Wenn du über mehrere Projekte hinweg arbeitest, hefte über
    **Anpassen** ein Board an, damit die Karte nicht unter dir wechselt.

### Die vier Kennzahlen

Die kleinen Kacheln sind Zählungen — und jede ist ein Link: Ein Tipp öffnet die
Vorgangsliste, bereits auf genau die gezählte Menge gefiltert, in denselben
Projekten.

| Kachel | Was gezählt wird |
| --- | --- |
| **Heutige Aufgaben** | *Deine* offenen Vorgänge, die heute fällig oder bereits überfällig sind, nach Priorität sortiert. |
| **In Arbeit** | Jeder Vorgang im Bereich, der begonnen, aber nicht fertig und nicht im Backlog ist. |
| **Backlog** | Jeder Vorgang im Bereich, der noch in Backlog oder Open sitzt. |
| **Erledigt** | Jeder Vorgang im Bereich in einem der Abschlussstatus deines Projekts. |

!!! warning "Nur die erste Kachel handelt von dir"
    **Heutige Aufgaben** zählt deine eigene Arbeit. Die anderen drei zählen die
    des ganzen Teams, über alle Projekte im Bereich des Dashboards. Ein Backlog
    von 33 sind nicht 33 Dinge, die auf dich warten.

### Fokus heute

Die Liste darunter ist dieselbe Menge wie die erste Kachel — deine offenen
Vorgänge, heute fällig oder überfällig —, höchste Priorität zuerst, und sie zeigt
die ersten fünf. Jede Zeile bringt den Vorgangstyp als Glyphe, den Titel, den
Schlüssel und in Rot, wie überfällig er ist. Der dünne Balken rechts ist der
aufgewendete Aufwand gegen die Zeitschätzung des Vorgangs, sofern es eine gibt.

Tippe auf eine Zeile, und der Vorgang öffnet sich über dem Dashboard; schließt du
ihn, bist du wieder da, wo du warst. **Alle Issues →** öffnet die vollständige
gefilterte Liste.

Ist die Liste leer, bekommst du „Keine dringenden Aufgaben für heute — genieß den
Tag!“ — eine echte Antwort, kein Platzhalter.

### Projektfortschritt

Der Donut ist eine Fortschrittsaufteilung über alle Projekte im Bereich. Die Zahl
in der Mitte ist der gelöste Anteil in Prozent; die Legende teilt dieselbe Summe
in **Erledigt**, **In Arbeit** und **Backlog** auf, mit der Gesamtzahl der
Vorgänge in der Ecke.

Lies ihn als Form, nicht als Zahl. Ein Backlog-Segment, das den Ring dominiert,
heißt, dass mehr hereinkommt, als hinausgeht — und das ist gut zu wissen, lange
bevor eine Deadline es sagt.

### Fokuszeit

Deine erfassten Stunden, und nur deine. Sieben Balken für die letzten sieben
Tage, der heutige in Bernstein, oben eine Summe in Stunden und ein Umschalter
**Woche** / **Monat**, der dieselben Daten in die letzten fünf Kalenderwochen
gruppiert.

Es steht auf `0,0 Std`, bis jemand Arbeit erfasst — wie die Einträge dorthin
kommen, steht unter [Zeit erfassen](/de/guide-time.html). Beachte, dass Zeit aus
einem Git-Commit dieses Diagramm nicht erreicht.

### Team-Ranking und Git-Aktivität

Zwei weitere Karten, beide etwas abseits vom Tagesgeschäft:

- **Team-Ranking** zählt die in den letzten 30 Tagen gelösten Vorgänge pro
  Person, die besten zehn. Die Karte ist augenzwinkernd gemeint und zählt bewusst
  Vorgänge statt Stunden — nichts hier belohnt es, mehr Zeit zu erfassen.
- **Git-Aktivität** listet jüngste Commits, Pull Requests und Merges aus den
  Repositories, mit denen deine Projekte verbunden sind. Sie erscheint nur, wenn
  eine Administratorin oder ein Administrator die
  [Git-Integration](/de/git-integration.html) eingerichtet hat.

### Anpassen

**Anpassen** oben rechts macht das Dashboard bearbeitbar.

![Das Dashboard im Bearbeitungsmodus mit den Auswählern für Hero-Board, Dashboard-Daten und Team-Ranking](/assets/img/shot-dashboard-customize.png)
*Der Bearbeitungsmodus. Über den Kacheln stehen ein Hinweisstreifen und drei Felder — „Hero-Board“, „Dashboard-Daten“ und „Team-Ranking“ —, jede Kachel bekommt ein Augensymbol, das sie ausblendet, und das amberfarbene „Fertig“ steht dort, wo „Anpassen“ stand.*

„Dashboard-Daten“ ist die Einstellung, die die Zahlen bewegt: Grenzt du sie auf
deine eigenen Projekte ein, zählen Kennzahlen, Donut und „Fokus heute“ keine
Arbeit mehr mit, mit der du nichts zu tun hast.

![Der Auswähler für das Hero-Board, geöffnet, mit Haken auf „Automatisch (aktiver Sprint)“](/assets/img/shot-dashboard-hero-board-picker.png)
*Das Feld „Hero-Board“ öffnet ein angedocktes Popover. „Automatisch (aktiver Sprint)“ trägt den Haken; darunter steht jedes Board, das du erreichst — hier „Hinata Platform Board“.*

Drücke **Fertig**, um zu speichern. Das Layout gehört zu deinem Konto und nicht
zu diesem Gerät, folgt dir also aufs Handy — und wer die Seite verlässt, ohne
Fertig zu drücken, verwirft die Änderungen.

## Berichte

**Berichte** in der Seitenleiste, auf dem Handy hinter **Mehr**. Berichte
betrachten **ein Projekt auf einmal**.

![Der Projektauswähler auf der Berichteseite, geöffnet, mit drei Projekten](/assets/img/shot-reports-project-picker.png)
*Der Auswähler unter der Überschrift, geöffnet. Er listet nur die Projekte, die dir dein Teamzugriff gewährt, mit einem Haken auf dem gerade gezeigten; ein anderes zu wählen, zeichnet jede Karte der Seite neu.*

### Burndown · letzte 30 Tage

![Die Hinata-Berichte mit dem 30-Tage-Burndown, der Gesamtzahl und der Verteilung nach Status](/assets/img/shot-reports.png)
*Der obere Teil der Seite. Die bernsteinfarbene Linie sind die an jedem der letzten 30 Tage offenen Vorgänge gegen eine gestrichelte Ideallinie, mit der heutigen Zahl in der Ecke; darunter „Aufgaben gesamt“ und „Aufgaben nach Status“.*

Die bernsteinfarbene Linie zeigt, wie viele Vorgänge an jedem der letzten 30 Tage
offen waren — verankert an der heutigen echten Zahl offener Vorgänge und rückwärts
rekonstruiert aus dem, was wann erstellt und gelöst wurde. Die gestrichelte graue
Linie ist eine gerade Referenz von deinem Startwert auf null — das Tempo, das du
bräuchtest, um bis heute alles abzuarbeiten.

Diese Referenzlinie ist ein Lineal, kein Plan. Niemand hat sich auf sie
verpflichtet. Ihre einzige Aufgabe ist es, der bernsteinfarbenen Linie etwas zu
geben, woran sie gemessen werden kann.

!!! tip "Ein Burndown, der sich nie beugt, sagt dir etwas"
    - **Flach.** Du schließt Arbeit genau so schnell, wie du sie öffnest. Nichts
      ist kaputt, aber es schrumpft auch nichts — eine Warteschlange im
      Gleichgewicht.
    - **Steigend.** Der Zulauf schlägt die Lieferung. Sieh dir das
      Backlog-Segment auf dem Dashboard an; die beiden sind sich einig, und
      keines davon ist ein Planungsproblem, das sich durch schnelleres Arbeiten
      lösen lässt.
    - **Eine Klippe kurz vor dem Ende.** Arbeit wurde in einem Schwung fertig.
      Meist heißt das, dass Vorgänge in einem Review- oder QA-Status lagen und
      alle auf einmal auf erledigt gesetzt wurden — was verdeckt, wo die
      Verzögerung wirklich war.
    - **Perfekt auf der gestrichelten Linie.** Sei eher misstrauisch als stolz.
      Echte Arbeit ist klumpig.

Die Zahl oben rechts ist der heutige Wert und die einzige Zahl auf dieser Karte,
die gemessen und nicht rekonstruiert ist.

### Aufgaben gesamt

Jeder Vorgang, den es in diesem Projekt je gab, gelöst oder nicht. Es ist der
Maßstab, an dem du alles andere auf der Seite liest: 7 Vorgänge *In Review* von
53 sind eine Warteschlange; von 5.000 sind sie ein Rundungsfehler.

### Aufgaben nach Status

Ein Balken pro Workflow-Status, längster zuerst, in der Farbe des Status und mit
der Anzahl beschriftet. Es sind die Status deines Projekts — genau die, wie deine
Board-Spalten heißen —, ein Projekt mit *In Parking* oder *Abgenommen* sieht sie
also auch hier.

Das ist der Engpass-Detektor. Ein Stau in einem einzelnen, nicht abschließenden
Status ist das klarste Signal, das diese Seite erzeugt: Arbeit kommt dort
schneller an, als sie jemand herausnimmt.

### Aufgaben nach Priorität

![Die Auswertungen nach Priorität, Bearbeiter und Tätigkeit weiter unten auf der Berichteseite](/assets/img/shot-reports-breakdowns.png)
*Die drei Karten unterhalb des Sichtbereichs: „Aufgaben nach Priorität“ mit einer Flagge pro Zeile, „Aufgaben nach Bearbeiter“ mit einem Avatar pro Zeile und „Zeit pro Tätigkeit (30 Tage)“, dessen Balken Dauern statt Anzahlen sind.*

Lies die Priorität als Anteil, nicht als Anzahl: Wenn der Großteil des Projekts
als dringend markiert ist, trägt die Markierung keine Information mehr — was das
verlangt, ist eine Triage-Runde und kein größeres Team.

### Aufgaben nach Bearbeiter

Vorgänge, die niemandem gehören, sammeln sich unter **unassigned** — meist die
interessanteste Zeile auf der Karte, denn Arbeit ohne Besitzer wird von niemandem
versehentlich fertig.

!!! warning "Vorgänge zählen ist nicht Aufwand messen"
    Jede Verteilung hier zählt Vorgänge, und Vorgänge sind nicht gleich groß. Eine
    Person mit zwölf winzigen Bugs schlägt in jedem dieser Diagramme eine Person,
    die eine dreiwöchige Migration trägt. Nutze sie, um Formen zu erkennen — einen
    Stau, eine leere Spalte, einen herrenlosen Haufen — und ein Gespräch, um sie
    zu deuten.

### Zeit pro Tätigkeit (30 Tage)

Die in den letzten 30 Tagen von allen erfasste Arbeit an diesem Projekt,
summiert je Tätigkeitsart. Sie enthält nur Arbeit, die als
[Zeiteintrag](/de/guide-time.html) erfasst wurde; Zeit aus einem Git-Commit
erreicht sie nicht.

### Sprint-Burndown und Velocity leben auf dem Board

Die Berichteseite ist projektweit und auf 30 Tage begrenzt. Die
sprint-bezogenen Kennzahlen — Sprint-Burndown, Velocity über abgeschlossene
Sprints, Ø Velocity, Umfangsänderungen und die Arbeitsverteilung nach Bearbeiter —
leben im Tab **Auswertung** des Boards selbst, neben Planung und Aktiver Sprint.
Siehe [Boards & Sprints](/de/guide-boards.html).

## All das ehrlich lesen

Eine Handvoll Gewohnheiten, die verhindern, dass ein Dashboard zur Dekoration
wird:

- **Prüfe, welches Zeitfenster gilt.** Burndown und Tätigkeitsaufschlüsselung
  decken 30 Tage ab; das Team-Ranking deckt 30 Tage ab; die Verteilungen decken
  den gesamten Zeitraum ab. Ein Projekt, das vor zwei Monaten die Richtung
  gewechselt hat, wirkt darüber hinweg widersprüchlich — und das ist der Beweis,
  dass die Diagramme recht haben.
- **Diagramme erben deinen Workflow.** „Aufgaben nach Status“ ist nur so
  aussagekräftig wie deine Status. Wenn alles in einem einzigen vagen *In
  Progress* sitzt, kann kein Bericht die Details erfinden — das ist ein Gespräch
  über die [Projekteinstellungen](/de/guide-projects.html).
- **Achte auf den fehlenden Balken.** Ein Bearbeiter ohne Balken, ein Status ohne
  Vorgänge, ein Tag ohne erfasste Zeit — Abwesenheiten tragen so viel Information
  wie Ausschläge.
- **Präsentiere nie eine Zahl ohne die Frage, die sie beantwortet.** „Vierzehn
  Vorgänge sind In Review“ ist eine Beobachtung. „Vierzehn Vorgänge sind In
  Review, weil eine Person jedes Review macht“ ist etwas, womit ein Team arbeiten
  kann.

## Einen Bericht exportieren

![Das Export-Menü oben rechts auf der Berichteseite, geöffnet](/assets/img/shot-reports-export-menu.png)
*„Exportieren“ oben rechts öffnet drei Möglichkeiten: „Als PDF exportieren“, „Als CSV exportieren“ und „Als JSON exportieren“. Jede umfasst das Projekt, das gerade auf dem Bildschirm ist, nicht alle.*

**Als PDF exportieren** baut aus dem, was du gerade siehst, ein druckbares
A4-Dokument: Name und Logo deiner Organisation oben, der Projektname, ein
Erstellungszeitstempel, die Gesamtzahl der Vorgänge, das Burndown-Diagramm und
jede Verteilungskarte als Tabelle aus Beschriftungen und Werten — inklusive der
Dauern aus „Zeit pro Tätigkeit“. Die Seiten sind in der Fußzeile nummeriert. Es
kommt über den üblichen Teilen- oder Speichern-Dialog deiner Plattform und heißt
etwa `hinata-report-Website-Relaunch-2026-08-20.pdf`, ist also ohne Umbenennen
bereit für eine Mail oder eine Gremienvorlage.

**Als CSV exportieren** und **Als JSON exportieren** geben dir dieselben Zahlen
als Daten, für eine Tabelle oder ein Skript. In der Web-App öffnen sie sich als
Download; in den Desktop- und Mobil-Apps werden sie in die Zwischenablage
kopiert, bestätigt von einem Toast — füge sie also ein, statt im
Download-Ordner zu suchen.

!!! tip "Exportiere in dem Moment, in dem du präsentierst"
    Jeder Export ist eine Momentaufnahme mit aufgedrucktem Erstellungszeitpunkt.
    Exportiere ihn, wenn du gleich darüber sprichst, dann stimmen die Fassung im
    Meeting und die auf dem Bildschirm überein.

!!! note "Berichte zeigen, was du sehen darfst"
    Die Berichte, die du bauen kannst, sind von denselben Sichtbarkeitsregeln
    begrenzt wie der Rest der App. Siehe
    [Projekte & Teams](/de/guide-projects.html).

## Nächste Schritte

- Verbessere die Eingangsdaten: Halte [Vorgänge](/de/guide-issues.html) in korrekten Status und gib ihnen Verantwortliche.
- Speise die Aufwandszahlen, indem du [Zeit erfasst](/de/guide-time.html).
- Hol dir Sprint-Kennzahlen aus dem Tab Auswertung unter [Boards & Sprints](/de/guide-boards.html).
