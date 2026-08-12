# Priority 3 — Networking & HTTP (Q481–Q497)

**Why these matter for micro1:** you'll build the AI recruiter's API and real-time chat. Expect HTTP methods/status codes, HTTPS/TLS, DNS, cookies/sessions, CORS, and WebSocket vs SSE (especially with streaming AI chat).

---

## Q481: What happens when you type a URL and press Enter?

**The full journey (a classic interview answer):**

1. **URL parsing** — browser extracts scheme, host, path, port (`https://zara.com/applications`).
2. **DNS resolution** — browser checks cache → OS cache → hosts file → recursive DNS resolver → root → TLD → authoritative server → **IP address** (e.g., `142.250.72.14`) (Q486).
3. **TCP handshake** — three-way handshake (SYN → SYN-ACK → ACK) establishes the connection (Q491).
4. **TLS handshake** — for HTTPS: negotiate cipher, verify the certificate against a CA, exchange keys → **encrypted channel** (Q487).
5. **HTTP request** — browser sends `GET /applications HTTP/1.1` (or HTTP/2) with headers (Host, Cookie, Accept).
6. **Server processing** — nginx/ALB → FastAPI → DB/cache → response with status + headers + body.
7. **Response** — browser parses HTML, then fetches CSS/JS/images (each a new request, HTTP/2 multiplexes them), renders the page, runs JS.
8. **Connection reuse** — keep-alive reuses the TCP/TLS connection for subsequent requests.

**Talk through steps 2–5 crisply; that's what they're probing.**

---

## Q482: What is the difference between HTTP and HTTPS?

- **HTTP** — plaintext. Anyone on the path (Wi-Fi, ISP, MITM) can read and modify traffic.
- **HTTPS = HTTP over TLS** — provides **confidentiality** (encrypted), **integrity** (tamper-evident), and **authentication** (the server's identity is verified via certificates) (Q487).

```
HTTP : http://zara.com      port 80,  plaintext
HTTPS: https://zara.com     port 443, TLS 1.2/1.3 encrypted
```

**Why it matters for you:** resumes, JWTs, cookies, chat transcripts are all sensitive — every byte must go over HTTPS. `Secure` cookies only sent over HTTPS. Also: SEO/rankings, and browsers mark HTTP sites as "not secure". Modern best practice: **HTTP → 301 → HTTPS** everywhere, HSTS header, no plaintext exceptions.

---

## Q483: HTTP request and response structure?

**Request:**
```text
POST /api/v1/applications HTTP/1.1
Host: zara.com
Authorization: Bearer eyJ...
Content-Type: application/json
Content-Length: 123

{"job_id":"job_1","candidate_id":"cand_2"}
```

**Response:**
```text
HTTP/1.1 201 Created
Content-Type: application/json
Content-Length: 45

{"id":"app_9","status":"submitted"}
```

- **Start line** (method + path + version / status line), **headers** (key: value), **blank line**, **body** (optional).
- **Request methods:** GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE, HEAD (headers only), OPTIONS (CORS preflight, Q494).
- **Headers:** Host, Content-Type, Authorization, Accept, Cookie; response: Content-Type, Set-Cookie, Cache-Control, Retry-After.
- **HTTP/1.1** one request per connection (pipelining is broken in practice); **HTTP/2** multiplexes many streams over one connection.

---

## Q484: What are idempotent and safe HTTP methods?

(Same as Q388 — here's the API-flavored answer.)

- **Safe** — no server state change, may be cached: GET, HEAD, OPTIONS.
- **Idempotent** — repeating has the same effect as once: GET, HEAD, PUT, DELETE, OPTIONS, TRACE. POST is *not*; PATCH isn't guaranteed.
- **Why it matters:** retries after timeouts are only safe on idempotent methods (or with idempotency keys, Q397). Proxies/caches treat GET as safe to retry/replay.

---

## Q485: What are the main HTTP status codes?

**2xx Success:** `200 OK`, `201 Created` (POST), `204 No Content` (DELETE).
**3xx Redirection:** `301 Moved Permanently`, `302 Found`, `304 Not Modified` (cache validators), `307/308` (preserve method/body).
**4xx Client errors (fixable by caller):** `400 Bad Request`, `401 Unauthorized` (no/malformed creds), `403 Forbidden` (authenticated but not allowed), `404 Not Found`, `405 Method Not Allowed`, `408 Request Timeout`, `409 Conflict` (duplicate/state conflict), `410 Gone`, `413 Payload Too Large` (big resume!), `422 Unprocessable Entity` (validation — FastAPI default), `429 Too Many Requests` (rate limit, Q393).
**5xx Server errors:** `500 Internal Server Error`, `501 Not Implemented`, `502 Bad Gateway` (upstream bad response), `503 Service Unavailable` (overloaded/maintenance), `504 Gateway Timeout` (upstream timed out).

**API rules:** use them *meaningfully* and consistently (Q392) — 401 vs 403 vs 422 tell the client what to do next; 503 + `Retry-After` enables sane retries.

---

## Q486: How does DNS work?

**DNS = the internet's phone book: domain names → IP addresses.**

**Resolution chain:** browser/OS cache → **recursive resolver** (ISP/1.1.1.1) → **root servers** → **TLD servers** (.com) → **authoritative servers** (the domain's records).

**Record types:**
- **A/AAAA** — IPv4/IPv6 address.
- **CNAME** — alias to another name.
- **MX** — mail server.
- **TXT** — arbitrary text (SPF, DKIM verification, domain verification).
- **NS** — authoritative name servers for a zone.

**Features relevant to you:**
- **TTL (time-to-live)** — how long resolvers cache; lower TTL = faster failover, more queries.
- **Round-robin DNS** — multiple A records → basic load distribution (not health-aware; real LB is better).
- **Route 53/Cloudflare** — hosted zones, health-check failover, weighted routing, latency-based routing.

**Interview answer:** "DNS translates names to IPs through a cache-first hierarchy — local cache → resolver → root → TLD → authoritative. I lower TTLs before an outage/maintenance so clients pick up the new IP fast."

---

## Q487: How does TLS/HTTPS encryption work?

**Goal:** an authenticated, encrypted, tamper-evident channel.

1. **Hello + negotiation** — client and server agree on protocol version + cipher suite (e.g., TLS 1.3, AES-256-GCM).
2. **Certificate** — server sends its certificate (public key + identity, signed by a CA).
3. **Verification** — client checks the certificate's chain against trusted root CAs, validity dates, and hostname match. (This is how you know the server is who it claims to be — **authentication**.)
4. **Key exchange** — via ECDHE (Ephemeral Diffie-Hellman) — both sides derive the *same* session key over public values; each session has a fresh key (**forward secrecy**: past traffic can't be decrypted if a server key leaks later).
5. **Symmetric encryption** — all data now flows AES-encrypted with the session key (**confidentiality** + HMAC integrity).

**Two key types:** **symmetric** (AES — same key both ways, fast, used for bulk data) and **asymmetric** (RSA/ECDSA — public/private pair, slow, used for key exchange/signing). TLS combines both: asymmetric to agree the key, symmetric to encrypt the data.

---

## Q488: What are cookies, and how do they work?

**Cookie** = small key/value piece of state the server sets via `Set-Cookie`; the browser stores it and sends it back with every request to that domain.

```http
Set-Cookie: refresh_token=abc123; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=2592000
```

**Key attributes:**
- **HttpOnly** — JS can't read it (XSS protection, Q404/Q410).
- **Secure** — only over HTTPS.
- **SameSite=Lax/Strict/None** — controls cross-site sending (CSRF defense, Q404).
- **Max-Age / Expires** — session vs persistent.
- **Domain/Path** — scoping.

**Uses:** session ids, refresh tokens (Q410), preferences, A/B flags. **Caution:** cookies are the vector for CSRF; and size limits (~4 KB per cookie, ~50 per domain).

---

## Q489: What's the difference between cookies and tokens?

| | **Cookies** | **Tokens (JWT)** |
|---|---|---|
| Where stored | Browser, auto-sent by the browser | Client code sends them (`Authorization` header) |
| Transport | Auto-attached by the browser (CSRF risk) | Explicit — no CSRF risk from being auto-sent |
| XSS exposure | None if `HttpOnly` | In localStorage/memory, readable by XSS |
| State | Server-side session store or stateless value | Self-contained claims, stateless verification |
| Revocation | Easy (server controls session) | Hard (short TTL / blocklist) |

**Modern combo:** short-lived access token in memory/header + refresh token in an HttpOnly cookie (Q408–411). Best of both: refresh is XSS-safe (HttpOnly), access token verification is stateless, CSRF is handled (Q404).

---

## Q490: What is the TCP three-way handshake? What is UDP?

**TCP (connection-oriented, reliable):**
1. Client → `SYN` ("can we talk?")
2. Server → `SYN-ACK` ("yes, and you?")
3. Client → `ACK` ("great, connection open")

After this, data flows in order with retransmission on loss, flow control, congestion control. **Used by:** HTTP/HTTPS, SSH, Postgres, Redis.

**UDP (connectionless, best-effort):** no handshake, no ordering, no retransmission — faster, less overhead. **Used by:** DNS queries, video/voice streaming, gaming. (DNS over UDP with TCP fallback.)

**Interview angle:** latency-critical or lossy networks → decide TCP (reliability) vs UDP (speed); for a chat you still want TCP/WebSocket; you'd add reliability at the app layer if you chose UDP.

---

## Q491: What is a WebSocket, and how does it work?

**WebSocket** = a full-duplex, persistent, bidirectional connection over TCP, established via an HTTP upgrade:

1. Client sends `GET /ws` with `Upgrade: websocket` + `Sec-WebSocket-Key`.
2. Server responds `101 Switching Protocols`.
3. Both sides now push messages anytime — no polling.

**Frames:** text/binary messages + ping/pong keepalives; close handshake at the end.

**Uses:** chat (your AI interview!), real-time collaboration, live dashboards, games. **Scaling concerns:** connections are long-lived server state — need sticky sessions or a pub/sub layer (Redis) to fan messages across instances, and idle keepalives (Q348–349).

---

## Q492: WebSocket vs SSE — which do you use and when?

| | **WebSocket** | **SSE (Server-Sent Events)** |
|---|---|---|
| Direction | **Bidirectional** | Server → client only |
| Protocol | Own (after HTTP upgrade) | Plain HTTP, `text/event-stream` |
| Reconnect | Manual/own logic | Auto-reconnect + `Last-Event-ID` |
| Binary | Yes | Text only |
| Server complexity | Stateful, needs pub/sub across instances | Stateless, easy |
| Proxy/edge support | Needs special config | Works through HTTP proxies |
| Best for | Chat, multiplayer, two-way | Notifications, live scores, one-way streams |

**For your AI chat:** a chat where the candidate sends and receives → **WebSocket** is natural (persistent session, Q349). For pure "screening result is ready" pushes → **SSE** is simpler. Many teams stream the LLM via SSE frames (Q399) and keep the interactive session on WebSocket. **Answer:** "SSE for one-way pushes (simple, auto-reconnect); WebSocket for true two-way chat."

---

## Q493: How does CORS work?

**CORS (Cross-Origin Resource Sharing)** — the browser's policy for letting a web page at origin A call an API at origin B.

**Why it exists:** the browser blocks cross-origin reads by default (a malicious page mustn't be able to read your bank API using your cookies). It doesn't block the request itself — it blocks the *page* from reading the response without permission.

**Flow for a cross-origin request:**
1. **Simple requests** (GET/POST with simple content types): browser sends the request, checks response headers.
2. **Preflight** for non-simple requests (custom headers, `application/json` body, PUT/DELETE): browser first sends `OPTIONS` with `Access-Control-Request-Method/Headers`; server must answer with `Access-Control-Allow-*`; only then the real request goes.
3. For credentialed requests (cookies/Authorization), server must echo the **specific origin** (not `*`) plus `Access-Control-Allow-Credentials: true`.

**Your API config:**
```python
allow_origins=["https://app.zara.com"]          # exact origin, not "*"
allow_credentials=True                          # cookies/Authorization
allow_methods=["GET","POST","PUT","DELETE"]
allow_headers=["Authorization","Content-Type","Idempotency-Key"]
```

**Troubleshooting 101:** CORS errors are browser-only (curl works) — that's the #1 tell. Check the origin allowlist and preflight response.

---

## Q494: What is a CDN, and how does it improve performance?

**CDN (Content Delivery Network)** = a global network of edge servers that cache and serve content closer to users (Q247/Q600-adjacent).

- **Static assets** (JS, CSS, images): cached at the edge; users download from a nearby PoP instead of your origin — big latency + origin bandwidth savings.
- **Dynamic/API:** advanced CDNs (Cloudflare Workers, Fastly) can compute/cache at the edge; plain CDNs cache only what's cacheable (GET, cache headers).
- **How it decides:** `Cache-Control: max-age`, `ETag`, purge/invalidation APIs.

**For your app:** serve the Next.js bundle and images via CDN (CloudFront); never cache user-specific API responses at the edge (they'd leak between users!) — cache-control per response (private/no-store for resumes/scores).

---

## Q495: How does HTTP caching work? (ETag, Cache-Control)

**Server-driven:** response headers tell clients/caches how long and under what conditions to reuse a response.

- **`Cache-Control: max-age=300`** — fresh for 300s; `public` (any cache) vs `private` (only the browser, e.g., user-specific data); `no-store` (never cache — resumes, tokens); `no-cache` (revalidate before reuse).
- **`ETag`** — a fingerprint of the representation. Client sends `If-None-Match: <etag>`; if unchanged, server replies `304 Not Modified` (no body) — saves bandwidth and work (Q493-related, Q251).
- **`Last-Modified` / `If-Modified-Since`** — time-based variant.
- **`Vary`** — cache key must vary by header (e.g., `Accept-Encoding`).

**For you:** job listings public + `max-age=60`; candidate data `private`/`no-store`; LLM/costly computed results can be cached *server-side* (Q432) with versioned keys, and only ETag-exposed to clients.

---

## Q496: What is HTTP/2, and why is it faster than HTTP/1.1?

**Key improvements:**
1. **Multiplexing** — many requests/responses share one TCP connection simultaneously; no head-of-line blocking at the connection level (HTTP/1.1 queues requests).
2. **Binary framing** — efficient header+payload framing (HTTP/1.1 is text-based).
3. **Header compression (HPACK)** — repetitive headers sent once.
4. **Server push** (deprecated-ish) — server preemptively sends resources.
5. **Prioritization** — critical resources first.

**Result:** fewer connections, less latency for many small assets (JS/CSS bundles), better mobile performance. **HTTP/3** (QUIC over UDP) goes further — connection migration, no TCP head-of-line blocking, faster handshakes. For your Next.js + FastAPI stack, the load balancer/CDN terminates these; your app mostly doesn't care.

---

## Q497: How do you debug network/API issues?

**Layered approach:**
1. **Browser DevTools Network tab** — is the request sent? status? timing? which phase is slow (DNS/TCP/TLS/request/response)? CORS error?
2. **`curl -v` / `httpie`** — bypass the browser to isolate server-side issues; check headers, certs, redirects.
3. **Server logs** — `request_id` links a failing request to logs/traces (Q65, Q631); check error middleware output.
4. **`ping`/`nslookup`/`dig`** — DNS resolution correct? (Q486).
5. **`tcpdump`/`ngrok`** — raw packets / inspect webhook payloads.
6. **Traces (OpenTelemetry)** — which hop is the bottleneck: LB → API → DB → LLM (Q444).

**Answer pattern:** "First confirm it's not a browser-side artifact (CORS, cache, dev tooling); curl reproduces the request server-side; then follow request_id through logs and traces to find the failing hop."
