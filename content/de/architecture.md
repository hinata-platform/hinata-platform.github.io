---
title: Architektur
description: Wie Hinata aufgebaut ist, von der Flutter-App über den Spring-Boot-Server bis zu MongoDB, S3, SMTP, SSE und dem Connect Gateway.
---

# Architektur

Hinata besteht aus zwei Teilen: einem Flutter-Client und einem Spring-Boot-Server. Beide sprechen über eine versionierte REST-API. Dahinter liegen MongoDB und S3-kompatibler Speicher.

## Die Komponenten

Vom Client bis zum Speicher:

<div class="arch" role="img" aria-label="Architektur: Die Flutter-App spricht über REST und SSE mit dem Spring-Boot-Server; der Server wird von MongoDB, S3/MinIO, SMTP und dem Hinata Connect Gateway gestützt."><div class="arch-node glass"><div class="arch-node-top"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg></span><span class="arch-txt"><strong>Client: hinata-app</strong><em>Flutter · eine Codebasis</em></span><span class="arch-tag">Android · iOS · Web · macOS · Windows · Linux</span></div><div class="arch-sub"><span class="arch-pill">UI · bloc/cubit · go_router</span><span class="arch-pill">ApiClient · dio · Bearer-Token · Accept-Language · Auto-Refresh</span></div></div><div class="arch-link"><span class="arch-vline"></span><span class="arch-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span><span class="arch-link-labels"><span>HTTPS · REST <code>/api/v1</code></span><span>SSE · Live-Updates</span></span></div><div class="arch-node glass"><div class="arch-node-top"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="8" x="2" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/></svg></span><span class="arch-txt"><strong>Server: hinata-server</strong><em>Spring Boot 4 · Java 21</em></span></div><div class="arch-sub"><span class="arch-pill">Controller → Services → Repositories</span><span class="arch-pill">JWT-Auth · Rate-Limiting · lokalisierte Fehler</span><span class="arch-pill">Laufzeiteinstellungen aus MongoDB (überschreiben env)</span></div></div><div class="arch-link"><span class="arch-vline"></span><span class="arch-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span></div><div class="arch-stores"><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg></span><strong>MongoDB</strong><em>Replica Set · X.509</em></div><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg></span><strong>S3 / MinIO</strong><em>Anhänge · presigned</em></div><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg></span><strong>SMTP</strong><em>Ausgehende E-Mail</em></div><div class="arch-store glass"><span class="arch-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/><path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/><circle cx="12" cy="12" r="2"/><path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/><path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"/></svg></span><strong>Connect</strong><em>Push · Universal Links</em></div></div></div>

- **App (Flutter)**: eine Codebasis für sechs Ziele, nämlich Android, iOS, Web, macOS, Windows und Linux (eine native GTK-3-Desktop-App mit der Application-ID `com.ahmadre.hinata`). State mit bloc/cubit, Routing mit go_router, Übersetzungen mit i18next (Englisch + Deutsch), Netzwerk über **dio** in einem `ApiClient`. Diagramme zeichnet fl_chart.
- **Server (Spring Boot 4, Java 21)**: stellt die REST-API unter `/api/v1` bereit, enthält die gesamte Geschäftslogik und Autorisierung und streamt Live-Updates.
- **MongoDB**: hält alle Daten. In Produktion läuft ein **Replica Set** (2 Datenknoten + 1 Arbiter) mit TLS und X.509-Client-Authentifizierung.
- **S3 / MinIO**: Objektspeicher für Anhänge und Avatare, mit zufälligen Objektschlüsseln und vorsignierten Downloads.
- **SMTP**: ausgehende Mail (Verifizierung, Benachrichtigungen, Passwort-Reset). In der Entwicklung übernimmt das Mailpit.
- **Hinata Connect Gateway**: zentrales Relay für Push und Universal Links. So bedient die eine veröffentlichte App viele selbst gehostete Server.

## Der Weg App → Server

Jeder Netzwerkaufruf der App läuft durch einen einzigen `ApiClient` auf Basis von **dio**. Er kümmert sich um Tokens und Header, die einzelnen Screens müssen das nicht:

- Er hängt das aktuelle **Bearer-Access-Token** an authentifizierte Anfragen.
- Er sendet **`Accept-Language`** (`en` oder `de`), damit der Server Fehlermeldungen lokalisiert.
- Bei `401` ruft er den Refresh-Endpunkt auf, holt ein neues Access-Token und **wiederholt die Anfrage einmal**. Scheitert der Refresh, leert er die Sitzung und leitet zum Login.

Der Server bietet eine stabile, versionierte Schnittstelle unter **`/api/v1`**. Alle Endpunkte stehen in der [API-Referenz](/de/api.html).

!!! info "Mehrere Server von Anfang an"
    Die native App hat keine fest eingebaute Server-URL. Nutzer speichern einen oder mehrere Server und wechseln zwischen ihnen. Access-Tokens gelten **pro Server**. Der Web-Build kann seine eigene Origin als Standard nutzen. Deshalb funktioniert dieselbe veröffentlichte App mit jedem Hinata-Server. Siehe [Branding & eigene Clients](/de/self-hosted-app.html).

## Live-Updates mit SSE

Der Server schickt Änderungen per **Server-Sent Events (SSE)** an verbundene Clients, statt dass sie pollen. Beispiel Anhänge: Kommt an einem Vorgang eine Datei dazu oder fällt weg, bekommt jeder offene Client, der den Vorgang streamt, die Änderung sofort über:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

SSE ist ein einseitiger, langlebiger HTTP-Stream. Das ist günstig, kommt gut durch Proxys und braucht kein WebSocket-Upgrade. Dein [Reverse Proxy](/de/reverse-proxy.html) darf diese Antworten nicht puffern.

## Ablauf einer Anfrage & Token-Refresh

Eine typische authentifizierte Anfrage:

1. **App**: sendet die Anfrage über `ApiClient`. dio hängt Bearer-Access-Token und `Accept-Language` an.
2. **Server**: prüft das JWT (HS512), erzwingt Rate-Limits pro IP und prüft die Berechtigung (z. B. braucht `/api/v1/admin/**` die Rolle `ADMIN`).
3. **Controller → Service → Repository**: Der Service wendet die Geschäftsregeln an und liest oder schreibt MongoDB. Die Dateien von Anhängen gehen an S3/MinIO.
4. **Antwort**: stabiles, lokalisiertes JSON. Entweder die Nutzdaten oder ein Fehler aus `messages.properties` in der Sprache des Clients, ohne Stacktraces.

Access-Tokens sind **kurzlebig**. Refresh-Tokens leben länger, werden aber **für API-Zugriff abgelehnt** und können nur neue Access-Tokens ausstellen. Läuft ein Access-Token mitten in der Sitzung ab, merkt der Nutzer vom Refresh nichts:

```text
App ──GET /issues (abgelaufenes Access-Token)──▶ Server
App ◀──────────── 401 Unauthorized ──────────────── Server
App ──POST /auth/refresh (Refresh-Token)────────▶ Server
App ◀──────── neues Access-Token ────────────────── Server
App ──GET /issues (wiederholt, neues Token)─────▶ Server
App ◀──────────────── 200 OK ──────────────────────── Server
```

Das vollständige Token-Modell steht unter [Authentifizierung](/de/authentication.html).

## Laufzeiteinstellungen in MongoDB

Der Großteil der Betriebskonfiguration liegt **in MongoDB und wird im Adminbereich der App verwaltet**. Beim Start fest in Umgebungsvariablen steht sie nicht. Dazu gehören SSO-Provider, E-Mail-Eingang (IMAP), Push, Git-OAuth-Apps und App-Einstellungen wie die minimale Client-Version.

Daraus folgen zwei Regeln:

- **Die Datenbank überschreibt die Umgebung.** Umgebungsvariablen wie `hinata.app.*` sind Standardwerte. Ein Wert aus dem Adminbereich gewinnt.
- **Änderungen greifen ohne Neustart.** Ein geänderter SSO-Provider oder ein Feature-Flag wirkt ab der nächsten Anfrage, ohne Redeploy oder Neustart des Containers.

!!! tip "Secrets sind write-only"
    In der Admin-API sind Secrets (OAuth-Client-Secrets, Tokens, Passwörter) **write-only**. Du kannst sie setzen, zurückgegeben werden sie nie. Gespeicherte Git-Access-Tokens liegen zusätzlich mit AES-GCM verschlüsselt in der Datenbank.

Für den Start reichen deshalb wenige Umgebungsvariablen (siehe [Konfigurationsreferenz](/de/configuration.html)). Alles andere stellst du ein, sobald der Server läuft.

## Lokalisierte Fehler

Fehlermeldungen entstehen **auf dem Server** aus Resource-Bundles: `messages.properties` (Englisch, Standard) und `messages_de.properties` (Deutsch). Maßgeblich ist der `Accept-Language`-Header des Clients. Der Server liefert einen stabilen, maschinenlesbaren Fehler, dessen Meldung schon in der richtigen Sprache ist. Der Client übersetzt nichts selbst.

## Das Connect Gateway

Push-Benachrichtigungen und Universal Links laufen über das **Hinata Connect Gateway**, einen gehosteten Dienst des App-Herausgebers. Sie sind nicht in jeden Server eingebaut.

- Dein Server verbindet sich mit dem Gateway. Die Push-Zugangsdaten der App liegen dort, deshalb brauchen **Self-Hoster kein eigenes Firebase-Projekt**.
- Universal Links öffnen die App auf dem richtigen Server, egal woher Einladung oder Reset-Link stammen.
- Der App-Herausgeber betreibt und sichert das Gateway. Self-Hoster müssen es weder betreiben noch verwalten. `HINATA_GATEWAY_BASE_URL` änderst du nur, wenn du eine eigene gebrandete App ausrollst.

!!! note "Linux bekommt die Benachrichtigungen, aber kein Push"
    Push braucht einen Zustelldienst des Betriebssystems. Unter Linux gibt es keinen, `firebase_messaging` hat keine Linux-Implementierung. Ein Linux-Client registriert deshalb nie ein Push-Token, und das Gateway kann ihm nichts zustellen. Die Ereignisse erreichen den Nutzer trotzdem im Benachrichtigungscenter der App und per E-Mail. Der Push-Schalter in den Kontoeinstellungen bleibt aktiv. Die Einstellung gehört zum Konto und steuert weiter das Telefon derselben Person.

So bedient die eine veröffentlichte App beliebig viele unabhängige, selbst gehostete Hinata-Server. Siehe [Hinata Connect Gateway](/de/connect-gateway.html).

## Wohin als Nächstes

- [Grundkonzepte](/de/concepts.html): das Vokabular, auf dem API und UI aufbauen.
- [Self-Hosting-Überblick](/de/self-hosting.html): welche Container du für diese Komponenten deployst.
- [Sicherheitsmodell](/de/security.html): die Garantien hinter dem Anfragepfad oben.
