---
title: Entwicklung
description: Richte Server (Spring Boot, Java 21) und App (Flutter) lokal ein, führe Tests aus und lerne Struktur und CI kennen.
---

# Entwicklung

So bringst du Server und App auf deinem Rechner zum Laufen. Hinata besteht aus
zwei Repositories. Richte zuerst den Server ein, denn mit ihm spricht die App.

- **Server**: [`github.com/hinata-platform/hinata-server`](https://github.com/hinata-platform/hinata-server)
- **App**: [`github.com/hinata-platform/hinata-app`](https://github.com/hinata-platform/hinata-app)

## Server (Spring Boot, Java 21)

### Voraussetzungen

- **JDK 21** (die CI nutzt Temurin).
- **Docker** mit Compose für die lokale Infrastruktur.
- Kein globales Gradle. Das Repo bringt den Gradle Wrapper mit (`./gradlew`).

### 1. Die Infrastruktur starten

Eine eigene Compose-Datei startet nur die Dienste, die der Server braucht: ein
MongoDB Replica Set, Mailpit (fängt lokal SMTP ab) und MinIO (S3-kompatibler
Speicher). Den Server selbst startest du aus der IDE oder mit dem Wrapper.

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
```

| Dienst | URL | Was es ist |
| --- | --- | --- |
| **Mailpit** | `http://localhost:8025` | Fängt alle ausgehenden Mails ab. Hier liest du Mails zu Verifizierung, Passwort-Reset und Benachrichtigungen. |
| **MinIO-Konsole** | `http://localhost:9001` | Zeigt den Bucket mit Anhängen und Avataren. |
| **MongoDB** | `localhost:27017` | Replica Set `rs0`, erreichbar mit `directConnection=true`. |

### 2. Den Server ausführen

Verbinde den Server mit dem lokalen Mongo und MinIO und starte ihn:

```bash
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

!!! tip "Einen realistischen Demo-Workspace seeden"
    Mit `HINATA_DEMO_SEED=true` bekommst du einen englischen Demo-Workspace mit
    Projekten, Vorgängen, Sprints und Wissensdatenbank. Das Erststart-Setup ist
    dann erledigt, und du bist als `rebar` / `hinata-demo-2026` angemeldet. Der
    Seeder hat `@Profile("!prod")` und fehlt in Produktionsbuilds komplett.

### 3. Die Tests ausführen

Ein Befehl, derselbe wie in der CI:

```bash
./gradlew build
```

!!! info "Dev- vs. Prod-Profile"
    Lokal läuft das Spring-Profil `dev` (Mongo standalone). Produktion nutzt
    `prod` (Replica Set mit TLS und X.509). Das brauchst du lokal so gut wie nie.
    Falls doch, siehe [MongoDB & X.509](/de/database.html).

## App (Flutter)

### Voraussetzungen

- Die **Flutter-Toolchain** im Stable Channel, wie in der CI. Führe
  `flutter doctor` aus und behebe, was es für deine Zielplattformen meldet.
- SDKs brauchst du nur für die Plattformen, die du baust.
- **Android:** Android Studio / SDK.
- **iOS und macOS:** Xcode.
- **Windows:** Visual Studio mit dem Workload *Desktopentwicklung mit C++*.
- **Web:** nichts extra.

### Ausführen

```bash
flutter pub get
flutter run
```

`flutter run` nimmt das verbundene Gerät. Ein Ziel wählst du so:

```bash
flutter run -d chrome    # Web
flutter run -d macos     # macOS-Desktop
flutter run -d windows   # Windows-Desktop
flutter devices          # angeschlossene Geräte/Emulatoren auflisten
```

Beim ersten Start fragt die App nach der **Server-URL**. Nimm deinen lokalen Server:

- Desktop / Web / iOS-Simulator: `http://localhost:8080`
- Android-Emulator: `http://10.0.2.2:8080` (so erreicht der Emulator deinen Host)

### Quality Gate

Dieselben Checks wie in der CI:

```bash
flutter analyze && flutter test
```

### Internationalisierung (i18n)

**Jeder sichtbare Text muss übersetzt sein.** Die App gibt es auf Englisch und
Deutsch. Die Texte liegen als i18next-JSON unter `assets/i18n/{en,de}/` und
werden über die Lokalisierungsschicht gelesen, nie fest im Widget.

!!! warning "Jede neue Zeichenkette braucht en + de"
    Neuer UI-Text braucht den Key in `assets/i18n/en/` **und** in
    `assets/i18n/de/`. Lös ihn über die Übersetzungsfunktion auf. Fehlt ein Key,
    zeigt die App ohne Warnung den rohen Key an. Für jeden PR mit UI-Änderungen
    ist das Pflicht, siehe [Mitwirken](/de/contributing.html).

## Projektstruktur

Die App ist **nach Features** gegliedert. Jedes Feature hat eigene Screens und
eigenen State. Gemeinsames liegt unter `core/`. Daten fließen in eine Richtung:

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

Ein Screen spricht nie direkt mit `dio`:

1. Der Screen schickt ein Event an einen **Bloc/Cubit**.
2. Der Bloc ruft eine Methode in **`HinataRepository`** auf.
3. Das Repository nutzt den **`ApiClient`**.

Nur der `ApiClient` kümmert sich um Bearer-Token, automatischen Refresh und den
`Accept-Language`-Header. Live-Änderungen kommen per **SSE** zurück und
aktualisieren den passenden Bloc.

## CI/CD

Beide Repositories nutzen **GitHub Actions**.

**Server** (`ci.yml`):

- Bei jedem Push und Pull Request läuft `./gradlew build`.
- Bei Pushes auf `main` und Versionstags (`v*`) wird ein **Docker-Image in der
  GitHub Container Registry (GHCR)** unter `ghcr.io/hinata-platform`
  veröffentlicht. Tag `latest` auf `main`, die semantische Version bei Tags.

**App** (`ci.yml`):

- Bei jedem Push und Pull Request laufen `flutter analyze` und `flutter test`,
  und das Web-Release wird gebaut.
- Bei Pushes auf `main` und `v*`-Tags landet das Flutter-**Web**-Image in GHCR.
- Ein eigener Release-Workflow baut die Mobil-Apps für die Stores.

!!! note "Die Image-Tags, die du deployst"
    Betreiber ziehen die GHCR-Images per Tag über `HINATA_SERVER_TAG` und
    `HINATA_APP_TAG` in der `.env` (Standard `latest`). Siehe
    [Produktiv-Deployment](/de/deployment.html).

## Wie es weitergeht

- [Mitwirken](/de/contributing.html): Konventionen, i18n-Regeln, Commit-Stil und PRs.
- [API-Referenz](/de/api.html): die REST-API und wie du die Scalar-Doku lokal aktivierst.
- [Architektur](/de/architecture.html): wie App, Server und Infrastruktur zusammenpassen.
- [Konfigurationsreferenz](/de/configuration.html): jede Umgebungsvariable.
