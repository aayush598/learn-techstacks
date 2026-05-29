# Vector Database — 100 Interview Q&A
> Based on real-world RAG pipelines, AI agent architectures, and production vector search systems. Covers Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS, and core ANN concepts.

---

## 1. Fundamentals & Concepts (Q1–Q20)

**Q1: What is a vector database and how is it different from a traditional database?**
A: A vector database stores and indexes vector embeddings for fast similarity search. Unlike traditional databases (which query exact matches on structured data via B-trees/hash indexes), vector databases use Approximate Nearest Neighbor (ANN) algorithms to find "most similar" vectors by distance metrics. They are purpose-built for high-dimensional similarity search at scale.

**Q2: Explain the concept of embeddings and why they are the foundation of vector databases.**
A: Embeddings are dense numerical representations of data (text, images, audio) produced by neural networks. They capture semantic meaning in a high-dimensional vector space where similar items cluster together. Vector databases index these embeddings so you can search by meaning rather than keywords — enabling semantic search, recommendations, and RAG.

**Q3: What is the "curse of dimensionality" and how does it affect vector search?**
A: As dimensions increase, the volume of space grows exponentially, making distances converge and nearest-neighbor search degrade toward random. Most ANN algorithms struggle beyond ~1000 dimensions. Solutions include dimensionality reduction (PCA, UMAP), quantization, and using specialized indexes (IVF, HNSW) designed for high-D spaces.

**Q4: What is the difference between ANN (Approximate Nearest Neighbor) and KNN (K-Nearest Neighbors)?**
A: KNN is exact — it checks every vector to find the true k nearest neighbors. ANN is approximate — it trades a small accuracy loss for massive speed gains (10-100x). ANN uses index structures (HNSW, IVF, PQ) to prune the search space. Vector databases always use ANN for production scale.

**Q5: What are the key similarity metrics used in vector databases?**
A: 
1. Cosine similarity — measures angle between vectors (range [-1,1]); popular for text embeddings
2. Euclidean distance (L2) — straight-line distance; sensitive to magnitude
3. Dot product — measures overlap; used when embeddings are normalized
4. Manhattan distance (L1) — sum of absolute differences; robust to outliers
5. Hamming distance — for binary vectors

**Q6: When would you choose cosine similarity over dot product?**
A: Cosine similarity is preferred when vector magnitude is not meaningful — e.g., text embeddings where document length shouldn't affect similarity. Dot product is preferred when both direction and magnitude matter — e.g., collaborative filtering where user preference strength is informative. Many normalized embeddings make cosine and dot product equivalent.

**Q7: What is the role of vector databases in RAG (Retrieval-Augmented Generation)?**
A: In RAG, the vector database stores chunked document embeddings. On query, the input is embedded with the same model, and the vector DB returns the most semantically relevant chunks. These chunks are fed as context to an LLM, enabling grounded generation without retraining. This solves LLM hallucination and knowledge cutoff problems.

**Q8: How does a vector database handle metadata filtering alongside vector search?**
A: Most vector DBs support "hybrid search" — you specify a vector similarity query + metadata filters (e.g., `WHERE category = 'finance'`). Two approaches: pre-filtering (apply metadata filter first, then search) — fast for selective filters but can miss neighbors; post-filtering (search first, then filter) — accurate but may return fewer results. Some DBs (Qdrant, Milvus) do filtered ANN natively.

**Q9: What is the difference between dense and sparse vectors? Which does a vector DB support?**
A: Dense vectors are low-dimensional, fully populated arrays (e.g., 768-dim from BERT). Sparse vectors are high-dimensional with mostly zeros (e.g., 50K-dim bag-of-words). Vector DBs primarily support dense vectors for ANN search. Sparse search is typically handled by inverted indexes (like Elasticsearch). Some DBs (Weaviate, Qdrant) now support hybrid dense + sparse search.

**Q10: Explain the CAP theorem as it applies to vector databases.**
A: Like distributed DBs, vector DBs face CAP tradeoffs:
- CP systems (e.g., Milvus in standalone mode) prioritize consistency over availability during partitions
- AP systems (e.g., Weaviate, Qdrant) prioritize availability and eventual consistency
- Most production vector DBs favor AP with tunable consistency for reads

**Q11: What is meant by "recall" in the context of vector search?**
A: Recall measures the fraction of true nearest neighbors returned by an ANN search. If exact KNN returns 100 relevant items and ANN returns 90, recall = 90%. Production systems typically target 95-99% recall. Higher recall requires more index probes / wider search, which increases latency.

**Q12: How does indexing work in a vector database at a high level?**
A: Raw vectors are passed to an index builder that organizes them into a data structure optimized for ANN search. During indexing, vectors are clustered (IVF), graph-connected (HNSW), or quantized (PQ). The index is stored alongside metadata. On query, the index prunes the search space to a fraction of the total vectors, returning approximate nearest neighbors.

**Q13: What is a vector dimension and how do you choose the right dimensionality?**
A: Dimension = the number of values in each vector. Common sizes: 384 (all-MiniLM-L6-v2), 768 (BERT-base), 1024 (OpenAI ada-002), 1536 (text-embedding-3-small). Higher dimensions capture more nuance but increase storage, query latency, and curse-of-dimensionality issues. Choose the dimension of the embedding model required for your task.

**Q14: Explain the difference between exhaustive search and approximate search.**
A: Exhaustive (flat) search computes distance against every vector — O(n) per query, 100% recall, but impractical beyond ~10K vectors. Approximate search uses an index to limit comparisons — O(log n) or O(sqrt(n)), 95-99% recall, necessary at scale.

**Q15: Can you use a vector database for keyword search?**
A: Not natively — vector DBs search by semantic similarity, not lexical matching. However, hybrid search approaches (combining BM25 + vector) in systems like Weaviate, Qdrant, or Elasticsearch's vector plugin allow both. For pure keyword search, an inverted index (Elasticsearch) is better.

**Q16: How do vector databases handle CRUD operations in real-time?**
A: Inserts: vectors are added to a buffer or the index dynamically (depends on DB — some rebuild, some support incremental insertion). Updates: delete old vector + insert new. Deletes: tombstone marking + periodic compaction. Reads: direct lookup by ID + vector search. Real-time ingest is supported but may require index tuning (e.g., HNSW vs IVF rebuild penalties).

**Q17: What is a "collection" or "index" in vector DB terminology?**
A: A collection (Weaviate/Qdrant) or index (Milvus/Pinecone) is the top-level container that holds vectors, metadata, and configuration (dimension, metric, index type). Comparable to a table in relational DBs. Each collection has a fixed vector dimension and distance metric set at creation.

**Q18: What is the role of an embedding model in a vector database pipeline?**
A: The embedding model converts raw data (text, images, audio) into vectors that the database indexes. Consistency is critical — you must use the SAME embedding model for indexing and querying to ensure vectors are in the same semantic space. Many vector DBs offer built-in embedding inference (Weaviate modules, Qdrant inference).

**Q19: Explain the concept of a "vector database vs vector index library (FAISS)."**
A: FAISS is a library — you manage storage, persistence, scaling, CRUD, and filtering yourself. A vector DB is a full system — it handles data management, persistence, distributed scaling, metadata filtering, backups, and provides an API. For production, use a vector DB. For research/experimentation, FAISS is fine.

**Q20: What are the most popular vector databases in 2025-2026?**
A: Pinecone (fully managed, easiest to start), Weaviate (open-source, hybrid search, GraphQL), Qdrant (Rust-based, fast, filtering-first), Milvus/Zilliz (cloud-native, Kubernetes-native), Chroma (lightweight, developer-friendly, embedded), Elasticsearch (with vector plugin), pgvector (PostgreSQL extension).

## 2. Vector Indexing & ANN Algorithms (Q21–Q40)

**Q21: Explain the HNSW (Hierarchical Navigable Small World) algorithm.**
A: HNSW builds a multi-layer graph. Bottom layer has all vectors; upper layers have progressively fewer. Search starts at the top layer (coarse) and descends, using greedy graph traversal at each level. Construction parameters: M (connections per node, default 16), ef_construction (search breadth during build). Query parameters: ef (search breadth). HNSW offers O(log n) search with high recall.

**Q22: What are the Pros and Cons of HNSW compared to IVF?**
A: Pros: faster queries (log n vs sqrt(n)), higher recall, no training phase. Cons: higher memory usage (graph edges), slower indexing (O(n log n) insertion), larger disk footprint. HNSW is best for read-heavy workloads; IVF is better for write-heavy with limited memory.

**Q23: How does IVF (Inverted File Index) work?**
A: IVF partitions the vector space into nlist clusters using k-means during training. At query time, the closest nprobe clusters are searched exhaustively. IVF reduces search from all vectors to vectors in the nearest clusters. Tuning: larger nlist = more clusters, finer granularity; larger nprobe = higher recall, slower query.

**Q24: What is Product Quantization (PQ) and when would you use it?**
A: PQ compresses vectors by splitting them into sub-vectors and quantizing each with a small codebook. A 768-dim vector might become 96 bytes instead of 3072 bytes (96% compression). Used for memory-constrained scenarios — reduced recall but enables billion-scale search on a single machine. Often combined with IVF as IVF-PQ.

**Q25: Compare IVF-Flat vs IVF-PQ vs IVF-SQ.**
A: 
- IVF-Flat: full-precision vectors in each cluster — highest recall, highest memory
- IVF-PQ: compressed vectors via product quantization — lower memory (4-8x), slightly lower recall
- IVF-SQ: scalar quantization (float32 → uint8) — 4x compression, moderate recall loss
- Trade-off: memory vs accuracy. IVF-Flat for high accuracy; IVF-PQ for scale.

**Q26: What is the ef parameter in HNSW and how does it affect performance?**
A: ef (exploration factor) controls how many candidates are examined during HNSW search. Higher ef = higher recall, higher latency. Default ef is often 10-50. Rule of thumb: start with ef = k * 10 (where k is number of results). Ef can be tuned per-query for dynamic accuracy-latency tradeoffs.

**Q27: How does a DiskANN index differ from in-memory HNSW?**
A: DiskANN (Microsoft) stores vectors on SSD with a compressed HNSW-like graph in memory. It uses Vamana (a variant of HNSW) optimized for SSD reads — supports billion-scale datasets on a single machine ($400 cheaper than RAM). Latency is ~5-10ms vs <1ms for in-memory. Used by Qdrant (on-disk mode) and others.

**Q28: What is the "M" parameter in HNSW construction?**
A: M is the maximum number of connections per node per layer (default 16 in most implementations). Higher M = more connected graph, better recall, more memory (each edge is ~4-8 bytes). Lower M = less memory, faster indexing, potential recall drop. For most use cases, M=16-32 is recommended.

**Q29: What happens to an ANN index when you insert new vectors?**
A: Behavior depends on index type:
- HNSW: incremental insertion is native — new vectors are added to graph dynamically without full rebuild
- IVF: insertions may distort cluster balance over time; periodic reclustering recommended
- PQ-based: adding vectors requires recomputing codebooks — bulk rebuild needed
- Most vector DBs buffer writes and periodically merge/flush to the main index

**Q30: Explain the difference between flat (brute force) indexing and ANN indexing.**
A: Flat index stores vectors as-is without any structure; query = compute distance to every vector. ANN index organizes vectors (graph, clusters, quantized codes) for sub-linear search. Flat = 100% recall, O(n) time. ANN = 95-99% recall, O(log n) or O(sqrt(n)) time. Flat is only used for small datasets (~10K) or as a baseline.

**Q31: What is a "filtered ANN" search and how does Qdrant implement it?**
A: Filtered ANN combines vector similarity with scalar metadata filters. Qdrant uses a "payload index" alongside the vector index — during search, it intersects HNSW graph traversal with filter conditions. It can pre-filter (using filter as mask) or use a "oversampling" strategy (fetch more candidates, then apply filter). Qdrant's cardinality estimation chooses the optimal strategy automatically.

**Q32: What is the ef_construction parameter in HNSW?**
A: ef_construction controls search width during HNSW graph building. Higher values = better quality graph (higher recall), slower build time. Typical range: 100-500. Must be balanced against M and dataset size.

**Q33: How does Milvus handle indexing with its Knowhere library?**
A: Milvus uses Knowhere (a unified ANN framework) which wraps multiple index types: IVF, HNSW, PQ, DiskANN, etc. Knowhere provides a consistent API for index building, search, and serialization. Milvus automatically selects index type based on data size and configuration, and supports both CPU and GPU-accelerated indexing.

**Q34: What is the role of quantization in reducing vector storage?**
A: Quantization reduces precision of vector components (float32→uint8 or binary) or applies product quantization to split-and-encode. This reduces memory footprint by 4-32x, enabling larger datasets in RAM, but introduces accuracy loss. Scalar quantization is common — maps float range to int range with minimal recall drop (<1%).

**Q35: How does Weaviate handle multi-vector indexing (named vectors)?**
A: Weaviate supports multiple named vectors per object — each with its own embedding model, index type, and distance metric. For example, an article can have a "title_vector" (768-dim cosine) and an "image_vector" (512-dim euclidean). Search queries target specific named vectors, enabling multi-modal hybrid search.

**Q36: What is the "golden vector" or "centroid" in IVF?**
A: In IVF, centroids are the cluster centers learned during k-means training. Each vector is assigned to the nearest centroid. During search, the closest centroids to the query are found, and only their assigned vectors are searched. The number of centroids (nlist) determines granularity.

**Q37: Can you use multiple ANN algorithms in the same vector database?**
A: Yes — most vector DBs support multiple index types per collection. Milvus allows switching index types (IVF_FLAT, HNSW, DISKANN) on the same collection. Qdrant supports HNSW only (with on-disk mode). Pinecone uses a proprietary algorithm. Weaviate supports HNSW with optional flat mode. The choice depends on workload.

**Q38: How does Chroma DB handle indexing by default?**
A: Chroma uses HNSW (via hnswlib) for ANN search by default. It additionally supports brute-force for small datasets and configurable index parameters (ef, M). Chroma automatically switches to brute-force below a configurable threshold (default 10K vectors).

**Q39: What is a "multi-vector" or "multi-representation" index?**
A: Instead of one vector per document, multiple vectors per document (e.g., one per paragraph or sentence). This improves retrieval granularity but increases storage. Late interaction models (ColBERT) use multi-vector representations. Some vector DBs support this natively.

**Q40: How do you benchmark ANN index performance?**
A: Key metrics: recall@k (accuracy), queries-per-second (QPS, throughput), latency p50/p99, index build time, memory usage. Standard benchmarks: ANN-Benchmarks (http://ann-benchmarks.com) tests HNSW, IVF, DiskANN, etc. on datasets like SIFT (128-dim), GIST (960-dim), GloVe (300-dim), MNIST.

## 3. Operations, CRUD & Data Management (Q41–Q60)

**Q41: How does a vector database handle duplicate vectors?**
A: Most vector DBs don't deduplicate by vector content — they use unique IDs as primary keys. Inserting the same vector with a new ID creates a new entry (duplicate). Some DBs allow upsert based on ID. To deduplicate by content, you'd need to query for near-duplicates before insert.

**Q42: What happens when you exceed the dimension limit of a collection?**
A: The dimension is set at collection creation and cannot be changed. Inserting vectors with mismatched dimensions throws an error. To use a different dimension, you must create a new collection and re-index. Some DBs (Weaviate) allow multi-vector classes with different dimensions.

**Q43: Explain vectors namespacing and multi-tenancy support in vector DBs.**
A: Most vector DBs support multi-tenancy via:
- Partitioning (Pinecone: namespaces; Qdrant: collections per tenant)
- Metadata filtering (Weaviate: class-level filtering; Milvus: partition key)
- Separate indexes per tenant (performance isolation but higher resource usage)
- Tenant isolation at API level

**Q44: How do vector databases handle data persistence and durability?**
A: Vectors are persisted to disk (usually as mmap files or SSTables). Write-ahead log (WAL) for crash recovery. Periodic flushing to main index. Snapshots for backup. Replication for high availability. In-memory indexes are rebuilt from disk on restart. Milvus uses etcd + object storage; Qdrant uses fsync for durability.

**Q45: What is the difference between batch ingestion and streaming ingestion?**
A: Batch ingestion: pre-compute all embeddings, bulk-insert into DB. Fast ingestion but higher memory spike. Streaming ingestion: insert vectors one-by-one as data arrives. Lower throughput but real-time availability. Some DBs (Qdrant, Weaviate) batch internally; others (Milvus) have explicit flush commands.

**Q46: How does a vector database handle index rebuilding?**
A: Triggered by: config change (index type), data distribution drift, scheduled maintenance. During rebuild, reads still serve from old index; writes go to new index. After rebuild, atomic swap. Some DBs (Milvus) support online index building; others require downtime or duplicate collection.

**Q47: What is a "point" in vector database terminology?**
A: A point (Qdrant) or object (Weaviate) is a single record containing: a unique ID, the vector, and optional payload/metadata. In Pinecone: "vector" with ID and metadata. In Milvus: "entity" with fields + vector.

**Q48: How do you update the metadata of a vector without changing its embedding?**
A: Most vector DBs support updating payload/metadata independently of the vector. Qdrant: `set_payload` operation. Weaviate: update object properties. Pinecone: `update` with only metadata field. This does not affect the index structure.

**Q49: What is a "full scan" and when does a vector DB resort to one?**
A: A full scan iterates every vector, computing distance for each — equivalent to brute-force KNN. Occurs when: no index is built, index is invalidated, or filter is too restrictive for ANN pruning. Full scans are expensive (O(n)) and should be avoided in production.

**Q50: How do vector databases support time-based or dynamic data (time-decay)?**
A: Approaches:
- Metadata filtering: add timestamp field, filter by time range at query time
- Time-decayed scoring: recompute similarity = (1 - decay_factor) * vector_sim + decay_factor * recency
- Data retention policies: TTL-based or scheduled deletion of old vectors
- Separate indexes per time window for scrolling windows

**Q51: What is the MVCC model in vector databases?**
A: Multi-Version Concurrency Control ensures consistent reads during writes. Qdrant uses MVCC for segment-based architecture — writes go to new segments while reads use a snapshot of segments at query start. This prevents read-write conflicts without locks.

**Q52: How does compaction work in Qdrant?**
A: Qdrant stores vectors in segments. Over time, segments accumulate (from updates, deletes, upserts). Compaction merges smaller segments into larger ones, reclaims storage from deleted vectors, and rebuilds HNSW graphs for merged data. Can run in background or be triggered manually.

**Q53: What are the tradeoffs of storing vectors on SSD vs in RAM?**
A: RAM: sub-millisecond latency, high throughput, expensive, limited capacity. SSD (on-disk): 5-20ms latency, lower throughput, cheaper, near-infinite capacity. Hybrid: hot vectors in RAM cache, cold on SSD. Milvus DiskANN, Qdrant on-disk, and Weaviate with disk-based vectors support SSD.

**Q54: How do you export or migrate vectors from one vector DB to another?**
A: Common approaches:
- Bulk export via API (iterate over all vectors, stream to file)
- Snapshot/restore (vendor-specific format)
- CSV/JSONL export with metadata
- Migration tools (e.g., VectorDBBench, custom scripts)
- Challenge: different DBs have different ID formats, metadata schemas, and vector representations

**Q55: What is a "segment" in Qdrant / "shard" in Milvus?**
A: Segment (Qdrant): self-contained unit with its own HNSW graph, vectors, payload index, and WAL. Multiple segments serve queries in parallel, merged at query time. Shard (Milvus): horizontal partition of data. Segments enable efficient updates/deletes; shards enable horizontal scaling.

**Q56: How does a vector DB handle storing vectors larger than available memory?**
A: Options:
- On-disk index (DiskANN/Qdrant on-disk): vectors on SSD, lightweight graph in memory
- Memory-mapped files (mmap): OS handles paging; vectors swapped in/out as needed
- Tiered storage: hot (RAM) + warm (SSD) + cold (object storage)
- Partitioning: split data across machines

**Q57: What is the purpose of a "write-ahead log" (WAL) in vector databases?**
A: WAL logs all mutations (insert, update, delete) before applying to the index. On crash recovery, the WAL is replayed to restore consistency. Qdrant uses WAL per segment; Milvus uses binlog. Without WAL, a crash could corrupt the index or lose recent writes.

**Q58: How do you handle vector deletion without rebuilding the entire index?**
A: 
- Tombstone marking: mark ID as deleted, filter out during search. Index structure remains unchanged.
- Soft delete: remove from search results but keep in index.
- Periodic compaction: physically remove deleted vectors and rebuild affected segments.
- HNSW: deleting nodes from a graph is complex; most DBs use tombstone + periodic rebuild.

**Q59: What is a "payload index" and how is it different from a vector index?**
A: Payload index (Qdrant/Weaviate) indexes metadata fields (keywords, numbers, geo) for fast filtering. It's a traditional inverted index or B-tree, NOT for vectors. The vector index handles similarity; the payload index handles filtering. Both are combined during query execution.

**Q60: Can you store non-vector data (blobs, full text) in a vector DB?**
A: Yes — most vector DBs store original data as part of the record. Weaviate stores objects (with vector + properties). Qdrant stores payload (arbitrary JSON). Pinecone supports metadata as key-value pairs. However, vector DBs are not optimized for blob storage — use object storage for large files and store references in the DB.

## 4. Similarity Search & Query Patterns (Q61–Q75)

**Q61: What is "hybrid search" and how is it implemented in vector DBs?**
A: Hybrid search combines vector similarity (ANN) with keyword/text search (BM25). Results are merged via reciprocal rank fusion (RRF) or weighted scoring. Weaviate implements with its `bm25` + `nearText` filters. Qdrant supports via `should` queries. This gives best of both: semantic understanding + exact keyword matching.

**Q62: Explain "maximum marginal relevance" (MMR) and its use in vector search.**
A: MMR balances relevance and diversity in results. After finding top-k similar vectors, MMR reranks to select a subset that is both relevant to the query AND dissimilar from each other. Prevents redundant results. Formula: MMR = λ * sim(query, doc_i) - (1-λ) * max(sim(doc_i, doc_j)). Used in RAG for diverse context.

**Q63: What is "late interaction" and how does ColBERT use it?**
A: Late interaction (ColBERT) encodes query and document into separate multi-vector representations and computes similarity via MaxSim (sum of max cosine between each query token and all document tokens). More accurate than single-vector embeddings but slower to compute. Plaid index enables efficient approximate late interaction search.

**Q64: What is the role of "query rewriting" before vector search?**
A: Query rewriting transforms raw user queries into forms better suited for vector similarity. Examples: expanding acronyms, correcting typos, decomposing complex queries, adding synonyms. Improves retrieval quality. Often done by an LLM before embedding. e.g., "What's the price?" → "What is the cost/pricing/subscription fee?"

**Q65: How do you implement multi-stage retrieval with a vector database?**
A: 
Stage 1 (ANN): fast approximate search, return top-100 candidates
Stage 2 (Rerank): apply a more expensive cross-encoder or LLM-based scorer to top-100
Stage 3 (Filter): apply business logic, deduplication, diversity constraints
This architecture combines speed of ANN with accuracy of expensive rerankers.

**Q66: What is the difference between "fetch" and "search" in vector DB operations?**
A: Fetch: retrieve a specific vector by its unique ID (O(1) by hash lookup, no similarity computation). Search: find vectors similar to a query vector (ANN search, O(log n)). They serve different purposes — fetch for direct lookup, search for discovery.

**Q67: How does score normalization work in vector search?**
A: Raw distance scores (cosine, euclidean, dot) aren't inherently interpretable. Normalization techniques:
- Min-max normalization (map scores to [0,1])
- Z-score (based on score distribution)
- Sigmoid calibration (fit to probability-like scores)
- Weaviate uses "certainty" (normalized to [0,1]); Qdrant uses raw distance

**Q68: What is "group by" or "aggregation" in a vector search context?**
A: Search results grouped by a metadata field. For example: find top-10 products similar to query, but return at most 1 per category. Qdrant supports `group_by` natively. Milvus supports grouping via post-processing. Avoids result domination by a single category.

**Q69: Explain the concept of "pagination" in vector queries.**
A: ANN search returns top-k results sorted by distance. Pagination (offset) is tricky — retrieving "results 101-120" requires re-running search with a larger k (e.g., 120), which is expensive. Alternatives: scroll API (cursor-based), and avoid deep pagination in vector search.

**Q70: What is a "vector search playground" and how does it help?**
A: Tools like Weaviate Console, Qdrant UI, and Pinecone console let you test similarity queries visually — inspect nearest neighbors, tune parameters (ef, M), compare metrics. Essential for understanding embedding quality and index behavior before production.

**Q71: How does the vector database handle searching for "nothing" (query of all zeros)?**
A: A zero vector is equidistant from all vectors in cosine space, and at origin in euclidean. Search with zero query vector returns arbitrary results (based on index structure, not semantics). Most validation layers reject zero vectors.

**Q72: Can you do multi-vector search (search by multiple query vectors at once)?**
A: Yes — supported by some DBs:
- Qdrant: multiple query vectors per request with `recommend` API
- Milvus: hybrid search across multiple vector fields
- Weaviate: named vectors allow different queries on different vector types
- Use cases: cross-modal search (image + text), multi-faceted recommendations

**Q73: What is "contextual retrieval" and how does it relate to vector search?**
A: Contextual retrieval augments a chunk with surrounding context before embedding — e.g., prepending "This chunk is from a document about [topic], specifically section [title]" to the chunk text. Improves retrieval quality because the embedding captures context, not just the isolated chunk.

**Q74: How does a vector DB handle queries for the "most dissimilar" vectors?**
A: Search with the opposite direction (cosine: farthest = dot negative; euclidean: farthest = maximized distance). Most DBs don't support "farthest neighbor" natively. You can achieve it by searching with the negated query vector (for dot product) or by inverting distances in post-processing. Limited practical use.

**Q75: What is the typical query latency budget for vector search in a user-facing RAG app?**
A: For interactive RAG: budget 200-500ms total for retrieval (embedding + vector search + reranking). Vector search should take <100ms. For batch/analytics: seconds to minutes. Acceptable latency depends on user expectations — lower for chatbots, higher for research tools.

## 5. Performance, Scaling & Production (Q76–Q90)

**Q76: How do you scale a vector database horizontally?**
A: 
- Sharding: partition data across nodes by ID hash or metadata key
- Replication: copy data to multiple nodes for HA and read throughput
- Distributed ANN: each node searches its local index; results merged at coordinator
- Milvus: worker nodes + message queue + object storage (cloud-native)
- Qdrant: cluster mode with Raft consensus
- Weaviate: replication factor + auto-sharding with consistent hashing

**Q77: What is a "distributed ANN" and how does it maintain recall?**
A: Each node maintains its own ANN index over a subset of data. Query is sent to all nodes (scatter), each does local ANN search, results are aggregated (gather), and merged by distance. Recall can degrade because true nearest neighbors might be spread across nodes. Oversampling (each node returns 2x its share) mitigates recall loss.

**Q78: How does caching improve vector search performance?**
A: 
- Query result cache: cache frequent queries with TTL
- Embedding cache: avoid re-embedding common queries
- HNSW node cache: hot nodes in RAM
- Filter result cache: pre-compute filtered subsets for frequent filters
- OS page cache: mmap-based DBs benefit naturally

**Q79: What's the difference between "throughput" and "latency" in vector DB benchmarking?**
A: Throughput = queries per second (QPS) under concurrent load. Latency = time per query (p50, p95, p99). They trade off — batching increases throughput but adds latency. Typical target: <100ms p95 latency for interactive apps. Use concurrency testing to measure throughput-latency curve.

**Q80: How do you handle vector DB backups and disaster recovery?**
A: 
- Snapshots: point-in-time copy of index + data (Qdrant: snapshot API; Milvus: backup tool)
- Replication: multi-node cluster survives node failure
- Object storage: persist WAL + index snapshots to S3/GCS
- Cross-region replication for geo-redundancy
- Recovery: restore snapshot + replay WAL

**Q81: What monitoring metrics are essential for a production vector DB?**
A: 
- Query latency (p50, p95, p99)
- QPS and throughput
- Memory usage (index + buffers)
- Disk usage and I/O
- Index build progress
- Recall (sample query vs exact search periodically)
- Error rate (timeouts, OOM, rate limits)
- Replication lag

**Q82: How do vector databases handle hot spots (popular vectors queried frequently)?**
A: 
- Caching: frequently accessed vectors cached in memory
- Load balancing: distribute queries across replicas
- Consistent hashing: prevent imbalanced shard access
- Rate limiting: per-tenant or per-user limits
- Separate hot storage tiered from cold

**Q83: What is "rate limiting" in managed vector DB APIs (Pinecone, Qdrant Cloud)?**
A: Rate limits cap QPS or throughput (MB/s) per index/project to prevent noisy neighbor issues. Pinecone: limits based on pod type (s1: 100 QPS, p1: 500 QPS). Qdrant Cloud: based on cluster size. Exceeding returns 429 errors. Mitigation: client-side retry with exponential backoff.

**Q84: How do you choose between a managed vector DB and self-hosted?**
A: Managed (Pinecone, Qdrant Cloud, Weaviate Cloud): zero ops, auto-scaling, SLAs, but vendor lock-in and higher cost at scale. Self-hosted (Milvus, Qdrant, Weaviate): full control, lower cost at scale, but Ops overhead. Decision factors: team size, scale, compliance, in-house DevOps expertise.

**Q85: What is the cost structure of a managed vector DB?**
A: Typically based on:
- Vector count and dimension
- Query throughput (QPS)
- Storage (RAM vs disk)
- Replication factor
- Data transfer
- Pinecone: per pod-hour; Qdrant Cloud: per cluster-hour; Weaviate Cloud: per unit-hour
- At scale, vector DB can be a significant cost — optimize via quantization, tiered storage

**Q86: How do you A/B test different vector databases for your use case?**
A: 
1. Define metrics: recall@k, latency p95, QPS, cost
2. Use VectorDBBench or ANN-Benchmarks with your dataset
3. Test with at least 2x your expected production scale
4. Measure build time, query speed, filter performance
5. Test failure scenarios (node loss, network partition)
6. Consider operational complexity

**Q87: What is "failure mode" for a vector DB during high load?**
A: Common failures:
- OOM (Killed): index too large for memory
- Connection pool exhaustion
- Slow queries piling up (thundering herd)
- Index rebuild failing mid-way
- Replication lag causing stale reads
- Mitigations: circuit breakers, bulkhead patterns, autoscaling

**Q88: How do you migrate from one vector DB to another in production?**
A: 
1. Dual-write to both DBs during migration
2. Backfill old data to new DB
3. Verify recall parity with sample queries
4. Gradually shift read traffic (10% → 50% → 100%)
5. Monitor latency, error rate, recall during cutover
6. Decommission old DB after validation period
Rollback plan: keep old DB running until fully validated.

**Q89: What is a "staging index" in Pinecone?**
A: Pinecone's serverless architecture uses "staging index" for bulk writes — higher throughput for ingestion but not searchable until promoted. This isolates indexing load from query serving. After indexing completes, the index is promoted to serving state.

**Q90: How do you optimize vector DB costs without sacrificing performance?**
A: 
- Quantization (float32 → binary reduces memory 32x, cost 32x)
- On-disk storage for cold vectors
- Tiered indexing (hot/warm/cold)
- Caching at application layer
- Delete stale/unused vectors
- Downsize during low traffic
- Choose the right pod type / instance size for workload

## 6. Ecosystem, Comparisons & Integration (Q91–Q100)

**Q91: How does pgvector compare to dedicated vector databases?**
A: pgvector is a PostgreSQL extension adding vector type + ANN indexes (IVF, HNSW). Pros: existing Postgres ecosystem, transactional consistency, no additional infra. Cons: limited ANN performance vs dedicated DBs, no distributed scaling, fewer features (no hybrid search natively). Best for: apps already on Postgres with <10M vectors.

**Q92: Compare Pinecone vs Weaviate vs Qdrant vs Milvus for production use.**
A: 
- Pinecone: easiest setup, fully managed, serverless option, highest cost, closed source
- Weaviate: strongest hybrid search, GraphQL API, open-source, modules for model inference
- Qdrant: fastest filtered search, Rust-based, memory-efficient, best Docker experience
- Milvus: most scalable, Kubernetes-native, GPU support, most complex to operate
- Choose based on: scale (Milvus/Qdrant for large), ease (Pinecone/Chroma), hybrid (Weaviate)

**Q93: How does Elasticsearch's vector search compare to dedicated vector DBs?**
A: Elasticsearch added ANN search via HNSW (Elastic 8.0+). Pros: single stack for full-text + vector, existing ecosystem, mature operations. Cons: vector performance lower than dedicated DBs, higher latency, limited to HNSW only, cost for dense vector storage. Best for: teams already on Elasticsearch with moderate vector scale.

**Q94: What is Chroma DB and when should you use it?**
A: Chroma is an open-source, embedded vector database for AI applications. Lightweight (pip install), stores data on disk or in-memory, simple Python API, integrates with LangChain and LlamaIndex. Best for: prototyping, small-scale apps, local development, tutorials. Not for production at scale.

**Q95: How do vector databases integrate with LangChain/LlamaIndex?**
A: Both frameworks provide unified vector store abstractions:
- LangChain: `vectorstores` interface with `similarity_search`, `as_retriever`
- LlamaIndex: `VectorStoreIndex` wrapping the DB
- Both support major DBs (Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS)
- Integration handles collection setup, embedding, search, metadata filtering, and retriever creation

**Q96: How does a vector database handle binary and float vectors in the same collection?**
A: Depends on the DB. Most require a single vector type per collection. Weaviate named vectors allow mixed. Binary vectors (each component is 0 or 1, stored as bits) use Hamming distance — 32x compression vs float32, good for near-duplicate detection. Float vectors are standard for semantic search.

**Q97: What is "sparse vector" support in modern vector DBs?**
A: Sparse vectors (e.g., from SPLADE) represent text as high-dimensional, mostly-zero vectors. Qdrant supports sparse vectors natively via `NamedVector` with `modifier: "sparse"`. Weaviate supports via `text2vec-transformers` module with sparse embeddings. Enables hybrid search combining dense semantic + sparse lexical matching.

**Q98: What is a "Tiered Index" architecture in vector databases?**
A: Tiered indexing splits data into hot (RAM), warm (SSD), and cold (object storage) tiers. Queries search tiers based on freshness/frequency. Milvus DiskANN + RAM cache implements this. Qdrant allows per-segment memory mode vs mmap mode. Reduces cost by keeping hot data in RAM and cold data on cheap storage.

**Q99: How does a vector database integrate with a streaming platform like Kafka?**
A: 
- Ingest: consume text/image from Kafka → embed → upsert to vector DB
- Realtime indexing: low-latency embedding + write path
- Qdrant: Kafka sink connector available
- Milvus: Pulsar for internal message queue; can integrate with Kafka for ingestion
- Weaviate: supports webhook automations for streaming

**Q100: What are the emerging trends in vector databases for 2026?**
A: 
1. Multi-modal vector search (text + image + audio + video unified)
2. On-device vector search (mobile, edge devices with embedded vector DBs)
3. SQL-native vector search (DuckDB, Postgres pgvector improvements)
4. Compute-storage separation for elasticity
5. Built-in embedding inference (reduce moving parts)
6. ColBERT-style late interaction support
7. Cost-efficient disk-based indexes (DiskANN maturation)
8. Agent-native vector stores (tool-calling interfaces for AI agents)
