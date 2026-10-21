# RAG Interview Questions and Answers

## Q1: What is RAG (Retrieval Augmented Generation)?
**A:** RAG is an AI framework that combines information retrieval with text generation. It retrieves relevant documents from a knowledge base and provides them as context to an LLM, enabling the model to generate accurate, grounded responses based on actual data rather than relying solely on parametric knowledge.

**Code:**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

store = FAISS.from_texts(
    ["RAG retrieves relevant documents before generation."],
    OpenAIEmbeddings(),
)
hits = store.similarity_search("How does RAG reduce hallucination?", k=1)
answer = ChatOpenAI().invoke(f"Context: {hits}\nQuestion: How does RAG ground answers?")
print(answer.content)
```

## Q2: Why is RAG important?
**A:** RAG addresses key limitations of LLMs: it provides access to current information (solving knowledge cutoff), reduces hallucinations by grounding responses in retrieved data, enables domain-specific knowledge without retraining, and allows citation of sources for verifiability.

**Code:**
```python
# Inject knowledge newer than the training cutoff, without any retraining.
fresh = ["RAG is the dominant pattern for grounded LLM applications in 2026."]
store = FAISS.from_texts(fresh, OpenAIEmbeddings())
answer = ChatOpenAI().invoke(
    f"Context: {store.similarity_search('latest RAG trend?', k=1)}\n"
    "Answer and cite sources."
)
print(answer.content)
```

## Q3: What are the main components of a RAG system?
**A:** The main components are: 1) Document Ingestion Pipeline (load, split, embed, store), 2) Vector Database (stores embeddings for similarity search), 3) Retriever (finds relevant documents), 4) LLM (generates responses using retrieved context), and 5) Prompt Template (structures the LLM input with context and query).

**Code:**
```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = TextLoader("kb.txt").load()                               # 1 load
chunks = RecursiveCharacterTextSplitter(                        # 2 split
    chunk_size=500, chunk_overlap=50).split_documents(docs)
store = Chroma.from_documents(chunks, OpenAIEmbeddings())       # 3+4 embed & store
hits = store.similarity_search("What is HNSW?", k=3)            # 5 retriever
prompt = f"Context:\n{hits}\nQuestion: What is HNSW?"           # 6 prompt template
answer = ChatOpenAI().invoke(prompt)                            # 7 LLM
```

## Q4: How does a basic RAG pipeline work?
**A:** 1) User submits a query, 2) Query is embedded into a vector, 3) Vector database performs similarity search to find relevant documents, 4) Retrieved documents are added to a prompt as context, 5) LLM generates a response grounded in the provided context, 6) Response with citations is returned to the user.

**Code:**
```python
def basic_rag(query):
    q_vec = embeddings.embed_query(query)                  # 2 embed query
    docs = store.similarity_search_by_vector(q_vec, k=4)   # 3 similarity search
    context = "\n\n".join(d.page_content for d in docs)    # 4 augment prompt
    return ChatOpenAI().invoke(                            # 5 generate
        f"Context:\n{context}\n\nQuestion: {query}"
    )
```

## Q5: What is the difference between RAG and fine-tuning?
**A:** RAG provides external knowledge at inference time without modifying the model. Fine-tuning updates model weights to incorporate new knowledge. RAG is better for frequently changing data and access control. Fine-tuning is better for learning new skills or styles. They are complementary and can be combined.

**Code:**
```python
# RAG: knowledge added at inference time -> no weight changes.
def rag_answer(q):
    return llm.invoke(f"Context: {store.similarity_search(q)}\nQ: {q}")

# Fine-tuning: weights are updated during training.
from sentence_transformers import SentenceTransformer, losses
model = SentenceTransformer("all-MiniLM-L6-v2")
model.fit(train_examples=[("What is RAG?", "Retrieval Augmented Generation.", 1.0)],
          loss=losses.MultipleNegativesRankingLoss(model))
```

## Q6: What types of RAG architectures exist?
**A:** Types include: Naive RAG (retrieve-then-generate), Advanced RAG (with pre/post-retrieval optimizations), Modular RAG (composable modules), Agentic RAG (agents decide retrieval strategy), Corrective RAG (self-correcting retrieval), and Speculative RAG (hypothesis-driven retrieval).

**Code:**
```python
def build_rag(kind, retriever, llm):
    if kind == "naive":      return lambda q: llm.invoke(f"Context: {retriever.q(q)}\nQ: {q}")
    if kind == "advanced":
        return lambda q: llm.invoke(
            f"Context: {rerank(q, retriever.q(q))}\nQ: {rewrite(q)}")
    if kind == "agentic":    return AgentExecutor(agent=agent, tools=[retriever_tool])
```

## Q7: What is Naive RAG?
**A:** Naive RAG is the simplest form: index documents, retrieve relevant chunks, augment prompt, generate response. It is straightforward but suffers from retrieval quality issues, lack of query understanding, and limited context utilization.

**Code:**
```python
def naive_rag(query):
    chunks = vectorstore.similarity_search(query, k=3)        # index -> retrieve
    context = "\n\n".join(c.page_content for c in chunks)     # augment prompt
    return llm.invoke(f"Context:\n{context}\n\nQuestion:\n{query}")   # generate
```

## Q8: What is Advanced RAG?
**A:** Advanced RAG adds pre-retrieval (query rewriting, expansion, decomposition) and post-retrieval (reranking, filtering, compression) optimizations. It improves retrieval accuracy and context quality through techniques like HyDE, query transformation, and multi-step retrieval.

**Code:**
```python
def advanced_rag(query):
    q = llm.invoke(f"Paraphrase for retrieval: {query}")     # pre-retrieval rewrite
    cands = store.similarity_search(q, k=20)
    top = reranker.rerank(q, cands, top_n=5)                 # post-retrieval rerank
    ctx = compress(top, query)                               # context compression
    return llm.invoke(f"Context: {ctx}\nQuestion: {query}")
```

## Q9: What is Modular RAG?
**A:** Modular RAG decomposes the RAG pipeline into interchangeable modules (search, filtering, reranking, memory, fusion, etc.) that can be composed flexibly. This enables custom RAG patterns like search-rerank-generate or multi-query fusion.

**Code:**
```python
from langchain_community.retrievers import BM25Retriever

pipeline = {
    "retriever": [store.as_retriever(), BM25Retriever.from_texts(docs)],
    "reranker": cross_encoder,
    "fusion": rrf,               # Reciprocal Rank Fusion drops in here
    "generator": llm,
}

def compose(query):
    fused = pipeline["fusion"]([r.invoke(query) for r in pipeline["retriever"]])
    return pipeline["generator"].invoke(f"Context: {fused[:5]}\nQ: {query}")
```

## Q10: What is Agentic RAG?
**A:** Agentic RAG uses an AI agent that autonomously decides when and how to retrieve information. The agent can decide whether retrieval is needed, choose which tools/databases to query, perform multi-step research, refine queries, and synthesize results from multiple sources.

**Code:**
```python
from langchain.agents import AgentExecutor, create_openai_tools_agent

agent = create_openai_tools_agent(llm, [retriever_tool, search_tool], prompt)
result = AgentExecutor(agent=agent, tools=[retriever_tool, search_tool]).invoke({
    "input": "Research the latest RAG papers, then summarize whether RAG beats fine-tuning."
})
```

## Q11: What is a vector database?
**A:** A vector database stores and indexes high-dimensional vector embeddings for fast similarity search. It supports operations like ANN (Approximate Nearest Neighbor) search, metadata filtering, and hybrid search. Examples include Pinecone, Weaviate, Qdrant, Chroma, and Milvus.

**Code:**
```python
import chromadb

client = chromadb.PersistentClient(path="./kb")
col = client.get_or_create_collection("docs", metadata={"hnsw:space": "cosine"})
col.add(ids=["1", "2"],
        embeddings=[[0.10, 0.20], [0.30, 0.40]],
        documents=["HNSW is a graph index.", "IVF partitions the space."])
hits = col.query(query_embeddings=[[0.11, 0.21]], n_results=2)
```

## Q12: How does similarity search work in vector databases?
**A:** Vector databases index embeddings using algorithms like HNSW (Hierarchical Navigable Small Worlds), IVF (Inverted File Index), or PQ (Product Quantization). Given a query vector, they find nearest neighbors using distance metrics like cosine similarity, Euclidean distance, or dot product.

**Code:**
```python
import numpy as np

def cosine(a, b):
    return float(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))

q = np.array([1.0, 0.0])
vectors = {"d1": np.array([0.95, 0.30]), "d2": np.array([-0.2, 0.9]), "d3": np.array([0.80, 0.60])}
ranked = sorted(vectors, key=lambda k: cosine(q, vectors[k]), reverse=True)
print(ranked)  # nearest neighbor first
```

## Q13: What are embeddings in RAG?
**A:** Embeddings are dense vector representations of text (or other data) that capture semantic meaning. In RAG, both documents and queries are embedded into the same vector space. Semantic similarity is measured by distance between vectors.

**Code:**
```python
from openai import OpenAI

client = OpenAI()
resp = client.embeddings.create(
    model="text-embedding-3-small",
    input=["RAG is retrieval augmented generation.", "How does RAG work?"],
)
vecs = [d.embedding for d in resp.data]
print(len(vecs), "vectors of dim", len(vecs[0]))  # same space -> comparable
```

## Q14: What embedding models are commonly used for RAG?
**A:** Popular embedding models include: OpenAI text-embedding-3-small/large, Cohere embed-english-v3.0, Google text-embedding-004, Sentence Transformers (all-MiniLM-L6-v2, BAAI/bge-large-en-v1.5), and open-source models from Mistral, Voyage AI, and Jina AI.

**Code:**
```python
from sentence_transformers import SentenceTransformer

small = SentenceTransformer("all-MiniLM-L6-v2")        # 384-dim, fast, CPU-friendly
large = SentenceTransformer("BAAI/bge-large-en-v1.5")  # 1024-dim, higher quality
print(small.encode("hello").shape, large.encode("hello").shape)
```

## Q15: What is chunking in RAG?
**A:** Chunking splits documents into smaller, coherent pieces before embedding and indexing. Good chunking preserves semantic boundaries, respects content structure, and creates chunks of appropriate size for retrieval. Strategies include fixed-size, recursive, semantic, and document-aware chunking.

**Code:**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=24)
chunks = splitter.split_text(article)
print(f"{len(chunks)} chunks; first chunk = {len(chunks[0])} chars")
```

## Q16: What chunking strategies are there?
**A:** Strategies include: Fixed-size (N characters with overlap), Recursive (split on separators like paragraphs and sentences), Semantic (based on embedding similarity changes), Document-aware (respecting Markdown/HTML structure), and Sentence-based (NLTK/spaCy sentence splitting).

**Code:**
```python
from langchain_text_splitters import (CharacterTextSplitter,
                                      MarkdownHeaderTextSplitter,
                                      RecursiveCharacterTextSplitter,
                                      SemanticChunker)

fixed     = CharacterTextSplitter(chunk_size=300)              # fixed-size
recursive = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ".", " "])
semantic  = SemanticChunker(embedding=OpenAIEmbeddings())      # embedding-based
md        = MarkdownHeaderTextSplitter([("##", "Section")])    # document-aware
```

## Q17: What is the optimal chunk size for RAG?
**A:** Optimal chunk size depends on the use case and LLM context window. Typical sizes range from 256-1024 tokens. Smaller chunks provide precise retrieval but may lack context. Larger chunks provide more context but may introduce noise. Experimentation is key.

**Code:**
```python
for size in (256, 512, 1024):
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=size // 5)
    store = Chroma.from_documents(splitter.split_documents(docs), OpenAIEmbeddings())
    hit = hit_rate(store, eval_questions, k=5)   # measure @k on YOUR dataset
    print(size, "hit_rate@5 =", hit)             # pick the best-scoring chunk size
```

## Q18: What is chunk overlap?
**A:** Chunk overlap adds a sliding window of N characters/tokens between consecutive chunks. This prevents information loss at chunk boundaries. Common overlap is 10-20% of chunk size. Overlap increases storage but improves retrieval completeness.

**Code:**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
chunks = splitter.split_text("the quick brown fox jumps over an indolent dog")
# tail of chunk[0] repeats at the head of chunk[1] -> boundary info survives
print(chunks[0][-10:], "|", chunks[1][:10])
```

## Q19: What is a retriever in RAG?
**A:** A retriever takes a user query and returns relevant documents from the knowledge base. Retrievers can be sparse (BM25, TF-IDF), dense (embedding-based), hybrid (combining sparse and dense), or multi-modal.

**Code:**
```python
from langchain_community.retrievers import BM25Retriever

dense_retriever  = store.as_retriever(search_kwargs={"k": 4})
sparse_retriever = BM25Retriever.from_documents(docs)
docs = [dense_retriever.invoke("What is a retriever?"),
        sparse_retriever.invoke("retriever")]      # dense + sparse -> hybrid
```

## Q20: What is dense retrieval?
**A:** Dense retrieval uses neural embeddings to represent queries and documents as dense vectors, then finds nearest neighbors in embedding space. It captures semantic similarity beyond keyword matching but requires good embedding models.

**Code:**
```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
q = model.encode("largest city?", normalize_embeddings=True)
ds = model.encode(["Paris is the capital.", "New York is the largest."],
                  normalize_embeddings=True)
print(util.cos_sim(q, ds))          # semantic neighbors in vector space
```

## Q21: What is sparse retrieval (BM25)?
**A:** BM25 is a keyword-based retrieval algorithm that ranks documents by term frequency and inverse document frequency. It is fast, does not require embeddings, excels at exact keyword matching, and is often used as a baseline or in hybrid retrieval systems.

**Code:**
```python
from rank_bm25 import BM25Okapi

corpus = [["the", "cat", "sat"], ["the", "dog", "ran"]]
bm25 = BM25Okapi(corpus)
print(bm25.get_scores(["cat"]))   # a higher score where the term appears
```

## Q22: What is hybrid retrieval?
**A:** Hybrid retrieval combines dense (semantic) and sparse (keyword) retrieval results, typically using weighted fusion (RRF, weighted sum, or learning to rank). This leverages the strengths of both approaches: semantic understanding from dense and exact matching from sparse.

**Code:**
```python
def hybrid_scores(query, alpha=0.5):
    dense = dense_score(query)              # embedding similarity, 0..1
    sparse = bm25.get_scores(query.split()) # raw BM25 term-matching score
    return [alpha * d + (1 - alpha) * s for d, s in zip(dense, sparse)]
```

## Q23: What is Reciprocal Rank Fusion (RRF)?
**A:** RRF combines multiple ranked lists by scoring each document as the sum of reciprocal ranks: score = sum of 1/(k + rank_i(d)). It is parameter-free and effective for fusing results from different retrieval methods without training.

**Code:**
```python
def rrf(*rank_lists, k=60):
    scores = {}
    for ranks in rank_lists:
        for rank, doc_id in enumerate(ranks):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)

fused = rrf(bm25_ranking, dense_ranking)
```

## Q24: What is query rewriting in RAG?
**A:** Query rewriting transforms the user's original query to improve retrieval quality. Examples include expanding acronyms, correcting spelling, adding synonyms, decomposing complex queries, and converting conversational queries into standalone search queries.

**Code:**
```python
def rewrite_query(raw, history=None):
    if history:
        return llm.invoke(f"Dereference follow-up '{raw}' using history {history}")
    return llm.invoke(f"Turn '{raw}' into a precise standalone search query: ").content
```

## Q25: What is HyDE (Hypothetical Document Embeddings)?
**A:** HyDE generates a hypothetical ideal document that would answer the query, embeds that instead of the query, and retrieves documents similar to the hypothesis. This bridges the vocabulary gap between short queries and long documents.

**Code:**
```python
from langchain.chains.hyde import HypotheticalDocumentEmbedder
from langchain_openai import OpenAIEmbeddings

hyde = HypotheticalDocumentEmbedder.from_llm_embeddings(llm, OpenAIEmbeddings())
q_vec = hyde.embed_query("How does HNSW work?")   # embed a hypothetical answer
docs = store.similarity_search_by_vector(q_vec, k=3)
```

## Q26: What is query expansion?
**A:** Query expansion adds related terms, synonyms, or generated variations to the original query before retrieval. This broadens the search to capture more relevant documents. Techniques include synonym expansion, LLM-generated expansions, and relevance feedback-based expansion.

**Code:**
```python
synonyms = {"car": "automobile vehicle sedan", "buy": "purchase acquire"}

def expand(query):
    tokens = query.lower().split()
    extra = [synonyms[t] for t in tokens if t in synonyms]
    return " ".join(tokens + extra)

print(expand("buy a car"))   # also searches "purchase acquire automobile..."
```

## Q27: What is query decomposition?
**A:** Query decomposition breaks a complex question into simpler sub-questions, retrieves documents for each sub-question, and synthesizes the results. For example, comparing the economies of France and Japan becomes separate queries for each country.

**Code:**
```python
sub_questions = llm.invoke(f"Decompose into sub-questions: {complex_q}").content.split("\n")
answers = [rag_answer(sq) for sq in sub_questions]               # retrieve per sub-question
synthesis = llm.invoke(f"Combine these answers:\n{answers}\nOriginal: {complex_q}")
```

## Q28: What is multi-hop RAG?
**A:** Multi-hop RAG requires multiple rounds of retrieval, where information from one retrieval informs the next query. This is needed for questions that require connecting information across multiple documents.

**Code:**
```python
def multi_hop(query, hops=3):
    context = []
    for _ in range(hops):
        q = f"{query}\nEvidence so far:\n{context}"
        context += [d.page_content for d in store.similarity_search(q, k=2)]
        if enough_info(context):
            break
    return llm.invoke(f"Evidence:\n{context}\nQuestion: {query}")
```

## Q29: What is iterative retrieval?
**A:** Iterative retrieval performs multiple rounds of retrieval, using results from previous rounds to refine the query. Each iteration can use the LLM's assessment of missing information to formulate better follow-up queries.

**Code:**
```python
def iterative_retrieval(query, max_rounds=4):
    q = query
    for _ in range(max_rounds):
        docs = store.similarity_search(q, k=5)
        q = llm.invoke(
            f"To answer '{query}', what is still missing? Given: {docs}").content
        if "nothing missing" in q:
            break
    return docs
```

## Q30: What is RAPTOR?
**A:** RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) builds a hierarchical tree of document summaries. Documents are chunked, embedded, clustered, and summarized recursively. Retrieval navigates this tree at appropriate levels of abstraction.

**Code:**
```python
from sklearn.cluster import AgglomerativeClustering

def summarize_level(texts, depth=0, max_depth=3):
    if depth == max_depth:
        return texts
    embs = embeddings.embed_documents(texts)
    labels = AgglomerativeClustering(n_clusters=None,
                                     distance_threshold=1.2).fit_predict(embs)
    out = []
    for cluster in set(labels):
        group = [t for t, l in zip(texts, labels) if l == cluster]
        out.append(llm.invoke(f"Summarize:\n{group}").content)
    return summarize_level(out, depth + 1, max_depth)   # build tree recursively
```

## Q31: What is Reranking in RAG?
**A:** Reranking takes the initial retrieval results (top-k from fast retrieval) and re-evaluates them using a more accurate but slower model (cross-encoder). This improves precision by reordering results based on deeper relevance assessment.

**Code:**
```python
from sentence_transformers import CrossEncoder

ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
cands = store.similarity_search(query, k=20)                  # fast first-pass
scores = ce.predict([(query, c.page_content) for c in cands]) # slow precise scoring
top5 = [c for _, c in sorted(zip(scores, cands), reverse=True)[:5]]
```

## Q32: What are cross-encoders for reranking?
**A:** Cross-encoders jointly process query-document pairs through a transformer, producing a relevance score. They are more accurate than bi-encoders but slower since each pair must be processed together.

**Code:**
```python
from sentence_transformers import CrossEncoder

ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
# query and document pass through the transformer together as one input:
score = ce.predict([("what is HNSW?", "HNSW is a graph-based ANN index.")])[0]
```

## Q33: What is the difference between bi-encoders and cross-encoders?
**A:** Bi-encoders encode query and document independently into fixed vectors (fast, scalable for retrieval). Cross-encoders process query-document pairs together (slow but accurate). Bi-encoders are used for initial retrieval; cross-encoders for reranking.

**Code:**
```python
# Bi-encoder: independent vectors -> embed once, reuse for millions of docs.
q_vec, d_vec = bi.encode([query, doc])
fast = float((q_vec @ d_vec).item())

# Cross-encoder: joint pair -> one score per pair, used only for top-k rerank.
precise = cross.predict([(query, doc)])[0]
```

## Q34: What is Cohere Rerank?
**A:** Cohere Rerank is a hosted reranking API that uses a cross-encoder model to score query-document relevance. It takes a query and a list of documents, returns relevance scores, and improves RAG quality by filtering out irrelevant documents.

**Code:**
```python
import cohere

co = cohere.Client(api_key=COHERE_KEY)
result = co.rerank(model="rerank-english-v3.0",
                   query=query,
                   documents=[d.page_content for d in candidates],
                   top_n=3)
for r in result.results:
    print(r.index, round(r.relevance_score, 3))
```

## Q35: What is the Lost-in-the-Middle problem?
**A:** The Lost-in-the-Middle problem refers to LLMs ignoring information in the middle of long contexts. When multiple retrieved documents are provided, those in the middle receive less attention. Solutions include placing the most relevant documents first and last.

**Code:**
```python
def reorder_for_attention(docs):
    docs.sort(key=lambda d: d.metadata["score"], reverse=True)
    if len(docs) < 2:
        return docs
    best, rest = docs[0], docs[1:]
    return [best] + rest[1:] + [rest[0]]   # strongest at start AND end
```

## Q36: How does context window size affect RAG?
**A:** Larger context windows allow more retrieved documents and longer documents. However, they do not solve the Lost-in-the-Middle problem and increase computational cost. Typical strategies include limiting to top-k documents and compressing context.

**Code:**
```python
def fit_budget(docs, budget_tokens):
    out, used = [], 0
    for c in sorted(docs, key=lambda d: d.metadata["score"], reverse=True):
        n = num_tokens(c.page_content)
        if used + n > budget_tokens:
            break
        out.append(c); used += n
    return out   # most relevant docs that still fit the LLC context window
```

## Q37: What is context compression in RAG?
**A:** Context compression reduces retrieved documents to only the most relevant parts before feeding them to the LLM. Techniques include extractive compression (select relevant sentences), abstractive compression (LLM summarizes), and selective retrieval.

**Code:**
```python
import nltk

def extractive_compress(docs, query, k=2):
    out = []
    for d in docs:
        sents = nltk.sent_tokenize(d.page_content)
        scored = sorted(sents, key=lambda s: similarity(query, s), reverse=True)
        out.extend(scored[:k])                  # keep only the k most relevant sentences
    return " ".join(out)
```

## Q38: What is the RAG prompt template?
**A:** A RAG prompt template structures the LLM input with system instructions, retrieved context (with source references), and user query. Example: "Answer the question based on the context. If the context does not contain the answer, say so."

**Code:**
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Answer based only on the context. If the answer is absent, say so.\n"
    "Context:\n{context}\n\nQuestion: {question}"
)
answer = llm.invoke(prompt.format(context=retrieved, question=query))
```

## Q39: How do you structure RAG prompts for best results?
**A:** Place context before the question, clearly separate context from instruction, include source attribution, ask the model to cite sources, instruct the model to say "I don't know" if the answer is not in context, and handle cases with no retrieved documents.

**Code:**
```python
TEMPLATE = (
    "You are a helpful assistant. Use ONLY the retrieved context.\n"
    "Context:\n{context}\n\n"
    "Rules: cite each fact as [n]; if absent, say exactly 'I don't know'.\n"
    "Question: {question}\nAnswer:"
)
```

## Q40: What is RAG evaluation?
**A:** RAG evaluation measures retrieval quality (precision, recall, MRR, NDCG), generation quality (faithfulness, answer relevance, completeness), and end-to-end metrics. Frameworks like RAGAS, TruLens, and ARES provide comprehensive evaluation.

**Code:**
```python
def recall_at_k(relevant, retrieved, k=5):
    return len(relevant & set(retrieved[:k])) / max(1, len(relevant))

def reciprocal_rank(relevant, retrieved):
    for i, pid in enumerate(retrieved, 1):
        if pid in relevant:
            return 1.0 / i
    return 0.0

def ndcg(relevant, retrieved, k=10):
    hits = [1 if p in relevant else 0 for p in retrieved[:k]]
    dcg = sum(h / __import__("math").log2(i + 2) for i, h in enumerate(hits))
    return dcg / (sum(1 / __import__("math").log2(i + 2) for i in range(min(k, len(relevant)))) + 1e-9)
```

## Q41: What is RAGAS?
**A:** RAGAS (RAG Assessment) is a framework for evaluating RAG systems. It measures Faithfulness (is the answer grounded in context?), Answer Relevance (does the answer address the question?), Context Precision (are retrieved documents relevant?), and Context Recall (are all relevant documents retrieved?).

**Code:**
```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (answer_relevancy, context_precision, context_recall,
                           faithfulness)

ds = Dataset.from_dict({
    "question": ["What is RAG?"],
    "answer": ["RAG retrieves context, then generates."],
    "contexts": [["RAG = Retrieval-Augmented Generation."]],
})
print(evaluate(ds, metrics=[faithfulness, answer_relevancy,
                            context_precision, context_recall]))
```

## Q42: What is faithfulness in RAG evaluation?
**A:** Faithfulness measures whether the generated answer is supported by the retrieved context. It checks for hallucinations or claims not present in the context. High faithfulness means the model does not add unsupported information.

**Code:**
```python
from ragas.metrics import faithfulness

score = faithfulness.answer(answer, contexts)   # 0..1, 1 = fully grounded
print("faithfulness:", score)
```

## Q43: What is answer relevance in RAG?
**A:** Answer relevance measures how well the generated answer addresses the user's question. Irrelevant details or overly generic responses score low. It is typically measured by computing similarity between the answer and the question.

**Code:**
```python
from ragas.metrics import answer_relevancy

score = answer_relevancy.answer(question, answer)   # higher = more on-topic
print("answer relevance:", score)
```

## Q44: What is context precision?
**A:** Context precision measures whether the retrieved documents are relevant to the question. It penalizes retrieval of irrelevant documents. High precision means most retrieved chunks contain information useful for answering the query.

**Code:**
```python
from ragas.metrics import context_precision

score = context_precision.score(question, retrieved_contexts)  # penalizes noise chunks
print("context precision:", score)
```

## Q45: What is context recall?
**A:** Context recall measures whether all necessary information to answer the question was retrieved. It penalizes missing relevant information. Low recall means the LLM lacks sufficient context and may hallucinate or fail to answer.

**Code:**
```python
from ragas.metrics import context_recall

score = context_recall.score(question, ground_truth, retrieved_contexts)
print("context recall:", score)
```

## Q46: How do you handle cases where no relevant documents are retrieved?
**A:** Strategies include: instruct the LLM to say "I don't have enough information", fall back to general knowledge (optionally flagged), try alternative retrieval (different embedding model, BM25), expand the query, or use rephrased queries.

**Code:**
```python
def robust_rag(q):
    docs = store.similarity_search(q, k=3)
    if not docs or docs[0].metadata["score"] < 0.4:
        docs = fallback_retriever.invoke(q)        # BM25, rephrased query, other model
    if not docs:
        return "I don't have enough information."  # honest refusal / flagged general answer
    return llm.invoke(f"Context: {docs}\nQ: {q}")
```

## Q47: What is self-RAG?
**A:** Self-RAG (by Asai et al.) is a framework where the LLM decides when to retrieve, generates reflections on retrieved passages (is it relevant, supporting, or refuting), and uses special tokens to control retrieval and generation steps.

**Code:**
```python
def self_rag(q, max_steps=5):
    context = []
    for _ in range(max_steps):
        if llm.decide(q) == "Retrieve":            # special token: retrieve?
            docs = retriever.invoke(q)
            context += [d for d in docs if llm.reflect(d) == "Relevant"]  # filter passages
        answer = llm.invoke(f"Context: {context}\nQ: {q}")
        if llm.reflect(answer) == "Supported":     # generation reflection token
            return answer
    return answer
```

## Q48: What is Corrective RAG (CRAG)?
**A:** CRAG evaluates the relevance of retrieved documents and takes corrective action: if documents are relevant it generates; if some are relevant it filters and keeps only relevant ones; if none are relevant it falls back to web search or LLM knowledge.

**Code:**
```python
def corrective_rag(q, threshold=0.6):
    docs = retriever.invoke(q)
    scores = eval_model([(q, d.page_content) for d in docs])
    if max(scores) >= threshold:                 # relevant -> generate
        return llm.invoke(f"Context: {docs}\nQ: {q}")
    kept = [d for d, s in zip(docs, scores) if s >= threshold]
    if kept:                                      # partially relevant -> filter
        return llm.invoke(f"Context: {kept}\nQ: {q}")
    return llm.invoke(f"Context: {web_search(q)}\nQ: {q}")   # fallback to web / LLM knowledge
```

## Q49: What is Speculative RAG?
**A:** Speculative RAG generates multiple possible answers from different document subsets (speculations), then evaluates them against the full set of retrieved documents. It improves both speed and accuracy.

**Code:**
```python
def speculative_rag(q):
    drafts = [llm.invoke(f"Answer using subset:\n{sub}\nQ: {q}")
              for sub in doc_subsets]            # several speculations in parallel
    return llm.invoke(f"Select the best-supported answer for: {q}\nDrafts: {drafts}")
```

## Q50: What is Graph RAG?
**A:** Graph RAG uses knowledge graphs instead of (or alongside) vector databases for retrieval. It captures entities, relationships, and community structure. Queries traverse the graph to find relevant information. Developed by Microsoft.

**Code:**
```python
import networkx as nx

G = nx.Graph()
G.add_edges_from([("RAG", "retriever"), ("RAG", "generator"), ("generator", "LLM")])
context = list(nx.bfs_tree(G, "RAG"))      # traverse relations instead of sim-search
print(context)
```

## Q51: How does Graph RAG work?
**A:** 1) Build a knowledge graph from documents (extract entities and relationships), 2) Detect communities using graph algorithms (Leiden clustering), 3) Generate summaries for communities, 4) For a query, find relevant communities and entities, 5) Retrieve connected information from the graph, 6) Augment the LLM with structured graph context.

**Code:**
```python
G = nx.Graph()
for doc in documents:
    for h, r, t in llm.extract_triples(doc):      # 1 build graph
        G.add_edge(h, t, relation=r)
comms = nx.community.greedy_modularity_communities(G)   # 2 community detection
summaries = [llm.invoke(f"Summarize community: {c}").content for c in comms]  # 3 summarize
hits = set()
for node in link_entities(query, G):              # 4 link query entities
    hits |= set(nx.ego_graph(G, node, radius=2).nodes)   # 5 retrieve connected info
answer = llm.invoke(f"Graph context: {hits} {summaries}\nQ: {query}")      # 6 generate
```

## Q52: What is Agentic RAG vs Simple RAG?
**A:** Simple RAG retrieves once and generates. Agentic RAG uses an AI agent that decides if retrieval is needed, chooses which sources to query, writes its own search queries, performs multi-step research, and synthesizes answers from multiple sources.

**Code:**
```python
def simple_rag(q):
    return llm.invoke(f"Context: {retriever.invoke(q)}\nQ: {q}")   # retrieve once

def agentic_rag(q):
    agent = create_openai_tools_agent(llm, [retriever_tool, search_tool], prompt)
    return AgentExecutor(agent=agent, tools=[retriever_tool, search_tool]).invoke({
        "input": q})["output"]                  # agent drives the retrieval loop
```

## Q53: What is Multi-Modal RAG?
**A:** Multi-Modal RAG retrieves and generates across multiple data types: text, images, tables, audio, and video. It uses multi-modal embeddings (CLIP, SigLIP) for cross-modal retrieval and multi-modal LLMs (GPT-4V, Gemini) for generation.

**Code:**
```python
from PIL import Image
from sentence_transformers import SentenceTransformer, util

clip = SentenceTransformer("clip-ViT-B-32")
text_emb = clip.encode("a red apple")
img_emb = clip.encode(Image.open("apple.png"))
print(float(util.cos_sim(text_emb, img_emb)))   # cross-modal similarity in one space
```

## Q54: What is Multi-Vector RAG?
**A:** Multi-Vector RAG creates multiple embeddings per document (chunk, summary, keywords, hypothetical questions). At retrieval time, it can match against different representations, improving coverage. The full document is provided as context.

**Code:**
```python
from langchain.retrievers.multi_vector import MultiVectorRetriever

retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=docstore)
# several embeddings per document: summary, keywords, hypothetical questions
retriever.vectorstore.add_texts(
    texts=[doc.summary, doc.keywords, doc.hypothetical_question],
    metadatas=[{"doc_id": doc.id}] * 3,
)
context = retriever.docstore.mget([doc.id])[0]   # serve the FULL document, not the vector
```

## Q55: What is Parent Document Retrieval?
**A:** Parent Document Retrieval stores chunks at two levels: small child chunks (for precise retrieval) and larger parent chunks (for full context). It retrieves the most relevant child chunk but provides the parent chunk as context.

**Code:**
```python
def parent_document_retrieval(query):
    child = child_store.similarity_search(query, k=2)[0]   # precise child hits
    return parent_map[child.metadata["parent_id"]]          # rich parent context
```

## Q56: What is Sentence Window Retrieval?
**A:** Sentence Window Retrieval embeds individual sentences for precise retrieval but provides surrounding sentences (a window) as context. This ensures the LLM gets sufficient context while maintaining precise retrieval.

**Code:**
```python
def sentence_window(query, half=2):
    hit = sentence_store.similarity_search(query, k=1)[0]   # match ONE sentence
    idx = sentences.index(hit.page_content)
    return " ".join(sentences[max(0, idx - half): idx + half + 1])  # return the window
```

## Q57: What are metadata filters in RAG?
**A:** Metadata filters restrict retrieval to documents with specific metadata attributes such as date range, author, category, source, or document type. This improves precision by narrowing the search space before similarity search.

**Code:**
```python
docs = store.similarity_search(q, k=5,
    filter={"source": "finance", "year": {"$gte": 2024}})   # narrow search space first
```

## Q58: What is time-weighted retrieval?
**A:** Time-weighted retrieval biases results toward more recent documents by combining relevance scores with recency weights. It is useful for domains where information freshness matters such as news and finance.

**Code:**
```python
from langchain.retrievers import TimeWeightedVectorStoreRetriever

retriever = TimeWeightedVectorStoreRetriever(vectorstore=store,
                                             decay_rate=0.05, k=4)
docs = retriever.invoke("What are the latest policy changes?")
```

## Q59: What is the Curse of Dimensionality in vector search?
**A:** The Curse of Dimensionality refers to distances between points becoming less meaningful in high-dimensional spaces. For very high dimensional embeddings (e.g., 4096d), nearest neighbor search becomes less effective, requiring dimensionality reduction or quantization.

**Code:**
```python
import numpy as np

rng = np.random.default_rng(0)
for dim in (8, 128, 1024):                        # distances flatten as dim grows
    pts = rng.normal(size=(1000, dim))
    d = np.linalg.norm(pts[:, None] - pts[None], axis=2)
    print(dim, "relative std:", round(float(d.std() / d.mean()), 4))
```

## Q60: How do you scale RAG systems?
**A:** Scaling strategies include sharding vector databases across nodes, using ANN indexes, implementing caching for frequent queries, batch document ingestion, distributed processing, and optimizing embedding generation with batching.

**Code:**
```python
import faiss

index = faiss.index_factory(dim, "IVF4096,Flat")  # ANN index for large corpora
index.train(vectors); index.add(vectors)          # train once, add per batch/shard
D, I = index.search(q_vec, k=10)
cached = lru_cache(similarity_search)              # cache frequent queries
```

## Q61: What is incremental indexing in RAG?
**A:** Incremental indexing adds new documents to the vector database without re-indexing existing ones. New documents are embedded and upserted into the index. This enables real-time updates and requires vector DB support for dynamic updates.

**Code:**
```python
def add_documents(new_docs):
    # embed only the new documents and upsert — existing vectors are untouched
    embs = embeddings.embed_documents([d.page_content for d in new_docs])
    index.add(np.array(embs, dtype="float32"))       # append, never full rebuild
```

## Q62: What is the difference between ANN and KNN search?
**A:** KNN (k-Nearest Neighbors) finds exact nearest neighbors by comparing against all vectors (accurate but slow). ANN (Approximate Nearest Neighbor) uses indexes like HNSW to find approximate neighbors quickly (faster, slightly less accurate).

**Code:**
```python
import faiss

knn = faiss.IndexFlatL2(dim)      # exact: scans every vector, O(n)
ann = faiss.IndexHNSWFlat(dim, 32)  # approximate: graph traversal, O(log n)
```

## Q63: What are the different ANN algorithms?
**A:** Common ANN algorithms: HNSW (best for high recall), IVF (memory efficient), PQ (Product Quantization - memory efficient), DiskANN (for SSD-based indexes), and LSH (Locality-Sensitive Hashing).

**Code:**
```python
import faiss

dim = 768
faiss.IndexHNSWFlat(dim, 32)                                    # HNSW: recall-first
faiss.IndexIVFFlat(faiss.IndexFlatL2(dim), dim, nlist=100)      # IVF: memory-efficient
faiss.IndexIVFPQ(faiss.IndexFlatL2(dim), dim, nlist, 8, 8)      # PQ: compresses vectors
faiss.IndexLSH(dim, nbits=128)                                  # LSH: hashing
```

## Q64: What is HNSW?
**A:** HNSW (Hierarchical Navigable Small World) is a graph-based ANN algorithm. It builds a multi-layer graph where upper layers have fewer nodes with long-range connections and lower layers have more nodes with short-range connections. Search traverses from top to bottom.

**Code:**
```python
import faiss

index = faiss.IndexHNSWFlat(dim, M=32)   # M neighbors per node
index.hnsw.efConstruction = 200          # build quality vs. speed
index.hnsw.efSearch = 64                 # search accuracy vs. latency
index.add(vectors)
D, I = index.search(q_vec, k=10)         # traverse top layer down to the bottom
```

## Q65: What is IVF (Inverted File Index)?
**A:** IVF partitions the vector space into Voronoi cells using k-means clustering. At search time, it searches only the closest cells to the query. IVF is memory-efficient but slower than HNSW for very high recall requirements.

**Code:**
```python
import faiss

index = faiss.IndexIVFFlat(faiss.IndexFlatL2(dim), dim, nlist=256)  # k-means cells
index.train(vectors)
index.add(vectors)
index.nprobe = 8                          # only the closest cells are searched
D, I = index.search(q_vec, k=10)
```

## Q66: What is Product Quantization (PQ)?
**A:** PQ compresses vectors by splitting them into sub-vectors and quantizing each sub-vector separately with a codebook. This dramatically reduces memory (16x-64x compression) at the cost of some accuracy. Often used with IVF.

**Code:**
```python
import faiss

index = faiss.IndexPQ(dim, m=8, nbits=8)  # 8 subvectors, 8-bit codebook each
index.train(vectors)
index.add(vectors)
D, I = index.search(q_vec, k=10)          # ~16x smaller than float32 vectors
```

## Q67: What is the role of a Parser in document ingestion?
**A:** A parser extracts text and structure from raw documents. Different parsers handle different formats: PDF (PyMuPDF, Unstructured), HTML (BeautifulSoup), Markdown, DOCX, and images (OCR with Tesseract).

**Code:**
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("spec.pdf")          # PDF parser extracts text + layout
pages = loader.load()
print(pages[0].page_content[:80])
```

## Q68: How do you handle PDFs in RAG?
**A:** PDF handling challenges include mixed content (text, images, tables), multi-column layouts, headers/footers extracting incorrectly, and scanned documents. Solutions include using specialized PDF parsers (PyMuPDF, marker, docling) and OCR for scanned PDFs.

**Code:**
```python
from pypdf import PdfReader
import pytesseract                       # OCR for scanned pages

for page in PdfReader("mixed.pdf").pages:
    text = page.extract_text()           # digital layer
    if not text.strip():                 # scanned -> OCR fallback
        text = pytesseract.image_to_string(page.to_image())
```

## Q69: What is table extraction in RAG?
**A:** Table extraction identifies and preserves tabular data from documents. Approaches include rule-based (regex, layout analysis), ML-based (Table Transformer), and LLM-based (prompted extraction). Preserved tables can be linearized into text.

**Code:**
```python
import pandas as pd

tables = pd.read_html("report.html")                    # rule-based extraction
linearized = "\n".join(t.to_markdown() for t in tables)  # keep tables as structured context
vectorstore.add_texts([linearized])
```

## Q70: What is the difference between structured and unstructured data in RAG?
**A:** Structured data is organized (SQL tables, CSV, JSON, knowledge graphs). Unstructured data is free-form (text, PDF, images). RAG traditionally handles unstructured data via chunking and embeddings. Structured data requires text-to-SQL or graph traversal approaches.

**Code:**
```python
# Unstructured: chunk + embed + vector similarity search.
docs = vectorstore.similarity_search(q)

# Structured: generate and run a query, then feed the rows as context.
sql = llm.invoke(f"Schema: {schema}\nSQL for: {q}")
rows = db.execute(sql).fetchall()
answer = llm.invoke(f"Rows: {rows}\nAnswer: {q}")
```

## Q71: What is Text-to-SQL in RAG?
**A:** Text-to-SQL converts natural language questions into SQL queries, retrieves results from databases, and uses those results as context for the LLM. This enables RAG over structured databases.

**Code:**
```python
def text_to_sql(question):
    sql = llm.invoke(f"Schema:\n{schema}\nWrite SQL for: {question}")
    try:
        rows = db.execute(sql).fetchall()
    except Exception as e:
        sql = llm.invoke(f"Fix this SQL ({e}): {sql}")     # self-correct on error
        rows = db.execute(sql).fetchall()
    return llm.invoke(f"Answer {question} from rows:\n{rows}")
```

## Q72: What is a RAG agent?
**A:** A RAG agent is an AI agent that uses retrieval as a tool. It decides whether to retrieve, what to search for, which sources to query, when to stop searching, and how to synthesize information. Agents enable adaptive retrieval strategies.

**Code:**
```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools=[retriever_tool, web_search_tool])
for step in agent.stream({"messages": [("user", question)]}):
    print(step)   # observe the agent deciding to retrieve, read, stop, and answer
```

## Q73: How do you handle real-time data in RAG?
**A:** For real-time data: use web search tools, continuously ingest streaming data, implement incremental indexing, use time-decayed relevance scoring, maintain a hot cache for frequent queries, and set up data pipelines for document ingestion.

**Code:**
```python
def live_rag(q):
    fresh = web_search_tool.invoke(q)          # real-time source
    indexed = vectorstore.similarity_search(q, k=3)   # incremental, always-updated index
    return llm.invoke(f"Context: {fresh + indexed}\nQuestion: {q}")
```

## Q74: What is data freshness in RAG?
**A:** Data freshness measures how up-to-date the knowledge base is. Strategies include timestamping documents, using time-weighted retrieval, scheduling re-indexing jobs, implementing incremental updates, and integrating real-time data sources.

**Code:**
```python
from datetime import UTC, datetime, timedelta

cut = datetime.now(UTC) - timedelta(days=7)
docs = vectorstore.similarity_search(
    q, k=10, filter={"updated_at": {"$gte": cut.isoformat()}})   # only fresh docs
```

## Q75: How do you handle duplicate documents in RAG?
**A:** Deduplication techniques include exact hash matching (MD5, SHA), near-duplicate detection (MinHash, SimHash), embedding similarity thresholding, and content-based deduplication. Deduplication reduces storage and prevents redundant retrieval.

**Code:**
```python
import hashlib

def dedupe(docs):
    seen, uniq = set(), []
    for d in docs:
        h = hashlib.md5(d.page_content.encode()).hexdigest()   # exact-match hash
        if h not in seen:
            seen.add(h); uniq.append(d)
        # MinHash / SimHash for near-duplicates; embedding distance for thresholding
    return uniq
```

## Q76: What is a RAG cache?
**A:** A RAG cache stores frequently retrieved results and generated responses. Levels include query cache (same query to cached response), embedding cache (same query to cached embedding), document cache (frequently retrieved docs), and partial cache.

**Code:**
```python
from redis import Redis

r = Redis()

def cached_rag(q):
    if (hit := r.get(f"rag:{q}")):           # query -> response cache
        return hit
    answer = llm.invoke(f"Context: {retriever.invoke(q)}\nQ: {q}")
    r.setex(f"rag:{q}", 300, answer)         # TTL invalidates on KB updates
    return answer
```

## Q77: What is streaming in RAG?
**A:** Streaming in RAG sends the response token-by-token as the LLM generates it. The UI can show retrieved documents first, then stream the generated answer. This improves perceived latency and user experience.

**Code:**
```python
def stream(q):
    sources = retriever.invoke(q)
    yield {"type": "sources", "documents": sources}        # show docs first
    for token in llm.stream(f"Context: {sources}\nQ: {q}"):  # then stream tokens
        yield {"type": "token", "content": token}
```

## Q78: What are citations in RAG?
**A:** Citations reference the specific source passages used to generate each part of the response. They enable fact-checking and build trust. Implementation includes source IDs in retrieved context and instructing the LLM to cite sources inline.

**Code:**
```python
ctx = "\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, 1))
answer = llm.invoke(f"Answer with inline citations [n]:\n{ctx}\nQuestion: {q}")
```

## Q79: How do you implement citations in RAG?
**A:** Assign unique IDs to each retrieved chunk, include IDs in the prompt context, instruct the model to reference IDs, and post-process to extract citations. Verify that cited content actually supports the associated claims.

**Code:**
```python
import re

ctx = "\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, 1))
resp = llm.invoke(f"Cite each fact with [n].\n{ctx}\nQuestion: {q}")
cited = set(map(int, re.findall(r"\[(\d+)\]", resp)))
assert cited <= set(range(1, len(docs) + 1))       # verify every citation exists
```

## Q80: What is RAG with conversational memory?
**A:** Conversational RAG maintains conversation history and uses it for context-aware retrieval. The system may reformulate follow-up questions using history, retrieve based on conversation context, and use previous retrievals to inform current retrieval.

**Code:**
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
condensed = llm.invoke(
    f"History: {memory.load_memory_variables({})}\nRewrite standalone: {new_q}")
docs = retriever.invoke(condensed)                # retrieve with conversational context
answer = llm.invoke(f"Context: {docs}\nQ: {new_q}")
memory.save_context({"input": new_q}, {"output": answer})
```

## Q81: How do you handle follow-up questions in RAG?
**A:** Use conversation history to contextualize follow-up queries. Techniques include rewriting the query incorporating context, retrieving based on the full conversation, and filtering results using session context.

**Code:**
```python
def answer_follow_up(new_q, history):
    standalone = rewrite_with_history(new_q, history)   # "Make this standalone: ..."
    docs = retriever.invoke(standalone)
    return llm.invoke(f"Context: {docs}\nQuestion: {new_q}")
```

## Q82: What are common failure modes in RAG?
**A:** Common failures include irrelevant retrieval (returning unrelated documents), incomplete retrieval (missing necessary information), lost in the middle (LLM ignores relevant context), hallucination (LLM ignores context), and citation errors.

**Code:**
```python
def debug_failure(q):
    hits = retriever.invoke(q)
    assert hits, "empty retrieval"                     # irrelevant / nothing found
    answer = llm.invoke(f"Context: {hits}\nQ: {q}")
    assert grounded(answer, hits), "hallucination"     # answer must cite context
    assert citations_valid(answer), "citation error"
```

## Q83: How do you debug a RAG system?
**A:** Debug by examining each component: inspect retrieved documents for relevance, check embedding quality, evaluate prompt construction, analyze LLM response for context usage, and test with known-answer queries.

**Code:**
```python
def debug_rag(q):
    hits = retriever.invoke(q)         # 1 retrieval: relevant?
    qv = embeddings.embed_query(q)     # 2 embedding quality / dimensions
    print("prompt:", build_prompt(q, hits))   # 3 prompt construction
    answer = llm.invoke(prompt)        # 4 response uses context?
    return answer                      # 5 compare against known-answer set
```

## Q84: What tools and frameworks are available for building RAG systems?
**A:** Popular frameworks include LangChain, LlamaIndex, Haystack, RAGatouille, and Canopy (by Pinecone). They provide document loaders, splitters, embedding integrations, vector store connectors, and retrieval pipelines.

**Code:**
```python
# LangChain: loaders, splitters, embeddings, vector stores, chains.
# LlamaIndex: data-aware indexes + query engines.
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(docs)     # connectors, chunking, embedding
answer = index.as_query_engine().query(question)  # retrieval + synthesis
```

## Q85: What is LangChain's role in RAG?
**A:** LangChain provides document loaders (50+ formats), text splitters, embedding wrappers, vector store integrations, retrieval chains (stuff, map-reduce, refine), and LCEL for composing RAG pipelines.

**Code:**
```python
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(llm, retriever=store.as_retriever(),
                                 chain_type="stuff")   # loaders, splitters, chains
answer = qa.invoke("What is HNSW?")
```

## Q86: What is LlamaIndex's role in RAG?
**A:** LlamaIndex specializes in data indexing and retrieval for RAG. It provides data connectors (160+ sources), advanced indexing strategies (tree, keyword, vector, hybrid), query engines, and routing.

**Code:**
```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

docs = SimpleDirectoryReader("knowledge").load_data()   # 160+ connectors
index = VectorStoreIndex.from_documents(docs)           # advanced indexing
resp = index.as_query_engine(similarity_top_k=3).query("What is chunking?")
```

## Q87: What is Haystack in RAG?
**A:** Haystack is an open-source framework for RAG pipelines. It provides components (Embedder, Retriever, Reader/Generator), document stores (Elasticsearch, Weaviate, Pinecone), and pipeline orchestration.

**Code:**
```python
from haystack import Pipeline

p = Pipeline()
p.add_component("retriever", retriever)      # e.g. InMemoryEmbeddingRetriever
p.add_component("prompt", prompt_template)
p.add_component("llm", generator)
p.connect("retriever.documents", "prompt.documents")
p.connect("prompt", "llm")
p.run({"retriever": {"query": question}})
```

## Q88: What is the difference between RAG and search engines?
**A:** Search engines return ranked lists of documents. RAG retrieves documents AND generates a synthesized answer. RAG provides direct answers with citations; search engines require users to browse results.

**Code:**
```python
results = retriever.invoke(q)                              # search: ranked doc list
answer = llm.invoke(f"Context: {results}\nAnswer: {q}")    # RAG: synthesized answer
```

## Q89: How do you choose between RAG and fine-tuning?
**A:** Choose RAG when: data changes frequently, you need source citations, or you need access control. Choose fine-tuning when: you need to teach new skills/formats, you have stable data patterns, or latency is critical.

**Code:**
```python
def choose(data_change_days, needs_citations, skills_to_teach, latency_ms):
    if data_change_days < 30 or needs_citations:
        return "RAG"
    if skills_to_teach or latency_ms < 100:
        return "fine-tune"
    return "hybrid"
```

## Q90: Can RAG and fine-tuning be combined?
**A:** Yes. Fine-tune an LLM on domain-specific instructions, then use RAG to provide current knowledge. The fine-tuned model better understands how to use retrieved context. This hybrid approach often outperforms either method alone.

**Code:**
```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("fine-tuned-base")  # teaches domain skills
answer = model.generate(f"Context: {retriever.invoke(q)}\nQ: {q}",  # RAG supplies facts
                        max_new_tokens=200)
```

## Q91: What is RAG for code generation?
**A:** Code RAG retrieves relevant code snippets, documentation, and examples from a codebase to augment code generation. It is used for repository-level code completion, API usage generation, and code Q&A.

**Code:**
```python
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter.from_language(Language.PYTHON, chunk_size=200)
chunks = splitter.split_text(open("agent.py").read())     # split by function/class
docs = vectorstore.similarity_search("How are messages aggregated here?", k=3)
```

## Q92: What is RAG for enterprise search?
**A:** Enterprise RAG indexes internal documents (policies, wikis, product docs, emails) and provides a natural language interface. It must handle access control, data privacy, diverse formats, and high accuracy.

**Code:**
```python
def enterprise_rag(q, user):
    docs = vectorstore.similarity_search(
        q, k=5, filter={"acl": {"$in": user.roles}})      # access control at search time
    return llm.invoke(f"Internal context: {docs}\nQuestion: {q}")
```

## Q93: How do you handle access control in RAG?
**A:** Implement access control by tagging documents with permissions, filtering retrieved results by user roles, using metadata-based ACLs, and ensuring the LLM never exposes unauthorized information.

**Code:**
```python
def access_controlled_search(q, user):
    allowed = vectorstore.similarity_search(
        q, k=10, filter={"permission": {"$in": user.groups}})   # metadata ACL pre-filter
    return [d for d in allowed if user.can_read(d)]             # post-search defense-in-depth
```

## Q94: What is the cost of operating a RAG system?
**A:** Costs include embedding generation, vector database hosting, LLM inference (token costs), document processing, and monitoring. Optimization strategies include caching, smaller embedding models, and efficient indexing.

**Code:**
```python
def monthly_cost(emb_calls, tokens_in, tokens_out, per_call=0.0001):
    return (emb_calls * per_call
            + tokens_in / 1e6 * INPUT_PER_M
            + tokens_out / 1e6 * OUTPUT_PER_M)

print(monthly_cost(2_000_000, 500e6, 100e6))   # cache + smaller models reduce this
```

## Q95: What are emerging trends in RAG?
**A:** Trends include Agentic RAG (autonomous retrieval agents), Long-context RAG (models with 1M+ context windows), Graph RAG (knowledge graph integration), Multi-modal RAG, and Self-RAG.

**Code:**
```python
trends = {
    "agentic": create_react_agent(llm, tools=[retriever_tool, web_tool]),
    "long_context": llm.invoke(f"Context: {retriever.invoke(q, k=100)}\nQ: {q}"),
    "graph": graph_rag(q),
    "multimodal": clip_retriever(q),
}
```

## Q96: How does long-context affect RAG?
**A:** Very long context windows (Gemini 1.5 Pro, Claude 3.5, GPT-4-128k) allow processing more retrieved documents. This changes RAG design with less need for chunking but still faces lost-in-the-middle and cost challenges.

**Code:**
```python
context = "\n\n".join(d.page_content for d in retriever.invoke(q, k=100))  # 100 docs
answer = long_llm.invoke(f"Context:\n{context}\nQuestion: {q}")            # fits 1M-token window
```

## Q97: What is RAG quality assurance?
**A:** QA involves: testing with diverse queries, measuring retrieval metrics (precision, recall, MRR), evaluating generation quality (faithfulness, relevance), monitoring for drift, and setting up human evaluation pipelines.

**Code:**
```python
for q, expected in golden_set:
    hits = retriever.invoke(q)
    answer = llm.invoke(f"Context: {hits}\nQ: {q}")
    assert relevant(hits), "retrieval regression"
    assert faithfulness(answer, hits) > 0.9, "grounding regression"
    log_telemetry(q, hits, answer)      # monitor drift over time
```

## Q98: How do you optimize RAG latency?
**A:** Optimize by: using ANN indexes for fast retrieval, caching frequent queries, streaming responses, pre-computing embeddings, using smaller embedding models, parallelizing retrieval, and optimizing LLM inference with quantization or smaller models.

**Code:**
```python
import faiss

index = faiss.IndexHNSWFlat(dim, 32)      # ANN instead of exact scan
cache = {}                                 # pre-computed embeddings + query cache
def fast(q):
    if q in cache:
        return cache[q]
    out = llm.invoke(f"Context: {index.search(q_vec, k=3)}\nQ: {q}")
    cache[q] = out
    return out                              # + streaming for perceived latency
```

## Q99: What is the RAG document pipeline?
**A:** The document pipeline includes: document loading (from various sources), cleaning (remove noise, normalize text), chunking (split into appropriate pieces), embedding (convert to vectors), and indexing (store in vector database with metadata).

**Code:**
```python
def ingest(path):
    raw = loader.load(path)                    # 1 loading
    clean = clean_text(raw)                    # 2 cleaning/normalizing
    chunks = splitter.split_text(clean)        # 3 chunking
    embs = embedder.embed_documents(chunks)    # 4 embedding
    return index.add(embs, texts=chunks,       # 5 indexing + metadata
                     metadatas=[{"source": path}] * len(chunks))
```

## Q100: What is the future of RAG?
**A:** Future directions include: Agentic RAG with autonomous research capabilities, native long-context integration, multi-modal retrieval across text/image/video, self-improving RAG with feedback loops, and standardized RAG evaluation benchmarks.

**Code:**
```python
def agentic_rag_v2(q):
    agent = create_react_agent(llm, tools=[retriever_tool, search_tool,
                                           sql_tool, scratchpad_tool])
    return agent.invoke({"messages": [("user", q)]})   # multi-modal, self-improving, autonomous
```