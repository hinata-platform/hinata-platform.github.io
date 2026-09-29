---
title: Wissensdatenbank
description: Ein eingebautes Wiki wie Confluence mit verschachtelten Markdown-Artikeln, geschützt über Projekt- und Teamrollen.
---

# Wissensdatenbank

Runbooks, Einarbeitungsleitfäden, Architekturentscheidungen, Besprechungsnotizen und Produktspezifikationen passen nicht in einen Vorgang. Dafür gibt es die **Wissensdatenbank**: ein eingebautes Wiki wie Confluence, direkt neben deiner Arbeit.

![Hinata-Wissensdatenbank](/assets/img/shot-knowledge.png)
*Spaces und verschachtelte Markdown-Artikel neben der Arbeit.*

## Artikel

Artikel schreibst du in **Markdown**, mit demselben Editor und derselben Symbolleiste wie in Vorgangsbeschreibungen: Überschriften, Listen, Codeblöcke, Tabellen, Callouts und Bilder. Artikel lassen sich in einer **Hierarchie** verschachteln: ein Space, seine Abschnitte und die Seiten darin.

- **Projektseiten:** Dokumentation für ein Projekt, direkt neben dessen Board und Vorgängen.
- **Teamseiten:** Dokumentation eines Teams, zum Beispiel Handbuch, Entwicklungsstandards oder Playbooks für Störungen.
- **Private Seiten:** Seiten ohne Projekt und Team, etwa ein Entwurf, den noch niemand sehen soll.

!!! info "Von echten Daten gestützt"
    Die Wissensdatenbank ist eine vollwertige Funktion im Backend (`/api/v1/articles`). Artikel liegen versioniert in deiner Datenbank und kommen wie alles andere über die API. Dadurch sind sie durchsuchbar, zugriffsgeschützt und immer aktuell.

## Smart Links

Beim Schreiben lösen **Smart Links** Verweise live auf:

- Erwähnst du einen Vorgang wie `MOB-42`, wird er zu einem Link mit dem aktuellen Titel und Status.
- Erwähnst du eine Person, verlinkt sie auf ihr Profil.

Ein Runbook, das auf `INF-7` verweist, zeigt also immer den aktuellen Vorgang.

## Zugriffssteuerung

Seiten sind über Projekt- und Teamrollen geschützt, wie der Rest von Hinata:

- Eine **Projektseite** liest, wer das Projekt sieht.
- Eine **Teamseite** lesen die Team-Admins und die Mitglieder, denen das Team sie geöffnet hat. Pro Mitglied gibt es drei Stufen: keine Seiten (die Voreinstellung), alle Seiten oder ausgewählte Seiten. Eine ausgewählte Seite schließt alles darunter ein.
- Eine Seite **ohne Projekt und Team** ist privat. Nur ihr Autor liest sie.

Sonst liest niemand eine Seite, auch Administratoren nicht. Den Seitenzugriff eines Mitglieds legen Team-Admins fest, wenn sie jemanden ins Team holen oder seine Rechte ändern. Andere Teammitglieder sehen nur, wie viele Seiten ein Kollege bekommen hat, aber nicht welche. Welche es sind, sehen die Team-Admins.

Private Seiten gehören zu deinen persönlichen Daten. Sie sind im Export deiner Daten enthalten und werden mit deinem Konto gelöscht. Das gilt auch für Seiten, die vor dem Update alle lesen konnten und jetzt privat für ihren Autor sind. Soll eine wichtige Seite bleiben, verschiebe sie in ein Projekt oder Team, bevor das Konto gelöscht wird.

### Seiten verschieben

Eine Seite an einen anderen Ort zu bringen, also in ein Projekt, in ein Team oder ins Private, braucht Rechte über den Ort, an dem sie jetzt liegt:

- Eine **Projektseite** verschieben die Projektleitungen und die Team-Admins eines Teams, dem das Projekt gehört.
- Eine **Teamseite** verschieben die Admins dieses Teams.
- Eine **private Seite** verschiebt ihr Autor.

Privat machen kann eine Seite nur ihr Autor.

Verschiebst du eine Seite, ziehen ihre Unterseiten mit. Unterseiten, die jemand von einem anderen Ort aus darunter abgelegt hat, bleiben aber, wo sie sind, und werden dort zu Seiten der obersten Ebene. Die private Seite einer Person zieht nie mit der Seite einer anderen Person um.

Einen Bereich löschen kannst du erst, wenn keine Seiten mehr darin liegen. Das gilt auch für Seiten, die du nicht sehen kannst.

!!! warning "Was sich beim Update ändert"
    Bestehende Seiten ohne Projekt und Team werden nach dem Update privat für ihre Autoren. Bestehende Teammitglieder haben zunächst keinen Zugriff auf die Seiten ihres Teams, bis ein Team-Admin sie ihnen öffnet. Seiten, die unter einer Seite von einem anderen Ort hingen, werden an ihrem eigenen Ort zu Seiten der obersten Ebene. Wurde der Autor einer Seite schon vor dem Update gelöscht, bleibt die Seite gespeichert, aber niemand kann sie lesen. Was damit geschieht, entscheidet der Betreiber. Soll eine Seite wieder für mehr Menschen lesbar sein, ordnet ihr Autor sie einem Projekt oder Team zu.

!!! tip "Verlinke Doku und Lieferung in beide Richtungen"
    Verweise im Kommentar eines Vorgangs auf einen Artikel und im Artikel auf den Vorgang. So bleibt die Wissensdatenbank lebendig.

## Nächste Schritte

- [Vorgänge](/de/issues.html): die Verweise, die Smart Links auflösen.
- [Projekte & Teams](/de/guide-projects.html): Team-Admins, Mitglieder und Seitenzugriff.
- [Befehlspalette](/de/search.html): alles schnell finden.
