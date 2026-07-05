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
  (`issues:read`, `issues:write`, `projects:read`, `kb:read`, `kb:write`,
  `worklog:write`, `search:read`). Ein Read-only-Token kann niemals schreiben.
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

Füge Hinata als Remote-MCP-Server hinzu und nutze dein Token als Bearer-Credential.
Für **Claude Code**:

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
Setup-Operationen.

| Tool | Scope | Funktion |
|---|---|---|
| `search_issues` | `issues:read` | Vorgänge nach Projekt, Status, Zuweisung, Sprint, Typ oder Text filtern |
| `list_my_issues` | `issues:read` | Dem verbundenen Nutzer zugewiesene Vorgänge |
| `get_issue` | `issues:read` | Ein Vorgang per id oder lesbarer id (z. B. `ASTA-42`) |
| `get_issue_hierarchy` | `issues:read` | Epic/Parent und Sub-Tasks eines Vorgangs |
| `list_projects` / `get_project` | `projects:read` | Für den Nutzer sichtbare Projekte |
| `search` | `search:read` | Globale Suche über Vorgänge, Projekte, Personen, Boards, Dokumente |
| `read_kb_article` | `kb:read` | Ein Wissensdatenbank-Artikel, unter Beachtung seiner Sichtbarkeit |
| `create_issue` | `issues:write` | Einen Vorgang anlegen |
| `update_issue` | `issues:write` | Felder eines Vorgangs ändern |
| `add_comment` | `issues:write` | Einen Vorgang kommentieren |
| `create_kb_article` | `kb:write` | Einen Wissensdatenbank-Artikel anlegen |
| `log_work` | `worklog:write` | Zeit auf einen Vorgang buchen |

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
  Schreibvorgang sowie jede Token-Erstellung/-Widerrufung wird im **Audit-Log**
  festgehalten.

!!! info "Auf der Roadmap"
    Ein künftiges Release ergänzt einen vollständigen **OAuth-2.1**-Flow (Dynamic
    Client Registration), sodass Claudes „Verbinden"-Button mit einem Klick eine
    Verbindung zu Hinata herstellt — ohne Token-Einfügen. PATs bleiben der
    einfachste Weg für Claude Code, Cursor und Skripte.
