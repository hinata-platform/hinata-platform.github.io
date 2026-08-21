---
title: Erste Schritte
description: Deine erste Stunde mit Hinata — mit dem Server deiner Organisation verbinden, anmelden und dich im Workspace und seiner Navigation zurechtfinden.
---

# Erste Schritte

In Hinata lebt die Arbeit deines Teams. Jede Aufgabe, jeder Fehler, jede Frage und jede Idee wird zu einem **Vorgang** (in der App heißt er *Issue*); Vorgänge liegen in **Projekten**; und Projekte wandern über Boards, Zeitachsen und Berichte, bis die Arbeit erledigt ist.

Jemand in deiner Organisation betreibt den Hinata-Server, und du hast ein Konto und eine App bekommen. Diese Seite bringt dich von der frisch installierten App zu einem Workspace, in dem du dich auskennst — und das meiste davon machst du nur ein einziges Mal.

## Die Begriffe, die du brauchst

Hinata borgt sich sein Vokabular vom agilen Projektmanagement. Falls dir etwas davon neu ist: Das hier ist die ganze Liste, und du darfst jederzeit zurückkommen.

| Begriff | Was er hier bedeutet |
| --- | --- |
| **Issue / Vorgang** | Ein Stück Arbeit: eine Aufgabe, ein Bug, ein Feature, eine Frage. Alles, was du tust, ist ein Vorgang. |
| **Projekt** | Der Behälter, in dem Vorgänge leben — ein Produkt, ein Dienst, eine Initiative. |
| **Projektkürzel** | Die kurze ID, die jeder Vorgang von seinem Projekt bekommt, etwa `HIN-42`. Zum Aussprechen, zum Einfügen in den Chat. |
| **Team** | Eine Gruppe von Personen — und die Projekte, die diese Gruppe öffnet. |
| **Board** | Die Spaltenansicht der Projektarbeit. Hier ziehst du Karten hinüber. |
| **Workflow-Status** | Die Spalten selbst: *Backlog*, *In Progress*, *Done* — was immer dein Projekt nutzt. |
| **Sprint** | Ein fester Zeitraum, meist zwei Wochen, mit einer ausgewählten Menge an Vorgängen. |
| **Backlog** | Alles, was noch in keinem Sprint steckt. |
| **Stichwort (Label)** | Ein farbiges Etikett für einen Vorgang, etwa `design` oder `security`. |
| **Epic** | Ein großes Arbeitspaket, zu dem andere Vorgänge gehören. |

Nichts davon musst du heute verstanden haben. Du nimmst es beim Benutzen auf.

## Bevor du loslegst

Drei Dinge bringen dich hinein:

1. **Die Adresse deines Servers.** Hinata ist self-hosted, diese Adresse gehört also nur deiner Organisation. Frag die Person, die ihn eingerichtet hat; sie sieht aus wie `https://track.example.org`.
2. **Ein Konto darauf.** Meistens eine Einladung per E-Mail. Auf manchen Servern kannst du dir selbst eines anlegen.
3. **Die App.** Android, iPhone und iPad, macOS, Windows, Linux — oder einfach ein Browser. Auf der Seite [Download](/de/download.html) findest du alle.

Die App ist überall dieselbe. Nichts auf dieser Seite gilt nur für den Desktop, sofern es nicht ausdrücklich dabeisteht.

## Mit deinem Server verbinden

Es gibt keine eine Adresse, bei der sich alle anmelden. Jede Organisation betreibt ihren eigenen Hinata-Server, deshalb muss die App zuerst wissen, welcher deiner ist — vorher kann sie dir gar nichts zeigen.

![Mit deinem Server verbinden](/assets/img/shot-connect-server.png)
*Der allererste Bildschirm nach der Installation: die Wortmarke hinata, ein Feld „Server-URL“, vorbelegt mit https://, und die Schaltfläche „Verbinden“. Mehr steht nicht darauf — kein Konto zur Auswahl, nichts zum Überspringen.*

Die App fragt diese Adresse, wer sie ist. Sie macht erst weiter, wenn der Server antwortet und sich als Hinata-Server ausweist. Bis dahin bleibst du genau da, wo du bist.

Das ist Absicht. Eine App, die rät oder still auf irgendeinen Standard zurückfällt, wäre eine App, die die Arbeit deiner Organisation irgendwohin schicken könnte, wo sie nicht hingehört. Hinata hält lieber an und fragt nach.

### Wenn die Verbindung scheitert

Dann steht da *„Verbindung zu diesem Server fehlgeschlagen. Bitte URL prüfen.“* Geh diese Liste durch, bevor du jemanden um Hilfe bittest:

- **Prüfe die Schreibweise, inklusive `https://`.** Ein fehlendes `s` ist mit Abstand die häufigste Ursache.
- **Prüfe, ob du im richtigen Netz bist.** Viele Organisationen betreiben Hinata hinter einem VPN oder im Büronetz. Aus dem Café ist er schlicht nicht erreichbar — und die App kann das nicht von einer falschen Adresse unterscheiden.
- **Prüfe, ob die Adresse einen Port braucht**, etwa `https://track.example.org:3356`. Wer den Server betreibt, weiß das.
- **Frag, ob der Server läuft.** Manchmal lautet die ehrliche Antwort: gerade nicht.

!!! note "Diesen Schritt kannst du nicht überspringen"
    In den veröffentlichten Apps steckt kein Server — weder im App-Store-Build noch im Play-Store-Build noch in den Desktop-Builds. Genau das macht sie zu *deiner* App, die auf *deinen* Server zeigt. Die einzige Ausnahme ist der Browser: Wenn deine Organisation die Web-Version selbst betreibt, kann die Adresse schon eingetragen sein — dann siehst du diesen Bildschirm nie.

### Mehr als ein Server

Hinata merkt sich jeden Server, mit dem du dich verbunden hast, und hält die Anmeldungen getrennt. Das zählt, wenn du mit einem Kunden arbeitest, der sein eigenes Hinata betreibt, oder wenn deine Firma neben dem echten noch einen Testserver hat. Gespeicherte Server erscheinen unter dem Verbindungsformular, du springst also schon vor dem Anmelden dazwischen hin und her — und aus der App heraus zeigt **Einstellungen → Server verwalten** dieselbe Liste.

![Die Serververwaltung](/assets/img/shot-server-manager.png)
*„Server verwalten“: eine Zeile pro gespeichertem Server, mit dem Abzeichen „Eigener“ oder „Cloud“, einem grünen Punkt und der Antwortzeit in Millisekunden, wenn er erreichbar ist, und einem roten „Offline“, wenn nicht. Der Haken markiert den Server, mit dem diese App gerade verbunden ist; „Server hinzufügen“ sitzt unten im Sheet.*

Die Erreichbarkeitsprüfung läuft, während das Sheet offen ist — eine Offline-Zeile heißt also: der Server, nicht die App.

!!! warning "Einen Server zu vergessen löscht seine Anmeldung"
    Wenn du einen Server aus der Liste entfernst, werden auch die gespeicherten Zugangsdaten *auf diesem Gerät* gelöscht. Dein Konto auf dem Server bleibt unangetastet — du musst dich beim nächsten Mal nur wieder anmelden.

## Anmelden

Sobald der Server antwortet, bekommst du seinen Anmeldebildschirm. Was darauf steht, hängt davon ab, wie deine Administration den Server eingerichtet hat — nicht jede Option unten wird bei dir dabei sein.

![Der Anmeldebildschirm](/assets/img/shot-sign-in.png)
*Ein Anmeldebildschirm mit allem eingeschaltet: „E-Mail oder Benutzername“, „Passwort“, „Passwort vergessen?“, „Anmelden“, eine Schaltfläche „Weiter mit …“ für den Single-Sign-on-Anbieter des Servers und darunter „Konto erstellen“. Der Chip oben auf der Karte nennt den Server, bei dem du dich anmeldest — und wechselt zu einem anderen.*

### Mit Benutzername und Passwort

Wenn du das Passwort mehrmals hintereinander vertippst, pausiert dich der Server eine Weile und sagt *„Zu viele Fehlversuche. Bitte später erneut versuchen.“* Das ist ein Schutz gegen Brute-Force-Angriffe, keine Strafe, und er löst sich nach ein paar Minuten von selbst auf.

### Wenn Zwei-Faktor aktiv ist

Ist für dein Konto die Zwei-Faktor-Authentifizierung eingeschaltet, kommt beim Anmelden ein Bildschirm dazu: **Zwei-Faktor-Authentifizierung**, mit der Frage nach dem **6-stelligen Code aus deiner Authenticator-App**.

Ein Wiederherstellungscode funktioniert hier ebenfalls — einer von denen, die du beim Einrichten speichern solltest. Jeder gilt genau einmal. Wie du das einrichtest (und neue Codes bekommst), steht unter [Dein Konto](/de/guide-account.html).

### Mit Single Sign-on

Drück **Weiter mit …**, dein Browser öffnet sich, du meldest dich so an, wie du es überall sonst tust, und landest angemeldet wieder in Hinata. Die Schaltfläche trägt den Namen eures Identitätsanbieters, es gibt also nichts zu raten.

Manche Server schalten Passwörter komplett ab und machen Single Sign-on zum einzigen Weg hinein. Dann sagt der Anmeldebildschirm das offen, statt dir ein Passwortfeld zu zeigen, das nicht funktionieren kann.

### Wenn du noch kein Konto hast

Auf manchen Servern kann sich jede und jeder mit **Konto erstellen** selbst eines anlegen; andere lassen nur eingeladene Personen hinein. Ist die Selbstregistrierung an, musst du normalerweise erst deine E-Mail-Adresse bestätigen, und auf strengeren Servern muss dich zusätzlich eine Administratorin oder ein Administrator freigeben.

So oder so enthält die Einladungs- oder Bestätigungsmail einen Link. Öffne ihn auf dem Gerät, auf dem du Hinata nutzen willst — dann bringt er dich direkt in die App.

### Wenn du dein Passwort vergessen hast

**Passwort vergessen?** schickt dir einen Link zum Zurücksetzen per E-Mail. Dieselbe Regel: Öffne ihn auf dem Gerät, das du nutzen willst; er landet dich in der App mit einer frischen Passwortabfrage, nicht in einem Browser-Tab, den du danach wegwerfen musst.

!!! note "Was davon du bekommst, entscheidet dein Server"
    Passwörter, Selbstregistrierung, Admin-Freigabe und Single Sign-on sind Schalter, die deine Administration kontrolliert — und die sich jederzeit ändern lassen, ohne dass jemand etwas neu installiert. Fehlt etwas von hier auf deinem Anmeldebildschirm, wurde es bewusst abgeschaltet. Wer den Server betreibt, findet die Details unter [Authentifizierung](/de/authentication.html) und [Single Sign-on](/de/sso.html).

## Die Tour

Beim allerersten Verbinden mit einem Server spielt die App eine kurze Einführung ab: eine Willkommensseite, dann drei Karten zu **Projekte**, **Sprints** und **Teams**.

Sie läuft *vor* der Anmeldung, es ist also wirklich nur eine Tour — nichts, was du dort antippst, berührt deinen Workspace. Wisch oder drück **Weiter**, um durchzugehen, **Überspringen** in der Ecke, um ans Ende zu springen, und **Loslegen** zum Abschließen.

Du siehst sie einmal pro Gerät. Wenn du sie noch einmal möchtest — nun ja, dafür gibt es dieses Handbuch.

## Ein Rundgang durch deinen Workspace

Nach dem Anmelden landest du auf **Home**, deinem Dashboard. So sieht das Ganze auf einem Desktop-Bildschirm aus:

![Das Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Home auf dem Desktop. Links läuft die dunkelblaue Navigationsleiste mit der bernsteinfarbenen Schaltfläche „Neue Aufgabe“ ganz oben; in der Mitte die Karte zum aktiven Sprint und die Liste „Fokus heute“; rechts stapeln sich Kennzahlen, Projektfortschritt und Fokuszeit.*

### Die Navigationsleiste

Die dunkle Leiste links bringt dich überall hin. Ganz oben sitzt die bernsteinfarbene Schaltfläche **Neue Aufgabe** — das Bedienelement, das du am häufigsten drückst, bewusst dort platziert, wo du es nicht übersehen kannst. Darunter sind die Ziele in zwei Gruppen geteilt.

**Work** ist das, was du täglich anfasst:

| Eintrag | Wofür er da ist |
| --- | --- |
| **Home** | Dein Dashboard: Fokus heute, aktiver Sprint, Fortschritt und Zeit. |
| **Teams** | Die Gruppen, in denen du bist — und welche Projekte jede davon öffnet. |
| **Projekte** | Jedes Projekt, das du sehen kannst, mit Kürzel, Mitgliedern und Workflow. |
| **Issues** | Die vollständige, filterbare Liste aller Vorgänge über deine Projekte hinweg. |
| **Board** | Das agile Board — Spalten, Swimlanes, Drag-and-drop. |

**Plan** holst du dir, wenn du einen Schritt zurücktrittst:

| Eintrag | Wofür er da ist |
| --- | --- |
| **Beobachtet** | Vorgänge, über die du auf dem Laufenden bleiben wolltest. |
| **Gantt** | Die Zeitachse: Termine, Abhängigkeiten, Meilensteine und der kritische Pfad. |
| **Stundenzettel** | Deine Woche an erfasster Arbeit, Stunde für Stunde. |
| **Berichte** | Burndown, Velocity, Durchlaufzeit und Verteilungen. |
| **Wissen** | Die Wissensdatenbank — Artikel, Notizen, Dokumentation. |

Ganz unten schrumpft **Einklappen** die Leiste auf reine Symbole, wenn du den Platz zurückhaben willst — die Reihenfolge bleibt gleich, dein Muskelgedächtnis überlebt das also — und **Einstellungen** öffnet dein Konto.

!!! tip "Lerne eine Tastenkombination, und zwar diese"
    **⌘K** auf macOS, **Strg+K** überall sonst, von jeder Stelle der App aus. Sie öffnet die Suchpalette, die Vorgänge, Projekte, Personen, Boards und Artikel findet, ein Kürzel wie `HIN-42` direkt annimmt und Befehle ausführt — darunter *Neuen Vorgang erstellen* und *Hell / Dunkel umschalten*. Mehr dazu unter [Dinge finden](/de/guide-search.html).

### Die obere Leiste

Die Leiste am oberen Rand trägt drei Dinge:

- **Die Wortmarke hinata** links. Auf einem gebrandeten Server steht hier stattdessen der Name und das Logo deiner Organisation.
- **Das Suchfeld** in der Mitte, mit dem ⌘K-Hinweis. Ein Klick darauf öffnet dieselbe Palette wie die Tastenkombination.
- **Glocke und dein Avatar** rechts. Die Glocke trägt einen Punkt, wenn etwas auf dich wartet; dein Avatar öffnet dein Konto.

### Dein Dashboard

Home beantwortet genau eine Frage: *Was sollte ich heute tun?* Von oben nach unten gelesen:

- **Die Begrüßung** kennt die Tageszeit und spricht dich mit Namen an. Darunter stehen das Datum und, wenn ein Sprint läuft, an welchem Tag davon du bist — „Sprint-Tag 14 von 14“ ist eine sanfte Art zu sagen, dass der Sprint heute endet.
- **Die große Karte** ist eben dieser aktive Sprint: Name, Ziel, Fortschritt als Prozentring, der Tag, die Story Points und die Anzahl der Vorgänge. **Zum Board** springt direkt in die Arbeit, und die Reihe Gesichter zeigt, wer daran sitzt. Läuft kein Sprint, lädt die Karte dich ein, einen zu planen.
- **Fokus heute** ist die kurze Liste der Vorgänge, die heute wirklich etwas von dir wollen — Typ-Symbol, Titel, Kürzel und, in Rot, wie überfällig sie sind. **Alle Issues** öffnet die vollständige Liste.
- **Die Kennzahlen** — Heutige Aufgaben, In Progress, Backlog, Done — sind Zahlen zum Handeln, keine Dekoration.
- **Projektfortschritt** teilt alles, was du sehen kannst, als Ring in Done, In Progress und Backlog auf.
- **Fokuszeit** zeigt die Stunden, die du erfasst hast, nach **Woche** oder **Monat**.
- **Team-Ranking** vergleicht die erledigte Arbeit der letzten 30 Tage, sobald genug davon zusammenkommt, um den Vergleich zu lohnen.

### Mach das Dashboard zu deinem

**Anpassen**, oben rechts, verwandelt das Dashboard in einen Editor.

![Das Dashboard im Bearbeitungsmodus](/assets/img/shot-dashboard-customize.png)
*Der Bearbeitungsmodus: über den Karten erscheinen drei Auswahlfelder — „Hero-Board“ auf „Automatisch (aktiver Sprint)“, „Dashboard-Daten“ auf „Alle Projekte“, „Team-Ranking“ auf „Alle Teams“ — jede Karte bekommt ein Auge zum Ausblenden, und aus „Anpassen“ ist „Fertig“ geworden.*

Auf *Automatisch* folgt die große Karte dem laufenden Sprint; zeigst du stattdessen auf ein Board, bleibt sie dort. Die beiden Auswahlfelder für den Datenbereich grenzen die Zahlen auf bestimmte Projekte oder Teams ein, statt auf alles, was du sehen kannst — das zählt, sobald du in mehr als zwei oder drei Dingen drinsteckst. Und eine Karte, die nicht zu eurer Arbeitsweise passt — meist das Team-Ranking — darf einfach verschwinden.

Drück **Fertig**, wenn es passt. Das Layout wird an deinem Konto gespeichert, nicht am Gerät — es wartet also auch auf deinem Handy auf dich.

### Auf dem Handy oder in einem schmalen Fenster

Dieselbe App, umsortiert statt reduziert.

![Home auf dem Handy](/assets/img/shot-mobile-dashboard.png)
*Derselbe Home-Bildschirm auf dem Handy: Sprint-Karte, Kennzahlen und „Fokus heute“, unten die schwebende Glasleiste — Home, Issues, Board, Mehr — mit ihrer abgesetzten Suchschaltfläche.*

![Das Sheet „Mehr“ auf dem Handy](/assets/img/shot-mobile-more-sheet.png)
*„Mehr“ öffnet ein Sheet über der Seite: oben dein Konto, darunter die ganze Gruppe „Plan“ als Kacheln — Projekte, Teams, Beobachtet, Gantt, Stundenzettel, Berichte, Wissen.*

Auf dem Handy fehlt nichts; es sind dieselben Bildschirme und dieselben Daten, für einen Daumen gelegt. [Auf dem Handy](/de/guide-mobile.html) beschreibt die Unterschiede, die es wirklich gibt.

## Hell, dunkel und deine Sprache

Öffne **Einstellungen** unten in der Leiste und such die Karte **Darstellung & App**.

![Die Sprachauswahl](/assets/img/shot-language-picker.png)
*Die Karte „Darstellung & App“ auf dem Handy, mit geöffneter Sprachauswahl: zwei Einträge, und ein Haken an dem, der gerade gilt. Darüber nennt die Karte den Server, mit dem diese App verbunden ist, und trägt „Server verwalten“.*

Dein allererster Start nimmt die Sprache, die zu deinem Gerät passt; danach bleibt deine Wahl bestehen. Sie reist außerdem mit jeder Anfrage an den Server mit — Meldungen und Fehler, die *vom* Server kommen, treffen also ebenfalls in deiner Sprache ein.

**Darstellung**, unter der Sprachzeile, sind drei Schaltflächen: dem **System** folgen, immer **Hell**, immer **Dunkel**. Der honigbernsteinfarbene Akzent ist in beiden bewusst derselbe Farbton, es verschiebt sich also nichts, wenn die Sonne untergeht. Und wenn du die Einstellungen gar nicht öffnen magst: Die ⌘K-Palette kennt *Hell / Dunkel umschalten* als Befehl.

Der Rest der Einstellungen — Profil, E-Mail-Adresse, Passwort, Zwei-Faktor, aktive Sitzungen und deine Daten — steht unter [Dein Konto](/de/guide-account.html).

## Deine ersten fünf Minuten

Wenn du gerade etwas Konkretes tun möchtest, mach das hier der Reihe nach. Jeder Schritt dauert unter einer Minute und zeigt dir einen Teil der App, den du täglich brauchst.

1. **Öffne Projekte** und sieh, worauf du Zugriff hast. Ist die Liste kürzer als erwartet, ist das normal — [Projekte & Teams](/de/guide-projects.html) erklärt, warum.
2. **Klick auf eine Projektkarte.** Sie öffnet die Vorgangsliste dieses Projekts.
3. **Öffne irgendeinen Vorgang.** Lies Beschreibung, Aktivität, Kommentare. Hier wird die meiste Zeit vergehen.
4. **Drück ⌘K und tipp ein Kürzel** — `HIN-1`, oder wie auch immer das Präfix deines Projekts lautet. Sieh zu, wie es direkt dorthin springt.
5. **Drück „Neue Aufgabe“** und leg etwas Kleines, Echtes an. Archivieren kannst du es hinterher immer noch.
6. **Geh zurück auf Home** und finde deinen neuen Vorgang in den Kennzahlen wieder.

## Dasselbe Konto, jedes Gerät

Hinata ist eine App, kompiliert für Android, iPhone und iPad, das Web, macOS, Windows und Linux. Dasselbe Konto, dieselben Daten, überall.

Änderungen reisen live: Setz etwas auf dem Laptop auf erledigt, und es ist auf deinem Handy erledigt, bevor du den Laptop weggelegt hast — die App hält eine offene Verbindung zum Server, statt ab und zu nachzufragen. Kommentare, Anhänge und Board-Bewegungen anderer Leute erscheinen genauso, ohne dass du irgendetwas neu lädst.

Eine Anmeldung auf einem neuen Gerät meldet dich nirgendwo sonst ab. **Einstellungen → Aktive Sitzungen** listet jedes Gerät, das gerade angemeldet ist, markiert das, auf dem du sitzt, und lässt dich jedes andere beenden — genau das Richtige, wenn ein Handy abhandenkommt.

## Wenn deine App anders aussieht als diese Seite

Eine Handvoll Dinge hängt wirklich davon ab, wie dein Server eingerichtet wurde. Es lohnt sich zu wissen, welche — damit du nicht nach einer Schaltfläche suchst, die es nie gab:

- **Wie du dich anmeldest** — Passwort, Single Sign-on oder nur eines von beiden.
- **Ob du dich selbst registrieren kannst**, und ob dich jemand freigeben muss.
- **Ob Push-Benachrichtigungen dein Gerät erreichen.** Benachrichtigungen in der App und per E-Mail funktionieren immer; Push hängt daran, dass der Server an ein Push-Relay angebunden ist — und unter Linux gibt es Push gar nicht.
- **Ob E-Mails zu Vorgängen werden.** Manche Server beobachten ein Postfach und legen eingehende Mails automatisch als Vorgänge ab.
- **Größen- und Typgrenzen für Anhänge**, die deine Betreiberin oder dein Betreiber setzt.
- **Name und Logo deiner Organisation**, die vom Server kommen, nicht aus der App.

Nichts davon kannst du selbst umstellen. Steht dir eines im Weg, ist die Person, die den Server betreibt, die richtige Ansprechpartnerin.

## Wie es weitergeht

Du bist drin und findest dich zurecht. Ab hier folg dem, was zu dem passt, was du wirklich tun musst:

- **[Projekte & Teams](/de/guide-projects.html)** — was ein Projekt ist, was das Präfix `HIN-42` bedeutet und warum du manche Projekte siehst und andere nicht. Fang hier an; fast alles andere setzt es voraus.
- **[Mit Vorgängen arbeiten](/de/guide-issues.html)** — einen anlegen, ihn gut ausfüllen und durch sein Leben bewegen.
- **[Boards & Sprints](/de/guide-boards.html)** — das Board, das Backlog und die Planung in Zyklen.
- **[Timeline & Abhängigkeiten](/de/guide-timeline.html)** — Termine, Reihenfolge und was was blockiert.
- **[Zeit erfassen](/de/guide-time.html)** — Arbeit buchen und den Stundenzettel füllen.
- **[Kommentare & Anhänge](/de/guide-collaboration.html)** — über Arbeit reden, dort wo die Arbeit liegt.
- **[Dinge finden](/de/guide-search.html)** — die Palette, Filter und dieser eine Vorgang aus dem März.
- **[Dokumentation schreiben](/de/guide-knowledge.html)** — die Wissensdatenbank, und wann du sie statt eines Vorgangs nutzt.
- **[Berichte & Dashboard](/de/guide-reports.html)** — was die Diagramme bedeuten und welchen du trauen kannst.
- **[Auf dem Laufenden bleiben](/de/guide-notifications.html)** — Benachrichtigungen, Beobachten und die Wochenübersicht.
- **[Dein Konto](/de/guide-account.html)** — Profil, Passwort, Zwei-Faktor, Sitzungen und deine Daten.
- **[Auf dem Handy](/de/guide-mobile.html)** — was sich auf kleinem Bildschirm ändert und was nicht.

!!! tip "Hier ist nichts aus Versehen unwiederbringlich"
    Vorgänge werden standardmäßig archiviert statt gelöscht, Projekte lassen sich archivieren statt entfernen, und die wirklich zerstörerischen Aktionen verlangen, dass du erst einen Namen eintippst. Schau dich um. Es passiert nichts.
