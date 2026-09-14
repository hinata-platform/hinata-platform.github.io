---
title: Mit Vorgängen arbeiten
description: Vorgänge anlegen, bearbeiten, verknüpfen, klonen, verschieben, archivieren und exportieren.
---

# Mit Vorgängen arbeiten

Fast alles in Hinata passiert an einem **Vorgang**: ein Fehler, ein Feature, ein Epic, eine kleine Aufgabe. Board, Timeline und Berichte zeigen dieselben Vorgänge nur unterschiedlich an.

## Was ein Vorgang ist

Ein Vorgang ist ein Stück Arbeit mit Titel, Status und Kommentaren. Er gehört zu genau einem Projekt und trägt dessen Schlüssel plus Nummer, etwa `HIN-42` oder `WEB-7`.

!!! note "Der Schlüssel bleibt"
    Jede Nummer wird nur einmal vergeben, auch wenn der Vorgang gelöscht wird. Nur beim Umzug in ein anderes Projekt bekommt er einen neuen Schlüssel, und der alte löst nicht mehr auf.

## Einen Vorgang anlegen

Alle Wege öffnen dasselbe Formular:

- Bernsteinfarbener Button **Neue Aufgabe** oben in der dunkelblauen Seitenleiste (auf jeder Seite)
- Button **Neue Aufgabe** rechts oben auf der Seite **Issues**
- **⌘K** (**Strg+K** unter Windows und Linux), „neu“ tippen, **Neuen Vorgang erstellen**
- **Sub-Task hinzufügen** oder **Untervorgang hinzufügen** an einem offenen Vorgang. Der neue hängt direkt daran.
- Auf dem Board: das Eingabefeld unten in einer Spalte. Der Vorgang bekommt den Status dieser Spalte.

### Was die Felder bedeuten

Pflicht sind nur Projekt und Titel.

![Der Dialog „Neue Aufgabe“](/assets/img/shot-issue-create.png)
*Projekt, Status, Priorität und Typ sind vorbelegt, der Rest bleibt leer.*

| Feld | Wofür es da ist |
| --- | --- |
| **Projekt** | Bestimmt Schlüssel, Status und Stichwörter. Du siehst nur Projekte, in denen du Mitglied bist. |
| **Titel** | Eine verständliche Zeile für Listen, Karten und Suche. |
| **Beschreibung** | Was, warum, wann fertig. Siehe [Mit dem Editor schreiben](#mit-dem-editor-schreiben). |
| **Status** | Die Spalte auf dem Board, aus dem Workflow des Projekts. |
| **Zugewiesene Person** | Wer die Arbeit macht. Leer: **Nicht zugewiesen**. In der Detailansicht gibt es **Mir zuweisen**. |
| **Priorität** | Showstopper, Kritisch, Hohe Priorität, Normal, Gering oder Sehr gering. Standard: **Normal**. |
| **Typ** | Epic, Story, Aufgabe, Fehler, Feature oder Sub-Task, siehe [Den richtigen Typ wählen](#den-richtigen-typ-wählen). |
| **Story Points** | Größe, keine Stunden. Zählt für Sprintkapazität und Velocity. |
| **Stichwort** | Farbige Schlagworte wie `frontend`, `needs-design`, `regression`. Neue legst du im Picker an. |
| **Sprint** | Leer heißt: Backlog. |
| **Epic** / **Übergeordnet** | Der Vorgang eine Ebene darüber („Übergeordnet“ bei Sub-Tasks). |
| **Startdatum** / **Fälligkeitsdatum** | Der Balken auf der [Timeline](/de/guide-timeline.html). Überschrittene Fälligkeit ist in Listen rot. |

!!! tip "Titel, die man wiederfindet"
    Statt „Login kaputt“ lieber „Login schlägt mit 500 fehl, wenn die E-Mail ein Plus enthält“.

## Den richtigen Typ wählen

Der Typ bestimmt Icon, Farbe und Ebene:

```text
Epic
└─ Story · Aufgabe · Fehler · Feature
   └─ Sub-Task
```

| Typ | Wofür | Ebene |
| --- | --- | --- |
| **Epic** | Thema über viele Sprints | Oben |
| **Story** | Nutzen aus Sicht der Nutzenden | Mitte, kann Sub-Tasks haben |
| **Aufgabe** | Arbeit ohne Außenwirkung, etwa eine Migration | Mitte |
| **Fehler** | Etwas ist kaputt | Mitte |
| **Feature** | Neue Fähigkeit | Mitte |
| **Sub-Task** | Ein Schritt in einem Vorgang der Mitte | Unten, hat immer etwas über sich |

Faustregel: Schiebst du es allein durch den Workflow, ist es Mitte. Ergibt es nur als Teil von etwas Sinn, ist es ein Sub-Task. Ist es zu groß zum Fertigwerden, ist es ein Epic.

!!! note "Sub-Tasks reisen mit"
    Archivierst oder stellst du den Vorgang darüber wieder her, gilt das auch für seine Sub-Tasks. Nimm sie also nicht für Arbeit, die du getrennt priorisieren willst.

### Die Hierarchie aufbauen

- **Von unten**: In der Detailspalte **Epic** setzen (bei Sub-Tasks **Übergeordnet**). Der Picker zeigt zuerst die letzten Epics.
- **Von oben**: **Untervorgang hinzufügen** am Epic oder **Sub-Task hinzufügen** an der Story.
- **Lösen**: **Kein Epic** wählen. Das Kind bleibt als eigener Vorgang bestehen.

Die Karte **Sub-Tasks** und das Abzeichen in Listen zeigen den Fortschritt, etwa „3 von 7 erledigt“. Das [Board](/de/guide-boards.html) kann Swimlanes nach Epic bilden oder auf ein Epic filtern.

## Den passenden Vorgang finden

Die Seite **Issues** listet alle Vorgänge, die du sehen darfst. Die Zahl unter der Überschrift zeigt, wie viele gerade angezeigt werden.

![Die Vorgangsliste in Hinata](/assets/img/shot-issues.png)
*Das Abzeichen `0/1` zählt erledigte Sub-Tasks, rote Daten sind überfällig.*

- **Gruppieren nach**: Keine, Status, Priorität, Zugewiesene Person, Projekt oder Typ
- **Sortieren**: Neueste, Älteste oder nach Änderungsdatum
- **Filter**: fünf Kategorien mit Mehrfachauswahl, dazu der Schalter **Archiviert**
- **Zeitraum**: Überfällig, Bis heute fällig, Diese Woche, Nächste 7 Tage, eigener Zeitraum und mehr
- **Exportieren**: die ganze gefilterte Ergebnismenge als PDF, CSV oder JSON

![Das Filter-Popover in der Vorgangsliste](/assets/img/shot-issue-filter.png)
*Ein Reiter pro Kategorie, die Schaltfläche zählt aktive Filter.*

Einen bestimmten Vorgang findest du schneller über die [Befehlspalette](/de/guide-search.html).

## Der Vorgang im Detail

Links der Inhalt, rechts die Fakten.

![Ein Hinata-Vorgang in der Detailansicht](/assets/img/shot-issue.png)
*Links Titel, Beschreibung und Sub-Tasks, rechts Details, Deployment und Timeline.*

### Die Kopfzeile

Pfeil zurück, Schlüssel und Status.

![Das Aktionsmenü an einem Vorgang](/assets/img/shot-issue-actions-menu.png)
*Das Menü **…**: „Beobachten“, „Exportieren …“, „Klonen …“, „In Projekt verschieben …“ und „Löschen“.*

### Die Hauptspalte

- **Titel** und **Beschreibung**: doppeltippen (Doppelklick) zum Bearbeiten
- **Sub-Tasks** (bei Epics **Untergeordnete Vorgänge**): mit Fortschritt und Feld zum Ergänzen
- **Verknüpfte Vorgänge**: siehe [Vorgänge miteinander verknüpfen](#vorgänge-miteinander-verknüpfen)
- **Anhänge**: siehe [Kommentare & Anhänge](/de/guide-collaboration.html)
- **Aktivität**: Tabs **Alle**, **Kommentare** und **Verlauf**

### Die Detailspalte

Klick auf einen Wert öffnet einen Picker für **Status**, **Zugewiesene Person** (mit **Mir zuweisen**), **Priorität**, **Typ**, **Epic** oder **Übergeordnet**, **Story Points**, **Stichwort** und **Sprint**. Nur **Autor** ist fest.

Die Karte **Timeline** enthält **Startdatum**, **Fälligkeitsdatum**, **Zeit erfassen** und nach dem Buchen etwa „1 Std. 30 Min. von 4 Std. aufgewendet“ (siehe [Zeit erfassen](/de/guide-time.html)). Ganz unten steht „Erstellt vor 3 Tagen“ oder „Aktualisiert vor …“.

!!! note "Karte Deployment nur mit Repository"
    Ist das Projekt mit GitHub, GitLab oder Bitbucket verbunden, zeigt **Deployment** Branches, Commits und Pull Requests mit dem Schlüssel, dazu Abkürzungen für Namen von Branch oder Commit. Verbinden können Administration oder Projektleitung, siehe [Git-Integration](/de/git-integration.html).

## Einen Vorgang bearbeiten

- **Felder rechts** speichern sofort. Eine Karte auf dem Board in eine andere Spalte ziehen ändert den Status.
- **Titel und Beschreibung**: doppeltippen, ändern, **Speichern** oder **Abbrechen**.

Änderungen anderer erscheinen live, ohne Neuladen und ohne etwas zu überschreiben.

!!! tip "Beobachter erfahren es"
    Feldänderungen benachrichtigen Beobachter, zugewiesene und erstellende Person. Siehe [Auf dem Laufenden bleiben](/de/guide-notifications.html).

## Den Aktivitätsverlauf lesen

- **Alle**: Kommentare und Änderungen zusammen, gut zum Aufholen
- **Kommentare**: nur Geschriebenes, der Standardtab
- **Verlauf**: nur Änderungen wie „hat den Status geändert“, mit Person und Zeitpunkt

Den Verlauf schreibt Hinata automatisch, niemand kann ihn bearbeiten.

## Einen Link zum Vorgang teilen

Klick auf den Schlüssel in der Kopfzeile (`HIN-42`) kopiert den Link. Ein grüner Haken bestätigt es. Der Link öffnet die App, falls installiert, sonst den Browser. Empfänger brauchen ein Konto auf deinem Server und Zugriff aufs Projekt.

## Mit dem Editor schreiben

Beschreibung und Kommentare nutzen denselben Editor. Die Werkzeugleiste bietet **Textstil** (Fließtext, Überschrift 1 bis 3), **Fett**, **Kursiv**, **Unterstrichen**, **Durchgestrichen**, **Inline-Code**, **Aufzählung**, **Nummerierte Liste**, **Aufgabenliste**, **Zitat**, **Link**, **Codeblock** (mit Sprachauswahl), **Tabelle**, **Trennlinie**, **Bild einfügen**, **Infobox**, **Warnung**, **Notiz**, **Tipp**, Rückgängig und Wiederholen.

- **`@`** sucht Vorgänge, Artikel der Wissensdatenbank und Personen. Ein Vorgang wird zum Chip, der Umbenennung und Status live mitzieht. Eine Person wird benachrichtigt.
- **Bilder** einfügen oder einsetzen lädt sie auf deinen Server. Auf dem Handy bietet **+** Kamera und Fotomediathek.

!!! tip "Markdown-Kürzel"
    Bindestrich am Zeilenanfang für Aufzählung, `1.` für nummerierte Liste, `#` für Überschrift, Backticks für Inline-Code.

## Vorgänge miteinander verknüpfen

In der Karte **Verknüpfte Vorgänge**: **Vorgang hinzufügen**, links eine der dreizehn Arten wählen, rechts Titel, Schlüssel oder URL eingeben (auch mehrere), dann **Verknüpfen**.

![Eine Verknüpfungsart wählen](/assets/img/shot-issue-link.png)
*Verknüpfungsart links, Suchfeld rechts, bestehende Verknüpfungen darüber.*

| Beziehung | Liest sich als | Wann |
| --- | --- | --- |
| **wird blockiert von** / **blockiert** | „HIN-42 wird blockiert von HIN-40“ | Arbeit kann erst starten, wenn die andere fertig ist |
| **dupliziert** / **wird dupliziert von** | „HIN-42 dupliziert HIN-11“ | Doppelt gemeldet |
| **hängt zusammen mit** | Von beiden Seiten gleich | Lose verbunden, keine Abhängigkeit |
| **klont** / **wird geklont von** | Beim [Klonen](#einen-vorgang-klonen) automatisch | Kopie und Original |
| **testet** / **wird getestet von** | „HIN-90 testet HIN-42“ | Test oder QA zu einer Arbeit |
| **aufgeteilt in** / **aufgeteilt aus** | „HIN-42 aufgeteilt in HIN-55“ | Zu groß, in mehrere geteilt |
| **hat erstellt** / **erstellt von** | Herkunft | Eine Arbeit hat eine andere ausgelöst |

Der andere Vorgang zeigt die Gegenrichtung sofort live an.

!!! info "Nur *blockiert* wirkt auf die Planung"
    Nur **blockiert** zeichnet die [Timeline](/de/guide-timeline.html) als Pfeil und zählt für den kritischen Pfad. Alle anderen Arten verschieben nie ein Datum.

## Einen Vorgang beobachten

**…** → **Beobachten**. Du bekommst Kommentare und Änderungen, bis du es ausschaltest. Das Popover zeigt alle Beobachter. Zugewiesene und erstellende Person werden ohnehin benachrichtigt, das Popover sagt es dann. Alles Beobachtete steht auf der Seite **Beobachtet**.

## Einen Vorgang klonen

**… → Klonen …** kopiert den Vorgang ins selbe Projekt, etwa als Vorlage.

![Der Klon-Dialog](/assets/img/shot-issue-clone.png)
*Titel mit Präfix „CLONE -“, die Schalter „Anhänge“, „Verknüpfungen“ und „Sprint-Werte“ sind aus.*

- Anhänge werden als eigene Dateien kopiert.
- Eine Verknüpfung **klont** zum Original entsteht immer, und **du** bist Autor.
- Kommentare, Arbeitszeiten und Verlauf bleiben beim Original.

## Einen Vorgang in ein anderes Projekt verschieben

**… → In Projekt verschieben …**: erst Zielprojekt wählen, dann die Status zuordnen. Hinata ordnet vorab zu, was passt, und zeigt Folgen und neue Schlüssel.

![Schritt zwei des Verschiebe-Assistenten](/assets/img/shot-issue-move.png)
*Aus HIN-4 wird MOB-9, die drei Sub-Tasks ziehen mit.*

Der alte Schlüssel löst danach nicht mehr auf.

!!! warning "Archivierte Vorgänge zuerst wiederherstellen"
    Für archivierte Vorgänge ist der Eintrag deaktiviert.

## Archivieren und löschen

**Archivieren** darf jedes Projektmitglied. Der Vorgang verschwindet aus Listen, Boards, Sprints und Suche, bleibt aber erhalten. Filter **Archiviert** findet ihn, **Wiederherstellen** holt ihn zurück. Sub-Tasks von Story, Aufgabe, Fehler und Feature gehen mit.

**Löschen** dürfen nur Admins der Plattform, Projektleitungen und Admins eines Teams, dem das Projekt gehört. Alle anderen sehen nur **Archivieren**. Wer löschen darf, bekommt im Dialog beides, Löschen in Rot.

!!! warning "Löschen ist endgültig"
    Kommentare, Arbeitszeiten, Verknüpfungen und Verlauf verschwinden mit. Bei **Story, Aufgabe, Fehler oder Feature** auch die Sub-Tasks. Bei einem **Epic** bleiben die Kinder als normale Vorgänge und verlieren nur die Verbindung. Im Zweifel archivieren.

## Einen Vorgang exportieren oder drucken

**… → Exportieren …** bietet **Drucken**, **Als PDF exportieren**, **Als Excel-Datei exportieren**, **Als Word-Datei exportieren** und **Als XML-Datei exportieren**.

- Der Server erzeugt alles, das Layout ist auf jedem Gerät gleich. Drucken nutzt dasselbe PDF.
- Enthalten: Felder, Beschreibung, Kommentare, verknüpfte Vorgänge, Liste der Anhänge, Änderungsverlauf.
- Excel hat zwei Blätter (Felder und Kommentare), XML ist maschinenlesbar.
- iOS, Android, macOS und Windows öffnen das Menü zum Teilen. Linux speichert in den Ordner Downloads und nennt den Dateinamen. Im Web übernimmt der Browser.

!!! tip "Ganze Liste exportieren"
    **Exportieren** auf der Seite **Issues** exportiert die aktuelle Liste samt Filtern und Gruppierung als PDF, CSV oder JSON.

## Verwandte Seiten

- **[Boards & Sprints](/de/guide-boards.html)**: Workflow, Sprints, Backlog
- **[Kommentare & Anhänge](/de/guide-collaboration.html)**: Unterhaltung, Dateien, Sprachnachrichten
- **[Timeline & Abhängigkeiten](/de/guide-timeline.html)**: Daten und *blockiert* im Diagramm
- **[Zeit erfassen](/de/guide-time.html)**: Arbeit buchen, Stundenzettel
- **[Auf dem Laufenden bleiben](/de/guide-notifications.html)**: wer was erfährt
- **[Dinge finden](/de/guide-search.html)**: ⌘K-Palette, Filter und Suche
