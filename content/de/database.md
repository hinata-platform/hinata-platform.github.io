---
title: MongoDB & X.509
description: Wie Hinata MongoDB betreibt — ein Produktiv-Replikatset mit TLS und X.509-Client-Authentifizierung, samt der PKI-Skripte, die jedes Zertifikat erzeugen.
---

# MongoDB & X.509

Hinata speichert alles — Projekte, Vorgänge, Kommentare, Wissensdatenbank-Artikel,
Laufzeiteinstellungen — in **MongoDB**. In der Produktion läuft sie als
**Replikatset** mit **TLS-Verschlüsselung** und **X.509-Client-Authentifizierung**,
dem MongoDB-„Goldstandard" für ein selbstgehostetes Cluster. Diese Seite erklärt
warum, wie die Topologie aufgebaut ist und was die Deploy-Skripte im Server-Repo
genau tun, damit du das Setup nachvollziehen und ihm vertrauen kannst.

!!! info
    Alle folgenden Befehle liegen im Server-Repo unter `deploy/`. Es sind schlichte
    `openssl`/`mongosh`-Skripte — nichts Magisches — du kannst sie also lesen, bevor
    du sie ausführst.

## Warum ein Replikatset

Ein einzelnes `mongod` reicht, um Daten zu *speichern*, aber Hinata setzt in der
Produktion bewusst auf ein Replikatset — aus zwei Gründen:

- **Mehrdokumenten-Transaktionen.** Operationen, die alles-oder-nichts sein müssen —
  etwa das Abschließen eines Sprints samt Verschieben seiner Vorgänge — nutzen
  MongoDB-Transaktionen. Die bietet MongoDB nur auf einem Replikatset, nie auf einem
  Einzelknoten.
- **Hochverfügbarkeit.** Mit zwei datenhaltenden Knoten und einem Arbiter übersteht
  das Cluster den Ausfall eines Datenknotens: Der verbleibende Knoten wird zum
  Primary gewählt und der Server läuft weiter.

!!! note "SSE wird in der App verarbeitet, nicht von Mongo"
    Hinatas Live-Anhang-Updates nutzen In-Process-Server-Sent-Events, keine
    Mongo-Change-Streams — das SSE-Feature selbst hängt also nicht vom Replikatset
    ab. Beim Replikatset geht es um Transaktionen und Verfügbarkeit.

## Produktiv-Topologie

Die Produktiv-`docker-compose.yml` bringt drei MongoDB-Container in einem privaten
Docker-Netzwerk hoch:

| Container | Rolle | Daten | Stimme |
| --- | --- | --- | --- |
| `mongo1` | Datenknoten (Priorität 2 — bevorzugter Primary) | ja (`mongo1-data`-Volume) | ja |
| `mongo2` | Datenknoten (Priorität 1) | ja (`mongo2-data`-Volume) | ja |
| `mongo-arbiter` | Arbiter — nur Wahl-Zünglein an der Waage | **keine** | ja |

Der Arbiter hält keine Daten; er existiert nur, damit Wahlen eine ungerade Anzahl
Stimmberechtigter haben, ohne für eine dritte volle Kopie zu zahlen. Jeder Knoten
läuft mit demselben Befehl:

```yaml
command: >-
  mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongo/keyfile
  --tlsMode requireTLS
  --tlsCertificateKeyFile /etc/mongo/certs/server.pem
  --tlsCAFile /etc/mongo/certs/ca.crt
```

Hier sind zwei unabhängige Authentifizierungsebenen im Spiel:

- **`--keyFile`** — ein geteiltes Geheimnis, mit dem sich die Replikatset-Mitglieder
  *gegenseitig* authentifizieren (interne Cluster-Auth, SCRAM).
- **`--tlsMode requireTLS` + `--tlsCAFile`** — jede *Client*-Verbindung muss TLS
  verwenden **und** ein Zertifikat vorlegen, das von der CA des Clusters signiert
  ist. Genau das ermöglicht die X.509-Client-Authentifizierung.

Das Replikatset wird beim ersten gesunden Start von `mongo1` automatisch
initialisiert — sein Docker-Healthcheck ruft `rs.initiate(...)` mit den drei
Mitgliedern auf, falls das Set noch nicht konfiguriert ist. Du musst das also nie
von Hand tun.

## Zwei Wege der App-Authentifizierung: SCRAM-Root vs. App-X.509

Es gibt zwei verschiedene MongoDB-Identitäten, die man nicht verwechseln sollte:

- **`MONGO_ROOT_USERNAME` / `MONGO_ROOT_PASSWORD`** — ein klassisches
  SCRAM-Root-Konto, das das Mongo-Image erzeugt (`MONGO_INITDB_ROOT_*`). Es ist
  *rein administrativ*: Es initialisiert das Replikatset und registriert den
  X.509-Benutzer. Der Hinata-Server nutzt es nie.
- **Der Anwendungs-X.509-Benutzer** — der Server authentifiziert sich mit einem
  **Client-Zertifikat**, nicht mit einem Passwort. Sein Benutzername *ist* der
  Subject-DN des Zertifikats und liegt in der speziellen
  `$external`-Authentifizierungsdatenbank.

Deshalb trägt der Produktiv-Verbindungsstring gar kein Passwort:

```text
mongodb://mongo1:27017,mongo2:27017/hinata?replicaSet=rs0&tls=true&authMechanism=MONGODB-X509&authSource=$external
```

Diese URI wird für dich in der `docker-compose.yml` gesetzt (als
`HINATA_MONGODB_URI` am Server-Container). Das Zertifikat, das der Server vorlegt,
stammt aus dem JVM-Keystore aus `HINATA_MONGO_TLS_KEYSTORE`, und er validiert das
Cluster mit dem Truststore aus `HINATA_MONGO_TLS_TRUSTSTORE`.

## Keyfile und PKI erzeugen

Drei Skripte erzeugen alles. Führe sie für einen frischen Produktivhost in dieser
Reihenfolge aus.

### 1. Replikatset-Keyfile und Vorschläge für Geheimnisse

```bash
cp .env.example .env
./deploy/generate-secrets.sh
```

`generate-secrets.sh` erstellt `deploy/mongo-keyfile` (`openssl rand -base64 756`,
Modus `400`), falls es noch nicht existiert — ein bestehendes überschreibt es nicht —
und gibt einfügefertige Werte für `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD` und
`MINIO_ROOT_PASSWORD` aus. Kopiere diese in deine `.env`.

### 2. Die X.509-Zertifizierungsstelle und die Zertifikate

```bash
./deploy/x509/generate-certs.sh prod
```

Das baut eine in sich geschlossene PKI unter `deploy/x509/prod/`:

| Datei | Was es ist |
| --- | --- |
| `ca.crt` / `ca.key` | Die private Zertifizierungsstelle (4096-Bit-RSA, 10 Jahre gültig) |
| `server.pem` | Das TLS-Cert + Key von `mongod`; sein SAN deckt `mongo1`, `mongo2`, `mongo-arbiter` ab |
| `hinata-app.p12` | JVM-**Keystore** — Client-Zertifikat + Key der App |
| `truststore.p12` | JVM-**Truststore** — nur die CA |
| `app-subject-dn.txt` | Der Subject-DN des Client-Certs = der Mongo-`$external`-Benutzername |
| `keyfile` | Ein Replikatset-Internal-Auth-Keyfile (nur prod) |

Das Anwendungszertifikat wird bewusst mit einer anderen Organizational Unit
(`OU=Hinata Application`) ausgestellt als das Server-/Mitglieds-Zertifikat, sodass
`mongod` es als normalen X.509-**Benutzer** behandelt und nicht als Cluster-Mitglied.

!!! warning "Die CA auf einem laufenden Cluster nicht neu erzeugen"
    `generate-certs.sh` überschreibt eine bestehende CA nur mit `--force`, denn ein
    Austausch der CA würde augenblicklich jedes Zertifikat ungültig machen, dem das
    laufende Cluster bereits vertraut. Nutze `--force` nur bei einem frischen Setup.

### 3. Den X.509-Benutzer registrieren

Bring die Datenknoten hoch und erstelle dann den `$external`-Benutzer, der zum DN des
App-Zertifikats gehört:

```bash
docker compose up -d mongo1 mongo2 mongo-arbiter
./deploy/x509/init-prod-user.sh
docker compose up -d hinata-server
```

`init-prod-user.sh` verbindet sich als SCRAM-Root-Konto (aus deiner `.env`) über TLS
und ruft `createUser` in `$external` mit dem DN aus `app-subject-dn.txt` auf, wobei
es `readWrite` und `dbAdmin` auf der `hinata`-Datenbank vergibt. Es ist idempotent —
existiert der Benutzer bereits, sagt es das und macht weiter.

## Die Dev-Datenbank (standalone, trotzdem TLS + X.509)

Die lokale Entwicklung läuft **nicht** als Replikatset.
`docker-compose.dev.yml` startet ein einzelnes standalone `mongod` — behält aber
dieselbe Sicherheitshaltung: `requireTLS`, `--auth` und nur X.509-Client-Zugriff. Ein
Befehl richtet alles ein:

```bash
./deploy/x509/setup-dev.sh
SPRING_PROFILES_ACTIVE=dev ./mvnw spring-boot:run
```

`setup-dev.sh` erzeugt die Dev-PKI (`deploy/x509/dev/`), startet das Dev-Mongo,
erstellt den `$external`-X.509-Benutzer über die Localhost-Ausnahme und prüft, dass
der X.509-Login funktioniert. `application-dev.yml` zeigt bereits auf die
TLS/X.509-Verbindung, du setzt `HINATA_MONGODB_URI` also nicht selbst.

!!! note "Dev bindet nur an Loopback"
    Das Dev-Mongo veröffentlicht `127.0.0.1:27017` — niemals `0.0.0.0` — eine
    Entwicklungsdatenbank ist also nie aus dem Netzwerk erreichbar.

## Keystore- und Truststore-Passwörter

Der JVM-Keystore und -Truststore sind PKCS#12-Dateien, geschützt durch Passwörter,
die du kontrollierst:

| Variable | Schützt | Standard |
| --- | --- | --- |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | `hinata-app.p12` (Client-Cert + Key) | `changeit` |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | `truststore.p12` (die CA) | `changeit` |

`generate-certs.sh` liest diese beiden Variablen beim Bau der `.p12`-Dateien. Wenn du
also andere Passwörter willst, exportiere sie **vor** dem Erzeugen der Zertifikate:

```bash
export HINATA_MONGO_TLS_KEYSTORE_PASSWORD='ein-langer-zufaelliger-wert'
export HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD='ein-weiterer-langer-zufaelliger-wert'
./deploy/x509/generate-certs.sh prod
```

Setze dann dieselben Werte in `.env`, damit der Server die Stores zur Laufzeit öffnen
kann.

!!! danger "Ändere jeden Standard vor dem Livegang"
    `changeit`, `hinata-dev-secret` und das Beispiel-`MONGO_ROOT_PASSWORD` in
    `.env.example` sind Entwicklungs-Bequemlichkeiten. Erzeuge frische Geheimnisse mit
    `./deploy/generate-secrets.sh` und setze echte Keystore-Passwörter für jedes ans
    Internet gerichtete Deployment.

## Datenpersistenz und Betriebssicherheit

- **Benannte Volumes.** Jeder Datenknoten schreibt in ein benanntes Docker-Volume
  (`mongo1-data`, `mongo2-data`), sodass deine Daten Container-Neustarts,
  Image-Upgrades und `docker compose up`-Neuaufbauten überstehen. Das Entfernen
  dieser Volumes (`docker compose down -v`) zerstört die Datenbank — tu das nicht.
- **Mongo nie öffentlich exponieren.** Die Replikatset-Ports bleiben im internen
  `hinata`-Docker-Netzwerk. Nichts im Standard-Compose veröffentlicht `27017` in der
  Produktion zum Host. Nur der Server (hinter deinem Reverse Proxy) sollte die
  Datenbank erreichen.
- **Der Arbiter ist kein Backup.** Er speichert keine Daten. Echte Backups kommen aus
  `mongodump`/Volume-Snapshots — siehe [Backups & Upgrades](/de/backups.html).

Zum umgebenden Stack — Objektspeicher, Mail und Reverse Proxy — siehe
[Objektspeicher (S3/MinIO)](/de/storage.html),
[E-Mail & SMTP](/de/email.html) und
[Reverse Proxy & TLS](/de/reverse-proxy.html). Jede Umgebungsvariable ist in der
[Konfigurationsreferenz](/de/configuration.html) katalogisiert.
