---
title: Projekte & Teams
description: Was ein Projekt ist, was das Kürzel HIN-42 bedeutet und wie Teams bestimmen, welche Projekte du siehst.
---

# Projekte & Teams

Jeder Vorgang gehört zu einem **Projekt**. Welche Projekte du siehst, hängt davon ab, ob dich ein **Team** dafür freischaltet oder dich jemand direkt hinzugefügt hat.

## Was ein Projekt ist

Ein Projekt bündelt ein Arbeitsgebiet: ein Produkt, einen Dienst oder eine interne Initiative. Es hat eigene Vorgänge, ein eigenes Board, eigene Spalten und eigene Stichwörter. Projekte kommen sich nicht in die Quere.

Jedes Projekt hat:

- **Ein Projektkürzel**, das Präfix an jedem Vorgang darin.
- **Workflow-Status**, also die Spalten, die ein Vorgang durchläuft.
- **Stichwörter**, wiederverwendbare farbige Tags.
- **Mitglieder** und eine oder mehrere **Leitungen**.
- **Ein Board**, ein Backlog, eine Zeitachse und Berichte, alle auf das Projekt begrenzt.

### Das Projektkürzel

Beim Anlegen bekommt ein Projekt ein kurzes Kürzel in Großbuchstaben, etwa `HIN`, `MOB` oder `INF`. Die Vorgänge darin heißen dann `HIN-1`, `HIN-2`, `HIN-3` und so weiter. Diesen Namen behält ein Vorgang dauerhaft.

So nutzt du das Kürzel:

- `HIN-42` in der Suchpalette springt direkt zum Vorgang.
- `HIN-42` im Chat versteht jede Person im Team.
- `HIN-42` im Branchnamen oder in der Nachricht eines Commits verknüpft die Arbeit mit dem Vorgang, wenn das Projekt an ein Repository angebunden ist.

Nummern werden der Reihe nach vergeben und **nie wiederverwendet**. Auch nach Archivieren, Löschen oder Verschieben kommt die `42` nicht zurück. Du kannst ein Kürzel also gefahrlos in Dokumente schreiben.

!!! tip "Sprich es einmal laut aus, bevor du dich festlegst"
    Das Kürzel tippst du ständig, in Commits, Branches und Gesprächen. `HIN` geht leicht, `PLATTFORM2026` nicht. Kurz ist besser.

!!! note "Ein Kürzel kann sich später ändern und nimmt seine Vorgänge mit"
    Ändert sich das Kürzel, bekommen alle Vorgänge das neue Präfix und behalten ihre Nummer: Aus `HIN-42` wird `PLAT-42`. Alte Links funktionieren dann nicht mehr. Ändere es deshalb lieber früh.

### Workflow-Status, Stichwörter und Mitglieder

- **Workflow-Status** sind die Spalten des Boards und die möglichen Werte für den Status. Neue Projekte starten mit *Backlog → Open → In Progress → In Review → Done*, wobei *Done* als erledigt markiert ist. Eine Leitung kann alles später ändern.
- **Stichwörter** sind farbige Tags, einmal pro Projekt definiert und an jedem Vorgang darin nutzbar, etwa `design`, `performance`, `security`, `good-first-issue`. Weil niemand sie frei tippt, bleiben sie einheitlich und durchsuchbar.
- **Mitglieder** arbeiten im Projekt. Sie erscheinen bei der Zuweisung, im Personenfilter des Boards und in Berichten. Mitglieder mit der Markierung **Leitung** dürfen die Konfiguration des Projekts ändern.

## Deine Projekte durchsehen

**Projekte** in der Navigationsleiste zeigt alle Projekte, die du sehen darfst.

![Die Projektübersicht](/assets/img/shot-projects.png)
*Die Seite „Projekte“ mit einer Karte pro Projekt.*

Über den Karten sitzt der Umschalter Aktiv / Archiviert, oben rechts „Neues Projekt“.

Ein Klick auf eine Karte öffnet die **Vorgangsliste** des Projekts. Die Schaltfläche **Einstellungen** auf der Karte siehst du nur, wenn du sie nutzen darfst.

### Was dir eine Karte auf einen Blick sagt

- **Quadratisches Symbol:** das Projektbild oder, ohne Bild, das Kürzel in dicktengleicher Schrift.
- **Zeile unter dem Namen:** Kürzel und Projektleitung, etwa `HIN · Leitung admin`.
- **Mitglieder** und **Status:** wie viele Personen hier arbeiten und wie viele Spalten der Workflow hat.
- **Balken:** wie viel der Arbeit erledigt ist.
- **Gesichter:** die Mitglieder, mit `+2`, wenn nicht alle hineinpassen.
- **Tagzahl:** wie viele Stichwörter das Projekt definiert.

### Aktiv und archiviert

Der Umschalter wechselt zwischen **Aktiv** und **Archiviert**. Unter dem Seitentitel steht der Stand, etwa *„3 aktiv · 0 archiviert“*.

Archivierte Projekte sind schreibgeschützt und verschwinden aus der aktiven Liste. Vorgänge, Kommentare, Anhänge und Historie bleiben auffindbar und lesbar. Gelöscht wird nichts, zurückholen geht jederzeit. Das passt für fertige, abgesagte oder ruhende Projekte.

### Ein Projekt anlegen

Klick oben rechts auf **Neues Projekt**.

![Der Dialog „Neues Projekt“](/assets/img/shot-project-new.png)
*Das Kürzel entsteht beim Tippen aus dem Namen, hier BP aus „Billing & Plans“.*

Außerdem gibt es Beschreibung, Projektleitung und Farbe. Unten steht der Workflow, mit dem das Projekt startet.

Den Vorschlag für das Kürzel kannst du überschreiben. Das Kürzel muss:

- in Großbuchstaben stehen und mit einem Buchstaben beginnen,
- zwei bis zehn Zeichen aus Buchstaben und Ziffern lang sein,
- auf dem ganzen Server eindeutig sein. Sonst siehst du vor dem Speichern *„Dieser Schlüssel ist bereits vergeben.“*

Workflow und Stichwörter passt du später in den Projekteinstellungen an.

## Teams und warum du nicht alles siehst

**Du siehst nicht automatisch jedes Projekt auf dem Server.** Eine Kollegin sieht vielleicht sechs Projekte, du nur zwei. Das ist kein Fehler. Zugriff auf ein Projekt muss gewährt werden.

### Die Regel in drei Zeilen

Du siehst ein Projekt, wenn **einer** dieser Punkte zutrifft:

1. Du bist **direkt Mitglied dieses Projekts**.
2. Ein **Team, in dem du bist, gewährt** dir dieses Projekt.
3. Du bist **Administratorin oder Administrator der Plattform** und siehst alles.

Der Server prüft das bei jeder Anfrage. Ein Projekt ohne Zugriff taucht deshalb auch nicht in Vorgangsliste, Suche, Berichten, Boardfiltern oder Benachrichtigungen auf. Einen extra Freigabeschritt gibt es nicht: Die Gewährung ist der Zugriff.

### Was ein Team ist

Ein Team ist eine Gruppe von Personen plus eine Reihe von Projekten. Wer im Team ist, kann in den Projekten des Teams arbeiten. Nimmst du dem Team ein Projekt weg, verlieren alle den Zugriff, die es nur über dieses Team hatten.

![Der Überblick eines Teams](/assets/img/shot-team.png)
*Eine Teamseite mit Kennzahlen, Projekten und letzter Aktivität.*

**Teams** in der Leiste zeigt die Teams, in denen du bist. Jede Karte zeigt Kürzel, Mitgliederzahl, einige Gesichter und wie viele Projekte das Team gewährt. Bei Teams, in denen du selbst bist, steht deine Rolle: **Admin** oder **Mitglied**.

Oben auf der Teamseite stehen „Mitglieder hinzufügen“ und „Projekt hinzufügen“. Dazu kommen vier Reiter:

- **Überblick:** Kennzahlen zu Mitgliedern, Team-Admins und Projekten, die gewährten Projekte und die letzte Aktivität.
- **Mitglieder:** wer im Team ist, mit Rolle und erreichbaren Projekten.
- **Projekte:** die gewährten Projekte. Hier hängst du bestehende an oder legst neue fürs Team an.
- **Einstellungen:** Name, Kürzel, Farbe und Symbol des Teams, eine Erklärung der Rollen und die Gefahrenzone.

### Zwei Rollen

| Rolle | Was sie darf |
| --- | --- |
| **Team-Admin** | Volle Kontrolle über dieses Team: Mitglieder, Projekte, Einstellungen. Dieselben Rechte wie die Plattformadministration, aber auf dieses eine Team begrenzt. Sieht immer jedes Projekt, das dem Team gehört. |
| **Mitglied** | Arbeitet an den gewährten Projekten. Kann Mitgliedschaft und Einstellungen des Teams nicht ändern. |

### Drei Stufen von Projektzugriff

Wenn du jemanden ins Team holst, legst du Rolle und Projektzugriff zusammen fest.

![Schritt zwei von „Mitglieder hinzufügen“](/assets/img/shot-team-add-members.png)
*Schritt 2, „Zugriff“: Rolle und Projektzugriff auf einer Seite.*

„Zurück“ führt zum Schritt „Personen“. „1 hinzufügen“ speichert Person, Rolle und Zugriff auf einmal.

- **Alle Projekte:** schließt auch Projekte ein, die später ans Team gehängt werden.
- **Bestimmte Projekte:** nur die angekreuzten Projekte.
- **Noch keine Projekte:** Die Person ist im Team, sieht aber noch kein Projekt. Praktisch, wenn du den Zugriff später klären willst.

**Team-Admins sind die Ausnahme:** Sie sehen immer alle Projekte ihres Teams, egal was eingestellt ist.

### Die Projekte, die einem Team gehören

Im Reiter **Projekte** gewährst du dem Team Projekte.

![Ein Projekt zu einem Team hinzufügen](/assets/img/shot-team-add-project.png)
*„Bestehendes anhängen“ listet alle Projekte, die das Team noch nicht hat.*

- Jede Zeile zeigt Kürzel, Name und Leitung mit einem Kästchen. Der Button zählt mit, etwa **1 anhängen**.
- **Neu erstellen** legt ein Projekt an, das von Anfang an dem Team gehört.

Entfernst du ein Projekt aus dem Team, verlieren die Mitglieder den Zugriff über dieses Team. Die App sagt dir das vor dem Bestätigen. Wer das Projekt auch direkt oder über ein anderes Team erreicht, behält es. Hinata prüft jeden Weg.

### „Ich bin sicher, dass es dieses Projekt gibt, aber ich finde es nicht“

Dann fehlt dir der Zugriff. Du hast drei Möglichkeiten:

- Lass dich **zum Projekt als Mitglied hinzufügen**.
- Lass dich **in ein Team aufnehmen**, das es gewährt.
- Bist du schon im Team, bitte einen Team-Admin, deinen Zugriff unter *Bestimmte Projekte* zu erweitern.

Das können Team-Admins des Teams, Leitungen des Projekts und die Plattformadministration. Die Änderung wirkt sofort, ohne neue Anmeldung.

!!! warning "Zugriff zu entziehen entzieht ihn überall, auf einmal"
    Nimmst du jemanden aus einem Team oder löst ein Projekt vom Team, fällt alles weg, was diese Gewährung ermöglicht hat: Projekt, Boards, Vorgänge und Benachrichtigungen. Die Person beobachtet auch keine Vorgänge mehr, die sie nicht mehr erreicht. Die Arbeit selbst bleibt unangetastet.

!!! note "Ein Team zu löschen löscht nie seine Projekte"
    Mitglieder verlieren den Zugriff über das Team. Projekte, Boards und Vorgänge bleiben im Workspace. Das steht auch in der Bestätigung.

## Ein Beispiel, bei dem es klick macht

Drei Projekte: **Hinata Platform** (`HIN`), **Mobile App** (`MOB`) und **Infrastructure** (`INF`). Dazu zwei Teams:

- **Core Platform** gewährt `HIN` und `INF`.
- **Design & Mobile** gewährt `MOB`.

Vier Personen:

- **Nora** ist Mitglied von Core Platform mit *Alle Projekte*. Sie sieht `HIN` und `INF`.
- **Sam** ist Mitglied von Design & Mobile und sieht nur `MOB`. `HIN` erscheint nirgends, auch nicht in Suche, Berichten oder Boardfiltern.
- **Ida** ist Team-Admin von Core Platform. Sie sieht `HIN` und `INF` unabhängig von Zugriffseinstellungen. Sie leitet außerdem `INF`, deshalb zeigt ihr nur diese Karte „Einstellungen“.
- **Ruben** ist Mitglied von Design & Mobile *und* direktes Mitglied von `HIN`, weil er dort einen Screen gestaltet. Er sieht `MOB` über das Team und `HIN` über die direkte Mitgliedschaft.

Nach der Einrichtung braucht es dafür keine Administration mehr. Team-Admins gewähren Projekte, Leitungen konfigurieren sie.

!!! tip "Teamgewährung oder direkte Mitgliedschaft?"
    Eine **Teamgewährung** passt, wenn eine ganze Gruppe ein Projekt braucht. Sie bleibt richtig, wenn Leute kommen und gehen. **Direkte Mitgliedschaft** passt für Einzelne, etwa eine Designerin, einen Freelancer oder jemanden aus einer anderen Abteilung. Beides lässt sich mischen. Der Zugriff ergibt sich aus allem, was zutrifft.

## Was eine Projektleitung ändern kann

Die **Einstellungen** eines Projekts dürfen seine **Leitungen** und die Plattformadministration ändern. Normale Mitglieder sehen die Seite nicht, deshalb fehlt ihnen die Schaltfläche auf der Karte. Den Adminbereich braucht eine Leitung dafür nicht.

![Projekteinstellungen](/assets/img/shot-project-settings.png)
*Die Projekteinstellungen von „Hinata Platform“.*

Links stehen Allgemein sowie Leitung & Mitglieder, rechts Stichwörter, Archiv und die Gefahrenzone.

### Allgemein

**Bild** (oder Kürzelsymbol), **Name**, **Kürzel**, **Beschreibung** und eine **Akzentfarbe**, die das Projekt in der ganzen App einfärbt.

Unter dem Kürzelfeld siehst du live, wie Vorgänge heißen werden, etwa *„Aufgaben lauten wie HIN-42“*.

### Leitung & Mitglieder

- **Markiere ein Mitglied mit einem Stern, um es zur Projektleitung zu machen.**
- Ein Projekt braucht immer mindestens eine Leitung. Ohne Leitung lässt sich nicht speichern.
- **Mitglieder hinzufügen** durchsucht alle Personen auf dem Server. Neue Mitglieder werden benachrichtigt.

### Stichwörter

Namen eintippen, Farbe wählen, **Hinzufügen** drücken. Später kannst du Stichwörter umbenennen, umfärben oder entfernen. Eine Umbenennung gilt für alle Vorgänge, die das Stichwort schon tragen.

### Workflow-Status

Die Spalten eines Vorgangs in ihrer Reihenfolge. Du kannst Status hinzufügen, umbenennen, per Ziehen umsortieren und entfernen.

- Der Schalter **Erledigt** markiert einen Status als *fertig*. Burndown, Fortschrittsringe und durchgestrichene Teilaufgaben richten sich danach.
- Ein Projekt braucht **mindestens zwei Status und mindestens einen erledigten**. Weniger lässt der Editor nicht zu.

![Einen Workflow-Status entfernen, in dem noch Vorgänge liegen](/assets/img/shot-workflow-state-migrate.png)
*„Status hat noch Aufgaben“ zählt die Vorgänge und bietet die übrigen Status als Ziel an.*

„Migrieren & entfernen“ bleibt inaktiv, bis du ein Ziel gewählt hast.

!!! warning "Nichts bleibt im Regen stehen"
    Ein Status lässt sich nicht entfernen, solange Vorgänge darin liegen. Du kannst sie auch vorher selbst verschieben.

### Speichern

Die Einstellungen sind ein Entwurf. Sobald du etwas änderst, erscheint unten eine Leiste mit **Ungespeicherte Änderungen**, **Verwerfen** und **Änderungen speichern**. Erst nach dem Speichern erreicht die Änderung das Projekt und andere Personen.

Ist etwas ungültig, zeigt die Leiste *„Pflichtfelder ausfüllen, um zu speichern“*.

### Archivieren

Die Karte **Archiv** hat einen Schalter: *Projekt ist aktiv*. Schaltest du ihn aus, wandert das Projekt in den Reiter „Archiviert“ und wird schreibgeschützt. Es bleibt vollständig lesbar, bis jemand den Schalter wieder einschaltet.

Wenn ein Projekt endet, ist das fast immer der richtige Schritt.

### Löschen

Die **Gefahrenzone** ganz unten hat eine Schaltfläche: **Projekt löschen**. Das ist die einzige wirklich unumkehrbare Aktion.

![Die Bestätigung zum Löschen eines Projekts](/assets/img/shot-project-delete.png)
*Die Bestätigung zeigt, was verloren geht, und fragt, was mit den Vorgängen passiert.*

- Die Bestätigung nennt die echten Zahlen: Boards und Sprints, Teams, von denen das Projekt gelöst wird, und Wikiartikel.
- Die Vorgänge kannst du löschen oder in ein anderes Projekt verschieben.
- „Löschen“ bleibt inaktiv, bis du den Projektnamen eintippst.
- Ein Board, das mit anderen Projekten geteilt ist, bleibt bestehen und verliert nur dieses Projekt.

!!! warning "Archivieren, außer es war ein Versehen"
    Löschen ist für ein Projekt, das es nie hätte geben sollen. Ein beendetes Projekt **archivierst du**. Das lässt sich wieder einschalten.

## Wer was darf

| Aktion | Wer |
| --- | --- |
| In einem Projekt arbeiten: Vorgänge anlegen, kommentieren, Zeit buchen, Karten bewegen | Jedes Mitglied des Projekts |
| Ein Projekt überhaupt sehen | Direkte Mitglieder, Personen, denen ein Team es gewährt, Plattformadministration |
| Name, Kürzel, Stichwörter, Workflow, Mitglieder eines Projekts ändern | Projektleitungen und Plattformadministration |
| Ein Projekt archivieren oder löschen | Projektleitungen und Plattformadministration |
| Teammitglieder hinzufügen oder entfernen, Rolle und Zugriff setzen | Team-Admins und Plattformadministration |
| Projekte eines Teams anhängen oder lösen | Team-Admins und Plattformadministration |
| Name, Kürzel, Farbe oder Symbol eines Teams ändern | Team-Admins und Plattformadministration |
| Alles Übrige: Nutzerkonten, Anmeldung, E-Mail, Integrationen | Plattformadministration, im Adminbereich |

Für die letzte Zeile wendest du dich an die Person, die den Server betreibt. Was dort liegt, steht unter [Adminbereich](/de/admin-area.html).

## Wie es weitergeht

- **[Mit Vorgängen arbeiten](/de/guide-issues.html):** gute Vorgänge schreiben.
- **[Boards & Sprints](/de/guide-boards.html):** die Workflow-Status als Spalten, über die du Karten ziehst.
- **[Dinge finden](/de/guide-search.html):** über alle sichtbaren Projekte suchen und auf eines eingrenzen.
- **[Berichte & Dashboard](/de/guide-reports.html):** wo erledigte Status und Fortschritt zu Diagrammen werden.
- **[Erste Schritte](/de/guide-start.html):** zurück zum Einstieg.
