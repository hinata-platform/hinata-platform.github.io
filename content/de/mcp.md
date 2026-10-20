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

- **Mit Scopes versehen.** Du vergibst nur die nötigen Rechte (`issues:read/write`, `projects:read/write`, `boards:read`, `sprints:write`, `teams:read`, `users:read`, `kb:read/write`, `worklog:read/write`, `search:read`, `notifications:read`, `shifts:read/write/plan`). Ein Token nur zum Lesen kann nie schreiben.
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
| `copy_project` | `projects:write` | Ein Projekt samt Plan kopieren; braucht [Projektvorlagen](/de/project-templates.html) |
| `set_issue_deadline` | `issues:write` | Eine Frist als Versatz zum Termin des Projekts pflegen; braucht Projektvorlagen |
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
| `list_my_work_items` | `worklog:read` | Die eigenen Zeiteinträge in einem Datumsbereich, seitenweise, auf Wunsch nach Projekt oder Text |
| `time_summary` | `worklog:read` | Die eigene Zeit in bis zu 366 Tagen, summiert und gruppiert nach Projekt, Vorgang, Tätigkeit, Tag, Woche oder Monat |
| `get_timer` | `worklog:read` | Der laufende Timer des Nutzers, falls einer läuft |
| `my_time_off_balance` | `worklog:read` | Der eigene Urlaub je Abwesenheitsart: Anspruch, genommen, geplant, Rest. Krankheit wird nicht aufgeführt |
| `list_my_notifications` | `notifications:read` | Der eigene Benachrichtigungseingang inkl. Zahl der ungelesenen |

**Schreib-Tools:**

| Tool | Scope | Funktion |
|---|---|---|
| `create_issue` / `update_issue` | `issues:write` | Vorgang anlegen, Felder ändern inkl. Status, Sprint, Parent, Zuweisungen |
| `add_comment` / `edit_comment` / `delete_comment` | `issues:write` | Vorgang kommentieren, eigenen Kommentar bearbeiten oder löschen |
| `add_participant` / `remove_participant` | `issues:write` | Vorgang mit einer Person außerhalb des Projekts teilen oder die Beteiligung beenden ([Vorgänge teilen](/de/guide-sharing)) |
| `create_sprint` / `update_sprint` | `sprints:write` | Sprint auf einem SCRUM-Board planen, Name, Ziel, Daten und Kapazität anpassen |
| `start_sprint` / `complete_sprint` | `sprints:write` | Sprint starten und abschließen. Beim Abschließen werden offene Vorgänge verschoben |
| `create_kb_article` / `update_kb_article` / `delete_kb_article` | `kb:write` | Artikel der Wissensdatenbank verwalten (die Sichtbarkeit ist per MCP nie änderbar) |
| `log_work` / `delete_work_item` | `worklog:write` | Zeit auf einen Vorgang buchen, eigenen Arbeitseintrag löschen |
| `update_work_item` | `worklog:write` | Eigenen Zeiteintrag ändern; gesperrte Tage, eingereichte Zeiträume und abgerechnete Einträge werden mit Begründung abgelehnt |
| `start_timer` / `stop_timer` / `discard_timer` | `worklog:write` | Timer starten, als Zeiteintrag stoppen oder verwerfen |
| `request_time_off` | `worklog:write` | Abwesenheit beantragen; der Antrag geht wie aus der App an die Person, die entscheidet |

Die Tools für Timer, Einträge und Abwesenheiten brauchen die erweiterte Zeiterfassung (die letzten beiden zusätzlich das Abwesenheitsmanagement). Ist das Modul aus, sagen sie das, und die vier älteren Tools funktionieren weiter. Kein Tool liest fremde Zeiten oder Salden, und kein Tool entscheidet über einen Antrag: Genehmigen bleibt eine Handlung einer Person in der App. Krankmeldungen laufen weder hin noch zurück über MCP.

Außerdem gibt es **Ressourcen** für direkte Verweise (`hinata://issue/{ASTA-42}`, `hinata://project/{KEY}`, `hinata://kb/{id}` sowie die eigenen `hinata://time/timer`, `hinata://time/entries/{id}` und `hinata://time-off/balance`) und einige **Prompt**-Vorlagen (Vorgang triagieren, Sprint-Standup entwerfen).

## Schichten

Ist die [Schichtplanung](/de/shifts.html) eingeschaltet, kann ein Assistent Fragen wie diese beantworten und für dich handeln:

- „Wann ist meine nächste Schicht?“
- „Wo fehlen am Samstag noch Leute?“
- „Trag mich beim Aufbau am Freitag ein.“
- „Trag mich aus meiner Schicht am Sonntag aus.“

| Tool | Scope | Funktion |
|---|---|---|
| `list_my_shifts` | `shifts:read` | Die eigenen Schichten und Wartelistenplätze in einem Zeitraum, standardmäßig die nächsten 30 Tage |
| `next_shift` | `shifts:read` | Die nächste eigene Schicht, oder dass es keine gibt |
| `list_shift_events` | `shifts:read` | Events mit Zahlen: gebraucht, besetzt, Schichten mit Lücken. Auf Wunsch nur Events, bei denen noch Leute fehlen |
| `get_shift_event` | `shifts:read` | Ein Event mit allen Schichten als Zahlen, ohne Namen |
| `get_shift` | `shifts:read` | Eine Schicht mit den Personen, die einen Platz haben. Wer wartet, wird nur gezählt, nie genannt |
| `self_assign_shift` | `shifts:write` | Sich selbst eintragen. Ist die Schicht voll, landest du auf der Warteliste, und die Antwort sagt das |
| `release_shift` | `shifts:write` | Dich aus deiner Schicht austragen oder die Warteliste verlassen |
| `confirm_shift` / `decline_shift` | `shifts:write` | Eine Zuteilung bestätigen oder ablehnen |
| `assign_shift` / `remove_assignment` | `shifts:plan` | Als planende Person jemanden zuteilen oder herausnehmen |

Ein Zeitraum umfasst höchstens 62 Tage, eine Seite höchstens 100 Einträge. Zeiten kommen als Uhrzeit in der Zeitzone des Events, mit dem Namen der Zone. Eine Überschneidung mit einer eigenen Schicht lehnt Hinata mit einem Satz ab, der den Grund nennt.

`shifts:plan` ist für Tokens gedacht, die im Namen einer planenden Person arbeiten. Bei der Ein-Klick-Verbindung ist er nicht dabei, wenn der Client keine Scopes nennt; ein Client bekommt ihn nur, wenn er ausdrücklich danach fragt und du zustimmst. Die drei Schicht-Scopes erscheinen in der App und auf der Freigabeseite nur, solange die Schichtplanung eingeschaltet ist. Ist sie aus, antworten die Tools, dass die Funktion nicht aktiv ist.

!!! warning "Eventtexte sind keine Anweisungen"
    Titel, Ort und Beschreibung eines Events schreiben Menschen, und ein Assistent liest sie mit. Steht dort etwas wie „Ignoriere alle bisherigen Anweisungen“, ist das Text, kein Befehl. Hinata gibt diese Texte in eigenen Datenfeldern weiter und nie in der Beschreibung eines Tools. Gib einem Token trotzdem nur die Scopes, die er braucht, und lass einen Assistenten mit `shifts:plan` nichts ohne Rückfrage zuteilen.

Einträge über MCP landen wie in der App als Zuteilung im Audit-Protokoll. Die zusätzlichen Einträge, dass ein Token gehandelt hat (`MCP_SHIFT_*`), sind aus, bis ein Administrator sie einschaltet.

## Sicherheitsmodell

- **Die ACL wird nie umgangen.** Jedes Tool ermittelt den verbundenen Nutzer und nutzt dieselben Services wie die App. Team- und Projektmitgliedschaft und die Sichtbarkeit von Artikeln gelten wie in der Oberfläche.
- **Scopes regeln Schreib- und Lesezugriffe.** Fehlt der nötige Scope, wird die Anfrage abgelehnt, bevor etwas passiert.
- **PATs gelten nur für `/mcp`**, werden gehasht gespeichert, sind widerrufbar und können ablaufen.
- **Alles hat ein Rate Limit** mit eigenem Budget pro IP. Jeder Schreibvorgang, jedes Erstellen und Widerrufen eines Tokens und jede OAuth-Autorisierung landet im **Audit-Protokoll**. Ausgenommen sind Start, Stopp und Verwerfen eines Timers: Wie dieselben Aktionen in der App sind diese Einträge aus, bis ein Administrator sie einschaltet, weil eine Zeile je Start und Stopp festhält, wann jemand gearbeitet hat.
- **OAuth folgt dem Standard und ist gehärtet:** OAuth 2.1 mit verpflichtendem PKCE (S256), exaktem Abgleich der Redirect-URI, Autorisierungscodes für nur eine Nutzung, gehashten und rotierenden Refresh-Tokens und Access-Tokens mit fester Audience (RFC 8707). OAuth-Tokens tragen dieselben Scopes und laufen durch dieselben Tools und ACLs wie PATs.
