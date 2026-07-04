---
title: Projekteinstellungen
description: Projektbezogene Konfiguration in Hinata — farbige Labels und Workflow-Status, der Entwurf-plus-Speicherleiste-Editor, Mitglieder und Team-Zugriff, der Projektschlüssel und Git-Verbindungen.
---

# Projekteinstellungen

Während der [Adminbereich](/de/admin-area.html) die gesamte Instanz konfiguriert,
konfigurieren die **Projekteinstellungen** ein einzelnes Projekt: seine Labels,
seinen Workflow, wer es sehen kann und welche Repositories es verfolgt. Alles hier
ist auf ein Projekt beschränkt und wird von dessen Projektleitung bearbeitet.

## Labels & Workflow-Status

Das Herzstück der Konfiguration eines Projekts sind zwei Listen farbiger,
benannter Elemente — **Labels** und **Workflow-Status**. Beide teilen sich dieselbe
Form:

```json
{ "id": "…", "name": "In Progress", "hue": 210 }
```

- **`name`** — das, was du siehst, und die Art, wie Vorgänge auf das Element
  verweisen. Labels und Status sind **namensbasiert (name-keyed)**: Ein Vorgang
  speichert den *Namen*, sodass Status und Labels projektweit über den Namen
  zusammenpassen.
- **`hue`** — eine Farbe, gespeichert als Farbton (Hue) in der gemeinsamen
  **ProjectPalette**, sodass jedes Projekt seine eigene, konsistente Färbung
  erhält, statt eines fest vorgegebenen globalen Sets.

**Workflow-Status** sind die Spalten, auf die dein [Board](/de/boards-sprints.html)
abbildet — z. B. *To Do → In Progress → In Review → Done*. **Labels** sind die
wiederverwendbaren Tags, die du Vorgängen über eine Mehrfachauswahl anhängst.

### Der Entwurf-plus-Speicherleiste-Editor

Das Bearbeiten von Labels und Status speichert nicht bei jedem Tastenanschlag. Du
bearbeitest einen **Entwurf** — hinzufügen, umbenennen, umfärben, umsortieren —
und eine **Speicherleiste** erscheint, solange du ungespeicherte Änderungen hast,
damit du sie alle auf einmal übernehmen oder verwerfen kannst. So verhindert ein
halbfertiges Umbenennen, dass sich Änderungen sofort durch das Projekt ziehen.

!!! info "Das Umbenennen eines Status wirkt kaskadierend"
    Weil Vorgänge über den Namen auf Status und Labels verweisen, löst das
    Umbenennen eines Elements eine **serverseitige Umbenennungs-Kaskade** aus:
    Bestehende Vorgänge werden auf den neuen Namen aktualisiert, sodass nichts
    verwaist. Eine **Boot-Migration** hält ältere Daten konsistent mit der
    aktuellen Form, während sich die Plattform weiterentwickelt. Du benennst einmal
    um; das Projekt zieht nach.

!!! tip "Farben sind projektbezogen"
    Farbtöne liegen in der Palette des Projekts, sodass zwei Projekte dieselben
    Statusnamen mit unterschiedlichen Farben verwenden können, ohne zu kollidieren.
    Wähle Farbtöne, die sowohl im hellen als auch im dunklen Modus lesbar bleiben.

## Mitglieder & Team-Zugriff

In den Projekteinstellungen steuerst du auch, **wer das Projekt sehen und darin
arbeiten kann**. Die Sichtbarkeit wird auf zwei Wegen gesteuert:

- **Mitglieder** — die Personen, die direkt zum Projekt hinzugefügt wurden.
- **Teams** — Hinatas [Teams](/de/projects-teams.html) gewähren pro Mitglied
  Projektzugriff. Eine Person sieht nur ein Projekt, das ihr Team (oder eine
  direkte Mitgliedschaft) gewährt; diese Zugriffsprüfung steuert die Sichtbarkeit
  des Projekts app-weit, sodass das Einschränken eines Projekts hier es aus Boards,
  Suche und Berichten aller entfernt, die keinen Zugriff haben.

## Projektschlüssel

Jedes Projekt hat einen kurzen **Schlüssel** (z. B. `ASTA`), der seinen
Vorgangsnummern vorangestellt wird (`ASTA-42`). Der Schlüssel ist das, worauf
Smart Commits, Branch-Namen und PR-Titel verweisen, um Arbeit mit einem Vorgang zu
verknüpfen — siehe [Git-Integration](/de/git-integration.html).

## Git-Verbindungen

Ein Projekt kann aus seinen Einstellungen **ein oder mehrere Repositories** auf
GitHub, GitLab oder Bitbucket verbinden. Sobald der Betreiber die OAuth-Apps im
[Adminbereich](/de/admin-area.html) registriert hat, fügt eine Projektleitung hier
Repositories hinzu, konfiguriert Automatisierungsregeln und das Branch-Template
(projektweit geteilt), und jedes verbundene Repo behält sein eigenes Token, seinen
eigenen Webhook und seinen eigenen Standard-Branch. Alle Details findest du in der
[Git-Integration](/de/git-integration.html).

## Wie sich Änderungen ausbreiten

- **Labels/Status** werden als Batch aus dem Entwurf gespeichert, wenn du die
  Speicherleiste bestätigst; Umbenennungen kaskadieren serverseitig zu
  bestehenden Vorgängen.
- **Zugriffsänderungen** werden sofort wirksam — das Entfernen eines Mitglieds
  oder der Team-Gewährung blendet das Projekt für sie app-weit aus.
- **Git-Verbindungen** registrieren beim Verbinden ihren Webhook, sodass
  Entwicklungsinformationen sofort auf Vorgänge fließen.

## Wie es weitergeht

- [Projekte & Teams](/de/projects-teams.html) — Teams, Mitgliedschaft und Sichtbarkeit.
- [Boards & Sprints](/de/boards-sprints.html) — wie Workflow-Status zu Board-Spalten werden.
- [Git-Integration](/de/git-integration.html) — verbinde die Repositories eines Projekts.
