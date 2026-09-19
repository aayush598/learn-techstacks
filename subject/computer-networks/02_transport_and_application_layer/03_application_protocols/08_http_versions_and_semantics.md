# HTTP Versions and Semantics — 100 Interview Q&A

## Q1: What is HTTP and what are its core design characteristics?

**A:** HTTP (Hypertext Transfer Protocol) is the application-layer protocol that governs how clients and servers exchange representations of resources on the web. It is a request-response protocol: a client sends an HTTP request asking for an action on a resource identified by a URI, and one or more intermediaries (proxies, gateways, CDNs) may shuttle that request toward an origin server, which returns a response carrying a status code, headers, and usually a body. HTTP was first formalized as an IETF standard in HTTP/1.0 (RFC 1945) and substantially hardened in HTTP/1.1 (RFC 2068, 2616, and the modern RFC 9110-9112 series).

Three design pillars stand out. HTTP is stateless: each request is self-describing, and the server is not required to remember anything between two requests (state is layered on with cookies, tokens, or other headers, not by the protocol core). HTTP is flexible about representations: the same URI can return HTML, JSON, JPEG, or negotiated variants, and the protocol describes how a client and server agree on format, language, and encoding. HTTP is also a "semantics over frame" protocol: modern versions (HTTP/2, HTTP/3) keep the same request/response model, methods, status codes, and headers while radically changing how those messages are transmitted on the wire.

Versioning illustrates the design intent: HTTP/1.1 defines the semantics of methods, status codes, headers, caching, and ranges; HTTP/2 keeps those semantics but replaces text-based lines with binary frames and multiplexing; HTTP/3 repeats the trick over QUIC. This layering means an understanding of HTTP's semantics (what the REST verbs mean, what a redirect implies, when a cache may reuse a response) survives every transport change underneath it.

## Q2: What is the difference between HTTP/0.9, HTTP/1.0, and HTTP/1.1?

**A:** HTTP/0.9 (1991) was an ultra-minimal "simple request" protocol: the client sent only `GET /path` and the server returned raw HTML with no status line, no headers, and no metadata — one method, one content type, and no caching or negotiation. It could barely serve the early web of static pages. HTTP/1.0 (RFC 1945, 1996) added the full request line (method, URI, version), status codes, headers, and support for arbitrary body types — but by default every request opened a new TCP connection and closed it when the response finished. That per-request connection churn is the defining inefficiency of HTTP/1.0.

HTTP/1.1 (RFC 2068, then 2616, then the modern split across RFC 9110-9112) fixed the connection model and much more. It made persistent (keep-alive) connections the default, requiring the server to maintain a reusable connection; it mandated the Host header so one IP address could host many virtual servers; it added chunked transfer encoding so responses of unknown length could be streamed; and it formalized caching, content negotiation, conditional requests, range requests, and the richer status/method vocabulary. It also added new methods (OPTIONS, and defined semantics for others) and more precise header semantics.

Two generations of fixes followed for HTTP/1.1's residual wounds: pipelining (a partial attempt at concurrency on one connection) and, later, HTTP/2's multiplexing. But even today, HTTP/1.1's text-based framing, with its connection-per-host limits and head-of-line blocking, is what HTTP/2 and HTTP/3 were built to replace while keeping the semantics HTTP/1.1 established.

## Q3: What is an HTTP method, and what are the core methods defined by HTTP?

**A:** An HTTP method (also called a request method or verb) is the token, placed first in a request line or in the :method pseudo-header, that describes the action the client is requesting on the identified resource. Methods are the heart of HTTP semantics: they tell the server what operation is desired (retrieve, create, replace, delete, inspect, tunnel, etc.) and they carry normative properties — safety and idempotency — that govern retries, caching, and proxies. The core methods standardized in RFC 9110 are GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, and TRACE.

GET retrieves the current representation of a resource and is the single most common method. HEAD is GET without a response body, useful for checking existence, size, or freshness without transferring data. POST sends a representation to be processed by the target resource; it is the general-purpose "act on the server" verb, used for form submission, JSON API creation, and RPC-style actions. PUT replaces the target resource's state with the submitted representation; DELETE removes the resource. OPTIONS asks about capabilities (typically yielding an Allow header), CONNECT establishes a tunnel (most prominently for proxied HTTPS), and TRACE echoes the request back for diagnostic purposes.

Beyond the core eight, HTTP allows extension methods, and WebDAV (PROPFIND, MKCOL, LOCK, etc.) is the canonical extension set. The Web platform frequently maps them onto REST: GET/POST/PUT/DELETE (and sometimes PATCH) cover CRUD, with PATCH being a partial update that is intentionally neither purely idempotent nor safe by definition. Understanding which method to use for which semantic is what separates well-designed HTTP APIs from ad-hoc ones.

## Q4: What is the difference between a request header and a response header?

**A:** A request header is a name-value pair sent as part of an HTTP request, conveying metadata the server needs to act and respond correctly: what the client can accept (Accept, Accept-Language, Accept-Encoding), how the body is coded (Content-Type, Content-Length), the client's identity (User-Agent), the host being addressed (Host), authentication credentials (Authorization), and caching/conditional state (If-None-Match, Cache-Control). A response header travels in the response message and tells the client what the server did: the representation's type and length (Content-Type, Content-Length), caching instructions (Cache-Control, Age, ETag), sender identity (Server), and control fields like Location (for redirects), Retry-After, and Allow.

Many header names appear in both directions with different or shared meaning: Content-Type is a representation header that applies to whichever body accompanies the message, so it can appear in either request or response; Cache-Control appears in both; User-Agent is request-only and Server is response-only. Headers are grouped into four categories in the modern spec: connection-wide general headers, request headers, response headers, and representation headers describing the transferred resource.

The pragmatic consequence for debugging is asymmetric: a request tells the server what the client wants and can produce; a response tells the client what the server produced and how to handle it. When an API misbehaves, the first debugging step is often to check whether the response headers contradict the request's Accept — that asymmetry (server sent JSON despite Accept: application/xml) is where most negotiation bugs live.

## Q5: What is an HTTP status code, and how are status codes grouped?

**A:** A status code is a three-digit integer in the response's status line (and the :status pseudo-header in HTTP/2/3) that summarizes the result of the server's attempt to fulfill the request. The first digit defines the class of outcome; the remaining two digits provide granularity. The classes are: 1xx informational (request received, processing continues), 2xx success (the request was understood, accepted, and processed), 3xx redirection (the client must take further action, typically by following a Location), 4xx client error (the request was bad — wrong syntax, missing permission, nonexistent resource), and 5xx server error (the server failed to fulfill an otherwise valid request).

The classes carry semantic weight beyond the number: 2xx is committable (the operation happened), 3xx is a pointer (follow me), 4xx is blame (your request, not my problem — fix it client-side), and 5xx is liability (my fault; retry may help). This classification drives client behavior automatically: browsers render 4xx as errors, honor redirects up to a bounded number of hops, and treat 5xx with retry heuristics. Load balancers and proxies make routing and retry decisions based purely on the class (e.g., don't retry a 400, do retry a 502 with care).

For API design, the class is usually more important than the exact code: 2xx signals success semantics, 4xx must not be retried blindly, and 5xx signals a transient condition where idempotent retries are reasonable. Knowing the common codes (200, 201, 202, 204, 206, 301, 302, 303, 304, 307, 308, 400-410, 413, 415, 422, 426, 429, 500-503, 504) and their canonical meanings is table stakes for senior HTTP work.

## Q6: What was the main limitation of HTTP/1.0 compared with HTTP/1.1?

**A:** HTTP/1.0 opened a brand-new TCP connection for every request and closed it after the response. On a page with dozens of resources, the browser opened dozens of TCP connections, each requiring a three-way handshake (one RTT) and, on HTTPS, a full TLS handshake (another one to two RTTs). On high-latency paths those extra round trips dominated page load time, and server stacks paid connection setup/teardown and per-socket memory overhead for every single fetch. This connection-per-request model is the defining inefficiency that HTTP/1.1 was invented to kill.

HTTP/1.1 made persistent (keep-alive) connections the default and formally defined the mechanics: the connection stays open across multiple request/response exchanges, with Content-Length or Transfer-Encoding delimiting message boundaries so the next response can be read off the same socket. It also added critical correctness features HTTP/1.0 lacked — the mandatory Host header for virtual hosting, chunked transfer encoding for streaming responses, and tighter framing rules — all of which were impossible or ambiguously defined in 1.0.

The architectural lesson persisted: connection reuse is the single cheapest latency optimization a protocol can make, and it is why HTTP/1.1 keep-alive, HTTP/2's single multiplexed connection, and HTTP/3's QUIC connection all share the same philosophy. The remaining HTTP/1.1 wound — that one connection still processes one response at a time, so parallelism requires many connections — became the target that HTTP/2 explicitly solved.

## Q7: What is a keep-alive (persistent) connection in HTTP/1.1, and how does it work?

**A:** A persistent connection is a TCP connection that the client and server agree to reuse for more than one request/response exchange instead of tearing it down after each message. HTTP/1.0 used `Connection: keep-alive` as an opt-in; HTTP/1.1 reversed the default so that persistent connections are the norm unless the message says `Connection: close`, which explicitly requests that the connection be closed after the exchange. Browsers typically reuse a handful of keep-alive connections per origin instead of opening one per request.

For the mechanism to work safely, both sides must know where one message ends and the next begins. That is solved by delimiting the body: with Content-Length the receiver knows when to stop reading, and with chunked transfer encoding the receiver reads chunk-size-prefixed segments until a zero-length terminator. If framing is wrong, a receiver will misparse the bytes of two responses as one response — the root cause of request/response smuggling, which is why HTTP/1.1 framing rules are precise and why servers aggressively reject ambiguous messages.

The benefits are latency (no handshake per fetch) and server efficiency (fewer sockets), and the costs are keepalive bookkeeping: servers must enforce idle timeouts, bound connections per client, and handle half-closed states cleanly. When HTTP/2 arrived, it replaced the multiple parallel keep-alive connections with one multiplexed connection carrying many concurrent logical streams — the same "reuse the expensive TCP+TLS setup" insight taken further.

## Q8: HTTP is described as stateless. What does that mean and how does the web layer state on top?

**A:** Stateless means the protocol core does not require the server to retain any per-client memory between requests; every request carries the information needed to understand itself. The server does not (by the protocol) know whether two requests come from the same user or how many requests preceded them. This property is what makes HTTP scalable — a stateless server can be replicated, load-balanced, and taken down and replaced without affecting correctness, because no session state lives on the server by default.

The web layers state on top through explicit, optional mechanisms: the Cookie header (a small token the server issues and the client echoes back), URL-based session identifiers (path or query parameters), Authorization headers (per-request credentials), and increasingly JWT or signed tokens in headers. All of these are "explicit state tokens" that travel with each request, which preserves the ability to replicate and scale while giving applications the illusion of stateful sessions. Cacheable responses benefit from statelessness too: a shared cache can serve the same representation to everyone because there is no per-user dependency unless response headers announce one (like Vary: Cookie).

The senior nuance is that statelessness is a spectrum, not a binary: a server may still keep caches, in-flight coordination, and connection state (a keep-alive connection is itself server state), but protocol correctness never depends on remembering one exchange to interpret the next. This is why "make your API stateless" is such durable advice — it buys elasticity, and the header machinery gives you the escape hatch when genuine session state is unavoidable.

## Q9: What is the difference between a URI, a URL, and a URN?

**A:** URI (Uniform Resource Identifier) is the umbrella term for any string that identifies a resource on the web; URL (Uniform Resource Locator) and URN (Uniform Resource Name) are its two specializations. A URL tells you not just what the resource is but where and how to retrieve it — `https://example.com/path?q=1#frag` carries the scheme (https), authority (example.com), path, query, and fragment, and is sufficient to initiate a fetch. A URN identifies a resource by name in a persistent, location-independent namespace (like `urn:isbn:0451450523` for a book), but does not by itself say how to get it.

A URI is a URL if it contains a scheme plus the addressing information needed to locate the resource (scheme, authority, path, query) and a URN if it uses a registered formal namespace. Every URL is a URI, every URN is a URI, and some schemes are ambiguous until parsed. Within HTTP, almost everything you manipulate is a URL — the request target and the Host header combine to form the effective target, and HTTP semantics operate on resources identified by URIs; redirects hand you a new URI to follow.

For interviews, the crisp distinction matters in caching and routing: caches key responses by the URL (including scheme/host/path/query, and accounting for the Vary header), while the entity being identified is the resource the URI points to — the same URI can return different representations, the fragment never leaves the client, and two URIs can identify the same resource (alias). Grasping this is prerequisite to reasoning correctly about cache invalidation and canonicalization.

## Q10: What is the Host header and why did HTTP/1.1 make it mandatory?

**A:** The Host header names the virtual host (the hostname) the client is trying to reach, e.g., `Host: www.example.com`. HTTP/1.0 had no such header, which meant a single IP address could serve only one site cleanly; HTTP/1.1 made Host mandatory so that one IP address could host many "virtual hosts" — many distinct websites, each keyed by hostname. It is part of the request's target identification: in a standard request line `GET /index.html HTTP/1.1`, the path is `/index.html` and the authority comes from Host.

Because Host is part of the effective request target, it participates in routing, caching, and access control. Proxies and CDNs use it to select the correct backend; web servers use it to select the correct virtual host's configuration; caches must key by the full authority to keep two sites on one IP from cross-contaminating. Security-critical behaviors hang on it too: an HTTP request with a Host claiming a name the server does not serve is typically rejected, and Host-header confusion has been a rich source of password-reset poisoning and cache-poisoning attacks.

The senior-grade subtlety is that HTTP/2/3 repeat this differently: the authority travels in the `:authority` pseudo-header, and HTTP/2 dropped URI-form request targets for most requests (using `:scheme`, `:authority`, and `:path` instead). The semantic stays identical — every request must say which host is authoritative — but the wire representation changed, so security filters written against "the Host header" must be rewritten to inspect pseudo-headers.

## Q11: What does it mean for an HTTP method to be idempotent, and which methods are idempotent?

**A:** Idempotency means that performing the same request multiple times produces the same server-side effect as performing it once — later repetitions must not change the outcome beyond the first execution. Formally, RFC 9110 says the client can repeat a request with identical consequences to a single execution (the response may of course differ, but the resulting resource state is the same and no additional harm is done). Idempotency is a property of the method's semantics, not of the request's bytes.

GET, HEAD, PUT, DELETE, OPTIONS, and TRACE are idempotent. GET and HEAD are also safe (read-only); PUT is idempotent because it converges the resource to the submitted representation; DELETE is idempotent because deleting an already-deleted resource is a no-op. POST is NOT idempotent — submitting a form twice creates two records or charges twice — and PATCH is NOT guaranteed idempotent (a JSON-Patch or merge-patch may be repeatable or not, but the spec deliberately does not promise it).

Idempotency exists to justify automatic retries. A client, proxy, or load balancer that sees a network failure can safely replay an idempotent request; doing so for POST could duplicate side effects. This is why senders retry GET/PUT/DELETE aggressively but require application-level idempotency keys for POST. Every serious HTTP API design (payments, orders, distributed systems) leans on this distinction, and understanding it is non-negotiable for senior interview work.

## Q12: What is a safe method, and what does "safe" operationally mean in HTTP?

**A:** A safe method is one that, by definition, does not modify the resource on the server: the request must not change the state of the origin resource in any way a fetch of that resource would detect or a side-effectful operation would cause. GET, HEAD, OPTIONS, and TRACE are safe. Formally RFC 9110 says a request is safe when it "does not alter the state of the origin server" — read-only in intent. Notably, safety is a normative claim about the method's semantics, not a performance guarantee: a GET can still trigger logging, analytics, and rate counting, but it must not mutate the resource.

Safety matters in three places. (1) Automation: automated agents, crawlers, and link-prefetchers must be able to issue safe requests without asking "can this mutate my data?" — that is why browsers and crawlers are allowed to prefetch GETs but never POSTs. (2) Prefetching and preloading: an `<img>`, a `<link rel="preload">`, or an early-hints hint is only safe to follow if the underlying method is safe. (3) Caching and retries: safe methods are cacheable by default, and caches can share responses across users without violating safety.

The senior nuance is the "semantic vs declarative" trap: a service may advertise `POST /report` while a client wants "safe status"; the method names are what carry the contract, not the path. That is why RESTful APIs use GET for reads, and why APIs that send all operations as POST (SOAP, many GraphQL transports) lose the safe/idempotent guarantees automatically and must re-implement them per-op.

## Q13: What does the Content-Type header convey, and how does it relate to MIME types?

**A:** Content-Type is the representation header that names the media type of the message body, using the MIME-type syntax made famous by email: a type/subtype pair like `text/html; charset=utf-8`, `application/json`, `multipart/form-data; boundary=...`, or `image/png`, optionally followed by parameters such as charset or format subtyping like `application/vnd.api+json`. It is how a server tells a client how to interpret the bytes it is about to receive, and how a client tells a server what format it is submitting. It is a representation header, so it describes the body of whichever message it appears in.

The practical rules are strict: the types themselves are registered with IANA, and parsers distinguish the generic types (text, image, audio, video, application, multipart, message, font, model) from structured syntax suffixes like `+json` and `+xml`, which let code detect "this is JSON regardless of the vendor type." CSS, HTML, and JavaScript are notoriously content-type-sensitive because browsers enforce MIME sniffing protections: a server that says `text/plain` for something a page expects to execute as script gets blocked, which is why `X-Content-Type-Options: nosniff` is recommended.

For API design, Content-Type is dual-use: `application/json` in a request says "I am sending JSON," and Accept in the same request says "I prefer to receive JSON," and the pair drives content negotiation. Misalignment between the two is a classic 415 (Unsupported Media Type) or 406 (Not Acceptable) error source, so senior engineers treat Content-Type and Accept as a coordinated pair rather than two unrelated headers.

## Q14: What is the difference between a header, a body, and a representation in HTTP messages?

**A:** An HTTP message consists of a start line (request line or status line), a set of headers, and optionally a message body. Headers convey metadata about the message and its transfer — what is being sent, how it is encoded, how it is delimited, who sent it — while the body carries the actual payload data. In HTTP/1.x the body follows a blank line after the headers and is delimited by Content-Length or chunked encoding; in HTTP/2 and 3 the body is carried in the DATA frames of a stream, and metadata has moved to pseudo-headers and frame types.

A representation is a higher-level concept: the combination of the resource's current data with its representation metadata (headers like Content-Type, Content-Language, Content-Encoding, ETag, Last-Modified, and Content-Location that describe that data). The same resource can have many representations — HTML and JSON views of the same object, UTF-8 vs UTF-16 text, gzip vs plain — and content negotiation is the process of selecting which representation to return. The body is the transport of one representation; the header set describes how to interpret it.

The distinction carries a famous trap: Content-Length refers to the message body (encoded bytes as transported), NOT the representation size (the decoded resource). If a response is gzip-compressed, Content-Length describes the compressed body; the client decompresses to obtain the representation. Caching, range requests, and integrity checks operate on these different notions — ETag and Content-Location are representation-level, while Transfer-Encoding is message-level — and conflating them is a classic source of cache bugs.

## Q15: What is the difference between 200 OK, 201 Created, and 204 No Content?

**A:** 200 OK is the general success response: the request succeeded, and the response body carries the result — for GET, the current representation of the resource; for PUT, commonly the updated representation. 201 Created is the success response for a request that resulted in the creation of a new resource, most naturally emitted by POST-to-a-collection or sometimes PUT-to-a-new-URI; it should carry a Location header identifying the newly created resource and usually a body describing or reflecting the new state. Failures to distinguish the two are among the most common API-design errors.

204 No Content means the request succeeded but there is intentionally NO body in the response — no representation, no bytes. It is the canonical response for DELETE (the resource is gone; nothing to say back) and for background-processing actions that produced no immediate data. Because there is no body, 204 must never carry body bytes — it is the "success, nothing to show" code.

The senior distinction is about what each code implies for the client: 200 says "here is the thing you asked about," 201 says "I made a new thing and here is where to find it," 204 says "the thing you asked for has been done and there is nothing to look at." All three are success, but only 201 invites a follow-up fetch (of the Location), and only 200 invites interpretation of the returned body. Choosing among them per operation is one of the highest-leverage semantic decisions in API design.

## Q16: What are 3xx redirection status codes, and what does the Location header do?

**A:** A 3xx status code signals that the client must take further action to complete the request, almost always by issuing a new request to a different URI. 301 Moved Permanently and 308 Permanent Redirect indicate the target resource now lives at the URI in the Location header and future requests should use it; 302 Found and 307 Temporary Redirect are ephemeral (used for login redirects, maintenance pages, and localization), telling the client to fetch the new URI for THIS request while keeping the old URI canonical; 303 See Other redirects a POST result to a GET of a new URI — the famous Post/Redirect/Get pattern that prevents duplicate form submissions on refresh. There is also 304 Not Modified, which is not a redirect to a new location at all but a cache validation response.

The Location response header carries the absolute or relative URI to follow. Its semantic weight depends on the code: a 301/302/307/308 FORCES a new request (automatically followed by browsers with an internal redirect up to a limited hop count), whereas a 304 means "use your cached copy." The method-rewriting history matters enormously: the original 301/302 officially allowed clients to rewrite a POST into a GET when following the redirect, and browsers still do that for 301/302 (and 303 mandates it), while 307 and 308 were created specifically to preserve the original method and body.

The senior traps are canonicalization and method handling: a 301 from http to https, from www to apex, or from trailing-slash to non-slash variants is how links converge; a 307 from a form POST that then loses the body on a proxy retry is a classic production bug; and cache invalidation via 301 must never point clients back in a loop. Knowing exactly when to use 301 vs 307 vs 308 is a standard senior-interview differentiator.

## Q17: What are the most important 4xx client-error status codes and what do they mean?

**A:** 4xx codes blame the request: the client sent something invalid and must fix it before retrying. The workhorses are: 400 Bad Request (malformed syntax or a request the server cannot parse into coherent semantics), 401 Unauthorized (you are not authenticated — and the response should include a WWW-Authenticate challenge), 403 Forbidden (you are authenticated but NOT allowed — do not retry without a permission change), and 404 Not Found (that resource does not exist here — and scheduling 404 is how sites conceal things they prefer not to reveal). 405 Method Not Allowed means the resource exists but you used the wrong verb, and the Allow header tells you the permitted methods.

The semantic failures deepen: 409 Conflict (your request contradicts the current state, e.g., creating something that already exists), 410 Gone (the resource once existed and is deliberately gone — useful for SEO because it signals permanence), 422 Unprocessable Content (the server understood the syntax but the content's semantic rules are violated — the JSON parsed but the email field is invalid), 429 Too Many Requests (you are rate-limited; honor Retry-After), and 413 Content Too Large, 415 Unsupported Media Type, 416 Range Not Satisfiable, and 426 Upgrade Required.

The senior rule: 400 for unparseable syntax, 401/403 for the authN/authZ split, 422 for well-formed-but-invalid business rules, 404/410 for existence vs permanent-gone, and 429 for throttling. Getting 401 vs 403 wrong (unauthenticated vs unauthorized) and 400 vs 422 wrong (syntax vs semantics) is the marker of junior API work; senior engineers also know that 404 over-detailing resource existence leaks information and that retries must never be automatic for any 4xx without idempotency guarantees.

## Q18: What are the main 5xx server-error status codes and how should clients treat them?

**A:** 5xx means the server failed to fulfill an otherwise valid request, and the blame sits server-side. 500 Internal Server Error is the catch-all (an unhandled exception, a bug); 501 Not Implemented means the server does not support the requested capability (the method or transfer coding is unknown); 502 Bad Gateway says an upstream returned an invalid response or the gateway itself failed; 503 Service Unavailable is the deliberate "I am overloaded or down for maintenance" signal, which SHOULD carry a Retry-After header; and 504 Gateway Timeout says an upstream did not respond in time. 507 Insufficient Storage and 508 Loop Detected are less common extension codes.

The semantically important property of 5xx is transience: any 5xx MAY be retried, and well-behaved clients do retry, using Retry-After when present and otherwise exponential backoff with jitter. Load balancers convert internal errors into 502/503/504 and add retry policy with idempotency awareness. A 500 for an idempotent PUT can be retried safely; a 500 for a POST cannot be blindly re-sent — hence "don't retry non-idempotent 5xx without an idempotency key."

The senior distinctions: 503 is the "shed load" signal and should be emitted by gateways under overload BEFORE work is committed, while 502/504 indicate upstream failure; a 500 that reveals a stack trace is a bug AND a security leak. Differentiating "server down" (503/502/504, retry sensible) from "server broken for this request" (500, investigate) from "server can't do this at all" (501) is reasoning load-balancer retry logic runs on daily.

## Q19: How do cookies work at the HTTP layer, and how do they interact with requests and responses?

**A:** A cookie is a small name-value piece of state that the server asks the client to store and echo back. The flow: the server's response includes a `Set-Cookie` header with a name, value, and attributes such as Domain, Path, Secure, HttpOnly, SameSite, and Max-Age/Expires; the browser stores it scoped to that domain and path; on subsequent requests to matching URLs, the client attaches a `Cookie: name=value...` header. This is how a stateless protocol becomes apparently stateful: the client presents the stored token with each request, and the server can rebuild the session or identity from it.

The attributes are load-bearing security surfaces. Domain and Path scope the cookie to the right hosts and paths; Secure restricts transmission to TLS; HttpOnly hides it from JavaScript (blocking XSS theft of session tokens); SameSite governs whether the cookie is sent on cross-site requests (Lax by default in modern browsers, Strict even tighter, None requires Secure) — the primary defense against CSRF. Max-Age/Expires control lifetime. The cookie jar is effectively a per-origin key-value store shared with the server's Set-Cookie writes.

The senior complexity lives in cookies' interaction with HTTP caching and privacy: because Set-Cookie responses are typically not cacheable and Cookie-bearers vary responses, shared caches must honor Vary: Cookie or Cache-Control restrictions; and a cookie that indiscriminately scopes to Domain=.example.com leaks across subdomains. Size caps matter too: browsers cap cookies (~4096 bytes each, ~50 per domain), and oversized or duplicated cookies are silently dropped — a classic cause of "session works in test, breaks in prod."

## Q20: How do GET and HEAD differ, and why is HEAD important?

**A:** GET requests the current representation of a resource; the server responds with a status line, headers, and the full body. HEAD is identical in every way except that the response MUST NOT include a body — the server sends the same headers it would for a GET (Content-Type, Content-Length, ETag, Last-Modified), but no entity bytes. The client sends `HEAD /path HTTP/1.1`, the server computes the headers as if for a GET, and the response body is empty. HEAD therefore lets a client inspect a resource without transferring it — the "peek, don't fetch" verb.

HEAD's value is operational: a client can check whether a large asset has changed (via ETag or Last-Modified in headers) before downloading it, verify existence and permissions cheaply, learn the Content-Length to decide whether an asset is too big, and warm caches. HTTP caches are required to handle HEAD by serving the cached GET headers. Because HEAD eliminates the body, it halves the bandwidth of metadata probes — the reason monitoring tools and service checks use HEAD natively.

The subtle requirement is that a server is REQUIRED to behave such that a HEAD response is, semantically, the GET headers with the body stripped, and if custom headers are computed dynamically, they must be computed for the HEAD path too, not given a stub. A senior interviewer checks whether you know that HEAD is not "GET minus body" sloppily implemented but a full-budget metadata operation — and that some implementations incorrectly serve cached GET body bytes to a HEAD, which leaks data.

## Q21: What does the User-Agent header convey, and what are its modern concerns?

**A:** User-Agent is a request header identifying the client software that is making the request — historically a long string combining product tokens like `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`. Browsers craft these strings with trademark surfacing so that server features work correctly, and beyond browsers the header identifies bots (Googlebot, curl/8.x, python-requests/x.y) and other clients. It is the single most common signal servers use to change behavior — redirect to a mobile site, serve a different layout, block a scraper.

The header's security posture is more complex than it looks. User-Agent is trivially spoofable — any HTTP library can claim to be Chrome — so servers must never treat it as a security boundary; anti-bot systems pair it with other signals (IP, TLS fingerprinting, request heuristics). Privacy groups have also curbed the header: browsers reduce its entropy and reserve granular exposure for client-hints headers (Sec-CH-UA-*). The header should never be used for cache keys or rate-limit identity.

The senior concern is that User-Agent also perpetuates feature fragmentation via UA-sniffing: serving content conditional on UA strings creates a permanent maintenance tax and invites bugs — which is why modern guidance is to prefer feature detection via Client Hints and to treat UA as legacy. Its survival matters mostly for bot identification and legacy sites; its replacement is the HTTP Client Hints ecosystem.

## Q22: What are Accept/Accept-* headers, and how does content negotiation work in HTTP?

**A:** Content negotiation is the process by which the client and server pick the representation of a resource to exchange. On the client side it is expressed with a family of Accept headers: `Accept` (the media types the client will accept — e.g. `Accept: application/json`), `Accept-Language` (natural language preferences like `en-US,en;q=0.9`), `Accept-Encoding` (transfer codings the client can decode, e.g. `gzip, br`), and `Accept-Charset` (mostly legacy). Each Accept value can carry a quality value `q=0.9` expressing relative preference, so negotiation is a weighted match against what the server can produce.

The server then chooses: the modern spec prefers the exact Accept match with highest quality, or, failing equality, a heuristic the server defines; once chosen, the server MUST attach `Vary` listing the request headers that influenced the choice, so caches know the response is not universally reusable. Media-type extensions (like `application/vnd.api+json`) participate via type/subtype matching and parameters.

The senior pitfall is cache correctness: a shared cache must treat Vary: Accept responses as distinct variants per Accept value, and mishandled Vary is the cause of "one user gets HTML and another gets JSON from the same URL" production bugs and of sensitive-data leaks when caches hand a variant to the wrong client. Also, q-values are relative preferences, and a server may serve a less-preferred but still-negotiable representation if the preferred one is unavailable — the correct answer to "why does my curl without Accept return the wrong format?" is usually "you sent no Accept, so the server's default won."

## Q23: What is the relationship between HTTP semantics and HTTP over TLS (HTTPS)?

**A:** HTTPS is HTTP's semantics executed over a TLS-encrypted, authenticated transport. Everything that makes HTTP semantics — methods, status codes, headers, caching, retries — is identical; TLS merely replaces the transport under the messages with a channel that provides confidentiality (nobody on-path reads the request/response), integrity (nobody on-path tampers), and authentication (the client verifies the origin via the server's certificate chain). The URL scheme changes (https://), the default port changes (443), and the framing is protected, but the request/response grammar is unchanged.

The security consequences are layered: without TLS, any on-path attacker can read, rewrite, or replay HTTP messages, poison caches, inject content, and hijack sessions; with TLS, the same attacker sees only encrypted bytes. Because HTTP semantics assume the wire is trustworthy (a 301 redirect is followed based on its content), HTTPS is what makes those semantic contracts actually safe to honor. This is why the modern web treats "HTTP semantically correct but unencrypted" as a defect, and why security headers (Secure cookies, HSTS, CSP) are defined assuming TLS is present.

The rigorous distinctions: TLS protects a specific transport connection — it does not change HTTP semantics such as idempotency, caching, or method safety. Replay protection against a network attacker comes from TLS for the packet stream, while application-layer replay protection for 0-RTT comes from the idempotency of the HTTP methods being replayed. Metadata like destination IP, port, sizes, and timing remains observable under HTTPS.

## Q24: What are the default ports for HTTP and HTTPS, and how do ports participate in URL and Host handling?

**A:** HTTP's default port is 80 and HTTPS's default is 443; a specification-declared scheme lets a URL omit the port entirely. When a non-default port is present (`https://example.com:8443/...`), it is part of the URI's authority for identifying the resource, and the request's Host header or `:authority` pseudo-header includes it (`Host: example.com:8443`). The default-port rule is a URI-scheme normalization: `http://example.com:80/` and `http://example.com/` identify the SAME resource, while an explicit non-default port changes identity.

Ports matter contextually in several places. First, the authority includes the port, so cookie scoping, cache keys, and CORS origin checks treat `https://a.com` and `https://a.com:8443` as different origins. Second, mixed-content policies treat ports on HTTPS pages strictly. Third, TLS certificates bind identity to hostname, not port, so a certificate normally covers all ports of the named host; but a server's virtual-host selection keys on the Host INCLUDING port.

For the interview, the takeaways are: the port is part of the authority the request carries; normalization happens only for the scheme-default port; and every place HTTP semantics compare or key by origin (cookies, CORS, caching, CSRF, WebSocket upgrade) is port-sensitive. The infamous password-reset hijack via Host-header port-faking works precisely because a port number travels with the authority and, if echoed into a reset link, changes which origin receives the token.

## Q25: What does `Connection: close` mean, and how do hop-by-hop headers differ from end-to-end headers?

**A:** `Connection: close` is a request or response header that tells the peer to close the TCP connection after the current message exchange instead of keeping it alive. In HTTP/1.x it is how either side opts out of persistent connections; the modern interpretation is that a server sends it to signal "this is the last response on this connection," and a client sends it when it does not want to reuse the socket. Sending it also means subsequent requests on that connection would be protocol violations, so proxies handle connection-related details carefully.

The deeper semantic is the distinction between hop-by-hop and end-to-end headers. End-to-end headers are meaningful only between the client and the ultimate recipient (the origin): Content-Type, ETag, Cache-Control, Authorization, etc., must be preserved (or deliberately modified) across intermediaries. Hop-by-hop headers are consumed and produced BY EACH INTERMEDIARY and must never be forwarded: these are exactly the headers named in the Connection header (Connection itself, and whatever it lists), plus a fixed set — Transfer-Encoding, Keep-Alive, TE, Upgrade, Proxy-Authenticate, Proxy-Authorization. If a header is hop-by-hop, a proxy must strip it before forwarding.

The correctness consequences: HTTP/2 and HTTP/3 ABOLISHED the Connection header (they cannot express `Connection: close`; connection state is per-stream, and connection-level signaling moved to frames like GOAWAY). But the hop-vs-end distinction survives, and the famous "hop-by-hop header smuggling" exploits the gap where one proxy strips a header and the next does not — precisely because the two classes are processed at different network positions.

## Q26: What is HTTP pipelining, and why did it fail in practice?

**A:** Pipelining is HTTP/1.1's attempt to parallelize: after sending request A, a client sends requests B and C on the same connection WITHOUT waiting for A's response, and the server is supposed to respond to them in FIFO order on the same socket. The idea is to amortize connection setup and let multiple requests ride one RTT. It was standardized in HTTP/1.1 and almost nobody deployed it successfully in browsers. The theory: four simple GET requests could arrive in one round trip.

The failures were practical and architectural. First, responses are strictly FIFO: if request B produces a slow response, responses C through Z wait behind it — head-of-line blocking at the byte-stream level. Second, servers and proxies implemented pipelining inconsistently: some reordered responses, some did not, so clients could not rely on the ordering; many rejected pipelined requests to close the connection. Third, half-duplex UI interference — users navigate away, browsers abort, and pipelining interacted badly with connection resets and retry logic. Fourth, security: some intermediaries mishandled pipelined request framing.

The lesson HTTP/2 learned was to never let one request block all others, and to make parallelism a per-stream property on ONE connection rather than best-effort ordering within the single byte stream. Pipelining is now uniformly disabled in browsers and deprecated in modern guidance; when an interviewer asks, the expected answer is: same-connection concurrency was a good idea, FIFO-response ordering and lack of control was its fatal flaw.

## Q27: What is head-of-line blocking in HTTP/1.1, and what are its two flavors?

**A:** There are two distinct head-of-line (HOL) problems in HTTP/1.1. The first is at the connection level: a single TCP connection delivers responses strictly in order, so if request 1's response is huge or slow, the responses to requests 2-5 — even if tiny and fast — must wait behind it. This is called response head-of-line blocking, and it is why browsers open six-ish parallel connections per origin, but that only multiplies the connection count, not eliminate the serialization for the requests assigned to each socket.

The second flavor sits one layer down: TCP itself guarantees ordered delivery of its byte stream, so if a segment is lost, the receiver stops delivering all later bytes until retransmission arrives — data HOL blocking that affects EVERY stream using that connection, regardless of application priorities. In HTTP/1.1 the two combine: a single lost packet stalls a response caravan, and a large first response stalls everything behind it.

HTTP/2 fixed the first flavor (multiple streams multiplexed over one connection, each with independent progress) but NOT the second (they still share one byte stream, so an underlying TCP loss stalls all multiplexed streams). HTTP/3 fixed both by moving stream multiplexing into the transport itself via QUIC, so loss on one stream's packets does not delay other streams. An interviewer asking this wants you to separate "application-layer serialization" from "transport-layer serialization" — the two HOLs, two fixes, and two remaining failure points.

## Q28: How does HTTP/1.1 handle multiple requests to the same server — what concurrency model does it offer?

**A:** HTTP/1.1 offers a connection pool model: a client opens a small set of persistent connections to the same origin (typically one to six), queues requests per connection, and processes them FIFO on each socket. The pool gives parallelism without violating "one response at a time per connection"; six connections means up to six in-flight requests. This is a genuine concurrency model but a crude one: parallelism is bounded by the pool size, and each connection is a serial conveyor belt.

The inefficiencies are structural. With a pool of six, a page loading sixty assets runs ten waves of six; a single slow asset can backlog its connection's queue while other connections idle. HTTP/2's answer is one connection carrying many multiplexed streams — concurrency without a pool — which removes both the queue-per-connection imbalance and the per-connection TCP/TLS overhead. The cost of HTTP/1.1's model shows directly in high-latency or slow-server scenarios: pool concurrency does not help when every connection waits on an ordering queue.

The senior view frames the connection pool as an application-layer policy: clients tune it (idle timeouts, per-host max, keep-alive reuse) and servers tune it too (per-IP limits, max connections, idle timeout). Pool sizing is a perpetual latency/headroom trade: too few connections underutilize the path, too many crowd the server and burn memory — an optimization problem HTTP/2 largely dissolves by multiplexing within one flow-controlled connection.

## Q29: What is virtual hosting, and how does the Host header enable it in HTTP/1.1?

**A:** Virtual hosting is serving multiple logical websites from a single IP address and server process, distinguished by the hostname the client is trying to reach. In HTTP/1.0, one server exposure could not distinguish `a.com` from `b.com` because the request target was only a path; HTTP/1.1 made the Host header mandatory so the request target became (authority, path): `GET /index.html HTTP/1.1` plus `Host: a.com` identifies which site's tree to serve.

This single semantic made the commercial web viable: shared hosting put thousands of sites on one box, and HTTPS added a twist — TLS was selected per certificate, and the SNI extension of TLS 1.2/1.3 carries the hostname before any HTTP bytes, so the connection can be matched to the virtual host even during the handshake. Virtual hosting is also how CDNs and load balancers route: the Host header selects the backend pool.

The attack surface moves with it: Host header confusion/poisoning (an attacker sets Host: victim.com to get the server to generate a URL that redirects traffic or a password reset to the attacker's server), and cache poisoning via Host. Mitigations validate Host against an allowlist before serving. The takeaway for senior work: Host is not routing trivia — it is part of the resource identifier, participates in virtual-host routing, certificate selection, and origin identity, and must be validated as carefully as the path.

## Q30: What are HTTP Range requests, the 206 Partial Content status, and the Range header syntax?

**A:** A Range request is a GET with a `Range: bytes=...` header asking the server to send only a subset of a resource's bytes rather than the whole entity. The canonical syntax is `bytes=0-499` (first 500 bytes), `bytes=500-999`, `bytes=-100` (last 100 bytes), `bytes=0-99,200-299` (multiple ranges) — plus the `If-Range` header that makes a range request conditional on an ETag/Last-Modified. When the server agrees, it responds 206 Partial Content with `Content-Range: bytes 0-499/1234` and exactly the requested bytes; for multi-range requests it may respond with a `multipart/byteranges` body.

206 is still a success response and carries representation metadata of the whole resource (Content-Length refers to the PARTIAL body length; Content-Range tells the total). If the server cannot or will not do ranges, it must return a full 200 with the whole body; if the requested range is unsatisfiable (start beyond EOF), it SHOULD return 416 Range Not Satisfiable with `Content-Range: bytes */<total>`.

Range requests are the backbone of resumable downloads, video streaming (browsers fetch sequential ranges), and byte-level deduplication in storage and CDN backends. Cache semantics interlock: a shared cache may coalesce range misses into full-fetch caching and serve ranges from a cached complete representation — but only when the representation is stable, so freshness metadata (ETag/Last-Modified) and Vary discipline still rule. Interview depth here lies in knowing 206's exact framing semantics and the HTTP-spec interaction with caching.

## Q31: What are conditional requests, and how do If-Modified-Since and ETag/If-None-Match work?

**A:** Conditional requests attach a precondition to an otherwise normal request, telling the origin "only act if this state still holds." The two dominant conditions: `If-Modified-Since: <date>` — a GET/HEAD carries the date of the cached copy, and the server answers 304 Not Modified (no body) if unchanged, or 200 with new body if changed; and `If-None-Match: "etag"` — the client sends the entity tag of its cached copy, and the server compares against the current resource's ETag, returning 304 on match and 200 on mismatch. If-None-Match takes precedence over If-Modified-Since when both appear.

Other conditional headers address concurrency, not caching: `If-Match: "etag"` performs the write only if the current representation still matches (the classic optimistic concurrency guard), while `If-Unmodified-Since` is the date-flavored equivalent. `If-Range` makes a Range request conditional on freshness so a resumed download does not splice bytes from a changed resource. `If-None-Match: *` (no tag value) fires when "the resource does not yet exist" — create-if-absent semantics.

The cache-coherence logic: ETags are stronger than dates (dates are 1-second granularity and clock-skewed across hosts), so modern guidance is to emit strong ETags and use If-None-Match. For distributed systems, ETag equality is only meaningful if the origin issues ETags consistently — CDNs maintain per-origin ETag mapping to keep the "reduce body with 304" behavior working across cache tiers, and breaking that mapping silently blasts bandwidth.

## Q32: What is cache freshness, and how do Cache-Control directives like max-age, no-cache, and no-store differ?

**A:** Cache freshness is the period during which a cached representation is allowed to serve WITHOUT contacting the origin, governed by `Cache-Control: max-age=3600` (the representation is fresh for 3600 seconds) or the old Expires header. When a cached copy is stale, a cache must revalidate against the origin — by sending a conditional request and getting 304 (still fresh, reuse) or 200 (new data, replace). This is the entire machinery of HTTP caching.

The three directives sit at different points on that spectrum. `no-cache` does NOT mean "do not cache" — it means "you MUST revalidate with the origin before every reuse." `no-store` means "do not store ANY copy at all." `max-age` gives a hard fresh window. `public` vs `private` split cacheability: `private` allows only the browser's cache (not shared caches), `public` allows shared caching.

The senior correctness points: freshness is compared in seconds using Date/Age headers; a response can mix directives; and `Cache-Control: no-store` for sensitive, per-user data is usually the right call because shared caching of user-specific content is a data-leak risk. Understanding "fresh vs stale vs revalidated" states is the heart of every caching debug.

## Q33: What is the difference between PUT and POST, and why does it matter for API design?

**A:** PUT is "store this representation at this URI, making it the resource's new state" — the client fully specifies the new value, the URI is the resource's own, and PUT is idempotent: replaying the same PUT N times converges to the same state. POST is "please process this representation" — act on the resource, where the action may create something new, start a side effect, or execute an arbitrary procedure; POST is neither safe nor idempotent by definition. The distinction is "set the value of X to this" (PUT) vs "do something with this payload" (POST).

The design consequences: a create-new-resource operation is POST to a collection (`POST /users`); a replace-the-whole-resource operation is PUT (`PUT /users/42` overwrites user 42); DELETE removes; PATCH is a partial update and is NOT guaranteed idempotent. Whether an API is "good REST" often reduces to whether PUT is being used for real, idempotent replacement and POST for everything else.

Three senior traps. (1) Idempotency is a RETRY contract: payment APIs expose POST + an Idempotency-Key header precisely because they cannot be PUT semantics. (2) Concurrency: two clients PUT disjoint fields of the same resource can clobber each other — the standard answer is If-Match/ETag on the PUT. (3) Partial updates expressed as PUT (sending partial JSON over a "full-replace" verb) silently break idempotent semantics. Choosing the verb by semantics rather than convenience is the most common senior-level API distinction interviewers probe.

## Q34: Why is DELETE idempotent while POST is not, and what does DELETE really "remove"?

**A:** DELETE's idempotency rests on "the target resource state converges to absent": deleting an already-deleted resource changes nothing (the state after the second delete equals the first — both "does not exist"), so replaying DELETE is harmless. The responses may differ (first returns 200/204, subsequent 404 or 204) — but idempotency is about SERVER STATE, not identical responses. POST, by contrast, has no such convergence: a second POST is a new action, a new record, a second charge — state does not naturally converge, so POST is not idempotent.

The semantic subtlety: DELETE removes the mapping from URI to representation at the origin; whether the underlying bytes are hard-deleted, soft-deleted, or scheduled for removal is an implementation detail invisible to the protocol. RESTful practice models "removal" as the client's chosen action and treats the resource's absence (404 after delete) as the natural post-condition.

For interviews, the sharp edge is that DELETE's idempotency is what makes automatic retry safe — a load balancer can retry a timed-out DELETE without creating a duplicate — while POST's non-idempotency is precisely why "double submit" bugs and duplicate charges happen. When a team hits "my delete endpoint is not idempotent," the cause is usually not the verb but side effects (delete triggering an email, decrementing a counter) — side effects must be governed by the same idempotency law. Keeping DELETE "no side effect beyond absence" is the senior contract.

## Q35: What is chunked transfer encoding, and when is it used?

**A:** Chunked transfer encoding is HTTP/1.1's framing mechanism for messages whose total body length is not known when headers are sent. Instead of Content-Length, the sender emits `Transfer-Encoding: chunked` and writes the body as a sequence of size-prefixed chunks: each chunk begins with a hexadecimal size, then that many bytes, then a zero-size chunk and optional trailers. It is what enables streaming: a server can start sending a response before it knows how many bytes it will produce.

Two critical rules. Chunked is hop-by-hop: an intermediary that receives a chunked message and forwards it must either preserve the chunked framing exactly or convert it to Content-Length after buffering — if it strips Transfer-Encoding without adding a definitive length, downstream parsing breaks (a smuggler's classic alley). And Transfer-Encoding and Content-Length MUST NOT both be present in the modern spec — a message carrying both is treated as a smuggling-capable ambiguity and typically rejected. Trailers (trailer headers declared with `Trailer:`) ride after the final chunk, exactly how one sends metadata unknown mid-stream.

Chunked drives important performance behaviors: servers use it to flush headers early (SSE, streaming responses), and proxies that cannot buffer eagerly forward chunks. HTTP/2 and HTTP/3 do not use literal "chunked" — their DATA-frame framing inherently supports streaming and trailers — but the semantic, "stream a body of unknown length," survives as basic framing. A senior answer links chunked to the next hop: how a proxy reconciles chunked upstream with Content-Length downstream is precisely the boundary where smuggling bugs live.

## Q36: What are the 1xx informational status codes, and what does 100 Continue accomplish?

**A:** The 1xx class reports that the server is still processing; it has no body and the "real" response follows. The meaningful members are 100 Continue, 102 Processing (legacy), and 103 Early Hints. 100 Continue is the answer to a client's `Expect: 100-continue` header: the client says "I have a big body; tell me the headers are OK and I'll send the body" — the server replies 100 Continue to authorize the upload, or a final status (like 413 or 401) to skip it entirely. Its purpose is to avoid wasting bandwidth sending a body that will be rejected.

The interplay has nuances: a client that sends Expect: 100-continue waits for the interim response; if nothing arrives it proceeds with the body anyway. Some intermediaries mishandle 100 Continue and forward the body anyway — the classic "100-continue smuggling" bug range. 103 Early Hints is distinct — it lets a server send interim `Link: rel=preload` headers BEFORE the final response so the client can begin fetching critical subresources while the main body is still being generated.

The senior difference: 100 is a permission/flow gate for the upload body, while 103 is a head-start optimization for the download side. Both are "interim" messages that the final response replaces, and clients must handle "interim headers + final headers" without double-processing.

## Q37: What is Content-Length, how is it framed, and what breaks when it is wrong?

**A:** Content-Length states, in octets, the exact size of the message body. It enables framing: the receiver reads exactly Content-Length bytes after the header block, and anything after that is the NEXT message. It also enables progress bars, download resumption (paired with Range), and defensive size limits. If Content-Length is smaller than the real body, trailing bytes become a new request; if larger, the receiver waits forever for bytes that never come — a request smuggling or hanging-request DoS. This is why the header's integrity is security-critical.

The interplay partners are Transfer-Encoding: when both are present, a server MUST treat the message as ambiguous and refuse (RFC 9112 forbids both) because a smuggler can hide a second request in the gap. Because Content-Length refers to the BYTES ON THE WIRE, it counts the encoded (compressed) body, not the decoded representation; after decompression the representation is a different size. It also becomes the wrong tool when the body is streamed of unknown length — that is Transfer-Encoding: chunked's job.

The senior-grade point is normative: Content-Length is a framing claim the receiver trusts to parse subsequent messages, so intermediaries must validate or recalculate it whenever they transform the body. A senior engineer debugging a "request hangs" or "requests garbled" bug reaches for Content-Length reconciliation immediately — it is the single most common source of interop breakage in HTTP/1.1, and one of the reasons HTTP/2 moved body framing into frames.

## Q38: What is hop-by-hop header handling, and what does the Connection header actually list?

**A:** The Connection header has two roles. First, it expresses a per-hop directive like `Connection: close` or `keep-alive`. Second, it NAMES the hop-by-hop headers that must be stripped before forwarding: `Connection: X-Foo` says "treat X-Foo as hop-by-hop; do not forward it." The fixed set of inherently hop-by-hop headers — Connection, Keep-Alive, TE, Upgrade, Transfer-Encoding, Proxy-Authorization, and Proxy-Authenticate — is never forwarded by a conforming proxy.

The security surface is the gap between intermediaries: an attacker crafts a request whose Connection header names a sensitive header the front proxy strips, but a back proxy re-forwards or expects — altering authorization, cache behavior, or smuggling semantics. This "hop-by-hop header smuggling" is why uniform Connection handling across every proxy is a non-negotiable security baseline.

The modern complication: HTTP/2 and HTTP/3 REMOVED the Connection header entirely. Neither carries Connection, Keep-Alive, Transfer-Encoding, Upgrade, or Proxy-Connection; semantics moved into connection-level frames and endpoint signaling. But any gateway translating HTTP/2 to HTTP/1.1 must reconstruct proper Connection behavior — and mismatched stripping at that seam is where today's smuggling vulnerabilities surface.

## Q39: What is the OPTIONS method, and how does the Allow header express a resource's capabilities?

**A:** OPTIONS asks a target resource (or the whole server, when addressed as `OPTIONS *`) to communicate the communication options that the resource supports. Its canonical answer is the `Allow` header listing the methods the resource accepts — `Allow: GET, HEAD, OPTIONS` — plus headers like Accept-Ranges. OPTIONS is a "discover capabilities" verb: safe, no side effects, and the basis of both CORS preflight (browsers send OPTIONS with `Access-Control-Request-Method` and get back `Access-Control-Allow-*` headers) and REST discoverability.

Its two famous consumers: CORS preflight, where a browser issuing a non-simple cross-origin request first sends OPTIONS to ask "is this OK?", and REST's hypermedia model where OPTIONS responses tell generic clients which verbs are available next. The same response shape drives generic tooling (curl's `-X OPTIONS`) and API explorers.

The senior caveats: OPTIONS is NOT a replacement for the Allow header appearing in 405 responses (a server that does not implement OPTIONS may still advertise Allow in 405), and intermediaries must forward OPTIONS opaquely. The newest spec wave folds some capability discovery into `Accept-Patch`/`Accept-Post` so clients learn update semantics before POSTing.

## Q40: What is the TRACE method, and why is it a security risk?

**A:** TRACE echo-receives the request as the server sees it, reflecting back the exact request line, headers, and body. Its designed purpose was diagnostics and debugging. Its fatal flaw is that TRACE reflects sensitive data back verbatim — including cookies, Authorization credentials, and custom headers — and a cross-site script can use an XSS vector to issue a TRACE through the browser and READ the echoed credentials back (the Cross-Site Tracing attack class). Because responses are readable, TRACE turns reflected auth material into exfiltratable data.

For that reason, production posture is to disable TRACE (typically with 405 or similar), and most web servers disable it by default or in security baselines. A server that must keep it should restrict it to authenticated administrative clients on private networks.

The senior detail: TRACE's danger is not the method itself but browsers translating a script's network trigger into the browser's own cookie-carrying TRACE — the same reason custom headers can be abused. "Disable TRACE" is the candid answer, and the interviewer is checking whether you know both the debugging rationale AND the cross-site-tracing exfiltration mechanism.

## Q41: What is the CONNECT method, and how do proxies use it to tunnel encrypted sessions?

**A:** CONNECT asks an intermediary proxy to establish a transparent end-to-end tunnel to a target host:port and to relay raw bytes both ways without inspecting them. In practice it is how an HTTP proxy carries HTTPS: the client sends `CONNECT example.com:443 HTTP/1.1`; if the proxy agrees, it replies `200 Connection Established`, and the TLS handshake and all subsequent encrypted traffic flow through the tunnel untouched. CONNECT is not about fetching a resource — it is a transport-facilitation method.

Why it exists: an HTTP proxy cannot inspect or relay an HTTPS session as HTTP because TLS encrypts the whole session; tunneling lets a proxy support HTTPS clients without decrypting (or only decrypting at a designated MITM proxy). Extensions include WebSocket over HTTP CONNECT and SOCKS-like tunneling.

The security boundary: a misconfigured open CONNECT proxy lets anyone tunnel any protocol (including SSH and other proxies) through it, turning it into an open relay/egress — that is why CONNECT targets are usually allowlisted by port (often only 443). Senior depth = recognizing CONNECT as the layering seam where HTTP's proxy model and TLS's end-to-end confidentiality meet, and why proxied HTTPS deployments choose a MITM CA rather than block tunneling outright.

## Q42: What are HTTP trailers, and how are they different from regular headers?

**A:** A trailer is metadata carried at the END of a message body rather than at the start. In HTTP/1.1, a sender declares intent with `Trailer: X-Foo, X-Bar`, uses `Transfer-Encoding: chunked`, and after the final zero-length chunk appends the trailer fields themselves. Trailers are for values NOT KNOWN when headers are written: a checksum computed after streaming the whole body, a final byte count, or a processing status like a gRPC-style `grpc-status`. They ride the message as its tail; the body is unchanged.

The rules distinguish carefully: a receiver that does not want trailers may discard them; hop-by-hop semantics mean a proxy that buffers a chunked message may drop or synthesize trailer data; and the `Trailer` header advertises each one. Authentication and authorization headers MUST NOT go in trailers; neither may any header that controls caching — trailers are for message-tail metadata only.

Under HTTP/2 and HTTP/3, trailers survive as trailing HEADERS blocks on the stream (a DATA frame followed by a HEADERS frame), which is how streaming uploads report a final digest or gRPC streams report final status. The senior answer connects the WHY: trailers enable "compute-then-send-then-sign" patterns and avoid double-pass buffering — a resource that could not be hashed before streaming can still authenticate its tail.

## Q43: What does the Server header reveal, and why is header-hygiene a security practice?

**A:** The Server header identifies the software behind the response — `Server: nginx`, `Server: Apache/2.4.57` — often with version detail and module listings. The security objection is information disclosure: a version-precise Server header is an automated exposé of vulnerable software — an attacker can scan for known CVEs instantly without fingerprinting by behavior. That is why the header is frequently stripped, minimized (`Server: nginx` without the version), or replaced with a value that has no version semantics, and why the same discipline applies to X-Powered-By and framework banners.

The pragmatic stance: the Server header is genuinely useful for diagnostics, which is why the RFC says its presence is informational, not security-validated. The resolution most teams adopt: minimize or remove it on public edges, log the true version internally, and rely on out-of-band inventory rather than wire banners. The nuance is that removing it entirely can trip old clients or proxies that sniff fixes based on Server; but the exposure risk dominates.

The interview probe is whether "hiding the Server header" is theater or mitigation. The senior answer: banner minimization raises the cost of automated CVE targeting (it eliminates the fastest scan path) but is NOT a security boundary — fingerprints by response shape, TLS feature set, error output, and behavior remain; defense belongs to patching and WAF policy, with banner hygiene as a cheap layer.

## Q44: Why do servers cap header sizes, and what does the 431 status code communicate?

**A:** Header caps exist because header-size is an untrusted, attacker-influenced input: forged giant header sets (thousands of cookies, abusively repeated tokens) can exhaust memory or CPU. Real servers enforce limits — Apache's RequestLineLimit, nginx's large_client_header_buffers, proxy stacks' per-header and total-header limits — and configuring them is a first-line DoS and smuggling hardening step. The limits typically couple a per-header cap (e.g., 8 KB) with a total cap (~32 KB) and a header-name cap.

When a request exceeds the limit, the correct status is 431 Request Header Fields Too Large (RFC 6585), signaling "reduce or shrink your headers and try again." Sending 431 is distinctly better than a generic 400 because it tells the client it is a SIZING problem — useful for automated clients that can shrink their cookie jars. The 414 URI Too Long and 413 Content Too Large are the same family guarding the request line and body respectively.

For senior work, the interop insight is that header limits and TLS-level limits vary per hop, so a valid large-request to a front CDN may be dropped by the backend with 431. The common prod bug is "browser works, API client fails" reducing to cookie count (each domain's cookies accumulate per host). Setting generous-but-bounded caps with clear 431 semantics is the correct balance.

## Q45: How do redirects interact with HTTP methods, and what do 301 vs 307 vs 308 change?

**A:** The redirect trio encodes how the method should be replayed on the Location. Historically, 301 and 302 BOTH said "go to Location," and browsers defaulted to rewriting POST into GET — a behavior that leaks bodies. 303 See Other was invented to make this rewriting EXPLICIT. 307 and 308 were added to say "repeat the SAME method (and body) at the new URI." So: 301/302/303 rewrite to GET (with 303 being the explicit POST→GET pattern), 307/308 preserve both method and entity.

The consequences are sharp: a 301/302 redirect of a POST turns it into a GET — if the server intended the POST to be replayed (payment submission), the semantics break; 303 is "your POST is done, GET the confirmation page"; 307/308 are "the SAME request must be re-sent." Caching also differs: 301/308 are cacheable-as-permanent; 302/307 are ephemeral.

The senior practical guidance: (1) Prefer 308/301 for permanent resource moves and 307/303 for ephemeral; (2) never use 301/302 for API POST contracts if you need the request replayed; (3) proxies that follow redirects must mirror the browser's rewrite rules; (4) in HTTP/2/3 the mechanism is identical — the METHOD re-encoding decision lives entirely in the status code semantics.

## Q46: What is the Age header, and how does HTTP calculate a cached response's freshness?

**A:** Age reports, in seconds, how long a response has been sitting in a shared cache — the time since the origin generated it that the cached copy has accumulated. `Age: 300` means the payload is five minutes old as measured by cache residency. Age is emitted by shared caches/CDNs, and consumer caching logic uses Age to decide whether a cached copy is still within its freshness window (`max-age` / Expires vs Age).

The freshness math: a response is fresh if age < freshness_lifetime, where freshness_lifetime comes from `max-age` (if present) else Expires calculation, else from heuristics. When stale, a cache revalidates (If-None-Match/If-Modified-Since) or serves stale if `stale-while-revalidate`/`stale-if-error` permits. Clocks matter: the Age and Date computation is only as accurate as the cache's clock versus the origin's, which is why `s-maxage` may be set per cache tier and why explicit max-age beats Expires.

The senior reading: Age gives visibility into freshness ("how fresh is this CDN copy?") and the mechanism that makes shared-cache behavior debuggable. Age being absent on origin responses but present on CDN hits distinguishes origin vs cache-caused staleness; and when debugging stale-content complaints, Age + Date + max-age tells the whole story of which tier held the copy.

## Q47: What is the difference between 409 Conflict and 422 Unprocessable Content?

**A:** 409 Conflict means the request is syntactically fine but CONFLICTS with the current state: creating something that already exists, an optimistic-concurrency mismatch (If-Match header does not match), or a rename that collides with an existing sibling. It invites the client to fetch the current state and decide. 422 Unprocessable Content means the server understood the syntax but the request's SEMANTIC content violates the rules: the JSON parsed, but the email is malformed, the date range is inverted, the field is out of domain. 422 is the "business-rule validation failed" code.

The distinguishing test: 409 is a STATE conflict (the request would be valid if the resource were in a different state), while 422 is a VALUE problem (the request is invalid regardless of state). Classic pairs: "username taken" → 409 (state-dependent conflict where the resource exists), "username contains illegal character" → 422 (invalid in any state).

The modern consensus: 400 for unparseable syntax, 422 for parseable-but-invalid semantics, 409 for state conflicts, and 412/428-style for If-Match failures. Getting this taxonomy right is what makes API error handling debuggable by automation.

## Q48: What does 429 Too Many Requests mean, and how do Retry-After and rate-limit headers interact?

**A:** 429 Too Many Requests declares that the client has exceeded a rate limit, and the response SHOULD carry `Retry-After` giving a delay-seconds after which the client may try again. It signals both "slow down" and "when may I retry," so compliant clients honor it instead of retrying horizontally. In practice servers also emit rate-limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, or the newer standard RateLimit-*), and 429 is distinct from 503 (server overload) — distinguishing them lets a load balancer decide whether to shed the client or the backend.

The interplay: Retry-After applies to both 429 and 503; rate limits must be behavior-independent — an attacker can rotate IPs, so real systems rate-limit on tokens/accounts/API keys; and clients that double as crawlers must honor 429 + Retry-After or they get banned.

Senior nuance: rate limiting must be token/account-based not IP-based (attackers rotate IPs), and 429 MUST be paired with Retry-After to avoid thundering-herd retries. The polite contract — back off, retry when asked — is what makes 429 usable for distributed scraping at scale.

## Q49: What is content encoding versus transfer encoding, and how does Accept-Encoding/gzip fit in?

**A:** Content encoding (representation encoding) transforms the RESOURCE bytes semantically — gzip, br (Brotli) — and is negotiated via `Accept-Encoding` (request) and announced with `Content-Encoding` (response); it is end-to-end: the client decompresses to obtain the raw representation. Transfer encoding transforms the MESSAGE on THIS HOP — `Transfer-Encoding: chunked` sizes the stream — and is hop-by-hop: each intermediary may re-frame; it never survives to the next hop.

The workflow: a client sends `Accept-Encoding: gzip, br`, the server selects br, compresses the body, writes `Content-Encoding: br`, and the client decompresses before interpreting. Compression on the wire cuts bytes 60-90% for text. The traps: Content-Length refers to the ENCODED body length; intermediaries that decompress must rewrite Content-Length and Vary; caches may store the same resource encoded differently (Vary: Accept-Encoding splits variants); and a mismatch where the response says gzip but bytes are not gzip is a protocol error.

The senior additions: Brotli wins over gzip at equal CPU for text; `no-transform` forbids intermediaries from transcoding; and the Accept-Encoding list with q-values gives the client fine control. The mental model: content-encoding = what data you get; transfer-encoding = how the message arrives.

## Q50: What is the OPTIONS/CORS preflight flow, and how do Access-Control-* headers govern it?

**A:** CORS is the browser-enforced permission model that lets a server choose which other origins may read its responses. When a page at origin A fetches from origin B with credentials or a non-simple request, the browser FIRST sends a preflight OPTIONS with `Origin: A`, `Access-Control-Request-Method: PUT`, and `Access-Control-Request-Headers: X-Api-Key`. The server responds 204 with `Access-Control-Allow-Origin: A`, `Access-Control-Allow-Methods: PUT, PATCH`, `Access-Control-Allow-Headers: X-Api-Key`, `Access-Control-Max-Age: 86400`, and optionally `Access-Control-Allow-Credentials: true`. If allowed, the browser sends the real request; if not, the fetch fails and no response bytes reach the page.

Simple requests skip preflight entirely: GET/HEAD/POST with only CORS-safe-listed headers and simple content types send Origin directly; the response must still carry Allow-Origin matching (or `*` for no-credentials requests). Allow-Credentials: true + Allow-Origin: <specific> — never `*` with credentials — is THE classic pairing; `*` with credentials is forbidden by spec. Vary: Origin must accompany dynamically-computed Allow-Origin so CDN caches do not serve one origin's variant to another.

The senior traps: (1) Preflight is browser-enforced, not a server firewall — API servers must still enforce auth/CSRF; (2) a custom Authorization header triggers preflight for every credentialed API call — which is why many teams prefer no-custom-header GETs; (3) `Access-Control-Max-Age` caches preflight results; (4) credentials require Allow-Credentials: true on BOTH the preflight and actual response. Mastering the preflight matrix is a recurring senior API interview question.

## Q51: What problems was HTTP/2 designed to solve, and what architecture did it choose?

**A:** HTTP/2 answers two linked failures of HTTP/1.1: head-of-line blocking and connection proliferation. HTTP/1.1 could process one response at a time per connection, so browsers opened 6+ TCP connections per origin, each bearing full TCP/TLS setup cost. HTTP/2 collapsed the model into ONE connection per origin carrying 100+ concurrent streams. It also removed the text-based framing that made parsing ambiguous and replaced it with precise binary framing — a 9-byte frame header (length, type, flags, stream id) heading frames of types DATA, HEADERS, PRIORITY, RST_STREAM, SETTINGS, PUSH_PROMISE, PING, GOAWAY, WINDOW_UPDATE, and CONTINUATION.

Each logical request/response occupies a stream (identified by an odd/even 31-bit ID), multiplexed onto the connection; the receiver reassembles each stream's HEADERS+DATA into the HTTP message. Because streams are independent, HEAD-of-line blocking at the HTTP layer disappears — that is the multiplexing win. Streams have their own states (idle, open, half-closed, closed), their own flow control, and their own RST_STREAM cancellation, so canceling a slow request costs nothing on sibling streams.

The loss-caused head-of-line remains because streams share one TCP byte stream: a lost packet stalls all streams until retransmission. That second HOL is what HTTP/3 later solved. But HTTP/2's contribution — a single connection, reliable parsing, HPACK header compression, and real concurrency — made it the dominant protocol of the 2020s web.

## Q52: How does HTTP/2 implement multiplexing, and how does that differ from HTTP/1.1 pipelining?

**A:** HTTP/2 multiplexing interleaves independent streams of frames over ONE TCP connection: the sender walks a scheduler and emits frames from many streams in any order, and the receiver treats frames with the same stream ID as one logical message. Streams have independent flow control and explicit END-of-message semantics, so a slow large response (stream 1) does not block tiny responses (streams 3, 5, 7). This is the fix pipelines lacked — pipelining required FIFO responses, while HTTP/2 requires NO order guarantee between streams.

Pipelines were also opaque: no way to cancel an individual response, no per-request flow control, and no hinting of urgency. HTTP/2 adds RST_STREAM (cancel one stream), per-stream WINDOW_UPDATE flow control, and an explicit PRIORITY mechanism. And because it is ONE connection, the OS-level cost of N sockets collapses.

The comparison trap: multiplexing does NOT remove TCP-level HOL (lost segments stall ALL streams on that connection), and it does NOT change HTTP semantics — methods/status/headers have identical meaning. What changed is the CONCURRENCY MODEL: one connection, many logical channels, explicit cancel, and no global ordering — the pattern that makes "many small fetches" fast. The senior answer contrasts "best-effort ordered pipeline" (1.1) vs "concurrent unordered multiplex" (H2), then notes the one remaining transport HOL that H3 solves.

## Q53: What is HPACK, and how does it compress HTTP/2 headers?

**A:** HPACK (RFC 7541) is HTTP/2's header compression scheme. Headers were transmitted as verbose ASCII in HTTP/1.1; HPACK encodes a HEADERS frame's field set as a sequence of compressed, potentially-indexed entries, using three techniques: a static table of well-known header names/values, a dynamic table that grows with recent fields, and Huffman encoding of literal values. A header like `:method: GET` may encode as a single byte referencing the static table.

The static table pre-populates ~61 entries (GET/POST, 200, 204, text/html, etc.); the dynamic table is maintained sliding-window style per connection side, so repeated headers (cookies, user-agent) become literal-with-index references after their first occurrence. Literal-without-indexing covers one-offs; never-index protects sensitive values (like Authorization) so they are not added to the shared dynamic table — a CRIME-hardening rule. Huffman coding shaves value bytes on top of the table savings.

The interop rules matter: the dynamic table is CONNECTION-SCOPED (shared across all streams), so an HPACK state desync breaks ALL streams — which is why a header-resync is catastrophic. And because table references can encode secret data, never-index marking prevents sensitive headers from entering the dynamic table. This compression-below-the-streams design is what QPACK rebuilds for HTTP/3's lossy multi-stream transport.

## Q54: What are the HPACK static and dynamic tables, and what does an indexed entry buy you?

**A:** The static table is a fixed list of 61 common name-value pairs (RFC 7541 Appendix A) — `:method: GET`, `:status: 200`, `content-type: text/html`, etc. It cannot be modified; its entries are stable forever. Indexing in HPACK means "the entire field is referenced by an integer, not re-sent." A static indexed field encodes in 1-2 bytes. The dynamic table is learned: it stores the most recent literal-with-incremental-indexing fields, sliding oldest out when the configured size is exceeded.

The win is repetition amortization: the second occurrence of a large header becomes a small index reference. HTTP/2 connections serving hundreds of requests reuse the same UAs and Accepts constantly — typical page loads compress header overhead by 10-20x after warmup. The dynamic table's freshness is the risk: it must stay synchronized across both peers; any drift (a proxy that re-indexes without acknowledgment) corrupts everything.

The senior detail: never-index values. Literal-without-indexing emits the field raw and MUST NOT add it to the dynamic table — mandated for fields like `Cookie` and `Authorization`. So the scheme is "compress the low-entropy repetition, keep the high-entropy secrets re-sent raw." QPACK inherits static+dynamic+Huffman but adds Section Acknowledgment and a dedicated encoder stream because loss breaks the H2 model where table state is shared in-order on one transport.

## Q55: What is HTTP/2's stream prioritization model, and what were its practical problems?

**A:** HTTP/2 prioritization uses PRIORITY frames expressing a dependency tree with weights. Each stream points at a parent stream (default the root), with a weight; a scheduler allocates bandwidth so children of a parent split proportionally. Clients compute this tree from page parse order — the CSS depends on HTML, images less so — and servers schedule frames accordingly.

Its practical failures: (1) The tree is client-side policy with no mandated server interpretation; many servers ignored PRIORITY entirely. (2) The model is fragile under reordering — dependency changes cascade, and implementations diverge. (3) Bandwidth starvation is real: a heavy, deprioritized stream can be delayed indefinitely. (4) Most clients stopped sending PRIORITY frames correctly; Chrome moved to hints only.

The IETF answer was RFC 9218, Extensible Priorities: drop the tree, use urgency (0-7) plus an incremental flag, in a plain header; the server interprets it directly. The transport-level scheduler (not the protocol) controls interleaving. Interview candidates should know: H2 had a tree, it was inconsistently implemented and often ignored, HTTP/3 replaced it with urgency+incremental.

## Q56: How does flow control work in HTTP/2, and what are connection-level vs stream-level windows?

**A:** HTTP/2 flow control is per-stream AND per-connection. The connection is initialized with a window (default 65535 bytes) advertised via WINDOW_UPDATE frames; each send-side bottlebooks apply: DATA frames on a stream count against the stream's window AND the connection's window, and the receiver refills either by sending WINDOW_UPDATE when it has consumed buffers. The connection-level window bounds total DATA in flight; stream-level windows bound a single logical channel, so a slow stream does not eat the whole connection's budget.

Windows are INITIAL-advertised and grown; too-small windows cause stalls, too-large risk memory overload on the receiver. Because flow control is the layer arbitrating "how much can I have on this connection and this stream," it interacts with priorities: the scheduler allocates the window among streams; a stream saturated by its own window does not consume others'.

The practical trouble: (1) Tiny default windows fragment a fast pipe into constant WINDOW_UPDATE chatter; stacks auto-tune initial windows (often 1-10 MB). (2) A stream-level window stall is a per-stream HOL — cancelable with RST_STREAM. (3) Flow control, message sizes, and TLS records must be aligned or you waste window with padding. For senior work, connecting flow control to "the receiver bounds burstiness per stream and per connection" is the correct structural answer.

## Q57: What is HTTP/2 server push, and why was it later deprecated by browsers?

**A:** Server push lets a server anticipate that a client fetching a resource (e.g., HTML) will also need subresources (CSS, JS, images) and PUSH them proactively. The mechanism: the server emits a PUSH_PROMISE frame naming a future resource, the client MAY accept it or reject with RST_STREAM. In theory push eliminates one round trip of request/response for each subresource.

The practical collapse: (1) Prediction quality was poor — servers pushed what the page MIGHT need, and clients frequently had it cached, wasting bandwidth. (2) Push consumed flow-control windows regardless of client need. (3) Push did not integrate well with HTTP caching semantics — pushed responses were not cache-vetted. (4) Push could serve as a tracking channel.

Browsers disabled it: Chrome rejected pushes, then all browsers followed. RFC 9113 standardizes it but effective support is off-by-default; HTTP/3 redefined it as severely constrained. The replacement that survived is `Link: <...>; rel=preload` + `103 Early Hints`: the server tells the client WHICH resources matter, and the CLIENT fetches them under its own cache discipline. The lesson: proactive delivery is only a win when the client needs the bytes — predicting, not pushing, is the durable design.

## Q58: What is the SETTINGS mechanism in HTTP/2, and how does negotiation really happen?

**A:** SETTINGS is an HTTP/2 connection-level frame establishing PARAMETERS the peer should honor. It is sent once per direction at connection start (mandatory-immediate per RFC) and can be re-opened later. Parameters include SETTINGS_MAX_CONCURRENT_STREAMS, SETTINGS_MAX_FRAME_SIZE, SETTINGS_INITIAL_WINDOW_SIZE, SETTINGS_MAX_HEADER_LIST_SIZE, SETTINGS_ENABLE_PUSH. The receiving endpoint must ACKNOWLEDGE each SETTINGS with a SETTINGS+ACK; until acknowledged, the values are NOT effective.

So "negotiation" is unilateral-plus-ack: each side DECLARES its own parameters (e.g., `MAX_CONCURRENT_STREAMS: 100` tells the peer "you may open up to 100 streams on me"), the peer confirms with ACK, and the effective value is what the RECEIVER declared. There is no symmetric handshake — each direction is governed by the other's declared limits, a one-way capability exchange.

The senior corners: (1) default values matter — initial window 65535 and max frame 16384 are the baseline the peer relies on until your SETTINGS arrives; (2) MAX_HEADER_LIST_SIZE is a hard-upper control for DoS; (3) MAX_CONCURRENT_STREAMS = 0 is a graceful "stop Opening streams" signal (the basis of connection draining); (4) forgetting to ACK settings silently freezes window/stream upgrades.

## Q59: What are the HTTP/2 frame types, and what is each one's role?

**A:** HTTP/2 frames are the atomic units of transport. The core set: DATA carries body bytes (reliable, flow-controlled); HEADERS opens a stream carrying pseudo-headers + fields with end_stream/end_headers flags; RST_STREAM cancels a stream with an error code; SETTINGS configures connection parameters (acked); PING is a keep-alive/RTT probe (must be echoed); GOAWAY tells the peer "no new streams"; WINDOW_UPDATE increases flow windows; PRIORITY expresses scheduling interest; PUSH_PROMISE announces a push; CONTINUATION carries overflow of a large HEADERS block.

The framing invariants make them reliable: a HEADERS block is a sequence of HEADERS + CONTINUATION frames; DATA is flow-controlled; RST_STREAM and GOAWAY carry error codes; the receiver processes each stream independently, so RST_STREAM on stream 5 leaves streams 3 and 7 running. Frame headers (length, type, flags, stream id) are fixed so lengths are exact and cannot be mis-framed — this byte-exactness is why smuggling-by-length-charge died at HTTP/2.

The senior classification: DATA and HEADERS are the application content; *_UPDATE/GOAWAY/SETTINGS/PING are connection instrumentation; RST_STREAM is the cancellation terminal; PUSH_PROMISE is HTTP/2's only "server speaks first" mechanism. Knowing which frame is flow-controlled (DATA only), which is connection-vs-stream-scoped, and how end_stream on HEADERS means an empty-body GET-like stream distinguishes a senior HTTP/2 engineer.

## Q60: What is the GOAWAY frame in HTTP/2, and how does graceful shutdown work?

**A:** GOAWAY is HTTP/2's "no more NEW streams" signal, sent when an endpoint wants to wind a connection down gracefully. It carries the last-stream-id (the highest stream ID the sender commits to processing) and an error code + debug data. After GOAWAY, the sender still processes streams with lower IDs but refuses new ones; the receiver stops opening new streams and, when out-of-flight work settles, sends its own GOAWAY and closes. The two-GOAWAY dance is how a graceful drain completes.

The graceful life: a server under deployment drain sends GOAWAY with its current highest stream, waits for remaining streams to complete, then closes TCP. Browsers and connection pools use GOAWAY to dismantle connections cleanly — no dropped requests — and to rebalance streams onto a fresh connection.

The pitfalls: an endpoint ignoring GOAWAY violates the protocol; last-stream-id semantics are muddled when both sides race their GOAWAYs; and error codes distinguish graceful close (NO_ERROR) from upgrades. For load balancing, GOAWAY is the mechanism that lets a backend "walk away" without killing in-flight requests — the answer to "how do you redeploy HTTP/2 servers without dropping users?"

## Q61: How does HTTP/2 interact with TLS, and what is ALPN for h2 vs h2c?

**A:** HTTP/2 on the public internet REQUIRES TLS, and must negotiate HTTP/2 during the TLS handshake via ALPN: the client's ClientHello includes `h2`, the server picks `h2` and sets it in ServerHello's ALPN extension. Requiring TLS means HTTP/2 draws on transport security (confidentiality, integrity, authenticity) that the protocol itself does not define. The exception is `h2c` (cleartext HTTP/2), designed for internal/LB-to-backend hops: a client uses either HTTP/1.1 `Upgrade: h2c` or sends the h2 preface directly (prior-knowledge h2c). Real browsers never use h2c.

The ALPN dance is how a client with one TLS connection lets the server choose among h2, HTTP/1.1, and (today) h3 options — and the negotiated protocol is then fixed for the connection. ALPN bundles security: an h2-only server that sees no h2 in ClientHello falls back to HTTP/1.1.

The senior issues: (1) TLS-rejection vs h2-not-negotiated must be distinguishable; (2) TLS 0-RTT must be gated to ONLY safe methods, because resumed session data is unprotected; (3) connection coalescing requires ALPN/cert matching. Master the h2 vs h2c vs h3 negotiation and you can explain half the protocol-selection bugs in the field.

## Q62: What is the HTTP/2 stream state machine, and why does RST_STREAM matter?

**A:** Every HTTP/2 stream moves through an explicit lifecycle: IDLE (no request yet), OPEN (an endpoint may send and receive), HALF-CLOSED (local) after sending end-stream, HALF-CLOSED (remote) when the peer ends, CLOSED (both sides finished or RST_STREAM). Transitions are driven by HEADERS with end-stream, DATA with end-stream, and RST_STREAM — invalid transitions are protocol errors that may terminate the connection.

RST_STREAM is the cancellation lever: it closes a stream immediately with an error code (NO_ERROR for clean, CANCELLED, REFUSED_STREAM, etc.). A client can abort a slow download without killing the connection; a server can refuse a pushed stream. Because streams are cheap to open and cancel, HTTP/2 multiplexing makes abort/fetch semantics nearly free — the reason browsers can "cancel a request" cleanly.

The senior lessons: RST_STREAM does NOT instantly return unused flow-control credit (the window is only reclaimed when the accounting balances), so pathological RSTs can temporarily exhaust the connection window; and error codes differ by layer (connection vs stream). Streams are the protocol's concurrency AND cancellation unit, with a strict state machine both endpoints must obey or the connection dies.

## Q63: How does HTTP/2 avoid request-framing ambiguities that enabled HTTP/1.1 smuggling, and what new surface did it open?

**A:** HTTP/1.1 smuggling lives in length ambiguity: Content-Length, Transfer-Encoding, and chunk-extensions variously give a front proxy and a back proxy different views of where one request ends. HTTP/2 eliminates framing ambiguity structurally: each message is a HEADERS block plus DATA frames with byte-exact lengths from the fixed frame header; there is no Content-Length-vs-Transfer-Encoding duality. That kills the classic smuggler.

The NEW surface is the semantic gap when a gateway TRANSLATES h2→h1 or h1→h2: the translation layer must decide how to write out edge-case messages. The canonical attacks: h2 request smuggling via `:content-length` mismatch — if a translator writes Content-Length for a body whose actual length differs (because the h2 stream carried more data frames), the h1 receiver mis-frames; and TE:chunked reattachment at a hop that re-inserts Transfer-Encoding. RFC 9113 precisely forbids these representations (a `:content-length` must match the DATA stream exactly, else connection error).

The interview answer is twofold: (1) HTTP/2 fixed 1.1 ambiguity at the cost of making TRANSLATORS the security boundary; (2) robust design requires the translator to reject ambiguous input rather than pass it through. The senior trick: look for h2-to-h1 reverse proxies and verify their length handling, because that seam is where modern smuggling exploits live.

## Q64: What is the difference between HTTP/1.1 connection coalescing and HTTP/2 connection coalescing?

**A:** In HTTP/1.1, "coalescing" describes a client reusing one keep-alive connection for sequential requests to the SAME host — a latency and socket win; each request still needs the response to finish before the next starts. HTTP/2's coalescing is bigger: one H2 connection multiplexes streams to different ORIGINS — provided those origins share the same IP, the same TLS certificate (SANs covering them), and compatible settings. A browser can fetch `a.com` and `b.com` over the SAME socket, saving a second handshake.

The rules that gate coalescing: the origins must be on the same connection (same IP + port), the certificate must be valid for both hostnames, and the connection settings must be compatible. Browser internals implement this as a coalescibility check.

The trap: coalescing is about TRANSPORT sharing, while origin identity (cookies, CORS, cache keys, TLS identity) remains strictly per-origin. So "I see a.com and b.com on one connection" is legal, but the two origins still have separate cookie jars, caches, and CORS policy — and an attacker who controls one name on a shared cert could trigger certificate confusion. In HTTP/3, coalescing is native — the mechanism propelling "one certificate, many edge hosts" CDN patterns.

## Q65: How does content negotiation select language and format, and what does Vary: Accept-Language do?

**A:** Negotiation runs on the request's Accept family: `Accept-Language: en-US,en;q=0.9,fr;q=0.7` expresses language preference; `Accept: text/html, application/xml;q=0.9` expresses format preference. The server matches those preferences against what it can produce — typically the highest-q match, tie-broken by server preference or request order. The model's wrinkle: because clients set q-values inconsistently, servers must treat them as hints and must return SOMETHING acceptable even when nothing matches exactly.

The permutation of headers x values the server used must be encoded into the response via `Vary: Accept-Language` (or `Vary: Accept, Accept-Encoding`), so caches key by those request-header values. Without Vary, a French-text copy negative-cached would be served wrongly to an English-only visitor; with Vary, each language variant becomes its own cache entry.

The senior points: Vary can only include REQUEST headers the cache saw; Vary: * means "every request is unique" (used for user-bound data); and negotiation minus q-values (a server that ignores Accept-Language entirely) is legal — but a server that honors SOME without Vary is a correctness bug. The answer: negotiation = client preferences (Accept-*) + server capability + Vary to make caching safe.

## Q66: When should you choose 303 See Other over 307 Temporary Redirect?

**A:** 303 See Other explicitly means "the result of your POST is over; go GET this new URI instead." It ALWAYS maps the follow-up to a GET, discarding method and body — the canonical Post/Redirect/Get pattern. 307 Temporary Redirect means "keep the SAME method and body, retry at this new URI temporarily."

So the choice reduces to replay intent: 303 = "use a GET now" (the POST succeeded, show the confirmation page via GET so refresh does not re-POST), 307 = "replay this exact request" (a non-GET that must reach the new location with its method). Real-world picks: form submission and login redirects → 303; MOVE of a non-safe resource where the server wants the call replayed → 307; maintenance moves of GET-only resources → 301 or 308 as a permanent same-method move.

The caching distinction: 301/308 (permanent) are cacheable by default; 302/307 (temporary) are typically re-checked. And in HTTP/2/3 the method-rewrite is still the semantic layer's job — the redirect is a status code; the client applies the rewrite rule. The interview conclusion: 303 specifically exists to turn side-effectful success into a safe follow-up GET; 307 exists so every redirect does NOT do that.

## Q67: What is the difference between 200 OK and 206 Partial Content for range requests?

**A:** 200 OK is the full-resource success: the response body is the complete representation. 206 Partial Content is the success answer to a Range GET: the body carries ONLY the requested byte ranges, with Content-Range indicating which ranges and the total size, and representation metadata (ETag, Last-Modified, Content-Encoding) describing the WHOLE resource. A client sees 206 when the server honors Range; 200 when it ignores ranges and serves the full body; and 416 when the range is unsatisfiable (start beyond EOF).

The caching and integrity rules are sharp. 206 is cacheable with its fragment, and shared caches may assemble complete cached representations by fetching missing ranges — provided the ETag/Last-Modified match makes reassembly coherent. 206 must not be returned for an invalid range; and because Content-Range references the TOTAL size, a 206 reveals the resource's full length even when only a piece is downloaded.

For senior candidates: If-Range makes range requests conditional (preventing a resumed download from splicing bytes from a changed resource); a server that cannot settle the length of a streamed body cannot promise ranges (sends 200 instead); and CDN origin-fetch behaves differently with ranges (request upstream full, cache the whole, serve the range). The mental model: 200 = complete; 206 = coerced fragment of a complete representation; 416 = the fragment request was nonsense.

## Q68: What is the `Vary` header, and what does `Vary: Accept-Encoding` actually mean for a cache?

**A:** Vary declares the REQUEST HEADER NAMES that influenced the response. A cache receiving `Vary: Accept-Encoding` must key that response by the A-C-E VARY value: the compressed variant and the plain variant become separate cache entries, and a request carrying `Accept-Encoding: gzip` gets the gzip entry while `identity` gets the plain. Without Vary, a gzipped copy leaks to a client that cannot decode it. `Vary: *` means "this response varies on anything — effectively uncacheable," used for per-user or per-request-tailored content.

The discipline rules: Vary is only honored by caches that can see the request headers named; intermediaries that transform the response must ensure Vary still truthfully describes the remaining variability — a proxy that decompresses while a shared cache keyed on Accept-Encoding lingers is a correctness landmine. Also: Vary headers compound (Vary: Accept-Encoding, Accept-Language), each name multiplying the key space — which is why big caches cap variant counts.

The senior nuance: Vary controls STORAGE partitioning AND revalidation. A Vary-ed response with a strong ETag must have the ETag computed over the SAME variant bytes. And CDN debugging (why is my English page served to a French request?) is ~70% likely a missing/wrong Vary. Describing Vary correctly is a strong signal a candidate understands HTTP caching deeply.

## Q69: What is request smuggling, and what are the canonical exploit shapes in HTTP/1.1?

**A:** Request smuggling is where an attacker uses the DIVERGENT parsing of the same byte stream by two intermediaries (typically a front proxy and a backend server) to inject traffic. The canonical shapes: CL.0, CL.TE, TE.CL, TE.TE — combinations where one parser trusts Content-Length and the other trusts Transfer-Encoding. The attacker crafts a first request whose tail is a partial second request; the front passes only the first; the backend reads past and parses the second as the victim's request — poisoning cache, hijacking sessions, or bypassing WAFs.

The fix: every parser must apply the same framing rules — RFC 9112 says if both Content-Length and Transfer-Encoding are present, treat as unconditional 400. HTTP/2 killed the ambiguity structurally (byte-exact frames), but every h2→h1 translator must re-check because the translation seam reopens CL/TE divergence.

The senior part: smuggling is the "framing is a security boundary" lesson — the attacker does not need to break TLS; the vulnerability is pure parsing. Defending means enumerating every hop, standardizing its parser version and length rules, and proactively testing seams. An interview answer that lands CL/TE ambiguity, the two-hop trust model, and the HTTP/2 translation seam is a full senior-depth answer.

## Q70: What is the purpose of `no-transform`, and which Cache-Control combinations must you never use?

**A:** `Cache-Control: no-transform` forbids intermediaries from altering the representation — no re-compression, no conversion of images, no insertion of tracking. It exists because intermediaries have a history of rewriting content in ways that break signatures, licensing, or content policies. It pairs with `private` for user-scoped data and intensifies the "intermediary transparency" argument for strong ETags.

The "never combine" list: `no-store` + `public` (storable by nobody vs storable by shared caches are contradictory), `no-cache` + `max-age>0` (max-age hints freshness but no-cache forces revalidation — legal but self-defeating), `must-revalidate` without a validator (a cache cannot honor it), `private` + `s-maxage` (s-maxage applies to SHARED caches — meaningless on a private response). `immutable` without a date also toggles nothing.

The nuance: no-transform interacts with Vary and content negotiation — an intermediary may only transcode when the response allows it and must then update Vary/encoding headers coherently; and it is an all-or-nothing declaration that some CDNs intentionally ignore under acceptable-use policies, which is why resources needing byte-identity should also carry a strong ETag AND immutable.

## Q71: How do HTTP/2 and HTTP/3 differ at the application layer?

**A:** HTTP/2 runs multiplexed streams over TCP with HPACK; HTTP/3 runs the same model over QUIC (UDP) with QPACK, and the differences reach into frames and flow control. HTTP/3 stream types differ: besides request streams, HTTP/3 defines UNIDIRECTIONAL streams for QPACK encoder and decoder, plus control streams carrying SETTINGS, GOAWAY, MAX_PUSH_ID, CANCEL_PUSH. Frames mostly match (DATA, HEADERS, SETTINGS, PING, GOAWAY, RST_STREAM) but with QUIC-era additions and GREASE frame types to exercise unknown-frame handling.

Header compression is the most visible change: HPACK needs a single, in-order dynamic table shared over one transport — on QUIC, headers travel on streams that may be lost and reordered, so a shared in-order table would desync. QPACK instead runs table updates over a dedicated encoder stream with acknowledgments, lets each stream's header block reference table positions either by index or by literal, and recovers missing references by asking the encoder to retransmit. This means a lost header update stalls only the affected streams, not the connection.

The other deltas: HTTP/3 gives each endpoint its own stream-numbering space (odd/even per direction); and the HTTP semantics (methods, status, caching, redirects) are IDENTICAL. The drift is "same semantics, new substrate: frames + QPACK + unidirectional control streams."

## Q72: What is the HTTP/3 SETTINGS and control-stream topology?

**A:** HTTP/3 opens its synchronous setup with a client-issued bidirectional request stream carrying SETTINGS, then the client opens unidirectional CONTROL streams (one for the transport's control frames, one for QPACK encoder, one for QPACK decoder-request), and the server mirrors with its own control and QPACK streams. Frames like SETTINGS, GOAWAY, MAX_PUSH_ID, CANCEL_PUSH ride the control stream; PING and DATAGRAM use connection-level semantics. Both SETTINGS may arrive in EITHER order; each side only ACKs the other's SETTINGS via its own control stream.

The novel streams exist because QUIC cannot guarantee ordering across different streams: control frames travel on a dedicated unidirectional stream so HEADERS/DATA interleavings do not touch them, and the QPACK encoder stream delivers table mutations IN ORDER (its own stream guarantees that). The decoder-request stream is where the client notices a table miss and asks the encoder to resend the absent entry.

For interview depth: HTTP/3's SETTINGS are processed with the same ACK dance as HTTP/2, and a misbehaving encoder stream is a connection-error condition. The topology — "one bidirectional request stream per request + three unidirectional control/QPACK per endpoint" — instantly explains why "the first stream" is not the first datagram.

## Q73: What is RFC 9218 Extensible Priorities, and how do HTTP/3 priorities differ from HTTP/2 weights?

**A:** RFC 9218 replaces HTTP/2's PRIORITY-frame dependency+weight tree with a far simpler model: each request may carry a `priority` header specifying an urgency value (0-7, 3 default) and an `incremental` flag. Urgency 0 wins over 1, etc.; the incremental flag declares "this request can be split across the scheduler's incremental delivery slots" (useful for streaming, video previews, HTML streaming) vs "send me as a whole unit." The SCHEDULER uses urgency to pick which stream's frames to emit.

The semantic gain: urgency is a small, communicable contract — a server can read it and schedule accordingly without parsing a tree; incremental lets low-latency, freshly-arriving bytes flow without being held for an entire response. HTTP/2's tree never achieved meaning because servers ignored it; the new model's simplicity (a number + a boolean) has genuinely been adopted by CDNs and Chrome.

The senior contrast: HTTP/2 PRIORITY_PAUSE was a starvation tool; RFC 9218's urgency is "relative scheduling intent," processed shoddily by some but far more implementable. The transport still does not reserve bandwidth — the scheduler does — so priorities are "policy," while QUIC provides the mechanisms (multiple streams, reset, flow control) that let policy act.

## Q74: What is PUSH_PROMISE in HTTP/2, and how does stream cancel interact with pushed promises?

**A:** PUSH_PROMISE is the frame a server sends BEFORE the actual push: on the stream it is fulfilling, it emits PUSH_PROMISE naming the resource (via a synthetic :method GET request) and promising a future stream. The client may accept (use it) or reject with RST_STREAM/REFUSED_STREAM. Pushed streams are identified and counted like normal streams, and MAX_CONCURRENT_STREAMS historically includes pushes — a server that pushes between ACKed limits can exhaust the client's budget.

The reason it matters beyond browsers: pushed transfers are a bandwidth-hog; a client that does not need the push can cancel, but the cancel only affects the later stream — the PROMISE itself cannot be unmade. And the interleaving contract: PUSH_PROMISE must be sent within the response HEADERS block of the triggering request, so the association is reliable; a promise referencing an already-cancelled stream is a protocol error.

Given browsers disabled push, the senior correct usage leans on the reference model: push is a cache-warming mechanism, and research showed the failures (cache misses, wasted bandwidth) outweigh its benefit. The conclusion: understand PUSH_PROMISE mechanics, then explain why HTTP/3 made it effectively inert, and gesture at the modern replacement (103 Early Hints + preload).

## Q75: What is the HTTP/3 "grease" frame-type recommendation?

**A:** RFC 9114 recommends implementations occasionally send "grease" frames — unknown-value frame types — so that middleboxes and LB software cannot hardcode "frame type 0x0 is DATA, everything else is a bug." By exercising random unknown types, endpoints train the ecosystem: a conformant receiver MUST silently skip unknown frame types, and a server that drops on unknown frames breaks interop with future extensions.

The contrast to HTTP/2: HTTP/2 also allows unknown frames to be ignored, but HTTP/3 formalizes the posture: unknown frames on request streams are to be IGNORED, while unknown frames on the control stream may be treated as a connection error. This is the "grease prevents ossification" design — any future feature (DATAGRAM, etc.) can deploy without a flag day, as long as receivers ignore rather than reject.

Interview depth: grease is a deliberate answer to TCP's invariants problem. Frame-type grease + version greasing + the quic-bit enforce "reject nothing you don't understand." The senior answer frames it as protocol-maximizing-extensibility, letting HTTP/3 add frames without a browser update — while cautioning that silently ignoring critical frames is dangerous, which is why the spec separates "ignore extension frames" from "control-stream frames must be understood."

## Q76: Design the HTTP semantics for an idempotent "create-or-replace" API. What methods, status codes, and headers?

**A:** The strongest pattern is PUT-to-a-known-URI with unconditional replace semantics: the client issues `PUT /orders/ABC-123` with the desired state; the server stores it whole (creating if absent, replacing if present), returning 200 (replaced) or 201 + Location (just created) — either way the operation is idempotent: N identical PUTs converge to the same state. To guard against race conditions, add `If-None-Match: *` for create-only ("only create, fail 412 if exists") or carry the client's ETag for guarded replace (`If-Match: "abc"` → 412 on mismatch).

When the exact PUT URI is unknown (server-assigned IDs), flip to POST with an Idempotency-Key header: `POST /orders` with `Idempotency-Key: <uuid>`; the server stores consumed keys and for any retry with the same key returns the original response. This is the payments-SDK pattern — POST + Idempotency-Key — and it works because the server enforces key constraints transactionally.

The senior refinements: (1) apply optimistic concurrency with If-Match + ETag, because an unconditional last-write-wins PUT clobbers concurrent editors; (2) respect Prefer: return=representation for response bodies; (3) use 409/412 vs 400/422 to distinguish state conflicts from invalid values; (4) never return redirects that rewrite the method from the contract. The evaluator checks: does the candidate reach for PUT-over-POST, If-Match/If-None-Match, and an idempotency key when IDs are server-side.

## Q77: What are the full membership semantics of 404, 410, and 401/403?

**A:** 404 Not Found means the resource does not exist on this origin right now — the canonical response for unknown URIs and, deliberately, for hidden endpoints (responding 404 for endpoints you prefer not to acknowledge is both privacy best-practice and mandatory in some threat models). 410 Gone says the resource DID exist and is now intentionally and permanently gone — the difference is permanence: SEO crawlers learn to de-index 410s, and clients stop expecting resurrection.

401 Unauthorized (the name is misleading) means YOU ARE NOT AUTHENTICATED: no credentials, expired credentials; the response SHOULD carry `WWW-Authenticate` describing the challenge. 403 Forbidden means YOU ARE AUTHENTICATED BUT NOT AUTHORIZED: the identity is proven, the permission is denied. The four interplay: missing login → 401; logged-in-but-can't-see → 403; can't-tell-existence → 404; definitely-was-but-gone → 410.

Senior application: 401 vs 403 is authN vs authZ; a client that gets 403 must NOT silently retry (no token refresh will help unless it changes the account), while 401 supports retry after obtaining credentials. 404-vs-410 changes crawler/client memory and cache behavior. On public APIs, prefer 404 over 403 for resource-level existence checks except where 403 is a genuine permission warning, because 404 denies information an attacker could use to map resources.

## Q78: What is the difference between a response's Cache-Control on shared vs private caches?

**A:** `private` restricts caching to the BROWSER (end-user's cache); `public` permits shared/intermediary caches (CDNs, proxies) to store the representation — with the crucial default that responses with `Authorization` are NOT shared-cached unless explicitly `public`. `s-maxage` overrides the caching lifetime for SHARED caches only; its browser-side counterpart is max-age. `must-revalidate` tells caches that once stale they MUST contact the origin before serving — stale data may never be served silently, even under network failure. `proxy-revalidate` narrows the obligation to shared caches.

So `Cache-Control: public, max-age=60, s-maxage=300` says "client stores 60s, CDNs store 300s, and even though the CDN may serve old bytes for 5 minutes, it must revalidate first." The failure mode it prevents is a shared cache serving stale representations forever or serving stale bytes on a network error — allowed only with `stale-if-error`.

Senior nuances: (1) must-revalidate only forces revalidation on STALE copies — fresh-but-dirty does not trigger it; (2) `no-cache` + `must-revalidate` is the paranoid combo (every reuse hits the origin); (3) proxies that add their own Age adjust the revalidation math; (4) for user-specific content, `private, no-store` typically beats sharing, because a shared cache holding a per-user ETag variant can still serve the wrong variant if Vary is wrong. The exam-worthy framing: directives have different meaning per cache type, and s-maxage/must-revalidate are the knobs that encode "CDN may be generous, but never wrong."

## Q79: What is stale-while-revalidate, and how does it change caching behavior?

**A:** `stale-while-revalidate` (SWR) permits a cache to serve a STALE representation IMMEDIATELY while, in the background, it contacts the origin to fetch the fresh copy for the next request. `Cache-Control: max-age=60, stale-while-revalidate=300` — after 60s the copy is stale, but for 300s a cache may serve old bytes instantly while revalidating asynchronously. The point is latency masking: revalidate-on-demand (no-cache) blocks each user's first request; SWR makes the FIRST request fast, and the cost slides into background.

The tradeoffs: SWR serves possibly-outdated data during the window — acceptable for content you control the freshness of; it does NOT help when the client must have the newest bytes (account balance, seat inventory). There is also `stale-if-error` (serve stale only when origin errors). On top of that a cache must encode "currently revalidating" per entry — the bane of naive implementation is a stampede where ALL instances revalidate simultaneously (the thundering herd); single-flight revalidation logic in the CDN solves it.

Interview-grade answer: contrast the four postures — max-age (fresh, fast), no-cache/revalidate (correct, slow), stale-if-error (fast when origin breaks), stale-while-revalidate (fast ALWAYS + eventually correct) — and mention that SWR efficiency depends 100% on the ETag-based 304 path working and on the cache being shared (single-flight).

## Q80: When should an API use PUT with If-Match over PATCH, and when is POST with Idempotency-Key better?

**A:** Choose PUT+If-Match when the operation is "replace this entire resource, but only if it is the version I think it is": the client has the current ETag, wants a full overwrite, and must not clobber concurrent edits. The precondition makes correctness atomic — the server 412s on mismatch; retries are safe because PUT is idempotent. Choose PATCH when the update is PARTIAL and the client does NOT want to send the whole state — but PATCH is NOT idempotent-by-default, so pair it with If-Match for the same concurrency safety.

Choose POST+Idempotency-Key when the action is a NON-idempotent side-effecting operation (charge a payment, create an order) that must be exactly-once: the client generates a key, the server dedupes — the same key returns the cached original response, a different key is a new action. This beats PUT semantics when the resource being created does not yet exist and the URI is unknown.

The senior-matriculation answer: PUT with If-Match for absolute, versioned replacement; PATCH with If-Match for versioned partial mutation; POST + Idempotency-Key for once-only side effects where the idempotency boundary lives in application state, not in the method's semantics. And note: never leave idempotency to chance when money is involved.

## Q81: What is the 412 Precondition Failed response, and how do preconditions interplay with caches and concurrency?

**A:** 412 is returned when a precondition header evaluates false — the server did NOT perform the method. The canonical preconditions: If-Match (perform the write only if the resource matches that ETag — the optimistic-concurrency guard), If-Unmodified-Since (perform only if unchanged since a datetime), If-None-Match (perform only if it does NOT match — the cache-revalidation guard), If-Modified-Since (the cache freshness guard, returning 304 when not modified). 412 is "you lost the race" for a guarded write.

The caches' interplay: preconditions make revalidation atomic. A stale cache sends If-None-Match; 304 revalidates (keep cache, headers refresh freshness); 200 replaces. If-Match on a write makes the UPDATE atomic against concurrent writers — a lost update returns 412 rather than silently clobbering. Server-side evaluation order matters (If-Match trumps If-Unmodified-Since; If-None-Match trumps If-Modified-Since), and a 412 means NO side effect happened, protecting writes from being performed under a stale view.

Senior detail: a PUT/PATCH/DELETE with If-Match is the protocol-native compare-and-swap; systems that GET → compute → PUT without If-Match are vulnerable to lost updates. And note that 412 handling should return the CURRENT ETag when cheap so clients can rebase; weak ETags are forbidden for If-Match writes that mutate.

## Q82: What is the correct response when a negotiated request has no matching Accept?

**A:** When the server cannot produce any representation satisfying the Accept header, the correct response is 406 Not Acceptable, with a body listing available representations. 406 = I can't RETURN what you asked for; 415 Unsupported Media Type answers the request's content-type problem: I can't READ what you sent. 400 remains for unparseable syntax; 422 for parseable-but-invalid semantics.

The distinctions are both verb-facing and cache-relevant: 406 is about content negotiation, 415 about content submission, and both are client errors. Neither should be retried blindly.

Senior nuance: 406 should not leak internal information about every variant; 415 should enumerate accepted types so automated fallback is possible. The common prod bug is 406 not being sent because the server silently defaulted — masking client bugs; and conversely, strict 406 on a `*/*` request is a server bug because wildcard means everything is acceptable.

## Q83: What is the "Origin" header's role in CORS, and how do Access-Control-Allow-Origin and Allow-Credentials combine?

**A:** `Origin: https://app.example.com` is a REQUEST header the browser attaches to cross-origin fetch declaring which origin initiated the request; the response's `Access-Control-Allow-Origin: https://app.example.com` (or `*`) tells the browser whether the RESPONSE may be REVEALED to that origin's JavaScript. Unlike Referer, Origin never includes a path and is immutable from script — a deliberate anti-CSRF signal.

`Access-Control-Allow-Credentials: true` declares the cross-origin request may carry CREDENTIALS (cookies, TLS-client auth). The rule: when credentials are allowed, Allow-Origin MUST be a specific origin (not `*`), and Vary: Origin MUST reflect that the Allow-Origin is origin-specific — otherwise an attacker reading a cached Allow-Origin from a shared cache poisons other origins. The pairing bug: `Allow-Origin: *` + `Allow-Credentials: true` is forbidden by spec and dropped by browsers.

Senior traps: (1) CORS does not authenticate — an allowed origin is a READ permission, not write; CSRF protection needs separate machinery (SameSite, tokens). (2) Wildcards and the preflight cache interact — a cached preflight with Allow-Origin: * cannot suddenly allow credentialed requests. (3) Echoing the request's Origin blindly into Allow-Origin is a CORS misconfiguration — validate against an allowlist server-side.

## Q84: How does `If-None-Match: *` create-if-absent compare with "GET then POST" for concurrency?

**A:** `If-None-Match: *` on a PUT tells the server "perform the create ONLY if no representation currently exists at this URI" — the server atomically checks existence and writes in ONE operation, returning 201 on success or 412 on conflict. The naive "GET then POST" pattern is check-then-act: the client GETs, learns "not found," then creates — a gap where another client can create the same resource between the GET and the write, producing a duplicate.

The concurrency win is the atomicity: If-None-Match: * and If-Match: etag are compare-and-swap primitives the origin evaluates against its current state under whatever transaction the endpoint holds. There is no application-level split. The corresponding Idempotency-Key create (POST to a collection with a key) achieves the same atomicity by making the KEY the uniqueness constraint.

The senior synthesis: if your API supports "create user with id X" (client-chosen IDs), If-None-Match: * is the proper atomic guard; if IDs are server-assigned, POST + Idempotency-Key achieves it. Engineers who rely on "GET to detect absence" build race-y systems; the protocol-native primitives exist precisely to close that gap.

## Q85: What is a "strong" versus "weak" ETag, and when does each serve which semantic?

**A:** A strong ETag ("abc123") means the representation is byte-for-byte what the tag describes — a semantically-equivalent comparison. A weak ETag (W/"abc123") means the representation is semantically equivalent — the same meaning but not necessarily identical bytes. The spec draws the line: weak tags are acceptable for cache revalidation (If-None-Match — "changed or not?"), while strong tags are REQUIRED for range requests and guarded writes (If-Match must reflect byte-identical state or concurrency protection is false).

The assignment is up to the server: an origin may emit weak tags when it wants "same semantic content updated with different bytes" — a cache's If-None-Match with a weak tag returns 304, saving a body transfer. Strong tags are typically content hashes or version numbers guaranteeing byte identity.

Senior-world guidance: (1) Cache/CDN ETag pass-through — when a CDN re-encodes a body, the ETag must change or the tag cannot validate the variant. (2) Deterministic content-hash strong ETags give cache-fill-correctness AND a natural optimistic-concurrency key. (3) For atomic writes, If-Match with a strong tag is the requirement — weak tags are only for "changed since last GET" decisions, never for "this exact byte state is what I'm overwriting."

## Q86: What is `Vary: Origin`, and how do you safely cache an API response that varies by requester?

**A:** `Vary: Origin` means the response differs depending on the request's Origin header, so cache entries must be keyed by Origin. It is the mandatory companion to origin-specific Access-Control-Allow-Origin responses: if a server computes Allow-Origin: https://a.com for requests from a.com, a shared cache MUST store that response under Vary: Origin, or another origin could receive a.com's Allow-Origin — either failing CORS or permitting cross-origin reads. Omitting Vary: Origin on a per-origin CORS response is among the most common CDN + CORS data-leak bugs.

For general API content that varies per requester, the guidance chains: `Cache-Control: private` (only the browser may cache), OR `no-store` for sensitive per-user data, OR if you genuinely want shared caching with correct variants: `public, s-maxage=..., Vary: Cookie, Authorization, Accept-Encoding`. The senior rule: Vary must list EVERY request header that influenced the representation, and shared caching of per-user data works only when the variants are keyed by the full differentiating input.

The resolution: either mark it private/no-store (no sharing) or drive Vary precisely (sharing per-variant). A `Vary: Authorization` step is a transparently-safe cors CDN key because the client's token distinguishes variants. And with Vary: *, a server can be maximally safe at the cost of uncacheability.

## Q87: How do HEAD and GET responses share a cache entry?

**A:** Per RFC 9111, a HEAD response is stored in cache storage like any other response, and a cache MAY satisfy a HEAD request using the stored representation of a GET — serving the headers with an empty body. The reverse does NOT hold — a HEAD cannot satisfy a GET (which needs the body). So HEAD fetches share the same cache entry as GET fetches for the same resource, keyed by request-target + Vary.

The freshness semantics: a HEAD request is processed with the same freshness rules — if the cached GET entry is fresh, HEAD is served 200+headers from cache; if stale, the cache may revalidate (If-None-Match) on HEAD's behalf, and the revalidation updates the stored entry. This is why a monitoring tool using HEAD can "warm" a cache's metadata without transferring bytes.

Senior edge cases: (1) Cache-Control: no-store forbids storing the HEAD response's headers; (2) an origin that behaves differently for HEAD (different Content-Length) creates inconsistent cache keys; (3) a HEAD whose headers claim a body length must still not leak the body when a cache later serves a GET. The interview point: HEAD is the cache-prudent "metadata peek," not a different resource, and its cache identity is shared with GET.

## Q88: What is the practical semantic difference between serving an API over HTTP/1.1 and HTTP/2?

**A:** At the SEMANTIC layer, nothing changes — methods, status, headers, caching, redirects are identical. What breaks is everything the transport model touches. First, concurrent stream limits: HTTP/2 permits ~100 simultaneous requests per connection, so an API that assumed one-active-request-per-socket will stall under H2's interleaving if it needs extra connections to break the constraint. Second, header limits are now SETTINGS-driven: huge headers that HTTP/1.1 accepted may hit MAX_HEADER_LIST_SIZE and fail.

Third, flow control: H2's per-stream windows are 65535-byte default; a large response without the client's WINDOW_UPDATE advancing stalls silently. Fourth, HEADERS frames are the only place you can end a GET; a half-stream that never terminates leaks a stream slot. Fifth, coalescing means a SLOW response blocks the connection's scheduler.

And the operational breakage: HTTP/2 exposes no Connection header (phony proxies break), no Transfer-Encoding: chunked (the translation layer must map frames), and Upgrade is gone. The senior answer: semantics are transport-independent; the breakage is always in the WAY the semantics are carried.

## Q89: How does HTTP/2's SETTINGS_MAX_FRAME_SIZE and the WINDOW_UPDATE dance affect a large response?

**A:** Every stack advertises SETTINGS_MAX_FRAME_SIZE (default 16384, max 16777215) — the largest DATA frame the receiver will accept. WINDOW_UPDATE advertises the flow-control window: the sender can emit at most min(connection window, stream window) bytes of DATA before needing WINDOW_UPDATE from the receiver. For a large response, the sender writes data frames up to frame-size and window limits, waits, reads WINDOW_UPDATE(s), and continues.

The interaction bites in three shapes: (1) very large responses over high-latency links stall waiting on tiny default windows (65535) unless the receiver raises INITIAL_WINDOW_SIZE early; (2) a WINDOW_UPDATE race where receiver grants credit but the stream is cancelled — bookkeeping must match or credit leaks; (3) a server that assumes one frame = one full message breaks under multiplexing.

The senior-grade rule: flow control throttles rate; frame size throttles granularity; both are per-connection requirements, and neither is optional. An implementation that "just sends everything" without honoring the advertising window is nonconformant. The practical weave with HTTP/3: same semantics but QUIC's own flow control supplies the per-stream/connection levels.

## Q90: What does it mean for HTTP to have "no notion of time," and what roles do Date, Expires, Age, and Retry-After play?

**A:** HTTP semantics deliberately avoid a strong notion of time save for a small set of timestamps whose looser equivalence classes matter: Date (when the origin generated the response), Expires (legacy "when should this expire" hint, superseded by max-age), Age (how long the response has sat in caches), Last-Modified (the origin's guess at last representation change — a weak validator), and Retry-After (a suggested wait before retrying). The protocol is careful NOT to assume clocks are synchronized: freshness math tolerates clock skew because Age is cache-observed and max-age is relative to the response's own Date.

So "no notion of time" means: HTTP does NOT rely on synchronized clocks for correctness — a response's observers must derive its age from transmitted headers, not wall-clock assumptions, and must treat Expires/Last-Modified as weakly consistent hints. Retry-After is the one place the protocol deliberately biases: it tells a client "try again after this delay," used by 429 and 503, and its honesty prevents thundering-herd retries.

The senior adders: (1) clock skew is why max-age + Age is reliable while Expires is not; (2) If-Modified-Since MUST NOT be used when a strong ETag is present (If-None-Match wins); (3) Retry-After vs its absence: polite clients backoff-exponentially when absent. HTTP structures time DELIBERATELY, providing headers for freshness, but demanding cache math rather than trusting clocks.

## Q91: How would you implement "read your own writes" consistency for a cacheable HTTP API?

**A:** The clean pattern: every mutable operation invalidates or purges the cached representations it affects, and GETs re-validate against a strong validator. Concretely: (1) every response carries a deterministic strong ETag (body hash) and explicit cache policy (`Cache-Control: public, max-age=...` or private/no-store), with Vary naming the request headers that varied the representation. (2) On a mutation, the origin bumps the resource's version/ETag, so any subsequent stale GET revalidates with If-None-Match and receives 304 or 200. (3) If your API exposes whether a response came from origin or cache (Age header), the mutating client can assert its write took effect by re-fetching and comparing the ETag.

The sticky part is the browser and CDN write history: a browser can, after a POST, bypass the cache by issuing the follow-up GET with `Cache-Control: no-cache`; a CDN can purge on invalidation via its management API. Without explicit invalidation, a user who POSTs and immediately GETs sees the OLD cached copy — the classic "my update disappeared" report.

Senior refinements: for low-consistency data, shrink max-age (5-30s) so stale-after-write windows stay bounded; for money/authN, mark private/no-store and force origin reads; and use `Cache-Control: no-cache` + ETag revalidation on mutation responses so caches re-fetch rather than serving eternal stale. Strong validators + explicit mutation invalidation + bounded freshness = read-your-writes for cache-trafficking APIs.

## Q92: What is the uncacheable-by-default rule for Authorization, and how do you make a user-specific API safe and performant?

**A:** RFC 9111: a response to a request with `Authorization` must NOT be shared-cached unless the response explicitly says `Cache-Control: public`. The reason is security: a shared cache that stores "responses to requests with Authorization" could serve one user's data to another. So the safe floor: user-specific content is served with `Cache-Control: private, no-store` (browser may cache per-user; shared caches may not), or `private, max-age=N` if browser-side freshness is acceptable.

To make it performant without leaking: (1) private + strong ETag + If-None-Match: the browser revalidates cheaply; the origin answers 304 without body. (2) Split the response into a public part (`public, max-age`) and per-user part (`private/no-store`) — CDN caches the former, browser handles the latter. (3) For rate-involved content, `Vary: Authorization` makes the shared cache per-user-keyed — which is safe but multiplies key space.

Senior practice: use the "ETag + no-cache" pattern for user-specific endpoints — each request does one trip to origin for If-None-Match, gets 304 without body; set `Cache-Control: private, no-store` on mutation responses; and treat "Authorization responses can be shared-cached with `public`" as a deliberate exception for genuinely-public endpoints that require auth to see — even then, Vary: Authorization is the conjunction most get right only with explicit intent.

## Q93: What is the difference between Cache-Control: no-cache and no-store in a mutating-response context?

**A:** `no-store` means "do not store this response at ALL" — neither body nor headers may be retained anywhere. It is the correct marker for one-shot, per-user, or data-difference responses where ANY reuse risks serving someone else's data (payment confirmations, session-invalidating responses). `no-cache` means "you MAY store it, but you MUST revalidate with the origin before REUSING it" — a shared cache holds the representation but a subsequent request triggers If-None-Match/If-Modified-Since.

The semantic difference in POST-response context: no-store says "don't keep the sensitive payload anywhere a subsequent restore could resurrect it"; no-cache says "keep it, but re-fetch before using." For mutation responses, the Post/Redirect/Get pattern means the redirect target (the GET) should be cacheable under its normal policy, while the POST response itself should be no-store if it carries unique bytes.

The famous interplay: a POST/redirect creating state — the POST response carries the reservation/confirmation unique bytes and should be no-store, while the GET confirmation page follows normal caching. Knowing that revalidation is cheapest when the origin is fast — guaranteeing a 304 — is the boundary interviewers probe.

## Q94: What is the role of the Upgrade header and WebSocket in HTTP semantics?

**A:** In HTTP/1.1, the `Upgrade: websocket` header (paired with `Connection: Upgrade`) performs a protocol switch on the SAME TCP connection: the client asks the server to switch to the WebSocket protocol, the server replies 101 Switching Protocols, and the socket stops being HTTP and starts speaking raw WebSocket frames. That is the entire trick — HTTP acts as a bootstrap handshake, and after 101 the request/response semantics are over on that connection.

With HTTP/2, `Connection: Upgrade` is BANNED, so the WebSocket-over-H2 path uses the extended CONNECT with the `:protocol: websocket` pseudo-header: the client opens a CONNECT stream with :protocol, the server sends 200, and the tunnel rides that stream. HTTP/3 mirrors this with the same CONNECT-on-a-QUIC-stream model.

The semantic question: is WebSocket "HTTP"? No — it is a separate protocol that borrows HTTP for its handshake; the entire semantics (messages, fragmentation, opcodes, ping/pong) live outside HTTP. But the HANDSHAKE decides which machine speaks HTTP and which speaks WS, so header-based negotiation and policy enforcement (origin validation) live at the HTTP layer. Senior answer = 101 is the switch; h2 uses extended CONNECT; HTTP semantics apply only until 101/CONNECT-established.

## Q95: What does GET with a body mean, and why is it discouraged?

**A:** RFC 9110 permits a GET to carry a request body, but it is DISCOURAGED because no defined HTTP semantics treat a GET payload meaningfully: caches never store it, proxies may drop it, some intermediaries reject it, and the negotiation/cache/replay rules are defined for the request's header/precondition parts only. The practical stance of the browser and nearly every framework: GET bodies are either ignored or treated as an error.

The reason it matters: a developer who overloads GET-with-JSON-body to "query with complex filters" discovers that a shared cache (which keys GET by URL + Vary) does not include the body in identity, so two DIFFERENT GET-with-bodies against the same URL retrieve each other's data, and a proxy that strips bodies breaks the query silently. That is why query parameters exist — the URL is the cache and identity key.

The senior guidance: preferred patterns for "semantic reads with complex input" are GET with well-formed query params, or POST with `Content-Type: application/json` when the query exceeds URL limits — and designers who need "I read, but I have a big readable input" often pick a deliberately "POST for query" endpoint (the widely used SOAP/GraphQL pattern) while acknowledging the loss of safe/idempotent guarantees. The constraint is not "GET cannot carry a body" but "the body is outside the semantic contract."

## Q96: What is the relationship between Allow, OPTIONS, and 405, and what does Accept-Post/Accept-Patch add?

**A:** `Allow` is the header enumerating the methods a resource permits: `Allow: GET, HEAD, OPTIONS` — and every 405 Method Not Allowed response SHOULD carry it. `OPTIONS` is the discovery verb that returns Allow so a client can learn the operations map without trying and failing. 405 + Allow is the standard "wrong verb" contract, distinct from 301 (resource at another location) and 404 (does not exist).

`Accept-Post: application/json` declares the media types the resource can process on a POST; `Accept-Patch: application/json-patch+json` declares what a PATCH endpoint accepts. They extend the Allow model into "what payloads are acceptable per method" — the machine-readable muscle of hypermedia-driven discovery. A client reads Allow to see verbs and Accept-Patch/Post to see payloads, then chooses.

Senior nuance: 405 ≠ 501 Not Implemented (server does not support the method AT ALL) — 405 is per-resource permission, 501 is capability. And CORS adds a twist: preflight (OPTIONS + Access-Control-Request-Method) parks on top of OPTIONS and the response also needs Access-Control-* headers, so a server must answer OPTIONS successfully even for methods it would 405 — CORS preflight never carries the real method. The takeaway: Allow + OPTIONS + 405 + Accept-* compose the "credible capability surface" of a resource.

## Q97: How does HTTP/3's MAX_PUSH_ID interact with stream cancellation, and what happened to push?

**A:** HTTP/3 controls push via MAX_PUSH_ID: the server may initiate push streams only up to the highest push ID the client has authorized. The client can refuse a specific push with CANCEL_PUSH, and any push stream exceeding MAX_PUSH_ID is a connection error unless reset. Push is therefore a client-delegated permission system — far more constrained than HTTP/2.

What happened: browser vendors disabled HTTP/2 push in practice (Chrome refused pushes, testing showed limited benefit and real bandwidth waste), so while RFC 9114 retains the concept, real HTTP/3 deployments never push. MAX_PUSH_ID is a concession: the client says "you may push with ID up to N" and never grants more.

So the full picture: HTTP/2 push = server-initiated PUSH_PROMISE with client can REFUSE; HTTP/3 push = client-authorized MAX_PUSH_ID + per-push CANCEL. The accurate senior statement is "push is a deprecated curiosity; the modern mechanisms are preload hints and Early Hints, both because they respect client cache discipline."

## Q98: If you were designing an HTTP-based API today, which version would you serve and what header/status architecture?

**A:** Serve BOTH HTTP/2 over TLS (the universal default for browsers) and HTTP/3 opportunistically via Alt-Svc where your edge supports QUIC, with HTTP/1.1 as automatic fallback for legacy. Because HTTP semantics are transport-independent, you inherit correctness across all three — the choice is a transport-performance decision, not semantics. In practice: one origin that advertises h3 via Alt-Svc, ALPN h2 as baseline, h1 only as residual fallback, all sharing the same cache-control, ETag, and Vary discipline.

The header/status architecture: strong deterministic ETags + If-None-Match everywhere caches are allowed; explicit Cache-Control on every response (max-age + s-maxage for public fragments, no-store/private for per-user payloads, no-cache for revalidate-first); Vary naming every variant dimension; semantic status codes as interviewers expect (200/201/204 by mutation intent, 301/308 permanent vs 303/307 temporary, 400-429 accurately split, 5xx honest and retry-safe); and idempotency-by-key on every non-GET side-effect endpoint, gated preconditions (If-Match) on writes, and Retry-After on throttle.

The senior closing note: the API's quality is defined less by which version and more by the SEMANTIC discipline — correct method idempotency/safety, honest status codes, faithful Vary/ETag caching, atomic guarded writes, and a coherent safe-method/idempotent/retryable taxonomy etched into every endpoint's contract. That is what separates an API that survives a CDN, a cache, a proxy chain, and a QA harness from one that quietly misbehaves in production.

## Q99: What is the correct use of 404 vs 410 vs 409, and what does each one communicate to clients?

**A:** 404 Not Found is the general "this URI does not map to a resource right now" — the client should not retry this URI without changing the request, and search engines de-index it. 410 Gone says the resource once existed and is permanently removed — a stronger signal than 404 for SEO (crawlers remove it from index more aggressively) and for clients (do not retry, the resource is deliberately gone). 409 Conflict says your request is syntactically fine but conflicts with current state — the client SHOULD fetch the current state, rebase, and retry (the protocol invites conflict resolution, not abandonment).

The interplay: 404 is absence (may return later, or may never have existed), 410 is permanent removal (the server knows it existed, it is gone by design), and 409 is a recoverable state mismatch. A 409 should include enough detail for the client to reconcile — the current ETag, the conflicting field, the existing resource's identifier — because 409 is an invitation to resolve. A 404 and 410 are both terminations, but 410 is an explicit one.

For API design: 404 for genuinely unknown paths; 410 for endpoints you deliberately dismantle (versioned APIs, removed features); 409 for business-rule conflicts (duplicate creation, optimistic-concurrency failure — though 412 Precondition Failed is more precise for ETag mismatches). The senior error taxonomy: 404 = "not here," 410 = "was here, gone forever," 409 = "is here, but you cannot do that to it right now."

## Q100: What is the historical evolution lesson of HTTP 1.0 → 3, and what does HTTP/3 keep, drop, and add?

**A:** The evolution teaches three lessons. First, connection reuse is non-negotiable: HTTP/1.1 made persistent connections the default, HTTP/2 collapsed N connections to one multiplexed connection, and HTTP/3 moved the transport to QUIC so that multiplexed streams have independent failure. The lesson is that connection setup cost dominates real-world latency more than any payload optimization.

Second, framing must be unambiguous: HTTP/1.1's text-based, Content-Length/chunked duality was a smuggling breeding ground; HTTP/2 replaced it with byte-exact binary frames; HTTP/3 preserves that rigor while adding QPACK to handle the lossy-multi-stream reality that HPACK could not. The lesson is that security lives in the framing — a protocol that lets intermediaries disagree about message boundaries is insecure by construction.

Third, semantics must be version-independent: HTTP methods, status codes, caching, and header semantics are the SAME across 1.1, 2, and 3. HTTP/2 added HPACK, multiplexing, and flow control but preserved the REST vocabulary; HTTP/3 swapped TCP for QUIC, added QPACK, and made 0-RTT and connection migration available, but the application layer did not change. The future lesson is clear: transport innovation must not break application contracts — greasing, version negotiation, and backward-compatible extensibility are the only ways a protocol survives at billion-endpoint scale.

What HTTP/3 keeps: all HTTP/1.1 semantics (methods, status, caching, headers, content negotiation), plus HTTP/2's framing discipline and HPACK-derived header compression. What it drops: TCP HOL blocking (solved by QUIC streams), kernel-space transport ownership (moved to userspace), and the connection-per-request model (one QUIC connection per origin). What it adds: 0-RTT session resumption, connection migration, built-in TLS 1.3, and the DATAGRAM extension for real-time data — all features that TCP could never offer. The architecture lesson: design the semantics to be immutable, and the transport to be replaceable.
