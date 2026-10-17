---
title: Erweitertes Time-Tracking
description: Timer, Kalender, Tags, Sperrdaten, Stundenzettel-Freigaben, Berichte, geteilte Einträge und Abrechnung im erweiterten Zeiterfassungsmodul.
---

# Erweitertes Time-Tracking

Schalten deine Organisationsadmins das erweiterte Modul ein, wird aus **Stundenzettel** in der Seitenleiste **Zeiterfassung**. Alles rund um deine Stunden liegt dann auf einer Seite. Die Grundlagen bleiben wie unter [Zeit erfassen](/de/guide-time.html) beschrieben.

## Die Ansichten

Oben in der **Zeiterfassung** wechselst du zwischen Pillen:

- **Liste**: deine Einträge nach Tagen.
- **Kalender**: eine Woche oder ein Monat mit deinen Einträgen als Blöcke.
- **Stundenzettel**: das Raster aus Tagen und Projekten.
- **Abwesenheiten**: Urlaub und Krankheit, siehe [Abwesenheiten](/de/absences.html).
- **Berichte**: Summen, Exporte und Abrechnung.
- **Freigaben**: nur, wenn Stundenzettel-Freigaben eingeschaltet sind.

![Die Liste der Zeiteinträge](/assets/img/shot-time-entries.png)
*Die Listenansicht mit den Einträgen einer Woche.*

**Neuer Eintrag** öffnet den Editor. Dort tippst du entweder eine Dauer oder Beginn und Ende ein. Du ergänzt eine Beschreibung, ordnest den Eintrag einem Projekt oder Vorgang zu und wählst Tags. **Zeit erfassen** an einem Vorgang öffnet denselben Editor, schon diesem Vorgang zugeordnet.

## Der Timer

Die Timerleiste steht oben in der Zeiterfassung. **Starten** lässt eine Stoppuhr laufen. Der Pfeil daneben öffnet **Zählweise wählen**:

- **Stoppuhr**: zählt hoch, bis du stoppst.
- **Countdown**: zählt standardmäßig von 25 Minuten herunter (1 bis 1440 Minuten) und stoppt bei null von selbst.
- **Pomodoro**: 25 Minuten Arbeit, 5 Minuten Pause, nach vier Runden eine lange Pause von 15 Minuten. Die Phase wechselt nicht von allein. Du drückst **Pause starten** und **Weiterarbeiten**. Jedes Arbeitsintervall wird ein eigener Eintrag. Pausen werden nie erfasst.

![Die Timerleiste](/assets/img/shot-time-timer.png)
*Die Timerleiste mit einer laufenden Stoppuhr.*

**Stoppen** macht aus dem Timer einen Eintrag. Verlangt deine Organisation Pflichtfelder, etwa einen Tag (Schlagwort) oder einen Vorgang, öffnet sich zuerst der Editor. Brichst du ab, läuft der Timer weiter. **Timer verwerfen** wirft ihn ohne Eintrag weg. Ein Timer, der 24 Stunden läuft, wird dort abgeschnitten.

Deine eigenen Längen und den Ton am Ende eines Intervalls stellst du unter **Einstellungen → Zeiterfassung** ein.

### Timer außerhalb der App

Die App kann den Timer auch außerhalb ihres Fensters zeigen. Die Karte **Timer außerhalb der App** fragt einmal, und nichts ist an, bevor du zustimmst:

- eine Mitteilung, wenn ein Countdown oder ein Pomodoro-Intervall endet,
- auf Android eine stille Mitteilung, das Widget auf dem Startbildschirm und eine Kachel in den Schnelleinstellungen, solange der Timer läuft,
- auf iPhone und iPad eine Live-Aktivität auf dem Sperrbildschirm und in der Dynamic Island und das Timer-Widget auf Home- und Sperrbildschirm,
- im Web eine Browser-Mitteilung, wenn der Tab im Hintergrund ist, die laufende Zeit im Tab-Titel und eine Markierung am App-Symbol der installierten Web-App,
- auf dem Desktop der laufende Timer in der Menüleiste oder im Infobereich, wie unten beschrieben, und auf dem Mac das Timer-Widget auf dem Schreibtisch und in der Mitteilungszentrale.

Die Texte sind allgemein und nennen nie den Vorgang. Deine Schalter bleiben auf diesem Gerät und gehen nicht an den Server.

Live-Aktivität und Widgets zeigen die Zeit und ob du arbeitest oder Pause machst. Die Beschreibung erscheint nur, wenn **Details auf dem Sperrbildschirm** an ist. Das Widget fügst du wie jedes andere hinzu: unter iOS aus der Widget-Galerie von Home- oder Sperrbildschirm, unter Android aus der Widget-Liste des Launchers. Ein Tipp darauf öffnet den Fokusmodus. Sind Live-Aktivitäten für Hinata in den Systemeinstellungen aus, sagen das die Einstellungen, und die Widgets laufen weiter.

**Ohne die App zu öffnen.** **Stopp** und **Pause machen** oder **Weiter** in der Mitteilung, die Knöpfe im Widget und auf Android die Kachel in den Schnelleinstellungen wirken direkt, die App bleibt zu. Auf iPhone und iPad (ab iOS 17) startet das Widget ohne laufenden Timer mit seinem Knopf eine Stoppuhr, und die Live-Aktivität hat selbst einen Stopp-Knopf, im Pomodoro auch die nächste Phase: in der aufgeklappten Dynamic Island, auf dem Sperrbildschirm und in der Mitteilungszentrale. Ein Tipp auf die Kachel stoppt den Timer, in einem Pomodoro wechselt er die Phase. Ein langer Druck oder ein Tipp ohne laufenden Timer öffnet den Fokusmodus. Auf einem gesperrten Gerät musst du zuerst entsperren. Die Kachel bietet Hinata nach deinem ersten Timer einmal an; du kannst sie auch selbst über das Bearbeiten der Schnelleinstellungen hinzufügen.

**Live Update (Android 16 und neuer).** Die Mitteilung des laufenden Timers wird zum Live Update: ein Chip in der Statusleiste, der die Zeit zählt, ein Eintrag oben in den Mitteilungen und auf Geräten, die das zeigen, der Sperrbildschirm, das Always-on-Display und die Now Bar von Samsung. Der Chip zeigt nur die Zeit, bei Arbeit und Pause gleich. Ein Pomodoro zeigt seinen Satz als einen Balken, ein Abschnitt je Intervall und Pause; auf Android 17 zeigen Countdown und Stoppuhr ihre Zeit als große Zahl. Der Schalter **Live Update in der Statusleiste** unter **Einstellungen → Zeiterfassung** ist mit der laufenden Mitteilung an. Sind Live Updates für Hinata in den Systemeinstellungen aus, sagen das die Einstellungen und öffnen die passende Seite; die Dauer-Mitteilung bleibt, wie sie war. Ob ein Gerät Live Updates für jede App zeigt, entscheidet der Hersteller; auf Samsung-Geräten heißt der Schalter **Live-Benachrichtigungen für alle Apps**. Wischst du die Mitteilung weg, bleibt sie weg, bis der Timer die Phase wechselt oder du einen neuen startest.

**Zuverlässigkeitsmodus (Android).** Die Akku-Manager mancher Hersteller beenden die Dauer-Mitteilung nach einer Weile. Mit **Zuverlässigkeitsmodus** hält ein Vordergrunddienst genau diese Mitteilung, solange der Timer läuft. Er startet nur, während die App offen ist, endet mit dem Timer, beim Abmelden oder wenn du ihn ausschaltest, und erhebt nichts. Ab Werk ist er aus.

**Im Hintergrund aktualisieren (iPhone und iPad).** Ab Werk ändert nur die geöffnete App die Live-Aktivität. Schaltest du unter **Einstellungen → Zeiterfassung** **Im Hintergrund aktualisieren** ein, kommen ein Phasenwechsel und ein Stopp auf einem anderen Gerät auch bei geschlossener App auf dem Sperrbildschirm an. Dein Server schickt sie Ende-zu-Ende verschlüsselt über Hinata Connect, Google und Apple, die nur sehen, wann etwas gesendet wird. Der Schalter gilt ab der nächsten Live-Aktivität. Was genau gesendet wird, steht unter [Datenschutz](/de/time-tracking-privacy.html).

**Als Alarm klingeln (iPhone und iPad ab iOS 26).** Unter **Einstellungen → Zeiterfassung** gibt es unter **Intervallende** den Schalter **Als Alarm klingeln**. Ist er an, endet ein Countdown oder ein Pomodoro-Intervall wie ein Wecker: der Alarm klingelt auch im Stumm-Modus, während eines Fokus und bei geschlossener App, und auf einer gekoppelten Apple Watch. Er ersetzt dann die Mitteilung am Intervallende. Bis dahin läuft der Countdown des Systems auf dem Sperrbildschirm und in der Dynamic Island, mit Stopp und im Pomodoro der nächsten Phase; die Stoppuhr behält ihre Live-Aktivität. Der klingelnde Alarm bietet **Stopp** und im Pomodoro **Pause machen** oder **Weiter**; beides wirkt wie der Knopf in der App, auch wenn die App zu ist. Beim ersten Einschalten fragt iOS, ob Hinata Alarme stellen darf. Ist die App vorn, sagt es der Hinweis in der App, und der Alarm bleibt still. Nimmt das System keine weiteren Alarme an, kommt das Intervallende wieder als Mitteilung, und die App sagt es einmal. Abmelden und **Jetzt löschen** nehmen alle Alarme weg.

**Siri, Kurzbefehle und Steuerelemente (iPhone und iPad).** Hinata bringt fünf Kurzbefehle mit: **Timer starten**, **Timer stoppen**, **Nächste Phase**, **Timer-Status** und **Fokus öffnen**. Du findest sie in der App Kurzbefehle unter Hinata und in der Suche auf dem Home-Bildschirm. Siri versteht zum Beispiel „Timer starten in Hinata“, „Timer stoppen in Hinata“ oder „Wie lange läuft mein Hinata Timer“. Beim ersten Mal fragt Siri, ob sie die Hinata-Kurzbefehle aktivieren soll. **Timer starten** startet eine Stoppuhr, auf Wunsch mit Beschreibung und einem deiner Projekte; für deine Projekte steht der Kurzbefehl auch gleich mit Projekt bereit. Läuft schon ein Timer, startet er keinen zweiten. Ab iOS 18 legst du drei Steuerelemente ins Kontrollzentrum, auf den Sperrbildschirm oder auf die Aktionstaste: **Timer** (an startet eine Stoppuhr, aus stoppt), **Nächste Phase** und **Fokus**. Starten, Stoppen und der Phasenwechsel wirken, ohne dass die App aufgeht, und die Live-Aktivität erscheint oder endet mit. Auf einem gesperrten Gerät verlangt iOS zuerst Face ID oder den Code. **Timer-Status** und das Steuerelement **Timer** kennen den Timer aus demselben Datensatz wie das Widget, also nur, wenn **Live-Aktivität und Widgets** an ist; die Beschreibung sagt Siri nie. Die Kurzbefehle brauchen iOS 17, die Steuerelemente iOS 18.

### Auf dem Desktop

**Menüleiste und Infobereich.** Auf dem Mac zeigt die Menüleiste die laufende Zeit neben dem Hinata-Symbol. Unter Windows und Linux zeigt ein Symbol im Infobereich, dass der Timer läuft, und unter Windows nennt sein Tooltip die Zeit. Arbeit und Pause sehen gleich aus, bei einer Bildschirmfreigabe sieht also niemand, wann du Pause machst: Während eines Pomodoro zeigen Menüleiste, Tooltip und Taskleiste nur, dass der Timer läuft, aber keine Zeit, denn die Restzeit eines Intervalls würde die Pause verraten. Ein Klick auf das Symbol öffnet ein Menü: starten oder stoppen, das nächste Pomodoro-Intervall, die Fokusansicht, das Fenster und Beenden. Erst das geöffnete Menü sagt, ob gerade Fokus oder Pause ist, und es nennt, woran du arbeitest, nur wenn du **Beschreibung im Menü** einschaltest (nicht unter Linux, siehe unten).

**Widgets auf dem Mac (ab macOS 14).** Das Timer-Widget gibt es auf dem Mac in klein und mittel, für den Schreibtisch und die Mitteilungszentrale. Es steht in der Widget-Galerie, sobald Hinata einmal gestartet ist: Rechtsklick auf den Schreibtisch, **Widgets bearbeiten**, nach Hinata suchen. Es zeigt wie auf dem iPhone nur die Zeit und ob du arbeitest oder Pause machst, nie die Beschreibung, und tickt ohne die App. Ein Klick öffnet den Fokusmodus. Knöpfe hat es auf dem Mac nicht. Der Schalter **Menüleiste und Widgets** unter Einstellungen → Zeiterfassung gilt für beides. Auch iPhone-Widgets lassen sich auf dem Mac ablegen (Galerie, **Von iPhone**); sie zeigen den Timer des iPhones.

**Beim Schließen weiterlaufen.** Schließt du das Fenster, läuft ein Timer in der Menüleiste oder im Infobereich weiter, und das Fenster kommt über das Menü zurück (auf dem Mac auch über das Dock). Auf dem Mac ist das von Anfang an an, ⌘Q beendet die App wie gewohnt. Unter Windows und Linux ist es aus, bis du es einschaltest.

**Taskleiste (Windows).** Der Taskleisten-Knopf füllt sich mit dem Fortschritt eines Countdowns, trägt eine kleine Markierung, solange der Timer läuft, und seine Vorschau hat zwei Knöpfe: starten oder stoppen und die Fokusansicht.

**Systemweite Kürzel.** Von Anfang an aus, und nur zusammen mit dem Symbol in Menüleiste oder Infobereich, damit ein Tastendruck nie einen Timer startet, den du nicht siehst. Schalte unter Einstellungen → Zeiterfassung **Systemweite Kürzel** ein, dann startest und stoppst du den Timer und öffnest die Fokusansicht aus jeder App:

| Kürzel | Mac | Windows |
| --- | --- | --- |
| Starten oder stoppen | **⌃⌥⌘S** | **Strg+Alt+Umschalt+S** |
| Fokusansicht | **⌃⌥⌘F** | **Strg+Alt+Umschalt+F** |

Andere Kombinationen wählst du, indem du auf eine klickst und die neuen Tasten drückst. Eine Kombination braucht Control oder Command (unter Windows Strg oder die Windows-Taste), denn Umschalt und Option allein schreiben in jeder App Zeichen; unter Windows ist Strg+Alt allein AltGr und wird aus demselben Grund abgelehnt. Nutzt eine andere App oder das System eine Kombination schon, sagen das die Einstellungen. Auf dem Mac ist das Kürzel einer anderen App nicht immer zu sehen, deshalb bittet dich **Jetzt prüfen**, eines davon einmal zu drücken, gern mit einer anderen App im Vordergrund, und sagt dir, ob der Tastendruck ankam. Während der Prüfung startet und stoppt nichts.

Die Kürzel laufen über die Kürzel-Registrierung des Betriebssystems. Die App hört nur ihre zwei Kombinationen und keine andere Taste, und sie fragt nach keiner Bedienungshilfen-Berechtigung.

**Linux.** Das Symbol im Infobereich braucht eine Leiste, die solche Symbole zeigt: KDE Plasma und die meisten Desktops tun das, GNOME mit der AppIndicator-Erweiterung (unter Ubuntu ist sie an). Ohne sie erscheint nichts, und das Fenster versteckt sich auch nicht in einen Infobereich, den du nicht siehst. Das Menü im Infobereich nennt unter Linux nie, woran du arbeitest, denn jedes Programm der Sitzung kann es lesen.

**Systemweite Kürzel unter Linux.** Hier legt dein Desktop fest, welche Tasten auslösen. Hinata schlägt dieselben Kombinationen wie unter Windows vor. GNOME (ab Version 48) und KDE Plasma 6 fragen beim ersten Einschalten einmal, welche Kürzel du erlaubst. Bis du dort bestätigst, haben die Kürzel noch keine Tasten, und die Einstellungen sagen das. Die Einstellungen zeigen dann die Tasten, die der Desktop gemeldet hat, und **Im System konfigurieren** öffnet seine Kürzel-Einstellungen, in denen du sie änderst. Hast du im Dialog abgelehnt, fragt derselbe Knopf noch einmal. Sway und andere wlroots-Desktops bieten keine systemweiten Kürzel an, dort steht „nicht verfügbar“. Das AppImage braucht seine Desktop-Integration (etwa über Gear Lever oder AppImageLauncher), damit der Desktop weiß, welche App fragt. Im Snap musst du dafür nichts von Hand verbinden. Auch unter Linux hört die App nur diese zwei Kürzel und keine andere Taste.

## Fokusmodus und Tastenkürzel

Der Fokusmodus zeigt nur den laufenden Timer und woran du arbeitest. Du öffnest ihn mit **⇧⌘F** (unter Windows und Linux **Strg+Umschalt+F**). **Esc** verlässt ihn.

![Der Fokusmodus](/assets/img/shot-time-focus.png)
*Der Fokus-Modus mit einer laufenden Stoppuhr.*

| Kürzel | Aktion |
| --- | --- |
| **⇧⌘S** | Timer starten oder stoppen |
| **⇧⌘E** | Zeit erfassen |
| **⇧⌘F** | Fokusmodus |

Unter Windows und Linux nimmst du **Strg** statt **⌘**. Die ⌘K-Palette hat außerdem Befehle für Zeiterfassung, Stundenzettel, Abwesenheiten und **Abwesenheit beantragen**.

## Der Kalender

**Kalender** zeigt eine **Woche** oder einen **Monat**. In der Woche ziehst du einen Block in 15-Minuten-Schritten auf, um einen Eintrag anzulegen, und verschiebst Blöcke per Ziehen. Langer Druck oder Rechtsklick auf einen Tag öffnet das Tagesmenü, zum Beispiel um für diesen Tag eine Abwesenheit zu beantragen.

![Der Kalender der Zeiterfassung](/assets/img/shot-time-calendar.png)
*Eine Woche im Kalender mit Einträgen und einem Feiertag.*

Feiertage, Abwesenheiten und Tage ohne geplante Stunden sind leicht markiert. Das ist keine Sperre. Ein Tag, der sich wirklich nicht mehr ändern lässt, trägt ein Schloss.

## Der Stundenzettel

Der Stundenzettel ist hier dasselbe Raster wie im Grundmodus, mit mehr darauf:

- In deiner eigenen Zeile tippst du auf eine Zelle, um Zeit für diesen Tag und dieses Projekt anzulegen oder zu korrigieren.
- **Deine Kapazität** stellt deine geplanten Stunden, abzüglich Feiertage und Abwesenheiten, neben das, was du gebucht hast. Nur du siehst das.
- Mit Freigaben folgt das Raster deinem Freigabezeitraum und zeigt darüber dessen Stand.

![Der Stundenzettel im Zeiterfassungsmodul](/assets/img/shot-timesheet.png)
*Der Stundenzettel für einen Monat.*

## Tags

Mit Tags ordnest du deine Zeit, zum Beispiel nach Kunde oder Art der Arbeit. Du wählst sie im Editor.

- Alle können Tags anlegen, außer deine Organisation erlaubt das nur Organisationsadmins.
- Umbenennen und löschen dürfen nur Organisationsadmins.
- Ein Name ist ohne Rücksicht auf Groß- und Kleinschreibung eindeutig und hat höchstens 40 Zeichen.
- Deine Organisation kann Tags zur Pflicht machen. Der Editor sagt dir das, bevor er speichert.

![Die Tag-Auswahl](/assets/img/shot-time-tags.png)
*Die Tags der Organisation und wie oft jeder genutzt wird.*

## Verlauf eines Eintrags

**Verlauf dieses Eintrags** im Editor zeigt, was andere an deinem Eintrag geändert haben, mit wer und wann. Deine eigenen Änderungen stehen dort nicht.

## Gesperrte Tage und Korrekturen

Manche Tage lassen sich nicht mehr ändern. Editor und Liste zeigen dann einen Chip mit dem Grund, wer die Sperre aufheben kann und was du tun kannst:

- **Sperrdatum**: deine Organisation hat alles vor einem Datum geschlossen.
- **Eingereichter Zeitraum**: der Zeitraum wurde eingereicht oder freigegeben.
- **Rechnung**: der Eintrag steht auf einer ausgestellten Rechnung.
- **Zu weit zurück**: der Tag ist älter, als deine Organisation erlaubt.

Was du tun kannst:

- **Korrektur anfragen** bittet die Personen, die die Sperre aufheben können, einen Eintrag für dich zu ändern.
- **Ältere Tage anfragen** bittet darum, Tage zu öffnen, die zu weit zurückliegen. Ein Organisationsadmin kann sie für dich öffnen, nach 14 Tagen schließen sie sich von selbst.

Deine offenen Anfragen findest du unter **Einstellungen → Zeiterfassung → Korrekturen und ältere Tage**.

## Stundenzettel-Freigaben

Nutzt deine Organisation Freigaben, reichst du deinen Stundenzettel je Zeitraum ein. Der Zeitraum kann wöchentlich, zweiwöchentlich, halbmonatlich, monatlich (Standard), quartalsweise oder von der Organisation festgelegt sein.

![Die Ansicht Freigaben](/assets/img/shot-time-approvals.png)
*Die Freigaben mit einem freigegebenen Monat.*

- **Zeitraum einreichen** geht, sobald der Zeitraum vorbei ist. Ein Zeitraum hat höchstens 92 Tage.
- **Zurückziehen** holt ihn zurück, solange niemand entschieden hat.
- Projektleitungen und Organisationsadmins **Freigeben** ihn oder **Zurückgeben** ihn mit Begründung.
- Ein freigegebener Zeitraum lässt sich **Wieder öffnen**, ebenfalls mit Begründung.
- Niemand gibt den eigenen Stundenzettel frei.

Eingereichte und freigegebene Tage sind für Änderungen gesperrt. **Freigaben** hat drei Reiter: **Meine**, **Zu entscheiden** und **Korrekturen**.

## Ziele, Erinnerungen und Hinweise

Erlauben es deine Organisationsadmins, legst du unter **Einstellungen → Zeiterfassung → Erinnerungen** ein **Tagesziel** und ein **Wochenziel** fest. Hinata erinnert dich, wenn Zeit fehlt, an deinen Arbeitstagen und zur Uhrzeit deiner Wahl. Niemand sonst erfährt, ob oder wann du erinnert wurdest.

Arbeitszeithinweise machen auf Dinge aufmerksam wie mehr als 10 Stunden an einem Tag, eine kurze Ruhezeit zwischen zwei Tagen, Arbeit am Sonntag oder an einem Feiertag oder einen spät erfassten Eintrag. Nur du siehst sie, und sie sperren nichts.

## Kalender-Abos

Haben deine Organisationsadmins den Kalender-Import eingeschaltet, kannst du deine eigenen Kalender von Google, Outlook oder Apple abonnieren. Hinata liest sie nur und schreibt nie zurück. Deine Abos siehst nur du.

![Kalender-Abos in den Einstellungen](/assets/img/shot-time-subscriptions.png)
*Ein abonnierter Kalender mit seinem letzten Abruf.*

1. Öffne **Einstellungen → Zeiterfassung → Kalender-Abos** und tippe auf **Hinzufügen**.
2. Gib einen Namen ein, füge die private ICS-Adresse ein (`https://` oder `webcal://`) und wähle eine Farbe.
3. Tippe auf **Abonnieren**.

- Bis zu 10 Kalender. Jeder wird alle 30 Minuten gelesen, von Hand aktualisieren kannst du einmal pro Minute.
- Nach fünf Fehlversuchen in Folge wird ein Kalender pausiert, bis du ihn fortsetzt.
- Termine stehen mit gestricheltem Rand im Kalender, von 30 Tagen zurück bis 90 Tage voraus. Sie zählen in keine Summe.
- Tippe auf einen Termin, um ihn als Eintrag zu übernehmen. Aus einem Termin wird höchstens ein Eintrag. Ganztägige Termine lassen sich nicht übernehmen.
- **Vergangene Termine automatisch übernehmen** macht das für dich, mit Projekt und Tags deiner Wahl.

!!! warning "Die Adresse ist ein Schlüssel"
    Wer die Adresse kennt, kann den Kalender lesen. Hinata speichert sie verschlüsselt und zeigt sie nie wieder an.

## Geteilte Einträge

Habt ihr zu mehreren an etwas gearbeitet, erfasst eine Person und teilt den Eintrag.

![Geteilte Einträge](/assets/img/shot-time-shares.png)
*Von dir geteilte Einträge, einer noch offen.*

1. Öffne deinen Eintrag und tippe auf **Teilen mit…**. Oder tippe **+** in die Beschreibung, um Personen des Projekts zu wählen.
2. Wähle bis zu 20 Personen und tippe auf **Einladungen senden**.

Die anderen finden die Einladung unter **Geteilte Einträge → Eingang**:

- **Annehmen** legt eine Kopie in den eigenen Einträgen an.
- **Anpassen** nimmt sie mit einem anderen Projekt oder anderen Tags an.
- **Ablehnen** sagt nein. Du siehst nur, dass abgelehnt wurde, nie warum.

Die Kopie gehört danach dieser Person. Für sie gelten deren Sperrdaten und Freigaben. Unter **Gesendet** verfolgst du deine Einladungen und kannst offene zurückziehen.

## Berichte, Export und Import

**Berichte** hat acht Reiter: **Projekt** und **Budgets** (siehe [Berichte & Dashboard](/de/guide-reports.html)), dann **Übersicht**, **Einträge**, **Auslastung**, **Abwesenheiten**, **Abrechnung** und **Gespeichert**. Du wählst Zeitraum, Filter und eine Gruppierung nach Projekt, Person, Team, Tätigkeit, Tags, Vorgang, Tag, Woche oder Monat.

![Die Zeitberichte](/assets/img/shot-time-reports.png)
*Die Übersicht der Zeitberichte, nach Projekt gruppiert.*

- Ein Bericht zählt nur, was du ohnehin sehen darfst. Namen anderer erscheinen nur, wo eine Richtlinie es erlaubt. Siehe [Zeiterfassung: Datenschutz & Recht](/de/time-tracking-privacy.html).
- **Auslastung** vergleicht Kapazität und gebuchte Zeit je Person. Es gibt sie nur, wenn deine Organisation sie eingeschaltet hat, und nur für Leitungen und Organisationsadmins.
- **Exportieren** liefert PDF (bis 5.000 Zeilen), Excel (bis 50.000) oder CSV (bis 100.000), oder du druckst. Jeder Export steht im Audit-Protokoll.
- **CSV importieren** übernimmt deine eigenen Einträge aus einer Datei bis 5 MB und 10.000 Zeilen. Exporte aus Hinata und toggl werden erkannt. Jede Zeile wird wie ein getippter Eintrag geprüft, und es werden alle gültigen Zeilen geschrieben oder keine.
- **Bericht speichern** behält bis zu 200 Berichte. Ein gespeicherter Bericht kann einen Link zum Teilen bekommen (nur für Angemeldete, jede Person sieht ihren eigenen Ausschnitt) oder wöchentlich oder monatlich per Mail an bis zu 50 Personen gehen, als Link ohne Anhang.

## Budgets

Ein Projekt kann ein **Zeitbudget** haben. Projektleitungen setzen es unter **Projekt-Einstellungen → Zeiterfassung**. Was davon verbraucht ist, zeigt Hinata als Honigstand an jeder Stelle, an der es zählt:

- in den Projekt-Einstellungen als Röhre für das Budget und eine für die Summe der Schätzungen,
- auf jeder Projektkarte und im Kopf eines Boards mit genau einem Projekt als Kapsel mit Prozentzahl,
- auf dem Dashboard in der Kachel **Budgets** als Wabe mit den drei vollsten Budgets,
- im Vorgang als Röhre für seine Schätzung und im Gantt als Honiglinie am Fuß jedes Balkens,
- in der Timer-Leiste für den laufenden Vorgang, auf dem Handy erst ab dem Warnanteil.

Für das Budget und für die Schätzungen wählt die Leitung je einen Modus:

- **Hinweis beim Erfassen** (Standard): Wer Zeit erfasst, sieht im Formular und in der Stundenzettel-Zelle ab dem Warnanteil, wie viel noch übrig ist, mit dem neuen Eintrag schon eingerechnet. Nach dem Speichern sagt ein Hinweis, wo das Projekt jetzt steht. Die Leitungen und die Admins der Teams des Projekts erfahren es sofort beim Warnanteil, bei 100 % und erneut bei 110, 125 und 150 %.
- **Nur stündliche Meldung**: kein Hinweis im Formular. Die Leitungen bekommen einmal je Stunde Bescheid, wie bisher.

Erfassen wird in keinem Modus gesperrt. Arbeitszeit muss sich immer aufzeichnen lassen. Ob Leitungen benachrichtigt werden, entscheidet die Richtlinie **Budget-Warnungen** der Organisation. Ist sie aus, sagt das die Einstellungsseite des Projekts.

### Verlauf und Prognose

Ein Tipp auf eine Wabe im Dashboard oder auf **Verlauf** in den Projekt-Einstellungen öffnet den Verlauf des Budgets. Die Honigfläche zeigt, wie sich die erfassten Stunden Tag für Tag aufsummiert haben, die Linie darüber das Budget und, falls vorhanden, die Summe der Schätzungen.

Unter der Röhre steht eine Prognose, etwa „Reicht bis etwa 14. November“. Hinata rechnet dafür mit dem Tempo der letzten 14 Tage je Arbeitstag. Wochenenden und die Feiertage des Standardkalenders zählen nicht mit. Gibt es weniger als drei Tage mit Einträgen, sagt die Prognose dazu, dass sie unsicher ist. Ist das Budget schon aufgebraucht oder ruht die Arbeit, steht dort genau das.

### Budget je Sprint

Auf einem Scrum-Board bekommt jeder Sprint ein eigenes Zeitbudget. Wer das Board verwalten darf, setzt es in der Sprintzeile über die Kapsel. Gezählt wird die Zeit auf den Vorgängen des Sprints während seiner Laufzeit. Der Hinweis beim Erfassen und die Meldungen an die Leitungen folgen denselben Regeln wie beim Projektbudget.

### Geldbudget

Ist die Abrechnung eingeschaltet, kann ein Projekt zusätzlich ein **Geldbudget** haben. Hinata bewertet jeden Eintrag mit dem Satz, der für ihn gilt, und zeigt den Betrag als dritte Röhre. Es gibt zwei Arten:

- **Erlös**: bewertet mit den abrechenbaren Sätzen. Die Leitung des Projekts setzt es und sieht es.
- **Kosten**: bewertet mit den Kostensätzen. Nur Admins der Organisation, die das Projekt auch verwalten, setzen und sehen es.

Mitglieder sehen das Geldbudget nie, auch nicht im Formular beim Erfassen. Meldungen zum Geldbudget gehen nur an die Leitungen und nur beim Erlös.

Alle Budgets, die du siehst, stehen gesammelt unter **Berichte → Budgets**, das vollste zuerst. Siehe [Berichte & Dashboard](/de/guide-reports.html).

## Abrechnung

Ist die Abrechnung eingeschaltet, bepreisen Projektleitungen und Organisationsadmins erfasste Zeit.

![Ein Rechnungsentwurf](/assets/img/shot-time-invoices.png)
*Die Rechnungsliste mit einem Entwurf.*

- **Stundensätze**: ein Erlössatz für abrechenbare Einträge, den Projektleitungen setzen, und ein Kostensatz, den nur Organisationsadmins sehen. Der genaueste Satz gewinnt: Vorgang, Projektmitglied, Person, Projekt, Team, Standard. Ein Satz ändert sich ab einem Datum.
- **Berichte** im Reiter **Abrechnung**: **Abrechnung**, **Profitabilität** (nur Organisationsadmins, nie je Person) und **Auslastung**.
- **Rechnungen**: **Rechnung entwerfen** für ein Projekt, bis 92 Tage und 5.000 Einträge. **Ausstellen** gibt ihr die nächste Nummer ohne Lücke, zum Beispiel `INV-2026-00001`, und sperrt ihre Einträge. **Gutschrift schreiben** storniert eine ausgestellte Rechnung einmal und gibt ihre Einträge wieder frei. Rechnungen gibt es als PDF, Word und Excel.

Ausgestellte Rechnungen und Gutschriften werden nie gelöscht.

## Zeiterfassung über MCP

Ein KI-Client, der über [MCP](/de/mcp.html) verbunden ist, kann deine eigenen Einträge erfassen, auflisten, ändern und löschen, deinen Stundenzettel und Summen lesen und deinen Timer starten, stoppen oder verwerfen. Er handelt immer mit deinen Rechten und liest nie die Zeit anderer.

## Nächste Schritte

- Urlaub und Krankheit: [Abwesenheiten: Urlaub und Krankheit](/de/absences.html).
- Für Admins: [einschalten und Regeln festlegen](/de/admin-time-tracking.html).
- Wer was sieht: [Zeiterfassung: Datenschutz & Recht](/de/time-tracking-privacy.html).
