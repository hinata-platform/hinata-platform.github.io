---
title: Single sign-on (SSO)
description: Configure OpenID Connect, OAuth 2.0, SAML 2.0 and LDAP single sign-on at runtime, with Keycloak, Authentik, Azure AD, Google, Synology SSO and more.
---

# Single sign-on (SSO)

With SSO, people sign in through your identity provider (IdP) with the account they already have.

- Supported: **OpenID Connect (OIDC)**, generic **OAuth 2.0**, **SAML 2.0** and **LDAP**.
- Providers are configured **at runtime in the Admin area**. They are stored in MongoDB, applied **without a restart**, and secrets are **write-only**.
- Tested with **Keycloak**, **Authentik**, **Synology SSO**, **Microsoft Entra ID (Azure AD)** and **Google**.

Local username and password sign-in: [Authentication](/en/authentication.html).

## How it works

1. An operator adds a provider under **Admin → SSO** and saves it. It is live immediately, with no environment change or redeploy.
2. The app fetches the enabled providers from the public endpoint **`/api/v1/auth/sso/providers`** and shows a sign-in button for each on the login screen.
3. The user authenticates at the identity provider.
4. The IdP redirects back to Hinata's callback. The server verifies the response, provisions or matches the user and hands control back to the app through the **`hinata://auth-callback`** deep link (or the matching universal link on the web build).

!!! info "Works behind proxies and tunnels"
    The OAuth 2.0 **authorization-request state is stored in MongoDB** instead of a cookie or HTTP session. So the flow survives reverse proxies, load balancers and dev tunnels (e.g. ngrok) that would otherwise drop or rewrite the session cookie. Elsewhere, that is a common cause of `authorization_request_not_found`.

## Runtime configuration, write-only secrets

Every provider setting (issuer, client id, scopes, attribute mapping) is edited in the Admin area and stored in Mongo, where the **database overrides the environment**.

Client secrets and signing keys are **write-only**: you can set or replace them, but the API never returns them. That keeps them out of logs, API responses and the app.

## OpenID Connect example

OIDC is the recommended protocol for modern IdPs (Keycloak, Authentik, Entra ID, Google, Synology SSO). A minimal configuration:

| Field | Example value | Notes |
| --- | --- | --- |
| Protocol | `OIDC` | OpenID Connect (OAuth 2.0 + identity layer) |
| Display name | `Company SSO` | Label on the login button |
| Issuer | `https://id.example.com/realms/company` | The IdP's issuer URL. Discovery document at `/.well-known/openid-configuration` |
| Client ID | `hinata` | The client you register in the IdP |
| Client secret | `••••••••` | Write-only, stored encrypted, never returned |
| Scopes | `openid profile email` | `openid` is required. `email` is used to match and provision users |
| Redirect URI | `https://api.track.example.com/api/v1/auth/sso/callback` | Register this exact URL in the IdP |

!!! warning "Register the exact redirect URI"
    The **redirect URI at the identity provider must match the server's callback URL exactly**: scheme, host, port and path. A trailing slash or `http` instead of `https` is the number-one cause of failed logins. Use your **public API base** (e.g. `https://api.track.example.com`), not an internal hostname. Add every environment you run (staging, production) as a separate allowed redirect.

### What the IdP must allow

- The **redirect URI** above, on your public API host.
- The return after login. The client handles the `hinata://auth-callback` deep link, so the IdP needs no extra config for it. Any web-based post-login redirect must be on your allowed origins (`HINATA_CORS_ALLOWED_ORIGINS`).

## Other protocols

- **OAuth 2.0:** for providers without a full OIDC discovery document. You enter the authorization, token and user-info endpoints yourself and map the returned profile fields.
- **SAML 2.0:** enterprise SSO. You exchange metadata with the IdP (entity id, ACS URL, signing certificate) and map assertion attributes to the Hinata user.
- **LDAP:** bind against a directory (e.g. Active Directory, OpenLDAP) with a search base and user and group filters. Good for on-prem directories without a web SSO layer.

!!! warning "SAML: mind the clock"
    SAML assertions are signed and time-bound. If the Hinata server's clock drifts from the IdP's, valid assertions are rejected as expired or not yet valid. Keep **NTP** running on the server host and allow only a small clock skew. Also validate the IdP's **signing certificate** and rotate it before it expires.

## Provisioning and access

A first SSO login provisions a Hinata user, matched on email. After that the usual model applies:

- Project and team membership decide what the person can see (teams' per-member project access).
- The Admin area requires `ADMIN`.

You can combine SSO with local auth. Set `localAuthEnabled = false` (see [Authentication](/en/authentication.html)) to make SSO the only way in.

## Troubleshooting

- **`authorization_request_not_found`:** almost always a proxy or tunnel dropping session state. Hinata already stores it in Mongo. Make sure you run a current build and your reverse proxy forwards the callback path untouched.
- **Redirect URI mismatch:** compare the URI registered at the IdP with your public API base, character for character.
- **SAML "assertion expired":** clock skew. Fix NTP on the server host.
- **No providers on the login screen:** check that the provider is enabled and the app can reach `/api/v1/auth/sso/providers` (public, no token required).

## Where to go next

- **[Authentication](/en/authentication.html):** local credentials, 2FA and the AuthPolicy flags you pair with SSO.
- **[Security model](/en/security.html):** how tokens, headers and rate limiting protect the whole surface.
- **[Reverse proxy & TLS](/en/reverse-proxy.html):** get the public host and forwarded headers right so callbacks land.
