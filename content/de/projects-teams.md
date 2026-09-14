---
title: Projekte & Teams
description: Projekte bündeln Arbeit unter einem Schlüssel wie ASTA-42, und Teams legen pro Mitglied fest, wer welche Projekte sieht.
---

# Projekte & Teams

Alles in Hinata liegt in einem **Projekt**. Wer ein Projekt sehen darf, legen **Teams** fest.

So trennst du etwa eine mobile App, einen Backend-Dienst und interne Tools sauber voneinander. Jedes Projekt hat eigenes Board, eigenen Workflow, eigene Labels und eine eigene Nummerierung der Vorgänge. Sehen können es nur die Leute, die es sehen sollen.

![Hinata Teams](/assets/img/shot-teams.png)
*Teams geben Mitgliedern Zugriff auf Projekte im ganzen Workspace.*

## Projekte

Ein Projekt ist ein abgeschlossener Arbeitsbereich. Jedes Projekt hat:

- **Einen Projektschlüssel:** ein kurzes Präfix in Großbuchstaben wie `HIN`, `MOB` oder `INF`. Vorgänge werden danach nummeriert (`MOB-42`). Eine Nummer wird nie neu vergeben, der Schlüssel bleibt also überall eindeutig.
- **Eigene Status:** die Spalten, durch die Vorgänge laufen (z. B. *To Do → In Progress → In Review → Done*). Sie gelten pro Projekt. Ein Forschungsprojekt kann so anders arbeiten als ein Lieferprojekt. Siehe [Projekteinstellungen](/de/project-settings.html).
- **Wiederverwendbare Labels:** farbige Tags (`frontend`, `needs-design`), einmal angelegt und für alle Vorgänge im Projekt nutzbar.
- **Mitglieder:** die Leute im Projekt. Sie erscheinen bei der Zuweisung, in Berichten und im Personenfilter des Boards.
- **Git-Verbindungen:** ein oder mehrere verknüpfte Repositories (siehe [Git-Integration](/de/git-integration.html)).

!!! tip "Wähle Schlüssel, die sich leicht tippen"
    Schlüssel stehen ständig in Commit-Nachrichten, Branch-Namen und im Chat (`git commit -m "MOB-42 fix crash"`). Kurze, einprägsame Schlüssel lohnen sich.

### Ein Projekt erstellen

Öffne **Projekte → Neues Projekt** und vergib Namen und Schlüssel. Status, Labels und Mitglieder änderst du jederzeit in den Projekteinstellungen, ohne bestehende Vorgänge zu stören. Umbenennungen werden sicher im ganzen Projekt übernommen.

## Teams

Ein **Team** ist eine Gruppe von Leuten mit Zugriff auf bestimmte Projekte. Ein Mitglied sieht nur die Projekte, die sein Team freigibt. Wer im *Mobile*-Team ist, sieht `MOB`. `INF` sieht er nur, wenn ein Team es ebenfalls freigibt.

Diese Prüfung gilt **im ganzen Workspace**: für Board, Vorgangslisten, Suchergebnisse, Berichte und sogar Benachrichtigungen. Einen extra Schritt zum Teilen gibt es nicht. Wer Mitglied ist, hat Zugriff.

!!! info "Wie der Zugriff durchgesetzt wird"
    Der Server prüft die Sichtbarkeit bei jeder Anfrage (der Aufrufer muss Mitglied des Projekts sein). Die App zeigt nur, was der Server liefert. Am Client lässt sich der Zugriff also nicht umgehen.

### Rollen

- **Mitglieder** erledigen die tägliche Arbeit: Vorgänge anlegen und bearbeiten, kommentieren, Zeit erfassen, Karten verschieben.
- **Admins** haben zusätzlich Zugang zum [Adminbereich](/de/admin-area.html) mit Benutzern, SSO, E-Mail zu Ticket, Git-OAuth-Apps und Einstellungen für die ganze App. Admin ist eine Workspace-Rolle (`ADMIN`) und wird an jedem `/api/v1/admin/**`-Endpunkt geprüft.

### Mitglieder verwalten

In den Team- und Projekteinstellungen fügst du Leute einem Team oder einem einzelnen Projekt hinzu oder entfernst sie. Änderungen wirken sofort. Ein entferntes Mitglied verliert die Sichtbarkeit bei seiner nächsten Anfrage.

## Wie Projekte und Teams zusammenpassen

```text
Team "Mobile"  ──gewährt──▶  Projekt MOB  ──enthält──▶  Vorgänge MOB-1, MOB-2, …
Team "Platform"──gewährt──▶  Projekt INF  ──enthält──▶  Vorgänge INF-1, INF-2, …
        │                        ▲
        └────gewährt ebenfalls───┘   (ein Team kann mehrere Projekte gewähren)
```

Ein Benutzer kann in mehreren Teams sein und sieht dann mehrere Projekte. Ein Projekt kann von mehreren Teams freigegeben werden. Bilde deine Organisation so ab, wie es passt, etwa nach Squad, Abteilung oder Kunde.

## Nächste Schritte

- Status und Labels eines Projekts einrichten: [Projekteinstellungen](/de/project-settings.html).
- Die wichtigsten Begriffe: [Kernkonzepte](/de/concepts.html).
- Ein Repository verbinden: [Git-Integration](/de/git-integration.html).
