---
title: Sicherheitsmodell
description: Hinatas Härtungskonzept, abgebildet auf die OWASP Top 10 — JWT-Design, BCrypt, Login-Sperre, Rate Limiting, gehärtete Header, sichere Uploads und Verschlüsselung im Ruhezustand.
---

# Sicherheitsmodell

Hinata ist dafür gebaut, dem öffentlichen Internet ausgesetzt zu werden. Diese Seite dokumentiert die Härtung der Plattform — die konkreten Maßnahmen, die Umgebungsvariablen, die sie einstellen, und eine **Betreiber-Checkliste** für ein sicheres Produktiv-Deployment. Alles Folgende ist auf die **OWASP Top 10** abgebildet, damit du die Abdeckung nachvollziehen kannst.

Für die benutzerseitige Seite der Authentifizierung (Registrierung, 2FA, Sitzungen) siehe [Authentifizierung](/de/authentication.html), und für föderiertes Login siehe [Single Sign-on](/de/sso.html).

## Tokens und Passwörter

- **Stateless JWT, HS512.** Access-Tokens sind kurzlebig; ein separates **Refresh-Token** stellt neue Access-Tokens aus. Entscheidend: Ein **Refresh-Token wird für normalen API-Zugriff abgelehnt** — es wird nur am Refresh-Endpunkt akzeptiert. Ein gestohlenes Access-Token läuft schnell ab; ein gestohlenes Refresh-Token kann nicht zum Lesen von Daten verwendet werden.
- **Widerrufbare Sitzungen.** Jedes Token trägt eine Session-ID (`sid`), die an einen Datensatz in der `sessions`-Collection gebunden ist, sodass einzelne Sitzungen widerrufen werden können, ohne das Signaturgeheimnis zu rotieren. Siehe [Authentifizierung → Sitzungen](/de/authentication.html).
- **BCrypt Stärke 12** für das Passwort-Hashing, mit einer **Mindestlänge von 10 Zeichen**. Länge plus ein bewusst langsamer Hash ist die Kernverteidigung gegen Brute Force von Zugangsdaten.

!!! danger "Ändere das JWT-Secret, bevor du den Server exponierst"
    `HINATA_JWT_SECRET` ist der HS512-Signaturschlüssel und muss in Produktion ein echtes Secret von **mindestens 64 Zeichen** sein. Generiere eines mit:
    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```
    Wer dieses Secret kennt, kann Tokens für jeden Benutzer fälschen. Liefere niemals den Standardwert aus.

## Login-Sperre und Rate Limiting

Zwei unabhängige Schichten schützen die Zugangsdaten- und API-Angriffsfläche.

**Datenbankgestützte Login-Sperre** zählt fehlgeschlagene Logins und sperrt das Konto/den Identifier nach einem Schwellwert. Da der Zähler in MongoDB lebt, **übersteht die Sperre Neustarts** und funktioniert über mehrere Serverinstanzen hinweg.

| Variable | Standard | Zweck |
| --- | --- | --- |
| `HINATA_MAX_LOGIN_FAILURES` | `5` | Fehlversuche, bevor der Identifier gesperrt wird |
| `HINATA_LOGIN_BLOCK_MINUTES` | `15` | Wie lange die Sperre andauert |

**Rate Limiting pro IP** (über **bucket4j**) deckelt das Anfragevolumen pro Client-IP, mit einem **strengeren Budget auf `/auth/**`**, um Password Spraying und Enumeration abzuschwächen.

| Variable | Standard | Zweck |
| --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | `true` | Hauptschalter für Rate Limiting |
| `HINATA_RATE_LIMIT_API` | `300` | Anfragen pro Minute für die allgemeine API |
| `HINATA_RATE_LIMIT_AUTH` | `10` | Anfragen pro Minute für `/auth/**` (streng) |

!!! warning "Rate Limiting braucht die echte Client-IP"
    Hinter einem Reverse Proxy scheint jede Anfrage vom Proxy zu kommen, es sei denn, du sagst Hinata, welchen Proxies es vertrauen soll. Setze `HINATA_TRUSTED_PROXIES` auf die CIDR(s) deines Load Balancers/Proxys, damit `X-Forwarded-For` nur von diesen honoriert wird. Lässt du es leer, vertraut Hinata keinem weitergeleiteten Header — sicher, aber jeder Client sieht aus wie der Proxy. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Autorisierung

- **Rollen-gesicherte Admin-Fläche.** Jede Route unter **`/api/v1/admin/**` erfordert die Rolle `ADMIN`**; ein normales Token kann keine Admin-Funktionen erreichen.
- **Mandanten-/Projekt-Sichtbarkeit.** Team-Mitgliedschaft steuert die Projekt-Sichtbarkeit app-weit — ein Benutzer sieht nur Projekte, die sein Team gewährt (siehe [Projekte & Teams](/de/projects-teams.html)).
- **Öffentliche Endpunkte sind explizit.** Nur eine kleine Allowlist ist ohne Token erreichbar: `/meta`, `/setup/status`, `/setup`, `/auth/login`, `/auth/refresh`, `/auth/sso/providers`, `/actuator/health`. Alles andere verlangt ein Bearer-Token.

## Gehärtete HTTP-Antworten

- **Security-Header** auf jeder Antwort: **HSTS** (HTTPS erzwingen), eine restriktive **Content-Security-Policy** und **`Referrer-Policy: no-referrer`**, unter anderem.
- **Stabile, lokalisierte JSON-Fehler ohne Stacktraces.** Fehler werden serverseitig aus Message-Bundles anhand des `Accept-Language` des Clients aufgelöst und in einer konsistenten Form zurückgegeben — keine internen Pfade, Klassennamen oder Stacktraces dringen zu Clients durch.
- **Regex-escapte Sucheingabe.** Von Benutzern gelieferte Suchbegriffe werden escaped, bevor sie die Query-Schicht erreichen, sodass ein präparierter Begriff nicht zu einem injizierten/teuren regulären Ausdruck werden kann.

## Datei-Uploads und Objektspeicher

- **Content-Type und Größe werden validiert** beim Upload, sodass Clients keine unerlaubten oder überdimensionierten Dateien einschleusen können (Limits sind ENV-gesteuert).
- **Randomisierte S3-Objektschlüssel**, sodass gespeicherte Objekte nicht per Name erratbar oder enumerierbar sind.
- **Presigned Downloads** — Anhänge werden über kurzlebige Presigned-URLs statt über einen öffentlichen Bucket ausgeliefert, sodass der Zugriff eingegrenzt und zeitlich befristet ist.

## Verschlüsselung im Ruhezustand für Integrations-Secrets

Git-Access-Tokens und andere Integrations-Secrets werden **mit AES-GCM verschlüsselt**, bevor sie die Datenbank berühren, mit dem Schlüssel in **`HINATA_GIT_TOKEN_SECRET`**. Secrets sind **write-only in der Admin-API** — du kannst sie setzen, aber sie werden nie zurückgegeben. Ändere den Standardschlüssel in Produktion; das Rotieren re-keyt gespeicherte Tokens.

## OWASP-Top-10-Mapping

| OWASP Top 10 (2021) | Wie Hinata darauf eingeht |
| --- | --- |
| A01 Broken Access Control | `ADMIN`-gesicherte Admin-Routen, explizite öffentliche Allowlist, Team-/Projekt-Sichtbarkeitssteuerung, pro Sitzung widerrufbare Tokens |
| A02 Cryptographic Failures | JWT HS512, BCrypt-12-Passwörter, AES-GCM-Verschlüsselung von Integrations-Secrets im Ruhezustand, TLS überall (Betreiber) |
| A03 Injection | Regex-escapte Suche, parametrisierter Mongo-Zugriff, Content-Type-/Größen-validierte Uploads |
| A04 Insecure Design | Refresh-Tokens für API-Nutzung abgelehnt, write-only Secrets, Deep-Link-Auth-Callbacks, Mongo-gespeicherter Authorization-State |
| A05 Security Misconfiguration | Gehärtete Header (HSTS/CSP/no-referrer), API-Docs-UI in Prod standardmäßig aus, Trusted-Proxy-Allowlist, stabile Fehler ohne Stacktraces |
| A06 Vulnerable Components | Aktiv gepflegte Basis aus Spring Boot 4 / Java 21; Images aktuell halten (Betreiber) |
| A07 Identification & Auth Failures | Passwort-Mindestlängen, DB-gestützte Login-Sperre, strenges `/auth/**`-Rate-Limiting, TOTP-2FA, widerrufbare Sitzungen |
| A08 Software & Data Integrity | Signatur-verifizierte Git-Webhooks, Single-Apply-Commit-Ledger (siehe [Git-Integration](/de/git-integration.html)) |
| A09 Logging & Monitoring | `/actuator/health` für Probes; Fehler serverseitig geloggt, ohne Internas an Clients preiszugeben |
| A10 SSRF | Server-vermittelte Integrationen mit festen Provider-Endpunkten statt vom Client gelieferten URLs |

## Härtungs-Checkliste für Betreiber

!!! danger "Erledige das, bevor du live gehst"
    - **Ändere `HINATA_JWT_SECRET`** in ein frisches 64-Zeichen-Secret (`openssl rand -base64 64`).
    - **Ändere jedes Standardpasswort** — `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` und die TLS-Keystore-/Truststore-Passwörter (`HINATA_MONGO_TLS_*_PASSWORD`, Standard `changeit`).
    - **Ändere `HINATA_GIT_TOKEN_SECRET`**, sodass Integrations-Tokens mit deinem eigenen Schlüssel verschlüsselt werden.

!!! tip "Dann ziehe den Perimeter fester"
    - **TLS überall** — terminiere HTTPS an deinem Reverse Proxy und nutze TLS zwischen Diensten; betreibe MongoDB in Produktion mit X.509-Client-Auth (siehe [MongoDB & X.509](/de/database.html)).
    - **Setze `HINATA_TRUSTED_PROXIES`** auf die CIDR deines Proxys, damit Rate Limiting und Login-Sperre die echte Client-IP sehen.
    - **Deaktiviere die Docs-UI in Prod** — halte `HINATA_DOCS_ENABLED=false`, sodass die Scalar-API-Docs-UI nicht exponiert wird.
    - **Grenze CORS ein** — setze `HINATA_CORS_ALLOWED_ORIGINS` auf genau deine Web-App-Origin(s), nichts Breiteres.
    - **Halte Images aktuell** — ziehe regelmäßig neue `ghcr.io/hinata-platform`-Images für Security-Fixes; siehe [Backups & Upgrades](/de/backups.html).
    - **Halte die Server-Uhr synchron** (NTP) — erforderlich für korrektes Token-Ablaufen und SAML-SSO.

## Wie geht es weiter

- **[Authentifizierung](/de/authentication.html)** — das Zugangsdaten-System, 2FA und Sitzungswiderruf.
- **[Single Sign-on](/de/sso.html)** — Authentifizierung an deinen IdP delegieren.
- **[Konfigurationsreferenz](/de/configuration.html)** — jede Umgebungsvariable an einem Ort.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html)** — Trusted Proxies und TLS-Terminierung.
