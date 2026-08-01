# Graph Databases

> **TL;DR**: Graph databases (Neo4j, Amazon Neptune, TigerGraph) make relationships first-class — nodes and edges stored and indexed as first-class entities — so path/traversal queries ("friends of friends", "fraud rings", "shortest path") that would explode into unreadable join trees in SQL run as direct local traversals in Cypher/Gremlin/SPARQL.

## 1. Why Does This Exist?
In a relational database, *relationships* are encoded as foreign keys, and "following" them means joining tables. For a single hop that's fine; for *variable-depth traversal* — "find all users within 3 hops," "which accounts are connected to this one by 2 transfers," "shortest path between two people" — the SQL becomes either impossible (unknown depth needs recursive CTEs) or produces enormous intermediate joins. A graph database exists to answer **relationship-first queries**: it stores nodes and edges *physically* so that walking an edge is a pointer-follow (O(1) adjacency), not a join lookup. The data model itself is the graph; queries are expressed as patterns (`MATCH (a)-[r]->(b)`) and executed by traversal. Where relational answers "what attributes does this thing have?", graphs answer "how is this thing *connected* to everything else?" — and some workloads (fraud, social, recommendation, knowledge graphs, network/routing, access control) are fundamentally connection queries.

## 2. How Does It Work?
- **Data model**: `Node` (with labels, properties) and `Relationship`/`Edge` (with type, direction, properties). Neo4j stores nodes in a doubly-linked list of adjacency structures and relationships with pointers to their start/end nodes — so a traversal walks linked lists, not indexes.
- **Query language**: **Cypher** (Neo4j) — pattern matching: `MATCH (a:Person)-[:KNOWS]->(b) RETURN b`; `OPTIONAL MATCH`, `WHERE` on properties, `SHORTESTPATH()`, `CALL {}` subqueries. Gremlin (Apache TinkerPop, Neptune/JanusGraph) is a graph *traversal* DSL. SPARQL is the RDF standard.
- **Indexing**: indexes on node labels/properties for the *entry point* (find the starting node fast); edge traversal itself is pointer-following, index-free adjacency.
- **Storage**: native graph engines store node-to-edge pointers (Neo4j), or adjacency lists on top of other stores (Neptune on graph engine; TigerGraph distributed).
- **Execution**: traversal/pattern-matching engines with cost-based planning; depth/selectivity pruning; `PROFILE`/`EXPLAIN` for plan reading.

## 3. When Is It Used?
- **Social graphs**: friends, follows, groups — "friends of friends", "mutual friends", "who can see this post?" (permission graphs).
- **Fraud detection**: ring detection, "2-hop money laundering," shared devices/IPs/IP addresses connecting accounts.
- **Recommendation**: "people who bought X also bought Y" — collaborative filtering through connection patterns.
- **Knowledge graphs**: entity relationships (Wikipedia/Wikidata-style), semantic search, NLP-entity linkage.
- **Network & routing**: shortest paths, supply-chain/telecom topology, dependency graphs (build systems, package managers).
- **Access control / governance**: entity-relationship RBAC, data lineage, org charts.
- Interviews: "when use a graph DB?", "Cypher vs SQL for friends-of-friends", "how would you model fraud detection?", "BFS/DFS vs recursive CTE".

## 4. Why Wasn't Another Approach Chosen?
- *Relational with recursive CTEs*: works for *bounded, fixed* depth (a `WITH RECURSIVE` friends-of-friends-3) but (a) depth isn't always fixed at query time, (b) each hop is a self-join over huge tables — cost grows with total graph size, not with the *subgraph explored*, and (c) the SQL is unreadable for anything beyond 2-3 hops. Graph engines traverse by adjacency pointers: cost ∝ explored neighborhood.
- *Denormalized adjacency in a KV/document store*: you can store "friends" arrays, but path queries ("shortest path between A and B", "find rings") become application BFS/DFS over many round trips — slow and unmaintainable. The graph engine makes traversal *native* and parallel.
- *General-purpose scan engines (Spark/OLAP)*: global graph analytics at huge scale have their place, but sub-second interactive path queries need a purpose-built store, not batch jobs.
- *Property graph vs RDF/triple stores*: property graphs (Neo4j) suit app/transactional use; RDF/SPARQL suits open linked data; most product/enterprise use is property-graph.

## 5. Intuition
A relational database answers "what's in this box?" — you open the box and read the label. A graph database answers "how are the boxes tied together?" — you follow the ropes. In SQL, following a rope is: look up the label on the box (join), find the rope (foreign key), follow it to the next box (another join), repeat — and every hop re-scans the whole storeroom. A graph store *labels the rope ends*: each box knows its ropes and the boxes at the other end (adjacency pointers). "Who's within 3 ropes of me?" = walk three steps through the pointers — you only ever touch the *neighborhood*, never the whole storeroom. That's why "friends of friends" is a flagship demo: in SQL it's a monstrous self-join tree; in Cypher it's three characters of pattern.

## 6. Real-World Analogy
**The airport's transfer network.** The relational database is the *departures board*: a huge table of flights, each with origin/destination columns. "How do I get from Mumbai to Berlin in 2 hops?" means the SQL engine must scan every flight looking for one that lands where another takes off (join 1), then repeat (join 2) — a board-wide search each time. The graph database is the *physical route map on the wall*: airports are dots, flights are lines between them; to find a 2-hop route you simply walk the lines, and the map *remembers* which dots connect to which (adjacency). The map doesn't care how many airports exist — you never scan them all, you just follow the corridor signs. Now add "find the airport that connects Mumbai to Berlin fastest" (shortest path), "which airports are isolated" (components), or "is there a transfer hub that unites 5 destinations in 2 hops" (ring/clique detection) — the map answers these by *drawing*, while the board answers them by *filtering and re-scanning*. If your questions are mostly "which flights exist from X" (attribute queries), the board is fine; the moment your questions are "how is X *connected*", the map wins.

## 7. Formal Definition
**Property graph model**: a directed graph `G = (V, E)` where vertices carry labels and property maps and edges carry a type and property map. **Native graph storage**: nodes stored with adjacency pointers to their incident relationships (index-free adjacency); relationship records reference start/end nodes, making traversal O(deg(v)) per step rather than O(global scan/join). **Query**: declarative pattern matching (Cypher `MATCH (a:P)-[r:T]->(b:Q)`), variable-length patterns `-[:T*1..3]->`, path functions (`shortestPath`), evaluated by a traversal engine with planning/estimation. **Cost**: traversal cost ∝ size of explored neighborhood, not total graph size — the fundamental advantage over relational join-based path queries.

## 8. Example
**Model (Cypher):**
```cypher
CREATE (a:Person {name:'Ana'})-[:FRIENDS_WITH]->(b:Person {name:'Bob'}),
       (b)-[:FRIENDS_WITH]->(c:Person {name:'Cara'}),
       (a)-[:FRIENDS_WITH]->(c),
       (c)-[:FRIENDS_WITH]->(d:Person {name:'Dan'});
```
**Queries:**
```cypher
-- Friends of friends (2 hops), excluding direct friends
MATCH (me:Person {name:'Ana'})-[:FRIENDS_WITH]->()-[:FRIENDS_WITH]->(foaf:Person)
WHERE NOT (me)-[:FRIENDS_WITH]->(foaf) AND foaf <> me
RETURN DISTINCT foaf.name;                       -- 'Dan'

-- Variable-depth: everyone within 3 hops
MATCH p = (me:Person {name:'Ana'})-[:FRIENDS_WITH*1..3]->(other:Person)
RETURN DISTINCT other.name;

-- Shortest path
MATCH p = shortestPath((a:Person {name:'Ana'})-[:FRIENDS_WITH*]-(z:Person {name:'Dan'}))
RETURN p;

-- Fraud ring: two accounts sharing a device AND a payment
MATCH (a1:Account)-[:USES]->(d:Device)<-[:USES]-(a2:Account),
      (a1)-[:SENT_TO]->(a2)
RETURN a1, a2, d;
```
The relational equivalent of "friends of friends at depth 3" is a self-join chain (or recursive CTE) whose cost grows with *total table size*; the Cypher version walks a fixed neighborhood.

## 9. Internal Working
1. **Storage (Neo4j)**: store files with fixed-size records — `nodemstore` (node records: label + first relationship pointer + property chain), `relationshipstore` (each relationship record: start node, end node, next/prev relationship pointers for both nodes) → adjacency via linked lists; property store for key-value properties. This gives *index-free adjacency*.
2. **Indexing**: label+property indexes (B-tree) find *entry nodes*; from there traversals walk adjacency records. (Native graph engines don't index every edge — they follow pointers.)
3. **Query execution**: Cypher is compiled to a pipeline of operators (`NodeIndexSeek` → `Expand(All)`/`Expand(Into)` → filters/aggregates); a cost-based planner estimates cardinalities (neighborhood selectivity); `EXPLAIN`/`PROFILE` show it. Variable-length patterns expand hops with pruning; `shortestPath` uses bidirectional BFS.
4. **Transactions**: ACID (Neo4j) with locking on nodes/relationships; WAL + checkpointing; `MATCH ... CREATE`/`MERGE` guarantee uniqueness (`MERGE` on a uniqueness constraint prevents duplicate nodes).
5. **Scale-out**: native single-node engines hold the hot graph in memory (sharding across nodes is hard because paths cross partitions); distributed systems (Neptune, TigerGraph, JanusGraph) shard by subgraph/partition key and accept cross-shard traversal cost. Many real deployments put the graph engine beside a primary OLTP DB and sync.

## 10. Time Complexity
- Node/edge lookup by indexed property: **O(log n)** (B-tree entry).
- Traversal of one hop from node v: **O(deg(v))** — the adjacency walk; total path query cost ≈ O(explored neighborhood).
- Friends-of-friends k-hops: O(Σ deg over frontier) — can explode for high-degree nodes (celebrity effect) → prune with selectivity, limits, or bidirectional search.
- `shortestPath`: bidirectional BFS O(b^(d/2)) (branching factor b, distance d).
- Global analytics (betweenness, community detection): O(V+E) to O(V·E) — the *not* real-time part (Spark/OLAP territory).
- Contrast: relational k-hop self-join cost O(|table|·hops) — graph wins by orders of magnitude as k and size grow.

## 11. Advantages
- **Natural model for relationships**: connections are the schema, not a join afterthought.
- **Traversal efficiency**: adjacency pointers → path queries cost neighborhood, not table scans; the "no global scan" property is the killer.
- **Readable, declarative queries**: Cypher patterns communicate the shape of what's asked; SQL for the same is unreadable recursion.
- **Flexible schema**: nodes/edges gain properties/labels without migrations (still avoid over-modeling).
- **ACID transactions** (Neo4j) for graph mutations — unlike many NoSQL systems.
- **Graph-specific algorithms built-in**: shortest path, community detection, PageRank — via Cypher `SHORTESTPATH`/APOC/Graph Data Science.
- **Great fit for fraud/social/recommendation** patterns that are simply infeasible in SQL at depth.

## 12. Disadvantages
- **Not for attribute/aggregation-heavy OLTP**: "sum sales by region" — a graph store is the wrong tool; use relational/warehouse.
- **Scale-out is hard**: native adjacency works best on one hot node in memory; sharding a graph splits paths (cross-partition hops are slow). Distributed graph = operational complexity.
- **Fewer engineers skilled** in Cypher/Gremlin vs SQL; steeper onboarding.
- **Data sync burden**: often a *secondary* store kept in sync from the primary OLTP DB (extra pipeline, eventual lag).
- **High-degree node blow-up**: celebrity/fan-out nodes make naive traversals expensive (need limits/pruning).
- **Smaller ecosystem** for analytics/BI integration compared to SQL/columnar stacks.

## 13. Interview Questions
1. **Q: When do you choose a graph database over SQL?** A: When the dominant queries are *relationship/traversal* based — variable-depth paths ("within k hops"), shortest paths, ring/community detection — and especially when depth isn't fixed (SQL recursive CTEs get unreadable and expensive). Use SQL for attribute/aggregation workloads even if it's "a graph-y domain" unless traversal is the core pattern.
2. **Q: What is index-free adjacency?** A: Storing each node with pointers to its incident relationships (and each relationship to its endpoints), so a traversal walks linked lists of adjacency records in O(deg) per hop — no global index lookups or joins per edge. The key structural advantage over relational path queries.
3. **Q: TRICKY: Friends-of-friends in SQL vs Cypher — why is Cypher better?** A: In SQL, a 2-hop query is two self-joins; a *variable*-depth query (any number of hops) needs a recursive CTE, and cost scales with total table size per hop. Cypher's `MATCH (me)-[:FOLLOWS*1..3]->(x)` walks adjacency pointers — cost scales with the explored *neighborhood*, and depth is a query parameter. Same answer, orders-of-magnitude cheaper execution and far more readable.
4. **Q: What is the property graph model?** A: Nodes (with labels + property maps) and relationships (typed, directed, with properties). vs RDF triple stores (subject-predicate-object, SPARQL, open linked-data). Property graphs suit product/transactional apps; RDF suits interop/ontology use.
5. **Q: How does Neo4j store data physically?** A: Fixed-size record files: node store (first relationship pointer, labels), relationship store (start/end node + prev/next pointers for both ends), property store (key-values), index store. Relationships are doubly linked on both endpoints → O(deg) adjacency traversal.
6. **Q: How do you model a "like" or a "follow" — node or edge?** A: An edge (`(:User)-[:LIKES]->(:Post)`) when it's a pure relationship; promote to a node if it gains its own properties/history (e.g., `(:Follow {since})`) or if you need to attach other edges to it (a "transfer" with its own metadata often becomes a node).
7. **Q: TRICKY: How would you detect a fraud ring?** A: Find groups where accounts are interconnected — e.g., accounts sharing devices/IPs *and* transacting with each other in cycles: `MATCH (a1)-[:USES]->(:Device)<-[:USES]-(a2)`, check transactions between them; or detect 2-hop cycles `MATCH (a)-[:SENT_TO]->(b)-[:SENT_TO]->(a)`. Cypher expresses "cycles in the graph" that SQL can't state declaratively.
8. **Q: What is `MERGE` and why does it matter?** A: `MERGE` = match-or-create (upsert): it guarantees no duplicate node/relationship by matching on a unique key — essential for idempotent graph writes and for maintaining uniqueness constraints (the analogue of a PK in a graph).
9. **Q: PR: My graph query is slow. What do you check?** A: (1) Entry point — is the starting node found by an *indexed* property (`NodeIndexSeek`) or a label scan? (2) High-degree fan-out — prune with `LIMIT`, selectivity, or bidirectional expansion. (3) Depth of variable-length patterns — bound with `*1..3`. (4) `EXPLAIN`/`PROFILE`: is there an unexpected CartesianProduct/Filter? (5) Data model — did you model a relationship as a node unnecessarily?
10. **Q: TRICKY: Why can't you just shard a graph across many nodes easily?** A: A path query touches nodes across partitions; each cross-partition hop becomes a network call, so sharding turns a local pointer-follow into distributed joins. Native engines keep the hot graph on one in-memory node; distributed graph engines (Neptune, TigerGraph) shard by subgraph and accept that cost — you trade traversal locality for scale.
11. **Q: Graph vs document store for a social network?** A: Documents (MongoDB) store per-user friend arrays — good for *profile* reads (my friends) but bad for *traversal* (friends-of-friends paths) which become app-level BFS with many round trips. Graphs do the traversal natively; documents win on flexible per-user payloads. Many systems mix: documents for profiles, graph for the social structure.
12. **Q: What is Gremlin vs Cypher?** A: Gremlin (Apache TinkerPop) is an imperative *traversal DSL* (step chains: `g.V('a').out('FRIEND').out('FRIEND')`) used by Neptune/JanusGraph; Cypher is declarative pattern matching (Neo4j). Similar power, different expressiveness — declarative Cypher is easier for pattern queries.
13. **Q: What is a recursive CTE and when is it acceptable vs a graph DB?** A: A SQL `WITH RECURSIVE` walks a hierarchy/bounded-depth tree in-database; fine for fixed small depth (org charts, BOM) with small tables. It becomes a maintenance/perf problem for large graphs, variable depth, or cyclic structures (cycle detection required) — that's the graph DB's home turf.
14. **Q: PRODUCTION: Should the graph DB be your system of record?** A: Often no — teams keep a primary OLTP DB (Postgres) as source of truth and sync the graph store (Kafka → graph ingest) for traversal queries, because graph engines historically favor read-heavy traversal and their write/availability model differs. Treat it as a query-optimized projection unless traversal-write patterns dominate.
15. **Q: How do you keep a graph store consistent with a primary DB?** A: Change-data-capture from the OLTP DB → sync jobs/applying upserts (`MERGE`) to the graph with idempotent keys; tolerate eventual sync lag; design graph queries to not require real-time consistency, or read the primary for correctness-critical bits.

## 14. Follow-Up Questions
1. **Q: What are the graph data science algorithms and when are they used?** A: PageRank (influence), community detection/Louvain (clusters/segments), betweenness centrality (bridges/hubs), shortest path, connected components (isolation detection). Run on snapshot exports (batch), not the hot transactional graph.
2. **Q: What is a "supernode"/high-degree node problem?** A: A node with huge fan-out (a celebrity, a shared IP) makes neighbor expansion blow up. Mitigations: cap expansion with LIMITs, index-assisted entry, split supernodes (fan-out by type/timestamp), or materialize partial results.
3. **Q: What is the Graph Data Science (GDS) library?** A: Neo4j's add-on computing graph algorithms (PageRank, Louvain, node2vec embeddings) in-memory over a projected graph — bridging graph *storage* (Cypher) and graph *analytics* (GDS).

## 15. Coding Example
```cypher
// Build a small social + purchase graph
CREATE (ana:Person {name:'Ana'})-[:FRIENDS_WITH]->(bob:Person {name:'Bob'}),
       (bob)-[:FRIENDS_WITH]->(cara:Person {name:'Cara'}),
       (ana)-[:FRIENDS_WITH]->(cara),
       (cara)-[:FRIENDS_WITH]->(dan:Person {name:'Dan'}),
       (ana)-[:PURCHASED {amount: 120}]->(prod:Product {name:'Laptop'}),
       (dan)-[:PURCHASED {amount: 340}]->(prod);
```
```cypher
// 1. Mutual friends of Ana and Dan
MATCH (a:Person {name:'Ana'})-[:FRIENDS_WITH]->(m)<-[:FRIENDS_WITH]-(d:Person {name:'Dan'})
RETURN m.name;
// 2. Everyone reachable in up to 3 hops from Ana (BFS)
MATCH (ana:Person {name:'Ana'})-[:FRIENDS_WITH*1..3]->(x:Person)
RETURN DISTINCT x.name ORDER BY x.name;
// 3. Shortest social path Ana -> Dan
MATCH p = shortestPath((ana:Person {name:'Ana'})-[:FRIENDS_WITH*]-(dan:Person {name:'Dan'}))
RETURN p;
// 4. Product recommendation: what did friends-of-friends buy that I didn't?
MATCH (me:Person {name:'Ana'})-[:FRIENDS_WITH*2..2]->(foaf:Person),
      (foaf)-[:PURCHASED]->(p:Product)
WHERE NOT (me)-[:PURCHASED]->(p) AND NOT (me)-[:FRIENDS_WITH]->(foaf)
RETURN DISTINCT p.name;
// 5. Fraud: two accounts sharing a device
MATCH (a1:Account)-[:USES]->(d:Device)<-[:USES]-(a2:Account)
WHERE a1 <> a2 AND (a1)-[:SENT_TO]->(a2)
RETURN a1.id, a2.id, d.id;
```
```sql
-- The relational analogue (fixed depth 2) — note the cost/readability gap
SELECT DISTINCT foaf.name
FROM friends me
JOIN friends hop1 ON me.friend_id = hop1.user_id
JOIN friends hop2 ON hop1.friend_id = hop2.user_id
WHERE me.user_id = 'Ana'
  AND NOT EXISTS (SELECT 1 FROM friends d
                   WHERE d.user_id = 'Ana' AND d.friend_id = hop2.user_id);
```

## 16. Industry Usage
- **Neo4j**: fraud at banks/credit (HSBC, Worldpay), network operations (NASA), knowledge graphs, healthcare entity linkage; ACID + Cypher + GDS.
- **Amazon Neptune**: managed graph in AWS — Gremlin/SPARQL/openCypher; used for social/identity/fraud in AWS-native stacks.
- **TigerGraph**: distributed, large-scale fraud/anti-money-laundering analytics (massive graphs, GSQL).
- **LinkedIn/other social networks**: the *original* motivation (LinkedIn's own graph engines); modern stacks often mix graph (traversal) with document/relational (profiles).
- **Knowledge graphs**: Google/Wikipedia/Wikidata linked data, semantic search, LLM RAG entity graphs (graph-RAG is the 2024+ trend).
- **RDF/SPARQL**: open data interoperability (DBpedia, schema.org); increasingly used alongside property graphs.

## 17. References
- Robinson, Webber & Eifrem, *Graph Databases*, 2nd ed. (O'Reilly) — the canonical text.
- Neo4j Cypher manual: https://neo4j.com/docs/cypher-manual/current/
- Neo4j Graph Data Science: https://neo4j.com/docs/graph-data-science/current/
- Angus & Angus, "Index-free adjacency" discussion in *Graph Databases*.
- Cyganiak et al., "RDF 1.1 Concepts and Abstract Syntax" (W3C).
- Marr, "NoSQL Graph Databases: Why, When and When Not", in *7 Databases in 7 Weeks*.

## 18. Cheat Sheet
- Property graph: nodes (labels+props), relationships (typed, directed, props); index-free adjacency = O(deg) traversal.
- Cypher: `MATCH (a:P)-[:R*1..3]->(b:Q)`, `OPTIONAL MATCH`, `WHERE`, `SHORTESTPATH()`, `MERGE` (upsert), `EXPLAIN`/`PROFILE`.
- Why it wins: traversal cost ∝ neighborhood, not table size; variable depth is a query parameter.
- When to use: fraud rings, social/recommendation, knowledge graphs, network/routing, access control, lineage.
- When not: attribute/aggregation OLTP, big analytics (use warehouse/columnar), simple CRUD.
- Traps: high-degree supernodes (cap with LIMIT), entry-point scans (index it), modeling relationships as nodes unnecessarily, expecting easy sharding (paths cross partitions).
- Scale-out: native = one hot in-memory node; distributed (Neptune/TigerGraph) = shard by subgraph, accept cross-shard cost.
- Keep-in-sync pattern: primary OLTP → CDC → graph projection (eventual).
- SQL alternative: recursive CTE — fine small/fixed-depth; unreadable+slow for variable depth.

## 19. Quiz
1. Index-free adjacency means: a) no indexes b) pointer-following traversal c) no storage d) in-memory only → **b**
2. Variable-depth query in SQL needs: a) JOIN b) recursive CTE c) subquery d) view → **b**
3. Graph traversal cost scales with: a) total table size b) explored neighborhood c) RAM d) #indexes → **b**
4. `MERGE` does: a) delete b) match-or-create c) aggregate d) sort → **b**
5. Supernode problem: a) too many nodes b) high-degree fan-out blow-up c) memory d) schema → **b**
6. Best tool for "sum sales by region"? a) Neo4j b) columnar/relational c) Redis d) graph → **b**
7. Which stores nodes+edges physically with pointers? a) Mongo b) Cassandra c) Neo4j d) ClickHouse → **c**
8. Fraud-ring pattern is expressed as: a) recursion b) cycles in the graph c) GROUP BY d) JSON → **b**

## 20. Flashcards
- **Q: Property graph?** → **A:** Nodes + typed/directed relationships, both with properties.
- **Q: Index-free adjacency?** → **A:** Node→relationship pointers; traversal without global lookups.
- **Q: Cypher pattern for 2-hop?** → **A:** `MATCH (a)-[:R]->()-[:R]->(b)`.
- **Q: Variable depth?** → **A:** `-[:R*1..3]->`.
- **Q: MERGE?** → **A:** Match-or-create (idempotent upsert).
- **Q: Graph wins when?** → **A:** Relationship/traversal queries (paths, rings, connectivity).
- **Q: Supernode?** → **A:** High-degree node → expansion blow-up; cap/prune.
- **Q: SQL equivalent?** → **A:** Recursive CTE (fixed/small depth only).
- **Q: Distributed graphs?** → **A:** Hard — paths cross partitions; native stays one-node.

## 21. Revision
Graph DBs make relationships first-class via index-free adjacency: nodes and edges stored with pointers, so path/traversal queries cost neighborhood size, not table scans. Cypher (`MATCH`, variable-length patterns, `SHORTESTPATH`, `MERGE`) expresses what SQL recursion can't. Use graphs for social, fraud, recommendation, knowledge graphs, and network/routing — not for attribute/aggregation OLTP. Watch for supernodes, unindexed entry points, and naive sharding (paths cross partitions). Often a read-heavy projection synced from a primary DB. The "when is it relationships not rows?" question is the interview's whole point.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "When choose a graph DB?" | 1, 3, 13 |
| "What is index-free adjacency?" | 2, 9, 13 |
| "Friends-of-friends SQL vs Cypher?" | 8, 13 |
| "Property graph vs RDF?" | 7, 13 |
| "How does Neo4j store data?" | 9, 13 |
| "Fraud-ring detection?" | 8, 13 |
| "Why is sharding graphs hard?" | 9, 13 |
| "Supernode problem?" | 10, 13 |
| "Should the graph DB be the source of truth?" | 13 |
| "Recursive CTE vs graph DB?" | 13 |
