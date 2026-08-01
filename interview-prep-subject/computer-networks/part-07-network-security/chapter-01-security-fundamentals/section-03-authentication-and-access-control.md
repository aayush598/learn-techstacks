# Authentication and Access Control

> **TL;DR**: Authentication proves *who* a user is (factors + MFA), authorization decides *what* they may do (RBAC/ABAC/ACLs), and the two are joined by sessions and identity protocols — OAuth 2.0/OIDC for delegated API access, SAML for enterprise SSO — with secure password storage, tokens, and least privilege as the operational backbone.

## 1. Why Does This Exist?
Every request an API receives asks two questions: "who is this?" and "what are they allowed to do?" — authentication and authorization. Without them, any caller could read/modify any resource (a single wrong answer = total compromise). Authentication exists because identity must be *proven*, not claimed: passwords, biometrics, hardware keys, certificates. Authorization exists because *proof of identity is not proof of permission*: knowing who you are doesn't mean you may delete the database. The two need a *state* mechanism (sessions, tokens) and a *federation* mechanism so you don't re-implement identity per app (OAuth/OIDC/SAML). This chapter's tools are the practical surface of the CIA/AAA goals (Section 01) and the cryptographic primitives (Section 02): authentication authenticates, authorization authorizes, and both rely on safe key/password handling.

## 2. How Does It Work?
**Authentication factors**: something you know (password), something you have (TOTP app, hardware key, phone), something you are (biometrics). **MFA** combines ≥2 factors. Passwords are verified against *salted slow hashes* (never plaintext). On success, the server issues a **session** (cookie/session ID stored server-side) or a **token** (JWT — self-contained, stateless, signed). **Authorization** then consults policies: **RBAC** (roles → permissions), **ABAC** (attributes/policies), **ACLs**. **Delegation/federation**: **OAuth 2.0** lets a third-party app get an access token (authorization code/pkce grant) without the user's password; **OIDC** (OAuth + ID token) adds user identity; **SAML** does enterprise SSO with XML assertions; **SAML/WS-Fed** for classic enterprise.

## 3. When Is It Used?
- **Every login flow**: passwords + MFA, sessions/cookies, "remember me."
- **API security**: bearer tokens, JWT, API keys, mTLS for service-to-service.
- **Enterprise SSO**: SAML/OIDC with Okta/Azure AD/Google Workspace; SAML in legacy corporate apps, OIDC in modern/SaaS.
- **Third-party delegation**: "Login with Google/Apple/GitHub" (OAuth), OAuth for apps acting on your behalf (calendar, storage).
- **Cloud IAM**: AWS IAM (policies = ABAC/JSON), GCP IAM, Azure RBAC — authorization at planet scale.
- **Service identity**: mTLS, SPIFFE/SPIRE, Kubernetes service accounts — machine-to-machine authn.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: trust the client's claim (send role in a cookie, no signature).* Catastrophically insecure — clients forge it. Tokens/sessions must be *signed* (JWT) or *server-side* (session ID) — the distinction between "client trust" and "cryptographic trust."
- *Alternative: passwords only, no MFA.* Passwords are phishable, reusable, crackable — single-factor is the #1 breach vector (credential stuffing). MFA (especially FIDO2/WebAuthn) resists phishing and reuse.
- *Alternative: stateless everything (JWT only).* JWTs are great (no DB lookup) but *can't be revoked* until expiry and bloat every request; sessions are revocable but need state. Real systems mix: short-lived tokens + refresh tokens + revocation lists.
- *Alternative: one global role table (RBAC-only).* Roles are coarse (a "staff" role grants too much); ABAC with attributes (resource, action, context) is finer but more complex. Modern clouds use hybrid: RBAC for humans, ABAC-style policies for resources.
- *Alternative: build identity per app.* Security-by-obscurity and inconsistent security; federation (OAuth/OIDC/SAML) centralizes authn, gives single sign-on, and separates "who" (IdP) from "what" (SP/RP) — the standard is decentralized identity.

## 5. Intuition
Authentication is the **bouncer checking ID** at the club door; authorization is the **seat map** telling you where you can sit. The ID proves who you are; the seat map defines what you can do. MFA is the bouncer requiring *two* proofs (ID + fingerprint + key card). Sessions are your **wristband** for the night — it proves you already got past the bouncer without showing ID every time. OAuth is **valet parking**: you give the valet (third-party app) a token to move *your* car only for a short time — not your house keys. RBAC is "VIP/backstage/general" passes; ABAC is the fine print ("only if you're over 18 and it's before 11 PM").

## 6. Real-World Analogy
An **airport**. Authentication = check-in and ID verification (password) + passport (MFA/hardware key). Authorization = your boarding pass zone (economy vs lounge) and visa (resource permissions). Sessions = the boarding pass that lets you move through without re-checking ID at every gate. OAuth = the travel agent given a *limited power of attorney* to rebook your flights (a scoped token) — not your passport. SAML/OIDC = the shared lounge network where one identity (your frequent-flier account) is accepted across many airlines (SSO).

## 7. Formal Definition
- **Authentication**: verifying a claimed identity by ≥1 factor: knowledge (password), possession (OTP/hardware key/certificate), inherence (biometric), plus context (location/device). **MFA** = ≥2 independent factors.
- **Authorization**: determining permitted actions on resources per policy — **RBAC** (role → permission set), **ABAC** (policies over subject/object/action/context attributes), **DAC/MAC** (classic discretionary/mandatory), **ACLs**.
- **Session**: server-side state keyed by a session ID (cookie), revocable.
- **JWT** (RFC 7519): signed, self-contained claims (header.payload.signature); stateless; bearer semantics.
- **OAuth 2.0** (RFC 6749): authorization framework — resource owner grants a client delegated access via **authorization code** (+ **PKCE**, RFC 7636) or **client credentials**; **refresh tokens** renew access tokens; **scopes** bound permissions.
- **OIDC** (OpenID Connect): OAuth 2.0 + an **ID token** (JWT) asserting identity → SSO + delegation.
- **SAML 2.0**: XML-based SSO; IdP issues assertions to SPs; enterprise classic.
- **Identity lifecycle**: provisioning/deprovisioning, rotation, revocation.

## 8. Example
**OAuth 2.0 authorization code + PKCE flow (Google login for a mobile app):**
1. App sends user to Google's authorization endpoint with `code_challenge` (PKCE) + requested scopes.
2. User authenticates at Google (password + MFA); Google redirects back with an authorization **code**.
3. App exchanges code + `code_verifier` for an **access token** (short-lived, e.g., 1 h) and a **refresh token** (long-lived).
4. App calls Google APIs with `Authorization: Bearer <access_token>`; Google checks token signature, expiry, scope.
5. Access token expires → app uses refresh token (+ client auth) for a new one — without re-asking the user.
The user's password never touched the app — *delegation without exposure*.

**RBAC vs ABAC:**
- RBAC: `role = "admin" → permissions {create_user, delete_user, read_all}`.
- ABAC: policy `allow if subject.group == "finance" AND resource.type == "report" AND action == "read" AND context.time within 09:00-18:00`.

## 9. Internal Working
1. **Password auth**: look up user → fetch salt → compute `argon2(salt, input)` → constant-time compare → issue session/token. Timing-safe comparison defeats side-channel guessing.
2. **Session store**: session ID in cookie (HttpOnly, Secure, SameSite) → server maps to user + expiry → revocable by deleting.
3. **JWT**: signed with server key (HS256 shared / RS256 private); verified on every request (no DB); trade-offs: can't revoke pre-expiry, size, key rotation.
4. **OAuth authorization server**: tracks clients, scopes, codes, tokens; issues access tokens (JWT or opaque); refresh tokens rotated; PKCE binds the code to the app (mobile/native).
5. **OIDC**: adds the ID token — claims (sub, email, name, nonce) the RP verifies against the JWKS (public keys) — establishing *who* while OAuth establishes *access*.
6. **RBAC enforcement**: middleware maps token → roles → permission set → route/action check; ABAC engines evaluate attribute policies (Open Policy Agent/Rego, AWS Cedar).
7. **mTLS/machine identity**: each service holds a cert; TLS client-auth proves identity; SPIFFE issues short-lived service identities.

## 10. Time Complexity / Performance
- **Password verify**: argon2 ≈ 0.1-1 s (deliberately slow, DoS-relevant — protect with rate limiting/captcha).
- **JWT verify**: one HMAC/RSA verify ≈ µs; **stateless** (no DB hit) → scales horizontally trivially.
- **Session lookup**: one DB/redis read (ms) — the cost of revocability.
- **OAuth**: few HTTP round trips (code→token) + token verification per request.
- **Access control check**: RBAC O(1) map lookup; ABAC policy evaluation O(policy size) — optimized engines handle millions of authz/s (AWS uses Cedar at scale).
- The design tension: stateless (JWT, fast, unrevocable) vs stateful (session, revocable, DB-bound).

## 11. Advantages
- **MFA**: dramatically raises cost of account takeover; FIDO2/WebAuthn resists phishing outright.
- **Sessions**: simple, revocable, server-controlled, no signing-key management for clients.
- **JWT**: stateless (scalable), self-contained (services verify without central auth), standard (RFC 7519), fine-grained claims.
- **OAuth 2.0 + PKCE**: delegation without password sharing; scopes give least privilege; refresh tokens balance UX and security.
- **OIDC/SAML**: single sign-on, centralized identity/security policy, separation of IdP from app.
- **RBAC/ABAC**: manageable permission modeling; ABAC scales to fine-grained, context-aware policies.

## 12. Disadvantages
- **Passwords**: weakest factor — phishable, reusable, crackable; MFA mandatory in 2020s.
- **JWT**: unrevocable before expiry; token theft = impersonation until expiry; payload size; key-rotation complexity.
- **OAuth**: complex spec, many grant types → misconfig (redirect URI attacks, scope over-grant, client-secret leaks).
- **SAML**: heavyweight XML, signature parsing vulnerabilities (XXE, key confusion), slower to modernize.
- **RBAC**: role explosion / coarse grants; ABAC: complexity, performance, governance.
- **Sessions**: server state = scaling + storage + revocation dependency.

## 13. Interview Questions
1. **Q: What's the difference between authentication and authorization?** A: Authentication = proving who you are (password/MFA/cert). Authorization = what you may do (roles/policies/ACLs). Authn precedes authz: proving identity grants nothing by itself — you still need permission for each action.

2. **Q: What are the authentication factors and what is MFA?** A: Knowledge (password/PIN), possession (phone, TOTP, hardware key), inherence (biometric), plus context (location/device). MFA = two or more *independent* factors, so compromising one doesn't break in.

3. **Q: How do you securely store passwords?** A: Never plaintext; per-user random salt + memory-hard KDF (argon2id/bcrypt/scrypt) tuned ~0.1-1 s; constant-time comparison; rate-limit the login endpoint to slow brute force. Plain/fast hashes (MD5/SHA-256 unsalted) are crackable instantly.

4. **Q: What's the difference between a session and a JWT?** A: Session = server-side state keyed by an opaque session ID (revocable, needs storage). JWT = self-contained signed token (stateless, verifiable without storage, but unrevocable until expiry). Choose by revocability vs scale; many systems use JWT + short expiry + refresh tokens.

5. **Q: How does OAuth 2.0 differ from OIDC?** A: OAuth 2.0 is an *authorization* framework — issues access tokens for APIs (delegation, scopes). OIDC builds on OAuth and adds an *ID token* (JWT with identity claims) — giving authentication/SSO on top. "OAuth for identity" without OIDC is a common mistake.

6. **Q: What is the authorization code flow with PKCE and why does PKCE exist?** A: App → auth server (user logs in) → redirect with a code → app exchanges code + PKCE verifier for tokens. PKCE (RFC 7636) binds the code to the requesting app via a one-time challenge — preventing code interception/authorization-code-swap attacks in native/mobile clients (no client secret can be kept safe there).

7. **Q: TRICKY — Your mobile app stores an OAuth client secret. What's wrong?** A: A native client can't keep secrets — the secret is extractable from the app binary. Native/mobile flows must use PKCE and *no client secret* (public clients); confidential secrets belong only in server-side daemons (client credentials grant).

8. **Q: What is the difference between an access token and a refresh token?** A: Access token: short-lived (minutes-hours), used on each API call, carries scopes. Refresh token: long-lived, used *only* to mint new access tokens, stored safely (HttpOnly/secure store), can be rotated/revoked. This split bounds token-theft exposure.

9. **Q: SCENARIO — A stolen JWT is being used to impersonate a user. How do you respond?** A: JWTs are unrevocable until expiry — so (1) rotate the signing key (kills all tokens), (2) add a token-version/jti denylist at the gateway, (3) shorten access-token TTL, (4) force re-auth + revoke refresh tokens, and (5) use rotating refresh tokens. The lesson: design for revocation even with stateless tokens.

10. **Q: What is SSO and how does SAML differ from OIDC?** A: SSO = one login across many apps via a central IdP. SAML: XML assertion-based, enterprise legacy, heavy. OIDC: JWT-based, modern, REST-friendly, web+native+mobile. Both federate identity; OIDC is the strategic direction, SAML persists in large enterprises.

11. **Q: PRODUCTION — Why does your service need mTLS for service-to-service calls?** A: Bearer tokens can leak (logs, caches) and don't establish *cryptographic* identity; mTLS authenticates both sides with certs — TLS client-auth proves the caller's identity at the transport layer, and short-lived machine certs (SPIFFE) bound identity and rotate automatically. This is how Kubernetes/Cloud runbooks and Zero Trust service meshes authenticate.

12. **Q: What is RBAC and when does it fail?** A: RBAC = permissions attached to roles, users get roles. It fails when roles are too coarse ("admin or nothing"), roles proliferate, or context matters (time/location/resource type) — then ABAC (attribute policies) or RBAC+ABAC hybrid is needed.

13. **Q: What is ABAC and give a policy example?** A: ABAC evaluates policies over attributes (subject, resource, action, context) — e.g., "allow if subject.role == auditor AND resource.region == EU AND action == read AND context.device == managed." It's expressive but needs policy engines (OPA/Cedar) and governance.

14. **Q: TRICKY — Why is a signed cookie/JWT not enough to make an API "authenticated"?** A: A valid signature proves *issuance* by the right key but says nothing about whether that token was stolen and replayed. You also need expiry, audience, issuer checks, and ideally revocation/denylist — and the API must verify ALL claims, not just the signature. Signing ≠ authorization.

15. **Q: SCENARIO — You log in and your session cookie is missing the `Secure` and `HttpOnly` flags. What attacks does that enable?** A: `HttpOnly` missing → XSS can read the cookie (session hijack). `Secure` missing → cookie sent over plain HTTP (sniffing). `SameSite` missing → CSRF. Defense: HttpOnly + Secure + SameSite=Lax/Strict + short expiry + rotation on privilege change.

16. **Q: What is a credential-stuffing attack and the best defense?** A: Attackers reuse leaked username/password pairs from other breaches. Defense: MFA (kills most stuffing), breach-list checking at signup/login, anomaly detection (impossible travel, new device), and rate limiting — no password policy alone stops it.

17. **Q: PRODUCTION — Design auth for a public API that third parties call.** A: (1) Issue scoped access tokens (OAuth2 client credentials/authorization code + PKCE); (2) short TTLs + rotating refresh tokens; (3) per-client rate limits + quotas; (4) request signing or mTLS for high-assurance clients; (5) audit logging + token revocation; (6) JWKS so clients verify signatures. Least privilege via scopes.

18. **Q: What is the "audience" claim in a JWT and why does it matter?** A: `aud` declares which recipient the token is for; a verifier must check it matches *its own* identifier — otherwise a token minted for another service is accepted (token confusion attack). `iss`, `aud`, `exp`, `nbf`, `iat` are the mandatory validation set.

## 14. Follow-Up Questions
1. **Q: What is WebAuthn/FIDO2 and why is it considered phishing-resistant?** A: It uses public-key cryptography with a hardware authenticator; the credential is bound to the *origin* (site), so a fake site can't replay it — even a perfect phishing page can't produce the signature. It also removes shared secrets entirely.

2. **Q: How does constant-time comparison work and why is it needed?** A: Compare hash digests byte-by-byte without early-exit (`hmac.compare_digest`), so timing doesn't leak how many prefix bytes matched — preventing an attacker from guessing the digest incrementally.

3. **Q: What is the OAuth "redirect URI" attack?** A: An attacker registers a malicious redirect URI; if the server doesn't strictly validate registered URIs, the authorization code is sent to the attacker's URL (code interception). Fix: exact-match allowlist of redirect URIs.

4. **Q: What's the difference between a bearer token and a proof-of-possession (DPoP) token?** A: Bearer: whoever holds it is authorized (theft = takeover). DPoP: the token is bound to a client key via a proof of possession — stealing the token alone isn't enough. mTLS is the transport-level proof-of-possession.

## 15. Coding Example
```python
import hashlib, hmac, os, time

def verify_password(password: str, salt_hex: str, hash_hex: str, iterations=600_000) -> bool:
    salt = bytes.fromhex(salt_hex)
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return hmac.compare_digest(candidate.hex(), hash_hex)   # constant-time

salt = os.urandom(16).hex()
h = hashlib.pbkdf2_hmac("sha256", b"correct horse", bytes.fromhex(salt), 600_000).hex()
print("auth ok:", verify_password("correct horse", salt, h))
print("auth bad:", verify_password("wrong", salt, h))
```
```python
# Minimal RBAC check + JWT-style claims (conceptual; use PyJWT in production)
ROLES = {"admin": {"user:read", "user:write", "billing:read"},
         "user":  {"user:read"}}

def can(role: str, permission: str) -> bool:
    return permission in ROLES.get(role, set())

print(can("admin", "billing:read"), can("user", "billing:read"))

def build_token(claims, secret):
    import json, base64
    header = base64.urlsafe_b64encode(b'{"alg":"HS256"}').decode().rstrip("=")
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    sig = base64.urlsafe_b64encode(hmac.new(secret.encode(), f"{header}.{body}".encode(),
                                            hashlib.sha256).digest()).decode().rstrip("=")
    return f"{header}.{body}.{sig}"

t = build_token({"sub": "u1", "role": "admin", "exp": int(time.time()) + 600}, "k")
print("JWT:", t[:40] + "...")
```
```bash
# Inspect real authentication/authorization in production
curl -sI https://github.com/login | grep -i set-cookie          # HttpOnly/Secure/SameSite flags
curl -s https://login.microsoftonline.com/.well-known/openid-configuration | python3 -m json.tool | head -20
curl -s https://accounts.google.com/.well-known/openid-configuration | python3 -m json.tool | grep -E "issuer|authorization_endpoint|jwks"
# OIDC public keys (JWKS) for token verification:
curl -s https://www.googleapis.com/oauth2/v3/certs | python3 -m json.tool | head -15
# Local password policy (auth.log):
sudo journalctl -u sshd | grep "Failed password" | wc -l
sudo faillock --user aayush; sudo pam-auth-update   # account lockout (MFA/rate-limit analog)
```

## 16. Industry Usage
- **Cloud IAM**: AWS IAM (Cedar/ABAC-style policies), GCP IAM (roles), Azure RBAC — the biggest authorization deployments.
- **Enterprise SSO**: Okta, Azure AD/Entra ID, Google Workspace via OIDC/SAML — most large companies federate.
- **Consumer auth**: Google/Apple/GitHub sign-in (OAuth/OIDC), FIDO2 passkeys (Apple/Google/Microsoft), TOTP/MFA everywhere.
- **Service mesh/zero trust**: Istio/Linkerd mTLS + SPIFFE identities; Google BeyondCorp and Cloudflare Access = zero-trust identity-aware access (Section 05 of ch-02).
- **Developer platforms**: GitHub fine-grained PATs (scopes), Stripe API keys, Twilio — all OAuth-style scoped tokens.
- **Kubernetes**: service accounts (JWTs), RBAC, OIDC for human users — the standard multi-identity runtime.

## 17. References
- RFC 6749 (OAuth 2.0) — https://datatracker.ietf.org/doc/html/rfc6749
- RFC 7636 (PKCE) — https://datatracker.ietf.org/doc/html/rfc7636
- OpenID Connect Core 1.0 — https://openid.net/specs/openid-connect-core-1_0.html
- RFC 7519 (JWT) — https://datatracker.ietf.org/doc/html/rfc7519
- SAML 2.0 (OASIS) — https://docs.oasis-open.org/security/saml/v2.0/
- OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- WebAuthn/FIDO2 (W3C) — https://www.w3.org/TR/webauthn-2/

## 18. Cheat Sheet
- Authn = who (password/MFA/cert); Authz = what (RBAC/ABAC/ACL); never conflate.
- Factors: know / have / are (+ context); MFA = ≥2 independent.
- Passwords: salt + argon2/bcrypt; constant-time compare; rate limit login.
- Session = server state (revocable); JWT = signed stateless (unrevocable until expiry).
- OAuth 2.0 = authorization (access tokens, scopes); OIDC = + identity (ID token). PKCE for native apps.
- Access token short-lived; refresh token long-lived + rotated + revocable.
- JWT must validate iss, aud, exp, nbf — signature alone is not authorization.
- RBAC roles→perms; ABAC attribute policies (OPA/Cedar); hybrid for real clouds.
- mTLS/SPIFFE = machine identity; WebAuthn = phishing-resistant human auth.
- Secure cookies: HttpOnly + Secure + SameSite + rotation.

## 19. Quiz
1. Authentication answers: a) what can you do b) who are you c) where are you d) when → **b**
2. MFA requires: a) password + email b) ≥2 independent factors c) 2 passwords d) biometric only → **b**
3. JWT is: a) server-side state b) signed stateless token c) a session cookie d) a password → **b**
4. OAuth 2.0 provides: a) identity b) authorization/delegation c) encryption d) hashing → **b**
5. OIDC adds to OAuth: a) refresh tokens b) an ID token c) scopes d) PKCE → **b**
6. PKCE prevents: a) brute force b) authorization-code interception c) XSS d) DDoS → **b**
7. RBAC means: a) role→permission mapping b) attribute policies c) ACLs d) MFA → **a**
8. A cookie with HttpOnly protects against: a) CSRF b) XSS reading it c) sniffing d) brute force → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-a, 8-b.

## 20. Flashcards
- **Q: Authn vs authz?** → **A:** Who you are (factors/MFA) vs what you can do (RBAC/ABAC/ACL).
- **Q: How to store passwords?** → **A:** Salt + memory-hard KDF (argon2/bcrypt), constant-time compare, rate-limit login.
- **Q: Session vs JWT?** → **A:** Revocable server state vs signed stateless token (unrevocable until expiry).
- **Q: OAuth vs OIDC?** → **A:** OAuth = access tokens/delegation; OIDC = + ID token identity (SSO).
- **Q: Why PKCE?** → **A:** Binds the auth code to the app; blocks code interception in native clients.
- **Q: Access vs refresh token?** → **A:** Short-lived per-request vs long-lived, rotated, revocation-able token minting new access tokens.
- **Q: What must a verifier check in a JWT?** → **A:** iss, aud, exp, nbf, signature — not just the signature.

## 21. Revision
Authentication proves identity (knowledge/password, possession/TOTP/hardware, inherence/biometric → MFA); authorization grants actions (RBAC roles→perms, ABAC attribute policies, ACLs). Passwords are stored as salted slow hashes (argon2/bcrypt) with constant-time compare. State: sessions (revocable server state) vs JWTs (signed stateless, validate iss/aud/exp). Delegation: OAuth 2.0 (access tokens, scopes, PKCE for native) + OIDC (ID token → SSO); SAML for enterprise legacy. Machine identity via mTLS/SPIFFE; phishing-resistant human auth via WebAuthn. Cookie hardening: HttpOnly + Secure + SameSite. Anchor: *"who" (authn) is proven with factors and tokens; "what" (authz) is granted by roles/policies; the two must be enforced separately and by the server, never trusted from the client.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Authentication vs authorization" | 13-Q1 / 7 |
| "Factors and MFA" | 13-Q2 |
| "How do you store passwords?" | 13-Q3 / 8 |
| "Session vs JWT trade-offs" | 13-Q4 / 9 |
| "OAuth vs OIDC" | 13-Q5 |
| "Authorization code + PKCE flow" | 8 / 13-Q6,7 |
| "Access vs refresh token" | 13-Q8 |
| "Stolen JWT — how to respond?" | 13-Q9 |
| "SAML vs OIDC / SSO" | 13-Q10 |
| "mTLS / machine identity" | 13-Q11 |
| "RBAC vs ABAC" | 13-Q12,13 |
| "Cookie flags / XSS session hijack" | 13-Q15 |
| "Design auth for a public API" | 13-Q17 |
