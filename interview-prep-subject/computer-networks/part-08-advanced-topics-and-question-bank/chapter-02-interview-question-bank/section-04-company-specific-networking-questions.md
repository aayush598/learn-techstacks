# Company-Specific Networking Questions

> **TL;DR**: Pattern-matched by company and role: Google (load balancing, BGP, HTTP/3, CLOS), Meta (rapid-fire TCP/HTTP + design), Amazon (TCP + LP-wrapped systems design), Microsoft (Windows networking, TCP/IP internals), Cloudflare (anycast, TLS, DDoS, edge), Netflix (CDN, streaming, long-fat-network TCP), Uber (geo/LBS latency), Stripe (HTTP/API, TLS, idempotency), plus wireless/embedded networking.

## 1. Why Does This Exist?
Different companies test networking at different depths because they *run* different things: Cloudflare's product IS anycast/TLS/DDoS, so they probe it to staff depth; Meta/Google ask rapid fundamentals before a design; Amazon wraps networking in leadership-principle-flavored system design; Netflix lives on TCP over long-fat networks with massive CDNs. Knowing *which* questions a company leans on lets you spend your study time where it pays — and it demystifies "what will they ask me here?". This section maps each major interviewer to its question patterns, with sample questions and the exact source sections to master.

## 2. How Does It Work?
For each company/role: (1) the company's *network reality* (what they run, at what scale), (2) the question *pattern* (rapid-fire vs design vs deep-dive vs debugging), (3) 6-10 *representative questions*, (4) the *source sections* to master for it. Study order: read the company you're targeting, drill its question set against Section 01's bank, and go deep on the cited sections. The meta-pattern: **every company** mixes (a) fundamentals speed, (b) one deep topic relevant to their infra, and (c) a design. Prepare all three per target.

## 3. When Is It Used?
- The final 1-2 weeks before a specific company's loop (after the general bank in Section 01).
- Multiple loops: prepare the shared core (TCP/UDP/HTTP/DNS/TLS) once, then the company-specific deep-dive.
- Phone screens: usually the shared core + one company flavor.

## 4. Why Wasn't Another Approach Chosen?
- *One generic prep:* different depths per company mean generic prep over- or under-shoots — Cloudflare-level TLS depth wasted at a place that only asks HTTP, or vice versa.
- *Memorizing "expected" questions:* questions are recycled but you must *answer with reasoning*; the section's value is the *depth map*, not a script.
- *Skipping the core:* company-specific questions sit on the shared core (Section 01); this section is the seasoning, not the meal.

## 5. Intuition
Companies interview in their own **dialect of the same language**. The core (TCP, HTTP, DNS, TLS, LB) is the grammar everyone shares; each company's dialect is the accent they test — Google tests the load-balancer/BGP grammar heavily, Netflix tests the TCP-over-long-links grammar, Cloudflare tests the anycast/TLS grammar. Learn the shared grammar first, then drill the accent of your target company.

## 6. Real-World Analogy
A **trucking company hiring across divisions**. The basics (driving, roads) are universal — everyone is tested on them. The cross-country division (Netflix) tests range/fuel/long-haul strategy; the city-delivery division (Uber) tests traffic/latency/short-route optimization; the port-authority division (Cloudflare) tests docking, cranes, and storm handling (DDoS). You still have to drive well everywhere — but you'd prepare the long-haul metrics before the cross-country interview and the port-storm playbook before the port-authority one.

## 7. Formal Definition
- **The shared core (any company)**: TCP/UDP semantics, HTTP/1.1-2-3, DNS resolution, TLS 1.3, IP/CIDR/NAT, LB tiers, CDN, and a system-design answer — Sections 01-02 of this chapter.
- **Company deep-dives**: each company's "dialect" — the infra-specific depth they test (below).

## 8. Example
**Google-style sample loop:**
```
Round 1: "What is a load balancer and the different types?" (L4/L7, GSLB)
Round 2: "How does BGP work? What are BGP communities?" (path-vector, policy)
Round 3: "Design a service that serves the globe with <100ms latency." (GSLB + anycast + CDN)
Round 4: "What is HTTP/3 and how is it different from HTTP/2?" (QUIC, HOL, 0-RTT)
The depth: Google's global scale → GSLB/anycast/BGP/CLOS are their home turf.
```

## 9. Internal Working — per company

**Google**
- Reality: global-scale search, YouTube, GCP; runs GSLB, anycast, BGP, Jupiter fabric, B4 SDN WAN.
- Pattern: fundamentals + global-systems depth + design; expects numbers.
- Sample: "L4 vs L7 LB + GSLB?"; "How does BGP pick a path?"; "What are BGP communities/policy?"; "Why anycast for DNS?"; "Design a global API with <100ms p95"; "What is HTTP/3/QUIC and when would you use it?"; "What is a CLOS/Jupiter fabric?"; "How do you make a design region-resilient?"
- Master: Section 08-01 (GSLB/anycast/EDNS), 08-03 (CLOS/DC), 13-BGP (P4), QUIC (P3), Section 02 (design).

**Meta (Facebook)**
- Reality: massive social graph, real-time (WhatsApp/Messenger), CDN at scale, custom LB (L4: L4LB, L7: Proxygen).
- Pattern: *fast* rapid-fire fundamentals then design; expects crisp definitions, no rambling.
- Sample: "TCP vs UDP + example?"; "3-way handshake flags?"; "How does a CDN work?"; "How does DNS resolve?"; "What's in a TLS handshake?"; "Design chat at 1B users"; "How do you scale a single service to millions?"; "What causes TCP retransmissions?"
- Master: Section 01 bank speed drill, Section 02 chat/design, P2/P3 protocols, P8 edge.

**Amazon**
- Reality: AWS infra, retail; LB-heavy (ALB/NLB), VPC, S3 scale; interviews wrap tech in LP stories.
- Pattern: LP ("tell me about a time...") + fundamentals + design; debugging/troubleshooting heavy.
- Sample: "Design a URL shortener / e-commerce API"; "What's the difference between ALB and NLB?"; "How does AWS VPC networking work?"; "What is a security group vs NACL?"; "How do you debug high latency in a microservice?"; "What's a DDoS and how do you mitigate?"; "Explain TCP slow start"; "S3 is 99.99% durable — how does that work at the network layer?"
- Master: P8 (VPC/LB/SG/NACL), P3 (congestion), P7 (DDoS/TLS), Section 02, LP framing.

**Microsoft**
- Reality: Windows networking stack, Azure, Windows TCP/IP internals, SMB, DirectServerReturn (DSR) LBs.
- Pattern: TCP/IP internals + Windows-specific + cloud design; expects precise definitions.
- Sample: "Explain the Windows TCP/IP receive path"; "What is DSR and how does an LB use it?"; "What is SMB and how is it secured?"; "How does Azure LB work?"; "What is the difference between a segment, packet, and frame?"; "How do you trace a connection in Windows (netstat, netsh, ETW)?"; "What is Nagle's algorithm and when does it hurt?"
- Master: P3 (TCP internals, Nagle), P8 (LB/DSR), P5 (frames/MAC), P7 (TLS/SMB security), Windows tooling (netsh, Get-NetTCPConnection).

**Cloudflare**
- Reality: their product IS the edge — anycast, TLS, DDoS, WAF, DNS, Workers.
- Pattern: deep-dive edge + security + attack defense; expects operational fluency.
- Sample: "How does anycast work and why do you use it?"; "How does a DDoS get absorbed?"; "Walk the TLS 1.3 handshake and explain 0-RTT replay"; "How does your DNS resolve and how does EDNS help?"; "What is a certificate chain and how do you validate it?"; "Design a global edge with <100ms for everyone"; "What's in a TCP connection today and how do you fix retransmits at the edge?"; "How do you serve 1M TLS connections at a PoP?"
- Master: Section 08-01/02 (anycast, GSLB), P7 (TLS, DDoS, certs), P3 (TCP at scale), Section 03 (kernels/edge).

**Netflix**
- Reality: streaming CDN (Open Connect appliances in ISP peering), TCP over long-fat networks, ABR, massive egress.
- Pattern: streaming/CDN/TCP-depth + design; expects real-world scale numbers.
- Sample: "How does a CDN reduce cost + latency for video?"; "What is TCP tuning over a long-fat network (BBR)?"; "How does adaptive bitrate work?"; "What is a manifest and how does DASH/HLS work?"; "Why cache at the edge instead of unicast everything?"; "Design video streaming for 1M concurrent viewers"; "What happens when a cache misses?"; "How do you measure and improve QoE (rebuffer)?"
- Master: P3 (TCP/BBR/BDP), P8 (CDN/edge), P2 (HTTP/streaming), Section 02 (streaming design).

**Uber**
- Reality: geo/real-time (dispatch, maps, ride matching), mobile clients, latency-critical.
- Pattern: latency + geo + mobile + design; expects latency math and mobile constraints.
- Sample: "How do you reduce mobile API latency?"; "What is the latency budget for a ride request?"; "Design a real-time ride-matching system"; "How do you handle a cellular network outage for drivers?"; "What is the difference between WebSocket and HTTP for live tracking?"; "How does GPS/geofencing data flow through the network?"; "Design geo-distributed dispatch with GSLB."
- Master: P3 (UDP/QUIC/WebSocket), P8 (GSLB/anycast/edge), P2 (mobile protocols), Section 02 (real-time design).

**Stripe**
- Reality: payments, HTTP APIs, idempotency, TLS/mTLS, rate limits, global API gateway.
- Pattern: API/TLS/HTTP-depth + security + design; expects correctness and edge cases.
- Sample: "Design a payments API with idempotency"; "How does mTLS work and why for service-to-service?"; "What is rate limiting and how do you implement it at the gateway?"; "Walk a TLS handshake for a payment page"; "What is the difference between idempotent and safe methods?"; "How do you secure an API against replay/MITM?"; "Design an API gateway for global payments."
- Master: P7 (TLS, mTLS, attacks), P2 (HTTP/API design), P8 (gateway design), Section 02.

**Wireless/Embedded/Network-engineering roles (Arista/Cisco/NVIDIA/carrier)**
- Reality: L2/L3 protocols, wireless (Wi-Fi/5G), physical layer, network hardware.
- Pattern: protocol depth + config/debug + math.
- Sample: "Walk CSMA/CA in Wi-Fi"; "What is STP and how does RSTP differ?"; "What is OSPF vs BGP?"; "What is Shannon/Nyquist and compute a rate"; "How does a VLAN tag work?"; "What is IGMP snooping?"; "Explain MPLS and how it differs from IP routing"; "What is a MACsec/802.1X and where does it sit?"
- Master: P4 (routing), P5 (L2/Wi-Fi/STP/VLAN), P6 (signals/physical), P8 (multicast), Section 03.

## 10. Time Complexity / Performance
- Prep time: shared core (Section 01) = 5-7 days; company deep-dive = 2-3 days; design (Section 02) = ongoing daily. Total ~2 weeks focused.
- The high-leverage 20%: TCP (congestion + handshake), HTTP/1-3 differences, DNS resolution + GSLB, TLS 1.3, one strong design with numbers. Master that before any company flavor.

## 11. Advantages
Targeted prep (study the dialect that pays); avoids over-preparing deep TCP for a pure-API role or under-preparing anycast for Cloudflare; demystifies "what do they even ask here?"; the depth map doubles as a gap list per company.

## 12. Disadvantages
Patterns drift (companies pivot their infra and questions); the sections can't guarantee "the exact question" — they guarantee the *depth*. Also: don't skip the shared core — over-indexing on one company's flavor under-prepares the fundamentals everyone tests.

## 13. Interview Questions (this section's own Q&A)
1. **Q: How do I prep for Google's networking loop?** A: Master global systems: GSLB/anycast/EDNS (Section 08-01), BGP + policy (P4), CLOS/DC fabric (08-03), HTTP/3/QUIC (P3), and a design with numbers + region-resilience (Section 02). Expect rapid fundamentals + one global design.
2. **Q: How do I prep for Cloudflare?** A: Edge and security depth: anycast (08-02), DDoS absorption (P7), TLS 1.3 + certs + pinning (P7), EDNS (08-01), TCP at the edge (P3), kernel/socket fluency (Section 03). Expect operational "how do you actually run X" questions.
3. **Q: How do I prep for Netflix?** A: Streaming + CDN + TCP-over-fat-network: CDN/edge caching (P8), TCP BBR/tuning + BDP (P3), DASH/HLS/ABR manifests (P2), streaming design (Section 02). Expect real numbers (Mbps/viewer, cache-hit ratios, egress).
4. **Q: How do I prep for Amazon?** A: LB/VPC depth + LP-wrapped systems design: ALB/NLB (P8), VPC/security groups/NACL (P8), congestion/TCP (P3), DDoS/TLS (P7), design (Section 02) — and frame every behavioral answer with a leadership principle (ownership, earn trust, dive deep).
5. **Q: How do I prep for a network-engineer/Arista-Cisco role?** A: Protocol depth: L2 (STP/VLAN/802.1X — P5), routing (OSPF/BGP — P4), Wi-Fi CSMA/CA (P5), Shannon/Nyquist math (P6), MPLS, multicast (P8), plus config/debug fluency (Section 03).
6. **Q: TRICKY — What's the *same* thing every company tests?** A: The shared core: TCP handshake + congestion, HTTP/1.1→2→3, DNS resolution, TLS 1.3, one LB/Cache/CDN design with numbers, and a debugging scenario (retransmits/latency). Master these once; company flavor sits on top.
7. **Q: What's the biggest prep mistake?** A: Memorizing company "question lists" instead of the *depth* — interviewers vary questions within a fixed depth band. Study the depth map; the questions follow.
8. **Q: How do I prep for a pure systems/backend role that "doesn't do networking"?** A: Still master TCP (why a service stalls), HTTP/2/3 (why the API is slow), TLS (why certs expire), LB/cache (how it scales), and one design — these are 30% of any backend loop even when it isn't labeled "networking."

## 14. Follow-Up Questions
1. **Q: What is DSR (Direct Server Return)?** A: An LB technique where the LB handles inbound traffic but the backend replies *directly* to the client (bypassing the LB on the return path) — used by Microsoft/Azure/HAProxy/F5 for high scale; halves LB load and latency on responses (Section 08-03 LB tier).
2. **Q: What is QoE in streaming and how do you measure it?** A: Quality of Experience: rebuffer ratio, startup time, bitrate ladder — measured via client telemetry (not network probes); the product-level metric behind CDN/TCP choices (Section 02 streaming).
3. **Q: What is BBR and why does Netflix use it?** A: Google's congestion control: models the path (max bandwidth × min RTT) and paces sends — recovers faster on loss, better on high-BDP/lossy paths (satellite/long-haul) than loss-based CUBIC. Perfect for video over long-fat networks (P3).
4. **Q: What is a "long-fat network" (LFN)?** A: High bandwidth × high delay (e.g., 100 Gbps × 100 ms): the BDP is enormous (1.25 GB), so TCP windows/buffers must be huge or the pipe idles; loss-based CC collapses on 1% loss — exactly why BBR/Reno-with-large-windows and CDN edge placement matter (P3/P8).

## 15. Coding Example
```python
# A company-agnostic "first 5 minutes of a network incident" runbook script
import subprocess, socket

def check(host="example.com"):
    cmds = [
        f"ping -c 3 {host}",                     # reachability + RTT
        f"mtr -rn -c 5 {host} 2>/dev/null | tail -5",   # path + per-hop loss
        f"curl -s -o /dev/null -w '%{{time_namelookup}} %{{time_connect}} "
        f"%{{time_appconnect}} %{{time_starttransfer}} %{{time_total}}\n' https://{host}",  # stage timing
        "ss -s",                                 # TCP state summary (timewait/retrans)
        "ss -ti | head -5",                      # cwnd/rtt/mss of live conns
    ]
    for c in cmds:
        print(f"$ {c}")
        print(subprocess.run(c, shell=True, capture_output=True, text=True).stdout)
check()
```
```bash
# Company-flavored probes
# Cloudflare-style: inspect the edge/TLS chain you're hitting
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | grep -E "issuer|Protocol|Cipher"
dig +short example.com @1.1.1.1                 # anycast resolver working?
# Netflix-style: measure the CDN edge + TCP health of a stream (conceptual):
iperf3 -c cdn-host -R -t 10                     # reverse path bandwidth
# Google-style: compare HTTP/2 vs HTTP/3 latency if h3 is available (via curl --http3)
curl --http2 -s -o /dev/null -w "%{time_total}\n" https://www.google.com
```

## 16. Industry Usage
This section's patterns come from real, published interview signals: Cloudflare's blog posts on edge/TLS/DDoS; Netflix's techblog on TCP/Open Connect; Google's SRE book + load-balancer papers; Microsoft/Azure engineering posts; Amazon AWS networking docs. Where the specific company is opaque, the shared-core + dialect approach still lands the majority of questions.

## 17. References
- Company engineering blogs: Netflix TechBlog (TCP, Open Connect), Cloudflare blog (anycast, TLS, DDoS), Google Cloud/blog (Jupiter, B4, GSLB), Meta engineering (LBs, Proxygen), AWS/Azure docs (VPC, LB).
- Section 01 (shared core), Section 02 (design), Section 03 (hands-on) — the three prep layers.
- RFCs: TCP (9293), HTTP/2 (9113), HTTP/3 (9114), TLS 1.3 (8446), BGP (4271), VXLAN (7348).

## 18. Cheat Sheet
- Shared core (all): TCP handshake/congestion, HTTP/1-2-3, DNS, TLS 1.3, LB/CDN design, a debugging scenario.
- Google: GSLB/anycast/BGP/CLOS + global design with numbers.
- Meta: FAST rapid-fire + chat/social design.
- Amazon: ALB/NLB/VPC/SG/NACL + LP-framed design.
- Microsoft: TCP internals, DSR, SMB, Windows tools (netsh/Get-NetTCPConnection).
- Cloudflare: anycast, DDoS absorb, TLS/certs depth, edge ops.
- Netflix: CDN/edge, BBR/BDP, ABR/manifest, streaming numbers.
- Uber: latency budget, mobile, real-time dispatch design.
- Stripe: API/TLS/mTLS, idempotency, gateway + rate limiting.
- Wireless/network-eng: L2/L3 protocols, Wi-Fi, Shannon/Nyquist, MPLS.
- Don't skip the core; depth map > question list.

## 19. Quiz
1. Cloudflare's home turf: a) video codecs b) anycast + TLS + DDoS c) SMB d) GPS → **b**
2. Netflix's home turf: a) BGP b) TCP over long-fat networks + CDN c) Windows d) MPLS → **b**
3. Amazon tests you on: a) BGP policy b) ALB/NLB + VPC + LP design c) anycast d) Wi-Fi → **b**
4. The shared core for ALL companies: a) TCP + HTTP + DNS + TLS + LB b) only design c) only coding d) none → **a**
5. Google's global design lever: a) SMB b) GSLB/anycast/BGP/CLOS c) IGMP d) TLS only → **b**
6. Stripe's signature question: a) design payments API with idempotency b) DDoS c) STP d) QAM → **a**
7. DSR is: a) a codec b) LB where backend replies directly c) a routing proto d) a TLS mode → **b**
8. BBR is preferred for: a) tiny RTTs b) high-BDP/lossy paths c) L2 d) UDP only → **b**

**Answers**: 1-b, 2-b, 3-b, 4-a, 5-b, 6-a, 7-b, 8-b.

## 20. Flashcards
- **Q: Google deep-dive topics** → **A:** GSLB/anycast/BGP/CLOS + global design.
- **Q: Cloudflare deep-dive** → **A:** anycast, DDoS absorb, TLS/cert depth, edge ops.
- **Q: Netflix deep-dive** → **A:** CDN edge, BBR/BDP, ABR, streaming numbers.
- **Q: Amazon deep-dive** → **A:** ALB/NLB, VPC/SG/NACL, LP-framed design.
- **Q: Stripe deep-dive** → **A:** API/TLS/mTLS, idempotency, gateway rate limiting.
- **Q: Shared core for all** → **A:** TCP, HTTP/1-3, DNS, TLS 1.3, LB/cache design, debugging.
- **Q: DSR** → **A:** LB terminates inbound; backend replies straight to client.
- **Q: BBR** → **A:** model-based CC (max BW × min RTT) for long-fat/lossy paths.

## 21. Revision
Every company tests the same core: TCP (handshake, congestion, tuning), HTTP/1→2→3 (multiplexing, HOL, QUIC), DNS (resolution, caching, GSLB), TLS 1.3 (1-RTT, forward secrecy, certs), LB/cache/CDN (tiers, anycast, edge), and a debugging story (latency, retransmits, drops). Company dialects: Google = global routing/LB/BGP/CLOS; Cloudflare = anycast/TLS/DDoS/edge ops; Netflix = TCP-over-fat-networks/CDN/ABR; Amazon = AWS LB/VPC/LP-design; Meta = fast fundamentals + chat/social design; Microsoft = TCP internals/DSR/SMB; Uber = latency/mobile/real-time; Stripe = API/TLS/idempotency; network-eng = L2/L3/Wi-Fi/math. Anchors: *master the core once, then the dialect; depth map > memorized questions; every loop = fundamentals + one deep topic + a design.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do I prep for Google/Cloudflare/Netflix/Amazon?" | 13-Q1..Q5 |
| "What does every company test the same?" | 13-Q6 |
| "What is DSR?" | 14-Q1 |
| "What is QoE / how measured?" | 14-Q2 |
| "Why does Netflix use BBR?" | 14-Q3 |
| "What is a long-fat network?" | 14-Q4 |
| "First 5 minutes of a network incident" | 15 (runbook) |
| "Biggest prep mistake?" | 13-Q7 |
| "Backend role that 'doesn't do networking'?" | 13-Q8 |
