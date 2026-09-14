---
title: Benachrichtigungen
description: Mitteilungen in der App, per E-Mail und per Push, pro Ereignis einstellbar.
---

# Benachrichtigungen

Hinata informiert über drei Kanäle. Jede Person legt selbst fest, welche Ereignisse sie wo erreichen.

## Kanäle

- **In-App**: ein Mitteilungscenter in der App, das sich sofort aktualisiert, wenn etwas passiert.
- **E-Mail**: Versand über das [SMTP-Relay](/de/email.html) deines Servers. Mails zu Zuweisungen oder Erwähnungen enthalten einen Deep Link, der den passenden Vorgang direkt in der App öffnet.
- **Push**: auf Android, iOS, macOS und Windows, zugestellt über das [Hinata Connect Gateway](/de/connect-gateway.html). So kann eine veröffentlichte App die Nutzer jedes selbst gehosteten Servers erreichen, ohne dass jeder Server eigene Zugangsdaten für Firebase braucht.

!!! info "E-Mail braucht ein echtes Relay"
    Mitteilungen in der App funktionieren sofort. Damit Mails wirklich ankommen, auch Links zur Verifizierung und zum Zurücksetzen des Passworts, braucht der Server ein konfiguriertes SMTP-Relay. Siehe [E-Mail & SMTP](/de/email.html).

## Was eine Benachrichtigung auslöst

Typische Ereignisse:

- **Zuweisung**: Dir wird ein Vorgang zugewiesen.
- **Erwähnungen**: Jemand erwähnt dich per `@` in einer Beschreibung oder einem Kommentar.
- **Kommentare**: Neue Aktivität an einem Vorgang, an dem du beteiligt bist.
- **Statusänderungen**: Ein Vorgang, dem du folgst, wechselt im Workflow den Status.
- **Sprintereignisse**: Start und Abschluss von Sprints und damit verbundene Änderungen an der Planung.
- **Einladungen**: Du wirst in den Workspace oder ein Team eingeladen.
- **Sicherheit**: Anmeldungen und Ereignisse zur Kontosicherheit. Sie sind immer aktiv und lassen sich nicht stummschalten.

## Die Benachrichtigungsmatrix

Unter **Einstellungen → Benachrichtigungen** hat jede Person eine Matrix: eine Zeile pro Ereignis, eine Spalte pro Kanal.

- Zwei Hauptschalter schalten E-Mail und Push komplett ein oder aus.
- Die Matrix regelt den Rest. Zum Beispiel: Mails zu Kommentaren aus, Mails zu Erwähnungen an. Oder Push für Zuweisungen, aber nicht für Zusammenfassungen.

!!! tip "Einmal einstellen, dann vergessen"
    Neue Teammitglieder sollten beim Onboarding dreißig Sekunden in ihre Matrix stecken. Wer gut eingestellte Benachrichtigungen hat, vertraut dem Tool. Wer das nicht tut, schaltet es oft ganz stumm.

Benachrichtigungen zur Sicherheit sind fest aktiviert. Ereignisse zur Kontosicherheit erreichen dich also immer.

## Nächste Schritte

- Zustellung konfigurieren: [E-Mail & SMTP](/de/email.html) und das [Connect Gateway](/de/connect-gateway.html).
- Verwalte deine eigenen Einstellungen unter [Konto & Einstellungen](/de/authentication.html).
