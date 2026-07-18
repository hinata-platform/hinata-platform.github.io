---
title: Hinata Connect Gateway
description: Ein zentrales, gehostetes Relay für mobile Push-Nachrichten und Universal Links, sodass die eine veröffentlichte App jeden selbst gehosteten Hinata-Server bedienen kann — ohne Firebase für Betreiber.
---

# Hinata Connect Gateway

Mobile Push-Benachrichtigungen und Universal Links haben eine unbequeme Voraussetzung: Sie sind an die Plattform-Anmeldedaten einer **veröffentlichten App** gebunden (Firebase/FCM, Apple/Google App-Site-Associations). Ein selbst gehosteter Server kann diese nicht für eine App besitzen, die er nicht in den Stores veröffentlicht hat. Das **Hinata Connect Gateway** löst das mit einem kleinen, zentralen Relay, sodass eine einzige veröffentlichte App *jeden* Hinata-Server bedienen kann — und Selbst-Hoster **überhaupt kein Firebase** brauchen.

## Was es macht

Das Gateway ist ein gemeinsamer, **gehosteter** Dienst (standardmäßig `https://connect.hinata.ahmadre.com`), der vom App-Herausgeber betrieben und abgesichert wird und zwei Dinge weiterleitet:

1. **Push-Benachrichtigungen** — die Push-Zugangsdaten der veröffentlichten App liegen im Gateway, sodass es Benachrichtigungen von jedem verbundenen Server an die richtigen Geräte weiterleiten kann.
2. **Universal- / App-Links** — es besitzt die verifizierte Link-Domain, sodass Einladungs-, Verifizierungs- und Passwort-Zurücksetzen-Links von *jedem* selbst gehosteten Server die installierte App auf dem richtigen Backend öffnen.

```text
  Selbst gehosteter Server A ─┐
  Selbst gehosteter Server B ─┼── verbindet sich ──▶  Hinata Connect Gateway  ──push──▶  📱 veröffentlichte App
  Selbst gehosteter Server C ─┘                          (gehosteter Dienst)     ──link──▶  richtiges Backend
```

Sobald dein Server mit dem Gateway verbunden ist, funktionieren Push- und Universal-Link-Weiterleitung einfach — die Plattform-Anmeldedaten liegen im Gateway, niemals in deinem Deployment.

## Warum es existiert (eine App, viele Server)

Weil die eine veröffentlichte App auf [jeden selbst gehosteten Server zeigen kann](/de/self-hosted-app.html), kann sie keine serverspezifischen Push-Anmeldedaten einbacken. Das Gateway ist das gemeinsame Teil, das „eine App, viele Server" ermöglicht und Betreiber dabei komplett aus dem Firebase-Geschäft heraushält.

!!! tip "Für den Standardfall nichts zu betreiben"
    Wenn du die Standard-App und das Standard-Gateway nutzt, gibt es keine Push-Infrastruktur zu betreiben: Das Gateway ist ein gehosteter Dienst, und Benachrichtigungen fließen, sobald deine Instanz verbunden ist. Das ist der empfohlene Weg für die meisten Selbst-Hoster.

## Konfiguration

| Variable | Zweck |
| --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Gateway-URL. Standard ist das gemeinsame gehostete Gateway; überschreibe sie nur, um auf dein eigenes zu zeigen (siehe unten). |

Universal Links werden als `https://<gateway>/l/<code>` weitergeleitet; die App dekodiert den Code, wechselt zum Ursprungsserver und leitet zum Ziel weiter — so öffnet eine Einladung von *deinem* Server die App, die auf *dein* Backend zeigt.

## Ein eigenes Gateway betreiben

Wenn du deine **eigene** gebrandete App in die Stores bringst, besitzt du deren Push-Anmeldedaten und Link-Domain — also betreibst du dein eigenes Gateway und richtest deinen Server mit `HINATA_GATEWAY_BASE_URL` darauf aus. Das ist ein fortgeschrittener Weg, der Hand in Hand mit einem vollständigen [eigenen Client-Build](/de/self-hosted-app.html) geht; die Form der Weiterleitung ist dieselbe wie beim gehosteten Gateway.

## Nächste Schritte

- Bringe deinen eigenen Client heraus unter [Branding & eigene Clients](/de/self-hosted-app.html).
- Konfiguriere Zustellkanäle unter [Benachrichtigungen](/de/notifications.html).
- Sieh dir die Link-Behandlung unter [Die Apps](/de/clients.html) an.
