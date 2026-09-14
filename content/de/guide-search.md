---
title: Dinge finden
description: Mit der Befehlspalette schnell zu Vorgängen, Projekten, Artikeln und Personen springen und mit der Vorgangsliste passende Arbeit filtern.
---

# Dinge finden

Zum Finden gibt es in Hinata zwei Werkzeuge:

- **Befehlspalette:** wenn du ein bestimmtes Ding suchst, etwa ein Ticket, ein Runbook oder eine Person.
- **Liste Issues:** wenn du alle Arbeit mit bestimmten Merkmalen sehen willst, etwa alle offenen Bugs oder alles, was diese Woche fällig ist.

## Die Palette von überall öffnen

Drücke **⌘K** auf dem Mac oder **Strg+K** unter Windows und Linux. Beide Kürzel gehen auf jeder Plattform. Der Hinweis auf dem Bildschirm zeigt die Taste deiner Tastatur.

Alternativ klickst du oben auf **Suchen oder springen zu…**. Das Feld öffnet dieselbe Palette. Auf dem Handy ist es ein Lupensymbol, und die Palette füllt den ganzen Bildschirm.

Die Palette liegt über deiner aktuellen Seite. Halb Getipptes bleibt erhalten. Mit **Esc** oder einem Klick auf den dunklen Hintergrund bist du wieder dort, wo du warst.

!!! tip "Sie funktioniert auch mitten in etwas"
    Das Kürzel gilt in der ganzen App: beim Lesen eines Vorgangs, beim Ziehen einer Karte, mitten in einem Kommentar. Nur wenn schon ein anderer Dialog offen ist, öffnet sich die Palette nicht zusätzlich.

![Die Befehlspalette über dem Dashboard, mit gruppierten Ergebnissen für die Suche „board"](/assets/img/shot-search.png)
*Eine Suche, gruppierte Treffer: Die Chips zeigen Anzahlen, und __Enter__ öffnet die ausgewählte Zeile.*

## Was sie durchsucht

Die Treffer kommen gruppiert, immer in derselben Reihenfolge:

| Gruppe | Was passt |
| --- | --- |
| **Befehle** | Aktionen und Ziele in der App, siehe [Sie ist auch eine Befehlsleiste](#sie-ist-auch-eine-befehlsleiste) |
| **Vorgänge** | Titel, Vorgangsschlüssel (`HIN-42`) und Labels, dazu Wörter aus der Beschreibung |
| **Projekte** | Projektname und Projektschlüssel, dazu die Projektbeschreibung |
| **Personen** | Anzeigename, Benutzername und Position |
| **Boards & Sprints** | Board-Namen, Sprint-Namen und Sprint-Ziele |
| **Wissen** | Artikeltitel und Labels, dazu der Text im Artikel |

So wird gesucht:

- **Kurze Felder** (Titel, Schlüssel, Namen, Labels) finden auch Teile. `len` findet *Lena*, `HIN-2` findet `HIN-241`.
- **Lange Felder** (Beschreibungen, Artikeltexte) finden nur ganze Wörter. Für einen Satz aus einer Beschreibung tippst du also ganze Wörter.

Unter **Alle** zeigt jede Gruppe bis zu fünf Treffer. In einer einzelnen Gruppe sind es bis zu vierundzwanzig.

## Auf eine Art von Treffern eingrenzen

Die Chips unter dem Suchfeld beschränken die Suche auf eine Kategorie: **Alle**, **Befehle**, **Vorgänge**, **Projekte**, **Personen**, **Boards & Sprints**, **Wissen**.

![Die Palette mit gewähltem Bereich „Wissen“ und leerem Suchfeld](/assets/img/shot-search-scope-knowledge.png)
*Bereich __Wissen__ bei leerem Feld: die zuletzt bearbeiteten Artikel mit Bereich und Alter.*

Klicke einen Chip an oder wechsle mit **Tab** vorwärts und **Umschalt+Tab** zurück. Deine Suche bleibt dabei im Feld stehen.

!!! tip "Eine leere Anfrage in einem Bereich ist eine Stöberliste"
    Ohne Suchbegriff zeigt ein Bereich die zuletzt bearbeiteten Einträge. So findest du wieder, woran das Team heute gearbeitet hat.

## Alles über die Tastatur

| Taste | Wirkung |
| --- | --- |
| **↑ / ↓** | Durch die Treffer bewegen, über Gruppengrenzen hinweg |
| **↵ Enter** | Ausgewählten Treffer öffnen oder ausgewählten Befehl ausführen |
| **Tab / Umschalt+Tab** | Zum nächsten / vorherigen Bereichs-Chip |
| **Esc** | Palette schließen |

Der beste Treffer ist schon ausgewählt. Meist reicht also: ⌘K, ein paar Zeichen, Enter. Fährst du mit der Maus über eine Zeile, wird sie ebenfalls ausgewählt.

## Ergebnisse lesen, bevor du sie öffnest

Jede Zeile zeigt genug, um den richtigen Treffer zu erkennen:

- **Vorgang:** Typsymbol, Schlüssel, farbiger Statuspunkt mit Statusname und rechts der Avatar der zugewiesenen Person.
- **Projekt:** farbiges Sechseck mit Projektschlüssel, Zahl der offenen und erledigten Vorgänge und die Mitglieder.
- **Person:** Avatar und Position.
- **Board oder Sprint:** Name, beim Sprint zusätzlich das Ziel.
- **Artikel:** Bereich und wann er zuletzt aktualisiert wurde. So fallen veraltete Duplikate auf.

## Letzte Suchen

Öffnest du die Palette mit leerem Feld, siehst du deine letzten sechs Suchbegriffe.

![Die Palette mit den letzten Suchen bei leerem Suchfeld](/assets/img/shot-search-recents.png)
*__Letzte Suchen__, der jüngste Begriff zuerst, rechts __Leeren__.*

- Gespeichert wird ein Begriff erst, wenn du einen seiner Treffer öffnest.
- Ein Klick setzt den Begriff ins Feld und sucht erneut. Er springt nicht direkt zu einem Treffer.
- Die Liste liegt auf dem jeweiligen Gerät. Handy und Laptop haben also eigene Listen.

## Sie ist auch eine Befehlsleiste

Tippe, was du tun willst, und die Palette bietet es an:

- **Zum Dashboard**, **Zu Projekte**, **Zu Vorgänge**, **Zum Board**, **Zur Timeline**, **Zu Berichte**, **Zu Wissen**: die ganze Navigation.
- **Neuen Vorgang erstellen:** öffnet das Board. Dort hat jede Spalte unten ein Feld **Aufgabe hinzufügen**.
- **Hell / Dunkel umschalten:** wechselt das Erscheinungsbild. Die Palette bleibt dabei offen, damit du sofort zurückschalten kannst.

Befehle werden auf deinem Gerät abgeglichen und erscheinen sofort. Die Beschriftung musst du nicht genau treffen: *„dunkel“*, *„Erscheinungsbild“* und *„Hell“* finden denselben Schalter.

## Woher die Antworten kommen

Alle Treffer (außer Befehlen) kommen von deinem eigenen Server. Es gibt keinen externen Suchindex, und nichts wird woandershin geschickt. Die Treffer sind aktuell: Ein eben umbenannter Vorgang ist unter dem neuen Titel auffindbar.

Die App fragt erst kurz nach deinem letzten Tastendruck und verwirft veraltete Antworten. Die Ergebnisse flackern also nicht beim Tippen. Auch bei langsamer Verbindung siehst du nie Treffer für `Kar`, wenn du schon `Karbon` getippt hast.

## Wenn nichts zurückkommt

Prüfe der Reihe nach:

1. **Ist noch ein Bereichs-Chip aktiv?** Ein gewählter Chip bleibt aktiv. Klicke auf **Alle**.
2. **Ist es ein Teil eines langen Wortes?** Teile findet die Suche nur in Titeln, Schlüsseln und Labels, nicht in Beschreibungen und Artikeln. Tippe das ganze Wort.
3. **Ist es archiviert?** Stelle `archiviert` voran.
4. **Liegt es in einem Projekt, auf das du Zugriff hast?** Zugriff bekommst du über Projektmitgliedschaft und Teams. Sieht eine Kollegin etwas, das du nicht siehst, lass dich hinzufügen oder lies [Projekte & Teams](/de/guide-projects.html).

## Die Palette auf dem Handy

Auf dem Handy füllt die Palette den Bildschirm und kommt von oben. Das Suchfeld ist oben, die Tastatur ist schon offen. Die Chips scrollen seitwärts. Die Fußzeile mit Tastenhinweisen fehlt.

Bereiche, letzte Suchen, das Stichwort fürs Archiv und Befehle funktionieren wie am Rechner. Mehr in [Auf dem Handy](/de/guide-mobile.html).

## Sechs Dinge, die Leute wirklich suchen

**„Jemand hat HIN-42 erwähnt.“**
Tippe den Schlüssel. Groß und klein ist egal, und ein Teil reicht: `hin-4` grenzt schon ein. Enter öffnet den obersten Treffer.

**„Ich kenne einen Satz aus der Beschreibung, nicht den Titel.“**
Tippe ganze Wörter, etwa *„Zertifikat Rotation“*. Beschreibungen und Artikeltexte werden mitdurchsucht. Kommt nichts, nimm nur das markanteste Wort. In langen Feldern wird Wort für Wort gesucht, nicht nach Teilen.

**„Ich will alles aus einem Projekt.“**
Suche das Projekt und drücke Enter. Du landest in der Liste Issues, schon auf dieses Projekt gefiltert. Dort grenzt du mit **Filter** und **Gruppieren nach** weiter ein.

**„Hat das jemand übernommen?“**
Öffne **Issues**, dann **Filter → Zugewiesen → Nicht zugewiesen**. Nimm **Status** dazu, wenn dich nur begonnene Arbeit interessiert.

**„Was habe ich letzte Woche angefasst?“**
**Filter → Zugewiesen → du**, **Sortieren → Änderungsdatum (neu)**, **Zeitraum → Letzte 7 Tage**. Arbeitest du in mehreren Projekten, gruppiere nach Projekt.

**„Wurde das gelöscht?“**
Archiviertes ist nicht weg. Tippe `archiviert` und dahinter den Suchbegriff, etwa `archiviert Login Bug`. Die Palette durchsucht dann archivierte Vorgänge und Projekte. `archiviert` allein zeigt die zuletzt archivierten Objekte. Das englische `archived` funktioniert genauso, egal in welcher Sprache die App läuft.

!!! note "Archivierte Vorgänge tragen ein Abzeichen"
    Treffer aus dem Archiv sind markiert. Wiederherstellen kannst du sie im Vorgang selbst, siehe [Mit Vorgängen arbeiten](/de/guide-issues.html).

## Vorgangsschlüssel sind Adressen

Jeder Vorgang hat einen festen Schlüssel: Projektschlüssel, Bindestrich, Nummer, also `HIN-42`. Er ist auf dem ganzen Server eindeutig und eignet sich für Chatnachrichten, Commits und Dokumente.

- **Im Browser** öffnet `…/browse/HIN-42` den Vorgang direkt.
- **In den Apps für Desktop und Handy** tippst du den Schlüssel in die Palette.

Wird ein Vorgang in ein anderes Projekt verschoben, bekommt er eine neue Nummer. Der alte Schlüssel funktioniert weiter: in der Palette, in `browse`-Links und in Artikeln und Vorgängen, die ihn schon nennen.

!!! tip "Klicke den Schlüssel, um einen Link zu kopieren"
    Klick in einem geöffneten Vorgang auf den Schlüssel, und ein Link landet in der Zwischenablage. Beim Darüberfahren erscheint ein Kopiersymbol, danach eine Bestätigung. Der Link öffnet den Vorgang in der App, wenn sie installiert ist, sonst im Browser.

## Wenn du eine Liste brauchst, keinen Sprung

Die Seite **Issues** zeigt alle Vorgänge aus allen Projekten, auf die du Zugriff hast. Zuletzt bearbeitete stehen oben, beim Scrollen wird nachgeladen. Vier Bedienelemente formen die Liste.

![Die Issues-Liste mit Gruppieren nach, Sortieren, Filter und Zeitraum über der Tabelle](/assets/img/shot-issues.png)
*Die Seite Issues mit den vier Bedienelementen über der Tabelle und rechts Exportieren.*

### Eine Zeile lesen

Jede Zeile zeigt **Schlüssel**, **Titel** mit Typsymbol, **Status**, **Priorität**, zugewiesene Person und **Fälligkeitsdatum**.

- **Fällig** zeigt relative Angaben: *3 T. überfällig* und *Heute* in Rot, dann *Morgen*, dann *in 5 T.* für die kommende Woche. Danach steht ein Datum.
- **Titel** zeigt bei Sub-Tasks einen Zähler wie `0/1` oder `3/4`. So siehst du, ob ein Vorgang wirklich fertig ist.

Ein Klick auf die Zeile öffnet den Vorgang.

### Die Liste formen

**Filter** öffnet ein Popover mit fünf Facetten (**Status**, **Priorität**, **Zugewiesen**, **Projekt**, **Typ**) und dem Schalter **Archiviert**.

- Innerhalb einer Facette gilt ODER: *Bug* und *Task* zeigt beides.
- Zwischen Facetten gilt UND: *Bug* plus *In Arbeit* plus *Lena* zeigt nur Lenas laufende Bugs.

![Das Filter-Popover mit geöffneter Facette „Zugewiesen“](/assets/img/shot-issues-filter.png)
*Je eine Auswahl in __Status__ und __Zugewiesen__: Die Fußzeile zeigt __2 aktiv__, die Kopfzeile 3 von 11 Aufgaben.*

Lange Facetten haben ein eigenes Suchfeld. **Zurücksetzen** in der Fußzeile leert alle Facetten.

**Gruppieren nach** teilt die Liste in Abschnitte, etwa nach Person für das Daily oder nach Projekt. Der Knopf trägt den Namen der aktiven Gruppierung.

![Das Menü „Gruppieren nach“ über der Vorgangsliste](/assets/img/shot-issues-groupby.png)
*Das Menü „Gruppieren nach“ mit Haken an der aktiven Gruppierung.*

**Sortieren** ordnet die gesamte Ergebnismenge, nicht nur die geladenen Zeilen: neueste oder älteste zuerst oder nach Änderungsdatum. Standard ist zuletzt bearbeitet zuerst.

**Zeitraum** grenzt nach Datum ein:

- Mit Start und Fälligkeit: passt, wenn die Spanne den Zeitraum überschneidet.
- Mit nur einem Datum: passt, wenn es im Zeitraum liegt.
- Ohne Datum: zählt die letzte Aktivität.

![Das Menü „Zeitraum“ über der Vorgangsliste](/assets/img/shot-issues-timerange.png)
*Überfälliges und Heutiges oben, rollende Zeiträume in der Mitte, __Eigener Zeitraum…__ öffnet einen Kalender.*

Auch dieser Knopf trägt den Namen des aktiven Zeitraums.

!!! note "Filter halten für den Besuch, nicht für immer"
    Gespeicherte Ansichten gibt es noch nicht. Deine Einstellungen gelten, bis du die Seite verlässt. Für eine tägliche Ansicht behalte den Link (siehe unten) oder baue ein [Board](/de/guide-boards.html), das seine Einstellungen speichert.

## Filter, die mit dem Link kommen

Manche Links bringen einen Filter mit. Ein Klick auf die Kachel **Heutige Aufgaben** im Dashboard öffnet die Liste Issues mit allem, was bis heute fällig ist. Die Zahl auf der Kachel entspricht der Zahl der Zeilen. Eine Projektkarte filtert genauso auf ihr Projekt.

Im Browser steht der Filter in der Adresszeile. Kopierst du den Link, sehen Kolleginnen dieselbe gefilterte Liste.

## Ergebnisse mitnehmen

**Exportieren** schreibt die komplette gefilterte Menge, nicht nur die geladenen Zeilen. Die App holt dafür erst alle Seiten vom Server.

![Das Export-Menü in der Werkzeugleiste der Vorgangsliste](/assets/img/shot-issues-export.png)
*Das Menü __Exportieren__ mit drei Formaten.*

- **Als PDF exportieren:** druckbare Tabelle mit Name und Logo deiner Organisation.
- **Als CSV exportieren:** für Tabellenkalkulationen.
- **Als JSON exportieren:** für Programme, die die Daten wieder einlesen.

Die Datei landet im Ordner Downloads. Die App zeigt dir den Dateinamen.

## Über die Hierarchie navigieren statt suchen

Arbeit ist in Hinata drei Ebenen tief: Ein **Epic** enthält Stories, Tasks, Bugs und Features, und diese können **Sub-Tasks** enthalten. Du kannst dich durch alle Ebenen klicken:

- Über jedem Titel steht ein **Breadcrumb**. Die übergeordneten Einträge sind anklickbar, vom Sub-Task zum Elternvorgang und weiter zum Epic.
- Ein Elternvorgang listet **untergeordnete Vorgänge** und **Sub-Tasks** in eigenen Panels, mit Fortschrittszähler.
- Auf dem Board macht **Gruppieren nach → Epic** eine Swimlane pro Epic. Du siehst eine ganze Initiative, auch die Teile, an denen niemand arbeitet.

Die Auswahl für Epic und Elternvorgang zeigt zuerst **Letzte Epics** und **Aktuelle Vorgänge**.

## Nach einer Person suchen

Personen findest du über Anzeigename, Benutzername und Position. *„Vogt“*, *„lvogt“* und *„Designerin“* finden dieselbe Kollegin.

Die *Arbeit* einer Person siehst du so: **Issues** öffnen, nach **Zugewiesen** filtern und nach Projekt oder Status gruppieren. Auf einem Board macht der Personenfilter dasselbe.

!!! note "Eine Person zu öffnen braucht Adminrechte"
    Ein Personentreffer führt in die Benutzerverwaltung. Die können nur Administratorinnen und Administratoren öffnen. Finden können alle.

## Einmal verlinken, seltener suchen

Tippe beim Schreiben einer Beschreibung, eines Kommentars oder Artikels **@** und wähle Vorgang, Artikel oder Person. Daraus wird ein Link, der:

- den echten Titel und Status des Vorgangs zeigt,
- beim Klick den Vorgang öffnet,
- die Panels **Verknüpfte Aufgaben** (am Artikel) und **Dokumentiert in** (am Vorgang) füllt.

Tippst du `HIN-42` nur als Text, passiert nichts davon. Mehr in [Dokumentation schreiben](/de/guide-knowledge.html).

## Suchen an anderen Stellen

- Das **Board** hat einen eigenen Filter mit Sprint, Autor, Stichwort und Epic sowie einen Personenfilter. Siehe [Boards & Sprints](/de/guide-boards.html).
- Die **Wissensdatenbank** hat über den Bereichen ein Suchfeld für Artikeltitel, Bereichsnamen und Labels. Siehe [Dokumentation schreiben](/de/guide-knowledge.html).
- **Beobachtet** sammelt die Vorgänge, denen du folgst. Siehe [Auf dem Laufenden bleiben](/de/guide-notifications.html).
- In einem Vorgang durchsucht das **@**-Menü Vorgänge, Artikel und Personen.

!!! tip "Die Faustregel"
    Kannst du das Ding benennen, nimm ⌘K. Kannst du es nur beschreiben (*offen, meine, überfällig*), nimm die Liste Issues. Brauchst du es morgen wieder, mach ein Board daraus.

## Nächste Schritte

- Was du mit dem Gefundenen machst: [Mit Vorgängen arbeiten](/de/guide-issues.html).
- Dieselbe Arbeit visuell ordnen: [Boards & Sprints](/de/guide-boards.html).
- Das Runbook schreiben, das die Palette nächstes Mal findet: [Dokumentation schreiben](/de/guide-knowledge.html).
