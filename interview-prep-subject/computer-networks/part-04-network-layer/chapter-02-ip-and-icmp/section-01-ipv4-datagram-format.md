# IPv4 Datagram Format

> **TL;DR**: The IPv4 datagram's 20-byte (up to 60) header is IP's contract on the wire — version/IHL, TOS + ECN, total length, identification + fragment fields, TTL, protocol, header checksum, and src/dst addresses; fragmentation splits oversized packets at MTU boundaries and the fields make reassembly deterministic.

## 1. Why Does This Exist?
The network layer needs a *packet format* that lets routers do exactly one thing fast — forward: read the destination, decide the next hop, decrement, and move on — while preserving enough metadata for the receiver (end-to-end), the transport (protocol demux), and the network (fragmentation, QoS, loop bounding). Every field exists to answer a specific operational question: "which version?" (version), "how long is the header?" (IHL), "is it urgent/QoS?" (TOS), "how big?" (total length), "is this a fragment and which one?" (ID, flags, offset), "is this packet still alive?" (TTL), "which protocol owns the payload?" (protocol), "did the header get corrupted in transit?" (header checksum), "who sent/receives?" (src/dst). Understanding the datagram *is* understanding IP's design — the fixed 20-byte core, the fragile checksum, the TTL semantics, and the fragmentation machinery are all interview staples because they're the visible surface of how the whole Internet forwards.

## 2. How Does It Work?
Header layout (20 bytes minimum):
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if IHL > 5)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
- **Version (4b)**: 4 = IPv4 (6 = IPv6).
- **IHL (4b)**: header length in 32-bit words (5 = 20 bytes, up to 15 = 60).
- **Type of Service / DSCP + ECN (8b)**: differentiated services (QoS class) + explicit congestion notification bits (ECT/CE).
- **Total Length (16b)**: header + payload, up to 65535 bytes.
- **Identification (16b)**: datagram ID — same ID on all fragments of one packet.
- **Flags (3b)**: DF (don't fragment), MF (more fragments follow), reserved.
- **Fragment Offset (13b)**: where this fragment's data starts, in 8-byte units.
- **TTL (8b)**: max hops (decremented each router; 0 → drop + ICMP time-exceeded).
- **Protocol (8b)**: payload owner: 1=ICMP, 2=IGMP, 6=TCP, 17=UDP, 89=OSPF, 47=GRE.
- **Header Checksum (16b)**: ones'-complement over just the *header* (recomputed per hop because TTL changes).
- **Source/Destination (32b each)**: addresses.

## 3. When Is It Used?
- **Every packet, always**: every IP datagram carries this header; `tcpdump -nn -vv` prints it; Wireshark dissects it.
- **Fragmentation**: when a datagram > MTU (e.g., 4000-byte UDP payload on a 1500 link) → split into fragments with same ID, MF flags, offsets; the destination reassembles.
- **QoS/ECN**: DSCP marks traffic classes (real-time, bulk); ECN marks congestion without dropping (see TCP congestion control).
- **TTL-based tooling**: `ping` (echo TTL), `traceroute` (crafted TTLs), and the "TTL exceeded" path map.
- **Header checksum debugging**: `netstat -s`/`ip -s` counters show checksum errors; corrupted headers are dropped silently.
- **Protocol demux**: the Protocol field tells the receiver's stack which handler (TCP/UDP/ICMP/OSPF) gets the payload — the network-layer "port" concept.
- **Security**: firewall rules inspect fields (protocol, TTL, DF); fragmentation abuse (frag floods, evasions) is a firewall/DDoS topic.

## 4. Why Wasn't Another Approach Chosen?
- **Why 20-byte fixed core + optional options?** Common-case forwarding must be cheap — routers read a *fixed* 20-byte area (no variable-offset scans). Rare needs (source route, timestamps, record route) are *options*, processed only by nodes that care. This "fast path + slow path" split is why IP survives at line rate.
- **Why a header checksum but no payload checksum?** IP's job is delivery, not integrity — the transport (TCP/UDP) checks payloads end-to-end. The *header* must be validated at every hop (a corrupt dest/TTL would misroute), and it's recomputed cheaply per hop. Payload checksums belong at the transport layer, not duplicated.
- **Why TTL as "time-to-live" but actually hop count?** Originally time-based (seconds); routers decrement by ≥1 and it became de-facto hop count. It bounds routing loops — a packet can't circulate forever. A hop limit (IPv6 formalizes it) is the cleanest loop control; the name is legacy.
- **Why fragmentation in the network (IPv4) vs only at the source (IPv6)?** IPv4 routers fragment because the path MTU was unknown (path-MTU discovery came later and still needs fallback). It works but costs: reassembly buffers, frag-based DoS, and the "one lost fragment kills the whole datagram" problem. IPv6's redesign made routers never fragment — a deliberate fix of an IPv4 wart.
- **Why the Protocol field instead of relying on ports?** Ports are transport-layer; a router (or firewall) needs to know the *payload type* without parsing the transport — 1 byte, unambiguous, demuxes the network layer. It's IP's equivalent of a "type" field.
- **Why 16-bit total length / 65535 max?** Ample for 1981 (LANs were <1500, WANs <4KB); the real ceiling is MTU + fragmentation, not the field. IPv6 moved payload length to the header for the same reason.

## 5. Intuition
The datagram header is a **shipping label on a parcel**: "This is parcel format version 4 (Version), the label is 20 lines (IHL), the weight class is 'express' (TOS), the total weight is 1,500 g (Total Length), the parcel serial number is #4821 (Identification), it's split into 3 boxes — this is box 2 of 3 (Flags + Offset), the parcel must pass through at most 64 sorting hubs (TTL), the handler is 'TCP' (Protocol), and here's a checksum of the label itself so hubs can verify the label wasn't smudged (Header Checksum). From: A. To: B." Every sorting hub (router) reads the label, checks it, decrements the hub count, and sends it onward without opening the parcel — that's exactly why the header is fixed-length, checked, and hop-bounded.

## 6. Real-World Analogy
**An international courier's air waybill**: The 20-byte header is the *machine-readable label* that every hub scans in milliseconds. Version = "air freight standard v4"; IHL = "label is 20 lines"; the shipping class (TOS/ECN) = "priority or economy"; Total Length = "this shipment weighs 1,500 units"; the barcode (Identification) + "box 2 of 3" (MF/Offset) lets the destination piece together a large shipment split across several trucks on a narrow road (MTU). TTL = "max 64 hops — a lost parcel can't loop the world forever"; Protocol = "content handler: dangerous goods (TCP), documents (UDP), customs (ICMP)"; the label checksum = a digit that lets each hub verify the label wasn't garbled (otherwise the parcel is misrouted — better to discard and let the sender resend). Source/Destination = the sender and receiver address. Every field maps to a real operational question the courier (router) answers per parcel.

## 7. Formal Definition
The IPv4 datagram (RFC 791, updated by RFC 6864) is the network-layer PDU: a variable-length header (minimum 20 bytes; IHL × 32 bits) followed by payload. Fields: Version (4), IHL (4), Differentiated Services (RFC 2474: DSCP 6 bits + ECN 2 bits, RFC 3168), Total Length (16, ≤ 65535), Identification (16, per-datagram fragment group), Flags (3: DF, MF), Fragment Offset (13, in 8-byte units), TTL (8, decremented per hop; 0 → discard + ICMP time-exceeded), Protocol (8: 1 ICMP, 6 TCP, 17 UDP, etc.), Header Checksum (16, ones' complement over the header, recomputed at each hop), Source and Destination addresses (32 each), and Options (IHL−5 words). Fragmentation: when packet > outgoing MTU and DF unset, split into fragments sharing ID, MF, and increasing offsets; reassembled at the destination (RFC 815).

## 8. Example
A real datagram, decoded:
```
$ sudo tcpdump -nn -i eth0 'icmp' -vv
IP (tos 0x0, ttl 64, id 4821, offset 0, flags [DF], proto ICMP (1),
    length 84)
    192.168.1.5 > 8.8.8.8: ICMP echo request, id 1000, seq 1, length 64
```
Reading the fields: ttl 64 (Linux default, 64−hops remaining), id 4821, offset 0 + flags [DF] = first and only fragment (don't fragment — the ICMP payload is small, no need), proto ICMP (1), length 84 (20-byte header + 64-byte payload), src 192.168.1.5, dst 8.8.8.8. On the return, `ttl` will be lower (8.8.8.8 sends ttl 128/64 or the path's actual hop count), letting `ping` show the round trip and TTL as a health signal.

Fragmentation example:
```
4,000-byte UDP datagram on a 1,500-byte MTU path:
  Fragment 1: id=100, MF=1, offset=0,   length 1500 (20+1480 payload)
  Fragment 2: id=100, MF=1, offset=185, length 1500 (20+1480 payload)  (185 = 1480/8)
  Fragment 3: id=100, MF=0, offset=370, length 1060 (20+1040 payload)
  Offsets are in 8-byte units → the receiver reassembles 1480+1480+1040 = 4000 bytes.
```

## 9. Internal Working
1. **Receive**: NIC → IP layer parses the fixed 20-byte header (checks IHL, total length, version); validates the header checksum — mismatch → drop (counter). Reads protocol → hands payload to TCP/UDP/ICMP/OSPF handler.
2. **Forward**: router looks up dst in the FIB (longest-prefix match) → next hop; **decrements TTL**; **recomputes the header checksum** (it changed with TTL); decrements total length only at reassembly, not forwarding; sends on the next link (possibly re-fragmenting if the next MTU is smaller and DF unset).
3. **TTL=0** at a router → discard + send ICMP time-exceeded back to the source (that's how traceroute works).
4. **Fragmentation**: sender or router splits a packet > MTU: each fragment carries the same ID, the MF flag (set on all but the last), and an offset (payload start / 8). The destination buffers fragments in a reassembly queue (RFC 815) keyed by (src, dst, protocol, ID); when a fragment with MF=0 arrives and all offsets are covered → reassemble → deliver. A timeout (default ~2-60 s) discards partial datagrams.
5. **DF + PMTU discovery**: with DF set, an oversized packet is dropped and the router sends ICMP "fragmentation needed" with its MTU → the sender lowers its MSS/segment size (path-MTU discovery, RFC 1191). This is how TCP avoids fragmentation entirely.
6. **ECN**: if ECN negotiated, routers can set the CE bit (instead of dropping); the receiver echoes to the sender (TCP ECE/CWR — see part-03 congestion control).
7. **Options**: e.g., record-route (path echo), source route (loose/strict — *now disabled* for security), timestamp — rarely used, mostly stripped/dropped by modern stacks due to abuse.

## 10. Time Complexity
- **Forwarding**: O(1) fixed-header parse + trie/TCAM lookup; header checksum is O(header words) (recomputed per hop, ~20 bytes — trivial). This is why IP is line-rate friendly.
- **Fragmentation**: O(fragments) at the splitter, O(1) per fragment at reassembly (hash on ID). Reassembly buffering is per-datagram memory up to 65 KB.
- **Reassembly DoS**: fragments can exhaust reassembly buffers (frag floods) — a real attack surface; firewalls fragment-rate-limit.
- **TTL loop bound**: worst case a packet travels TTL hops (64-255) before death — the *hard bound* that keeps loops finite.
- **Option parsing**: options force the slow path (variable header) — why they're deprecated in practice and gone in IPv6 (extension headers only).

## 11. Advantages
- **Fixed fast path**: 20-byte core, no variable parsing in the common case → silicon-friendly, line-rate forwarding.
- **Self-contained**: each datagram carries everything it needs (src/dst, protocol, TTL) — stateless, no connection, routers share no state.
- **Fragmentation works**: any-sized payload fits any MTU path (with DF/PMTU as the modern optimization).
- **TTL bounds loops**: a simple, robust loop killer with no router coordination.
- **Protocol multiplexing**: one byte selects TCP/UDP/ICMP/OSPF/… — the layer's "type" field.
- **ECN/DSCP**: congestion marking + QoS classes ride the TOS byte — extensible without new fields.

## 12. Disadvantages
- **Header checksum recomputation per hop**: wastes CPU at every router (IPv6 dropped it entirely).
- **Fragmentation is fragile**: one lost fragment discards the whole datagram; reassembly buffers are a DoS target; frag-based firewall evasion (overlapping fragments) is a classic attack.
- **Options are weak/abused**: variable length forces slow path; source-route options were a security hole and are disabled; almost nothing uses options today.
- **TTL semantics muddled**: "time to live" but actually hops; 8-bit cap (max 255) is fine, but the name confuses.
- **No payload integrity/authenticity**: spoofable source, no anti-replay — IPsec (a bolt-on) is required; IPv4 has no built-in security.
- **Stateless by design**: no path state → asymmetric routing and middlebox fragility (why NAT/LB machinery is so complex).

## 13. Interview Questions
1. **Q: Draw the IPv4 header and label the fields.** A: Version/IHL, TOS(+ECN), Total Length, Identification, Flags (DF/MF), Fragment Offset, TTL, Protocol, Header Checksum, Source, Destination (+ options). 20 bytes minimum.
2. **Q (tricky): What is IHL?** A: Internet Header Length in 32-bit words (5–15): 20–60 bytes. It tells the receiver where the payload starts when options are present.
3. **Q: What does TTL do?** A: Time-To-Live (hop limit): each router decrements it; at 0 the router drops the packet and sends ICMP Time-Exceeded to the source. Bounds routing loops. (Linux sends ttl 64; Windows 128; routers commonly 255.)
4. **Q (FAANG): How does traceroute use the TTL field?** A: It sends probes with TTL=1, 2, 3...; each router at the TTL boundary replies ICMP Time-Exceeded (revealing its address). Sequentially incrementing TTL maps every hop. When the destination responds (echo reply / port unreachable), the path is complete.
5. **Q: What is the Protocol field?** A: Identifies the payload's protocol: 1=ICMP, 2=IGMP, 6=TCP, 17=UDP, 89=OSPF, 47=GRE — the network-layer demux ("which handler"). (0 = IP-in-IP.)
6. **Q: Why does the header checksum exist and why only the header?** A: To catch corruption that would *misroute* (bad dst/TTL/length) at every hop; recomputed per hop because TTL changes. Payload integrity is the transport's job (TCP/UDP checksums end-to-end) — duplicating it in IP would be waste.
7. **Q (tricky): Why is the checksum recomputed at each router?** A: Because TTL decrements, the header bytes change → the checksum over them changes. Every router must recompute; that per-hop cost is exactly what IPv6 eliminated by removing the header checksum.
8. **Q: What is fragmentation and how are fragments reassembled?** A: Splitting a packet > MTU into fragments sharing the ID, with MF flags and 8-byte-unit offsets; the destination reassembles by (src, dst, protocol, ID) and delivers when all bytes are present. One lost fragment → the whole datagram is dropped after timeout.
9. **Q (FAANG): What is the DF bit and path MTU discovery?** A: Don't Fragment: the packet must not be split; an oversized DF packet is dropped with ICMP "fragmentation needed" (RFC 1191) revealing the path MTU → the sender shrinks segments. TCP uses it to avoid fragmentation; PMTUD is why TCP doesn't normally fragment.
10. **Q: What's the maximum IP packet size?** A: Total Length field = 16 bits → 65,535 bytes (header + payload). In practice limited by MTU + reassembly (and jumbo frame support); IPv6's jumbo payload option extends further.
11. **Q (production): `tcpdump` shows `flags [DF]`. Is that normal?** A: Yes — modern stacks set DF so path-MTU discovery works (no mid-path fragmentation). Fragmented *inbound* traffic or DF-mismatches are worth investigating (frag floods, PMTU blackholes).
12. **Q: What are the IPv4 header options and why are they rare?** A: Source route, record route, timestamps, router alert — carried when IHL > 5. Mostly disabled/deprecated because they force slow-path parsing and source-route was a security vulnerability. IPv6 replaced them with extension headers.
13. **Q (tricky): How does the receiver know a packet is a fragment?** A: MF flag set OR Fragment Offset ≠ 0. The first fragment has offset 0 + MF=1; the last has MF=0 + offset > 0; a whole packet has MF=0, offset 0. A lone "offset=0, MF=0" is a normal whole datagram.
14. **Q: What is the relationship between MTU and the Total Length field?** A: Total Length is the datagram's full size (≤65535); MTU is the *link's* max frame size. A datagram larger than the MTU must be fragmented (or dropped if DF). MSS (TCP) = MTU − IP header − TCP header (1460 at 1500).
15. **Q (FAANG): Why did IPv6 remove the header checksum?** A: Because the checksum requires *recomputation at every hop* (TTL changes) — a per-hop cost with no payload benefit (transport covers integrity). Removing it makes routers faster and simpler; IPv6 relies on Layer 2 (CRC) + Layer 4 (checksum). IPv4 kept it for historical safety.
16. **Q: What does ECN in the TOS byte do?** A: Explicit Congestion Notification: routers set the CE bit instead of dropping during congestion; the receiver informs the sender (TCP ECE/CWR) which halves cwnd *without* packet loss. The TOS byte's low 2 bits carry ECT/CE.
17. **Q: What is the DSCP field?** A: Differentiated Services Code Point (6 bits of the TOS byte) — QoS class marking (voice EF, video AF, best-effort default); routers with QoS policies treat classes differently (see part-04 QoS section).

## 14. Follow-Up Questions
1. **Q: How does IP-in-IP / GRE encapsulation interact with the header?** A: A whole datagram becomes the *payload* of another (proto 4/47): the outer header has its own TTL/checksum; the inner is forwarded intact — the basis of tunnels/VPNs (see part-04 IPsec/tunneling). TTL handling: routers decrement only the outer.
2. **Q: What is "IP fragmentation" vs "TCP segmentation"?** A: Segmentation is *TCP's* split of a byte stream into segments ≤ MSS (a logical, per-connection act). Fragmentation is *IP's* split of an already-formed datagram at the MTU (a physical, per-packet act). Segmentation prevents fragmentation (DF + MSS ≤ MTU).
3. **Q (tricky): Why are overlapping fragments dangerous?** A: Attackers craft fragments with overlapping offsets (RFC 1858/3128): a firewall sees "benign fragment A" while the reassembled packet contains "evil byte range B." Old firewalls reassembled differently than the target → evasion. Modern firewalls reassemble or drop fragments — the classic IP-security story.
4. **Q: What is the "MSS clamping" trick and where does it fail?** A: Routers/NATs rewrite the TCP MSS in SYN to ≤ the path MTU − 40, avoiding the need for fragmentation or PMTUD. It fails on *encrypted* TCP options or when the endpoint ignores MSS — the "why is my VPN MTU so small" classic.
5. **Q (FAANG): "Why does my download stop working over a tunnel but works directly?"** A: Classic MTU mismatch: the tunnel adds header bytes, so the effective path MTU shrinks; a 1500-byte TCP segment now exceeds it; if DF is set (default) and the blackhole router drops the ICMP "needs frag" message, PMTUD can't work → the connection stalls. Fix: clamp MSS on the tunnel / lower MTU. The header fields *are* the diagnosis.

## 15. Coding Example
```python
# Parse an IPv4 header from a raw packet (fields in order)
import struct

def parse_ipv4(pkt):
    if len(pkt) < 20:
        return None
    version_ihl, tos, total = pkt[0], pkt[1], struct.unpack(">H", pkt[2:4])[0]
    ident, flags_frag = struct.unpack(">HH", pkt[4:8])
    ttl, proto, cksum = pkt[8], pkt[9], struct.unpack(">H", pkt[10:12])[0]
    src = ".".join(str(x) for x in pkt[12:16])
    dst = ".".join(str(x) for x in pkt[16:20])
    return dict(version=version_ihl >> 4, ihl=(version_ihl & 0xF) * 4, tos=tos,
                total_length=total, id=ident, flags=flags_frag >> 13,
                fragment_offset=(flags_frag & 0x1FFF) * 8, ttl=ttl,
                protocol=proto, checksum=cksum, src=src, dst=dst)

print(parse_ipv4(bytes([0x45, 0x00, 0x00, 0x54, 0x00, 0x00,
                        0x40, 0x00, 0x40, 0x01, 0x00, 0x00,
                        192, 168, 1, 5, 8, 8, 8, 8])))
# version=4 ihl=20 total_length=84 flags=2(DF) ttl=64 protocol=1(ICMP)
```
```bash
# Watch the header in the wild
$ sudo tcpdump -nn -i eth0 'ip' -vv | head
#   IP (tos 0x0, ttl 64, id 4821, offset 0, flags [DF], proto TCP (6), length 60)
# Kernel counters (checksum/drop diagnostics):
$ ip -s link show eth0
$ cat /proc/net/snmp | grep -E '^Ip'
#   Ip: Forwarding DefaultTTL InReceives InHdrErrors ...  <- HdrErrors = checksum/format drops
```

## 16. Industry Usage
- **Every router/firewall/LB**: forwarding engines parse this header per packet; TCAMs match on (dst, TTL-range, protocol, DSCP); firewalls filter by protocol/ports. The header *is* the forwarding language.
- **CDNs/anycast (Cloudflare, Google, root servers)**: TTL + DSCP + protocol fields feed routing/security decisions; BGP + anycast load-balance by destination.
- **Path-MTU/fragmentation engineering**: VPNs (wireguard/openvpn), tunnels, and cloud networking fight fragmentation daily (MSS clamping, jumbo frames); "PMTU blackhole" is a standard ops diagnosis.
- **Security (the dark side)**: fragment-based evasions, TTL-based OS fingerprinting (ttl 64=Linux, 128=Windows), source-spoofing (needs BCP 38 egress filtering), and header-option abuse — the header fields drive IDS/IPS signatures.
- **QoS/DC fabrics**: DSCP marking in clouds/datacenters (voice/video classes), ECN enablement (DCTCP), and switch-priority mapping — the TOS byte is the QoS API.
- **Protocol engineering**: the Protocol field registry (IANA) and header evolution (RFC 6864, RFC 3168 ECN, RFC 2474 DSCP) — the datagram is the layer's living spec.

## 17. References
- RFC 791 — Internet Protocol: https://www.rfc-editor.org/rfc/rfc791
- RFC 6864 — Updated IP ID specification: https://www.rfc-editor.org/rfc/rfc6864
- RFC 1191 — Path MTU Discovery: https://www.rfc-editor.org/rfc/rfc1191
- RFC 3168 — ECN (ECN in IP/TCP): https://www.rfc-editor.org/rfc/rfc3168
- RFC 2474 — DSCP (DiffServ): https://www.rfc-editor.org/rfc/rfc2474
- RFC 815 — IP Datagram Reassembly Algorithms: https://www.rfc-editor.org/rfc/rfc815
- IANA protocol numbers: https://www.iana.org/assignments/protocol-numbers
- Kurose & Ross, *Computer Networking*, Ch. 4 §4.3.1–4.3.2.

## 18. Cheat Sheet
- Header: 20-60 B = Ver/IHL(8) TOS/ECN(8) TotalLen(16) ID(16) Flags+Off(16) TTL(8) Proto(8) Cksum(16) Src(32) Dst(32).
- IHL = words; 5 = 20 B. Version 4 (IPv6 = 6).
- TOS: DSCP (QoS) + ECN (ECT/CE) — congestion marking.
- Protocol: 1 ICMP, 6 TCP, 17 UDP, 89 OSPF, 47 GRE.
- TTL: hop count; 0 → drop + ICMP time-exceeded. Linux 64, Windows 128.
- Fragments: same ID; MF; offset in 8-byte units; reassemble at dst; one lost → whole datagram dropped.
- DF: don't fragment → PMTUD (ICMP frag-needed) → MSS clamp.
- Header checksum: per-hop (TTL changes); payload checksum is L4's job.
- Max size 65535; practical = MTU-bound + fragmentation.
- `tcpdump -vv` prints it; `ip -s`/`/proc/net/snmp` show errors.

## 19. Quiz
1. Min IPv4 header: a) 20 B b) 60 B c) 8 B d) 40 B → **a**
2. IHL field units: a) bytes b) 32-bit words c) bits d) fragments → **b**
3. Protocol for TCP: a) 1 b) 6 c) 17 d) 89 → **b**
4. TTL at 0 → a) forward b) drop + ICMP time-exceeded c) fragment d) loop → **b**
5. Fragment offsets are in: a) bytes b) 8-byte units c) words d) bits → **b**
6. DF means: a) delay fragment b) don't fragment c) drop forward d) data frame → **b**
7. Header checksum is recomputed: a) never b) at each hop c) at the dest d) at the source only → **b**
8. Max IP packet size: a) 1500 b) 65535 c) 2^32 d) 64K+ → **b**
9. Linux default TTL: a) 32 b) 64 c) 128 d) 255 → **b**
10. Which is NOT an IPv4 header field? a) TTL b) Protocol c) Window d) Fragment Offset → **c**

## 20. Flashcards
- **Q: Header fields?** → **A:** Ver/IHL, TOS+ECN, TotalLen, ID, Flags+Off, TTL, Proto, Cksum, Src, Dst.
- **Q: IHL?** → **A:** header length in 32-bit words (5 = 20 B).
- **Q: TTL?** → **A:** hop count; 0 = drop + ICMP time-exceeded.
- **Q: Protocol field?** → **A:** 1 ICMP, 6 TCP, 17 UDP — payload owner.
- **Q: Fragments?** → **A:** same ID, MF flag, 8-byte offsets; reassembled at dst.
- **Q: DF?** → **A:** don't fragment → PMTUD / MSS clamp.
- **Q: Header checksum?** → **A:** per-hop (TTL changes); payload integrity = L4.
- **Q: Why IPv6 dropped it?** → **A:** per-hop recompute cost; L2+L4 cover integrity.

## 21. Revision
IPv4 header: Ver/IHL/TOS+ECN/TotalLen(65535)/ID/Flags(DF,MF)+Off(8-byte)/TTL(hops, 0→ICMP time-exceeded)/Proto(6=TCP,17=UDP,1=ICMP)/checksum(per-hop)/Src/Dst, 20-60 B. Fragmentation splits at MTU (same ID, MF, offsets), reassembled at dst; DF → PMTUD → MSS clamp; one lost fragment kills the datagram. No payload checksum (L4's job), no built-in security. Options (IHL>5) deprecated → IPv6 extension headers. tcpdump -vv shows it; /proc/net/snmp Ip counters show drops.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Draw/describe the IPv4 header." | 2 How It Works / 7 Formal Definition |
| "What does TTL do / traceroute?" | 13 Q&A / 9 Internal Working |
| "What is fragmentation / reassembly?" | 13 Q&A / 8 Example |
| "DF / path MTU discovery?" | 13 Q&A / 10 Time Complexity |
| "Why header checksum / per-hop?" | 13 Q&A / 12 Disadvantages |
| "Protocol field?" | 13 Q&A / 5 Intuition |
| "Why did IPv6 drop the checksum?" | 13 Q&A / 14 Follow-Up |
| "Overlapping fragment attacks?" | 14 Follow-Up / 16 Industry Usage |
| "Why does my VPN stall (MTU)?" | 14 Follow-Up / 15 Coding |
