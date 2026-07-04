---
title: Setup & Erststart
description: Der Erststart-Ablauf — App mit dem Server verbinden, den Versions-Check bestehen und dann Organisation samt erstem Admin per Assistent oder nicht-interaktiv anlegen.
---

# Setup & Erststart

Ein frischer Hinata-Server hat keine Benutzer und keine Organisation. Der
**Erststart** behebt das: Du richtest die App auf deinen Server, und ein
in-App-**Setup-Assistent** legt die Organisation und das erste Admin-Konto an.
Diese Seite führt durch den interaktiven Ablauf, die vollautomatische Alternative
und das Seeden eines Wegwerf-Demo-Workspace zur lokalen Evaluierung.

## Der Ablauf im Überblick

1. **Verbinden** — die App fragt nach deiner Server-URL und ruft `HINATA_BASE_URL` auf.
2. **Versions-Check** — die App prüft ihre Version gegen `HINATA_APP_MIN_VERSION`;
   ältere Clients werden zum Update aufgefordert, bevor es weitergeht.
3. **Setup-Status** — die App ruft `GET /api/v1/setup/status` auf. Ist das Setup
   nicht abgeschlossen, zeigt sie statt des Logins den Assistenten.
4. **Org + Admin anlegen** — du gibst den Organisationsnamen und das erste
   Admin-Konto ein; die App sendet `POST /api/v1/setup`.
5. **Onboarding-Tour** — nach dem Login hebt eine kurze geführte Tour Dashboard,
   Projekte und die ⌘K-Palette hervor.

!!! info "Setup-Endpunkte sind öffentlich"
    `GET /setup/status` und `POST /setup` gehören zu den wenigen Endpunkten, die
    kein Token brauchen — sie müssen funktionieren, bevor ein Konto existiert.
    Nach Abschluss verweigert `POST /setup` einen erneuten Lauf, es kann also
    keine zweite unerwünschte Organisation anlegen.

## Die App verbinden

Native Apps hinterlegen niemals fest eine Server-URL — du gibst sie beim ersten
Start ein (der Web-Build nutzt standardmäßig seine eigene Herkunft). Gib der App
deine **API**-Basis:

```text
https://api.track.example.com
```

Die App speichert diesen Server, prüft ihn live und lässt dich später mehrere
Server speichern und zwischen ihnen wechseln. Siehe [Die Apps](/de/clients.html)
für den Multi-Server-Manager und [Reverse Proxy & TLS](/de/reverse-proxy.html)
dafür, wie dieser Hostname auf den API-Container abbildet.

!!! tip "Der Versions-Check ist dein Force-Update-Schalter"
    `HINATA_APP_MIN_VERSION` (Standard `1.0.0`) ist die Mindest-Client-Version,
    die dein Server akzeptiert. Erhöhe sie nach einer Breaking Change, und ältere
    Apps werden zum Update aufgefordert — ausgeliefert über `/api/v1/meta` und
    auch live editierbar in [Adminbereich → App](/de/admin-area.html) (DB
    überschreibt Env).

## Interaktiver Setup-Assistent

Meldet `GET /setup/status`, dass das Setup unvollständig ist, zeigt die App den
Assistenten. Du gibst an:

- **Organisationsname** — der Name deines Workspace/Unternehmens.
- **Admin-Anzeigename** — wie der erste Admin in der Oberfläche erscheint.
- **Admin-Benutzername** und **E-Mail**.
- **Admin-Passwort** — mindestens 10 Zeichen (mit BCrypt, Stärke 12, gehasht).

Das Absenden sendet `POST /api/v1/setup`, das in einem atomaren Schritt die
Organisation und den ersten `ADMIN`-Benutzer anlegt und dich direkt einloggt. Von
dort legst du Projekte an und lädst Leute ein — siehe
[Projekte & Teams](/de/projects-teams.html).

## Nicht-interaktives Setup (Automatisierung)

Für skriptgesteuerte oder reproduzierbare Deployments kannst du den Assistenten
komplett überspringen und den Server das Setup beim Booten abschließen lassen.
Setze `HINATA_SETUP_AUTO_COMPLETE=true` und liefere die Admin-Daten als
Umgebungsvariablen:

```properties
# In-App-Erststart-Assistent überspringen und Org + ersten Admin beim Booten anlegen
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-to-a-strong-password
HINATA_SETUP_ADMIN_DISPLAY_NAME=Platform Admin
```

Beim nächsten Start legt der Server Organisation und Admin an, und
`GET /setup/status` meldet sofort „abgeschlossen“ — die App geht also direkt zum
Login. Das ist idempotent: Ist das Setup bereits erledigt, werden diese Variablen
ignoriert.

!!! warning "Das Admin-Passwort wie jedes andere Geheimnis behandeln"
    `HINATA_SETUP_ADMIN_PASSWORD` landet im Klartext in deiner `.env` bzw. im
    Secret-Store deines Orchestrators. Nutze einen starken Wert, halte die Datei
    aus der Versionskontrolle heraus (siehe [Backups & Upgrades](/de/backups.html))
    und ändere das Passwort nach dem ersten Login in der App. Die Mindestlänge ist
    10 Zeichen; der Server weist Kürzeres ab.

## Onboarding-Tour

Nach dem ersten Login startet die App eine kurze Onboarding-Tour, die auf den
*heutigen Fokus* des Dashboards hinweist, wie du dein erstes Projekt anlegst und
auf die ⌘K-Befehlspalette ([Suche & Palette](/de/search.html)). Es ist ein
einmaliger Hinweis und jederzeit schließbar.

## Lokal evaluieren mit dem Demo-Seed

Für einen schnellen lokalen Blick auf Hinata mit realistischen Inhalten —
Projekte, Vorgänge, Sprints, Wissensdatenbank und Personen — aktiviere den
Demo-Seeder. Er legt einen kompletten englischen Workspace an **und** schließt
den Erststart für dich ab:

```properties
# Nur Dev — realistischen Demo-Workspace beim Booten seeden
HINATA_DEMO_SEED=true
# Optional: bei jedem Boot denselben Datensatz löschen und neu seeden (wiederholbares Testen)
HINATA_DEMO_RESET=false
```

Logge dich ein mit:

```text
Benutzername: rebar
Passwort:     hinata-demo-2026
```

!!! danger "Den Demo-Seed niemals in Produktion aktivieren"
    Der Seeder ist mit `@Profile("!prod")` annotiert, wird unter dem `prod`-Profil
    also **komplett übersprungen**, unabhängig von `HINATA_DEMO_SEED`. Er dient
    dem Durchklicken der App und dem Erstellen von Screenshots auf einem
    Dev-Profil. Er liefert ein allbekanntes Passwort und **löscht mit
    `HINATA_DEMO_RESET=true` den Workspace bei jedem Boot** — gegen echte Daten
    offensichtlich katastrophal. Lass ihn überall aus, wo es zählt.

## Fehlerbehebung

| Symptom | Wahrscheinliche Ursache |
| --- | --- |
| App zeigt „Update erforderlich“ und geht nicht weiter | Client-Version < `HINATA_APP_MIN_VERSION`; App aktualisieren oder Gate senken |
| Assistent erscheint nie, geht direkt zum Login | Setup bereits abgeschlossen (`GET /setup/status` meldet fertig) oder Auto-Complete lief |
| Server beim Verbinden nicht erreichbar | Falsche URL, Proxy/TLS falsch konfiguriert oder CORS-Origin fehlt — siehe [Reverse Proxy & TLS](/de/reverse-proxy.html) |
| `POST /setup` abgelehnt | Setup wurde bereits einmal abgeschlossen; es läuft nur, wenn keine Org existiert |

## Nächste Schritte

- [Authentifizierung](/de/authentication.html) — Logins, Registrierung, 2FA und Passwort-Reset
- [Adminbereich](/de/admin-area.html) — Feature-Flags, App-Einstellungen, Laufzeitkonfiguration
- [Projekte & Teams](/de/projects-teams.html) — erstes Projekt anlegen und Leute einladen
- [Backups & Upgrades](/de/backups.html) — den laufenden Stack absichern
