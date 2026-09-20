---
title: Projektvorlagen
description: Ein Projekt kopieren, eines als Vorlage behalten und Fristen als Versatz zum Termin pflegen, statt jedes Datum von Hand zu setzen.
---

# Projektvorlagen

Manche Projekte wiederholen sich. Die Erstiwoche, die Mensaparty, der Aktionstag im Sommer: jedes Mal dieselbe Kette aus Raum buchen, Geld beantragen, Plakate drucken, ankündigen, abrechnen. Nur der Termin ist ein anderer.

Dafür gibt es drei Dinge, die zusammengehören: ein **Termin am Projekt**, **Fristen als Versatz** zu diesem Termin, und das **Kopieren** eines ganzen Projekts.

!!! info "Muss eingeschaltet sein"
    Projektvorlagen sind ein eigenes Modul und auf einer frischen Instanz aus. Die Administration schaltet sie unter **Adminbereich → Plattform** ein; siehe [Konfigurationsreferenz](/de/configuration.html). Solange sie aus sind, verhalten sich Projekte genau wie bisher.

## Der Termin am Projekt

Jedes Projekt kann einen **Termin** tragen: den Tag der Veranstaltung, des Aktionstags, der Party. Du setzt ihn in den Projekteinstellungen unter „Vorlagen und Termin“.

Der Termin macht für sich genommen nichts. Er ist der Tag, von dem aus gerechnet wird.

![Projekttermin, Vorlagen-Kennzeichen und Kopieren in den Projekteinstellungen](/assets/img/shot-project-templates-card.png)
*Alles, was das Modul einem Projekt hinzufügt, steht in einer Karte: der Termin, das Kennzeichen und der Weg zur Kopie.*

## Fristen als Versatz

Eine Frist lässt sich weiterhin als festes Datum setzen. Neu ist die zweite Betriebsart: **„Zum Termin“**. Du gibst eine Zahl an, eine Einheit und eine Richtung, und daneben steht sofort das Datum, das dabei herauskommt.

```
Frist   ( ) Datum      [ 14.10.2026 ]
        (•) Zum Termin [ 4 ] [ Wochen ] [ vorher ]  ->  15.10.2026
```

![Eine Frist als Versatz zum Projekttermin](/assets/img/shot-issue-deadline-offset.png)
*Eine Zahl, eine Einheit und eine Richtung — und darunter der Tag, der dabei herauskommt.*

Zwei Dinge dazu sind wichtig:

- **Das Datum wird trotzdem geschrieben.** Board, Zeitachse, Berichte, die Erinnerungsmail und die App lesen weiterhin ein Datum. Der Versatz ist die Regel, das Datum ihr Ergebnis.
- **Ein Datum von Hand gewinnt.** Wer eine Frist direkt auf einen Tag setzt, löst den Versatz ab. Das steht vorher da, und die nächste Terminverschiebung lässt diese Frist dann in Ruhe.

### Kalendertage oder Werktage

Vorausgewählt sind Kalendertage: „28 Tage vorher“ sind 28 Tage, Wochenende eingeschlossen. Wer stattdessen Werktage braucht, stellt das an genau dieser Frist um.

!!! info "Werktage brauchen einen Feiertagskalender"
    Werktage überspringen immer Wochenenden. Feiertage überspringen sie nur, wenn am Projekt ein Feiertagskalender gewählt ist. Ohne ihn zählt ein Feiertag wie ein gewöhnlicher Arbeitstag. Die Kalender pflegt die Administration im Adminbereich.

## Den Termin verschieben

Die Veranstaltung wird verlegt. Du änderst den Termin in den Projekteinstellungen, und bevor etwas geschrieben wird, zeigt ein Blatt, was passieren würde:

- welche Fristen mitziehen, mit altem und neuem Datum
- wie viele es insgesamt sind
- wie viele **stehen bleiben**, weil jemand sie von Hand gesetzt hat

![Das Blatt zeigt, welche Fristen einem neuen Projekttermin folgen würden](/assets/img/shot-project-schedule-move.png)
*Bevor etwas geschrieben wird: der alte Tag, der neue, wie weit es geht, und jede Frist, die mitzieht.*

Erst „Verschieben“ schreibt. Abbrechen ändert nichts.

Wird der Termin gelöscht, bleiben die Fristen stehen, wo sie sind, und behalten ihren Versatz. Es geht nichts verloren.

## Ein Projekt kopieren

Auf einer Projektkarte am Rechner oder in den Projekteinstellungen: **Projekt kopieren**. Auf dem Telefon führt der Weg über die Projekteinstellungen. Du gibst Namen, Kürzel und wahlweise einen Termin an und wählst, was mitkommt.

![Das Kopier-Blatt mit den Schaltern und den Zahlen des Servers](/assets/img/shot-project-copy.png)
*Die Zahlen unter den Schaltern kommen vom Server: wie viele Vorgänge, wie viele Dateien, wie viel.*

### Was mitkommt

| Bereich | Inhalt |
| --- | --- |
| Projekt | Beschreibung, Farbe, Bild, Workflow-Spalten, Stichwörter, erledigte Status |
| Vorgänge | Titel, Beschreibung, Typ, Priorität, Stichwörter, Schätzung, Story Points, Reihenfolge, **Unteraufgaben in voller Tiefe**, Abhängigkeiten und Verknüpfungen **innerhalb** des Projekts, die Versätze |
| Wahlweise | Mitglieder und Leitung, Anhänge, Zeit-Einstellungen, das Board mit seinen Spalten |

### Was nie mitkommt

Kommentare, der Aktivitätsverlauf, erfasste Zeiten, Beobachter, die Meldenden, der Status (die Kopie startet im ersten Workflow-Status), Sprints, die Git-Verbindung und der Mail-Eingang.

Das ist keine Sparsamkeit, sondern die Trennung von Plan und Geschichte: Eine Kopie erbt den Plan. Die Git-Verbindung bleibt zurück, weil sie einen verschlüsselten Zugriffsschlüssel und einen Webhook trägt, die zu genau einem Projekt gehören.

### Grenzen

- Höchstens 500 Vorgänge je Kopie. Darüber lehnt der Server ab und nennt die tatsächliche Zahl, statt ein halbes Projekt anzulegen.
- Anhänge höchstens 50 Dateien und 100 MB.
- Geht unterwegs etwas schief, wird alles wieder abgeräumt. Ein halbes Projekt ist schlimmer als kein Projekt.

## Eine Vorlage behalten

Ein Projekt, das nur als Bauplan existiert, wird als **Vorlage** gekennzeichnet. Dafür gibt es zwei Wege, und sie beantworten zwei verschiedene Fragen:

- **Das Projekt gibt es schon und es *ist* der Bauplan.** Schalte in seinen Einstellungen „Als Vorlage anbieten“ ein. Das Projekt wandert aus der laufenden Liste zu den Vorlagen; sonst ändert sich nichts daran.
- **Du willst einen Bauplan *von* einem Projekt, das weiterläuft.** Öffne den Tab **Vorlagen** und drücke auf das Plus. Du wirst gefragt, aus welchem Projekt die Vorlage entstehen soll, und bekommst eine Kopie — das gewählte Projekt bleibt unangetastet.

So oder so steht das Ergebnis unter „Vorlagen“ statt zwischen den laufenden Projekten und bietet als erste Aktion **„Projekt anlegen“**.

![Der Tab „Vorlagen“ in der Projektübersicht](/assets/img/shot-project-templates.png)
*Eine Vorlage ist ein gewöhnliches Projekt, das woanders steht — und hier steht es.*

Sonst ändert sich nichts: gleiche Rechte, gleiche Suche, gleiche Boards.

„Projekt anlegen“ fragt Name, Kürzel und Termin und erledigt Kopieren und Rechnen in einem Schritt. Der Umfang ist dabei vorbelegt — Struktur, Vorgänge, Mitglieder und Zeit-Einstellungen ja, Anhänge und Board nein. Wer es anders will, nimmt den Kopierweg.

![Ein Projekt aus einer Vorlage anlegen](/assets/img/shot-project-instantiate.png)
*Aus einer Vorlage bleiben nur drei Angaben: Name, Kürzel und der Termin, von dem alles gerechnet wird.*

Eine Vorlage trägt üblicherweise gar keinen Termin: Ihre Vorgänge halten nur Versätze. Das Anlegen ist der Moment, in dem daraus Daten werden.

## Über MCP

Mit eingeschaltetem Modul kennt der [MCP-Server](/de/mcp.html) zwei zusätzliche Werkzeuge:

- `copy_project` — ein Projekt kopieren, mit Name, optionalem Kürzel, optionalem Termin und den Umfangsschaltern. Braucht den Scope `projects:write`.
- `set_issue_deadline` — die Frist eines Vorgangs als Versatz setzen oder wieder entfernen. Braucht `issues:write`.

## Wenn etwas nicht geht

**Neben der Frist steht „Projekt hat noch keinen Termin“.** Der Versatz ist gespeichert und bleibt es. Es fehlt nur der Tag, von dem aus gerechnet wird; setze ihn in den Projekteinstellungen.

**Die Kopie hat andere Daten als das Original.** So soll es sein: Fristen mit Versatz werden am Termin der Kopie neu gerechnet. Feste Daten kommen unverändert mit.

**Eine Frist ist beim Verschieben nicht mitgezogen.** Dann trägt sie keinen Versatz mehr — jemand hat sie von Hand gesetzt. Stelle sie im Fristfeld wieder auf „Zum Termin“.

**Werktage ergeben ein anderes Datum als erwartet.** Prüfe, ob am Projekt ein Feiertagskalender gewählt ist. Ohne ihn zählen Feiertage als Arbeitstage.
