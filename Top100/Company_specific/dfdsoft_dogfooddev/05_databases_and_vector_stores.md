# DFDSOFT / DogFoodDev — Databases & Vector Stores (100 Q&A)
> Role: AI Coding & Agent Development Specialist  > Candidate: Aayush Gid (PostgreSQL/SQLite/Milvus/FAISS/embeddings/RAG background)

---

## SQL Fundamentals (Q1–Q12)

**Q1: What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN?**

A: `INNER JOIN` returns only rows with matches in both tables. `LEFT JOIN` returns all rows from the left table and matching rows from the right (NULLs where no match). `RIGHT JOIN` is the reverse. `FULL OUTER JOIN` returns all rows from both tables, with NULLs on the non-matching side. Example:
```sql
SELECT o.id, c.name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id;
```

**Q2: Explain GROUP BY and HAVING. How do they differ from WHERE?**

A: `WHERE` filters rows *before* grouping. `GROUP BY` collapses rows into groups based on column values. `HAVING` filters *after* grouping, so it can use aggregate functions. `WHERE` cannot reference aggregates.
```sql
SELECT department, COUNT(*) AS cnt
FROM employees
WHERE status = 'active'
GROUP BY department
HAVING COUNT(*) > 5;
```

**Q3: What is a window function and how does it differ from GROUP BY?**

A: Window functions perform calculations across a set of rows *related to the current row* without collapsing them. Unlike `GROUP BY`, they preserve all rows. Common ones: `ROW_NUMBER()`, `RANK()`, `LEAD()`, `LAG()`, `SUM() OVER(...)`.
```sql
SELECT name, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dept
FROM employees;
```

**Q4: What are correlated vs non-correlated subqueries?**

A: A **non-correlated subquery** executes independently of the outer query (runs once). A **correlated subquery** references columns from the outer query and executes once per outer row.
```sql
-- Non-correlated
SELECT * FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE name = 'Engineering');

-- Correlated
SELECT * FROM employees e WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id);
```

**Q5: How do indexes speed up queries, and what are the trade-offs?**

A: Indexes (typically B-trees) create a sorted lookup structure so the DB avoids full table scans. Trade-offs: extra storage, slower `INSERT`/`UPDATE`/`DELETE` due to index maintenance, and unused indexes waste resources. Choose indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY`.
```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**Q6: What does EXPLAIN ANALYZE tell you, and how do you read its output?**

A: `EXPLAIN ANALYZE` shows the *actual* query plan and real execution times. Key fields: `Seq Scan` vs `Index Scan`, `cost` (estimated), `actual time`, `rows`, `loops`. Look for sequential scans on large tables, nested loops with high row counts, and sorts that could use indexes.
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
```

**Q7: What are covering indexes and when should you use them?**

A: A covering index includes all columns needed by a query, so PostgreSQL can answer the query entirely from the index without touching the heap. Use `INCLUDE` or put all columns in the index key.
```sql
CREATE INDEX idx_covering ON orders(customer_id, order_date) INCLUDE (total_amount);
-- Query uses only the index:
SELECT order_date, total_amount FROM orders WHERE customer_id = 42;
```

**Q8: Explain the difference between a WHERE clause filter and a HAVING clause filter with a practical example.**

A: `WHERE` filters individual rows before aggregation; `HAVING` filters grouped results after aggregation. You cannot use aggregate functions in `WHERE`.
```sql
-- WHERE filters before grouping
SELECT product_id, SUM(quantity) AS total_sold
FROM order_items
WHERE order_date >= '2026-01-01'
GROUP BY product_id
HAVING SUM(quantity) > 100;
```

**Q9: What is a self-join and when would you use one?**

A: A self-join joins a table to itself, useful for hierarchical or relational data within the same table (e.g., employees and their managers).
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

**Q10: How do UNION and UNION ALL differ, and when would you choose each?**

A: `UNION` combines results and removes duplicates (requires sorting/hashing). `UNION ALL` keeps all rows, which is faster. Use `UNION ALL` when you know there are no duplicates or don't care, for performance.

**Q11: What is a CTE (Common Table Expression), and what is a recursive CTE?**

A: A CTE (`WITH` clause) creates a named temporary result set for readability. A recursive CTE references itself to traverse hierarchical data (org charts, tree structures).
```sql
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, t.depth + 1
    FROM employees e JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

**Q12: What are the main aggregate functions and when do you use each?**

A: `COUNT(*)` counts rows; `SUM(col)` totals numeric values; `AVG(col)` averages; `MIN/MAX` find extremes. Use `COUNT(DISTINCT col)` for unique counts. These are used with `GROUP BY` to summarize data.

---

## PostgreSQL (Q13–Q24)

**Q13: What PostgreSQL data types are most useful for AI/agent applications?**

A: `JSONB` for storing unstructured metadata and tool call results, `UUID` (`gen_random_uuid()`) for distributed ID generation, `ARRAY` for multi-value tags, `TEXT` with `pg_trgm` for fuzzy search, `TIMESTAMPTZ` for event timelines, and `SERIAL`/`BIGSERIAL` for auto-incrementing PKs.

**Q14: When would you use JSONB over a normalized schema in PostgreSQL?**

A: Use `JSONB` when the schema is highly variable (e.g., storing LLM tool call outputs, different document metadata per source). Use normalized tables when you need strict consistency, foreign keys, and efficient joins on structured fields. JSONB supports GIN indexes for fast key lookup.
```sql
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metadata JSONB NOT NULL DEFAULT '{}'
);
CREATE INDEX idx_metadata ON agent_logs USING GIN(metadata);
```

**Q15: Explain PostgreSQL isolation levels and their practical impact.**

A: Four levels: `READ UNCOMMITTED` (not truly available in PG), `READ COMMITTED` (default, each statement sees committed data), `REPEATABLE READ` (snapshot per transaction, phantom reads possible), `SERIALIZABLE` (full isolation, may cause serialization failures). For most agent/RAG pipelines, `READ COMMITTED` suffices. Use `REPEATABLE READ` when you need consistent reads within a transaction.

**Q16: What is a materialized view and when should you use one?**

A: A materialized view stores the result of a query on disk, refreshed periodically. Use for expensive aggregations or joined queries that don't need real-time freshness (e.g., pre-computed search indices, analytics dashboards).
```sql
CREATE MATERIALIZED VIEW mv_popular_docs AS
    SELECT doc_id, COUNT(*) AS search_count
    FROM search_logs GROUP BY doc_id;
REFRESH MATERIALIZED VIEW mv_popular_docs;
```

**Q17: How does pg_trgm support fuzzy search, and when would you use it?**

A: `pg_trgm` breaks strings into trigrams and uses GIN/GiST indexes for similarity search. Good for typo-tolerant search on short text (names, titles). For long-form semantic search, embeddings are better. Combine with `pg_similarity` or use `similarity()` / `word_similarity()`.
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_name_trgm ON users USING GIN(name gin_trgm_ops);
SELECT * FROM users WHERE name % 'Aayush' ORDER BY similarity(name, 'Aayush') DESC;
```

**Q18: What are the best practices for PostgreSQL schema design in an AI agent system?**

A: Use UUIDs for IDs (avoid sequential ID guessing), separate hot data (recent logs) from cold data (archives), use JSONB for flexible metadata, add created_at/updated_at timestamps, normalize agent configurations, and use foreign keys for referential integrity. Partition large tables by time.

**Q19: How do you implement full-text search in PostgreSQL vs using a vector store?**

A: PostgreSQL `tsvector`/`tsquery` provides lexical full-text search with stemming and ranking—great for keyword search. Vector stores (Milvus, FAISS) provide semantic search via embeddings. For many RAG systems, hybrid approach works: use PostgreSQL `tsvector` for exact/keyword matching, vector store for semantic, and combine with reciprocal rank fusion.

**Q20: Explain ACID properties in the context of a RAG ingestion pipeline.**

A: **Atomicity**: Ingestion of a document (chunk + embedding + metadata) either fully succeeds or fully rolls back. **Consistency**: Constraints (foreign keys, NOT NULL) are always satisfied after commit. **Isolation**: Concurrent ingestions don't interfere. **Durability**: Committed ingestion survives crashes. Use transactions for multi-step ingestion.

**Q21: What is the N+1 query problem and how do you solve it in PostgreSQL?**

A: N+1 occurs when you fetch N parent rows then issue N separate queries for children. Solutions: `JOIN` in one query, `IN` subquery, or `LATERAL JOIN`. In ORMs, use eager loading (`select_related`/`joinedload`).
```sql
-- N+1 problem
-- SELECT * FROM orders; then for each: SELECT * FROM items WHERE order_id = ?

-- Solution with JOIN
SELECT o.*, i.*
FROM orders o
JOIN order_items i ON i.order_id = o.id;
```

**Q22: How do you handle concurrent vector ingestion into PostgreSQL without conflicts?**

A: Use `INSERT ... ON CONFLICT` for upserts, batch inserts within transactions, and use advisory locks for coordination. For high-throughput, use a queue (e.g., pgmq) and worker processes.
```sql
INSERT INTO document_chunks (doc_id, chunk_idx, content, embedding)
VALUES ($1, $2, $3, $4)
ON CONFLICT (doc_id, chunk_idx) DO UPDATE SET
    content = EXCLUDED.content,
    embedding = EXCLUDED.embedding,
    updated_at = NOW();
```

**Q23: What PostgreSQL extensions are most useful for AI/ML workloads?**

A: `pgvector` for vector similarity search directly in PG, `pg_trgm` for fuzzy text, `uuid-ossp`/`gen_random_uuid()` for UUIDs, `pg_stat_statements` for query analysis, `pg_cron` for scheduled refresh of materialized views, and `pgmq` for message queuing.

**Q24: When would you store embeddings in PostgreSQL (pgvector) vs a dedicated vector store?**

A: Use pgvector when you want simplicity (one database), have <10M vectors, need ACID transactions alongside vectors, or want SQL-based filtering. Use dedicated stores (Milvus, Pinecone) for >10M vectors, sub-millisecond latency at scale, advanced ANN algorithms, and multi-vector/hybrid search. For DogFoodDev prototyping, pgvector is excellent; scale to Milvus for production.

---

## SQLite (Q25–Q32)

**Q25: When should you choose SQLite over PostgreSQL?**

A: Use SQLite for embedded applications, local development/prototyping, mobile apps, testing (in-memory DB), and single-server applications with low concurrency. SQLite is zero-config, serverless, and stored in a single file. Avoid for high-concurrency writes or multi-server access.

**Q26: What is WAL mode in SQLite and why does it matter?**

A: WAL (Write-Ahead Logging) mode allows concurrent reads while a write is in progress, improving performance significantly. Default journal mode blocks reads during writes. Enable with `PRAGMA journal_mode=WAL;`. Essential for any SQLite DB with concurrent access.

**Q27: What are SQLite's main limitations compared to PostgreSQL?**

A: No built-in network access (serverless), limited concurrency (single writer), no `RIGHT`/`FULL OUTER JOIN` (added in 3.39), no `MATERIALIZED VIEW`, limited data types (no native UUID/JSONB), no user roles/permissions, and no stored procedures. Schema changes can lock the DB.

**Q28: How do you use Python's sqlite3 module effectively?**

A: Use parameterized queries (never string interpolation), context managers for connections/cursors, and `row_factory = sqlite3.Row` for dict-like access.
```python
import sqlite3

conn = sqlite3.connect("app.db", timeout=10)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA journal_mode=WAL;")

docs = conn.execute(
    "SELECT * FROM documents WHERE content LIKE ?", (f"%{query}%",)
).fetchall()
```

**Q29: What does ATTACH DATABASE do in SQLite and when is it useful?**

A: `ATTACH DATABASE` lets you query multiple SQLite files in a single query. Useful for cross-database joins, migrating data, or working with sharded data.
```sql
ATTACH DATABASE 'archive.db' AS archive;
SELECT * FROM main.documents d
JOIN archive.old_documents o ON d.id = o.id;
```

**Q30: How do you implement FTS (full-text search) in SQLite?**

A: SQLite has built-in FTS5. Create a virtual table and use the `MATCH` operator.
```sql
CREATE VIRTUAL TABLE docs_fts USING fts5(content, tokenize='porter unicode61');
INSERT INTO docs_fts VALUES ('Embeddings are vector representations of text');
SELECT * FROM docs_fts WHERE docs_fts MATCH 'embeddings vector';
```

**Q31: How would you use SQLite as an embedding cache in a RAG pipeline?**

A: Cache embeddings by content hash to avoid re-computing. Use WAL mode for concurrent access.
```python
def get_embedding(conn, content: str, embed_fn):
    content_hash = sha256(content.encode()).hexdigest()
    row = conn.execute("SELECT embedding FROM cache WHERE hash = ?", (content_hash,)).fetchone()
    if row:
        return np.frombuffer(row[0], dtype=np.float32)
    emb = embed_fn(content)
    conn.execute("INSERT INTO cache (hash, embedding) VALUES (?, ?)",
                 (content_hash, emb.tobytes()))
    conn.commit()
    return emb
```

**Q32: How do you benchmark and optimize SQLite query performance?**

A: Use `EXPLAIN QUERY PLAN`, add indexes on filtered/sorted columns, enable WAL mode, use `PRAGMA optimize`, batch inserts in transactions, and set `PRAGMA cache_size` higher for large DBs. For bulk loading, disable indexes, load, then recreate them.

---

## NoSQL Concepts (Q33–Q40)

**Q33: What are the main NoSQL data models and when do you use each?**

A: **Document** (MongoDB): flexible schema, nested objects—good for varied metadata. **Key-value** (Redis): fast lookups, caching—good for session data, feature flags. **Column-family** (Cassandra): wide-column, time-series—good for event logs at scale. **Graph** (Neo4j): relationships—good for knowledge graphs. Choose based on access patterns, not data shape.

**Q34: Explain the CAP theorem.**

A: In a distributed system, you can guarantee only two of three: **Consistency** (every read returns the most recent write), **Availability** (every request gets a response), **Partition Tolerance** (system works despite network failures). Since partitions are inevitable, you choose between CP (consistent but may reject requests) and AP (available but may return stale data).

**Q35: What is eventual consistency and where does it appear in AI systems?**

A: Eventual consistency means all nodes converge to the same state given enough time, but reads may temporarily return stale data. In AI systems: vector store replication (Milvus replicas may lag), distributed embedding pipelines, and caching layers (Redis with TTL).

**Q36: When would you choose SQL (PostgreSQL) over NoSQL (MongoDB) for an AI agent system?**

A: Choose SQL when: you need ACID transactions (e.g., billing, user data), relationships matter (agent→task→result), you need complex joins, or data is structured. Choose NoSQL when: schema varies per document type, you need horizontal write scaling, or the data maps naturally to documents (e.g., LLM conversation logs with nested messages).

**Q37: What is a document database and how does it differ from a relational database?**

A: Document databases store data as JSON-like documents (BSON) without a fixed schema—each document can have different fields. Relational databases enforce a fixed schema with tables, rows, and columns. Document DBs trade query flexibility and schema evolution for less structural rigidity.

**Q38: What are the trade-offs of using Redis as a caching layer in a RAG system?**

A: Pros: sub-millisecond reads, TTL-based expiration, pub/sub for invalidation, simple key-value model. Cons: data loss risk (if not persistent), memory constraints, no complex queries. Use for caching frequent retrieval results, embedding lookups, or conversation history with TTL.

**Q39: Explain horizontal vs vertical scaling in the context of vector databases.**

A: Vertical scaling: bigger machine (more RAM, CPU). Simple but has limits. Horizontal scaling: more machines. Milvus supports horizontal scaling via sharding (distributed by primary key) and replication. For <10M vectors, vertical scaling of pgvector may suffice. Beyond that, horizontal scaling with Milvus or Pinecone is necessary.

**Q40: What is a knowledge graph and how does it relate to RAG?**

A: A knowledge graph stores entities and their relationships as nodes and edges. In RAG, a knowledge graph can complement vector search: retrieve related entities via graph traversal, then use embeddings for semantic similarity. This is called GraphRAG and improves multi-hop reasoning.

---

## MongoDB (Q41–Q48)

**Q41: What is MongoDB's document model and when is it useful for AI systems?**

A: MongoDB stores BSON documents in collections. Each document can have arbitrary fields. Useful for AI systems when storing varied LLM outputs (tool calls, structured extractions), conversation histories with nested messages, or experiment tracking with per-run metadata.

**Q42: Write a MongoDB aggregation pipeline to find the most common tool calls in the last 7 days.**

A:
```javascript
db.agent_logs.aggregate([
  { $match: { timestamp: { $gte: ISODate("2026-08-13") } } },
  { $unwind: "$tool_calls" },
  { $group: { _id: "$tool_calls.name", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]);
```

**Q43: What is embedding vs referencing in MongoDB and when would you choose each?**

A: **Embedding** stores related data inside the parent document (denormalization)—fast reads, no joins, but data duplication and larger documents. **Referencing** stores an `ObjectId` to another collection—normalized, smaller documents, but requires `$lookup` for joins. Embed for data read together and rarely updated; reference for large/many-to-many relationships.

**Q44: How do you create an index in MongoDB, and what types exist?**

A: `db.collection.createIndex({ field: 1 })` creates an ascending B-tree index. Types: single field, compound (multi-field), multikey (arrays), text (full-text), geospatial, hash (sharding). Use `explain()` to verify index usage.
```javascript
db.conversations.createIndex({ "messages.timestamp": -1 });
db.conversations.createIndex({ "metadata.tags": 1, "created_at": -1 });
```

**Q45: How does MongoDB handle horizontal scaling (sharding)?**

A: MongoDB distributes data across shards using a shard key. The `mongos` router directs queries. Choose a shard key with high cardinality and even distribution (e.g., hashed `_id` or a user ID). Without a good shard key, you get hotspots.

**Q46: What are change streams in MongoDB and how could you use them in an AI pipeline?**

A: Change streams provide real-time event feeds of data changes. Use them to trigger downstream processing: when a new document is inserted into a collection, automatically generate embeddings, update a vector store, or trigger an agent workflow.
```javascript
const changeStream = db.documents.watch();
changeStream.on("change", async (change) => {
  if (change.operationType === "insert") {
    await generateAndStoreEmbedding(change.fullDocument);
  }
});
```

**Q47: How do you query arrays and nested documents in MongoDB?**

A: Use dot notation for nested fields and `$in`/`$all` for arrays.
```javascript
// Nested field
db.docs.find({ "metadata.source": "pdf" });

// Array contains value
db.docs.find({ "tags": { $in: ["rag", "embeddings"] } });

// Array of objects
db.conversations.find({ "messages.role": "assistant" });
```

**Q48: What is the MongoDB aggregation framework and how does it compare to SQL?**

A: The aggregation pipeline processes documents through stages (`$match`, `$group`, `$project`, `$lookup`, `$unwind`). Similar to SQL `WHERE`, `GROUP BY`, `SELECT`, `JOIN`, and `UNNEST` respectively. More flexible for nested/unstructured data; SQL is more efficient for relational queries with proper indexes.

---

## Embeddings Fundamentals (Q49–Q60)

**Q49: What are embeddings in the context of AI/ML?**

A: Embeddings are dense, fixed-length numerical vectors that represent the semantic meaning of text, images, or other data. Similar items have vectors that are close together in the embedding space. They enable semantic search, clustering, classification, and recommendation.

**Q50: Explain the difference between dense and sparse embeddings.**

A: **Dense embeddings** (e.g., OpenAI ada-002, BGE) are low-dimensional vectors (768–3072) where most values are non-zero, capturing semantic meaning. **Sparse embeddings** (e.g., BM25, SPLADE) are high-dimensional vectors where most values are zero, capturing term frequency/importance—similar to TF-IDF but learned. Dense is better for semantic similarity; sparse for exact keyword matching.

**Q51: Compare embedding models: OpenAI ada-002, sentence-transformers, and BGE.**

A: **OpenAI ada-002**: API-based, 1536 dimensions, good general quality, costs per token, no local compute. **Sentence-transformers** (e.g., all-MiniLM-L6-v2): open-source, runs locally, 384–768 dimensions, good for retrieval tasks, free. **BGE** (BAAI): open-source, state-of-the-art on MTEB benchmarks, 768–1024 dimensions, strong multilingual support. Choose BGE/sentence-transformers for privacy, cost, and speed; ada-002 for simplicity.

**Q52: What is cosine similarity and why is it the default metric for embedding comparison?**

A: Cosine similarity measures the cosine of the angle between two vectors: `cos(A,B) = (A·B) / (||A|| × ||B||)`. It ranges from -1 to 1. It's the default because it's invariant to magnitude—focusing on direction (semantic orientation) rather than magnitude (length/intensity). Useful when embedding magnitudes vary.

**Q53: When would you use dot product or L2 distance instead of cosine similarity?**

A: **Dot product**: when vectors are already normalized (then equivalent to cosine), or when magnitude matters (e.g., popularity-weighted search). **L2 (Euclidean) distance**: when you need absolute spatial distance, useful in clustering. For most RAG applications, cosine similarity or dot product on normalized vectors works best.

**Q54: How do you generate embeddings at scale for a RAG pipeline?**

A: Batch API calls (OpenAI processes 2048 per request), use async/concurrent processing, implement retry with exponential backoff, cache embeddings by content hash (use SQLite/Redis), and monitor rate limits. For local models, use GPU acceleration and batch inference.
```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def embed_batch(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [d.embedding for d in response.data]
```

**Q55: What is the significance of embedding dimensions and how do you choose?**

A: Dimensions determine the capacity to capture semantic information. Higher dimensions (3072) capture more nuance but increase storage, index size, and search latency. Lower dimensions (384) are faster and cheaper but may lose nuance. For most RAG, 768–1536 dimensions balance quality and performance. Use dimensionality reduction (PCA) if needed.

**Q56: What are Matryoshka embeddings and why do they matter?**

A: Matryoshka embeddings (e.g., OpenAI's text-embedding-3) are trained so that prefixes of the full vector are meaningful. You can truncate to 256 or 512 dimensions and still get decent performance, saving storage and compute. Useful for trade-off between speed and accuracy at different retrieval tiers.

**Q57: How do you handle embedding updates when source documents change?**

A: Detect changes (hash comparison), regenerate embeddings only for changed chunks, update vector store entries (delete old + insert new), and maintain a mapping table (chunk_id → content_hash). Use transactions for consistency. For large-scale, use a change data capture (CDC) pipeline.

**Q58: What is the difference between embedding a query vs embedding a document for retrieval?**

A: Many models use different prompts/instructions for queries vs documents. For retrieval-optimized models (BGE, E5), prefix the query with "Represent this sentence for searching relevant passages: ". Documents typically don't get this prefix. This asymmetry improves retrieval quality.

**Q59: How do you evaluate embedding quality for a RAG system?**

A: Use retrieval metrics on labeled data: Recall@K, NDCG, MRR. Create a benchmark dataset of query-document pairs with relevance labels. Test across domains. Also evaluate end-to-end: does better retrieval improve generation quality (answer faithfulness, relevance)?

**Q60: What are multi-vector embeddings and when would you use them?**

A: Multi-vector embeddings represent one document with multiple vectors (e.g., one per chunk, or per sentence). At query time, retrieve across all vectors and aggregate (max-similarity, ColBERT late interaction). Use when documents are long and a single embedding loses important details. ColBERT is a key example.

---

## Vector Stores (Q61–Q72)

**Q61: What is a vector store and how does it differ from a traditional database?**

A: A vector store is specialized for storing and querying high-dimensional vectors with similarity search (ANN). Traditional databases use exact matching (B-tree indexes). Vector stores use approximate algorithms (HNSW, IVF) optimized for finding "nearest neighbors" in embedding space, often trading perfect accuracy for speed.

**Q62: Explain ANN (Approximate Nearest Neighbor) algorithms and why exact search doesn't scale.**

A: Exact nearest neighbor (brute-force) compares the query against every vector—O(n) complexity, infeasible for millions of vectors. ANN algorithms (HNSW, IVF, LSH) use indexing structures to narrow the search space, achieving sub-linear query time (O(log n) or better) with slight accuracy trade-offs (recall ~95-99%).

**Q63: How does HNSW (Hierarchical Navigable Small World) work?**

A: HNSW builds a multi-layer graph where each node connects to nearby neighbors. The top layers have long-range edges for fast navigation; lower layers have short-range edges for precision. Search starts at the top, greedily navigates to the approximate region, then drills down. Build time O(n·log(n)), query time O(log(n)). Excellent for high recall.

**Q64: What is IVF (Inverted File Index) and when would you use it over HNSW?**

A: IVF partitions vectors into clusters (Voronoi cells) using k-means. At query time, only the nearest clusters are searched. Use IVF when: you need faster index building than HNSW, memory is constrained, or you're doing batch operations (IVF supports efficient batch adds with `nprobe` tuning). HNSW generally has better recall but higher memory.

**Q65: What is metadata filtering in vector search and how is it implemented?**

A: Metadata filtering applies pre-filters (e.g., `WHERE category = 'python'`) before or during vector search. Implementation varies: **Pre-filter** (filter first, then search—fast but may miss nearest neighbors if filtered out), **Post-filter** (search all, then filter—high recall but slow), **In-filter** (integrated into ANN traversal—optimal). Milvus supports in-filter; FAISS requires manual pre-filtering.

**Q66: What is hybrid search and why is it important for RAG?**

A: Hybrid search combines dense (semantic) and sparse (keyword/BM25) retrieval, merging results with techniques like reciprocal rank fusion (RRF). Important because dense search misses exact terms (product codes, acronyms) and sparse search misses semantic similarity. Hybrid search captures both.

**Q67: What is Reranking in the context of vector retrieval?**

A: Reranking takes the top-K results from initial retrieval and re-scores them with a more powerful (but slower) model, typically a cross-encoder that reads query and document jointly. Cross-encoders (e.g., Cohere Rerank, bge-reranker) are more accurate than bi-encoders but too slow for full corpus search. Use as a second stage: retrieve top-50, rerank to top-5.

**Q68: What is Reciprocal Rank Fusion (RRF) and how do you implement it?**

A: RRF merges ranked lists by summing `1/(k + rank)` for each result across lists (k is typically 60). It's score-normalized, so it works across different scoring scales (cosine similarity vs BM25).
```python
def rrf_merge(ranked_lists: list[list], k: int = 60) -> list:
    scores = {}
    for lst in ranked_lists:
        for rank, doc_id in enumerate(lst):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)
```

**Q69: How do you benchmark a vector store's performance?**

A: Metrics: **Recall@K** (fraction of true nearest neighbors in top-K), **QPS** (queries per second), **latency** (p50, p95, p99), **index build time**, **memory usage**. Use standard benchmarks (ANN-Benchmarks, BIGANN). Test with your actual data distribution, not random vectors—distribution affects IVF/HNSW performance.

**Q70: What is product quantization (PQ) and when would you use it?**

A: PQ compresses vectors by splitting them into subvectors and quantizing each to a codebook centroid. Reduces memory by 8-64x with moderate recall loss. Use when memory is constrained and you need to fit billions of vectors on有限 RAM. FAISS's `IndexIVFPQ` combines IVF for partitioning + PQ for compression.

**Q71: How do you handle vector store versioning and updates in production?**

A: Use blue-green deployments: build a new index alongside the old, atomically switch the alias. For updates, use soft deletes (flag as deleted) and periodic compaction. Maintain an audit log of index versions. For Milvus, use collection aliases and bulk insert for new versions.

**Q72: What are the key considerations for choosing a vector store for a production RAG system?**

A: Consider: scale (number of vectors), latency requirements, filtering needs (metadata, temporal), hybrid search support, managed vs self-hosted, cost (compute + storage), consistency guarantees, backup/recovery, and ecosystem integration. Prototyping: pgvector or FAISS. Production at scale: Milvus, Pinecone, or Weaviate.

---

## Milvus (Q73–Q84)

**Q73: Describe Milvus's distributed architecture.**

A: Milvus 2.x has a microservice architecture: **Proxy** (client-facing, load balancing), **Query Node** (executes searches), **Data Node** (handles inserts/deletes, writes to log), **Index Node** (builds indexes), **Root Coordinator** (metadata), **Query Coordinator**, **Data Coordinator**, **Index Coordinator**. State is managed by etcd; logs by Pulsar/Kafka; data stored in object storage (S3/MinIO).

**Q74: How do you create a Milvus collection and define its schema?**

A:
```python
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection

fields = [
    FieldSchema("id", DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema("content", DataType.VARCHAR, max_length=4096),
    FieldSchema("metadata", DataType.JSON),
]
schema = CollectionSchema(fields, enable_dynamic_field=True)
collection = Collection("documents", schema)
```

**Q75: What index types does Milvus support and which should you choose?**

A: **IVF_FLAT**: good balance of speed/recall, needs training. **IVF_PQ**: memory-efficient for large datasets, lower recall. **HNSW**: high recall, fast queries, no training needed, higher memory. **SCANN**: quantization-based, good for very large datasets. **GPU indexes** (CAGRA): extreme throughput. Choose HNSW for <10M vectors (best recall), IVF_PQ for >100M vectors (memory constraint).

**Q76: How do you perform metadata filtering in Milvus search?**

A: Milvus supports boolean expressions in search. Use `expr` parameter.
```python
results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"ef": 128}},
    limit=10,
    expr='metadata["category"] == "python" and metadata["year"] >= 2025',
    output_fields=["content", "metadata"]
)
```

**Q77: What is Milvus's hybrid search and how do you configure it?**

A: Hybrid search combines multiple vector fields (e.g., dense + sparse embeddings) in a single query. Configure with `Collection.hybrid_search()` using multiple `AnnSearchRequest` objects, each targeting a different field with its own params and anns_field.
```python
from pymilvus import AnnSearchRequest, RRFRanker

dense_req = AnnSearchRequest(
    data=[dense_query], anns_field="dense_embedding",
    param={"metric_type": "COSINE", "params": {"ef": 128}}, limit=50
)
sparse_req = AnnSearchRequest(
    data=[sparse_query], anns_field="sparse_embedding",
    param={"metric_type": "IP"}, limit=50
)
results = collection.hybrid_search(
    [dense_req, sparse_req],
    ranker=RRFRanker(),
    limit=10
)
```

**Q78: How does Milvus handle multi-vector search (e.g., ColBERT-style)?**

A: Milvus supports multiple vector fields per entity. For ColBERT-style search, store per-token embeddings as a JSON array or use multiple vector fields. Use `Function` API to extract vectors at insert time. At search time, use ` hybrid_search` or reranking to combine per-token similarities.

**Q79: What is reranking in Milvus and how do you implement it?**

A: Milvus supports built-in reranking via `Ranker` objects. `RRFRanker` combines ranked lists using reciprocal rank fusion. `WeightedRanker` applies custom weights. For cross-encoder reranking, retrieve top-K from Milvus, then rerank externally.
```python
from pymilvus import RRFRanker

results = collection.hybrid_search(
    [dense_req, sparse_req],
    ranker=RRFRanker(k=60),
    limit=10
)
```

**Q80: How do you manage Milvus in production (scaling, monitoring, backup)?**

A: Use Milvus Lite for development, standalone for single-node, distributed (Kubernetes with Milvus operator) for production. Monitor via Prometheus/Grafana (built-in metrics). Backup: Milvus supports snapshot-based backup. Scale horizontally by adding query/data/index nodes. Use collection aliases for zero-downtime index rebuilds.

**Q81: What is the difference between Milvus 2.x and earlier versions?**

A: Milvus 2.x is completely redesigned: microservice architecture (vs monolithic), supports distributed deployment, log-based architecture with Pulsar/Kafka, object storage for persistence, better resource isolation, and improved scalability. Milvus 1.x had simpler architecture but limited scalability.

**Q82: How do you perform incremental updates in Milvus?**

A: Milvus supports upsert (insert or update) by primary key. For embedding updates, delete old vectors and insert new ones in a transaction-like manner. For bulk updates, use `bulk_insert` with JSON/Parquet files. Maintain a mapping of source_id to Milvus primary key for updates.

**Q83: How do you tune Milvus search parameters for your use case?**

A: Key params: **HNSW**: `ef` (higher = better recall, slower). **IVF**: `nprobe` (higher = better recall, slower). **Metric**: cosine for normalized embeddings, IP for unnormalized, L2 for spatial. Tune by measuring recall@K vs latency trade-off on your actual queries. Start with defaults, then increase `ef`/`nprobe` until recall plateaus.

**Q84: How would you integrate Milvus into a Python RAG pipeline?**

A: Use `pymilvus` library. Flow: connect → create collection → insert embeddings → build index → load to memory → search → disconnect. For production, use connection pooling and handle retries. Example:
```python
from pymilvus import connections, Collection

connections.connect("default", host="localhost", port="19530")
collection = Collection("documents")
collection.load()

results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"ef": 128}},
    limit=10,
    output_fields=["content"]
)
```

---

## FAISS (Q85–Q92)

**Q85: What is FAISS and when would you choose it over a managed vector service?**

A: FAISS (Facebook AI Similarity Search) is a C++ library with Python bindings for efficient similarity search. Choose FAISS when: you need full control, have GPU resources, want zero-cost, need sub-millisecond latency, or are building offline/embedded systems. Choose managed (Milvus, Pinecone) for distributed scale, easy operations, and built-in metadata filtering.

**Q86: What are the main FAISS index types and their trade-offs?**

A: **IndexFlatL2**: exact search, O(n), small datasets. **IndexIVFFlat**: partitioned search, faster, needs training. **IndexHNSW**: graph-based, high recall, fast. **IndexIVFPQ**: compressed, memory-efficient, lower recall. **IndexScalarQuantizer**: integer quantization. Training: IVF and PQ require training on sample data; Flat and HNSW do not.

**Q87: How do you use FAISS in Python?**

A:
```python
import faiss
import numpy as np

dim = 1536
index = faiss.IndexHNSWFlat(dim, 32)  # 32 neighbors per node
index.hnsw.efSearch = 128

# Add vectors
vectors = np.random.randn(100000, dim).astype('float32')
index.add(vectors)

# Search
query = np.random.randn(1, dim).astype('float32')
distances, indices = index.search(query, k=10)
```

**Q88: How do you enable GPU acceleration in FAISS?**

A:
```python
import faiss

res = faiss.StandardGpuResources()
index_cpu = faiss.IndexIVFFlat(quantizer, dim, nlist)
gpu_index = faiss.index_cpu_to_gpu(res, 0, index_cpu)  # GPU 0
gpu_index.train(data)
gpu_index.add(vectors)
distances, indices = gpu_index.search(query, k=10)
```
GPU acceleration is especially effective for large batch searches and index training.

**Q89: How do you persist and load a FAISS index?**

A:
```python
import faiss

# Save
faiss.write_index(index, "index.faiss")

# Load
index = faiss.read_index("index.faiss")

# For GPU: convert to CPU first
gpu_index = faiss.index_gpu_to_cpu(gpu_index)
faiss.write_index(gpu_index, "index.faiss")
```

**Q90: How do you add metadata filtering to FAISS?**

A: FAISS doesn't have built-in metadata filtering. Common approaches: **Pre-filter** (filter IDs before search using a mask), **Post-filter** (search all, filter results after), or **IVF with partitioning** (map metadata to IVF cells). Pre-filtering is simplest:
```python
# Pre-filter: only search vectors where metadata_condition holds
valid_ids = np.array([i for i, m in enumerate(metadata) if m["category"] == "python"])
sub_index = faiss.IndexIDMap(index)
sub_index.add_with_ids(vectors[valid_ids], valid_ids)
distances, indices = sub_index.search(query, k=10)
```

**Q91: When would you use IndexIVFFlat vs IndexHNSW in FAISS?**

A: **IVFFlat**: faster index build, lower memory per vector, good for very large datasets where you can tolerate slightly lower recall. Needs training data. **HNSW**: higher recall, no training needed, faster queries for moderate datasets, but higher memory and slower index build. For most use cases <10M vectors, HNSW is preferred. For >100M, IVF_PQ may be necessary.

**Q92: How do you implement a complete vector search pipeline with FAISS for RAG?**

A:
```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Index documents
doc_embeddings = model.encode(documents).astype("float32")
dim = doc_embeddings.shape[1]
index = faiss.IndexHNSWFlat(dim, 32)
index.hnsw.efConstruction = 200
index.add(doc_embeddings)

# Query
query_emb = model.encode([query]).astype("float32")
distances, indices = index.search(query_emb, k=10)
results = [documents[i] for i in indices[0]]
```

---

## RAG Pipeline Implementation (Q93–Q100)

**Q93: What are the key stages of a RAG pipeline?**

A: 1) **Document loading** (PDF, HTML, DB), 2) **Chunking** (split into passages), 3) **Embedding generation**, 4) **Vector store ingestion**, 5) **Query processing** (expansion, routing), 6) **Retrieval** (similarity search), 7) **Reranking** (cross-encoder), 8) **Context assembly** (prompt construction), 9) **LLM generation**, 10) **Evaluation** (faithfulness, relevance).

**Q94: Compare chunking strategies: fixed-size, semantic, and recursive.**

A: **Fixed-size**: split every N characters/tokens with overlap. Simple, fast, but may split mid-sentence. **Semantic**: use embeddings to find natural break points. Higher quality, but slower and more complex. **Recursive** (LangChain): split on `["\n\n", "\n", ".", " "]` recursively. Good default—respects document structure. Chunk size typically 256–1024 tokens with 10-20% overlap.

**Q95: How do you implement retrieval strategies: similarity, MMR, and threshold?**

A: **Similarity**: return top-K most similar (default). **MMR (Maximal Marginal Relevance)**: balance relevance with diversity, reducing redundant chunks. **Threshold**: filter out results below a similarity score.
```python
# Similarity (basic)
results = index.search(query_emb, k=10)

# MMR (LangChain)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10, "fetch_k": 50, "lambda_mult": 0.7}
)

# Threshold
results = [r for r in raw_results if r.score > 0.75]
```

**Q96: What is context assembly and why does it matter for generation quality?**

A: Context assembly is constructing the prompt with retrieved chunks. Strategies: simple concatenation, ranked placement (most relevant first), metadata-aware formatting (include source, date), deduplication, and token budget management (fill context window without truncation). Poor assembly leads to LLM confusion, hallucinations, or ignoring relevant context.

**Q97: How do you evaluate RAG system quality?**

A: Key metrics: **Faithfulness** (does the answer stay grounded in retrieved context?), **Answer relevance** (does it answer the question?), **Context relevance** (are retrieved chunks relevant?), **Context recall** (did we retrieve all necessary information?). Use RAGAS framework or LLM-as-judge with test sets. Create evaluation datasets with query-context-answer triples.

**Q98: What are common RAG failure modes and how do you mitigate them?**

A: **Poor retrieval** (missing relevant docs): improve chunking, try hybrid search. **Too much context** (LLM ignores relevant chunks): use reranking, reduce context. **Hallucination despite context**: improve prompt, use grounded generation. **Stale information**: implement refresh pipeline. **Ambiguous queries**: add query expansion/clarification step.

**Q99: How do you implement a recursive document loader in Python for multiple file types?**

A:
```python
from pathlib import Path

def load_documents(path: Path) -> list[dict]:
    documents = []
    for file in path.rglob("*"):
        if file.suffix == ".pdf":
            text = extract_pdf(file)
        elif file.suffix == ".md":
            text = file.read_text()
        elif file.suffix == ".py":
            text = f"# File: {file.name}\n{file.read_text()}"
        else:
            continue
        documents.append({"source": str(file), "content": text})
    return documents
```

**Q100: How would you design a production RAG system end-to-end, from ingestion to serving?**

A: **Ingestion**: document loader → chunker → embedding model → vector store (Milvus) + metadata DB (PostgreSQL). Use a message queue (pgmq/Redis) for async processing. **Serving**: query → optional expansion → hybrid search (dense + sparse) → rerank (cross-encoder) → context assembly → LLM → streaming response. **Monitoring**: log queries, retrieval results, latency, faithfulness scores. **Evaluation**: periodic RAGAS eval on golden dataset. **Infrastructure**: vector store (Milvus cluster), relational DB (PostgreSQL), cache (Redis), monitoring (Prometheus/Grafana).
