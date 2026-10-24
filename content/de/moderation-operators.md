---
title: Moderation für Betreiber
description: Für Admins und Betreiber. Was der Digital Services Act von einem Hinata-Server verlangt, was Hinata für jede Pflicht tut, die Jahreszahlen, Datenschutzhinweise, Mitbestimmung, Aufbewahrung und die Meldung an die Polizei.
---

# Moderation für Betreiber

Wer einen Hinata-Server betreibt, bietet nach dem Digital Services Act (DSA) einen Hostingdienst an, und in manchen Fällen eine Online-Plattform. Diese Seite sagt, welche Pflichten daraus folgen, was Hinata für jede davon tut und was bei dir bleibt. Sie ist keine Rechtsberatung. Wo dein Fall unklar ist, frag die Stelle, die deine Organisation rechtlich berät.

Wie Moderierende im Alltag arbeiten, steht unter [Moderation](/de/moderation.html). Die Einstellungen liegen unter [Adminbereich › Moderation](/de/admin-area.html#moderation).

## Hostingdienst oder Online-Plattform

Ein Hinata-Server speichert, was seine Mitglieder schreiben und hochladen, in ihrem Auftrag. Damit ist er ein **Hostingdienst** (Art. 3 Buchst. g Ziff. iii DSA).

Zur **Online-Plattform** wird er, wenn er diese Inhalte auch öffentlich verbreitet (Art. 3 Buchst. i und k). Braucht man zum Lesen ein Konto, gelten Inhalte nur dann als öffentlich, wenn jede Person, die fragt, automatisch hereinkommt, ohne dass ein Mensch entscheidet, wer zugelassen wird (Erwägungsgrund 14). In Hinata geht das auf zwei Wegen:

- Selbstregistrierung ohne Freigabe,
- ein SSO-Anbieter, der beim ersten Anmelden aktive Konten anlegt, ohne Freigabe und ohne Liste erlaubter E-Mail-Domains.

Eine Online-Plattform hat weitere Pflichten (Art. 20 bis 28), darunter ein Beschwerdesystem, die außergerichtliche Streitbeilegung und eigene Transparenzzahlen.

**Was das Update umgestellt hat:** Beim Update auf eine Version mit Moderation und bei jeder neuen Instanz schließt Hinata jeden dieser Wege, indem es die Freigabe einschaltet, und sagt allen Admins Bescheid. Wer einen Weg wieder öffnet, bestätigt das beim Speichern ausdrücklich. Solange einer offen ist, beginnt **Adminbereich › Moderation** mit **Wer hereinkommt** und sagt, was das bedeutet.

## Instanzen in einem Unternehmen oder Verein

Eine Instanz nur für die eigenen Beschäftigten oder Mitglieder, bei der ein Admin entscheidet, wer hereinkommt, ist eine geschlossene Gruppe. Ihre Inhalte sind nicht öffentlich, also ist sie keine Online-Plattform. Ob der DSA für ein Werkzeug, das nur den eigenen Leuten dient, überhaupt gilt, ist nicht abschließend geklärt. Hinata gibt dir in jedem Fall, was ein Hostingdienst braucht, so dass du die Frage nicht zuerst beantworten musst.

## Öffentliche Stellen

Kleinst- und Kleinunternehmen sind von den Jahreszahlen befreit (Art. 15 Abs. 2) und als Online-Plattform von den meisten Pflichten einer Plattform (Art. 19). Nach der Empfehlung der Kommission zur Definition der KMU (2003/361/EG, Anhang, Art. 3 Abs. 4) ist ein Unternehmen kein KMU, wenn öffentliche Stellen 25 % oder mehr seines Kapitals oder seiner Stimmrechte kontrollieren. Öffentliche Stellen selbst, etwa Verwaltungen, Hochschulen oder eine Studierendenschaft als Körperschaft des öffentlichen Rechts, bekommen diese Befreiungen deshalb nie:

- Sie veröffentlichen die Jahreszahlen (Art. 15).
- Ist ihre Instanz eine Online-Plattform, haben sie alle ihre Pflichten (Art. 20 bis 28), Art. 19 nimmt sie ihnen nicht ab.

## Deine Pflichten und was Hinata tut

| Pflicht | DSA | In Hinata |
| --- | --- | --- |
| Eine Kontaktstelle für Behörden | Art. 11 | **Adminbereich › Moderation › Kontakt für Meldungen**. Nenne die Sprachen, in denen du antwortest, im Impressum oder in den Hausregeln. |
| Eine Kontaktstelle für die Menschen, die den Dienst nutzen | Art. 12 | Derselbe Kontakt. Die App zeigt ihn unter **Einstellungen › Hilfe und Kontakt** und auf der Anmeldeseite, und `/api/v1/meta` veröffentlicht ihn ohne Anmeldung. |
| Ein gesetzlicher Vertreter in der EU | Art. 13 | Nur für Anbieter außerhalb der EU. |
| Bedingungen, die sagen, wie moderiert wird | Art. 14 | Die **Hausregeln**, in Fassungen, die sich nie mehr ändern, mit **So moderieren wir**, das der Server ergänzt. Alle stimmen zu, bevor sie schreiben. |
| Jahreszahlen | Art. 15 | Die [Jahreszahlen](#jahreszahlen) im Muster der Kommission, fertig zum Herunterladen. |
| Melde- und Abhilfeverfahren | Art. 16 | **Melden …** an jedem Inhalt und jedem Profil, das Formular für Menschen ohne Konto, eine Bestätigung guten Glaubens, eine Eingangsbestätigung und das Ergebnis für alle, die gemeldet haben. |
| Eine Begründung | Art. 17 | Jedes Entfernen und jede Sperre schickt der verantwortlichen Person eine Begründung, in der App und per E-Mail. |
| Der Verdacht einer Straftat gegen Leben oder Sicherheit | Art. 18 | Der Ablaufplan für Moderierende, der Vermerk **Strafverfolgung informiert** und die [Meldung an die Polizei](#meldung-an-die-polizei). |

Was Art. 20 von Online-Plattformen verlangt, bietet Hinata auf jeder Instanz: einen Widerspruch innerhalb von sechs Monaten, über den jemand entscheidet, der beim ersten Mal nicht entschieden hat.

## Dein Impressum

Ein digitaler Dienst, der in Deutschland geschäftsmäßig angeboten wird, braucht ein Impressum (§ 5 DDG). Trag die Adresse des Impressums deiner Organisation unter **Adminbereich › Moderation › Kontakt für Meldungen** ein. Die App verlinkt es dann unter **Einstellungen › Hilfe und Kontakt**, und die Hausregeln nennen es. Das Impressum selbst schreibt Hinata nicht für dich.

Das Impressum des Anbieters der App ist ein anderes, siehe [Impressum](/de/impressum.html).

## Bausteine für deine Datenschutzhinweise

Für alles, was die Moderation auf deinem Server verarbeitet, bist du verantwortlich. Das sagt auch die Datenschutzerklärung der App. Deine Datenschutzhinweise sollten abdecken:

- **Was verarbeitet wird:** Meldungen (Grund, Text, wer gemeldet hat, wann), Fälle (eine Kopie des gemeldeten Inhalts, die Entscheidung, die Begründung, der Verlauf), die Quarantäne entfernter Inhalte, Blockierungen, Zustimmungen zu den Hausregeln (Fassung und Zeitpunkt) und die Zähler für die Jahreszahlen, die keine Namen enthalten.
- **Rechtsgrundlagen:** Art. 6 Abs. 1 lit. c DSGVO in Verbindung mit Art. 16 bis 18 DSA für Meldungen, Begründungen und Meldungen an Behörden, und Art. 6 Abs. 1 lit. f DSGVO für einen sicheren Ort der Zusammenarbeit und die Durchsetzung der Hausregeln. Öffentliche Stellen können sich bei ihren Aufgaben nicht auf lit. f stützen (Art. 6 Abs. 1 Unterabs. 2) und nehmen lit. e mit der Vorschrift, die ihnen die Aufgabe gibt.
- **Der Schutz der Meldenden:** Die gemeldete Person erfährt nicht, wer gemeldet hat. Sie zu informieren würde den Zweck der Meldung vereiteln, deshalb gilt die Informationspflicht hier nicht (Art. 14 Abs. 5 lit. b DSGVO). In Deutschland schützt außerdem § 29 BDSG, was um eines Dritten willen geheim bleiben muss, auch bei einer Auskunft. Wer etwas über Kinder gemeldet hat, bleibt immer verdeckt.
- **Aufbewahrung:** wie unter [Aufbewahrung und Sicherungen](#aufbewahrung-und-sicherungen).
- **Die automatische Textprüfung:** Sie läuft auf deinem Server, nichts verlässt ihn. Solange **Unklare Fälle zur Moderation geben** an ist, liest der Server die Texte aller Mitglieder und meldet, was er findet, ohne dass jemand gemeldet hätte. Das ist eine systematische Überwachung: Mach vorher eine Datenschutz-Folgenabschätzung (Art. 35 DSGVO).

## Mitbestimmung

In einem Betrieb mit Betriebsrat können die Moderation und vor allem die automatische Textprüfung technische Einrichtungen sein, die dazu geeignet sind, Verhalten oder Leistung der Beschäftigten zu überwachen (§ 87 Abs. 1 Nr. 6 BetrVG). Dann muss der Betriebsrat vorher zustimmen, am besten in einer Betriebsvereinbarung. Im öffentlichen Dienst gilt das Personalvertretungsrecht des Bundes oder deines Landes. Aus diesem Grund fragt Hinata noch einmal nach, bevor **Unklare Fälle zur Moderation geben** angeht.

## Aufbewahrung und Sicherungen

Unter **Adminbereich › Moderation › Aufbewahrung und Zahlen** wählst du, ob erledigte Fälle 6 oder 12 Monate bleiben. Jede Nacht löscht Hinata, was abgelaufen ist: den Fall, seine Meldungen und die Quarantäne. Eine Entscheidung ohne Maßnahme bleibt 30 Tage, ein Fall, bei dem die Strafverfolgung informiert wurde, mindestens 12 Monate, und Moderierende können einen Fall länger halten, wenn eine Behörde ihn braucht. Die Einzelheiten stehen unter [Moderation](/de/moderation.html#aufbewahrung).

Deine Sicherungen überdauern das. Ein Snapshot behält, was er enthält, bis deine Aufbewahrung der Sicherungen ihn entfernt, und restic im Modus append-only kann keine einzelnen Fälle löschen. Schreib das in deine Datenschutzhinweise und halte die Aufbewahrung der Sicherungen kurz. Spielst du eine ältere Sicherung zurück, löscht der nächste nächtliche Lauf wieder, was inzwischen abgelaufen ist, denn jeder Fall trägt sein eigenes Löschdatum. Siehe [Backups & Upgrades](/de/backups.html).

## Hinter einem Reverse Proxy

Das Formular für Meldungen ohne Konto begrenzt, wie viele Meldungen eine Adresse schicken darf. Hinter einem Reverse Proxy sieht der Server nur die Adresse des Proxys, solange du `HINATA_TRUSTED_PROXIES` nicht setzt, und dann hält eine einzige Grenze alle gleichzeitig auf. **Adminbereich › Moderation** warnt einen Tag lang, wenn Anfragen über einen Proxy kommen, dem der Server nicht vertraut. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Jahreszahlen

**Adminbereich › Moderation › Aufbewahrung und Zahlen › Jahreszahlen … herunterladen** gibt dir ein ZIP mit einer CSV-Datei je Teil des Musters der Kommission (Durchführungsverordnung (EU) 2024/2835, Anhang I): Teile 1 bis 8 und 11. Die Teile 9 und 10 betreffen nur sehr große Plattformen. Frühere Jahre stehen zur Auswahl, sobald es für sie Zahlen gibt.

- **Der Zeitraum ist das Kalenderjahr.** Veröffentliche den Bericht spätestens zwei Monate nach seinem Ende, also bis Ende Februar (Art. 2 Abs. 3 der Durchführungsverordnung). Die Dateien sind maschinenlesbar, wie die Verordnung es verlangt: CSV nach RFC 4180, in UTF-8.
- **Gezählt wird beim Ereignis.** Jede Meldung, jede Entscheidung und jeder Widerspruch zählt in dem Moment, in dem er geschieht. Ein erledigter Fall ist nach einigen Monaten gelöscht, aus den Fällen ließen sich die Zahlen am Jahresende also nicht mehr lesen.
- **Keine Namen, keine Inhalte, keine Ranglisten.** Die Dateien enthalten Zahlen, Daten und die Namen, die das Muster selbst festlegt.
- **Leer oder null.** Eine Zelle bleibt leer, wenn sie auf einem Hinata-Server nicht zutreffen kann, etwa eine Herabstufung, die Hinata nie vornimmt. Eine Null heißt: Es hätte geschehen können, ist aber nicht geschehen.

Teil 1 füllt Hinata mit dem Namen des Dienstes (Hinata und deine Organisation), dem Anbieter (dem Betreiber unter **Kontakt für Meldungen**) und den Daten. Prüf die Zahlen vor dem Veröffentlichen und ergänze, was Hinata nicht wissen kann:

- **Teil 3**, Anordnungen von Behörden der Mitgliedstaaten (Art. 9 und 10). Hinata erfasst sie nicht.
- **Teil 11**, die qualitativen Angaben in deinen eigenen Worten, etwa wie viele Menschen moderieren und wie sie geschult sind.
- Was außerhalb von Hinata erledigt wurde, etwa eine Meldung per Brief.

### Wo Hinatas Gründe im Muster stehen

Das Muster hat eigene Kategorien. Hinata stellt jeden seiner acht Gründe in eine Kategorie und eine Unterkategorie, so dass die Unterkategorien sich zu ihrer Kategorie addieren. Wo das Muster für einen Grund keine Unterkategorie hat, steht er unter *Not captured by any other sub-category*, mit einer Beschreibung.

| Grund in Hinata | Meldungen (Teil 4) | Maßnahmen nach Gesetz (Teil 5) | Maßnahmen nach Hausregeln (Teil 6) |
| --- | --- | --- | --- |
| Belästigung, Beleidigung oder Hass | Cyber violence › Cyber harassment | ebenso | ebenso |
| Drohung oder Gewalt | Violence › Incitement to violence and hatred | ebenso | ebenso |
| Gefährdung von Kindern | Protection of minors › Child sexual abuse material | ebenso | ebenso |
| Private Daten ohne Zustimmung | Data protection and privacy violations › Missing processing ground | ebenso | ebenso |
| Spam, Betrug oder Schadsoftware | Scams and fraud › Other: *Spam, phishing and malicious files* | ebenso | ebenso |
| Sexuelle Inhalte | Kategorie von der meldenden Person nicht angegeben | Cyber violence › Non-consensual image sharing | Other violation of terms and conditions › Adult sexual material |
| Rechtsverletzung | Kategorie von der meldenden Person nicht angegeben | Intellectual property infringements › Other: *Copyright or another right of others* | wie Teil 5 |
| Etwas anderes | Kategorie von der meldenden Person nicht angegeben | nur in der Summe | Other violation of terms and conditions › Other: *Other breaches of the house rules* |

Texte, die die Textprüfung ablehnt, zählen in Teil 6 als Maßnahmen mit automatisierten Mitteln, unter dem Grund, den die Prüfung gefunden hat. Abgelehnte Uploads zählen dort als *Files of a type the instance does not accept*.

## Bilder mit bekanntem Missbrauchsmaterial abgleichen

Hinata vergleicht Bilder nicht mit bekannten Darstellungen des sexuellen Missbrauchs von Kindern und hat keinen Anschluss an einen Dienst, der das tut. Auf einer geschlossenen Instanz sieht sich ein Mensch jedes gemeldete Bild an. Ist deine Instanz halb offen, mit vielen Menschen, die niemand kennt, kannst du einen solchen Dienst selbst beantragen:

- **[Image Intercept](https://www.iwf.org.uk/our-technology/image-intercept)** der Internet Watch Foundation: kostenlos für kleinere Unternehmen, die die Bedingungen erfüllen, bis zu einer Million Prüfungen im Monat. Du meldest dein Interesse an, und die IWF prüft, ob du in Frage kommst. Der Abgleich läuft mit PhotoDNA und kryptografischen Hashes und darf nur dazu dienen, bekanntes Material zu erkennen, zu sperren und zu entfernen.
- **[Arachnid Shield](https://projectarachnid.com/en/)** des Canadian Centre for Child Protection: eine Schnittstelle ohne Kosten für Anbieter, mit einem Schlüssel nach der Anmeldung. Dienste mit vielen Uploads können stattdessen eine lokale Liste von Hashes beantragen.

In beiden Fällen baust du den Anschluss selbst oder lässt ihn bauen. Die Bilder oder ihre Hashes gehen an den Dienst, prüf ihn also vorher datenschutzrechtlich: einen Vertrag zur Auftragsverarbeitung, die Übermittlung ins Vereinigte Königreich oder nach Kanada und eine Datenschutz-Folgenabschätzung. Einen Treffer behandelst du wie eine Meldung über Kinder: entfernen, vermerken, melden, siehe den Ablaufplan unter [Moderation](/de/moderation.html#wenn-leben-oder-kinder-in-gefahr-sind).

## Meldung an die Polizei

Erfährt ein Hostingdienst von Informationen, die den Verdacht begründen, dass eine Straftat, die eine Gefahr für das Leben oder die Sicherheit einer Person darstellt, begangen wurde, begangen wird oder begangen werden könnte, informiert er sofort die Strafverfolgungs- oder Justizbehörden des betroffenen Mitgliedstaats (Art. 18 DSA). Der DSA nennt den sexuellen Missbrauch von Kindern unter den Beispielen (Erwägungsgrund 56).

In Deutschland nimmt das Bundeskriminalamt (BKA) diese Meldungen zentral entgegen (§ 13 DDG):

1. **Registriere dich, bevor du es brauchst.** Den Zugang zum Portal des BKA unter `https://u-entrance.bka.de` beantragst du per E-Mail an `U-Entrance@bka.bund.de`, mit der persönlichen Adresse der verantwortlichen Person oder einer neutralen Adresse des Teams. Das BKA bestätigt den Zugang per E-Mail.
2. **Das Portal nimmt keine Notrufe an.** Ist jemand jetzt in Gefahr, ruf 110.
3. **Was eine Meldung enthält:** ob eine Gefahr besteht, den Bereich (Terrorismus, Hasskriminalität, Sexualdelikte zum Nachteil von Kindern oder Sonstiges), das Konto oder Profil, dein Aktenzeichen, eine Beschreibung und die Uhrzeit in UTC.
4. **Bei Darstellungen des Missbrauchs von Kindern nennst du die Fundstelle und den Fall, nie das Material.** Niemand leitet es weiter. Der Inhalt bleibt in der Quarantäne, wo die Polizei ihn sichern kann, und **Strafverfolgung informiert** hält den Fall dafür lange genug.

Außerhalb Deutschlands frag die Polizei deines Landes oder deinen Koordinator für digitale Dienste, wohin solche Meldungen gehen.
