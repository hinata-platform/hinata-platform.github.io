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

A first SSO login provisions a Hinata user. After that the usual model applies:

- Project and team membership decide what the person can see (teams' per-member project access).
- The Admin area requires `ADMIN`.

You can combine SSO with local auth. Set `localAuthEnabled = false` (see [Authentication](/en/authentication.html)) to make SSO the only way in.

### How a sign-in finds its account

Hinata binds every account to the identifier the provider itself gives the person, not to the email address. With many providers people can change their address in their own profile or pick any address when they register. The identifier is the provider's.

| Method | Identifier | Name of the provider |
| --- | --- | --- |
| OpenID Connect | `sub` | Issuer URI |
| OAuth 2.0 | `sub` or `id` from the user info, otherwise the configured name attribute | Host of the authorization URL |
| SAML 2.0 | NameID | Entity ID of the IdP |
| LDAP | `entryUUID` or `objectGUID` of the entry, otherwise its DN | Base DN |

If an account holds this identifier at the same provider, the sign-in goes into that account, even when the address at the provider has changed since. If no account has the address yet, Hinata creates one and binds it to the identifier right away. If the provider sends no address at all, Hinata creates no account.

If an account has the address but is not bound to this identifier, the address decides in three cases only, and the account is bound then.

- The account was created through the same method and is not bound yet. OpenID Connect and OAuth 2.0 count as one method here. This applies to every SSO account from before binding, exactly once, at its first sign-in since.
- The account is bound through the same provider, whose name has changed (right-hand column). Hinata takes that as a switch of identity provider and binds the accounts again at their next sign-in. Another address for the same provider, such as `ldaps` instead of `ldap` or another path for OAuth 2.0, is no switch.
- It is a local account, and local sign-in is off. SSO is the only way in then.

Even then: if the provider itself says it has not confirmed the address (`email_verified` is `false`), the address binds no existing account. The person still gets a new account, as there is nothing in it yet. And only a sign-in that gets in binds: an account that is deactivated, waiting for approval or an open invitation stays unbound.

Hinata refuses everything else. Whoever only gives the address learns nothing about the account behind it, so not whether it is deactivated or an invitation is open either. The audit log has the exact reason. A local account with a password is reachable over SSO only while local sign-in is off; otherwise the person signs in with their password.

Every refusal is in the audit log, and so is every binding of an existing account by its address, even when that event is switched off in the audit settings. The person also gets a security notification naming the provider and the name somebody signed in with there. If it was not them, they hear about it right away.

Every way in follows the same rules as a password sign-in: a deactivated account, or one still waiting for approval, gets no access over SSO either.

!!! warning "An identifier that is the address does not protect"
    If the provider's identifier is the email address, the binding depends on the address again. That happens with a SAML NameID in email format, and with OAuth 2.0 when the provider sends neither `sub` nor `id` and the name attribute is `email` (the default). Hinata logs a warning on the server. Use the `persistent` NameID for SAML and a stable name attribute such as `id` for OAuth 2.0. A `transient` NameID changes with every sign-in; the person would not get in after the first time.

### Invitations with SSO

If the server has SSO, an invited person can accept the invitation with SSO too. The invitation page then offers "Join with ‹provider›". The sign-in carries the invitation along, and the link from the invitation email proves the address. Hinata completes the invitation with it and binds the account to the identifier, even when the provider knows the person under another address. The roles from the invitation stay.

With local sign-in off, that is the only way. No password can be set then: nobody could sign in with it, and the account would stay unbound until the first SSO sign-in with its address. Nobody completes an invitation by its address alone.

### When the identifier changes

If the provider renames an account or changes the NameID, the person no longer gets into their Hinata account. Under Admin area › Users › person, "Disconnect SSO sign-in" removes the binding. All of the person's sessions end with it. The next SSO sign-in with the address may then bind the account again, whichever account at the provider it comes from. So only do this when you are sure the right person signs in next. Hinata always records the removal, even when the event is switched off in the audit settings.

### After the update that brings the binding

On its first start Hinata signs out, once, everybody who was reachable by their address alone before. With any SSO method or LDAP on, or local sign-in off, that is every account: which account such a sign-in entered is known only from the audit log, which can be switched off and forgets after a year. With all of them off, it is every account created through SSO or LDAP, and every account the audit log shows an SSO sign-in for. Whoever signs in afterwards binds their account to themselves. Best announce the update beforehand.

At their first sign-in after it, SSO accounts from before the binding get a security notification that their account was connected. Everybody else gets the usual notification about a sign-in from a new device.

!!! warning "Check `email_verified` first"
    If your provider sends `email_verified: false` for your people, Hinata does not bind their accounts from before the binding, and they no longer get in. Keycloak does that, for instance, for everybody from an LDAP federation while "Trust Email" is off there, and for people an admin created without "Email verified". Change that at the provider before the update.

Personal access tokens and connected AI clients stay. Check the audit log of accounts with SSO sign-ins for tokens or grants the person does not know about, and revoke them if needed.

## Troubleshooting

- **`authorization_request_not_found`:** almost always a proxy or tunnel dropping session state. Hinata already stores it in Mongo. Make sure you run a current build and your reverse proxy forwards the callback path untouched.
- **Redirect URI mismatch:** compare the URI registered at the IdP with your public API base, character for character.
- **SAML "assertion expired":** clock skew. Fix NTP on the server host.
- **No providers on the login screen:** check that the provider is enabled and the app can reach `/api/v1/auth/sso/providers` (public, no token required).
- **"There is already an account with this email address that is not connected to this sign-in":** the account is local, it was created through another method (SAML instead of OIDC, say), it is bound to another identifier at the provider, or it is deactivated, waiting for approval or an open invitation. The audit log names the reason in its `LOGIN_FAILURE` entry. Local accounts sign in with their password, invited people through the link in their invitation. If the person's identifier changed, disconnect the SSO sign-in as described above.
- **"Your sign-in service reports this email address as unconfirmed":** the provider sends `email_verified: false`, and an account with the address exists already. Have the address confirmed at the provider, or let the provider trust its addresses (Keycloak: "Trust Email" in the LDAP federation).
- **"Your sign-in service did not send an email address":** the provider sends no address attribute, or the configured attribute holds no address. Check the method's attribute mapping in the admin area.

## Where to go next

- **[Authentication](/en/authentication.html):** local credentials, 2FA and the AuthPolicy flags you pair with SSO.
- **[Security model](/en/security.html):** how tokens, headers and rate limiting protect the whole surface.
- **[Reverse proxy & TLS](/en/reverse-proxy.html):** get the public host and forwarded headers right so callbacks land.
