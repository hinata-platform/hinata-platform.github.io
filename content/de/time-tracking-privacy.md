---
title: Zeiterfassung: Datenschutz & Recht
description: Was die Zeiterfassung speichert, auf welcher Rechtsgrundlage und welche Richtlinie welche Auswertung erlaubt. Mit Checklisten für Betriebsvereinbarung, DSFA und VVT.
---

# Zeiterfassung: Datenschutz & Recht

Arbeitszeit ist ein personenbezogenes Datum. Wer sie erfasst, könnte damit auch Menschen überwachen.

Diese Seite richtet sich an dich als Betreiberin oder Betreiber einer Hinata-Instanz und an alle, die die Einführung mit dir vorbereiten: Betriebs- oder Personalrat, Datenschutzbeauftragte und Personalabteilung. Du erfährst, was das Modul speichert, auf welche Rechtsgrundlagen du dich stützen kannst, welche Einstellung welche Auswertung über Personen erlaubt und wie Betroffene ihre Rechte in der App wahrnehmen.

Der Rechtsrahmen hier ist deutsches und europäisches Recht, weil Mitbestimmung und Arbeitszeiterfassung dort am engsten geregelt sind.

!!! warning "Keine Rechtsberatung"
    Diese Seite ordnet ein und liefert Arbeitsmaterial. Eine Beratung ersetzt sie nicht. Mehr dazu [am Ende der Seite](#keine-rechtsberatung). Stand: 11.10.2026.

## Wer verantwortlich ist

Hinata wird selbst gehostet. Verantwortlicher im Sinne von Art. 4 Nr. 7 DSGVO für alles, was auf einer Instanz liegt, ist ihr Betreiber, meist also der Arbeitgeber. Der Herausgeber der App sieht keine Zeitdaten (siehe [Datenschutzerklärung](/de/privacy-policy.html)).

Betriebsvereinbarung, Datenschutz-Folgenabschätzung und Verzeichnis von Verarbeitungstätigkeiten sind deshalb deine Dokumente. Hinata liefert die Einstellungen und die Funktionen für die Betroffenenrechte. Welche davon laufen, entscheidest du.

Jede Richtlinie, die eine Aussage über eine Person möglich macht, ist ab Werk aus. Nach einem Update bleibt die Zeiterfassung so, wie sie war, bis jemand bewusst etwas einschaltet. Die Richtlinien stellen Organisationsadmins auf der Seite [Organisation](/de/organization.html) unter **Zeiterfassung** ein. Bleibt eine leer, gilt der Wert aus der Umgebung des Servers. Jede Richtlinie mit ihrem Standard steht unter [Zeiterfassung verwalten](/de/admin-time-tracking.html#richtlinienmatrix).

## Zweck und Datenkategorien

Das Modul zeichnet Arbeitszeit auf. Es dient den gesetzlichen Aufzeichnungspflichten und der Projektsteuerung. Wenn eingeschaltet, dient es auch der Freigabe von Stundenzetteln, der Abwesenheitsplanung und der Abrechnung. Dafür speichert es:

| Kategorie | Inhalt | Anmerkung |
| --- | --- | --- |
| Zeiteinträge | Tag, Dauer, optional Start- und Endzeit, Projekt, Vorgang, Tätigkeitsart, Beschreibung, Tags, abrechenbar ja/nein, Quelle (App, Timer, Smart Commit, Kalender), `createdAt`, `updatedAt`, `updatedBy` | Der Kern. Ohne Start- und Endzeit ist ein Eintrag nur eine Dauer an einem Tag. |
| Laufender Timer | Startzeitpunkt und die Angaben für den späteren Eintrag | Höchstens einer je Person. Beim Stoppen wird er zum Eintrag, nach einem vollen Tag endet er von selbst. |
| Einreichungen und Freigaben | Zeitraum, Status (eingereicht, freigegeben, abgelehnt, zurückgezogen), wer wann entschieden hat, Notizen | Nur wenn Stundenzettel-Freigaben eingeschaltet sind. |
| Korrekturanfragen und Bitten um ältere Tage | Betroffener Eintrag oder Zeitraum, Begründung, Antwort mit Notiz, Zeitpunkte | Eigene Sammlung. Das Audit-Protokoll wiederholt sie (`TIME_CORRECTION_REQUESTED`, `TIME_BACKFILL_REQUESTED`, `TIME_CORRECTION_ANSWERED`). |
| Für eine Person geöffnete Tage | Zeitraum, wer geöffnet hat, Ablaufzeitpunkt, gegebenenfalls eine Nachricht | Schließen sich nach zwei Wochen von selbst und stehen im Audit-Protokoll (`TIME_BACKFILL_GRANTED`, `TIME_BACKFILL_REVOKED`). |
| Geteilte Einträge | Wer wem eine Kopie eines Eintrags angeboten hat, ein Abbild von Tag, Dauer, Zeiten und Vorgang, Status, die Kopie nach Annahme | Der Eintrag bleibt beim Absender. Wer annimmt, bekommt eine Kopie in die eigene Erfassung. Das Audit-Protokoll hält Anbieten, Annehmen und Zurückziehen fest (`TIME_ENTRY_SHARED`, `TIME_SHARE_ACCEPTED`, `TIME_SHARE_REVOKED`). |
| Persönliche Einstellungen für den Timer | Zum Beispiel Länge von Pomodoros und Pausen | Am Konto gespeichert, nur für die Person selbst wichtig. |
| Kenntnisnahme des Datenschutzhinweises | Zeitpunkt (`timePrivacyAcknowledgedAt`) | Beleg, dass informiert wurde. Keine Einwilligung. |
| Arbeitszeiten | Geplante Minuten je Wochentag, der Tag, ab dem sie gelten, der gewählte Feiertagskalender, wer sie wann festgelegt hat | Planungsdaten. Ändert ein Organisationsadmin sie für eine andere Person, steht das im Audit-Protokoll (`AVAILABILITY_SCHEDULE_CHANGED`). |
| Abwesenheiten | Art (Urlaub, Krankheit, Sonstiges), erster und letzter Tag, halber Tag, optionale Notiz | Planungsdaten. Eine Abwesenheit hindert niemanden daran, Zeit zu erfassen. Ändert ein Organisationsadmin eine für eine andere Person, steht das ohne die Notiz im Audit-Protokoll (`AVAILABILITY_TIME_OFF_CHANGED`). |
| Abwesenheitskonten | Je Art und Jahr: Anspruch, Zuteilungen, Buchungen, Korrekturen, jeweils mit dem Tag, an dem sie wirken, der Begründung und der Person, die gehandelt hat | Planungsdaten. Das Journal ist die Quelle: kein Saldo wird gespeichert, jede Zahl auf jedem Bildschirm wird daraus gerechnet. Die Begründung einer Korrektur steht **nur** auf der Journalzeile. |
| Beschäftigungsdaten für die Berechnung | Eintritts- und Austrittsdatum, optionale Notiz | Nur dafür da, Ansprüche zu rechnen (§§ 4, 5 und 7 Abs. 4 BUrlG). Lesen und schreiben kann sie nur die Abwesenheitsverwaltung. Sie gehen mit dem Konto. |
| Abwesenheitsanträge | Art, Zeitraum, Anteil des ersten und letzten Tages, eingefrorene Tagesmenge, Status, optionale Notiz, die beim Einreichen ermittelten entscheidenden Personen, optionale Vertretung, die Historie jedes Schritts mit Zeitpunkt und handelnder Person | Der Antrag ist das Dokument, die Abwesenheit sein Ergebnis. Die Begründung einer Entscheidung steht **nur** hier, nie im Audit-Protokoll. Das Protokoll hält Art, Zeitraum und Menge fest (`TIME_OFF_REQUEST_SUBMITTED`, `_APPROVED`, `_REJECTED`, `_WITHDRAWN`, `_CANCELLED`). |
| Krankmeldungen | Zeitraum, halber Tag, Art | Eine Meldung, kein Antrag: keine entscheidende Person, kein Status, kein Pflichtfeld und **kein Nachweis**. Das Protokoll hält nur fest, dass gemeldet wurde, und für welchen Zeitraum (`TIME_OFF_SICK_REPORTED`). |
| Hinweise auf Urlaubsverfall | Wer wann informiert wurde, zu welcher Art und welchem Jahr, wie viele Tage offen waren und wann sie verfallen | Nachweis für einen Verfall. Wird nie gelöscht (`TIME_OFF_EXPIRY_NOTICE_SENT`). |
| Kalender-Abos | Name, Farbe, die Adresse des Kalenders, mit AES-256-GCM verschlüsselt und an den Datensatz gebunden, ihr Host, Status und letzter Fehler, die Übernahmeregel, Zeitstempel | Nur mit eingeschaltetem Kalender-Import. Nur die Person, der das Abo gehört, sieht es. Die Adresse wird nie wieder angezeigt, auch ihr nicht, und steht in keinem Log, keiner Antwort und keinem Export. Das Audit-Log hält Anlegen und Entfernen nur mit dem Host fest (`TIME_CALENDAR_SUBSCRIPTION_CREATED`, `_DELETED`). |
| Kalendertermine | Je Vorkommen von 30 Tagen zurück bis 90 Tage voraus: Beginn, Ende, Zeitzone, Titel und Ort (je auf 200 Zeichen gekürzt), ganztägig, frei oder belegt, vorläufig oder bestätigt | Ein Zwischenspeicher, der bei jedem Abruf ersetzt wird und **nur** der Person angezeigt wird, die abonniert hat. Termine stehen in keinem Bericht, keinem Posteingang und keinem fremden Export. Erst ein Termin, den die Person übernimmt, wird zu Daten, die andere sehen können, als gewöhnlicher Eintrag mit der Quelle *Kalender*. |
| Stundensätze | Verkaufs- und Personalkostensätze je Team, Projekt, Person, Person in einem Projekt oder Vorgang, jeweils mit Geltungszeitraum und wer sie angelegt hat | Nur mit eingeschalteter Abrechnung. Sätze werden nie überschrieben: Eine Änderung ist ein neuer Satz ab einem Datum. Ein Personalkostensatz einer Person kann ihr Gehalt verraten. |
| Rechnungen und Gutschriften | Nummer, Empfänger, Positionen mit Beschreibung, Minuten, Satz und Betrag wie gestellt, die Einträge, aus denen eine Position entstand | Ein Buchungsbeleg. Wird nie gelöscht (§ 147 AO, § 257 HGB). |
| Timer-Kopien auf dem Gerät | Zustand des Timers für Systemflächen: Start, Modus und Phase, ab Werk ohne Beschreibung | Bleibt auf dem Gerät. Siehe [Timer außerhalb der App](#timer-außerhalb-der-app). |

!!! danger "Eine Begründung bleibt beim Vorgang, nicht im Protokoll"
    Wenn jemand ein Konto berichtigt, verlangt Hinata einen Grund. Diesen Grund schreibt es auf die Journalzeile, **nicht** ins Audit-Protokoll. Für die **Ablehnung eines Antrags** gilt dasselbe: Der Satz steht auf dem Antrag und verschwindet mit ihm. Das ist Absicht: Eine Begründung kann eine Gesundheitsangabe oder eine Schwerbehinderung nennen (§ 208 SGB IX), also ein Datum nach Art. 9 DSGVO. Im Audit-Protokoll überlebte sie das Löschen des Kontos, überstünde das Abschalten des Moduls und wäre für alle lesbar, die das Protokoll sehen. Das Audit-Protokoll hält fest, **dass** jemand korrigiert oder entschieden hat, für welche Art, welchen Zeitraum und um wie viel.

!!! info "Wer diese Protokolleinträge liest"
    Einträge zu Arbeitszeit, Stundenzetteln und Abwesenheiten stehen im Protokoll auf der Seite [Organisation](/de/organization.html). Administratoren sehen sie unter **Adminbereich → Audit** nicht. Einträge zu Abwesenheiten, also Anträge, Krankmeldungen und Konten, sieht dort nur, wer die Abwesenheiten führt: die benannte Abwesenheitsverwaltung oder, solange niemand benannt ist, die Organisationsadmins. Welche dieser Ereignisse aufgezeichnet werden, legen die Organisationsadmins fest, nicht die Administratoren.

!!! info "Warum die Kenntnisnahme keine Einwilligung ist"
    Im Arbeitsverhältnis ist eine Einwilligung wegen der Abhängigkeit selten freiwillig. Die Pflicht zur Arbeitszeiterfassung hängt ohnehin nicht von ihr ab. Der Klick auf **Verstanden** belegt deshalb nur, dass die Information nach Art. 13 DSGVO erfolgt ist. Wer nicht klickt, verliert dadurch kein Recht und gewinnt auch keins.

## Empfänger und Fristen

### Empfänger

- Die Person selbst sieht ihre eigenen Daten immer.
- Organisationsadmins sehen Stunden, Person und Projektschlüssel für alle. Vorgangstitel und Beschreibungen nur aus Projekten, in denen sie Mitglied sind.
- Leitungen sehen einzelne Einträge nur mit `leadsSeeMemberEntries`. Sonst sehen sie Summen.
- Andere Projektmitglieder sehen an einem Vorgang nur Tag, Dauer und Tätigkeit.
- Die Abwesenheitsverwaltung sieht Abwesenheiten und Konten aller, Krankheit eingeschlossen.
- Kunden bekommen Rechnungen, wenn die Abrechnung eingeschaltet ist.
- Auftragsverarbeiter: Hosting, Mailserver und für Push-Benachrichtigungen das Gateway [Hinata Connect](/de/connect-gateway.html) mit Firebase Cloud Messaging und dem Apple Push Notification Service.

### Fristen

- Zeiteinträge: nie gelöscht, bis du **Einträge löschen nach** setzt, dann mindestens 24 Monate.
- Angaben zu Krankheit: nach 12 Monaten vergröbert. Abgeschlossene Abwesenheitsanträge: nach 36 Monaten gelöscht. Urlaubsjournal: bleibt, außer du setzt mindestens 3 Jahre.
- Hinweise auf Urlaubsverfall, Rechnungen und Gutschriften: nie gelöscht.
- Audit-Protokoll: 365 Tage.

Die vollständige Tabelle steht unter [Aufbewahrung](/de/admin-time-tracking.html#aufbewahrung).

## Rechtsgrundlagen

### Datenschutzrecht

- **Art. 6 Abs. 1 lit. b DSGVO:** Durchführung des Arbeitsvertrags, etwa wenn Vergütung oder Überstundenausgleich von der erfassten Zeit abhängt.
- **Art. 6 Abs. 1 lit. c DSGVO:** Erfüllung einer rechtlichen Pflicht, hier der Pflicht zur Arbeitszeiterfassung (siehe unten).
- **Art. 6 Abs. 1 lit. f DSGVO:** berechtigte Interessen, etwa Projektsteuerung oder Abrechnung mit Kunden. Dafür brauchst du eine dokumentierte Abwägung. Betroffene können nach Art. 21 DSGVO widersprechen.
- **Art. 88 DSGVO i. V. m. § 26 Abs. 4 BDSG:** Betriebs- und Dienstvereinbarungen sowie Tarifverträge können spezifischere Vorschriften für den Beschäftigtendatenschutz sein. Das gilt nur, wenn sie Art. 88 Abs. 2 DSGVO erfüllen, also angemessene und besondere Maßnahmen zum Schutz der Beschäftigten enthalten.
- **Art. 9 Abs. 2 lit. b DSGVO i. V. m. § 22 Abs. 1 Nr. 1 lit. b BDSG:** für Krankheitstage, die Gesundheitsdaten sind. Siehe [Gesundheitsdaten](#gesundheitsdaten).

!!! warning "§ 26 Abs. 1 S. 1 BDSG trägt nicht mehr"
    Der EuGH hat am 30.03.2023 entschieden (C-34/21): Nationale Regeln zum Beschäftigtendatenschutz, die Art. 88 Abs. 2 DSGVO nicht erfüllen, bleiben unangewendet, sofern sie nicht selbst eine Rechtsgrundlage nach Art. 6 Abs. 3 DSGVO sind. Das BAG hat daraus mit Urteil vom 08.05.2025 (8 AZR 209/21) gefolgert, dass § 26 Abs. 1 BDSG unangewendet bleibt. Stütze die Verarbeitung deshalb auf Art. 6 Abs. 1 DSGVO und, wo es sie gibt, auf eine Kollektivvereinbarung.

### Pflicht zur Arbeitszeiterfassung

- **EuGH, Urteil vom 14.05.2019, C-55/18 *CCOO*:** Die Mitgliedstaaten müssen Arbeitgeber verpflichten, ein objektives, verlässliches und zugängliches System einzurichten, das die tägliche Arbeitszeit jeder Person misst.
- **BAG, Beschluss vom 13.09.2022, 1 ABR 22/21:** In Deutschland folgt diese Pflicht schon aus § 3 Abs. 2 Nr. 1 ArbSchG, wenn man ihn unionsrechtskonform auslegt. Beginn und Ende der täglichen Arbeitszeit samt Überstunden sind zu erfassen. Ob ein elektronisches System eingeführt wird, kann der Betriebsrat nicht erzwingen. Wie es arbeitet, bestimmt er mit.
- **§ 16 Abs. 2 ArbZG:** Arbeitszeit über acht Stunden am Werktag ist aufzuzeichnen. Die Nachweise sind mindestens zwei Jahre aufzubewahren. Eine Frist für die Aufzeichnung nennt die Vorschrift nicht.
- **§ 9 ArbZG:** verbietet die Arbeit an Sonn- und Feiertagen, mit den Ausnahmen der §§ 10 bis 13 ArbZG. Verboten ist die Arbeit, nicht ihre Aufzeichnung. Deshalb sperrt Hinata nie einen Eintrag an einem Feiertag.
- **§ 17 Abs. 1 MiLoG:** Für geringfügig Beschäftigte (§ 8 Abs. 1 SGB IV) und in den Branchen aus § 2a SchwarzArbG (unter anderem Bau, Gastronomie, Personenbeförderung, Logistik, Gebäudereinigung, Fleischwirtschaft, Sicherheitsgewerbe) sind Beginn, Ende und Dauer der täglichen Arbeitszeit aufzuzeichnen. Das muss spätestens bis zum Ende des **siebten Kalendertags** nach dem Arbeitstag geschehen. Die Aufzeichnungen sind mindestens zwei Jahre aufzubewahren. Verstöße kosten nach § 21 Abs. 1 Nr. 8 MiLoG ein Bußgeld.

!!! note "Ausblick: Referentenentwurf vom 18.06.2026 (nicht verabschiedet)"
    Ein Referentenentwurf des BMAS zur Änderung des ArbZG vom 18.06.2026 sieht unter anderem vor, die Arbeitszeit in der Regel noch am Tag der Arbeit aufzuzeichnen. Er ist **nicht verabschiedet**. Das ist der Stand beim Schreiben dieser Seite. Bis ein Gesetz beschlossen ist, gilt die Rechtslage oben.

### Mitbestimmung

Die Bewertung obliegt in jedem Fall den Betriebsparteien. Diese Tatbestände können berührt sein:

- **§ 87 Abs. 1 Nr. 6 BetrVG:** Einführung und Anwendung technischer Einrichtungen, die dazu bestimmt sind, Verhalten oder Leistung zu überwachen. Nach ständiger Rechtsprechung des BAG reicht es, dass eine Einrichtung objektiv dazu geeignet ist. Eine Absicht zur Überwachung ist nicht nötig. Das ist der zentrale Tatbestand für das ganze Modul.
- **§ 87 Abs. 1 Nr. 1 BetrVG:** Fragen der Ordnung des Betriebs, etwa Pflichtfelder oder wie genau Beschreibungen sein müssen.
- **§ 87 Abs. 1 Nr. 2 BetrVG:** Beginn und Ende der täglichen Arbeitszeit, Pausen und die Verteilung auf die Wochentage, etwa in Arbeitszeiten und Feiertagskalendern.
- **§ 87 Abs. 1 Nr. 3 BetrVG:** vorübergehende Verkürzung oder Verlängerung der Arbeitszeit, etwa wo Berichte und Ziele auf Überstunden zeigen.
- **§ 87 Abs. 1 Nr. 5 BetrVG:** Urlaubsgrundsätze, Urlaubsplan und die Festlegung des Urlaubs einzelner Personen. Siehe [Abwesenheiten](#abwesenheiten-eigenes-recht).
- **§ 87 Abs. 1 Nr. 7 BetrVG:** Gesundheitsschutz, etwa die Arbeitszeit-Hinweise zu Ruhezeiten.
- **Öffentlicher Dienst:** Hier gilt das Personalvertretungsrecht. Für Dienststellen des Bundes ist das § 80 Abs. 1 Nr. 21 BPersVG, in den Ländern das jeweilige Landespersonalvertretungsgesetz (LPVG).

### Steuer- und Handelsrecht

Gestellte Rechnungen und Gutschriften sind Buchungsbelege. § 147 AO und § 257 HGB verlangen, sie aufzubewahren. Hinata löscht sie nie, und die Einträge, die eine Rechnung nennt, sind von Löschung und Änderung ausgenommen, bis eine Gutschrift sie freigibt.

### Datenschutz-Folgenabschätzung

Die [Muss-Liste der Datenschutzkonferenz](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf) nennt unter Nr. 8 die umfangreiche Verarbeitung von Daten über das Verhalten von Beschäftigten, mit denen sich ihre Arbeit so bewerten lässt, dass Rechtsfolgen entstehen oder sie sonst erheblich beeinträchtigt werden.

Je mehr Auswertungen über Personen du einschaltest, desto eher brauchst du eine DSFA nach Art. 35 DSGVO. Prüf das mit der [DSFA-Checkliste](#dsfa-checkliste) und halte das Ergebnis fest. Das gilt auch, wenn du zu dem Schluss kommst, dass keine DSFA nötig ist.

## Richtlinienmatrix

Die vollständige Matrix mit Wirkung, Sichtbarkeit, Hinweis zur Mitbestimmung und Standard jeder Richtlinie steht unter [Zeiterfassung verwalten](/de/admin-time-tracking.html#richtlinienmatrix). Nutze sie als Anlage zu eurer Vereinbarung. Für alles darin gelten diese vier Grundsätze:

1. **Hinata verhindert nie die Aufzeichnung geleisteter Arbeitszeit.** Feiertage, Wochenenden, Betriebsruhe und Abwesenheiten werden markiert, nicht gesperrt. Grundlage: BAG 13.09.2022, 1 ABR 22/21 und EuGH 14.05.2019, C-55/18 (CCOO); § 16 Abs. 2 ArbZG verlangt die Aufzeichnung der Arbeitszeit über die werktägliche hinaus, und dazu zählt nach herrschender Auslegung jede Arbeit an Sonn- und Feiertagen. § 9 ArbZG verbietet die Arbeit an Feiertagen, nicht ihre Dokumentation.
2. **Gesperrt wird ausschließlich die Vergangenheit, nie Gegenwart oder Zukunft.** Das Sperrdatum ist ein Integritätswerkzeug für abgeschlossene Zeiträume (Art. 32 DSGVO; Aufbewahrung § 16 Abs. 2 ArbZG / § 17 MiLoG, zwei Jahre), kein Steuerungsinstrument.
3. **Jede Unveränderlichkeit hat einen dokumentierten Rückweg.** Sperrdatum, Freigabe und Rechnung: mit Korrekturantrag, Reopen bzw. Gutschrift, immer mit Begründung im Audit. Ohne Rückweg kollidiert die Sperre mit Art. 16 DSGVO: Arbeitszeit ist ein personenbezogenes Datum, unrichtige Daten sind unverzüglich zu berichtigen.
4. **Verspätete Erfassung wird nie abgelehnt, höchstens kenntlich gemacht.** Nachträge sind bis zur Richtlinie `maxDaysBack` (Default 365 Tage) möglich, darüber hinaus über den Ausnahmeweg. Die Frist des § 17 Abs. 1 MiLoG (sieben Kalendertage in den Branchen des § 2a SchwarzArbG und bei geringfügig Beschäftigten, bußgeldbewehrt nach § 21 MiLoG) bleibt eine organisatorische Pflicht des Betreibers; Hinata unterstützt sie mit dem Selbst-Hinweis und erzwingt sie nicht.

!!! note "Was das Audit-Protokoll ab Werk festhält"
    Eingriffe in fremde Daten stehen ab Werk im Audit-Protokoll: das Löschen oder Ändern eines fremden Eintrags, ein Eintrag für eine andere Person (`TIME_ENTRY_CREATED_FOR`, etwa per Smart Commit), Änderungen am Sperrdatum, wieder geöffnete Zeiträume, für eine Person geöffnete Tage, Korrekturanfragen, Entscheidungen über Stundenzettel und Abwesenheiten und jeder Lauf der automatischen Löschung. Das schützt die Betroffenen, denn es hält fest, was mit ihren Daten passiert. Wann sie arbeiten, steht dort nicht: Die Timer-Ereignisse und `TIME_ENTRY_CREATED` sind ab Werk aus.

## Was Hinata bewusst nicht tut

- Keine Aktivitätsüberwachung: keine Screenshots, keine Tastenanschläge, keine Protokolle von Apps oder Webseiten.
- Keine Erkennung von Untätigkeit. Ein laufender Timer prüft nicht, ob jemand an der Tastatur sitzt.
- Keine Ranglisten und keine Vergleichswerte zwischen Personen.
- Keine Team-Erinnerungen. Eine Erinnerung geht immer nur an die Person, die sich das Ziel gesetzt hat.
- Keine Buchungssperre an Feiertagen, Wochenenden oder außerhalb der Arbeitszeiten.
- Kein Sperrdatum in der Zukunft.
- Keine automatische Einreichung von Stundenzetteln, keine Sanktion und keine Auswertung, wer spät erfasst hat.
- Den Grund jeder Sperre sieht die Person selbst: warum der Tag geschlossen ist, wer ihn öffnen kann und wie sie darum bittet. Jede Ablehnung nennt Grund, zuständige Stelle und den Rückweg.

## Zeitberichte, Exporte und geteilte Links

Die Zeitberichte unter **Zeiterfassung → Berichte** öffnen keine neue Sicht auf Personen. Sie lesen, was die Richtlinien ohnehin freigeben.

- **Summen** je Projekt, Tätigkeit, Tags, Vorgang oder Zeitraum enthalten die eigenen Einträge und alle Einträge der Projekte, die jemand sieht. Dass an einem Vorgang Zeit gebucht wurde, sieht jedes Mitglied bereits am Vorgang. Eine Summe nennt niemanden.
- **Personen** nennt ein Bericht nur bei den eigenen Einträgen und, mit `leadsSeeMemberEntries`, bei den Mitgliedern der Projekte, die jemand leitet. Dieselbe Regel gilt für die Liste der Einträge und für jeden Export.
- **Organisationsadmins** sehen Stunden, Person und Projektschlüssel für alle. Vorgangstitel, Vorgangsschlüssel, Beschreibungen und Projektnamen sehen sie nur bei Projekten, in denen sie Mitglied sind, und bei ihren eigenen Einträgen. Die Suche in den Beschreibungen durchsucht nur Einträge, die sie lesen dürfen.
- Das alles steht in der Abfrage an die Datenbank. Nichts wird erst gelesen und danach weggefiltert.

Wer einen gespeicherten Bericht **teilt**, gibt einen Link weiter, nicht seine Sicht. Wer den Link öffnet, muss angemeldet sein und bekommt den Bericht mit dem, was er selbst sehen darf. Vom Link speichert Hinata nur einen Hash, und die Person, die ihn erzeugt hat, kann ihn jederzeit widerrufen.

Ein **geplanter Bericht per Mail** geht an eine Liste von bis zu 50 aktiven Konten. Jede Person bekommt ihn mit ihrer eigenen Sicht, ohne Anhang und mit einem Link in die App. Wer einen Bericht plant, bekommt ihn nur, wenn er selbst auf der Liste steht. Das Protokoll des Versands zählt Berichte, nicht Personen.

Jeder **Export** eines Berichts steht im Audit-Protokoll (`TIME_REPORT_EXPORTED`) mit Format, Zahl der Zeilen und einem Fingerabdruck der Filter. Namen und Suchwörter stehen dort nicht. Ein **CSV-Import** schreibt nur Einträge, die dieselben Prüfungen bestehen wie ein getippter Eintrag, also nie in einen gesperrten oder eingereichten Zeitraum. Importiert ein Organisationsadmin für eine andere Person, steht das im Audit-Protokoll (`TIME_ENTRIES_IMPORTED`).

## Checkliste Betriebs- oder Dienstvereinbarung

Eine Vereinbarung zur Zeiterfassung mit Hinata sollte mindestens diese Punkte klären:

- **Gegenstand und Geltungsbereich:** welche Instanz, welche Beschäftigten, welche Module. Leg die [Richtlinienmatrix](/de/admin-time-tracking.html#richtlinienmatrix) mit einer Spalte „unser Wert“ als Anlage bei.
- **Zwecke:** abschließend aufzählen, etwa Aufzeichnungspflichten, Projektsteuerung, Abwesenheitsplanung und Abrechnung. Jede andere Nutzung, besonders zur Kontrolle von Verhalten oder Leistung, ausdrücklich regeln oder ausschließen.
- **Datenkategorien und Pflichtfelder:** ob Projekt, Vorgang, Beschreibung oder Tag Pflicht sind. Wie genau Beschreibungen sein sollen und was nicht hineingehört, zum Beispiel Gesundheitsangaben wie „Arzttermin“.
- **Sichtbarkeit:** wer wessen Einträge sieht (die Person selbst, Leitungen nur mit `leadsSeeMemberEntries`, Organisationsadmins) und wer diese Rolle bekommt. An Vorgängen sehen andere Mitglieder nur Tag, Dauer und Tätigkeit.
- **Freigaben:** ob Stundenzettel eingereicht werden, in welchem Rhythmus, wer freigibt und was bei Ablehnung und Wiederöffnen passiert.
- **Auswertungen und Benachrichtigungen:** Auslastungsberichte, Abwesenheitsberichte, Budget-Warnungen und Ziel-Erinnerungen, jeweils ein oder aus, mit Empfängern und Schwellen. Dazu, ob Berichte geteilt und regelmäßig per Mail verschickt werden dürfen, und an wen.
- **Timer und Audit-Protokoll:** ob Start- und Endzeiten erfasst werden und ob die Ereignisse zum Timer im Audit-Protokoll eingeschaltet werden dürfen (Standard: aus).
- **Timer außerhalb der App:** welche Systemflächen angeboten werden, als Funktionen beschrieben (siehe [unten](#timer-außerhalb-der-app)).
- **Korrekturen und Sperren:** Sperrdatum, Umgang mit Korrekturanfragen, wieder geöffneten Zeiträumen und für Einzelne geöffneten Tagen, Nachtragen (`maxDaysBack`, `lateEntryHintDays`).
- **Abwesenheiten:** siehe die eigene [Checkliste zu Abwesenheiten](#mitbestimmung-beim-urlaub).
- **Abrechnung:** ob Personalkostensätze hinterlegt werden und wer sie sieht.
- **Kalender-Import:** freiwillig, nur der eigene Kalender, Umgang mit privaten Terminen.
- **Aufbewahrung und Löschung:** konkrete Werte für `entryPurgeMonths`, `descriptionPurgeMonths` und die Fristen für Abwesenheiten, und der Umgang mit freigegebenen Zeiträumen.
- **Exporte und Schnittstellen:** wer CSV- oder Berichtsexporte zieht und wohin sie gehen. Zugriffe über API und MCP haben dieselben Rechte wie die App. Nenn sie trotzdem.
- **Transparenz:** Text des Datenschutzhinweises (eingebaute Vorlage oder eigener Text) und Schulung für Leitungen und Organisationsadmins.
- **Änderungen:** Bevor eine neue Version von Hinata oder eine Richtlinie eine neue Auswertung über Personen einschaltet, wird die Interessenvertretung informiert und erneut beteiligt. Änderungen an den Richtlinien stehen im Audit-Protokoll.
- **Kontrollrechte:** Einsicht der Interessenvertretung in Einstellungen und Audit-Protokoll, Auswertung der Erfahrungen nach einer festen Frist.
- **Folgen von Verstößen:** zum Beispiel, dass Daten, die entgegen der Vereinbarung ausgewertet wurden, nicht verwendet werden dürfen.
- **Laufzeit, Kündigung und Nachwirkung.**

## DSFA-Checkliste

- **Schwellwertprüfung festhalten:** DSK-Muss-Liste Nr. 8 und die Kriterien aus WP 248 Rev. 01, darunter systematische Überwachung, schutzbedürftige Betroffene und Bewerten oder Einstufen. Je mehr Zeilen der [Richtlinienmatrix](/de/admin-time-tracking.html#richtlinienmatrix) eingeschaltet sind, desto eher ist eine DSFA nötig.
- **Systematische Beschreibung** (Art. 35 Abs. 7 lit. a DSGVO): Datenkategorien, Datenflüsse (App, Server, Mail, Push, Exporte, MCP), eingeschaltete Richtlinien mit ihren Werten und Empfänger.
- **Notwendigkeit und Verhältnismäßigkeit** (lit. b): Für jede eingeschaltete Richtlinie den Zweck nennen und begründen, warum ein milderes Mittel nicht reicht, etwa Projektsummen statt einzelner Buchungen. Datenminimierung: Pflichtfelder sparsam wählen, Start- und Endzeit nur, wo nötig.
- **Risiken für Betroffene** (lit. c): Kontrolle von Leistung und Verhalten, Profile aus Timerzeiten, Rückschlüsse aus Beschreibungen und Kalenderterminen (Gesundheit, Privates), Krankheitstage und Abwesenheitsquoten, Personalkostensätze, Exporte außerhalb des Systems, falsch vergebene Rollen, zu lange oder zu kurze Aufbewahrung.
- **Maßnahmen** (lit. d): Standardwerte aus, das Panel „Wer sieht meine Zeitdaten?“, Aufbewahrungsfristen, Sperrdatum mit protokollierten Ausnahmen, das [Sicherheitsmodell](/de/security.html) (TLS, Rollen, Ratenbegrenzung), verschlüsselte [Backups](/de/backups.html) und Schulungen.
- **Beteiligte:** Rat der oder des Datenschutzbeauftragten einholen (Art. 35 Abs. 2), Interessenvertretung einbeziehen, bei Bedarf die Betroffenen selbst fragen (Art. 35 Abs. 9).
- **Restrisiko bewerten:** Bleibt ein hohes Risiko, musst du vorher die Aufsichtsbehörde konsultieren (Art. 36 DSGVO).
- **Überprüfen:** bei jeder Änderung einer Richtlinie und bei neuen Versionen von Hinata mit neuen Auswertungen (Art. 35 Abs. 11).

## Vorlage: Verzeichnis von Verarbeitungstätigkeiten (Art. 30 DSGVO)

Die Spalte „Vorschlag“ enthält Formulierungen für eine typische Instanz. Die letzte Spalte füllst du für deine Organisation aus.

| Feld | Vorschlag für Hinata | Eure Angabe |
| --- | --- | --- |
| Verantwortlicher (Art. 30 Abs. 1 lit. a) | Name und Kontaktdaten des Betreibers, ggf. Vertreter | … |
| Datenschutzbeauftragte/r | Kontaktdaten | … |
| Bezeichnung der Verarbeitung | Arbeits- und Projektzeiterfassung, Abwesenheitsplanung und Abrechnung mit Hinata | … |
| Zwecke (lit. b) | Erfüllung der Aufzeichnungspflichten (§ 3 Abs. 2 Nr. 1 ArbSchG, § 16 Abs. 2 ArbZG, ggf. § 17 MiLoG); Projektsteuerung; ggf. Freigabe von Stundenzetteln; ggf. Urlaubs- und Abwesenheitsplanung; ggf. Abrechnung mit Kunden | … |
| Rechtsgrundlagen | Art. 6 Abs. 1 lit. b, c und f DSGVO; für Krankheitstage Art. 9 Abs. 2 lit. b DSGVO i. V. m. § 22 Abs. 1 Nr. 1 lit. b BDSG; ggf. Betriebs- oder Dienstvereinbarung nach Art. 88 DSGVO i. V. m. § 26 Abs. 4 BDSG | … |
| Kategorien betroffener Personen (lit. c) | Beschäftigte; ggf. Auszubildende, Leiharbeitskräfte, freie Mitarbeitende mit Konto | … |
| Kategorien personenbezogener Daten (lit. c) | Kontostammdaten; Zeiteinträge (Tag, Dauer, optional Start und Ende, Projekt, Vorgang, Tätigkeitsart, Beschreibung, Tags, abrechenbar, Quelle, Änderungsdaten); laufender Timer; Einreichungen und Freigaben mit Notizen; Korrekturanfragen, Bitten um ältere Tage und Antworten; für die Person geöffnete Tage; geteilte Einträge; Einstellungen für den Timer; Zeitpunkt der Kenntnisnahme des Datenschutzhinweises; Arbeitszeiten; Abwesenheiten, Abwesenheitskonten, Abwesenheitsanträge, Krankmeldungen (nur Art und Tage), Beschäftigungsdaten, Hinweise auf Urlaubsverfall; bei eingeschaltetem Kalender-Import Kalender-Abos (Adresse verschlüsselt) und die daraus gelesenen Termine; bei eingeschalteter Abrechnung Stundensätze und Rechnungen | … |
| Speicherort (MongoDB-Sammlungen) | `work_items`, `running_timers`, `timesheet_approvals`, `time_correction_requests`, `time_backfill_grants`, `time_entry_shares`, `time_tags`, `saved_reports`, `time_imports`, `time_marks`, `time_departed_users`, `time_retention_runs`, `project_time_settings`, `working_schedules`, `holiday_calendars`, `holidays`, `time_off`, `time_off_types`, `time_off_entitlements`, `time_off_ledger`, `time_off_employment`, `time_off_requests`, `time_off_notices`, `time_off_proposals`, `time_off_year_runs`, `time_off_retention_runs`, `calendar_subscriptions`, `calendar_events`, `billing_rates`, `invoices`, `invoice_sequences` | … |
| Empfänger (lit. d) | Die Person selbst; Organisationsadmins; Abwesenheitsverwaltung; Leitungen nur bei eingeschalteter Richtlinie; andere Projektmitglieder nur Tag, Dauer und Tätigkeit an Vorgängen; Kunden über Rechnungen; ggf. Lohnbuchhaltung über Exporte; Dienstleister für Hosting und E-Mail als Auftragsverarbeiter | … |
| Übermittlung in Drittländer (lit. e) | Keine, wenn Server, Speicher und Mailserver in der EU laufen. Push-Benachrichtigungen gehen über das Gateway [Hinata Connect](/de/connect-gateway.html), Firebase Cloud Messaging (Google) und den Apple Push Notification Service; bewerte sie nach dem EU-US Data Privacy Framework oder Standardvertragsklauseln. Mit eingeschaltetem Kalender-Import ruft der Server jeden abonnierten Kalender bei dem Anbieter ab, den die Person gewählt hat (zum Beispiel Google, Microsoft oder Apple) | … |
| Löschfristen (lit. f) | `entryPurgeMonths` (nie oder frühestens 24 Monate nach dem Tag des Eintrags); `descriptionPurgeMonths` für gelöschte Konten; Angaben zu Krankheit 12 Monate, abgeschlossene Anträge 36 Monate, Urlaubsjournal dauerhaft oder mindestens 3 Jahre; Rechnungen und Hinweise auf Urlaubsverfall nie; Audit-Protokoll 365 Tage | … |
| Technische und organisatorische Maßnahmen (lit. g, Art. 32) | Verweis auf das [Sicherheitsmodell](/de/security.html): TLS, rollenbasierte Rechte, Sperrdatum, Audit-Protokoll, Ratenbegrenzung, Backups; Richtlinienwerte laut Anlage | … |
| DSFA | durchgeführt ja/nein, Datum, Ergebnis der Schwellwertprüfung | … |
| Letzte Überprüfung | Datum und Anlass (zum Beispiel neue Richtlinie eingeschaltet) | … |

## Betroffenenrechte in Hinata

### Information (Art. 12 bis 14 DSGVO)

Wer das Modul zum ersten Mal öffnet, sieht den Datenschutzhinweis einmal als Sheet. **Verstanden** schließt ihn und speichert den Zeitpunkt (`timePrivacyAcknowledgedAt`). Das belegt die Information und ist keine Einwilligung. Danach bleibt der Hinweis unter **Einstellungen → Zeiterfassung → Datenschutz** erreichbar.

Dort steht auch das Panel **„Wer sieht meine Zeitdaten?“**. Hinata berechnet es aus den Richtlinien, die gerade aktiv sind. Niemand pflegt es von Hand. Schaltest du zum Beispiel `leadsSeeMemberEntries` ein, steht dort sofort, dass Leitungen die Einträge sehen. Das Panel kann also nicht veralten. Es zeigt auch, was andere Mitglieder an einem Vorgang sehen: wie viel Zeit gebucht wurde, aber nicht, wer sie gebucht hat, und nicht die Beschreibung.

Die eingebaute Vorlage gibt es in neun Sprachen. Unter **Organisation → Zeiterfassung → Datenschutz und Aufbewahrung** kannst du sie im Feld **Datenschutzhinweis** durch deinen eigenen Text ersetzen, etwa mit einem Verweis auf eure Betriebsvereinbarung. Bleibt das Feld leer, gilt die Vorlage. Auch die Datenschutzerklärung deiner Instanz muss das Modul abdecken, siehe [Die Datenschutzerklärung deiner Instanz](/de/admin-time-tracking.html#die-datenschutzerklärung-deiner-instanz).

### Auskunft und Datenübertragbarkeit (Art. 15 und 20 DSGVO)

Der Datenexport des Kontos enthält auch die Zeitdaten: Zeiteinträge, laufenden Timer, Einreichungen, Korrekturanfragen und Bitten um ältere Tage samt Antworten, für die Person geöffnete Tage, geteilte Einträge, Einstellungen für den Timer, den Zeitpunkt der Kenntnisnahme, die Arbeitszeiten und Abwesenheiten der Person, ihre Abwesenheitskonten mit jeder Journalzeile und deren Begründung, ihre Abwesenheitsanträge mit jeder Notiz und jeder Entscheidungsbegründung sowie ihre Kalender-Abos mit den daraus gelesenen Terminen. Ein Abo steht dort mit seinem Host, nie mit seiner Adresse, denn die Adresse ist ein Schlüssel zu einem fremden Dienst, und ein Export ist eine Datei, die weitergegeben wird. Gerade die Ablehnungsbegründung gehört dorthin: Sie steht bewusst in keinem Protokoll, also ist dieser Export der Ort, an dem die betroffene Person sie vollständig bekommt (Art. 15 DSGVO).

Es gibt ihn als JSON über `GET /api/v1/me/export` und als PDF-Bericht, dessen Link per E-Mail kommt. Sehr lange Historien werden dort gekürzt. Ein Hinweis im Export verweist dann auf den CSV-Export.

Die eigenen Einträge als CSV bekommst du in der App unter **Einstellungen → Zeiterfassung** oder direkt über die API:

```bash
curl -H "Authorization: Bearer $HINATA_TOKEN" \
  -o meine-zeiten.csv \
  "https://api.track.example.com/api/v1/time/export.csv?from=2026-01-01&to=2026-06-30"
```

Die Datei ist UTF-8 mit BOM, Excel zeigt Umlaute also richtig an. Zellen, die mit einem Formelzeichen beginnen, werden entschärft, damit kein Tabellenprogramm sie ausführt. Der Export wird gestreamt und umfasst bis zu 100 000 Zeilen. Wie oft eine Person ihn abrufen kann, ist begrenzt. Laufen gerade viele Exporte gleichzeitig, bittet Hinata darum, es kurz darauf noch einmal zu versuchen. Der Export enthält nur die Einträge der Person, die ihn anfordert.

### Berichtigung (Art. 16 DSGVO)

Deine eigenen Einträge bearbeitest du selbst. Liegt ein Tag vor dem Sperrdatum, in einem eingereichten Zeitraum oder auf einer Rechnung, ist er eingefroren. Die App sagt dir, warum, wer ihn öffnen kann und wie du darum bittest. Dann schickst du über **Korrektur anfragen** eine Begründung an die Person, die die Sperre aufheben kann. Beim Sperrdatum sind das die Organisationsadmins, bei einem eingereichten Zeitraum die Projektleitung oder wer freigibt. Pro Eintrag geht das einmal am Tag.

Die Antwort kommt mit einer Notiz als Benachrichtigung. Du findest sie am Eintrag und in seinem Verlauf. Die Antwort allein ändert noch nichts. Ändern kannst du den Eintrag erst, wenn der Tag wirklich wieder offen ist. Dafür gibt es vier Wege:

- Bei einem eingereichten Zeitraum öffnet die Projektleitung die Einreichung wieder.
- Beim Sperrdatum öffnet ein Organisationsadmin den Tag nur für dich, direkt aus der Anfrage heraus mit **Tage öffnen**. Die Öffnung gilt zwei Wochen und steht im Audit-Protokoll. Steht eine Notiz dabei, liest du sie als Antwort.
- Soll ein Zeitraum für alle wieder offen sein, legt ein Organisationsadmin eine Ausnahme vom Sperrdatum an. Die Begründung steht im Audit-Protokoll.
- Bei einem abgerechneten Eintrag gibt eine Gutschrift zur Rechnung ihn wieder frei.

Im Verlauf eines Eintrags sieht eine Projektleitung nur die Anfragen zu Einreichungen ihrer Projekte, weil nur diese an sie gerichtet sind. Anfragen zum Sperrdatum bleiben zwischen dir und den Organisationsadmins.

### Löschung und Speicherbegrenzung (Art. 17 und Art. 5 Abs. 1 lit. e DSGVO)

Wird ein Konto gelöscht, entfernt Hinata das Konto, einen laufenden Timer, noch nicht freigegebene Einreichungen, die Anfragen der Person, die für sie geöffneten Tage, ihre Arbeitszeiten, Abwesenheiten und Beschäftigungsdaten sowie ihre Abwesenheitsanträge, über die nie entschieden wurde. Entschiedene Anträge bleiben pseudonymisiert stehen, wie genehmigte Einreichungen und Buchungen: Sie sind der Nachweis darüber, wem was gewährt wurde. Im Verlauf von Einträgen steht danach kein Name mehr für sie, und die Texte ihrer Korrekturanfragen zeigt Hinata dort niemandem mehr.

Kalender-Abos und ihre Termine werden ebenfalls entfernt. Einträge, die eine Person aus einem Kalender übernommen hat, bleiben wie jeder andere Eintrag. Löscht jemand ein einzelnes Abo, verschwinden seine Termine sofort, und wer eine neue Adresse einfügt, verliert die Termine der alten. Das Ausschalten des Kalender-Imports beendet jeden Abruf und blendet die Termine aus, löscht aber nichts.

Freigegebene Einreichungen bleiben, weil sie ein Geschäftsnachweis sind. Auch die Zeiteinträge bleiben, mit der Nutzer-ID als Pseudonym, weil die Stunden zum Nachweis des Projekts gehören.

!!! note "Pseudonym ist nicht anonym"
    Solange sich eine Nutzer-ID einer Person zuordnen lässt, bleiben die Einträge personenbezogene Daten (Art. 4 Nr. 5 DSGVO). Dafür gibt es die Fristen unten.

Die Aufbewahrung stellst du unter **Organisation → Zeiterfassung → Datenschutz und Aufbewahrung** ein:

- **Beschreibungen leeren nach** (`descriptionPurgeMonths`) leert nach N Monaten die Beschreibungen in den Einträgen gelöschter Personen und die Notizen an ihren Stundenzetteln. Stunden und Entscheidungen bleiben.
- **Einträge löschen nach** (`entryPurgeMonths`) löscht für alle Personen Einträge, die älter als N Monate sind. Einträge in einem eingereichten oder freigegebenen Zeitraum und Einträge auf einer Rechnung löscht Hinata nie. Erlaubt sind 0 für nie oder mindestens 24 Monate. Ein kleinerer Wert aus der Umgebung des Servers gilt als 24.
- Die Fristen für Abwesenheiten (**Krankheit vergröbern nach**, **Abgeschlossene Anträge löschen nach**, **Urlaubsjournal löschen nach**) stehen unter [Aufbewahrung](/de/admin-time-tracking.html#aufbewahrung).

Die Löschung läuft nachts in Stapeln, auch mit mehreren Serverinstanzen nur einmal. Ein Lauf hat ein festes Zeitbudget. Wird er in dieser Zeit nicht fertig, macht der nächste Lauf dort weiter, wo er aufgehört hat. Jeder Lauf steht mit seinen Zählern im Audit-Protokoll (`TIME_RETENTION_RUN`, `TIME_OFF_RETENTION_RUN`), auch einer, der mit einem Fehler abbricht.

!!! warning "Standard ist 0: Es wird nichts automatisch gelöscht"
    Beide Fristen für Einträge stehen ab Werk auf `0`. Hinata löscht also keinen Eintrag, bis du dich bewusst für eine Frist entscheidest. Das ist Absicht: Eine Löschung lässt sich nicht rückgängig machen, und welche Frist passt, hängt von deiner Organisation ab.

Warum 24 Monate ein guter Ausgangspunkt sind: § 16 Abs. 2 ArbZG und § 17 Abs. 1 MiLoG verlangen beide, die Nachweise mindestens zwei Jahre aufzubewahren. Früher darfst du nicht löschen, deshalb nimmt Hinata keinen kleineren Wert an.

Danach gilt der Grundsatz der Speicherbegrenzung: Daten, die du für keinen Zweck mehr brauchst, musst du löschen. Rechnungen folgen eigenen Fristen (§ 147 AO, § 257 HGB).

!!! tip "Puffer für spät Nachgetragenes"
    Hinata zählt die Monate ab dem Tag des Eintrags. § 17 MiLoG zählt die zwei Jahre ab dem Zeitpunkt, der für die Aufzeichnung maßgeblich ist. Wenn bei euch oft spät nachgetragen wird, plan ein paar Monate Puffer ein.

### Widerspruch (Art. 21 DSGVO)

Widersprechen kann man, wo die Verarbeitung auf berechtigten Interessen beruht (Art. 6 Abs. 1 lit. f DSGVO), etwa bei Projektsteuerung oder Abrechnung. Einen Knopf dafür hat Hinata nicht. Der Betreiber prüft den Widerspruch und schaltet die Auswertung bei Erfolg ab oder begrenzt sie, zum Beispiel durch Abschalten der Auslastungsberichte. Gegen die Aufzeichnung der Arbeitszeit zur Erfüllung einer gesetzlichen Pflicht (Art. 6 Abs. 1 lit. c DSGVO) gibt es kein Widerspruchsrecht.

### Keine automatisierten Entscheidungen (Art. 22 DSGVO)

Budget-Warnungen, Ziel-Erinnerungen, Arbeitszeit-Hinweise und Hinweise auf späte Nachträge sind nur Hinweise. Hinata sperrt oder bewertet niemanden automatisch und kürzt nichts. Auch Urlaub nach langer Krankheit verfällt nie automatisch: Hinata schlägt den Verfall nur vor, und ein Mensch entscheidet. Was aus einem Hinweis folgt, entscheidet ein Mensch.

## ArbZG-Selbsthinweise

Mit **Arbeitszeit-Hinweise** (`arbzgHintsEnabled`, Standard: aus) zeigt Hinata einer Person an ihren eigenen Einträgen, wo sie an Grenzen des Arbeitszeitgesetzes stößt. Hinata rechnet dabei nur für die Person selbst und für höchstens 31 Tage. Es gibt vier Hinweise:

- Die Tagessumme liegt über 10 Stunden, der Höchstgrenze nach [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html).
- Zwischen dem Ende eines Arbeitstags und dem Beginn des nächsten liegen weniger als 11 Stunden Ruhezeit ([§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html)). Dafür braucht es Einträge mit Start- und Endzeit.
- Es gibt Einträge an einem Sonntag ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).
- Es gibt Einträge an einem Feiertag des Kalenders, nach dem sich die Person richtet ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).

Die Hinweise werden nicht gespeichert, nicht an Leitungen oder Organisationsadmins gegeben und nicht über mehrere Personen zusammengefasst. Sie helfen der Person selbst. Sie beweisen nicht, dass eure Arbeitszeiten dem ArbZG entsprechen, und sind kein Urteil. Das Gesetz kennt Ausnahmen, etwa für Sonntagsarbeit, von denen Hinata nichts wissen kann.

## Nachtragen: was möglich ist und was du organisatorisch sicherstellen musst

Hinata lehnt einen Nachtrag nie ab, nur weil er spät kommt. § 16 Abs. 2 ArbZG kennt keine Frist. Die Pflicht zur Aufzeichnung bleibt bestehen, bis aufgezeichnet ist, und eine späte Aufzeichnung ist besser als keine. Der EuGH verlangt in C-55/18 gerade, dass sich die tägliche Arbeitszeit tatsächlich messen lässt.

Einen ganzen Monat am Monatsende nachzutragen, ist möglich und erlaubt. Ebenso, über mehrere Monate nachzutragen. Wo eine Branchenfrist gilt, stellt der Betreiber sie organisatorisch sicher. Die Software macht Verspätung höchstens sichtbar, und nur für die betroffene Person.

Mit `lateEntryHintDays` kannst du einen Hinweis einschalten (Standard: leer, also kein Hinweis). Ist ein Wert gesetzt, zeigt ein später erfasster Eintrag „N Tage nach dem Arbeitstag erfasst“. Das sieht nur die Person selbst, in keinem Bericht taucht es auf.

Die Schwelle ist einstellbar und nicht fest auf sieben Tage gesetzt. Die Frist von sieben Tagen aus § 17 MiLoG gilt nur für bestimmte Branchen und geringfügig Beschäftigte, und der Referentenentwurf vom 18.06.2026 könnte die Aufzeichnung am selben Tag zur Regel machen. Wo das MiLoG gilt, liegt `7` nahe.

`maxDaysBack` (Standard: 365) schützt vor Tippfehlern, damit etwa 2025 statt 2026 nicht unbemerkt durchgeht. Ältere Tage bietet die Datumsauswahl gar nicht erst an, und beim Speichern lehnt Hinata sie ab. Beide Stellen zeigen den Ausweg:

1. Die Person bittet mit einer Begründung darum, die Tage zu öffnen. Das geht direkt an der Meldung, in der Datumsauswahl oder unter **Einstellungen → Zeiterfassung → Ältere Tage anfragen**. Die Anfrage wird protokolliert.
2. Ein Organisationsadmin öffnet die Tage für diese Person unter **Organisation → Zeiterfassung → Korrekturanfragen** mit **Tage öffnen**. Die Öffnung gilt zwei Wochen und nur für diese Person. Die Begründung dazu liest die Person als Antwort, und sie steht im Audit-Protokoll. Unter **Für Personen geöffnete Tage** lässt sich eine Öffnung früher schließen.
3. Die Person trägt die Zeit nach.

!!! danger "Die MiLoG-Frist einzuhalten, bleibt deine Pflicht"
    Hinata unterstützt dich dabei, erzwingt aber nichts. Wo § 17 MiLoG gilt, musst du organisatorisch dafür sorgen, dass Beginn, Ende und Dauer innerhalb von sieben Kalendertagen aufgezeichnet werden. Dazu gehören klare Zuständigkeiten, Erinnerungen im Team und eine Regel für Ausfälle wie Krankheit oder Urlaub. Die Verantwortung bleibt beim Arbeitgeber, auch wenn die Beschäftigten selbst erfassen.

## Abwesenheiten: eigenes Recht

### Mitbestimmung beim Urlaub

Abwesenheitsmanagement und Team-Abwesenheitskalender fallen unter **§ 87 Abs. 1 Nr. 5 BetrVG**: allgemeine Urlaubsgrundsätze, Urlaubsplan und im Streitfall die zeitliche Lage des Urlaubs einzelner Personen. Das gilt zusätzlich zu Nr. 6. Regelt mindestens:

- ob Abwesenheitsmanagement und Teamkalender eingeschaltet sind, und auf welcher Stufe (`absenceCalendarVisibility`);
- die Abwesenheitsarten, welche eine Genehmigung brauchen, und wer entscheidet;
- wer die Abwesenheiten verwaltet (`absenceManagers`) und damit Krankheitstage sieht;
- ob Krankheitstage hier überhaupt eingetragen werden oder ob *Sonstiges* für die Planung reicht;
- Übertrag, Verfall und die Hinweise auf Urlaubsverfall (`expiryNotice`);
- ob der Abwesenheitsbericht und die Abwesenheitsquote je Person genutzt werden (`absenceReportsEnabled`, `absenceRateEnabled`);
- die Fristen für Abwesenheiten (`timeOffRetention`).

### Hinweispflicht, Verfall und Verjährung

- **Urlaub verfällt nur nach rechtzeitigem Hinweis.** BAG, Urteil vom 19.02.2019, 9 AZR 541/15, nach EuGH vom 06.11.2018, C-684/16 *Max-Planck* und C-619/16 *Kreuziger*. Hinata schickt diesen Hinweis einmal im Jahr an einem festen Tag (Standard 1. Oktober) und einige Wochen vor jeder Frist (Standard 6). Die Hinweise werden nie gelöscht.
- **Die Verjährung beginnt erst mit dem Hinweis.** BAG, Urteil vom 20.12.2022, 9 AZR 266/20. Deshalb bleibt das Urlaubsjournal, oder mindestens drei Jahre (§§ 195, 199 BGB).
- **Lange Krankheit: Verfall nach 15 Monaten.** Urlaub, der wegen Krankheit nicht genommen werden konnte, verfällt fünfzehn Monate nach dem Ende seines Urlaubsjahres (EuGH vom 22.11.2011, C-214/10 *KHS*; BAG, Urteil vom 20.12.2022, 9 AZR 245/19). Ob jemand die ganze Zeit wirklich nicht arbeiten konnte, ist eine Feststellung über einen Menschen. Hinata schlägt den Verfall nur vor. Die Abwesenheitsverwaltung bestätigt oder verwirft ihn, mit Begründung.

### Gesundheitsdaten

Ein Krankheitstag sagt etwas über die Gesundheit einer Person, und die schützt Art. 9 DSGVO besonders. Rechtsgrundlage ist Art. 9 Abs. 2 lit. b DSGVO i. V. m. § 22 Abs. 1 Nr. 1 lit. b BDSG.

- Hinata speichert keinen Grund und keine Diagnose, nur die Art und die Tage.
- Es gibt keinen Platz, um ein Attest hochzuladen. Seit 2023 ruft der Arbeitgeber die elektronische Arbeitsunfähigkeitsbescheinigung (eAU) nach § 109 SGB IV bei der Krankenkasse ab.
- Keine Benachrichtigung über eine Abwesenheit nennt ihre Art: nicht in der Glocke, nicht in der Mail, nicht auf dem Sperrbildschirm.
- Benennt ihr Personen für die Abwesenheitsverwaltung, sehen nur sie eine Krankheit als Krankheit. Organisationsadmins sehen dann nur, dass jemand abwesend ist. Ist niemand benannt, führen die Organisationsadmins die Abwesenheiten selbst und sehen sie vollständig.
- Nach 12 Monaten wird ein Krankheitstag ab Werk zu „abwesend (sonstiges)“ vergröbert.

!!! warning "Versteckt wird nur die Krankheit, nicht jede empfindliche Art"
    Eine Krankmeldung erscheint für entscheidende Personen als *Sonstiges*. Für jede andere Art gilt das nicht: Wer über einen Antrag entscheidet, liest den Namen der Art, und eine selbst angelegte Art (*Elternzeit*, *Kur*, eine Freistellung nach § 208 SGB IX) sagt damit etwas über die Person. Zwei Wege bleiben euch: Die Art braucht keine Genehmigung, dann entscheidet niemand über sie, oder ihr gebt ihr einen Namen, der nichts verrät. Regelt das, bevor ihr den Katalog erweitert.

!!! info "Wer erfährt, dass ein Urlaub kürzer wurde"
    Fällt eine Krankheit auf genehmigten Urlaub, bucht Hinata die überschnittenen Tage zurück und kürzt den Urlaub (§ 9 BUrlG). Die entscheidenden Personen erfahren, **dass** der Urlaub kürzer wurde, nie, warum. Der Grund bliebe sonst eine Gesundheitsangabe, die über eine Planungsmeldung ihren Weg zur Führungskraft fände.

### Was Hinata bei Abwesenheiten nicht tut

- Keine Lohnabrechnung. Hinata rechnet Tage, nie Urlaubsentgelt oder andere Beträge.
- Keine Krankheitsquote je Person, außer ihr schaltet ihre eigene Richtlinie ein (`absenceRateEnabled`), und dann nur für die Abwesenheitsverwaltung.
- Kein automatischer Verfall nach Krankheit.
- Kein Attest, kein Grund, keine Diagnose.

## Timer außerhalb der App

Seit dieser Version kann der Timer die Person auch außerhalb des App-Fensters erreichen:

- **Ende eines Intervalls:** eine System-Benachrichtigung, wenn ein Countdown oder ein Pomodoro-Intervall endet. Auf Android, iOS, macOS und Windows wird sie im Voraus geplant und kommt deshalb auch bei geschlossener App. Unter Linux und im Browser kommt sie, solange die App im Hintergrund läuft.
- **Laufender Timer:** auf Android eine stille Dauer-Benachrichtigung, deren Uhr das System weiterzählt. In einer installierten Web-App eine Markierung am App-Symbol.
- **Tab-Titel:** im Browser auf Wunsch die laufende Zeit im Tab-Titel. Nur die Zeit.

Menüleiste und Tray, Live Activity, Widgets auf Home- und Sperrbildschirm, Steuerelemente, Wecker und App-Kurzbefehle folgen in späteren Versionen.

- **Nur auf dem Gerät.** Die Flächen erheben nichts und senden nichts an den Arbeitgeber. Es gibt keine Telemetrie, und Ereignisse der Flächen werden nicht protokolliert. Wer den Timer aus einer Benachrichtigung stoppt, ruft dieselbe Route wie der Knopf in der App, und der Server kann beides nicht unterscheiden.
- **Allgemeine Texte.** Eine Benachrichtigung sagt, dass ein Intervall vorbei ist, nie, wofür. Sie verschwindet von selbst, wo das System das erlaubt (Android nach zehn Minuten, Linux nach einer Frist, der Browser von sich aus). Unter iOS und macOS behält das System sie in der Mitteilungszentrale, bis die Person sie löscht.
- **Ab Werk ohne Beschreibung.** Ein gesperrtes Android-Gerät zeigt nur den App-Namen. Details auf dem entsperrten Bildschirm und auf dem Sperrbildschirm sind zwei eigene Schalter, beide aus.
- **Sie verfallen.** Lokale Kopien enden spätestens 24 Stunden nach dem Start von selbst und verschwinden beim Abmelden und mit dem Konto.
- **Einzeln schaltbar.** Alles bleibt aus, bis die Person die Karte **Timer außerhalb der App** einmal bestätigt. Danach lässt sich jede Fläche unter **Einstellungen → Zeiterfassung** einzeln ausschalten. Das Panel **Wer sieht meine Zeitdaten?** zeigt, was auf diesem Gerät aktiv ist, und **Jetzt löschen** entfernt die lokalen Kopien sofort.

Empfehlung: Nehmt die Flächen als Funktionen des mitbestimmten Systems in die Checkliste der Betriebsvereinbarung auf.

**Geräte des Arbeitgebers oder verwaltete Geräte.** Auf einem verwalteten Gerät sieht die Geräteverwaltung installierte Apps und je nach Einrichtung auch deren gespeicherte Daten. Regelt in der Vereinbarung, dass die Geräteverwaltung nicht genutzt wird, um Zeitdaten zu lesen. Mit den Standardwerten enthalten die lokalen Kopien keine Beschreibung.

**Live Activity per Push aktualisieren (geplant, später).** Eine Live Activity im Hintergrund zu aktualisieren, braucht Push. Bevor das kommt, nehmt es ins VVT auf. Unterauftragsverarbeiter sind das Gateway [Hinata Connect](/de/connect-gateway.html), Google Firebase Cloud Messaging und der Apple Push Notification Service. Bewertet die Übermittlung in Drittländer nach dem EU-US Data Privacy Framework oder Standardvertragsklauseln.

**Wecker (geplant).** Wecker über Apples AlarmKit (iOS und iPadOS 26) durchbrechen den Stummmodus. Deshalb muss jede Person sie ausdrücklich selbst einschalten.

**App-Kurzbefehle (geplant).** Die gesprochenen Sätze von App-Kurzbefehlen wertet Apple auf seiner Seite aus, ohne Hinata zu sagen, wer was gesagt hat. Hinata bekommt nur die Aktion, die daraus folgt.

## Keine Rechtsberatung

Diese Seite ist eine sorgfältige Einordnung, aber keine Rechtsberatung. Die Rechtslage zur Arbeitszeiterfassung ändert sich gerade. Was für deine Organisation gilt, hängt von Branche, Tarifbindung, Beschäftigtengruppen und euren Vereinbarungen ab.

Software allein ist nie „rechtssicher“. Rechtmäßig wird eine Verarbeitung erst durch die Entscheidungen, die du damit triffst. Betriebs- oder Dienstvereinbarung, Datenschutz-Folgenabschätzung und Verzeichnis von Verarbeitungstätigkeiten sind Aufgaben des Betreibers. Hol dir für die Einführung fachkundigen Rat, zum Beispiel von deiner oder deinem Datenschutzbeauftragten und aus dem Arbeitsrecht.

Stand: 11.10.2026.

## Quellen

- [Datenschutz-Grundverordnung (EU) 2016/679](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679), Art. 4, 5, 6, 9, 12 bis 22, 30, 32, 35, 36 und 88
- [§ 22 BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__22.html), [§ 26 BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__26.html)
- [EuGH, Urteil vom 30.03.2023, C-34/21](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62021CJ0034)
- [BAG, Urteil vom 08.05.2025, 8 AZR 209/21](https://www.bundesarbeitsgericht.de/entscheidung/8-azr-209-21/)
- [EuGH, Urteil vom 14.05.2019, C-55/18 *CCOO*](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62018CJ0055)
- [BAG, Beschluss vom 13.09.2022, 1 ABR 22/21](https://www.bundesarbeitsgericht.de/entscheidung/1-abr-22-21/)
- [EuGH, Urteile vom 06.11.2018, C-684/16 *Max-Planck*](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62016CJ0684) und [C-619/16 *Kreuziger*](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62016CJ0619)
- [BAG, Urteil vom 19.02.2019, 9 AZR 541/15](https://www.bundesarbeitsgericht.de/entscheidung/9-azr-541-15/)
- [EuGH, Urteil vom 22.11.2011, C-214/10 *KHS*](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62010CJ0214)
- [BAG, Urteile vom 20.12.2022, 9 AZR 266/20](https://www.bundesarbeitsgericht.de/entscheidung/9-azr-266-20/) und [9 AZR 245/19](https://www.bundesarbeitsgericht.de/entscheidung/9-azr-245-19/)
- [§ 3 ArbSchG](https://www.gesetze-im-internet.de/arbschg/__3.html)
- [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html), [§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html), [§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html), [§ 16 ArbZG](https://www.gesetze-im-internet.de/arbzg/__16.html)
- [§ 17 MiLoG](https://www.gesetze-im-internet.de/milog/__17.html), [§ 21 MiLoG](https://www.gesetze-im-internet.de/milog/__21.html)
- [§ 2a SchwarzArbG](https://www.gesetze-im-internet.de/schwarzarbg_2004/__2a.html), [§ 8 SGB IV](https://www.gesetze-im-internet.de/sgb_4/__8.html), [§ 109 SGB IV](https://www.gesetze-im-internet.de/sgb_4/__109.html)
- [BUrlG](https://www.gesetze-im-internet.de/burlg/), [§ 195 BGB](https://www.gesetze-im-internet.de/bgb/__195.html), [§ 199 BGB](https://www.gesetze-im-internet.de/bgb/__199.html)
- [§ 147 AO](https://www.gesetze-im-internet.de/ao_1977/__147.html), [§ 257 HGB](https://www.gesetze-im-internet.de/hgb/__257.html)
- [§ 87 BetrVG](https://www.gesetze-im-internet.de/betrvg/__87.html), [§ 80 BPersVG](https://www.gesetze-im-internet.de/bpersvg_2021/__80.html)
- [BMAS: Arbeitszeitgesetz](https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/arbeitszeitgesetz.html) (der Referentenentwurf vom 18.06.2026 ist dort nicht veröffentlicht)
- [DSK: Liste der Verarbeitungstätigkeiten, für die eine DSFA durchzuführen ist (Version 1.1)](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf)

## Nächste Schritte

- Wie Personen Zeit erfassen, steht unter [Zeit erfassen](/de/guide-time.html).
- Jede Richtlinie mit ihrem Standard: [Zeiterfassung verwalten](/de/admin-time-tracking.html).
- Die technischen Schutzmaßnahmen beschreibt das [Sicherheitsmodell](/de/security.html).
