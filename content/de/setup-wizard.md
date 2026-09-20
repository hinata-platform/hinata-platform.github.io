---
title: Setup & Erststart
description: Beim Erststart verbindest du die App mit dem Server und legst Organisation und ersten Admin an, per Assistent oder automatisch.
---

# Setup & Erststart

Ein frischer Hinata-Server hat weder Benutzer noch Organisation. Beim **Erststart** verbindest du die App mit dem Server, und ein **Setup-Assistent** in der App legt Organisation und erstes Admin-Konto an.

## Der Ablauf im Überblick

1. **Verbinden:** Die App fragt nach deiner Server-URL und ruft `HINATA_BASE_URL` auf.
2. **Versionsprüfung:** Die App vergleicht ihre Version mit `HINATA_APP_MIN_VERSION`. Ältere Clients müssen erst aktualisieren.
3. **Setup-Status:** Die App ruft `GET /api/v1/setup/status` auf. Ist das Setup nicht abgeschlossen, zeigt sie den Assistenten statt des Logins.
4. **Organisation und Admin anlegen:** Du gibst Organisationsnamen und Admin-Konto ein. Die App sendet `POST /api/v1/setup`.
5. **Onboarding-Tour:** Nach dem Login zeigt eine kurze Tour Dashboard, Projekte und die ⌘K-Palette.

!!! info "Setup braucht kein Token"
    `GET /setup/status` und `POST /setup` sind öffentlich, weil sie vor dem ersten Konto funktionieren müssen. Nach Abschluss lehnt `POST /setup` jeden weiteren Lauf ab. Eine zweite, unerwünschte Organisation lässt sich so nicht anlegen.

## Die App verbinden

Native Apps haben keine fest eingebaute Server-URL. Du gibst sie beim ersten Start ein (die Webversion nutzt standardmäßig ihre eigene Herkunft). Trage die Basis-URL deiner **API** ein:

```text
https://api.track.example.com
```

Die App speichert den Server und prüft ihn live. Später kannst du mehrere Server speichern und zwischen ihnen wechseln. Mehr dazu:

- [Die Apps](/de/clients.html): Verwaltung mehrerer Server.
- [Reverse Proxy & TLS](/de/reverse-proxy.html): wie der Hostname zum API-Container führt.

!!! tip "Mit der Mindestversion erzwingst du Updates"
    `HINATA_APP_MIN_VERSION` (Standard `1.0.0`) ist die älteste App-Version, die dein Server akzeptiert. Erhöhst du sie nach einer Breaking Change, werden ältere Apps zum Update aufgefordert. Der Wert kommt über `/api/v1/meta` und lässt sich live unter [Adminbereich → Plattform](/de/admin-area.html) ändern (DB überschreibt Env).

## Interaktiver Setup-Assistent

Meldet `GET /setup/status` ein offenes Setup, erscheint der Assistent. Du gibst ein:

- **Organisationsname:** Name deines Workspace oder Unternehmens.
- **Admin-Anzeigename:** So erscheint der erste Admin in der Oberfläche.
- **Admin-Benutzername** und **E-Mail**.
- **Admin-Passwort:** mindestens 10 Zeichen (mit BCrypt gehasht, Stärke 12).

Beim Absenden legt `POST /api/v1/setup` Organisation und ersten `ADMIN`-Benutzer in einem atomaren Schritt an und meldet dich direkt an. Danach legst du Projekte an und lädst Leute ein, siehe [Projekte & Teams](/de/projects-teams.html).

## Automatisches Setup

Für skriptgesteuerte oder reproduzierbare Deployments überspringst du den Assistenten. Der Server schließt das Setup dann beim Booten ab. Setze `HINATA_SETUP_AUTO_COMPLETE=true` und die Admin-Daten als Umgebungsvariablen:

```properties
# In-App-Erststart-Assistent überspringen und Org + ersten Admin beim Booten anlegen
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-to-a-strong-password
HINATA_SETUP_ADMIN_DISPLAY_NAME=Platform Admin
```

Beim nächsten Start legt der Server Organisation und Admin an. `GET /setup/status` meldet sofort „abgeschlossen“, und die App geht direkt zum Login. Das ist idempotent: Ist das Setup schon erledigt, werden die Variablen ignoriert.

!!! warning "Das Admin-Passwort ist ein Secret"
    `HINATA_SETUP_ADMIN_PASSWORD` steht im Klartext in deiner `.env` bzw. im Secret-Store deines Orchestrators. Nimm einen starken Wert, halte die Datei aus der Versionskontrolle heraus (siehe [Backups & Upgrades](/de/backups.html)) und ändere das Passwort nach dem ersten Login in der App. Kürzer als 10 Zeichen lehnt der Server ab.

## Onboarding-Tour

Nach dem ersten Login zeigt eine kurze Tour den *heutigen Fokus* im Dashboard, wie du dein erstes Projekt anlegst und die ⌘K-Befehlspalette ([Suche & Palette](/de/search.html)). Sie erscheint nur einmal und lässt sich jederzeit schließen.

## Lokal evaluieren mit dem Demo-Seed

Für einen schnellen lokalen Blick mit realistischen Inhalten (Projekte, Vorgänge, Sprints, Wissensdatenbank, Personen) aktivierst du den Demo-Seeder. Er legt einen kompletten englischen Workspace an **und** schließt den Erststart für dich ab:

```properties
# Nur Dev: realistischen Demo-Workspace beim Booten seeden
HINATA_DEMO_SEED=true
# Optional: bei jedem Boot denselben Datensatz löschen und neu seeden (wiederholbares Testen)
HINATA_DEMO_RESET=false
```

Anmeldung:

```text
Benutzername: rebar
Passwort:     hinata-demo-2026
```

!!! danger "Den Demo-Seed nie in Produktion aktivieren"
    Der Seeder hat `@Profile("!prod")` und wird im `prod`-Profil **komplett übersprungen**, egal was in `HINATA_DEMO_SEED` steht. Er ist zum Durchklicken und für Screenshots auf einem Dev-Profil gedacht. Das Passwort ist öffentlich bekannt, und mit `HINATA_DEMO_RESET=true` **löscht er den Workspace bei jedem Boot**. Lass ihn überall aus, wo echte Daten liegen.

## Fehlerbehebung

| Symptom | Wahrscheinliche Ursache |
| --- | --- |
| App zeigt „Update erforderlich“ und geht nicht weiter | Client-Version < `HINATA_APP_MIN_VERSION`. App aktualisieren oder Mindestversion senken |
| Assistent erscheint nie, App geht direkt zum Login | Setup schon abgeschlossen (`GET /setup/status` meldet fertig) oder Auto-Complete lief |
| Server beim Verbinden nicht erreichbar | Falsche URL, Proxy oder TLS falsch konfiguriert oder CORS-Origin fehlt. Siehe [Reverse Proxy & TLS](/de/reverse-proxy.html) |
| `POST /setup` abgelehnt | Setup lief schon einmal. Es läuft nur, solange keine Organisation existiert |

## Nächste Schritte

- [Authentifizierung](/de/authentication.html): Logins, Registrierung, 2FA und Passwort zurücksetzen
- [Adminbereich](/de/admin-area.html): Plattform-Einstellungen, Laufzeitkonfiguration
- [Projekte & Teams](/de/projects-teams.html): erstes Projekt anlegen und Leute einladen
- [Backups & Upgrades](/de/backups.html): den laufenden Stack absichern
