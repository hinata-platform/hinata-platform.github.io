---
title: Hinata Connect Gateway
description: Ein zentrales Relay für mobile Push-Nachrichten und Universal Links, sodass eine einzige veröffentlichte White-Label-App jeden selbst gehosteten Hinata-Server bedienen kann — ohne Firebase für Betreiber.
---

# Hinata Connect Gateway

Mobile Push-Benachrichtigungen und Universal Links haben eine unbequeme Voraussetzung: Sie sind an die Plattform-Anmeldedaten einer **veröffentlichten App** gebunden (Firebase/FCM, Apple/Google App-Site-Associations). Ein selbst gehosteter Server kann diese nicht für eine App besitzen, die er nicht in den Stores veröffentlicht hat. Das **Hinata Connect Gateway** löst das mit einem kleinen, zentralen Relay, sodass eine einzige veröffentlichte App *jeden* Hinata-Server bedienen kann — und Selbst-Hoster **überhaupt kein Firebase** brauchen.

## Was es macht

Das Gateway ist ein gemeinsamer, zentraler Dienst (standardmäßig `https://connect.hinata.ahmadre.com`), der zwei Dinge weiterleitet:

1. **Push-Benachrichtigungen** — es hält die FCM-Anmeldedaten der veröffentlichten App und leitet Push-Nachrichten von jedem registrierten Server an die richtigen Geräte weiter.
2. **Universal- / App-Links** — es besitzt die verifizierte Link-Domain, sodass Einladungs-, Verifizierungs- und Passwort-Zurücksetzen-Links von *jedem* selbst gehosteten Server die installierte App auf dem richtigen Backend öffnen.

```text
  Selbst gehosteter Server A ─┐
  Selbst gehosteter Server B ─┼──registriert sich beim Booten──▶  Hinata Connect Gateway  ──push──▶  📱 veröffentlichte App
  Selbst gehosteter Server C ─┘                                    (besitzt FCM + Link-Domain)   ──/l/<code>──▶  Deep Link
```

Dein Server **registriert sich beim Booten selbst beim Gateway**. Von da an funktionieren Push- und Universal-Link-Weiterleitung einfach — die FCM-Schlüssel und die App-Site-Association-Dateien liegen im Gateway, niemals in deinem Deployment.

## Warum es existiert (White-Label)

Weil eine veröffentlichte [White-Label](/de/white-label.html)-App auf viele Server zeigen kann, kann sie keine serverspezifischen Push-Anmeldedaten einbacken. Das Gateway ist das gemeinsame Teil, das „eine App, viele Server" ermöglicht und Betreiber dabei komplett aus dem Firebase-Geschäft heraushält.

!!! tip "Für den Standardfall nichts zu konfigurieren"
    Wenn du die Standard-App und das Standard-Gateway nutzt, gibt es keine Push-Einrichtung: Dein Server registriert sich beim Booten, und Benachrichtigungen fließen. Das ist der empfohlene Weg für die meisten Selbst-Hoster.

## Konfiguration

| Variable | Zweck |
| --- | --- |
| `HINATA_GATEWAY_BASE_URL` | Gateway-URL. Standard ist das gemeinsame Gateway; überschreibe sie, um auf dein eigenes zu zeigen. |
| `HINATA_GATEWAY_BOOTSTRAP_SECRET` | Optional — nur wenn dein Gateway die Registrierung hinter einem Bootstrap-Secret absichert. |

Universal Links werden als `https://<gateway>/l/<code>` weitergeleitet, wobei `<code>` den Ursprungsserver, den In-App-Pfad und ein Token kodiert. Die App dekodiert ihn lokal, wechselt zum richtigen Server und leitet zum Ziel weiter — so öffnet eine Einladung von *deinem* Server die App, die auf *dein* Backend zeigt.

## Ein eigenes Gateway betreiben

Wenn du deine **eigene** gebrandete App in die Stores bringst, besitzt du deren FCM-Anmeldedaten und Link-Domain — also betreibst du dein eigenes Gateway und richtest deinen Server mit `HINATA_GATEWAY_BASE_URL` darauf aus. Das ist ein fortgeschrittener Weg, der Hand in Hand mit einem vollständigen [White-Label-Build](/de/white-label.html) geht; die Mechanik von Registrierung und Weiterleitung ist identisch zum gemeinsamen Gateway.

!!! warning "Härtung der Selbstregistrierung"
    Ein Gateway, das offene Registrierung akzeptiert, sollte in der Produktion geschützt werden (z. B. mit einem Bootstrap-Secret), sodass sich nur deine Server registrieren können. Verwende `HINATA_GATEWAY_BOOTSTRAP_SECRET`, wenn du dein eigenes betreibst.

## Nächste Schritte

- Bringe deinen eigenen Client heraus unter [White-Label & Branding](/de/white-label.html).
- Konfiguriere Zustellkanäle unter [Benachrichtigungen](/de/notifications.html).
- Sieh dir die Link-Behandlung unter [Die Apps](/de/clients.html) an.
