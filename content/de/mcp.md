---
title: MCP-Server (KI)
description: Verbinde Claude, Cursor und andere KI-Clients über das Model Context Protocol mit Hinata. Gescopte Personal Access Tokens, ein eingebetteter /mcp-Endpunkt und Tools, die als der verbundene Nutzer innerhalb seiner Berechtigungen handeln.
---

# MCP-Server (KI)

Hinata spricht das **Model Context Protocol (MCP)** — den offenen Standard, mit
dem KI-Clients externe Systeme erreichen. Richte Claude (Desktop, Web oder Claude
Code), Cursor oder einen beliebigen spec-konformen Client auf deine Hinata-Instanz
aus, und er kann Vorgänge suchen und anlegen, die Wissensdatenbank lesen und
schreiben und Arbeit buchen — **immer im Rahmen der exakten Berechtigungen des
verbundenen Nutzers**. Deine Projektdaten werden damit direkt aus dem
KI-Workflow von Entwickler:innen und PMs steuerbar.

!!! info "Wo es läuft"
    Der MCP-Server ist **in das Hinata-Backend eingebettet** — kein Sidecar, kein
    zweites Deployment. Er wird unter **`/mcp`** auf demselben Host wie die API
    bereitgestellt und erbt die Zugriffskontrolle der Plattform unverändert: jeder
    Tool-Aufruf läuft durch dieselbe Service-Schicht (Team-/Projekt-Mitgliedschaft,
    Artikel-Sichtbarkeit) wie eine normale Anfrage.

## Authentifizierung — Personal Access Tokens

Ein KI-Client verbindet sich mit einem **Personal Access Token (PAT)**, das du in
der App erstellst. Ein PAT ist:

- **Gescopt** — du vergibst eine minimale Teilmenge an Fähigkeiten
  (`issues:read/write`, `projects:read`, `boards:read`, `sprints:write`,
  `teams:read`, `users:read`, `kb:read/write`, `worklog:read/write`,
  `search:read`, `notifications:read`). Ein Read-only-Token kann niemals
  schreiben.
- **Widerrufbar** — jederzeit widerrufbar; die nächste Anfrage mit diesem Token
  wird sofort abgelehnt.
- **Gehasht gespeichert** — nur ein SHA-256-Hash wird abgelegt. Der Klartext wird
  **einmalig** bei der Erstellung angezeigt und nie wieder.
- **Auf `/mcp` beschränkt** — ein PAT authentifiziert ausschließlich den
  MCP-Endpunkt. An der regulären REST-API wird es abgelehnt, sodass ein gescoptes
  Token niemals zu uneingeschränktem Kontozugriff werden kann.

!!! warning "Token bei der Erstellung kopieren"
    Das vollständige Token (Präfix `hn_pat_…`) wird nur bei der Erstellung
    angezeigt. Trage es sofort in die Konfiguration deines Clients ein — du kannst
    es später nicht mehr abrufen, nur widerrufen und ein neues erstellen.

## Ein Token erstellen

Öffne in der App **Konto → Zugriffstokens**, wähle **Neues Token**, gib ihm einen
Namen (z. B. *Claude Desktop*), wähle die benötigten Geltungsbereiche und optional
ein Ablaufdatum und kopiere das erzeugte Token.

!!! info "Feature-Flag"
    Zugriffstokens erscheinen nur, wenn die MCP-Funktion aktiviert ist. Admins
    schalten sie frei — und begrenzen die Token-Anzahl pro Nutzer — unter
    **Adminbereich → MCP**.

## Einen Client verbinden

Es gibt zwei Wege — je nach Client.

### Ein-Klick-Verbindung (OAuth 2.1)

Für **Claude.ai** und **Claude Desktop** fügst du Hinata als Custom-Connector nur
mit seiner MCP-URL hinzu — `https://DEIN-HINATA-HOST/mcp` — und drückst
**Verbinden**. Hinata ist ein vollständiger **OAuth-2.1-Authorization-Server**:
der Client entdeckt ihn (RFC 9728 / RFC 8414 Metadaten), registriert sich
automatisch (Dynamic Client Registration) und öffnet einen Browser, in dem du
dich **wie gewohnt bei Hinata anmeldest — Passwort, 2FA oder SSO — und die
angefragten Geltungsbereiche freigibst**. Kein Token zum Kopieren. Der Zugriff
läuft über ein kurzlebiges Token mit rotierendem Refresh-Token, alles widerrufbar.

!!! info "OAuth braucht HTTPS"
    Der OAuth-Flow setzt voraus, dass dein Server über **HTTPS** unter einer
    öffentlichen URL (seiner `base-url`) erreichbar ist. Er ist standardmäßig
    aktiv; Admins können ihn — oder die offene Client-Registrierung — unter
    **Adminbereich → MCP** deaktivieren.

### Bearer-Token (PAT)

Für **Claude Code**, **Cursor** und Skripte nutzt du ein Personal Access Token:

```bash
claude mcp add --transport http hinata https://DEIN-HINATA-HOST/mcp \
  --header "Authorization: Bearer hn_pat_dein_token_hier"
```

Jeder Client mit Remote-MCP über Streamable HTTP funktioniert genauso — richte ihn
auf `https://DEIN-HINATA-HOST/mcp` aus und sende das Token als
`Authorization: Bearer`-Header.

## Was die KI tun kann

Der Server stellt eine kuratierte, feste Menge an Tools bereit — nie eine
generische „beliebigen Endpunkt aufrufen"-Fläche und nie Admin-, Auth- oder
Setup-Operationen. Jedes Tool trägt die Standard-MCP-Annotationen
(`readOnlyHint`, `destructiveHint`), sodass Clients wie Claude sichere
Lese-Tools von Schreib- und Lösch-Operationen unterscheiden können.

**Lese-Tools:**

| Tool | Scope | Funktion |
|---|---|---|
| `search_issues` | `issues:read` | Vorgänge nach Projekt, Status, Zuweisung, Sprint, Backlog, Typ oder Text filtern |
| `list_my_issues` | `issues:read` | Dem verbundenen Nutzer zugewiesene Vorgänge |
| `get_issue` | `issues:read` | Ein Vorgang per id oder lesbarer id (z. B. `ASTA-42`) |
| `get_issue_hierarchy` | `issues:read` | Epic/Parent und Sub-Tasks eines Vorgangs |
| `list_comments` | `issues:read` | Kommentare eines Vorgangs, paginiert |
| `list_attachments` | `issues:read` | Anhang-Metadaten eines Vorgangs (Name, Typ, Größe) |
| `get_dev_info` | `issues:read` | Verknüpfte Branches, Commits, Pull Requests und Builds eines Vorgangs |
| `list_projects` / `get_project` | `projects:read` | Sichtbare Projekte inkl. Workflow-Status und Labels |
| `list_project_members` | `projects:read` | Projektmitglieder — Personen zu Zuweisungs-Ids auflösen |
| `get_project_metrics` | `projects:read` | Vorgangszahlen: gesamt, gelöst, offen, je Workflow-Status |
| `list_boards` / `get_board` | `boards:read` | Zugängliche Agile-Boards; Spalten, WIP-Limits, aktiver Sprint |
| `list_sprints` | `boards:read` | Sprints eines Boards, auf Wunsch inkl. archivierter |
| `get_sprint_report` | `boards:read` | Sprint-Einblicke: Burndown, Velocity, Scope-Änderungen, Auslastung |
| `list_teams` / `get_team` | `teams:read` | Die Teams des Nutzers inkl. Mitgliedern und Rollen |
| `search_users` | `users:read` | Verzeichnissuche nach Name, Benutzername oder Titel |
| `get_me` | `users:read` | Das eigene Profil des verbundenen Nutzers |
| `search` | `search:read` | Globale Suche über Vorgänge, Projekte, Personen, Boards, Dokumente |
| `read_kb_article` | `kb:read` | Inhalt eines Wissensdatenbank-Artikels, unter Beachtung seiner Sichtbarkeit |
| `list_kb_articles` | `kb:read` | Sichtbare Wissensdatenbank-Artikel, nach Projekt oder Space |
| `list_work_items` | `worklog:read` | Die gebuchte Zeit eines Vorgangs |
| `my_timesheet` | `worklog:read` | Die eigene gebuchte Zeit in einem Datumsbereich |
| `list_my_notifications` | `notifications:read` | Der eigene Benachrichtigungseingang inkl. Ungelesen-Zähler |

**Schreib-Tools:**

| Tool | Scope | Funktion |
|---|---|---|
| `create_issue` / `update_issue` | `issues:write` | Vorgang anlegen; Felder ändern inkl. Status, Sprint, Parent, Zuweisungen |
| `add_comment` / `edit_comment` / `delete_comment` | `issues:write` | Vorgang kommentieren; eigenen Kommentar bearbeiten oder löschen |
| `create_sprint` / `update_sprint` | `sprints:write` | Sprint auf einem SCRUM-Board planen; Name, Ziel, Daten, Kapazität anpassen |
| `start_sprint` / `complete_sprint` | `sprints:write` | Sprint-Lebenszyklus; Abschließen verschiebt offene Vorgänge |
| `create_kb_article` / `update_kb_article` / `delete_kb_article` | `kb:write` | Wissensdatenbank-Artikel verwalten (der Sichtbarkeits-Scope ist per MCP nie änderbar) |
| `log_work` / `delete_work_item` | `worklog:write` | Zeit auf einen Vorgang buchen; eigenes Work-Item löschen |

Zusätzlich veröffentlicht er **Ressourcen** (`hinata://issue/{ASTA-42}`,
`hinata://project/{KEY}`, `hinata://kb/{id}`) zur direkten Referenz sowie einige
**Prompt**-Vorlagen (Vorgang triagen, Sprint-Standup entwerfen).

## Sicherheitsmodell

- **Die ACL wird nie umgangen.** Jedes Tool löst den verbundenen Nutzer auf und
  delegiert durch dieselben Services wie die App — Team-/Projekt-Mitgliedschaft
  und Artikel-Sichtbarkeit gelten genau wie in der Oberfläche.
- **Scopes gaten Schreib- (und Lese-)Zugriffe.** Ein Token ohne den nötigen
  Geltungsbereich wird abgelehnt, bevor irgendetwas passiert.
- **PATs sind `/mcp`-exklusiv**, gehasht gespeichert, widerrufbar und optional
  ablaufend.
- **Alles ist rate-limitiert** auf einem eigenen Pro-IP-Budget, und jeder
  Schreibvorgang sowie jede Token-Erstellung/-Widerrufung und OAuth-Autorisierung
  wird im **Audit-Log** festgehalten.
- **OAuth ist standardkonform und gehärtet**: OAuth 2.1 mit verpflichtendem PKCE
  (S256), exaktem Redirect-URI-Abgleich, Einmal-Autorisierungscodes, gehashten +
  rotierenden Refresh-Tokens und audience-gebundenen Access-Tokens (RFC 8707).
  OAuth-Tokens tragen dieselben Scopes und laufen durch dieselben Tools und ACLs
  wie PATs.
