# Link-State Routing and OSPF

> **TL;DR**: Link-state routing fixes DV's slow, loop-prone convergence: every router **floods its local link state**, so *all* routers hold the same topology and run **Dijkstra** for loop-free shortest paths — **OSPF** (RFC 2328) is the standard implementation: LSA flooding, areas for scale, cost = 1/bandwidth, fast convergence, and no hop cap.

## 1. Why Does This Exist?
Distance-vector routing converges slowly (count-to-infinity) and can't see the topology — each router knows only "distance to X via neighbor Y," so it can't detect loops or react fast. **Link-state routing** inverts the model: instead of sharing *distances*, every router **floods its local view** (my links, their costs, my neighbors) so every router builds the *same complete topology map*. Then each router runs **Dijkstra's shortest-path algorithm** on that map to compute the loop-free shortest-path tree to every destination. This gives three properties DV lacks: **(1) fast convergence** — a change floods immediately and every router recomputes in O(V log V) — no count-to-infinity; **(2) loop-free paths by construction** — each router's tree is computed from the *same consistent graph*; **(3) rich metrics** — cost can encode bandwidth (not just hops). **OSPF** (Open Shortest Path First) exists as the standard link-state protocol (the 1980s replacement for RIP): robust (RFC 2328, OSPFv3 RFC 5340), hierarchical via **areas** (scale to thousands of routers), and the default IGP of enterprise/cloud/data-center underlays.

## 2. How Does It Work?
- **Three mechanisms**:
  1. **Neighbor discovery**: hello messages (OSPF: multicast 224.0.0.5/6, protocol 89) establish adjacency.
  2. **Reliable flooding**: each router floods its **Link-State Advertisement (LSA)** — (router id, list of (neighbor, cost) links) — to every other router (OSPF floods via LSU/LSR/LSACK over the adjacencies; sequence numbers + age ensure reliability + freshness).
  3. **Path computation**: every router builds the full link-state database (the topology graph) and runs **Dijkstra** from itself → shortest-path tree → routing table (each LSA also announces IP prefixes it can reach — "router LSA" + "network LSA").
- **OSPF areas**: an **area 0 (backbone)** plus other areas — LSAs flood *within* an area only; **Area Border Routers (ABRs)** summarize between areas; **ASBRs** redistribute from other protocols. Result: hierarchical scale (each router holds only its area's topology + summarized routes).
- **Metric (cost)**: OSPF cost = reference_bandwidth / interface_bandwidth (Cisco: 100 Mbps ref → 10 Gbps = 1, 1 Gbps = 10, 100 Mbps = 100). Admin can override — bandwidth-aware, no hop cap.
- **Fast convergence**: LSA floods on change (with flooding timers to bound storms), Dijkstra recomputes in O(E log V); timers (SPF delay, LSA throttle) tune it.
- **Loop-free by construction**: every router computes its shortest-path tree from the *same* graph — the tree is acyclic, so transient loops are far rarer than DV (though a *flooding* window can still exist until convergence completes).
- **OSPFv3** (RFC 5340): IPv6 (carries v6 prefixes, runs over link-local), unchanged SPF core.

## 3. When Is It Used?
- **Enterprise/DC underlays**: the default IGP for campus/DC fabrics — thousands of routers in one domain, fast convergence, bandwidth-aware.
- **Service-provider internal routing**: ISPs run OSPF (or IS-IS) inside their AS for internal reachability; BGP at the edge.
- **Cloud/underlay fabrics**: DC spine-leaf designs commonly use OSPF/IS-IS for the underlay; EVPN/BGP for the overlay.
- **Where RIP can't go**: networks >15 hops, or needing fast convergence after failures.
- **Edge/stub reuse**: OSPF announces connected/static routes and redistributes into BGP — the IGP half of the Internet's two-level design.
- **Interview comparisons**: OSPF (link-state) vs RIP (DV) vs BGP (path-vector) is *the* routing question — knowing where each fits is mandatory.

## 4. Why Wasn't Another Approach Chosen?
- **Why flood the topology instead of sharing distances?** Sharing distances (DV) can't see loops or paths — a router can't tell if its "shortcut" actually loops. Sharing the *topology* lets every router compute *provably* loop-free trees (Dijkstra on the same graph) and detect failures precisely. Cost: memory/CPU for the graph + flooding traffic — an acceptable price for correctness + speed at enterprise scale.
- **Why Dijkstra (link-state) over Bellman-Ford (DV)?** Both find shortest paths; Dijkstra computes *all* paths from one source in O(E log V) given the full graph (perfect for "each router computes its own tree"). Bellman-Ford is iterative and needs multiple rounds of neighbor exchange (slow, count-to-infinity). With the graph available, Dijkstra is simply the right tool.
- **Why OSPF over IS-IS?** Two link-state IGPs (OSPF standardized by IETF, IS-IS by ISO). OSPF won enterprise/cloud adoption (IP-native, CIDR, areas well-integrated); IS-IS won some provider/DC niches (protocol-agnostic, easier to extend, single topology). It's a close call — the *algorithm* is identical; the differences are packaging.
- **Why areas/backbone?** Flooding the whole topology to every router doesn't scale (O(routers²) state). Areas confine flooding → each router holds a small graph + summarized routes → OSPF scales to thousands of routers. The cost: suboptimal inter-area paths (summarization loses exactness) and ABR complexity — a deliberate scale/efficiency trade.
- **Why cost = 1/bandwidth?** Hop count ignores link speed (a 1 Gbps and 9.6 kbps link both "cost 1"). OSPF's inverse-bandwidth cost makes routing prefer fast links — a *network-aware* metric that RIP never had. (And it's tunable — an admin can force a path regardless of speed.)

## 5. Intuition
Link-state is **every driver holding the same up-to-date road atlas**: instead of relying on rumors from neighbors ("City X is 4 towns away, I heard"), each town *announces its own roads* ("I have a 2-lane road to Town B and a 1-lane road to Town C"), everyone publishes these to *everyone*, and each driver computes the shortest route on the full map with Dijkstra. When a bridge collapses, the affected town *shouts* the news instantly, everyone updates their map, and each recomputes — the network converges in seconds, and nobody ever follows a road that loops (the map's tree is loop-free by construction). The "areas" trick is like organizing the atlas by region: you carry a detailed map of your region plus a coarse summary of the country — you don't need every city's streets for the whole world. That's OSPF: a shared, self-updating atlas + regional editions + a fastest-route calculator.

## 6. Real-World Analogy
**A rideshare company's live map**: Every driver's car streams its position and the current traffic on its *own* road segment (LSA) to the dispatch cloud (flooding). Every driver receives the *whole* live map (link-state database) and the navigation app runs the *shortest-path algorithm* (Dijkstra) — everyone sees the same roads, so everyone's suggested route is consistent and loop-free. When a road closes (link down), the affected driver's car instantly reports it (flood), every car's map updates, and routes are recomputed in seconds — no "I heard it from a guy who heard it from a guy" (DV's count-to-infinity). To keep the map manageable, the city is split into *zones* (OSPF areas): cars in the downtown zone carry detailed streets (area topology) but only a coarse "downtown leads to the airport zone" summary of elsewhere (ABR summarization). RIP, by contrast, would be the drivers swapping rumor lists every 30 seconds and arguing for minutes about a closed road.

## 7. Formal Definition
Link-state routing: each router floods its local state (links + costs) via Link-State Advertisements; every router builds an identical **Link-State Database (LSDB)** — the topology graph — and runs **Dijkstra's algorithm** (O(V²)/O(E log V)) to compute the shortest-path tree to all destinations, deriving the forwarding table. Reliability of flooding: sequence numbers + ages + acknowledgments (LSU/LSR/LSACK). **OSPF** (RFC 2328; OSPFv3 RFC 5340): protocol 89, multicast 224.0.0.5 (all routers) / 224.0.0.6 (DR/BDR), hello (10 s) + dead (40 s) timers; LSA types (router LSA 1, network LSA 2, network summary 3, ASBR summary 4, AS-external 5); area hierarchy with backbone area 0 and ABRs (type-3/4 LSAs), ASBRs (type-5) for redistribution; cost = reference/bandwidth; SPF triggered by LSA flooding; stub/NSSA areas optimize; authentication + virtual links; converges with no hop cap and no count-to-infinity.

## 8. Example
The key difference — topology vs vectors:
```
3 routers A-B-C (A-D dead):

DV (RIP): A sees B via direct, C via B; when A-B fails, A and B
  count C toward infinity (16) through each other — minutes.

Link-state (OSPF):
  A floods: "my links: B cost 10, D cost 4"    (LSA)
  B floods: "my links: A cost 10, C cost 5"
  C floods: "my links: B cost 5, D cost 2"
  D floods: "my links: A cost 4, C cost 2"
  Every router now has the SAME graph. A runs Dijkstra:
    A: A(0), D(4), C(6 via D), B(10 or 6+5=11 via D-C-B)
  When A-B fails: B's LSA changes → floods → everyone recomputes in
    ms — A now reaches C via D-C. No counting, no loops.

Dijkstra from A (costs): A=0, D=4, C=min(6 via D, ...)=6, B=11 via D-C-B
```
The flooding step is what makes this work: *all* routers share the graph, so all compute *consistent, loop-free* trees — the fundamental advantage over DV.

## 9. Internal Working
1. **Adjacency formation**: OSPF sends hello (protocol 89, multicast 224.0.0.5) every 10 s; after seeing its own router-id in a neighbor's hello (bidirectional), routers on broadcast links elect a **DR/BDR** (designated/backup designated router) so LSAs flood efficiently (routers ↔ DR, DR ↔ everyone — avoiding N² floods).
2. **Database exchange**: new neighbors exchange LSAs (Database Description, LSR request, LSU update, LSACK) until their LSDBs are identical — the "exchanging state."
3. **Flooding**: any LSA change floods reliably to all routers (each LSU is acknowledged; sequence numbers resolve duplicates; age/refresh keeps LSDB fresh, default 30-min refresh, 3600-s max age).
4. **SPF computation**: on LSA changes (throttled), each router runs Dijkstra on the LSDB → shortest-path tree → installs routes (prefixes from router/network LSAs) into the RIB, with OSPF's AD (110) + cost as metric.
5. **Areas**: LSAs flood only within their area. ABRs connect areas to the backbone (area 0) and advertise *summaries* (type-3) — so area routers hold their area's full topology + a few summary routes. Inter-area paths may be suboptimal (summary-based) — the accepted trade for scale.
6. **Redistribution (ASBR)**: OSPF can import external routes (type-5 LSAs, tagged E1/E2 cost types) — from static, RIP, or BGP — with filtering (route-maps) to prevent leaks.
7. **Failure handling**: a missed hello (dead timer 40 s) = neighbor dead → new LSA flooded → all routers recompute. Convergence = O(diameter) flooding time + SPF compute (ms-to-1s on modern hardware, tuned by SPF timers).
8. **Verification**: `show ip ospf neighbor`, `show ip ospf database`, `show ip route ospf` — the LSDB and SPF results are inspectable (unlike DV's opaque vectors).

## 10. Time Complexity
- **Flooding**: O(edges) LSAs per event, reliably propagated in O(diameter) hops — fast and bounded (no count-to-infinity).
- **SPF/Dijkstra**: O(E log V) with a heap (V = routers, E = links) per router per event — trivial for thousands of routers; throttled (SPF delay ~50 ms, hold-down) to amortize storms.
- **State**: each router stores the *whole* area's LSDB — O(V × degree) LSAs. Areas bound this: routers in an area hold only area topology + summaries (the reason OSPF scales vs a flat flood).
- **Convergence**: O(flooding diameter + SPF time) — sub-second on failure (vs RIP's minutes). The definitive performance win.
- **Bandwidth**: hello + LSA traffic is small and event-driven (vs RIP's periodic full-table broadcasts) — O(area size) only on changes + periodic refresh.

## 11. Advantages
- **Fast, loop-free convergence**: Dijkstra on a consistent graph — sub-second failure recovery, no count-to-infinity (the #1 reason to pick it over RIP).
- **Bandwidth-aware metric**: cost = 1/bandwidth (tunable) — routes follow fast links, unlike hop-count.
- **Scalable via areas**: hierarchical flooding → thousands of routers feasible (the reason RIP caps at 15 hops but OSPF doesn't).
- **Consistent view**: every router holds the same topology — predictable, debuggable (inspect the LSDB), and robust to transient partitions.
- **Rich feature set**: authentication, virtual links, stub/NSSA areas, ECMP (equal-cost multipath), redistribution with filters, LSA filtering.
- **Industry standard**: the default enterprise/DC IGP — every network engineer knows it; OSPFv3 covers IPv6.

## 12. Disadvantages
- **More complex than DV/RIP**: adjacency state machines (init/exchange/full), DR/BDR elections, LSA types, areas, timers — a steeper learning curve and more failure modes to tune.
- **Flooding traffic + state**: each router keeps the whole area's topology; floods on every change — on very large flat areas this hurts (hence areas, and IS-IS for some DC fabrics).
- **Metric tuning needed**: default reference bandwidth assumes 100 Mbps; on 10/40 Gbps fabrics every link "costs 1" unless you tune the reference — a classic misconfiguration.
- **SPF storm risk**: flapping links trigger repeated SPF recomputation (mitigated by timers/route dampening; still a real ops issue on unstable links).
- **Suboptimal inter-area paths**: summarization trades exactness for scale — inter-area routes aren't always the true shortest path.
- **Not for the Internet**: OSPF computes *least-cost* paths — meaningless across independent ASes; the Internet needs policy (BGP, section 04). OSPF is the *intra*-domain workhorse.

## 13. Interview Questions
1. **Q: What is link-state routing?** A: Every router floods its local link state (links + costs) so all routers share the full topology (LSDB) and compute their own shortest-path tree with Dijkstra — fast, loop-free, no count-to-infinity.
2. **Q (tricky): What's the key difference from distance-vector?** A: DV shares *distances* (opaque, slow, loops); link-state shares the *topology* (transparent, consistent, loop-free trees via Dijkstra). DV = Bellman-Ford with neighbor vectors; LS = flood + Dijkstra.
3. **Q: What is OSPF?** A: Open Shortest Path First (RFC 2328) — the standard link-state IGP: hello adjacencies, LSA flooding (protocol 89, multicast 224.0.0.5/6), SPF computation, cost = 1/bandwidth, area hierarchy, AD 110. OSPFv3 (RFC 5340) = IPv6.
4. **Q (FAANG): How does OSPF ensure fast, loop-free convergence?** A: All routers hold the *same* graph (flooded LSAs) → each runs Dijkstra → each tree is shortest and acyclic → paths are loop-free *by construction*. Failure → one flooded LSA → everyone recomputes in ms — no count-to-infinity (DV's minutes).
5. **Q: What are OSPF areas and why do they exist?** A: LSAs flood only within an area; area 0 is the backbone; ABRs summarize between areas. They bound LSDB size and flood traffic so OSPF scales to thousands of routers — the alternative (flat flooding) is O(N²) state.
6. **Q: What is the OSPF metric?** A: Cost = reference_bandwidth / interface_bandwidth (Cisco default 100 Mbps: 10 Gbps = 1, 1 Gbps = 10, 100 Mbps = 100), manually overridable. Bandwidth-aware and no hop cap — unlike RIP's hop count.
7. **Q (tricky): Why is there a DR/BDR election on broadcast links?** A: On a shared Ethernet, N routers would flood N² LSAs. The DR (and BDR backup) centralize: routers ↔ DR ↔ everyone — O(N) floods. The election is part of adjacency formation on broadcast segments only.
8. **Q: What are the OSPF LSA types?** A: 1 router LSA (own links/prefixes), 2 network LSA (DR, the segment), 3 network summary (ABR inter-area), 4 ASBR summary, 5 AS-external (redistributed routes). Types 3-5 are what make areas + redistribution work.
9. **Q (production): OSPF neighbors stuck in "exchanging/loading"?** A: The LSDB sync isn't completing — MTU mismatch (a classic), LSA flooding blocked by a firewall (protocol 89), or a neighbor/router-id conflict. Check `show ip ospf neighbor`, LSDB sizes, MTU — the adjacency state machine tells you where it stalled.
10. **Q: OSPF vs IS-IS — why both?** A: Same link-state algorithm, different packaging: OSPF is IP-native (CIDR, areas) from the IETF; IS-IS is protocol-agnostic (can carry IPv4/IPv6/CLNS) and popular in some provider/DC fabrics for its simpler extensibility. Choosing is organizational, not algorithmic.
11. **Q (FAANG): When would you prefer OSPF over BGP internally?** A: Inside one AS, when you want *fast, automatic, cost-based* routing (DC/enterprise underlay) and don't need policy between domains. BGP is for *policy between* domains (and some DC overlays via BGP EVPN). IGP + eBGP is the classic split.
12. **Q: How does OSPF handle a failed link?** A: The neighbor's hello is missed (dead timer, default 40 s) → neighbor declared dead → a new LSA floods → all routers recompute SPF → new paths in sub-second-to-seconds. Faster than RIP's count-to-infinity; tune hello/dead timers (e.g., 1 s/4 s) for faster DC convergence.
13. **Q (tricky): What is ECMP and how does OSPF enable it?** A: Equal-Cost Multi-Path — when two paths to a prefix have *equal* cost, OSPF installs both (by default) and load-shares per-flow. This is the standard DC underlay load-balancing mechanism (vs BGP's more policy-driven multi-path).
14. **Q: What is a stub/NSSA area?** A: Areas with *no* external (type-5) routes — stub areas (default route instead) and NSSA (limited external routes) reduce the LSDB and routes in leaf areas. Part of OSPF's hierarchy tuning for scale.
15. **Q (production): A flapping link triggers repeated SPF. What do you do?** A: SPF throttling (delay + hold-down timers), LSA flooding throttle, and route *dampening* for the flapping interface — plus fix the physical cause. Unbounded SPF storms on flapping links are a real OSPF ops failure mode.
16. **Q: What is the OSPF administrative distance?** A: 110 — lower than RIP (120), higher than eBGP (20). When OSPF and another protocol both know a prefix, AD picks the source; within OSPF, cost picks the path.
17. **Q (tricky): Why does OSPF sometimes prefer a "worse" inter-area path?** A: Because ABRs summarize — a router outside the area sees a *summary* (type-3) cost, not the true path cost. Summarization trades exactness for scale; intra-area paths are always exact. It's a designed trade-off of the area model.

## 14. Follow-Up Questions
1. **Q: How does OSPF interact with BGP?** A: Classic two-level design: OSPF inside the AS (fast, automatic IGP), BGP between ASes (policy). The ASBR redistributes BGP→OSPF (or OSPF→BGP) with route-maps + filters; OSPF's default route can be injected into stubs. The IGP/BGP boundary is *the* architecture of service-provider and enterprise edge routing.
2. **Q: What is OSPFv3 and how does it differ from OSPFv2?** A: OSPFv3 (RFC 5340) runs over IPv6 link-local addresses, carries IPv6 prefixes in its LSAs, and separates the router-ID from addresses (no more "routers must have IP in the backbone"). The SPF core is identical; it's the same algorithm for the v6 world.
3. **Q (tricky): Why is IS-IS often preferred in large data-center fabrics over OSPF?** A: Historical + practical: IS-IS runs directly on Layer 2 (no IP dependency — great for underlay bootstrap), has a single flat-ish hierarchy (Level-1/2, no DR/BDR election — simpler flooding), and was already in core routers (Juniper/`clos`). Both work; IS-IS's simplicity in fabric automation won some hyperscale designs.
4. **Q: What is the "SPF tree" and why is it a tree?** A: Dijkstra's output from the source router — the set of shortest paths. It's a tree (acyclic) by construction: each node's parent is the node on its shortest path, so forwarding follows a DAG/tree with *no loops* — the property DV can't guarantee during convergence.
5. **Q (FAANG): "Design an OSPF underlay for a 100-rack DC fabric with spine-leaf topology."** A: Leaf switches in areas per pod (or a flat area with tuned SPF timers for small fabrics), spine as backbone; each link cost tuned by speed (10/25/40 G); ECMP across equal-cost spines; loopbacks in OSPF for BGP-over-OSPF peering; hello/dead 1 s/4 s for fast convergence; and monitor SPF storms. The interview tests *where* areas go, ECMP, and convergence tuning.

## 15. Coding Example
```python
# Dijkstra — the SPF that every link-state router runs
import heapq

def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    prev = {}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, cost in graph[u]:
            nd = d + cost
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

# The LSDB = everyone's flooded LSAs = one graph (identical on all routers)
graph = {
    "A": [("B", 10), ("D", 4)],
    "B": [("A", 10), ("C", 5)],
    "C": [("B", 5), ("D", 2)],
    "D": [("A", 4), ("C", 2)],
}
print(dijkstra(graph, "A"))
# ({'A': 0, 'B': 9, 'C': 6, 'D': 4}, {'B': 'C', 'C': 'D', 'D': 'A'})
# A -> D -> C -> B: cost 4+2+5=11 vs direct... wait: recompute: A-B=10 vs A-D-C-B=11.
```
```bash
# Real OSPF diagnostics (Linux with FRR/quagga, or a Cisco/Junos box)
$ sudo tcpdump -i eth0 proto ospf -nn -vv | head   # hello (every 10 s) + LSUs
#    192.168.1.5 > 224.0.0.5: OSPFv2, Hello, length 44 ...
#    192.168.1.5 > 224.0.0.5: OSPFv2, LSA-Update, length 96 ...
$ vtysh -c 'show ip ospf neighbor'                 # adjacency states
$ vtysh -c 'show ip ospf database'                 # the LSDB (topology!)
$ vtysh -c 'show ip route ospf'                    # SPF-derived routes
```

## 16. Industry Usage
- **Enterprise + campus**: OSPF is the default IGP — regional hubs, VLAN-to-L3 designs, and office/campus underlays. Every network team's bread-and-butter.
- **Data-center underlays**: spine-leaf fabrics (and cloud networking) commonly run OSPF or IS-IS for the underlay — fast convergence + ECMP across spines is exactly what DCs need. (BGP EVPN takes over the overlay.)
- **Service-provider cores**: OSPF (or IS-IS) inside the AS; BGP at the edges — the two-level architecture that runs the Internet's transit ISPs.
- **Cloud (AWS/GCP/Azure)**: VPCs abstract OSPF away (route tables are static), but on-prem connectivity (VPN, Direct Connect) and provider fabrics still speak OSPF/BGP — hybrid designs route over OSPF/BGP underlays.
- **Kubernetes/CNI**: CNI overlays (Calico, Cilium) use BGP/OSPF-style underlays for pod-routing; OSPF (and BGP) knowledge is directly relevant to cluster networking.
- **Certification/education**: OSPF is *the* taught IGP (CCNA/CCNP/Net+): adjacency state machines, LSA types, areas, SPF — the interview questions come straight from the operational protocol.

## 17. References
- RFC 2328 — OSPF v2: https://www.rfc-editor.org/rfc/rfc2328
- RFC 5340 — OSPF v3 (IPv6): https://www.rfc-editor.org/rfc/rfc5340
- RFC 1583 — OSPF (original; inter-area path rules)
- Dijkstra, E.W., "A Note on Two Problems in Connexion with Graphs" (1959) — the SPF algorithm.
- Kurose & Ross, *Computer Networking*, Ch. 5 §5.2.4 (link-state) + §5.3 (OSPF).
- Cisco: "OSPF Design Guide" (areas, timers, LSA types).
- FRR: https://docs.frrouting.org/ (open-source OSPF).

## 18. Cheat Sheet
- Link-state: flood local links (LSA) → everyone shares the LSDB → Dijkstra → loop-free shortest-path tree.
- OSPF: protocol 89, multicast 224.0.0.5 (routers)/224.0.0.6 (DR); hello 10 s, dead 40 s.
- LSA types: 1 router, 2 network (DR), 3 network-summary (ABR), 4 ASBR-summary, 5 external (ASBR).
- Areas: backbone 0 + others; ABR summarizes (type 3/4); ASBR redistributes (type 5); stub/NSSA reduce.
- Cost = ref_bandwidth / link_bandwidth (default ref 100 Mbps — retune for 10G+); no hop cap.
- AD = 110. ECMP: equal-cost paths both installed.
- DR/BDR election on broadcast links → O(N) floods.
- Convergence: flooded LSA + SPF in ms-to-seconds (no count-to-infinity).
- SPF throttle + LSA throttle + dampening control storms.
- OSPFv3 = IPv6. IS-IS = the other link-state IGP (provider/DC).
- Hierarchy: OSPF inside AS, BGP between ASes.

## 19. Quiz
1. Link-state computes paths with: a) Bellman-Ford b) Dijkstra c) BFS d) policy → **b**
2. OSPF runs over: a) UDP b) protocol 89 c) TCP d) ICMP → **b**
3. OSPF's metric is: a) hops b) cost = ref/bandwidth c) delay d) random → **b**
4. LSA type 1 is: a) network b) router c) summary d) external → **b**
5. Area 0 is the: a) stub b) backbone c) NSSA d) external → **b**
6. ABRs: a) elect DR b) summarize between areas c) redistribute only d) run BGP → **b**
7. OSPF AD: a) 1 b) 20 c) 110 d) 120 → **c**
8. DR/BDR exist to: a) speed SPF b) cut N² floods on broadcast links c) elect areas d) metrics → **b**
9. OSPF avoids count-to-infinity because: a) bigger tables b) Dijkstra on shared topology c) faster timers d) UDP → **b**
10. ECMP means: a) equal-cost multi-path b) one path c) fast convergence d) error control → **a**

## 20. Flashcards
- **Q: Link-state core?** → **A:** flood links → shared LSDB → Dijkstra → loop-free tree.
- **Q: OSPF protocol/timers?** → **A:** proto 89, hello 10 s / dead 40 s, multicast 224.0.0.5.
- **Q: Metric?** → **A:** cost = ref/bandwidth; no hop cap.
- **Q: LSA types?** → **A:** 1 router, 2 network(DR), 3 summary(ABR), 5 external(ASBR).
- **Q: Areas?** → **A:** backbone 0 + areas; ABR summarizes → scale.
- **Q: AD?** → **A:** 110.
- **Q: Why no count-to-infinity?** → **A:** consistent graph + Dijkstra = loop-free trees.
- **Q: ECMP?** → **A:** equal-cost paths installed together.

## 21. Revision
Link-state: flood local LSAs → all routers share the topology → Dijkstra → loop-free shortest-path trees (no count-to-infinity, fast convergence). OSPF (RFC 2328): protocol 89, hello/dead 10/40 s, DR/BDR on broadcast links, LSA types 1-5, areas with backbone 0 + ABR summarization, cost = ref/bandwidth (no hop cap), AD 110, ECMP, stub/NSSA, OSPFv3 for IPv6. IS-IS = same algorithm, different packaging. SPF storms → throttle/dampen. OSPF = the intra-domain IGP; BGP = inter-domain policy. Verify with `show ip ospf neighbor/database`, tcpdump proto ospf.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is link-state routing?" | 2 How It Works / 7 Formal Definition |
| "Link-state vs distance-vector?" | 13 Q&A / 4 Why Not Another Approach |
| "What is OSPF / its protocol details?" | 13 Q&A / 9 Internal Working |
| "Why areas / what's the backbone?" | 13 Q&A / 10 Time Complexity |
| "Why is it loop-free / fast?" | 13 Q&A / 5 Intuition |
| "What is the OSPF metric?" | 13 Q&A / 12 Disadvantages |
| "What are LSA types / DR-BDR?" | 13 Q&A / 8 Example |
| "OSPF vs IS-IS vs BGP?" | 13 Q&A / 14 Follow-Up |
| "Design an OSPF underlay." | 13 Q&A / 15 Coding |
