# VLANs and Switching Principles — 100 Interview Q&A

## Q1: What is a VLAN and what problem does it solve?

**A:** A VLAN (Virtual Local Area Network) is a logical segmentation of a physical network into multiple isolated Layer 2 broadcast domains. Devices in the same VLAN communicate as if they were on the same physical segment, regardless of their physical location on the switch fabric. A single switch can carry dozens of independent VLANs, with each VLAN behaving like its own isolated switch.

The primary problems VLANs solve are broadcast containment, security isolation, and network flexibility. Without VLANs, every broadcast frame in a flat network reaches every connected device, wasting bandwidth and CPU. With VLANs, broadcasts are confined to the VLAN's membership, and traffic between VLANs only flows through a routing device (Layer 3 gateway), enabling policy enforcement at the boundary.

VLANs also decouple logical grouping from physical wiring. A finance team spread across four floors can share one VLAN without re-cabling, and moving a user between offices only requires re-tagging their access port. This flexibility, combined with broadcast and security control, makes VLANs the fundamental unit of segmentation in every modern switched network.

## Q2: How does a VLAN relate to a broadcast domain?

**A:** A broadcast domain is the set of all devices that receive a broadcast frame sent by any one of them. In Ethernet, broadcast frames are sent to the all-ones destination address (FF:FF:FF:FF:FF:FF). A VLAN defines precisely which ports constitute a given broadcast domain — members of VLAN 10 receive VLAN 10 broadcasts, and those frames never appear on ports in other VLANs.

Each VLAN is, by definition, its own broadcast domain. When a switch creates a VLAN, it partitions the physical switch fabric so that a broadcast arriving on a port of VLAN 10 is flooded only to the other ports that belong to VLAN 10. A switch in a 100-port network with five VLANs of 20 ports each has five separate broadcast domains of 20 ports.

This equivalence has deep design consequences. The size of a VLAN sets an upper bound on broadcast and multicast traffic and on the number of hosts contending in one failure domain. Administrators size VLANs based on acceptable broadcast overhead, which is why network design guidance recommends caps on hosts per VLAN rather than simply connecting everything together.

## Q3: What is the relationship between a VLAN and an IP subnet?

**A:** A VLAN is a Layer 2 construct, while a subnet is a Layer 3 construct. A VLAN provides broadcast domain isolation, and an IP subnet provides logical addressing. Best practice is a one-to-one mapping: one VLAN equals one subnet. Each VLAN has one default gateway VLAN interface (SVI) that routers use to route traffic into and out of that network segment.

The mapping matters because ARP and other Layer 2 resolution only works within a VLAN. Two hosts in the same subnet but in different VLANs cannot contact each other directly — each must reach the gateway, which is reachable. Conversely, two hosts in the same VLAN but different subnets cannot communicate without misconfiguration, since IP addressing will not match the Layer 2 domain.

One VLAN per subnet keeps troubleshooting simple and aligns with DHCP, which is usually scoped per subnet. Configuring multiple subnets inside one VLAN is permitted (superscopes, secondary addresses) but considered an anti-pattern because it muddies broadcast domain boundaries and routing behavior. The senior interviewer expects you to articulate this mapping cleanly and justify it in design.

## Q4: What is the range of VLAN IDs and which values are reserved?

**A:** The 802.1Q VLAN ID field is 12 bits, giving a range of 0 to 4095. VLAN IDs 0 and 4095 are reserved and cannot be used for user traffic. VLAN 0 is used internally for priority-tagged frames (PCP set, VID 0), and VLAN 4095 is reserved for implementation-specific use. The usable range for enterprise VLANs is 1 through 4094.

VLAN 1 is the default VLAN — every switch port is a member of VLAN 1 until reconfigured, and the default management interface lives there. VLAN 1 cannot be deleted on most platforms, and the 802.1Q trunk native VLAN is commonly VLAN 1 by default. Cisco normal-range VLANs (1-1005) are supported everywhere, while extended-range VLANs (1006-4094) historically required specific VTP modes and are stored differently.

Several vendors carve out reserved ranges. On Cisco switches, VLANs 1002-1005 are reserved for legacy token ring and FDDI support. On some platforms VLAN 4094 is used for control plane or internal use. The interviewer will check that you understand the 4094 usable ceiling, the privileged/security role of VLAN 1, and why organizations frequently avoid VLAN 1 for user traffic altogether.

## Q5: What is an access port and what are its characteristics?

**A:** An access port is a switch port assigned to exactly one VLAN and designed to carry untagged traffic for a single end station or a small set of end stations. Access ports are used on connections to PCs, printers, IP phones, cameras, and other hosts. The port simply forwards frames to the host without VLAN tags, and the host is unaware it belongs to a particular VLAN.

The assigned VLAN is called the access VLAN. All frames received on the access port are implicitly associated with that VLAN, and all frames delivered to the host are untagged. When frame tagging matters, some implementations allow a voice VLAN on access ports for phone traffic while the access VLAN carries the desktop traffic — this is the classic dual-VLAN access uplink design.

Access ports have important trust properties. By default they do not negotiate trunking on most modern configurations (with DTP it was a historical risk), and they are the natural boundary for features like port security, DHCP snooping untrusted state, and Dynamic ARP Inspection. An access port should never accept 802.1Q-tagged frames unless it is explicitly a trunk, otherwise VLAN hopping is possible.

## Q6: What is a trunk port and how does it differ from an access port?

**A:** A trunk port is a switch port that carries traffic for multiple VLANs simultaneously, typically connecting two switches, a switch to a router, or a switch to a host that must receive multiple VLANs. Trunk ports add an 802.1Q tag to each frame to identify which VLAN it belongs to, so the receiving device can correctly place the frame in the intended broadcast domain.

The operational difference from an access port is fundamental: the access port assumes one VLAN and strips/avoids tags, while the trunk port multiplexes many VLANs and relies on tags. A trunk carries untagged frames for exactly one VLAN — the native VLAN — and tagged frames for every other allowed VLAN. The allowed VLAN list on the trunk is an explicit filter of what the trunk may carry.

Trunk ports are high-risk surfaces in layer 2 security. Because they can carry every VLAN, an attacker who converts an access port into a trunk (via DTP or manual misconfiguration) gains membership in all VLANs. Trunk hardening — disabling DTP, restricting allowed VLANs, and changing the native VLAN — is mandatory best practice, and the senior interviewer will probe whether you treat trunks as security boundaries.

## Q7: What is 802.1Q tagging?

**A:** 802.1Q is the IEEE standard for VLAN tagging on Ethernet. It inserts a 4-byte tag within the Ethernet frame, immediately after the source MAC address and before the EtherType/Length field, which allows up to 4094 VLAN identifiers to be carried through a trunk. The frame's FCS (frame check sequence) is recomputed because the tag changes the frame content.

Without tagging, a switch receiving frames on a physical link cannot determine which VLAN a frame belongs to. Tagging adds this VLAN membership information to the frame itself, enabling a single physical link to multiplex many VLANs. The tag is inserted on the sending side, carried across the trunk, and removed (or preserved) as the frame exits toward its destination on an access port.

Because the standard tag adds only 4 bytes, 802.1Q is interoperable between vendors and practically universal today. The older ISL encapsulation (Cisco proprietary, 30-byte header) is obsolete. The interviewer expects precision here: the tag is inserted after the source MAC, it changes the minimum frame size semantics (increasing the effective minimum data field), and it is applied to both directions, not just ingress.

## Q8: Describe the structure of the 802.1Q tag.

**A:** The 802.1Q tag is 4 bytes and is divided into two main fields. The first 2 bytes are the Tag Protocol Identifier (TPID), fixed at 0x8100, marking the frame as 802.1Q-tagged. The second 2 bytes are the Tag Control Information (TCI), which carries three sub-fields: Priority Code Point (PCP), Drop Eligible Indicator (DEI), and VLAN Identifier (VID).

The PCP is 3 bits (0-7), encoding IEEE 802.1p class-of-service priority that can be mapped to egress queues or DSCP values (.1p affects QoS). The DEI is 1 bit, historically the Canonical Format Indicator (CFI), now signaling drop eligibility under congestion. The VID is 12 bits (0-4095), with 0 and 4095 reserved, giving 4094 usable VLANs.

Understanding the layout matters for both troubleshooting and design. When you see a 0x8100 tag in a capture you are looking at a trunk frame; a 0x88a8 tag indicates QinQ (802.1ad) stacking, and 0x9100 is an older stacking attempt. The tag placement, after the source MAC, and the PCP/DEI/VID bit layout are exactly the facts a senior candidate must have cold.

## Q9: What is the native VLAN on a trunk?

**A:** The native VLAN is the single VLAN on a trunk port whose frames are carried untagged. All other VLANs on the trunk are explicitly tagged with 802.1Q. The native VLAN concept exists because 802.1Q must interoperate with devices that do not understand tags — before framing, a trunk frequently carried VLAN 1 traffic untagged so that simple platforms could still communicate.

When a trunk sends a frame belonging to the native VLAN, it omits the tag; when it receives an untagged frame on the trunk, it attributes that frame to the native VLAN. Both ends must agree on the native VLAN for the mapping to be consistent. A mismatch breaks traffic silently for that VLAN — the receiving switch may drop the frames or place them in the wrong VLAN, which is a classic VLAN-troubleshooting hunt.

Native VLAN misuse is a well-known security issue. Defenses include changing the native VLAN away from VLAN 1, pruning VLAN 1 from trunks, and explicitly tagging the native VLAN (non-default) so no untagged data traverses the trunk at all. Because an attacker can double-tag frames onto the native VLAN (the VLAN hopping double-tagging attack), native VLAN hardening is a standard requirement in security reviews.

## Q10: Why is VLAN 1 a security concern and what is the default VLAN?

**A:** VLAN 1 is the default VLAN on virtually all enterprise switches. Every port belongs to VLAN 1 until assigned otherwise, and the management interface (in-band management) is typically reachable through VLAN 1. VLAN 1 is also the default native VLAN for 802.1Q trunks, meaning untagged traffic on trunks maps to VLAN 1.

Using VLAN 1 for user traffic is discouraged because every attacker gaining Layer 2 membership in VLAN 1 can reach the management plane and any other devices still sitting in the default VLAN. VLAN 1 also cannot be deleted on most platforms, so if it carries traffic, it will always carry traffic. Redundant paths and misconfigured new ports also frequently land in VLAN 1 unintentionally.

The secure design pattern is to assign user traffic to dedicated non-default VLANs, move management to a dedicated VLAN (typically a high number), change the native VLAN to an unused ID, prune VLAN 1 from trunked links, and disable unused ports (placing them in a dead or quarantine VLAN with shutdown). This removes the "default assumption" that makes VLAN 1 a common highway for lateral movement.

## Q11: How are VLANs assigned to switch ports?

**A:** VLAN membership on a port is configured by type. A port in access mode is assigned to one access VLAN explicitly (`switchport access vlan`). A port in trunk mode carries a list of allowed VLANs and one native VLAN. Membership can also be dynamic through protocols like VMPS (legacy), 802.1X identity-based assignment, or automation tools that push port profiles with associated VLANs.

Static assignment is the overwhelmingly common method in production — an administrator or automation system configures the exact VLAN for each access port, and the configuration overrides the default of VLAN 1. Dynamic assignment via 802.1X allows the VLAN to follow the user or device: the authenticator readies a port, and after successful authentication the RADIUS server returns an authorized VLAN for that session.

Membership decisions cascade into behavior: QoS policies, security features (port security, DHCP snooping state), and access list policies are all scoped per VLAN. A senior engineer treats port-to-VLAN assignment as identity and policy data, not just connectivity — which is why modern fabrics automate VLAN assignment from source-of-truth inventories rather than leaving it as ad-hoc manual configuration.

## Q12: What is the MAC address table on a switch and how is it built?

**A:** The MAC address table (also called the CAM table or forwarding database) associates MAC addresses with ingress ports (and VLANs). When a frame arrives, the switch inspects the source MAC address and records the mapping: source MAC learned on that port, in that VLAN. The table is used for subsequent forwarding decisions — when a switch needs to send a frame, it looks up the destination MAC to find the egress port.

Learning is content-addressable: the switch stores the entry indexed by MAC and VLAN, and it recomputes on every frame. If a MAC address moves to a different port, the switch typically updates the binding. Entries age out after a number of seconds (CAM aging, commonly 120-300 seconds) to prevent stale bindings from misdirecting traffic when devices are moved or replaced.

A switch cannot build a unicast entry for a MAC it has never seen as a source, which is why expected return traffic is needed for symmetric learning. If the destination MAC is unknown, the switch floods the frame to all ports in the VLAN. For a senior candidate the key is that the MAC table is not just a lookup — it defines what can be forwarded without flooding, and its integrity is the foundation of Layer 2 forwarding correctness.

## Q13: What is flooding and when does a switch flood a frame?

**A:** Flooding is the process of sending a frame out every port in the destination's VLAN (except the ingress port). A switch floods for three main reasons: the destination MAC is not in the MAC address table (unknown unicast), the destination MAC is the broadcast address, or the destination is a multicast address without an optimized forwarding path (for example, no IGMP snooping entry).

The purpose of flooding is reachability: if the switch does not know where the destination lives, it must assume every member of the VLAN is a candidate. Unicast flooding is a temporary and inefficient state that relies on the destination eventually responding — after which the switch learns the return path and stops flooding. Broadcast floods are inherent to the broadcast domain, and multicast floods happen when the switch lacks membership information.

Flooding is a red flag subject in troubleshooting. Excessive unknown-unicast flooding can indicate a noisy or asymmetric traffic pattern, a CAM table full of spoofed entries (MAC flooding attack), or a network with many short-lived connections. Storm control exists precisely to bound flooding rates. A designer bounds VLAN size specifically so that flooding stays cheap and controlled.

## Q14: What is the purpose of inter-VLAN routing?

**A:** Inter-VLAN routing forwards traffic between different VLANs, which are isolated Layer 2 broadcast domains by definition. Devices in separate VLANs cannot communicate directly at Layer 2; a Layer 3 device must route between them. Inter-VLAN routing converts the segmentation created by VLANs into a controlled policy boundary where ACLs, QoS, and inspection can be applied.

The classic implements are three: the router-on-a-stick (a single trunk-linked router), SVIs on a multilayer switch (a virtual interface per VLAN on the switch itself), and routed ports (each L3 switchport is a /30 or /31-facing interface). SVI-based routing on a Layer 3 switch is the standard enterprise answer because it routes in hardware at the switch's forwarding rate.

Inter-VLAN routing is where segmentation becomes security. If no routing exists between VLANs, the VLANs are completely airtight — but users then cannot reach servers. The design questions are which VLANs need to talk, through what policy (ACL, firewall), and where the boundary should sit. The senior engineer routes between VLANs (often L3 everywhere) and reserves L2 isolation for the rare cases that need true bridging.

## Q15: What does it mean to "create a VLAN" on a switch and what state does it have?

**A:** Creating a VLAN on a switch allocates an identifier and its associated attributes (name, type, MTU, state) in the switch's VLAN database. Until then, the VLAN does not exist in the forwarding plane. On most platforms the VLAN is "active" only if it has at least one port assigned to it; an active VLAN with no ports still exists but cannot carry traffic.

A VLAN is per-switch state, which is a critical load-bearing fact. Two switches connected by a trunk do not automatically share VLAN knowledge — each switch has its own VLAN database. Protocols like VTP and GVRP were invented to propagate VLAN definitions across switches, and their failure modes (revision number takeovers) are exactly why modern best practice is to define VLANs declaratively and consistently on every switch rather than relying on propagation.

The distinction between "VLAN exists" and "VLAN carries traffic" matters in troubleshooting: a VLAN listed as active in the database but with no trunk allowed on the path explains mysterious connectivity failures. A senior candidate frames VLAN creation not as a single command but as the synchronization of state across every switch the VLAN must span.

## Q16: What is the difference between tagged and untagged frames on a trunk?

**A:** Untagged frames have no VLAN identifier in the header — the receiving switch must infer the VLAN. On an access port that inference is simply the port's assigned access VLAN. On a trunk port, untagged frames are attributed to the native VLAN. Tagged frames carry the 4-byte 802.1Q tag and the switch uses the VID field directly.

Every frame belongs to exactly one VLAN; tagging only makes that membership explicit on the wire. A switch strips the tag before forwarding to an access port (the end device sees plain Ethernet), and it adds or preserves the tag when forwarding across a trunk. The tag travels only within the switched infrastructure that understands it.

The operational consequence is that hosts on access ports never emit or receive tags, so they cannot choose their own VLAN — the switch imposes it. On trunks, both ends must agree on which VLANs are tagged versus untagged (the native VLAN specifically), because a disagreement silently misattributes frames. A senior engineer always verifies native VLAN symmetry and permitted VLAN lists when diagnosing inter-switch issues.

## Q17: What is a Switch Virtual Interface (SVI)?

**A:** An SVI (Switch Virtual Interface) is a logical Layer 3 interface that represents an entire VLAN on a multilayer switch. It has an IP address and acts as the default gateway for hosts in that VLAN. One SVI per VLAN is the standard pattern: the SVI is the routing endpoint that places the VLAN into the switch's IP routing table.

Traffic destined for other VLANs is forwarded at Layer 2 to the switch's fabric, then routed through the SVI. Because the SVI is virtual, its forwarding runs in hardware on modern ASICs, giving near line-rate inter-VLAN routing with no dedicated router. SVIs can host ACLs, HSRP/VRRP (first-hop redundancy), and DHCP relay — they are the center of gravity for per-VLAN policy.

Key design nuance: on many platforms an SVI is "operationally up" only when the VLAN has at least one active port. A common misconfig is a SVI that never answers pings because the VLAN has no alive access ports or the trunk carrying it is down. This up-down coupling is a classic senior-level troubleshooting trap and worth stating explicitly.

## Q18: What is the difference between a hub and a switch?

**A:** A hub is a physical-layer repeater: every frame received on any port is retransmitted out every other port. All connected devices share one collision domain and one broadcast domain. Only one device can transmit at a time (half-duplex), and throughput is divided among all stations. Hubs repeated the electrical signal without any forwarding intelligence.

A switch is a link-layer bridge that learns MAC addresses and forwards each frame only to the destination port (or floods when the destination is unknown). Every port of a modern switch is its own collision domain, full-duplex, so simultaneous device pairs can communicate independently, and total throughput scales with the ports rather than being shared.

The practical distinction is capacity and contention. Hubs could not scale and are obsolete; switches give each device dedicated bandwidth and dramatically reduce collisions. The interview value here is not the obvious answer but the reasoning: the switch's forwarding decision (learn, flood, forward, filter) is the fundamental operation that makes switched Ethernet work, and hubs had no such decision at all.

## Q19: Walk through how a switch forwards a frame from ingress to egress.

**A:** A frame arrives on an ingress port. The switch first validates basic frame integrity and determines the VLAN: access ports assign the port's access VLAN, trunk ports read the tag (or use the native VLAN if untagged). The switch then performs a MAC learning step — recording the source MAC to the ingress port in that VLAN — and a forwarding decision for the destination.

The forwarding decision is a content-addressable lookup against the MAC address table using the destination MAC and VLAN. Three outcomes are possible: if a matching entry exists and points to another port, the switch forwards only to that port; if the entry is absent, the switch floods to all ports in the VLAN except the ingress; if the entry resolves to the ingress port itself, the switch filters/discards (the source and destination are on the same port). 

Before egress, features are applied — QoS classification/marking, port security, storm control, ACLs — and on trunk egress the frame may gain a tag, while access egress removes any tag. The order of these operations (learn before forward, filtering by VLAN, features at ingress and egress) is exactly what a senior candidate should be able to articulate in one breath, since every switch implements this same core pipeline.

## Q20: What are CAM and TCAM and why does a switch need them?

**A:** CAM (Content-Addressable Memory) is memory addressed by content rather than by address: you present the lookup key (say, a MAC address) and the memory returns the associated data (the port) in one access, in constant time regardless of table size. For MAC learning, switches index the MAC table in CAM so that millions of lookups per second are feasible.

TCAM (Ternary Content-Addressable Memory) extends CAM by allowing three states per bit: 0, 1, or don't-care (mask). TCAM is used for pattern-based lookups — access lists, QoS classification, and longest-prefix-match routing — where rules must be matched against packet fields with wildcards. A routing entry like 10.0.0.0/8 is stored as a prefix with the low 24 bits masked.

The distinction is load-bearing: MAC forwarding is an exact match (CAM), while ACLs, flow matching, and route lookups are ternary matches (TCAM). TCAM is a fixed, expensive, partitioned resource — a senior engineer budgets TCAM between routes, ACLs, and features, and understands why hardware capacity limits the scalability of policy-heavy designs. CAM/TCAM exhaustion is a real failure mode, not a theoretical one.

## Q21: How does a switch treat broadcast frames and what can limit them?

**A:** A broadcast frame has a destination of FF:FF:FF:FF:FF:FF. Because every host in the broadcast domain is a valid recipient, the switch floods broadcast frames out every port in the source VLAN except the ingress port. This is by design — broadcast is how hosts discover each other (ARP), announce services, and run legacy protocols such as NetBIOS.

The cost is proportional to VLAN size and broadcast rate. Each broadcast consumes radio-like airtime on every switch port, and every connected host must at least partially process it. Common broadcast sources include ARP, DHCP, mDNS, NetBIOS, and address scans. Excessive broadcast causes noticeable CPU load on hosts and can approach link saturation.

Controls include VLAN segmentation (smaller broadcast domains), storm control to rate-limit broadcast, and protocol optimization (ARP suppression in VXLAN/EVPN fabrics removes the broadcast dependency across the overlay). Broadcast domains being equivalent to VLANs is why VLAN planning is fundamentally a broadcast domain sizing exercise — a fact the interviewer expects you to connect to your answers on broadcast behavior.

## Q22: What problem does Spanning Tree Protocol solve and how does it work at a high level?

**A:** Spanning Tree Protocol (STP, IEEE 802.1D) prevents Layer 2 loops. Switched networks with redundant links are essential for availability, but without loop prevention, a broadcast frame could circulate forever between switches, multiplying into a broadcast storm. A loop in a fully connected switched network collapses every device on it in seconds.

STP resolves this by electing a root bridge and computing a tree from it. Each switch blocks the one port that would create a cycle, leaving exactly one active path to the root per segment. Blocked ports still listen to BPDUs, so the topology can be recomputed if a link fails. The result is a loop-free forwarding tree that can include every device while guaranteeing a single active path.

The catch is convergence time and state changes. Classic STP needs 30-50 seconds to bring a port to forwarding on link up, and roughly 30 seconds on topology change. RSTP (802.1w) collapses this to a few seconds or less. A senior candidate must understand not just what STP does but its cost — slow failover, blocked-port waste, and the reasons modern fabrics avoid it entirely where possible.

## Q23: What is the difference between a collision domain and a broadcast domain?

**A:** A collision domain is a set of devices that can contend for the same shared transmission medium, where simultaneous transmission causes a collision. On a hub, all ports form one collision domain (half-duplex). On a switch, each port is its own full-duplex collision domain, and collisions at the data-link layer effectively do not happen.

A broadcast domain is the set of devices that receive each other's broadcast frames. Switches forward broadcasts by VLAN, making each VLAN a broadcast domain. Segmentation of one does not imply segmentation of the other: you can have 100 full-duplex switches (100 collision domains) all in one VLAN (one broadcast domain).

This distinction cleanly separates the hub-era problem (collisions — solved by switching and full duplex) from the modern problem (broadcast — solved by VLANs and overlays). The two are frequently conflated in interviews, and a strong answer quantifies: hubs make both domains large, switches shrink collision domains to one per port but leave broadcast domain control entirely to VLAN/fabric design.

## Q24: What is the difference between Layer 2 and Layer 3 switching?

**A:** Layer 2 switching inspects MAC addresses and forwards frames within a VLAN at the data-link layer. It learns MAC-to-port bindings, floods unknowns, and never looks at IP. Layer 3 switching adds routing: it decapsulates packets, performs an IP longest-prefix-match lookup, decapsulates/encapsulates frames, and forwards at wire speed using hardware ASICs.

The word "switch" masks real differences. A pure L2 device is a high-speed bridge; an L3 switch is effectively a router that happens to use switch hardware and typically has SVIs (per-VLAN interfaces) rather than physical interface routing. Modern enterprise access switches route locally with SVIs, then hand to a collapsed-core L3 switch — a "switch at the edge, router at the core" architecture.

The practical question is where you put the L3 boundary. Full L3 at the access (routed access) shrinks failure domains and removes broadcast dependency but increases routing complexity; L2 at the access with L3 at the distribution/core is the traditional campus model. Explaining the functional difference is basic; explaining the topology and failure-domain consequences is the senior part.

## Q25: What is MAC address aging and why is the aging timer important?

**A:** MAC address aging is the process by which a switch removes entries from its MAC address table after no traffic has refreshed them for a configured interval (the aging time, typically 120-300 seconds). Each incoming frame with the MAC as source refreshes the timer. When the timer expires, the entry is removed and the MAC is treated as unknown again, causing flooding until it is re-learned.

Aging exists so that the table reflects reality. Devices move ports, disconnects happen silently, and NICs get replaced — without aging, the table would keep stale bindings forever, blackholing or misdirecting traffic. The trade-off is between accuracy and efficiency: too-short aging causes constant flooding of active flows; too-long aging delays re-convergence when a device actually moves.

Aging interacts with other systems: de-aging on port-down events clears bindings for down links, and on topology change (TCN) many switches flush the table or reduce the aging timer to minutes to re-learn quickly. In storage and HPC environments, very short aging can cause persistent microdroplets. A senior engineer tunes aging per network type and understands it as part of the switch's convergence machinery, not a static setting.

## Q26: How does the 802.1Q tag affect frame size and MTU planning?

**A:** The 802.1Q tag adds 4 bytes to every tagged frame. The MAC header (14 bytes) plus the tag (4 bytes) plus the payload (up to 1500 bytes) plus the FCS (4 bytes) yields a maximum frame size of 1522 bytes for tagged frames. Any device on a trunk must accept frames at least this large, or tagged frames with maximum payloads will be dropped as too big.

The Ethernet payload is still nominally 1500 bytes; the tag lives in the header extension, not the payload. This is why most switchports and NICs handle 1522-byte frames natively, and why operators who want to carry maximum-payload tagged traffic set MTU ≥ 1522 on trunks. Jumbo-frame environments raise effective MTU accordingly (1500 payload becomes up to 9216/9000 and the tag adds on top).

MTU planning must be consistent end to end. If one switch in a trunk path has a smaller MTU, maximum-size tagged frames fail silently at that point — a classic source of "large files transfer fine, but some flows fail" symptoms. Aggregation switches carrying many VLANs should have matching MTU/(tag-aware) settings across all trunk interfaces, and overlays (VXLAN) add their own headers on top, compounding the requirement.

## Q27: What happens when the native VLAN mismatches on the two ends of a trunk?

**A:** Native VLAN mismatch is the classic inter-switch mystery and it has two distinct symptoms. First, VLAN-1 (or whatever VLAN the trunk uses natively) frames travel untagged and arrive at the peer, which attributes them to its own native VLAN. If the two native VLANs differ, untagged traffic intended for one VLAN is placed into a different VLAN on the peer — silently breaking that VLAN's traffic or leaking it.

Second, 802.1Q BPDUs for PVST/RPVST+ are sent untagged on the native VLAN. When native VLANs differ, switches can misinterpret each other's BPDUs, potentially computing an incorrect spanning-tree topology, blocking unexpected ports, or causing loops — the mismatch can trigger loops, not just unicast misdirection.

Troubleshooting sequence: you see inter-VLAN connectivity broken on one VLAN while others work; `show interface trunk` reveals different native VLANs; the fix is to align native VLANs on both ends. Some designs set an explicit "native VLAN" heavily used (QinQ/native tagging) and some shift native handling away from default VLAN 1 for security, but both ends of every trunk must match — a senior answer connects this to both data- and control-plane failure modes.

## Q28: What are the three principal methods of inter-VLAN routing?

**A:** The first is router-on-a-stick: a single router interface becomes a trunk, and multiple subinterfaces (one per VLAN) carry tagged traffic. Traffic must traverse the link twice per conversation (in and out), bottlenecking on one link, and the router's CPU performs routing — simple, cheap, but non-scalable and generally obsolete.

The second is SVI-based routing on a multilayer switch: each VLAN gets a virtual interface with an IP address, and the switch's ASIC routes between VLANs in hardware at line rate. Management is simple, latency is minimal, and this is the standard enterprise pattern for access and distribution layers.

The third is routed ports: physical switchports (or /30 links to routers/firewalls) where each interface is an independent L3 interface with its own subnet, no VLAN concept involved. Routed ports are the building block for routed access designs and spine-leaf fabrics. The senior nuance: SVI vs routed ports is a model of the L3 boundary — L3-in-the-switch (SVI) versus L3-adjacency-per-interface — and the choice determines failover behavior, broadcast domain size, and where policy can live.

## Q29: What is a router-on-a-stick and why is it considered legacy?

**A:** Router-on-a-stick interconnects VLANs by adding one trunk-protocol subinterface per VLAN to a single router physical interface. Each subinterface terminates a different VLAN, and the router's CPU performs IP routing between them. It is the minimal viable inter-VLAN routing: one link, one router, many VLANs.

The limitations become obvious under load. Every routed packet enters and exits the same single link, halving effective bandwidth (in and out share the wire). Routing is software-based CPU work, sub-line-rate, and the single physical port and single router are a shared collision point and failure domain. With tactic many VLANs, subinterface configuration also grows linearly.

It remains useful only in labs, tiny networks, or transitional designs where a Layer 3 switch is unavailable. Any interviewer asking this wants you to articulate why the industry moved to SVI-based switching: hardware forwarding, per-VLAN policy, no CPU bottleneck, and no single-link constraint. A senior candidate dismisses router-on-a-stick for production but can still explain exactly its failure modes and why it persists in small deployments.

## Q30: How does SVI-based inter-VLAN routing work and when should you use it?

**A:** In SVI-based routing, each VLAN is represented by one virtual Layer 3 interface with an IP address — the SVI. Hosts in the VLAN use that SVI address as their default gateway. When a host sends a packet to a different VLAN, the frame travels at Layer 2 to the switch's ASIC, which routes on the IP destination and decides the egress SVI, then re-encapsulates onto the destination VLAN.

Routing happens in hardware. The ASIC performs a route lookup (typically TCAM-based longest-prefix-match), decrements TTL, swaps the source/destination MAC to the egress SVI's addresses, and forwards the frame on the destination VLAN's ports. Because everything is inside the switch, latency is microseconds and throughput is at the switch's forwarding rate.

SVIs are the right choice for the campus distribution/core and the DC access: you get line-rate routing, per-VLAN ACLs, HSRP/VRRP redundancy, DHCP relay, and centralized management, all without external routers per VLAN. The design question is L3 placement — SVIs at the access (routed access) shrink the broadcast/failure domain dramatically, at the cost of more routing peers — and that trade-off is exactly what the interviewer wants to hear.

## Q31: What is the difference between an SVI and a routed port?

**A:** An SVI is a logical interface that addresses an entire VLAN — all hosts in that VLAN share the SVI as their gateway, and the SVI is the L3 endpoint for the VLAN's traffic. A routed port is a physical switchport with no Layer 2 (no VLAN and no switching provided); it behaves like a router's interface with its own IP in its own subnet, typically /30 or /31, carrying only that point-to-point link.

Functionally, SVIs route between whole broadcast domains; routed ports route between single links. The design consequence: SVIs preserve large L2 broadcast domains (the VLAN radius), while routed ports force L3 into the access layer — every switch-to-switch or switch-to-server link is its own tiny layer-3 segment. Routed access designs fundamentally reduce L2 failure domains.

Operationally, SVIs are where you terminate DHCP relay, first-hop redundancy, per-VLAN ACLs, and VLAN-scoped features; routed ports are where you build L3 adjacencies (OSPF/BGP) and implement policies per physical link. Modern spine-leaf fabrics run routed ports everywhere and keep VLAN use minimal, while classic campus designs run SVIs at the core. The senior answer ties the choice to failure-domain size and policy granularity, not just "which is newer."

## Q32: Compare 802.1Q and ISL trunking.

**A:** 802.1Q is the IEEE standard (802.1Q / 802.1ad) that inserts a 4-byte TPID+TCI tag into the Ethernet frame (0x8100, 3-bit PCP, 1-bit DEI, 12-bit VID). It carries 4094 usable VLANs, is vendor-neutral and must interoperate with any 802.1Q device, and is the only trunk protocol in modern networks.

ISL (Inter-Switch Link) was Cisco's proprietary trunk encapsulation: a 30-byte header wraps the entire frame (26-byte ISL header plus 4-byte CRC trailer), and the outer header carries the VLAN ID (10 bits). ISL encapsulated the full frame rather than tagging it, so it could never pass through non-Cisco devices and added more overhead. ISL supported effectively 1000 usable VLANs.

ISL is dead — no switch in the last 20 years ships it. The interviewer's real purpose is to check that you understand the distinction between tagging (in-band, standard, derivable from any capture via 0x8100) and encapsulation (out-of-band wrapper, proprietary). Answers that say "ISL wraps, 802.1Q tags" and explain the VID/PCP semantics and why 802.1Q won are what counts.

## Q33: What is ISL encapsulation and why did it disappear?

**A:** ISL wraps frames in an additional 30-byte header: 26 bytes that include a 15-bit frame type, a 10-bit VLAN ID, and canonicity/reserved bits, plus a 4-byte trailing CRC specifically for the ISL envelope. Because it encapsulated the entire original frame, ISL carried the full frame unmodified — VLAN information was in an outer envelope rather than being inserted into the Ethernet header.

That design had consequences: ISL was Cisco-only, added substantial overhead (30 bytes vs 4), and the outer wrapping meant non-Cisco and many consumer/embedded NICs could not parse or forward it. Interoperability disputes and later IEEE standardization made 802.1Q the path forward, and Cisco dropped ISL support entirely from modern switch lines.

The disappearance was monotonic: as 802.1Q became universal, supporting the extra ISL machinery — with its separate CRC and encapsulation logic — became dead weight. For interviews, the point is that you understand encapsulation-versus-tagging, the vendor-interop argument that settled the war, and that "ISL is gone" is not a historical footnote but the reason trunk configurations today universally mean 802.1Q.

## Q34: What is DTP (Dynamic Trunking Protocol) and what are its modes?

**A:** DTP (Dynamic Trunking Protocol) is a Cisco Layer 2 protocol that negotiates trunk status between switch ports on a link. It lets two ends automatically decide to form a trunk. The port modes are Access (make it an access port), Trunk (make it a trunk), Dynamic Auto (agree to trunk only if the peer asks), and Dynamic Desirable (actively try to form a trunk), plus On/Off variants in some contexts.

The fundamental problem: DTP enabled by default (on legacy hardware, dynamic auto/desirable) lets a connected device turn a switchport into a trunk without authorization. An attacker plugging into a dynamic port can negotiate trunking, then tag frames for any VLAN and access layer 2 segments they should not see — the switch-spoofing variant of VLAN hopping.

Best practice is well-known: set all end-user ports to access mode with trunking explicitly disabled (`switchport nonegotiate` where available, or relying on access mode never sending DTP), disable unused ports, and restrict DTP to actual infrastructure links where truly needed. The interviewer checks whether you treat DTP as a configuration feature or a security exposure — a senior answer treats it as the latter by default.

## Q35: What is VTP and how does it attempt to simplify VLAN management?

**A:** VTP (VLAN Trunking Protocol) is a Cisco Layer 2 messaging protocol that distributes VLAN definitions (VLAN ID, name, type) from one switch to others across trunk links. A single VTP server switch can define a VLAN once, and the protocol propagates that VLAN to all VTP clients, eliminating the need to create the same VLAN manually on every switch in the domain.

Messages are multicast between servers and clients; each switch maintains a domain name, configuration revision number, and a VLAN database. The revision number is the master key: a higher-revision database overwrites the receiver's database regardless of direction, which is exactly what makes VTP dangerous. Any switch inserted with a higher revision wipes the VLAN database of the entire VTP domain.

VTP's fine print: VTP client switches cannot create VLANs locally (they only accept server definitions), VTP transparent switches relay but do not apply updates, and VTP pruning can remove VLANs that are unused over trunks. Because of the revision-number wipe risk, virtually all modern Cisco guidance is VTP transparent or off for data-carrying VLANs, and VLAN creation is done declaratively per switch or via automation rather than via the protocol.

## Q36: What are the VTP modes — server, client, and transparent — and how do they behave?

**A:** VTP server is the default and the manager of the VLAN database: servers create, delete, and rename VLANs, send VTP advertisements, and propagate their revision number. VTP clients cannot create VLANs locally; they accept and apply whatever the domain's highest-revision server says, and forward VTP messages. VTP transparent switches maintain their own VLAN database, do not adopt messages, but forward VTP advertisements.

The practical difference is who owns VLAN definitions. Server/clients synchronize to the highest revision number; transparent ignores synchronization entirely. Because "client" switches cannot locally create VLANs, many operators found client mode paralyzing — you could not quickly define a VLAN on one access switch — which made transparent mode the pragmatic favorite.

The security and failure reality: any device that is a VTP server (or client in some implementations) with a higher revision number can overwrite the VLAN database domain-wide, and that wipe propagates across trunk links. Transparent mode prevents this by design because the switch ignores updates. This is why the modern best-practice answer is to run VTP off or transparent and manage VLANs with automation, not protocol propagation.

## Q37: What is the VTP configuration revision number and why is it dangerous?

**A:** The VTP configuration revision number is a 32-bit counter in every VTP advertisement. Each modification of the VLAN database increments it. Switches compare received revision numbers against their own and apply the database with the higher number — the receiving switch adopts the incoming VLAN definitions if the number is greater, regardless of which switch is "more correct."

The danger: a switch that has been configured incorrectly, carries stale VLAN definitions, or is inserted into a VTP domain with a high revision will propagate its whole database as authoritative. Classic incidents: an operator configures a new switch in isolation, its revision climbs, it joins the domain, and the domain's VLAN definitions are silently replaced — old VLANs vanish and ports lose their valid assignments mid-operation.

Mitigations: reset the revision number before adding switches (on Cisco, changing the VTP domain or using a configuration that zeroes it), run VTP transparent/off, or accept that the protocol is a security landmine. The interviewer wants you to explain why revision number, not server-client direction, is the true authority — and why that makes VTP unauditable for modern production use.

## Q38: What is VTP pruning and what behavior does VLAN pruning on trunks achieve?

**A:** VTP pruning stops VLAN traffic from being forwarded over a trunk when there are no active members of that VLAN downstream on that trunk. Instead of flooding every VLAN's frames and broadcasts over every trunk, the switch keeps trunk forwarding lists to VLANs actually needed beyond the link, saving bandwidth and reducing broadcast exposure across the fabric.

There are two flavors: VTP pruning (automatic, driven by the VTP protocol knowing VLAN membership) and manual per-VLAN trunk pruning (explicit `allowed vlan` lists). Automatic VTP pruning requires VTP v2 and configured pruning candidate sets; manual pruning is simply restricting which VLANs are permitted on a trunk. Modern practice is manual `allowed vlan` lists — deterministic, auditable, and protocol-independent.

The downside of unrestrained VLAN forwarding on trunks: every VLAN's broadcasts reach every switch and consume trunk bandwidth even when nobody downstream cares. Pruning solves that, but pruning misconfigurations can break connectivity (a pruned trunk drops traffic for a VLAN that is actually needed). The senior answer explains pruning as both traffic hygiene and an exposure-reduction control, and notes you should prune with intent, never with "all allowed" blindly.

## Q39: How does MAC address learning work on a trunk port?

**A:** MAC learning on a trunk uses the same mechanism as access ports — the switch records source MAC plus the VID field of the frame into the MAC table, but now the VLAN is the tag's value instead of the port's access VLAN. Frames arriving with tags for different VLANs update separate entries: the same physical port can hold MAC entries in many VLANs simultaneously, one per (MAC, VLAN) pair.

Because the MAC table is indexed by (MAC, VLAN), a MAC address can legitimately appear in multiple VLANs on one trunk (e.g., a router with one interface spanning several SVIs). This is why lookups and aging are per MAC-per-VLAN, and why ACLs/port security on trunks operate per VLAN as well.

Learning must respect trunk policies: frames for VLANs not in the allowed list are dropped before learning, and some features (like port security) treat the trunk as multi-VLAN containers rather than single-VLAN ports. The learning-derived behavior on trunks — a broadcast for a VLAN with no downstream entry floods only in that VLAN — is why "MAC table per VLAN" is the right mental model for a senior engineer.

## Q40: What is unknown unicast flooding and how do you contain it?

**A:** Unknown unicast flooding occurs when a switch receives a frame whose destination MAC is not in its MAC address table for that VLAN. Having no forwarding target, it floods the frame to every port in the VLAN except the ingress port. The frame reaches the intended recipient (if present), which then replies — letting the switch learn the correct port and stop flooding.

Flooding is correct and inevitable in some situations — asymmetric routing, conversations where the return path does not traverse the same switch, or broadcast-heavy protocols. It becomes a problem when it is persistent: MAC table saturation (MAC flooding attack), freshly changed or sparse traffic patterns, or misconfigured trunk/access VLAN mismatches causing the destination to be in a different VLAN than the switch believes.

Containment is architectural: smaller VLANs shrink flood domains; routed access or L3-overlay designs eliminate most unknown-unicast by making VLAN boundaries tiny; storm control bounds flood bandwidth; and MAC-table diagnosis (checking whether the destination has a binding at all) finds the root cause. The senior answer frames unknown unicast not as a bug but as an expected cost of Layer 2 transparency that you engineer around.

## Q41: What is MAC flapping and how does spanning tree interact with the MAC table?

**A:** MAC flapping is when a switch sees the same MAC address appear on different ports repeatedly (or rapidly), updating the MAC table back and forth. It is a top symptom of a Layer 2 loop: with a loop, frames are continuously re-circulated and re-learned on different ports, causing constant relearning, CPU load on the switch, and instability in the MAC table.

Spanning tree prevents MAC flapping by removing the loops, but the interactions run deeper. When STP changes topology (a blocked port becomes forwarding, or vice versa), the switch must re-learn MAC addresses because the reachable location of every MAC may have changed. This is why STP issues a Topology Change Notification (TCN) — switches either flush the MAC table or shorten the aging timer so stale entries are cleared and new ones learned promptly.

The emergency behavior matters: during reconvergence, if MAC tables age slowly and stale entries point to the old (now blocked) egress, frames get dropped or misdelivered until relearning. For a senior candidate, the key insight is that STP and MAC learning are coupled — topology change handling is really "flush and re-learn fast," and its tuning (forward delay, aging) directly sets how quickly the network trusts fresh forwarding state.

## Q42: How is the root bridge elected in classic STP?

**A:** The root is elected by lowest Bridge ID, a compound value of a 2-byte priority (default 32768, step 4096) and the 6-byte bridge MAC address. Every switch starts by claiming itself root with its own BID and exchanging BPDUs. When a switch sees a BPDU with a lower root BID, it adopts that root and propagates the information, so the lowest BID wins across the entire bridged network.

The election is a distributed lowest-value computation. Because bridge priority is the dominant field, an administrator makes a switch root deterministically by lowering its priority (e.g., 4096 for the desired root, 8192 for a backup). Ties in priority are decided by MAC — so the switch with the numerically lowest MAC wins, which is why you never rely on that and instead set priorities explicitly.

Practical consequences: default equal priorities leave root selection to MAC address, which is nearly random operationally — the root lands wherever and convergence behavior differs. A senior engineer sets primary/secondary root priorities explicitly, places root switches at the distribution/core, and monitors the STP topology to ensure the intended spanning tree is actually in force after real-world changes.

## Q43: What is a BPDU and what information does it carry?

**A:** A BPDU (Bridge Protocol Data Unit) is the control message that STP and its derivatives (RSTP, MST, PVST+) exchange between switches to compute a loop-free topology. Classic STP runs two types: Configuration BPDUs (root information and port status) and TCN BPDUs (topology change notifications).

The Configuration BPDU payload includes the sender's root bridge ID, the switch's own bridge ID, the root path cost to the root, the port ID of the transmitting port, message age (how long propagating through the network), maximum age, hello time, and forward delay. RSTP extends this with a flags field for proposal/agreement and port roles/states, and PVST+ stamps VLAN IDs so computation is per VLAN.

BPDUs are also the substrate of several defense features: BPDU Guard (shutdown a port that unexpectedly receives BPDUs), Root Guard (reject a port that would become root), and Loop Guard (block on BPDU absence). Understanding what a BPDU is and what it carries is the foundation for the entire spanning-tree interview — and it is exactly where "per-VLAN BPDUs" (PVST) vs "shared BPDUs with instance mapping" (MST) diverge.

## Q44: What are the port states and port roles in classic STP?

**A:** Classic STP port states are Disabled, Blocking, Listening, Learning, and Forwarding. Blocking ports do not forward data but receive BPDUs; Listening builds the topology (transition from block to listen to learn); Learning populates the MAC table without forwarding; Forwarding carries live traffic. On link up, the sequence is Block→Listen→Learn→Forward, taking up to 30-50 seconds total.

Port roles in 802.1D are Root port (the port with the best path to the root), Designated port (the best port for each segment, on the side that wins the path comparison), and Blocking ports (alternate/backup paths that are shut off). RSTP renames roles to Root, Designated, Alternate, and Backup, and adds discard/learning/forwarding states.

The interview-grade answer connects roles and states: the root bridge's ports are all designated; every segment has exactly one designated port (its forwarding side) and the root port on the far side; everything else blocks. That single-tree property is what guarantees loop freedom, and the 30-second learning delay exists to prevent transient loops during transitions — the exact thing RSTP eliminates with its rapid transition mechanism.

## Q45: What is PortFast and when should it be enabled?

**A:** PortFast is a switchport feature that takes a port out of the STP learning cycle on link-up: it transitions the port almost immediately to forwarding instead of waiting the 30-50 seconds of Listening/Learning. PortFast is designed for access ports connected to end devices (hosts, servers, printers, IP phones), where no bridge is downstream and loop risk is effectively nil.

The absolute requirement: PortFast must only be applied to ports where no other switch exists on the other end. A PortFast port that receives a BPDU indicates a loop was just created — which is why PortFast is almost always paired with BPDUGuard (shutdown the port) and often with root guard. PortFast on a link to another switch can create a storm.

Important subtlety: PortFast also has an STP impact after initial convergence — many implementations apply a "PortFast trunk" variant on trunks going to non-STP devices like servers with link aggregation. The interviewer wants you to state the purpose (skip the 30-50s wait), the non-negotiable constraint (end device only), and the required guards — a senior answer never says "PortFast with no BPDU guard" without pushing back.

## Q46: How does Rapid Spanning Tree Protocol (RSTP) improve convergence over classic STP?

**A:** RSTP (802.1w) converges within a handful of seconds, sometimes sub-second on failure, versus STP's classic 30-50 seconds, primarily by allowing ports to transition to forwarding rapidly through a deterministic handshake. The core mechanism is Proposal/Agreement: when a link comes up, the upstream switch proposes itself as designated, the downstream agrees (after sync — blocking all non-root ports), and the edge transitions to forwarding immediately. No per-state timers stretch the transition.

RSTP also redefines port states (Discarding, Learning, Forwarding) and roles (Root, Designated, Alternate, Backup). Alternate ports hold a pre-computed backup path to the root, so when the current root path fails, the alternate takes over with minimal delay — no recomputation needed, just a role flip. Edge ports (PortFast equivalents) never participate in the handshake.

RSTP removes reliance on the 3 for these transitions, keeps backward compatibility with 802.1D by falling back on timers when receiving classic BPDUs, and folds TCN into regular BPDUs rather than separate messages. The practical result: loops are prevented structurally, failover is nearly instantaneous, and modern platforms run RSTP/PVST+/Rapid PVST as the default operational mode instead of classic STP.

## Q47: What is a topology change notification (TCN) and what does it trigger?

**A:** A TCN is generated when a port transitions to forwarding state, or when an edge/access port comes up/down — i.e., whenever the reachable set of MAC addresses may have changed. In classic STP, the switch sends a TCN BPDU to the root and the root responds with a TCN acknowledgment. In RSTP, the change is folded into the regular BPDU flags (TC bit) and broadcast to all neighbors, reaching the root faster without a request/acknowledge round trip.

The function of a TCN is not just notification: it forces the network to flush (or drastically age) MAC address tables quickly. If a device moved, stale MAC entries would otherwise keep directing frames to the wrong port for the full aging interval. Clearing/relearning on topology change makes forwarding converge with the new topology in seconds rather than minutes.

Because STP treats any access-port up/down as a topology change, flapping access ports or servers continuously trigger MAC table flushes network-wide, causing temporary flooding and inefficiency even in a stable core. That is exactly why edge ports/topology change controls exist (e.g., limiting TCN generation for edge links) — a senior answer explains the coupling and the tuning that prevents healthy networks from thrashing their MAC tables.

## Q48: What are PVST and PVST+ and how do they differ from standard STP?

**A:** PVST (Per-VLAN Spanning Tree) runs a separate spanning-tree instance per VLAN, each with its own root election and BPDUs. PVST+ extends PVST to behave well with plain 802.1Q trunks: it still holds one instance per VLAN but tags BPDUs per VLAN, fallbacks to a single shared tree on plain-802.1Q links (using the native VLAN), and interoperates with standard 802.1D switches.

The benefit of per-VLAN spanning trees is topologies tailored per VLAN: different VLANs can have different roots, different root paths, and use different uplinks. You can load-share — VLANs 10-20 on one distribution switch, 21-30 on the other — while each retains loop-free semantics, maximizing uplink utilization that a single shared tree would leave idle.

The costs are linear scaling: each additional VLAN multiplies BPDU processing, and convergence events (ports flapping) must be handled per instance. RPVST+ (Rapid PVST+) pairs per-VLAN trees with RSTP rapid convergence, and is the common Cisco default. The senior nuance: per-VLAN trees give you load balancing and per-VLAN root control, but MSTP gives you per-VLAN behavior with fewer instances at scale — and artifact to walk through when you compare them.

## Q49: What is EtherChannel and how does it interact with spanning tree?

**A:** EtherChannel (port-channel) bundles 2 to 8 (up to 16 with some platforms) physical links into one logical link with a single MAC address (the bundle's MAC). To the switches and STP, the port-channel is one logical port — one BPDU, one loop-free path, one set of STP roles. This removes the need for STP to block any of the bundle's member links, since all are part of one logical path.

Load is distributed across members via a hash of packet fields (typically source/dest MAC, IP, or ports), so the bundle's capacity can approach the sum of its members. Aggregation requires both ends configured identically (same speed/duplex/VLANs) and negotiated by LACP (IEEE standard) or PAgP (Cisco), or configured statically.

The STP interaction is the crucial design point: EtherChannel collapses multiple physical paths into one, so it removes half the reasons STP has to block. In modern fabrics, aggregation + L3 between distribution/core means STP is barely engaged on uplinks — the bundle just participates as a single port in the tree, and failover inside the bundle is transparent to STP (the link never toggles if one member drops).

## Q50: Why is a Layer 2 loop catastrophic and how does STP prevent it?

**A:** A Layer 2 loop without STP transforms broadcast and multicast frames into infinite recursive copies: a frame enters at a switch, a second copy at another, and each duplicate re-enters and re-multiplies until link saturation. The effect is a broadcast storm that consumes all available bandwidth, saturates switch CPU with MAC-table churn, and renders hosts in the looped domain unusable within seconds.

The loop is self-sustaining because of the forwarding rules: broadcasts are always flooded to every port in the VLAN, and with two paths between switches, each copy gets re-flooded again — exponential growth in copies per hop. Unicast frames also recirculate from repeated unknowns, and MAC flapping (the same MAC seen on both ports) makes the MAC table unstable, so even unicast forwarding degrades.

STP eliminates the loop structurally: it elects a root and ensures exactly one active path to it, placing every redundant port into blocking. In the presence of redundant links, only one path forwards at a time, so copies cannot circulate. The senior conclusion is that STP is not optional politeness — it is what makes redundant switched topology safe, and the moment you design without it you had better have guaranteed acyclic topology (L3 everywhere, VXLAN overlays, unidirectional links avoided; redundant bundles resolved by aggregation and MC-LAG).

## Q51: Walk through classic STP convergence using the 30-50 second timers.

**A:** When a link enabling a port starts forwarding, a classic STP port walks Blocking -> Listening -> Learning -> Forwarding. Listening lasts one forward delay (default 15s), during which the port learns the topology but does not forward. Learning lasts another forward delay (15s) for MAC learning. After those 30 seconds, the port reaches Forwarding. A failed link triggers root selection and the same per-port forward delays, typically 30-50 seconds total (max age 20s + 2 × forward delay 15s = 50s worst case).

The purpose of the delays is safety: after a topology change, stale MAC entries and incomplete port roles could cause a temporary loop if the port forwarded immediately, so STP intentionally stalls forwarding while it observes. Max age (20s) also bounds how long a switch waits before declaring a root dead and recomputing — no BPDU from the root for 20 seconds forces a new election.

Modern workloads cannot tolerate 30-50 second outages, which is exactly why RSTP collapsed this logic: proposal/agreement and pre-computed alternate ports allow milliseconds-to-seconds transitions on failure. RSTP keeps backward compatibility with classic timers when interoperating. The senior answer frames the two settings (forward delay, max age) as the loop-safety latency most deployments must consciously tune or replace.

## Q52: What are BPDU Guard, Root Guard, Loop Guard, and UDLD and when do you deploy each?

**A:** BPDU Guard shuts down (or error-disables) a port that receives a BPDU. It is the enforcement for access ports: if an access port (PortFast) sees a BPDU, someone attached a switch — BPDU Guard converts a would-be loop into an outage of just that port. Root Guard protects the root: a port with Root Guard rejects incoming superior BPDUs, so a rogue/new switch cannot force itself to become the root; the port becomes inconsistent instead of the root election being hijacked.

Loop Guard blocks a port when BPDUs cease, even if it is still up and receiving traffic. It addresses the failure where a unidirectional link lets one direction of BPDU pass and one direction break — a silent forwarding port with no STP messages can create a loop; Loop Guard stops that port from forwarding. UDLD (Unidirectional Link Detection) is the physical complement: it exchanges probes and error-disables links that work in one direction only, catching fiber/optics faults BPDU-based logic cannot see.

Deployment rules of thumb: BPDU Guard + PortFast on every access port; Root Guard on distribution/access uplinks toward the core; Loop Guard on all blocked/redundant links; UDLD aggressive on fiber trunk ports and channels. These are complementary, and a senior design statement is that the four of them are what make STP practically safe in production, not STP itself.

## Q53: How does RSTP's proposal/agreement mechanism achieve rapid convergence?

**A:** RSTP eliminates per-state timer delays for the handshake path. On a point-to-point link going to forwarding, the upstream switch sends a Proposal BPDU (proposal = "let this port be designated"). If the downstream switch's root port is the link being proposed, it answers with an Agreement only after performing sync — putting all its other ports into blocking/discarding so the proposal cannot create a loop. The proposing port goes to forwarding immediately.

Because the downstream already sent its Agreement and blocked everything non-root before agreeing, the new segment is safe the moment the port forwards — the two-step handshake guarantees no transient loop, so no forward-delay wait is needed. Edge ports transition instantly without any handshake; alternate ports flip to active instantly on failure.

The full rapid behavior: RSTP sets a flag bit for Proposal/Agreement within the 2-byte BPDU flags field (Bit 6 = agreement, Bit 1 = proposal), and compresses the state machine so root/designated roles are updated by processing BPDUs on roles, not timers. Failure of the current root path promotes the alternate port immediately — the pre-computed back-up path is the difference between RSTP's sub-second failover and STP's 30-50 seconds.

## Q54: What is MSTP and when does per-instance spanning tree pay off versus PVST+?

**A:** MSTP (802.1s / Multiple Spanning Tree Protocol) runs multiple spanning-tree instances that map any number of VLANs to few instances — typically each instance carries a set of VLANs reduced to a small number of region-wide trees. The region boundary (region name, revision number, and instance-to-VLAN mapping hashes) lets switches agree on instance membership; one Internal Spanning Tree (IST) instance provides a regional backbone plus interoperability with legacy spanning tree.

The payoff versus PVST+ is scale. PVST+ needs 4094 instances in the worst case; MSTP caps the tree count at the configured instances (often two). With hundreds or thousands of VLANs, PVST+ multiplies BPDU processing, convergence events, and configuration surface; MSTP bounds them while keeping load-balance-by-VLAN-group capabilities.

The trade-off: MSTP's mapping and region configuration is more complex, and inter-vendor behavior (803.1s base) matters — MST is standardized, PVST is Cisco-specific. Practical guidance: small/flat networks run RPVST+ (simple, well documented); large multitenant or SP fabrics run MST or abandon per-VLAN STP for VXLAN/BGP-EVPN overlays. The senior answer describes the mapping cost (region identity + VLAN-to-instance mapping must match across a region) and when that cost exceeds the benefit.

## Q55: How do you tune spanning tree timers and what are safe settings for production?

**A:** STP timers: hello time (2s default), forward delay (15s), max age (20s). As a safety constraint, 802.1D requires 2×(forward_delay − 1) ≥ max_age and max_age ≥ 2×(hello_time + 1) — the timers interlock to preserve loop-safety math. Aggressive tuning (e.g., forward delay 4s) can break the constraint and reintroduce transient-loop risk on legacy networks, so changes must respect the inequalities.

Realistically, tuning classic STP timers squeezes only the listening+learning window; it does not give rapid convergence — RSTP already gives sub-second failover. Reduce forward delay only when you are forced to interoperate with a platform that does not run RSTP. The large lever in legacy STP is the global timers on the root (BPDUs carrying root parameters propagate), and the practical lever in modern networks is ensuring RSTP is in force so timers matter only for edge/bootstrapping.

Safe settings for decayed classic STP: keep forward delay at 4-6s, max age at 12s, hello 2s — but always first confirm the network runs RSTP to avoid tuning legacy loops back into existence. The senior recommendation, honestly: do not rely on timer tuning for uplink failover; rely on RSTP/MSTP for the real trees and use timer adjustment for ring/legacy interoperability only.

## Q56: What are MAC flooding and MAC spoofing attacks and why do they matter on switches?

**A:** MAC flooding (CAM overflow) saturates the switch's MAC address table by sending a huge volume of frames each with a unique, rapidly changing source MAC. Once the table is full, the switch cannot learn legitimate entries and enters a fail-open flood-all mode for unknown destinations — the attacker's port now receives copies of frames intended for other hosts. The attack converts a targeted VLAN into a sniffing domain.

MAC spoofing targets a specific host: the attacker sends frames (or ARP) claiming a victim's MAC, causing the switch to bind that MAC to the attacker's port, rerouting the victim's inbound traffic. It is the Layer 2 cousin of IP spoofing and is often used to facilitate session hijacking or bypass destination-based filtering.

Defenses: port security (limit MACs per port, sticky learning, shutdown on violation) blocks new MACs at the port; MAC address protection restricts learning rates; and building the security stack — DHCP snooping + DAI + IP Source Guard — verifies claims against a trusted binding table rather than trusting traffic. The senior angle is that these attacks are trivially preventable at the access layer, so a switched network that allows MAC flooding is a network design failure, not a mystery.

## Q57: How does port security work and what are the violation modes?

**A:** Port security bounds how many MAC addresses a port may learn and which specific addresses may use it. The administrator configures a maximum (1 on most access ports) and optionally declares secure MAC addresses; learned MACs can be sticky (persisted across restarts). Excess addresses trigger a violation action: protect (drop excess traffic), restrict (drop and log/send trap), or shutdown (error-disable the port after a configurable recovery).

The violation mode defines the blast radius. Protect is quiet but allows the port to stay up (politely dropping extra frames); restrict reports the event; shutdown is the safe default for hostile environments — an unauthorized device kills the port, alerting operations. Sticky security is common for static inventory ports: the switch records the first MAC and enforces it henceforth.

Nuance: port security on trunk ports means per-VLAN MAC counts, and EtherChannel bundles treat member ports independently unless aggregated (some platforms support port-channel security). Port security is the first line against MAC flooding/spoofing, but it is effective only when combined with the trust model — DHCP snooping binding tables and 802.1X authentication — which distinguishes "authorized but new" from "attack" without manual MAC whitelisting.

## Q58: What is VLAN hopping and how do the two techniques differ?

**A:** VLAN hopping is escaping the VLAN assigned to a port to reach traffic/VLANs it should not access. The first technique — switch spoofing — negotiates trunking via DTP: the attacker's device responds as a switch, the access port becomes a trunk (in dynamic auto/desirable mode), and the attacker can tag frames as any VLAN.

The second technique — double tagging — sends frames carrying two 802.1Q tags. The first (outer) tag contains the attacker's VLAN (native VLAN on many trunks); the first switch strips the native tag and, on the trunk, forwards the frame tagged with the inner (victim) VLAN; the receiving switch decapsulates into the victim VLAN. The return path does not work, so it is essentially one-way in common setups, yet still exfiltrates victim-VLAN traffic.

Defenses differ per technique: disable DTP and use access mode (nonegotiate) to end switch spoofing; change the native VLAN, disable the native VLAN on trunks when equal security, and ensure only the intended untagged VLAN is permitted to end double-tagging. Double-tagging also requires the attacker to be in the native VLAN. A senior consolidated answer: VLAN hopping is configuration/hardening failure, fixable entirely at L2 without any auth machinery.

## Q59: What are private VLANs and how do they segment within a broadcast domain?

**A:** Private VLANs (PVLANs) subdivide a single broadcast domain into finer segments while keeping one subnet/gateway. Three port roles: promiscuous (talks to everyone, typically the uplink to the gateway/trunk), isolated (can only talk to promiscuous — no communication with other isolated ports), and community (can talk to promiscuous and to other community members, never to isolated or other communities).

The primary use: multi-tenant or guest networks where each subscriber/host shares the same subnet (DHCP range and gateway) but cannot reach each other directly — the provider gateway handles inter-subscriber traffic and policy instead. PVLANs replace several separate VLANs+ACLs with one VLAN and L2 enforcement.

Under the hood, the switch enforces the split with MAC-table constraint (isolated ports cannot reference each other's CAM entries), which is why PVLANs still forward Broadcast/Multicast from promiscuous to all. Caveats for deployment: PVLANs change how DHCP/ARP behave (broadcast still crosses), and features like HSRP, DHCP snooping, and protocol-based VLANs interact specially with PVLAN ports. The senior candidate describes PVLAN as "one broadcast domain, multiple enforcement domains."

## Q60: What is QinQ (802.1ad) and when is it used?

**A:** QinQ is stacked VLAN tagging (IEEE 802.1ad): the frame carries two 802.1Q tags, an outer S-VID (service VLAN) and an inner C-VID (customer VLAN). This lets a service provider multiplex thousands of customers over a single aggregated link, with each customer's VLANs preserved inside their S-VID, without merging VLAN ID spaces across customers.

Implementations: on service-provider metro-Ethernet, the S-tag identifies the customer; the switch encapsulates (pushes) on ingress and pops on egress. The setup transports customer VPN-like semantics. QinQ appends a second tag (S-tag) outside the customer's tag, and 802.1ad transports the inner frame transparently — preserving the customer's STP and tagging logic — versus the newer 802.1ah Provider Backbone Bridging (MAC-in-MAC) for very large scale.

Operational consequences: QinQ makes payload larger (same MTU math: two tags, 8 bytes, so trunk MTU must exceed 1522-1530), TTL/loop control runs only on the S-tag in many implementations, and inner traffic appears opaque to the provider. Senior use cases: DSL/FTTH provider backhauls, DCI (data center interconnect) transparency, and cloud provider multitenancy where customers run their own VLAN IDs.

## Q61: What is the typical attack against the native VLAN and how do you harden it?

**A:** The native VLAN (default VLAN 1) carries untagged traffic on 802.1Q trunks. Attack vectors: (1) the double-tagging attack rides the native VLAN because the outer tag is stripped at the first switch, leaving the inner tag to re-tag into the victim VLAN; (2) if the native VLAN is VLAN 1 and carries management or user traffic, an attacker can inject poisoned frames untagged onto any trunk and have them land in VLAN 1.

Hardening is straightforward: change the native VLAN to an unused VLAN ID on every trunk (never VLAN 1); prune/remove native VLAN from allowed lists when you do not need untagged traffic on the link; disable DTP; and where strictness reigns, tag the native VLAN (there is the option to force 802.1Q "dot1q tag native") leaving no untagged frames on the link at all.

Additionally: management VLAN should be distinct from VLAN 1 and restricted; unused ports should go to a dead/quarantine VLAN in shutdown; and CDP/LLDP on user-facing ports should be disabled to reduce information disclosure on trunks. The senior summary: native VLAN hardening is cheap, defense-in-depth against both data- and control-plane L2 attacks, and the single highest-value L2 hardening item besides disabling DTP.

## Q62: What are VTP attacks and how do you eliminate them?

**A:** VTP attack vectors derive from the revision number: a device joining a VTP domain with a higher configuration revision forces its whole VLAN database onto every switch, silently deleting or renaming VLANs anywhere in the domain. Because VTP is unauthenticated in many deployments, injecting forged advertisements can also reconfigure the domain.

Classes of attack: (1) revision-number takeover (drop a malicious static config in), wiping/changing VLAN definitions; (2) message spoofing if the attacker can emit VTP frames on a trunk; (3) denial-of-service by flapping VTP states. VTP v3 adds authentication (MD5 password) and better domain control, but the practical point is that VTP is avoidable.

The robust answer: run VTP off or transparent, define VLANs declaratively (via automation/templates or CLI) on every switch, never rely on protocol propagation for production VLAN state, and segregate trunk VLANs with allowed lists so customers/Access ports can never inject VTP. If some protocol is truly needed, use standards-based mechanisms (GVRP/802.1Q VLAN registration) or better, fabric controllers — and always treat VTP domain-wide VLAN modification as a critical control-plane exposure.

## Q63: How does DTP become an attack surface and how do you eliminate it?

**A:** DTP runs on every switchport by default in legacy configurations (dynamic auto/desirable), negotiating trunk status with any connected device. An attacker can plug into such a port and force a trunk, exhausting the switch's allowed VLAN list with tagged frames — the switch-spoofing technique of VLAN hopping. Because trunk ports can carry any allowed VLAN, the attacker gains Layer 2 membership across the domain.

Elimination: configure every end-user and device port as access mode with trunking disabled; the key is `switchport nonegotiate` (or the absence of DTP in modes that never negotiate) so no DTP frames are emitted, plus explicitly limiting the allowed VLANs on any genuinely needed trunk. Disable unused ports (admin down). Also consider the global default: on modern platforms, disable dense switchports.

Beyond DTP, treat all trunk-facing ports as security boundaries: allowed-VLAN lists, native VLAN change, no CDP/LLDP on user-facing ports (information leakage), and no untrusted devices ever on a trunk-enabled port. The senior answer: DTP is a convenience protocol with no place on a security-reviewed network; every port that can be access should be access, and every trunk should be administrative and immutable.

## Q64: What is a protected port (private VLAN edge) and how does it restrict traffic?

**A:** A protected port (also called PVLAN edge or port isolated) is a switchport configuration that blocks all Layer 2 traffic from other protected ports on the same switch/VLAN unless the traffic is destined to a non-protected port. Two protected ports cannot exchange frames directly — the switch drops the broadcast of source-to-destination between protected members — effectively an isolated-port behavior.

The mechanism is switch-local (not a protocol), so it works without private VLAN configuration; it simply constrains the MAC forwarding of protected ports to send frames only to unprotected (normal) ports. It is used to isolate guest devices, prevent peer-to-peer traffic among hosts on the same VLAN, and block device-to-device discovery in multitenant edge networks.

Comparison to PVLAN: protected ports are simpler and per-switch; PVLAN is fabric-wide and gives component/communal semantics (isolated/community/promiscuous roles). Protected ports still forward to the uplink (non-protected), so inter-host traffic must always route via the gateway. The senior note: protected ports are the less-scalable cousin of PVLANs and acceptable for small/quarantine segments, but full services (DHCP, monitoring, VLAN-wide features) prefer PVLAN.

## Q65: What are the architectural differences between L2 and L3 switching at the hardware level?

**A:** The forwarding engine differs: an L2 switch performs a MAC lookup (exact-match CAM) and a quick egress-port calculation, all at wire speed, with no IP logic in the datapath. An L3 switch additionally performs a destination-IP longest-prefix-match (TCAM), decrements TTL, rewrites the Layer 2 header (source/dest MAC), and possibly applies ACLs normally reserved for routers — all in hardware ASIC pipelines offering line-rate routing.

CPU use differs: in L2-only designs, the switch CPU handles control-plane traffic (STP, LLDP, management) but not forwarding; in L3 switching, the CPU builds and maintains the routing/ARP tables (OSPF/BGP/ARP), while the ASIC does the forwarding — the control plane is software, the data plane is hardware.

Capacity implications: L3 paths consume TCAM for route prefixes; pure L2 paths consume CAM for MAC entries; a large enterprise core with 50k routes shares fine TCAM budget with ACLs. The senior formulation: L2 vs L3 switching is a datapath question — one either encrypts frames transparently (L2 bridged) or terminates them and makes IP forwarding decisions (L3 routed) — and the engineering question is where the boundary belongs for routers, policy, and failure domains.

## Q66: What is TCAM and why does it underpin high-performance switching?

**A:** TCAM (Ternary Content-Addressable Memory) stores entries where each bit can be 0, 1, or X (don't-care mask), enabling parallel pattern matching (e.g., "10.0.0.0/8"). Given a packet field, the TCAM returns all matching entries in one lookup — constant-time regardless of table size — making it ideal for longest-prefix-match routing and ACL/QoS classification. For-warding lookups happen against TCAM at billions of lookups per second.

The debate: exactly the routing table (prefixes), ACL entries, QoS markers, VRF, and security filters share the same TCAM slices; the fixed size means a switch with 256k route entries can split between routes and ACLs. Having TCAM full is an operational failure: as new routes/ACLs fail to install, forwarding silently breaks or policy is not enforced.

Architecture nuance: TCAM search yields multiple matches (all entries that match), so the switch picks the best match (lowest install priority for routes, first-list-in-config for ACLs) — matching is in hardware but resolution logic matters. The senior point: TCAM is what turns rule-based forwarding into constant-time hardware lookup, and comprehending TCAM budget/concurrency is the difference between "it worked in the lab" and "it survived production scale."

## Q67: How does OpenFlow/SDN change how switches make forwarding decisions?

**A:** Classic switches have a fixed vendor-defined pipeline: the switch computes its own MAC table and runs STP/Routing to decide forwarding, with forwarding logic inside the device. OpenFlow/SDN separates the control plane from the data plane: a centralized controller installs flow tables (matched header fields) into the switch, and the switch forwards by matching bits against those flow entries — it takes no independent routing decisions for the flows it serves.

In the pure OpenFlow model, a flow entry is (match — e.g., in_port, dest MAC, dest IP, ethertype) -> (actions — e.g., output port, modify header, drop). The controller's view is global, so it can compute forwarding centrally, avoid loops without STP, enforce per-flow policy, and update forwarding instantly. The switch becomes a programmable pipeline rather than a fixed protocol machine.

The nuance: wide production deployment of pure OpenFlow gave way to hybrid devices — switches keep conventional L2/L3 silicon for the bulk of traffic while the controller steers exceptions and policies. Recent platform evolution (hardware pipelines, P4, programmable ASICs) made "the network is software" practical at scale. The senior answer frames OpenFlow as: control plane centralization, data plane generality, and the decision of what deserves to be controller-routed versus ASIC-forwarded.

## Q68: How did VXLAN evolve the concept of VLAN in modern data center?

**A:** VXLAN (RFC 7348) encapsulates an entire Layer 2 frame — complete with its 802.1Q VLAN tag preserved as inner VLAN — inside a UDP/IP packet (UDP 4789) with a 24-bit VNI (Virtual Network Identifier). The VNI provides 16 million isolated virtual networks, replacing the 4096-ID limit that boxed classic VLANs. Because the outer packet is routable, VXLAN lets a single layer-2 broadcast domain traverse a Layer-3 network: server pods across racks, buildings, or sites can share one L2 segment.

The overlay decouples the tenant's topology (VLANs/VNIs) from the physical fabric. VTEPs (VXLAN Tunnel Endpoints, on hosts or switches) encapsulate/decapsulate; the physical spine/fabric is pure L3. Broadcast, unknown-unicast, and multicast (BUM) traffic is handled either via multicast replication, head-end replication, or EVPN's BGP-based control plane (the modern answer) with ARP/ND suppression to eliminate most flood traffic.

The senior framing: VXLAN did not replace VLANs per se — it virtualized the classroom by carrying VLAN-inside-VNI, pushing the broadcast domain from the physical to the overlay, and letting operators run L3 everywhere physically. The migration path is usually: VLANs stay as the L2 segment per VNI, withe the fabric arbitrating where privacy and scale, ACLs, and routing live.

## Q69: How does link aggregation collapse spanning tree redundancy and improve resiliency?

**A:** EtherChannel presents N physical links as one logical link — a single STP port with one port role/bridge path. Since the bundle is one port, STP sees one path, never blocks any member, and a member failure does not trigger an STP topology change or failover — the aggregate continues carrying traffic on remaining members. This removes the redundancy-vs-loop tension that classic STP has no answer for except blocking.

Resiliency improves structurally: per-link failures are absorbed at the aggregation layer (no spanning-tree recomputation), link failures are detected via LACP (when member dead, the switch stops hashing to it) in sub-second time, and the surviving members carry the full load. The failure domain per bundle shrinks from "tree reconvergence" to "hash redistribution."

The caveat: the bundle can fail entirely (all members) like any link, and if both ends are switches, you still need = spanning tree above the bundle for loop-free multi-switch rings. In distribution/core, ECMP L3 (not STP) governs multiple paths; in L2 domains, the bundle essentially reduces STP decisions to "one logical link." The senior answer: aggregation does not replace STP — it removes STP from the path it does not need, pushing the loop-freedom concern upward to multi-path transport.

## Q70: How does EtherChannel load balancing work and what factors drive the hash?

**A:** EtherChannel distributes frames across member links using a hash of selected header fields. The fundamental rule: frames in the same flow must always take the same member (per-flow consistency), otherwise out-of-order delivery breaks TCP. Common keys: source MAC, destination MAC, both MACs, source IP, destination IP, both IPs, or IP + L4 ports. The configured mode picks the fields hashed; results map to members modulo the port count (or via a more even bucket scheme in modern ASICs).

Field choice drives distribution quality. L4 ports produce the finest granularity but require deeper parsing; MAC-based hashing convinces a L2 switch with few hosts to massively skew. Hash only guarantees evenness statistically — with the modulo/evenness property, 2-3 large flows scheduled to same port can saturate one member while others idle, so distribution is load-agnostic, not load-aware.

Higher-end switches use a larger number of buckets (e.g., 32-64) remapped to active members, and hardware can rebalance when members come/go. The senior angle: choosing the hash key is architecture — you align it to the traffic mix (server/storage uses IP+port; transparent L2 topologies use MAC+IP), and you accept that aggregation is a statistical engine, hence you size members to absorb skew and never assume perfect balancing.

## Q71: Compare LACP and PAgP for link aggregation.

**A:** LACP (Link Aggregation Control Protocol, IEEE 802.3ad/802.1AX) is the standardized aggregation protocol. It runs in active or passive mode, sends PDUs every second by default, and negotiates bundles only between devices that both speak it. It is vendor-interoperable (Cisco, Arista, Juniper, Linux bonding, ESXi/vSwitch, cloud environments — all support it) and offers stable/active member selection and port-priority tie-breaks.

PAgP (Port Aggregation Protocol) is Cisco's proprietary equivalent, with modes auto/desirable and essentially the same negotiation semantics, plus support for "on" static bundling. It is obsolete functionally but still exists for legacy Cisco fabric. Both negotiate: only matching-speed/duplex/VLAN members join; the number of successful negotiation packets is a quick health indicator.

The practical choice: LACP in active mode on both ends, with the passive side (or cross-platform) handled by LACP requiring >= 1 active side. Static "on" bundling (no negotiation) is valid on point-to-point links but error-prone for change management. The senior answer: prefer LACP active-active for everything modern, include PAgP only as compatibility knowledge, and remember that the negotiation protocol (LACP/PAgP) is different from the hashing mechanism (Q70) that carries the traffic.

## Q72: What are storm controls and when do you configure them?

**A:** Storm control rate-limits broadcast, multicast, and unknown-unicast traffic on a port: when any of the three exceeds a configured threshold (percentage of interface or absolute pps), the switch drops the excess or error-disables (supress mode). Without it, a broadcast storm (from a loop, misbehaving device, virus propagation) can saturate links and starve legit traffic silently.

Configuration: threshold per traffic class (broadcast 1-2% is common on access, with unicast/multicast set higher or separate); drop-traffic mode (start dropping, then recover automatically) versus shut-down. It coexists with the "unknown unicast flood" that is normal in bridge mode — the control caps only the runaway over-provision, not transient legitimate flooding.

The senior nuance: storm control is a symptom limiter, not a fix — a storm source is a loop/misconfig/attack, so storm control protects the neighborhood but you still locate and remove the cause. It is also a central defense in network segmentation: on access ports, setting broadcast low alongside DAI/snooping reduces the blast radius of ARP flood or DHCP flood attacks. Knowing threshold tuning vs default (unlimited) is the difference between "I added storm control" and "I made the network resilient."

## Q73: What is IGMP snooping and what does it change about multicast flooding?

**A:** A switch without IGMP snooping forwards all multicast frames as unknown — flooded to every port in the VLAN — because multicast MACs do not match unicast MAC entries. IGMP snooping listens to the IGMP membership reports hosts send (and queries the router sends), building a per-group, per-VLAN multicast address table: the switch then forwards multicast only to ports whose hosts joined that group, plus the router-facing port for the querier.

Beyond forwarding, the snooping switch optimizes the querier: it forwards multicast to the router port so the router's multicast routing (PIM) knows group members, suppresses duplicate reports to the router, and depending on implementation, can act as an IGMP querier if none exists (ensuring hosts see group queries in segments without a routed querier).

Caveats: snooping depends on seeing group membership; if reports are not seen (host doesn't send IGMP), multicast reverts to flooding. Storm control, per-VLAN snooping, and fast-leave (immediate removal) are tuning levers. The senior insight: snooping converts a broadcast-domain multicast pain into an exactly-targeted forwarding table — which is why multicast in large L2 works only when your switch does snooping well.

## Q74: How do MAC entries and VLAN interact in the forwarding database (FDB)?

**A:** The forwarding database (FDB) is indexed by the pair (MAC address, VLAN). A MAC learned in VLAN 10 is stored as VLAN10/MAC -> port; a second instance of the same MAC in VLAN 21 is a separate entry. Lookups for destination are always VLAN-scoped: an ingress frame in VLAN 10 matches only VLAN-10 entries, never VLAN-21 — which is why the same physical machine can legitimately appear on two ports if it spans VLANs (e.g., a router with subinterfaces).

Learning and flooding operate within the frame's VLAN: a VLAN-10 broadcast learns/updates VLAN-10 entries only; unknown unicast on VLAN 10 floods VLAN-10 ports only. Aging is per (MAC, VLAN) or per-VLAN; a topology change flushes entries per-VLAN and per-port. Trunk ports are exceptional: the same physical port hosts entries across many VLANs, so port-based security counting must accommodate per-VLAN MACs.

The senior design consequence: all forwarding behavior — learning granularity, floods, and security — is VLAN-qualified. Overlay mapping (VLAN map to VNI on VXLAN) preserves this by carrying the inner VLAN. The interviewer probing this wants you to state clearly: the switch does not have "a device table," it has a per-VLAN FDB, and that is why broadcasts and floods stay inside their VLAN.

## Q75: What are cut-through and store-and-forward switching and when does each matter?

**A:** Store-and-forward (SAF) fully receives the frame, checks the CRC/validates it, then forwards at (potentially) the same wire rate. Since an errored frame is dropped rather than forwarded, SAF guarantees corruption-free egress and is the default on enterprise switches for Ethernet. The cost is added latency — essentially one full frame-duration — which matters on long-distance DCI or latency-critical financial traffic.

Cut-through begins forwarding as soon as the header (destination MAC, plus optionally a slice of the payload) is parsed; total time is on the order of a hundred ns. It does not check the CRC, so error frames can egress — the receiving end discards them — and a damaged frame on a fed link can copy errors across. Fragment-free is a hybrid that waits through the first 64 bytes (enough to catch collision-in-medium fragments in CSMA/CD) before forwarding.

Choice is operational: egress-facing server-to-server (low error rates, low port bandwidth) tolerates cut-through for micro-latency; uplinks/core where safety matters use store-and-forward; fabric intermediate (cut-through across a small campus) is a tuning decision. The senior point: the measure of a switch is not just its bus speed but its internal forwarding latency and whether it hides or reveals damaged frames — and modern ASICs make both fast enough that the decision is mostly about error governance rather than raw latency.

## Q76: How would you design a campus network's VLAN and spanning tree architecture?

**A:** A canonical campus design has three tiers — access, distribution, and core. Layer 2 (VLANs + spanning tree) lives below the distribution: each access switch is one broadcast domain (or a small set of access-VLANs), the distribution switches run SVIs as the L3 gateway per subnet, and VLANs do not extend above the distribution. At the distribution, RPVST+ (or MST) runs per VLAN with two distribution root switches and load-sharing of VLAN groups per root.

Broadcast domain planning: 50-200 hosts per access VLAN is the pragmatic cap, aligned with IP ranges (a /24 holds a single L2 segment typically). Management VLANs are isolated; user, voice, guest, IT/IoT VLANs are separated, each with its own subnet and ACL at the gateway. Uplinks from access to distribution are aggregated (EtherChannel) so STP has little to do; redundant distribution pairs use VRRP/HSRP per SVI.

Failure-domain logic: STP protects the L2 segments against accidental loops; routed access (L3 at the access) is the modern alternative that removes STP entirely by making every access switch a routed boundary. The senior framing: decide where L3 starts — SVIs at distribution keeps L2 manageable; routed access trades VLANS for routing peers; in both, STP operates only where L2 truly exists.

## Q77: How do you size VLANs — how many hosts, how many switches — and what are the trade-offs?

**A:** Hosts per VLAN: practical guidance is 50-200 in campus (with broadcast safety), larger in storage/fabric networks only when traffic discipline allows. The constraints that drive size: broadcast domain load (ARP/DHCP/mDNS), fault domain (a loop or storm affects all), STP convergence behavior, and the CHAOS of unknowns (unknown unicast flood multiplies with member count). Each VLAN is also a threshold of MAC-table entries per port/switch.

Bounded by switch capacity: the number of access switches in a VLAN must not exceed what the distribution can preserve loop-free under STP and still converge in target time — with EtherChannel to the distribution, the cap is dictated by the number of point-to-point bundle paths, not switch count. Management overhead grows per VLAN ID, so hundreds of VLANs require disciplined naming and housekeeping

The trade-off matrix becomes: small VLANs give better broadcast/loop blast radius and converge faster, but multiply subnet, routing, and access-port administration; large VLANs simplify administration but stress convergence and forwarding pruning. Modern answer: prefer smaller L2 domains, route more (routed access / L3 to access), and let the fabric (EVPN) handle scale rather than stretching giant single broadcast domains across the campus.

## Q78: What are realistic STP convergence targets and how do you validate them?

**A:** RSTP/PVST+ should transition a blocking-to-forwarding port in ~1-4 seconds under normal conditions (the proposal/agreement handshake is sub-second on point-to-point). The accepted target is: user traffic loss < 10 s, and distribution/core failover < 2-5 s when redundancy is L2. Anything slower implies a classic-timer fallback, a shared-medium link, or topology issues — none of which belong in a healthy RSTP domain.

Classic STP targets: up to 50 seconds worst case (max age 20 + forward delay 30). If your design cannot meet 5 s, either upgrade to RSTP/MST or move the redundancy to L3 (ECMP, VRRP across SVIs) where failover is measured in milliseconds via BFD and route convergence.

Validation practices: run `show spanning-tree` topology snapshots from multiple vantage points, confirm convergence timers are actually RSTP not 802.1D, monitor for topology/TCM events and MAC flapping, simulate failures (/shut a link, kill a port) and measure traffic loss, and capture BPDUs to verify the root and role agreement. The senior point: you do not trust STP because it is configured — you prove convergence is in spec with fault-injection tests, because a silently malfunctioning STP domain fails exactly at the worst moment.

## Q79: How does BGP EVPN solve the broadcast domain scalability problem at data center scale?

**A:** BGP EVPN (RFC 7432) runs an MP-BGP control plane between VTEPs that learns and distributes MAC/IP reachability as routes (Type-2 for MAC/IP, Type-3 for anycast-IGMP multicast). Instead of flood-and-learn VXLAN or multicast-based BUM transport, every VTEP knows which remote VTEP hosts a given MAC — so an ARP/ND request or unknown unicast can be answered/suppressed locally rather than replicated fabric-wide.

The classic VLAN pain points EVPN removes: no 4096 VLAN limit (VNI space), no flooding on links for resolution (ARP suppression at the edge), no STP in the fabric (the L2 is virtual, the physical fabric is pure L3 ECMP), and instant mobility (MAC movement events update routes without flooding). It also consolidates multi-homing and active-active design via ESI/Ethernet segments.

Integration with switching: VLANs remain the tenant's L2 construct; the fabric maps VLAN->VNI and the control plane programs the MAC table accordingly. This is why EVPN-VXLAN is the de facto modern DC fabric: it scales L2 services to thousands of devices while keeping the physical network routed, loop-free, and flooding-free. The senior angle: EVPN is the system that ended both "VLAN max 4096" and "STP must span the DC" — it redefines broadcast domains as control-plane knowledge.

## Q80: What is multi-chassis link aggregation (MLAG/vPC) and how does it interact with spanning tree?

**A:** MLAG (vendor-specific: vPC on Cisco, MLAG on Arista, MC-LAG generally) lets two switches present as a single logical switch to a downstream device (host or access switch) over a bundle that spans both chassis. The downstream bundles two physical links (one to each switch) into one logical port-channel; each member is active-forwarding, and a single-volume failure is invisible to STP.

How spanning tree interacts: from STP's perspective, both MLAG members appear as one switch (one bridge ID, synchronized BPDUs), so the downstream bundle is a single STP port carrying both links. No member blocks; a peer failure updates hashing, not the spanning tree. STP above the MLAG pair still operates (the pair presents as one logical device in the tree), still loop-free on redundant uplinks.

The critical operational knowledge: peer-link failure, the interconnect between the two switches, must not cause split-brain spanning-tree configurations — the pair falls back to single-switch or suspends/isolates ports to keep the topology accurate. The senior answer: MLAG removes STP from the access-to-distribution path, leaving STP only where physical redundancy demands it, and it is a prerequisite for active/active first-hop redundancy designs that do not rely on one switch doing all the work.

## Q81: What happens during a peer-link failure in vPC/MLAG and how do you preserve correct forwarding?

**A:** In vPC/MLAG, the peer link (PL) is the interconnect across which the pair exchange control and data for multi-chassis flows. When the peer link fails but the pair still sees users (no direct user-to-user), the switching fabric could split into two independent devices both claiming the same MACs/VLANs — the "split-brain" condition where both sides forward independently and potentially create the same loop STP cannot see because both think they are the primary.

Each MLAG implementation has a designed response. Cisco vPC uses a peer-link keepalive and a "dual-active detection" mechanism: on detecting peer-link loss, the secondary switch suspends its virtual port-channel members and makes its ports go blocking to keep the topology loop-free. Arista MLAG similarly uses keepalive plus a primary-election and deactivates the secondary side to maintain loop freedom.

Operationally, this is why MLAG deployments require (a) a parallel keepalive path independent of the peer link, (b) careful sizing — the peer link carries all-to-all traffic and must match combined bandwidth, and (c) defined primary/secondary roles. The senior teaching point: the failure domain is "cannot have both side-edge forwarding," and any design claiming active/active must also state what the system does when the two brains lose contact — because those race conditions are where production outages are born.

## Q82: What are the differences between software-defined switching (OVS) and hardware switching?

**A:** Open vSwitch (OVS) is a soft switch in userspace (dpdk variants) with a flow-table pipeline: the first packet of a flow is slow-path-consulted with the controller/table, and subsequent packets are fast-path matched against compiled flow rules. It excels at programmability (OpenFlow), portability (runs anywhere), and tunneling (VXLAN/GENEVE), and it is the substrate of virtual networking in KVM/OpenStack/container-land.

Hardware switching is silicon: ASIC pipelines (TCAM matching, fixed pipeline stages, header rewriting) achieve line rate on millions of flows but are specialized — programmability comes through vendor APIs/telemetry, and features are bounded by what the silicon implements. The modern middle ground: match-action tables (OpenFlow/P4 goals) are implemented in merchant silicon (e.g., Broadcom Trident/Tomahawk), letting OVS-inside-hardware-style logic run at wire speed.

The engineering reality: OVS + DPDK forwarding a server NIC offers tens of Gbps with CPU, and software switches peer multiple tenants in virtual hosts, but line-rate 100G+ multi-vendor fabrics need ASIC path. The senior framing: it is not OVS vs silicon — it is where the packet's destiny is decided (virtual switch on the host, or physical switch in the rack) and how the control plane programs whichever data plane exists.

## Q83: How do merchant silicon and ASIC pipelines shape modern switch architecture and TCAM budgeting?

**A:** Merchant silicon (Broadcom, Marvell, Cisco's BCM, NVIDIA Spectrum) implements a fixed forwarding pipeline: parse -> classify (ACL/TCAM) -> forwarding decision (MAC/IP lookup) -> rewrite -> queue. The pipeline is highly optimized, deterministic, and fixed at fab time; the vendor's ASIC maps its features (L2/L3, ACL, QoS, tunneling) onto pipeline stages and TCAM slices. Line-rate operation is a consequence of the pipeline, not software.

TCAM budget is a constraint with direct consequences: routes, ACLs, and flows share TCAM; hundreds of thousands of prefix entries cost TCAM, and ACLs per VLAN cost more. When the TCAM is full, additional ACLs/routes do not install, and the failed-install is silent on some platforms — the !-cmd result is a partial policy. Capacity planning means knowing your prefix and ACL headroom, not just "it has TCAM."

The senior architectural point: because pipelines are silicon-fixed and TCAM is partitioned, every new feature (VXLAN, DPI hooks, RSPAN) competes for the same resources. Buying a switch is really buying a budget — of flows, prefixes, ACLs, and queue buffers — and architects design feature sets to fit the silicon, which is why different vendors excel at different workloads and why "just add an ACL" can degrade a fabric.

## Q84: How does a switch implement QoS and 802.1p priority and where does CoS map to DSCP?

**A:** A switch classifies a frame on ingress: it can read the 802.1p PCP 3-bit, or impose per-port/per-VLAN default classification on untagged or unclassified traffic. It maps that class to an internal QoS value (queue group), applies policers/traffic conditioning if any, and on egress schedules the frame on the appropriate queue (typically 4-8 queues per port) via a scheduler (strict priority + WRR/DWRR) plus optional ECN marking. 802.1p is therefore just the "tag into the queue" mechanism.

Where CoS maps to DSCP: CoS is classified at L2 (marking/queue), DSCP at L3 — the mapping policy `mls qos map cos-dscp` / `mls qos map dscp-cos` on Cisco (or equivalent) defines how one converts to the other, commonly 1-queue-per-class or tighter 8-queue. The 802.1Q tag's PCP/DEI fields can carry the class across trunks; DSCP carries it across L3.

Design consequences: Cisco-style quiet trust (trust dscp on uplinks) prevents a host from setting DSCP to a high class and getting priority it should not have, so the switch re-marks untrusted ports; voice VLANs get trust cos; storm control before queueing. The senior insight: QoS is an ingress-classification to egress-scheduling pipeline — and poor configuration (untrusted DSCP, no PCP mapping) quietly destroys fairness even when bandwidth is huge.

## Q85: How does IGMP snooping interact with multicast routing and what are the failure modes?

**A:** IGMP snooping is at the access/distribution switch: it watches hosts' IGMP joins/leaves and builds a per-group (per-VLAN) multicast forwarding table so multicast reaches only ports with members, plus the router/mrouter port for the querier. The router (with PIM) needs to see joins to forward multicast into the VLAN; the snooping switch forwards queries and extends membership state.

Failure modes: (1) the switch does not see reports (host sends IGMP but switch fails to snoop) — multicast floods as unknown to all ports in the VLAN, preserving reachability but increasing load; (2) no querier in the segment — hosts never hear queries, their membership expires and multicast stops being delivered; some switches provide an IGMP querier fallback for L2-only segments; (3) fast-leave and proxy-reporting affect report suppression timing; (4) multicast storms unhandled.

Design practice: enable snooping per VLAN, identify the mrouter port (router that routes multicast for that segment), ensure a determined querier exists, bound group limits when needed, and treat snooping as a learning layer — the router still decides which groups route in, and the switch only optimizes who locally gets copies. The senior answer connects: snooping makes multicast LAN-friendly, but the multicast routing model (PIM) and the querier story are the real availability drivers.

## Q86: What symptoms indicate a VLAN mismatch or an STP loop and how do you isolate them?

**A:** VLAN mismatch on interconnected switches shows up as silent traffic isolation on the mismatched VLAN: only the native VLAN's traffic proceeds, tagged traffic crossing the mismatched link is dropped (or mis-homed), and inter-switch reachability fails for every non-native allowed VLAN. STP loop symptoms are opposite and louder: broadcast/unknown-unicast flooding, saturated uplinks, high CPU, MAC flapping, duplicate packets, and contact instability across the looped domain.

Isolation workflow: check `show interfaces trunk` on both ends, compare native/allow VLAN lists and commit; dump `show mac address-table` across a few switches to find a MAC flapping between ports; capture a few seconds and inspect for BPDUs/TCN and the flood ratios; and, if a storm is present, immediately evaluate the loop — identify the forwarding ports that should not forward, and (for a service outage) take out the suspected link to restore service before root-causing.

The senior-scale practice: run "spanning tree topology" snapshots plus a flooding observer or a storm-control alert; when you suspect loops, collect syslog/SNMP (TCN counts, MAC flap logs), compare trunks' allowed/native on both ends of suspected links, and validate with a single-vlan test (ping across each VLAN) to pinpoint which broadcast domain is broken. Diagnosis is about correlating three artifacts — MAC table, STP state, and trunk config — not guessing.

## Q87: How do you safely break a Layer 2 loop in a production network?

**A:** The priority is service restoration: locate the loop — the worst suspects are ports that are forwarding when they should be blocked (they will show as forwarding/root/designated while peers show blocking, or you will observe MAC flapping across them) — and (a) shutdown/preventing forwarding on the redundant link (or promote a designated port to a legal role) to immediately stop the storm. If the loop is massive/a tree flapping, isolate the FIRST suspicious switch by removing trunk uplinks, or error-disable the flapping ports.

After stabilization, diagnosis: review Spanning Tree for illegitimate root or role flips; confirm every port is in a legal state (root/designated on allowed paths, alternate/backup on redundant); check BPDU Guard/Root Guard status and the "PortFast" access ports that received BPDUs; run `show mac address-table` across all switches to spot flapping. Use monitoring to correlate the storm time with events (switch reboots, config changes, new equipment patched-in).

Permanent safety: make redundant links loop-proof by (a) proper STP with BPDU/Root/Loop Guard, (b) removing accidental bridging (EtherChannel everywhere across redundant bundles), (c) no foreign switch insertion (BPDU Guard on access), and (d) bounded timers. The senior mantra: STP is the heart-lung — it is essential; but a loop is the fastest service outage in networking, so practice runbooks with the storm scenario before it happens.

## Q88: What are the scaling limits of PVST/RPVST+ and when do you switch to MST?

**A:** RPVST+ runs one instance per VLAN with one bridge ID, its own BPDUs, and independent re-convergence. Scale costs: BPDU processing grows linearly with VLAN count (every switch processes every instance's BPDUs), and a link flap or topology change triggers re-convergence logic across all instances the switch serves. Sizing the number of VLANs (e.g., >50-100) with many uplink switches can hit CPU convergence issues in outage moments, and operational complexity rises in next-per-VLAN root tuning.

MST uses a small number of instances (often 2-4) that map groups of VLANs to instances; each instance is one spanning tree, so BPDU and convergence costs stay flat — the limit instead is mapping clarity (which VLANs in which instance, one region agreement, instance-to-IST interaction). Platforms and scale mesh: MST keeps CPU and BPDU load constant while still enabling per-instance load balancing of VLAN groups.

The switchover reasoning: RPVST+ is perfectly defensible up to a few hundred active VLANs; MST wins when (a) VLAN count is high, (b) the fabric must scale across many devices, or (c) you need region-based filtering (MST regions referencing other bridges). The senior recommendation: use MST for core/distribution spanning many hundred VLANs, keep per-VLAN (RPVST+) only in small-roling edge segments, and match MST mapping exactly across the region — mapping mismatches fragment region behavior silently.

## Q89: What is the modern best practice for VTP — server, client, transparent, or off?

**A:** Industry consensus converged on no VTP for data-carrying VLANs. Use VTP off (or transparent for relay/non-participation) and create VLANs explicitly per switch — usually via templates, automation, or a fabric controller — so no switch can overwrite another's database. VTP server/client remains acceptable only in tightly controlled, fully-Cisco, no third-party-addition environments, and even then the revision-number wipe risk makes it a liability.

The reasons: VTP can silently erase/rename VLANs domain-wide (revision number authority), requires trunk to propagate, and offers no auditable flow for device changes; automation now achieves the original goal (consistent VLAN definition everywhere) with deterministic, reviewable, versionable configs instead of an unauthenticated control-plane protocol.

VTP v3 adds authentication, private VLAN and MST support, and per-role isolation, which is a genuine improvement — but the deployment wisdom is unchanged: define VLANs in one source of truth and propagate by config-management, not by a protocol loop. The senior answer must articulate: VTP solves a configuration-distribution problem that automation solves better, so the correct choice is not "which mode" but "no VTP at all."

## Q90: How does 802.1X with dynamic VLAN assignment work in a switched environment?

**A:** 802.1X places a port in an unauthenticated state until the attached device proves identity via EAP (usually EAP-TLS with machine certs, or PEAP for users) toward a RADIUS server. Between the client and the switch, EAP frames are carried over an uncontrolled port (or through a guest VLAN). The RADIUS server, upon successful authentication, returns an Access-Accept that includes the VLAN to assign (in the cisco-av-pair or similar attributes) and optionally an ACL and QoS profile.

The switch then opens the controlled port and puts it into the returned VLAN, typically with a per-session (dynamic-tagged) assignment so the VLAN follows identity without static per-port VLAN config. If the RADIUS attributes are absent, the switch falls back to the port's configured access VLAN — and if authentication fails, the port can be placed in a quarantine or guest VLAN, or blocked entirely.

Operational considerations: dynamic VLAN assignment assumes the VLAN exists on the switch, the trunk carries it, and DHCP/other scopes are ready; coexistence with VoIP no dot1x variants (multi-auth/multi-host vs single-host) defines how many identities a port honors; and the port must be able to handle both unauthenticated (LLDP, EAPOL) and authenticated traffic states. The senior answer: 802.1X makes the switch a policy enforcer, and the VLAN becomes an attribute of the session — the modern way to translate "who the user is" into "which network segment they join."

## Q91: How do VLANs map to VNIs in an EVPN-VXLAN fabric and where does broadcast live?

**A:** In EVPN-VXLAN, each VLAN (the tenant's L2 segment) maps to exactly one VNI on the VTEPs; the fabric transports "VLAN X" as "VNI 10001" encapsulation over the L3 fabric. The switch keeps a VLAN->VNI mapping, forwards by inner-VLAN MAC table, and the outer UDP/IP tunnel emerges from the exact VTEP. The fabric itself is L3; the VNI is network-isolation-and-mapping, not a flow construct.

Broadcast/unknown-unicast/multicast (BUM): rather than flooding on physical broadcast domains, EVPN typically performs head-end replication (each VTEP duplicating BUM to the remote VTEPs that have members of that VNI) or multicast groups. ARP/ND suppression is the big win: the VTEP learns remote MAC/IP via EVPN Type-2 routes, so it answers ARP locally without an over-the-fabric broadcast; multicast uses Type-3 for anycast-IGMP membership.

The design synthesis: the VLAN exists only at the edges (access and gateway VTEPs); it does not exist between. Broadcast is either replicated edge-to-edge when necessary or suppressed when the control plane knows the answer. This is the answer to "VLAN max 4096" and "broadcast domain scale" — reliably, L2 services scale by VNI and control-plane resolution, and the fabric stays loop-free (ECMP), no STP in the spine/leaf.

## Q92: What are the underlay and overlay design considerations for an EVPN-VXLAN fabric?

**A:** Underlay: spine-leaf topology over an L3 fabric running OSPF/IS-IS or eBGP as the IGP, with ECMP across all spine paths; every leaf and spine interface is a routed port — no L2 VLANs and no STP in the underlay. MTU must carry VXLAN (payload + outer headers); jumbo MTU (9000 likely) everywhere with consistency. BGP (RFC4271 and EVPN address family) is the normal combination: eBGP underlay + EVPN control plane for MAC/IP learning.

Overlay: leaf VTEPs terminate VNIs; a VNI per segment (VLAN-to-VNI mapping), with EVPN Type-2 routes advertising MAC/IP and Type-3/Type-5 carrying multicast and IP-prefix (for routing into/out of the fabric). Load balancing of multicast (anycast first-hop gateway — the same IP/MAC on the overlay in every leaf) makes VLANs appear identical anywhere, enabling mobility with no flood/failover event.

The senior synthesis: the underlay gives you reachability and ECMP; the overlay gives you L2 services abstracted from topology; the control plane (EVPN) replaces flood-learn. Failure semantics: anycast gateway + VXLAN + EVPN separates "physical failure" (underlay reroutes, ECMP) from "logical failure" (a VTEP dies, its MACs re-advertised from the neighbor). This is why modern DC fabrics are designed as EVPN-VXLAN rather than VLAN + STP.

## Q93: How do campus and data center switching designs differ and why can't you copy one to the other?

**A:** Campus design assumes many leaves, sparse-to-moderate bandwidth per user, L2 at the edge (VLANs + STP), a distribution layer for routing/redundancy, and management of hundreds of switches with user mobility. Failover is human-tolerant — seconds of routing/link recovery latency do not break browsers, but broadcast/VLAN sprawl and STP complexity are the chronic enemies.

Data center design assumes dense east-west traffic, thousands of servers in a few pods, high bandwidth per port, and tenancy that must scale: fabric-first L3 (spine-leaf, ECMP everywhere), VXLAN/EVPN overlays for L2 services, anycast-gateway mobility, and microburst/safe-DC rocks handling sensibly. Tenants expect 9's of lattice availability and sub-millisecond-visible convergence.

Why you cannot copy: campus carries broadcast domains and user VLANS and tolerates slow convergence; DC cannot host thousands of VLAN/STP-evolving edges and needs routing where campus uses bridging. Conversely, DC's VXLAN+EVPN complexity is unnecessary hardware for a 300-user campus. The senior summary: both are about failure domains and convergence speed — campus accepts larger broadcast/latency domains with slow failover, DC budgets wire-speed routing, microburst buffers, and millisecond convergence — and the correct architecture follows the workloads, not the pretend-to-be-arbitrary.

## Q94: How do you automate and program VLAN and switching configuration at scale?

**A:** The modern stack: define VLANs, ports, and policies as data (YAML or a source-of-truth like NetBox/IPAM), then render per-device config with Jinja2 templates and push via NETCONF/RESTCONF/gNMI (on voice) or CLI through drivers (Ansible). The pipeline is: inventory -> source of truth (facts) -> template render -> diff -> validate -> apply -> post-check, with native MIBs/NDFs (e.g., Cisco NDF, Arista CloudVision) supporting model-driven config and state.

Because VLAN definition is microservice-per-switch (per platform database), automation guarantees consistency: the same VLAN ID/name/MTU/STP settings land on every switch, and trunk allowed/native VLAN lists are deterministic. Orchestration also programs EVPN/MLAG parameters (anycast-gateway MAC per VLAN, VNI mappings) so the whole fabric converges from one policy file, not humanly-edited configs.

The senior importance: automation transforms VLAN administration from synchronous command execution to intent + validation. (a) changes are diff-reviewed before apply; (b) rollback is possible; (c) drift is continuously detected (config against source of truth) and remediated; (d) life-cycle events (new VLAN for a new tenant) are one version-controlled change instead of a manual multi-switch session. The failure mode to avoid: automation that applies unvalidated config — because a VLAN typo or an over-broad trunk prune now propagates network-wide instantly and is repeated on every switch, which is why validation and gated change are mandatory.

## Q95: What do switch specs like switching capacity, forwarding rate, and oversubscription mean and how do you size them?

**A:** Switching capacity (bandwidth) is the aggregate of all ports in both directions; forwarding rate is the number of packets per second the ASIC can process (e.g., 2.5 Bpps). A switch whose ports sum to 200 Gbps but can only forward a fraction of that on small packets would drop — full-size frames are cheap per bit, but small packets cost one lookup each, which is why line-rate is quoted in pps, not bps. Oversubscription is the ratio of downstream port capacity to upstream bandwidth (e.g., 48x10G access, 2x40G uplink = 6:1), deliberately chosen per workload.

Correct sizing: compute pps (bytes/pkt × egress capacity) and confirm the ASIC meets it for your smallest-common-packet workload; evaluate oversubscription against traffic profile — burst tenants need lower ratios; east-west DC fabrics aim near 1:1 uplinks or layered oversub (spine has no defined spine). Head-of-line blocking (HOLB): buffer exhaustion bursts overflow on egress to other queues — buffer depth and VOQ mitigate. When a switch "drops packets under load," half the time it is oversubscription, not tonnage.

The senior lesson: specs are ceilings, not promises — 2/3 Gbps switching capacity does not mean every flow achieves it; small packets, ACL insets, and buffering economics are the real determinants, and you size the design with a measured packet-size and burst profile, not the marketing sheet.

## Q96: How do you plan MTU and jumbo frames end to end in a switching environment?

**A:** MTU planning is a coordinate across every hop: host NICs, access ports, trunks (VLAN tags), and L3 interfaces. The eternal trap: each segment accepts up to its own MTU, and a packet carrying maximum payload across a hop whose MTU is smaller is dropped — silently on L2. Start with the payload maximum (e.g., 9000-byte jumbo for storage/iSCSI/NFS, 1500 for general LAN), add the tag overhead (802.1Q +4 bytes; VXLAN +50 bytes) and configure every hop's MTU to be at least the payload plus that overhead, rather than relying on fragmentation (which is harmful for storage traffic) — no exceptions.

Practical rules: set the same MTU across an L2 broadcast domain (all access + trunks), test end to end (ping with DF/no-fragment, vary sizes), be aware that crafted ACLs can filter based on DF, and align MTU with STP/RPVST BPDUs (they are carried within MTU). DC with VXLAN sets outer MTU 9000 (or 9216) so the inner 1500/Jumbo payload fits within the tunnel, and the fabric's L3 underlay carries the full 9000.

The senior acceptance: .MTU is a class of design invariant — "the sum of header overheads must never breach any hop." Change management discipline demands a single source of truth for the MTU policy (e.g., NetBox) and automated push of the same template, plus an MTU discovery tool (ping with DF across every path) part of release validation for new links.

## Q97: What are DCB, PFC, and lossless Ethernet and how do they interact with switching?

**A:** Data Center Bridging (DCB) is the IEEE suite for lossless Ethernet: PFC (Priority Flow Control, 802.1Qbb) pauses flows per priority class at the ingress/egress queue; ETS (Enhanced Transmission Selection, 802.1Qaz) schedules guaranteed bandwidth shares per class; and DCBX (DCB Exchange Protocol) negotiates parameters on links. Together they lets Ethernet emulate the lossless consumption patterns Fibre Channel delivered, which is exactly why FCoE (Fibre Channel over Ethernet) became viable.

How it interacts with switching: a switch within a PFC domain believes "this priority will never drop — the peer promises to pause before overflow." That changes the reliability model: the network promises no drops on the lossless class and defers congestion by pausing the peer's priority flow. When a queue overflows, PFC pauses upstream traffic on that class, holding congestion in place, and the burst propagates head-of-line — a single storm can make the whole data center degrade badly if PFC domains are misconfigured.

The design caveat: PFC works on a single lossless domain (typically one VLAN/DCBX segment); spanning inter-switch loops breaks the pause logic; oversubscription defeats pauses. The senior summary: lossless Ethernet trades drops for complex, coupled QoS control, and it is a contraction — you use PFC/DCB only where you genuinely need zero-loss queues (FCoE, some RDMA), and you keep them scoped/VLAN-isolated because the pause storm is a worse failure mode than a drop at an edge link.

## Q98: What telemetry and monitoring do you run on a switched fabric and how do you detect issues?

**A:** Two tiers: control-plane state and data-plane behavior. Control-plane: spanning-tree BPDU/role changes, VTP/trunk state, MAC-table changes and flapping events, ARP/ND resolution rates, VLAN membership drift, router adjacencies (BGP/OSPF for L3). Data-plane: interface utilization, error counters (CRC, runts, giants), unicast/multicast/broadcast storm levels, per-queue discard/buffer (HOL), and flow counts. 

Tools: switch CLIs (`show mac address-table`, `show spanning-tree`, `show interfaces trunk`) for ad-hoc, SNMP for counters, streaming telemetry (gRPC/gNMI, NETCONF) for push models and state deltas, sFlow/NetFlow-IPFIX for flow sampling, and RSPAN/ERSPAN for packet capture. Integration into a network-monitoring stack (LibreNMS/Nagios/PRTG/ELK + NetBox as source of truth) with alerts on MAC flapping, STP TCN, trunk mismatch, broadcast rate, and CPU.

Detection patterns: MAC flapping = loop or moving host; high unknown-unicast flood = CAM counterfeit or asymmetric path; STP TCN storms = config churn or failing edge; trunk mismatch errors = config drift; buffer fullness = microburst/HOL. The senior point: you are not just monitoring link up/down — you monitor the control-plane events that precede failures, and you pair telemetry with automated drift checks so the fabric declares itself healthy only when state and config agree.

## Q99: How do programmable data planes (P4) and in-network computing change switching architecture?

**A:** P4 lets you program the forwarding pipeline itself — match-action stages, headers parsed, protocol fields carried — instead of buying silicon fixed to Ethernet/IP. The switch becomes a configurable function: you can add telemetry headers, define custom flows, implement encapsulation beyond VXLAN/GENEVE, or offload — in-network computing — reductions, load balancing, DNS/anycast logic, or caching directly on the ASIC/switch at line rate.

The architectural consequence: flexibility moves from "which fixed protocols does this ASIC do" to "what pipeline did the operator compile." Programmable silicon (Tofino family, Nexus One/Starlight, NVIDIA Spectrum-X is partly reprogrammable) gives vendor-independent feature/behavior, addressing the TCAM/fixed-pipeline limit that Q83 described. It supports the SDN philosophy — data plane is software-defined — more deeply than OpenFlow controllers ever did with fixed chips.

The tension: programmability costs talent, firmware maintenance, and the "silicon confidence" (Cisco-quality error handling on their own chips). Most networks buy fixed specs; P4 shines for cutting-edge features at scale. The senior framing: the direction is verified — pipelines are becoming program + data — the innovation is making the switch behave how the workload demands (custom telemetry, cross-fabric load balance, lossless RDMA offloads) rather than the workload contorting to the switch.

## Q100: Does a modern data center still need spanning tree — how would you design an L2 fabric without STP?

**A:** Not in the L3-everywhere fabric: spine-leaf with routed ports everywhere (every switch-to-switch link is L3 ECMP, no VLAN bridge between switches) has acyclic topology by construction — no STP needed for loops, you get fast ECMP convergence and zero broadcast domains to maintain. L2 services (VXLAN/EVPN) provide "VLAN-like" semantics as overlay, with broadcast suppressed at the edge — STP's reason for existing is eliminated.

Where STP is still indicated: transparent ends-of-fabric or dual-homed hosts without overlay, backward-compatible gear, and some access-layer switch-to-switch extension where you refuse L3. In those islands, you still run MST/RPVST+ + BPDU Guard + filtering, but you should cap the island's size or convert.

The architecture you would design: leaf-spine, eBGP or OSPF underlay, VXLAN/EVPN overlay, anycast gateway, per-VLAN. If forced (dual-homed access/legacy host), MLAG/vPC at the pair to present one L2 path, STP as emergency net, bounded BPDUs to kill loops in minutes, plus loop-free guarantees. The senior synthesis: STP is a last-resort safety net for L2, not a design feature — the two levers that kill it are routing everywhere and control-plane-learned L2 (EVPN). Future-forward answer: place failure domains at L3, give tenants L2 via VNI, and reserve STP for the shrinking islands of transparent bridging that lack a routed alternative.
