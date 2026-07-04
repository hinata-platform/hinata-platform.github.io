---
title: Setup & first run
description: The first-run flow — connect the app to your server, pass the version gate, then create your organization and first admin via the wizard or non-interactively.
---

# Setup & first run

A fresh Hinata server has no users and no organization. The **first run** is
where that gets fixed: you point the app at your server, and an in-app **setup
wizard** creates the organization and the first admin account. This page walks
through the interactive flow, the fully automated alternative, and how to seed a
throwaway demo workspace for local evaluation.

## The flow at a glance

1. **Connect** — the app asks for your server URL and calls `HINATA_BASE_URL`.
2. **Version gate** — the app checks its version against `HINATA_APP_MIN_VERSION`;
   older clients are asked to update before they can continue.
3. **Setup status** — the app calls `GET /api/v1/setup/status`. If setup is not
   complete, it shows the wizard instead of the login screen.
4. **Create org + admin** — you fill in the organization name and the first admin
   account; the app posts to `POST /api/v1/setup`.
5. **Onboarding tour** — after logging in, a short guided tour highlights the
   dashboard, projects and the ⌘K palette.

!!! info "Setup endpoints are public"
    `GET /setup/status` and `POST /setup` are among the few endpoints that need
    no token — they have to work before any account exists. Once setup is
    complete, `POST /setup` refuses to run again, so it can't be used to create a
    second rogue organization.

## Connecting the app

Native apps never bake in a server URL — you enter it on first launch (the web
build defaults to its own origin). Give the app your **API** base:

```text
https://api.track.example.com
```

The app stores this server, probes it live, and lets you save and switch between
multiple servers later. See [The apps](/en/clients.html) for the multi-server
manager, and [Reverse proxy & TLS](/en/reverse-proxy.html) for how that
hostname maps to the API container.

!!! tip "The version gate is your force-update switch"
    `HINATA_APP_MIN_VERSION` (default `1.0.0`) is the minimum client version your
    server accepts. Bump it after a breaking change and older apps are prompted
    to update — this is served through `/api/v1/meta` and can also be edited live
    in [Admin area → App](/en/admin-area.html) (DB overrides env).

## Interactive setup wizard

When `GET /setup/status` reports that setup is incomplete, the app shows the
wizard. You provide:

- **Organization name** — your workspace/company name.
- **Admin display name** — how the first admin appears in the UI.
- **Admin username** and **e-mail**.
- **Admin password** — minimum 10 characters (hashed with BCrypt, strength 12).

Submitting posts to `POST /api/v1/setup`, which creates the organization and the
first `ADMIN` user in one atomic step, then logs you straight in. From there you
create projects and invite people — see [Projects & teams](/en/projects-teams.html).

## Non-interactive setup (automation)

For scripted or reproducible deployments you can skip the wizard entirely and
have the server complete setup on boot. Set `HINATA_SETUP_AUTO_COMPLETE=true` and
provide the admin details as environment variables:

```properties
# Skip the in-app first-run wizard and provision the org + first admin on boot
HINATA_SETUP_AUTO_COMPLETE=true
HINATA_SETUP_ORGANIZATION_NAME=Example Org
HINATA_SETUP_ADMIN_EMAIL=admin@example.com
HINATA_SETUP_ADMIN_USERNAME=admin
HINATA_SETUP_ADMIN_PASSWORD=change-me-to-a-strong-password
HINATA_SETUP_ADMIN_DISPLAY_NAME=Platform Admin
```

On the next start the server provisions the organization and admin, and
`GET /setup/status` immediately reports complete — so the app goes straight to
the login screen. This is idempotent: if setup is already done, these variables
are ignored.

!!! warning "Treat the admin password like any other secret"
    `HINATA_SETUP_ADMIN_PASSWORD` lands in your `.env` / orchestrator secret
    store in plaintext. Use a strong value, keep the file out of version control
    (see [Backups & upgrades](/en/backups.html)), and change the password from
    inside the app after first login. The minimum length is 10 characters; the
    server rejects anything shorter.

## Onboarding tour

After the first login the app runs a short onboarding tour that points out the
dashboard's *today's focus*, how to create your first project, and the ⌘K
command palette ([Search & palette](/en/search.html)). It's a one-time nudge and
can be dismissed at any point.

## Evaluating locally with the demo seed

For a quick local look at Hinata with realistic content — projects, issues,
sprints, a knowledge base and people — enable the demo seeder. It provisions a
complete English workspace **and** completes first-run setup for you:

```properties
# Dev only — seed a realistic demo workspace on boot
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
    The seeder is annotated `@Profile("!prod")`, so it is **skipped entirely**
    under the `prod` profile regardless of `HINATA_DEMO_SEED`. It exists for
    clicking through the app and capturing screenshots on a dev profile. It ships
    a well-known password and, with `HINATA_DEMO_RESET=true`, **wipes the
    workspace on every boot** — obviously catastrophic against real data. Keep it
    off anywhere that matters.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| App shows "update required" and won't continue | Client version < `HINATA_APP_MIN_VERSION`; update the app or lower the gate |
| Wizard never appears, goes straight to login | Setup already complete (`GET /setup/status` returns done) or auto-complete ran |
| Can't reach the server on connect | Wrong URL, proxy/TLS misconfigured, or CORS origin missing — see [Reverse proxy & TLS](/en/reverse-proxy.html) |
| `POST /setup` rejected | Setup already completed once; it can only run when no org exists |

## Next steps

- [Authentication](/en/authentication.html) — logins, registration, 2FA and password reset
- [Admin area](/en/admin-area.html) — feature flags, app settings, runtime config
- [Projects & teams](/en/projects-teams.html) — create your first project and invite people
- [Backups & upgrades](/en/backups.html) — keep the running stack safe
