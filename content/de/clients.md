---
title: Die Apps
description: Wie sich die Hinata-App für Android, iOS, Web, macOS, Windows und Linux verbindet, anmeldet und mehrere Server verwaltet.
---

# Die Apps

Hinata hat einen einzigen Flutter-Client für **Android**, **iOS**, das **Web**,
**macOS**, **Windows** und **Linux**. Es gibt keine getrennte Mobil- und
Desktop-App. Dieselben Bildschirme, derselbe State und dieselbe Netzwerkschicht
passen sich an die Plattform an.

Diese Seite erklärt Verbindung, Versionssperre, Anmeldung, mehrere Server und
den Betrieb unter Linux.

![Hinata auf dem Smartphone](/assets/img/shot-mobile-dashboard.png)
*Eine App aus einer Flutter-Codebasis für sechs Plattformen.*

## Eine Codebasis, sechs Plattformen

Der Client nutzt Flutter, bloc/cubit für den State, go_router fürs Routing und
i18next für die Sprachen. Jeder Netzwerkaufruf läuft über einen `ApiClient` auf
Basis von **dio** (automatische Token-Erneuerung, `Accept-Language`-Header).
Eine neue Funktion landet damit überall gleichzeitig.

- **Responsiv:** Breakpoints aus dem Goldenen Schnitt statt fester Pixelbreiten.
  Dieselbe Oberfläche passt auf Telefon, Tablet, Desktopfenster und Browsertab.
- **Lokalisiert:** Oberfläche auf **Englisch** und **Deutsch** (i18next).
  Fehlermeldungen übersetzt **der Server**. Der Client schickt die Sprache per
  `Accept-Language`, der Server antwortet mit der fertigen Meldung.
- **Hell und dunkel:** navyblaue Navigationsleiste, warmer Papierton im
  Arbeitsbereich und der honigfarbene Akzent `#D9A032`, der in beiden Modi
  gleich wirkt. Glasflächen gibt es in der mobilen Navigation, der ⌘K-Palette
  und der Anhang-Lightbox.
- **Nativ auf dem Desktop:** echte native Builds statt eines Browsers im Rahmen.
  macOS, Windows (als MSIX) und Linux als **GTK-3**-Anwendung. Details unter
  [Hinata unter Linux](#hinata-unter-linux).

## So funktioniert es: vom Start bis zum Workspace

Jeder frische Start läuft in dieser Reihenfolge ab:

| Schritt | Was passiert |
| --- | --- |
| **Verbinden** | Beim ersten Start fragt die App nach deiner **Server-URL** und geht erst weiter, wenn der Server unter `/api/v1/meta` antwortet. |
| **Versionssperre** | Die App vergleicht ihre Version mit dem Minimum des Servers (`HINATA_APP_MIN_VERSION`, bereitgestellt als `minAppVersion`) und erzwingt ein Update, wenn der Client zu alt ist. |
| **Setup-Assistent** | Ein neuer Server wird direkt in der App eingerichtet (Organisationsname und erster Admin), außer er wurde mit `HINATA_SETUP_*` vorkonfiguriert. |
| **Onboarding** | Eine einmalige, illustrierte Tour durch die wichtigsten Funktionen. |
| **Anmelden** | Lokale Zugangsdaten oder **SSO** (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP). |

### Verbinden

Die native App fragt zuerst nach der Server-URL. Sie prüft `/api/v1/meta` und
geht erst weiter, wenn der Server antwortet. So landest du nie bei einem Host,
der kein Hinata-Server ist.

Früher genutzte Server stehen als Verknüpfungen unter dem URL-Feld. Nach einem
kurzen Ausfall verbindest du dich mit einem Tipp neu.

!!! info "Native Apps haben keine feste Server-URL"
    In einer veröffentlichten nativen App ist keine Serveradresse einkompiliert.
    Deshalb kann eine App jedem Hinata-Betreiber dienen. Nur der **Web**-Build
    darf standardmäßig seinen eigenen Origin nutzen (über `kIsWeb`), weil er
    ohnehin von einem bekannten Host kommt. Siehe
    [Multi-Server](#multi-server-eine-app-viele-server).

### Versionssperre

Bei jedem Start liest die App die Mindestversion vom Server. Ist die installierte
App älter, erscheint statt des Workspaces der Bildschirm **Update erforderlich**.

Betreiber setzen den Wert mit `HINATA_APP_MIN_VERSION` oder live im
[Adminbereich](/de/admin-area.html) → App-Einstellungen. Der Datenbankwert
gewinnt. So bringst du alle Clients auf einen neuen Build, sobald eine
inkompatible Änderung live geht, ohne Abstimmung auf Clientseite.

### Setup-Assistent

Zeigt die App auf einen frisch installierten Server, führt sie dich durch die
Ersteinrichtung: Name der Organisation und erstes Administratorkonto.

Ohne Assistent geht es mit `HINATA_SETUP_AUTO_COMPLETE=true` zusammen mit
`HINATA_SETUP_ORGANIZATION_NAME` und den Admin-Zugangsdaten. Siehe
[Setup & Erststart](/de/setup-wizard.html).

### Anmelden

Du meldest dich an mit:

- **Lokalen Zugangsdaten:** Benutzername oder E-Mail und Passwort.
  Selbstregistrierung, E-Mail-Verifizierung, Passwort vergessen und optionale
  Freigabe durch einen Admin laufen über Feature-Flags (siehe
  [Authentifizierung](/de/authentication.html)).
- **SSO:** OpenID Connect, OAuth 2.0, SAML 2.0 oder LDAP, eingerichtet im
  Adminbereich. Zurück in die App geht es über den Deep Link
  `hinata://auth-callback`. Siehe [Single Sign-on](/de/sso.html).

Ist für das Konto Zwei-Faktor-Authentifizierung (TOTP) aktiv, folgt nach dem
Passwort die Abfrage eines Einmalcodes.

## Multi-Server: eine App, viele Server

Eine Hinata-App spricht mit beliebig vielen unabhängigen Servern. Du wechselst
zwischen ihnen, ohne dich bei den anderen abzumelden.

- Jeden Server fügst du einmal hinzu, die App merkt ihn sich.
- Über den Umschalter wechselst du frei. Jeder Server behält seine eigene Sitzung.
- Access Tokens gelten nur für den Server, der sie ausgestellt hat. Beim Wechsel
  wandern keine Zugangsdaten zwischen Instanzen.

### Der Server-Manager

Im **Server-Manager** (im Glasdesign) verwaltest du deine gespeicherten Server.
Beim Öffnen prüft er alle **parallel**. Jede Zeile zeigt einen Live-Status mit
pulsierendem Punkt und echtem Ping in Millisekunden. Sie springt von *prüfe…*
auf *online* (mit Latenz) oder *offline*.

Im Manager kannst du:

- Einen Server **hinzufügen**. Vor dem Speichern läuft ein **Verbindungstest**,
  eine falsche oder nicht erreichbare URL fällt sofort auf.
- Name oder URL eines Servers **bearbeiten**.
- Einen Server, den du nicht mehr brauchst, **löschen**.
- Mit einem Tipp zu einem Online-Server **wechseln**.

!!! tip "Self-hosted oder Cloud nebeneinander"
    Jede Zeile hat ein Badge, damit du deine selbst gehostete Instanz sofort
    erkennst. Weil Tokens pro Server gelten, kannst du einen Server für die
    Arbeit und einen privaten bedenkenlos in derselben App halten.

## Woher du die App bekommst

| Du möchtest… | Verwende |
| --- | --- |
| **Einen Server einfach im Browser nutzen** | Die gehostete **Web-App**. Ein Betreiber stellt sie unter `https://track.example.com` bereit (Overlay `docker-compose.app.yml`). Keine Installation. |
| **Den Client selbst aus dem Quellcode ausführen** | Klone [hinata-app](https://github.com/hinata-platform/hinata-app), `flutter pub get`, `flutter run`. GPL-3.0. |
| **Eine gebrandete App in die Stores bringen** | Baue deinen **eigenen** Client, siehe [Branding & eigene Clients](/de/self-hosted-app.html). |

Die Store-Builds haben keine einkompilierte Server-URL. Du bringst deinen eigenen
Server mit, und eine veröffentlichte App dient über das
[Hinata Connect Gateway](/de/connect-gateway.html) jedem Betreiber.

Das Gateway leitet auch Push weiter: an FCM für Android, iOS und macOS, an WNS
für Windows. Unter Linux gibt es keinen solchen Dienst, der Linux-Build bekommt
also kein Push. Benachrichtigungen kommen dort in der App und per E-Mail an.

Linux gibt es über den **Snap Store**: `snap install hinata` installiert ein
strikt isoliertes Snap für amd64 und arm64 von
[snapcraft.io/hinata](https://snapcraft.io/hinata). Das **Flatpak**-Manifest und
das **AppImage**-Skript liegen im Repository, zum Selberbauen.

!!! note "Open Source, GPL-3.0"
    Die App steht unter **GPL-3.0**. Du darfst sie bauen, ändern und als eigenen
    gebrandeten Client ausliefern. Was du dafür änderst, steht im
    [Leitfaden für eigene Clients](/de/self-hosted-app.html).

## Hinata unter Linux

Linux ist ein vollwertiges Ziel. Die App ist eine native **GTK-3**-Anwendung mit
dem Binary `hinata` und der Application-ID `com.ahmadre.hinata`, gebaut aus
derselben Flutter-Codebasis wie Handy und Web. Anmeldung, SSO, Multi-Server,
Boards, Anhänge, Drucken und PDF-Export funktionieren wie überall.

### Installieren

| Format | Was du bekommst |
| --- | --- |
| **Snap** | Der Kanal, über den Hinata unter Linux ausgeliefert wird. `sudo snap install hinata` auf jeder Distribution mit snapd, für x86-64 und ARM64, strikt isoliert. Zwei Berechtigungen musst du selbst verbinden (siehe unten). |
| **Flatpak** | Baust und installierst du selbst: mit `flatpak-builder` aus dem Manifest in `packaging/linux/flatpak/`. Es liegt auf keinem gehosteten Flatpak-Remote und nicht auf Flathub. |
| **AppImage** | Eine portable Datei zum Selberbauen: `packaging/linux/appimage/build-appimage.sh` erzeugt sie aus einem Release-Bundle, dann `chmod +x` und starten. Sie ist nirgends veröffentlicht, die CI hängt sie nur an einen Workflow-Lauf und an kein Release. Sie linkt absichtlich gegen GTK, GStreamer und libsecret deines Systems und behält so dein Desktop-Theme und die Codecs deiner Distribution. |
| **Aus dem Quellcode** | `flutter build linux --release` erzeugt ein verschiebbares Bundle (Binary `hinata` plus `data/` und `lib/`), das du installieren kannst, wo du willst. |

!!! info "Zwei Berechtigungen brauchen einen Klick"
    Snap führt die App strikt isoliert aus. Zwei Schnittstellen verbinden sich
    nicht automatisch, weil ein Store diesen Zugriff bewusst erteilen lässt:

    ```bash
    sudo snap connect hinata:password-manager-service   # angemeldet bleiben
    sudo snap connect hinata:audio-record               # Sprachnachricht aufnehmen
    ```

    Ohne die erste läuft die App, speichert deine Sitzung aber nicht im
    Schlüsselbund. Jeder Neustart landet dann auf der Anmeldung. Ohne die zweite
    tut die Mikrofontaste nichts. Die App nennt die fehlende Berechtigung.
    Dieselben Schalter findest du in Ubuntus App Center unter „Berechtigungen“.

    Den verlässlichen Stand zeigt `snap info hinata`: welche Kanäle eine
    Revision haben und welcher Build dort liegt. **stable** (das liest ein
    einfaches `snap install hinata`) hat die veröffentlichte Version für beide
    Architekturen. **edge** hat den Build des letzten Tags. Er ist neuer als
    stable und weniger erprobt: `snap install hinata --edge`.

Alle drei Rezepte liegen in `packaging/linux/` in
[hinata-app](https://github.com/hinata-platform/hinata-app). Sie installieren
denselben Desktop-Eintrag, dasselbe Icon und dieselbe AppStream-Metainfo.

- Flatpak und AppImage verpacken ein vorher gebautes Bundle. `flatpak-builder`
  baut seine Module ohne Netzwerk, deshalb braucht das Flatpak ein fertiges
  Bundle.
- Das Snap führt den Flutter-Build selbst aus. Ein Snapcraft-Build-Schritt hat
  Netzwerk, und die Flutter-Engine-Artefakte und pdfium werden erst beim Build
  geladen.

AppImage und rohes Bundle entstehen auf einem fest gepinnten
`ubuntu-22.04`-Runner. Das legt ihre glibc-Untergrenze bewusst fest. Ein
Flutter-Bundle ist dynamisch gegen die glibc des Build-Systems gelinkt, und glibc
ist nur vorwärtskompatibel. Auf einem neueren Runner gebaut, würde die Binary auf
älteren Distributionen nicht starten. Das Snap braucht diesen Pin nicht, seine
libc kommt aus der `core24`-Base.

!!! note "Nicht auf Flathub"
    Hinata wird nicht auf Flathub angeboten. Unter Linux kommt die App über den
    Snap Store. Flatpak-Manifest und AppImage-Skript sind zum Selberbauen da.

So baust du selbst unter Debian oder Ubuntu:

```bash
sudo apt install \
  clang cmake ninja-build pkg-config \
  libgtk-3-dev liblzma-dev libsecret-1-dev libjsoncpp-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

flutter config --enable-linux-desktop
flutter build linux --release
```

### Deep Links landen im Fenster, aus dem du gestartet bist

Der Desktop-Eintrag registriert das Schema `x-scheme-handler/hinata`. Die App
läuft als **Single-Instance**-GTK-Anwendung. Ein zweiter Start von `hinata` gibt
seine Argumente an die laufende Kopie weiter und öffnet kein zweites Fenster.

Deshalb funktioniert `hinata://auth-callback`. SSO-Rückkehr, Einladung oder Link
zum Zurücksetzen des Passworts kommen in deinem Fenster an, egal ob die App schon
offen war oder erst durch den Link startet.

### Was unter Linux anders ist

Zwei Dinge fehlen unter Linux. Einige weitere brauchen Programme, die deine
Distribution vielleicht nicht installiert hat.

| Bereich | Unter Linux | Warum |
| --- | --- | --- |
| **Push-Benachrichtigungen** | Nicht verfügbar. Benachrichtigungen kommen **in der App** und **per E-Mail**. | `firebase_messaging` hat keine Linux-Implementierung, und es gibt keinen Desktop-Push-Dienst, bei dem sich ein Token registrieren ließe. Nichts übernimmt die Rolle von FCM auf Mobilgeräten oder WNS unter Windows. |
| **Kameraaufnahme** | *Foto aufnehmen* wird nicht angeboten. Vorhandene Bilder oder Dateien anhängen geht normal. | Für Linux gibt es keine Kamera-Implementierung. Ein Eintrag, der nur einen Fehlerdialog zeigen könnte, bleibt weg. |
| **Angemeldet bleiben** | Braucht einen Schlüsselbund, siehe Hinweis unten. | Sitzungs-Tokens werden über den freedesktop Secret Service gespeichert. |
| **Sprachkommentare** | Die Wiedergabe braucht die GStreamer-Plugin-Pakete, die Aufnahme `pulseaudio-utils` und `ffmpeg`. | `just_audio` hat keine Linux-Implementierung, die Wiedergabe läuft über ein eigens geschriebenes GStreamer-Plugin. Der Recorder erzeugt AAC, deshalb ist `gstreamer1.0-libav` Pflicht. |
| **Dateiauswahl für Anhänge** | Nutzt `zenity`, `qarma` oder `kdialog`. Fehlen alle, nennt die App die Programme, die du installieren kannst. | Die Flutter-Dateiauswahl hat kein natives Linux-Backend und steuert einen dieser Dialoge an. |
| **Downloads** | Ein Anhang landet direkt im Downloads-Ordner, ein Toast nennt die Datei. | Linux hat kein Teilen-Menü, also sagt dir die App, wo die Datei liegt. |

Deine **Benachrichtigungseinstellungen bleiben** unter Linux **sichtbar und
bearbeitbar**, obwohl dort nie ein Push kommt. Sie gehören zu deinem Konto und
steuern auch dein Handy.

!!! warning "Angemeldet bleiben braucht einen Schlüsselbund"
    Hinata speichert Sitzungs-Tokens über den freedesktop **Secret Service** im
    Schlüsselbund, also in GNOME Keyring, KWallet oder etwas Kompatiblem. Ein
    minimaler Fenstermanager, ein Container oder eine SSH-Sitzung auf einen
    Desktop mit nie entsperrtem Schlüsselbund hat keinen solchen Speicher.

    Die Anmeldung klappt trotzdem, die Sitzung hält aber nur bis zum Schließen
    der App. Das sagt dir die App sofort.

    ```bash
    sudo apt install gnome-keyring     # Debian / Ubuntu
    sudo dnf install gnome-keyring     # Fedora
    ```

Auf einer normalen Desktop-Installation funktioniert alles aus der Tabelle. Auf
einem schlanken System (Container, nackter Fenstermanager) ist das die
vollständige Liste:

```bash
sudo apt install \
  gnome-keyring zenity \
  pulseaudio-utils ffmpeg \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-libav
```

!!! tip "Die fertigen Pakete bringen das meiste mit"
    Die Flatpak-Runtime enthält GTK, `zenity`, FFmpeg und die GStreamer-Plugins.
    Auf dem Host braucht ein Flatpak nur noch einen Schlüsselbund.

    Das Snap bringt FFmpeg, die Aufnahmewerkzeuge von PulseAudio und die
    zusätzlichen GStreamer-Plugins selbst mit. Dateien wählt es über das
    Desktop-Portal statt über `zenity`. Zwei Berechtigungen reichen an
    Schlüsselbund und Mikrofon und verbinden sich deshalb nicht von allein:

    ```bash
    sudo snap connect hinata:password-manager-service   # angemeldet bleiben
    sudo snap connect hinata:audio-record               # Sprachkommentare aufnehmen
    ```

## Wie es weitergeht

- [Branding & eigene Clients](/de/self-hosted-app.html): Laufzeit-Branding oder dein eigener Client.
- [Authentifizierung](/de/authentication.html): lokale Konten, Registrierung, 2FA.
- [Single Sign-on](/de/sso.html): einen Identitätsanbieter anbinden.
- [Setup & Erststart](/de/setup-wizard.html): einen frischen Server einrichten.
