# Datacenter and Cloud Networking

> **TL;DR**: Modern DCs and clouds are built on CLOS/spine-leaf fabrics with ECMP spreading traffic, VXLAN overlays for L2 mobility and scale, SDN control planes (BGP/EVPN), L4/L7 load-balancer tiers, lossless Ethernet for storage (NVMe-oF/RoCE with PFC), and the cloud abstraction of VPCs/subnets/security groups over that same fabric.

## 1. Why Does This Exist?
The old three-tier DC design (core → distribution → access, spanning-tree blocked links) couldn't scale: STP blocked redundant paths (wasted bandwidth), oversubscription was baked into every tier, east-west (server-to-server) traffic exploded with distributed apps, and adding capacity meant restructuring. **Datacenter networking** exists to build a fabric that is: (1) **scalable** — add capacity by adding identical switches (CLOS); (2) **high-bandwidth** — all links used via ECMP instead of STP blocking; (3) **agile** — VMs/containers move anywhere, so the network must allow L2 mobility (VXLAN) and be software-driven (SDN); and (4) **efficient for the actual workload** — distributed systems, storage (NVMe-oF), and cloud tenancy. The cloud then *wraps* that fabric in abstractions (VPC, subnet, security group) so tenants get a "private network" without seeing the physical reality. This is the substrate every "design a large-scale system" answer assumes.

## 2. How Does It Work?
**The physical fabric (CLOS / spine-leaf):**
- Every **leaf** (ToR, top-of-rack) connects to **every spine** (no leaf-to-leaf links); every leaf has equal paths to every other leaf through any spine.
- Traffic uses **ECMP** (equal-cost multi-path): hashing flow 5-tuples across the parallel links → all links carry traffic (no STP blocking).
- **Scale math**: N spines × M leaves = M racks with N× uplink bandwidth each; add spines for capacity, leaves for more racks.
**The overlay (VXLAN):**
- To allow VMs/containers to move anywhere and to make L2 domains huge without STP limits, **VXLAN** (RFC 7348) encapsulates L2 frames in UDP/IP (outer: VTEP-to-VTEP) with a 24-bit VNI = 16M tenants/segments. The physical underlay routes; the overlay provides L2/L3 isolation.
- **EVPN (RFC 7432)** runs BGP over the underlay to distribute MAC/VTEP reachability (control plane), replacing flooding.
**The cloud abstraction:**
- Tenants get **VPCs** (isolated virtual networks), **subnets**, **IGW/NAT**, **security groups** (stateful L4 filters on instances), **route tables**, and **LB/mesh** services — all implemented over the shared fabric with VXLAN + SDN controllers.

## 3. When Is It Used?
- **Every hyperscaler DC** (AWS/GCP/Azure/Meta/Google) — spine-leaf + VXLAN/EVPN + SDN.
- **Enterprise DC modernization** — replacing three-tier with spine-leaf, private clouds.
- **Container/K8s networking** — Calico/Cilium/Flannel use VXLAN or BGP overlays over the underlay; service meshes (Istio) layer mTLS/policies.
- **Cloud tenancy** — VPC/subnet/security-group model; cloud LBs (ALB/NLB), NAT gateways, transit gateways.
- **Storage networks** — NVMe-oF (NVMe over Fabrics) over RoCE/RDMA; lossless Ethernet (PFC/ETS) in DCs.
- **HPC/AI clusters** — InfiniBand-style fat-trees or Ethernet spine-leaf with RDMA.

## 4. Why Wasn't Another Approach Chosen?
- *Three-tier + STP:* STP blocks redundant paths → ~50% bandwidth idle, no load sharing, slow convergence, and scaling meant hierarchical redesign. CLOS + ECMP uses *all* links and scales by adding identical switches — the density/diagram is a fat-tree.
- *Pure L2 datacenter (big flat VLAN):* broadcast domains that huge collapse (ARP storms, MAC table limits), STP loops, and no isolation. VXLAN keeps a *flat L2 overlay* (for VM mobility and legacy apps) while the *underlay routes* — best of both.
- *Static VLANs for tenancy:* 4094 VLANs max, port-level provisioning; VXLAN gives 16M VNIs with software-driven provisioning — the difference between a cloud and a giant switch.
- *No ECMP (per-flow static routing):* ECMP hashes flows across parallel paths — perfect utilization and simple; alternatives (per-packet) break TCP ordering, so flow hashing is the choice. (For large "elephant" flows, L4/L7 LB or dynamic rehashing is layered on.)
- *Switch-by-switch config:* impossible at scale — SDN/EVPN/BGP centralizes the control plane and automates the data path.

## 5. Intuition
The DC fabric is a **highway grid with no stop signs**. CLOS is "every neighborhood (rack) connects directly to every highway (spine)"; ECMP is the traffic-light-free intersection that splits cars (flows) evenly across all lanes so no lane idles. VXLAN is the **packaging truck**: your server's Ethernet frame gets sealed in an addressed box (UDP) so it can travel across the whole city (the routed underlay) and be delivered to another server as if it were next door — even though they're on different streets. EVPN is the city's directory: instead of every truck yelling "who has this MAC?" across town (flooding), a central registry (BGP) tells each depot which trucks hold which goods. The cloud (VPC) is the gated communities: from the street (physical fabric) you only see walls; inside each community (VPC), private streets (subnets) and guards (security groups) control who can enter — while the whole grid hums underneath.

## 6. Real-World Analogy
A **massive office building with an elevator bank**. The building is the DC. Floors (racks) each have a reception desk (leaf switch). Every desk has a dedicated elevator shaft straight to the roof lobby (spine) — and the lobby connects to *every* floor's desk (full mesh leaf-spine). When two floors need to move documents (traffic), the elevator dispatcher (ECMP) sends each shipment (flow) to whichever shaft is least busy, splitting the load so all shafts stay busy. There are no blocked corridors (no STP). To move a department (a VM) from the 3rd to the 20th floor without changing its mailing address (IP/MAC — overlay), you put the department's mail in a courier box (VXLAN) addressed to the new floor; the courier system (underlay routing) delivers it, and everyone keeps writing to the same address. The cloud is the building's rental units (VPCs): each company rents floors with their own intercom (security groups) and keys (IAM), never seeing the shared elevator shafts they ride on.

## 7. Formal Definition
- **CLOS / spine-leaf**: a k-ary (3-stage) folded fat-tree; leaves connect only to spines, spines only to leaves; all paths equal-cost → **ECMP** spreads flows. Oversubscription = (leaf uplink total) / (leaf server-facing total), tuned per tier (e.g., 3:1 server-facing, 1:1 or higher spine).
- **ECMP**: hashing packets of a flow (5-tuple: src/dst IP+port, proto) to one of K equal paths; K ≥ 16-64 paths per pair in modern fabrics; **LAG** (LACP) for link bundling.
- **VXLAN** (RFC 7348): L2-over-UDP encapsulation; outer header = VTEP IPs + UDP 4789 + VNI (24-bit). **VTEP** = VXLAN tunnel endpoint (leaf/ToR or host). **EVPN** (RFC 7432): BGP control plane distributing MACs + VNI + VTEP reachability, with multihoming (ES). **Overlay vs underlay**: underlay = physical routed fabric (IP/BGP); overlay = tenant L2/L3 above it.
- **SDN**: separating control plane (centralized: SDN controller, BGP route reflectors, cloud control planes) from data plane (switches/forwarding ASICs).
- **LB tiers**: L4 (NLB: 4-tuple hashing, per-flow, high throughput) → L7 (ALB/NGINX/envoy: content-aware, HTTP/2, TLS, health) → service mesh (sidecar L7).
- **Storage**: **NVMe-oF** (NVMe over Fabrics) over **RoCE** (RDMA over Converged Ethernet, lossless: **PFC** priority flow control + ETS, or lossy with priority) — microsecond latency, μs-grade copy.
- **Cloud abstractions**: VPC (isolated virtual network), subnet (routed segment), IGW/NAT GW, security group (stateful instance firewall), NACL (stateless subnet filter), route tables, Transit Gateway (hub peering), service mesh for east-west.

## 8. Example
**AWS-style request path through the DC/cloud fabric:**
```
Client → IGW (Internet Gateway) → VPC → ALB (L7, TLS terminate, HTTP/2)
      → target group → EC2 in subnet A (security group allows 443 from ALB)
Physical reality: client packets enter the DC via edge LB → spine fabric →
leaf A (VTEP) → VXLAN-encapsulated toward leaf B (host subnet) → host agent
→ container/VM → service (envoy sidecar mTLS to the next hop).
```
**ECMP spread (3-leaf × 3-spine):**
```
Leaf1 ↔ Spine1, Spine2, Spine3  (3 equal paths to Leaf2)
Flow (A→B): hash(src,dst,ports,proto) → choose path 2 (Spine2)
Flow (C→D): hash(...) → choose path 1   → all three spines carry ~equal load
```

## 9. Internal Working
1. **Underlay**: each leaf advertises its loopback + server prefixes via BGP (or OSPF) to spines; spines are route reflectors; every leaf has equal-cost paths to every other leaf → ECMP hashes per flow.
2. **Overlay (VXLAN)**: when a frame must cross leaves, the ingress VTEP encapsulates (outer dst = egress VTEP IP via the underlay); the egress VTEP decapsulates and delivers on the local L2. The VNI isolates tenants.
3. **EVPN control plane**: MAC/ARP/route info is advertised via BGP (MP-BGP EVPN families); switches learn remote MACs without flooding (BUM traffic is controlled/limited); multihomed servers get redundancy via ESI/DF election.
4. **Cloud SDN**: a central controller programs VTEPs, route tables, security groups, and LBs via APIs (not CLI on each box); tenant config is translated into overlay state.
5. **L4/L7 LB**: NLB hashes 4-tuples to a target per flow (sticky by hash); ALB terminates TLS, parses HTTP, applies rules, and rebalances per request (with connection reuse). Health checks drive target membership.
6. **Storage path**: NVMe-oF requires lossless conditions — RoCE uses PFC to guarantee no-drop for the priority class and ETS to allocate bandwidth; congestion notified via ECN/QCN.
7. **Failure handling**: spine failure → ECMP rehash (fewer paths, seconds); leaf failure → EVPN multihoming reroutes; fabric-wide reconvergence via BFD/fast-reroute.

## 10. Time Complexity / Performance
- **ECMP**: O(1) hash per packet; spread is statistical — big flows ("elephants") can imbalance a single hash; mitigations: hashing on more fields, per-flow consistent hashing, LB-tier traffic shaping.
- **Path count**: K paths for K spines; K=16-64 typical; more paths = better utilization but more BGP state (route reflectors scale it).
- **Latency**: leaf-spine adds 1 switch hop per direction (~0.5-2 µs/switch on modern ASICs); total DC RTT ~1-10 µs rack-to-rack (vs 50-100 ms across the internet). Underlay = routed IP, no STP blocking.
- **Overlay overhead**: +50 bytes (VXLAN/UDP/IP) per frame; MTU must be raised (jumbo ~9000) on the underlay; hardware VXLAN (ASIC) keeps throughput at line rate.
- **Storage**: NVMe-oF over RoCE ≈ 1-3 µs fabric latency vs FC; lossless mode needs buffer/reservation headroom; bad flows can trigger PFC storms (head-of-line blocking) — operators tune carefully.
- **LB scale**: L4 NLB handles millions of flows (stateless hash + HW); L7 is CPU/connection-bound (100k-1M req/s per instance cluster with HTTP/2 + pooling).

## 11. Advantages
- **Scale & capacity**: add spines/leaves without redesign; ECMP uses all links (no STP waste).
- **Mobility & tenancy**: VXLAN gives L2 mobility + 16M segments; VMs/containers move without re-addressing.
- **Automation & agility**: SDN/EVPN/API-driven — provisioning in minutes, not weeks; cloud tenants self-serve.
- **Fault isolation**: spine/leaf symmetric design = predictable failure handling (rehash, multihoming); failures are contained per segment.
- **High bandwidth**: equal-cost multipath + jumbo frames + hardware overlays → multi-Tbps fabric.
- **Cloud value**: VPC/security-group abstractions deliver isolation and policy without physical segmentation.

## 12. Disadvantages
- **Complexity**: underlay + overlay + SDN + EVPN + LB tiers is a huge operational surface (many moving control planes).
- **Oversubscription**: fabric is provisioned with a ratio (e.g., 3:1) — a noisy neighbor can saturate leaf uplinks (needs QoS/rate limits).
- **ECMP imbalance**: hash collisions on big flows → uneven links; consistent hashing/LB needed.
- **Overlay bugs & overhead**: VXLAN MTU issues, VTEP misconfig, PFC storms, broadcast/frame replication limits; harder to troubleshoot than flat L2 (tcpdump needs decap).
- **Lossless Ethernet fragility**: PFC head-of-line blocking can amplify congestion; lossless ≠ no congestion.
- **Vendor/tooling lock-in** and the cost of high-port-count switches/ASICs.
- **Cloud abstraction leaks**: security groups misconfig, route-table mistakes, and "which VPC/region?" decisions still bite operators.

## 13. Interview Questions
1. **Q: What is a CLOS / spine-leaf fabric and why is it used?** A: Every leaf (ToR) connects to every spine; no leaf-leaf links; all paths equal → ECMP spreads traffic. It scales by adding identical switches, uses all links (no STP blocking), and gives predictable bisectional bandwidth — the standard for modern DCs and clouds.

2. **Q: What is ECMP and how does it work?** A: Equal-Cost Multi-Path: the router/switches hash each flow (5-tuple) and map it to one of K equal-cost paths, so parallel links share load. Per-flow hashing preserves TCP ordering (unlike per-packet). Limitations: big flows can collide on a link; mitigated with more paths and hashing quality.

3. **Q: What problem does VXLAN solve and how?** A: L2 domains limited by VLANs (4094) and STP; VM mobility needs big/flat L2 with isolated tenants. VXLAN wraps L2 frames in UDP (VNI 24-bit = 16M segments) between VTEPs over a routed underlay — L2 mobility + massive tenancy + no STP limits, with the underlay doing routing/ECMP.

4. **Q: What is an overlay vs an underlay?** A: Underlay = physical routed fabric (spines/leaves, IP/BGP, ECMP). Overlay = the virtual network above it (VXLAN segments, tenant L2/L3, security groups). The overlay decouples tenant networking from physical topology — move a VM anywhere, the address stays.

5. **Q: What is EVPN?** A: EVPN (RFC 7432) uses BGP to distribute MAC/route/VTEP reachability over the underlay — a control plane for the overlay. It replaces data-plane flooding ("who has this MAC?") with protocol-advertised state, enabling multihoming, fast convergence, and automation.

6. **Q: What is the difference between L4 and L7 load balancing?** A: L4 (NLB-style): hashes the 4-tuple, per-flow, stateless, very high throughput, no content awareness. L7 (ALB/NGINX/envoy): terminates TLS, parses HTTP, routes by path/host, health-aware, per-request rebalancing (with connection pooling), but is CPU/connection-bound. Tier: L4 in front to handle scale, L7 behind for smarts.

7. **Q: TRICKY — What is oversubscription in a DC fabric?** A: The ratio of server-facing bandwidth (leaves' downlinks) to uplink bandwidth (leaves→spines). 3:1 = for every 3 Gbps of server capacity, 1 Gbps of fabric uplink — acceptable because average utilization is low. Busty apps hit the ratio (noisy neighbor); low oversubscription = expensive. Design: keep spine-tier oversubscription low (1:1), leaf-tier moderate.

8. **Q: What is RoCE / NVMe-oF and why does it need lossless Ethernet?** A: NVMe over Fabrics runs storage over the network with RDMA (RoCE = RDMA over Converged Ethernet), giving µs latency vs ms for TCP. RDMA assumes lossless delivery (no retransmits), so RoCE uses PFC (priority flow control) to prevent drops on the priority class — with the cost of head-of-line blocking if misconfigured.

9. **Q: PRODUCTION — A rack's traffic spikes and other tenants suffer. Why and how do you fix it?** A: Likely leaf oversubscription + noisy neighbor: a flow (or workload) saturates the leaf's uplinks. Fixes: (1) raise QoS/rate limiting per tenant/flow; (2) move the heavy flow off the oversubscribed leaf (rebalance or pin to a less-loaded leaf); (3) add spine uplinks/upgrade oversubscription ratio; (4) use ECMP/LB-tier rehashing for large flows; (5) telemetry to catch "elephant flows" before they bite.

10. **Q: How does a cloud VPC differ from a physical VLAN?** A: A VPC is an *overlay* tenant network (VXLAN VNI + SDN control plane): 16M segments vs 4094 VLANs, software-provisioned in minutes, with security groups (stateful, per-instance) and route tables — all decoupled from physical switches. A VLAN is a physical L2 partition on one/adjacent switches. The VPC is the cloud abstraction; the VLAN is the switch primitive.

11. **Q: What is a security group vs a NACL?** A: Security group = stateful, instance-level (allow rules; return traffic auto-allowed; evaluated per instance in the SG). NACL = stateless, subnet-level, allow+deny rules (explicit return rules needed). Order: SG is the primary per-workload control; NACL is a subnet-wide backstop. Common interview trap: SG is stateful, NACL is not.

12. **Q: TRICKY — Why do we still need L2 at all in the overlay?** A: Legacy apps, VM migration, and some hardware require L2 semantics (ARP, DHCP, multicast, broadcast) even in the cloud. VXLAN preserves that L2 view while the underlay routes — you get L2 *behavior* without L2 *limitations* (scaling, STP, mobility). "Route where you can, switch where you must" is the DC design mantra.

13. **Q: How does a container network (K8s) map onto the fabric?** A: K8s uses CNI: pod IPs are routed/overlaid over the underlay. Options: (1) a flat routable pod CIDR with BGP (Calico) — pods get real routes, ECMP handles it; (2) an overlay (Flannel VXLAN, Calico VXLAN) — pod traffic encapsulated to node VTEPs; (3) service mesh (Istio) layers mTLS + L7 policy as a sidecar. The DC fabric just routes/encapsulates — the CNI does pod-level networking above it.

14. **Q: What is a "fat-tree" and how is it related to CLOS?** A: A fat-tree is the bisectional-bandwidth-balanced version of a CLOS: as you go up the tiers, link capacities stay equal to guarantee full bisectional bandwidth (any pair of leaves can exchange at full rate). CLOS/spine-leaf is the practical folded realization (spines at the top, leaves below) with equal-capacity spine links — this is exactly how big AI/HPC and hyperscaler fabrics are dimensioned.

15. **Q: SCENARIO — Latency between two same-rack VMs is 20 µs, but a new app shows 200 µs and intermittent drops. Debug.** A: (1) Is it intra-leaf or did the flow cross the fabric? Check leaf↔leaf path (ECMP rehash under load); (2) check for VXLAN MTU mismatch (frames dropped/ICMP need-frag); (3) check PFC storms (lossless class head-of-line blocking — look for pause frames); (4) check the host/CNI path (veth, iptables, sidecar proxy adds latency); (5) check the LB tier — if traffic hairpins through an L7 proxy, that's the real 200 µs. Trace: `tcpdump` at both VTEPs + host.

16. **Q: What is the role of a route reflector in the fabric?** A: In a full mesh of leaves, BGP sessions = N²; route reflectors (spines) centralize peering: each leaf peers with the RRs (or spines act as RRs), and the RR redistributes routes — scaling the control plane to hundreds/thousands of leaves while keeping ECMP paths.

17. **Q: PRODUCTION — Design a multi-AZ cloud network for a global SaaS.** A: (1) VPC per region, subnets per AZ, IGW/NAT for egress, security groups per tier (Web→App→DB with least privilege); (2) ALB in front (L7, TLS, health), NLB or mesh for east-west; (3) Transit Gateway or peering across regions, or an overlay (mesh) for multi-region; (4) DB across AZs with synchronous replication + failover; (5) service mesh (mTLS) for microservices; (6) DDoS/WAF at the edge (Section 01). Emphasize: isolate per tier, least-privilege SG, multi-AZ redundancy, encryption in transit.

## 14. Follow-Up Questions
1. **Q: What is a "microburst" and why does it matter?** A: Bursts of packets arriving faster than a port drains for a few µs-ms — queueing causes drops even at low average utilization. In lossy fabrics, TCP recovers but latency spikes; in lossless (RoCE), PFC activates → head-of-line blocking. Mitigations: larger buffers, ECN, pacing, telemetry.

2. **Q: What is "consistent hashing" in the LB/fabric context?** A: A hash that maps keys to nodes while minimizing remapping when the node set changes (e.g., a target leaves the pool). Used by LB tiers (sticky flows survive membership change) and by distributed caches; contrasts with plain modulo hashing which rebalances everything on membership change.

3. **Q: What is the difference between "east-west" and "north-south" traffic?** A: North-south = in/out of the DC (internet ↔ DC, via edge LBs). East-west = server-to-server inside the DC (microservices, storage, replication) — the majority of DC traffic today, which is why spine-leaf/ECMP and overlay routing are optimized for it.

4. **Q: What is a "spine-level failure" and what breaks?** A: A spine failing removes K-1 paths for each leaf → ECMP rehashes to the surviving spines (capacity drop but no outage if design allows); BGP/EVPN reconverges. If the fabric is oversubscribed at 1:1, one spine failure can drop bisectional capacity — which is why N+1 spine counts and BFD fast detection are standard.

## 15. Coding Example
```python
# ECMP hashing (consistent per-flow) + spine-leaf path selection
import hashlib

def ecmp_path(flow_5tuple, num_paths):
    key = "|".join(map(str, flow_5tuple)).encode()
    h = int(hashlib.md5(key).hexdigest(), 16)
    return h % num_paths  # stable per flow (same hash → same path, TCP-safe)

flows = [("10.0.0.1", "10.0.0.2", 443, 50000, 6), ("10.0.0.1", "10.0.0.3", 443, 50001, 6)]
for f in flows:
    print(f"flow {f[3]} -> spine path {ecmp_path(f, 4)}")
```
```bash
# Real fabric/cloud verification commands
# Underlay (spine-leaf) BGP + ECMP state on a leaf:
ip route show | grep -c "nexthop"            # multiple nexthops = ECMP paths
show bgp ipv4 unicast summary 2>/dev/null | head      # (Cisco/JunOS equivalent)
# VXLAN VTEP + VNI state:
bridge fdb show | grep -E "vxlan|tun" | head      # MAC → VTEP mapping (EVPN learned)
ip -d link show | grep -A4 vxlan
# Cloud view (AWS):
aws ec2 describe-instances --query 'Reservations[].Instances[].{id:InstanceId, vpc:VpcId, sg:SecurityGroups[0].GroupId}' --output table
aws ec2 describe-security-groups --query 'SecurityGroups[].{name:GroupName, ingress:IpPermissions}' --output json | head -40
# Host / storage path checks:
ethtool -K eth0 tx-checksum-ip-generic on && ethtool -S eth0 | grep -iE "pause|rx_fifo"  # PFC / drops
```
```bash
# Spin up a VXLAN pair in a lab (quick overlay sanity check)
# On host A:
ip link add vx0 type vxlan id 100 dstport 4789 remote 192.168.1.20 dev eth0
ip addr add 10.10.0.1/24 dev vx0; ip link set vx0 up
# On host B: same with 10.10.0.2/24 and remote 192.168.1.10 → ping 10.10.0.1 works
ping -c 2 10.10.0.1
```

## 16. Industry Usage
- **Hyperscalers**: Google (Jupiter fabric — spine-leaf + SDN + B4 WAN), Meta (fabric + AI clusters), AWS (spine-leaf + VXLAN/EVPN, Nitro offload), Microsoft Azure (SONiC-based fabric).
- **Networking vendors**: Arista, Cisco (ACI/Nexus), Juniper, and open source **SONiC** (Microsoft's DC OS) — the de-facto hyperscaler switch OS.
- **Cloud networking**: AWS VPC/Transit Gateway, GCP VPC/Private Service Connect, Azure vNet — all overlay the shared fabric.
- **K8s/containers**: Calico, Cilium (eBPF), Flannel; service meshes (Istio/Linkerd) for east-west mTLS.
- **Storage**: NVMe-oF over RoCE in AWS (EBS), enterprise storage; InfiniBand in HPC/AI (but Ethernet spine-leaf + RoCE is displacing it).
- **AI/ML clusters**: massive spine-leaf fat-trees for GPU training (e.g., Meta's 32k-GPU clusters), where bisectional bandwidth is everything.

## 17. References
- RFC 7348 (VXLAN) — https://datatracker.ietf.org/doc/html/rfc7348
- RFC 7432 (EVPN) — https://datatracker.ietf.org/doc/html/rfc7432
- RFC 2992 (ECMP analysis) — https://datatracker.ietf.org/doc/html/rfc2992
- Google Jupiter fabric papers; Meta fabric talks (engineering blogs).
- Microsoft SONiC — https://sonic-net.github.io/SONiC/
- Kurose & Ross, *Computer Networking*, 8th ed., §6.7 (data center networking), plus cloud networking chapters.
- AWS VPC docs / security group vs NACL — https://docs.aws.amazon.com/vpc/latest/userguide/security.html

## 18. Cheat Sheet
- CLOS/spine-leaf: leaves ↔ all spines, no leaf-leaf; ECMP spreads flows; scale = add spines/leaves.
- ECMP: 5-tuple hash → one of K paths (per-flow, TCP-safe); imbalance from "elephant" flows.
- VXLAN: L2-in-UDP (VNI 24-bit = 16M segments), VTEP endpoints, underlay routes, overlay isolates.
- EVPN: BGP control plane for MAC/VNI/VTEP (no flooding), multihoming.
- Overlay vs underlay: overlay = tenant L2/L3 (mobility, tenancy); underlay = physical routed fabric.
- LB: L4 (4-tuple, stateless, scale) → L7 (TLS/HTTP, health) → mesh (east-west mTLS).
- Oversubscription: leaf uplink vs downlink ratio; noisy neighbor risk; keep spine low (1:1).
- Storage: NVMe-oF/RoCE = RDMA over lossless Ethernet (PFC/ETS); µs latency; PFC storm risk.
- Cloud: VPC (overlay tenant), subnet, IGW/NAT, SG (stateful, instance) vs NACL (stateless, subnet).
- Fat-tree = CLOS with full bisectional bandwidth — AI/HPC fabric standard.
- Route reflectors scale BGP from N² to N; BFD for fast convergence.

## 19. Quiz
1. In a CLOS fabric, a leaf connects to: a) other leaves b) all spines c) one spine d) nothing → **b**
2. ECMP spreads traffic by: a) per-packet b) per-flow hash c) round-robin d) DNS → **b**
3. VXLAN VNI is how many bits? a) 12 b) 16 c) 24 d) 32 → **c**
4. Which protocol is the VXLAN control plane? a) OSPF b) EVPN c) IGMP d) STP → **b**
5. Security groups are: a) stateless b) stateful c) subnet-level d) DNS → **b**
6. NACLs are: a) instance-level b) subnet-level and stateless c) stateful d) overlay → **b**
7. RoCE needs: a) lossy Ethernet b) lossless Ethernet (PFC) c) TCP d) UDP only → **b**
8. The fat-tree's goal: a) cheap switches b) full bisectional bandwidth c) fewer ports d) L2 only → **b**

**Answers**: 1-b, 2-b, 3-c, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: CLOS fabric shape** → **A:** Every leaf ↔ every spine; no leaf-leaf; all equal-cost paths via ECMP.
- **Q: What is ECMP?** → **A:** 5-tuple hash spreads flows over equal-cost paths — all links used, TCP-safe.
- **Q: What does VXLAN encapsulate?** → **A:** L2 frames in UDP between VTEPs with a 24-bit VNI (16M tenants).
- **Q: Overlay vs underlay** → **A:** Underlay = routed physical fabric; overlay = tenant L2/L3 above it.
- **Q: EVPN's job** → **A:** BGP-distributed MAC/VNI/VTEP state instead of data-plane flooding.
- **Q: L4 vs L7 LB** → **A:** L4 = 4-tuple hash, stateless, huge scale; L7 = TLS/HTTP/health, per-request, CPU-bound.
- **Q: Why does RoCE need PFC?** → **A:** RDMA has no retransmit — lossless delivery required for µs storage.
- **Q: SG vs NACL** → **A:** SG = stateful, instance; NACL = stateless, subnet.

## 21. Revision
Modern DC/cloud = CLOS/spine-leaf fabric (leaves↔all spines, ECMP per-flow hashing, all links used), VXLAN overlays (L2-in-UDP, 16M VNIs, VTEPs) with EVPN BGP control plane (no flooding, multihoming), SDN automation, L4→L7→mesh LB tiers, and NVMe-oF/RoCE storage (lossless PFC). The cloud wraps this in VPC/subnet/security-group (stateful) vs NACL (stateless) abstractions over the shared fabric. Oversubscription and elephant-flow imbalance are the recurring design risks; fat-trees (full bisectional bandwidth) power AI/HPC. Anchors: *spine-leaf + ECMP = scale with all links used; VXLAN = L2 mobility + tenancy over a routed underlay; EVPN = BGP as the overlay control plane; SG stateful/instance vs NACL stateless/subnet; RoCE needs lossless Ethernet; cloud VPC = the same fabric behind tenant abstractions.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a CLOS/spine-leaf fabric?" | 13-Q1 |
| "What is ECMP?" | 13-Q2 |
| "What problem does VXLAN solve?" | 13-Q3 |
| "Overlay vs underlay" | 13-Q4 |
| "What is EVPN?" | 13-Q5 |
| "L4 vs L7 load balancing" | 13-Q6 |
| "What is oversubscription?" | 13-Q7 |
| "RoCE / NVMe-oF / PFC" | 13-Q8 |
| "Noisy neighbor / leaf saturation" | 13-Q9 |
| "VPC vs VLAN" | 13-Q10 |
| "Security group vs NACL" | 13-Q11 |
| "Why L2 still in the overlay?" | 13-Q12 |
| "K8s networking over the fabric" | 13-Q13 |
| "Fat-tree and bisectional bandwidth" | 13-Q14 |
| "Design multi-AZ cloud network" | 13-Q17 |
