---
title: Single Sign-on (SSO)
description: Single Sign-on per OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP zur Laufzeit einrichten, etwa mit Keycloak, Authentik, Azure AD, Google oder Synology SSO.
---

# Single Sign-on (SSO)

Mit SSO melden sich alle über deinen Identity Provider (IdP) an, mit dem Konto, das sie schon haben.

- Unterstützt: **OpenID Connect (OIDC)**, generisches **OAuth 2.0**, **SAML 2.0** und **LDAP**.
- Provider richtest du **zur Laufzeit im Adminbereich** ein. Sie liegen in MongoDB, sind **ohne Neustart** aktiv, und Secrets sind **write-only**.
- Getestet mit **Keycloak**, **Authentik**, **Synology SSO**, **Microsoft Entra ID (Azure AD)** und **Google**.

Lokale Anmeldung mit Benutzername und Passwort: [Authentifizierung](/de/authentication.html).

## Wie es funktioniert

1. Ein Betreiber legt unter **Admin → SSO** einen Provider an und speichert. Er ist sofort aktiv, ohne Änderung an der Umgebung oder neues Deployment.
2. Die App lädt die aktiven Provider vom öffentlichen Endpunkt **`/api/v1/auth/sso/providers`** und zeigt für jeden einen Anmeldebutton auf dem Login.
3. Der Benutzer meldet sich beim Identity Provider an.
4. Der IdP leitet zu Hinatas Callback zurück. Der Server prüft die Antwort, legt den Benutzer an oder ordnet ihn zu und gibt über den Deep Link **`hinata://auth-callback`** an die App zurück (im Web-Build über den passenden Universal Link).

!!! info "Funktioniert hinter Proxies und Tunneln"
    Der **State des OAuth-2.0-Authorization-Requests liegt in MongoDB** statt in Cookie oder HTTP-Session. Deshalb klappt der Ablauf auch hinter Reverse Proxies, Load Balancern und Dev-Tunneln (z. B. ngrok), die das Session-Cookie sonst verwerfen oder umschreiben. Das ist anderswo eine häufige Ursache für `authorization_request_not_found`.

## Laufzeitkonfiguration und Secrets

Alle Providereinstellungen (Issuer, Client-ID, Scopes, Attribut-Mapping) bearbeitest du im Adminbereich. Sie liegen in Mongo, und die **Datenbank überschreibt die Umgebung**.

Client-Secrets und Signaturschlüssel sind **write-only**: Du kannst sie setzen oder ersetzen, die API gibt sie aber nie zurück. So tauchen sie weder in Logs noch in API-Antworten oder in der App auf.

## OpenID-Connect-Beispiel

OIDC ist das empfohlene Protokoll für moderne IdPs (Keycloak, Authentik, Entra ID, Google, Synology SSO). Eine minimale Konfiguration:

| Feld | Beispielwert | Hinweise |
| --- | --- | --- |
| Protokoll | `OIDC` | OpenID Connect (OAuth 2.0 + Identitätsschicht) |
| Anzeigename | `Company SSO` | Beschriftung auf dem Login-Button |
| Issuer | `https://id.example.com/realms/company` | Issuer-URL des IdP. Discovery-Dokument unter `/.well-known/openid-configuration` |
| Client-ID | `hinata` | Der Client, den du im IdP registrierst |
| Client-Secret | `••••••••` | Write-only, verschlüsselt gespeichert, nie zurückgegeben |
| Scopes | `openid profile email` | `openid` ist Pflicht. `email` dient zum Zuordnen und Anlegen von Benutzern |
| Redirect-URI | `https://api.track.example.com/api/v1/auth/sso/callback` | Genau diese URL im IdP registrieren |

!!! warning "Registriere die exakte Redirect-URI"
    Die **Redirect-URI beim Identity Provider muss exakt zur Callback-URL des Servers passen**: Schema, Host, Port und Pfad. Ein abweichender Slash am Ende oder `http` statt `https` ist der häufigste Grund für fehlgeschlagene Logins. Nimm deine **öffentliche API-Basis** (z. B. `https://api.track.example.com`) und keinen internen Hostnamen. Trage jede Umgebung (Staging, Produktion) als eigene erlaubte Redirect-URI ein.

### Was der IdP erlauben muss

- Die **Redirect-URI** von oben auf deinem öffentlichen API-Host.
- Den Rücksprung nach dem Login. Den Deep Link `hinata://auth-callback` verarbeitet der Client, dafür braucht der IdP keine Einstellung. Webbasierte Weiterleitungen nach dem Login müssen aber auf deinen erlaubten Origins liegen (`HINATA_CORS_ALLOWED_ORIGINS`).

## Weitere Protokolle

- **OAuth 2.0:** für Provider ohne vollständiges OIDC-Discovery-Dokument. Du trägst Authorization-, Token- und User-Info-Endpunkt selbst ein und mappst die zurückgegebenen Profilfelder.
- **SAML 2.0:** SSO für Unternehmen. Du tauschst Metadaten mit dem IdP aus (Entity-ID, ACS-URL, Signaturzertifikat) und mappst Assertion-Attribute auf den Hinata-Benutzer.
- **LDAP:** Bind gegen ein Verzeichnis (z. B. Active Directory, OpenLDAP) mit Suchbasis sowie Benutzer- und Gruppenfiltern. Passt für Verzeichnisse im eigenen Netz ohne Web-SSO.

!!! warning "SAML: achte auf die Uhr"
    SAML-Assertions sind signiert und zeitlich begrenzt. Weicht die Uhr des Hinata-Servers von der des IdP ab, werden gültige Assertions als abgelaufen oder noch nicht gültig abgelehnt. Lass **NTP** auf dem Server laufen und erlaube nur eine kleine Uhrabweichung. Validiere außerdem das **Signaturzertifikat** des IdP und tausche es vor Ablauf aus.

## Provisioning und Zugriff

Beim ersten SSO-Login entsteht ein Hinata-Benutzer, zugeordnet über die E-Mail. Danach gilt das normale Modell:

- Projekt- und Teammitgliedschaft bestimmen, was die Person sieht (Projektzugriff pro Mitglied über Teams).
- Für den Adminbereich ist `ADMIN` nötig.

Du kannst SSO mit lokaler Anmeldung kombinieren. Mit `localAuthEnabled = false` (siehe [Authentifizierung](/de/authentication.html)) wird SSO der einzige Zugang.

## Fehlerbehebung

- **`authorization_request_not_found`:** fast immer ein Proxy oder Tunnel, der den Session-State verwirft. Hinata speichert ihn bereits in Mongo. Prüfe, ob du einen aktuellen Build nutzt und dein Reverse Proxy den Callback-Pfad unverändert weiterleitet.
- **Redirect-URI passt nicht:** Vergleiche die beim IdP registrierte URI Zeichen für Zeichen mit deiner öffentlichen API-Basis.
- **SAML „assertion expired“:** Uhrabweichung. Korrigiere NTP auf dem Server.
- **Keine Provider auf dem Login:** Prüfe, ob der Provider aktiv ist und die App `/api/v1/auth/sso/providers` erreicht (öffentlich, ohne Token).

## Wie geht es weiter

- **[Authentifizierung](/de/authentication.html):** lokale Zugangsdaten, 2FA und die AuthPolicy-Flags, die du mit SSO kombinierst.
- **[Sicherheitsmodell](/de/security.html):** wie Tokens, Header und Rate Limiting die gesamte Angriffsfläche schützen.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html):** öffentlichen Host und weitergeleitete Header richtig setzen, damit Callbacks ankommen.
