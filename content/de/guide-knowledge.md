---
title: Dokumentation schreiben
description: Artikel in der Wissensdatenbank schreiben, sie in Bereiche und Unterseiten einsortieren und mit den Vorgängen und Personen verknüpfen, die sie beschreiben.
---

# Dokumentation schreiben

Vorgänge beschreiben Arbeit, die gerade passiert. Dokumentation beschreibt, wie die Dinge *sind* — das Runbook, dem du um drei Uhr nachts folgst, die Entscheidung, an deren Zustandekommen sich niemand erinnert, die Onboarding-Seite, die einer neuen Kollegin eine Woche Nachfragen erspart.

Genau dafür ist Hinatas **Wissensdatenbank** da. Sie ist ein Wiki im ehrlichen Sinn: Seiten stecken in Seiten, wer eine Seite lesen kann, darf sie auch verbessern, und jeder Artikel kann auf die Vorgänge und Personen zeigen, um die es geht — so bleiben Dokumentation und Arbeit aneinander.

## Bereiche, Artikel und Unterseiten

Drei Ebenen, und nicht mehr, denn ein tieferes Ablagesystem pflegt am Ende niemand:

- Ein **Bereich** ist ein Regal — *Engineering*, *Product*, *Design*, *Operations*. Er hat einen Namen, ein Symbol, eine Farbe und eine Zeile dazu, was hineingehört.
- Ein **Artikel** ist eine Seite in einem Bereich.
- Jeder Artikel kann **Unterseiten** haben, und die wieder eigene. Hier wohnt die eigentliche Struktur: oben ein Handbuch, darunter seine Kapitel.

![Die Startseite der Wissensdatenbank: Suche, eine Karte pro Bereich und die zuletzt aktualisierten Artikel](/assets/img/shot-knowledge.png)

*Die Startseite der Wissensdatenbank. Jede Karte ist ein Bereich mit eigener Farbe, Beschreibung und Artikelzahl; die gestrichelte Kachel legt einen neuen an. Darunter zeigt **Kürzlich aktualisiert**, woran das Team geschrieben hat — mit Bereich und Autor in jeder Zeile.*

Die Startseite zeigt jeden Bereich als Karte, dazu eine Liste **Kürzlich aktualisiert** — praktisch der Weg, auf dem die meisten eine Seite von letzter Woche wiederfinden.

### Einen Bereich anlegen

Klicke die gestrichelte Kachel **Neuer Bereich**. Gib ihm einen **Namen**, optional eine **Beschreibung** dessen, was darin lebt, wähle ein **Symbol** und eine **Farbe**, dann **Bereich erstellen**. Er erscheint sofort im Raster, leer und bereit.

Halte die Zahl der Bereiche klein und ihren Zuschnitt weit. Ein Bereich pro Team oder pro Disziplin funktioniert; einer pro Projekt meistens nicht, denn die meiste Dokumentation handelt von einem *Thema*, das jedes einzelne Projekt überlebt.

!!! warning "Ein Bereich lässt sich nur löschen, solange er leer ist"
    **Bereich löschen** wird nur bei einem Bereich ohne Artikel angeboten. Enthält er Seiten, verschiebe oder lösche sie zuerst. Das ist Absicht: Ein Regal zu entfernen darf niemals stillschweigend die Bücher darin mitnehmen.

## Einen Artikel schreiben

Drücke **Neuer Artikel** — auf der Startseite der Wissensdatenbank oder in der Artikelansicht, wo der Knopf neben **Alle Bereiche** sitzt.

Du bekommst ein Titelfeld, eine Bereichsauswahl und den Textkörper. Tippe zuerst den Titel: Er wird zur Überschrift der Seite, zur Zeile im Baum und zu dem, wonach später alle suchen — ein Moment Nachdenken lohnt sich also. *„Release-Checkliste & Versions-Gating“* ist auffindbar. *„Notizen“* nicht.

Die Bereichsauswahl in der Kopfzeile entscheidet, auf welchem Regal der Artikel landet. Du kannst das jederzeit ändern.

Bist du fertig, drücke **Veröffentlichen** (bei einem neuen Artikel) oder **Speichern** (bei einem, den du bearbeitest). Es gibt keinen separaten Entwurfsstatus, den du dir merken müsstest — ein Artikel ist geschrieben oder eben nicht.

!!! tip "Fang ihn gleich als Unterseite an"
    Gehört der Artikel unter einen bestehenden, erstelle ihn nicht von der Startseite aus. Öffne den Elternartikel im Baum, nimm sein Zeilenmenü und wähle **Unterseite hinzufügen**. Er entsteht an der richtigen Stelle, im richtigen Bereich, ganz ohne Aufräumen danach.

## Eine erste Seite von Anfang bis Ende

Falls du noch nie eine geschrieben hast — das ist die ganze Schleife in sechs Schritten:

1. Öffne **Wissen** in der Seitenleiste und drücke **Neuer Artikel**.
2. Gib ihm einen Titel nach der Frage, die er beantwortet — *„Wie wir ein Release ausrollen“*, nicht *„Release“*.
3. Wähle im Dropdown neben dem Titel den passenden Bereich.
4. Schreibe den Text. Nimm **Überschrift 2** für jede Etappe, eine **nummerierte Liste** für die Schritte darin und eine **Warnung**-Box für das eine, was schiefgeht, wenn man es überspringt.
5. Tippe **@**, wo du das Ticket erwähnst, aus dem das entstanden ist, und wähle es aus der Liste.
6. Drücke **Veröffentlichen**.

Diese Seite ist ab jetzt über ihren Titel und über die Wörter darin auffindbar, sie erscheint fürs Team unter **Kürzlich aktualisiert**, und der verknüpfte Vorgang zeigt diesen Artikel nun unter **Dokumentiert in**. Zwei Minuten Schreiben, dauerhaft an der Arbeit befestigt.

## Der Editor

Der Textkörper ist ein Rich-Text-Editor: Was du tippst, ist das, wie die Seite aussehen wird — keine Syntax zu lernen, keine Vorschau, zwischen der du hin- und herschalten musst.

Über dem Text sitzt die Werkzeugleiste, in der Reihenfolge, in der man danach greift:

| Gruppe | Knöpfe |
| --- | --- |
| **Verlauf** | Rückgängig, Wiederholen |
| **Textstil** | Ein Dropdown: Fließtext, Überschrift 1–3, Zitat, Aufzählung, Nummerierte Liste, Aufgabenliste, Codeblock |
| **Formatierung** | Fett, Kursiv, Unterstrichen, Durchgestrichen, Inline-Code, Link |
| **Ausrichtung** | Linksbündig, Zentriert, Rechtsbündig, Blocksatz |
| **Blöcke** | Infobox, Warnung, Notiz, Tipp, Trennlinie |
| **Einfügen** | Bild einfügen, Erwähnen / verlinken (@) |

Ein paar davon lohnen eine eigene Erwähnung.

**Textstil ist ein Dropdown, keine Knopfreihe**, weil eine Zeile immer nur eines davon sein kann. Es zeigt, worin der Cursor gerade steckt — *Gemischt*, wenn deine Auswahl mehrere Arten umspannt.

**Die vier farbigen Boxen** — Infobox, Warnung, Notiz und Tipp — sind der schnellste Weg zu einer überfliegbaren Seite. Steck den einen Satz, der jemandem einen Ausfall erspart, in eine Warnung, und er wird gelesen; lass ihn im vierten Absatz stehen, und er wird es nicht.

**Aufgabenlisten** sind echte Kästchen zum Abhaken. Sie sind für Checklisten, denen man folgt, nicht für Arbeit, die verfolgt wird — brauchen die Punkte Verantwortliche und Termine, wollen sie [Vorgänge](/de/guide-issues.html) sein.

**Codeblöcke** tragen eine Sprache, ein Shell-Schnipsel und ein JSON-Payload sind also unterschiedlich eingefärbt und auf einen Blick auseinanderzuhalten.

!!! tip "Markiere Text, und die Werkzeuge kommen zu dir"
    Markierst du eine Passage, erscheint darüber eine kleine Glas-Leiste mit den Formatierungen, die du am wahrscheinlichsten brauchst — inklusive Link-Editor. Die Adresse tippst du direkt über den Wörtern, die verlinkt werden, du siehst also weiter, was du verlinkst, während du tippst, wohin.

### Tastenkürzel

Am Schreibtisch funktionieren die gewohnten, deine Hände müssen den Text also nie verlassen:

| Kürzel | Wirkung |
| --- | --- |
| **⌘B / Strg+B** | Fett |
| **⌘I / Strg+I** | Kursiv |
| **⌘U / Strg+U** | Unterstrichen |
| **⌘Z / Strg+Z** | Rückgängig |
| **⇧⌘Z / Strg+Y** | Wiederholen |

Alles andere wohnt auf der Werkzeugleiste. Für die farbigen Boxen und für **@** gibt es kein Kürzel — aber **@** ist ohnehin ein Zeichen, das du tippst, und genau deshalb wurde es gewählt.

### Links, Bilder und Trennlinien

**Links** setzt du über die Werkzeugleiste oder die Auswahl-Leiste. Adresse tippen oder einfügen; **Link entfernen** nimmt ihn wieder weg. Adressen, denen zu folgen nicht sicher wäre, werden abgelehnt statt stillschweigend gespeichert.

**Bilder** lädst du mit dem Bild-Knopf von deinem Gerät hoch; sie landen dort, wo der Cursor steht. Zieh an den Griffen in den Ecken, um die Größe zu ändern, und setz eine Bildunterschrift darunter, wenn das Bild eine braucht. PNG, JPEG, GIF und WebP werden akzeptiert — SVG bewusst nicht, weil eine SVG-Datei Code enthalten kann. Wie groß ein Bild sein darf, legt fest, wer euren Server betreibt; siehe [Objektspeicher](/de/storage.html), falls du das bist.

**Trennlinien** trennen Abschnitte einer langen Seite. Setz sie sparsam ein — Überschriften machen den Job besser und füttern zusätzlich die Gliederung.

!!! warning "Eine leere Seite über eine volle zu speichern, ist gesperrt"
    Geht beim Laden eines Artikels etwas schief, weigert sich der Editor, einen leeren Text über bestehenden Inhalt zu speichern, und sagt dir warum. Es ist die einzige Aktion hier, die eine ganze Seite Schreibarbeit mit einem Klick zerstören könnte — also wurde sie unmöglich gemacht statt nur unwahrscheinlich.

## Smart-Links: @ ist die wichtige Taste

Tippe irgendwo im Artikel **@** — oder drück den **@**-Knopf in der Werkzeugleiste — und über dem Glas öffnet sich eine Auswahl, die **Vorgänge, Artikel und Personen** gleichzeitig durchsucht. Wählst du etwas aus, wird ein *Chip* eingefügt: kein Text, der wie eine Referenz aussieht, sondern ein lebendiger Link.

Genau darin liegt der ganze Unterschied:

- Ein **Vorgangs-Chip** zeigt Typ, Schlüssel und echten Titel des Vorgangs und öffnet ihn beim Klick. Fahr am Schreibtisch mit der Maus darüber oder halte ihn auf dem Handy gedrückt, und eine Vorschaukarte zeigt Status, Priorität und zugewiesene Person, ohne dass du die Seite verlässt.
- Ein **Artikel-Chip** verlinkt eine andere Seite und zeigt ihr Symbol und ihren Titel.
- Ein **Personen-Chip** zeigt Avatar und Vornamen, damit *„frag @Lena“* auch dann noch stimmt, wenn Lenas Position sich ändert.

Verschwindet das Ziel eines Chips, sagt der Chip das, statt so zu tun als ob — ein toter Link wird rot gezeichnet und nicht still zu gewöhnlichem Text.

!!! warning "HIN-42 von Hand zu tippen ist bloß Text"
    Nur Chips, die du mit **@** einfügst, zählen als Link. Bloße Zeichen sehen ähnlich aus und verhalten sich völlig anders: Sie öffnen nichts, sie erscheinen nicht unter **Verknüpfte Aufgaben**, und der Vorgang erfährt nie, dass er dokumentiert ist. Ein Tastendruck ist der ganze Unterschied.

## Dokumentation, die weiß, was sie beschreibt

Weil Chips Links sind, kann Hinata die Verbindung von beiden Enden zeigen — und genau das macht aus einem Wiki etwas, dem das Team traut.

- Am Fuß eines Artikels listet **Verknüpfte Aufgaben** jeden Vorgang, den die Seite erwähnt, als Karte mit aktuellem Status. Ein Runbook zeigt dir den Stand der Arbeit, die es beschreibt, ohne dass du nachsehen gehst.
- An einem Vorgang listet **Dokumentiert in** jeden Artikel, der ihn verlinkt. Wer kalt auf einem Ticket landet, findet die Seite, die das dahinterliegende Subsystem erklärt.

Keine der beiden Listen wird von Hand gepflegt. Beide leiten sich aus den Chips im Text ab, sie können also gar nicht veralten — schreib den Link einmal, und die Beziehung existiert in beide Richtungen, dauerhaft.

![Ein Artikel mit Seitenbaum links, Text in der Mitte sowie Mitwirkenden und Details rechts](/assets/img/shot-knowledge-article.png)

*Die Artikelansicht: links Bereichsauswahl und Seitenbaum, in der Mitte der Artikel mit Bereichs-Chip, Zeile zur Urheberschaft, Labels und Text — beachte die Infobox und den Personen-Chip im Fließtext — und rechts Mitwirkende und Details. **Bearbeiten** und der Löschknopf sitzen neben der Autorenzeile.*

## Sich in einem Artikel zurechtfinden

Die Artikelansicht hat drei Spalten, und beide Randspalten lassen sich über die kleinen Schalter an ihren Innenkanten wegklappen, wenn du in voller Breite lesen willst.

**Links** stehen Bereichsauswahl und Seitenbaum. Der Baum zeigt die gesamte Verschachtelung des aktuellen Bereichs; der Artikel, den du liest, ist hervorgehoben, und seine Unterseiten hängen darunter.

**In der Mitte** steht der Artikel: sein Bereichs-Chip, Titel, Autor und wann er zuletzt aktualisiert wurde, seine Labels und der Text.

**Rechts** steht die Randspalte:

- **Auf dieser Seite** — eine Gliederung aus den Überschriften, die nur erscheint, wenn der Artikel mehr als eine hat. Ein Klick springt zur Überschrift.
- **Mitwirkende** — die Personen, die der Seite zugeschrieben sind.
- **Verwandte Artikel** — andere Seiten, die diese verlinkt.
- **Details** — wann sie erstellt wurde, in welchem Bereich sie liegt und ihr Status.

Auf dem Handy wandert der Baum in eine Schublade, die du bei Bedarf öffnest — der Artikel bekommt so die volle Breite.

## Auf dem Handy schreiben

Alles funktioniert auf dem Handy, mit drei sinnvollen Unterschieden:

- Die **Werkzeugleiste scrollt seitwärts**. Rückgängig und Wiederholen stehen vorn, weil es auf einem Touchgerät kein Tastenkürzel dafür gibt und man am schnellsten danach greift.
- Der **Seitenbaum wohnt in einer Schublade**, damit der Artikel die volle Breite bekommt; öffne sie, wenn du zwischen Seiten wechseln willst.
- **Halte einen Chip gedrückt**, statt mit der Maus darüberzufahren, um die Vorschaukarte zu sehen.

Lesen ist auf dem Handy angenehm; eine lange Seite zu schreiben ist es auf keinem Gerät. Handys sind dafür da, den Absatz zu korrigieren, der dir in der Bahn aufgefallen ist. Siehe [Auf dem Handy](/de/guide-mobile.html).

## Umsortieren: ziehen, verschachteln, verschieben

Der Baum ist keine Dekoration — er ist die Bearbeitungsfläche für Struktur:

- **Zieh eine Seite auf eine andere**, um sie darunter zu hängen. Ihre eigenen Unterseiten reisen mit; du musst nie einen Teilbaum von Hand wieder anhängen.
- **Lass sie auf der Wurzelzone** oben im Baum fallen, um sie zurück auf die oberste Ebene zu holen. Das Zeilenmenü bietet **Auf oberste Ebene verschieben** für dasselbe ohne Ziehen.
- Im Zeilenmenü stecken außerdem **Unterseite hinzufügen** und **Löschen**.
- Um eine Seite in einen *anderen Bereich* zu verschieben, öffne sie, drücke **Bearbeiten** und ändere den Bereich in der Kopfzeile.

!!! warning "Löschen ist endgültig, und Elternseiten sind geschützt"
    **Löschen** fragt nach und nennt den Artikel beim Namen, denn es gibt kein Rückgängig und keinen Papierkorb. Eine Seite mit Unterseiten lässt sich überhaupt nicht löschen, solange die nicht woandershin verschoben sind — das Menü sagt das, statt eine Aktion anzubieten, die Waisen hinterließe.

## Wer was sieht — und wer was ändern darf

Die Sichtbarkeit eines Artikels folgt dem Rahmen, in dem er entstanden ist:

| Rahmen | Wer ihn sieht |
| --- | --- |
| **Global** | Alle mit einem Konto auf eurem Server |
| **Projekt** | Alle mit Zugriff auf dieses Projekt |
| **Team** | Die Mitglieder dieses Teams |

In der App geschriebene Artikel sind standardmäßig **global**, also organisationsweit. Projekt- und teamgebundene Artikel stammen aus Integrationen, die sie mit einem Rahmen anlegen, und sie folgen exakt dem Zugriff, den du auf dieses Projekt oder Team ohnehin hast: Ist ein Projekt für dich unsichtbar, sind es auch seine Seiten — sie tauchen weder in der Suche noch in irgendeiner Liste auf. Administratorinnen und Administratoren sehen alles. Der Zugriff auf Projekte selbst kommt aus Mitgliedschaft und Teams — siehe [Projekte & Teams](/de/guide-projects.html).

!!! warning "Wer eine Seite lesen kann, kann sie bearbeiten und löschen"
    Es gibt keine Rechte pro Artikel und keinen Nur-Lesen-Modus. Das ist ein Wiki: Derselbe Zugriff, mit dem du eine Seite öffnest, erlaubt dir, sie zu verbessern — und sie zu entfernen. Vertraue dem Team und verlass dich darauf, dass dort, wo Rechte nicht schützen, die Struktur schützt (eine Elternseite lässt sich nicht löschen, solange sie Kinder hat).

## Die Wissensdatenbank durchsuchen

Zwei Suchen erreichen deine Artikel, und sie sind in Verschiedenem gut.

Das **Suchfeld auf der Wissens-Startseite** passt auf Artikeltitel, Bereichsnamen und Labels. Nimm es, wenn du durch die eigene Dokumentation stöberst und dich halb an einen Titel erinnerst.

Die **⌘K-Palette** durchsucht zusätzlich den *Text in* den Artikeln — und alles andere gleich mit. Nimm sie, wenn du dich an einen Satz erinnerst, aber nicht daran, auf welcher Seite er stand. Siehe [Dinge finden](/de/guide-search.html).

Labels helfen beiden. Ein Artikel, der welche trägt, zeigt sie als Chips unter seinem Titel, und sowohl die Startseiten-Suche als auch die Palette passen darauf; ein konsistentes Label wie `runbook` macht also eine ganze Kategorie mit einer Abfrage abrufbar. Der Editor hat heute kein Feld für Labels — sie kommen deshalb meist von dem, was den Artikel angelegt hat, und nicht von deiner Tastatur.

## Was hierher gehört und was in einen Vorgang

Die beiden Hälften von Hinata beantworten verschiedene Fragen, und etwas in die falsche zu legen ist der häufigste Weg, auf dem Dokumentation veraltet.

| Schreib einen Artikel, wenn … | Schreib einen Vorgang, wenn … |
| --- | --- |
| es auch nach getaner Arbeit noch stimmt | es irgendwann fertig ist und dann vorbei |
| die Lesenden später dazukommen | die Lesenden es gerade tun |
| es beschreibt, wie etwas funktioniert | es eine Änderung beschreibt, die gemacht werden soll |
| niemand dafür zuständig sein muss | jemand es besitzen und abschließen muss |

Ein brauchbarer Test: Bräuchte die Seite einen *Status*, ist es ein Vorgang. Bräuchte sie ein *Datum der letzten Durchsicht*, ist es ein Artikel.

## Eine Seite ehrlich halten

Ein Artikel trägt seine eigene kleine Spur: Die Autorenzeile sagt, wer ihn geschrieben hat und wann er zuletzt aktualisiert wurde; **Mitwirkende** in der Randspalte nennt seinen Autor; **Details** hält fest, wann er erstellt wurde.

Es gibt keine Versionshistorie und keinen Weg, eine frühere Fassung wiederherzustellen — deshalb lohnen sich zwei Gewohnheiten. Bearbeite an Ort und Stelle, statt Text komplett zu ersetzen; die Sperre gegen das Speichern einer leeren Seite fängt eine Katastrophe ab, aber kein gut gemeintes Neuschreiben. Und ist eine Seite nicht falsch, sondern überholt, schreib das oben hin und verlinke die Seite, die sie ablöst, statt sie zu löschen: Ein Link, der irgendwohin führt, schlägt einen, der ins Leere läuft.

Die Liste **Kürzlich aktualisiert** auf der Startseite ist das, was einer Wissensdatenbank am nächsten an einem Herzschlag kommt. Hat sich dort seit Monaten nichts bewegt, folgt die Dokumentation der Wirklichkeit nicht mehr — und das sieht man meist lange, bevor sich jemand daran verbrennt.

## Gewohnheiten, die eine Wissensdatenbank am Leben halten

- **Eine Seite, ein Thema.** Braucht eine Seite zwei Überschriften, die je ein Titel sein könnten, sind es zwei Seiten — und eine davon ist Unterseite der anderen.
- **Verlinke den Vorgang, statt ihn nachzuerzählen.** Ein `@`-Chip bleibt richtig, während die Arbeit weitergeht; ein Absatz, der das Ticket zusammenfasst, ist binnen einer Woche falsch.
- **Schreib die Warnung zuerst.** Der Satz, den jemand am dringendsten braucht, gehört in eine farbige Box weit oben, nicht ans Ende einer Textwand.
- **Repariere, was dir auffällt.** Du darfst es ohnehin bearbeiten. Ein Wiki verfällt viel häufiger an Höflichkeit als an Vandalismus.
- **Lass die Gliederung navigieren.** Echte Überschriften ergeben die Liste *Auf dieser Seite* — und Überschriften sind ohnehin das, was Überfliegende zuerst lesen.

## Nächste Schritte

- Häng Dokumentation an die Arbeit, die sie beschreibt: [Mit Vorgängen arbeiten](/de/guide-issues.html).
- Lerne die schnellsten Wege zurück zu einer Seite: [Dinge finden](/de/guide-search.html).
- Wie Projekt- und Teamzugriff vergeben wird: [Projekte & Teams](/de/guide-projects.html).
