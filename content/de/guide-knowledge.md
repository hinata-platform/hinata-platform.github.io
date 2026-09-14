---
title: Dokumentation schreiben
description: Artikel in der Wissensdatenbank schreiben, ordnen und mit Vorgängen und Personen verknüpfen.
---

# Dokumentation schreiben

Vorgänge beschreiben laufende Arbeit. Dokumentation beschreibt, wie die Dinge *sind*: Runbooks, Entscheidungen, Einstiegsseiten.

Dafür gibt es die **Wissensdatenbank**, ein Wiki. Seiten lassen sich verschachteln, wer eine Seite lesen kann, darf sie bearbeiten, und Artikel verlinken die Vorgänge und Personen, um die es geht.

## Bereiche, Artikel und Unterseiten

- Ein **Bereich** ist ein Regal, etwa *Engineering*, *Product*, *Design* oder *Operations*. Er hat Namen, Symbol, Farbe und eine Zeile Beschreibung.
- Ein **Artikel** ist eine Seite in einem Bereich.
- Jeder Artikel kann **Unterseiten** haben, beliebig tief. Zum Beispiel oben ein Handbuch, darunter seine Kapitel.

![Die Startseite der Wissensdatenbank: Suche, eine Karte pro Bereich und die zuletzt aktualisierten Artikel](/assets/img/shot-knowledge.png)
*Die Startseite der Wissensdatenbank.*

Jede Karte zeigt Farbe, Beschreibung und Artikelzahl eines Bereichs. Darunter listet **Kürzlich aktualisiert** die neuesten Änderungen mit Bereich und Autor.

### Einen Bereich anlegen

Klicke die Kachel **Neuer Bereich**, gib Name und Beschreibung ein und wähle Symbol und Farbe.

![Der Dialog „Neuer Bereich“ mit ausgefülltem Namen und Beschreibung](/assets/img/shot-kb-new-space.png)
*Der Dialog „Neuer Bereich“.*

**Bereich erstellen** wird erst mit einem Namen aktiv. Der Bereich erscheint dann sofort im Raster.

Leg lieber wenige, breite Bereiche an, etwa einen pro Team oder Disziplin. Einer pro Projekt passt selten, weil Themen Projekte überdauern.

!!! warning "Ein Bereich lässt sich nur löschen, solange er leer ist"
    **Bereich löschen** gibt es nur für Bereiche ohne Artikel. Verschiebe oder lösche vorher alle Seiten.

## Einen Artikel schreiben

Tippe auf **Neuer Artikel**, auf der Startseite oder in der Artikelansicht neben **Alle Bereiche**.

![Der Artikeleditor bei einer neuen Seite, Titel getippt, Text noch leer](/assets/img/shot-kb-new-article.png)
*Der Editor bei einer neuen Seite.*

- **Titel** über der Werkzeugleiste. Er wird Überschrift, Zeile im Seitenbaum und Suchbegriff. *„Checkliste für Releases“* findet man, *„Notizen“* nicht.
- **Bereichsauswahl** daneben. Lässt sich jederzeit ändern.
- **Knopf rechts:** **Veröffentlichen** bei neuen Seiten, **Speichern** beim Bearbeiten.

Einen Entwurfsstatus gibt es nicht.

!!! tip "Fang ihn gleich als Unterseite an"
    Fahr im Baum über den Elternartikel und drück das **+** (**Unterseite hinzufügen**). Der Artikel entsteht direkt an der richtigen Stelle.

## Eine erste Seite von Anfang bis Ende

1. Öffne **Wissen** in der Seitenleiste und drücke **Neuer Artikel**.
2. Wähle einen Titel nach der Frage, die er beantwortet: *„Wie wir ein Release ausrollen“*, nicht *„Release“*.
3. Wähle im Dropdown neben dem Titel den Bereich.
4. Schreib den Text mit **Überschrift 2** pro Etappe, einer **nummerierten Liste** für die Schritte und einer **Warnung** für das, was schiefgehen kann.
5. Tippe **@** und wähle das zugehörige Ticket.
6. Drücke **Veröffentlichen**.

Die Seite ist jetzt über Titel und Text auffindbar, steht unter **Kürzlich aktualisiert**, und der Vorgang zeigt sie unter **Dokumentiert in**.

## Der Editor

Du schreibst direkt formatiert, ohne Syntax und ohne Vorschau. Die Werkzeugleiste:

| Gruppe | Knöpfe |
| --- | --- |
| **Verlauf** | Rückgängig, Wiederholen |
| **Textstil** | Ein Dropdown: Fließtext, Überschrift 1 bis 3, Zitat, Aufzählung, Nummerierte Liste, Aufgabenliste, Codeblock |
| **Formatierung** | Fett, Kursiv, Unterstrichen, Durchgestrichen, Inline-Code, Link |
| **Ausrichtung** | Linksbündig, Zentriert, Rechtsbündig, Blocksatz |
| **Blöcke** | Infobox, Warnung, Notiz, Tipp, Trennlinie |
| **Einfügen** | Bild einfügen, Erwähnen / verlinken (@) |

![Das Dropdown „Textstil“ offen über dem Artikeleditor](/assets/img/shot-kb-text-style.png)
*Das Dropdown „Textstil“ mit neun Formen.*

- **Textstil** ist ein Dropdown, weil eine Zeile nur eine Form haben kann. Ein Haken markiert die aktuelle. Umfasst die Auswahl mehrere, steht dort **Gemischt**.
- **Farbige Boxen** (Infobox, Warnung, Notiz, Tipp) machen Wichtiges sichtbar.
- **Aufgabenlisten** haben echte Kästchen und sind für Checklisten gedacht. Brauchen Punkte Verantwortliche und Termine, nimm [Vorgänge](/de/guide-issues.html).
- **Codeblöcke** haben eine Sprache und werden passend eingefärbt.

!!! tip "Markiere Text, und die Werkzeuge kommen zu dir"
    Über markiertem Text erscheint eine kleine Leiste mit den häufigsten Formatierungen und dem Linkeditor. Die Adresse tippst du direkt über den markierten Wörtern.

### Tastenkürzel

| Kürzel | Wirkung |
| --- | --- |
| **⌘B / Strg+B** | Fett |
| **⌘I / Strg+I** | Kursiv |
| **⌘U / Strg+U** | Unterstrichen |
| **⌘Z / Strg+Z** | Rückgängig |
| **⇧⌘Z / Strg+Y** | Wiederholen |

Für farbige Boxen und **@** gibt es kein Kürzel. **@** tippst du einfach.

### Links, Bilder und Trennlinien

- **Links** über die Werkzeugleiste oder die Leiste über markiertem Text. **Link entfernen** löscht ihn. Unsichere Adressen lehnt der Editor ab.
- **Bilder** lädst du mit dem Bildknopf hoch, sie landen am Cursor. Größe über die Eckgriffe, Bildunterschrift darunter. Erlaubt sind PNG, JPEG, GIF und WebP. SVG nicht, weil es Code enthalten kann. Die maximale Größe legt fest, wer den Server betreibt, siehe [Objektspeicher](/de/storage.html).
- **Trennlinien** sparsam einsetzen. Überschriften erscheinen zusätzlich in der Gliederung.

!!! warning "Eine leere Seite über eine volle zu speichern, ist gesperrt"
    Geht beim Laden etwas schief, speichert der Editor keinen leeren Text über bestehenden Inhalt und nennt den Grund.

## Smarte Links mit @

Tippe **@** im Text oder drück den Knopf **@** am Ende der Werkzeugleiste. Wählst du einen Vorschlag, entsteht ein *Chip*, ein echter Link.

![Die Auswahl „Erwähnen / verlinken (@)“ über dem Artikeleditor](/assets/img/shot-kb-mention-picker.png)
*Die Auswahl für Vorgänge, Artikel und Personen.*

Die Liste wird beim Tippen enger. Jede Zeile zeigt ein Symbol für die Art und den Vorgangsschlüssel oder Bereich. Im Beispiel findet `ok` vier Vorgänge, zwei Artikel und Amara Okafor.

- **Vorgang:** zeigt Typ, Schlüssel und aktuellen Titel, öffnet per Klick. Maus darüber (Desktop) oder gedrückt halten (Handy) zeigt Status, Priorität und zugewiesene Person.
- **Artikel:** zeigt Symbol und Titel der Seite.
- **Person:** zeigt Avatar und Vornamen, auch wenn sich die Position ändert.

Verschwindet das Ziel, wird der Chip rot.

!!! warning "HIN-42 von Hand zu tippen ist bloß Text"
    Nur mit **@** eingefügte Chips sind Links. Getippter Text öffnet nichts und erscheint nicht unter **Verknüpfte Aufgaben**.

## Dokumentation, die weiß, was sie beschreibt

Chips wirken in beide Richtungen, ganz automatisch:

- **Verknüpfte Aufgaben** am Ende eines Artikels listet jeden erwähnten Vorgang mit aktuellem Status.
- **Dokumentiert in** am Vorgang listet jeden Artikel, der ihn verlinkt.

![Ein Vorgangs-Chip im Artikeltext mit geöffneter Vorschaukarte](/assets/img/shot-kb-chip-preview.png)
*Die Vorschaukarte eines Vorgangs.*

Die Vorschaukarte zeigt Status, Titel, zugewiesene Person, Priorität und Label, unten **Aufgabe öffnen**.

![Ein Artikel mit Seitenbaum links, Text in der Mitte sowie Mitwirkenden und Details rechts](/assets/img/shot-knowledge-article.png)
*Die Artikelansicht.*

## Sich in einem Artikel zurechtfinden

Drei Spalten. Die äußeren klappst du über die Schalter an ihren Innenkanten weg.

- **Links:** Bereichsauswahl und Seitenbaum. Der aktuelle Artikel ist hervorgehoben.
- **Mitte:** Bereichschip, Titel, Autor, letzte Aktualisierung, Labels und Text. **Bearbeiten** und Löschen stehen neben der Autorenzeile.
- **Rechts:** **Auf dieser Seite** (Gliederung, nur bei mehr als einer Überschrift), **Mitwirkende**, **Verwandte Artikel** (Seiten, die dieser Artikel verlinkt) und **Details** (Erstellungsdatum, Bereich, Status).

## Auf dem Handy schreiben

- Die **Werkzeugleiste scrollt seitwärts**, Rückgängig und Wiederholen stehen vorn.
- Der **Seitenbaum liegt in einer Schublade**, der Artikel hat die volle Breite.
- **Halte einen Chip gedrückt** für die Vorschaukarte.

Siehe [Auf dem Handy](/de/guide-mobile.html).

## Umsortieren: ziehen, verschachteln, verschieben

- **Zieh eine Seite auf eine andere**, um sie einzuhängen. Unterseiten wandern mit.
- **Lass sie auf der Wurzelzone** oben im Baum fallen, um sie auf die oberste Ebene zu holen.
- **Anderer Bereich:** Seite öffnen, **Bearbeiten**, Bereich in der Kopfzeile ändern.

Fährst du über eine Zeile, erscheinen **+** (**Unterseite hinzufügen**) und das Menü.

![Das Zeilenmenü einer Seite im Wissensbaum](/assets/img/shot-kb-tree-menu.png)
*Das Menü einer Seite im Baum.*

- **Auf oberste Ebene verschieben** löst die Seite ohne Ziehen aus ihrem Elternartikel.
- **Löschen** entfernt die Seite. Hat sie Unterseiten, heißt der Eintrag **Löschen (zuerst Unterseiten verschieben)** und tut nichts.

!!! warning "Löschen ist endgültig, und Elternseiten sind geschützt"
    **Löschen** fragt mit dem Artikelnamen nach. Es gibt kein Rückgängig und keinen Papierkorb. Seiten mit Unterseiten lassen sich erst löschen, wenn die Unterseiten verschoben sind.

## Wer was sieht und ändern darf

| Rahmen | Wer ihn sieht |
| --- | --- |
| **Global** | Alle mit einem Konto auf eurem Server |
| **Projekt** | Alle mit Zugriff auf dieses Projekt |
| **Team** | Die Mitglieder dieses Teams |

- In der App geschriebene Artikel sind **global**.
- Artikel mit Rahmen Projekt oder Team kommen aus Integrationen. Siehst du das Projekt oder Team nicht, siehst du auch die Seiten nicht, weder in der Suche noch in Listen.
- Administratorinnen und Administratoren sehen alles.

Projektzugriff: [Projekte & Teams](/de/guide-projects.html).

!!! warning "Wer eine Seite lesen kann, kann sie bearbeiten und löschen"
    Es gibt keine Rechte pro Artikel und keinen reinen Lesezugriff. Nur Elternseiten mit Unterseiten sind vor dem Löschen geschützt.

## Die Wissensdatenbank durchsuchen

- **Suchfeld auf der Startseite von Wissen:** Artikeltitel, Bereichsnamen und Labels.
- **Palette (⌘K):** zusätzlich der Text in Artikeln und alles andere in Hinata. Siehe [Dinge finden](/de/guide-search.html).

Labels stehen als Chips unter dem Titel, beide Suchen finden sie. Ein Label wie `runbook` holt eine ganze Kategorie. Der Editor hat noch kein Feld für Labels, sie kommen meist von dem, was den Artikel angelegt hat.

## Was hierher gehört und was in einen Vorgang

| Schreib einen Artikel, wenn … | Schreib einen Vorgang, wenn … |
| --- | --- |
| es auch nach getaner Arbeit noch stimmt | es irgendwann fertig ist und dann vorbei |
| die Lesenden später dazukommen | die Lesenden es gerade tun |
| es beschreibt, wie etwas funktioniert | es eine Änderung beschreibt, die gemacht werden soll |
| niemand dafür zuständig sein muss | jemand es besitzen und abschließen muss |

Faustregel: Braucht die Seite einen *Status*, ist es ein Vorgang. Braucht sie ein *Datum der letzten Durchsicht*, ist es ein Artikel.

## Eine Seite aktuell halten

Autorenzeile, **Mitwirkende** und **Details** zeigen Autor, letzte Aktualisierung und Erstellungsdatum. Eine Versionshistorie gibt es nicht. Deshalb:

- **Bearbeite gezielt**, statt den ganzen Text zu ersetzen.
- **Ist eine Seite überholt**, schreib das oben hin und verlinke die neue Seite, statt sie zu löschen.

Tut sich unter **Kürzlich aktualisiert** monatelang nichts, ist die Dokumentation vermutlich veraltet.

## Gewohnheiten, die eine Wissensdatenbank am Leben halten

- **Eine Seite, ein Thema.** Sonst teile sie in Seite und Unterseite.
- **Verlinke den Vorgang, statt ihn nachzuerzählen.** Ein Chip mit `@` bleibt aktuell.
- **Schreib die Warnung zuerst**, in einer farbigen Box weit oben.
- **Repariere, was dir auffällt.** Du darfst jede Seite bearbeiten, die du lesen kannst.
- **Nutze echte Überschriften.** Sie ergeben *Auf dieser Seite*.

## Nächste Schritte

- Häng Dokumentation an die Arbeit, die sie beschreibt: [Mit Vorgängen arbeiten](/de/guide-issues.html).
- Lerne die schnellsten Wege zurück zu einer Seite: [Dinge finden](/de/guide-search.html).
- Wie Projekt- und Teamzugriff vergeben wird: [Projekte & Teams](/de/guide-projects.html).
