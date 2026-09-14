---
title: Mitwirken
description: Wie du zu Hinata beiträgst, mit Repositories, Konventionen, Übersetzungen, Commits und Fehlerberichten.
---

# Mitwirken

Hinata ist **Open Source unter der GPL-3.0-Lizenz**. Beiträge sind willkommen: Fehlerberichte, Übersetzungen, Doku und Code.

Du musst kein Experte sein. Ein klarer Fehlerbericht, ein behobener Tippfehler oder eine bessere deutsche Formulierung helfen schon.

## Die beiden Repositories

Server und Client haben jeweils eigene Issues und Pull Requests.

| Repository | Was es ist | Link |
| --- | --- | --- |
| **hinata-server** | Spring Boot 4 / Java 21 REST-API, MongoDB, S3/MinIO, SMTP. | [github.com/hinata-platform/hinata-server](https://github.com/hinata-platform/hinata-server) |
| **hinata-app** | Der Flutter-Client für Android, iOS, Web, macOS, Windows und Linux aus einer Codebasis. | [github.com/hinata-platform/hinata-app](https://github.com/hinata-platform/hinata-app) |

Öffne Issue oder PR in dem Repository, dem der geänderte Code gehört. Betrifft eine Änderung beide (etwa ein neuer Endpunkt plus UI), öffnest du zwei PRs und verlinkst sie gegenseitig.

## Einrichtung

Die vollständige Anleitung steht unter [Entwicklung](/de/development.html): JDK 21 und Compose für den Server, die Flutter-Toolchain für die App. Kurz:

```bash
# Server
docker compose -f docker-compose.dev.yml up -d
./gradlew bootRun

# App
flutter pub get
flutter run
```

Lass vor dem PR lokal dieselben Checks laufen wie die CI:

```bash
./gradlew build                   # Server
flutter analyze && flutter test   # App
```

## Konventionen

- **Passe dich dem umgebenden Code an.** Übernimm den Stil der Datei und formatiere keine unbeteiligten Zeilen um.
- **Server:** idiomatisches Spring Boot. Controller bleiben schlank, Geschäftsregeln gehören in Services, Datenzugriff in Repositories. Autorisierungsprüfungen und lokalisierte Fehler-Keys legst du dort ab, wo der bestehende Code sie hat.
- **App:** der nach Features gegliederte Datenfluss in eine Richtung aus [Entwicklung](/de/development.html). Screens rufen einen **Bloc/Cubit** auf, der ruft **`HinataRepository`** auf, und das nutzt den **`ApiClient`**. Rufe `dio` nie aus einem Widget auf.
- **Icons:** nur **Lucide-Icons** (`lucide_icons_flutter`), nie Material oder Cupertino.
- **Kleine PRs.** Eine logische Änderung pro PR lässt sich viel leichter prüfen als ein großer, gemischter Diff.

### Übersetzungen sind Pflicht

Die App gibt es auf **Englisch und Deutsch**. Jeder sichtbare Text braucht einen Key in **beiden** Sprachen und läuft über die Lokalisierung. Fest in ein Widget geschriebener Text wird nicht angenommen.

!!! warning "Jeder neue Text braucht einen Key in en und de"
    Lege den Key in `assets/i18n/en/` **und** `assets/i18n/de/` an und rendere ihn über die Übersetzungsfunktion. PRs mit festem Text oder ohne deutschen Key gehen zur Korrektur zurück. Fehlt ein Key, sehen Nutzer den rohen Key-Namen.

Du sprichst kein Deutsch? Leg den deutschen Key trotzdem an. Eine grobe Übersetzung ist viel besser als ein fehlender Key, und jemand kann sie später verbessern. Siehe [Entwicklung → Internationalisierung](/de/development.html).

## Commits und Pull Requests

- Schreib Commit-Nachrichten im Imperativ und mit **neutralen Begriffen aus Hinata selbst**. Beschreibe, *was das Feature tut*, z. B. „add issue linking“. Nenne nicht die UI eines anderen Produkts.
- Halte die Betreffzeile kurz. Das *Warum* gehört in den Text, wenn es nicht offensichtlich ist.
- Die PR-Beschreibung sagt, was sich geändert hat, warum und wie du es geprüft hast. Verlinke das Issue. Bei sichtbaren Änderungen hilft ein Screenshot sehr.
- Bitte erst um Review, wenn die CI grün ist (Build, Analyze, Tests).

## Probleme melden

Ein gutes Issue enthält:

- **Was du erwartet hast** und **was tatsächlich passiert ist**.
- **Schritte zur Reproduktion**, so kurz und genau wie möglich.
- **Umgebung:** Server-Image-Tag bzw. App-Version, Plattform (Android, iOS, Web, macOS, Windows, Linux) und Wichtiges zum Deployment (Reverse Proxy, SSO-Provider).
- **Unter Linux zusätzlich:** Distribution, Desktopsitzung (GNOME oder Plasma, X11 oder Wayland) und wie du installiert hast (Snap, Flatpak, AppImage oder eigenes `flutter build linux`). Dateiauswahl, Schlüsselbund und Audiowerkzeuge kommen vom System. Diese Angaben sind daher oft schon der halbe Fehlerbericht.
- **Logs oder Fehlermeldungen**, aber **schwärze vorher Secrets** (Tokens, Passwörter, Connection-Strings).

Schau vorher in die [FAQ & Fehlerbehebung](/de/faq.html). Viele „Bugs“ sind bekannte Konfigurationsprobleme (CORS, Proxy-Buffering, Mail-Relay, Trusted Proxies).

!!! danger "Niemals Secrets in ein öffentliches Issue"
    Keine echten JWT-Secrets, Datenbankpasswörter, OAuth-Client-Secrets oder Access-Tokens in Issues, PRs oder Screenshots. Wurde ein Secret offengelegt, rotiere es.

## Lizenz

Mit deinem Beitrag stimmst du zu, dass er unter der **GPL-3.0** des Projekts steht, wie der Rest von Hinata. Details stehen in der Datei `LICENSE` jedes Repositorys.

## Wie es weitergeht

- [Entwicklung](/de/development.html): lokales Setup, Projektstruktur und CI.
- [API-Referenz](/de/api.html): die REST-Schnittstelle, die du vielleicht erweiterst.
- [FAQ & Fehlerbehebung](/de/faq.html): häufige Probleme und ihre Lösungen.
