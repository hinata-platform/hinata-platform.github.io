# Navigation & site structure for the Hinata documentation.
# Single source of truth consumed by build.py. Each page lists its slug and its
# per-language title. Ordering here defines sidebar order and prev/next links.

import json
import os
import re
import urllib.request


APP_REPO = "hinata-platform/hinata-app"


def _tag_page(page: int) -> list:
    """One page of hinata-app tags from the GitHub API."""
    req = urllib.request.Request(
        f"https://api.github.com/repos/{APP_REPO}/tags?per_page=100&page={page}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "hinata-docs-build"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)


def _latest_app_version() -> str:
    """Highest vX.Y.Z release tag on hinata-app.

    There is no version number written down anywhere in this repository — it is
    resolved from the GitHub API on every build. The tag endpoint is not ordered
    by semver, so we page through everything and take the maximum rather than
    trusting the first entry. A failure aborts the build instead of inventing a
    number: publishing a wrong version is worse than not publishing.

    The resolved value is baked into the pages; assets/version.js refreshes it in
    the browser, so a release that ships after the last deploy is still shown.
    """
    versions = []
    try:
        for page in range(1, 4):
            tags = _tag_page(page)
            versions += [
                tuple(int(n) for n in m.groups())
                for m in (re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", t.get("name", "")) for t in tags)
                if m
            ]
            if len(tags) < 100:
                break
    except (OSError, ValueError) as exc:  # URLError/HTTPError are OSErrors
        raise RuntimeError(f"cannot resolve the latest {APP_REPO} tag: {exc}") from exc
    if not versions:
        raise RuntimeError(f"no vX.Y.Z tags found on {APP_REPO}")
    return ".".join(str(n) for n in max(versions))


SITE = {
    "name": "Hinata",
    "tagline": {
        "en": "Open-source, self-hosted project management",
        "de": "Open-Source, selbst-gehostetes Projektmanagement",
    },
    # Resolved live from the newest hinata-app tag; the browser refreshes it too.
    "version": _latest_app_version(),
    "app_repo": APP_REPO,
    "accent": "#D9A032",
    "repo_org": "https://github.com/hinata-platform",
    "repo_app": f"https://github.com/{APP_REPO}",
    "repo_server": "https://github.com/hinata-platform/hinata-server",
    "base_url": "https://hinata.ahmadre.com",
    "languages": ["en", "de"],
}

# UI strings that appear in the chrome (not in page bodies).
UI = {
    "en": {
        "search_placeholder": "Search the docs…",
        "search_hint": "Search",
        "on_this_page": "On this page",
        "previous": "Previous",
        "next": "Next",
        "edit_page": "Edit this page",
        "last_built": "Last built",
        "menu": "Menu",
        "theme": "Toggle theme",
        "language": "Language",
        "get_started": "Get started",
        "self_host": "Self-host it",
        "docs": "Documentation",
        "no_results": "No results found",
        "search_empty": "Start typing to search across every page.",
        "back_home": "Back to overview",
        "copy": "Copy",
        "copied": "Copied!",
    },
    "de": {
        "search_placeholder": "Doku durchsuchen…",
        "search_hint": "Suche",
        "on_this_page": "Auf dieser Seite",
        "previous": "Zurück",
        "next": "Weiter",
        "edit_page": "Diese Seite bearbeiten",
        "last_built": "Zuletzt erstellt",
        "menu": "Menü",
        "theme": "Thema wechseln",
        "language": "Sprache",
        "get_started": "Loslegen",
        "self_host": "Selbst hosten",
        "docs": "Dokumentation",
        "no_results": "Keine Ergebnisse gefunden",
        "search_empty": "Tippen, um alle Seiten zu durchsuchen.",
        "back_home": "Zurück zur Übersicht",
        "copy": "Kopieren",
        "copied": "Kopiert!",
    },
}

# Sidebar groups. Each group: id, per-language label, and ordered pages.
# A page: (slug, {"en": title, "de": title}). The first page 'index' is home.
NAV = [
    {
        "id": "overview",
        "icon": "compass",
        "label": {"en": "Overview", "de": "Überblick"},
        "pages": [
            ("index", {"en": "Introduction", "de": "Einführung"}),
            ("architecture", {"en": "Architecture", "de": "Architektur"}),
            ("concepts", {"en": "Core concepts", "de": "Grundkonzepte"}),
        ],
    },
    {
        "id": "getting-started",
        "icon": "rocket",
        "label": {"en": "Getting started", "de": "Erste Schritte"},
        "pages": [
            ("quick-start", {"en": "Quick start", "de": "Schnellstart"}),
            ("requirements", {"en": "Requirements", "de": "Voraussetzungen"}),
        ],
    },
    {
        "id": "guide",
        "icon": "sparkles",
        "label": {"en": "User guide", "de": "Handbuch"},
        "pages": [
            ("guide-start", {"en": "Getting started", "de": "Erste Schritte"}),
            ("guide-projects", {"en": "Projects & teams", "de": "Projekte & Teams"}),
            ("guide-issues", {"en": "Working with issues", "de": "Mit Vorgängen arbeiten"}),
            ("guide-boards", {"en": "Boards & sprints", "de": "Boards & Sprints"}),
            ("guide-timeline", {"en": "Timeline & dependencies", "de": "Timeline & Abhängigkeiten"}),
            ("guide-time", {"en": "Tracking your time", "de": "Zeit erfassen"}),
            ("guide-collaboration", {"en": "Comments & attachments", "de": "Kommentare & Anhänge"}),
            ("guide-search", {"en": "Finding things", "de": "Dinge finden"}),
            ("guide-knowledge", {"en": "Writing documentation", "de": "Dokumentation schreiben"}),
            ("guide-reports", {"en": "Reports & dashboard", "de": "Berichte & Dashboard"}),
            ("guide-notifications", {"en": "Staying informed", "de": "Auf dem Laufenden bleiben"}),
            ("guide-account", {"en": "Your account", "de": "Dein Konto"}),
            ("guide-mobile", {"en": "On your phone", "de": "Auf dem Handy"}),
        ],
    },
    {
        "id": "self-hosting",
        "icon": "server",
        "label": {"en": "Self-hosting", "de": "Self-Hosting"},
        "pages": [
            ("self-hosting", {"en": "Overview", "de": "Überblick"}),
            ("deployment", {"en": "Production deployment", "de": "Produktiv-Deployment"}),
            ("configuration", {"en": "Configuration reference", "de": "Konfigurationsreferenz"}),
            ("database", {"en": "MongoDB & X.509", "de": "MongoDB & X.509"}),
            ("storage", {"en": "Object storage (S3/MinIO)", "de": "Objektspeicher (S3/MinIO)"}),
            ("email", {"en": "E-mail & SMTP", "de": "E-Mail & SMTP"}),
            ("reverse-proxy", {"en": "Reverse proxy & TLS", "de": "Reverse Proxy & TLS"}),
            ("setup-wizard", {"en": "Setup & first run", "de": "Setup & Erststart"}),
            ("backups", {"en": "Backups & upgrades", "de": "Backups & Upgrades"}),
        ],
    },
    {
        "id": "features",
        "icon": "sparkles",
        "label": {"en": "Features", "de": "Funktionen"},
        "pages": [
            ("features", {"en": "Feature tour", "de": "Feature-Tour"}),
            ("projects-teams", {"en": "Projects & teams", "de": "Projekte & Teams"}),
            ("issues", {"en": "Issues & hierarchy", "de": "Vorgänge & Hierarchie"}),
            ("boards-sprints", {"en": "Boards & sprints", "de": "Boards & Sprints"}),
            ("timeline", {"en": "Gantt & time tracking", "de": "Gantt & Zeiterfassung"}),
            ("reports", {"en": "Reports & dashboard", "de": "Berichte & Dashboard"}),
            ("knowledge-base", {"en": "Knowledge base", "de": "Wissensdatenbank"}),
            ("notifications", {"en": "Notifications", "de": "Benachrichtigungen"}),
            ("search", {"en": "Search & palette", "de": "Suche & Palette"}),
        ],
    },
    {
        "id": "security",
        "icon": "shield",
        "label": {"en": "Auth & security", "de": "Auth & Sicherheit"},
        "pages": [
            ("authentication", {"en": "Authentication", "de": "Authentifizierung"}),
            ("sso", {"en": "Single sign-on (SSO)", "de": "Single Sign-on (SSO)"}),
            ("security", {"en": "Security model", "de": "Sicherheitsmodell"}),
        ],
    },
    {
        "id": "integrations",
        "icon": "plug",
        "label": {"en": "Integrations", "de": "Integrationen"},
        "pages": [
            ("git-integration", {"en": "Git integration", "de": "Git-Integration"}),
            ("email-to-ticket", {"en": "E-mail to ticket", "de": "E-Mail zu Vorgang"}),
            ("connect-gateway", {"en": "Hinata Connect gateway", "de": "Hinata Connect Gateway"}),
            ("mcp", {"en": "MCP server (AI)", "de": "MCP-Server (KI)"}),
        ],
    },
    {
        "id": "apps",
        "icon": "devices",
        "label": {"en": "Apps & branding", "de": "Apps & Branding"},
        "pages": [
            ("download", {"en": "Download", "de": "Download"}),
            ("clients", {"en": "The apps", "de": "Die Apps"}),
            ("self-hosted-app", {"en": "Branding & custom clients", "de": "Branding & eigene Clients"}),
        ],
    },
    {
        "id": "administration",
        "icon": "settings",
        "label": {"en": "Administration", "de": "Administration"},
        "pages": [
            ("admin-area", {"en": "Admin area", "de": "Adminbereich"}),
            ("project-settings", {"en": "Project settings", "de": "Projekteinstellungen"}),
        ],
    },
    {
        "id": "reference",
        "icon": "book",
        "label": {"en": "Reference", "de": "Referenz"},
        "pages": [
            ("api", {"en": "API reference", "de": "API-Referenz"}),
            ("development", {"en": "Development", "de": "Entwicklung"}),
            ("contributing", {"en": "Contributing", "de": "Mitwirken"}),
            ("faq", {"en": "FAQ & troubleshooting", "de": "FAQ & Fehlerbehebung"}),
        ],
    },
]

# Standalone legal pages: built like docs pages (per language) but NOT part of
# the sidebar navigation — they are linked from the site footers and referenced
# by the apps/store listings at /privacy-policy and /terms-of-service.
LEGAL_PAGES = [
    ("privacy-policy", {"en": "Privacy policy", "de": "Datenschutzerklärung"}),
    ("terms-of-service", {"en": "Terms of service", "de": "Nutzungsbedingungen"}),
]
