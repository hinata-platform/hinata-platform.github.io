---
title: Die Apps
description: Eine Flutter-Codebasis für Android, iOS, Web, macOS, Windows und Linux — wie sich der Client verbindet, Versionen sperrt, sich anmeldet und mehrere Server aus einem Liquid-Glass-Server-Manager verwaltet.
---

# Die Apps

Hinata liefert einen einzigen Flutter-Client, der aus **einer Codebasis** auf
**Android**, **iOS**, im **Web** und auf allen drei Desktops — **macOS**,
**Windows** und **Linux** — läuft. Es gibt keine separate Mobil- und Desktop-App,
die synchron gehalten werden müssten — dieselben Bildschirme, derselbe State,
dieselbe Netzwerkschicht passen sich an, worauf auch immer sie laufen. Diese
Seite erklärt, wie sich die App mit deinem Server verbindet, wie sie entscheidet,
ob sie aktuell ist, wie du dich anmeldest, wie eine einzige App mit vielen
Servern gleichzeitig spricht und was du wissen solltest, wenn du sie unter Linux
betreibst.


![Hinata auf dem Smartphone](/assets/img/shot-mobile-dashboard.png)
*Eine Flutter-Codebasis — Android, iOS, Web, macOS, Windows und Linux aus einer App.*

## Eine Codebasis, sechs Plattformen

Der Client ist mit Flutter gebaut. Der State wird mit bloc/cubit verwaltet, das
Routing mit go_router, die Lokalisierung mit i18next, und jeder Netzwerkaufruf
läuft über einen einzigen `ApiClient` auf Basis von **dio** (automatische
Token-Erneuerung, `Accept-Language`-Header). Weil es nur eine Codebasis gibt,
landet eine Funktion überall auf einmal.

- **Responsiv von Grund auf.** Das Layout passt sich über aus dem Goldenen Schnitt
  abgeleitete Breakpoints an, statt über feste Pixelbreiten, sodass dieselbe
  Oberfläche sauber vom Telefon zum Tablet zum Desktop-Fenster zum Browser-Tab
  umfließt.
- **Lokalisiert.** Die Oberfläche gibt es in **Englisch** und **Deutsch**
  (i18next), und Fehlermeldungen werden **vom Server** über den
  `Accept-Language`-Header lokalisiert — der Client sendet die Sprache des
  Benutzers, der Server gibt die bereits übersetzte Meldung zurück.
- **Hell & dunkel.** Eine navyblaue Navigationsleiste, ein warmes
  Papier-Workspace und der charakteristische Honig-Amber-Akzent `#D9A032`, der im
  hellen und dunklen Modus identisch wirkt, mit Liquid-Glass-Oberflächen auf der
  mobilen Navigation, der ⌘K-Palette und der Anhang-Lightbox.
- **Nativ auf dem Desktop.** Die drei Desktop-Ziele sind echte native Builds und
  kein Browser im Rahmen: macOS, Windows (als MSIX paketiert) und Linux als
  **GTK-3**-Anwendung. Was das praktisch bedeutet, steht unter
  [Hinata unter Linux](#hinata-unter-linux).

## So funktioniert es: vom Start bis zum Workspace

Jeder frische Start durchläuft einen kurzen, vorhersehbaren Weg, bevor du in deinem
Workspace landest.

| Schritt | Was passiert |
| --- | --- |
| **Verbinden** | Beim ersten Start fragt die App nach deiner **Server-URL** und fährt erst fort, wenn der Server unter `/api/v1/meta` antwortet. |
| **Versionssperre** | Die App vergleicht ihre eigene Version mit dem Minimum des Servers (`HINATA_APP_MIN_VERSION`, bereitgestellt als `minAppVersion`) und erzwingt ein Update, wenn der Client zu alt ist. |
| **Setup-Assistent** | Ein brandneuer Server wird direkt in der App konfiguriert — Organisationsname und erster Admin — es sei denn, er wurde mit `HINATA_SETUP_*` gebootstrappt. |
| **Onboarding** | Eine einmalige, illustrierte Tour durch die wichtigsten Funktionen. |
| **Anmelden** | Lokale Zugangsdaten oder **SSO** (OpenID Connect, OAuth 2.0, SAML 2.0, LDAP). |

### Verbinden

Das Allererste, wonach eine native App fragt, ist eine Server-URL. Sie prüft
`/api/v1/meta` und weigert sich fortzufahren, bis der Server antwortet, sodass du
nie mit einem Host „verbunden" enden kannst, der kein Hinata-Server ist. Zuvor
verwendete Server erscheinen als Ein-Tipp-Verknüpfungen unter dem URL-Feld, was das
Wiederverbinden nach einem kurz nicht erreichbaren Server zu einem einzigen Tipp
macht.

!!! info "Native Apps backen nie eine Server-URL ein"
    Eine veröffentlichte native App hat keine Serveradresse einkompiliert. Genau
    das ermöglicht es, dass eine App jedem Hinata-Betreiber dient. Nur der
    **Web**-Build darf standardmäßig auf seinen eigenen Origin zeigen (über
    `kIsWeb`), weil er bereits von einem bekannten Host ausgeliefert wird. Siehe
    [Multi-Server](#multi-server-eine-app-viele-server) unten.

### Versionssperre

Bei jedem Start liest die App die vom Server angegebene minimale Client-Version.
Ist die installierte App älter, zeigt sie statt des Workspaces einen Bildschirm
**Update erforderlich**. Betreiber steuern diesen Wert mit der Umgebungsvariable
`HINATA_APP_MIN_VERSION` oder überschreiben ihn live im
[Adminbereich](/de/admin-area.html) → App-Einstellungen (der Datenbankwert
gewinnt). Das bedeutet, du kannst jeden Client in dem Moment auf einen neuen Build
zwingen, in dem eine breaking Change ausgeliefert wird — ganz ohne clientseitige
Koordination.

### Setup-Assistent

Richte die App auf einen frisch deployten Server, und sie führt dich in der
Oberfläche durch die Ersteinrichtung: den Namen deiner Organisation und das erste
Administratorkonto. Wenn du lieber unbeaufsichtigt bootstrappen möchtest, setze
`HINATA_SETUP_AUTO_COMPLETE=true` zusammen mit `HINATA_SETUP_ORGANIZATION_NAME` und
den Admin-Zugangsdaten, und der Assistent wird übersprungen. Siehe
[Setup & Erststart](/de/setup-wizard.html).

### Anmelden

Sobald ein Server eingerichtet ist, authentifizierst du dich entweder mit:

- **Lokalen Zugangsdaten** — Benutzername/E-Mail und Passwort.
  Selbstregistrierung, E-Mail-Verifizierung, Passwort-vergessen und optionale
  Admin-Genehmigung werden alle unterstützt und über Feature-Flags gesteuert (siehe
  [Authentifizierung](/de/authentication.html)).
- **SSO** — OpenID Connect, OAuth 2.0, SAML 2.0 oder LDAP, vom Betreiber im
  Adminbereich konfiguriert. SSO kehrt über den Deep Link `hinata://auth-callback`
  zur App zurück. Siehe [Single Sign-on](/de/sso.html).

Wenn die Zwei-Faktor-Authentifizierung (TOTP) für ein Konto aktiviert ist, fügt die
Anmeldung nach dem Passwortschritt eine Einmalcode-Abfrage hinzu.

## Multi-Server: eine App, viele Server

Eine einzige Hinata-App kann mit beliebig vielen unabhängigen Servern sprechen und
zwischen ihnen wechseln, ohne sich von den anderen abzumelden.

- **Mehrere Server speichern.** Füge jeden Server einmal hinzu; die App merkt sie
  sich.
- **Frei wechseln.** Bewege dich über den Umschalter zwischen den Servern; jeder
  behält seine eigene Sitzung.
- **Pro Server gescopte Tokens.** Access Tokens sind auf den Server beschränkt, der
  sie ausgestellt hat — beim Serverwechsel gelangen nie Zugangsdaten zwischen
  Instanzen.

### Der Server-Manager

Der Liquid-Glass-**Server-Manager** ist der Ort, an dem du deine gespeicherten
Server verwaltest. Beim Öffnen prüft er jeden gespeicherten Server **parallel**,
sodass jede Zeile einen Live-Status zeigt — einen pulsierenden Punkt und einen
echten Ping in Millisekunden — und von *prüfe…* auf *online* (mit Latenz) oder
*offline* umschaltet, sobald Ergebnisse eintreffen.

Im Manager kannst du:

- Einen Server **hinzufügen** — die App führt vor dem Speichern einen
  **Verbindungstest** durch, sodass eine nicht erreichbare oder falsche URL sofort
  erkannt wird.
- Namen oder URL eines gespeicherten Servers **bearbeiten**.
- Einen Server, den du nicht mehr nutzt, **löschen**.
- Mit einem Tipp zu einem beliebigen Online-Server **wechseln**.

!!! tip "Self-hosted oder Cloud, nebeneinander"
    Jede Zeile ist mit einem Badge versehen, sodass du deine eigene selbst
    gehostete Instanz auf einen Blick von anderen unterscheiden kannst. Weil Tokens
    pro Server gescopt sind, ist es völlig sicher, einen Arbeitsserver und einen
    privaten Server in derselben App zu halten.

## Woher du die App bekommst

Es gibt drei Wege, den Client auszuführen, je nachdem, wer du bist.

| Du möchtest… | Verwende |
| --- | --- |
| **Einen Server einfach im Browser nutzen** | Die gehostete **Web-App** — ein Betreiber liefert sie unter `https://track.example.com` aus (das Overlay `docker-compose.app.yml`). Nichts zu installieren. |
| **Den Client selbst aus dem Quellcode ausführen** | Klone [hinata-app](https://github.com/hinata-platform/hinata-app), `flutter pub get`, `flutter run`. GPL-3.0. |
| **Eine gebrandete App in die Stores bringen** | Baue deinen **eigenen** Client — siehe [Branding & eigene Clients](/de/self-hosted-app.html). |

Die veröffentlichten Store-Builds folgen dem Bring-your-own-Server-Modell: Weil
native Apps keine einkompilierte Server-URL tragen, kann eine veröffentlichte App
über das
[Hinata Connect Gateway](/de/connect-gateway.html) jedem Betreiber dienen. Dieses
Gateway leitet auch Push-Benachrichtigungen weiter — an FCM für Android, iOS und
macOS und an WNS für Windows. Unter Linux gibt es keinen solchen Dienst, an den
sich weiterleiten ließe, deshalb erhält der Linux-Build gar kein Push;
Benachrichtigungen erreichen dich stattdessen in der App und per E-Mail.

Unter Linux führt der Weg über den **Snap Store**: Dorthin wird der Build als
strikt isoliertes Snap für amd64 und arm64 hochgeladen. Hochgeladen heißt noch
nicht installierbar — bislang liegt keine Revision auf einem Kanal, es gibt also
nichts zu installieren und auch keine Store-Seite; der Abschnitt weiter unten
sagt, wie der Stand ist. Das **Flatpak**-Manifest und das **AppImage**-Skript
liegen weiterhin daneben im Repository — dieselbe App, nur von dir gebaut statt
von einem Store.

!!! note "Open Source, GPL-3.0"
    Die App ist unter **GPL-3.0** lizenziert. Es steht dir frei, sie zu bauen, zu
    modifizieren und deinen eigenen gebrandeten Client auszuliefern — siehe den
    [Leitfaden für eigene Clients](/de/self-hosted-app.html) für genau das, was zu ändern ist.

## Hinata unter Linux

Linux ist ein vollwertiges Ziel, keine Kompatibilitätsschicht. Die App wird als
native **GTK-3**-Desktop-Anwendung gebaut — eine Binary, `hinata`, mit der
Application-ID `com.ahmadre.hinata` — aus exakt derselben Flutter-Codebasis wie
die Telefon- und die Web-Variante. Anmeldung, SSO, Multi-Server, Boards, Anhänge,
Drucken und PDF-Export verhalten sich genau wie überall sonst.

### Installieren

| Format | Was du bekommst |
| --- | --- |
| **Snap** | Der Kanal, über den Hinata unter Linux ausgeliefert wird. `sudo snap install hinata` auf jeder Distribution mit snapd, für x86-64 und ARM64, streng isoliert. Zwei Berechtigungen verbinden sich nicht von selbst — siehe unten. |
| **Flatpak** | Baust und installierst du selbst: mit `flatpak-builder` aus dem Manifest in `packaging/linux/flatpak/`. Es liegt auf keinem gehosteten Flatpak-Remote, und nach Flathub geht es auch nicht — siehe unten. |
| **AppImage** | Eine portable Datei, die du selbst baust: `packaging/linux/appimage/build-appimage.sh` macht aus einem Release-Bundle eine, dann `chmod +x` und starten. Veröffentlicht ist sie nirgends — die CI hängt sie an einen Workflow-Lauf, nicht an ein Release. Sie linkt bewusst gegen GTK, GStreamer und libsecret deines Systems und behält so dein Desktop-Theme und die Codecs deiner Distribution, statt eigene Kopien einzufrieren. |
| **Aus dem Quellcode** | `flutter build linux --release` erzeugt ein verschiebbares Bundle (die Binary `hinata` plus `data/` und `lib/`), das du installieren kannst, wo du möchtest. |

!!! info "Zwei Berechtigungen brauchen einen Klick"
    Snap führt die App streng isoliert aus, und zwei der angeforderten
    Schnittstellen verbinden sich nicht automatisch. Beides ist die Art von
    Zugriff, die ein Store bewusst erteilen lässt statt beim Installieren
    mitzugeben:

    ```bash
    sudo snap connect hinata:password-manager-service   # angemeldet bleiben
    sudo snap connect hinata:audio-record               # Sprachnachricht aufnehmen
    ```

    Ohne die erste läuft die App, kann deine Sitzung aber nicht im
    Schlüsselbund behalten — jeder Neustart landet auf der Anmeldung. Ohne die
    zweite tut die Mikrofon-Schaltfläche nichts. Die App benennt die fehlende
    Berechtigung, statt stillschweigend nichts zu tun, und dieselben Schalter
    stehen in Ubuntus App Center unter „Berechtigungen“.

Alle drei Rezepte liegen in `packaging/linux/` in
[hinata-app](https://github.com/hinata-platform/hinata-app), und alle drei
installieren denselben Desktop-Eintrag, dasselbe Icon und dieselbe
AppStream-Metainfo. Flatpak und AppImage paketieren ein vorher gebautes Bundle;
das Snap führt den Flutter-Build selbst aus, denn ein Snapcraft-Build-Schritt
hat Netzwerk — und sowohl die Flutter-Engine-Artefakte als auch pdfium werden
erst während eines Builds geladen. `flatpak-builder` lässt seine Module ganz
ohne Netzwerk laufen; deshalb muss man dem Flatpak ein fertiges Bundle
hinlegen.

AppImage und rohes Bundle entstehen auf einem fest gepinnten
`ubuntu-22.04`-Runner, wodurch ihre glibc-Untergrenze eine Entscheidung ist und
kein Zufall: Ein Flutter-Bundle ist dynamisch gegen die glibc gelinkt, mit der
es gebaut wurde, und glibc ist nur vorwärtskompatibel — ein neuerer Runner würde
also still und leise eine Binary erzeugen, die auf älteren Distributionen nicht
startet. Das Snap braucht diesen Pin nicht: Seine libc kommt aus seiner
`core24`-Base, nicht von der Maschine, die es gebaut hat.

!!! note "Warum nicht Flathub"
    Die [Anforderungen an Einreichungen](https://docs.flathub.org/docs/for-app-authors/requirements)
    von Flathub schließen Anwendungen aus, deren Inhalte mit einem LLM erzeugt
    wurden — auf Hinata trifft das zu. Das Manifest bleibt trotzdem im
    Repository, weil es baut und installiert: Es ist ein Rezept, kein Kanal.

So baust du sie selbst unter Debian oder Ubuntu:

```bash
sudo apt install \
  clang cmake ninja-build pkg-config \
  libgtk-3-dev liblzma-dev libsecret-1-dev libjsoncpp-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

flutter config --enable-linux-desktop
flutter build linux --release
```

### Deep Links landen im Fenster, aus dem du gestartet bist

Der Desktop-Eintrag registriert das Schema `x-scheme-handler/hinata`, und die App
läuft als **Single-Instance**-GTK-Anwendung: Ein zweiter Start von `hinata` gibt
seine Argumente an die bereits laufende Kopie weiter, statt ein konkurrierendes
Fenster zu öffnen. Genau das lässt `hinata://auth-callback` funktionieren — eine
SSO-Rückkehr, eine Einladung oder ein Link zum Zurücksetzen des Passworts kommt
in dem Fenster an, aus dem du gestartet bist, egal ob die App schon offen war
oder der Link sie erst gestartet hat.

### Was unter Linux anders ist

Zwei Dinge sind unter Linux wirklich nicht verfügbar, und ein paar weitere
stützen sich auf Programme, die deine Distribution installiert haben kann oder
auch nicht. Die ehrliche Liste:

| Bereich | Unter Linux | Warum |
| --- | --- | --- |
| **Push-Benachrichtigungen** | Nicht verfügbar. Benachrichtigungen erreichen dich **in der App** und **per E-Mail**. | `firebase_messaging` hat keine Linux-Implementierung, und es gibt keinen Desktop-Push-Dienst, bei dem sich ein Token registrieren ließe — nichts übernimmt die Rolle, die FCM auf Mobilgeräten und WNS unter Windows spielt. |
| **Kameraaufnahme** | Der Eintrag *Foto aufnehmen* wird gar nicht erst angeboten. Ein vorhandenes Bild oder eine vorhandene Datei anzuhängen funktioniert normal. | Für Linux existiert keine Kamera-Implementierung. Den Eintrag wegzulassen ist besser als eine Schaltfläche, deren einziges mögliches Ergebnis ein Fehlerdialog ist. |
| **Angemeldet bleiben** | Braucht einen Schlüsselbund — siehe den Hinweis unten. | Sitzungs-Tokens werden über den freedesktop Secret Service geschrieben. |
| **Sprachkommentare** | Die Wiedergabe braucht die GStreamer-Plugin-Pakete, die Aufnahme `pulseaudio-utils` und `ffmpeg`. | `just_audio` liefert keine Linux-Implementierung, deshalb läuft die Wiedergabe über ein für diese App geschriebenes GStreamer-Plugin. Der Recorder erzeugt AAC — genau deshalb ist `gstreamer1.0-libav` nötig und nicht optional. |
| **Dateiauswahl für Anhänge** | Nutzt `zenity`, `qarma` oder `kdialog`. Ist keines davon installiert, nennt die App die Programme, die du installieren kannst, statt einfach nichts zu öffnen. | Die Flutter-Dateiauswahl hat kein natives Linux-Backend; sie steuert einen dieser Dialoge an. |
| **Downloads** | Ein Anhang landet direkt in deinem Downloads-Ordner, und ein Toast nennt die Datei. | Unter Linux gibt es kein Share-Sheet, dem sich die Datei übergeben ließe — also sagt die App dir, wo sie gelandet ist. |

Deine **Benachrichtigungseinstellungen bleiben** auf einem Linux-Desktop
**sichtbar und bearbeitbar**, obwohl dort nie ein Push ausgelöst wird. Die
Einstellung gehört zu deinem Konto, nicht zu dem Rechner, an dem du gerade sitzt
— sie unter Linux auszublenden, würde dir den Schalter nehmen, der dein Telefon
steuert.

!!! warning "Angemeldet bleiben braucht einen Schlüsselbund"
    Hinata legt deine Sitzungs-Tokens über den freedesktop **Secret Service** im
    Schlüsselbund des Systems ab — GNOME Keyring, KWallet oder alles andere, das
    ihn implementiert. Ein minimaler Fenstermanager, ein Container oder eine
    SSH-Sitzung auf einen Desktop, dessen Schlüsselbund nie entsperrt wurde, hat
    nichts, worin sie sich speichern ließen. Die Anmeldung funktioniert trotzdem
    und deine Sitzung hält, bis du die App schließt — und die App sagt dir das
    sofort, statt es dich beim nächsten Start herausfinden zu lassen.

    ```bash
    sudo apt install gnome-keyring     # Debian / Ubuntu
    sudo dnf install gnome-keyring     # Fedora
    ```

Alles in der Tabelle oben funktioniert auf einer normalen Desktop-Installation.
Auf einem schlanken System — einem Container, einem nackten Fenstermanager — ist
das hier die vollständige Liste:

```bash
sudo apt install \
  gnome-keyring zenity \
  pulseaudio-utils ffmpeg \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-libav
```

!!! tip "Die fertigen Pakete bringen das meiste davon mit"
    Die Flatpak-Runtime enthält GTK, `zenity`, FFmpeg und die GStreamer-Plugins
    bereits. Eine Flatpak-Installation braucht auf dem Host also nur noch einen
    Schlüsselbund, damit du angemeldet bleibst. Das Snap bringt FFmpeg,
    PulseAudios Aufnahme-Werkzeuge und die zusätzlichen GStreamer-Plugins selbst
    mit und wählt Dateien über das Desktop-Portal statt über `zenity`. Zwei
    seiner Berechtigungen verbinden sich nicht von allein, weil sie an
    Schlüsselbund und Mikrofon reichen:

    ```bash
    sudo snap connect hinata:password-manager-service   # angemeldet bleiben
    sudo snap connect hinata:audio-record               # Sprachkommentare aufnehmen
    ```

## Wie es weitergeht

- [Branding & eigene Clients](/de/self-hosted-app.html) — Laufzeit-Branding oder dein eigener Client.
- [Authentifizierung](/de/authentication.html) — lokale Konten, Registrierung, 2FA.
- [Single Sign-on](/de/sso.html) — verbinde einen Identitätsanbieter.
- [Setup & Erststart](/de/setup-wizard.html) — einen frischen Server konfigurieren.
