---
title: E-Mail zu Vorgang
description: Mach eingehende E-Mails per IMAP zu Vorgängen, eingestellt im Adminbereich und ohne Neustart.
---

# E-Mail zu Vorgang

Hinata kann ein Postfach überwachen und aus jeder ungelesenen E-Mail einen Vorgang
machen. Du richtest eine Support- oder Eingangsadresse auf ein IMAP-Postfach aus.
Jede neue Mail wird dann ein Vorgang im Projekt deiner Wahl:

- Betreff wird Titel.
- Text wird Beschreibung.
- Absender wird als Melder gespeichert.

Das ist der **eingehende** Teil. Ausgehende Mails (Verifizierung, Passwort-Reset,
Benachrichtigungen) erklärt [E-Mail & SMTP](/de/email.html).

!!! info "Zur Laufzeit konfiguriert, kein Neustart"
    Du stellst den E-Mail-Eingang im **Adminbereich** ein. Die Einstellungen
    liegen in **MongoDB**. Einschalten, Postfach ändern oder Zielprojekt wechseln
    wirkt **ohne Serverneustart**, weil der Poller die Einstellungen in jedem
    Durchlauf neu liest.

## So funktioniert es

Der Server fragt das Postfach regelmäßig ab. Ist der Eingang aktiviert und sind
Host und Standardprojekt gesetzt, passiert in jedem Durchlauf Folgendes:

1. Verbindung per IMAP oder IMAPS.
2. Der gewählte Ordner wird nach **ungelesenen** Nachrichten durchsucht.
3. Aus jeder Nachricht entsteht ein Vorgang.
4. Die Nachricht wird als **gelesen** markiert und nie doppelt importiert.

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

Schlägt ein Durchlauf fehl (Postfach nicht erreichbar, falsche Zugangsdaten), wird
der Fehler geloggt. Der nächste Durchlauf versucht es erneut. Es geht keine Mail
verloren, weil ungelesene Nachrichten beim nächsten erfolgreichen Abruf importiert
werden.

## Was erstellt wird

Jede Nachricht wird ein Vorgang im gewählten **Standardprojekt**:

| Vorgangsfeld | Stammt aus |
| --- | --- |
| **Titel** | Der **Betreff** der E-Mail (oder `(no subject)`, falls leer), auf eine sichere Länge gekürzt |
| **Beschreibung** | Ein kurzer Kopf mit dem Absender, dann der Klartext der Nachricht. Gibt es keinen Klartextteil, wird der HTML-Teil zu Text umgewandelt |
| **Typ** | **Task** |
| **Melder** | Die E-Mail-Adresse des Absenders |
| **Autor** | Der Absender, falls seine Adresse zu einem aktiven Hinata-Konto gehört. Dann bekommt er wie jeder Beobachter Benachrichtigungen zu jeder Änderung. Gehört die Adresse niemandem, bleibt der Vorgang ohne Autor. Der Kopf der Beschreibung nennt den Absender trotzdem |

!!! note "Ein Autor ohne Projektmitgliedschaft"
    Autor zu sein gibt keinen Zugriff. Nur wer Projektmitglied ist, kann den
    Vorgang öffnen. Ein Autor außerhalb des Projekts bekommt weiter E-Mail- und
    Push-Benachrichtigungen, aber ohne Link, denn der würde nur zum Fehler „kein
    Mitglied“ führen. Soll er den Vorgang verfolgen, nimm ihn ins Projekt auf.

Es ist ein normaler Vorgang. Er startet im Standardstatus des Workflows und
erscheint auf Board und Backlog. Du kannst ihn zuweisen, labeln, verlinken und
kommentieren. Ist das Projekt mit Git verbunden, sammelt er
Entwicklungsinformationen, sobald jemand seinen Schlüssel erwähnt.

!!! tip "Wähle ein dediziertes Eingangsprojekt"
    Leite eingehende Mails in ein eigenes Projekt, zum Beispiel einen
    *Support-Posteingang*. Dort sichtet jemand jeden neuen Vorgang, weist ihn zu,
    setzt Typ und Priorität oder verschiebt ihn ins richtige Projekt. So landen
    keine ungefilterten Mails auf einem aktiven Board.

## Konfiguration

Öffne **Adminbereich → E-Mail-Eingang** und trag die Postfachdaten ein:

| Einstellung | Standard | Bedeutung |
| --- | --- | --- |
| **Aktiviert** | `false` | Hauptschalter für den Poller |
| **Host** | (leer) | Hostname des IMAP-Servers |
| **Port** | `993` | IMAP-Port |
| **SSL** | `true` | IMAPS verwenden (implizites TLS). Der Standardport dafür ist `993` |
| **Benutzername** | (leer) | Postfach-Login |
| **Passwort** | (leer) | Postfach-Passwort. Nur schreibbar, die API gibt es nie zurück |
| **Ordner** | `INBOX` | Welcher Ordner gescannt wird |
| **Standardprojekt** | (leer) | Das Projekt, in dem die Vorgänge landen |
| **Poll-Intervall** | `60` s | Mindestabstand zwischen zwei Abrufen in Sekunden |

Der Eingang tut nichts, solange nicht **Aktiviert** an ist **und** **Host** und
**Standardprojekt** gesetzt sind. Eine halbfertige Konfiguration bleibt also
wirkungslos.

!!! warning "Verwende ein dediziertes Postfach"
    Jede **ungelesene** Nachricht im Ordner wird importiert und als gelesen
    markiert. Nutze ein Postfach nur für diesen Zweck. In einem gemeinsamen
    Posteingang würden sonst normale ungelesene Mails zu Vorgängen und als gelesen
    markiert.

## Wie es ausgehendes SMTP ergänzt

Beide Richtungen sind unabhängig und werden getrennt eingestellt:

- **Eingehend (diese Seite):** IMAP-Abruf, eingestellt im Adminbereich (MongoDB).
  Macht aus empfangenen Mails Vorgänge.
- **Ausgehend ([E-Mail & SMTP](/de/email.html)):** das SMTP-Relay, über das Hinata
  Mails zu Verifizierung, Passwort-Reset und Benachrichtigungen *sendet*.

Du kannst jede Richtung allein nutzen. Eine reine Statusseite sendet vielleicht
nur, eine Eingangsadresse empfängt vielleicht nur. Die meisten
Produktivinstallationen nutzen beides: SMTP für die Mails an Nutzer und den
Eingang für Supportanfragen.

## Verwandte Seiten

- [E-Mail & SMTP](/de/email.html): ausgehende E-Mails einrichten.
- [Adminbereich](/de/admin-area.html): hier stellst du den Eingang ein.
- [Projekte & Teams](/de/projects-teams.html): das Eingangsprojekt wählen und sichten.
- [Benachrichtigungen](/de/notifications.html): wie Personen von neuen Vorgängen erfahren.
