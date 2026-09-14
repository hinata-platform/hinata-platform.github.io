---
title: Vorgänge & Hierarchie
description: Der Vorgang ist Hinatas zentrales Arbeitselement, geordnet in der Hierarchie Epic → Story → Sub-Task.
---

# Vorgänge & Hierarchie

Alles, was du in Hinata planst, zuweist, besprichst und auslieferst, ist ein **Vorgang**: ein Epic über ein Quartal, eine Story im aktuellen Sprint, ein frisch gemeldeter Bug oder ein Sub-Task. Diese Seite zeigt, was ein Vorgang enthält, wie Vorgänge verschachtelt werden und wie sie mit Git zusammenhängen.

!!! info "Wo Vorgänge leben"
    Jeder Vorgang gehört zu genau einem [Projekt](/de/projects-teams.html) und trägt dessen Schlüssel als Präfix, etwa `ASTA-42` oder `WEB-7`. Die Nummer wird einmal vergeben und nie wiederverwendet. Den Schlüssel kannst du also dauerhaft in Chats, Commit-Nachrichten oder den Browser einfügen.


![Hinata Vorgangsdetail](/assets/img/shot-issue.png)
*Das Vorgangsdetail mit Beschreibung, Sub-Tasks, Verknüpfungen, Anhängen, Details und Git-Aktivität.*

## Anatomie eines Vorgangs

Ein Vorgang enthält:

- **Typ**: **Epic, Story, Task, Bug, Feature** oder **Sub-Task**. Der Typ bestimmt Icon, Farbe und den Platz in der Hierarchie.
- **Titel & Beschreibung**: Die Beschreibung ist **Markdown** mit gemeinsamer Toolbar (Überschriften, Listen, Code, Links). Smart Links lösen Vorgänge und Personen beim Tippen auf.
- **Priorität**: eine abgestufte Skala von niedrigster bis höchster.
- **Bearbeiter & Melder**: wer die Arbeit erledigt und wer sie gemeldet hat.
- **Labels**: wiederverwendbare, farbige [Projekt-Labels](/de/project-settings.html) zum Filtern (z. B. `frontend`, `needs-design`).
- **Story Points**: eine Schätzung für die Sprintkapazität und den Velocity-Bericht.
- **Daten**: Start- und Fälligkeitsdatum, die auch die [Gantt-Timeline](/de/timeline.html) steuern.
- **Workflow-Zustand**: die Spalte auf dem [Board](/de/boards-sprints.html), aus den Zuständen des Projekts.
- **Kommentare**: flache Diskussion mit Antwort-Threads, Reaktionen und Sprachnachrichten.
- **Anhänge**: Dateien und Bilder.
- **Abhängigkeiten & Verknüpfungen**: Beziehungen zu anderen Vorgängen.

### Typen auf einen Blick

| Typ | Typische Verwendung | Rolle in der Hierarchie |
| --- | --- | --- |
| **Epic** | Ein großer Arbeitsblock über viele Sprints | Oberste Ebene, über Storys, Tasks, Bugs und Features |
| **Story** | Ein Stück Nutzen für Anwender | Mittlere Ebene, kann Sub-Tasks haben |
| **Task** | Arbeit, die Anwender nicht direkt sehen | Mittlere Ebene, kann Sub-Tasks haben |
| **Bug** | Ein zu behebender Fehler | Mittlere Ebene, kann Sub-Tasks haben |
| **Feature** | Eine zu bauende Funktion | Mittlere Ebene, kann Sub-Tasks haben |
| **Sub-Task** | Ein kleiner Schritt innerhalb einer Story, Task, Bug oder Feature | Unterste Ebene |

## Beschreibungen & Kommentare

Beschreibung und Kommentare unterstützen **Markdown** mit gemeinsamer Toolbar. So bekommst du Überschriften, Checklisten, Codeblöcke und Links, ohne die Syntax zu kennen.

- **@-Erwähnungen** benachrichtigen ein Teammitglied direkt.
- **Smart Links** erkennen Vorgangsschlüssel und machen daraus Verweise. `ASTA-42` wird aufgelöst und bleibt hervorgehoben, auch wenn sich der Titel später ändert. Die [Wissensdatenbank](/de/knowledge-base.html) nutzt dieselbe Technik.

!!! tip "Halte die Diskussion am Vorgang"
    Entscheidungen aus Kommentaren bleiben dauerhaft am Vorgang. Wer das Ticket später übernimmt, findet sie dort.

Kommentare stehen flach und linksbündig untereinander wie in Jira, ohne Chatblasen. Das lässt sich bei langen Vorgängen leichter überfliegen. Jeder Wurzelkommentar kann einen eigenen **Antwort-Thread** haben, der erst beim Öffnen lädt. Sortiere nach **neuestem zuerst** oder **ältestem zuerst** und springe per Permalink zu jedem Kommentar.

![Hinata-Kommentare mit Antwort-Thread](/assets/img/shot-comments.png)

- **Reaktionen**: ein Emoji auf einen Kommentar, wie bei WhatsApp. Pro Kommentar hast du eine Reaktion, eine neue ersetzt die alte.
- **Sprachkommentare**: Nimm im Composer eine kurze Sprachnachricht auf. Sie landet in deinem **S3/MinIO**-Bucket und spielt inline als Sprachblase mit Wellenform ab, zwischen den Textkommentaren.
- **Kontextmenü**: Lange drücken (am Desktop mit der Maus darüberfahren) für Antworten, Kopieren, Link kopieren, Anheften, Bearbeiten, Löschen und Mehrfachauswahl zum Löschen eigener Kommentare. Der kopierte Link scrollt zu genau diesem Kommentar und lässt ihn aufblinken.
- **Echtzeit**: Neue Kommentare, Bearbeitungen, Reaktionen und Löschungen kommen per **Server-Sent Events**. Alle sehen die Diskussion sofort, ohne neu zu laden.

## Anhänge

Ziehe Dateien direkt auf einen Vorgang. Sie liegen in deinem **S3/MinIO**-Bucket unter zufälligen Objektschlüsseln und werden über kurzlebige **presigned** URLs ausgeliefert. So wird nichts versehentlich öffentlich.

- Datei per **Drag & Drop** auf das Anhangraster ziehen oder über die Upload-Schaltfläche vom Gerät wählen.
- Bilder öffnen sich groß in einer **Lightbox** im Liquid-Glass-Stil.
- Änderungen kommen **live per Server-Sent Events**. Fügt jemand eine Datei hinzu oder entfernt sie, aktualisiert sich deine Ansicht ohne Neuladen.
- Größen- und Typlimits setzt der Betreiber per Umgebungsvariablen. Siehe [Objektspeicher](/de/storage.html).

## Abhängigkeiten & Verknüpfungen

Verknüpfe Vorgänge, um Beziehungen auszudrücken, etwa dass ein Vorgang einen anderen **blockiert** oder mit ihm **in Beziehung steht**. Abhängigkeiten erscheinen in der [Gantt-Timeline](/de/timeline.html). Eine blockierende Verknüpfung wird dort als Linie zwischen den Balken gezeichnet. So siehst du, was zuerst fertig sein muss.

## Die dreistufige Hierarchie

Hinata ordnet Arbeit in **drei Ebenen**, ähnlich wie Jira:

```text
Epic
└─ Story / Task / Bug / Feature
   └─ Sub-Task
```

- **Epic**: oberste Ebene. Gruppiert die Storys, Tasks, Bugs und Features, die es liefern.
- **Story, Task, Bug oder Feature**: mittlere Ebene. Kann an einem Epic hängen und sich in Sub-Tasks aufteilen.
- **Sub-Task**: kleinster Schritt, immer unter einem übergeordneten Element.

Am Vorgang selbst baust und navigierst du diese Struktur:

- **Breadcrumb**: zeigt oben die Abstammung (Epic › Story › Sub-Task). Ein Klick springt eine Ebene höher.
- **Auswahl des übergeordneten Elements**: Setze oder ändere es über eine durchsuchbare Auswahl, etwa um eine Story an ein Epic zu hängen.
- **Panel für untergeordnete Elemente**: listet an einem Epic seine Elemente und lässt dich weitere hinzufügen.
- **Sub-Task-Panel**: listet an einer Story, Task, Bug oder Feature die Sub-Tasks und lässt dich inline neue anlegen.

### Archivieren vs. Löschen

**Archivieren** ist ein weiches Löschen:

- Jedes Projektmitglied darf archivieren.
- Sub-Tasks werden mitarchiviert.
- Der Vorgang verschwindet standardmäßig aus Suche, Board und Sprints.
- Du kannst ihn genauso leicht wieder entarchivieren.

**Endgültiges Löschen** ist destruktiv und dürfen nur Plattform-Admin, Projektleiter oder Team-Admin. Hinata prüft deine Rechte am Vorgang und bietet nur die Option an, die du nutzen darfst.

!!! warning "Endgültiges Löschen lässt sich nicht rückgängig machen"
    Was mitgelöscht wird, hängt vom Typ ab:

    - **Standardvorgang** (Story, Task, Bug, Feature): Die Sub-Tasks werden samt Kommentaren, Arbeitsprotokollen und Verknüpfungen mit entfernt. Ein Sub-Task kann ohne übergeordnetes Element nicht existieren.
    - **Epic**: Die untergeordneten Vorgänge bleiben als normale Vorgänge der obersten Ebene erhalten. Sie verlieren nur die Epic-Verknüpfung.

    Archiviere im Zweifel zuerst.

Die Hierarchie steuert auch das Board: Du kannst das [agile Board](/de/boards-sprints.html) nach **Epic** oder **Sub-Task** in Swimlanes gruppieren und auf ein einzelnes Epic filtern.

## Vorgänge und Git

Ist ein Projekt mit einem Repository verbunden, verknüpft Hinata über den Vorgangsschlüssel:

- Ein **Branch**, dessen Name `ASTA-42` enthält, gehört zu diesem Vorgang.
- Ein **Commit** gehört nur dazu, wenn seine Nachricht `ASTA-42` nennt. Dass er auf dem Branch des Vorgangs liegt, reicht nicht.
- Ein **Pull oder Merge Request** wird über Titel oder Quell-Branch verknüpft.

Branches, Commits, PR/MRs und Build-Status erscheinen dann direkt am Vorgang.

### Smart Commits

Mit **Trailern** in der Commit-Nachricht wirkst du direkt auf einen Vorgang:

```text
ASTA-42 #comment Fixed the race in the uploader
ASTA-42 #time 2h 30m
ASTA-42 #done
```

- `#comment <text>` fügt dem Vorgang einen Kommentar hinzu.
- `#time 2h 30m` erfasst Arbeit am Vorgang.
- Jedes andere `#word` setzt den passenden Workflow-Zustand.

Die Nebeneffekte laufen **genau einmal**, auch wenn Anbieter Webhooks erneut zustellen. Einrichtung, Automatisierungsregeln und Webhooks beschreibt [Git-Integration](/de/git-integration.html).

## Verwandte Seiten

- **[Projekte & Teams](/de/projects-teams.html)**: wo Vorgänge, Schlüssel, Labels und Workflow-Zustände definiert werden.
- **[Boards & Sprints](/de/boards-sprints.html)**: Vorgänge durch den Workflow und in Sprints bewegen.
- **[Gantt & Zeiterfassung](/de/timeline.html)**: Daten, Abhängigkeiten und Arbeitszeit erfassen.
- **[Git-Integration](/de/git-integration.html)**: ein Repo verbinden und Smart Commits nutzen.
