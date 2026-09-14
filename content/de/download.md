---
title: Download
description: Hol dir die Hinata-App für Android, iOS, macOS, Windows, Linux oder das Web.
---

# Hinata herunterladen

Hinata ist ein Client für **deinen eigenen Server**. Nach dem Start fragt die App
zuerst nach einer Serveradresse. Hast du noch keinen Server, fang bei
[Self-Hosting](/de/self-hosting.html) an. Du brauchst nur eine
Docker-Compose-Datei und ein paar Minuten.

Die App ist eine Flutter-Codebasis für sechs Plattformen. Bildschirme, Daten und
Tastenkürzel sind überall gleich.

## App holen

<ul class="plat-grid">
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg><strong>Android</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Für Handy und Tablet, mit Push-Benachrichtigungen und vollständiger Navigation.</p>
  <span class="plat-actions">
    <a href="https://play.google.com/store/apps/details?id=com.ahmadre.hinata"><img class="b-play" src="/assets/img/badges/google-play.png" alt="Jetzt bei Google Play"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg><strong>iOS</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Für iPhone und iPad, mit Push-Benachrichtigungen und Deep Links direkt zum Vorgang.</p>
  <span class="plat-actions">
    <a href="https://apps.apple.com/us/app/hinata/id6781889251"><img class="b-apple" src="/assets/img/badges/app-store.svg" alt="Laden im App Store"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/></svg><strong>macOS</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Nativer Desktopclient, notarisiert und im Mac App Store.</p>
  <span class="plat-actions">
    <a href="https://apps.apple.com/us/app/hinata/id6781889251"><img class="b-apple" src="/assets/img/badges/mac-app-store.svg" alt="Laden im Mac App Store"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg><strong>Windows</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Als MSIX paketiert, mit Push über die Windows Push Notification Services.</p>
  <span class="plat-actions">
    <a href="https://apps.microsoft.com/detail/9N5NVNPKBBLR"><img class="b-ms" src="/assets/img/badges/microsoft-store.svg" alt="Erhältlich bei Microsoft"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg><strong>Linux</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Nativer GTK 3 Client, streng isoliert, für x86-64 und ARM64. Rezepte für Flatpak und AppImage liegen weiter im Repository.</p>
  <span class="plat-actions">
    <a href="https://snapcraft.io/hinata"><img class="b-snap b-snap-black" src="/assets/img/badges/snap-store-dark.svg" alt="Im Snap Store erhältlich"><img class="b-snap b-snap-white" src="/assets/img/badges/snap-store-light.svg" alt="Im Snap Store erhältlich"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg><strong>Web</strong></span>
  <span class="plat-status live">Enthalten</span>
  <p>Keine Installation. Dein Server liefert die Web-App selbst aus. Adresse öffnen und anmelden.</p>
  <span class="plat-actions">
    <a class="plat-link" href="/de/self-hosting.html">Wie du sie hostest</a>
  </span>
</li>
</ul>

!!! info "Eine App, viele Server"
    In der Hinata-App ist **keine Serveradresse fest eingebaut**. Derselbe Build
    verbindet sich mit dem Server deiner Firma, deines Vereins oder einer lokalen
    Testinstanz, jeweils mit eigener Sitzung. Den Server-Manager dafür erklärt
    [Die Apps](/de/clients.html).

## Was jede Plattform kann

Fast alles ist überall gleich. Das sind die Unterschiede:

| | Android | iOS | macOS | Windows | Linux | Web |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| Boards, Sprints, Vorgänge, Gantt, Berichte | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Push-Benachrichtigungen | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Benachrichtigungen in der App & per E-Mail | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Foto mit der Kamera aufnehmen | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Vorhandene Dateien anhängen | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sprachnachricht aufnehmen | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Über Neustarts angemeldet bleiben | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| `hinata://`-Deep-Links | ✅ | ✅ | ✅ | ✅ | ✅ | entfällt |

⚠️ heißt: Das funktioniert, sobald das System etwas bereitstellt, das die App
nicht mitbringen kann. Unter Linux brauchst du:

- **Angemeldet bleiben:** einen Schlüsselbund, der den Secret Service umsetzt
  (z. B. GNOME Keyring oder KWallet).
- **Sprachnachrichten abspielen:** die GStreamer-Plugin-Pakete.
- **Sprachnachrichten aufnehmen:** PulseAudio und FFmpeg.

Fehlt etwas, sagt die App dir, was. Details und Paketlisten stehen unter
[Die Apps](/de/clients.html#hinata-unter-linux).

!!! note "Warum es unter Linux kein Push gibt"
    Auf Mobilgeräten und unter Windows läuft Push über das
    [Hinata Connect Gateway](/de/connect-gateway.html) an FCM und WNS. Linux hat
    keinen vergleichbaren Dienst. Benachrichtigungen kommen dort in der App und
    per E-Mail an. Deine Benachrichtigungseinstellungen kannst du trotzdem ändern.
    Sie gehören zu deinem **Konto** und gelten auch für dein Handy.

## Nach der Installation

1. **Serveradresse eingeben.** Die App prüft, ob dort ein Hinata-Server antwortet,
   bevor sie weitermacht.
2. **Anmelden** mit deinen Zugangsdaten oder über das
   [Single Sign-on](/de/sso.html) deines Betreibers.
3. Fertig. Der Arbeitsbereich ist derselbe wie auf jedem anderen Gerät.

!!! tip "Aufgefordert zu aktualisieren?"
    Verlangt ein Server eine neuere App-Version, zeigt die App einen Button zum
    passenden Store. Betreiber hinterlegen diese Links pro Plattform im
    Adminbereich. Der Button führt also zu dem Store, aus dem du installiert hast.

Neu bei Hinata? Das [Handbuch](/de/guide-start.html) führt dich Schritt für
Schritt durch die App.
