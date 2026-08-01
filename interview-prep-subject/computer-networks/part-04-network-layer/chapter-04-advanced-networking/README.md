# Advanced Networking

> **TL;DR**: The scale-out machinery that makes the Internet usable — **NAT/PAT** (many private hosts share one public IP), **VPNs/IPsec** (encrypted tunnels over untrusted networks), **load balancing** (L4–L7, global GSLB), **CDNs** (content pushed to the edge), and **QoS** (classify + prioritize + police the traffic that fights for bandwidth).

## Chapter Roadmap
- **NAT & PAT**: static/dynamic NAT, port address translation, the NAT table, why it's controversial, and how it breaks end-to-end (and why IPv6 removes it).
- **VPN, tunneling & IPsec**: tunneling protocols (GRE, IPsec, WireGuard, SSL VPNs), IKE key exchange, tunnel vs transport modes, and the "private network over the public Internet."
- **Load balancing at scale**: L4 (TCP/UDP) vs L7 (HTTP) load balancing, algorithms (round-robin, least-connections, IP hash), health checks, session affinity, and global GSLB (DNS-based).
- **CDNs**: content caching at edge PoPs, anycast, cache hit/miss, TTLs, purge, and how Cloudflare/CloudFront/Akamai accelerate the web.
- **QoS & traffic management**: classification, marking (DSCP), shaping/policing, queues (PQ, WFQ), congestion avoidance (WRED), and the priority/cost tradeoffs.

## Section Files
- `section-01-nat-and-pat.md` — NAT types, PAT, NAT table, hole punching, and IPv6.
- `section-02-vpn-tunneling-and-ipsec.md` — tunnels, IPsec/IKE, WireGuard, TLS VPNs.
- `section-03-load-balancing-at-scale.md` — L4/L7 LB, algorithms, health checks, GSLB.
- `section-04-content-delivery-networks-cdn.md` — caching, anycast, TTL, purge, cache misses.
- `section-05-qos-and-traffic-management.md` — classification, DSCP, shaping/policing, queues, WRED.

## Interview Q&A Preview
- **"How does NAT work?"** → A NAT/PAT gateway rewrites the source IP+port of outgoing packets (keeping a mapping in its table) and rewrites them back on return — one public IP serves thousands of private hosts. It buys IPv4 time, but breaks inbound connections (no table entry → no return path) and complicates P2P, which is why IPv6 pushes end-to-end addressing.
- **"Load balancing: L4 vs L7?"** → L4 balances TCP/UDP sessions (IP+port, fast, protocol-agnostic); L7 balances HTTP requests (reads headers/cookies/path, does routing, TLS termination, and app-aware decisions like sticky sessions). Modern stacks use both: L4 at the edge, L7 in the app tier.
- **"Why do CDNs make the web faster?"** → Content is cached at PoPs *closer to the user* (anycast DNS → nearest PoP → shorter RTT). Cache hits serve from the edge (no origin round-trip); TTLs and purges keep it fresh. Faster = lower latency + offloaded origin + resilience under load (your CDN absorbed the spike).
- **"What is QoS and how is it applied?"** → Classify traffic (voice/video/bulk), mark it (DSCP), then queue + schedule: high-priority classes jump the queue (PQ/WFQ), while shaping/policing and WRED (early drop) keep queues bounded. QoS doesn't add bandwidth — it *allocates* congestion fairly by priority.
