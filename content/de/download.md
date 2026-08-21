---
title: Download
description: Hol dir die Hinata-App für Android, iOS, macOS, Windows, Linux oder das Web — woher jeder Build kommt, was er auf der jeweiligen Plattform kann und was du vor dem Anmelden brauchst.
---

# Hinata herunterladen

Hinata ist ein Client für **deinen eigenen Server** — die App zu installieren ist
also nur die halbe Miete: Das Erste, wonach sie fragt, ist eine Server-Adresse.
Wenn dir noch niemand eine eingerichtet hat, fang bei
[Self-Hosting](/de/self-hosting.html) an; es braucht eine Docker-Compose-Datei
und ein paar Minuten.

Die App ist eine Flutter-Codebasis, sechsfach kompiliert. Dieselben Bildschirme,
dieselben Daten, dieselben Tastenkürzel — egal, wo du sie öffnest.

## App holen

<ul class="plat-grid">
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg><strong>Android</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Für Handy und Tablet, mit Push-Benachrichtigungen und der vollständigen Navigation.</p>
  <span class="plat-actions">
    <a href="https://play.google.com/store/apps/details?id=com.ahmadre.hinata"><img class="b-play" src="/assets/img/badges/google-play.png" alt="Jetzt bei Google Play"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg><strong>iOS</strong></span>
  <span class="plat-status soon">In Prüfung</span>
  <p>Der Build für iPhone und iPad liegt bei der App-Review. Die Seite unten ist bereits online — sie führt bis zur Freigabe zur Mac-App.</p>
  <span class="plat-actions">
    <a class="plat-link" href="https://apps.apple.com/us/app/hinata/id6781889251">Zur Store-Seite</a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/></svg><strong>macOS</strong></span>
  <span class="plat-status live">Verfügbar</span>
  <p>Ein nativer Desktop-Client, notarisiert und über den Mac App Store verteilt.</p>
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
  <p>Ein nativer GTK-3-Client, streng isoliert, für x86-64 und ARM64. Die Rezepte für Flatpak und AppImage bleiben im Repository, wer die lieber mag.</p>
  <span class="plat-actions">
    <a href="https://snapcraft.io/hinata"><img class="b-snap b-snap-black" src="/assets/img/badges/snap-store-dark.svg" alt="Im Snap Store erhältlich"><img class="b-snap b-snap-white" src="/assets/img/badges/snap-store-light.svg" alt="Im Snap Store erhältlich"></a>
  </span>
</li>
<li class="plat-card glass">
  <span class="plat-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg><strong>Web</strong></span>
  <span class="plat-status live">Enthalten</span>
  <p>Nichts zu installieren. Dein Server liefert die Web-App selbst aus — Adresse öffnen und anmelden.</p>
  <span class="plat-actions">
    <a class="plat-link" href="/de/self-hosting.html">Wie du sie hostest</a>
  </span>
</li>
</ul>

!!! info "Eine App, viele Server"
    In einer veröffentlichten Hinata-App ist **keine Server-Adresse einkompiliert**.
    Derselbe Build aus demselben Store verbindet sich mit dem Server deiner Firma,
    dem deines Vereins und einer lokalen Testinstanz — jeder mit eigener Sitzung.
    [Die Apps](/de/clients.html) beschreibt den Server-Manager, der sie
    auseinanderhält.

## Was jede Plattform kann

Fast alles ist überall identisch. Das hier sind die Unterschiede, die du vor der
Wahl deines Arbeitsplatzes kennen solltest — und jeder hat einen Grund statt
eines Eintrags auf einer Roadmap.

| | Android | iOS | macOS | Windows | Linux | Web |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| Boards, Sprints, Vorgänge, Gantt, Berichte | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Push-Benachrichtigungen | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Benachrichtigungen in der App & per E-Mail | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Foto mit der Kamera aufnehmen | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Vorhandene Dateien anhängen | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sprachnachricht aufnehmen | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Über Neustarts angemeldet bleiben | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| `hinata://`-Deep-Links | ✅ | ✅ | ✅ | ✅ | ✅ | — |

⚠️ heißt: Es funktioniert, sobald das System etwas bereitstellt, das die App nicht
selbst mitbringen kann. Unter Linux braucht das Angemeldetbleiben einen
Schlüsselbund (GNOME Keyring, KWallet — alles, was den Secret Service umsetzt),
und Sprachnachrichten brauchen die GStreamer-Plugin-Pakete zum Abspielen sowie
PulseAudio und FFmpeg zum Aufnehmen. Die App benennt das fehlende Teil, statt
stillschweigend nichts zu tun. [Die Apps](/de/clients.html#hinata-unter-linux)
hat die Details und die Paketlisten.

!!! note "Warum es unter Linux kein Push gibt"
    Push wird auf Mobilgeräten und unter Windows über das
    [Hinata Connect Gateway](/de/connect-gateway.html) an FCM und WNS
    weitergereicht. Ein Linux-Desktop hat keinen vergleichbaren Dienst, bei dem
    sich ein Token registrieren ließe — Benachrichtigungen kommen dort also in der
    App und per E-Mail an. Deine Benachrichtigungseinstellungen bleiben trotzdem
    bedienbar: Sie gehören zu deinem **Konto**, nicht zu dem Gerät, an dem du
    gerade sitzt, und steuern weiterhin dein Handy.

## Nach der Installation

1. **Server-Adresse eingeben.** Die App prüft, ob dort etwas antwortet, bevor sie
   weitergeht — du kannst also nie halb mit etwas verbunden sein, das gar kein
   Hinata-Server ist.
2. **Anmelden** mit deinen Zugangsdaten oder über das
   [Single Sign-on](/de/sso.html), das dein Betreiber eingerichtet hat.
3. Das war's — der Arbeitsbereich ist derselbe wie auf jedem anderen Gerät.

!!! tip "Aufgefordert zu aktualisieren?"
    Verlangt ein Server eine neuere App-Version, sagt die App das und bietet einen
    Button direkt zur richtigen Stelle für deine Plattform. Betreiber hinterlegen
    diese Links pro Plattform im Adminbereich — der Button führt also zu dem Store,
    aus dem du tatsächlich installiert hast.

Neu bei Hinata? Das [Handbuch](/de/guide-start.html) führt dich Bildschirm für
Bildschirm durch die App.
