# Cookies, Sessions, and Authentication

> **TL;DR**: HTTP is stateless, so cookies (client-side tokens), sessions (server-side state keyed by an ID), and authentication headers/tokens (Bearer/JWT/OAuth) exist to give the stateless protocol *identity, state, and authorization* — each is a different place to put state, with different security properties.

## 1. Why Does This Exist?
Every real product needs to know *who you are* (authentication), *what you can do* (authorization), and *what you were doing* (state — cart, session, preferences). HTTP's statelessness means each request arrives with no memory. The answer: **state must be stored somewhere** — and the design question is *where*: on the client (cookies, JWTs), on the server (session stores), or in a mix. Cookies exist because browsers needed a sanctioned way for servers to attach state to the client; sessions exist because cookies alone are visible/forgeable; tokens exist because APIs (non-browser clients) needed a standard credential format. This triad is the basis of login on the entire web.

## 2. How Does It Work?
- **Cookies**: the server sends `Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Lax`; the browser stores it (keyed by domain/path) and sends it back as `Cookie: session_id=abc123` on every subsequent request. Cookie attributes: `Expires/Max-Age`, `Domain`, `Path`, `Secure` (HTTPS only), `HttpOnly` (invisible to JS → blocks XSS cookie theft), `SameSite` (Lax/Strict/None — CSRF protection).
- **Sessions**: the cookie holds only a random **session ID**; the server maps `session_id → data` in a store (in-memory, Redis, DB). The ID is opaque, unpredictable, and its *value alone is useless* — the state lives server-side. Session fixation/logout/invalidation are server-controlled.
- **Authentication (credentials)**: the client proves identity each request via headers or cookies:
  - **Basic Auth**: `Authorization: Basic base64(user:pass)` (weak; TLS-only).
  - **Bearer tokens**: `Authorization: Bearer <token>` — opaque (server-side session token) or self-contained (JWT).
  - **JWT**: a signed JSON claim set (`header.payload.signature`) — stateless auth: the server verifies the signature (HMAC or RSA/ECDSA) instead of looking up a session. No server storage.
  - **OAuth 2.0 / OIDC**: delegated authorization — a third-party identity provider (Google, GitHub) issues tokens; scopes limit what they can do.
- **Security models**: XSS (steal cookies → session hijack), CSRF (forge authenticated requests), fixation, token theft.

## 3. When Is It Used?
- **Cookies + sessions**: classic web logins (server-rendered apps, traditional session-based auth) — Django, Rails, PHP apps.
- **JWT / Bearer**: **API authentication** — SPAs, mobile apps, microservices (no server-side session store to scale), auth services (Auth0, Clerk, AWS Cognito).
- **OAuth2/OIDC**: "Sign in with Google/GitHub", delegated access to APIs (scope-limited), enterprise SSO.
- **mTLS**: service-to-service (covered in TLS section) — certificate-based identity.
- **Cookies for non-auth state**: preferences, A/B testing buckets, tracking/analytics, CSRF tokens themselves.

## 4. Why Wasn't Another Approach Chosen?
- **Why cookies (client storage) vs server storing *everything*?** If all state were server-side, the server would need a key per client anyway — cookies provide the *standard browser mechanism* for carrying that key. Also, some state is inherently client-side (preferences). But cookies are visible/inspectable → don't put secrets in them.
- **Why server sessions vs just signing everything (JWT)?** Sessions are revocable (logout, kill a session), don't leak data to the client, and are simpler to invalidate. They need a store (scale + latency). JWTs are stateless (scale out without a session DB) but **cannot be revoked** (until expiry) and can be decoded (don't put secrets in them). Choice depends on: revocation needs vs. stateless scale.
- **Why Bearer tokens vs Basic auth per request?** Basic sends the password every request (replay risk, no scoping). Bearer tokens are scoped, revocable, short-lived, and don't require re-prompting credentials. JWT vs opaque: JWT carries claims (self-describing) but is bigger; opaque is a DB lookup but tiny and instantly revocable.
- **Why OAuth 2.0 vs letting apps store passwords?** Never share credentials with third parties. OAuth issues *scoped, revocable* tokens without exposing the password — the standard for delegated access.

## 5. Intuition
- **Cookie** = a **sticky note the server sticks to your browser**; every time you visit, the browser shows it ("I am session #abc123").
- **Session** = the **server's filing cabinet**: the sticky note says "look up drawer abc123" — the cabinet (server memory/Redis) holds your cart, login state, etc.
- **JWT** = a **signed ID card**: the card itself *contains* your name, role, expiry — anyone can read it, but only the issuer can sign it; you can't tamper with it without breaking the signature.
- **OAuth** = a **valet key**: Google issues you a special key that lets the app open only the specific doors (scopes) you allowed, and you can take it back anytime.

## 6. Real-World Analogy
**Hotel**: Checking in = login. The front desk gives you a **key card** (session cookie/token). The card has a room number but is useless on its own; the hotel's records (server session store) link it to your details. If you want to see your bill, you show the card (each request carries the credential). A **JWT** is like a *pre-printed room-pass* that already has your name + checkout date printed and is signed by the hotel manager's stamp (signature) — you can carry it anywhere without phoning the hotel, but you can't edit it, and if the manager wants to cancel your pass, they must wait for expiry unless they add a blocklist. **OAuth** = the valet ticket Google's garage issues that lets a third-party app move your car only within the agreed lot (scoped authorization), revocable anytime.

## 7. Formal Definition
- **Cookie** (RFC 6265): a small piece of state the server stores on the client via `Set-Cookie`, automatically returned in `Cookie` headers on matching domain/path, governed by attributes (`Secure`, `HttpOnly`, `SameSite`, `Domain`, `Path`, `Expires`/`Max-Age`).
- **Session**: a server-side association between a client (identified by a random, unguessable session ID, typically carried in a cookie) and server-stored state; the session is created at login, updated per request, and destroyed at logout/expiry.
- **Bearer token / JWT**: `Authorization: Bearer <token>`; a **JWT** (RFC 7519) is a compact, URL-safe, *signed* JSON object (`alg`, `claims`, `signature`) that encodes identity/authorization claims (subject, issuer, expiry, scopes); verified by the recipient using the issuer's key.
- **OAuth 2.0** (RFC 6749): an authorization framework issuing short-lived **access tokens** (and refresh tokens) with **scopes**, without sharing user credentials. **OpenID Connect (OIDC)** = OAuth 2.0 + an ID token for authentication.

## 8. Example
Login → authenticated request, both models:
**Session-based:**
```
Client -> Server: POST /login {user, pass}
Server: verify creds, create session {user_id, role}, store in Redis (key = sid=abc123xyz)
Server -> Client: Set-Cookie: sid=abc123xyz; HttpOnly; Secure; SameSite=Lax
Client -> Server (next request): Cookie: sid=abc123xyz
Server: sid exists in Redis → user=42, role=admin → serve
Logout: Server deletes Redis key → cookie now points nowhere (revoked instantly)
```
**JWT-based:**
```
Client -> Server: POST /login {user, pass}
Server: verify → sign JWT (header {alg: HS256}, claims {sub:42, role:admin, exp: 1h}, HMAC signature)
Server -> Client: {"access_token": "eyJhbGciOiJIUzI1NiIs...", "refresh_token": "..."}
Client -> Server (API): Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Server: verify signature (no DB lookup) → trust claims → serve
Revocation: can't un-sign a valid JWT → blocklist / short expiry (15 min) + refresh rotation
```

## 9. Internal Working
1. **Cookie storage**: browsers keep a cookie jar per domain; `Set-Cookie` writes; `Cookie` sends; 4 KB limit per cookie, ~50-180 per domain (browser-dependent). Third-party cookies = set by a different domain (tracking) — being phased out (Chrome).
2. **Session store**: Redis `SETEX sid user:42 TTL`; distributed sessions need sticky sessions *or* a shared store (Redis). Invalidation: logout deletes, idle timeout, absolute timeout.
3. **JWT verify**: split on `.` → base64url-decode header & payload → recompute signature with the shared secret (HMAC) or public key (RSA/ECDSA) → compare (constant-time) → check `exp`/`nbf`/`iss`/`aud`. Never trust a JWT without signature verification.
4. **Token lifecycle**: access token (short, minutes) + refresh token (long, revocable, rotating). On expiry → POST /token with refresh → new access token. Refresh tokens stored server-side (rotation + reuse detection) for security.
5. **Attack mitigations**:
   - **XSS** (malicious JS runs on your page): `HttpOnly` cookies (JS can't read them), CSP, input sanitization. JWT in localStorage is XSS-stealable → prefer cookies or memory for SPAs.
   - **CSRF** (attacker forges requests using your cookies): `SameSite=Lax/Strict`, CSRF tokens, `Origin`/`Referer` checks. Bearer tokens in headers aren't auto-sent → CSRF-resistant by design.
   - **Session fixation**: regenerate session ID at login.
   - **Replay**: TLS everywhere + short expiries.
6. **OAuth2 flows**: Authorization Code (PKCE) for SPAs; Client Credentials (machine-to-machine); Authorization Code + PKCE is the current standard for web/mobile.

## 10. Time Complexity
- **Session lookup**: O(1) Redis GET per request; adds 1 RTT (mitigate: local cache, cookie-based encryption (encrypted sessions) but that's stateless-with-cost).
- **JWT verification**: O(1) crypto (HMAC ~µs; RSA/ECDSA ~50-100 µs) — *no* storage lookup → horizontal scale without a shared store; but every request pays crypto CPU.
- **Token refresh**: rare (per 15-60 min) vs session GET (every request) — JWT trades lookup for occasional crypto.
- **Storage**: sessions need Redis/DB scale; JWTs are stateless (no DB for auth, but refresh-token store still needed).

## 11. Advantages
- **Cookies**: automatic browser handling (no JS code), domain-scoped, attributes for security, works for all browsing.
- **Sessions**: instantly revocable, server-controlled state, client can't read/modify, simple model, no crypto per request.
- **JWT**: stateless scale (no session store), self-contained claims (no lookup), works across services (microservices share the signing key), portable to non-browser clients.
- **OAuth2**: no credential sharing, scoped delegation, revocable, industry standard for third-party access.

## 12. Disadvantages
- **Cookies**: visible to client, 4 KB limit, CSRF surface (auto-sent), privacy/tracking baggage, third-party cookie restrictions.
- **Sessions**: server storage + lookup latency, sticky-session issues, scale cost, session-fixation risk if IDs are predictable.
- **JWT**: cannot revoke before expiry (blocklist needed), payload is readable (no secrets!), larger tokens, key management (signing key compromise = total break), no auto-logout, clock-skew issues with `exp`.
- **OAuth2**: complex flows (PKCE, refresh rotation), token storage security, provider dependency.

## 13. Interview Questions
1. **Q: Why does HTTP need cookies if it's stateless?** A: Statelessness means the *protocol* holds no memory, but applications need identity/state. Cookies are the browser's sanctioned mechanism to attach a stable token to requests so the server can identify and track a client across requests.
2. **Q: Difference between cookies and sessions?** A: Cookie = client-side token (may hold an ID or small data). Session = server-side state (data store) keyed by a session ID carried in a cookie. The cookie is the key to the session filing cabinet.
3. **Q (tricky): Is a cookie a security risk by itself?** A: No — the *contents* and *attributes* matter. A random session ID with HttpOnly+Secure+SameSite is safe; storing a password or user data in a cookie is not. Never put secrets or unverified data in cookies.
4. **Q: What do HttpOnly, Secure, SameSite do?** A: HttpOnly = JS can't read it (blocks XSS theft). Secure = only sent over HTTPS. SameSite (Lax/Strict/None) = controls cross-site sending (Lax/Strict block CSRF). All three are cookie-security defaults.
5. **Q: What is CSRF and how do you prevent it?** A: An attacker's site makes your browser send an authenticated request (cookies auto-attach) to a vulnerable site. Prevent: `SameSite=Lax/Strict`, CSRF tokens (server-issued per-session secret in a hidden field), Origin/Referer checks. Bearer-token APIs are CSRF-resistant (token not auto-sent).
6. **Q: What is XSS and how does it threaten auth?** A: Injected JS runs in your origin → can read localStorage/sessionStorage (JWT theft) and call APIs with your tokens. Mitigations: HttpOnly cookies (JS can't read), CSP, sanitize inputs, don't store tokens in JS-accessible storage.
7. **Q: JWT vs server-side session — which and why?** A: JWT: stateless scale, self-contained, no session store (great for microservices/APIs); but un-revocable, readable, key-managed. Sessions: instant revocation, server control, simpler security; but need a store + lookup. Choose by revocation needs and scale model.
8. **Q (production): How do you revoke a JWT before expiry?** A: You can't un-sign a valid signature. Options: (1) blocklist (deny-listed jti/expiry) in Redis, (2) short access-token TTL (10-15 min) + rotating refresh tokens, (3) if using OIDC, rely on IdP logout + token revocation endpoints. Best practice: short-lived access + revocable refresh.
9. **Q: What is the difference between authentication and authorization?** A: Authentication = who are you? (login, credentials, JWT `sub`). Authorization = what can you do? (roles, scopes, policies). A JWT carries both (claims: sub + role/scopes); OAuth2 is *authorization* (scopes), OIDC adds authentication (ID token).
10. **Q (scenario): SPA + mobile app + 3 backend microservices. Auth design?** A: OAuth2 Authorization Code + PKCE for both clients; short-lived access tokens (JWT, shared signing key or JWKS) so each service verifies without a central store; refresh tokens held by the IdP with rotation; HttpOnly cookie OR memory for the SPA token (avoid localStorage for XSS resistance). Add scope checks at each service.
11. **Q: What is OAuth 2.0 and what problem does it solve?** A: An authorization framework letting a third-party app get *scoped, revocable* access to a user's resources without the user sharing their password. Issued access tokens + refresh tokens; flows: Authorization Code (+PKCE), Client Credentials, etc.
12. **Q: What is PKCE and why is it needed for SPAs?** A: Proof Key for Code Exchange — the SPA sends a hashed random verifier at authorize time and proves possession at token time. Prevents authorization-code interception (the old "implicit flow" hole). Required for public clients (no secret).
13. **Q: What's in a JWT and why can't the client modify it?** A: `header.payload.signature` (base64url). Claims: sub (subject), iss, exp, nbf, aud, scopes. The signature (HMAC with server secret or RSA/ECDSA with private key) means any tampering breaks verification — the server (or any holder of the key) detects it.
14. **Q (tricky): Where should a SPA store a JWT?** A: Cookie (HttpOnly) → XSS-safe but CSRF must be handled; in-memory (module scope) → lost on refresh, XSS-safe-ish; localStorage → easiest but XSS-stealable. Industry lean: HttpOnly cookies or in-memory with refresh rotation; avoid localStorage for sensitive tokens.
15. **Q: How does session-based auth behave across multiple servers?** A: Sessions must live in a *shared* store (Redis) or use sticky load balancing (bad for resilience). JWTs sidestep it (stateless) — a key reason API-heavy architectures choose JWTs. Production: Redis-backed session store.
16. **Q: What is a refresh token and why rotate it?** A: A long-lived credential exchanged for new short-lived access tokens. Rotation: each refresh issues a *new* refresh token and invalidates the old — if an attacker steals a used token, reuse detection trips an alert. Best practice for token theft resistance.
17. **Q (production): Your API suddenly returns 401s for all users. Debug?** A: Check: signing key rotation (did you roll keys without JWKS update?), clock skew (JWT exp/nbf vs server time — NTP), token store/Redis outage (sessions), IdP downtime, and cookie domain/path changes. Standard: distributed auth debugging checklist.
18. **Q: What is the difference between SameSite=Lax and Strict?** A: Lax: cookies sent on top-level *navigations* (link clicks) but not on subresource/fetch cross-site requests — good UX, strong CSRF protection. Strict: never sent cross-site — stronger but breaks cross-site links (OAuth redirects may need None+Secure). Lax is the default (Chrome 80+).

## 14. Follow-Up Questions
1. **Q: What is a "session fixation" attack?** A: Attacker sets a known session ID for the victim (e.g., via a link), then hijacks it. Fix: regenerate the session ID on login (server-side) — never trust a pre-auth ID.
2. **Q: How does a CSRF token actually work?** A: Server embeds a random per-session secret in the form; on POST it verifies the token matches the session. Attacker's site can't read the token (same-origin policy) → forged request fails the check.
3. **Q: What is the "logout everywhere" problem with JWTs?** A: Stateless JWTs have no server record → revoking all of a user's sessions requires a blocklist or a "token version" claim (bump `v` to invalidate all). Opaque/session tokens handle this trivially (delete keys).
4. **Q: What is OpenID Connect vs OAuth 2.0?** A: OAuth2 = authorization (access tokens, scopes). OIDC = OAuth2 + an **ID token** (a signed JWT asserting *authentication*: who the user is). OIDC sits on top: "OAuth 2.0 for login."
5. **Q: Why are cookies limited to 4 KB and what if you need more?** A: Browser spec limit; for bigger state use session IDs (server-side data) rather than stuffing the cookie. If you must, chunk across cookies — but that's an anti-pattern; the real answer is "don't put large data in cookies."

## 15. Coding Example
```python
# Flask-style session + JWT auth, side by side
import hashlib, hmac, base64, json, time

# --- JWT (HMAC-SHA256), minimal ---
SECRET = b"super-secret-signing-key"
def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def jwt_encode(claims: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h = b64url(json.dumps(header).encode())
    p = b64url(json.dumps(claims).encode())
    sig = b64url(hmac.new(SECRET, f"{h}.{p}".encode(), hashlib.sha256).digest())
    return f"{h}.{p}.{sig}"

def jwt_verify(token: str) -> dict:
    h, p, sig = token.split(".")
    expected = b64url(hmac.new(SECRET, f"{h}.{p}".encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, expected):   # constant-time compare
        raise ValueError("bad signature")
    claims = json.loads(base64.urlsafe_b64decode(p + "=="))
    if claims["exp"] < time.time():
        raise ValueError("expired")
    return claims

claims = {"sub": "user-42", "role": "admin", "exp": int(time.time()) + 3600}
token = jwt_encode(claims)
print("JWT:", token)
print("Verified claims:", jwt_verify(token))

# --- Session store (Redis-style), conceptual ---
sessions = {}
def login(user):
    sid = "sid-" + str(abs(hash(user)))[:10]   # in reality: secrets.token_urlsafe(32)
    sessions[sid] = {"user": user, "login": time.time()}
    return sid

def authorize(request_cookie_sid):
    return sessions.get(request_cookie_sid)    # O(1) lookup, instantly revocable

sid = login("alice")
print("Session:", sid, "->", authorize(sid))   # {'user': 'alice', ...}
sessions.pop(sid, None)                        # logout = delete the key
print("After logout:", authorize(sid))         # None (revoked instantly)
```
```bash
# See cookies and tokens on the wire
$ curl -i -c cookies.txt https://example.com/login -d "user=alice&pass=x"
# Set-Cookie: sid=abc123; HttpOnly; Secure; SameSite=Lax
$ curl -b cookies.txt https://example.com/account     # sends Cookie: sid=abc123
$ curl -H "Authorization: Bearer $TOKEN" https://api.example.com/me
```

## 16. Industry Usage
- **Stripe/Auth0/Clerk**: OAuth2/OIDC + JWTs for API auth; short access tokens + rotating refresh tokens; webhooks signed with HMAC — the canonical production auth patterns.
- **Amazon/AWS**: Cognito (OIDC, JWTs via JWKS); SigV4 (signed requests — a different header-based scheme); IAM roles = session/token-based credentials for services.
- **Google**: OAuth2 for all APIs; Sign in with Google (OIDC); their auth server issues JWTs verifiable via Google's JWKS.
- **Meta/Netflix**: microservice architectures verify JWTs at every service boundary (shared signing keys / JWKS); session tokens for first-party web apps.
- **Every framework**: Django/Express/Spring implement session stores + signed cookies out of the box; CSRF middleware is default — the session/cookie model is the web's baseline.

## 17. References
- RFC 6265 — HTTP State Management (cookies): https://www.rfc-editor.org/rfc/rfc6265
- RFC 7519 — JWT: https://www.rfc-editor.org/rfc/rfc7519
- RFC 6749 — OAuth 2.0: https://www.rfc-editor.org/rfc/rfc6749
- RFC 7636 — PKCE: https://www.rfc-editor.org/rfc/rfc7636
- RFC 6750 — Bearer tokens: https://www.rfc-editor.org/rfc/rfc6750
- MDN — Cookies / SameSite: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
- OWASP Session Management Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

## 18. Cheat Sheet
- Cookie = client-side state, auto-sent; attributes: HttpOnly, Secure, SameSite.
- Session = server store keyed by random session ID in a cookie → revocable instantly.
- JWT = signed self-contained claims (header.payload.signature) → stateless, un-revocable (pre-expiry), readable.
- Bearer = `Authorization: Bearer <token>` (CSRF-resistant; not auto-sent).
- XSS → HttpOnly cookies + CSP; CSRF → SameSite + tokens.
- Session fixation → regenerate ID at login.
- OAuth2 = authorization (scopes); OIDC = + authentication (ID token).
- PKCE for SPAs; refresh rotation for theft resistance.
- 401 = unauthenticated; 403 = unauthorized.
- Never put secrets in JWTs/cookies; short TTL + rotate.

## 19. Quiz
1. HttpOnly prevents: a) CSRF b) JS reading the cookie (XSS theft) c) HTTPS downgrade d) caching → **b**
2. SameSite=Lax blocks: a) all cross-site b) most CSRF c) XSS d) session fixation → **b**
3. JWTs are: a) revocable b) stateless + signed c) opaque d) encrypted → **b**
4. Sessions are stored: a) in the cookie b) server-side c) in the URL d) in DNS → **b**
5. OAuth2 issues: a) passwords b) scoped access/refresh tokens c) cookies d) TLS keys → **b**
6. CSRF works because cookies are: a) encrypted b) auto-sent c) HttpOnly d) signed → **b**
7. PKCE protects: a) client-secret theft b) code interception c) JWTs d) cookies → **b**
8. To revoke a JWT early you need: a) nothing b) a blocklist / short TTL + refresh rotation c) delete cookie d) restart server → **b**
9. 401 vs 403: a) 401 not authorized b) 401 unauthenticated, 403 unauthorized c) same d) 403 unauthenticated → **b**
10. Refresh token rotation: a) issues new token, invalidates old b) never changes c) stores password d) signs cookies → **a**

## 20. Flashcards
- **Q: Cookie vs session?** → **A:** Cookie = client token; session = server-side state keyed by cookie ID.
- **Q: What does HttpOnly do?** → **A:** Blocks JS access → thwarts XSS cookie theft.
- **Q: SameSite?** → **A:** Controls cross-site cookie sending → CSRF defense.
- **Q: JWT structure?** → **A:** header.payload.signature (base64url, signed).
- **Q: Why JWT can't be revoked early?** → **A:** Signature remains valid; need blocklist or short TTL + refresh rotation.
- **Q: CSRF fix?** → **A:** SameSite, CSRF tokens, Origin checks (bearer APIs are immune).
- **Q: OAuth2 vs OIDC?** → **A:** OAuth2 = authorization (scopes); OIDC = + authentication (ID token).
- **Q: Where not to store tokens in SPA?** → **A:** localStorage (XSS-stealable); prefer HttpOnly cookie or memory.

## 21. Revision
HTTP statelessness → state must live somewhere: cookies (client, auto-sent, 4 KB, attributes HttpOnly/Secure/SameSite), sessions (server store keyed by random ID in a cookie — instantly revocable), and tokens (Bearer/JWT — stateless signed claims, un-revocable pre-expiry, readable). XSS → HttpOnly + CSP; CSRF → SameSite + tokens. OAuth2/OIDC = delegated authorization + authentication with scoped, revocable tokens (PKCE for SPAs, refresh rotation). 401 = unauthenticated, 403 = unauthorized. Design choice: sessions for web + instant revocation; JWTs for APIs + stateless scale.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Cookie vs session vs JWT?" | 2 How It Works / 13 Q&A |
| "How do you protect against XSS/CSRF?" | 9 Internal Working / 13 Q&A |
| "How do you revoke a JWT?" | 13 Q&A / 14 Follow-Up |
| "Design auth for SPA + microservices." | 13 Q&A / 15 Coding |
| "What is OAuth2/PKCE?" | 13 Q&A / 9 Internal Working |
| "Where should an SPA store tokens?" | 13 Q&A / 14 Follow-Up |
| "401 vs 403?" | 13 Q&A / 2 How It Works |
| "Refresh token rotation?" | 13 Q&A / 16 Industry Usage |
