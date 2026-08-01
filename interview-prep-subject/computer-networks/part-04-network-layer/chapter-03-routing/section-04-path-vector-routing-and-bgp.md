# Path-Vector Routing and BGP

> **TL;DR**: **BGP** (RFC 4271) is the Internet's routing protocol — a **path-vector** algorithm where each AS advertises full *AS paths* to neighbors, making routes loop-free, scalable, and **policy-driven**. Routers pick best paths via attributes (local-pref, AS path length, MED, origin) — economics and policy, not shortest-path math, decide inter-domain routing. eBGP between ASes, iBGP inside one.

## 1. Why Does This Exist?
The Internet is ~100,000 independent **ASes** (autonomous systems — ISPs, clouds, universities) that must exchange reachability — but *none* of them would accept OSPF-style least-cost routing (they'd route through competitors), and none would accept link-state flooding (topologies are commercial secrets). The Internet's routing problem is not "shortest path" but **"which path do I *want* to take?"** — governed by contracts (who I peer with, what I'll transit, what I prefer), not by a metric. **BGP** exists as the **path-vector** protocol that solves exactly this: reachability is announced as an *AS path* ("I can reach 8.0.0.0/8 via ASes 64500, 64501, 64502"), which makes loops *detectable* (see your own AS in the path → discard), is fully **scalable** (only reachability is shared, not topology), and lets each AS apply **policy** at every hop (local-pref, MED, path prepending — "route traffic my way" via economic incentives). Every organization that connects to the Internet runs BGP; it *is* the Internet's control plane.

## 2. How Does It Work?
- **Path-vector**: a BGP UPDATE announces a prefix + its **attributes**, notably `AS_PATH` (the sequence of ASes to reach it). When an AS passes the route on, it *prepends its own AS*. Loop detection: if your AS is already in the AS_PATH, discard.
- **eBGP vs iBGP**: **eBGP** = between ASes (direct peers, typically); **iBGP** = inside one AS (all iBGP speakers must be *fully meshed* or use route reflectors, because iBGP routes aren't re-advertised to other iBGP peers).
- **Path selection** (best path, in order): highest **local-pref** (local policy) → shortest **AS_PATH** → lowest **origin** → lowest **MED** (multi-exit discriminator — peer's preference) → eBGP over iBGP → lowest IGP metric to the next hop → lowest router-ID (tie-break).
- **Attributes**: `local-pref` (own policy, higher better), `AS_PATH` (loop + length), `MED` (entered/exited at a specific link, lower better, sent to a peer), `origin` (IGP/EGP/incomplete), `next-hop`, `communities` (tagging for policy).
- **Peering**: **over TCP/179** (reliable — BGP doesn't invent its own reliability), with open/keepalive (60 s)/notification messages. **Multihop** for indirect peers; **MD5/TCP-AO** authentication.
- **Prefixes**: BGP announces **networks** (prefixes): an AS announces its own allocations and, optionally, transit customers' (with policies about who it re-advertises to).
- **iBGP scale**: route reflectors (clusters) and confederations avoid full-mesh — the operational topology of large providers.
- **Convergence**: BGP is *deliberately* slow (policy + path-length comparisons, MRAI timer ~30 s between updates to a peer) — correctness and policy beat speed.

## 3. When Is It Used?
- **Internet edge**: every ISP, cloud (AWS/GCP/Azure), CDN, and large enterprise connects to the Internet *via BGP* — announcing their prefixes (a /24 or larger needs an RIR allocation) and learning the global table.
- **Multi-homing**: a site with 2+ ISPs uses BGP to advertise itself to both and choose which path to use (best-path selection + policy) — failover and load distribution.
- **Peering / IXPs**: networks exchange traffic at Internet Exchanges (IXPs) via eBGP sessions — settlement-free peering vs paid transit are *BGP policy* decisions.
- **Transit**: an ISP sells reachability by re-advertising customer prefixes (with policy) — the entire Internet economy runs on BGP's path-vector + policy.
- **Cloud hybrid**: Direct Connect/VPN BGP sessions (AWS/GCP/Azure announce your VPC prefixes to your on-prem router) — the standard hybrid-cloud control plane.
- **DC fabrics (BGP EVPN)**: BGP as the overlay control plane for EVPN/VXLAN in data centers — the modern DC networking stack.
- **Anycast**: CDNs announce the *same* prefix from many locations via BGP → clients route to the nearest.

## 4. Why Wasn't Another Approach Chosen?
- **Why path-vector, not link-state (OSPF)?** Link-state floods the *whole topology* to everyone and computes least-cost paths — unthinkable across independent ASes (commercial secrecy, scale, and no shared metric). Path-vector shares only *reachability* (prefix + path), scales (no topology database), and enables *policy* (each AS decides what it advertises and prefers). DV had no loop detection; path-vector's AS_PATH adds it — DV + loop detection + policy = BGP.
- **Why not DV (RIP-style)?** RIP shares distances hop-by-hop with count-to-infinity and no policy. At Internet scale, count-to-infinity is unacceptable and policy is essential. Path-vector's "distance = AS_PATH length" is a *policy input*, not a hard metric.
- **Why TCP/179?** BGP rides TCP so it gets reliability, ordered delivery, and flow control *for free* — the control plane doesn't reinvent transport. TCP's 4KB-ish message and keepalive semantics fit UPDATE/keepalive perfectly.
- **Why "best path by policy," not shortest?** ASes have *economic* goals: prefer peers over transit (local-pref), prefer shorter paths (fewer middlemen = cheaper), influence routing toward/away from links (MED, prepending). A least-cost algorithm would route everyone through the cheapest path — commercially impossible. BGP's path selection *is* a policy engine, not an optimization.
- **Why eBGP/iBGP split?** eBGP carries external policy + loop protection via AS_PATH; iBGP propagates routes *within* an AS (all speakers must have consistent views for loop-free forwarding). The split isolates policy at the border while keeping internal routing consistent.

## 5. Intuition
BGP is **airlines trading "we can get you there" itineraries**: Each airline (AS) publishes "we can fly you to City X" with the *route* ("via Partner 1, then us") attached. If a route ever lists your own airline, you know it's a loop — throw it out (AS_PATH loop detection). Each airline then *chooses* which itineraries to accept by its own business rules (local-pref): "always prefer our alliance partner's route over a rival's, even if the rival's is shorter" — that's policy, not distance. When your plane must enter a foreign hub, the *hub* decides how much it charges you (MED) and which gate you use. Airlines never share their secret route networks (link-state would) — they only exchange *who can reach what*, and they never claim to reach a city they can't (BGP only advertises what it will actually deliver). The whole system is deliberately slow to change (itineraries are re-negotiated, not recomputed) — correctness and commerce beat speed.

## 6. Real-World Analogy
**Global shipping alliances**: Shipping lines (ASes) publish route cards: "From Hamburg we can deliver to Tokyo via the Suez line, our Asia partner, then us" (the AS path). A line that sees its *own* name already on a card knows that card loops back on itself — reject it (loop detection). Ports (routers) then pick which cards to honor by *contract*: "We always accept cards from our alliance, never cards that cross a rival's hub" (local-pref — economics over distance). When a container must traverse a foreign port, that port charges and influences the routing (MED, prepending). Lines never reveal their full route maps to competitors (no link-state flooding) and only claim destinations they actually serve (BGP's "only advertise what you can deliver" honesty — a broken claim = a route *hijack*). If the Suez line fails, cards are re-issued and re-negotiated slowly (BGP convergence) — shipping always prioritized *commerce* over speed, which is exactly why the Internet's inter-domain routing runs on BGP rather than shortest-path.

## 7. Formal Definition
BGP-4 (RFC 4271) is an inter-domain routing protocol using the **path-vector** algorithm. Peers establish a TCP/179 session (port 179), exchange OPEN (capabilities), UPDATE (NLRI: prefix + path attributes), NOTIFICATION (errors), KEEPALIVE (60-s interval, hold 180 s). Attributes: `ORIGIN` (0 IGP, 1 EGP, 2 incomplete), `AS_PATH` (sequence of AS numbers; loop detection + length), `NEXT_HOP`, `LOCAL_PREF` (iBGP-announced local policy, higher preferred), `MED` (multi-exit discriminator, lower preferred, sent to one peer), `COMMUNITIES` (policy tags), `AGGREGATOR`. Best-path selection: highest local-pref → shortest AS_PATH → lowest origin → lowest MED → eBGP over iBGP → lowest IGP cost to next-hop → lowest router-ID. eBGP = between ASes; iBGP = within (full mesh or route reflectors). Policy is applied via route maps/filters on import/export; the **MRAI** (minimum route advertisement interval, ~30 s) throttles updates.

## 8. Example
Best-path selection (the canonical walk):
```
We (AS 64500) receive two routes to 203.0.113.0/24:

Route A: AS_PATH 64500 64501 64502,  local-pref 200,  MED 100, next-hop 64501
Route B: AS_PATH 64500 64503 64504 64505,  local-pref 150, MED 50, next-hop 64503

Step 1: local-pref — A (200) > B (150)   → A wins (local policy trumps everything)
Step 2 (if local-prefs equal): shorter AS_PATH wins
Step 3: origin (IGP < EGP < incomplete)
Step 4: lower MED
Step 5: eBGP > iBGP
Step 6: lower IGP cost to next-hop
Step 7: lower router-ID (tie-break)
```
Note the *ordering*: local-pref (policy) first, then AS path length (economics), then MED (peer preference), then technical tie-breaks. This ordering *is* the protocol's "what matters most" statement — and it's the single most-asked BGP interview question.

## 9. Internal Working
1. **Session**: TCP/179 connection; OPEN with capabilities (multiprotocol, route refresh, graceful restart); KEEPALIVE every 60 s (hold timer 180 s — miss 3 → session reset); NOTIFICATION for errors. Authentication: MD5/TCP-AO (RFC 2385/5925).
2. **UPDATEs**: advertise (NLRI + attributes), withdraw (explicit prefix lists), or both. Received routes are stored in the **Adj-RIB-In** (per-peer input), policy-filtered, passed to **Loc-RIB** (the AS's chosen routes), and re-advertised per-policy from **Adj-RIB-Out**.
3. **Policy (route maps)**: on *import* and *export*, ASes filter/manipulate: deny/malicious prefixes (filtering!), set local-pref/communities, prepend AS_PATH (make a route less attractive), tag with communities for downstream decisions. This is where "the Internet's politics" lives.
4. **Best-path computation**: per-prefix, per the selection steps (section 8). Only the winner is installed in the FIB and re-advertised.
5. **iBGP correctness**: iBGP speakers must *all* receive the external route (full mesh or route reflectors) so every router has a consistent view; iBGP-learned routes are *not* re-advertised to other iBGP peers (that's the reflector's job).
6. **Route reflectors**: a reflector accepts iBGP routes and re-advertises to clients — reducing N² full-mesh to a hub-and-spoke while preserving the iBGP semantics (with loop-avoidance via originator-ID/cluster-list).
7. **Convergence & damping**: MRAI (~30 s) throttles updates per peer (bounded rate, `updates in 15 s`); route *dampening* suppresses flapping prefixes (penalty → suppress) to protect the network; but dampening is often *disabled* today (it hurt fast failover).
8. **Failure/failover**: a lost session (missed keepalives) → all routes from that peer withdrawn → re-computation → new best paths (can take seconds-to-minutes — BGP's known slow convergence, mitigated by BFD + RIB re-optimization).

## 10. Time Complexity
- **State**: each router holds the *global* route table (~1M prefixes × attributes) — memory in the GBs on edge routers. This is *the* scale problem BGP is built for: reachability only (no topology), aggregated prefixes.
- **Convergence**: deliberately slow — O(MRAI × path-length) between updates; a global routing change can take minutes. BGP trades speed for policy correctness and stability (route flaps are the alternative).
- **Path selection**: O(routes) per update — a comparison per prefix; trivial CPU but bounded by table size.
- **Flap damping**: per-prefix penalty accumulation — O(1) per flap.
- **Table growth**: aggregation (prefix summarization at ISPs) is the counterforce keeping the table ~1M instead of millions of host routes — the same aggregation logic as CIDR (part-04 ch1).

## 11. Advantages
- **The Internet's control plane**: one protocol, universally deployed — every AS, every cloud, every CDN. Its ubiquity *is* its strength.
- **Policy-driven**: local-pref/AS_PATH/MED/communities let every AS express economics and contracts — no other protocol can do inter-domain policy.
- **Scalable**: only reachability is shared (no topology); AS_PATH provides loop detection without a global database; aggregation keeps the table manageable.
- **Loop-free by construction**: an AS discards any route containing itself — simple, distributed loop prevention.
- **Robust transport**: TCP-based — reliable, ordered, no retransmission design of its own.
- **Flexible**: communities, route reflectors, confederations, multiprotocol (VPNv4/6, EVPN, labeled-unicast) — BGP extends to DC overlays and MPLS VPNs.

## 12. Disadvantages
- **Slow convergence**: MRAI + policy = minutes on failures (vs OSPF's sub-second) — a known architectural cost.
- **Policy = complexity + accidents**: route-map errors cause blackholes, loops, or *hijacks*; misconfigurations are the #1 BGP outage cause.
- **Security**: no intrinsic authentication of UPDATEs (only peer auth) — **prefix hijacking** (announce someone's prefix), path spoofing, and route leaks are real (mitigated by RPKI/ROA + BGPsec, still being deployed).
- **Full-mesh iBGP pain**: every iBGP speaker needs every route → route reflectors/confederations add operational complexity.
- **No global optimization**: best-path is policy-determined, not "shortest" — paths can be suboptimal by design (and AS_PATH length is a weak proxy for quality).
- **Operational heavy**: filtering, policies, monitoring, and troubleshooting BGP (route maps, communities, dampening, RPKI) is a specialization in itself.

## 13. Interview Questions
1. **Q: What is BGP and why is it needed?** A: The Border Gateway Protocol (RFC 4271) — the Internet's inter-domain routing protocol. It exchanges *reachability* (prefix + AS path) between independent ASes with **policy** control, unlike OSPF's least-cost internal routing.
2. **Q (tricky): Why "path-vector" and not distance-vector?** A: DV shares distances (count-to-infinity, no policy). Path-vector shares the *full AS path*: loops are detectable (see your own AS → drop), and each AS applies *policy* (advertise/prefer/deny) — DV + loop detection + policy = BGP.
3. **Q: What is the AS_PATH and what does it enable?** A: The ordered list of ASes a route traverses. It (a) detects loops (a router rejects a route containing its own AS), (b) provides path *length* (a best-path tie-breaker), and (c) enables policy (prepend to make routes less attractive).
4. **Q (FAANG): Walk through BGP best-path selection.** A: (1) highest local-pref, (2) shortest AS_PATH, (3) lowest origin, (4) lowest MED, (5) eBGP over iBGP, (6) lowest IGP metric to next-hop, (7) lowest router-ID. Local policy first, then economics, then technical tie-breaks.
5. **Q: eBGP vs iBGP?** A: eBGP = between ASes (as-path prepending, policy at borders). iBGP = inside one AS (all speakers must receive every route — full mesh or route reflectors; iBGP routes aren't re-advertised to other iBGP peers).
6. **Q: What are the main BGP attributes?** A: ORIGIN (IGP/EGP/incomplete), AS_PATH (loop + length), NEXT_HOP, LOCAL_PREF (own policy, higher better), MED (peer's preference, lower better), COMMUNITIES (policy tags), AGGREGATOR. Local-pref is the big policy lever; MED is negotiated between specific peers.
7. **Q (production): A route you announced got hijacked. What's the defense?** A: RPKI/ROA (cryptographic origin validation — "is this AS allowed to announce this prefix?"), prefix filtering on import/export, and BGPsec (path signing, still rolling out). Detection: monitoring (BGPstream/RIPE RIS) + RPKI validation at every AS. Origin validation is the pragmatic 2020s defense.
8. **Q: Why does BGP run over TCP?** A: It inherits reliability/ordering/flow control for the control plane — no need to reinvent transport (unlike OSPF which runs over IP directly). TCP/179 + KEEPALIVE (60 s, hold 180 s) + MD5/TCP-AO auth.
9. **Q (tricky): Why is BGP convergence slow?** A: Policy-driven + MRAI (minimum route advertisement interval, ~30 s) throttles update rate; path-length comparisons are policy, not fast math; failover waits on session-timeout + re-computation. "Correct + stable + policy-respecting" beats "fast" for the Internet.
10. **Q: What is a route reflector and why?** A: In iBGP, every speaker needs every route → full-mesh is O(N²). A route reflector re-advertises iBGP routes to its *clients* (hub-and-spoke), preserving iBGP semantics with loop-avoidance (originator-ID/cluster-list). The standard iBGP scaling technique.
11. **Q (FAANG): What is multi-homing with BGP and why does it matter?** A: An AS connects to 2+ ISPs and announces its prefix to all; it *selects* which provider to use via policy (local-pref), and both providers advertise the prefix — the Internet routes *to* you via both, giving failover + load distribution. BGP is what makes redundancy across ISPs actually work.
12. **Q: What are communities?** A: Optional transitive attribute tags (32-bit values, e.g., "no-export", "prepend 3 times") — ISPs use them to signal downstream actions without exposing policy details. The Internet's distributed policy "macros."
13. **Q (production): Your edge router's BGP session keeps dropping. Diagnose?** A: Check the TCP/179 connectivity (MTU! BGP over MTU-blackholed links is classic), KEEPALIVE/hold timer mismatch, MD5/TCP-AO auth failure, or a flapping route-map. `show ip bgp summary` (stale/up/down) + tcpdump port 179 is the drill.
14. **Q: What is route aggregation in BGP?** A: Announcing a *summary* prefix instead of many specifics (e.g., 10.0.0.0/16 for 256 × /24s) — fewer global routes, smaller tables, faster convergence. The Internet's table is manageable *because* ISPs aggregate. Cost: specifics are hidden (traffic may take a suboptimal but workable path).
15. **Q (tricky): What is a route leak?** A: A route learned from one peer is incorrectly re-advertised to another (violating policy) — often a misconfiguration that attracts or diverts traffic (e.g., an accidental "default route to a customer"). Leaks are a top cause of Internet outages; defense = strict import/export policies + "no-default-to-customer" rules.
16. **Q: How does BGP interoperate with OSPF?** A: The classic two-level design: OSPF (or IS-IS) is the *IGP* inside the AS (fast, automatic, cost-based); BGP is the *EGP* at the edges (policy-based). The ASBR redistributes between them with filters — "IGP for the fabric, BGP for the world."
17. **Q (FAANG): Why would a CDN announce the same prefix from multiple locations (anycast)?** A: BGP best-path selection makes every network choose the *nearest* announcement → clients route to the closest PoP. That's how DNS root servers, Cloudflare, and Google's edge work — BGP as a global load-balancer.

## 14. Follow-Up Questions
1. **Q: What is the difference between peering and transit?** A: Peering = two networks exchange each other's traffic at no cost (usually at an IXP); transit = one network *buys* reachability to the whole Internet from another. BGP policy implements both: peering = announce only your + your customers' prefixes to the peer; transit = announce everything.
2. **Q: What is BGP hijacking and the current defense stack?** A: Announcing someone else's prefix (or a more specific one) to attract their traffic. Defenses: RPKI (ROAs cryptographically bind prefix → AS), BGPsec (path signing, emerging), ROV (route origin validation) at every router, and monitoring (RIPE RIS, Cloudflare Radar, BGPmon). It's the Internet's biggest *security* problem — and RPKI adoption is the industry's answer.
3. **Q (tricky): What is AS_PATH prepending and why use it?** A: Deliberately repeating your own AS in the path (e.g., "64500 64500 64500") to make a route *longer* and thus less preferred — used to influence which of your links inbound traffic uses (traffic engineering without changing your topology). It's the classic "policy via path length" trick.
4. **Q: What is the "Internet table" and how big is it?** A: The global BGP routing table — all announced prefixes (~1M as of 2024, growing). Every full-table BGP router must store it (memory in the GBs); ISPs summarize to slow growth. Size + growth = why edge routers are big and why filtering matters.
5. **Q (FAANG): "You join a new ISP. Walk me through the BGP bring-up."** A: (1) Get an RIR allocation (own prefixes, ideally with RPKI ROAs); (2) configure eBGP sessions to the ISP(s) with MD5/TCP-AO + MRAI/keepalive timers; (3) announce *your* prefixes (never defaults/leaks); (4) filter: reject bogons/shortest-paths-as-first-hop, apply max-prefix limits; (5) run RPKI/ROV; (6) monitor with BGP tools. The interview tests *safe bring-up discipline* — filtering, honesty (only announce yours), and redundancy.

## 15. Coding Example
```python
# Best-path selection — the core BGP decision, implemented
def best_path(routes):
    """routes: list of dicts with local_pref, as_path, origin, med, type(e/i), igp_cost, router_id"""
    def key(r):
        # order matters: (local_pref desc, as_path_len asc, origin asc, med asc, eBGP>iBGP, igp asc, id asc)
        return (-r["local_pref"], len(r["as_path"]), r["origin"],
                r["med"], 0 if r["type"] == "e" else 1, r["igp_cost"], r["router_id"])
    return min(routes, key=key)

routes = [
    dict(local_pref=200, as_path=[64501, 64502], origin=0, med=100, type="e", igp_cost=10, router_id="1.1.1.1"),
    dict(local_pref=150, as_path=[64503, 64504, 64505], origin=0, med=50, type="e", igp_cost=5, router_id="2.2.2.2"),
]
print(best_path(routes))   # Route A (local_pref 200 wins, even with longer MED)
```
```bash
# The BGP toolbox
$ tcpdump -i eth0 tcp port 179 -nn | head            # OPEN/UPDATE/KEEPALIVE traffic
$ vtysh -c 'show bgp summary'                         # sessions, states, prefixes
$ vtysh -c 'show bgp ipv4 unicast 203.0.113.0/24'     # best path + attributes
$ vtysh -c 'show bgp neighbors 1.2.3.4 received-routes'
$ whois -h whois.radb.net -- '-i origin AS64500'      # see announced prefixes (RIS/route views)
# Check the global table / RPKI status:
$ curl -s https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS64500
```

## 16. Industry Usage
- **ISPs & transit (the backbone)**: every ISP's edge runs BGP — peering at IXPs, transit agreements, customer multi-homing, and global table propagation. The Internet's economy is literally BGP policy.
- **Cloud providers (AWS/Azure/GCP)**: Direct Connect/VPN/Interconnect sessions are BGP; clouds announce customer VPC prefixes to on-prem routers; BGP brings up the hybrid-cloud control plane (border-gateway protocols on every DX link).
- **CDNs & anycast (Cloudflare, Akamai, Google, Netflix)**: BGP anycast announces the same IPs globally → clients route to the nearest PoP; plus BGP-driven failover, traffic engineering via prepending, and RPKI defense against hijacks.
- **DC fabrics (BGP EVPN/VXLAN)**: BGP is the modern DC *overlay* control plane (EVPN address families) — the same protocol that runs the Internet now runs fabric overlays at scale.
- **Fintech/trading networks**: BGP route selection + communities drive low-latency path choice; dark-fiber/colo edge routing is BGP-heavy.
- **Security/trust infrastructure**: RPKI/ROV (RPKI-ROV adoption campaigns), BGPmon/RIPE RIS/Cloudflare Radar monitor hijacks; "BGP security" is one of the most active operational security domains.

## 17. References
- RFC 4271 — BGP-4: https://www.rfc-editor.org/rfc/rfc4271
- RFC 4456 — Route Reflection: https://www.rfc-editor.org/rfc/rfc4456
- RFC 2385 / RFC 5925 — TCP MD5 / TCP-AO auth: https://www.rfc-editor.org/rfc/rfc5925
- RFC 8210 — RPKI-RTR (RPKI/ROV): https://www.rfc-editor.org/rfc/rfc8210
- RFC 8205 — BGPsec: https://www.rfc-editor.org/rfc/rfc8205
- Kurose & Ross, *Computer Networking*, Ch. 5 §5.4 (BGP).
- RIPE Routing Information Service (RIS): https://stat.ripe.net / https://www.ripe.net/ris
- Cloudflare BGP/RPKI docs: https://developers.cloudflare.com/bgp/

## 18. Cheat Sheet
- BGP = path-vector, inter-domain, policy-driven; TCP/179; KEEPALIVE 60 s / hold 180 s.
- eBGP (between ASes, AS_PATH prepends) vs iBGP (inside AS, full mesh / route reflectors).
- Attributes: LOCAL_PREF (own, high), AS_PATH (loop + length), ORIGIN (IGP/EGP/incomplete), MED (peer, low), NEXT_HOP, COMMUNITIES.
- Best path: local-pref → AS_PATH len → origin → MED → eBGP>iBGP → IGP cost → router-ID.
- Loop detection: reject routes containing your own AS.
- AD: eBGP 20, iBGP 200. MRAI ~30 s = slow convergence by design.
- Scale: route reflectors, confederations, aggregation (summary prefixes).
- Security: RPKI/ROA + ROV (origin validation), BGPsec (path), prefix filtering; hijacks + leaks are top outages.
- Anycast: same prefix from many PoPs → nearest wins.
- Hybrid cloud: Direct Connect/VPN use BGP; DC overlays use BGP EVPN.
- Tools: `show bgp summary/ipv4`, tcpdump port 179, RIPE RIS.

## 19. Quiz
1. BGP is: a) link-state b) path-vector c) DV d) static → **b**
2. BGP runs over: a) UDP b) TCP/179 c) ICMP d) raw IP → **b**
3. Best-path first criterion: a) AS_PATH b) local-pref c) MED d) origin → **b**
4. Loop detection uses: a) hop count b) AS_PATH c) TTL d) communities → **b**
5. eBGP: a) inside AS b) between ASes c) full mesh only d) UDP → **b**
6. iBGP scale trick: a) areas b) route reflectors c) DR/BDR d) split horizon → **b**
7. LOCAL_PREF is: a) peer's b) local policy, higher preferred c) lower preferred d) external → **b**
8. MED: a) lower preferred b) higher preferred c) loop d) local → **a**
9. MRAI throttles: a) packets b) BGP updates c) SPF d) hellos → **b**
10. Prefix hijack defense: a) RPKI/ROV b) OSPF c) faster MRAI d) MED → **a**

## 20. Flashcards
- **Q: What is BGP?** → **A:** the Internet's path-vector, policy-driven inter-domain routing.
- **Q: Why path-vector?** → **A:** AS_PATH = loop detection + length + policy; no topology sharing.
- **Q: Best path order?** → **A:** local-pref → AS_PATH len → origin → MED → eBGP>iBGP → IGP → ID.
- **Q: eBGP vs iBGP?** → **A:** between ASes (policy/prepend) vs inside (full mesh/reflectors).
- **Q: Attributes?** → **A:** local-pref (own), AS_PATH, origin, MED (peer), communities.
- **Q: Why slow?** → **A:** policy + MRAI ~30 s; correctness/stability > speed.
- **Q: Hijack defense?** → **A:** RPKI/ROA + ROV; BGPsec; prefix filtering.
- **Q: Anycast?** → **A:** same prefix from many sites → nearest wins.

## 21. Revision
BGP (RFC 4271) = the Internet's path-vector protocol over TCP/179: eBGP (between ASes, AS_PATH prepend + policy) vs iBGP (inside AS, full mesh or route reflectors). Attributes: local-pref (own policy, high), AS_PATH (loop + length), origin, MED (peer, low), communities. Best path: local-pref → AS_PATH len → origin → MED → eBGP>iBGP → IGP cost → router-ID. Loop detection: reject own AS in path. MRAI (~30 s) → slow-but-stable convergence. Scale via aggregation/reflectors/confederations. Security: RPKI/ROV + BGPsec + filtering (hijacks/leaks = top outages). Uses: Internet edge, multi-homing, IXP peering, hybrid cloud (DX), DC overlays (EVPN), anycast.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is BGP / why is it needed?" | 2 How It Works / 7 Formal Definition |
| "Why path-vector, not OSPF/DV?" | 13 Q&A / 4 Why Not Another Approach |
| "Walk through best-path selection." | 13 Q&A / 8 Example |
| "eBGP vs iBGP?" | 13 Q&A / 9 Internal Working |
| "What are the attributes?" | 13 Q&A / 5 Intuition |
| "Why is BGP slow to converge?" | 13 Q&A / 10 Time Complexity |
| "What is a hijack / route leak + defense?" | 13 Q&A / 14 Follow-Up |
| "Route reflectors / multi-homing / anycast?" | 13 Q&A / 16 Industry Usage |
| "BGP bring-up at a new ISP?" | 13 Q&A / 15 Coding |
