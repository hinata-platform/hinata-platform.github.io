---
title: Voraussetzungen
description: Was du brauchst, um Hinata selbst zu hosten und aus dem Quellcode zu bauen.
---

# Voraussetzungen

Hinata läuft gut auf einem einzelnen kleinen Server und lässt sich von dort aus skalieren. Hier steht, was Host, Komponenten, Clients und Entwicklung brauchen.

## Anforderungen an den Host

Server und Abhängigkeiten laufen als Container. Der Host braucht also vor allem eine Container-Laufzeit und genug Reserven für JVM, MongoDB und MinIO.

| Ressource | Minimum | Empfohlen |
| --- | --- | --- |
| **CPU** | 2 Kerne (x86_64 oder arm64) | 4+ Kerne |
| **RAM** | 4 GB | 8 GB+ (JVM und Replikatset mit 3 Mitgliedern brauchen am meisten) |
| **Festplatte** | 20 GB SSD | 50 GB+ SSD, wächst mit Anhängen und Datenbankgröße |
| **OS** | Beliebiges Linux mit modernem Kernel | Eine stabile Serverdistribution, die du regelmäßig patchst |

- **Docker Engine + Docker Compose v2** sind die einzigen harten Softwarevoraussetzungen. Die Compose-Dateien nutzen v2-Syntax (`docker compose`, nicht das veraltete `docker-compose`).
- **Architektur**: Images gibt es für **x86_64** und **arm64**. Apple Silicon, AWS Graviton und arm64-Geräte wie der Raspberry Pi funktionieren.

!!! note "Anhänge treiben das Festplattenwachstum"
    Die Datenbank bleibt schlank. Was wächst, ist der Objektspeicher mit Anhängen und Avataren in S3/MinIO. Plane das Volume hinter MinIO (oder deinen externen Bucket) danach, wie viel deine Teams mit der Zeit hochladen.

## Anforderungen der Komponenten

Ein produktiver Stack besteht aus diesen Diensten:

| Komponente | Was sie braucht | Hinweise |
| --- | --- | --- |
| **Server (Spring Boot)** | JVM-Laufzeitumgebung (im Image), die Umgebung aus `.env` | Stellt die API bereit. Host-Port standardmäßig `3356` |
| **MongoDB** | Ein **Replikatset** (2 Datenknoten + 1 Arbiter) in Prod, mit TLS + X.509 | Laufzeiteinstellungen und alle Daten liegen hier |
| **S3 / MinIO** | Ein S3-kompatibler Bucket (Standardname `hinata`) + Zugangsdaten | Anhänge, Avatare, vorsignierte Downloads |
| **SMTP-Relay** | Ein echtes ausgehendes Mail-Relay in Prod (Mailpit in Dev) | Verifizierung, Benachrichtigungen, Passwort-Reset |
| **Reverse Proxy** | Terminiert TLS, leitet an die Ports von Server und App weiter | Öffentliches DNS + Zertifikat, siehe unten |
| **Hinata Connect Gateway** | *Optional*: das gehostete Gateway oder dein eigenes | Push-Benachrichtigungen + Universal Links |

### Netzwerk

- **Öffentliches DNS + TLS.** Außerhalb lokaler Tests brauchst du öffentliche DNS-Namen und TLS. Terminiere TLS an einem [Reverse Proxy](/de/reverse-proxy.html) und leite an die internen Ports weiter. Typisch sind `api.track.example.com` (API) und `track.example.com` (Web-App).
- **Interne Ports.** Standardmäßig nutzt der Server **`3356`** und der Web/App-Container **`3456`** (`HINATA_PORT` / `HINATA_APP_PORT`). Dein Proxy leitet dorthin weiter. Direkt ins Internet gehören diese Ports nicht.
- **Vertrauenswürdige Proxies.** Setze `HINATA_TRUSTED_PROXIES` auf die CIDRs deiner Reverse Proxies. Nur von dort wird `X-Forwarded-For` beachtet. Leer heißt: keinem vertrauen.
- **CORS.** Die gehostete Web-App ruft die API cross-origin auf. Trage deine Browser-Origins in `HINATA_CORS_ALLOWED_ORIGINS` ein.

!!! warning "TLS immer davor terminieren"
    Die internen Ports (`3356`/`3456`) sprechen reines HTTP und gehören hinter einen Proxy, der TLS terminiert. Gib sie nie direkt frei. Für gespeicherte Produktivserver verlangt die App `https://`.

### MongoDB-Replikatset

Produktiv braucht Hinata ein **Replikatset** statt einer einzelnen MongoDB. Es ist nötig für die Transaktionsgarantien, auf die Hinata baut, und erlaubt sicheren rollierenden Betrieb.

Das mitgelieferte Compose startet **2 Datenknoten + 1 Arbiter** mit **TLS und X.509-Client-Authentifizierung**. Die App meldet sich per X.509-Zertifikat an. Das SCRAM-Root-Passwort bleibt für interne und administrative Zwecke.

- Cluster-Keyfile erzeugen: `./deploy/generate-secrets.sh`
- Produktiv-PKI erzeugen: `./deploy/x509/generate-certs.sh prod`, danach den X.509-Benutzer mit `./deploy/x509/init-prod-user.sh` anlegen.

Details findest du unter [MongoDB & X.509](/de/database.html).

### Objektspeicher

Hinata braucht einen Objektspeicher:

- **Gebündeltes MinIO** ist der einfache Standard: Bucket `HINATA_S3_BUCKET` (Standard `hinata`), Zugang über `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`. In Dev kommen `HINATA_S3_ACCESS_KEY` / `HINATA_S3_SECRET_KEY` dazu.
- **Externer S3-kompatibler Anbieter**: AWS S3, Google Cloud Storage, Cloudflare R2, DigitalOcean Spaces, …
- **Azure Blob Storage**: `HINATA_STORAGE_PROVIDER=azure`.

Siehe [Objektspeicher](/de/storage.html).

### SMTP

Für E-Mail-Verifizierung, Benachrichtigungen und Passwort-Reset brauchst du ein ausgehendes **SMTP-Relay**. Konfiguriere es mit `HINATA_SMTP_HOST/PORT/USERNAME/PASSWORD/AUTH/STARTTLS` und einer passenden `HINATA_MAIL_FROM`. In der Entwicklung fängt **Mailpit** alle Mails unter `http://localhost:8025` ab, damit nichts den Rechner verlässt. Siehe [E-Mail & SMTP](/de/email.html).

### Hinata Connect Gateway (optional)

Push-Benachrichtigungen und Universal Links laufen über das gehostete **Connect Gateway**. Damit brauchst du **kein eigenes Firebase-Projekt**. Du kannst auch ohne Push arbeiten oder eine eigene App unter deiner Marke mit eigenem Gateway ausrollen und `HINATA_GATEWAY_BASE_URL` setzen. Siehe [Hinata Connect Gateway](/de/connect-gateway.html).

## Anforderungen an die Clients

Die [App](/de/clients.html) läuft auf:

- **Android** und **iOS** (Smartphones und Tablets),
- **Web** (jeder moderne Browser),
- **macOS**,
- **Windows**,
- **Linux** als nativer GTK-3-Build. Am schnellsten geht `sudo snap install hinata` aus dem Snap Store (x86-64 und ARM64). Die Rezepte für Flatpak und AppImage bauen dieselbe App. [Die Apps](/de/clients.html#hinata-unter-linux) nennt die zwei Berechtigungen, die du beim Snap von Hand verbinden musst.

Die App kann mit mehreren Servern arbeiten. Nutzer brauchen nur die URL eines laufenden Servers, sonst keine Einrichtung.

### Was ein Linux-Desktop mitbringen muss

Der Linux-Client nutzt GTK, GStreamer und libsecret des Systems. Deshalb übernimmt er dein Theme und die Codecs deiner Distribution. Dafür braucht er einen normalen Desktop. Auf GNOME oder Plasma ist alles schon da. Die Liste ist für Container, minimale Fenstermanager und abgespeckte Images wichtig.

| Paket (Debian-/Ubuntu-Namen) | Wofür | Ohne das Paket |
| --- | --- | --- |
| `libgtk-3-0` | die App selbst | sie startet nicht |
| `libsecret-1-0` plus ein Schlüsselbund (GNOME Keyring, KWallet oder alles, was den Secret Service spricht) | angemeldet bleiben über Neustarts hinweg | die Sitzung endet, wenn die App geschlossen wird (die App weist darauf hin) |
| `zenity`, `qarma` oder `kdialog` | die Dateiauswahl für Anhänge | die Auswahl nennt, welches der drei zu installieren ist |
| `pulseaudio-utils` und `ffmpeg` | Sprachkommentare aufnehmen | die Aufnahme startet nicht |
| `gstreamer1.0-plugins-base/good/bad` und `gstreamer1.0-libav` | Sprachkommentare abspielen | die Wiedergabe scheitert und nennt das fehlende Paket |

Auch `gstreamer1.0-libav` ist Pflicht. Sprachkommentare werden auf jeder Plattform als AAC aufgenommen, und libav liefert den Decoder dafür. Fehlt es, lädt die Sprachblase, spielt aber nicht ab.

!!! note "Die fertigen Pakete bringen fast alles davon selbst mit"

    - **Flatpak**: Die Freedesktop-Runtime enthält GTK, zenity, GStreamer mit libav, libsecret und FFmpeg. Die Aufnahmewerkzeuge von PulseAudio baut das Paket selbst ein.
    - **Snap**: Es baut auf dem GNOME-Platform-Snap auf und bringt `gstreamer1.0-plugins-bad`, `gstreamer1.0-libav`, `pulseaudio-utils` und `ffmpeg` selbst mit. Dateien wählt es über das Desktop-Portal, `zenity` ist also nicht nötig.

    Den Schlüsselbund liefert in beiden Fällen der Host, weil er zur Anmeldesitzung des Nutzers gehört und nicht zur Sandbox. Beim Snap musst du ihn mit `snap connect hinata:password-manager-service` verbinden, die Aufnahme mit `snap connect hinata:audio-record`.

!!! info "Zwei Dinge, die Linux nicht kann"

    - Es gibt **kein Push**. `firebase_messaging` hat keine Linux-Implementierung, und es gibt keinen Push-Dienst für den Desktop. Benachrichtigungen kommen in der App und per E-Mail an.
    - Es gibt **keine Webcam-Aufnahme**. Für Linux existiert keine Kamera-Implementierung, deshalb bietet die App „Foto aufnehmen“ gar nicht erst an. Vorhandene Dateien anhängen funktioniert wie überall.

## Entwicklungsvoraussetzungen

Zum Bauen aus dem Quellcode brauchst du die Toolchains der einzelnen Repositories:

- **[hinata-server](https://github.com/hinata-platform/hinata-server)**: **JDK 21** und der mitgelieferte Gradle-Wrapper (`./gradlew`). Starte die Entwicklungsdienste (Mongo-Replikatset, Mailpit, MinIO) und dann den Server:

```bash
docker compose -f docker-compose.dev.yml up -d   # Mongo RS, Mailpit, MinIO
HINATA_MONGODB_URI="mongodb://localhost:27017/hinata?replicaSet=rs0&directConnection=true" \
HINATA_S3_ACCESS_KEY=hinata HINATA_S3_SECRET_KEY=hinata-dev-secret \
./gradlew bootRun
```

Die Tests laufen mit `./gradlew build`.

- **[hinata-app](https://github.com/hinata-platform/hinata-app)**: ein **Flutter**-SDK und die native Toolchain jedes Ziels, das du baust. Das sind das Android SDK, Xcode für iOS und macOS, Visual Studio mit der Workload für Desktopentwicklung mit C++ für Windows und die GTK-Entwicklungspakete für Linux. State über bloc/cubit, Routing über go_router, i18n über i18next.

### Für den Linux-Desktop bauen

Der Linux-Build kompiliert gegen Systembibliotheken. Installiere zuerst deren Header, unter Debian oder Ubuntu:

```bash
sudo apt install \
  clang cmake ninja-build pkg-config \
  libgtk-3-dev liblzma-dev libsecret-1-dev libjsoncpp-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

Dann baust du wie für jedes andere Ziel:

```bash
flutter config --enable-linux-desktop
flutter build linux --release
```

Wofür die Pakete gebraucht werden:

- `libgtk-3-dev`: der Embedder, inklusive GTK-Druckunterstützung für Drucken und PDF-Export.
- `libsecret-1-dev`: die sichere Ablage der Tokens, ohne die keine Sitzung bestehen bleibt.
- GStreamer-Header: die Audiowiedergabe für Sprachkommentare.

Außerdem brauchst du eine **Rust**-Toolchain ([rustup](https://rustup.rs)). Das Plugin für Zwischenablage und Drag & Drop ist eine Rust-Crate und wird unter Linux aus dem Quellcode kompiliert.

Ergebnis ist das verschiebbare Verzeichnis `build/linux/<arch>/release/bundle/` mit dem Binary `hinata` neben `data/` und `lib/`. Genau das packen die Flatpak- und AppImage-Rezepte in `packaging/linux/`.

!!! note "Baue Linux auf der ältesten Distribution, die du unterstützen willst"
    Ein Flutter-Bundle ist dynamisch gegen die glibc des Rechners gelinkt, der es gebaut hat. glibc ist nur vorwärtskompatibel: Ein Binary von einer neuen Distribution startet auf einer älteren nicht. Hinatas CI pinnt den Linux-Job deshalb auf `ubuntu-22.04`. So ist die glibc-Untergrenze des Bundles bewusst gewählt.

!!! tip "Willst du es nur zum Laufen bringen?"
    Zum *Betreiben* von Hinata brauchst du weder JDK noch Flutter. Der [Schnellstart](/de/quick-start.html) zieht fertige Images. Die Toolchains brauchst du nur zum Bauen aus dem Quellcode oder zum Mitwirken. Siehe [Entwicklung](/de/development.html) und [Mitwirken](/de/contributing.html).

## Nächste Schritte

- [Schnellstart](/de/quick-start.html): drei Befehle bis zum laufenden Stack.
- [Produktiv-Deployment](/de/deployment.html): der vollständige Weg in die Produktion.
- [Reverse Proxy & TLS](/de/reverse-proxy.html): öffentliches DNS, Zertifikate und Weiterleitung.
