#!/usr/bin/env python3
"""Screenshots for two user guide pages, light and dark, English.

- guide-sharing: sharing one issue with a person outside its project.
- guide-reports: the dashboard and the report page (with advanced time
  tracking on, /reports is the module's "Project" tab).

Same conventions as tools/capture.py: the built web app, a seeded demo server,
the session put into localStorage, desktop at 1440 x 900 @2. Every picture is
taken in both themes (`x.png` and `x-dark.png`; lib/markdown.ts shows the one
matching the reader's theme). The app itself never saves anything here: dialogs
and menus are photographed and closed again, the dashboard's edit mode is left
by navigating away.

What the pictures need and the demo seed does not carry is put in first through
the ordinary API, idempotently (a second run changes nothing):

- INF-2 "Offline cache for the dashboard" (project Infrastructure, which Lena
  and Mei are not members of) gets a short description, is shared with Lena
  and Mei by admin, and carries one comment by admin and Lena's answer.
- Time budgets, so the budget card and the Budgets tab have something to show:
  Hinata Platform 80 h plus a money budget of 15,000, Infrastructure 20 h, and the
  running sprint 40 h.

Run:  <venv>/bin/python tools/capture_guide_extra.py [sharing|reports]
Env:  HINATA_API (default http://localhost:8081), WEB_ORIGIN (default http://localhost:3001)
"""
from __future__ import annotations

import json
import os
import sys
import time

import requests
from playwright.sync_api import sync_playwright

API = os.environ.get("HINATA_API", "http://localhost:8081")
WEB = os.environ.get("WEB_ORIGIN", "http://localhost:3001")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
DESKTOP = (1440, 900, 2)
PASSWORD = "hinata-demo-2026"
SEMANTICS = """() => { const e = document.querySelector('flt-semantics-placeholder');
  if (e) for (const t of ['pointerdown','mousedown','pointerup','mouseup','click']) {
    const E = t.startsWith('pointer') ? PointerEvent : MouseEvent;
    e.dispatchEvent(new E(t, {bubbles: true, cancelable: true})); } }"""

SHARED_KEY = "INF-2"
SHARED_DESCRIPTION = (
    "Keep the last dashboard response on the device, so Home opens without a "
    "connection. The header shows how old the data is."
)
COMMENT_ADMIN = (
    "Lena, which dashboard cards have to work offline? We only cache what you pick."
)
COMMENT_LENA = "Today's focus and the sprint card. The ranking can wait for the network."


def login(user):
    r = requests.post(f"{API}/api/v1/auth/login", timeout=15,
                      json={"identifier": user, "password": PASSWORD})
    r.raise_for_status()
    return r.json()


def api(method, path, token, body=None):
    r = requests.request(method, f"{API}{path}", json=body, timeout=20,
                         headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json() if r.text else None


def content(page):
    return page if isinstance(page, list) else page.get("content", [])


SESSIONS = {u: login(u) for u in ("admin", "lena")}
ADMIN = SESSIONS["admin"]["accessToken"]
LENA = SESSIONS["lena"]["accessToken"]
USERS = {u["username"]: u["id"] for u in api("GET", "/api/v1/users?size=50", ADMIN)}
PROJECTS = {p["key"]: p["id"] for p in content(api("GET", "/api/v1/projects", ADMIN))}


def seed_sharing():
    issue = next(i for i in content(api(
        "GET", f"/api/v1/issues?projectId={PROJECTS['INF']}&size=50", ADMIN))
        if i["readableId"] == SHARED_KEY)
    iid = issue["id"]
    if not issue.get("description"):
        api("PATCH", f"/api/v1/issues/{iid}", ADMIN, {"description": SHARED_DESCRIPTION})
    for user in ("lena", "mei"):
        if USERS[user] not in (issue.get("participantIds") or []):
            api("PUT", f"/api/v1/issues/{iid}/participants/{USERS[user]}", ADMIN)
            time.sleep(1)
    comments = content(api("GET", f"/api/v1/issues/{iid}/comments?size=50", ADMIN))
    if not any(c.get("text") == COMMENT_ADMIN for c in comments):
        root = api("POST", f"/api/v1/issues/{iid}/comments", ADMIN, {"text": COMMENT_ADMIN})
        api("POST", f"/api/v1/issues/{iid}/comments", LENA,
            {"text": COMMENT_LENA, "replyToId": root["id"]})
    return iid


def seed_budgets():
    def project(key, minutes, cents=None):
        path = f"/api/v1/projects/{PROJECTS[key]}/time-settings"
        current = api("GET", path, ADMIN)
        if current.get("budgetMinutes"):
            return
        body = {k: current.get(k) for k in (
            "defaultBillable", "approvalRequired", "approvalPeriod", "lockBefore",
            "alertThresholds", "budgetLimitMode", "estimateLimitMode",
            "budgetCents", "budgetRateKind")}
        body["budgetMinutes"] = minutes
        if cents:
            body["budgetCents"], body["budgetRateKind"] = cents, "BILLABLE"
        api("PUT", path, ADMIN, body)

    project("HIN", 80 * 60, 15_000_00)
    project("INF", 20 * 60)
    for board in content(api("GET", "/api/v1/boards", ADMIN)):
        for sprint in api("GET", f"/api/v1/sprints?boardId={board['id']}", ADMIN):
            usage = api("GET", f"/api/v1/sprints/{sprint['id']}/time-usage", ADMIN)
            if sprint.get("startDate") and not usage.get("budgetMinutes"):
                api("PUT", f"/api/v1/sprints/{sprint['id']}/time-settings", ADMIN,
                    {"budgetMinutes": 40 * 60})


def init_script(user, theme):
    s = SESSIONS[user]
    prefs = {
        "flutter.onboarding_done": True,
        "flutter.locale": "en",
        "flutter.theme_mode": theme,
        "flutter.server_url": API,
        f"flutter.connect_hint_seen::{API}": True,
        f"flutter.multi_select_hint_seen::{API}": True,
        "flutter.access_token": s["accessToken"],
        "flutter.refresh_token": s["refreshToken"],
    }
    return "\n".join(f"localStorage.setItem({json.dumps(k)}, {json.dumps(json.dumps(v))});"
                     for k, v in prefs.items())


missing = []


def go(page, route, wait=7):
    page.goto(f"{WEB}{route}", wait_until="load")
    time.sleep(wait)
    page.evaluate(SEMANTICS)
    time.sleep(1.5)


def click(page, label, exact=True, first=False, wait=2.5):
    for loc in (page.get_by_role("button", name=label, exact=exact),
                page.get_by_role("menuitem", name=label, exact=exact),
                page.get_by_label(label, exact=exact),
                page.get_by_text(label, exact=exact)):
        if loc.count():
            (loc.first if first else loc.last).dispatch_event("click")
            time.sleep(wait)
            return True
    missing.append(label)
    print("  MISSING", label, flush=True)
    return False


def close(page):
    page.keyboard.press("Escape")
    time.sleep(1.2)


def scroll(page, dy, x=850, y=600):
    page.mouse.move(x, y)
    page.mouse.wheel(0, dy)
    time.sleep(2)


def context(browser, user, theme):
    w, h, dpr = DESKTOP
    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr,
                              color_scheme=theme, locale="en-GB")
    ctx.add_init_script(init_script(user, theme))
    return ctx, ctx.new_page()


def shooter(theme):
    suffix = "" if theme == "light" else "-dark"

    def shot(page, name, wait=1.5):
        time.sleep(wait)
        page.screenshot(path=os.path.join(OUT, f"{name}{suffix}.png"))
        print("shot", name + suffix, flush=True)
    return shot


def run_sharing(browser, theme):
    shot = shooter(theme)

    # A member: the "…" menu, the person search, the list of participants.
    ctx, page = context(browser, "admin", theme)
    go(page, f"/issues/{SHARED_KEY}")
    page.mouse.click(1408, 108)  # the "…" button at the right of the issue head
    time.sleep(2)
    shot(page, "shot-sharing-menu")
    if click(page, "Share with…", wait=3):
        shot(page, "shot-sharing-dialog")
        page.mouse.click(1217, 277)  # the search field at the top of the dialog
        time.sleep(1)
        page.keyboard.type("Amara", delay=60)
        time.sleep(3)
        shot(page, "shot-sharing-search")
        close(page)
    ctx.close()

    # The participant: her view of the issue, the note she got, her Watched
    # list and the question before leaving (answered with Escape).
    ctx, page = context(browser, "lena", theme)
    go(page, f"/issues/{SHARED_KEY}")
    shot(page, "shot-sharing-participant")
    if click(page, "Leave"):
        shot(page, "shot-sharing-leave")
        close(page)
    # The issue's history: who shared it with whom.
    go(page, f"/issues/{SHARED_KEY}")
    if click(page, "History"):
        scroll(page, 600, x=850, y=500)
        shot(page, "shot-sharing-history")
    go(page, "/notifications")
    shot(page, "shot-sharing-notification")
    go(page, "/watched")
    shot(page, "shot-sharing-watched")
    ctx.close()


def run_reports(browser, theme):
    shot = shooter(theme)
    ctx, page = context(browser, "admin", theme)

    go(page, "/dashboard")
    shot(page, "shot-dashboard")
    page.mouse.click(1337, 126)  # "Customize" in the page head
    time.sleep(3)
    shot(page, "shot-dashboard-customize")
    page.mouse.click(468, 250)  # the "Hero board" field of the edit bar
    time.sleep(2.5)
    shot(page, "shot-dashboard-hero-board-picker")
    close(page)

    go(page, "/reports")
    shot(page, "shot-reports")
    if click(page, "Hinata Platform", first=True):
        shot(page, "shot-reports-project-picker")
        close(page)
    if click(page, "Export"):
        shot(page, "shot-reports-export-menu")
        close(page)
    go(page, "/reports")
    scroll(page, 700)
    shot(page, "shot-reports-breakdowns")

    go(page, "/time/reports?tab=budgets")
    shot(page, "shot-reports-budgets")
    ctx.close()


which = sys.argv[1:] or ["sharing", "reports"]
if "sharing" in which:
    seed_sharing()
if "reports" in which:
    seed_budgets()

with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in os.environ.get("THEMES", "light,dark").split(","):
        if "sharing" in which:
            run_sharing(browser, theme)
        if "reports" in which:
            run_reports(browser, theme)
    browser.close()

if missing:
    print("missing:", sorted(set(missing)))
    sys.exit(1)
