---
title: Dein Konto
description: Profil, Anmeldung, 2FA, Sitzungen, Sprache und deine Daten in den Einstellungen.
---

# Dein Konto

Öffne **Einstellungen** unten in der Navigationsleiste oder klicke oben rechts auf
dein Profilbild. Dort findest du auch **Profil bearbeiten** und **Abmelden**. Auf
dem Handy liegt das Einstellungssymbol neben der Glocke.

![Der Einstellungsbildschirm von Hinata](/assets/img/shot-settings.png)
*Die Einstellungen auf dem Desktop.*

!!! tip "Auf dem Handy eine Liste"
    Jede Karte wird zu einer Zeile, die sich als eigene Seite öffnet. Welche
    Zeilen du siehst, hängt von deinem Konto ab. Der Zurückpfeil führt erst zur
    Liste und dann zurück.

![Die Einstellungen auf dem Handy als Liste von Bereichen](/assets/img/shot-mobile-settings-index.png)
*Die Einstellungen auf dem Handy.*

## Dein Profil

Das Banner oben zeigt, wie andere dich sehen: Bild, Anzeigename, `@Benutzername`,
Position, Rollen und den Monat, in dem du dazugekommen bist.

![Der Dialog „Profil bearbeiten“](/assets/img/shot-account-edit-profile.png)
*„Profil bearbeiten“ mit ausgegrautem „Benutzername“.*

- **Anzeigename**: steht auf Karten, in Kommentaren und in der
  Bearbeiterauswahl. Jederzeit änderbar.
- **Position**: freier Text, etwa „Maintainer“.
- **Benutzername**: nicht änderbar, weil `@`-Erwähnungen und alte Kommentare
  darauf verweisen.

### Dein Bild

Klicke auf das Kamerasymbol am Profilbild und wähle **Foto hochladen**. Erlaubt
sind JPEG, PNG, GIF und BMP bis 12 MB. Der Server speichert das Bild als JPEG mit
höchstens 512 Pixeln an der langen Kante.

**Foto entfernen** zeigt wieder deine farbigen Initialen.

## Deine Anmeldeadresse

Die Karte **E-Mail & Sicherheit** zeigt deine Anmeldeadresse als **Verifiziert**
oder **Nicht verifiziert**.

![Der Dialog „E-Mail ändern“](/assets/img/shot-account-change-email.png)
*Der Dialog hinter „Ändern“.*

1. Klicke auf **Ändern** und gib die neue Adresse ein.
2. Klicke auf den Link in der Mail. Bis dahin zeigt die Karte *Bestätigung
   ausstehend für …*, und die alte Adresse gilt weiter.
3. Nach der Bestätigung wirst du auf allen Geräten abgemeldet. Ein
   Sicherheitshinweis kommt in Glocke und Postfach.

!!! note "Mit Single Sign-on"
    Meldest du dich über einen Identitätsanbieter an, steht auf der Karte
    *E-Mail und Passwort werden von deinem Identitätsanbieter verwaltet*. Die
    Buttons zum Ändern und Zurücksetzen fehlen dann. Siehe
    [Single Sign-on](/de/sso.html).

## Dein Passwort

**Zurücksetzen** in der Zeile Passwort schickt dir einen einmaligen Link per
E-Mail. Er läuft nach 30 Minuten ab. Ein Formular zum Ändern gibt es nicht.

![Der Dialog „Passwort zurücksetzen“](/assets/img/shot-account-password-reset.png)
*Der Dialog mit „Link per E-Mail senden“.*

- Das neue Passwort braucht mindestens **10 Zeichen**. Sonderzeichen und Ziffern
  sind keine Pflicht. Vier normale Wörter sind sicherer als `P@ssw0rd!`.
- Danach bist du überall abgemeldet, auch auf dem aktuellen Gerät.

## Zwei-Faktor-Authentifizierung

Mit 2FA brauchst du beim Anmelden zusätzlich einen sechsstelligen Code aus einer
App auf dem Handy. Die Zeile zeigt **Aktivieren** oder *Aktiv · 10
Wiederherstellungscodes übrig*.

### Aktivieren

Drücke **Aktivieren**. Der Assistent dauert etwa eine Minute.

1. Scanne den QR-Code mit einer App wie Google Authenticator, 1Password oder
   Authy. Auf demselben Handy kopierst du den „Schlüssel zur manuellen Eingabe“.
2. Gib den sechsstelligen Code ein. „Bestätigen & aktivieren“ wird klickbar,
   sobald alle sechs Felder gefüllt sind.
3. **Wiederherstellungscodes speichern**: Du bekommst zehn Codes. Jeder ersetzt
   genau einmal den Code aus der App. **Alle kopieren** legt sie in die
   Zwischenablage.

![Schritt 1 mit QR-Code und Schlüssel zur manuellen Eingabe](/assets/img/shot-2fa-scan.png)
*Schritt 1, QR-Code und Schlüssel sind verpixelt.*

![Schritt 2 mit fünf von sechs gefüllten Feldern](/assets/img/shot-2fa-verify.png)
*Schritt 2, die letzte Ziffer fehlt noch.*

!!! warning "Die Codes siehst du nur einmal"
    Hinata speichert nur Hashes. Bewahre die Codes so auf, dass du ohne Handy
    herankommst, etwa im Passwortmanager oder ausgedruckt.

### Im Alltag

- Beim **Anmelden** fragt Hinata den Code nach dem Passwort ab. Er wechselt alle
  30 Sekunden. Ein gerade abgelaufener Code gilt noch kurz.
- **Codes** erzeugt zehn neue Wiederherstellungscodes und macht die alten
  ungültig. Dafür brauchst du einen aktuellen Code, also vor dem Handywechsel.
- **Deaktivieren** schaltet 2FA ab. Auch das braucht einen aktuellen Code oder
  einen Wiederherstellungscode.

## Aktive Sitzungen

Hier steht jedes angemeldete Gerät, das zuletzt aktive zuerst: Browser oder
Hinata-App, Betriebssystem, maskierte IP-Adresse und letzte Aktivität. Dein Gerät
ist als **Dieses Gerät** markiert.

- Der Pfeil in einer Zeile meldet dieses Gerät ab.
- **Andere abmelden** beendet sofort alle anderen Sitzungen.

### Was eine Sitzung von selbst beendet

Alle Geräte werden abgemeldet, wenn du dein Passwort zurücksetzt, eine neue
E-Mail-Adresse bestätigst oder dein Konto löschst. Dasselbe passiert, wenn ein
Administrator dein Konto deaktiviert. App schließen, Neustart oder Netzverlust
beenden keine Sitzung.

!!! tip "Gerät verloren oder fremder Eintrag?"
    Drücke zuerst **Andere abmelden** und setze danach dein Passwort
    **zurück**. So ist niemand mehr angemeldet, wenn das neue Passwort gilt.

Fremde Anmeldungen meldet dir die Benachrichtigung **Sicherheitshinweise** in
Glocke und Postfach. Siehe [Auf dem Laufenden bleiben](/de/guide-notifications.html).

## Sprache und Darstellung

Die Karte **Darstellung & App** enthält:

- **Sprache**: eine von [neun](/de/features.html#sprachen) (Englisch, Deutsch,
  Französisch, Spanisch, Russisch, Chinesisch, Japanisch, Hindi, Arabisch). Sie
  gilt sofort für die Oberfläche und für E-Mails und Fehlermeldungen des
  Servers. Mit Arabisch läuft das Layout von rechts nach links.
- **Darstellung**: **System**, **Hell** oder **Dunkel**. System folgt deinem
  Betriebssystem.
- **Verbundener Server**, daneben **Server verwalten**, wenn du mehrere nutzt.
  Siehe [Auf dem Handy](/de/guide-mobile.html#mehrere-server-eine-app).
- **Datenschutzerklärung**: der Datenschutzhinweis deines Betreibers und die
  Versionen von App und Server.

!!! note "Name und Logo kommen vom Server"
    Organisationsname und Logo oben links ändert ein Administrator für alle.
    Siehe [Adminbereich](/de/admin-area.html).

## Teams und Projekte, die du erreichst

Die Karte **Zugriff** ist nur eine Anzeige. Unter **Teams** und **Projekte**
siehst du, wo du Mitglied bist, mit Mitgliederzahl und deiner Rolle. Fehlt ein
Projekt, muss dich jemand zum passenden Team hinzufügen. Siehe
[Projekte & Teams](/de/guide-projects.html).

## Zugriffstokens

Hat dein Betreiber die Funktion aktiviert, erstellst du auf der Karte
**Zugriffstokens** Personal Access Tokens für KI-Assistenten und Skripte. Sie
dürfen nur, was du erlaubst. Das Geheimnis siehst du nur beim Erstellen. Fehlt
die Karte, ist die Funktion aus. Siehe [MCP-Server](/de/mcp.html).

## Deine Daten

Deine Rechte aus der DSGVO sind hier als Buttons umgesetzt.

### Eine Kopie exportieren (Art. 15)

**Daten & Datenschutz → Anfordern**. Innerhalb von 24 Stunden bekommst du eine
E-Mail mit einem sicheren Downloadlink, der drei Tage gilt. Du brauchst keinen
Grund, und niemand wird informiert.

### Konto löschen (Art. 17)

**Gefahrenzone → Konto löschen**. Zur Bestätigung tippst du genau DELETE ins
Feld.

![Der Dialog zum Kontolöschen mit leerem Feld](/assets/img/shot-account-delete-confirm.png)
*Die Bestätigung, noch ohne DELETE.*

!!! warning "Das lässt sich nicht rückgängig machen"
    Profil, Zugangsdaten und Sitzungen werden dauerhaft gelöscht. Du bist sofort
    überall abgemeldet und bekommst eine Bestätigung per E-Mail. Deine Vorgänge,
    Kommentare und Historie bleiben, aber **anonymisiert**. Es gibt keine
    Karenzzeit und keine Wiederherstellung.

    Willst du nur aus einem Projekt raus, bitte einen Administrator, dir den
    Zugriff zu entziehen.

Als **letzter aktiver Administrator** kannst du dein Konto nicht löschen. Mach
vorher jemand anderen zum Administrator.

## Nächste Schritte

- [Auf dem Laufenden bleiben](/de/guide-notifications.html): Benachrichtigungen einstellen
- [Erste Schritte](/de/guide-start.html): Anmelden und der erste Tag
- [Auf dem Handy](/de/guide-mobile.html): mobiles Layout und mehrere Server
- [Authentifizierung](/de/authentication.html): Passwörter und 2FA aus Sicht des Betreibers
