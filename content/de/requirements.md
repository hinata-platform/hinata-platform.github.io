---
title: Voraussetzungen
description: Was du zum Selbst-Hosten von Hinata brauchst — Host-Dimensionierung, Docker Engine + Compose v2, Netzwerk und TLS, MongoDB-Replikatset, S3/MinIO, SMTP und Entwicklungsvoraussetzungen.
---

# Voraussetzungen

Hinata läuft bequem auf einem einzelnen, bescheidenen Server und skaliert von dort aus nach oben. Diese Seite listet auf, was der Host braucht, was jede Komponente erwartet und was du zum Bauen aus dem Quellcode benötigst.

## Host-Anforderungen

Der Server und seine Abhängigkeiten werden als Container ausgeliefert, daher braucht der Host hauptsächlich eine Container-Laufzeitumgebung und genug Reserve, um die JVM, MongoDB und MinIO nebeneinander zu betreiben.

| Ressource | Minimum | Empfohlen |
| --- | --- | --- |
| **CPU** | 2 Kerne (x86_64 oder arm64) | 4+ Kerne |
| **RAM** | 4 GB | 8 GB+ (die JVM + ein 3-Mitglieder-Replikatset sind die Hauptverbraucher) |
| **Festplatte** | 20 GB SSD | 50 GB+ SSD, wachsend mit Anhängen und Datenbankgröße |
| **OS** | Beliebiges Linux mit modernem Kernel | Eine stabile Server-Distribution, die du regelmäßig patchst |

- **Docker Engine + Docker Compose v2** sind die einzigen harten Software-Voraussetzungen. Die Compose-Dateien verwenden v2-Syntax (`docker compose`, nicht das veraltete `docker-compose`).
- **Architektur**: Images werden für **x86_64** und **arm64** veröffentlicht, sodass Apple Silicon, AWS Graviton und Raspberry-Pi-artige arm64-Geräte alle funktionieren.

!!! note "Anhänge treiben das Festplattenwachstum"
    Die Datenbank selbst bleibt schlank; die variable Größe ist der Objektspeicher. Anhänge und Avatare liegen in S3/MinIO, dimensioniere daher das Volume hinter MinIO (oder deinem externen Bucket) danach, wie viel deine Teams im Laufe der Zeit hochladen werden.

## Komponenten-Anforderungen

Ein produktiver Hinata-Stack ist eine Handvoll zusammenarbeitender Dienste. Hier ist, was jeder einzelne braucht.

| Komponente | Was sie braucht | Hinweise |
| --- | --- | --- |
| **Server (Spring Boot)** | JVM-Laufzeitumgebung (im Image), die Umgebung aus `.env` | Veröffentlicht die API; Host-Port `3356` standardmäßig |
| **MongoDB** | Ein **Replikatset** (2 Datenknoten + 1 Arbiter) in Prod, mit TLS + X.509 | Laufzeiteinstellungen und alle Daten liegen hier |
| **S3 / MinIO** | Ein S3-kompatibler Bucket (Standardname `hinata`) + Zugangsdaten | Anhänge, Avatare; vorsignierte Downloads |
| **SMTP-Relay** | Ein echtes ausgehendes Mail-Relay in Prod (Mailpit in Dev) | Verifizierung, Benachrichtigungen, Passwort-Reset |
| **Reverse Proxy** | Terminiert TLS, leitet an die Server-/App-Ports weiter | Öffentliches DNS + Zertifikat; siehe unten |
| **Hinata Connect Gateway** | *Optional* — das gehostete Gateway oder dein eigenes | Push-Benachrichtigungen + Universal Links |

### Netzwerk

- **Öffentliches DNS + TLS.** Für alles über einen lokalen Test hinaus brauchst du öffentliche DNS-Namen und TLS. Terminiere TLS an einem [Reverse Proxy](/de/reverse-proxy.html) und leite über die internen Ports an Hinata weiter. Typische Namen sind `api.track.example.com` (API) und `track.example.com` (Web-App).
- **Interne Ports.** Der Server veröffentlicht standardmäßig **`3356`** und der Web-/App-Container **`3456`** (`HINATA_PORT` / `HINATA_APP_PORT`). Das sind die Ports, an die dein Proxy weiterleitet; sie sollten nicht direkt dem Internet ausgesetzt werden.
- **Vertrauenswürdige Proxies.** Setze `HINATA_TRUSTED_PROXIES` auf die CIDRs deiner Reverse Proxies, damit `X-Forwarded-For` nur von diesen berücksichtigt wird. Leer bedeutet, keinem zu vertrauen.
- **CORS.** Die gehostete Web-App ruft die API cross-origin auf, liste daher deine Browser-Origins in `HINATA_CORS_ALLOWED_ORIGINS` auf.

!!! warning "TLS immer davor terminieren"
    Die internen Ports (`3356`/`3456`) sprechen einfaches HTTP und sind dafür gedacht, hinter einem TLS-terminierenden Proxy zu sitzen. Setze sie niemals direkt aus. Die App verlangt `https://` für gespeicherte Produktivserver.

### MongoDB-Replikatset

Produktives Hinata erwartet ein **Replikatset**, kein eigenständiges MongoDB, aus zwei Gründen: Es ist für die transaktionalen Garantien erforderlich, auf die sich Hinata stützt, und es ermöglicht einen sicheren rollierenden Betrieb. Das mitgelieferte Compose bringt **2 Datenknoten + 1 Arbiter** mit **TLS und X.509-Client-Authentifizierung** hoch. Die App authentifiziert sich gegenüber MongoDB mit einem X.509-Zertifikat — nicht mit dem SCRAM-Root-Passwort, das für interne/administrative Zwecke reserviert ist.

- Erzeuge das Cluster-Keyfile mit `./deploy/generate-secrets.sh`.
- Erzeuge die Produktiv-PKI mit `./deploy/x509/generate-certs.sh prod`, lege dann den X.509-Benutzer mit `./deploy/x509/init-prod-user.sh` an.

Vollständige Details findest du unter [MongoDB & X.509](/de/database.html).

### Objektspeicher

Hinata braucht einen Objektspeicher. Das gebündelte MinIO ist der einfache Standard (Bucket `HINATA_S3_BUCKET`, Standard `hinata`), konfiguriert mit `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`; in Dev werden zusätzlich `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` verwendet. Du kannst Hinata stattdessen auch auf jeden externen S3-kompatiblen Anbieter (AWS S3, Google Cloud Storage, Cloudflare R2, DigitalOcean Spaces, …) oder auf Azure Blob Storage (`HINATA_STORAGE_PROVIDER=azure`) ausrichten. Siehe [Objektspeicher](/de/storage.html).

### SMTP

Für echte Mail — E-Mail-Verifizierung, Benachrichtigungen und Passwort-Reset — konfiguriere ein ausgehendes **SMTP-Relay** mit `HINATA_SMTP_HOST/PORT/USERNAME/PASSWORD/AUTH/STARTTLS` und einer sinnvollen `HINATA_MAIL_FROM`. In der Entwicklung fängt **Mailpit** alles unter `http://localhost:8025` ab, sodass nichts die Maschine verlässt. Siehe [E-Mail & SMTP](/de/email.html).

### Hinata Connect Gateway (optional)

Push-Benachrichtigungen und Universal Links fließen durch das **Connect Gateway**, einen gehosteten Dienst. Seine Nutzung bedeutet, dass Selbst-Hoster **kein eigenes Firebase-Projekt** benötigen. Es ist optional; du kannst ohne Push betreiben oder deine eigene gebrandete App mit eigenem Gateway ausrollen und `HINATA_GATEWAY_BASE_URL` setzen. Siehe [Hinata Connect Gateway](/de/connect-gateway.html).

## Client-Anforderungen

Die [App](/de/clients.html) läuft auf:

- **Android**- und **iOS**-Smartphones/Tablets,
- **Web** (jeder moderne Browser),
- **macOS**-Desktop,
- **Windows**-Desktop,
- **Linux**-Desktop — ein nativer GTK-3-Build, installiert als Flatpak, als AppImage oder aus einem Bundle, das du selbst gebaut hast; ein Snap liegt im Snap Store, aber noch auf keinem Kanal. [Die Apps](/de/clients.html#hinata-unter-linux) nennt den aktuellen Installationsstand des Snaps.

Weil die App mehrserverfähig ist, brauchen Nutzer nur die URL eines laufenden Servers; keine benutzerbezogene Installationskonfiguration ist erforderlich.

### Was ein Linux-Desktop mitbringen muss

Der Linux-Client bindet sich an GTK, GStreamer und libsecret des Systems, statt eigene Kopien mitzuliefern — deshalb trägt er dein Theme und spielt mit den Codecs, die deine Distribution installiert hat. Die Kehrseite: Er setzt einen gewöhnlichen Desktop darunter voraus. Alles Folgende ist auf einer normalen GNOME- oder Plasma-Installation längst vorhanden; die Liste zählt für Container, minimale Fenstermanager und abgespeckte Images.

| Paket (Debian-/Ubuntu-Namen) | Wofür | Ohne das Paket |
| --- | --- | --- |
| `libgtk-3-0` | die App selbst | sie startet nicht |
| `libsecret-1-0` plus ein Schlüsselbund (GNOME Keyring, KWallet — alles, was den Secret Service spricht) | angemeldet bleiben über Neustarts hinweg | die Sitzung lebt nur, solange die App offen ist — und die App sagt das auch |
| `zenity`, `qarma` oder `kdialog` | die Dateiauswahl für Anhänge | die Auswahl nennt, welches der drei zu installieren ist |
| `pulseaudio-utils` und `ffmpeg` | Sprachkommentare aufnehmen | die Aufnahme startet nicht |
| `gstreamer1.0-plugins-base/good/bad` und `gstreamer1.0-libav` | Sprachkommentare abspielen | die Wiedergabe scheitert und nennt das fehlende Paket |

`gstreamer1.0-libav` sieht optional aus und ist es nicht: Sprachkommentare werden auf jeder Plattform als AAC aufgenommen, und libav bringt den passenden Decoder mit. Fehlt es, lädt die Sprachblase und weigert sich dann abzuspielen.

!!! note "Die fertigen Pakete bringen fast alles davon selbst mit"
    Das Flatpak sitzt auf der Freedesktop-Runtime, die GTK, zenity, GStreamer inklusive libav, libsecret und FFmpeg bereits enthält, und es baut PulseAudios Aufnahme-Werkzeuge selbst ins Paket. Das Snap sitzt auf dem GNOME-Platform-Snap und legt den Rest selbst dazu — `gstreamer1.0-plugins-bad`, `gstreamer1.0-libav`, `pulseaudio-utils`, `ffmpeg`; Dateien wählt es über das Desktop-Portal, `zenity` braucht es also ebenfalls nicht. Der Schlüsselbund ist in beiden Fällen das Stück, das weiterhin vom Host kommt — er gehört zur Anmeldesitzung des Nutzers, nicht zur Sandbox. Im Snap kommt dazu, dass er mit `snap connect hinata:password-manager-service` verbunden sein will, und die Aufnahme mit `snap connect hinata:audio-record`.

!!! info "Zwei Dinge, die Linux nicht kann"
    Es gibt **kein Push**: `firebase_messaging` hat keine Linux-Implementierung, und es existiert kein Desktop-Push-Dienst, bei dem sich die App registrieren könnte — Benachrichtigungen kommen deshalb in der App und per E-Mail an. Und es gibt **keine Webcam-Aufnahme** — für Linux existiert keine Kamera-Implementierung, deshalb bietet die App „Foto aufnehmen“ gar nicht erst an, statt beim Antippen zu scheitern. Vorhandene Dateien anzuhängen funktioniert genau wie überall sonst.

## Entwicklungsvoraussetzungen

Das Bauen aus dem Quellcode (statt Images zu ziehen) erfordert die Toolchains hinter jedem Repository:

- **[hinata-server](https://github.com/hinata-platform/hinata-server)** — **JDK 21** und der gebündelte Gradle-Wrapper (`./gradlew`). Bringe die Entwicklungsabhängigkeiten mit `docker compose -f docker-compose.dev.yml up -d` hoch (Mongo-Replikatset, Mailpit, MinIO) und starte dann den Server:

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

Führe die Testsuite mit `./gradlew build` aus.

- **[hinata-app](https://github.com/hinata-platform/hinata-app)** — ein **Flutter**-SDK plus die native Toolchain jedes Ziels, das du baust: das Android-SDK, Xcode für iOS und macOS, Visual Studio mit der Desktop-C++-Workload für Windows und die GTK-Entwicklungspakete für Linux. State über bloc/cubit, Routing über go_router, i18n über i18next.

### Das Linux-Desktop-Ziel bauen

Der Linux-Build kompiliert gegen Systembibliotheken, statt sie mitzuliefern — installiere daher zuerst deren Header, unter Debian oder Ubuntu:

```bash
sudo apt install \
  clang cmake ninja-build pkg-config \
  libgtk-3-dev liblzma-dev libsecret-1-dev libjsoncpp-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

Danach baust du es wie jedes andere Ziel:

```bash
flutter config --enable-linux-desktop
flutter build linux --release
```

Jedes Paket hat seinen Grund: `libgtk-3-dev` ist der Embedder und bringt die GTK-Druckunterstützung mit, auf der Drucken und PDF-Export aufsetzen, `libsecret-1-dev` trägt die sichere Token-Ablage, die eine Sitzung überhaupt am Leben hält, und die GStreamer-Header bauen die Audiowiedergabe, die Sprachkommentare brauchen. Zusätzlich brauchst du eine **Rust**-Toolchain ([rustup](https://rustup.rs)) — das Plugin für Zwischenablage und Drag & Drop ist eine Rust-Crate, die unter Linux aus dem Quellcode kompiliert und nicht vorgebaut ausgeliefert wird.

Heraus kommt ein verschiebbares Verzeichnis `build/linux/<arch>/release/bundle/` — das Binary `hinata` neben `data/` und `lib/` — und genau das packen die Flatpak- und AppImage-Rezepte in `packaging/linux/`.

!!! note "Baue Linux auf der ältesten Distribution, die du unterstützen willst"
    Ein Flutter-Bundle ist dynamisch gegen die glibc der Maschine gelinkt, die es gebaut hat, und glibc ist nur vorwärtskompatibel — ein auf einer brandneuen Distribution gebautes Binary startet auf einer älteren nicht. Genau deshalb pinnt Hinatas CI für den Linux-Job `ubuntu-22.04`: So ist die glibc-Untergrenze des Bundles eine Entscheidung und kein Zufall.

!!! tip "Willst du es nur zum Laufen bringen?"
    Du brauchst weder JDK noch Flutter, um Hinata zu *betreiben* — der [Schnellstart](/de/quick-start.html) zieht vorgefertigte Images. Die Entwicklungs-Toolchains sind nur für das Bauen aus dem Quellcode oder das Mitwirken. Siehe [Entwicklung](/de/development.html) und [Mitwirken](/de/contributing.html).

## Nächste Schritte

- [Schnellstart](/de/quick-start.html) — drei Befehle zu einem laufenden Stack.
- [Produktiv-Deployment](/de/deployment.html) — der vollständige Produktiv-Weg.
- [Reverse Proxy & TLS](/de/reverse-proxy.html) — öffentliches DNS, Zertifikate und Weiterleitung.
