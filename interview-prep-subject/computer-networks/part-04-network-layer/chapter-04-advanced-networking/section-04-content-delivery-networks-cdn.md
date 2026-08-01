# Content Delivery Networks (CDN)

> **TL;DR**: A **CDN** caches content at **edge PoPs** (points of presence) close to users, so most requests never reach the origin — cutting latency (shorter RTT), offloading the origin, absorbing traffic spikes, and surviving origin failures. Anycast DNS sends users to the nearest PoP; cache hits serve from the edge; TTLs + purges keep content fresh. Cloudflare, Akamai, CloudFront, and Fastly run the web's front line.

## 1. Why Does This Exist?
The web's core latency problem is **physical distance**: a user in Mumbai requesting content from a server in Virginia pays ~200+ ms of round-trip time (RTT) just for the network, multiplied by every object (HTML, CSS, JS, images, video) — plus the *origin server* must serve every request, so it saturates under load. A **CDN** exists to put content *near the user*: a network of **edge PoPs** (thousands of servers in hundreds of cities) caches and serves content, so a request travels to the *nearest* PoP (a few ms) instead of halfway around the world. The payoffs: **latency** (cache hit = edge RTT, not origin RTT), **origin offload** (hits never touch the origin — 90–99% offload is typical), **scale/resilience** (PoPs absorb viral spikes and DDoS — the CDN eats traffic your origin couldn't), **availability** (if the origin fails, cached content still serves), and **economics** (less origin bandwidth/CPU). CDNs exist because distance, physics, and traffic spikes are unavoidable — caching near the user is the cheapest, most effective fix.

## 2. How Does It Work?
- **Anycast + DNS**: the CDN announces the same IPs from many PoPs (anycast → BGP routes each client to the *nearest* PoP), or uses DNS-based **GSLB** (authoritative DNS returns the best PoP IP by geo/latency/health). Users always end up at a *nearby* edge.
- **Edge servers** cache copies of content; a request is: **cache hit** → serve from the edge (fast, no origin); **cache miss** → **forward/originate** from the origin, cache a copy for next time.
- **TTLs**: the origin's `Cache-Control: max-age` (and `Expires`) tells the CDN how long a copy is valid. Within TTL: serve from cache (no revalidation). After TTL: **revalidate** with `If-Modified-Since`/`ETag` (origin says "304 Not Modified" → serve cached copy, refresh TTL) or re-fetch (origin changed → cache new copy).
- **Cache key**: the URL (plus `Vary` headers like Accept-Encoding/Accept-Language — different variants get different cache entries). Everything else (cookies, user identity) usually must be *excluded* from the key to keep content shared.
- **Dynamic vs static**: static content (images, CSS, JS, video, fonts) caches great; dynamic (per-user pages, APIs) needs smarter handling — edge *computing* (Cloudflare Workers, Lambda@Edge) or query-string-aware caching.
- **Purge/invalidation**: a content change must remove the old cached copy: **purge** (explicit invalidation of a URL/path) or **versioning** (cache-busting: add `?v=2` to URLs so new content is a new key — the recommended approach).
- **Additional edge services** bundled with CDNs: **DDoS protection** (absorb at the edge), **TLS** (edge terminates HTTPS, `Origin Server` gets the request from the CDN), **image optimization** (resize/format at the edge), **WAF** (filter at the edge), **compression** (Brotli/gzip), and **edge compute** (run logic at the PoP).

## 3. When Is It Used?
- **Static assets for every website**: CSS/JS/images/fonts served from the CDN — even a blog uses a CDN (WordPress/Cloudflare/JSdelivr). The default web architecture.
- **Video streaming (Netflix, YouTube, Hulu)**: CDNs + edge caches deliver the world's largest traffic volumes; Netflix's Open Connect appliances live *inside* ISPs. Video *is* the CDN's biggest job.
- **Software/OS downloads (npm, Maven, Docker Hub, Windows/macOS updates)**: mirrored/anycast CDNs distribute terabytes of binaries to the closest node.
- **SaaS/API acceleration**: edge caches for APIs, edge workers for geo-specific logic, and origin shields (a single caching layer in front of the origin).
- **Global multi-region apps**: CDNs provide the "served from nearest" experience *without* running servers in every region — the pragmatic route to global performance.
- **Live events/launches**: CDNs absorb the spike — the origin never sees the viral burst (this is *why* product launches "don't crash").
- **DDoS mitigation**: put the site on a CDN → traffic hits edge capacity (multi-Tbps), not your origin — the standard defense.

## 4. Why Wasn't Another Approach Chosen?
- **Why not just scale the origin (bigger servers / more regions)?** You can't buy your way past physics: 200 ms RTT to one region is unavoidable no matter how big the server is. CDNs *move the content closer to the user* (few ms) — the only real fix for distance. And a scaled origin still sees every request; a CDN offloads 90%+ of them (huge cost savings vs "buy more origin").
- **Why not just buy servers in every country?** You'd need thousands of locations, anycast/DNS routing, capacity planning, and global ops — that *is* what a CDN is, built once and shared. Individual sites can't justify the economics; a CDN amortizes edge infrastructure across millions of customers.
- **Why caching, not precomputing everything?** Some content is dynamic; caching handles the *repeated* 90% and forwards the novel 10% — the right cost/perf balance. Edge compute (workers) then makes even dynamic content cheap and close.
- **Why anycast over just DNS with geo?** DNS geo is coarse (resolver-based, not user-based) and cache-poisonable; anycast lets *routing* (BGP) choose the nearest — plus it absorbs DDoS (traffic spreads across all PoPs). Modern CDNs use anycast as the base and DNS/geo as fine-tuning.
- **Why HTTP-level caching, not a new protocol?** HTTP caching (`Cache-Control`, ETags, 304s) is standardized, works with every origin, and is nearly free — building a proprietary transfer protocol would fight the entire web stack. CDNs *extend* HTTP (TLS at edge, HTTP/2/3) rather than replace it.

## 5. Intuition
A CDN is a **city-wide chain of bookstores with a single warehouse**. Instead of every customer traveling to the central warehouse (origin) in another city (200 ms of travel), each neighborhood gets a bookstore (edge PoP) that keeps copies of the *popular books* (cached content) on its shelves. A customer walks in, finds the book → served instantly (cache hit, milliseconds). If the store doesn't have it, it phones the warehouse, gets a copy, hands it over — and puts the copy on the shelf for the next customer (cache miss → fetch + cache). The bookstore checks its shelf-life sticker (TTL): books within their "good until" date are sold as-is; past it, the store calls the warehouse "has this book changed?" and gets a "no, it's the same" (304) — so it keeps selling and refreshes the date. When the publisher revises a book (new version), they don't recall all copies — they just change the title (`v2`) so old editions die naturally (cache-busting). And when a hurricane of demand hits (viral spike), the *bookstores* absorb it — customers never even reach the warehouse (origin offload + DDoS absorption).

## 6. Real-World Analogy
**Supermarket distribution with local franchises**: A national chain's products are made at a central factory (the origin). Instead of shipping every single item from the factory to each customer (200 ms, warehouse overloaded), the chain opens *local warehouses* (edge PoPs) in every city. Customers shop at the local warehouse — most needs are met from the local shelf (cache hit, milliseconds); when the local warehouse is missing something, it orders from the factory, serves the customer, and restocks the shelf (miss → fetch + cache). Each product has a **sell-by date** (TTL): within date → sold directly; expired → the local warehouse calls the factory "is the recipe still the same?" (revalidation) — a "yes, same" reply (304) means it's re-stickered and sold again. When the factory launches a new product version, it changes the *label* (`v2`) rather than recalling old stock — old-labeled items simply age out (cache-busting). When a promotion goes viral, the *local warehouses* absorb the crowd (offload + DDoS), and the factory (origin) keeps humming — and customers in the next city over get served by *their* local warehouse in milliseconds, never touching the factory at all.

## 7. Formal Definition
A **CDN** is a globally distributed system of edge servers (PoPs) that serves content from caches near the user. **Ingress**: DNS-based GSLB (authoritative DNS selects best PoP by geo/latency/health) and/or **anycast** (same IP from many PoPs → BGP routes to nearest). **Caching model**: HTTP caching via `Cache-Control: max-age`, `ETag`, `Last-Modified`, `Expires`; hit (serve from edge) vs miss (fetch from origin, cache) vs revalidate (`If-None-Match`/`If-Modified-Since` → 304 Not Modified). **Cache key**: URL + `Vary` headers. **Invalidation**: explicit **purge** (URL/path/pattern) or **cache-busting** (versioned URLs). **Origin shield**: an extra caching tier directly in front of the origin. **Edge compute**: Workers/Lambda@Edge run logic at PoPs. **Related services**: TLS termination, DDoS/WAF, compression, image optimization, HTTP/2–3. Popular: Cloudflare, Akamai, CloudFront (AWS), Fastly, Cloud CDN (GCP), Netflix Open Connect.

## 8. Example
A cache flow (recreate the decision tree):
```
GET https://cdn.example.com/img/logo.png  (from Mumbai; anycast → Mumbai PoP)

PoP cache: miss → fetch from origin (US):
  1. PoP → origin:  GET /img/logo.png
  2. origin:  200 OK  +  Cache-Control: public, max-age=86400  +  ETag: "abc123"
  3. PoP stores logo.png keyed on URL, with TTL 86400s
  4. PoP → user:  200 OK  (Mumbai RTT ≈ 20 ms, not 200 ms)

5 min later, another Mumbai user:
  PoP cache: HIT → serve locally, 200 OK, from cache (0 origin traffic)

Next day, TTL expired → revalidate:
  PoP → origin:  If-None-Match: "abc123"
  origin: 304 Not Modified (unchanged) → PoP keeps copy, refreshes TTL
  PoP → user: 200 OK (served from cache; only a tiny conditional request hit origin)

Image updated → versioned URL: /img/logo.png?v=2
  New key → miss → fetch fresh; v=1 ages out via TTL.   (purge not needed)
```
The *keys*: hit/miss/304 + TTL. The *point*: only 1 of the 3 requests touched the origin.

## 9. Internal Working
1. **Anycast routing**: the CDN announces its edge IP blocks from all PoPs; BGP best-path sends each client to the nearest announcing PoP (minimizing RTT). DNS GSLB adds geo/health/latency fine-tuning and the mapping to the right edge IP.
2. **Cache lookup**: on each request, the PoP computes the cache key (URL + normalized headers per `Vary`), hashes it, and looks up its local cache (RAM, then SSD, then "disk") — misses forward upstream.
3. **Forwarding/originate**: a miss goes to the origin (directly, or via the **origin shield** tier which consolidates misses into one connection — the "funnel" that protects the origin from cache-stampede on a cold miss).
4. **Response handling**: the PoP parses `Cache-Control` to decide cacheability (public/private, max-age, no-store), stores with the correct TTL, serves the user, and *learns* to fetch-ahead (prefetch) or serve-stale-during-revalidation (`stale-while-revalidate`) for resilience.
5. **TTL/revalidation**: on expiry, conditional GET (`If-None-Match`/`If-Modified-Since`); 304 → refresh TTL, keep serving; 200 → replace, serve new.
6. **Invalidation/purge**: a console/API call flushes specific keys across all PoPs (propagated via the CDN's control plane, eventually consistent); cache-busting URLs are the zero-purge alternative.
7. **Edge compute**: Workers/Lambda@Edge intercept at the PoP — routing, A/B tests, geo logic, response transformation — before the cache, giving app logic the same "near the user" benefit.
8. **Observability/ops**: cache hit ratio (hit ÷ total), offload %, TTL-tuning, purge logs, and PoP-level metrics are the CDN's health dashboard — the "hit ratio" is the single number every CDN engineer watches.

## 10. Time Complexity
- **Cache lookup**: O(1) — hash on URL/Vary-key; the PoP serves millions of req/s across RAM/SSD tiers at hardware speed.
- **Hit vs miss latency**: hit = edge RTT (single digit ms); miss = edge RTT + origin RTT (100–300 ms, regional) — *an order of magnitude* difference, which is the entire CDN value proposition.
- **Revalidation**: only a tiny conditional request (304) touches the origin — ~1 KB vs a full content transfer; amortized per TTL window, so origin load is ~1/(hits per TTL) of naive serving.
- **Purge propagation**: O(PoPs), eventually consistent (seconds) — a global purge hits thousands of PoPs; versioned URLs avoid it entirely.
- **The scale reality**: CDNs move *terabytes per second*; the "time complexity" that matters is **offload %** (cache hit ratio) — a 95%+ hit ratio means the origin sees 1/20th of the traffic.

## 11. Advantages
- **Latency**: content served from the nearest PoP — single-digit ms RTT instead of cross-continental 200 ms (the *only* real fix for distance).
- **Origin offload**: 90%+ of requests never reach the origin → cheaper, smaller origin infrastructure.
- **Scale & resilience**: PoPs absorb viral spikes and DDoS (multi-Tbps edge capacity); origin stays calm behind them.
- **Availability**: cached content serves even when the origin is down/overloaded (stale-while-revalidate adds a safety net).
- **Global experience without global ops**: serve every region's users fast without running servers there.
- **Bundled services**: TLS, WAF, compression, image optimization, edge compute — the CDN edge becomes a full application platform.

## 12. Disadvantages
- **Staleness**: TTL-window caching serves slightly-old content after updates (fixed by purge/versioning — but that's ops complexity).
- **Cache invalidation is hard**: purges propagate eventually; mis-set `Cache-Control` causes the classic "why is my new deploy still showing old JS?" — cache-busting is mandatory discipline.
- **Dynamic content isn't cacheable**: per-user/API data bypasses the cache → the CDN becomes a pass-through (still useful for TLS/DDoS, but no offload). Edge compute mitigates but adds complexity.
- **Cookie/Vary cache-key pitfalls**: user-specific cookies in the key destroy hit ratio (every user = own entry); too-aggressive caching of personalized pages leaks data (privacy bug).
- **Trust & cost**: the CDN now terminates your TLS (a third party with your traffic), and you pay per GB — CDN economics favor high-hit-ratio static workloads.
- **Complexity of the edge**: purge, TTL tuning, edge-compute logic, and multi-CDN setups add a whole operations layer.

## 13. Interview Questions
1. **Q: What is a CDN and why is it needed?** A: A network of edge PoPs that caches and serves content near users — fixing physical distance (latency), offloading the origin, absorbing spikes/DDoS, and surviving origin failures.
2. **Q (tricky): Cache hit vs miss — walk through the flow.** A: Hit = PoP serves from its cache (edge RTT, ms). Miss = PoP forwards to the origin, caches a copy with the TTL from `Cache-Control`, serves the user. Revalidate = TTL expired → conditional GET (`If-None-Match`/`If-Modified-Since`) → 304 → keep + refresh TTL.
3. **Q: How does a user reach the nearest PoP?** A: Anycast (the same IP announced from many PoPs → BGP routes to the nearest) and/or DNS GSLB (authoritative DNS returns the best PoP IP by geo/latency/health). Both push the user to a nearby edge.
4. **Q (FAANG): What is cache invalidation and how do you do it safely?** A: Removing the stale cached copy after content changes: explicit **purge** (URL/path — propagated to all PoPs, eventually consistent) or **cache-busting** (versioned URLs `?v=2` — new key, old one ages out via TTL). Versioning is the recommended approach (no global purge needed, atomic per-URL).
5. **Q: What is the cache key and what breaks it?** A: The URL + `Vary` headers (Accept-Encoding, Accept-Language). User-specific cookies/headers in the key destroy the hit ratio (each user becomes a unique entry) — the classic "CDN stopped caching" bug.
6. **Q (tricky): How do you cache dynamic, per-user content?** A: You mostly don't at the pure-CDN layer — use short TTLs, `private`/`no-store`, or edge compute (Workers/Lambda@Edge) to personalize *at the edge* while caching the shared parts (e.g., cached HTML shell + personalized fragments).
7. **Q: What does `Cache-Control: max-age` do vs `ETag`?** A: `max-age` = how long the CDN/browser can serve from cache *without asking* (TTL). `ETag` = a content fingerprint for *revalidation* after the TTL expires (304 vs 200). Both together = the standard freshness model.
8. **Q (FAANG): "Your product launches and the site should not crash. How?"** A: Behind a CDN: the spike hits the edge (which absorbs and caches), the origin sees only cache misses; pre-warm the cache, set sane TTLs, use an origin shield, and let stale-while-revalidate carry the origin if it falters. The CDN *is* the launch strategy.
9. **Q: What is an origin shield?** A: An extra caching tier directly in front of the origin that consolidates many PoP misses into fewer origin requests — protecting the origin from a cache-stampede when a cold object goes viral.
10. **Q (tricky): Why is `stale-while-revalidate` useful?** A: Serve the stale cached copy *immediately* while revalidating in the background — users get near-zero latency even when the origin is slow/down; availability without sacrificing freshness.
11. **Q: CDN vs DNS round-robin / GSLB?** A: GSLB is *part* of the CDN's ingress (DNS chooses the best PoP by health/geo); the CDN itself is the caching + serving layer. A DNS-only setup has no edge caches — it just spreads load across *origins*. CDN = routing *and* caching.
12. **Q (FAANG): "Design a CDN for a video platform."** A: Anycast/GSLB ingress → edge PoPs with large SSD/Tiered caches → origin shield → storage origin; segment-based caching (small chunks, long TTLs), HTTP/2–3 + adaptive bitrate, predictive prefetch for popular content, and a strong purge/versioning story for edits. The point: cache *near* users, make misses cheap, absorb spikes at the edge.
13. **Q: What are the main CDN metrics?** A: Cache hit ratio (the big one), offload %, edge latency (p50/p99), origin requests, purge propagation time, byte throughput. A dropping hit ratio → cache-key bug or TTL misconfig.
14. **Q (tricky): CDN and DDoS — why does it work?** A: Traffic goes to the edge (anycast spreads it across all PoPs — multi-Tbps capacity, distributed across the planet). The origin never sees it; edge WAF/rate-limiters drop the garbage. The attack exhausts *the CDN's* resources, not yours.
15. **Q: What happens to TLS with a CDN?** A: The CDN terminates TLS at the edge (client → CDN, HTTPS); the CDN→origin leg is separate (usually HTTPS via a shared/full cert). This means the CDN can inspect/route/modify requests — the *trust* tradeoff of putting your site on a CDN.

## 14. Follow-Up Questions
1. **Q: Browser caching vs CDN caching?** A: Both use HTTP caching headers, but the browser cache serves *that user's* device (max-age ~ short, per-user) while the CDN cache serves *all users* at a shared PoP. CDNs send longer TTLs to the browser (`max-age`) and shorter ones to themselves (`s-maxage` — the "shared cache" directive).
2. **Q (production): "We deployed a new frontend but users still see the old version." Diagnose?** A: (1) Browser/CDN cache on an unchanged URL — the #1 cause: you didn't cache-bust; fix by versioning the bundle (`app.abc123.js`). (2) TTL too long — shorten or purge. (3) Verify the CDN is actually being bypassed (hard-refresh, incognito). (4) Check that the origin returns the new `Cache-Control`. The discipline: *versioned URLs + short TTLs + explicit purge*.
3. **Q: What is a "cache stampede/thundering herd"?** A: When a cold/missed object suddenly gets massive demand (or a TTL expires all at once), *every* PoP misses simultaneously and floods the origin — the origin falls over. Mitigations: origin shield, request coalescing (single in-flight fetch), randomized TTLs (jitter), stale-while-revalidate.
4. **Q (tricky): Private vs public caching, and `s-maxage`?** A: `public` = shareable (CDN + browser); `private` = only the user's browser (sessions, personalized); `s-maxage` = TTL for *shared* caches (CDN) overriding the browser TTL — the precise knob for "cache it at the CDN for 60s, at the browser for 0s."
5. **Q: When would you NOT put something on a CDN?** A: Highly sensitive per-user data (unless `private`/no-store + edge compute), ultra-dynamic real-time feeds (WebSockets — though edge handles those too), and legally restricted content where location matters. CDNs are great for *shared, time-tolerant* content.

## 15. Coding Example
```python
# A miniature CDN cache: hit / miss / revalidate / versioning
from datetime import datetime, timedelta

class EdgeCache:
    def __init__(self):
        self.cache = {}                     # key -> (body, etag, expires)

    def serve(self, url, origin):
        entry = self.cache.get(url)
        if entry and entry[2] > datetime.now():
            return "HIT", entry[0]          # within TTL: serve from cache
        body, etag = origin.get(url)        # miss or expired
        if entry and entry[1] == etag:
            self.cache[url] = (body, etag, datetime.now() + timedelta(seconds=60))
            return "REVALIDATE 304", entry[0]
        self.cache[url] = (body, etag, datetime.now() + timedelta(seconds=60))
        return "MISS -> fetched", body

class Origin:
    def __init__(self): self.calls = 0
    def get(self, url):
        self.calls += 1
        return f"<content for {url}>", f"etag-{url}"

o = Origin(); c = EdgeCache()
print(c.serve("/img/logo.png", o))          # MISS -> fetched (origin hit #1)
print(c.serve("/img/logo.png", o))          # HIT (origin untouched)
print(c.serve("/img/logo.png?v=2", o))      # MISS -> fetched (versioning = new key)
print("origin calls:", o.calls)             # 2 — the CDN ate the rest
```
```bash
# The CDN toolbox
$ curl -sI https://cdn.example.com/img/logo.png
#   Cache-Control: max-age=86400   ← TTL
#   age: 120                       ← seconds since cached at the edge
#   x-cache: HIT                   ← hit vs MISS vs MISS_STALE
$ curl -s -H 'If-None-Match: "abc123"' -o /dev/null -w '%{http_code}\n' \
    https://cdn.example.com/img/logo.png        # 304 = revalidated from cache
$ dig +short api.example.com                     # which PoP does DNS pick? (geo/anycast)
```

## 16. Industry Usage
- **The web's default layer**: nearly every site (WordPress, e-commerce, blogs) sits behind Cloudflare/CloudFront/Fastly for static assets + TLS + WAF. The CDN is the Internet's front door.
- **Streaming (Netflix, YouTube, Hulu)**: Open Connect (Netflix) puts appliances *inside ISPs*; YouTube uses Google's global edge — the largest CDN workloads on Earth. Video *defines* the CDN.
- **Package/mirror distribution (npm, Maven, PyPI, Docker Hub, Windows Update)**: anycast CDNs + mirrors serve multi-TB releases to the nearest node — the reason downloads are fast everywhere.
- **SaaS/API acceleration**: Fastly/Cloudflare serve APIs at the edge, run Workers for per-region logic, and use origin shields to protect backends — "global without servers everywhere."
- **DDoS defense**: every major attack is mitigated *at the edge* (Cloudflare, Akamai Prolexic, AWS Shield) — "put your site on a CDN" is the first line of security advice.
- **E-commerce/launches**: Black Friday, ticket drops, product launches route through CDNs that pre-warm + absorb — the launch "doesn't crash" because the edge took the hit.

## 17. References
- Kurose & Ross, *Computer Networking*, Ch. 2 §2.2.5 (CDN/HTTP caching), Ch. 7 (streaming/CDNs).
- RFC 7234 — HTTP Caching (Cache-Control, ETag, 304): https://www.rfc-editor.org/rfc/rfc7234
- RFC 9111 — HTTP caching (current): https://www.rfc-editor.org/rfc/rfc9111
- Cloudflare CDN/Workers docs: https://developers.cloudflare.com/
- Fastly caching docs: https://docs.fastly.com/
- Netflix Open Connect: https://openconnect.netflix.com/
- MDN HTTP caching: https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching

## 18. Cheat Sheet
- CDN = edge PoPs that cache content near users → latency + offload + spike absorption.
- Ingress: anycast (same IP, many PoPs, BGP nearest) + DNS GSLB (geo/health).
- Cache flow: HIT (edge) / MISS (fetch+cache) / 304 (revalidate, keep serving).
- Freshness: `Cache-Control: max-age`, `s-maxage` (shared TTL), `ETag`/`Last-Modified`.
- Cache key: URL + `Vary`; exclude user cookies or hit ratio dies.
- Invalidation: purge (eventually consistent) or versioned URLs (`?v=2`) — the standard.
- Origin shield = funnel PoP misses into one tier → protect origin from stampedes.
- stale-while-revalidate = serve stale now, refresh in background (availability).
- Metrics: cache hit ratio, offload %, origin req, edge latency.
- Edge compute: Workers/Lambda@Edge — logic near the user.
- TLS terminates at the edge (trust tradeoff). DDoS absorbed at the edge.
- Debug: `curl -sI` (Cache-Control/age/x-cache), 304s, `dig`.

## 19. Quiz
1. A cache hit serves from: a) origin b) edge PoP c) DNS d) DB → **b**
2. A 304 means: a) content changed b) not modified, keep cached c) error d) purge → **b**
3. `max-age=86400` sets: a) purge time b) TTL in seconds c) hit ratio d) key → **b**
4. Cache-busting = a) purge all b) versioned URLs c) longer TTL d) no-store → **b**
5. Anycast sends users to: a) origin b) nearest PoP c) DNS d) LB → **b**
6. `s-maxage` applies to: a) browser only b) shared caches (CDN) c) DNS d) TLS → **b**
7. Origin shield protects the origin from: a) DDoS only b) cache stampede c) DNS d) TLS → **b**
8. Hit ratio is: a) hits/total b) misses/total c) TTL d) purge count → **a**
9. The #1 cause of "users see old version": a) no cache-busting b) DNS c) TLS d) anycast → **a**
10. CDN handles DDoS because: a) encryption b) edge absorbs/anycast spread c) WAF only d) origin → **b**

## 20. Flashcards
- **Q: Why CDN?** → **A:** fix distance latency, offload origin, absorb spikes/DDoS.
- **Q: Hit / miss / 304?** → **A:** edge serve / origin fetch+cache / revalidate-keep.
- **Q: TTL + ETag?** → **A:** freshness window + fingerprint for revalidation.
- **Q: Invalidation?** → **A:** purge or versioned URLs (`?v=2`) — versioning is safer.
- **Q: Anycast / GSLB?** → **A:** BGP-nearest PoP / DNS geo-health choice.
- **Q: Cache key?** → **A:** URL + Vary; exclude user identity or hit ratio dies.
- **Q: Origin shield?** → **A:** funnel misses → protect origin from stampede.
- **Q: stale-while-revalidate?** → **A:** serve stale now, refresh later (availability).
- **Q: Key metric?** → **A:** cache hit ratio / offload %.

## 21. Revision
CDN = edge PoPs caching content near users. Ingress via anycast (same IP many PoPs → BGP nearest) + DNS GSLB (geo/health). Flow: HIT (serve edge), MISS (fetch origin + cache with TTL from `Cache-Control`), 304 (revalidate → keep). Cache key = URL + `Vary`; user cookies in the key kill hit ratio. Freshness: `max-age`, `s-maxage` (shared/CDN TTL), ETag/If-None-Match. Invalidation: purge (eventually consistent) vs versioned URLs (`?v=2`, the recommended zero-purge path). Origin shield funnels misses → protects against stampedes; stale-while-revalidate gives availability during slow/failed origins. Edge compute (Workers/Lambda@Edge) personalizes at the edge. Metrics: hit ratio, offload %, edge latency. TLS terminates at the edge (trust tradeoff). Used: static assets everywhere, streaming (Open Connect), package mirrors, API acceleration, DDoS defense, launches. Debug: `curl -sI` (`Cache-Control`, `age`, `x-cache`), 304s, `dig`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a CDN / why is it needed?" | 2 How It Works / 5 Intuition |
| "Hit vs miss vs revalidate?" | 13 Q&A / 8 Example |
| "How does a user reach the nearest PoP?" | 13 Q&A / 9 Internal Working |
| "Cache invalidation / cache-busting?" | 13 Q&A / 9 Internal Working |
| "Cache key / Vary / cookie pitfalls?" | 13 Q&A / 12 Disadvantages |
| "Caching dynamic content?" | 13 Q&A / 14 Follow-Up |
| "Launch resilience / DDoS?" | 13 Q&A / 16 Industry Usage |
| "Design a video CDN?" | 13 Q&A / 10 Time Complexity |
| "Why do users see old content?" | 13 Q&A / 14 Follow-Up |
| "Metrics / hit ratio?" | 13 Q&A / 9 Internal Working |
