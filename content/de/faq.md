---
title: FAQ & Fehlerbehebung
description: Antworten auf häufige Fragen zu Hinata — Kosten, Firebase, Branding, Datenbanken, SSO — plus eine Fehlerbehebungstabelle mit konkreten Lösungen für die üblichen Probleme.
---

# FAQ & Fehlerbehebung

Die Fragen, die Self-Hoster am häufigsten stellen, und eine Fehlerbehebungstabelle für
die Probleme, die in der Praxis wirklich auftreten — jeweils mit der konkreten
Einstellung oder dem Befehl, der sie behebt. Falls dein Problem hier nicht auftaucht,
gehen die überall verlinkten Seiten pro Teilsystem tiefer ins Detail.

## Häufig gestellte Fragen

### Ist Hinata wirklich kostenlos, ohne Limits?

Ja. Hinata ist **Open Source unter der GPL-3.0-Lizenz**, und es gibt **keine Nutzer-,
Team- oder Board-Limits — niemals**. Du betreibst es auf deiner eigenen Infrastruktur
und fügst so viele Personen, Projekte, Teams und Boards hinzu, wie du möchtest. Es gibt
keine kostenpflichtige Stufe, keine Sitzplatzabrechnung und keine Feature-Schranke; die
gesamte Plattform ist der Code in den beiden Repositories.

### Brauche ich Firebase für Push-Benachrichtigungen?

**Nein.** Mobile Push-Benachrichtigungen und Universal- (Deep-) Links werden über das
zentrale [Hinata Connect Gateway](/de/connect-gateway.html) weitergeleitet, einen
gehosteten Dienst. Die Push-Zugangsdaten der veröffentlichten App liegen im Gateway —
nicht in deinem Deployment — sodass Self-Hoster für Push **nichts** konfigurieren.
(Firebase betrifft dich nur, wenn du deinen **eigenen** Client mit eigener
Store-Präsenz baust und ausrollst und dein eigenes Gateway betreibst.)

### Kann ich meine eigene Domain und mein eigenes Branding verwenden?

**Ja.** Du lieferst ohnehin bereits alles unter deiner eigenen Domain aus
(`track.example.com` für die Web-App, `api.track.example.com` für die API), und
die App übernimmt Name und Logo deiner Organisation zur Laufzeit von deinem
Server. Darüber hinaus kannst du deinen eigenen gebrandeten Client bauen: eigene
Package-ID, App-Name, Icons und Splash, Akzentfarbe, ausgerichtet auf das
Gateway. Siehe [Branding & eigene Clients](/de/self-hosted-app.html). Native Apps backen
niemals eine Server-URL fest ein — Nutzer speichern Server und wechseln zwischen ihnen —
sodass eine gebrandete App viele Instanzen bedienen kann.

### Welche Datenbanken und welchen Speicher verwendet Hinata?

- **MongoDB** ist das führende System. Die Produktion läuft als **Replica Set** (2
  Datenknoten + 1 Arbiter) mit TLS und X.509-Client-Authentifizierung — siehe
  [MongoDB & X.509](/de/database.html).
- **S3-kompatibler Objektspeicher** hält Anhänge und Avatare, mit randomisierten
  Objektschlüsseln und vorsignierten Downloads. Der Stack liefert **MinIO** mit, aber
  jeder S3-kompatible Speicher funktioniert — siehe [Objektspeicher](/de/storage.html).

Es gibt keine separate SQL-Datenbank und keinen Message-Broker; Live-Updates nutzen SSE.

### Funktioniert SSO mit meinem Identity Provider?

Sehr wahrscheinlich. Hinata unterstützt **OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP**,
zur Laufzeit im Adminbereich konfiguriert (in MongoDB gespeichert, kein Neustart). Das
deckt die gängigen Anbieter ab — Keycloak, Authentik, Azure AD, Google, Synology SSO und
alles, was diese Protokolle spricht. Siehe [Single Sign-on (SSO)](/de/sso.html).

### Erfordern Konfigurationsänderungen einen Neustart?

Die meisten nicht. Laufzeiteinstellungen (SSO, E-Mail-Eingang, Push, Git-OAuth-Apps,
App-Einstellungen) werden **in MongoDB gespeichert und im Adminbereich verwaltet**, und
**die Datenbank überschreibt die Umgebung**. Änderungen greifen bei der nächsten Anfrage.
Nur die Bootstrap-Umgebungsvariablen (wie `HINATA_JWT_SECRET`) erfordern ein
Redeploy. Siehe [Architektur → Laufzeiteinstellungen](/de/architecture.html).

## Fehlerbehebung

Jede Zeile nennt das Symptom, die übliche Ursache und die konkrete Lösung.

| Symptom | Wahrscheinliche Ursache | Lösung |
| --- | --- | --- |
| **App verbindet sich nicht mit dem Server** | Falsche Basis-URL, blockiertes CORS oder ein TLS-Problem | Stelle sicher, dass `HINATA_BASE_URL` die öffentliche API-URL ist und über HTTPS erreichbar; füge den Origin der Web-App zu `HINATA_CORS_ALLOWED_ORIGINS` hinzu; prüfe, dass das Zertifikat gültig ist. |
| **App hängt in einer erzwungenen Update-Schleife** | `HINATA_APP_MIN_VERSION` ist höher als die Version des Clients | Senke `HINATA_APP_MIN_VERSION` auf eine Version, die deine installierten Clients erreichen oder darunter liegt (oder aktualisiere die Clients). Auch unter Admin → App editierbar, was die Umgebung überschreibt. |
| **E-Mails kommen nie an** | Kein echtes SMTP-Relay, falsche Absenderidentität oder fehlende Web-Basis-URL | Setze ein echtes `HINATA_SMTP_*`-Relay (Mailpit ist nur für die Entwicklung); setze `HINATA_MAIL_FROM` auf eine Adresse, für die dein Relay senden darf; setze `HINATA_WEB_BASE_URL`, damit Deep Links in E-Mails auf den richtigen Host zeigen. |
| **SSE / Live-Updates funktionieren nicht** | Der Reverse Proxy puffert den Stream | Deaktiviere das Response-Buffering für den Stream-Pfad (z. B. `proxy_buffering off;` bei nginx), damit Events beim Auftreten geflusht werden. |
| **Zu aggressives Rate-Limiting / falsche Client-IP** | Jede Anfrage sieht aus, als käme sie vom Proxy | Setze `HINATA_TRUSTED_PROXIES` auf das CIDR des Proxys, damit der Server die echte Client-IP aus `X-Forwarded-For` liest und pro Nutzer statt pro Proxy limitiert. |
| **MongoDB startet nicht** | Replica Set nicht initialisiert, Keyfile/PKI falsch | Stelle sicher, dass das Replica Set initialisiert ist und das Mongo-**Keyfile** existiert (`./deploy/generate-secrets.sh`); für die Produktion die X.509-PKI generieren und den Client-Nutzer registrieren. |
| **Alle nach einem Redeploy abgemeldet** | `HINATA_JWT_SECRET` hat sich geändert | Halte `HINATA_JWT_SECRET` über Deployments hinweg **stabil** — eine Änderung macht jeden ausgestellten Token ungültig. Generiere es einmal und bewahre es sicher auf. |
| **Git-Webhooks kommen nie an** | Webhook-Basis-URL nicht öffentlich, Callback nicht registriert | Setze `HINATA_GIT_WEBHOOK_BASE_URL` auf eine **öffentliche** API-Basis und registriere `<public-api-base>/git/oauth/callback` beim Anbieter; der Webhook wird beim Verbinden automatisch registriert. |

### App verbindet sich nicht mit dem Server

Die App spricht mit der API unter `HINATA_BASE_URL`, und Browser- (Web-) Builds
unterliegen CORS. Drei Dinge sind der Reihe nach zu prüfen:

1. **`HINATA_BASE_URL`** ist die öffentliche API-URL (z. B. `https://api.track.example.com`)
   und tatsächlich vom Gerät aus erreichbar.
2. **CORS** — für den Web-Client muss der Browser-Origin (z. B.
   `https://track.example.com`) in `HINATA_CORS_ALLOWED_ORIGINS` gelistet sein, den die
   gehostete Web-App per Cross-Origin aufruft.
3. **TLS** — das Zertifikat muss für den API-Host gültig sein; ein selbstsigniertes oder
   nicht passendes Zertifikat schlägt in manchen Clients stillschweigend fehl.

Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html) und
[Konfigurationsreferenz](/de/configuration.html).

### Erzwungene Update-Schleife

Bei jedem Start vergleicht die App ihre Version mit dem Minimum des Servers und erzwingt
ein Update, wenn sie niedriger ist. Wenn du `HINATA_APP_MIN_VERSION` höher setzt, als
deine Nutzer tatsächlich installiert haben, bleiben sie hängen. Senke es auf eine
Version, die deine Flotte erreicht oder darunter liegt — oder editiere es unter
**Admin → App**, dessen Wert die Umgebung überschreibt.

### E-Mails werden nicht zugestellt

Verifizierungs-, Passwort-Reset- und Benachrichtigungs-E-Mails verlassen den Server nur
über ein **echtes SMTP-Relay** — Mailpit ist nur ein Abfänger für die Entwicklung.
Konfiguriere `HINATA_SMTP_HOST`, `_PORT`, `_USERNAME`, `_PASSWORD`, `_AUTH` und
`_STARTTLS`, und setze `HINATA_MAIL_FROM` auf eine Adresse, für die dein Relay senden
darf (eine nicht passende `From`-Identität ist eine häufige Ursache für stille
Ablehnungen). Setze `HINATA_WEB_BASE_URL`, damit die Deep Links in diesen E-Mails auf
deine Web-App zeigen. Siehe [E-Mail & SMTP](/de/email.html).

### Live-Updates / SSE funktionieren nicht

[Anhänge und andere Live-Funktionen](/de/api.html#live-updates-with-server-sent-events)
werden über Server-Sent Events gestreamt. Ein Reverse Proxy, der Responses puffert, hält
die Events zurück, bis die Verbindung schließt, was genau wie „Live-Sync ist kaputt“
aussieht. Schalte das Buffering für den Stream-Pfad aus — bei nginx
`proxy_buffering off;`. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html).

### Rate-Limiting oder falsche Client-IP protokolliert

Rate-Limiting schlüsselt nach der Client-IP. Hinter einem Proxy scheint jede Anfrage von
der Adresse des Proxys zu kommen, es sei denn, du sagst dem Server, welchen Proxys er
vertrauen soll. Setze `HINATA_TRUSTED_PROXIES` auf das CIDR des Proxys, damit der Server
die echte Client-IP aus `X-Forwarded-For` liest. Leer bedeutet, keinem zu vertrauen —
richtig, wenn es keinen Proxy gibt, falsch, wenn es einen gibt.

### MongoDB startet nicht

MongoDB läuft als Replica Set, das ein gemeinsames **Keyfile** für die interne
Authentifizierung braucht, und in der Produktion **X.509** für die App-Verbindung. Wenn
es nicht hochkommt, bestätige, dass das Keyfile generiert wurde
(`./deploy/generate-secrets.sh`), das Replica Set initialisiert ist und — für die
Produktion — die PKI generiert wurde (`./deploy/x509/generate-certs.sh prod`) und der
Client-Nutzer registriert ist (`./deploy/x509/init-prod-user.sh`). Siehe
[MongoDB & X.509](/de/database.html).

### Login-Schleifen nach einem Redeploy

JWTs werden mit `HINATA_JWT_SECRET` signiert. Ändert sich dieser Wert zwischen Deployments,
wird jeder zuvor ausgestellte Token ungültig und Clients werden zum Login zurückgeworfen.
Generiere das Secret **einmal** (`openssl rand -base64 64 | tr -d '\n'`) und halte es in
deinem `.env` / Secret-Store über jedes Redeploy hinweg stabil.

### Git-Webhooks kommen nicht an

Damit Push-/PR-/CI-Events deinen Server erreichen, muss der Webhook-Empfänger öffentlich
erreichbar und der OAuth-Callback beim Anbieter registriert sein. Setze
`HINATA_GIT_WEBHOOK_BASE_URL` auf eine **öffentliche** API-Basis (fällt zurück auf
`HINATA_BASE_URL` + `/api/v1`) und registriere `<public-api-base>/git/oauth/callback` bei
jedem Anbieter. Der projektbezogene Webhook wird automatisch registriert, wenn du ein
Repository verbindest. Siehe [Git-Integration](/de/git-integration.html).

## Wie es weitergeht

- [Konfigurationsreferenz](/de/configuration.html) — jede Umgebungsvariable an einem Ort.
- [Reverse Proxy & TLS](/de/reverse-proxy.html) — CORS, SSE-Buffering und Trusted Proxies.
- [E-Mail & SMTP](/de/email.html) — Zustellung von Verifizierungs- und Benachrichtigungs-E-Mails.
- [Self-Hosting-Überblick](/de/self-hosting.html) — das große Ganze und eine Konfigurations-Checkliste.
