---
title: Zeit erfassen
description: Zeit an einem Vorgang erfassen, eigene Einträge korrigieren, den Stundenzettel lesen und Zeit direkt per Commit buchen.
---

# Zeit erfassen

Du erfasst eine Dauer an einem Vorgang. Daraus entstehen dein Stundenzettel, die Fokuszeit auf deinem Dashboard und die Aufwandszeile am Vorgang. Diese Seite beschreibt den Grundmodus. Nutzt deine Organisation das erweiterte Time-Tracking, lies auch [den letzten Abschnitt](#wenn-das-erweiterte-time-tracking-aktiv-ist).

## Zeit an einem Vorgang erfassen

1. Öffne den Vorgang und suche die Karte **Timeline**. Im breiten Fenster steht sie rechts unter Details, auf dem Handy weiter unten.
2. Tippe oben rechts auf der Karte auf **Zeit erfassen**.
3. Trag **Stunden** und **Minuten** ein, prüfe das **Datum** und drücke **Speichern**.

![Das Sheet „Zeit erfassen“](/assets/img/shot-time-log.png)
*Das Sheet „Zeit erfassen“ mit Dauer, Datum und optionaler Notiz.*

Pflicht ist nur die Dauer. **Notiz (optional)** füllst du, wenn du willst. Nach dem Speichern steigt der Aufwand am Vorgang und der Eintrag erscheint auf der Karte.

!!! tip "Dauer schnell eintippen"
    **Stunden** startet bei `1`, **Minuten** bei `0`. Für anderthalb Stunden tippst du `30` in **Minuten**. Für 20 Minuten setzt du **Stunden** auf `0` und **Minuten** auf `20`.

### Was du eingeben kannst

- Ein Eintrag dauert mindestens eine Minute und höchstens 24 Stunden.
- Du kannst bis zu ein Jahr zurückgehen. Zukünftige Tage gehen nicht. Pläne gehören in [Start- und Fälligkeitsdatum](/de/guide-timeline.html).
- Mehrere Einträge am selben Vorgang und Tag sind normal und addieren sich.

## Die Einträge an einem Vorgang

Jede Zeile zeigt Dauer und Datum. Darunter steht, wer erfasst hat, und die Notiz.

- An deinen eigenen Einträgen siehst du deinen Namen und deine Notiz.
- An Einträgen anderer steht **Anderes Mitglied** und keine Notiz. Die Projektleitung sieht Namen und Notizen im Projekt.
- **Alle Einträge (24)** unter der Liste öffnet die ganze Historie mit der bisherigen Summe. Weitere Zeilen laden beim Scrollen nach.

Einträge mit **Smart Commits (vor 2.0)** stammen aus alten Versionen. Sie gehören niemandem, zählen aber mit. Nur die Projektleitung kann sie entfernen.

## Einen Eintrag korrigieren oder löschen

Jeder Eintrag, den du ändern darfst, hat rechts ein Menü.

- **Bearbeiten** öffnet dasselbe Sheet mit den aktuellen Werten. Nach **Speichern** wird der Aufwand neu berechnet. Die Datumsregeln oben gelten weiter.
- **Löschen** fragt vorher nach und nennt Dauer und Tag. Das lässt sich nicht rückgängig machen, der Aufwand sinkt um genau diesen Betrag.

Wer was darf:

- **Eigene Einträge:** bearbeiten und löschen, immer.
- **Einträge anderer:** Die Projektleitung darf sie löschen, aber nicht bearbeiten. So steht unter einem Namen nie etwas, das die Person nicht selbst geschrieben hat. Bitte sie, neu zu erfassen. Jede solche Löschung landet im Audit-Protokoll.

!!! tip "Zu wenig erfasst?"
    Erfasse die fehlende Zeit als zweiten Eintrag. Bearbeiten ist für eine Dauer, die schlicht falsch ist.

## Schätzung und Aufwand

Die Karte **Timeline** zeigt eine Zeile wie `9h 30m von 10h aufgewendet`.

- Die erste Zahl ist die Summe aller Einträge am Vorgang, von allen.
- Die zweite ist die **Zeitschätzung** für die ganze Aufgabe.

Du siehst das auch auf der Karte im Board als kleinen Chip und in der [Timeline-Ansicht](/de/guide-timeline.html) als gefüllten Teil des Balkens.

Mit der erweiterten Zeiterfassung wird daraus ein **Honigstand**: eine Glasröhre, die sich mit Honig füllt. Ab dem Warnanteil des Projekts wird der Honig dunkler, ab 100 % wird er rot, und was darüber hinausgeht, steht als eigene kleine Kapsel daneben, zum Beispiel `+30 min`.

Beim Erfassen siehst du vor dem Speichern, was dein Eintrag mit der Schätzung und dem Projektbudget macht. Der Eintrag erscheint dann schraffiert hinter dem, was schon erfasst ist. Speichern geht immer: Ein Budget sperrt nie.

!!! note "Eine Schätzung ist kein Story Point"
    Story Points aus der Sprintplanung sind ein eigenes Feld. Ohne Zeitschätzung steht dort `9h 30m von — aufgewendet`. Deine Zeit zählt trotzdem überall.

## Der wöchentliche Stundenzettel

**Stundenzettel** findest du in der Seitenleiste, auf dem Handy unter **Mehr**.

![Der wöchentliche Stundenzettel](/assets/img/shot-timesheet.png)
*Eine Woche im Stundenzettel, eine Zeile je Person und Projekt.*

- Jede Zeile ist eine Person in einem Projekt. Die Spalten sind die Wochentage, dann **Gesamt**.
- Die Woche beginnt mit dem ersten Wochentag deiner Sprache: Montag auf Deutsch, Sonntag im US-Englisch.
- Die Pfeile springen eine Woche zurück oder vor. **Heute** bringt dich zur aktuellen Woche.
- Zeit an einem Vorgang, dessen Projekt es nicht mehr gibt, steht unter **Nicht zugeordnet**.
- Der Stundenzettel ist zum Lesen da. Erfasst wird am Vorgang.

### Filter

- Du siehst nur deine eigene Zeit. Der Server lehnt Anfragen nach fremden Stunden ab.
- Organisationsadmins sehen alle Zeilen und haben zwei durchsuchbare Filter: **Alle Nutzer** und **Alle Projekte**. Vorgangstitel und Projektnamen sehen sie nur bei Projekten, in denen sie Mitglied sind.

!!! note "Leer heißt nicht kaputt"
    „In dieser Woche wurden keine Arbeitszeiten erfasst.“ gilt nur für die angezeigte Woche. Geh zuerst mit dem linken Pfeil zurück.

## Zeit per Commit erfassen

Ist dein Projekt mit einem Git-Repository verbunden, erfasst eine Zeile in der Commit-Nachricht Zeit:

```text
MOB-42 #time 2h 30m
```

Das legt an `MOB-42` einen echten Eintrag an, genau wie einer, den du in der App eintippst.

- Dauern verstehen `w`, `d`, `h` und `m`. Ein Tag hat 8 Stunden, eine Woche 5 Tage, `1d 4h` sind also zwölf Stunden.
- Der Eintrag gehört **der Person, die den Commit geschrieben hat**, erkannt an der Autor-E-Mail. Die Notiz enthält den kurzen Commit-Hash und den Betreff.
- Er trägt den Tag, an dem der Commit entstand, in der Zeitzone dieser Person.
- Es gelten dieselben Regeln wie in der App. Ein Commit kann zum Beispiel nicht auf einen gesperrten Tag buchen.

!!! note "Die Commit-Zeit fehlt?"
    Die Autor-E-Mail muss zu einem aktiven Hinata-Konto passen, das Mitglied im Projekt ist. Sonst wird die Zeile übersprungen und keine Zeit erfasst. Prüf zuerst `git config user.email`. Das Repository verbindet die Projektleitung, siehe [Git-Integration](/de/git-integration.html).

## Wenn das erweiterte Time-Tracking aktiv ist

Deine Organisationsadmins können das erweiterte Modul einschalten. Dann ändert sich Folgendes:

- Aus **Stundenzettel** in der Seitenleiste wird **Zeiterfassung**, mit Liste, Kalender und Stundenzettel an einem Ort.
- **Zeit erfassen** am Vorgang öffnet den größeren Editor mit Beginn und Ende, Tags und abrechenbar.
- Du bekommst einen Timer, Freigaben für deinen Stundenzettel, Sperrdaten, Berichte und Exporte.
- Urlaub und Krankheit findest du in der Zeiterfassung unter **Abwesenheiten**.

Weiter geht es hier:

- [Erweitertes Time-Tracking](/de/time-tracking-advanced.html) für alles, was das Modul kann.
- [Abwesenheiten: Urlaub und Krankheit](/de/absences.html) für Urlaub, Krankheit und Salden.
- Für Admins: [einschalten und Regeln festlegen](/de/admin-time-tracking.html).
- [Zeiterfassung: Datenschutz & Recht](/de/time-tracking-privacy.html) dafür, wer was sehen darf.

## Nächste Schritte

- Setze die Daten, an denen Zeit gemessen wird, in der [Timeline](/de/guide-timeline.html).
- Sieh nach, was aus deinen Stunden wird, im [Dashboard und in den Berichten](/de/guide-reports.html).
