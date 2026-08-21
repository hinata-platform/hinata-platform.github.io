#!/usr/bin/env python3
"""Capture fresh, English screenshots of the Hinata app for the docs.

Serves the built Flutter web bundle, logs in to the seeded demo backend,
pre-authenticates the app via localStorage, then screenshots each doc-relevant
route at a desktop and (for a few) a mobile viewport. Output PNGs land in the
docs repo's assets/img/ so build.py copies them into the site.

Most of the shots are not a bare route: the user guide is about how the app is
operated, so they are a dialog mid-wizard, an open picker, a filled-in form —
a state only a click reaches. Those live in ACTIONS, one small function per
shot, each of which also hands back the way out (an overlay left open would
land on top of the next picture). Nothing in there ever commits: no Create, no
Save, no Delete, no "Move now" — the demo server is the data every other shot
is taken against.

Every picture is verified before it is published — right pixel size, and not
the near-uniform frame of a canvas that had not painted — and a shot that fails
is left out rather than shipped, with the run printing what it could not get.

Prereqs:
  - a seeded demo server on :8080 (SPRING_PROFILES_ACTIVE=dev HINATA_DEMO_SEED=true)
  - `flutter build web --release` in hinata-app  (build/web must exist)
  - venv with playwright + requests + pillow, and `playwright install chromium`

Besides the per-page shots this seeds what the guide needs and the demo seeder
does not carry: a threaded conversation, four attachments, and a notification
feed produced by the *other* demo accounts (all through the ordinary API). It
also takes the two gate screens — "Connect to your server" and sign-in — in
their own token-less browser contexts, and re-renders the landing page's framed
hero images (frame-macbook.png / frame-iphone.png) via
hinata-app/tool/device_frames.py.

Run:  <venv>/bin/python tools/capture.py
"""
from __future__ import annotations

import argparse
import functools
import http.server
import io
import json
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading
import zipfile

from datetime import date, timedelta

from urllib.parse import urlparse

import requests
from PIL import Image
from playwright.sync_api import sync_playwright

APP_ROOT = "/Users/rebar/Documents/Dev/Hivora/hinata-app"
WEB_DIR = os.path.join(APP_ROOT, "build", "web")
OUT_DIR = "/Users/rebar/Documents/Dev/Hivora/hinata-platform.github.io/assets/img"

API = os.environ.get("HINATA_API", "http://localhost:8080")
WEB_PORT = int(os.environ.get("WEB_PORT", "3000"))
WEB_ORIGIN = f"http://localhost:{WEB_PORT}"
LOGIN = {"identifier": "admin", "password": "hinata-demo-2026"}
HEADLESS = os.environ.get("HEADLESS", "1") != "0"

DESKTOP = (1440, 900, 2)
MOBILE = (390, 844, 3)
# Hero viewports match the device frames' screen cut-outs so the composited
# shot fills them without distortion (see tool/device_frames.py docstring).
HERO_DESKTOP = (1440, 929, 2)   # 16:10.32 — MacBook frame
SETTLE_MS = int(os.environ.get("SETTLE_MS", "7500"))

DEVICE_FRAMES = os.path.join(APP_ROOT, "tool", "device_frames.py")

# The iPhone hero is a REAL simulator screenshot (native status bar + Dynamic
# Island), captured exactly like hinata-app/tool/capture_ios.sh: seed the app's
# sandbox plist (tokens + screenshot_route), simctl launch, simctl screenshot.
# The sim shot (1320×2868) matches the frame's screen cut-out 1:1, so
# device_frames adds NO synthesized status bar. UDID default mirrors
# capture_ios.sh; override with IOS_UDID.
IOS_UDID = os.environ.get("IOS_UDID", "BD91470D-338D-48C6-856B-0821AE6A316B")
IOS_BUNDLE = "com.ahmadre.hinata"
IOS_SETTLE_S = int(os.environ.get("IOS_SETTLE_S", "13"))

# Chromium launch flags for headless SwiftShader rendering of the Flutter web
# canvas (shared by the per-page shots and the framed MacBook hero).
_CHROMIUM_ARGS = [
    "--hide-scrollbars",
    "--force-color-profile=srgb",
    "--enable-unsafe-swiftshader",
    "--use-gl=angle",
    "--use-angle=swiftshader",
]

# Gate/redirect screens the app shows while it is NOT connected + signed in
# (the "Connect to your server" form, the login form, the boot splash, the
# first-run wizard). A screenshot must NEVER land on one of these. The app uses
# clean path URLs and go_router rewrites the address bar on every redirect, so
# we detect a gate purely from the browser URL and refuse to capture it.
GATE_ROUTES = {
    "/connect", "/connecting", "/login", "/setup", "/onboarding", "/update",
}

# Wheel-scroll (px) applied before the screenshot, for below-the-fold content.
SCROLLS = {
    "shot-notification-matrix": 900,
}

# One shot needs a wider window than the rest: the timesheet is a horizontally
# scrolling table, and at 1440 px its week ends on Saturday with the row Total
# off-frame — while the paragraph under the picture is about Sunday and that
# Total. Width, not crop, because the app lays the table out for the width it
# is given.
WIDTHS = {"shot-timesheet": 1780}

# The two screens the signed-in app can never reach, captured in their own
# browser contexts (see capture_gate_shots).
GATE_SHOTS = ("shot-connect-server", "shot-sign-in")

# Issues the guide screenshots by name rather than by position. The seed's ids
# change on every reseed and /issues has no stable first row, while these titles
# are what the seeder itself keys its links, watchers and work items on.
MAIN_ISSUE_TITLE = "Redesign the agile board with calmer column rhythm"
CHAIN_ISSUE_TITLE = "Issue detail: inline edit for estimate & spent"
CONFLICT_ISSUE_TITLE = "Adaptive icon clips on Android 13 themed mode"
# Watched issues other people act on, so the notification feed is a feed.
NOTIFY_ISSUE_TITLES = (
    MAIN_ISSUE_TITLE,
    "Sprint header shows wrong remaining capacity",
    "Blue-green deploy script for the self-host bundle",
)

# The plain-text attachment the viewer shot opens: only a text file puts line
# numbers, wrapping and copy-all in the same frame. Long enough to fill the
# viewer's stage — five lines on a full-screen dark canvas read as a file that
# failed to load, not as a file being shown.
TEXT_ATTACHMENT = "board-drop.log"
DEMO_LOG = """20:14:01.884 board  attach HIN-4 column=in-progress lane=default
20:14:01.902 board  hit-test: card HIN-4 (240x96) under pointer 612,318
20:14:01.941 drag   lift begin  id=HIN-4 from=todo index=3
20:14:02.004 drag   sway 2.1deg  shadow 12 -> 24
20:14:02.118 board  reorder commit id=HIN-4 column=in-progress
20:14:02.119 board  animation key reused for 2 cards - ghost frame
20:14:02.140 render layer tree rebuilt: 3 columns, 41 cards
20:14:02.401 render raster window 16.8ms (budget 16.7ms)
20:14:02.402 render   |- picture  HIN-4 card          4.1ms
20:14:02.403 render   |- backdrop column header blur  9.6ms
20:14:02.404 render   |- picture  drop socket         1.2ms
20:14:02.588 board  auto-scroll edge=right velocity=180px/s
20:14:02.771 board  column in-progress accepts drop (wip 6/8)
20:14:03.010 drag   landing begin id=HIN-4 target=in-progress index=0
20:14:03.244 render raster window 11.2ms
20:14:03.902 board  drop committed, ghost cleared after 1 frame
20:14:03.905 api    PATCH /api/v1/issues/HIN-4 {state: In Progress}
20:14:04.117 sync   SSE issue.updated HIN-4 rev 41
20:14:04.118 board  applying remote rev 41 (local rev 41) - no-op
20:14:04.302 board  column totals recomputed: todo 12, doing 6, done 5
20:14:04.510 render raster window 9.4ms
20:14:05.006 board  idle - 0 pending mutations
20:14:11.442 sync   SSE heartbeat
20:14:22.115 board  filter changed: assignee=lena
20:14:22.140 board  visible cards 41 -> 9
20:14:22.418 render raster window 12.9ms
20:14:26.883 board  filter cleared
20:14:27.004 board  visible cards 9 -> 41
20:14:41.512 sync   SSE heartbeat
20:14:58.220 board  detach HIN-4 - view disposed
"""

# A second saved server for the multi-server shots. Deliberately a host that
# does not answer: it probes as offline, which is honest and still shows the
# reachability check the manager runs on every row.
SECOND_SERVER = {"url": "https://track.example.org", "label": "Acme"}

# What the demo server's identity provider is called for the sign-in shot. The
# seeded one is named in German, and a German button on an English page reads
# as a bug rather than as configuration.
SSO_DEMO_NAME = "Acme Cloud"

# What to type into the ⌘K palette for shot-search. Short enough to look like
# something a person actually typed, broad enough that the seeded demo answers
# it across several result groups.
SEARCH_QUERY = os.environ.get("SEARCH_QUERY", "board")

# The description of the shot issue. The seeder leaves every issue's body empty,
# and eight of the guide's pictures are of exactly that issue — with the guide
# claiming, twice, that the description "renders in full: headings, lists, a code
# block, a quote and a table". Written as markdown because the API converts it
# (LexicalJson is a storage format, markdown is the input one), and kept short
# because on a phone the Sub-tasks card has to stay in the same frame.
MAIN_ISSUE_DESCRIPTION = """### What "calmer" means

- **Gutter** — one spacing token, no per-column overrides.
- **Card height** — capped, the overflow row folded behind its counter.
- **Header** — sticky, and never re-laid-out mid-drag.

```dart
const columnGutter = 12.0; // was 8, 10 and 16, depending on the view
```

| Breakpoint | Columns | Card |
| --- | --- | --- |
| 1280 px and up | 4 | full meta row |
| below 768 px | 1 | key and title only |

> Agreed with design on 12 August: the board is read far more often than it is
> dragged, so the resting state wins every trade-off.
"""

# Threaded demo conversation seeded (idempotently) on the shot issue, so the
# comments screenshot shows a realistic root comment + reply thread.
DEMO_THREAD = (
    "Has anyone re-tested drag-and-drop ordering since the board refactor? "
    "On Safari the dragged card leaves a ghost behind for one frame after the drop.",
    [
        "@admin Reproduced on Safari — looks like the reorder animation racing "
        "the drop commit. I'll attach a trace from the dev panel.",
        "Good catch. Scoping the card animation key to the issue id should fix "
        "it; pushing a patch to the sprint branch today.",
        "Patch is up and verified on Safari and Firefox — the ghost frame is gone.",
    ],
)


def login():
    r = requests.post(f"{API}/api/v1/auth/login", json=LOGIN, timeout=15)
    r.raise_for_status()
    d = r.json()
    return d["accessToken"], d["refreshToken"]


def current_route(page):
    """The app's current route, from the (clean-path) browser URL."""
    return urlparse(page.url).path.rstrip("/") or "/"


def ensure_connected(page, label, timeout_ms=25000):
    """Block until the app is PAST every gate screen — i.e. the server URL is
    connected and the user is signed in — then return the live route.

    Raises if the app stays on /connect, /login, /connecting, … so we never
    save a screenshot of the "Connect to your server" / login screen. When this
    fires, the fix is upstream (start the seeded demo server on the API URL, and
    make sure WEB_ORIGIN is in HINATA_CORS_ALLOWED_ORIGINS) — not shipping the
    broken shot."""
    waited, step = 0, 500
    while waited < timeout_ms:
        route = current_route(page)
        if route not in GATE_ROUTES:
            return route
        page.wait_for_timeout(step)
        waited += step
    raise RuntimeError(
        f"{label}: app is still on the gate screen {current_route(page)!r} "
        f"after {timeout_ms} ms — the connect URL is not connected / no session. "
        f"Is the seeded demo server up on {API}, and is {WEB_ORIGIN} listed in "
        f"HINATA_CORS_ALLOWED_ORIGINS? Refusing to capture a connect/login shot."
    )


def first_board_id(access):
    r = requests.get(f"{API}/api/v1/boards",
                     headers={"Authorization": f"Bearer {access}"}, timeout=15)
    r.raise_for_status()
    data = r.json()
    data = data if isinstance(data, list) else data.get("content", [])
    return data[0]["id"]


def first_id(access, path):
    """The id of the first entry of a collection endpoint, or None.

    The user guide screenshots a project, a team and a knowledge article by id,
    and the demo seed's ids change on every reseed — so they are looked up
    rather than pinned. Returns None instead of raising: a missing collection
    should cost one screenshot, not the whole run.
    """
    try:
        r = requests.get(f"{API}/api/v1/{path}",
                         headers={"Authorization": f"Bearer {access}"}, timeout=15)
        r.raise_for_status()
        data = r.json()
        data = data if isinstance(data, list) else data.get("content", [])
        return data[0]["id"] if data else None
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return None


def an_issue_id(access):
    r = requests.get(f"{API}/api/v1/issues?size=60",
                     headers={"Authorization": f"Bearer {access}"}, timeout=15)
    r.raise_for_status()
    data = r.json()
    data = data if isinstance(data, list) else data.get("content", [])
    # prefer one with a description and comments for a richer detail view
    ranked = sorted(
        data,
        key=lambda i: (bool(i.get("description")), i.get("commentCount") or 0),
        reverse=True,
    )
    return (ranked or data)[0]["id"] if data else None


def enable_semantics(page):
    """Turn on Flutter web's semantics tree so canvas widgets become queryable
    DOM nodes (role + aria-label). Flutter ships a hidden "Enable accessibility"
    placeholder; activating it flips the tree on. Returns True once the tree is
    up — including when an earlier shot in the same context already turned it
    on, which is why the placeholder being gone is a success, not a failure."""
    try:
        ph = page.locator(
            "flt-semantics-placeholder, [aria-label='Enable accessibility']"
        )
        if not ph.count():
            return page.locator("flt-semantics").count() > 0
        if ph.count():
            ph.first.dispatch_event("click")
            page.wait_for_timeout(700)
            return True
    except Exception as e:
        print(f"    (semantics enable failed: {e})")
    return False


def expand_reply_threads(page, max_threads=4):
    """Open every collapsed "N replies" thread so the comments screenshot shows
    the expanded thread, not just the collapsed affordance. The toggle's
    accessible label is the i18n "N replies"/"N reply", so we match a digit
    followed by 'repl' — which never hits the bare 'Reply' composer action."""
    if not enable_semantics(page):
        return 0
    opened = 0
    label = re.compile(r"\d+\s+repl", re.I)
    for _ in range(max_threads):
        toggle = page.get_by_role("button", name=label)
        if not toggle.count():
            break
        try:
            toggle.first.click(timeout=2500)
            opened += 1
            page.wait_for_timeout(2600)   # let the reply page load over the API
        except Exception:
            break
    if opened:
        print(f"    ↳ expanded {opened} reply thread(s)")
    return opened


def seed_demo_thread(access, issue_id):
    """Idempotently seed the DEMO_THREAD conversation on the shot issue."""
    h = {"Authorization": f"Bearer {access}"}
    base = f"{API}/api/v1/issues/{issue_id}/comments"
    root_text, replies = DEMO_THREAD
    r = requests.get(f"{base}?size=100", headers=h, timeout=15)
    r.raise_for_status()
    data = r.json()
    data = data if isinstance(data, list) else data.get("content", [])
    if any(c.get("text") == root_text for c in data):
        print(f"demo thread already present on issue {issue_id}")
        return
    root = requests.post(base, headers=h, timeout=15,
                         json={"text": root_text})
    root.raise_for_status()
    root_id = root.json()["id"]
    for text in replies:
        requests.post(base, headers=h, timeout=15,
                      json={"text": text, "replyToId": root_id}).raise_for_status()
    print(f"seeded demo thread ({1 + len(replies)} comments) on issue {issue_id}")


def seed_issue_description(access, issue_id):
    """Give the shot issue the body the guide describes. Idempotent."""
    h = {"Authorization": f"Bearer {access}"}
    url = f"{API}/api/v1/issues/{issue_id}"
    current = requests.get(url, headers=h, timeout=15)
    current.raise_for_status()
    if "columnGutter" in (current.json().get("description") or ""):
        print(f"issue {issue_id} already carries its description")
        return
    requests.patch(url, headers=h, timeout=20,
                   json={"description": MAIN_ISSUE_DESCRIPTION}).raise_for_status()
    print(f"seeded the description on issue {issue_id}")


def seed_work_entries(access, issue_id):
    """Fill the issue's Timeline card, which lists the eight newest entries and
    is captioned as doing exactly that. Several people, several activity types
    and several days, because a list of eight identical rows would prove nothing
    the sentence next to it claims. Idempotent: it tops the list up to eight."""
    h = {"Authorization": f"Bearer {access}"}
    base = f"{API}/api/v1/issues/{issue_id}/work-items"
    have = requests.get(base, headers=h, timeout=15)
    have.raise_for_status()
    existing = have.json()
    if len(existing) >= 8:
        print(f"work log already full ({len(existing)} entries)")
        return
    today = date.today()
    # (who, minutes, activity, days back, note)
    # Every activity here has to be one of the six the Log-time sheet offers
    # (work_log_sheet.dart), because the guide's own text next to this shot says
    # the six are the entire vocabulary. The field accepts any string, so a
    # seventh would be written, stored and photographed — an activity the guide
    # shows one paragraph above the picker that does not contain it.
    entries = [
        ("mei", 45, "Testing", 0, "Column rhythm pass on Safari and Firefox."),
        ("lena", 90, "Design", 1, "Spacing tokens for the three breakpoints."),
        ("tomas", 60, "Development", 1, "Reworked the column header after review."),
        ("admin", 30, "Meeting", 2, "Design sync on the resting state."),
        ("amara", 120, "Development", 3, "Folded the card meta row behind its counter."),
        ("mei", 75, "Documentation", 4, "Wrote up the breakpoint table."),
    ]
    for who, minutes, activity, back, note in entries:
        if len(existing) + 1 > 8:
            break
        token = access if who == "admin" else login_as(who)
        requests.post(base, headers={"Authorization": f"Bearer {token}"}, timeout=15,
                      json={"durationMinutes": minutes,
                            "date": (today - timedelta(days=back)).isoformat(),
                            "activityType": activity,
                            "description": note}).raise_for_status()
        existing.append(None)
    # The card prints "spent of estimate", and eight entries against the seed's
    # four-hour estimate would read as a runaway rather than as a work log. The
    # estimate is raised to the next whole hour above what has been logged.
    logged = requests.get(base, headers=h, timeout=15).json()
    spent = sum(item["durationMinutes"] for item in logged)
    requests.patch(f"{API}/api/v1/issues/{issue_id}", headers=h, timeout=20,
                   json={"estimateMinutes": -(-spent // 60) * 60}).raise_for_status()
    print(f"seeded work entries up to {len(existing)} on issue {issue_id}")


def seed_next_sprint(access, board_id):
    """Plan the sprint after the running one.

    The Complete-sprint dialog exists to choose where unfinished work goes, and
    with a single sprint on the board that choice is a list of one. Created but
    not started, which is what "planned" means here. Idempotent."""
    h = {"Authorization": f"Bearer {access}"}
    listed = requests.get(f"{API}/api/v1/sprints", headers=h, timeout=15,
                          params={"boardId": board_id})
    listed.raise_for_status()
    sprints = listed.json()
    if len(sprints) > 1:
        print(f"board already has {len(sprints)} sprints")
        return
    if not sprints:
        return
    running = sprints[0]
    end = running.get("endDate")
    start = date.fromisoformat(end) + timedelta(days=1) if end else date.today()
    number = int(re.findall(r"\d+", running.get("name") or "24")[-1]) + 1
    requests.post(f"{API}/api/v1/sprints", headers=h, timeout=20, json={
        "boardId": board_id,
        "name": f"Sprint {number}",
        "goal": "Ship the calmer board to everyone and clear the drag backlog.",
        "startDate": start.isoformat(),
        "endDate": (start + timedelta(days=13)).isoformat(),
        "capacityPoints": 40,
    }).raise_for_status()
    print(f"planned Sprint {number} after {running.get('name')}")


def seed_team_activity(access, team_id):
    """Give the team overview the feed its caption promises.

    Only team operations write that feed, so these are real ones, performed
    through the ordinary API and left standing: the team gains a fourth member,
    that member is made a Team-Admin, and the team's description is rewritten.
    Idempotent: it runs only while the feed is empty."""
    h = {"Authorization": f"Bearer {access}"}
    feed = requests.get(f"{API}/api/v1/teams/{team_id}/activity", headers=h,
                        timeout=15, params={"size": 5})
    feed.raise_for_status()
    body = feed.json()
    rows = body if isinstance(body, list) else body.get("content", [])
    if rows:
        print(f"team activity already seeded ({len(rows)} entries)")
        return
    team = requests.get(f"{API}/api/v1/teams/{team_id}", headers=h, timeout=15)
    team.raise_for_status()
    detail = team.json()
    members = {m.get("userId") or m.get("id") for m in (detail.get("members") or [])}
    directory = requests.get(f"{API}/api/v1/users", headers=h, timeout=15).json()
    joiner = next((u for u in directory if u["id"] not in members
                   and u["username"] != "admin"), None)
    if joiner is None:
        print("no one left to add to the team — feed stays empty")
        return
    requests.post(f"{API}/api/v1/teams/{team_id}/members", headers=h, timeout=20,
                  json={"userIds": [joiner["id"]], "role": "MEMBER",
                        "access": {"scope": "ALL"}}).raise_for_status()
    requests.patch(f"{API}/api/v1/teams/{team_id}/members/{joiner['id']}",
                   headers=h, timeout=20,
                   json={"role": "ADMIN"}).raise_for_status()
    requests.patch(f"{API}/api/v1/teams/{team_id}", headers=h, timeout=20, json={
        "description": "Owns the board, the editor and everything under /api/v1.",
    }).raise_for_status()
    print(f"seeded team activity (added + promoted {joiner['displayName']}, "
          f"rewrote the description)")


def seed_comment_reactions(access, issue_id):
    """Put reactions on the thread. A page section named "React to a comment"
    next to a thread carrying none is the sort of gap a reader notices before
    the prose. One per person per comment is the product's rule, so these are
    four different people. Idempotent."""
    h = {"Authorization": f"Bearer {access}"}
    base = f"{API}/api/v1/issues/{issue_id}/comments"
    listed = requests.get(f"{base}?size=100", headers=h, timeout=15)
    listed.raise_for_status()
    body = listed.json()
    comments = body if isinstance(body, list) else body.get("content", [])
    if any(c.get("reactions") for c in comments):
        print("comment reactions already seeded")
        return
    if not comments:
        return
    # The root of the seeded thread and, when it is loaded, the reply that
    # closes it — a "verified, it's gone" is what a 👍 is actually for.
    root_text, replies = DEMO_THREAD
    root = next((c for c in comments if c.get("text") == root_text), comments[0])
    thread = requests.get(f"{base}/{root['id']}/replies?size=20", headers=h, timeout=15)
    page = thread.json() if thread.ok else {}
    loaded = page if isinstance(page, list) else page.get("content", [])
    closing = next((c for c in loaded if c.get("text") == replies[-1]), None)
    targets = [(root, "👍")] + ([(closing, "🎉")] if closing else [])
    for comment, emoji in targets:
        for who in ("lena", "mei", "tomas"):
            requests.put(f"{base}/{comment['id']}/reactions", timeout=15,
                         headers={"Authorization": f"Bearer {login_as(who)}"},
                         json={"emoji": emoji}).raise_for_status()
    print(f"seeded reactions on {len(targets)} comment(s)")


def frame_heroes(browser, seed):
    """MacBook hero: web capture at the frame's screen aspect, composited into
    the landing-page device frame via tool/device_frames.py (subprocess, so
    the only extra dep here is Pillow in this venv)."""
    device, (w, h, dpr), route, out_name = (
        "macbook", HERO_DESKTOP, "/dashboard", "frame-macbook.png")
    with tempfile.TemporaryDirectory(prefix="hinata-hero-") as tmp:
        ctx = browser.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=dpr,
            color_scheme="dark",
            locale="en-GB",
            base_url=WEB_ORIGIN,
        )
        ctx.add_init_script(seed)
        page = ctx.new_page()
        page.goto(f"{WEB_ORIGIN}{route}", wait_until="domcontentloaded")
        page.wait_for_timeout(SETTLE_MS + 3000)
        # Never composite the connect/login screen into the hero frame.
        ensure_connected(page, f"hero-{device}")
        raw = os.path.join(tmp, f"hero-{device}.png")
        page.screenshot(path=raw)
        ctx.close()
        out = os.path.join(OUT_DIR, out_name)
        subprocess.run([sys.executable, DEVICE_FRAMES, device, raw, out],
                       check=True)
        print(f"  ✓ {out_name:24} {w}x{h}@{dpr} {route} (framed)")


def _sim(*args, **kw):
    return subprocess.run(["xcrun", "simctl", *args], capture_output=True,
                          text=True, **kw)


def iphone_hero_from_simulator(access, refresh):
    """iPhone hero from a REAL iPhone simulator screenshot — native status bar
    and Dynamic Island, no synthesized chrome. Same mechanics as
    hinata-app/tool/capture_ios.sh: seed the app sandbox plist with the server
    URL + tokens + screenshot_route, launch, screenshot, then frame it.

    Requires: the simulator booted (open -a Simulator) and the Hinata app
    installed on it. Fails loudly otherwise — we never fake this shot."""
    import glob
    import plistlib
    import time

    if _sim("list", "devices", "booted").stdout.find(IOS_UDID) < 0:
        raise RuntimeError(
            f"iPhone simulator {IOS_UDID} is not booted. Boot it (open -a "
            f"Simulator), install the app, or set IOS_UDID to a booted device "
            f"with {IOS_BUNDLE} installed."
        )
    plists = glob.glob(os.path.expanduser(
        f"~/Library/Developer/CoreSimulator/Devices/{IOS_UDID}/data/Containers"
        f"/Data/Application/*/Library/Preferences/{IOS_BUNDLE}.plist"))
    if not plists:
        raise RuntimeError(
            f"{IOS_BUNDLE} is not installed on simulator {IOS_UDID} — build & "
            f"install it first (flutter run -d <sim> or xcodebuild)."
        )
    pl = plists[0]

    _sim("terminate", IOS_UDID, IOS_BUNDLE)
    _sim("spawn", IOS_UDID, "launchctl", "stop",
         "com.apple.cfprefsd.xpc.daemon")
    time.sleep(1)
    try:
        with open(pl, "rb") as f:
            prefs = plistlib.load(f)
    except Exception:
        prefs = {}
    prefs.update({
        "flutter.server_url": API,
        "flutter.access_token": access,
        "flutter.refresh_token": refresh,
        "flutter.onboarding_done": True,
        "flutter.locale": "en",
        "flutter.screenshot_route": "/dashboard",
    })
    with open(pl, "wb") as f:
        plistlib.dump(prefs, f, fmt=plistlib.FMT_BINARY)

    r = _sim("launch", IOS_UDID, IOS_BUNDLE)
    if r.returncode != 0:
        raise RuntimeError(f"simctl launch failed: {r.stderr.strip()}")
    time.sleep(IOS_SETTLE_S)
    with tempfile.TemporaryDirectory(prefix="hinata-hero-ios-") as tmp:
        raw = os.path.join(tmp, "hero-iphone.png")
        r = _sim("io", IOS_UDID, "screenshot", "--type=png", raw)
        if r.returncode != 0:
            raise RuntimeError(f"simctl screenshot failed: {r.stderr.strip()}")
        out = os.path.join(OUT_DIR, "frame-iphone.png")
        subprocess.run([sys.executable, DEVICE_FRAMES, "iphone", raw, out],
                       check=True)
    _sim("terminate", IOS_UDID, IOS_BUNDLE)
    print(f"  ✓ {'frame-iphone.png':24} simulator {IOS_UDID[:8]}… /dashboard (framed, native)")


def goto_route(page, route, settle=None):
    """Drive go_router through the History API. The app boots through an
    auth/connect redirect that always lands on /dashboard, so an initial deep
    link is lost; pushState keeps the authenticated session and really routes."""
    page.evaluate(
        "(r) => { window.history.pushState(null, '', r);"
        " window.dispatchEvent(new PopStateEvent('popstate', {state: null})); }",
        route,
    )
    page.wait_for_timeout(SETTLE_MS if settle is None else settle)


def reload_app(page):
    """Boot the app again. The cheapest way out of a state that has no cancel —
    a filled-in New issue dialog, dashboard edit mode — and never a save: the
    draft only ever lived in the tab that is being thrown away."""
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(SETTLE_MS + 1500)
    ensure_connected(page, "reload")
    enable_semantics(page)


def add_saved_server(page):
    """Give this browser profile a second saved server and reload into it.

    A manager sheet with one row says nothing about a section on running several
    servers. The second profile is unreachable and probes as offline, which is
    honest and still shows the reachability check the prose describes.

    Timing matters: AppStorage migrates the legacy token into per-server storage
    only while the server list is still absent, so this must run *after* boot —
    seeding the list up front would sign the app out."""
    added = page.evaluate(
        """(extra) => {
          const key = 'flutter.servers.v1';
          let list = [];
          try { list = JSON.parse(JSON.parse(localStorage.getItem(key) || '"[]"')); }
          catch (e) { list = []; }
          if (!Array.isArray(list) || !list.length) return false;
          if (list.some((s) => s.url === extra.url)) return true;
          list.push(extra);
          localStorage.setItem(key, JSON.stringify(JSON.stringify(list)));
          return true;
        }""",
        SECOND_SERVER,
    )
    if not added:
        print("    (no saved-server list yet — manager stays single-row)")
        return
    reload_app(page)


def leave_editor(page):
    """Leave the knowledge editor without publishing. Cancel is the editor's own
    way out; a draft-discard confirm may stand behind it."""
    click_if(page, "Cancel")
    click_if(page, "Discard")
    page.keyboard.press("Escape")
    page.wait_for_timeout(600)


def clear_composer(page):
    """Empty the comment composer again. A half-typed mention left in it would
    ride along into the next shot of the same issue."""
    try:
        page.keyboard.press("Control+a")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(400)
    except Exception:
        pass


def verify_png(path, expect):
    """Refuse a picture the app had not painted.

    A shot is only shipped when the file is there, has the viewport's pixel size
    and actually carries an image: a near-uniform frame is the canvas before
    first paint, or a screen the route never reached. Returns (ok, note)."""
    if not os.path.exists(path) or os.path.getsize(path) < 8000:
        return False, "missing or truncated file"
    with Image.open(path) as im:
        size = im.size
        if size != expect:
            return False, f"{size[0]}x{size[1]}, expected {expect[0]}x{expect[1]}"
        small = im.convert("RGB").resize((64, 64))
    colors = small.getcolors(maxcolors=4096) or []
    channels = [value for _, pixel in colors for value in pixel]
    span = max(channels) - min(channels) if channels else 0
    if span < 24 or len(colors) < 12:
        return False, f"near-uniform image (span {span}, {len(colors)} colours)"
    return True, f"{size[0]}x{size[1]}"


# --- demo data the guide needs -----------------------------------------------

def login_as(username):
    """A token for one of the seeded demo people. They share the admin password,
    which is what lets the capture produce notifications that come from someone
    else — the only kind the notification centre is about."""
    r = requests.post(f"{API}/api/v1/auth/login", timeout=15,
                      json={"identifier": username, "password": LOGIN["password"]})
    r.raise_for_status()
    return r.json()["accessToken"]


def prune_own_sessions(access):
    """Sign the *other* sessions of the demo account out.

    Every capture run logs in again, and the account page prints one row per
    live session — after a few runs it reads "45 signed-in devices, Unknown ·
    Browser" and pushes the cards below it off the screen. Only this account's
    own sessions are touched, and only the ones this run is not using."""
    r = requests.post(f"{API}/api/v1/me/sessions/revoke-others",
                      headers={"Authorization": f"Bearer {access}"}, timeout=15)
    if r.ok:
        print("signed out the demo account's other sessions")


def non_member(access, team_id):
    """Someone in the directory who is not on this team, by display name — the
    only person the Add-members picker can still offer."""
    h = {"Authorization": f"Bearer {access}"}
    team = requests.get(f"{API}/api/v1/teams/{team_id}", headers=h, timeout=15)
    team.raise_for_status()
    on_team = {m.get("userId") for m in (team.json().get("members") or [])}
    directory = requests.get(f"{API}/api/v1/users", headers=h, timeout=15).json()
    for user in directory:
        if user["id"] not in on_team and user["username"] != "admin":
            return user["displayName"]
    return None


def issue_by_title(access, title):
    """The seeded issue with this title, or None. Titles rather than ids or list
    positions: the ids change on every reseed and the first row of /issues is
    not stable between calls, while the seeder keys its links, watchers and work
    items on exactly these titles."""
    r = requests.get(f"{API}/api/v1/issues?size=200",
                     headers={"Authorization": f"Bearer {access}"}, timeout=20)
    r.raise_for_status()
    data = r.json()
    data = data if isinstance(data, list) else data.get("content", [])
    for issue in data:
        if issue.get("title") == title:
            return issue
    return None


def estimate_candidates(access, project_id):
    """Rows that already carry a story-point estimate, for the planning-poker
    shot. Several, because only the rows above the fold can be clicked and which
    those are depends on how many issues the sprint holds — the shot walks the
    list until it finds one the planning view is actually showing."""
    r = requests.get(f"{API}/api/v1/issues?size=200&projectId={project_id}",
                     headers={"Authorization": f"Bearer {access}"}, timeout=20)
    r.raise_for_status()
    data = r.json()
    data = data if isinstance(data, list) else data.get("content", [])
    rows = [i for i in data if i.get("storyPoints")]
    # The sprint section is rendered above the backlog, so its rows are the
    # likeliest to be above the fold; the backlog runs newest-first below it.
    rows.sort(key=lambda i: (not i.get("sprintId"), -(i.get("numberInProject") or 0)))
    return [(i["readableId"], i["storyPoints"]) for i in rows]


def seed_demo_attachments(access, issue_id):
    """Put four real files on the shot issue: two that get a thumbnail and two
    that fall back to a colour-coded glyph tile, so the attachments grid shows
    what the section describes instead of an empty drop zone. Idempotent."""
    h = {"Authorization": f"Bearer {access}"}
    base = f"{API}/api/v1/issues/{issue_id}/attachments"
    detail = requests.get(f"{API}/api/v1/issues/{issue_id}", headers=h, timeout=15)
    detail.raise_for_status()
    have = {a.get("fileName") for a in (detail.json().get("attachments") or [])}
    log = DEMO_LOG.encode()
    zipped = io.BytesIO()
    with zipfile.ZipFile(zipped, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("safari-trace/board-drop.log", log.decode())
    pdf = (
        b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Resources<</Font<</F1 4 0 R>>>>"
        b"/Contents 5 0 R>>endobj\n"
        b"4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n"
        b"5 0 obj<</Length 78>>stream\nBT /F1 18 Tf 64 760 Td (Board rhythm - review notes) Tj ET\n"
        b"endstream endobj\ntrailer<</Root 1 0 R>>\n"
    )
    shot = os.path.join(OUT_DIR, "shot-board.png")
    files = [
        ("board-columns-before.png", open(shot, "rb").read() if os.path.exists(shot) else None,
         "image/png"),
        ("review-notes.pdf", pdf, "application/pdf"),
        ("board-drop.log", log, "text/plain"),
        ("safari-trace.zip", zipped.getvalue(), "application/zip"),
    ]
    # The log is the file the viewer screenshot opens, and it is the length of
    # the log that decides whether that picture reads as a viewer or as a failed
    # load. An older, shorter one is replaced rather than kept.
    for existing in (detail.json().get("attachments") or []):
        if existing.get("fileName") == TEXT_ATTACHMENT and \
                (existing.get("size") or 0) < len(log) - 32:
            requests.delete(f"{base}/{existing['id']}", headers=h, timeout=30)
            have.discard(TEXT_ATTACHMENT)
            print(f"replaced the stale {TEXT_ATTACHMENT}")
    added = 0
    for name, blob, mime in files:
        if blob is None or name in have:
            continue
        r = requests.post(base, headers=h, timeout=60,
                          files={"file": (name, blob, mime)})
        r.raise_for_status()
        added += 1
    if added:
        print(f"seeded {added} attachment(s) on issue {issue_id}")


def seed_demo_notifications(access, issues):
    """Make the notification centre show a feed rather than a lone sign-in alert.

    Everything here is produced through the ordinary API by *other* demo people
    — a mention, two comments on watched issues, an assignment and a status
    change — because a notification is by definition something somebody else
    did. Idempotent: it only runs while the feed is still nearly empty."""
    h = {"Authorization": f"Bearer {access}"}
    feed = requests.get(f"{API}/api/v1/notifications?size=20", headers=h, timeout=15)
    feed.raise_for_status()
    data = feed.json()
    data = data if isinstance(data, list) else data.get("content", [])
    if len(data) >= 5:
        print(f"notification feed already seeded ({len(data)} entries)")
        return
    me = requests.get(f"{API}/api/v1/me", headers=h, timeout=15).json()
    main, other, third = issues
    lena, mei, tomas = login_as("lena"), login_as("mei"), login_as("tomas")

    def post(token, issue_id, payload):
        requests.post(f"{API}/api/v1/issues/{issue_id}/comments",
                      headers={"Authorization": f"Bearer {token}"},
                      json=payload, timeout=15).raise_for_status()

    # A mention is a smartlink node, not an "@name" in the text — that is what
    # the notification layer looks for, and what renders as a chip.
    mention_doc = json.dumps({"root": {"type": "root", "version": 1, "format": "",
        "indent": 0, "direction": "ltr", "children": [{"type": "paragraph",
        "version": 1, "format": "", "indent": 0, "direction": "ltr", "children": [
            {"type": "smartlink", "version": 1, "kind": "user",
             "label": me.get("displayName") or me.get("username"), "targetId": me["id"]},
            {"type": "text", "version": 1, "detail": 0, "format": 0, "mode": "normal",
             "style": "", "text": " the calmer column rhythm is on staging — can you "
                                  "sign off on the spacing before we ship it?"}]}]}})
    post(mei, main["id"], {"textDoc": mention_doc})
    post(lena, main["id"], {"text": "Re-tested on Safari and Firefox after the patch — "
                                    "the ghost frame is gone on both."})
    post(tomas, other["id"], {"text": "Capacity is computed from the sprint's committed "
                                      "points now, so the header stops disagreeing with "
                                      "the burndown."})
    # An assignment and a status change: two more kinds, each with its own glyph
    # in the centre.
    requests.patch(f"{API}/api/v1/issues/{third['id']}",
                   headers={"Authorization": f"Bearer {tomas}"},
                   json={"assigneeId": me["id"]}, timeout=15).raise_for_status()
    requests.patch(f"{API}/api/v1/issues/{other['id']}",
                   headers={"Authorization": f"Bearer {lena}"},
                   json={"state": "In Review"}, timeout=15).raise_for_status()
    print("seeded notification feed (mention, comments, assignment, status change)")


def english_sso_name(access):
    """Rename the demo identity provider for the sign-in shot, and hand back the
    undo. The seeded server's provider is called "Mit AStA Cloud fortfahren" —
    a German string on an English page reads as a bug, and the button is
    rendered from whatever the server calls its provider."""
    h = {"Authorization": f"Bearer {access}"}
    settings = requests.get(f"{API}/api/v1/admin/settings", headers=h, timeout=15)
    settings.raise_for_status()
    body = settings.json()
    original = body.get("oidc", {}).get("displayName")
    if original is None or original == SSO_DEMO_NAME:
        return lambda: None
    body["oidc"]["displayName"] = SSO_DEMO_NAME
    requests.put(f"{API}/api/v1/admin/settings", headers=h, json=body,
                 timeout=20).raise_for_status()

    def restore():
        # A full run takes longer than an access token lives, so this signs in
        # again rather than reusing the one from half an hour ago.
        fresh = {"Authorization": f"Bearer {login()[0]}"}
        body["oidc"]["displayName"] = original
        requests.put(f"{API}/api/v1/admin/settings", headers=fresh, json=body,
                     timeout=20).raise_for_status()
    return restore


# =============================================================================
# Interaction toolkit
#
# Flutter paints to a canvas, so every control below is addressed through the
# semantics tree (enable_semantics). Two shapes recur and are worth naming:
# a control whose accessible name is its Semantics label *and* its visible Text
# concatenated ("Customize\nCustomize"), which only a regex matches; and a text
# field, which Flutter materialises as an <input> only while it is focused —
# until then it is reachable through the label painted above it, not by
# get_by_label.
# =============================================================================


def tap(page, name, *, exact=True, nth=0, after=2000, role="button", timeout=9000):
    """Click a control by its accessible name, then let the UI settle."""
    page.get_by_role(role, name=name, exact=exact).nth(nth).click(timeout=timeout)
    page.wait_for_timeout(after)


def tap_re(page, pattern, *, nth=0, after=2000, timeout=9000):
    """Click by regex — for the label+Text names an exact match never hits."""
    page.get_by_role("button", name=re.compile(pattern)).nth(nth).click(timeout=timeout)
    page.wait_for_timeout(after)


def tap_text(page, text, *, exact=True, nth=0, after=2000, timeout=9000):
    """Click a text node. Rows that are a bare GestureDetector (a board card, a
    tree row) expose their label as text without a button role."""
    page.get_by_text(text, exact=exact).nth(nth).click(timeout=timeout)
    page.wait_for_timeout(after)


def tap_row(page, text, *, nth=0, after=1500, timeout=9000):
    """Click a list row by text it contains. A row carries every line of its
    content in one accessible name ("AO\nAmara Okafor\nFrontend Engineer"), so
    an exact name never matches and the inner text is not a node of its own."""
    page.get_by_role("button", name=re.compile(re.escape(text))).nth(nth).click(timeout=timeout)
    page.wait_for_timeout(after)


def box_of(locator, what):
    box = locator.bounding_box()
    if not box:
        raise RuntimeError(f"{what}: no bounding box — the control is not on screen")
    return box


def tap_box(page, locator, *, fx=0.5, fy=0.5, dx=0, dy=0, after=1500, what="target"):
    """Click inside a control's box at a fraction of its size (plus an optional
    pixel offset). For tap targets with no semantics node of their own — a
    column's dotted "Add issue" row, a backlog row's checkbox — and for rows
    that hide a second control at their centre (the date row's clear ×)."""
    box = box_of(locator, what)
    page.mouse.click(box["x"] + box["width"] * fx + dx,
                     box["y"] + box["height"] * fy + dy)
    page.wait_for_timeout(after)


def fill(page, label, text, *, delay=60, after=900, exact=True, clear=False):
    """Type into the field with this accessible name. Flutter exposes a field
    that carries a hint (or has focus) as a real <input>/<textarea>, which is
    addressable; a field that is neither has to be clicked by geometry.

    `clear` first selects what is already in the field — a field that starts at
    "0" otherwise reads "030" after typing 30, which is the sort of detail a
    screenshot of a form is entirely about."""
    page.get_by_label(label, exact=exact).first.click(timeout=9000)
    page.wait_for_timeout(400)
    if clear:
        page.keyboard.press("ControlOrMeta+a")
        page.wait_for_timeout(200)
    page.keyboard.type(text, delay=delay)
    page.wait_for_timeout(after)


def write(page, text, *, delay=70, after=1000):
    page.keyboard.type(text, delay=delay)
    page.wait_for_timeout(after)


def scroll(page, dy, *, at=None, after=2200):
    """Wheel-scroll the content under the pointer. Flutter renders to canvas, so
    a wheel event over the content is what moves the inner scrollable."""
    size = page.viewport_size
    x, y = at or (size["width"] // 2, size["height"] // 2)
    page.mouse.move(x, y)
    page.mouse.wheel(0, dy)
    page.wait_for_timeout(after)


def taller(page, height=1250):
    """Give one shot a taller window, and hand back the undo.

    The relationship menu is thirteen rows anchored under its dropdown: in a
    900 px window it ships cut off after seven, and a menu with its last rows
    missing is exactly what the picture exists to prevent."""
    was = dict(page.viewport_size)
    page.set_viewport_size({"width": was["width"], "height": height})
    page.wait_for_timeout(1800)
    return lambda: (page.set_viewport_size(was), page.wait_for_timeout(1200))


def wider(page, width=1780):
    """Give one shot a wider window, and hand back the undo.

    The timesheet is a table that scrolls sideways: at 1440 px its week ends on
    Saturday, with Sunday and the row's Total off-frame — and the paragraph
    under the picture is about Sunday and that Total."""
    was = dict(page.viewport_size)
    page.set_viewport_size({"width": width, "height": was["height"]})
    page.wait_for_timeout(2500)
    return lambda: (page.set_viewport_size(was), page.wait_for_timeout(1200))


def scroll_into_view(page, name, *, role="button", exact=True, step=700, tries=8,
                     after=1100):
    """Wheel down until this control is inside the window.

    A fixed scroll distance is a guess about page length, and the pages the
    guide shoots grow with the seed — one more attachment or link moves the
    comment thread half a screen. Playwright cannot scroll a canvas into view
    itself, so the wheel does it a step at a time."""
    return bring_into_view(
        page, lambda: page.get_by_role(role, name=name, exact=exact).first,
        step=step, tries=tries, after=after, what=repr(name))


def bring_into_view(page, find, *, step=700, tries=8, after=1100, what="target"):
    """As scroll_into_view, for a target that is not addressed by role+name."""
    height = page.viewport_size["height"]
    for _ in range(tries):
        target = find()
        box = target.bounding_box() if target.count() else None
        if box and box["y"] > 40 and box["y"] + box["height"] <= height - 8:
            return box
        # Once the target has a position, scroll by exactly what it takes to
        # centre it — a fixed step overshoots on a phone and then oscillates
        # between above the window and below it until the tries run out.
        scroll(page, int(box["y"] - height * 0.45) if box else step, after=after)
    raise RuntimeError(f"{what} never came into view")


def click_if(page, name, *, exact=True, after=1200, role="button", timeout=4000):
    """Click a control when it is there, and shrug when it is not — used by the
    teardowns, where the overlay may already have closed itself."""
    try:
        target = page.get_by_role(role, name=name, exact=exact)
        if target.count():
            target.first.click(timeout=timeout)
            page.wait_for_timeout(after)
            return True
    except Exception:
        pass
    return False


def dismiss_barrier(page, after=900):
    """Close an overlay through the barrier it laid over the app.

    Glass popovers ignore Escape and answer only to their barrier, and the two
    barriers are labelled differently — "Dismiss" for a popover, "Modal barrier"
    for a wolt sheet. Clicked near the top-left corner, because the barrier's
    own centre is usually the overlay sitting on it."""
    for barrier in barriers(page):
        try:
            barrier.first.click(position={"x": 6, "y": 6}, timeout=4000)
            page.wait_for_timeout(after)
            return True
        except Exception:
            continue
    return False


# The two barriers an overlay lays over the app — a glass popover's and a wolt
# sheet's. Both are also what makes a leftover overlay poisonous to the *next*
# shot: they swallow the wheel, so its scroll silently does nothing.
OVERLAY_BARRIER = re.compile(r"^(Dismiss|Modal barrier)$")


def barriers(page):
    """Every barrier currently over the app. A popover's carries an aria-label,
    a wolt sheet's only its text, so both spellings have to be asked for."""
    found = []
    for query in (lambda: page.get_by_label(OVERLAY_BARRIER),
                  lambda: page.get_by_role("button", name=OVERLAY_BARRIER)):
        try:
            hit = query()
            if hit.count():
                found.append(hit)
        except Exception:
            continue
    return found


def overlay_open(page):
    return bool(barriers(page))


def clear_overlays(page, tries=3):
    """Make sure a shot starts on a bare screen, and say whether it does."""
    for _ in range(tries):
        if not overlay_open(page):
            return True
        dismiss(page)
    return not overlay_open(page)


def dismiss(page, *buttons, barrier=True, escape=True):
    """Close whatever a shot opened, in the order the app answers to: the named
    button (dialogs and wizards), then the barrier (glass popovers), then
    Escape (sheets). Overlays survive the pushState navigation between shots, so
    an unclosed one would land on top of the next picture."""
    for label in buttons:
        click_if(page, label)
    if barrier:
        dismiss_barrier(page)
    if escape:
        page.keyboard.press("Escape")
        page.wait_for_timeout(700)
    # A "Discard this draft?" confirm can stand between a filled-in dialog and
    # its close — leaving the draft is exactly what we want.
    for label in ("Discard", "Discard draft", "Leave"):
        if click_if(page, label):
            break


# =============================================================================
# Per-shot interactions
#
# The guide documents how the app is *operated*, so most of its images show a
# state the app only reaches through a click: a dialog mid-wizard, an open
# picker, a menu, a filled-in form. Each function below drives one such state
# and returns the callable that closes it again (or None when the shot opened
# nothing). The runner navigates, waits, calls this, takes the picture, then
# runs the cleanup.
#
# Nothing here may commit: no Create, no Save, no Delete, no "Move now". The
# demo server is the data every other shot is taken against.
# =============================================================================

ACTIONS = {}


def action(*names):
    def register(fn):
        for name in names:
            ACTIONS[name] = fn
        return fn
    return register


# --- search palette & comment thread ----------------------------------------

@action("shot-search")
def _search(page, ids):
    # Ctrl+K is handled globally by the shell (meta or ctrl, see
    # app_shell._onGlobalKey), so this works headless on any OS. A query is
    # typed because an empty palette shows only the prompt, and the guide page
    # is about what results look like.
    page.keyboard.press("Control+k")
    page.wait_for_timeout(1500)
    write(page, SEARCH_QUERY, delay=110, after=3000)
    return lambda: dismiss(page, barrier=False)


@action("shot-comments")
def _comments(page, ids):
    # Threads collapse by default; the page is about the expanded thread. The
    # thread is searched for rather than reached by a fixed scroll: the issue
    # grew a description, links and four attachments, and every one of those
    # moved the feed further down than the distance that was measured once.
    bring_into_view(page, lambda: page.get_by_role(
        "button", name=re.compile(r"replies|\d+\s+reply", re.I)).first,
        step=900, tries=12, what="the comment thread")
    # The scroll afterwards is because loading replies grows the list under us.
    if expand_reply_threads(page):
        scroll(page, 420, after=1800)
    return None


# --- getting started ---------------------------------------------------------

@action("shot-dashboard-customize")
def _dashboard_customize(page, ids):
    # Edit mode is a state the normal dashboard gives no hint of: three scope
    # pickers appear and every card grows an eye toggle. Done writes the layout
    # to the account, so it is never pressed — leaving the route drops the draft.
    tap_re(page, r"Customize", after=2200)
    return None


@action("shot-dashboard-hero-board-picker")
def _dashboard_hero_picker(page, ids):
    # The tip "pin the board you care about" points at a picker two clicks deep.
    click_if(page, re.compile(r"Customize"), exact=False)
    page.wait_for_timeout(1800)
    tap_re(page, r"Hero board", after=1400)
    return lambda: dismiss(page)


@action("shot-language-picker")
def _language_picker(page, ids):
    # Language and appearance are one card; the picker shows the list is two
    # entries long, so nobody keeps hunting for their own locale.
    tap(page, "English (UK)", after=1600)
    return lambda: dismiss(page)


@action("shot-server-manager", "shot-mobile-servers")
def _server_manager(page, ids):
    # A single saved server proves nothing about a section on running several,
    # so a second (unreachable, honestly offline) profile is added to this
    # browser profile first. It has to happen after boot: the app migrates the
    # legacy token into per-server storage only while the server list is still
    # missing, so seeding the list up front would sign the app out.
    add_saved_server(page)
    tap(page, "Manage servers", after=3000)
    return lambda: dismiss(page)


@action("shot-mobile-more-sheet")
def _mobile_more(page, ids):
    # The phone nav claims nothing is missing; the sheet is where the Plan group
    # went.
    try:
        tap(page, "More", after=1800)
    except Exception:
        tap_text(page, "More", after=1800)
    return lambda: dismiss(page)


# --- projects & teams --------------------------------------------------------

@action("shot-project-new")
def _project_new(page, ids):
    # Five fields, one optional. The name is typed so the key and the glyph
    # preview derive themselves — a blank dialog hides that they do.
    tap(page, "New project", after=3000)
    write(page, "Billing & Plans", after=1200)
    return lambda: dismiss(page, "Cancel")


@action("shot-team-add-members")
def _team_add_members(page, ids):
    # Step 2 is the argument for the wizard: role and project access are set in
    # the same breath as the invitation. "Add 1" really adds — never pressed.
    tap(page, "Add members", after=3000)
    # Not a name from the seed: the activity feed is seeded by really adding
    # somebody to this team, so which people the picker still offers depends on
    # who that was.
    tap_row(page, ids["addable_person"], after=1200)
    tap(page, "Continue", after=2600)
    return lambda: dismiss(page, "Cancel")


@action("shot-team-add-project")
def _team_add_project(page, ids):
    # Ticked, because the row's tick box and the count on the confirm button are
    # the whole of what this dialog does — an untouched list ends in "Attach 0",
    # which documents nothing. Attach is never pressed.
    tap(page, "Add project", after=3200)
    tap_row(page, "Mobile App", after=1400)
    return lambda: dismiss(page, "Cancel")


@action("shot-workflow-state-migrate")
def _workflow_state_migrate(page, ids):
    # The page's warning box, enforced: the app names the state, counts its
    # issues and refuses to remove it until they have somewhere to go. The
    # settings draft is never saved, so nothing reaches the project.
    scroll(page, 1200)
    tap(page, "Remove state", nth=1, after=2600)
    return lambda: dismiss(page, "Cancel")


@action("shot-project-delete")
def _project_delete(page, ids):
    # The counts are real and Delete stays inert until the project's name is
    # typed — which is why the field is left empty here.
    tap(page, "Delete project", after=3200)
    return lambda: dismiss(page, "Cancel")


# --- issues ------------------------------------------------------------------

@action("shot-issue-create")
def _issue_create(page, ids):
    # Where the twelve fields of the reference table actually live: text left,
    # Details and Timeline stacked right, only Project and Title pre-filled.
    tap(page, "New issue", after=3500)
    fill(page, "Title", "Board columns lose their order after a hard refresh", after=1200)
    # A dirty draft ignores the header's close, and the modal survives a route
    # change — so this one is left by throwing the tab's state away.
    return lambda: reload_app(page)


@action("shot-issue-actions-menu")
def _issue_actions_menu(page, ids):
    # Four later sections all begin "open the … menu"; this is that menu.
    tap(page, "More actions", after=2500)
    return lambda: dismiss(page)


@action("shot-issue-filter")
def _issue_filter(page, ids):
    # Facets are tabs inside one popover, and the counter is what "the button
    # shows how many filters are active" looks like. Cleared again afterwards:
    # the list keeps its filter, and every later /issues shot would inherit it.
    tap(page, "Filter", after=2500)
    tap_row(page, "In Progress", after=1200)
    tap_row(page, "In Review", after=1500)
    return lambda: (click_if(page, "Clear all"), dismiss(page))


@action("shot-issues-filter")
def _issues_filter(page, ids):
    # The same popover as shot-issue-filter, in the state the search page argues
    # about: within a facet the choices are alternatives, between facets they add
    # up. Two facets are picked, and the Assignee one is left open.
    tap(page, "Filter", after=2500)
    tap(page, "Status", after=1400)
    tap_row(page, "In Progress", after=1200)
    tap(page, "Assignee", after=1400)
    tap_row(page, "Lena Vogt", after=1600)
    return lambda: (click_if(page, "Clear all"), dismiss(page))


@action("shot-issues-groupby")
def _issues_groupby(page, ids):
    # Captured in the None state — the button renames itself to the grouping.
    tap(page, "Group by", after=2200)
    return lambda: dismiss(page)


@action("shot-issues-timerange")
def _issues_timerange(page, ids):
    tap(page, "Time range", after=2200)
    return lambda: dismiss(page)


@action("shot-issues-export", "shot-reports-export-menu")
def _export_menu(page, ids):
    # Never select a format: the export pages the whole result set and then
    # starts a download inside the capture browser.
    tap(page, "Export", after=1800)
    return lambda: dismiss(page)


@action("shot-issue-clone")
def _issue_clone(page, ids):
    # The three switches are the section's three bullets, off by default.
    tap(page, "More actions", after=2200)
    tap(page, "Clone…", after=3000)
    return lambda: dismiss(page, "Cancel")


@action("shot-issue-move")
def _issue_move(page, ids):
    # Step 2 is the whole section in one frame: status mapping, the consequences
    # the app worked out by itself, and the keys the issue and its sub-tasks
    # will get. "Move now" really moves and renumbers — never pressed.
    tap(page, "More actions", after=2200)
    tap(page, "Move to project…", after=2800)
    tap(page, "Choose a project…", after=2500)
    tap_row(page, "Mobile App", after=2000)
    tap(page, "Next", after=3200)
    return lambda: dismiss(page, "Cancel")


@action("shot-issue-link")
def _issue_link(page, ids):
    # The relationship table's seven rows, in the app's own words, and from both
    # ends. Scrolled a little past the card so the 13-row menu opens downwards.
    restore = taller(page, 1300)
    scroll(page, 1700)
    tap(page, "Add issue", after=2500)
    tap(page, "is blocked by", after=2500)
    return lambda: (dismiss(page, "Cancel"), restore())


@action("shot-issue-watch-panel")
def _issue_watch_panel(page, ids):
    # Two levels deep behind an unlabelled glyph, and the only place the roster
    # and the "you already get these as the assignee" note exist.
    tap(page, "More actions", after=2200)
    tap(page, "Watch", after=2600)
    return lambda: dismiss(page)


# --- boards ------------------------------------------------------------------

@action("shot-board-new-dialog")
def _board_new(page, ids):
    # Kanban vs Scrum cannot be changed later, and the dialog is where the two
    # descriptions sit side by side.
    tap(page, "New board", after=2800)
    return lambda: dismiss(page, "Cancel")


@action("shot-board-columns")
def _board_columns(page, ids):
    # Where WIP limits are set — an ordinary text box per column, which "the
    # count badge reads 3/5" does not suggest.
    tap(page, "Board options", after=2200)
    tap(page, "Columns", after=3500)
    return lambda: dismiss(page, "Cancel")


@action("shot-board-quick-create")
def _board_quick_create(page, ids):
    # The composer only exists mid-flow. The dotted row has no semantics node of
    # its own — it lives inside the column's label — so it is hit by geometry.
    # Enter would create the issue; Escape drops the draft.
    tap(page, "Active sprint", after=5000)
    column = page.locator('[aria-label^="Open"]').first
    tap_box(page, column, fx=0.5, fy=1.0, dy=-20, after=3000, what="Open column")
    write(page, "Tighten the column header spacing", after=1200)
    return lambda: dismiss(page, barrier=False)


@action("shot-board-filter")
def _board_filter(page, ids):
    # Proves three claims at once: the facet is a searchable multi-select, the
    # button carries a count badge, and the people strip is the same setting.
    tap(page, "Active sprint", after=5000)
    tap(page, "Filter", after=2500)
    tap(page, "Assignee", after=1800)
    tap_row(page, "Amara Okafor", after=1200)
    tap_row(page, "Mei Lin", after=2000)
    # The board keeps its filter, so every later board shot would inherit it.
    return lambda: (click_if(page, "Clear all"), dismiss(page))


@action("shot-board-group-by")
def _board_group_by(page, ids):
    # "Project" is absent because this board spans one project — the option set
    # is board-dependent, which is what the table's last row explains.
    tap(page, "Active sprint", after=5000)
    tap_re(page, r"Group by", after=2000)
    return lambda: dismiss(page)


@action("shot-board-estimate")
def _board_estimate(page, ids):
    # The planning-poker grid, and which issue is being estimated — the part
    # people get wrong. The control's accessible name is only the number, so it
    # must be scoped inside its row.
    tap(page, "Planning", after=5000)
    # The poker control is a sibling of its row, not a child of it, and its
    # accessible name is only the number — so the row is found by its key and
    # the control by sitting on the same line.
    for key, _ in ids["estimate_targets"]:
        row = page.locator(f'[aria-label*="{key}"]').first
        if not row.count():
            continue
        line = row.bounding_box()
        # The screen's root node carries every label on the page, so a match
        # that is not row-sized is that root and not the row we asked for.
        if not line or line["height"] > 120:
            continue
        points = page.get_by_role("button", name=re.compile(r"^\d{1,2}$"))
        for i in range(points.count()):
            spot = points.nth(i).bounding_box()
            if spot and abs(spot["y"] - line["y"]) < line["height"]:
                points.nth(i).click(timeout=9000)
                page.wait_for_timeout(3000)
                return lambda: dismiss(page, "Cancel")
    raise RuntimeError("no estimated row on screen in the planning view")


@action("shot-board-complete-sprint")
def _board_complete_sprint(page, ids):
    # The page's one irreversible action: the completed/not-completed split and
    # the destination for the rest, in one frame. The dialog's own "Complete
    # sprint" would archive the seeded sprint and empty every other board shot.
    tap(page, "Planning", after=5000)
    tap(page, "Complete sprint", after=3000)
    return lambda: dismiss(page, "Cancel")


# --- timeline ----------------------------------------------------------------

def _gantt_week(page):
    """Put the chart on the Week zoom. Zoom and link toggles survive the
    pushState navigation between shots, so each Gantt shot sets its own."""
    click_if(page, "Week", after=2500)


@action("shot-gantt-links")
def _gantt_links(page, ids):
    # The panel is the only place the link and conflict totals are stated.
    _gantt_week(page)
    tap(page, "Links", after=2500)
    return lambda: dismiss(page)


@action("shot-gantt-conflict")
def _gantt_conflict(page, ids):
    # All four conflict signals in one frame: red connector, red bar outline,
    # warning triangle, hover explanation. A click would pin the bar and dim
    # the chart, so the pointer only hovers.
    _gantt_week(page)
    bar = page.get_by_role("button", name=re.compile(rf'^{ids["conflict_key"]} ')).first
    bar.hover(timeout=9000)
    page.wait_for_timeout(2500)
    return lambda: page.mouse.move(20, 20)


@action("shot-gantt-critical-path")
def _gantt_critical_path(page, ids):
    # "Everything on that chain carries an amber ring" is unverifiable from
    # text. Toggled back off afterwards — it would leak into later chart shots.
    _gantt_week(page)
    tap(page, "Links", after=2000)
    page.get_by_label(re.compile(r"^Critical path")).first.click(timeout=9000)
    page.wait_for_timeout(1500)
    dismiss(page)
    page.wait_for_timeout(1500)

    def restore():
        tap(page, "Links", after=1800)
        page.get_by_label(re.compile(r"^Critical path")).first.click(timeout=9000)
        page.wait_for_timeout(1200)
        dismiss(page)
    return restore


@action("shot-issue-link-composer")
def _issue_link_composer(page, ids):
    # Steps 1-3 of the numbered flow at once: where Add issue lives, the closed
    # relationship dropdown, that the search matches titles as well as keys, and
    # that Link/Cancel are the confirm step.
    scroll(page, 700, at=(600, 600))
    tap(page, "Add issue", after=3000)
    fill(page, "Enter URL, search or paste", "capacity", delay=90, after=3500)
    return lambda: dismiss(page, "Cancel")


@action("shot-issue-link-types")
def _issue_link_types(page, ids):
    # The 13-row menu needs room below the dropdown, so the composer is scrolled
    # into the top third first.
    restore = taller(page, 1300)
    scroll(page, 1500, at=(600, 600))
    tap(page, "Add issue", after=3000)
    tap(page, "is blocked by", after=2500)
    return lambda: (dismiss(page, "Cancel"), restore())


@action("shot-issue-dates")
def _issue_dates(page, ids):
    # The row, its clear × and the calendar in one frame. Clicked left of centre
    # on purpose: the × sits at the centre and a centre click wipes the date.
    scroll(page, 500, at=(1200, 600))
    row = page.get_by_label(re.compile(r"^Start date")).first
    tap_box(page, row, fx=0.35, after=3000, what="Start date row")
    return lambda: dismiss(page, "Cancel")


# --- time tracking -----------------------------------------------------------

def _open_work_log(page, scroll_px=0, at=None):
    if scroll_px:
        scroll(page, scroll_px, at=at)
    tap(page, "Log time", after=2500)


@action("shot-time-log")
def _time_log(page, ids):
    # Filled in, because the two-box duration is the tip the section leads with:
    # Hours and Minutes really are separate boxes. Save writes a work entry.
    _open_work_log(page, 500, at=(1200, 600))
    fill(page, "Minutes", "30", after=600, clear=True)
    tap_re(page, r"^Activity type", after=1600)
    tap(page, "Testing", role="menuitem", after=1500)
    fill(page, "Note (optional)", "Re-ran the sprint capacity cases on Safari and Firefox.",
         delay=25, after=800)
    return lambda: dismiss(page, "Cancel")


@action("shot-time-activity")
def _time_activity(page, ids):
    # Six entries and no "other" — that the list is short and fixed is the
    # section's whole argument.
    _open_work_log(page, 500, at=(1200, 600))
    tap_re(page, r"^Activity type", after=2000)
    return lambda: (dismiss(page), dismiss(page, "Cancel"))


@action("shot-time-date")
def _time_date(page, ids):
    # Back-dating a year and no future day, enforced by the picker itself: the
    # tail of the month is rendered disabled rather than failing on Save.
    _open_work_log(page, 500, at=(1200, 600))
    # The button's accessible name *is* the formatted date, and the format
    # follows the browser locale (en-GB here: "20 Aug 2026"), so it is matched
    # by shape rather than by a string that changes every day.
    page.get_by_role("button", name=re.compile(
        r"^(\d{1,2} \w{3} \d{4}|\w{3} \d{1,2}, \d{4})$")).first.click(timeout=9000)
    page.wait_for_timeout(3000)
    return lambda: (dismiss(page, "Cancel"), dismiss(page, "Cancel"))


@action("shot-time-entries")
def _time_entries(page, ids):
    # No clicking: the Timeline card carries both "spent of estimate" and the
    # entry list, and the entries are several people's, not just yours.
    scroll(page, 700, at=(1200, 600))
    return None


# --- collaboration -----------------------------------------------------------

@action("shot-comment-menu")
def _comment_menu(page, ids):
    # Reply/Copy/Copy link/Pin for anyone, Edit/Select/Delete only on your own
    # comment, Delete red at the bottom.
    # Every comment carries its own "More", and the tree lists somebody else's
    # first. Ours is the one on our own comment — the only menu that also
    # offers Edit, Select and the red Delete, which is the section's point.
    # The comment bodies are not in the semantics tree, so the seeded thread is
    # found by its own "N replies" toggle: our comment is the one above it.
    # Either state of the toggle: "3 replies" while collapsed, "Hide replies"
    # once an earlier shot has opened it. Not a bare "repl", which would also
    # match the Reply action every comment carries.
    threads = re.compile(r"replies|\d+\s+reply", re.I)
    toggle = bring_into_view(page,
                             lambda: page.get_by_role("button", name=threads).first,
                             what="our own comment's reply thread")
    more = page.get_by_role("button", name="More", exact=True)
    above = [(i, b) for i, b in
             ((i, more.nth(i).bounding_box()) for i in range(more.count()))
             if b and b["y"] < toggle["y"]]
    if not above:
        raise RuntimeError("no comment menu above the reply thread")
    index = max(above, key=lambda pair: pair[1]["y"])[0]
    more.nth(index).click(timeout=9000)
    page.wait_for_timeout(1200)
    return lambda: dismiss(page)


@action("shot-comment-reactions")
def _comment_reactions(page, ids):
    # What one click offers, and that the full picker is behind the "…".
    # Clicking an emoji would write a reaction into the demo data.
    #
    # The smiley is chosen by where it sits, not by being the first one on the
    # page: the feed scrolls *under* a translucent app bar, so the topmost
    # "React" can be inside the window and behind the bar at the same time —
    # and the bar then eats the click, leaving nothing but a hover tooltip.
    bring_into_view(page, lambda: page.get_by_role(
        "button", name=re.compile(r"replies|\d+\s+reply", re.I)).first,
        step=900, tries=12, what="the comment thread")
    height = page.viewport_size["height"]
    react = page.get_by_role("button", name="React", exact=True)
    spot = next((box for box in (react.nth(i).bounding_box()
                                 for i in range(react.count()))
                 if box and 150 < box["y"] < height - 170), None)
    if spot is None:
        raise RuntimeError("no React button clear of the app bar")
    page.mouse.click(spot["x"] + spot["width"] / 2, spot["y"] + spot["height"] / 2)
    page.wait_for_timeout(1600)
    return lambda: dismiss(page)


@action("shot-comment-mention")
def _comment_mention(page, ids):
    # One menu searches issues, articles and people together as you type.
    # Clicked at its centre rather than through the field's own locator: the
    # composer is docked over the thread, and Playwright refuses to click an
    # element it believes something else covers.
    box = scroll_into_view(page, "Comment…", role="textbox")
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(800)
    # `ke` on purpose: it is the shortest query this seed answers with all three
    # kinds at once — three issues, the "Auth & token refresh" article and Jonas
    # Becker — and the section under the picture is about all three. The menu
    # lists issues first and people last, so a broader query buries the person
    # below the fold and the picture then argues the opposite of the text.
    write(page, "@ke", delay=120, after=1600)
    return lambda: (page.keyboard.press("Escape"), clear_composer(page))


@action("shot-comment-attach-menu", "shot-mobile-composer-attach")
def _comment_attach(page, ids):
    # The "+" is icon-only with no accessible name at all, so it is hit by
    # geometry: the composer row is [+] · field · mic.
    box = scroll_into_view(page, "Comment…", role="textbox")
    page.mouse.click(box["x"] - 32, box["y"] + box["height"] / 2)
    page.wait_for_timeout(1600)
    # Rebooted rather than merely closed: with the composer focused the page
    # stops answering the wheel, and the next shot of the same issue then never
    # reaches the card it needs.
    return lambda: (dismiss(page), reload_app(page))


@action("shot-attachments")
def _attachments(page, ids):
    # The block itself: four tiles, "Add files", and the download and remove
    # buttons a tile grows while the pointer is on it. The grid wraps after
    # three, so stopping at the first row leaves the fourth — the only one with
    # a real thumbnail — under the composer; one tile height further down puts
    # both rows in the frame.
    scroll_into_view(page, re.compile(re.escape(ids["text_attachment"])))
    scroll(page, 250, after=1400)
    # Re-read where the tile ended up, on a short leash: a wheel scroll over a
    # Flutter canvas lands where its own physics put it, not exactly where it
    # was pushed, and the hover buttons are worth one query — but not a 30 s
    # stall on a stale semantics handle if the node has been rebuilt.
    tile = page.get_by_role(
        "button", name=re.compile(re.escape(ids["text_attachment"]))).first
    try:
        box = tile.bounding_box(timeout=5000)
    except Exception:
        box = None
    if box:
        # Two moves: Flutter's hover fires on a pointer that travels, and a
        # single jump onto the tile can arrive as a teleport it ignores.
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 60)
        page.wait_for_timeout(400)
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 40)
        page.wait_for_timeout(1400)
    return lambda: page.mouse.move(20, 20)


@action("shot-attachment-actions")
def _attachment_actions(page, ids):
    # The filled grid the section describes — thumbnails, glyph tiles, and where
    # "Download all" lives.
    scroll_into_view(page, re.compile(re.escape(ids["text_attachment"])))
    tap(page, "More actions", nth=1, after=1800)
    return lambda: dismiss(page)


@action("shot-attachment-viewer")
def _attachment_viewer(page, ids):
    # The text file on purpose: it puts Line numbers / Wrap long lines / Copy
    # all text in frame, the half of the viewer nothing else shows.
    scroll_into_view(page, re.compile(re.escape(ids["text_attachment"])))
    tap_row(page, ids["text_attachment"], after=3000)
    return lambda: dismiss(page, "Close")


# --- search ------------------------------------------------------------------

@action("shot-search-scope-knowledge")
def _search_scope(page, ids):
    # The chips carry a live count each, and an empty query inside a scope is a
    # browse list of the most recently touched items of that kind.
    page.keyboard.press("Control+k")
    page.wait_for_timeout(1800)
    page.get_by_role("button", name=re.compile(r"^Knowledge")).first.click(timeout=9000)
    page.wait_for_timeout(2200)
    return lambda: dismiss(page, barrier=False)


@action("shot-search-recents")
def _search_recents(page, ids):
    # Recents are only written when a result is opened, so three are run first.
    # All three resolve against local commands, so nothing depends on the API.
    for term in ("board", "reports", "knowledge"):
        page.keyboard.press("Control+k")
        page.wait_for_timeout(1400)
        write(page, term, delay=90, after=1600)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2200)
        goto_route(page, "/dashboard", settle=2500)
    page.keyboard.press("Control+k")
    page.wait_for_timeout(1800)
    return lambda: dismiss(page, barrier=False)


# --- knowledge base ----------------------------------------------------------

@action("shot-kb-new-space")
def _kb_new_space(page, ids):
    # Four fields at once, icon and colour as pickers rather than text, and a
    # confirm button that stays dead until the space has a name.
    tap(page, "New space", after=2600)
    write(page, "Support", after=800)
    page.keyboard.press("Tab")
    write(page, "Escalations, on-call handover and customer runbooks.", delay=25, after=900)
    return lambda: dismiss(page, "Cancel")


@action("shot-kb-new-article")
def _kb_new_article(page, ids):
    # Steps 1-3 and 6 in one frame: title, the space picker beside it, and that
    # the button says Publish on a new page.
    tap(page, "New article", after=3000)
    write(page, "How to roll a release", after=1000)
    return lambda: leave_editor(page)


@action("shot-kb-text-style")
def _kb_text_style(page, ids):
    # A line can only be one shape at a time, which is why this is a dropdown
    # and not a row of toggles. With no caret the picker reads "Mixed".
    tap(page, "New article", after=3000)
    write(page, "Cut a release branch, then tag it.", delay=25, after=600)
    # The title has the caret on open; the body has to be clicked, and its only
    # node is the hint it paints while empty.
    body = box_of(page.get_by_text("Write something…", exact=True).first, "article body")
    page.mouse.click(body["x"] + 40, body["y"] + 10)
    page.wait_for_timeout(800)
    write(page, "Every release starts from a green pipeline on main.", delay=25, after=900)
    page.get_by_role("button", name=re.compile(r"^Text style:")).first.click(timeout=9000)
    page.wait_for_timeout(1800)
    return lambda: (dismiss(page), leave_editor(page))


@action("shot-kb-mention-picker")
def _kb_mention_picker(page, ids):
    # "@" opens one picker across issues, articles and people — the modal, its
    # search field, and how a row identifies its kind.
    tap(page, "New article", after=3000)
    write(page, "Release checklist", after=800)
    tap_re(page, r"Mention . link", after=2200)
    # `ok` on purpose: it is what this seed answers with all three kinds and no
    # repeated title — four issues, two articles and Amara Okafor. This dialog
    # has no result cap, so a broad query fills it with the same titles from
    # three projects and the picker reads as broken.
    write(page, "ok", delay=120, after=1600)
    return lambda: (dismiss(page), leave_editor(page))


@action("shot-kb-chip-preview")
def _kb_chip_preview(page, ids):
    # The three chip shapes inline in real prose, plus the hover preview with
    # status, priority and assignee. A click would navigate to the issue.
    # Booted fresh on this article: hovering a chip is the one interaction that
    # depends on the page being settled and unscrolled, and the shot before this
    # one leaves the knowledge view somewhere else.
    reload_app(page)
    page.get_by_role("button", name=ids["chip_key"], exact=True).first.hover(timeout=9000)
    page.wait_for_timeout(1500)
    return lambda: page.mouse.move(20, 20)


@action("shot-kb-tree-menu")
def _kb_tree_menu(page, ids):
    # Drag cannot be photographed; this menu is the part of the tree a still
    # image can show, including that Delete lives there. The ellipsis has no
    # label and only exists while the row is hovered, so it is hit by geometry.
    row = page.get_by_role("button", name=ids["tree_article_title"], exact=True).first
    row.hover(timeout=9000)
    page.wait_for_timeout(900)
    # Hovering reveals two controls at the row's right edge. Only the left one
    # ("Add sub-page") has a name, so the ellipsis is found by sitting next to
    # it — a bare click on the row would just open the article again.
    plus = box_of(page.get_by_role("button", name="Add sub-page").first, "row + button")
    page.mouse.click(plus["x"] + plus["width"] + 14, plus["y"] + plus["height"] / 2)
    page.wait_for_timeout(1800)
    return lambda: dismiss(page)


# --- reports -----------------------------------------------------------------

@action("shot-reports-project-picker")
def _reports_project_picker(page, ids):
    # Reports are one project at a time; the picker makes that rule visible.
    tap(page, ids["project_name"], after=1400)
    return lambda: dismiss(page)


@action("shot-reports-breakdowns")
def _reports_breakdowns(page, ids):
    # Priority, assignee and time-per-activity — the three cards the existing
    # /reports shot cuts off, and the only ones that read durations.
    scroll(page, 820)
    return None


# --- notifications & account -------------------------------------------------

@action("shot-notification-bell")
def _notification_bell(page, ids):
    # The preview the reader meets first, on every screen. "Mark all read" would
    # clear the unread tint for every later shot, so it is never pressed.
    #
    # Clicked by geometry: the shell's top bar — search field, bell, avatar —
    # publishes nothing to the semantics tree, the same way the navy rail does
    # not. The bell sits a fixed distance in from the right edge.
    page.mouse.click(page.viewport_size["width"] - 103, 42)
    page.wait_for_timeout(2500)
    # This popover has no barrier node and ignores Escape; it closes on a click
    # somewhere else, and everywhere else on the dashboard is a card that would
    # navigate. Throwing the tab's state away is the one exit that is inert.
    return lambda: reload_app(page)


@action("shot-account-edit-profile")
def _account_edit_profile(page, ids):
    # One disabled input between two editable ones says "your username is
    # permanent" better than the paragraph can.
    tap(page, "Edit profile", after=1600)
    return lambda: dismiss(page, "Cancel")


@action("shot-account-change-email")
def _account_change_email(page, ids):
    # The guarantee — the old address stays live until the new one is confirmed
    # — is printed inside the dialog. The field stays empty: sending would start
    # a real address change on the demo admin.
    tap(page, "Change", after=1600)
    return lambda: dismiss(page, "Cancel")


@action("shot-account-password-reset")
def _account_password_reset(page, ids):
    # Reset does not open a change-password form, and the dialog says so.
    tap(page, "Reset", after=1500)
    return lambda: dismiss(page, "Cancel")


@action("shot-2fa-scan")
def _twofa_scan(page, ids):
    # Step 1 is where readers get stuck ("I can't scan, I'm on the phone") and
    # the manual entry key under the code is the answer.
    tap(page, "Enable", after=2500)
    return lambda: dismiss(page, "Cancel")


@action("shot-2fa-verify")
def _twofa_verify(page, ids):
    # A segmented six-box entry, not a text field, and a button that only arms
    # once all six are filled. "Verify & enable" would enable 2FA on the demo
    # admin and lock password login out of every later run.
    tap(page, "Enable", after=2500)
    tap(page, "Continue", after=1500)
    write(page, "314159", delay=120, after=900)
    return lambda: dismiss(page, "Cancel")


@action("shot-account-delete-confirm")
def _account_delete(page, ids):
    # The type-to-confirm gate is the section's whole safety story: an empty
    # field beside a dead button. It stays empty.
    scroll(page, 1400, at=(1100, 600))
    tap(page, "Delete account", after=1600)
    return lambda: dismiss(page, "Cancel")


# --- mobile ------------------------------------------------------------------

@action("shot-mobile-time-log")
def _mobile_time_log(page, ids):
    # The sheet slides up from the bottom, and on a phone the Timeline card is
    # far below the fold — both are claims a desktop shot cannot carry.
    scroll_into_view(page, "Log time", step=900)
    tap(page, "Log time", after=2500)
    return lambda: dismiss(page, "Cancel")


@action("shot-mobile-board-select")
def _mobile_board_select(page, ids):
    # Cards do not drag on touch: the round checkboxes and "Move to…" are the
    # replacement. The checkbox has no accessible name, so it is hit by
    # geometry — 12 px padding plus half of an 18 px box from the row's left.
    # Backlog rows are groups named after the person, then the key — and the
    # round checkbox inside them has no node at all, so it is hit at the row's
    # left inset (12 px padding plus half of an 18 px box).
    rows = page.locator('[aria-label*="-"]')
    picked = 0
    for i in range(rows.count()):
        box = rows.nth(i).bounding_box()
        if not box or box["height"] > 60 or not 120 < box["y"] < 700:
            continue
        page.mouse.click(box["x"] + 21, box["y"] + box["height"] / 2)
        page.wait_for_timeout(900)
        picked += 1
        if picked == 2:
            break
    if picked < 2:
        raise RuntimeError("could not tick two backlog rows")
    # "Move to…" is deliberately left closed. It is a Material dropdown opened
    # on the shell's *inner* navigator, so the floating tab pill — a sibling
    # painted after it — lands on top of the menu's last row: whatever the
    # destination list holds, its bottom entry is photographed cut in half. The
    # bar, the ticked rows and the picker itself are the part of this that a
    # still image can carry honestly.
    return None


def shots(ids):
    """Every image the site uses, in capture order.

    Ordered by route so one browser context can walk the app the way a person
    would, and so the shots that change something the app remembers (a filter,
    a chart toggle, dashboard edit mode) sit next to the plain shot of the same
    screen rather than in front of it."""
    board = f"/boards/{ids['board_id']}"
    issue = f"/issues/{ids['issue_id']}"
    chain = f"/issues/{ids['chain_issue_id']}" if ids.get("chain_issue_id") else None
    lst = [
        # dashboard, palette, bell
        ("shot-dashboard", DESKTOP, "/dashboard"),
        ("shot-search", DESKTOP, "/dashboard"),
        ("shot-search-scope-knowledge", DESKTOP, "/dashboard"),
        ("shot-search-recents", DESKTOP, "/dashboard"),
        ("shot-notification-bell", DESKTOP, "/dashboard"),
        ("shot-dashboard-customize", DESKTOP, "/dashboard"),
        ("shot-dashboard-hero-board-picker", DESKTOP, "/dashboard"),
        # projects & teams
        ("shot-projects", DESKTOP, "/projects"),
        ("shot-project-new", DESKTOP, "/projects"),
        ("shot-teams", DESKTOP, "/teams"),
        # issues: the list and everything reachable from one issue
        ("shot-issues", DESKTOP, "/issues"),
        ("shot-issue-create", DESKTOP, "/issues"),
        ("shot-issue-filter", DESKTOP, "/issues"),
        ("shot-issues-filter", DESKTOP, "/issues"),
        ("shot-issues-groupby", DESKTOP, "/issues"),
        ("shot-issues-timerange", DESKTOP, "/issues"),
        ("shot-issues-export", DESKTOP, "/issues"),
        ("shot-issue", DESKTOP, issue),
        ("shot-issue-actions-menu", DESKTOP, issue),
        ("shot-issue-clone", DESKTOP, issue),
        ("shot-issue-move", DESKTOP, issue),
        ("shot-issue-watch-panel", DESKTOP, issue),
        ("shot-issue-link", DESKTOP, issue),
        ("shot-time-entries", DESKTOP, issue),
        ("shot-time-log", DESKTOP, issue),
        ("shot-time-activity", DESKTOP, issue),
        ("shot-time-date", DESKTOP, issue),
        ("shot-attachments", DESKTOP, issue),
        ("shot-attachment-actions", DESKTOP, issue),
        ("shot-attachment-viewer", DESKTOP, issue),
        ("shot-comments", DESKTOP, issue),
        ("shot-comment-menu", DESKTOP, issue),
        ("shot-comment-reactions", DESKTOP, issue),
        ("shot-comment-mention", DESKTOP, issue),
        ("shot-comment-attach-menu", DESKTOP, issue),
        # boards
        ("shot-board", DESKTOP, board),
        ("shot-board-quick-create", DESKTOP, board),
        ("shot-board-filter", DESKTOP, board),
        ("shot-board-group-by", DESKTOP, board),
        ("shot-board-estimate", DESKTOP, board),
        ("shot-board-complete-sprint", DESKTOP, board),
        ("shot-board-new-dialog", DESKTOP, "/board"),
        ("shot-board-columns", DESKTOP, "/board"),
        # timeline
        ("shot-gantt", DESKTOP, "/gantt"),
        ("shot-gantt-links", DESKTOP, "/gantt"),
        ("shot-gantt-conflict", DESKTOP, "/gantt"),
        ("shot-gantt-critical-path", DESKTOP, "/gantt"),
        # time, reports, knowledge, admin
        ("shot-timesheet", DESKTOP, "/timesheet"),
        ("shot-reports", DESKTOP, "/reports"),
        ("shot-reports-breakdowns", DESKTOP, "/reports"),
        ("shot-reports-project-picker", DESKTOP, "/reports"),
        ("shot-reports-export-menu", DESKTOP, "/reports"),
        ("shot-knowledge", DESKTOP, "/knowledge"),
        ("shot-kb-new-space", DESKTOP, "/knowledge"),
        ("shot-kb-new-article", DESKTOP, "/knowledge"),
        ("shot-kb-text-style", DESKTOP, "/knowledge"),
        ("shot-kb-mention-picker", DESKTOP, "/knowledge"),
        ("shot-notifications", DESKTOP, "/notifications"),
        ("shot-watched", DESKTOP, "/watched"),
        ("shot-weekly-summary", DESKTOP, "/weekly-summary"),
        ("shot-admin", DESKTOP, "/admin/users"),
        # account: the plain page first, then each modal it opens
        ("shot-settings", DESKTOP, "/settings"),
        ("shot-notification-matrix", DESKTOP, "/settings"),
        ("shot-account-edit-profile", DESKTOP, "/settings"),
        ("shot-account-change-email", DESKTOP, "/settings"),
        ("shot-account-password-reset", DESKTOP, "/settings"),
        ("shot-2fa-scan", DESKTOP, "/settings"),
        ("shot-2fa-verify", DESKTOP, "/settings"),
        ("shot-account-delete-confirm", DESKTOP, "/settings"),
        # the saved-server list is edited for this one, so it goes last
        ("shot-server-manager", DESKTOP, "/settings"),
        # phone
        ("shot-mobile-dashboard", MOBILE, "/dashboard"),
        ("shot-mobile-more-sheet", MOBILE, "/dashboard"),
        ("shot-mobile-issues", MOBILE, "/issues"),
        ("shot-mobile-issue", MOBILE, issue),
        ("shot-mobile-composer-attach", MOBILE, issue),
        ("shot-mobile-time-log", MOBILE, issue),
        ("shot-mobile-board", MOBILE, board),
        ("shot-mobile-board-select", MOBILE, board),
        ("shot-mobile-settings-index", MOBILE, "/settings"),
        ("shot-language-picker", MOBILE, "/settings?section=appearance"),
        ("shot-mobile-notification-matrix", MOBILE, "/settings?section=notifications"),
        ("shot-mobile-servers", MOBILE, "/settings?section=appearance"),
    ]
    # Ids come from the seed and are absent on an empty server; skip rather than
    # capture a "not found" screen.
    if chain:
        lst += [
            ("shot-issue-link-composer", DESKTOP, chain),
            ("shot-issue-link-types", DESKTOP, chain),
            ("shot-issue-dates", DESKTOP, chain),
        ]
    if ids.get("project_id"):
        settings = f"/projects/{ids['project_id']}/settings"
        lst += [
            ("shot-project-settings", DESKTOP, settings),
            ("shot-workflow-state-migrate", DESKTOP, settings),
            ("shot-project-delete", DESKTOP, settings),
        ]
    if ids.get("team_id"):
        team = f"/teams/{ids['team_id']}"
        lst += [
            ("shot-team", DESKTOP, team),
            ("shot-team-add-members", DESKTOP, team),
            ("shot-team-add-project", DESKTOP, team),
        ]
    if ids.get("article_id"):
        lst.append(("shot-knowledge-article", DESKTOP, f"/knowledge/{ids['article_id']}"))
    if ids.get("chip_article_id"):
        lst.append(("shot-kb-chip-preview", DESKTOP, f"/knowledge/{ids['chip_article_id']}"))
    if ids.get("tree_article_id"):
        lst.append(("shot-kb-tree-menu", DESKTOP, f"/knowledge/{ids['tree_article_id']}"))
    if not ids.get("estimate_key"):
        lst = [s for s in lst if s[0] != "shot-board-estimate"]
    if not ids.get("conflict_key"):
        lst = [s for s in lst if s[0] != "shot-gantt-conflict"]
    if not ids.get("text_attachment"):
        lst = [s for s in lst if s[0] != "shot-attachment-viewer"]
    return lst


def init_script(access=None, refresh=None, server=API):
    """The localStorage a booting app finds. Tokens are omitted for the two gate
    screens, which are only themselves while nobody is signed in."""
    prefs = {
        "flutter.onboarding_done": True,
        "flutter.locale": "en",
        "flutter.theme_mode": "light",
    }
    if server:
        prefs["flutter.server_url"] = server
    if access:
        prefs["flutter.access_token"] = access
        prefs["flutter.refresh_token"] = refresh
    return "\n".join(
        f"localStorage.setItem({json.dumps(k)}, {json.dumps(json.dumps(v))});"
        for k, v in prefs.items()
    )


def capture_gate_shots(browser, staging, record):
    """The two screens the normal loop refuses to take.

    ensure_connected exists so no screenshot ever lands on /connect or /login by
    accident — but the guide's first page is about exactly those two screens, so
    they get their own contexts with their own storage: no tokens at all for the
    connect form, a server URL but no session for sign-in.
    """
    w, h, dpr = DESKTOP
    for name, route, server in (("shot-connect-server", "/connect", None),
                                ("shot-sign-in", "/login", API)):
        ctx = browser.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=dpr,
            color_scheme="light",
            locale="en-GB",
            base_url=WEB_ORIGIN,
        )
        ctx.add_init_script(init_script(server=server))
        if server is None:
            # The built config.js bakes in whatever HINATA_BASE_URL the local
            # .env carries. With it, the app auto-connects to that host, fails,
            # and the connect form comes up carrying a red error and a stale
            # "Saved servers" row instead of the empty first-run screen.
            ctx.route("**/config.js", lambda r: r.fulfill(
                status=200, content_type="text/javascript",
                body='window.hinataDefaultServer = "";'))
        page = ctx.new_page()
        page.goto(f"{WEB_ORIGIN}{route}", wait_until="domcontentloaded")
        page.wait_for_timeout(SETTLE_MS + 2500)
        landed = current_route(page)
        if landed != route:
            record(name, False, f"app left {route} for {landed}")
        else:
            tmp = os.path.join(staging, f"{name}.png")
            page.screenshot(path=tmp)
            # Read the live viewport: a shot may have grown the window to fit a
            # menu that does not deserve to be cut off (see taller()).
            live = page.viewport_size
            keep(tmp, name, (live["width"] * dpr, live["height"] * dpr), record)
        ctx.close()


# Regions that must never reach a published page, as fractions of the image so
# they survive a viewport change. The 2FA enrolment dialog shows a REAL TOTP
# secret twice: once as a scannable QR code and once as the manual-entry key
# beneath it. It belongs to a throwaway demo account on localhost, which is
# exactly the reasoning that gets a working secret published — so it is
# destroyed here, at the one place every screenshot passes through, rather than
# by remembering to do it afterwards.
REDACTIONS = {
    "shot-2fa-scan": [
        (0.4236, 0.3556, 0.5764, 0.6000),   # the QR code
        (0.3524, 0.6306, 0.6476, 0.7083),   # the manual entry key
    ],
}


def redact(path, name):
    """Pixelate the secret regions of a shot beyond recovery.

    Downscale to a handful of pixels and blow it back up with NEAREST: unlike a
    blur this throws the information away instead of smearing it, so no amount
    of sharpening brings back a scannable code or a readable key. An amber rule
    is drawn round each region so a reader sees the redaction was deliberate
    rather than a rendering fault."""
    boxes = REDACTIONS.get(name)
    if not boxes:
        return
    from PIL import Image, ImageDraw
    im = Image.open(path).convert("RGB")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    for left, top, right, bottom in boxes:
        box = (int(left * w), int(top * h), int(right * w), int(bottom * h))
        region = im.crop(box)
        rw, rh = region.size
        small = region.resize((max(1, rw // 20), max(1, rh // 20)), Image.BILINEAR)
        im.paste(small.resize((rw, rh), Image.NEAREST), box)
        draw.rectangle(box, outline=(217, 160, 50), width=4)
    im.save(path, optimize=True)


def keep(tmp, name, expect, record):
    """Move a verified screenshot into the docs. A shot that fails verification
    is dropped on the floor: the previously published image is better than a
    blank one, and the run reports what it could not get."""
    ok, note = verify_png(tmp, expect)
    if ok:
        # Before verification would pass it on, and before it can be moved
        # anywhere a commit could pick it up.
        redact(tmp, name)
        os.replace(tmp, os.path.join(OUT_DIR, f"{name}.png"))
    record(name, ok, note)
    return ok


class _Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript", ".mjs": "text/javascript",
        ".wasm": "application/wasm", ".json": "application/json",
        ".css": "text/css", ".html": "text/html", ".symbols": "text/plain",
    }

    def log_message(self, *a):
        pass

    def do_GET(self):
        # SPA fallback: the app uses clean path URLs (usePathUrlStrategy), so a
        # request for /reports must serve index.html and let the app route.
        fs = self.translate_path(self.path)
        last = self.path.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        if (not os.path.exists(fs) or os.path.isdir(fs)) and "." not in last:
            self.path = "/index.html"
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def serve():
    handler = functools.partial(_Handler, directory=WEB_DIR)
    # Reuse the address: a run that ends while a browser socket is still in
    # TIME_WAIT otherwise refuses to start the next one.
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", WEB_PORT), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def articles(access):
    r = requests.get(f"{API}/api/v1/articles?size=50",
                     headers={"Authorization": f"Bearer {access}"}, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else data.get("content", [])


def chip_article(access):
    """An article whose prose carries an issue chip, and the chip's key. The
    hover preview is the pay-off the knowledge page promises, and it needs a
    real chip in real text — not one the capture typed."""
    for article in articles(access):
        doc = article.get("contentDoc") or ""
        for match in re.finditer(r'\{[^{}]*"type"\s*:\s*"smartlink"[^{}]*\}', doc):
            node = json.loads(match.group(0))
            if node.get("kind") == "issue" and node.get("label"):
                return article["id"], node["label"]
    return None, None


def child_article(access):
    """An article that sits under another one: its row menu is the only one that
    carries both "Move to top level" and "Delete"."""
    for article in articles(access):
        if article.get("parentId"):
            return article["id"], article["title"]
    return None, None


def resolve_ids(access):
    """Everything the shots address by id, resolved from the live seed.

    Nothing is pinned: the demo ids change on every reseed. Where a shot needs a
    *particular* issue — one carrying links, sub-tasks, a sprint and logged time
    at once — it is found by title, because the first row of /issues is not
    stable between calls and no seeded issue has a description to rank by."""
    main_issue = issue_by_title(access, MAIN_ISSUE_TITLE)
    chain_issue = issue_by_title(access, CHAIN_ISSUE_TITLE)
    conflict_issue = issue_by_title(access, CONFLICT_ISSUE_TITLE)
    project_id = first_id(access, "projects")
    chip_id, chip_key = chip_article(access)
    tree_id, tree_title = child_article(access)
    projects = requests.get(f"{API}/api/v1/projects",
                            headers={"Authorization": f"Bearer {access}"}, timeout=15).json()
    projects = projects if isinstance(projects, list) else projects.get("content", [])
    ids = {
        "board_id": first_board_id(access),
        "issue_id": (main_issue or {}).get("id") or an_issue_id(access),
        "chain_issue_id": (chain_issue or {}).get("id"),
        "conflict_key": (conflict_issue or {}).get("readableId"),
        "project_id": project_id,
        "project_name": projects[0]["name"] if projects else None,
        "team_id": first_id(access, "teams"),
        "article_id": first_id(access, "articles"),
        "chip_article_id": chip_id,
        "chip_key": chip_key,
        "tree_article_id": tree_id,
        "tree_article_title": tree_title,
        "text_attachment": TEXT_ATTACHMENT,
    }
    ids["estimate_targets"] = estimate_candidates(access, project_id)
    ids["estimate_key"] = ids["estimate_targets"][0][0] if ids["estimate_targets"] else None
    return ids


def main(frames_only=False, only=None):
    assert os.path.isdir(WEB_DIR), f"missing web build at {WEB_DIR} — run flutter build web"
    os.makedirs(OUT_DIR, exist_ok=True)
    # Preflight: refuse to start unless the seeded demo server is actually up.
    # Without this the app would boot straight into the connect screen and every
    # shot would be a "Connect to your server" screen.
    try:
        requests.get(f"{API}/actuator/health", timeout=5).raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(
            f"demo server not reachable at {API} ({e}). Start it first:\n"
            f"  cd hinata-server && SPRING_PROFILES_ACTIVE=dev HINATA_DEMO_SEED=true "
            f"./gradlew bootRun\nand wait until {API}/actuator/health is UP."
        )
    httpd = serve()
    access, refresh = login()
    seed = init_script(access, refresh)

    # --frames-only: just re-render the two landing-page device heroes
    # (frame-macbook.png / frame-iphone.png) and skip every per-page shot. The
    # heroes only need /dashboard, so no board/issue/thread seeding is required.
    if frames_only:
        print(f"frames-only: re-rendering device heroes; headless={HEADLESS}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS, args=_CHROMIUM_ARGS)
            try:
                frame_heroes(browser, seed)
            finally:
                browser.close()
        iphone_hero_from_simulator(access, refresh)
        httpd.shutdown()
        print("done →", OUT_DIR)
        return

    prune_own_sessions(access)
    ids = resolve_ids(access)
    if ids.get("issue_id"):
        # Before the thread: the attachment shots read the issue back, and the
        # description is what the issue's own two screenshots are captioned on.
        seed_issue_description(access, ids["issue_id"])
        seed_work_entries(access, ids["issue_id"])
        seed_demo_thread(access, ids["issue_id"])
        seed_comment_reactions(access, ids["issue_id"])
        seed_demo_attachments(access, ids["issue_id"])
    if ids.get("board_id"):
        seed_next_sprint(access, ids["board_id"])
    if ids.get("team_id"):
        seed_team_activity(access, ids["team_id"])
        # After the seeding, not before it: seeding the activity feed puts one
        # more person on the team, and that is one person the Add-members
        # picker no longer offers.
        ids["addable_person"] = non_member(access, ids["team_id"])
    watched = [i for i in (issue_by_title(access, t) for t in NOTIFY_ISSUE_TITLES) if i]
    if len(watched) == 3:
        seed_demo_notifications(access, watched)
    todo = shots(ids)
    if only:
        wanted = set(only)
        unknown = wanted - {s[0] for s in todo} - set(GATE_SHOTS)
        if unknown:
            raise SystemExit(
                f"unknown shot(s): {', '.join(sorted(unknown))}. Available: "
                + ", ".join(s[0] for s in todo)
            )
        todo = [s for s in todo if s[0] in wanted]
    gates = [g for g in GATE_SHOTS if not only or g in only]
    print(f"logged in; board {ids['board_id']}; issue {ids['issue_id']}; "
          f"{len(todo) + len(gates)} shots; headless={HEADLESS}")

    results = []

    def record(name, ok, note):
        results.append((name, ok, note))
        # Flushed: a full run takes half an hour, and a redirected log that only
        # appears at the end cannot be watched.
        print(f"  {'✓' if ok else '✗'} {name:30} {note}", flush=True)

    args = _CHROMIUM_ARGS
    boot_ms = int(os.environ.get("BOOT_MS", "8500"))
    staging = tempfile.mkdtemp(prefix="hinata-shots-")

    def capture_group(browser, group):
        """One context per viewport: boot once, then navigate client-side.

        The app boots through an auth/connect redirect that always lands on
        /dashboard, so an initial deep link is lost. Instead we boot once and
        drive go_router via the History API — which keeps the authenticated
        session and actually changes route."""
        if not group:
            return
        w, h, dpr = group[0][1]
        ctx = browser.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=dpr,
            color_scheme="light",
            locale="en-GB",
            base_url=WEB_ORIGIN,
        )
        ctx.add_init_script(seed)
        page = ctx.new_page()
        page.goto(f"{WEB_ORIGIN}/dashboard", wait_until="domcontentloaded")
        page.wait_for_timeout(boot_ms)
        # Prove the app booted into the connected+signed-in app, not the connect
        # form, before we screenshot a single route.
        ensure_connected(page, "boot")
        for name, _, route in group:
            goto_route(page, route)
            # A rejected token / dropped server would bounce this route to
            # /login or /connect; verify we're still inside the app first.
            ensure_connected(page, name)
            # Every interaction addresses controls through the semantics tree,
            # and it is the app itself that must switch it on.
            enable_semantics(page)
            # An overlay the shot before this one failed to close would sit in
            # this picture *and* eat its scrolling, so it is worth a reboot.
            if not clear_overlays(page):
                reload_app(page)
            # Scroll position survives a pushState to the same route, and the
            # shot before this one may have left the page halfway down.
            scroll(page, -6000, after=900)
            if SCROLLS.get(name):
                scroll(page, SCROLLS[name], after=2500)
            # Every teardown this shot owes, innermost last: a window resize is
            # undone after whatever the interaction opened inside it.
            undo = []
            if WIDTHS.get(name):
                undo.append(wider(page, WIDTHS[name]))
            step = ACTIONS.get(name)
            if step:
                try:
                    closer = step(page, ids)
                    if closer:
                        undo.insert(0, closer)
                except Exception as e:
                    # Whatever half-opened is still on screen and would block
                    # every following shot in this context.
                    record(name, False, f"interaction failed: {_why(e)}")
                    for step_back in undo:
                        try:
                            step_back()
                        except Exception:
                            pass
                    dismiss(page)
                    reload_app(page)
                    continue
            tmp = os.path.join(staging, f"{name}.png")
            page.screenshot(path=tmp)
            # Read the live viewport: a shot may have grown the window to fit a
            # menu that does not deserve to be cut off (see taller()).
            live = page.viewport_size
            keep(tmp, name, (live["width"] * dpr, live["height"] * dpr), record)
            for step_back in undo:
                try:
                    step_back()
                except Exception as e:
                    print(f"    (cleanup after {name} failed: {_why(e)})")
                    dismiss(page)
                    reload_app(page)
        ctx.close()

    desktop = [s for s in todo if s[1] == DESKTOP]
    mobile = [s for s in todo if s[1] == MOBILE]
    undo_sso = english_sso_name(access) if "shot-sign-in" in gates else (lambda: None)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, args=args)
        try:
            if gates:
                capture_gate_shots(browser, staging, record)
            capture_group(browser, desktop)
            capture_group(browser, mobile)
            if not only:
                frame_heroes(browser, seed)
        finally:
            browser.close()
    httpd.shutdown()
    missing = [(n, why) for n, ok, why in results if not ok]
    print(f"\n{len(results) - len(missing)}/{len(results)} shots captured → {OUT_DIR}")
    for name, why in missing:
        print(f"  NOT SHIPPED  {name:30} {why}")
    # Report first, then the two teardowns that can fail on their own: leaving
    # the demo server renamed, or a simulator that is not booted, must not cost
    # the run its report.
    try:
        undo_sso()
    except Exception as e:
        print(f"  (could not restore the SSO provider name: {_why(e)})")
    # Real-device hero last: everything web-based is already on disk if this
    # raises (sim not booted / app not installed).
    if not only:
        iphone_hero_from_simulator(access, refresh)


def _why(exc):
    """The first line of an exception — Playwright's messages carry a page of
    call log after it, which drowns the run report."""
    return str(exc).split("\n")[0][:160]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Capture fresh English screenshots of the Hinata app for the docs."
    )
    parser.add_argument(
        "--only",
        action="append",
        metavar="SHOT",
        help="Capture only this shot (repeatable), e.g. --only shot-search. "
             "Skips the device heroes. Without it every shot is captured.",
    )
    parser.add_argument(
        "--frames-only",
        action="store_true",
        help="Only re-render the native device heroes (frame-macbook.png / "
             "frame-iphone.png) and skip every per-page shot.",
    )
    cli = parser.parse_args()
    main(frames_only=cli.frames_only, only=cli.only)
