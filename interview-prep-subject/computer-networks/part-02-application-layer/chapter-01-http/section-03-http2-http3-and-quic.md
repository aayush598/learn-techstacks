# HTTP/2, HTTP/3, and QUIC

> **TL;DR**: HTTP/2 (RFC 9113) multiplexes many requests over one TCP/TLS connection using binary frames + HPACK; HTTP/3 (RFC 9114) runs the same semantics over QUIC (RFC 9000) on UDP to kill TCP head-of-line blocking — they exist because web pages ballooned to 100+ requests while HTTP/1.1 allowed only ~6 serialized-per-connection.

## 1. Why Does This Exist?
Modern pages load 100+ resources (CSS, JS, images, fonts, API calls). HTTP/1.1 forces browsers to open ~6 connections per origin, each a fresh TCP+TLS handshake, with requests serialized per connection → wasted RTTs, idle bandwidth, and queuing. HTTP/2 (2015) exists to fix *request-level* inefficiency: one connection, multiplexed streams, compressed headers, low handshake cost. But TCP itself still causes **transport-level head-of-line blocking** — one lost segment stalls every stream sharing that connection. HTTP/3/QUIC (2018+) exists to remove that: per-stream reliability over UDP, integrated TLS 1.3, 0-RTT resumption, and connection migration. Both exist to make the web *faster under real-world latency and loss*.

## 2. How Does It Work?
**HTTP/2** — a binary framing layer between TLS/TCP and HTTP semantics:
- Messages are split into **frames**: HEADERS, DATA, RST_STREAM, SETTINGS, WINDOW_UPDATE, PING, PUSH_PROMISE.
- Frames are tagged with a **stream ID** (client-odd, server-even). Multiple streams interleave on one connection (multiplexing).
- **HPACK** compresses headers (static + dynamic tables → integers).
- **Flow control** per stream + per connection (window updates).
- **Server push** (now deprecated), stream priorities (deprecated), connection-level settings.
- Over one TCP connection, multiplexed; typically always over TLS (ALPN "h2").

**HTTP/3** — same semantics (methods, status, headers via **QPACK**), but:
- Runs over **QUIC**: each HTTP stream = an independent QUIC stream with its *own* ordering/reliability.
- QUIC (RFC 9000) = TLS 1.3 integrated (crypto handshake produces transport keys), packet numbers with proper ACK handling, **0-RTT**, **connection IDs** for migration.
- Frame types nearly identical to h2 (HEADERS/DATA/SETTINGS etc.), but carried inside QUIC stream data.
- No TCP, no TLS-over-TCP layering: QUIC *is* the secure transport.

## 3. When Is It Used?
- **HTTP/2**: the web default since ~2015-2018 — every major browser (h2 over TLS); gRPC (h2 mandatory for bidirectional streaming); CDNs (Cloudflare, Akamai), AWS ALB, nginx. Best where latency and connection count matter and loss is low.
- **HTTP/3**: the *new* default at Google (youtube.com, google.com), Meta (facebook/instagram apps), Cloudflare (default for all customers), Apple (Safari default), and Netflix. Best on high-loss mobile networks, long-distance connections, and latency-sensitive apps (video, chat, gaming).
- **Fallback**: clients/browsers attempt h3, then h2, then h1.1 (via ALPN); load balancers/gateways often terminate h2/h3 and speak h1.1 to origins.

## 4. Why Wasn't Another Approach Chosen?
- **Why not just "more HTTP/1.1 connections"?** Browsers cap ~6 per origin (RFC/implementation safety) to limit server load and NAT/firewall churn; more connections also waste handshake RTTs and TCP slow-start per connection. Multiplexing within one connection is strictly better.
- **Why binary frames instead of text lines?** Text requires delimiter scanning (`\r\n\r\n`), can't interleave (needs a length to multiplex), and is verbose. Binary framing = length-prefixed frames → safe interleaving and cheap parsing. Backward compatibility kept by *tunneling* h2 over TLS with ALPN (h1.1 clients never see it).
- **Why not fix TCP (new TCP, e.g., TCP-NO)?** TCP's wire format is frozen in OSes and middleboxes (NATs, firewalls, load balancers all parse TCP); you can't deploy a new TCP on the open Internet. **Encapsulating a new transport in UDP** (QUIC) rides existing infra while owning all transport logic in userspace — instantly deployable, evolvable, and encrypted by default.
- **Why integrate TLS 1.3 into QUIC instead of layering?** Layering TLS over TCP (h2) costs an extra RTT and lets middleboxes see unencrypted metadata. QUIC folds crypto into the handshake (1-RTT total, 0-RTT resumption) and encrypts more fields (packet numbers, most headers) — privacy + speed.

## 5. Intuition
HTTP/2 is a **supermarket with one checkout line** (one TCP connection) where each shopper (stream) moves at the same speed, but if *anyone* drops an item and has to fetch it again (packet loss), *everyone in line* waits (TCP HOL). HTTP/3/QUIC is the same supermarket where every shopper gets **their own checkout lane** (independent QUIC stream) — if one shopper drops something, only they wait. HTTP/1.1 is the *old* supermarket where you had to queue at 6 separate registers (6 connections) for your ~100 items, one item (request) at a time.

## 6. Real-World Analogy
**Highway tollbooths**: HTTP/1.1 = 6 tollbooths, each car (request) pays toll individually (handshake), cars queue *in single file* per booth (serialized). HTTP/2 = one modern toll plaza where all cars use E-ZPass and merge onto the highway as fast as they arrive (multiplexed streams on one road), but a single breakdown (one lost packet) brings the whole plaza to a crawl (TCP HOL). HTTP/3 = the same E-ZPass plaza but with a *separate dedicated lane per lane-destination* (per-stream QUIC): a breakdown in lane A doesn't stop lane B's cars. Each version is a faster toll plaza because the *traffic pattern* (many small web requests) changed.

## 7. Formal Definition
**HTTP/2** (RFC 9113) is a binary-framed protocol that enables *efficient, multiplexed* transfer of HTTP semantics over a single (typically TLS) connection. It introduces: a framing layer (frame types: HEADERS, DATA, SETTINGS, RST_STREAM, PUSH_PROMISE, WINDOW_UPDATE, PING), **stream multiplexing** (concurrent request/response streams, identified by stream ID), **HPACK** header compression, and explicit flow control. It does *not* change HTTP semantics (methods, status codes, headers, caching).
**HTTP/3** (RFC 9114) is the same HTTP semantics carried over **QUIC** (RFC 9000): a UDP-based, encrypted, multiplexed transport providing per-stream reliability/ordering, integrated TLS 1.3, 0-RTT resumption, connection IDs for migration, and its own congestion control. Header compression uses **QPACK** (RFC 9204). HTTP/3 eliminates TCP head-of-line blocking because streams are independent delivery units.

## 8. Example
Numbers: a page with 100 resources, RTT = 100 ms, all cache misses.
- **HTTP/1.1**: ~6 connections; each resource ≈ (TCP handshake 1 RTT + TLS 1 RTT) ÷ 6-connection amortization + serialization. Roughly: first resource 2-3 RTT, then pipelined-ish over 6 connections ≈ **3-5+ seconds** (and worse with slow-start).
- **HTTP/2**: one connection (1 TCP + 1 TLS RTT total); 100 streams concurrent; each resource ≈ 1 RTT (but the *first* stream also pays slow-start ramp). ≈ **200-400 ms** for all 100 (loss-free). 
- **HTTP/3**: same as h2 minus TLS RTT overlay + 0-RTT on revisit; with 2% loss, h2's *single* TCP connection stalls every stream on every loss (each loss = 1 RTT stall); h3's independent streams mean loss hits only the affected stream → **page load time largely unaffected by small loss**.

Loss example (the money shot): 2% loss, 100 streams, RTT 100 ms. In h2, the TCP connection drops ~2% of segments → every stream that shares the connection waits for retransmission (worst case n-losses × RTT serialized). In h3, each of the 100 streams loses ~2% of *its* packets; retransmission is per-stream, so other streams complete uninterrupted. Measured in production (Google/Cloudflare data): h3 cuts p95 page load ~10-30% on mobile.

## 9. Internal Working
1. **Negotiation**: ALPN in TLS ClientHello offers `h2`, `h3`; the server picks. (h3 needs QUIC first: the TLS handshake *is* the QUIC handshake via "QUIC Transport Parameters" in the ClientHello.)
2. **HTTP/2 connection setup**: TLS handshake → client sends SETTINGS, server SETTINGS → streams become usable. **Stream lifecycle**: `idle → open → half-closed → closed`; `RST_STREAM` cancels one stream; `GOAWAY` drains the connection.
3. **Multiplexing**: `HEADERS` + `DATA` frames for stream 1,2,3… interleaved on the wire; the receiver reassembles each stream's byte sequence. Priority (deprecated in RFC 9113) could hint ordering.
4. **HPACK**: static table (61 common headers), dynamic table (per-connection learned), Huffman coding. A repeated `:authority: example.com` becomes a 1-2 byte index.
5. **Flow control**: each stream has a send window; WINDOW_UPDATE replenishes; the connection has its own window. Prevents one stream starving others and prevents buffer overflow.
6. **QUIC internals (h3)**: 
   - Connection = 64-bit **connection ID** (not IP:port) → packets can migrate networks seamlessly.
   - **Streams**: bidirectional/unidirectional, each with independent byte ranges, ordering, ACKs.
   - **Packet numbers** are monotonic per connection (not per stream); ACKs use ranges → fast detection of loss.
   - **0-RTT**: client with cached config sends HTTP request in the first QUIC packet after ClientHello (replay risk mitigated).
   - **Congestion control**: NewReno/CUBIC/BBR (plug-in) — QUIC controls the algorithm in userspace, no kernel dependency.
7. **QPACK (h3 headers)**: like HPACK but must handle *stream interleaving* — the dynamic table is updated out-of-band on dedicated streams (unidirectional), with acknowledgement to avoid the "blocked on header reference" problem.

## 10. Time Complexity
- **Handshake**: h1.1 ≈ 3 RTT (TCP 1 + TLS 2) or 2 with TLS 1.3; h2 ≈ 2 RTT (TCP 1 + TLS 1.3); h3 ≈ 1 RTT (0-RTT on resumption). Per *origin* — h2/h3 amortize over all requests.
- **Requests over one connection**: h1.1 O(1) outstanding per connection (×6); h2 O(streams) ≈ 100-1000 concurrent; h3 same streams, independent of loss.
- **Loss penalty**: h2 = per-loss stall of *all* streams (O(1 × RTT) per loss); h3 = per-loss stall of *one* stream only (O(streams⁻¹ × RTT)).
- **Header compression**: HPACK/QPACK O(1) per header (table index) vs O(bytes) for text headers each time.

## 11. Advantages
- **HTTP/2**: one connection (fewer handshakes), multiplexing (no per-request queuing), HPACK (90% smaller headers), connection reuse across origins (coalescing), integrated TLS, gRPC support.
- **HTTP/3**: no TCP HOL (per-stream delivery), 0-RTT (faster revisits), connection migration (Wi-Fi↔cellular), integrated TLS 1.3 (fewer RTTs + more encryption of metadata), better behavior on lossy mobile, userspace evolvability, no kernel upgrade needed.
- **Both**: same HTTP semantics → drop-in for apps; web-scale performance gains measured at Google/Cloudflare/Meta.

## 12. Disadvantages
- **HTTP/2**: TCP HOL remains (the big one), HPACK CPU cost, server push deprecated (dead weight), binary debugging harder, middlebox interference with multiplexing (rarely), TFO not always available.
- **HTTP/3**: UDP may be rate-limited/blocked by some firewalls/legacy NATs, CPU overhead of crypto (higher than h2), ecosystem maturity (kernel/OS libraries, tools), QPACK complexity (blocked streams on dynamic-table references), some content security policies/older proxies don't speak it.
- **Both**: complexity vs h1.1 — small internal APIs may not need it; debugging requires h2/h3-aware tools.

## 13. Interview Questions
1. **Q: What problem does HTTP/2 solve?** A: HTTP/1.1's one-request-at-a-time model over ~6 connections — wasted handshakes, serialization, and idle bandwidth. HTTP/2 multiplexes many streams over one connection with binary framing and HPACK.
2. **Q: How does HTTP/2 multiplex?** A: Messages are split into frames (HEADERS/DATA) tagged with stream IDs; frames from many streams interleave on one TCP connection; the receiver reassembles per stream. Flow control is per-stream + per-connection.
3. **Q (tricky): Does HTTP/2 eliminate head-of-line blocking?** A: Request-level, yes (no FIFO queueing). Transport-level, **no** — it still uses TCP: one lost segment stalls *all* streams until retransmission. That's exactly what HTTP/3/QUIC fixes.
4. **Q: What is HPACK?** A: HTTP/2 header compression: static table (61 common headers) + dynamic table (per-connection) + Huffman; repeated headers become integer indexes. Cuts header bytes ~90% vs text h1.
5. **Q: What is QUIC and why does it use UDP?** A: QUIC is a secure, reliable, multiplexed transport implemented in userspace over UDP. UDP lets it ride all existing infrastructure (NATs/firewalls/OS) while owning transport logic — deployable and evolvable without kernel changes or TCP's frozen wire format.
6. **Q: How does QUIC remove TCP HOL blocking?** A: Each HTTP/3 stream is an *independent QUIC stream* with its own reliability and ordering. A lost packet affects only its stream's retransmission — other streams deliver data unaffected.
7. **Q: What is 0-RTT and its security trade-off?** A: On resumption (cached TLS/QUIC parameters), the client can send the first request immediately — 0 round trips before data. Risk: **replay** — an attacker can re-send a captured 0-RTT request (mitigated by replay windows, idempotent-method-only, server anti-replay).
8. **Q: How does QUIC handle connection migration?** A: Connections are identified by a 64-bit **connection ID**, not IP:port. When the client's IP changes (Wi-Fi→cellular), packets carrying the same CID continue the session seamlessly — TCP would force a new connection.
9. **Q (production): Why do you see h2 in production but h1.1 to origins?** A: Clients (browsers) speak h2/h3 to the edge; origins often run legacy stacks. Edge termination translates protocols (e.g., Cloudflare: h3/h2 at edge, h1.1/h2 to origin). It's a deployment reality, not a limitation.
10. **Q: What is QPACK and why is it harder than HPACK?** A: QPACK (h3) compresses headers but, unlike HPACK (h2), must account for out-of-order stream delivery — dynamic-table updates travel on dedicated unidirectional streams with acknowledgement so a stream doesn't block waiting for a table entry.
11. **Q (tricky): Can a client use HTTP/3 without QUIC support in the OS?** A: Yes — QUIC is userspace (like OpenSSL-based libraries: quiche, MsQuic, lsquic). The kernel only needs UDP. That's *why* QUIC won: no kernel/module upgrades required for deployment.
12. **Q: When would you prefer HTTP/2 over HTTP/3?** A: When loss is low and you need maximal ecosystem maturity (debugging, WAF/proxy compatibility, UDP-blocked environments). For lossy/long-distance/mobile, h3 wins. Modern answer: offer both, prefer h3.
13. **Q: What is server push and why was it deprecated?** A: HTTP/2 let servers send resources before the client asked. Deprecated (RFC 9113): it pushed resources clients already had (waste), fought flow control, and preload/103-Early-Hints do the job better.
14. **Q: How do flow control windows work in HTTP/2 vs QUIC?** A: h2: WINDOW_UPDATE per stream + per connection. QUIC: per stream + per connection too, but *packet-level* flow control also prevents buffer overflow — and windows are expressed in bytes of stream data with proper stream-level backpressure.
15. **Q (scenario): A mobile app is slow on 4G with 5% loss. Which protocol change helps most?** A: HTTP/3 — TCP HOL means every loss stalls all streams; QUIC isolates losses per stream. Also consider QUIC's 0-RTT and connection migration. This is exactly Meta/Google's measured mobile win.
16. **Q: What are the QUIC frame/stream types vs HTTP/3 frame types?** A: QUIC frames = STREAM, ACK, MAX_DATA, MAX_STREAM_DATA, CRYPTO, PING, CONNECTION_CLOSE. HTTP/3 frames ride inside QUIC STREAM frames: HEADERS, DATA, SETTINGS, GOAWAY, PRIORITY_UPDATE. Layered: QUIC is transport; HTTP/3 is the framing on top.

## 14. Follow-Up Questions
1. **Q: Why is the TLS handshake in QUIC "integrated"?** A: The QUIC handshake *is* TLS 1.3 — the ClientHello/ServerHello carry QUIC transport parameters, and both keys (crypto + transport) are derived from the same handshake. One round trip sets up encryption *and* the transport; h2 needed TLS then SETTINGS separately.
2. **Q: What does "packet number" vs "stream offset" mean in QUIC?** A: Packet numbers are per-connection, monotonic, for loss detection/ACKs. Stream offsets are per-stream, for reassembly. This separation is what lets QUIC ACK loss without stalling unrelated streams.
3. **Q: How does QUIC handle retransmission ambiguity (TCP's "spurious retransmit" problem)?** A: TCP retransmits a segment with the same seq; QUIC gives every *packet* a unique packet number and acknowledges *ranges* — no ambiguity about which transmission is being ACKed. Cleaner loss signals for congestion control (Reno→BBR).
4. **Q: What is "connection coalescing" in h2 vs "connection ID" in QUIC?** A: h2 coalescing = reuse one connection for multiple origins sharing IP+cert. QUIC CIDs additionally allow *migration* and *multipath* (a connection spanning multiple network paths). Different mechanisms for the same goal: fewer, more useful connections.
5. **Q: Does HTTP/3 break existing proxies/security tools?** A: It hides more from middleboxes (encrypted packet numbers/headers) — good for privacy, hard for DPI-based security/WAFs. Response: TLS-inspection proxies terminate QUIC at the edge (they hold the keys) — the industry's actual answer.

## 15. Coding Example
```bash
# Negotiate and test each protocol version with curl
$ curl -sS -o /dev/null -w "%{http_version}\n" https://www.google.com/     # likely "3"
$ curl -sS --http2 -o /dev/null -w "%{http_version}\n" https://www.google.com/   # 2
$ curl -sS --http1.1 -o /dev/null -w "%{http_version}\n" https://www.google.com/ # 1.1
```
```python
# aiohttp: make parallel requests — HTTP/2 multiplexing vs sequential
import asyncio, aiohttp

async def fetch_all(urls):
    conn = aiohttp.TCPConnector(limit=100)          # many concurrent streams
    async with aiohttp.ClientSession(connector=conn) as s:
        tasks = [s.get(u) for u in urls]
        return await asyncio.gather(*[t for t in []] )  # simplified: use gather with await

# Real multiplexing: same TCP/TLS connection, many streams (HTTP/2)
urls = [f"https://example.com/resource/{i}" for i in range(20)]
asyncio.run(fetch_all(urls))
```
```
# See the negotiated protocol in the TLS handshake (ALPN)
$ openssl s_client -connect www.google.com:443 -alpn 'h2,h3,http/1.1' -brief 2>/dev/null
# ALPN protocol: h2        <- what actually got negotiated
$ curl -v --http3 https://www.google.com/ 2>&1 | grep -i "using HTTP\|QUIC"
# * using HTTP/3
# * QUIC connection to www.google.com:443
```

## 16. Industry Usage
- **Google**: invented SPDY→HTTP/2 and QUIC; chrome.com/youtube.com/google.com are h3; internal RPCs use gRPC (h2). Their QUIC deployment is the reference case study.
- **Meta**: Facebook/Instagram apps default to HTTP/3 — internal data showed significant p95 latency + error-rate wins on mobile loss.
- **Cloudflare**: HTTP/3 for all customers by default; operates quiche (open-source QUIC); their edge terminates h2/h3 and measures sub-ms multiplexing benefits.
- **AWS**: ALB and CloudFront support h2/h3; CloudFront is the CDN path for h3; AWS's "Internet" CDN migrations push h3 adoption.
- **Apple**: Safari is h3-default; macOS/iOS QUIC (Network.framework) shipped before many vendors — consumer internet at scale runs on QUIC now.

## 17. References
- RFC 9113 — HTTP/2: https://www.rfc-editor.org/rfc/rfc9113
- RFC 9114 — HTTP/3: https://www.rfc-editor.org/rfc/rfc9114
- RFC 9000 — QUIC: https://www.rfc-editor.org/rfc/rfc9000
- RFC 9001 — QUIC + TLS 1.3, RFC 9204 — QPACK.
- RFC 8446 — TLS 1.3 (used by QUIC).
- Google QUIC design doc / Chromium QUIC — https://www.chromium.org/quic/
- Cloudflare "HTTP/3 explained" — https://blog.cloudflare.com/http3-the-past-present-and-future/

## 18. Cheat Sheet
- h2 = binary frames, multiplexed streams, HPACK, one TCP+TLS connection.
- h2 removes request-level HOL; TCP HOL remains.
- h3 = h2 semantics over QUIC (UDP); per-stream reliability → no TCP HOL.
- QUIC = TLS 1.3 integrated, 0-RTT, connection IDs (migration), userspace, evolvable.
- QPACK = header compression for h3 (streams may be out of order).
- ALPN negotiates h1.1/h2/h3.
- Server push deprecated → use preload / 103 Early Hints.
- 2% loss → h2 stalls everything; h3 isolates per stream (the mobile win).
- Packet numbers per connection (loss detection); stream offsets per stream (reassembly).

## 19. Quiz
1. HTTP/2 uses: a) one TCP connection b) 6 connections c) UDP d) no connection → **a**
2. HTTP/3 uses: a) TCP b) UDP+QUIC c) SCTP d) raw Ethernet → **b**
3. HTTP/2 HOL persists because of: a) header size b) TCP c) HPACK d) QPACK → **b**
4. Which gives 0-RTT on resumption? a) h1.1 b) h2 c) h3 d) none → **c**
5. HPACK belongs to: a) h3 b) h2 c) h1.1 d) QUIC → **b**
6. QUIC stream delivery: a) global ordering b) per-stream ordering c) no ordering d) random → **b**
7. Connection migration uses: a) IP b) connection ID c) port d) MAC → **b**
8. Server push was: a) improved b) deprecated c) mandatory d) for h1 → **b**
9. QUIC runs in: a) kernel b) userspace over UDP c) firmware d) hardware only → **b**
10. QPACK handles: a) TCP HOL b) out-of-order header references c) DNS d) TLS certs → **b**

## 20. Flashcards
- **Q: h2 vs h3 core difference?** → **A:** h2 over TCP (TCP HOL); h3 over QUIC/UDP (per-stream, no HOL).
- **Q: What is HPACK?** → **A:** h2 header compression (static+dynamic tables).
- **Q: Why UDP for QUIC?** → **A:** Ride existing middleboxes/OS; own transport in userspace; deployable/evolvable.
- **Q: What is 0-RTT?** → **A:** Send first request immediately on resumption (replay risk).
- **Q: Connection migration?** → **A:** Connection IDs (not IP) → seamless network changes.
- **Q: Server push status?** → **A:** Deprecated (RFC 9113); use preload/Early Hints.
- **Q: Which is better on 5% loss?** → **A:** h3 — loss hits only the affected stream.

## 21. Revision
HTTP/2 = binary framing + multiplexed streams + HPACK over one TCP/TLS connection — fixes request-level HOL but keeps TCP HOL (one loss stalls all streams). HTTP/3 = same semantics over QUIC (UDP): each stream independent reliability/ordering → no TCP HOL; integrated TLS 1.3, 0-RTT, connection-ID migration, userspace deployable. QPACK (h3 headers) handles out-of-order references. ALPN negotiates the version. Server push deprecated (use preload/103). For lossy mobile links, h3 is the win; for low-loss mature stacks, h2 still shines. Both drop-in over h1.1 semantics.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why HTTP/2 and what does it fix?" | 1 Why / 13 Q&A |
| "Does h2 eliminate HOL?" | 13 Q&A / 7 Formal Definition |
| "How does QUIC remove HOL?" | 9 Internal Working / 13 Q&A |
| "Why UDP for QUIC?" | 4 Why Another Approach / 13 Q&A |
| "0-RTT trade-offs?" | 13 Q&A / 9 Internal Working |
| "Connection migration?" | 13 Q&A / 14 Follow-Up |
| "Server push deprecation?" | 13 Q&A / 11 Advantages |
| "Mobile app slow on 4G — which protocol?" | 13 Q&A / 16 Industry Usage |
