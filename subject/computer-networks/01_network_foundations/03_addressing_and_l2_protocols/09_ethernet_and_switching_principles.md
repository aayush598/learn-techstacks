# Ethernet and Switching Principles — 100 Interview Q&A

## Q1: What is Ethernet and what role does it play in modern networking?

**A:** Ethernet is the dominant family of wired local-area network technologies defined by the IEEE 802.3 standard. It specifies both the physical signaling (cables, connectors, encoding) and the data-link-layer frame format that lets devices on a broadcast domain communicate. It evolved from Robert Metcalfe's coaxial shared-bus design at Xerox PARC into the multi-hundred-gigabit switched fabric used in every data center and campus today, while the fundamental frame structure has stayed remarkably stable.

In practice, modern Ethernet almost always runs full-duplex switched point-to-point links, which removed the shared-medium collision domains that the original CSMA/CD access method was built to manage. CSMA/CD is still formally defined for 802.3 backward compatibility, but no production network invokes it. Today Ethernet spans 2.94 Mbps business prototypes to 400 Gbps and 800 Gbps per-port standards across copper, multimode fiber, and single-mode fiber.

Architecturally, Ethernet sits at Layer 2 (data link) of the OSI model, above the physical layer and below the network layer. It is responsible for hop-by-hop delivery within a single segment using 48-bit MAC addresses. Any discussion of switching, VLANs, spanning tree, or link aggregation is fundamentally a discussion about how Ethernet frames are learned, filtered, and forwarded — which is why Ethernet is the foundation of networking knowledge.

## Q2: Describe the Ethernet frame format in detail.

**A:** An Ethernet II (DIX) frame begins with a 7-byte Preamble and a 1-byte Start Frame Delimiter (SFD), which provide bit-clock synchronization and are not counted as part of the frame. The next field is the 6-byte Destination MAC Address, followed by the 6-byte Source MAC Address. If IEEE 802.1Q VLAN tagging is used, a 4-byte tag is inserted after the source address containing a 12-bit VLAN ID and a 3-bit priority (PCP) used for QoS.

The 2-byte EtherType/Length field follows the address fields. If the value is 1500 or below it historically meant payload length (802.3 raw framing); if it is above 1500 it identifies the encapsulated protocol — 0x0800 for IPv4, 0x86DD for IPv6, 0x0806 for ARP, 0x8100 for 802.1Q, 0x8847 for MPLS. The Data/Payload then spans 46 to 1500 bytes; payloads smaller than 46 bytes are padded so the total frame is at least 64 bytes.

Finally, a 4-byte Frame Check Sequence (FCS) holds a CRC-32 computed over the frame from Destination MAC through the payload. Receivers recompute the CRC and silently discard mismatched frames. Maximum standard frame size is 1518 bytes (1522 with a single VLAN tag, 1526 with QinQ). This layout is why Ethernet expands capacity through speed and per-port density rather than frame changes: the header is fixed and understood by every device on the wire.

## Q3: What is a MAC address and how is it structured?

**A:** A MAC address is a 48-bit (6-octet) identifier assigned to a network interface. The first 24 bits are the Organizationally Unique Identifier (OUI) issued by the IEEE Registration Authority to a vendor; the last 24 bits are vendor-assigned, ideally unique per interface. This globally unique burned-in address is the EUI-48 format used as the source and destination fields in Ethernet frames.

Two bits in the first octet carry special meaning. The least-significant bit (b0) is the Individual/Group bit: 0 means unicast (a single interface), 1 means multicast or broadcast (a group). The second bit (b1) is the Universal/Local bit: 0 means globally assigned, 1 means locally administered (typical for virtualization, testing, or privacy). A MAC of all 1s (FF:FF:FF:FF:FF:FF) is the broadcast address; 01:00:5E:xx:xx:xx is the IPv4 multicast range.

EUI-64 extends a MAC to 64 bits by splicing in 0xFFFE, used for IPv6 link-local and SLAAC addresses. Privacy extensions additionally randomize the interface identifier to prevent device tracking. But regardless of format, the Layer 2 switching plane always keys its forwarding decisions on the 48-bit MAC; the extended formats only appear at Layer 3 and above.

## Q4: What is CSMA/CD and why is it no longer relevant in switched Ethernet?

**A:** Carrier Sense Multiple Access with Collision Detection was the media-access method for half-duplex, shared-medium Ethernet. Each station listened for a quiet wire (carrier sense), transmitted, monitored for simultaneous energy (collision detection), and on detecting a collision emitted a jam signal and applied a truncated binary exponential backoff before retrying, giving up after roughly 16 attempts. This arbitration is what made a shared bus safe for many transmitters.

The 64-byte minimum frame exists precisely because of CSMA/CD. On a maximally configured 10 Mbps thick-coaxial segment, the round-trip propagation delay was about 51 microseconds, corresponding to 512 bits. A sender still transmitting at the moment the collision signal returns can detect and retry; a shorter frame would complete before the collision was known, so the sender would wrongly believe delivery succeeded.

Switched, full-duplex Ethernet removed the shared medium. Every port is a separate collision domain, and each link carries independent transmit and receive pairs, so two stations can never interfere with each other's signals. With no possible collision, CSMA/CD is never invoked — the feature exists mainly for legacy half-duplex hub environments. This elimination of collisions is exactly why Ethernet could scale from 10 Mbps to 400+ Gbps: speed lost to arbitration became pure payload bandwidth.

## Q5: What is the difference between half-duplex and full-duplex Ethernet?

**A:** Half-duplex mode allows either transmission or reception at a given instant, but not both, because the medium is shared or treated as shared. It relies on CSMA/CD to arbitrate access, and effective throughput is a fraction of nominal link speed due to collisions, backoffs, and inter-frame gaps. Half-duplex was required whenever multiple stations shared a bus or attached via hubs, and it is essentially obsolete in modern infrastructure.

Full-duplex mode permits simultaneous transmit and receive over a dedicated point-to-point link, effectively doubling aggregate bandwidth and eliminating collisions entirely. A switch port and a NIC connected full-duplex can exchange data in both directions concurrently; CSMA/CD is disabled. Full duplex requires both ends to negotiate the same mode and requires a switch as the peer (a hub-to-NIC link is inherently half-duplex).

Auto-negotiation (IEEE 802.3u) lets each side advertise speed and duplex and then lock onto the highest common capability. A classic failure is hardcoding one end to full-duplex while the other auto-negotiates: the negotiating side detects no Fast Link Pulses and falls back to half-duplex, producing a duplex mismatch with late collisions and CRC errors. The rule for troubleshooting is simple: never hardcode one side only — either auto-negotiate both ends or hardcode both identically.

## Q6: What is auto-negotiation and how does it work?

**A:** Auto-negotiation, defined in IEEE 802.3 Clause 28, is the process by which two directly connected Ethernet devices advertise their speed and duplex capabilities and select the highest-performance common mode. It uses bursts of Fast Link Pulses (FLPs) that encode a 16-bit Base Page listing capabilities — 10BASE-T half/full, 100BASE-TX half/full, and pause support — with an Extended page for 1000BASE-T and faster capabilities.

During negotiation each side transmits FLP bursts while listening; once both have exchanged and acknowledged pages, each compares advertised abilities and chooses the highest common denominator. Two devices supporting only up to 100 Mbps will lock at 100 Mbps full duplex even if one end could technically reach 1 Gbps with a different peer. The whole exchange completes in under a second and also handles clock master/slave selection at Gigabit speeds.

Auto-negotiation also implements parallel detection: if one end only sends plain link pulses (a legacy non-negotiating 10 Mbps device), the other end recognizes a lower-speed partner and configures accordingly. Because parallel detection cannot sense duplex, the negotiated mode defaults to half-duplex — the origin of hardcoded/auto duplex mismatches. Best practice in all production environments is to leave both ends on auto-negotiate, which manages speed, duplex, and cable quality issues automatically.

## Q7: What is the role of the Frame Check Sequence in Ethernet?

**A:** The Frame Check Sequence is a 4-byte CRC-32 appended to every Ethernet frame, computed over the destination and source MAC, any VLAN tag, the EtherType, and the payload. The polynomial is the standard 32-bit CRC used by Ethernet (0x04C11DB7), and receivers recompute it over the received frame; a matching value means the frame is bit-error-free at the data-link layer, while a mismatch causes the frame to be silently dropped.

Ethernet deliberately performs no retransmission at Layer 2. Dropping corrupt frames is cheaper and simpler than ARQ, and reliability is delegated to higher layers such as TCP. This separation of concerns is a core Ethernet design principle: the link just moves bits fast and cheaply, and only the endpoints reconstruct reliability and ordering.

CRC-32 can detect every single-bit and double-bit error, every odd number of bit errors, and every burst of up to 32 consecutive corrupted bits; the chance of an undetected error is roughly 2^-32. Modern high-rate PHYs add forward error correction or stronger internal CRCs below the MAC, but the 32-bit FCS at the MAC layer remains the standard contract between any two Ethernet endpoints and is directly observable in packet captures.

## Q8: What are the minimum and maximum Ethernet frame sizes and why?

**A:** The minimum Ethernet frame is 64 bytes (Destination MAC through FCS; the preamble and SFD are excluded), and the maximum is 1518 bytes for an untagged frame, 1522 bytes with an 802.1Q tag, and 1526 with stacked QinQ tags. Both bounds are direct consequences of protocol mechanics rather than arbitrary choices.

The 64-byte floor is a CSMA/CD artifact: a transmitting station must still be on the wire when a collision signal returns from the farthest point of the segment. At 10 Mbps over a maximum-length repeater topology, round-trip time corresponds to 512 bits, so frames shorter than that could not reliably detect collisions. Although full-duplex switched networks never collide, the minimum persists for framing compatibility, and Ethernet implicitly relies on the 46-byte payload padding to enforce it.

The 1518-byte ceiling balances throughput against latency and buffering. Longer frames amortize headers and inter-frame gaps over more useful payload, but also demand bigger receive buffers and increase serialization delay, which hurt latency-sensitive and interactive traffic. Jumbo frames up to 9000 bytes are a non-standard extension used in storage and HPC environments, always with end-to-end support — if any hop lacks the larger MTU, frames are dropped or fragmented rather than delivered intact.

## Q9: How does a switch learn MAC addresses?

**A:** A switch learns MAC addresses passively through self-learning. When a frame arrives, the switch reads the Source MAC Address, records a mapping of that MAC to the ingress port, the VLAN ID, and a timestamp, and stores the entry in its Content-Addressable Memory (CAM) forwarding table. No configuration or advertising protocol is involved; the switch simply updates the table on every observed frame.

Each entry is temporary. A configurable aging timer (default roughly 300 seconds) deletes entries that have not refreshed, which keeps the table accurate when devices move, power off, or fail over. If a MAC reappears on a different port, the entry is overwritten to point to the new port. This aging plus relearning is what makes Ethernet plug-and-play and self-healing.

Learning operates alongside forwarding: source addresses are always learned (or refreshed), while destination addresses are looked up to choose an egress port. This bidirectional use of the same table is why CAM capacity, aging timers, and flooding behavior are the central operational concerns of switched networks.

## Q10: What happens when a switch receives a frame with an unknown destination MAC?

**A:** If the destination MAC is not present in the CAM table, the switch cannot identify the egress port, so it floods the frame to every active port in the same VLAN except the ingress port. This is called unknown unicast flooding, and it guarantees delivery without a table entry. Once the destination transmits a frame of its own, the switch learns its port and subsequent frames are delivered directly.

Flooding is a deliberate trade of bandwidth for correctness. It is unavoidable in a self-learning model, because the first frame in either direction necessarily arrives before any learning occurred. In a healthy network, flooding is rare: it occurs primarily for broadcast, multicast, ARP resolution bursts, and destinations that have been silent long enough to age out of the table.

Excessive flooding is a diagnostic signal. It typically indicates an oversized broadcast domain, an undersized CAM table, over-aggressive aging timers, or devices that rarely transmit but receive often (backup targets, printers, sensors). Fixes include splitting VLANs, tuning aging timers, adding static entries for silent critical devices, and enabling storm control to cap unknown-unicast rates.

## Q11: How are broadcast and multicast frames forwarded by a switch?

**A:** Broadcast frames carry destination MAC FF:FF:FF:FF:FF:FF and are forwarded out every port in the ingress VLAN except the ingress port, regardless of the CAM table contents. This is intentional because broadcast underpins ARP, DHCP, and common discovery protocols: every host in the broadcast domain must see those frames, so flooding them is the correct semantic.

Multicast frames are similar by default. Without multicast awareness, a switch treats multicast MAC destinations as groups to flood to the whole VLAN, because it cannot know which ports contain interested receivers. That approximation is wasteful: an IPTV stream addressed to a multicast group is delivered even to switches and hosts that never subscribed.

IGMP snooping fixes this by observing IGMP membership reports and mapping multicast groups to specific ports. With snooping enabled, the switch forwards multicast frames only to ports that have active group members plus the multicast router port. Snooping converts multicast from a broadcast-equivalent, bandwidth-destroying behavior into the efficient one-to-many delivery model multicast was designed for, and it is standard practice on every managed switch.

## Q12: What is a forwarding database and how does a switch use it?

**A:** The forwarding database, or MAC address table, is the CAM-resident map of learned and configured MAC addresses to ports and VLANs. Each entry stores the MAC, the ingress port, the VLAN, and an age timestamp, along with static/dynamic classification. Lookups are hardware-accelerated in Content-Addressable Memory, yielding O(1) decisions measured in nanoseconds.

On arrival, a frame's destination MAC is looked up. A match yields the exact egress port, and the frame is forwarded there only. A miss triggers flooding. If the match equals the ingress port, the frame is discarded as redundant — the destination is reachable on the same segment and forwarding would loop it back. Source learning updates the table every frame regardless of the destination decision.

CAM capacity is finite and platform-specific, from a few thousand entries on small switches to hundreds of thousands on data-center equipment. Because a full table forces flooding of every unknown destination, CAM sizing, port security (which caps per-port learnings), and VLAN segmentation (which shrinks the address set per domain) are all operational levers that protect switch performance.

## Q13: Explain broadcast domains and how switches relate to them.

**A:** A broadcast domain is the set of devices that receives every broadcast frame transmitted by any member of the set. By default, all ports on a plain Layer 2 switch participate in the same broadcast domain — a broadcast on one port floods to all others. Broadcast domains are bounded by Layer 3 boundaries: routers and routed switch interfaces do not forward Layer 2 broadcasts, so they separate domains.

Broadcast traffic is not waste; ARP, DHCP, and discovery protocols require it. The problem is scale. Every broadcast forces every host to interrupt its CPU and inspect a frame not meant for it, and broadcast storms can saturate links and switches. Broadcast domain size is therefore a primary network design variable.

VLANs are the tool for shaping broadcast domains: each VLAN is an independent broadcast domain, so segmentation by function or security level contains broadcast radiation. Inter-VLAN traffic is routed at Layer 3 rather than flooded. The essential network-design duality — the same switch both creates broadcast domains (one per VLAN) and breaks them apart with VLAN IDs and routing — is central to any senior conversation about segmentation, security, and performance.

## Q14: How does the Spanning Tree Protocol prevent loops?

**A:** STP builds a loop-free logical tree over a physically redundant mesh by electing one switch as the Root Bridge and driving every other switch to compute the single least-cost path toward it. Redundant alternate paths are placed in blocking state. The result is that between any two devices there is exactly one active Layer 2 path — the tree — while every backup link silently waits.

Switches exchange Bridge Protocol Data Units (BPDUs) carrying the Root Bridge ID, the sending bridge's path cost to the root, and the sending bridge ID. Every switch compares received BPDUs and keeps the best: the one advertising the lowest-cost route to the root. This best-path information determines root ports (the switch's path toward the root) and designated ports (the segment's path toward the root); non-winning ports become blocking (alternate/backup).

If the topology changes — a link fails or a switch is added — BPDUs reveal the change, the tree is recalculated, and blocked ports may transition to forwarding. The original 802.1D converged in 30–50 seconds because it relied on timers; RSTP (802.1w) replaced timers with an active proposal/agreement handshake, converging in a second or less, proving that loop prevention and speed are compatible.

## Q15: What are the STP port states?

**A:** Original 802.1D defines five port states. Disabled means the port is administratively down and neither sends BPDUs nor forwards data. Blocking is the dormant state for loop-prevention: the port listens for BPDUs but does not forward data or learn MAC addresses. Most redundant ports live in blocking, providing failover capacity.

Listening and Learning are transitional states entered when a port wins root or designated role. In Listening, the port exchanges BPDUs but still blocks data and does no MAC learning; this window lets the topology stabilize before forwarding begins, avoiding transient loops. In Learning, data is still blocked, but the switch now populates its CAM table from incoming frames, so that when forwarding starts the database is already warm and flooding is minimized.

The final, per-state Forwarding state is where data and MAC learning proceed normally. The forward-delay timer (default 15 seconds) governs how long the port sits in Listening and in Learning, which is why classic STP takes 30 seconds to move a port from Blocking to Forwarding on its own initiative. RSTP collapses these states into three (discarding, learning, forwarding) and drives transitions with handshakes instead of timers.

## Q16: What is the Root Bridge and how is it elected?

**A:** The Root Bridge is the switch that anchors the spanning tree: it is the only switch with no root port, and every other switch computes its tree path relative to it. All forwarding decisions ultimately favor paths toward the root, which makes root placement a first-order design decision: the logical center of the network should be a well-connected, high-capacity switch.

Election is deterministic and automatic. Every switch sends BPDUs that carry its Bridge ID — a 2-byte configurable priority (default 32768) combined with its 48-bit MAC. The switch with the lowest Bridge ID wins the root. With identical default priorities, the tie is broken by MAC address, so without configuration the root is effectively a coin flip weighted by MAC value. That usually lands on an access-edge switch, which is operationally poor.

Administrators therefore pin the root explicitly. Set the priority of the chosen core/distribution switch very low (e.g., 0 or 4096 via `spanning-tree vlan <id> root primary`) and a redundant peer slightly higher (secondary). Doing so makes root placement deterministic, keeps the logical tree centered on the strongest hardware, and prevents a low-cost access switch from silently becoming the bottleneck that all traffic is forced to traverse.

## Q17: What are the STP port roles?

**A:** STP distinguishes port roles from port states. The Root Port is the single port on a non-root switch that provides the least-cost path toward the Root Bridge; it is always forwarding and is the switch's only uplink to the tree's center. Root Port selection uses cost first, then the upstream bridge ID, then upstream port priority, then port index as tiebreakers.

A Designated Port is the segment's best path toward the root — there is exactly one per LAN segment, and it is forwarding. On a segment shared by two switches, the switch advertising the better path owns the designated port; the neighbor's port therefore cannot be designated and is blocked. The Root Bridge, being best for every segment it touches, holds designated ports on all its links.

Alternate and Backup are the non-forwarding roles that provide redundancy. An Alternate Port offers a valid alternative path to the root (it could replace a failed root port), while a Backup Port offers redundancy for a designated port on the same segment. RSTP leverages these roles for fast failover: an alternate port can take over a failed root port in milliseconds without recalculating the tree, which is the mechanism behind sub-second RSTP convergence.

## Q18: What is the difference between STP, RSTP, and MSTP?

**A:** Classic STP (802.1D) runs a single spanning tree instance for the entire bridge and VLAN set, converges in 30–50 seconds via timer-driven transitions, and wastes redundancy: a blocked link is blocked for every VLAN. RSTP (802.1w) keeps one instance but replaces timers with proactive proposal/agreement handshakes, collapses state to discarding/learning/forwarding, introduces alternate/backup roles, and converges in about a second. It also handles edge ports natively for instant host connectivity.

MSTP (802.1s) generalizes RSTP by letting a network run multiple spanning tree instances, each carrying a configured subset of VLANs. VLANs mapped to different instances can use different active paths, enabling active/standby traffic engineering — instance 1 uses link A, instance 2 uses link B — that a single instance cannot express. This is the pragmatic enterprise answer to both STP's wasted bandwidth and PVST+'s N-instance overhead.

MSTP groups switches into regions defined by an identical configuration (region name, revision, and VLAN-to-instance mapping); mismatched regional configuration silently splits the tree and can create substantial forwarding churn. Between regions a single Common and Internal Spanning Tree (CIST) organizes the inter-region topology. Choosing among the three means answering: how fast must convergence be, how many redundant links matter, and how much VLAN-aware path selection do I need?

## Q19: What is port security and what are its violation modes?

**A:** Port security restricts which MAC addresses may transmit on a switch port, primarily to stop CAM-table flooding and unauthorized device attachment. The administrator sets a maximum count of MAC addresses per port; addresses are learned dynamically, learned and pinned (sticky), or explicitly pre-statically configured. Any traffic from a disallowed address beyond the cap is a violation.

The three violation actions differ in severity. Protect silently drops offending frames while leaving the port up and authorized traffic flowing. Restrict behaves like Protect but increments a violation counter and emits a syslog/SNMP alert, giving visibility. Shutdown — the default on Cisco platforms — immediately places the port into err-disabled state, severing connectivity until an administrator (or automatic recovery) restores it.

Shutdown is the strongest defense and is appropriate for user-facing access ports, where an extra device is almost always unauthorized. Sticky learning, which bakes the first-seen MAC into the running config, prevents a device swap from silently changing which address is trusted. A common baseline is max-addresses 1 plus sticky on desktop access ports, protecting both the CAM table and the presumption of a single known endpoint.

## Q20: What is a VLAN and how does it relate to switching?

**A:** A Virtual Local Area Network is a logical partition of Layer 2 on managed switches: ports are assigned to VLANs so that devices share connectivity and broadcast isolation regardless of physical location. Each VLAN is its own broadcast domain, and frames in VLAN 10 cannot reach VLAN 20 without a Layer 3 device, which is exactly why VLANs produce both security and performance benefits versus one giant flat LAN.

The same physical switch can carry hundreds of VLANs simultaneously. Traffic between VLANs — for example between an Engineering and a Finance subnet that share a switch — must be routed, either by a router on a stick or by Layer 3 switch VLAN interfaces (SVIs). This separation confines broadcasts, isolates failures, and lets administrators enforce policy per group of users without rewiring.

802.1Q tagging lets a single link carry many VLANs by inserting a 4-byte tag (with a 12-bit VLAN ID, so up to 4094 usable VLANs) into each frame. Trunk ports carry tagged multi-VLAN traffic between switches and routers; access ports deliver untagged single-VLAN traffic to hosts. The native VLAN, which travels untagged on a trunk, is where misconfiguration causes VLAN leaks and is a classic security surface.

## Q21: What is the difference between a Layer 2 switch and a Layer 3 switch?

**A:** A Layer 2 switch forwards based on MAC addresses within a VLAN. It learns the CAM tables, floods unknown unicast, and cannot move packets between subnets: inter-VLAN traffic must hairpin through an external router. It is simpler, cheaper, and ideal for access ports and pure L2 domains, but it presents a routing bottleneck whenever VLANs actually need to exchange traffic.

A Layer 3 switch adds hardware-based IP routing. It creates IP-addressed virtual interfaces (SVIs) per VLAN, or routed ports, and forwards between them at wire speed using TCAM-backed longest-prefix-match lookups. Wire-speed inter-VLAN routing is the practical reason enterprises collapse the distribution layer: routing in hardware eliminates the router hairpin that otherwise halves inter-VLAN throughput and doubles latency.

The two overlap in practice: most modern access-layer devices route; most so-called routers switch in hardware. The distinction that still matters is functional placement — which device terminates broadcast domains and subnets, and whether the forwarding plane works on MACs, IPs, or both. A senior answer therefore frames this as an architecture decision, not a vendor category: "Layer 3 switching" is how you scale inter-VLAN bandwidth beyond a shared router.

## Q22: What is a MAC address table overflow attack?

**A:** A CAM overflow (MAC flooding) attack floods a switch with frames carrying random spoofed source MAC addresses. Self-learning dutifully consumes CAM entries for each new source, so the table fills to capacity. Once full, the switch can no longer learn legitimate addresses — every unknown destination is flooded to all ports in the VLAN, and every legitimate host's entry may be displaced and re-flooded.

The attacker's win is promiscuity: because the switch now floods unknown unicast, frames intended for specific victims are delivered to the attacker's port, enabling sniffing of traffic that should have been unicast. Secondary damage is chaos: legitimate devices experience intermittent connectivity, their frames wandering the full broadcast domain instead of being delivered point-to-point.

Defenses target the root mechanism. Port security caps how many MACs a single port can contribute, storm control rate-limits new-sourced traffic, and aggressive CAM aging shortens the attacker's memory footprint. Segmenting VLANs shrinks both the blast radius and the practical table pressure. Modern detection logic watches per-port source-MAC rates and flags the characteristic surge, allowing automated containment before the table saturates.

## Q23: What is 802.1Q VLAN tagging?

**A:** IEEE 802.1Q is the standardized mechanism for carrying VLAN membership on Ethernet. It inserts a 4-byte tag between the Source MAC and the EtherType: a 2-byte Tag Protocol ID (TPID) fixed at 0x8100, plus a 3-bit Priority Code Point (PCP) for COS marking, a 1-bit Drop Eligible Indicator (DEI), and a 12-bit VLAN ID (VID). The tag effectively grows every frame on a trunk by 4 bytes, which is why MTU and max-frame calculations must account for it.

Trunks insert tags for each frame's VLAN so the far-end switch can forward into the correct domain; access ports strip the tag and forward untagged into their configured VLAN. The native VLAN is the special case — its frames cross a trunk untagged — and native VLAN mismatch is a primary source of "traffic appears in the wrong VLAN" incidents. 802.1Q also reserves rules: VLANs 0 and 4095 are reserved, 1 is the default/management-serving VLAN, 1002–1005 map to legacy FDDI/Token Ring, and VLAN ID range divisibility varies by platform.

QinQ (802.1ad) stacks an outer 802.1ad tag over an inner 802.1Q tag, literally multiplying available tag space and letting a service provider carry many customer VLANs over a single trunk with an S-VLAN encapsulation. The IP-multicast and MAC ranges are untouched by tagging; the tag only affects frame size and the position of the EtherType and payload.

## Q24: What is the difference between access ports and trunk ports?

**A:** An access port belongs to exactly one VLAN and carries that VLAN untagged. It is how a switch faces end devices — PCs, printers, phones, APs — that have no VLAN awareness. Incoming frames are assigned to the port's configured access VLAN; outgoing frames are untagged. Access ports are also where port security, DHCP snooping, 802.1X, and BPDU Guard are typically layered because they face untrusted endpoints.

A trunk port carries multiple VLANs simultaneously using 802.1Q tags, connecting switches to switches, switches to routers, or switches to VLAN-aware servers/hypervisors. Configuring a trunk means describing which VLANs may traverse it (allowed VLAN list) and which VLAN is native (untagged). One physical pair of wires thus carries many logical broadcast domains, which is how scaling VLAN architecture beyond a single switch works.

The operational dangers cluster around permissive defaults. A trunk that allows all VLANs extends every broadcast domain across the whole network; an access port left in dynamic trunking mode can be negotiated into undesired trunking; and native-VLAN ambiguity can cause cross-VLAN leak. Senior engineers treat trunk access lists and disabled DTP as mandatory hygiene, not options.

## Q25: What is ARP and how does it resolve an IP to a MAC address?

**A:** Address Resolution Protocol is the Layer 2/3 glue protocol: given an IPv4 address within the local subnet, ARP returns the 48-bit MAC used to encapsulate frames to that address. Every IPv4 host keeps an ARP cache (IP to MAC, with TTL) and consults it before every unicast send. A cache miss requires an ARP Request broadcast ("who-has 10.1.2.3") to every host in the broadcast domain.

Only the host that owns the target IP responds, with a unicast ARP Reply carrying its MAC. The requester inserts the mapping into its cache and proceeds. The process is on-demand and completely dynamic: no pre-seeding, no configuration, no hierarchy — the protocol solved the "flat layer 3 to flat layer 2" mapping problem for an entire addressing generation, and it still does.

The security consequence is structural. ARP is stateless and unauthenticated, so any host may send unsolicited replies ("I own the gateway IP") — ARP spoofing — hijacking another host's traffic. The effect is a man-in-the-middle at the link layer that IPsec or TLS at higher layers must detect otherwise. Defenses include Dynamic ARP Inspection with DHCP-snooping binding tables, static ARP for critical infrastructure, and IPv6's NDP/SEND alternative, which replaces the broadcast model with multicast and adds cryptographic protections.


## Q26: How do unicast, broadcast, and multicast forwarding differ?

**A:** Unicast forwarding delivers a frame to exactly one destination by using the CAM table: a hit forwards to the mapped egress port, a miss floods. Broadcast forwarding sends to every port in the VLAN regardless of the table — mandated by protocols like ARP and DHCP that need universal visibility. Multicast forwarding sends to an identified group; absent multicast awareness (IGMP snooping), it is treated as broadcast to the whole VLAN.

Any port carrying all three needs distinct behaviors: the MAC multicast range 01:00:5E:xx:xx:xx maps to IPv4 multicast groups, and IGMP snooping maps those groups to the subset of ports with interested receivers. The expense of broadcast/multicast flooding is one of the main pressures that forces VLAN and subnet design, while multicast-aware snooping makes streaming and rendezvous protocols efficient at scale.

From a forwarding-plane standpoint the differences are critical: unicast is bandwidth-conserving and generates switch ASIC lookups, broadcast is protocol-mandated and inherently expensive, and multicast is optional — correct but cheap only if the switch monitors membership. A switched network that ignores group traffic either floods millions of streams or breaks rendezvous protocols entirely.

## Q27: What is flow control in Ethernet?

**A:** IEEE 802.3 PAUSE frames implement link-level flow control: a congested receiver that is about to overrun buffers transmits a PAUSE frame requesting its peer to stop sending for a specified number of time quanta (512-bit units). This gives the receiver time to drain queues. PAUSE is a MAC-layer mechanism that pauses the whole link regardless of traffic class or upper-layer protocols.

The problem with PAUSE is its breadth: it pauses TCP too, even when the congestion is local (the switch buffer) rather than end-to-end. Because TCP interprets pauses or losses as congestion and shrinks its window, unconstrained PAUSE can strangle throughput in data centers. This is why modern environments limit PAUSE to specific classes rather than the whole link.

Priority Flow Control (PFC, 802.1Qbb) expands PAUSE to run per-priority-class. A switch can pause only the storage traffic class (e.g., FCoE / RDMA) while leaving data-class flows running, enabling lossless delivery for latency-critical protocols. For senior-level answers, the key insight is that arbitrarily dropping frames is often better than pausing — PAUSE/PFC create head-of-line-blocking and are tuned per-class, never blindly enabled across a fabric.

## Q28: What is an EtherChannel or Link Aggregation Group?

**A:** Link Aggregation (IEEE 802.3ad / 802.1AX) bundles two or more physical links between the same pair of devices into a single logical link, the Link Aggregation Group (LAG). Bundling multiplies aggregate capacity — four 1-Gbps links yield roughly 4 Gbps — while STP sees the bundle as one port, eliminating the wasted standby link that redundant physical paths otherwise suffer. Traffic distributes across members via a hash of header fields.

Distribution is flow-based, not packet-based: a hashing function (typically over source/destination MAC, IP, and L4 ports) deterministically assigns each flow to one member link, which preserves packet ordering within a flow. Consequently no single flow can exceed the bandwidth of one member; the aggregate benefit comes from scaling the number of flows, not making one flow faster.

LACP (802.3ad) automates the negotiation: each side exchanges LACP PDUs and both enforce the same member set, adding/removing links dynamically. Without LACP, a static LAG still works but provides no peer discovery and silently misbehaves if the far end disagrees. Load-balance hashing choice matters more at scale than people expect: an address-pair hash can pile all traffic onto one member, turning intended redundancy into a lopsided bottleneck.

## Q29: What are the differences between cut-through and store-and-forward switching?

**A:** Store-and-forward buffers the entire frame, validates the FCS, and only then forwards. Corrupt and runt frames never leave the switch, at the cost of latency roughly proportional to frame size (about 12 microseconds for a 1500-byte frame at 1 Gbps). Cut-through decides at the Destination MAC (the first few bytes), forwarding almost immediately, and never checks the FCS — so bad frames propagate downstream.

Cut-through's latency advantage is real for HPC, storage networks, and latency-sensitive trading: saving the full-frame buffer stage can be microseconds per hop and much more on oversubscribed links. The error-cost downside is that a cable fault or electrical interference generates a flood of corrupt frames that now consume downstream bandwidth and CPU until the source-adjacent switch drops them.

Fragment-free (cut-through after 64 bytes) is a hybrid that still avoids forwarding most collision fragments. Most modern enterprise/data-center switches default to store-and-forward, since ASIC buffering has closed much of the gap and integrity matters more than the last microsecond. The choice is therefore an operational one: whether a packet arriving just-out-of-integrity is acceptable against a guarantee of no software or mac-layer retries.

## Q30: What are the differences between a hub, a switch, and a router?

**A:** A hub is a Layer 1 multiport repeater: it retransmits incoming bits out every other port, forming one collision and one broadcast domain. It does not read frames, cannot learn addresses, and does not isolate traffic — throughput is shared across all ports and protected only by CSMA/CD. A switch is a Layer 2 device that reads frames, learns per-port MACs, forwards selectively, and creates a separate collision domain per port; broadcasts still propagate across the whole VLAN.

A router is a Layer 3 device that makes decisions on IP addresses and network-layer reachability. It terminates broadcast domains rather than forwarding their broadcasts, maintains a routing table (learned statically, via protocols, or from an SDN controller), and passes packets toward their destination hop by hop. Routers also apply ACLs, NAT, and QoS on the network layer boundary.

The overlap is real: Layer 3 switches route in hardware and routers switch in hardware. But the distinguishing roles matter for design: hubs have no place in modern data paths, switches scale flat L2 forwarding, and routers scale inter-subnet reachability, policy filtering, and WAN/Internet attachment. A senior architect reaches for whichever device matches the boundary being crossed.

## Q31: What is a VLAN trunk and how is it configured?

**A:** A trunk is a single link that carries multiple VLANs by encapsulating each frame with a 802.1Q tag on the wire. It interpolates VLAN membership between devices: switches, routers, and VLAN-aware servers all connect via trunks. Trunk configuration sets the encapsulation (802.1Q), the allowed VLAN list — restricting which domains can traverse — and the native VLAN.

The practical configuration on a port: choose the mode as trunk, specify which VLANs are allowed (`switchport trunk allowed vlan <list>`), and set the native VLAN to the same untagged VLAN on both ends. Linux/VMware/ESXi trunk terms are "tagged VLAN" and "native," while Cisco calls the untagged VLAN "native." Mismatched trunk parameters produce silent VLAN leakage or unreachable devices — the classic native-VLAN mismatch.

Security posture matters as much as connectivity: DTP (Dynamic Trunking Protocol) can make an access port say yes to a rogue device's trunk request; disabling it (`switchport nonegotiate`) hardens the port. In a campus network, every trunk's allowed list should be pruned to the VLANs that actually need the path, which keeps broadcast domains bounded and failure domains small.

## Q32: How is inter-VLAN routing implemented?

**A:** Inter-VLAN routing moves packets between different Layer 2 broadcast domains (VLANs) by treating each VLAN as its own subnet at Layer 3. The classic hub-and-spoke arrangement is "router on a stick": a single physical router link is split into subinterfaces, one per VLAN, each tagged with its VLAN ID; the router pivots packets between tagged subinterfaces. A switch trunk carries the tagged frames to the router.

A Layer 3 switch simplifies this by giving each VLAN an IP address on a virtual interface (SVI) and routing between them directly in silicon. This is the de facto campus and data-center pattern — routing close to the access layer with no external router needed, at wire speed, with ACLs applied per VLAN boundary. The same SVI design underpins default-gateway behavior: hosts in VLAN X use their SVI as the gateway to reach VLAN Y's subnet.

An alternative is routed access (a "routed edge" with each access switch holding its own Layer 3 gateway and terminating VLANs on the switch itself), eliminating the router-on-a-stick bottleneck at the cost of flatter L3 addressing. For a senior answer, inter-VLAN routing is a placement decision: where is the routed boundary, is it in hardware, and does the design keep broadcast domains small and recovery deterministic?

## Q33: What is VTP and why do many enterprises disable it?

**A:** VLAN Trunking Protocol (VTP) is Cisco's protocol for propagating VLAN database changes across a switch domain. A VTP server creates/deletes/renames VLANs, and clients within the domain adopt the server's VLAN database automatically, simplifying provisioning on dozens of access switches. The danger is that the same automation that saves time also propagates mistakes.

VTP version 2/3 introduced revision-number guards and improved scaling, yet the core risk remains: a switch with a higher revision number can overwrite the domain's VLAN database, and a mis-keyed deletion can wipe every VLAN on every switch reachable in the domain. The failure mode is both violent and silent until traffic stops.

Consequently, most security-minded enterprises disable VTP (mode transparent/off) and manage VLAN definitions out-of-band with automation (Ansible, NetBox/declarative config). For a senior answer: VTP is a helpful but risky convenience; the modern default is no protocol-synchronized state, deterministic per-switch configuration, and continuous validation — precisely because Layer 2 failures are both wide and hard to debug when they originate as a one-line change.

## Q34: What is PortFast (edge) and how does it relate to BPDU Guard?

**A:** PortFast (or edge) tells spanning tree that a port faces an end host rather than another switch, allowing that port to leap straight to Forwarding instead of traversing 30 seconds of listening/learning. Since a host is not going to create a Layer 2 loop, waiting is pure latency. Every access port that attaches an endpoint (and its IP phone, AP, printer) should be edge.

The hazard is that a port marked edge may connect to another switch, generating a loop that STP cannot see because the port forwards immediately. BPDU Guard is the countermeasure: if any BPDU appears on an edge port, the port is placed in err-disabled state. RSTP native edge ports are the same concept.

Applying "edge + BPDU Guard," loop guard, and DHCP/DAR/IP source guard together on access ports is baseline access-hardening. A port that sees BPDUs is almost never a legitimate host, so err-disable is the right reaction: it is the network refusing to become a loop or a rogue switch's entry point. Automatic recovery via errdisable timers keeps operational cost low while preserving the safety net.

## Q35: What is Root Guard and how does it protect the spanning tree?

**A:** Root Guard is a per-port STP protection: on a root-guarded port, if a BPDU arrives that claims a better (lower) Bridge ID — which would make that port the root port toward a new root — the port is placed into a root-inconsistent state (blocking) rather than accepting the new root. Its job is to keep a pre-designated root stable against rogue or misconfigured switches joining the topology.

The mechanism is asymmetric by design: a root-guarded port may never become a root port, period. Legitimate new switches sending BPDUs to a root-guarded access port cause the port to drop to inconsistent until the offending BPDUs stop. This is different from BPDU Guard, which err-disables the entire port when any BPDU is seen; Root Guard retains the link state and recovers automatically when the superior BPDU disappears.

Deployment guidance: place Root Guard on ports toward access switches and possible loop surfaces, and accept that a downlink to a newly-joining legitimate switch will momentarily block — that is the point. The senior answer resolves around root-path integrity: root guard, in conjunction with explicit root-priority configuration, makes the root election deterministic and immune to accidental `priority 0` configuration on an edge device.

## Q36: What is Loop Guard and when would you enable it?

**A:** Loop Guard protects against a specific physical failure: a unidirectional link where a STP designated port keeps its state (sends BPDUs) but receives nothing back from the other end's root port. Because the receive path is dead, the port never learns of topology changes and may keep forwarding — producing a loop of its own through the silent segment.

Loop Guard works by detecting the absence of BPDUs on a port that should be receiving them, converting the port to a loop-inconsistent state until BPDUs resume. The condition is auto-recovers when the link regains bidirectional functionality. This complements UDLD, which detects the unidirectional link itself at the fiber level; Loop Guard observes STP behavior and is therefore more portable across switch types.

Trigger scenarios to enable it: any port between switches that could silently lose its RX path (fiber), redundant topologies where a hidden loop would be catastrophic, and access ports where an interposed hub warrants protection. Loop Guard with UDLD and root guard is the standard three-tool armory against the silent loop, and the operational cost is trivial versus debugging an invisible broadcast storm.

## Q37: What is the IEEE 802.1X port authentication model?

**A:** 802.1X (Port-Based Network Access Control) requires a device to authenticate before a port is allowed to carry user traffic. Three roles exist: the Supplicant (end-user NIC/device client), the Authenticator (the switch acting as the gatekeeper), and the Authentication Server (typically RADIUS, e.g., FreeRADIUS, Cisco ISE, Microsoft NPS). The switch ports start "unauthorized," permitting only EAPOL (Extensible Authentication Protocol over LAN) or no data.

The exchange is a RADIUS/EAP handshake: the switch relays EAP messages between supplicant and RADIUS server until the server returns Accept, Reject, or a fallback policy. On Accept, the switch marks the port authorized and applies the returned attributes — VLAN assignment, dACL, QoS. Reject leaves the port restricted to a remediation or guest VLAN. Ports can also run MAB (MAC Authentication Bypass) for devices without a supplicant, and for device+user dual authentication.

For enterprise access, 802.1X is the baseline for machine identity (certificates) and user identity (credentials), feeding dynamic VLAN/VoIP segmentation. Senior familiarity goes beyond the handshake: avoiding rogue supplicant devices, handling asymmetric VLAN assignment, RADIUS server high availability, and dynamics of dynamic ACL enforcement are all part of a complete campus access story.

## Q38: What becomes of frames with a source MAC the switch has already learned on a different port?

**A:** When a frame arrives with a source MAC that the CAM maps to a different ingress port, the switch faces a MAC move: it can either rewrite the mapping to the new port (relearn) or, with MAC move protection enabled, drop the frame and increment a counter. The correct behavior depends on legitimate vs. illegitimate movement.

Legitimate movements include laptop NIC drivers changing the source MAC, virtualization live-migrations, NIC teaming failover, and roaming endpoints. In those cases the switch should relearn instantly — slow learning would interrupt service. Illegitimate cases include a MAC spoofing attacker trying to capture a victim's traffic: by sending forged source-MAC frames, they drag the victim's mapping onto their own port, and the victim's genuine frames get dropped at the victim port.

Modern switches therefore expose "MAC move" policies and limit the number of moves per time window, along with logging that makes the pattern visible. A senior understanding: MAC move detection is both a security primitive (spoof defense) and a correctness primitive (fast relearning), and the operational design distinguishes intentional roaming/failover from hostile table poisoning.

## Q39: What is MACsec and how does it secure Ethernet at Layer 2?

**A:** MACsec (IEEE 802.1AE) provides hop-to-hop Ethernet encryption, integrity, and replay protection — directly on the wire, in the NIC/PHY, at line rate. It authenticates every frame with an ICV and encrypts the payload with AES-128/256-GCM, making a fiber tap or a malicious switch-in-the-path unable to read or modify frames. Each link is secured independently (hop-by-hop), not end-to-end.

Key establishment is handled by MACsec Key Agreement (MKA) over 802.1X/EAP (connectivity associations and secure associations). A pair of negotiated keys (Secure Connectivity Association/Key) encrypts and authenticates frames, with a pair of Secure Channel identifiers associated with the link endpoints. This is the accepted mechanism for protecting storage networks, PCI-DSS scopes, and cloud provider interconnects at Layer 2.

The senior nuance is where MACsec belongs architecturally: it protects the physical link only, so it stops passive taps and data tampering at the transport layer, but it cannot protect against a compromised switch or endpoint, and key lifecycle management is essential. Deploying MACsec to encrypt spine-leaf links and between host and ToR for sensitive tenants is a common data-center pattern, with the load carried entirely by hardware crypto engines to avoid CPU overhead.

## Q40: What is STP's role in a stacked or MLAG environment?

**A:** In a switch stack (StackWise, VSS, or similar), multiple physical chassis converge into one logical switch; STP runs as if all the member devices were one switch, and the stack presents a single root/designated role per segment. MLAG (Multi-Chassis Link Aggregation — vPC on Cisco Nexus, MLAG on Arista/Cumulus, LACP-multi-chassis elsewhere) extends the same single-LAG illusion across two separate switches.

Both eliminate the classic STP tradeoff: aggregated ports can be active across two chassis simultaneously because the pair of switches coordinate the bundle as if they shared a control plane, publishing the peer link as one MAC/hash domain. Redundant active links become usable instead of STP-blocked, and each access switch's two uplinks both forward.

The unresolved STP role then becomes secondary: MLAG plus STP coexistence requires each chassis to behave identically for STP (same Bridge ID advertisement) so the two-chassis domain looks like one root. Mismatched MLAG/STP consistency causes transient loops. The senior story is that MLAG is the modern "no STP cost" way to make L2 redundancy useful, provided coordination, control-plane state, and STP identity are coherent across the pair.

## Q41: How does a switch provide QoS at Layer 2?

**A:** Layer 2 QoS starts with the Priority Code Point (PCP): the 3-bit field in the 802.1Q tag marks frames into up to 8 classes of service (0–7), commonly CoS 5 for voice, 4 for video, 3 for call signaling, and 0 as default. Managed switches map PCP to internal queues (typically 8 hardware queues per port) and then use scheduling discipline to decide which queue drains first.

Scheduling is where value materializes: Strict Priority empties highest CoS first, guaranteeing low latency for voice but risking starvation of lower classes; Weighted/Deficit Round Robin (WRR/DWRR) gives each queue a share so no class starves. Many designs combine both — drain CoS 5/6 strictly, share the rest with weights. Bottlenecked ports forward per-queue drop policies (tail drop, WTD/WRED) to protect loss-sensitive flows.

The trust boundary matters most in practice: the switch may trust marked PCP from a phone but re-mark traffic from PCs. Attaching to IP DSCP, the switch can mark/remap per flow at admission, ensuring the fabric's CoS policy is applied where endpoints connect. The senior answer connects L2 CoS to the end-to-end QoS story: consistent marking, admission trust, queueing, and explicit drop control are all one coherent system.

## Q42: What is a SPAN/Mirroring and how is it used for visibility?

**A:** Port mirroring (SPAN on Cisco, port mirror elsewhere) copies frames from selected source ports or VLANs to a designated egress port where a packet analyzer, IDS, or recorder sits. The copy is identical to the original; the original path is unaffected. This visibility is the bedrock of troubleshooting, security monitoring, and occasionally regulatory recording.

Limitations are real: mirroring multiples the traffic and can saturate the monitor port when many 10G source ports feed a 10G analyzer; only copies of frames the switch processes are mirrored (ingress, egress, or both); and monitoring 100% of a data-center fabric by SPAN is impractical at scale, which is why flow-sampling (NetFlow/sFlow/IPFIX) complements it.

Deployment patterns include a central IDS/IPS with SPAN aggregation for campus segments, tcpdump/Wireshark on a jump host for one-off debugging, and (at scale) mirror-to-analyzer via dedicated tap points or packet brokers that fan out to multiple tools. The junior/senior split is understanding that mirroring is a sampling strategy with port and rate constraints, and that well-designed fabrics challenge mirror capacity rather than abuse it.

## Q43: What is the Ethernet Preamble and Start Frame Delimiter?

**A:** Every Ethernet frame begins with a 7-byte Preamble of alternating 1s and 0s (0x55), then a 1-byte Start Frame Delimiter (SFD) ending in 11 (0xD5). The receiver's PHY uses the Preamble to lock onto the transmitted bit clock, and the SFD's distinctive ending marks the end of preamble — precisely where the Destination MAC begins. Neither is counted in frame length or covered by the FCS.

The net effect is synchronization plus framing: without a clock recovery preamble, receivers could not sample bits reliably on older shared/half-duplex media. On modern auto-negotiated links the roles have simplified but the format is unchanged: the Receiver locks, decodes the SFD, and then consumes the MAC header.

For a senior answer, remembering the Preamble/SFD nuances matters in two contexts: calculating real line-rate overhead (7+1 bytes per frame reduce effective throughput), and understanding network analyzers that strip Preamble/SFD (they show the frame as starting at the Destination MAC). The exact bytes are latency/overhead trivia, but the reason they exist — robust symbol/bit recovery — is a genuine Ethernet-physics insight.

## Q44: What is unknown unicast flooding and when does a switch stop doing it?

**A:** Unknown unicast flooding happens when the CAM has no entry for a destination MAC: the switch sends the frame out every port except the source port, in the same VLAN. It is how the switch guarantees delivery before it knows a neighbor, and it is the observable cost of self-learning. Flooding ends as soon as the destination transits the network (its source learning generates the CAM entry) or the administrator adds a static entry.

The rate of flooding is therefore a direct function of CAM miss rate: distances, silent destinations (drains, printers, sensors), high host counts, and aggressive aging all raise it. Unicast flooding is traffic that has been broadcast to everyone and is bandwidth-wasteful; storm control lets a switch rate-limit it, and a healthy design keeps the flood rate near zero.

Architecturally, flooding is one of the reasons "flat L2" scales poorly: as MAC table pressure and silent-destination rates rise, floods consume link capacity that unicast routing would not. Senior designs tune aging, segment VLANs, and use multicast/EVPN control-plane learning rather than flood-and-learn when scaling beyond a campus.

## Q45: What is the role of EtherType in a frame?

**A:** EtherType is a 2-byte field comprising either the length of the payload (for IEEE 802.3 raw framing, value under 1500) or the protocol identifier of the encapsulated payload (value over 1500). It is how a receiver knows whether the payload is IPv4 (0x0800), IPv6 (0x86DD), ARP (0x0806), VLAN-tagged (0x8100), MPLS (0x8847), LLDP (0x88CC), or a host of others.

Multiplexing at Layer 2 is exactly this: the same Ethernet link carries many network-layer protocols, and EtherType demultiplexes them without a length-prefix protocol. The value 0x0800/0x86DD being over 1500 is our cue that the length-over-1500 convention is a 802.3 design relic; payload type, not payload length, is what L3 cares about.

For a senior answer, EtherType matters in several practical places: hardware decoders (ASIC/TCAM matching on EtherType to steer frames to routing, bridging, or special processing), jumbo frame calculation (VLAN tag shifts the Offset of EtherType), and security rules that filter by EtherType as a weak "protocol allowlist." The field is part of the fixed header that all parsing logic assumes.

## Q46: What is the role of a VLAN in multicast and how does it affect snooping?

**A:** Without VLAN isolation, a multicast stream addressed to a group floods every port in every segment (or is forwarded by IGMP snooping per VLAN). VLANs make multicast group membership VLAN-scoped: membership and queries are per-VLAN. IGMP snooping inspects membership reports per VLAN and builds per-VLAN multicast forwarding state; the group table is a mapping of (VLAN, group) to the ports that subscribed.

Since snooping consults VLAN boundaries first, a stream destined for VLAN 10 only reaches ports in VLAN 10. This is both feature and hazard: an administrator who forgets to configure a mrouter port or who never throws a querier in a new VLAN can make multicast transparently fail (snooping sees no query, so it may flood or black-hole depending on platform behavior).

The practical consequence is that multicast support and VLAN design are interdependent: each VLAN needs a querier (usually the router of that VLAN), mrouter ports on trunks, and consistent snooping state across switches. Senior conversations about multicast almost always start, not end, with "which VLAN, who will be the querier, and where are the L3 boundaries."

## Q47: What is the difference between a CAM table and the forwarding logic of a switch?

**A:** CAM (Content-Addressable Memory) stores the MAC-to-port/VLAN mappings that classic bridging uses. The "content-addressable" property is key: lookups compare the target MAC against all entries simultaneously and return a match (or the "don't care" mask) in one cycle, at price of high silicon area. CAM is exactly the right structure for exact-match destination MAC and for static forwarding decisions.

Forwarding logic is where policy sits above the CAM lookup: VLAN membership validation (frame tagged/untagged rules), ACL filtering, QoS marking and policing, MAC-based security checks, MLPS/QinQ transforms, and TCAM-based flow classification all gate which frames actually reach the egress port. The ASIC pipeline runs ingress decision, destination lookup, and egress scheduling; CAM holds only a lookup table.

For a senior answer, be precise: CAM gives you flat/LPM exact-match table access; TCAM additionally supports ternary matching (0/1/don't care) so ACLs, QoS classification, and flow entries live there. The engineering tradeoff is table size vs. density vs. power, which is precisely why flow-table-heavy features (ACLs, micro-segmentation) are TCAM-consumers and why overflow has visible consequences.

## Q48: How does a switch choose between hardware and software forwarding?

**A:** A switch's data plane is typically a programmable ASIC (or NPU, FPGA) that handles line-rate forwarding — CAM lookup, ACL match, QoS, and queueing all occur in silicon with per-packet cost near zero. Control-plane functions (routing protocols, STP, LLDP, management) run in CPU. The critical rule is which packets stay in data plane versus punting to CPU for handling.

Exceptions force software path: frames needing special handling (unknown unicast in some designs, management frames like BPDU/LLDP/ARP to CPU, control-plane rate-limits, multicast not covered by hardware), and packets hitting software-defined exceptions (NAT, encryption, tunneling, deep ACL features). Punt rate-limiter protects the CPU from being overwhelmed by a flood of exception frames.

The production failure mode is CPU saturation — for example, a broadcast storm parses as a flood of control-plane punts, CPU pegs, STP/OSPF/BGP processing stalls, and the switch effectively "hangs." A senior answer ties forwarding architecture (hardware fast-path vs. software slow-path), exception rates, and routing/control-plane health together: the switch is fine only as long as data plane handles what data plane should and the CPU budget stays quiet.

## Q49: What happens to frames when a switch is oversubscribed?

**A:** Oversubscription means the aggregate ingress capacity of a switch exceeds its forwarding or egress capacity (a common 48×10G-to-4×40G port layout has a fundamental ingress:egress ratio). When input spike exceeds output bandwidth, frames queue in memory-buffers. If buffer fills, tail drop or weighted tail drop discards frames — the packet is dropped at the input or egress queue, and TCP or the application eventually recovers.

Buffer sizing is everything: shallow buffers (typical small/standalone switches) drop on micro-bursts; deep buffers (data-center switches, ~9MB+ shared buffer) absorb burst traffic long enough for the mesh to drain. Buffer management inside the ASIC determines whether drops are per-queue fair or necessarily head-of-line blocking for a congested output.

The senior framing is that oversubscription is a deliberate design property, not a bug — a 1.25:1 or 2:1 fabric is standard for cost efficiency. Correctly engineered fabrics use buffers to smooth the bursts and monitoring to detect sustained drops; a fabric that drops constantly is mis-sized or mis-architected, and measurements (per-queue drops, utilization deltas) rather than link-speed changes reveal the truth.

## Q50: What is the difference between storm control and broadcast filtering?

**A:** Storm control is a reactive, rate-based guard: a switch port limits broadcast/multicast/unknown-unicast frame rates, and when inbound rates exceed the configured threshold the switch drops excess packets (or in some implementations shuts the port). Broadcast filtering (e.g., broadcast storm control thresholds, or VLAN-level broadcast suppression) is the same protection applied at configuration rather than rate.

The concepts overlap in spirit but differ in mechanism: storm control is per-port rate policing on the data path; filtering usually refers to inbound ACL or port-access filtering that disallows selected broadcast/multicast traffic entirely (as in rare "filter all broadcast" configurations). Most organizations rely on storm control, which drops only excess and leaves the rest flowing.

The senior nuance: rate-based protection is essential on access ports facing hosts (a virus/botnet can generate a storm), while core/aggregation ports should have higher or disabled storm thresholds. Dropping broadcast proactively has real functional impact — ARP, DHCP, and OSPF/BGP multicasts would die — so "filtering" too aggressively is self-sabotage. Control storm control at the boundary where storm sources live, not in the middle.


## Q51: How do you compute effective throughput on Ethernet accounting for overhead?

**A:** Ethernet per-frame overhead comprises the 7-byte Preamble plus 1-byte SFD, a 6-byte destination MAC, 6-byte source MAC, 2-byte EtherType, and the 4-byte FCS, plus the minimum inter-frame gap (IFG) of 12 bytes. A VLAN tag adds 4 more bytes. For a 1518-byte frame at line rate, the overhead is roughly 38 bytes of framing plus 12 bytes of IFG, so the payload ratio is about 1518/(1518+38+12).

Throughput at a given rate is (payload bytes × link rate) / (total wire bytes). At 1 Gbps with maximum-size frames, usable payload is roughly 985 Mbps; with minimum 64-byte frames the ratio collapses to near 50–60% because 20% of the wire bytes are management overhead. This is why real-world saturation numbers are lower than raw link rate.

For a senior answer, connect the numbers to design: 9000-byte jumbo frames raise efficiency close to 99%, which is why storage and HPC fabrics standardize jumbo MTUs; and packet-rate ceilings (pps) are often the binding constraint — a switch advertises a forwarding rate in Mpps derived from minimum 64-byte frames, and latency-sensitive apps at 10G with 64-byte packets stress both Mpps capacity and NIC/socket overhead, not link bandwidth.

## Q52: What is an SVI and how does it compare to a routed port?

**A:** An SVI (Switch Virtual Interface) is a software interface carrying an IP address for a VLAN: it is the Layer 3 gateway for all hosts in that VLAN and the endpoint of that VLAN at Layer 3. SVIs let a Layer 3 switch route between VLANs using the same ASIC data path as its L2 switching, at wire speed, and each VLAN gets exactly one subnet gateway.

A routed port is a physical switch port configured as a Layer 3 interface (no VLAN, no L2), often used for switch-to-switch or switch-to-router links, or for access ports in "routed access" designs. Routed ports support routing protocols directly; SVIs support them too, either as gateways for downstream hosts or as L3 endpoints of VLAN-based segments.

Placing the gateway on the access switch (SVIs per access VLAN), at the distribution (shared SVI for many access VLANs), or entirely at the core changes both failover behavior (hosts follow their SVI) and broadcast domain size. The senior decision is about keeping L2 domains aligned with routing domains: SVI design determines where broadcast domains end, IP renumbering scope, and how gracefully failures propagate to hosts.

## Q53: What is a brownfield approach for migrating from legacy hubs to switches?

**A:** A brownfield migration replaces shared-medium hubs with switches incrementally rather than all at once, preserving existing cabling, endpoint IP addressing, and (ideally) VLAN topology while removing collision domains. The key steps are: inventory what connects to the hub (MAC count, expected traffic), place the hub behind a switch port for a monitoring/drain window, and cut over to a pure-switch dedicated port per host.

Incremental migration means each isolated port becomes its own collision domain, and legacy half-duplex NICs are fine as long as the port negotiates speed and fallback half-duplex. As hosts upgrade to full-duplex auto-negotiation, throughput rises naturally. The trickiest part is rarely cables — it is handling scattered adopters (legacy printers with 10 Mbps NICs), addressing (no changes allowed because IP addressing must stay), and any protocol that relied on shared-media visibility (some proprietary discovery).

From a senior view, brownfield switching is fundamentally about risk and imperfection: you cannot afford a forklift, so you phase and validate. The sequence is segment-by-segment: isolate, snapshot, swap, verify (duplex, errors, addressing), repeat — and the correct end state is zero hubs anywhere, because hubs are the single point where broadcasts and collisions collide and where firmware/ARP/management become fragile.

## Q54: How does a switch handle VLAN-tagged frames that arrive untagged on an access port?

**A:** An access port is for a single VLAN: incoming untagged frames are assigned to its configured access VLAN and forwarded within that domain; any 802.1Q tag the port strips on egress. If a frame arrives on an access port carrying an 802.1Q tag, the switch has two policies: either it drops the frame (payload/trunk mismatch) or it accepts the tag under "trunk port + untagged/mismatched handling."

The correct behavior matters because a misconfigured or malicious endpoint could inject a tag. A host on the access VLAN that switches tagging off/on midstream, or a rogue device double-tagging with an outer VLAN ID of its own access VLAN, can hop VLANs unless the switch ignores or filters tags on access ports.

Senior hardening: access ports should ignore or drop tagged frames (802.1Q "untagged only" enforcement), trunk ports should prune VLAN list and set native VLAN to an unused ID, and the router/switch should never forward an 802.1Q-tagged inner frame whose outer tag is a low-priority/native VLAN. This is precisely the family of attacks known as VLAN hopping via double tagging, and the defense is layer-2 hygiene plus access-port tag filtering.

## Q55: What is asymmetric routing and why is it a problem in Layer 2 networks?

**A:** Asymmetric routing means forward and reverse traffic for one flow take different paths. In a pure L2 switched network it is rare; asymmetric paths from a host to different firewalls or from two gateways can make a stateful device (firewall, IDS) drop valid sessions because it only saw one direction. In any L3 design with multiple equal gateways or stateful middleboxes on different paths, asymmetry is normal — and must be handled.

The L2-specific problem appears when asymmetric routing meets a switch that learns MACs: if the same source MAC appears on two ports (a server sending via two interfaces), the MAC flaps and flooding spikes. On shared-L2, a broadcast domain that spans redundant paths without proper STP/MLAG coordination will flap continuously.

The accepted solutions are: confine L2 to single-path per VLAN (MLAG/vPC treats the pair as one logical device so MAC stays stable), bridged path selection per flow at the gateway, or per-flow state synchronization between stateful devices (cluster/firewall HA). The senior answer ties L2 to L3: asymmetric routing is a routing-plane feature; making it work with L2 MAC stability and stateful semantics is an architecture requirement, not an accident.

## Q56: How does a switch detect and react to a MAC address flap between two ports?

**A:** A MAC flap is the same source MAC being learned on two different ports in quick succession; the switch moves the CAM entry from port A to B, then A, then B, generating consecutive "MAC move" messages. The reaction depends on the switch's MAC-move policy: default platforms relocate instantly, others have an optional move-detection counter and err-disable on threshold.

The trigger causes are almost always prototypical: an STP breakdown has created a loop, a shared-port/NIC teaming misconfiguration causes redundant frames, or a virtual machine live-migrated while the network was unaware. Before any config change, the correct senior move is to capture the MAC-move log, look for the timeframe it started, and correlate with network events (STP topo change, VM migration, cable move).

Resolution is about the root cause, not just clearing alerts: fix STP (restore blocked ports/root), correct port channel configuration for dual-NIC hosts, or use static CAM/port binding for VMs. The operational metric to watch is MAC-move rate; a single-digit-per-hour count on a busy access switch is normal from laptop roaming, dozens-per-second are suspicious and usually a loop.

## Q57: What is the role of a multicast router port (mrouter) and how does a switch learn it?

**A:** A multicast router port (mrouter port) is a switch port facing a multicast router or the L3 boundary that runs IGMP. The switch forwards all multicast group traffic toward the mrouter port, and it forwards the router's IGMP queries to all receiver ports. This is the anchor of snooping: without a known mrouter, a switch cannot route group membership flows correctly, and multicast may cease or flood.

The switch learns mrouter ports from IGMP queries (and by configuration: static mrouter config on ports facing routers). Different platforms use different heuristics — some forward group traffic to all ports if no mrouter is seen, others rely strictly on configured mrouter. The failure mode when a VLAN's querier is lost: IGMP snooping stops, multicast stops (or floods), and hosts that relied on streams silently lose them.

Operationally, every VLAN needs exactly the right mrouter set: the router port (its VLAN interface) and any other L3 path must be configured or learned correctly. In designs where multiple L3 devices serve one VLAN, explicit mrouter port configuration is safer than relying on query learning, and stale mrouter state after a router failover is a classic late-night multicast outage.

## Q58: What is the role of the MAC Address Table in bypassing the CAM lookup for VLANs?

**A:** The MAC Address Table (CAM) is fundamentally per-VLAN: each entry binds (MAC, VLAN) to an ingress port, and lookups are performed with the VLAN as part of the key. This per-VLAN scope is what lets a switch separate identical MACs in different VLANs (a common pattern in deduplicated VM or service-provider space) and what constrains flooding to stay inside the VLAN.

VLAN-aware lookup also means that "is this frame in the correct VLAN?" is only partially about the CAM entry: the switch first checks the frame's VLAN (via tag or access port assignment), then asks "does my CAM know this destination in this VLAN?" If not — flood within this VLAN. This is the practical sense in which the table "bypasses" or abstracts the L2 path: it recognizes the domain first, then the address.

Senior familiarity with this model matters for three operations: injecting static entries per VLAN (a static route to a MAC), sizing per-VLAN MAC tables (a very large VLAN can exhaust a global table), and debugging VLAN leaks where the same MAC exists on two VLANs — the CAM is correct per-VLAN, so the bug is likely inter-VLAN routing or a trunk/tag misconfiguration, not a look-up corruption.

## Q59: What are the differences between L2 bridging and L3 routing in terms of MAC and IP?

**A:** Bridging forwards by MAC within a VLAN: frame header is untouched except for VLAN tag add/remove, destination MAC is looked up in the CAM, and the switch is essentially invisible to higher layers. Routing forwards by IP across subnets: the router (L2 device) changes both source and destination MAC at each hop, decrements TTL/hop limit, checks the IP destination, rewrites the frame, and re-emits on the next subnet.

The router is therefore the boundary where L2 domains end: its interfaces terminate broadcast domains, and its IP forwarding decision separates the L2 frame inside its broadcast domain from the next hop's. A switch never rewrites MACs; a router always does (per hop). This is why "routed access" replaces the L2 hairpin with a direct L3 boundary.

Senior relevance: every design question that touches inter-VLAN traffic, failover, or asymmetric routing reduces to "am I rewriting L2 or L3?" — and every troubleshooting instinct that treats ARP/broadcast as L2-only must flip at the routed boundary. Where one network engineer sees two VLANs needing "routing," another sees two devices needing "no L2 broadcast and correct L3 gateway."

## Q60: How do you troubleshoot a "duplicate IP address" error in a switched network?

**A:** Duplicate IPs in a switch network are almost always an ARP/DHCP topology problem, and the first diagnostic is the ARP cache: is the conflicting address appearing from two MACs? Then check which ports those MACs are on — the same physical switch? Different switches? Then review whether mobility or static config put two devices on the same subnet accidentally.

Common causes are: DHCP+static overlap (a recent static assignment collides with a DHCP pool), two devices inheriting a same set during provisioning/imaging, a VM clone that forgot to renew its IP, or a misrouted VLAN spanning L2 multiple subnets. The evidence trail usually lives in switch logs (MAC moves for the collision) and DHCP lease history, not in the IP stack alone.

Resolution follows root cause: reserve the MAC/static range in DHCP, enable per-VLAN static/dynamic IP collision detection, ensure each device's ARP/DHCP is the same subnet scope, and add IP+MAC (DAI/IP source guard) at the access layer to block spoofers. A senior engineer treats the message as an alarm: the fix is the topology (which subnet broadcast domains overlap), not just "change the IP on one box."

## Q61: How does a fabric (leaf-spine) design differ from a classic campus L2 design?

**A:** A leaf-spine fabric is a two-tier Clos topology: every leaf switch (ToR, aggregation) connects to every spine switch, and every path is a single hop. All leaves are equidistant, so ECMP (equal-cost multipath) load-balances traffic across every spine at once, scaling bandwidth statically. Leaf-spine designs are inherently L3 (or VXLAN-over-L3), and failures just reduce ECMP members without changing path length.

Classic campus L2 typically carries access-to-distribution to core with fixed L2 segments, STP/MST, and VLANs that span a tree. It is functionally correct for moderate sizes but has L2 constraints: no multipath balancing, STP actively blocks links, convergence can slow, broadcast domains scale per VLAN, and VLAN sprawl becomes an operational cost.

The senior continuum is not "L2 bad, L3 good" — it is "match the failure/size model": fixed-L2 campus is fine for small user counts and modest bandwidth needs; leaf-spine is the answer when capacity must scale horizontally (any-to-any bandwidth) and when recovery time targets demand symmetrical deterministic topologies (Clos) rather than spanning tree. The answer picks per-requirement, not per-marketing.

## Q62: What is the role of the MAC address in STP port roles and root election?

**A:** The MAC address is the tiebreaker that makes STP deterministic. The Root Bridge election compares bridge IDs: priority first, then the 48-bit MAC. Default priority is identical across switches, so the root frequently resolves to the switch with the lowest MAC, which is effectively random relative to network geography. Administrators override priority specifically to force the root where they want it.

Each non-root switch then computes paths to the root. If two paths have equal cost, the upstream bridge ID (again MAC) breaks the tie; equal upstream ID is broken by upstream port priority, then port index. These rules guarantee exactly one winning path — which is the entire point: STP must produce a unique root and unique best path or the loop-free contract collapses.

For a senior answer, this explains the classic STP failure mode: two switches with equal priorities and no root configuration elect a root such that the middle of the network is not the root, traffic loops suboptimally, or — worse — a misnumbered bridge ID makes a random access switch root and every uplink flaps. Deterministic root placement (explicit priority + RFC-clean MAC) is the fix.

## Q63: What is the "listening" state for in a switch?

**A:** In classic STP, Listening is the phase between Blocking and Learning where a port that has been elected root or designated temporarily refuses data forwarding. It is where switch-to-switch BPDUs still flow, letting the network verify that no better path has appeared, before the port commits to forwarding. It prevents transient data forwarding during topology reconvergence.

The 15-second listening window is the price of timer-based STP: the switch must let 30+ seconds pass in case a new best BPDU arrives that would flip the port back to blocking. RSTP eliminates this by proposal/agreement: a designated port that has converged its subtree peers directly, and listening/learning collapse into the discard→learning→forwarding path driven by handshakes rather than the forward-delay clock.

Senior relevance: "listening" is where the loop risk concentrates. A loop either forms because a port forwards too early, or because the switch refused to reconverge. Modern RSTP does not wait — it negotiates—and "listening" survives only in legacy/omniscient-timer mode. When debugging slow convergence, the question isn't "is this port listening?" but "why is this designated port timer-driven instead of handshake-driven?"

## Q64: What is a "designated port" and how is it chosen?

**A:** A designated port is the path toward the root from a given LAN segment: the single forwarding port on that segment, owned by the switch whose Bridge ID offers the best path (or, at the root itself, any port). Every L2 segment (link) has exactly one designated port, and every non-designated port on that segment is blocked. Existence of exactly one designated port per segment is what makes the tree loop-free.

Selection proceeds by the STP comparison rules: lowest root path cost first; if ties, lowest upstream Bridge ID; then upstream port priority; then port index. The root bridge always holds designated ports (its path cost is zero), and if two equal-lower bridges share a segment, the lower bridge ID wins. The losing bridge blocks its segment port entirely — including against its own other ports.

For a senior conversation, the nuance is RSTP: designated ports on point-to-point links can transition instantly via the proposal/agreement handshake rather than waiting out forward delay. Designated port is also the role on which Loop Guard operates (it watches designated ports for BPDU silence) and where link-loss into port-only failures converges fastest.

## Q65: How does a VXLAN overlay interact with a leaf-spine underlay?

**A:** VXLAN encapsulates the original L2 frame in a UDP/IP packet (port 4789, VNI = 24-bit segment ID), so the overlay's MAC/VLAN traffic rides over a routable L3 underlay. The leaf (VTEP, VXLAN Tunnel Endpoint) terminates the tunnel at the edge: it bridges/VLANs locally, learns remote MAC/VNI via EVPN or flood-and-learn, and encapsulates toward the remote VTEP across the spine.

The spine is deliberately L3-only: it does not hold the overlay state, just routes the outer IP to the correct leaf. Because the overlay is a mesh of tunnels, the underlay can use ECMP freely — the encapsulation gives the spine a stable 5-tuple to hash on, and any leaf can reach any leaf with equal cost. This is how a fabric gets any-to-any connectivity with L2 semantics while every failure stays in the routed plane.

Senior depth: the control plane decides the difference between a VXLAN that "works" and one that "scales." Flood-and-learn VXLAN is a broadcast image of L2 problems; EVPN (BGP route discovery of MAC/IP) moves learning out of the data plane, terminates floods, and enables multi-pathing and active-active. The underlay (IS-IS or eBGP + ECMP) and the overlay control plane (EVPN) together replace the spanning tree's role in the fabric.

## Q66: What are the practical limits of 802.1Q VLAN count and how do you extend them?

**A:** A native 802.1Q tag allocates 12 bits for the VLAN ID, so 4096 possible IDs, minus reserved values, leaving up to 4094 VLANs usable. This is the hard addressing limit of a single tag. Most platforms also reserve high ranges and enforce polish/cost limits on how many active VLANs can be effectively switched.

Extensions include: QinQ (802.1ad) stacking an outer S-TAG over the inner C-TAG, giving 4094×4094 segments ideal for provider Ps-VLAN mapping; VXLAN (24-bit VNI ≈ 16 million) as an overlay, replacing tags on the wire with encapsulated segmentation at the VTEP; and MACsec/EVPN MAC-VRF designs where segmentation still rides an IP overlay rather than per-VLAN tag.

For a senior answer, the limit is more about control plane than bits: 4094 native VLANs are hard to operate because every switch needs consistent membership, pruning, and STP/MST state. VXLAN/EVPN move that burden into a central control plane (decoupled from tag space), and "how many segments do you need" determines when tag-space exhaustion calls for an overlay rather than QinQ.

## Q67: What is LLDP and why is it important in a switched network?

**A:** LLDP (IEEE 802.1AB) is a vendor-neutral link-layer discovery protocol that lets a switch advertise its identity (system name/description, port ID/description) to directly adjacent neighbors via periodic frames. It is the "who am I on this wire" handshake that settles cabling, inventory, and topology documentation without manual labeling.

Switch automation relies on LLDP for verification: an NMS or Ansible playbook reads the LLDP neighbors table (via SNMP `lldpRemTable` or CLI) to confirm "switch-A port Gi1/0/12 connects to switch-B port Gi1/0/24," cross-checking the physical map before applying VLAN/interface changes. It is also foundational for voice: LLDP-MED lets a switch tell an IP phone which VLAN/CoS to use, automatically zero-touch provisioning phones.

For a senior answer, LLDP is a control-plane source of truth you should treat as sensitive: it leaks topology data to any device that listens. Many enterprises disable LLDP on user-facing ports and enable it only where discovery is useful. In spine/leaf, LLDP is effectively mandatory for fabric validation tooling, and its data shapes automated change planning.

## Q68: What is the difference between VLAN pruning and VLAN filtering?

**A:** VLAN pruning limits which VLANs a trunk actually carries: on a trunk you declare an allowed-VLAN list, and frames for unlisted VLANs are not sent (or are dropped at the egress port). This reduces broadcast/multicast flooding scope and keeps unneeded VLAN domains from extending across the network. Filtering, by contrast, is an ingress policy: an ACL or port-security rule decides whether a tagged frame from a known VLAN may enter a port.

Pruning is a topological control (which VLANs reach which switch); filtering is a per-port enforcement (which frames may actually pass). They composite: pruning stops unwanted VLAN reach entirely; a filter additionally stops permitted-VLAN frames that specific policy forbids (e.g., deny all voices except trusted MACs; deny a spoofing source within a VLAN).

Operationally, pruning is where most organizations actually solve their VLAN sprawl — a trunk list that matches the "VLANs that must traverse here" set is one of the best Layer 2 hygiene habits. Filtering is where security lives: it catches traffic within an allowed VLAN that violates specific policies. Both are cheap in CAM/TCAM and should both be deliberate, not defaults.

## Q69: How does ARP work across a router and how is it affected by switching?

**A:** ARP resolves a destination IP to a MAC within a L2 domain (broadcast domain). When a host needs to send to another subnet, it does not ARP for the far end: it sends the frame to its default gateway's MAC (obtained by ARPing for the gateway's IP). The router decapsulates, looks up the destination in its routing table, and re-encapsulates toward the next hop — ARPing for the next hop if needed. Each L2 hop resolves independently.

Switching affects ARP in two ways. Broadcast flooding delivers ARP requests to all hosts in the VLAN (switch floods broadcast), so ARP resolution cost is borne by the whole broadcast domain; and the CAM stores the resulting MAC-to-port entries, so ARP-triggered traffic behaves identically to any other destination-unknown traffic afterward.

Senior nuance: ARP cache health is a source of operational problems. Rate-limit ARP to the CPU (control-plane policer), use ARP/DAI with DHCP-snooping bindings to stop spoofing, and keep broadcast domains small so ARP floods don't become a real load. In large L2 domains, an ARP storm after a failover is the classic event that both saturates the CPU and floods the switch — ARP was always the load that scaling fails on.

## Q70: What is MAC learning with port security, and when is static MAC the better choice?

**A:** Dynamic MAC learning with port security caps the number of MACs per ingress port and is the simplest access-layer control: "up to N distinct MAC addresses, anything beyond is a violation." It is excellent for shape detection (device density) and works with sticky learning to pin the first-seen addresses into config — a form of stateful memory that prevents an attacker from quietly swapping endpoints.

Static MAC (static CAM entries) hard-codes a MAC to a port and never learns/purges automatically; it is deterministic and is the right tool when a single known endpoint (a server NIC, a camera, a printer) must be bound absolutely and no movement is expected. The tradeoff is management burden and the impossibility of auto-adaptation.

The senior selection rule: security posture first (port security caps rate and density), static CAM for identity-critical single endpoints, and dynamic learning for anything mobile (laptops, VOIP roaming) where sticky would age wrongly. Port security itself has a failure mode — it cannot prevent legitimate roaming; so "max 1 + sticky" on a roaming laptop network is a false sense of security. Match the mechanism to the endpoint behavior, not the reverse.

## Q71: How do you monitor for a spanning-tree problem before it becomes a broadcast storm?

**A:** The precursors of an STP failure are measurable: root bridge inconsistencies (the root ID flapping or an unexpected switch winning), a drastic MAC-move rate increase (frames circling a hidden loop), control-plane CPU spikes (especially control-plane processing of BPDUs/ARP), and err-disabled events from BPDU Guard/Root Guard. Monitoring these telemetry streams catches a tree problem before traffic collapses.

Anomaly detection compares baselines: "MAC moves jumped from 5/hour to 800/minute" is the classic signature of a hidden loop whose frames are circulating. Monitoring root ID continuity and apology-cluster counters (STP TCN counts) catches re-convergence storms. The management plane should also monitor BPDU/ARP/IGMP control-plane packet admission for the same reason.

The senior move is to pair detection with containment: automatic BPDU Guard/Root Guard/Loop Guard at edges, rate-limiters on CPU punts, and a "MAC move threshold per port" policy that err-disables the offending access port. Monitoring alone makes you smarter; monitoring plus automated containment makes the network self-healing against the hidden-L2-loop class of failures.

## Q72: Why would two same-speed links between switches be unequal in forwarding?

**A:** Two same-speed links can be unequal in actual capacity due to hashing, buffering, and forwarding-plane differences. If they are bundled in a port channel, the load-balance algorithm distributes flows per hash — an asymmetric flow profile (many small flows between two VIPs, a few elephant flows) can put most traffic on one member. If they are independent physical links, STP blocks one entirely, so "same speed" ≠ "same path."

Even at same nominal speed, forwarding differences arise: one link is a routed L3 port with ECMP and the other is L2, or one port's buffer/cos-a/guarantee vs. tail-drop differs, or the same pps rating is differently congested because one path carries multicast flooding or management traffic. OSPF/BGP ECMP also divide per-hash, not per-byte.

The senior answer: same speed is a nominal claim, not an operational guarantee. Engineers verify with sustained test traffic per member, examine hash distribution across flows, adjust the load-balance fields to spread the failing flow set, and check STP state/ECMP membership. The common "slow port in a bundle" is almost always a hash aliasing problem, not a hardware defect.

## Q73: What is the difference between FEC and CRC on a 10/25G Ethernet link?

**A:** CRC (the 4-byte FCS) is the MAC-layer integrity check computed end-to-end per frame and verified by the receiver's MAC. FEC (forward error correction, e.g., RS-FEC per IEEE 802.3bj/802.3cd, Firecode/kr) is a physical-layer mechanism that adds redundant parity symbols to the bit stream so the receiver can repair a small number of bit errors in-line rather than wait for retransmission. CRC detects; FEC corrects.

FEC exists because 25G/100G/400G electrical/optical signaling runs at low margin: without FEC the pre-FEC BER (bit error rate) would be too high, and end-to-end MAC CRC would drop frames constantly. With FEC, corrected bit errors never reach the MAC layer at all; the frame arrives intact. FEC costs latency (tens of ns added per link) and bandwidth (RS(528,514) consumes ~2.7% of line rate on 100G-KR4/CR4).

The senior operational nuance: FEC pre-FEC BER thresholds are the troubleshooting bridge between optical margin and MAC drops. When a 100G link reports rising pre-FEC BER but no CRC, the fiber/transceiver is degrading — swap before MAC drops appear. When CRC drops appear first, the link signal has degraded past FEC's correction window, which points to a bigger (new module/cable fault) problem.

## Q74: What is the practical distinction between a "broadcast domain" and a "failure domain"?

**A:** A broadcast domain is the set of hosts that can see broadcast frames — bounded by L2 VLAN boundaries. A failure domain is the set of devices that suffer when a single fault or misconfiguration occurs. These overlap heavily in L2 networks: a broadcast storm, MAC loop, or STP misconfig can blow through an entire VLAN, so both domains usually coincide, which is why network design tries to shrink them together.

The senior insight is that L2 faults hit all members of the broadcast domain simultaneously — that is what makes them "failure domains." Segmenting VLANs shrinks the blast radius of storms/floops, but the L2 failure domain is also bounded by where the STP/looping risk stops. A network that separates failure via routed boundaries shrinks L2 blast radius but creates L3 convergence, which has its own availability cost.

Operationally, failure-domain engineering is about declaring intent: "VLAN 10's broadcast domain and its failure domain are both this access switch" is a design statement. Senior designers plan redundancy, prevention (STP/MST + BPDU guard), and blur — they know exactly which fault kills how many devices, and build per-VLAN/per-fabric limits accordingly.

## Q75: What is a Layer 2 VPN in the context of campus/enterprise switching?

**A:** A Layer 2 VPN delivers a virtual private L2 segment between two sites: hosts see each other as if on the same broadcast domain — same VLAN, same subnet, ARP/broadcast behavior across the WAN. In its simplest form this is L2TPv3 or VPLS/VPWS on provider MPLS; in modern enterprise it is VXLAN/EVPN over an IP WAN, or OTV for specific site coupling.

L2VPNs solve specific real problems: VM mobility (live migration requires the source/destination VLAN to appear simultaneous), multi-sited clustering (extending L2 for heartbeat/multicast), and legacy apps that cannot cross L3. Each of these benefits, though, is a trade: floods/broadcasts now travel the WAN, MAC lookup crosses WAN, and the broadcast/failure domain stretches from hours to days away.

The senior position: treat L2 VPN as a surgical tool, not a network-wide default. Design for the few VLANs that genuinely need stretch (usually just those with migration/clustering), collapse it for everything else, and think hard about the control plane — EVPN learns MAC/IP via BGP instead of flooding, which converts L2VPN from an L2-problem-shaper into an L3-scalable solution. The question is "what must be contiguous", answered by the actual migration requirement, not the convenience of one flat tag.


## Q76: How would you design a loop-free, high-availability L2 edge for a campus?

**A:** The design goal is deterministic redundancy with no reliance on slow STP convergence and no single point of failure. Use two distribution/core switches running a Multi-Chassis Link Aggregation (vPC/MLAG) pair, so they behave as one logical switch for access-layer ports. Every access switch attaches with two links into the pair via a port channel (one to each peer), and both links forward simultaneously — no STP blocking wasted.

Each access switch holds its own L2 forwarding table; the distribution pair exchanges ISL/peer-link and synchronizes MAC/MST state so both members answer identically. STP still runs (as root configuration with explicit priority) but only as a safety net: with the LAG bundle active, loops cannot form, and STP's 30-second re-convergence is irrelevant because failures are handled by LAG/member loss in milliseconds.

Host-facing ports are edge (PortFast) with BPDU Guard and Loop Guard; inter-switch trunks use standard/MST with a manually pinned root. The resulting failure envelope: a distribution switch dies → unaffected (peer carries it via control-plane sync); a link dies → member removed from the LAG; an access switch dies → that subtree down, all others clean. The hardest part is state coherence (MAC/IP/MST synchronization between the pair), which is precisely why the pair must be engineered as one logical device.

## Q77: How do you decide between spanning-tree and routed access for a new building?

**A:** The decision is a trade-off between L2 semantics, failure domains, and operational complexity. Routed access terminates every access switch's VLAN at that switch (each access port gets an IP gateway, OSPF/BGP runs to the distribution), so loops cannot form and convergence is sub-second via routing. It eliminates STP, broadcast domains shrink to a single switch, and any failure is isolated to an L2-U-intact routed boundary.

Routed access costs: IP addressing on every access interface, routing protocol state on access hardware, and the loss of certain L2 niceties (sustained L2 adjacency across the building, VM mobility). If the building genuinely needs host-facing mobility, multicast, or bridging across the fabric — typically because of VoIP/storage virtualization requirements — spanning-tree L2 (MSTP/vPC) keeps that capability at the cost of STP free-space and broadcast sizing.

The senior threshold is requirements, not hype: if the workloads are laptops, IP phones, printers with no inter-access L2 mobility need, routed access wins (fewer failure vectors, cleaner troubleshooting, better from a security-dynamic standpoint). If the building hosts VDI/blasts/migrations that require L2 stretch, MSTP plus a well-placed vPC pair is honest engineering. Look at multi-tier campus, choose by L2 need per segment, not globally.

## Q78: What is the role of the control plane in a modern switch and why does it matter?

**A:** The control plane runs the switch's intelligence: routing protocols (OSPF/BGP), STP/RSTP/MST, LLDP, ARP/ND processing, management (SSH, SNMP, NETCONF), and the data structures (RIB/FIB, CAM updates, protocol state machines) that program the data plane. It is CPU-resident, comparatively slow, and — critically — shared by all forwarding decisions that require exception resolution.

The data plane executes the programmed rules at line rate in ASIC/TCAM: forwarding, filtering, QoS, encapsulation. It cannot make policy decisions; it only consults the tables the control plane builds. The two must stay consistent: a packet hash, a route that dies, or a prefix change must propagate from control plane to data plane before traffic depends on it. Queueing and programming latency matter.

Operational relevance: control-plane attacks (a storm of unknown MACs, ARP floods, BGP route churn) starve the switch of the CPU time it needs to keep table state fresh, causing forwarding to drift and drops to grow even though the ASIC is idle. Therefore control-plane policing (CPP/CoPP), rate-limiters on punted frames, and resilient protocol state are arguably more important than raw forwarding speed. A modern senior network engineer reasons about the switch as a control-plane + data-plane pair, not as a magic black box.

## Q79: How do you validate that a port channel is actually distributing traffic evenly?

**A:** Validation starts with the interface counters: compare ingress/egress counters per member (`show port-channel load-balance`, per-member `show interface` octets/errors) over a sustained window. Because hashing is flow-based, counts are only meaningful at flow granularity — you need synthetic or real flows that exercise different (src/dst) address pairs and inspect the per-member byte delta.

Next, inspect hashing parameters: default is often src/dst IP (L3) or src/dst MAC (L2). If your traffic is heavily skewed (many small flows to one server MAC, or thousands of flows to one IP), the hash concentrates on a member. Change the hashing fields (L2, L3, L4) and re-measure; asymmetric traffic may call for L4-port-based hashing for better distribution.

The senior tip is symmetric-hash: hashing on both src and dst fields (not just one) prevents same-pair flows from always landing on one member, and some platforms allow per-vlan/port hashing. If you see a persistent 3:1 member ratio, verify MAC changes/co-/, corrupt FCS counters for hidden faults, and consider rebundling (remove/add member) to reset the LAG state. The metric to watch is per-member utilization delta, not the aggregate port-channel counter — the whole point is that the aggregate hides imbalance.

## Q80: How do you design MACsec into a spine-leaf fabric without a key-management choke point?

**A:** MACsec in a spine-leaf fabric is a link-anchored design: every spine-to-leaf and leaf-to-host link encrypts independently. Key management is distributed — never a single RADIUS server per link. The design uses MKA over 802.1X/EAP: each pair of links runs its own secure-channel assocation, with keys derived via 802.1X authenticator (switch) — RADIUS server (per-fabric exposure). Leaf acts as authenticator for downlink hosts; spine-leaf neighbor links authenticate with the switch as both supplicant and authenticator.

Because MKA is per-link, a RADIUS outage only blocks new link bring-up (and rekey cycles) — established channels keep their keys and keep flowing. The fabric-wide pattern: an Ethernet access switch per link, MKA on the access switch, RADIUS server pool for key delivery, and hardware crypto engines so the MACsec burden never reaches the CPU.

The senior caveat: MACsec protects the wire, not the switches. A compromised switch decrypts its own links, so MACsec must be paired with switch-integrity controls (secure boot, signed firmware). Monitoring 'connectivity-association' counts per device and failed-key events rounds out the story — and the only way MACsec breaks is as a full-fabric authentication failure, so the RADIUS/AAA pool is the true control point to make resilient.

## Q81: When would an EVPN-VXLAN fabric pay for itself over MSTP/vPC?

**A:** EVPN-VXLAN pays for itself at the point where L2 domain size, MAC table pressure (each switch learns every remote MAC), and east-west bandwidth become the dominant constraints. The pragmatic triggers: you exceed ~100s of VLANs, you need any-to-any connectivity at scale, you must terminate VM mobility across many VTEPs, or you want deterministic multi-path (VXLAN hashing/ECMP) instead of STP-blocked, hy half-active redundancies of vPC/MSTP.

The economic comparison: MSTP/vPC requires every L2 hop to hold full VLAN and MAC state, and STP actively blocks paths, so bandwidth scales by using more switches rather than more paths. EVPN-VXLAN moves MAC/IP knowledge to a central BGP control plane, floods only when needed, and lets the underlay balance everywhere. The break-even is when adding a spine doubles usable bandwidth instead of adding parallel MSPT trees.

The senior caveat is operational maturity: EVPN-VXLAN demands an underlay routing protocol, BGP discipline (route targets, VNI mapping, MAC learning), and orchestrators that can keep overlay/underlay cohesive. Teams that adopt it for latency or flex without that maturity often migrate back. The honest evaluation is total cost of operation: if your team can already run dynamic routing at the ACL-boundary, EVPN-VXLAN is the point of diminishing MSTP value; otherwise a well-designed MSTP/vPC is simpler and sufficient.

## Q82: How does a switch perform MAC learning in a VXLAN fabric?

**A:** In traditional L2, MAC learning is passive: switches learn every source MAC they observe. In VXLAN with EVPN control plane, learning is elevated: the VTEP (leaf) monitors local MAC/IP via its own L2, then publishes those MAC/IP-VNI bindings into BGP EVPN, and remote VTEPs learn them via the control plane route exchange — not via data-path flooding. The switch therefore "learns" remote MACs as FIB/EVPN-imported routes, not as CAM sniffing.

The effect is that remote MACs exist in the CAM/ARP tables of VTEPs the moment the control plane delivers the route, and unknown frames between VTEPs are not flooded across the WAN — only the control plane (BGP) carries the address gossip. This changes the flood-and-learn architecture of classic VXLAN (RFC 7348) into the modern layered model: underlay forwards encapsulated data, overlay control plane feeds FIB/route tables.

Operational consequences: MAC table size on a VTEP now includes imported remote MACs, which affects TCAM/CAM sizing; route churn (VM migration) must be handled by BGP route updates, so MAC moves are no longer silent but become BGP events; and the network's failure domain splits — data-plane floods vanish but control-plane flapping becomes the new monitor (BGP session metrics). A senior engineer conversation about VXLAN almost always lands on the control-plane/flap story, not the encapsulation.

## Q83: How do you troubleshoot asymmetric burst drops on a single leaf uplink?

**A:** "Asymmetric" burst drops on one leaf uplink point to a very specific geometry: the egress bandwidth of that leaf port is lower than the aggregate ingress of the many server-facing ports feeding it — a classic oversubscription micro-burst. The drop counter is almost always egress tail-drop/queue drop on that uplink, while ingress ports show no drop. Confirm direction: drop counters on egress, not ingress.

Two sub-causes: either the leaf's buffer cannot absorb the synchronized burst (shallow-buffer ASIC), or the micro-bursts are real (e.g., every rack doing a simultaneous storage flush). The fix space runs from buffer tuning (enable dynamic buffer allocation, guarantee a buffer headroom for the drop-heavy class), to scheduling (change egress QOS/CoS to priority-drain), to architectural (rebalance flow distribution across both uplink members, verify the uplink is not the incorrect 1:1 aggregate).

The senior toolset: measure at the 10-100ms granularity (per-queue drop counters over 1s is too coarse), correlate with TCP retransmission spikes, and reproduce with a controlled synthetic burst (tc/netem/IXIA). If sustained bursts regularly exceed the uplink's buffered capacity with no flow at L4 to back off (UDP storage), the answer is capacity, not tuning. Always confirm the burst is at the uplink, not the far-end egress (a drop at the destination switch looks like a burst here).

## Q84: What is the IEEE 802.1CB (FRER) and where does it fit in Ethernet reliability?

**A:** IEEE 802.1CB Frame Replication and Elimination for Reliability (FRER) is a TSN (Time-Sensitive Networking) mechanism that creates duplicate copies of a frame and sends them along two disjoint paths; the receiver eliminates the duplicates. If one path loses a frame, the other path's copy still arrives, giving bounded latency and loss tolerance for critical streams (industrial control, audio/video, automotive).

Operation is per-stream: a stream is tagged with a sequence number, the source creates and sends N copies on N redundant paths, and each intermediate hop eliminates copies it has already forwarded (per-stream sequence identification + elimination). The practical effect: packet loss on any single element-path is masked end-to-end without relying on retransmission — which would break real-time bounds.

Senior framing: FRER trades bandwidth for latency-critical resilience. It complements (not replaces) the two sides of modern Ethernet reliability: data-plane redundancy (LAG/MLAG) protects links but not L3 paths; FRER protects the stream at the expense of doubling bandwidth. Its role in campus/building networks is niche (industrial and automotive), but its design shows the direction of TSN: Ethernet adapting fully to deterministic, closed-loop control requirements where STP's re-convergence is never fast enough.

## Q85: What are the effects of multicast flooding on a leaf-spine fabric?

**A:** Multicast flooding in a fabric behaves exactly like it does in any L2 domain: frames are sent to every port in the VLAN. In a leaf-spine topology, every leaf in the VLAN receives the multicast stream even if only one host subscribed, wasting bandwidth on every spine uplink and on every downlink that has no member; the fabric's core is then a collection of misdirected copies.

Leaf-spine also amplifies the problem geometrically: multicast to a group that has members on three leaves floods all three leaves (and any non-member leaves too if no IGMP snooping), and any head-of-line-blocking for those floods slows unicast flows. The remedy is IGMP snooping at every leaf + correct mrouter port configuration, plus consider PIM or mLAG to keep the group path engineered rather than flooded.

The senior move: size the fabric's multicast blast radius deliberately — a multicast-heavy workload (vSphere heartbeat, surveillance, AV) deserves a dedicated VLAN/VNI with its own querier and snooping policy, and the fabric should still avoid flooding across the spine when members are localized. EVPN-VXLAN has this built-in (per-VNI multicast tag/EVPN IMET routes), which is why multicast-heavy fabrics migrate to EVPN rather than fight with classic snooping.

## Q86: How does a Layer 2 switch protect the control plane from a broadcast storm?

**A:** The switch protects the control plane by policing what reaches the CPU: control-plane policing (CoPP) or CP/CPU queue discipline sets explicit rates for everything that must punt — ARP, ICMP, LLDP, STP/BPDU, OSPF/BGP, and exception frames. Broadcast frames destined to the CPU are rate-limited and dropped ahead of protocol processing, so a storm never starves the routing/STP logic.

The data plane keeps forwarding even under flood: switch ASICs process traffic they can handle in hardware; only exceptional frames (unknown MAC destined to the local router, CPU-mapped multicast) reach the CPU, and CoPP caps them. The combination — hardware fast-path immune to floods + CPU protected by paddled policing + rate-limit on ingress broadcast (storm control) — is what makes switches resilient to the exact storm events that torched hub-era networks.

Operational detail: CoPP must be explicitly whitelisted (not a deny-all); BPDU/LLDP/OSPF must always get minimum admission; the "unknown MAC destined to me" classifier is the one to watch because CAM-learning load and punt load together compound. A senior design puts CoPP and DHCP snooping/DAI at the same place: it doesn't just filter at egress, it refuses spoofed sources at ingress so the control plane never sees them.

## Q87: What would the ARP broadcast problem look like in a 1000-host VLAN?

**A:** ARP traffic in a single VLAN scales poorly by nature: every unresolved IP-to-MAC query broadcasts to all 1000 hosts. At steady state, hosts ARP on cache misses; after an event (boot storm, DHCP renewal window, gateway failover, VM cluster primary change), thousands of hosts re-resolve within the same seconds, and each ARP request carries a full broadcast on every switch. Aggregate = tens of thousands of broadcasts per second hitting every host and every switch CPU.

The consequences pile up: switch CPU punts for ARP (each ARP request must be examined), host NIC interrupts and OS ARP-cache processes spike, and network boot storms trigger proxy-ARP scalding. If the gateway's MAC changes (failover), the flood becomes a thundering-herd ARP replay at the exact moment of failover — the worst possible time for the network to be at peak CPU.

The senior mitigation stack: segment the VLAN (smaller broadcast domains), enable ARP cache tuning per host (longer timeout, proxy ARP), use a gateway with a stable virtual MAC (HSRP/VRRP) so failover doesn't invalidate every cache, and add switch-side protections (DHCP snooping + DAI to cap ARP rate, storm control broadcast). At large scale, prefer an L3 boundary per access switch and route between segments — ARP blast radius then shrinks to each segment's own hosts, which is precisely why "flat 1000-host VLAN" is an anti-pattern even when the switch can technically do it.

## Q88: How do you diagnose a slow port-channel member with a healthy aggregate?

**A:** If the bundle throughput is fine but a member is slow, the first split is between data-plane and control-plane issues. Check per-member interface counters first: errors (CRC, input/output drops, discarded), queue drops, and duplex state; a member with drops or errors while others are clean is either a marginal cable (FEC pre-FEC errors), a link that negotiated lower speed, or a forwarding-plane hash funnel.

Next confirm the hash does not concentrate that member: correlate the slow member's per-port utilization with the flow distribution. If low traffic yet drops, the issue is likely a single saturated flow that hash pinned to that member (elephant flow), or the member carries control-plane streams. Toggle load-balance fields and observe the member's utilization change.

The senior habit is measurement discipline: capture with a sustained 5-tuple stream and measure per-member rates against the hashing policy; check STP role (a member stuck in blocking doesn't carry L2 traffic), verify LACP negotiated keys, and confirm you are not seeing MACsec/encryption overhead asymmetrically. Fixes range from replacing the cable (FEC margin) to re-balancing hash keys to rebundling the LAG. Above all: never "fix" the slow member by removing it and losing failover capacity.

## Q89: How does a switch implement VRF-lite and why would a campus need it?

**A:** VRF (Virtual Routing and Forwarding) lets a single switch maintain multiple independent Layer 3 routing tables (each with its own routing protocols, next hops, and route-leaking policies). VRF-lite is VRF on a switch without MPLS — each VLAN/interface is assigned to a VRF, and inter-VRF traffic moves through explicit route-leaking or an external gateway. It is the campus-scale approximation of provider VPN tables.

Campus needs: tenant isolation (different customers or departments sharing hardware while routing stays separated), security segmentation (guest/MIoT VRFs with no path to the corporate table), and controlled inter-VRF carve-outs (a shared service VRF that sees specific corporate routes but not vice versa). Because each VRF is a separate FIB, a misbehaving tenant cannot contaminate another tenant's routing state.

The senior consideration: VRF-lite adds real operational load — routing protocol per VRF, route-map discipline for leaking, and every new VLAN/inter-VRF link needs careful design. Its payoff is that the campus can run many logical networks on one physical fabric without flat shared-L2 or giant security risk. The failure mode to design against is silent route leakage (VRF import/export misconfig leaking guest routes into corporate), which monitoring must catch before it becomes a breach.

## Q90: What is the difference between "flooding" and "broadcasting" in Ethernet?

**A:** Broadcasting is a deliberate L2 mechanism: a frame sent to the broadcast destination (FF:FF:FF:FF:FF:FF) that every host is supposed to receive; it is the transport primitive for ARP, DHCP, and discovery protocols. A switch forwards broadcast to every port in the VLAN because the protocol demands it. Flooding is a switch behavior, not a frame type: when the destination MAC is unknown, the switch sends the frame out all ports — but only as a last resort, and only in that VLAN.

They are frequently conflated because both involve "out all ports," but they differ in intent and handling. Broadcast frames are always flooded within the VLAN; unicast-frames-to-unknown are flooded only when the CAM misses. Floating differences are observable in counters: storm control and unknown-unicast flooding rate-limiters apply to each independently; a frame with an FF:FF:FF:FF:FF:FF destination is broadcast regardless of the switch's CAM.

For operations, the distinction matters for diagnosis: broadcast flooding hits every host by design; unknown-unicast flooding is a symptom of CAM miss rate (silent destination, aging, table saturation). Traffic that "floods everything" carries two separate smells — the broadcast storm (protocol/loop) and unknown-unicast flooding (table pressure) — and the correct fix is different in each case.

## Q91: How does a switch behave if the CAM table is full and learning is turned off?

**A:** With learning off and the CAM full, the switch is in the strictest forwarding mode: frames to a known destination are forwarded normally; every unknown destination is flooded because there is no table space to learn it. The flood rate is maximal and permanent, since the unused capacity never fills. The switch also stops relearning sources that moved — a moved MAC stays stuck at its old port (or the old port's entry persists), causing legitimate traffic to wrong-path until the entry ages out.

The key operational observation is that with a full static/frozen CAM, the switch behaves like a fixed-wiring crossbar plus a broadcast fan-out: known entries act as exact-match routes, everything else broadcasts to the VLAN. This is how some "hidden" security features (CAM-full = flood) were historically exploited — the flood makes the attacker's port a receiver of everything the switch can't resolve.

The senior take: shutting off learning is not a security control; it is a behavior overload. Learning must remain on and be protected by per-port hardening (port security caps, MAC-move limits) — a full CAM is a design/attack failure, not a mode. When a full CAM is actually required (static-only segments), pair it with explicit static entries for every destination in that VLAN and monitor flood counters so the transition to "everything floods" never goes silent.

## Q92: What is the role of a "dynamic ARP inspection" table and how is it built?

**A:** Dynamic ARP Inspection (DAI) validates ARP packets against a binding table — which IP is allowed to speak on which port with which MAC. That table is built primarily from DHCP snooping: as hosts obtain leases, snooping records host MAC, IP, lease, VLAN, port. DAI then checks every ARP request/reply on untrusted ports against these bindings; mismatches get dropped and logged rather than poisoning ARP caches.

DAI's default trust model is: ports facing routers/switches are trusted (no validation), ports facing hosts are untrusted (validated). The validation gives the network its first spoofed-ARP defenses at the access edge — the same mechanism that protects against the classic man-in-the-middle where an attacker claims the gateway's IP.

Senior depth: DAI only detects what its table knows, so correctness depends on the binding source. DHCP-snooping-derived entries are always up to date for dynamic hosts; static hosts need explicit DAI static bindings; and a rogue DHCP server (if not itself blocked by DHCP snooping) can poison the table. Therefore DAI, DHCP snooping, and IP Source Guard are deployed together — the second blocks rogue servers from establishing binds, the first validates ARP, the last validates IP source — a layered edge control that transforms "ARP spoofing is possible" into "ARP spoofing is blocked at the ingress."

## Q93: How does the PCPU/control plane handle ARP for thousands of hosts?

**A:** The switch CPU handles ARP for traffic destined to the router: the gateway's ARP cache per VLAN, and pragmatic operations like proxy-ARP for the VLAN itself. Except for VPN-termination and some edge cases, hosts' ARP among themselves never crosses the CPU — the CPU only processes the ARP to the gateway's own MAC (the SVI's address). The load is thus proportional to gateway-facing resolutions plus whatever spans between the SVI and hosts.

Control-plane protection begins with rate-limits: ARP to the CPU is capped per source/VLAN; DHCP snooping tells the switch which IP genuinely owns a VLAN/port; and proxy-ARP can centralize "which IP is next hop" where the gateway answers for off-subnet targets. Under load the correct architecture is not a bigger CPU — it is shrinking the ARP surface: smaller broadcast domains, stable virtual MAC for the default gateway (HSRP/VRRP), and routing at the access switch so each segment resolves only to the same access-layer router.

For a senior answer, the pattern is: CPU ARP is a convex function of gateway fails/roam/ARP-invalidation events, and protective engineering is about event shape (stable virtual MAC, no gateway migration storms), not just packet counts. Monitoring 'ARP queue depth' and punted-ARP rates is the linear sensor that tells you whether the switch is control-plane-healthy — days before a broadcast storm makes it obvious.

## Q94: What is a switch "access control list" and how is it evaluated for a frame?

**A:** An ACL on a switch is a prioritized list of rules evaluated against each frame: match criteria (EtherType, MAC, IP, port, DSCP, VLAN, and on modern switches L4 fields), then action (permit/deny, redirect, mark QoS). Evaluation is typically TCAM-backed, so each frame hits the first matching entry in O(1) — the price being the ACL must compile into hardware entries.

The security/correctness shape depends on placement. Ingress ACL on an access port stops malicious frames before they traverse the fabric; an ACL on an SVI or trunk filters per-VLAN or per-trunk traffic; VACL (VLAN ACL) evaluates at the VLAN level regardless of ingress/egress direction. The evaluation model is the same (match → action), but its placement determines what it protects.

Senior detail: ACL order matters (first match wins, and hardware often applies default-deny if a hole exists in the wildcard), ACL resource is TCAM budget, and complex ACLs (many masks, ranges) consume multiple ternary entries. A well-formed ACL is also a documentation artifact: the rule order should match the traffic's logical order, not just the security's. Modern platforms increasingly shift ACL evaluation into distributed flow-table or macro-segmentation engines, but the fundamental match-action model survives.

## Q95: Why would two switches pass a ping but fail a large-file transfer?

**A:** Ping (small ICMP packets) exercising the data path is different from bulk transfer: the two rarely fail for the same reason. The suspects: MTU (a ping with default size fits 1518; a TCP stream with MSS 1460 and jumbo frames can hit an MTU gap), asymmetric path (ping can take an L3 path that a stateful device blocks one direction of bulk traffic), or buffer/queue drops on the transfer (queue-full/tail-drop for the port the transfer traverses while ping's tiny packets always fit).

The senior workflow: reproduce the failure deterministically (iperf, dd/scp), capture at the receiver (Wireshark shows retransmissions/out-of-order, window dumps), then check per-hop MTU (ping with DF set at increasing sizes finds the break), and confirm the forwarding path is symmetric for the transfer (trace route both directions; inter-VLAN routing through the same gateway may not be true for all families).

Also worth checking: flow learns a path but the hash sends packets to a member that is saturated; an L4 ACL/DDoS rule matches the transfer's dst-port but not the ICMP type; TCP vs ICMP QoS trust marks; or a TTL/SSH-related trick where the transfer itself is fine but the flow state is asymmetric. Frame the answer as "different layers, different failure modes" — ping is a path probe, a transfer is a stateful, buffered resource consumer on every hop.

## Q96: How do you design an EVPN overlay for multi-tenancy without a large broadcast domain?

**A:** Multi-tenancy in EVPN is per-tenant segmentation: each tenant gets its own set of VNIs (VXLAN Network Identifiers) and its own EVI (EVPN Instance), so a tenant's IP/MAC/VLAN space is isolated from every other tenant's at the overlay layer, with zero broadcast leakage across tenants. The underlay remains a shared routed fabric; the control plane ensures a tenant's routes only exist in that tenant's EVI.

The isolation mechanics: BGP route targets + route distinguishers (each tenant's VRF/EVI gets distinct RT/RD), so route import/export is per-tenant-scoped; MAC/IP routes (EVPN type-2) and IP-prefix routes (type-5) only install into the tenant's VRF/VNI. A tenant crossing switch-A or VM-migrating to switch-B does not require its L2 domain to span more than the VTEPs that host it. The overlay eliminates the need for one giant L2 domain: VLANs are only local to the access switch the tenant segments sit on.

The senior building blocks: a BGP RR (route reflector) per tenant-group or pair of spine RRs; consistent RD/RT/DSCP geometry per tenant; per-VNI MAC learning scoped by EVPN; and a naming/DPR (device-profile record) system that ties a tenant's VRF, VNIs, BD, and VLAN together so that "add tenant X to switch Y" is a two-command operation, not a hand-plumbed VLAN across the campus. The failure surface to design for is control-plane bloat: massive EVPN route tables and too many per-tenant VRFs; use route summarization and filter the RR to keep the RR's FIB sane.

## Q97: What is the cost of "flooding a VLAN" compared to routing the same traffic?

**A:** Flooding a VLAN sends the frame to every port in the domain — the cost is O(ports) bandwidth, O(hosts) receive interrupts, and switch CPU punts for every broadcast/unknown-unicast, whether or not the destination exists. Routing sends the frame along the shortest path toward one destination: the cost is per-hop forwarding in the ASIC, plus the routing decision itself, plus the L3 peeling every L2 boundary (which is fine since hosts don't see floods).

The comparison is not about raw speed but about what each does to the network: flooding consumes all links and all host and switch CPUs in proportion to domain size; routing consumes the links along the path and leaves every other link untouched. A 500-host VLAN with heavy ARP or chatty app: flooding adds 500x the CPU interrupts that routing would. The flip side is that routing adds per-hop parse/decision latency and requires L3 awareness at every boundary — a VLAN with most traffic internal (message bus, replication) may route slower than flooding inside the domain.

The senior answer turns this into a design rule: L2 inside the domain is cheap because hosts don't re-encapsulate; L3 at the boundary is cheap because floods never cross it. Place the boundary where floods hurt — right at the point where broadcast size exceeds the cost of the route — and the answer is usually "route boundaries at the access/distribution edge, L2 where the group is small and local."

## Q98: How does the concept of a "MAC-in-IP" encapsulation map to VLAN/MPLS-policy interactions?

**A:** "MAC-in-IP" is the general encapsulation family where the original (inner) Ethernet frame — with its MAC addresses and VLAN tag — is carried inside an IP/UDP or IP tunnel at the outer layer. VXLAN (inner MAC + VLAN → outer IPv4/UDP), NVGRE (GRE key), and Geneve (optional metadata) all defer the L2 semantics into an encapsulation that an IP underlay can route; the inner MAC is not consumed, only carried.

The link to VLAN/MPLS policy: an inner VLAN tag can coexist with an outer MPLS label (MPLS-in-VXLAN, EVPN-MPLS switching) — the inner tag is preserved for L2 services while the outer label selects the VPN/route. Policy onto the outer packet (DSCP, QoS, ACL, ECMP hashing) is made at the VTEP, while the inner headers remain opaque to the transit network — which is both a feature (isolation) and a risk (inner spoofing/integrity must be verified at egress).

The senior consequence: the VTEP is the policy boundary, and the translation between inner (VLAN/MPLS/segmentation) and outer (IP/UDP/DSCP) happens there. Whether the overlay is EVPN-VXLAN or MPLS, the MAC-in-IP model means L2 services survive a routed transport; the design decision is where to terminate that translation (at each access leaf) and how inner-permitted policy maps to outer marking so the fabric's QoS/ACL story talks the same language as the tenant's. It is exactly this layering that lets EVPN unify L2 and L3 VPNs on one control plane.

## Q99: What are the failure modes of an MSTP region misconfiguration?

**A:** An MSTP region misconfiguration means the region name, revision number, or the VLAN-to-instance mapping differ between switches on the same link. MSTP treats switches with different configuration as belonging to separate regions and places a boundary between them. The visible damage depends on where the mismatch is: two region-adjacent switches run the CIST (region spanning tree) across the boundary, and per-instance load-balancing (VLAN1 on path A, VLAN2 on path B) silently stops working — every VLAN now flows along the CIST path.

Silent starvation is the classic failure: both instances' load-balancing disappears, one link saturates while its peer idles, and "why is the 10G link pinned but the 9.9G link empty?" confuses operators. Worse, if the boundary coincides with a single physical link, that link becomes the only crossing for potentially all VLANs — a failure and performance single point that topology changes cannot reroute because the region boundary does not move.

Troubleshooting order: `show spanning-tree mst configuration` across the fabric, diff region name/revision/VLAN-map, and re-issue identical config everywhere. MSC (mismatch) logs on the port point to the offending link. The senior discipline is configuration validation: MSTP correctness is a fabric-wide invariant, not a per-switch setting — Zero-touch config management (NetBox/Ansible) and change gating are the practical guarantees that a one-switch typo cannot silently re-route an entire region into a bottleneck.

## Q100: How would you architect "no spanning tree needed at all" in a campus?

**A:** The honest answer is that a campus cannot generally eliminate STP entirely, but it can confine it to triviality: the goal is a topology where STP has no redundant L2 path to block, and therefore no role in deciding data paths. The pattern is "routed everywhere": every access switch terminates VLANs and subnets itself (no VLANs across the fabric), access-to-distribution runs routed L3 links (OSPF or eBGP), and the core/distribution fabric is fully L3 with ECMP. L2 exists only inside the access switch's own VLAN — which is then edge (PortFast) with no STP-redundancy anywhere.

Where L2 stretch is unavoidable (VM mobility, shared storage VLAN), the correct replacement is an overlay: EVPN-VXLAN terminated at the access switch, so the underlay is routed (no STP across the fabric) and the overlay's L2 semantics live on the VTEP — the MAC learning and forwarding that STP used to arbitrate are now handled by the EVPN control plane, not by blocking-links or timers. STP still technically runs on the residual L2 boundaries (the access switch's own bridging domain) but it is trivially acyclic and converges instantly because there is no redundancy to arbitrate.

The senior caution: "no STP" is achievable only if the L3 plane is fully designed — routing protocols, convergence targets, ECMP hashing, and summarization all become the availability story instead of spanning tree. It is a deliberate exchange: simpler L2 and no STP-tuning, at the cost of rigorous L3 S.O.P. and EVPN discipline. Teams that mistake "no L2 topology" for "no routing investment" will trade one failure family (STP loops) for another (routing convergence and BGP hygiene) — the architecture is better and simpler only when the L3/EVPN machinery is operated with the same care L2 got.

