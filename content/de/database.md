---
title: MongoDB & X.509
description: So betreibt Hinata MongoDB in der Produktion, als Replikatset mit TLS und X.509 samt den Skripten für alle Zertifikate.
---

# MongoDB & X.509

Hinata speichert alles in **MongoDB**: Projekte, Vorgänge, Kommentare, Artikel der Wissensdatenbank und Laufzeiteinstellungen. In der Produktion läuft MongoDB als **Replikatset** mit **TLS** und **X.509** für die Anmeldung der Clients.

!!! info
    Alle Befehle liegen im Server-Repo unter `deploy/`. Es sind einfache `openssl`- und `mongosh`-Skripte, die du vorher lesen kannst.

## Warum ein Replikatset

- **Transaktionen über mehrere Dokumente.** Manches muss ganz oder gar nicht passieren, etwa einen Sprint abschließen und seine Vorgänge verschieben. MongoDB kann Transaktionen nur im Replikatset, nie auf einem Einzelknoten.
- **Hochverfügbarkeit.** Zwei Datenknoten und ein Arbiter überstehen den Ausfall eines Datenknotens. Der andere wird Primary, und der Server läuft weiter.

!!! note "SSE wird in der App verarbeitet, nicht von Mongo"
    Live-Updates für Anhänge laufen über Server-Sent Events im Serverprozess, nicht über Change Streams. SSE braucht also kein Replikatset.

## Produktiv-Topologie

Die `docker-compose.yml` für die Produktion startet drei MongoDB-Container in einem privaten Docker-Netzwerk:

| Container | Rolle | Daten | Stimme |
| --- | --- | --- | --- |
| `mongo1` | Datenknoten (Priorität 2, bevorzugter Primary) | ja (Volume `mongo1-data`) | ja |
| `mongo2` | Datenknoten (Priorität 1) | ja (Volume `mongo2-data`) | ja |
| `mongo-arbiter` | Arbiter, entscheidet nur bei Wahlen | **keine** | ja |

Der Arbiter hält keine Daten. Er sorgt nur für eine ungerade Zahl an Stimmen, ohne dritte volle Kopie. Alle Knoten starten mit demselben Befehl:

```yaml
command: >-
  mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongo/keyfile
  --tlsMode requireTLS
  --tlsCertificateKeyFile /etc/mongo/certs/server.pem
  --tlsCAFile /etc/mongo/certs/ca.crt
```

Zwei unabhängige Ebenen der Authentifizierung:

- **`--keyFile`:** gemeinsames Geheimnis, mit dem sich die Mitglieder *untereinander* anmelden (interne Cluster-Auth, SCRAM).
- **`--tlsMode requireTLS` + `--tlsCAFile`:** jede *Client*-Verbindung braucht TLS **und** ein Zertifikat, das die CA des Clusters signiert hat. Das ermöglicht X.509 für Clients.

Beim ersten gesunden Start von `mongo1` ruft der Healthcheck `rs.initiate(...)` mit den drei Mitgliedern auf, falls das Set noch nicht eingerichtet ist. Von Hand musst du nichts tun.

## Zwei Wege der App-Authentifizierung: SCRAM-Root vs. App-X.509

- **`MONGO_ROOT_USERNAME` / `MONGO_ROOT_PASSWORD`:** ein klassisches SCRAM-Root-Konto aus dem Mongo-Image (`MONGO_INITDB_ROOT_*`). Es ist *nur zur Verwaltung* da: Es richtet das Replikatset ein und registriert den X.509-Benutzer. Der Hinata-Server nutzt es nie.
- **Der X.509-Benutzer der Anwendung:** Der Server meldet sich mit einem **Client-Zertifikat** an, ohne Passwort. Sein Benutzername *ist* der Subject-DN des Zertifikats und liegt in der speziellen Datenbank `$external`.

Der Verbindungsstring enthält deshalb kein Passwort:

```text
mongodb://mongo1:27017,mongo2:27017/hinata?replicaSet=rs0&tls=true&authMechanism=MONGODB-X509&authSource=$external
```

Die `docker-compose.yml` setzt ihn als `HINATA_MONGODB_URI` am Server-Container. Das Zertifikat des Servers kommt aus dem JVM-Keystore in `HINATA_MONGO_TLS_KEYSTORE`. Das Cluster prüft er mit dem Truststore aus `HINATA_MONGO_TLS_TRUSTSTORE`.

## Keyfile und PKI erzeugen

Führe die drei Skripte auf einem neuen Produktivhost in dieser Reihenfolge aus.

### 1. Replikatset-Keyfile und Vorschläge für Geheimnisse

```bash
cp .env.example .env
./deploy/generate-secrets.sh
```

`generate-secrets.sh` legt `deploy/mongo-keyfile` an (`openssl rand -base64 756`, Modus `400`), falls es fehlt. Ein vorhandenes überschreibt es nicht. Außerdem gibt es Werte für `HINATA_JWT_SECRET`, `MONGO_ROOT_PASSWORD` und `MINIO_ROOT_PASSWORD` aus, die du in `.env` kopierst.

### 2. Die X.509-Zertifizierungsstelle und die Zertifikate

```bash
./deploy/x509/generate-certs.sh prod
```

Das erzeugt eine eigenständige PKI unter `deploy/x509/prod/`:

| Datei | Was es ist |
| --- | --- |
| `ca.crt` / `ca.key` | Die private Zertifizierungsstelle (RSA mit 4096 Bit, 10 Jahre gültig) |
| `server.pem` | TLS-Zertifikat und Key von `mongod`. Das SAN deckt `mongo1`, `mongo2`, `mongo-arbiter` ab |
| `hinata-app.p12` | JVM-**Keystore**: Client-Zertifikat und Key der App |
| `truststore.p12` | JVM-**Truststore**: nur die CA |
| `app-subject-dn.txt` | Subject-DN des Client-Zertifikats, gleich dem Benutzernamen in `$external` |
| `keyfile` | Keyfile für die interne Auth im Replikatset (nur prod) |

Das App-Zertifikat hat bewusst eine andere Organizational Unit (`OU=Hinata Application`) als das Zertifikat der Server und Mitglieder. So behandelt `mongod` es als normalen X.509-**Benutzer**, nicht als Cluster-Mitglied.

!!! warning "Die CA auf einem laufenden Cluster nicht neu erzeugen"
    `generate-certs.sh` überschreibt eine bestehende CA nur mit `--force`. Eine neue CA macht sofort alle Zertifikate ungültig, denen das laufende Cluster vertraut. Nutze `--force` nur bei einer frischen Einrichtung.

### 3. Den X.509-Benutzer registrieren

Starte die Datenknoten und lege den Benutzer in `$external` an, der zum DN des App-Zertifikats passt:

```bash
docker compose up -d mongo1 mongo2 mongo-arbiter
./deploy/x509/init-prod-user.sh
docker compose up -d hinata-server
```

`init-prod-user.sh` meldet sich per TLS mit dem SCRAM-Root-Konto aus deiner `.env` an. Es ruft `createUser` in `$external` mit dem DN aus `app-subject-dn.txt` auf und vergibt `readWrite` und `dbAdmin` auf der Datenbank `hinata`. Das Skript ist idempotent: Gibt es den Benutzer schon, meldet es das und macht weiter.

## Die Dev-Datenbank (standalone, trotzdem TLS + X.509)

Lokal startet `docker-compose.dev.yml` ein einzelnes `mongod`, **kein** Replikatset. Die Sicherheit bleibt gleich: `requireTLS`, `--auth` und Zugriff nur per X.509. Ein Befehl richtet alles ein:

```bash
./deploy/x509/setup-dev.sh
SPRING_PROFILES_ACTIVE=dev ./gradlew bootRun
```

`setup-dev.sh` erzeugt die Dev-PKI (`deploy/x509/dev/`), startet das Dev-Mongo, legt den X.509-Benutzer in `$external` über die Localhost-Ausnahme an und prüft den Login per X.509. `application-dev.yml` nutzt diese Verbindung schon, `HINATA_MONGODB_URI` setzt du also nicht selbst.

!!! note "Dev bindet nur an Loopback"
    Das Dev-Mongo veröffentlicht `127.0.0.1:27017`, nie `0.0.0.0`. Aus dem Netzwerk ist es nicht erreichbar.

## Keystore- und Truststore-Passwörter

Keystore und Truststore der JVM sind PKCS#12-Dateien mit Passwörtern, die du festlegst:

| Variable | Schützt | Standard |
| --- | --- | --- |
| `HINATA_MONGO_TLS_KEYSTORE_PASSWORD` | `hinata-app.p12` (Client-Zertifikat + Key) | `changeit` |
| `HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD` | `truststore.p12` (die CA) | `changeit` |

`generate-certs.sh` liest beide Variablen beim Erzeugen der `.p12`-Dateien. Eigene Passwörter exportierst du also **vorher**:

```bash
export HINATA_MONGO_TLS_KEYSTORE_PASSWORD='ein-langer-zufaelliger-wert'
export HINATA_MONGO_TLS_TRUSTSTORE_PASSWORD='ein-weiterer-langer-zufaelliger-wert'
./deploy/x509/generate-certs.sh prod
```

Setze danach dieselben Werte in `.env`, damit der Server die Stores zur Laufzeit öffnen kann.

!!! danger "Ändere jeden Standard vor dem Livegang"
    `changeit`, `hinata-dev-secret` und das Beispiel für `MONGO_ROOT_PASSWORD` in `.env.example` sind nur für die Entwicklung. Erzeuge für jedes Deployment im Internet neue Geheimnisse mit `./deploy/generate-secrets.sh` und setze echte Keystore-Passwörter.

## Datenpersistenz und Betriebssicherheit

- **Benannte Volumes.** Die Datenknoten schreiben in `mongo1-data` und `mongo2-data`. Deine Daten überstehen Neustarts, Image-Upgrades und Neuaufbauten mit `docker compose up`. `docker compose down -v` löscht diese Volumes und damit die Datenbank. Tu das nicht.
- **Mongo nie öffentlich erreichbar machen.** Die Ports bleiben im internen Docker-Netzwerk `hinata`, das Standard-Compose veröffentlicht `27017` in der Produktion nicht auf dem Host. Nur der Server (hinter deinem Reverse Proxy) soll die Datenbank erreichen.
- **Der Arbiter ist kein Backup.** Er speichert keine Daten. Backups kommen aus `mongodump` oder Snapshots der Volumes, siehe [Backups & Upgrades](/de/backups.html).

Weiter geht es mit [Objektspeicher (S3/MinIO)](/de/storage.html), [E-Mail & SMTP](/de/email.html) und [Reverse Proxy & TLS](/de/reverse-proxy.html). Alle Umgebungsvariablen stehen in der [Konfigurationsreferenz](/de/configuration.html).
