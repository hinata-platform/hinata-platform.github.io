#!/usr/bin/env python3
"""Capture fresh, English screenshots of the Hinata app for the docs.

Serves the built Flutter web bundle, logs in to the seeded demo backend,
pre-authenticates the app via localStorage, then screenshots each doc-relevant
route at a desktop and (for a few) a mobile viewport. Output PNGs land in the
docs repo's assets/img/ so build.py copies them into the site.

Prereqs:
  - a seeded demo server on :8080 (SPRING_PROFILES_ACTIVE=dev HINATA_DEMO_SEED=true)
  - `flutter build web --release` in hinata-app  (build/web must exist)
  - venv with playwright + requests, and `playwright install chromium`

Run:  <venv>/bin/python tools/capture.py
"""
from __future__ import annotations

import functools
import http.server
import json
import os
import socketserver
import threading

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
SETTLE_MS = int(os.environ.get("SETTLE_MS", "7500"))


def login():
    r = requests.post(f"{API}/api/v1/auth/login", json=LOGIN, timeout=15)
    r.raise_for_status()
    d = r.json()
    return d["accessToken"], d["refreshToken"]


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
    httpd = serve()
    access, refresh = login()
    board_id = first_board_id(access)
    issue_id = an_issue_id(access)
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
        for name, _, route in group:
            page.evaluate(
                "(r) => { window.history.pushState(null, '', r);"
                " window.dispatchEvent(new PopStateEvent('popstate', {state: null})); }",
                route,
            )
            page.wait_for_timeout(SETTLE_MS)
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
        finally:
            browser.close()
    httpd.shutdown()
    print("done →", OUT_DIR)


if __name__ == "__main__":
    main()
