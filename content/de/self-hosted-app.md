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
| 1 | **Package- / Bundle-ID** | `com.yourorg.yourapp` — Android `applicationId` + `namespace`, iOS/macOS `PRODUCT_BUNDLE_IDENTIFIER` |
| 2 | **App-Anzeigename** | Android `android:label`, iOS/macOS Anzeigename |
| 3 | **Icons & Splash** | `assets/branding/` + `flutter_launcher_icons` / `flutter_native_splash` |
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

### 2 — App-Anzeigename

Setze den sichtbaren Namen, der unter dem Icon angezeigt wird:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<application android:label="Your App Name" ... >
```

Unter iOS/macOS setzt du den Anzeigenamen in den Info-Einstellungen des
Runner-Targets.

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

## Store-Releases brauchen eine Datenschutzerklärung

Sowohl Apples App Store als auch Google Play verlangen für die Prüfung eine
erreichbare **URL zur Datenschutzerklärung**, und du brauchst sie ohnehin für die
DSGVO-Konformität. Hinata zeigt diese URL in der App über die Servereinstellung
`HINATA_PRIVACY_POLICY_URL` an (auch live im [Adminbereich](/de/admin-area.html) →
App-Einstellungen editierbar). Setze sie, bevor du einreichst.

!!! tip "Barrierefreiheit ist Teil der Konformität"
    Die Oberfläche ist mit Blick auf Barrierefreiheit gebaut — skalierbarer Text,
    semantische Widgets und ausreichender Kontrast. Behalte das im Kopf, wenn du
    deine Akzentfarbe und eigene Texte wählst.

## Branding-Checkliste

Arbeite von oben nach unten; jeder Schritt ist unabhängig.

1. **Forke** [hinata-app](https://github.com/hinata-platform/hinata-app) und halte GPL-3.0 ein.
2. Setze die **Package-/Bundle-ID** (`com.yourorg.yourapp`) auf Android, iOS und macOS.
3. Setze den **App-Anzeigenamen** auf jeder Plattform.
4. Ersetze das Artwork in `assets/branding/` und lass die Icon- + Splash-Generatoren laufen.
5. Ändere das **Akzentfarb**-Token im Theme; verifiziere den hellen **und** dunklen Modus.
6. Entscheide dich für dein **Gateway** — Standard oder dein eigenes über `HINATA_GATEWAY_BASE_URL`.
7. Liefere `assetlinks.json` + AASA unter `https://track.example.com/.well-known/`
   aus (das Web-Image erledigt das) und liste deine **Release-Schlüssel-SHA-256** auf.
8. Aktiviere die **Associated Domains**-Fähigkeit für iOS Universal Links.
9. Setze **`HINATA_PRIVACY_POLICY_URL`** auf dem Server.
10. Baue, signiere und reiche bei den Stores ein.

## Wie es weitergeht

- [Die Apps](/de/clients.html) — wie sich der Client verbindet, Versionen sperrt und Server verwaltet.
- [Hinata Connect Gateway](/de/connect-gateway.html) — Push- + Universal-Link-Relay.
- [Konfigurationsreferenz](/de/configuration.html) — jede Servereinstellung.
