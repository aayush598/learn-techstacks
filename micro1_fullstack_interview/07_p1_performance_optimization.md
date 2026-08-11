# Priority 1 — Performance & Optimization (Q243–Q265)

**Why these matter for micro1:** the role explicitly says "concurrency patterns and backend optimizations," "scalability and performance." Expect: find-the-bottleneck questions, caching, pagination, batching, and scale ("100k rows", "10k concurrent requests", "LLM latency").

**Golden method (say this every time):** measure → identify the bottleneck → fix the biggest cost → re-measure. Never optimize blind.

---

## Q243: How would you optimize a slow API?

**Systematic process:**
1. **Measure:** latency percentiles (p50/p95/p99), throughput, error rate. Reproduce with realistic load.
2. **Profile the request path** — which stage dominates?
   - Network/DB round-trips vs CPU vs I/O (traces, APM).
   - **Slowest call first:** DB query (EXPLAIN), external API (timeout/retry/cache), LLM call (largest cost often).
3. **Apply targeted fixes:**
   - **DB:** index the hot queries, N+1 fix, pagination, connection pool sizing (Q244, Q245).
   - **External calls:** parallelize with `asyncio.gather`, bound concurrency, cache, timeout (Q120).
   - **Payload:** response models (strip fields), compression, pagination.
   - **Caching:** Redis for hot/repeatable data (Q248–253).
   - **Code:** profiling CPU hotspots, algorithmic fixes, async where blocked (Q244).
4. **Re-measure** — prove the improvement; watch p95 and error rate.

---

## Q244: How would you identify the bottleneck in a backend application?

1. **APM/tracing** (Datadog/New Relic/open-telemetry): per-request breakdown of time — DB, HTTP, code, queue.
2. **Profiling:**
   - CPU: `cProfile`/`py-spy` (attaches to a running process without restart — safe in prod).
   - Memory: `memory_profiler`, tracemalloc.
   - I/O wait: `py-spy dump`, async traces.
3. **DB:** `pg_stat_statements` (most expensive queries), slow-query log, `EXPLAIN ANALYZE` (Q169).
4. **Metrics:** request latency, DB connection pool saturation, CPU, GC pauses, event-loop blocking time.
5. **Load test** to see where it breaks (Latency/throughput curve) — k6, locust.
6. **Rule out the obvious:** no concurrency (blocking I/O in async), N+1, missing indexes, unbounded fan-out.

**Outcome:** a ranked list of costs, then optimize the top item.

---

## Q245: How would you optimize a slow database query?

1. **Get the plan:** `EXPLAIN (ANALYZE, BUFFERS)` — find Seq Scans, sorts, row-estimate mismatches (Q169).
2. **Indexes:** add for filtered/joined/ordered columns; composite index order (equality → range) (Q163–165).
3. **`ANALYZE`** if statistics are stale (est. rows ≠ actual rows).
4. **Rewrite:**
   - Remove functions on columns in `WHERE`.
   - `OR`/`IN` → proper index usage (maybe `UNION ALL`).
   - `LIKE '%x%'` → trigram index (`pg_trgm`).
   - Correlated subqueries → joins/CTEs.
   - Avoid `SELECT *`; fetch only needed columns.
5. **Reduce work:** pagination (keyset), push filters down, aggregation in DB not in app.
6. **Scale the data access:** read replicas for reports, partitioning for huge tables, materialized views for heavy aggregates.
7. **Concurrency:** connection pool sizing, avoid locks/bloat (VACUUM), `statement_timeout`.
8. **Measure again** — compare before/after times and plans.

---

## Q246: How would you optimize a React application?

1. **Measure first:** React DevTools Profiler, Lighthouse, bundle analyzer.
2. **Bundle size:** code splitting by route (`React.lazy`/dynamic `import`), tree-shaking, analyze chunks (Q259).
3. **Re-renders:** `React.memo` + `useCallback`/`useMemo` for hot lists; split state; stable keys (Q208–209).
4. **Long lists:** virtualization (react-window) — render only visible rows (Q260–261).
5. **Network:** React Query caching, debounce search inputs, pagination, server-side filtering.
6. **Rendering:** avoid expensive renders in lists; images lazy; `content-visibility`; CSS containment.
7. **Perceived performance:** skeletons, optimistic UI (Q580), streaming SSR (Next.js).
8. **Web Vitals:** LCP (lazy images, preload critical), INP (avoid heavy JS on input), CLS (stable layout).

---

## Q247: How would you reduce API response time?

1. **Optimize the slowest hop** (profile it — Q244): DB query, external API, LLM, serialization.
2. **Parallelize independent work:** `asyncio.gather` external calls + DB (Q120).
3. **Cache** repeatable results (Redis) — skip the expensive work (Q248).
4. **Trim payload:** response models, compression (gzip/brotli), pagination.
5. **Edge/global:** CDN for static + cached responses; deploy closer to users.
6. **Stream** instead of waiting for everything: SSE/WebSocket for incremental data (LLM streaming).
7. **Async processing:** move slow work (reports, resumes) to background queues; return 202 + poll.
8. **Connection reuse/pooling**, keep-alive, HTTP/2.
9. **DB:** indexes, connection pool, read replicas (Q245).

---

## Q248: What is caching?

Storing the result of an expensive operation **so repeat requests skip recomputation** — trading consistency for speed.

```python
# cache-aside: check cache → miss → compute → store with TTL
data = redis.get(key)
if data is None:
    data = expensive_query()
    redis.set(key, data, ex=ttl)
return data
```

- Layers: client (browser), CDN, reverse proxy (nginx), app (in-process/Redis), DB (query cache/buffers), HTTP (headers `Cache-Control`).
- **Cache-aside**, **write-through**, **write-behind**, and **read-through** are the main strategies.
- Costs: stale data, invalidation complexity, memory.

---

## Q249: Where can caching be implemented?

1. **Browser/HTTP layer** — `Cache-Control`, `ETag`, service workers (static assets, GET responses).
2. **CDN** — static files, images, rendered pages (CloudFront/Cloudflare).
3. **Reverse proxy** — nginx caching layer in front of the API.
4. **Application layer** — in-process (dict, `functools.lru_cache`) or **Redis** (shared, TTL, distributed).
5. **Database layer** — PostgreSQL shared buffers, query result caches, materialized views.
6. **Compute layer** — GPU/model response caching for LLMs (semantic caches, Q678).
7. **Client state** — React Query caches API data in memory.

Each layer answers different scale points; combine them (CDN for static, Redis for API, app for in-memory hot data).

---

## Q250: What is Redis?

An **in-memory data store** — key/value, single-threaded, sub-millisecond latency. Often described as "a data structure server."

- Data types: strings, lists, sets, sorted sets, hashes, streams, bitmaps.
- Features: **TTL/expiry**, pub/sub, Lua scripting, transactions, **streams** (message queue), **persistence** (RDB snapshots / AOF append-only).
- Typical uses: **cache**, sessions, rate limiting (INCR/EXPIRE), leaderboards (sorted sets), distributed locks (`SET NX PX`), job queues (streams/BRPOPLPUSH), real-time counters, feature flags.

---

## Q251: When would you use Redis?

1. **Cache** for hot, repeatable reads (profiles, configs, LLM responses, API responses) with TTL.
2. **Session store** — shared across server instances (vs sticky sessions).
3. **Rate limiting / token buckets** — `INCR` + `EXPIRE` atomicity.
4. **Distributed locks** — cross-instance mutual exclusion (`SET key val NX PX`).
5. **Leaderboards / ranking** — sorted sets (`ZADD`, `ZRANGE`).
6. **Counters** — analytics, page views.
7. **Message queue / pub-sub** — light-weight task fan-out (Redis Streams with consumer groups).
8. **Caching expensive computations** — DB aggregates, LLM responses.

Use PostgreSQL for durable relational truth; Redis for fast volatile data with TTL.

---

## Q252: What is cache invalidation?

The mechanism that **removes/updates cached data when the source changes** so users don't see stale values.

Strategies:
1. **TTL (expiry)** — simplest; data auto-invalidates after N seconds (Q253). Risk: staleness window.
2. **Write-through** — update cache on every write (always fresh; more write cost).
3. **Invalidation on write (cache-aside)** — on DB update, `DELETE` the cache key; next read repopulates. Also bump a **version key** (invalidate groups).
4. **Event-based** — DB triggers/CDC or app events fan out to clear relevant keys.
5. **ETag/Last-Modified** — HTTP-level conditional requests.

**Tradeoff:** consistency vs complexity/latency. Choose per data type (session: TTL; user profile: write-through; LLM answer: long TTL).

---

## Q253: What is TTL?

**Time To Live** — how long a cached value lives before automatic expiry.

```python
redis.set(key, value, ex=3600)   # expires after 1 hour
```

- Set per-key; Redis purges lazily + periodically.
- Tuning: short TTL (seconds) for volatile data (rate counters, streaming), longer (minutes/hours) for stable data (config, reference data, LLM answers).
- TTL is the **default invalidation strategy** — it bounds staleness and memory growth without explicit invalidation logic.

---

## Q254: What is connection pooling?

See Q108–110, Q172. In context of performance: pools reuse connections (TCP/TLS/DB handshakes) across requests, cap concurrent connections to the DB/external service, and prevent "too many connections" failures. Size `pool ≈ workers × concurrency`; add `pool_pre_ping`/recycle for health. External poolers (PgBouncer) for massive concurrency.

---

## Q255: What is batching?

Grouping many small operations into **fewer large ones** to cut per-operation overhead.

- **DB:** `INSERT` multiple rows at once; `WHERE id IN (...)` instead of per-id queries (fixes N+1).
- **External APIs:** provider batch endpoints (e.g., OpenAI batch API — 50% discount).
- **Frontend:** debounce/throttle rapid events (search, scroll, resize).
- **I/O:** bulk network writes, micro-batching for analytics ingestion (collect N events / flush every T seconds).

Example:
```sql
-- instead of 100 single inserts
INSERT INTO scores (user_id, score) VALUES (1, 90), (2, 85), ...;
```

---

## Q256: What is pagination?

Splitting a large result set into **pages** so each request returns a bounded slice.

- **Offset pagination:** `LIMIT n OFFSET m` — simple; slow at high offsets (skips scanned rows); unstable if data changes between pages (dupes/misses).
- **Cursor (keyset) pagination:** `WHERE id > last_id ORDER BY id LIMIT n` — O(page) cost, stable under inserts; needs an index; ideal for large/infinite lists (Q257, Q390).

```sql
-- offset
SELECT * FROM users ORDER BY id LIMIT 50 OFFSET 100;
-- cursor
SELECT * FROM users WHERE id > 100 ORDER BY id LIMIT 50;
```

- Envelope: `{items, next_cursor, has_more}` or `{items, page, total}`.
- Always paginate large lists; never `SELECT *` unbounded.

---

## Q257: Offset pagination vs cursor pagination?

| | **Offset** | **Cursor (keyset)** |
|---|---|---|
| Mechanics | `LIMIT n OFFSET m` | `WHERE key > last_key ORDER BY key LIMIT n` |
| Cost | O(offset) — grows with page number | O(page size) — constant per page |
| Stability | Skips/duplicates if data changes | Stable under inserts/deletes (only forward) |
| Random access | Yes (jump to page 5) | No (must walk) |
| Total count | Easy | Extra query if needed |
| Best for | Small tables, admin tables | Large tables, feeds, chat history |

**Recommendation:** cursor for production scale (chat history, feeds); offset for small/admin UIs. Many APIs offer both.

---

## Q258: What is lazy loading?

**Deferring** the loading of a resource until it's actually needed.

- **Frontend:** dynamic `import()` of routes/components only when navigated to (Q259); `<img loading="lazy">` for below-fold images; `useLazyQuery` in React Query.
- **Backend:** lazy relationship loading (SQLAlchemy lazy=True — though this causes N+1, Q348), defer expensive joins.
- **Networking:** lazy connect/initialize clients.

Benefits: smaller initial payload, faster first paint. Costs: loading flicker when needed (mitigate with suspense/skeletons).

---

## Q259: What is code splitting?

Splitting the JS bundle into **chunks loaded on demand**, so the initial page ships less code.

```jsx
// route-level split
const Dashboard = React.lazy(() => import("./Dashboard"));

function App() {
  return (
    <Suspense fallback={<Spinner/>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard/>} />
      </Routes>
    </Suspense>
  );
}
```

- Next.js App Router does **automatic route-level code splitting**.
- Also: vendor chunking, dynamic imports for heavy libraries (e.g., a markdown renderer only on the doc page).
- Measured via bundle analyzer; goal: smaller critical path, no huge single chunk.

---

## Q260: What is virtualization?

Rendering **only the visible subset** of a large list (plus a small buffer), while using spacers to keep scroll metrics correct — instead of mounting all rows.

```jsx
import { FixedSizeList as List } from "react-window";
<List height={600} itemCount={100000} itemSize={35}>
  {({ index, style }) => <Row style={style} item={items[index]} />}
</List>
```

- Libraries: react-window, react-virtualized, TanStack Virtual.
- Why: 100k DOM nodes crush memory/paint; 20 visible nodes are fast.
- Use when lists are large (1k+ rows), especially with heavy rows (chat history, logs, candidate tables).

---

## Q261: How would you handle 100,000 records in a frontend application?

1. **Never render all at once.** The answer starts with pagination/virtualization:
   - **Server-side pagination** (Q256) — load pages of 50–100; standard for data tables.
   - **Virtualization** (Q260) — for large client lists that must stay in memory.
   - **Infinite scroll** (Q579) — lazy append.
2. **Filter/sort server-side** — don't download 100k rows to filter on the client.
3. **Debounce** search input (Q578).
4. **Aggregate client-side if needed** — derive counts/sums with `useMemo`.
5. **Cache** pages in React Query to avoid refetching.
6. **Consider streaming/SSR** for first paint.

**Priority answer:** "Pagination is the primary answer; virtualization when the visible dataset is large; never materialize 100k DOM nodes."

---

## Q262: How would you handle 10,000 concurrent API requests?

**This is about architecture, not just code:**

1. **Async server:** FastAPI + Uvicorn workers (each worker's event loop handles thousands of concurrent I/O-bound requests) — `asyncio` + async clients (Q79–95).
2. **Worker count:** don't add workers blindly; match CPUs for CPU-bound; more workers = more memory + connection overhead. Use Uvicorn with multiple workers (or Gunicorn+Uvicorn) (Q652).
3. **Connection pooling** for DB (bounded), PgBouncer if needed; async DB drivers.
4. **Rate limiting + backpressure** at the edge (Q107, Q293).
5. **Cache** hot reads (Redis/CDN) to cut origin load.
6. **Queue** heavy work (resume parsing, LLM calls) to background workers (SQS/Celery/RQ) — API returns fast, workers process.
7. **Autoscaling** horizontally (Q370) behind a load balancer; stateless app servers (sessions in Redis).
8. **Limits at every dependency** — external APIs (LLM) with semaphores so 10k inbound doesn't blast the provider.
9. **Observability** — connection limits, queue depth, p99, timeouts (Q632–633).
10. **Load test** (k6/locust) to find the real ceiling; scale with evidence.

---

## Q263: How would you reduce database load?

1. **Caching** — Redis for hot reads (Q248–253); move reads off the DB.
2. **Read replicas** — route reporting/heavy reads to replicas; primary stays for writes (Q566–567).
3. **Indexes** — fix the slow queries so scans become point lookups (Q245).
4. **Pagination** — cap result sizes (Q256).
5. **Batching** — fewer round trips: multi-row inserts, `IN` clauses, batch updates (Q255).
6. **Denormalization/materialized views** — precompute aggregates for dashboards (Q159, Q556).
7. **Connection pooling** — bound and reuse connections (Q172).
8. **Query offloading** — move aggregation to app-level caches or a warehouse for analytics.
9. **Background processing** — heavy writes batched via queues.
10. **Tuning** — `statement_timeout`, `work_mem` for sorts, autovacuum (Q336), avoiding locks.
11. **Partitioning** for very large tables (Q558–560).

---

## Q264: How would you optimize an endpoint that calls an LLM?

1. **Reduce tokens** — the biggest lever: shorter prompts/system prompts, relevant context only (RAG, Q660), concise instructions, fewer output tokens.
2. **Model routing** — use a small/cheap model for easy tasks, big model only when needed (Q674–675).
3. **Cache responses** — exact-match cache (Redis) + **semantic cache** (embedding-similar queries reuse answers) for repeat questions (Q678).
4. **Stream** — SSE/WebSocket so the client gets the first token fast; perceived latency ↓ (Q399, Q496).
5. **Parallelize** — if multiple LLM calls are independent, `asyncio.gather` them (Q120); if dependent, pipeline them.
6. **Prompt/context management** — trim chat history (Q287–288), summarize old turns.
7. **Batching** — OpenAI batch API for non-urgent bulk (50% cheaper).
8. **Timeouts + retries + fallbacks** — bounded, so a slow LLM doesn't hang the endpoint (Q269–272).
9. **Concurrency control** — semaphore per provider to avoid hitting rate limits/backlog (Q272).
10. **Measure** — token counts, latency per stage (TTFT), cache hit rate, cost per request.

---

## Q265: How would you reduce latency in an AI workflow?

1. **Stream the LLM output** — first token in ~100-300ms instead of waiting for full completion (Q496).
2. **Run steps in parallel** where independent (embedding + retrieval + classification concurrently) (Q120).
3. **Cache aggressively** — prompt-response caches, semantic caches, precomputed embeddings/retrieval (Q678).
4. **Shorten context** — fewer tokens in = faster generation; use summaries (Q287–288).
5. **Use faster models for sub-tasks** — routing (Q674–675); distill where quality allows.
6. **Pre-warm / keep-alive** — warm model endpoints, persistent connections (HTTP keep-alive, connection pools).
7. **Deploy closer** — region/edge; avoid cross-continent hops.
8. **Async + queues** — don't block the request on heavy steps; return fast, process in background.
9. **Efficient retrieval** — ANN indexes (HNSW), smaller candidate sets, rerank only top-k (Q661–669).
10. **Speculative/optimistic** — predict next action while waiting (prefetch retrieval during generation).
11. **Batching prompts** where the workflow allows provider-level batching (Q255).
12. **Measure per stage** (TTFT, tokens/sec, retrieval ms, queue time) — optimize the largest stage.