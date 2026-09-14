---
title: Erste Schritte
description: Mit dem Server verbinden, anmelden und dich im Workspace zurechtfinden.
---

# Erste Schritte

In Hinata ist jede Aufgabe, jeder Fehler und jede Idee ein **Vorgang** (in der App *Issue*). Vorgänge liegen in **Projekten** und laufen über Boards, Zeitachsen und Berichte, bis sie erledigt sind.

Diese Seite bringt dich von der frisch installierten App in deinen Workspace.

## Die Begriffe, die du brauchst

| Begriff | Was er hier bedeutet |
| --- | --- |
| **Issue / Vorgang** | Ein Stück Arbeit: eine Aufgabe, ein Bug, ein Feature, eine Frage. |
| **Projekt** | Der Behälter für Vorgänge, etwa ein Produkt, ein Dienst oder eine Initiative. |
| **Projektkürzel** | Die kurze ID, die jeder Vorgang von seinem Projekt bekommt, etwa `HIN-42`. |
| **Team** | Eine Gruppe von Personen und die Projekte, die sie öffnen kann. |
| **Board** | Die Spaltenansicht der Projektarbeit, in der du Karten verschiebst. |
| **Workflowstatus** | Die Spalten selbst, zum Beispiel *Backlog*, *In Progress* und *Done*. |
| **Sprint** | Ein fester Zeitraum, meist zwei Wochen, mit ausgewählten Vorgängen. |
| **Backlog** | Alles, was noch in keinem Sprint steckt. |
| **Stichwort (Label)** | Ein farbiges Etikett für einen Vorgang, etwa `design` oder `security`. |
| **Epic** | Ein großes Arbeitspaket, zu dem andere Vorgänge gehören. |

## Bevor du loslegst

Du brauchst:

1. **Die Adresse deines Servers**, etwa `https://track.example.org`. Jede Organisation betreibt ihren eigenen Server. Frag die Person, die ihn eingerichtet hat.
2. **Ein Konto**, meist per Einladung per E-Mail. Auf manchen Servern legst du dir selbst eins an.
3. **Die App** für Android, iPhone und iPad, macOS, Windows, Linux oder den Browser. Alle unter [Download](/de/download.html).

Die App ist überall gleich. Was nur am Desktop gilt, steht dabei.

## Mit deinem Server verbinden

![Mit deinem Server verbinden](/assets/img/shot-connect-server.png)
*Der erste Bildschirm nach der Installation.*

Gib die Adresse ins Feld „Server-URL“ ein (vorbelegt mit `https://`) und tippe auf „Verbinden“. Die App geht erst weiter, wenn sich der Server als Hinata-Server ausweist. Sie rät nie und nimmt keinen Standardserver.

### Wenn die Verbindung scheitert

Du siehst *„Verbindung zu diesem Server fehlgeschlagen. Bitte URL prüfen.“* Prüf:

- **Schreibweise inklusive `https://`.** Ein fehlendes `s` ist die häufigste Ursache.
- **Das Netz.** Viele Server sind nur über VPN oder im Büronetz erreichbar. Für die App sieht das aus wie eine falsche Adresse.
- **Den Port**, etwa `https://track.example.org:3356`. Wer den Server betreibt, weiß das.
- **Ob der Server gerade läuft.**

!!! note "Diesen Schritt kannst du nicht überspringen"
    In den Apps aus App Store, Play Store und den Desktopversionen ist kein Server eingebaut. Nur im Browser kann die Adresse schon eingetragen sein, wenn deine Organisation die Webversion selbst betreibt.

### Mehr als ein Server

Hinata merkt sich jeden Server und hält die Anmeldungen getrennt, etwa für einen Kunden mit eigenem Hinata oder einen Testserver. Gespeicherte Server stehen unter dem Verbindungsformular. In der App findest du sie unter **Einstellungen → Server verwalten**.

![Die Serververwaltung](/assets/img/shot-server-manager.png)
*„Server verwalten“ mit einer Zeile pro Server.*

Jede Zeile trägt das Abzeichen „Eigener“ oder „Cloud“. Ein grüner Punkt mit der Antwortzeit in Millisekunden heißt erreichbar, ein rotes „Offline“ heißt, der Server antwortet nicht. Geprüft wird, solange das Sheet offen ist. Der Haken markiert den verbundenen Server, „Server hinzufügen“ steht unten.

!!! warning "Einen Server zu vergessen löscht seine Anmeldung"
    Entfernst du einen Server, werden seine Zugangsdaten *auf diesem Gerät* gelöscht. Dein Konto bleibt. Du meldest dich nächstes Mal neu an.

## Anmelden

Welche Optionen der Anmeldebildschirm zeigt, legt deine Administration fest.

![Der Anmeldebildschirm](/assets/img/shot-sign-in.png)
*Der Anmeldebildschirm mit allen Optionen.*

Der Chip oben auf der Karte nennt den Server, bei dem du dich anmeldest. Darüber wechselst du auch zu einem anderen.

### Mit Benutzername und Passwort

Gib „E-Mail oder Benutzername“ und „Passwort“ ein und tippe auf „Anmelden“. Nach mehreren Fehlversuchen sperrt dich der Server ein paar Minuten: *„Zu viele Fehlversuche. Bitte später erneut versuchen.“*

### Wenn Zwei-Faktor aktiv ist

Ein zusätzlicher Bildschirm **Zwei-Faktor-Authentifizierung** fragt nach dem **6-stelligen Code aus deiner Authenticator-App**. Ein Wiederherstellungscode geht auch, jeder genau einmal. Einrichtung und neue Codes: [Dein Konto](/de/guide-account.html).

### Mit Single Sign-on

Tippe auf **Weiter mit …** (mit dem Namen eures Identitätsanbieters). Du meldest dich im Browser wie gewohnt an und landest angemeldet in Hinata. Erlaubt ein Server nur Single Sign-on, sagt der Anmeldebildschirm das und zeigt kein Passwortfeld.

### Wenn du noch kein Konto hast

Erlaubt der Server es, legst du mit **Konto erstellen** selbst eins an. Sonst kommen nur Eingeladene hinein. Meist bestätigst du zuerst deine E-Mail-Adresse. Auf strengeren Servern muss dich die Administration zusätzlich freigeben.

Öffne den Link aus der Mail auf dem Gerät, auf dem du Hinata nutzt. Er führt direkt in die App.

### Wenn du dein Passwort vergessen hast

**Passwort vergessen?** schickt dir einen Link per E-Mail. Öffne ihn auf deinem Gerät, dann fragt die App direkt nach dem neuen Passwort.

!!! note "Was davon du bekommst, entscheidet dein Server"
    Passwörter, Selbstregistrierung, Freigabe durch die Administration und Single Sign-on lassen sich jederzeit ohne Neuinstallation umschalten. Fehlt etwas, ist es bewusst aus. Für Betreiber: [Authentifizierung](/de/authentication.html) und [Single Sign-on](/de/sso.html).

## Die Tour

Beim ersten Verbinden mit einem Server zeigt die App vor der Anmeldung eine kurze Einführung: eine Willkommensseite und drei Karten zu **Projekte**, **Sprints** und **Teams**. Sie ändert nichts an deinem Workspace.

Wisch oder tippe auf **Weiter**. **Überspringen** springt ans Ende, **Loslegen** schließt ab. Du siehst die Tour einmal pro Gerät.

## Ein Rundgang durch deinen Workspace

Nach dem Anmelden landest du auf **Home**, deinem Dashboard.

![Das Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Home auf dem Desktop.*

### Die Navigationsleiste

Die dunkelblaue Leiste links führt überallhin. Oben sitzt die bernsteinfarbene Schaltfläche **Neue Aufgabe**, darunter zwei Gruppen.

**Work** für den Alltag:

| Eintrag | Wofür er da ist |
| --- | --- |
| **Home** | Dein Dashboard: Fokus heute, aktiver Sprint, Fortschritt und Zeit. |
| **Teams** | Deine Gruppen und die Projekte, die jede davon öffnet. |
| **Projekte** | Jedes Projekt, das du sehen kannst, mit Kürzel, Mitgliedern und Workflow. |
| **Issues** | Die filterbare Liste aller Vorgänge in deinen Projekten. |
| **Board** | Das agile Board mit Spalten, Swimlanes und Ziehen und Ablegen. |

**Plan** für den Überblick:

| Eintrag | Wofür er da ist |
| --- | --- |
| **Beobachtet** | Vorgänge, über die du auf dem Laufenden bleiben willst. |
| **Gantt** | Die Zeitachse mit Terminen, Abhängigkeiten, Meilensteinen und kritischem Pfad. |
| **Stundenzettel** | Deine erfasste Arbeit der Woche, Stunde für Stunde. |
| **Berichte** | Burndown, Velocity, Durchlaufzeit und Verteilungen. |
| **Wissen** | Die Wissensdatenbank mit Artikeln, Notizen und Dokumentation. |

Unten verkleinert **Einklappen** die Leiste auf Symbole, **Einstellungen** öffnet dein Konto.

!!! tip "Die wichtigste Tastenkombination"
    **⌘K** auf macOS, **Strg+K** sonst, überall in der App. Die Suchpalette findet Vorgänge, Projekte, Personen, Boards und Artikel, springt direkt zu `HIN-42` und kennt Befehle wie *Neuen Vorgang erstellen* und *Hell / Dunkel umschalten*. Mehr unter [Dinge finden](/de/guide-search.html).

### Die obere Leiste

- Links die Wortmarke hinata, auf gebrandeten Servern Name und Logo deiner Organisation.
- In der Mitte das Suchfeld. Es öffnet dieselbe Palette wie ⌘K.
- Rechts die Glocke (mit Punkt, wenn etwas auf dich wartet) und dein Avatar, der dein Konto öffnet.

### Dein Dashboard

Home zeigt, was heute ansteht:

- **Begrüßung** mit Namen, Datum und, wenn ein Sprint läuft, dem Sprinttag. „Sprint-Tag 14 von 14“ heißt: Der Sprint endet heute.
- **Die große Karte** zeigt den aktiven Sprint: Name, Ziel, Fortschrittsring, Tag, Story Points und Anzahl der Vorgänge. **Zum Board** öffnet die Arbeit, die Gesichter zeigen, wer mitarbeitet. Ohne Sprint lädt sie ein, einen zu planen.
- **Fokus heute** listet deine Vorgänge für heute mit Typsymbol, Titel, Kürzel und Überfälligkeit in Rot. **Alle Issues** öffnet die ganze Liste.
- **Kennzahlen:** Heutige Aufgaben, In Progress, Backlog, Done.
- **Projektfortschritt** zeigt alles Sichtbare als Ring aus Done, In Progress und Backlog.
- **Fokuszeit** zeigt deine erfassten Stunden nach **Woche** oder **Monat**.
- **Team-Ranking** vergleicht die erledigte Arbeit der letzten 30 Tage, sobald genug zusammenkommt.

### Mach das Dashboard zu deinem

Tippe oben rechts auf **Anpassen**.

![Das Dashboard im Bearbeitungsmodus](/assets/img/shot-dashboard-customize.png)
*Der Bearbeitungsmodus mit drei Auswahlfeldern.*

- **Hero-Board:** Auf „Automatisch (aktiver Sprint)“ folgt die große Karte dem laufenden Sprint. Wählst du ein Board, bleibt sie dort.
- **Dashboard-Daten** („Alle Projekte“) und **Team-Ranking** („Alle Teams“) grenzen die Zahlen auf bestimmte Projekte oder Teams ein.
- **Das Auge** auf jeder Karte blendet sie aus.

Tippe auf **Fertig**. Das Layout hängt an deinem Konto und gilt auch auf dem Handy.

### Auf dem Handy oder in einem schmalen Fenster

![Home auf dem Handy](/assets/img/shot-mobile-dashboard.png)
*Home auf dem Handy.*

![Das Sheet „Mehr“ auf dem Handy](/assets/img/shot-mobile-more-sheet.png)
*Das Sheet „Mehr“.*

Unten schwebt eine Glasleiste mit Home, Issues, Board und Mehr sowie eine eigene Suchschaltfläche. **Mehr** zeigt dein Konto und die Gruppe „Plan“ als Kacheln: Projekte, Teams, Beobachtet, Gantt, Stundenzettel, Berichte, Wissen.

Bildschirme und Daten sind dieselben. Die wenigen Unterschiede stehen unter [Auf dem Handy](/de/guide-mobile.html).

## Hell, dunkel und deine Sprache

Öffne **Einstellungen** und dort die Karte **Darstellung & App**. Sie zeigt auch den verbundenen Server und „Server verwalten“.

![Die Sprachauswahl](/assets/img/shot-language-picker.png)
*Die Sprachauswahl mit zwei Sprachen.*

- **Sprache:** Beim ersten Start gilt die Sprache deines Geräts, danach deine Wahl. Auch Meldungen und Fehler vom Server kommen in dieser Sprache.
- **Darstellung:** **System**, **Hell** oder **Dunkel**. Der Bernsteinakzent bleibt in beiden gleich. Alternativ: *Hell / Dunkel umschalten* in der Palette.

Alles Weitere (Profil, E-Mail-Adresse, Passwort, Zwei-Faktor, aktive Sitzungen, deine Daten) steht unter [Dein Konto](/de/guide-account.html).

## Deine ersten fünf Minuten

1. **Öffne Projekte.** Eine kurze Liste ist normal, [Projekte & Teams](/de/guide-projects.html) erklärt warum.
2. **Klick auf eine Projektkarte.** Du siehst ihre Vorgänge.
3. **Öffne einen Vorgang** und lies Beschreibung, Aktivität und Kommentare.
4. **Drück ⌘K und tipp ein Kürzel** wie `HIN-1`. Die App springt direkt hin.
5. **Tippe auf „Neue Aufgabe“** und leg etwas Kleines, Echtes an. Archivieren geht später.
6. **Geh zurück auf Home.** Dein Vorgang zählt jetzt in den Kennzahlen mit.

## Dasselbe Konto, jedes Gerät

Hinata läuft auf Android, iPhone und iPad, im Web, auf macOS, Windows und Linux, mit demselben Konto und denselben Daten.

Änderungen kommen live an, weil die App eine offene Verbindung zum Server hält. Kommentare, Anhänge und verschobene Karten erscheinen ohne Neuladen.

Eine neue Anmeldung meldet dich nirgendwo ab. **Einstellungen → Aktive Sitzungen** zeigt alle angemeldeten Geräte, markiert dein aktuelles und beendet jedes andere, etwa bei einem verlorenen Handy.

## Wenn deine App anders aussieht als diese Seite

Das hängt vom Server ab, und nur die Person, die ihn betreibt, kann es ändern:

- **Anmeldung** mit Passwort, Single Sign-on oder nur einem davon.
- **Selbstregistrierung** und ob dich jemand freigeben muss.
- **Push-Benachrichtigungen.** Benachrichtigungen in der App und per E-Mail gehen immer. Push braucht einen Server mit Anbindung an ein Relay und fehlt unter Linux ganz.
- **E-Mails als Vorgänge.** Manche Server legen Mails aus einem Postfach automatisch als Vorgänge an.
- **Grenzen für Anhänge** bei Größe und Dateityp.
- **Name und Logo** deiner Organisation.

## Wie es weitergeht

- **[Projekte & Teams](/de/guide-projects.html):** Projekte, Kürzel und Sichtbarkeit. Fang hier an.
- **[Mit Vorgängen arbeiten](/de/guide-issues.html):** anlegen, ausfüllen, voranbringen.
- **[Boards & Sprints](/de/guide-boards.html):** Board, Backlog und Planung in Zyklen.
- **[Timeline & Abhängigkeiten](/de/guide-timeline.html):** Termine und Blockaden.
- **[Zeit erfassen](/de/guide-time.html):** Arbeit buchen, Stundenzettel füllen.
- **[Kommentare & Anhänge](/de/guide-collaboration.html):** am Vorgang über die Arbeit reden.
- **[Dinge finden](/de/guide-search.html):** Palette und Filter.
- **[Dokumentation schreiben](/de/guide-knowledge.html):** die Wissensdatenbank.
- **[Berichte & Dashboard](/de/guide-reports.html):** was die Diagramme bedeuten.
- **[Auf dem Laufenden bleiben](/de/guide-notifications.html):** Benachrichtigungen, Beobachten, Wochenübersicht.
- **[Dein Konto](/de/guide-account.html):** Profil, Passwort, Zwei-Faktor, Sitzungen, Daten.
- **[Auf dem Handy](/de/guide-mobile.html):** was sich auf kleinen Bildschirmen ändert.

!!! tip "Aus Versehen geht kaum etwas verloren"
    Vorgänge werden standardmäßig archiviert, Projekte lassen sich archivieren. Für wirklich zerstörerische Aktionen musst du einen Namen eintippen. Schau dich ruhig um.
