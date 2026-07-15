---
title: Einführung
description: Hinata ist ein quelloffener, selbst-gehosteter Projekt- und Issue-Tracker mit einer veröffentlichten Client-App für deinen eigenen Server — ohne Nutzer-, Team- oder Board-Limits. Lerne die Plattform kennen.
---

# Hinata

Hinata ist ein **unabhängiger, quelloffener, selbst-gehosteter Projekt- und Issue-Tracker** — eine moderne Alternative zu gehosteten Trackern, die du vollständig auf deiner eigenen Infrastruktur betreibst. Es folgt dem Modell **eine App, selbst gehostete Server**: Betreiber hosten ihre eigene Server-Instanz, und die eine veröffentlichte Client-App verbindet sich mit ihr — Name und Logo deiner Organisation werden zur Laufzeit übernommen. Lizenziert unter **GPL-3.0**, aktuelle Plattformversion **{{version}}**.

Keine Nutzer-Limits. Keine Team-Limits. Keine Board-Limits. Niemals. Was du selbst hostest, gehört dir.

!!! tip "Zwei Wege hinein"
    Neu hier? Spring direkt zum [Schnellstart](/de/quick-start.html) und bring in drei Befehlen einen Stack zum Laufen. Bereit für den echten Betrieb? Geh zum [Self-Hosting](/de/self-hosting.html) für den Produktivpfad.


![Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Das Hinata-Dashboard — Tagesfokus, aktiver Sprint-Fortschritt und Team-Leistung.*

## Was ist Hinata?

Hinata ist eine vollständige agile Projektmanagement-Suite: Projekte und Teams, Vorgänge mit einer echten Epic → Story → Sub-task-Hierarchie, agile Boards, Sprints, eine Gantt-Timeline, Zeiterfassung, Berichte und eine Confluence-artige Wissensdatenbank. Es ist darauf ausgelegt, sich modern und schnell anzufühlen — betreibbar von einem einzigen Team auf einem einzigen Server oder skaliert hinter einem Reverse Proxy für eine ganze Organisation.

Zwei Dinge unterscheiden es von den meisten selbst-gehosteten Trackern:

- **Es liefert eine echte plattformübergreifende App.** Nicht nur eine Web-Oberfläche — eine einzige Flutter-Codebasis, kompiliert für Android, iOS, Web und macOS, mit Live-Updates über Server-Sent Events, offline-freundlicher Navigation und einer ⌘K-Befehlspalette.
- **Du bringst deinen eigenen Server mit.** Der Client hat keinen fest eingebauten Backend-Server. Du lässt die veröffentlichte App auf deinen eigenen Server zeigen, speicherst mehrere Server und wechselst zwischen ihnen, und das Branding kommt zur Laufzeit von deinem Server — oder du baust und veröffentlichst deinen eigenen Client mit eigener Package-ID, eigenem Namen, Icons und Akzentfarbe.

!!! info "Designsprache"
    Hinata trägt eine navyblaue Navigationsleiste, eine warme Papier-Arbeitsfläche und einen honig-bernsteinfarbenen Akzent (`#D9A032`), der in Hell und Dunkel gleich wirkt. Liquid-Glass-Oberflächen erscheinen auf der mobilen Navigation, der ⌘K-Palette und der Attachment-Lightbox. Es soll jeden Tag Freude machen, es anzusehen.

## Für wen es ist

- **Self-Hoster & datenschutzbewusste Teams**, die ihre Projektdaten auf selbst kontrollierter Hardware wollen, unter einer Copyleft-Lizenz, ohne sitzplatzbasierte Preise.
- **Agenturen und Produktstudios**, die einen gebrandeten Tracker an ihre eigenen Kunden ausliefern wollen — dieselbe Engine, deine Marke.
- **Betreiber & Plattform-Teams**, die echte Infrastruktur-Kontrollen brauchen: MongoDB-Replica-Sets, S3-Objektspeicher, SMTP, SSO, Rate-Limiting und ein geprüftes Sicherheitsmodell.
- **Entwickler**, die eine zugängliche, gut dokumentierte Codebasis (Spring Boot 4 + Flutter) schätzen, die sie lesen, erweitern und zu der sie beitragen können.

## Die zwei Repositories

Hinata ist in zwei quelloffene Repositories aufgeteilt:

| Repository | Was es ist | Stack |
| --- | --- | --- |
| [hinata-server](https://github.com/hinata-platform/hinata-server) | Die Backend-API, Geschäftslogik und Datenschicht. Veröffentlicht ein Docker-Image auf GHCR. | Spring Boot 4, Java 21, MongoDB (Replica Set), S3/MinIO, SMTP |
| [hinata-app](https://github.com/hinata-platform/hinata-app) | Der Client für jede Plattform, aus einer Codebasis. | Flutter, bloc/cubit, go_router, dio, i18next (en + de), fl_chart |

Die App spricht über eine versionierte REST-API unter `/api/v1` mit dem Server. Siehe [Architektur](/de/architecture.html), wie die Teile zusammenpassen.

## Plattformen

Eine Flutter-Codebasis, vier Ziele:

- **Android** — Smartphones und Tablets, App Links für `https://track.example.com`.
- **iOS** — iPhone und iPad, Universal Links über Associated Domains.
- **Web** — ein voll ausgestatteter Flutter-Web-Build, ausgeliefert vom Web-Container.
- **macOS** — ein nativer Desktop-Client.

## Was drinsteckt

Ein Rundgang durch die Plattform, jeweils mit einer vertiefenden Seite:

- **[Projekte & Teams](/de/projects-teams.html)** — projektspezifische Workflows und Issue-Keys (wie `ASTA-42`), wiederverwendbare farbige Labels und Teams, deren mitgliederbasierter Projektzugriff steuert, was jede Person überhaupt sehen kann.
- **[Vorgänge & Hierarchie](/de/issues.html)** — Typen, Prioritäten, Tags, Kommentare, Attachments und Abhängigkeiten, mit einer Jira-artigen dreistufigen Hierarchie: **Epic → Story/Task/Bug/Feature → Sub-task**.
- **[Boards & Sprints](/de/boards-sprints.html)** — agile Boards mit Spalten, die auf Workflow-Status abgebildet sind, WIP-Limits und einem Backlog, plus einem Board / Backlog / Timeline-Umschalter und vollständiger Sprint-Planung mit Burndown.
- **[Gantt & Zeiterfassung](/de/timeline.html)** — ein Timeline-Lesemodell mit Start-/Fälligkeitsdaten und Abhängigkeiten sowie Arbeitseinträge mit Aktivitätstypen und Wochenzeitnachweisen.
- **[Berichte & Dashboard](/de/reports.html)** — Burndown, Velocity, Cycle Time, Verteilungen und Erstellt-vs.-Gelöst, exportierbar als PDF, plus ein Fokus-Dashboard.
- **[Wissensdatenbank](/de/knowledge-base.html)** — hierarchische Markdown-Artikel, global oder pro Projekt, mit Smart Links, die echte Vorgänge und Personen auflösen.
- **[Benachrichtigungen](/de/notifications.html)** — In-App und E-Mail, plus Push über das Hinata Connect Gateway.
- **[Suche & Palette](/de/search.html)** — eine ⌘K Liquid-Glass-Befehlspalette mit Triggern, Verlauf und einem responsiven Sheet.
- **[Git-Integration](/de/git-integration.html)** — verbinde Projekte mit GitHub, GitLab oder Bitbucket für echte Entwicklungsinfos, Smart Commits und Workflow-Automatisierung.
- **[Single Sign-on](/de/sso.html)** — OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP, zur Laufzeit konfiguriert, ohne Neustart.

Willst du den vollständigen Rundgang? Lies die [Feature-Tour](/de/features.html).

## Warum Hinata selbst hosten

!!! note "Die Kurzfassung"
    Dir gehören der Server, die Daten und die Marke. Es ist GPL-3.0, bleibt also offen. Es gibt keine Sitzplatz-Limits oder hinter Paywalls versteckte Funktionen, und alles von SSO bis Push funktioniert, ohne deine Daten an Dritte zu geben.

- **Deine Daten, deine Regeln.** Alles liegt in deinem MongoDB und deinem S3-Bucket. Attachments verwenden zufällige Objekt-Keys und presignte Downloads.
- **Kein Firebase nötig.** Push-Benachrichtigungen und Universal Links werden über das [Hinata Connect Gateway](/de/connect-gateway.html) weitergeleitet, sodass eine einzige veröffentlichte App viele Server bedienen kann und Self-Hoster kein eigenes Firebase-Projekt brauchen.
- **Laufzeitkonfiguration.** SSO, E-Mail-Ingest, Push und Git-OAuth-Apps werden in MongoDB gespeichert und aus dem Adminbereich verwaltet — die Datenbank überschreibt die Umgebung, und Änderungen greifen **ohne Neustart**.
- **Ernst gemeinte Sicherheit.** Stateless JWT (HS512), BCrypt-Passwort-Hashing, datenbankgestützte Login-Sperre, Rate-Limiting pro IP, gehärtete HTTP-Header und ein Modell, das auf die OWASP Top 10 abgebildet ist. Siehe das [Sicherheitsmodell](/de/security.html).

## Loslegen

<div class="cta-row">

Zwei klare Pfade, je nachdem, was du als Nächstes brauchst:

</div>

- **[Loslegen →](/de/quick-start.html)** — der schnellste Weg zu einem laufenden Server und einer laufenden App, in drei Befehlen mit Docker Compose.
- **[Selbst hosten →](/de/self-hosting.html)** — der Produktivpfad: Deployment, Konfiguration, Datenbank, Speicher, Mail und Reverse Proxy.

!!! tip "Willst du erst die beweglichen Teile verstehen?"
    Lies die [Architektur](/de/architecture.html) für das Datenfluss-Bild und die [Grundkonzepte](/de/concepts.html) für das Vokabular — Organisationen, Projekte, Vorgänge, Sprints, Teams und mehr.
