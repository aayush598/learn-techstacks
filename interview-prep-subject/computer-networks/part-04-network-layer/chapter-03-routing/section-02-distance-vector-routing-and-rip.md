# Distance-Vector Routing and RIP

> **TL;DR**: Distance-vector (DV) routing runs **distributed Bellman-Ford**: every router tells its neighbors "my distance to each destination," neighbors keep the cheapest, and the best paths propagate hop-by-hop. **RIP** (RFC 2453) is the canonical implementation — hop-count metric, periodic 30-second updates, count-to-infinity (max 16), fixed by split-horizon, poison-reverse, triggered updates, and hold-down.

## 1. Why Does This Exist?
For a router to route, it must know reachable destinations and their costs. **Distance-vector** is the simplest way to compute that *distributedly*: each router needs no global knowledge — it only asks its neighbors "what can you reach, and at what cost?" and adds its own link cost. The **Bellman-Ford** recurrence — `best_dist(d) = min over neighbors (link_cost(neighbor) + neighbor's_dist(d))` — is computed iteratively, locally, and provably converges if the network stops changing. DV exists because it's **simple and decentralized**: no topology flooding, no global database, no coordinator — just "distance + next hop" messages between neighbors. **RIP** (Routing Information Protocol) exists as the 1980s standard implementation (from the ARPANET's routing, standardizing the "distance vector with hop count" approach): trivial to run on small networks, shipped in every OS (routed), and still the *pedagogical* answer to "how does distance-vector actually behave?" because it exhibits every DV concept — convergence, counting-to-infinity, split-horizon — in one simple protocol.

## 2. How Does It Work?
- **The model**: each router keeps a table: (destination → distance, next hop). It periodically (RIP: every 30 s) sends the *entire* table to neighbors as "vectors."
- **Bellman-Ford update**: on receiving a neighbor's vector, for each destination: `new_dist = neighbor_dist + link_cost`; if `new_dist < current`, update (next hop = that neighbor). This is a *relaxation* step repeated until no change (convergence).
- **RIP specifics**: metric = hop count (link cost 1; 16 = infinity); updates via UDP port 520, broadcast/multicast (224.0.0.9); periodic 30 s + triggered updates on change; route timeout 180 s (6 missed updates → mark invalid); garbage-collection 120 s more.
- **Count-to-infinity**: a failed route is propagated as "increased distance" through neighbors that still believe in it — distances increment toward infinity (16) before the network agrees it's gone. This is DV's core failure mode.
- **Fixes**:
  - **Split horizon**: don't advertise a route back to the neighbor you learned it from ("don't teach me my own route").
  - **Poison reverse**: *do* advertise it back, but with distance = infinity (16) — "this route through you is dead."
  - **Triggered updates**: send immediately on change (not waiting for the 30 s timer) — faster propagation.
  - **Hold-down**: after a change, ignore *increases* for a period (let bad news propagate before re-learning worse paths).
  - **Max hop 15** (RIP): bounds the count-to-infinity cost; networks >15 hops need another protocol.
- **Convergence**: RIP can take minutes on failure (each count-to-infinity iteration = a timer cycle) — its defining weakness; OSPF (section 03) exists for fast convergence.

## 3. When Is It Used?
- **Small networks (<15 hops)**: tiny enterprises, labs, small campuses where 30-second convergence and hop-count metrics are fine.
- **Legacy/embedded**: older routers, IoT-ish devices, and the `routed` daemon's world; RIP is still the protocol some CPE/VoIP gear speaks.
- **Educational value (the big one)**: DV + RIP are *the* way to learn routing — every textbook and every interview question about distributed algorithms uses them.
- **DV in disguise**: **BGP** is a *path-vector* (DV's cousin — see section 04); **EIGRP** is a distance-vector with DUAL (feasible successors, loop avoidance — Cisco). Understanding DV explains both.
- **Comparative tooling**: to contrast with link-state (OSPF): RIP = "slow, simple, table exchange"; OSPF = "fast, complex, topology flood." The interview always asks the comparison.

## 4. Why Wasn't Another Approach Chosen?
- **Why "distance vector" (share tables) instead of "share the whole topology" (link-state)?** Simplicity: DV requires *only* your neighbors' distance claims — no topology database, no flood, no global computation. 1980s routers had little memory/CPU; a table of (dest, dist, next-hop) messages was affordable. The cost is slow convergence + count-to-infinity; link-state (section 03) trades memory/CPU for speed.
- **Why hop count as the metric?** Simple, locally computed, no configuration (every link = 1). RIP never needed administrators to assign costs — a "works out of the box" feature. The cost: ignores bandwidth/latency (a 9.6 kbps satellite hop = a 1 Gbps LAN hop), which is why real networks use OSPF cost/BGP policy.
- **Why periodic full-table updates?** Reliable-enough propagation without sequence numbers: resend everything every 30 s so lost updates self-heal. The cost: bandwidth (tables on every timer) + slow propagation of changes — the very thing triggered updates optimize.
- **Why count-to-infinity accepted at all?** Because DV's local knowledge can't *detect* a broken route instantly — it can only *relax* toward it. The fixes (split horizon/poison reverse/triggered/hold-down) bound the damage; 15-hop infinity bounds the *time*. It's a pragmatic compromise that OSPF's topology broadcast later made obsolete for big networks.
- **Why keep RIP at all (vs just teaching OSPF)?** Historical + pedagogical + minimal deployment: it's the smallest complete routing protocol — a perfect baseline for understanding everything else, and genuinely adequate where networks are small and stable.

## 5. Intuition
Distance-vector is the **"grapevine rumor" algorithm**: every town (router) tells its neighbors "I can reach City X in N hours" — and each neighbor adds its own travel time, keeps the shortest rumor, and spreads the improved number onward. The best routes "percolate" outward from each destination like ripples. **RIP** is this with specific rules: towns announce their whole rumor sheet every 30 seconds (and immediately when something changes); "16 hours" means "impossible." The flaw: if a road to City X *vanishes*, towns that still believe they can reach X via a neighbor keep passing slightly-larger numbers back and forth — each cycle adding one hop — until the rumor finally hits 16 ("gone"). That is **count-to-infinity**: the network "forgets" slowly and noisily. Split horizon is the rule "don't repeat a rumor back to the town you heard it from" — because repeating it is *exactly* how the ghost rumor survives.

## 6. Real-World Analogy
**A group of town criers with rumor maps**: Each crier keeps a list "how far to every city" and, every half-hour, reads their whole list to the neighboring towns (RIP's 30-s update). A crier who hears "City X is 3 towns away via the north road" writes "X: 4 via north" if it's shorter than what they had. The trick works beautifully while the roads exist. But when the north road *closes*, crier A still tells B "X is 4 away" (their old number); B, whose only knowledge of X is via A, now says "X is 5 away" and tells C... and A gets it back as "6" — each round trip adds a hop. The number creeps toward 16 ("infinity") as the towns argue about a city that's simply gone — **count-to-infinity**. The rules that fix it: don't tell a neighbor about a place *you* learned from that neighbor (split horizon), and when a road fails, tell everyone "X is impossible" *loudly and at once* (poison reverse + triggered update). Even then, the towns converge in minutes — which is why big cities (networks) switched to broadcasting the *full road map* instead of rumors (link-state/OSPF).

## 7. Formal Definition
Distance-vector routing is the distributed Bellman-Ford algorithm: router `i` maintains `D_i(d)` = best distance to `d` via next hop `h_i(d)`, initialized from directly-connected links; periodically sends its vector `{d: D_i(d)}` to neighbors; on receiving neighbor `j`'s vector, updates `D_i(d) = min(D_i(d), cost(i,j) + D_j(d))`. Convergence when no update improves any entry. **RIP** (RFC 2453, RIPng RFC 2080 for IPv6): metric = hop count (≤15; 16 = ∞), full-table updates over UDP/520 every 30 s (with jitter), triggered updates on metric change, route timeout 180 s, garbage collection 120 s, split-horizon and poison-reverse to mitigate count-to-infinity, hold-down (RFC 1058) to suppress premature route flip-back. Count-to-infinity: the sequence of gradually increasing distances by which a failed route is finally learned as unreachable. RIP is suitable for networks ≤15 hops; scale/bandwidth needs favor link-state.

## 8. Example
Convergence and count-to-infinity in 3 routers:
```
Initial (all links up):
 A: B=1, C=2 (via B)       B: A=1, C=1        C: A=2 (via B), B=1

After A-B link fails:
 A loses its direct path to B and C.
 A hears from B (split horizon OFF here): "B: C=1" → A sets C=2 via B, and (badly) B=2 via B?
 With split horizon: B does NOT advertise C (or B) routes learned FROM A back to A
   → A can't re-learn them via B → A marks B and C unreachable (16).
 Without split horizon (the classic demo):
   A: B=2 via B, C=3 via B   (counts up)
   B: C=1 unchanged; hears A's "C=3" → no change
   A: after timeout, A says "B=16" → B: A=16 → B: C now only via... → eventual ∞
   Distances creep: 2, 3, 4... 16 — count-to-infinity, taking N×30s rounds.
```
With split horizon + triggered updates, A marks B/C dead in the *first* exchange; without them, the network takes minutes. This one experiment *is* the DV failure story — interviewers love walking it.

## 9. Internal Working
1. **Table init**: connected routes (metric 1 or 0), then 30-s timer starts.
2. **Periodic update**: RIP sends its full table (dest, metric, next hop) to neighbors (UDP 520, multicast 224.0.0.9; broadcasts if not multicast-capable). Version 2 adds subnet masks (CIDR) + authentication.
3. **Receive & relax**: for each entry, `new = metric + 1`; if `new < current` → adopt (next hop = sender); if `new == current` from a *different* neighbor → keep best/equal (ECMP possible); if `new > current` → ignore (or, for the *same* next hop with higher metric, update — the count-to-infinity path).
4. **Failure detection**: a neighbor route times out after 180 s (6 missed 30-s updates) → marked invalid (metric 16) → propagated as "unreachable" (triggered update) → garbage-collected after 120 s more. Triggered updates (RFC 1058) send *immediately* on metric change to shorten propagation.
5. **Split horizon / poison reverse**: with split horizon, outgoing updates omit routes learned from the receiving neighbor; with poison reverse, they include them as metric 16. Both prevent the "teach me my own route" echo that fuels count-to-infinity. Split horizon (omit) is the safer default.
6. **Hold-down**: after learning a route became worse, the router *holds* the new (worse) value for a period rather than immediately accepting an even-worse alternative — giving the bad news time to reach everyone and preventing flapping/loops. (RIP implementations vary; classic Cisco RIP used it.)
7. **Convergence cost**: each count-to-infinity iteration costs one update round; with 30-s timers a small loop can take minutes to settle. This latency is RIP's defining operational limitation.

## 10. Time Complexity
- **Per-update processing**: O(destinations × neighbors) — a table scan + relax per received vector; fine for small tables (RIP networks are ≤15 hops, usually <1000 routes).
- **Bandwidth**: O(table size) every 30 s per link — proportional to network size; this *scales poorly* (one reason RIP caps at small networks). Triggered updates reduce the *event* traffic but not the periodic baseline.
- **Convergence**: O(diameter × update_interval) for good news (best-case fast via triggered updates); O(count-to-infinity iterations × interval) for bad news — up to 16 rounds × 30 s ≈ minutes. This *time complexity* is RIP's reason for retirement on large networks.
- **Count-to-infinity bound**: capped at 16 (infinity) — the protocol's built-in guarantee that "it can't count forever," at the cost of limiting the network to 15 hops.

## 11. Advantages
- **Simple**: the algorithm is a few lines (Bellman-Ford relax); implementation trivial — every OS could run `routed`.
- **Distributed & decentralized**: no central coordinator, no global topology database; each router needs only neighbor updates.
- **Automatic**: routers discover topology by exchanging vectors — no manual tables (vs static).
- **Low memory/CPU**: tiny tables, tiny messages — runs on 1980s hardware (and today's smallest devices).
- **Self-healing for good news**: new/reachable destinations propagate quickly via triggered updates.
- **Pedagogically essential**: the clearest demonstration of a *distributed* routing algorithm — and the foundation for understanding BGP (path-vector) and EIGRP (DV+DUAL).

## 12. Disadvantages
- **Count-to-infinity**: slow, noisy failure convergence (minutes); a real outage cost even at small scale.
- **Hop-count metric blindness**: 1 Gbps and 9.6 kbps links both cost 1 — no bandwidth/latency awareness (unlike OSPF's cost, BGP's policy).
- **Scaling limits**: full-table broadcasts every 30 s + 15-hop cap = tiny networks only; the table exchange wastes bandwidth as size grows.
- **Slow convergence by design**: periodic (30 s) updates mean even good news has up to 30-s delay without triggered updates; hold-down adds more.
- **No policy/security**: trusts neighbor vectors blindly (any neighbor can inject routes — a route-hijack vector); no authentication by default (RIPv2 adds weak auth).
- **Not loop-free in the transient**: during convergence, transient loops are possible (packets bounce) — link-state's SPF tree guarantees loop-free paths.

## 13. Interview Questions
1. **Q: What is distance-vector routing?** A: A distributed algorithm where each router keeps (destination, distance, next hop), sends its whole table to neighbors, and adopts the cheaper path via Bellman-Ford relaxation: `dist = min(dist, link_cost + neighbor_dist)`.
2. **Q (tricky): How does Bellman-Ford work in a distributed setting?** A: Each router iteratively relaxes against neighbors' vectors; when no update improves any entry, the network has converged. Provably correct if the topology stabilizes — each router locally computes the globally-shortest paths.
3. **Q: What is RIP?** A: Routing Information Protocol (RFC 2453) — DV over UDP/520, hop-count metric (15 max, 16 = ∞), 30-s periodic full-table updates + triggered updates, route timeout 180 s, split horizon/poison reverse.
4. **Q (FAANG): What is count-to-infinity?** A: When a route fails, neighbors that still believe it exists keep advertising increasing distances to each other (each adds a hop), converging only when the count reaches infinity (16 for RIP) — slow, wasteful failure convergence. Fixes: split horizon, poison reverse, triggered updates, hold-down.
5. **Q: What is split horizon?** A: Don't advertise a route back to the neighbor you learned it from — prevents a router from "re-learning" its own route via the router that heard it from it (the echo that fuels count-to-infinity).
6. **Q: What is poison reverse?** A: The opposite trick: *do* advertise the route back, but as metric = infinity (16) — loudly telling the neighbor "this route through you is dead." Stronger than split horizon in some cases (at the cost of more messages).
7. **Q (tricky): What is hold-down and when is it used?** A: After a route's metric increases (bad news), the router ignores *even worse* alternatives for a hold-down period — giving the bad news time to propagate network-wide before a flapping path is re-learned. Classic RIP/Cisco behavior; prevents premature route flip-back loops.
8. **Q: Why is the RIP metric 15-hop capped?** A: Hop count is the metric and 16 = infinity — the cap bounds count-to-infinity (at most 15 increments) and defines the protocol's scale. Networks needing >15 hops must use OSPF/IS-IS (metric-based, no hop cap).
9. **Q (production): Why did my network take minutes to converge after a link failure?** A: Classic RIP: the failing route count-to-infinity through neighbors (each round trip +1 hop, each round a timer period), until split-horizon/triggered updates finally clear it — with 30-s timers, minutes is normal. Fix: OSPF (fast) or triggered-update tuning (best-effort).
10. **Q: DV vs link-state — which is better and why?** A: DV: simple, low resources, slow convergence + count-to-infinity. Link-state: every router floods its local state and runs Dijkstra → fast, loop-free convergence, but more memory/CPU + flood complexity. Networks >small choose link-state (OSPF); the Internet's scale chooses BGP (path-vector) — see sections 03/04.
11. **Q (tricky): Is BGP a distance-vector protocol?** A: No — it's a *path-vector* protocol (section 04): like DV it propagates reachability neighbor-to-neighbor, but it carries the *entire AS path* (not just distance) so loops are detectable and *policy* can be applied. Path-vector is DV's answer to scale + policy.
12. **Q: What is EIGRP and how does it differ from RIP?** A: Cisco's DV protocol with **DUAL** (Diffusing Update Algorithm): routers keep *feasible successors* (loop-free backups) and converge instantly on failure without count-to-infinity; metric combines bandwidth+delay (not hops). DV's modern refinement.
13. **Q (FAANG): What happens when two DV routers disagree about a link that failed?** A: Count-to-infinity: each re-learns the other's (now higher) distance and propagates it, incrementing each round, until infinity — or, with split-horizon/poison-reverse, the failed route is marked 16 in one exchange. The *speed* of agreement is the difference between naive DV and "fixed" DV.
14. **Q: Why does RIP send full tables every 30 seconds?** A: Simplicity + self-healing: no sequence numbers, no acknowledgments — periodic full-table resends recover from any lost update. The cost is bandwidth and slow propagation, which is why large networks abandoned it.
15. **Q (production): You see RIP table entries "16" for a healthy route. Diagnose.** A: Metric 16 = infinity = the route was declared unreachable: a neighbor timed out (180 s), hold-down suppressed a re-learn, or split-horizon hid the real path. Check the neighbor's updates (`debug ip rip` / `tcpdump udp 520`), the link state, and whether the router that *should* advertise the route is up.
16. **Q: What are RIPv1 vs RIPv2 differences?** A: v2 (RFC 2453): classless (subnet masks — CIDR), multicast 224.0.0.9 (vs broadcast), triggered updates, and optional authentication. v1 is classful and broadcast — the modern deployments are v2 (or RIPng for IPv6).
17. **Q (tricky): Can DV routing form a loop that never converges?** A: With the standard fixes (split horizon, poison reverse, infinity cap) the protocol *guarantees* eventual convergence — the infinity bound is exactly that guarantee. Without the fixes, count-to-infinity still terminates at 16 (bounded), just slowly. True non-termination was the OSPF-era worry that motivated topology-based (loop-free) algorithms.

## 14. Follow-Up Questions
1. **Q: What exactly causes "count-to-infinity" — is it a bug or a property?** A: A property of DV's local knowledge: a router can't distinguish "my old route vanished" from "my neighbor's route got worse," so it propagates the *increase* hoping another path exists. It's correct-in-the-limit (reaches infinity) but slow — the reason the fixes exist and why link-state was built.
2. **Q: How do triggered updates + split horizon shorten convergence?** A: Triggered = send immediately on a metric *change* (not waiting 30 s) → bad news propagates in ~diameter RTTs, not timer periods. Split horizon = don't echo a route back to its source → the echo loop that *re-inflates* count-to-infinity never starts. Together they make failure convergence fast at small scale.
3. **Q (tricky): Why does a hold-down period sometimes *increase* convergence time?** A: It deliberately waits before accepting a worse alternative — during flaps or cascading failures, that wait *prevents* loops (the goal), but in a clean failover it delays recovery. It's a "slow-but-loop-free" trade you must size (Cisco default 180 s) to the network's diameter.
4. **Q: How would you fix RIP's convergence for a modern small network?** A: RIPng/RIPv2 with triggered updates + split horizon + tuned timers, or — the real answer — switch to OSPF (fast convergence, cost metric) or a static floating-route design for tiny networks. RIP's simplicity is only a win where convergence speed doesn't matter.
5. **Q (FAANG): "Why did the Internet choose BGP (a DV-ish design) over OSPF-style link-state for inter-domain routing?"** A: Scale + policy: link-state floods the *entire* topology to everyone (impossible across thousands of independent ASes), and OSPF optimizes a *metric* (meaningless across administrative domains). Path-vector propagates reachability + policy attributes (section 04) — it keeps DV's "neighbor-to-neighbor" scale and adds loop detection + policy. The *choice of algorithm class* is driven by the environment, not the algorithm's elegance.

## 15. Coding Example
```python
# Distributed Bellman-Ford — the DV core in one function
INF = 16  # RIP's infinity

def bellman_ford(routers, edges):
    # routers: set of ids; edges: dict (i,j) -> cost (symmetric assumed)
    dist = {r: {d: INF for d in routers} for r in routers}
    for r in routers:
        dist[r][r] = 0
    # repeated relaxation = each "round" is one DV update exchange
    for _ in range(len(routers) - 1):
        for (i, j), c in edges.items():
            for d in routers:
                if dist[i][d] > dist[j][d] + c:
                    dist[i][d] = dist[j][d] + c
                if dist[j][d] > dist[i][d] + c:
                    dist[j][d] = dist[i][d] + c
    return dist

routers = {"A", "B", "C", "D"}
edges = {("A", "B"): 1, ("B", "C"): 1, ("C", "D"): 1, ("A", "D"): 4}
d = bellman_ford(routers, edges)
print(d["A"])  # {'A':0,'B':1,'C':2,'D':3}  (A-C via B: 2, not the direct 4)

# Count-to-infinity simulation (naive, no split horizon):
# A-B fails; A and B re-learn each other's inflated distances until INF.
# The takeaway: "distances increment to 16" is the DV failure fingerprint.
```
```bash
# See real RIP on the wire (UDP 520)
$ sudo tcpdump -i eth0 udp port 520 -nn -vv | head
#   224.0.0.9.520 > 224.0.0.9.520: RIP, response, length 64
#     routes: 10.0.0.0/24 metric 1, 192.168.1.0/24 metric 2, ...
$ ip route show                       # the resulting table (via routed/quagga)
$ which routed zebra bird quagga      # common RIP daemons if any installed
```

## 16. Industry Usage
- **Legacy + small-footprint**: RIP still runs in small/embedded/CPE gear, older VoIP/SBC boxes, and labs where its simplicity is a feature. It's rare in new enterprise design — but *any* network with a 20-year-old router may still speak it.
- **Pedagogy & certification**: RIP is the standard teaching protocol (CCNA/Net+ curricula) — every engineer learns convergence, count-to-infinity, and split-horizon through it. It's the shared vocabulary of routing.
- **The DV design lineage in production**: **EIGRP** (Cisco's DV+DUAL, common in legacy enterprise) and **BGP** (path-vector, the entire Internet) are DV's descendants — so DV thinking is *operationally live* wherever EIGRP/BGP run.
- **Comparative diagnostics**: "why did this RIP (or EIGRP/BGP) route flap/count?" is the same *distributed-algorithm* debugging skill; understanding DV's failure modes transfers directly to BGP route-flap and EIGRP SIA issues.
- **Research/education**: distributed algorithms (convergence, oscillation, loop-freedom) are studied through DV — and interview questions ("count-to-infinity", "split horizon") are drawn straight from this protocol family.

## 17. References
- RFC 1058 — RIP v1: https://www.rfc-editor.org/rfc/rfc1058
- RFC 2453 — RIP v2 (classless): https://www.rfc-editor.org/rfc/rfc2453
- RFC 2080 — RIPng (IPv6): https://www.rfc-editor.org/rfc/rfc2080
- Kurose & Ross, *Computer Networking*, Ch. 5 §5.2 (routing algorithms; Bellman-Ford/DV).
- Tanenbaum, *Computer Networks*, Ch. 5 (distance-vector).
- RFC 4271 — BGP-4 (path-vector, DV's successor): https://www.rfc-editor.org/rfc/rfc4271

## 18. Cheat Sheet
- DV = distributed Bellman-Ford: `dist(d) = min(dist(d), cost + neighbor_dist(d))`, iterated to convergence.
- Each router sends its *full table* to neighbors; keeps best (dest, dist, next hop).
- RIP: UDP/520, hop metric (≤15, 16=∞), 30-s full-table updates + triggered updates, timeout 180 s, GC 120 s.
- Count-to-infinity: failed routes increment toward 16 through stale neighbors — the core DV flaw.
- Fixes: split horizon (don't echo back), poison reverse (echo as ∞), triggered updates (immediate), hold-down (ignore worse for a period).
- Metric blindness: every link costs 1 — no bandwidth/latency awareness.
- Scale: ≤15 hops; full-table periodic sends kill bandwidth as it grows.
- EIGRP = DV + DUAL (feasible successors, instant convergence); BGP = path-vector (policy + loop detection).
- Converges fast on good news (triggered), slow on bad news (count-to-infinity) — RIP's reason for retirement.
- Debug: `tcpdump udp 520`, `ip route` (via a RIP daemon), debug rip.

## 19. Quiz
1. DV is based on: a) Dijkstra b) Bellman-Ford c) BFS d) policy → **b**
2. RIP metric: a) cost b) hops c) delay d) bandwidth → **b**
3. RIP infinity: a) 15 b) 16 c) 100 d) 255 → **b**
4. Count-to-infinity is fixed by: a) larger table b) split horizon/poison reverse c) faster CPU d) RIPng → **b**
5. Split horizon means: a) don't echo a route to its source b) split tables c) no loops d) faster → **a**
6. Poison reverse advertises the route as: a) normal b) infinity c) hidden d) lowest → **b**
7. RIP updates every: a) 10 s b) 30 s c) 60 s d) 5 s → **b**
8. Hold-down: a) ignores worse routes for a period b) speeds updates c) adds cost d) splits horizon → **a**
9. EIGRP is: a) link-state b) DV + DUAL c) path-vector d) static → **b**
10. BGP is: a) link-state b) path-vector c) pure DV d) hybrid → **b**

## 20. Flashcards
- **Q: DV algorithm?** → **A:** distributed Bellman-Ford; relax on neighbor vectors.
- **Q: RIP metric/infinity?** → **A:** hops; 15 max, 16 = unreachable.
- **Q: Count-to-infinity?** → **A:** failed routes increment to ∞ via stale neighbors.
- **Q: Split horizon?** → **A:** don't advertise a route back to its source.
- **Q: Poison reverse?** → **A:** advertise it back as ∞.
- **Q: Triggered updates?** → **A:** send immediately on change (not 30 s).
- **Q: Hold-down?** → **A:** ignore worse routes briefly (loop prevention).
- **Q: EIGRP / BGP?** → **A:** DV+DUAL / path-vector (DV's successors).

## 21. Revision
DV = distributed Bellman-Ford: routers exchange full tables, keep (dest, dist, next hop), relax until convergence. RIP = DV over UDP/520, hop metric (15/∞), 30-s periodic + triggered updates, timeout 180 s; fixes for count-to-infinity: split horizon (no echo-back), poison reverse (echo as ∞), hold-down (ignore worse briefly). Count-to-infinity = failed routes creep to 16 through stale neighbors — minutes of convergence. Metrics are hop-blind (no bandwidth). Scale ≤15 hops. EIGRP (DV+DUAL) and BGP (path-vector) are DV's production descendants. Good news converges fast; bad news slow.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is distance-vector routing?" | 2 How It Works / 7 Formal Definition |
| "Explain count-to-infinity." | 13 Q&A / 8 Example |
| "Split horizon / poison reverse / hold-down?" | 13 Q&A / 5 Intuition |
| "Why does RIP cap at 15 hops?" | 13 Q&A / 9 Internal Working |
| "DV vs link-state?" | 13 Q&A / 10 Time Complexity |
| "Why is BGP path-vector, not DV?" | 13 Q&A / 11 Advantages |
| "Why did my network converge slowly?" | 13 Q&A / 12 Disadvantages |
| "Is EIGRP a DV protocol?" | 13 Q&A / 14 Follow-Up |
| "How does DV handle failure?" | 13 Q&A / 15 Coding |
