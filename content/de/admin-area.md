---
title: Adminbereich
description: Benutzer, Plattform-Einstellungen, SSO, Git und E-Mail zu Vorgang im laufenden Betrieb verwalten.
---

# Adminbereich

Im **Adminbereich** konfigurierst du den größten Teil von Hinata direkt in der
App. Die Einstellungen landen in MongoDB, **überschreiben die Umgebung** und
wirken **ohne Neustart**.

!!! info "Wer Zugriff hat"
    Nur Benutzer mit der Rolle **`ADMIN`**. Jeder Endpunkt unter
    `/api/v1/admin/**` ist auch serverseitig auf Admins beschränkt. Andere
    Benutzer sehen den Bereich nie.

![Hinata-Adminbereich](/assets/img/shot-admin.png)
*Nutzer, Plattform-Einstellungen, SSO, Git und E-Mail zu Vorgang an einem Ort.*

## Wie die Laufzeitkonfiguration funktioniert

Zum Starten braucht der Server nur wenige Umgebungsvariablen: ein JWT-Secret, die
Datenbankverbindung und ein Mail-Relay. SSO-Anbieter, E-Mail-Ingest, OAuth-Apps
für Git und die Plattform-Einstellungen richtest du im Adminbereich ein. Sie liegen in
MongoDB. Dabei gilt:

- **DB überschreibt Env.** Umgebungswerte wie `hinata.app.*` sind nur
  *Standardwerte*. Was du im Adminbereich setzt, gewinnt.
- **Kein Neustart nötig.** Änderungen an Anbietern oder Flags wirken ab der
  nächsten Anfrage, ohne Redeploy oder Neustart des Containers.
- **Secrets sind nur schreibbar.** OAuth-Client-Secrets, Tokens und Passwörter
  kannst du **setzen**, die Admin-API gibt sie aber nie zurück. Gespeicherte
  Git-Tokens sind zusätzlich mit AES-GCM verschlüsselt.

## Die Bereiche

Der Adminbereich hat drei Gruppen:

- **Allgemein**, **Plattform** und **Sicherheit**
- **Authentifizierung**, **E-Mail** und **Git-Integration**
- **Audit-Protokoll** und **Benutzer**

### Benutzer

Hier verwaltest du die Personen auf deiner Instanz:

- ausstehende Registrierungen **genehmigen**
- Konten **aktivieren** oder deaktivieren
- **Rollen** zuweisen, auch `ADMIN`

Ist die Selbstregistrierung mit Admin-Genehmigung aktiv (siehe unten), warten neue
Anmeldungen hier, bis ein Admin sie freigibt.

### Plattform

Drei Karten: welche Clients dein Server annimmt, wie sich Menschen anmelden und
was diese Plattform anbietet.

- **Mindestversion** (`minVersion`): die
  [Versionssperre](/de/clients.html#versionssperre). Ältere Clients müssen
  updaten. Überschreibt `HINATA_APP_MIN_VERSION`.
- **URL der Datenschutzerklärung**: der Link in der App. Pflicht für Releases im
  App Store und bei Google Play sowie für die DSGVO. Überschreibt
  `HINATA_PRIVACY_POLICY_URL`.
- **Anmeldung**: lokale Anmeldung, Selbstregistrierung und Freigabe durch die
  Administration.
- **Plattform-Verhalten**: mehrere Personen an einem Vorgang, Antworten per
  E-Mail und **Projektvorlagen** — Projekte kopieren, das Vorlagen-Kennzeichen
  und Fristen als Versatz zum Termin des Projekts. Aus lassen heißt: Projekte
  verhalten sich genau wie bisher. Dieser Schalter hat drei Stellungen, denn
  leer bedeutet, dass `HINATA_PROJECT_TEMPLATES_ENABLED` entscheidet. Siehe
  [Projektvorlagen](/de/project-templates.html). Die erweiterte Zeiterfassung
  steht hier ebenfalls, eingestellt wird sie aber in ihrem eigenen Bereich.

!!! tip "Gewinnt gegen die Umgebung"
    Alles unter Plattform überschreibt die passende
    `hinata.app.*`-Umgebungsvariable. Umgebungswerte sind nur der Startpunkt
    einer neuen Instanz.

### Authentifizierung & SSO

Hier legst du fest, wie sich Personen anmelden:

- **lokale Authentifizierung**, **Selbstregistrierung** und
  **Admin-Genehmigung** ein- oder ausschalten
- **SSO-Anbieter** registrieren: OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP
  (Synology SSO, Keycloak, Authentik, Azure AD, Google, …)

Anbieter werden in Mongo gespeichert und wirken sofort. Siehe
[Authentifizierung](/de/authentication.html) und [Single Sign-on](/de/sso.html).

### Git-Integration

Registriere **eine OAuth-App pro Anbieter** (GitHub, GitLab, Bitbucket), damit
Projekte ihre Repositories verbinden können. Du trägst ein:

- Client-ID und Secret
- die öffentliche Basis-URL der API für OAuth-Callback und Webhooks
- optional ein Secret zur Verschlüsselung der Tokens

Das richtest du einmal für die ganze Plattform ein. Einzelne Repos verbinden die
Projekte danach in ihren eigenen Einstellungen. Siehe
[Git-Integration](/de/git-integration.html).

### E-Mail (Mail-to-Ticket)

Richte den **IMAP-Abruf** ein, damit aus eingehenden E-Mails Vorgänge werden.
Auch das liegt in Mongo und wirkt ohne Neustart. Siehe
[E-Mail zu Vorgang](/de/email-to-ticket.html).

### Audit-Protokoll

Zeigt administrative und sicherheitsrelevante Aktionen auf der Instanz.

## Wie es weitergeht

- [Single Sign-on](/de/sso.html): einen Identitätsanbieter verbinden.
- [Git-Integration](/de/git-integration.html): OAuth-Apps und Repos pro Projekt.
- [E-Mail zu Vorgang](/de/email-to-ticket.html): eingehende Mails in Vorgänge umwandeln.
- [Authentifizierung](/de/authentication.html): Konten, Registrierung und 2FA.
