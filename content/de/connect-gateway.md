---
title: Hinata Connect Gateway
description: Ein zentrales, gehostetes Relay für Push und Universal Links, damit die veröffentlichte App jeden selbst gehosteten Hinata-Server bedienen kann, ganz ohne Firebase für Betreiber.
---

# Hinata Connect Gateway

Push-Benachrichtigungen und Universal Links hängen an den Plattformzugangsdaten einer **veröffentlichten App** (Firebase/FCM, Windows Push Notification Services, App-Site-Associations von Apple und Google). Ein selbst gehosteter Server kann diese für eine App, die er nicht selbst in den Stores veröffentlicht hat, nicht besitzen.

Das **Hinata Connect Gateway** ist ein kleines, zentrales Relay. Damit bedient eine einzige veröffentlichte App *jeden* Hinata-Server, und wer selbst hostet, braucht **gar kein Firebase**.

## Was es macht

Das Gateway ist ein gemeinsamer, **gehosteter** Dienst (standardmäßig `https://connect.hinata.ahmadre.com`). Der Herausgeber der App betreibt und sichert ihn. Es leitet zwei Dinge weiter:

1. **Push-Benachrichtigungen:** Die Zugangsdaten für Push liegen im Gateway. Es leitet Benachrichtigungen jedes verbundenen Servers an die richtigen Geräte weiter. Für Android, iOS und macOS geht das über **FCM**, für den Windows-Build über **WNS**, weil Firebase Windows nicht unterstützt.
2. **Universal Links und App Links:** Das Gateway besitzt die verifizierte Link-Domain. Links zum Einladen, Verifizieren und Zurücksetzen des Passworts von *jedem* selbst gehosteten Server öffnen so die installierte App mit dem richtigen Backend.

```text
  Selbst gehosteter Server A ─┐
  Selbst gehosteter Server B ─┼── verbindet sich ──▶  Hinata Connect Gateway  ──push──▶  📱 veröffentlichte App
  Selbst gehosteter Server C ─┘                          (gehosteter Dienst)     ──link──▶  richtiges Backend
```

Ist dein Server mit dem Gateway verbunden, funktionieren Push und Universal Links. Die Plattformzugangsdaten liegen im Gateway und nie in deinem Deployment.

## Warum es existiert (eine App, viele Server)

Die veröffentlichte App kann [auf jeden selbst gehosteten Server zeigen](/de/self-hosted-app.html). Deshalb kann sie keine Zugangsdaten für Push pro Server enthalten. Das Gateway macht „eine App, viele Server“ möglich, und Betreiber müssen sich nicht um Firebase kümmern.

!!! tip "Im Normalfall musst du nichts betreiben"
    Mit der Standard-App und dem Standard-Gateway betreibst du keine eigene Infrastruktur für Push. Benachrichtigungen kommen an, sobald deine Instanz verbunden ist. Das ist der empfohlene Weg für die meisten, die selbst hosten.

## Konfiguration

| Variable | Zweck |
| --- | --- |
| `HINATA_GATEWAY_BASE_URL` | URL des Gateways. Standard ist das gemeinsame gehostete Gateway. Überschreibe sie nur, wenn du ein eigenes nutzt (siehe unten). |

Universal Links laufen über `https://<gateway>/l/<code>`. Die App dekodiert den Code, wechselt zum Ursprungsserver und öffnet das Ziel. So öffnet eine Einladung von *deinem* Server die App mit *deinem* Backend.

## Ein eigenes Gateway betreiben

Bringst du eine **eigene** gebrandete App in die Stores, gehören dir ihre Zugangsdaten für Push und ihre Link-Domain. Dann betreibst du ein eigenes Gateway und stellst deinen Server mit `HINATA_GATEWAY_BASE_URL` darauf ein. Das ist ein fortgeschrittener Weg und gehört zu einem vollständigen [eigenen Client-Build](/de/self-hosted-app.html). Die Weiterleitung funktioniert wie beim gehosteten Gateway.

## Nächste Schritte

- Eigenen Client veröffentlichen: [Branding & eigene Clients](/de/self-hosted-app.html).
- Zustellkanäle einrichten: [Benachrichtigungen](/de/notifications.html).
- Wie die App Links verarbeitet: [Die Apps](/de/clients.html).
