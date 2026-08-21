---
title: Dein Konto
description: Alles auf deinem Einstellungs-Bildschirm — Profil und Profilbild, E-Mail und Passwort, Zwei-Faktor-Authentifizierung, aktive Sitzungen, Sprache und Design sowie Datenexport und Kontolöschung.
---

# Dein Konto

Deine Kontoeinstellungen sind der einzige Bildschirm in Hinata, bei dem es
ausschließlich um *dich* geht und nicht um die Arbeit. Dein Name und dein Bild,
wie Kolleginnen und Kollegen sie sehen; wie du dich anmeldest; welche Geräte
gerade angemeldet sind; in welcher Sprache die App mit dir spricht; und was mit
deinen Daten passiert, wenn du gehst.

Du öffnest sie über **Einstellungen** unten in der Navigationsleiste oder über
dein Profilbild oben rechts — dieses Menü hat außerdem ein schnelles
**Profil bearbeiten** und **Abmelden**. Auf dem Handy sitzt das
Einstellungs-Symbol neben der Glocke in der oberen Leiste.

![Der Einstellungs-Bildschirm von Hinata](/assets/img/shot-settings.png)
*Die Einstellungen auf dem Desktop. Oben läuft das Profil-Banner mit „Profil bearbeiten“ und „Abmelden“. Darunter teilt sich die Seite: links beginnen E-Mail & Sicherheit und Aktive Sitzungen, rechts Zugriff und Darstellung & App. Deine Benachrichtigungsmatrix und die Datenfunktionen laufen in denselben zwei Spalten unterhalb des sichtbaren Bereichs weiter.*

!!! tip "Auf dem Handy ist das eine Liste, keine Wand"
    Schmale Bildschirme machen aus demselben Inhalt ein Verzeichnis, und jeder
    Eintrag öffnet sich als eigene Seite. Der Zurück-Pfeil bringt dich erst
    zurück ins Verzeichnis und dann dorthin, wo du hergekommen bist.

![Die Einstellungen auf dem Handy: das Profil-Banner über einer Liste von Bereichen](/assets/img/shot-mobile-settings-index.png)
*Die Einstellungen auf dem Handy. Das Profil-Banner behält „Profil bearbeiten“ und „Abmelden“; darunter wird jede Karte des Desktop-Bildschirms zu einer Zeile — „E-Mail & Sicherheit“, „Aktive Sitzungen“, „Benachrichtigungen“, „Zugriff“, „Darstellung & App“ und für Administratoren „Adminbereich“. Welche Zeilen du bekommst, hängt von deinem Konto ab.*

## Dein Profil

Das Banner ganz oben zeigt, wie alle anderen dich sehen: dein Bild, deinen
Anzeigenamen, deinen `@Benutzernamen`, deine Position, deine Rollen und den
Monat, in dem du dazugekommen bist.

![Der Dialog „Profil bearbeiten“ mit ausgegrautem Feld „Benutzername“](/assets/img/shot-account-edit-profile.png)
*„Profil bearbeiten“ öffnet sich über dem Einstellungs-Bildschirm. „Anzeigename“ und „Position“ sind änderbar; „Benutzername“ liegt ausgegraut dazwischen, und die Unterzeile sagt, warum.*

Dein Anzeigename ist das, was Kolleginnen und Kollegen auf Karten, in Kommentaren
und in der Bearbeiter-Auswahl sehen — ihn zu ändern kostet nichts. Die Position
ist freier Text: „Maintainer“, „Design-Leitung“, „Werkstudentin“ — was auch immer
jemandem hilft zu entscheiden, ob er dich fragen sollte.

Der **Benutzername lässt sich nicht ändern**, weil `@`-Erwähnungen darauf auflösen
und alte Kommentare weiter darauf zeigen. Ihn verschieben zu lassen würde die
Geschichte still umschreiben.

### Dein Bild

Klicke auf das kleine Kamera-Abzeichen an deinem Profilbild oder öffne die Zeile
für das Profilbild und wähle **Foto hochladen**. JPEG, PNG, GIF und BMP werden
akzeptiert, bis 12 MB — ein Foto direkt vom Handy ist also kein Problem. Der
Server verkleinert alles auf höchstens 512 Pixel an der langen Kante und legt es
als JPEG ab; aus einem 9-MB-Upload wird also kein 9-MB-Download für alle, die
das Board öffnen.

**Foto entfernen** setzt dich auf die farbigen Initialen zurück, die Hinata aus
deinem Namen erzeugt. Kein Foto zu haben, wird nicht bestraft — aber ein Board
voller Initialen ist tatsächlich schwerer zu überfliegen als eines voller
Gesichter.

## Deine Anmeldeadresse

Die Karte **E-Mail & Sicherheit** beginnt mit der Adresse, mit der du dich
anmeldest, markiert als **Verifiziert** oder **Nicht verifiziert**.

![Der Dialog „E-Mail ändern“, mit der aktuellen Adresse schreibgeschützt über der neuen](/assets/img/shot-account-change-email.png)
*„Ändern“ in der Zeile E-Mail öffnet diesen Dialog. Die aktuelle Adresse steht schreibgeschützt über der neuen, und die Unterzeile trägt die Zusage: Deine Anmelde-E-Mail ändert sich erst nach der Bestätigung.*

Bis du den Link in dieser Mail anklickst, zeigt die Karte *Bestätigung ausstehend
für …*, und nichts hat sich bewegt. Ein Tippfehler kostet dich also nichts — du
bestätigst schlicht nie.

In dem Moment, in dem du *doch* bestätigst, passieren zwei Dinge: Jedes Gerät,
das an deinem Konto angemeldet ist, wird abgemeldet, und ein Sicherheitshinweis
landet in deiner Glocke und in deinem Postfach. Eine Adressänderung ist eine
Änderung daran, wie das Konto wiederhergestellt wird — Hinata behandelt sie
entsprechend.

!!! note "Es sei denn, deine Organisation nutzt Single Sign-on"
    Meldest du dich über einen Identitätsanbieter an, sagt die Karte das —
    *E-Mail und Passwort werden von deinem Identitätsanbieter verwaltet* — und
    die Buttons zum Ändern und Zurücksetzen sind weg. Beides lebt dort, wo die
    Konten deiner Organisation leben. [Single Sign-on](/de/sso.html) beschreibt
    die Konstruktion.

## Dein Passwort

Hinata fragt dich nicht in einem Formular nach deinem alten Passwort.

![Der Bestätigungsdialog „Passwort zurücksetzen“](/assets/img/shot-account-password-reset.png)
*„Zurücksetzen“ in der Zeile Passwort öffnet kein Formular zum Ändern. Es öffnet dies: eine Zeile, dass ein einmaliger Link in dein Postfach geht und nach 30 Minuten abläuft, und einen einzigen Knopf „Link per E-Mail senden“.*

Das ist Absicht. Ein Passwort-ändern-Formular in einer angemeldeten Sitzung
schützt nichts, wenn jemand an deinem entsperrten Laptop sitzt. Ein Link ins
Postfach bedeutet, dass wer das Passwort ändert, auch das Postfach kontrollieren
muss.

Neue Passwörter müssen mindestens **10 Zeichen** lang sein. Ein abgeschlossenes
Zurücksetzen meldet dich außerdem überall ab — auch in der Sitzung, aus der du
es gestartet hast. Das Erste danach ist also die Anmeldung mit dem neuen
Passwort.

!!! tip "Länge schlägt Sonderzeichen"
    Vier gewöhnliche Wörter, die du dir wirklich merkst, schlagen `P@ssw0rd!` in
    jeder Hinsicht, die zählt. Nichts in Hinata verlangt ein Symbol oder eine
    Ziffer — verlangt wird Länge, weil genau die das Raten teuer macht.

## Zwei-Faktor-Authentifizierung

Mit aktivierter Zwei-Faktor-Authentifizierung braucht die Anmeldung dein Passwort
*und* einen sechsstelligen Code aus einer App auf deinem Handy. Wer das Passwort
stiehlt, kommt trotzdem nicht hinein.

Die Zeile zeigt **Aktivieren**, solange es aus ist, und *Aktiv · 10
Wiederherstellungscodes übrig*, wenn es an ist.

### Aktivieren

Drücke **Aktivieren**. Der Assistent hat drei Schritte und dauert etwa eine
Minute.

![Schritt 1 des Zwei-Faktor-Assistenten, mit QR-Code und Schlüssel zur manuellen Eingabe](/assets/img/shot-2fa-scan.png)
*Schritt 1 von 3. Scanne den Code mit einer Authenticator-App — Google Authenticator, 1Password, Authy. Sitzt du gerade auf genau dem Handy, das scannen würde, kopiere stattdessen den „Schlüssel zur manuellen Eingabe“ darunter. Beides ist hier verpixelt: Es ist ein echtes Geheimnis, und ein funktionierendes gehört nicht auf eine Webseite.*

![Schritt 2 des Zwei-Faktor-Assistenten, fünf der sechs Felder gefüllt](/assets/img/shot-2fa-verify.png)
*Schritt 2 von 3 sind sechs einzelne Felder statt eines Textfelds, und der Cursor springt von selbst weiter. „Bestätigen & aktivieren“ bleibt ausgegraut, bis alle sechs gefüllt sind — hier fehlt noch das letzte.*

Schritt 2 gibt es, damit bewiesen ist, dass deine Authenticator-App das richtige
Geheimnis wirklich gespeichert hat, bevor Hinata anfängt, es zu verlangen. Genau
das verhindert, dass du dich aus einem Konto aussperrst, das du nie sauber
eingerichtet hast.

**Schritt 3 von 3 · Wiederherstellungscodes speichern.** Du bekommst **zehn
einmalig verwendbare Codes**. Jeder funktioniert genau einmal anstelle des
sechsstelligen Codes, falls du den Zugriff auf deine Authenticator-App
verlierst. **Alle kopieren** legt sie in die Zwischenablage.

!!! warning "Die Wiederherstellungscodes werden genau einmal angezeigt"
    Hinata zeigt sie nie wieder an — es speichert nur Hashes und kann es
    schlicht nicht. Leg sie dorthin, wo du noch herankommst, wenn ausgerechnet
    das Handy fehlt: in einen Passwort-Manager, als Ausdruck in eine Schublade.
    Nicht als Notiz auf demselben Handy.

### Im Alltag

- **Beim Anmelden** wird der Code als zweiter Schritt nach dem Passwort
  abgefragt. Er wechselt alle 30 Sekunden; ein gerade abgelaufener Code wird
  noch einen Moment akzeptiert, damit langsames Tippen nicht bestraft wird.
- **Codes** erzeugt einen frischen Satz von zehn und macht die alten ungültig.
  Dafür brauchst du einen aktuellen Code — genau deshalb lohnt es sich *vor* dem
  Handywechsel und nicht danach.
- **Deaktivieren** schaltet es ab. Auch das verlangt einen aktuellen Code oder
  einen Wiederherstellungscode: Eine Sicherheitsfunktion abzuschalten muss so
  aufwendig sein wie sie zu benutzen.

## Aktive Sitzungen

Jedes an deinem Konto angemeldete Gerät steht hier, die zuletzt aktive Sitzung
zuerst: was es ist (ein Browser, die Hinata-App), das Betriebssystem, eine
maskierte IP-Adresse und wann es zuletzt aktiv war. Das Gerät, an dem du gerade
sitzt, ist als **Dieses Gerät** markiert.

Zwei Wege, auf die Liste zu reagieren:

- Der **Abmelden-Pfeil** in einer Zeile beendet genau diese Sitzung. Das Gerät
  muss sich beim nächsten Versuch neu anmelden.
- **Andere abmelden** beendet sofort jede Sitzung außer dieser.

### Was eine Sitzung von selbst beendet

- **Ein abgeschlossenes Zurücksetzen des Passworts** meldet jedes Gerät ab.
- **Eine bestätigte E-Mail-Änderung** meldet jedes Gerät ab.
- **Ein Administrator, der dein Konto deaktiviert**, meldet jedes Gerät ab.
- **Das Löschen deines Kontos** meldet jedes Gerät ab, endgültig.

Alles andere — die App schließen, den Rechner neu starten, das Netz verlieren —
lässt die Sitzung unberührt. Genau deshalb lohnt ab und zu ein Blick in die
Liste: Sitzungen laufen nicht aus Ordnungsliebe ab.

!!! tip "Der Ein-Minuten-Sicherheitscheck"
    Laptop verloren, eine Sitzung auf einem geteilten Rechner offen gelassen
    oder einen Eintrag schlicht nicht wiedererkannt? Drücke
    **Andere abmelden** und setze danach dein Passwort **zurück**. In dieser
    Reihenfolge — erst abmelden heißt, dass das neue Passwort auf einem Konto
    landet, an dem niemand mehr die Tür aufhält.

Bei Sitzungen zahlt sich auch die Benachrichtigung **Sicherheitshinweise** aus:
Eine Anmeldung, die nicht von dir kam, taucht in deiner Glocke und in deinem
Postfach auf — und dieser Bildschirm ist der nächste, den du dann öffnest. Siehe
[Auf dem Laufenden bleiben](/de/guide-notifications.html).

## Sprache und Darstellung

Die Karte **Darstellung & App** enthält die kleinen Entscheidungen:

- **Sprache** — Englisch oder Deutsch. Sie ändert die Oberfläche sofort und ist
  zugleich die Sprache, in der der Server dir E-Mails schickt und Fehlermeldungen
  zurückgibt. Eine Einstellung, überall.
- **Darstellung** — **System**, **Hell** oder **Dunkel**. System folgt dem, was
  dein Betriebssystem tut, inklusive Umschalten bei Sonnenuntergang, wenn dein
  System das macht.
- **Der verbundene Server** — mit welchem Server diese App spricht, daneben
  **Server verwalten**, falls du mehrere nutzt. Siehe
  [Auf dem Handy](/de/guide-mobile.html#mehrere-server-eine-app).
- **Datenschutzerklärung** — der Datenschutzhinweis deines Betreibers sowie die
  Versionsnummern von App und Server, praktisch beim Melden eines Problems.

!!! note "Das Branding deines Betreibers, kein Theme"
    Organisationsname und Logo oben links kommen vom Server, nicht aus deinen
    Einstellungen. Sie ändern sich für alle gleichzeitig, wenn ein Administrator
    sie ändert — siehe [Adminbereich](/de/admin-area.html), falls du das bist.

## Teams und Projekte, die du erreichst

Die Karte **Zugriff** ist reine Anzeige und beantwortet eine Frage, die sonst
ärgerlich schwer zu beantworten ist: *Wovon bin ich eigentlich Mitglied?*
Wechsle zwischen **Teams** und **Projekte**; jede Zeile zeigt Name,
Mitgliederzahl und deine Rolle dort.

Wenn eine Kollegin schwört, dass es ein Projekt gibt, und du es nicht findest,
schau zuerst hier. Eine leere Liste ist kein Fehler — Projektsichtbarkeit kommt
über Teammitgliedschaft, und jemand muss dich hinzufügen.
[Projekte & Teams](/de/guide-projects.html) erklärt, wie das funktioniert.

## Zugriffstokens

Hat dein Betreiber es aktiviert, erscheint eine Karte **Zugriffstokens**. Sie
stellt Personal Access Tokens aus, mit denen KI-Assistenten und Skripte in
deinem Namen mit Hinata arbeiten können — begrenzt auf das, was du ihnen
erlaubst. Das Geheimnis wird einmal beim Erstellen angezeigt und danach nie
wieder.

Siehst du die Karte nicht, ist die Funktion auf deinem Server abgeschaltet, und
du musst nichts tun. [MCP-Server](/de/mcp.html) hat die Details für alle, bei
denen sie an ist.

## Deine Daten

Die letzten beiden Karten sind deine Rechte nach der DSGVO — als Buttons
verdrahtet statt als E-Mail-Adresse, an die du schreiben müsstest.

### Eine Kopie exportieren (Art. 15)

**Daten & Datenschutz → Anfordern** bittet den Server, alles zusammenzustellen,
was er über dich weiß. Du bekommst eine E-Mail mit einem sicheren Download-Link;
der Bericht wird innerhalb von 24 Stunden erstellt, und der Link bleibt drei Tage
gültig.

Du brauchst keinen Grund, und niemand wird darüber informiert, dass du gefragt
hast.

### Konto löschen (Art. 17)

**Gefahrenzone → Konto löschen** löscht dein Konto.

![Der Dialog zum Kontolöschen mit leerem Bestätigungsfeld und deaktiviertem Knopf](/assets/img/shot-account-delete-confirm.png)
*Die Bestätigung. „Konto löschen“ bleibt wirkungslos, bis im Feld genau DELETE steht — und der Satz darüber ist der, den man zuerst liest: Profil, Zugangsdaten und Sitzungen gehen, erstellte Vorgänge und Kommentare werden anonymisiert.*

!!! warning "Das lässt sich nicht rückgängig machen"
    Das Löschen deines Kontos entfernt dauerhaft dein Profil, deine Zugangsdaten
    und jede offene Sitzung — du bist in dem Moment überall abgemeldet, und eine
    Bestätigung geht dir per E-Mail zu.

    Die **von dir erstellte Arbeit wird nicht gelöscht** — Vorgänge, Kommentare
    und Historie bleiben, damit die Aufzeichnungen deines Teams keine Löcher
    bekommen —, aber sie wird **anonymisiert**: Dein Name kommt herunter und
    lässt sich nicht wieder anbringen. Es gibt kein Rückgängig, keine Karenzzeit
    und keine Wiederherstellung. Willst du dich nur aus einem Projekt
    zurückziehen, bitte stattdessen einen Administrator, dir den Zugriff zu
    entziehen.

Ein Fall, in dem der Button sich weigert: Bist du der **letzte aktive
Administrator** des Workspace, lässt Hinata dich nicht löschen. Jemand muss die
anderen wieder hereinlassen können. Gib zuerst jemand anderem Administrator-Rechte
und lösche dann.

## Nächste Schritte

- [Auf dem Laufenden bleiben](/de/guide-notifications.html) — die
  Benachrichtigungsmatrix, die auf demselben Bildschirm sitzt.
- [Erste Schritte](/de/guide-start.html) — Anmelden, das Layout und was am
  ersten Tag zu tun ist.
- [Auf dem Handy](/de/guide-mobile.html) — dieser Bildschirm im mobilen Layout
  und wie sich mehrere Server eine App teilen.
- [Authentifizierung](/de/authentication.html) — die Betreibersicht auf
  Passwörter, Registrierung und 2FA-Richtlinien.
