---
title: Reverse proxy & TLS
description: Put the web app and API behind nginx, Caddy or Traefik with HTTPS, SSE and trusted-proxy headers.
---

# Reverse proxy & TLS

Hinata publishes two plain HTTP services on the host:

- the **web app** on `HINATA_APP_PORT` (default `3456`)
- the **API** on `HINATA_PORT` (default `3356`)

In production you never expose these ports directly. A reverse proxy terminates
TLS and forwards requests to the containers.

The recommended layout uses two subdomains:

| Subdomain | Purpose | Forwards to |
| --- | --- | --- |
| `track.example.com` | Flutter web app | `host:3456` (`HINATA_APP_PORT`) |
| `api.track.example.com` | REST API + SSE | `host:3356` (`HINATA_PORT`) |

!!! info "Why two subdomains"
    The web app calls the API cross-origin. Separate hostnames keep CORS
    explicit, let you scale or cache each one independently, and match the
    defaults in `.env.example` (`HINATA_BASE_URL` / `HINATA_WEB_BASE_URL`).

Below you'll find ready configs for **nginx**, **Caddy** and **Traefik**.

## Before you start: three settings that must match

Set these on the Hinata **server** container, whatever proxy you use (see the
[Configuration reference](/en/configuration.html)):

```properties
# Public URLs the server advertises (JWT issuer, e-mail deep links, SSO redirects)
HINATA_BASE_URL=https://api.track.example.com
HINATA_WEB_BASE_URL=https://track.example.com

# Browser origins allowed to call the API cross-origin: MUST include the web app
HINATA_CORS_ALLOWED_ORIGINS=https://track.example.com

# CIDR(s) of your reverse proxy so the server trusts X-Forwarded-* from it
HINATA_TRUSTED_PROXIES=172.16.0.0/12
```

!!! danger "Get HINATA_TRUSTED_PROXIES right or lose per-client rate limiting"
    Hinata reads the real client IP from `X-Forwarded-For` **only** when the
    immediate peer is inside `HINATA_TRUSTED_PROXIES`. If it's empty, nobody is
    trusted and every request appears to come from the proxy.

    Rate limiting (`HINATA_RATE_LIMIT_*`) and brute-force login blocking key on
    client IP. A wrong value means **one shared bucket for the whole internet**.
    Either everyone gets throttled together, or a spoofed `X-Forwarded-For`
    bypasses the limit.

    Use the proxy's address **as the container sees it** (usually the Docker
    bridge subnet, e.g. `172.16.0.0/12`). Not the proxy's public IP.

    Find the address in the server logs, or inspect the network:

    ```bash
    docker network inspect hinata_hinata \
      --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
    ```

!!! tip "HSTS is already handled"
    The server sends `Strict-Transport-Security`, CSP and `Referrer-Policy`
    itself. You do **not** need to add HSTS in the proxy. Let the proxy handle
    TLS and certificate renewal.

## nginx + Let's Encrypt (certbot)

Get certificates for both hostnames first. Then use the server blocks below.

### Get certificates

```bash
sudo certbot certonly --nginx \
  -d track.example.com \
  -d api.track.example.com
```

Certbot sets up the renewal timer itself. Test it with
`sudo certbot renew --dry-run`.

### Server blocks

```nginx
# --- Redirect all HTTP to HTTPS ---------------------------------------------
server {
    listen 80;
    listen [::]:80;
    server_name track.example.com api.track.example.com;
    return 301 https://$host$request_uri;
}

# --- Web app: track.example.com  →  host:3456 -------------------------------
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name track.example.com;

    ssl_certificate     /etc/letsencrypt/live/track.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/track.example.com/privkey.pem;

    # Flutter web can ship large canvaskit/wasm assets
    client_max_body_size 25m;

    location / {
        proxy_pass http://127.0.0.1:3456;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;
    }
}

# --- API: api.track.example.com  →  host:3356 -------------------------------
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name api.track.example.com;

    ssl_certificate     /etc/letsencrypt/live/api.track.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.track.example.com/privkey.pem;

    # Attachments upload here: raise to match your ENV-driven attachment limit
    client_max_body_size 50m;

    location / {
        proxy_pass http://127.0.0.1:3356;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;
    }

    # --- Server-Sent Events (live attachment sync) --------------------------
    # SSE connections stay open; disable buffering and use long read timeouts,
    # otherwise clients only receive events in bursts or the stream drops.
    location ~ ^/api/v1/.*/stream$ {
        proxy_pass http://127.0.0.1:3356;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Upgrade handling (harmless for SSE, ready for WebSocket)
        proxy_set_header Connection        "";
        proxy_set_header Upgrade           $http_upgrade;

        proxy_buffering    off;   # push each event through immediately
        proxy_cache        off;
        chunked_transfer_encoding off;
        proxy_read_timeout 3600s; # keep the stream alive up to an hour idle
        proxy_send_timeout 3600s;
    }
}
```

!!! warning "Don't buffer the stream"
    The most common SSE bug is a proxy that buffers the response. With
    `proxy_buffering off` and a long `proxy_read_timeout` on the `/stream`
    location, attachment updates arrive in real time. With default buffering,
    events look "stuck" until the connection closes.

## Caddy (automatic HTTPS)

Caddy is the least work. It obtains and renews Let's Encrypt certificates
itself, without certbot or timers. This is the whole `Caddyfile`:

```caddy
track.example.com {
    reverse_proxy 127.0.0.1:3456
}

api.track.example.com {
    # SSE / streaming endpoints: stream through without buffering
    @stream path_regexp stream ^/api/v1/.*/stream$
    reverse_proxy @stream 127.0.0.1:3356 {
        flush_interval -1
    }

    reverse_proxy 127.0.0.1:3356
}
```

!!! tip "Caddy already does the right thing"
    Caddy sets `X-Forwarded-For`, `X-Forwarded-Proto` and `X-Forwarded-Host`
    automatically. `flush_interval -1` turns off buffering so SSE flows right
    away. WebSocket upgrades pass through with no extra config. Just make sure
    `HINATA_TRUSTED_PROXIES` covers the address Caddy reaches the container from.

For a real deployment on ports 80/443, Caddy needs a valid e-mail for ACME.
Both DNS records must point at the host:

```caddy
{
    email admin@example.com
}
```

## Traefik (labels)

If Traefik already runs as your Docker ingress, add labels to the `hinata-app`
and `hinata-server` services. No separate config file needed. The example
assumes a `websecure` entrypoint on `:443` and a resolver named `le`:

```yaml
services:
  hinata-server:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.hinata-api.rule=Host(`api.track.example.com`)"
      - "traefik.http.routers.hinata-api.entrypoints=websecure"
      - "traefik.http.routers.hinata-api.tls.certresolver=le"
      - "traefik.http.services.hinata-api.loadbalancer.server.port=8080"

  hinata-app:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.hinata-web.rule=Host(`track.example.com`)"
      - "traefik.http.routers.hinata-web.entrypoints=websecure"
      - "traefik.http.routers.hinata-web.tls.certresolver=le"
      - "traefik.http.services.hinata-web.loadbalancer.server.port=80"
```

!!! note "Traefik and SSE"
    Traefik doesn't buffer responses by default, so the attachment SSE endpoint
    works out of the box. Set `HINATA_TRUSTED_PROXIES` to the CIDR of Traefik's
    container or network. Traefik forwards `X-Forwarded-For`, and Hinata only
    honours it from a trusted peer.

## Verifying it works

```bash
# API reachable and healthy through the proxy
curl -s https://api.track.example.com/actuator/health
# → {"status":"UP"}

# Public metadata (no token required)
curl -s https://api.track.example.com/api/v1/meta

# Web app serves HTML
curl -sI https://track.example.com | head -n 1
```

Also check that real client IPs get logged. Hit an endpoint from another machine
and watch the server logs. The logged IP should be **yours**, not the Docker
gateway. If it shows the proxy's address, `HINATA_TRUSTED_PROXIES` is wrong.

## Next steps

- [Configuration reference](/en/configuration.html): every environment variable
- [Production deployment](/en/deployment.html): the full Docker Compose stack
- [Setup & first run](/en/setup-wizard.html): create the first organization and admin
- [Backups & upgrades](/en/backups.html): run the stack over time
