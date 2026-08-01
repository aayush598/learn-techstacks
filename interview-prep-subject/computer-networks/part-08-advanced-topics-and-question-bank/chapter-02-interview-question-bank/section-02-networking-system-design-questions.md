# Networking System Design Questions

> **TL;DR**: The classic architecture-interview questions — URL shortener, chat app, video streaming, CDN, API gateway, IoT ingest, multiplayer game, search — each answered network-first: DNS/GSLB steering, LB tiers, edge/cache placement, latency math, and the protocol choices (HTTP/2/3, WebSocket, QUIC) that make them scale.

## 1. Why Does This Exist?
System-design interviews aren't about drawing boxes — they're about justifying *every* box with a number and a protocol. The network layer is where most designs live or die: DNS steering (GSLB) decides where users land, LB tiers decide how load spreads, CDN/edge placement decides latency, and the transport choice (TCP/HTTP/2 vs QUIC vs WebSocket) decides whether your design survives lossy, high-latency, or real-time conditions. This section exists to give you a **reusable network-first design framework** and worked answers to the eight most-asked questions, so you can lead with the network instead of fumbling it.

## 2. How Does It Work?
**The network-first design framework (use for every question):**
1. **Requirements & numbers** — traffic, latency budget, availability, geo.
2. **DNS/GSLB** — where does the user resolve? Global steering (geo/ECS + latency + health).
3. **Edge & LB tiers** — CDN/edge cache (static offload), L4 (scale), L7 (routing/TLS/WAF).
4. **Protocol choice** — HTTP/1.1 vs 2 vs 3/QUIC, WebSocket/SSE, UDP custom — with *why* (HOL, RTT, mobility).
5. **State & sessions** — where does session state live (sticky, Redis, JWT stateless)? Anycast vs GSLB constraints.
6. **Data path & capacity math** — throughput, BDP, buffer sizes, per-region capacity.
7. **Failure & scale** — region failover, health checks, autoscaling, DDoS.
8. **Reality check** — "what breaks at 10x?" walk the bottleneck.
Each worked answer below follows this shape and calls out the numbers.

## 3. When Is It Used?
- The **system-design round** at Google/Meta/Amazon/Stripe/Cloudflare (design X at scale).
- Any **"how would you build...?"** senior/staff question with a network component (almost all of them).
- **Architecture review** discussions in interviews for infra/networking roles.
- Pair with Section 01 (rapid-fire) and Section 03 (hands-on) for a complete prep stack.

## 4. Why Wasn't Another Approach Chosen?
- *Just memorize designs:* interviewers probe with "what if latency doubles / this region dies / traffic spikes 10x" — you need the *reasoning*, not a recipe. The framework gives reasoning.
- *App-only design (no network):* every interviewer pushes on the network — "how does the user reach it? what if a region dies? how do you handle DDoS?" The framework front-loads the network answers.
- *Over-detailed networks:* you don't need to design BGP; you need the *right level* (GSLB, LB tiers, cache placement, protocol choice) with justification. The answers calibrate that level.

## 5. Intuition
Think of every system as **the same four layers from the user's eyes**: (1) *Find it* — DNS/GSLB picks the right region; (2) *Reach it* — edge/LB tiers route and absorb; (3) *Serve it* — app/stateless services behind caches; (4) *Protect it* — TLS/WAF/DDoS + failover. Every question is the same skeleton with different business logic. If you can draw and defend those four layers with numbers, you can design anything — the network is the common denominator.

## 6. Real-World Analogy
A **restaurant chain with global delivery**. Finding you: the chain's directory (DNS/GSLB) knows which branch can serve your zip code fastest. Ordering: your order hits the city's central kitchen (L7 LB) which routes to a branch (app tier) that's not busy. Speed: popular dishes are pre-made at a satellite kitchen near you (CDN/edge cache). Delivery: couriers (protocols) chosen for freshness (WebSocket for live order tracking) vs regular mail (HTTP for static pages). If a branch burns down (region failover), the directory reroutes instantly. Capacity: when it's 8pm (peak), the chain opens more branches (autoscale) and limits delivery radius (rate limit) so nobody waits forever.

## 7. Formal Definition
- **Design interview rubric**: requirements → API/data model → architecture → scale/failure → trade-offs; scored on *reasoning quality*, numbers, and stated trade-offs.
- **Network primitives used**: DNS + GSLB (Section 08-01), anycast (08-02), L4/L7 LB + spine-leaf (08-03), CDN/edge, HTTP/1.1/2/3, QUIC, WebSocket/SSE, TCP/UDP (P3), TLS/mTLS (P7), NAT (P4).
- **Latency budget math**: total = DNS + TLS + RTT to edge + edge→origin + processing; CDN cuts the user→edge distance; 100 ms budget typical for interactive; < 400 ms for most web.

## 8. Example
**Quick mini-answer — Design a URL shortener (network parts):**
```
User clicks short URL → DNS: GSLB (anycast) resolves shrt.example.com → nearest edge
Edge (L4/L7, anycast CDN) → hits the regional LB → stateless app (JWT session, no sticky)
App: read cache (Redis, hit ~95%) → else DB (shard by hash of short-code, read replica)
Redirect 301/302 → origin? No: the edge cache stores the mapping (long TTL) → offload
Failure: region dies → GSLB health check removes it → next region; DB replicas per region
Scale: stateless app ×N behind LB; cache + sharded DB; numbers: 100M/day ≈ 1.2k qps avg
```
This is the "find → reach → serve → protect" skeleton in action.

## 9. Internal Working (per question)
**Q1. Design a URL shortener.**
- Find: anycast GSLB DNS; short-code (base62) in the URL path.
- Reach: edge LB (L7, TLS) → regional LB → app (stateless).
- Serve: Redis cache (code→URL, TTL 24h) → sharded SQL (hash(code)%N) with read replicas.
- Write: app generates code, writes to DB + invalidates cache; async stats pipeline.
- Numbers: 100M/day writes ≈ 1.2k wps; 1B reads/day ≈ 12k rps → 2-4 app instances + cache tier suffice; scale-out is stateless.
- Failure: cache loss = DB thundering herd (mitigate with locks/rebuild); DB shard down = failover replica; region down = GSLB steer.

**Q2. Design a chat application (WhatsApp/Slack-style).**
- Find: GSLB + anycast edge; WebSocket to edge LB (L7, sticky via JWT/user-id hash).
- Reach: edge LB → chat service (stateless) → per-conversation state.
- Serve: message bus (pub/sub, partitioned per conversation) → delivery service → DB (partitioned) for history.
- Realtime: WebSocket (full-duplex, low latency); SSE fallback; presence via pub/sub; ack/re-delivery per client for reliability (app-level, not TCP).
- Scale: shard conversations by hash (state locality); region failover with message queue replay; offline delivery (push) via bus.
- Numbers: 100M DAU, avg 100 msgs/day → ~120k msg/s peak × ~1 KB = ~120 MB/s bus throughput → partition across many nodes.

**Q3. Design a video streaming platform (Netflix-style).**
- Find: GSLB steers to nearest CDN PoP (anycast edge cache).
- Reach: edge LB → catalog API; media comes from edge *cache* (open connect/appliance), not origin.
- Serve: manifest (DASH/HLS) + segment files (4-10 s chunks) served by cache; adaptive bitrate (ABR) picks quality by measured throughput.
- Protocol: HTTP/2/3 (range requests, parallel segments, QUIC for mobility); TCP tuning for high-BDP (BBR/CUBIC).
- Numbers: 1M concurrent viewers × 5 Mbps avg = 5 Tbps egress → must be CDN-distributed (origin can't do it); cache hit ~95%+ at edge.
- Failure: cache miss → edge fetch from origin (penalty); region failover; DRM licensing per segment.

**Q4. Design a CDN (Akamai/Cloudflare-style).**
- Find: anycast for the edge IPs + GSLB for site-level steering (Section 08-01).
- Reach: anycast PoPs each with L4/L7 edge → cache tier → origin (tunneled, e.g., authenticated backhaul).
- Serve: cache with LRU/TTL + revalidation (ETag); purges via control plane; TLS termination at edge.
- Scale: PoP capacity = anycast attract; cache hit ratio drives origin offload; global index/control plane for config distribution.
- Numbers: cache server at a PoP does 10-50 Gbps; PoPs ~1-3 Tbps; global aggregate tens of Tbps.

**Q5. Design an API gateway / microservices front door.**
- Reach: L4 NLB → gateway instances (L7: routing, auth, rate limit, TLS, request shaping) → per-service mesh mTLS.
- Serve: gateway routes by path/host to services; circuit breakers/timeouts per route; idempotency keys for writes.
- Protocol: HTTP/2 to clients (multiplex), gRPC internally; mTLS between services.
- Numbers: gateway = CPU-bound (TLS + parsing); NLB spreads flows; scale gateways by CPU; per-service rate limits + quotas.
- Failure: gateway redundancy (N+1 per AZ), health checks, circuit breakers isolate a slow service.

**Q6. Design a real-time multiplayer game (mobile).**
- Reach: anycast/GSLB to the nearest regional relay/edge; UDP preferred (low latency, loss-tolerant).
- Serve: game logic in regional "room" servers; state = authoritative server (anti-cheat); snapshots every 33-100 ms.
- Protocol: UDP custom (QUIC-style, or DTLS) with interpolation/input buffering to hide loss; TCP only for login/meta.
- Numbers: room = 10-50 players; server handles N rooms; region capacity = concurrent players; matchmaking via GSLB latency maps.
- Failure: player migration (QUIC connection migration / client rejoin), room failover, loss hides via interpolation.

**Q7. Design an IoT telemetry ingest (millions of devices).**
- Reach: devices → edge endpoints (anycast, UDP/QUIC or MQTT over TCP 8883) → regional ingest LB.
- Serve: ingest service → partition by device-id hash → message bus → time-series DB (TSDB sharded).
- Protocol: MQTT (publish/subscribe, lightweight, QoS) or HTTP/2/3 batch for less critical data; QUIC for lossy mobile.
- Numbers: 10M devices × 1 msg/min = ~170k msg/s × 1 KB ≈ 170 MB/s ingest → many partitioned nodes; idempotent device IDs dedupe.
- Failure: device reconnect storms (exponential backoff server-side), queue as buffer when TSDB is slow.

**Q8. Design a search / autocomplete at scale.**
- Find/reach: edge + GSLB; L7 LB → query service (stateless) → index tier (partitioned, replicated).
- Serve: in-memory index shards (by term), top-k merges, cache hot queries (Redis/CDN for results); trie/bigram suggestions precomputed.
- Protocol: HTTP/2/3 for low-latency UI; persistent connections reduce per-query TLS cost.
- Numbers: latency budget < 100 ms; cache hit for tail queries; index replica per region; shard count by corpus size.
- Failure: index rebuild/version skew, replica failover, load shedding on hot shards.

## 10. Time Complexity / Performance
- **Latency budgets**: URL shortener < 50 ms (cache); chat delivery < 100 ms; streaming first-frame < 1-2 s; game 50-100 ms tick; IoT ingest batching ms-s; search < 100 ms.
- **Scale levers**: cache (10-100× offload), CDN/edge (moves traffic closer + absorbs), L4 LB (millions of flows), sharding (linear scale), anycast (nearest node).
- **The one number that matters**: throughput ≈ requests × avg work; then "which tier is the bottleneck at 10×?" — answer: cache (ok) → DB (shard) → network (region/capacity).

## 11. Advantages
The framework is **question-agnostic** (find→reach→serve→protect), numbers-driven, and network-first; it produces answers interviewers can probe without you going off the rails; it surfaces the important trade-offs (statefulness vs anycast, cache vs origin, HTTP/2 vs 3) explicitly.

## 12. Disadvantages
It's an interview artifact, not a build blueprint — real systems add deployments, monitoring, cost optimization, and vendor constraints. Also, answers are judgment calls; two good interviewers can disagree (which is fine — reasoning is what's scored).

## 13. Interview Questions (from this section)
1. **Q: Walk me through designing a URL shortener.** A: See Q1 worked answer: anycast GSLB → edge L7 → stateless app → Redis cache (95% hit) → sharded DB; base62 codes; 301 redirects; async stats; region failover via health-check steering.
2. **Q: Design a chat app at 100M DAU.** A: See Q2: WebSocket to edge LB (sticky via user hash), pub/sub per conversation, DB partitioned, offline delivery via queue, app-level acks; numbers: ~120k msg/s peak.
3. **Q: Design a video streaming platform.** A: See Q3: GSLB → CDN edge cache, manifest + 4-10 s segments, ABR, HTTP/2/3 + TCP tuning (BBR), DRM per segment; origin offload by edge cache hit ratio; 5 Tbps scale impossible without CDN.
4. **Q: Design a CDN.** A: See Q4: anycast edge IPs + GSLB site steering, L4/L7 + cache tier with LRU/TTL/ETag, purges via control plane, TLS termination at edge, origin via authenticated tunnel.
5. **Q: Design an API gateway for microservices.** A: See Q5: NLB (L4) → gateway (L7: route/auth/rate-limit/TLS) → services with mesh mTLS; circuit breakers; idempotency keys; N+1 gateway redundancy.
6. **Q: Design a real-time game (mobile multiplayer).** A: See Q6: UDP/QUIC with client-side prediction/interpolation, authoritative room servers, regional anycast relays, latency-map matchmaking; TCP only for login/meta.
7. **Q: Design IoT telemetry ingest for 10M devices.** A: See Q7: anycast edge → ingest LB → partition by device-id → bus → TSDB; MQTT/QUIC protocols; idempotency; reconnect backoff; bus as buffer.
8. **Q: Design autocomplete/search at scale.** A: See Q8: edge + L7 LB → stateless query service → in-memory index shards + top-k merge + hot-query cache; < 100 ms budget; replica per region.
9. **Q: What would you change at 10× traffic?** A: (1) caches hit ratio → add layers/CDN; (2) DB → read replicas → sharding; (3) LBs → scale-out (stateless); (4) region → add regions + GSLB steering; (5) DDoS → anycast scrub + WAF + rate limit. The bottleneck walk *is* the answer.
10. **Q: How do you make the design resilient to a regional outage?** A: Active-active regions, GSLB health-check failover (short TTLs), data replication (sync per-AZ, async cross-region), stateless apps (JWT/Redis), and a runbook; accept the trade-off of async replication (data loss window) vs synchronous cost.
11. **Q: TRICKY — When would you *not* use a CDN?** A: For dynamic, user-specific, or real-time data (chats, dashboards, streaming of live events) — caches serve stale/static content; also for low-traffic internal services where edge adds complexity. Use caches for what's cacheable (static, hot-read, idempotent).
12. **Q: How do you decide HTTP/2 vs HTTP/3/QUIC for your design?** A: HTTP/2 for most web (multiplexing, mature infra); HTTP/3/QUIC when the client is mobile/roaming (connection migration), when lossy networks cause TCP HOL blocking, or when you need 0-RTT/1-RTT for latency. Same app protocol, different transport.
13. **Q: PRODUCTION — Your latency budget is 100 ms. Where does it go?** A: DNS (cached ~0-5 ms) → TLS (1 RTT ~30 ms on 30 ms RTT; 0-RTT resumption) → edge→origin (~30 ms) → app+DB (~20-40 ms) → totals ~100 ms; shave with edge cache (skip origin), resumption, and keep DNS/TLS cached. Always state the budget breakdown.
14. **Q: How do you handle a DDoS on the design?** A: Anycast scrubbing at the edge (absorb + filter), L4/L7 rate limits, WAF rules, per-IP/user quotas, auto-scaling for absorption, and origin protection (only edge can reach origin via authenticated tunnel). (Section 07 covers attack details.)
15. **Q: SCENARIO — A region's LB is at 95% CPU. Design the fix.** A: (1) offload TLS to a separate edge/TLS-tier; (2) split L4 (spread) from L7 (route); (3) scale-out the L7 tier (stateless) behind L4; (4) reduce per-request cost (HTTP/2 pooling, caching headers); (5) add a second region + GSLB steer. Then implement: autoscale with health checks.
16. **Q: How do you choose sticky sessions vs stateless JWT?** A: Sticky = easier, but ties clients to a node (LB affinity by hash) and complicates scaling/failover. Stateless JWT = any node can serve (pure scale-out, no affinity), but revocation is harder and token size adds bytes; use short TTLs + a cache to revoke. For chat/stateful flows, keep state in a cache (Redis) and keep nodes stateless.
17. **Q: What is the role of health checks in the design?** A: They drive LB membership (remove unhealthy), GSLB region failover (Section 08-01), and autoscale signals. Probe the *app* path (not just TCP): /healthz returns 200 only when dependencies are healthy. Health checks are what make "region down" and "pod dying" automatic instead of manual.

## 14. Follow-Up Questions
1. **Q: What numbers should I memorize?** A: RTT budget 100 ms; cache hit 95%+; CDN egress per PoP 10-50 Gbps; L4 LB millions of flows; HTTP/2 vs 3; TLS 1-RTT; BDP formula; 5 Mbps/viewer streaming; msg size ~1 KB. Say numbers out loud — interviewers probe them.
2. **Q: How do I practice?** A: Do one design a day with the framework; speak it aloud in 20 min; force the "10×" bottleneck walk every time; use the network-first order (DNS→LB→edge→origin→scale→failure) so it becomes reflexive.
3. **Q: What if the interviewer only wants app-level?** A: Compress the network layer to 2-3 sentences (GSLB + edge + L4/L7) then focus depth where asked — but always *state* the network tier once, because it sets the latency/scale assumptions for everything else.

## 15. Coding Example
```python
# Capacity math for a design (the numbers interviewers love to probe)
def capacity(users_per_day, requests_per_user, peak_to_avg=3):
    avg_rps = users_per_day * requests_per_user / 86_400
    return avg_rps, avg_rps * peak_to_avg, avg_rps * peak_to_avg * 1024  # rps, peak rps, bytes/s @1KB

avg, peak, bw = capacity(100_000_000, 10)   # URL shortener-ish: 1B requests/day
print(f"avg {avg:.0f} rps | peak {peak:.0f} rps | {bw/1e9:.1f} GB/s")  # ~11.6k rps avg, ~2.5 GB/s peak
```
```bash
# Verify real-world latency budget parts on a target (curl gives the same numbers as a design answer)
curl -s -o /dev/null -w "dns %{time_namelookup}ms | tcp %{time_connect}ms | tls %{time_appconnect}ms | ttfb %{time_starttransfer}ms | total %{time_total}ms\n" https://example.com
# Cache headers that drive the edge-cache design decision:
curl -sI https://example.com | grep -iE "cache-control|etag|expires"
# Region/LB reality: resolve and trace your CDN/edge route
dig +short www.google.com && mtr -rn -c 5 www.google.com | tail -4
```

## 16. Industry Usage
- **Google/Meta/Amazon**: system design with a *lot* of network probing (GSLB, LB tiers, cache, region failover, latency math).
- **Cloudflare/Fastly/Akamai**: designs *are* the network (anycast, edge, GSLB, TLS).
- **Netflix/Spotify/Uber**: streaming/CDN and geo/location-heavy designs.
- **Stripe/PayPal**: API gateway, idempotency, TLS/mTLS, rate limiting under load.
- **Every infra/SRE role**: capacity math + failure scenarios dominate.

## 17. References
- Section 08-01 (GSLB/DNS/EDNS), 08-02 (anycast/multicast/broadcast), 08-03 (DC/cloud) for the network primitives.
- Part 03 (TCP/QUIC/HTTP/2), Part 02 (HTTP/3, WebSocket, CDN), Part 07 (TLS/DDoS) for protocol choices.
- System Design Interview (Alex Xu) + "Designing Data-Intensive Applications" (Kleppmann) for the general rubric.
- Cloudflare/AWS architecture blogs for real-world numbers (e.g., "how Cloudflare scales").

## 18. Cheat Sheet
- Framework: **find** (DNS/GSLB) → **reach** (edge/L4/L7) → **serve** (cache/stateless app/DB) → **protect** (TLS/WAF/DDoS/failover).
- Say numbers: budget 100 ms, cache hit 95%, L4 millions of flows, CDN PoP 10-50 Gbps, ~1 KB/msg, 5 Mbps/stream.
- Every answer ends with the "10× bottleneck walk" (cache → DB → network → regions).
- Choose protocols with a reason: HTTP/2 (web, multiplex), QUIC (mobility/lossy/HOL), WebSocket (realtime), UDP (games), MQTT (IoT).
- Health checks drive LB + GSLB + autoscale — make them app-path.
- Region failover = active-active + GSLB health steer + async replication (accept the data-loss window).
- Stats/state: keep nodes stateless (JWT/Redis); state in cache; sticky only when forced.

## 19. Quiz
1. The network-first order is: a) DB→LB→DNS b) DNS→LB→cache→origin c) cache→DNS d) none → **b**
2. A URL shortener's write rate for 100M/day: a) 1.2k wps b) 12k wps c) 100 rps d) 1M/s → **a** (≈1.2k wps; reads dominate)
3. Which fixes TCP HOL blocking for HTTP? a) HTTP/2 b) QUIC c) keepalive d) gzip → **b**
4. A CDN's main job: a) DNS b) cache at the edge to cut latency + origin load c) BGP d) TLS → **b**
5. Cache hit ratio assumed: a) 50% b) 95%+ c) 10% d) 0% → **b**
6. For real-time games you choose: a) HTTP/1.1 b) UDP with prediction c) FTP d) SMTP → **b**
7. Region failover rides on: a) TTL b) GSLB health checks + short TTLs c) NAT d) MTU → **b**
8. The one number to state first in a design: a) MTU b) the latency budget / scale numbers c) port range d) none → **b**

**Answers**: 1-b, 2-a, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Design framework** → **A:** find (DNS/GSLB) → reach (edge/L4/L7) → serve (cache/stateless) → protect (TLS/DDoS/failover).
- **Q: URL shortener stack** → **A:** anycast DNS → edge L7 → Redis (95%) → sharded DB; base62; 301.
- **Q: Chat realtime protocol** → **A:** WebSocket to edge LB, pub/sub per conversation, app-level acks.
- **Q: Streaming scale number** → **A:** ~5 Mbps/viewer; 1M viewers ≈ 5 Tbps → must be CDN-distributed.
- **Q: When NOT to use a CDN** → **A:** dynamic/user-specific/real-time content.
- **Q: 10× bottleneck walk** → **A:** cache → DB (replica→shard) → LB (scale-out) → regions → DDoS scrub.
- **Q: Health checks role** → **A:** LB membership, GSLB failover, autoscale; probe the app path.

## 21. Revision
System design = a network-first skeleton applied to any business. Always lead with: **find** (DNS/GSLB/anycast steering), **reach** (edge/CDN cache + L4→L7 LB tiers), **serve** (stateless apps, Redis, sharded DB with replicas), **protect** (TLS/WAF/DDoS anycast scrub, health-check-driven failover). State numbers early (latency budget 100 ms, cache hit 95%, L4 flows, streaming 5 Mbps). Choose transports with reasons (HTTP/2 web, QUIC mobile/HOL, WebSocket realtime, UDP games, MQTT IoT). End every answer with the 10× bottleneck walk and a region-failover story. Anchors: *find→reach→serve→protect; numbers before pictures; health checks drive everything; the design is the network (DNS→LB→cache→origin→failover).*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Design a URL shortener" | 9-Q1 / 13-Q1 |
| "Design a chat app" | 9-Q2 / 13-Q2 |
| "Design video streaming" | 9-Q3 / 13-Q3 |
| "Design a CDN" | 9-Q4 / 13-Q4 |
| "Design an API gateway" | 9-Q5 / 13-Q5 |
| "Design a real-time game" | 9-Q6 / 13-Q6 |
| "Design IoT ingest" | 9-Q7 / 13-Q7 |
| "Design search/autocomplete" | 9-Q8 / 13-Q8 |
| "What changes at 10× traffic?" | 13-Q9 |
| "Regional outage resilience" | 13-Q10 |
| "HTTP/2 vs QUIC choice" | 13-Q12 |
| "Latency budget breakdown" | 13-Q13 |
| "Health checks in design" | 13-Q17 |
