---
title: Timeline & Abhängigkeiten
description: Dein Projekt als Gantt-Diagramm lesen, Abhängigkeiten ziehen und Terminkonflikte finden.
---

# Timeline & Abhängigkeiten

Die Zeitachse zeigt, *wann* Arbeit passiert: als Balken im Kalender, mit Abhängigkeiten und Warnungen bei Terminkonflikten.

Sie **speichert nichts Eigenes**. Balken sind Startdatum und Fälligkeitsdatum eines Vorgangs, Pfeile sind Verknüpfungen. Änderst du das am Vorgang, ändert sich das Diagramm.

## Die Zeitachse öffnen

- **Gantt** in der Seitenleiste öffnet die Seite **Zeitachse** für ein Projekt. Oben rechts wählst du das Projekt. Du siehst nur Projekte, in denen du Mitglied bist (siehe [Projekte & Teams](/de/guide-projects.html)).
- Die Ansicht **Timeline** auf einem Kanban-Board zeigt nur die Vorgänge dieses Boards, mit dessen Filtern (siehe [Boards & Sprints](/de/guide-boards.html)).

## Was du da vor dir hast

![Die Hinata-Zeitachse](/assets/img/shot-gantt.png)
*Vorgänge links, heute blau markiert, Meilensteine als Rauten, ein Konflikt in Rot.*

- **Vorgangsspalte** links: Typ, Schlüssel, Titel. Bleibt beim Scrollen stehen, Klick öffnet den Vorgang.
- **Datumsachse** oben: Monate, im Zoom **Woche** auch Tage. Wochenenden sind hinterlegt.
- **Heute**: eingekreist und als senkrechte Linie. Beim Öffnen scrollt das Diagramm dorthin.
- **Schwebende Steuerung** unten rechts: **Verknüpfungen**, **Heute**, **Woche** und **Monat**. Auf dem Handy nur als Symbole.

Das Diagramm scrollt seitwärts durch die Zeit und nach unten durch die Vorgänge.

### Zwischen Wochen und Monaten zoomen

- **Woche**: eine Spalte pro Tag, Schlüssel im Balken. Für die Tagesplanung.
- **Monat**: eine Spalte pro Monat, ohne Beschriftung im Balken. Ein Jahr auf einem Bildschirm.
- **Heute** springt in beiden Stufen zurück.

Die Zeilen sind nach Startdatum sortiert.

## Was einen Vorgang auf die Zeitachse bringt

Ein Vorgang jeden Typs erscheint, sobald er **ein Startdatum, ein Fälligkeitsdatum oder beides** hat und nicht archiviert ist. Ist die Zeitachse leer, zeigt sie dir, was zu tun ist.

### Die Daten setzen

In der Karte **Timeline** am Vorgang: **Startdatum** ist der erste, **Fälligkeitsdatum** der letzte Tag, einschließlich.

![Der Datumsauswähler, geöffnet aus der Timeline-Karte eines Vorgangs](/assets/img/shot-issue-dates.png)
*Tipp auf die Beschriftung öffnet den Kalender, das × löscht das Datum sofort.*

Aus dem Diagramm: Balken lange drücken oder Titel links anklicken. Der Vorgang öffnet sich darüber. Nach dem Schließen bleiben Zoom und Scrollposition.

!!! tip "Zwei Daten für Arbeit, eines für einen Termin"
    Für einen Zeitraum beide Daten setzen, für einen Stichtag nur das Fälligkeitsdatum.

## Einen Balken lesen

- **Länge**: Startdatum bis Fälligkeitsdatum, beide eingeschlossen. Montag bis Freitag sind fünf Tage.
- **Farbe**: der Status, wie auf dem Board. Erledigte Vorgänge bekommen die Farbe für erledigt, ein fertiger Plan wird grün.
- **Hellere Füllung**: der Fortschritt, also **gebuchte Zeit im Verhältnis zur Schätzung** (2 von 4 Stunden sind 50 %). Offene Vorgänge zeigen höchstens 99 %, erst erledigt 100 %. Ohne Schätzung 0 %.

Ein leerer Balken heißt also „nicht angefangen“ oder „nicht geschätzt“. Zeit buchen: [Zeit erfassen](/de/guide-time.html).

!!! tip "Füllung mit heute vergleichen"
    Nach einem Drittel der Zeit 80 % voll: Schätzung zu klein. Kurz vor Schluss kaum gefüllt: Die Arbeit hat nicht richtig begonnen.

Der Tooltip beim Überfahren zeigt Schlüssel, Status, Prozent, Beziehungen und eine Warnung bei Konflikt.

### Daten, Schätzungen und Story Points sind drei verschiedene Dinge

| Was du setzt | Was es bedeutet | Wo es auftaucht |
| --- | --- | --- |
| **Start- & Fälligkeitsdatum** | *Wann* die Arbeit stattfindet | Balken auf der Zeitachse, Spalte „Fällig“, rotes Datum bei Überfälligkeit |
| **Schätzung & gebuchte Zeit** | *Wie viel Aufwand* nötig ist und war | Füllung im Balken, „aufgewendet von“ am Vorgang, Stundenzettel |
| **Story Points** | *Wie groß* er relativ ist | Sprintkapazität, Burndown, Velocity, nie die Zeitachse |
| **Sprint** | *Welches Zeitfenster* er belegt | Board und Backlog, nie die Zeitachse |

## Ein Fälligkeitsdatum allein ist ein Meilenstein

Nur Fälligkeitsdatum, kein Startdatum: Der Vorgang wird als **Raute** gezeichnet, umrandet solange offen, gefüllt wenn erledigt. Gut für Launch, Übergabe oder Prüfung. Verknüpf die vorherige Arbeit damit, dann zeigen Pfeile darauf.

## Eine Abhängigkeit ziehen

Eine **Abhängigkeit**: Vorgang B kann erst beginnen, wenn A fertig ist. Im Diagramm ein durchgezogener Pfeil vom rechten Ende von A zum linken Ende von B.

1. Vorgang öffnen, Abschnitt **Verknüpfte Vorgänge**.
2. **Vorgang hinzufügen**, Art **wird blockiert von** oder **blockiert** wählen.
3. Vorgänge suchen (auch mehrere), **Verknüpfen**.

![Das Verknüpfungsfeld an einem Vorgang](/assets/img/shot-issue-link-composer.png)
*Verknüpfungsart links, Suche nach Titel oder Schlüssel rechts.*

Die Verknüpfung erscheint sofort an beiden Vorgängen und auf der Zeitachse.

### Jede Beziehung und was das Diagramm damit macht

Nur *blockiert* bestimmt die Reihenfolge. Alle anderen Arten sind blasse Striche und standardmäßig ausgeblendet.

![Die Auswahlliste der Verknüpfungsarten](/assets/img/shot-issue-link-types.png)
*Jede Richtung ist ein eigener Eintrag, die Liste scrollt.*

| Verknüpfungsart | Liest sich als | Auf der Zeitachse |
| --- | --- | --- |
| **Blockiert** | *blockiert* / *wird blockiert von* | Durchgezogener Pfeil. Schränkt den Terminplan ein, kann kollidieren, zählt für den kritischen Pfad |
| **Hängt zusammen** | *hängt zusammen mit* (beidseitig) | Blasser Strich |
| **Dupliziert** | *dupliziert* / *wird dupliziert von* | Blasser Strich |
| **Klont** | *klont* / *wird geklont von* | Blasser Strich |
| **Testet** | *testet* / *wird getestet von* | Blasser Strich |
| **Aufteilung** | *aufgeteilt in* / *aufgeteilt aus* | Blasser Strich |
| **Erstellt** | *hat erstellt* / *erstellt von* | Blasser Strich |

„HIN-12 **wird blockiert von** HIN-9“ und „HIN-9 **blockiert** HIN-12“ sind dieselbe Verknüpfung.

!!! tip "Blockieren nur für echte Zwänge"
    Für eine bloße Wunschreihenfolge nimm *hängt zusammen mit*. Sonst entstehen sinnlose Konflikte und ein falscher kritischer Pfad.

!!! note "Beide Enden müssen im Diagramm sein"
    Hat der andere Vorgang keine Daten oder liegt er in einem anderen Projekt, fehlt der Pfeil. Die Verknüpfung existiert trotzdem.

## Auswählen, was gezeichnet wird

**Verknüpfungen** öffnet drei Schalter, die sofort wirken. Auf breiten Bildschirmen als Popover, auf dem Handy von unten.

![Das Panel „Verknüpfungen“ der Zeitachse](/assets/img/shot-gantt-links.png)
*„Abhängigkeiten“, „Weitere Verknüpfungen“ und „Kritischer Pfad“, jeweils mit Anzahl im Diagramm.*

!!! note "Die Schalter gelten nur für dich"
    Sie ändern nur deine Ansicht und setzen sich beim Verlassen der Seite zurück.

## Wenn ein Plan nicht aufgeht: Terminkonflikte

Ein **Terminkonflikt**: Der blockierte Vorgang beginnt an oder vor dem Tag, an dem sein Blockierer endet.

![Ein Terminkonflikt auf der Zeitachse](/assets/img/shot-gantt-conflict.png)
*HIN-7 beginnt, bevor der blockierende HIN-6 endet.*

Du erkennst ihn am roten gestrichelten Pfeil, der roten Umrandung, dem Warndreieck in der Vorgangsspalte und am Tooltip („Beginnt, bevor der blockierende Vorgang abgeschlossen ist“). Das Panel **Verknüpfungen** zählt die Konflikte.

Hinata löst sie nicht selbst. Verschieb die Daten oder entferne die Verknüpfung.

## Der kritische Pfad

**Kritischer Pfad** hebt die längste Kette blockierender Abhängigkeiten hervor, gemessen in Tagen.

![Der kritische Pfad auf der Zeitachse](/assets/img/shot-gantt-critical-path.png)
*Die Kette HIN-4 → HIN-2 → HIN-5 → HIN-6 → HIN-7 → HIN-8 in Bernstein.*

**Diese Vorgänge haben keinen Puffer.** Verzögert sich einer um einen Tag, verzögert sich das Ende der Kette. Zusätzliche Leute helfen hier am meisten.

!!! note "Der Pfad ist nur so gut wie die Verknüpfungen"
    Er kennt nur blockierende Verknüpfungen zwischen datierten Vorgängen in diesem Diagramm.

## Einen Vorgang in den Fokus nehmen

| Das tust du | Das passiert |
| --- | --- |
| Balken klicken oder antippen | Heftet den Vorgang an. Er und seine verknüpften Nachbarn bleiben hell, der Rest wird blass |
| Erneut klicken oder antippen | Hebt die Anheftung auf |
| Auf leeres Raster klicken oder tippen | Hebt sie ebenfalls auf |
| Über einen Balken fahren | Tooltip mit Schlüssel, Status, Fortschritt, Beziehungen und Konflikt |
| Balken lange drücken oder doppelklicken | Öffnet den Vorgang |
| Titel in der linken Spalte anklicken | Öffnet den Vorgang |
| Diagramm ziehen | Scrollt durch Zeit oder Vorgänge |

Der Vorgang öffnet sich über der Zeitachse. Danach sind Projekt, Zoom und Scrollposition unverändert.

## Die Timeline im Board

Wie diese Seite, aber mit den Vorgängen und Filtern des Boards. Unterschiede: Vorgänge ohne Daten stehen unter dem Raster, Sub-Tasks fehlen.

## Ein Release planen, von Anfang bis Ende

1. **Meilenstein**: Vorgang *Release 2.4 geht live* mit nur einem Fälligkeitsdatum.
2. **Daten**: Jedem nötigen Vorgang Startdatum und Fälligkeitsdatum geben.
3. **Abhängigkeiten**: **wird blockiert von** setzen, wo etwas warten muss. Das letzte Arbeitspaket mit dem Meilenstein verknüpfen.
4. **Konflikte**: In **Verknüpfungen** die Zahl prüfen und jeden lösen.
5. **Kritischer Pfad**: Vorgänge darauf ohne verantwortliche Person oder bei überlasteten Personen sind euer Risiko.
6. **Zoom Monat**: Viele Balken in der letzten Woche deuten auf zu optimistische Schätzungen.
7. **Regelmäßig reinschauen**: Das Diagramm aktualisiert sich von selbst.

## Warum steht mein Vorgang nicht auf der Zeitachse?

- Er hat keine Daten (häufigste Ursache).
- Er ist archiviert.
- Oben rechts ist ein anderes Projekt gewählt.
- Er ist ein Sub-Task und du bist in der Timeline eines Boards.
- Ein Filter im Board versteckt ihn.

Fehlt nur ein Pfeil, hat meist der andere Vorgang keine Daten.

## Was die Zeitachse nicht tut

- **Balken ziehen**: geht nicht. Daten änderst du am Vorgang, dort landen sie im Verlauf und Beobachtende werden benachrichtigt.
- **Mehrere Projekte**: nur über ein gemeinsames Board und dessen Timeline.
- **Automatisch planen**: Hinata gleicht keine Auslastung aus, verschiebt keine Termine und leitet keine Daten aus Schätzungen ab.

## Wie es weitergeht

- **[Mit Vorgängen arbeiten](/de/guide-issues.html)**: Daten, Verknüpfungen, Hierarchie
- **[Boards & Sprints](/de/guide-boards.html)**: Arbeit nach Status, Timeline im Board
- **[Zeit erfassen](/de/guide-time.html)**: Aufwand buchen für den Fortschritt
- **[Berichte & Dashboard](/de/guide-reports.html)**: Plan gegen Wirklichkeit
