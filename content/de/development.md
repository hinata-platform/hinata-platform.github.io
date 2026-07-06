---
title: Entwicklung
description: Richte eine lokale Entwicklungsumgebung für den Hinata-Server (Spring Boot / Java 21) und die App (Flutter) ein, führe Tests aus und verstehe die Projektstruktur und CI.
---

# Entwicklung

Diese Seite bringt dich von einem frischen Clone zu einem laufenden Server und
einer laufenden App auf deiner eigenen Maschine. Hinata besteht aus zwei
Repositories — einem **Spring-Boot**-Server und einem **Flutter**-Client — und jedes
hat eine kurze, vorhersehbare Dev-Schleife. Arbeite zuerst den Server durch (er ist
das, womit die App spricht), dann die App.

- **Server**: [`github.com/hinata-platform/hinata-server`](https://github.com/hinata-platform/hinata-server)
- **App**: [`github.com/hinata-platform/hinata-app`](https://github.com/hinata-platform/hinata-app)

## Server (Spring Boot, Java 21)

### Voraussetzungen

- **JDK 21** (die CI nutzt Temurin).
- **Docker** mit Compose für die lokale Infrastruktur.
- Kein globales Gradle nötig — das Repo liefert den Gradle Wrapper (`./gradlew`).

### 1. Die Infrastruktur starten

Eine eigene Compose-Datei bringt nur die Backing-Services hoch, die der Server
braucht — ein MongoDB-Replica-Set, Mailpit (ein lokaler SMTP-Catcher) und MinIO
(S3-kompatibler Speicher) — sodass du den Server selbst aus deiner IDE oder dem
Wrapper ausführen kannst:

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
```

| Dienst | URL | Was es ist |
| --- | --- | --- |
| **Mailpit** | `http://localhost:8025` | Fängt alle ausgehenden Mails ab — öffne es, um Verifizierungs-/Reset-/Benachrichtigungs-E-Mails zu lesen. |
| **MinIO-Konsole** | `http://localhost:9001` | Durchsuche den Objektspeicher-Bucket, der Anhänge und Avatare hält. |
| **MongoDB** | `localhost:27017` | Replica Set `rs0`, erreicht mit `directConnection=true`. |

### 2. Den Server ausführen

Richte den Server auf das lokale Mongo und MinIO aus und starte ihn mit dem
Wrapper:

```bash
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

!!! tip "Einen realistischen Demo-Workspace seeden"
    Füge `HINATA_DEMO_SEED=true` hinzu, um einen vollständigen englischen
    Demo-Workspace zu befüllen (Projekte, Vorgänge, Sprints, eine
    Wissensdatenbank), sodass du etwas zum Durchklicken hast. Es schließt außerdem
    das Erststart-Setup ab und meldet sich als `rebar` / `hinata-demo-2026` an. Der
    Seeder ist mit `@Profile("!prod")` annotiert und wird daher aus Produktions-
    Builds vollständig herauskompiliert — er ist eine reine Dev-Bequemlichkeit.

### 3. Die Tests ausführen

Die Quality Gate ist ein einziger Befehl — derselbe, den die CI ausführt:

```bash
./gradlew build
```

!!! info "Dev- vs. Prod-Profile"
    Die lokale Entwicklung nutzt das `dev`-Spring-Profil (Standalone-Mongo). Die
    Produktion nutzt `prod` (ein TLS-+-X.509-Replica-Set). Du brauchst das
    Prod-Profil auf deiner Maschine so gut wie nie; siehe
    [MongoDB & X.509](/de/database.html), falls du es reproduzieren willst.

## App (Flutter)

### Voraussetzungen

- Die **Flutter-Toolchain** (Stable-Channel — derselbe Channel, mit dem die CI
  baut). Führe `flutter doctor` aus und behebe alles, was es für deine
  Zielplattformen anmerkt.
- Plattform-SDKs nur für die Ziele, die du baust: Android Studio / SDK für Android,
  Xcode für iOS und macOS. Web braucht nichts Zusätzliches.

### Ausführen

```bash
flutter pub get
flutter run
```

`flutter run` zielt auf das jeweils verbundene Gerät. Um ein Ziel explizit zu
wählen:

```bash
flutter run -d chrome    # Web
flutter run -d macos     # macOS-Desktop
flutter devices          # angeschlossene Geräte/Emulatoren auflisten
```

Beim ersten Start fragt die App nach deiner **Server-URL**. Richte sie auf deinen
lokalen Server:

- Desktop / Web / iOS-Simulator: `http://localhost:8080`
- Android-Emulator: `http://10.0.2.2:8080` (der Alias des Emulators für deinen Host)

### Quality Gate

Dieselben Checks, die die CI ausführt, lokal:

```bash
flutter analyze && flutter test
```

### Internationalisierung (i18n)

Hinata ist mehrsprachig, und **jede für den Benutzer sichtbare Zeichenkette muss
übersetzt werden** — die App wird mit Englisch und Deutsch ausgeliefert. Die
Zeichenketten liegen als i18next-JSON unter `assets/i18n/{en,de}/` und werden über
die Lokalisierungsschicht gelesen (niemals fest in einem Widget verdrahtet).

!!! warning "Jede neue Zeichenkette braucht en + de"
    Wenn du UI-Text hinzufügst, füge den Key sowohl zu `assets/i18n/en/` **als
    auch** zu `assets/i18n/de/` hinzu und löse ihn über die Übersetzungsfunktion
    auf. Ein fehlender Key rendert stillschweigend die rohe Key-Zeichenkette. Das
    ist eine harte Anforderung für jeden PR, der die UI berührt — siehe
    [Mitwirken](/de/contributing.html).

## Projektstruktur

Die App folgt einer **feature-first**-Struktur. Jedes Feature besitzt seine Screens
und seinen State; gemeinsame Infrastruktur liegt unter `core/`. Daten fließen in
eine Richtung:

```text
Features (Screens/Widgets)
    │
    ▼
Bloc / Cubit            State-Management
    │
    ▼
HinataRepository        domänennaher Datenzugriff
    │
    ▼
ApiClient (dio)         REST /api/v1, Token-Refresh, Accept-Language
    │
    ▼
Hinata-Server           Spring Boot, /api/v1  ──SSE──▶ zurück zum Bloc
```

```text
lib/
  core/        theme, responsive system, i18n, api, models, blocs,
               router, storage, widgets
  features/    connect, setup, onboarding, auth, shell, dashboard,
               projects, issues, board, sprint, gantt, timesheet,
               reports, knowledge, search, notifications, settings, admin
packages/
  liquid_glass_widgets/   vendored glass surfaces (full control)
```

Ein Screen spricht niemals direkt mit `dio`: Er dispatcht an einen **Bloc/Cubit**,
der eine Methode auf **`HinataRepository`** aufruft, das den **`ApiClient`** nutzt.
Dieser eine Client ist der Ort, an dem das Bearer-Token, der automatische Refresh
und der `Accept-Language`-Header einmal für die ganze App behandelt werden.
Live-Änderungen kommen über **SSE** zurück und aktualisieren den relevanten Bloc.

## CI/CD

Beide Repositories verwenden **GitHub Actions**.

- **Server** (`ci.yml`): Bei jedem Push und Pull Request wird `./gradlew build`
  ausgeführt. Bei Pushes auf `main` und bei Versions-Tags (`v*`) baut und
  **veröffentlicht es ein Docker-Image in der GitHub Container Registry (GHCR)**
  unter `ghcr.io/hinata-platform`, getaggt mit `latest` auf `main` und mit der
  semantischen Version bei Tags.
- **App** (`ci.yml`): Bei jedem Push und Pull Request werden `flutter analyze` und
  `flutter test` ausgeführt und das Web-Release gebaut. Bei Pushes auf `main` und
  `v*`-Tags veröffentlicht es das kompilierte Flutter-**Web**-Image in GHCR. Ein
  separater Release-Workflow kümmert sich um die Store-Builds für die Mobil-Apps.

!!! note "Die Image-Tags, die du deployst"
    Betreiber ziehen diese GHCR-Images per Tag — `HINATA_SERVER_TAG` und
    `HINATA_APP_TAG` in der Deployment-`.env` (Standard `latest`). Siehe
    [Produktiv-Deployment](/de/deployment.html).

## Wie es weitergeht

- [Mitwirken](/de/contributing.html) — Konventionen, i18n-Regeln, Commit-Stil und wie du einen PR öffnest.
- [API-Referenz](/de/api.html) — die REST-Oberfläche und wie du die Scalar-Doku-UI lokal aktivierst.
- [Architektur](/de/architecture.html) — wie App, Server und Infrastruktur zusammenpassen.
- [Konfigurationsreferenz](/de/configuration.html) — jede Umgebungsvariable.
