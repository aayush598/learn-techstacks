# Repeaters, Hubs, Switches, Routers, Gateways

> **TL;DR**: These five devices form an intelligence ladder — repeater (L1, regenerates signals), hub (L1, broadcasts bits), switch (L2, forwards frames by MAC), router (L3, forwards packets by IP), gateway (any layer, translates between protocols) — and the differences exist because each level of forwarding decision solves a different scaling problem.

## 1. Why Does This Exist?
Cables and signals can only travel so far and connect so many devices. Each device exists to solve a specific problem:
- **Repeater**: solves *signal attenuation* — a signal weakens with distance, so a repeater regenerates it to extend a segment.
- **Hub**: solves *fan-out* — a single connection must reach multiple devices; a hub electrically connects all ports to one shared medium.
- **Switch**: solves *efficiency and isolation* — a hub wastes bandwidth (every frame to everyone) and creates collisions; a switch forwards each frame *only* to the correct port based on MAC addresses.
- **Router**: solves *connecting separate networks* — switches can't scale to the Internet or join different IP subnets; a router forwards packets between networks by IP address.
- **Gateway**: solves *protocol incompatibility* — two networks with different stacks (e.g., old X.25 vs IP, or a proxy translating protocols) need a translator.
The ladder exists because **no single device solves all problems** — the right device is chosen by the layer of the problem.

## 2. How Does It Work?
| Device | Layer | Input | Decision | Output | Memory |
|---|---|---|---|---|---|
| Repeater | L1 | Bits | None (regenerate) | All ports | None |
| Hub | L1 | Bits | None (broadcast) | All ports | None |
| Bridge/Switch | L2 | Frames | Lookup dest MAC in MAC table | The matching port (or flood) | MAC table |
| Router | L3 | Packets | Longest-prefix match on dest IP | Next-hop interface | Routing/FIB table |
| Gateway | L2-L7 | Protocol units | Translate/protocol-convert | Depends on translation | Connection/state table |

- Repeaters/hubs operate on **voltage/light pulses**: no addressing, no parsing of headers.
- Switches parse the **Ethernet header** (dest MAC) and use a self-learning table: they watch source MACs on ingress ports, store them, and forward unknown destinations to all ports (flooding), then refine as they learn.
- Routers parse the **IP header**, match the destination against the routing table (routes = subnet + next hop), and rewrite the link header for the next hop.
- Gateways are protocol translators — a "protocol converter" between different stacks (e.g., a SIP→H.323 gateway, an email gateway, or the home-router's "default gateway" role meaning "exit to the Internet").

## 3. When Is It Used?
- **Repeater**: extending Ethernet segments (legacy 10BASE5/2), regenerating fiber/digital signals over long distances (optical repeaters, amplifiers), Wi-Fi extenders/APs in mesh.
- **Hub**: legacy LANs, lab/teaching environments, and — historically — anywhere a shared collision domain was acceptable. Rare today (switches are cheap).
- **Switch**: *every* modern LAN — office, home, datacenter. Also "L3 switch" for routing within a building; stacking for scale.
- **Router**: Internet edge (home router, ISP CPE), WAN interconnects, datacenter core (though "core switches" now route in hardware), MPLS/VPN endpoints, cloud VPC route tables.
- **Gateway**: network-to-network translation (VoIP gateways, IoT protocol gateways, protocol conversion in enterprise), and the everyday "default gateway" = the router that is your exit point.

## 4. Why Wasn't Another Approach Chosen?
The key design choices and why alternatives were rejected:
- **Why regenerate (repeater) instead of making longer cables?** Cable length limits are physical (attenuation, crosstalk, timing). You can't electrically push a signal 10 km; you regenerate it. Repeaters were the cheapest fix.
- **Why a hub instead of many cables?** To fan out one uplink to many devices without a smart device — cheap but dumb (all ports in one collision domain).
- **Why a switch instead of a hub?** Hub efficiency is O(1/N) per host on a shared medium with collisions. A switch gives each port a dedicated, full-duplex link — total bandwidth scales with ports, no collisions. When silicon got cheap, switches replaced hubs everywhere.
- **Why a router instead of a giant switch?** Switches forward by MAC (flat, non-hierarchical) — they can't scale to millions of networks and can't do path selection across heterogeneous networks. Routers use hierarchical IP addresses + routing protocols (OSPF/BGP) to scale globally. You can't route the Internet with switches alone.
- **Why a gateway instead of "just use a router"?** A router speaks the same protocol (IP) on both sides; when the two sides have *different* protocol stacks, nothing common exists to route — you need translation. Gateway = translator; router = forwarder.

## 5. Intuition
Think of a **delivery network with escalating intelligence**:
- Repeater = a loudspeaker that shouts your message again, louder, so it travels farther. It doesn't know who it's for.
- Hub = the loudspeaker connected to *everyone's* phones — every message goes to every person. No privacy, no efficiency.
- Switch = a **post office at each building** that reads the *name on the envelope* (MAC) and only delivers to that apartment. It learns which apartment is in which corridor.
- Router = the **intercity routing center** that reads the *city on the package* (IP) and chooses which highway (interface) to send it on.
- Gateway = the **translator/interpreter** who translates your request between two countries' postal systems that use different formats.

## 6. Real-World Analogy
**The office building mail system**: If the CEO wants to send a memo to everyone, a hub = photocopy and put in *everyone's* inbox (wasteful but simple). A switch = the inter-office mail clerk who has a directory ("Alice is on floor 2") and hand-delivers only to the right desk, learning the directory as they work. The router = the courier service at the front desk deciding which external courier (ISP link) carries the letter out of the building to *another* building's mail system. The gateway = the bilingual receptionist who translates your letter because the other building uses a different language/format. Each device is the "smartest person needed for that job" — nothing more.

## 7. Formal Definition
- **Repeater**: a physical-layer (L1) device that receives a signal, regenerates it (restoring amplitude/timing), and retransmits it on all ports, extending the distance a segment can span. It operates on bits and has no addressing logic.
- **Hub** (multi-port repeater): an L1 device that connects several stations on one shared medium; all ports belong to a *single collision domain* and a *single broadcast domain*.
- **Switch** (multi-port bridge): an L2 device that forwards frames based on the destination MAC address using a self-learning forwarding table (source MACs learned per ingress port), giving each port an independent collision domain.
- **Router**: an L3 device that forwards packets between networks based on the destination IP address using a routing table computed by static config or routing protocols (OSPF, BGP); it terminates broadcast domains.
- **Gateway**: a device that translates between two *different* protocol stacks (at any layer), performing protocol conversion rather than simple forwarding. The term is also used for a network's entry/exit point ("default gateway").

## 8. Example
A 20-host office LAN going from worst to best device:
1. **Hub (all 20 on one hub)**: one collision domain. Effective bandwidth = 10 Mbps shared. Two hosts transmitting at once → collision → both back off. Adding the 21st host makes everyone slower. Broadcasts (ARP) reach all 20.
2. **Switch (20 ports)**: 20 separate collision domains (each port full-duplex). Full 10/100/1000 Mbps per host. Switch learns MACs after first traffic; an ARP broadcast still floods to all 20 (one broadcast domain).
3. **Router (separating office into 2 subnets + Internet)**: subnet A (10 hosts) ↔ subnet B (10 hosts) ↔ Internet. Broadcasts now stay within each subnet (2 broadcast domains). Host A→host B traffic crosses the router (L3 hop). The router's table: `10.0.1.0/24 → port 1`, `10.0.2.0/24 → port 2`, `0.0.0.0/0 → ISP` (default route).
4. **Gateway example**: connecting the office's legacy IPX network to the IP network requires a protocol gateway (translates IPX↔IP), because a router can't forward between different network-layer protocols.

## 9. Internal Working
1. **Repeater (internal)**: input port → amplifier/regenerator (clock recovery, reshape waveform) → output port(s). Both directions; no parsing. Limitation: 5-4-3 rule (legacy Ethernet: max 5 segments, 4 repeaters, 3 populated segments) because propagation timing constraints.
2. **Hub (internal)**: all ports electrically shorted into one bus internally — an incoming frame is retransmitted on every port simultaneously. Half-duplex, CSMA/CD still applies (collisions possible).
3. **Switch (internal)**: 
   a. Ingress: parse dest/source MAC, verify FCS.
   b. Learn: store (source MAC → ingress port) with aging (~5 min).
   c. Lookup: dest MAC in table → forward to that port; unknown → *flood* to all ports (except ingress).
   d. Broadcast/multicast MACs → flood. 
   e. Cut-through (forward on dest MAC before full frame) vs store-and-forward (CRC-checked) — production switches default store-and-forward for integrity.
   f. Spanning Tree Protocol (STP, IEEE 802.1D) blocks redundant links to prevent loops — switches learn paths, not routing.
4. **Router (internal)**: 
   a. Parse IP header, verify checksum, decrement TTL.
   b. `longest-prefix-match(dest IP, FIB)` → next hop + egress interface.
   c. Rewrite link header (new src/dst MAC), recompute link FCS, transmit.
   d. Routing table built by: directly-connected, static routes, or dynamic protocols (OSPF link-state, BGP path-vector, RIP distance-vector).
   e. Hardware fast-path: TCAM-based FIB lookup at line rate (400G routers); control plane (routing daemons) separate from data plane (forwarding ASICs).
5. **Gateway (internal)**: receives protocol-A unit, maps addresses/headers/payload to protocol-B format, forwards. May maintain state (call/session tables for VoIP), do NAT, or provide translation services (SMTP→HTTP for webmail APIs).

## 10. Time Complexity
- **Repeater/hub**: O(1) — bit regeneration, no lookup.
- **Switch forwarding**: O(1) with hash-based MAC table (or CAM); the table is searched by destination MAC hash. MAC table memory: O(number of hosts).
- **Router forwarding**: O(1) with TCAM (hardware longest-prefix match at line rate); software FIB lookup O(log n) with trie/LPM structures.
- **Bandwidth scaling**: hub total throughput = single link rate (shared); switch = per-port rate × ports (independent); router = per-port rates with internal switching fabric (crossbar, ~N² in ideal non-blocking).
- **Convergence** (time to recover from topology change): spanning tree ~50 s (STP) → milliseconds (RSTP/MSTP); routing protocols: OSPF fast-converge ~ms-s; BGP seconds-minutes.

## 11. Advantages
- **Repeater**: cheap, simple, extends reach without processing.
- **Hub**: trivial cost, no config, transparent to all protocols (bit-level).
- **Switch**: full-duplex per port, no collisions, learning-based efficiency, scales bandwidth with ports, VLANs, QoS, easy management (SNMP).
- **Router**: hierarchical addressing → global scale, path diversity (multiple routes), security boundary (ACLs), broadcast containment, WAN interconnects.
- **Gateway**: connects incompatible systems, enables legacy-to-modern migration, protocol independence at boundaries.

## 12. Disadvantages
- **Repeater/hub**: no isolation — one broadcast domain, one collision domain; waste bandwidth; half-duplex; no security or QoS.
- **Switch**: broadcasts still flood (L2 scale limit — mitigated by VLANs); loop risk (needs STP); MAC table size limits; doesn't provide L3 security (needs router/ACL).
- **Router**: higher per-packet cost (more header processing); config complexity (routing protocols); potential bottleneck if undersized; latency adds a hop.
- **Gateway**: translation overhead, stateful (single point of failure), often a performance/security bottleneck, complex to configure and maintain.

## 13. Interview Questions
1. **Q: What layer does each device operate at?** A: Repeater & hub = L1 (bits); switch & bridge = L2 (frames, MAC); router = L3 (packets, IP); gateway = varies (any layer, translation).
2. **Q (tricky): What's the difference between a hub and a switch beyond "smart"?** A: Hub = one shared medium: single collision domain, half-duplex, every frame to every port. Switch = per-port collision domain, full-duplex, frame forwarded only to the destination port via a learned MAC table.
3. **Q: How does a switch learn MAC addresses?** A: On ingress, it records (source MAC → ingress port) in a table with an aging timer (~5 min). On egress, it looks up the *destination* MAC; unknown destinations are flooded to all ports except the ingress one.
4. **Q (production): What happens when a switch receives a frame whose destination MAC is not in its table?** A: It floods it to all other ports. This is how ARP and unknown traffic work initially. If the switch has no port for a MAC after learning phase, flooding continues — a source of wasted bandwidth and (with VLANs) of broadcast-storm risk.
5. **Q: Why can't a switch replace a router?** A: Switches forward by *flat* MAC addresses and don't participate in routing protocols or hierarchical addressing. They can't choose a path across *different networks* (the Internet). Routers route by IP with a global, hierarchical scheme. A "L3 switch" blurs it (does IP routing in hardware) but still lacks WAN features (BGP, NAT at scale).
6. **Q: What is a "default gateway"?** A: The router a host sends packets to when the destination is not on the local subnet — the host's exit point. It's a role of a router (usually the home/office router), not a separate device type.
7. **Q (scenario): 100 hosts, heavy file sharing. Hub or switch?** A: Switch — hub creates one shared 100 Mbps collision domain where throughput collapses under load and collisions kill efficiency; a switch gives each pair full-duplex bandwidth and parallel flows.
8. **Q: What is store-and-forward vs cut-through switching?** A: Store-and-forward: buffer the whole frame, verify CRC, then forward (errors dropped). Cut-through: forward as soon as dest MAC is read (lower latency, but forwards corrupt frames). Production networks default to store-and-forward on edge; some use cut-through in low-latency fabrics (HFT).
9. **Q: What is Spanning Tree Protocol and why does a switch need it?** A: Switches with redundant links create L2 loops that circulate broadcast frames forever (broadcast storm). STP (802.1D/RSTP) elects a root and blocks redundant ports, ensuring a loop-free topology while keeping failover paths.
10. **Q (tricky): Is a home Wi-Fi router a "router"?** A: It's a composite: router (NAT + routing), switch (LAN ports), AP (Wi-Fi radio), DHCP server, DNS forwarder, and firewall — a multi-function gateway. Calling it "just a router" undersells it.
11. **Q: What is a gateway vs a router?** A: A router forwards packets between networks that *speak the same protocol* (IP). A gateway *translates* between *different* protocols/stacks. Every router is a "gateway" in the loose "default gateway" sense, but a true gateway does protocol conversion.
12. **Q (production): Why do datacenters use "switches" at the core even for routing?** A: They're L3 switches (routers in switch form factor) doing IP routing in hardware at line rate (400G). The "core switch" label reflects form factor + hardware forwarding, not that it's only L2.
13. **Q: What's the difference between a bridge and a switch?** A: Historically a bridge = 2-port L2 device; a switch = multi-port bridge on an ASIC. Same forwarding logic (MAC learning + forwarding). "Switch" is marketing for "fast multi-port bridge."
14. **Q (scenario): A user reports slow network. First devices to suspect?** A: Check physical (L1: cable/link light), then switch (L2: MAC table, CRC errors, congestion, broadcast storms), then router (L3: TTL, queue drops, routing tables). Devices are the failure *locations* in layer-by-layer troubleshooting.
15. **Q: Can a router work without a routing table?** A: Only for directly-connected subnets. Any packet to a non-local destination needs a route — explicit, default (0.0.0.0/0), or learned from a routing protocol. No route = "Network Unreachable" (ICMP).
16. **Q (tricky): Does a hub forward a frame to the sender's port?** A: Yes — a hub retransmits on *all* ports including the ingress one (it has no concept of "sender port"). A switch explicitly does NOT forward back to the ingress port. Tiny detail, common gotcha.

## 14. Follow-Up Questions
1. **Q: What's the 5-4-3 rule and why did it die?** A: Legacy Ethernet allowed max 5 segments, 4 repeaters, 3 populated segments due to round-trip timing (propagation + collision detection). Switches eliminated the shared collision domain, so the rule is obsolete.
2. **Q: What's the difference between MAC learning and routing?** A: MAC learning is *passive observation* of a single LAN; routing is *proactive path computation* across networks (metrics, topology, convergence). Switches learn; routers compute.
3. **Q: How do VLANs affect broadcast domains?** A: A VLAN partitions one physical switch into multiple logical broadcast domains (one per VLAN). Broadcast frames only reach ports in the same VLAN — the primary tool for scaling L2 networks.
4. **Q: What's the difference between a router's control plane and data plane?** A: Control plane = routing daemons/table computation (slow, CPU); data plane = forwarding packets via FIB/TCAM (fast, ASIC). This separation is why routers forward at line rate.
5. **Q: Why do optical "repeaters" sometimes not regenerate but amplify?** A: Amplifiers (EDFA) boost light signal strength but add noise without reshaping (no timing recovery); regenerators fully rebuild the signal. For long-haul, the choice is about distance, budget, and bit-rate transparency.

## 15. Coding Example
```python
# Simulating switch MAC learning + forwarding, and router longest-prefix routing
class Switch:
    def __init__(self, ports):
        self.ports = ports
        self.mac_table = {}   # mac -> port
    def receive(self, frame, in_port):
        src, dst = frame["src"], frame["dst"]
        self.mac_table[src] = in_port                     # learn source
        if dst == "ff:ff:ff:ff:ff:ff":                    # broadcast -> flood
            return [p for p in self.ports if p != in_port]
        if dst in self.mac_table:                         # known -> unicast
            return [self.mac_table[dst]]
        return [p for p in self.ports if p != in_port]    # unknown -> flood

class Router:
    def __init__(self, routes):
        self.fib = sorted(routes, key=lambda r: r["prefix_len"], reverse=True)
    def route(self, dst_ip):
        for r in self.fib:                                # longest prefix match
            prefix, plen = r["prefix"], r["prefix_len"]
            if dst_ip >> (32 - plen) == prefix >> (32 - plen):
                return r["next_hop"]
        return None

sw = Switch(ports=[1, 2, 3, 4])
print("Unknown unicast ->", sw.receive({"src": "aa:aa", "dst": "bb:bb"}, 1))  # flood [2,3,4]
print("Now known      ->", sw.receive({"src": "aa:aa", "dst": "bb:bb"}, 1))  # [2] once bb learned

rt = Router([{"prefix": 0xC0A80000, "prefix_len": 24, "next_hop": "10.0.0.1"},   # 192.168.0.0/24
             {"prefix": 0x00000000, "prefix_len": 0,  "next_hop": "1.1.1.1"}])   # default
print("192.168.0.55 ->", rt.route(0xC0A80037))   # 10.0.0.1 (longest match)
print("8.8.8.8      ->", rt.route(0x08080808))   # 1.1.1.1 (default route)
```
```
# Linux: inspect the real devices on your machine
$ ip link                    # L1/L2 devices: ethernet, lo, wlan0
$ ip route                   # router FIB: prefix + next hop (longest prefix match)
# default via 192.168.1.1 dev eth0
# 192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
$ bridge link show           # switch MAC learning table (Linux bridge)
```

## 16. Industry Usage
- **Amazon/AWS**: VPC route tables are *router* configuration (LPM); VPC subnets; Internet Gateway (IGW) is a gateway device; NAT Gateway; transit gateways (hubs). Security groups = router-level (L3/L4) filtering.
- **Google**: Jupiter fabric = datacenter *switch* network (leaf-spine, 1 PB/s bisection); B4 WAN = *routers* + SDN control. Google's Global LB = Anycast L3/L7.
- **Meta**: DCs use *switches* (ToR + spine) with BGP for L2/L3 interop; their "Data Center Fabric" is a giant switch network.
- **Cisco/Juniper/Arista**: enterprise three-tier design (access switch → distribution switch → core router/switch); SD-WAN (routers with centralized control).
- **Every home/office**: the "router" is the composite gateway — the single most common networking device on Earth.

## 17. References
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 1.2-1.4 (switches vs routers).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 3 (Data Link / bridges & switches), Ch. 5 (routing).
- Cisco Press, *CCNA 200-301 Official Cert Guide*, Vol. 1 (LAN switching, routers).
- IEEE 802.1D (STP), IEEE 802.3 (Ethernet), RFC 826 (ARP), RFC 1812 (router requirements).
- Forouzan, *Data Communications and Networking*, 5th ed., Ch. 12-14.

## 18. Cheat Sheet
- Ladder: repeater (L1) → hub (L1) → switch (L2, MAC) → router (L3, IP) → gateway (translate).
- Hub = 1 collision domain + 1 broadcast domain; switch = per-port collision domain, 1 broadcast domain; router = separates broadcast domains.
- Switch learns source MACs, forwards by dest MAC, floods unknowns/broadcasts.
- Router: longest-prefix-match FIB, TTL decrement, per-hop link-header rewrite.
- Default gateway = host's exit router. L3 switch = switch that routes in hardware.
- STP prevents L2 loops; RSTP converges in ms.
- 5-4-3 rule dead (switched Ethernet).
- Hub forwards back to ingress port; switch does not.

## 19. Quiz
1. A hub creates: a) per-port collision domains b) one shared collision domain c) no collisions d) broadcast separation → **b**
2. A router forwards by: a) MAC b) IP (longest prefix) c) port number d) frame length → **b**
3. A switch with an unknown dest MAC: a) drops b) floods c) buffers d) routes → **b**
4. STP prevents: a) routing loops b) broadcast storms from L2 loops c) collisions d) NAT conflicts → **b**
5. Which is L1? a) router b) switch c) repeater d) gateway → **c**
6. The "default gateway" is usually a: a) switch b) router c) repeater d) bridge → **b**
7. A gateway vs a router: a) same thing b) gateway translates protocols c) router translates d) no difference → **b**
8. Cut-through switching forwards: a) after CRC b) as soon as dest MAC read c) after full frame d) never → **b**
9. Switch MAC table stores: a) IP→MAC b) source MAC→port c) dest MAC→IP d) route→nexthop → **b**
10. Broadcasts reach: a) all ports of a router b) all ports in a broadcast domain (same L2) c) only one host d) the WAN → **b**

## 20. Flashcards
- **Q: Device→layer ladder?** → **A:** Repeater/hub L1, switch L2, router L3, gateway translate.
- **Q: Collision/broadcast domains of a hub?** → **A:** One of each (shared medium).
- **Q: How do switches learn?** → **A:** Source MAC → ingress port, aged ~5 min; forward by dest MAC, flood unknowns.
- **Q: What does a router match on?** → **A:** Longest-prefix-match on destination IP in the FIB.
- **Q: What is a default gateway?** → **A:** The router a host uses to leave its subnet.
- **Q: Why does a switch need STP?** → **A:** To break L2 loops that would cause broadcast storms.

## 21. Revision
Devices climb the intelligence ladder. Repeater/hub = L1, dumb bit regeneration/duplication (one collision domain, one broadcast domain). Switch = L2, learns source MACs, forwards by dest MAC, per-port collision domains, floods unknowns/broadcasts (still one broadcast domain). Router = L3, longest-prefix-match IP forwarding, terminates broadcast domains, connects networks via routing tables. Gateway = protocol translator between different stacks. The home "router" is a composite gateway. Switches need STP against loops; routers compute paths with OSPF/BGP. The device ladder is also the troubleshooting ladder: L1 lights → L2 MAC/CRC → L3 routes.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Hub vs switch vs router?" | 2 How It Works / 13 Q&A |
| "What layer is each device?" | 7 Formal Definition / 13 Q&A |
| "How does a switch learn MACs?" | 9 Internal Working / 13 Q&A |
| "Why can't a switch replace a router?" | 4 Why Another Approach / 13 Q&A |
| "What is a default gateway?" | 13 Q&A / 3 When Used |
| "What is STP for?" | 9 Internal Working / 13 Q&A |
| "Gateway vs router?" | 13 Q&A / 7 Formal Definition |
