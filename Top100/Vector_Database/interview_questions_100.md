# Vector Database — 100 Interview Q&A
> Based on real-world RAG pipelines, AI agent architectures, and production vector search systems. Covers Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS, and core ANN concepts.

---

## 1. Fundamentals & Concepts (Q1–Q20)

**Q1: What is a vector database and how is it different from a traditional database?**
A: A vector database stores and indexes vector embeddings for fast similarity search. Unlike traditional databases (which query exact matches on structured data via B-trees/hash indexes), vector databases use Approximate Nearest Neighbor (ANN) algorithms to find "most similar" vectors by distance metrics. They are purpose-built for high-dimensional similarity search at scale.

**Code:**
```python
import faiss
import numpy as np

d = 128
index = faiss.IndexFlatIP(d)                      # vector DB = index over embeddings
index.add(np.random.randn(1000, d).astype("float32"))
query = np.random.randn(1, d).astype("float32")
scores, ids = index.search(query, k=5)            # similarity, not exact-match SQL
print(ids)
```

**Q2: Explain the concept of embeddings and why they are the foundation of vector databases.**
A: Embeddings are dense numerical representations of data (text, images, audio) produced by neural networks. They capture semantic meaning in a high-dimensional vector space where similar items cluster together. Vector databases index these embeddings so you can search by meaning rather than keywords — enabling semantic search, recommendations, and RAG.

**Code:**
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embs = model.encode(["vector DBs power semantic search",
                     "Bananas are a fruit",
                     "SQL queries are exact matches"])
query = model.encode(["what is semantic search?"])[0]
sims = query @ embs.T / (np.linalg.norm(query) * np.linalg.norm(embs, axis=1))
print(embs.shape, sims)      # meaning clusters: "semantic search" ~ doc 0
```

**Q3: What is the "curse of dimensionality" and how does it affect vector search?**
A: As dimensions increase, the volume of space grows exponentially, making distances converge and nearest-neighbor search degrade toward random. Most ANN algorithms struggle beyond ~1000 dimensions. Solutions include dimensionality reduction (PCA, UMAP), quantization, and using specialized indexes (IVF, HNSW) designed for high-D spaces.

**Code:**
```python
import numpy as np

for dim in [2, 20, 200, 2000]:
    x = np.random.randn(5000, dim).astype("float32")
    y = np.random.randn(5000, dim).astype("float32")
    d = np.linalg.norm(x - y, axis=1)
    # distance std shrinks → neighbours become indistinguishable = the curse
    print(f"dim={dim:5d}  mean={d.mean():.2f}  std={d.std():.2f}")
```

**Q4: What is the difference between ANN (Approximate Nearest Neighbor) and KNN (K-Nearest Neighbors)?**
A: KNN is exact — it checks every vector to find the true k nearest neighbors. ANN is approximate — it trades a small accuracy loss for massive speed gains (10-100x). ANN uses index structures (HNSW, IVF, PQ) to prune the search space. Vector databases always use ANN for production scale.

**Code:**
```python
import faiss
import numpy as np

x = np.random.randn(50_000, 64).astype("float32")
flat = faiss.IndexFlatL2(64)                  # exact KNN: checks all 50K vectors
flat.add(x)
ivf = faiss.index_factory(64, "IVF100,Flat")  # ANN: prunes the search space
ivf.train(x); ivf.add(x)

q = np.random.randn(1, 64).astype("float32")
_, exact = flat.search(q, 10)
ivf.nprobe = 10
_, approx = ivf.search(q, 10)
print("overlap:", set(exact[0]) & set(approx[0]))
```

**Q5: What are the key similarity metrics used in vector databases?**
A: 
1. Cosine similarity — measures angle between vectors (range [-1,1]); popular for text embeddings
2. Euclidean distance (L2) — straight-line distance; sensitive to magnitude
3. Dot product — measures overlap; used when embeddings are normalized
4. Manhattan distance (L1) — sum of absolute differences; robust to outliers
5. Hamming distance — for binary vectors

**Code:**
```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 4.0, 6.0])
cosine    = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
euclid    = np.linalg.norm(a - b)
dot       = a @ b
manhattan = np.abs(a - b).sum()
hamming   = (a != b).mean()
print("cos", round(cosine, 3), "l2", round(euclid, 3), "dot", dot,
      "l1", manhattan, "hamming", hamming)
```

**Q6: When would you choose cosine similarity over dot product?**
A: Cosine similarity is preferred when vector magnitude is not meaningful — e.g., text embeddings where document length shouldn't affect similarity. Dot product is preferred when both direction and magnitude matter — e.g., collaborative filtering where user preference strength is informative. Many normalized embeddings make cosine and dot product equivalent.

**Code:**
```python
import numpy as np

u = np.array([1.0, 0, 0])                # same direction, different length
v = np.array([2.0, 0, 0])
print("cosine:", u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))   # 1.0, length ignored
print("dot   :", u @ v)                                             # 2.0, magnitude matters
n = lambda x: x / np.linalg.norm(x)
print("equal after normalising:", n(u) @ n(v))                      # cosine == dot per vector
```

**Q7: What is the role of vector databases in RAG (Retrieval-Augmented Generation)?**
A: In RAG, the vector database stores chunked document embeddings. On query, the input is embedded with the same model, and the vector DB returns the most semantically relevant chunks. These chunks are fed as context to an LLM, enabling grounded generation without retraining. This solves LLM hallucination and knowledge cutoff problems.

**Code:**
```python
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = ["Blender is free, open-source software",
          "RAG grounds LLM answers in retrieved context",
          "Paris is the capital of France"]
index = faiss.IndexFlatIP(384)
index.add(model.encode(chunks))

q = model.encode(["where is paris?"])
_, ids = index.search(q, 1)                # retrieve the relevant chunk
prompt = f"Answer using this context:\n{chunks[ids[0][0]]}"
print(prompt)                              # fed to the LLM as grounded context
```

**Q8: How does a vector database handle metadata filtering alongside vector search?**
A: Most vector DBs support "hybrid search" — you specify a vector similarity query + metadata filters (e.g., `WHERE category = 'finance'`). Two approaches: pre-filtering (apply metadata filter first, then search) — fast for selective filters but can miss neighbors; post-filtering (search first, then filter) — accurate but may return fewer results. Some DBs (Qdrant, Milvus) do filtered ANN natively.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.create_collection("docs", vectors_config=models.VectorParams(32, models.Distance.COSINE))
hits = client.query_points(
    collection_name="docs",
    query=[0.1] * 32,
    query_filter=models.Filter(must=[
        models.FieldCondition(key="category", match=models.MatchValue(value="finance"))]),
    limit=10)                               # vector sim + metadata filter, one call
print(len(hits))
```

**Q9: What is the difference between dense and sparse vectors? Which does a vector DB support?**
A: Dense vectors are low-dimensional, fully populated arrays (e.g., 768-dim from BERT). Sparse vectors are high-dimensional with mostly zeros (e.g., 50K-dim bag-of-words). Vector DBs primarily support dense vectors for ANN search. Sparse search is typically handled by inverted indexes (like Elasticsearch). Some DBs (Weaviate, Qdrant) now support hybrid dense + sparse search.

**Code:**
```python
import numpy as np
from scipy import sparse

dense = np.random.randn(768)                         # BERT-style, fully populated
sparse_v = sparse.csr_matrix([[0, 1, 0, 0, 3, 0]])  # 50K-dim, mostly zeros
print("dense shape:", dense.shape, "| sparse nnz:", sparse_v.nnz)
# dense → ANN in a vector DB; sparse → inverted index (BM25 / SPLADE)
```

**Q10: Explain the CAP theorem as it applies to vector databases.**
A: Like distributed DBs, vector DBs face CAP tradeoffs:
- CP systems (e.g., Milvus in standalone mode) prioritize consistency over availability during partitions
- AP systems (e.g., Weaviate, Qdrant) prioritize availability and eventual consistency
- Most production vector DBs favor AP with tunable consistency for reads

**Code:**
```python
class WritePath:
    def __init__(self, n_nodes):
        self.nodes = [None] * n_nodes
        self.quorum = n_nodes // 2 + 1

    def write(self, key, value, reachable):
        acks = sum(1 for n in reachable if n)
        return "committed" if acks >= self.quorum else "buffered"

#  CP: block until quorum ack → consistency first
#  AP: accept the write, replicate lazily → availability first
print(WritePath(3).write("v1", [0.1, 0.2], reachable=[True, False, False]))
```
**Q11: What is meant by "recall" in the context of vector search?**
A: Recall measures the fraction of true nearest neighbors returned by an ANN search. If exact KNN returns 100 relevant items and ANN returns 90, recall = 90%. Production systems typically target 95-99% recall. Higher recall requires more index probes / wider search, which increases latency.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(10_000, 64).astype("float32")
flat = faiss.IndexFlatL2(64); flat.add(x)              # exact KNN = ground truth
ann = faiss.index_factory(64, "IVF64,Flat"); ann.train(x); ann.add(x); ann.nprobe = 4
q = np.random.randn(10, 64).astype("float32")
_, exact = flat.search(q, 10)
_, approx = ann.search(q, 10)
recall = len(set(exact[0]) & set(approx[0])) / len(exact[0]) * 100
print(f"recall@10 = {recall:.0f}%")                     # fraction of true NN returned
```

**Q12: How does indexing work in a vector database at a high level?**
A: Raw vectors are passed to an index builder that organizes them into a data structure optimized for ANN search. During indexing, vectors are clustered (IVF), graph-connected (HNSW), or quantized (PQ). The index is stored alongside metadata. On query, the index prunes the search space to a fraction of the total vectors, returning approximate nearest neighbors.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(50_000, 96).astype("float32")
ivf = faiss.index_factory(96, "IVF128,Flat")   # index builder organises vectors
ivf.train(x)                                   # k-means learns 128 clusters
ivf.add(x)                                     # vectors assigned to clusters
q = np.random.randn(1, 96).astype("float32")
ivf.nprobe = 8                                 # prune search to 8 of 128 clusters
print(ivf.search(q, 5))
```

**Q13: What is a vector dimension and how do you choose the right dimensionality?**
A: Dimension = the number of values in each vector. Common sizes: 384 (all-MiniLM-L6-v2), 768 (BERT-base), 1024 (OpenAI ada-002), 1536 (text-embedding-3-small). Higher dimensions capture more nuance but increase storage, query latency, and curse-of-dimensionality issues. Choose the dimension of the embedding model required for your task.

**Code:**
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
v = model.encode(["hello"])                        # 384-dim
print("dim:", v.shape[1], "| bytes/vector:", v.nbytes)
```

**Q14: Explain the difference between exhaustive search and approximate search.**
A: Exhaustive (flat) search computes distance against every vector — O(n) per query, 100% recall, but impractical beyond ~10K vectors. Approximate search uses an index to limit comparisons — O(log n) or O(sqrt(n)), 95-99% recall, necessary at scale.

**Code:**
```python
import faiss, numpy as np, time

x = np.random.randn(200_000, 64).astype("float32")
q = np.random.randn(100, 64).astype("float32")
flat = faiss.IndexFlatL2(64); flat.add(x)              # O(n) exhaustive
hnsw = faiss.index_factory(64, "HNSW32"); hnsw.add(x)  # O(log n) approximate
for name, idx in [("flat", flat), ("hnsw", hnsw)]:
    t = time.perf_counter(); idx.search(q, 10)
    print(name, round((time.perf_counter() - t) / len(q) * 1e3, 3), "ms/query")
```

**Q15: Can you use a vector database for keyword search?**
A: Not natively — vector DBs search by semantic similarity, not lexical matching. However, hybrid search approaches (combining BM25 + vector) in systems like Weaviate, Qdrant, or Elasticsearch's vector plugin allow both. For pure keyword search, an inverted index (Elasticsearch) is better.

**Code:**
```python
from rank_bm25 import BM25Okapi
import numpy as np

docs = ["vector databases store embeddings", "bm25 counts term frequency"]
bm25 = BM25Okapi([d.split() for d in docs])
lex = bm25.get_scores("embeddings".split())      # exact lexical hits
sem = np.random.rand(len(docs))                  # vector scores from FAISS
hybrid = 0.6 * (lex / lex.max()) + 0.4 * sem     # fused score
print(hybrid)
```

**Q16: How do vector databases handle CRUD operations in real-time?**
A: Inserts: vectors are added to a buffer or the index dynamically (depends on DB — some rebuild, some support incremental insertion). Updates: delete old vector + insert new. Deletes: tombstone marking + periodic compaction. Reads: direct lookup by ID + vector search. Real-time ingest is supported but may require index tuning (e.g., HNSW vs IVF rebuild penalties).

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("docs", points=[models.PointStruct(id=1, vector=[0.1, 0.2, 0.3])])  # insert
client.upsert("docs", points=[models.PointStruct(id=1, vector=[0.1, 0.2, 0.9])])  # update
client.set_payload("docs", {"tag": "a"}, points=[1])                              # metadata
client.delete("docs", points_selector=models.PointIdsList(points=[1]))            # tombstone
# incremental ingest: HNSW grows natively; IVF/PQ need periodic rebuild/merge
```

**Q17: What is a "collection" or "index" in vector DB terminology?**
A: A collection (Weaviate/Qdrant) or index (Milvus/Pinecone) is the top-level container that holds vectors, metadata, and configuration (dimension, metric, index type). Comparable to a table in relational DBs. Each collection has a fixed vector dimension and distance metric set at creation.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="articles",                # the container ("table")
    vectors_config=models.VectorParams(size=384,          # fixed dimension
                                       distance=models.Distance.COSINE),  # fixed metric
)
print(client.get_collection("articles"))
```

**Q18: What is the role of an embedding model in a vector database pipeline?**
A: The embedding model converts raw data (text, images, audio) into vectors that the database indexes. Consistency is critical — you must use the SAME embedding model for indexing and querying to ensure vectors are in the same semantic space. Many vector DBs offer built-in embedding inference (Weaviate modules, Qdrant inference).

**Code:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # ONE encoder for both sides
doc = model.encode("How do I train a model?")
query = model.encode("model training")            # same model → same semantic space
print(float(query @ doc))                          # otherwise scores are meaningless
```

**Q19: Explain the concept of a "vector database vs vector index library (FAISS)."**
A: FAISS is a library — you manage storage, persistence, scaling, CRUD, and filtering yourself. A vector DB is a full system — it handles data management, persistence, distributed scaling, metadata filtering, backups, and provides an API. For production, use a vector DB. For research/experimentation, FAISS is fine.

**Code:**
```python
import faiss, numpy as np
# FAISS = library: you own storage, CRUD, scale and persistence
index = faiss.IndexFlatL2(128)
index.add(np.random.randn(10_000, 128).astype("float32"))
faiss.write_index(index, "/tmp/idx.faiss")        # manual save / load

# Vector DB = managed system: durability + API handled for you
from qdrant_client import QdrantClient, models
client = QdrantClient(":memory:")
client.create_collection("docs", models.VectorParams(128, models.Distance.L2))
```

**Q20: What are the most popular vector databases in 2025-2026?**
A: Pinecone (fully managed, easiest to start), Weaviate (open-source, hybrid search, GraphQL), Qdrant (Rust-based, fast, filtering-first), Milvus/Zilliz (cloud-native, Kubernetes-native), Chroma (lightweight, developer-friendly, embedded), Elasticsearch (with vector plugin), pgvector (PostgreSQL extension).

**Code:**
```python
# Same task, different 2025-26 vendors — all expose a collection/index call:
from qdrant_client import QdrantClient, models
client = QdrantClient(":memory:")                                  # Rust, filtering-first
client.create_collection("items", models.VectorParams(768, models.Distance.COSINE))
# pgvector:  CREATE EXTENSION vector; CREATE TABLE t (v vector(768));
# Pinecone:  pc.create_index("items", dimension=768, metric="cosine")
# Chroma:    client.create_collection("items", metadata={"hnsw:space": "cosine"})
```
## 2. Vector Indexing & ANN Algorithms (Q21–Q40)

**Q21: Explain the HNSW (Hierarchical Navigable Small World) algorithm.**
A: HNSW builds a multi-layer graph. Bottom layer has all vectors; upper layers have progressively fewer. Search starts at the top layer (coarse) and descends, using greedy graph traversal at each level. Construction parameters: M (connections per node, default 16), ef_construction (search breadth during build). Query parameters: ef (search breadth). HNSW offers O(log n) search with high recall.

**Code:**
```python
import hnswlib
import numpy as np

x = np.random.randn(50_000, 64).astype("float32")
idx = hnswlib.Index(space="cosine", dim=64)
idx.init_index(max_elements=50_000, ef_construction=200, M=16)  # build params
idx.add_items(x)
idx.set_ef(50)                                        # query search breadth
q = np.random.randn(1, 64).astype("float32")
labels, dists = idx.knn_query(q, k=10)                # coarse top layer → fine bottom
print(labels)
```

**Q22: What are the Pros and Cons of HNSW compared to IVF?**
A: Pros: faster queries (log n vs sqrt(n)), higher recall, no training phase. Cons: higher memory usage (graph edges), slower indexing (O(n log n) insertion), larger disk footprint. HNSW is best for read-heavy workloads; IVF is better for write-heavy with limited memory.

**Code:**
```python
import faiss, numpy as np, time

x = np.random.randn(100_000, 64).astype("float32")
q = np.random.randn(100, 64).astype("float32")
for name, key in {"HNSW32": "HNSW32", "IVF256,Flat": "IVF256,Flat"}.items():
    idx = faiss.index_factory(64, key)
    if hasattr(idx, "train"): idx.train(x)
    t0 = time.perf_counter(); idx.add(x)
    idx.search(q, 10)
    ms = (time.perf_counter() - t0) / len(q) * 1e3
    print(f"{name}: {ms:.2f} ms/query")
# HNSW → faster queries, no training, more RAM · IVF → cheaper, needs centroids
```

**Q23: How does IVF (Inverted File Index) work?**
A: IVF partitions the vector space into nlist clusters using k-means during training. At query time, the closest nprobe clusters are searched exhaustively. IVF reduces search from all vectors to vectors in the nearest clusters. Tuning: larger nlist = more clusters, finer granularity; larger nprobe = higher recall, slower query.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(100_000, 64).astype("float32")
ivf = faiss.index_factory(64, "IVF256,Flat")   # nlist = 256 k-means clusters
ivf.train(x)                                   # phase 1: learn centroids
ivf.add(x)                                     # phase 2: assign each vector
ivf.nprobe = 8                                 # probe the 8 nearest clusters
q = np.random.randn(1, 64).astype("float32")
print(ivf.search(q, 5))                        # search shrinks to 8/256 of data
```

**Q24: What is Product Quantization (PQ) and when would you use it?**
A: PQ compresses vectors by splitting them into sub-vectors and quantizing each with a small codebook. A 768-dim vector might become 96 bytes instead of 3072 bytes (96% compression). Used for memory-constrained scenarios — reduced recall but enables billion-scale search on a single machine. Often combined with IVF as IVF-PQ.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(1_000_000, 768).astype("float32")
pq = faiss.index_factory(768, "PQ64")          # split 768-dim into 64 sub-vectors
pq.train(x); pq.add(x)
print("bytes/vector after PQ:", pq.sa_code_size, "vs", 768 * 4, "flat")   # ~64 vs 3072
```

**Q25: Compare IVF-Flat vs IVF-PQ vs IVF-SQ.**
A: 
- IVF-Flat: full-precision vectors in each cluster — highest recall, highest memory
- IVF-PQ: compressed vectors via product quantization — lower memory (4-8x), slightly lower recall
- IVF-SQ: scalar quantization (float32 → uint8) — 4x compression, moderate recall loss
- Trade-off: memory vs accuracy. IVF-Flat for high accuracy; IVF-PQ for scale.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(500_000, 128).astype("float32")
for name, key in {"IVF-Flat": "IVF128,Flat", "IVF-PQ": "IVF128,PQ32", "IVF-SQ": "IVF128,SQ8"}.items():
    idx = faiss.index_factory(128, key); idx.train(x); idx.add(x)
    print(f"{name:8s} bytes/vector: {idx.sa_code_size}")
# Flat = max recall & memory · SQ8 = 4x smaller · PQ32 = 8-16x smaller
```

**Q26: What is the ef parameter in HNSW and how does it affect performance?**
A: ef (exploration factor) controls how many candidates are examined during HNSW search. Higher ef = higher recall, higher latency. Default ef is often 10-50. Rule of thumb: start with ef = k * 10 (where k is number of results). Ef can be tuned per-query for dynamic accuracy-latency tradeoffs.

**Code:**
```python
import hnswlib, numpy as np

x = np.random.randn(50_000, 64).astype("float32")
q = np.random.randn(1, 64).astype("float32")
idx = hnswlib.Index(space="l2", dim=64)
idx.init_index(max_elements=50_000, M=16, ef_construction=200); idx.add_items(x)
for ef in [10, 50, 200]:
    idx.set_ef(ef)
    _, dist = idx.knn_query(q, k=10)
    print(f"ef={ef:4d}  nearest dist: {round(dist[0][0], 4)}")   # higher ef → nearer hit
```

**Q27: How does a DiskANN index differ from in-memory HNSW?**
A: DiskANN (Microsoft) stores vectors on SSD with a compressed HNSW-like graph in memory. It uses Vamana (a variant of HNSW) optimized for SSD reads — supports billion-scale datasets on a single machine ($400 cheaper than RAM). Latency is ~5-10ms vs <1ms for in-memory. Used by Qdrant (on-disk mode) and others.

**Code:**
```python
import diskannpy, numpy as np
# Vamana graph + compressed vectors in RAM; raw vectors on SSD
diskannpy.build_disk_index(
    data=np.random.randn(500_000, 96).astype("float32"),
    distance_metric="l2", index_path="/tmp/diskann",
    graph_degree=64, complexity=100, search_list_size=100,
)
q = np.random.randn(1, 96).astype("float32")
ids, dist = diskannpy.search_disk_index(q, k=10, index_path="/tmp/diskann",
                                        complexity=50, query_scratch=diskannpy.Scratch())
print(ids)   # billion-scale on one SSD box at ~5-10ms instead of <1ms RAM
```

**Q28: What is the "M" parameter in HNSW construction?**
A: M is the maximum number of connections per node per layer (default 16 in most implementations). Higher M = more connected graph, better recall, more memory (each edge is ~4-8 bytes). Lower M = less memory, faster indexing, potential recall drop. For most use cases, M=16-32 is recommended.

**Code:**
```python
import hnswlib, numpy as np

x = np.random.randn(30_000, 32).astype("float32")
for m in [8, 16, 32]:
    idx = hnswlib.Index(space="l2", dim=32)
    idx.init_index(max_elements=30_000, M=m, ef_construction=200)
    idx.add_items(x)
    mb = idx.get_memory_usage() / len(x) / 1e6
    print(f"M={m:2d}  {mb:.4f} MB/vector")      # higher M = denser graph, more RAM
```

**Q29: What happens to an ANN index when you insert new vectors?**
A: Behavior depends on index type:
- HNSW: incremental insertion is native — new vectors are added to graph dynamically without full rebuild
- IVF: insertions may distort cluster balance over time; periodic reclustering recommended
- PQ-based: adding vectors requires recomputing codebooks — bulk rebuild needed
- Most vector DBs buffer writes and periodically merge/flush to the main index

**Code:**
```python
import hnswlib, numpy as np

x = np.random.randn(10_000, 64).astype("float32")
idx = hnswlib.Index(space="l2", dim=64)
idx.init_index(max_elements=100_000, M=16, ef_construction=200)
idx.add_items(x)                                   # initial load
idx.add_items(np.random.randn(5_000, 64).astype("float32"))   # incremental, no rebuild
print("elements now:", idx.get_current_count())
# HNSW inserts natively; IVF drifts until reclustering; PQ needs codebook rebuild
```

**Q30: Explain the difference between flat (brute force) indexing and ANN indexing.**
A: Flat index stores vectors as-is without any structure; query = compute distance to every vector. ANN index organizes vectors (graph, clusters, quantized codes) for sub-linear search. Flat = 100% recall, O(n) time. ANN = 95-99% recall, O(log n) or O(sqrt(n)) time. Flat is only used for small datasets (~10K) or as a baseline.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(20_000, 64).astype("float32")
flat = faiss.IndexFlatL2(64); flat.add(x)              # brute force ~ O(n)
ann  = faiss.index_factory(64, "HNSW32"); ann.add(x)   # graph index ~ O(log n)
q = np.random.randn(1, 64).astype("float32")
print("flat:", flat.search(q, 10)[1])
print("ann :", ann.search(q, 10)[1])
```
**Q31: What is a "filtered ANN" search and how does Qdrant implement it?**
A: Filtered ANN combines vector similarity with scalar metadata filters. Qdrant uses a "payload index" alongside the vector index — during search, it intersects HNSW graph traversal with filter conditions. It can pre-filter (using filter as mask) or use a "oversampling" strategy (fetch more candidates, then apply filter). Qdrant's cardinality estimation chooses the optimal strategy automatically.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
# Qdrant intersects the HNSW traversal with payload conditions (native filtered ANN)
hits = client.query_points(
    collection_name="docs",
    query=[0.1, 0.2, 0.3],
    query_filter=models.Filter(must=[
        models.FieldCondition(key="year", range=models.Range(gte=2024)),
        models.FieldCondition(key="tags", match=models.MatchAny(any=["rag", "llm"]))]),
    limit=10,
)
print(len(hits))
```

**Q32: What is the ef_construction parameter in HNSW?**
A: ef_construction controls search width during HNSW graph building. Higher values = better quality graph (higher recall), slower build time. Typical range: 100-500. Must be balanced against M and dataset size.

**Code:**
```python
import hnswlib, numpy as np, time

x = np.random.randn(30_000, 64).astype("float32")
for ef_build in [50, 200, 500]:
    idx = hnswlib.Index(space="l2", dim=64)
    idx.init_index(max_elements=30_000, M=16, ef_construction=ef_build)
    t = time.perf_counter(); idx.add_items(x); dt = time.perf_counter() - t
    print(f"ef_construction={ef_build}  build={dt:.2f}s")
# higher ef_construction → denser/better graph, slower build
```

**Q33: How does Milvus handle indexing with its Knowhere library?**
A: Milvus uses Knowhere (a unified ANN framework) which wraps multiple index types: IVF, HNSW, PQ, DiskANN, etc. Knowhere provides a consistent API for index building, search, and serialization. Milvus automatically selects index type based on data size and configuration, and supports both CPU and GPU-accelerated indexing.

**Code:**
```python
from pymilvus import connections, Collection

connections.connect("default", host="localhost", port="19530")
col = Collection("articles")
col.create_index(
    field_name="vector",
    index_params={"index_type": "HNSW", "metric_type": "COSINE",
                  "params": {"M": 16, "efConstruction": 200}},
)
# Knowhere = unified ANN wrapper: same API for IVF, HNSW, PQ, DiskANN, GPU
```

**Q34: What is the role of quantization in reducing vector storage?**
A: Quantization reduces precision of vector components (float32→uint8 or binary) or applies product quantization to split-and-encode. This reduces memory footprint by 4-32x, enabling larger datasets in RAM, but introduces accuracy loss. Scalar quantization is common — maps float range to int range with minimal recall drop (<1%).

**Code:**
```python
import numpy as np

v = np.random.randn(100_000, 768).astype("float32")     # 307 MB float32
mins, maxs = v.min(axis=0), v.max(axis=0)
q8 = np.round((v - mins) / (maxs - mins) * 255).astype("uint8")   # scalar quantization
print("float32 MB:", round(v.nbytes / 1e6), "| uint8 MB:", round(q8.nbytes / 1e6), "| 4x smaller")
```

**Q35: How does Weaviate handle multi-vector indexing (named vectors)?**
A: Weaviate supports multiple named vectors per object — each with its own embedding model, index type, and distance metric. For example, an article can have a "title_vector" (768-dim cosine) and an "image_vector" (512-dim euclidean). Search queries target specific named vectors, enabling multi-modal hybrid search.

**Code:**
```python
# Weaviate named vectors: multiple embeddings + metrics per object
import weaviate

client = weaviate.connect_to_local()
col = client.collections.get("Article")
for obj in col.query.fetch_objects(limit=1):
    print(obj.vector)        # {"title_vector": [...], "image_vector": [...]}
col.query.near_text(query="AI funding", target_vector="title_vector", limit=5)
```

**Q36: What is the "golden vector" or "centroid" in IVF?**
A: In IVF, centroids are the cluster centers learned during k-means training. Each vector is assigned to the nearest centroid. During search, the closest centroids to the query are found, and only their assigned vectors are searched. The number of centroids (nlist) determines granularity.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(50_000, 64).astype("float32")
index = faiss.index_factory(64, "IVF64,Flat")
index.train(x)                                  # k-means learns 64 centroids
centroids = index.quantizer.reconstruct_n(0, index.nlist)   # the "golden vectors"
print(centroids.shape)                          # (64, 64)
q = np.random.randn(1, 64).astype("float32")
_, centers = index.quantizer.search(q, 3)       # nearest centroids to the query
print(centers)
```

**Q37: Can you use multiple ANN algorithms in the same vector database?**
A: Yes — most vector DBs support multiple index types per collection. Milvus allows switching index types (IVF_FLAT, HNSW, DISKANN) on the same collection. Qdrant supports HNSW only (with on-disk mode). Pinecone uses a proprietary algorithm. Weaviate supports HNSW with optional flat mode. The choice depends on workload.

**Code:**
```python
from pymilvus import Collection

col = Collection("articles")
for itype in ["HNSW", "IVF_FLAT", "DISKANN"]:
    params = {"M": 16} if itype == "HNSW" else ({"nlist": 128} if itype == "IVF_FLAT" else {})
    col.create_index("vector", {"index_type": itype, "metric_type": "COSINE", "params": params})
# One collection, swap the ANN algorithm to match read/write workload
```

**Q38: How does Chroma DB handle indexing by default?**
A: Chroma uses HNSW (via hnswlib) for ANN search by default. It additionally supports brute-force for small datasets and configurable index parameters (ef, M). Chroma automatically switches to brute-force below a configurable threshold (default 10K vectors).

**Code:**
```python
import chromadb

client = chromadb.PersistentClient(path="/tmp/chroma")
coll = client.create_collection(
    "docs",
    metadata={"hnsw:space": "cosine", "hnsw:M": 16, "hnsw:ef_construction": 200},
)  # hnswlib HNSW by default; brute force below the size threshold
coll.upsert(ids=["1"], embeddings=[[0.1, 0.2, 0.3]])
print(coll.query(query_embeddings=[[0.1, 0.2, 0.3]], n_results=1)["ids"])
```

**Q39: What is a "multi-vector" or "multi-representation" index?**
A: Instead of one vector per document, multiple vectors per document (e.g., one per paragraph or sentence). This improves retrieval granularity but increases storage. Late interaction models (ColBERT) use multi-vector representations. Some vector DBs support this natively.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
token_vecs = model.encode(tokens)          # ColBERT-style: several vectors per doc
client.upsert("docs", points=[
    models.PointStruct(id="d1", vector=v, payload={"doc": "d1", "token_i": i})
    for i, v in enumerate(token_vecs)])
# retrieval compares the query against every stored vector (MaxSim), not one vector/doc
```

**Q40: How do you benchmark ANN index performance?**
A: Key metrics: recall@k (accuracy), queries-per-second (QPS, throughput), latency p50/p99, index build time, memory usage. Standard benchmarks: ANN-Benchmarks (http://ann-benchmarks.com) tests HNSW, IVF, DiskANN, etc. on datasets like SIFT (128-dim), GIST (960-dim), GloVe (300-dim), MNIST.

**Code:**
```python
import faiss, numpy as np, time

x = np.random.randn(100_000, 64).astype("float32")
q = np.random.randn(1000, 64).astype("float32")
flat = faiss.IndexFlatL2(64); flat.add(x)
hnsw = faiss.index_factory(64, "HNSW32"); hnsw.add(x)
_, exact = flat.search(q, 10)
t = time.perf_counter(); _, approx = hnsw.search(q, 10); latency = time.perf_counter() - t
recall = np.mean([len(set(e) & set(a)) / 10 for e, a in zip(exact, approx)])
print(f"recall@10={recall:.2f}  qps={len(q)/latency:.0f}  p50={(latency/len(q))*1e3:.2f}ms")
```
## 3. Operations, CRUD & Data Management (Q41–Q60)

**Q41: How does a vector database handle duplicate vectors?**
A: Most vector DBs don't deduplicate by vector content — they use unique IDs as primary keys. Inserting the same vector with a new ID creates a new entry (duplicate). Some DBs allow upsert based on ID. To deduplicate by content, you'd need to query for near-duplicates before insert.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
embed = [0.1, 0.2, 0.3]
client.upsert("docs", points=[models.PointStruct(id=1, vector=embed)])
client.upsert("docs", points=[models.PointStruct(id=1, vector=embed)])   # same ID → upsert, not dup
client.upsert("docs", points=[models.PointStruct(id=2, vector=embed)])   # new ID → duplicate entry
print(client.count("docs", exact=True).count)   # 2 points, identical vector content
```

**Q42: What happens when you exceed the dimension limit of a collection?**
A: The dimension is set at collection creation and cannot be changed. Inserting vectors with mismatched dimensions throws an error. To use a different dimension, you must create a new collection and re-index. Some DBs (Weaviate) allow multi-vector classes with different dimensions.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.create_collection("c", vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE))
try:
    client.upsert("c", points=[models.PointStruct(id=1, vector=[0.1] * 512)])  # wrong dim
except Exception as exc:
    print("rejected:", type(exc).__name__)   # create a new collection to change dimension
```

**Q43: Explain vectors namespacing and multi-tenancy support in vector DBs.**
A: Most vector DBs support multi-tenancy via:
- Partitioning (Pinecone: namespaces; Qdrant: collections per tenant)
- Metadata filtering (Weaviate: class-level filtering; Milvus: partition key)
- Separate indexes per tenant (performance isolation but higher resource usage)
- Tenant isolation at API level

**Code:**
```python
import pinecone

pc = pinecone.Pinecone()
pc.create_index("prod", dimension=768, metric="cosine")
index = pc.Index("prod")
index.upsert(vectors=[("1", [0.1, 0.2])], namespace="tenant-a")   # isolated per tenant
index.upsert(vectors=[("1", [0.9, 0.8])], namespace="tenant-b")   # same ID, other tenant
print([r.id for r in index.query(vector=[0.1, 0.2], namespace="tenant-a").matches])
```

**Q44: How do vector databases handle data persistence and durability?**
A: Vectors are persisted to disk (usually as mmap files or SSTables). Write-ahead log (WAL) for crash recovery. Periodic flushing to main index. Snapshots for backup. Replication for high availability. In-memory indexes are rebuilt from disk on restart. Milvus uses etcd + object storage; Qdrant uses fsync for durability.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(5_000, 64).astype("float32")
index = faiss.IndexFlatL2(64); index.add(x)
faiss.write_index(index, "/tmp/index.faiss")       # snapshot to durable disk
loaded = faiss.read_index("/tmp/index.faiss")       # rebuilt on restart
# production: WAL for crash recovery + replication for HA + periodic snapshots
```

**Q45: What is the difference between batch ingestion and streaming ingestion?**
A: Batch ingestion: pre-compute all embeddings, bulk-insert into DB. Fast ingestion but higher memory spike. Streaming ingestion: insert vectors one-by-one as data arrives. Lower throughput but real-time availability. Some DBs (Qdrant, Weaviate) batch internally; others (Milvus) have explicit flush commands.

**Code:**
```python
import faiss, numpy as np, time

index = faiss.IndexFlatL2(128)
vectors = np.random.randn(1_000_000, 128).astype("float32")

t0 = time.perf_counter(); index.add(vectors); batch = time.perf_counter() - t0  # bulk insert
index = faiss.IndexFlatL2(128)
t0 = time.perf_counter()
for v in vectors: index.add(v.reshape(1, -1))      # one-by-one streaming
stream = time.perf_counter() - t0
print(f"batch={batch:.2f}s  streaming={stream:.2f}s")
```

**Q46: How does a vector database handle index rebuilding?**
A: Triggered by: config change (index type), data distribution drift, scheduled maintenance. During rebuild, reads still serve from old index; writes go to new index. After rebuild, atomic swap. Some DBs (Milvus) support online index building; others require downtime or duplicate collection.

**Code:**
```python
import faiss, numpy as np

x = np.random.randn(50_000, 64).astype("float32")
old = faiss.index_factory(64, "IVF128,Flat")      # reads keep serving from `old`
old.train(x); old.add(x)
new = faiss.index_factory(64, "HNSW32")           # build replacement in the background
new.add(x)
index = new                                       # atomic swap when the rebuild is ready
```

**Q47: What is a "point" in vector database terminology?**
A: A point (Qdrant) or object (Weaviate) is a single record containing: a unique ID, the vector, and optional payload/metadata. In Pinecone: "vector" with ID and metadata. In Milvus: "entity" with fields + vector.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
point = models.PointStruct(
    id="3fa85f64-bfe0-4f2c-9ef4-9dbbc4dec36f",   # unique ID
    vector=[0.1, 0.2, 0.3],                       # the embedding
    payload={"title": "A point", "price": 9.99},  # optional payload / metadata
)
print(client.upsert("docs", points=[point]))
# = "object" (Weaviate) · "vector+metadata" (Pinecone) · "entity" (Milvus)
```

**Q48: How do you update the metadata of a vector without changing its embedding?**
A: Most vector DBs support updating payload/metadata independently of the vector. Qdrant: `set_payload` operation. Weaviate: update object properties. Pinecone: `update` with only metadata field. This does not affect the index structure.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("docs", points=[models.PointStruct(id=1, vector=[0.1, 0.2, 0.3], payload={"verified": False})])
client.set_payload("docs", payload={"verified": True}, points=[1])   # metadata-only update
res = client.retrieve("docs", ids=[1])
print(res[0].payload)        # embedding untouched → index structure unchanged
```

**Q49: What is a "full scan" and when does a vector DB resort to one?**
A: A full scan iterates every vector, computing distance for each — equivalent to brute-force KNN. Occurs when: no index is built, index is invalidated, or filter is too restrictive for ANN pruning. Full scans are expensive (O(n)) and should be avoided in production.

**Code:**
```python
import faiss, numpy as np, time

x = np.random.randn(500_000, 64).astype("float32")
flat = faiss.IndexFlatL2(64); flat.add(x)          # no structure → full scan O(n)
q = np.random.randn(1, 64).astype("float32")
t = time.perf_counter(); flat.search(q, 10)
print("full scan:", round((time.perf_counter() - t) * 1e3, 1), "ms")
# happens when no index exists / is invalidated / a pre-filter kills ANN pruning
```

**Q50: How do vector databases support time-based or dynamic data (time-decay)?**
A: Approaches:
- Metadata filtering: add timestamp field, filter by time range at query time
- Time-decayed scoring: recompute similarity = (1 - decay_factor) * vector_sim + decay_factor * recency
- Data retention policies: TTL-based or scheduled deletion of old vectors
- Separate indexes per time window for scrolling windows

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("events", points=[models.PointStruct(id=i, vector=v, payload={"ts": ts})
                                for i, (v, ts) in enumerate([([0.1, 0.2], 1_700_000_000),
                                                             ([0.9, 0.1], 1_700_100_000)])])
hits = client.query_points(
    "events", query=[0.1, 0.2],
    query_filter=models.Filter(must=[models.FieldCondition(key="ts", range=models.Range(gte=1_700_050_000))]),
    limit=10)
# or time-decayed scoring: score = 0.7 * vsim + 0.3 * recency
print(len(hits))
```
**Q51: What is the MVCC model in vector databases?**
A: Multi-Version Concurrency Control ensures consistent reads during writes. Qdrant uses MVCC for segment-based architecture — writes go to new segments while reads use a snapshot of segments at query start. This prevents read-write conflicts without locks.

**Code:**
```python
# MVCC: writers append new segments; readers see a stable snapshot
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("docs", points=[models.PointStruct(id=1, vector=[0.1], payload={"v": 1})])
snap = client.retrieve("docs", ids=[1])           # read = snapshot of segments
client.set_payload("docs", payload={"v": 2}, points=[1])   # concurrent write → new segment
print(snap[0].payload, "->", client.retrieve("docs", ids=[1])[0].payload)   # no locks, torn reads
```

**Q52: How does compaction work in Qdrant?**
A: Qdrant stores vectors in segments. Over time, segments accumulate (from updates, deletes, upserts). Compaction merges smaller segments into larger ones, reclaims storage from deleted vectors, and rebuilds HNSW graphs for merged data. Can run in background or be triggered manually.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.update_collection(
    "docs",
    optimizer_config=models.OptimizersConfigDiff(
        memmap_threshold=20000,      # small segments → merged past the threshold
        max_segment_size=100000,     # reclaim tombstones, rebuild HNSW graph
    ),
)
# compaction trades background CPU/disk for stable query latency
```

**Q53: What are the tradeoffs of storing vectors on SSD vs in RAM?**
A: RAM: sub-millisecond latency, high throughput, expensive, limited capacity. SSD (on-disk): 5-20ms latency, lower throughput, cheaper, near-infinite capacity. Hybrid: hot vectors in RAM cache, cold on SSD. Milvus DiskANN, Qdrant on-disk, and Weaviate with disk-based vectors support SSD.

**Code:**
```python
import numpy as np, time

x = np.random.randn(200_000, 64).astype("float32")
np.save("/tmp/vectors.npy", x)
mmap = np.load("/tmp/vectors.npy", mmap_mode="r")          # "SSD": OS pages from disk
ram = np.load("/tmp/vectors.npy")                          # "RAM": resident array
def q(v): return np.linalg.norm(mmap - v, axis=1).argmin()
t = time.perf_counter(); q(mmap[0]); print("mmap/SSD ms:", round((time.perf_counter() - t) * 1e3, 2))
# RAM: <1ms but expensive · SSD: 5-20ms, cheap & near-infinite (DiskANN / on-disk mode)
```

**Q54: How do you export or migrate vectors from one vector DB to another?**
A: Common approaches:
- Bulk export via API (iterate over all vectors, stream to file)
- Snapshot/restore (vendor-specific format)
- CSV/JSONL export with metadata
- Migration tools (e.g., VectorDBBench, custom scripts)
- Challenge: different DBs have different ID formats, metadata schemas, and vector representations

**Code:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
records, offset = [], None
while True:                                    # stream every point out
    page, offset = client.scroll("docs", limit=1000, offset=offset, with_vectors=True)
    records.extend(page)
    if offset is None:
        break
with open("/tmp/export.jsonl", "w") as f:      # vendor-neutral export → import into target
    f.writelines(r.model_dump_json() + "\n" for r in records)
```

**Q55: What is a "segment" in Qdrant / "shard" in Milvus?**
A: Segment (Qdrant): self-contained unit with its own HNSW graph, vectors, payload index, and WAL. Multiple segments serve queries in parallel, merged at query time. Shard (Milvus): horizontal partition of data. Segments enable efficient updates/deletes; shards enable horizontal scaling.

**Code:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
# segment (Qdrant) = self-contained HNSW+WAL unit, merged at query time
# shard (Milvus) = horizontal partition enabling scale-out across nodes
print(client.get_collection("docs").segments_count, "segments being served")
```

**Q56: How does a vector DB handle storing vectors larger than available memory?**
A: Options:
- On-disk index (DiskANN/Qdrant on-disk): vectors on SSD, lightweight graph in memory
- Memory-mapped files (mmap): OS handles paging; vectors swapped in/out as needed
- Tiered storage: hot (RAM) + warm (SSD) + cold (object storage)
- Partitioning: split data across machines

**Code:**
```python
import numpy as np

# 50M x 384 float32 ≈ 76 GB — bigger than RAM
shape = (50_000_000, 384)
big = np.lib.format.open_memmap("/tmp/big.dat", mode="w+", dtype="float32", shape=shape)
big[0] = np.random.randn(384)                  # OS pages only the hot parts into RAM
print("on-disk, mmap-managed:", big[0].shape)
# DiskANN / mmap / tiered storage keep the full index addressable without 76 GB RAM
```

**Q57: What is the purpose of a "write-ahead log" (WAL) in vector databases?**
A: WAL logs all mutations (insert, update, delete) before applying to the index. On crash recovery, the WAL is replayed to restore consistency. Qdrant uses WAL per segment; Milvus uses binlog. Without WAL, a crash could corrupt the index or lose recent writes.

**Code:**
```python
import json

wal = open("/tmp/wal.jsonl", "a")
def mutate(op, id_, vec):
    wal.write(json.dumps({"op": op, "id": id_, "v": list(vec)}) + "\n")   # journal first
    wal.flush()                                          # durable before touching the index
    apply_to_index(id_, vec)                             # crash mid-way → replay WAL
# Qdrant: WAL per segment · Milvus: binlog · without it a crash corrupts the index
```

**Q58: How do you handle vector deletion without rebuilding the entire index?**
A: 
- Tombstone marking: mark ID as deleted, filter out during search. Index structure remains unchanged.
- Soft delete: remove from search results but keep in index.
- Periodic compaction: physically remove deleted vectors and rebuild affected segments.
- HNSW: deleting nodes from a graph is complex; most DBs use tombstone + periodic rebuild.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("docs", points=[models.PointStruct(id=42, vector=[0.1, 0.2])])
client.delete("docs", points_selector=models.PointIdsList(points=[42]))   # tombstone mark
print(client.query_points("docs", query=[0.1, 0.2], limit=5))             # filtered out of search
# physical removal happens later via segment compaction — no full index rebuild
```

**Q59: What is a "payload index" and how is it different from a vector index?**
A: Payload index (Qdrant/Weaviate) indexes metadata fields (keywords, numbers, geo) for fast filtering. It's a traditional inverted index or B-tree, NOT for vectors. The vector index handles similarity; the payload index handles filtering. Both are combined during query execution.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.create_payload_index("docs",
                            field_name="category",
                            field_schema=models.PayloadSchemaType.KEYWORD)   # inverted index
client.query_points(
    "docs", query=[0.1, 0.2],
    query_filter=models.Filter(must=[models.FieldCondition(key="category",
                                                           match=models.MatchValue("sci"))]))
# vector index → similarity · payload index → filtering, joined per query
```

**Q60: Can you store non-vector data (blobs, full text) in a vector DB?**
A: Yes — most vector DBs store original data as part of the record. Weaviate stores objects (with vector + properties). Qdrant stores payload (arbitrary JSON). Pinecone supports metadata as key-value pairs. However, vector DBs are not optimized for blob storage — use object storage for large files and store references in the DB.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("docs", points=[models.PointStruct(
    id="1", vector=embedding,
    payload={"text": "full document text",          # small blobs live in payload
             "pdf_ref": "s3://bucket/doc.pdf"})])   # large files → object-storage refs
```
## 4. Similarity Search & Query Patterns (Q61–Q75)

**Q61: What is "hybrid search" and how is it implemented in vector DBs?**
A: Hybrid search combines vector similarity (ANN) with keyword/text search (BM25). Results are merged via reciprocal rank fusion (RRF) or weighted scoring. Weaviate implements with its `bm25` + `nearText` filters. Qdrant supports via `should` queries. This gives best of both: semantic understanding + exact keyword matching.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.query_points(
    "docs",
    prefetch=[
        models.Prefetch(query=dense_vec, using="dense", limit=20),
        models.Prefetch(query="exact keywords", using="sparse", limit=20),   # BM25 side
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),   # reciprocal rank fusion
    limit=10,
)
# semantic relevance + exact lexical term hits in one result set
```

**Q62: Explain "maximum marginal relevance" (MMR) and its use in vector search.**
A: MMR balances relevance and diversity in results. After finding top-k similar vectors, MMR reranks to select a subset that is both relevant to the query AND dissimilar from each other. Prevents redundant results. Formula: MMR = λ * sim(query, doc_i) - (1-λ) * max(sim(doc_i, doc_j)). Used in RAG for diverse context.

**Code:**
```python
import numpy as np

def mmr(query, docs, k=5, lam=0.7):
    picked = [int(np.argmax(query @ docs))]          # most relevant first
    rest = [i for i in range(len(docs)) if i not in picked]
    for _ in range(1, min(k, len(docs))):
        score = lambda i: (lam * float(query @ docs[i]) -
                           (1 - lam) * max(float(np.dot(docs[i], docs[j])) for j in picked))
        nxt = max(rest, key=score)                    # relevant AND dissimilar to chosen
        picked.append(nxt); rest.remove(nxt)
    return picked

q = np.array([1.0, 0.0])
docs = [np.array([1.0, 1.0]), np.array([0.0, 1.0]), np.array([-1.0, 0.0])]
print(mmr(q, docs, k=2))
```

**Q63: What is "late interaction" and how does ColBERT use it?**
A: Late interaction (ColBERT) encodes query and document into separate multi-vector representations and computes similarity via MaxSim (sum of max cosine between each query token and all document tokens). More accurate than single-vector embeddings but slower to compute. Plaid index enables efficient approximate late interaction search.

**Code:**
```python
import numpy as np

q_tokens = np.random.randn(4, 128)     # 4 query token vectors
d_tokens = np.random.randn(8, 128)     # 8 document token vectors
sims = np.stack([q @ d_tokens.T for q in q_tokens])    # (4, 8) cosine-ish matrix
maxsim = float(sims.max(axis=1).sum())                 # ColBERT MaxSim score
print(maxsim)
```

**Q64: What is the role of "query rewriting" before vector search?**
A: Query rewriting transforms raw user queries into forms better suited for vector similarity. Examples: expanding acronyms, correcting typos, decomposing complex queries, adding synonyms. Improves retrieval quality. Often done by an LLM before embedding. e.g., "What's the price?" → "What is the cost/pricing/subscription fee?"

**Code:**
```python
def rewrite_with_llm(raw: str) -> str:
    # LLM expands shorthand → better embeddings (offline step before embedding)
    return {"what's price?": "what is the cost, pricing, or subscription fee?"}.get(raw.lower(), raw)

for raw in ["what's price?", "how do I start langchain?"]:
    q = rewrite_with_llm(raw)
    print(raw, "→", q)       # embed the *rewritten* query, not the raw one
```

**Q65: How do you implement multi-stage retrieval with a vector database?**
A: 
Stage 1 (ANN): fast approximate search, return top-100 candidates
Stage 2 (Rerank): apply a more expensive cross-encoder or LLM-based scorer to top-100
Stage 3 (Filter): apply business logic, deduplication, diversity constraints
This architecture combines speed of ANN with accuracy of expensive rerankers.

**Code:**
```python
from sentence_transformers import CrossEncoder
import numpy as np

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
cands = [3, 7, 12, 19]                          # stage 1: ANN top-100 → narrowed here
pairs = [(query_text, docs[i]) for i in cands]  # stage 2: rerank only the candidates
scores = reranker.predict(pairs)
top = [cands[i] for i in np.argsort(scores)[-2:][::-1]]   # stage 3: business filters
print(top)
```

**Q66: What is the difference between "fetch" and "search" in vector DB operations?**
A: Fetch: retrieve a specific vector by its unique ID (O(1) by hash lookup, no similarity computation). Search: find vectors similar to a query vector (ANN search, O(log n)). They serve different purposes — fetch for direct lookup, search for discovery.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("docs", points=[models.PointStruct(id=1, vector=[0.1, 0.2])])
print(client.retrieve("docs", ids=[1])[0].id)           # FETCH: O(1) ID lookup
hits = client.query_points("docs", query=[0.1, 0.2], limit=5)   # SEARCH: ANN traversal
print([h.id for h in hits])
```

**Q67: How does score normalization work in vector search?**
A: Raw distance scores (cosine, euclidean, dot) aren't inherently interpretable. Normalization techniques:
- Min-max normalization (map scores to [0,1])
- Z-score (based on score distribution)
- Sigmoid calibration (fit to probability-like scores)
- Weaviate uses "certainty" (normalized to [0,1]); Qdrant uses raw distance

**Code:**
```python
import numpy as np

dist = np.array([0.1, 0.5, 0.9])
minmax = (dist - dist.min()) / (dist.max() - dist.min())   # → [0,1]
certainty = 1 - dist / 2                                    # Weaviate-style
print("minmax:", minmax.round(2), "certainty:", certainty.round(2))
# Qdrant returns raw distances; normalise at the app layer for thresholds
```

**Q68: What is "group by" or "aggregation" in a vector search context?**
A: Search results grouped by a metadata field. For example: find top-10 products similar to query, but return at most 1 per category. Qdrant supports `group_by` natively. Milvus supports grouping via post-processing. Avoids result domination by a single category.

**Code:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
res = client.query_points_grouped(
    collection_name="products",
    query=query_vec,
    group_by="category",      # max 1 hit per category → no single category dominates
    limit=5,
    group_size=1,
)
print([g.key for g in res.groups])
```

**Q69: Explain the concept of "pagination" in vector queries.**
A: ANN search returns top-k results sorted by distance. Pagination (offset) is tricky — retrieving "results 101-120" requires re-running search with a larger k (e.g., 120), which is expensive. Alternatives: scroll API (cursor-based), and avoid deep pagination in vector search.

**Code:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
records, offset = client.scroll("docs", limit=100, offset=None)      # page 1 (cursor)
print("page 1:", len(records))
records, offset = client.scroll("docs", limit=100, offset=offset)   # page 2 — no re-search
print("page 2:", len(records))
```

**Q70: What is a "vector search playground" and how does it help?**
A: Tools like Weaviate Console, Qdrant UI, and Pinecone console let you test similarity queries visually — inspect nearest neighbors, tune parameters (ef, M), compare metrics. Essential for understanding embedding quality and index behavior before production.

**Code:**
```python
import chromadb

client = chromadb.Client()
coll = client.create_collection("demo")
coll.upsert(ids=["t1", "t2", "t3"],
            embeddings=[[1, 0], [0, 1], [1, 1]],
            metadatas=[{"label": "a"}, {"label": "b"}, {"label": "a"}])
print(coll.query(query_embeddings=[[1, 0]], n_results=2))   # inspect nearest neighbours
```
**Q71: How does the vector database handle searching for "nothing" (query of all zeros)?**
A: A zero vector is equidistant from all vectors in cosine space, and at origin in euclidean. Search with zero query vector returns arbitrary results (based on index structure, not semantics). Most validation layers reject zero vectors.

**Code:**
```python
import numpy as np

zero = np.zeros(384)
print("norm:", np.linalg.norm(zero))          # no direction → equidistant to everything
if not np.any(zero):
    raise ValueError("reject zero vectors at validation")   # search would be meaningless
```

**Q72: Can you do multi-vector search (search by multiple query vectors at once)?**
A: Yes — supported by some DBs:
- Qdrant: multiple query vectors per request with `recommend` API
- Milvus: hybrid search across multiple vector fields
- Weaviate: named vectors allow different queries on different vector types
- Use cases: cross-modal search (image + text), multi-faceted recommendations

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
client.upsert("items", points=[models.PointStruct(id=i, vector=v)
                               for i, v in enumerate(embed_matrix)])
res = client.recommend(                         # multiple query vectors at once
    collection_name="items",
    positive=[0, 1], negative=[2],              # "like these, unlike that"
    limit=5,
)
print([h.id for h in res])
```

**Q73: What is "contextual retrieval" and how does it relate to vector search?**
A: Contextual retrieval augments a chunk with surrounding context before embedding — e.g., prepending "This chunk is from a document about [topic], specifically section [title]" to the chunk text. Improves retrieval quality because the embedding captures context, not just the isolated chunk.

**Code:**
```python
def contextualize(chunk: str, doc_title: str, section: str) -> str:
    # embedding now captures surrounding context, not the isolated chunk
    return f"This chunk is from {doc_title!r}, section {section!r}. Content: {chunk}"

chunks = [contextualize(c, "Vector DB Guide", "Indexing") for c in raw_chunks]
```

**Q74: How does a vector DB handle queries for the "most dissimilar" vectors?**
A: Search with the opposite direction (cosine: farthest = dot negative; euclidean: farthest = maximized distance). Most DBs don't support "farthest neighbor" natively. You can achieve it by searching with the negated query vector (for dot product) or by inverting distances in post-processing. Limited practical use.

**Code:**
```python
import numpy as np

q = np.array([0.5, 0.5])      # for dot-product search
neg = -q                      # farthest neighbour ≈ nearest to the negated query
print("farthest finds:", neg)
```

**Q75: What is the typical query latency budget for vector search in a user-facing RAG app?**
A: For interactive RAG: budget 200-500ms total for retrieval (embedding + vector search + reranking). Vector search should take <100ms. For batch/analytics: seconds to minutes. Acceptable latency depends on user expectations — lower for chatbots, higher for research tools.

**Code:**
```python
import time

t0 = time.perf_counter()
vec = embed(query_text)                          #   30-80 ms
hits = vector_store.search(vec, k=5)             # <100 ms budget
reranked = sorted(hits, key=lambda h: h.score, reverse=True)[:3]
print("total retrieval ms:", round((time.perf_counter() - t0) * 1e3))
# interactive RAG budget ≈ 200-500 ms end-to-end
```
## 5. Performance, Scaling & Production (Q76–Q90)

**Q76: How do you scale a vector database horizontally?**
A: 
- Sharding: partition data across nodes by ID hash or metadata key
- Replication: copy data to multiple nodes for HA and read throughput
- Distributed ANN: each node searches its local index; results merged at coordinator
- Milvus: worker nodes + message queue + object storage (cloud-native)
- Qdrant: cluster mode with Raft consensus
- Weaviate: replication factor + auto-sharding with consistent hashing

**Code:**
```python
import concurrent.futures as cf
import numpy as np, faiss

shards = [faiss.IndexFlatL2(64) for _ in range(4)]      # 4 nodes/partitions
for s in shards:
    s.add(np.random.randn(10_000, 64).astype("float32"))
q = np.random.randn(1, 64).astype("float32")
with cf.ThreadPoolExecutor() as ex:                     # scatter query to every node
    results = [f.result() for f in [ex.submit(s.search, q, 20) for s in shards]]  # oversample 2x
ids = np.concatenate([r[1] for r in results])[:10]      # gather → global top-k at coordinator
print(ids)
```

**Q77: What is a "distributed ANN" and how does it maintain recall?**
A: Each node maintains its own ANN index over a subset of data. Query is sent to all nodes (scatter), each does local ANN search, results are aggregated (gather), and merged by distance. Recall can degrade because true nearest neighbors might be spread across nodes. Oversampling (each node returns 2x its share) mitigates recall loss.

**Code:**
```python
import concurrent.futures as cf
import faiss, numpy as np

shards = [faiss.IndexFlatL2(64) for _ in range(4)]      # node subset
for sh in shards:
    sh.add(np.random.randn(10_000, 64).astype("float32"))
q = np.random.randn(1, 64).astype("float32")
with cf.ThreadPoolExecutor() as ex:                     # scatter
    best = [f.result() for f in [ex.submit(sh.search, q, 20) for sh in shards]]  # 2x share
ids, dists = zip(*best)                                  # gather
ids, dists = np.concatenate(ids)[0], np.concatenate(dists)[0]
order = dists.argsort()[:10]                             # merge by distance across nodes
print(ids[order])
```

**Q78: How does caching improve vector search performance?**
A: 
- Query result cache: cache frequent queries with TTL
- Embedding cache: avoid re-embedding common queries
- HNSW node cache: hot nodes in RAM
- Filter result cache: pre-compute filtered subsets for frequent filters
- OS page cache: mmap-based DBs benefit naturally

**Code:**
```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def cached_query(q: str):        # query-result cache → hot queries skip ANN entirely
    return vector_store.search(embed_model.encode([q])[0], k=10)

hits = cached_query("what is a vector db?")
```

**Q79: What's the difference between "throughput" and "latency" in vector DB benchmarking?**
A: Throughput = queries per second (QPS) under concurrent load. Latency = time per query (p50, p95, p99). They trade off — batching increases throughput but adds latency. Typical target: <100ms p95 latency for interactive apps. Use concurrency testing to measure throughput-latency curve.

**Code:**
```python
import time, concurrent.futures as cf

def bench(index, queries, concurrency=16):
    t0 = time.perf_counter()
    with cf.ThreadPoolExecutor(concurrency) as ex:
        list(ex.map(lambda q: index.search(q, 10), queries * 5))
    wall = time.perf_counter() - t0
    print(f"throughput = {len(queries) * 5 / wall:.0f} QPS")   # latency = p50/p95/p99 of calls
# batching lifts QPS but pushes tail latency up — plot the throughput-latency curve
```

**Q80: How do you handle vector DB backups and disaster recovery?**
A: 
- Snapshots: point-in-time copy of index + data (Qdrant: snapshot API; Milvus: backup tool)
- Replication: multi-node cluster survives node failure
- Object storage: persist WAL + index snapshots to S3/GCS
- Cross-region replication for geo-redundancy
- Recovery: restore snapshot + replay WAL

**Code:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
snap = client.create_snapshot("docs")               # point-in-time copy: index + payloads
print(snap.snapshot.time)
# restore: upload snapshot + recover; add cross-region replication for geo-redundancy
```

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

**Code:**
```python
import numpy as np, faiss, time

pops = []
for _ in range(50):
    t0 = time.perf_counter(); index.search(qvec, 10); pops.append((time.perf_counter() - t0) * 1e3)
print("p50 %.1fms  p99 %.1fms" % (np.percentile(pops, 50), np.percentile(pops, 99)))
print("index RAM:", round(faiss.get_mem_usage_current() / 1e6), "MB")
# also watch: QPS, build progress, disk I/O, error rate, replication lag, recall@k drift
```

**Q82: How do vector databases handle hot spots (popular vectors queried frequently)?**
A: 
- Caching: frequently accessed vectors cached in memory
- Load balancing: distribute queries across replicas
- Consistent hashing: prevent imbalanced shard access
- Rate limiting: per-tenant or per-user limits
- Separate hot storage tiered from cold

**Code:**
```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def hot(query):                       # popular query vectors served from RAM
    return index.search(query, 10)
# + consistent-hash sharding, replica load-balancing, per-tenant rate limits
```

**Q83: What is "rate limiting" in managed vector DB APIs (Pinecone, Qdrant Cloud)?**
A: Rate limits cap QPS or throughput (MB/s) per index/project to prevent noisy neighbor issues. Pinecone: limits based on pod type (s1: 100 QPS, p1: 500 QPS). Qdrant Cloud: based on cluster size. Exceeding returns 429 errors. Mitigation: client-side retry with exponential backoff.

**Code:**
```python
import time

def call(query, max_retries=5):
    for attempt in range(max_retries):
        resp = client.query(query)
        if resp.status_code != 429:
            return resp
        time.sleep(min(2 ** attempt, 30))    # exponential backoff on 429
    raise RuntimeError("rate limited")
```

**Q84: How do you choose between a managed vector DB and self-hosted?**
A: Managed (Pinecone, Qdrant Cloud, Weaviate Cloud): zero ops, auto-scaling, SLAs, but vendor lock-in and higher cost at scale. Self-hosted (Milvus, Qdrant, Weaviate): full control, lower cost at scale, but Ops overhead. Decision factors: team size, scale, compliance, in-house DevOps expertise.

**Code:**
```python
def pick(team_size: int, scale: int, compliance: bool):
    if compliance or team_size <= 3:          # little ops time → managed (Pinecone / Qdrant Cloud)
        return "managed"
    if scale > 100_000_000:                   # big + control → self-hosted (Milvus / Qdrant)
        return "self_hosted"
    return "managed" if scale < 50_000_000 else "self_hosted"

print(pick(team_size=3, scale=20_000_000, compliance=False))
```

**Q85: What is the cost structure of a managed vector DB?**
A: Typically based on:
- Vector count and dimension
- Query throughput (QPS)
- Storage (RAM vs disk)
- Replication factor
- Data transfer
- Pinecone: per pod-hour; Qdrant Cloud: per cluster-hour; Weaviate Cloud: per unit-hour
- At scale, vector DB can be a significant cost — optimize via quantization, tiered storage

**Code:**
```python
def monthly_cost(vectors, dim, replicas, price_per_gb_hour=0.10):
    gb = vectors * dim * 4 / 1e9 * replicas          # RAM footprint
    return round(gb * price_per_gb_hour * 730, 2)     # × hours in a month

print(monthly_cost(50_000_000, 384, 2))
# quantize (4-32x) or move cold data to disk to cut the bill
```
**Q86: How do you A/B test different vector databases for your use case?**
A: 
1. Define metrics: recall@k, latency p95, QPS, cost
2. Use VectorDBBench or ANN-Benchmarks with your dataset
3. Test with at least 2x your expected production scale
4. Measure build time, query speed, filter performance
5. Test failure scenarios (node loss, network partition)
6. Consider operational complexity

**Code:**
```python
import faiss, numpy as np, time

x = np.random.randn(100_000, 64).astype("float32")
q = np.random.randn(200, 64).astype("float32")
flat = faiss.IndexFlatL2(64); flat.add(x)
_, truth = flat.search(q, 10)                     # ground truth = exact baseline
for name, key in {"IVF": "IVF128,Flat", "HNSW": "HNSW32"}.items():
    idx = faiss.index_factory(64, key)
    if hasattr(idx, "train"): idx.train(x)
    idx.add(x)
    t0 = time.perf_counter(); _, hits = idx.search(q, 10); dt = time.perf_counter() - t0
    recall = np.mean([len(set(a) & set(b)) / 10 for a, b in zip(hits, truth)])
    print(f"{name}: recall@10={recall:.2f}  qps={len(q)/dt:.0f}")
# run at 2x prod scale on your own dataset (VectorDBBench / ANN-Benchmarks)
```

**Q87: What is "failure mode" for a vector DB during high load?**
A: Common failures:
- OOM (Killed): index too large for memory
- Connection pool exhaustion
- Slow queries piling up (thundering herd)
- Index rebuild failing mid-way
- Replication lag causing stale reads
- Mitigations: circuit breakers, bulkhead patterns, autoscaling

**Code:**
```python
from datetime import datetime, timedelta

class Breaker:
    def __init__(self, threshold=5, cooldown_s=30):
        self.fails, self.open_until = 0, None
    def call(self, query):
        if self.open_until and datetime.now() < self.open_until:
            raise RuntimeError("circuit open")          # fail fast, no thundering herd
        try:
            return index.search(query, 10)
        except MemoryError:                              # OOM = #1 failure mode
            self.fails += 1
            if self.fails > self.threshold:
                self.open_until = datetime.now() + timedelta(seconds=self.cooldown_s)
```

**Q88: How do you migrate from one vector DB to another in production?**
A: 
1. Dual-write to both DBs during migration
2. Backfill old data to new DB
3. Verify recall parity with sample queries
4. Gradually shift read traffic (10% → 50% → 100%)
5. Monitor latency, error rate, recall during cutover
6. Decommission old DB after validation period
Rollback plan: keep old DB running until fully validated.

**Code:**
```python
import random

def write_both(id_, vec, meta):
    legacy.upsert(id_, vec, meta)              # rollback target stays hot
    target.upsert(id_, vec, meta)              # dual-write keeps both in sync

def read_from(step):
    db = target if random.random() < step else legacy
    return db.query(query_vector, top_k=10)    # cutover: 10% → 50% → 100%

for step in (0.1, 0.5, 1.0):
    print(read_from(step))
```

**Q89: What is a "staging index" in Pinecone?**
A: Pinecone's serverless architecture uses "staging index" for bulk writes — higher throughput for ingestion but not searchable until promoted. This isolates indexing load from query serving. After indexing completes, the index is promoted to serving state.

**Code:**
```python
import pinecone

pc = pinecone.Pinecone()
index = pc.Index("serverless-index")
index.upsert(vectors=batch, namespace="staging")   # bulk writes, not served yet
index.query(vector=qvec, namespace="staging")      # promoted → becomes searchable
# isolates bulk-ingest load from the query-serving path until promotion
```

**Q90: How do you optimize vector DB costs without sacrificing performance?**
A: 
- Quantization (float32 → binary reduces memory 32x, cost 32x)
- On-disk storage for cold vectors
- Tiered indexing (hot/warm/cold)
- Caching at application layer
- Delete stale/unused vectors
- Downsize during low traffic
- Choose the right pod type / instance size for workload

**Code:**
```python
import numpy as np

v = np.random.randn(100_000, 768).astype("float32")
binary = (v > 0).astype(np.uint8)                       # binary quantization, 32x less memory
print("float32 MB:", round(v.nbytes / 1e6), "-> binary MB:", round(binary.nbytes / 1e6))
# also: on-disk for cold vectors, app-level cache, TTL deletes, downsize off-peak
```
## 6. Ecosystem, Comparisons & Integration (Q91–Q100)

**Q91: How does pgvector compare to dedicated vector databases?**
A: pgvector is a PostgreSQL extension adding vector type + ANN indexes (IVF, HNSW). Pros: existing Postgres ecosystem, transactional consistency, no additional infra. Cons: limited ANN performance vs dedicated DBs, no distributed scaling, fewer features (no hybrid search natively). Best for: apps already on Postgres with <10M vectors.

**Code:**
```python
import psycopg

with psycopg.connect("dbname=app") as conn:
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.execute("CREATE TABLE IF NOT EXISTS docs (id int, embedding vector(768))")
    conn.execute("CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)")
    rows = conn.execute("""
        SELECT id FROM docs ORDER BY embedding <=> %s LIMIT 10
    """, (query_vector,)).fetchall()
    print([r[0] for r in rows])
```

**Q92: Compare Pinecone vs Weaviate vs Qdrant vs Milvus for production use.**
A: 
- Pinecone: easiest setup, fully managed, serverless option, highest cost, closed source
- Weaviate: strongest hybrid search, GraphQL API, open-source, modules for model inference
- Qdrant: fastest filtered search, Rust-based, memory-efficient, best Docker experience
- Milvus: most scalable, Kubernetes-native, GPU support, most complex to operate
- Choose based on: scale (Milvus/Qdrant for large), ease (Pinecone/Chroma), hybrid (Weaviate)

**Code:**
```python
# Same workload, vendor trade-offs — pick by constraint:
vendors = {
    "Pinecone": {"ease": 9, "scale": 7, "hybrid": 4, "cost": 2, "license": "closed"},
    "Weaviate": {"ease": 7, "scale": 7, "hybrid": 9, "cost": 7, "license": "BSL"},
    "Qdrant":   {"ease": 8, "scale": 8, "hybrid": 8, "cost": 8, "license": "Apache"},
    "Milvus":   {"ease": 5, "scale": 9, "hybrid": 7, "cost": 7, "license": "Apache"},
}
print(sorted(vendors, key=lambda v: vendors[v]["scale"], reverse=True))
```

**Q93: How does Elasticsearch's vector search compare to dedicated vector DBs?**
A: Elasticsearch added ANN search via HNSW (Elastic 8.0+). Pros: single stack for full-text + vector, existing ecosystem, mature operations. Cons: vector performance lower than dedicated DBs, higher latency, limited to HNSW only, cost for dense vector storage. Best for: teams already on Elasticsearch with moderate vector scale.

**Code:**
```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
# ES 8+: dense_vector field auto-indexes with HNSW
es.indices.create(index="docs", mappings={
    "properties": {"embedding": {"type": "dense_vector",
                                 "dims": 384, "index": True,
                                 "similarity": "cosine",
                                 "index_options": {"type": "hnsw", "m": 16, "ef_construction": 200}}}})
res = es.search(index="docs", knn={"field": "embedding", "query_vector": q, "k": 10})
print(res["hits"]["hits"][0]["_id"])
```

**Q94: What is Chroma DB and when should you use it?**
A: Chroma is an open-source, embedded vector database for AI applications. Lightweight (pip install), stores data on disk or in-memory, simple Python API, integrates with LangChain and LlamaIndex. Best for: prototyping, small-scale apps, local development, tutorials. Not for production at scale.

**Code:**
```python
import chromadb

client = chromadb.Client()                          # embedded: no server to run
coll = client.create_collection("demo")
coll.upsert(ids=["1", "2"], documents=["Vector DB 101", "SQL joins"],
            embeddings=[[0.1, 0.2], [0.9, 0.8]])
r = coll.query(query_embeddings=[[0.2, 0.1]], n_results=1)
print(r["documents"])   # best for prototyping / local dev, not heavy production
```

**Q95: How do vector databases integrate with LangChain/LlamaIndex?**
A: Both frameworks provide unified vector store abstractions:
- LangChain: `vectorstores` interface with `similarity_search`, `as_retriever`
- LlamaIndex: `VectorStoreIndex` wrapping the DB
- Both support major DBs (Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS)
- Integration handles collection setup, embedding, search, metadata filtering, and retriever creation

**Code:**
```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

store = Chroma.from_texts(
    ["RAG needs retrieval", "Vector DBs scale"],
    embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
retriever = store.as_retriever(search_kwargs={"k": 2})
print([d.page_content for d in retriever.invoke("retrieval")])
```

**Q96: How does a vector database handle binary and float vectors in the same collection?**
A: Depends on the DB. Most require a single vector type per collection. Weaviate named vectors allow mixed. Binary vectors (each component is 0 or 1, stored as bits) use Hamming distance — 32x compression vs float32, good for near-duplicate detection. Float vectors are standard for semantic search.

**Code:**
```python
import numpy as np

a = np.random.randint(0, 2, 384).astype(np.uint8)      # binary embedding
b = np.random.randint(0, 2, 384).astype(np.uint8)
hamming = (np.unpackbits(a) != np.unpackbits(b)).sum()  # Hamming → 32x smaller than float32
print("hamming distance:", hamming)
# same collection usually needs one type; Weaviate named vectors allow mixing
```

**Q97: What is "sparse vector" support in modern vector DBs?**
A: Sparse vectors (e.g., from SPLADE) represent text as high-dimensional, mostly-zero vectors. Qdrant supports sparse vectors natively via `NamedVector` with `modifier: "sparse"`. Weaviate supports via `text2vec-transformers` module with sparse embeddings. Enables hybrid search combining dense semantic + sparse lexical matching.

**Code:**
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")
sparse_vec = models.SparseVector(indices=[3, 17], values=[1.5, 0.8])   # SPLADE-style
client.upsert("docs", points=[models.PointStruct(
    id="1_1", vector={"dense": dense_vec, "sparse": sparse_vec})])
# hybrid: dense semantic + sparse lexical matching in one search
client.query_points("docs", query=["llm", "retrieval"])
```

**Q98: What is a "Tiered Index" architecture in vector databases?**
A: Tiered indexing splits data into hot (RAM), warm (SSD), and cold (object storage) tiers. Queries search tiers based on freshness/frequency. Milvus DiskANN + RAM cache implements this. Qdrant allows per-segment memory mode vs mmap mode. Reduces cost by keeping hot data in RAM and cold data on cheap storage.

**Code:**
```python
from collections import OrderedDict

class TieredIndex:
    def __init__(self, ram_cap):
        self.hot = OrderedDict()          # hot = RAM
        self.cap = ram_cap
    def promote(self, key, vec):
        self.hot[key] = vec; self.hot.move_to_end(key)
        while len(self.hot) > self.cap:   # evict coldest to SSD / object storage
            self.hot.popitem(last=False)
    def search(self, q):
        return list(self.hot.values())    # hot first, then warm/disk tiers
# Milvus DiskANN + RAM cache · Qdrant per-segment memory vs mmap mode
```

**Q99: How does a vector database integrate with a streaming platform like Kafka?**
A: 
- Ingest: consume text/image from Kafka → embed → upsert to vector DB
- Realtime indexing: low-latency embedding + write path
- Qdrant: Kafka sink connector available
- Milvus: Pulsar for internal message queue; can integrate with Kafka for ingestion
- Weaviate: supports webhook automations for streaming

**Code:**
```python
from confluent_kafka import Consumer
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
c = Consumer({"bootstrap.servers": "localhost:9092", "group.id": "vectordb"})
c.subscribe(["articles"])
while True:
    msg = c.poll(1.0)
    if msg and not msg.error():
        text = msg.value().decode()
        vdb.upsert(id=msg.key().decode(),
                   vector=model.encode([text])[0],
                   payload={"text": text})
        # stream → embed → upsert, index stays fresh in near-real-time
```

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

**Code:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("clip-ViT-B-32-multilingual-v1")   # text + image, one space
txt = model.encode(["a red car"])[0]
img = model.encode([Image.open("car.png")])[0]
vdb.upsert([("txt", txt), ("img", img)])
print(vdb.query(txt, top_k=2))      # a text query finds the matching image — multi-modal
```