# Top-100 Networking Interview Questions and Answers

> **TL;DR**: 100 rapid-fire networking Q&A spanning all seven parts + advanced architecture — drill them aloud with the answer covered; any you can't answer in under 60 seconds means go back to the section referenced.

## 1. Why Does This Exist?
Interviewers don't ask one big question — they ask a *stream* of rapid-fire ones to gauge depth and reflexes: "TCP vs UDP?", "what's in a TCP header?", "how does DNS work?", "why is TLS 1.3 faster?". This section exists to convert the entire roadmap into a recall device. Each question is answered in one to three lines, tagged with its source part, and grouped by topic so you can drill systematically. The discipline matters as much as the facts: **cover the answer, say it aloud, check it** — retrieval practice, not re-reading, is what sticks.

## 2. How Does It Work?
1. Work through the topics in order (Layers → TCP → UDP → IP → Routing → DNS → HTTP → TLS/Security → LB/Architecture → Troubleshooting).
2. For each question: read only the question, answer aloud in your own words, then reveal.
3. Mark the ones you missed; re-drill only those the next day (spaced repetition).
4. Use the "Source" column to jump back to the deep material when an answer feels thin.
There are exactly **100 questions** (Q1-Q100). Good target: sub-60-second answers for all.

## 3. When Is It Used?
- 1-2 weeks before interviews: daily 30-minute rapid-fire drill.
- The day of: last-pass skim of the ones you marked.
- As a self-diagnostic: if a topic has 3+ misses, re-read that part's sections.

## 4. Why Wasn't Another Approach Chosen?
- *Just re-read the parts:* passive, no retrieval, no confidence signal. The bank forces recall + self-grading.
- *Only coding problems:* interviews are 50/50 theory and hands-on — the rapid-fire round tests exactly the theory in this bank.
- *Only big practice mocks:* expensive and infrequent; the bank is free daily reps that compound.

## 5. Intuition
Like **flashcards for a pilot's preflight**: you must answer from memory, instantly, without the manual open. The bank is the manual compressed into 100 test questions; the Source column is the manual's index.

## 6. Real-World Analogy
A **boxer's shadow-boxing round** — 100 quick jabs (questions) with no thinking pause, so that in the ring (the interview) the fundamentals are automatic and your conscious attention goes to the hard combinations (system design).

## 7. Formal Definition
None needed — the "formal definition" IS the question bank below. See each question's answer. The bank is organized into 12 groups; each Q&A is (question → answer, Source).

## 8. Example
**Q12: What are the three-way handshake's flags?** → SYN (client), SYN+ACK (server), ACK (client). Source: Part 03.
That's the unit: one line in, one line out, instantly.

## 9. Internal Working
The bank works by forcing retrieval: reading a question activates memory search; answering aloud engages verbal working memory; the reveal closes the loop with feedback; marking misses feeds spaced repetition. Grouping by topic builds semantic clusters (TCP flags with handshake with timestamps), and the Source tags give a corrective path back to depth.

## 10. Time Complexity / Performance
- 100 questions × ~30 s = ~50 min for a full pass; 30-60 min/day targeted on misses is ideal.
- No asymptotic cost — it's constant-time retrieval that *speeds up* with reps (this is the point).

## 11. Advantages
Complete, topic-grouped, sourced, recall-forced coverage of the whole roadmap in one artifact; integrates with spaced repetition; doubles as a diagnostic.

## 12. Disadvantages
Answers are compressed (1-3 lines) — they're a test, not a teacher; you must go back to the Source for depth. Also static — the interview landscape shifts, so pair with Section 04 (company-specific).

## 13. Interview Questions (the Bank)
**Group 1 — Layers & Models (Q1-Q6)**
1. **Q: Name the OSI layers in order.** A: Physical, Data Link, Network, Transport, Session, Presentation, Application (mnemonic: "Please Do Not Throw Sausage Pizza Away"). Source: P1.
2. **Q: What's the difference between OSI and TCP/IP model?** A: OSI = 7 theoretical layers (separates session/presentation); TCP/IP = 4 practical layers (Application merges the top three). The internet runs TCP/IP; OSI is a reference. Source: P1.
3. **Q: What does each layer do in one line?** A: Physical = bits on media; Data Link = frames on a link (MAC, error check); Network = IP packet routing; Transport = end-to-end segments + reliability; Application = user protocols. Source: P1.
4. **Q: Where do firewalls/LBs fit in the model?** A: L4 = transport (ports/flows); L7 = application (HTTP/TLS). Devices often span layers (a WAF is L7, a stateful firewall is L3/L4). Source: P1/P7.
5. **Q: Encapsulation: what's added at each layer?** A: Application → TCP header (transport) → IP header (network) → Ethernet header+trailer (link) → bits. Each layer wraps the previous. Source: P1.
6. **Q: What's a PDU at each layer?** A: Link = frame; Network = packet; Transport = segment (TCP) / datagram (UDP); Application = message. Source: P1.

**Group 2 — Physical & Link (Q7-Q12)**
7. **Q: What is a MAC address vs IP address?** A: MAC = burned-in L2 identifier on the NIC, used within a link/VLAN; IP = logical L3 address, routable. MACs change per hop; IPs survive (mostly) end-to-end. Source: P5.
8. **Q: What is ARP and how does it work?** A: Address Resolution Protocol: maps an IP to a MAC on a local link. Broadcast "who has 10.0.0.5?" → target replies with its MAC (unicast). Source: P5.
9. **Q: What is a broadcast domain vs a collision domain?** A: Broadcast = where an L2 broadcast reaches (VLAN/LAN). Collision domain = where two transmissions can collide (one port in full-duplex switched networks — no collisions). Source: P5.
10. **Q: What does a switch do vs a hub?** A: Hub = dumb repeater (shared collision domain). Switch = learns MACs, forwards only to the right port (full-duplex, isolated). Source: P5.
11. **Q: What is STP and why does it exist?** A: Spanning Tree Protocol: breaks loops in redundant L2 topologies by blocking redundant links (prevents broadcast storms), then enables them on failure. Source: P5.
12. **Q: What is a VLAN and how does 802.1Q tag frames?** A: VLAN = logical L2 partition (broadcast domain). 802.1Q inserts a 4-byte tag (VID 12 bits = 4096) between src MAC and ethertype. Source: P5.

**Group 3 — TCP fundamentals (Q13-Q25)**
13. **Q: What are TCP's guarantees?** A: Reliable, ordered, byte-stream, connection-oriented, flow + congestion controlled. Source: P3.
14. **Q: What does a TCP header contain (main fields)?** A: src/dst ports (16-bit), seq/ack numbers, data offset, flags (NSR-ECE-CWR, URG/ACK/PSH/RST/SYN/FIN), window size, checksum, options, data. Source: P3.
15. **Q: Walk the 3-way handshake.** A: Client SYN (seq=x) → Server SYN+ACK (seq=y, ack=x+1) → Client ACK (ack=y+1). Establishes both directions + ISNs. Source: P3.
16. **Q: How does TCP close a connection?** A: 4-way FIN exchange: A FIN → B ACK → B FIN → A ACK; plus TIME_WAIT on the first closer (2×MSL). Source: P3.
17. **Q: What is a sequence number for?** A: Ordering + duplicate detection + reliability (ACKs refer to seq). Initial sequence numbers are randomized (ISN randomization) to prevent spoofing. Source: P3.
18. **Q: What's the difference between cumulative ACK and selective ACK?** A: Cumulative ACK = "everything up to N received" (one number). SACK = bitmap of individual received segments — allows retransmitting only the *lost* ones, not all after the gap. Source: P3.
19. **Q: What is flow control?** A: Receiver-driven pacing: the receiver advertises a window (rwnd) in each ACK; sender never sends more than rwnd unacknowledged (prevents receiver buffer overflow). Source: P3.
20. **Q: What is congestion control vs flow control?** A: Flow = receiver buffer (rwnd). Congestion = network capacity (cwnd): sender limits in-flight data based on inferred network state (loss/ECN). Effective window = min(cwnd, rwnd). Source: P3.
21. **Q: What is slow start?** A: cwnd starts small (e.g., 10 segments) and doubles per RTT until ssthresh; exponential growth to find capacity fast. Source: P3.
22. **Q: What is congestion avoidance (AIMD)?** A: After ssthresh, cwnd grows additively (+1 segment/RTT) and on loss halves (multiplicative decrease) — the classic AIMD sawtooth. Source: P3.
23. **Q: What is the retransmission timer (RTO)?** A: Timeout waiting for an ACK; computed from RTT + variance (Karn's: ignore retransmitted samples); exponential backoff on repeated loss; fast retransmit (3 dup ACKs) triggers earlier. Source: P3.
24. **Q: What is fast retransmit and fast recovery?** A: Fast retransmit = retransmit on 3 dup-ACKs (don't wait for RTO). Fast recovery = on dup-ACKs, halve cwnd instead of slow-start (ssthresh = cwnd/2). Source: P3.
25. **Q: What is a TCP window / what limits throughput?** A: Throughput ≤ cwnd/RTT. Bandwidth-delay product: window must cover BDP or you underutilize (1000 bytes × RTT for 100 Mbps on a 1 Gbps link). Source: P3.

**Group 4 — TCP advanced (Q26-Q34)**
26. **Q: What is TCP_NODELAY / Nagle?** A: Nagle batches small sends (wait for ACK to send next). TCP_NODELAY disables it — for low-latency interactive traffic. Source: P3.
27. **Q: What is the delayed ACK?** A: Receiver holds ACK ~40 ms (or until 2 segments) to piggyback; with Nagle this causes ~40 ms stalls (fix: disable Nagle). Source: P3.
28. **Q: What is TIME_WAIT and why 2×MSL?** A: The first-closing side waits 2×MSL to ensure the final ACK and any late packets clear the network; prevents ghost-connection mixups. Source: P3.
29. **Q: What is TCP keepalive?** A: Idle probe (default 7200 s, then 75 s × 9) to detect dead peers; not the same as app-level heartbeats. Source: P3.
30. **Q: What is ECN?** A: Explicit Congestion Notification: routers mark (CE bit) instead of dropping; sender halves cwnd without a loss. Requires both ends + network support. Source: P3.
31. **Q: What are the modern congestion control algorithms?** A: CUBIC (default Linux; cubic growth for high-BDP); BBR (Google; model-based: paces at max BW × min RTT, no loss-driven); Reno (AIMD classic). Source: P3.
32. **Q: What is the difference between TCP and UDP header?** A: TCP: 20+ bytes, seq/ack/window/flags. UDP: 8 bytes — src/dst port, length, checksum. No reliability/ordering. Source: P3.
33. **Q: When would you choose UDP?** A: Low-latency, loss-tolerant or app-managed reliability: DNS, VoIP/games, video streaming, QUIC's base, monitoring. Source: P3.
34. **Q: What is QUIC and what does it solve?** A: UDP-based, HTTP/3: 0-RTT/1-RTT handshake (TLS 1.3 built-in), stream multiplexing with no head-of-line blocking, connection migration (mobile). Source: P3.

**Group 5 — UDP & applications (Q35-Q38)**
35. **Q: Name 3 classic UDP applications.** A: DNS (53), DHCP (67/68), NTP (123), TFTP (69), VoIP/RTP. Source: P2/P3.
36. **Q: What is DNS and its records?** A: Maps names→IP. A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (nameserver), TXT, SRV. Source: P2.
37. **Q: How does DNS resolution work (recursive)?** A: Resolver → root → TLD → authoritative, caching at each step; TTL governs cache freshness. Source: P2.
38. **Q: What is DHCP?** A: Dynamic Host Configuration: DORA (Discover, Offer, Request, Ack) assigns IP/gateway/DNS from a pool with leases. Source: P4.

**Group 6 — IP & addressing (Q39-Q52)**
39. **Q: What is IPv4 vs IPv6?** A: IPv4 = 32-bit (4.3B), dotted decimal, NAT-heavy. IPv6 = 128-bit, hexadecimal, built-in security/autoconfig, no broadcast, no NAT needed. Source: P4.
40. **Q: What is CIDR?** A: Classless Inter-Domain Routing: IP/prefix (e.g., 10.0.0.0/8 = 2^24 hosts); replaces classful A/B/C addressing. Source: P4.
41. **Q: What are private vs public IPs?** A: Private (RFC 1918): 10/8, 172.16/12, 192.168/16 — non-routable on the internet (NAT translates). Public: globally unique. Source: P4.
42. **Q: What is a subnet mask and how do you compute a subnet?** A: /24 = 255.255.255.0 → 256 addresses, 254 usable; network = IP AND mask; broadcast = network OR ~mask. Source: P4.
43. **Q: What are loopback, link-local, multicast, broadcast addresses?** A: 127.0.0.1 (loopback), 169.254/16 (link-local APIPA), 224/4 (multicast), 255.255.255.255 (limited broadcast). Source: P4.
44. **Q: What is NAT and its types?** A: Network Address Translation: one public IP, many private. Static, dynamic, PAT (port address translation = many-to-one). Source: P4.
45. **Q: What is the TTL/Hop Limit field?** A: Decrements each router; at 0 → ICMP time exceeded (this is how traceroute works). Source: P4.
46. **Q: What is MTU and MSS?** A: MTU = max L3 packet a link carries (Ethernet 1500). MSS = max TCP payload = MTU − IP(20) − TCP(20) = 1460 typical. Source: P4.
47. **Q: What is fragmentation?** A: IP splits packets > MTU (IPv4; IPv6 sends ICMPv6 "packet too big" instead). DF-bit prevents it; TCP avoids it via MSS negotiation. Source: P4.
48. **Q: What is ICMP used for?** A: Control/error: ping (echo), traceroute (TTL), destination unreachable, path MTU discovery (frag needed). Source: P4.
49. **Q: What is a routing protocol vs routed protocol?** A: Routed = IP (carried). Routing = how routers learn paths: RIP (distance-vector), OSPF (link-state, within AS), BGP (path-vector, between ASes). Source: P4.
50. **Q: What is BGP in one line?** A: Border Gateway Protocol: path-vector protocol exchanging reachability between ASes (internet's glue), chooses paths on AS-path length + policy. Source: P4.
51. **Q: What is an AS?** A: Autonomous System = a network under one operator with one routing policy (identified by ASN). Source: P4.
52. **Q: What is ECMP?** A: Equal-Cost Multi-Path: hashing flows across multiple equal-cost routes to a destination (used in DC fabrics and LBs). Source: P8.

**Group 7 — HTTP (Q53-Q64)**
53. **Q: What is HTTP/1.1's key characteristics?** A: Persistent connections (keep-alive), pipelining (limited), text-based, one request per connection at a time (head-of-line blocking). Source: P2.
54. **Q: What is HTTP/2's key improvements?** A: Multiplexed streams over one TCP connection (fixes HOL at HTTP layer), binary framing, header compression (HPACK), server push, stream priorities. Source: P2.
55. **Q: What is HTTP/2's remaining problem?** A: TCP-level head-of-line blocking: one lost packet stalls *all* streams (TCP ordering). Source: P2.
56. **Q: How does HTTP/3 fix HOL blocking?** A: Runs over QUIC/UDP with independent streams — a lost packet only blocks its own stream, plus 1-RTT handshake + connection migration. Source: P2.
57. **Q: What is a status code class?** A: 1xx info, 2xx success, 3xx redirect, 4xx client error, 5xx server error. Common: 200, 301/302, 304, 400, 401, 403, 404, 429, 500, 502, 503, 504. Source: P2.
58. **Q: What is a cookie vs session?** A: Cookie = client-side small token (Set-Cookie); session = server-side state keyed by a session ID (usually in a cookie). Auth is cookie/session based (or JWT). Source: P2.
59. **Q: What are HTTP caching headers?** A: Cache-Control (max-age, no-cache, no-store, s-maxage), ETag (revalidation), Last-Modified/304. Source: P2.
60. **Q: What is CORS?** A: Browser policy for cross-origin requests; server responds with Access-Control-Allow-Origin etc. It's a *browser* mechanism (not a server firewall). Source: P2.
61. **Q: What is a WebSocket and when vs HTTP?** A: Full-duplex persistent connection over a TCP upgrade (ws://); for real-time push (chat, games); HTTP for request/response. Source: P2.
62. **Q: What is SSE vs WebSocket?** A: SSE = server→client one-way over plain HTTP (EventSource, auto-reconnect); WebSocket = bidirectional. Source: P2.
63. **Q: What is REST vs gRPC?** A: REST = HTTP + JSON, resource-oriented. gRPC = HTTP/2 + protobuf, strongly typed, streaming — for internal services. Source: P2.
64. **Q: What is a CDN and what does it do?** A: Content Delivery Network: caches content at edge PoPs near users (DNS GSLB + anycast), cuts latency and origin load; also TLS/WAF/DDoS edge. Source: P2/P8.

**Group 8 — TLS & Security (Q65-Q75)**
65. **Q: What is symmetric vs asymmetric crypto?** A: Symmetric (AES): one key, fast, for bulk data. Asymmetric (RSA/ECC): key pair, slow, for key exchange/signatures. Source: P7.
66. **Q: When is each used in TLS?** A: Asymmetric authenticates (certificate + ECDHE key agreement); symmetric encrypts the bulk data (AES-GCM). Source: P7.
67. **Q: What is a hash and what is it used for?** A: One-way, deterministic digest (SHA-256); used for integrity, password storage, fingerprinting. Not reversible. Source: P7.
68. **Q: Hash vs encryption vs signing?** A: Hash = one-way integrity. Encryption = reversible secrecy. Signing = hash + private key = authenticity + non-repudiation. Source: P7.
69. **Q: Walk the TLS 1.3 handshake.** A: ClientHello (ECDHE key share) → ServerHello (its ECDHE + cipher) + cert + CertificateVerify + Finished → Finished; 1 RTT, then AEAD records. Source: P7.
70. **Q: What is forward secrecy?** A: Ephemeral ECDHE keys: even if the long-term key leaks, past sessions can't be decrypted. Mandatory in TLS 1.3. Source: P7.
71. **Q: What is a certificate chain and validation?** A: Leaf → intermediates → trusted root; check dates + SAN + signatures + revocation. Source: P7.
72. **Q: What are the common web attacks and defenses?** A: XSS (escape input/CSP), SQLi (parameterized queries), CSRF (CSRF tokens/SameSite), DDoS (rate limit/LB/scrub), MITM (TLS/pinning). Source: P7.
73. **Q: What is a DDoS and how do you mitigate?** A: Distributed DoS — volumetric (scrub/anycast/rate-limit), protocol (SYN cookies, LBs), application (WAF, per-IP limits, caching). Source: P7.
74. **Q: What is IPsec vs TLS?** A: IPsec = L3, protects all IP (VPNs, transparent). TLS = L4, per-connection (web). IPsec complex + NAT issues; TLS lightweight + 443-friendly. Source: P7.
75. **Q: What is Zero Trust in one line?** A: "Never trust, always verify": every request authenticated/authorized/encrypted regardless of source; PDP/PEP model; default deny. Source: P7.

**Group 9 — LB & architecture (Q76-Q85)**
76. **Q: L4 vs L7 load balancer?** A: L4 = 4-tuple hash, stateless, huge scale, no content awareness. L7 = TLS/HTTP/health, per-request, smart but CPU-bound. Source: P8.
77. **Q: What is GSLB?** A: DNS-level global LB: geo/ECS + latency + health + weights steer each client to the best region; cached for TTL. Source: P8.
78. **Q: What is anycast?** A: Same IP announced from many sites; BGP routes to the nearest; stateless services only; auto-failover; DDoS absorb. Source: P8.
79. **Q: What is EDNS Client Subnet?** A: Resolver sends a client /24 so the authoritative geolocates the *client*, not the resolver. Source: P8.
80. **Q: What is a CLOS/spine-leaf fabric?** A: Every leaf ↔ every spine, ECMP across equal paths; scale by adding switches; all links used. Source: P8.
81. **Q: What is VXLAN?** A: L2-in-UDP overlay (24-bit VNI), VTEP endpoints; L2 mobility + 16M segments over a routed underlay. Source: P8.
82. **Q: What is multicast used for?** A: Efficient one-to-many (IPTV, PTP, market data); IGMP joins + PIM trees; one copy per link. Source: P8.
83. **Q: What is a security group vs NACL?** A: SG = stateful, instance-level. NACL = stateless, subnet-level. Source: P8.
84. **Q: What is the bandwidth-delay product?** A: BDP = bandwidth × RTT = data in flight at full speed; the window must cover it (100 Gbps × 100 ms = 1.25 GB). Source: P3/P6.
85. **Q: How do you scale a single-server app to millions of users?** A: LB tier (L4/L7) → horizontally scale stateless app → cache (CDN/Redis) → DB tier (read replicas/sharding) → TLS + DDoS edge → GSLB/anycast globally. Source: P8.

**Group 10 — Wireless & media (Q86-Q90)**
86. **Q: How does Wi-Fi avoid collisions (CSMA/CA)?** A: Listen-before-talk + random backoff + ACK; RTS/CTS for hidden nodes. Unlike Ethernet (CSMA/CD) — wireless can't detect collision while transmitting. Source: P5.
87. **Q: 2.4 vs 5 vs 6 GHz trade-offs?** A: Lower = better range/walls, worse congestion; higher = faster, shorter range. 6 GHz (Wi-Fi 6E/7) = new capacity. Source: P5.
88. **Q: What is Shannon's capacity?** A: C = B·log2(1+SNR) — max error-free rate given bandwidth and signal-to-noise. Source: P6.
89. **Q: What is Nyquist's limit?** A: Max symbol rate = 2×B; with M levels, rate = 2B·log2(M) — why you use QAM to push bits/symbol. Source: P6.
90. **Q: Fiber vs copper?** A: Fiber: high bandwidth, long distance (100 km+), immune to EMI; copper (Cat6): short (<100 m), cheap, good for DC/access. Source: P6.

**Group 11 — Protocols & services (Q91-Q95)**
91. **Q: What is DNS over HTTPS (DoH)?** A: DNS queries tunneled in HTTPS (443) to prevent snooping/poisoning on the wire; privacy + integrity trade-off (resolver visibility). Source: P2/P7.
92. **Q: What is a VPN and its two main types?** A: Site-to-site (IPsec tunnel between gateways) and remote-access (IPsec IKEv2 / WireGuard / TLS VPN); encrypts traffic to a trusted network. Source: P7.
93. **Q: What is SSH used for and how is it secured?** A: Remote shell/file transfer over an encrypted channel; host keys (TOFU) + password/publickey auth; multiplexed channels/port-forwarding. Source: P7.
94. **Q: What is mTLS?** A: Mutual TLS — both sides present certs; service-to-service identity + encryption in meshes. Source: P7.
95. **Q: What is a jump host / bastion?** A: A hardened entry point you SSH into to reach internal hosts; narrows the attack surface. Source: P7.

**Group 12 — Troubleshooting & numbers (Q96-Q100)**
96. **Q: You see high TCP retransmissions. What do you check?** A: Packet loss (tcpdump, drop counts), congestion (cwnd), MTU/MSS mismatch, buffer limits, network congestion; correlate RTO/retransmits with drop graph. Source: P3/P8.
97. **Q: What does a 504 Gateway Timeout mean and where do you look?** A: A proxy/LB waited too long for upstream. Check upstream health, timeouts, app slowness, LB→app connectivity (not the client). Source: P2/P8.
98. **Q: What are the first commands for a latency complaint?** A: ping (reachability/RTT), mtr (path + per-hop loss), ss/netstat (connections), dig (DNS time), curl -w (total time breakdown), iperf (bandwidth). Source: P8.
99. **Q: What is the difference between RTT, ping latency, and packet loss?** A: RTT = round-trip time of a probe; ping shows min/avg/max; loss = % dropped — both degrade TCP (loss halves cwnd). Source: P3/P6.
100. **Q: How do you tell if a problem is network vs application?** A: Reproduce with curl -w (split DNS/TCP/TLS/first-byte/total), check server-side logs vs client-side, tcpdump on both ends, compare throughput (iperf) vs app throughput. Source: P8.

## 14. Follow-Up Questions
1. **Q: What do you do when you answer a question wrong in a drill?** A: Don't just re-read — re-answer with the Source section open, then re-drill it in 24h and again in 3 days (spaced repetition); phrase it out loud each time.
2. **Q: How deep should an answer be?** A: 2-3 sentences + a concrete example (a port, a number, a packet trace). Depth = the Source section's 22-block treatment; the bank answer is the elevator version.
3. **Q: How do I convert this bank into system-design strength?** A: For each Q, ask "how does this behave at 1M QPS?" — e.g., TCP keepalive → "proxies cap idle; use app heartbeats"; cookies → "JWTs with short TTL behind an LB." Cross-wire with Section 02.

## 15. Coding Example
```python
# Self-quiz helper: shuffle the bank, show a question, check your recall
import random

bank = [
    ("What does the 3-way handshake look like?", "SYN -> SYN+ACK -> ACK"),
    ("L4 vs L7 load balancer?", "L4 hashes 4-tuple; L7 parses HTTP/TLS"),
    ("What is BDP?", "bandwidth x RTT = in-flight bytes needed"),
    ("What does TLS 1.3 fix?", "1-RTT, forward secrecy, AEAD-only"),
    ("What is anycast?", "same IP from many sites; routing picks nearest"),
]
q, a = bank[random.randrange(len(bank))]
print(f"Q: {q}\nA (reveal after you answer): {a}")
```
```bash
# Pair the bank with real-world verification of the claims
curl -s -w "dns=%{time_namelookup} tcp=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer}\n" -o /dev/null https://example.com
ss -t state established | head                       # see real TCP state machines
dig +short example.com                               # see DNS in action
mtr -rn -c 10 1.1.1.1                                # anycast + path RTT
```

## 16. Industry Usage
The rapid-fire format is standard at **Meta** (fast fundamentals before system design), **Microsoft/AWS loops**, **Stripe/Cloudflare phone screens**, and every networking/infra role. It's also the format of certification exams (CCNA-style) and SRE on-call readiness.

## 17. References
- Each answer's Source tag points to the exact part/section for depth.
- RFC index: TCP (793/7323), UDP (768), IP (791/8200), DNS (1035), HTTP (9110/9113/9114), TLS (8446), BGP (4271), VXLAN (7348), ECMP (2992).
- Kurose & Ross, *Computer Networking*, 8th ed., for the canonical deep dives.

## 18. Cheat Sheet
- Drill format: cover → answer aloud → reveal → mark miss → re-drill 24h/3d.
- 60-second target per answer; 2-3 sentences + an example.
- Groups: Layers, Link, TCP, UDP, IP, HTTP, TLS, LB/Arch, Wireless, Services, Troubleshooting.
- Misses map to Source → read that section → re-quiz.
- Pair with Section 02 (design) and Section 03 (coding/Linux) for the full skill stack.

## 19. Quiz
1. TCP is: a) connectionless b) reliable, ordered byte stream c) UDP-based d) L2 → **b**
2. TLS 1.3 handshake RTTs: a) 2 b) 1 c) 0 d) 3 → **b**
3. Anycast picks the node by: a) DNS b) routing c) health d) GeoIP → **b**
4. Security group is: a) stateless subnet b) stateful instance c) DNS d) routing → **b**
5. BDP = a) bandwidth + RTT b) bandwidth × RTT c) MTU/RTT d) cwnd only → **b**
6. Which fixes HTTP/2's HOL blocking? a) TCP Fast Open b) QUIC c) keepalive d) Nagle → **b**
7. ECN signals congestion by: a) drop b) marking bits c) RST d) ICMP → **b**
8. SHA-256 is a: a) cipher b) hash c) signature d) MAC → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: 3-way handshake** → **A:** SYN → SYN+ACK → ACK.
- **Q: L4 vs L7 LB** → **A:** 4-tuple hash vs HTTP/TLS-aware.
- **Q: What limits TCP throughput?** → **A:** min(cwnd,rwnd)/RTT; window must cover BDP.
- **Q: HTTP/2's remaining problem** → **A:** TCP head-of-line blocking; QUIC/HTTP/3 fixes it.
- **Q: TLS 1.3 highlights** → **A:** 1-RTT, mandatory ECDHE (forward secrecy), AEAD-only.
- **Q: Anycast** → **A:** same IP, nearest via routing, stateless-only.
- **Q: Shannon** → **A:** C = B·log2(1+SNR).

## 21. Revision
This bank = the roadmap as a recall test. Core anchors to keep instantly: **TCP** (SYN/SYN-ACK/ACK, seq/ack, rwnd vs cwnd, slow start → AIMD, RTO + fast retransmit, BDP = window size); **IP** (CIDR, RFC1918, MTU/MSS, TTL, NAT/PAT, BGP = AS path); **HTTP** (1.1 HOL → 2.0 streams/HPACK → 3.0/QUIC kills TCP HOL); **TLS 1.3** (1-RTT, ECDHE forward secrecy, AEAD, cert chain); **LB/Arch** (L4→L7→GSLB→anycast, spine-leaf/ECMP, VXLAN/EVPN); **Security** (XSS/SQLi/CSRF/DDoS, IPsec vs TLS, Zero Trust); **Numbers** (MTU 1500, MSS 1460, ports 0-65535, TTL 64, MSL 120s, BDP formula). Drill daily, go deep on misses, then move to design + hands-on.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| The entire 100-question bank (Q1-Q100) | 13-Q1..Q100 |
| "Walk the 3-way handshake" | 13-Q15 |
| "TCP vs UDP" | 13-Q13/32 |
| "What is congestion control?" | 13-Q20-24 |
| "HTTP/1 vs 2 vs 3" | 13-Q53-56 |
| "Walk TLS 1.3" | 13-Q69 |
| "L4 vs L7 LB" | 13-Q76 |
| "What is anycast?" | 13-Q78 |
| "BDP / what limits TCP?" | 13-Q25/84 |
| "Shannon / Nyquist" | 13-Q88/89 |
| "How do you debug latency?" | 13-Q98 |
