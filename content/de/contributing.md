---
title: Mitwirken
description: Wie du zu Hinata beitragen kannst — die beiden Repositories, Coding-Konventionen, die i18n-Anforderung, der Commit-Stil und wie du Probleme meldest oder einen Pull Request öffnest.
---

# Mitwirken

Hinata ist **Open Source unter der GPL-3.0-Lizenz**, und Beiträge sind sehr
willkommen — Fehlerberichte, Übersetzungen, Doku und Code bringen das Projekt alle
voran. Diese Seite erklärt, wo der Code liegt, wie du dich einrichtest, und die
Konventionen, die Pull Requests leicht überprüf- und mergebar halten.

Du musst kein Experte sein, um zu helfen. Ein klarer Fehlerbericht, das Beheben
eines Tippfehlers oder eine kleine Verbesserung an einer deutschen Zeichenkette ist
ein wirklich nützlicher Beitrag.

## Die beiden Repositories

Hinata ist in einen Server und einen Client aufgeteilt, jeder mit eigenem
Issue-Tracker und eigenen Pull Requests:

| Repository | Was es ist | Link |
| --- | --- | --- |
| **hinata-server** | Spring Boot 4 / Java 21 REST-API, MongoDB, S3/MinIO, SMTP. | [github.com/hinata-platform/hinata-server](https://github.com/hinata-platform/hinata-server) |
| **hinata-app** | Der Flutter-Client — Android, iOS, Web, macOS aus einer Codebasis. | [github.com/hinata-platform/hinata-app](https://github.com/hinata-platform/hinata-app) |

Öffne dein Issue oder deinen Pull Request gegen das Repository, dem der Code
gehört, den du änderst. Eine Änderung, die beide betrifft (ein neuer Endpunkt plus
seine UI), sind zwei koordinierte PRs — erwähne jeden im jeweils anderen, damit ein
Reviewer dem Faden folgen kann.

## Einrichtung

Der schnellste Weg zu einer laufenden Dev-Umgebung ist die Seite
[Entwicklung](/de/development.html) — sie behandelt JDK 21 und die
Compose-Infrastruktur für den Server sowie die Flutter-Toolchain für die App, plus
die genauen Befehle. Kurz gesagt:

```bash
# Server
docker compose -f docker-compose.dev.yml up -d
./mvnw spring-boot:run

# App
flutter pub get
flutter run
```

Bevor du einen PR öffnest, stelle sicher, dass die Quality Gates lokal durchlaufen
— es sind dieselben Checks, die die CI ausführt:

```bash
./mvnw verify              # Server
flutter analyze && flutter test   # App
```

## Coding-Konventionen

- **Passe dich dem umgebenden Code an.** Folge dem Stil, der bereits in der Datei
  vorhanden ist, die du bearbeitest; formatiere keine unbeteiligten Zeilen neu.
- **Server** — idiomatisches Spring Boot: Controller bleiben schlank,
  Geschäftsregeln leben in Services, Datenzugriff in Repositories. Halte
  Autorisierungsprüfungen und lokalisierte Fehler-Keys dort, wo der bestehende Code
  sie ablegt.
- **App** — der feature-first, unidirektionale Fluss, der in
  [Entwicklung](/de/development.html) beschrieben ist: Screens dispatchen an einen
  **Bloc/Cubit**, der **`HinataRepository`** aufruft, das den **`ApiClient`** nutzt.
  Rufe `dio` niemals aus einem Widget auf.
- **Icons** — die App verwendet **ausschließlich Lucide-Icons**
  (`lucide_icons_flutter`), niemals Material- oder Cupertino-Icon-Sets.
- **Halte Änderungen fokussiert.** Eine logische Änderung pro PR lässt sich weit
  leichter überprüfen als ein großer gemischter Diff.

### Die i18n-Anforderung (nicht verhandelbar)

Die App ist mehrsprachig und wird mit **Englisch und Deutsch** ausgeliefert. Jede
für den Benutzer sichtbare Zeichenkette muss als Key in **beiden** Sprachen
existieren und über die Lokalisierungsschicht aufgelöst werden — niemals fest in
einem Widget verdrahtet.

!!! warning "Jede neue UI-Zeichenkette braucht einen en- + de-Key"
    Wenn du Text hinzufügst, füge den Key sowohl zu `assets/i18n/en/` **als auch**
    zu `assets/i18n/de/` hinzu und rendere ihn über die Übersetzungsfunktion. Ein
    PR, der eine nackte Zeichenkette einführt oder einen englischen Key ohne sein
    deutsches Gegenstück hinzufügt, wird zur Korrektur zurückgeschickt. Ein
    fehlender Key rendert den Benutzern stillschweigend den rohen Key-Namen.

Wenn du kein Deutsch sprichst, füge trotzdem den deutschen Key hinzu — eine
Best-Effort-Übersetzung, die ein Reviewer oder ein Muttersprachler verfeinern kann,
ist weit besser als ein fehlender Key. Siehe
[Entwicklung → Internationalisierung](/de/development.html).

## Commit- und Pull-Request-Stil

- Schreibe Commit-Nachrichten im Imperativ und beschreibe die Änderung in
  **neutralen, produkteigenen Begriffen** — beschreibe, *was das Feature tut*, z. B.
  „add issue linking“, statt die UI eines anderen Produkts zu benennen.
- Halte die Betreffzeile kurz; nutze den Text, um das *Warum* zu erklären, wenn es
  nicht offensichtlich ist.
- Sage in der PR-Beschreibung, was sich geändert hat und warum, und wie du es
  verifiziert hast. Verlinke das Issue, das es behandelt. Wenn die Änderung in der
  UI sichtbar ist, hilft ein Screenshot sehr.
- Stelle sicher, dass die CI grün ist (Build, Analyze, Tests), bevor du um Review
  bittest.

## Probleme melden

Ein guter Fehlerbericht spart allen Zeit. Wenn du ein Issue öffnest, gib an:

- **Was du erwartet hast** und **was tatsächlich passiert ist**.
- **Schritte zur Reproduktion** — je kleiner und präziser, desto besser.
- **Umgebung** — Server-Image-Tag / App-Version, Plattform (Android, iOS, Web,
  macOS) und alles Relevante zu deinem Deployment (Reverse Proxy, SSO-Provider).
- Relevante **Logs oder Fehlermeldungen** — aber **schwärze Secrets** (Tokens,
  Passwörter, Connection-Strings), bevor du einfügst.

Prüfe zuerst die [FAQ & Fehlerbehebung](/de/faq.html) — viele „Bugs“ sind
Konfigurationsprobleme mit bekannter Lösung (CORS, Proxy-Buffering, Mail-Relay,
Trusted Proxies).

!!! danger "Niemals Secrets in ein öffentliches Issue aufnehmen"
    Füge keine echten JWT-Secrets, Datenbank-Passwörter, OAuth-Client-Secrets oder
    Access-Tokens in ein Issue, einen PR oder einen Screenshot ein. Wenn ein Secret
    offengelegt wurde, rotiere es.

## Lizenz

Mit deinem Beitrag stimmst du zu, dass deine Beiträge unter der **GPL-3.0**-Lizenz
des Projekts lizenziert sind, denselben Bedingungen wie der Rest von Hinata. Siehe
die Datei `LICENSE` in jedem Repository.

## Wie es weitergeht

- [Entwicklung](/de/development.html) — vollständiges lokales Setup, Projektstruktur und CI.
- [API-Referenz](/de/api.html) — die REST-Oberfläche, die du möglicherweise erweiterst.
- [FAQ & Fehlerbehebung](/de/faq.html) — häufige Probleme und ihre Lösungen.
