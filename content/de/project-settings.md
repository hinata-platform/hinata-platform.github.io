---
title: Projekteinstellungen
description: Einstellungen pro Projekt, mit farbigen Labels und Status, Entwurf und Speicherleiste, Mitgliedern, Teamzugriff, Projektschlüssel und Git-Verbindungen.
---

# Projekteinstellungen

Der [Adminbereich](/de/admin-area.html) konfiguriert die ganze Instanz. Die **Projekteinstellungen** gelten für ein einzelnes Projekt: Labels, Workflow, Sichtbarkeit und verbundene Repositories. Bearbeitet werden sie von der Projektleitung.

## Labels & Status

Kern der Projektkonfiguration sind zwei Listen mit farbigen, benannten Einträgen: **Labels** und **Status** des Workflows. Beide haben dieselbe Form:

```json
{ "id": "…", "name": "In Progress", "hue": 210 }
```

- **`name`**: was du siehst und worüber Vorgänge auf den Eintrag verweisen. Labels und Status sind **über den Namen verknüpft**. Ein Vorgang speichert den *Namen*, und die Zuordnung im Projekt läuft über diesen Namen.
- **`hue`**: die Farbe, gespeichert als Farbton in der gemeinsamen **ProjectPalette**. So hat jedes Projekt eine eigene, einheitliche Färbung statt eines festen globalen Farbsatzes.

**Status** sind die Spalten deines [Boards](/de/boards-sprints.html), z. B. *To Do → In Progress → In Review → Done*. **Labels** sind wiederverwendbare Tags, die du Vorgängen per Mehrfachauswahl anhängst.

### Entwurf und Speicherleiste

Änderungen an Labels und Status werden nicht bei jedem Tastendruck gespeichert. Du bearbeitest einen **Entwurf**: hinzufügen, umbenennen, umfärben, umsortieren. Solange Änderungen ungespeichert sind, erscheint eine **Speicherleiste**. Dort übernimmst oder verwirfst du alles auf einmal. So wirkt eine halb fertige Umbenennung nicht sofort im ganzen Projekt.

!!! info "Umbenennen wirkt auf bestehende Vorgänge"
    Vorgänge verweisen per Namen auf Status und Labels. Eine Umbenennung löst deshalb eine **Kaskade auf dem Server** aus, die bestehende Vorgänge auf den neuen Namen aktualisiert. So verwaist nichts. Eine **Migration beim Serverstart** hält ältere Daten passend zur aktuellen Form.

!!! tip "Farben gelten pro Projekt"
    Farbtöne liegen in der Palette des Projekts. Zwei Projekte können dieselben Statusnamen mit unterschiedlichen Farben nutzen, ohne sich in die Quere zu kommen. Wähle Farbtöne, die im hellen und dunklen Modus lesbar bleiben.

## Mitglieder & Teamzugriff

Hier legst du auch fest, **wer das Projekt sieht und darin arbeitet**. Dafür gibt es zwei Wege:

- **Mitglieder:** Personen, die direkt zum Projekt hinzugefügt wurden.
- **Teams:** Hinatas [Teams](/de/projects-teams.html) geben pro Mitglied Zugriff auf Projekte.

Eine Person sieht ein Projekt nur, wenn ihr Team oder eine direkte Mitgliedschaft es freigibt. Diese Prüfung gilt in der ganzen App. Schränkst du ein Projekt hier ein, verschwindet es für alle ohne Zugriff aus Boards, Suche und Berichten.

## Projektschlüssel

Jedes Projekt hat einen kurzen **Schlüssel** (z. B. `ASTA`), der vor den Vorgangsnummern steht (`ASTA-42`). Smart Commits, Branch-Namen und PR-Titel nutzen ihn, um Arbeit mit einem Vorgang zu verknüpfen. Siehe [Git-Integration](/de/git-integration.html).

## Git-Verbindungen

Ein Projekt kann in seinen Einstellungen **ein oder mehrere Repositories** auf GitHub, GitLab oder Bitbucket verbinden.

- Voraussetzung: Der Betreiber hat die OAuth-Apps im [Adminbereich](/de/admin-area.html) registriert.
- Die Projektleitung fügt hier Repositories hinzu und richtet Automatisierungsregeln und das Branch-Template ein (beides gilt für das ganze Projekt).
- Jedes verbundene Repo hat ein eigenes Token, einen eigenen Webhook und einen eigenen Standard-Branch.

Alle Details stehen unter [Git-Integration](/de/git-integration.html).

## Wie sich Änderungen ausbreiten

- **Labels und Status** werden gesammelt aus dem Entwurf gespeichert, wenn du die Speicherleiste bestätigst. Umbenennungen überträgt der Server auf bestehende Vorgänge.
- **Zugriffsänderungen** wirken sofort. Entfernst du ein Mitglied oder eine Teamfreigabe, ist das Projekt für diese Personen in der ganzen App ausgeblendet.
- **Git-Verbindungen** registrieren beim Verbinden ihren Webhook. Entwicklungsinfos erscheinen dann sofort an den Vorgängen.

## Wie es weitergeht

- [Projekte & Teams](/de/projects-teams.html): Teams, Mitgliedschaft und Sichtbarkeit.
- [Boards & Sprints](/de/boards-sprints.html): wie Status zu Spalten im Board werden.
- [Git-Integration](/de/git-integration.html): die Repositories eines Projekts verbinden.
