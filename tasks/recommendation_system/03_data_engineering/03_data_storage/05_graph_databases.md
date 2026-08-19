# Graph Databases — Knowledge Graph and Social Graph for Recommendations

## 1. Why Graph Databases for Recommendation Systems

### 1.1 The Graph Advantage

Recommendation systems are inherently graph problems — users connect to items through interactions, items connect to items through similarities, users connect to users through social relationships. Graph databases store and query these relationships natively, without the expensive JOINs required in relational databases.

### 1.2 When Graph Databases Add Value

| Use Case | Graph Advantage | SQL Equivalent |
|----------|----------------|----------------|
| Social recommendations ("friends who liked X") | Single traversal: 2–3 hops in milliseconds | Multi-hop JOINs, expensive at scale |
| Knowledge graph recommendations | Path-based queries, semantic traversal | Recursive CTEs, very expensive |
| Item similarity via shared attributes | Co-occurrence traversal | Self-joins on interaction table |
| Influencer identification | Centrality algorithms (PageRank, Betweenness) | Complex iterative queries |
| Fraud detection in reviews | Community detection, anomaly patterns | Multi-table analysis |
| Sequential recommendations | Path analysis on user journey graph | Window functions + self-joins |

---

## 2. Neo4j for Knowledge Graph Recommendations

### 2.1 Data Model

```cypher
// User nodes
CREATE (u:User {
  user_id: "usr_12345",
  age_bucket: "25-34",
  country: "US",
  segment: "power_user",
  created_at: datetime("2025-01-15")
})

// Item nodes
CREATE (i:Item {
  item_id: "itm_67890",
  title: "Sony WH-1000XM5",
  category: "Headphones",
  brand: "Sony",
  price: 349.99,
  avg_rating: 4.6
})

// Category nodes (hierarchical taxonomy)
CREATE (c1:Category {name: "Electronics"})
CREATE (c2:Category {name: "Audio"})
CREATE (c3:Category {name: "Headphones"})
CREATE (c1)-[:HAS_SUBCATEGORY]->(c2)-[:HAS_SUBCATEGORY]->(c3)
CREATE (i)-[:BELONGS_TO]->(c3)

// User-Item interactions
CREATE (u)-[:PURCHASED {timestamp: datetime(), rating: 5}]->(i)
CREATE (u)-[:VIEWED {timestamp: datetime(), duration_seconds: 120}]->(i)
CREATE (u)-[:RATED {score: 4.5, timestamp: datetime()}]->(i)

// User-User social connections
CREATE (u1)-[:FOLLOWS {since: datetime()}]->(u2)
CREATE (u1)-[:SIMILAR_TO {similarity: 0.82, computed_at: datetime()}]->(u3)

// Item-Item relationships
CREATE (i1)-[:SIMILAR_TO {similarity: 0.91, method: "content"}]->(i2)
CREATE (i1)-[:COMPLEMENTARY_TO {confidence: 0.75}]->(i3)
CREATE (i1)-[:FREQUENTLY_BOUGHT_WITH {co_occurrence: 0.68}]->(i4)
```

### 2.2 Index Creation

```cypher
// Create indexes for fast lookups
CREATE INDEX user_id_index FOR (u:User) ON (u.user_id);
CREATE INDEX item_id_index FOR (i:Item) ON (i.item_id);
CREATE INDEX category_name_index FOR (c:Category) ON (c.name);

// Composite indexes for common query patterns
CREATE INDEX item_category_price FOR (i:Item) ON (i.category, i.price);

// Full-text search index for item search
CREATE FULLTEXT INDEX item_search FOR (i:Item) ON EACH [i.title, i.brand];
```

### 2.3 Cypher Query Examples for Recommendations

**Friends' Purchases ("Social Proof" Recommendations)**:
```cypher
// Find items purchased by users I follow, that I haven't purchased
MATCH (me:User {user_id: $userId})-[:FOLLOWS]->(friend:User)-[p:PURCHASED]->(item:Item)
WHERE NOT (me)-[:PURCHASED]->(item)
  AND p.rating >= 4
  AND p.timestamp > datetime() - duration('P30D')
RETURN item, COUNT(DISTINCT friend) AS friend_count
ORDER BY friend_count DESC
LIMIT 20;
```

**Knowledge Graph Walk ("Because You Bought X")**:
```cypher
// Items related through the knowledge graph: same category + similar attributes
MATCH (purchased:Item {item_id: $itemId})-[:BELONGS_TO]->(cat:Category)<-[:BELONGS_TO]-(similar:Item)
WHERE similar.item_id <> $itemId
  AND similar.price BETWEEN purchased.price * 0.7 AND purchased.price * 1.3
  AND NOT EXISTS {
    MATCH (me:User {user_id: $userId})-[:PURCHASED]->(similar)
  }
WITH similar, cat, 
     gds.similarity.cosine(similar.embedding, purchased.embedding) AS content_similarity
ORDER BY content_similarity DESC
LIMIT 50
RETURN similar, content_similarity, cat.name AS category;
```

**Influencer Detection (PageRank)**:
```cypher
// Run PageRank on the user-item interaction graph to find influential users
CALL gds.pageRank.write({
  nodeProjection: ['User', 'Item'],
  relationshipProjection: {
    PURCHASED: { type: 'PURCHASED', orientation: 'UNDIRECTED' },
    RATED: { type: 'RATED', orientation: 'UNDIRECTED' }
  },
  writeProperty: 'pagerank_score'
})
YIELD nodePropertiesWritten, ranIterations;

// Get top influential users by PageRank score
MATCH (u:User)
WHERE u.pagerank_score IS NOT NULL
RETURN u.user_id, u.pagerank_score, u.segment
ORDER BY u.pagerank_score DESC
LIMIT 100;
```

**Community Detection (Louvain)**:
```cypher
// Detect user communities based on co-purchase patterns
CALL gds.louvain.stream({
  nodeProjection: 'User',
  relationshipProjection: {
    CO_PURCHASE: {
      type: 'PURCHASED_SAME_ITEMS',
      orientation: 'UNDIRECTED',
      properties: 'weight'
    }
  }
})
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS user, communityId
RETURN communityId, COUNT(*) AS community_size,
       COLLECT(user.user_id)[0..5] AS sample_users
ORDER BY community_size DESC
LIMIT 20;
```

### 2.4 Graph Data Science (GDS) Library

Neo4j's GDS library provides out-of-the-box graph algorithms for recommendations:

| Algorithm Category | Algorithms | Recommendation Use Case |
|-------------------|-----------|------------------------|
| **Similarity** | Node Similarity, Cosine, Pearson | Item-to-item similarity, user-to-user similarity |
| **Centrality** | PageRank, Betweenness, Degree | Influencer identification, important items |
| **Community Detection** | Louvain, Label Propagation | User segmentation, interest communities |
| **Pathfinding** | Shortest Path, All Shortest Paths | "Users who bought X also bought Y" path discovery |
| **Node Embeddings** | Node2Vec, FastRP | Learn low-dimensional node representations for ML |

---

## 3. JanusGraph for Distributed Graph Recommendations

### 3.1 Architecture

JanusGraph is a distributed graph database designed for graphs with billions of edges, backed by storage backends (Cassandra, HBase, ScyllaDB) and indexing backends (Elasticsearch, Solr).

- **Storage Backend**: Cassandra/ScyllaDB provides distributed, eventually consistent storage for the graph structure.
- **Index Backend**: Elasticsearch provides full-text search and complex predicates on vertex/edge properties.
- **Gremlin Query Language**: Apache TinkerPop's Gremlin provides a standardized, traversable query language.

### 3.2 JanusGraph Schema

```groovy
// Define the graph schema
mgmt = graph.openManagement()

// Vertex labels
user = mgmt.makeVertexLabel('user').make()
item = mgmt.makeVertexLabel('item').make()
category = mgmt.makeVertexLabel('category').make()

// Property keys
userId = mgmt.makePropertyKey('user_id').dataType(String.class).make()
itemId = mgmt.makePropertyKey('item_id').dataType(String.class).make()
title = mgmt.makePropertyKey('title').dataType(String.class).make()
price = mgmt.makePropertyKey('price').dataType(Double.class).make()
timestamp = mgmt.makePropertyKey('timestamp').dataType(Date.class).make()
rating = mgmt.makePropertyKey('rating').dataType(Float.class).make()

// Edge labels
purchased = mgmt.makeEdgeLabel('purchased').make()
viewed = mgmt.makeEdgeLabel('viewed').make()
similarTo = mgmt.makeEdgeLabel('similarTo').make()
belongsTo = mgmt.makeEdgeLabel('belongsTo').make()

// Composite indexes (exact match)
mgmt.buildIndex('userById', Vertex.class).addKey(userId).unique().build()
mgmt.buildIndex('itemById', Vertex.class).addKey(itemId).unique().build()

// Mixed index (full-text + range queries via Elasticsearch)
mgmt.buildIndex('itemSearch', Vertex.class)
    .addKey(title, Mapping.TEXT.asParameter())
    .addKey(price)
    .addMixedIndex('search', ElasticsearchIndex.class)
    .build()

mgmt.commit()
```

### 3.3 Gremlin Query Examples

```groovy
// Find items similar to a given item, traversing the knowledge graph
g.V().has('item_id', 'itm_67890')
  .outE('similarTo').has('similarity', gt(0.7))
  .inV()
  .where(outE('belongsTo').inV().has('name', 'Electronics'))
  .order().by('similarity', desc)
  .limit(20)
  .valueMap(true)

// Multi-hop recommendation: items purchased by friends of friends
g.V().has('user_id', 'usr_12345')
  .out('follows').out('purchased')
  .where(not(__.in('purchased').has('user_id', 'usr_12345')))
  .groupCount()
  .order(local).by(values, desc)
  .limit(local, 20)

// User similarity based on shared purchases
g.V().has('user_id', 'usr_12345')
  .out('purchased').in('purchased')
  .where(not(__.has('user_id', 'usr_12345')))
  .groupCount()
  .order(local).by(values, desc)
  .limit(local, 10)
```

---

## 4. Graph Traversal Patterns for Recommendations

### 4.1 Traversal Depth and Performance

| Hop Depth | Query Pattern | Typical Latency | Use Case |
|-----------|--------------|-----------------|----------|
| 1 hop | User → Item (direct interactions) | < 5ms | History retrieval |
| 2 hops | User → Item → Similar Items | < 20ms | "Similar items" recommendations |
| 3 hops | User → Friend → Purchased Items | < 50ms | Social recommendations |
| 4 hops | User → Item → Category → Items → Users → Items | < 200ms | Knowledge graph walks |
| 5+ hops | Deep walks | > 500ms | Offline computation only |

**Key Insight**: Keep graph traversals to ≤ 3 hops for real-time serving. Deeper traversals should be pre-computed or run as batch jobs.

### 4.2 Traversal Optimization Strategies

- **Index-Backed Traversals**: Ensure that graph traversals use indexed lookups at each step. Unindexed traversals degrade to full graph scans.
- **Early Filtering**: Apply filters as early as possible in the traversal to reduce the intermediate result set.
- **Path Limiting**: Limit the number of paths explored at each step. Use `limit()` after `order()` to cap results.
- **Pre-Computed Paths**: For common traversal patterns (e.g., 2-hop item similarity), pre-compute and store the results rather than traversing at query time.
- **Bounded BFS**: Use breadth-first search with a depth limit and a maximum frontier size to prevent exponential expansion.

### 4.3 Graph vs Matrix Factorization

| Aspect | Graph Traversal | Matrix Factorization |
|--------|----------------|---------------------|
| Interpretability | High (explicit paths) | Low (latent factors) |
| Explainability | "Recommended because friend X also bought it" | "Recommended based on your taste profile" |
| Cold-Start | Can use graph structure (categories, attributes) | Needs interaction data |
| Scalability | Limited by traversal depth and graph size | Scales with matrix factorization algorithms |
| Freshness | Real-time if graph is up-to-date | Depends on retraining frequency |
| Best For | Social recs, knowledge graph, explainability | Large-scale CF, deep learning models |

---

## 5. Graph Database Performance Considerations

### 5.1 Memory and Storage

| Component | Neo4j | JanusGraph + Cassandra |
|-----------|-------|----------------------|
| Memory Model | In-memory graph + disk-based store | Distributed across Cassandra nodes |
| Memory Requirement | Full working set fits in RAM for best performance | Partitioned across cluster; each node holds a shard |
| Storage | Proprietary (native graph storage) | Cassandra (columnar, compressed) |
| Write Throughput | 10K–50K writes/sec (single node) | 100K+ writes/sec (distributed cluster) |
| Read Throughput | 10K–100K reads/sec (single node) | 100K+ reads/sec (distributed cluster) |

### 5.2 When NOT to Use Graph Databases

- **Simple Key-Value Lookups**: Use Redis or DynamoDB — graph databases add unnecessary overhead for simple lookups.
- **Bulk Analytics on Flat Data**: Use columnar stores (Parquet, ClickHouse) — graph databases are not optimized for full-table scans and aggregations.
- **Very Deep Traversals (10+ hops)**: Pre-compute offline; graph databases will not handle deep real-time traversals efficiently.
- **When the "Graph" is Actually a Tree**: Hierarchical data (category trees, org charts) may be better served by specialized tree stores or recursive CTEs in SQL.
