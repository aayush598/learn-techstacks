# Routing

> **TL;DR**: Routing is how routers build and use the tables that send packets toward any destination — **static** (hand-configured), **distance-vector** (distributed Bellman-Ford; RIP, count-to-infinity), **link-state** (flood + Dijkstra; OSPF, fast convergence), and **path-vector** (BGP: AS paths + policy, the Internet's inter-domain glue).

## Chapter Roadmap
- **Routing fundamentals & static**: forwarding vs routing, the FIB, convergence, administrative distance, metric, and when static wins.
- **Distance-vector (RIP)**: Bellman-Ford distributed, count-to-infinity, split horizon, poison reverse, hop-count metric.
- **Link-state (OSPF)**: LSA flooding, Dijkstra, areas/hierarchies, fast convergence, tie-breaking metrics.
- **Path-vector (BGP)**: AS paths, policy routing, attributes (local-pref, AS path, MED), iBGP/eBGP, and the Internet's routing reality.

## Section Files
- `section-01-routing-fundamentals-and-static-routing.md` — forwarding, tables, metrics, AD, convergence, static vs dynamic.
- `section-02-distance-vector-routing-and-rip.md` — Bellman-Ford, RIP, count-to-infinity + fixes, comparison.
- `section-03-link-state-routing-and-ospf.md` — Dijkstra, flooding, OSPF areas, fast convergence.
- `section-04-path-vector-routing-and-bgp.md` — BGP attributes, path selection, iBGP/eBGP, peering, policy.

## Interview Q&A Preview
- **"Distance-vector vs link-state?"** → Distance-vector: neighbors exchange entire tables, Bellman-Ford, simple but slow convergence + count-to-infinity. Link-state: every router floods its *local* state, everyone runs Dijkstra, fast + loop-free, but heavier (OSPF). Path-vector (BGP) is the Internet's choice because it's policy-driven, not metric-driven.
- **"What is count-to-infinity?"** → A DV failure mode: when a route fails, nodes keep incrementing the hop count through alternate paths instead of learning it's gone, converging only after reaching infinity (16 for RIP). Fixes: split horizon, poison reverse, triggered updates, hold-down.
- **"Why does BGP use path-vector instead of link-state?"** → The Internet is inter-domain: routes are *policy*, not least-cost paths. BGP propagates full AS paths so each AS can apply policy (who will I transit? what do I prefer?) — Dijkstra across thousands of independently-governed ASes is meaningless; path-vector lets each domain express its own decisions.
