# DNS Resolution Process

> **TL;DR**: Resolving `www.example.com` is a two-step dance — the **recursive resolver** (your ISP/8.8.8.8) asks on your behalf, walking **root → TLD → authoritative** (iterative queries) to get the answer, then **caches** it for the TTL — so the first lookup costs several round trips and every repeat is instant.

## 1. Why Does This Exist?
A client needs an IP address before it can connect, but it shouldn't have to know the DNS tree's internals or take on the latency of walking root→TLD→authoritative for every lookup. The resolution process exists to answer two needs: (1) **client simplicity** — the OS asks *one* address (the recursive resolver) and gets the answer; (2) **efficiency** — caching makes repeated lookups nearly free, and TTLs bound staleness. It's the difference between a citizen calling one operator who does the whole chain (recursive) vs the citizen themselves calling three different operators one at a time (iterative).

## 2. How Does It Work?
**Recursive resolution** (client → resolver):
1. Client's stub resolver asks the configured recursive resolver: "What is `www.example.com`?"
2. The recursive resolver does the walk *on behalf of the client*:
   - **Iterative query to root**: "Who serves `.com`?" → referral to a `.com` nameserver (NS + glue).
   - **Iterative query to .com**: "Who serves `example.com`?" → referral to example.com's nameservers.
   - **Iterative query to authoritative**: "What's `www.example.com`?" → **the answer** (A record, AA bit set).
3. Resolver returns the answer to the client AND **caches** it (positive cache, TTL) and caches the referrals (negative cache for NXDOMAIN).
4. Subsequent lookups for the same name (or TLD) hit the cache — often 0 upstream queries.

**Iterative resolution** (querying servers directly, e.g., `dig +trace`): the client itself walks root→TLD→authoritative, each server answering with the next pointer rather than the final answer.

## 3. When Is It Used?
- **Every name lookup**: browsers, `curl`, email (MX resolution), APIs. The recursive path is the default for users.
- **`dig`/`nslookup` debugging**: iterative (`+trace`), query a specific resolver (`@8.8.8.8`), or query the authoritative server directly (`@ns1.example.com`).
- **CDN routing**: authoritative servers return *different* answers based on the *resolver's* IP (GeoDNS) or health (route by latency) — so resolution isn't just "one answer," it's "routing as a side effect."
- **Caching layers**: browser cache → OS stub cache → local resolver (dnsmasq) → public resolver (8.8.8.8) → authoritative. Each layer absorbs queries.

## 4. Why Wasn't Another Approach Chosen?
- **Why recursive instead of forcing clients to walk the tree?** Client-side walking (iterative) means every client needs root-hint updates, does multiple RTTs, and caches poorly. Centralizing the walk in a resolver gives: shared caching (a million clients → one cached answer), fewer root/TLD queries (load reduction), and simpler clients. Cost: clients trust the resolver (privacy — hence DoH) and depend on it (resolver outage = no DNS).
- **Why not just give the client the whole database?** Impossible (distributed, huge); also stale immediately. The resolver's cache is the pragmatic middle: only answers you need, with TTL-bounded freshness.
- **Why cache at all instead of always walking?** The root/TLD servers would be crushed by trillions of queries; latency would be brutal (several RTTs per lookup). Caching is the load- and latency-killer. TTLs exist to balance freshness vs. load.

## 5. Intuition
Resolution is **asking a travel agent (recursive resolver) to book a trip**: You (client) don't know airlines or airports — you hand the agent the destination (domain). The agent calls the airport authority (root), which says "ask the country's aviation office" (TLD), which says "ask the airline's own desk" (authoritative), which gives the flight number (IP). The agent then **remembers the route** (cache) so next time you just say the destination and it's instant. TTL = how long the agent trusts its memory before calling again.

## 6. Real-World Analogy
**The university switchboard**: You want Prof. Smith's office. You call the main switchboard (root) — "don't know, try the Science Faculty office" (TLD). Science Faculty says "Prof. Smith is in the Physics Department" (referral). Physics's office (authoritative) says "Room 4A-21" (the answer). Now imagine you're the *secretary* (recursive resolver) whom hundreds of students (clients) call: after finding it once, you keep a sticky note (cache) — so the 500th student asking gets the answer instantly without you calling anyone. The switchboard chain is only needed when the note isn't there.

## 7. Formal Definition
DNS resolution is the process of translating a domain name into resource records (typically an IP address) via the **recursive resolver** model. A **recursive resolver** (or full resolver) performs iterative queries to root, TLD, and authoritative servers on behalf of clients, following referrals (NS + glue records), then returns the final answer and caches it for the TTL. An **iterative query** asks a server to return either the best answer it has or a *referral* to a more authoritative server. Caching applies to: positive answers (A/AAAA…), negative answers (NXDOMAIN, NODATA — cached as the SOA's negative TTL), and referrals. TTLs (in each RR's TTL, minimum of SOA MINTTL for negative) bound cache lifetime. The process is defined in RFC 1034/1035; extended by RFC 2308 (negative caching), RFC 7719 (terminology).

## 8. Example
Timeline for the *first* lookup of `www.example.com` (uncached, RTT ≈ 30 ms each step):
```
Client                      Recursive resolver            Root      .com NS    Authoritative
  |--- recursive Q -------->|
  |                          |--- iterative Q -------->|   "who is .com?"
  |                          |<------ NS + glue --------|   a.gtld-servers.net
  |                          |--- iterative Q ------------------------>|  "who is example.com?"
  |                          |<------------------------ NS + glue ------|  ns1.example.com
  |                          |--- iterative Q ----------------------------------->|  "www.example.com?"
  |                          |<--------------------------------------- A 93.184.216.34 (AA) -|
  |<---- answer + TTL ------>
  |  (cached for TTL=3600 s)
```
Total: 3-4 RTTs (~90-120 ms) for the first lookup, then ~0 for the rest (browser cache, OS cache, resolver cache). With a warm resolver but cold client, the resolver answers from cache in ~1 ms.

**TTL behavior**: resolver caches `A www.example.com = 93.184.216.34 TTL 3600`. At t=3601s the record expires; next query re-walks (or asks authoritative). A website changing its IP must wait up to the old TTL for full propagation — the price of caching.

## 9. Internal Working
1. **Client side**: browser cache → OS stub (`getaddrinfo`) → `/etc/resolv.conf` nameserver → recursive resolver (UDP 53, retries with TCP for truncated responses).
2. **Recursive resolver state**: cache (positive/negative), and per-domain **delegation state** (which NS to ask next). It tracks pending queries to dedupe concurrent lookups (one upstream query serves 100 clients).
3. **Referral following**: on NS referral, the resolver *prefers* authoritative servers, may "ns-hopping" if the first fails; it validates the referral with the parent's glue.
4. **Authoritative answer**: the response has AA bit; resolver returns it (and caches). If AA missing, the answer is treated as a referral or ignored.
5. **Negative caching** (RFC 2308): NXDOMAIN (name doesn't exist) and NODATA (name exists, no record of that type) are cached using the SOA's `minimum` field (or SOA TTL) — prevents hammering the authoritative server for typos.
6. **TC bit / TCP fallback**: if the UDP response has the TC (truncated) bit set (large answers, DNSSEC, many records), the resolver retries over **TCP 53**. Also: UDP responses >512 B are legacy-truncated unless EDNS0 (larger buffers) is negotiated.
7. **EDNS0** (RFC 6891): extends UDP buffer sizes (up to 4096+ bytes), required for DNSSEC and large answers; without EDNS0, DNSSEC responses get truncated → TCP.
8. **DoH/DoT**: the *same* resolution process, but the client→resolver leg runs over TLS (853) or HTTPS (443) — hiding the query from on-path observers.
9. **Prefetching/optimization**: resolvers prefetch popular records before expiry; browsers/OS do speculative prefetch on hover/link — all to convert later lookups to cache hits.

## 10. Time Complexity
- **Cold lookup**: O(depth) round trips ≈ 3-4 RTT (root + TLD + authoritative) — constant, ~90-150 ms typical.
- **Warm lookup**: O(1) cache hit — sub-ms (resolver) to ~ms (network to resolver).
- **Cache hit ratio**: 80-95% for real workloads (popular names dominate); TTL and popularity drive it.
- **Dedup**: N concurrent clients looking up the same name = 1 upstream query (resolver merging) — O(1) upstream per name.

## 11. Advantages
- **Client simplicity**: one resolver address, one query, full answer.
- **Shared caching**: massive load reduction on root/TLD/authoritative (trillions → millions of upstream queries).
- **Latency**: warm lookups ≈ 0-5 ms; cold ≈ 100-150 ms (still fast vs TCP/TLS).
- **Resilience**: multiple authoritative servers, retries, ns-hopping; anycast resolvers.
- **Negative caching**: typos don't hammer the tree.
- **Protocol transparency**: EDNS0, TCP fallback, DNSSEC, DoH/DoT all slot into the same process.

## 12. Disadvantages
- **Privacy**: the resolver sees all queries (mitigated by DoH/DoT, but then your DNS provider is your browser/OS vendor).
- **Single point of dependence**: resolver outage = no DNS for clients (mitigate: multiple resolvers, local caching).
- **Cache poisoning/spoofing**: an attacker answering before the real server can poison cache (mitigated: 0x20 randomization, DNSSEC, random source ports).
- **Staleness**: TTL-bound — changes propagate slowly; misconfigurations persist for TTLs.
- **Performance on cold start**: first lookup adds 100+ ms (mitigated by prefetch, browser hints).

## 13. Interview Questions
1. **Q: What's the difference between a recursive and an iterative query?** A: Recursive = the resolver asks the tree *on your behalf* and returns the final answer. Iterative = each server returns a *referral* (NS/glue) and you ask the next server yourself. Resolvers use iterative queries upstream; clients use recursive queries to resolvers.
2. **Q: Walk through resolving www.example.com from an empty cache.** A: Stub → resolver → (1) root: "who is .com?" → referral to a.gtld-servers.net; (2) .com: "who is example.com?" → referral to ns1.example.com; (3) authoritative: "www.example.com?" → A 93.184.216.34 (AA). Resolver caches all, returns the answer. ~3-4 RTTs.
3. **Q (tricky): Why do you ask the root at all if the resolver knows .com?** A: The resolver's *cache* may already hold .com's NS (referrals are cached too, often with longer TTLs). The root is only consulted when the cache misses. In practice, resolvers rarely hit the root after warmup.
4. **Q: What is a referral vs an answer?** A: A referral = "I don't know, but ask *these* servers" (NS + glue, no AA bit). An answer = "here is the record" (AA bit set by the authoritative server). Distinguishing them is how resolvers know whether to keep walking.
5. **Q (production): What is negative caching and how is its TTL set?** A: NXDOMAIN/NODATA responses are cached so typos don't hammer the tree. The duration comes from the SOA record's `minimum` field (RFC 2308) — often 1-2 hours. Slow "new domain propagation" is this TTL at work.
6. **Q: How does the resolver pick between multiple authoritative servers?** A: It queries one NS, retries others on failure (ns-hopping), rotates between them (round-robin), and can use RTT/EDNS-client-subnet hints. The resolver owns failover, not the client.
7. **Q: What happens when a DNS response is truncated (TC bit)?** A: The UDP answer has more data than fits (legacy 512 B, or EDNS0 limit). The resolver retries over **TCP 53**. Common with DNSSEC and many-record zones.
8. **Q: What is TTL and why does it matter for deployments?** A: Time-To-Live — how long a record may be cached. Short TTL (60-300s) = fast failover but more authoritative load; long TTL (3600-86400) = cheap but slow propagation. "Lower your TTL before a migration, raise it after" is the standard ops rule.
9. **Q (scenario): You change an A record but users still get the old IP for an hour. Why?** A: Caches (browser, OS, resolver, CDN) are honoring the previous TTL. The authoritative server instantly serves the new record — but every cache layer holds the old one until TTL expiry. Solution: lower TTL *before* the change.
10. **Q: What is cache poisoning and how is it prevented?** A: An attacker sends a fake response before the real one, polluting the resolver's cache. Defenses: random source ports, **0x20 case randomization**, DNSSEC (signed answers), and transaction ID randomization (all in RFC 5452 guidance). DNSSEC is the definitive fix.
11. **Q: What is a "stub resolver"?** A: The OS-level client (`getaddrinfo`/`res_query` in libc) that reads `/etc/resolv.conf`, sends recursive queries to the configured resolver, and caches little. It's the thin client in the resolution architecture.
12. **Q: How does DNS resolution differ for a CDN (GeoDNS)?** A: The *authoritative* server inspects the **resolver's IP** (ECS — EDNS Client Subnet) and returns the nearest edge PoP's IP. Different resolvers → different A records → "resolution-based routing." This is how you get "nearby server" answers without the client being tracked.
13. **Q (production): 1.1.1.1 vs 8.8.8.8 — what's operationally different?** A: Both anycast public resolvers. Differences: privacy policies (Cloudflare = minimal logging, no ECS by default), features (1.1.1.1 supports DoH/DoT/0x20, 8.8.8.8 supports DoH/DoT/ECS), and some sites route by resolver (GeoDNS sees different addresses). Choose by latency + policy.
14. **Q: What is the difference between a forwarder and a recursive resolver?** A: A forwarder (e.g., dnsmasq) passes queries to an *upstream* resolver instead of walking the tree itself — it doesn't do iterative resolution. Common in home routers/enterprise: small cache + forward to ISP/8.8.8.8.
15. **Q: Why does DNS use UDP but fall back to TCP?** A: UDP (53) = one packet, stateless, fast, cheap for the tiny query/answer pattern. TCP = needed for large responses (TC bit), zone transfers, and reliable delivery. UDP+retry is the default; TCP is the safety net.
16. **Q (tricky): A user's `nslookup` works but `ping` fails. What's wrong?** A: DNS resolved the name fine, so the issue is *after* resolution — ICMP blocked, routing, firewall, or the host is down. This is the classic "DNS isn't always the problem" debugging moment: separate resolution from connectivity.

## 14. Follow-Up Questions
1. **Q: What is ECS (EDNS Client Subnet)?** A: An EDNS0 option letting the resolver tell the authoritative server a *prefix* of the client's IP (privacy-limited). It fixes GeoDNS accuracy behind shared resolvers (everyone appears to be from 8.8.8.8's location).
2. **Q: How does a resolver handle "in-flight deduplication"?** A: It tracks outstanding queries by (name, type, class); 100 clients asking the same name → 1 upstream query, and all 100 get the answer when it returns. This is a major load reduction at scale.
3. **Q: What is QNAME minimization?** A: The resolver sends only the *necessary* label to each server (e.g., to .com it asks only about `example.com`, not the full `www.example.com`) — reducing what each layer learns about your query (privacy, RFC 9156).
4. **Q: Why do ISPs' resolvers return different results than 8.8.8.8 for some sites?** A: GeoDNS (resolver location), ISP-local zones/caching, parental filtering, or (badly) interception/typosquatting. This is exactly why users sometimes "use 8.8.8.8 and it works."
5. **Q: What happens during a DNS outage at a resolver?** A: Clients can't resolve → "server not found" even though the network is up. Mitigations: multiple resolvers (fallback), local caching resolvers, browser HSTS/preload, and keeping hosts-file fallbacks for critical systems.

## 15. Coding Example
```python
import socket, time

def resolve_with_timing(host, tries=3):
    for i in range(tries):
        t0 = time.perf_counter()
        info = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
        t1 = time.perf_counter()
        print(f"try {i+1}: {(t1-t0)*1000:6.2f} ms  -> {info[0][4]}")
        # First call usually misses the OS cache (slower); later calls are cached.
        time.sleep(0.1)

resolve_with_timing("example.com")
# try 1:  12.30 ms  -> ('93.184.216.34', 443)   (stub -> recursive, maybe cached)
# try 2:   0.11 ms  -> ('93.184.216.34', 443)   (OS/browser cache hit)
# try 3:   0.09 ms  -> ('93.184.216.34', 443)   (cache)
```
```bash
# Walk the tree yourself (iterative) vs asking a resolver (recursive)
$ dig +norecurse www.example.com @a.root-servers.net      # root: referral to .com
$ dig +norecurse www.example.com @a.gtld-servers.net      # .com: referral to example.com NS
$ dig +norecurse www.example.com @a.iana-servers.net      # authoritative: the A record!
$ dig www.example.com                                     # full recursive via /etc/resolv.conf
$ dig +trace example.com                                  # show every referral automatically
```

## 16. Industry Usage
- **Cloudflare 1.1.1.1**: anycast recursive resolver with DoH/DoT, 0x20 randomization, and DNSSEC validation — resolution process at extreme scale (trillions of queries).
- **AWS Route 53**: authoritative service with health-check-based failover — the authoritative half of resolution; also provides a resolver (Route53 Resolver) for hybrid/VPC DNS.
- **Kubernetes/CoreDNS**: cluster-internal resolver; pods query CoreDNS which forwards/iterates for external names — the resolution process scoped to a datacenter.
- **CDNs (Akamai, Cloudflare)**: authoritative DNS + GeoDNS/ECS to route users to edge PoPs — the "resolution as routing" pattern powering ~all web delivery.
- **Enterprises**: split-horizon DNS (internal resolver serves `internal.example.com` with private IPs, external resolves the public zone) — same process, different answers by source.

## 17. References
- RFC 1034/1035 — DNS resolution model: https://www.rfc-editor.org/rfc/rfc1034
- RFC 2308 — Negative Caching: https://www.rfc-editor.org/rfc/rfc2308
- RFC 6891 — EDNS0: https://www.rfc-editor.org/rfc/rfc6891
- RFC 8484 — DNS over HTTPS (DoH): https://www.rfc-editor.org/rfc/rfc8484
- RFC 9156 — QNAME Minimization.
- RFC 7719 — DNS Terminology.
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2.4 (DNS).

## 18. Cheat Sheet
- Recursive resolver = the walker; iterative = referral-following.
- Chain: root → TLD → authoritative → answer (3-4 RTT cold, ~0 warm).
- Referral = NS + glue, no AA; answer = AA bit set.
- TTLs: positive cache, negative cache (SOA minimum), referrals cached too.
- TC bit → retry over TCP. EDNS0 → bigger UDP.
- Stub = libc client; forwarder ≠ recursive resolver.
- GeoDNS/ECS = resolver-based routing (CDNs).
- Cache poisoning defenses: random ports, 0x20, DNSSEC.
- QNAME minimization = privacy.
- Lower TTL before migrations; higher after.

## 19. Quiz
1. A recursive resolver: a) walks the tree for you b) only serves its zone c) is authoritative d) uses only TCP → **a**
2. Referrals come with: a) AA bit b) NS + glue c) answers d) TTL only → **b**
3. The root server gives: a) final IP b) referral to TLD c) AAAA d) MX → **b**
4. Negative caching uses: a) NS TTL b) SOA minimum c) A TTL d) EDNS0 → **b**
5. TC bit means: a) timeout b) truncated → use TCP c) test d) cache → **b**
6. Cache poisoning is best fixed by: a) TCP b) DNSSEC c) shorter TTL d) more resolvers → **b**
7. A stub resolver: a) walks the tree b) forwards to recursive c) is authoritative d) signs zones → **b**
8. GeoDNS routes by: a) client browser b) resolver IP/ECS c) TTL d) port → **b**
9. Cold lookup RTTs: a) 0 b) 1 c) 3-4 d) 10 → **c**
10. ECS lets resolver send: a) full query b) client IP prefix c) password d) TTL → **b**

## 20. Flashcards
- **Q: Recursive vs iterative?** → **A:** Recursive = resolver walks for you; iterative = referral-following by the asker.
- **Q: Resolution chain?** → **A:** root → TLD → authoritative → answer.
- **Q: What's a referral?** → **A:** NS + glue pointer (no AA), not the answer.
- **Q: What is negative caching?** → **A:** Caching NXDOMAIN/NODATA (TTL = SOA minimum).
- **Q: TC bit?** → **A:** Truncated UDP → retry over TCP.
- **Q: How to set up DNS failover?** → **A:** Short TTLs + multiple authoritative NS + health checks.
- **Q: What's a stub resolver?** → **A:** The OS client forwarding to a recursive resolver.

## 21. Revision
Resolution = client → recursive resolver → iterative walk (root → TLD → authoritative via referrals with NS+glue) → answer with AA bit → cache per TTL. Cold = 3-4 RTTs; warm = ~0. Negative caching (SOA minimum) handles typos; TC bit → TCP fallback; EDNS0 enlarges UDP. Stub resolvers forward; forwarders pass upstream. GeoDNS/ECS route by resolver location (CDNs). Poisoning fixed by 0x20/random ports/DNSSEC. Ops rule: drop TTL before migrations. Separate "DNS works" from "connectivity works" when debugging.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Walk me through DNS resolution." | 8 Example / 13 Q&A |
| "Recursive vs iterative?" | 2 How It Works / 13 Q&A |
| "What is a referral?" | 13 Q&A / 7 Formal Definition |
| "Why is the resolver slow on first lookup?" | 8 Example / 10 Time Complexity |
| "How do you debug slow DNS?" | 13 Q&A / 15 Coding |
| "Why don't users see new IPs for an hour?" | 13 Q&A / 9 Internal Working |
| "How does a CDN route via DNS?" | 13 Q&A / 16 Industry Usage |
| "What is negative caching?" | 13 Q&A / 9 Internal Working |
