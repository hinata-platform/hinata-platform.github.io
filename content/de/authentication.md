---
title: Authentifizierung
description: Wie Hinata Benutzer authentifiziert — lokale Zugangsdaten, Selbstregistrierung, E-Mail-Verifizierung, Passwort-vergessen, Admin-Freigabe, Zwei-Faktor-Authentifizierung und Sitzungen.
---

# Authentifizierung

Hinata liefert ein vollständiges lokales Authentifizierungssystem mit: Login per Benutzername/Passwort, optionaler Selbstregistrierung samt E-Mail-Verifizierung, einem Passwort-vergessen-Flow, der die App über einen Deep Link erreicht, optionaler Admin-Freigabe neuer Konten und zeitbasierter Zwei-Faktor-Authentifizierung. Jeder Modus wird zur Laufzeit aus dem Adminbereich umgeschaltet — ohne Neustart, ohne erneutes Deployment.

Diese Seite behandelt das eingebaute Zugangsdaten-System. Für föderiertes Login (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP) siehe [Single Sign-on](/de/sso.html); für die zugrunde liegende Härtung und das Bedrohungsmodell siehe das [Sicherheitsmodell](/de/security.html).


![Hinata-Kontoeinstellungen](/assets/img/shot-settings.png)
*Kontoeinstellungen — Profil, Sicherheit, 2FA, Sitzungen und Benachrichtigungen.*

## Lokale Zugangsdaten

Benutzer melden sich mit einem Benutzernamen (oder einer E-Mail-Adresse) und einem Passwort an. Passwörter werden mit **BCrypt (Stärke 12)** gehasht und niemals im Klartext gespeichert oder geloggt. Bei Erfolg stellt der Server ein kurzlebiges **JWT-Access-Token** und ein **Refresh-Token** aus; die App speichert sie pro Server und aktualisiert sie transparent.

Vom Server erzwungene Passwortregeln:

- **Mindestens 10 Zeichen** — die Länge ist der stärkste Hebel gegen Brute Force.
- Gehasht mit BCrypt Stärke 12, sodass jede Verifizierung bewusst langsam ist.

!!! tip "Länge vor Komplexität"
    Hinata verlangt absichtlich Länge statt eines Zoos an Sonderzeichen-Regeln. Eine Passphrase mit 10+ Zeichen ist zugleich stärker und für Menschen leichter zu merken. Ermutige deine Benutzer, einen Passwortmanager zu verwenden.

## Feature-Flags: AuthPolicy

Drei Flags steuern das Verhalten der lokalen Authentifizierung. Sie leben in einer **AuthPolicy**, die in MongoDB gespeichert und über **Admin → Benutzer / App** bearbeitbar ist — der Datenbankwert überschreibt den Standard aus der Umgebung und wird **ohne Neustart** wirksam.

| Flag | Was es steuert | Typischer Standard |
| --- | --- | --- |
| `localAuthEnabled` | Ob Login per Benutzername/Passwort überhaupt erlaubt ist. Schalte es **aus**, um SSO-only zu erzwingen. | `true` |
| `registrationEnabled` | Ob Besucher sich selbst aus der App registrieren können. Aus = Admins legen jedes Konto an. | hängt vom Deployment ab |
| `requireAdminApproval` | Ob ein neu registriertes (und E-Mail-verifiziertes) Konto von einem Admin freigegeben werden muss, bevor es sich anmelden kann. | `false` |

Die App liest die effektive Policy beim Start vom öffentlichen Endpunkt `/api/v1/meta` und passt den Login-Bildschirm entsprechend an — sie blendet den Registrieren-Link aus, wenn Registrierung deaktiviert ist, blendet das Passwortformular aus, wenn lokale Authentifizierung deaktiviert ist, und so weiter.

!!! info "SSO-only-Deployments"
    Setze `localAuthEnabled = false`, sobald dein SSO-Provider konfiguriert ist und jeder Benutzer eine föderierte Identität hat. Das Passwortformular verschwindet und nur die SSO-Buttons bleiben. Du kannst es jederzeit wieder einschalten, um den Zugang wiederherzustellen.

## Selbstregistrierung und E-Mail-Verifizierung

Wenn `registrationEnabled` aktiv ist, zeigt die App einen **Konto-erstellen**-Flow. Der Ablauf ist:

1. Der Besucher übermittelt Anzeigename, Benutzername, E-Mail und Passwort (validiert gegen die obigen Passwortregeln).
2. Der Server legt das Konto in einem **unverifizierten** Zustand an und schickt einen Verifizierungslink per E-Mail.
3. Der Link öffnet die App (Deep Link) oder den Web-Build und bestätigt die E-Mail gegenüber dem Server.
4. Ist `requireAdminApproval` aktiv, wartet das Konto anschließend in einer **ausstehenden** Warteschlange, bis ein Admin es unter **Admin → Benutzer** freigibt. Andernfalls kann sich der Benutzer nach der Verifizierung sofort anmelden.

!!! warning "E-Mail muss tatsächlich funktionieren"
    Verifizierung, Freigabe und Passwort-Reset hängen alle vom ausgehenden Mailversand ab. Konfiguriere `HINATA_SMTP_*` und `HINATA_MAIL_FROM`, bevor du die Selbstregistrierung aktivierst, und prüfe die Zustellung — siehe [E-Mail & SMTP](/de/email.html). In der Entwicklung liefert der Stack Mailpit mit, sodass du jede Nachricht lokal lesen kannst.

### Optionale Admin-Freigabe

Mit `requireAdminApproval = true` landen verifizierte Konten in einer ausstehenden Liste. Admins geben sie unter **Admin → Benutzer** frei (oder lehnen sie ab). Das ist die empfohlene Haltung für ein offenes Registrierungsformular in einem öffentlichen Netz: Jeder kann Zugang anfragen, aber ein menschlicher Gatekeeper hält den Workspace sauber.

## Passwort vergessen

Der Reset-Flow ist bewusst App-first und verrät nichts darüber, welche Adressen existieren:

1. Auf dem Login-Bildschirm tippt der Benutzer auf **Passwort vergessen?** und gibt seine E-Mail ein.
2. Der Server antwortet immer gleich (er bestätigt nie, ob eine Adresse registriert ist) und schickt, falls das Konto existiert, einen Reset-Link per E-Mail.
3. Der Link trägt ein Einmal-Token und öffnet die App über den **`hinata://`-Deep-Link** (oder einen **HTTPS-Universal-Link** zu `https://track.example.com` auf dafür konfigurierten Plattformen). Die Reset-Oberfläche wird nativ von der App gerendert — das Backend liefert kein Passwort-HTML.
4. Der Benutzer setzt ein neues Passwort (erneut mit dem Minimum von 10 Zeichen) und das Token wird verbraucht.

!!! info "Warum ein Deep Link?"
    Den Reset-Bildschirm innerhalb der App zu belassen bedeutet, dass es keine servergerenderte Passwortseite gibt, die separat gehärtet, gestylt oder lokalisiert werden müsste. Die E-Mail übergibt schlicht ein Token zurück an den Client, dem du bereits vertraust. Auf nativen Plattformen registriert die App das `hinata://auth-callback`-/Reset-Schema; im Web-Build öffnet der Universal-Link dieselbe Route.

## Zwei-Faktor-Authentifizierung (TOTP)

Hinata unterstützt **zeitbasierte Einmalpasswörter (TOTP)** — die sechsstelligen Codes von Google Authenticator, 1Password, Aegis und ähnlichen Apps.

### 2FA aktivieren

Aus den **Einstellungen** (dem Konto-Bildschirm `/settings`) öffnet ein Benutzer den Zwei-Faktor-Bereich:

1. Der Server generiert ein TOTP-Secret und liefert eine `otpauth://`-Provisioning-URI zurück, angezeigt als QR-Code.
2. Der Benutzer scannt sie mit seiner Authenticator-App.
3. Er bestätigt durch Eingabe eines aktuellen 6-stelligen Codes, was 2FA für das Konto aktiviert.

### Die 2FA-Abfrage beim Login

Sobald TOTP aktiviert ist, wird das Login zweistufig. Der Benutzer übermittelt Benutzername und Passwort; sind die Zugangsdaten gültig, antwortet der Server mit einer **2FA-Abfrage** statt mit Tokens. Die App fordert dann den aktuellen 6-stelligen Code an und schließt das Login ab. Erst nach einem korrekten Code stellt der Server die Access- und Refresh-Tokens aus.

!!! tip "Halte einen Wiederherstellungspfad bereit"
    Behandle das Authenticator-Gerät wie ein Zugangsdatum. Verliert ein Benutzer es, kann ein Admin den zweiten Faktor des Kontos aus dem Adminbereich zurücksetzen, sodass sich der Benutzer neu registrieren kann.

## Sitzungen

Jedes erfolgreiche Login erzeugt einen Datensatz in einer **`sessions`-Collection** in MongoDB, und das ausgestellte JWT trägt einen **Session-ID-Claim (`sid`)**, der das Token an diesen Datensatz bindet. Das macht Tokens einzeln widerrufbar — Abmelden oder Widerrufen einer Sitzung entwertet ihre `sid`, sodass ein durchgesickertes Token abgeschaltet werden kann, ohne das globale Signaturgeheimnis zu rotieren.

### Sitzungsverwaltung

Aus den **Einstellungen** sehen Benutzer ihre aktiven Sitzungen (Gerät / Client, letzte Aktivität) und können jede davon **widerrufen** — zum Beispiel nach einer Anmeldung auf einem gemeinsam genutzten Rechner. Das Widerrufen einer Sitzung stoppt sofort die Annahme ihrer Tokens.

!!! note "Refresh-Tokens sind nur zum Refresh da"
    Access- und Refresh-Tokens sind getrennt. Ein Refresh-Token wird **nur** am Refresh-Endpunkt akzeptiert, um ein neues Access-Token auszustellen — überall sonst in der API wird es abgelehnt. Siehe das [Sicherheitsmodell](/de/security.html) für das vollständige Token-Design.

## Konto, Datenschutz und Avatar

Derselbe `/settings`-Bildschirm ist der Self-Service-Hub des Benutzers:

- **Profil** — Anzeigename und Details.
- **E-Mail-Änderung** — mit erneuter Verifizierung der neuen Adresse.
- **Benachrichtigungsmatrix** — pro Kategorie In-App- und E-Mail-Einstellungen.
- **Avatar-Upload** — ein Profilbild, gespeichert in S3/MinIO (hochgeladen über die Konto-API, zurückgeliefert über einen Private-Bucket-Proxy, serverseitig begrenzt und neu kodiert). Benutzer können es jederzeit hochladen oder entfernen.
- **DSGVO-Export & -Löschung** — ein Benutzer kann seine persönlichen Daten selbst **exportieren** und sein Konto selbst **löschen**, womit die Anforderungen an Datenportabilität und Recht auf Löschung ohne Admin-Ticket erfüllt sind.

!!! info "DSGVO by Design"
    Da Hinata selbst gehostet wird, verlassen die Daten deine Infrastruktur nie — und die eingebauten Export-/Lösch-Werkzeuge bedeuten, dass du Auskunfts- und Löschanfragen direkt aus der App erfüllen kannst.

## Wie geht es weiter

- **[Single Sign-on](/de/sso.html)** — lokales Login durch OIDC, OAuth 2.0, SAML 2.0 oder LDAP ersetzen oder ergänzen.
- **[Sicherheitsmodell](/de/security.html)** — JWT-Design, Rate Limiting, Login-Sperre, Header und das OWASP-Mapping.
- **[Adminbereich](/de/admin-area.html)** — wo die AuthPolicy-Flags, die Benutzerfreigabe und die App-Einstellungen leben.
