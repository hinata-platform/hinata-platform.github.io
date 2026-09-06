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
      en: 'Burndown, velocity, cycle time, distributions — plus a personal daily focus view.',
      de: 'Burndown, Velocity, Cycle Time, Verteilungen — plus persönlicher Tagesfokus.',
    },
  },
  {
    emoji: '📋',
    title: { en: 'Agile boards', de: 'Agile Boards' },
    desc: {
      en: 'Board, Backlog & Timeline views with drag-and-drop, WIP limits and swimlanes.',
      de: 'Board-, Backlog- & Timeline-Ansichten mit Drag-and-drop, WIP-Limits und Swimlanes.',
    },
  },
  {
    emoji: '🏃',
    title: { en: 'Sprints', de: 'Sprints' },
    desc: {
      en: 'Plan, run and review sprints with capacity, story points and burndown.',
      de: 'Sprints planen, starten und auswerten — mit Kapazität, Story Points und Burndown.',
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
      en: 'GitHub, GitLab & Bitbucket — real OAuth, signed webhooks, smart commits, automation.',
      de: 'GitHub, GitLab & Bitbucket — echtes OAuth, signierte Webhooks, Smart Commits, Automation.',
    },
  },
  {
    emoji: '🔑',
    title: { en: 'SSO & security', de: 'SSO & Sicherheit' },
    desc: {
      en: 'OpenID Connect, OAuth 2.0, SAML, LDAP. JWT, BCrypt, rate limiting, OWASP-hardened.',
      de: 'OpenID Connect, OAuth 2.0, SAML, LDAP. JWT, BCrypt, Rate-Limiting, OWASP-gehärtet.',
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
      en: 'Work items by activity type and weekly timesheets, feeding reports.',
      de: 'Arbeitszeiten nach Aktivität und wöchentliche Timesheets — direkt in den Berichten.',
    },
  },
  {
    emoji: '🎨',
    title: { en: 'Bring your own server', de: 'Bring your own Server' },
    desc: {
      en: 'One app, your self-hosted server, runtime branding. One Flutter codebase, six platforms — mobile, web and desktop.',
      de: 'Eine App, dein selbst gehosteter Server, Laufzeit-Branding. Eine Flutter-Codebasis, sechs Plattformen — Mobile, Web und Desktop.',
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
    en: 'Hinata is an independent, self-hosted project & issue tracker — agile boards, sprints, Gantt, time tracking, a knowledge base and deep Git integration. One Flutter app, six platforms: Android, iOS, Web, macOS, Windows and Linux. No user, team or board limits. Ever.',
    de: 'Hinata ist ein unabhängiger, selbst-gehosteter Projekt- & Issue-Tracker — agile Boards, Sprints, Gantt, Zeiterfassung, Wissensdatenbank und tiefe Git-Integration. Eine Flutter-App, sechs Plattformen: Android, iOS, Web, macOS, Windows und Linux. Keine Nutzer-, Team- oder Board-Limits. Niemals.',
  },
  cta_start: { en: 'Get started', de: 'Loslegen' },
  cta_host: { en: 'Self-hosting guide', de: 'Self-Hosting-Guide' },
  features_title: {
    en: 'Everything a modern team needs',
    de: 'Alles, was ein modernes Team braucht',
  },
  features_sub: {
    en: 'One platform, no add-ons, no seat pricing.',
    de: 'Eine Plattform, keine Add-ons, keine Preise pro Sitzplatz.',
  },
  host_title: { en: 'Up and running in minutes', de: 'In Minuten einsatzbereit' },
  host_sub: {
    en: 'Docker Compose brings up the server, a MongoDB replica set, object storage and mail. Point the app at your URL and finish the in-app setup wizard.',
    de: 'Docker Compose startet Server, MongoDB-Replica-Set, Objektspeicher und Mail. Richte die App auf deine URL und schließe den In-App-Setup-Assistenten ab.',
  },
  host_cta: { en: 'Full deployment guide →', de: 'Vollständiger Deployment-Guide →' },
  mcp_badge: { en: 'AI-native · MCP', de: 'KI-nativ · MCP' },
  mcp_title_1: { en: 'Talk to Hinata', de: 'Sprich mit Hinata' },
  mcp_title_2: { en: 'from Claude', de: 'über Claude' },
  mcp_sub: {
    en: 'Hinata speaks the Model Context Protocol — a built-in /mcp endpoint, no sidecar to run. Connect Claude, Claude Code, Cursor or any MCP client and search issues, create work, log time or read the knowledge base, always within the connected user’s exact permissions.',
    de: 'Hinata spricht das Model Context Protocol — ein eingebauter /mcp-Endpunkt, kein Sidecar nötig. Verbinde Claude, Claude Code, Cursor oder einen beliebigen MCP-Client und durchsuche Vorgänge, lege Arbeit an, buche Zeit oder lies die Wissensdatenbank — immer innerhalb der exakten Berechtigungen des verbundenen Nutzers.',
  },
  mcp_cta: { en: 'Explore the MCP server →', de: 'MCP-Server entdecken →' },
  mcp_clients: {
    en: 'Claude · Claude Code · Cursor · any MCP client',
    de: 'Claude · Claude Code · Cursor · jeder MCP-Client',
  },
  repos_title: { en: 'Two repositories, one platform', de: 'Zwei Repositories, eine Plattform' },
  app_desc: {
    en: 'The Flutter client — Android, iOS, Web, macOS, Windows & Linux from one codebase.',
    de: 'Der Flutter-Client — Android, iOS, Web, macOS, Windows & Linux aus einer Codebasis.',
  },
  server_desc: {
    en: 'The Spring Boot 4 backend — Java 21, MongoDB, S3, SSO, Git integration.',
    de: 'Das Spring-Boot-4-Backend — Java 21, MongoDB, S3, SSO, Git-Integration.',
  },
  langs_title: {
    en: 'Nine languages, all of them complete',
    de: 'Neun Sprachen, alle vollständig',
  },
  langs_sub: {
    en: 'Every string, not a translated menu bar over an English app — and Arabic turns the whole layout right to left, not only the words.',
    de: 'Jede Zeichenkette, nicht eine übersetzte Menüleiste über einer englischen App — und Arabisch dreht das ganze Layout nach rechts-nach-links, nicht nur die Wörter.',
  },
  langs_note: {
    en: 'A flag is a country, not a language. They are signposts, because nine of them read faster than nine names.',
    de: 'Eine Flagge ist ein Land, keine Sprache. Sie stehen hier als Wegweiser, weil neun Bilder schneller zu erfassen sind als neun Namen.',
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
