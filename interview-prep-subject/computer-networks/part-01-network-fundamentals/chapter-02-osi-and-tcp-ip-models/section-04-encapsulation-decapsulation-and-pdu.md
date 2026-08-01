# Encapsulation, Decapsulation, and PDU

> **TL;DR**: Encapsulation is how each layer adds its own header to the data as it travels down the stack (data → segment → packet → frame → bits), and decapsulation is the reverse unwrapping at the destination — this PDU chaining is the *mechanism* that lets layered protocols work together.

## 1. Why Does This Exist?
Layering only works if layers can *pass data to each other*. Encapsulation is the answer: as data descends the stack, each layer wraps the received unit with **its own header** (control info the peer layer needs — addresses, ports, checksums, sequence numbers), producing its own PDU. This exists because:
1. **Peer-to-peer communication needs per-layer metadata**: TCP needs ports/seq numbers, IP needs addresses/TTL, Ethernet needs MAC/CRC. Each belongs in a *separate* header read only by the matching layer on the other side.
2. **Modularity**: a layer can change its header format without breaking layers above/below (e.g., IPv4→IPv6: only the IP header changes).
3. **Multiplexing/demultiplexing**: the type fields (Ethertype, IP protocol, TCP port) tell each layer which upper-layer protocol to hand data to.

## 2. How Does It Work?
The **PDU chain** (protocol data unit at each layer):
- **Application**: message/Data (HTTP request)
- **Transport**: **Segment** (TCP) or **Datagram** (UDP) = TCP header + app data
- **Internet**: **Packet** (IP datagram) = IP header + segment
- **Link**: **Frame** = link header (MAC) + packet + link trailer (CRC/FCS)
- **Physical**: **Bits** on the wire

Encapsulation = "add a header going down." Decapsulation = "strip a header going up." Each layer treats everything above it as opaque *payload*. The destination peer for a header is the *same layer* on the far end — but intermediate devices may act too: routers strip/add *link* headers at every hop (they must, to forward between links) but leave the IP packet intact.

## 3. When Is It Used?
- **Every single packet on the Internet**: a web request, email, DNS query, video stream — all are encapsulated/decapsulated at every hop.
- **Tunnels (VPNs, VXLAN, GRE)**: encapsulation *of the same or higher layers* — IP-in-IP, Ethernet-in-UDP, TCP-in-TCP — used to carry private traffic across public networks, to build overlays, or to traverse NATs.
- **Protocol stacks in the kernel**: Linux `sk_buff` holds headers at every layer; NIC drivers add/remove Ethernet header; IP/TCP code adds/removes their headers.
- **Middleboxes**: NAT rewrites IP (L3) + port (L4) headers; proxies terminate and re-encapsulate entire connections.

## 4. Why Wasn't Another Approach Chosen?
Alternatives to header-based encapsulation:
- **Out-of-band signaling** (metadata sent separately, e.g., control channel): rejected — fragile (must stay in sync), harder to route, doubles the failure surface. Headers keep control info with the data it governs.
- **Connection state at every router** (no per-packet headers, routers track flows): rejected — violates statelessness/end-to-end; routers would need to remember every flow, breaking scale and making failures complex. Headers make packets *self-describing*: any router can forward without prior state.
- **One global header format** (single encapsulation for all layers): rejected — no layering modularity; changing addressing would rewrite everything. Nested headers give each layer independence.
- **Fixed-length headers only**: rejected — options fields (TCP options, IP options, MPLS labels) allow extensibility; fixed-only would block evolution (this is why IPv4 has variable-length options and IPv6 removed most of them for simplicity).

## 5. Intuition
Encapsulation is **Russian nesting dolls / envelopes within envelopes**. You write a letter (application data). You put it in an envelope addressed to the *person* (transport: port/process). That envelope goes into a larger envelope addressed to the *city* (network: IP address). That goes into a crate labeled with the *street address* (link: MAC). At each stop, someone opens only *their* envelope and forwards the rest. The recipient opens envelopes in reverse order until the letter is revealed. Each layer reads only its own envelope's address and leaves the inner contents untouched — that's the essence of the design.

## 6. Real-World Analogy
**The international shipping container**: Your product (HTTP data) is packed in a box labeled with the receiver's *name* (port — which person in the building). The box goes in a shipping container labeled with the *destination city* (IP address). The container sits on a truck with a *local plate and driver manifest* (MAC address on the link). At each port, workers check the container's label (router reads IP) and load it onto the next truck; the inner box's name label isn't touched until the final destination. The truck manifest (link header) changes at every leg; the container label (IP header) stays until the endpoint; the name label (port) opens at the destination process.

## 7. Formal Definition
**Encapsulation** is the process by which a protocol at layer N wraps the PDU received from layer N+1 in its own header (and, at the data link layer, trailer) to produce layer-N's PDU. **Decapsulation** is the reverse — stripping the header at the destination peer. The PDU at layer N, together with the protocol used, is identified to the peer by the layer-below's *type* field (e.g., Ethertype 0x0800 = IPv4, IP protocol 6 = TCP, TCP port 443 = HTTPS). Headers are read only by the peer layer (the "peer-to-peer" principle); intermediate routers typically process only link (L2) and network (L3) headers.

## 8. Example
Full walk: sending an 2000-byte HTTP POST from Host A (192.168.1.10) to Host B (10.0.0.5, MTU 1500):
1. **Application**: HTTP produces ~2000 B body + headers (Message).
2. **Transport (TCP)**: TCP adds 20 B header (ports 54321→80, seq=1000), then **segments** into two MSS-sized pieces because 2000+20 > MSS(1460): Segment 1 = seq 1000 (1460 B payload), Segment 2 = seq 2460 (540 B payload). Each = 20 B header + data.
3. **Internet (IP)**: each segment gets a 20 B IPv4 header → two packets of 1480 B and 560 B.
4. **Link (Ethernet)**: each packet + 14 B Ethernet header + 4 B FCS → frames of 1498 B and 578 B (both ≤ MTU 1500). The router's MAC is the next-hop for the destination *IP* (ARP resolved it).
5. **Physical**: frames become bits on the cable.
On the path, Router R strips Ethernet header, reads IP dst (10.0.0.5), does longest-prefix-match, decrements TTL, re-encapsulates in *new* Ethernet header (with the next hop's MAC), forwards. At Host B: Ethernet header stripped (CRC verified) → IP header stripped (checksum verified) → TCP segments reassembled in order (seq continuity) → 2000 B body delivered to the listening process on port 80.

## 9. Internal Working
1. **Socket API**: `send(data)` → kernel copies data into the socket buffer; TCP layer builds segments from it (data + seq/ack, checksum over pseudo-header including IPs).
2. **IP layer** (`ip_queue_xmit` in Linux): looks up route (FIB), builds IP header (version, IHL, total length, ID, flags/frag offset, TTL, protocol, header checksum), prepends to segment.
3. **Link layer / driver** (`dev_queue_xmit`): builds frame (dst/src MAC from ARP/neighbor cache, Ethertype = 0x0800 or 0x86DD for IPv6), appends FCS; NIC card converts to bits.
4. **At each router**: NIC strips Ethernet → `ip_rcv` validates IP header (checksum, TTL) → forwarding decision → `neigh_resolve_output` builds new Ethernet header → next NIC transmits. IP packet *untouched* except TTL/checksum.
5. **At destination**: NIC delivers frame → link layer strips Ethernet → IP layer strips IP → `tcp_v4_rcv` demuxes by (src/dst IP + ports) to the socket → TCP strips header, updates state, delivers bytes to app buffer → app `recv()` reads the 2000 B body.
6. **Key detail — checksums**: IP checksum covers only the IP header; TCP checksum covers TCP header + payload + a *pseudo-header* (IPs + protocol + length). Ethernet CRC covers the whole frame. Errors caught at link are dropped silently (end-to-end repair via TCP).

## 10. Time Complexity
- **Encapsulation cost**: O(header size) constant per layer — adding/removing 20-40 B headers is O(1).
- **Copy cost** (real-world "cost of layering"): zero-copy kernels (sendfile, MSG_ZEROCOPY, io_uring) exist precisely to avoid copies; naive stacks copy at each layer → O(layers × packet size).
- **Checksums**: TCP checksum O(n) in segment size — computed in hardware (checksum offload) on modern NICs → effectively O(1) per byte with hardware assist.
- **Header overhead ratio**: 40 B per 1460 B payload ≈ 2.7%; tiny packets (IoT) suffer far worse ratios.

## 11. Advantages
- **Modularity**: change one layer's format without touching others (IPv4→IPv6).
- **Peer isolation**: each layer reads only its own header → independent evolution.
- **Multiplexing**: type fields let one link carry many protocols; one IP host runs thousands of apps via ports.
- **Stateless forwarding**: packets are self-describing → routers forward without per-flow state (scale).
- **Tunneling**: encapsulation enables VPNs, overlays (VXLAN), and encapsulation-based security (IPsec ESP).

## 12. Disadvantages
- **Overhead**: per-packet header bytes (especially small packets) waste bandwidth; deep nesting (VXLAN-in-UDP-in-IP) shrinks MTU and adds CPU.
- **Fragmentation complexity**: large payloads must be split at L4 (segmentation) and possibly L3 (fragmentation); fragments add overhead and risk (IPv4 in-path fragmentation is notorious; IPv6 bans it).
- **Limited transparency**: middleboxes must parse headers; header modifications (NAT, QoS DSCP rewrites) can break end-to-end integrity (NAT breaks IPsec unless NAT-T).
- **Hiding bugs**: because headers are per-layer, a corrupt *payload* may pass link CRC (only header covered) and get caught only at TCP — wasted bandwidth.

## 13. Interview Questions
1. **Q: What is encapsulation?** A: Each layer wraps the upper-layer PDU with its own header (+ trailer at L2), producing its own PDU as data descends the stack — so a message accumulates headers: data → segment → packet → frame → bits.
2. **Q: Name the PDU at each layer.** A: L7-5: message/data; L4: segment (TCP) or datagram (UDP); L3: packet; L2: frame; L1: bits.
3. **Q (tricky): Does a router decapsulate all the way to the application?** A: No. It strips and re-adds only the *link* header (to forward between links) and processes the *network* header (IP, TTL). It does NOT touch the TCP header or payload. Deep inspection (DPI, NAT at L4) is optional and unusual for core routers.
4. **Q: What happens to a packet's IP header as it traverses routers?** A: It stays intact except TTL (decremented) and header checksum (recomputed). The link headers are completely replaced at every hop. This is why "same IP header, fresh frame each hop."
5. **Q (production): Why is the TCP checksum computed over a pseudo-header?** A: To detect *misdelivery*: it covers source/dest IPs, protocol, and length, so if a packet is delivered to the wrong host (e.g., by a routing error), the TCP checksum fails even though the payload is intact. Cheap end-to-end integrity.
6. **Q: What is fragmentation vs segmentation?** A: Segmentation = L4 splitting the byte stream to fit MSS (e.g., 2000 B → 1460+540). Fragmentation = L3 splitting an already-formed packet to fit a link MTU (e.g., 1480 B IP packet into two over an MTU-576 link). Segmentation is end-to-end; IPv4 fragmentation can recur per hop; IPv6 forbids in-path fragmentation (Path MTU Discovery).
7. **Q (scenario): MTU is 1500, application sends 3000 B. Trace the encapsulation.** A: TCP segments to ≤1460 B payload → 2-3 segments (MSS = 1460 with 40 B headers). Each gets 20 B IP header → packets ≤1500 B → each fits one Ethernet frame (14 B hdr + 4 B FCS). If a link had MTU 576, IP would fragment packets further.
8. **Q: What is the Ethertype / protocol-type field for?** A: Demultiplexing: Ethertype (0x0800 IPv4, 0x86DD IPv6, 0x8100 VLAN) tells the receiver which network-layer protocol the frame carries; the IP "protocol" field (6=TCP, 17=UDP, 1=ICMP) tells which transport; the port tells which app. This is how one link multiplexes all protocols.
9. **Q: What is a PDU vs an SDU?** A: SDU (service data unit) = the data handed *to* a layer (the payload). PDU = SDU + the layer's own header. Encapsulation converts SDU→PDU going down; decapsulation converts PDU→SDU going up.
10. **Q (tricky): In an IP-in-IP tunnel, how many IP headers are on the wire?** A: Two: the outer (encapsulating, routed by the network) and inner (original, protected/private). The outer destination is the tunnel endpoint; the inner is the true destination. This is exactly how GRE, IPsec tunnel mode, and VXLAN work.
11. **Q: Why did IPv6 remove in-path fragmentation?** A: Because fragmentation is expensive, error-prone, and used as a DDoS/evasion vector. IPv6 requires Path MTU Discovery (ICMPv6 "Packet Too Big"); routers drop oversize packets and signal. Simpler, cleaner — a design lesson.
12. **Q (production): What happens to a frame whose Ethernet FCS/CRC fails?** A: The link layer silently drops it. No retransmission at L2 (except some retry links like Wi-Fi). TCP at the end detects the gap (missing seq) and retransmits — the end-to-end repair model. For UDP, the data is lost.
13. **Q: What is "header overhead" and why do tiny packets hurt?** A: Every packet carries ≥40 B of IP+TCP headers regardless of payload. A 60 B VoIP packet is ~67% overhead; a 1460 B segment is ~2.7%. Small-packet-heavy workloads (IoT, gaming, trading) waste bandwidth and CPU.
14. **Q: How does NAT interact with encapsulation/checksums?** A: NAT rewrites IP addresses, so it must recompute the IP header checksum (and, since TCP's pseudo-header includes IPs, the TCP checksum too — for TCP, NAT updates the checksum via incremental adjustment to avoid full recomputation). This is why NAT breaks protocols that embed IPs in payloads (FTP), requiring ALGs.
15. **Q: What is the purpose of encapsulation for security (IPsec ESP)?** A: ESP encrypts the entire payload + most of the IP header and adds an auth trailer — a form of encapsulation that gives confidentiality + integrity. Tunnel mode encapsulates the *whole* original IP packet inside a new IP packet (IP-in-IP), hiding internal addresses.
16. **Q (FAANG): Why can't you reliably infer the application protocol from the transport header alone?** A: Because the payload (app data) isn't parsed at L4, and ports can be reused/nonstandard (routable ports, proxies). Deep inspection needs L7 parsing — another example that encapsulation *hides* semantics from lower layers by design.

## 14. Follow-Up Questions
1. **Q: Why does Wi-Fi have a link-layer retransmission when Ethernet doesn't?** A: Because RF is lossy (errors per frame are common), and Wi-Fi's ACK/retry (802.11) is cheap at link scope — far better than making TCP retransmit across the whole path. Ethernet's wire is reliable, so it relies on end-to-end TCP. Link-layer retry is a *per-technology* choice.
2. **Q: What is Path MTU Discovery (PMTUD) and the MSS clamping hack?** A: PMTUD (RFC 1191, 8201) uses ICMP "Packet Too Big" to learn the min MTU along a path. When ICMP is blocked (common behind NAT), MTU issues cause black-holing — the production fix is *MSS clamping* (TCP option rewritten to fit the tunnel MTU).
3. **Q: How does GRO/GSO (Generic Receive/Segmentation Offload) interact with encapsulation?** A: The NIC coalesces/splits packets to amortize headers — this *bypasses* strict per-packet encapsulation costs but must preserve checksum/segmentation semantics, which is why kernels carefully verify offload features before trusting them.
4. **Q: What are "double tags" (Q-in-Q) in 802.1ad?** A: Service-provider encapsulation: a second VLAN tag wraps a customer's tagged frame — an L2 form of encapsulation that lets ISPs carry customers' VLANs over their own infrastructure. Same principle as IP-in-IP, one layer down.
5. **Q: What is "TCP encapsulation in TCP" and why is it a problem?** A: Tunnels like SSH SOCKS or some VPNs run TCP over TCP; the outer TCP retransmits on loss, and the inner TCP sees those delays as congestion and reduces its window → "TCP meltdown" (head-of-line blocking doubled). Correct designs run tunnels over UDP (WireGuard, QUIC) — a favorite FAANG "gotcha."

## 15. Coding Example
```python
# Manual encapsulation/decapsulation simulation with real header bytes
import struct

def encap(protocol, header_bytes, payload):
    return {"protocol": protocol, "headers": header_bytes + payload}

# Simulate: HTTP message -> TCP segment -> IP packet -> Ethernet frame
http  = b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
tcp_hdr = struct.pack(">HHII", 54321, 80, 1000, 1)      # src,dst,seq,ack
ip_hdr  = struct.pack(">BBHBBH", 0x45, 0, 0, 64, 6, 0)  # v4/IHL/TTL/proto
eth_hdr = b"\xaa\xbb\xcc\xdd\xee\xff" + b"\x00\x11\x22\x33\x44\x55" + b"\x08\x00"

frame = eth_hdr + ip_hdr + tcp_hdr + http          # encapsulate down the stack
print(f"Frame size: {len(frame)} bytes, payload 'visible' only after full decap")

# Decapsulation (destination): strip in reverse order
assert frame[12:14] == b"\x08\x00"                  # Ethertype says IPv4
packet = frame[14:]
assert packet[9] == 6                                # IP protocol = TCP
segment = packet[20:]
src_port, dst_port = struct.unpack(">HH", segment[0:4])
print(f"TCP segment: src={src_port} dst={dst_port}")
app_data = segment[20:]
print(f"Application payload: {app_data!r}")
```
```
# tcpdump - a live encapsulation walk: headers shown at each layer
$ tcpdump -nn -vvv -c 1 'tcp port 80'
# 22:31:00.123 IP (tos 0x0, ttl 64, id 1234, proto TCP (6), length 74)   <- IP header
#     192.168.1.10.54321 > 93.184.216.34.80: Flags [P.], cksum 0x12ab (incorrect)  <- TCP header
#     Data (54 bytes)                                                      <- HTTP payload
```

## 16. Industry Usage
- **Kubernetes/CNI overlays**: VXLAN encapsulates Ethernet frames in UDP/IP so pods across nodes share one L2 domain — a giant production example of encapsulation (VXLAN = L2 over UDP over IP).
- **VPN products**: WireGuard (UDP), IPsec tunnel mode (IP-in-IP + ESP), and enterprise SD-WAN all rely on encapsulation to provide privacy and private addressing over public networks.
- **Cloud LBs**: AWS NLB (L4) reads TCP headers; ALB (L7) terminates TLS then re-encapsulates on the way to targets — decap/re-encap at scale (millions of conns).
- **The Linux networking stack**: `sk_buff` (socket buffer) literally stores each layer's header; eBPF programs (XDP/TC) inspect/rewrite headers *inside* the encapsulation path — the modern way to manipulate PDUs in production.
- **Service mesh (Istio/Envoy)**: L7 proxies terminate and re-encapsulate requests, adding headers — "encapsulation as a service" for tracing, auth, and routing.

## 17. References
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, 8th ed., Ch. 1.5.1 (Encapsulation, Fig. 1.26).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 1.4 (PDUs / encapsulation).
- RFC 791 (IPv4 header) — https://www.rfc-editor.org/rfc/rfc791
- RFC 8200 (IPv6, no in-path fragmentation) — https://www.rfc-editor.org/rfc/rfc8200
- RFC 1191 / RFC 8201 (Path MTU Discovery) — https://www.rfc-editor.org/rfc/rfc1191
- RFC 7348 (VXLAN) — https://www.rfc-editor.org/rfc/rfc7348
- RFC 8666 / GRE — RFC 2784.

## 18. Cheat Sheet
- PDU chain: data/message → segment (TCP) / datagram (UDP) → packet → frame → bits.
- Encapsulation: add header going DOWN; decapsulation: strip going UP.
- SDU = payload handed to layer; PDU = SDU + that layer's header.
- Routers strip/add only LINK headers; IP header persists (TTL + checksum change).
- Type fields demultiplex: Ethertype (0x0800 IPv4), IP protocol (6=TCP), ports.
- TCP checksum covers pseudo-header (IPs) → catches misdelivery.
- IPv6 forbids in-path fragmentation → PMTUD.
- Tunnels = encapsulation of same/higher layers (IP-in-IP, VXLAN-in-UDP, TCP-in-TCP → meltdown).
- Segmentation = L4 (MSS); fragmentation = L3 (MTU).

## 19. Quiz
1. PDU at L4: a) frame b) packet c) segment d) bits → **c**
2. Which header does a router replace at every hop? a) IP b) TCP c) Ethernet d) HTTP → **c**
3. SDU stands for: a) service data unit b) segment data unit c) source delivery unit d) serial data → **a**
4. Ethertype 0x0800 means: a) IPv6 b) IPv4 c) ARP d) VLAN → **b**
5. IP protocol field 6 means: a) UDP b) TCP c) ICMP d) IGMP → **b**
6. IPv6 handles MTU via: a) in-path fragmentation b) PMTUD/ICMPv6 c) no mechanism d) link retry → **b**
7. TCP checksum covers: a) header only b) payload only c) pseudo-header+header+payload d) nothing → **c**
8. A frame with bad CRC is: a) retransmitted b) silently dropped c) repaired d) sent to app → **b**
9. VXLAN encapsulates: a) IP in TCP b) Ethernet in UDP c) TCP in IP d) HTTP in TLS → **b**
10. TCP-over-TCP tunnels cause: a) faster transfer b) "TCP meltdown" c) no issue d) less overhead → **b**

## 20. Flashcards
- **Q: PDU chain top→bottom?** → **A:** Data → segment/datagram → packet → frame → bits.
- **Q: What does a router strip and add?** → **A:** Link headers; IP header persists (TTL/checksum updated).
- **Q: SDU vs PDU?** → **A:** SDU = payload in; PDU = SDU + header out.
- **Q: Why pseudo-header in TCP checksum?** → **A:** Detect misdelivery (wrong IP/port) end-to-end.
- **Q: Segmentation vs fragmentation?** → **A:** L4 MSS split vs L3 MTU split (IPv6: no in-path frag).
- **Q: What is TCP-over-TCP meltdown?** → **A:** Nested retransmit/congestion feedback collapse — why tunnels use UDP.
- **Q: What is VXLAN?** → **A:** Ethernet frames carried in UDP/IP overlays (L2 over L3).

## 21. Revision
Encapsulation is the mechanism behind layering: every layer wraps the upper PDU with its own header going down (data → segment → packet → frame → bits) and unwraps going up. SDU = payload, PDU = SDU + header. Routers only swap link headers; the IP header persists (TTL + checksum change). Type fields (Ethertype, IP protocol, ports) demultiplex. TCP's pseudo-header catches misdelivery. IPv6 bans in-path fragmentation (use PMTUD). Tunnels (IP-in-IP, VXLAN-in-UDP) are encapsulation; avoid TCP-in-TCP (meltdown).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is encapsulation and the PDU chain?" | 2 How It Works / 13 Q&A |
| "What does a router strip/keep?" | 9 Internal Working / 13 Q&A |
| "Why pseudo-header in TCP checksum?" | 13 Q&A / 9 Internal Working |
| "Segmentation vs fragmentation?" | 13 Q&A / 7 Formal Definition |
| "How do tunnels work?" | 3 When Used / 13 Q&A |
| "Why no IPv6 fragmentation?" | 11 Advantages / 13 Q&A |
| "What happens to a corrupt frame?" | 13 Q&A / 9 Internal Working |
