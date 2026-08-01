# QUIC Protocol In Depth

> **TL;DR**: QUIC (RFC 9000) is a **UDP-based, TLS-1.3-encrypted, multiplexed, reliable, connection-migrating transport** that runs in user space — it kills TCP's head-of-line blocking with independent streams, merges the TCP+TLS handshake into 1 RTT (0-RTT for repeats), survives IP changes via connection IDs, and is the transport under HTTP/3 on every major browser.

## 1. Why Does This Exist?
By 2013, TCP was the bottleneck in four concrete ways: **(1) Head-of-line blocking** — one lost segment stalls *every* multiplexed stream (HTTP/2 had just made this worse); **(2) kernel lock-in** — deploying a new congestion-control/reliability algorithm meant kernel patches on millions of hosts and waiting on OS vendors; **(3) handshake latency** — TCP (1 RTT) + TLS (1-2 RTTs) = 2-3 RTTs before a single byte; **(4) connection migration** — an IP change (wifi→LTE) killed the connection because TCP's identity is the four-tuple. Middleboxes (NATs, firewalls, LBs) had also *frozen* TCP's evolution — new options get dropped or broken. QUIC solves all four at once by moving the transport to **user space over UDP**, adding **streams**, baking in **TLS 1.3**, and using **connection IDs** instead of tuples. Google shipped it in Chrome in 2013 (gQUIC), then standardized as RFC 9000 in 2021 — HTTP/3 (RFC 9114) rides it. It's the first new Internet transport in 40 years to actually deploy at scale.

## 2. How Does It Work?
- **Over UDP**: every QUIC packet is wrapped in a UDP datagram (dst port 443). Inside: a QUIC header (with Connection ID) + a sequence of **frames** (STREAM, ACK, CRYPTO, PING, NEW_CONNECTION_ID, CONNECTION_CLOSE...).
- **Connection ID**: a (usually random) 64-bit id that *identifies the connection*, not the IP tuple. Both ends negotiate IDs; the connection survives IP/port changes.
- **Streams**: the connection carries many **independent bidirectional/unidirectional byte streams**, each with its own seq/ACK/reliability. Streams can open/close dynamically (STREAM frames + FIN bit). This is the anti-HOL-blocking core.
- **Reliability (RFC 9002)**: packet-number-based (not byte-based) ACKs + retransmission; packet numbers never repeat (a retransmitted stream *frame* gets a *new* packet number). SACK-style ACK ranges. Loss detection like TCP's RTO/DUPACK but per-packet, in user space.
- **Congestion control**: RFC 9002 defines a TCP-like algorithm (NewReno/CUBIC) in *user space*; BBR and others plug in as libraries. No kernel involvement.
- **TLS 1.3 integrated**: QUIC is *always* encrypted — the TLS handshake runs in CRYPTO frames *inside* the connection. 1-RTT full handshake; 0-RTT with a resumption ticket (early data, replayable).
- **HTTP/3 (RFC 9114)**: HTTP maps onto QUIC — requests on streams, QPACK header compression (avoids the head-of-line-blocking header problem HTTP/2's HPACK had).
- **Frames do everything**: STREAM (data), ACK (ack ranges), CRYPTO (TLS), PING (keepalive), NEW_CONNECTION_ID (migration), PATH_CHALLENGE/PATH_RESPONSE (path validation), CONNECTION_CLOSE (graceful).

## 3. When Is It Used?
- **HTTP/3 everywhere**: Chrome, Edge, Safari, Firefox all enable HTTP/3 by default; Google, YouTube, Cloudflare, Akamai, Meta, X (Twitter), Apple — major properties serve it.
- **High-latency links**: the 1-RTT/0-RTT handshake saves 1-2 RTTs — 100-300 ms on mobile/satellite; 0-RTT repeat requests are a page-load win.
- **Multiplexing-heavy apps**: dashboards, real-time feeds, many parallel requests on one connection — where TCP's HOL blocking hurt HTTP/2.
- **Mobile clients**: connection migration keeps sockets alive across wifi↔LTE; NAT rebinding handled by Connection IDs.
- **Games, RPC, media**: gQUIC's follow-ons (WebTransport, QUIC RTP) use QUIC's streams for game/streaming transport.
- **Tunnels/VPNs (MASQUE)**: QUIC-based proxies and MASQUE tunneling ride the same connection for UDP/TCP/IP-in-QUIC.
- **Low-latency DDoS/CDN edge**: Cloudflare/Google use QUIC's 0-RTT + migration + stateless retry (address validation) as a first-class edge feature.

## 4. Why Wasn't Another Approach Chosen?
- **Why UDP and not a new IP protocol number?** Deployment reality: the Internet's middleboxes (NATs, firewalls, ALGs) were built for TCP/UDP. A new transport would be dropped/reordered by countless devices. UDP is *the* generic pass-through — senders can shove anything into the payload and the network forwards it. It's the classic "hiding a new protocol in an old one" trick (like PPP over Ethernet).
- **Why not extend TCP (TFO, Multipath TCP, TLS 1.3-in-TCP)?** TCP's evolution is frozen by (a) kernel vendors (years to ship), (b) middleboxes that strip/drop new options, and (c) byte-stream semantics that can't express independent streams. MPTCP exists but never deployed at scale for exactly these reasons. User-space over UDP sidesteps all three.
- **Why streams instead of one byte stream?** TCP's byte stream is *one* ordering domain: one loss blocks all data after it. Streaming (the model of SCTP, and now QUIC) gives independent ordering domains — the app (HTTP/3) gets per-request streams so a dropped request never stalls others. Streams are the fundamental *design* answer to HOL blocking.
- **Why TLS inside (not above)?** Putting TLS in the transport means the *entire* packet is encrypted (headers protected), connection IDs are cryptographically separated (privacy), and the handshake merges into one exchange — 1 RTT total instead of TCP+TLS's 2-3. "Transport + security co-design" was a deliberate, first-principles choice.
- **Why packet numbers that never repeat (vs TCP byte seq)?** TCP's byte-based seq conflates "retransmitted data" with "new data" (ambiguous ACKs, Karn's). QUIC numbers *packets*; a retransmit is a *new* packet — ACKs are unambiguous, RTT estimates clean, and loss recovery simpler.
- **Why Connection IDs instead of the four-tuple?** The tuple changes on migration/NAT; the connection must not. Connection IDs decouple connection identity from network path — the unique insight that makes migration trivial.

## 5. Intuition
Imagine a **multi-lane highway where every car (packet) can change lanes (retransmission) independently**, but instead of one giant convoy where a single broken-down truck stalls every car behind it (TCP), QUIC is a fleet of *independent convoys (streams)* on the same road: the truck stalls *its* convoy only, the others keep moving. And the fleet uses **license plates (connection IDs)** instead of "this car came from that street address" — so when the fleet moves to a new road (IP change), the same plates keep the delivery working. It's also *faster to get going*: the driver has a **pre-approved pass (0-RTT ticket)** so their first parcel ships in the same moment they arrive — no waiting at the gate. And everything is wrapped in a sealed envelope (TLS) the whole way — nobody on the road can read the cargo.

## 6. Real-World Analogy
**A courier company with delivery "streams"**: TCP is a single, serialized conveyor belt — if parcel 500 is lost, parcels 501-999 queue up behind it, *even in different orders* (head-of-line blocking). QUIC is a sorting facility with **independent lanes per customer**: a lost parcel on lane 7 doesn't delay lane 3's parcels at all (streams). Every parcel gets a **barcode (connection ID)** that names the *account*, not the street — so when a customer moves house (IP change), the parcels keep arriving under the same account (migration). The courier has a **fast-checkout card (0-RTT resumption)**: repeat customers drop their parcels at the door on the first visit of the day (0 RTT). And the whole sorting floor runs **encrypted** — even the courier company's own sorting rules are invisible to outsiders. TCP is the old single-belt warehouse; QUIC is the modern multi-lane, account-numbered, encrypted one.

## 7. Formal Definition
QUIC (RFC 9000, "A UDP-Based Multiplexed and Secure Transport") is a connection-oriented, encrypted, multiplexed transport running over UDP. Key structures: a **connection** identified by Connection IDs (both endpoints hold a set), carrying **bidirectional and unidirectional streams** (arbitrary count, each a byte stream with its own flow/reliability). Frames: STREAM (offset/length/fin), ACK (ack ranges over packet numbers), CRYPTO (TLS handshake), PING, NEW_CONNECTION_ID, PATH_CHALLENGE/PATH_RESPONSE, RESET_STREAM, CONNECTION_CLOSE. Handshake: TLS 1.3 (RFC 9001) via CRYPTO frames → 1-RTT full, 0-RTT early data with resumption. Loss recovery: RFC 9002 (packet-number ACKs, RTO/fast-recovery analogs). Congestion control: user-space, default NewReno/CUBIC-like. HTTP/3 (RFC 9114) + QPACK (RFC 9204) map HTTP. QUIC version negotiation via version field; the protocol is extensible via new frame/stream types.

## 8. Example
A QUIC handshake in Wireshark/tcpdump — what you actually see on the wire:
```
Client                               Server
  |  UDP 443, Initial packet          |
  |  CRYPTO frame: ClientHello        |   1. Client "Initial" (plaintext-ish, protected)
  |---------------------------------->|      carries DCID it chose, TLS CH
  |  UDP 443, Initial + Handshake     |
  |  CRYPTO: ServerHello + ...        |   2. Server's Initial + Handshake packets
  |<----------------------------------|      (ServerHello, cert, ...)
  |  UDP 443, Handshake + 1-RTT       |
  |  CRYPTO: Finished; STREAM: GET /  |   3. Client Finished + app data, 1-RTT
  |---------------------------------->|
  |  UDP 443, 1-RTT: ACK + STREAM     |   4. Server response — all encrypted
  |<----------------------------------|
Total: 1 RTT to deliver app data (vs TCP+TLS's 2-3). 0-RTT variant: step 1 already
carries an encrypted STREAM with the request using a cached session ticket.
```
On the wire (tcpdump): `UDP, length 1350` — from the outside it's *just UDP port 443*; the QUIC long header (bit 0x80) + DCID make it identifiable. Retransmission: a lost STREAM frame is re-sent in a *new* packet with a *new* packet number — so `tcpdump` shows `[Retransmission]` of *packet numbers*, not TCP-style `[R]` on the same seq.

## 9. Internal Working
1. **Packet layout**: long header (version-initial: DCID/SCID, version, type) or short header (1-RTT, DCID + packet number). Payload = frames, each tagged (type, length). Integrity: AEAD (TLS keys); Header Protection hides packet numbers/types.
2. **Handshake**: Initial packets (with a token/DCID) → server responds with its own Initial (SCID) + Handshake packets (ServerHello etc. in CRYPTO frames); keys advance (initial → handshake → 1-RTT application keys). 1-RTT full; 0-RTT: client uses a cached `early_data` ticket to encrypt its first STREAM/request.
3. **Streams**: a stream has an ID (bit 0: client/server, bit 1: bidi/unidi, high bits: stream number). Frames carry offset+length+fin; the receiver reassembles per-stream. Streams can be `RESET_STREAM`'d (abort that stream, keep the connection) — TCP can't abort a "stream."
4. **Reliability/loss recovery (RFC 9002)**: each packet has a number (monotonic per path). ACK frames carry ranges of received numbers. On loss (RTO or 3-spaced ACK detection), the *frames* are re-sent in new packets — *stream data* is retransmitted under a fresh number, so no ambiguity. RTT estimation, RTO (with jitter), and congestion control mirror TCP but live in the app.
5. **Congestion control**: same windows/slow-start/AIMD concepts (RFC 9002 + NewReno/CUBIC); because it's user-space, BBR/custom algorithms are drop-in libraries — no kernel.
6. **Connection migration**: when the IP changes, the client sends PATH_CHALLENGE/PATH_RESPONSE to validate the new path, then moves the connection (both sides keep the same Connection IDs or rotate with NEW_CONNECTION_ID). Packets in flight are retransmitted on the new path. NAT rebinding (new source port) is automatically tolerated.
7. **0-RTT security model**: early data is replayable (an attacker can resend the captured 0-RTT request) — servers must accept only idempotent/safe requests in 0-RTT, and use the retry token for address validation (anti-DDoS).
8. **QPACK (HTTP/3 header compression)**: avoids HTTP/2's HPACK HOL-blocking by compressing headers with stream-independent dynamic tables + explicit acknowledgment.
9. **Deployment reality**: works through most NATs/firewalls because it's UDP/443; some enterprise firewalls still block UDP → graceful HTTP/3 fallback to HTTP/2 via ALPN (browsers negotiate).

## 10. Time Complexity
- **Handshake**: 1 RTT full (vs TCP 1 + TLS 1.3 1 = 2, or TCP+TLS 1.2 = 3); 0 RTT with resumption. The *biggest* user-visible win — page-load latency on mobile drops by the handshake's RTTs.
- **HOL blocking**: eliminated across streams — a lost packet on stream A costs stream A only (~1 RTT), streams B-Z proceed. TCP costs all streams.
- **Per-packet work**: user-space means a context switch + copy per packet (UDP socket), so QUIC typically uses *more* CPU than kernel TCP — the "QUIC is CPU-expensive" caveat (mitigated by GSO/GRO offload, TSO-like segmentation).
- **State**: per-stream state per connection — a connection with 100 streams carries 100 × (stream state + buffers); multiplexed HTTP/3 amortizes it.
- **Loss recovery**: fast — packet-number ACKs + ranges make loss detection precise; RTO jitter tuning avoids spurious timeouts.
- **Scale**: user-space + UDP = the server does the demux; Cloudflare/Google serve millions of QUIC connections per node (they run it in production at 10s of Gbps).

## 11. Advantages
- **No head-of-line blocking**: streams isolate losses per stream — the killer feature vs TCP+HTTP/2.
- **1-RTT/0-RTT handshake**: merges transport + TLS; repeat connections send data in 0 RTT.
- **Always encrypted**: entire packet protected (headers, ACKs, streams) — privacy + tamper-evidence; TLS 1.3 built-in.
- **Connection migration**: IP/NAT changes don't kill the connection (mobile, multihoming).
- **User-space evolvability**: congestion control, loss recovery, and new features ship in apps/libraries — no kernel wait (this is *why* it's deployable).
- **Multiplexing done right**: arbitrary streams, stream-level resets, stream-level flow control — a richer transport API than TCP's single byte stream.
- **Forward-compatible**: version field + extensible frames/streams — future-proof vs TCP's frozen wire format.

## 12. Disadvantages
- **UDP/443 not always allowed**: some enterprise/captive networks drop UDP → fallback to HTTP/2 needed (graceful but adds complexity).
- **CPU overhead**: user-space + per-packet crypto + UDP demux costs 2-5× TCP's CPU; needs GSO/GRO offload for high throughput (a real edge-server consideration).
- **0-RTT replay risk**: early data is replayable → servers must restrict 0-RTT to safe/idempotent operations (a design constraint, not a bug, but a footgun).
- **Middlebox/NAT unpredictability**: NAT UDP timeouts (60-120 s idle) kill long-idle QUIC connections unless PING keepalives; some NATs rewrite ports (handled by migration logic, but it's extra machinery).
- **Complexity**: streams + frames + encryption + migration + user-space CC is a *lot* of moving parts; debugging requires QUIC-aware tools (Wireshark can decrypt, but it's far harder than TCP).
- **Younger than TCP**: deployment and hard-won edge cases are fewer; some networks misbehave (e.g., random UDP loss when they deprioritize 443).

## 13. Interview Questions
1. **Q: What is QUIC?** A: A UDP-based, TLS-1.3-encrypted, multiplexed, reliable transport (RFC 9000) with independent streams, connection-ID-based migration, 0-RTT, and user-space congestion control — the transport under HTTP/3.
2. **Q (tricky): Why did QUIC use UDP instead of a new IP protocol?** A: Deployment reality — new IP protocol numbers get dropped/mangled by NATs, firewalls, and middleboxes (and take years to standardize). UDP/443 is forwarded by *everyone*; QUIC is the "hide a new transport in a generic envelope" trick. Kernel lock-in is the other half: user-space means shipping algorithms without waiting for OS vendors.
3. **Q: What is head-of-line blocking and how does QUIC fix it?** A: TCP is one byte stream — a lost segment stalls *everything* after it, including other HTTP/2 streams sharing the connection. QUIC has independent streams, each with its own reliability — one stream's loss never blocks another. This is the #1 reason HTTP/3 exists.
4. **Q: What is 0-RTT?** A: With a cached session ticket (TLS 1.3 resumption), the client sends encrypted application data in the *first* flight — the request arrives in the same RTT as connection setup (vs 1 RTT for full QUIC, 2-3 for TCP+TLS). Caveat: replayable, so only safe/idempotent requests.
5. **Q (FAANG): How does connection migration work?** A: Connection identity = Connection IDs, not the four-tuple. On IP change (wifi→LTE), the client validates the new path with PATH_CHALLENGE/RESPONSE, then continues under the same (or rotated) CID. The tuple changes; the connection doesn't — TCP would just die.
6. **Q: How does QUIC do reliability differently from TCP?** A: Packet numbers are monotonic and *never repeat* — retransmitting a stream frame = a *new* packet with a new number. So ACKs are unambiguous (no Karn's ambiguity), RTT estimation is clean, and loss recovery is per-packet. TCP conflates byte seq with retransmission identity.
7. **Q (production): QUIC traffic on your edge box costs more CPU than TCP. Why?** A: User-space processing: UDP socket + per-packet AEAD encryption + demux (vs kernel TCP's hardware offloads). Mitigations: GSO/GRO (segment in hardware), dedicated cores, and careful buffer tuning. It's the price of transport-in-userspace.
8. **Q: What's the QUIC handshake cost?** A: 1 RTT full (TLS 1.3 inside the transport — CRYPTO frames), 0 RTT with resumption. Compare: TCP+TLS 1.2 = 3 RTTs, TCP+TLS 1.3 = 2 RTTs. The savings compound on high-RTT mobile/satellite links.
9. **Q (tricky): Why are QUIC headers encrypted?** A: Privacy (no visible seq/stream info to observers) + tamper-evidence + preventing network devices from interfering with transport semantics (some middleboxes hack TCP). Header Protection (a mask derived from the AEAD) hides packet numbers/types; Connection IDs remain visible for routing.
10. **Q: What is HTTP/3?** A: HTTP mapped onto QUIC (RFC 9114): requests/responses on streams, QPACK header compression (stream-independent, avoids HPACK HOL blocking), 0-RTT for idempotent GETs, connection migration for mobile. ALPN "h3" negotiates it; browsers fall back to h2.
11. **Q (FAANG): What's the difference between streams and connections?** A: A connection is the transport (CID, keys, path). Streams are independent byte channels *within* it (each with own flow control, reliability, FIN). One connection = many streams. TCP has one implicit stream per connection — the core architectural difference.
12. **Q: How does QUIC handle a reset of one stream?** A: RESET_STREAM + STOP_SENDING frames abort *that* stream (error code, final offset) while the connection and other streams continue — unlike TCP where a reset kills the whole connection.
13. **Q (production): Your NAT drops idle UDP. How do QUIC apps stay alive?** A: PING frames on a keepalive timer (receiver-transport-parameter `max_idle_timeout` governs server-side close; clients send PINGs well before NAT timeouts). This is exactly the "mobile app connection dies" classic — QUIC's answer is app-controlled keepalives.
14. **Q: How is QUIC's congestion control different?** A: Same concepts (slow start, cwnd, AIMD-ish, RFC 9002) but implemented in *user space* — libraries can drop in BBR/custom algorithms without kernel changes. That's a headline feature: the algorithm marketplace, not the kernel.
15. **Q (tricky): What's the "retry" mechanism in QUIC?** A: Server Retry: the server responds to an Initial with a Retry packet (token = address validation proof). The client re-sends with the token; the server verifies the client is at the claimed address — an anti-spoofing/anti-DDoS measure (like SYN cookies, but explicit in the protocol).
16. **Q: What is a Connection ID and why does it matter?** A: A routable (often random) id identifying the connection to both ends — decouples connection identity from IP/port tuple. Enables migration, NAT rebinding, and load-balancer routing (LBs hash on DCID). Privacy: clients can rotate CIDs per path to avoid tracking.
17. **Q (FAANG): How would you deploy QUIC in production behind a load balancer?** A: Terminate QUIC at the edge (CID-based routing, no tuple affinity), use it *only* if the client supports h3 (ALPN), keep HTTP/2 as fallback (some networks drop UDP), size CPU for user-space crypto, and enable GSO/GRO. This is exactly what Cloudflare/AWS do.

## 14. Follow-Up Questions
1. **Q: How does QUIC interact with NAT?** A: NAT maps UDP by tuple and has *idle timeouts* (~60-120 s) — long-idle QUIC dies unless keepalive PINGs run. NAT rebinding (port change) is handled by connection migration (the CID stays). Some enterprise NATs refuse UDP/443 wholesale → HTTP/3 simply doesn't connect → fallback to h2.
2. **Q: What is "multipath QUIC" and why do people want it?** A: MPQUIC (draft) uses *multiple* paths (wifi + LTE simultaneously) within one connection via multiple Connection IDs — load-balancing + resilience. It's TCP's Multipath TCP idea, but user-space and with migration already built in — much more deployable.
3. **Q (tricky): Why does HTTP/3 need QPACK when HTTP/2 has HPACK?** A: HPACK's dynamic table is *stateful across streams* — a header block loss delays all subsequent compressions (HOL in the *header* domain). QPACK decouples per-stream header blocks from a shared table with explicit acknowledgment — no cross-stream stalls. Same goal, stream-aware design.
4. **Q: What is WebTransport and how does it relate to QUIC?** A: A browser API exposing QUIC's streams to web apps (WebTransport over HTTP/3) — unreliable datagrams + reliable streams + connection migration, from JS. It's the "QUIC for apps," positioning UDP-like APIs in browsers with the reliability options.
5. **Q (FAANG): "Why isn't everything on QUIC yet?"** A: (a) UDP/443 not universal (enterprise/captive blocking); (b) CPU cost of user-space crypto vs kernel TCP offload; (c) legacy tooling (tcpdump/Wireshark need QUIC support; proxies/middleboxes expect TCP); (d) TCP is "good enough" for many; (e) QUIC's benefits are biggest for multiplexed/high-latency/mobile workloads — bulk file transfers see less. Adoption is real (a big % of web is HTTP/3) but not total.

## 15. Coding Example
```python
# QUIC in code: the modern way is to use a library (aioquic / quic-go / msquic)
# This example is a minimal HTTP/3 client using aioquic.
import asyncio
from aioquic.asyncio.client import connect
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import DataReceived, HeadersReceived

async def main():
    async with connect("example.com", 443, alpn_protocols=["h3"]) as conn:
        h3 = H3Connection(conn)
        stream_id = h3.create_requests_stream()          # a fresh QUIC stream
        h3.send_headers(stream_id, [(b":method", b"GET"), (b":scheme", b"https"),
                                     (b":authority", b"example.com"), (b":path", b"/")])
        conn.transmit()                                   # 0-RTT if session cached!
        while True:
            event = await conn.wait_for_event()
            if isinstance(event, HeadersReceived) or isinstance(event, DataReceived):
                print(event)                              # response headers + body
                break

asyncio.run(main())
```
```bash
# See QUIC on the wire — it's UDP/443 with recognizable packet types
$ sudo tcpdump -i eth0 udp port 443 -nn -v | head
#   IP 10.0.0.5.53000 > 1.2.3.4.443: UDP, length 1350
#   ... QUIC (long header, type Initial, DCID ...) / QUIC (short header)
$ tshark -i eth0 udp port 443 -Y quic | head          # frames, streams, ACKs
# Check HTTP/3 negotiation:
$ curl --http3-only -sv https://www.cloudflare.com -o /dev/null 2>&1 | grep -i h3
#   * using HTTP/3
```

## 16. Industry Usage
- **Browsers & OSes**: Chrome/Edge/Safari/Firefox enable HTTP/3 by default; Windows/macOS/iOS/Android ship QUIC stacks (msquic, NSS, quiche-based). "QUIC is at web scale" is no longer a claim, it's measured traffic.
- **Big web platforms**: Google (search, YouTube, Gmail), Meta, X, Apple, Cloudflare, Akamai, AWS (CloudFront/ALB), Fastly — HTTP/3 on major properties; Cloudflare alone serves a large share of global web traffic over QUIC.
- **Video/streaming**: YouTube/Netflix-over-Cloudflare use HTTP/3 for low-latency start + resilience; WebRTC/QUIC experiments for live.
- **Edge networking**: Cloudflare's "QUIC 1.0" infra, Google's gQUIC→RFC transition, and MASQUE (QUIC-based proxy/tunnel) for privacy browsing.
- **Datacenter/cloud**: Envoy/HAProxy add h3 listeners; service meshes prototype QUIC for RPC; AWS/GCP/Cloudflare route on Connection IDs at L4 — QUIC is the transport of choice for *new* high-multiplex latency-sensitive workloads.

## 17. References
- RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport: https://www.rfc-editor.org/rfc/rfc9000
- RFC 9001 — Using TLS to Secure QUIC: https://www.rfc-editor.org/rfc/rfc9001
- RFC 9002 — QUIC Loss Detection and Congestion Control: https://www.rfc-editor.org/rfc/rfc9002
- RFC 9114 — HTTP/3: https://www.rfc-editor.org/rfc/rfc9114
- RFC 9204 — QPACK: https://www.rfc-editor.org/rfc/rfc9204
- RFC 9221 — QUIC Datagrams (unreliable streams): https://www.rfc-editor.org/rfc/rfc9221
- Langley et al., "The QUIC Transport Protocol: Design and Internet-Scale Deployment" (SIGCOMM 2017).

## 18. Cheat Sheet
- QUIC = UDP + TLS 1.3 + streams + connection IDs + user-space CC (RFC 9000-9002).
- Streams: independent byte channels; per-stream reliability/FIN/reset → no HOL blocking.
- Handshake: 1 RTT full, 0 RTT with resumption ticket (replayable → idempotent only).
- Connection ID: identity, not tuple → migration (wifi↔LTE) + NAT rebinding survive.
- Packets: long/short header + frames (STREAM, ACK, CRYPTO, PING, PATH_CHALLENGE...).
- Reliability: monotonic packet numbers never repeat; retransmit = new packet → clean ACKs.
- Congestion control: user-space (RFC 9002, CUBIC/BBR drop-in).
- HTTP/3 (RFC 9114) + QPACK (RFC 9204); ALPN h3; fallback to h2 when UDP blocked.
- CPU cost > TCP (user-space crypto) → GSO/GRO; NAT UDP idle timeouts → PING keepalives.
- Server Retry = address validation (anti-DDoS, like SYN cookies).

## 19. Quiz
1. QUIC runs over: a) TCP b) UDP c) a new IP protocol d) SCTP → **b**
2. The feature that kills HOL blocking: a) 0-RTT b) streams c) CIDs d) TLS → **b**
3. Connection identity in QUIC: a) four-tuple b) Connection ID c) IP d) port → **b**
4. 0-RTT sends: a) only PING b) encrypted app data c) SYNs d) nothing → **b**
5. Retransmitted QUIC stream data gets: a) same packet number b) new packet number c) new CID d) no number → **b**
6. Full QUIC handshake costs: a) 0 RTT b) 1 RTT c) 2 RTTs d) 3 RTTs → **b**
7. 0-RTT is safe for: a) any request b) idempotent requests c) writes d) auth → **b**
8. Which fixes TCP's HOL blocking? a) HTTP/2 b) SACK c) QUIC streams d) TFO → **c**
9. QUIC's crypto: a) optional b) always on (TLS 1.3) c) app-level d) none → **b**
10. ALPN protocol for HTTP/3: a) h2 b) h3 c) http/3 d) quic → **b**

## 20. Flashcards
- **Q: What is QUIC?** → **A:** UDP + TLS 1.3 + multiplexed streams + CIDs + user-space CC.
- **Q: How does it fix HOL blocking?** → **A:** independent streams, per-stream reliability.
- **Q: 0-RTT?** → **A:** cached ticket → encrypted app data in first flight; replayable.
- **Q: Connection ID?** → **A:** connection identity ≠ tuple → migration/NAT survive.
- **Q: Why UDP?** → **A:** middlebox pass-through + no kernel lock-in.
- **Q: Reliability difference?** → **A:** monotonic packet numbers; retransmit = new packet.
- **Q: HTTP/3 = ?** → **A:** HTTP on QUIC streams + QPACK headers; ALPN h3.
- **Q: Big caveats?** → **A:** CPU cost, UDP/443 blocking, 0-RTT replay.

## 21. Revision
QUIC (RFC 9000): user-space transport over UDP — streams kill HOL blocking, CIDs enable migration, TLS 1.3 is built-in (1-RTT full, 0-RTT repeats, replayable→idempotent), packet numbers never repeat (clean ACKs), CC in user space (RFC 9002). HTTP/3 (RFC 9114) + QPACK on top; ALPN h3 with h2 fallback. Deployment wins on multiplexing, mobile latency, and RTT savings; costs are CPU (GSO/GRO), UDP/443 filtering, NAT idle timeouts (PINGs). Edge infra (Cloudflare/Google/AWS) routes on CIDs.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why did Google build QUIC on UDP?" | 13 Q&A / 4 Why Not Another Approach |
| "What is HOL blocking and the fix?" | 13 Q&A / 5 Intuition |
| "What is 0-RTT and its caveat?" | 13 Q&A / 8 Example |
| "How does connection migration work?" | 13 Q&A / 9 Internal Working |
| "How is QUIC reliability different?" | 13 Q&A / 10 Time Complexity |
| "Why is QUIC CPU-expensive?" | 13 Q&A / 12 Disadvantages |
| "What is HTTP/3 / QPACK?" | 13 Q&A / 14 Follow-Up |
| "Why isn't everything on QUIC?" | 13 Q&A / 15 Coding |
| "How do CDNs deploy QUIC?" | 16 Industry Usage / 13 Q&A |
