---
title: Git-Integration
description: Verbinde Hinata-Projekte mit GitHub, GitLab und Bitbucket für Entwicklungsinfos, Smart Commits und Automatisierung.
---

# Git-Integration

Verbinde ein Hinata-Projekt mit **einem oder mehreren** Repositories auf **GitHub,
GitLab oder Bitbucket**. Branches, Commits, Pull oder Merge Requests und CI-Builds mit
einem Vorgangsschlüssel erscheinen dann direkt am Vorgang.

Dazu kommen:

- **Smart Commits**: Du bearbeitest einen Vorgang direkt aus der Commit-Nachricht.
- **Automatisierung**: Git-Ereignisse bewegen Vorgänge durch deinen Workflow.

Der Server führt einen echten OAuth-Flow mit dem Anbieter aus und registriert einen
signierten Webhook. Ein Ereignis wird erst gespeichert, wenn seine Signatur zum Secret
passt, das beim Verbinden hinterlegt wurde.

!!! info "Wie Arbeit an einen Vorgang gebunden wird"
    Hinata verknüpft über den **Vorgangsschlüssel**, also die lesbare ID wie `ASTA-42`
    (Regex `[A-Z][A-Z0-9]+-\d+`). Ein Branch wird über den Schlüssel im **Namen**
    verknüpft, ein Commit über die Schlüssel in seiner **Nachricht** und ein PR/MR über
    **Titel oder Quell-Branch**. Ein Commit wird *nie* verknüpft, nur weil er auf dem
    Branch eines Vorgangs liegt.

## Was du am Vorgang bekommst

Jeder Vorgang eines verbundenen Projekts zeigt ein Panel mit Entwicklungsinfos. Es
entsteht aus verifizierten Webhook-Ereignissen:

| Anzeige | Quellereignis | Hinweise |
| --- | --- | --- |
| **Branches** | `push` mit neuer Ref / `create` | Name, Basis (Default-Branch des Repos), Anbieter und Repo |
| **Commits** | `push` | SHA, erste Zeile der Nachricht, Zeitstempel, „verified“-Flag. Neueste zuerst (begrenzt) |
| **Pull-/Merge-Requests** | `pull_request` / Merge Request / `pullrequest:*` | Nummer, Titel, Status (`OPEN`, `DRAFT`, `MERGED`, `CLOSED`), Quell-/Ziel-Branch, Kommentarzahl |
| **CI-Builds** | `workflow_run` / Pipeline | Workflow-Name, Branch und Status (`pending`, `running`, `passing`, `failing`) |

Einen verknüpften PR/MR bearbeitest du direkt am Vorgang:

```text
POST /api/v1/issues/{key}/dev-info/prs/{number}/merge   → mergen
POST /api/v1/issues/{key}/dev-info/prs/{number}/ready    → als bereit zur Review markieren
GET  /api/v1/issues/{key}/dev-info                        → das Panel lesen
```

- Dev-Infos lesen und PRs bearbeiten: **Projektmitgliedschaft**.
- Verbindung eines Projekts ändern: Rolle **Project Lead oder Admin**.

## Einrichtung für Betreiber (einmalig, plattformweit)

Die Git-Integration richtest du **einmal für die ganze Plattform** ein. Du registrierst
**eine OAuth-App pro Anbieter** und hinterlegst ihre Zugangsdaten. Danach kann jeder
Project Lead Repos verbinden.

### 1. OAuth-App-Zugangsdaten hinterlegen

Registriere bei jedem Anbieter eine OAuth-App (GitHub, GitLab) oder einen
OAuth-Consumer (Bitbucket). Client-ID und Secret gibst du Hinata auf einem von zwei
Wegen:

- im **Adminbereich → Git-Integration** der App (in MongoDB gespeichert, ohne Neustart wirksam)
- per Umgebungsvariablen

Die **Datenbank überschreibt die Umgebung**. Secrets sind in der Admin-API
**write-only** und werden nie zurückgegeben.

| Variable | Zweck |
| --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` / `HINATA_GIT_GITHUB_CLIENT_SECRET` | Zugangsdaten der GitHub-OAuth-App |
| `HINATA_GIT_GITLAB_CLIENT_ID` / `HINATA_GIT_GITLAB_CLIENT_SECRET` | Zugangsdaten der GitLab-OAuth-App |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` / `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Zugangsdaten des Bitbucket-OAuth-Consumers |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Öffentliche API-Basis für OAuth-Callback **und** Webhook-Registrierung. Fallback ist `HINATA_BASE_URL` + `/api/v1` |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM-Schlüssel, der gespeicherte Access-Tokens und Webhook-Secrets im Ruhezustand verschlüsselt. **Standardwert in Produktion ändern** |

### 2. Öffentliche API-Basis setzen

OAuth-Callback und Webhooks müssen **vom Anbieter aus** erreichbar sein. Hinata muss
deshalb seine öffentliche API-Basis kennen. Setze dafür `HINATA_GIT_WEBHOOK_BASE_URL`:

```properties
HINATA_GIT_WEBHOOK_BASE_URL=https://api.track.example.com/api/v1
```

Bleibt sie leer, nimmt Hinata `HINATA_BASE_URL` + `/api/v1`.

### 3. OAuth-Callback registrieren

Trage bei jedem Anbieter diese Callback-URL in der OAuth-App ein:

```text
<öffentliche-api-basis>/git/oauth/callback
```

Mit der Basis von oben ist das
`https://api.track.example.com/api/v1/git/oauth/callback`.

!!! warning "Secret für die Tokenverschlüsselung ändern"
    `HINATA_GIT_TOKEN_SECRET` ist der AES-GCM-Schlüssel für jeden gespeicherten
    Access-Token und jedes Webhook-Secret einer Verbindung **im Ruhezustand**. Setze in
    Produktion einen zufälligen Wert, nie den ausgelieferten Standard. Ändert er sich,
    lassen sich alte Tokens nicht mehr entschlüsseln. Betroffene Repos musst du dann neu
    verbinden.

## Der OAuth-Flow (serverseitig vermittelt)

Der Server vermittelt einen dreibeinigen OAuth-Flow. So hält die App nie das
Client-Secret des Anbieters. Ein nicht erratbarer, kurzlebiger `state` (in MongoDB mit
**15-Minuten-TTL**) ordnet den Umweg über den Browser wieder dem Projekt zu:

```text
App   POST /projects/{id}/git/oauth/start   (Anbieter)
        │
        ▼
Server  baut Authorize-URL des Anbieters, speichert Session-State (Mongo, TTL 15m)
        │  liefert { authorizeUrl, state }
        ▼
Nutzer  öffnet die Authorize-URL im Browser und stimmt zu
        │
        ▼
Anbieter  GET /git/oauth/callback?code&state   (öffentlich, kein Bearer-Token)
        │
        ▼
Server  tauscht code → Access-Token, speichert es AES-GCM-verschlüsselt
        │  markiert die Session als AUTHORIZED
        ▼
App     pollt GET /git/oauth/session/{state}  → AUTHORIZED
        │
        ▼
App     GET  /projects/{id}/git/owners        → Owner/Org wählen
        App  GET  /projects/{id}/git/repos     → Repository wählen
        App  POST /projects/{id}/git/connect   → verbinden (registriert den Webhook)
```

Der Callback ist **öffentlich**, weil der Anbieter den Browser ohne Bearer-Token
dorthin leitet. Seine Sicherheit hängt deshalb allein am nicht erratbaren `state`. Er
zeigt eine kleine HTML-Seite: Der Tab kann geschlossen werden, weiter geht es in Hinata.

### Selbst betriebene Server (Enterprise / Data Center)

Selbst gehostetes **GitHub Enterprise**, **GitLab** (self-managed) und **Bitbucket
Data Center** brauchen keinen OAuth-Flow. Verbinde sie mit Repo-URL und **Personal
Access Token**:

```text
POST /api/v1/projects/{id}/git/connect-token
{ "repoUrl": "https://git.example.com/team/app.git", "token": "<personal-access-token>" }
```

Der Token wird wie ein OAuth-Token mit AES-GCM verschlüsselt gespeichert.
Webhook-Registrierung und Verknüpfungsregeln sind dieselben.

## Webhooks

Beim Verbinden registriert der Server einen Hook für `push`, Branch-`create`, PR/MR und
CI-Ereignisse. Er zeigt auf einen **öffentlichen** Empfänger und wird mit einem
**projektspezifischen Secret** signiert, das beim Verbinden entsteht. Jede Zustellung
wird geprüft, bevor etwas gespeichert wird:

| Anbieter | Endpunkt | Verifizierung |
| --- | --- | --- |
| **GitHub** | `POST /api/v1/git/webhooks/github` | HMAC-SHA256 über den Rohbody (`X-Hub-Signature-256`) |
| **GitLab** | `POST /api/v1/git/webhooks/gitlab` | Tokenvergleich (`X-Gitlab-Token`) |
| **Bitbucket** | `POST /api/v1/git/webhooks/bitbucket` | geteiltes Secret in der URL-Query (`?secret=…`) |

Der Empfänger findet über das Repository im Payload das Projekt und das verbundene
Repo. Er prüft das Secret **dieser Verbindung** und verknüpft erst danach mit
Vorgangsschlüsseln.

- Unbekanntes Repository: wird ohne Fehler mit `200` ignoriert.
- Bekanntes Repository mit falscher Signatur: wird als nicht autorisiert abgewiesen.

## Verknüpfungsregeln

- **Branch**: über den Vorgangsschlüssel im **Branch-Namen**.
- **Commit**: nur über die Vorgangsschlüssel in der **Commit-Nachricht**. Er wird *nie*
  verknüpft, nur weil er auf dem Branch eines Vorgangs liegt.
- **PR / MR**: über die Vorgangsschlüssel in **Titel oder Quell-Branch**.
- Ein Schlüssel verknüpft nur mit einem **existierenden** Vorgang im **Projekt dieses
  Repos**. Schlüssel zu fehlenden Vorgängen oder Vorgängen anderer Projekte werden
  ignoriert.

!!! note "Nebeneffekte genau einmal"
    Anbieter stellen Webhooks erneut zu. Außerdem taucht ein Commit wieder auf, wenn ein
    Feature-Branch in den Default-Branch gemerged wird. Die **Nebeneffekte** eines
    Commits (Smart Commits und die Transition „Commit gepusht“) laufen deshalb **genau
    einmal**. Das sichert ein kleines Ledger (`git_processed_commits`). Ohne es würde
    jede erneute Zustellung Kommentare und Zeitbuchungen doppelt anlegen.

    Das Panel selbst ist idempotent: Derselbe SHA oder dieselbe PR-Nummer wird
    aktualisiert und nicht dupliziert.

## Automatisierung

Die Automatisierung stellst du **pro Projekt** ein, passend zu den **Workflow-Status
dieses Projekts**. Sie verbindet Git-Ereignisse mit Statusübergängen:

| Auslöser | Regel |
| --- | --- |
| **Branch erstellt** (ein `create` oder ein `push`, der eine neue Ref einführt) | referenzierten Vorgang bewegen (z. B. → *In Bearbeitung*) |
| **Commit gepusht** mit Schlüsselbezug (auf beliebigem Branch) | referenzierten Vorgang bewegen |
| **PR / MR geöffnet** (opened / reopened / ready-for-review) | referenzierten Vorgang bewegen (z. B. → *In Review*) |
| **PR / MR gemerged** | referenzierten Vorgang bewegen (z. B. → *Erledigt*) |

!!! tip "Nur vorwärts"
    Die Automatisierung bewegt einen Vorgang nur **vorwärts** im Workflow. Ein später
    Commit zieht einen Vorgang in *In Review* oder *Erledigt* nicht zurück nach *In
    Bearbeitung*. Ein bereits erfüllter Übergang bewirkt nichts. Die Regeln setzt du mit
    `PATCH /api/v1/projects/{id}/git/automation`.

## Smart Commits

Smart Commits aktivierst du in den Automatisierungseinstellungen des Projekts. Dann
wirken Trailer in einer Commit-Nachricht direkt auf den genannten Vorgang:

| Trailer | Wirkung |
| --- | --- |
| `ASTA-42 #comment shipped it` | fügt `ASTA-42` einen Kommentar hinzu |
| `ASTA-42 #time 2h 30m` | bucht `2h 30m` Arbeit auf `ASTA-42` |
| `ASTA-42 #done` (jedes andere `#word`) | überführt `ASTA-42` in den passenden Workflow-Status |

```text
ASTA-42 #comment Nullpointer bei leerer Suche behoben #time 45m #in-review
```

Dieser Commit fügt einen Kommentar hinzu, bucht 45 Minuten und bewegt `ASTA-42` nach
*In Review*. Ein unbekanntes `#word` (kein passender Status) oder ein Schlüssel ohne
existierenden Vorgang wird ohne Fehler übersprungen. Der Rest der Nachricht greift
trotzdem.

## Mehrere Repositories pro Projekt

Ein Projekt kann **mehrere** Repositories verbinden, etwa ein App-Repo und ein
Server-Repo desselben Teams.

- **Für das ganze Projekt**: die Automatisierungsregeln und die **Branch-Vorlage**
  (Standard `{key}-{summary}`, schlägt aus einem Vorgang einen Branch-Namen vor).
- **Pro Repository**: eigener Zugriffs-**Token**, eigener **Webhook** mit
  Signatur-Secret und eigener **Default-Branch**.

Am Vorgang erscheint nur Arbeit aus **verbundenen** Repos. Zusätzliche Repos verwaltest
du neben dem primären. Trennen und Resync können ein einzelnes Repo per ID ansprechen:

```text
POST   /api/v1/projects/{id}/git/connect         → Repo hinzufügen (OAuth)
POST   /api/v1/projects/{id}/git/connect-token   → selbst betriebenes Repo hinzufügen (PAT)
POST   /api/v1/projects/{id}/git/resync?repoId=… → Status eines Repos neu laden
DELETE /api/v1/projects/{id}/git?repoId=…        → ein Repo trennen (repoId weglassen = alle)
PATCH  /api/v1/projects/{id}/git/branch-template → geteilte Branch-Vorlage setzen
```

## Sicherheit

- **Verschlüsselung im Ruhezustand**: Access-Tokens und Webhook-Secrets werden mit
  `HINATA_GIT_TOKEN_SECRET` per **AES-GCM** verschlüsselt und **nie von der API
  zurückgegeben** (im Adminbereich write-only).
- **Signaturprüfung**: Ein Webhook-Ereignis wird nur gespeichert, wenn seine Signatur
  (HMAC, Token oder Query-Secret) zum projektspezifischen Secret passt. Unbekannte
  Repos werden ignoriert, falsche Signaturen abgewiesen.
- **Minimale Rechte**: Dev-Infos lesen und PRs bearbeiten erfordert
  Projektmitgliedschaft. Verbinden, Trennen und Automatisierung ändern erfordert die
  Rolle Project Lead oder Admin.
- **Begrenzter Umfang**: Commits und Builds pro Vorgang sind gedeckelt und werden
  gekürzt, damit das Panel bei aktiven Repos nicht unbegrenzt wächst.

## Verwandte Seiten

- [Projekte & Teams](/de/projects-teams.html): Vorgangsschlüssel, Workflows und Mitgliedschaft.
- [Vorgänge & Hierarchie](/de/issues.html): wo das Panel mit den Entwicklungsinfos erscheint.
- [Adminbereich](/de/admin-area.html): wo die OAuth-Zugangsdaten zur Laufzeit liegen.
- [Konfigurationsreferenz](/de/configuration.html): alle `HINATA_GIT_*`-Variablen.
