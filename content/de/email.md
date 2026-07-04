---
title: E-Mail & SMTP
description: Konfiguriere den ausgehenden Mailversand, damit Hinata Zuweisungs-, Verifizierungs- und Passwort-Zurücksetzungs-E-Mails zustellen kann — Mailpit in der Entwicklung, ein echter SMTP-Relay in der Produktion.
---

# E-Mail & SMTP

Hinata versendet transaktionale E-Mails über **SMTP**: Benachrichtigungen zur
Vorgangszuweisung, E-Mail-Verifizierung für neue Konten und Passwort-Zurücksetzungs-Links. In
der lokalen Entwicklung werden diese von **Mailpit** abgefangen, sodass du sie im Browser lesen
kannst; in der Produktion richtest du Hinata auf einen **echten SMTP-Relay**, damit diese
Nachrichten tatsächlich die Postfächer der Menschen erreichen.

!!! info "Eingehende Mail ist eine separate Funktion"
    Diese Seite handelt von *ausgehender* Mail. Das Umwandeln eingehender E-Mails in Vorgänge
    (IMAP-Polling) wird im Adminbereich konfiguriert und auf einer eigenen Seite dokumentiert:
    [E-Mail zu Vorgang](/de/email-to-ticket.html).

## Konfigurationsvariablen

| Variable | Zweck | Dev-Standard |
| --- | --- | --- |
| `HINATA_SMTP_HOST` | SMTP-Server-Hostname | `mailpit` |
| `HINATA_SMTP_PORT` | SMTP-Port | `1025` |
| `HINATA_SMTP_USERNAME` | SMTP-Auth-Benutzername | *(leer)* |
| `HINATA_SMTP_PASSWORD` | SMTP-Auth-Passwort | *(leer)* |
| `HINATA_SMTP_AUTH` | SMTP-Authentifizierung aktivieren | `false` |
| `HINATA_SMTP_STARTTLS` | Die Verbindung mit STARTTLS upgraden | `false` |
| `HINATA_MAIL_FROM` | Absenderadresse für ausgehende Mail | `hinata@localhost` |
| `HINATA_WEB_BASE_URL` | Wohin E-Mail-Deep-Links zeigen (die Flutter-Web-App) | *(fällt auf Basis-URL zurück)* |

Jeder Wert ist eine einfache Umgebungsvariable — setze sie in `.env` oder direkt am Container.

## Entwicklung: Mailpit

Der Dev-Stack (`docker-compose.dev.yml`) enthält Mailpit, das Mail auf `localhost:1025`
annimmt und jede Nachricht in einer Web-UI anzeigt:

```bash
docker compose -f docker-compose.dev.yml up -d   # includes Mailpit
```

Öffne **`http://localhost:8025`**, um zu lesen, was auch immer Hinata versendet. Keine
Zugangsdaten, kein STARTTLS — Mailpit verschluckt alles, was genau das ist, was du während der
Entwicklung willst. Da der Standard `HINATA_SMTP_HOST` `mailpit` ist (und `mailpit`/`1025` im
Compose-Netzwerk), musst du nichts konfigurieren, damit lokale Mail funktioniert.

!!! warning "Mailpit stellt nie zu"
    Mailpit ist eine Falle, die Mail *anzeigt*; sie leitet sie nicht an echte Postfächer weiter.
    Wenn Verifizierungs- oder Zurücksetzungs-E-Mails in der Produktion nicht ankommen, ist die
    Ursache fast immer, dass nie ein echter Relay konfiguriert wurde und Hinata noch mit einem
    Dev-Mail-Fänger spricht.

## Produktion: ein echter SMTP-Relay

Für einen Produktionsserver richtest du Hinata auf einen SMTP-Relay, den du kontrollierst oder
abonnierst. Eine typische STARTTLS-Konfiguration auf Port 587:

```properties
HINATA_SMTP_HOST=smtp.example.org
HINATA_SMTP_PORT=587
HINATA_SMTP_USERNAME=hinata@example.org
HINATA_SMTP_PASSWORD=your-smtp-password
HINATA_SMTP_AUTH=true
HINATA_SMTP_STARTTLS=true
HINATA_MAIL_FROM=Hinata <hinata@example.org>
```

Das deckt die überwältigende Mehrheit der Relays ab — Provider-SMTP, ein
Transaktions-Mail-Dienst oder dein eigenes Postfix. Setze `HINATA_SMTP_AUTH=true` und gib
Zugangsdaten an, wann immer der Relay einen Login erfordert (fast immer der Fall bei einem
gehosteten Relay).

!!! danger "MAIL_FROM muss oft einer authentifizierten Identität entsprechen"
    Viele Relays weisen eine Nachricht ab, deren `From`-Adresse keine Identität ist, als die du
    authentifiziert und autorisiert bist zu senden (SPF/DKIM-Ausrichtung). Wenn Mail stillschweigend
    verworfen oder mit einem Fehler "sender not allowed" zurückgewiesen wird, lasse
    `HINATA_MAIL_FROM` einem verifizierten Absender/einer verifizierten Domain auf deinem Relay
    entsprechen — dies ist die häufigste Stolperfalle bei ausgehender Mail.

## Deep Links: wohin die E-Mails zeigen

Die Links in Hinatas E-Mails — "diesen Vorgang öffnen", "deine Adresse verifizieren", "dein
Passwort zurücksetzen" — müssen deine **Flutter-Web-App** öffnen, nicht die API. Dieses Ziel ist
`HINATA_WEB_BASE_URL`:

```properties
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com
```

Wenn `HINATA_WEB_BASE_URL` leer ist, fallen Deep Links auf `HINATA_BASE_URL` zurück. Bei einem
geteilten Host-/API-Deployment (der übliche Fall) würde das Nutzer zur API-Domain schicken, also
**setze `HINATA_WEB_BASE_URL` explizit** auf die öffentliche URL deiner Web-App.

!!! tip "Zurücksetzungs- und Verifizierungs-Links kommen ohne Backend aus"
    Passwort-Zurücksetzung und Verifizierung geschehen über die App via dieser Deep Links — der
    Server rendert dafür keine eigenen HTML-Seiten. `HINATA_WEB_BASE_URL` richtig zu setzen ist
    das, was diese Abläufe auf einem funktionierenden Bildschirm landen lässt.

## Deine Konfiguration testen

1. Setze die SMTP-Variablen und starte den Server neu.
2. Löse eine echte Nachricht aus — fordere zum Beispiel eine Passwort-Zurücksetzung an oder weise
   einem Teammitglied mit aktivierten Benachrichtigungen einen Vorgang zu.
3. Bestätige die Zustellung (prüfe das Postfach oder das Ausgangsprotokoll deines Relays). In der
   Entwicklung beobachte Mailpit unter `http://localhost:8025`.
4. Falls nichts ankommt: Prüfe `HINATA_MAIL_FROM` erneut gegen die erlaubten Absender deines
   Relays, bestätige die Port-/STARTTLS-Paarung (587 + STARTTLS oder 465 für implizites TLS) und
   stelle sicher, dass `HINATA_SMTP_AUTH=true` gesetzt ist, wenn Zugangsdaten erforderlich sind.

Für den vollständigen Variablenkatalog siehe die
[Konfigurationsreferenz](/de/configuration.html); für eingehende Mail-zu-Vorgang siehe
[E-Mail zu Vorgang](/de/email-to-ticket.html).
