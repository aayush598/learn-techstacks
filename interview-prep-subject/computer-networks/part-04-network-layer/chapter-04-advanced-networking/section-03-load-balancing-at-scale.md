# Load Balancing at Scale

> **TL;DR**: **Load balancing** spreads traffic across a pool of servers (or links) so no single machine is overwhelmed and failures don't take the service down. **L4** balances TCP/UDP sessions by IP+port (fast, protocol-agnostic); **L7** reads HTTP (headers/cookies/path) for app-aware routing, TLS termination, and sticky sessions; **GSLB/DNS** balances across data centers globally. The LBs, health checks, algorithms, and session affinity are the machinery behind every "scales to millions of requests" statement.

## 1. Why Does This Exist?
One server has finite CPU, memory, connections, and bandwidth. When a service grows past one machine, or needs to survive failures, you must spread requests across **a pool of servers**. Load balancing exists to solve *three* problems at once: **scale** (distribute load so no server saturates), **availability** (hide failures — if one server dies, the LB stops sending to it and clients never notice), and **maintainability** (roll out new versions / do maintenance without downtime by draining a server from the pool). It's the fundamental building block of every distributed system: web tiers, databases (read replicas), caches, message queues, and microservices all sit behind load balancers. Without LBs you'd have *one* point of failure and a hard ceiling on capacity — with them you get horizontal scaling, graceful degradation, and the ability to add capacity by adding boxes. Every "serves millions of requests" architecture in every interview answer implicitly starts with a load balancer in front of the app pool.

## 2. How Does It Work?
- **The pool + health checks**: the LB keeps a list of servers, runs **health checks** (TCP connect, HTTP GET to `/healthz`, or a deep app check) at intervals, and *only routes to healthy servers*. Failure = removed from rotation; recovery = re-added.
- **L4 (transport) load balancing**: balances at the **TCP/UDP session** level — sees IP:port only, doesn't read the payload. Fast, protocol-agnostic, handles any TCP app. Often **DSR** (direct server return): the LB forwards the packet but the server replies *directly* to the client, avoiding the LB bottleneck on return traffic.
- **L7 (application) load balancing**: terminates TLS, reads the HTTP request (method, path, headers, cookies), and routes with app knowledge: `/api/*` → API pool, `*.static` → CDN, cookie "session=..." → the same server (sticky), auth checks, and response rewriting. Slower, but infinitely smarter. (HAProxy, NGINX, Envoy, ALB.)
- **Algorithms**: **round-robin** (rotate — naive but fair-ish), **weighted round-robin** (capacity-aware), **least-connections** (send to the least-loaded — the default for long-lived connections), **least response time** (fastest responder), **IP-hash** / **consistent-hashing** (same client → same server: stickiness + cache locality, with minimal reshuffling when the pool changes), and **random**.
- **Session affinity (stickiness)**: when the app stores state in the server's memory (sessions), the LB must send the same client to the same server — via **source-IP hash**, **cookie insertion** (LB sets `SET-COOKIE`), or URL rewriting. In stateless designs (JWT/Redis sessions), stickiness becomes unnecessary — the 2020s best practice.
- **Global/server load balancing (GSLB)**: DNS-based — the authoritative DNS answers with the *nearest* (geo, latency, health, load) LB IP; combines with **anycast** (the same IP announced from many locations; BGP routes to the nearest) for global distribution and failover.
- **TCP-level details**: the LB does connection pooling (reuse backend TCP connections), keepalives, retries, and **connection draining** (stop new connections, finish in-flight before shutdown — graceful deployment).

## 3. When Is It Used?
- **Web/app tiers**: an ALB/Envoy in front of every web and API pool — the default architecture for any service with more than one instance.
- **Microservices / service mesh**: sidecar LBs (Envoy/Istio, Linkerd) do per-service load balancing, retries, circuit breaking, and mTLS — load balancing *inside* the mesh, not just at the edge.
- **Database scale-out**: read replicas behind a proxy LB (PgBouncer for Postgres, MySQL Router, Redis Cluster) — reads spread, writes pinned to the primary.
- **Global (GSLB)**: multi-region apps balance *across data centers* via DNS/anycast + health-based failover (route to the region that's up).
- **NAT/tunnel scale**: carrier and DC load balancers spread many-to-one NAT and IPsec tunnels across gateway pools.
- **Every public cloud**: AWS ALB/NLB/ELB, GCP L7/L4 LBs, Azure Load Balancer/Azure Front Door — the managed, auto-scaling version everyone uses.

## 4. Why Wasn't Another Approach Chosen?
- **Why not just DNS round-robin?** DNS can return multiple A records (clients pick randomly) — but it has no server *health* awareness, no removal of failed servers, no connection-level session state, and DNS caching defeats rapid failover (TTLs). The LB adds *active health checks + immediate failover + connection awareness* that DNS alone can't. (GSLB *uses* DNS, but combines it with health/LB logic at the authoritative server.)
- **Why L4 vs L7 vs both?** L4 is fast and protocol-agnostic but blind (can't do path-based routing or TLS). L7 is smart but per-request CPU-heavy. Production uses **both**: a fast L4 LB (NLB, or anycast+DPDK/`tcpdump`-sized) at the edge terminating traffic, and L7 LBs (Envoy/ALB) in the app tier. Layering gives speed at the front, intelligence at the back.
- **Why not just let clients connect to servers directly (peer-to-peer)?** Control: the service owner must enforce capacity, routing, auth, and upgrades — a single LB (or mesh) is the point of *control* for all of that. (For truly massive CDN/anycast scale, the "LB" is distributed into every PoP.)
- **Why consistent hashing over simple modulo?** Modulo-hashing (`server = hash(key) % N`) reshuffles *everything* when N changes → cache thundering herd. Consistent hashing maps keys onto a ring so adding/removing a server moves only ~1/N of keys — the standard for cache-distributed systems (Redis/memcached, CDNs).
- **Why round-robin over random?** RR is deterministic and simple; random avoids the "stampede" pattern and spreads load evenly for short requests. Modern LBs use **least-connections / EWMA response time** because they track *actual load*, not just distribution order — the "smart" default beats the "fair" one under heterogeneous request costs.

## 5. Intuition
A load balancer is a **very good restaurant hostess** at a popular restaurant. Every guest (request) arrives; the hostess decides which table (server) to seat them at. She doesn't seat everyone at the first table until it's overloaded (no LB = collapse) — she *rotates* tables (round-robin), or better, knows which waiter is least busy (least-connections) and seats there. She knows which tables are actually staffed (health checks — a broken table is skipped instantly, guests never see it). Some guests are *regulars* with standing orders (sticky sessions) — she seats them at "their" table (session affinity) so their unfinished meal (session state) stays consistent. When it's time to close a section for cleaning (rolling deployment), she stops seating new guests there and lets the current ones finish (connection draining) before closing. And when the restaurant is a *chain* (global), the reservation desk (GSLB/DNS) tells each caller "go to the location nearest to you that's actually open" (geo + health routing) — so the whole system handles a location closing (region failure) without a single customer noticing.

## 6. Real-World Analogy
**The airport check-in hall**: Passengers (requests) arrive and the dispatcher (the load balancer) assigns them to counters (servers). A naive dispatcher sends every passenger to counter #1 until it has a mile-long queue (no LB — collapse); a good one alternates queues (round-robin), or watches the queues and sends passengers to the shortest (least-connections — the airport actually does this). The dispatcher *closes* counters that are unstaffed (health checks — passengers are never sent to a closed counter). VIPs with open itineraries are always sent to the same counter so the agent remembers them (sticky sessions). When a counter closes for a shift change, the dispatcher stops sending new passengers but lets the queue drain (connection draining — smooth rolling maintenance). And the *airport itself* is chosen by the airline's route system (GSLB/DNS): "the closest airport to you that is actually operating" — if your city's airport closes (region failure), the route system reroutes everyone automatically, and passengers at that airport find the airline sent them elsewhere before they ever stood in line.

## 7. Formal Definition
Load balancing distributes workload across multiple computing resources to maximize throughput, availability, and efficiency. **L4 (transport)**: balances TCP/UDP by (src/dst IP, port) — no payload inspection; examples: AWS NLB, LVS, HAProxy (TCP mode), anycast+DDoS-scale DPDK LBs. **L7 (application)**: terminates TLS, parses HTTP/2 (method, URI, headers, cookies) for routing/stickiness/rewriting; examples: Envoy, NGINX, HAProxy (HTTP), AWS ALB, GCP L7 LB. **Algorithms**: round-robin, weighted RR, least-connections, least-response-time (EWMA), IP-hash, consistent hashing (ring, ~1/N reshuffle). **Health checks**: TCP connect / HTTP status / deep payload; failure → remove, recovery → re-add. **Session affinity**: source-IP hash, LB-set cookie, or client-side (stateless/JWT). **DSR** (direct server return): server replies directly, bypassing the LB's return path. **GSLB**: DNS + geo/health-aware answer selection; **anycast**: same IP advertised from multiple locations → nearest wins via BGP.

## 8. Example
The classic N-tier architecture (recreate this on a whiteboard):
```
             ┌──────────────────────────────────────────┐
  clients ──►│  L4 LB (edge)  ──►  L7 LB (Envoy/ALB)   │
             │      │                   │              │
             │  (TLS term + routing)  (path/cookie)    │
             │              │                          │
             │      ┌───────┴───────┐                  │
             │   /api  pool     web  pool              │
             │   (10×api-srv)   (5×web)                │
             └──────────────────────────────────────────┘
                            │
                       Redis (sessions) / DB replicas (behind their own LBs)

Routing decision (L7):  GET /api/users/42  + cookie "sid=abc"
  → cookie sid=abc → server api-3 (sticky session)
  → health check says api-3 is UP → forward, reuse pooled TCP conn
  → api-3 replies; LB passes response through (or DSR if L4)
Failover: api-3's /healthz starts returning 503 → LB marks it DOWN
  → next request → api-1; api-3 drained before any shutdown.
```
Note the *layering*: the edge L4 doesn't parse HTTP (it just moves sessions fast); the L7 LB makes the app-aware decisions; health checks run independently at both levels; session state lives in Redis, so even sticky-session servers are interchangeable.

## 9. Internal Working
1. **Health-check loop**: LB probes each backend every N s (TCP connect, or HTTP GET `/healthz` expecting 200/JSON `{"ok":true}`). On failure (timeout, 5xx, bad body), the server is marked down — *but* flapping servers get slow-start/backoff to avoid "turbulence."
2. **Connection management (L4)**: the LB terminates client connections and creates *pooled* backend connections (keeps them warm, reduces handshake cost per request). For UDP, it maintains session tables (client ip:port → backend ip:port).
3. **DSR/NAT vs proxy**: L4 NAT-mode LBs rewrite dst IP to the backend (server sees the client's real IP — good for auth/logs); DSR mode lets the server reply directly (fastest, but needs the LB's IP on loopback); full-proxy mode terminates and re-encrypts (L7, hides client IP unless `X-Forwarded-For`).
4. **Algorithm execution**: per-new-request, pick a backend: least-connections = min(active conns); EWMA = min(EWMA(response time)); consistent hash = ring slot for the key; then send.
5. **Stickiness**: LB sets `SET-COOKIE: SRV=<server-id>` on the first response; subsequent requests with that cookie → same server; or source-IP hash when cookies aren't possible (e.g., raw TCP).
6. **Graceful lifecycle**: deployment drains (remove from pool, wait for in-flight), then rotates; failure detection removes instantly; capacity scales by adding servers (auto-scaling groups).
7. **GSLB/DNS**: authoritative DNS has health data per site; on a query it returns the site-appropriate LB IP (geo/latency/health); TTLs are short (30–60 s) so failover is quick; anycast gives the same IP from many sites (BGP-driven "closest is best").
8. **Observability**: LBs export metrics (req/s, error rate, latency histograms, queue depth) — the *first* place to look when a service degrades; circuit breakers at the mesh level trip on error thresholds.

## 10. Time Complexity
- **L4 forwarding**: O(1) per packet (hash on 5-tuple; hardware/smartNIC/DPDK does this at line rate, tens of millions of packets/sec per LB).
- **L7 decision**: O(1)–O(payload) — header parse + rule match (path/cookie); TLS termination is the real cost (per-connection CPU, though TLS 1.3 + session resumption help).
- **Algorithm cost**: round-robin/least-connections = O(1); consistent hashing = O(log N) per lookup (ring). The pool is small (tens–hundreds of backends), so these are effectively free.
- **Health checks**: O(pool) every interval — the constant background cost; checking too aggressively (fast, small intervals) wastes backend CPU; too slowly = slow failover.
- **Scale reality**: one LB pool = thousands–millions of concurrent connections (state per session!). The *state* is the complexity — LB memory ∝ active sessions; connection tables are the "capacity" metric of L4 LBs (why DSR/stateless designs exist).

## 11. Advantages
- **Horizontal scaling**: add servers → add capacity; no single-machine ceiling.
- **Availability**: instant failover on server/region failure — clients never see it (the service is *as good as its health checks*).
- **Graceful ops**: rolling deploys, maintenance, and scaling with zero downtime (drain → rotate → replace).
- **App-aware routing (L7)**: path/header/cookie routing, TLS termination, request rewriting, auth — the LB is a *policy* point.
- **Simplicity of architecture**: the LB is the single entry point — one DNS name, one place to add caching/limits/tracing.
- **Protocol-agnostic (L4)**: any TCP/UDP app gets balanced without app changes.

## 12. Disadvantages
- **Single point of failure (itself)**: the LB must be redundant (active-active or active-standby with VRRP/keepalived) — the "LB is a SPOF" classic interview trap.
- **State cost**: connection tables + stickiness make LBs stateful — memory-heavy, hard to scale out, and painful across regions (why stateless/DSR designs and anycast exist).
- **Stickiness traps**: sticky sessions pin traffic (imbalanced load, longer failover — sessions lost when the pinned server dies). The fix (stateless services / externalized sessions) is an architecture decision.
- **L7 CPU/TLS cost**: terminating TLS + parsing HTTP per request is expensive — TLS termination farms / offload needed at scale.
- **Latency/overhead**: extra hop (proxy adds ~ms), plus connection-pool inefficiencies if misconfigured.
- **Health-check blindness**: LBs trust health checks; a "healthy but broken" backend (bad healthz logic) still receives traffic — the classic "it's green but the site's down" incident.

## 13. Interview Questions
1. **Q: What is load balancing and why do you need it?** A: Distributing traffic across a pool of servers for scale (no single bottleneck), availability (failover on failure), and maintainability (zero-downtime deploys). It's the foundation of horizontal scaling.
2. **Q (FAANG): L4 vs L7 load balancing?** A: L4 balances TCP/UDP *sessions* by IP:port — fast, protocol-agnostic, can't read payload. L7 terminates TLS and reads HTTP (path, headers, cookies) — app-aware routing, stickiness, rewriting, but per-request CPU. Production layers both: L4 at the edge, L7 in the app tier.
3. **Q: Round-robin vs least-connections?** A: RR = rotate fairly (simple, ignores load); least-connections = send to the fewest active connections (tracks *actual* load — the right default when requests have different costs). Weighted RR handles capacity differences; least-response-time handles heterogeneous servers.
4. **Q (tricky): What is session affinity and when do you need it?** A: Sending the same client to the same server when the app keeps session state in memory (cookies/IP-hash/sticky). Needed for stateful backends; *avoidable* by making services stateless (JWT/Redis sessions) — the modern best practice that removes the stickiness failure mode.
5. **Q: How do health checks work and why do they matter?** A: The LB probes each backend (TCP connect, HTTP `/healthz`, deep check) on a timer; failure → removed from rotation, recovery → re-added. LBs are only as good as their health checks — a "healthy-but-broken" backend is a classic outage cause.
6. **Q (FAANG): How do you deploy without downtime?** A: Rolling/blue-green: drain the old server (stop new connections, finish in-flight), let the LB's health check mark it down, replace, then re-add. The LB's connection draining + health checks make zero-downtime deploys possible.
7. **Q: What is DSR (direct server return)?** A: The LB forwards the request but the *server* replies directly to the client (bypassing the LB on the return path) — the return traffic bottleneck disappears. Requires servers to bind the LB's IP on loopback; used by high-throughput L4 LBs.
8. **Q (tricky): What is consistent hashing and why is it better than modulo?** A: `server = hash(key) % N` reshuffles *all* keys when N changes → cache thundering herd. Consistent hashing places servers on a ring; adding/removing a server moves only ~1/N of keys — minimal reshuffling, standard for cache-distributed systems (memcached/Redis).
9. **Q: How do you scale the load balancer itself?** A: Make it stateless/redundant: active-active pairs, VRRP/keepalived failover, hardware/DPDK LBs for L4, and **anycast** (same IP from many sites → BGP sends each client to the nearest) — the CDN/DNS-level answer to "what if the LB is the bottleneck?"
10. **Q (FAANG): DNS round-robin vs a load balancer?** A: DNS can return multiple IPs, but it has no health awareness, no per-connection state, and caching (TTL) delays failover. The LB adds *active* health checks, connection management, sticky sessions, and immediate failover. GSLB *combines* DNS (geo/latency) with LB health data — best of both.
11. **Q: What does `X-Forwarded-For` do?** A: In proxy/L7 mode the LB terminates the client connection, so backends must learn the client's real IP from the `X-Forwarded-For` header (or PROXY protocol for L4). Critical for auth/logs/rate-limiting; must be trusted and scrubbed to avoid spoofing.
12. **Q (tricky): Load balancer is a single point of failure — how do you make it HA?** A: Redundancy: active-passive (VIP + VRRP heartbeat — the standby takes the IP on failure) or active-active (both serve, VIP via ECMP/anycast), stateless LBs (sessions in a shared store or cookie-based), and health-checked pools at *every* layer. The LB itself must be as available as the service it fronts.
13. **Q: What metrics does an LB expose and what do you watch?** A: Requests/sec, error rate (5xx), latency percentiles (p50/p99), queue depth, backend health flapping, connection count. The p99 latency + error rate are the first signs of a degrading backend or an overloaded LB.
14. **Q (FAANG): "Design the load balancing for a global API."** A: Anycast/GSLB DNS → nearest regional L4 LB (fast, DDoS-scaled) → regional L7 LB (TLS term, routing, stickiness via cookie) → stateless app pool → Redis sessions + DB replicas behind their own LBs; health checks everywhere, circuit breakers in the mesh, metrics + tracing. The point: *layered* LBs with stateless backends and per-region redundancy.
15. **Q (tricky): What is a "connection drain" and why is it important?** A: When a server leaves rotation, the LB stops sending *new* connections but lets in-flight ones finish — so clients never get mid-request errors during deploys/failures. Skipping drain = dropped in-flight requests = the classic "deploy breaks the site" symptom.

## 14. Follow-Up Questions
1. **Q: Envoy/Istio service mesh — how is it load balancing?** A: Each service gets a sidecar proxy that balances, retries, circuit-breaks, and mTLS-encrypts its own requests to peers — load balancing moves *into* the app topology (per-service pools, automatic retries, resilience patterns) instead of just at the edge. L7 in the mesh + L4/L7 at the edge = the modern stack.
2. **Q: How does the LB preserve client IPs in cloud NAT/proxy setups?** A: Via `X-Forwarded-For` (HTTP) or the **PROXY protocol** (a TCP-level header injected by the L4 LB — avoids header spoofing). Backends must be configured to read it and to scrub untrusted values.
3. **Q (production): "Traffic spikes, one backend is drowning, p99 explodes. What do you check?"** A: (1) Health checks still green but backend queue saturated → check the LB's *least-connections/EWMA* (a naive RR would keep drowning it); (2) look at per-backend latency + connection count metrics; (3) the LB's own CPU (TLS offload saturated?); (4) then scale the pool (autoscaling lag is often the real cause — set preemptive scaling).
4. **Q: What is sticky-session cookie insertion?** A: On first response the LB appends `Set-Cookie: SRV=server-id`; the client echoes it; the LB routes by it. Works across L7 only, and must be cleaned on server removal (or the cookie pins clients to a dead server → brief errors until LB ignores stale cookies).
5. **Q (tricky): Load balancing vs circuit breaking vs rate limiting — the distinction?** A: LB = distribution (spread load). Circuit breaker = stop sending to a *failing* dependency entirely (fail fast, trip on error thresholds, half-open to recover). Rate limiting = cap requests per client/tenant (protect the system from bursts). All three live at the edge/mesh and are often confused in interviews — know the boundary.

## 15. Coding Example
```python
import time
import random
from collections import deque

class LeastConnectionsLB:
    """A tiny least-connections load balancer with health checks."""
    def __init__(self, backends):
        self.backends = {b: {"conns": 0, "healthy": True} for b in backends}

    def health_check(self):
        for b in self.backends:                      # fake /healthz probe
            self.backends[b]["healthy"] = random.random() > 0.1

    def pick(self):
        self.health_check()
        healthy = [(b, s["conns"]) for b, s in self.backends.items() if s["healthy"]]
        b = min(healthy, key=lambda x: x[1])[0]      # fewest active connections
        self.backends[b]["conns"] += 1
        return b

    def done(self, b):
        self.backends[b]["conns"] -= 1

lb = LeastConnectionsLB(["api-1", "api-2", "api-3"])
for _ in range(10):
    b = lb.pick(); print("route to", b, "->", lb.backends)
    time.sleep(0.05); lb.done(b)
```
```bash
# The LB toolbox
$ curl -i -H "Host: api.example.com" http://lb-ip/healthz          # probe via LB
$ curl -I -s -H "X-Forwarded-For: 1.2.3.4" http://lb-ip/           # test routing
# See what's actually happening (HAProxy):
$ socat - UNIX-CONNECT:/run/haproxy.sock <<< "show stat"           # per-backend health/conns
$ socat - UNIX-CONNECT:/run/haproxy.sock <<< "show servers state"
# tcpdump at the LB: 5-tuple per session; watch backend selection:
$ tcpdump -ni eth0 -tttt 'host backend-pool' | head
```

## 16. Industry Usage
- **Cloud managed LBs (the default)**: AWS ALB (L7) + NLB (L4) + Global Accelerator (anycast), GCP L7/L4 + Cloud Load Balancing + Cloud CDN, Azure Front Door/Load Balancer — every production service fronts its pool with one.
- **The big internet LBs (open source)**: HAProxy (10M+ conns on one box, the L4/L7 workhorse), NGINX (L7 + caching + TLS), Envoy (the mesh LB — Lyft origin, now the CNCF standard behind Istio/gateway APIs), and LVS/DPDK/Dataplane kernels for L4 at scale.
- **Service mesh**: Envoy sidecars in Istio/Linkerd/Consul — per-service balancing, retries, circuit breakers, mTLS inside the mesh (the 2020s production standard).
- **Global/GSLB**: Route 53 + ALB, NS1, Akamai — DNS geo/latency/health balancing across regions; CDN anycast (Cloudflare/Google) routes every client to the nearest PoP.
- **Databases**: PgBouncer/Haproxy in front of Postgres replicas, MySQL Router, Redis Cluster's own sharding+proxy — reads balanced, writes pinned.
- **Edge/DDoS**: L4 anycast LBs absorb volumetric attacks (they spread traffic across huge pools) — the reason "put everything behind an anycast LB" is security advice.

## 17. References
- Kurose & Ross, *Computer Networking*, Ch. 2 §2.2.5 (web server/caching, load distribution).
- NGINX Load Balancing docs: https://nginx.org/en/docs/http/load_balancing.html
- HAProxy docs (algorithms, health, statelessness): https://www.haproxy.org/
- Envoy Proxy docs (LB policies, circuit breaking): https://www.envoyproxy.io/docs/
- Consistent hashing: https://en.wikipedia.org/wiki/Consistent_hashing
- AWS ALB vs NLB: https://docs.aws.amazon.com/elasticloadbalancing/
- PROXY protocol: https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt

## 18. Cheat Sheet
- LBs give: scale (horizontal), availability (failover), ops (drain/roll).
- L4 = TCP/UDP session (IP:port), fast, DSR possible, protocol-agnostic.
- L7 = TLS term + HTTP parse (path/cookie/header) → app-aware routing.
- Algorithms: RR, weighted RR, least-connections (default), least-response-time, IP-hash, consistent hash, random.
- Health checks: TCP connect / HTTP GET /healthz; failure → out of rotation.
- Stickiness: cookie or source-IP; avoid by making backends stateless.
- GSLB = DNS + geo/latency/health; anycast = same IP from many sites (BGP nearest).
- DSR: server replies direct → return traffic skips the LB.
- `X-Forwarded-For` / PROXY protocol = real client IP to backends.
- Draining = stop new conns, finish in-flight (zero-downtime deploys).
- The LB itself must be HA (active-active/standby, anycast) — never a SPOF.
- Watch: req/s, error rate, p99 latency, queue depth, health flapping.

## 19. Quiz
1. L7 LB reads: a) IP only b) HTTP headers/path c) TCP ports d) DNS → **b**
2. Default-ish algorithm for heterogeneous load: a) RR b) least-connections c) random d) static → **b**
3. Consistent hashing minimizes: a) latency b) reshuffling on pool change c) TLS d) health checks → **b**
4. Stickiness is needed for: a) stateless apps b) in-memory sessions c) DNS d) UDP → **b**
5. DSR means: a) server replies direct b) client replies c) DNS d) static → **a**
6. GSLB uses: a) DNS b) OSPF c) QoS d) NAT → **a**
7. Health check failure: a) server stays b) removed from rotation c) LB restarts d) DNS → **b**
8. Drain = a) stop new conns + finish in-flight b) drop all c) restart d) cache → **a**
9. LB's own HA uses: a) VRRP/anycast b) DNS only c) QoS d) BGP best-path → **a**
10. Client's real IP at L7 comes via: a) X-Forwarded-For b) src IP c) cookie d) PROXY-only → **a**

## 20. Flashcards
- **Q: L4 vs L7 LB?** → **A:** session-level (IP:port, fast) vs HTTP-aware (path/cookie/TLS, smart).
- **Q: Least-connections?** → **A:** route to fewest active connections — tracks real load.
- **Q: Consistent hashing?** → **A:** ring-based; only ~1/N keys move when pool changes.
- **Q: Stickiness?** → **A:** same client → same server (cookie/IP-hash) for stateful backends.
- **Q: Health checks?** → **A:** probes → remove unhealthy from rotation.
- **Q: DSR?** → **A:** server replies directly, bypassing LB return path.
- **Q: GSLB / anycast?** → **A:** DNS geo/health + same-IP-many-sites for global balance.
- **Q: Draining?** → **A:** stop new, finish in-flight → zero-downtime deploys.
- **Q: LB as SPOF?** → **A:** make it redundant (active-active, anycast) + stateless.

## 21. Revision
Load balancing = distribute traffic across a pool for scale, availability, ops. L4 (TCP/UDP session, fast, DSR) vs L7 (TLS term, HTTP-aware routing, stickiness). Algorithms: RR, weighted RR, least-connections (default), EWMA response time, consistent hashing (ring, ~1/N reshuffle vs modulo's total reshuffle). Health checks (TCP/HTTP `/healthz`) drive removal/recovery. Stickiness via cookie/IP-hash — but stateless backends (JWT/Redis) remove it. DSR = direct server return. GSLB = DNS + geo/latency/health; anycast = same IP many sites (BGP nearest). Draining enables zero-downtime deploys. `X-Forwarded-For`/PROXY = client IP. LB must itself be HA (VRRP/anycast/stateless). Watch req/s, errors, p99. Used: cloud ALB/NLB, HAProxy/NGINX/Envoy, service mesh (sidecar LBs), DB read replicas, CDN anycast.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is load balancing / why?" | 2 How It Works / 5 Intuition |
| "L4 vs L7?" | 13 Q&A / 7 Formal Definition |
| "Algorithms (RR vs least-conns, consistent hash)?" | 13 Q&A / 5 Intuition |
| "Session affinity / stickiness?" | 13 Q&A / 9 Internal Working |
| "Health checks?" | 13 Q&A / 9 Internal Working |
| "Zero-downtime deploys / draining?" | 13 Q&A / 9 Internal Working |
| "What is DSR?" | 13 Q&A / 7 Formal Definition |
| "GSLB / anycast / DNS vs LB?" | 13 Q&A / 10 Time Complexity |
| "LB as SPOF / scaling the LB?" | 13 Q&A / 12 Disadvantages |
| "Design a global load-balanced API?" | 13 Q&A / 16 Industry Usage |
