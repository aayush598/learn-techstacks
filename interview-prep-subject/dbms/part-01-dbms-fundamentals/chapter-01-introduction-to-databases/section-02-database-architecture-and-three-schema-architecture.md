# Database Architecture and Three-Schema Architecture

> **TL;DR**: The three-schema architecture splits a database into external (views), conceptual (logical model), and internal (physical storage) levels so that changing one level never breaks the levels above it — this layered isolation is what makes data independence possible.

## 1. Why Does This Exist?
Before layered schemas, an application was bound to one file layout: change a file's record order or add a field and every program had to be rewritten. The three-schema architecture exists to **decouple** (a) what individual users see, (b) what the whole organization logically knows, and (c) how the data physically exists on disk. Its purpose is *data independence*: let the physical storage evolve (SSD→different engine, index changes) and the logical design evolve (add columns, split tables) **without rewriting applications**. It exists because software survives longer than storage layouts, and only a strict separation of levels guarantees that.

## 2. How Does It Work?
The architecture defines three levels and the *mappings* between them:
1. **External level** — views tailored to each user/application; a user only sees their slice.
2. **Conceptual level** — the whole community's logical view: all entities, attributes, relationships, constraints, in one model (the ER/relational schema).
3. **Internal level** — physical storage description: file organization, indexes, page sizes, compression, data structures (B+ trees, heaps, hash files).
Two mappings translate between adjacent levels: **external→conceptual** and **conceptual→internal**. A query written against a view is mapped down to the conceptual model, then translated into physical access operations against the internal layout. A *DBA* owns the conceptual and internal schemas; *end-users* only ever see external views.

## 3. When Is It Used?
- **Every RDBMS**: Postgres, MySQL, Oracle, SQL Server all implement external (views, schemas), conceptual (tables with constraints), internal (tablespaces, indexes, storage engines).
- **Multi-team enterprises**: sales, HR, and finance each get different *views* over the same customer table — the external level in production.
- **Schema migration**: when a column is renamed or a table is split, an updatable *view* preserves old application queries — logical data independence in practice.
- **Physical tuning**: a DBA changes an index or moves a table to a faster tablespace with zero application impact — physical data independence in practice.
- **Security**: hiding salary columns from most users is implemented as external views over the conceptual schema.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: no levels — apps talk to files directly (pre-1970).** Rejected: any storage or schema change ripples through all code; no sharing, no security boundaries.
- **Alternative: only two levels (logical + physical).** Rejected because every user/application needs a tailored, secured slice; without the external level you can't give "finance sees only balance" without copying data. SQL's *views* and authorization both need the external layer.
- **Alternative: "one giant view" for everyone.** Rejected: leaks sensitive columns, couples all apps to one global model, and breaks when two teams need different granularity (e.g., one needs customer + address combined, another wants them separate).
- **Why three and not more?** Three is the *minimal* set that cleanly separates "user", "logical organization", and "physical storage". More levels add mapping cost without new independence benefits. ANSI/X3-SPARC standardized exactly three.

## 5. Intuition
Think of a **restaurant**. The *external level* is the menu — diners see a curated slice (starters, mains, desserts), tailored and formatted for them; they never see the kitchen. The *conceptual level* is the chef's master recipe book — the complete, consistent set of recipes the whole restaurant shares. The *internal level* is the kitchen itself — how ingredients are stored, in which fridges, which pans are used, how fast dishes can be plated. The diner who asks for "the grilled salmon" (external) is mapped through the recipe (conceptual) to actual fridge-stock and stove work (internal). If the kitchen moves from gas to induction (internal change), the menu and recipes don't change at all. If recipes are revised (conceptual change), diners still order by the menu. Only the *mapping* adapts.

## 6. Real-World Analogy
An **airport** with three layers: the departure board (external) — each airline shows its own flights, filtered and formatted per airline; the flight schedule database (conceptual) — the single authoritative set of all flights, gates, crews for the whole airport; the physical airport (internal) — runways, gates, terminals, baggage belts. When the airport repaves runway 2 (internal change), the departure board and schedule don't change. When airlines renumber flight numbers (conceptual change), boards are updated by mapping, not by rewriting every sign. The *mapping* is what absorbs change.

## 7. Formal Definition
ANSI/X3-SPARC (1975) proposed the **three-schema architecture**: (1) **External schema (view level)** — the description of each user's view of the database; (2) **Conceptual schema (logical level)** — the community-wide description of the database structure, independent of storage; (3) **Internal schema (physical level)** — the description of the physical storage structures. The two mappings — *external/conceptual* and *conceptual/internal* — transform requests between levels. **Logical data independence** = immunity of external schemas to changes in the conceptual schema. **Physical data independence** = immunity of the conceptual schema to changes in the internal schema. (Elmasri & Navathe Ch. 2; Silberschatz Ch. 1.2.)

## 8. Example
University DB with a `Student` table containing `(id, name, gpa, salary_hint)`. 
- **Internal**: rows stored in a heap file `student.dat`, with a B+ tree index on `id`, pages of 8 KB, `gpa` compressed.
- **Conceptual**: relation `Student(id INT PK, name VARCHAR, gpa NUMERIC, salary_hint INT)` with constraint `gpa BETWEEN 0 AND 4`.
- **External**: two views — `Registrar_View(id, name, gpa)` for academics, `Finance_View(id, salary_hint)` for billing. A registrar querying `gpa` never sees `salary_hint`; a billing query never touches `gpa`.
Now the DBA replaces the heap with a clustered index on `id` (internal change) — nothing above changes (physical independence). Later the university renames `name` → `full_name` in the conceptual schema but keeps a view that still exposes `name` (logical independence) — the registrar's app keeps working.

## 9. Internal Working
1. User runs `SELECT gpa FROM Registrar_View WHERE id=101;` (external level).
2. The **external/conceptual mapping** translates the view reference into the conceptual relation `Student` and the attribute `gpa`.
3. The optimizer builds a plan against the **conceptual schema** — it doesn't care about storage yet.
4. The **conceptual/internal mapping** selects access methods: index on `id` → B+ tree seek → fetch the page(s) containing `id=101`.
5. The buffer manager reads the page from disk/cache; the storage manager projects out `gpa`; the row is returned up through the levels.
6. Any schema change at one level only requires updating the *mapping*, not rewriting the queries at higher levels — that is precisely the independence the architecture buys.

## 10. Time Complexity
- Mappings are logical, not computational — overhead is negligible (compiled into the query plan).
- The *storage* layers underneath have real costs: B+ tree point lookup **O(log_f n)**, full scan **O(n)**, index update **O(log_f n)** per write.
- View materialization (if a view is materialized): O(size of view) to refresh; non-materialized views add only a small rewrite cost (a few percent) since they just inline the defining query.

## 11. Advantages
- **Data independence** (logical + physical) — the core payoff; applications survive schema and storage evolution.
- **Security** — external views hide columns/rows per user; access control at the view level.
- **Centralized administration** — one conceptual schema, one DBA team, consistent constraints.
- **Tailored interfaces** — each application gets exactly the shape of data it needs, even over the same tables.
- **Support for legacy apps** — old apps keep their old views after migrations.
- **Standardized by ANSI/X3-SPARC** — taught and implemented everywhere, so the vocabulary transfers across DBMS products.

## 12. Disadvantages
- **Mapping overhead** — every query crosses one or two mappings; extra indirection can cost small performance.
- **Complexity** — three schemas + two mappings + view maintenance is hard to design and explain to non-DBAs.
- **Performance mismatch** — a user's convenient view may map to expensive joins; the DBA must balance ease vs speed.
- **Not fully realized** — real DBMSs implement the spirit (views, catalog, storage layers) but not literally three separately maintained schemas; the "pure" architecture is an ideal.
- **View update problems** — updates through views are restricted; you can't always push writes down through a mapping (e.g., aggregate views).

## 13. Interview Questions
1. **Q: Name the three levels of the three-schema architecture.** A: External (view level), Conceptual (logical level), Internal (physical level), plus the two mappings between them. It was proposed by the ANSI/X3-SPARC committee in 1975.
2. **Q: What is the purpose of the three-schema architecture?** A: Data independence — to decouple user applications from logical structure and from physical storage, so changes at any level don't force changes at higher levels.
3. **Q: What is logical data independence?** A: The external schemas (views) are immune to changes in the conceptual schema. Example: renaming a column in the base table but exposing it under the old name via a view.
4. **Q: What is physical data independence?** A: The conceptual schema is immune to changes in the internal (storage) schema. Example: replacing a heap file with a B+ tree index, or moving to a new engine, without touching table definitions or applications.
5. **Q: Who sees which level?** A: End-users/applications see external views; the whole organization shares the conceptual schema; the DBA owns and maintains the conceptual and internal schemas. Users never interact with the internal level.
6. **Q (tricky): Which level stores the index metadata?** A: Indexes are part of the *internal* level — the physical access structures. But the *description* of those indexes (catalog rows) lives in the system catalog, which itself is managed through the conceptual/internal layers. Don't confuse the index's existence with its metadata.
7. **Q: What is a view, and at which level does it live?** A: A view is a virtual table defined by a query over base tables; it lives at the *external* level. It's the primary tool for implementing the external schema and security.
8. **Q (scenario): Ops adds a composite index on (dept_id, salary). The app and queries don't change at all. Which independence is this?** A: Physical data independence — the storage/access-structure layer changed, and the conceptual schema and applications were unaffected.
9. **Q (production): Your migration renames `students.name` to `students.full_name`. Hundreds of apps break. How do you save them?** A: Create a view `students` exposing the old column names that maps to the new table. Old apps keep querying `students.name` (external level) while the conceptual schema changes — logical data independence in practice. (Updatable views make writes work too.)
10. **Q: Why can't we just have one schema?** A: Because then every user shares one global structure (no security, no tailored slices) and every storage change breaks every app (no independence). The external level gives per-user views; the internal level absorbs storage churn.
11. **Q (tricky): Is a clustered index part of the conceptual schema?** A: No. Clustered vs non-clustered, page size, and file organization are *internal* (physical) concerns. The conceptual schema is only tables, attributes, types, and constraints. This is a common place candidates mix up levels.
12. **Q: What is the difference between a view and a base table?** A: A base table physically stores data; a view is a *virtual* table computed from a query — it stores no data itself (unless materialized), just the defining query. Changes to base tables are reflected in the view automatically.
13. **Q: How does the three-schema architecture relate to the system catalog?** A: The catalog (data dictionary) stores the descriptions of all three schemas and the mappings — it's the metadata that makes the architecture self-describing and lets the DBMS translate between levels.
14. **Q (production): Should you materialize a view?** A: Materialize when the view is queried often, expensive to recompute, and the underlying data changes rarely (or you can live with staleness). Otherwise keep it virtual — avoids storage and staleness. Engines support it as a trade-off knob.
15. **Q: What's the difference between an external schema and a schema in Postgres?** A: Two different meanings. The three-schema "external schema" is a view-level description. A Postgres *schema* is a namespace holding tables/views — closer to the conceptual layer. Name the level you mean.
16. **Q (hard): If a DBMS is NoSQL, does the three-schema architecture apply?** A: Loosely. Document stores have a conceptual-ish level (collections) and internal level (BSON files, shards) but typically *no* explicit external view layer — the API *is* the view. The architecture's value (independence) applies less because schema is often flexible/implicit.
17. **Q: What does the external/conceptual mapping do?** A: It translates a user's view-level query into a query against the conceptual schema (renaming, projecting, joining as needed by the view definition).
18. **Q: What does the conceptual/internal mapping do?** A: It translates logical operations (scan relation R, select attribute A) into physical operations (which file, which index, which pages, in what order), chosen by the optimizer.
19. **Q (tricky): Can physical data independence be perfect?** A: No — storage changes sometimes affect query *performance* noticeably (e.g., dropping an index changes a plan from 1 ms to 5 s). Independence means correctness doesn't break; it does *not* guarantee performance doesn't change.
20. **Q (scenario): An interviewer asks "your schema changed and your app broke — which layer failed?"** A: The external/conceptual mapping failed — the app depended on a conceptual schema detail that changed; if the app used only a well-designed external view, it would have been insulated. So the lesson is: apps should bind to views, not base tables.

## 14. Follow-Up Questions
1. **Q: Why is ANSI/X3-SPARC called "three-schema" not "three-tier"?** A: Schema = description level; tier = deployment topology. The three-schema is a *conceptual* layering; three-tier is a *physical* distribution (client/app/db). Don't conflate.
2. **Q: Does SQL have a keyword for creating external schemas?** A: `CREATE VIEW` is the external-level tool; `CREATE SCHEMA` (Postgres/Oracle) creates a namespace, which is different. Views are the practical external schema.
3. **Q: How do ORMs (Hibernate/Prisma) relate to this architecture?** A: An ORM maps objects (external view of the app) onto tables (conceptual). It's a *custom external schema* — which is why ORM-heavy apps still break on schema changes: their mapping is the external/conceptual mapping.
4. **Q: Which is more common in production: materialized or virtual views?** A: Virtual views are far more common (Postgres uses them heavily; BigQuery does too). Materialized views appear in data warehouses (Snowflake, Postgres MATVIEW) where recomputation cost is justified.
5. **Q: Can you update data through a view?** A: Only if the view is *updatable* (maps 1:1 to one base table's columns, no aggregation/DISTINCT). Postgres automatically makes simple views updatable; others need triggers/instead-of rules.

## 15. Coding Example
```sql
-- External level: a view (the external schema for the registrar app)
CREATE VIEW registrar_view AS
SELECT id, name, gpa FROM student;   -- hides salary_hint

-- Registrar queries the view; internally maps to the conceptual table
SELECT name FROM registrar_view WHERE gpa > 3.5;

-- Physical data independence: storage changes, apps unaffected
CREATE INDEX idx_student_id ON student(id);       -- internal level change
CLUSTER student USING idx_student_id;             -- reorganize pages: internal

-- Logical data independence: rename column, keep old name via view
ALTER TABLE student RENAME COLUMN name TO full_name;
CREATE VIEW student AS SELECT id, full_name AS name, gpa FROM student;
```

```python
# Simulating the mapping layers in Python
external = {"name", "gpa"}          # what registrar sees
conceptual = {"id": "int", "name": "str", "gpa": "float", "salary_hint": "int"}
internal = {"file": "student.dat", "index": "btree(id)", "page_size": 8192}

def map_external_to_conceptual(cols):     # external -> conceptual
    return {c for c in cols if c in conceptual}

def execute(cols):
    mapped = map_external_to_conceptual(cols)
    # ... then optimizer picks internal access method (index vs scan)
    return f"executed scan for {sorted(mapped)} on {internal['file']}"

print(execute(external))   # uses only name, gpa; salary_hint never accessed
```

## 16. Industry Usage
- **Every major RDBMS** implements the three levels: Postgres has `VIEW`s + `pg_catalog` + storage/tablespaces; Oracle has *synonyms* and *views* over *segments*; SQL Server has *schemas* and *partitioned tablespaces*.
- **Banking core systems** are architected so regulators see one view, tellers another, auditors another — the external level is a compliance requirement, not an option.
- **Schema migration tools** (Flyway, Liquibase, Prisma migrations) succeed only because the internal layer absorbs storage churn while views absorb schema churn — that's data independence sold as a feature.
- **Snowflake's separation of storage and compute** is a physical-layer change that left customers' SQL untouched — a billion-dollar product built on physical data independence.
- **Data warehouses** materialize views (Snowflake `MATERIALIZED VIEW`, Postgres `MATERIALIZED VIEW`) precisely because the mapping from external to conceptual is too expensive to recompute per query.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 2 (Database System Concepts and Architecture).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Sec. 1.2 (View of Data).
- Tsichritzis, D. & Klug, A., "The ANSI/X3/SPARC DBMS Framework", AFIPS, 1978.
- PostgreSQL Documentation, Views: https://www.postgresql.org/docs/current/tutorial-views.html
- MySQL Documentation, Views: https://dev.mysql.com/doc/refman/8.0/en/create-view.html

## 18. Cheat Sheet
- 3 levels: External (views) → Conceptual (tables+constraints) → Internal (files+indexes).
- 2 mappings: external↔conceptual, conceptual↔internal.
- Logical independence = external immune to conceptual changes (views).
- Physical independence = conceptual immune to internal changes (indexes/storage).
- Views = the external-level tool; materialized views trade freshness for speed.
- Catalog stores all three schemas + mappings (self-description).
- ANSI/X3-SPARC 1975; Codd's relational model predates it (1970).
- Apps should bind to views, not base tables.

## 19. Quiz
1. The user-facing level of the three-schema architecture is: a) internal b) conceptual c) external d) physical → **c**
2. Adding a B+ tree index is a change at which level? a) external b) conceptual c) internal d) view → **c**
3. Renaming a column without breaking apps via a view is: a) physical independence b) logical independence c) normalization d) sharding → **b**
4. Which does the conceptual schema describe? a) pages and files b) tables, attributes, constraints c) user screens d) OS settings → **b**
5. A view is also called: a) materialized table b) virtual table c) index d) tablespace → **b**
6. Who owns the internal schema? a) end user b) application developer c) DBA d) web server → **c**
7. The ANSI/X3-SPARC architecture has how many schemas? a) 1 b) 2 c) 3 d) 4 → **c**
8. Which statement is TRUE? a) views store their own copy of data b) views are defined by queries c) views cannot be used for security d) views change the internal schema → **b**
9. Physical data independence protects: a) views from user changes b) conceptual schema from storage changes c) tables from NULLs d) queries from syntax errors → **b**
10. The metadata describing all three schemas lives in: a) WAL log b) system catalog c) redo log d) temp files → **b**

## 20. Flashcards
- **Q: Name the three schema levels.** → **A:** External (views), Conceptual (logical tables), Internal (physical storage).
- **Q: Logical data independence?** → **A:** External views immune to conceptual-schema changes.
- **Q: Physical data independence?** → **A:** Conceptual schema immune to storage-level changes.
- **Q: What is a view?** → **A:** A virtual table defined by a query over base tables.
- **Q: Which level holds indexes?** → **A:** Internal (physical) level.
- **Q: Where does the catalog live?** → **A:** Inside the database, describing all levels and mappings.
- **Q: Who proposed three-schema?** → **A:** ANSI/X3-SPARC (1975).
- **Q: How to give security via levels?** → **A:** External views per user hide columns/rows.

## 21. Revision
The three-schema architecture separates **external (views)**, **conceptual (tables + constraints)**, and **internal (files, indexes, page layouts)** levels, joined by two mappings. Its only reason for existing is **data independence**: logical independence (rename/split columns — views absorb it) and physical independence (swap indexes/storage engines — no one above notices). Views are the practical external level; the system catalog is where all schemas and mappings are described. In interviews, name the levels, then immediately name which change hits which level (adding an index = internal; renaming a column = conceptual, absorbed by a view). Never say "index is part of the schema" — it's internal.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are the 3 levels of the three-schema architecture?" | 7 / 13 Q1 |
| "What is data independence? Logical vs physical?" | 7 / 13 Q3-4 |
| "Where do indexes live in the architecture?" | 13 Q6, Q11 |
| "How do you migrate a schema without breaking apps?" | 13 Q9 |
| "What is a view and how is it used?" | 13 Q7, Q12 |
| "Who owns the internal schema?" | 13 Q5 |
| "Why do apps bind to views, not tables?" | 13 Q20 |
