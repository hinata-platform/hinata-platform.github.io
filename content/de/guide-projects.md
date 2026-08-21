---
title: Projekte & Teams
description: Was ein Projekt ist, was das Kürzel HIN-42 an jedem Vorgang bedeutet, wie Teams entscheiden, welche Projekte du siehst, und was eine Projektleitung ändern darf.
---

# Projekte & Teams

Jeder Vorgang in Hinata gehört zu einem **Projekt**, und jedes Projekt, das du öffnen kannst, wurde dir durch ein **Team** geöffnet — oder dadurch, dass dich jemand direkt hinzugefügt hat. Diese beiden Ideen erklären das meiste von dem, was du siehst. Und das meiste von dem, was du nicht siehst.

Diese Seite behandelt beides, in der Reihenfolge, in der du ihnen begegnest: was ein Projekt ist, wie du deine Projekte durchsiehst, warum deine Liste kürzer sein kann als die einer Kollegin, und was eine Projektleitung ändern kann, ohne je in die Nähe eines Adminbereichs zu kommen.

## Was ein Projekt ist

Ein Projekt ist ein Behälter für ein Arbeitsgebiet — ein Produkt, ein Dienst, eine interne Initiative. Es hält seine eigenen Vorgänge, sein eigenes Board, seine eigenen Spalten und seine eigenen Stichwörter. Zwei Projekte können völlig unterschiedlich arbeiten und kommen sich nie in die Quere.

Praktisch gibt dir ein Projekt fünf Dinge:

- **Ein Projektkürzel**, das Präfix an jedem Vorgang darin.
- **Workflow-Status** — die Spalten, die ein Vorgang durchläuft.
- **Stichwörter** — wiederverwendbare farbige Tags für seine Vorgänge.
- **Mitglieder** und eine oder mehrere **Leitungen**.
- **Ein Board**, ein Backlog, eine Zeitachse und Berichte, alle auf das Projekt begrenzt.

### Das Projektkürzel

Beim Anlegen bekommt ein Projekt ein kurzes Kürzel in Großbuchstaben: `HIN`, `MOB`, `INF`. Jeder Vorgang darin wird dann daraus durchnummeriert — `HIN-1`, `HIN-2`, `HIN-3` — und diese Kombination ist für den Rest seines Lebens der Name des Vorgangs.

Das ist das Nützlichste, was du über Hinata lernen kannst, denn das Kürzel reist überall mit:

- Tipp `HIN-42` in die Suchpalette und du landest direkt bei diesem Vorgang.
- Schreib `HIN-42` in eine Chatnachricht und alle wissen, was du meinst.
- Setz `HIN-42` in einen Branch-Namen oder eine Commit-Nachricht — ist dein Projekt an ein Repository angebunden, verknüpft sich die Arbeit von selbst zurück mit dem Vorgang.

Die Nummern werden der Reihe nach vergeben und **nie wiederverwendet**. Archivier `HIN-42`, lösch ihn, verschieb ihn — die `42` kommt für nichts anderes zurück. Genau deshalb kannst du ein Kürzel gefahrlos in ein Dokument schreiben, das den Vorgang überlebt.

!!! tip "Sprich es einmal laut aus, bevor du dich festlegst"
    Kürzel landen in Commit-Nachrichten, Branch-Namen und der Hälfte deiner Gespräche. `HIN` tippt sich hundertmal am Tag angenehm; `PLATTFORM2026` nicht. Kurz gewinnt.

!!! note "Ein Kürzel kann sich später ändern und nimmt seine Vorgänge mit"
    Wird ein Projekt umbenannt und sein Kürzel geändert, bekommt jeder Vorgang das neue Präfix und behält seine Nummer: Aus `HIN-42` wird `PLAT-42`. Alte Links lösen dann nicht mehr auf — es lohnt sich also, das früh zu tun statt spät. Aber es ist keine Falle, in die du dauerhaft tappen kannst.

### Workflow-Status, Stichwörter und Mitglieder

Der Rest dessen, was ein Projekt trägt, wird weiter unten beschrieben. In Kürze:

**Workflow-Status** sind die Spalten des Boards und die möglichen Werte für den Status eines Vorgangs. Ein neues Projekt startet mit einem sinnvollen Standard — *Backlog → Open → In Progress → In Review → Done*, wobei *Done* als erledigt markiert ist — und eine Leitung kann das alles später ändern.

**Stichwörter** sind wiederverwendbare Tags mit einer Farbe, einmal pro Projekt definiert und danach an jedem Vorgang darin verfügbar. `design`, `performance`, `security`, `good-first-issue`. Weil sie auf Projektebene definiert und nicht frei getippt werden, bleiben sie aufgeräumt und durchsuchbar.

**Mitglieder** sind die Personen, die im Projekt arbeiten. Sie tauchen in Zuweisungs-Auswahlen, im Personenfilter des Boards und in Berichten auf. Eine oder mehrere von ihnen sind als **Leitung** markiert — die Personen, die die Konfiguration des Projekts ändern dürfen.

## Deine Projekte durchsehen

**Projekte** in der Navigationsleiste listet alles, was du sehen kannst.

![Die Projektübersicht](/assets/img/shot-projects.png)
*Die Seite „Projekte“: eine Karte pro Projekt mit Kürzel-Symbol, Name, Kürzel und Leitung, den Zahlen für Mitglieder und Workflow-Status, einem Fortschrittsbalken, Mitglieder-Avataren und der Anzahl der Stichwörter. Der Umschalter Aktiv / Archiviert sitzt über den Karten, „Neues Projekt“ oben rechts.*

Ein Klick irgendwo auf eine Karte öffnet die **Vorgangsliste** dieses Projekts — das ist der Hauptweg hinein. Die Schaltfläche **Einstellungen** auf der Karte ist ein eigenes Ziel und erscheint nur, wenn du sie benutzen darfst (dazu unten mehr).

### Was dir eine Karte auf einen Blick sagt

- **Das quadratische Symbol** ist das Bild des Projekts — oder sein Kürzel in einer dicktengleichen Schrift, wenn es keines hat.
- **Die Zeile unter dem Namen** ist Kürzel und Projektleitung: `HIN · Leitung admin`.
- **Mitglieder** und **Status** sind Zahlen: wie viele Personen hier arbeiten und wie viele Spalten der Workflow hat.
- **Der Balken** ist der Fortschritt: wie viel der Arbeit erledigt ist.
- **Die Gesichter** sind die Mitglieder, mit einem `+2`, wenn mehr da sind als hineinpassen.
- **Die Tag-Zahl** ist die Anzahl der Stichwörter, die das Projekt definiert.

### Aktiv und archiviert

Der Umschalter über den Karten wechselt zwischen **Aktiv** und **Archiviert**, und die Zeile unter dem Seitentitel hält den Stand fest: *„3 aktiv · 0 archiviert“*.

Archivieren ist die Art, wie ein Projekt endet, ohne zerstört zu werden. Ein archiviertes Projekt verschwindet aus der aktiven Liste und wird schreibgeschützt — seine Vorgänge, Kommentare, Anhänge und die ganze Historie bleiben genau da, wo sie waren, und du kannst sie weiterhin finden und lesen. Gelöscht wird nichts.

Damit ist Archivieren der richtige Schritt für ein fertiges Projekt, ein abgesagtes oder eines, das einfach ruht. Und es ist umkehrbar: Schalt zurück, und das Projekt ist wieder da.

### Ein Projekt anlegen

**Neues Projekt**, oben rechts, ist die ganze Zeremonie.

![Der Dialog „Neues Projekt“](/assets/img/shot-project-new.png)
*Der Dialog „Neues Projekt“. Das Kürzel schreibt sich beim Tippen aus dem Namen — aus „Billing & Plans“ wurde BP, im Feld „Projektkürzel“ und im Symbol daneben — und Beschreibung, Projektleitung und Farbe sind der Rest. Die Zeile unten nennt den Workflow, mit dem das Projekt startet.*

Den Vorschlag darfst du überschreiben. Das Kürzel muss in Großbuchstaben stehen, mit einem Buchstaben beginnen, zwischen zwei und zehn Zeichen aus Buchstaben und Ziffern lang und auf dem ganzen Server eindeutig sein — hat es jemand schon, bekommst du vor dem Speichern *„Dieser Schlüssel ist bereits vergeben.“* zu lesen.

Sonst ist hier nichts endgültig. Workflow und Stichwörter passt du danach in den Projekteinstellungen an; es besteht kein Druck, alles in einem Durchgang richtig zu machen.

## Teams — und warum du nicht alles siehst

Jetzt kommt der Teil, der Leute überrascht. Deshalb hier ganz direkt:

**Du siehst nicht automatisch jedes Projekt auf dem Server.** Deine Kollegin öffnet Projekte und findet sechs Karten, wo du zwei findest. Nichts ist kaputt, und niemand versteckt etwas vor dir persönlich — Hinata behandelt Projektzugriff schlicht als etwas, das gewährt werden muss, statt als etwas, das alle standardmäßig bekommen.

### Die Regel in drei Zeilen

Du siehst ein Projekt, wenn **einer** dieser Punkte zutrifft:

1. Du bist **direkt Mitglied dieses Projekts**.
2. Ein **Team, in dem du bist, gewährt** dir dieses Projekt.
3. Du bist **Plattform-Administratorin oder -Administrator** und siehst alles.

Das ist die ganze Regel. Und sie wird bei jeder einzelnen Anfrage auf dem Server durchgesetzt, nicht dadurch, dass die App Schaltflächen versteckt — ein Projekt, das du nicht sehen darfst, taucht deshalb auch nicht in deiner Vorgangsliste, deinen Suchergebnissen, deinen Berichten, deinen Board-Filtern oder deinen Benachrichtigungen auf. Es gibt keinen „Für mich freigeben“-Schritt, den jemand vergessen könnte: Gewährt zu sein *ist* der Zugriff.

### Was ein Team ist

Ein Team ist eine Gruppe von Personen plus eine Menge von Projekten. Setz jemanden ins Team, gewähr dem Team ein Projekt — und diese Person kann darin arbeiten. Nimm das Projekt vom Team, und alle, die es nur über dieses Team erreicht haben, verlieren es leise wieder.

![Der Überblick eines Teams](/assets/img/shot-team.png)
*Eine Teamseite: oben Name und Kürzel des Teams mit „Mitglieder hinzufügen“ und „Projekt hinzufügen“, darunter die Reiter Überblick / Mitglieder / Projekte / Einstellungen, die Kennzahlen für Mitglieder, Team-Admins und Projekte, die Liste der Projekte, die das Team gewährt, und ein Feed der letzten Aktivität — hier die neu geschriebene Beschreibung sowie Amara Okafor, hinzugefügt und anschließend befördert.*

Der Eintrag **Teams** in der Leiste listet die Teams, in denen du bist. Jede Karte zeigt das Kürzel, die Mitgliederzahl, ein paar Gesichter, wie viele Projekte das Team gewährt und — bei den Teams, in denen du tatsächlich bist — ein Abzeichen mit deiner eigenen Rolle darin: **Admin** oder **Mitglied**.

Öffne eines, und du bekommst vier Reiter:

- **Überblick** — die Kennzahlen, die Projekte, die dieses Team gewährt, und was zuletzt darin passiert ist.
- **Mitglieder** — wer im Team ist, mit welcher Rolle, und was jede Person erreichen kann.
- **Projekte** — die Projekte, die das Team gewährt, mit der Möglichkeit, ein bestehendes anzuhängen oder ein neues fürs Team anzulegen.
- **Einstellungen** — Name, Kürzel, Farbe und Symbol des Teams, eine Erklärung in Klartext, was jede Rolle darf, und die Gefahrenzone.

### Zwei Rollen

Innerhalb eines Teams gibt es genau zwei Rollen, und die App schreibt aus, was jede bedeutet:

| Rolle | Was sie darf |
| --- | --- |
| **Team-Admin** | Volle Kontrolle über dieses Team — Mitglieder, Projekte, Einstellungen. Dieselben Rechte wie eine Plattform-Administration, aber auf dieses eine Team begrenzt. Sieht immer jedes Projekt, das dem Team gehört. |
| **Mitglied** | Arbeitet an den gewährten Projekten. Kann Mitgliedschaft und Einstellungen des Teams nicht ändern. |

### Drei Stufen von Projektzugriff

Wenn jemand zu einem Team hinzugefügt wird, wird der Projektzugriff zusammen mit der Rolle festgelegt.

![Schritt zwei von „Mitglieder hinzufügen“](/assets/img/shot-team-add-members.png)
*Schritt 2, „Zugriff“: die Rolle — „Mitglied“ oder „Team-Admin“ — und darunter die drei Stufen des Projektzugriffs. „Zurück“ führt zum Schritt „Personen“; „1 hinzufügen“ legt Person, Rolle und Zugriff in einem Rutsch fest.*

**Alle Projekte** bleibt richtig, während das Team wächst: Später angehängte Projekte sind dabei, ohne dass jemand die Person noch einmal anfassen muss. **Bestimmte Projekte** ist genau das, was du ankreuzt, und nichts anderes aus dem Bestand des Teams. **Noch keine Projekte** setzt jemanden ins Team, ohne ihm etwas zu öffnen — nützlich, wenn du Leute jetzt aufnehmen und den Zugriff später klären willst.

**Team-Admins sind die Ausnahme**: Sie sehen immer alles, was ihrem Team gehört, egal was die Zugriffseinstellung sagt. Genau das macht sie zu Admins.

### Die Projekte, die einem Team gehören

Der Reiter **Projekte** eines Teams ist der Ort, an dem das Gewähren tatsächlich passiert.

![Ein Projekt zu einem Team hinzufügen](/assets/img/shot-team-add-project.png)
*„Projekt hinzufügen“, auf dem Reiter „Bestehendes anhängen“: jedes Projekt, das das Team noch nicht hat, je eine Zeile mit Kürzel, Name und Leitung, dazu ein Kästchen. „Mobile App“ ist hier angehakt, deshalb zählt der Bestätigen-Button mit — __1 anhängen__. „Neu erstellen“ daneben legt ein frisches Projekt an, das dem Team vom ersten Tag an gehört.*

Ein Projekt aus einem Team zu entfernen ist das Spiegelbild, und die App ist vor dem Bestätigen ehrlich über die Folge: Mitglieder verlieren den Zugriff, den dieses Team gewährt hat. Erreichen sie das Projekt noch auf anderem Weg — als direktes Mitglied oder über ein zweites Team — behalten sie es. Hinata prüft jeden Weg, bevor es etwas wegnimmt.

### „Ich bin sicher, dass es dieses Projekt gibt, aber ich finde es nicht“

Das ist die häufigste Verwirrung in Hinata, und die Antwort ist kurz: Jemand muss dir Zugriff gewähren. Entweder

- lass dich **zum Projekt als Mitglied hinzufügen**, oder
- lass dich **in ein Team aufnehmen**, das es gewährt, oder — wenn du in diesem Team schon bist —
- bitte einen Team-Admin, deinen Projektzugriff von *Bestimmte Projekte* so zu erweitern, dass es dabei ist.

Jeder Team-Admin des betreffenden Teams, jede Leitung des Projekts und jede Plattform-Administration kann das tun, und die Änderung greift sofort. Du musst dich nicht ab- und wieder anmelden; das Projekt erscheint einfach.

!!! warning "Zugriff zu entziehen entzieht ihn überall, auf einmal"
    Jemanden aus einem Team zu nehmen oder ein Projekt von einem Team zu lösen, entzieht alles, was diese Gewährung getragen hat — das Projekt, seine Boards, seine Vorgänge und die Benachrichtigungen darüber. Die Personen beobachten dann auch keine Vorgänge mehr, die sie nicht mehr erreichen. Die Arbeit selbst bleibt unangetastet; nur der Zugriff verschwindet.

!!! note "Ein Team zu löschen löscht nie seine Projekte"
    Die Bestätigung sagt das ausdrücklich: Mitglieder verlieren den Zugriff, den das Team gewährt hat, und Projekte, Boards und Vorgänge bleiben im Workspace. Ein Team ist eine Berechtigungsstruktur, kein Behälter.

## Ein Beispiel, bei dem es klick macht

Abstrakte Regeln sind schwer zu behalten. Hier also eine erfundene Organisation, so aufgebaut, wie es die meisten Teams am Ende tun.

Nimm an, es gibt drei Projekte — **Hinata Platform** (`HIN`), **Mobile App** (`MOB`) und **Infrastructure** (`INF`) — und zwei Teams:

- **Core Platform** gewährt `HIN` und `INF`.
- **Design & Mobile** gewährt `MOB`.

Und jetzt vier Personen:

- **Nora** ist Mitglied von Core Platform mit Zugriff auf *Alle Projekte*. Sie öffnet Projekte und sieht zwei Karten: `HIN` und `INF`.
- **Sam** ist Mitglied von Design & Mobile und sieht eine Karte: `MOB`. `HIN` taucht dort nirgends auf — nicht in der Suche, nicht in Berichten, nicht in einem Board-Filter.
- **Ida** ist Team-Admin von Core Platform. Sie sieht `HIN` und `INF` unabhängig von jeder persönlichen Zugriffseinstellung, weil Team-Admins immer sehen, was ihrem Team gehört. Sie ist außerdem Leitung von `INF` — deshalb ist `INF` die einzige Karte, die ihr eine Schaltfläche „Einstellungen“ zeigt.
- **Ruben** ist Mitglied von Design & Mobile *und* wurde direkt zu `HIN` als Projektmitglied hinzugefügt, weil er darin einen Screen gestaltet. Er sieht `MOB` über sein Team und `HIN` über die direkte Mitgliedschaft — zwei verschiedene Wege, dasselbe Ergebnis.

Nach der ersten Einrichtung brauchte nichts davon eine Administration. Team-Admins gewähren Projekte, Projektleitungen konfigurieren sie, und alle anderen finden schlicht die richtige Arbeit vor.

!!! tip "Team-Gewährung oder direkte Mitgliedschaft?"
    Nimm eine **Team-Gewährung**, wenn eine ganze Gruppe ein Projekt braucht — sie bleibt richtig, während Leute in die Gruppe kommen und gehen. Nimm die **direkte Mitgliedschaft** für die eine Designerin, den einen Freelancer, die eine Person aus einer anderen Abteilung. Beides zu mischen ist normal, und der Zugriff ist die Vereinigung von allem, was zutrifft.

## Was eine Projektleitung ändern kann

Jedes Projekt hat eine Seite **Einstellungen**, und die gehört den Menschen, die dieses Projekt führen: seinen **Leitungen** und den Plattform-Administrationen. Bist du gewöhnliches Mitglied, kannst du den ganzen Tag im Projekt arbeiten und diese Seite nie sehen — deshalb fehlt die Schaltfläche „Einstellungen“ auf der Karte bei dir.

Nichts davon braucht den Adminbereich. Eine Leitung konfiguriert ihr eigenes Projekt.

![Projekteinstellungen](/assets/img/shot-project-settings.png)
*Die Projekteinstellungen des Projekts „Hinata Platform“: links die Karte Allgemein mit Bild, Name, Kürzel, Beschreibung und Akzentfarbe, darunter Leitung & Mitglieder; rechts stapeln sich Stichwörter, Archiv und die Gefahrenzone.*

### Allgemein

Das **Bild** des Projekts (oder sein Kürzel-Symbol, wenn es keines hat), sein **Name**, sein **Kürzel**, eine **Beschreibung** und eine **Akzentfarbe**, die das Projekt quer durch die App einfärbt.

Unter dem Kürzelfeld zeigt dir die Seite in Echtzeit die Folge — *„Aufgaben lauten wie HIN-42“* — eine Kleinigkeit, die schon viel Reue erspart hat.

### Leitung & Mitglieder

Die Liste der Personen im Projekt. **Markiere ein Mitglied mit einem Stern, um es zur Projektleitung zu machen**; ein Projekt braucht immer mindestens eine. Die Seite sagt das, und sie weigert sich zu speichern, wenn du keine übrig ließest.

**Mitglieder hinzufügen** öffnet eine Suche über alle Personen auf dem Server. Neu hinzugefügte Personen werden benachrichtigt, dass sie das Projekt nun haben.

### Stichwörter

Wiederverwendbare Tags für die Vorgänge dieses Projekts: Namen eintippen, Farbe wählen, **Hinzufügen** drücken. Du kannst sie später umbenennen, umfärben oder entfernen — und ein Umbenennen zieht durch jeden Vorgang, der das Stichwort schon trägt. Nichts bleibt auf den alten Namen zeigen.

### Workflow-Status

Die Spalten, die ein Vorgang durchläuft, in ihrer Reihenfolge. Füg einen hinzu, benenn einen um, zieh sie in eine andere Reihenfolge, entfern einen, den ihr nicht nutzt.

Jeder Status hat einen Schalter **Erledigt**, der ihn als Status markiert, der als *fertig* zählt. Dieser Schalter ist es, der Burndown-Diagramme, Fortschrittsringe und durchgestrichene Teilaufgaben die Wahrheit sagen lässt — es lohnt sich also, ihn richtig zu setzen. Ein Projekt braucht **mindestens zwei Status und mindestens einen erledigten**; der Editor lässt dich unter keines von beiden.

![Einen Workflow-Status entfernen, in dem noch Vorgänge liegen](/assets/img/shot-workflow-state-migrate.png)
*Wer einen Status löscht, in dem noch Vorgänge liegen, bekommt „Status hat noch Aufgaben“: Der Dialog zählt sie, nennt den Status, in dem sie stehen, und bietet die übrigen Status als Ziel an. „Migrieren & entfernen“ bleibt inaktiv, bis eines gewählt ist.*

!!! warning "Nichts bleibt im Regen stehen"
    Ein Status lässt sich nicht entfernen, solange Vorgänge darin liegen. Du kannst diese Vorgänge auch vorher selbst verschieben, wenn du es bewusster machen möchtest.

### Speichern

Die Projekteinstellungen sind ein Entwurfs-Editor, kein Live-Editor. Änderst du etwas, erscheint unten eine Leiste mit **Ungespeicherte Änderungen** sowie **Verwerfen** und **Änderungen speichern**. Nichts, was du angefasst hast, erreicht das Projekt — oder den Bildschirm anderer Leute — bevor du speicherst.

Ist etwas ungültig, sagt die Leiste *„Pflichtfelder ausfüllen, um zu speichern“*, statt dich ein kaputtes Projekt speichern zu lassen.

### Archivieren

Die Karte **Archiv** hat einen einzigen Schalter: *Projekt ist aktiv*. Schalt ihn aus, und das Projekt wandert in den Reiter „Archiviert“, wird schreibgeschützt und bleibt dort — vollständig und lesbar — bis jemand ihn wieder einschaltet.

Das ist fast immer das, was du willst, wenn ein Projekt endet. Es kostet nichts und verliert nichts.

### Löschen

Die **Gefahrenzone** ganz unten hat eine Schaltfläche: **Projekt löschen**. Das ist die eine wirklich unumkehrbare Aktion im Leben eines Projekts.

![Die Bestätigung zum Löschen eines Projekts](/assets/img/shot-project-delete.png)
*Die Bestätigung listet den Schaden mit den echten Zahlen des Projekts auf, das du löschst — Boards und Sprints, die Teams, von denen es gelöst wird, die Wiki-Artikel — und fragt dann, was mit den Vorgängen passieren soll: löschen oder in ein anderes Projekt verschieben? „Löschen“ bleibt inaktiv, bis der Projektname eingetippt ist.*

Ein Board, das mit anderen Projekten geteilt ist, überlebt das Löschen; es verliert nur dieses eine.

!!! warning "Archivieren, außer es war ein Versehen"
    Löschen ist für ein Projekt, das es nie hätte geben sollen. Für eines, das einfach zu Ende ist: **archivier es**. Das kostet nichts, verliert nichts und lässt sich wieder einschalten.

## Wer was darf

Eine Übersicht zum Überfliegen, wenn du unsicher bist, ob du jemanden fragen oder es einfach tun sollst:

| Aktion | Wer |
| --- | --- |
| In einem Projekt arbeiten — Vorgänge anlegen, kommentieren, Zeit buchen, Karten bewegen | Jedes Mitglied des Projekts |
| Ein Projekt überhaupt sehen | Direkte Mitglieder, Personen, denen ein Team es gewährt, Plattform-Administrationen |
| Name, Kürzel, Stichwörter, Workflow, Mitglieder eines Projekts ändern | Projektleitungen und Plattform-Administrationen |
| Ein Projekt archivieren oder löschen | Projektleitungen und Plattform-Administrationen |
| Teammitglieder hinzufügen oder entfernen, Rolle und Zugriff setzen | Team-Admins und Plattform-Administrationen |
| Projekte eines Teams anhängen oder lösen | Team-Admins und Plattform-Administrationen |
| Name, Kürzel, Farbe oder Symbol eines Teams ändern | Team-Admins und Plattform-Administrationen |
| Alles Übrige — Nutzerkonten, Anmeldung, E-Mail, Integrationen | Plattform-Administrationen, im Adminbereich |

Brauchst du etwas aus der letzten Zeile, suchst du die Person, die den Server betreibt. Die Seite [Adminbereich](/de/admin-area.html) beschreibt, was dort liegt.

## Wie es weitergeht

- **[Mit Vorgängen arbeiten](/de/guide-issues.html)** — jetzt, wo du weißt, wo Vorgänge leben, lern, wie man gute schreibt.
- **[Boards & Sprints](/de/guide-boards.html)** — die Workflow-Status von dieser Seite, als Spalten, über die du Karten ziehst.
- **[Dinge finden](/de/guide-search.html)** — über alle Projekte suchen, die du sehen kannst, und auf eines eingrenzen.
- **[Berichte & Dashboard](/de/guide-reports.html)** — wo aus erledigten Status und Fortschrittsbalken Diagramme werden.
- **[Erste Schritte](/de/guide-start.html)** — zurück zur Eingangstür, falls du hier zuerst gelandet bist.
