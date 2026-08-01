# Networking Crash-Course Revision

> **TL;DR**: The final all-in-one pass — every part's cheat sheet distilled into one read: OSI layers, TCP/UDP, IP/BGP, DNS, HTTP/1-2-3, TLS 1.3, L2/ethernet, physical-layer math, security, LB/anycast/DC architectures, the key numbers (MTU 1500, MSS 1460, ports, TTL, backoff timers), and a morning-of checklist. Re-read this the night before and skim it the morning of.

## 1. Why Does This Exist?
By now you've studied the deep 22-block sections. The problem the night before (and morning of) an interview is **density**: you need the whole roadmap in your head at once, organized so any question triggers the right answer. This crash course exists to compress everything into a single re-readable artifact — one pass, ~30-40 minutes, that re-anchors every part and gives you a "morning of" checklist. It is the synthesizer: all the long-form material becomes one integrated mental model.

## 2. How Does It Work?
1. Read Part by Part in order (Layers → L2 → L3 → L4 → L7 → Physical → Security → Advanced).
2. For each part: the ONE-LINE summary → the key mechanisms → the numbers → the likely questions.
3. Use the anchors (bolded one-liners) as memory hooks; the numbers as quick facts.
4. Finish with the "Morning-of checklist" and the "Numbers you must know" table.
Read it twice (night before + morning of). It replaces re-reading the long sections at the last minute.

## 3. When Is It Used?
- **T-1 night**: full read.
- **T-0 morning**: skim the checklist + numbers + anchors.
- **Between rounds**: glance at the tables.
- As the capstone pass after completing Parts 01-08.

## 4. Why Wasn't Another Approach Chosen?
- *Re-reading the deep sections:* at T-1 you don't need new depth, you need *integration* — the crash course does in 40 minutes what re-reading 8 parts does in days, at the right level.
- *Only the Q-bank (Section 01):* flashcards test recall but don't *structure* the mental model; the crash course supplies the structure (the map), the bank supplies the drills (the reps).
- *Skip revision entirely:* the interview's rapid-fire round punishes disorganized recall — a structured last pass measurably lifts it.

## 5. Intuion
A **suitcase repacked for travel**: the deep sections are your wardrobe (knowledge); the crash course is repacking it so everything fits in one carry-on and you can find any item in a second. It doesn't add clothes — it organizes them for the trip.

## 6. Real-World Analogy
A **pilot's approach checklist** before landing. The pilot already knows how to fly (the deep material); the checklist (crash course) makes sure nothing is forgotten in the high-pressure moment — flaps, gear, speed — in the right order. The interview is the landing; this is the checklist.

## 7. Formal Definition
A cross-part synthesis document: one-line-per-part summaries, mechanism lists, number tables, anchor one-liners, and a pre-interview checklist. It intentionally compresses — depth lives in the sections; this is the map.

## 8. Example
**TCP in the crash course (one paragraph):** reliable, ordered byte stream; 3-way handshake (SYN→SYN+ACK→ACK); seq/ack numbering; flow control = rwnd, congestion control = cwnd (slow start → AIMD); RTO from RTT+variance, fast retransmit on 3 dup-ACKs; throughput ≤ cwnd/RTT, window must cover BDP; TIME_WAIT 2×MSL; modern: CUBIC, BBR, SACK, ECN, QUIC/HTTP3.
That paragraph *is* TCP for the interview — the depth lives in Part 03.

## 9. Internal Working
The crash course compresses by: (a) **one-line summaries** per part (the elevator answer), (b) **mechanism lists** (the "what happens" sequence), (c) **numbers** (facts to say out loud), (d) **anchors** (memorable one-liners that trigger recall), and (e) **checklists** (the interview-format action plan). Reading it activates the same neurons as the deep sections (the anchors were chosen from them) but with far less time-to-recall.

## 10. Time Complexity / Performance
- T-1: ~40 min full read; T-0: ~10 min checklist + numbers + anchors.
- The payback: instant recall in the rapid-fire round (where hesitation loses points) and an organized springboard into design questions.

## 11. Advantages
One artifact covering all 8 parts; correct density (numbers + anchors, not prose); doubles as a pre-interview checklist; time-efficient (the right tool at T-1/T-0).

## 12. Disadvantages
It's a *revision* artifact, not a learning one — if a topic is still fuzzy, the crash course will gloss over it (you must go back to the section). It also can't simulate the interview itself (drill with Section 01 and 03 for that).

## 13. Interview Questions — the integrated revision pass

### Part 01 — Foundations (Layers)
**Summary**: OSI 7 layers (Physical→Application) vs TCP/IP 4 layers; encapsulation adds a header each layer (frame→packet→segment→message); "what layer is this?" is the universal filter.
**Anchors**: *Layers in order: Please Do Not Throw Sausage Pizza Away; every layer adds a header to the previous PDU; L4=segments, L3=packets, L2=frames.*
**Numbers**: PDU names (frame/packet/segment/message); the 7 layers.
**Likely Qs**: name layers; encapsulation; PDU names; where LB/firewall fit.

### Part 02 — Application layer (HTTP/DNS/Email/CDN)
**Summary**: HTTP/1.1 = persistent, one-request-at-a-time (HOL); HTTP/2 = multiplexed streams + HPACK over one TCP (fixes HTTP-HOL, not TCP-HOL); HTTP/3 = QUIC/UDP (kills TCP-HOL, 0/1-RTT, connection migration). DNS = hierarchical lookup with caching (TTL). Cookies/sessions/JWT = state. CDN = edge cache.
**Anchors**: *HTTP/2 fixes request HOL, QUIC fixes transport HOL; DNS = root→TLD→authoritative with caching; CDN = cache at the edge (latency + origin offload).*
**Numbers**: ports 80/443/53; HTTP codes (200/301/304/400/401/403/404/429/500/502/503/504); DNS records (A/AAAA/CNAME/MX/TXT/SRV); HTTP/2 multiplexing vs HTTP/3 streams.
**Likely Qs**: HTTP/1 vs 2 vs 3; DNS resolution; cookies vs sessions; status codes; WebSocket vs SSE.

### Part 03 — Transport layer (TCP/UDP/QUIC)
**Summary**: TCP = reliable, ordered, congestion/flow controlled; handshake SYN→SYN+ACK→ACK; rwnd = receiver buffer, cwnd = network (slow start → AIMD); RTO = RTT+variance with backoff; fast retransmit (3 dup-ACKs); throughput ≤ cwnd/RTT; BDP = bandwidth×RTT; TIME_WAIT 2×MSL. UDP = 8-byte header, no guarantees. QUIC/HTTP3 = UDP + TLS 1.3 + streams.
**Anchors**: *TCP window = min(cwnd, rwnd); slow start doubles, AIMD halves on loss; retransmit on RTO or 3 dup-ACKs; window must cover BDP; TIME_WAIT 2×MSL; QUIC kills transport HOL.*
**Numbers**: MSS 1460 (MTU 1500−20−20); ports 0-65535; MSL ~60 s (TIME_WAIT ~2 min); default Linux cwnd ~10 segments; RTT examples (LAN <1 ms, transoceanic ~150-250 ms).
**Likely Qs**: handshake; flow vs congestion; slow start/AIMD; retransmission; BDP; Nagle/TCP_NODELAY; UDP vs TCP; QUIC.

### Part 04 — Network layer (IP/Routing/NAT)
**Summary**: IPv4 (32-bit, NAT-heavy) vs IPv6 (128-bit, no NAT/broadcast); CIDR (IP/prefix); RFC1918 private ranges; NAT/PAT (one public IP, many hosts); TTL/hop-limit (traceroute); MTU/fragmentation (IPv6: ICMPv6 too-big); ICMP (ping/traceroute/PTMU); routing: OSPF (intra-AS link-state), BGP (inter-AS path-vector, AS-path + policy); ECMP.
**Anchors**: *CIDR = IP/prefix; private = 10/8, 172.16/12, 192.168/16; BGP = internet's glue via AS-path + policy; ECMP hashes flows across equal paths.*
**Numbers**: MTU 1500; IPv4 4.3B addresses; IPv6 2^128; default TTL 64 (Linux); BGP = TCP 179; OSPF = IP 89.
**Likely Qs**: subnet math; NAT types; TTL/traceroute; fragmentation/MTU/MSS; OSPF vs BGP; BGP path selection; ECMP.

### Part 05 — Data link layer (Ethernet/Wi-Fi/Switching)
**Summary**: MAC (L2, per-link) vs IP (L3, end-to-end); ARP maps IP→MAC (broadcast); switches learn MACs, full-duplex, isolated collision domains; VLANs = 802.1Q (4-byte tag, 12-bit VID); STP breaks loops (broadcast storms); framing + error detection (CRC) from the frames chapters; Wi-Fi = CSMA/CA (listen + backoff + ACK, RTS/CTS) because wireless can't detect collisions.
**Anchors**: *ARP = "who has IP?" broadcast; STP blocks redundant links (then unblocks on failure); CSMA/CA listens because you can't detect while transmitting; 802.1Q = 4-byte VLAN tag.*
**Numbers**: Ethernet MTU 1500; MAC 48-bit; 802.1Q = 4 bytes, VID 12 bits (4096); 2.4/5/6 GHz bands; Wi-Fi 6/6E/7.
**Likely Qs**: ARP; MAC vs IP; switch/hub; VLAN/802.1Q; STP; CSMA/CA vs CSMA/CD; MAC address format.

### Part 06 — Physical layer (Signals/Media/Math)
**Summary**: Analog vs digital (digital = noise-immune); line coding (NRZ, Manchester, 4B5B, 8B10B, 64B66B) + modulation (ASK/FSK/PSK/QAM); media: twisted pair (<100 m), coax, fiber (100 km+, EMI-immune), radio; multiplexing (FDM/TDM/WDM/CDMA); switching (circuit vs packet); Nyquist (symbol rate ≤ 2B) + Shannon (C = B·log2(1+SNR)).
**Anchors**: *Nyquist = 2B·log2(M) (symbols), Shannon = B·log2(1+SNR) (the real ceiling); fiber wins on distance/bandwidth/EMI; packet switching = statistical sharing.*
**Numbers**: Shannon example: 3 kHz, SNR 30 dB → ~30 kbps; fiber 10-400 Gbps per lane; Cat6 10 Gbps ≤ 55 m; WiFi channels 20/40/80/160 MHz.
**Likely Qs**: Shannon/Nyquist computation; bandwidth vs throughput; fiber vs copper; FDM vs TDM; circuit vs packet.

### Part 07 — Security (TLS/PKI/Attacks/VPN/Zero Trust)
**Summary**: CIA triad + AAA; symmetric (AES, bulk) vs asymmetric (RSA/ECC, key exchange/signing); hashing (SHA-256, one-way) vs encryption (reversible) vs signing (hash + private key); TLS 1.3 = 1-RTT, ECDHE (forward secrecy), AEAD (AES-GCM), cert chain (X.509) + CertificateVerify; attacks: XSS/SQLi/CSRF/DDoS/MITM; defenses: firewalls (packet/stateful/APP/WAF), IDS/IPS; IPsec (L3, ESP/IKEv2) vs TLS (L4); SSH (TOFU host keys); Zero Trust (never trust, always verify; PDP/PEP).
**Anchors**: *TLS 1.3 = 1 RTT, ephemeral ECDHE = forward secrecy, AEAD-only; hashing isn't reversible; certificates = PKI binds key to identity; Zero Trust = verify every request, deny by default.*
**Numbers**: TLS 1.3 1-RTT (0-RTT resume); SHA-256 256-bit; RSA 2048/3072; AES-128/256; TIME_WAIT unrelated. IPsec UDP 500/4500; SSH 22; HTTPS 443.
**Likely Qs**: TLS 1.3 handshake; symmetric vs asymmetric; hash vs encryption; cert chain; XSS/SQLi/CSRF/DDoS; IPsec vs TLS; Zero Trust.

### Part 08 — Advanced (GSLB/Anycast/DC/Design)
**Summary**: GSLB = DNS steering (geo/ECS + latency + health + weights, TTL-cached); anycast = same IP from many sites, routing picks nearest (stateless only, DDoS absorb); EDNS = client subnet for accuracy; multicast = one-to-many via IGMP/PIM (IPTV); broadcast = link-local only; DC = CLOS/spine-leaf + ECMP + VXLAN overlay + EVPN; cloud = VPC/SG/NACL; LB tiers L4→L7→GSLB.
**Anchors**: *GSLB picks the region (DNS, coarse), anycast picks the node (nearest, stateless-only); spine-leaf + ECMP uses every link; VXLAN = L2 mobility over a routed underlay; SG = stateful instance, NACL = stateless subnet.*
**Numbers**: VXLAN VNI 24-bit (16M); ECMP K paths (16-64); CDN PoP 10-50 Gbps; streaming ~5 Mbps/viewer; latency budget 100 ms.
**Likely Qs**: GSLB/anycast/EDNS; anycast vs multicast vs broadcast; spine-leaf/ECMP/VXLAN; design questions (Section 02).

## 14. Follow-Up Questions (revision-depth)
1. **Q: How do I know what I don't know?** A: Do Section 01's 100 questions as a diagnostic: any topic with 3+ misses = re-read that part's sections *before* the crash course. The crash course is the top of the funnel, not the teacher.
2. **Q: What if I blank on a question in the interview?** A: Anchor-recall: jump to the part's anchor (e.g., "TCP = reliable ordered; window = min(cwnd,rwnd)") and rebuild from the mechanism list. Saying the anchor buys structure even under pressure.
3. **Q: How do I convert this into design answers?** A: Every design answer = "find (DNS/GSLB) → reach (edge/L4/L7) → serve (cache/stateless/DB) → protect (TLS/DDoS/failover)" + numbers + the 10× bottleneck walk. The anchors give you the building blocks; Section 02 gives the pattern.

## 15. Coding Example
```python
# One-line "state of the network" harness to run the morning of an interview
import subprocess
checks = [
    "ping -c 2 1.1.1.1",                       # reachability + RTT
    "mtr -rn -c 3 1.1.1.1 2>/dev/null | tail -3",   # path
    "dig +short example.com",                  # DNS
    "curl -s -o /dev/null -w '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer}\n' https://example.com",  # stage timing
    "ss -s",                                   # TCP state summary
    "ip -brief addr",                          # local addressing
]
for c in checks:
    print("$", c); print(subprocess.run(c, shell=True, capture_output=True, text=True).stdout)
```

## 16. Industry Usage
The crash-course style (structured anchors + numbers + checklist) mirrors how working engineers actually *use* their network knowledge: a mental index you jump into on-call or in an interview, with the depth reached on demand. It's also the format of senior-level "brushing" — SREs and network engineers maintain exactly this kind of personal summary of their stack.

## 17. References
Each part's section list (index of the full roadmap); RFC index (793, 768, 791, 8200, 1035, 9110-9114, 8446, 4271, 7348, 7432); Kurose & Ross, *Computer Networking*, 8th ed., as the canonical textbook; Section 01 (drill) + Section 02 (design) + Section 03 (hands-on) as the three practice pillars.

## 18. Cheat Sheet — numbers you must know
| Item | Value |
|---|---|
| MTU / MSS (Ethernet) | 1500 / 1460 |
| MAC | 48-bit |
| 802.1Q VLAN tag | 4 bytes, VID 12-bit (4096) |
| Ports | 0-65535; well-known < 1024 (80 HTTP, 443 TLS, 53 DNS, 22 SSH, 67/68 DHCP, 123 NTP) |
| BGP / OSPF | TCP 179 / IP 89 |
| Default TTL | 64 |
| MSL / TIME_WAIT | ~60 s / ~2 min (2×MSL) |
| Shannon | C = B·log2(1+SNR) |
| Nyquist | 2B·log2(M) |
| TLS 1.3 handshake | 1 RTT (0-RTT resume) |
| IPsec IKE | UDP 500 / 4500 (NAT-T) |
| VXLAN VNI | 24-bit (16M) |
| CDN PoP throughput | 10-50 Gbps |
| Streaming / viewer | ~5 Mbps |
| Private ranges | 10/8, 172.16/12, 192.168/16 |

## 19. Quiz (final integrated)
1. Which fixes HTTP/2's TCP head-of-line blocking? a) keepalive b) QUIC c) SACK d) ECN → **b**
2. TCP window to use on a 10 Gbps × 50 ms link? a) 64 KB b) ~62.5 MB c) 1 KB d) 1 GB → **b** (BDP)
3. Anycast is for: a) stateful apps b) stateless services c) databases d) WebSockets → **b**
4. TLS 1.3 mandates: a) RSA exchange b) ephemeral ECDHE c) CBC d) SSLv3 → **b**
5. The order to design any system: a) DB→LB→DNS b) find→reach→serve→protect c) cache→origin d) none → **b**
6. VXLAN VNI bits: a) 12 b) 16 c) 24 d) 32 → **c**
7. Which tool shows cwnd/rtt/mss of live connections? a) ping b) ss -ti c) dig d) ethtool → **b**
8. A stateful, instance-level firewall in AWS is a: a) NACL b) security group c) IGW d) VPC → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-c, 7-b, 8-b.

## 20. Flashcards (the anchors as flashcards)
- **Q: TCP in one line** → **A:** Reliable ordered byte stream; window = min(cwnd,rwnd); slow start → AIMD; retransmit on RTO/3 dup-ACKs.
- **Q: HTTP/1→2→3** → **A:** 1 = persistent + HOL; 2 = streams/HPACK (fixes HTTP-HOL); 3 = QUIC/UDP (kills transport HOL).
- **Q: BGP** → **A:** Path-vector, inter-AS, TCP 179, chooses on AS-path + policy.
- **Q: TLS 1.3** → **A:** 1-RTT, mandatory ECDHE (forward secrecy), AEAD-only, cert chain + CertificateVerify.
- **Q: Anycast** → **A:** Same IP from many sites; routing picks nearest; stateless-only; DDoS absorb.
- **Q: CLOS/VXLAN** → **A:** Spine-leaf + ECMP (all links used); VXLAN = L2-in-UDP overlay (16M VNIs).
- **Q: Zero Trust** → **A:** Never trust, always verify; PDP/PEP; default deny.
- **Q: Design framework** → **A:** find (DNS/GSLB) → reach (edge/L4/L7) → serve (cache/stateless) → protect (TLS/DDoS/failover).

## 21. Revision (the whole roadmap in anchors)
**Layers**: P-D-N-T-S-P-A; each adds a header. **L2**: MAC, ARP, switch, VLAN/802.1Q, STP, CSMA/CA (Wi-Fi). **L3**: IPv4/6, CIDR, NAT/PAT, TTL, MTU/MSS, ICMP, OSPF/BGP/ECMP. **L4**: TCP = reliable/ordered, rwnd vs cwnd, slow start→AIMD, RTO + fast retransmit, BDP window, TIME_WAIT 2×MSL, Nagle; UDP = 8B, no guarantees; QUIC = HTTP/3. **L7**: HTTP/1-2-3, DNS (root→TLD→auth, TTL), cookies/JWT, CDN edge. **P6**: Nyquist/Shannon, fiber/copper, FDM/TDM, packet switching. **Security**: TLS 1.3 (1-RTT, ECDHE, AEAD), X.509 chain, XSS/SQLi/CSRF/DDoS, IPsec vs TLS, Zero Trust. **Advanced**: GSLB (DNS steering), anycast (nearest), multicast (group), spine-leaf/ECMP/VXLAN/EVPN, LB tiers, VPC/SG/NACL. **Design**: find→reach→serve→protect + numbers + 10× walk. **Numbers**: MTU 1500/MSS 1460, TTL 64, MSL 60 s, Shannon/Nyquist, TLS 1-RTT, VXLAN 16M, CDN 10-50 Gbps.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Summarize each layer/protocol" | 13 (all parts) |
| "TCP in one paragraph" | 13-Part03 |
| "HTTP/1 vs 2 vs 3" | 13-Part02 |
| "Walk TLS 1.3" | 13-Part07 |
| "Anycast/GSLB/DC in one breath" | 13-Part08 |
| "The numbers you know?" | 18 (table) |
| "Design any system" | 13-Part08 + Section 02 |
| "How do I know what I don't know?" | 14-Q1 |
| "What if I blank?" | 14-Q2 |
