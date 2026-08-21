---
title: Branding & eigene Clients
description: Eine veröffentlichte Client-App für selbst gehostete Hinata-Server — Laufzeit-Branding vom Server, und wie du bei Bedarf deinen eigenen Client baust (Package-ID, Name, Icons, Splash, Akzent, Deep Links). Praktisch, Schritt für Schritt, GPL-3.0.
---

# Branding & eigene Clients

Hinata folgt dem Modell **eine App, selbst gehostete Server**, wie du es von
Rocket.Chat oder Nextcloud kennst: Du betreibst deine eigene Server-Instanz, und
die eine veröffentlichte Hinata-App verbindet sich mit ihr. Die native App trägt
**keinen fest eingebauten Backend-Server** — Nutzer bringen ihren eigenen Server
mit, und das Branding (Organisationsname und Logo) kommt zur Laufzeit vom Server
über `/api/v1/meta`. Push und Universal Links funktionieren für jede Instanz über
das [Hinata Connect Gateway](/de/connect-gateway.html), sodass die meisten
Betreiber nie etwas bauen müssen. Willst du *doch* einen eigenen Client unter
deinem eigenen Store-Eintrag, steht es dir frei, ihn zu bauen und zu
veröffentlichen — diese Seite ist der praktische Leitfaden dazu.

!!! note "Open Source, GPL-3.0"
    Der Client ist unter **GPL-3.0** lizenziert. Du darfst ihn neu branden,
    modifizieren und verteilen, sofern du die Lizenz einhältst — vor allem musst du
    deinen entsprechenden Quellcode deinen Benutzern zu denselben Bedingungen zur
    Verfügung stellen.

## Die Zero-Build-Option: die gehostete Web-App

Bevor du irgendetwas baust, überlege, ob du überhaupt eine native App brauchst. Das
Server-Repository liefert `docker-compose.app.yml`, ein Overlay, das den
kompilierten Flutter-**Web**-Client als statische Dateien unter deiner eigenen
Domain ausliefert, z. B. `https://track.example.com`.

```bash
docker compose -f docker-compose.yml -f docker-compose.app.yml up -d
```

Das gibt Benutzern eine gebrandete URL im Browser mit **nichts zu installieren und
nichts zu bauen**. Der Web-Build zeigt auf die API, für die er konfiguriert ist,
sodass viele Betreiber nur dies betreiben und mobile Benutzer über die
veröffentlichten Apps erreichen lassen. Greife zu einem eigenen nativen Build,
wenn du gezielt deine eigene Store-Präsenz, dein eigenes Icon und deinen eigenen
Namen brauchst.

## Was du änderst

Ein eigener Client ist ein Fork von
[hinata-app](https://github.com/hinata-platform/hinata-app), bei dem eine Handvoll
Identitätswerte ausgetauscht sind. Es gibt fünf Dinge zu ändern.

| # | Was | Wo |
| --- | --- | --- |
| 1 | **Package- / Bundle-ID** | `com.yourorg.yourapp` — Android `applicationId` + `namespace`, iOS/macOS `PRODUCT_BUNDLE_IDENTIFIER`, Windows `msix_config.identity_name` + `publisher`, Linux `APPLICATION_ID` + `BINARY_NAME` in `linux/CMakeLists.txt` |
| 2 | **App-Anzeigename** | Android `android:label`, iOS/macOS Anzeigename, Windows `msix_config.display_name`, Linux `Name=` im Desktop-Eintrag |
| 3 | **Icons & Splash** | `assets/branding/` + `flutter_launcher_icons` / `flutter_native_splash`; Linux nimmt ein 512×512-PNG aus `packaging/linux/` |
| 4 | **Akzentfarbe** | das Honig-Amber-Akzent-Token `#D9A032` im Theme |
| 5 | **Gateway** | auf das Hinata Connect Gateway (oder dein eigenes) zeigen |

### 1 — Package- / Bundle-ID

Wähle einen Reverse-DNS-Identifier, den du besitzt, z. B. `com.yourorg.yourapp`,
und setze ihn überall:

```kotlin
// android/app/build.gradle.kts
android {
    namespace = "com.yourorg.yourapp"
    defaultConfig {
        applicationId = "com.yourorg.yourapp"
    }
}
```

Für iOS und macOS setzt du `PRODUCT_BUNDLE_IDENTIFIER` im Xcode-Projekt
(Runner-Target). Diese ID ist nach der Veröffentlichung in einem Store permanent —
wähle sorgfältig.

Windows identifiziert ein MSIX-Paket anders: `identity_name`, `publisher` und
`publisher_display_name` im `msix_config`-Block von `pubspec.yaml` werden dir
**vom Partner Center zugewiesen** (Produktverwaltung → Produktidentität).
Übernimm sie zeichengenau — bei jeder Abweichung lehnt der Store das Paket ab.

Linux hält seine Identität in `linux/CMakeLists.txt` — die GTK-Application-ID und
den Namen des Binaries, das im Bundle landet:

```cmake
# linux/CMakeLists.txt
set(BINARY_NAME "yourapp")
set(APPLICATION_ID "com.yourorg.yourapp")
```

Die Application-ID reicht allerdings weiter als bis zum Prozess. Sie ist auch der
Dateiname des Desktop-Eintrags (`com.yourorg.yourapp.desktop`), die
`StartupWMClass` darin, die `<id>` der AppStream-Metainfo, die Flatpak-`app-id`
und der Bus-Name im `dbus`-Slot des Snaps — AppStream und die Desktop-Shells
verknüpfen diese Dateien allein über diese eine Zeichenkette. Bleibt ein einziges Vorkommen zurück, zeigt die Shell deine App mit
einem generischen Icon, oder der Store-Eintrag passt nie zur installierten App.
Der Binary-Name wandert ebenfalls mit: `Exec=` im Desktop-Eintrag,
`<provides><binary>` in der Metainfo und das `command:` von Flatpak und Snap.

!!! note "Warum die Linux-Packaging-Dateien außerhalb von `linux/` liegen"
    In hinata-app liegen der Desktop-Eintrag, das Icon, die AppStream-Metainfo und
    die Rezepte für Snap, Flatpak und AppImage in `packaging/linux/`, nicht in
    `linux/`.
    `flutter create --platforms=linux .` schreibt alles unter `linux/` neu, und
    handgepflegte Packaging-Eingaben haben in diesem Wirkungsbereich nichts zu
    suchen. Ein gemeinsames Verzeichnis bedeutet außerdem, dass jedes Format —
    Flatpak, AppImage, ein Distributionspaket, ein schlichtes `install` — exakt
    dieselben Dateien ausliefert.

### 2 — App-Anzeigename

Setze den sichtbaren Namen, der unter dem Icon angezeigt wird:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<application android:label="Your App Name" ... >
```

Unter iOS/macOS setzt du den Anzeigenamen in den Info-Einstellungen des
Runner-Targets; unter Windows setzt du `msix_config.display_name` in
`pubspec.yaml`.

Unter Linux ist der sichtbare Name `Name=` im Desktop-Eintrag, daneben stehen
`GenericName` und `Comment` — alle drei nehmen lokalisierte Varianten
(`Comment[de]=…`), so bekommt eine deutsche Sitzung deutschen Text im Starter.
Setze `<name>` und `<summary>` in der AppStream-Metainfo passend dazu: Das ist,
was GNOME Software und KDE Discover im Eintrag anzeigen.

### 3 — Icons & Splash

Lege dein Artwork in `assets/branding/` (App-Icon, adaptiver Vordergrund, Splash)
und generiere die nativen Assets mit dem bereits in `pubspec.yaml` verdrahteten
Tooling neu:

```bash
dart run flutter_launcher_icons        # App-Icons neu generieren (android/ios/web/macos)
dart run flutter_native_splash:create  # Splash-Screens neu generieren
```

Die Blöcke `flutter_launcher_icons` und `flutter_native_splash` in `pubspec.yaml`
steuern die Quellbilder und Hintergrundfarben (hell `#F4F3EF`, dunkel `#131119`
standardmäßig) — passe sie an deine Marke an und lass die Generatoren dann erneut
laufen.

Windows nimmt sein Kachel- und Taskleisten-Icon stattdessen aus
`msix_config.logo_path`. Zeige dort auf eine **abgerundete** Variante deines
Icons: Windows maskiert nichts von sich aus, ein randlos quadratisches Icon
erscheint auf der Kachel also als hartes Quadrat.

Linux ist das Ziel, das die Generatoren auslassen. `flutter_launcher_icons`
schreibt die Assets für Android, iOS, Web und macOS; das Linux-Icon ist ein
schlichtes **512×512-PNG**, das du selbst installierst, benannt nach der
Application-ID — in hinata-app ist das
`packaging/linux/icons/hicolor/512x512/apps/com.ahmadre.hinata.png`. Nimm dasselbe
abgerundete Artwork wie für Windows: Auch GNOME und KDE maskieren App-Icons nicht,
ein randloses Quadrat wirkt dort also ebenso als hartes Quadrat. Einen Splash gibt
es nicht zu generieren — das GTK-Fenster erscheint, sobald die App bereit ist.

### 4 — Akzentfarbe

Der charakteristische Honig-Amber-Akzent lebt als Farb-Token im Theme
(`lib/core/theme/app_colors.dart`, `accent = Color(0xFFD9A032)`). Ändere ihn in
deine Markenfarbe; das Token wird app-weit konsumiert, sodass eine einzige
Bearbeitung Buttons, Highlights und aktive Zustände neu einfärbt. Wähle einen
Farbton mit genug Kontrast, um in **beiden** Modi, hell und dunkel, lesbar zu sein.

### 5 — Auf ein Gateway zeigen

Push-Benachrichtigungen und Universal Links werden über das
[Hinata Connect Gateway](/de/connect-gateway.html) weitergeleitet, sodass
Self-Hoster kein eigenes Firebase-Projekt brauchen. Eine gebrandete App, die du
selbst veröffentlichst, besitzt ihre eigenen Push-Zugangsdaten und ihre eigene
Link-Domain — du betreibst also dein eigenes Gateway und richtest deinen Server
mit `HINATA_GATEWAY_BASE_URL` darauf aus.

## Deep Links & Universal Links

Damit `https://track.example.com/...`-Links deine App statt eines Browser-Tabs
öffnen, lieferst du zwei Zuordnungsdateien aus und deklarierst die Fähigkeit in der
App.

- **Android App Links** — eine `assetlinks.json`, ausgeliefert unter
  `https://track.example.com/.well-known/assetlinks.json`, die deinen
  `package_name` und die **SHA-256-Fingerprints deines Release-Signaturschlüssels**
  auflistet.
- **iOS Universal Links** — eine `apple-app-site-association` (AASA)-Datei,
  ausgeliefert unter
  `https://track.example.com/.well-known/apple-app-site-association`, die deine
  `appID` (`TEAMID.com.yourorg.yourapp`) und die zu erfassenden URL-Pfade
  auflistet.

Beide Dateien werden vom **Web-Image** ausgeliefert, sodass ihr Hosting automatisch
erfolgt, sobald die Web-App unter deiner Domain läuft. Beispiel
`assetlinks.json`:

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

!!! warning "Verwende die SHA-256 deines Release-Schlüssels, nicht des Debug-Schlüssels"
    Android verifiziert App Links gegen den Fingerprint des Schlüssels, der die
    **installierte APK/AAB signiert** hat. Liste die SHA-256 deines
    Play-Release-Signaturschlüssels (Upload) in `assetlinks.json` auf, sonst fallen
    Links stillschweigend auf den Browser zurück. Du kannst mehrere Fingerprints
    (Debug, Upload, Play-managed) nebeneinander auflisten.

!!! info "iOS braucht die Associated-Domains-Fähigkeit"
    Universal Links funktionieren nur, wenn die App die Domain in ihrem
    **Associated Domains**-Entitlement (`applinks:track.example.com`) deklariert
    und diese Fähigkeit im Provisioning Profile aktiviert ist. Ohne sie ruft iOS
    deine AASA-Datei nie ab.

### Linux: dein eigenes URL-Schema

Linux hat kein Gegenstück zu App Links oder Universal Links — `assetlinks.json`
und die AASA-Datei sind Android- und Apple-Mechanismen, und im Freedesktop-Umfeld
antwortet nichts darauf. Ein Link auf `https://track.example.com/...` öffnet sich
deshalb im Browser, und die Seite bietet von dort den Weg in die App an.

Was funktioniert — und zwar gut — ist das eigene Schema: Der Desktop-Eintrag
beansprucht es, und der Client ist eine **Single-Instance**-GTK-Anwendung. Ein
SSO-Rücksprung, eine Einladung oder ein Passwort-Reset landet also in genau dem
Fenster, in dem der Nutzer bereits angemeldet ist, statt eine zweite Kopie zu
starten.

```ini
# com.yourorg.yourapp.desktop
Exec=yourapp %u
MimeType=x-scheme-handler/yourscheme;
```

Ein umgebrandeter Client braucht sein **eigenes** Schema. `hinata://` gehört der
veröffentlichten App, und wenn zwei installierte Apps dasselbe Schema
beanspruchen, ist es Zufall, welcher von beiden der Desktop den Link gibt. Ändere
es überall dort, wo es beansprucht wird — im Android-Intent-Filter, in
`CFBundleURLSchemes` unter iOS und macOS, in der `MimeType=`-Zeile oben — und im
Client-Code, der eine eingehende URI erkennt.

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
    Ein Warmstart reicht die URI über D-Bus an die laufende Instanz weiter; ein
    Kaltstart bekommt sie als Prozessargument, bevor überhaupt ein Plugin
    registriert ist. Das sind wirklich zwei verschiedene Codepfade — probiere den
    Link also mit geöffneter und mit geschlossener App.

## Store-Releases brauchen eine Datenschutzerklärung

Apples App Store, Google Play und der Microsoft Store verlangen für die Prüfung
alle eine erreichbare **URL zur Datenschutzerklärung**, und du brauchst sie
ohnehin für die DSGVO-Konformität. Hinata zeigt diese URL in der App über die
Servereinstellung `HINATA_PRIVACY_POLICY_URL` an (auch live im
[Adminbereich](/de/admin-area.html) → App-Einstellungen editierbar). Setze sie,
bevor du einreichst.

Linux kennt keinen solchen Torwächter — ein AppImage oder dein eigenes
Flatpak-Remote muss niemandem Rechenschaft ablegen. Ein Store schon: Der **Snap
Store** prüft, was ein strikt isoliertes Snap anfordert, bei privilegierten
Anforderungen von Hand. Und veröffentlichst du auf **Flathub**, wird der Eintrag
aus deiner AppStream-Metainfo erzeugt: Diese Datei braucht dann Name,
Kurzbeschreibung, Beschreibung, Lizenz, ein OARS-Content-Rating und mindestens
einen Screenshot unter einer stabilen, gehosteten URL.

Hinata selbst liefert Linux über den Snap Store aus und nicht über Flathub:
Dessen [Anforderungen an Einreichungen](https://docs.flathub.org/docs/for-app-authors/requirements)
schließen Anwendungen aus, deren Inhalte mit einem LLM erzeugt wurden. Behält
dein Fork Hinatas Oberfläche und Texte, gilt das auch für ihn.

!!! tip "Barrierefreiheit ist Teil der Konformität"
    Die Oberfläche ist mit Blick auf Barrierefreiheit gebaut — skalierbarer Text,
    semantische Widgets und ausreichender Kontrast. Behalte das im Kopf, wenn du
    deine Akzentfarbe und eigene Texte wählst.

## Branding-Checkliste

Arbeite von oben nach unten; jeder Schritt ist unabhängig.

1. **Forke** [hinata-app](https://github.com/hinata-platform/hinata-app) und halte GPL-3.0 ein.
2. Setze die **Package-/Bundle-ID** (`com.yourorg.yourapp`) auf Android, iOS und
   macOS, die **MSIX-Identität** aus dem Partner Center auf Windows sowie
   `APPLICATION_ID` + `BINARY_NAME` in `linux/CMakeLists.txt` — benenne danach den
   Linux-Desktop-Eintrag, die `<id>` der Metainfo, die Flatpak-`app-id` und den
   `name` des `dbus`-Slots im Snap passend um. Das `name:` des Snaps selbst ist
   eine eigene, storeweite Kennung, die du auf snapcraft.io registrierst.
3. Setze den **App-Anzeigenamen** auf jeder Plattform, inklusive `Name=` im
   Linux-Desktop-Eintrag und `<name>` in der Metainfo.
4. Ersetze das Artwork in `assets/branding/` und lass die Icon- + Splash-Generatoren
   laufen; zeige mit `msix_config.logo_path` für Windows auf ein abgerundetes Icon und
   installiere dasselbe abgerundete Icon als 512×512-PNG unter `packaging/linux/icons/…`.
5. Ändere das **Akzentfarb**-Token im Theme; verifiziere den hellen **und** dunklen Modus.
6. Entscheide dich für dein **Gateway** — Standard oder dein eigenes über `HINATA_GATEWAY_BASE_URL`.
7. Liefere `assetlinks.json` + AASA unter `https://track.example.com/.well-known/`
   aus (das Web-Image erledigt das) und liste deine **Release-Schlüssel-SHA-256** auf.
8. Aktiviere die **Associated Domains**-Fähigkeit für iOS Universal Links und
   beanspruche dein eigenes `x-scheme-handler/`-Schema im Linux-Desktop-Eintrag.
9. Setze **`HINATA_PRIVACY_POLICY_URL`** auf dem Server.
10. Baue, signiere und reiche bei den Stores ein.

## Wie es weitergeht

- [Die Apps](/de/clients.html) — wie sich der Client verbindet, Versionen sperrt und Server verwaltet.
- [Hinata Connect Gateway](/de/connect-gateway.html) — Push- + Universal-Link-Relay.
- [Konfigurationsreferenz](/de/configuration.html) — jede Servereinstellung.
