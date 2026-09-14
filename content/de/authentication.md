---
title: Authentifizierung
description: Wie sich Benutzer bei Hinata anmelden, mit Passwort, Registrierung, E-Mail-Verifizierung, Passwort-Reset, Freigabe durch Admins, 2FA und Sitzungen.
---

# Authentifizierung

Hinata bringt eine vollständige lokale Anmeldung mit:

- Login mit Benutzername und Passwort
- optionale Selbstregistrierung mit E-Mail-Verifizierung
- Passwort vergessen, mit Deep Link in die App
- optionale Freigabe neuer Konten durch Admins
- zeitbasierte Zwei-Faktor-Authentifizierung

Jeden Modus schaltest du zur Laufzeit im Adminbereich um, ohne Neustart oder Redeploy.

Föderiertes Login (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP) steht unter [Single Sign-on](/de/sso.html). Härtung und Bedrohungsmodell stehen im [Sicherheitsmodell](/de/security.html).


![Hinata-Kontoeinstellungen](/assets/img/shot-settings.png)
*Kontoeinstellungen mit Profil, Sicherheit, 2FA, Sitzungen und Benachrichtigungen.*

## Lokale Zugangsdaten

Benutzer melden sich mit Benutzername (oder E-Mail-Adresse) und Passwort an. Passwörter werden mit **BCrypt (Stärke 12)** gehasht und nie im Klartext gespeichert oder geloggt. Nach dem Login stellt der Server ein kurzlebiges **JWT-Access-Token** und ein **Refresh-Token** aus. Die App speichert beide pro Server und erneuert sie automatisch.

Passwortregeln des Servers:

- **Mindestens 10 Zeichen.** Länge schützt am stärksten gegen Brute Force.
- Gehasht mit BCrypt Stärke 12, jede Prüfung ist dadurch absichtlich langsam.

!!! tip "Länge vor Komplexität"
    Hinata verlangt Länge statt vieler Regeln für Sonderzeichen. Eine Passphrase mit 10+ Zeichen ist stärker und leichter zu merken. Empfiehl deinen Benutzern einen Passwortmanager.

## Feature-Flags: AuthPolicy

Drei Flags steuern die lokale Anmeldung. Sie liegen in der **AuthPolicy** in MongoDB und sind unter **Admin → Benutzer / App** änderbar. Der Wert aus der Datenbank überschreibt den Standard aus der Umgebung und wirkt **ohne Neustart**.

| Flag | Was es steuert | Typischer Standard |
| --- | --- | --- |
| `localAuthEnabled` | Ob Login per Benutzername/Passwort überhaupt erlaubt ist. **Aus** erzwingt reines SSO. | `true` |
| `registrationEnabled` | Ob Besucher sich in der App selbst registrieren können. Aus heißt: Admins legen jedes Konto an. | hängt vom Deployment ab |
| `requireAdminApproval` | Ob ein neu registriertes (und E-Mail-verifiziertes) Konto von einem Admin freigegeben werden muss, bevor es sich anmelden kann. | `false` |

Die App liest die gültige Policy beim Start vom öffentlichen Endpunkt `/api/v1/meta` und passt den Anmeldebildschirm an. Ist die Registrierung aus, fehlt der Link zum Registrieren. Ist die lokale Anmeldung aus, fehlt das Passwortformular.

!!! info "Deployments nur mit SSO"
    Setze `localAuthEnabled = false`, sobald dein SSO-Provider eingerichtet ist und jeder Benutzer eine föderierte Identität hat. Dann verschwindet das Passwortformular und nur die SSO-Buttons bleiben. Du kannst das Flag jederzeit wieder einschalten, um den Zugang wiederherzustellen.

## Selbstregistrierung und E-Mail-Verifizierung

Ist `registrationEnabled` aktiv, zeigt die App den Ablauf **Konto erstellen**:

1. Der Besucher gibt Anzeigename, Benutzername, E-Mail und Passwort ein (geprüft nach den Passwortregeln oben).
2. Der Server legt das Konto **unverifiziert** an und schickt einen Verifizierungslink per E-Mail.
3. Der Link öffnet die App (Deep Link) oder den Web-Build und bestätigt die E-Mail beim Server.
4. Ist `requireAdminApproval` aktiv, wartet das Konto danach als **ausstehend**, bis ein Admin es unter **Admin → Benutzer** freigibt. Sonst kann sich der Benutzer direkt nach der Verifizierung anmelden.

!!! warning "E-Mail muss tatsächlich funktionieren"
    Verifizierung, Freigabe und Passwort-Reset brauchen ausgehende Mail. Richte `HINATA_SMTP_*` und `HINATA_MAIL_FROM` ein, bevor du die Selbstregistrierung aktivierst, und prüfe die Zustellung. Siehe [E-Mail & SMTP](/de/email.html). In der Entwicklung liefert der Stack Mailpit mit, dort liest du jede Nachricht lokal.

### Optionale Freigabe durch Admins

Mit `requireAdminApproval = true` landen verifizierte Konten in einer Warteliste. Admins geben sie unter **Admin → Benutzer** frei oder lehnen sie ab. Das empfiehlt sich für ein offenes Registrierungsformular im öffentlichen Netz: Jeder kann Zugang anfragen, ein Mensch entscheidet darüber.

## Passwort vergessen

Der Reset läuft in der App und verrät nicht, welche Adressen existieren:

1. Auf dem Anmeldebildschirm tippt der Benutzer auf **Passwort vergessen?** und gibt seine E-Mail ein.
2. Der Server antwortet immer gleich und bestätigt nie, ob eine Adresse registriert ist. Existiert das Konto, schickt er einen Reset-Link.
3. Der Link enthält ein Einmal-Token und öffnet die App über den **`hinata://`-Deep-Link** (oder einen **HTTPS-Universal-Link** zu `https://track.example.com` auf Plattformen, die dafür eingerichtet sind). Die App zeigt den Reset-Bildschirm selbst an. Das Backend liefert kein Passwort-HTML.
4. Der Benutzer setzt ein neues Passwort (wieder mindestens 10 Zeichen) und das Token ist verbraucht.

!!! info "Warum ein Deep Link?"
    So gibt es keine Passwortseite auf dem Server, die extra gehärtet, gestaltet und übersetzt werden müsste. Die E-Mail gibt nur ein Token an den Client zurück, dem du schon vertraust. Auf nativen Plattformen registriert die App das Schema `hinata://auth-callback` / Reset. Im Web-Build öffnet der Universal Link dieselbe Route.

## Zwei-Faktor-Authentifizierung (TOTP)

Hinata unterstützt **zeitbasierte Einmalpasswörter (TOTP)**, also die sechsstelligen Codes aus Google Authenticator, 1Password, Aegis und ähnlichen Apps.

### 2FA aktivieren

In den **Einstellungen** (dem Kontobildschirm `/settings`) öffnet der Benutzer den Bereich für Zwei-Faktor:

1. Der Server erzeugt ein TOTP-Secret und liefert eine `otpauth://`-Provisioning-URI, angezeigt als QR-Code.
2. Der Benutzer scannt den Code mit seiner Authenticator-App.
3. Er gibt einen aktuellen 6-stelligen Code ein. Damit ist 2FA für das Konto aktiv.

### Die 2FA-Abfrage beim Login

Mit TOTP läuft das Login in zwei Schritten:

1. Der Benutzer sendet Benutzername und Passwort. Sind sie gültig, antwortet der Server mit einer **2FA-Abfrage** statt mit Tokens.
2. Die App fragt den aktuellen 6-stelligen Code ab. Erst nach einem richtigen Code stellt der Server Access- und Refresh-Token aus.

!!! tip "Halte einen Wiederherstellungspfad bereit"
    Behandle das Gerät mit der Authenticator-App wie ein Zugangsdatum. Verliert ein Benutzer es, setzt ein Admin den zweiten Faktor des Kontos im Adminbereich zurück. Danach richtet der Benutzer 2FA neu ein.

## Sitzungen

Jedes erfolgreiche Login legt einen Eintrag in der **`sessions`-Collection** in MongoDB an. Das JWT trägt einen **Session-ID-Claim (`sid`)**, der das Token mit diesem Eintrag verknüpft. So lassen sich Tokens einzeln widerrufen: Abmelden oder Widerrufen entwertet die `sid`. Ein geleaktes Token ist damit abschaltbar, ohne das globale Signaturgeheimnis zu rotieren.

### Sitzungsverwaltung

In den **Einstellungen** sehen Benutzer ihre aktiven Sitzungen (Gerät / Client, letzte Aktivität). Jede davon können sie **widerrufen**, zum Beispiel nach einer Anmeldung an einem gemeinsam genutzten Rechner. Die Tokens einer widerrufenen Sitzung werden sofort abgelehnt.

!!! note "Refresh-Tokens sind nur zum Refresh da"
    Access- und Refresh-Tokens sind getrennt. Ein Refresh-Token gilt **nur** am Refresh-Endpunkt, um ein neues Access-Token auszustellen. Überall sonst lehnt die API es ab. Das vollständige Token-Design steht im [Sicherheitsmodell](/de/security.html).

## Konto, Datenschutz und Avatar

Unter `/settings` verwalten Benutzer ihr Konto selbst:

- **Profil**: Anzeigename und Details.
- **E-Mail-Änderung**: Die neue Adresse wird erneut verifiziert.
- **Benachrichtigungsmatrix**: pro Kategorie Einstellungen für In-App und E-Mail.
- **Avatar-Upload**: ein Profilbild in S3/MinIO. Hochgeladen über die Konto-API, ausgeliefert über einen Proxy für den privaten Bucket, serverseitig in der Größe begrenzt und neu kodiert. Benutzer können es jederzeit hochladen oder entfernen.
- **DSGVO-Export & -Löschung**: Benutzer können ihre persönlichen Daten selbst **exportieren** und ihr Konto selbst **löschen**. Das erfüllt Datenportabilität und Recht auf Löschung ohne Ticket beim Admin.

!!! info "DSGVO by Design"
    Hinata läuft auf deiner eigenen Infrastruktur, die Daten verlassen sie nie. Mit Export und Löschung in der App erfüllst du Auskunfts- und Löschanfragen direkt.

## Wie geht es weiter

- **[Single Sign-on](/de/sso.html)**: lokales Login durch OIDC, OAuth 2.0, SAML 2.0 oder LDAP ersetzen oder ergänzen.
- **[Sicherheitsmodell](/de/security.html)**: JWT-Design, Rate Limiting, Login-Sperre, Header und das OWASP-Mapping.
- **[Adminbereich](/de/admin-area.html)**: wo AuthPolicy-Flags, Benutzerfreigabe und App-Einstellungen liegen.
