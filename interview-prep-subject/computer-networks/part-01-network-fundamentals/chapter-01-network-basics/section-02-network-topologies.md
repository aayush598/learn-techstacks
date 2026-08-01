# Network Topologies

> **TL;DR**: A topology is the layout of how nodes and links are connected — physical (wiring) and logical (data path) — and it exists because the arrangement of connections determines cost, fault tolerance, scalability, and how congestion/collisions behave in a network.

## 1. Why Does This Exist?
Once you have multiple devices, you must decide *how to wire them together*. The choice isn't arbitrary: topology is the single biggest driver of three engineering properties: **(1) cost** (how much cable and how many ports), **(2) fault tolerance** (what happens when a cable or node dies), and **(3) scalability** (can you add nodes cheaply?). Designers choose a topology to match the reliability budget and budget constraints. This is a design-decision layer of networking, not a protocol layer.

## 2. How Does It Work?
A topology defines the connection graph: `nodes (devices) + links (edges)`. Physical topology = actual cable/radio layout; logical topology = the path data actually takes (which can differ — a *logical ring* can run over a *physical star*, e.g., Token Ring over a hub). Topologies are evaluated on: cost per node, fault tolerance (single point of failure?), ease of adding/removing nodes, performance under load (collision domains, contention), and management complexity.

## 3. When Is It Used?
- **Bus**: legacy Ethernet (10BASE2/10BASE5 thinnet/thicknet); rarely used today. Still relevant conceptually for understanding shared-medium contention.
- **Star**: the dominant topology in practice — office LANs and datacenters (each host → one switch).
- **Ring**: legacy Token Ring (IBM), FDDI (fiber rings for MANs). Used in *topology* terms for SONET/SDH rings in telecom.
- **Mesh**: the Internet backbone (router mesh), datacenter fabrics (fat-tree/leaf-spine = structured mesh), wireless mesh (Wi-Fi repeaters), and **full mesh** for critical core networks (only a handful of nodes).
- **Tree/hierarchical**: campus networks, enterprise networks (access → distribution → core), and modern datacenter (ToR → spine).
- **Hybrid**: real networks combine topologies — a star-of-stars, ring-of-stars, etc.

## 4. Why Wasn't Another Approach Chosen?
Each topology solves one problem and creates another — the trade-off is fundamental:
- **Bus vs star**: bus is cheapest (one cable) but any break or added node disrupts everyone (shared collision domain). Star centralizes wiring at a switch, isolating faults but requiring a hub/switch and more cabling. When switches got cheap, star won.
- **Ring vs star**: rings give *deterministic* token access (no collisions) and pass a message around even if one node fails (with dual rings), but a broken link can partition the ring and latency scales with size. Stars are simpler and the switch does the scheduling.
- **Mesh vs star**: mesh has no single point of failure and huge aggregate bandwidth, but wiring cost is quadratic (N(N-1)/2 links for full mesh). Star has a single point of failure (the switch) but is linear in cost. Real systems use *partial mesh* at the core, star at the edge — a hybrid.
- **Logical vs physical**: using a logical ring on physical star (Token Ring) let the protocol behave deterministically while wiring cheaply — rejected when Ethernet's CSMA/CD + switches made shared medium unnecessary.

## 5. Intuition
Topology is the "seating chart" of your network. Star = everyone at one dinner table (the switch) passing dishes; bus = people sitting along one long bench passing plates down the line (everyone on the bench hears everything and can only talk one at a time); ring = a circle of people each passing notes to the next person in line; mesh = everyone can whisper directly to anyone. The difference between *physical* and *logical* is like a party where people are seated at round tables (physical) but agree to pass notes clockwise (logical ring).

## 6. Real-World Analogy
**Road networks**: bus = one-lane road with everyone's driveway on it (any crash blocks everyone); star = all roads lead to one central roundabout (roundabout fails → town isolated); ring = a ring-road with exits (works with one lane broken if you have the inner ring, i.e., dual-ring); mesh = city grid with many alternate routes (any road can close and you reroute — this is why the Internet mesh is resilient). 

## 7. Formal Definition
A network topology is the arrangement of nodes and links in a communication network. The **physical topology** describes the actual geometric and physical layout of the transmission media; the **logical topology** describes the path that data packets take as they traverse the network. A *collision domain* is the set of devices that can "hear" each other's transmissions on a shared medium; a *broadcast domain* is the set of devices that receive a broadcast frame (usually bounded by a router).

## 8. Example
Consider a 5-node LAN under two designs:
- **Bus (10BASE2)**: one coaxial cable, all 5 nodes tap in. Cost = 1 cable + 5 taps. Any cable cut → entire LAN down. Only one node may transmit at a time (shared 10 Mbps → per-node share ≈ 2 Mbps avg under load).
- **Star (10BASE-T + switch)**: 5 cables from nodes to one switch. Cost = 5 cables + 1 switch (8-port). A node's cable dying affects only that node. The switch forwards frames per port, giving each link full 10 Mbps (collision-free full duplex on each port).
- **Full mesh (backbone)**: if these 5 are *routers* in a critical core, full mesh = 5×4/2 = **10 links**; each router has 4 interfaces. Any two nodes have a direct path; 4 links can fail without full partition. Cost: 10 cables + 4-port router cards.

## 9. Internal Working
1. **Bus**: all nodes tap a single shared medium. At any instant one node transmits; others *listen*. Two simultaneous transmissions → **collision** → both back off (CSMA/CD). Any physical break or bad connector causes reflections → entire segment fails (terminators needed at both ends, 50Ω).
2. **Star**: central switch is the *point of presence*. Each host has dedicated link; the switch *learns* MAC addresses (MAC table) and forwards frames only to the destination port. Fault isolation per port; switch itself is SPOF (mitigate with dual switches = "stacking" or redundant links).
3. **Ring**: each node regenerates/retransmits to the next. Token passing guarantees deterministic access (no collisions). A single break used to partition; modern rings (FDDI/SONET) are *dual counter-rotating rings* — on a break, traffic wraps around, so a single break doesn't partition.
4. **Mesh**: routers fully/inter-partially connected. Routing protocols (OSPF/BGP) compute alternate paths; a failed link causes convergence to a new shortest path. Full mesh is used only at core tiers; partial mesh scales.
5. **Tree**: hierarchy with access (host-facing), distribution (aggregation + policy), core (fast forwarding). Adding capacity = adding parallel uplinks.

## 10. Time Complexity
- **Cost scaling** (links for full mesh): O(N²) — N(N-1)/2; star: O(N); bus: O(1) (one cable, up to segment limits); ring: O(N).
- **Failure diameter** (worst-case path after failures): mesh ≥ ring ≥ star (single node) ≥ bus (whole segment).
- **Communication latency** (hop count worst case): bus/star = 2 (node→medium→node), ring = O(N/2) (N-1 hops worst case, avg N/2), full mesh = 1 (direct).
- **Reliability**: star SPOF = switch (1 point); full mesh requires N-1 failures to isolate a node.

## 11. Advantages
- **Bus**: cheapest cabling; easy to add a node (tap); no active component (works with zero power beyond NICs — passive).
- **Star**: fault isolation per port; easy to add/remove nodes; central management point; full-duplex per-link speeds.
- **Ring**: deterministic latency (token); fairness; survives single link/node failure with dual-ring.
- **Mesh**: maximum fault tolerance; no single point of failure; high aggregate bandwidth; short paths.
- **Tree**: scales to thousands of nodes; natural hierarchy matches orgs; incremental growth.

## 12. Disadvantages
- **Bus**: entire network dies on a break; shared bandwidth; collision-prone at scale; terminators must be perfect.
- **Star**: switch is SPOF; more cabling (hub-spoke = longer total wire); switch becomes bottleneck/cost center.
- **Ring**: single break partitions (non-dual); latency grows with N; adding/removing a node disrupts the ring.
- **Mesh**: O(N²) cabling/ports — prohibitively expensive beyond ~10 nodes; complex routing; hard to manage.
- **Tree**: upper layers are SPOF-ish; oversubscription at uplinks; failure at distribution isolates whole access segments.

## 13. Interview Questions
1. **Q: What is a network topology?** A: The layout of nodes and links — physical (wiring) and logical (data path). It determines cost, fault tolerance, and performance.
2. **Q: Compare bus, star, ring, and mesh for fault tolerance.** A: Bus — any break kills the segment. Star — switch is SPOF, but port faults isolated. Ring — break partitions unless dual-ring. Mesh — survives multiple failures; only N-1 failures isolate a node.
3. **Q (tricky): What's the difference between physical and logical topology?** A: Physical = actual cabling/layout; logical = the data path. E.g., Token Ring over a star-wired hub: physical star, logical ring. Ethernet over a switch: physical star, logical point-to-point.
4. **Q: Why is full mesh impractical for large networks?** A: Links = N(N-1)/2 — quadratic. 100 nodes need 4950 links and 99 ports per node. Real systems use partial mesh at the core and star at the edge.
5. **Q (scenario): Your office LAN keeps dying when any cable is cut. Which topology are you likely in, and what's the fix?** A: Bus (legacy shared coax). Fix: convert to star with switches. This is exactly what happened in the 1990s Ethernet evolution.
6. **Q: What's a collision domain vs a broadcast domain?** A: Collision domain = devices whose simultaneous transmissions collide (shared medium, e.g., a hub port). Broadcast domain = devices that see each other's broadcast frames (a LAN segment); routers bound broadcast domains.
7. **Q (production): In a datacenter, why is the leaf-spine (fat-tree) topology chosen over full mesh?** A: Fat-tree provides full-bisection bandwidth (any leaf to any leaf with equal bandwidth) using cheap commodity switches in a structured mesh, with O(N) cabling per layer rather than O(N²). Full mesh doesn't scale to thousands of racks.
8. **Q: How does a star topology scale when one switch is full?** A: Two options: *stack* switches (vendor stacking = one logical switch) or go *hierarchical* — add distribution/core switches connecting access switches (tree). Modern approach: top-of-rack (ToR) switches uplinked to spine.
9. **Q (tricky): A logical ring on a physical star — does a node failure break the ring?** A: With a *star-wired ring* (e.g., Token Ring MSAUs), the hub bypasses dead ports, so the ring self-heals — better than physical ring where every node must be up.
10. **Q: Why was Ethernet's bus topology abandoned?** A: Shared medium = collisions (CSMA/CD), segment length limits (185 m for 10BASE2), and total segment failure on any break. Star + switches gives collision-free full-duplex, per-port speed, and fault isolation.
11. **Q: What is oversubscription and which topology introduces it?** A: In a tree, N access switches share M uplinks to the distribution/core. Ratio N:M > 1 = oversubscribed (e.g., 20:1). It exists because most traffic doesn't leave the rack; it's a cost/performance dial. Full mesh has 1:1.
12. **Q (scenario): You're designing a 4-site WAN backbone. Mesh or ring?** A: Full mesh (4 sites = 6 links) gives direct path and redundancy — trivial cost at N=4. At 10+ sites, move to partial mesh or dual-ring.
13. **Q: What does "single point of failure" (SPOF) mean and which topologies have it?** A: A component whose failure takes down the network. Star = the switch; tree = distribution/core; bus = the cable. Ring/mesh avoid a fixed SPOF (ring still partitions on single break unless dual-ring).
14. **Q (practical): How does adding a node to each topology work?** A: Bus — tap the cable (segment length limits). Star — plug into a free switch port. Ring — break the ring, insert node (disruption). Mesh — add links to everyone (or at least to the network's partial-mesh members).
15. **Q: What topology does Wi-Fi use?** A: Logical *star* (infrastructure mode: all clients ↔ AP) over a physical broadcast medium (shared RF channel = one collision domain, though CSMA/CA avoids collisions). Mesh mode exists for repeaters.

## 14. Follow-Up Questions
1. **Q: Why is a hub a physical star but a logical bus?** A: Wiring is star (cables to hub) but the hub *electronically* connects all ports into one shared medium — a single collision domain. A switch makes it a true star (per-port domains).
2. **Q: How do you compute a ring's average hop count?** A: For N nodes, max hops = N-1 (worst direction), average ≈ N/2. Dual-ring and wrap reduce this after failures.
3. **Q: What's the reliability math of partial mesh?** A: With N nodes, degree d (links per node), the network is d-connected: it survives d-1 arbitrary link failures. Choose d from the reliability budget (Internet core ~ d ≥ 3).
4. **Q: What is a "ring of stars" used for?** A: Campus/enterprise backbones — buildings (stars) joined in a ring for redundancy; a break in the inter-building ring still partitions unless dual-ring or the switches are meshed.
5. **Q: Which topology offers the lowest worst-case latency and why?** A: Full mesh (1 hop) for small cores. For scale, tree/fat-tree with fixed diameter (4 hops: host→ToR→spine→ToR→host) keeps latency bounded while scaling — that's why datacenters love it.

## 15. Coding Example
```python
# Compare topologies on link count and failure resilience
import itertools

def links_needed(topology, n):
    if topology == "bus":    return 1
    if topology == "star":   return n          # n spokes to center
    if topology == "ring":   return n          # n-1 + 1 (closing link)
    if topology == "mesh":   return n * (n-1) // 2  # full mesh
    raise ValueError(topology)

def min_failures_to_isolate(topology, n):
    if topology == "bus":    return 1   # one cable cut
    if topology == "star":   return 1   # hub fails
    if topology == "ring":   return 1   # one link breaks the loop
    if topology == "mesh":   return n-1 # all links of a node must fail

for t in ["bus", "star", "ring", "mesh"]:
    for n in [5, 10, 20]:
        print(f"{t:5s} n={n:3d}  links={links_needed(t,n):4d}  "
              f"failures-to-isolate={min_failures_to_isolate(t,n)}")
# bus   n= 5  links=   1  failures-to-isolate=1
# star  n= 5  links=   5  failures-to-isolate=1
# ring  n= 5  links=   5  failures-to-isolate=1
# mesh  n= 5  links=  10  failures-to-isolate=4   <-- quadratic cost, huge resilience
```

## 16. Industry Usage
- **Datacenters (Meta/Amazon/Google)**: *leaf-spine (Clos/fat-tree)* topology — a structured partial mesh. Each ToR (leaf) connects to every spine switch; gives full-bisection bandwidth and 1-2 hops between any racks, and allows adding racks without rewiring.
- **Telecom backbones**: SONET/SDH *dual counter-rotating rings* for metro fiber (50 ms protection switching), plus *partial mesh* at national/international cores.
- **Enterprise campuses**: hierarchical *tree* (access → distribution → core), the classic Cisco three-tier design.
- **Wireless mesh**: municipal Wi-Fi, IoT sensor meshes (Zigbee/Thread use mesh), Wi-Fi 6E repeaters — self-healing on node loss.
- **The Internet itself**: a *mesh of autonomous systems (ASes)* connected at IXPs (Internet exchange points), using BGP to route around failures — mesh resilience at planetary scale.

## 17. References
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 2 (Physical Layer / topologies) and Ch. 3.
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, 8th ed., Ch. 1.2-1.3 (network edge/core).
- Forouzan, *Data Communications and Networking*, 5th ed., Ch. 1.6 (topology).
- IEEE 802.3 (Ethernet standard, bus→star history), IEEE 802.5 (Token Ring).
- Cisco Press, *CCNA 200-301 Official Cert Guide*, Part on LAN Design (access/distribution/core).
- RFC 1918 (private addressing — used in star/tree designs), https://www.rfc-editor.org/rfc/rfc1918

## 18. Cheat Sheet
- Topology = node+link layout; physical vs logical (data path).
- Cost: bus(1 cable) < star(N) ≈ ring(N) << mesh(N(N-1)/2).
- SPOF: bus=cable, star=hub/switch, ring=link(unless dual), mesh=none.
- Star is the practical default (switches); mesh is for critical cores.
- Collision domain bounded by hubs (shared); broadcast domain bounded by routers.
- Token ring = deterministic access; Ethernet = contention (CSMA/CD then switched).
- Datacenter = leaf-spine (Clos) partial mesh, oversubscription ratio.
- Hybrid topologies (star-of-stars, tree) dominate real networks.

## 19. Quiz
1. Which topology has O(N²) link count? a) bus b) star c) ring d) full mesh → **d**
2. A hub is physically star but logically: a) bus b) ring c) mesh d) tree → **a**
3. Single point of failure in a star: a) cable b) the switch c) terminator d) NIC → **b**
4. Which is the cheapest cabling topology? a) mesh b) star c) bus d) ring → **c**
5. FDDI/SONET use what to survive a break? a) hub b) dual counter-rotating rings c) full mesh d) token bus → **b**
6. Broadcast domains are bounded by: a) switches b) hubs c) routers d) repeaters → **c**
7. 10 nodes in full mesh need how many links? a) 10 b) 20 c) 45 d) 100 → **c** (10×9/2)
8. In a tree, oversubscription refers to: a) SPOF b) uplink fan-in ratio c) cable length d) latency → **b**
9. A logical ring over physical star needs what per-port device? a) MSAU/MAU b) repeater c) terminator d) transceiver → **a**
10. Leaf-spine topology is a structured: a) bus b) full mesh c) partial mesh d) ring → **c**

## 20. Flashcards
- **Q: Define physical vs logical topology.** → **A:** Physical = actual wiring; logical = data path (e.g., Token Ring = physical star, logical ring).
- **Q: Link counts?** → **A:** bus=1, star=N, ring=N, full mesh=N(N-1)/2.
- **Q: SPOF of each topology?** → **A:** bus=cable, star=hub, ring=one link (unless dual), mesh=none.
- **Q: What bounds collision vs broadcast domains?** → **A:** Collision = hubs/shared medium; broadcast = routers.
- **Q: Why star won over bus?** → **A:** Fault isolation, full-duplex per port, no shared-medium collisions, cheap switches.
- **Q: Datacenter topology?** → **A:** Leaf-spine (Clos), partial mesh, full-bisection bandwidth.

## 21. Revision
Topology is the connection layout that trades cost against resilience. Bus = one shared cable (cheapest, whole segment dies on a break); star = center switch (fault isolation, but SPOF); ring = token-passing, deterministic, self-heals with dual-ring; mesh = maximum resilience at quadratic cost, used at cores; tree/leaf-spine = scalable hierarchical/structured partial mesh, used in datacenters. Distinguish physical vs logical (Token Ring = physical star/logical ring). Know collision domains (hub/shared medium) vs broadcast domains (router-bounded). Real networks are hybrids.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Compare bus/star/ring/mesh." | 8 Example / 13 Q&A |
| "Why full mesh is impractical?" | Time Complexity / 13 Q&A |
| "Physical vs logical topology?" | 2 How It Works / 13 Q&A |
| "Collision domain vs broadcast domain?" | 7 Formal Definition / 13 Q&A |
| "Why datacenters use leaf-spine?" | 16 Industry Usage / 13 Q&A |
| "What is oversubscription?" | 13 Q&A / Follow-Up |
| "Why did Ethernet abandon the bus?" | 4 Why Another Approach / 13 Q&A |
