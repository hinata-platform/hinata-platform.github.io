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

Wenn deine Administration die erweiterte Zeiterfassung eingeschaltet hat, findest du in deinen **Einstellungen** den Abschnitt **Arbeitszeiten** und in der Zeiterfassung die Ansicht **Abwesenheiten**. Beides ist Planung. Du kannst an jedem Tag Zeit erfassen, auch an Feiertagen und an Tagen, an denen du nicht da bist.

- **Geplante Stunden** sind deine Stunden je Wochentag. Solange du keine eigenen festlegst, gilt die Vorgabe des Servers. Eine Änderung gilt ab dem Datum, das du wählst, frühere Wochen behalten ihre Stunden. Hier wählst du auch den Feiertagskalender, nach dem du dich richtest.
- **Abwesenheiten** sind Urlaub, Krankmeldungen oder Sonstiges, für einen einzelnen Tag oder einen Zeitraum. Ein einzelner Tag kann ein halber Tag sein. Die Notiz ist freiwillig, sehen können sie nur du und die Abwesenheitsverwaltung. Du findest und pflegst sie in der Zeiterfassung unter **Abwesenheiten**.
- **Feiertage** kommen aus den Kalendern, die deine Administration im Adminbereich unter **Feiertage** pflegt. Sie trägt Tage von Hand ein oder importiert ein Jahr aus einer Kalenderadresse.

Was sich dadurch zeigt:

- Eintragsliste und Kalender markieren Feiertage, Abwesenheiten und Tage ohne geplante Stunden. Die Markierung ist bewusst zurückhaltend, denn sie ist keine Sperre. Ein Tag, der sich wirklich nicht mehr ändern lässt, trägt ein Schloss.
- Dein eigener Stundenzettel zeigt **Deine Kapazität**: deine geplanten Stunden im Zeitraum, abzüglich Feiertage und Abwesenheiten, neben dem, was du gebucht hast. Nur du siehst das.
- Mit eingeschalteten Arbeitszeithinweisen bekommt ein Eintrag an einem Feiertag einen Hinweis, genau wie ein Eintrag an einem Sonntag.

## Abwesenheiten in der Zeiterfassung

Deine Abwesenheiten stehen dort, wo auch deine Stunden stehen: in der Zeiterfassung, neben Liste, Kalender und Stundenzettel. Die Ansicht **Abwesenheiten** hat vier Bereiche.

- **Meine** ist die Liste deiner Tage, mit einer Suche über die Notizen, einem Zeitraum, einer Art und der Reihenfolge. Was noch auf eine Entscheidung wartet, steht oben.
- **Anträge** sind deine eigenen Anträge mit dem, was daraus wurde.
- **Zu entscheiden** ist der Posteingang für alle, die entscheiden.
- **Konten** zeigt dir, was dir in diesem Jahr zusteht, und das Journal dahinter.

Eintragen kannst du von überall in der Zeiterfassung: im Kopf über **Abwesenheit beantragen** oder den Pfeil neben **Neuer Eintrag**, auf dem Telefon über das **+**, und im Kalender über das Tagesmenü — langer Druck oder Rechtsklick auf einen Tag. Das Formular startet dann auf dem Tag, den du angefasst hast.

Ein Tipp auf eine Abwesenheit, ein Band im Kalender oder eine Markierung in Liste und Stundenzettel öffnet dasselbe Blatt. Es zeigt, woher die Abwesenheit kommt, und bietet genau das an, was noch geht: bearbeiten und löschen bei einer eingetragenen, zurückziehen und bearbeiten bei einem offenen Antrag, stornieren bei einem genehmigten, und einen neuen Antrag nach einer Ablehnung.

## Abwesenheitskonten

Hat deine Administration zusätzlich die **Abwesenheitsverwaltung** eingeschaltet, steht unter **Abwesenheiten** auf der Pille **Konten**, was dir in diesem Jahr zusteht.

- **Konten** zeigen je Abwesenheitsart, was dir zusteht, was du genommen hast, was geplant ist und was bleibt. Eine Art ohne Kontingent, zum Beispiel Krankmeldungen, zeigt statt einer Zahl, was in diesem Jahr darauf entfallen ist: Entgeltfortzahlung ist kein Anspruch in Tagen.
- **Journal** listet jede Bewegung eines Kontos, mit dem Tag, an dem sie wirkt, und der Begründung, wenn es eine gab. Dein Konto entsteht aus dieser Liste, nicht aus einer gespeicherten Zahl, und deshalb lässt sich jede Zahl darauf zurückführen.
- Die Tage selbst stehen auf der Pille **Meine**, vergangene wie kommende.

Sehen kann das nur, wen es angeht: du selbst und die Personen, die deine Organisation als Abwesenheitsverwaltung benannt hat.

!!! info "Eine Zahl, die noch nicht da ist"
    Steht bei einer Art **Noch nicht zugeteilt**, ist für dieses Jahr noch kein Anspruch eingetragen. Das ist kein Fehler und keine Aussage über deinen Vertrag, sondern heißt nur: Die Verwaltung hat das Jahr noch nicht zugeteilt.

## Abwesenheit beantragen

Sagt eine Abwesenheitsart, dass sie genehmigt werden muss, wird sie beantragt statt eingetragen. **Abwesenheit beantragen** steht im Kopf der Abwesenheiten und in jedem Menü, das die Zeiterfassung zum Hinzufügen anbietet.

Im Formular wählst du die Art, den Zeitraum und, wenn die Art es erlaubt, ob der erste oder der letzte Tag ein halber ist. Während du die Daten wählst, rechnet der Server mit und sagt dir, was die Spanne kostet: wie viele Arbeitstage darin liegen, wie viele Feiertage sie geschluckt hat und was dir danach bleibt. Wochenenden, Feiertage und Tage, an denen du laut deinem Muster nicht arbeitest, kosten nichts — ein Feiertag, der in den Urlaub fiel, war nie Urlaub.

Zwei Felder sind freiwillig. Die **Notiz** liest, wer entscheidet. Eine **Vertretung** wird informiert und muss nichts bestätigen: Dein Urlaub soll nicht an der Aufmerksamkeit einer anderen Person hängen.

Was beim Einreichen berechnet wurde, wird eingefroren. Wechselst du später von fünf auf vier Tage die Woche, deutet das einen entschiedenen Antrag nicht um — in keine Richtung.

!!! info "Beantragte Tage sieht man, bevor sie entschieden sind"
    Ein Tag, den du beantragt hast, ist in Kalender und Stundenzettel schraffiert und trägt eine Sanduhr. Das ist bewusst weder die stille Fläche einer eingetragenen Abwesenheit noch das Schloss eines gesperrten Tages: Der Tag ist beansprucht, nicht geschlossen, und Zeit lässt sich darauf weiterhin erfassen.

## Krank melden

Krankheit wird gemeldet, nicht beantragt. **Krank melden** verlangt nur den Zeitraum, ist sofort wirksam und geht auch rückwirkend. Es gibt keine genehmigende Person, kein Pflichtfeld und keinen Weg, auf dem der Server eine Krankmeldung ablehnen könnte.

Einen Nachweis lädst du hier nicht hoch, und das ist Absicht: Seit 2023 holt der Arbeitgeber die Arbeitsunfähigkeitsbescheinigung bei der Krankenkasse ab (§ 109 SGB IV). Eine Gesundheitsangabe in einem Projektwerkzeug wäre ein besonders geschütztes Datum, das dort nichts zu suchen hat. Deinem Arbeitgeber musst du die Krankheit weiterhin selbst melden (§ 5 EFZG); hinata ist diese Meldung nicht.

Fällt die Krankheit auf Tage, die du schon als Urlaub genehmigt bekommen hast, gehen diese Tage von selbst auf dein Konto zurück und der Urlaub wird gekürzt (§ 9 BUrlG). Wer den Urlaub entschieden hat, erfährt die Kürzung als Tatsache, nie ihren Grund.

## Anträge und Posteingang

Unter **Anträge** stehen deine Anträge mit dem, was daraus wurde: offen, genehmigt, abgelehnt, zurückgezogen oder storniert. Solange niemand entschieden hat, kannst du einen Antrag **zurückziehen** oder **bearbeiten**: Zeitraum, halbe Tage, Notiz und Vertretung lassen sich ändern, und die Tage werden neu gerechnet. Wechselst du dabei die Art, geht der Antrag an die Personen, die für die neue Art entscheiden, und die alten erfahren, dass er sie nicht mehr betrifft. Ist er genehmigt und liegt noch ganz in der Zukunft, kannst du ihn selbst **stornieren** — die Tage gehen zurück, und wer entschieden hat, wird informiert. Hat die Abwesenheit schon begonnen, übernimmt das die Abwesenheitsverwaltung, weil es dann kein Plan mehr ist, sondern eine Aufzeichnung.

**Zu entscheiden** ist der Posteingang. Er ist leer für alle, die nichts zu entscheiden haben, und das ist eine ehrliche Antwort, kein verstecktes Feature. Jede Karte nennt die Person, den Zeitraum, die Tagesmenge und, wo es zutrifft, drei Hinweise: dass der Saldo nicht reicht, dass die Frist kürzer ist als die Art verlangt, und wie viele andere im selben Zeitraum abwesend sind. Wie viele Urlaubstage jemand noch hat, steht dort nicht — die Antwort ist ein Ja oder Nein, keine Zahl.

**Eine Ablehnung braucht eine Begründung.** § 7 Abs. 1 BUrlG lässt eine Ablehnung nur wegen dringender betrieblicher Belange oder vorrangiger Wünsche anderer zu, und eine Ablehnung, die keines von beidem nennt, kann niemand prüfen. Die Begründung erreicht die antragstellende Person und steht in der Historie des Antrags.

**Über den eigenen Antrag entscheidet niemand selbst**, auch keine Administration. Wer einen Antrag stellt, wird aus dem Kreis der entscheidenden Personen gestrichen; findet sich danach niemand mehr, landet der Antrag bei den Administratoren. Ein Antrag, der in einem sichtbaren Posteingang liegen bleibt, ist ein Problem, um das sich jemand kümmern kann — ein Antrag, der verschwunden ist, nicht.

Steht eine Art auf automatischer Genehmigung, wird der Antrag sofort entschieden, du wirst benachrichtigt, und in der Historie steht, dass niemand darüber geurteilt hat.

!!! info "Und wenn niemand übrig bleibt?"
    In einer Organisation aus einer einzigen Person bleibt die Empfängerliste leer: Wer den Antrag stellt, wäre die einzige Person, die ihn entscheiden könnte, und über den eigenen entscheidet niemand. Der Antrag ist deshalb nicht verloren. Wer die Abwesenheitsverwaltung führt, darf jeden Antrag entscheiden, auch einen ohne Empfänger — sobald also eine zweite Person dazukommt oder jemand dafür benannt wird, steht er in deren Posteingang.

## Abwesenheiten im Team

Hat die Administration den **Team-Abwesenheitskalender** eingeschaltet, gibt es in der Zeiterfassung unter den Abwesenheiten einen fünften Bereich: **Team**. Er zeigt, wer in einer Gruppe wann abwesend ist, als Planungsansicht und nicht als Anwesenheitsliste. Du siehst Zeiträume, nie Uhrzeiten, und die Personen stehen nach Namen sortiert, nie danach, wer am meisten weg war.

Oben wählst du die Gruppe: **Meine Projekte**, eines deiner Teams oder ein Projekt. In einer Gruppe erscheint nur, wer selbst Zeit auf einem ihrer Projekte erfasst hat. Mitglied zu sein reicht nicht, denn wer ein Projekt oder ein Team anlegt, kann dort jede Person aufnehmen, ohne zu fragen. Daneben schaltest du zwischen **Monat** und **Quartal** um und blätterst mit den Pfeilen.

Was du über eine Abwesenheit erfährst, legt die Administration fest, und jede Abwesenheitsart kann es weiter einschränken:

- **Nur, dass jemand abwesend ist:** ein neutraler Balken mit dem Wort *Abwesend*.
- **Die Art der Abwesenheit:** der Balken trägt Symbol und Namen der Art. Eine Art, die nur für die Person selbst sichtbar ist, erscheint bei anderen gar nicht.
- **Krankheit** steht auf jeder Stufe nur als *Abwesend* da, auch in deiner eigenen Zeile. Das ist eine Gesundheitsangabe (Art. 9 DSGVO), und ein Kalender, auf den andere schauen, ist nicht der Ort dafür.

Ein **beantragter** Zeitraum ist schraffiert und mit einer Sanduhr markiert, ein genehmigter ist ausgefüllt. Wochenenden und Feiertage liegen als Fläche dahinter.

Leitungen eines Projekts, Admins eines Teams und die Abwesenheitsverwaltung sehen über den Zeilen zusätzlich, wie viel **Kapazität** der Gruppe an jedem Tag bleibt: die geplanten Stunden aller, abzüglich Feiertagen und genehmigter Abwesenheiten. **Beantragt zeigt, genehmigt zählt:** ein offener Antrag senkt die Kapazität nicht, sonst hätte ein zurückgezogener Antrag die Planung rückwirkend verändert. Die Zahl ist immer eine Summe und nennt nie eine Person.

Auf dem Telefon wird aus dem Kalender eine **Wochenliste**: je Woche die verfügbaren Stunden als Satz, darunter die Personen, die fehlen, mit Zeitraum und Art. Ein Raster aus fünf sichtbaren Tagen wäre dort nicht lesbar.

Auf dem Dashboard zeigt die Karte **Heute abwesend** bis zu fünf Namen aus deinen Projekten und darunter, wie viele es noch sind.

## Abwesenheitsarten und Ansprüche verwalten

Die folgenden beiden Seiten sieht, wer die Abwesenheitsverwaltung führt. Das muss keine Administration sein: Die Organisation kann Personen dafür benennen, und sie finden den Weg dorthin in ihren eigenen Einstellungen.

**Abwesenheitsarten** ist der Katalog. Jede Art legt fest, ob sie bezahlt ist, ob sie gegen ein Kontingent zählt, wie ein Anspruch entsteht, was ins nächste Jahr übertragen wird, wer sie sieht und wer sie genehmigt. Die vier vorgegebenen Arten bleiben immer; ihre Gattung lässt sich nicht ändern, weil daran hängt, wie die Zeiterfassung sie behandelt. Eine Art, die schon benutzt wurde, wird stillgelegt statt gelöscht — sonst verlören vergangene Jahre ihren Bezug.

**Ansprüche** ist das Verzeichnis neben dem Stand jeder Person für eine Art und ein Jahr. Von hier aus wird zugeteilt, für eine Person oder für viele auf einmal; vor dem Zuteilen zeigt eine Vorschau, was bei wem herauskäme und warum. Eine **Korrektur** verschiebt ein Konto um einen Betrag und verlangt immer eine Begründung — ein Saldo, der sich ohne genannten Grund bewegt hat, ist der, nach dem in einem Jahr jemand fragt.

!!! warning "Was der Standard verspricht"
    Urlaub steht auf 20 Tagen, nicht auf 30. Das ist der gesetzliche Mindesturlaub bei einer Fünftagewoche (§ 3 Abs. 1 BUrlG). Ein Standard soll nichts zusagen, was dein Arbeitgeber nicht zugesagt hat; was darüber hinausgeht, trägt die Verwaltung ein.

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
