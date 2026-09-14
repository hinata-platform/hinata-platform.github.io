---
title: Branding & eigene Clients
description: Laufzeit-Branding vom Server und wie du bei Bedarf deinen eigenen Hinata-Client baust.
---

# Branding & eigene Clients

Hinata folgt dem Modell **eine App, selbst gehostete Server**, wie Rocket.Chat
oder Nextcloud. Du betreibst deinen Server, die veröffentlichte Hinata-App
verbindet sich damit.

- Die native App hat **keine fest eingebaute Server-URL**. Nutzer bringen ihren
  eigenen Server mit.
- Das Branding (Organisationsname und Logo) kommt zur Laufzeit vom Server über
  `/api/v1/meta`.
- Push und Universal Links laufen für jede Instanz über das
  [Hinata Connect Gateway](/de/connect-gateway.html).

Die meisten Betreiber müssen also nichts bauen. Willst du trotzdem einen eigenen
Client unter eigenem Store-Eintrag, darfst du ihn bauen und veröffentlichen.
Diese Seite zeigt, wie das geht.

!!! note "Open Source, GPL-3.0"
    Der Client steht unter **GPL-3.0**. Du darfst ihn umbenennen, ändern und
    verteilen, solange du die Lizenz einhältst. Vor allem musst du deinen
    Quellcode deinen Nutzern zu denselben Bedingungen bereitstellen.

## Die Zero-Build-Option: die gehostete Web-App

Prüfe zuerst, ob du überhaupt eine native App brauchst. Das Server-Repository
enthält `docker-compose.app.yml`. Dieses Overlay liefert den kompilierten
Flutter-**Web**-Client als statische Dateien unter deiner Domain aus, z. B.
`https://track.example.com`.

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

Nutzer bekommen eine gebrandete URL im Browser, **ohne Installation und ohne
Build**. Der Web-Build spricht mit der API, für die er konfiguriert ist. Viele
Betreiber nutzen nur das und lassen Mobilnutzer die veröffentlichten Apps
verwenden. Einen eigenen nativen Build brauchst du nur für eigenen Store-Eintrag,
eigenes Icon und eigenen Namen.

## Was du änderst

Ein eigener Client ist ein Fork von
[hinata-app](https://github.com/hinata-platform/hinata-app) mit ein paar
ausgetauschten Identitätswerten. Es sind fünf Dinge.

| # | Was | Wo |
| --- | --- | --- |
| 1 | **Package- / Bundle-ID** | `com.yourorg.yourapp`: Android `applicationId` + `namespace`, iOS/macOS `PRODUCT_BUNDLE_IDENTIFIER`, Windows `msix_config.identity_name` + `publisher`, Linux `APPLICATION_ID` + `BINARY_NAME` in `linux/CMakeLists.txt` |
| 2 | **App-Anzeigename** | Android `android:label`, iOS/macOS Anzeigename, Windows `msix_config.display_name`, Linux `Name=` im Desktop-Eintrag |
| 3 | **Icons & Splash** | `assets/branding/` + `flutter_launcher_icons` / `flutter_native_splash`; Linux nimmt ein 512×512-PNG aus `packaging/linux/` |
| 4 | **Akzentfarbe** | das Farbtoken `#D9A032` (Honig-Amber) im Theme |
| 5 | **Gateway** | auf das Hinata Connect Gateway (oder dein eigenes) zeigen |

### 1. Package- und Bundle-ID

Wähle eine Reverse-DNS-Kennung, die dir gehört, z. B. `com.yourorg.yourapp`,
und setze sie überall.

```kotlin
// android/app/build.gradle.kts
android {
    namespace = "com.yourorg.yourapp"
    defaultConfig {
        applicationId = "com.yourorg.yourapp"
    }
}
```

Unter iOS und macOS setzt du `PRODUCT_BUNDLE_IDENTIFIER` im Xcode-Projekt
(Runner-Target). Nach der Veröffentlichung in einem Store ist die ID endgültig,
wähle sie also sorgfältig.

Unter Windows vergibt das **Partner Center** `identity_name`, `publisher` und
`publisher_display_name` für den `msix_config`-Block in `pubspec.yaml`
(Produktverwaltung → Produktidentität). Übernimm sie zeichengenau, sonst lehnt
der Store das Paket ab.

Unter Linux stehen die GTK-Application-ID und der Name des Binaries in
`linux/CMakeLists.txt`:

```cmake
# linux/CMakeLists.txt
set(BINARY_NAME "yourapp")
set(APPLICATION_ID "com.yourorg.yourapp")
```

Die Application-ID steht noch an weiteren Stellen. AppStream und die
Desktop-Shells verknüpfen diese Dateien nur über diese eine Zeichenkette:

- Dateiname des Desktop-Eintrags (`com.yourorg.yourapp.desktop`) und die
  `StartupWMClass` darin
- `<id>` der AppStream-Metainfo
- Flatpak-`app-id`
- Bus-Name im `dbus`-Slot des Snaps

Vergisst du eine Stelle, zeigt die Shell ein generisches Icon, oder der
Store-Eintrag passt nie zur installierten App.

Der Binary-Name steht in `Exec=` im Desktop-Eintrag, in `<provides><binary>` in
der Metainfo und im `command:` von Flatpak und Snap.

!!! note "Warum die Paketdateien für Linux nicht in `linux/` liegen"
    Desktop-Eintrag, Icon, AppStream-Metainfo und die Rezepte für Snap, Flatpak
    und AppImage liegen in hinata-app unter `packaging/linux/`.
    `flutter create --platforms=linux .` schreibt alles unter `linux/` neu und
    würde handgepflegte Dateien überschreiben. Außerdem liefert so jedes Format
    (Flatpak, AppImage, Distributionspaket, einfaches `install`) exakt dieselben
    Dateien aus.

### 2. App-Anzeigename

Setze den Namen, der unter dem Icon steht:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<application android:label="Your App Name" ... >
```

Unter iOS/macOS setzt du den Anzeigenamen in den Info-Einstellungen des
Runner-Targets, unter Windows `msix_config.display_name` in `pubspec.yaml`.

Unter Linux ist es `Name=` im Desktop-Eintrag, dazu `GenericName` und `Comment`.
Alle drei gibt es lokalisiert (`Comment[de]=…`), so zeigt der Starter in einer
deutschen Sitzung deutschen Text. Passe `<name>` und `<summary>` in der
AppStream-Metainfo an. Diese Werte zeigen GNOME Software und KDE Discover im
Eintrag.

### 3. Icons & Splash

Lege dein Artwork (App-Icon, adaptiver Vordergrund, Splash) in `assets/branding/`
und erzeuge die nativen Assets mit dem Tooling aus `pubspec.yaml` neu:

```bash
dart run flutter_launcher_icons        # App-Icons neu generieren (android/ios/web/macos)
dart run flutter_native_splash:create  # Splash-Screens neu generieren
```

Die Blöcke `flutter_launcher_icons` und `flutter_native_splash` in `pubspec.yaml`
steuern Quellbilder und Hintergrundfarben (Standard: hell `#F4F3EF`, dunkel
`#131119`). Passe sie an deine Marke an und starte die Generatoren erneut.

Windows nimmt Kachel- und Taskleistensymbol aus `msix_config.logo_path`. Nimm
dort eine **abgerundete** Variante deines Icons. Windows maskiert nichts, ein
randloses quadratisches Icon wirkt auf der Kachel wie ein hartes Quadrat.

Linux lassen die Generatoren aus. `flutter_launcher_icons` schreibt nur die
Assets für Android, iOS, Web und macOS. Das Linux-Icon ist ein einfaches
**512×512-PNG**, das du selbst installierst und nach der Application-ID
benennst. In hinata-app ist das
`packaging/linux/icons/hicolor/512x512/apps/com.ahmadre.hinata.png`.

Nimm dasselbe abgerundete Artwork wie für Windows, denn auch GNOME und KDE
maskieren keine App-Icons. Einen Splash gibt es unter Linux nicht, das
GTK-Fenster erscheint, sobald die App bereit ist.

### 4. Akzentfarbe

Der honigfarbene Akzent ist ein Farbtoken im Theme
(`lib/core/theme/app_colors.dart`, `accent = Color(0xFFD9A032)`). Ändere ihn auf
deine Markenfarbe. Das Token gilt in der ganzen App, eine Änderung färbt Buttons,
Hervorhebungen und aktive Zustände um. Wähle einen Farbton mit genug Kontrast für
den hellen **und** den dunklen Modus.

### 5. Auf ein Gateway zeigen

Push und Universal Links laufen über das
[Hinata Connect Gateway](/de/connect-gateway.html). Self-Hoster brauchen deshalb
kein eigenes Firebase-Projekt.

Eine gebrandete App, die du selbst veröffentlichst, hat eigene
Push-Zugangsdaten und eine eigene Link-Domain. Du betreibst dann ein eigenes
Gateway und stellst es am Server mit `HINATA_GATEWAY_BASE_URL` ein.

## Deep Links & Universal Links

Damit Links auf `https://track.example.com/...` deine App statt eines Browsertabs
öffnen, lieferst du zwei Zuordnungsdateien aus und deklarierst die Fähigkeit in
der App.

- **Android App Links:** eine `assetlinks.json` unter
  `https://track.example.com/.well-known/assetlinks.json` mit deinem
  `package_name` und den **SHA-256-Fingerprints deines Release-Signaturschlüssels**.
- **iOS Universal Links:** eine `apple-app-site-association`-Datei (AASA) unter
  `https://track.example.com/.well-known/apple-app-site-association` mit deiner
  `appID` (`TEAMID.com.yourorg.yourapp`) und den URL-Pfaden, die die App
  übernehmen soll.

Beide Dateien liefert das **Web-Image** aus, sobald die Web-App unter deiner
Domain läuft. Beispiel für `assetlinks.json`:

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.yourorg.yourapp",
      "sha256_cert_fingerprints": [
        "AA:BB:CC:...:release-signing-key-sha256"
      ]
    }
  }
]
```

!!! warning "SHA-256 des Release-Schlüssels verwenden"
    Android prüft App Links gegen den Fingerprint des Schlüssels, der die
    **installierte APK/AAB signiert** hat. Trage die SHA-256 deines
    Play-Release-Signaturschlüssels (Upload) in `assetlinks.json` ein. Sonst
    öffnen Links ohne Meldung im Browser. Mehrere Fingerprints (Debug, Upload,
    Play-managed) dürfen nebeneinander stehen.

!!! info "iOS braucht Associated Domains"
    Universal Links funktionieren nur, wenn die App die Domain im Entitlement
    **Associated Domains** (`applinks:track.example.com`) deklariert und diese
    Fähigkeit im Provisioning Profile aktiv ist. Sonst ruft iOS deine AASA-Datei
    nie ab.

### Linux: dein eigenes URL-Schema

Linux hat kein Gegenstück zu App Links oder Universal Links. `assetlinks.json`
und die AASA-Datei sind Mechanismen von Android und Apple, unter freedesktop
reagiert nichts darauf. Ein Link auf `https://track.example.com/...` öffnet sich
daher im Browser, und die Seite bietet von dort den Weg in die App an.

Ein eigenes Schema funktioniert dagegen gut. Der Desktop-Eintrag beansprucht es,
und der Client ist eine **Single-Instance**-GTK-Anwendung. SSO-Rücksprung,
Einladung oder Passwort-Reset landen im Fenster, in dem der Nutzer schon
angemeldet ist, und starten keine zweite Kopie.

```ini
# com.yourorg.yourapp.desktop
Exec=yourapp %u
MimeType=x-scheme-handler/yourscheme;
```

Ein Client mit eigenem Branding braucht ein **eigenes** Schema. `hinata://`
gehört der veröffentlichten App. Beanspruchen zwei installierte Apps dasselbe
Schema, entscheidet der Zufall, welche den Link bekommt. Ändere es überall:

- im Android-Intent-Filter
- in `CFBundleURLSchemes` unter iOS und macOS
- in der `MimeType=`-Zeile oben
- im Client-Code, der eine eingehende URI erkennt

Registriere und prüfe den Handler, nachdem du den Desktop-Eintrag installiert
hast:

```bash
update-desktop-database ~/.local/share/applications
xdg-mime default com.yourorg.yourapp.desktop x-scheme-handler/yourscheme
xdg-mime query default x-scheme-handler/yourscheme

xdg-open 'yourscheme://verify-email?token=test'   # einmal mit laufender App,
                                                  # einmal mit geschlossener
```

!!! tip "Teste beide Eingänge"
    Beim Warmstart geht die URI per D-Bus an die laufende Instanz. Beim
    Kaltstart kommt sie als Prozessargument, bevor ein Plugin registriert ist.
    Das sind zwei verschiedene Codepfade. Teste den Link also mit geöffneter und
    mit geschlossener App.

## Store-Releases brauchen eine Datenschutzerklärung

App Store, Google Play und Microsoft Store verlangen für die Prüfung eine
erreichbare **URL zur Datenschutzerklärung**. Für die DSGVO brauchst du sie
ohnehin. Hinata zeigt diese URL in der App über die Servereinstellung
`HINATA_PRIVACY_POLICY_URL` an (auch live im [Adminbereich](/de/admin-area.html)
→ App-Einstellungen änderbar). Setze sie vor dem Einreichen.

Bei einem AppImage oder einem eigenen Flatpak-Remote prüft niemand. Bei Stores
schon:

- Der **Snap Store** prüft, was ein strikt isoliertes Snap anfordert,
  privilegierte Anforderungen von Hand.
- **Flathub** erzeugt den Eintrag aus deiner AppStream-Metainfo. Diese Datei
  braucht dann Name, Kurzbeschreibung, Beschreibung, Lizenz, ein
  OARS-Content-Rating und mindestens einen Screenshot unter einer stabilen,
  gehosteten URL.

Hinata selbst wird nicht auf Flathub angeboten. Unter Linux kommt die App über
den Snap Store.

!!! tip "Barrierefreiheit ist Teil der Konformität"
    Die Oberfläche achtet auf Barrierefreiheit: skalierbarer Text, semantische
    Widgets und ausreichender Kontrast. Denk daran, wenn du Akzentfarbe und
    eigene Texte wählst.

## Branding-Checkliste

Arbeite von oben nach unten. Jeder Schritt steht für sich.

1. **Forke** [hinata-app](https://github.com/hinata-platform/hinata-app) und halte GPL-3.0 ein.
2. Setze die **Package- und Bundle-ID** (`com.yourorg.yourapp`) für Android, iOS
   und macOS, die **MSIX-Identität** aus dem Partner Center für Windows sowie
   `APPLICATION_ID` + `BINARY_NAME` in `linux/CMakeLists.txt`. Benenne danach
   den Linux-Desktop-Eintrag, die `<id>` der Metainfo, die Flatpak-`app-id` und
   den `name` des `dbus`-Slots im Snap passend um. Das `name:` des Snaps selbst
   ist eine eigene, storeweite Kennung, die du auf snapcraft.io registrierst.
3. Setze den **App-Anzeigenamen** auf jeder Plattform, auch `Name=` im
   Linux-Desktop-Eintrag und `<name>` in der Metainfo.
4. Ersetze das Artwork in `assets/branding/` und starte die Generatoren für Icons
   und Splash. Setze `msix_config.logo_path` für Windows auf ein abgerundetes
   Icon und installiere dasselbe abgerundete Icon als 512×512-PNG unter
   `packaging/linux/icons/…`.
5. Ändere das Token der **Akzentfarbe** und prüfe den hellen **und** dunklen Modus.
6. Wähle dein **Gateway**: Standard oder dein eigenes über `HINATA_GATEWAY_BASE_URL`.
7. Liefere `assetlinks.json` und AASA unter `https://track.example.com/.well-known/`
   aus (das erledigt das Web-Image) und trage die **SHA-256 deines
   Release-Schlüssels** ein.
8. Aktiviere **Associated Domains** für iOS Universal Links und beanspruche dein
   eigenes `x-scheme-handler/`-Schema im Linux-Desktop-Eintrag.
9. Setze **`HINATA_PRIVACY_POLICY_URL`** auf dem Server.
10. Bauen, signieren und bei den Stores einreichen.

## Wie es weitergeht

- [Die Apps](/de/clients.html): wie sich der Client verbindet, Versionen sperrt und Server verwaltet.
- [Hinata Connect Gateway](/de/connect-gateway.html): Weiterleitung für Push und Universal Links.
- [Konfigurationsreferenz](/de/configuration.html): jede Servereinstellung.
