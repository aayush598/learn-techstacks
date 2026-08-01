# SQL vs NoSQL Decision Guide

> **TL;DR**: Choose by workload shape, not hype — start relational by default (integrity, joins, transactions, ad-hoc queries); pick a NoSQL family only when a specific pattern dominates (O(1) key access → KV, flexible objects → document, write-heavy availability → wide-column, analytic scans → columnar, relationship traversal → graph), and formalize the choice with a question checklist plus a consistency/availability/latency requirement analysis.

## 1. Why Does This Exist?
Teams endlessly ask "SQL or NoSQL?" — and the honest answer is "it depends on the workload." This guide exists to make that decision *systematic* instead of cargo-culted. Every engine (Parts 01-07 relational; Chapter 01 NoSQL families) is a set of trade-offs: generality + integrity + transactions (relational) vs scale + availability + flexibility + specialization (NoSQL). The guide converts the abstract trade-offs into a concrete checklist: What does the *read* look like (by-key? aggregates? traversals?)? What does the *write* look like (transactional? append-heavy?)? What consistency do you *really* need (Part 05 vocabulary)? How does data scale (rows, bytes, writes/sec)? Answering those — not brand preference — is what a senior engineer does before any "should we use Mongo?" discussion, and it's exactly what interviewers probe.

## 2. How Does It Work?
A structured decision process:
1. **Name the dominant access patterns** (list the top 5-10 queries): point lookups by key? joins across entities? aggregations over many rows? paths/traversals? append-heavy time-series?
2. **Name the dominant write patterns**: transactional multi-row updates? append-only events? last-write-wins counters? hot-key increments?
3. **Requirement analysis**: consistency (strong? causal? eventual? — Part 05's isolation vocabulary), availability (RPO/RTO, multi-DC?), latency (p99 targets), scale (write throughput, data volume, read amplification), team ops capacity.
4. **Map patterns → engine**: by-key-only → KV; objects-with-variable-schema + field queries → document; write-heavy-append + availability + time-range reads → wide-column; analytic scans → columnar/warehouse; relationships/traversal → graph; default (joins, integrity, ad-hoc) → relational.
5. **Validate**: run the top queries on a prototype; check EXPLAIN (Part 07), verify the consistency story; reject the pick if the dominant query is a poor fit.
6. **Document the decision** (ADR) including the *rejected* options and why.

## 3. When Is It Used?
- Architecture kickoff / tech choice for a new service.
- "Should we migrate X from Postgres to Mongo?" — the answer is usually no; the guide explains why (or when yes).
- Polyglot persistence decisions: which store for *which* data (users in Postgres, cache in Redis, analytics in ClickHouse, social graph in Neo4j).
- Interview answers: "how would you pick a database for X?" — the framework is the answer.
- Reviewing existing systems: does each store's usage match its strengths (and is the misuse obvious from the queries)?

## 4. Why Wasn't Another Approach Chosen?
- *"Always use Postgres" (default-dogmatism)*: right for most OLTP, but for truly scale-bound or specialized patterns (100k writes/s telemetry, billion-row scans, variable-depth traversal) it means fighting the engine with sharding/recursive CTEs. The guide keeps relational as the *default* but acknowledges the escape hatches with evidence.
- *"Always use Mongo" (hype-following)*: drops integrity/joins you often actually need, then teams rebuild them in app code. The guide makes you prove you *don't* need them before giving them up.
- *"Use one store for everything" (monolith-ism)*: forces the wrong tool on some workload; polyglot persistence (a store per data's *pattern*) is usually right — with the cost of operational sprawl, which the guide makes explicit.
- *"Benchmark-driven only"*: microbenchmarks without workload analysis pick winners for the wrong queries; the guide anchors decisions in *actual* access patterns first, then validates with measurement.
- *"Migrate everything to NewSQL"*: real SQL + scale + strong consistency sounds free, but consensus overhead, ops complexity, and maturity concerns make it a *targeted* choice (finance-scale correctness), not a default.

## 5. Intuition
Choosing a database is like **choosing a vehicle for a delivery business**. The default is the *sedan* (relational): seats for passengers, trunk space, drives anywhere, gets you from A to B with receipts (transactions) and street-legal paperwork (integrity) — perfect for most deliveries. You *do not* buy a different vehicle because someone says "sedans are outdated." You specialize only when a pattern dominates: if 90% of deliveries are single parcel to a known locker → the *courier scooter* (key-value): tiny, O(1), cheap per trip. If parcels are weird-shaped and self-contained → the *cargo van* (document): flexible loading, no ties between loads. If you ship 10,000 parcels/hour to a hub and never want to stop → the *sorting conveyor* (wide-column): append-and-go, never blocks. If your analytics need "total spend by region over 2 years" → the *warehouse forklift* (columnar): moves tons fast, but can't do a local delivery. If the business is *who-knows-whom* → the *courier routing map* (graph): follows connections. The mistake is picking the conveyor because "it's newer" while your business is local courier deliveries — or buying the sedan and pretending it can sort 10k parcels/hour.

## 6. Real-World Analogy
**A media company building a news app.** The *users, subscriptions, and billing* are classic relational data: accounts need integrity, payments need transactions, "find me all subscribers on plan X in region Y" needs ad-hoc joins and grouping → **Postgres**. The *article content* is self-contained objects with variable metadata (some have video embeds, some data-journalism blocks, all different schemas) and reads are "fetch this article by id" → **document store** (MongoDB) or just JSONB in Postgres (the "JSONB question" — you may not need a second store). The *view counters* and *session data* are ephemeral, key-driven, high-write → **Redis** (KV, TTL). The *reading-history analytics* ("article reads by section by hour for the last 6 months") is a big scan/aggregation → **columnar/warehouse** (ClickHouse/BigQuery), fed by streaming events. The *author→editor→article→topic knowledge graph* for "related stories" → **graph** (Neo4j) if traversal matters. One app, five data patterns, five stores — each chosen by its *query shape*, not by brand. The failure mode is forcing articles into the users table (rigid schema) or forcing billing into MongoDB (no transactions). The guide's checklist would catch both before the code starts.

## 7. Formal Definition
**Decision framework inputs**: dominant read patterns R = {by-key, joins, aggregates, scans, traversals}; dominant write patterns W = {transactional-update, append-only, LWW-counter}; requirements C = {strong consistency, causal, eventual} (Part 05), A = {availability target, RPO/RTO, multi-DC}, L = {latency p99}, S = {write throughput, data volume, query breadth}; team ops capability.
**Rule**: default to a relational engine; deviate to a NoSQL family only when (∃ a dominant pattern in R ∪ W that the relational engine serves poorly) ∧ (the chosen family's guarantee drop — from ACID to BASE/eventual, and its query-model restriction — is *acceptable* for the top queries) ∧ (ops cost is affordable). **Polyglot persistence**: partition data by pattern and assign each partition the fitting engine, with the caveat of increased operational complexity and cross-store consistency (often acceptable as it's eventually-consistent by design).

## 8. Example
Problem: **building a mobile ride-hailing app — which store for what?**
1. **Riders, drivers, wallets, trip ledger** → relational (Postgres): ACID for wallet updates (money), joins for "driver with rating>4.5 in zone X", reporting SQL. Decision: default relational.
2. **Driver locations (high-write updates)** → could be Redis (KV with TTL) or a KV geo layer: writes are ephemeral, keyed by driver, no integrity needed, must be low-latency. Not relational (write storm on one table would bottleneck).
3. **Trip events / telemetry stream** → append-only, enormous volume, analytics later → columnar/warehouse (ClickHouse/BigQuery) fed by a queue; point reads rare.
4. **"Frequent rider" social/referral network (who invited whom, mutual riders)** → graph (Neo4j) if viral/referral analytics matter; or keep it in Postgres with a `referrals` table if depth is shallow (2-3 hops, low volume) — the guide's "is it really traversal-bound?" check.
5. **Session/auth tokens** → Redis (TTL).
The guide's output: Postgres as system of record + Redis cache/session + warehouse for analytics + (optional) graph for referrals — with each choice defended by pattern + consistency + ops cost. If wallet updates needed distributed ACID at scale, *then* NewSQL (CockroachDB) becomes the candidate — but only after proving Postgres+partitioning insufficient.

## 9. Internal Working
1. **Profile the top queries** (from monitoring, Part 07 §3): for each, mark access type (by-key/join/aggregate/traversal), consistency requirement, latency, frequency.
2. **Test the relational default first**: can Postgres/MySQL handle the pattern with the tools we have (indexes, partitions, recursive CTE for bounded depth, JSONB for flexible shapes)? If yes → stop; don't add a store you don't need. (JSONB is the underrated answer to "document-ish" needs in Postgres.)
3. **Escalate only on evidence**: a dominant pattern that relational serves badly (per measurement/plan), or a scale/consistency requirement relational can't meet (single-writer bottleneck, RPO).
4. **Match family** via the mapping table (Section 8/13) and verify the *guarantee drop is acceptable* (esp. consistency: eventual vs strong for money/inventory — use Part 05's isolation knowledge).
5. **Prototype the top-3 queries on the candidate**; compare latency/cost on realistic data; sanity-check ops (backups, failover, team skill).
6. **Write the decision** (ADR): chosen store, rejected options, the pattern evidence. Revisit when the workload changes (the decision is a point-in-time answer).

## 10. Time Complexity
- Decision cost: hours, not years — the framework's value is *structure*, not speed. The mistake to avoid is making it reversible-proof ("we'll migrate later") — migrations cost team-months.
- Validation cost: prototype = one spike (hours-days).
- Long-term cost of the *wrong* choice: re-architecture. The framework exists to spend the small planning cost to avoid the large migration cost.
- Ongoing: each new data pattern should re-run the checklist (a new store is a new ops burden — "one more system to operate" is a real cost term).

## 11. Advantages
- **Defensible, documented decisions** — the ADR records *why*, not just *what*.
- **Right tool per pattern** — polyglot persistence where it pays; avoids over-engineering (JSONB instead of a Mongo install).
- **Consistency risks surfaced early** — the framework forces you to name the consistency requirement (Part 05) before choosing eventual consistency.
- **Interview-ready**: the framework *is* a strong answer to "which database would you use for X?"
- **Migration-aware**: keeps the default relational, so common cases don't pay NoSQL's costs.
- **Ops-cost honesty**: counts "one more system to run" as a real term, which prevents store-sprawl.

## 12. Disadvantages
- **Framework ≠ correctness**: the mapping is heuristic; real workloads need validation (prototype + measurement).
- **Polyglot sprawl**: many stores = more ops, more failure modes, cross-store consistency gaps (a bug source).
- **Over-analysis paralysis**: teams can benchmark forever instead of shipping; the guide must be time-boxed.
- **Requirement discovery is hard**: teams often *believe* they need strong consistency (or not) without measuring — the guide surfaces this but can't resolve it alone.
- **Evolving workload**: a choice right at year 1 can be wrong at year 3 (scale change flips the answer); the guide needs revisiting, which teams skip.
- **No mechanical answer**: two teams with the same workload can legitimately choose differently (ops capability, risk tolerance) — the guide makes the *reason* explicit, not the answer deterministic.

## 13. Interview Questions
1. **Q: SQL vs NoSQL — how do you actually decide?** A: Start from the *dominant access patterns* and *consistency needs*, not brand. Default to relational; deviate only when a specific pattern dominates that relational serves badly (by-key O(1) → KV, flexible objects → document, write-heavy availability → wide-column, analytic scans → columnar, traversal → graph) AND the guarantee drop is acceptable. Validate with the top queries on a prototype.
2. **Q: TRICKY: "Just use Postgres + JSONB" — when is that enough?** A: When the flexible-schema need is one or two columns on an otherwise-relational entity (settings, specs), and you don't need the *distributed* document store's scale. Postgres JSONB gives indexing (GIN), expressions, and joins with relational tables — often the cheapest correct answer. Reach for a real document store when the whole object model is document-shaped *and* you need horizontal write scale.
3. **Q: When would you migrate from MongoDB to Postgres?** A: When the app's real queries turn out relational — joins across entities, reporting SQL, strict integrity/transactions — and Mongo's flexibility is unused. The signal is `$lookup` chains, duplicate denormalized data being updated in 5 places, and app-side transaction emulation. Migrate when the engine fights the workload, not for fashion.
4. **Q: What is polyglot persistence?** A: Using different storage engines for different data in one system — each chosen for its data's access pattern (relational for core, Redis for cache, columnar for analytics, graph for relations). Pros: right tool each. Cons: ops sprawl, cross-store consistency (usually eventual), more failure modes.
5. **Q: TRICKY: Your team chose Redis as the "database" for a session/auth service. Risks?** A: Redis is durable-ish (AOF/RDB) but not a correctness-strong system of record: LWW, no multi-key ACID, eviction risk, memory-bound. For sessions that's often fine (TTL, recreatable); for auth tokens whose loss logs users out at scale, that may matter. The framework: what's the RPO if Redis loses 30 seconds of writes? If unacceptable, persist elsewhere.
6. **Q: How do you choose between Cassandra and DynamoDB?** A: Managed-vs-self-hosted first (DynamoDB = zero ops, RCU/WCU pricing, 400KB item cap; Cassandra = self-run, tunable consistency levels, CQL richness, but ops burden). Then consistency control (DynamoDB strong reads vs Cassandra QUORUM dial) and existing cloud investment. Same *family*, different operational contract.
7. **Q: When is a columnar/warehouse store needed vs a relational DB with indexes?** A: When analytic scans dominate (aggregations over 10^8-10^12 rows) and the relational engine's row-store I/O becomes the bottleneck — then a warehouse (Redshift/BigQuery/ClickHouse) with columnar storage + MPP answers in seconds what a row store takes minutes-hours. Relational-with-indexes stays right for mixed OLTP+light reporting.
8. **Q: TRICKY: E-commerce cart — SQL or NoSQL?** A: Cart is *per-user keyed data* with TTL-ish lifetime → could be Redis/DynamoDB (KV). BUT the cart touches inventory (decrement) and checkout (transaction) → inventory/order must be relational/transactional. Common design: cache the cart in Redis, persist orders/stock in Postgres, keep them consistent with careful flows. The *boundary* is where money/integrity begins.
9. **Q: How do you evaluate consistency requirements in practice?** A: List each data item's tolerance to (a) stale reads (seconds? minutes? never?) and (b) lost updates (LWW acceptable?). Money, inventory, and unique constraints → strong/transactional. Feeds, counters, caches, profiles → eventual is usually fine. This is Part 05's isolation vocabulary applied to the decision.
10. **Q: What's your framework when the workload is "read-heavy, simple schema, huge concurrency"?** A: Relational default + Redis cache-aside absorbs the reads; add read replicas; consider KV if the reads are purely by-key. Don't jump to a distributed KV for "huge concurrency" without first caching — most read-heavy OLTP is solved by cache + replicas + proper indexes (Part 07), which keeps integrity intact.
11. **Q: TRICKY: Why is "NoSQL scales better" both true and false?** A: True for *write* scale on append/partitionable workloads (Cassandra) and for by-key *read* scale (KV, via partitioning + caching). False as a blanket: relational read scale via replicas/read-heavy caching is also excellent, and NoSQL *general query* scale (joins/traversals across partitions) is poor. "Scales better" applies to specific patterns, not to "the app."
12. **Q: How do you handle "we need both flexible schema AND strong transactions"?** A: Keep the transaction boundary relational; put flexible-schema data as JSONB/JSON columns (indexable) inside it — or accept document + *explicitly application-managed* consistency for the flexible parts. There's no free lunch; the guide's job is making the chosen compromise explicit.
13. **Q: What does "eventual consistency" cost you concretely in an app?** A: Stale reads (a user sees an old value briefly), lost updates under LWW (concurrent writers), and the need for reconciliation code (vector clocks, read-repair, idempotency). For non-critical data that's a price worth paying; for money/inventory it's usually not. Naming *which* data pays the price is the design step.
14. **Q: PR: Someone proposes a "database per microservice." Agree?** A: Per-service *ownership* of its data is right (bounded context); a *different engine* per service is a cost decision. Relational per service is fine (one engine, many databases). Deploy a *different family* (graph, columnar, KV) only when that service's pattern demands it — polyglot for a reason, not for trend.
15. **Q: What's the role of NewSQL in this decision?** A: When you need SQL semantics + horizontal write scale + strong cross-node transactions (finance-grade, distributed OLTP) and can pay consensus overhead + ops complexity — Spanner, CockroachDB, TiDB. It's the "have it all" corner; most workloads never need it, but the *capability* matters for the biggest systems.

## 14. Follow-Up Questions
1. **Q: What is a "workload profile" and how do you build one?** A: A ranked list of your top queries by frequency/latency/cost (from pg_stat_statements/logs), plus write patterns and data growth — the input to the decision. Building it before choosing prevents "we picked Mongo for joins" post-hoc.
2. **Q: How do you run a validation spike?** A: Load a realistic dataset (1-10% of expected volume), run the *top-3* predicted queries, compare latency/cost/EXPLAIN across candidates, and check the consistency behavior under failure (kill a node). Days of spike beats months of migration.
3. **Q: When is it acceptable to *not* have a system of record?** A: Only for data that's reconstructable (caches, derived caches, transient state) — even then someone "owns" regeneration. The framework keeps at least one authoritative store per data class; everything else is a projection of it.

## 15. Coding Example
```sql
-- The "JSONB vs document store" test: can Postgres serve it?
CREATE TABLE products (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku text NOT NULL,
  price numeric NOT NULL,
  specs jsonb NOT NULL DEFAULT '{}'
);
CREATE INDEX idx_products_specs ON products USING GIN (specs jsonb_path_ops);
-- "black electronics" — indexed JSONB query, joinable with relational tables
SELECT * FROM products
 WHERE specs @> '{"color":"black"}' AND price < 1000
 ORDER BY price;
```
```python
# Validating the top queries (decision evidence)
def decide_candidate(reads, writes, consistency):
    if consistency == "strong" or "join" in reads:
        return "relational"          # default until proven otherwise
    if "by-key" in reads and not {"aggregate", "traversal"} & set(reads):
        return "key-value"
    if "scan-aggregate" in reads:
        return "columnar"
    if "traversal" in reads:
        return "graph"
    return "relational"              # no dominant NoSQL pattern
```
```sql
-- The consistency question (Part 05 vocabulary) drives the choice:
--  money → READ COMMITTED / SERIALIZABLE + transactions (relational)
--  counters → Redis INCR (LWW is fine)
--  analytics → eventual (columnar)
--  inventory decrement → must be transactional (relational / LWT)
```

## 16. Industry Usage
- **Default relational, everywhere**: most systems (Postgres/MySQL) carry the core — the "Postgres is enough" school (JSONB, partitioning) is mainstream for 80% of workloads.
- **Polyglot at scale**: e-commerce (Postgres + Redis + warehouse), social (relational core + Redis + graph), telemetry (relational config + Cassandra ingestion + columnar analytics).
- **NewSQL for the biggest transactional systems**: Spanner (Google), CockroachDB (multi-cloud OLTP), TiDB (PingCAP) — the "SQL + scale + strong consistency" niche.
- **The JSONB pattern**: teams increasingly reach for Postgres JSONB before adding a document store — an acknowledged best practice that shrinks the "Mongo everywhere" mistake.
- **Warehouse separation**: OLTP (relational) + OLAP (columnar) with ETL/CDC streaming is the standard architecture across industries.

## 17. References
- "One Database Per Service?" — Martin Fowler, "Polyglot Persistence": https://martinfowler.com/bliki/PolyglotPersistence.html
- Use The Index, Luke — PostgreSQL JSONB: https://www.postgresql.org/docs/current/datatype-json.html
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 2-5, 7 — the decision vocabulary (consistency, replication, partitioning).
- Brewer, "CAP Twelve Years Later" and Abadi, "PACELC" (as in Section 01).
- "Choosing a Database for a New System" — standard engineering ADR templates (e.g., ThoughtWorks tech radar write-ups).

## 18. Cheat Sheet
- Decision order: patterns → consistency → scale → ops → map → validate → ADR.
- Default relational; deviate only on evidence.
- Mapping: by-key → KV; flexible objects → document (or JSONB first!); write-heavy+availability → wide-column; scans → columnar; traversal → graph; joins/integrity/transactions → relational; SQL+scale+ACID → NewSQL.
- JSONB (Postgres) often beats a new document store — reach for the engine only when scale demands it.
- Consistency check: money/inventory/unique → strong/transactional; feeds/counters/cache → eventual OK.
- Polyglot persistence: right tool per pattern, but count the ops cost; keep a system of record.
- "NoSQL scales better" = specific patterns, not a blanket truth.
- Prototype the top-3 queries; measure, then decide.
- Revisit the decision as the workload changes; write the ADR so the *why* survives.

## 19. Quiz
1. Default choice? a) Mongo b) relational c) Cassandra d) Redis → **b**
2. O(1) by-key reads only → a) graph b) KV c) columnar d) relational → **b**
3. Analytic scans over billions → a) KV b) document c) columnar d) graph → **c**
4. Traversal-heavy → a) graph b) relational c) KV d) warehouse → **a**
5. Flexible schema, single column → a) new store b) JSONB c) Cassandra d) HBase → **b**
6. Money/inventory → a) eventual b) strong/transactional c) LWW d) cache → **b**
7. Polyglot persistence cost is: a) zero b) ops sprawl + cross-store consistency c) slower reads d) none → **b**
8. NewSQL is for: a) cache b) SQL + scale + strong consistency c) graphs d) analytics → **b**

## 20. Flashcards
- **Q: Decision order?** → **A:** Patterns → consistency → scale → ops → map → validate.
- **Q: Default engine?** → **A:** Relational (deviate only on evidence).
- **Q: Flexible schema, one column?** → **A:** Postgres JSONB first.
- **Q: Traversal workload?** → **A:** Graph DB.
- **Q: Money/inventory consistency?** → **A:** Strong / transactional.
- **Q: "NoSQL scales better" is?** → **A:** Pattern-specific, not a blanket truth.
- **Q: Polyglot cost?** → **A:** Ops sprawl + cross-store consistency gaps.
- **Q: NewSQL?** → **A:** SQL + scale + strong consistency (Spanner/CockroachDB/TiDB).

## 21. Revision
The decision is workload-shaped, not brand-shaped: name the dominant reads/writes, state consistency needs (Part 05), then map — by-key → KV, objects → document (JSONB first!), write-heavy+availability → wide-column, scans → columnar, traversal → graph; everything else stays relational; SQL+scale+ACID → NewSQL. Validate by prototyping the top queries, document the ADR, and revisit as the workload grows. Most systems: one relational core + Redis + a warehouse — with extra families only when a pattern truly demands it.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "SQL vs NoSQL — how do you decide?" | 2, 13 |
| "When is Postgres JSONB enough?" | 13 |
| "Migrate Mongo → Postgres?" | 13 |
| "What is polyglot persistence?" | 4, 13 |
| "Redis as the DB for sessions?" | 13 |
| "Cassandra vs DynamoDB?" | 4, 13 |
| "Columnar vs relational-with-indexes?" | 13 |
| "E-commerce cart — SQL or NoSQL?" | 13 |
| "How do you evaluate consistency needs?" | 2, 13 |
| "DB per microservice — agree?" | 13 |
