---
title: Auf dem Laufenden bleiben
description: Wie Hinata dich über Glocke, E-Mail und Push informiert und wie du das einstellst.
---

# Auf dem Laufenden bleiben

Hinata meldet Ereignisse über Glocke, E-Mail und Push. Du legst pro Ereignis fest, was dich unterbrechen darf.

## Worüber Hinata dich benachrichtigt

Diese zehn Ereignisse findest du auch in deinen Einstellungen.

| Ereignis | Löst aus, wenn |
| --- | --- |
| **Erwähnungen & Antworten** | Dich jemand per `@` in einer Beschreibung oder einem Kommentar erwähnt oder auf deinen Kommentar antwortet |
| **Vorgang dir zugewiesen** | Du als Bearbeiter hinzugefügt wirst |
| **Kommentare zu meinen Vorgängen** | Jemand einen Vorgang kommentiert, den du erstellt hast oder beobachtest |
| **Statusänderungen** | Ein Vorgang, mit dem du zu tun hast, in eine andere Spalte wandert |
| **Beobachtete Vorgänge** | Sich irgendetwas an einem Vorgang ändert, den du abonniert hast |
| **Neue Vorgänge aus E-Mails** | Eine eingehende E-Mail zu einem Vorgang in einem deiner Projekte wird |
| **Sprints & Fristen** | Ein Sprint startet oder endet oder eine Fälligkeit näher rückt |
| **Team- & Projekteinladungen** | Du zu einem Team oder Projekt hinzugefügt wirst |
| **Wöchentliche Zusammenfassung** | Deine Übersicht der Woche am Montag fertig ist |
| **Sicherheitshinweise** | Eine neue Anmeldung, eine Passwort- oder E-Mail-Änderung stattfindet |

Gut zu wissen:

- **Als Bearbeiter oder Ersteller musst du nicht beobachten.** Änderungen erreichen dich über „Statusänderungen“. „Beobachtete Vorgänge“ ist für Vorgänge, die niemandem zugewiesen sind und die du trotzdem im Blick behalten willst.
- **An Fälligkeiten erinnert Hinata einmal.** Jeden Morgen schaut der Server zwei Tage voraus und erinnert die Bearbeiter offener Vorgänge. Es gibt eine Erinnerung pro Fälligkeitsdatum. Wird das Datum verschoben, kommt eine neue.
- **Über deine eigenen Aktionen hörst du nichts.** Die Glocke zeigt, was andere getan haben.
- **Niemand hört von Arbeit, die er nicht sehen darf.** Beim Versand prüft Hinata, ob die Person das Projekt erreicht, in dem der Vorgang *jetzt* liegt. Wer aus einem Projekt entfernt wurde, bekommt keine Mails mehr dazu.

!!! note "Neue Vorgänge aus E-Mails hängen von deinem Server ab"
    Dieses Ereignis gibt es nur, wenn dein Betreiber ein Postfach mit einem Projekt verbunden hat. Siehe [E-Mail zu Vorgang](/de/email-to-ticket.html).

## Die Glocke und das Mitteilungscenter

Die Glocke sitzt auf jedem Bildschirm oben in der Leiste. Ein Punkt zeigt Ungelesenes an.

![Die Mitteilungsvorschau unter der Glocke mit fünf Einträgen](/assets/img/shot-notification-bell.png)
*Die fünf neuesten Mitteilungen unter der Glocke, ungelesene bernsteinfarben hinterlegt.*

Oben rechts steht „Alle als gelesen markieren“, unten „Alle Mitteilungen anzeigen“. Das vollständige Center gruppiert nach **Heute**, **Gestern**, **Diese Woche**, **Dieser Monat** und **Früher** und lädt beim Scrollen nach.

![Das Mitteilungscenter von Hinata](/assets/img/shot-notifications.png)
*Im Center erklärt jede Zeile in einem Satz, was passiert ist.*

- **Antippen** öffnet das Ziel, etwa den Kommentar mit deiner Erwähnung, und markiert die Mitteilung als gelesen.
- **Nach rechts wischen** schaltet zwischen gelesen und ungelesen um.
- **Nach links wischen** löscht deine Kopie. Am Vorgang ändert sich nichts.

!!! tip "Ungelesen als Merkliste"
    Setz eine Mitteilung wieder auf ungelesen, um sie dir für später zu merken. Der Punkt an der Glocke bleibt, bis du es erledigt hast.

## Drei Kanäle und welche du steuerst

| Kanal | Wo er erscheint | Abschaltbar? |
| --- | --- | --- |
| **In-App** | Glocke und Mitteilungscenter | Nein, wird immer aufgezeichnet |
| **E-Mail** | Dein Postfach | Ja, pro Ereignis |
| **Push** | Systembenachrichtigungen deines Handys oder Desktops | Ja, pro Ereignis |

Die Glocke zeichnet immer alles auf. Deine Einstellungen regeln nur, ob dich etwas zusätzlich *unterbricht*.

- **E-Mail** braucht einen Mailversand, den dein Betreiber einrichtet.
- **Push** gibt es unter Android, iOS, macOS und Windows, nicht unter Linux und im Browser. Siehe [Download](/de/download.html).

!!! note "Der Schalter für Push bleibt überall bedienbar"
    Die Einstellung gehört zu deinem **Konto**. Du kannst sie also auch unter Linux oder im Browser ändern, und sie gilt für dein Handy. Die App weist nur darauf hin, dass dieses Gerät kein Push empfängt.

## Stell ein, was dich erreicht

Öffne **Einstellungen → Benachrichtigungen**.

![Die Benachrichtigungsmatrix in den Einstellungen, mit den beiden Hauptschaltern über dem Raster](/assets/img/shot-notification-matrix.png)
*Oben die Hauptschalter, darunter eine Zeile pro Ereignis mit „E-Mail“ und „Push“.*

Die Hauptschalter **E-Mail-Benachrichtigungen** und **Push-Benachrichtigungen** schalten einen Kanal ganz ab. Deine Auswahl pro Ereignis bleibt gespeichert. Zugestellt wird nur, wenn Hauptschalter *und* Zelle an sind.

![Dieselben Benachrichtigungseinstellungen auf dem Handy, eine Karte pro Ereignis](/assets/img/shot-mobile-notification-matrix.png)
*Auf dem Handy wird jedes Ereignis zu einer eigenen Karte.*

Voreinstellungen eines neuen Kontos:

| Ereignis | E-Mail | Push |
| --- | :---: | :---: |
| Erwähnungen & Antworten | an | an |
| Vorgang dir zugewiesen | an | an |
| Kommentare zu meinen Vorgängen | an | aus |
| Statusänderungen | aus | an |
| Beobachtete Vorgänge | an | an |
| Neue Vorgänge aus E-Mails | aus | an |
| Sprints & Fristen | an | an |
| Team- & Projekteinladungen | an | aus |
| Wöchentliche Zusammenfassung | an | aus |
| Sicherheitshinweise | fest an | fest an |

Sicherheitshinweise lassen sich nicht abschalten. Ihre Zeile zeigt ein Schloss und *Immer aktiv*.

!!! tip "Nimm dir einmal zwei Minuten"
    Schalte die zwei oder drei Zeilen ab, auf die du nie reagierst. Dann bedeutet jede Mitteilung etwas.

## Vorgänge beobachten und bewusst zuhören

1. Öffne den Vorgang.
2. Tippe in der Kopfzeile auf **⋯**.
3. Wähle **Beobachten**.

![Das Beobachten-Panel an einem Vorgang, mit Schalter und Beobachterliste](/assets/img/shot-issue-watch-panel.png)
*Das Panel mit Schalter, deinem Status und „Beobachter dieses Vorgangs“.*

Ein Toast bestätigt: *Du beobachtest diesen Vorgang jetzt.* Der Schalter heißt dann „Beobachtung beenden“. Ein Hinweis wie „Du erhältst bereits Benachrichtigungen als Ersteller.“ zeigt, ob du ohnehin schon informiert wirst.

Alle Abos stehen unter **Beobachtet** in der Seitenleiste (auf dem Handy unter **Mehr**).

![Die Seite „Beobachtete Vorgänge“](/assets/img/shot-watched.png)
*Eine Zeile pro Abo mit Status, Priorität, Bearbeiter und Fälligkeit.*

Ohne Abos erklärt die Seite, wie du sie füllst.

!!! info "Warum beobachtete Vorgänge dein Postfach nicht fluten"
    Glocke und Push melden jede Änderung sofort. Mails fasst Hinata zusammen: Nach etwa fünf Minuten ohne Bearbeitung kommt **eine** Mail mit allen Änderungen, spätestens aber nach einer halben Stunde.

    Bearbeiter und Ersteller bekommen ihre Mail sofort, auch wenn sie zusätzlich beobachten.

## Deine Wochenübersicht

Jeden Montagmorgen fasst Hinata deine Woche zusammen: was das Team und du abgeschlossen habt, deine Fokuszeit und was als Nächstes ansteht. Sie kommt in die Glocke und, wenn die E-Mail für „Wöchentliche Zusammenfassung“ an ist, auch per Mail. Beide öffnen dieselbe Seite. Gibt es nichts zu berichten, kommt keine Übersicht.

![Die Seite Wochenübersicht](/assets/img/shot-weekly-summary.png)
*Die Wochenübersicht mit Kennzahlen, Sprintfortschritt und anstehenden Aufgaben.*

- **Kopf**: Zeitraum, vom Team abgeschlossene Vorgänge, deine erledigten Vorgänge und deine Fokuszeit.
- **Die Woche hinter uns**: Abgeschlossen, Erstellt, Fokuszeit und der Fortschritt des aktiven Sprints.
- **Top-Mitwirkende und Erledigte Highlights**: wer was bewegt hat und eine Auswahl fertiger Arbeit.
- **Deine anstehenden To-Dos**: deine offenen Vorgänge nach Dringlichkeit. Oben steht die Zahl **überfälliger** Einträge, Überfälliges ist rot. Tippe eine Zeile an, um den Vorgang zu öffnen.

Abschalten kannst du die Übersicht in der Zeile **Wöchentliche Zusammenfassung**.

!!! tip "Lies sie vor dem Montagstermin"
    Sie zeigt, was letzte Woche fertig wurde und was diese Woche wackelt.

## Wenn etwas nicht ankommt

Die häufigsten Ursachen stehen oben.

1. **Prüfe den Hauptschalter.** Ein stummgeschalteter Kanal gilt für alle Ereignisse. Die App zeigt das am Schalter an.
2. **Prüfe die Zeile des Ereignisses.** Kommentare und Statusänderungen sind standardmäßig für je einen Kanal aus.
3. **Prüfe, ob du beteiligt bist.** Du hörst von Vorgängen als Bearbeiter, Ersteller oder Beobachter. Mitglied im Projekt zu sein reicht nicht.
4. **Für Push: Prüfe die Berechtigung am Gerät.** Die App fragt beim ersten Anmelden. Hast du abgelehnt, erlaube Push in den Systemeinstellungen. Prüfe unter [Download](/de/download.html), ob deine Plattform Push kann.
5. **Für E-Mail: Frag deinen Betreiber.** Ohne funktionierenden Mailversand auf dem Server hilft keine Einstellung.

!!! warning "Eine Mitteilung zu löschen macht nichts rückgängig"
    Du löschst nur deine Kopie. Soll der Vorgang dich nicht mehr stören, beende die Beobachtung oder gib ihn ab.

## Nächste Schritte

- [Kommentare & Anhänge](/de/guide-collaboration.html): wie du Erwähnungen schreibst, die häufigste Quelle von Mitteilungen.
- [Mit Vorgängen arbeiten](/de/guide-issues.html): Bearbeiter, Ersteller und das Menü ⋯.
- [Dein Konto](/de/guide-account.html): der Rest der Einstellungen.
- [Berichte & Dashboard](/de/guide-reports.html): die Zahlen hinter der Wochenübersicht, jederzeit abrufbar.
