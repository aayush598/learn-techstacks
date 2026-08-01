# HTTP Methods, Status Codes, and Headers

> **TL;DR**: HTTP's semantics live in three things — methods (verbs that define intent: GET, POST, PUT, DELETE, PATCH…), status codes (3-digit outcomes: 2xx success, 3xx redirect, 4xx client error, 5xx server error), and headers (metadata that controls caching, auth, content type, connections) — and they exist to make requests self-describing, cachable, and safely retryable.

## 1. Why Does This Exist?
A request/response protocol needs three things to be *usable at web scale*: **intent** (what to do with the resource — methods), **outcome** (did it work and why — status codes), and **metadata** (how to interpret/cache/authenticate — headers). Without these, clients couldn't distinguish "create vs read", "found vs created vs error", or "cache this for a day". These three design axes (RFC 9110) exist to make HTTP *semantic*: machines can act correctly on generic responses, caches can decide freshness, and clients can safely retry idempotent operations — the foundation of reliable distributed systems.

## 2. How Does It Work?
**Methods** (verbs in the request line):
- **GET** — retrieve a representation. Safe (no side effects), idempotent, cacheable.
- **HEAD** — like GET but no body (headers only). Used for probing/checking freshness.
- **POST** — submit/process (create resource, run action). Not safe, not idempotent, generally not cacheable.
- **PUT** — replace a resource *at a URI* with the body. Idempotent.
- **DELETE** — remove a resource. Idempotent (deleting a non-existent resource is "success").
- **PATCH** — partial modification. Not necessarily idempotent (it *should* be in practice but the spec says it can vary).
- **OPTIONS** — discover capabilities (CORS preflight). **TRACE** — echo for diagnostics (often disabled for security). **CONNECT** — establish tunnel (HTTPS proxy).

**Status codes** (3-digit classes):
- **1xx informational**: 100 Continue, 101 Switching Protocols, **103 Early Hints**.
- **2xx success**: 200 OK, 201 Created, 202 Accepted, 204 No Content, 206 Partial Content (range).
- **3xx redirection**: 301 Moved Permanently, 302 Found (temporary), 303 See Other, 304 Not Modified (caching), 307 Temporary Redirect, 308 Permanent Redirect.
- **4xx client error**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 408 Timeout, 409 Conflict, 410 Gone, 413 Payload Too Large, 429 Too Many Requests, 418 Teapot (RFC 2324, joke).
- **5xx server error**: 500 Internal Server Error, 501 Not Implemented, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout.

**Headers** — classified by context:
- **Request**: Host, User-Agent, Accept, Accept-Encoding, Authorization, Cookie, Referer, Origin, Content-Type, Content-Length, If-None-Match, If-Modified-Since, Range.
- **Response**: Server, Set-Cookie, Location, Cache-Control, ETag, Last-Modified, Content-Type, Content-Length, Allow, Retry-After, WWW-Authenticate, Access-Control-*.
- **General**: Connection, Date, Transfer-Encoding, Via.

## 3. When Is It Used?
- **REST APIs**: GET/POST/PUT/DELETE/PATCH map to read/create/replace/delete/update; status codes communicate outcomes; headers carry auth tokens, content negotiation, caching.
- **Web pages**: GET for navigation, POST for form submission; 3xx for redirects; 304 for cache revalidation; 429 for rate limiting; 5xx for outages.
- **File downloads**: GET with `Range` → 206 Partial Content (resumable downloads); `Content-Disposition` for filenames.
- **Auth flows**: 401 + `WWW-Authenticate` (challenge), `Authorization: Bearer <token>`; cookies via `Set-Cookie`; OAuth redirects via 302/303.
- **Proxies/CDNs**: `Via`, `X-Forwarded-For`, `Age`, `Cache-Control` — all header-driven.

## 4. Why Wasn't Another Approach Chosen?
- **Why verbs (methods) instead of action URLs** (`/do-delete?id=5`)? Because methods are a *closed set with defined semantics* — safe/idempotent/cacheable properties let caches and proxies reason about them *without understanding the app*. Action URLs are arbitrary strings no machine can interpret. HTTP chose small, meaningful verbs.
- **Why 3-digit numeric codes instead of text?** Numeric codes are machine-parseable and extensible; the reason phrase is decorative (and was made optional). Clients switch on the number; text is for humans.
- **Why not just 200/400/500?** Too coarse. Proxies and clients need to distinguish "retry" (429/503/504), "you're not allowed" (401/403), "still valid copy" (304), "partial content" (206). Fine-grained codes drive correct client behavior.
- **Why headers instead of fixed fields?** Fixed fields can't evolve (adding a header = no breaking change). Headers are extensible, multi-valued, and per-context (request/response/general). The cost is verbosity — hence HPACK (h2) compression.

## 5. Intuition
Methods = **verbs you can use on a book at a library**: "show me this book" (GET), "write this book here" (PUT), "add a page" (PATCH), "rip out the book" (DELETE), "submit a book request form" (POST). Status codes = the librarian's **traffic-light replies**: "here you go" (200), "moved to another aisle" (301/302), "not here" (404), "you're not allowed" (403), "system down, come back later" (503). Headers = the **sticky notes** on the request/response envelope: "cache this for a day", "I'm a mobile browser", "here's my auth token".

## 6. Real-World Analogy
**Restaurant ordering**: Methods = the verb of your order — "bring me the menu" (GET), "order the salmon" (POST — creates), "substitute the whole meal for a salad" (PUT — replace), "no dessert please" (DELETE). Status codes = the kitchen's reply system — "order up" (200), "we moved to a new location" (301), "not on the menu" (404), "you're not a customer" (401), "kitchen on fire, come back later" (503). Headers = the ticket annotations — "no onions" (Accept-Encoding/Content-Type analogies), "priority: regular customer" (Authorization/Cookie).

## 7. Formal Definition
HTTP methods are request verbs defined in RFC 9110, each with **safe** (no server state change) and **idempotent** (same result on repetition) semantics: GET/HEAD/OPTIONS/TRACE are safe and idempotent; PUT/DELETE are idempotent; POST and PATCH are neither (POST by definition, PATCH by spec-wording). Status codes are three-digit integers whose first digit denotes the response class: 1xx informational, 2xx success, 3xx redirection, 4xx client error, 5xx server error (RFC 9110 §15). Headers are field-name/value pairs with defined semantics per context (request/response), extensible via the RFC registry (e.g., `Authorization`, `Cache-Control`, `ETag`).

## 8. Example
A realistic REST conversation (JSON API), full headers:
```
Client -> Server
POST /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOi...            # JWT
Content-Type: application/json
Accept: application/json
If-None-Match: "abc123"                          # conditional

{"name": "Ada", "email": "ada@example.com"}
```
```
Server -> Client
HTTP/1.1 201 Created
Location: /api/users/42                          # new resource
Content-Type: application/json
Cache-Control: no-store
ETag: "xyz789"

{"id": 42, "name": "Ada", "createdAt": "2026-08-01T00:00:00Z"}
```
Follow-up `GET /api/users/42` with `If-None-Match: "xyz789"` → `304 Not Modified` (client's cache is fresh) — saving bandwidth. A bad body → `400 Bad Request`; wrong token → `401 Unauthorized` with `WWW-Authenticate: Bearer`; rate-limited → `429 Too Many Requests` with `Retry-After: 30`.

## 9. Internal Working
1. **Method parsing**: server maps method + path to a handler (e.g., in Express, `app.post('/api/users')`). Method routing is exact (no wildcards on the verb, but semantics apply).
2. **Safety/idempotency enforcement**: caches and proxies treat GET as non-mutating (may cache by default); POST is never auto-cached (requires explicit headers); retry logic in clients uses idempotency keys for POST when needed.
3. **Status code generation**: the app returns the code; the server/framework sets reason + headers. Standard codes have standard meaning but apps add custom (e.g., `2xx` business codes in JSON bodies is an anti-pattern — use real codes).
4. **Header processing**: server reads request headers (auth, content-type, conditional/caching), acts on them; sets response headers (content-type, caching, CORS, Set-Cookie).
5. **Content negotiation**: `Accept` (client's desired format) ↔ `Content-Type` (server's actual format); `Accept-Encoding: gzip, br` → server sends `Content-Encoding: gzip`.
6. **Conditional requests**: `ETag`/`Last-Modified` (response) ↔ `If-None-Match`/`If-Modified-Since` (request) → `304` or full body (200). This is the machinery behind "cache revalidation".
7. **Redirections**: 301/308 permanent vs 302/307 temporary; 302 historically switched POST→GET (303); 307/308 preserve method/body. Browsers auto-follow GET 3xx; POST needs handling.
8. **Proxies**: add `Via`, `X-Forwarded-For`; CDNs add `Age`, `X-Cache`; the `Forwarded` header (RFC 7239) standardizes the X-* mess.

## 10. Time Complexity
- **Per-request overhead**: headers add latency on the wire; HPACK (h2) / QPACK (h3) shrink them to near-O(1) per repeated header. Text headers in h1.1 are O(header bytes) each time.
- **Cache lookup**: 304 revalidation = one round trip + ETag comparison (O(1) string compare) instead of a full body transfer — the bandwidth win is O(payload size).
- **Routing**: method+path matching is O(1) for exact routes; wildcards make it O(route pattern count). 
- **Idempotency keys**: hash lookup O(1) — retries dedupe in O(1).

## 11. Advantages
- **Machine-readable semantics**: caches/proxies act on methods + codes without app knowledge.
- **Safe retries**: idempotent methods make distributed retry safe (the backbone of reliability patterns).
- **Cacheable web**: headers + 304 + ETag drive the CDN/browser cache economy (a huge % of web traffic is cache hits).
- **Extensible**: header registry grows without breaking clients; custom headers (`X-*`) for app needs.
- **Self-describing**: Content-Type + Accept = format negotiation; auth headers = security at the edge.

## 12. Disadvantages
- **Semantics are conventions, not enforced**: nothing *prevents* a server from making GET destructive — clients must trust the server. Apps frequently misuse 200 for everything, defeating machine reasoning.
- **Verbose (h1)**: headers repeated per request — wasteful without h2/h3 compression.
- **Status-code ambiguity**: e.g., 404 vs 403 leakage, 302 vs 303 vs 307 subtlety; "200 with error JSON" anti-pattern breaks monitoring.
- **No built-in auth/idempotency**: Authorization and idempotency are app-implemented; `TRACE`/`CONNECT` need hardening.
- **Header abuse for state**: cookies in headers are a privacy + security surface (CSRF, XSS via cookie stealing).

## 13. Interview Questions
1. **Q: What are the main HTTP methods and their semantics?** A: GET (retrieve, safe), HEAD (headers only), POST (submit/create, unsafe), PUT (replace, idempotent), DELETE (remove, idempotent), PATCH (partial update), OPTIONS (capabilities/CORS), CONNECT (tunnels), TRACE (echo). Safe = no side effect; idempotent = repeat-safe.
2. **Q: What's the difference between safe and idempotent?** A: Safe = no server state change at all (GET, HEAD). Idempotent = repeating produces the same result (PUT, DELETE — repeat is harmless). POST is neither; PATCH may be either. Safe implies idempotent; not vice versa.
3. **Q (tricky): Is DELETE idempotent even when the resource doesn't exist?** A: Yes — deleting a non-existent resource is still "success" (200/204). The *server state after* repeated DELETEs is identical (resource absent). Idempotency is about end-state, not response codes.
4. **Q: When would you use POST instead of PUT?** A: POST = "create under a server-assigned ID" (the URL isn't chosen by the client) or "run an action/process"; PUT = "replace the resource *at this exact URI*" (client chooses the target). POST is also correct for non-idempotent actions (payments, sends).
5. **Q: Explain 2xx/3xx/4xx/5xx with one example each.** A: 200 OK, 201 Created, 204 No Content (2xx); 301 Moved Permanently, 302 Found, 304 Not Modified (3xx); 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests (4xx); 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout (5xx).
6. **Q: What's the difference between 401 and 403?** A: 401 = *unauthenticated* — "who are you?" (provide credentials; usually WWW-Authenticate challenge). 403 = *authenticated but not allowed* — "we know who you are, but you can't do this." Returning 404 instead of 403 is sometimes done to avoid leaking existence.
7. **Q (production): Why does your server return 502 vs 503 vs 504?** A: 502 = upstream sent a bad/invalid response (origin crashed/misbehaved). 503 = the *service itself* is unavailable (overloaded, maintenance; send Retry-After). 504 = gateway/upstream timed out. Load balancers/gateways generate these when the origin fails — they're the *proxy's* view of the origin.
8. **Q: What is 304 Not Modified and how is it used?** A: A conditional GET where the client sends `If-None-Match` (ETag) or `If-Modified-Since`; if unchanged, the server replies 304 with *no body* — the client uses its cached copy. It's how browsers/CDNs revalidate without re-downloading.
9. **Q: 301 vs 302 vs 307 vs 308?** A: 301/308 = permanent (308 preserves method/body); 302/307 = temporary (307 preserves method/body; 302 historically converts POST→GET, superseded by 303). Browsers auto-follow GET redirects; for POST/API use 307/308 to keep semantics.
10. **Q: What headers would you set for an API to prevent caching of sensitive data?** A: `Cache-Control: no-store` (never cache), `Pragma: no-cache` (legacy), and often `Authorization`-checking middleware. For CDN-shared caches, `Cache-Control: private` limits caching to the user's browser.
11. **Q (practical): How does content negotiation work?** A: Client sends `Accept: application/json, text/html;q=0.9` (preference order); server replies with the best format in `Content-Type` (and `Content-Encoding: gzip/br` based on `Accept-Encoding`). Server-driven negotiation vs. the simpler "just send JSON" convention.
12. **Q: What is an ETag and why is it better than Last-Modified?** A: ETag = opaque validator (usually a content hash) that changes when the representation changes. Last-Modified has 1-second granularity and can miss changes. ETags support strong validation (`If-Match`/`If-None-Match`) precisely.
13. **Q (scenario): A client retries a POST after a timeout. How do you keep it idempotent?** A: Use an **Idempotency-Key** header: the server stores (key → response) and returns the stored response for repeat keys. Stripe does this. Alternatively make the action idempotent in business logic (order IDs, unique constraints).
14. **Q: What does `Range` and 206 Partial Content do?** A: `Range: bytes=0-1023` asks for a chunk; the server replies 206 with that chunk. Enables resumable downloads, video seeking, and incremental processing. Servers reply `416 Range Not Satisfiable` for bad ranges.
15. **Q: What is `Cache-Control` max-age vs s-maxage vs no-cache?** A: `max-age=N` = fresh for N s in any cache; `s-maxage` = only shared (CDN) caches; `no-cache` = must revalidate before use (it does NOT mean "don't cache"). `no-store` = truly never store.
16. **Q (tricky): What is CORS and which method/header does it involve?** A: Cross-Origin Resource Sharing — browser security for cross-origin requests. Preflight uses `OPTIONS` with `Access-Control-Request-Method`; the server replies `Access-Control-Allow-Origin/Methods/Headers`. Without it, browsers block cross-origin reads (though simple GET/POST without custom headers skip preflight).
17. **Q: Why is returning 200 with error JSON considered an anti-pattern?** A: It breaks every client/proxy/monitor that switches on status codes — retries, caching, alerting, load-balancer health checks all misbehave. Use real codes (4xx/5xx) and put *business* detail in the body.
18. **Q: What is the `Location` header used for?** A: In 201 (where the new resource is), in 301/302/307/308 (where to redirect), and in 202/3xx for async job status URLs. It's the pointer to the follow-up resource.

## 14. Follow-Up Questions
1. **Q: What is `Expect: 100-continue`?** A: Client asks the server "may I send the body?" Server replies `100 Continue`; saves bandwidth for large uploads the server would reject. Mostly auto-handled by frameworks.
2. **Q: How do idempotency keys interact with retries in distributed systems?** A: The key is hashed/looked-up before processing; concurrent duplicate requests must be deduped (locks, unique DB constraint on key). Storage of (key, response) must be durable. This is a classic system-design pattern (Stripe, payment APIs).
3. **Q: What is 103 Early Hints?** A: Server sends "you'll need these resources" (Link headers) *before* the final response — lets the browser preload CSS/fonts during a slow origin response, improving LCP. HTTP/2-era addition.
4. **Q: When is `HEAD` better than `GET`?** A: For probes: check existence/headers without downloading a body — used by CDNs, link checkers, and monitoring. It must return identical headers to a GET (minus body).
5. **Q: What is `Retry-After` and when is it sent?** A: A response header (429/503/504) telling the client when to retry — a date or seconds. Respecting it prevents retry storms that make outages worse (thundering herd).

## 15. Coding Example
```python
# Express-style routing — methods and status codes drive the API
from http.server import BaseHTTPRequestHandler, HTTPServer

class Api(BaseHTTPRequestHandler):
    users = {}

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/users/"):
            uid = self.path.split("/")[-1]
            if uid in self.users:
                self._json(self.users[uid], 200)          # 200 OK
            else:
                self._json({"error": "not found"}, 404)   # 404
        else:
            self._json({"error": "bad request"}, 400)

    def do_POST(self):
        if self.path == "/users":
            import json
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))
            uid = str(len(self.users) + 1)
            self.users[uid] = data
            self._json(data, 201)                          # 201 Created
            self.send_header("Location", f"/users/{uid}")  # pointer to resource
        else:
            self._json({"error": "method not allowed"}, 405)

    def do_PUT(self):
        # idempotent replace: repeatable, same end-state
        uid = self.path.split("/")[-1]
        length = int(self.headers["Content-Length"])
        self.users[uid] = json.loads(self.rfile.read(length))
        self._json(self.users[uid], 200)

    def do_DELETE(self):
        uid = self.path.split("/")[-1]
        self.users.pop(uid, None)   # idempotent: deleting absent = success
        self.send_response(204)     # 204 No Content
        self.end_headers()
```
```bash
# The three layers in action with curl
$ curl -i -X POST https://api.example.com/users -H "Content-Type: application/json" \
       -H "Authorization: Bearer $TOKEN" -d '{"name":"Ada"}'
# HTTP/2 201 ... Location: /users/42
$ curl -i -H "If-None-Match: \"xyz789\"" https://api.example.com/users/42
# HTTP/1.1 304 Not Modified          <- cache revalidation, no body
$ curl -i https://api.example.com/users/999
# HTTP/1.1 404 Not Found
```

## 16. Industry Usage
- **Stripe**: the canonical idempotency-key API — every POST carries `Idempotency-Key`, stored server-side so retries are safe. Status codes are strict (400/401/402/429).
- **AWS**: S3 uses PUT (object at a key), GET, DELETE; presigned URLs; 304 for conditional GETs; 100-continue for large PUTs. API Gateway/LB route by method+path and emit 5xx on origin failure.
- **Google**: gRPC maps RPC errors to HTTP status codes (e.g., `INVALID_ARGUMENT` → 400, `DEADLINE_EXCEEDED` → 504); Cloud APIs use strict codes.
- **Netflix/Meta**: edge gateways use 3xx for geographic redirects, 429 for abuse throttling, 304 heavily for cache revalidation in their CDN/microservice layers.
- **Cloudflare**: intercepts 5xx to serve error pages/retry; uses `Cache-Control`, `ETag`, and 304s to serve a large fraction of traffic from cache (0 origin hits).

## 17. References
- RFC 9110 — HTTP Semantics (methods, status codes, headers): https://www.rfc-editor.org/rfc/rfc9110
- RFC 9112 — HTTP/1.1: https://www.rfc-editor.org/rfc/rfc9112
- RFC 9113 — HTTP/2, RFC 9114 — HTTP/3.
- RFC 7233 — Range Requests; RFC 5861 — stale-while-revalidate; RFC 8288 — Link headers.
- MDN HTTP documentation — https://developer.mozilla.org/en-US/docs/Web/HTTP
- Stripe API docs (idempotency) — https://docs.stripe.com/api/idempotent_requests

## 18. Cheat Sheet
- Methods: GET/HEAD safe+idempotent; PUT/DELETE idempotent; POST/PATCH not (POST by spec).
- Status: 1xx info, 2xx OK, 3xx redirect, 4xx client, 5xx server.
- 401 = not authenticated; 403 = not authorized; 404 = missing; 429 = throttled.
- 301/308 permanent; 302/307 temporary; 304 = cached copy valid.
- ETag + If-None-Match → 304 revalidation.
- Headers: Authorization, Content-Type, Accept, Cache-Control, Set-Cookie, Location, Retry-After.
- no-store ≠ no-cache; max-age vs s-maxage.
- Range → 206 Partial Content; 416 for bad range.
- Idempotency-Key for safe POST retries (Stripe pattern).

## 19. Quiz
1. Which is safe and idempotent? a) POST b) PUT c) GET d) PATCH → **c**
2. Which is idempotent but not safe? a) GET b) DELETE c) POST d) HEAD → **b**
3. 403 means: a) not authenticated b) not authorized c) missing d) teapot → **b**
4. 304 tells the client: a) redirect b) use cached copy c) server error d) created → **b**
5. 307 preserves: a) nothing b) method + body c) only headers d) cookies → **b**
6. Which status does a rate limiter return? a) 404 b) 429 c) 502 d) 201 → **b**
7. `Cache-Control: no-store` means: a) revalidate b) never store c) store in browser only d) max-age 0 → **b**
8. Range request success code: a) 200 b) 206 c) 226 d) 300 → **b**
9. Which method is used for CORS preflight? a) GET b) POST c) OPTIONS d) HEAD → **c**
10. 504 means: a) origin invalid response b) service unavailable c) gateway timeout d) not modified → **c**

## 20. Flashcards
- **Q: Safe vs idempotent?** → **A:** Safe = no state change (GET/HEAD/OPTIONS/TRACE); idempotent = repeat-safe (GET, PUT, DELETE, HEAD, OPTIONS).
- **Q: 401 vs 403?** → **A:** 401 unauthenticated; 403 unauthorized.
- **Q: 301 vs 307?** → **A:** Both redirects; 301 permanent (may change method), 307 temporary preserving method+body.
- **Q: How does cache revalidation work?** → **A:** ETag + If-None-Match → 304 or 200.
- **Q: POST vs PUT?** → **A:** POST = create with server-assigned ID / action; PUT = replace at client-chosen URI.
- **Q: What header makes retries safe?** → **A:** Idempotency-Key.
- **Q: Which code for too many requests?** → **A:** 429 with Retry-After.

## 21. Revision
Methods define intent: GET/HEAD/OPTIONS/TRACE are safe; PUT/DELETE idempotent; POST/PATCH not. Status codes class responses: 2xx OK (200, 201, 204, 206), 3xx redirect/cache (301/302/307/308, 304), 4xx client (400, 401 vs 403, 404, 429), 5xx server (500, 502, 503, 504). Headers carry metadata: Authorization, Content-Type/Accept (negotiation), Cache-Control/ETag/If-None-Match (caching + 304), Set-Cookie, Location, Retry-After. Idempotency-Key makes POST retries safe. Use real status codes — 200-with-error-JSON is an anti-pattern.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain HTTP methods and idempotency." | 2 How It Works / 13 Q&A |
| "When POST vs PUT vs PATCH?" | 13 Q&A / 15 Coding |
| "401 vs 403 / 502 vs 503 vs 504?" | 13 Q&A / 8 Example |
| "How does ETag / 304 work?" | 9 Internal Working / 13 Q&A |
| "How do you make POST idempotent?" | 13 Q&A / 14 Follow-Up |
| "Cache-Control semantics?" | 13 Q&A / 18 Cheat Sheet |
| "CORS preflight?" | 13 Q&A / 15 Coding |
