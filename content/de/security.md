---
title: Sicherheitsmodell
description: So härtet Hinata die Plattform, abgebildet auf die OWASP Top 10, mit einer Checkliste für Betreiber.
---

# Sicherheitsmodell

Hinata ist für den Betrieb im öffentlichen Internet gebaut. Hier stehen die Schutzmaßnahmen, ihre Umgebungsvariablen und eine **Checkliste für Betreiber**, abgebildet auf die **OWASP Top 10**.

Registrierung, 2FA und Sitzungen aus Nutzersicht: [Authentifizierung](/de/authentication.html). Föderierter Login: [Single Sign-on](/de/sso.html).

## Tokens und Passwörter

- **Stateless JWT, HS512.** Access-Tokens sind kurzlebig, neue stellt ein separates **Refresh-Token** aus. Das **Refresh-Token wird für normalen API-Zugriff abgelehnt** und gilt nur am Refresh-Endpunkt. Ein gestohlenes Access-Token läuft schnell ab, ein gestohlenes Refresh-Token kann keine Daten lesen.
- **Widerrufbare Sitzungen.** Jedes Token trägt eine Session-ID (`sid`) mit Eintrag in der Collection `sessions`. So lassen sich einzelne Sitzungen widerrufen, ohne das Signaturgeheimnis zu wechseln. Siehe [Authentifizierung → Sitzungen](/de/authentication.html).
- **BCrypt mit Stärke 12** für Passwörter, **Mindestlänge 10 Zeichen**. Länge und ein bewusst langsamer Hash schützen vor Brute Force.

!!! danger "Ändere das JWT-Secret, bevor du den Server exponierst"
    `HINATA_JWT_SECRET` ist der Signaturschlüssel für HS512 und braucht in der Produktion **mindestens 64 Zeichen**. Generiere ihn mit:
    ```bash
    openssl rand -base64 64 | tr -d '\n'
    ```
    Wer das Secret kennt, kann Tokens für jeden Benutzer fälschen. Nutze nie den Standardwert.

## Login-Sperre und Rate Limiting

Zwei unabhängige Schichten schützen Logins und API.

**Login-Sperre in der Datenbank.** Fehlgeschlagene Logins werden gezählt. Ab einem Schwellwert wird Konto oder Identifier gesperrt. Der Zähler liegt in MongoDB, die Sperre **übersteht also Neustarts** und gilt über mehrere Serverinstanzen hinweg.

| Variable | Standard | Zweck |
| --- | --- | --- |
| `HINATA_MAX_LOGIN_FAILURES` | `5` | Fehlversuche, bevor der Identifier gesperrt wird |
| `HINATA_LOGIN_BLOCK_MINUTES` | `15` | Wie lange die Sperre andauert |

**Rate Limiting pro IP** (mit **bucket4j**) begrenzt die Anfragen pro Client-IP. Für `/auth/**` gilt ein **strengeres Budget** gegen Password Spraying und das Ausprobieren von Konten.

| Variable | Standard | Zweck |
| --- | --- | --- |
| `HINATA_RATE_LIMIT_ENABLED` | `true` | Hauptschalter für Rate Limiting |
| `HINATA_RATE_LIMIT_API` | `300` | Anfragen pro Minute für die allgemeine API |
| `HINATA_RATE_LIMIT_AUTH` | `10` | Anfragen pro Minute für `/auth/**` (streng. Die öffentliche Abfrage der SSO-Anbieter zählt aufs API-Budget) |

!!! warning "Rate Limiting braucht die echte Client-IP"
    Hinter einem Reverse Proxy kommt sonst jede Anfrage scheinbar vom Proxy. Setze `HINATA_TRUSTED_PROXIES` auf die CIDR(s) deines Load Balancers oder Proxys, dann gilt `X-Forwarded-For` nur von dort. Ist die Variable leer, vertraut Hinata keinem weitergeleiteten Header. Das ist sicher, aber alle Clients sehen aus wie der Proxy. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Autorisierung

- **Adminbereich nur mit Rolle.** Jede Route unter **`/api/v1/admin/**` verlangt die Rolle `ADMIN`**. Ein normales Token erreicht keine Adminfunktionen.
- **Sichtbarkeit von Mandanten und Projekten.** Die Teammitgliedschaft steuert in der ganzen App, welche Projekte jemand sieht: nur die, die sein Team freigibt (siehe [Projekte & Teams](/de/projects-teams.html)).
- **Öffentliche Endpunkte sind festgelegt.** Ohne Token erreichbar ist nur diese kurze Liste: `/meta`, `/setup/status`, `/setup`, `/auth/login`, `/auth/refresh`, `/auth/sso/providers`, `/actuator/health`. Alles andere verlangt ein Bearer-Token.

## Gehärtete HTTP-Antworten

- **Security-Header** auf jeder Antwort, unter anderem **HSTS** (erzwingt HTTPS), eine strenge **Content-Security-Policy** und **`Referrer-Policy: no-referrer`**.
- **Stabile, lokalisierte JSON-Fehler ohne Stacktraces.** Der Server holt Fehlertexte passend zum `Accept-Language` des Clients aus Message-Bundles und liefert sie immer im selben Format. Interne Pfade, Klassennamen oder Stacktraces erreichen nie den Client.
- **Escapte Sucheingaben.** Suchbegriffe werden escaped, bevor sie die Abfrageschicht erreichen. Ein präparierter Begriff wird so nie zu einem eingeschleusten oder teuren regulären Ausdruck.

## Datei-Uploads und Objektspeicher

- **Content-Type und Größe werden beim Upload geprüft**, damit niemand unerlaubte oder zu große Dateien einschleust (Limits per ENV).
- **Zufällige S3-Objektschlüssel.** Gespeicherte Objekte lassen sich über den Namen weder erraten noch auflisten.
- **Presignte Downloads.** Anhänge kommen über kurzlebige presignte URLs statt aus einem öffentlichen Bucket. Der Zugriff ist so eingegrenzt und zeitlich begrenzt.

## Verschlüsselung im Ruhezustand für Integrations-Secrets

Git-Access-Tokens und andere Secrets von Integrationen werden vor dem Speichern **mit AES-GCM verschlüsselt**, mit dem Schlüssel aus **`HINATA_GIT_TOKEN_SECRET`**. In der Admin-API sind Secrets **nur schreibbar** und werden nie zurückgegeben. Ändere den Standardschlüssel in der Produktion. Beim Rotieren werden gespeicherte Tokens neu verschlüsselt.

## OWASP-Top-10-Mapping

| OWASP Top 10 (2021) | Wie Hinata darauf eingeht |
| --- | --- |
| A01 Broken Access Control | Adminrouten nur mit `ADMIN`, feste Liste öffentlicher Endpunkte, Sichtbarkeit über Team und Projekt, Tokens pro Sitzung widerrufbar |
| A02 Cryptographic Failures | JWT HS512, Passwörter mit BCrypt 12, Integrations-Secrets mit AES-GCM verschlüsselt, TLS überall (Betreiber) |
| A03 Injection | Escapte Suche, parametrisierter Zugriff auf MongoDB, Uploads mit Prüfung von Content-Type und Größe |
| A04 Insecure Design | Refresh-Tokens für die API abgelehnt, nur schreibbare Secrets, Auth-Callbacks per Deep Link, Authorization-State in MongoDB |
| A05 Security Misconfiguration | Gehärtete Header (HSTS/CSP/no-referrer), Oberfläche der API-Docs in Prod standardmäßig aus, Liste vertrauenswürdiger Proxys, stabile Fehler ohne Stacktraces |
| A06 Vulnerable Components | Aktiv gepflegte Basis aus Spring Boot 4 / Java 21. Images aktuell halten (Betreiber) |
| A07 Identification & Auth Failures | Mindestlänge für Passwörter, Login-Sperre in der Datenbank, strenges Rate Limiting auf `/auth/**`, 2FA per TOTP, widerrufbare Sitzungen |
| A08 Software & Data Integrity | Git-Webhooks mit geprüfter Signatur, Commit-Ledger, das jeden Commit nur einmal anwendet (siehe [Git-Integration](/de/git-integration.html)) |
| A09 Logging & Monitoring | `/actuator/health` für Probes. Fehler werden auf dem Server geloggt, ohne Interna an Clients zu geben |
| A10 SSRF | Integrationen laufen über den Server mit festen Endpunkten der Anbieter statt mit URLs vom Client |

## Härtungscheckliste für Betreiber

!!! danger "Erledige das, bevor du live gehst"

    - **Ändere `HINATA_JWT_SECRET`** in ein neues Secret mit 64 Zeichen (`openssl rand -base64 64`).
    - **Ändere jedes Standardpasswort:** `MONGO_ROOT_PASSWORD`, `MINIO_ROOT_PASSWORD` und die Passwörter für TLS-Keystore und Truststore (`HINATA_MONGO_TLS_*_PASSWORD`, Standard `changeit`).
    - **Ändere `HINATA_GIT_TOKEN_SECRET`**, damit Integrations-Tokens mit deinem eigenen Schlüssel verschlüsselt werden.

!!! tip "Dann ziehe den Perimeter fester"

    - **TLS überall:** HTTPS am Reverse Proxy terminieren und TLS zwischen den Diensten nutzen. MongoDB in der Produktion mit X.509 betreiben (siehe [MongoDB & X.509](/de/database.html)).
    - **Setze `HINATA_TRUSTED_PROXIES`** auf die CIDR deines Proxys, damit Rate Limiting und Login-Sperre die echte Client-IP sehen.
    - **Deaktiviere die Docs-UI in Prod:** Lass `HINATA_DOCS_ENABLED=false`, damit die Scalar-Oberfläche der API-Docs nicht erreichbar ist.
    - **Grenze CORS ein:** Setze `HINATA_CORS_ALLOWED_ORIGINS` genau auf die Origin(s) deiner Web-App, nicht mehr.
    - **Halte Images aktuell:** Ziehe regelmäßig neue Images von `ghcr.io/hinata-platform` für Sicherheitsfixes. Siehe [Backups & Upgrades](/de/backups.html).
    - **Halte die Serveruhr synchron** (NTP). Das braucht der Tokenablauf und SAML-SSO.

## Wie geht es weiter

- **[Authentifizierung](/de/authentication.html):** Zugangsdaten, 2FA und Widerruf von Sitzungen.
- **[Single Sign-on](/de/sso.html):** Anmeldung an deinen IdP abgeben.
- **[Konfigurationsreferenz](/de/configuration.html):** jede Umgebungsvariable an einem Ort.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html):** vertrauenswürdige Proxys und TLS-Terminierung.
