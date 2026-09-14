---
title: MCP-Server (KI)
description: Verbinde Claude, Cursor und andere KI-Clients über das Model Context Protocol mit Hinata, immer mit den Rechten des verbundenen Nutzers.
---

# MCP-Server (KI)

Hinata spricht das **Model Context Protocol (MCP)**, den offenen Standard für KI-Clients. Verbinde Claude (Desktop, Web oder Claude Code), Cursor oder einen anderen Client, der die Spezifikation einhält.

Der Client kann dann Vorgänge suchen und anlegen, die Wissensdatenbank lesen und schreiben und Zeit buchen. **Er hat immer genau die Rechte des verbundenen Nutzers.**

!!! info "Wo es läuft"
    Der MCP-Server ist **im Hinata-Backend eingebaut**, ohne Sidecar oder zweites Deployment. Er läuft unter **`/mcp`** auf demselben Host wie die API. Jeder Toolaufruf geht durch dieselbe Serviceschicht wie eine normale Anfrage, mit denselben Regeln für Team- und Projektmitgliedschaft und die Sichtbarkeit von Artikeln.

## Authentifizierung: Personal Access Tokens

Ein KI-Client verbindet sich mit einem **Personal Access Token (PAT)**, das du in der App erstellst. Ein PAT ist:

- **Mit Scopes versehen.** Du vergibst nur die nötigen Rechte (`issues:read/write`, `projects:read`, `boards:read`, `sprints:write`, `teams:read`, `users:read`, `kb:read/write`, `worklog:read/write`, `search:read`, `notifications:read`). Ein Token nur zum Lesen kann nie schreiben.
- **Widerrufbar.** Jederzeit. Die nächste Anfrage mit dem Token wird sofort abgelehnt.
- **Gehasht gespeichert.** Nur ein SHA-256-Hash wird gespeichert. Den Klartext siehst du **einmal** beim Erstellen.
- **Auf `/mcp` beschränkt.** Die normale REST-API lehnt PATs ab. Ein Token mit Scopes wird so nie zum vollen Kontozugriff.

!!! warning "Token bei der Erstellung kopieren"
    Das vollständige Token (Präfix `hn_pat_…`) siehst du nur beim Erstellen. Trage es sofort in deinen Client ein. Später kannst du es nur noch widerrufen und ein neues erstellen.

## Ein Token erstellen

1. Öffne in der App **Konto → Zugriffstokens**.
2. Wähle **Neues Token** und gib ihm einen Namen (z. B. *Claude Desktop*).
3. Wähle die nötigen Geltungsbereiche und optional ein Ablaufdatum.
4. Kopiere das erzeugte Token.

!!! info "Feature-Flag"
    Zugriffstokens erscheinen nur, wenn die MCP-Funktion aktiv ist. Admins schalten sie unter **Adminbereich → MCP** frei und begrenzen dort die Zahl der Tokens pro Nutzer.

## Einen Client verbinden

Es gibt zwei Wege, je nach Client.

### Ein-Klick-Verbindung (OAuth 2.1)

Für **Claude.ai** und **Claude Desktop** fügst du Hinata als Custom Connector mit der MCP-URL `https://DEIN-HINATA-HOST/mcp` hinzu und drückst **Verbinden**.

Hinata ist ein vollständiger **OAuth-2.1-Authorization-Server**:

- Der Client findet den Server über Metadaten (RFC 9728 / RFC 8414).
- Er registriert sich selbst (Dynamic Client Registration).
- Ein Browser öffnet sich. Du **meldest dich wie gewohnt bei Hinata an (Passwort, 2FA oder SSO) und gibst die angefragten Geltungsbereiche frei**.

Du musst kein Token kopieren. Der Zugriff läuft über ein kurzlebiges Token mit rotierendem Refresh-Token, beides widerrufbar.

!!! info "OAuth braucht HTTPS"
    Dein Server muss über **HTTPS** unter einer öffentlichen URL (seiner `base-url`) erreichbar sein. OAuth ist standardmäßig aktiv. Admins können es oder die offene Client-Registrierung unter **Adminbereich → MCP** abschalten.

### Bearer-Token (PAT)

Für **Claude Code**, **Cursor** und Skripte nutzt du ein Personal Access Token:

```bash
claude mcp add --transport http hinata https://DEIN-HINATA-HOST/mcp \
  --header "Authorization: Bearer hn_pat_dein_token_hier"
```

Jeder Client mit Remote-MCP über Streamable HTTP funktioniert genauso: `https://DEIN-HINATA-HOST/mcp` eintragen und das Token im Header `Authorization: Bearer` senden.

## Was die KI tun kann

Der Server bietet eine feste Auswahl an Tools. Es gibt keinen Aufruf beliebiger Endpunkte und keine Operationen für Admin, Auth oder Einrichtung.

Jedes Tool trägt die MCP-Annotationen `readOnlyHint` und `destructiveHint`. Clients wie Claude erkennen daran, welche Tools nur lesen und welche schreiben oder löschen.

**Lese-Tools:**

| Tool | Scope | Funktion |
|---|---|---|
| `search_issues` | `issues:read` | Vorgänge nach Projekt, Status, Zuweisung, Sprint, Backlog, Typ oder Text filtern |
| `list_my_issues` | `issues:read` | Dem verbundenen Nutzer zugewiesene Vorgänge |
| `get_issue` | `issues:read` | Ein Vorgang per id oder lesbarer id (z. B. `ASTA-42`) |
| `get_issue_hierarchy` | `issues:read` | Epic oder Parent und Sub-Tasks eines Vorgangs |
| `list_comments` | `issues:read` | Kommentare eines Vorgangs, paginiert |
| `list_attachments` | `issues:read` | Metadaten der Anhänge eines Vorgangs (Name, Typ, Größe) |
| `get_dev_info` | `issues:read` | Verknüpfte Branches, Commits, Pull Requests und Builds eines Vorgangs |
| `list_projects` / `get_project` | `projects:read` | Sichtbare Projekte inkl. Workflowstatus und Labels |
| `list_project_members` | `projects:read` | Projektmitglieder, um Personen den IDs für Zuweisungen zuzuordnen |
| `get_project_metrics` | `projects:read` | Vorgangszahlen: gesamt, gelöst, offen, je Workflowstatus |
| `list_boards` / `get_board` | `boards:read` | Zugängliche Boards mit Spalten, WIP-Limits und aktivem Sprint |
| `list_sprints` | `boards:read` | Sprints eines Boards, auf Wunsch inkl. archivierter |
| `get_sprint_report` | `boards:read` | Sprintauswertung: Burndown, Velocity, Scope-Änderungen, Auslastung |
| `list_teams` / `get_team` | `teams:read` | Die Teams des Nutzers inkl. Mitgliedern und Rollen |
| `search_users` | `users:read` | Verzeichnissuche nach Name, Benutzername oder Titel |
| `get_me` | `users:read` | Das eigene Profil des verbundenen Nutzers |
| `search` | `search:read` | Globale Suche über Vorgänge, Projekte, Personen, Boards, Dokumente |
| `read_kb_article` | `kb:read` | Inhalt eines Artikels der Wissensdatenbank, unter Beachtung seiner Sichtbarkeit |
| `list_kb_articles` | `kb:read` | Sichtbare Artikel der Wissensdatenbank, nach Projekt oder Space |
| `list_work_items` | `worklog:read` | Die gebuchte Zeit eines Vorgangs |
| `my_timesheet` | `worklog:read` | Die eigene gebuchte Zeit in einem Datumsbereich |
| `list_my_notifications` | `notifications:read` | Der eigene Benachrichtigungseingang inkl. Zahl der ungelesenen |

**Schreib-Tools:**

| Tool | Scope | Funktion |
|---|---|---|
| `create_issue` / `update_issue` | `issues:write` | Vorgang anlegen, Felder ändern inkl. Status, Sprint, Parent, Zuweisungen |
| `add_comment` / `edit_comment` / `delete_comment` | `issues:write` | Vorgang kommentieren, eigenen Kommentar bearbeiten oder löschen |
| `create_sprint` / `update_sprint` | `sprints:write` | Sprint auf einem SCRUM-Board planen, Name, Ziel, Daten und Kapazität anpassen |
| `start_sprint` / `complete_sprint` | `sprints:write` | Sprint starten und abschließen. Beim Abschließen werden offene Vorgänge verschoben |
| `create_kb_article` / `update_kb_article` / `delete_kb_article` | `kb:write` | Artikel der Wissensdatenbank verwalten (die Sichtbarkeit ist per MCP nie änderbar) |
| `log_work` / `delete_work_item` | `worklog:write` | Zeit auf einen Vorgang buchen, eigenen Arbeitseintrag löschen |

Außerdem gibt es **Ressourcen** für direkte Verweise (`hinata://issue/{ASTA-42}`, `hinata://project/{KEY}`, `hinata://kb/{id}`) und einige **Prompt**-Vorlagen (Vorgang triagieren, Sprint-Standup entwerfen).

## Sicherheitsmodell

- **Die ACL wird nie umgangen.** Jedes Tool ermittelt den verbundenen Nutzer und nutzt dieselben Services wie die App. Team- und Projektmitgliedschaft und die Sichtbarkeit von Artikeln gelten wie in der Oberfläche.
- **Scopes regeln Schreib- und Lesezugriffe.** Fehlt der nötige Scope, wird die Anfrage abgelehnt, bevor etwas passiert.
- **PATs gelten nur für `/mcp`**, werden gehasht gespeichert, sind widerrufbar und können ablaufen.
- **Alles hat ein Rate Limit** mit eigenem Budget pro IP. Jeder Schreibvorgang, jedes Erstellen und Widerrufen eines Tokens und jede OAuth-Autorisierung landet im **Audit-Protokoll**.
- **OAuth folgt dem Standard und ist gehärtet:** OAuth 2.1 mit verpflichtendem PKCE (S256), exaktem Abgleich der Redirect-URI, Autorisierungscodes für nur eine Nutzung, gehashten und rotierenden Refresh-Tokens und Access-Tokens mit fester Audience (RFC 8707). OAuth-Tokens tragen dieselben Scopes und laufen durch dieselben Tools und ACLs wie PATs.
