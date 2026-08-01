# HTTP Overview and Versions

> **TL;DR**: HTTP is the application-layer request/response protocol that carries the web (RFC 9110), and its five versions — 0.9, 1.0, 1.1, 2, 3 — each exist to solve a specific bottleneck of the previous one: from "read-only HTML" to multiplexed, encrypted, UDP-based transport.

## 1. Why Does This Exist?
The web needed a *simple, shared, stateless* way for clients (browsers) to fetch and manipulate resources from servers. HTTP exists because prior approaches (FTP-style session state, telnet, email protocols) were wrong-shaped for hypermedia: too stateful, too heavy, too chatty. HTTP's design goals — text-based, request/response, stateless, extensible via headers, resource-oriented via URLs — made it trivial to implement and scale, which is why it won and now carries ~everything. Each version exists because a *specific scaling bottleneck* appeared:
- **HTTP/0.9** (1991): bare-bones `GET /path` → HTML. No headers, no status, no POST.
- **HTTP/1.0** (RFC 1945): added methods, headers, status codes, and *one connection per request*.
- **HTTP/1.1** (RFC 2616/9110): persistent connections, pipelining, chunked encoding, host headers, caching — fixed the "connect per request" disaster.
- **HTTP/2** (RFC 7540): multiplexed streams over one TCP connection + header compression (HPACK) — killed head-of-line blocking at the request level.
- **HTTP/3** (RFC 9114): runs over **QUIC (UDP)** — removes TCP-level head-of-line blocking and cuts handshake latency.

## 2. How Does It Work?
The core pattern is unchanged across versions: a **client sends a request** (method + URI + headers + optional body), a **server sends a response** (status line + headers + optional body). Statelessness: each request is independent; state lives in the app (cookies/tokens). Differences are transport-layer:
- **1.0/1.1**: text framed over **TCP** (RFC 9293). One connection per request (1.0); connection reuse + pipelining (1.1). Headers are ASCII, delimited by `\r\n\r\n`; body length via `Content-Length` or `Transfer-Encoding: chunked`.
- **2**: binary framing layer splits messages into frames (HEADERS/DATA), multiplexed into **streams** over one TCP connection; header compression (HPACK); server push (deprecated). Always-over-TLS in practice.
- **3**: same semantics as 2, but frames ride **QUIC** (RFC 9000) over UDP, giving independent stream delivery, 0-RTT resumption, and integrated TLS 1.3.

## 3. When Is It Used?
- **HTTP/1.1**: still the baseline — simple APIs, small services, internal tools, legacy systems, anything not needing multiplexing. Most "HTTP" servers support it.
- **HTTP/2**: the web's default since ~2015 — every major browser uses h2 over TLS (ALPN "h2"); gRPC is HTTP/2-only (bidirectional streaming); CDNs (Cloudflare, Akamai) and cloud LBs (ALB) terminate h2.
- **HTTP/3**: adopted by Google (youtube.com, google.com), Cloudflare, Facebook/Meta, Apple, and increasingly the default on modern browsers/load balancers; best for high-latency/high-loss networks (mobile) and low-latency apps.
- **Version negotiation**: browsers and servers negotiate via ALPN (TLS extension) or `Upgrade: h2c` (h2 cleartext, rare).

## 4. Why Wasn't Another Approach Chosen?
- **Why not FTP-style session state?** Sessions require per-client server state → doesn't scale to millions of clients and harms caching/proxying. HTTP chose *statelessness* and pushes state into the app (cookies, tokens). This is the "end-to-end" ethos applied to the web.
- **Why text headers instead of binary from day one?** Debuggability (telnet/curl-readable) and simplicity. Downside: verbose (overhead) — which is *why* HTTP/2 introduced binary HPACK compression.
- **Why not just keep adding to HTTP/1.1?** HTTP/1.1's model (one request/response at a time per connection, pipelining broken in practice) capped throughput at ~6 connections per origin (browser limit). Multiplexing *required* a binary framing redesign → HTTP/2. And TCP's head-of-line blocking (one lost segment stalls every stream) *required* moving to UDP+QUIC → HTTP/3.
- **Why QUIC over UDP instead of new TCP?** TCP is entrenched in middleboxes (NAT, firewalls) and OS kernels; changing TCP on the wire breaks both. Encapsulating QUIC in UDP rides existing infrastructure while QUIC *reimplements* reliable, ordered delivery at the application layer — with crypto integrated and no kernel upgrade needed.

## 5. Intuition
HTTP is the **waiter** between your browser (customer) and the server (kitchen): the customer says "GET me the menu" (GET), "order a dish" (POST), "change my order" (PUT), "cancel" (DELETE), the waiter brings status ("200 OK" / "404 not found"). Versions are like different waiters:
- 1.0: a single waiter per request — you wait for that one order before you can order again (one connection per request).
- 1.1: a dedicated waiter at your table (persistent connection) who can also *predict* the next order (pipelining) — but only serves orders one at a time.
- 2: a whole wait staff (streams) over one person delivering everything concurrently — but if the *delivery boy* (TCP) drops a plate, the entire table's orders stall (HOL blocking).
- 3: a self-driven robot waiter (QUIC over UDP) that delivers each table's order independently — one dropped plate doesn't stall the others.

## 6. Real-World Analogy
**Library catalog request**: HTTP/0.9 = you walk up and ask "Do you have book X?" (no formalities). HTTP/1.0 = a librarian who stamps each request formally, but each question needs a *new trip to the desk*. HTTP/1.1 = the librarian stays at the desk, you can ask many questions and the librarian anticipates the next one — but answers come one at a time. HTTP/2 = one librarian handles all your questions in parallel through a fast internal sorting system (multiplexed streams) — but if the book elevator (TCP) jams, every question waits. HTTP/3 = a personal robot per question, each with its own tiny elevator (independent QUIC streams) — a jam in one doesn't block the rest.

## 7. Formal Definition
Hypertext Transfer Protocol (HTTP) is a stateless, application-layer, request/response protocol for distributed, collaborative, hypermedia information systems (RFC 9110, obsoleting RFC 7230/7231). It is built on a *generic message framework*: clients send requests, servers reply with responses, using *methods* (GET, POST, PUT, DELETE, PATCH…), *status codes* (1xx-5xx), and *header fields* (request/response/general/representation). HTTP/2 (RFC 7540/9113) adds a binary framing layer with multiplexed streams and HPACK compression over a single TCP/TLS connection. HTTP/3 (RFC 9114) runs the same semantics over QUIC (RFC 9000), a UDP-based transport with TLS 1.3 integrated, eliminating TCP HOL blocking.

## 8. Example
A version-by-version walk fetching `https://example.com/hello` (small, no TLS in example):
- **HTTP/1.1** (new connection each time): 
```
GET /hello HTTP/1.1\r\n
Host: example.com\r\n
Connection: keep-alive\r\n
Accept: */*\r\n\r\n
```
Response:
```
HTTP/1.1 200 OK\r\n
Content-Type: text/html; charset=utf-8\r\n
Content-Length: 13\r\n
Connection: keep-alive\r\n\r\n
Hello, World!
```
Two round trips total for one resource (SYN/ACK/TLS + request). To load 10 resources, the browser opens ~6 parallel connections (RFC/browser limits) — each a full TCP+TLS handshake.
- **HTTP/2**: one TLS/TCP connection for all 10 resources; 10 streams multiplexed; HPACK-compressed headers (the verbose `Host:`/`Accept:` text shrinks to a few bytes). Latency saved: no per-resource handshakes.
- **HTTP/3**: same multiplexing but each *stream* is delivered independently over QUIC. If one stream's packet is lost, only that stream's resource waits — no stalling of the other 9.

## 9. Internal Working
1. **URL parsing** → host, port, path, query. DNS resolves host → IP.
2. **Connection setup**: TCP (3-way handshake) + optionally TLS (1-RTT for TLS 1.3). For HTTP/3: QUIC handshake (1-RTT, or 0-RTT with a cached ticket).
3. **Request serialization** (1.1): request line `METHOD SP URI SP HTTP/x.y CRLF`, headers, `CRLF`, optional body. Body length via `Content-Length` or chunked.
4. **Server processing**: routing (virtual hosts by Host/`:authority`), auth, business logic, response building.
5. **Response framing**: status line `HTTP/x.y SP code SP reason CRLF`, headers, body. `Connection: keep-alive` (1.1 default) allows reuse.
6. **Version 2 framing**: message → HEADERS + DATA frames, stream IDs (odd = client-initiated, even = server), flow control per stream and per connection (window updates). HPACK: static/dynamic header tables (indexes replace repeated header strings).
7. **Version 3 framing**: same frame types carried in QUIC streams (each stream = separate reliability/ordering domain); QUIC integrates TLS 1.3 handshake and does its own congestion control (NewReno/CUBIC/BBR).
8. **Caching & intermediaries**: caches (browser, CDN) use headers (`Cache-Control`, `ETag`, `Last-Modified`); proxies rewrite; `Via` header logs hops. Each hop is a full HTTP conversation (end-to-end semantics preserved).

## 10. Time Complexity
- **Per-request latency (1.1, fresh connection)**: DNS (RTT) + TCP handshake (1 RTT) + TLS (1-2 RTT) + HTTP round trip (1 RTT) ≈ 3-5 RTT before first byte. HTTP/3 with 0-RTT ≈ 1 RTT.
- **Connection overhead**: HTTP/1.1 needs ~6 TCP+TLS connections per origin (browser limit) — each handshake is 2-3 RTT of wasted time; HTTP/2 multiplexes everything over one → connection amortization O(1) per origin.
- **Header overhead**: text headers ~500-800 B per request in 1.1; HPACK reduces repeat sends to ~a few bytes (dynamic table index). Binary framing is O(header size) constant.
- **Parallelism**: 1.1 = O(6) concurrent requests per origin (connections); 2 = O(streams, ~100+) per connection; 3 = same streams, but independent of packet loss (no TCP HOL).

## 11. Advantages
- **HTTP/1.1**: simple, debuggable (curl/telnet), ubiquitous, well-understood caching.
- **HTTP/2**: single connection → fewer handshakes; multiplexing → no per-request queueing; HPACK → less bandwidth; better TLS integration; server push (experimental); adopted by gRPC.
- **HTTP/3**: no TCP HOL blocking → better under loss; 0-RTT resumption; built-in TLS 1.3; better mobile performance (connection migration via QUIC connection IDs).
- **All**: stateless (scales), resource-based (cachable), extensible (headers, methods), version-negotiable (ALPN), works through proxies/CDNs.

## 12. Disadvantages
- **HTTP/1.1**: HOL blocking at request level, 6-connection cap, verbose headers, no compression built-in (except TLS-level), slow on high-latency.
- **HTTP/2**: TCP-level HOL blocking remains (one lost packet stalls all streams), CPU cost of HPACK, server-push complexity, harder debugging (binary frames), TCP+TLS+HPACK slow-start.
- **HTTP/3**: QUIC is young — new kernel/network stacks, UDP rate-limiting in some firewalls, higher CPU for crypto, NXDOMAIN of OS/network tooling, smaller ecosystem.
- **All**: text headers are wasteful; statelessness shifts complexity to apps; intermediaries (proxies) can corrupt/leak; no built-in auth (auth via headers/cookies is app-defined).

## 13. Interview Questions
1. **Q: What is HTTP?** A: A stateless, application-layer request/response protocol for hypermedia transfer — clients request resources by URL/method; servers respond with status + representation. Defined in RFC 9110.
2. **Q: Why is HTTP stateless and why does that matter?** A: Each request is independent — the server keeps no session memory. This makes servers scalable (any server can serve any request), cachable, and proxyable. State is pushed to the app (cookies, tokens).
3. **Q: What changed between HTTP/1.0 and 1.1?** A: 1.1 added persistent connections (keep-alive), pipelining, chunked transfer encoding, Host header (virtual hosting), and richer caching headers (Cache-Control, ETag). 1.0 opened a new connection per request.
4. **Q (tricky): Why is pipelining in HTTP/1.1 rarely used?** A: Pipelining requires responses in order (FIFO) — one slow response blocks all later ones (head-of-line blocking), and proxy bugs made it unsafe (RFC 7230 calls it problematic). HTTP/2's multiplexed streams replace it properly.
5. **Q: How does HTTP/2 multiplex requests?** A: A binary framing layer divides the message into HEADERS and DATA frames, tagged with a stream ID, all interleaved over *one* TCP connection. The receiver reassembles per stream. Flow control applies per stream and per connection.
6. **Q: What problem does HTTP/3 solve that HTTP/2 can't?** A: TCP head-of-line blocking: in HTTP/2, one lost TCP segment stalls *every* multiplexed stream until retransmission. HTTP/3 runs over QUIC (UDP), where each stream has its own reliability/ordering — a loss delays only that stream.
7. **Q: What is QUIC and why UDP?** A: QUIC (RFC 9000) is a transport protocol implementing reliable, ordered, encrypted delivery in *userspace over UDP*. UDP because TCP's wire format can't change (middleboxes/OS); QUIC owns the logic, so it can evolve without kernel upgrades.
8. **Q (production): Why does your browser open ~6 connections per origin in HTTP/1.1 but 1 in HTTP/2?** A: 1.1 supports one outstanding request per connection → browsers open ~6 parallel TCP+TLS connections to compensate. HTTP/2 multiplexes hundreds of streams over one connection — fewer handshakes, no per-request setup.
9. **Q: What is 0-RTT in HTTP/3?** A: A client that cached the server's TLS/QUIC parameters can send its first request immediately on connection resumption (0-RTT), saving a full RTT. Security trade-off: replayable requests (mitigations: replay windows, only safe methods).
10. **Q (tricky): Is HTTP/3 "just HTTP/2 over UDP"?** A: No — HTTP/3 removes stream multiplexing from the transport (each stream = independent QUIC stream), integrates TLS 1.3 in the handshake, changes flow control to per-stream, and reimplements reliability/ordering per stream. It's a redesigned transport + same semantics.
11. **Q: What is ALPN?** A: Application-Layer Protocol Negotiation — a TLS extension where client and server agree on the protocol (h2 vs h3 vs http/1.1) *during* the handshake. This is how browsers pick the best HTTP version securely.
12. **Q: What is HPACK?** A: Header compression for HTTP/2: a static table (common headers) + dynamic table (per-connection learned headers), encoding repeated header names/values as small integers. Cuts header bytes ~90%.
13. **Q (production): When would you *not* use HTTP/2?** A: For tiny internal APIs with simple clients (1.1 is simpler), for raw streaming where frame overhead hurts, behind legacy proxies lacking h2, or where connection longevity isn't a win. Practical answer: h2 is default on modern infra; h3 where loss/mobile matters.
14. **Q: What is the difference between a request line and a status line?** A: Request line = `METHOD URI VERSION`. Status line = `VERSION CODE REASON`. Both end with CRLF; headers follow until an empty line (the `\r\n\r\n` separator) before the body.
15. **Q: What does `Connection: keep-alive` do and why was it the default in 1.1?** A: It reuses the TCP connection for multiple requests, avoiding per-request handshake + slow-start. 1.1 made it the default; the header is largely vestigial now (used to signal "close": `Connection: close`).
16. **Q (scenario): A user says a page loads slowly. HTTP version could be the cause — how do you check?** A: Look at the browser/network tab (Protocol column: h1/h2/h3), `curl -v` (ALPN negotiated), or capture with tcpdump/Wireshark. If h1, latency multiplies per resource (6-connection cap, handshakes); upgrading to h2/h3 + keep-alive + CDN is the fix.
17. **Q: What is server push (HTTP/2) and why is it deprecated?** A: Server could preemptively send resources it predicted the client would request. Deprecated (RFC 9113): it wasted bandwidth (clients often cached), complicated flow control, and duplicates — modern alternatives are 103 Early Hints and preload links.
18. **Q: What happens when a server doesn't support the client's HTTP version?** A: They negotiate via ALPN (TLS) or `Upgrade` header; if neither side matches, the connection fails or falls back to HTTP/1.1. Proxies/CDNs handle version translation transparently (h3 at edge → h2/h1 to origin).

## 14. Follow-Up Questions
1. **Q: Why do large file downloads work fine on HTTP/1.1 but streaming suffers?** A: 1.1 delivers one big response fine; the pain is *many small concurrent requests* (web pages) because each needs a connection or queues. Multiplexing (h2) + independent streams (h3) fix the concurrent-small-request case.
2. **Q: What is "connection coalescing" in HTTP/2?** A: Using one connection for multiple origins that share a certificate/IP — reduces connections further. Requires matching certs (SAN) and IPs; a common CDN optimization.
3. **Q: How does QUIC handle connection migration (Wi-Fi → cellular)?** A: QUIC uses 64-bit connection IDs independent of IP:port. When the IP changes, packets carrying the same CID continue the session — TCP would have needed a new connection. A huge mobile win.
4. **Q: What is the "TCP fast open" analog and how does it differ from QUIC 0-RTT?** A: TFO sends data in the SYN (needs cached cookie) — but it's still TCP (HOL blocking, kernel-dependent). QUIC 0-RTT reuses TLS resumption + QUIC state, is cryptographically protected, and is userspace-deployable.
5. **Q: What is `Cache-Control: no-store` vs `private` vs `max-age`?** A: `no-store` = never cache; `private` = cache only in the user's browser (not shared/CDN); `max-age=N` = cache for N seconds. They're HTTP/1.1's cache-coherence machinery, orthogonal to HTTP version.

## 15. Coding Example
```bash
# Curl against each HTTP version (real-world usage)
$ curl -v --http1.1 https://example.com/       # HTTP/1.1
$ curl -v --http2    https://example.com/       # HTTP/2 (ALPN h2)
$ curl -v --http3    https://example.com/       # HTTP/3 (QUIC/UDP)
# output shows: * ALPN, offering h2, h3 ... ; * TLS handshake ... ; * using HTTP/3
```
```python
# Minimal HTTP/1.1 client via raw socket — shows the wire format
import socket

s = socket.create_connection(("example.com", 80), timeout=5)
request = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"        # tell server to close so we know body end
    "\r\n"
)
s.sendall(request.encode())
response = b""
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    response += chunk
s.close()
head, _, body = response.partition(b"\r\n\r\n")
print(head.decode())                # status line + headers
print("---BODY---")
print(body[:200])
```
```
# Observe the request/response pairs with tcpdump (HTTP/1.1, cleartext)
$ tcpdump -nn -i eth0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
# 22:41:00.001 IP 192.168.1.10.54321 > 93.184.216.34.80: Flags [P.], seq 1:74
#   GET / HTTP/1.1  (request line shown in payload)
# 22:41:00.180 IP 93.184.216.34.80 > 192.168.1.10.54321: Flags [P.], seq 1:201
#   HTTP/1.1 200 OK (status line + headers + body)
```

## 16. Industry Usage
- **Google**: was the primary driver of SPDY→HTTP/2 and gRPC (HTTP/2), and champions HTTP/3/QUIC (Chrome is h3-default, YouTube/Bard use QUIC heavily).
- **Cloudflare/Akamai**: terminate h2/h3 at the edge (hundreds of Gbps), translate to h1 toward origins; offer "0-RTT" for repeat visitors.
- **AWS**: ALB (Application Load Balancer) negotiates HTTP/1.1 and h2 (h3 recently), routes by host/path; CloudFront does h1/h2/h3 at edges.
- **Meta**: Facebook's mobile app + m.facebook.com heavily use HTTP/3 for mobile loss resistance; their "Grace" platform drives h3 adoption.
- **Every web stack**: Express/Spring/nginx — the same HTTP semantics across all versions; "HTTP/2 in front, HTTP/1.1 to legacy" is a common CDN pattern.

## 17. References
- RFC 9110 — HTTP Semantics (obsoletes 7230-7235): https://www.rfc-editor.org/rfc/rfc9110
- RFC 9112 — HTTP/1.1: https://www.rfc-editor.org/rfc/rfc9112
- RFC 9113 — HTTP/2: https://www.rfc-editor.org/rfc/rfc9113
- RFC 9114 — HTTP/3: https://www.rfc-editor.org/rfc/rfc9114
- RFC 9000 — QUIC: https://www.rfc-editor.org/rfc/rfc9000
- RFC 7540/7541 — HTTP/2 + HPACK (legacy), RFC 8446 — TLS 1.3.
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2 (HTTP).

## 18. Cheat Sheet
- HTTP = stateless request/response (RFC 9110); resource-addressed by URL.
- Versions: 0.9 (GET only) → 1.0 (methods/headers, one conn) → 1.1 (keep-alive, pipelining, Host) → 2 (binary multiplexing, HPACK, 1 conn) → 3 (QUIC/UDP, no HOL).
- Pipelining (1.1) FIFO HOL; HTTP/2 request-level HOL gone, TCP HOL remains; HTTP/3 kills TCP HOL.
- QUIC = TLS 1.3 + reliability in userspace over UDP; 0-RTT; connection migration via CIDs.
- ALPN negotiates h2/h3 over TLS.
- Body framed by Content-Length or chunked.
- Statelessness → cookies/tokens for state; caching via Cache-Control/ETag.

## 19. Quiz
1. HTTP/2's key win: a) text headers b) multiplexed streams over one connection c) UDP d) 6 connections → **b**
2. HTTP/3 runs over: a) TCP b) UDP c) SCTP d) raw IP → **b**
3. TCP HOL blocking means: a) headers too big b) one lost segment stalls all streams c) slow start d) connection limit → **b**
4. HTTP/1.1's `Host` header enables: a) chunking b) virtual hosting c) pipelining d) compression → **b**
5. 0-RTT belongs to: a) HTTP/1.1 b) HTTP/2 c) HTTP/3 resumption d) FTP → **c**
6. HPACK compresses: a) bodies b) headers c) URLs d) certificates → **b**
7. The `\r\n\r\n` separates: a) status and body b) headers and body c) method and URI d) chunk sizes → **b**
8. HTTP is: a) stateful b) stateless c) connection-oriented d) circuit-switched → **b**
9. ALPN negotiates: a) ports b) HTTP version over TLS c) cipher d) IP version → **b**
10. Server push was deprecated in: a) RFC 9113 (HTTP/2) b) RFC 9110 c) RFC 9000 d) never → **a**

## 20. Flashcards
- **Q: HTTP versions in order?** → **A:** 0.9, 1.0, 1.1, 2, 3.
- **Q: 1.1 → 2 main changes?** → **A:** Binary framing, multiplexed streams, HPACK, single connection.
- **Q: 2 → 3 main change?** → **A:** TCP→QUIC/UDP; no transport HOL; TLS 1.3; 0-RTT.
- **Q: What is the `\r\n\r\n`?** → **A:** Header/body separator in HTTP/1.x text messages.
- **Q: Why stateless?** → **A:** Scale, cache, proxy; state in cookies/tokens.
- **Q: What does ALPN do?** → **A:** Negotiates the HTTP version during TLS handshake.
- **Q: What is QUIC's big mobile win?** → **A:** Connection migration via connection IDs (Wi-Fi→cellular).

## 21. Revision
HTTP is the stateless request/response protocol of the web (RFC 9110). Version ladder: 0.9 (GET) → 1.0 (methods/headers, connection-per-request) → 1.1 (keep-alive, pipelining, Host, chunked) → 2 (binary frames, multiplexed streams, HPACK, one TLS connection) → 3 (QUIC over UDP: per-stream reliability, no TCP HOL, 0-RTT, TLS 1.3). HTTP/1.1 suffers request-level HOL + 6-connection cap; HTTP/2 removes that but keeps TCP HOL; HTTP/3 removes TCP HOL via independent QUIC streams. ALPN negotiates the version. Remember: h2 = one TCP conn, h3 = one UDP+QUIC conn.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain HTTP versions and their differences." | 2 How It Works / 13 Q&A |
| "Why does HTTP/2 use one connection?" | 8 Example / 13 Q&A |
| "What is TCP HOL blocking and how does HTTP/3 fix it?" | 4 Why Another Approach / 13 Q&A |
| "What is QUIC?" | 13 Q&A / 9 Internal Working |
| "Why is HTTP stateless?" | 4 Why Another Approach / 13 Q&A |
| "What is 0-RTT?" | 13 Q&A / Follow-Up |
| "How does a browser choose h2 vs h3?" | 13 Q&A / 9 Internal Working |
