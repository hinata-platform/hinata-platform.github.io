---
title: Adminbereich
description: Der In-App-Adminbereich — verwalte Benutzer, App-Einstellungen, SSO, Git-OAuth-Apps und Mail-to-Ticket. Die Laufzeitkonfiguration liegt in MongoDB, überschreibt die Umgebung und wirkt ohne Neustart.
---

# Adminbereich

Der größte Teil der betrieblichen Konfiguration von Hinata ist nicht beim Start in
Umgebungsvariablen eingefroren — er liegt im **Adminbereich**, einem
In-App-Steuerungspanel, das seine Einstellungen in MongoDB schreibt. Das ist ein
prägendes Merkmal der Plattform: Die **Datenbank überschreibt die Umgebung**, und
Änderungen wirken **ohne Neustart**. Du konfigurierst eine laufende Instanz live,
aus derselben App, in der auch deine Benutzer arbeiten.

!!! info "Wer Zugriff hat"
    Der Adminbereich erfordert die Rolle **`ADMIN`**, und jeder Endpunkt unter
    `/api/v1/admin/**` ist serverseitig auf Admins beschränkt. Reguläre Benutzer
    sehen ihn nie.


![Hinata-Adminbereich](/assets/img/shot-admin.png)
*Der Adminbereich — Nutzer, App-Einstellungen, SSO, Git und E-Mail-zu-Vorgang, alles zur Laufzeit.*

## Wie die Laufzeitkonfiguration funktioniert

Um einen Server zu starten, braucht es nur eine Handvoll Umgebungsvariablen (ein
JWT-Secret, die Datenbankverbindung, ein Mail-Relay). Alles andere — SSO-Anbieter,
E-Mail-Ingest, Git-OAuth-Apps, App-Einstellungen — wird im Adminbereich
konfiguriert und in MongoDB gespeichert. Daraus folgen drei Regeln:

- **DB überschreibt Env.** Umgebungswerte wie `hinata.app.*` sind *Standardwerte*.
  Ein Wert, den du im Adminbereich setzt, gewinnt gegenüber der Umgebung.
- **Kein Neustart nötig.** Aktualisiere einen Anbieter oder ein Flag, und es wird
  bei der nächsten Anfrage wirksam — kein Redeploy, kein Container-Neustart.
- **Secrets sind schreibgeschützt (write-only).** OAuth-Client-Secrets, Tokens und
  Passwörter können **gesetzt** werden, werden aber von der Admin-API nie
  zurückgegeben. Gespeicherte Git-Tokens sind zusätzlich mit AES-GCM verschlüsselt
  gelagert.

## Die Bereiche

Der Adminbereich ist in Gruppen gegliedert: **Allgemein**, **App** und
**Sicherheit**; **Authentifizierung**, **E-Mail** und **Git-Integration**; sowie
**Audit-Log** und **Benutzer**.

### Benutzer

Verwalte die Personen auf deiner Instanz: **genehmige** ausstehende
Registrierungen, **aktiviere** oder deaktiviere Konten und weise **Rollen**
(einschließlich `ADMIN`) zu. Wenn die Selbstregistrierung mit Admin-Genehmigung
aktiviert ist (siehe unten), reihen sich neue Anmeldungen hier in eine
Warteschlange ein, bis ein Admin sie freigibt.

### App-Einstellungen

Steuere, wie sich Clients gegenüber deinem Server verhalten:

- **Mindestversion** (`minVersion`) — die [Versionssperre](/de/clients.html#versionssperre).
  Ältere Clients werden zum Update gezwungen. Überschreibt `HINATA_APP_MIN_VERSION`.
- **URL der Datenschutzerklärung** — der Link, den die App anzeigt; erforderlich
  für App-Store-/Play-Releases und die DSGVO. Überschreibt
  `HINATA_PRIVACY_POLICY_URL`.
- **Feature-Flags** — schalte Plattformfunktionen um, einschließlich der
  Auth-Flags `localAuthEnabled`, `registrationEnabled` und `requireAdminApproval`
  sowie beliebiger `name → enabled`-Flags, die du hinzufügst.

!!! tip "Diese überschreiben die passenden Env-Variablen"
    Alles, was du hier unter App-Einstellungen setzt, gewinnt gegenüber der
    entsprechenden `hinata.app.*`-Umgebungsvariable. Env-Werte sind nur der
    Ausgangspunkt für eine frische Instanz.

### Authentifizierung & SSO

Konfiguriere, wie sich Personen anmelden. Schalte **lokale Authentifizierung**,
**Selbstregistrierung** und **Admin-Genehmigung** um und registriere
**SSO-Anbieter** — OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP (Synology SSO,
Keycloak, Authentik, Azure AD, Google, …). Anbieter werden in Mongo gespeichert
und sind sofort wirksam. Siehe [Authentifizierung](/de/authentication.html) und
[Single Sign-on](/de/sso.html).

### Git-Integration

Registriere **eine OAuth-App pro Anbieter** (GitHub, GitLab, Bitbucket), damit
Projekte ihre Repositories verbinden können. Du gibst Client-ID + Secret, die
öffentliche API-Basis-URL für den OAuth-Callback und Webhooks sowie ein optionales
Token-Verschlüsselungs-Secret ein. Das ist die plattformweite, einmalige
Einrichtung; Projekte verbinden anschließend einzelne Repos in ihren eigenen
Einstellungen. Siehe [Git-Integration](/de/git-integration.html).

### E-Mail (Mail-to-Ticket)

Konfiguriere das **IMAP-Polling**, damit eingehende E-Mails in Vorgänge
umgewandelt werden. Wie alles hier wird es in Mongo gespeichert und wirkt ohne
Neustart. Siehe [E-Mail zu Vorgang](/de/email-to-ticket.html).

### Audit-Log

Sieh dir eine Aufzeichnung administrativer und sicherheitsrelevanter Aktionen auf
der Instanz an.

## Wie es weitergeht

- [Single Sign-on](/de/sso.html) — verbinde einen Identitätsanbieter.
- [Git-Integration](/de/git-integration.html) — OAuth-Apps und projektbezogene Repos.
- [E-Mail zu Vorgang](/de/email-to-ticket.html) — wandle eingehende Mails in Vorgänge um.
- [Authentifizierung](/de/authentication.html) — Konten, Registrierung und 2FA.
