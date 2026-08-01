# Routing Fundamentals and Static Routing

> **TL;DR**: Routing is *the* network-layer core — deciding "which way does a packet go?" via **forwarding tables (FIB)** computed by **routing protocols**; static routing is the hand-configured baseline (simple, deterministic, no protocol) that still powers default routes, stub networks, and cold-start bootstrap before dynamic protocols converge.

## 1. Why Does This Exist?
A network of N devices is useless unless packets find their destination — and the Internet's scale (billions of hosts, ~1M prefixes, thousands of interconnected ASes) makes "remember every path" impossible. Routing exists to answer two questions with *scalability*: (1) **forwarding** — for each incoming packet, which outgoing link? (an O(1)-ish lookup in a table) and (2) **route computation** — how do we *build* that table? (algorithms: static, distance-vector, link-state, path-vector). Routing exists because **topologies change** (links fail, nodes come/go, traffic shifts) and the network must adapt — automatically, consistently, and loop-free. Static routing is the *baseline* answer: a human encodes the paths. It works when topology is fixed and small (default routes, stub networks, edge links) and is the *only* answer until a dynamic protocol converges — which is why even fully-dynamic networks start with a static bootstrap. Understanding the fundamental split — *forwarding* (data plane, fast) vs *routing* (control plane, smart) — is the first thing every routing interview question assumes.

## 2. How Does It Work?
- **Forwarding table (FIB)**: destination prefix → next hop (IP or interface) + metric + AD. A packet's lookup = longest-prefix match → next hop → ARP → frame → out.
- **Routing table (RIB) vs FIB**: the RIB is the router's full learned state (from static + protocols); the FIB is the *active* optimized forwarding copy.
- **Route sources + Administrative Distance (AD)**: when multiple protocols know the same prefix, AD breaks the tie (lower wins): connected=0, static=1, eBGP=20, OSPF=110, RIP=120, iBGP=200.
- **Metric**: within a protocol, the cost of a route (RIP=hops, OSPF=cost/link-speed, BGP=policy) — the *tie-breaker inside* one protocol.
- **Static route**: `ip route add <prefix> via <next-hop> [metric]` — a hand-written, unlearned route. Options: default route (0.0.0.0/0 → gateway), floating static (backup with higher metric, activates on primary loss), recursive static (next hop reachable via another route).
- **Dynamic routing**: routers exchange reachability and compute routes (see sections 02–04). Static routes have AD 1 (almost always preferred) and *never* converge themselves.
- **Convergence**: the process by which all routers agree on the topology after a change — time to agreement (static: instant but human; RIP: slow, count-to-infinity; OSPF: fast; BGP: policy-paced).
- **The Internet's hierarchy**: intra-domain (OSPF/IS-IS inside an AS) + inter-domain (BGP between ASes) — a *two-level* routing architecture, because a single protocol can't scale to both.

## 3. When Is It Used?
- **Default route**: every host has one (`0.0.0.0/0 → gateway`) — the simplest, most common static route on the planet.
- **Stub networks / edge**: a small network with one way out needs only a default route — no protocol overhead.
- **Point-to-point links / VPNs / tunnels**: static routes over tunnels (IPsec, GRE) where the path is fixed.
- **Cold-start/bootstrap**: before OSPF/BGP converge, routers need *some* route — static is the seed.
- **Failover planning**: floating statics (metric 100/200) for backup paths when you want *deterministic* primary/backup behavior.
- **Policy/simplicity**: where you don't want dynamic churn (lab networks, air-gapped, or security-sensitive fixed paths).
- **Hosts and firewalls**: hosts mostly use static (default route + connected); firewalls route with statics for DMZ/VPN legs.

## 4. Why Wasn't Another Approach Chosen?
- **Why a *table* at all (FIB) instead of recomputing each packet?** Path computation is expensive (algorithms, topology state); per-packet recompute would be O(graph) per packet — impossible at line rate. Compute the table *once* (control plane), then forward with O(1) lookups (data plane). The table is the *cached decision*.
- **Why separate forwarding from routing?** Two very different timescales: forwarding must run at packet rate (nanoseconds, hardware); route computation can be slow (milliseconds+, software). Separating them lets each optimize independently — the fundamental architecture of every router.
- **Why static at all when dynamic exists?** Dynamic protocols have cost (traffic, state, convergence risk, complexity) and *assume* a fully-arranged topology. Static is deterministic (no surprises), zero-overhead, and secure (no route injection). Its limit is scale/change — but for fixed, small, or bootstrapped networks it's strictly better.
- **Why AD + metric (two-tier preference)?** AD compares *across* sources ("trust OSPF over RIP"); metric compares *within* a source ("this OSPF path is cheaper"). Without the distinction, conflicting sources would be ambiguous — AD is the "protocol trust" axis, metric the "path cost" axis.
- **Why longest-prefix match over exact/class-based?** Exact-match needs the *same* mask on both ends; class-based is rigid. Longest-prefix is the most specific — it makes aggregation + specific routes coexist naturally (0.0.0.0/0 default + /24 subnet + /32 host all in one table). It's the CIDR-native lookup (see part-04 ch1).

## 5. Intuition
Routing is **planning a road trip with a map that updates itself** — except the "driver" (packet) doesn't plan at all: it just reads the current *signpost* at each intersection (next hop) written by the mapmaker (routing). The **forwarding table** is the signpost at this intersection: "destinations starting 10.1 → highway A; everything else → highway B." **Routing** is how the signs get written: static = a human wrote them by hand; dynamic = the mapmaker recalculated from neighbors' reports. **AD** is your trust in different mapmakers (a road atlas you trust more than a random tourist's advice); **metric** is "which road is shorter." **Convergence** is the moment the map settles after a bridge collapses — every intersection's signposts agree again. Static routing = hand-painted signposts: perfect for a small town with one road out (default route), hopeless for a continent.

## 6. Real-World Analogy
**A highway sign system run by "routing departments"**: Every intersection has a signboard (FIB) saying "City X → Exit 4; Everything else → straight." A **static** sign is painted by the local department and never changes — right for a town with one exit (a stub network: all traffic leaves via the default). **Dynamic** signs are updated by the traffic control center as it learns road closures from every intersection's reports (distance-vector: "I can reach City X in 3 hops via the west road") or from a shared blueprint of every road (link-state: everyone has the full map and computes the shortest path). The **Administrative Distance** is the department's trust ranking: a painted static sign outranks a dynamically-computed one, which outranks a rumor from a distant city (RIP). The **default route** is the famous "Everything else → the big highway" sign every town needs. And **convergence** is how quickly all the signboards agree after a bridge collapses — the difference between minutes (static: human re-paints) and seconds (OSPF) and longer (BGP policy debates).

## 7. Formal Definition
Routing is the process of computing paths to destinations (control plane); forwarding is the per-packet lookup-and-send (data plane). A router's Routing Information Base (RIB) holds routes from static configuration and dynamic protocols; the Forwarding Information Base (FIB) is the optimized copy used for lookups. Each route = (destination prefix, next hop, outgoing interface, metric, administrative distance). **Administrative Distance** (Cisco; RFC 4271 appendix for BGP AD values) ranks route sources — connected 0, static 1, eBGP 20, OSPF 110, IS-IS 115, RIP 120, iBGP 200. **Metric** ranks paths within a source. Static routing: manually configured routes (`ip route add prefix via next-hop`); default route = 0.0.0.0/0; floating static = a backup with a higher metric activated when the primary disappears. Convergence = the period after a topology change until all routers agree and forwarding is loop-free.

## 8. Example
A typical host/router static routing setup:
```
Host (Linux):
$ ip route show
default via 192.168.1.1 dev eth0          <- the default static route (stub)
192.168.1.0/24 dev eth0 proto kernel      <- connected (auto), AD 0

Router:
$ ip route show
10.0.0.0/24 via 192.168.2.1 dev eth1      <- static, AD 1
10.1.0.0/16 via 192.168.2.2 dev eth1      <- static (aggregated)
172.16.0.0/12 via 10.0.0.1 dev eth0       <- static (backup) metric 200
default via 192.168.2.1 dev eth1          <- default static

Longest-prefix decision for 10.1.5.5:
  matches 10.1.0.0/16 (16 bits) -> send via 192.168.2.2   (most specific wins)
```
The router's control plane combines these hand-written entries with whatever dynamic protocol also runs; AD 1 means static *always* beats OSPF (110) for the same prefix. This is the classic "static wins unless it vanishes" behavior that floating statics exploit (a static route that *points at* a dynamic next hop dies when the next hop is unreachable, promoting the backup).

## 9. Internal Working
1. **RIB build**: the router collects routes: connected (auto, from interface config), static (config file/CLI), and dynamic (from routing protocols' updates). Each route is stored with its source's AD and its protocol metric.
2. **RIB → FIB**: for each prefix, the router picks the best route: lowest AD, then lowest metric, then tie-breakers (longer prefix first). The winning route is installed in the FIB; the FIB is what the data plane reads.
3. **Forwarding**: for each packet, the FIB lookup (longest-prefix match, trie/TCAM) → next hop + outgoing interface → L2 resolution (ARP/NDP) → frame out. The data plane never consults routing protocols.
4. **Static route semantics**: a static route to a next hop is *installed* if the next hop is reachable (a recursive lookup); if the next hop dies, the static route is removed from the FIB → a *floating* static (metric 200) then wins for that prefix → automatic backup. Static routes are never updated by protocol updates; they require manual change (and careful design).
5. **Default route propagation**: hosts/stub routers advertise/use 0.0.0.0/0 so *everything else* goes out the one known path — the cheapest, most robust static of all (no per-destination knowledge needed).
6. **Failure handling**: static — a dead link breaks the route until a human fixes it (or a floating static promotes). Dynamic — protocols detect, flood, and recompute (fast/automatic). This is the static-vs-dynamic reliability trade.
7. **Verification**: `ip route`, `show ip route`, `ping/traceroute` per destination, `ip route get <dest>` (the exact FIB decision) — the standard debugging loop.

## 10. Time Complexity
- **Forwarding lookup**: O(prefix-length) worst (trie walk), effectively O(1) in TCAM hardware — *constant*, regardless of table size (that's the point of the table).
- **Static route management**: O(1) per route to add/remove; no computation or messaging — zero convergence *traffic*, but convergence is "as fast as a human."
- **FIB size**: bounded by configured prefixes; the data plane's TCAM is finite (a real constraint on route counts).
- **Failure recovery**: static = human time (minutes–days) or floating-static promotion (ms after detection); dynamic = protocol convergence (see sections 02–04).
- **Scalability**: static scales to *small, fixed* topologies; beyond a few hundred routes or any churn, it becomes unmanageable — the crossover point where dynamic wins.

## 11. Advantages
- **Deterministic**: no surprises — the path is exactly what you configured; perfect for security-sensitive or regulated paths.
- **Zero overhead**: no protocol traffic, no state, no CPU for route computation — best for small/stub/fixed networks.
- **No convergence risk**: nothing to "converge"; static routes are immune to route flaps, count-to-infinity, and protocol bugs.
- **Bootstrap enabler**: the seed routes that let dynamic protocols start; the default route every host depends on.
- **Simple to debug**: one `ip route` shows the whole intent; a human can reason about every path.
- **Floating statics**: deterministic primary/backup behavior without protocol tuning.

## 12. Disadvantages
- **Manual, error-prone**: every link change needs human edits; mistakes cause blackholes/loops that aren't self-detected.
- **No automatic adaptation**: link down = route down (until fixed); no load-balancing, no re-route around failures.
- **Doesn't scale**: hundreds of routes + churn = unmaintainable; no topology awareness, no aggregation logic.
- **No redundancy reasoning**: a "via X" route fails even if another path exists — the router can't discover alternatives.
- **Silent staleness**: a static route can point at a long-dead next hop (the router only drops it if the next hop is *directly* unreachable); nothing revalidates.
- **Monitoring burden**: humans must watch for drift — hence "static + alerting" is common but operationally heavy.

## 13. Interview Questions
1. **Q: What is the difference between routing and forwarding?** A: Routing = the *control plane* — computing the path (via static config or protocols). Forwarding = the *data plane* — per-packet lookup in the FIB and send out the right link. One is "planning," the other "executing" (fast, per-packet).
2. **Q (tricky): What is the FIB vs the RIB?** A: The RIB (routing table) holds all learned/configured routes with their sources and metrics; the FIB (forwarding table) is the *optimized active copy* — the winning route per prefix, structured for fast lookup. Data plane reads FIB; control plane writes it.
3. **Q: What is Administrative Distance and how does it work?** A: The trust ranking used when *different* protocols offer the same prefix: lower wins — connected 0, static 1, eBGP 20, OSPF 110, RIP 120, iBGP 200. Metric (inside a protocol) then decides among equal-AD routes.
4. **Q (FAANG): What is the difference between AD and metric?** A: AD compares *across* route sources ("trust static over OSPF over RIP"); metric compares *within* one protocol ("this OSPF path costs 20, that one 30"). AD = which protocol; metric = which path.
5. **Q: What is a static route and when do you use it?** A: A hand-configured route (`ip route add 10.0.0.0/24 via 192.168.2.1`). Use for: default routes, stub/edge networks, tunnels/VPNs, bootstrap before protocols converge, and deterministic primary/backup (floating statics).
6. **Q: What is the default route?** A: 0.0.0.0/0 — the "everything else" static route (least-specific, matches last). Every host has one via its gateway; it's the Internet's most important static route.
7. **Q (tricky): What is a floating static route?** A: A backup static with a *higher* metric than the primary (e.g., 200 vs 1). It sits unused in the RIB; when the primary (or its next hop) dies, the floating route activates automatically — deterministic failover without a dynamic protocol.
8. **Q: Why do we still use static routing when dynamic exists?** A: Determinism (no surprises/security), zero overhead (no protocol traffic/state), no convergence risk, and simplicity on small/fixed/stub networks. Dynamic is for scale + change; static is the baseline everything starts from.
9. **Q (production): A static route's next hop disappears. What happens?** A: The route is removed from the FIB when the next hop becomes unreachable (recursive lookup fails) — so traffic fails over to any better route (e.g., a floating static). But if the next hop is *indirectly* reachable via another path, the route may *stay* installed and silently misdirect — a classic static-route gotcha.
10. **Q: How does a router choose among multiple routes to the same prefix?** A: 1) Lowest AD (protocol trust), 2) lowest metric (path cost), 3) longer prefix (specificity — handled at lookup anyway), 4) implementation tie-breakers (e.g., vendor's default). The winner goes into the FIB.
11. **Q (FAANG): Why is the FIB lookup "O(1)"?** A: The data plane uses a trie or (in hardware) TCAM keyed on prefixes — the lookup cost is bounded by the *prefix length* (≤32), not the table size. That's the whole design: slow computation once, instant lookup forever.
12. **Q: What is convergence and why does it matter?** A: The period after a topology change until all routers agree on the new paths (loop-free, consistent). Static: instant but manual; RIP: slow (count-to-infinity); OSPF: seconds (fast); BGP: policy-paced. Slow convergence = blackholes/loops during the window.
13. **Q (tricky): What happens if two routers have conflicting static routes?** A: Depending on the topology, packets loop (A→B→A) or blackhole — statics don't detect or resolve conflicts. This is *the* argument for dynamic protocols: self-consistent, loop-free computation. Statics assume the human got it right.
14. **Q: What is a "connected" route?** A: A route auto-installed for a directly-connected subnet (interface's own network) — AD 0 (the most trusted, since it's local reality). It's the base of every routing table; static/dynamic build on top.
15. **Q (production): Your ISP link dies; hosts still send via the static default route. What do you do?** A: The static 0.0.0.0/0 via the ISP gateway is still *installed* if the gateway is reachable (it's on-link, so the recursive check passes) — traffic blackholes out the dead link. Fix: a *tracking* mechanism (IP SLA/`track`) that removes the static on failure, or a floating static to the backup link with tracking — or switch to dynamic (BGP/OSPF) at the edge.
16. **Q: What is the hierarchy of the Internet's routing?** A: Two levels: **intra-domain** (OSPF/IS-IS inside one AS/ISP, detailed topology) and **inter-domain** (BGP between ASes, policy-based). One protocol can't scale to both — the split is fundamental (see sections 03/04).
17. **Q (tricky): Can a static route be used for load balancing?** A: Yes, multiple static routes to the same prefix (equal metrics) enable *per-destination* load sharing in many implementations (Cisco does per-destination by default) — but it's static (no dynamic redistribution) and per-flow behavior depends on the implementation. Dynamic protocols (ECMP via OSPF/BGP) are the usual choice for real balancing.

## 14. Follow-Up Questions
1. **Q: How do static routes interact with dynamic protocols?** A: They coexist in the RIB; AD decides who wins (static=1 usually beats OSPF=110, eBGP=20). Static can be *redistributed* into a protocol (announce the stub's default), and a static can point at a dynamic next hop — the common "static for the policy, dynamic for the reachability" pattern.
2. **Q: What is "recursive static routing"?** A: A static route whose next hop is *itself* reached via another route (e.g., `via 192.168.2.1` where 192.168.2.1 is reachable through a /30). The router resolves the next hop each time; if the underlying route dies, the static is withdrawn — the mechanism floating statics rely on.
3. **Q (tricky): Why is the default route's prefix /0?** A: It must match *every* destination — the shortest possible prefix (0 bits). Longest-prefix match then means: the default only wins when nothing more specific matches — exactly the "catch-all" semantics the Internet's edge needs.
4. **Q: What is route redistribution and why is it risky?** A: Taking routes from one protocol and announcing them in another (e.g., static→OSPF, OSPF→BGP). Risk: loops, suboptimal paths, and route-injection security issues — redistribution *must* be filtered. It's the "glue" between routing domains and a classic source of outages.
5. **Q (FAANG): "Design the routing for a small office with a VPN to HQ and a backup ISP link."** A: Static baseline: default via ISP (primary), floating static via VPN (metric 200) as backup, VPN tunnel routes static, no dynamic protocol needed. If the office grows or adds sites → OSPF intra-office + BGP at the edge. The interview scores the *static-first thinking*, AD/metric usage, and knowing when dynamic is warranted.

## 15. Coding Example
```python
# Longest-prefix match — the FIB lookup, implemented
def add_route(table, prefix, plen, next_hop, ad, metric):
    table.append(dict(prefix=prefix, plen=plen, next_hop=next_hop,
                      ad=ad, metric=metric))

def lookup(table, ip):
    ip_i = int.from_bytes([int(x) for x in ip.split(".")], "big")
    best = None
    for r in table:
        mask = (0xFFFFFFFF << (32 - r["plen"])) & 0xFFFFFFFF
        if (ip_i & mask) == (r["prefix"] & mask):       # matches?
            key = (r["ad"], r["metric"], -r["plen"])    # AD, then metric, then specificity
            if best is None or key < best[0]:
                best = (key, r)
    return best[1] if best else None

t = []
def net(s): return int.from_bytes([int(x) for x in s.split(".")], "big")
add_route(t, net("0.0.0.0"), 0, "gw", 1, 0)           # default (static)
add_route(t, net("10.0.0.0"), 8, "r8", 110, 10)       # OSPF
add_route(t, net("10.1.0.0"), 16, "r16", 110, 5)      # OSPF, more specific
add_route(t, net("10.1.5.0"), 24, "r24", 1, 1)        # static, most specific

print(lookup(t, "10.1.5.5")["next_hop"])   # r24 (static, /24 — wins by AD+prefix)
print(lookup(t, "10.2.9.9")["next_hop"])   # r8  (OSPF /8 — beats default)
print(lookup(t, "8.8.8.8")["next_hop"])    # gw  (default catch-all)
```
```bash
# The real routing toolbox
$ ip route show                                   # the RIB view
$ ip route get 10.1.5.5                           # the exact FIB decision (debug!)
$ ip route add 10.0.0.0/24 via 192.168.2.1        # add a static
$ ip route add 0.0.0.0/0 via 192.168.2.1 metric 200   # floating static (backup)
$ ip route del 10.0.0.0/24                        # remove
$ ip route flush cache                            # clear the route cache
```

## 16. Industry Usage
- **Edge/host routing everywhere**: every host's default route is static; home routers, small offices, and stub networks are pure static. It's the most-deployed "routing protocol" in history (it's just configuration).
- **Enterprise/DC underlays**: static prefixes for uplinks/loopbacks/tunnels, floating statics for backup links, and static routes *between* OSPF/BGP domains — "static for the policy, dynamic for the fabric" is standard design.
- **Cloud (AWS/GCP/Azure)**: VPC route tables are *static* by default (explicit prefix → target); "route tables + internet gateway + NAT gateway" is all static plumbing; Transit Gateway/peering adds more static entries; BGP appears only for Direct Connect/VPN (see part-04 ch4).
- **Service providers**: static routes seed loopbacks and external links; default routes dominate customer edge; the "default + static" pattern is what makes CPE boxes work without protocols.
- **Security/regulated**: air-gapped or compliance-sensitive networks use pure static routing (no protocol = no injection vector, deterministic paths) — a deliberate, documented choice.
- **Networking education/FAANG**: the forwarding-vs-routing split, AD/metric, and longest-prefix logic are the *foundation* every routing question builds on — mastering this section makes the protocol sections click.

## 17. References
- RFC 1812 — Router Requirements (forwarding/routing basics): https://www.rfc-editor.org/rfc/rfc1812
- RFC 4271 — BGP-4 (AD values appendix; inter-domain): https://www.rfc-editor.org/rfc/rfc4271
- Kurose & Ross, *Computer Networking*, Ch. 5 (routing algorithms + forwarding).
- Tanenbaum, *Computer Networks*, Ch. 5 (network layer).
- Cisco: "IP Routing: What is Administrative Distance" (official AD table).
- Linux: `man ip-route`, `ip-route(8)`.

## 18. Cheat Sheet
- Routing (control plane) builds the RIB; forwarding (data plane) reads the FIB.
- Route = prefix + next hop + metric + AD; longest-prefix match for lookup.
- AD (lower = more trusted): connected 0, static 1, eBGP 20, OSPF 110, RIP 120, iBGP 200.
- Metric: cost *within* a protocol (hops/cost/policy). AD first, then metric.
- Static: manual, AD 1, deterministic, zero overhead; default route = 0.0.0.0/0.
- Floating static: higher-metric backup, activates when primary dies.
- Stub/edge: default route only. Bootstrap: static seeds dynamic.
- Convergence: all routers agree after a change — static=manual, RIP=slow, OSPF=fast, BGP=policy.
- Hierarchy: intra-domain (OSPF/IS-IS) + inter-domain (BGP).
- `ip route get <dst>` = the exact FIB decision (the debugging tool).
- Static limits: no auto-failover, no self-repair, doesn't scale → dynamic when needed.

## 19. Quiz
1. Routing computes; forwarding: a) encrypts b) looks up + sends per packet c) stores d) fragments → **b**
2. FIB is: a) full RIB b) optimized active copy c) config d) cache only → **b**
3. AD of static: a) 0 b) 1 c) 110 d) 120 → **b**
4. AD of OSPF: a) 1 b) 20 c) 110 d) 200 → **c**
5. Default route prefix: a) /8 b) /24 c) 0.0.0.0/0 d) /32 → **c**
6. Metric is used: a) across protocols b) within a protocol c) for lookup d) for TTL → **b**
7. Floating static: a) removes primary b) backup with higher metric c) dynamic d) redistributed → **b**
8. Longest-prefix match: a) default wins b) most specific wins c) AD wins d) metric wins → **b**
9. Stub network needs: a) OSPF b) BGP c) a default route d) IS-IS → **c**
10. Two-level Internet routing: a) static+dynamic b) intra (OSPF/IS-IS) + inter (BGP) c) DV+LS d) none → **b**

## 20. Flashcards
- **Q: Routing vs forwarding?** → **A:** control plane (compute) vs data plane (lookup+send).
- **Q: RIB vs FIB?** → **A:** learned state vs optimized active copy.
- **Q: AD values?** → **A:** connected 0, static 1, eBGP 20, OSPF 110, RIP 120, iBGP 200.
- **Q: AD vs metric?** → **A:** across protocols (trust) vs within (cost).
- **Q: Default route?** → **A:** 0.0.0.0/0 — the catch-all.
- **Q: Floating static?** → **A:** backup with higher metric, activates on primary failure.
- **Q: Longest-prefix?** → **A:** most specific route wins.
- **Q: Convergence?** → **A:** all routers agree after a change; static=manual, OSPF=fast.

## 21. Revision
Routing = control plane (build RIB via static/dynamic); forwarding = data plane (FIB lookup, longest-prefix). Route = prefix + next hop + metric + AD (connected 0, static 1, eBGP 20, OSPF 110, RIP 120, iBGP 200); AD first, then metric. Static routes: deterministic, zero overhead, AD 1; default 0.0.0.0/0; floating statics = deterministic backup. Static wins for stub/fixed/bootstrap; dynamic for scale + change. Convergence: static=manual, RIP=slow, OSPF=seconds, BGP=policy. Internet = intra-domain (OSPF/IS-IS) + inter-domain (BGP). Debug: `ip route get`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Routing vs forwarding?" | 2 How It Works / 7 Formal Definition |
| "RIB vs FIB?" | 13 Q&A / 9 Internal Working |
| "AD and metric?" | 13 Q&A / 10 Time Complexity |
| "When to use static routing?" | 13 Q&A / 3 When Is It Used |
| "Default route / floating static?" | 13 Q&A / 5 Intuition |
| "Longest-prefix match?" | 13 Q&A / 6 Real-World Analogy |
| "Why is forwarding O(1)?" | 13 Q&A / 11 Advantages |
| "Static vs dynamic trade-off?" | 13 Q&A / 12 Disadvantages |
| "Design routing for a small office." | 13 Q&A / 15 Coding |
