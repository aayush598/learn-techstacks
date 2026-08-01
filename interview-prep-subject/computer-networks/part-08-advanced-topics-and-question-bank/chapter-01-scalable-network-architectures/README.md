# Chapter: Scalable Network Architectures

## What this chapter covers
How the internet's big systems survive global scale: **Global Load Balancing** (DNS anycast, EDNS, GeoIP, GSLB health-aware steering), **Anycast vs Multicast vs Broadcast** (when each is right, and the protocols that use them — DNS/DDoS scrubbing, IPTV/PTP, ARP/DHCP), and **Datacenter & Cloud Networking** (CLOS/spine-leaf fabrics, VXLAN overlays, ECMP, SDN, load-balancer tiers, storage networks, VPCs, service meshes). These are the architectures behind Google/Cloudflare/Akamai/AWS — and the knowledge that turns generic system-design answers into senior-level ones. Sections are ordered: why global traffic routing works the way it does (01), the three fundamental forwarding models (02), and the physical/logical design inside the building and cloud (03).

## Sections (in study order)

1. **Section 01 — Global Load Balancing, DNS Anycast, and EDNS**
   The production way to route users to the nearest/healthiest replica: DNS-based GSLB (GeoIP, latency, weighted, health-based steering), anycast for the critical nameservers, EDNS Client Subnet for accuracy, and the load-balancer hierarchy (GSLB → edge LB → service LB). Includes the math of "nearest" (round-trip proxies), TTL trade-offs, and the difference between DNS steering and anycast steering.
2. **Section 02 — Anycast, Multicast, and Broadcast**
   The three models beyond unicast. Anycast: same IP announced from many places, route picks nearest (DNS root/`a.root-servers.net`, 1.1.1.1/8.8.8.8, DDoS scrubbing). Multicast: one-to-many group delivery with IGMP/PIM (IPTV, PTP, video distribution). Broadcast: local link, L2 only (ARP, DHCP) — and why L3 broadcast is confined to the subnet. Covers the costs and pitfalls of each.
3. **Section 03 — Datacenter and Cloud Networking**
   Inside the building: CLOS/spine-leaf fabric with ECMP (equal-cost multipath), the leaf-to-spine math for oversubscription, VXLAN overlays for scale/L2 mobility, SDN control planes (BGP/EVPN), four-post load balancers (L4/L7), storage (NVMe-oF/RoCE, lossless Ethernet with PFC), and the cloud abstraction: VPCs, subnets, IGW/NAT, security groups, transit/mesh, and serverless networking.

## Prerequisites
Parts 01-04 (IP/BGP, TCP, DNS, HTTP). For Section 03, Part 05's switching/VLAN/STP grounding is assumed. Security concepts (Part 07) reappear in the DDoS-scrubbing and VPC-security material.

## Key takeaways after this chapter
- Global traffic = DNS GSLB (steering) + anycast (nearest replica / DDoS absorb) + health checks — three levers, each with latency/consistency trade-offs.
- Anycast = "route picks the closest of many same-IP nodes" — perfect for stateless resolvers/CDN, wrong for stateful servers.
- Multicast = efficient one-to-many (the only way to stream to millions without N copies); broadcast = local-link only, never routed.
- DCs are CLOS fabrics (spine-leaf) + ECMP + VXLAN overlays; the cloud wraps the same in VPC/subnet/security-group abstractions.
- LB tiers: L4 (per-flow, high throughput) → L7 (content-aware) → GSLB (global steering) — each tier offloads the next.
