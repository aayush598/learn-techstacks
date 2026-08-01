# Data Models: Hierarchical, Network, Relational, Object

> **TL;DR**: A data model is a family of concepts for describing data structure, constraints, and operations — four have shaped history (hierarchical, network, relational, object), and the relational model won because it's simple, set-based, mathematically grounded, and queryable with a declarative language.

## 1. Why Does This Exist?
Before any data can be stored or queried, we must decide **how to structure it** — that's what a data model does. It answers three questions: *What shapes can data take?* (structure), *What rules must it obey?* (constraints), *What can you do with it?* (operations). Without an explicit model, every application invents its own ad-hoc structure and nothing can interoperate, query, or enforce integrity. Data models exist so that (a) DBMSs can be built generically over a fixed vocabulary (record, table, tree, graph, object), (b) schemas can be designed and communicated, and (c) query languages can be defined once per model. The relational model exists specifically to remove the *programming required to navigate* data that plagued the earlier models.

## 2. How Does It Work?
Each model defines its own structural unit and querying mechanism:
- **Hierarchical** (IMS, 1960s): data as a *tree* — parent-child links; a record has one parent (with virtual parents as a later hack). Navigation is top-down, pointer-based.
- **Network** (CODASYL/DBTG, 1970s): data as a *directed graph* — records in sets with owner-member links; many-to-many supported natively via links.
- **Relational** (Codd 1970): data as *relations* (tables of rows/columns); no physical pointers — connections are made by *values* (keys); queries are set-based via relational algebra.
- **Object** (ODMG, OO DBMS of the 1990s): data as *objects* with identity, methods, inheritance, and complex nested types.
- **Modern**: the relational model dominates, extended with object-relational features (Postgres: `CREATE TYPE`, JSONB); NoSQL adds *document*, *key-value*, *graph*, *column-family* models.

## 3. When Is It Used?
- **Hierarchical**: legacy systems still in production — IMS at banks and telcos; LDAP/X.500 directory trees; XML's nested structure is hierarchical.
- **Network**: rare today; historically in telecom and mainframe apps (the old network databases were replaced but their descendants persist).
- **Relational**: *the default* — OLTP, OLAP, ERP, finance, web backends: MySQL, PostgreSQL, Oracle, SQL Server. Use when you need joins, ACID, and a standard query language.
- **Object**: niche — engineering/CAD, scientific data, telecom; mostly subsumed into object-relational (Postgres custom types, SQL:1999).
- **Post-relational (NoSQL)**: documents (MongoDB) when schema is flexible; graphs (Neo4j) when relationships ARE the data; key-value (Redis) for caching/sessions; column-family (Cassandra) for massive time-series/sharded writes.

## 4. Why Wasn't Another Approach Chosen?
The relational model beat the others for a clear set of reasons:
- **Hierarchical rejected because**: one parent per node forced data duplication (a student enrolled in two courses appears twice), only predefined traversal paths worked, and ad-hoc queries were painful (you could only ask questions along the tree's fixed paths).
- **Network rejected because**: it fixed many-to-many but required *navigational* programming — the programmer walked pointers manually (DML "FIND NEXT"), so every report was a small program; there was no set-based "give me all X".
- **Relational chosen because**: structure is *uniform and simple* (just tables), queries are *declarative* (say what, not how), it rests on *set theory and logic* (a rigorous foundation = provable optimization), and *data independence* is natural (no embedded pointers to break). 
- **Object rejected (as a replacement) because**: OODBMSs lacked a standard query language and lost set-based optimization; the industry chose *hybridization* — relational with object extensions — which is what Postgres and Oracle are today.
- **Why not one model for everything?** Different workloads have different structure/consistency/scale needs; polyglot persistence picks the right model per use-case. But if forced to choose one, relational is the safest default.

## 5. Intuition
The four models are four ways of organizing a city's roads: **hierarchical** is a single road per district — to reach anywhere you drive up to a junction and back down one fixed trunk (restrictive, but fast on known routes). **Network** is a spiderweb of two-way streets with traffic lights every block — flexible routing but you must know the exact turns (navigational programming). **Relational** is a system of *addresses and street signs*: you don't drive a fixed route; you ask "find all houses where the owner works at X" and a planner (the optimizer) computes the route for you. **Object** is a smart city where each building contains its own services (methods), not just data. Relational won because asking questions became *descriptive* instead of *driving directions*.

## 6. Real-World Analogy
A **family tree vs a phone book**. The hierarchical model is the family tree — everyone has exactly one biological parent-line per branch, and "find all grandchildren who like cricket" requires walking every branch. The network model is a rich genealogy with many marriage links — richer, but you must traverse each link by hand. The relational model is a **phone book** — a flat, searchable table; plus a second book linking names to addresses. You don't navigate — you *search by value* ("everyone with last name Sharma", "everyone in Delhi"). Search by value is why the phone book model (relational) defeated the tree and graph models for general-purpose data.

## 7. Formal Definition
A **data model** is a set of concepts used to describe the structure (data types, relationships, constraints) and semantics of data, plus a set of basic operations for manipulating it. (Elmasri & Navathe, Ch. 2.)
- **Hierarchical model**: a collection of record types connected by parent-child links, forming a rooted tree (one parent per record type).
- **Network model (CODASYL)**: record types connected by named *set* relationships (owner-member); a member may have many owners — a graph.
- **Relational model (Codd 1970)**: data described as relations (n-ary tuples in a schema over domains); relationships represented by shared values (foreign keys); manipulated with relational algebra/calculus.
- **Object data model (ODMG 1.0-3.0)**: objects with identity, state (attributes), behavior (methods), inheritance, and complex attribute types.

## 8. Example
University data — same miniworld, four shapes:
- **Hierarchical**: `DEPARTMENT → COURSE → STUDENT` as a tree. Student S1 in both CS101 and MATH101 must be *duplicated* under both courses (data redundancy!) because a node has one parent.
- **Network**: `COURSE` owns set `enrolls` with members `STUDENT`; a student can be member of many sets — no duplication, but queries need `FIND`, `FIND NEXT`, `FIND OWNER`.
- **Relational**: tables `Course(cno, cname)`, `Student(sid, sname)`, `Enroll(sid, cno, grade)`. To find all students in CS101: `SELECT sname FROM Student JOIN Enroll USING(sid) WHERE cno='CS101'` — no pointers, just value matching.
- **Object**: class `Student` with `enroll()`, attribute `courses: set<Course>`; query via method calls — expressive but no set-based algebra.

## 9. Internal Working
1. **Hierarchical**: records stored with physical child pointers (or IMS's hierarchical sequence). Query = start at root, walk pointers. Only supports "given parent, find children" efficiently.
2. **Network**: records stored with owner-member pointer chains (next/prior/owner pointers per set). DML is navigational: `FIND STUDENT RECORD SET ENROLLS` then `FIND NEXT`.
3. **Relational**: rows stored in files; relationships materialized *by value comparison* at query time (joins). The optimizer rewrites the declarative query into a physical plan (index scan, hash join).
4. **Object**: objects stored with OIDs; methods executed by the DBMS; nested objects (structs) may be stored inline or as references.
5. **Modern relational (e.g. Postgres)**: JSONB gives schema-flexible *document* semantics inside a relational engine — the "object/relational" synthesis. The catalog holds metadata for all of it.

## 10. Time Complexity
- **Hierarchical**: navigation down a fixed path O(depth) per access, but *predefined* paths only; finding data by a non-path attribute requires full tree scan O(n).
- **Network**: pointer-chasing O(path length) but the path must be programmed; set-based aggregation requires manual traversal O(n·links).
- **Relational**: declarative query optimized — index seek O(log_f n), hash join O(n+m), nested loop O(n·m) worst case. The optimizer's freedom to choose is the win.
- **Object**: attribute access O(1); but *ad-hoc* cross-object queries often need scans or in-app logic O(n).

## 11. Advantages
- **Hierarchical**: simple, fast access along known paths; great for strictly nested data (org charts, XML, filesystems).
- **Network**: native many-to-many without duplication; flexible navigation.
- **Relational**: uniform simple structure; declarative set-based queries; mathematical foundation → provable optimization; strong data independence; standard SQL across vendors.
- **Object**: natural fit for OO languages; encapsulation; complex nested data types without join-stitching.

## 12. Disadvantages
- **Hierarchical**: duplication for multi-parent data; rigid; no ad-hoc queries; DBA must design the tree perfectly up front.
- **Network**: navigation is programming (slow development); no data independence; steep learning curve.
- **Relational**: impedance mismatch with OO code (need ORM); less natural for deeply nested/recursive data; schema rigidity.
- **Object**: weak query standards; poor interoperability; set optimization lost; market failure of pure OODBMS.

## 13. Interview Questions
1. **Q: What is a data model?** A: A collection of concepts for describing data structure, constraints, and operations. Examples: relational, hierarchical, network, object, document, graph. It defines the vocabulary a DBMS understands.
2. **Q: Compare hierarchical, network, and relational models.** A: Hierarchical = tree, one parent per node, pointer navigation, duplication for many-to-many. Network = graph, many-to-many via owner-member sets, but navigational programming. Relational = tables, value-based links (FK), declarative set queries — no programming the path.
3. **Q: Why did the relational model win?** A: Simplicity (just tables), set-based declarative queries (what-not-how), a rigorous mathematical foundation (algebra/calculus → optimizer can rewrite provably), strong data independence (no pointers to break), and standard SQL.
4. **Q: What is the navigational problem in pre-relational models?** A: Queries were implemented by walking pointers one step at a time (FIND NEXT), so the programmer specified the *entire access path*. Any new question = new program. The relational model made queries descriptive instead.
5. **Q: Who invented the relational model and when?** A: E.F. Codd, in "A Relational Model of Data for Large Shared Data Banks", CACM 13(6), 1970. He proposed normalizing relations and formalized the algebra.
6. **Q (tricky): Is XML a hierarchical data model?** A: Structurally yes — XML is a tree with one parent per node. But XML has its own query standards (XPath, XQuery) and can reference across trees with IDs, so it's "hierarchical with links". Treat it as tree-shaped data, not a relational model.
7. **Q (scenario): Your data is a social network where "who follows whom" IS the query. Which model?** A: A graph model (Neo4j) — traversals over relationships are O(path) instead of recursive self-joins. Relational can express it but recursive CTEs + join tables get slow and awkward at depth.
8. **Q: What is an object-relational DBMS (ORDBMS)?** A: A relational engine extended with object features: user-defined types, inheritance, method-like functions. PostgreSQL is the canonical example (`CREATE TYPE`, table inheritance, `jsonb`). It's the practical answer to "relational or object?".
9. **Q: What's the difference between a data model and a schema?** A: A data model is the *conceptual toolkit* (relations, records, links); a schema is a *specific description* of one database built with that toolkit. "Relational" is the model; "Students(id, name)" is a schema in it.
10. **Q (production): When would you pick a document model (MongoDB) over relational?** A: When the data is naturally aggregate-shaped (a blog post with comments inside), schema changes often, or you need horizontal write scale and can relax ACID/joins. Pick relational when relationships, joins, or transactions dominate.
11. **Q: What is the CODASYL/DBTG network model?** A: A 1960s-70s standard where records are organized into owner-member *sets*; a record can belong to many sets (many-to-many). Used in mainframe DBMSs (IDMS). It fixed the hierarchical duplication problem but kept navigational access.
12. **Q (tricky): Does the relational model forbid pointers physically?** A: No — physical pointers exist in storage (B+ tree leafs point to rowids). What the *model* forbids is *logical* pointers in the user's view: connections must be expressed by key values so queries can match any two values. That's data independence.
13. **Q: What did IMS stand for and where is it used?** A: Information Management System — IBM's hierarchical DBMS (1966) for the Apollo program; still runs huge bank/telco batch workloads today. Its hierarchical data model was the first to reach massive scale.
14. **Q: What is the "impendence mismatch"?** A: The mismatch between the relational model (sets/tuples) and OO programming languages (objects/nested graphs). ORMs (Hibernate, Prisma) bridge it but add N+1 and mapping bugs. Object models avoid it; that was their pitch.
15. **Q (production): Postgres has tables, arrays, and jsonb — which model is it?** A: Object-relational. Base is relational; object extensions (arrays, composite types, jsonb) let you store nested structures without sacrificing relational querying and ACID. This is the industry-standard compromise.
16. **Q: Why is a "record" in a file not the same as a "tuple" in a relation?** A: A tuple is a *set-member*: position-independent, has a schema, must be unique per key; a file record is just bytes in a fixed order. Relations have algebra; files don't. The relational model adds semantics the file format lacks.
17. **Q (hard): Give a query the hierarchical model cannot answer without redesigning the tree.** A: "All customers who ordered product P" if the tree is `Customer→Order→Product` but not `Product→Order` — the inverse direction needs either a second tree or a full scan. In relational: one `JOIN`/index answers any direction. That direction-freedom is the relational advantage.
18. **Q: What is entity-relationship (ER) modeling and how does it relate?** A: ER is a *conceptual design technique* (entities, attributes, relationships), not a DBMS storage model; it's typically mapped to the relational model (entities→tables, relationships→FKs). It's how you design the conceptual schema before implementation.
19. **Q: Which data model does LDAP use?** A: LDAP is directory (hierarchical) — entries in a tree keyed by DN (distinguished name). Used for authn/z directories (users, orgs) where reads dominate. It's a practical survivor of the hierarchical era.
20. **Q (scenario): You're designing a catalog for a fashion app with varying product attributes. Relational or document?** A: The honest answer: *both* — a relational core for products/categories/orders + a JSONB/JSON column for variant attributes (Postgres) or a document store for the flexible parts. Pure relational with EAV tables is a known anti-pattern; pure document breaks reporting joins.

## 14. Follow-Up Questions
1. **Q: When did NoSQL arise and what problems did it target?** A: Late 2000s, from web scale: horizontal write scaling, flexible schemas, and avoiding join cost. CAP theorem debates drove the split; today SQL engines re-absorbed most features (jsonb, sharding).
2. **Q: What does the CAP theorem say about model choice?** A: Under network partition you choose CP or AP. Relational usually = CP (consistency); document/cassandra often = AP. The model choice implies which guarantee you're buying.
3. **Q: Could a new "model" dethrone relational?** A: Only if it solves a pain relational can't absorb. Graph analytics and vector similarity (for AI) are the current challengers — but they coexist with relational rather than replace it (polyglot).
4. **Q: How do columnar models differ from relational?** A: Columnar (Snowflake, ClickHouse) is a *physical storage* trick over relational semantics — values stored per-column for compression and scan speed. The logical model is still tables; it's OLAP-optimized relational.
5. **Q: Is the ER model a "data model" in the DBMS sense?** A: It's a *semantic/conceptual* data model — good for design and communication — but it lacks a formal query algebra, so it's not a DBMS storage model. That's why ER maps *down* to relational.

## 15. Coding Example
```sql
-- Relational: value-based links. No pointers, no navigation.
CREATE TABLE course (cno TEXT PRIMARY KEY, cname TEXT);
CREATE TABLE student (sid INT PRIMARY KEY, sname TEXT);
CREATE TABLE enroll (
    sid  INT REFERENCES student(sid),
    cno  TEXT REFERENCES course(cno),
    PRIMARY KEY (sid, cno)
);

-- Declarative: "all students in CS101" — optimizer chooses the plan
SELECT s.sname
FROM   student s
JOIN   enroll e ON e.sid = s.sid
WHERE  e.cno = 'CS101';
```
```python
# Network-style navigation (would be forbidden in relational!)
def network_query():
    course = find_record("COURSE", "CS101")
    s = find_first_member(course, "enrolls")     # pointer walking
    names = []
    while s is not None:
        owner = find_owner(s, "student_of")       # manual traversal
        names.append(owner["sname"])
        s = find_next_member(course, "enrolls")   # navigate the set
    return names
```

## 16. Industry Usage
- **IMS (hierarchical)** still processes ~billions of transactions/day in banks and telecoms; mainframes outlive generations of "modern" tech.
- **Relational engines dominate revenue**: Oracle, SQL Server, PostgreSQL, MySQL power essentially all OLTP systems of any size.
- **PostgreSQL** is the canonical object-relational DBMS — custom types, arrays, `jsonb`, `hstore`, and table inheritance ship in a relational core.
- **Neo4j** (graph), **MongoDB/Couchbase** (document), **Cassandra/HBase** (column-family), **Redis/Memcached** (key-value) each own a workload slice — polyglot persistence is standard practice.
- **GraphQL/REST API layers** increasingly sit over relational cores, while recommendation systems use *graph and vector* models — the modern stack is explicitly multi-model.
- Codd's 1970 paper was the basis for the 1981 Turing Award and for every SQL standard since SQL-86.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 2 (Data Models, Schemas, and Instances).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 1 & 12 (Data Models).
- Codd, E. F., "A Relational Model of Data for Large Shared Data Banks", CACM 13(6), 1970.
- Codd, E. F., "The Relational Model for Database Management: Version 2", 1990.
- ODMG 3.0 Standard (object data management).
- PostgreSQL Documentation: https://www.postgresql.org/docs/current/ (Data Types, jsonb, inheritance).

## 18. Cheat Sheet
- 4 classic models: hierarchical (tree), network (graph, navigational), relational (tables, value links), object (OODBMS).
- Relational won: simple, declarative, set-based, mathematically rigorous, data-independent.
- NoSQL models: document, key-value, column-family, graph — each for a workload.
- ORDBMS = relational + objects (Postgres) — the practical winner.
- ER model is conceptual/design, mapped down to relational.
- Codd 1970, CACM 13(6) — the birth of relational.
- IMS = hierarchical survivor; LDAP = hierarchical directory.
- "Navigational" = you program the path; "declarative" = optimizer finds the path.

## 19. Quiz
1. Which model uses owner-member sets? a) hierarchical b) network c) relational d) object → **b**
2. The relational model connects records by: a) pointers b) keys/values c) OIDs d) offsets → **b**
3. IMS is which model? a) network b) hierarchical c) relational d) object → **b**
4. Who proposed the relational model? a) Bachman b) Codd c) Stonebraker d) Date → **b**
5. "You program the access path" describes: a) declarative querying b) navigational access c) SQL d) indexing → **b**
6. PostgreSQL is best described as: a) pure OODBMS b) object-relational c) hierarchical d) graph DB → **b**
7. A document model suits: a) strict ACID money movement b) aggregate-shaped flexible data c) deep relationship traversal d) key-value cache → **b**
8. For "who follows whom" queries, the best model is: a) relational b) graph c) hierarchical d) key-value → **b**
9. The relational model's query basis is: a) recursive descent b) relational algebra c) pointer chasing d) BFS → **b**
10. A tuple differs from a file record because: a) it has bytes b) it's set-based with a schema c) it's faster d) it's bigger → **b**

## 20. Flashcards
- **Q: What is a data model?** → **A:** Concepts for describing data structure, constraints, and operations.
- **Q: 4 classic data models?** → **A:** Hierarchical, network, relational, object.
- **Q: Why did relational win?** → **A:** Simple tables, declarative set queries, math foundation, data independence.
- **Q: What is navigational access?** → **A:** Queries by walking pointers manually (network/hierarchical).
- **Q: What is ORDBMS?** → **A:** Relational + object features (Postgres).
- **Q: IMS is what model?** → **A:** Hierarchical (IBM, 1966).
- **Q: When to use graph model?** → **A:** When relationships are the data (social, network).
- **Q: When to use document model?** → **A:** Flexible schema, aggregate-shaped data.

## 21. Revision
A data model = structure + constraints + operations. Pre-relational: hierarchical (tree, one parent, duplication) and network (graph, many-to-many, but navigational DML). Relational (Codd 1970) = tables linked by *values*, declarative algebra, strong independence — it won. Object model failed to replace it; the industry merged into **object-relational** (Postgres). NoSQL split into document/key-value/column/graph for special workloads. For interviews: compare the models on three axes (structure, how you query, redundancy), and always justify relational with "declarative set semantics + data independence". Mention IMS and LDAP as hierarchical survivors, Neo4j/MongoDB/Cassandra as modern multi-model stack.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Compare hierarchical, network, relational models" | 7 / 13 Q2 |
| "Why did relational win?" | 4 / 13 Q3 |
| "What is navigational vs declarative?" | 2 / 13 Q4 |
| "When would you use a graph/document DB?" | 13 Q7, Q10 |
| "What is an ORDBMS?" | 13 Q8 |
| "What is IMS / CODASYL?" | 13 Q6, Q11, Q13 |
| "Data model vs schema?" | 13 Q9 |
