#!/usr/bin/env python3
"""Capture fresh, English screenshots of the Hinata app for the docs.

Serves the built Flutter web bundle, logs in to the seeded demo backend,
pre-authenticates the app via localStorage, then screenshots each doc-relevant
route at a desktop and (for a few) a mobile viewport. Output PNGs land in the
docs repo's assets/img/ so build.py copies them into the site.

Prereqs:
  - a seeded demo server on :8080 (SPRING_PROFILES_ACTIVE=dev HINATA_DEMO_SEED=true)
  - `flutter build web --release` in hinata-app  (build/web must exist)
  - venv with playwright + requests + pillow, and `playwright install chromium`

Besides the per-page shots this also seeds a threaded demo comment on the shot
issue, captures it (shot-comments), and re-renders the landing page's framed
hero images (frame-macbook.png / frame-iphone.png) via
hinata-app/tool/device_frames.py.

Run:  <venv>/bin/python tools/capture.py
"""
from __future__ import annotations

import functools
import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading

from urllib.parse import urlparse

import requests
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

# Gate/redirect screens the app shows while it is NOT connected + signed in
# (the "Connect to your server" form, the login form, the boot splash, the
# first-run wizard). A screenshot must NEVER land on one of these. The app uses
# clean path URLs and go_router rewrites the address bar on every redirect, so
# we detect a gate purely from the browser URL and refuse to capture it.
GATE_ROUTES = {
    "/connect", "/connecting", "/login", "/setup", "/onboarding", "/update",
}

# Wheel-scroll (px) applied before the screenshot, for below-the-fold content.
SCROLLS = {"shot-comments": 1600}

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
    placeholder; activating it flips the tree on. Returns True on success."""
    try:
        ph = page.locator(
            "flt-semantics-placeholder, [aria-label='Enable accessibility']"
        )
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


def shots(board_id, issue_id):
    board = f"/boards/{board_id}"
    lst = [
        ("shot-dashboard", DESKTOP, "/dashboard"),
        ("shot-board", DESKTOP, board),
        ("shot-reports", DESKTOP, "/reports"),
        ("shot-gantt", DESKTOP, "/gantt"),
        ("shot-issues", DESKTOP, "/issues"),
        ("shot-knowledge", DESKTOP, "/knowledge"),
        ("shot-teams", DESKTOP, "/teams"),
        ("shot-settings", DESKTOP, "/settings"),
        ("shot-admin", DESKTOP, "/admin/users"),
        ("shot-timesheet", DESKTOP, "/timesheet"),
        ("shot-mobile-dashboard", MOBILE, "/dashboard"),
        ("shot-mobile-board", MOBILE, board),
        ("shot-mobile-issues", MOBILE, "/issues"),
    ]
    if issue_id:
        lst.insert(6, ("shot-issue", DESKTOP, f"/issues/{issue_id}"))
        lst.insert(7, ("shot-comments", DESKTOP, f"/issues/{issue_id}"))
    return lst


def init_script(access, refresh):
    prefs = {
        "flutter.server_url": API,
        "flutter.access_token": access,
        "flutter.refresh_token": refresh,
        "flutter.onboarding_done": True,
        "flutter.locale": "en",
        "flutter.theme_mode": "light",
    }
    return "\n".join(
        f"localStorage.setItem({json.dumps(k)}, {json.dumps(json.dumps(v))});"
        for k, v in prefs.items()
    )


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
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", WEB_PORT), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
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
    board_id = first_board_id(access)
    issue_id = an_issue_id(access)
    if issue_id:
        seed_demo_thread(access, issue_id)
    seed = init_script(access, refresh)
    todo = shots(board_id, issue_id)
    print(f"logged in; board {board_id}; issue {issue_id}; {len(todo)} shots; "
          f"headless={HEADLESS}")

    args = [
        "--hide-scrollbars",
        "--force-color-profile=srgb",
        "--enable-unsafe-swiftshader",
        "--use-gl=angle",
        "--use-angle=swiftshader",
    ]
    boot_ms = int(os.environ.get("BOOT_MS", "8500"))

    def capture_group(browser, group):
        """One context per viewport: boot once, then navigate client-side.

        The app boots through an auth/connect redirect that always lands on
        /dashboard, so an initial deep link is lost. Instead we boot once and
        drive go_router via the History API (pushState + popstate) — which keeps
        the authenticated session and actually changes route."""
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
            page.evaluate(
                "(r) => { window.history.pushState(null, '', r);"
                " window.dispatchEvent(new PopStateEvent('popstate', {state: null})); }",
                route,
            )
            page.wait_for_timeout(SETTLE_MS)
            # A rejected token / dropped server would bounce this route to
            # /login or /connect; verify we're still inside the app first.
            ensure_connected(page, name)
            if SCROLLS.get(name):
                # Flutter web renders to canvas; wheel events over the content
                # scroll the inner scrollable (comments live below the fold).
                page.mouse.move(w // 2, h // 2)
                page.mouse.wheel(0, SCROLLS[name])
                page.wait_for_timeout(2500)
            if name == "shot-comments":
                # Open the reply thread so the shot shows it expanded, then nudge
                # it back into view (loading replies grows the list).
                if expand_reply_threads(page):
                    page.mouse.move(w // 2, h // 2)
                    page.mouse.wheel(0, 260)
                    page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(OUT_DIR, f"{name}.png"))
            print(f"  ✓ {name:24} {w}x{h}@{dpr} {route}")
        ctx.close()

    desktop = [s for s in todo if s[1] == DESKTOP]
    mobile = [s for s in todo if s[1] == MOBILE]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, args=args)
        try:
            capture_group(browser, desktop)
            capture_group(browser, mobile)
            frame_heroes(browser, seed)
        finally:
            browser.close()
    # Real-device hero last: everything web-based is already on disk if this
    # raises (sim not booted / app not installed).
    iphone_hero_from_simulator(access, refresh)
    httpd.shutdown()
    print("done →", OUT_DIR)


if __name__ == "__main__":
    main()
