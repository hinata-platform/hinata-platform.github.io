---
title: Projekte & Teams
description: Projekte gruppieren deine Arbeit unter einem Schlüssel wie ASTA-42; Teams gewähren Zugriff pro Mitglied und entscheiden, wer im gesamten Workspace was sieht.
---

# Projekte & Teams

Alles in Hinata lebt innerhalb eines **Projekts**, und wer ein Projekt sehen darf, entscheiden **Teams**. Zusammen geben sie dir eine saubere Trennung zwischen, sagen wir, einer mobilen App, einem Backend-Dienst und einer Initiative für interne Tools — jeweils mit eigenem Board, eigenem Workflow, eigenen Labels und eigener Vorgangs-Nummerierung, sichtbar nur für die Personen, die sie sehen sollen.


![Hinata Teams](/assets/img/shot-teams.png)
*Teams gewähren pro Mitglied Projektzugriff über den gesamten Workspace.*

## Projekte

Ein Projekt ist ein in sich geschlossener Workspace für ein Arbeitsvolumen. Jedes Projekt besitzt:

- **Einen Projektschlüssel** — ein kurzes Präfix in Großbuchstaben wie `HIN`, `MOB` oder `INF`. Jeder Vorgang im Projekt wird von diesem Schlüssel ausgehend nummeriert (`MOB-42`), und die Nummer wird nie wiederverwendet, sodass ein Schlüssel ein stabiler, überall einfügbarer Bezeichner ist.
- **Eigene Workflow-Status** — die Spalten, durch die Vorgänge wandern (z. B. *To Do → In Progress → In Review → Done*). Status sind pro Projekt, sodass ein Forschungsprojekt und ein Lieferprojekt Arbeit unterschiedlich abbilden können. Siehe [Projekteinstellungen](/de/project-settings.html).
- **Wiederverwendbare Labels** — farbige Tags (`frontend`, `needs-design`), die du einmal definierst und über jeden Vorgang im Projekt hinweg wiederverwendest.
- **Mitglieder** — die Personen, die im Projekt arbeiten, sichtbar in Zuweisungs-Auswahlen, Berichten und dem Personenfilter des Boards.
- **Git-Verbindungen** — ein oder mehrere verknüpfte Repositories (siehe [Git-Integration](/de/git-integration.html)).

!!! tip "Wähle Schlüssel, die du gern tippst"
    Schlüssel tauchen den ganzen Tag in Commit-Nachrichten, Branch-Namen und im Chat auf (`git commit -m "MOB-42 fix crash"`). Kurze, einprägsame Schlüssel zahlen sich aus.

### Ein Projekt erstellen

Öffne **Projekte → Neues Projekt**, gib ihm einen Namen und einen Schlüssel, und du bist startklar. Du kannst die Workflow-Status, Labels und Mitglieder jederzeit in den Projekteinstellungen anpassen, ohne bestehende Vorgänge zu stören — Umbenennungen werden sicher über das gesamte Projekt kaskadiert.

## Teams

Ein **Team** ist eine Gruppe von Personen mit Zugriff auf eine definierte Menge von Projekten. Teams sind das Rückgrat der Sichtbarkeit in Hinata: Ein Mitglied sieht immer nur die Projekte, die ihm sein Team gewährt. Jemand im *Mobile*-Team sieht das `MOB`-Projekt; `INF` sieht er nicht, es sei denn, ein Team gewährt es ebenfalls.

Diese Zugriffsprüfung läuft **workspace-weit** — sie steuert das Board, die Vorgangslisten, die Suchergebnisse, die Berichte und sogar die Benachrichtigungen. Es gibt keinen separaten „Teilen“-Schritt, den man vergessen könnte; die Mitgliedschaft *ist* die Berechtigung.

!!! info "Wie der Zugriff durchgesetzt wird"
    Die Projektsichtbarkeit wird auf dem Server für jede Anfrage ausgewertet (eine Zusicherung, dass der Aufrufer Mitglied des Projekts ist). Die App zeigt schlicht nie an, was der Server nicht zurückgibt, sodass der Zugriff nicht durch Herumstochern am Client umgangen werden kann.

### Rollen

- **Mitglieder** erledigen die alltägliche Arbeit: Vorgänge erstellen und bearbeiten, kommentieren, Zeit erfassen, Karten verschieben.
- **Admins** erreichen zusätzlich den [Admin-Bereich](/de/admin-area.html) — Benutzer, SSO, E-Mail-zu-Ticket, Git-OAuth-Apps und app-weite Einstellungen. Admin ist eine Workspace-Rolle (`ADMIN`), durchgesetzt an jedem `/api/v1/admin/**`-Endpunkt.

### Mitglieder verwalten

Füge Personen zu einem Team oder zu einem einzelnen Projekt hinzu oder entferne sie in den Team-/Projekteinstellungen. Änderungen greifen sofort — ein entferntes Mitglied verliert bei seiner nächsten Anfrage die Sichtbarkeit.

## Wie Projekte und Teams zusammenpassen

```text
Team "Mobile"  ──gewährt──▶  Projekt MOB  ──enthält──▶  Vorgänge MOB-1, MOB-2, …
Team "Platform"──gewährt──▶  Projekt INF  ──enthält──▶  Vorgänge INF-1, INF-2, …
        │                        ▲
        └────gewährt ebenfalls───┘   (ein Team kann mehrere Projekte gewähren)
```

Ein Benutzer kann mehreren Teams angehören und sieht daher mehrere Projekte; ein Projekt kann von mehreren Teams gewährt werden. Modelliere deine Organisation, wie du magst — nach Squad, nach Abteilung, nach Kunde — und die richtigen Personen sehen einfach die richtige Arbeit.

## Nächste Schritte

- Konfiguriere die Status und Labels eines Projekts in den [Projekteinstellungen](/de/project-settings.html).
- Lerne das Vokabular in den [Kernkonzepten](/de/concepts.html).
- Verbinde ein Repository in der [Git-Integration](/de/git-integration.html).
