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
- **Keine Hintertür für Admins.** Die Rolle `ADMIN` öffnet nur den Adminbereich. Projekte, Teams, Vorgänge, Boards, Seiten der Wissensdatenbank, Suchtreffer und Zeiteinträge sieht ein Admin nur über seine eigene Mitgliedschaft, wie alle anderen.
- **Organisationsaufgaben mit eigener Rolle.** Die Einstellungen für Zeiterfassung, Freigaben, Abwesenheiten, Feiertage und Abrechnung verlangen die Rolle `ORG_ADMIN`. Andere erhalten dort 403, auch Admins. Siehe [Organisation](/de/organization.html).
- **Rollen, die sich nicht selbst vergeben.** Ein Admin kann sich nicht selbst zum Organisationsadmin machen, das muss ein anderer Admin tun. Das ist eine Maßnahme für Nachvollziehbarkeit und keine harte Sperre, denn mit einem zweiten Adminkonto ginge es trotzdem. Deshalb wird jede Vergabe aufgezeichnet, ohne dass sich das abschalten lässt. Der letzte Organisationsadmin lässt sich nicht entfernen, deaktivieren oder löschen. Wer die Rolle bekommt oder abgibt, wird allen Organisationsadmins gemeldet. Für die Rolle Moderation (`MODERATOR`) gilt dasselbe. Ob jemand moderiert, prüft der Server am gespeicherten Konto, nicht am Token: Eine entzogene Rolle wirkt sofort.
- **Schutz vor Kontoübernahme durch Admins.** Ändert ein Admin die Anmeldeadresse einer Person, bekommt sie eine Nachricht an ihre alte Adresse. Einen Tag lang geht danach kein Zurücksetzen des Passworts an sie, weder aus dem Adminbereich noch über die öffentliche Seite „Passwort vergessen“, die in dieser Zeit stillschweigend nichts verschickt.
- **Getrenntes Audit-Protokoll.** Unter **Adminbereich → Audit** stehen nur Einträge der Plattform: Anmeldungen, Konten, Konfiguration und Integrationen. Einträge zu Arbeitszeit, Stundenzetteln und Abwesenheiten stehen im Protokoll der Seite Organisation. Einträge zu Abwesenheiten sieht dort nur, wer die Abwesenheiten führt. Welche dieser Ereignisse aufgezeichnet werden, entscheiden die Organisationsadmins. Admins können das nicht ändern, und der Hauptschalter der Plattform schaltet sie nicht ab. Einträge zu Vorgängen und Seiten erscheinen für Admins ohne Details, also ohne Vorgangsschlüssel und Seiten-IDs. Änderungen an den Rollen Admin und Organisationsadmin und jede Änderung einer Anmeldeadresse durch einen Admin werden immer aufgezeichnet und lassen sich nicht abschalten.
- **Wissensdatenbank über Rollen geschützt.** Eine Seite liest, wer ihr Projekt sieht, wer Team-Admin ihres Teams ist oder wem das Team sie geöffnet hat. Seiten ohne Projekt und Team liest nur ihr Autor. Die Suche liefert nur, was der Aufrufer erreichen darf. Eine Seite an einen anderen Ort verschieben darf nur, wer über ihren jetzigen Ort bestimmt, und privat machen kann sie nur ihr Autor.
- **Öffentliche Endpunkte sind festgelegt.** Was ohne Token erreichbar ist, steht vollständig unter [Was ohne Anmeldung erreichbar ist](#was-ohne-anmeldung-erreichbar-ist). Alles andere verlangt ein Bearer-Token.

## Was ohne Anmeldung erreichbar ist

Inhalte einer Instanz erreichen nur ihre Mitglieder. Davon hängt auch ab, dass eine Instanz rechtlich ein Hostingdienst bleibt und keine Online-Plattform wird, siehe [Moderation für Betreiber](/de/moderation-operators.html). Ohne Token antwortet der Server deshalb nur auf diese Wege:

| Wofür | Wege |
| --- | --- |
| Anmelden, beitreten, Zugang zurückholen | `POST /api/v1/auth/login`, `/2fa`, `/refresh`, `/register`, `/verify-email`, `/resend-verification`, `/reset/request`, `/reset/accept`, `/invite/accept`, `/sso/exchange`; `GET /api/v1/auth/invite/info`, `/sso/providers`, `/sso/start/{id}` |
| Links aus Mails und Kalender-Abos, jeder mit eigenem Geheimnis | `GET /api/v1/me/email-change/confirm`, `GET` und `POST /api/v1/me/password-reset/confirm`, `GET /api/v1/me/export.pdf`, `GET /api/v1/shifts/feed/{token}.ics` |
| Was die App vor dem Anmelden über den Server erfährt: Name, Logo, Kontakt für Meldungen | `GET /api/v1/meta`, `GET /api/v1/meta/logo` |
| Die Hausregeln und das Formular für Meldungen ohne Konto (DSA Art. 14 und 16) | `GET /api/v1/public/rules`, `GET` und `POST /api/v1/public/report` |
| Profilbilder für Mails und Pushes | `GET /api/v1/users/{id}/avatar` |
| Erster Start eines neuen Servers, danach abgelehnt | `GET /api/v1/setup/status`, `POST /api/v1/setup` |
| Git-Anbieter; ein Webhook zählt nur mit der Signatur eines verbundenen Repositorys | `GET /api/v1/git/oauth/callback`, `POST /api/v1/git/webhooks/github`, `/gitlab`, `/bitbucket` |
| OAuth für KI-Clients an `/mcp` | `GET /.well-known/oauth-authorization-server`, `GET /.well-known/oauth-protected-resource` und `…/mcp`, `POST /oauth/register`, `GET /oauth/authorize`, `POST /oauth/token` |
| Hinata Connect prüft, dass der Server seine Domain kontrolliert | `GET /.well-known/hinata-connect-challenge` |
| Zustand für die Container-Laufzeit, nur der Status | `GET /actuator/health` und darunter |
| Beschreibung der API, abschaltbar mit `HINATA_DOCS_ENABLED=false` | `GET /v3/api-docs`, `/docs`, `/docs/scalar.js`, `/webjars/**` |
| Fehlerantworten | `/error` |
| Weiterleitungen zu und von einem Identity Provider | `/oauth2/authorization/{id}`, `/login/oauth2/code/{id}`, `/saml2/authenticate/{id}`, `/login/saml2/sso/{id}`, `/logout` (nur eine Weiterleitung, ein Token ist keine Sitzung) |

Ein Test im Server (`UnauthenticatedSurfaceTest`) liest das bei jedem Build aus dem laufenden Server: jede Route jedes Handler-Mappings, die Filter jeder Security-Kette, jedes Servlet und jeden Servlet-Filter. Kommt ein Weg ohne Anmeldung dazu, auf welche Art auch immer, schlägt der Test fehl, bis jemand ihn geprüft und hier eingetragen hat. Eingaben dieser Wege sind begrenzt, zum Beispiel der Name eines dynamisch registrierten OAuth-Clients auf 100 Zeichen und höchstens zehn Weiterleitungsadressen.

### Meldungen ohne Konto

Das Meldeformular unter `/api/v1/public/report` ist eine Seite des Servers ohne JavaScript. Damit es weder zum Spam-Versand noch zum Lahmlegen taugt:

- Jedes Formular trägt ein Einmal-Token, an den Hash der IP-Adresse gebunden. Es gilt frühestens nach 3 Sekunden und höchstens 2 Stunden und ist nach dem Senden verbraucht. Ein verstecktes Feld fängt Bots.
- Gesendet wird nur von derselben Herkunft (`Sec-Fetch-Site` beziehungsweise `Origin`), sonst 403.
- Die Grenzen liegen in der Datenbank: 10 Meldungen je Stunde und Adresse, 3 am Tag je E-Mail-Adresse, 100 je Stunde insgesamt. Ist eine Grenze erreicht, zeigt die Seite den Kontakt der Instanz statt eines Fehlers.
- Der Server ruft die angegebene Adresse nie ab. Zeigt sie auf einen Inhalt dieser Instanz, hängt die Meldung genau dort, und die Moderation sieht den Inhalt erst, wenn eine zweite Person ihn freigibt. Die Seite sagt nie, ob es den Inhalt gibt.
- Die Eingangsbestätigung wiederholt nichts von dem, was eingegeben wurde, und nennt keine internen Kennungen.

Die Grenzen je Adresse brauchen hinter einem Reverse Proxy `HINATA_TRUSTED_PROXIES`, siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

## Gehärtete HTTP-Antworten

- **Security-Header** auf jeder Antwort, unter anderem **HSTS** (erzwingt HTTPS), eine strenge **Content-Security-Policy** und **`Referrer-Policy: no-referrer`**.
- **Stabile, lokalisierte JSON-Fehler ohne Stacktraces.** Der Server holt Fehlertexte passend zum `Accept-Language` des Clients aus Message-Bundles und liefert sie immer im selben Format. Interne Pfade, Klassennamen oder Stacktraces erreichen nie den Client.
- **Escapte Sucheingaben.** Suchbegriffe werden escaped, bevor sie die Abfrageschicht erreichen. Ein präparierter Begriff wird so nie zu einem eingeschleusten oder teuren regulären Ausdruck.

## Texte und Links

- **Links führen nur ins Web, zur Mail oder in die App.** Beim Speichern behält ein Link in einem Text nur Ziele mit `http`, `https` oder `mailto` und Pfade der App, die mit genau einem `/` beginnen. Alles andere, etwa `javascript:`, `data:` oder `//fremder.host`, verliert den Link und behält seine Wörter. Das gilt für jeden Weg in einen Text, auch für Markdown aus MCP und aus Mails. Eine einmalige Migration hat es für alle vorher gespeicherten Texte nachgeholt.
- **Außerhalb des Browsers folgen die Apps nur Adressen mit Schema.** Ein relativer Pfad bedeutet dort nichts, und Windows öffnete ihn als Pfad auf der Festplatte, `//host` als Netzwerkfreigabe.
- **Die automatische Textprüfung** lehnt eindeutige Verstöße beim Speichern ab, auf jedem Weg. Sie läuft im Server, ohne fremden Dienst. Siehe [Adminbereich](/de/admin-area.html).

## Datei-Uploads und Objektspeicher

- **Content-Type und Größe werden beim Upload geprüft**, damit niemand unerlaubte oder zu große Dateien einschleust (Limits per ENV).
- **Zufällige S3-Objektschlüssel.** Gespeicherte Objekte lassen sich über den Namen weder erraten noch auflisten.
- **Presignte Downloads.** Anhänge kommen über kurzlebige presignte URLs statt aus einem öffentlichen Bucket. Der Zugriff ist so eingegrenzt und zeitlich begrenzt.

## Verschlüsselung im Ruhezustand für Integrations-Secrets

Git-Access-Tokens und andere Secrets von Integrationen werden vor dem Speichern **mit AES-GCM verschlüsselt**, mit dem Schlüssel aus **`HINATA_GIT_TOKEN_SECRET`**. In der Admin-API sind Secrets **nur schreibbar** und werden nie zurückgegeben. Ändere den Standardschlüssel in der Produktion. Beim Rotieren werden gespeicherte Tokens neu verschlüsselt.

## OWASP-Top-10-Mapping

| OWASP Top 10 (2021) | Wie Hinata darauf eingeht |
| --- | --- |
| A01 Broken Access Control | Adminrouten nur mit `ADMIN`, Organisationsrouten nur mit `ORG_ADMIN`, keine Inhaltsrechte aus Plattformrollen, feste Liste öffentlicher Endpunkte, Sichtbarkeit über Team und Projekt, Tokens pro Sitzung widerrufbar |
| A02 Cryptographic Failures | JWT HS512, Passwörter mit BCrypt 12, Integrations-Secrets mit AES-GCM verschlüsselt, TLS überall (Betreiber) |
| A03 Injection | Escapte Suche, parametrisierter Zugriff auf MongoDB, Uploads mit Prüfung von Content-Type und Größe |
| A04 Insecure Design | Refresh-Tokens für die API abgelehnt, nur schreibbare Secrets, Auth-Callbacks per Deep Link, Authorization-State in MongoDB |
| A05 Security Misconfiguration | Gehärtete Header (HSTS/CSP/no-referrer), Oberfläche der API-Docs in Prod standardmäßig aus, Liste vertrauenswürdiger Proxys, stabile Fehler ohne Stacktraces |
| A06 Vulnerable Components | Aktiv gepflegte Basis aus Spring Boot 4 / Java 21. Images aktuell halten (Betreiber) |
| A07 Identification & Auth Failures | Mindestlänge für Passwörter, Login-Sperre in der Datenbank, strenges Rate Limiting auf `/auth/**`, 2FA per TOTP, widerrufbare Sitzungen |
| A08 Software & Data Integrity | Git-Webhooks mit geprüfter Signatur, Commit-Ledger, das jeden Commit nur einmal anwendet (siehe [Git-Integration](/de/git-integration.html)) |
| A09 Logging & Monitoring | `/actuator/health` für Probes. Fehler werden auf dem Server geloggt, ohne Interna an Clients zu geben |
| A10 SSRF | Integrationen laufen über den Server mit festen Endpunkten der Anbieter statt mit URLs vom Client, ein per URL eingetragenes Logo lädt der Server nur von öffentlichen Adressen auf Port 80 oder 443 und prüft jede Weiterleitung neu |

## Härtungscheckliste für Betreiber

!!! danger "Erledige das, bevor du live gehst"

    - **Ändere `HINATA_JWT_SECRET`** in ein neues Secret mit 64 Zeichen (`openssl rand -base64 64`).
    - **Ändere jedes Standardpasswort:** `MONGO_ROOT_PASSWORD`, `HINATA_S3_SECRET_KEY`, die Geheimnisse `SEAWEEDFS_*` und die Passwörter für TLS-Keystore und Truststore (`HINATA_MONGO_TLS_*_PASSWORD`, Standard `changeit`).
    - **Ändere `HINATA_GIT_TOKEN_SECRET`**, damit Integrations-Tokens mit deinem eigenen Schlüssel verschlüsselt werden.

!!! tip "Dann ziehe den Perimeter fester"

    - **TLS überall:** HTTPS am Reverse Proxy terminieren und TLS zwischen den Diensten nutzen. MongoDB in der Produktion mit X.509 betreiben (siehe [MongoDB & X.509](/de/database.html)).
    - **Setze `HINATA_TRUSTED_PROXIES`** auf die CIDR deines Proxys, damit Rate Limiting und Login-Sperre die echte Client-IP sehen.
    - **Deaktiviere die Docs-UI in Prod:** Lass `HINATA_DOCS_ENABLED=false`, damit die Scalar-Oberfläche der API-Docs nicht erreichbar ist.
    - **Grenze CORS ein:** Setze `HINATA_CORS_ALLOWED_ORIGINS` genau auf die Origin(s) deiner Web-App, nicht mehr.
    - **Vertraue keiner Anfrage nur wegen ihrer Herkunft:** Ein Logo, das per URL eingetragen ist, lädt der Server selbst herunter. Adressen auf dem eigenen Rechner und in privaten Netzen lehnt er ab, jede öffentliche Adresse auf Port 80 oder 443 erreicht er aber. Dazu gehören dein eigener Reverse Proxy und interne Dienste mit öffentlicher IPv4- oder IPv6-Adresse. Schütze deshalb jeden Dienst mit einer Anmeldung, der Anfragen nur nach ihrer Herkunft zulässt, etwa von der IP deines Servers oder aus deinem internen Netz.
    - **Halte Images aktuell:** Ziehe regelmäßig neue Images von `ghcr.io/hinata-platform` für Sicherheitsfixes. Siehe [Backups & Upgrades](/de/backups.html).
    - **Halte die Serveruhr synchron** (NTP). Das braucht der Tokenablauf und SAML-SSO.

## Wie geht es weiter

- **[Authentifizierung](/de/authentication.html):** Zugangsdaten, 2FA und Widerruf von Sitzungen.
- **[Single Sign-on](/de/sso.html):** Anmeldung an deinen IdP abgeben.
- **[Konfigurationsreferenz](/de/configuration.html):** jede Umgebungsvariable an einem Ort.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html):** vertrauenswürdige Proxys und TLS-Terminierung.
