---
title: Dinge finden
description: Mit der Befehlspalette in zwei Tastendrücken zu jedem Vorgang, Projekt, Artikel oder jeder Person springen — und mit der Vorgangsliste genau die Menge an Arbeit bauen, die du sehen musst.
---

# Dinge finden

An ein Tracker-System stellst du zwei sehr verschiedene Fragen. Die erste lautet *„Wo ist dieses eine Ding?“* — ein Ticket, das jemand im Meeting erwähnt hat, das Runbook vom letzten Frühjahr, der Name einer Kollegin. Die zweite lautet *„Wie sieht alle Arbeit einer bestimmten Form aus?“* — jeder offene Bug in zwei Projekten, alles, was diese Woche fällig ist, alles, was niemand übernommen hat.

Hinata beantwortet die erste mit der **Befehlspalette** und die zweite mit der Liste **Issues**. Zu wissen, wann du zu welcher greifst, ist der größte Teil der Übung.

## Die Palette von überall öffnen

Drücke **⌘K** auf dem Mac, **Strg+K** unter Windows und Linux. Beide Kombinationen funktionieren auf jeder Plattform — der Hinweis auf dem Bildschirm nennt einfach die Taste, die deine Tastatur tatsächlich hat.

Du kannst auch auf das Feld **Suchen oder springen zu…** in der oberen Leiste klicken. Es sieht aus wie ein Textfeld, verhält sich aber wie ein Knopf: Ein Klick öffnet dieselbe Palette. Auf dem Handy wird aus dem Feld ein Lupensymbol in der oberen Leiste, und die Palette fährt als bildschirmfüllendes Sheet von oben herein, statt mitten im Fenster zu schweben.

Die Palette öffnet sich *über* dem, was du gerade tust. Nichts halb Getipptes geht verloren, nichts scrollt dahinter weg. Drücke **Esc** oder klicke auf den abgedunkelten Hintergrund, und du bist genau dort, wo du warst.

!!! tip "Sie funktioniert auch mitten in etwas"
    Das Tastenkürzel gehört der App selbst, nicht einem bestimmten Bildschirm. Beim Lesen eines Vorgangs, beim Ziehen einer Karte, mitten in einem Kommentar — ⌘K öffnet trotzdem. Die einzige Ausnahme: Liegt bereits ein anderer Dialog obenauf, stapelt die Palette kein zweites Fenster darüber.

![Die Befehlspalette über dem Dashboard, mit gruppierten Ergebnissen für die Suche „board"](/assets/img/shot-search.png)

*Eine Eingabe, alles auf einmal: Jeder Bereichs-Chip trägt seine Anzahl (9 Befehle, 71 Vorgänge, 3 Projekte, 7 Personen), Treffer sind überall hervorgehoben, und jede Vorgangszeile zeigt Schlüssel und Status. Der beste Treffer — der Befehl **Zum Board** — ist bereits ausgewählt, **Enter** würde ihn also öffnen. Die Leiste unten nennt die einzigen drei Tasten, die du brauchst.*

## Was sie durchsucht

Fang an zu tippen, und die Treffer kommen gruppiert an, immer in derselben Reihenfolge, damit dein Auge weiß, wo es hinschauen muss:

| Gruppe | Was passt |
| --- | --- |
| **Befehle** | Aktionen und Ziele in der App — siehe [Sie ist auch eine Befehlsleiste](#sie-ist-auch-eine-befehlsleiste) |
| **Vorgänge** | Titel, Vorgangsschlüssel (`HIN-42`) und Labels — dazu Wörter aus der Beschreibung |
| **Projekte** | Projektname und Projektschlüssel, dazu die Projektbeschreibung |
| **Personen** | Anzeigename, Benutzername und Position |
| **Boards & Sprints** | Board-Namen, Sprint-Namen und Sprint-Ziele |
| **Wissen** | Artikeltitel und Labels, dazu der Text im Artikel |

Zwei Arten von Treffern laufen gleichzeitig, und der Unterschied lohnt sich, weil er Ergebnisse erklärt, die sonst inkonsistent wirken. **Teiltreffer** greifen auf den kurzen Feldern — `len` findet *Lena*, `HIN-2` findet `HIN-241`, ein halber Projektname findet das Projekt. **Ganze Wörter** werden zusätzlich in den langen Feldern gesucht: in Beschreibungen und Artikeltexten. Ein Wortfragment findet also einen Titel, aber nicht den Satz, der in einer Beschreibung steckt; dafür tippst du das ganze Wort.

In der Standardansicht **Alle** zeigt jede Gruppe bis zu fünf Treffer. Wählst du eine einzelne Gruppe, sind es bis zu vierundzwanzig.

## Auf eine Art von Treffern eingrenzen

Die Reihe von Chips unter dem Suchfeld — **Alle**, **Befehle**, **Vorgänge**, **Projekte**, **Personen**, **Boards & Sprints**, **Wissen** — schränkt die Suche auf eine Kategorie ein. Jeder Chip trägt die Anzahl der Objekte dieser Art, die es gibt: ein leises, aber nützliches Gefühl für Größenordnungen.

Klicke einen Chip an oder drücke **Tab**, um vorwärts durch sie zu wandern, und **Umschalt+Tab** zurück. Deine Suchanfrage bleibt dabei im Feld stehen, du kannst also einmal tippen und dann zwischen „meinte ich den Vorgang oder den Artikel?“ hin- und herspringen.

!!! tip "Eine leere Anfrage in einem Bereich ist eine Stöberliste"
    Wähle einen Bereich, ohne etwas zu tippen, und du bekommst die zehn zuletzt bearbeiteten Objekte dieser Art. Das ist der schnellste Weg zurück zu dem, woran das Team heute Morgen gearbeitet hat — ganz ohne ein Wort aus dem Titel zu kennen.

## Alles über die Tastatur

| Taste | Wirkung |
| --- | --- |
| **↑ / ↓** | Durch die Treffer bewegen, über Gruppengrenzen hinweg |
| **↵ Enter** | Ausgewählten Treffer öffnen oder ausgewählten Befehl ausführen |
| **Tab / Umschalt+Tab** | Zum nächsten / vorherigen Bereichs-Chip |
| **Esc** | Palette schließen |

Der beste Treffer ist bereits ausgewählt, wenn die Ergebnisse eintreffen. Der Normalfall lautet also: ⌘K drücken, vier Zeichen tippen, Enter drücken. Auch die Maus wählt eine Zeile aus, wenn du darüberfährst — du kannst also auf der Tastatur anfangen und mit einem Klick enden, ohne dass die Markierung springt.

## Ergebnisse lesen, bevor du sie öffnest

Jede Zeile trägt genug Kontext, um „ist das der richtige?“ zu beantworten, ohne dass du etwas öffnest — und die Form der Zeile verrät, um welche Art Objekt es sich handelt:

- **Ein Vorgang** zeigt sein Typ-Symbol, seinen Schlüssel in Monospace, einen farbigen Statuspunkt samt Statusnamen und rechts das Avatar der zugewiesenen Person. Drei Tickets mit fast identischem Titel unterscheidest du direkt in der Liste an Status und Besitzer.
- **Ein Projekt** zeigt ein farbiges Sechseck mit dem Projektschlüssel, wie viele Vorgänge offen und wie viele erledigt sind, und die Gesichter seiner Mitglieder.
- **Eine Person** zeigt Avatar und Position.
- **Ein Board oder Sprint** zeigt seinen Namen und beim Sprint zusätzlich sein Ziel — das erkennt man meist besser als die Sprint-Nummer.
- **Ein Artikel** zeigt, in welchem Bereich er liegt und wann er zuletzt aktualisiert wurde. Ein veraltetes Duplikat fällt so auf, bevor du es liest.

## Letzte Suchen

Öffne die Palette mit leerem Feld, und sie zeigt deine **letzten Suchen** — die letzten sechs Begriffe, die du tatsächlich benutzt hast, der jüngste zuerst. Ein Klick setzt den Begriff zurück ins Feld und führt ihn erneut aus; er springt nicht direkt zu einem Treffer, denn eine Suche, die du wiederholst, willst du meistens noch einmal durchsehen.

Die Liste liegt auf dem Gerät, an dem du sitzt — Handy und Laptop merken sich also Verschiedenes. **Leeren** räumt sie ab.

## Sie ist auch eine Befehlsleiste

Die Palette ist nicht nur ein Suchfeld. Tippe, was du *tun* willst, und sie bietet es an:

- **Zum Dashboard**, **Zu Projekte**, **Zu Vorgänge**, **Zum Board**, **Zur Timeline**, **Zu Berichte**, **Zu Wissen** — die ganze Navigation, ohne auf die Seitenleiste zu zielen.
- **Neuen Vorgang erstellen** — bringt dich aufs Board, wo jede Spalte an ihrem Fuß ein **Aufgabe hinzufügen**-Eingabefeld trägt.
- **Hell / Dunkel umschalten** — dreht das Erscheinungsbild. Dieser Befehl lässt die Palette bewusst offen, damit du das Ergebnis ansiehst und bei Nichtgefallen sofort zurückschaltest.

Befehle werden auf deinem Gerät abgeglichen und erscheinen sofort, noch bevor der Server antwortet. Die Beschriftung musst du nicht exakt treffen: *„dunkel“*, *„Erscheinungsbild“* und *„Hell“* finden alle denselben Schalter.

## Woher die Antworten kommen

Alles, was die Palette zeigt, kommt von deinem eigenen Server. Es gibt keinen externen Suchindex, nichts wird woandershin geschickt, und die Treffer sind so frisch wie die Daten — ein Vorgang, den jemand vor einer Minute umbenannt hat, ist unter seinem neuen Titel auffindbar.

Die App wartet nach deinem letzten Tastendruck einen Sekundenbruchteil, bevor sie fragt, und wirft Antworten weg, die ein neuerer Tastendruck bereits überholt hat. Deshalb setzen sich die Ergebnisse einen Wimpernschlag nach dem Tippen, statt durch jedes Zwischenwort zu flackern — und deshalb lässt dich eine langsame Verbindung nie auf die Treffer für `Kar` schauen, während du längst `Karbon` getippt hast.

Die Ausnahme sind Befehle: Sie werden auf deinem Gerät abgeglichen und erscheinen im selben Moment, in dem du tippst.

## Wenn nichts zurückkommt

Sagt die Palette, sie habe keine Treffer, arbeite das der Reihe nach ab:

1. **Ist noch ein Bereichs-Chip aktiv?** Ein Chip, den du vorhin gedrückt hast, bleibt gedrückt. **Alle** macht wieder weit.
2. **Ist es ein Fragment eines langen Wortes?** Fragmente greifen auf Titeln, Schlüsseln und Labels — nicht im Text von Beschreibungen und Artikeln. Versuche das ganze Wort.
3. **Ist es archiviert?** Stelle der Anfrage `archiviert` voran.
4. **Liegt es in einem Projekt, das du erreichst?** Zugriff auf Projekte kommt aus deiner Projektmitgliedschaft und aus deinen Teams. Wenn eine Kollegin etwas sieht, das du nicht siehst, ist das der Grund — lass dich hinzufügen oder lies [Projekte & Teams](/de/guide-projects.html).

## Die Palette auf dem Handy

Auf dem Handy nimmt die Palette den ganzen Bildschirm ein und fährt von oben herein: das Feld oben unter deinem Daumen, die Tastatur schon offen. Die Bereichs-Chips scrollen seitwärts, die Treffer füllen den Rest, und die Fußzeile mit den Tastaturhinweisen entfällt — es gibt ja keine Tastatur, auf die sie hinweisen könnte. Alles andere — Bereiche, letzte Suchen, das Archiv-Stichwort, Befehle — verhält sich genau wie am Schreibtisch. Mehr zum Handy-Layout in [Auf dem Handy](/de/guide-mobile.html).

## Sechs Dinge, die Leute wirklich suchen

**„Jemand hat HIN-42 erwähnt, das will ich lesen.“**
Tippe den Schlüssel. Groß- und Kleinschreibung ist egal, und du brauchst ihn nicht ganz — `hin-4` grenzt schon ein. Enter auf dem obersten Treffer.

**„Ich erinnere mich an einen Satz aus der Beschreibung, nicht an den Titel.“**
Tippe den Satz als ganze Wörter. Beschreibungen und Artikeltexte werden mitdurchsucht, *„Zertifikat Rotation“* findet also das Ticket, dessen Titel davon nichts sagt. Kommt nichts zurück, reduziere auf das eine markanteste Wort — in den langen Feldern wird Wort für Wort gesucht, nicht Fragment für Fragment.

**„Ich will alles aus einem Projekt.“**
Suche das Projekt über seinen Namen, drücke Enter, und du landest in der Issues-Liste, bereits auf dieses Projekt gefiltert. Von dort schneidest du sie mit **Filter** und **Gruppieren nach** zurecht.

**„Das hat doch niemand übernommen, oder?“**
Öffne **Issues**, dann **Filter → Zugewiesen → Nicht zugewiesen**. Nimm **Status** dazu, wenn dich nur bereits begonnene Arbeit interessiert. Das ist die Abfrage, die findet, was still am Boden des Backlogs vor sich hin gammelt.

**„Was habe ich letzte Woche angefasst?“**
**Filter → Zugewiesen → du**, **Sortieren → Änderungsdatum (neu)**, **Zeitraum → Letzte 7 Tage**. Gruppiere nach Projekt, wenn du über mehrere hinweg arbeitest und die Antwort nach Bereichen getrennt willst.

**„Das wurde gelöscht — oder doch nicht?“**
Was du archivierst, ist nie wirklich weg. Tippe `archiviert` und dahinter, was du suchst — `archiviert Login Bug` — und die Palette durchsucht das Archiv statt des aktiven Workspace: archivierte Vorgänge und archivierte Projekte. Tippe `archiviert` allein, um die zuletzt archivierten Objekte zu sehen. Das englische Wort `archived` funktioniert genauso, egal in welcher Sprache deine App läuft.

!!! note "Archivierte Vorgänge tragen ein Abzeichen"
    Treffer aus dem Archiv sind markiert, du verwechselst ein archiviertes Ticket also nie mit einem aktiven. Wiederhergestellt wird es aus dem Vorgang selbst — siehe [Mit Vorgängen arbeiten](/de/guide-issues.html).

## Vorgangsschlüssel sind Adressen

Jeder Vorgang hat einen kurzen, dauerhaften Schlüssel: Projektschlüssel, Bindestrich, Nummer — `HIN-42`. Genau den paste man in eine Chat-Nachricht, eine Commit-Message oder ein Dokument, weil er kurz genug ist, um ihn vorzulesen, und auf dem ganzen Server eindeutig.

In der Web-App kommst du direkt über `…/browse/HIN-42` zu diesem Vorgang. In der Desktop- und der Handy-App erledigt der Schlüssel in der Palette dasselbe mit weniger Tastendrücken.

Schlüssel überleben einen Umzug. Wird ein Vorgang in ein anderes Projekt verschoben, bekommt er eine neue Nummer — aber der alte Schlüssel funktioniert weiter: in der Palette, in `browse`-Links und in jedem Artikel und jedem Vorgang, der ihn schon referenziert. Ein Link, den du vor einem Jahr geschrieben hast, verrottet nicht, nur weil jemand die Projekte umsortiert hat.

!!! tip "Klicke den Schlüssel, um einen Link zu kopieren"
    Klickst du bei einem geöffneten Vorgang auf seinen Schlüssel, landet ein teilbarer Link in der Zwischenablage — beim Darüberfahren erscheint ein Kopiersymbol, und der Schlüssel bestätigt anschließend. Dieser Link löst in beide Richtungen auf: Wo die App installiert ist, öffnet er den Vorgang in der App, sonst im Browser.

## Wenn du eine Liste brauchst, keinen Sprung

Die Seite **Issues** ist die andere Hälfte des Findens. Sie zeigt jeden Vorgang aus jedem Projekt, auf das du Zugriff hast, zuletzt bearbeitete zuerst, und lädt beim Scrollen nach. Vier Bedienelemente formen sie.

![Die Issues-Liste mit Gruppieren nach, Sortieren, Filter und Zeitraum über der Tabelle](/assets/img/shot-issues.png)

*Die Seite Issues: 71 Aufgaben aus allen sichtbaren Projekten, die vier Ansichts-Bedienelemente über der Tabelle und rechts Exportieren. Das Feld **Suchen oder springen zu…** mit seinem ⌘K-Abzeichen sitzt auf jedem Bildschirm in der oberen Leiste.*

### Eine Zeile lesen

Jede Zeile ist ein Vorgang: sein **Schlüssel**, der **Titel** mit einem Symbol für seinen Typ, sein **Status**, seine **Priorität**, seine zugewiesene Person und sein **Fälligkeitsdatum**. Zwei dieser Spalten arbeiten mehr, als sie aussehen:

- **Fällig** spricht relativ, solange das hilft, und in Daten, sobald es das nicht mehr tut — *3 T. überfällig* und *Heute* in Rot, dann *Morgen*, dann *in 5 T.* für alles innerhalb der kommenden Woche, danach ein schlichtes Datum. Du kannst hundert Zeilen nach Ärger absuchen, ohne ein einziges Kalenderdatum zu lesen.
- **Titel** trägt einen kleinen Zähler, wenn der Vorgang Sub-Tasks hat — `0/1`, `3/4` — damit ein Elternvorgang, der fertig aussieht, es aber nicht ist, das sagt, bevor du ihn öffnest.

Ein Klick irgendwo auf die Zeile öffnet den Vorgang.

### Die Liste formen

**Filter** öffnet ein Popover mit fünf Facetten — **Status**, **Priorität**, **Zugewiesen**, **Projekt** und **Typ** — dazu einen Schalter **Archiviert**. Innerhalb einer Facette sind die Auswahlen Alternativen: *Bug* und *Task* zeigt beides. Zwischen Facetten addieren sie sich: *Bug* plus *In Arbeit* plus *Lena* zeigt nur Lenas laufende Bugs. Der Knopf trägt einen Zähler, solange etwas aktiv ist, und **Zurücksetzen** räumt auf.

**Gruppieren nach** teilt die Liste in beschriftete Abschnitte — nach Status, Priorität, zugewiesener Person, Projekt oder Typ. Vor dem Daily nach Person gruppiert, wird aus der Liste eine Agenda pro Kopf; nach Projekt gruppiert, eine Portfolio-Ansicht.

**Sortieren** ordnet die gesamte Ergebnismenge, nicht nur die Zeilen, bis zu denen du gescrollt hast: neueste zuerst, älteste zuerst oder nach Änderungsdatum in beide Richtungen. Voreingestellt ist zuletzt bearbeitet zuerst.

**Zeitraum** grenzt nach Datum ein — **Überfällig**, **Bis heute fällig**, **Heute**, **Diese Woche**, **Dieser Monat**, die letzten oder nächsten 7 und 30 Tage oder ein **Eigener Zeitraum…** aus dem Kalender. Er liest Daten so, wie du es tätest: Ein Vorgang mit Start *und* Fälligkeit passt, wenn seine Spanne das Fenster überlappt; einer mit nur einem der beiden passt, wenn dieses Datum im Fenster liegt; einer ohne beides fällt auf seine letzte Aktivität zurück, damit ungeplante Arbeit trotzdem auftaucht.

!!! note "Filter halten für den Besuch, nicht für immer"
    Gespeicherte Ansichten gibt es noch nicht. Was du einstellst, bleibt, bis du die Seite verlässt; beim nächsten Mal öffnet die Liste ungefiltert. Für eine Ansicht, die du täglich brauchst, behalte den Link — siehe unten — oder baue sie als [Board](/de/guide-boards.html), das seine Konfiguration sehr wohl behält.

## Filter, die mit dem Link kommen

Manche Links bringen ihren Filter mit. Die Kacheln auf deinem Dashboard sind das klarste Beispiel: Ein Klick auf **Heutige Aufgaben** öffnet die Issues-Liste bereits auf das eingegrenzt, was bis heute fällig ist — und die Zahl, die du angeklickt hast, entspricht der Zahl der Zeilen, die du bekommst. Über eine Projektkarte gilt dasselbe für dieses Projekt.

In der Web-App trägt die Adresszeile diesen Zuschnitt mit, ein Link, den du von dort kopierst, öffnet sich bei Kolleginnen also genauso gefiltert wie bei dir.

## Ergebnisse mitnehmen

**Exportieren** schreibt die vollständige gefilterte Menge, nicht nur die Zeilen, die du hereingescrollt hast — die App blättert zuerst die ganze Ergebnismenge auf dem Server durch. Du hast die Wahl:

- **Als PDF exportieren** — eine druckbare Tabelle mit Name und Logo deiner Organisation.
- **Als CSV exportieren** — für die Tabellenkalkulation.
- **Als JSON exportieren** — für alles, was es wieder einlesen soll.

Die Datei landet in deinem Downloads-Ordner, und die App nennt dir den verwendeten Dateinamen.

## Über die Hierarchie navigieren statt suchen

Manches läuft man schneller ab, als man es sucht. Arbeit ist in Hinata drei Ebenen tief verschachtelt — ein **Epic** hält Stories, Tasks, Bugs und Features, und jedes davon kann **Sub-Tasks** halten — und jede Ebene ist begehbar:

- Jeder Vorgang zeigt über seinem Titel einen **Breadcrumb**. Die übergeordneten Einträge sind anklickbar: ein Sprung von einem Sub-Task zum Elternvorgang, noch einer zum Epic, das beide rahmt.
- Ein Elternvorgang listet seine **untergeordneten Vorgänge** und seine **Sub-Tasks** in eigenen Panels, mit Fortschrittszähler. Wer das Epic kennt, muss darin nie etwas suchen.
- Auf dem Board macht **Gruppieren nach → Epic** aus den Spalten Swimlanes, eine pro Epic. Das ist der schnellste Blick auf eine ganze Initiative — inklusive der Teile, an denen niemand arbeitet.

Und wenn du etwas doch an einen Elternvorgang hängst, öffnen die Epic- und Eltern-Auswahl mit **Letzte Epics** und **Aktuelle Vorgänge** — meistens ist das Gesuchte einer der letzten, die du angefasst hast.

## Nach einer Person suchen

Personentreffer passen auf Anzeigename, Benutzername und Position — *„Vogt“*, *„lvogt“* und *„Designerin“* finden also dieselbe Kollegin. Ein schneller Weg, um zu klären, wer eine Rolle innehat, die du nur der Beschreibung nach kennst.

Um die *Arbeit* einer Person zu sehen statt ihres Profils, geh andersherum vor: **Issues** öffnen, nach **Zugewiesen** filtern und nach Projekt oder Status gruppieren. Der **Personen**-Filter des Boards tut dasselbe für ein einzelnes Board — und das ist meistens genau das, was ein Daily braucht.

!!! note "Eine Person zu öffnen braucht Adminrechte"
    Ein Personentreffer führt in die Benutzerverwaltung, die nur Administratorinnen und Administratoren öffnen können. Finden können alle Personen; die Verzeichnisseite öffnen nicht.

## Einmal verlinken, seltener suchen

Die beste Suche ist die, die du nie ausführen musst. Wann immer du eine Beschreibung, einen Kommentar oder einen Artikel schreibst: Tippe **@** und wähle den Vorgang, den Artikel oder die Person, die du meinst. Was im Text landet, ist ein lebendiger Link: Er zeigt den echten Titel und Status des Vorgangs, er öffnet ihn beim Klick, und er speist die Panels, die Dinge verbinden — **Verknüpfte Aufgaben** am Fuß eines Artikels, **Dokumentiert in** am Vorgang selbst.

`HIN-42` als bloße Zeichen zu tippen bringt nichts davon. Es ist lesbar, und jemand kann es in die Palette kopieren, aber die beiden Dinge bleiben Fremde. Ein einziger Tastendruck macht aus einer Erwähnung eine Verbindung, und der zahlt sich jedes Mal aus, wenn jemand anderes suchen geht. Was diese Links können, sobald es sie gibt, steht in [Dokumentation schreiben](/de/guide-knowledge.html).

## Suchen an anderen Stellen

Suche wohnt nicht nur in der Palette:

- Das **Board** hat einen eigenen Filter mit Facetten, die die globale Liste nicht braucht — Sprint, Autor, Stichwort und Epic — dazu einen Personen-Filter, um auf ein oder zwei Kolleginnen einzugrenzen. Siehe [Boards & Sprints](/de/guide-boards.html).
- Die **Wissensdatenbank** hat über ihrem Bereichsraster ein eigenes Suchfeld für Artikeltitel, Bereichsnamen und Labels. Siehe [Dokumentation schreiben](/de/guide-knowledge.html).
- **Beobachtet** sammelt die Vorgänge, denen du folgst — oft der kürzeste Weg zurück in laufende Arbeit. Siehe [Auf dem Laufenden bleiben](/de/guide-notifications.html).
- In einem Vorgang durchsucht das **@**-Menü Vorgänge, Artikel und Personen, damit du beim Schreiben das eine mit dem anderen verknüpfst.

!!! tip "Die Faustregel"
    Kannst du das Ding benennen, nimm ⌘K. Kannst du es nur beschreiben — *offen, meine, überfällig* — nimm die Issues-Liste. Brauchst du es morgen wieder, mach ein Board daraus.

## Nächste Schritte

- Was du mit dem Gefundenen anstellst, steht in [Mit Vorgängen arbeiten](/de/guide-issues.html).
- Dieselbe Arbeit visuell formen: [Boards & Sprints](/de/guide-boards.html).
- Schreibe das Runbook, das die Palette beim nächsten Mal findet: [Dokumentation schreiben](/de/guide-knowledge.html).
