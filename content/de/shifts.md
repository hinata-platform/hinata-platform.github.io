---
title: Schichtplanung
description: Events mit Schichten planen, in die sich Leute eintragen. Ein eigenes Modul, das die Administration zuschaltet.
---

# Schichtplanung

Ein Messestand braucht drei Tage lang jeden Vormittag zwei Leute und jeden Nachmittag drei. Das Sommerfest eines Vereins braucht Hilfe an Theke, Grill und Kasse. Die Werkstatt einer Verwaltung muss jeden Samstag besetzt sein. Jedes Mal geht es um dieselbe Frage: Wer ist wann wo, und wo fehlt noch jemand?

Dafür gibt es die Schichtplanung. Ein Projekt plant **Events**, und ein Event hat **Schichten** mit Beginn, Ende und der Zahl der Leute, die gebraucht werden. Mitglieder tragen sich in freie Schichten ein, und die Planung sieht auf einen Blick, wo noch Plätze offen sind.

!!! info "Muss eingeschaltet sein"
    Die Schichtplanung ist ein eigenes Modul und auf einer frischen Instanz aus. Die Administration schaltet sie unter **Adminbereich → Plattform** ein. Solange sie aus ist, verhält sich Hinata genau wie bisher.

## Einschalten

Unter **Adminbereich → Plattform** steht der Schalter **Schichtplanung**. Er hat drei Stellungen: an, aus und leer. Leer heißt, dass die Umgebungsvariable `HINATA_SHIFTS_ENABLED` entscheidet, und die ist ab Werk `false`. Siehe [Konfigurationsreferenz](/de/configuration.html#schichtplanung).

Speichern genügt, ein Neustart ist nicht nötig. In der App erscheint danach in der Navigation unter **Plan** der Punkt **Schichten**, direkt nach der Zeiterfassung. Auf dem Telefon steht er im Blatt **Mehr**. Andere Geräte übernehmen die Änderung, sobald sie die Einstellungen des Servers neu lesen, spätestens beim nächsten Start der App.

Wird das Modul wieder ausgeschaltet, verschwindet der Punkt. Ein Link auf eine Schichtseite führt dann auf die Seite „Nicht gefunden“, und der Server beantwortet alle Anfragen an das Modul mit 404. Gespeicherte Daten bleiben dabei erhalten.

## Voraussetzung: ein Replica Set

Wer sich in eine Schicht einträgt, bekommt einen Platz. Den letzten Platz bekommt genau eine Person, auch wenn zwei im selben Moment tippen, und dieselbe Person kann nicht zur selben Zeit an zwei Orten eingetragen sein. Beides sichert der Server mit Transaktionen in MongoDB ab, und Transaktionen gibt es nur in einem **Replica Set**.

- Die Produktion aus [Deployment](/de/deployment.html) läuft als Replica Set mit eingeschalteten Transaktionen (`HINATA_MONGO_TRANSACTIONS`, im Profil `prod` ab Werk `true`). Dort ist nichts weiter zu tun.
- Läuft dein Server mit einer einzelnen MongoDB ohne Replica Set, bleibt die Schichtplanung aus, ganz gleich, was der Schalter oder die Umgebung sagt. Der Server schreibt beim Start eine Warnung mit dem Grund ins Log, und im Adminbereich steht statt des Schalters der Hinweis **Braucht ein MongoDB Replica Set**.

Wie du ein Replica Set aufsetzt, steht unter [MongoDB & X.509](/de/database.html).

## Für Helfer

Unter **Schichten** gibt es drei Ansichten: **Meine**, **Kalender** und **Events**. Auf dem Telefon wechselst du sie über die Pille unter dem Titel, auf einem breiten Fenster stehen alle drei nebeneinander im Kopf der Seite.

### Meine Schichten

Ganz oben steht deine **nächste Schicht** als eigene Karte: Tag und Uhrzeit groß, wie lange es noch dauert, bis wann sie geht, wo sie stattfindet und mit wem du sie hast. Darunter folgen deine weiteren Schichten, nach Tagen sortiert. Am Ende zeigt die Seite bis zu drei **offene Schichten in deinen Projekten** aus den nächsten zwei Wochen, in denen noch Leute fehlen, und einen Weg zu allen Events.

Jede Schicht zeigt ihre Besetzung als kleine Wabe mit einer Zahl daneben, etwa `2 / 3`. Ein Dreieck heißt, dass noch jemand fehlt, ein Haken, dass genug Leute da sind, ein Schloss, dass die Schicht voll ist. Hat eine Schicht eine Obergrenze, die vom Soll abweicht, steht sie dabei: `4 / 3 · max. 5`. Ein Screenreader liest das als ganzen Satz vor, zum Beispiel „Besetzung 2 von 3, es fehlt noch 1 Person“.

Hast du gerade keine Verbindung, zeigt die Seite den Stand vom letzten Laden. Gespeichert werden dafür nur deine eigenen Schichten mit Zeiten, Titeln und Zahlen, keine Namen anderer Leute. Beim Abmelden und wenn die Administration das Modul ausschaltet, wird das wieder gelöscht.

### Eintragen

Unter **Events** siehst du die Events aller Projekte, in denen du Mitglied bist, oder über die Projekt-Pille nur eines. Jedes Event zeigt, wie viele Plätze besetzt sind und wie viele Schichten noch Leute brauchen. Ein Tipp öffnet das Event mit seinen Schichten, nach Tagen sortiert. Der Filter **Nur unterbesetzt** blendet alles aus, was schon besetzt ist.

Bei einer freien Schicht steht **Eintragen**. Ein Tipp genügt, du bist dann sofort bestätigt. Eine volle Schicht sagt das in Worten, etwa „Voll, 5 von 5“, statt eines grauen Knopfs. Steht im Kopf des Events „Nur die Orga teilt zu“, trägt dort niemand sich selbst ein; die Planung teilt die Leute zu.

Tippst du auf eine Schicht, öffnet sich ihr Blatt: Zeit und Dauer, Ort, wer schon eingetragen ist und wie viele Plätze frei sind. Dort findest du auch den Weg zum Event.

Hast du zur selben Zeit schon eine andere Schicht, lehnt Hinata das Eintragen ab und sagt dir warum. Bist du an dem Tag als abwesend eingetragen, klappt das Eintragen trotzdem, aber Hinata weist dich darauf hin.

### Bestätigen und Ablehnen

Teilt dich die Planung einer Schicht zu, steht sie mit **Zugeteilt** in deiner Liste und wartet auf deine Antwort. **Bestätigen** sagt zu. **Ablehnen** (im Blatt oder auf der Karte der nächsten Schicht) gibt den Platz wieder frei, damit die Planung jemand anderen einteilen kann.

### Abgeben

Kannst du eine bestätigte Schicht doch nicht übernehmen, öffne sie und wähle **Abgeben**. Hinata fragt einmal nach, dann ist dein Platz wieder frei und andere können sich eintragen. Später kannst du dich erneut eintragen, solange noch Platz ist.

### Zeiten und Zeitzonen

Jedes Event hat eine eigene Zeitzone. Hinata zeigt die Zeiten so, wie sie vor Ort gelten. Steht dein Gerät auf einer anderen Zeitzone, steht bei der Schicht ein Hinweis wie „Zeiten in Europe/Berlin“.

## Der Kalender

Die Ansicht **Kalender** zeigt alle Schichten deiner Projekte. Auf einem breiten Fenster ist das eine Woche mit Stunden, auf dem Telefon ein Tag mit der Wochenleiste darüber. Über **Monat** (auf dem Telefon im Menü neben **Heute**) siehst du einen ganzen Monat, in dem jeder Tag nur zeigt, dass etwas ist: ein gefüllter Punkt für eine eigene Schicht, ein Ring für eine Schicht, die noch Leute braucht. Ein Tipp auf einen Tag öffnet ihn.

Jede Schicht trägt die Farbe ihres Projekts. Deine eigenen Schichten haben einen Haken, Schichten mit freien Plätzen ein Dreieck und im Titel, wie viele fehlen, etwa „Aufbau · fehlt 1“. Eine eigene Schicht, in der noch jemand fehlt, zeigt beides. Mit **Alle Projekte** grenzt du den Kalender auf ein Projekt ein, mit **Nur unterbesetzt** auf die Schichten, in denen noch jemand fehlt. Beides gilt für Woche, Tag und Monat, und die Adresse merkt sich Projekt, Ansicht und Tag.

Der Kalender zeigt alle Zeiten in deiner eigenen Zeitzone. Hat ein Event eine andere, steht darüber „Zeiten in deiner Zone“. Das Event und das Blatt einer Schicht zeigen die Zeiten vor Ort.

## Für die Orga

Planen dürfen die Leitung des Projekts, die Admins seiner Teams und alle, die in den Projekteinstellungen unter **Schichtplanung** als Planer eingetragen sind. Wer plant, sieht in den Ansichten zusätzliche Knöpfe; alle anderen sehen sie nicht.

### Ein Event anlegen

Unter **Events** legt **Event** ein neues an. Du wählst das Projekt (ist die Liste auf ein Projekt eingegrenzt, steht es schon fest), gibst einen Namen, Beginn, Ende und den Ort an. Unter **Weitere Angaben** stehen die Zeitzone, ob sich Mitglieder selbst eintragen dürfen, und eine Beschreibung. Ein Event dauert höchstens 14 Tage.

Die Zeitzone ist die deines Geräts, solange du keine andere wählst. Beginn und Ende gelten in der gewählten Zone. Wechselst du sie später, bleiben die Uhrzeiten stehen: Aus 18:00 in Berlin wird 18:00 in New York. Hat das Event schon Schichten, nennt Hinata vor dem Speichern, wann das Event dann auf deiner Uhr beginnt, und die Schichten behalten ihre Uhrzeiten mit.

Über **Mehr** im Event bearbeitest du es, sagst es ab oder löschst es. Eine Absage sagt alle Schichten ab und gibt allen Eingetragenen Bescheid; die Einträge bleiben sichtbar. Löschen geht erst, wenn niemand mehr eingetragen ist, also nach einer Absage. Verschiebst du ein Event und haben dadurch Leute zwei Schichten zur selben Zeit, sagt Hinata dir, wie viele.

### Schichten anlegen

Im Event legt **Schicht** eine neue an: eine Bezeichnung wie „Aufbau“ oder „Kasse“, der Tag und die Uhrzeiten. Endet eine Schicht vor ihrem Beginn, geht sie über Mitternacht in den nächsten Tag. Eine Schicht liegt immer innerhalb ihres Events und dauert höchstens 24 Stunden.

Unter **Wie viele Leute?** stehen zwei Zahlen:

- **Gebraucht** ist das Soll, mindestens 1. Solange weniger Leute eingetragen sind, gilt die Schicht als unterbesetzt.
- **Obergrenze** ist, wie viele höchstens kommen dürfen. Ohne Obergrenze ist jede Hilfe willkommen. Die Obergrenze liegt nie unter dem Soll. Senkst du sie bei einer Schicht, in der schon mehr Leute stehen, lehnt Hinata das ab und nennt die Zahl; nimm dann erst jemanden heraus.

### Auf weitere Tage übernehmen

Dauert ein Event mehrere Tage, öffnet **Auf weitere Tage übernehmen** eine Reihe von Tagen. Wähle die Tage, an denen dieselbe Schicht zur selben Uhrzeit stattfinden soll. Beim Speichern legt Hinata sie an allen gewählten Tagen an oder an keinem. Passt sie an einem Tag nicht, etwa weil das Event an diesem Tag früher endet, markiert Hinata genau diesen Tag und sagt, warum.

### Zuteilen und herausnehmen

Bei jeder Schicht steht im Event **Zuteilen**. Es öffnet die Mitglieder des Projekts mit Suche, ganz oben **Mich eintragen**; wer schon auf der Schicht steht, ist ausgegraut. Zugeteilte Personen bekommen Bescheid und bestätigen oder lehnen ab. Ist jemand an dem Tag als abwesend eingetragen und darfst du das sehen, weist Hinata darauf hin.

Im Blatt einer Schicht nimmst du Leute mit dem kleinen Kreuz neben ihrem Namen wieder heraus, bearbeitest die Schicht oder löschst sie.

### Verschieben

Im Kalender kannst du eine Schicht deines Projekts an eine andere Stelle ziehen. Hinata fragt einmal nach, bevor es sie verschiebt; bei einem Termin einer Serie ist das die Frage, ob nur dieser oder alle künftigen gemeint sind. Dieselbe Änderung geht immer auch über **Von** und **Bis** im Editor, ganz ohne Ziehen. Neue Schichten legst du im Editor an, nicht durch Ziehen im Kalender.

### Serien

Ein Bereitschaftsdienst jede Woche, eine Sprechstunde einmal im Monat, der Thekendienst jeden Freitag: Solche Events legst du einmal an, und Hinata wiederholt sie als Serie. Im Event-Editor steht dafür die Zeile **Wiederholen**, anfangs auf **Nie**. Ein Tipp öffnet die Auswahl:

- **Täglich**
- **Wöchentlich** am Wochentag des Beginns
- **Monatlich** am Tag des Beginns, etwa am 15.
- **Eigene Regel**: wöchentlich an mehreren Tagen, ein Abstand wie alle zwei Wochen und ein Ende nach einer Anzahl oder an einem Datum

Sobald eine Regel gewählt ist, stehen im Kopf des Editors die Regel in Worten und darunter die nächsten Termine. So siehst du vor dem Speichern, was entsteht. Ohne Ende läuft die Serie weiter.

Jeder Termin einer Serie ist ein ganz normales Event mit eigenen Schichten. Eintragen, Zuteilen, Erinnern, der Kalender und das Kalender-Abo funktionieren wie bei jedem anderen Event. Hinata legt die Termine der nächsten drei Monate an, höchstens 52 auf einmal, und zieht jede Nacht nach. Karten und Kopf eines Termins zeigen die Regel mit einem Wiederholungssymbol.

Ein Event über mehrere zusammenhängende Tage, etwa eine Messewoche, ist keine Serie. Dafür gibt es **Auf weitere Tage übernehmen**.

**Nur dieses oder alle künftigen.** Änderst du einen Termin einer Serie, sagst ihn ab, löschst ihn oder änderst, legst an oder löschst eine seiner Schichten, fragt Hinata, wofür das gelten soll. Vorausgewählt ist nichts.

- **Nur dieses** ändert nur diesen Termin. Er folgt danach nicht mehr der Serie und zeigt „abweichend von der Serie“. Sagst du ihn ab oder löschst ihn, entsteht an diesem Tag auch später kein neuer.
- **Alle künftigen** gilt für diesen Termin und alle folgenden. Vergangene Termine bleiben, wie sie sind. Wer auf einer Schicht eingetragen ist, bleibt es und bekommt Bescheid, wenn sich seine Schicht ändert. Haben dadurch Leute zwei Schichten zur selben Zeit, nennt Hinata, wie viele.

Eine neue Regel gilt immer ab dem Termin, an dem du sie änderst. Eine Schicht, die du gleich an mehreren Tagen anlegst, geht nur in diesen Termin. Eine Schicht für alle künftigen Termine zu löschen geht erst, wenn in keinem künftigen Termin mehr jemand darauf eingetragen ist.

**Eine Serie beenden.** Lösche einen Termin mit **Alle künftigen**. Ab diesem Tag gibt es die Serie nicht mehr: Termine ohne Eintragungen verschwinden, Termine mit Eintragungen werden abgesagt, und die Eingetragenen bekommen Bescheid. Mit **Absagen** und **Alle künftigen** bleiben alle folgenden Termine sichtbar, aber abgesagt.

## Schichten im eigenen Kalender

Deine Schichten können auch in deinem Kalender auf dem Telefon oder am Rechner stehen, in Apple Kalender, Google Kalender oder Outlook. Unter **Einstellungen → Benachrichtigungen → Schichten im eigenen Kalender** erzeugt **Abo-Adresse erzeugen** eine private Adresse, die dein Kalender abonniert.

- Die Adresse wird **nur einmal** angezeigt. Kopiere sie oder öffne sie mit **In Kalender öffnen** direkt in deiner Kalender-App. Hinata speichert sie auf dem Gerät nicht.
- Danach zeigt der Abschnitt nur noch, seit wann das Abo läuft und wann ein Kalender es zuletzt abgerufen hat.
- **Neu erzeugen** macht eine neue Adresse; bestehende Abos funktionieren dann nicht mehr. **Entfernen** beendet das Abo; die Schichten verschwinden beim nächsten Abruf aus deinem Kalender.
- Das Abo enthält deine eigenen Schichten von 30 Tagen zurück bis 180 Tage voraus. Abgesagte Events stehen als abgesagt darin.

!!! warning "Datenschutz"
    Das Abo ist eine Übermittlung an den Kalenderanbieter, den du wählst. Bei Google und Microsoft ruft deren Server die Adresse ab und speichert deine Schichten dort. Wer die Adresse kennt, sieht deine Schichten; gib sie nicht weiter und erzeuge eine neue, wenn sie in falsche Hände geraten ist.

### Benachrichtigungen

Unter **Einstellungen → Benachrichtigungen** steht die Zeile **Schichten**. Dort schaltest du E-Mail und Push für Zuteilungen, Änderungen, Absagen und die Erinnerung vor Schichtbeginn ein oder aus. Ein Tipp auf eine solche Benachrichtigung öffnet das Event oder deine Schichten.

## Was die Schichtplanung ist

- **Events in einem Projekt.** Ein Event hat einen Ort, einen Zeitraum und eine eigene Zeitzone. Sehen können es die Mitglieder des Projekts, sonst niemand.
- **Schichten mit Soll und Obergrenze.** Jede Schicht sagt, wie viele Leute sie braucht, und wahlweise, wie viele höchstens kommen dürfen. Mehrere Leute in einer Schicht sind der Regelfall, nicht die Ausnahme.
- **Eintragen statt Listen herumschicken.** Wer mithilft, trägt sich selbst in eine freie Schicht ein. Die Planung kann Leute auch direkt zuteilen.
- **Konflikte, bevor sie passieren.** Überschneiden sich zwei Schichten derselben Person, lehnt der Server die zweite ab.
- **Für jede Organisation.** Ein Unternehmen auf einer Messe, ein Verein beim Sommerfest, eine Verwaltung mit Bereitschaftsdiensten, ein Veranstalter mit vielen Helfern: Das Modul kennt nur Events, Schichten und Menschen.

## Was sie nicht ist

- **Keine Zeiterfassung.** Eine Schicht erfasst keine Arbeitszeit, und das Modul hängt nicht an der [erweiterten Zeiterfassung](/de/time-tracking-advanced.html). Ehrenamtliche oder externe Helfer brauchen kein Stundenkonto, um sich einzutragen.
- **Keine Vorgänge.** Schichten erscheinen nicht auf Boards, in Sprints oder in den Berichten über Vorgänge, und sie zählen nicht als Issues.
- **Kein automatischer Dienstplan.** Hinata verteilt keine Leute von selbst und kennt keine Qualifikationen je Schicht. Einen Tausch zwischen zwei Personen gibt es nicht als eigenen Schritt: Die eine gibt ihre Schicht ab, die andere trägt sich ein.
- **Kein Abgleich in beide Richtungen.** Mit Google oder Microsoft wird nichts synchronisiert, und Termine aus fremden Kalendern werden nicht zu Schichten.

## Wenn etwas nicht geht

**Statt des Schalters steht da „Braucht ein MongoDB Replica Set“.** Der Server läuft ohne Transaktionen. Richte ein Replica Set ein und setze `HINATA_MONGO_TRANSACTIONS=true`, danach den Server neu starten.

**Der Schalter ist an, aber in der App fehlt „Schichten“.** Die App hat die Einstellungen des Servers noch nicht neu gelesen. Schließe sie und öffne sie wieder.

**Ein Link auf eine Schicht zeigt „Nicht gefunden“.** Das Modul ist auf diesem Server aus, oder der Link gehört zu einem anderen Server.
