---
title: E-Mail zu Vorgang
description: Verwandle eingehende E-Mails per IMAP-Polling in Hinata-Vorgänge, vollständig zur Laufzeit im Adminbereich konfiguriert — kein Neustart erforderlich.
---

# E-Mail zu Vorgang

Hinata kann ein Postfach überwachen und jede eingehende Nachricht in einen Vorgang
verwandeln. Richte eine Support- oder Eingangsadresse auf ein IMAP-Postfach aus, und
jede ungelesene E-Mail wird zu einem neuen Vorgang im Projekt deiner Wahl — Betreff als
Titel, Textkörper als Beschreibung, Absender als Melder erfasst. Es ist die
**eingehende** Hälfte von Hinatas E-Mail-Geschichte; die **ausgehende** Hälfte
(Verifizierung, Passwort-Reset, Benachrichtigungen) wird auf der Seite
[E-Mail & SMTP](/de/email.html) behandelt.

!!! info "Zur Laufzeit konfiguriert, kein Neustart"
    Der E-Mail-Eingang wird im **Adminbereich** der App konfiguriert, und die
    Einstellungen liegen in **MongoDB**. Das Aktivieren, das Ändern des Postfachs oder
    das Umstellen des Zielprojekts greifen alle **ohne Neustart des Servers** — der
    Poller liest die aktuellen Einstellungen in jedem Zyklus.

## So funktioniert es

Der Server betreibt einen geplanten Poller. In jedem Zyklus liest er die aktuellen
Eingangseinstellungen und verbindet sich, wenn der Eingang aktiviert und ein Host sowie
ein Standardprojekt konfiguriert sind, über IMAP (oder IMAPS) mit dem Postfach, scannt
den gewählten Ordner nach **ungelesenen** Nachrichten, erzeugt aus jeder einen Vorgang
und markiert die Nachricht als **gelesen**, sodass sie nie zweimal importiert wird.

```text
geplanter Poll (respektiert dein Poll-Intervall)
        │
        ▼
aktiviert? Host + Standardprojekt gesetzt?  ── nein ──▶ nichts tun
        │ ja
        ▼
IMAP/IMAPS verbinden → Ordner öffnen (READ_WRITE)
        │
        ▼
UNSEEN-Nachrichten suchen
        │
        ▼
für jede: Vorgang im Standardprojekt erstellen, dann als SEEN markieren
```

Schlägt ein Poll fehl (Postfach nicht erreichbar, falsche Zugangsdaten), wird der Fehler
protokolliert und der nächste Zyklus versucht es einfach erneut — ein vorübergehender
Ausfall verliert nie eine E-Mail, weil ungelesene Nachrichten beim nächsten
erfolgreichen Poll abgeholt werden.

## Was erstellt wird

Jede importierte Nachricht wird zu einem Vorgang im **Standardprojekt**, das du
ausgewählt hast:

| Vorgangsfeld | Stammt aus |
| --- | --- |
| **Titel** | Der **Betreff** der E-Mail (oder `(no subject)`, falls leer), auf eine sichere Länge gekürzt |
| **Beschreibung** | Ein kurzer Header, der vermerkt, von wem er erstellt wurde, dann der Klartext-Textkörper der Nachricht (der HTML-Teil wird zu Text reduziert, falls kein Klartext-Teil existiert) |
| **Typ** | **Task** |
| **Melder** | Die E-Mail-Adresse des Absenders wird am Vorgang erfasst |

Da es ein normaler Vorgang ist, gilt sofort alles andere in Hinata: Er landet im
Standard-Workflow-Status des Projekts, erscheint auf Board und Backlog, kann zugewiesen,
mit Labels versehen, verlinkt und kommentiert werden und — wenn das Projekt mit Git
verbunden ist — Entwicklungsinformationen aufnehmen, sobald jemand seinen Schlüssel
referenziert.

!!! tip "Wähle ein dediziertes Eingangsprojekt"
    Richte den Eingang auf ein Projekt aus, das existiert, um rohe eingehende E-Mails zu
    empfangen (zum Beispiel ein *Support-Posteingang*). Eine Person triagiert jeden neuen
    Vorgang — weist ihn zu, setzt Typ und Priorität oder verschiebt ihn ins richtige
    Projekt — statt ungefilterte E-Mails auf einem aktiven Lieferboard landen zu lassen.

## Konfiguration

Öffne den **Adminbereich → E-Mail-Eingang** und gib die Postfachdetails an. Die
verfügbaren Einstellungen und ihre Standardwerte:

| Einstellung | Standard | Bedeutung |
| --- | --- | --- |
| **Aktiviert** | `false` | Hauptschalter für den Poller |
| **Host** | — | Hostname des IMAP-Servers |
| **Port** | `993` | IMAP-Port |
| **SSL** | `true` | IMAPS verwenden (implizites TLS); der Standardport dafür ist `993` |
| **Benutzername** | — | Postfach-Login |
| **Passwort** | — | Postfach-Passwort (write-only — wird von der API nie zurückgegeben) |
| **Ordner** | `INBOX` | Welcher Ordner gescannt wird |
| **Standardprojekt** | — | Das Projekt, das die erstellten Vorgänge empfängt |
| **Poll-Intervall** | `60` s | Mindestsekunden zwischen Postfach-Scans |

Der Eingang bleibt untätig, bis **Aktiviert** an ist **und** sowohl ein **Host** als auch
ein **Standardprojekt** gesetzt sind — so tut eine halbfertige Konfiguration nie etwas
Unerwartetes.

!!! warning "Verwende ein dediziertes Postfach"
    Jede **ungelesene** Nachricht im gewählten Ordner wird importiert und dann als gelesen
    markiert. Richte den Eingang auf ein Postfach aus, das nur diesem Zweck dient, nicht
    auf einen gemeinsam genutzten menschlichen Posteingang — sonst würden gewöhnliche
    ungelesene E-Mails in Vorgänge verwandelt und als gelesen markiert.

## Wie es ausgehendes SMTP ergänzt

Die beiden Richtungen sind unabhängig und werden separat konfiguriert:

- **Eingehend (diese Seite)** — IMAP-Polling, im Adminbereich (MongoDB) konfiguriert,
  verwandelt empfangene E-Mails *in* Vorgänge.
- **Ausgehend — [E-Mail & SMTP](/de/email.html)** — das SMTP-Relay, das Hinata nutzt, um
  Verifizierungs-, Passwort-Reset- und Benachrichtigungs-E-Mails zu *senden*.

Du kannst jede ohne die andere betreiben. Eine schreibgeschützte Statusseite sendet
vielleicht nur ausgehende E-Mails; eine Eingangsadresse nimmt vielleicht nur E-Mails
entgegen. Die meisten Produktiv-Deployments betreiben beide: SMTP, damit Nutzer ihre
E-Mails erhalten, und den Eingang, damit Support-Anfragen zu nachverfolgten Vorgängen
werden.

## Verwandte Seiten

- [E-Mail & SMTP](/de/email.html) — Konfiguration ausgehender E-Mails.
- [Adminbereich](/de/admin-area.html) — wo der Eingang zur Laufzeit konfiguriert wird.
- [Projekte & Teams](/de/projects-teams.html) — Auswahl und Triage des Eingangsprojekts.
- [Benachrichtigungen](/de/notifications.html) — wie Personen über neue Vorgänge informiert werden.
