---
title: Organisation
description: Die Rolle Organisationsadmin und die Seite Organisation mit Arbeitszeit, Freigaben, Abwesenheiten, Feiertagen, Abrechnung und Fristen.
---

# Organisation

In Hinata gibt es zwei Rollen für Aufgaben, die über einzelne Projekte hinausgehen. **Administratoren** betreiben die Plattform. **Organisationsadmins** kümmern sich um Arbeitszeit, Abwesenheiten und Abrechnung der ganzen Organisation. Die beiden Rollen sind unabhängig voneinander. Eine Person kann eine davon haben, beide oder keine.

## Zwei Rollen

| Rolle | Wofür sie da ist | Wo sie arbeitet |
| --- | --- | --- |
| **Administrator** (`ADMIN`) | Konten, Anmeldung und SSO, Servereinstellungen, E-Mail, Git und das Audit-Protokoll | [Adminbereich](/de/admin-area.html) |
| **Organisationsadmin** (`ORG_ADMIN`) | Arbeitszeit mit erweiterter Zeiterfassung, Stundenzettel-Freigaben, Abwesenheiten, Feiertagskalender, Zeit-Tags, Ausnahmen vom Sperrdatum, Abrechnung und der Standard für relative Fristen | Seite **Organisation** in der App |

Beide Rollen vergibst du unter **Adminbereich → Benutzer**. Organisationsadmins haben keinen Zugang zum Adminbereich.

### Regeln für die Rolle Organisationsadmin

- Als Administrator kannst du dich nicht selbst zum Organisationsadmin machen. Das muss ein anderer Administrator tun. Diese Regel sorgt für Nachvollziehbarkeit, sie ist keine harte Sperre: Wer ein zweites Administratorkonto hat, kann sich die Rolle darüber trotzdem geben. Deshalb wird jede Vergabe im Audit-Protokoll festgehalten, und alle Organisationsadmins bekommen eine Benachrichtigung.
- Der letzte Organisationsadmin lässt sich nicht entfernen, deaktivieren oder löschen. Ernenne zuerst eine andere Person.
- Kommt jemand zur Rolle dazu oder gibt sie ab, bekommen alle Organisationsadmins eine Benachrichtigung.
- Jede Änderung an den Rollen Admin und Organisationsadmin landet im Audit-Protokoll. Das lässt sich nicht abschalten.

!!! info "Keine der beiden Rollen öffnet fremde Projekte"
    Ein Administrator sieht nur Projekte, Teams, Vorgänge, Boards, Seiten der Wissensdatenbank, Suchtreffer und Zeiteinträge, bei denen er selbst Mitglied ist, genau wie alle anderen. Die Plattform zu betreiben heißt nicht, die Arbeit anderer zu lesen. Auch Organisationsadmins sehen Projektinhalte nur über ihre eigene Mitgliedschaft. Zeiteinträge sehen sie dagegen alle, weil Freigaben, Korrekturen und Abrechnung das verlangen. Wie weit das geht, steht unten unter [Berichte und Exporte](#berichte-und-exporte).

## Die Seite Organisation

Als Organisationsadmin findest du in deinen **Einstellungen** die Zeile **Organisation**. Andere Personen sehen sie nicht. Dort liegt alles, was für die ganze Organisation gilt:

- **Zeiterfassung**: die erweiterte Zeiterfassung und ihre Richtlinien, etwa Rundung, Sperrdatum, Stundenzettel-Freigaben, Datenschutzhinweis und Aufbewahrung. Siehe [Datenschutz der Zeiterfassung](/de/time-tracking-privacy.html).
- **Abwesenheiten**: die Abwesenheitsverwaltung mit Arten, Ansprüchen und Konten, dazu die Personen, die sie mitführen dürfen.
- **Feiertage**: die Feiertagskalender, von Hand gepflegt oder aus einer Kalenderadresse importiert.
- **Zeit-Tags**, **Ausnahmen vom Sperrdatum** und für einzelne Personen geöffnete Tage.
- **Abrechnung**: Sätze, Kosten und Rechnungen.
- **Zählweise**: ob die Organisation in Kalendertagen oder Werktagen rechnet, für neue relative Fristen und als Standard für Benachrichtigungszeiten.
- **Protokoll**: die Einträge des Audit-Protokolls zu Arbeitszeit, Stundenzetteln und Abwesenheiten. Administratoren sehen sie nicht. Mehr dazu unter [Das Protokoll der Organisation](#das-protokoll-der-organisation).

Dazu kommen Aufgaben im Alltag: Organisationsadmins entscheiden Stundenzettel und Abwesenheitsanträge, wenn sonst niemand dafür da ist, öffnen gesperrte Tage auf Anfrage und dürfen Einträge für andere importieren.

## Krankmeldungen

Unter **Abwesenheiten** kannst du Personen nennen, die Abwesenheiten mitführen. Hast du solche Personen genannt, sehen nur sie eine Krankheit als Krankheit. Organisationsadmins sehen dann nur, dass jemand abwesend ist, aber nicht, warum. Ist niemand genannt, kümmern sich die Organisationsadmins selbst um die Abwesenheiten und sehen sie vollständig.

## Das Protokoll der Organisation

Das Protokoll auf der Seite Organisation zeigt Einträge zu Arbeitszeit, Stundenzetteln und Abwesenheiten. Einträge zu Abwesenheiten, also Anträge, Krankmeldungen und Konten, sieht dort nur, wer die Abwesenheiten führt. Das ist die benannte Abwesenheitsverwaltung oder, solange niemand benannt ist, die Organisationsadmins.

Welche dieser Ereignisse aufgezeichnet werden, legst du als Organisationsadmin für jedes Ereignis einzeln fest (über die API `PUT /api/v1/org/settings` mit `auditEvents`). Administratoren können diese Schalter nicht umlegen, und auch der Hauptschalter für das Audit-Protokoll der Plattform bringt diese Einträge nicht zum Schweigen.

## Berichte und Exporte

In Zeitberichten, Exporten, gruppierten Übersichten und bei der Freigabe von Stundenzetteln siehst du Stunden, Person und Projektschlüssel für alle. Vorgangstitel, Vorgangsschlüssel, Beschreibungen und Projektnamen siehst du nur bei Projekten, in denen du Mitglied bist, und bei deinen eigenen Einträgen. Die Suche in den Beschreibungen durchsucht nur Einträge, die du lesen darfst.

## Standard für relative Fristen

Mit eingeschalteten [Projektvorlagen](/de/project-templates.html) kann eine Frist als Versatz zum Termin des Projekts gelten, etwa „4 Wochen vorher“. Unter **Zählweise** legst du fest, ob die Organisation in **Kalendertagen** oder **Werktagen** rechnet. Das gilt für solche Fristen und zugleich als Standard für die [Benachrichtigungszeiten](/de/guide-notifications.html#wann-dich-etwas-erreicht): Bei Werktagen bekommt jede Person ohne eigene Wahl E-Mail und Push nur an Werktagen von 9 bis 17 Uhr, bei Kalendertagen jederzeit. Solange du nichts wählst, gilt der Standard des Servers, also Kalendertage (siehe `HINATA_PROJECT_TEMPLATES_DEFAULT_BASIS` in der [Konfigurationsreferenz](/de/configuration.html#projektvorlagen-und-relative-fristen)).

Jedes Projekt kann davon abweichen: beim Anlegen, beim Kopieren oder später in seinen Einstellungen unter **Fristen zählen in**.

Die Einstellung wählt nur vor, womit eine neue Frist startet. Bestehende Fristen behalten ihre eigene Zählweise und verschieben sich nicht.

## Nach dem Update

Damit nichts stehen bleibt, wird beim Update jeder bestehende Administrator einmalig auch Organisationsadmin. Alles funktioniert also wie vorher. Diese Übergabe steht für jede Person einzeln im Audit-Protokoll, und jede betroffene Person bekommt eine Benachrichtigung. Sollen die Rollen getrennt sein, nimmst du sie danach unter **Adminbereich → Benutzer** bewusst auseinander.

Bei einer neuen Installation bekommt die erste Person, die der [Einrichtungsassistent](/de/setup-wizard.html) anlegt, beide Rollen.

## Wie es weitergeht

- [Zeit erfassen](/de/guide-time.html): Arbeitszeiten, Abwesenheiten und Berichte aus Sicht der Nutzer.
- [Datenschutz der Zeiterfassung](/de/time-tracking-privacy.html): die Richtlinien im Einzelnen.
- [Adminbereich](/de/admin-area.html): was Administratoren verwalten.
