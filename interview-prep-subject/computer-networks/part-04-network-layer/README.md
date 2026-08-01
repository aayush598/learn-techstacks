# Network Layer

> **TL;DR**: The network layer gets packets from any source to any destination — IP addressing (IPv4/IPv6), datagram formats, ICMP/ARP helper protocols, and the routing algorithms (distance-vector, link-state, path-vector) that compute the forwarding tables — plus the scale-out machinery (NAT, VPNs, load balancing, CDNs, QoS) that makes the Internet actually work.

## Part Roadmap
- **IP addressing**: IPv4 classes/subnetting/CIDR, IPv6, special addresses, and subnet math.
- **IP + helper protocols**: IPv4 datagram format, ARP/RARP, ICMP + traceroute internals.
- **Routing**: static, distance-vector (RIP/Bellman-Ford), link-state (OSPF/Dijkstra), path-vector (BGP), and how forwarding tables are built.
- **Advanced networking**: NAT/PAT, VPNs/IPsec, load balancing, CDNs, QoS.
- **The big questions**: "How does a packet find its way?", "What is subnetting?", "How does BGP work?", "What is NAT?", "How does traceroute work?"

## Chapter Files
- `chapter-01-ip-addressing/` — IPv4 classes & addressing, subnetting & CIDR, IPv6.
- `chapter-02-ip-and-icmp/` — IPv4 datagram format, ARP/RARP, ICMP & traceroute.
- `chapter-03-routing/` — fundamentals & static, distance-vector (RIP), link-state (OSPF), path-vector (BGP).
- `chapter-04-advanced-networking/` — NAT/PAT, VPN/IPsec, load balancing, CDN, QoS.

## Interview Q&A Preview
- **"What is subnetting and why CIDR?"** → Subnetting carves an IP block into networks for routing/security; CIDR (RFC 4632) replaced classful addressing with prefix-length notation, ending the waste of class A/B/C fixed boundaries — the Internet runs on /0–/32 prefix math.
- **"How does BGP choose paths?"** → Not shortest-path! BGP is a **path-vector** protocol: it propagates full AS paths and applies policy (local pref, AS path length, MED) to pick the best route — economics and policy, not distance, drive inter-AS routing.
- **"How does NAT work and why is it controversial?"** → NAT rewrites IP+port tuples at a gateway (PAT), letting thousands of private hosts share one public IP — it bought IPv4 time but breaks end-to-end, kills inbound connections, and complicates P2P (the reason IPv6 exists).

## Key Diagrams to Recreate
1. **Subnet math**: 192.168.1.0/24 → subnet mask 255.255.255.0, network/broadcast/host ranges.
2. **IPv4 vs IPv6 header** (20 bytes vs 40 bytes, simplified).
3. **Routing algorithms table**: distance-vector (distributed Bellman-Ford, count-to-infinity) vs link-state (Dijkstra, LSA flooding) vs path-vector (AS paths + policy).
4. **NAT flow**: private 192.168.1.5:50000 → NAT → public 203.0.113.7:50000 → internet; return path reversed.
5. **Packet journey**: host → ARP → gateway → routing → ICMP/TTL → next hop → destination.
