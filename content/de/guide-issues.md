---
title: Mit Vorgängen arbeiten
description: Vorgang anlegen, jedes Feld verstehen, die Hierarchie von Epic bis Sub-Task nutzen, verknüpfen, beobachten, klonen, lieber archivieren als löschen und exportieren.
---

# Mit Vorgängen arbeiten

Fast alles, was du in Hinata tust, passiert an einem **Vorgang**. Ein Fehler, den gerade jemand gemeldet hat, das Feature aus dem laufenden Sprint, das Epic für das nächste Quartal, die Zwei-Minuten-Aufgabe auf einer Checkliste — das sind alles Vorgänge, und sie verhalten sich alle gleich. Wenn du diese Seite kennst, erklären sich Board, Timeline und Berichte von selbst: Sie sind nur verschiedene Blicke auf dasselbe.

## Was ein Vorgang ist

Ein Vorgang ist ein Stück Arbeit mit einem Namen, einem Status und einem Ort, an dem darüber gesprochen wird. Er gehört zu genau einem Projekt und trägt dessen Schlüssel plus eine Nummer: `HIN-42`, `WEB-7`. Über diesen Schlüssel sprichst du überall darüber — im Chat, in einem Commit, laut im Daily.

!!! note "Der Schlüssel bleibt"
    Eine Nummer wird einmal vergeben und nie wieder verwendet, auch wenn der Vorgang später gelöscht wird. Ein Schlüssel, den du heute in ein Dokument kopierst, zeigt also in zwei Jahren noch auf dieselbe Sache. Nur wenn ein Vorgang in ein anderes Projekt umzieht, bekommt er dort einen neuen Schlüssel, und der alte löst nicht mehr auf.

## Einen Vorgang anlegen

Es gibt vier Wege hinein, und alle öffnen dasselbe Formular:

- Der bernsteinfarbene Button **Neue Aufgabe** oben in der dunkelblauen Seitenleiste — immer da, egal auf welcher Seite du bist.
- Der Button **Neue Aufgabe** rechts oben auf der Issues-Seite.
- Die Befehlspalette: **⌘K** (**Strg+K** unter Windows und Linux), „neu“ tippen, **Neuen Vorgang erstellen** wählen.
- **Sub-Task hinzufügen** oder **Untervorgang hinzufügen** an einem bereits geöffneten Vorgang — das legt den neuen Vorgang an *und* hängt ihn in einem Schritt an den übergeordneten.

Auf dem Board gibt es einen fünften: den Inline-Composer unten in einer Spalte, der einen neuen Vorgang direkt im Status dieser Spalte anlegt.

### Was die Felder bedeuten

Pflicht sind nur Projekt und Titel — alles andere darf leer bleiben und später ergänzt werden, von dir oder von der Person, die die Arbeit übernimmt.

![Der Dialog „Neue Aufgabe“](/assets/img/shot-issue-create.png)
*„Neue Aufgabe“: links Titel und Beschreibung, rechts „Details“ und „Timeline“ übereinander. Projekt, Status, Priorität und Typ kommen bereits gesetzt; zugewiesene Person, Epic, Story Points, Stichwort, Sprint und beide Datumsfelder bleiben leer, bis sie jemand füllt. „Speichern“ ist die einzige Schaltfläche unten.*

| Feld | Wofür es da ist |
| --- | --- |
| **Projekt** | In welchem Projekt der Vorgang lebt. Bestimmt Schlüssel, verfügbare Status und Stichwort-Set. Du siehst nur Projekte, in denen du Mitglied bist. |
| **Titel** | Eine Zeile, so geschrieben, dass eine fremde Person versteht, worum es geht. Das erscheint in Listen, auf Karten und in Suchergebnissen. |
| **Beschreibung** | Die ganze Geschichte: was, warum, woran man merkt, dass es fertig ist. Formatierter Text — siehe [Mit dem Editor schreiben](#mit-dem-editor-schreiben). |
| **Status** | In welcher Board-Spalte der Vorgang steht. Die Auswahl kommt aus dem Workflow des Projekts, das „In Review“ des einen Projekts kann im anderen „QA“ heißen. |
| **Zugewiesene Person** | Wer die Arbeit macht. Bleibt das Feld leer, steht dort **Nicht zugewiesen**; in der Detailansicht gibt es die Abkürzung **Mir zuweisen**. |
| **Priorität** | Showstopper, Kritisch, Hohe Priorität, Normal, Gering oder Sehr gering. Neue Vorgänge starten auf **Normal**. |
| **Typ** | Epic, Story, Aufgabe, Fehler, Feature oder Sub-Task — siehe [Den richtigen Typ wählen](#den-richtigen-typ-wahlen). |
| **Story Points** | Deine Schätzung der Größe, nicht der Stunden. Fließt in Sprint-Kapazität und Velocity-Bericht ein. |
| **Stichwort** | Wiederverwendbare, farbige Schlagworte des Projekts — `frontend`, `needs-design`, `regression`. Neue kannst du direkt im Picker anlegen. |
| **Sprint** | In welchen Sprint der Vorgang geplant ist. Leer heißt: er liegt im Backlog. |
| **Epic** / **Übergeordnet** | Der Vorgang eine Ebene darüber. Bei einem normalen Vorgang heißt die Zeile „Epic“, bei einem Sub-Task „Übergeordnet“. |
| **Startdatum** / **Fälligkeitsdatum** | Der Balken, den dieser Vorgang auf der [Timeline](/de/guide-timeline.html) zeichnet. Ein Fälligkeitsdatum in der Vergangenheit erscheint in jeder Liste rot. |

!!! tip "Schreib den Titel für die Person, die ihn in sechs Monaten findet"
    „Login kaputt“ ist ein Titel, den du in einem Suchergebnis nicht wiedererkennst. „Login schlägt mit 500 fehl, wenn die E-Mail ein Plus enthält“ schon. Die Beschreibung darf so lang sein, wie sie sein muss — der Titel ist der Teil, der auf einen Blick funktionieren muss.

## Den richtigen Typ wählen

Der Typ bestimmt Icon und Farbe und — wichtiger — wo der Vorgang in der Hierarchie stehen darf. Hinata kennt drei Ebenen:

```text
Epic
└─ Story · Aufgabe · Fehler · Feature
   └─ Sub-Task
```

| Typ | Wofür | Ebene |
| --- | --- | --- |
| **Epic** | Ein Thema über viele Sprints — „Self-Service-Onboarding“ | Oben. Bündelt die Vorgänge, die es liefern |
| **Story** | Ein Stück Wert, aus Sicht der Nutzenden beschrieben | Mitte. Kann an einem Epic hängen und Sub-Tasks tragen |
| **Aufgabe** | Arbeit ohne direkte Außenwirkung — eine Migration, ein Spike | Mitte |
| **Fehler** | Etwas ist kaputt | Mitte |
| **Feature** | Eine Fähigkeit, die gebaut wird, wenn „Story“ zu förmlich wirkt | Mitte |
| **Sub-Task** | Ein Schritt innerhalb eines Vorgangs der mittleren Ebene — „Migration schreiben“ | Unten. Hat immer etwas über sich |

Die praktische Regel: Wenn du es aufs Board legen und für sich durch einen Workflow schieben würdest, ist es ein Vorgang der mittleren Ebene. Wenn es nur als Teil von etwas anderem Sinn ergibt, ist es ein Sub-Task. Wenn es zu groß ist, um fertig zu werden, und du den Fortschritt über viele Vorgänge sehen willst, ist es ein Epic.

!!! note "Sub-Tasks reisen mit ihrem Elternvorgang"
    Ein Sub-Task steht nie allein. Archivierst du den Vorgang darüber, wird er mit archiviert; stellst du diesen wieder her, kommt er zurück. Das ist Absicht — deshalb sind Sub-Tasks der richtige Ort für Checklisten-Arbeit und der falsche für alles, was du einmal getrennt umpriorisieren möchtest.

### Die Hierarchie aufbauen

Du musst den Baum nie vorab planen. Häng die Dinge an, sobald sie klar werden:

- **Von unten**: Vorgang öffnen und in der Detailspalte **Epic** (oder bei einem Sub-Task **Übergeordnet**) setzen. Es öffnet sich ein durchsuchbarer Picker, der zuerst die letzten Epics zeigt.
- **Von oben**: Ein Epic öffnen und **Untervorgang hinzufügen** benutzen, oder eine Story öffnen und **Sub-Task hinzufügen**. Der neue Vorgang entsteht bereits verbunden, im selben Projekt.
- **Lösen**: Derselbe Picker hat einen Eintrag **Kein Epic**. Das Kind verschwindet nicht — es wird wieder ein Vorgang der obersten Ebene.

Sobald eine Hierarchie existiert, arbeitet sie für dich. Die Sub-Task-Karte zeigt eine Fortschrittszeile „3 von 7 erledigt“, der wahre Stand eines Vorgangs ist also sichtbar, ohne dass du etwas öffnest. Listen zeigen neben dem Titel ein kleines Abzeichen mit derselben Zahl. Und das [Board](/de/guide-boards.html) kann in Swimlanes nach Epic gruppieren oder auf ein einziges Epic filtern — aus einem vollen Board wird so genau die Arbeit, die zu einem Thema gehört.

## Den passenden Vorgang finden

Die Seite **Issues** listet alles, was du über deine Projekte hinweg sehen darfst. Die Zahl unter der Überschrift sagt, wie viele Vorgänge gerade in der Ansicht sind, die Werkzeugleiste engt sie ein.

![Die Vorgangsliste in Hinata](/assets/img/shot-issues.png)
*Die Listenansicht: ID, Titel, Status, Priorität, Bearbeiter und Fällig, oben Gruppieren nach, Sortieren, Filter und Zeitraum, rechts der Export. Das kleine Abzeichen neben einem Titel (hier `0/1`) zählt erledigte Sub-Tasks; ein rotes Fälligkeitsdatum ist überfällig.*

- **Gruppieren nach** — Keine, Status, Priorität, Zugewiesene Person, Projekt oder Typ. Gruppieren macht aus der flachen Liste beschriftete Abschnitte — der schnellste Weg zu sehen, wo ein Projekt Schlagseite hat.
- **Sortieren** — Neueste oder Älteste zuerst, oder nach Änderungsdatum.
- **Filter** — fünf Kategorien, jeweils mehrfach wählbar, dazu ein Schalter **Archiviert**, der weich gelöschte Vorgänge zurück in die Ansicht holt.
- **Zeitraum** — Überfällig, Bis heute fällig, Diese Woche, Nächste 7 Tage, ein eigener Zeitraum und so weiter.
- **Exportieren** — schreibt die aktuelle, gefilterte Liste als PDF, CSV oder JSON. Dabei wird die komplette Ergebnismenge durchblättert, nicht nur die sichtbaren Zeilen.

![Das Filter-Popover in der Vorgangsliste](/assets/img/shot-issue-filter.png)
*„Filter“ ist ein einziges Popover, keine fünf Bedienelemente: ein Reiter pro Kategorie, darunter die Optionen der aktiven, mit einem Haken an jedem gewählten Wert. Zwei sind hier an, deshalb trägt die Schaltfläche in der Werkzeugleiste eine 2 und unten im Popover steht „2 aktiv“ neben „Zurücksetzen“ und dem Schalter „Archiviert“. Die Unterzeile zählt, was der Filter übrig lässt — 14 von 14 Vorgängen, gegenüber den 57 einer ungefilterten Liste.*

Ein Klick auf eine Zeile öffnet den Vorgang. Um einen bestimmten Vorgang über seinen Schlüssel oder über Wörter im Text zu finden, ist die [Befehlspalette](/de/guide-search.html) schneller als jeder Filter.

## Der Vorgang im Detail

Ein geöffneter Vorgang sieht überall gleich aus: eine breite Hauptspalte für den Inhalt, eine schmale rechte Spalte für die Fakten.

![Ein Hinata-Vorgang in der Detailansicht](/assets/img/shot-issue.png)
*Links: der Titel, dann die Beschreibung — Überschrift, Liste, Codeblock, Tabelle und Zitat, alles an Ort und Stelle dargestellt —, darunter die Sub-Task-Karte, und über allem schwebt der Kommentar-Composer. Verknüpfte Vorgänge und das Anhang-Raster folgen weiter unten in derselben Spalte. Rechts: die Details-Karte, eine Deployment-Karte für das verbundene Repository und die Timeline-Karte mit „Zeit erfassen“.*

### Die Kopfzeile

Zurück-Pfeil, Vorgangsschlüssel und der aktuelle Status als farbiger Chip.

![Das Aktionsmenü an einem Vorgang](/assets/img/shot-issue-actions-menu.png)
*Das Menü **…** rechts oben trägt alles, was kein Feld ist: „Beobachten“, „Exportieren …“, „Klonen …“, „In Projekt verschieben …“ und, als Einziges in Rot, „Löschen“. Vier der folgenden Abschnitte beginnen hier.*

### Die Hauptspalte

- **Titel** — Doppeltippen (Doppelklick) bearbeitet ihn an Ort und Stelle.
- **Beschreibung** — genauso, und sie zeigt alles, was der Editor kann: Überschriften, Listen, Tabellen, Codeblöcke, Infoboxen, Bilder und lebende Links auf andere Vorgänge.
- **Sub-Tasks** (an einem Epic: **Untergeordnete Vorgänge**) — eine Karte mit allem, was darunter hängt, einer Fortschrittszeile „2 von 5 erledigt“ und einem Inline-Feld, um ohne Seitenwechsel etwas zu ergänzen.
- **Verknüpfte Vorgänge** — die Beziehungen zu anderen Vorgängen; siehe [Vorgänge miteinander verknüpfen](#vorgange-miteinander-verknupfen).
- **Anhänge** — eine Ablagefläche und ein Raster mit Dateien. [Kommentare & Anhänge](/de/guide-collaboration.html) behandelt das ausführlich.
- **Aktivität** — Unterhaltung und Protokoll, auf drei Tabs: **Alle**, **Kommentare** und **Verlauf**.

### Die Detailspalte

Jede Zeile ist bearbeitbar: Wert anklicken, ein durchsuchbarer Picker öffnet sich.

**Status**, **Zugewiesene Person** (mit der Abkürzung **Mir zuweisen**), **Priorität**, **Typ**, **Epic** oder **Übergeordnet**, **Story Points**, **Stichwort**, **Sprint** und **Autor** — wer den Vorgang erstellt hat, die einzige Zeile, die du nicht ändern kannst.

Darunter trägt die Karte **Timeline** das **Startdatum**, das **Fälligkeitsdatum**, den Link **Zeit erfassen** und eine Zeile „1 Std. 30 Min. von 4 Std. aufgewendet“, sobald jemand Zeit gebucht hat. [Zeit erfassen](/de/guide-time.html) erklärt diese Seite.

Ganz unten steht leise „Erstellt vor 3 Tagen“, das nach der ersten Änderung zu „Aktualisiert vor …“ wechselt.

!!! note "Die Deployment-Karte erscheint nur mit verbundenem Repository"
    Ist dein Projekt mit GitHub, GitLab oder Bitbucket verbunden, zeigt eine Karte **Deployment** Branches, Commits und Pull Requests, die den Schlüssel dieses Vorgangs nennen, dazu Abkürzungen zum Anlegen eines Branch- oder Commit-Namens. Kein verbundenes Repository heißt: keine Karte — nichts ist kaputt. Das Verbinden ist Sache der Administration oder der Projektleitung und steht in der [Git-Integration](/de/git-integration.html).

## Einen Vorgang bearbeiten

Für die Felder rechts gibt es keinen Bearbeitungsmodus und keinen Speichern-Button: Neuen Wert wählen, fertig gespeichert. Dasselbe gilt fürs Ziehen einer Karte in eine andere Board-Spalte — das ist das Feld Status, nur von woanders geändert.

Titel und Beschreibung sind die Ausnahme, weil du dort tippst statt wählst: **doppeltippen**, ändern, dann **Speichern** oder **Abbrechen**.

Jede Änderung wird protokolliert. Unter **Aktivität → Verlauf** siehst du, wer Status, zugewiesene Person, Datum oder Stichwörter geändert hat, und wann. Und weil der Vorgang live ist, überschreibt dir eine Kollegin, die denselben Vorgang bearbeitet, nichts: Ihre Änderung erscheint dort, wo du gerade hinschaust, ohne Neuladen.

!!! tip "Beobachter erfahren es"
    Eine Feldänderung benachrichtigt die Personen, die den Vorgang beobachten, dazu die zugewiesene Person und die erstellende Person — du musst also kein „Fälligkeitsdatum geändert, zur Info“ in die Kommentare schreiben. Wer was bekommt, steht in [Auf dem Laufenden bleiben](/de/guide-notifications.html).

## Den Aktivitätsverlauf lesen

Der Abschnitt **Aktivität** unten am Vorgang hat drei Tabs:

- **Alle** — Unterhaltung und Änderungen ineinander verwoben, als eine Zeitleiste. Der richtige Tab, wenn du einen länger nicht angesehenen Vorgang aufholst.
- **Kommentare** — nur das, was Menschen geschrieben haben. Damit startet ein Vorgang, denn meistens ist die Diskussion der Grund, warum du gekommen bist.
- **Verlauf** — nur, was sich geändert hat: „hat den Status geändert“, „hat die zugewiesene Person geändert“, „hat das Fälligkeitsdatum geändert“, mit Person und Zeitpunkt.

Der Verlauf wird automatisch geschrieben und lässt sich nicht bearbeiten — genau das macht ihn vertrauenswürdig. Wenn jemand fragt „seit wann ist das dringend?“, steht die Antwort auf diesem Tab.

## Einen Link zum Vorgang teilen

Klick auf den Vorgangsschlüssel in der Kopfzeile — `HIN-42` — und ein Link darauf liegt in deiner Zwischenablage, bestätigt durch einen grünen Haken und einen kleinen Hinweis. Den kannst du in Chat, E-Mail oder ein Dokument einfügen.

Der Link ist ein Deep Link. Hat dein Gegenüber die App installiert, öffnet er den Vorgang in der App, sonst im Browser. In beiden Fällen braucht die Person ein Konto auf deinem Server und Zugriff auf das Projekt — ein Link ist eine Abkürzung, kein Schlüssel.

## Mit dem Editor schreiben

Beschreibung und jeder Kommentar benutzen denselben Editor für formatierten Text; einmal lernen genügt.

Die Werkzeugleiste bietet **Textstil** (Fließtext, Überschrift 1–3), **Fett**, **Kursiv**, **Unterstrichen**, **Durchgestrichen**, **Inline-Code**, **Aufzählung**, **Nummerierte Liste**, **Aufgabenliste**, **Zitat**, **Link**, **Codeblock** (mit Sprachauswahl), **Tabelle**, **Trennlinie**, **Bild einfügen**, Infoboxen — **Infobox**, **Warnung**, **Notiz**, **Tipp** — sowie Rückgängig und Wiederholen.

Zwei Dinge lohnen sich über die Buttons hinaus:

- **Tippe `@`, um etwas zu verlinken.** Es öffnet sich ein Menü, das gleichzeitig Vorgänge, Artikel der Wissensdatenbank und Personen durchsucht. Wählst du einen Vorgang, entsteht ein lebender Chip mit Schlüssel und aktuellem Status — wird der Vorgang umbenannt oder erledigt, zieht der Chip mit. Wählst du eine Person, ist es eine Erwähnung, und sie wird benachrichtigt.
- **Bilder lassen sich einfügen oder einsetzen**, sie landen beim Schreiben im Speicher deines Servers. Auf dem Handy bietet der **+**-Button des Composers direkt Kamera und Fotomediathek an.

!!! tip "Markdown-Kürzel funktionieren weiterhin"
    Beginne eine Zeile mit einem Bindestrich für eine Aufzählung, mit `1.` für eine nummerierte Liste, mit `#` für eine Überschrift, oder setz ein Wort in Backticks für Inline-Code. Wer ohnehin in Markdown denkt, darf die Werkzeugleiste komplett ignorieren.

## Vorgänge miteinander verknüpfen

Die Karte **Verknüpfte Vorgänge** hält fest, wie dieser Vorgang zu anderen steht.

![Eine Verknüpfungsart wählen](/assets/img/shot-issue-link.png)
*„Vorgang hinzufügen“ öffnet eine Zeile direkt in der Karte: links die Verknüpfungsart, rechts ein Feld, das einen Teil des Titels, einen Vorgangsschlüssel oder eine eingefügte URL annimmt. Das Menü der Verknüpfungsarten hält dreizehn Verben — es scrollt über die elf sichtbaren hinaus — und die vorhandenen Verknüpfungen stehen darüber, nach Verb gruppiert.*

Du kannst mehrere Vorgänge auf einmal auswählen, **Verknüpfen** legt sie an.

| Beziehung | Liest sich als | Wann |
| --- | --- | --- |
| **wird blockiert von** / **blockiert** | „HIN-42 wird blockiert von HIN-40“ | Die Arbeit kann wirklich nicht starten, bevor die andere fertig ist |
| **dupliziert** / **wird dupliziert von** | „HIN-42 dupliziert HIN-11“ | Dasselbe Problem wurde zweimal gemeldet; eines behalten, das andere verknüpfen |
| **hängt zusammen mit** | Liest sich von beiden Seiten gleich | Lose verbunden — gut zu wissen, aber keine Abhängigkeit |
| **klont** / **wird geklont von** | Wird beim [Klonen](#einen-vorgang-klonen) automatisch gesetzt | Eine Kopie und ihr Original |
| **testet** / **wird getestet von** | „HIN-90 testet HIN-42“ | Eine Test- oder QA-Aufgabe zu einem Stück Arbeit |
| **aufgeteilt in** / **aufgeteilt aus** | „HIN-42 aufgeteilt in HIN-55“ | Ein Vorgang wurde zu groß und ist zu mehreren geworden |
| **hat erstellt** / **erstellt von** | Herkunft | Aus einem Stück Arbeit ist ein weiteres entstanden |

Verknüpfungen haben eine Richtung, und beide Enden bleiben im Gleichschritt: Legst du hier „blockiert“ an, zeigt der andere Vorgang sofort „wird blockiert von“ — live, ohne Neuladen.

!!! info "Nur *blockiert* wirkt auf die Planung"
    **blockiert** ist die eine Beziehung, die die [Timeline](/de/guide-timeline.html) als Verbindung zwischen zwei Balken zeichnet und beim kritischen Pfad mitzählt. Alle anderen sind Dokumentation für Menschen — wertvoll, aber sie verschieben nie ein Datum.

## Einen Vorgang beobachten

Öffne das Menü **…** und wähl **Beobachten**. Ab dann wirst du über Kommentare und Änderungen an diesem Vorgang benachrichtigt, bis du es wieder ausschaltest, und dasselbe Popover listet alle anderen Beobachter — du siehst also, wer sonst noch hinschaut.

Zwei Dinge sparen dir einen Klick:

- Bist du **zugewiesene Person** oder **erstellende Person**, wirst du ohnehin benachrichtigt — das Popover sagt das, statt dich etwas abonnieren zu lassen, das du längst bekommst.
- Alles, was du beobachtest, sammelt die Seite **Beobachtet** in der Seitenleiste.

## Einen Vorgang klonen

**… → Klonen …** kopiert einen Vorgang in dasselbe Projekt — praktisch für wiederkehrende Arbeit oder als Vorlage für eine Serie ähnlicher Tickets.

![Der Klon-Dialog](/assets/img/shot-issue-clone.png)
*Klonen: Die Zusammenfassung kommt mit dem Präfix „CLONE - “, und was mitkommt, sind drei Schalter — „Anhänge“, „Verknüpfungen“, „Sprint-Werte“ — alle aus, jeder mit der Zeile, die sagt, was das Einschalten tut.*

Anhänge, die mitkommen, werden als eigene gespeicherte Dateien kopiert; das spätere Entfernen der einen rührt die andere nicht an. Was du auch wählst: Eine **klont**-Verknüpfung zurück zum Original wird immer angelegt, und **du** wirst als Autor der Kopie eingetragen.

!!! note "Die Diskussion bleibt beim Original"
    Kommentare, Arbeitszeiten und Verlauf wandern nie in einen Klon. Genau das ist der Sinn: Ein Klon ist ein frischer Start mit derselben Form, keine Momentaufnahme einer Unterhaltung.

## Einen Vorgang in ein anderes Projekt verschieben

**… → In Projekt verschieben …** siedelt einen Vorgang um. Das ist ein zweistufiger Assistent, weil ein Umzug selten verlustfrei ist: erst das Zielprojekt, dann alles, was nicht einfach mitkommen kann.

![Schritt zwei des Verschiebe-Assistenten](/assets/img/shot-issue-move.png)
*Schritt zwei. Jeder beteiligte Status wird auf einen abgebildet, den das Zielprojekt hat — hier passt alles, es ist also nichts zu entscheiden — darunter die Folgen, die Hinata selbst ermittelt hat, und ganz unten die neuen Schlüssel: Aus HIN-4 wird MOB-9, und die drei Sub-Tasks ziehen mit.*

Hinata ordnet vorab jeden Status zu, den es zuordnen kann, und fragt nur nach dem Rest. Im neuen Projekt bekommt der Vorgang einen neuen Schlüssel, und der alte löst nicht mehr auf.

!!! warning "Archivierte Vorgänge zuerst wiederherstellen"
    Für archivierte Vorgänge ist der Eintrag deaktiviert. Erst wiederherstellen, dann verschieben.

## Archivieren und löschen

Das sind zwei verschiedene Dinge, und Hinata schubst dich zum umkehrbaren.

**Archivieren** ist ein weiches Löschen und steht jedem Projektmitglied offen. Der Vorgang verschwindet aus Listen, Boards, Sprints und der Suche, aber nichts wird zerstört — der Filter **Archiviert** findet ihn wieder, **Wiederherstellen** holt ihn zurück, genau wie er war. Archivierst du eine Story, Aufgabe, einen Fehler oder ein Feature, werden die Sub-Tasks mitarchiviert; beim Wiederherstellen kommen sie mit zurück.

**Löschen** ist endgültig und an Rollen gebunden: Plattform-Admins, Projektleitungen und die Admins eines Teams, dem das Projekt gehört. Gehörst du nicht dazu, bietet dir das Menü **Archivieren** und sonst nichts — nicht als Strafe, sondern weil es hinter dem anderen Button kein Zurück gibt. Darfst du löschen, bietet der Bestätigungsdialog beides an, Archivieren als ruhige Wahl und Löschen in Rot.

!!! warning "Löschen ist endgültig und nimmt anderes mit"
    Ein gelöschter Vorgang nimmt seine Kommentare, Arbeitszeiten, Verknüpfungen und seinen Verlauf mit. Beim Löschen einer **Story, Aufgabe, eines Fehlers oder Features verschwinden auch die Sub-Tasks**. Beim Löschen eines **Epics** verschwinden die Kinder *nicht* — sie leben als gewöhnliche Vorgänge der obersten Ebene weiter und verlieren nur ihre Epic-Verbindung. Im Zweifel: archivieren. Ein archivierter Vorgang kostet nichts und lässt sich immer zurückholen.

## Einen Vorgang exportieren oder drucken

Manchmal muss ein Vorgang die App verlassen — für einen Bericht, ein Audit, eine Kundin oder eine Sitzung, in der jemand auf Papier besteht. **… → Exportieren …** bietet:

- **Drucken** — schickt den Vorgang an den Druckdialog deines Systems.
- **Als PDF exportieren**
- **Als Excel-Datei exportieren**
- **Als Word-Datei exportieren**
- **Als XML-Datei exportieren**

Gerendert wird alles auf dem Server, das Layout — Überschriften, Tabellen, Codeblöcke, die Details — ist also identisch, egal von welchem Gerät du gefragt hast. Drucken ist kein eigenes Format: Gedruckt wird genau das PDF, das der PDF-Eintrag herunterlädt, ein gedruckter und ein gespeicherter Vorgang können sich also nie widersprechen.

Ein Export ist das ganze Ticket, nicht nur die Beschreibung: die Felder, die formatierte Beschreibung, die Kommentare, die verknüpften Vorgänge, die Liste der angehängten Dateien und der Änderungsverlauf. PDF und Word ergeben ein Dokument zum Lesen; Excel ergibt zwei Blätter — eines mit Feldern, eines mit Kommentaren — für alle, die mit dem Inhalt arbeiten statt ihn zu lesen; XML ist die maschinenlesbare Fassung.

Wo die Datei landet, hängt von der Plattform ab: iOS, Android, macOS und Windows öffnen das System-Teilen-Menü, du wählst also Dateien, Downloads, AirDrop oder Mail; Linux speichert direkt in deinen Downloads-Ordner und nennt dir den Dateinamen; der Web-Build übergibt sie deinem Browser.

!!! tip "Lieber eine ganze Liste exportieren"
    Der Button **Exportieren** auf der Issues-Seite exportiert die Liste, die du gerade siehst — mit Filtern, Gruppierung und allem — als PDF, CSV oder JSON. Nimm den Export am Vorgang, wenn jemand den vollen Text eines Tickets braucht, und den Listenexport, wenn ein Überblick gefragt ist.

## Verwandte Seiten

- **[Boards & Sprints](/de/guide-boards.html)** — Vorgänge durch den Workflow schieben, Sprints planen, im Backlog arbeiten.
- **[Kommentare & Anhänge](/de/guide-collaboration.html)** — Unterhaltung, Dateien und Sprachnachrichten an einem Vorgang.
- **[Timeline & Abhängigkeiten](/de/guide-timeline.html)** — was Startdatum, Fälligkeitsdatum und *blockiert*-Verknüpfungen zeichnen.
- **[Zeit erfassen](/de/guide-time.html)** — Arbeit an einem Vorgang buchen und den Stundenzettel füllen.
- **[Auf dem Laufenden bleiben](/de/guide-notifications.html)** — wer was erfährt und wie du es leiser stellst.
- **[Dinge finden](/de/guide-search.html)** — die ⌘K-Palette, Filter und Suche.
