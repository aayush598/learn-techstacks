# Denormalization and When to Use It

> **TL;DR**: Denormalization deliberately merges tables or adds redundant columns to trade write/space correctness for **read speed** — fewer joins, fewer index lookups, fewer round trips. It's a performance decision, not a correctness one: you reintroduce the anomalies 3NF removed and must control them with app/trigger discipline. Use it when reads dominate, joins are hot, and you can measure the win.

## 1. Why Does This Exist?
3NF/BCNF schemas are *correct* but joins are expensive. A hot dashboard query `SELECT ... FROM orders o JOIN customers c ON o.customer_id=c.id JOIN addresses a ON c.address_id=a.id` chases three B+ tree paths per row. When 99% of load is reads, the normalized design's "store each fact once" purity costs wall-clock time: each join is a probe, a cache miss, and a round trip. **Denormalization exists to spend redundancy (space + write time) to buy read latency and throughput.** Real systems (analytics, read-heavy APIs, caches, data warehouses) are built around denormalized data — star schemas, columnar stores, materialized views — because normalized joins don't scale for analytics. It's the deliberate, disciplined violation of the normal forms, not an accident.

## 2. How Does It Work?
Denormalization is any technique that reintroduces redundancy to reduce joins or reads:
- **Duplicated columns**: `order_rows.customer_name` instead of joining customers (violates 2NF/3NF — transitive/partial storage).
- **Merged tables**: flatten a 1:N (parent repeated in child rows) — violates 1NF/3NF but kills the parent join.
- **Precomputed aggregates / materialized views**: `daily_orders_total` column or a summary table — violates the "no derived data" discipline but saves aggregation per query.
- **Stored/lifted arrays or JSON**: embedding children into a parent row — one row read instead of N.
- **Wide star schemas**: facts + denormalized dimension attributes for BI.
**The contract**: you accept update/insert/delete anomalies and pay back with *controls* — triggers to propagate updates, background jobs to refresh, application-level consistency checks, or eventual-consistency tolerance.

## 3. When Is It Used?
- **Read-heavy OLTP**: hot read paths (profile pages, dashboards) with joins on millions of rows.
- **Data warehousing / BI**: star schemas denormalize dimension attributes into fact tables for scan speed.
- **Materialized views / read models**: CQRS read models are denormalized projections.
- **Cache-friendly access**: document/array embedding to read one row per page.
- **When normalized writes don't matter** (append-only analytics, immutable events) — denormalization costs almost nothing.
- **NOT** when writes dominate, consistency is strict, or the redundancy must be updated transactionally at scale (sync propagation pain).

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: keep 3NF and let the DB optimize joins.** Rejected where the DB's optimizer/cost model still probes per row — B+ tree joins on big tables are fundamentally more expensive than reading one wide row. Indexes reduce join cost but don't eliminate it.
- **Alternative: add indexes instead.** Chosen first — indexes are the cheap fix; denormalization is when indexes aren't enough (join count × rows still high).
- **Alternative: cache (Redis) the read.** Chosen often — but caching duplicates data outside the DB, with cache invalidation complexity; denormalized columns are a simpler, in-DB cache.
- **Why not keep normalization "for safety"?** Because measured latency targets (p99 under X ms) can't be met with 5-join queries; denormalization is the tool that meets the SLO, with controls replacing the lost constraints.
- **Why not go all-in denormalized?** Because update anomalies + drift become unmanageable; the answer is a *targeted*, measured redundancy — denormalize the hot 5% only.

## 5. Intuition
Normalization is **organizing a library** (each fact stored once, in its right shelf — correct but you must walk between shelves). Denormalization is **keeping a photocopy of the popular page right at the front desk**: the dashboard user reads one sheet instead of walking five aisles. The photocopy is redundant (the original still exists) and can go stale (someone edits the book) — so you tape a note ("refresh nightly") and accept that a 5-minute-old dashboard is fine. The whole craft is choosing *which* photocopies are worth it: the hot ones, the read-only ones, and the ones where staleness is tolerable. Where the library rule (3NF) was about never duplicating truth, the front-desk rule (denormalization) is about duplicating truth *cheaply and controlled* where latency demands.

## 6. Real-World Analogy
A **restaurant kitchen with a printed menu and a chalkboard specials board**. The menu (normalized) lists every dish; the board (denormalized) duplicates today's three specials right where customers see them — no walking to the store room to read ingredient lists. The board is redundant: the dish data still lives in the store room, and if the kitchen changes a special mid-shift, the board must be updated too (the "propagation trigger"). It works because: specials change rarely (low write rate), customers read constantly (high read rate), and a 5-minute-stale board is harmless (staleness tolerance). The board is the perfect denormalized index — justified by exactly the three conditions that make denormalization safe: read-heavy, rarely-updated, staleness-tolerant.

## 7. Formal Definition
No single formal definition — denormalization is the inverse of normalization: a schema is denormalized relative to 3NF/BCNF/4NF when it intentionally contains redundant data (duplicated columns, merged relations, derived/aggregate values, embedded structures) that a normalized design would not store, for the purpose of reducing query cost. Formally: the schema violates one or more normal-form conditions (e.g., a non-key attribute depending transitively on the key, or a child table repeating parent facts) *by design*, and the redundancy is managed by propagation mechanisms (triggers, jobs, application logic) rather than by the relational constraints themselves.

## 8. Example
**Normalized (3NF)**:
```
CUSTOMER(customer_id PK, name, city)
ORDERS(order_id PK, customer_id FK, total)
-- Daily dashboard: sum of totals per city = join + group by
```
**Denormalized option 1 — redundant column**:
```
ORDERS(order_id PK, customer_id FK, customer_city, total)
-- dashboard: SELECT city, SUM(total) GROUP BY city — one table, no join
-- cost: city repeated per order; renaming a city = update every order row (update anomaly)
-- control: trigger on CUSTOMER.city update → propagate to ORDERS.customer_city
```
**Denormalized option 2 — materialized summary**:
```
CREATE MATERIALIZED VIEW city_totals AS
  SELECT city, SUM(total) FROM ORDERS GROUP BY city;  -- refreshed per policy
-- dashboard reads the precomputed view: O(rows in view) not O(orders)
-- control: REFRESH MATERIALIZED VIEW CONCURRENTLY (Postgres) or app-triggered refresh
```
**Option 3 — embedded JSON (read-one-row)**:
```
ORDERS(order_id PK, customer JSONB)  -- {'name','city',...} copied in
-- one row read per order page; customer edits need re-sync (eventual).
```

## 9. Internal Working
1. **Measure first**: profile the hot query (EXPLAIN ANALYZE); confirm joins/aggregation dominate.
2. **Classify write pattern**: if the redundant data changes rarely (dimension attributes) denormalization is cheap; if it changes per transaction, sync cost rises.
3. **Pick the technique**: duplicate column (simplest), merge tables, materialized view (Postgres `MATERIALIZED VIEW` with `CONCURRENTLY`), or embedded JSON (document store pattern).
4. **Build the propagation control**: triggers (Postgres `AFTER UPDATE ... FOR EACH ROW`), jobs (`REFRESH MATERIALIZED VIEW`), CDC pipelines, or event-sourced read models.
5. **Bound staleness**: decide tolerance (seconds/minutes); eventual consistency is usually fine for dashboards.
6. **Verify with EXPLAIN**: confirm the denormalized path eliminates joins; measure p99 before/after.
7. **Document the anomaly**: every denormalized column gets a comment + owning service so drift is explainable.
8. **Isolate**: keep normalized source as the system of record; denormalize only the hot read layer.

## 10. Time Complexity
- **Normalized join query**: O(rows_to_join × B+ tree probe) — roughly O(n·log m) per join.
- **Denormalized read**: O(result_rows) single-table scan / index read — one order of magnitude fewer probes.
- **Aggregate query**: normalized = O(orders); materialized = O(cities) after refresh.
- **Write cost**: denormalized inserts/updates pay O(redundancy fan-out) — the price of the read win.
- **Refresh**: `REFRESH MATERIALIZED VIEW CONCURRENTLY` runs O(orders) periodically, amortized.

## 11. Advantages
- **Massive read latency win**: join elimination, fewer probes, fewer round trips.
- **Cheap dashboard/aggregation reads**: precomputed sums make OLAP queries O(summary) not O(fact).
- **Simple hot-path queries**: one table, one index, easy to reason about and cache.
- **Enables CQRS/read-model patterns**: denormalized projections power fast APIs.
- **App-level read patterns stay stable** while the source-of-truth schema evolves.

## 12. Disadvantages
- **Update/insert/delete anomalies return**: renamed city must propagate; missed propagation = drift.
- **Sync machinery complexity**: triggers/jobs/CDC are new failure modes and new code.
- **Staleness**: read models lag the source — wrong for strict-consistency domains (payments, inventory at checkout).
- **Disk bloat**: redundancy multiplies storage (acceptable for wide, compressed analytics).
- **Two sources of truth**: drift is subtle and hard to debug ("why is this order's city old?").
- **Write amplification**: every source update fans out.

## 13. Interview Questions
1. **Q: What is denormalization?** A: Deliberately reintroducing redundancy (duplicated columns, merged tables, aggregates, embedded data) to reduce join/read cost — violating normal forms by design, with propagation controls.
2. **Q: When do you denormalize?** A: When reads dominate, joins are hot, updates to the redundant data are rare, and staleness is tolerable — and after indexes/caching aren't enough. Measure with EXPLAIN first.
3. **Q: What's the trade?** A: Read speed for write complexity + space + anomaly risk. Normalized = safe but slower reads; denormalized = fast reads, managed drift.
4. **Q (scenario): Dashboard sums orders per city; join is slow.** A: Add `customer_city` to ORDERS (redundant column) or build a materialized view; refresh via trigger/job; verify with EXPLAIN.
5. **Q: How do you control drift?** A: Triggers propagating dimension updates, `REFRESH MATERIALIZED VIEW CONCURRENTLY`, CDC/event pipelines, or app-level reconciliation — always bounded staleness.
6. **Q: Star schema — normalized or not?** A: Fact tables reference dimension tables by key (normalized-ish) but dimensions are wide/denormalized and facts may carry copied attributes for BI scan speed.
7. **Q (tricky): When is denormalization a mistake?** A: Strict-consistency writes (payments), frequently-updated dimensions (high sync fan-out), or unmeasured "optimization" — if EXPLAIN doesn't show the win, you paid for nothing.
8. **Q: What does CQRS have to do with denormalization?** A: CQRS separates commands (normalized writes) from queries (denormalized read models); read models are projected/denormalized copies of the write side — the architectural form of denormalization.
9. **Q: What anomalies do you reintroduce?** A: Update (rename city across all orders), insert (partial facts), delete (losing the last redundant row hides data) — the exact ones 3NF removed, now controlled manually.
10. **Q: Materialized view vs denormalized column?** A: MV = precomputed query result, refreshed on schedule (Postgres `REFRESH ... CONCURRENTLY`); column = inline copy. MV is better for aggregates; column for per-row join elimination.
11. **Q (scenario): Twitter-style feed — normalized or denormalized?** A: Denormalized/eventual — feeds are read-heavy, hot, and staleness-tolerant; typically a cache/read model keyed by user storing precomputed post lists.
12. **Q: How is embedded JSON (Postgres JSONB / Mongo) denormalization?** A: It flattens child data into the parent row — reads fetch one row instead of N+1; updates to embedded data require rewriting the parent (write amplification, 4NF violation).
13. **Q (hard): You denormalized, then a rename caused mass drift. Fix?** A: Add a propagation trigger from source to copies; or move the volatile attribute back to the normalized side and keep only stable ones denormalized; or store the dimension id and join only for the rename case.
14. **Q: Does denormalization help analytics at scale?** A: Yes — that's the columnar/star-schema model: precomputed copies and wide rows let scans skip joins; aggregation happens at load time, not query time.
15. **Q: How do you decide the "hot 5%"?** A: Query profiling (pg_stat_statements, slow log): top latency×frequency queries; denormalize only the attributes/joins they touch; keep the rest normalized.
16. **Q (tricky): Is a cache (Redis) denormalization?** A: Conceptually yes — a copy of data for faster reads; the difference is it lives outside the DB, with its own invalidation. Denormalized columns are the "cache inside the table."
17. **Q: What's the correctness guarantee after denormalization?** A: None automatic — you must guarantee it (triggers, jobs, app logic). The system of record stays normalized; denormalized layers are projections.
18. **Q: When do you NEVER denormalize?** A: Money flows, inventory at checkout, unique-constraint-critical domains — places where stale/duplicated truth causes real harm; keep strict normalization + strong constraints.
19. **Q: Materialized views in Postgres?** A: `CREATE MATERIALIZED VIEW` stores the query result; refresh via `REFRESH MATERIALIZED VIEW CONCURRENTLY` (non-blocking) or plain `REFRESH`; indexes supported — a first-class denormalization tool.
20. **Q: Final judgment call: normalized vs denormalized in a systems-design interview?** A: Say: "Start normalized (3NF) for correctness; profile; denormalize the hot read paths with controlled propagation and bounded staleness; keep source of truth canonical." That's the senior answer.

## 14. Follow-Up Questions
1. **Q: What's the "eventual consistency" relationship?** A: Denormalized copies are eventually consistent by nature — drift window = propagation lag; you explicitly size it to the use case (dashboards tolerate minutes, checkout must not).
2. **Q: Star schema vs snowflake schema?** A: Star = denormalized dimensions (wide, one-level); snowflake = normalized dimensions (multi-level, more joins). Star wins read speed, which is why it dominates.
3. **Q: How do indexes interact with denormalization?** A: Indexes reduce per-join probe cost; denormalization removes the join entirely. You denormalize when even indexed joins are too slow (still n·log m).
4. **Q: Does columnar storage change the calculus?** A: Yes — columnar scans (Redshift, ClickHouse) read only needed columns and are so fast that wide denormalized rows become cheap; warehouses lean further into denormalization than OLTP.
5. **Q: Can triggers be replaced?** A: Yes — CDC pipelines (Debezium→read model), materialized-view refreshes, event sourcing; triggers are the in-DB simplest, pipelines scale better.

## 15. Coding Example
```sql
-- BEFORE: normalized join for the dashboard
SELECT c.city, SUM(o.total)
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.city;                      -- join per order row

-- AFTER: redundant column (denormalized)
ALTER TABLE orders ADD COLUMN customer_city TEXT;
UPDATE orders o SET customer_city = c.city FROM customers c WHERE c.customer_id = o.customer_id;
SELECT city, SUM(total) FROM orders GROUP BY city;   -- one table, no join

-- Propagation control: trigger keeps the copy fresh
CREATE FUNCTION sync_city() RETURNS trigger AS $$
BEGIN
  UPDATE orders SET customer_city = NEW.city
  WHERE customer_id = NEW.customer_id;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
CREATE TRIGGER trg_city AFTER UPDATE OF city ON customers
  FOR EACH ROW EXECUTE FUNCTION sync_city();

-- Alternative: materialized view (Precomputed summary)
CREATE MATERIALIZED VIEW city_totals AS
  SELECT c.city, SUM(o.total) AS total
  FROM orders o JOIN customers c ON c.customer_id=o.customer_id
  GROUP BY c.city;
CREATE INDEX ON city_totals(city);
REFRESH MATERIALIZED VIEW CONCURRENTLY city_totals;  -- nightly job
```
```python
# Read-model denormalization pattern (CQRS)
class OrderReadModel:
    def __init__(self, order_id, customer_name, customer_city, total): ...
# Written by a projection from the normalized source on change events;
# queries hit this row only -> no joins at read time.
```

## 16. Industry Usage
- **Data warehouses**: star schemas, wide fact tables, and pre-aggregated rollups are the industry norm — analytics is built on denormalization.
- **Read-heavy SaaS**: dashboards, leaderboards, and profile pages denormalize the hot attributes; normalized OLTP stays behind an API.
- **Postgres/MySQL**: materialized views, generated columns (`GENERATED ALWAYS AS (...)`), and triggers are the standard tooling; ORMs expose `has_many` embedded data.
- **CQRS/event sourcing** (e.g., banking read models): projections duplicate state by design; the write side stays normalized.
- **Columnar engines** (Snowflake, BigQuery, ClickHouse, Redshift): denormalized wide tables + columnar scans make even 10M-row GROUP BYs fast — the strongest argument for "denormalize for analytics."

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 24 (Denormalization for information retrieval / physical DB design).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 25.3 (physical design; denormalization).
- Kimball, R., *The Data Warehouse Toolkit*, Ch. 1–2 (star schemas as denormalization).
- PostgreSQL docs: CREATE MATERIALIZED VIEW, REFRESH MATERIALIZED VIEW CONCURRENTLY, CREATE TRIGGER.
- Fowler, M., *Patterns of Enterprise Application Architecture* (CQRS, read models).

## 18. Cheat Sheet
- Denormalization = reintroduce redundancy to kill joins/reads.
- Do it when: read-heavy + rare updates to the copied data + staleness OK + measured (EXPLAIN).
- Techniques: duplicate column, merge tables, materialized view, embedded JSON, star schema.
- Controls: triggers, refresh jobs, CDC, event projections.
- Costs: anomalies return, drift, disk, write amplification.
- NEVER for: money/inventory/unique-constraint-critical writes.
- Senior answer: normalize first, profile, denormalize the hot 5% with bounded staleness.
- CQRS/read models are the architectural denormalization.

## 19. Quiz
1. Denormalization trades for: a) write correctness b) read speed c) space d) both b and c → **d**
2. Safe denormalization requires: a) reads dominate b) rare updates c) staleness OK d) all → **d**
3. The anomaly that returns: a) update (rename city) b) none c) only FK d) only 1NF → **a**
4. Postgres precomputed query result tool: a) VIEW b) MATERIALIZED VIEW c) SEQUENCE d) FDW → **b**
5. Star schema = : a) normalized dimensions b) denormalized wide dimensions c) no facts d) 5NF → **b**
6. CQRS read models are: a) normalized b) denormalized projections c) triggers d) indexes → **b**
7. When to NEVER denormalize: a) dashboard b) payments/inventory c) analytics d) read model → **b**
8. Refresh that doesn't block reads: a) plain REFRESH b) CONCURRENTLY c) VACUUM d) nothing → **b**
9. First step before denormalizing: a) rename tables b) EXPLAIN/profile c) drop indexes d) add triggers → **b**
10. Drift control mechanisms: a) triggers b) jobs c) CDC d) all → **d**

## 20. Flashcards
- **Q: What is denormalization?** → **A:** Reintroducing redundancy to kill joins/reads.
- **Q: When is it safe?** → **A:** Read-heavy, rare updates, staleness OK, measured win.
- **Q: The cost?** → **A:** Anomalies return, drift, disk, write amplification.
- **Q: Main techniques?** → **A:** Duplicate columns, merged tables, materialized views, embedded JSON, star schemas.
- **Q: Drift control?** → **A:** Triggers, refresh jobs, CDC, event projections.
- **Q: NEVER denormalize when?** → **A:** Payments/inventory/unique-constraint-critical writes.
- **Q: What's a materialized view?** → **A:** Precomputed query result, refreshed on schedule.
- **Q: Senior judgment?** → **A:** Normalize first, profile, denormalize the hot 5% with bounded staleness.

## 21. Revision
Denormalization = **deliberate redundancy for read speed** — duplicate columns (`orders.customer_city`), merged tables, **materialized views**, embedded JSON, star schemas. Justify it by three conditions: **read-heavy, rarely-updated copied data, staleness tolerated** — and only after **EXPLAIN** shows joins/aggregation dominate. The costs are the **3NF anomalies returning** (rename a city → update every row) plus **drift**, so you add **controls**: triggers, `REFRESH MATERIALIZED VIEW CONCURRENTLY`, CDC/read-model projections. Never denormalize strict-consistency domains (payments, inventory at checkout). Interview answer: "start normalized, profile, denormalize only the hot read paths, keep a canonical source of truth, bound the staleness." That's the whole craft — choosing which photocopies to keep at the front desk.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is denormalization / when do you use it?" | 1–2 / 13 Q1–Q2 |
| "What's the trade?" | 13 Q3 |
| "Dashboard summing orders by city — fix?" | 13 Q4 |
| "How do you control drift?" | 13 Q5 / 15 |
| "Star schema normalized?" | 13 Q6 / 14 Q2 |
| "When is it a mistake?" | 13 Q7 |
| "CQRS read models?" | 13 Q8 |
| "Materialized views in Postgres?" | 13 Q19 |
