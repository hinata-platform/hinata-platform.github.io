---
title: Single sign-on (SSO)
description: Configure OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP single sign-on in Hinata at runtime — Keycloak, Authentik, Azure AD, Google, Synology SSO and more.
---

# Single sign-on (SSO)

Hinata can delegate authentication to your identity provider so people sign in with the account they already have. It supports **OpenID Connect (OIDC)**, generic **OAuth 2.0**, **SAML 2.0** and **LDAP**, and every provider is configured **at runtime from the Admin area** — stored in MongoDB, applied **without a restart**, with secrets held **write-only**.

Tested against common IdPs including **Keycloak**, **Authentik**, **Synology SSO**, **Microsoft Entra ID (Azure AD)** and **Google**. For the built-in username/password system see [Authentication](/en/authentication.html).

## How it works

1. An operator adds a provider under **Admin → SSO** and saves it. Because the config lives in Mongo, it is live immediately — no environment change, no redeploy.
2. The app fetches the list of enabled providers from the public endpoint **`/api/v1/auth/sso/providers`** and renders a sign-in button per provider on the login screen.
3. The user is sent to the identity provider to authenticate.
4. The IdP redirects back to Hinata's callback; the server verifies the response, provisions or matches the user, and hands control back to the app through the **`hinata://auth-callback`** deep link (or the equivalent universal link on the web build).

!!! info "Works behind proxies and tunnels"
    The OAuth 2.0 **authorization-request state is stored in MongoDB**, not in a cookie or HTTP session. That means the flow survives reverse proxies, load balancers and dev tunnels (e.g. ngrok) that would otherwise drop or rewrite the session cookie — a common cause of `authorization_request_not_found` errors elsewhere.

## Runtime configuration, write-only secrets

Everything about a provider — issuer, client id, scopes, attribute mapping — is edited in the Admin area and persisted to Mongo, where the **database overrides the environment**. Client secrets and signing keys are **write-only**: you can set or replace them, but the API never echoes them back. This keeps credentials out of logs, out of API responses and out of the app.

## OpenID Connect example

OIDC is the recommended protocol for modern IdPs (Keycloak, Authentik, Entra ID, Google, Synology SSO). A minimal configuration:

| Field | Example value | Notes |
| --- | --- | --- |
| Protocol | `OIDC` | OpenID Connect (OAuth 2.0 + identity layer) |
| Display name | `Company SSO` | Label on the login button |
| Issuer | `https://id.example.com/realms/company` | The IdP's issuer URL; discovery document at `/.well-known/openid-configuration` |
| Client ID | `hinata` | The client you register in the IdP |
| Client secret | `••••••••` | Write-only; stored encrypted, never returned |
| Scopes | `openid profile email` | `openid` is required; `email` is used to match/provision |
| Redirect URI | `https://api.track.example.com/api/v1/auth/sso/callback` | Register this exact URL in the IdP |

!!! warning "Register the exact redirect URI"
    The **redirect / callback URI you enter at the identity provider must match the server's callback URL exactly** — scheme, host, port and path. A trailing-slash or `http`-vs-`https` mismatch is the number-one cause of failed logins. Use your **public API base** (e.g. `https://api.track.example.com`), not an internal hostname, and add every environment you run (staging, production) as a separate allowed redirect.

### What the IdP must allow

- The **redirect URI** above, on your public API host.
- The app's post-login return target — the `hinata://auth-callback` deep link is handled by the client, so no extra IdP config is needed for it, but any web-based post-login redirect must be on your allowed origins (`HINATA_CORS_ALLOWED_ORIGINS`).

## Other protocols

- **OAuth 2.0** — for providers without a full OIDC discovery document. You supply the authorization, token and user-info endpoints explicitly and map the returned profile fields.
- **SAML 2.0** — enterprise SSO. You exchange metadata with the IdP (entity id, ACS URL, signing certificate) and map assertion attributes to the Hinata user.
- **LDAP** — bind against a directory (e.g. Active Directory, OpenLDAP) with a search base and user/group filters; good for on-prem directories without a web-SSO layer.

!!! warning "SAML: mind the clock"
    SAML assertions are time-bound and signed. If the Hinata server's clock drifts from the IdP's, valid assertions are rejected as expired or not-yet-valid. Keep **NTP** running on the server host and allow only a small clock-skew tolerance. Also verify you are validating the IdP's **signing certificate** and rotate it before it expires.

## Provisioning and access

A first SSO login provisions a Hinata user matched on email. From there the usual model applies: project and team membership gate what the person can see (teams' per-member project access), and `ADMIN` is required for the Admin area. You can combine SSO with local auth, or set `localAuthEnabled = false` (see [Authentication](/en/authentication.html)) to make SSO the only way in.

## Troubleshooting

- **`authorization_request_not_found`** — almost always a proxy/tunnel dropping session state. Hinata already stores this in Mongo; make sure you are on a current build and that your reverse proxy forwards the callback path untouched.
- **Redirect URI mismatch** — re-check the URI registered at the IdP against your public API base, character for character.
- **SAML "assertion expired"** — clock skew; fix NTP on the server host.
- **No providers on the login screen** — confirm the provider is enabled and that the app can reach `/api/v1/auth/sso/providers` (it is public, no token required).

## Where to go next

- **[Authentication](/en/authentication.html)** — local credentials, 2FA and the AuthPolicy flags you pair with SSO.
- **[Security model](/en/security.html)** — how tokens, headers and rate limiting protect the whole surface.
- **[Reverse proxy & TLS](/en/reverse-proxy.html)** — get the public host and forwarded headers right so callbacks land.
