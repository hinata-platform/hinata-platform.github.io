---
title: Wissensdatenbank
description: Ein eingebautes Wiki wie Confluence mit verschachtelten Markdown-Artikeln, global oder pro Projekt.
---

# Wissensdatenbank

Runbooks, Einarbeitungsleitfäden, Architekturentscheidungen, Besprechungsnotizen und Produktspezifikationen passen nicht in einen Vorgang. Dafür gibt es die **Wissensdatenbank**: ein eingebautes Wiki wie Confluence, direkt neben deiner Arbeit.

![Hinata-Wissensdatenbank](/assets/img/shot-knowledge.png)
*Spaces und verschachtelte Markdown-Artikel neben der Arbeit.*

## Artikel

Artikel schreibst du in **Markdown**, mit demselben Editor und derselben Symbolleiste wie in Vorgangsbeschreibungen: Überschriften, Listen, Codeblöcke, Tabellen, Callouts und Bilder. Artikel lassen sich in einer **Hierarchie** verschachteln: ein Space, seine Abschnitte und die Seiten darin.

- **Globale Artikel:** Dokumentation für den ganzen Workspace, lesbar für alle mit Zugriff. Zum Beispiel Unternehmenshandbuch, Entwicklungsstandards oder Playbooks für Störungen.
- **Projektbezogene Artikel:** Dokumentation für ein einzelnes Projekt, direkt neben dessen Board und Vorgängen.

!!! info "Von echten Daten gestützt"
    Die Wissensdatenbank ist eine vollwertige Funktion im Backend (`/api/v1/articles`). Artikel liegen versioniert in deiner Datenbank und kommen wie alles andere über die API. Dadurch sind sie durchsuchbar, zugriffsgeschützt und immer aktuell.

## Smart Links

Beim Schreiben lösen **Smart Links** Verweise live auf:

- Erwähnst du einen Vorgang wie `MOB-42`, wird er zu einem Link mit dem aktuellen Titel und Status.
- Erwähnst du eine Person, verlinkt sie auf ihr Profil.

Ein Runbook, das auf `INF-7` verweist, zeigt also immer den aktuellen Vorgang.

## Zugriffssteuerung

Artikel folgen denselben [Sichtbarkeitsregeln für Teams und Projekte](/de/projects-teams.html) wie der Rest von Hinata:

- Einen Projektspace sieht, wer das Projekt sieht.
- Globale Spaces folgen dem Zugriff auf den Workspace.

Zusätzlich einstellen musst du nichts.

!!! tip "Verlinke Doku und Lieferung in beide Richtungen"
    Verweise im Kommentar eines Vorgangs auf einen Artikel und im Artikel auf den Vorgang. So bleibt die Wissensdatenbank lebendig.

## Nächste Schritte

- [Vorgänge](/de/issues.html): die Verweise, die Smart Links auflösen.
- [Projekte & Teams](/de/projects-teams.html): wer welche Artikel sieht.
- [Befehlspalette](/de/search.html): alles schnell finden.
