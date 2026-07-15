---
title: Die Apps
description: Eine Flutter-Codebasis für Android, iOS, Web und macOS — wie sich der Client verbindet, Versionen sperrt, sich anmeldet und mehrere Server aus einem Liquid-Glass-Server-Manager verwaltet.
---

# Die Apps

Hinata liefert einen einzigen Flutter-Client, der aus **einer Codebasis** auf
**Android, iOS, Web und macOS** läuft. Es gibt keine separate Mobil- und
Desktop-App, die synchron gehalten werden müssten — dieselben Bildschirme, derselbe
State, dieselbe Netzwerkschicht passen sich an, worauf auch immer sie laufen. Diese
Seite erklärt, wie sich die App mit deinem Server verbindet, wie sie entscheidet,
ob sie aktuell ist, wie du dich anmeldest und wie eine einzige App mit vielen
Servern gleichzeitig spricht.


![Hinata auf dem Smartphone](/assets/img/shot-mobile-dashboard.png)
*Eine Flutter-Codebasis — Android, iOS, Web und macOS aus einer App.*

## Eine Codebasis, vier Plattformen

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
[Hinata Connect Gateway](/de/connect-gateway.html) jedem Betreiber dienen.

!!! note "Open Source, GPL-3.0"
    Die App ist unter **GPL-3.0** lizenziert. Es steht dir frei, sie zu bauen, zu
    modifizieren und deinen eigenen gebrandeten Client auszuliefern — siehe den
    [Leitfaden für eigene Clients](/de/self-hosted-app.html) für genau das, was zu ändern ist.

## Wie es weitergeht

- [Branding & eigene Clients](/de/self-hosted-app.html) — Laufzeit-Branding oder dein eigener Client.
- [Authentifizierung](/de/authentication.html) — lokale Konten, Registrierung, 2FA.
- [Single Sign-on](/de/sso.html) — verbinde einen Identitätsanbieter.
- [Setup & Erststart](/de/setup-wizard.html) — einen frischen Server konfigurieren.
