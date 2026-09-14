---
title: API-Referenz
description: Einstieg in die Hinata-REST-API unter /api/v1 mit Bearer-Tokens, öffentlichen Endpunkten, SSE-Streams und der Scalar-Docs-UI.
---

# API-Referenz

Hinata stellt eine stabile, versionierte REST-API unter **`/api/v1`** bereit. Die App
nutzt genau diese API für alles, von Projekten und Vorgängen über Boards und Sprints
bis zur Wissensdatenbank. Deine Skripte und Integrationen können also alles, was der
Client kann.

Diese Seite ist eine **Orientierung**. Sie erklärt die Regeln, die überall gelten.
Die vollständige, stets aktuelle Endpunktliste zeigt die
[Scalar-Docs-UI](#die-vollständige-fläche-erkunden).

## Basis-URL und Versionierung

Alle Endpunkte liegen unter dem Präfix `/api/v1` auf dem öffentlichen API-Host deines Servers:

```text
https://api.track.example.com/api/v1
```

`v1` ist die Vertragsversion. Breaking Changes kämen unter einem neuen Präfix, du
kannst dich also auf `v1` festlegen. In der App konfigurierst du diese Basis pro
Server. In eigenen Clients hängst du die Pfade unten an
`https://api.track.example.com/api/v1` an.

## Authentifizierungsmodell

Hinata nutzt **zustandslose JWTs (HS512)** mit zwei Arten von Token:

| Token | Lebensdauer | Wofür es da ist |
| --- | --- | --- |
| **Access-Token** | Kurzlebig | Das Bearer-Zugangsdatum, das du bei jeder authentifizierten Anfrage sendest. |
| **Refresh-Token** | Länger lebend | Wird **nur** verwendet, um über `/auth/refresh` ein neues Access-Token auszustellen. |

Das Access-Token gehört in den `Authorization`-Header:

```text
Authorization: Bearer <access-token>
```

!!! warning "Refresh-Tokens werden für API-Zugriff abgelehnt"
    Ein Refresh-Token lässt sich **nur** an `/auth/refresh` gegen ein neues
    Access-Token tauschen. An jedem anderen Endpunkt wird es als Bearer-Zugangsdatum
    abgelehnt, zum Beispiel als `Authorization: Bearer …` an `/issues`. Rufe
    authentifizierte Endpunkte immer mit einem gültigen **Access**-Token auf.

Läuft das Access-Token ab, tauschst du dein Refresh-Token gegen ein neues, statt dich
neu anzumelden:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"refreshToken":"<refresh-token>"}'
```

Die App macht das automatisch. Ihr `ApiClient` fängt ein `401` ab, ruft
`/auth/refresh`, übernimmt das neue Access-Token und wiederholt die Anfrage einmal.
Das vollständige Token-Modell steht unter [Authentifizierung](/de/authentication.html).

### Lokalisierte Fehler mit Accept-Language

Sendest du den Header **`Accept-Language`** (`en` oder `de`), bekommst du
Fehlermeldungen in dieser Sprache. Der Server löst sie aus Resource-Bundles auf, der
Client braucht keine Übersetzungslogik:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept-Language: de'
```

Fehler sind stabiles, maschinenlesbares JSON. Die `message` ist schon in der
angefragten Sprache. Stacktraces sind nie enthalten.

## Öffentliche Endpunkte (kein Token)

Diese Endpunkte gehen **ohne** Bearer-Token. Die App braucht sie, bevor jemand
angemeldet ist: um den Server zu finden, den Setup-Status zu prüfen und sich
anzumelden.

| Methode | Endpunkt | Zweck |
| --- | --- | --- |
| `GET` | `/meta` | Server-Metadaten: minimale App-Version, Datenschutz-URL, Auth-Feature-Flags. |
| `GET` | `/setup/status` | Ob das Erststart-Setup abgeschlossen wurde. |
| `POST` | `/setup` | Erststart-Setup abschließen (Organisation + erster Admin). |
| `POST` | `/auth/login` | Zugangsdaten gegen Access- + Refresh-Tokens tauschen. |
| `POST` | `/auth/refresh` | Ein Refresh-Token gegen ein neues Access-Token tauschen. |
| `GET` | `/auth/sso/providers` | Die konfigurierten SSO-Provider auflisten (OIDC, OAuth2, SAML, LDAP). |
| `GET` | `/actuator/health` | Liveness-/Health-Probe für Load Balancer und Uptime-Checks. |

!!! note "Alles andere braucht ein Bearer-Token"
    Jeder Pfad, der nicht in der Tabelle steht, braucht ein gültiges
    **Access**-Token. Admin-Routen unter `/api/v1/admin/**` brauchen zusätzlich die
    Rolle `ADMIN`.

## Anmelden, dann die API aufrufen

Der normale Ablauf: Mit `POST /auth/login` holst du Tokens. Das Access-Token sendest
du dann bei jedem weiteren Aufruf als Bearer-Zugangsdatum.

**1. Anmelden** und Access-Token und Refresh-Token erhalten:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -H 'Accept-Language: en' \
  -d '{"usernameOrEmail":"rebar","password":"your-password"}'
```

Die Antwort enthält die Tokens (Feldnamen können `accessToken` und `refreshToken`
sein) und den angemeldeten Benutzer. Kopiere das **Access-Token**.

**2. Authentifizierten Endpunkt aufrufen**, mit dem Token als Bearer-Zugangsdatum:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>'
```

!!! tip "Erfasse das Token in einem Schritt"
    Mit `jq` meldest du dich an und legst das Access-Token in der Shell zur
    Wiederverwendung ab:

    ```bash
    TOKEN=$(curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
      -H 'Content-Type: application/json' \
      -d '{"usernameOrEmail":"rebar","password":"your-password"}' \
      | jq -r '.accessToken')

    curl -sS https://api.track.example.com/api/v1/projects \
      -H "Authorization: Bearer $TOKEN"
    ```

Ist TOTP-Zwei-Faktor für das Konto aktiv, liefert `/auth/login` statt Tokens eine
2FA-Abfrage. Die Tokens gibt es, sobald die Abfrage abgeschlossen ist. Siehe
[Authentifizierung](/de/authentication.html).

## Live-Updates mit Server-Sent Events

Manche Ressourcen schicken Änderungen per **Server-Sent Events (SSE)** an verbundene
Clients, du musst also nicht pollen. Das klarste Beispiel sind **Anhänge**: Kommt an
einem Vorgang eine Datei dazu oder fällt weg, erfährt das jeder Client sofort, der
diesen Vorgang streamt:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

Öffne den Stream mit `curl`. Das Flag `-N` schaltet das Puffern ab, damit Events
sofort erscheinen:

```bash
curl -N https://api.track.example.com/api/v1/issues/ASTA-42/attachments/stream \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept: text/event-stream'
```

Die Verbindung bleibt offen und sendet bei jeder Änderung an den Anhängen ein Event.
SSE ist ein einseitiger, langlebiger HTTP-Stream und braucht kein WebSocket-Upgrade.

!!! warning "Deaktiviere Proxy-Puffern für SSE"
    Puffert ein Reverse Proxy die Antworten, hält er SSE-Events zurück, bis die
    Verbindung schließt. Dann sieht es so aus, als „funktionierten Live-Updates
    nicht“. Schalte das Puffern für den Stream-Pfad ab (zum Beispiel
    `proxy_buffering off;` bei nginx). Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html)
    und die [FAQ](/de/faq.html).

## Rate Limiting

Die API ist mit bucket4j **pro Client-IP** begrenzt. Für Anmelderouten gilt ein
strenges Budget gegen Brute Force:

| Bereich | Standardlimit | Umgebungsvariable |
| --- | --- | --- |
| Allgemeine API | **300** Anfragen/Minute | `HINATA_RATE_LIMIT_API` |
| `/auth/**` | **10** Anfragen/Minute | `HINATA_RATE_LIMIT_AUTH` |

Einzige Ausnahme ist `GET /auth/sso/providers`. Es zählt zum allgemeinen Budget. Der
Anmeldebildschirm fragt den Endpunkt bei jedem Aufruf ab, um die SSO-Buttons zu
zeichnen, und die Antwort verrät nichts Erratbares.

`HINATA_RATE_LIMIT_ENABLED` schaltet das Rate Limiting (standardmäßig an).
Wiederholt fehlgeschlagene Logins lösen zusätzlich eine **Sperre in der Datenbank**
aus, die Neustarts übersteht:

- `HINATA_MAX_LOGIN_FAILURES`, Standard 5
- `HINATA_LOGIN_BLOCK_MINUTES`, Standard 15

!!! tip "Hinter einem Reverse Proxy: setze Trusted Proxies"
    Das Rate Limiting richtet sich nach der Client-IP. Steht dein Server hinter
    einem Proxy und ist `HINATA_TRUSTED_PROXIES` nicht auf den CIDR des Proxys
    gesetzt, kommt jede Anfrage scheinbar vom Proxy. Dann teilen sich alle einen
    Bucket. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Die vollständige Fläche erkunden

Die vollständige, stets aktuelle Endpunktliste liefert eine interaktive
**Scalar-API-Docs-UI**. Sie hängt am Flag `HINATA_DOCS_ENABLED` und ist **in
Produktion standardmäßig aus**, damit deine API nicht öffentlich beschrieben wird. In
der Entwicklung ist sie der beste Weg, Routen, Schemas und Parameter durchzusehen.

Aktiviere sie lokal, bevor du den Server startest:

```bash
HINATA_DOCS_ENABLED=true ./gradlew bootRun
```

Oder in einer `.env`-/Compose-Umgebung:

```properties
HINATA_DOCS_ENABLED=true
```

Die Docs-UI öffnest du dann im Browser unter der Basis-URL deines Servers.

!!! danger "Exponiere die Docs-UI nicht in Produktion"
    Die Scalar-UI beschreibt jeden Endpunkt und jedes Schema. Lass
    `HINATA_DOCS_ENABLED=false` auf Servern, die aus dem Internet erreichbar sind.
    Aktiviere sie nur auf vertrauenswürdigen, lokalen Dev-Instanzen.

## Wie geht es weiter

- [Authentifizierung](/de/authentication.html): der vollständige Token-Lebenszyklus, 2FA und SSO-Login.
- [Single Sign-on (SSO)](/de/sso.html): OIDC / OAuth2 / SAML / LDAP und `/auth/sso/providers`.
- [Git-Integration](/de/git-integration.html): OAuth-Flow und Webhook-Endpunkte mit Signaturprüfung.
- [Entwicklung](/de/development.html): den Server aus dem Quellcode starten und die API in der Docs-UI erkunden.
