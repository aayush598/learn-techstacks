# Authentication (JWT/OAuth) + Redis Caching - 250+ Interview Q&A
## For YC Startups & Top Tech Companies

## JWT & Token Auth (Q1-Q50)
### Q1: What is JWT? Explain its structure.
**Answer:** JWT (JSON Web Token) is a compact, URL-safe token format for representing claims between parties. Structure: `header.payload.signature`
- **Header**: `{"alg": "HS256", "typ": "JWT"}` - algorithm and token type
- **Payload**: `{"sub": "user123", "iat": 1516239022, "exp": 1516242622}` - claims (registered, public, private)
- **Signature**: HMAC-SHA256(base64(header) + "." + base64(payload), secret) - verifies integrity and authenticity

### Q2: JWT vs Session-based auth - which is better?
**Answer:** JWT is stateless (no server-side storage), scales horizontally easily, works well for microservices and mobile apps. Sessions are stateful (server stores session), easier to revoke (just delete session), simpler for traditional server-rendered apps. JWT cannot be revoked without a blacklist. Sessions need shared session store in multi-server setups.

### Q3: Access token vs Refresh token - explain the pattern.
**Answer:** Access token (short-lived, 15-60 min) sent with API requests. Refresh token (long-lived, days-months) stored securely, used only to get new access tokens. Flow: login → get both tokens → use access token → on 401, call /refresh with refresh token → get new access token (rotate refresh token too). Benefits: limits exposure if access token stolen, can revoke refresh tokens.

### Q4: HS256 vs RS256 - when to use each?
**Answer:** HS256 (HMAC with SHA-256): symmetric, same secret signs and verifies, faster, simpler. Good for single-service apps. RS256 (RSA with SHA-256): asymmetric, private key signs, public key verifies. Services can verify without knowing private key. Best for microservices, third-party verification. Always prefer RS256 for production.

### Q5: How do you handle JWT revocation?
**Answer:** Strategies: (1) Blacklist in Redis - store revoked JTIs until expiry, check on each request. (2) Short TTL + refresh token rotation - access tokens expire quickly, revoke refresh tokens on logout. (3) Token version in DB - increment version on password change, reject old version tokens. (4) Just let tokens expire - simplest but least secure.

### Q6: What is OAuth 2.0? Explain the main flows.
**Answer:** OAuth 2.0 is an authorization framework. Flows: (1) Authorization Code - most secure, for server-side apps. (2) Implicit (deprecated in OAuth 2.1) - for SPAs, now use PKCE. (3) Client Credentials - server-to-server, no user. (4) Resource Owner Password Credentials (deprecated) - directly uses username/password. (5) Device Code - for input-constrained devices.

### Q7: What is PKCE and why was it introduced?
**Answer:** Proof Key for Code Exchange. Protects auth code flow for public clients (SPAs, mobile apps). Instead of client_secret, the app generates a code_verifier (cryptographically random) and sends code_challenge (SHA256 hash) during auth request. When exchanging code, sends code_verifier. Server verifies challenge matches. Prevents interception attacks even if auth code is intercepted.

### Q8: What is OpenID Connect (OIDC)?
**Answer:** Authentication layer on top of OAuth 2.0. Adds ID token (JWT) containing user identity. Standardizes `/userinfo` endpoint. Adds `openid` scope. Most modern auth systems (Google, Auth0, Clerk) use OAuth 2.0 + OIDC. OAuth 2.0 alone is for delegation (app can access your data), OIDC adds authentication (verifying who you are).

### Q9: How does Clerk auth work? (your resume)
**Answer:** Clerk is a user management and authentication platform. Provides pre-built components (SignIn, SignUp, UserButton), session management, MFA, social login (Google, GitHub, etc). Uses JWT for session tokens. Integrates via ClerkProvider in React/Next.js. Middleware protects routes. Webhooks for user events. Your GuardrailZ project uses Clerk for auth.

### Q10: How do you securely store tokens on the client?
**Answer:** httpOnly cookies (not accessible to JavaScript, prevents XSS theft) or in-memory (refreshed on page load). localStorage is vulnerable to XSS. Best practice: BFF (Backend-for-Frontend) pattern - frontend never sees tokens, backend manages them in httpOnly cookies.

### Q11: What is CSRF and how to prevent it?
**Answer:** Cross-Site Request Forgery - attacker tricks authenticated user into making unwanted requests. Prevention: (1) CSRF tokens - random token in forms, validated server-side. (2) SameSite cookies (Strict or Lax). (3) Custom headers (e.g., X-Requested-By) - not sent cross-origin. (4) Double-submit cookie pattern. (5) Origin/Referer header validation.

### Q12: XSS attacks - types and prevention?
**Answer:** Cross-Site Scripting: attacker injects malicious scripts. Types: Stored (persistent in DB), Reflected (in URL), DOM-based (client-side). Prevention: input sanitization, output encoding (React auto-escapes), Content-Security-Policy headers, httpOnly cookies, proper Content-Type headers.

### Q13: Password hashing - bcrypt vs argon2 vs scrypt?
**Answer:** bcrypt: slower than SHA, built-in salt, configurable cost (2^cost iterations). Max 72 bytes. argon2: winner of PHC, memory-hard (resists GPU attacks), 3 variants (argon2d/2i/2id). scrypt: memory-hard, used by Litecoin. Recommendation: argon2id if available, bcrypt as fallback. NEVER use SHA-* or MD5 for passwords.

### Q14: RBAC vs ABAC?
**Answer:** RBAC (Role-Based Access Control): users have roles, roles have permissions. Simple, predictable. Subject to role explosion. ABAC (Attribute-Based Access Control): policies evaluate user attributes, resource attributes, environment. More flexible but complex. Example: "Managers can edit reports in their department during business hours".

### Q15: What is SSO (Single Sign-On)?
**Answer:** Users authenticate once and access multiple applications. Implemented via SAML 2.0 (enterprise, XML-based) or OIDC (modern, JSON-based). IdP (Identity Provider) authenticates, SP (Service Provider) trusts IdP. SAML uses assertions, OIDC uses ID tokens. Clerk, Auth0, Okta provide SSO.

### Q16: What is MFA and how to implement it?
**Answer:** Multi-Factor Authentication. Factors: something you know (password), have (phone/security key), are (fingerprint). Common: TOTP (Time-based One-Time Password via authenticator app), SMS codes, push notifications, security keys (WebAuthn/FIDO2). Implement as second factor after password verification.

### Q17: Rate limiting auth endpoints - strategies?
**Answer:** (1) IP-based: track failed attempts per IP. (2) Account-based: track failed attempts per username. (3) Progressive delays: increase delay between attempts. (4) CAPTCHA after N failures. (5) Account lockout: temporary/permanent after threshold. Use Redis with sliding window algorithm.

### Q18: Password reset flow - design it.
**Answer:** (1) User enters email. (2) Generate cryptographically random token (crypto.randomBytes(32)). (3) Store token hash + expiry (1 hour) in DB. (4) Send email with link containing token. (5) On click, verify token hash and expiry. (6) Prompt for new password. (7) Hash new password, update DB. (8) Invalidate all sessions/tokens. (9) Send confirmation email. NEVER send the token in URLs that get logged.

### Q19: What is the BFF (Backend-for-Frontend) pattern?
**Answer:** A dedicated backend service for the frontend that handles auth tokens. Frontend authenticates with BFF (via httpOnly cookie), BFF manages access/refresh tokens with external IdP. Benefits: tokens never exposed to browser JavaScript, reduces XSS risk, simplifies frontend auth logic. Common with SPAs and mobile apps.

### Q20: Auth middleware in FastAPI - how to implement?
**Answer:** Create dependency: `async def get_current_user(token: str = Depends(oauth2_scheme))`. Decode JWT, validate expiry, fetch user. Use `Depends(get_current_user)` in protected routes. FastAPI's OAuth2PasswordBearer extracts token from Authorization header.

## OAuth & Social Login (Q51-Q80)
### Q21: Explain the OAuth 2.0 Authorization Code flow step-by-step.
**Answer:** (1) Client redirects user to authorization server: `/authorize?response_type=code&client_id=ID&redirect_uri=URI&scope=openid+profile+email`. (2) User authenticates and consents. (3) Auth server redirects back with code: `redirect_uri?code=AUTH_CODE`. (4) Client sends POST to `/token` with code, client_id, client_secret, redirect_uri. (5) Auth server returns access_token, refresh_token, id_token. (6) Client can call `/userinfo` with access_token to get user details.

### Q22: What are OAuth scopes?
**Answer:** Scopes define the specific permissions the application is requesting. Examples: `openid` (for OIDC), `profile` (read user profile), `email` (read email), `photos.read` (specific API permission). Scopes appear in the JWT payload. The user sees what scopes are being requested on the consent screen. Principle of least privilege - only request scopes you need.

### Q23: What is a client_secret? How is it used?
**Answer:** A secret known only to the client application and authorization server. Used during token exchange to prove the client's identity. Confidential clients (server-side apps) can store secrets securely. Public clients (SPAs, mobile) cannot - they use PKCE instead. Rotate secrets periodically.

### Q24: Social login implementation challenges?
**Answer:** Multiple accounts for same email (merge strategy), account linking (same user via Google + GitHub), email verification (third-party claims email is verified), profile data consistency, token refresh for each provider, handling provider outages, logout across providers.

## Session & Cookie Auth (Q81-Q100)
### Q25: Session-based auth - how does it work?
**Answer:** (1) User logs in with credentials. (2) Server creates session, stores it (in-memory, Redis, or DB). (3) Server sets httpOnly cookie with session ID. (4) Browser sends cookie with every request. (5) Server looks up session from cookie. (6) On logout, server deletes session. Stateless on client, stateful on server.

### Q26: httpOnly vs secure vs sameSite cookie attributes?
**Answer:** httpOnly: JavaScript cannot access (prevents XSS theft). secure: only sent over HTTPS. sameSite: Strict (same-site only), Lax (top-level navigations allowed), None (cross-site, requires Secure). For auth cookies: httpOnly + secure + sameSite=Lax.

### Q27: Where should you store session data?
**Answer:** Redis (most common - fast, TTL support, shared across instances), database (persistent but slower), in-memory (only for single-server). For multi-server deployments, use Redis or a database. Never store sensitive data in the cookie itself.

## Redis Caching (Q101-Q200)
### Q28: What is Redis? Core data structures?
**Answer:** In-memory data structure store. Data structures: String (key-value, counters), List (queue/stack via LPUSH/RPUSH), Set (unique members, SADD/SINTER), Sorted Set (leaderboards, ZADD/ZRANK), Hash (object-like, HSET/HGET), Bitmap (SETBIT/GETBIT), HyperLogLog (cardinality estimation, PFADD/PFCOUNT), Stream (message queue, XADD/XREAD).

### Q29: Redis persistence - RDB vs AOF?
**Answer:** RDB: point-in-time snapshots, compact file, faster recovery, can lose data between snapshots. AOF: logs every write, more durable (configurable fsync: always/everysec/no), larger file, slower recovery. Best practice: enable both. Use AOF for durability, RDB for faster restarts.

### Q30: Redis eviction policies?
**Answer:** noeviction (return error), allkeys-lru (evict least recently used), volatile-lru (evict LRU from keys with TTL), allkeys-lfu (least frequently used), volatile-lfu, volatile-ttl (shortest TTL first), allkeys-random, volatile-random. LRU/LFU most common for caching.

### Q31: Cache aside pattern?
**Answer:** Read: check cache → if miss, read from DB, write to cache, return. Write: write to DB, invalidate cache (or update cache). Pros: simple, handles cache misses. Cons: cache stampede risk if many misses simultaneously, stale data possible.

### Q32: What is cache stampede? How to prevent?
**Answer:** When cache key expires and many requests simultaneously hit DB. Prevention: (1) Locking/mutex - first request acquires lock, others wait. (2) Early recomputation - refresh cache before it expires (hedged TTL). (3) Stale-while-revalidate - serve stale data while async refresh. (4) Probabilistic early expiration.

### Q33: Redis Sentinel vs Cluster?
**Answer:** Sentinel: high availability (automatic failover), monitoring, single master with replicas, not for scalability. Cluster: automatic sharding across nodes (16384 hash slots), built-in HA, horizontal scaling. Use Sentinel for moderate throughput HA, Cluster for high throughput + scalability.

### Q34: Redlock algorithm - what is it? Problems?
**Answer:** Distributed lock algorithm for Redis. Acquire lock on N/2+1 Redis instances. Each has short TTL. Subtract elapsed time from validity. Release by deleting key. Controversial - Martin Kleppmann argued it's unsafe in certain scenarios (clock drift, long GC pauses). Consider alternatives: etcd, ZooKeeper, or use simple single-instance lock if crash safety not critical.

### Q35: Rate limiting with Redis - implement sliding window?
**Answer:** Use Sorted Set with timestamp as score. For each request: `ZREMRANGEBYSCORE key 0 (now-window`, `ZCARD key`, if count < limit: `ZADD key now now`, `EXPIRE key window`. Or use the generic cell rate algorithm with Lua scripting for precision.

### Q36: Redis transactions - how do they work?
**Answer:** MULTI starts transaction, commands are queued (not executed), EXEC executes all atomically. WATCH provides optimistic locking - if watched key changes before EXEC, transaction aborts. Unlike SQL transactions, Redis transactions don't have rollback.

### Q37: Redis pub/sub vs Streams?
**Answer:** Pub/Sub: fire and forget, no message persistence, subscribers must be active. Streams: persisted, consumer groups, message acknowledgment, history replay. Use pub/sub for real-time notifications where message loss is acceptable. Use Streams for reliable messaging, event sourcing, job queues.

### Q38: Redis as a message queue?
**Answer:** Use List (LPUSH/BRPOP) for simple queue. Use Stream (XADD/XREADGROUP) for advanced queuing with consumer groups, ACKs, retries. For production-grade messaging, consider dedicated message queues (RabbitMQ, Kafka, SQS).

### Q39: Sorted sets use cases?
**Answer:** Leaderboards (ZADD score member, ZRANGE/ZREVRANGE), rate limiting (score = timestamp), autocomplete (score = frequency), time-series data, delayed queues (score = execution time), range queries.

### Q40: Redis in FastAPI integration?
**Answer:** Use aioredis (now redis-py with asyncio). Create Redis client at startup, inject as FastAPI dependency. For caching: `@cache(expire=60)` decorator. Libraries: fastapi-cache, aiocache. Store sessions in Redis. Implement rate limiting with Redis. Background tasks can publish to Redis streams.

## Security Headers & Best Practices (Q201-Q250)
### Q41: Content Security Policy (CSP) - what is it?
**Answer:** HTTP header that restricts which resources (scripts, styles, images) can be loaded. Prevents XSS and data injection attacks. Example: `Content-Security-Policy: default-src 'self'; script-src 'self' trusted-cdn.com; img-src *`.

### Q42: API key authentication - pros/cons?
**Answer:** Simple, good for machine-to-machine. Problems: API keys are long-lived, hard to rotate, often exposed in code/URLs, no user context. Better: use API key + secret, or switch to OAuth 2.0 client credentials. Rate limit by key, allow key rotation, store hashed.

### Q43: SQL injection prevention?
**Answer:** Never concatenate user input into SQL queries. Use parameterized queries (SQLAlchemy ORM, parameterized statements with ? placeholders), input validation, ORM layers (SQLAlchemy, Django ORM), stored procedures with parameters.

### Q44: How does Clerk handle session management?
**Answer:** Clerk uses short-lived JWT access tokens + long-lived refresh tokens. Sessions stored server-side. Clerk middleware checks session on every request. Client-side Clerk SDK handles token refresh automatically. Session activity tracked for analytics and security.
