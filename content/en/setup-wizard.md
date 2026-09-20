---
title: Setup & first run
description: On first run you connect the app to your server and create the organization and first admin, via the wizard or automatically.
---

# Setup & first run

A fresh Hinata server has no users and no organization. On **first run** you point the app at your server, and an in-app **setup wizard** creates the organization and the first admin account.

## The flow at a glance

1. **Connect:** the app asks for your server URL and calls `HINATA_BASE_URL`.
2. **Version gate:** the app checks its version against `HINATA_APP_MIN_VERSION`. Older clients must update first.
3. **Setup status:** the app calls `GET /api/v1/setup/status`. If setup is not complete, it shows the wizard instead of the login screen.
4. **Create org and admin:** you enter the organization name and the admin account. The app posts to `POST /api/v1/setup`.
5. **Onboarding tour:** after login, a short tour highlights the dashboard, projects and the ⌘K palette.

!!! info "Setup needs no token"
    `GET /setup/status` and `POST /setup` are public because they must work before any account exists. Once setup is complete, `POST /setup` refuses to run again, so nobody can create a second rogue organization.

## Connecting the app

Native apps never bake in a server URL. You enter it on first launch (the web build defaults to its own origin). Enter your **API** base:

```text
https://api.track.example.com
```

The app stores the server and probes it live. Later you can save several servers and switch between them. More on this:

- [The apps](/en/clients.html): the multi-server manager.
- [Reverse proxy & TLS](/en/reverse-proxy.html): how that hostname maps to the API container.

!!! tip "The minimum version forces updates"
    `HINATA_APP_MIN_VERSION` (default `1.0.0`) is the oldest client version your server accepts. Raise it after a breaking change and older apps are prompted to update. The value is served through `/api/v1/meta` and can be edited live in [Admin area → Platform](/en/admin-area.html) (DB overrides env).

## Interactive setup wizard

When `GET /setup/status` reports setup as incomplete, the wizard appears. You provide:

- **Organization name:** your workspace or company name.
- **Admin display name:** how the first admin appears in the UI.
- **Admin username** and **e-mail**.
- **Admin password:** at least 10 characters (hashed with BCrypt, strength 12).

Submitting calls `POST /api/v1/setup`, which creates the organization and the first `ADMIN` user in one atomic step and logs you straight in. From there you create projects and invite people, see [Projects & teams](/en/projects-teams.html).

## Non-interactive setup (automation)

For scripted or reproducible deployments you skip the wizard and let the server complete setup on boot. Set `HINATA_SETUP_AUTO_COMPLETE=true` and provide the admin details as environment variables:

```properties
# Skip the in-app first-run wizard and provision the org + first admin on boot
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-to-a-strong-password
HINATA_SETUP_ADMIN_DISPLAY_NAME=Platform Admin
```

On the next start the server creates the organization and admin. `GET /setup/status` reports complete right away, so the app goes straight to login. This is idempotent: if setup is already done, the variables are ignored.

!!! warning "The admin password is a secret"
    `HINATA_SETUP_ADMIN_PASSWORD` sits in plaintext in your `.env` or your orchestrator's secret store. Use a strong value, keep the file out of version control (see [Backups & upgrades](/en/backups.html)) and change the password in the app after first login. The server rejects anything shorter than 10 characters.

## Onboarding tour

After the first login, a short tour points out the dashboard's *today's focus*, how to create your first project, and the ⌘K command palette ([Search & palette](/en/search.html)). It shows once and can be dismissed at any point.

## Evaluating locally with the demo seed

For a quick local look with realistic content (projects, issues, sprints, a knowledge base, people), enable the demo seeder. It creates a complete English workspace **and** completes first-run setup for you:

```properties
# Dev only: seed a realistic demo workspace on boot
HINATA_DEMO_SEED=true
# Optional: wipe and re-seed the same dataset on every boot (repeatable testing)
HINATA_DEMO_RESET=false
```

Log in with:

```text
username: rebar
password: hinata-demo-2026
```

!!! danger "Never enable the demo seed in production"
    The seeder is annotated `@Profile("!prod")`, so it is **skipped entirely** under the `prod` profile, whatever `HINATA_DEMO_SEED` says. It is meant for clicking through the app and taking screenshots on a dev profile. Its password is publicly known, and with `HINATA_DEMO_RESET=true` it **wipes the workspace on every boot**. Keep it off anywhere real data lives.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| App shows "update required" and won't continue | Client version < `HINATA_APP_MIN_VERSION`. Update the app or lower the minimum version |
| Wizard never appears, app goes straight to login | Setup already complete (`GET /setup/status` returns done) or auto-complete ran |
| Can't reach the server on connect | Wrong URL, proxy or TLS misconfigured, or CORS origin missing. See [Reverse proxy & TLS](/en/reverse-proxy.html) |
| `POST /setup` rejected | Setup already ran once. It only runs while no organization exists |

## Next steps

- [Authentication](/en/authentication.html): logins, registration, 2FA and password reset
- [Admin area](/en/admin-area.html): feature flags, app settings, runtime config
- [Projects & teams](/en/projects-teams.html): create your first project and invite people
- [Backups & upgrades](/en/backups.html): keep the running stack safe
