import { SITE } from './content';

export type Lang = 'en' | 'de';
type L = Record<Lang, string>;

/** Everything the landing page says, in both languages.
 *
 * The landing is one URL, not two — it is what a link from a store listing or a
 * README lands on, and it has to be shareable — so it carries both languages
 * and picks one in the browser. The documentation trees do the opposite,
 * because a docs page is a thing people deep-link into and cite.
 */
export const FEATURES: Array<{ emoji: string; title: L; desc: L }> = [
  {
    emoji: '📊',
    title: { en: 'Dashboard & reports', de: 'Dashboard & Berichte' },
    desc: {
      en: 'Burndown, velocity, cycle time and distributions, plus your personal focus for the day.',
      de: 'Burndown, Velocity, Cycle Time und Verteilungen, dazu dein persönlicher Tagesfokus.',
    },
  },
  {
    emoji: '📋',
    title: { en: 'Agile boards', de: 'Agile Boards' },
    desc: {
      en: 'Board, Backlog & Timeline views with drag-and-drop, WIP limits and swimlanes.',
      de: 'Board, Backlog und Timeline mit Drag and Drop, WIP-Limits und Swimlanes.',
    },
  },
  {
    emoji: '🏃',
    title: { en: 'Sprints', de: 'Sprints' },
    desc: {
      en: 'Plan, run and review sprints with capacity, story points and burndown.',
      de: 'Sprints planen, starten und auswerten, mit Kapazität, Story Points und Burndown.',
    },
  },
  {
    emoji: '🐛',
    title: { en: 'Issues & hierarchy', de: 'Vorgänge & Hierarchie' },
    desc: {
      en: 'Epics → stories/tasks/bugs → sub-tasks, dependencies, labels, comments, attachments.',
      de: 'Epics → Stories/Tasks/Bugs → Sub-Tasks, Abhängigkeiten, Labels, Kommentare, Anhänge.',
    },
  },
  {
    emoji: '🔗',
    title: { en: 'Git integration', de: 'Git-Integration' },
    desc: {
      en: 'GitHub, GitLab and Bitbucket with real OAuth, signed webhooks, smart commits and automation.',
      de: 'GitHub, GitLab und Bitbucket mit echtem OAuth, signierten Webhooks, Smart Commits und Automatik.',
    },
  },
  {
    emoji: '🔑',
    title: { en: 'SSO & security', de: 'SSO & Sicherheit' },
    desc: {
      en: 'OpenID Connect, OAuth 2.0, SAML, LDAP. JWT, BCrypt, rate limiting, OWASP-hardened.',
      de: 'OpenID Connect, OAuth 2.0, SAML, LDAP. JWT, BCrypt, Rate Limiting, gehärtet nach OWASP.',
    },
  },
  {
    emoji: '📚',
    title: { en: 'Knowledge base', de: 'Wissensdatenbank' },
    desc: {
      en: 'Hierarchical Markdown articles, global or per project, with smart links.',
      de: 'Hierarchische Markdown-Artikel, global oder pro Projekt, mit Smart Links.',
    },
  },
  {
    emoji: '⏱️',
    title: { en: 'Time tracking', de: 'Zeiterfassung' },
    desc: {
      en: 'Log work by activity type and see it in weekly timesheets and reports.',
      de: 'Arbeitszeit nach Tätigkeit erfassen und im Stundenzettel und in Berichten sehen.',
    },
  },
  {
    emoji: '🎨',
    title: { en: 'Bring your own server', de: 'Dein eigener Server' },
    desc: {
      en: 'One app connects to your own server and shows your logo and name. Six platforms from one Flutter codebase.',
      de: 'Eine App verbindet sich mit deinem Server und zeigt dein Logo und deinen Namen. Sechs Plattformen aus einer Flutter-Codebasis.',
    },
  },
];

/** The nine shipped translations, in the order the app's language picker lists
 * them. A flag is a country and not a language — said out loud under the row,
 * because Spanish is not only Spain's and Arabic belongs to more than twenty
 * countries. They are here because nine flags read faster than nine names. */
export const LANGUAGES: Array<[string, string, string]> = [
  ['🇬🇧', 'English', 'en'],
  ['🇩🇪', 'Deutsch', 'de'],
  ['🇫🇷', 'Français', 'fr'],
  ['🇪🇸', 'Español', 'es'],
  ['🇷🇺', 'Русский', 'ru'],
  ['🇨🇳', '简体中文', 'zh'],
  ['🇯🇵', '日本語', 'ja'],
  ['🇮🇳', 'हिन्दी', 'hi'],
  ['🇸🇦', 'العربية', 'ar'],
];

export const LANGUAGE_ANCHOR: Record<Lang, string> = {
  en: 'features/#languages',
  // A heading's anchor is the heading's own words.
  de: 'features/#sprachen',
};

export const T: Record<string, L> = {
  eyebrow: {
    en: 'Open source · Self-hosted · GPL-3.0',
    de: 'Open Source · Self-hosted · GPL-3.0',
  },
  headline_1: { en: 'Project management', de: 'Projektmanagement,' },
  headline_2: { en: 'you actually own.', de: 'das dir gehört.' },
  sub: {
    en: 'Hinata is a project and issue tracker you run on your own server. Boards, sprints, Gantt, time tracking, a knowledge base and Git integration. One app for Android, iOS, Web, macOS, Windows and Linux. No limits on users, teams or boards.',
    de: 'Mit Hinata verwaltest du Projekte und Vorgänge auf deinem eigenen Server. Boards, Sprints, Gantt, Zeiterfassung, Wissensdatenbank und Git-Integration. Eine App für Android, iOS, Web, macOS, Windows und Linux. Keine Grenzen bei Nutzern, Teams oder Boards.',
  },
  cta_start: { en: 'Get started', de: 'Loslegen' },
  cta_host: { en: 'Self-hosting guide', de: 'Selbst hosten' },
  features_title: {
    en: 'Everything a modern team needs',
    de: 'Alles, was ein modernes Team braucht',
  },
  features_sub: {
    en: 'Everything in one platform. No add-ons, no price per user.',
    de: 'Alles in einer Plattform. Keine Add-ons, kein Preis pro Nutzer.',
  },
  host_title: { en: 'Up and running in minutes', de: 'In Minuten einsatzbereit' },
  host_sub: {
    en: 'Docker Compose starts the server, a MongoDB replica set, object storage and mail. Enter your URL in the app and follow the setup.',
    de: 'Docker Compose startet den Server, ein MongoDB Replica Set, Objektspeicher und Mail. Gib deine URL in der App ein und folge der Einrichtung.',
  },
  host_cta: { en: 'Deployment guide →', de: 'Zur Deployment-Anleitung →' },
  mcp_badge: { en: 'MCP', de: 'MCP' },
  mcp_title_1: { en: 'Talk to Hinata', de: 'Sprich mit Hinata' },
  mcp_title_2: { en: 'from Claude', de: 'über Claude' },
  mcp_sub: {
    en: 'Hinata has a built-in /mcp endpoint for the Model Context Protocol. Connect Claude, Claude Code, Cursor or any MCP client to search issues, create work, log time or read the knowledge base. It only sees what the connected user may see.',
    de: 'Hinata hat einen eingebauten /mcp-Endpunkt für das Model Context Protocol. Verbinde Claude, Claude Code, Cursor oder einen anderen MCP-Client, um Vorgänge zu suchen, Arbeit anzulegen, Zeit zu buchen oder die Wissensdatenbank zu lesen. Er sieht nur, was der verbundene Nutzer sehen darf.',
  },
  mcp_cta: { en: 'Explore the MCP server →', de: 'MCP-Server entdecken →' },
  mcp_clients: {
    en: 'Claude · Claude Code · Cursor · any MCP client',
    de: 'Claude · Claude Code · Cursor · jeder MCP-Client',
  },
  repos_title: { en: 'Two repositories, one platform', de: 'Zwei Repositories, eine Plattform' },
  app_desc: {
    en: 'The Flutter app for Android, iOS, Web, macOS, Windows and Linux.',
    de: 'Die Flutter-App für Android, iOS, Web, macOS, Windows und Linux.',
  },
  server_desc: {
    en: 'The Spring Boot 4 backend with Java 21, MongoDB, S3, SSO and Git integration.',
    de: 'Das Backend mit Spring Boot 4, Java 21, MongoDB, S3, SSO und Git-Integration.',
  },
  langs_title: {
    en: 'Nine languages, all of them complete',
    de: 'Neun Sprachen, alle vollständig',
  },
  langs_sub: {
    en: 'The whole app is translated. In Arabic the layout runs right to left, too.',
    de: 'Die ganze App ist übersetzt. Auf Arabisch läuft auch das Layout von rechts nach links.',
  },
  langs_note: {
    en: 'The flags stand for languages, not countries. They are just quicker to scan than names.',
    de: 'Die Flaggen stehen für Sprachen, nicht für Länder. Man erkennt sie nur schneller als Namen.',
  },
  langs_cta: { en: 'All nine, in detail →', de: 'Alle neun im Detail →' },
  docs: { en: 'Docs', de: 'Doku' },
  self_host: { en: 'Self-host', de: 'Self-Host' },
  privacy: { en: 'Privacy', de: 'Datenschutz' },
  terms: { en: 'Terms', de: 'Nutzungsbedingungen' },
};

export const QUICKSTART = `cp .env.example .env
./deploy/generate-secrets.sh   # Mongo keyfile + secrets
docker compose up -d`;

export const MCP_CONNECT = `claude mcp add --transport http hinata \\
  https://your-hinata-host/mcp \\
  --header "Authorization: Bearer hn_pat_..."`;

export const LINKS = {
  org: String(SITE.repo_org),
  app: String(SITE.repo_app),
  server: String(SITE.repo_server),
};
