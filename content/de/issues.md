---
title: Vorgänge & Hierarchie
description: Der Vorgang ist Hinatas zentrales Arbeitselement — Typen, Prioritäten, Labels, Markdown, Kommentare, Anhänge und Abhängigkeiten — organisiert in einer dreistufigen Hierarchie Epic → Story → Sub-Task.
---

# Vorgänge & Hierarchie

Der **Vorgang** ist das Atom der Arbeit in Hinata. Alles, was du planst, zuweist, besprichst und auslieferst, ist ein Vorgang: ein Epic, das sich über ein Quartal erstreckt, eine Story in diesem Sprint, ein gerade gemeldeter Bug oder ein Sub-Task auf einer Checkliste. Diese Seite behandelt, was ein Vorgang enthält, wie sich Vorgänge zu einer Hierarchie verschachteln und wie sie sich mit deiner Git-Historie verknüpfen.

!!! info "Wo Vorgänge leben"
    Jeder Vorgang gehört zu genau einem [Projekt](/de/projects-teams.html) und trägt den Schlüssel dieses Projekts als Präfix — `ASTA-42`, `WEB-7`. Die Nummer wird einmal vergeben und nie wiederverwendet, sodass ein Schlüssel ein stabiler, menschenfreundlicher Bezeichner ist, den du in einen Chat, eine Commit-Nachricht oder einen Browser einfügen kannst.


![Hinata Vorgangsdetail](/assets/img/shot-issue.png)
*Das Vorgangsdetail — Beschreibung, Sub-Tasks, Verknüpfungen, Anhänge, Details und Git-Aktivität.*

## Anatomie eines Vorgangs

Öffne einen beliebigen Vorgang, um die vollständige Detailansicht zu sehen. Ein Vorgang enthält:

- **Typ** — einer von **Epic, Story, Task, Bug, Feature** oder **Sub-Task**. Der Typ legt Icon und Farbe fest und entscheidet, wo der Vorgang in der Hierarchie sitzen kann (siehe unten).
- **Titel & Beschreibung** — die Beschreibung ist vollständiges **Markdown**, bearbeitet mit einer gemeinsamen Toolbar (Überschriften, Listen, Code, Links). Smart Links lösen echte Vorgänge und Personen auf, während du tippst.
- **Priorität** — eine abgestufte Skala von niedrigster bis höchster, damit das Team weiß, was zuerst anzupacken ist.
- **Bearbeiter & Melder** — wer die Arbeit erledigt und wer sie aufgeworfen hat.
- **Labels** — wiederverwendbare, farbige [Projekt-Labels](/de/project-settings.html) zum Schneiden und Filtern (z. B. `frontend`, `needs-design`).
- **Story Points** — eine Schätzung, die für Sprint-Kapazität und den Velocity-Bericht verwendet wird.
- **Daten** — ein Start- und Fälligkeitsdatum, die auch die [Gantt-Timeline](/de/timeline.html) steuern.
- **Workflow-Zustand** — die Spalte, in der der Vorgang auf dem [Board](/de/boards-sprints.html) sitzt, aus der eigenen Menge an Zuständen des Projekts.
- **Kommentare** — eine flache, verschachtelte Diskussion mit Antwort-Threads pro Kommentar, Reaktionen und Sprachnachrichten (siehe unten).
- **Anhänge** — Dateien und Bilder (siehe unten).
- **Abhängigkeiten & Verknüpfungen** — Beziehungen zu anderen Vorgängen.

### Typen auf einen Blick

| Typ | Typische Verwendung | Rolle in der Hierarchie |
| --- | --- | --- |
| **Epic** | Ein großer Arbeitsblock über viele Sprints | Oberste Ebene — übergeordnet für Storys, Tasks, Bugs, Features |
| **Story** | Ein nutzergerichteter Wertausschnitt | Mittlere Ebene — kann Sub-Tasks haben |
| **Task** | Eine Arbeitseinheit, die nicht nutzergerichtet ist | Mittlere Ebene — kann Sub-Tasks haben |
| **Bug** | Ein zu behebender Defekt | Mittlere Ebene — kann Sub-Tasks haben |
| **Feature** | Eine zu bauende Fähigkeit | Mittlere Ebene — kann Sub-Tasks haben |
| **Sub-Task** | Ein kleiner Schritt innerhalb einer Story/Task/Bug/Feature | Blattebene |

## Beschreibungen & Kommentare

Die Beschreibung und jeder Kommentar unterstützen **Markdown** mit einer gemeinsamen Editor-Toolbar, sodass du Überschriften, Checklisten, Codeblöcke und Links erhältst, ohne die Syntax auswendig zu lernen. Während du tippst, benachrichtigen **@-Erwähnungen** ein Teammitglied direkt, und **Smart Links** erkennen separat Vorgangsschlüssel und verwandeln sie in lebendige Referenz-Pills — erwähne `ASTA-42`, und es löst sich auf (und bleibt hervorgehoben), selbst wenn sich der Titel später ändert. Dies ist dieselbe Smart-Link-Engine, die auch die [Wissensdatenbank](/de/knowledge-base.html) nutzt.

!!! tip "Halte die Diskussion am Vorgang"
    Kommentare leben bei der Arbeit, nicht in einem separaten Chat. Wenn eine Entscheidung in einem Kommentar getroffen wird, bleibt sie für immer am Vorgang angehängt — das zukünftige Du (und alle, die das Ticket erben) werden es dir danken.

Kommentare werden flach und linksbündig dargestellt, im Jira-Stil, statt als Chat-Bubbles — das lässt sich bei einem lange laufenden Vorgang leichter überfliegen. Jeder Wurzelkommentar kann seinen eigenen **Antwort-Thread** tragen, der erst beim Öffnen nachgeladen wird, sodass ein vielbesprochener Vorgang nicht jede Antwort im Voraus laden muss. Sortiere den Thread nach **neuestem zuerst** oder **ältestem zuerst** und springe über den Permalink direkt zu jedem Kommentar.

![Hinata-Kommentare mit Antwort-Thread](/assets/img/shot-comments.png)

- **Reaktionen** — reagiere auf einen Kommentar mit einem Emoji, im WhatsApp-Stil; du hast eine Reaktion pro Kommentar, eine neue Wahl ersetzt die alte.
- **Sprachkommentare** — nimm direkt im Composer eine kurze Sprachnachricht auf. Sie wird in dein **S3/MinIO**-Bucket hochgeladen und spielt inline als Waveform-Bubble ab, neben Textkommentaren im selben Thread.
- **Kontextmenü** — halte einen Kommentar lange gedrückt (oder fahre am Desktop mit der Maus darüber) für Antworten, Kopieren, Link kopieren (ein Deep Link, der zu genau diesem Kommentar scrollt und ihn aufblinken lässt), Anheften, Bearbeiten, Löschen sowie Mehrfachauswahl zum Stapel-Löschen eigener Kommentare.
- **Live-Updates** — neue Kommentare, Bearbeitungen, Reaktionen und Löschungen strömen über **Server-Sent Events**, sodass alle, die einen Vorgang beobachten, die Diskussion in Echtzeit aktualisiert sehen, ohne neu zu laden.

## Anhänge

Ziehe Dateien direkt auf einen Vorgang. Anhänge werden in deinem eigenen **S3/MinIO**-Bucket mit zufällig erzeugten Objektschlüsseln gespeichert und über kurzlebige **presigned** URLs ausgeliefert, sodass nichts versehentlich öffentlich ist.

- **Ziehe eine Datei per Drag & Drop** auf das Anhang-Raster oder nutze die Upload-Schaltfläche, um von deinem Gerät auszuwählen.
- Bilder öffnen sich in einer **Liquid-Glass-Lightbox** für eine Ansicht in voller Größe.
- Änderungen strömen **live über Server-Sent Events** — wenn ein Teammitglied eine Datei hinzufügt oder entfernt, aktualisiert sich deine Ansicht ohne Neuladen.
- Größen- und Typlimits werden vom Betreiber über Umgebungsvariablen gesetzt. Siehe [Objektspeicher](/de/storage.html) für die Admin-Seite.

## Abhängigkeiten & Verknüpfungen

Vorgänge stehen selten allein. Verknüpfe sie, um Beziehungen auszudrücken — zum Beispiel, dass ein Vorgang einen anderen **blockiert** oder mit ihm **in Beziehung steht**. Abhängigkeiten fließen in die [Gantt-Timeline](/de/timeline.html) ein, wo eine blockierende Verknüpfung als Verbindung zwischen Balken gezeichnet wird, sodass offensichtlich wird, was fertig sein muss, bevor etwas anderes beginnen kann.

## Die dreistufige Hierarchie

Hinata organisiert Arbeit in einer Jira-artigen **dreistufigen Hierarchie**:

```text
Epic
└─ Story / Task / Bug / Feature
   └─ Sub-Task
```

- Ein **Epic** ist die Spitze eines Baums und gruppiert die Storys, Tasks, Bugs und Features, die es liefern.
- Eine **Story, Task, Bug oder Feature** sitzt in der Mitte und kann an ein Epic angehängt und in Sub-Tasks zerlegt werden.
- Ein **Sub-Task** ist ein Blatt — der kleinste Schritt, immer unter einem übergeordneten Arbeitselement.

Du navigierst und baust diese Struktur direkt am Vorgang:

- **Breadcrumb** — jeder Vorgang zeigt oben seine Abstammung (Epic › Story › Sub-Task), sodass du immer weißt, wo du bist, und mit einem Klick eine Ebene nach oben springen kannst.
- **Übergeordneten-Auswahl** — setze oder ändere das übergeordnete Element eines Vorgangs (zum Beispiel eine Story an ein Epic anhängen) über eine durchsuchbare Auswahl.
- **Untergeordneten-Panel** — an einem Epic listet ein Panel seine untergeordneten Arbeitselemente auf und lässt dich weitere hinzufügen.
- **Sub-Task-Panel** — an einer Story/Task/Bug/Feature listet ein Panel ihre Sub-Tasks auf und lässt dich sie inline hinzufügen.

### Archivieren vs. Löschen

Meistens willst du einen Vorgang nicht dauerhaft löschen — du willst ihn nur aus dem Weg räumen. **Archivieren** ist ein weiches Löschen: Jedes Projektmitglied kann einen Vorgang archivieren (Sub-Tasks kaskadieren mit), und er verschwindet standardmäßig aus Suche, Board und Sprints — ist aber nicht weg und lässt sich genauso leicht wieder entarchivieren.

**Endgültiges Löschen** ist destruktiv und rollenbeschränkt: Nur ein Plattform-Admin, der Projektleiter oder ein Team-Admin kann einen Vorgang dauerhaft löschen. Die Oberfläche von Hinata prüft deine Berechtigungen am Vorgang und bietet dir nur die Option an, die du tatsächlich nutzen darfst.

!!! warning "Endgültiges Löschen eines übergeordneten Elements kaskadiert — ohne Rückgängig"
    Das dauerhafte Löschen eines Vorgangs, der untergeordnete Elemente hat, **kaskadiert**: Seine untergeordneten Elemente (und deren Sub-Tasks) werden zusammen mit ihren Kommentaren, Arbeitsprotokollen und Verknüpfungen mit ihm entfernt. Es gibt kein Rückgängig — archiviere also zuerst, wenn du dir nicht sicher bist, und hebe das endgültige Löschen für Aufräumarbeiten auf, die wirklich nicht mehr existieren sollen.

Die Hierarchie treibt auch das Board an: Du kannst das [agile Board](/de/boards-sprints.html) nach **Epic** oder **Sub-Task** in Swimlanes gruppieren und das ganze Board auf ein einzelnes Epic herunterfiltern.

## Vorgänge und Git

Ein Vorgangsschlüssel ist die Brücke zu deinem Code. Sobald ein Projekt mit einem Repository verbunden ist, verknüpft Hinata Branches, Commits und Pull Requests anhand ihres Schlüssels mit Vorgängen:

- Ein **Branch**, dessen Name `ASTA-42` enthält, verknüpft sich mit diesem Vorgang.
- Ein **Commit**, dessen Nachricht auf `ASTA-42` verweist, verknüpft sich mit ihm — und nur dann; ein Commit wird nie allein deshalb verknüpft, weil er auf dem Branch eines Vorgangs liegt.
- Ein **Pull-/Merge-Request** verknüpft sich über seinen Titel oder Quell-Branch.

Die verknüpften Entwicklungsinformationen — Branches, Commits, PR/MRs und Build-Status — erscheinen am Vorgang, sodass du den Zustand des Codes sehen kannst, ohne das Ticket zu verlassen.

### Smart Commits

Du kannst auch direkt aus einer Commit-Nachricht heraus auf einen Vorgang einwirken, indem du **Trailer** nutzt:

```text
ASTA-42 #comment Fixed the race in the uploader
ASTA-42 #time 2h 30m
ASTA-42 #done
```

- `#comment <text>` fügt dem Vorgang einen Kommentar hinzu.
- `#time 2h 30m` erfasst Arbeit am Vorgang.
- Jedes andere `#word` überführt den Vorgang in einen passenden Workflow-Zustand.

Nebeneffekte von Smart Commits werden **genau einmal** angewendet, auch wenn Provider Webhooks erneut zustellen. Für das vollständige Bild — Provider-Einrichtung, Automatisierungsregeln und Webhooks — siehe [Git-Integration](/de/git-integration.html).

## Verwandte Seiten

- **[Projekte & Teams](/de/projects-teams.html)** — wo Vorgänge, Schlüssel, Labels und Workflow-Zustände definiert werden.
- **[Boards & Sprints](/de/boards-sprints.html)** — bewege Vorgänge durch deinen Workflow und in Sprints.
- **[Gantt & Zeiterfassung](/de/timeline.html)** — Daten, Abhängigkeiten und das Erfassen von Arbeit.
- **[Git-Integration](/de/git-integration.html)** — verbinde ein Repo und nutze Smart Commits.
