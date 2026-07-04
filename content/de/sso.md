---
title: Single Sign-on (SSO)
description: OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP Single Sign-on in Hinata zur Laufzeit konfigurieren — Keycloak, Authentik, Azure AD, Google, Synology SSO und mehr.
---

# Single Sign-on (SSO)

Hinata kann die Authentifizierung an deinen Identity Provider delegieren, sodass sich Personen mit dem Konto anmelden, das sie bereits haben. Es unterstützt **OpenID Connect (OIDC)**, generisches **OAuth 2.0**, **SAML 2.0** und **LDAP**, und jeder Provider wird **zur Laufzeit aus dem Adminbereich** konfiguriert — gespeichert in MongoDB, angewendet **ohne Neustart**, wobei Secrets **write-only** gehalten werden.

Getestet gegen gängige IdPs, darunter **Keycloak**, **Authentik**, **Synology SSO**, **Microsoft Entra ID (Azure AD)** und **Google**. Für das eingebaute Benutzername/Passwort-System siehe [Authentifizierung](/de/authentication.html).

## Wie es funktioniert

1. Ein Betreiber fügt unter **Admin → SSO** einen Provider hinzu und speichert ihn. Da die Konfiguration in Mongo lebt, ist sie sofort live — keine Umgebungsänderung, kein erneutes Deployment.
2. Die App holt die Liste der aktivierten Provider vom öffentlichen Endpunkt **`/api/v1/auth/sso/providers`** und rendert pro Provider einen Anmelde-Button auf dem Login-Bildschirm.
3. Der Benutzer wird zum Identity Provider zur Authentifizierung geschickt.
4. Der IdP leitet zurück an Hinatas Callback; der Server verifiziert die Antwort, provisioniert oder matcht den Benutzer und übergibt die Kontrolle über den **`hinata://auth-callback`**-Deep-Link zurück an die App (oder den entsprechenden Universal-Link im Web-Build).

!!! info "Funktioniert hinter Proxies und Tunneln"
    Der **OAuth-2.0-Authorization-Request-State wird in MongoDB gespeichert**, nicht in einem Cookie oder einer HTTP-Session. Das bedeutet, dass der Flow Reverse Proxies, Load Balancer und Dev-Tunnel (z. B. ngrok) übersteht, die sonst das Session-Cookie verwerfen oder umschreiben würden — eine häufige Ursache von `authorization_request_not_found`-Fehlern anderswo.

## Laufzeitkonfiguration, write-only Secrets

Alles an einem Provider — Issuer, Client-ID, Scopes, Attribut-Mapping — wird im Adminbereich bearbeitet und in Mongo persistiert, wo die **Datenbank die Umgebung überschreibt**. Client-Secrets und Signaturschlüssel sind **write-only**: Du kannst sie setzen oder ersetzen, aber die API gibt sie nie zurück. So bleiben Zugangsdaten aus Logs, aus API-Antworten und aus der App heraus.

## OpenID-Connect-Beispiel

OIDC ist das empfohlene Protokoll für moderne IdPs (Keycloak, Authentik, Entra ID, Google, Synology SSO). Eine minimale Konfiguration:

| Feld | Beispielwert | Hinweise |
| --- | --- | --- |
| Protokoll | `OIDC` | OpenID Connect (OAuth 2.0 + Identitätsschicht) |
| Anzeigename | `Company SSO` | Beschriftung auf dem Login-Button |
| Issuer | `https://id.example.com/realms/company` | Die Issuer-URL des IdP; Discovery-Dokument unter `/.well-known/openid-configuration` |
| Client-ID | `hinata` | Der Client, den du im IdP registrierst |
| Client-Secret | `••••••••` | Write-only; verschlüsselt gespeichert, nie zurückgegeben |
| Scopes | `openid profile email` | `openid` ist erforderlich; `email` wird zum Matchen/Provisionieren verwendet |
| Redirect-URI | `https://api.track.example.com/api/v1/auth/sso/callback` | Registriere genau diese URL im IdP |

!!! warning "Registriere die exakte Redirect-URI"
    Die **Redirect-/Callback-URI, die du beim Identity Provider einträgst, muss exakt mit der Callback-URL des Servers übereinstimmen** — Schema, Host, Port und Pfad. Ein abweichender Slash am Ende oder ein `http`-vs.-`https`-Mismatch ist die Ursache Nummer eins für fehlgeschlagene Logins. Verwende deine **öffentliche API-Basis** (z. B. `https://api.track.example.com`), nicht einen internen Hostnamen, und füge jede Umgebung, die du betreibst (Staging, Produktion), als separate erlaubte Redirect-URI hinzu.

### Was der IdP erlauben muss

- Die **Redirect-URI** von oben, auf deinem öffentlichen API-Host.
- Das Post-Login-Rücksprungziel der App — der `hinata://auth-callback`-Deep-Link wird vom Client behandelt, sodass dafür keine zusätzliche IdP-Konfiguration nötig ist, aber jeder webbasierte Post-Login-Redirect muss auf deinen erlaubten Origins (`HINATA_CORS_ALLOWED_ORIGINS`) liegen.

## Weitere Protokolle

- **OAuth 2.0** — für Provider ohne vollständiges OIDC-Discovery-Dokument. Du gibst die Authorization-, Token- und User-Info-Endpunkte explizit an und mappst die zurückgegebenen Profilfelder.
- **SAML 2.0** — Enterprise-SSO. Du tauschst Metadaten mit dem IdP aus (Entity-ID, ACS-URL, Signaturzertifikat) und mappst Assertion-Attribute auf den Hinata-Benutzer.
- **LDAP** — Bind gegen ein Verzeichnis (z. B. Active Directory, OpenLDAP) mit einer Suchbasis und Benutzer-/Gruppenfiltern; geeignet für On-Prem-Verzeichnisse ohne Web-SSO-Schicht.

!!! warning "SAML: achte auf die Uhr"
    SAML-Assertions sind zeitgebunden und signiert. Weicht die Uhr des Hinata-Servers von der des IdP ab, werden gültige Assertions als abgelaufen oder noch-nicht-gültig abgelehnt. Halte **NTP** auf dem Server-Host am Laufen und erlaube nur eine kleine Toleranz für Uhrabweichung. Prüfe außerdem, dass du das **Signaturzertifikat** des IdP validierst, und rotiere es, bevor es abläuft.

## Provisioning und Zugriff

Ein erstes SSO-Login provisioniert einen Hinata-Benutzer, gematcht über die E-Mail. Von da an gilt das übliche Modell: Projekt- und Team-Mitgliedschaft steuern, was die Person sehen kann (der pro Mitglied gewährte Projektzugriff der Teams), und `ADMIN` ist für den Adminbereich erforderlich. Du kannst SSO mit lokaler Authentifizierung kombinieren oder `localAuthEnabled = false` setzen (siehe [Authentifizierung](/de/authentication.html)), um SSO zum einzigen Zugangsweg zu machen.

## Fehlerbehebung

- **`authorization_request_not_found`** — fast immer ein Proxy/Tunnel, der den Session-State verwirft. Hinata speichert diesen bereits in Mongo; stelle sicher, dass du auf einem aktuellen Build bist und dass dein Reverse Proxy den Callback-Pfad unverändert weiterleitet.
- **Redirect-URI-Mismatch** — prüfe die beim IdP registrierte URI Zeichen für Zeichen gegen deine öffentliche API-Basis.
- **SAML „assertion expired"** — Uhrabweichung; korrigiere NTP auf dem Server-Host.
- **Keine Provider auf dem Login-Bildschirm** — bestätige, dass der Provider aktiviert ist und dass die App `/api/v1/auth/sso/providers` erreichen kann (er ist öffentlich, kein Token erforderlich).

## Wie geht es weiter

- **[Authentifizierung](/de/authentication.html)** — lokale Zugangsdaten, 2FA und die AuthPolicy-Flags, die du mit SSO kombinierst.
- **[Sicherheitsmodell](/de/security.html)** — wie Tokens, Header und Rate Limiting die gesamte Angriffsfläche schützen.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html)** — den öffentlichen Host und die weitergeleiteten Header richtig setzen, damit Callbacks ankommen.
