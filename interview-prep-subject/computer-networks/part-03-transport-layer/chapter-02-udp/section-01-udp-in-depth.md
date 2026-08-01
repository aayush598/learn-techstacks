# UDP In Depth

> **TL;DR**: UDP (RFC 768) is the connectionless transport protocol: an 8-byte header (src port, dst port, length, checksum) wrapping payload into *datagrams* delivered best-effort with no handshake, no ordering, no retransmission, and no flow/congestion control. It trades reliability for low latency and app control — and is the foundation of DNS, DHCP, streaming, gaming, and QUIC.

## 1. Why Does This Exist?
TCP guarantees reliable, ordered, connection-oriented delivery — but that guarantee costs a three-way handshake, connection state, sequence/ACK bookkeeping, retransmission timers, and head-of-line blocking. Many workloads *don't want* those semantics: a DNS query is one round trip and the app can simply retry; a VoIP/RTP frame is stale if it arrives late; a video frame is better dropped than retransmitted; a game state update is superseded by the next one. UDP exists to give apps **datagram semantics with minimal overhead and maximal control**: fire the packet, forget it, and let the application decide whether/why/when reliability matters. It's also the reason TCP's own hard problems (congestion, retransmission) can be *moved into user space* — QUIC is UDP with an app-level TCP rebuilt on top.

## 2. How Does It Work?
- **Connectionless**: no handshake, no setup/teardown. A sender just creates a datagram, stamps the destination (IP, port), and transmits. Each datagram is independent.
- **8-byte header**: SrcPort(16) | DstPort(16) | Length(16) | Checksum(16).
- **Length** = UDP header + payload (min 8, max 65535). Payload max = 65507 bytes (65535 - 8 UDP - 20 IPv4), practically ~1472 bytes before IP fragmentation at MTU 1500.
- **Checksum** (IPv4 optional but 0 usually means disabled; IPv6 *mandatory*): computed over the payload + UDP header + a 12-byte *pseudo-header* (src IP, dst IP, zero, protocol=17, UDP length). End-to-end integrity across IP + UDP.
- **Multiplexing**: delivery to the socket bound to (dst IP, dst port); with "connected" sockets the src IP+port is also matched.
- **No reliability**: delivery, ordering, and duplication are NOT guaranteed. IPv6 routers may silently drop.
- **Fragmentation**: large datagrams are fragmented at the IP layer (IPv4 routers, IPv6 end-hosts) and reassembled at the destination.

## 3. When Is It Used?
- **DNS** (port 53): queries/responses as single datagrams; retry with timeout; TCP fallback for large (DNSSEC, zone transfer) responses.
- **DHCP** (67/68): boot-time, server may be unknown → broadcast; connectionless is natural.
- **VoIP / RTP / WebRTC** (RTP over UDP): real-time audio/video — late data is useless; RFC 3550.
- **Live streaming**: RTMP/WebRTC/live transcodes prefer low-latency UDP delivery.
- **Online gaming**: position/state updates supersede old ones; no point retransmitting.
- **Network services**: NTP (123) time sync, SNMP (161/162), TFTP (69), syslog (514), QUIC (443), WireGuard (51820), VXLAN (4789), DNS over QUIC.
- **Multicast/broadcast**: one-to-many delivery only works via UDP (IP multicast is UDP-based).

## 4. Why Wasn't Another Approach Chosen?
- **Why not TCP with the app setting timeouts?** Because TCP's *connection state*, ordered buffering, and head-of-line blocking are structural — you can't opt out. With TCP you pay the cost of ordering even when you don't need it. UDP keeps the transport minimal and lets the app choose.
- **Why not raw IP packets?** Apps would have to manage ports, checksums, fragmentation, and demux themselves, and would lose the port-based multiplexing that lets many apps share an IP. UDP gives ports + checksum + zero state.
- **Why a checksum at all?** To catch *corruption in transit* cheaply (bit flips in memory/links) at a 1% cost — data integrity is valuable even without reliability (a corrupt DNS answer is worse than none).
- **Why no flow/congestion control?** The trade-off: UDP takes the congestion-control problem *out of the kernel* and hands it to the app — enabling novel schemes (TCP-friendly pacing, real-time-friendly pacing) instead of being stuck with the kernel's default. This is exactly what QUIC exploits.
- **Why did IPv6 make the checksum mandatory?** IPv4's optional checksum was often disabled (0); IPv6 mandates it because higher-layer checks are cheap insurance.

## 5. Intuition
A **postcard**: no registered mail, no return receipt, no tracking number, no signature. You write the address (destination IP:port), add your return address (source IP:port) in case they want to reply, drop it in the slot, and it's gone. If it arrives mangled, you'll never know — unless *you* decide to send another postcard after a while if no reply came. The postal system (IP layer) may split a heavy postcard into multiple envelopes (fragmentation) and reassemble them at the destination. For "send the score once a second and don't care if one score is lost" — postcards are perfect. That's UDP: fast, stateless, and the sender is in charge of any retry logic.

## 6. Real-World Analogy
**A radio station**: The DJ broadcasts (multicast/unicast) continuously with no idea who's listening (connectionless, no state). Listeners tune in mid-song and catch whatever's on the air. There's no "request for the next song," no acknowledgment, no retransmission of a garbled second of audio — if you miss it, it's gone forever, and the next second is what matters. If the station wanted guaranteed delivery, it'd need to know every listener, track what each heard, and re-send — a massive overhead that real-time radio explicitly rejects. That's exactly why streaming/gaming/VoIP (real-time) live on UDP while file downloads (stored, reliable) live on TCP.

## 7. Formal Definition
UDP (User Datagram Protocol, RFC 768) is a connectionless transport protocol providing unreliable, unordered, best-effort delivery of *datagrams* between processes identified by 16-bit ports, over IP. Header: SourcePort(16) | DestPort(16) | Length(16) | Checksum(16) = 8 bytes. It adds only four services on top of IP: port-based multiplexing/demultiplexing, payload length, a 16-bit ones'-complement checksum (IPv4 optional, IPv6 mandatory) computed over a pseudo-header + UDP header + data, and segmentation of the app's write into one datagram per send. It provides **no** handshake, reliability, ordering, duplicate detection, flow control, or congestion control.

## 8. Example
A DNS query captured in the wild (tcpdump):
```
$ sudo tcpdump -i eth0 udp port 53 -nn -vv
17:32:01.123456 IP 10.0.0.5.53000 > 8.8.8.8.53: 30000+ A? example.com. (30)
  UDP, length 30          <- 8-byte header + 22-byte DNS payload
17:32:01.212345 IP 8.8.8.8.53 > 10.0.0.5.53000: 30000 1/0/0 A 93.184.216.34 (46)
  UDP, length 46          <- the answer datagram; no handshake, no ACK
```
Sender: one `sendto()` with 30 bytes → one datagram. Receiver: one `recvfrom()`. The "connection" is just (10.0.0.5, 53000) ↔ (8.8.8.8, 53) held only by the *apps*. If the reply never arrives, the resolver retries the query after a timeout — reliability is the app's job.

## 9. Internal Working
1. **Send path**: app calls `sendto(fd, buf, len, 0, &dest, destlen)` → the kernel copies up to len bytes into one datagram, appends the UDP header, computes the checksum (pseudo-header + UDP + data), hands to IP. IP fragments if len+8+20 > MTU (IPv4; IPv6 uses end-to-end fragmentation via the 16-bit "UDP payload length" + extension headers).
2. **Receive path**: IP reassembles fragments → hands the datagram to UDP → UDP checks the checksum (drop on mismatch), looks up the (dstIP, dstPort) (and src if connected) in the socket table → appends to the socket's receive queue → wakes `recvfrom()`. No port found → ICMP port-unreachable.
3. **No state, no queues of connections**: the socket holds only buffer + local addr (+ optionally remote). This is why UDP is so cheap for servers: one socket serves unlimited senders.
4. **Connected UDP socket** (`connect()` on UDP): stores the peer, so the kernel rejects datagrams from other sources and can send ICMP-unreachable back — a pure optimization, *not* a connection.
5. **Checksum details**: ones' complement sum; the pseudo-header "pulls in" the IP addresses so the transport detects misrouted payloads. IPv6 pseudo-header uses 128-bit addresses (IPv6 checksum mandatory).
6. **UDP on IPv6**: no IP-layer header checksum, so UDP checksum is mandatory; the pseudo-header changes (128-bit addresses); fragmentation only via extension headers at the source.
7. **Stateless servers scale**: because there's no per-connection tuple table, a UDP server can handle hundreds of thousands of RPS with a few sockets — the app reads the sender from `recvfrom` and replies to it. Perfect for DNS/DHCP control planes.

## 10. Time Complexity
- **Per-datagram cost**: O(1) amortized — copy + checksum + one socket-table lookup. No handshake (RTT saved), no retransmission timers, no state reaping.
- **Latency**: one RTT for request/response (vs 1.5 RTTs TCP with handshake + 1 data). No head-of-line blocking.
- **Memory**: near-zero per sender; the socket's buffer is shared. Servers scale horizontally without a connection table.
- **The "cost" is paid in delivery**: unreliable ≈ maybe 1-3% packet loss on a WAN that an app must tolerate or mask. Fragmentation amplification is a known DoS vector (fragmented UDP floods).
- **Throughput**: checksum is the main CPU cost (~1-2 cycles/byte); tuned NICs can offload UDP checksums (TCO/GRO) → line-rate.

## 11. Advantages
- **Minimal latency**: no handshake (saves an RTT), no head-of-line blocking, no congestion backoff — the *lowest-overhead* way to move bytes.
- **App control**: the app decides retransmission, pacing, and priority — QUIC and gaming engines rebuilt exactly that control.
- **Stateless scale**: one socket serves unlimited senders; ideal for DNS/DHCP/NTP-class control planes.
- **Broadcast/multicast**: the only way to send one-to-many (IP multicast is UDP).
- **Simple**: 8-byte header, minimal kernel code, minimal buffer/state — fewer failure modes than TCP's state machine.
- **Real-time friendly**: late data is dropped naturally — perfect for audio/video/games.

## 12. Disadvantages
- **Unreliable**: delivery not guaranteed; apps must retry, tolerate, or mask loss. Silent packet loss is invisible (no RST/ICMP notification to the socket in most cases).
- **No ordering**: datagrams can arrive in any order; apps needing order must sequence manually.
- **No congestion control (kernel-level)**: can overrun the network or starve TCP flows; responsible apps must pace (TCP-friendly rate control).
- **Fragmentation**: IP fragmentation costs CPU + is a classic DoS vector (ping-of-death, frag floods); large UDP payloads get dropped wholesale if any fragment is lost.
- **Checksum weakness**: 16-bit, no error correction; real-time apps add FEC for resilience.
- **Not firewall/NAT friendly**: stateful firewalls/NAT treat UDP as "connections" (tuple timeouts); long-lived UDP flows can be killed by short NAT timeouts; multicast is blocked in most public cloud environments.

## 13. Interview Questions
1. **Q: What is UDP and what does it guarantee?** A: Connectionless, best-effort datagram delivery. Exactly one guarantee — checksummed, port-delivered datagrams. No delivery, ordering, or duplicate guarantees.
2. **Q: Size of the UDP header? Fields?** A: 8 bytes: src port, dst port (16 each), length (16), checksum (16).
3. **Q (tricky): What is the maximum UDP payload?** A: 65507 bytes (65535 - 8 UDP - 20 IPv4). Practical safe payload without fragmentation = MTU - 8 - 20 = 1472 bytes at 1500 MTU.
4. **Q: Why does DNS prefer UDP?** A: Query/response fits in one datagram; a UDP send + timeout retry is cheaper than a TCP handshake (one RTT saved); large answers (DNSSEC, AXFR) fall back to TCP.
5. **Q: How does UDP do reliability?** A: It doesn't — the *application* adds retransmission/timeout (like DNS resolvers), or accepts loss (RTP/video/games). "UDP is TCP's simplicity; reliability lives above it."
6. **Q (FAANG): Why is QUIC built on UDP instead of a new IP protocol?** A: Because UDP is a pass-through — no kernel changes, no middlebox/NAT updates, no firewall rewrites. It's a 50-year-old deployment trick: put your new transport *inside* a UDP packet so the whole Internet just forwards it. That's the killer insight.
7. **Q: What is the UDP pseudo-header for?** A: A 12-byte structure (IPv4) carrying src/dst IPs + protocol + UDP length, checksummed with the header+data — so UDP detects data delivered to the *wrong* destination/protocol, end-to-end integrity across IP+UDP.
8. **Q: Is the IPv4 UDP checksum optional?** A: Yes — sender may send 0 (disabled) in IPv4; IPv6 *mandates* it (no IP header checksum, and routers don't fragment/recompute). Real-world IPv4 always uses it.
9. **Q: What happens if a UDP datagram arrives at a closed port?** A: The receiver sends ICMP port-unreachable; the UDP socket does NOT get an error by default (unless "connected"). This is how port scanners and UDP service discovery work.
10. **Q (tricky): What is the difference between UDP and raw sockets?** A: UDP adds ports + checksum + datagram boundaries; raw sockets hand you the raw IP packet — no ports, no checksum, and you need root. Tools like traceroute use raw ICMP/UDP; apps use UDP.
11. **Q: When should you pick UDP over TCP?** A: When per-packet latency matters more than delivery (RTP/WebRTC/live video, gaming, voice), when request/response is tiny (DNS/NTP/DHCP), when you need broadcast/multicast, or when you want to build custom reliability (QUIC, custom gaming protocol, TFTP).
12. **Q (production): Is Netflix using UDP or TCP?** A: Mostly TCP for on-demand (it needs reliable progressive playback + CDN friendliness + TLS); live/WebRTC uses UDP. It's a *myth* that all video is UDP — the industry moved reliability up and uses TCP where loss is unacceptable.
13. **Q: What is UDP fragmentation and why is it a problem?** A: A datagram > MTU is split by IP and reassembled at the destination; losing one fragment drops the whole datagram, and fragmented UDP is a classic DoS amplifier. Solution: send ≤ MTU (1472), use UDP Lite or smaller payloads.
14. **Q (tricky): What is UDP Lite?** A: RFC 3828 — a variant that checksums only part of the payload (e.g., the RTP header), tolerating corrupted payload data where partial loss is fine (video payloads). It's the "skip checksum for the body" extension.
15. **Q: How do you measure UDP loss/latency for debugging?** A: `iperf3 -u`, `socat`, `mtr` (raw UDP path), tcpdump for retransmission-free flow analysis, and app-level sequence numbers. ICMP-unreachable and NAT timeouts (e.g., ~60 s) are the classic UDP production failures.
16. **Q (FAANG): What are UDP's weaknesses as a transport for a new protocol?** A: No congestion control (must implement yourself), no fairness to TCP, NAT timeout fragility, no kernel acknowledgment, and 16-bit checksum. QUIC addressed all of these in user space.
17. **Q: What is the "length" field in the UDP header?** A: UDP header + payload in bytes (min 8). It lets the receiver know where the UDP header ends even with IP-layer padding.
18. **Q: Can UDP be used for reliable file transfer?** A: Yes — TFTP (69) is UDP with ACK/timeout per block; other custom protocols do the same with FEC. But you're reimplementing TCP; use TCP unless latency/throughput demands otherwise (e.g., UDT/FASP-style WAN transfers).

## 14. Follow-Up Questions
1. **Q: What is the "connectionless" vs "connected" UDP distinction?** A: Connectionless = each send is independent (any sender, any reply). A "connected" UDP socket (via `connect()`) only *stores* the peer — filtering + kernel errors — it's still not a connection. Nobody handshakes.
2. **Q: How does UDP handle congestion?** A: It doesn't in the kernel. The app must implement pacing (TCP-friendly rate control / TFRC, RFC 5348) or risk starving TCP and hammering the network. This "responsibility" is exactly why QUIC exists — a UDP app with proper congestion control.
3. **Q: What's the role of UDP in WebRTC?** A: WebRTC uses RTP/SRTP over UDP for media (real-time, loss-tolerant, FEC for resilience) and DTLS over UDP for encryption; RTCP reports loss/latency to drive adaptive bitrate. UDP + app-level reliability = the WebRTC model.
4. **Q: Why do game engines use UDP when they need ordering?** A: They need *latest* state, not *all* states — a delayed "position: x" is garbage; a newer one supersedes it. TCP's ordered retransmission causes head-of-line stalls ("rubber-banding"), so games send each tick independently and drop stale data. Ordering is only reconstructed where it matters (chat, spawn events).
5. **Q: What is a "UDP hole punching" NAT technique?** A: Both peers `connect()` to a rendezvous server that learns their public (IP, port); then each sends a datagram to the other's public tuple, opening NAT mappings; subsequent packets flow directly. It works *because* UDP is stateless enough that NATs open mappings on outbound sends. This powers P2P games, WebRTC, and Tor-like setups.
6. **Q (tricky): What happens if a UDP datagram is sent larger than the reassembly buffer?** A: Reassembly fails, the fragments are timed out and discarded; the app sees loss. This is why the "UDP payload ≤ MTU" rule matters — plus many middleboxes drop fragments entirely (they can't track reassembly cheaply).

## 15. Coding Example
```python
# UDP echo — datagram semantics in code (RFC 862 style)
import socket

# ---- Server: ONE socket serves unlimited clients ----
srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
srv.bind(("0.0.0.0", 9000))          # no listen(), no accept()
while True:
    data, addr = srv.recvfrom(2048)  # addr = (ip, port) of sender
    print(f"Got {len(data)}B from {addr}")
    srv.sendto(data, addr)           # reply to that exact sender

# ---- Client: fire-and-forget, then wait with timeout ----
cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli.settimeout(1.0)                  # app-level reliability
msg = b"hello udp"
cli.sendto(msg, ("127.0.0.1", 9000)) # no connect() needed
try:
    reply, _ = cli.recvfrom(2048)    # may never arrive!
    print("Echo:", reply)
except socket.timeout:
    print("No reply — retry is the app's job")
```
```bash
# Measure UDP throughput & loss (the standard tools)
$ iperf3 -u -c 10.0.0.5 -b 10M -t 10       # client: 10 Mbps for 10 s
$ iperf3 -s -u                             # server: prints loss/latency stats
# Watch the datagrams + checksum, no handshake anywhere:
$ sudo tcpdump -i eth0 udp and port 9000 -nn -vv
#   10.0.0.5.45000 > 10.0.0.5.9000: UDP, length 7
```

## 16. Industry Usage
- **DNS infrastructure (BIND, Unbound, Cloudflare 1.1.1.1)**: UDP 53 is the default; DoT/DoH move to TCP/TLS, DoQ to QUIC.
- **WebRTC (Google Meet, Zoom, Teams)**: SRTP over UDP + DTLS-SRTP; adaptive bitrate via RTCP.
- **Gaming (Fortnite, CS2, CoD)**: custom UDP protocols with client-side prediction + server reconciliation; ENet, RakNet, GameNetworkingSockets.
- **QUIC (HTTP/3)**: the world's biggest new "UDP app" — Chrome/Edge/Safari/Firefox, YouTube, Google, Cloudflare, Akamai all serve HTTP/3 over UDP/443.
- **Telemetry & control planes**: NTP (123), SNMP (161), syslog (514), VXLAN (4789), WireGuard (51820), QUIC (443) — every low-latency control protocol picks UDP.
- **CDN & live streaming**: Low-latency HLS/LL-DASH over WebRTC (UDP) for interactive live; SRT (secure reliable transport) wraps UDP with app-level reliability for high-latency public networks.
- **Cloud NAT/DDoS**: UDP is the top protocol for reflection/amplification DDoS (DNS/NTP/SSDP), which is why cloud firewalls default-block most UDP except 443.

## 17. References
- RFC 768 — UDP: https://www.rfc-editor.org/rfc/rfc768
- RFC 3828 — UDP Lite: https://www.rfc-editor.org/rfc/rfc3828
- RFC 5348 — TCP-Friendly Rate Control (TFRC) for UDP congestion: https://www.rfc-editor.org/rfc/rfc5348
- RFC 3550 — RTP (real-time UDP media): https://www.rfc-editor.org/rfc/rfc3550
- RFC 9000 — QUIC (a UDP-based transport): https://www.rfc-editor.org/rfc/rfc9000
- Kurose & Ross, *Computer Networking*, Ch. 3 (UDP section).
- Linux man: `udp(7)`, `ip(7)`, `sendto(2)`, `recvfrom(2)`.

## 18. Cheat Sheet
- Header: 8B = src(16) dst(16) len(16) cksum(16).
- Max payload: 65507; safe no-frag payload: 1472 @ MTU 1500.
- Connectionless: no handshake, no ACK, no retransmit, no order.
- Guarantees: nothing but checksummed, port-delivered datagrams.
- Checksum: pseudo-header (IPs + proto + len) + UDP + data; IPv6 mandatory.
- Uses: DNS, DHCP, NTP, SNMP, TFTP, syslog, RTP/WebRTC, games, QUIC, VXLAN, WireGuard.
- "Connected" UDP = `connect()` stored peer, still no connection.
- Reliability is the app's job (timeout+retry) or refused (real-time).
- Closed port → ICMP port-unreachable (UDP socket silent unless connected).
- Fragmentation (IPv4 by routers, IPv6 at source) = DoS vector; keep ≤ MTU.

## 19. Quiz
1. UDP header size: a) 20 B b) 8 B c) 40 B d) 12 B → **b**
2. UDP guarantees: a) ordering b) delivery c) checksummed delivery to a port d) all → **c**
3. Practical no-frag payload @ 1500 MTU: a) 65507 b) 1472 c) 1500 d) 65535 → **b**
4. The pseudo-header contains: a) ports only b) IPs + protocol + len c) MAC d) nothing → **b**
5. Which uses UDP: a) DNS queries b) HTTPS c) SSH d) SMTP → **a**
6. QUIC runs over: a) TCP b) a new IP protocol c) UDP d) raw sockets → **c**
7. Closed UDP port yields: a) RST b) ICMP port-unreachable c) nothing ever d) retransmit → **b**
8. IPv6 UDP checksum: a) optional b) mandatory c) not used d) 32-bit → **b**
9. "Connected" UDP socket: a) has a handshake b) stores the peer c) is reliable d) needs listen → **b**
10. Who handles UDP retransmission? a) the kernel b) TCP c) the application d) the router → **c**

## 20. Flashcards
- **Q: UDP header fields?** → **A:** src port, dst port, length, checksum (8 B).
- **Q: UDP's single guarantee?** → **A:** checksummed, port-delivered datagrams.
- **Q: Why no handshake?** → **A:** connectionless; saves RTT; app controls reliability.
- **Q: Max UDP payload?** → **A:** 65507 B; 1472 B safe at MTU 1500.
- **Q: What is the pseudo-header?** → **A:** IPs + protocol + UDP len, for end-to-end integrity.
- **Q: Why QUIC on UDP?** → **A:** passes through kernels/NATs/firewalls; no new IP protocol needed.
- **Q: Real-time media's protocol?** → **A:** UDP (RTP) — late data is useless.

## 21. Revision
UDP = connectionless datagram transport: 8-byte header (src/dst port, length, checksum), no handshake/order/reliability/congestion control, checksum over pseudo-header+header+data (mandatory in IPv6). One socket serves unlimited senders (stateless scale). Used by DNS/DHCP/NTP/SNMP/TFTP/syslog, RTP/WebRTC/games (real-time), and QUIC (UDP as a deployment trick for new transports). Closed port → ICMP unreachable. Max payload 65507; fragmentation is a DoS vector — keep ≤ MTU. Reliability, when needed, lives in the app (DNS retry, QUIC, WebRTC FEC). Measure with iperf3/tcpdump.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is UDP and what does it guarantee?" | 2 How It Works / 7 Formal Definition |
| "Why is DNS over UDP?" | 3 When Is It Used / 13 Q&A |
| "Why did QUIC choose UDP?" | 13 Q&A / 4 Why Not Another Approach |
| "What is the UDP header / max payload?" | 2 How It Works / 13 Q&A |
| "What is the pseudo-header for?" | 9 Internal Working / 13 Q&A |
| "UDP vs TCP — when to pick?" | 13 Q&A / 3 When Is It Used |
| "How does UDP handle congestion?" | 14 Follow-Up / 12 Disadvantages |
| "Is video really over UDP?" | 13 Q&A / 16 Industry Usage |
