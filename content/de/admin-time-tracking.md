---
title: Zeiterfassung verwalten
description: Erweitertes Time-Tracking, Abwesenheitsmanagement und Abrechnung einschalten und jede Richtlinie mit Wirkung, Sichtbarkeit, Mitbestimmung und Standard einstellen.
---

# Zeiterfassung verwalten

Diese Seite richtet sich an Organisationsadmins und Betreiber. Sie beschreibt die drei Modulschalter, jede Richtlinie der Zeiterfassung mit ihrem Standard, die Aufbewahrung, Feiertage, Abrechnung und die MCP-Werkzeuge.

Warum jede Einstellung rechtlich zählt, steht unter [Zeiterfassung: Datenschutz & Recht](/de/time-tracking-privacy.html). Wie Personen Zeit erfassen, steht unter [Zeit erfassen](/de/guide-time.html).

!!! info "Feature-Flag"
    Die erweiterte Zeiterfassung erscheint nur, wenn sie eingeschaltet ist. Organisationsadmins schalten sie unter **Organisation → Zeiterfassung** ein. Administratoren sehen unter **Adminbereich → Plattform → Plattform-Verhalten**, ob sie an ist. Der Standard kommt aus `HINATA_TIME_TRACKING_ADVANCED_ENABLED` (`false`). Eine Änderung wirkt ohne Neustart.

## Wer was einstellt

- **Organisationsadmins** (`ORG_ADMIN`) stellen die Modulschalter und alle Richtlinien auf der Seite [Organisation](/de/organization.html) unter **Zeiterfassung** ein.
- **Administratoren** (`ADMIN`) wählen unter **Adminbereich → Allgemein** die Feiertagsregion. Unter **Adminbereich → Plattform** sehen sie nur, ob die erweiterte Zeiterfassung an ist. Sind sie auch Organisationsadmin, führt die Zeile sie dorthin.
- **Die Umgebung des Servers** liefert die Standardwerte (`HINATA_TIME_TRACKING_*`). Jede Richtlinie darf leer bleiben. Dann steht dort **Env-Default**, und die Umgebung entscheidet. Ein gespeicherter Wert gewinnt. **Env-Default übernehmen** leert ihn wieder.
- Jede Änderung an den Richtlinien und am Sperrdatum steht im Audit-Protokoll (`TIME_POLICY_CHANGED`, `TIME_LOCK_CHANGED`).

## Die Module

### Erweitertes Time-Tracking

- Schalter **Erweitertes Time-Tracking** (`advancedEnabled`), Standard aus.
- Bringt Timer, die Kalenderansicht, Freigaben, Verfügbarkeit, Berichte und Abrechnung.
- Aus: Der bisherige Stundenzettel bleibt genau so, wie er ist, und die Endpunkte des Moduls gibt es für die Apps nicht. Ausschalten blendet das Modul aus und löscht nichts.
- Umgebung: `HINATA_TIME_TRACKING_ADVANCED_ENABLED=false`. Die App liest das Client-Flag `advanced_time_tracking`.

### Abwesenheitsmanagement

- Schalter **Abwesenheitsmanagement** (`absenceManagementEnabled`), Standard aus. Client-Flag `absence_management`.
- Bringt Abwesenheitsarten, Jahresansprüche, Salden, Anträge und Krankmeldungen.
- Setzt die erweiterte Zeiterfassung voraus, weil jeder Tag, den es zählt, aus Arbeitszeitmustern, Feiertagskalendern und Kapazität kommt. Solange die erweiterte Zeiterfassung aus ist, behält der Schalter seine Stellung und wirkt nicht.
- Ausschalten verliert keine Daten. Arten, Ansprüche, Buchungen und Anträge bleiben. Abwesenheiten prägen weiter die Kapazität.
- Umgebung: `HINATA_TIME_TRACKING_ABSENCE_MANAGEMENT_ENABLED=false`.

### Abrechnung

- Schalter **Abrechnung** (`billingEnabled`), Standard aus. Client-Flag `billing`. Setzt die erweiterte Zeiterfassung voraus.
- Bringt Stundensätze mit Verlauf, Personalkosten, Abrechnungs- und Profitabilitätsberichte, Rechnungen und Gutschriften. Leitungen und Organisationsadmins sehen sie. **Stundensätze verwalten** öffnet die Sätze.
- Alle Beträge stehen in einer Währung (`currency`, Standard `EUR`). Rechnungsnummern sehen so aus: `INV-2026-00001`. Den Präfix setzt nur `HINATA_TIME_TRACKING_INVOICE_PREFIX`.
- Eine gestellte Rechnung ist eingefroren, und mit ihr die Einträge, die sie nennt. Der Rückweg ist eine Gutschrift (`INVOICE_CREDITED` im Audit-Protokoll). Sie gibt die Einträge für Korrekturen wieder frei.
- Gestellte Rechnungen und Gutschriften werden nie gelöscht (§ 147 AO, § 257 HGB). Ein Projekt mit einer davon lässt sich nicht löschen.

## Vier Grundsätze

Diese vier Regeln gelten für jede Richtlinie unten. Du kannst sie in der Vereinbarung zitieren.

1. **Hinata verhindert nie die Aufzeichnung geleisteter Arbeitszeit.** Feiertage, Wochenenden, Betriebsruhe und Abwesenheiten werden markiert, nicht gesperrt. Grundlage: BAG 13.09.2022, 1 ABR 22/21 und EuGH 14.05.2019, C-55/18 (CCOO); § 16 Abs. 2 ArbZG verlangt die Aufzeichnung der Arbeitszeit über die werktägliche hinaus, und dazu zählt nach herrschender Auslegung jede Arbeit an Sonn- und Feiertagen. § 9 ArbZG verbietet die Arbeit an Feiertagen, nicht ihre Dokumentation.
2. **Gesperrt wird ausschließlich die Vergangenheit, nie Gegenwart oder Zukunft.** Das Sperrdatum ist ein Integritätswerkzeug für abgeschlossene Zeiträume (Art. 32 DSGVO; Aufbewahrung § 16 Abs. 2 ArbZG / § 17 MiLoG, zwei Jahre), kein Steuerungsinstrument.
3. **Jede Unveränderlichkeit hat einen dokumentierten Rückweg.** Sperrdatum, Freigabe und Rechnung: mit Korrekturantrag, Reopen bzw. Gutschrift, immer mit Begründung im Audit. Ohne Rückweg kollidiert die Sperre mit Art. 16 DSGVO: Arbeitszeit ist ein personenbezogenes Datum, unrichtige Daten sind unverzüglich zu berichtigen.
4. **Verspätete Erfassung wird nie abgelehnt, höchstens kenntlich gemacht.** Nachträge sind bis zur Richtlinie `maxDaysBack` (Default 365 Tage) möglich, darüber hinaus über den Ausnahmeweg. Die Frist des § 17 Abs. 1 MiLoG (sieben Kalendertage in den Branchen des § 2a SchwarzArbG und bei geringfügig Beschäftigten, bußgeldbewehrt nach § 21 MiLoG) bleibt eine organisatorische Pflicht des Betreibers; Hinata unterstützt sie mit dem Selbst-Hinweis und erzwingt sie nicht.

## Richtlinienmatrix

Jede Richtlinie der Zeiterfassung, mit ihrem Standard aus dem Code. Nutze die Tabelle als Anlage zur Betriebs- oder Dienstvereinbarung. Ergänze eine Spalte mit eurem Wert und dem Grund.

Die Bewertung nach § 87 BetrVG obliegt in jeder Zeile den Betriebsparteien. Die Spalte nennt, worauf ihr schauen solltet. „Nr. 6“ heißt § 87 Abs. 1 Nr. 6 BetrVG. Im öffentlichen Dienst gilt das jeweilige Landespersonalvertretungsgesetz (LPVG), für den Bund § 80 Abs. 1 Nr. 21 BPersVG.

| Richtlinie | Wirkung | Wer sieht was | Mitbestimmung | Standard |
| --- | --- | --- | --- | --- |
| **Erweitertes Time-Tracking** (`advancedEnabled`) | Das Modul: Timer mit Start und Ende, Kalender, Freigaben, Verfügbarkeit, Berichte, Abrechnung. Erst damit werden Beginn und Ende der Arbeit einer Person zu Daten. | Hängt von den Zeilen darunter ab. | Einführung einer technischen Einrichtung, die objektiv zur Überwachung geeignet ist (Nr. 6). Vor dem Einschalten vereinbaren. | aus |
| **Abwesenheitsmanagement** (`absenceManagementEnabled`) | Abwesenheitsarten, Ansprüche, Salden, Anträge, Krankmeldungen. Setzt die erweiterte Zeiterfassung voraus. | Jede Person die eigenen. Die Abwesenheitsverwaltung alle. | § 87 Abs. 1 Nr. 5 BetrVG (Urlaubsgrundsätze, Urlaubsplan), zusätzlich zu Nr. 6. | aus |
| **Wer Abwesenheiten verwaltet** (`absenceManagers`) | Benannte Personen pflegen Arten, Ansprüche und Salden und entscheiden Anträge. | Sie sehen einen Krankheitstag als Krankheit. Sobald jemand benannt ist, sehen Organisationsadmins nur „abwesend“. | Wer Gesundheitsdaten bekommt (Art. 9 DSGVO), gehört in die Vereinbarung. | leer: Organisationsadmins verwalten |
| **Team-Abwesenheitskalender** (`absenceCalendarVisibility`) | Kolleginnen und Kollegen sehen sich gegenseitig abwesend: `OFF`, nur dass jemand weg ist (`BUSY_ONLY`), oder die Art (`TYPE`). Nur mit Abwesenheitsmanagement. | Krankheit immer nur als abwesend. Leitungen sehen die Kapazität als Summe, ab drei Personen. | Ein Urlaubsplan (§ 87 Abs. 1 Nr. 5 BetrVG). | `OFF` |
| **Projekt, Vorgang, Beschreibung, Tag erforderlich** (`requiredFields`) | Projekt, Vorgang, Beschreibung oder Tag müssen am Eintrag stehen. | Keine Änderung. | Inhalt der Aufzeichnung (Nr. 6). Verhaltensregeln können Nr. 1 berühren. | alle aus |
| **Gesperrt vor** (`lockBefore`) mit **Wieder geöffnete Zeiträume** (`lockExceptions`) | Einträge vor dem Tag sind für alle eingefroren, auch für Admins. Das Datum liegt nie in der Zukunft. Ein wieder geöffneter Zeitraum öffnet benannte Tage für alle, mit Begründung. | Zeitraum und Begründung sehen alle. | Regelt, wer Anfragen und Ausnahmen liest. | kein Sperrdatum, keine Zeiträume |
| **Erfassen bis** (`maxDaysBack`) | Schutz vor Tippfehlern. Ein älterer Tag wird abgelehnt und zeigt den Ausweg: eine Anfrage, dann öffnet ein Organisationsadmin die Tage für diese Person für zwei Wochen. | Anfrage und Öffnung stehen im Audit-Protokoll. | Teil des Systems (Nr. 6). | 365 Tage |
| **Hinweis auf späte Erfassung nach** (`lateEntryHintDays`) | Markiert einen Eintrag, der mehr als N Tage nach dem Arbeitstag erfasst wurde. Blockiert nichts. | Nur die Person. In keinem Bericht. | Teil des Systems (Nr. 6). | leer: kein Hinweis |
| **Rundung** (`rounding`) | Rundet Dauern in Berichten auf einen Schritt. Gespeicherte Minuten ändern sich nie. | Keine Änderung. | Regeln, wo Berichte in die Vergütung eingehen (Nr. 6). | keine Rundung, Schritt 15 Minuten |
| **Tags einschränken** (`limitTagAccess`) | Nur Organisationsadmins legen neue Tags an. | Keine Änderung. | Teil des Systems (Nr. 6). | aus |
| **Standardmäßig abrechenbar** (`defaultBillable`) | Neue Einträge sind zunächst abrechenbar. | Keine Änderung. | Teil des Systems (Nr. 6). | aus |
| **Kalender-Import** (`icsImportEnabled`) | Personen abonnieren ihren eigenen Kalender und übernehmen Termine als Einträge. Setzt `HINATA_ICS_SECRET` voraus. | Abos und Termine nur für ihre Besitzer. Ein übernommener Termin wird ein normaler Eintrag. | Regelt Freiwilligkeit und private Termine. | aus |
| **Leitungen sehen Einträge der Mitglieder** (`leadsSeeMemberEntries`) | Leitungen sehen einzelne Einträge, Verlauf und Stundenzettel-Zeilen ihrer Projektmitglieder und dürfen diese Einträge ändern. | Aus: Leitungen sehen nur Projektsummen. Ein: Sie sehen auch, an welchen Tagen diese Mitglieder abwesend sind (Urlaub oder Sonstiges, Krankheit nur als Sonstiges, nie eine Notiz), wenn das Mitglied in den letzten zwölf Monaten Zeit auf eines ihrer Projekte gebucht hat. | Vorgesetzte lesen einzelne Buchungen. Die Kernfrage jeder Vereinbarung (Nr. 6). | aus |
| **Stundenzettel-Freigaben** (`approvalsEnabled`) mit **Freigabe-Zeitraum** (`approvalPeriod`) | Personen reichen einen Zeitraum ein. Eine Leitung oder ein Organisationsadmin gibt ihn mit Notiz frei oder lehnt ihn ab. Braucht die Zeile darüber. | Wer freigibt, liest die Einträge des Zeitraums. | Regelt Rhythmus, freigebende Personen und Ablehnungen (Nr. 6). | aus, monatlich, Woche beginnt am Montag |
| **Auslastungsberichte** (`workloadReportsEnabled`) | Gebuchte Zeit gegen Kapazität, je Person. | Organisationsadmins und Projektleitungen. Eine Leitung nur für ihre eigenen Projekte. | Ein direkter Vergleich zwischen Menschen (Nr. 6). Zweck und Grenzen regeln. | aus |
| **Bericht „Abwesenheiten und Salden“** (`absenceReportsEnabled`) | Zahlen zu Abwesenheiten und Salden. Nur mit Abwesenheitsmanagement. | Alle die eigenen. Die Abwesenheitsverwaltung alle. Leitungen Summen über mindestens drei Personen ohne Krankheit, und nur, wenn sie die Einträge der Mitglieder sehen. | Nr. 5 und Nr. 6. | aus |
| **Abwesenheitsquote je Person** (`absenceRateEnabled`) | Der Anteil abwesender Tage je Person in diesem Bericht. | Nur die Abwesenheitsverwaltung, nie Leitungen. | Verhaltens- und Gesundheitsdatum: eine eigene Entscheidung (Nr. 6). | aus |
| **Budget-Warnungen** (`alertsEnabled`) | Leitungen eines Projekts und Admins seiner Teams bekommen eine Nachricht beim Warnanteil (80 %, sofern das Projekt keinen anderen setzt), bei 100 % und erneut bei 110, 125 und 150 % von Budget oder Schätzungen. Zugewiesene Personen bekommen eine, wenn ihr Vorgang seine Schätzung erreicht, ab 100 % auch die Leitungen. Im Projektmodus **Hinweis beim Erfassen** (Standard) sofort, im Modus **Nur stündliche Meldung** einmal je Stunde. Erfassen wird nie gesperrt. Der Hinweis im Formular an die erfassende Person erscheint auch, wenn diese Richtlinie aus ist. | Die Nachricht nennt Projekt oder Vorgang und Summen, nie eine Person. In kleinen Projekten kann sie trotzdem auf jemanden zeigen. | Regelt Schwellen und Empfänger (Nr. 6). | aus |
| **Ziel-Erinnerungen** (`targetRemindersEnabled`) mit **Vorgeschlagenes Tagesziel** (`suggestedDailyTargetMinutes`) und **Vorgeschlagenes Wochenziel** (`suggestedWeeklyTargetMinutes`) | Erinnert eine Person, wenn ihre eigene Zeit hinter ihrem eigenen Ziel liegt. Organisationsadmins können ein Ziel nur vorschlagen. | Nur die Person. Nicht protokolliert. | Ob und welches Ziel vorgeschlagen wird, gehört in die Vereinbarung. | aus, kein Vorschlag |
| **Arbeitszeit-Hinweise** (`arbzgHintsEnabled`) | Hinweise nach §§ 3, 5 und 9 ArbZG an den eigenen Einträgen. | Nur die Person. Nicht gespeichert. | Der Gesundheitsschutz kann Nr. 7 berühren. Teil des Systems (Nr. 6). | aus |
| **Abrechnung** (`billingEnabled`) mit **Währung** (`currency`) | Sätze, Personalkosten, Berichte, Rechnungen. Setzt die erweiterte Zeiterfassung voraus. | Leitungen und Organisationsadmins. Personalkostensätze können das Gehalt verraten. | Regelt, wer Kostensätze sieht (Nr. 6). | aus, `EUR` |
| **Aufbewahrung** (`retention`) | **Einträge löschen nach** (`entryPurgeMonths`) für alle. **Beschreibungen leeren nach** (`descriptionPurgeMonths`) für gelöschte Konten. | Bestimmt, wie weit zurück sich überhaupt etwas auswerten lässt. | Fristen gehören in die Vereinbarung und ins VVT. | 0 und 0: nichts wird gelöscht |
| **Aufbewahrung von Abwesenheiten** (`timeOffRetention`) | Vergröbert Krankheit, löscht abgeschlossene Anträge, auf Wunsch das Urlaubsjournal. | Wie im Abwesenheitsmanagement. | Fristen gehören in die Vereinbarung. | 12 Monate, 36 Monate, Journal bleibt |
| **Hinweise auf Urlaubsverfall** (`expiryNotice`) | Ein jährlicher Hinweis an einem festen Tag und einer einige Wochen vor jeder Frist. Ohne rechtzeitigen Hinweis verfällt kein Urlaub. | Die betroffene Person. Der Versand steht im Audit-Protokoll. | Teil der Urlaubsgrundsätze (Nr. 5). | 1. Oktober, 6 Wochen vorher |
| **Datenschutzhinweis** (`privacyNotice`) | Der Text vor der ersten Nutzung und unter **Einstellungen → Zeiterfassung**. | Alle. | Den Text in der Vereinbarung nennen. | leer: eingebaute Vorlage |
| **Feiertage der Plattform** (`region`) | Die Region, deren Feiertage die Organisation bekommt, jedes Jahr gefüllt. Stellen Administratoren ein. | Alle. Feiertage werden markiert, nie gesperrt. | Die Verteilung der Arbeitszeit kann Nr. 2 berühren. | automatisch, aus der Zeitzone |
| Audit-Ereignisse `TIME_ENTRY_CREATED`, `TIME_TIMER_STARTED`, `TIME_TIMER_STOPPED`, `TIME_TIMER_DISCARDED` und `MCP_TIMER_STARTED`, `MCP_TIMER_STOPPED`, `MCP_TIMER_DISCARDED` | Ein lückenloses Protokoll, wann jede Person Einträge angelegt und Timer gestartet oder gestoppt hat, also wann sie gearbeitet hat. | Die `TIME_`-Ereignisse: Organisationsadmins im Protokoll der Organisation. Die `MCP_`-Ereignisse: Administratoren unter **Adminbereich → Audit-Protokoll**. | Nur mit ausdrücklicher Regelung einschalten (Nr. 6). | aus |
| Timer außerhalb der App: System-Benachrichtigung am Intervallende und laufender Timer auf Android (seit dieser Version); Menüleiste und Tray, Live Activity, Widgets, Steuerelemente, Wecker (geplant) | Eine Funktion: der eigene Timer der Person auf ihrem eigenen Gerät. Gerätelokal. Erhebt nichts und sendet nichts an den Arbeitgeber. | Die Person und wer auf ihren Bildschirm schaut. | Teil des mitbestimmten Zeiterfassungssystems; in der Betriebs- oder Dienstvereinbarung als Funktion beschreiben; die Bewertung nach § 87 Abs. 1 Nr. 6 BetrVG obliegt den Betriebsparteien. | aus, bis die Person es einmal bestätigt |

!!! note "Was der Server über Timer-Aktionen festhält"
    Wo die Timer-Ereignisse im Audit-Protokoll eingeschaltet sind, speichert es zu jedem Eintrag IP-Adresse und User-Agent, wie bei jedem Audit-Eintrag. Ein Timer, der über eine Systemfläche gestartet wird, kommt beim Server an wie einer aus der App. Der Server kann die beiden nicht unterscheiden.

## Aufbewahrung

Gelöscht wird nachts, auch mit mehreren Serverinstanzen nur einmal. Jeder Lauf steht im Audit-Protokoll (`TIME_RETENTION_RUN`, `TIME_OFF_RETENTION_RUN`).

| Daten | Einstellung | Standard | Regel |
| --- | --- | --- | --- |
| Zeiteinträge | **Einträge löschen nach** (`entryPurgeMonths`) | 0, nie | Sonst mindestens 24 Monate. Nie in einem eingereichten oder freigegebenen Zeitraum, nie auf einer Rechnung. |
| Beschreibungen gelöschter Konten | **Beschreibungen leeren nach** (`descriptionPurgeMonths`) | 0, nie | Die Stunden bleiben. |
| Angaben zu Krankheit | **Krankheit vergröbern nach** (`sickDetailPurgeMonths`) | 12 Monate | Danach steht ein Krankheitstag als „abwesend (sonstiges)“ da, ohne Notiz. Tag und Saldo bleiben. |
| Abgeschlossene Anträge | **Abgeschlossene Anträge löschen nach** (`requestPurgeMonths`) | 36 Monate | Abgelehnte, zurückgezogene und stornierte. Genehmigte bleiben als Nachweis. |
| Urlaubsjournal | **Urlaubsjournal löschen nach** (`ledgerPurgeYears`) | 0, bleibt | Sonst mindestens 3 Jahre (§§ 195, 199 BGB). |
| Hinweise auf Urlaubsverfall | keine | nie gelöscht | Auch das Audit-Protokoll behält sie. Ein Verfall stützt sich auf sie. |
| Rechnungen und Gutschriften | keine | nie gelöscht | § 147 AO, § 257 HGB. |
| Audit-Protokoll | Servereinstellung `audit.retentionDays` | 365 Tage | Außer den Hinweisen auf Urlaubsverfall. |
| Marken von Erinnerungen | keine | 90 Tage | Sie enthalten keinen Inhalt. |
| Kalendertermine | keine | 30 Tage zurück bis 90 Tage voraus | Bei jedem Abruf ersetzt. |

!!! warning "Nichts wird gelöscht, bis du eine Frist wählst"
    Die Aufbewahrung der Einträge steht ab Werk auf `0`. § 16 Abs. 2 ArbZG und § 17 Abs. 1 MiLoG verlangen zwei Jahre, 24 Monate sind deshalb eine übliche Wahl. Danach gilt die Speicherbegrenzung (Art. 5 Abs. 1 lit. e DSGVO).

## Feiertage

- Administratoren wählen die Region unter **Adminbereich → Allgemein → Feiertage der Plattform**. Standard ist **Automatisch, aus der Zeitzone**. **Keine** legt keinen Kalender an.
- Aus der Region macht der Server einen Feiertagskalender und füllt jedes Jahr das laufende und das nächste Jahr, ohne Import (`HINATA_HOLIDAYS_AUTO_FILL=true`).
- Organisationsadmins können den Kalender umbenennen, seine Tage ändern, ihm eine andere Quelle geben oder ihn löschen. Siehe [Feiertage](/de/organization.html#feiertage).
- Ein Feiertag ist eine Markierung. Alle können an ihm weiter Zeit erfassen (Grundsatz 1).

## Die Datenschutzerklärung deiner Instanz

- Deine eigene Datenschutzerklärung muss das Modul Zeiterfassung abdecken. Verlinke sie unter **Adminbereich → Plattform → App-Versionen → Datenschutz-URL** (`privacyPolicyUrl`, Umgebung `HINATA_PRIVACY_POLICY_URL`).
- Hinata bringt einen Datenschutzhinweis für das Modul in neun Sprachen mit. Organisationsadmins ersetzen ihn im Feld **Datenschutzhinweis** (`privacyNotice`). Leer heißt: der eingebaute Text in der Sprache der Person.
- Den eingebauten Text kannst du als Vorlage für deine eigene Erklärung nehmen. Prüf ihn gegen eure Einstellungen: Er beschreibt die Standardwerte, und das Panel **Wer sieht meine Zeitdaten?** zeigt, was eingeschaltet ist.

## MCP

KI-Clients können den eigenen Timer der Person bedienen, ihre eigenen Einträge auflisten und ändern, ihre eigene Zeit summieren, ihr eigenes Urlaubskonto lesen und Urlaub beantragen. Sie lesen nie die Zeit anderer und entscheiden nie einen Antrag. Die Timer-Ereignisse über MCP (`MCP_TIMER_*`) sind ab Werk aus, wie die in der App. Details auf der Seite [MCP-Server](/de/mcp.html).

## Nächste Schritte

- Rechtlicher Hintergrund und Checklisten: [Zeiterfassung: Datenschutz & Recht](/de/time-tracking-privacy.html).
- Rollen und die Seite Organisation: [Organisation](/de/organization.html).
- Umgebungsvariablen: [Konfigurationsreferenz](/de/configuration.html).
