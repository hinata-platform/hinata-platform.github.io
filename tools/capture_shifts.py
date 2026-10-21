#!/usr/bin/env python3
"""Screenshots for the user guide's shift planning page, light and dark, English.

Same conventions as tools/capture.py: the built web app, a seeded demo server
with shift planning switched on, the session put into localStorage, desktop at
1440 x 900 @2 and phone at 390 x 844 @3. Each picture is taken in both themes
(`x.png` and `x-dark.png`; lib/markdown.ts shows the one matching the reader's
theme). Nothing here saves: every dialog is photographed and closed again.
Output: assets/img/shot-shifts-*.png.

Run:  <venv>/bin/python tools/capture_shifts.py
Env:  HINATA_API (default http://localhost:8081), WEB_ORIGIN (default http://localhost:3001)
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import requests
from playwright.sync_api import sync_playwright

API = os.environ.get("HINATA_API", "http://localhost:8081")
WEB = os.environ.get("WEB_ORIGIN", "http://localhost:3001")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
DESKTOP = (1440, 900, 2)
PHONE = (390, 844, 3)
SEMANTICS = """() => { const e = document.querySelector('flt-semantics-placeholder');
  if (e) for (const t of ['pointerdown','mousedown','pointerup','mouseup','click']) {
    const E = t.startsWith('pointer') ? PointerEvent : MouseEvent;
    e.dispatchEvent(new E(t, {bubbles: true, cancelable: true})); } }"""


def api(method, path, token=None, body=None):
    r = requests.request(method, f"{API}{path}", json=body, timeout=15,
                         headers={"Authorization": f"Bearer {token}"} if token else {})
    r.raise_for_status()
    return r.json() if r.text else None


login = api("POST", "/api/v1/auth/login", body={"identifier": "admin", "password": "hinata-demo-2026"})
ACCESS, REFRESH = login["accessToken"], login["refreshToken"]
now = datetime.now(timezone.utc)
iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
events = api("GET", f"/api/v1/shifts/events?from={iso(now - timedelta(days=1))}"
                    f"&to={iso(now + timedelta(days=60))}&size=50", ACCESS)["content"]
FAIR = next(e for e in events if e["title"].startswith("Trade fair"))
PARTY = next(e for e in events if e["title"].startswith("Summer party"))
FAIR_DAY = FAIR["startsLocal"][:10]


def init_script(theme):
    prefs = {
        "flutter.onboarding_done": True,
        "flutter.locale": "en",
        "flutter.theme_mode": theme,
        "flutter.server_url": API,
        f"flutter.connect_hint_seen::{API}": True,
        f"flutter.multi_select_hint_seen::{API}": True,
        "flutter.access_token": ACCESS,
        "flutter.refresh_token": REFRESH,
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


def run(browser, theme):
    suffix = "" if theme == "light" else "-dark"

    def shot(page, name, wait=1.5):
        time.sleep(wait)
        page.screenshot(path=os.path.join(OUT, f"{name}{suffix}.png"))
        print("shot", name + suffix, flush=True)

    # --- desktop ---------------------------------------------------------------
    w, h, dpr = DESKTOP
    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr,
                              color_scheme=theme, locale="en-GB")
    ctx.add_init_script(init_script(theme))
    page = ctx.new_page()

    # The switch sits far down the platform section, under the app release
    # fields; scroll it to the middle so the picture shows the switch itself
    # (and no instance's own URLs above it).
    go(page, "/admin?section=app")
    switch = page.get_by_text("Shift planning", exact=True)
    for _ in range(12):
        if switch.count():
            break
        page.mouse.move(w * 0.65, h * 0.6)
        page.mouse.wheel(0, 500)
        time.sleep(0.8)
    if switch.count():
        switch.last.scroll_into_view_if_needed()
        time.sleep(1)
        page.mouse.move(w * 0.65, h * 0.6)
        page.mouse.wheel(0, 250)
        time.sleep(1.5)
        shot(page, "shot-shifts-admin-switch")
    else:
        missing.append("admin switch")

    go(page, "/shifts")
    shot(page, "shot-shifts-mine")

    go(page, "/shifts/events")
    shot(page, "shot-shifts-events")

    go(page, f"/shifts/events/{FAIR['id']}")
    shot(page, "shot-shifts-event")
    # The first afternoon row (Monday): its sheet with the people on it.
    page.mouse.click(900, 322)
    time.sleep(2.5)
    shot(page, "shot-shifts-sheet")
    close(page)
    if click(page, "Assign", first=True):
        shot(page, "shot-shifts-assign")
        close(page)
    # "More" is an icon button beside "+ Shift" in the page head.
    page.mouse.click(1252, 116)
    time.sleep(2)
    if page.get_by_text("Export shift plan", exact=True).count():
        shot(page, "shot-shifts-event-menu")
        if click(page, "Export shift plan"):
            shot(page, "shot-shifts-export")
        close(page)

    go(page, f"/shifts/events/{PARTY['id']}")
    # Grill (second row) is full: its sheet offers the waiting list.
    page.mouse.click(900, 322)
    time.sleep(2.5)
    shot(page, "shot-shifts-waitlist")
    close(page)

    go(page, f"/shifts/calendar?span=week&date={FAIR_DAY}")
    shot(page, "shot-shifts-calendar-week")
    # Sweep 9:30 to 11:30 on Thursday, which has no morning shift: the editor
    # opens on exactly that time. In English the week starts on Sunday, so at
    # 1440 px Thursday's column is centred at x 1027; 9:30 sits at y 490 and
    # 11:30 at y 593 with the week opened an hour before its first shift.
    x, y0, y1 = 1027, 490, 593
    page.mouse.move(x, y0)
    page.mouse.down()
    for i in range(1, 13):
        page.mouse.move(x, y0 + (y1 - y0) * i / 12)
        time.sleep(0.05)
    page.mouse.up()
    time.sleep(3)
    shot(page, "shot-shifts-calendar-sweep")
    close(page)
    if click(page, "Add", wait=2):
        shot(page, "shot-shifts-calendar-add")
        close(page)

    go(page, f"/shifts/calendar?span=month&date={FAIR_DAY}")
    shot(page, "shot-shifts-calendar-month")

    go(page, "/shifts/events")
    if click(page, "Event", wait=3):
        shot(page, "shot-shifts-event-editor")
        if click(page, "Repeat", exact=False):
            shot(page, "shot-shifts-repeat")
            if click(page, "Custom rule"):
                shot(page, "shot-shifts-repeat-custom")
        close(page)
        close(page)

    go(page, f"/projects/{FAIR['projectId']}/settings")
    click(page, "Shift planning", wait=2)
    shot(page, "shot-shifts-planners")

    go(page, "/settings?section=notifications")
    feed = page.get_by_text("Shifts in your own calendar", exact=True)
    for _ in range(10):
        if feed.count():
            break
        page.mouse.move(w * 0.6, h * 0.55)
        page.mouse.wheel(0, 600)
        time.sleep(0.8)
    if feed.count():
        feed.last.scroll_into_view_if_needed()
        time.sleep(1.5)
    shot(page, "shot-shifts-feed")
    ctx.close()

    # --- phone -----------------------------------------------------------------
    w, h, dpr = PHONE
    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr,
                              color_scheme=theme, locale="en-GB", is_mobile=True, has_touch=True)
    ctx.add_init_script(init_script(theme))
    page = ctx.new_page()
    go(page, "/shifts")
    shot(page, "shot-shifts-mobile-mine")
    go(page, f"/shifts/calendar?span=week&date={FAIR_DAY}")
    shot(page, "shot-shifts-mobile-calendar")
    page.mouse.click(95, 25)
    time.sleep(2)
    shot(page, "shot-shifts-mobile-calendar-menu")
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        run(browser, theme)
    browser.close()

if missing:
    print("missing:", sorted(set(missing)))
    sys.exit(1)
