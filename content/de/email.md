---
title: E-Mail & SMTP
description: Ausgehende E-Mails für Zuweisungen, Verifizierung und Passwort zurücksetzen einrichten, mit Mailpit in der Entwicklung und einem echten SMTP-Relay in Produktion.
---

# E-Mail & SMTP

Hinata verschickt E-Mails über **SMTP**:

- Benachrichtigungen, wenn dir ein Vorgang zugewiesen wird
- E-Mail-Verifizierung für neue Konten
- Links zum Zurücksetzen des Passworts

In der Entwicklung fängt **Mailpit** diese Mails ab, und du liest sie im Browser. In Produktion brauchst du einen **echten SMTP-Relay**, damit sie in den Postfächern ankommen.

!!! info "Eingehende Mail ist eine eigene Funktion"
    Diese Seite behandelt *ausgehende* Mail. Eingehende E-Mails als Vorgänge (IMAP-Polling) richtest du im Adminbereich ein, siehe [E-Mail zu Vorgang](/de/email-to-ticket.html).

## Konfigurationsvariablen

| Variable | Zweck | Dev-Standard |
| --- | --- | --- |
| `HINATA_SMTP_HOST` | Hostname des SMTP-Servers | `mailpit` |
| `HINATA_SMTP_PORT` | SMTP-Port | `1025` |
| `HINATA_SMTP_USERNAME` | Benutzername für die SMTP-Anmeldung | *(leer)* |
| `HINATA_SMTP_PASSWORD` | Passwort für die SMTP-Anmeldung | *(leer)* |
| `HINATA_SMTP_AUTH` | SMTP-Authentifizierung aktivieren | `false` |
| `HINATA_SMTP_STARTTLS` | Verbindung per STARTTLS verschlüsseln | `false` |
| `HINATA_MAIL_FROM` | Absenderadresse ausgehender Mails | `hinata@localhost` |
| `HINATA_WEB_BASE_URL` | Ziel der Links in E-Mails (die Flutter-Web-App) | *(fällt auf Basis-URL zurück)* |

Alle Werte sind normale Umgebungsvariablen. Setze sie in `.env` oder direkt am Container.

## Entwicklung: Mailpit

Der Dev-Stack (`docker-compose.dev.yml`) enthält Mailpit. Es nimmt Mail auf `localhost:1025` an und zeigt jede Nachricht im Browser:

```bash
docker compose -f docker-compose.dev.yml up -d   # includes Mailpit
```

Unter **`http://localhost:8025`** liest du alles, was Hinata verschickt. Mailpit braucht weder Zugangsdaten noch STARTTLS und nimmt jede Mail an. Der Standard für `HINATA_SMTP_HOST` ist `mailpit` (im Compose-Netzwerk `mailpit`/`1025`), lokal musst du also nichts einstellen.

!!! warning "Mailpit stellt nie zu"
    Mailpit zeigt Mails nur an und leitet sie nicht an echte Postfächer weiter. Kommen in Produktion keine Mails zur Verifizierung oder zum Zurücksetzen an, wurde fast immer kein echter Relay eingerichtet, und Hinata spricht noch mit einem Mail-Catcher für die Entwicklung.

## Produktion: ein echter SMTP-Relay

Richte Hinata auf einen SMTP-Relay, den du selbst betreibst oder bei einem Anbieter nutzt. Typisch ist STARTTLS auf Port 587:

```properties
HINATA_SMTP_HOST=smtp.example.org
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.org
HINATA_SMTP_PASSWORD=your-smtp-password
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=Hinata <hinata@example.org>
```

Das passt für fast alle Relays: den SMTP deines Providers, einen Dienst für Transaktionsmails oder dein eigenes Postfix. Verlangt der Relay eine Anmeldung (bei gehosteten Relays fast immer), setze `HINATA_SMTP_AUTH=true` und gib Zugangsdaten an.

!!! danger "MAIL_FROM muss oft zu einer authentifizierten Identität passen"
    Viele Relays lehnen Mails ab, deren `From`-Adresse keine Identität ist, als die du angemeldet und sendeberechtigt bist (SPF/DKIM-Ausrichtung). Wird Mail ohne Meldung verworfen oder mit „sender not allowed“ abgewiesen, setze `HINATA_MAIL_FROM` auf einen verifizierten Absender oder eine verifizierte Domain deines Relays. Das ist die häufigste Stolperfalle beim Mailversand.

## Deep Links: wohin die E-Mails zeigen

Links in Hinatas E-Mails („diesen Vorgang öffnen“, „deine Adresse verifizieren“, „dein Passwort zurücksetzen“) müssen deine **Flutter-Web-App** öffnen und nicht die API. Das Ziel legt `HINATA_WEB_BASE_URL` fest:

```properties
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com
```

Ist `HINATA_WEB_BASE_URL` leer, nutzen die Links `HINATA_BASE_URL`. Laufen Web-App und API auf getrennten Hosts (der übliche Fall), landen Nutzer dann auf der API-Domain. **Setze `HINATA_WEB_BASE_URL` deshalb explizit** auf die öffentliche URL deiner Web-App.

!!! tip "Zurücksetzen und Verifizieren laufen in der App"
    Beides läuft über diese Deep Links in der App. Der Server rendert dafür keine eigenen HTML-Seiten. Nur mit korrekter `HINATA_WEB_BASE_URL` landen die Links auf einem funktionierenden Bildschirm.

## Deine Konfiguration testen

1. Setze die SMTP-Variablen und starte den Server neu.
2. Löse eine echte Nachricht aus, z. B. eine Passwortzurücksetzung oder eine Vorgangszuweisung an ein Teammitglied mit aktiven Benachrichtigungen.
3. Prüfe die Zustellung im Postfach oder im Ausgangsprotokoll des Relays. In der Entwicklung schaust du in Mailpit unter `http://localhost:8025`.
4. Kommt nichts an:
   - Vergleiche `HINATA_MAIL_FROM` mit den erlaubten Absendern des Relays.
   - Prüfe Port und STARTTLS (587 mit STARTTLS oder 465 für implizites TLS).
   - Setze `HINATA_SMTP_AUTH=true`, wenn Zugangsdaten nötig sind.

Alle Variablen stehen in der [Konfigurationsreferenz](/de/configuration.html). Für eingehende Mail als Vorgang siehe [E-Mail zu Vorgang](/de/email-to-ticket.html).
