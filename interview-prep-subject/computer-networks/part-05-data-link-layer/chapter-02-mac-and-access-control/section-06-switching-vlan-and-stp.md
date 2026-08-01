# Switching, VLAN, and Spanning Tree Protocol

> **TL;DR**: A switch forwards frames by learned MAC→port mappings (transparent bridging), VLANs (IEEE 802.1Q) segment a physical switch into multiple isolated L2 broadcast domains with a 4-byte tag, and Spanning Tree Protocol (IEEE 802.1D) turns redundant, looping topologies into a loop-free tree by electing a root bridge and blocking redundant ports.

## 1. Why Does This Exist?
A single Ethernet segment can only grow so far: every station shares the medium, collisions and broadcast flooding grow with the segment, and one broken link kills the whole "collision/broadcast domain." Ethernet needs *more machines than one cable can hold* — that's what a switch (a.k.a. multi-port bridge, IEEE 802.1D transparent bridge) solves: it learns where each MAC lives and forwards frames only to the right port, isolating traffic, eliminating collisions (each port is its own full-duplex segment), and multiplying bandwidth (N ports can carry N conversations simultaneously). Switches alone aren't enough, though: a campus/data center must separate departments, tenants, or security zones even when they share the same physical fabric — that's **VLANs**. And because resilient networks connect switches in *redundant loops* (if a link fails, another path takes over), those loops would cause broadcast storms and MAC-table thrashing — that's what **STP** exists to prevent.

## 2. How Does It Work?
**Switching (transparent bridging)**: the switch maintains a MAC table (MAC → port + age). It learns from the *source* MAC of every ingress frame (associating it with the ingress port), and forwards by *destination* MAC: known → forward out that port only; unknown/multicast/broadcast → flood all ports (except ingress). Ports in the same collision/broadcast domain are learned/forwarded accordingly; VLANs partition learning and flooding. **VLAN (802.1Q)**: a 4-byte tag (TPID 0x8100 + PCP/DEI + 12-bit VID) inserted after the source MAC; switches use the VID to restrict flooding and forwarding to member ports; trunk links carry many VLANs tagged, access ports are untagged in one VLAN. **STP (802.1D)**: switches exchange BPDUs, elect the lowest-bridge-ID switch as **root**, compute the least-cost path to root on every switch, and put non-root, non-designated ports in **Blocking**; only root/designated ports forward. If a working link fails, a blocked port transitions to forwarding (via listening/learning) — redundancy without loops.

## 3. When Is It Used?
- **Switching**: everywhere — from 8-port home switches to 4K-port data-center fabrics (ToR, leaf-spine); L2-only, wire-speed, low latency.
- **VLANs**: department/tenant segmentation; security zones; guest networks; storage (iSCSI) vs data separation; VM/multi-tenant cloud networking (VLAN per tenant, trunking to hypervisors); voice VLANs (LLDP-MED); reducing broadcast domains.
- **STP/RSTP**: any redundant-switch design — campus, DC topologies with dual uplinks; RSTP (802.1w) for sub-second convergence; MSTP (802.1s) for per-VLAN trees. DCs increasingly use TRILL/SPB or just layer-3 (leaf-spine with ECMP) to avoid STP's blocking, but STP remains the L2 loop-prevention baseline.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: hubs/repeaters (no intelligence).* Hubs broadcast everything → one big collision domain, no isolation, no throughput scaling. Switches use the frames' MACs to isolate traffic and give each port a full-duplex segment — a strictly better replacement at near-equal cost.
- *Alternative: routers for every segment.* Routers isolate broadcast domains and provide security, but they're slower (L3 processing), costlier, and can't handle raw LAN forwarding volume; you need *some* L2 everywhere. Switches were built because L2 forwarding is cheap and wire-speed.
- *Alternative: one giant flat LAN, no VLANs.* Every broadcast (ARP, DHCP, mDNS) hits every host; a loop or flood affects everyone; no tenant isolation; MAC-table sizes explode. VLANs give broadcast isolation and segmentation *without* buying more switches — the L2 analogue of subnetting.
- *Alternative: rely on TCP/upper layers to handle loops.* A loop is catastrophic at L2: broadcast frames circulate forever (broadcast storm), and the MAC table flaps because the same MAC is seen on multiple ports. There is *no upper-layer recovery* — L2 must prevent loops itself, hence STP (vs. running routing protocols like OSPF/BGP which compute loop-free paths in software).
- *Alternative: run all redundant links as active (load-balance) like routers do.* Ethernet has no TTL in frames, so a packet entering a loop is never discarded — it circulates forever. STP deliberately *blocks* ports (wasting capacity) because active-active at L2 is unsafe without TTL; that's why modern DCs prefer L3 ECMP and why TRILL/SPB/VXLAN-BGP-EVPN (which add TTL-like hop counts) exist.

## 5. Intuition
A switch is a **sorted-mail post office**: it learns which "mailbox" (port) each address lives behind by watching the return address of every letter, and then sorts mail to the correct pigeonhole instead of photocopying it to everyone. VLANs are **separate post offices in one building**: green mail (VLAN 10) is never delivered to the blue department (VLAN 20), even though they share the same loading dock (the trunk). STP is the **traffic cop** who switches off some routes so that, even though the road map has loops (redundancy), every destination has *exactly one* path — if the cop's chosen route breaks, he reactivates a spare.

## 6. Real-World Analogy
Think of **airports (switches), airline alliances (VLANs), and road redundancy (STP)**. A switch is the airport baggage system that reads each bag's tag (destination MAC) and sends it down the correct conveyor to the right gate; it learns which gate to use by seeing which gate *emits* bags with each label (source MAC learning). VLANs are like the airport keeping international and domestic passengers strictly separate — same terminal, different security checkpoints and boarding areas. STP is the city's road network built with multiple bridges (redundancy) but with one-way streets chosen so that you can *always* reach every district by exactly one route; when a bridge collapses (link down), traffic previously blocked is re-routed — never two ways to the same place at once (that would cause circling traffic = broadcast storm).

## 7. Formal Definition
**Transparent bridge / switch** (IEEE 802.1D): a multi-port L2 device that learns {source MAC → port} on every received frame, ages entries (default 300 s), forwards known unicast to the learned port, and floods unknown/multicast/broadcast; forwarding is transparent to hosts (they don't know a switch is in the path). **VLAN** (IEEE 802.1Q): an 802.3 frame is extended by a 4-byte tag — TPID (0x8100), PCP (3-bit priority), DEI, VID (12-bit VLAN ID, 0 & 4095 reserved) — inserted between source MAC and EtherType; ports are access (untagged) or trunk (tagged); each VLAN is an isolated broadcast domain with its own MAC learning and flooding. **STP** (IEEE 802.1D): each bridge has a Bridge ID (priority 0–65535 + MAC); BPDUs are exchanged every 2 s (hello); the lowest Bridge ID is the root; every bridge computes the least-cost path to the root (cost = 1 per 10 Gb/s up to 100 per 10 Mb/s; path cost = sum); the bridge nearest root on each LAN is the designated bridge; non-designated ports go Blocking; a blocked port may transition Listening(15s)→Learning(15s)→Forwarding. **RSTP** (802.1w) converges in seconds by using proposal/agreement and edge ports; **MSTP** (802.1s) maps multiple VLANs to multiple spanning trees.

## 8. Example
**VLAN-tagged frame walk.** Host on access port (VLAN 10) sends an untagged frame to host on a trunk. The switch:
1. Receives frame on access port → tag is added: insert TPID `0x8100`, PCP `000`, DEI `0`, VID `000000001010` (=10) between SrcMAC and EtherType.
2. Looks up (VLAN 10, dest MAC) → learned on trunk port → forwards tagged out the trunk.
3. Remote switch strips the tag on its access port (VLAN 10) and delivers untagged to the destination.
Frame grows from 1518 to 1522 bytes; the CRC-32 must be recomputed because the frame content changed.

**STP example.** Switches S1 (BID = 32768.MAC1), S2 (32768.MAC2), S3 (4096.MAC3), all interconnected in a triangle. 
- Lowest BID wins → **S3 is root** (priority 4096 < 32768). 
- S3's ports are root ports (designated); S1/S2 compute cost to S3: S1→S3 via direct link cost 4 (1 GbE), S1→S2→S3 cost 4+4=8 → S1's direct link is its root path; the S1–S2 link's *designated* side is chosen (one port blocks). 
- Result: a spanning tree rooted at S3 — exactly one active path between any two switches; the blocked port is a backup.

## 9. Internal Working
1. **MAC learning + aging**: ingress frame → learn source MAC→port (or refresh); entries age out (default 300 s; `mac-address-table aging-time`). A MAC seen on two ports alternately = port-flap (loop warning).
2. **Forwarding decision**: hash(VLAN, dest MAC) → FDB lookup → forward to port, or flood; broadcast/multicast always flood the VLAN.
3. **VLAN data plane**: untagged → access port's PVID → forward in that VLAN, tag on trunk; tagged → check VID allowed on ingress trunk; drop if not. CPU generates BPDUs/ARP/etc. from the management VLAN.
4. **STP state machine**: every port is Root (toward root), Designated (best on its LAN), or Blocking. BPDUs: Root ID, Sender Bridge ID, Root Path Cost, Port ID. Election: root by lowest BID; then per-switch lowest cost to root; then lowest sender BID; then lowest port ID. Forwarding begins only after Listening→Learning timers (STP: 30 s; RSTP: handshake ~ms).
5. **RSTP optimizations**: edge ports (hosts) skip timers; proposal/agreement propagates the tree quickly; link failure detected in ms → alternate port takes over.
6. **Failure handling**: on root-port failure, a switch immediately enables the best alternate/backup blocked port (RSTP) — that's the redundancy STP buys.

## 10. Time Complexity / Performance
- **Forwarding**: O(1) per frame — a hash lookup into the FDB (TCAM/hash in ASICs) at wire speed (400 Gbps = ~600 Mpps at 84-byte frames).
- **Learning**: O(1) per frame; table size = number of learned MACs (switch ASIC capacity: 8K–2M entries; DC fabrics use larger or offload).
- **STP convergence**: classic 802.1D = 30–50 s (Listening+Learning timers per topology change); RSTP = ms–s (link-down detection + alternate ports); MSTP = per-instance.
- **VLAN count**: 4094 usable VIDs per 802.1Q — a real scale limit (why VXLAN's 16M VNIs and Q-in-Q exist for huge multi-tenant clouds).

## 11. Advantages
- **Switching**: isolates collision domains, gives full-duplex per port, line-rate forwarding, low latency, cheap silicon, transparent to hosts.
- **VLANs**: security/tenant isolation without new hardware; broadcast-domain reduction; flexible reconfiguration (move a host's VLAN by port config, not cabling); QoS via PCP bits; multi-tenant clouds (VLAN/VXLAN per tenant).
- **STP**: makes redundant topologies safe — no broadcast storms, no MAC flapping; automatic failover; simple, distributed, no central controller; RSTP converges in seconds.

## 12. Disadvantages
- **MAC-table limits**: flooding when table full (security risk + inefficiency); MAC flooding attacks fill it.
- **Broadcast still floods the VLAN**: every broadcast (ARP, DHCP) reaches all VLAN members — storms still possible within a VLAN without storm control.
- **STP blocks ports → wasted capacity** (active/standby); convergence delay (classic STP 30-50 s) = outage during failover; complex timer tuning; one misconfigured BID can hijack the root.
- **VLAN limits**: 4094 VIDs; VLAN hopping attacks; tag handling adds 4 bytes + recompute CRC.
- **L2 scalability ceiling**: flat MAC learning doesn't scale to huge DCs (hence L3 leaf-spine, VXLAN-BGP-EVPN, TRILL/SPB).

## 13. Interview Questions
1. **Q: How does a switch learn MAC addresses?** A: It reads the *source* MAC of every frame and records {MAC → ingress port} with an age timer (default 300 s). Later, a frame destined to that MAC is forwarded only out that port; on unknown/unlearned MAC it floods.

2. **Q: What's the difference between a switch and a hub?** A: A hub is a physical-layer repeater — every frame goes to every port, one collision domain, total throughput = link rate. A switch is a data-link device: it learns MAC→port, forwards only to the destination port, and each port is a separate collision domain with full-duplex — N simultaneous conversations.

3. **Q: What is a VLAN and how does the 802.1Q tag work?** A: A VLAN is a broadcast domain created in software — frames in VLAN 10 never reach VLAN 20 even on the same switch. The tag is 4 bytes inserted after the source MAC: TPID 0x8100 + PCP(3) + DEI(1) + VID(12). Trunk ports carry tagged frames of many VLANs; access ports are untagged.

4. **Q: What are access ports vs trunk ports?** A: Access: carries one untagged VLAN (frames get tagged internally by the switch's PVID); hosts' NICs see plain Ethernet. Trunk: carries tagged frames for multiple VLANs (used between switches / to hypervisors). Trunk = tagged; access = untagged.

5. **Q: Why does a tagged frame need the FCS recomputed?** A: Because the CRC-32 (FCS) covers dest MAC through payload; inserting the 4-byte tag changes those bytes, so the switch recomputes the FCS. The frame grows 1518→1522 bytes and must be re-validated.

6. **Q: What problem does STP solve and how?** A: Redundant links create L2 loops; Ethernet frames have no TTL, so loops → broadcast storms and MAC-table flapping. STP elects a root bridge, computes shortest paths, and *blocks* redundant ports so exactly one active path exists per segment — turning a mesh into a tree while keeping backup paths for failover.

7. **Q: TRICKY — How is the root bridge elected?** A: Every switch sends BPDUs announcing its Bridge ID (priority 2 bytes + MAC 6 bytes). The lowest Bridge ID wins: lowest priority first, then lowest MAC. Tie-break for the *root path cost* then *sender BID* then *port ID* decides which of two competing links stays forwarding.

8. **Q: What are the STP port states and their timers?** A: Blocking (no forwarding, 20 s max-age), Listening (15 s), Learning (15 s, builds MAC table but doesn't forward), Forwarding (active), Disabled. Classic convergence = ~30-50 s; RSTP cuts it to ~ms–1 s using alternate ports + proposal/agreement.

9. **Q: PRODUCTION — A switch reports a new root bridge after every reboot. What's wrong?** A: The rebooting switch likely has a *lower* priority (or lower MAC) than intended, so STP elects it root and the whole topology reconverges — causing outages. Fix: set the intended root's priority explicitly (e.g., `spanning-tree vlan 1 root primary`, or priority 4096), keep BIDs deterministic, and monitor `show spanning-tree`.

10. **Q: What are RSTP and MSTP, and when would you use them?** A: RSTP (802.1w) converges in seconds using edge ports and proposal/agreement — default on modern switches. MSTP (802.1s) maps VLANs to multiple spanning-tree instances, allowing load balancing across VLANs instead of one tree blocking half the fabric.

11. **Q: SCENARIO — You connect two switches with two cables "for redundancy" and the LAN dies. Why?** A: Without STP, the redundant link creates a loop: broadcast frames circulate endlessly (broadcast storm) and MAC tables flap. The fix is enabling STP/RSTP (it's usually on by default, but if someone disabled it or it failed, the storm returns) — and verifying with `show spanning-tree` + `show mac address-table`.

12. **Q: How does STP "waste" capacity and why do data centers dislike it?** A: STP blocks redundant links → active/standby (a 2×2 fabric uses ~half its bandwidth). DCs want active-active → they move to L3 with ECMP (equal-cost multi-path) or to overlay designs (VXLAN+BGP-EVPN) where the *fabric* is L3 and L2 is virtualized — STP only applies inside the broadcast domain.

13. **Q: What is a broadcast storm and what causes it?** A: A broadcast frame circulating a loop, re-broadcast at every switch, multiplying until the network saturates — caused by loops (no STP), or by certain failure modes (STP disabled, forwarding loops in misconfigured trunks). Mitigations: STP, storm control, BPDU guard, loop guard.

14. **Q: TRICKY — A host's MAC appears on two different switch ports at once. What's happening?** A: Either the host is genuinely on both (bonding/teaming without LACP, or VM with multiple NICs sharing a MAC), or there's a loop (the switch sees the same frame twice). The FDB flaps; the switch may bounce the port or block on `spanning-tree portfast bpduguard`. This is the classic loop diagnostic.

15. **Q: What is the path cost in STP and how does it change with speed?** A: Cost = 100 Mb/s: 19; 1 Gb/s: 4; 10 Gb/s: 2; 100 Gb/s: 1 (standardized values; older formula = 1000/speed). Root path cost = sum of costs toward root; the lowest-cost path is used; equal costs are broken by sender BID/port ID.

16. **Q: PRODUCTION — How do you troubleshoot "MAC table full" on a switch?** A: Check for a loop (same MAC on many ports, flapping), an attacker flooding random source MACs (MAC flooding → switch turns into a hub → sniffing), or an undersized FDB for the network size. Use `show mac address-table count`, storm-control/MAC limits, and L3 segmentation to shrink the domain.

17. **Q: What is the difference between a collision domain and a broadcast domain?** A: Collision domain = set of devices that can collide (one shared wire); each switch port is its own. Broadcast domain = set that receives each other's broadcasts (a VLAN); switches flood within a VLAN, so a VLAN is a broadcast domain. Routers terminate broadcast domains.

18. **Q: SCENARIO — You add VLAN 100 on a trunk and hosts in VLAN 100 on both ends can't ping. Diagnose.** A: Check: is the trunk `allowed vlan` list correct (native VLAN mismatch is the #1 cause — untagged traffic on one end tagged on the other)? Are both access ports' PVID = 100? Is the VLAN created on *all* transit switches? Do the hosts have IPs in the same subnet? Capture with `tcpdump -e vlan` to see tags.

## 14. Follow-Up Questions
1. **Q: What is the native VLAN and what's the risk of a native-VLAN mismatch?** A: The untagged VLAN on a trunk (default 1). If two ends disagree, untagged frames (BPDUs are native!) get classified differently — a classic cause of STP/BPDU forwarding errors and VLAN hopping. Keep native VLAN consistent (ideally a dedicated one).

2. **Q: What are BPDU guard, root guard, and loop guard?** A: BPDU guard: shut down a port that receives BPDUs (stops rogue bridges). Root guard: block a port that would become root. Loop guard: block a port that stops receiving BPDUs (prevents a failing one-way link from forming a loop). These are the operational hardening of STP.

3. **Q: Why does VXLAN exist given VLANs?** A: 802.1Q has 4094 VIDs and is confined to L2 fabrics; VXLAN gives 16M VNIs and encapsulates L2 in UDP/IP so tenants can span IP networks (and clouds). VLAN = L2 tag; VXLAN = L2-over-L3 tunnel — the multi-tenant cloud replacement.

4. **Q: What's the difference between store-and-forward and cut-through switching?** A: Store-and-forward: receive whole frame, validate FCS, then forward (no bad frames propagate; more latency). Cut-through: forward as soon as the destination MAC is read (~no FCS check; lower latency; used in low-latency DC fabrics). Latency difference ~hundreds of ns.

## 15. Coding Example
```python
from dataclasses import dataclass, field
from collections import OrderedDict

@dataclass
class SwitchPort:
    name: str
    vlan: int

class LearningSwitch:
    def __init__(self):
        self.fdb = OrderedDict()      # (vlan, mac) -> port
        self.ports = {}               # port -> vlan

    def learn(self, vlan, src_mac, port, age_max=300):
        self.fdb[(vlan, src_mac)] = port
        # trivial aging: drop if not refreshed (production uses timers)

    def forward(self, frame, port):
        vlan = frame.vlan
        self.learn(vlan, frame.src_mac, port)
        if frame.dst_mac == "ff:ff:ff:ff:ff:ff":
            return [p for p in self.ports if p != port]   # broadcast -> flood
        dst = self.fdb.get((vlan, frame.dst_mac))
        if dst is not None:
            return [dst]                                   # known -> unicast
        return [p for p in self.ports if p != port]        # unknown -> flood

def tag_frame(dst, src, vid, payload):
    """802.1Q tagging: TPID 0x8100 + PCP/DEI/VID inserted before EtherType."""
    import struct
    tci = (0 << 13) | (0 << 12) | vid            # PCP=0, DEI=0, VID
    return (bytes.fromhex(dst.replace(":","")) + bytes.fromhex(src.replace(":",""))
            + struct.pack("!HH", 0x8100, tci) + b"\x08\x00" + payload)
```
```python
# Minimal STP root election (802.1D logic)
class Bridge:
    def __init__(self, priority, mac):
        self.bid = (priority, mac)          # Bridge ID (priority + MAC)
        self.root = self.bid                 # starts as its own root
        self.root_path_cost = 0

def stp_elect(bridges, links):
    # BPDU propagation: root = min bid over all; costs = shortest path
    changed = True
    while changed:
        changed = False
        for b in bridges:
            for other in bridges:
                if other in links.get(b, []):
                    cost = 4 if 1000 else 4    # 1 GbE = cost 4
                    cand_cost = other.root_path_cost + cost
                    if other.bid < b.root or (other.bid == b.root and cand_cost < b.root_path_cost):
                        b.root = other.bid
                        b.root_path_cost = cand_cost
                        changed = True
    return {b.mac: (b.root, b.root_path_cost) for b in bridges}

bridges = [Bridge(32768, "aa"), Bridge(32768, "bb"), Bridge(4096, "cc")]
print(stp_elect(bridges, {"aa": {"bb","cc"}, "bb": {"aa","cc"}, "cc": {"aa","bb"}}))
```
```bash
# Practical switch/VLAN/STP debugging
ip link add link eth0 name eth0.10 type vlan id 10      # Linux VLAN subinterface
bridge vlan show                                         # native/allowed VLANs
bridge link show                                         # port state + STP
sudo bridge link set dev eth0 cost 4                     # STP cost tweak
sudo brctl show / bridge fdb show                        # FDB contents (bridging)
tcpdump -i any -e -nn 'vlan'                             # see 802.1Q tags on the wire
ip -details link show br0                                # STP state of bridge ports
```

## 16. Industry Usage
- **Data centers**: leaf-spine L2/L3 fabrics; 100G/400G ToR switches (Arista, Cisco, Juniper, NVIDIA); VXLAN + BGP-EVPN for multi-tenant L2-over-L3; MC-LAG for active-active uplinks.
- **Cloud**: AWS/GCP/Azure VPCs are VLAN/VXLAN-based tenant isolation over shared fabrics; hypervisor vSwitch (Open vSwitch) implements MAC learning + VLAN/overlay in software.
- **Enterprise/campus**: RSTP/MSTP (often Cisco PVST+) with access hardening (BPDU guard, root guard); VLAN segmentation per department/security zone.
- **Service provider**: QinQ (802.1ad) for subscriber multiplexing; Metro Ethernet (802.1ah) MAC-in-MAC.
- **Linux**: the bridge/switch/STP stack (`bridge`, `ip link set type bridge stp_state`, `brctl`) powers containers/VMs networking; Open vSwitch + DPDK forward at line rate.

## 17. References
- IEEE Std 802.1D-2004 (MAC Bridges / STP), 802.1w/RSTP, 802.1Q-2018 (VLAN) — https://standards.ieee.org/ieee/802.1Q/6824/
- Kurose & Ross, *Computer Networking*, 8th ed., §6.4.2/§6.4.3 (Switches, VLANs).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §4.1.4 (Spanning Tree), §4.4 (Bridges).
- RFC 5517 (Cisco's STP/802.1D history) — https://datatracker.ietf.org/doc/html/rfc5517
- Radia Perlman, *Interconnections: Bridges, Routers, Switches* — the definitive STP/bridge reference.
- Linux bridging docs — https://docs.kernel.org/networking/bridge.html

## 18. Cheat Sheet
- Switch = L2, learns source MAC→port, forwards to learned port, floods unknown/broadcast/multicast; each port = its own collision/full-duplex domain.
- FDB entries age out (300 s default); MAC table full → flood (security risk).
- 802.1Q tag: TPID 0x8100 | PCP(3) DEI(1) VID(12) inserted before EtherType; frame 1518→1522; FCS recomputed.
- Access port = one untagged VLAN (PVID); trunk = tagged, many VLANs; native VLAN = untagged on trunk.
- VLAN = broadcast domain; routers end broadcast domains.
- STP: elect root (lowest BID = priority+MAC); compute least-cost path; block redundant ports → tree.
- BPDU hello 2 s; ports Blocking→Listening(15s)→Learning(15s)→Forwarding; max-age 20 s.
- RSTP converges in seconds; MSTP = multiple trees per VLAN group.
- Loop symptoms: broadcast storm, MAC flapping, port bounce; prevent with STP + BPDU guard.
- VXLAN replaces VLAN at cloud scale (16M VNIs, L2-over-UDP).

## 19. Quiz
1. A switch learns MACs from: a) destination MAC b) source MAC c) EtherType d) FCS → **b**
2. Unknown unicast is: a) dropped b) flooded c) queued d) routed → **b**
3. 802.1Q tag size: a) 2 B b) 4 B c) 8 B d) 6 B → **b**
4. VID is: a) 8 bits b) 12 bits c) 16 bits d) 3 bits → **b**
5. The root bridge has: a) highest BID b) lowest BID c) most ports d) highest cost → **b**
6. STP port in Listening state: a) forwards b) learns c) neither d) sends BPDUs only → **c**
7. STP convergence time (classic): a) ms b) 1 s c) 30–50 s d) 5 min → **c**
8. Which replaces VLANs at cloud scale? a) QinQ b) VXLAN c) MPLS d) STP → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-c, 7-c, 8-b.

## 20. Flashcards
- **Q: How does a switch learn and forward?** → **A:** Learns source MAC→port; forwards known dest to that port, floods unknown/broadcast.
- **Q: What is a VLAN?** → **A:** A broadcast domain isolated in software via a 4-byte 802.1Q tag (TPID 0x8100 + VID).
- **Q: Access vs trunk port?** → **A:** Access = one untagged VLAN; trunk = tagged, carries many VLANs.
- **Q: Why does STP exist?** → **A:** L2 frames have no TTL; loops → broadcast storms + MAC flapping; STP blocks redundant ports → loop-free tree.
- **Q: How is the root elected?** → **A:** Lowest Bridge ID (priority + MAC) wins.
- **Q: What are the STP port states?** → **A:** Blocking→Listening→Learning→Forwarding (timers ~15 s each, classic).
- **Q: What happens to the FCS when tagging?** → **A:** Recomputed (tag is in the CRC scope), frame grows 4 bytes.
- **Q: Why do DCs prefer L3/ECMP over STP?** → **A:** STP blocks ports (wasted bandwidth, slow failover); L3 ECMP is active-active.

## 21. Revision
A switch is a transparent L2 forwarder: it learns {source MAC→port} from ingress frames and forwards by destination MAC — known→unicast, unknown/broadcast/multicast→flood — with each port an isolated full-duplex collision domain. VLANs (802.1Q) segment a physical switch into independent broadcast domains using a 4-byte tag (TPID 0x8100, PCP, DEI, 12-bit VID) inserted before the EtherType (FCS recomputed, frame 1518→1522); access ports are untagged (PVID), trunks carry tagged frames. STP (802.1D) prevents L2 loops (no TTL in Ethernet): elect the root by lowest Bridge ID, compute least-cost paths via BPDUs, and block redundant ports, converging in 30–50 s (RSTP in seconds). Because STP wastes capacity, data centers use L3 leaf-spine ECMP and VXLAN-BGP-EVPN overlays instead. Anchor: *switch = learned mail sorter; VLAN = isolated broadcast domain; STP = one active path per LAN, backups on stand-by.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How does a switch learn/forward?" | 9 / 13-Q1,2 |
| "What is a VLAN / how does the 802.1Q tag work?" | 13-Q3,4,5 |
| "Why does STP exist / how is root elected?" | 13-Q6,7 / 8 |
| "STP port states and timers" | 13-Q8 |
| "New root after reboot — why?" | 13-Q9 |
| "Two cables to a switch kill the LAN — why?" | 13-Q11 |
| "Why do DCs avoid STP?" | 13-Q12 |
| "MAC appears on two ports / MAC table full" | 13-Q14,16 |
| "VLAN 100 can't ping across trunk — diagnose" | 13-Q18 |
| "Native VLAN mismatch / BPDU guard" | 14-Q1,2 |
