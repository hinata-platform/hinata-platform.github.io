---
title: Git-Integration
description: Verbinde Hinata-Projekte mit echten GitHub-, GitLab- und Bitbucket-Repositories für Dev-Infos je Vorgang, Smart Commits und Workflow-Automatisierung.
---

# Git-Integration

Verbinde jedes Hinata-Projekt mit **einem oder mehreren** Repositories auf **GitHub,
GitLab oder Bitbucket** — und deine Vorgänge bekommen eine lebendige
Entwicklungs-Timeline: Branches, Commits, Pull-/Merge-Requests und CI-Builds, die einen
Vorgangsschlüssel referenzieren, erscheinen direkt am jeweiligen Vorgang. Dazu kommen
**Smart Commits** (einen Vorgang direkt aus der Commit-Nachricht heraus bearbeiten) und
**Status-Automatisierung** (echte Git-Ereignisse bewegen Vorgänge durch deinen
Workflow).

Alles hier ist **echt** — nichts wird emuliert oder vorgetäuscht. Der Server wickelt
einen tatsächlichen OAuth-Flow mit dem Anbieter ab, registriert einen signierten
Webhook und speichert ein Ereignis erst, nachdem dessen Signatur gegen das beim
Verbinden hinterlegte Secret verifiziert wurde.

!!! info "Wie Arbeit an einen Vorgang gebunden wird"
    Hinata verknüpft über den **Vorgangsschlüssel** — die lesbare ID wie `ASTA-42`
    (Regex `[A-Z][A-Z0-9]+-\d+`). Ein Branch wird über den Schlüssel im **Namen**
    verknüpft, ein Commit über den/die Schlüssel in seiner **Nachricht**, ein PR/MR über
    seinen **Titel oder Quell-Branch**. Ein Commit wird *nie* nur deshalb mit einem
    Vorgang verknüpft, weil er auf dessen Branch liegt — nur die Schlüssel in seiner
    eigenen Nachricht zählen.

## Was du am Vorgang bekommst

Sobald ein Projekt verbunden ist, zeigt jeder Vorgang ein Dev-Info-Panel, das aus
verifizierten Webhook-Ereignissen aufgebaut wird:

| Anzeige | Quellereignis | Hinweise |
| --- | --- | --- |
| **Branches** | `push` mit neuer Ref / `create` | Name, Basis (Default-Branch des Repos), Anbieter und Repo |
| **Commits** | `push` | SHA, erste Zeile der Nachricht, Zeitstempel, „verified“-Flag; neueste zuerst (begrenzt) |
| **Pull-/Merge-Requests** | `pull_request` / Merge Request / `pullrequest:*` | Nummer, Titel, Status (`OPEN`, `DRAFT`, `MERGED`, `CLOSED`), Quell-/Ziel-Branch, Kommentarzahl |
| **CI-Builds** | `workflow_run` / Pipeline | Workflow-Name, Branch und Status (`pending`, `running`, `passing`, `failing`) |

Du kannst einen verknüpften PR/MR auch **direkt aus dem Vorgang** bearbeiten, ohne
Hinata zu verlassen:

```text
POST /api/v1/issues/{key}/dev-info/prs/{number}/merge   → mergen
POST /api/v1/issues/{key}/dev-info/prs/{number}/ready    → als bereit zur Review markieren
GET  /api/v1/issues/{key}/dev-info                        → das Panel lesen
```

Das Lesen von Dev-Infos oder das Bearbeiten eines PR erfordert **Projektmitgliedschaft**;
das Ändern der Verbindung eines Projekts erfordert die Rolle **Project Lead oder Admin**.

## Betreiber-Einrichtung (einmalig, plattformweit)

Die Git-Integration wird **einmal pro Plattform** konfiguriert, nicht pro Projekt. Du
registrierst **eine OAuth-App pro Anbieter** und gibst dem Server ihre Zugangsdaten;
danach kann jeder Project Lead darüber Repos verbinden.

### 1. OAuth-App-Zugangsdaten hinterlegen

Registriere bei jedem gewünschten Anbieter eine OAuth-App (GitHub / GitLab) bzw. einen
OAuth-Consumer (Bitbucket) und gib Hinata Client-ID + Secret — entweder im
**Adminbereich → Git-Integration** der App (in MongoDB gespeichert, ohne Neustart
wirksam) oder per Umgebungsvariablen. Wie überall in Hinata **überschreibt die Datenbank
die Umgebung**, und Secrets sind in der Admin-API **write-only** — sie werden nie
zurückgegeben.

| Variable | Zweck |
| --- | --- |
| `HINATA_GIT_GITHUB_CLIENT_ID` / `HINATA_GIT_GITHUB_CLIENT_SECRET` | GitHub-OAuth-App-Zugangsdaten |
| `HINATA_GIT_GITLAB_CLIENT_ID` / `HINATA_GIT_GITLAB_CLIENT_SECRET` | GitLab-OAuth-App-Zugangsdaten |
| `HINATA_GIT_BITBUCKET_CLIENT_ID` / `HINATA_GIT_BITBUCKET_CLIENT_SECRET` | Bitbucket-OAuth-Consumer-Zugangsdaten |
| `HINATA_GIT_WEBHOOK_BASE_URL` | Öffentliche API-Basis für OAuth-Callback **und** Webhook-Registrierung; Fallback ist `HINATA_BASE_URL` + `/api/v1` |
| `HINATA_GIT_TOKEN_SECRET` | AES-GCM-Schlüssel, der gespeicherte Access-Tokens und Webhook-Secrets im Ruhezustand verschlüsselt — **Standardwert in Produktion ändern** |

### 2. Öffentliche API-Basis setzen

Sowohl der OAuth-Callback als auch die Webhooks müssen **vom Anbieter aus** erreichbar
sein, deshalb muss Hinata seine eigene öffentliche API-Basis kennen. Setze dafür
`HINATA_GIT_WEBHOOK_BASE_URL`, z. B.:

```properties
HINATA_GIT_WEBHOOK_BASE_URL=https://api.track.example.com/api/v1
```

Bleibt sie leer, leitet Hinata sie aus `HINATA_BASE_URL` + `/api/v1` ab.

### 3. OAuth-Callback registrieren

Trage bei jedem Anbieter als Autorisierungs-Callback-URL der OAuth-App den öffentlichen
Callback des Servers ein:

```text
<öffentliche-api-basis>/git/oauth/callback
```

Mit der Basis von oben ist das
`https://api.track.example.com/api/v1/git/oauth/callback`.

!!! warning "Token-Verschlüsselungs-Secret ändern"
    `HINATA_GIT_TOKEN_SECRET` ist der AES-GCM-Schlüssel, der jeden gespeicherten
    Access-Token und jedes verbindungseigene Webhook-Secret **im Ruhezustand**
    verschlüsselt. Setze in Produktion einen echten, zufälligen Wert ein — niemals den
    ausgelieferten Standard. Ändert er sich, lassen sich zuvor gespeicherte Tokens nicht
    mehr entschlüsseln und betroffene Repos müssen neu verbunden werden.

## Der OAuth-Flow (serverseitig vermittelt)

Das Verbinden eines Repos durchläuft einen echten dreibeinigen OAuth-Flow, den der
Server vermittelt, damit die App nie das Client-Secret des Anbieters hält. Der nicht
erratbare, kurzlebige `state` (in MongoDB mit **15-Minuten-TTL** gespeichert) verbindet
den Browser-Umweg wieder mit dem Projekt:

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

Der Callback-Endpunkt ist **öffentlich** — der Anbieter leitet den Browser des Nutzers
ohne Bearer-Token dorthin — seine Sicherheit ruht daher vollständig auf dem nicht
erratbaren `state`. Er liefert eine kleine HTML-Seite zurück, die dem Nutzer sagt, dass
er den Tab schließen und zu Hinata zurückkehren kann.

### Selbst betriebene Server (Enterprise / Data Center)

Selbst gehostete Instanzen von **GitHub Enterprise**, **GitLab** (self-managed) und
**Bitbucket Data Center** überspringen den OAuth-Tanz komplett. Verbinde sie stattdessen
mit einer Repo-URL und einem **Personal Access Token**:

```text
POST /api/v1/projects/{id}/git/connect-token
{ "repoUrl": "https://git.example.com/team/app.git", "token": "<personal-access-token>" }
```

Der Token wird genau wie ein OAuth-Token AES-GCM-verschlüsselt gespeichert, und dieselbe
Webhook-Registrierung und dieselben Verknüpfungsregeln gelten.

## Webhooks

Beim Verbinden registriert der Server einen Hook (für `push`, Branch-`create`, PR/MR und
CI-Ereignisse), der auf einen **öffentlichen**, signaturgeprüften Empfänger zeigt und
mit einem **projektspezifischen Secret** signiert wird, das beim Verbinden erzeugt wird.
Jede eingehende Zustellung wird verifiziert, bevor irgendetwas gespeichert wird:

| Anbieter | Endpunkt | Verifizierung |
| --- | --- | --- |
| **GitHub** | `POST /api/v1/git/webhooks/github` | HMAC-SHA256 über den Rohbody (`X-Hub-Signature-256`) |
| **GitLab** | `POST /api/v1/git/webhooks/gitlab` | Token-Vergleich (`X-Gitlab-Token`) |
| **Bitbucket** | `POST /api/v1/git/webhooks/bitbucket` | geteiltes Secret in der URL-Query (`?secret=…`) |

Der Empfänger findet über das Repository im Payload das Projekt (und das exakt verbundene
Repo), verifiziert das Secret **dieser Verbindung** und verknüpft das Ereignis erst dann
mit Vorgangsschlüsseln. Ein unbekanntes Repository wird stillschweigend mit `200`
ignoriert; ein bekanntes Repository, dessen Signatur nicht verifiziert, wird als nicht
autorisiert abgewiesen.

## Verknüpfungsregeln

Die Regeln sind bewusst streng, damit deine Vorgänge ehrlich bleiben:

- **Branch** → verknüpft über den Vorgangsschlüssel im **Branch-Namen**.
- **Commit** → verknüpft nur über den/die Vorgangsschlüssel in der **Commit-Nachricht**.
  Er wird *nie* nur deshalb verknüpft, weil er auf dem Branch eines Vorgangs liegt.
- **PR / MR** → verknüpft über den/die Vorgangsschlüssel in **Titel oder Quell-Branch**.
- Ein Schlüssel verknüpft nur mit einem **echten** Vorgang, der zum **Projekt dieses
  Repos** gehört — ein Schlüssel, der auf einen nicht existierenden Vorgang oder einen
  Vorgang in einem anderen Projekt zeigt, wird ignoriert.

!!! note "Nebeneffekte genau einmal"
    Anbieter stellen Webhooks erneut zu, und derselbe Commit wird erneut gelistet,
    sobald ein Feature-Branch in den Default-Branch gemerged wird. Deshalb werden die
    **Nebeneffekte** eines Commits — Smart Commits und die „Commit gepusht“-Transition —
    **genau einmal** angewendet, abgesichert durch ein kleines Ledger
    (`git_processed_commits`). Ohne dieses würde jede erneute Zustellung jeden Kommentar
    erneut posten und jede Zeitbuchung erneut anlegen. (Das Aufnehmen eines
    Branch/Commit/PR ins Panel ist selbst idempotent — derselbe SHA bzw. dieselbe
    PR-Nummer wird aktualisiert, nicht dupliziert.)

## Automatisierung

Die Automatisierung wird **pro Projekt** gegen die **eigenen Workflow-Status** dieses
Projekts konfiguriert und verbindet echte Git-Ereignisse mit Status-Übergängen:

| Auslöser | Regel |
| --- | --- |
| **Branch erstellt** (ein `create` oder ein `push`, der eine neue Ref einführt) | referenzierten Vorgang bewegen (z. B. → *In Bearbeitung*) |
| **Commit gepusht** mit Schlüsselbezug (auf beliebigem Branch) | referenzierten Vorgang bewegen |
| **PR / MR geöffnet** (opened / reopened / ready-for-review) | referenzierten Vorgang bewegen (z. B. → *In Review*) |
| **PR / MR gemerged** | referenzierten Vorgang bewegen (z. B. → *Erledigt*) |

!!! tip "Nur vorwärts — kämpft nie gegen dich"
    Die Automatisierung bewegt einen Vorgang immer nur **vorwärts** im Workflow, nie
    rückwärts. Ein später Commit kann einen Vorgang in *In Review* oder *Erledigt* nicht
    zurück nach *In Bearbeitung* ziehen, und ein bereits erfüllter Übergang ist ein
    No-op. Konfiguriere die Regeln mit `PATCH /api/v1/projects/{id}/git/automation`.

## Smart Commits

Trailer in einer Commit-Nachricht wirken direkt auf den referenzierten Vorgang. Smart
Commits müssen in den Automatisierungs-Einstellungen des Projekts aktiviert sein; dann
gilt für einen Vorgangsschlüssel in der Nachricht:

| Trailer | Wirkung |
| --- | --- |
| `ASTA-42 #comment shipped it` | fügt `ASTA-42` einen Kommentar hinzu |
| `ASTA-42 #time 2h 30m` | bucht `2h 30m` Arbeit auf `ASTA-42` |
| `ASTA-42 #done` (jedes andere `#word`) | überführt `ASTA-42` in den passenden Workflow-Status |

```text
ASTA-42 #comment Nullpointer bei leerer Suche behoben #time 45m #in-review
```

Dieser eine Commit fügt einen Kommentar hinzu, bucht 45 Minuten und bewegt `ASTA-42`
nach *In Review*. Ein unbekanntes `#word` (kein passender Status) oder ein Schlüssel
ohne echten Vorgang wird stillschweigend übersprungen — der Rest der Nachricht greift
trotzdem.

## Mehrere Repositories pro Projekt

Ein Projekt kann **mehrere** Repositories verbinden — etwa ein App-Repo und ein
Server-Repo, die dasselbe Team betreut. Was **projektweit geteilt** und was **pro Repo**
ist:

- **Projektweit geteilt**: die Automatisierungsregeln und die **Branch-Vorlage**
  (Standard `{key}-{summary}`, um aus einem Vorgang einen Branch-Namen vorzuschlagen).
- **Pro Repository**: der eigene Zugriffs-**Token**, der eigene **Webhook** samt
  Signatur-Secret und der eigene **Default-Branch**.

Nur Arbeit, die in ein **verbundenes** Repo gepusht wird, erscheint an den Vorgängen des
Projekts. Verwalte die zusätzlichen Repos neben dem primären; Trennen oder erneutes
Synchronisieren kann ein einzelnes Repo per ID ansprechen:

```text
POST   /api/v1/projects/{id}/git/connect         → Repo hinzufügen (OAuth)
POST   /api/v1/projects/{id}/git/connect-token   → selbst betriebenes Repo hinzufügen (PAT)
POST   /api/v1/projects/{id}/git/resync?repoId=… → Status eines Repos neu laden
DELETE /api/v1/projects/{id}/git?repoId=…        → ein Repo trennen (repoId weglassen = alle)
PATCH  /api/v1/projects/{id}/git/branch-template → geteilte Branch-Vorlage setzen
```

## Sicherheit

- **Verschlüsselung im Ruhezustand**: Access-Tokens und verbindungseigene
  Webhook-Secrets werden mit `HINATA_GIT_TOKEN_SECRET` **AES-GCM-verschlüsselt** und
  **nie von der API zurückgegeben** (Secrets sind im Adminbereich write-only).
- **Signaturgeprüfte Aufnahme**: Kein Webhook-Ereignis wird gespeichert, wenn seine
  Signatur (HMAC / Token / Query-Secret) nicht gegen das hinterlegte projektspezifische
  Secret verifiziert. Unbekannte Repos werden ignoriert; falsche Signaturen abgewiesen.
- **Least Privilege**: Dev-Infos lesen oder einen PR bearbeiten erfordert
  Projektmitgliedschaft; Verbinden, Trennen oder Ändern der Automatisierung erfordert die
  Rolle Project Lead oder Admin.
- **Begrenzter Zustand**: Commits und Builds pro Vorgang sind gedeckelt und werden
  getrimmt, damit ein aktives Repo kein unbegrenztes Panel wachsen lässt.

## Verwandte Seiten

- [Projekte & Teams](/de/projects-teams.html) — Vorgangsschlüssel, Workflows und Mitgliedschaft.
- [Vorgänge & Hierarchie](/de/issues.html) — wo das Dev-Info-Panel erscheint.
- [Adminbereich](/de/admin-area.html) — wo OAuth-App-Zugangsdaten zur Laufzeit liegen.
- [Konfigurationsreferenz](/de/configuration.html) — der vollständige `HINATA_GIT_*`-Satz.
