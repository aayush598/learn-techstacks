# SCTP and Other Transport Protocols

> **TL;DR**: Beyond TCP/UDP sits a transport zoo — **SCTP** (RFC 9260: message-oriented, multihomed, multi-streamed, with partial reliability), **DCCP** (congestion-controlled but unreliable), plus **TLS/DTLS**, **RTP/RTCP**, **QUIC's unreliable datagrams**, and the protocols-in-a-hurry — each trading a specific set of guarantees (ordering, reliability, multihoming, message boundaries) to fit a niche that TCP/UDP can't serve.

## 1. Why Does This Exist?
TCP and UDP aren't the only possible trade-offs: TCP gives you a *reliable, ordered byte stream with a single path*; UDP gives you *unreliable datagrams with no congestion control*. But real workloads want other points in the design space:
- **Telephony/SIP** wants *message boundaries* (not a byte stream), *reliability*, *ordering*, *multihoming* (two network paths), and *protection against one stream blocking another* — TCP can't multihome, and its byte-stream model mangles signaling messages.
- **Voice/video** wants *congestion control without reliability* — DCCP's exact sweet spot.
- **Multihomed/high-availability systems** want connection survival across NIC/link failure — SCTP's multihoming.
- **Transport-level experiments** want deployment *without* kernel changes — hence DTLS over UDP, and QUIC's datagram extension.
Each protocol is the answer to "which combination of (reliability, ordering, boundaries, multihoming, congestion control, security) fits my workload?" — and why engineers keep designing new ones rather than forcing everything through TCP/UDP.

## 2. How Does It Work?
- **SCTP** (Stream Control Transmission Protocol, RFC 9260): a **message-oriented, reliable, connection-oriented** transport. A SCTP association (connection) carries **multiple streams** (each with its own ordered delivery — no inter-stream head-of-line blocking); supports **multihoming** (each end has a set of IP addresses; the association picks primary + fallback paths); uses a 4-way handshake (INIT/INIT-ACK/COOKIE-ECHO/COOKIE-ACK — with a **cookie** to resist SYN-flood-like attacks); **partial reliability** (PR-SCTP) can expire messages; heartbeat + SACK keep paths alive; message chunks (DATA, SACK, HEARTBEAT, SHUTDOWN...).
- **DCCP** (Datagram Congestion Control Protocol, RFC 4340): unreliable datagrams **with congestion control** — you get UDP's latency + the *network fairness* of TCP (CCID 2 ≈ Reno, CCID 3 ≈ TFRC). Connection-oriented handshake, but no reliability.
- **DTLS** (RFC 6347): TLS *over datagrams* (UDP) — the "UDP with encryption" for SIP/RTP/CoAP.
- **RTP/RTCP** (RFC 3550): the real-time media pair — RTP carries sequenced, timestamped media; RTCP reports loss/jitter for adaptation.
- **QUIC Datagrams** (RFC 9221): QUIC now has unreliable datagram frames (streams + datagrams in one connection).
- **TLS**: the security layer over TCP (its *own* protocol family — see part-02 TLS section).

## 3. When Is It Used?
- **SCTP**: telecom signaling (SIP/SIGTRAN over SCTP), 5G core (NGAP/NAS over SCTP), load balancers that want multihoming, and some DB/storage replication for multi-path survival. Also the carrier for **WebRTC's SCTP data channels** (via DTLS, the browser's only SCTP deployment).
- **DCCP**: niche — streaming video over lossy networks where TCP fairness is required without TCP latency (research + early VoIP experiments; not widespread in production).
- **DTLS**: WebRTC (SRTP+DTLS for media + SCTP-over-DTLS for data), CoAP+DTLS (IoT), SIP with SRTP, VPNs (WireGuard is a separate design, but DTLS fills the "TLS over UDP" slot).
- **RTP/RTCP**: every VoIP/video call (Zoom, Meet, Teams, Twilio) — the media workhorse over UDP.
- **QUIC datagrams**: WebTransport, games, live metrics — reliable streams *and* unreliable datagrams over one authenticated connection.
- **When TCP isn't deployable**: multicast (UDP only), broadcast, low-latency real-time, and any kernel-change-averse deployment (user-space stacks over UDP).

## 4. Why Wasn't Another Approach Chosen?
- **Why SCTP over TCP for signaling?** TCP is a *byte stream* — a signaling protocol must frame messages (and one corrupted message can desync the parser), has no multihoming (a NIC failure kills a TCP connection), and no multiple streams (a slow signaling stream can block others). SCTP's message boundaries + streams + multihoming map exactly onto carrier telephony's needs. TCP can't do any of those three.
- **Why a 4-way handshake in SCTP (vs TCP's 3)?** The extra COOKIE-ECHO/COOKIE-ACK exchanges a *cookie*: the server sends state (in the INIT-ACK) *without allocating resources*, and only after the client echoes the cookie does it commit — an anti-SYN-flood design baked into the protocol, so SCTP needs no SYN cookies as an afterthought.
- **Why DCCP instead of UDP+your-own-CC?** DCCP standardizes the congestion control (CCID 2/3) so streams are *TCP-friendly by default* and interoperable — your custom UDP+CC is bespoke, unproven, and un-fair to TCP. DCCP provides the CC *in the transport* without the reliability.
- **Why DTLS and not just TCP+TLS for real-time?** TCP's retransmission + ordering adds latency that real-time media can't afford; but unencrypted UDP is unacceptable. DTLS = "TLS semantics over datagrams" — you keep UDP's timing *and* get TLS's authentication/privacy. Encryption must match the transport's semantics (record numbering that tolerates loss/reorder).
- **Why RTP over UDP rather than SCTP?** RTP needs *minimal latency* and *app-level loss tolerance* (FEC/adaptive bitrate); SCTP's reliability (even partial) is overkill, and its message framing doesn't help media. RTP + RTCP keeps the transport raw and the *control* explicit.
- **Why QUIC added datagrams instead of using a separate UDP socket?** A second socket breaks multiplexing, encryption, and migration; datagram frames *inside* QUIC inherit the connection's auth, congestion control, and migration — one connection for both reliable streams and best-effort datagrams.

## 5. Intuition
SCTP is **a courier with multiple trucks and multiple labeled crates**: it has several trucks (multihomed paths) so if one breaks down it reroutes without losing the order; and it packs *your* cargo in separate, labeled crates (streams) so one crate's delay doesn't hold the others. It also hand-delivers a signed cookie before trusting a new client (4-way handshake). DCCP is **a UDP courier with a speed governor**: it still throws things fast and doesn't guarantee arrival (like UDP), but it *agrees to follow traffic laws* (congestion control) so it doesn't clog the roads or unfairly hog them from TCP. DTLS is **a sealed postcard service**: postcards (datagrams) with a tamper-proof seal (encryption), even though the postal service still drops and reorders them. RTP/RTCP is **a radio station with a studio feedback loop**: RTP is the broadcast (timestamped, sequenced media), RTCP is the listener phone-in that reports "we lost 3% — raise/lower the quality."

## 6. Real-World Analogy
**A freight logistics network (SCTP)** vs **a single-truck company (TCP)**: The single-truck company loses the whole shipment if its one truck breaks down on the only route (TCP: no multihoming) and delivers a literal *heap* of cargo that the customer must sort (byte stream). The freight network sends the same shipment across *two routes* simultaneously (multihoming), packs each customer's goods in clearly labeled containers (streams — one container's delay doesn't block another's), and requires a signed proof-of-identity before accepting a shipment from a new customer (cookie handshake). **DCCP** is a mail courier who refuses to guarantee delivery but *always obeys speed limits and traffic lights* — cheap and fast, yet fair to other road users (congestion control without reliability). **RTP/RTCP** is the live TV truck: the picture (RTP) streams out in real time with a timecode; the control room gets a laggy stats feed (RTCP) telling them if the audience is seeing enough (loss → adjust bitrate).

## 7. Formal Definition
**SCTP** (RFC 9260): a reliable, connection-oriented, *message-oriented* transport. An **association** (not connection) between two endpoints, each identified by a set of transport addresses (multihoming). Carries **multiple streams** — each a sequenced sequence of messages; delivery order guaranteed *within* a stream, not across streams. Handshake: INIT → INIT-ACK (with cookie + state) → COOKIE-ECHO → COOKIE-ACK (4-way, cookie-based DoS protection). Reliability via DATA chunks + SACK; path supervision via HEARTBEAT; **PR-SCTP** (RFC 3758) adds partial reliability (message expiry). **DCCP** (RFC 4340): connection-oriented, unreliable datagram transport with congestion control — CCID 2 (TCP-like, RFC 4341) and CCID 3 (TFRC, RFC 4342); no retransmission, no ordering. **DTLS** (RFC 6347): TLS record protocol adapted to datagrams (record-number replay window, retransmission of handshake messages, stateless cookies). **RTP/RTCP** (RFC 3550): RTP provides sequenced, timestamped media payloads; RTCP reports reception statistics for adaptation.

## 8. Example
SCTP association setup (the 4-way handshake on the wire):
```
Client (1.2.3.4)                     Server (5.6.7.8, 9.10.11.12)
  |  INIT (incl. both its IPs +     |
  |  4 streams + cookie)            |   1. Client proposes its multihomed addresses
  |--------------------------------->|
  |  INIT-ACK (with STATE COOKIE)   |   2. Server sends its addresses + a state
  |<---------------------------------|      cookie (no resource allocated yet)
  |  COOKIE-ECHO (echo the cookie)  |   3. Client proves it's reachable at claimed addr
  |--------------------------------->|
  |  COOKIE-ACK                     |   4. Server commits resources -> association up
  |<---------------------------------|
```
Then data flows on *streams* (e.g., stream 0 = control, stream 1 = media). If the 1.2.3.4 path dies, the association *continues* via 9.10.11.12 (multihoming) — SACKs and HEARTBEATs report path health. TCP, by contrast, has one address pair and one byte stream — the association model is the entire point.

## 9. Internal Working
1. **SCTP association**: negotiated during INIT (number of streams, chunk types, PR-SCTP support). Each endpoint maintains a "transport address set"; one primary path + alternates; HEARTBEAT (lightweight chunks) tracks path liveness; on failure the sender switches streams' primary.
2. **SCTP streams**: DATA chunks carry a Stream ID + Stream Sequence Number. The receiver reassembles *per stream* — message boundaries preserved (a message may span chunks via FSN). Ordering is per-stream (unordered delivery option exists); a lost message on stream 0 doesn't block stream 1 — the anti-HOL-blocking design (decades before QUIC).
3. **SCTP reliability**: cumulative TSN (transmission sequence number) ACKs + gap reports (like SACK); retransmission to the *alternate* path on failure; PR-SCTP lets a sender mark a message "drop after X" (expired by time/retries) — the partial-reliability extension.
4. **SCTP cookie mechanism**: the INIT-ACK carries the *entire server state* encrypted as a cookie; the server stores nothing until COOKIE-ECHO — so a flood of INITs costs the server almost nothing (the anti-DoS design that TCP achieves only with SYN cookies as an afterthought).
5. **DCCP**: handshake (DCCP-Request/Response/Reset/Ack) negotiates the CCID; data packets carry sequence numbers (for the CC algorithm, not reliability) and optionally checksums; the chosen CCID (2 ≈ Reno window, 3 ≈ TFRC rate-based) paces sending; no retransmission — a lost DCCP packet is simply lost.
6. **DTLS**: record layer like TLS but with a *replay window* (antireplay bitmap) instead of exact record sequencing; the handshake retransmits its own messages (timeout-based) because datagrams drop; a stateless *HelloVerifyRequest* cookie mitigates amplification/DoS.
7. **RTP**: each packet = header (version, PT, sequence, timestamp, SSRC) + payload; timestamp drives playback; sequence drives jitter/loss detection; RTCP Sender/Receiver Reports (SR/RR) carry lost/fraction statistics — the basis of adaptive bitrate.
8. **QUIC datagrams (RFC 9221)**: a DATAGRAM frame marked unreliable — delivered best-effort *within* the QUIC connection (authenticated, congestion-controlled, migratable); coexists with reliable streams on the same connection.

## 10. Time Complexity
- **SCTP**: per-message O(1) framing + per-stream reassembly; multihoming adds O(paths) state. The 4-way handshake costs ~2 RTTs (vs TCP's 1) — the price of cookie-based DoS resistance. Stream independence removes cross-stream blocking *by construction* (O(1) per stream vs O(window) for TCP HOL).
- **DCCP**: CCID 2 window math ≈ TCP (O(1)/ACK); CCID 3 TFRC is rate-based (O(1) periodic). Zero retransmission → no RTO/timer machinery.
- **DTLS**: handshake retransmission timers (like TCP's but for the security layer); record processing ≈ TLS + replay window.
- **RTP/RTCP**: O(1) per packet; RTCP bandwidth is ~5% of the session by design — a *built-in* cost ceiling.
- **Deployment cost**: SCTP/DCCP are rare in user space; mainstream OSes have kernel SCTP (Linux) but not everywhere — the "why it hasn't replaced TCP" cost is deployment, not algorithm.

## 11. Advantages
- **SCTP**: message boundaries (no parser framing), multihoming (path-failure survival), multi-streaming (no cross-stream HOL blocking), cookie-based DoS resistance, partial reliability option — the most *feature-complete* transport that ever standardized.
- **DCCP**: UDP latency + TCP fairness — congestion control *without* the reliability overhead; ideal for streaming/loss-tolerant bulk.
- **DTLS**: TLS-grade security over UDP — enables encrypted real-time without TCP latency.
- **RTP/RTCP**: the de-facto real-time standard — timestamped, sequenced, feedback-driven adaptation; universally implemented (telephony, video, broadcast).
- **QUIC datagrams**: best-effort + reliable in one authenticated, migratable connection.
- **The principle**: choosing the *right guarantee set* per workload beats forcing everything through TCP/UDP — the zoo is a design menu.

## 12. Disadvantages
- **SCTP**: 2-RTT handshake, larger header/chunk overhead, OS/device support is uneven (Windows only via kernel-mode, no NAT traversal built-in — it needs special ALGs; middleboxes routinely block unknown protocols), and the byte-stream world (HTTP/TLS ecosystems) doesn't use it. "The best transport nobody deployed."
- **DCCP**: minimal deployment (few OSes, fewer apps), and the fair-CC guarantee only matters if everyone uses it — it never got the ecosystem push.
- **DTLS**: handshake over lossy UDP can be slow (timeout retransmits); replay window is a fixed size; cookie exchange adds an RTT to connection setup.
- **RTP/RTCP**: RTCP adds ~5% bandwidth; RTP itself has no security (needs SRTP), no reliability (needs app FEC/retransmit), and interop pain (SDP/negotiation complexity).
- **Ecosystem gravity**: TCP/UDP have 40 years of middleware, NAT, firewalls, hardware offload, and developer tooling; any new transport fights that — the biggest disadvantage of *all* non-TCP/UDP protocols.

## 13. Interview Questions
1. **Q: What is SCTP?** A: A message-oriented, reliable, connection-oriented transport (RFC 9260) with multiple streams (per-stream ordering — no cross-stream HOL blocking), multihoming (multiple IPs per endpoint, failover), and a cookie-based 4-way handshake. The "best transport nobody deployed."
2. **Q (tricky): How is SCTP different from TCP?** A: (1) Messages, not bytes; (2) multiple streams with *independent* ordering — a loss on stream 0 doesn't block stream 1 (the anti-HOL-blocking that QUIC later copied); (3) multihoming — the association survives a path failing; (4) a 4-way INIT/COOKIE handshake with built-in DoS resistance; (5) optional partial reliability (PR-SCTP).
3. **Q: Why did SCTP use a 4-way handshake?** A: The server sends its state as a *cookie* in INIT-ACK without allocating resources; only after COOKIE-ECHO does it commit. SYN-flood-style attacks cost the server almost nothing — DoS resistance built into the protocol, not an afterthought.
4. **Q (FAANG): Why didn't SCTP replace TCP?** A: Deployment gravity: middleboxes/NATs/firewalls don't understand it, OS support is uneven, hardware offload is absent, the whole TCP/HTTP/TLS ecosystem expects byte streams, and its multihoming needs special network support. The Internet is a de-facto TCP/UDP-only network — that's precisely why QUIC chose UDP as its carrier.
5. **Q: What is multihoming?** A: An SCTP endpoint can present multiple IP addresses; the association picks a primary path and heartbeats the rest; on failure it *continues* on an alternate path without reconnecting. TCP's connection is bound to one tuple — an IP change kills it.
6. **Q: What is DCCP and when would you use it?** A: Datagram Congestion Control Protocol (RFC 4340): unreliable datagrams (like UDP) *with* congestion control (CCID 2 ≈ TCP Reno, CCID 3 ≈ TFRC). For loss-tolerant real-time traffic that must be TCP-friendly but can't tolerate retransmission latency.
7. **Q (tricky): DCCP vs UDP vs TCP?** A: TCP = reliable + CC + ordering; UDP = none of those; DCCP = CC only (no reliability, no ordering). DCCP is the "fairness without the guarantee" point — the traffic that needs to behave well on the network but can afford loss.
8. **Q: What is DTLS?** A: TLS over datagrams (RFC 6347): same security guarantees, adapted to UDP — replay-window instead of exact record sequencing, handshake retransmission on loss, stateless cookies vs amplification. It's how WebRTC encrypts (SRTP keyed via DTLS).
9. **Q (production): Why does WebRTC use SRTP + DTLS?** A: Media (SRTP) must be low-latency and loss-tolerant — RTP over UDP; keys must be negotiated securely and connectionless — DTLS-SRTP. You can't use TLS over TCP for a real-time video stream (latency), so the datagram-native security layers take over.
10. **Q: What is RTP and how does it relate to UDP?** A: RTP (RFC 3550) is the real-time media transport: sequenced, timestamped payload packets (audio/video) over UDP, with RTCP as the statistics/feedback channel (loss, jitter) driving adaptive bitrate. UDP gives the latency; RTP gives the timing/loss signal.
11. **Q (tricky): Why would QUIC add unreliable datagrams when it already has streams?** A: Some data is best-effort by nature (game state, live telemetry, preview frames) and shouldn't pay retransmission/ordering. QUIC datagrams (RFC 9221) carry that in the *same* authenticated, congestion-controlled, migratable connection — one connection for both modes instead of a second UDP socket.
12. **Q: What is PR-SCTP?** A: Partial Reliability (RFC 3758): a message can be marked to expire after a time/retry budget — deliver if you can, else drop. The "reliability, on your terms" option that neither TCP (always) nor UDP (never) provides.
13. **Q (FAANG): You need a transport for a high-availability storage replication system. Which do you pick and why?** A: SCTP, if deployable: multihoming (link failover without reconnecting), multiple streams (isolate control from data), message boundaries (native framing), and PR-SCTP (skip stale deltas). If SCTP isn't available (typical), QUIC with streams + connection migration gives most of the same properties over UDP/443.
14. **Q: What's the difference between a "connection" (TCP) and an "association" (SCTP)?** A: An association is a relationship between *endpoints* (sets of addresses) rather than a pair of sockets, and it bundles multiple streams. TCP is exactly one (tuple, byte-stream) pair; SCTP is (many addresses, many streams).
15. **Q (production): Is WebRTC's data channel SCTP?** A: Yes — SCTP runs *over* DTLS-over-UDP specifically so browsers can use SCTP's features (multiple streams, partial reliability) despite no kernel/network support for raw SCTP. It's the only wide-scale SCTP deployment in the world.
16. **Q: Why do telecoms use SCTP for SIP?** A: SIP signaling is messages (not a stream), needs reliability + ordering, and carrier-grade setups require multihoming (a trunk link failure must not drop calls) and stream isolation (one busy stream shouldn't block call control). SCTP matches all four exactly; TCP fails multihoming + message framing.
17. **Q (tricky): What's the role of TCP in the real-time world?** A: Setup/control: SIP/WebRTC signaling and TLS/DTLS-SRTP negotiation run over TCP; media runs over UDP/RTP. The common design is "TCP for the handshake/control, UDP/RTP for the stream" — the transport *split* is a classic architecture answer.

## 14. Follow-Up Questions
1. **Q: How did QUIC inherit SCTP's ideas?** A: Multi-streaming (SCTP's streams → QUIC's streams, both killing HOL blocking), stream-level reset, and user-space control. But QUIC fixed SCTP's deployment problem (UDP carrier + TLS + no middlebox requirement) — "SCTP's design, TCP's ecosystem, UDP's carrier." Great interview line.
2. **Q: What is "partial reliability" and where does it matter?** A: Time-bound reliability: deliver the message if it fits the deadline, else drop it. Real-time deltas (stock ticks, game states, live sensor data) become garbage when stale — PR-SCTP and QUIC's DATAGRAM both express "reliable-ish, deadline-bound."
3. **Q (tricky): Why is RTP not a "transport protocol" like TCP?** A: It deliberately provides *no* reliability, ordering, congestion control, or port demux beyond UDP — it's a *payload format* layer (sequence + timestamp + codec mapping) on top of UDP, leaving transport behavior (latency vs loss) to the app. That's why it's "application-layer" in the OSI sense even though it's transport-adjacent.
4. **Q: When would DCCP beat QUIC datagrams?** A: If you want *standardized* TCP-fair CC with zero app logic and no encryption overhead (research/hardware). In practice QUIC datagrams win on deployability (UDP/443, TLS, migration) — DCCP never got the ecosystem. It's the "also-ran" that explains *why* QUIC's approach won.
5. **Q (FAANG): "Design a transport for low-latency stock trading."** A: Requirements: minimal + deterministic latency (no TCP ACK/retransmit stalls), message boundaries, redundancy (multihoming — two networks), and protocol-level integrity. Answer: UDP (lowest latency, no HOL) + app-level FEC/sequence for integrity + dual-path multicast/unicast; or SCTP if the market's network supports it; definitely *not* TCP (retransmission latency + single path). The *design process* (guarantee-set selection) is the interview.

## 15. Coding Example
```python
# RTP-style media framing over UDP — the real-time pattern in miniature
import socket, struct, time, random

def rtp_header(pt=96, seq=0, ts=0, ssrc=0x1234):
    # version=2, padding=0, ext=0, cc=0, marker=0, payload type=pt, seq, ts, ssrc
    first = (2 << 6) | pt
    return struct.pack(">BBHII", first, 0, seq, ts, ssrc)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
seq, ts = 0, 0
for _ in range(5):                       # 5 media packets, no reliability
    payload = bytes([random.randint(0, 255) for _ in range(160)])   # 20 ms of PCM
    pkt = rtp_header(seq=seq, ts=ts) + payload
    sock.sendto(pkt, ("127.0.0.1", 4004))  # best-effort, ~20 ms apart
    seq += 1; ts += 160
    time.sleep(0.02)

# (Real RTP would add RTCP receiver reports driving adaptive bitrate.)
```
```bash
# RTP/SCTP/DCCP on the wire
$ sudo tcpdump -i eth0 udp port 4004 -nn -vv | head
#   UDP, length 172   (12-byte RTP header + 160-byte payload)
$ tshark -i eth0 udp port 4004 -Y rtp          # RTP stream + sequence analysis
# Inspect any SCTP on the box (rare outside telecom/WebRTC):
$ sudo modprobe sctp && ss -san | grep -i sctp
```

## 16. Industry Usage
- **Telecom core (the big one)**: SCTP carries SIP/SIGTRAN in carrier networks and the 5G core (NGAP, NAS/AMF) — a $100B industry runs on "the transport that never deployed" in the web world. Availability/failover is the mandate; multihoming is mandatory.
- **WebRTC**: SCTP-over-DTLS for data channels (file transfer, game state over the browser's SCTP), SRTP+DTLS for media — the largest real-time + SCTP deployment on the public Internet.
- **VoIP/video platforms (Twilio, Zoom, Meet, Teams)**: RTP/RTCP over UDP/SRTP with DTLS keying; adaptive bitrate from RTCP feedback; the entire real-time web is RTP-family.
- **IoT**: CoAP over DTLS (UDP-based, constrained devices) — datagram-native security for small payloads.
- **Fintech/HFT**: low-latency UDP + FEC + dual-path (multihoming via a *network* transport, often not SCTP but raw UDP) — the "deterministic latency" niche.
- **Protocol designers (the lesson)**: QUIC's datagrams, WebTransport, and MASQUE all borrow the "pick your guarantee set" framing — the modern transport design language is this section's design space.

## 17. References
- RFC 9260 — Stream Control Transmission Protocol (SCTP): https://www.rfc-editor.org/rfc/rfc9260
- RFC 3758 — PR-SCTP (partial reliability): https://www.rfc-editor.org/rfc/rfc3758
- RFC 4340 — Datagram Congestion Control Protocol (DCCP): https://www.rfc-editor.org/rfc/rfc4340
- RFC 4341/4342 — CCID 2 (TCP-like), CCID 3 (TFRC): https://www.rfc-editor.org/rfc/rfc4341
- RFC 6347 — Datagram Transport Layer Security (DTLS 1.2): https://www.rfc-editor.org/rfc/rfc6347
- RFC 3550 — RTP/RTCP: https://www.rfc-editor.org/rfc/rfc3550
- RFC 9221 — QUIC Unreliable Datagram Extension: https://www.rfc-editor.org/rfc/rfc9221

## 18. Cheat Sheet
- SCTP: message-oriented, association (multihomed), multi-stream (no cross-stream HOL), 4-way cookie handshake, PR-SCTP partial reliability. Telecom + WebRTC.
- DCCP: unreliable datagrams + congestion control (CCID 2 ≈ Reno, CCID 3 ≈ TFRC). Never deployed widely.
- DTLS: TLS over UDP — replay window, handshake retransmission, stateless cookies. WebRTC keying, CoAP.
- RTP/RTCP: sequenced/timestamped media (RTP) + loss/jitter feedback (RTCP, ~5% bw). The real-time standard.
- QUIC datagrams (RFC 9221): unreliable frames inside a reliable, encrypted, migratable connection.
- TCP = reliable+ordered+single path. UDP = nothing. DCCP = CC only. SCTP = reliable+ordered-per-stream+multihomed+message.
- Why not deployed: middlebox/ecosystem gravity — "TCP/UDP-only Internet" is why QUIC rode UDP.
- 5G core: SCTP (NGAP). Browser: SCTP-over-DTLS. VoIP: RTP/UDP/SRTP.

## 19. Quiz
1. SCTP handshake has how many segments? a) 2 b) 3 c) 4 d) 5 → **c**
2. SCTP associations support: a) one IP b) multihoming c) byte streams d) no streams → **b**
3. SCTP stream ordering is: a) global b) per-stream c) none d) FIFO all → **b**
4. The cookie in SCTP's handshake provides: a) speed b) DoS resistance c) encryption d) pacing → **b**
5. DCCP provides: a) reliability b) congestion control c) ordering d) TLS → **b**
6. DTLS runs over: a) TCP b) UDP c) SCTP d) raw IP → **b**
7. WebRTC media uses: a) TCP b) RTP over UDP c) SCTP only d) DCCP → **b**
8. RTP packets carry: a) only bytes b) sequence + timestamp c) ACKs d) keys → **b**
9. PR-SCTP allows: a) partial reliability b) no reliability c) byte streams d) TLS → **a**
10. Which carries 5G core signaling? a) DCCP b) SCTP c) RTP d) DTLS → **b**

## 20. Flashcards
- **Q: SCTP's key features?** → **A:** messages, multihoming, multi-streams, 4-way cookie handshake, PR-SCTP.
- **Q: SCTP vs TCP?** → **A:** messages vs bytes; streams (no cross-stream HOL); multihoming; cookie handshake.
- **Q: Why 4-way handshake?** → **A:** stateless cookie → built-in SYN-flood resistance.
- **Q: DCCP?** → **A:** UDP + congestion control (CCID 2/3), no reliability.
- **Q: DTLS?** → **A:** TLS over UDP; replay window + handshake retransmit.
- **Q: RTP/RTCP?** → **A:** media transport (seq/ts) + feedback (loss/jitter).
- **Q: QUIC datagrams?** → **A:** unreliable frames in a reliable encrypted connection.
- **Q: Why didn't SCTP win?** → **A:** ecosystem/middlebox gravity; QUIC rode UDP instead.

## 21. Revision
The transport design space: TCP (reliable, ordered, single-path byte stream), UDP (nothing), DCCP (CC without reliability), SCTP (reliable, per-stream ordered, multihomed, message-oriented, cookie 4-way handshake, PR-SCTP). SCTP serves telecom/5G core + WebRTC data channels (over DTLS). DTLS = TLS over UDP (replay window, handshake retransmit) — WebRTC keying. RTP/RTCP = real-time media over UDP (seq+timestamp, RTCP feedback ~5% bw). QUIC datagrams add unreliable frames inside a reliable encrypted connection. Non-deployment of SCTP/DCCP = middlebox/ecosystem gravity — the reason QUIC rode UDP.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is SCTP and how is it different from TCP?" | 2 How It Works / 13 Q&A |
| "Why a 4-way handshake?" | 13 Q&A / 4 Why Not Another Approach |
| "Why didn't SCTP replace TCP?" | 13 Q&A / 10 Time Complexity |
| "What is DCCP?" | 13 Q&A / 7 Formal Definition |
| "What is DTLS and why for WebRTC?" | 13 Q&A / 9 Internal Working |
| "What is RTP/RTCP?" | 13 Q&A / 8 Example |
| "Why QUIC datagrams?" | 13 Q&A / 14 Follow-Up |
| "Design a transport for X" | 13 Q&A / 15 Coding |
| "Where does SCTP actually run?" | 16 Industry Usage |
