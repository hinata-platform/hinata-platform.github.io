---
title: Architektur
description: Wie Hinata zusammenpasst — Flutter-App, dio-ApiClient, REST /api/v1, Spring Boot, MongoDB-Replica-Set, S3/MinIO, SMTP, SSE und das Connect Gateway.
---

# Architektur

Hinata besteht aus zwei deploybaren Einheiten — einem Flutter-Client und einem Spring-Boot-Server — die über eine versionierte REST-API kommunizieren, gestützt auf MongoDB und S3-kompatiblen Speicher. Diese Seite erklärt, wie die Teile zusammenpassen, wie eine Anfrage fließt und wo die Laufzeitkonfiguration liegt.

## Die Komponenten

Auf einen Blick, vom Client bis zum Speicher:

```text
┌──────────────────────────────────────────────────────────────┐
│  Client — hinata-app (Flutter)                                │
│  Android · iOS · Web · macOS · eine Codebasis                 │
│                                                                │
│   UI (bloc/cubit, go_router)                                  │
│        │                                                       │
│   ApiClient (dio)                                             │
│    · hängt Bearer-Access-Token an                            │
│    · sendet Accept-Language (en / de)                        │
│    · erneuert automatisch bei 401, wiederholt einmal         │
└───────────────┬────────────────────────────────┬─────────────┘
                │ HTTPS  REST /api/v1             │ SSE (live)
                ▼                                 ▼
┌──────────────────────────────────────────────────────────────┐
│  Server — hinata-server (Spring Boot 4, Java 21)             │
│                                                                │
│   Controller → Services → Repositories                        │
│   JWT-Auth · Rate-Limiting · lokalisierte Fehler             │
│   Laufzeit-Einstellungen aus MongoDB (überschreiben env)     │
└───┬────────────────┬───────────────────┬──────────────┬───────┘
    │                │                   │              │
    ▼                ▼                   ▼              ▼
┌────────┐    ┌────────────┐      ┌────────────┐  ┌──────────┐
│MongoDB │    │  S3/MinIO  │      │    SMTP    │  │  Hinata  │
│Replica │    │Attachments │      │  ausgeh.   │  │ Connect  │
│  Set   │    │ presigned  │      │   E-Mail   │  │ Gateway  │
└────────┘    └────────────┘      └────────────┘  └──────────┘
```

- **App (Flutter)** — eine einzige Codebasis für Android, iOS, Web und macOS. State wird mit bloc/cubit verwaltet, Routing mit go_router, Lokalisierung mit i18next (Englisch + Deutsch) und Networking über **dio** innerhalb eines `ApiClient`. Diagramme werden mit fl_chart gezeichnet.
- **Server (Spring Boot 4, Java 21)** — stellt die REST-API unter `/api/v1` bereit, hält die gesamte Geschäftslogik und Autorisierung und streamt Live-Updates.
- **MongoDB** — das System of Record. In Produktion läuft ein **Replica Set** (2 Datenknoten + 1 Arbiter) mit TLS und X.509-Client-Authentifizierung.
- **S3 / MinIO** — Objektspeicher für Attachments und Avatare, mit zufälligen Objekt-Keys und presignten Downloads.
- **SMTP** — ausgehende Mail (Verifizierung, Benachrichtigungen, Passwort-Reset). Mailpit übernimmt das in der Entwicklung.
- **Hinata Connect Gateway** — ein zentrales Push-Relay und Universal-Link-Relay, sodass eine einzige veröffentlichte White-Label-App viele Server bedienen kann.

## Der Weg App → Server

Jeder Netzwerkaufruf aus der App läuft durch einen einzigen `ApiClient`, aufgebaut auf **dio**. Dieser Client ist der Ort für Querschnittsbelange, sodass einzelne Screens nie über Tokens oder Header nachdenken müssen:

- Er hängt das aktuelle **Bearer-Access-Token** an authentifizierte Anfragen an.
- Er sendet einen **`Accept-Language`**-Header (`en` oder `de`), damit der Server Fehlermeldungen lokalisieren kann.
- Bei einem `401` ruft er transparent den Refresh-Endpunkt auf, tauscht ein frisches Access-Token ein und **wiederholt die ursprüngliche Anfrage einmal**. Schlägt der Refresh fehl, wird die Sitzung geleert und zum Login geroutet.

Der Server stellt eine stabile, versionierte Oberfläche unter **`/api/v1`** bereit. Siehe die [API-Referenz](/de/api.html) für die vollständige Endpunktliste.

!!! info "Multi-Server von Grund auf"
    Die native App backt nie eine Server-URL ein. Nutzer speichern einen oder mehrere Server und wechseln zwischen ihnen, und Access-Tokens sind **pro Server** gescopet. Der Web-Build kann auf seinen eigenen Origin defaulten. Genau das macht dieselbe veröffentlichte App gegen jeden Hinata-Server nutzbar — siehe [White-Label & Branding](/de/white-label.html).

## Live-Updates mit SSE

Statt zu pollen, pusht der Server Änderungen über **Server-Sent Events (SSE)** an verbundene Clients. Das klarste Beispiel sind Attachments: Wird eine Datei zu einem Vorgang hinzugefügt oder entfernt, erhält jeder offene Client, der diesen Vorgang streamt, die Änderung sofort unter:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

SSE ist ein einseitiger, langlebiger HTTP-Stream, was Live-Sync günstig und proxy-freundlich hält — kein WebSocket-Upgrade nötig. Stelle sicher, dass dein [Reverse Proxy](/de/reverse-proxy.html) diese Antworten nicht puffert.

## Anfrage-Lebenszyklus & Token-Refresh

Eine typische authentifizierte Anfrage:

1. **App** stellt eine Anfrage über `ApiClient`; dio hängt das Bearer-Access-Token und `Accept-Language` an.
2. **Server** authentifiziert das JWT (HS512), erzwingt Rate-Limits pro IP und prüft die Autorisierung (zum Beispiel erfordert `/api/v1/admin/**` die Rolle `ADMIN`).
3. **Controller → Service → Repository** — die Service-Schicht wendet Geschäftsregeln an und liest/schreibt MongoDB; Attachment-Bytes gehen an S3/MinIO.
4. **Antwort** ist ein stabiler, lokalisierter JSON-Body — Erfolgs-Payload oder ein Fehler, aufgelöst aus `messages.properties` in der Sprache des Clients, ohne Stacktraces.

Access-Tokens sind bewusst **kurzlebig**; Refresh-Tokens sind langlebiger, werden aber **für API-Zugriff abgelehnt** — sie können nur neue Access-Tokens ausstellen. Läuft ein Access-Token mitten in der Sitzung ab, ist der Refresh-Tanz für den Nutzer unsichtbar:

```text
App ──GET /issues (abgelaufenes Access-Token)──▶ Server
App ◀──────────── 401 Unauthorized ──────────────── Server
App ──POST /auth/refresh (Refresh-Token)────────▶ Server
App ◀──────── neues Access-Token ────────────────── Server
App ──GET /issues (wiederholt, neues Token)─────▶ Server
App ◀──────────────── 200 OK ──────────────────────── Server
```

Siehe [Authentifizierung](/de/authentication.html) für das vollständige Token-Modell.

## Laufzeit-Einstellungen in MongoDB

Ein prägendes Merkmal von Hinata: Der Großteil der operativen Konfiguration wird **in MongoDB gespeichert und aus dem Adminbereich der App verwaltet**, nicht beim Boot in Umgebungsvariablen eingefroren. Das umfasst SSO-Provider, E-Mail-Ingest (IMAP), Push, Git-OAuth-Apps und App-Einstellungen wie die minimale Client-Version.

Daraus folgen zwei Regeln:

- **Die Datenbank überschreibt die Umgebung.** Umgebungsvariablen wie `hinata.app.*` sind Standardwerte; ein im Adminbereich gesetzter Wert gewinnt.
- **Änderungen greifen ohne Neustart.** Aktualisiere einen SSO-Provider oder ein Feature-Flag, und es wirkt bei der nächsten Anfrage — kein Redeploy, kein Container-Neustart.

!!! tip "Secrets sind write-only"
    In der Admin-API sind Secrets (OAuth-Client-Secrets, Tokens, Passwörter) **write-only** — du kannst sie setzen, aber sie werden nie zurückgegeben. Gespeicherte Git-Access-Tokens sind zusätzlich mit AES-GCM at rest verschlüsselt.

Deshalb braucht das Bootstrapping nur eine Handvoll Umgebungsvariablen (siehe [Konfigurationsreferenz](/de/configuration.html)); alles andere wird live konfiguriert, sobald der Server läuft.

## Lokalisierte Fehler

Fehlermeldungen werden **serverseitig** aus Resource-Bundles aufgelöst — `messages.properties` (Englisch, der Standard) und `messages_de.properties` (Deutsch) — anhand des `Accept-Language`-Headers des Clients. Die App sendet die Sprache des Nutzers, und der Server gibt einen stabilen, maschinenlesbaren Fehler zurück, dessen menschliche Meldung bereits in der richtigen Sprache ist. Keine Übersetzungslogik lebt im Client.

## Das Connect Gateway

Push-Benachrichtigungen und Universal Links werden über das **Hinata Connect Gateway** weitergeleitet, statt in jeden Server eingebacken zu sein:

- Der Server **registriert sich beim Boot beim Gateway**.
- Server-spezifische Firebase/FCM-Zugangsdaten leben im Gateway, nicht in jedem Server, sodass **Self-Hoster kein Firebase-Projekt brauchen**.
- Die App behandelt Universal Links der Form `/l/<code>` über das Gateway.
- Überschreibe das Gateway mit `HINATA_GATEWAY_BASE_URL`, um ein eigenes zu betreiben.

Diese Indirektion ermöglicht es, dass eine veröffentlichte White-Label-App eine unbegrenzte Anzahl unabhängiger Hinata-Server bedient. Siehe [Hinata Connect Gateway](/de/connect-gateway.html) für das vollständige Design.

## Wohin als Nächstes

- [Grundkonzepte](/de/concepts.html) — das Vokabular, auf dem API und UI aufbauen.
- [Self-Hosting-Überblick](/de/self-hosting.html) — wie diese Komponenten auf Container abgebildet werden, die du deployst.
- [Sicherheitsmodell](/de/security.html) — die Garantien hinter dem obigen Anfragepfad.
