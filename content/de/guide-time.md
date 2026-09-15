---
title: Zeit erfassen
description: Arbeitszeit an Vorgängen erfassen, korrigieren und im Stundenzettel prüfen.
---

# Zeit erfassen

Du erfasst eine Dauer am Vorgang und wählst die Art der Arbeit. Daraus entstehen dein Stundenzettel, die Fokuszeit auf deiner Startseite und die Aufwandsauswertung in den Berichten.

## Zeit an einem Vorgang erfassen

1. Öffne den Vorgang und suche die Karte **Timeline**. Im breiten Fenster steht sie rechts unter Details, auf dem Handy weiter unten.
2. Tippe oben rechts auf der Karte auf **Zeit erfassen**.
3. Trag die Dauer ein und drücke **Speichern**.

![Das Sheet „Zeit erfassen“](/assets/img/shot-time-log.png)
*Das ausgefüllte Sheet mit 1 Stunde 30 Minuten und der Tätigkeitsart „Testen“.*

Pflicht ist nur die Dauer, die Notiz ist optional. Nach dem Speichern steigt der Aufwand am Vorgang, der Eintrag erscheint auf der Karte und dein Stundenzettel zählt ihn mit.

!!! tip "Dauer schnell eintippen"
    **Stunden** startet bei `1`, **Minuten** bei `0`. Für anderthalb Stunden tippst du `30` in **Minuten**. Für 20 Minuten setzt du **Stunden** auf `0` und **Minuten** auf `20`. Die Felder nehmen nur Ziffern an.

![Das Sheet „Zeit erfassen“ auf dem Handy](/assets/img/shot-mobile-time-log.png)
*Auf dem Handy fährt das Sheet von unten hoch, Stunden und Minuten bleiben nebeneinander.*

### Was du eingeben kannst und was nicht

- Ein Eintrag dauert mindestens eine Minute und höchstens 24 Stunden. Arbeit über Mitternacht teilst du auf zwei Tage auf.
- Du kannst bis zu ein Jahr rückdatieren, aber nichts in der Zukunft erfassen. Für Pläne gibt es [Start- und Fälligkeitsdatum](/de/guide-timeline.html).
- Mehrere Einträge am selben Tag und Vorgang sind normal und addieren sich.

![Der Datumsauswähler im Sheet „Zeit erfassen“](/assets/img/shot-time-date.png)
*Der Auswähler öffnet auf heute, graut die Zukunft aus und reicht 365 Tage zurück.*

### Die Eintragsliste

![Die Timeline-Karte eines Vorgangs mit ihren Arbeitseinträgen](/assets/img/shot-time-entries.png)
*Die Karte Timeline mit Aufwandszeile und den acht jüngsten Einträgen.*

Jede Zeile zeigt Dauer · Tätigkeitsart und rechts das Datum. Die Liste enthält die Einträge aller Beteiligten.

- Bei fremden Einträgen siehst du nur Dauer und Tätigkeitsart.
- Name und Notiz siehst du an deinen eigenen Einträgen. Die Projektleitung sieht sie auch und kann Einträge korrigieren.

!!! note "Warum an fremden Einträgen kein Name steht"
    Name und Datum an jedem Eintrag ergäben eine Aufzeichnung, wer wann wie lange gearbeitet hat. So eine Auswertung von Beschäftigtendaten muss bewusst eingeführt werden, wo nötig mit Betriebsvereinbarung. Eine Richtlinie für Betreiber, die das für Projektleitungen freigibt, ist geplant. Bis dahin gilt die Regel für alle.

**Alle Einträge (24)** unter der Liste öffnet die ganze Historie mit der bisher erfassten Gesamtzeit. Weitere Einträge laden beim Scrollen nach.

## Die richtige Tätigkeitsart wählen

Es gibt sechs feste Tätigkeitsarten. So bedeuten sie für alle dasselbe und die Zahlen lassen sich addieren.

![Das Menü „Tätigkeitsart“](/assets/img/shot-time-activity.png)
*Das Menü „Tätigkeitsart“ mit sechs Einträgen und ohne „Sonstiges“.*

- **Entwicklung**: die Sache bauen und ändern.
- **Testen**: sie prüfen, von Hand oder mit Tests.
- **Dokumentation**: sie aufschreiben, in der [Wissensdatenbank](/de/guide-knowledge.html) oder anderswo.
- **Design**: festlegen, wie sie aussieht oder sich verhält.
- **Meeting**: Zeit mit anderen zu diesem Vorgang.
- **Support**: anderen helfen, die Sache zu nutzen oder weiterzukommen.

Daraus entsteht der Bericht **Zeit pro Tätigkeit**. Er stimmt nur, wenn alle Meetings auch als Meeting erfassen. In der englischen App heißen die Arten *Development*, *Testing* und so weiter. Dahinter steckt derselbe Wert, Berichte zählen also sprachunabhängig.

## Schätzung, Aufwand und der Unterschied dazwischen

Die Karte **Timeline** zeigt eine Zeile wie `9h 30m von 10h aufgewendet` (siehe [die Eintragsliste](#die-eintragsliste)).

- Die erste Zahl ist die Summe aller Einträge am Vorgang, von allen Beteiligten.
- Die zweite ist die **Zeitschätzung**, die ursprüngliche Annahme für die ganze Aufgabe.

Nähert sich die erste Zahl der zweiten, wird es knapp. Eine Zeitschätzung siehst du außerdem:

- **Auf der Karte im Board** als kleiner Chip mit dem bisherigen Aufwand.
- **In der [Timeline](/de/guide-timeline.html)** als gefüllter Anteil im Balken. Ist er voll, obwohl noch Tage übrig sind, war die Schätzung zu optimistisch.

!!! note "Eine Schätzung ist kein Story Point"
    **Schätzen** in der Sprintplanung (die Karten mit Fibonacci-Zahlen) setzt **Story Points**, eine relative Größe für Planung und Velocity. Das ist ein anderes Feld als die Zeitschätzung, und die meisten Teams nutzen es im Alltag. Ohne Zeitschätzung steht dort `9h 30m von — aufgewendet`. Deine erfasste Zeit zählt trotzdem überall.

## Der wöchentliche Stundenzettel

**Stundenzettel** findest du in der Seitenleiste, auf dem Handy unter **Mehr**.

![Der Hinata-Stundenzettel mit einer Woche und ihrer Navigation](/assets/img/shot-timesheet.png)
*Eine Woche im Stundenzettel, eine Zeile je Person und Projekt.*

### Eine Zeile lesen

- Jede Zeile ist eine Person in einem Projekt. Das Projekt kommt automatisch aus dem Vorgang.
- Die Spalten laufen von Montag bis Sonntag, am Ende steht **Gesamt**.
- Tage ohne Einträge zeigen einen Strich statt einer Null.

### Zwischen Wochen wechseln

- Die Woche steht oben rechts. Die Pfeile daneben springen eine Woche zurück oder vor.
- Wochen beginnen am Montag. Arbeit vom Sonntag landet am Ende ihrer Woche.
- **Heute** im Seitenkopf springt zur aktuellen Woche und lädt sie neu. Der Knopf ist nur aktiv, wenn du eine andere Woche ansiehst.

### Wessen Zeit du siehst

- Du siehst nur **deine eigene** Arbeit. Der Server lehnt Anfragen nach fremden Stunden ab.
- Administratorinnen und Administratoren sehen alle Zeilen. Sie haben je einen durchsuchbaren Filter für Person und Projekt.

Zeit an einem verschobenen Vorgang oder einem Projekt, das es nicht mehr gibt, bleibt deine. Sie steht unter **Nicht zugeordnet**.

!!! note "Leer heißt nicht kaputt"
    „In dieser Woche wurden keine Arbeitszeiten erfasst“ gilt nur für die angezeigte Woche. Geh mit dem linken Pfeil zurück, bevor du einen Fehler vermutest.

## Eine Woche schnell füllen

- **Erfasse, sobald du aufhörst.** Du bist schon im Vorgang, das Sheet braucht vier Tipps.
- **Gestern vergessen?** Öffne die Vorgänge von gestern, erfasse dort und stell das **Datum** auf gestern.
- **Erfasse per Commit.** Ist dein Projekt mit einem Git-Repository verbunden und sind Smart Commits aktiv, reicht diese Zeile in der Nachricht:

```text
MOB-42 #time 2h 30m
```

Erlaubt sind `w`, `d`, `h` und `m`. Ein Tag hat 8 Stunden, eine Woche 5 Tage, `1d 4h` sind also zwölf Stunden. Das Repository verbindet eine Administratorin oder ein Administrator, siehe [Git-Integration](/de/git-integration.html).

Der Eintrag gehört **der Autorin oder dem Autor des Commits**, erkannt an der E-Mail-Adresse im Commit. Er erscheint in deren Stundenzettel, Fokuszeit und im Bericht „Zeit pro Tätigkeit“. Datum ist der Tag des Commits in der Zeitzone dieser Person. Die Notiz enthält kurze SHA und Betreffzeile. Ohne Tätigkeitsart zählt er als **Entwicklung**.

!!! note "Ein Commit bucht nur auf ein bekanntes Konto"
    Die Adresse muss zu einem aktiven Hinata-Konto gehören, und die Person muss Mitglied des Projekts sein. Sonst wird die Zeile übersprungen, im Serverprotokoll vermerkt und keine Zeit gebucht, auch nicht bei der Person, die das Repository verbunden hat. Fehlen deine Commits, prüfe zuerst `git config user.email`.

## Einen Eintrag korrigieren

Jeder Eintrag auf der Karte und im Sheet **Alle Einträge** hat rechts ein Menü.

- **Eintrag bearbeiten** öffnet das Sheet mit den aktuellen Werten. Nach **Speichern** wird der **Aufwand** neu berechnet. Die Datumsregeln gelten weiter.
- **Löschen** fragt mit Dauer und Tag nach und lässt sich nicht rückgängig machen. Der **Aufwand** sinkt um genau diese Dauer.

### Wessen Einträge du ändern darfst

- **Deine eigenen** darfst du immer bearbeiten und löschen.
- **Fremde** darfst du als Projektleitung oder Administration löschen, aber nicht bearbeiten. So steht unter einem Namen nie etwas, das die Person nicht selbst erfasst hat. Bitte sie danach, neu zu erfassen. Jede Löschung steht mit beiden Namen im Audit-Protokoll.

!!! tip "Zu wenig erfasst?"
    Erfasse die fehlende Zeit als zweiten Eintrag. Einträge am selben Vorgang und Tag addieren sich. Bearbeiten ist für falsche Dauern gedacht.

Einträge mit **Smart Commits (vor 2.0)** stammen aus älteren Versionen, die Zeit aus Commits mit `#time` direkt gebucht haben. Sie haben keinen Namen, zählen aber weiter. Entfernen können sie nur Projektleitung oder Administration.

## Arbeitszeiten, Abwesenheiten und Feiertage

Wenn deine Administration die erweiterte Zeiterfassung eingeschaltet hat, findest du in deinen **Einstellungen** den Abschnitt **Arbeitszeiten und Abwesenheiten**. Er dient nur der Planung. Du kannst an jedem Tag Zeit erfassen, auch an Feiertagen und an Tagen, an denen du nicht da bist.

- **Geplante Stunden** sind deine Stunden je Wochentag. Solange du keine eigenen festlegst, gilt die Vorgabe des Servers. Eine Änderung gilt ab dem Datum, das du wählst, frühere Wochen behalten ihre Stunden. Hier wählst du auch den Feiertagskalender, nach dem du dich richtest.
- **Abwesenheiten** sind Urlaub, Krankheit oder Sonstiges, für einen einzelnen Tag oder einen Zeitraum. Ein einzelner Tag kann ein halber Tag sein. Die Notiz ist freiwillig, sehen können sie nur du und die Administration.
- **Feiertage** kommen aus den Kalendern, die deine Administration im Adminbereich unter **Feiertage** pflegt. Sie trägt Tage von Hand ein oder importiert ein Jahr aus einer Kalenderadresse.

Was sich dadurch zeigt:

- Eintragsliste und Kalender markieren Feiertage, Abwesenheiten und Tage ohne geplante Stunden. Die Markierung ist bewusst zurückhaltend, denn sie ist keine Sperre. Ein Tag, der sich wirklich nicht mehr ändern lässt, trägt ein Schloss.
- Dein eigener Stundenzettel zeigt **Deine Kapazität**: deine geplanten Stunden im Zeitraum, abzüglich Feiertage und Abwesenheiten, neben dem, was du gebucht hast. Nur du siehst das.
- Mit eingeschalteten Arbeitszeithinweisen bekommt ein Eintrag an einem Feiertag einen Hinweis, genau wie ein Eintrag an einem Sonntag.

## Wo deine erfasste Zeit landet

1. **Am Vorgang**: Der Aufwand wird aus allen Einträgen neu berechnet und ist immer die echte Summe.
2. **Fokuszeit im [Dashboard](/de/guide-reports.html)**: deine Minuten der letzten sieben Tage, heute in Bernstein. **Monat** zeigt die letzten fünf Kalenderwochen. Es zählt nur *deine* Einträge.
3. **Dein Stundenzettel**, wie oben beschrieben.
4. **Bericht „Zeit pro Tätigkeit“** in den [Berichten](/de/guide-reports.html): die Zeit des ganzen Projekts aus den letzten 30 Tagen nach Tätigkeitsart, als Dauer.
5. **Deine Wochenübersicht**: deine Fokuszeit der Woche neben dem, was du abgeschlossen hast. Siehe [Auf dem Laufenden bleiben](/de/guide-notifications.html).

## Gewohnheiten, die die Zahlen wertvoll halten

- **Runde maßvoll.** 25 Minuten als 30 sind in Ordnung. Zwei Stunden als ganzer Tag verfälschen jede spätere Schätzung.
- **Erfasse Meetings.** Sie gehen am häufigsten verloren.
- **Erfasse am richtigen Vorgang.** Arbeit an einer [Unteraufgabe](/de/guide-issues.html) erfasst du dort. Aufwand wird nicht an den übergeordneten Vorgang weitergegeben.
- **Erfasse nichts an einem Epic.** Dort lässt sich die Zeit keiner konkreten Arbeit zuordnen.
- **Niemand bewertet dich nach Stunden.** Fokuszeit steht nur auf deinem eigenen Dashboard. Das Ranking im Team zählt gelöste Vorgänge.

!!! info "Zeiterfassung benachrichtigt niemanden"
    Beobachter eines Vorgangs erfahren nichts von neuen Einträgen. War die Aufgabe viel größer als gedacht, schreib einen [Kommentar](/de/guide-collaboration.html).

## Nächste Schritte

- Setze die Daten, gegen die Zeit gemessen wird, in der [Timeline](/de/guide-timeline.html).
- Sieh, was aus deinen Stunden wird, im [Dashboard und in den Berichten](/de/guide-reports.html).
- Lerne, wie Vorgänge und Unteraufgaben zusammenpassen, unter [Mit Vorgängen arbeiten](/de/guide-issues.html).
