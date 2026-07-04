---
title: Benachrichtigungen
description: Bleib auf dem Laufenden mit In-App-, E-Mail- und Push-Benachrichtigungen — jede Nutzerin und jeder Nutzer stellt über eine ereignisbezogene Benachrichtigungsmatrix genau ein, was ankommt.
---

# Benachrichtigungen

Hinata hält alle informiert, ohne sie zu überfluten. Benachrichtigungen kommen über drei Kanäle, und jede Person entscheidet genau, welche Ereignisse sie erreichen und wo.

## Kanäle

- **In-App** — ein Live-Benachrichtigungscenter in der App, das aktualisiert wird, sobald etwas passiert.
- **E-Mail** — zugestellt über das [SMTP-Relay](/de/email.html) deines Servers. Handlungsrelevante E-Mails (eine Zuweisung, eine Erwähnung) enthalten einen Deep Link, der genau das passende Issue in der App öffnet.
- **Push** — mobile Push-Benachrichtigungen, zugestellt über das [Hinata Connect Gateway](/de/connect-gateway.html), sodass eine veröffentlichte App Nutzer jedes selbst gehosteten Servers benachrichtigen kann, ohne dass jeder Server eigene Firebase-Anmeldedaten besitzen muss.

!!! info "E-Mail braucht ein echtes Relay"
    In-App-Benachrichtigungen funktionieren sofort. Damit E-Mails tatsächlich zugestellt werden — einschließlich Verifizierungs- und Passwort-Zurücksetzen-Links — braucht der Server ein echtes konfiguriertes SMTP-Relay. Siehe [E-Mail & SMTP](/de/email.html).

## Was eine Benachrichtigung auslöst

Typische Ereignisse sind:

- **Zuweisung** — dir wird ein Issue zugewiesen.
- **Erwähnungen** — jemand erwähnt dich per `@` in einer Beschreibung oder einem Kommentar.
- **Kommentare** — neue Aktivität bei einem Issue, an dem du beteiligt bist.
- **Statusänderungen** — ein von dir verfolgtes Issue durchläuft den Workflow.
- **Sprint-Ereignisse** — Sprint-Start/-Abschluss und zugehörige Planungsänderungen.
- **Einladungen** — du wirst in den Workspace oder ein Team eingeladen.
- **Sicherheit** — Anmeldungen und Ereignisse zur Kontosicherheit (immer aktiv — diese kannst du nicht stummschalten).

## Die Benachrichtigungsmatrix

Unter **Einstellungen → Benachrichtigungen** erhält jede Person eine Matrix: eine Zeile pro Ereignistyp, eine Spalte pro Kanal. Zwei Hauptschalter aktivieren oder deaktivieren E-Mail und Push komplett, und die Matrix feinjustiert den Rest. Schalte Kommentar-E-Mails ab, behalte aber Erwähnungs-E-Mails; erhalte Push für Zuweisungen, aber nicht für Zusammenfassungen — ganz so, wie es zu deiner Arbeitsweise passt.

!!! tip "Einmal einstellen, dann vergessen"
    Ermutige neue Teammitglieder, während des Onboardings dreißig Sekunden in ihre Matrix zu investieren. Gut abgestimmte Benachrichtigungen sind der Unterschied zwischen einem Tool, dem Menschen vertrauen, und einem, das sie komplett stummschalten.

Sicherheitsrelevante Benachrichtigungen sind bewusst fest aktiviert, sodass Ereignisse zur Kontosicherheit dich immer erreichen.

## Nächste Schritte

- Zustellung konfigurieren: [E-Mail & SMTP](/de/email.html) und das [Connect Gateway](/de/connect-gateway.html).
- Verwalte deine eigenen Einstellungen unter [Konto & Einstellungen](/de/authentication.html).
