# Company-Specific DBMS Questions

> **TL;DR**: How DBMS rounds differ by employer — big-tech (breadth + distributed consistency + system design), finance/DB-reliant (strict SQL + normalization + data integrity + backup/recovery), data roles (patterns + optimization), startups (practical trade-offs + speed) — plus the company-specific question families to expect and how to target prep.

## 1. Why Does This Exist?
The same DBMS knowledge gets tested *differently* by different employers: a FAANG backend loop embeds database questions inside system design and asks about distributed consistency; a fintech asks strict transactional questions ("how do you guarantee no double-spend?"); a data-engineering track runs SQL pattern rounds; a startup asks "would you use Postgres or Mongo for this and why?" at whiteboard speed. This file exists to map your prep to the *test format* you'll actually face — because interview success is partly "knowing the subject" and partly "knowing the shape of the test." Understanding each company type's emphasis (breadth vs depth vs practicality vs correctness-paranoia) lets you weight the 8 parts correctly and rehearse the *delivery style* (EXPLAIN walks for DBRE, quick trade-off calls for startups, formal rigor for finance).

## 2. How Does It Work?
The file profiles four employer archetypes and their DBMS emphases:
1. **Big Tech / Platform (FAANG, Microsoft, Amazon, Google, Stripe-adjacent)**: breadth + distributed systems + system design. Emphasize Parts 04-08 (indexing, isolation, MVCC, CAP/PACELC, NoSQL, sharding), and the design skeleton (§2 of this chapter). Expect "design X's data layer", "explain MVCC", "CAP follow-ups".
2. **Finance / Payments / Insurance (fintech, banks, trading)**: correctness-first, transactional rigor, integrity, audit/recovery. Emphasize Parts 02-06 (constraints, normalization, ACID, isolation levels, deadlocks, recovery, backups/PITR). Expect "how do you prevent a race on a balance?", "what isolation level for transfers?", "design the ledger".
3. **Data Engineering / Analytics (data teams, warehouses)**: SQL patterns + optimization + warehouses. Emphasize Parts 07-08 (EXPLAIN, query tuning, columnar, partition pruning) and the SQL-challenge chapter. Expect LeetCode SQL, "optimize this 10-minute query".
4. **Startups / Product companies**: speed + practical trade-offs + polyglot judgment. Emphasize Part 08 §5 (the decision guide) + caching + "MVP with Postgres" pragmatism. Expect "which DB for this feature?", "JSONB vs Mongo", "how would you migrate".
Plus cross-cutting **company-specific question families** (the recurring specifics — e.g., Amazon's "why Postgres/Aurora", Uber's geo-indexing, Stripe's ledger/money movement, Google's Spanner story, Apple's consistency posture) to research per target.

## 3. When Is It Used?
- When tailoring prep for a specific target company (list its DBMS emphasis + family questions).
- When choosing *which parts to deep-dive* based on role (backend vs data vs DBA vs startup).
- For mock interviews with the right format (timed SQL for data roles; design walks for big-tech; whiteboard trade-offs for startups).
- To anticipate the *style* of follow-ups (big-tech probes CAP/PACELC; finance probes the transaction boundary; data roles probe EXPLAIN).
- Interviews: "explain MVCC", "what isolation level for payments", "why did this query get slow", "design the ledger", "Postgres vs Mongo", "how do you back this up?"

## 4. Why Wasn't Another Approach Chosen?
- *Generic prep only*: universal depth is necessary but not sufficient — format awareness wins points (e.g., a finance interview that *says* "transactional correctness" while you're pitching NoSQL would sink). The file adds the *test-shape* dimension.
- *Memorizing company question lists*: specific questions leak online but change; the *archetype* (why finance tests what it tests) predicts the new ones. Profile-based prep survives question rotation.
- *Practicing only answers*: delivery matters — finance wants rigor + numbers; startups want speed + judgment; data roles want clean executable SQL. The file covers *how* to deliver, not just what.
- *Ignoring role differences*: "DBMS interview" at a data-eng role ≠ at a backend role; the file separates the three major role tracks.

## 5. Intuition
Different employers are different **interviewers with different grading rubrics** — like taking the same exam in different *languages*: the syllabus is one thing, the format another. Big-tech grades on *systems reasoning*: can you take a product and walk through the distributed data design (breadth, Part 08/design chapter). Finance grades on *correctness discipline*: can you reason under worst case, prove the transaction boundary, name the isolation level and the recovery story (Part 05/06 rigor). Data roles grade on *craft*: can you write and optimize SQL cold (the SQL chapter). Startups grade on *decision speed*: can you pick a tool, justify it in two sentences, and start (Part 08 §5). The same person, same knowledge — but weighted differently. Prep correctly = know the syllabus *and* practice in the language of the target.

## 6. Real-World Analogy
**The same subject, different professional exams.** A pilot's knowledge is one body; but the *FAA written* tests procedures and regulations (correctness, like finance), an *airline technical* probes systems and failure analysis (like big-tech), and a *charter-company* interview checks you can fly today's plane with today's weather (like a startup). You don't study "aviation" differently — you study the *emphasis*: the FAA candidate drills FAR/AIM verbatim; the airline candidate drills QRH procedures and decision-trees; the charter pilot drills the preflight and judgment calls. This file is the *exam-specific study guide* for DBMS: it keeps the same syllabus but tells you which chapters carry the weight, which question families to expect, and how to phrase answers so the grader recognizes the skill they're scoring.

## 7. Formal Definition
Company-specific DBMS prep = (universal syllabus) × (role/archetype weighting) × (format: timed SQL / design walk / whiteboard trade-off / correctness-grilling) × (company family questions). Archetype weightings: big-tech (Parts 04-08 + design + distributed consistency); finance (Parts 02-06 + integrity/recovery + the transaction boundary); data (Parts 02, 07-08 + SQL patterns + optimization); startup (Part 08 §5 + caching + JSONB-vs-document + migration pragmatics). Format-aware delivery: big-tech = structured walk with trade-off narration; finance = prove the worst case + name the isolation/durability knob; data = clean, executable, index-aware SQL with EXPLAIN mention; startup = decide fast, justify in two sentences, offer the fallback.

## 8. Example
**"Explain MVCC" — four delivery styles:**
- **Big-tech**: "MVCC gives snapshot isolation: each version carries xmin/xmax transaction ids; a reader sees a consistent snapshot via the visibility map; writers don't block readers. Postgres keeps old versions in-page cleaned by VACUUM; this trades bloat for read-write concurrency. A follow-up: it permits write skew — which SERIALIZABLE/SSI catches." (breadth + mechanism + follow-up awareness) → Part 05 Ch2/3
- **Finance**: "For transfers I use SERIALIZABLE or at least REPEATABLE READ with explicit SELECT ... FOR UPDATE on the account rows — MVCC's snapshot semantics must not let two concurrent transfers read the same balance. I'd add a version column and optimistic retry; I'd also confirm the durability path (WAL fsync) because snapshot isolation alone doesn't guarantee no lost commits." (correctness + the boundary) → Part 05/06
- **Data**: "With MVCC, long-running analytics transactions see a stable snapshot, so my warehouse ETL can read consistently without blocking production writers — but I must watch VACUUM pressure and bloat on hot-update tables; I check pg_stat_user_tables for dead tuples." (operational/performance angle) → Part 05/07
- **Startup**: "Postgres gives us MVCC snapshot isolation for free, which is why we run everything on it — readers never block writers and we don't need Mongo for that. If we hit hot-row contention later, we'd look at batching, not a migration." (speed + judgment + tool choice) → Part 08 §5
Same knowledge, four formats — the archetype dictates the *weight of each clause*.

## 9. Internal Working
To target a company: (1) identify the archetype(s) by company + role; (2) re-weight the syllabus (which parts deserve the deep-dive hours); (3) rehearse the format (timed SQL, design walk, whiteboard, grilling); (4) research the *family questions* (see Section 13 — the recurring, company-specific DBMS themes); (5) run mock interviews in that format; (6) for the top 2 targets, draft the two-sentence "house answers" (e.g., "why Postgres/Aurora at Amazon?"). The "trap" to avoid: treating every DBMS interview as the same format — a finance-style grilling answered in big-tech breadth reads as hand-wavy; a startup speed-question answered with a 5-minute design walk reads as over-engineering.

## 10. Time Complexity
- Syllabus mastery is fixed cost (~the 8 parts).
- Format tailoring: ~2-4 hours per target company (weighting + family questions + mock).
- The payoff: the *same* preparation produces outsized returns when the delivery matches the grader's rubric — format mismatch is where otherwise-strong candidates lose points.
- Priority: master the syllabus first, tailor format second; tailoring without syllabus is empty theater.

## 11. Advantages
- **Format-aware delivery**: matches what the grader is actually scoring.
- **Efficient weighting**: spend deep-dive hours where the target tests depth.
- **Family-question readiness**: the recurring specifics are pre-researched per archetype.
- **Anticipates follow-ups**: each archetype's probes (CAP, transaction boundary, EXPLAIN, tool choice) are known.
- **Portable**: the four-archetype model covers most employers; individual companies slot in.

## 12. Disadvantages
- **Archetypes are approximations**: a specific team within a company can vary wildly; always verify the actual role.
- **Company question lists rot**: specifics change; the *profile* stays, so don't memorize lists exclusively.
- **Can encourage over-tailoring**: don't skip universal depth (Part 05's isolation ladder, Part 07's EXPLAIN) for format tricks — most interviews still test breadth.
- **Requires up-front research**: the family questions demand time on the company/team.

## 13. Interview Questions
1. **Q: (Big-tech) Explain CAP with a real distributed system example.** A: DynamoDB (eventual + availability during partitions) vs Spanner (consistency-first, synchronous). During a partition, DynamoDB answers with possibly-stale data; Spanner may reject writes. PACELC adds the latency/consistency trade when no partition. → Part 08 §1
2. **Q: (Big-tech) Design the data layer of a social feed (or newsfeed).** A: Fan-out on write + cached KV timelines + graph for follow relations + warehouse for analytics; timeline eventual, likes LWW-OK; hot celebrities special-cased. → §2 of this chapter
3. **Q: (Finance) What isolation level for a money transfer and why?** A: SERIALIZABLE (or REPEATABLE READ + explicit `SELECT ... FOR UPDATE` on both account rows) to prevent lost updates and write skew; verify both debits+credits atomic (one transaction), add optimistic versioning for contention, and confirm WAL durability before COMMIT. → Part 05/06
4. **Q: (Finance) How do you detect and prevent double-spend / duplicate payments?** A: Unique constraint on a payment idempotency key (`client_ref + amount`) — the DB enforces it; plus the transaction boundary around the ledger insert; plus idempotent retries (same key → same result). → Part 02/05
5. **Q: (Finance) Design a double-entry ledger.** A: `ledger_entries(id, account_id, entry_type, amount, ref, created_at)` with a transaction inserting both the debit and credit rows atomically (sum of amounts = 0 invariant); unique index on (ref, entry_type) for idempotency; account balances derived or cached with constraints; audit trail = append-only with timestamps. → Part 02/05/06
6. **Q: (Finance) How do you back up and recover a production DB with RPO=0?** A: WAL archiving (continuous) + base backups + point-in-time recovery; synchronous replication or quorum for RPO=0; test restores regularly; document RTO. → Part 06 Ch3
7. **Q: (Data) Optimize a query that takes 10 minutes on a 1B-row table.** A: EXPLAIN → check for full scans (missing index), bad join order (stale stats → ANALYZE), spills (work_mem), then add the right (composite/covering) index, ensure partition pruning, or move to a columnar/warehouse if it's analytic. → Part 07
8. **Q: (Data) Write SQL: monthly retention cohort.** A: Join signups to activity on month offsets; `COUNT(DISTINCT user) GROUP BY signup_month, month_offset` (or a pivot); the trick is the self-join/cross join on month and `DISTINCT` counting. → §3 of this chapter
9. **Q: (Data) Why is this `GROUP BY` over a billion rows slow, and what's the fix?** A: Row-store full scan reading all columns; fix: columnar store (read only needed columns), partition by time, materialized pre-aggregates, or a covering index for the group-by keys. → Part 07/08
10. **Q: (Startup) Postgres vs MongoDB for our new feature — decide now.** A: Ask one question each: do we need joins/transactions/ad-hoc SQL (→ Postgres, likely default) and is the schema truly variable + reads per-object (→ Mongo)? For most MVPs: Postgres + JSONB; choose Mongo only if the whole data model is document-shaped *and* we need horizontal write scale. → Part 08 §5
11. **Q: (Startup) How do we scale read traffic without a big migration?** A: Cache-aside (Redis) for hot reads, read replicas, proper composite/covering indexes verified with EXPLAIN, connection pooling — order: indexes → cache → replicas; sharding is the last resort. → Part 07 §3/08 §5
12. **Q: (Startup) JSONB vs a separate document store — when do you actually move?** A: Start with JSONB (indexable via GIN, joins with relational tables). Move to a document store when document-heavy reads + write scale demand distributed partitioning that Postgres sharding doesn't serve. → Part 08 §5
13. **Q: (Amazon-adjacent) Why do teams default to Aurora/Postgres, and when does DynamoDB win?** A: Postgres/Aurora: joins, transactions, SQL, managed; DynamoDB wins for by-key O(1) workloads at serverless scale (sessions, metadata, leaderboards) where relational generality is unused and single-digit-ms key reads with seamless scale matter. → Part 08 §2
14. **Q: (Google-adjacent) What does Spanner buy you and what does it cost?** A: SQL + horizontal scale + strong consistency (TrueTime-based external consistency + Paxos replication). Cost: consensus latency, complexity, operations; you pay it only when global strong transactions are a hard requirement. → Part 08 §5
15. **Q: (Uber-adjacent) How do you serve "find cars near me"?** A: Geo-indexing (PostGIS/geohash + a spatial index, or a geohash-as-shard-key in a KV), TTL on driver pings (stale if >5s), caching of the grid; match is transactional state (driver assigned exactly once — unique constraint on the assignment). → Part 04/08
16. **Q: (Apple-adjacent) Consistency posture for a consumer sync feature?** A: Eventual consistency with versioned conflict resolution (vector clocks / last-write-wins per field), per-user strong reads for their own writes, and the sync engine resolving merges — the "iCloud model". → Part 08 §1
17. **Q: (Stripe-adjacent) What makes payments data different from typical web data?** A: Money is *global transactional state*: no LWW, no eventual, idempotency keys, immutable append-only ledger entries, isolation (SERIALIZABLE or careful locking), and durable WAL before acknowledgment. The DBMS answer must never sacrifice correctness for scale. → Part 05/06/08
18. **Q: (Any) You have 30 minutes to explain one database topic deeply — which and why?** A: MVCC/Isolation (Part 05): it combines the isolation ladder, lock vs versioning, write skew, and connects to real engines — breadth + depth in one story, and it's the most-asked family. → Part 05

## 14. Follow-Up Questions
1. **Q: "Your finance answer assumed one node. What if you must shard the ledger?"** → Global-state tension: prefer not to shard money; if forced, NewSQL (distributed transactions) or partition-by-account with per-account serialization (Part 08 §5).
2. **Q: "Your cache design — what happens on miss/write?"** → Cache-aside + delete-on-write + TTL + single-flight; never cache authoritative state (Part 08 §2).
3. **Q: "Make the data answer match the company's known stack."** → Name their actual products (Aurora, DynamoDB, Spanner, PostGIS, Redis) and map your generic answer onto them.
4. **Q: "Two sentences, why did you choose that engine?"** → Practice the compressed justification — archetype-appropriate speed.

## 15. Coding Example
```sql
-- Finance: idempotent payment + transaction boundary (the "double-spend" answer)
CREATE TABLE payments (
  id BIGSERIAL PRIMARY KEY,
  idempotency_key text NOT NULL UNIQUE,      -- DB-enforced dedupe
  account_id BIGINT NOT NULL REFERENCES accounts(id),
  amount NUMERIC(19,2) NOT NULL CHECK (amount > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
BEGIN;
  SELECT ... FROM accounts WHERE id = :acct FOR UPDATE;    -- lock balance
  -- validate sufficient balance; raise/rollback otherwise
  INSERT INTO payments (idempotency_key, account_id, amount) VALUES (:key, :acct, :amt);
  UPDATE accounts SET balance = balance - :amt WHERE id = :acct;
  UPDATE accounts SET balance = balance + :amt WHERE id = :recipient;
COMMIT;   -- single transaction; WAL fsynced before ack (durability)
```
```sql
-- Data role: retention cohort (monthly)
WITH signups AS (
  SELECT user_id, date_trunc('month', created_at) AS m0
  FROM users
),
active AS (
  SELECT user_id, date_trunc('month', created_at) AS m
  FROM sessions GROUP BY user_id, date_trunc('month', created_at)
)
SELECT s.m0,
       COUNT(DISTINCT s.user_id) AS cohort,
       COUNT(DISTINCT CASE WHEN a.m = s.m0 THEN s.user_id END) AS m0,
       COUNT(DISTINCT CASE WHEN a.m = s.m0 + INTERVAL '1 month' THEN s.user_id END) AS m1,
       COUNT(DISTINCT CASE WHEN a.m = s.m0 + INTERVAL '2 months' THEN s.user_id END) AS m2
FROM signups s LEFT JOIN active a ON a.user_id = s.user_id
GROUP BY s.m0 ORDER BY s.m0;
```

## 16. Industry Usage
- **Big tech**: DBMS questions embedded in system design; distributed consistency (CAP/PACELC, Spanner, DynamoDB) is the signature; Part 08 + the design skeleton dominate.
- **Finance/payments**: transaction boundary, isolation, idempotency, ledger modeling, recovery — the "correctness-paranoia" interview; Parts 02/05/06.
- **Data roles**: SQL pattern rounds + optimization + warehouse awareness; Parts 07/08 + the SQL chapter.
- **Startups**: practical trade-offs and speed ("would you use Postgres for this?"); Part 08 §5.
- **DBA/DBRE roles**: EXPLAIN walks, backups/PITR, bloat/vacuum, replication — operational depth across Parts 06/07.

## 17. References
- Company engineering blogs (the "house answers" source): Amazon/AWS (DynamoDB, Aurora), Google (Spanner paper), Stripe (ledger/money movement), Uber (geo/PostGIS, schemaless), Meta (fan-out/timeline), Apple (iCloud sync).
- The papers behind the families (as cited in Part 08 §1): Dynamo, Spanner, Bigtable, Cassandra.
- Part 05/06/07/08 references for the depth each archetype leans on.
- LeetCode/DataLemur for the data-role SQL format.

## 18. Cheat Sheet
- Four archetypes: big-tech (breadth + distributed), finance (correctness + integrity + recovery), data (patterns + optimization), startup (speed + trade-offs + tool choice).
- Weight: big-tech → Parts 04-08 + design; finance → Parts 02-06; data → Parts 02/07-08 + SQL; startup → Part 08 §5 + cache.
- Format: big-tech = structured walk; finance = prove worst case + name isolation/durability; data = clean index-aware SQL + EXPLAIN; startup = two-sentence justification.
- Money data rules (any company): no LWW, idempotency keys, single transaction boundary, WAL durability before ack, serializable-or-for-update.
- House answers to draft: "why Postgres/Aurora" (AWS), "why Spanner" (Google), "why PostGIS" (Uber), "idempotency + ledger" (Stripe), "versioned sync" (Apple).
- Common family questions: MVCC, isolation for money, CAP example, design a feed/ledger, optimize a 10-min query, Postgres vs Mongo.
- Trap: format mismatch (rigor for startup questions, breadth for finance grilling).

## 19. Quiz
1. Finance interviews weight: a) NoSQL b) correctness/recovery c) caches d) graph → **b**
2. Big-tech signature question: a) backup script b) design + distributed consistency c) pivot SQL d) DDL → **b**
3. Data-role round is typically: a) SQL patterns b) deadlock theory c) CAP d) ORMs → **a**
4. Payments need: a) LWW b) idempotency + transaction boundary c) eventual d) fan-out → **b**
5. Startup DBMS questions want: a) 5-min walkthrough b) fast justified decision c) formal proof d) histogram math → **b**
6. RPO=0 requires: a) async replica b) sync/quorum + WAL c) cache d) vacuum → **b**
7. "Why Postgres/Aurora" is a house answer for: a) Uber b) AWS c) Stripe d) Apple → **b**
8. The most-asked deep topic to prepare: a) 4NF b) MVCC/isolation c) hash cost d) R-tree → **b**

## 20. Flashcards
- **Q: Big-tech DBMS weight?** → **A:** Parts 04-08 + system design + distributed consistency.
- **Q: Finance DBMS weight?** → **A:** Integrity, isolation, idempotency, recovery (Parts 02-06).
- **Q: Data-role format?** → **A:** Timed SQL patterns + optimization + EXPLAIN.
- **Q: Startup format?** → **A:** Fast justified tool decisions (Part 08 §5).
- **Q: Payments rule?** → **A:** Idempotency key + single transaction + durable ack.
- **Q: RPO=0?** → **A:** Sync/quorum replication + continuous WAL archiving.
- **Q: Most common deep topic?** → **A:** MVCC / isolation levels.
- **Q: Prep priority?** → **A:** Syllabus first, then format tailoring per target.

## 21. Revision
The syllabus is universal; the *test* differs. Big-tech = breadth + distributed consistency + the design skeleton (Parts 04-08). Finance = correctness discipline — transaction boundary, isolation for money, idempotency, ledger modeling, recovery/PITR (Parts 02-06). Data roles = executable, optimized SQL + EXPLAIN (Parts 07-08 + SQL chapter). Startups = fast, justified engine choices (Part 08 §5) + caching. Draft the house answers for your targets, rehearse the format (not just the content), and always keep MVCC/isolation as the deep-topic ace.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "CAP with a real system" (big-tech) | 2, 13 |
| "Isolation level for a transfer" (finance) | 2, 13 |
| "Design the ledger" (finance) | 8, 13 |
| "Backup with RPO=0" (finance) | 8, 13 |
| "Optimize a 10-min query" (data) | 8, 13 |
| "Retention cohort SQL" (data) | 8, 15 |
| "Postgres vs Mongo, decide now" (startup) | 4, 13 |
| "Why Postgres/Aurora vs DynamoDB" (AWS) | 13 |
| "What does Spanner buy/cost" (Google) | 13 |
| "Find cars near me" (Uber) | 13 |
