---
title: API-Referenz
description: Orientierung für die Hinata-REST-API unter /api/v1 — das Bearer-Token-Authentifizierungsmodell, öffentliche Endpunkte, Live-SSE-Streams und die Scalar-Docs-UI.
---

# API-Referenz

Hinata stellt eine stabile, versionierte REST-API unter **`/api/v1`** bereit. Jedes
Feature, das du in der App siehst — Projekte, Vorgänge, Boards, Sprints, die
Wissensdatenbank — wird von genau dieser Fläche angetrieben, sodass alles, was der
Client kann, auch deine eigenen Skripte und Integrationen können. Diese Seite ist
eine **Orientierung**, kein erschöpfender Abzug jedes Endpunkts: Sie behandelt das
Authentifizierungsmodell, die Handvoll öffentlicher Endpunkte, wie Live-Updates über
SSE streamen und wie du die vollständige Fläche interaktiv erkundest.

!!! info "Das ist eine Karte, nicht das Gelände"
    Die API ist groß und entwickelt sich mit der Plattform. Statt hier jede Route zu
    duplizieren (und zu veralten), lehrt dich diese Seite die überall geltenden
    Regeln und verweist dich dann auf die [Scalar-Docs-UI](#die-vollstandige-flache-erkunden)
    für die vollständige, stets aktuelle Endpunktliste.

## Basis-URL und Versionierung

Alle Endpunkte liegen unter dem Präfix `/api/v1` auf dem öffentlichen API-Host deines Servers:

```text
https://api.track.example.com/api/v1
```

Das Segment `v1` ist die Vertragsversion. Breaking Changes würden unter einem neuen
Präfix ausgeliefert, sodass du sicher auf `v1` pinnen kannst. In der App ist diese
Basis das, was du pro Server konfigurierst; in deinen eigenen Clients behandle
`https://api.track.example.com/api/v1` als Wurzel und hänge die unten stehenden Pfade an.

## Authentifizierungsmodell

Hinata verwendet **Stateless JWTs (HS512)**. Es gibt zwei Arten von Token, und die
Unterscheidung ist wichtig:

| Token | Lebensdauer | Wofür es da ist |
| --- | --- | --- |
| **Access-Token** | Kurzlebig | Das Bearer-Zugangsdatum, das du bei jeder authentifizierten Anfrage sendest. |
| **Refresh-Token** | Länger lebend | Wird **nur** verwendet, um über `/auth/refresh` ein neues Access-Token auszustellen. |

Du authentifizierst eine Anfrage, indem du das Access-Token in den `Authorization`-Header legst:

```text
Authorization: Bearer <access-token>
```

!!! warning "Refresh-Tokens werden für API-Zugriff abgelehnt"
    Ein Refresh-Token kann **nur** an `/auth/refresh` gegen ein neues Access-Token
    getauscht werden — es wird an keinem anderen Endpunkt als Bearer-Zugangsdatum
    akzeptiert. Sendest du ein Refresh-Token als `Authorization: Bearer …` an etwa
    `/issues`, wird die Anfrage abgelehnt. Rufe einen authentifizierten Endpunkt immer
    mit einem frischen **Access**-Token auf.

Wenn ein Access-Token abläuft, tausche dein Refresh-Token gegen ein neues, statt dich
erneut anzumelden:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"refreshToken":"<refresh-token>"}'
```

Die App tut das transparent: Ihr `ApiClient` fängt ein `401` ab, ruft
`/auth/refresh`, tauscht das neue Access-Token ein und wiederholt die ursprüngliche
Anfrage einmal. Siehe [Authentifizierung](/de/authentication.html) für das vollständige Token-Modell.

### Lokalisierte Fehler mit Accept-Language

Sende einen **`Accept-Language`**-Header (`en` oder `de`) und der Server lokalisiert
Fehlermeldungen für dich — sie werden serverseitig aus Ressourcen-Bundles aufgelöst,
die anhand dieses Headers verschlüsselt sind. Ein deutscher Client erhält deutschen
Fehlertext ohne jegliche Übersetzungslogik im Client:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept-Language: de'
```

Fehler sind stabiles, maschinenlesbares JSON mit einer menschlichen `message` bereits
in der angeforderten Sprache und enthalten niemals Stacktraces.

## Öffentliche Endpunkte (kein Token)

Eine kleine Menge von Endpunkten ist **ohne** Bearer-Token erreichbar — alles, was
die App braucht, bevor ein Benutzer angemeldet ist (den Server entdecken,
Setup-Status prüfen, anmelden). Alles andere erfordert Authentifizierung.

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
    Jeder Pfad, der nicht in der obigen Tabelle steht, erfordert ein gültiges
    **Access**-Token. Admin-Routen unter `/api/v1/admin/**` erfordern zusätzlich die
    Rolle `ADMIN`.

## Anmelden, dann die API aufrufen

Der Alltags-Flow: `POST /auth/login`, um Tokens zu erhalten, dann sende das
zurückgegebene Access-Token als Bearer-Zugangsdatum bei nachfolgenden Aufrufen.

**1. Anmelden** und ein Access-Token sowie ein Refresh-Token erhalten:

```bash
curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -H 'Accept-Language: en' \
  -d '{"usernameOrEmail":"rebar","password":"your-password"}'
```

Die Antwort enthält die Tokens (Feldnamen können `accessToken` und `refreshToken`
einschließen) plus den angemeldeten Benutzer. Kopiere das **Access-Token**.

**2. Rufe einen authentifizierten Endpunkt** mit diesem Token als Bearer-Zugangsdatum auf:

```bash
curl -sS https://api.track.example.com/api/v1/projects \
  -H 'Authorization: Bearer <access-token>'
```

!!! tip "Erfasse das Token in einem Schritt"
    Mit `jq` kannst du dich anmelden und das Access-Token zur Wiederverwendung in
    einer Shell ablegen:

    ```bash
    TOKEN=$(curl -sS -X POST https://api.track.example.com/api/v1/auth/login \
      -H 'Content-Type: application/json' \
      -d '{"usernameOrEmail":"rebar","password":"your-password"}' \
      | jq -r '.accessToken')

    curl -sS https://api.track.example.com/api/v1/projects \
      -H "Authorization: Bearer $TOKEN"
    ```

Ist TOTP-Zwei-Faktor für das Konto aktiviert, gibt `/auth/login` eine 2FA-Abfrage
statt Tokens zurück; schließe die Abfrage ab, um sie zu erhalten. Siehe
[Authentifizierung](/de/authentication.html).

## Live-Updates mit Server-Sent Events

Manche Ressourcen pushen Änderungen über **Server-Sent Events (SSE)** an verbundene
Clients, statt dass du pollen musst. Das klarste Beispiel sind **Anhänge**: Wird eine
Datei zu einem Vorgang hinzugefügt oder von ihm entfernt, wird jeder Client, der
diesen Vorgang streamt, sofort benachrichtigt unter:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

Öffne den Stream mit `curl` (das Flag `-N` deaktiviert das Puffern, sodass Events
ausgegeben werden, sobald sie eintreffen):

```bash
curl -N https://api.track.example.com/api/v1/issues/ASTA-42/attachments/stream \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Accept: text/event-stream'
```

Die Verbindung bleibt offen und sendet ein Event, jedes Mal wenn sich die Anhänge des
Vorgangs ändern. SSE ist ein einseitiger, langlebiger HTTP-Stream — kein
WebSocket-Upgrade erforderlich.

!!! warning "Deaktiviere Proxy-Puffern für SSE"
    Ein Reverse Proxy, der Antworten puffert, hält SSE-Events zurück, bis die
    Verbindung schließt, was so aussieht, als „funktionierten Live-Updates nicht".
    Schalte das Puffern für den Stream-Pfad aus (zum Beispiel `proxy_buffering off;`
    bei nginx). Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html) und die
    [FAQ](/de/faq.html).

## Rate Limiting

Die API ist **pro Client-IP** mit bucket4j ratenlimitiert, mit einem strengen Budget
auf Authentifizierungsrouten, um Brute-Force-Versuche abzuschwächen:

| Bereich | Standardlimit | Umgebungsvariable |
| --- | --- | --- |
| Allgemeine API | **300** Anfragen/Minute | `HINATA_RATE_LIMIT_API` |
| `/auth/**` | **10** Anfragen/Minute | `HINATA_RATE_LIMIT_AUTH` |

Rate Limiting wird über `HINATA_RATE_LIMIT_ENABLED` umgeschaltet (standardmäßig an).
Wiederholt fehlgeschlagene Logins lösen zusätzlich eine **datenbankgestützte Sperre**
aus (`HINATA_MAX_LOGIN_FAILURES`, Standard 5; `HINATA_LOGIN_BLOCK_MINUTES`, Standard
15), die Neustarts übersteht.

!!! tip "Hinter einem Reverse Proxy: setze Trusted Proxies"
    Rate Limiting schlüsselt auf die Client-IP. Sitzt dein Server hinter einem Proxy
    und hast du `HINATA_TRUSTED_PROXIES` nicht auf die CIDR des Proxys gesetzt,
    scheint jede Anfrage vom Proxy zu kommen und teilt sich einen Bucket. Siehe
    [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Die vollständige Fläche erkunden

Die vollständige, stets aktuelle Endpunktliste wird von einer interaktiven
**Scalar-API-Docs-UI** ausgeliefert, gesichert durch das Flag `HINATA_DOCS_ENABLED`.
Sie ist **in Produktion standardmäßig aus**, sodass du deine gesamte API-Fläche nie
an die Öffentlichkeit preisgibst — aber sie ist der beste Weg, jede Route, jedes
Schema und jeden Parameter während der Entwicklung zu durchstöbern.

Aktiviere sie lokal, indem du das Flag setzt, bevor du den Server startest:

```bash
HINATA_DOCS_ENABLED=true ./mvnw spring-boot:run
```

Oder in einer `.env`-/Compose-Umgebung:

```properties
HINATA_DOCS_ENABLED=true
```

Öffne dann die Docs-UI in deinem Browser unter der Basis-URL deines Servers. Weil sie
die gesamte Fläche exponiert, **lasse `HINATA_DOCS_ENABLED=false` in Produktion** und
nutze sie nur auf einer Dev-Instanz.

!!! danger "Exponiere die Docs-UI nicht in Produktion"
    Die Scalar-UI beschreibt jeden Endpunkt und jedes Schema. Halte sie auf
    internetzugewandten Deployments deaktiviert; aktiviere sie nur auf
    vertrauenswürdigen, lokalen Dev-Servern.

## Wie geht es weiter

- [Authentifizierung](/de/authentication.html) — der vollständige Token-Lebenszyklus, 2FA und SSO-Login.
- [Single Sign-on (SSO)](/de/sso.html) — OIDC / OAuth2 / SAML / LDAP und `/auth/sso/providers`.
- [Git-Integration](/de/git-integration.html) — OAuth-Flow und signaturverifizierte Webhook-Endpunkte.
- [Entwicklung](/de/development.html) — den Server aus dem Quellcode betreiben, um die API mit der Docs-UI zu erkunden.
