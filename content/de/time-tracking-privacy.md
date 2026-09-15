---
title: Zeiterfassung: Datenschutz & Recht
description: Was die Zeiterfassung speichert, auf welcher Rechtsgrundlage und welche Richtlinie welche Auswertung erlaubt. Mit Checklisten für Betriebsvereinbarung, DSFA und VVT.
---

# Zeiterfassung: Datenschutz & Recht

Arbeitszeit ist ein personenbezogenes Datum. Wer sie erfasst, könnte damit auch Menschen überwachen.

Diese Seite richtet sich an dich als Betreiberin oder Betreiber einer Hinata-Instanz und an alle, die die Einführung mit dir vorbereiten: Betriebs- oder Personalrat, Datenschutzbeauftragte und Personalabteilung. Du erfährst, was das Modul speichert, auf welche Rechtsgrundlagen du dich stützen kannst, welche Einstellung welche Auswertung über Personen erlaubt und wie Betroffene ihre Rechte in der App wahrnehmen.

!!! warning "Keine Rechtsberatung"
    Diese Seite ordnet ein und liefert Arbeitsmaterial. Eine Beratung ersetzt sie nicht. Mehr dazu [am Ende der Seite](#keine-rechtsberatung).

## Wer verantwortlich ist

Hinata wird selbst gehostet. Verantwortlicher im Sinne von Art. 4 Nr. 7 DSGVO für alles, was auf einer Instanz liegt, ist ihr Betreiber, meist also der Arbeitgeber. Der Herausgeber der App sieht keine Zeitdaten (siehe [Datenschutzerklärung](/de/privacy-policy.html)).

Betriebsvereinbarung, Datenschutz-Folgenabschätzung und Verzeichnis von Verarbeitungstätigkeiten sind deshalb deine Dokumente. Hinata liefert die Einstellungen und die Funktionen für die Betroffenenrechte. Welche davon laufen, entscheidest du.

Jede Richtlinie, die eine Aussage über eine Person möglich macht, ist ab Werk aus. Nach einem Update bleibt die Zeiterfassung so, wie sie war, bis jemand bewusst etwas einschaltet. Die Richtlinien findest du im [Adminbereich](/de/admin-area.html) unter **Zeiterfassung**. Lässt du eine leer, gilt der Wert aus der Umgebung des Servers.

## Zweck und Datenkategorien

Das Modul zeichnet Arbeitszeit auf. Es dient den gesetzlichen Aufzeichnungspflichten und der Projektsteuerung. Wenn eingeschaltet, dient es auch der Freigabe von Stundenzetteln und der Abrechnung. Dafür speichert es:

| Kategorie | Inhalt | Anmerkung |
| --- | --- | --- |
| Zeiteinträge | Tag, Dauer, optional Start- und Endzeit, Projekt, Vorgang, Tätigkeitsart, Beschreibung, Tags, abrechenbar ja/nein, Quelle (App, Timer, Smart Commit, Kalender), `createdAt`, `updatedAt`, `updatedBy` | Der Kern. Ohne Start- und Endzeit ist ein Eintrag nur eine Dauer an einem Tag. |
| Laufender Timer | Startzeitpunkt und die Angaben für den späteren Eintrag | Höchstens einer je Person. Beim Stoppen wird er zum Eintrag. |
| Einreichungen und Freigaben | Zeitraum, Status (eingereicht, freigegeben, abgelehnt, zurückgezogen), wer wann entschieden hat, Notizen | Nur wenn Stundenzettel-Freigaben eingeschaltet sind. |
| Korrekturanfragen und Bitten um ältere Tage | Betroffener Eintrag oder Zeitraum, Begründung, Antwort mit Notiz, Zeitpunkte | Eigene Sammlung. Das Audit-Protokoll wiederholt sie (`TIME_CORRECTION_REQUESTED`, `TIME_BACKFILL_REQUESTED`, `TIME_CORRECTION_ANSWERED`). |
| Für eine Person geöffnete Tage | Zeitraum, wer geöffnet hat, Ablaufzeitpunkt, gegebenenfalls eine Nachricht | Schließen sich nach zwei Wochen von selbst und stehen im Audit-Protokoll (`TIME_BACKFILL_GRANTED`, `TIME_BACKFILL_REVOKED`). |
| Persönliche Einstellungen für den Timer | Zum Beispiel Länge von Pomodoros und Pausen | Am Konto gespeichert, nur für die Person selbst wichtig. |
| Kenntnisnahme des Datenschutzhinweises | Zeitpunkt (`timePrivacyAcknowledgedAt`) | Beleg, dass informiert wurde. Keine Einwilligung. |
| Arbeitszeiten | Geplante Minuten je Wochentag, der Tag, ab dem sie gelten, der gewählte Feiertagskalender, wer sie wann festgelegt hat | Planungsdaten. Ändert die Administration sie für eine andere Person, steht das im Audit-Protokoll (`AVAILABILITY_SCHEDULE_CHANGED`). |
| Abwesenheiten | Art (Urlaub, Krankheit, Sonstiges), erster und letzter Tag, halber Tag, optionale Notiz | Planungsdaten. Eine Abwesenheit hindert niemanden daran, Zeit zu erfassen. Ändert die Administration eine für eine andere Person, steht das ohne die Notiz im Audit-Protokoll (`AVAILABILITY_TIME_OFF_CHANGED`). |

!!! warning "Ein Krankheitstag ist ein Gesundheitsdatum"
    Die Abwesenheitsart *Krankheit* sagt etwas über die Gesundheit einer Person, und die schützt Art. 9 DSGVO besonders. Hinata speichert keinen Grund und keine Diagnose, nur die Art und die Tage. Regelt in der Vereinbarung, ob Krankheitstage hier überhaupt eingetragen werden oder ob *Sonstiges* für die Planung reicht.

!!! info "Warum die Kenntnisnahme keine Einwilligung ist"
    Im Arbeitsverhältnis ist eine Einwilligung wegen der Abhängigkeit selten freiwillig. Die Pflicht zur Arbeitszeiterfassung hängt ohnehin nicht von ihr ab. Der Klick auf **Verstanden** belegt deshalb nur, dass die Information nach Art. 13 DSGVO erfolgt ist. Wer nicht klickt, verliert dadurch kein Recht und gewinnt auch keins.

## Rechtsgrundlagen

### Datenschutzrecht

- **Art. 6 Abs. 1 lit. b DSGVO:** Durchführung des Arbeitsvertrags, etwa wenn Vergütung oder Überstundenausgleich von der erfassten Zeit abhängt.
- **Art. 6 Abs. 1 lit. c DSGVO:** Erfüllung einer rechtlichen Pflicht, hier der Pflicht zur Arbeitszeiterfassung (siehe unten).
- **Art. 6 Abs. 1 lit. f DSGVO:** berechtigte Interessen, etwa Projektsteuerung oder Abrechnung mit Kunden. Dafür brauchst du eine dokumentierte Abwägung. Betroffene können nach Art. 21 DSGVO widersprechen.
- **Art. 88 DSGVO i. V. m. § 26 Abs. 4 BDSG:** Betriebs- und Dienstvereinbarungen sowie Tarifverträge können spezifischere Vorschriften für den Beschäftigtendatenschutz sein. Das gilt nur, wenn sie Art. 88 Abs. 2 DSGVO erfüllen, also angemessene und besondere Maßnahmen zum Schutz der Beschäftigten enthalten.

!!! warning "§ 26 Abs. 1 S. 1 BDSG trägt nicht mehr"
    Der EuGH hat am 30.03.2023 entschieden (C-34/21): Nationale Regeln zum Beschäftigtendatenschutz, die Art. 88 Abs. 2 DSGVO nicht erfüllen, bleiben unangewendet, sofern sie nicht selbst eine Rechtsgrundlage nach Art. 6 Abs. 3 DSGVO sind. Das BAG hat daraus mit Urteil vom 08.05.2025 (8 AZR 209/21) gefolgert, dass § 26 Abs. 1 BDSG unangewendet bleibt. Stütze die Verarbeitung deshalb auf Art. 6 Abs. 1 DSGVO und, wo es sie gibt, auf eine Kollektivvereinbarung.

### Pflicht zur Arbeitszeiterfassung

- **EuGH, Urteil vom 14.05.2019, C-55/18 *CCOO*:** Die Mitgliedstaaten müssen Arbeitgeber verpflichten, ein objektives, verlässliches und zugängliches System einzurichten, das die tägliche Arbeitszeit jeder Person misst.
- **BAG, Beschluss vom 13.09.2022, 1 ABR 22/21:** In Deutschland folgt diese Pflicht schon aus § 3 Abs. 2 Nr. 1 ArbSchG, wenn man ihn unionsrechtskonform auslegt. Beginn und Ende der täglichen Arbeitszeit samt Überstunden sind zu erfassen. Ob ein elektronisches System eingeführt wird, kann der Betriebsrat nicht erzwingen. Wie es arbeitet, bestimmt er mit.
- **§ 16 Abs. 2 ArbZG:** Arbeitszeit über acht Stunden am Werktag ist aufzuzeichnen. Die Nachweise sind mindestens zwei Jahre aufzubewahren. Eine Frist für die Aufzeichnung nennt die Vorschrift nicht.
- **§ 17 Abs. 1 MiLoG:** Für geringfügig Beschäftigte (§ 8 Abs. 1 SGB IV) und in den Branchen aus § 2a SchwarzArbG (unter anderem Bau, Gastronomie, Personenbeförderung, Logistik, Gebäudereinigung, Fleischwirtschaft, Sicherheitsgewerbe) sind Beginn, Ende und Dauer der täglichen Arbeitszeit aufzuzeichnen. Das muss spätestens bis zum Ende des **siebten Kalendertags** nach dem Arbeitstag geschehen. Die Aufzeichnungen sind mindestens zwei Jahre aufzubewahren. Verstöße kosten nach § 21 Abs. 1 Nr. 8 MiLoG ein Bußgeld.
- **Referentenentwurf des BMAS zur Änderung des ArbZG vom 18.06.2026:** Er sieht unter anderem vor, die Arbeitszeit in der Regel noch am Tag der Arbeit aufzuzeichnen. Der Entwurf ist **nicht verabschiedet**. Bis ein Gesetz beschlossen ist, gilt die Rechtslage oben.

### Mitbestimmung

- **§ 87 Abs. 1 Nr. 6 BetrVG:** Der Betriebsrat bestimmt mit, wenn technische Einrichtungen eingeführt und angewendet werden, die dazu bestimmt sind, Verhalten oder Leistung zu überwachen. Nach ständiger Rechtsprechung des BAG reicht es, dass eine Einrichtung objektiv dazu geeignet ist. Eine Absicht zur Überwachung ist nicht nötig.
- **Öffentlicher Dienst:** Hier gilt das Personalvertretungsrecht. Für Dienststellen des Bundes ist das § 80 Abs. 1 Nr. 21 BPersVG, in den Ländern das jeweilige Landespersonalvertretungsgesetz (LPVG).

### Datenschutz-Folgenabschätzung

Die [Muss-Liste der Datenschutzkonferenz](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf) nennt unter Nr. 8 die umfangreiche Verarbeitung von Daten über das Verhalten von Beschäftigten, mit denen sich ihre Arbeit so bewerten lässt, dass Rechtsfolgen entstehen oder sie sonst erheblich beeinträchtigt werden.

Je mehr Auswertungen über Personen du einschaltest, desto eher brauchst du eine DSFA nach Art. 35 DSGVO. Prüf das mit der [DSFA-Checkliste](#dsfa-checkliste) und halte das Ergebnis fest. Das gilt auch, wenn du zu dem Schluss kommst, dass keine DSFA nötig ist.

## Richtlinienmatrix

Die Tabelle zeigt für jede Richtlinie, welche Auswertung über Personen sie möglich macht. Du kannst sie als Anlage zur Betriebsvereinbarung nutzen. Trag daneben ein, welchen Wert ihr gewählt habt und warum.

Die Bewertung nach § 87 BetrVG obliegt bei jeder Richtlinie den Betriebsparteien. Die Spalte „Mitbestimmung“ nennt, was darüber hinaus zu beachten ist.

| Richtlinie | Standard | Welche Auswertung über Personen sie ermöglicht | Mitbestimmung |
| --- | --- | --- | --- |
| **Erweitertes Time-Tracking** (`advancedEnabled`) | aus | Das Modul selbst: Timer mit Start- und Endzeit, Einreichungen, Korrekturanfragen und alle Richtlinien darunter. Erst damit werden Beginn und Ende der Arbeit einer Person zu Daten. | Das ist die Einführung einer technischen Einrichtung, die objektiv zur Überwachung geeignet ist (§ 87 Abs. 1 Nr. 6 BetrVG, im öffentlichen Dienst das Personalvertretungsrecht). Vereinbare sie vor dem Einschalten mit Betriebs- oder Personalrat. |
| **Leitungen sehen Einträge der Mitglieder** (`leadsSeeMemberEntries`) | aus | Aus: Leitungen sehen nie, wer was gebucht hat. An Vorgängen sehen sie wie alle anderen Mitglieder nur Tag, Dauer und Tätigkeit, und fremde Einträge ändern sie nicht. Berichte laufen je Projekt. Ein: Leitungen sehen die Einträge der Mitglieder, den Verlauf eines Eintrags, die Einträge hinter einer Einreichung und im Stundenzettel die Zeilen der Mitglieder von Projekten, die sie leiten. Diese Einträge dürfen sie dann auch ändern. Außerdem sehen sie, an welchen Tagen diese Mitglieder abwesend sind, sofern das Mitglied in den letzten zwölf Monaten selbst Zeit auf eines ihrer Projekte gebucht hat: Urlaub oder Sonstiges, nie eine Notiz, einen Krankheitstag nur als Sonstiges, nie die geplanten Stunden, und ändern können sie nichts davon. | Damit können Vorgesetzte einzelne Buchungen lesen. Das ist die Kernfrage jeder Vereinbarung. |
| **Stundenzettel-Freigaben** (`approvalsEnabled`) mit **Freigabe-Zeitraum** | aus, Rhythmus monatlich | Personen reichen einen Zeitraum ein. Eine Leitung oder ein Admin gibt ihn mit Notiz frei oder lehnt ihn ab. Wer freigibt, liest die Einträge der Person. Deshalb braucht es die Richtlinie darüber. Der Rhythmus bestimmt, wie eng geprüft wird. | Regelt Rhythmus, freigebende Personen und den Umgang mit Ablehnungen. |
| **Auslastungsberichte** (`workloadReportsEnabled`) | aus | Gebuchte Zeit gegen Kapazität je Person. Das ist ein direkter Vergleich zwischen Menschen. | Regelt Zweck, Empfänger und Grenzen der Nutzung ausdrücklich. |
| **Budget-Warnungen** (`alertsEnabled`) | aus | Leitungen bekommen eine Nachricht, wenn ein Projekt eine Schwelle gebuchter Zeit überschreitet. Das ist projektbezogen, lässt sich in kleinen Projekten aber auf Einzelne zurückführen. | Regelt Schwellen und Empfänger. |
| **Ziel-Erinnerungen** (`targetRemindersEnabled`) | aus | Eine Person wird erinnert, wenn ihre eigene gebuchte Zeit unter dem Soll liegt. Die Nachricht geht nur an sie selbst. | Niemand sonst bekommt einen Bericht. Wie das Soll entsteht, gehört trotzdem in die Vereinbarung. |
| **Arbeitszeit-Hinweise** (`arbzgHintsEnabled`) | aus | Hinweise nach §§ 3, 5 und 9 ArbZG auf den eigenen Einträgen, nur für die Person selbst. Nichts wird gespeichert oder weitergegeben. Siehe [ArbZG-Selbsthinweise](#arbzg-selbsthinweise). | Nur die allgemeine Bewertung (siehe oben). |
| `lateEntryHintDays` | leer, also kein Hinweis | Ein Eintrag zeigt „N Tage nach dem Arbeitstag erfasst“. Das sieht nur die Person selbst. In Berichten taucht es nicht auf. Siehe [Nachtragen](#nachtragen-was-möglich-ist-und-was-du-organisatorisch-sicherstellen-musst). | Nur die allgemeine Bewertung (siehe oben). |
| **Gesperrt vor** (`lockBefore`) und **Wieder geöffnete Zeiträume** | kein Sperrdatum | Einträge vor einem Stichtag sind für alle eingefroren. Ein Projekt kann ein eigenes, früheres Sperrdatum setzen. Eine Ausnahme öffnet einen benannten Zeitraum für alle. Die Begründung steht im Audit-Protokoll. Auf Anfrage öffnet die Administration Tage auch nur für eine Person, für zwei Wochen. Anfragen und Begründungen können Rückschlüsse auf Einzelne erlauben. | Regelt, wer Anfragen und Ausnahmen liest und wie lange sie bleiben. |
| `maxDaysBack` | 365 Tage | Schutz vor Tippfehlern. Ältere Tage werden abgelehnt, und die Meldung nennt den Weg über die Administration. Die kann die Tage für die Person öffnen. Anfrage und Öffnung werden mit Begründung protokolliert. | Nur die allgemeine Bewertung (siehe oben). |
| **Aufbewahrung** (`retention`) | 0 und 0, also keine automatische Löschung | Bestimmt, wie weit zurück überhaupt ausgewertet werden kann. Einträge löscht Hinata nie oder frühestens nach 24 Monaten. | Löschfristen gehören in die Vereinbarung und ins VVT. |
| **Kalender-Import** (`icsImportEnabled`) | aus | Personen abonnieren ihren eigenen Kalender und übernehmen Termine als Einträge. So werden Titel und Uhrzeiten der Termine zu Zeitdaten. | Regelt Freiwilligkeit und den Umgang mit privaten Terminen. |
| **Abrechnung** (`billingEnabled`) | aus | Sätze, Personalkosten, Abrechnungs- und Profitabilitätsberichte und Rechnungen. Leitungen und Admins sehen sie. Aus Personalkostensätzen lässt sich auf das Gehalt Einzelner schließen. | Regelt, wer Kostensätze sieht. |
| Ereignisse im Audit-Protokoll: `TIME_ENTRY_CREATED`, `TIME_TIMER_STARTED`, `TIME_TIMER_STOPPED`, `TIME_TIMER_DISCARDED` | aus | Ein lückenloses Protokoll, wann jede Person Einträge angelegt und Timer gestartet oder gestoppt hat, also von Beginn und Ende ihrer Arbeit. Weil so ein Protokoll objektiv zur Überwachung geeignet ist, sind diese Ereignisse ab Werk aus. | Nur mit ausdrücklicher Regelung einschalten. |

!!! note "Was das Audit-Protokoll immer festhält"
    Eingriffe in fremde Daten stehen immer im Audit-Protokoll: das Löschen eines fremden Eintrags, ein Eintrag für eine andere Person (`TIME_ENTRY_CREATED_FOR`, etwa per Smart Commit), Änderungen am Sperrdatum, wieder geöffnete Zeiträume, für eine Person geöffnete Tage, Korrekturanfragen und jeder Lauf der automatischen Löschung. Das schützt die Betroffenen, denn es hält fest, was mit ihren Daten passiert. Wann sie arbeiten, steht dort nicht.

## Checkliste Betriebs- oder Dienstvereinbarung

Eine Vereinbarung zur Zeiterfassung mit Hinata sollte mindestens diese Punkte klären:

- **Gegenstand und Geltungsbereich:** welche Instanz, welche Beschäftigten, welche Module. Leg die gewählten Werte als Anlage bei, am einfachsten die [Richtlinienmatrix](#richtlinienmatrix) mit einer Spalte „unser Wert“.
- **Zwecke:** abschließend aufzählen, etwa Aufzeichnungspflichten, Projektsteuerung und Abrechnung. Jede andere Nutzung, besonders zur Kontrolle von Verhalten oder Leistung, ausdrücklich regeln oder ausschließen.
- **Datenkategorien und Pflichtfelder:** ob Projekt, Vorgang, Beschreibung oder Tag Pflicht sind. Wie genau Beschreibungen sein sollen und was nicht hineingehört, zum Beispiel Gesundheitsangaben wie „Arzttermin“.
- **Sichtbarkeit:** wer wessen Einträge sieht (die Person selbst, Leitungen nur mit `leadsSeeMemberEntries`, die Administration) und wer Adminrechte bekommt. An Vorgängen sehen andere Mitglieder nur Tag, Dauer und Tätigkeit.
- **Freigaben:** ob Stundenzettel eingereicht werden, in welchem Rhythmus, wer freigibt und was bei Ablehnung und Wiederöffnen passiert.
- **Auswertungen und Benachrichtigungen:** Auslastungsberichte, Budget-Warnungen und Ziel-Erinnerungen, jeweils ein oder aus, mit Empfängern und Schwellen.
- **Timer und Audit-Protokoll:** ob Start- und Endzeiten erfasst werden und ob die Ereignisse zum Timer im Audit-Protokoll eingeschaltet werden dürfen (Standard: aus).
- **Korrekturen und Sperren:** Sperrdatum, Umgang mit Korrekturanfragen, wieder geöffneten Zeiträumen und für Einzelne geöffneten Tagen, Nachtragen (`maxDaysBack`, `lateEntryHintDays`).
- **Abrechnung:** ob Personalkostensätze hinterlegt werden und wer sie sieht.
- **Kalender-Import:** freiwillig, nur der eigene Kalender, Umgang mit privaten Terminen.
- **Aufbewahrung und Löschung:** konkrete Werte für `entryPurgeMonths` und `descriptionPurgeMonths` und der Umgang mit freigegebenen Zeiträumen.
- **Exporte und Schnittstellen:** wer CSV- oder Berichtsexporte zieht und wohin sie gehen. Zugriffe über die API haben dieselben Rechte wie die App. Nenn sie trotzdem.
- **Transparenz:** Text des Datenschutzhinweises (eingebaute Vorlage oder eigener Text) und Schulung für Leitungen und Administration.
- **Änderungen:** Bevor eine neue Version von Hinata oder eine Richtlinie eine neue Auswertung über Personen einschaltet, wird die Interessenvertretung informiert und erneut beteiligt. Änderungen an den Richtlinien stehen im Audit-Protokoll.
- **Kontrollrechte:** Einsicht der Interessenvertretung in Einstellungen und Audit-Protokoll, Auswertung der Erfahrungen nach einer festen Frist.
- **Folgen von Verstößen:** zum Beispiel, dass Daten, die entgegen der Vereinbarung ausgewertet wurden, nicht verwendet werden dürfen.
- **Laufzeit, Kündigung und Nachwirkung.**

## DSFA-Checkliste

- **Schwellwertprüfung festhalten:** DSK-Muss-Liste Nr. 8 und die Kriterien aus WP 248 Rev. 01, darunter systematische Überwachung, schutzbedürftige Betroffene und Bewerten oder Einstufen. Je mehr Zeilen der [Richtlinienmatrix](#richtlinienmatrix) eingeschaltet sind, desto eher ist eine DSFA nötig.
- **Systematische Beschreibung** (Art. 35 Abs. 7 lit. a DSGVO): Datenkategorien, Datenflüsse (App, Server, Mail, Push, Exporte), eingeschaltete Richtlinien mit ihren Werten und Empfänger.
- **Notwendigkeit und Verhältnismäßigkeit** (lit. b): Für jede eingeschaltete Richtlinie den Zweck nennen und begründen, warum ein milderes Mittel nicht reicht, etwa Projektsummen statt einzelner Buchungen. Datenminimierung: Pflichtfelder sparsam wählen, Start- und Endzeit nur, wo nötig.
- **Risiken für Betroffene** (lit. c): Kontrolle von Leistung und Verhalten, Profile aus Timerzeiten, Rückschlüsse aus Beschreibungen und Kalenderterminen (Gesundheit, Privates), Personalkostensätze, Exporte außerhalb des Systems, falsch vergebene Rollen, zu lange oder zu kurze Aufbewahrung.
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
| Bezeichnung der Verarbeitung | Arbeits- und Projektzeiterfassung mit Hinata | … |
| Zwecke (lit. b) | Erfüllung der Aufzeichnungspflichten (§ 3 Abs. 2 Nr. 1 ArbSchG, § 16 Abs. 2 ArbZG, ggf. § 17 MiLoG); Projektsteuerung; ggf. Freigabe von Stundenzetteln; ggf. Abrechnung mit Kunden | … |
| Rechtsgrundlagen | Art. 6 Abs. 1 lit. b, c und f DSGVO; ggf. Betriebs- oder Dienstvereinbarung nach Art. 88 DSGVO i. V. m. § 26 Abs. 4 BDSG | … |
| Kategorien betroffener Personen (lit. c) | Beschäftigte; ggf. Auszubildende, Leiharbeitskräfte, freie Mitarbeitende mit Konto | … |
| Kategorien personenbezogener Daten (lit. c) | Kontostammdaten; Zeiteinträge (Tag, Dauer, optional Start und Ende, Projekt, Vorgang, Tätigkeitsart, Beschreibung, Tags, abrechenbar, Quelle, Änderungsdaten); laufender Timer; Einreichungen und Freigaben mit Notizen; Korrekturanfragen, Bitten um ältere Tage und Antworten; für die Person geöffnete Tage; Einstellungen für den Timer; Zeitpunkt der Kenntnisnahme des Datenschutzhinweises | … |
| Empfänger (lit. d) | Die Person selbst; Administration; Leitungen nur bei eingeschalteter Richtlinie; andere Projektmitglieder nur Tag, Dauer und Tätigkeit an Vorgängen; ggf. Lohnbuchhaltung oder Kunden über Exporte; Dienstleister für Hosting und E-Mail als Auftragsverarbeiter | … |
| Übermittlung in Drittländer (lit. e) | Keine, wenn Server, Speicher und Mailserver in der EU laufen. Push-Benachrichtigungen gehen über das Gateway [Hinata Connect](/de/connect-gateway.html) und Firebase Cloud Messaging | … |
| Löschfristen (lit. f) | `entryPurgeMonths` (nie oder frühestens 24 Monate nach dem Tag des Eintrags), `descriptionPurgeMonths` für gelöschte Konten; Einträge in eingereichten oder freigegebenen Zeiträumen gesondert | … |
| Technische und organisatorische Maßnahmen (lit. g, Art. 32) | Verweis auf das [Sicherheitsmodell](/de/security.html): TLS, rollenbasierte Rechte, Sperrdatum, Audit-Protokoll, Ratenbegrenzung, Backups; Richtlinienwerte laut Anlage | … |
| DSFA | durchgeführt ja/nein, Datum, Ergebnis der Schwellwertprüfung | … |
| Letzte Überprüfung | Datum und Anlass (zum Beispiel neue Richtlinie eingeschaltet) | … |

## Betroffenenrechte in Hinata

### Information (Art. 12 bis 14 DSGVO)

Wer das Modul zum ersten Mal öffnet, sieht den Datenschutzhinweis einmal als Sheet. **Verstanden** schließt ihn und speichert den Zeitpunkt (`timePrivacyAcknowledgedAt`). Das belegt die Information und ist keine Einwilligung. Danach bleibt der Hinweis unter **Einstellungen → Zeiterfassung → Datenschutz** erreichbar.

Dort steht auch das Panel **„Wer sieht meine Zeitdaten?“**. Hinata berechnet es aus den Richtlinien, die gerade aktiv sind. Niemand pflegt es von Hand. Schaltest du zum Beispiel `leadsSeeMemberEntries` ein, steht dort sofort, dass Leitungen die Einträge sehen. Das Panel kann also nicht veralten. Es zeigt auch, was andere Mitglieder an einem Vorgang sehen: wie viel Zeit gebucht wurde, aber nicht, wer sie gebucht hat, und nicht die Beschreibung.

Die eingebaute Vorlage gibt es in neun Sprachen. Unter **Adminbereich → Zeiterfassung → Datenschutz und Aufbewahrung** kannst du sie im Feld **Datenschutzhinweis** durch deinen eigenen Text ersetzen, etwa mit einem Verweis auf eure Betriebsvereinbarung. Bleibt das Feld leer, gilt die Vorlage.

### Auskunft und Datenübertragbarkeit (Art. 15 und 20 DSGVO)

Der Datenexport des Kontos enthält auch die Zeitdaten: Zeiteinträge, laufenden Timer, Einreichungen, Korrekturanfragen und Bitten um ältere Tage samt Antworten, für die Person geöffnete Tage, Einstellungen für den Timer, den Zeitpunkt der Kenntnisnahme sowie die Arbeitszeiten und Abwesenheiten der Person.

Es gibt ihn als JSON über `GET /api/v1/me/export` und als PDF-Bericht, dessen Link per E-Mail kommt. Sehr lange Historien werden dort gekürzt. Ein Hinweis im Export verweist dann auf den CSV-Export.

Die eigenen Einträge als CSV bekommst du in der App unter **Einstellungen → Zeiterfassung** oder direkt über die API:

```bash
curl -H "Authorization: Bearer $HINATA_TOKEN" \
  -o meine-zeiten.csv \
  "https://api.track.example.com/api/v1/time/export.csv?from=2026-01-01&to=2026-06-30"
```

Die Datei ist UTF-8 mit BOM, Excel zeigt Umlaute also richtig an. Zellen, die mit einem Formelzeichen beginnen, werden entschärft, damit kein Tabellenprogramm sie ausführt. Der Export wird gestreamt und umfasst bis zu 100 000 Zeilen. Wie oft eine Person ihn abrufen kann, ist begrenzt. Laufen gerade viele Exporte gleichzeitig, bittet Hinata darum, es kurz darauf noch einmal zu versuchen. Der Export enthält nur die Einträge der Person, die ihn anfordert.

### Berichtigung (Art. 16 DSGVO)

Deine eigenen Einträge bearbeitest du selbst. Liegt ein Tag vor dem Sperrdatum oder in einem eingereichten Zeitraum, ist er eingefroren. Dann schickst du über **Korrektur anfragen** eine Begründung an die Person, die die Sperre aufheben kann. Beim Sperrdatum ist das die Administration, bei einem eingereichten Zeitraum die Projektleitung oder wer freigibt. Pro Eintrag geht das einmal am Tag.

Die Antwort kommt mit einer Notiz als Benachrichtigung. Du findest sie am Eintrag und in seinem Verlauf. Die Antwort allein ändert noch nichts. Ändern kannst du den Eintrag erst, wenn der Tag wirklich wieder offen ist. Dafür gibt es drei Wege:

- Bei einem eingereichten Zeitraum öffnet die Projektleitung die Einreichung wieder.
- Beim Sperrdatum öffnet die Administration den Tag nur für dich, direkt aus der Anfrage heraus mit **Tage öffnen**. Die Öffnung gilt zwei Wochen und steht im Audit-Protokoll. Schreibt die Administration etwas dazu, liest du es als Antwort.
- Soll ein Zeitraum für alle wieder offen sein, legt die Administration eine Ausnahme vom Sperrdatum an. Die Begründung steht im Audit-Protokoll.

Im Verlauf eines Eintrags sieht eine Projektleitung nur die Anfragen zu Einreichungen ihrer Projekte, weil nur diese an sie gerichtet sind. Anfragen zum Sperrdatum bleiben zwischen dir und der Administration.

### Löschung und Speicherbegrenzung (Art. 17 und Art. 5 Abs. 1 lit. e DSGVO)

Wird ein Konto gelöscht, entfernt Hinata das Konto, einen laufenden Timer, noch nicht freigegebene Einreichungen, die Anfragen der Person, die für sie geöffneten Tage sowie ihre Arbeitszeiten und Abwesenheiten. Im Verlauf von Einträgen steht danach kein Name mehr für sie, und die Texte ihrer Korrekturanfragen zeigt Hinata dort niemandem mehr.

Freigegebene Einreichungen bleiben, weil sie ein Geschäftsnachweis sind. Auch die Zeiteinträge bleiben, mit der Nutzer-ID als Pseudonym, weil die Stunden zum Nachweis des Projekts gehören.

!!! note "Pseudonym ist nicht anonym"
    Solange sich eine Nutzer-ID einer Person zuordnen lässt, bleiben die Einträge personenbezogene Daten (Art. 4 Nr. 5 DSGVO). Dafür gibt es die Fristen unten.

Die Aufbewahrung stellst du unter **Adminbereich → Zeiterfassung → Datenschutz und Aufbewahrung** ein:

- **Beschreibungen leeren nach** (`descriptionPurgeMonths`) leert nach N Monaten die Beschreibungen in den Einträgen gelöschter Personen und die Notizen an ihren Stundenzetteln. Stunden und Entscheidungen bleiben.
- **Einträge löschen nach** (`entryPurgeMonths`) löscht für alle Personen Einträge, die älter als N Monate sind. Einträge in einem eingereichten oder freigegebenen Zeitraum löscht Hinata nie. Erlaubt sind 0 für nie oder mindestens 24 Monate. Ein kleinerer Wert aus der Umgebung des Servers gilt als 24.

Die Löschung läuft nachts in Stapeln, auch mit mehreren Serverinstanzen nur einmal. Ein Lauf hat ein festes Zeitbudget. Wird er in dieser Zeit nicht fertig, macht der nächste Lauf dort weiter, wo er aufgehört hat. Jeder Lauf steht mit seinen Zählern im Audit-Protokoll (`TIME_RETENTION_RUN`), auch einer, der mit einem Fehler abbricht.

!!! warning "Standard ist 0: Es wird nichts automatisch gelöscht"
    Beide Fristen stehen ab Werk auf `0`. Hinata löscht also nichts, bis du dich bewusst für eine Frist entscheidest. Das ist Absicht: Eine Löschung lässt sich nicht rückgängig machen, und welche Frist passt, hängt von deiner Organisation ab.

Warum 24 Monate ein guter Ausgangspunkt sind: § 16 Abs. 2 ArbZG und § 17 Abs. 1 MiLoG verlangen beide, die Nachweise mindestens zwei Jahre aufzubewahren. Früher darfst du nicht löschen, deshalb nimmt Hinata keinen kleineren Wert an.

Danach gilt der Grundsatz der Speicherbegrenzung: Daten, die du für keinen Zweck mehr brauchst, musst du löschen. Andere Aufbewahrungspflichten, etwa für abgerechnete Leistungen, prüfst du gesondert.

!!! tip "Puffer für spät Nachgetragenes"
    Hinata zählt die Monate ab dem Tag des Eintrags. § 17 MiLoG zählt die zwei Jahre ab dem Zeitpunkt, der für die Aufzeichnung maßgeblich ist. Wenn bei euch oft spät nachgetragen wird, plan ein paar Monate Puffer ein.

### Keine automatisierten Entscheidungen (Art. 22 DSGVO)

Budget-Warnungen, Ziel-Erinnerungen, Arbeitszeit-Hinweise und Hinweise auf späte Nachträge sind nur Hinweise. Hinata sperrt oder bewertet niemanden automatisch und kürzt nichts. Was aus einem Hinweis folgt, entscheidet ein Mensch.

## ArbZG-Selbsthinweise

Mit **Arbeitszeit-Hinweise** (`arbzgHintsEnabled`, Standard: aus) zeigt Hinata einer Person an ihren eigenen Einträgen, wo sie an Grenzen des Arbeitszeitgesetzes stößt. Hinata rechnet dabei nur für die Person selbst und für höchstens 31 Tage. Es gibt vier Hinweise:

- Die Tagessumme liegt über 10 Stunden, der Höchstgrenze nach [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html).
- Zwischen dem Ende eines Arbeitstags und dem Beginn des nächsten liegen weniger als 11 Stunden Ruhezeit ([§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html)). Dafür braucht es Einträge mit Start- und Endzeit.
- Es gibt Einträge an einem Sonntag ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).
- Es gibt Einträge an einem Feiertag des Kalenders, nach dem sich die Person richtet ([§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html)).

Die Hinweise werden nicht gespeichert, nicht an Leitungen oder die Administration gegeben und nicht über mehrere Personen zusammengefasst. Sie helfen der Person selbst. Sie beweisen nicht, dass eure Arbeitszeiten dem ArbZG entsprechen, und sind kein Urteil. Das Gesetz kennt Ausnahmen, etwa für Sonntagsarbeit, von denen Hinata nichts wissen kann.

## Nachtragen: was möglich ist und was du organisatorisch sicherstellen musst

Hinata lehnt einen Nachtrag nie ab, nur weil er spät kommt. § 16 Abs. 2 ArbZG kennt keine Frist. Die Pflicht zur Aufzeichnung bleibt bestehen, bis aufgezeichnet ist, und eine späte Aufzeichnung ist besser als keine. Der EuGH verlangt in C-55/18 gerade, dass sich die tägliche Arbeitszeit tatsächlich messen lässt.

Mit `lateEntryHintDays` kannst du einen Hinweis einschalten (Standard: leer, also kein Hinweis). Ist ein Wert gesetzt, zeigt ein später erfasster Eintrag „N Tage nach dem Arbeitstag erfasst“. Das sieht nur die Person selbst, in keinem Bericht taucht es auf.

Die Schwelle ist einstellbar und nicht fest auf sieben Tage gesetzt. Die Frist von sieben Tagen aus § 17 MiLoG gilt nur für bestimmte Branchen und geringfügig Beschäftigte, und der Referentenentwurf vom 18.06.2026 könnte die Aufzeichnung am selben Tag zur Regel machen. Wo das MiLoG gilt, liegt `7` nahe.

`maxDaysBack` (Standard: 365) schützt vor Tippfehlern, damit etwa 2025 statt 2026 nicht unbemerkt durchgeht. Ältere Tage bietet die Datumsauswahl gar nicht erst an, und beim Speichern lehnt Hinata sie ab. Beide Stellen zeigen den Ausweg:

1. Die Person bittet mit einer Begründung darum, die Tage zu öffnen. Das geht direkt an der Meldung, in der Datumsauswahl oder unter **Einstellungen → Zeiterfassung → Ältere Tage anfragen**. Die Anfrage wird protokolliert.
2. Eine Administratorin oder ein Administrator öffnet die Tage für diese Person unter **Adminbereich → Zeiterfassung → Korrekturanfragen** mit **Tage öffnen**. Die Öffnung gilt zwei Wochen und nur für diese Person. Die Begründung der Administration liest die Person als Antwort, und sie steht im Audit-Protokoll. Unter **Für Personen geöffnete Tage** lässt sich eine Öffnung früher schließen.
3. Die Person trägt die Zeit nach.

!!! danger "Die MiLoG-Frist einzuhalten, bleibt deine Pflicht"
    Hinata unterstützt dich dabei, erzwingt aber nichts. Wo § 17 MiLoG gilt, musst du organisatorisch dafür sorgen, dass Beginn, Ende und Dauer innerhalb von sieben Kalendertagen aufgezeichnet werden. Dazu gehören klare Zuständigkeiten, Erinnerungen im Team und eine Regel für Ausfälle wie Krankheit oder Urlaub. Die Verantwortung bleibt beim Arbeitgeber, auch wenn die Beschäftigten selbst erfassen.

## Keine Rechtsberatung

Diese Seite ist eine sorgfältige Einordnung, aber keine Rechtsberatung. Die Rechtslage zur Arbeitszeiterfassung ändert sich gerade. Was für deine Organisation gilt, hängt von Branche, Tarifbindung, Beschäftigtengruppen und euren Vereinbarungen ab.

Software allein ist nie „rechtssicher“. Rechtmäßig wird eine Verarbeitung erst durch die Entscheidungen, die du damit triffst. Betriebs- oder Dienstvereinbarung, Datenschutz-Folgenabschätzung und Verzeichnis von Verarbeitungstätigkeiten sind Aufgaben des Betreibers. Hol dir für die Einführung fachkundigen Rat, zum Beispiel von deiner oder deinem Datenschutzbeauftragten und aus dem Arbeitsrecht.

## Quellen

- [Datenschutz-Grundverordnung (EU) 2016/679](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679), Art. 4, 5, 6, 12 bis 22, 30, 35, 36 und 88
- [§ 26 BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__26.html)
- [EuGH, Urteil vom 30.03.2023, C-34/21](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62021CJ0034)
- [BAG, Urteil vom 08.05.2025, 8 AZR 209/21](https://www.bundesarbeitsgericht.de/entscheidung/8-azr-209-21/)
- [EuGH, Urteil vom 14.05.2019, C-55/18 *CCOO*](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62018CJ0055)
- [BAG, Beschluss vom 13.09.2022, 1 ABR 22/21](https://www.bundesarbeitsgericht.de/entscheidung/1-abr-22-21/)
- [§ 3 ArbSchG](https://www.gesetze-im-internet.de/arbschg/__3.html)
- [§ 3 ArbZG](https://www.gesetze-im-internet.de/arbzg/__3.html), [§ 5 ArbZG](https://www.gesetze-im-internet.de/arbzg/__5.html), [§ 9 ArbZG](https://www.gesetze-im-internet.de/arbzg/__9.html), [§ 16 ArbZG](https://www.gesetze-im-internet.de/arbzg/__16.html)
- [§ 17 MiLoG](https://www.gesetze-im-internet.de/milog/__17.html), [§ 21 MiLoG](https://www.gesetze-im-internet.de/milog/__21.html)
- [§ 2a SchwarzArbG](https://www.gesetze-im-internet.de/schwarzarbg_2004/__2a.html), [§ 8 SGB IV](https://www.gesetze-im-internet.de/sgb_4/__8.html)
- [§ 87 BetrVG](https://www.gesetze-im-internet.de/betrvg/__87.html), [§ 80 BPersVG](https://www.gesetze-im-internet.de/bpersvg_2021/__80.html)
- [BMAS: Arbeitszeitgesetz](https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/arbeitszeitgesetz.html) (der Referentenentwurf vom 18.06.2026 ist dort nicht veröffentlicht)
- [DSK: Liste der Verarbeitungstätigkeiten, für die eine DSFA durchzuführen ist (Version 1.1)](https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf)

## Nächste Schritte

- Wie Personen Zeit erfassen, steht unter [Zeit erfassen](/de/guide-time.html).
- Die Richtlinien stellst du im [Adminbereich](/de/admin-area.html) ein.
- Die technischen Schutzmaßnahmen beschreibt das [Sicherheitsmodell](/de/security.html).
