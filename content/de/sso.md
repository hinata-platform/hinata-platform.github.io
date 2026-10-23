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

Beim ersten SSO-Login entsteht ein Hinata-Benutzer. Danach gilt das normale Modell:

- Projekt- und Teammitgliedschaft bestimmen, was die Person sieht (Projektzugriff pro Mitglied über Teams).
- Für den Adminbereich ist `ADMIN` nötig.

Du kannst SSO mit lokaler Anmeldung kombinieren. Mit `localAuthEnabled = false` (siehe [Authentifizierung](/de/authentication.html)) wird SSO der einzige Zugang.

### Wie eine Anmeldung ihr Konto findet

Hinata bindet jedes Konto an die Kennung, die der Anbieter selbst für die Person vergibt, nicht an die E-Mail-Adresse. Die Adresse können Personen bei vielen Anbietern im eigenen Profil ändern oder bei der Registrierung frei wählen. Die Kennung vergibt der Anbieter.

| Verfahren | Kennung | Name des Anbieters |
| --- | --- | --- |
| OpenID Connect | `sub` | Issuer-URI |
| OAuth 2.0 | `sub` oder `id` aus den Benutzerdaten, sonst das eingestellte Namensattribut | Host der Autorisierungs-URL |
| SAML 2.0 | NameID | Entity-ID des IdP |
| LDAP | `entryUUID` oder `objectGUID` des Eintrags, sonst sein DN | Basis-DN |

Gibt es ein Konto mit dieser Kennung beim selben Anbieter, geht die Anmeldung in dieses Konto, auch wenn sich die Adresse beim Anbieter inzwischen geändert hat. Gibt es noch kein Konto mit der Adresse, legt Hinata eines an und bindet es gleich an die Kennung. Schickt der Anbieter gar keine Adresse, legt Hinata kein Konto an.

Gibt es ein Konto mit der Adresse, das nicht an diese Kennung gebunden ist, entscheidet die Adresse nur in drei Fällen. Das Konto wird dabei gebunden.

- Das Konto ist über dasselbe Verfahren entstanden und noch nicht gebunden. OpenID Connect und OAuth 2.0 zählen dabei als ein Verfahren. Das betrifft jedes SSO-Konto aus der Zeit vor der Bindung genau einmal, beim ersten Anmelden danach.
- Das Konto ist über denselben Anbieter gebunden, dessen Name sich geändert hat (Spalte rechts). Hinata nimmt dann an, dass du den Identity Provider gewechselt hast, und bindet die Konten beim nächsten Anmelden neu. Eine andere Adresse für denselben Anbieter, etwa `ldaps` statt `ldap` oder ein anderer Pfad bei OAuth 2.0, ist kein Wechsel.
- Es ist ein lokales Konto, und die lokale Anmeldung ist ausgeschaltet. SSO ist dann der einzige Zugang.

Auch dann gilt: Sagt der Anbieter selbst, dass er die Adresse nicht bestätigt hat (`email_verified` ist `false`), bindet sie kein bestehendes Konto. Ein neues Konto bekommt die Person trotzdem, denn darin liegt noch nichts. Gebunden wird außerdem nur, wer auch hereinkommt: Ist das Konto deaktiviert, wartet es auf die Freigabe oder ist es eine offene Einladung, bleibt es ungebunden.

Alles andere lehnt Hinata ab. Wer nur die Adresse angibt, erfährt dabei nichts über das Konto dahinter, also auch nicht, ob es deaktiviert ist oder eine Einladung offen ist. Den genauen Grund findest du im Audit-Protokoll. Ein lokales Konto mit Passwort erreicht man über SSO nur bei ausgeschalteter lokaler Anmeldung; sonst meldet sich die Person mit ihrem Passwort an.

Jede Ablehnung steht im Audit-Protokoll, und jede Bindung eines bestehenden Kontos über die Adresse ebenso, auch wenn das Ereignis in den Audit-Einstellungen aus ist. Die Person bekommt dazu eine Sicherheitsmitteilung mit dem Anbieter und dem Namen, unter dem sich dort jemand angemeldet hat. War sie es nicht, erfährt sie es sofort.

Für alle Wege gelten dieselben Sperren wie bei der Anmeldung mit Passwort: Ein deaktiviertes Konto oder eines, das noch auf die Freigabe wartet, bekommt auch über SSO keinen Zugang.

!!! warning "Eine Kennung, die die Adresse ist, schützt nicht"
    Ist die Kennung beim Anbieter die E-Mail-Adresse, hängt die Bindung wieder an der Adresse. Das passiert bei einer SAML-NameID im E-Mail-Format und bei OAuth 2.0, wenn der Anbieter weder `sub` noch `id` schickt und das Namensattribut `email` ist (die Voreinstellung). Hinata schreibt das als Warnung ins Server-Log. Nimm bei SAML die NameID `persistent` und bei OAuth 2.0 ein festes Namensattribut wie `id`. Eine `transient` NameID wechselt bei jeder Anmeldung; die Person käme nach dem ersten Mal nicht mehr herein.

### Einladungen mit SSO

Hat der Server SSO, kann eine eingeladene Person die Einladung auch mit SSO annehmen. Auf der Einladungsseite steht dann „Mit ‹Anbieter› beitreten“. Die Anmeldung trägt die Einladung mit sich, und der Link aus der Einladungsmail beweist die Adresse. Hinata schließt die Einladung damit ab und bindet das Konto an die Kennung, auch wenn der Anbieter die Person unter einer anderen Adresse kennt. Die Rollen aus der Einladung bleiben.

Ist die lokale Anmeldung aus, ist das der einzige Weg. Ein Passwort lässt sich dann nicht setzen: Anmelden könnte sich damit niemand, und das Konto bliebe bis zur ersten SSO-Anmeldung mit seiner Adresse ungebunden. Über die Adresse allein schließt niemand eine Einladung ab.

### Wenn sich die Kennung ändert

Benennt der Anbieter ein Konto um oder ändert die NameID, kommt die Person nicht mehr in ihr Hinata-Konto. Unter Adminbereich › Benutzer › Person hebst du die Bindung mit „SSO-Verbindung lösen“ auf. Alle Sitzungen der Person enden dabei. Die nächste SSO-Anmeldung mit der Adresse kann das Konto dann neu binden, egal von welchem Konto beim Anbieter sie kommt. Mach das deshalb nur, wenn du sicher bist, dass sich als Nächstes die richtige Person anmeldet. Hinata protokolliert das Lösen immer, auch wenn das Ereignis in den Audit-Einstellungen ausgeschaltet ist.

### Nach dem Update auf die Bindung

Beim ersten Start meldet Hinata einmalig alle ab, die vorher allein über die Adresse erreichbar waren. Ist ein SSO-Verfahren oder LDAP eingeschaltet oder die lokale Anmeldung aus, sind das alle Konten. In welches Konto eine solche Anmeldung kam, weiß nämlich nur das Audit-Protokoll, und das lässt sich ausschalten und vergisst nach einem Jahr. Ist alles davon aus, sind es die Konten aus SSO oder LDAP und die Konten, in die sich laut Audit-Protokoll jemand über SSO angemeldet hat. Wer sich danach anmeldet, bindet sein Konto an sich. Kündige das Update am besten vorher an.

Bei der ersten Anmeldung danach bekommen SSO-Konten aus der Zeit vor der Bindung eine Sicherheitsmitteilung, dass ihr Konto verbunden wurde. Alle anderen bekommen die übliche Mitteilung über eine Anmeldung von einem neuen Gerät.

!!! warning "Prüfe vorher `email_verified`"
    Schickt dein Anbieter für deine Leute `email_verified: false`, bindet Hinata ihre Konten aus der Zeit vor der Bindung nicht, und sie kommen nicht mehr herein. Keycloak tut das zum Beispiel für alle Personen aus einer LDAP-Föderation, solange dort „Trust Email“ aus ist, und für Personen, die ein Admin ohne „E-Mail bestätigt“ angelegt hat. Stell das beim Anbieter vor dem Update um.

Persönliche Zugriffstoken und verbundene KI-Clients bleiben bestehen. Prüfe im Audit-Protokoll bei Konten mit SSO-Anmeldungen, ob dort Token oder Freigaben angelegt wurden, die die Person nicht kennt, und widerrufe sie gegebenenfalls.

## Fehlerbehebung

- **`authorization_request_not_found`:** fast immer ein Proxy oder Tunnel, der den Session-State verwirft. Hinata speichert ihn bereits in Mongo. Prüfe, ob du einen aktuellen Build nutzt und dein Reverse Proxy den Callback-Pfad unverändert weiterleitet.
- **Redirect-URI passt nicht:** Vergleiche die beim IdP registrierte URI Zeichen für Zeichen mit deiner öffentlichen API-Basis.
- **SAML „assertion expired“:** Uhrabweichung. Korrigiere NTP auf dem Server.
- **Keine Provider auf dem Login:** Prüfe, ob der Provider aktiv ist und die App `/api/v1/auth/sso/providers` erreicht (öffentlich, ohne Token).
- **„Für diese E-Mail-Adresse gibt es schon ein Konto, das nicht mit dieser Anmeldung verbunden ist“:** Das Konto ist lokal, es ist über ein anderes Verfahren entstanden (etwa SAML statt OIDC), es ist an eine andere Kennung beim Anbieter gebunden, oder es ist deaktiviert, wartet auf die Freigabe oder ist eine offene Einladung. Welcher Grund es war, steht im Audit-Protokoll beim Eintrag `LOGIN_FAILURE`. Lokale Konten melden sich mit ihrem Passwort an, Eingeladene über den Link in ihrer Einladung. Hat sich die Kennung der Person geändert, löse die Verbindung wie oben beschrieben.
- **„Dein Anmeldedienst meldet diese E-Mail-Adresse als nicht bestätigt“:** Der Anbieter schickt `email_verified: false`, und es gibt schon ein Konto mit der Adresse. Lass die Adresse beim Anbieter bestätigen oder ihn den Adressen vertrauen (Keycloak: „Trust Email“ in der LDAP-Föderation).
- **„Dein Anmeldedienst hat keine E-Mail-Adresse übermittelt“:** Der Anbieter schickt kein Adressattribut, oder das eingestellte Attribut enthält keine Adresse. Prüfe die Attributzuordnung des Verfahrens im Adminbereich.

## Wie geht es weiter

- **[Authentifizierung](/de/authentication.html):** lokale Zugangsdaten, 2FA und die AuthPolicy-Flags, die du mit SSO kombinierst.
- **[Sicherheitsmodell](/de/security.html):** wie Tokens, Header und Rate Limiting die gesamte Angriffsfläche schützen.
- **[Reverse Proxy & TLS](/de/reverse-proxy.html):** öffentlichen Host und weitergeleitete Header richtig setzen, damit Callbacks ankommen.
