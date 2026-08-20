---
title: Timeline & Abhängigkeiten
description: Dein Projekt als Gantt-Diagramm lesen — Balken, Meilensteine und Fortschritt — dann die Abhängigkeiten zwischen Vorgängen ziehen und sehen, wo der Plan nicht aufgeht.
---

# Timeline & Abhängigkeiten

Die Zeitachse beantwortet eine Frage, die ein Board nicht beantworten kann: *wann*. Ein Board sagt dir, in welchem Status alles ist; die Zeitachse legt dieselbe Arbeit auf einen Kalender, zeichnet die Verbindungen zwischen den Teilen und zeigt dir, wo zwei davon für denselben Zeitraum zugesagt wurden.

Das Wichtigste vorweg: Die Zeitachse **speichert nichts Eigenes**. Jeder Balken ist das Start- und Fälligkeitsdatum eines Vorgangs. Jeder Verbinder ist eine Verknüpfung zwischen zwei Vorgängen. Ändere ein Datum am Vorgang, und der Balken wandert; entferne eine Verknüpfung, und der Pfeil verschwindet. Es gibt keinen zweiten Plan, den man synchron halten müsste — und genau deshalb kann man dem Bild trauen.

## Die Zeitachse öffnen

Wähle **Gantt** in der Seitenleiste. Die Seite heißt **Zeitachse** und hat oben rechts eine Projektauswahl: Das Diagramm zeigt immer ein Projekt.

In dieser Auswahl findest du nur Projekte, in denen du Mitglied bist. Fehlt ein Projekt, das du erwartest, ist das eine Frage der Projekt- oder Team-Mitgliedschaft und hat mit der Zeitachse nichts zu tun — [Projekte & Teams](/de/guide-projects.html) erklärt, wie der Zugriff funktioniert.

Es gibt einen zweiten Weg hinein. Auf einem Kanban-Board legt die Ansicht **Timeline** die Vorgänge dieses Boards aus — genau so gefiltert, wie du das Board gefiltert hast. Beide Diagramme lesen sich identisch; sie starten nur von unterschiedlichen Mengen an Vorgängen. Zum Umschalter siehe [Boards & Sprints](/de/guide-boards.html).

Wann was: die **Gantt-Seite**, wenn du das ganze Projekt willst, auch Arbeit, die kein Board abdeckt; die **Timeline des Boards**, wenn du den Ausschnitt willst, den du schon eingegrenzt hast.

## Was du da vor dir hast

![Die Hinata-Zeitachse](/assets/img/shot-gantt.png)
*Die Seite „Zeitachse“. Links eine fixierte Spalte mit den Vorgängen — Typ, Schlüssel und Titel. Oben der Monat mit seinen Tagesziffern, heute (der 20.) blau eingekreist, dazu eine blaue Linie quer durchs Diagramm. Unten rechts die schwebende Steuerung: Verknüpfungen, Heute, Woche und Monat. Das Diagramm öffnet immer zentriert auf heute — Balken außerhalb des sichtbaren Ausschnitts liegen daneben, bis du scrollst oder auf Monat umschaltest.*

Vier Teile, jeder mit einer Aufgabe:

- **Die Vorgangsspalte** links ist fixiert — sie bleibt stehen, während das Diagramm seitwärts scrollt, damit du nie den Überblick verlierst, welche Zeile du liest. Ein Klick auf einen Titel öffnet den Vorgang.
- **Die Datumsachse** oben zeigt das Monatsband und in der Zoomstufe **Woche** darunter die einzelnen Tagesziffern. Wochenenden sind hinterlegt, damit eine Woche wie eine Woche aussieht.
- **Heute** ist doppelt markiert: eingekreist in der Achse und als senkrechte Linie durchs Diagramm. Beim Öffnen scrollt die Zeitachse auf heute, weil man fast immer dort anfangen will.
- **Die schwebende Steuerung** unten rechts trägt **Verknüpfungen** (welche Verbinder gezeichnet werden), **Heute** (zurück zum Jetzt) und den Zoom **Woche** / **Monat**. Woche liefert Tagesgenauigkeit; Monat presst mehrere Quartale auf einen Bildschirm.

!!! tip "Es scrollt in beide Richtungen"
    Das Diagramm scrollt seitwärts durch die Zeit und nach unten durch die Vorgänge; Achse und Vorgangsspalte laufen mit. Auf dem Handy schrumpft die schwebende Steuerung zu Symbolen, damit dem Diagramm jeder Pixel bleibt.

### Zwischen Wochen und Monaten zoomen

Die zwei Zoomstufen sind nicht bloß größer und kleiner — sie beantworten unterschiedliche Fragen.

**Woche** ist die Arbeitsstufe. Jeder Tag bekommt eine eigene Spalte, Wochenenden sind hinterlegt, und jeder Balken trägt seinen Vorgangsschlüssel im Inneren. Nimm sie, wenn du entscheidest, was an welchem Tag passiert, prüfst, ob zwei Personen gegeneinander verplant sind, oder das Diagramm in einer Planung laut vorliest.

**Monat** presst jeden Monat in eine Spalte. Einzelne Tage verschwinden, die Beschriftungen in den Balken ebenso, dafür passt ein Jahr Arbeit auf einen Bildschirm. Nimm sie für die Form eines Plans: wo das volle Quartal liegt, ob die Meilensteine gleichmäßig verteilt sind, wie weit der letzte Balken wirklich reicht.

**Heute** bringt dich in beiden Stufen zurück ins Jetzt — der schnellste Weg zurück, wenn du bis ins nächste Frühjahr gescrollt bist.

Die Zeilen sind nach Startdatum sortiert, das Diagramm liest sich also grob von links oben nach rechts unten, so wie ein Gantt-Diagramm gemeint ist.

## Was einen Vorgang auf die Zeitachse bringt

Ein Vorgang erscheint, sobald er **ein Startdatum, ein Fälligkeitsdatum oder beides** hat und nicht archiviert ist. Das ist die ganze Regel. Jeder Typ zählt — Epics, Stories, Tasks, Bugs, Features und Sub-Tasks gleichermaßen — solange ein Datum dranhängt.

Ein Vorgang ohne Daten steht nicht im Diagramm. Das ist kein Fehler; es heißt, dass noch niemand gesagt hat, wann er stattfindet. Ist die Zeitachse leer, sagt sie dir das — und was zu tun ist.

### Die Daten setzen

Öffne den Vorgang und such die Karte **Timeline**. Sie hat zwei Zeilen:

- **Startdatum** — der erste Tag, den die Arbeit abdeckt.
- **Fälligkeitsdatum** — der letzte Tag, einschließlich.

Tippe eine der Zeilen an, um ein Datum zu wählen. Ist eines gesetzt, löscht ein kleines **×** daneben es wieder.

Das geht direkt aus dem Diagramm: Balken lange drücken (oder den Titel in der linken Spalte anklicken), und der Vorgang öffnet sich über der Zeitachse. Datum setzen, wieder schließen — das Diagramm wird neu gezeichnet, mit Scrollposition und Zoom genau dort, wo du sie verlassen hast.

!!! tip "Zwei Daten für Arbeit, eines für einen Termin"
    Gib einem Vorgang beide Daten, wenn er einen Zeitraum belegt. Gib ihm nur ein Fälligkeitsdatum, wenn er ein Moment ist und kein Zeitraum — siehe *Ein Fälligkeitsdatum allein ist ein Meilenstein* weiter unten.

## Einen Balken lesen

Ein Balken läuft vom Start- bis zum Fälligkeitsdatum, beide Tage eingeschlossen; ein Vorgang von Montag bis Freitag ist also fünf Tage breit.

**Die Farbe ist der Workflow-Status des Vorgangs** — dieselbe Farbe wie seine Spalte auf dem Board und sein Status-Chip im Vorgang. Erreicht der Vorgang einen Status, den dein Projekt als erledigt zählt, wechselt der Balken auf die Erledigt-Farbe; ein fertiger Plan wird also sichtbar von links nach rechts grün.

**Die hellere Füllung von der linken Kante ist der Fortschritt.** Woher diese Zahl kommt, lohnt sich zu wissen — sie ist kein Regler, den jemand zieht:

- Fortschritt ist **gebuchte Zeit gegen die Schätzung**. Zwei Stunden auf eine Vier-Stunden-Schätzung sind 50 %.
- Solange der Vorgang offen ist, ist er bei 99 % gedeckelt, egal wie viel gebucht wurde. Erst ein Erledigt-Status bringt ihn auf 100 %.
- Ein Vorgang ohne Schätzung zeigt 0 %, ganz gleich, wie viel Arbeit hineingeflossen ist.

Ein leerer Balken kann also „noch nicht angefangen“ heißen oder „hat niemand geschätzt“. Beides ist wissenswert, keines ist ein Fehler. Das Buchen von Aufwand steht unter [Zeit erfassen](/de/guide-time.html).

!!! tip "Ein Balken, der voller ist als der Kalender, ist eine Warnung"
    Vergleiche die Füllung damit, wo die Heute-Linie den Balken kreuzt. Ein Balken, der nach einem Drittel der Strecke zu 80 % gefüllt ist, hatte eine zu kleine Schätzung; einer, der zwei Tage vor Schluss kaum gefüllt ist, wurde noch gar nicht wirklich begonnen. Beides steht in keiner Statusliste — es ist das Nützlichste, was dir das Diagramm nebenbei erzählt.

Im Zoom **Woche** steht der Vorgangsschlüssel im Balken, damit auch ein Screenshot lesbar bleibt. Fährst du über einen Balken, nennt dir ein Tooltip Schlüssel, Status, Prozentwert, jede Beziehung, die dieser Vorgang im Diagramm hat, und eine Warnung, falls sein Termin kollidiert.

### Daten, Schätzungen und Story Points sind drei verschiedene Dinge

Sie werden leicht verwechselt, und die Zeitachse interessiert sich nur für eines davon. Es lohnt sich, festzuhalten, welche Zahl was tut:

| Was du setzt | Was es bedeutet | Wo es auftaucht |
| --- | --- | --- |
| **Start- & Fälligkeitsdatum** | *Wann* die Arbeit stattfindet | Der Balken auf der Zeitachse, die Spalte „Fällig“ in Vorgangslisten, das rote Datum auf einer überfälligen Karte |
| **Schätzung & gebuchte Zeit** | *Wie viel Aufwand* nötig ist und war | Die Fortschrittsfüllung im Balken, „aufgewendet von“ am Vorgang, Stundenzettel |
| **Story Points** | *Wie groß* er relativ zu anderer Arbeit ist | Sprint-Kapazität, Burndown und Velocity — nie die Zeitachse |
| **Sprint** | *Welches Zeitfenster* er belegt | Board und Backlog — ebenfalls nie die Zeitachse |

Ein Vorgang kann mit acht Story Points in einem Sprint stecken und trotzdem auf der Zeitachse fehlen, weil ihm niemand Daten gegeben hat. Umgekehrt genauso. Keines ist falsch; es sind Antworten auf verschiedene Fragen, und du brauchst nur die, die dein Team wirklich nutzt.

## Ein Fälligkeitsdatum allein ist ein Meilenstein

Ein Vorgang mit Fälligkeitsdatum, aber ohne Startdatum hat keine Länge — er ist ein Termin, kein Arbeitszeitraum. Die Zeitachse zeichnet ihn so, wie es jedes Gantt-Diagramm tut: als **Raute** an diesem einen Tag, umrandet solange der Vorgang offen ist, gefüllt sobald er erledigt ist.

Nimm sie für die Fixpunkte, an denen ein Plan hängt: ein Launch, eine Übergabe, eine Prüfung, der Tag, an dem der Raum gebucht ist. Weil ein Meilenstein ein ganz normaler Vorgang ist, lässt er sich zuweisen, diskutieren, beobachten und — am nützlichsten — verknüpfen, sodass alles, was vorher passieren muss, als Pfeil auf ihn zeigt.

## Eine Abhängigkeit ziehen

Eine **Abhängigkeit** ist ein Vorgang, der einen anderen blockiert: Der zweite kann nicht beginnen, bevor der erste fertig ist. Im Diagramm ist das ein durchgezogener Verbinder aus der rechten Kante des Blockierers, mit einer Pfeilspitze in die linke Kante des blockierten Vorgangs.

Zum Anlegen öffnest du den Vorgang und gehst zum Abschnitt **Verknüpfte Vorgänge**:

1. Wähle **Vorgang hinzufügen**.
2. Wähle die Verknüpfungsart aus der Liste. **wird blockiert von** und **blockiert** sind die beiden, die einen Terminplan einschränken.
3. Such die Vorgänge des Projekts nach Schlüssel oder Titel, wähle einen (oder mehrere) und bestätige mit **Verknüpfen**.

Die Verknüpfung erscheint sofort an beiden Vorgängen — der andere zeigt dieselbe Beziehung aus seiner Sicht formuliert — und der Verbinder erscheint auf der Zeitachse.

### Jede Beziehung — und was das Diagramm damit macht

Nur eine der sieben Verknüpfungsarten sagt etwas über *Reihenfolge*. Der Rest sagt, wie Vorgänge zusammengehören — am Vorgang nützlich, auf einem Kalender meist Rauschen. Deshalb zeichnet die Zeitachse sie als blasse Striche und lässt sie ausgeschaltet, bis du sie einschaltest.

| Verknüpfungsart | Liest sich als | Auf der Zeitachse |
| --- | --- | --- |
| **Blockiert** | *blockiert* / *wird blockiert von* | Durchgezogener Pfeil. Schränkt den Terminplan ein, kann kollidieren, zählt für den kritischen Pfad |
| **Hängt zusammen** | *hängt zusammen mit* (beidseitig) | Blasser Strich |
| **Dupliziert** | *dupliziert* / *wird dupliziert von* | Blasser Strich |
| **Klont** | *klont* / *wird geklont von* | Blasser Strich |
| **Testet** | *testet* / *wird getestet von* | Blasser Strich |
| **Aufteilung** | *aufgeteilt in* / *aufgeteilt aus* | Blasser Strich |
| **Erstellt** | *hat erstellt* / *erstellt von* | Blasser Strich |

Die Richtung zählt bei allen außer *hängt zusammen mit*, das sich von beiden Enden gleich liest. Nimm die Formulierung von dem Vorgang aus, den du gerade offen hast — „HIN-12 **wird blockiert von** HIN-9“ und „HIN-9 **blockiert** HIN-12“ erzeugen exakt dieselbe Verknüpfung.

!!! tip "Blockieren nur für echte Zwänge"
    Es ist verlockend, *blockiert* für „das sollten wir wohl zuerst machen“ zu nehmen. Tu es nicht — es ist die eine Beziehung, die das Diagramm ernst nimmt, und ein Plan voller weicher Blockaden erzeugt Konflikte, die niemand beheben will, und einen kritischen Pfad, der nichts bedeutet. Ist die Reihenfolge eine Vorliebe, nimm *hängt zusammen mit* und schreib die Begründung in einen Kommentar.

!!! note "Beide Enden müssen im Diagramm sein"
    Ein Verbinder braucht zwei Balken, zwischen denen er laufen kann. Verknüpfst du einen Vorgang mit einem ohne Daten — oder mit einem aus einem anderen Projekt — wird nichts gezeichnet, weil der Pfeil nirgends landen kann. Die Verknüpfung existiert weiterhin an beiden Vorgängen, sie hat nur keine Linie. Fehlt eine Abhängigkeit, die du erwartest, prüf zuerst die Daten des anderen Vorgangs.

## Auswählen, was gezeichnet wird

Die Schaltfläche **Verknüpfungen** auf der schwebenden Steuerung öffnet die Ansichtsoptionen. Drei Schalter, jeder sofort wirksam:

| Schalter | Standard | Was gezeichnet wird |
| --- | --- | --- |
| **Abhängigkeiten** | An | Die blockierenden Verknüpfungen — die, die den Terminplan wirklich einschränken |
| **Weitere Verknüpfungen** | Aus | Alle anderen Beziehungen, als blasse Striche |
| **Kritischer Pfad** | Aus | Betonung der längsten Kette von Abhängigkeiten |

Jede Zeile nennt dir, wie viele Verknüpfungen dieser Art das Diagramm überhaupt enthält — du siehst also sofort, ob ein Einschalten etwas ändern würde; „0 blockierende Verknüpfungen in diesem Diagramm“ ist für sich schon eine Antwort. Darunter stehen eine Legende für die vier Linienarten und, falls vorhanden, ein roter Balken mit der Zahl der Terminkonflikte.

Auf breiten Bildschirmen öffnet sich das Panel als Popover neben der Schaltfläche, auf dem Handy fährt es von unten hoch. Es gibt nichts zu bestätigen — jeder Schalter wirkt beim Umlegen.

!!! note "Diese Schalter gehören dir, und sie sind vorübergehend"
    Den kritischen Pfad einzuschalten ändert, was *du* siehst, nicht was andere sehen, und am Projekt ändert sich gar nichts. Die Einstellungen setzen sich außerdem zurück, wenn du die Seite verlässt — die Zeitachse öffnet also immer in ihrem schlichtesten, lesbarsten Zustand.

## Wenn ein Plan nicht aufgeht: Terminkonflikte

Ein **Terminkonflikt** ist eine Abhängigkeit, deren Daten ihr widersprechen: Der blockierte Vorgang soll an oder vor dem Tag beginnen, an dem sein Blockierer endet.

Konkret — *HIN-9 Datenbank migrieren* läuft Montag bis Donnerstag, und *HIN-12 App umstellen* ist als **wird blockiert von** HIN-9 markiert, beginnt aber am Dienstag. Der Plan sagt, HIN-12 wartet auf HIN-9; der Kalender sagt, er beginnt drei Tage zu früh. Beides kann nicht stimmen — und es ist genau der Widerspruch, der jedes Status-Meeting überlebt, bis ihn jemand aufzeichnet.

Die Zeitachse wird deshalb laut, denn ein leiser Konflikt ist ein verpasster Termin drei Wochen später:

- Der Verbinder zwischen beiden Vorgängen wird **rot**.
- Der Balken des blockierten Vorgangs bekommt eine **rote Umrandung**.
- Neben seinem Titel in der Vorgangsspalte erscheint ein **Warndreieck**, mit der Erklärung beim Darüberfahren.
- Das Verknüpfungs-Panel zeigt eine rote Zahl aller Konflikte im Diagramm.

Es gibt nur zwei ehrliche Auswege, und Hinata nimmt dir bewusst keinen davon ab: die Daten so verschieben, dass der blockierte Vorgang nach seinem Blockierer beginnt — oder entscheiden, dass die Abhängigkeit gar keine war, und die Verknüpfung entfernen. Den Vorgang von jemandem still umzuplanen wäre der dritte Weg, und es ist der, der Vertrauen kostet.

## Der kritische Pfad

Schalte **Kritischer Pfad** ein, und die Zeitachse hebt die längste Kette blockierender Abhängigkeiten im Projekt hervor — in Tagen gemessen, vom ersten Vorgang der Kette bis zum letzten. Alles auf dieser Kette trägt einen bernsteinfarbenen Ring.

Was dieser Ring praktisch heißt: **Diese Vorgänge haben keinen Puffer.** Rutscht einer davon um einen Tag, rutscht das Ende der ganzen Kette um einen Tag, weil nichts das abfängt. Vorgänge abseits des kritischen Pfads haben Luft; die darauf nicht. Es ist die kürzeste Antwort auf „wo sollten die zusätzlichen Hände hin?“.

!!! note "Der Pfad ist nur so gut wie die Verknüpfungen"
    Der kritische Pfad wird aus den blockierenden Verknüpfungen zwischen den Vorgängen dieses Diagramms berechnet. Arbeit, die niemand verknüpft hat, und Arbeit, die niemand datiert hat, ist für ihn unsichtbar. Sieht das Ergebnis falsch aus, fehlt meist eine Abhängigkeit, die in jemandes Kopf statt im Vorgang steht.

## Einen Vorgang in den Fokus nehmen

Klick oder tipp einen Balken an, und er ist **angeheftet**: Dieser Vorgang und alles, was eine Verknüpfung entfernt ist, bleiben hell, der Rest des Diagramms wird blass. Es ist der schnellste Weg zur Frage „worauf wartet das, und was wartet darauf?“, ohne jede Zeile zu lesen.

Alle Gesten, die das Diagramm versteht, auf einen Blick:

| Das tust du | Das passiert |
| --- | --- |
| Balken klicken oder antippen | Heftet den Vorgang an — er und seine verknüpften Nachbarn bleiben hell, der Rest wird blass |
| Erneut klicken oder antippen | Hebt die Anheftung auf |
| Auf leeres Raster klicken oder tippen | Hebt sie ebenfalls auf |
| Über einen Balken fahren | Tooltip mit Schlüssel, Status, Fortschritt, allen Beziehungen und einem etwaigen Konflikt |
| Balken lange drücken oder doppelklicken | Öffnet den Vorgang |
| Titel in der linken Spalte anklicken | Öffnet den Vorgang |
| Diagramm ziehen | Scrollt durch die Zeit oder nach unten durch die Vorgänge |

Der Vorgang öffnet sich *über* der Zeitachse statt sie zu ersetzen. Beim Schließen landest du also wieder bei demselben Projekt, demselben Zoom und derselben Scrollposition — und ein geändertes Datum ist bereits neu gezeichnet.

## Die Timeline-Ansicht des Boards

Die Ansicht **Timeline** eines Kanban-Boards ist dasselbe Diagramm, gebaut aus den Vorgängen dieses Boards:

- Alles, was gerade auf dem Board liegt, erscheint — genau so gefiltert, wie du das Board gefiltert hast.
- Vorgänge **ohne** Daten fallen nicht unter den Tisch: Sie stehen unter dem Raster, markiert als ohne Start- oder Fälligkeitsdatum, damit eine Planung sieht, was noch terminiert werden muss.
- Sub-Tasks bleiben außen vor. Sie sind Detail, das in ihren übergeordneten Vorgang gehört, und auf einer Roadmap bringen sie Rauschen statt Information.
- Abhängigkeiten, Konflikte, Meilensteine und der kritische Pfad lesen sich genau wie hier.

## Ein Release planen, von Anfang bis Ende

Die ganze Seite als eine durchgespielte Abfolge. Angenommen, ihr liefert in sechs Wochen.

1. **Zuerst den Meilenstein anlegen.** Leg einen Vorgang *Release 2.4 geht live* an, gib ihm **nur ein Fälligkeitsdatum** — den Liefertag — und kein Startdatum. Er erscheint als Raute an diesem Tag, und alles andere hat jetzt ein Ziel.
2. **Die Arbeit datieren.** Geh die Vorgänge durch, die bis dahin fertig sein müssen, und gib jedem ein Start- und ein Fälligkeitsdatum. Balken tauchen auf. Ob alles passt, ist noch egal.
3. **Verknüpfen, was wirklich wartet.** Für jedes Paar, bei dem eines wirklich nicht beginnen kann, bevor das andere fertig ist, setz eine Verknüpfung **wird blockiert von**. Verknüpf auch das letzte Arbeitspaket mit dem Meilenstein, damit die Raute an der Kette hängt statt daneben zu schweben.
4. **Nach Rot suchen.** Öffne **Verknüpfungen** und lies die Konfliktzahl. Jeder Konflikt ist eine Zusage, die der Kalender nicht halten kann — behebe jeden, indem du ein Datum verschiebst oder zugibst, dass die Abhängigkeit optional war.
5. **Den kritischen Pfad einschalten.** Die bernsteinfarbene Kette ist die Abfolge, die euren Liefertermin bestimmt. Was darauf keine verantwortliche Person hat — oder eine mit drei weiteren bernsteinfarbenen Vorgängen — ist das Risiko, von dem du jetzt sechs Wochen vorher weißt.
6. **Im Monatszoom gegenprüfen.** Tritt einen Schritt zurück und sieh dir die Form an. Eine Wand aus Balken in der letzten Woche ist das klassische Zeichen für optimistische Schätzungen — und auf einen Blick viel leichter zu sehen, als aus einer Liste zu argumentieren.
7. **Wiederkommen.** Weil das Diagramm aus den Vorgängen entsteht, kostet ein erneuter Blick nichts. Wandern die Daten und wird Zeit gebucht, füllen sich die Balken und die Konflikte melden sich von allein.

## Warum steht mein Vorgang nicht auf der Zeitachse?

Fast immer eines von fünf Dingen:

- **Er hat keine Daten.** Die Zeitachse braucht ein Startdatum, ein Fälligkeitsdatum oder beides. Das ist mit Abstand die häufigste Ursache.
- **Er ist archiviert.** Archivierte Vorgänge bleiben absichtlich draußen. Hol ihn zurück, dann ist er wieder da.
- **Du schaust auf ein anderes Projekt.** Die Gantt-Seite zeigt ein Projekt zur Zeit — prüf die Auswahl oben rechts.
- **Es ist ein Sub-Task in der Timeline-Ansicht eines Boards.** Dort bleiben Sub-Tasks außen vor. Auf der Gantt-Seite erscheinen sie, sofern sie datiert sind.
- **Du bist in der Timeline eines Boards und ein Filter versteckt ihn.** Diese Ansicht respektiert die Board-Filter; setz sie zurück und schau erneut.

Und wenn der Vorgang da ist, aber ein **Verbinder** fehlt, liegt es fast immer daran, dass der Vorgang am anderen Ende der Verknüpfung keine Daten hat — es gibt also nichts, wohin der Pfeil zeigen könnte.

## Was die Zeitachse nicht tut

Über die Grenzen Bescheid zu wissen erspart dir die Suche nach einem Bedienelement, das es nicht gibt:

- **Du kannst keinen Balken ziehen, um umzuplanen.** Daten werden am Vorgang bearbeitet, wo die Änderung in seiner Historie landet und alle Beobachtenden davon erfahren. Den Vorgang aus dem Diagramm zu öffnen ist ein langer Druck.
- **Sie zeigt ein Projekt zur Zeit.** Nutz die Projektauswahl zum Wechseln; für eine projektübergreifende Sicht leg die Projekte auf ein gemeinsames Board und nimm dessen Timeline.
- **Sie plant nichts für dich.** Kein automatischer Ausgleich, kein Umplanen zur Konfliktlösung, keine aus Schätzungen erfundenen Daten. Das Diagramm zeigt, was dein Team tatsächlich aufgeschrieben hat — einschließlich der nützlichen Stellen, an denen zwei widersprüchliche Dinge dastehen.

## Wie es weitergeht

- **[Mit Vorgängen arbeiten](/de/guide-issues.html)** — Daten, Verknüpfungen und Hierarchie am Vorgang selbst.
- **[Boards & Sprints](/de/guide-boards.html)** — dieselbe Arbeit nach Status, samt der Timeline-Ansicht des Boards.
- **[Zeit erfassen](/de/guide-time.html)** — Aufwand buchen, was den Fortschritt in einem Balken füllt.
- **[Berichte & Dashboard](/de/guide-reports.html)** — wie der Plan sich gegen das schlägt, was tatsächlich passiert ist.
