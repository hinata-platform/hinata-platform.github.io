# Renders the root landing page (/). Bilingual via data-en/data-de attributes
# toggled client-side; defaults to the visitor's browser language.
from nav import SITE

FEATURES = [
    ("📊", {"en": "Dashboard & reports", "de": "Dashboard & Berichte"},
     {"en": "Burndown, velocity, cycle time, distributions — plus a personal daily focus view.",
      "de": "Burndown, Velocity, Cycle Time, Verteilungen — plus persönlicher Tagesfokus."}),
    ("📋", {"en": "Agile boards", "de": "Agile Boards"},
     {"en": "Board, Backlog & Timeline views with drag-and-drop, WIP limits and swimlanes.",
      "de": "Board-, Backlog- & Timeline-Ansichten mit Drag-and-drop, WIP-Limits und Swimlanes."}),
    ("🏃", {"en": "Sprints", "de": "Sprints"},
     {"en": "Plan, run and review sprints with capacity, story points and burndown.",
      "de": "Sprints planen, starten und auswerten — mit Kapazität, Story Points und Burndown."}),
    ("🐛", {"en": "Issues & hierarchy", "de": "Vorgänge & Hierarchie"},
     {"en": "Epics → stories/tasks/bugs → sub-tasks, dependencies, labels, comments, attachments.",
      "de": "Epics → Stories/Tasks/Bugs → Sub-Tasks, Abhängigkeiten, Labels, Kommentare, Anhänge."}),
    ("🔗", {"en": "Git integration", "de": "Git-Integration"},
     {"en": "GitHub, GitLab & Bitbucket — real OAuth, signed webhooks, smart commits, automation.",
      "de": "GitHub, GitLab & Bitbucket — echtes OAuth, signierte Webhooks, Smart Commits, Automation."}),
    ("🔑", {"en": "SSO & security", "de": "SSO & Sicherheit"},
     {"en": "OpenID Connect, OAuth 2.0, SAML, LDAP. JWT, BCrypt, rate limiting, OWASP-hardened.",
      "de": "OpenID Connect, OAuth 2.0, SAML, LDAP. JWT, BCrypt, Rate-Limiting, OWASP-gehärtet."}),
    ("📚", {"en": "Knowledge base", "de": "Wissensdatenbank"},
     {"en": "Hierarchical Markdown articles, global or per project, with smart links.",
      "de": "Hierarchische Markdown-Artikel, global oder pro Projekt, mit Smart Links."}),
    ("⏱️", {"en": "Time tracking", "de": "Zeiterfassung"},
     {"en": "Work items by activity type and weekly timesheets, feeding reports.",
      "de": "Arbeitszeiten nach Aktivität und wöchentliche Timesheets — direkt in den Berichten."}),
    ("🎨", {"en": "Bring your own server", "de": "Bring your own Server"},
     {"en": "One app, your self-hosted server, runtime branding. One Flutter codebase on Android, iOS, Web & macOS.",
      "de": "Eine App, dein selbst gehosteter Server, Laufzeit-Branding. Eine Flutter-Codebasis auf Android, iOS, Web & macOS."}),
]

T = {
    "eyebrow": {"en": "Open source · Self-hosted · GPL-3.0",
                "de": "Open Source · Self-hosted · GPL-3.0"},
    "headline_1": {"en": "Project management", "de": "Projektmanagement,"},
    "headline_2": {"en": "you actually own.", "de": "das dir gehört."},
    "sub": {
        "en": "Hinata is an independent, self-hosted project & issue tracker — agile boards, sprints, Gantt, time tracking, a knowledge base and deep Git integration. One Flutter app for Android, iOS, Web and macOS. No user, team or board limits. Ever.",
        "de": "Hinata ist ein unabhängiger, selbst-gehosteter Projekt- & Issue-Tracker — agile Boards, Sprints, Gantt, Zeiterfassung, Wissensdatenbank und tiefe Git-Integration. Eine Flutter-App für Android, iOS, Web und macOS. Keine Nutzer-, Team- oder Board-Limits. Niemals.",
    },
    "cta_start": {"en": "Get started", "de": "Loslegen"},
    "cta_host": {"en": "Self-hosting guide", "de": "Self-Hosting-Guide"},
    "features_title": {"en": "Everything a modern team needs", "de": "Alles, was ein modernes Team braucht"},
    "features_sub": {"en": "One platform, no add-ons, no seat pricing.",
                     "de": "Eine Plattform, keine Add-ons, keine Preise pro Sitzplatz."},
    "host_title": {"en": "Up and running in minutes", "de": "In Minuten einsatzbereit"},
    "host_sub": {
        "en": "Docker Compose brings up the server, a MongoDB replica set, object storage and mail. Point the app at your URL and finish the in-app setup wizard.",
        "de": "Docker Compose startet Server, MongoDB-Replica-Set, Objektspeicher und Mail. Richte die App auf deine URL und schließe den In-App-Setup-Assistenten ab.",
    },
    "host_cta": {"en": "Full deployment guide →", "de": "Vollständiger Deployment-Guide →"},
    "mcp_badge": {"en": "AI-native · MCP", "de": "KI-nativ · MCP"},
    "mcp_title_1": {"en": "Talk to Hinata", "de": "Sprich mit Hinata"},
    "mcp_title_2": {"en": "from Claude", "de": "über Claude"},
    "mcp_sub": {
        "en": "Hinata speaks the Model Context Protocol — a built-in /mcp endpoint, no sidecar to run. Connect Claude, Claude Code, Cursor or any MCP client and search issues, create work, log time or read the knowledge base, always within the connected user's exact permissions.",
        "de": "Hinata spricht das Model Context Protocol — ein eingebauter /mcp-Endpunkt, kein Sidecar nötig. Verbinde Claude, Claude Code, Cursor oder einen beliebigen MCP-Client und durchsuche Vorgänge, lege Arbeit an, buche Zeit oder lies die Wissensdatenbank — immer innerhalb der exakten Berechtigungen des verbundenen Nutzers.",
    },
    "mcp_cta": {"en": "Explore the MCP server →", "de": "MCP-Server entdecken →"},
    "mcp_clients": {"en": "Claude · Claude Code · Cursor · any MCP client",
                    "de": "Claude · Claude Code · Cursor · jeder MCP-Client"},
    "repos_title": {"en": "Two repositories, one platform", "de": "Zwei Repositories, eine Plattform"},
    "app_desc": {"en": "The Flutter client — Android, iOS, Web & macOS from a single codebase.",
                 "de": "Der Flutter-Client — Android, iOS, Web & macOS aus einer Codebasis."},
    "server_desc": {"en": "The Spring Boot 4 backend — Java 21, MongoDB, S3, SSO, Git integration.",
                    "de": "Das Spring-Boot-4-Backend — Java 21, MongoDB, S3, SSO, Git-Integration."},
    "docs_title": {"en": "Read the docs", "de": "Zur Dokumentation"},
}


def _t(key, both=True):
    en = T[key]["en"].replace('"', "&quot;")
    de = T[key]["de"].replace('"', "&quot;")
    return f'data-en="{en}" data-de="{de}"'


def render_landing(build_time: str) -> str:
    cards = ""
    for emoji, title, desc in FEATURES:
        cards += f"""
        <article class="feat-card glass">
          <div class="feat-emoji">{emoji}</div>
          <h3 data-en="{title['en']}" data-de="{title['de']}">{title['en']}</h3>
          <p data-en="{desc['en']}" data-de="{desc['de']}">{desc['en']}</p>
        </article>"""

    quickstart = """cp .env.example .env
./deploy/generate-secrets.sh   # Mongo keyfile + secrets
docker compose up -d"""

    mcp_connect = """claude mcp add --transport http hinata \\
  https://your-hinata-host/mcp \\
  --header "Authorization: Bearer hn_pat_..." """.rstrip()

    return f"""<!doctype html>
<html lang="en" data-theme="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hinata · Open-source, self-hosted project management</title>
<meta name="description" content="Hinata is an independent, self-hosted project & issue tracker with agile boards, sprints, Gantt, time tracking, a knowledge base and Git integration. Android, iOS, Web & macOS.">
<link rel="canonical" href="{SITE['base_url']}/">
<meta property="og:type" content="website">
<meta property="og:title" content="Hinata — project management you actually own">
<meta property="og:description" content="Open-source, self-hosted project & issue tracking. Boards, sprints, Gantt, Git integration. Android · iOS · Web · macOS.">
<meta property="og:url" content="{SITE['base_url']}/">
<meta name="theme-color" content="#151327">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<script>
  (function() {{
    try {{
      var t = localStorage.getItem('hinata-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', t);
    }} catch(e) {{ document.documentElement.setAttribute('data-theme','light'); }}
  }})();
</script>
</head>
<body class="landing">
<div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>

<header class="topbar">
  <div class="topbar-inner glass">
    <a class="brand" href="/">
      <span class="brand-mark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg></span>
      <span class="brand-name">Hinata<em>docs</em></span>
    </a>
    <nav class="landing-nav">
      <a href="/en/" data-en="Docs" data-de="Doku">Docs</a>
      <a href="/en/self-hosting.html" data-en="Self-host" data-de="Self-Host">Self-host</a>
      <a href="{SITE['repo_org']}" target="_blank" rel="noopener">GitHub</a>
    </nav>
    <div class="topbar-actions">
      <button class="lang-switch" id="langSwitch" aria-label="Language"><span id="langLabel">EN</span></button>
      <button class="icon-btn theme-toggle" id="themeToggle" aria-label="Toggle theme">
        <svg class="icon-sun" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
        <svg class="icon-moon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
      </button>
    </div>
  </div>
</header>

<main class="landing-main">
  <section class="hero">
    <span class="hero-eyebrow glass" {_t('eyebrow')}>{T['eyebrow']['en']}</span>
    <h1 class="hero-title">
      <span {_t('headline_1')}>{T['headline_1']['en']}</span>
      <span class="hero-accent" {_t('headline_2')}>{T['headline_2']['en']}</span>
    </h1>
    <p class="hero-sub" {_t('sub')}>{T['sub']['en']}</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="/en/quick-start.html" {_t('cta_start')}>{T['cta_start']['en']}</a>
      <a class="btn btn-ghost glass" href="/en/self-hosting.html" {_t('cta_host')}>{T['cta_host']['en']}</a>
    </div>
    <div class="hero-platforms">
      <span>Android</span><i>·</i><span>iOS</span><i>·</i><span>Web</span><i>·</i><span>macOS</span>
      <span class="ver-pill">v{SITE['version']}</span>
    </div>
  </section>

  <div class="hero-shot-wrap">
    <img class="device device-mac" src="/assets/img/frame-macbook.png" width="4260" height="2840"
         alt="Hinata on desktop — the dashboard shown in a MacBook" loading="eager">
    <img class="device device-phone" src="/assets/img/frame-iphone.png" width="1470" height="3000"
         alt="Hinata on mobile — the dashboard shown on an iPhone" loading="eager">
  </div>

  <section class="section">
    <div class="section-head">
      <h2 {_t('features_title')}>{T['features_title']['en']}</h2>
      <p {_t('features_sub')}>{T['features_sub']['en']}</p>
    </div>
    <div class="feat-grid">{cards}</div>
  </section>

  <section class="section">
    <div class="host-split glass">
      <div class="host-copy">
        <h2 {_t('host_title')}>{T['host_title']['en']}</h2>
        <p {_t('host_sub')}>{T['host_sub']['en']}</p>
        <a class="btn btn-primary" href="/en/deployment.html" {_t('host_cta')}>{T['host_cta']['en']}</a>
      </div>
      <div class="host-code">
        <div class="code-window">
          <div class="code-dots"><i></i><i></i><i></i></div>
          <pre><code>{quickstart}</code></pre>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="host-split mcp-split glass">
      <div class="host-code">
        <div class="code-window">
          <div class="code-dots"><i></i><i></i><i></i></div>
          <pre><code>{mcp_connect}</code></pre>
        </div>
      </div>
      <div class="host-copy">
        <span class="mcp-badge" {_t('mcp_badge')}>{T['mcp_badge']['en']}</span>
        <h2 class="mcp-title">
          <span {_t('mcp_title_1')}>{T['mcp_title_1']['en']}</span>
          <span {_t('mcp_title_2')}>{T['mcp_title_2']['en']}</span>
        </h2>
        <p {_t('mcp_sub')}>{T['mcp_sub']['en']}</p>
        <a class="btn btn-primary" href="/en/mcp.html" {_t('mcp_cta')}>{T['mcp_cta']['en']}</a>
        <p class="mcp-clients" {_t('mcp_clients')}>{T['mcp_clients']['en']}</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-head"><h2 {_t('repos_title')}>{T['repos_title']['en']}</h2></div>
    <div class="repo-grid">
      <a class="repo-card glass" href="{SITE['repo_app']}" target="_blank" rel="noopener">
        <div class="repo-badge">Flutter · Dart</div>
        <h3>hinata-app</h3>
        <p data-en="{T['app_desc']['en']}" data-de="{T['app_desc']['de']}">{T['app_desc']['en']}</p>
        <span class="repo-link">github.com/hinata-platform/hinata-app →</span>
      </a>
      <a class="repo-card glass" href="{SITE['repo_server']}" target="_blank" rel="noopener">
        <div class="repo-badge">Spring Boot 4 · Java 21</div>
        <h3>hinata-server</h3>
        <p data-en="{T['server_desc']['en']}" data-de="{T['server_desc']['de']}">{T['server_desc']['en']}</p>
        <span class="repo-link">github.com/hinata-platform/hinata-server →</span>
      </a>
    </div>
  </section>
</main>

<footer class="landing-footer">
  <p>© <span id="year">2026</span> Hinata · Made with 🍯 · GPL-3.0</p>
  <div>
    <a href="/en/">Docs</a>
    <a href="{SITE['repo_app']}" target="_blank" rel="noopener">App</a>
    <a href="{SITE['repo_server']}" target="_blank" rel="noopener">Server</a>
    <a href="/privacy-policy" data-en="Privacy" data-de="Datenschutz">Privacy</a>
    <a href="/terms-of-service" data-en="Terms" data-de="Nutzungsbedingungen">Terms</a>
  </div>
</footer>

<script src="/assets/landing.js" defer></script>
</body>
</html>
"""
