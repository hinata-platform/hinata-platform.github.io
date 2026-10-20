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
