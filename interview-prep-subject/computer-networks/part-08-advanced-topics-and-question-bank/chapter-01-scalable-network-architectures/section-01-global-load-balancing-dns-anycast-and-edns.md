# Global Load Balancing, DNS Anycast, and EDNS

> **TL;DR**: Production traffic is steered globally by a GSLB hierarchy — DNS-based selection (GeoIP/latency/weighted/health) decides *which* region serves you, anycast IPs route you to the *nearest* of several identical nodes, and EDNS Client Subnet fixes DNS's "resolver location" inaccuracy — all governed by TTLs and health checks.

## 1. Why Does This Exist?
A single server can't serve the planet: latency would be hundreds of ms (speed of light), capacity would collapse under load, and one outage would take everything down. **Global load balancing** exists to answer one question per user — *"which replica of this service should you talk to?"* — optimally. "Optimal" means: nearest (lowest latency), healthiest (not down/overloaded), and capacity-aware. The internet has no built-in "steer this user to that server" primitive, so the industry layers it: **DNS** decides the region/AS (a small, cached, cheap redirect), **anycast** lets the routing layer pick the nearest of many identical nodes without any DNS involvement, and **EDNS Client Subnet** makes DNS's location decisions accurate by telling the resolver (or its upstream) the *client's* IP. Without these, YouTube/Netflix/Cloudflare-scale services are impossible — latency, capacity, and resilience all fail.

## 2. How Does It Work?
**The GSLB (Global Server Load Balancing) hierarchy:**
1. **DNS-based steering (GSLB)**: `user.example.com` → the GSLB DNS answers with the A/AAAA of the "best" region/DC based on: GeoIP (client's country/region), measured latency map (RTT probes between ASes/POPS), weighted/percent steering (canary, traffic shift), health (region/endpoint health checks), and capacity.
2. **Anycast for the DNS layer (and often the service)**: the GSLB nameservers and CDN edge IPs are announced from many locations via BGP; the routing protocol itself sends you to the nearest. "The network does the load balancing."
3. **EDNS Client Subnet (RFC 7871)**: DNSSEC-secure-ish extension where the client's resolver sends a /24 of the client's IP up to the authoritative DNS, so the answer matches *client* location, not the (possibly distant) resolver's.
4. **Edge → origin handoff**: once steered to a region/edge (CDN PoP or GSLB'd DC), the request hits the edge LB (L4/L7, Part 08 Section 03) which picks a real backend; origin still answer the edge (origin offload).
The *mechanism* is deliberately dumb and fast: DNS answers are cached at every level (browser, OS, resolver), so the steering decision must be correct at TTL-scale, not per-request.

## 3. When Is It Used?
- **CDNs** (Cloudflare, Akamai, Fastly): DNS GSLB + anycast edge; a `cdn.foo.com` resolves to the nearest PoP.
- **Global web services**: `example.com` steered by GeoIP to US/EU/APAC regions; failover to another region on health check failure.
- **DNS root and TLD servers**: 13 root servers are anycast across ~1500 instances; 1.1.1.1 / 8.8.8.8 anycast globally.
- **DDoS scrubbing**: a victim's IP is anycast-advertised from scrubbing centers (Cloudflare/Akamai) so attack traffic lands in absorb-and-filter infrastructure.
- **Health-aware failover**: traffic shifting during launches (weighted/canary), region outage response.
- **Game/matchmaking**: region steering based on latency measurements to the user.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: single DNS answer (no GSLB).* Every user would get one fixed IP → global latency, no region failover, no capacity distribution. DNS steering is the standard because it's *already in the path* (every host queries DNS) and answers are cacheable at huge scale with zero per-request cost.
- *Alternative: only anycast, no DNS.* Anycast is amazing for *stateless* nodes (resolvers, edge cache servers) but wrong for *stateful* servers — a session can hop to a different node if routing changes mid-flow (TCP connections break, session state lost). DNS GSLB gives *deterministic* steering (region/DC choice is stable) while anycast gives *nearest-node* steering. Real systems use both: anycast for the edge/DNS, DNS GSLB for the region/DC decision.
- *Alternative: HTTP-level redirects / client-side LB.* Works but adds a redirect round trip and can't fix DNS-level placement; DNS GSLB is "one hop, cached, free." Client-side (e.g., eDNS SRV / service discovery) is used *inside* DCs, not globally.
- *Alternative: GeoIP without EDNS.* When a user's resolver is in another region, GeoIP on the *resolver's* IP misroutes the user. EDNS Client Subnet fixes this by carrying the client's subnet — chosen because it works with the existing DNS hierarchy and only costs a few bytes.

## 5. Intuition
Global LB is like **airport gate assignment**. DNS GSLB is the airline picking your *airport* (region) based on where you are, where seats (capacity) are free, and which airport isn't shut down (health). Anycast is the *gate*: once you arrive, any of several identical gates (nearby edge nodes) can serve you, and the airport staff (routers) send you to whichever gate is physically closest. EDNS is the airline asking your *travel agent* (resolver) for your actual street address, not just the travel agent's city — otherwise it sends you to the wrong airport. TTL is the flight schedule: the airline can only re-plan your routing when the schedule refreshes.

## 6. Real-World Analogy
A **global pizza chain's ordering system**. Your app (the client) asks the directory (DNS): "where's the nearest open store?" The directory consults a live board (GSLB): it knows each store's health (health checks), its coverage area (GeoIP), how busy it is (capacity/weight), and which store is closest by phone distance (latency map). It answers "Store 142 — 1 Main St" and the address is cached for a while (TTL). Meanwhile, stores advertise their address on a map app (anycast): if two identical stores share a street number, the navigation app (routing) just sends you to whichever is actually closest — no directory needed. If a store burns down (outage), the directory stops recommending it (health check fails) and the next closest store (DNS failover) takes over. EDNS is the directory asking your local branch (recursive resolver) for your zip code — because a customer calling from a branch office in a different city might get routed to the wrong store otherwise.

## 7. Formal Definition
- **GSLB**: a load-balancing tier that uses DNS responses (plus HTTP redirects in some products) to steer clients to the best of several geographically distributed sites; inputs: GeoIP, RTT/latency topology, weights, health, capacity; outputs: A/AAAA/CNAME records with TTLs.
- **DNS steering mechanics**: authoritative DNS answers per-question (or per-client-subnet with EDNS); short TTLs for changeable steering (60-300 s) vs long TTLs for stability; CNAME chaining (user → GSLB host → edge CDN).
- **Anycast** (RFC 4786): a single IP is announced via BGP from multiple sites; routers forward toward the closest (best BGP path). Unicast-flavored service delivery: "the routing table picks the server."
- **EDNS Client Subnet (ECS)**, RFC 7871: the recursive resolver appends a client-IP prefix (typically /24) to the query; the authoritative server returns a more accurate answer and echoes back the scope.
- **Health checks**: TCP/UDP/HTTP probes (e.g., HTTP 200 on `/healthz` with expected body) driving the steering decision; bad health → remove from answers → failover.
- **Weights / canary**: percentage-based steering for launches (5% → 50% → 100%), managed via DNS weights or CDN rules.

## 8. Example
**A user in Mumbai loads `api.example.com` (GSLB deployed):**
```
1. Resolver asks authoritative GSLB: "A api.example.com?" (with ECS: client subnet 103.21.x.x/24)
2. GSLB: GeoIP → Mumbai user → steer to APAC. Latency map says SIN DC ~30ms, BLR DC ~5ms.
   Health: SIN healthy, BLR healthy. Weights: 90/10 during canary (BLR new build).
   Answer: api.example.com A 43.245.88.10 (BLR edge LB) TTL 120s.
3. Client connects to 43.245.88.10 (edge LB) → routes to healthy backend pool in BLR DC.
4. Anycast in play: the GSLB nameservers themselves are anycast (e.g., ns1-4 at 8 sites),
   so the *query* went to the nearest nameserver; the DNS root servers are anycast too.
5. If BLR goes down → health check fails → GSLB stops returning BLR IP → clients
   (after TTL expiry + retry) get SIN IP → automatic regional failover.
```

## 9. Internal Working
1. **GeoIP**: mapping client IP (from ECS or resolver IP) to region; databases (MaxMind) + RFC 1918/ISP data; limitations (mobile/IPv6/CGNAT, VPNs) — latency-based maps often beat GeoIP alone.
2. **Latency topology**: the operator measures RTT from every PoP/DC to destination ASes (probing) and builds a matrix; GSLB picks the region with the lowest expected RTT for that client AS.
3. **Anycast decision**: routers converge on the nearest (BGP shortest-path/AS-path) instance of the IP; on link failure, routing converges (seconds-minutes) to the next-closest — this is also *why* anycast DDoS scrubbers can absorb attacks: traffic lands at the closest scrubbing PoP.
4. **ECS propagation**: client → resolver (with ECS) → authoritative; the authoritative echoes the scope so the resolver knows the answer's geolocation accuracy; caches keyed by (qname, scope).
5. **Health & traffic management**: continuous probes; on failure, the region is removed from answers (failover), weights shift traffic gradually (canary), and edge origins re-register.
6. **Caching & TTL dynamics**: TTL determines how fast a re-steer propagates. A TTL too short (30s) → resolver thrash; too long (1h+) → slow failover. Best practice: shorter TTLs at the GSLB host, longer at stable records; use DNS CNAME levels so only the leaf TTL is short.
7. **Connection safety**: because DNS answers change, GSLB'd sites keep clients on persistent connections (TCP/HTTP2/QUIC) and use server-side redirect/weighted rebalancing for long-lived sessions — a client re-querying after TTL may get a *different* region IP.

## 10. Time Complexity / Performance
- **DNS latency**: a cached answer ≈ 0-5 ms (resolver), uncached authoritative ≈ 20-100 ms across the globe. One DNS query per new hostname — then cached for the TTL, so the *ongoing* cost is ~zero.
- **Anycast convergence**: RTT to the nearest node is typically 5-60 ms (vs 100-300 ms for a single global site); on failure, BGP convergence is seconds (with fast convergence/tuning) — during which some flows may briefly black-hole (mitigated by anycast + DNS GSLB redundancy).
- **GSLB decision cost**: per-query GeoIP+health lookup is microseconds on the authoritative server; health checks run on the order of seconds (5-10 s intervals).
- **Steering quality**: DNS steering is "region-granular and TTL-lagged" — you can't adapt per-request. Latency impact: wrong region = +100-200 ms; that's why ECS and latency maps matter and why CDNs overlay anycast.
- **Throughput**: authoritative GSLB DNS easily handles millions of qps (anycast + stateless); it's the cheap, cacheable layer of global routing.

## 11. Advantages
- **Massive scale at near-zero cost**: DNS answers are cached everywhere; steering decisions are free once made.
- **Latency wins**: users reach the nearest region/edge (anycast + GSLB) — the biggest single lever for perceived performance.
- **Resilience**: regional failover via health checks; anycast absorbs both traffic spikes and DDoS (scrubbing centers).
- **Operational control**: weights/canary traffic shifts, capacity-aware steering, disaster-recovery steering all via DNS config — no client changes.
- **Compatibility**: DNS is universal; EDNS is a tiny extension; works with every client without SDKs.

## 12. Disadvantages
- **Coarse granularity & staleness**: region-level (not server-level) and TTL-lagged — a region can be overloaded before steering notices.
- **Anycast isn't for stateful services**: sessions can break when routes converge (TCP RST/timeout) or a node's anycast IP moves; needs sticky sessions or stateless design.
- **Caching fights back**: clients/resolvers ignore/override TTLs; broken middleboxes strip EDNS; misconfigured resolvers return stale answers → wrong-region routing.
- **ECS privacy/scale trade-offs**: exposing client subnets raises privacy concerns (pseudonymous but quasi-identifying); every distinct (qname, scope) is a cache entry → resolver cache bloat (mitigated by the /24 scope bound).
- **Measurement pitfalls**: GeoIP inaccuracy (VPNs, mobile CGNAT), latency maps can go stale, and BGP anycast can load-imbalance if nodes are unequally attractive.
- **Operational complexity**: running a GSLB means operating DNS health + topology + weights across regions — a whole distributed-systems surface (but Cloudflare/Route53/GCP LB make it managed).

## 13. Interview Questions
1. **Q: How does global load balancing actually work?** A: A GSLB tier answers DNS with the best region/endpoint per client, using GeoIP (or EDNS client subnet) + a latency map + health checks + weights. Combined with anycast (for edge/DNS nodes), it steers users to the nearest healthy replica; answers are cached for a TTL, so steering is coarse and TTL-lagged by design.

2. **Q: What is the difference between DNS-based steering and anycast?** A: DNS steering is a *decision* at query time (region/DC, capacity-aware, health-aware, weighted) — coarse, cached. Anycast is a *routing* behavior: the same IP is announced from many places and routers send you to the nearest. DNS = "which site," anycast = "which node of that IP," often used together.

3. **Q: What is EDNS Client Subnet and what problem does it solve?** A: ECS (RFC 7871) lets the resolver include a client-IP prefix (/24) in the query so the authoritative DNS can geolocate the *client*, not just the resolver. Without it, a user in Mumbai whose resolver is in Singapore gets Singapore-based answers — a few hundred ms of wrongness. It also lets CDNs give the *user* a better edge PoP.

4. **Q: Why are the DNS root servers anycast?** A: There are 13 root server *identities* but ~1500 actual instances worldwide, all announced with the same anycast IPs (a.root-servers.net → many instances). Anycast makes queries reach the nearest instance (latency + resilience), spreads load, and survives regional outages — the routing table does the balancing.

5. **Q: TRICKY — Why can't you anycast a stateful application?** A: Anycast picks the nearest node *per route*, and routes can converge/reconverge (link flapping, maintenance, policy). A TCP session or in-memory session that lands on node A can suddenly be routed to node B (connection reset, session lost). Anycast works only for stateless services (DNS resolvers, CDN cache servers, DDoS scrubbers, TLS-terminating edges that can re-forward) — stateful apps need DNS GSLB (deterministic region) + sticky sessions, or global state (not typical).

6. **Q: How does anycast absorb a DDoS attack?** A: The victim's IP is anycast-announced from scrubbing/edge centers. Attack traffic is routed to the *nearest* scrubbing PoP, where it's analyzed, rate-limited, and filtered (L4/L7) before only clean traffic is forwarded to the origin (via a tunnel). The attack is distributed across many PoPs and absorbed at the edge, never reaching the origin.

7. **Q: What is the role of TTL in global load balancing?** A: TTL controls how long steering decisions persist in caches. Short TTL = fast failover and re-steering but more queries/thrash; long TTL = stable, cheap routing but slow failover. Practice: short TTLs (60-300 s) on the GSLB leaf records, longer on stable apex records, and CNAME chains so only the volatile leaf is short.

8. **Q: What is a "latency map" in GSLB?** A: A matrix of measured RTT from each DC/PoP to each client AS/region (built by active probing). The GSLB steers a client to the region with the lowest expected RTT for that client. It often outperforms GeoIP alone because networks are asymmetric and peering varies.

9. **Q: PRODUCTION — Your GSLB steers Indian users to Singapore but they complain of high latency. Why?** A: (1) GeoIP database may misclassify the client (VPN/CGNAT/mobile carrier NAT); (2) ECS missing → GSLB saw only the resolver's location; (3) latency map stale/measured wrong (peering changed); (4) the target DC's anycast edge is down so steering fell to SIN (health check removed the right region); (5) TTL still caching an old (worse) answer. Fixes: enable ECS, validate GeoIP overrides, refresh latency probes, check health-check config, shorten TTLs during the incident.

10. **Q: What is canary/weighted traffic steering?** A: Steering by weight — e.g., 5% of queries return region B (new build), 95% region A. Managed via DNS weights or CDN rules. Used to gradually shift load during launches, A/B region tests, and migration — with the ability to pull back instantly by changing weights (subject to TTL lag).

11. **Q: How does a CDN use GSLB + anycast together?** A: The CDN hostname is CNAME'd to the CDN's GSLB. DNS resolution steers the user to the best PoP/region (GSLB + ECS), and *within* that region the PoP's IP is anycast so routers pick the nearest edge cache server of that PoP. GSLB picks the region; anycast picks the node.

12. **Q: What happens when a GSLB-managed region goes down?** A: Health checks (TCP/HTTP probes) detect the failure within seconds; the GSLB stops returning that region's IPs; clients whose TTL expires (or that retry) get the next-best region → failover. Until TTL expiry, some clients still hit the dead region (mitigated by short TTLs, LB-level retry/redirect, and the edge answering 5xx then redirecting).

13. **Q: TRICKY — Why does the authoritative DNS need ECS when GeoIP on the resolver IP usually works?** A: Because resolvers are not near their users: corporate resolvers, open resolvers, and CDN resolvers can be in a different city/region/country than the client. If the answer is keyed to the *resolver's* IP, everyone behind that resolver gets the same (wrong) region. ECS keys the answer to the *client's* subnet — one accurate answer per scope instead of one (possibly wrong) answer for millions of users.

14. **Q: What is "origin offload" / why doesn't the GSLB point everyone straight at origin?** A: Origin servers are region-fixed and precious. Global traffic is fronted by edge/CDN infrastructure (caches, TLS, WAF, DDoS scrub) that absorbs requests and only forwards what it must to origin. The GSLB steers to the edge; the edge reduces origin load (cache hit rate), so origin stays small and cheap.

15. **Q: SCENARIO — A launch steers 50% traffic to a new region and it fails immediately. What's the recovery path?** A: (1) Health checks should auto-failover — verify they're configured with a fast threshold; (2) set weight of the bad region to 0 (or remove its records) — effective within TTL; (3) if TTL is long, force cache clear or shorten TTL in advance; (4) confirm LB-level retry/redirect (edge returns a redirect to the healthy region) as an extra safety net; (5) postmortem: why did health checks miss it?

16. **Q: What is the difference between L4/L7 load balancing and GSLB?** A: L4/L7 load balancers spread *individual connections* across backends *inside* a DC/PoP (per-request/per-flow, sub-millisecond). GSLB is the *global* tier that picks the *region/DC* via DNS (per-hostname, TTL-lagged). Tier order: GSLB (region) → edge L4/L7 (PoP) → origin L4/L7 (DC). Each tier offloads the next.

17. **Q: PRODUCTION — Design global load balancing for a low-latency trading API with 99.99% uptime.** A: (1) GSLB with latency-map steering + ECS, short TTLs (30-60 s) and health-check-driven failover; (2) active-active regions with edge anycast for the API's stateless tier (TLS terminate + forward); (3) sticky/failover for stateful sessions, or make the API stateless (state in cache); (4) capacity-aware weights (never point 100% at one region), per-region rate limits; (5) DDoS anycast scrub layer in front; (6) 5-9s resilience at the LB itself (active-active L4 at each region); (7) continuous probe + steer telemetry to verify decisions.

## 14. Follow-Up Questions
1. **Q: What's the difference between GeoIP steering and latency-based steering?** A: GeoIP maps IP → region from a database (static, may be wrong for mobile/VPN). Latency-based uses live RTT probes from each DC to client ASes (dynamic, reflects real peering/paths). Best practice is combining: GeoIP for coarse placement, latency for final region choice; re-probe periodically.

2. **Q: What are the limits of the ECS /24 scope?** A: A /24 is coarse for IPv4 (256 addresses) and a similar scope for IPv6; the authoritative can only answer with that scope, so it can't give per-/32 answers at scale; cache keys multiply by scope, increasing resolver memory; and the client IP may still be an exit/CGNAT address.

3. **Q: How do anycast and unicast coexist in one network?** A: They're both just IP: anycast uses the same address space, but BGP advertises the prefix from multiple locations; unicast prefixes are announced from one primary location (with backups). Operators manage the distinction via BGP communities/policies and make sure anycast prefixes aren't accidentally routed as single-homed.

4. **Q: What happens to an in-flight TCP connection when anycast converges mid-flow?** A: If the flow was to node A and routing now points to node B, node B has no TCP state → the connection breaks (RST/timeout). This is exactly why stateful apps can't sit behind plain anycast; the edge must either be stateless, keep state replicated, or terminate + re-connect (proxy).

## 15. Coding Example
```python
# Simulate GSLB steering decision (geo + latency + health + weights)
import random

REGIONS = {"blr": {"geo": "APAC", "lat_ms": 5,  "healthy": True,  "weight": 90},
           "sin": {"geo": "APAC", "lat_ms": 30, "healthy": True,  "weight": 10},
           "fra": {"geo": "EU",   "lat_ms": 140,"healthy": True,  "weight": 100},
           "iad": {"geo": "US",   "lat_ms": 250,"healthy": False, "weight": 100}}

def gslb_pick(client_geo="APAC", ecs=True):
    cands = [r for r, c in REGIONS.items()
             if c["healthy"] and (c["geo"] == client_geo or not ecs)]
    if not cands:
        return None, "NO_HEALTHY_REGION"
    best = min(cands, key=lambda r: (REGIONS[r]["lat_ms"], -REGIONS[r]["weight"]))
    return best, f"steer {client_geo} client -> {best} ({REGIONS[best]['lat_ms']}ms)"
print(gslb_pick())          # bly region, health-aware
REGIONS["blr"]["healthy"] = False
print(gslb_pick())          # failover to sin
```
```bash
# Real-world verification of steering & anycast (run on a box)
dig +short api.example.com                          # current answer (what GSLB gave)
dig +tcp +norecurse +subnet=103.21.244.0/24 api.example.com   # simulate ECS query to auth
whois 1.1.1.1 | grep -iE "OrgName|NetRange"         # confirm anycast resolver ownership
# traceroute shows WHICH anycast node you actually hit:
traceroute -n 1.1.1.1 | tail -5                     # ends at the nearest Cloudflare PoP
mtr -n -c 10 1.1.1.1                                # RTT + loss per hop (anycast path health)
# DNS answer stability across a TTL window:
while true; do dig +short api.example.com; sleep 10; done   # watch weights/health steer change
# Health-check endpoint used by GSLB:
curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" https://api.example.com/healthz
```

## 16. Industry Usage
- **CDNs/edge**: Cloudflare (anycast for DNS + edge + DDoS scrubbing, ECS, L4/L7 at every PoP), Akamai (GSLB via DNS, its Intelligent Platform), Fastly, Amazon CloudFront.
- **DNS infra**: Verisign, ICANN root operators (anycast), Google Public DNS (8.8.8.8 anycast + ECS), Cloudflare 1.1.1.1.
- **Cloud GSLB**: AWS Route53 (health checks, latency routing, weighted routing, failover), GCP Cloud DNS + Global Load Balancing (anycast VIPs with Google's backbone), Azure Traffic Manager.
- **Global apps**: Netflix (DNS steering to regional Open Connect caches), Meta/Google (GSLB + anycast for user traffic and DDoS).
- **DDoS mitigation**: Cloudflare/Imperva/Akamai anycast scrub layers.

## 17. References
- RFC 7871 (EDNS Client Subnet) — https://datatracker.ietf.org/doc/html/rfc7871
- RFC 4786 (IP Anycast) — https://datatracker.ietf.org/doc/html/rfc4786
- RFC 3258 / RFC 8108 (distributing authoritative name servers)
- AWS Route53 routing policies docs — https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html
- Cloudflare "How DNS works" / anycast overview — https://www.cloudflare.com/learning/dns/what-is-anycast/
- Kurose & Ross, *Computer Networking*, 8th ed., §2.5 (DNS), and CDN material.

## 18. Cheat Sheet
- GSLB = DNS answers per client: GeoIP/ECS + latency map + health + weights → region/endpoint + TTL.
- Anycast = same IP from many nodes; BGP picks the nearest; for stateless services only.
- ECS (RFC 7871) = resolver sends client /24; fixes resolver-location inaccuracy.
- Steering granularity: DNS = region (coarse, cached), anycast = node (nearest), LB = backend (per-request).
- TTL: short on GSLB leaf (fast failover), long on apex (stability); CNAME chains isolate volatility.
- Health checks drive failover; weights drive canary/shift; latency maps beat GeoIP alone.
- Tier order: GSLB (region) → edge L4/L7 (PoP, anycast) → origin LB (DC).
- DDoS scrub = anycast the victim IP into edge centers; filter, forward clean via tunnel.
- Stateful apps: use DNS GSLB + sticky, not raw anycast.

## 19. Quiz
1. GSLB steers at which level? a) per-request b) per-hostname/DNS c) per-packet d) per-route → **b**
2. EDNS Client Subnet carries: a) the resolver's IP b) a client prefix c) the full route d) the TTL → **b**
3. Anycast chooses the server via: a) DNS b) BGP routing c) GeoIP d) health checks → **b**
4. Anycast is safe for: a) stateful apps b) stateless services c) TCP sessions d) databases → **b**
5. Short GSLB TTL buys: a) stability b) fast failover c) fewer queries d) cheaper DNS → **b**
6. The three inputs to a GSLB decision are: a) geo, latency, health b) port, proto, TTL c) MTU, RTT, TTL d) none → **a**
7. Root server identity count: a) 13 b) 1500 c) 100 d) 3 → **a** (13 identities, ~1500 instances)
8. DDoS scrub absorbs traffic by: a) DNS filtering b) anycasting the IP into scrub centers c) GeoIP d) TTL → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-a, 7-a, 8-b.

## 20. Flashcards
- **Q: What is a GSLB?** → **A:** DNS-level load balancing: steer each client to the best region/endpoint (geo/ECS + latency + health + weights), cached for a TTL.
- **Q: Anycast in one line** → **A:** Same IP announced from many places; BGP routes you to the nearest; stateless services only.
- **Q: What does ECS fix?** → **A:** Resolver-location inaccuracy — answers keyed to the client's subnet, not the resolver's IP.
- **Q: Why not anycast stateful apps?** → **A:** Route convergence mid-flow breaks TCP/session state.
- **Q: Short vs long TTL** → **A:** Short = fast failover/re-steer; long = stability/cheap caching.
- **Q: How does anycast stop DDoS?** → **A:** Scrub centers anycast the IP, absorb + filter at the edge, tunnel clean traffic to origin.
- **Q: What tier does GSLB sit above?** → **A:** Region-level (DNS); then edge L4/L7 (PoP, anycast), then origin LB (DC).

## 21. Revision
Global LB = GSLB (DNS: geo/ECS + latency map + health + weights, TTL-cached) + anycast (BGP picks nearest of many same-IP nodes — stateless only) + EDNS Client Subnet (accurate client location). Decisions are coarse and TTL-lagged by design; failover rides on health checks + short leaf TTLs; canary on weights; DDoS absorbs via anycast scrubbing; and the real hierarchy is GSLB → edge L4/L7 → origin L4/L7. Anchors: *DNS picks the region (cached, coarse), anycast picks the node (nearest, stateless-only), ECS fixes resolver-geo errors; TTL = how fast steering changes; health checks = failover; weights = canary; tiers: GSLB → edge → origin.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How does global load balancing work?" | 13-Q1 |
| "DNS steering vs anycast" | 13-Q2 |
| "What is EDNS Client Subnet?" | 13-Q3 |
| "Why are root servers anycast?" | 13-Q4 |
| "Why not anycast stateful apps?" | 13-Q5 |
| "How does anycast absorb DDoS?" | 13-Q6 |
| "Role of TTL in GSLB" | 13-Q7 |
| "What is a latency map?" | 13-Q8 |
| "GSLB steering users wrong region — debug" | 13-Q9 |
| "Canary/weighted steering" | 13-Q10 |
| "CDN: GSLB + anycast together" | 13-Q11 |
| "Region failover mechanics" | 13-Q12 |
| "L4/L7 LB vs GSLB" | 13-Q16 |
| "Design GSLB for low-latency API" | 13-Q17 |
