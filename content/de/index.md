---
title: Einführung
description: Hinata ist ein quelloffener Tracker für Projekte und Vorgänge, den du selbst hostest, ohne Limits bei Nutzern, Teams oder Boards.
---

# Hinata

Hinata ist ein quelloffener Tracker für Projekte und Vorgänge auf deinem eigenen Server. Eine veröffentlichte App verbindet sich mit deinem Server und übernimmt zur Laufzeit Name und Logo deiner Organisation.

- Lizenz: **GPL-3.0**
- Aktuelle Version: **{{version}}**
- Keine Limits bei Nutzern, Teams oder Boards

!!! tip "Zwei Wege hinein"
    Neu hier? Mit dem [Schnellstart](/de/quick-start.html) läuft ein Stack in drei Befehlen. Für den echten Betrieb geht es zum [Self-Hosting](/de/self-hosting.html).


![Hinata-Dashboard](/assets/img/shot-dashboard.png)
*Das Dashboard mit Tagesfokus, Sprintfortschritt und Teamleistung.*

## Was ist Hinata?

Alles für agiles Projektmanagement: Projekte und Teams, Vorgänge mit Hierarchie (Epic → Story → Sub-task), Boards, Sprints, eine Timeline im Gantt-Stil, Zeiterfassung, Berichte und eine Wissensdatenbank im Stil von Confluence. Es läuft für ein Team auf einem Server oder hinter einem Reverse Proxy für eine ganze Organisation.

Das unterscheidet Hinata von den meisten selbst gehosteten Trackern:

- **Eine echte App für jede Plattform.** Eine Flutter-Codebasis für sechs Plattformen, mit Änderungen live über Server-Sent Events, offlinefreundlicher Navigation und ⌘K-Befehlspalette.
- **Dein eigener Server.** Die App hat keinen eingebauten Server. Du trägst einen oder mehrere Server ein und wechselst zwischen ihnen. Das Branding kommt zur Laufzeit vom Server. Oder du veröffentlichst einen eigenen Client mit eigener Package-ID, eigenem Namen, eigenen Icons und eigener Akzentfarbe.

!!! info "Designsprache"
    Navyblaue Navigationsleiste, warme Arbeitsfläche in Papieroptik und ein honigbernsteinfarbener Akzent (`#D9A032`), der hell und dunkel gleich wirkt. Liquid Glass gibt es in der mobilen Navigation, der ⌘K-Palette und der Lightbox für Anhänge.

## Für wen es ist

- **Self-Hoster und datenschutzbewusste Teams:** Daten auf eigener Hardware, Copyleft-Lizenz, keine Preise pro Sitzplatz.
- **Agenturen und Produktstudios:** ein Tracker unter eigener Marke für die eigenen Kunden.
- **Betreiber und Plattformteams:** MongoDB-Replikatsets, S3-Objektspeicher, SMTP, SSO, Rate Limiting und ein geprüftes Sicherheitsmodell.
- **Entwickler:** eine gut dokumentierte Codebasis (Spring Boot 4 + Flutter) zum Lesen, Erweitern und Mitmachen.

## Die zwei Repositories

| Repository | Was es ist | Stack |
| --- | --- | --- |
| [hinata-server](https://github.com/hinata-platform/hinata-server) | Backend-API, Geschäftslogik und Datenschicht. Veröffentlicht ein Docker-Image auf GHCR. | Spring Boot 4, Java 21, MongoDB (Replica Set), S3/MinIO, SMTP |
| [hinata-app](https://github.com/hinata-platform/hinata-app) | Der Client für jede Plattform, aus einer Codebasis. | Flutter, bloc/cubit, go_router, dio, i18next (en + de), fl_chart |

Die App spricht mit dem Server über eine versionierte REST-API unter `/api/v1`. Mehr dazu unter [Architektur](/de/architecture.html).

## Plattformen

Eine Flutter-Codebasis, sechs Ziele. Details stehen unter [Die Apps](/de/clients.html).

- **Android:** Smartphones und Tablets, App Links für `https://track.example.com`.
- **iOS:** iPhone und iPad, Universal Links über Associated Domains.
- **Web:** vollständiger Webbuild, ausgeliefert vom Webcontainer.
- **macOS:** native App für den Desktop.
- **Windows:** native App für den Desktop, als MSIX im Microsoft Store, Push über die Windows Push Notification Services (WNS).
- **Linux:** native App mit GTK 3 (Application-ID `com.ahmadre.hinata`), installiert mit `snap install hinata` aus dem [Snap Store](https://snapcraft.io/hinata) als strikt isoliertes Snap für amd64 und arm64. Rezepte für Flatpak und AppImage liegen im Repository. Die zwei Berechtigungen, die du bei Snap verbindest, erklärt [Die Apps](/de/clients.html#hinata-unter-linux). Ein `hinata://`-Link (SSO-Rücksprung, Einladung, Passwort-Reset) landet im offenen Fenster, weil die App den Scheme-Handler registriert und als Einzelinstanz läuft.

!!! note "Was unter Linux anders läuft"
    Es gibt keinen Push-Dienst für den Desktop. Benachrichtigungen kommen in der App und per E-Mail statt als Systembanner. Deine Benachrichtigungseinstellungen gelten weiter für dein Handy.

    Es gibt keine Kameraaufnahme, der Composer bietet „Foto aufnehmen“ nicht an. Vorhandene Fotos und andere Dateien hängst du normal an.

    Angemeldet bleiben braucht einen Schlüsselbund (GNOME Keyring, KWallet oder alles, was den Secret Service spricht). Fehlt er, sagt die App das, und die Sitzung endet beim Schließen des Fensters.

## Was drinsteckt

Jeder Bereich hat eine eigene Seite:

- **[Projekte & Teams](/de/projects-teams.html):** Workflows und Schlüssel pro Projekt (wie `ASTA-42`), wiederverwendbare farbige Labels und Teams, deren Projektzugriff pro Mitglied steuert, was jemand sieht.
- **[Vorgänge & Hierarchie](/de/issues.html):** Typen, Prioritäten, Tags, Kommentare, Anhänge, Abhängigkeiten und drei Ebenen wie in Jira: **Epic → Story/Task/Bug/Feature → Sub-task**.
- **[Boards & Sprints](/de/boards-sprints.html):** Spalten pro Workflowstatus, WIP-Limits, Backlog, der Umschalter Board / Backlog / Timeline und Sprintplanung mit Burndown.
- **[Gantt & Zeiterfassung](/de/timeline.html):** Timeline mit Start- und Fälligkeitsdaten und Abhängigkeiten, Arbeitseinträge mit Aktivitätstypen und Wochenzeitnachweisen.
- **[Berichte & Dashboard](/de/reports.html):** Burndown, Velocity, Cycle Time, Verteilungen und Erstellt vs. Gelöst, als PDF exportierbar, dazu ein Dashboard für deinen Fokus.
- **[Wissensdatenbank](/de/knowledge-base.html):** Markdown-Artikel in einer Hierarchie, global oder pro Projekt, mit Smart Links auf echte Vorgänge und Personen.
- **[Benachrichtigungen](/de/notifications.html):** in der App, per E-Mail und als Push über das Hinata Connect Gateway.
- **[Suche & Palette](/de/search.html):** ⌘K-Befehlspalette in Liquid Glass mit Triggern, Verlauf und responsivem Sheet.
- **[Git-Integration](/de/git-integration.html):** GitHub, GitLab oder Bitbucket anbinden, für Entwicklungsinfos, Smart Commits und Automatisierung im Workflow.
- **[Single Sign-on](/de/sso.html):** OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP, zur Laufzeit konfiguriert, ohne Neustart.

Den ganzen Rundgang gibt es in der [Feature-Tour](/de/features.html).

## Warum Hinata selbst hosten

- **Deine Daten.** Server, Daten und Marke gehören dir. Alles liegt in deiner MongoDB und deinem S3-Bucket. Anhänge nutzen zufällige Objektschlüssel und presignte Downloads.
- **Offen und ohne Paywall.** GPL-3.0, keine Limits pro Sitzplatz, keine Funktionen hinter einer Bezahlschranke. Von SSO bis Push läuft alles, ohne deine Daten an Dritte zu geben.
- **Kein Firebase nötig.** Push und Universal Links laufen über das [Hinata Connect Gateway](/de/connect-gateway.html). So bedient eine veröffentlichte App viele Server, und du brauchst kein eigenes Firebase-Projekt.
- **Konfiguration zur Laufzeit.** SSO, E-Mail-Ingest, Push und OAuth-Apps für Git liegen in MongoDB und werden im Adminbereich verwaltet. Die Datenbank hat Vorrang vor der Umgebung, Änderungen greifen **ohne Neustart**.
- **Sicherheit.** Stateless JWT (HS512), BCrypt für Passwörter, Login-Sperre in der Datenbank, Rate Limiting pro IP und gehärtete HTTP-Header, abgebildet auf die OWASP Top 10. Mehr im [Sicherheitsmodell](/de/security.html).

## Loslegen

<div class="cta-row">

Zwei Wege, je nachdem, was du als Nächstes brauchst:

</div>

- **[Loslegen →](/de/quick-start.html)** Server und App in drei Befehlen mit Docker Compose.
- **[Selbst hosten →](/de/self-hosting.html)** Der Weg in die Produktion: Deployment, Konfiguration, Datenbank, Speicher, Mail und Reverse Proxy.

!!! tip "Erst verstehen, wie alles zusammenhängt?"
    Die [Architektur](/de/architecture.html) zeigt den Datenfluss. Die [Grundkonzepte](/de/concepts.html) erklären die Begriffe: Organisationen, Projekte, Vorgänge, Sprints, Teams und mehr.
