---
title: Vorgänge teilen
description: Einen Vorgang mit einer Person außerhalb des Projekts teilen, die ihn lesen und kommentieren soll.
---

# Vorgänge teilen

Manchmal muss jemand einen einzelnen Vorgang verfolgen, der weder im Projekt noch in einem berechtigten Team ist. Die Referentin, die bei der IT eine eSIM bestellt hat, soll Rückfragen beantworten können, ohne das ganze IT-Projekt zu sehen. Dafür teilst du genau diesen Vorgang mit ihr. Sie ist dann **beteiligt**.

## Was Beteiligte können

| Aktion | Mitglied | Beteiligte |
| --- | --- | --- |
| Vorgang lesen, Verlauf und Anhänge ansehen | ja | ja |
| Kommentieren, antworten, reagieren, Sprachnachricht schicken, Anhang hochladen | ja | ja |
| Eigenen Kommentar bearbeiten oder löschen | ja | ja |
| Felder ändern, verschieben, archivieren, löschen, klonen | ja | nein |
| Bearbeiter des Vorgangs werden | ja | nein |
| Zeit buchen | ja | nein |
| Beobachten, exportieren | ja | ja |
| Weitere Personen beteiligen | ja | nein, nur sich selbst entfernen |

![Ein Vorgang aus Sicht einer Beteiligten, mit dem Hinweis oben](/assets/img/shot-sharing-participant.png)
*Lena ist an INF-2 beteiligt und sieht das Projekt Infrastructure nicht.*

Beteiligte sehen vom Projekt nur, was der Vorgang zum Anzeigen braucht: Name, Schlüssel, Status und Stichwörter. Projektseite, Board, Sprints, andere Vorgänge, Berichte, die Mitgliederliste und gebuchte Zeiten bleiben für sie unsichtbar. Verknüpfte Vorgänge und übergeordnete Epics erscheinen nur, wenn sie selbst mit ihnen geteilt sind.

## Einen Vorgang teilen

1. Öffne den Vorgang und tippe oben rechts auf **⋯**.
2. Wähle **Teilen mit …**.

![Das Menü ⋯ eines Vorgangs mit Teilen mit …](/assets/img/shot-sharing-menu.png)
*Teilen mit … steht im Menü ⋯ des Vorgangs.*

3. Suche die Person über das Feld **Person suchen …** und tippe auf sie.

![Die Suche im Dialog zum Teilen](/assets/img/shot-sharing-search.png)
*Ein Tipp auf die Person teilt den Vorgang mit ihr.*

Sie steht dann unter **Beteiligte**, mit dem Hinweis, wer sie wann beteiligt hat. Darunter siehst du die Mitglieder, die den Vorgang ohnehin sehen.

![Der Dialog zum Teilen mit zwei Beteiligten und den Mitgliedern darunter](/assets/img/shot-sharing-dialog.png)
*Beteiligte mit dem Hinweis, wer sie beteiligt hat, darunter die Mitglieder.* Ein Vorgang lässt sich mit höchstens 25 Personen teilen. Infrage kommen alle aktiven Konten deiner Organisation. Wer kein Konto hat, erreicht euch weiter über [E-Mail zu Vorgang](/de/email-to-ticket).

Teilen dürfen alle, die im Projekt mitarbeiten. Wählst du jemanden, der schon Mitglied ist, ändert sich nichts.

### Zwei Abkürzungen

- **Erwähnung im Kommentar:** Erwähnst du mit `@` jemanden, der den Vorgang nicht sehen kann, erscheint unter dem Kommentarfeld ein Hinweis. **Beteiligen** öffnet den Dialog mit der Person.
- **Zuweisen:** Wer das Projekt nicht öffnen kann, kann den Vorgang nicht übernehmen. Statt einer Fehlermeldung bietet Hinata an, die Person zu beteiligen.

## Was die beteiligte Person bekommt

Sie erhält eine Mitteilung „… hat dich an INF-2 beteiligt“. Die Glocke klingelt immer; Push und E-Mail richten sich nach ihrer Einstellung **Zuweisungen**. Ab dann beobachtet sie den Vorgang und hört von Kommentaren und Änderungen wie jede Beobachterin.

![Lenas Mitteilungen mit der Beteiligung und einem neuen Kommentar](/assets/img/shot-sharing-notification.png)
*Beteiligung und erster Kommentar in Lenas Mitteilungen.*

Den Vorgang findet sie unter **Beobachtet**, in der Liste **Issues** und in der Suche. Im Vorgang steht oben ein Hinweis, dass sie beteiligt ist und das Projekt nicht sieht. Wer in gar keinem Projekt ist, bekommt auf der leeren Seite **Issues** einen Verweis auf **Beobachtet**.

![Die Seite Beobachtet mit dem geteilten Vorgang oben](/assets/img/shot-sharing-watched.png)
*Geteilte Vorgänge stehen unter Beobachtet.*

## Beteiligung beenden

- Mitglieder öffnen **Teilen mit …** und tippen bei der Person auf **Entfernen**.
- Beteiligte tippen im Hinweis oben im Vorgang auf **Verlassen** und bestätigen.

![Die Rückfrage vor dem Verlassen eines Vorgangs](/assets/img/shot-sharing-leave.png)
*Vor dem Verlassen fragt Hinata noch einmal nach.*

Danach sieht die Person den Vorgang nicht mehr, ihr Abonnement endet, und schon gesammelte Mails werden verworfen. Eine Zuweisung bleibt davon unberührt.

## Was festgehalten wird

Jede Beteiligung und jedes Entfernen steht im **Verlauf** des Vorgangs („… hat Lena Vogt beteiligt“) und im Audit-Log der Organisation.

![Der Reiter Verlauf des Vorgangs mit der Beteiligung](/assets/img/shot-sharing-history.png)
*Die Beteiligung im Verlauf des Vorgangs.* Wird ein Konto gelöscht, verschwindet es aus allen Beteiligungen. Wird ein Vorgang verschoben, bleiben die Beteiligten dabei.

!!! note "Kein Hinweis am Vorgang"
    Für Mitglieder sieht ein geteilter Vorgang aus wie jeder andere. Wer beteiligt ist, zeigt der Dialog **Teilen mit …**.
