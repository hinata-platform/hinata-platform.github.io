---
title: FAQ & Fehlerbehebung
description: Antworten auf häufige Fragen zu Hinata und konkrete Lösungen für typische Probleme.
---

# FAQ & Fehlerbehebung

Häufige Fragen von Self-Hostern und Lösungen für die Probleme, die in der Praxis
auftreten. Die verlinkten Seiten gehen tiefer ins Detail.

## Häufig gestellte Fragen

### Ist Hinata wirklich kostenlos, ohne Limits?

Ja. Hinata ist **Open Source unter der GPL-3.0-Lizenz**. Es gibt **keine Limits für
Nutzer, Teams oder Boards**, auch künftig nicht. Eine kostenpflichtige Version,
Abrechnung pro Nutzer oder gesperrte Funktionen gibt es nicht. Die ganze Plattform
ist der Code in den beiden Repositories.

### Brauche ich Firebase für Push-Benachrichtigungen?

**Nein.** Push und Universal Links (Deep Links) laufen über das zentrale
[Hinata Connect Gateway](/de/connect-gateway.html), einen gehosteten Dienst. Die
Push-Zugangsdaten der App liegen dort, du konfigurierst für Push **nichts**.
Firebase brauchst du nur, wenn du einen **eigenen** Client mit eigenem Store-Eintrag
und eigenem Gateway betreibst.

### Kann ich meine eigene Domain und mein eigenes Branding verwenden?

**Ja.** Alles läuft ohnehin unter deiner Domain (`track.example.com` für die
Web-App, `api.track.example.com` für die API). Name und Logo deiner Organisation
holt die App zur Laufzeit von deinem Server.

Du kannst auch einen eigenen Client bauen: eigene Package-ID, eigener App-Name,
Icons, Splash und Akzentfarbe, verbunden mit dem Gateway. Siehe
[Branding & eigene Clients](/de/self-hosted-app.html). Native Apps haben keine fest
eingebaute Server-URL. Nutzer speichern Server und wechseln zwischen ihnen, deshalb
bedient eine App viele Instanzen.

### Welche Datenbanken und welchen Speicher verwendet Hinata?

- **MongoDB** hält alle Daten. In Produktion läuft ein **Replica Set** (2
  Datenknoten + 1 Arbiter) mit TLS und X.509-Client-Authentifizierung. Siehe
  [MongoDB & X.509](/de/database.html).
- **S3-kompatibler Objektspeicher** hält Anhänge und Avatare, mit zufälligen
  Objektschlüsseln und vorsignierten Downloads. Mitgeliefert ist **MinIO**, jeder
  S3-kompatible Speicher funktioniert. Siehe [Objektspeicher](/de/storage.html).

Es gibt keine separate SQL-Datenbank und keinen Message-Broker. Live-Updates laufen
über SSE.

### Funktioniert SSO mit meinem Identity Provider?

Sehr wahrscheinlich. Hinata unterstützt **OpenID Connect, OAuth 2.0, SAML 2.0 und
LDAP**. Du richtest das zur Laufzeit im Adminbereich ein (gespeichert in MongoDB,
ohne Neustart). Damit gehen Keycloak, Authentik, Azure AD, Google, Synology SSO und
alles, was diese Protokolle spricht. Siehe [Single Sign-on (SSO)](/de/sso.html).

### Erfordern Konfigurationsänderungen einen Neustart?

Meistens nicht. Laufzeiteinstellungen (SSO, E-Mail-Eingang, Push, Git-OAuth-Apps,
App-Einstellungen) liegen **in MongoDB und werden im Adminbereich verwaltet**.
**Die Datenbank überschreibt die Umgebung.** Änderungen greifen bei der nächsten
Anfrage. Nur Bootstrap-Variablen wie `HINATA_JWT_SECRET` brauchen ein Redeploy.
Siehe [Architektur → Laufzeiteinstellungen](/de/architecture.html).

## Fehlerbehebung

Symptom, übliche Ursache und Lösung auf einen Blick. Darunter folgen Details.

| Symptom | Wahrscheinliche Ursache | Lösung |
| --- | --- | --- |
| **App verbindet sich nicht mit dem Server** | Falsche Basis-URL, blockiertes CORS oder ein TLS-Problem | `HINATA_BASE_URL` muss die öffentliche API-URL sein und per HTTPS erreichbar. Origin der Web-App in `HINATA_CORS_ALLOWED_ORIGINS` eintragen. Zertifikat prüfen. |
| **App hängt in einer erzwungenen Update-Schleife** | `HINATA_APP_MIN_VERSION` ist höher als die Version des Clients | `HINATA_APP_MIN_VERSION` auf die Version der installierten Clients oder darunter senken (oder Clients aktualisieren). Auch unter Admin → Plattform änderbar, das überschreibt die Umgebung. |
| **E-Mails kommen nie an** | Kein echtes SMTP-Relay, falsche Absenderadresse oder fehlende Web-Basis-URL | Echtes `HINATA_SMTP_*`-Relay setzen (Mailpit nur für die Entwicklung). `HINATA_MAIL_FROM` auf eine Adresse setzen, die dein Relay senden darf. `HINATA_WEB_BASE_URL` setzen, damit Links in E-Mails auf den richtigen Host zeigen. |
| **SSE / Live-Updates funktionieren nicht** | Der Reverse Proxy puffert den Stream | Response-Buffering für den Stream-Pfad abschalten (z. B. `proxy_buffering off;` bei nginx), damit Events sofort ankommen. |
| **Zu strenges Rate-Limiting / falsche Client-IP** | Jede Anfrage scheint vom Proxy zu kommen | `HINATA_TRUSTED_PROXIES` auf das CIDR des Proxys setzen. Dann liest der Server die echte IP aus `X-Forwarded-For` und limitiert pro Nutzer statt pro Proxy. |
| **MongoDB startet nicht** | Replica Set nicht initialisiert, Keyfile oder PKI falsch | Replica Set initialisieren und prüfen, ob das Mongo-**Keyfile** existiert (`./deploy/generate-secrets.sh`). In Produktion die X.509-PKI erzeugen und den Client-Nutzer registrieren. |
| **Alle nach einem Redeploy abgemeldet** | `HINATA_JWT_SECRET` hat sich geändert | `HINATA_JWT_SECRET` über Deployments **stabil** halten. Jede Änderung macht alle ausgestellten Tokens ungültig. Einmal erzeugen und sicher aufbewahren. |
| **Git-Webhooks kommen nie an** | Webhook-Basis-URL nicht öffentlich, Callback nicht registriert | `HINATA_GIT_WEBHOOK_BASE_URL` auf eine **öffentliche** API-Basis setzen und `<public-api-base>/git/oauth/callback` beim Anbieter registrieren. Der Webhook wird beim Verbinden automatisch registriert. |

### App verbindet sich nicht mit dem Server

Prüfe der Reihe nach:

1. **`HINATA_BASE_URL`** ist die öffentliche API-URL (z. B.
   `https://api.track.example.com`) und vom Gerät aus erreichbar.
2. **CORS**: Web-Builds rufen die API cross-origin auf. Ihre Origin (z. B.
   `https://track.example.com`) muss in `HINATA_CORS_ALLOWED_ORIGINS` stehen.
3. **TLS**: Das Zertifikat muss für den API-Host gültig sein. Selbstsignierte oder
   unpassende Zertifikate scheitern in manchen Clients ohne Fehlermeldung.

Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html) und
[Konfigurationsreferenz](/de/configuration.html).

### Erzwungene Update-Schleife

Die App vergleicht beim Start ihre Version mit dem Minimum des Servers und erzwingt
ein Update, wenn sie älter ist. Senke `HINATA_APP_MIN_VERSION` auf die installierte
Version oder darunter. Alternativ änderst du den Wert unter **Admin → Plattform**, der die
Umgebung überschreibt.

### E-Mails werden nicht zugestellt

Verifizierung, Passwort-Reset und Benachrichtigungen brauchen ein **echtes
SMTP-Relay**. Mailpit fängt Mails nur in der Entwicklung ab.

- `HINATA_SMTP_HOST`, `_PORT`, `_USERNAME`, `_PASSWORD`, `_AUTH` und `_STARTTLS`
  setzen.
- `HINATA_MAIL_FROM` auf eine Adresse setzen, die dein Relay senden darf. Ein
  unpassender `From`-Absender führt oft zu Ablehnungen ohne Meldung.
- `HINATA_WEB_BASE_URL` setzen, damit die Links in den E-Mails auf deine Web-App
  zeigen.

Siehe [E-Mail & SMTP](/de/email.html).

### Live-Updates / SSE funktionieren nicht

[Anhänge und andere Live-Funktionen](/de/api.html#live-updates-mit-server-sent-events)
streamen per Server-Sent Events. Ein puffernder Reverse Proxy hält die Events zurück,
bis die Verbindung schließt. Schalte das Buffering für den Stream-Pfad ab, bei nginx
mit `proxy_buffering off;`. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

### Rate-Limiting oder falsche Client-IP protokolliert

Das Rate-Limiting richtet sich nach der Client-IP. Hinter einem Proxy kommt jede
Anfrage scheinbar vom Proxy. Setze `HINATA_TRUSTED_PROXIES` auf das CIDR des Proxys,
dann liest der Server die echte IP aus `X-Forwarded-For`. Leer heißt, keinem Proxy zu
vertrauen. Das passt nur ohne Proxy.

### MongoDB startet nicht

Das Replica Set braucht ein gemeinsames **Keyfile** für die interne
Authentifizierung, in Produktion zusätzlich **X.509** für die App. Prüfe:

- Das Keyfile ist erzeugt (`./deploy/generate-secrets.sh`).
- Das Replica Set ist initialisiert.
- Nur Produktion: Die PKI ist erzeugt (`./deploy/x509/generate-certs.sh prod`) und
  der Client-Nutzer registriert (`./deploy/x509/init-prod-user.sh`).

Siehe [MongoDB & X.509](/de/database.html).

### Login-Schleifen nach einem Redeploy

JWTs werden mit `HINATA_JWT_SECRET` signiert. Ändert sich der Wert, sind alle zuvor
ausgestellten Tokens ungültig und Clients landen wieder beim Login. Erzeuge das
Secret **einmal** (`openssl rand -base64 64 | tr -d '\n'`) und halte es in deiner
`.env` oder im Secret-Store stabil.

### Git-Webhooks kommen nicht an

Push-, PR- und CI-Events brauchen einen öffentlich erreichbaren Webhook-Empfänger und
einen registrierten OAuth-Callback.

- Setze `HINATA_GIT_WEBHOOK_BASE_URL` auf eine **öffentliche** API-Basis (ohne
  Angabe gilt `HINATA_BASE_URL` + `/api/v1`).
- Registriere `<public-api-base>/git/oauth/callback` bei jedem Anbieter.

Den Webhook pro Projekt registriert Hinata automatisch, wenn du ein Repository
verbindest. Siehe [Git-Integration](/de/git-integration.html).

## Wie es weitergeht

- [Konfigurationsreferenz](/de/configuration.html): jede Umgebungsvariable an einem Ort.
- [Reverse Proxy & TLS](/de/reverse-proxy.html): CORS, SSE-Buffering und Trusted Proxies.
- [E-Mail & SMTP](/de/email.html): Zustellung von Verifizierungs- und Benachrichtigungsmails.
- [Self-Hosting-Überblick](/de/self-hosting.html): das große Ganze und eine Checkliste zur Konfiguration.
