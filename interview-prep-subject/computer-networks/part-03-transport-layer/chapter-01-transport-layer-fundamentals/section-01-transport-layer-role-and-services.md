# Transport Layer: Role and Services

> **TL;DR**: The transport layer sits between the application and the network, converting the network's *host-to-host, best-effort* IP service into a *process-to-process* channel with a chosen service mix — TCP trades latency/overhead for reliability, ordering, flow and congestion control; UDP offers minimal connectionless delivery — and this choice is the single biggest design decision in every networked application.

## 1. Why Does This Exist?
The network layer (IP) delivers *packets* to *hosts* — not to processes, not reliably. But applications need: (1) **demultiplexing** — a server's web traffic must reach the web process, not the mail process; (2) **reliability** — lost/corrupted/reordered packets must be detected and repaired; (3) **congestion safety** — a fast sender must not collapse the network. The transport layer exists precisely to add these on top of IP *without changing IP*: it converts IP's "best-effort datagram delivery to a host" into "a reliable (or unreliable) byte channel between processes." The reason it's a separate layer (not built into IP or into every app) is the **end-to-end principle**: IP stays minimal and dumb; the reliability machinery lives at the edges, shared by all apps via TCP.

## 2. How Does It Work?
Transport provides a menu of **services**; each protocol picks a subset:
| Service | TCP | UDP | Meaning |
|---|---|---|---|
| Connection-oriented | ✅ | ❌ | Explicit setup/teardown before data |
| Reliable (retransmission) | ✅ | ❌ | Lost data detected + resent |
| In-order delivery | ✅ | ❌ | Bytes delivered in send order |
| Byte-stream vs datagram | stream | datagram | Segmentation/assembly vs message boundaries |
| Flow control | ✅ | ❌ | Sender respects receiver buffer capacity |
| Congestion control | ✅ | ❌ | Sender respects network capacity |
| Ports/multiplexing | ✅ | ✅ | Process-to-process addressing |
| Checksum (integrity) | ✅ | ✅ | Corrupt-data detection |
| Full-duplex | ✅ | ✅ | Both directions simultaneously |
| Connectionless/low-latency | ❌ | ✅ | No handshake, minimal overhead |

**Mechanism at a glance**: the sender's transport takes application data, segments it (TCP) or keeps datagrams (UDP), adds a header (ports + seq/ack for TCP), passes to IP. The receiver's transport uses ports to demultiplex to the right socket, reassembles (TCP) in order, and repairs losses via ACKs/retransmission. It's the "middleman" between the app's needs and the network's capabilities.

## 3. When Is It Used?
- **TCP**: web (HTTP/HTTPS), email (SMTP/IMAP), file transfer (FTP/SFTP), SSH, databases (Postgres/MySQL), APIs, git — anything needing correctness/ordering.
- **UDP**: DNS (query/response), VoIP/RTP, video streaming (with app-level reliability or loss tolerance), gaming, DHCP (bootstrap, no IP yet), TFTP, NTP (time sync), QUIC's substrate (HTTP/3), multicast.
- **Both/derived**: QUIC (reliable over UDP), SCTP (reliable + message-oriented — telecom, WebRTC data channels historically), DCCP (congestion-controlled but unreliable — real-time).
- **Load balancers**: L4 (TCP/UDP ports) vs L7 (HTTP) — the transport-level balancing decision is a daily cloud choice.

## 4. Why Wasn't Another Approach Chosen?
- **Why not put reliability in IP?** IP is deliberately minimal so routers stay fast/stateless; the end-to-end argument (Saltzer/Reed/Clark) says reliability belongs at the edges where the loss is *known*. A reliable-IP would slow everything for everyone; instead TCP gives reliability only to apps that want it, and UDP gives none to the rest.
- **Why not let every application implement reliability?** Reimplementing ACK/retransmission/flow/congestion control in every app = disaster (bugs, inconsistency, no shared congestion behavior). Centralizing in TCP gives one battle-tested implementation (and now QUIC) that all apps share.
- **Why TCP as byte-stream instead of message-oriented?** A byte stream decouples *send boundaries* from *delivery* — the receiver doesn't need to parse message framing; apps add their own framing (HTTP content-length, JSON length prefixes). Message orientation (SCTP, or UDP+app logic) preserves message boundaries but is more complex; TCP's stream model won for simplicity + web apps.
- **Why UDP at all?** Because some apps *don't want* reliability overhead: real-time (a late retransmit is worse than a lost packet — video), simple queries (DNS), and bootstrap (DHCP needs UDP-broadcast-before-IP). UDP is the "no guarantees, lowest overhead" choice — and its users add exactly the reliability they need (QUIC did).
- **Why a separate transport layer (not one protocol per app)?** One shared transport abstraction (BSD sockets) lets apps use a standard API, and the OS multiplexes many apps over one IP stack — the efficiency and portability win.

## 5. Intuition
IP is the **courier company** that will deliver *any* package to the *right building* (host), best-effort — it may lose a package or deliver them out of order. The transport layer is the **office you hire** to handle your specific needs:
- **TCP** = the "guaranteed delivery service": every page of your manuscript is numbered, the office confirms receipt, re-sends lost pages, and delivers the full document *in order* at the destination. Cost: more calls, slower, but nothing lost.
- **UDP** = the "postcard service": you drop cards, they arrive whenever, maybe not in order, and if one's lost you don't find out (until you ask again). Perfect for live TV (a dropped frame is fine) or a DNS question.
The transport layer is *your choice of office* — same courier (IP) underneath, different guarantees on top.

## 6. Real-World Analogy
**The express freight company (TCP) vs the postcards (UDP)**: TCP is like FedEx's guaranteed express: a driver picks up your box, you get a tracking number (seq), the system confirms delivery (ACK), re-routes lost boxes (retransmit), and won't overwhelm the receiving dock (flow control) or the roads (congestion control). UDP is dropping postcards in a mailbox: cheap, fast, no tracking, no guarantees — fine for "I'm fine, visiting Paris" but not for legal documents. And the *ports* are the "attention: HR department" labels on the envelope — the courier (IP) drops the mail at the building; the mailroom (transport) routes it to the right department (process).

## 7. Formal Definition
The transport layer (OSI L4 / TCP-IP Transport) provides **end-to-end communication services for processes** over the network layer. Its primary functions: **multiplexing/demultiplexing** (ports), **reliable transfer** (TCP: ACKs, sequence numbers, retransmission), **ordered delivery** (TCP reassembly), **flow control** (TCP: receiver window), **congestion control** (TCP: cwnd/AIMD), and **integrity** (checksums). **TCP** (RFC 9293) is a connection-oriented, reliable, ordered byte-stream protocol. **UDP** (RFC 768) is a connectionless, unreliable, message-oriented datagram protocol providing only ports + checksum. Each transport PDU is a **segment** (TCP) or **datagram** (UDP). The service model is defined by the application's requirements: correctness, latency, bandwidth, and loss tolerance.

## 8. Example
Two apps on the same host, same moment — transport in action:
```
Host 192.168.1.10 runs:  web browser (TCP) + VoIP app (UDP)
Web:  TCP segment (src port 54321 -> dst 443, seq 1000, ack 5000)
VoIP: UDP datagram (src port 57000 -> dst 5060, 20ms of audio)
Both handed to IP, both leave via the same NIC.
Remote host 10.0.0.5: IP delivers both; TCP demuxes by (dst IP, dst port 443)
  -> web process; UDP demuxes by (dst port 5060) -> VoIP process.
Same network, same NIC — different transport semantics per app.
```
Numbers: a 1000-byte HTTP response over TCP = one segment (1460 B max payload) → one IP packet → one frame. The same 20ms VoIP audio = a 200-byte UDP datagram → an IP packet → a frame. TCP adds ~20 B header + ACK traffic; UDP adds 8 B header and nothing else.

## 9. Internal Working
1. **Sender**: app calls `send()` → OS transport buffers data → TCP segments it to MSS (typically 1460 B) adding seq/ack/window/checksum; UDP copies the datagram as-is with an 8 B header.
2. **Demultiplexing at receiver**: the OS hashes the (srcIP, srcPort, dstIP, dstPort) four-tuple to find the exact socket; for UDP, it can match by (dstIP, dstPort) alone (connectionless); for TCP, all four fields + connection state. Unknown port → ICMP "port unreachable" / RST (TCP).
3. **TCP machinery** (details in later sections): sequence/ack numbering per byte, ACK accumulation, timers (retransmission, delayed-ACK, keepalive), window updates (rwnd, cwnd), state transitions.
4. **UDP machinery**: nothing — no state, no retransmission. The checksum is optional in IPv4 (0 = off) but mandatory in IPv6.
5. **Kernel implementations**: Linux `net/ipv4/tcp_*.c`, `udp_*.c`; sockets (`sock` struct), buffers (send/recv queues), and protocol handlers (`tcp_v4_rcv`, `udp_rcv`) — the transport code is the OS's most-traveled path.
6. **Integration with IP**: transport headers ride inside IP payloads; IP's Protocol field (6=TCP, 17=UDP) tells IP's demux which transport handler gets the packet.

## 10. Time Complexity
- **Per-packet processing**: TCP O(1) per segment (seq/ack/window, checksum O(payload) — offloaded to NIC hardware → O(1)-ish at line rate); UDP O(1) per datagram.
- **TCP overhead per connection**: handshake = 1 RTT; teardown = up to 4 segments; per-byte ACK cost ~ O(1) per segment. TCP can sustain millions of segments/sec on modern NICs (sendfile, GSO/GRO, checksum offload).
- **UDP overhead**: ~0 — no state, no timers, no ACKs; the lowest-latency transport (barring QUIC's added machinery).
- **Memory**: per-TCP-socket buffers (send/recv queues, kernel `tcp_mem` limits) — a server with 100k sockets uses GBs; UDP sockets are lightweight.

## 11. Advantages
- **TCP**: reliability + ordering (correctness), flow/congestion control (fairness, network safety), full-duplex streaming, ubiquitous (everything runs on it), battle-tested.
- **UDP**: minimal overhead (8 B header), no handshake latency, no head-of-line blocking at transport, low latency, connectionless (no state — scales trivially), message boundaries preserved, good for real-time + bootstrap.
- **Choice itself**: the transport menu lets each app pick its cost/guarantee trade-off (the "network neutrality of transport").

## 12. Disadvantages
- **TCP**: head-of-line blocking (one loss stalls the whole stream), congestion-control throughput limits (slow start, fairness to others), handshake/teardown latency, overhead per byte (ACK traffic), amplification of RTT, buffer bloat sensitivity.
- **UDP**: no reliability/ordering/flow/congestion control — apps must build them (and most shouldn't), no congestion-awareness (can collapse a network), limited by firewalls/proxies (some block it), no built-in error recovery.
- **Shared**: port exhaustion under abuse, checksum-only integrity (no end-to-end encryption by default — that's TLS/QUIC's job).

## 13. Interview Questions
1. **Q: What is the transport layer's job?** A: It provides process-to-process, end-to-end communication over the host-to-host, best-effort IP service — adding multiplexing (ports), and optionally reliability, ordering, flow control, and congestion control (TCP) or keeping it minimal (UDP).
2. **Q: What services does TCP provide that UDP doesn't?** A: Connection orientation, reliability (retransmission), in-order delivery, flow control (receiver window), and congestion control (cwnd/AIMD). Both provide ports and checksums; UDP is connectionless and message-oriented.
3. **Q (tricky): Is UDP "unreliable"?** A: The *protocol* makes no reliability guarantees — but applications can build reliability on it (QUIC does exactly this). "Unreliable" means "no guarantee," not "always loses data." DNS works perfectly over UDP; lost DNS answers just get re-asked.
4. **Q: What is multiplexing and demultiplexing in transport?** A: Multiplexing = the sender's transport gathers data from many sockets and hands them to IP. Demultiplexing = the receiver's transport uses the destination port (and for TCP, the four-tuple) to route each segment/datagram to the correct socket/process.
5. **Q (production): Why does a server with one IP handle a million TCP connections?** A: Each connection is identified by the four-tuple (srcIP, srcPort, dstIP, dstPort) — the destination (IP, port 443) is shared, but the *source* tuple differs per client. The OS demultiplexes by hashing the full tuple into separate socket structures.
6. **Q: What is the end-to-end argument and how does it justify the transport layer?** A: Reliability/correctness should live at the *edges* (transport/app), not in the core (IP/routers). The network stays dumb and fast; the transport layer (at the edge) fixes loss/ordering. This is why IP is best-effort and TCP does the repair.
7. **Q: Why is TCP a byte stream but UDP a datagram?** A: TCP delivers an ordered byte stream (send boundaries erased; apps add framing). UDP preserves message boundaries (each datagram is a complete message). Byte stream = simpler for web/file apps; datagram = natural for query/response + real-time.
8. **Q (scenario): A live video call + a file download on the same network. Which transport for each and why?** A: Video → UDP (late data is useless; a retransmit would arrive after its time slot; slight loss is fine). File → TCP (needs exact bytes in order; latency irrelevant). This is exactly how Zoom (UDP/RTP for media) + browsers (TCP for downloads) coexist.
9. **Q: What is a segment vs a datagram vs a packet?** A: Segment = TCP transport PDU. Datagram = UDP transport PDU (also IP PDU). Packet = network-layer (IP) PDU. Frame = link-layer PDU. Each layer names its own unit.
10. **Q: How does the receiver know which transport protocol a packet carries?** A: IP's Protocol field: 6 = TCP, 17 = UDP (also 1 = ICMP, 132 = SCTP). The IP layer uses it to dispatch to the right transport handler before ports are examined.
11. **Q (tricky): Can TCP be "faster" than UDP for small messages?** A: Rarely — TCP's handshake + ACKs add latency; but for *reliable* small messages, TCP's delayed-ACK batching and Nagle can amortize well. Generally UDP+app-reliability (or QUIC) beats raw TCP for latency-sensitive reliable transfers.
12. **Q: What is the TCP slow start and why is it at the transport layer?** A: Congestion control lives in transport because only the sender knows its sending rate and observes losses — a per-sender responsibility (end-to-end). Slow start probes available capacity (exponential growth) to avoid flooding the network on start.
13. **Q (production): Your app uses UDP for telemetry and some packets vanish on the WAN. Diagnose.** A: UDP has no recovery — loss could be queue drops (bufferbloat), congestion, or ICMP black-holing (firewalls). Fixes: add app-level ACKs/sequence numbers (or move to QUIC), set DSCP/QoS, use a reliable overlay. The point: UDP pushed the reliability responsibility to you.
14. **Q: What are the port number ranges?** A: 0-1023 well-known (HTTP 80/443, DNS 53, SSH 22), 1024-49151 registered (Postgres 5432, MySQL 3306, RDP 3389), 49152-65535 dynamic/ephemeral (client-side source ports).
15. **Q: What is the TCP checksum covering (pseudo-header)?** A: TCP's checksum covers the TCP header + payload + a *pseudo-header* (src IP, dst IP, protocol, length) — detecting misdelivery to the wrong host. UDP's checksum covers UDP header + payload + pseudo-header too (mandatory in IPv6).
16. **Q: How does the transport layer interact with load balancers?** A: L4 LBs (NLB) forward *transport-level* (TCP/UDP) flows by the four-tuple — no HTTP parsing, connection-oriented NAT (SNAT/DNAT). This is the "L4 vs L7" distinction from Part 02, built on this layer's semantics.
17. **Q (FAANG): "Why is my 1 Gbps link only delivering 100 Mbps to a single TCP flow?"** A: TCP throughput ≈ Window/RTT (or cwnd/RTT). At RTT 100 ms, you need window ≥ 1 Gbps × 0.1 s = 12.5 MB ≈ 100 Mb of in-flight data — likely hitting the receiver window (rwnd) or cwnd limits, or loss-driven congestion control backing off. Fix: window scaling, more flows, or delay-based CC (BBR).
18. **Q: What is head-of-line blocking and which transports have it?** A: TCP has it — one lost segment blocks delivery of *all* subsequent bytes until retransmission. UDP has none at the transport (apps see gaps immediately). QUIC removes it *per-stream* (independent streams). This single property drives the HTTP/3 design.

## 14. Follow-Up Questions
1. **Q: What exactly does the BSD socket API give the transport layer?** A: `socket()` creates an end-point, `bind()`/`connect()`/`listen()`/`accept()` set up TCP, `send/recv` move bytes, `setsockopt` tunes buffers (SO_RCVBUF, TCP_NODELAY) — the standard interface to these transport services.
2. **Q: What is the difference between congestion control and flow control?** A: Flow control = receiver can't keep up (rwnd — receiver buffer). Congestion control = *network* can't keep up (cwnd — the sender's estimate of path capacity). Both are windows; TCP uses the min.
3. **Q: When would you implement reliability on UDP instead of using TCP?** A: When you need low latency + partial reliability (some losses acceptable), message boundaries, multicast, or custom ordering (e.g., game state where only the latest matters — "TBR" — or RTP for media). QUIC packages this trade-off for HTTP.
4. **Q: What is the transport layer's role in a zero-trust network?** A: mTLS (TLS in transport-ish layer) + application-layer auth; the transport provides the encrypted channel (TCP+TLS) while app policy decides who connects. Ports are no longer trust boundaries.
5. **Q: Why does the OS track "connection" state only for TCP and not UDP?** A: TCP is stateful by design (seq/ack/window/timers per connection). UDP is connectionless — no state; each datagram is independent. That's why UDP scales trivially (no connection table) but gives no reliability.

## 15. Coding Example
```python
# Transport-layer selection in Python — same app data, two service models
import socket

def tcp_echo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP: reliable stream
    s.connect(("127.0.0.1", 8000))
    s.sendall(b"hello")                      # bytes arrive reliably, in order
    data = s.recv(1024)
    s.close()
    return data

def udp_echo():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP: datagrams
    s.sendto(b"hello", ("127.0.0.1", 8001))  # one message; no guarantees
    data, _ = s.recvfrom(1024)
    s.close()
    return data

print(tcp_echo(), udp_echo())
```
```
# Observe both transports on one interface (Linux)
$ ss -tn | head            # TCP connection table (state, four-tuples)
# State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
# ESTAB  0      0      192.168.1.10:54321  10.0.0.5:443
$ ss -un | head            # UDP "connections" (just bound sockets, no state)
# Recv-Q Send-Q Local Address:Port  Peer Address:Port
# 0      0      0.0.0.0:53               0.0.0.0:*
$ tcpdump -nn 'tcp or udp'  # see both protocols' headers on the wire
```

## 16. Industry Usage
- **Every web/app**: TCP+TLS is the default; UDP appears for DNS/QUIC/media. Cloud LBs (ALB/NLB), proxies (nginx), and service meshes all operate at the transport layer.
- **Amazon/AWS**: NLB is L4 (TCP/UDP), ALB is L7 (HTTP); CloudFront uses TCP/TLS; AWS Global Accelerator uses Anycast (UDP-based) for fast paths. VPC security groups filter by transport (port/protocol).
- **Google**: BBR congestion control (a *transport-layer* algorithm in their kernel/QUIC), QUIC for HTTP/3 (Google-owned), gRPC over TCP+TLS.
- **Zoom/Teams**: UDP/RTP for media with app-level FEC/RTX (transport semantics tuned for real-time), TCP fallback.
- **Cloudflare**: terminates TCP/UDP/QUIC at the edge; their congestion-control and TCP-stack tuning (TCP "optimizer") is a product feature — transport tuning at Internet scale.

## 17. References
- RFC 9293 — TCP (obsoletes RFC 793): https://www.rfc-editor.org/rfc/rfc9293
- RFC 768 — UDP: https://www.rfc-editor.org/rfc/rfc768
- RFC 1122 — Host requirements (transport): https://www.rfc-editor.org/rfc/rfc1122
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 3 (Transport Layer).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 6 (Transport).
- Stevens, *TCP/IP Illustrated Vol. 1*.

## 18. Cheat Sheet
- Transport = process-to-process, end-to-end, over IP's host-to-host.
- TCP: connection-oriented, reliable, ordered stream, flow+congestion control, ports, checksum.
- UDP: connectionless datagrams, ports, checksum, nothing else.
- Multiplex/demultiplex by ports; TCP demux = four-tuple.
- Segment = TCP PDU; datagram = UDP PDU.
- IP Protocol field: 6=TCP, 17=UDP.
- End-to-end argument: reliability at edges, not the core.
- Port ranges: 0-1023 well-known, 1024-49151 registered, 49152-65535 ephemeral.
- TCP throughput ≈ min(rwnd,cwnd)/RTT.
- TCP = HOL blocking; UDP none; QUIC per-stream.

## 19. Quiz
1. Which is a TCP service? a) connectionless b) reliability c) no ports d) no checksum → **b**
2. UDP provides: a) flow control b) congestion control c) ports + checksum d) ordering → **c**
3. Demultiplexing uses: a) IP only b) ports/four-tuple c) MAC d) TTL → **b**
4. IP Protocol field for UDP: a) 6 b) 17 c) 1 d) 132 → **b**
5. The end-to-end argument places reliability at: a) routers b) edges (transport/app) c) NIC d) DNS → **b**
6. Well-known ports: a) 0-1023 b) 1024-49151 c) 49152-65535 d) 1-100 → **a**
7. TCP PDU is called: a) datagram b) frame c) segment d) packet → **c**
8. Flow control is governed by: a) cwnd b) rwnd c) MSS d) TTL → **b**
9. Congestion control is governed by: a) rwnd b) cwnd c) port d) MTU → **b**
10. Which has per-stream HOL blocking? a) TCP b) UDP c) QUIC d) none → **a** (QUIC isolates per stream)

## 20. Flashcards
- **Q: Transport layer job?** → **A:** Process-to-process, end-to-end delivery over IP; ports + optional reliability/flow/congestion.
- **Q: TCP vs UDP services?** → **A:** TCP adds reliability/ordering/flow/congestion/connection; UDP = ports + checksum, datagrams.
- **Q: What is demultiplexing?** → **A:** Routing segments/datagrams to the right socket by ports/four-tuple.
- **Q: Port ranges?** → **A:** 0-1023 well-known, 1024-49151 registered, 49152-65535 ephemeral.
- **Q: End-to-end argument?** → **A:** Reliability at the edges; dumb, fast core.
- **Q: TCP throughput formula?** → **A:** min(cwnd, rwnd)/RTT.
- **Q: Segment vs datagram?** → **A:** TCP segment; UDP datagram.

## 21. Revision
Transport converts IP's host-to-host best-effort into process-to-process channels. TCP = connection-oriented, reliable, ordered byte-stream with flow (rwnd) + congestion (cwnd) control and ports; UDP = connectionless datagrams with just ports + checksum. Multiplex/demultiplex by ports; TCP demux = four-tuple; IP Protocol 6=TCP, 17=UDP. End-to-end argument: reliability at edges. Port ranges: well-known 0-1023, registered 1024-49151, ephemeral 49152-65535. TCP throughput ≈ min(rwnd,cwnd)/RTT; TCP has HOL blocking; QUIC isolates per stream.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does the transport layer do?" | 1 Why / 13 Q&A |
| "TCP vs UDP services?" | 2 How It Works / 13 Q&A |
| "What is multiplexing/demultiplexing?" | 13 Q&A / 9 Internal Working |
| "Why reliability at transport, not IP?" | 4 Why Another Approach / 13 Q&A |
| "Port ranges?" | 13 Q&A / 7 Formal Definition |
| "Why is TCP slow on high-BDP links?" | 13 Q&A / 10 Time Complexity |
| "Which transport for video?" | 13 Q&A / 8 Example |
