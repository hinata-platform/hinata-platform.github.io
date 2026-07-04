---
title: Wissensdatenbank
description: Eine eingebaute Wissensdatenbank im Confluence-Stil — hierarchische Markdown-Artikel, global oder pro Projekt, mit Smart Links, die echte Vorgänge und Personen auflösen.
---

# Wissensdatenbank

Nicht alles gehört in einen Vorgang. Runbooks, Onboarding-Leitfäden, Architekturentscheidungen, Meeting-Notizen und Produktspezifikationen brauchen ein eigenes Zuhause — und Hinata gibt ihnen eines. Die **Wissensdatenbank** ist ein eingebautes Wiki im Confluence-Stil, das direkt neben deiner Arbeit lebt, sodass Dokumentation und Lieferung nie auseinanderdriften.


![Hinata-Wissensdatenbank](/assets/img/shot-knowledge.png)
*Die Wissensdatenbank — Spaces und hierarchische Markdown-Artikel direkt neben der Arbeit.*

## Artikel

Artikel werden in **Markdown** geschrieben, mit demselben gemeinsamen Editor und derselben Symbolleiste, die du aus Vorgangsbeschreibungen kennst — Überschriften, Listen, Codeblöcke, Tabellen, Callouts und Bilder. Sie schachteln sich in eine **Hierarchie**, sodass du eine echte Struktur aufbauen kannst: einen Space, seine Abschnitte und die Seiten darin.

- **Globale Artikel** — workspace-weite Dokumentation, die jeder (mit Zugriff) lesen kann: Unternehmenshandbuch, Engineering-Standards, Incident-Playbooks.
- **Projektbezogene Artikel** — Dokumentation, die auf ein einzelnes Projekt beschränkt ist und neben dem Board und den Vorgängen dieses Projekts sitzt.

!!! info "Von echten Daten gestützt"
    Die Wissensdatenbank ist eine vollwertige Backend-Funktion (`/api/v1/articles`), kein statisches Bündel. Artikel werden in deiner Datenbank gespeichert, versioniert und wie alles andere über die API ausgeliefert — sodass sie durchsuchbar, zugriffskontrolliert und stets aktuell sind.

## Smart Links

Die Wissensdatenbank ist kein abgeschotteter Garten. Während du schreibst, lösen **Smart Links** Live-Referenzen auf:

- Erwähne einen Vorgang (`MOB-42`), und er wird zu einem Live-Link, der den echten Titel und Status des Vorgangs zeigt.
- Erwähne eine Person, und sie wird zu ihrem tatsächlichen Profil aufgelöst.

Weil die Links live sind, zeigt ein Runbook, das auf `INF-7` verweist, immer auf den echten, aktuellen Vorgang — keine veralteten Kopien, keine kaputten Querverweise.

## Zugriffssteuerung

Artikel respektieren dieselbe [Team- und Projektsichtbarkeit](/de/projects-teams.html) wie der Rest von Hinata. Ein projektbezogener Space ist für die Personen sichtbar, die dieses Projekt sehen können; globale Spaces folgen dem Workspace-Zugriff. Es gibt nichts zusätzlich zu konfigurieren — die Personen, die eine Seite sehen sollen, können es bereits.

!!! tip "Verlinke Doku und Lieferung in beide Richtungen"
    Verweise aus einem Vorgangskommentar auf einen Artikel und aus einem Artikel auf einen Vorgang. Diese wechselseitige Verlinkung ist es, die eine Wissensdatenbank lebendig hält, statt sie in einem vergessenen Wiki verrotten zu lassen.

## Nächste Schritte

- Lerne die [Vorgangs](/de/issues.html)-Referenzen kennen, die Smart Links auflösen.
- Verstehe [Projekte & Teams](/de/projects-teams.html), die den Artikelzugriff einschränken.
- Finde alles blitzschnell mit der [Befehlspalette](/de/search.html).
