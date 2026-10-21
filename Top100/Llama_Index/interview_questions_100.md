# LlamaIndex — 100 Interview Q&A
> Based on production RAG systems, data indexing, advanced retrieval patterns, and agentic AI using LlamaIndex v0.10+.

---

## 1. Core Concepts & Architecture (Q1–Q20)

**Q1: What is LlamaIndex and what problem does it solve?**
A: LlamaIndex is a data framework for building LLM applications over external data. It solves: 1) connecting LLMs to private/enterprise data (PDFs, databases, APIs), 2) data ingestion and indexing at scale, 3) advanced retrieval strategies (beyond naive vector search), 4) structured data extraction, and 5) agentic RAG with tool use. It specializes in the "R" of RAG — retrieval.

**Q2: Explain the core LlamaIndex abstractions: Documents, Nodes, Index, Retriever, and QueryEngine.**
A: 
- Document: a container for any data source (PDF, API, database) — has text + metadata
- Node: a chunk of a Document (after splitting); the atomic unit for embedding and retrieval
- Index: a data structure that organizes Nodes for fast retrieval (VectorStoreIndex, SummaryIndex, KeywordTableIndex)
- Retriever: extracts relevant Nodes from an Index given a query
- QueryEngine: combines Retriever + LLM + Response Synthesis into an end-to-end query interface

**Q3: What is the difference between Document and Node in LlamaIndex?**
A: Document is the raw input — a file, webpage, or API response. Node is a processed chunk (after parsing/splitting). A Document produces multiple Nodes. Nodes store: text, metadata, embedding (optional), and relationships to other Nodes. Retrieval works on Nodes, not Documents. You can reconstruct Documents from their Nodes via parent relationships.

**Q4: Explain the role of "index structures" in LlamaIndex.**
A: Index structures determine how Nodes are organized for retrieval:
- VectorStoreIndex: default — embed all nodes, store in vector DB, search by similarity
- SummaryIndex: stores nodes as sequential list — useful for summarization (process all nodes)
- KeywordTableIndex: extracts keywords per node, builds keyword→node mapping — fast for keyword queries
- TreeIndex: builds a hierarchical tree of summaries — useful for summarization over large corpora
- PropertyGraphIndex: builds a knowledge graph from nodes for graph-based retrieval

**Q5: What is a "retriever" and how does it differ from a "query engine"?**
A: Retriever: fetches relevant nodes from an index. Returns `NodeWithScore[]`. Does NOT call an LLM. QueryEngine: wraps retriever + optional LLM steps (synthesis, reranking). Returns a RESPONSE (string or structured). Retriever is a component of QueryEngine. You can use retrievers standalone for embedding + search without generation.

**Q6: How does LlamaIndex's "response synthesis" work?**
A: Response synthesis takes retrieved nodes and generates an answer. Modes:
- `refine`: generate answer with first node → refine with each subsequent node (sequential, good for accumulation)
- `compact`: concatenate nodes into as few LLM calls as possible (respects context window)
- `tree_summarize`: recursively summarize groups of nodes into a tree
- `accumulate`: generate answer per node, then concatenate
- `no_text`: return retrieved nodes directly without LLM
- `simple`: single-shot with all context

**Q7: What is the "query pipeline" in LlamaIndex?**
A: QueryPipeline is LlamaIndex's equivalent of LangChain LCEL — a DAG of modules (retrievers, prompts, LLMs, parsers) composed via `|` operator. Supports branching, merging, cycles (via loop modules). More advanced than linear chains. Example: `pipeline = retriever | reranker | prompt | llm | parser`.

**Q8: Explain the difference between LlamaIndex and LangChain.**
A: LlamaIndex: data-centric — excels at data ingestion, indexing, retrieval strategies, structured data extraction. LangChain: orchestration-centric — excels at chains, agents, tools, and ecosystem integrations. LlamaIndex has deeper retrieval capabilities (advanced chunking, auto-retrieval, knowledge graphs). Many production apps use both: LlamaIndex for data pipeline, LangChain for agent orchestration.

**Q9: What is a "ServiceContext" in LlamaIndex (and why is it deprecated)?**
A: ServiceContext bundled LLM, embedding model, chunk size, and callback manager into one object. Deprecated in v0.10+ in favor of direct Settings: `Settings.llm`, `Settings.embed_model`, `Settings.chunk_size`, `Settings.callback_manager`. The Settings singleton provides global defaults overridable per-call.

**Q10: How does LlamaIndex's Settings work?**
A: Settings is a global configuration object:
```python
from llama_index.core import Settings
Settings.llm = OpenAI(model="gpt-4o", temperature=0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.chunk_size = 512
Settings.chunk_overlap = 50
```
Available globally; individual components can override via constructor args (e.g., `index.as_retriever(similarity_top_k=5)`).

**Q11: What is the `Index` vs `Retriever` vs `QueryEngine` relationship in code?**
A: 
```python
index = VectorStoreIndex.from_documents(docs)      # Build index
retriever = index.as_retriever(similarity_top_k=5)  # Create retriever
query_engine = index.as_query_engine()              # Create query engine (retriever + synth)

# Usage:
nodes = retriever.retrieve("query")                 # Just retrieval
response = query_engine.query("query")              # Full RAG
```

**Q12: How does LlamaIndex handle streaming responses?**
A: Query engines support streaming via `query_engine.stream_query("query")` which yields response chunks as they're generated. The streaming is toggleable per-query-engine configuration. Streaming works with response synthesis modes (refine, compact, etc.). For async: `await query_engine.aquery("query")`.

**Q13: What is the `ComposableGraph` in LlamaIndex?**
A: ComposableGraph (advanced) connects multiple indexes together. For example: an index per document → a summary index of summaries → query traverses the graph. Allows hierarchical retrieval. Less used in modern LlamaIndex — QueryPipeline and sub-question query engines achieve similar goals more flexibly.

**Q14: How do "indices" compose with other indices?**
A: Via `QueryEngineTool` wrapping each index's query engine, then composing with a `RouterQueryEngine` or `SubQuestionQueryEngine`. This lets you query across multiple indexes in one query. The router decides which index to query; sub-question engine decomposes the query into sub-queries per index.

**Q15: What is a `ChatEngine` in LlamaIndex?**
A: ChatEngine extends QueryEngine with multi-turn conversation. Maintains chat history. Supports `chat()` and `achat()` methods. Modes:
- `simple`: context + history + LLM
- `condense_question`: rephrase query based on history + context
- `context`: retrieve context each turn
- `condense_plus_context`: condense query + retrieve context
Stateful: maintains message history per session.

**Q16: What are "callback managers" and how do they work in LlamaIndex?**
A: CallbackManager enables observability: tracking events (node parsing, embedding, retrieval, LLM call, synthesis). Global via `Settings.callback_manager`. Events fire start/end with metadata. Integrates with: LangTracer, Arize, Weights & Biases, custom handlers. Essential for debugging RAG pipelines.

**Q17: How does LlamaIndex handle LLM token counting and cost tracking?**
A: Via `TokenCountingCallback` or integration with LangTracer/LangSmith. Tracks: prompt tokens, completion tokens, total tokens per query. For OpenAI: uses tiktoken. Available via callback events. Cost estimation: multiply token counts by model-specific rates.

**Q18: What is the "dispatcher" in LlamaIndex?**
A: Dispatcher is a callback-based event system that broadcasts LlamaIndex events (chunking, embedding, retrieval, LLM call) to registered handlers. Used for: logging, tracing, debugging, custom instrumentation. Replaces older callback systems. Configured globally via `Settings` or per-component.

**Q19: How does LlamaIndex versioning work (v0.9 → v0.10+)?**
A: v0.10 was a major restructuring:
- `llama-index` → core + integration packages (`llama-index-core`, `llama-index-llms-openai`, `llama-index-embeddings-huggingface`)
- ServiceContext → Settings
- Simplification of index/retriever/query-engine interfaces
- More composable query pipelines
- Better streaming support
Breaking changes: import paths, ServiceContext removal, callback system rewrite.

**Q20: What is the `llama-index-core` vs integration packages architecture?**
A: `llama-index-core`: core abstractions (Document, Node, Index, Retriever, QueryEngine, Settings). Integration packages: `llama-index-llms-openai`, `llama-index-embeddings-huggingface`, `llama-index-vector-stores-pinecone`, etc. Install only what you need — keeps dependencies lean. Import from `llama_index.core` for core, `llama_index.llms.openai` for specific integrations.

## 2. Data Ingestion & Indexing (Q21–Q40)

**Q21: How does LlamaIndex ingest documents?**
A: Via `SimpleDirectoryReader` or format-specific readers:
```python
from llama_index.core import SimpleDirectoryReader
docs = SimpleDirectoryReader("./data").load_data()
```
Readers produce `Document[]`. Supported: PDF (PyMuPDF), HTML, Markdown, CSV, JSON, DOCX, images (with OCR), databases, Notion, Slack, GitHub, YouTube transcripts, Google Docs, etc.

**Q22: What are "node parsers" and how do they split documents?**
A: Node parsers determine chunking strategy:
- `SentenceSplitter`: splits by sentence boundaries (respects paragraph boundaries) — default
- `TokenTextSplitter`: splits by token count
- `SentenceWindowNodeParser`: keeps sentence + surrounding window — enables sentence-level retrieval with window context
- `SemanticSplitterNodeParser`: splits by semantic similarity of sentences (embedding-based)
- `MarkdownNodeParser`: splits by markdown headers
- `HierarchicalNodeParser`: creates parent/child node hierarchy

**Q23: Explain the "SentenceWindowNodeParser" and its advantages.**
A: Splits text into individual sentences as child nodes, but each child node includes a window of surrounding sentences as metadata. Retrieval: find relevant sentence via embedding → return the sentence + its window as context. Benefits: precise retrieval (sentence-level embedding is specific) with rich context (window provides surrounding meaning).

**Q24: What is "hierarchical node parsing"?**
A: `HierarchicalNodeParser` creates a tree: document → sections (level 1) → subsections (level 2) → paragraphs (level 3) → sentences (level 4). Each level is a node with parent/child relationships. Retrieval: search at leaf level → return parent nodes as context. This gives: precise retrieval (small leaf chunks) + meaningful context (larger parent chunks).

**Q25: How do you handle images and tables in document ingestion?**
A: 
- Images: `ImageReader` extracts text via OCR (pytesseract). For multi-modal RAG: store image embedding + text description.
- Tables: `PandasExcelReader` or `CSVReader`. `UnstructuredReader` extracts table structure. Embed both table-as-text and table-as-description.
- `LLM RAG with tables`: convert table to text description before embedding, or use table-aware retrievers.
- LlamaIndex supports multi-modal nodes (text + image in same node).

**Q26: What is "LlamaParse" and how does it improve document parsing?**
A: LlamaParse is LlamaIndex's managed document parser. Handles: complex layouts, tables, headers/footers, images-with-captions, multi-column layouts. Uses LLM to understand document structure. Better than open-source parsers for complex PDFs (research papers, financial reports, legal docs). Pay-per-page. Integrates with `LlamaParseReader`.

**Q27: How does metadata extraction work in LlamaIndex?**
A: `MetadataExtractor` enriches nodes during ingestion:
```python
from llama_index.core.extractors import (
    TitleExtractor, SummaryExtractor, KeywordExtractor
)
extractors = [TitleExtractor(), SummaryExtractor(), KeywordExtractor()]
node_parser = SentenceSplitter()
nodes = node_parser.get_nodes_from_documents(docs)
for node in nodes:
    for extractor in extractors:
        extractor.extract(node)
```
Adds metadata (title, summary, keywords) to nodes — improves retrieval by allowing metadata filtering.

**Q28: What is "metadata filtering" and how does it improve retrieval?**
A: Metadata filtering narrows search to relevant nodes before or after vector search:
```python
retriever = index.as_retriever(
    filters=MetadataFilters(
        filters=[ExactMatchFilter(key="category", value="finance")]
    )
)
```
Filters: ExactMatch, KeywordMatch, NumericComparison, DateComparison. Enables: date-range queries, category-based retrieval, access control.

**Q29: How do you ingest from a database into LlamaIndex?**
A: 
```python
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

sql_database = SQLDatabase.from_uri("postgresql://...")
query_engine = NltSQLTableQueryEngine(sql_database=sql_database)
response = query_engine.query("What were total sales in 2024?")
```
Two approaches: 1) Text-to-SQL (LLM generates SQL from natural language), 2) DatabaseReader (convert tables to documents for vector search). `NLSQLTableQueryEngine` combines both.

**Q30: What is "indexing at scale" strategy in LlamaIndex?**
A: 
1. Streaming ingestion: `SimpleDirectoryReader` with `lazy_load()` → process in batches
2. Parallel embedding: use `embed_model.aget_text_embedding_batch()` for concurrency
3. Batching: `index.insert_nodes(nodes)` in batches (e.g., 100 at a time)
4. Vector store with batching support (Pinecone, Qdrant batch APIs)
5. For millions of docs: use LlamaIndex's `IngestionPipeline` with vector store as destination
6. Monitor: use callbacks to track throughput and errors

**Q31: What is an `IngestionPipeline`?**
A: IngestionPipeline is a modular pipeline for document processing:
```python
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512),
        TitleExtractor(),
        embedding_model,
    ],
    vector_store=vector_store
)
pipeline.run(documents=docs)
```
Supports caching (skip unchanged documents), incremental updates, parallel processing. The standard approach for production ingestion.

**Q32: How does LlamaIndex handle incremental indexing (updates only)?**
A: Via `DocStoreStrategy` in IngestionPipeline:
- `Upsert`: insert new, update existing, delete removed
- `UpsertsAndDelete`: same but explicitly removes deleted docs
- `DuplicateOnly`: skip duplicates
Uses document hashing and caching to avoid re-embedding unchanged documents. Requires a `docstore` (in-memory, MongoDB, Redis) to track document state.

**Q33: What is the "document store" (docstore) in LlamaIndex?**
A: Docstore tracks which documents/nodes have been indexed. `SimpleDocumentStore` (in-memory), `MongoDBDocumentStore`, `RedisDocumentStore`. Used by IngestionPipeline for incremental indexing. Stores: doc_id, node_id, hash, metadata, ref_doc_id. Enables: skip unchanged docs, delete removed docs, track provenance.

**Q34: How does LlamaIndex handle chunk overlap?**
A: `chunk_overlap` parameter in text splitters. E.g., `SentenceSplitter(chunk_size=512, chunk_overlap=50)`. Overlap ensures context isn't lost at chunk boundaries — chunks share a few sentences of overlap. Important for: entities or concepts that span chunk boundaries. Too much overlap increases token count; too little may miss context.

**Q35: What is the recommended chunk_size for different use cases?**
A: 
- Q&A / precise retrieval: 128-256 tokens (smaller = more precise)
- Summarization: 512-1024 tokens (larger = more context)
- Document-wide queries: 1024+ tokens
- With reranking: smaller chunks (128-256) + reranker on top for best results
- Embedding model matters: ada-002 (1536 dim) works well with 256-512 tokens; BGE-small (384 dim) with 128-256
- Rule of thumb: start with 512, benchmark recall, adjust

**Q36: What are "structured" vs "unstructured" data handling in LlamaIndex?**
A: Unstructured (text, PDF, HTML): document readers → node parsers → embeddings → vector store. Structured (SQL, CSV, API): can be converted to natural language and indexed as documents, or queried via Text-to-SQL. LlamaIndex provides both approaches and can combine structured + unstructured in a single query engine.

**Q37: How do you handle large PDF documents (100+ pages)?**
A: 
1. Use `LlamaParse` for reliable structure extraction
2. Chunk with markdown-aware parser (preserve section hierarchy)
3. Use hierarchical node parsing (retrieve section-level context)
4. Consider "summary index" for document overview + "vector index" for specific content
5. Use parent document retriever: small chunks for search, large context for LLM
6. For 500+ page docs: embed chapter summaries + detailed per-section nodes

**Q38: What is the "RouterQueryEngine" and how does it differ from "SubQuestionQueryEngine"?**
A: RouterQueryEngine: LLM chooses ONE tool/query engine to answer the query (fast, focused). SubQuestionQueryEngine: decomposes query into sub-questions, sends each to potentially different query engines, then synthesizes answers (comprehensive, multi-source). Router is faster; SubQuestion is more thorough.

**Q39: How do you handle multi-lingual documents in LlamaIndex?**
A: 
- Embedding models: use multilingual models (multilingual-e5-large, BGE-m3, Cohere multilingual)
- Translation: pre-translate documents to English before indexing (add original as metadata)
- Language detection: add language tag as metadata for filtering
- Mixed-language collections: multilingual embedding model handles code-switching

**Q40: What are "Document Management" best practices in LlamaIndex?**
A: 
- Track document source, version, ingestion timestamp in metadata
- Use IngestionPipeline with DocStore for incremental updates
- Periodically re-index if embedding model changes
- Monitor embedding quality: find low-confidence queries, analyze failure modes
- Backup vector store + doc store
- Tag documents by domain, department, access level for security filtering

## 3. Retrieval Strategies (Q41–Q60)

**Q41: What is the default retrieval strategy in LlamaIndex and how do you customize it?**
A: Default: top-k vector similarity search using the index's embedding model. Customizations: `index.as_retriever(similarity_top_k=10)`, change to MMR mode (`vector_store_query_mode="mmr"`), add metadata filters, use hybrid search. For advanced: use `RetrieverQueryEngine` with custom retriever classes.

**Q42: Explain the different retrieval modes in LlamaIndex.**
A: 
- `similarity`: top-k by vector distance
- `mmr`: maximum marginal relevance — balance relevance + diversity
- `sparse`: keyword-based retrieval (BM25)
- `hybrid`: combination of dense + sparse (e.g., weighted sum)
- `auto`: let the retriever decide based on query
- Each mode configurable via `vector_store_query_mode` parameter

**Q43: What is "MMR retrieval" and when should you use it?**
A: MMR retrieves a diverse set of results — it penalizes results that are too similar to already-selected results. Parameters: `mmr_threshold` (balance between relevance and diversity, 0-1). Use when: you want to avoid redundant context, cover multiple perspectives, or when top-k results are all very similar.

**Q44: How does "hybrid search" work in LlamaIndex?**
A: Combines dense (vector embedding) and sparse (BM25/keyword) retrieval. Results are merged via reciprocal rank fusion (RRF) or weighted scoring. High-level: capture both semantic meaning (dense) and exact keyword matches (sparse). Essential for: domain-specific terminology, proper nouns, exact phrase matching.

**Q45: What is "auto-retrieval" in LlamaIndex?**
A: Auto-retrieval enables natural language querying with automatic metadata filtering. The LLM extracts structured filters from the query:
`"Show me finance articles from 2024"` → `{"query": "finance articles", "filters": {"category": "finance", "year": 2024}}`
Implemented via: `VectorIndexAutoRetriever`. Uses the LLM to decide both the search query AND the metadata filters.

**Q46: What is "recursive retrieval" in LlamaIndex?**
A: Recursive retrieval: retrieve → maybe retrieve more based on results. Patterns:
- Retrieve nodes → check if context is sufficient → if not, retrieve more
- Retrieve references from retrieved nodes (link following)
- Retrieve parent nodes of retrieved child nodes (hierarchical)
- Multi-step: retrieve initial set, then use them to generate better queries
Implemented via `RecursiveRetriever`.

**Q47: What is the "Reranking" process and which rerankers does LlamaIndex support?**
A: Reranking: after initial retrieval (fast ANN), apply a cross-encoder to score and reorder top-k results. LlamaIndex supports:
- `CohereRerank`: API-based, good general purpose
- `CrossEncoderRerank`: local (sentence-transformers cross-encoders), e.g., BAAI/bge-reranker-large
- `LLMRerank`: use LLM to score relevance
- `SentenceTransformerRerank`: lightweight, fast
The reranker is inserted in the query pipeline between retriever and response synthesis.

**Q48: How does "Response Synthesis" mode affect retrieval?**
A: Different modes change how retrieved nodes are consumed:
- `refine`: sequential — can handle many nodes but slow
- `compact`: concatenate to fit context — fewer LLM calls, needs larger context
- `tree_summarize`: parallel — good for many nodes, higher quality
- `accumulate`: per-node LLM calls + concatenation — preserves detail
- `no_text`: no LLM — just return retrieved chunks
Choose based on: latency budget, context window size, quality requirements.

**Q49: What is a "sub-question query engine"?**
A: SubQuestionQueryEngine decomposes a complex query into simpler sub-questions, answers each by querying a specific tool/query engine, then synthesizes the final answer:
```
Query: "Compare Q4 2024 revenue with Q4 2023"
→ SubQ1: "What was Q4 2024 revenue?" → query finance tool
→ SubQ2: "What was Q4 2023 revenue?" → query finance tool
→ Synthesize comparison
```
Implemented via `SubQuestionQueryEngine`. Each sub-question can target a different index.

**Q50: What is a "router query engine"?**
A: RouterQueryEngine selects the best query engine from a set:
```python
router = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(),
    query_engine_tools=[
        QueryEngineTool.from_defaults(finance_engine, description="Good for finance questions"),
        QueryEngineTool.from_defaults(hr_engine, description="Good for HR questions"),
    ]
)
```
The selector (LLM-based) picks the single best tool based on tool descriptions. For multi-tool: `SubQuestionQueryEngine`.

**Q51: How does "retrieval with feedback" work?**
A: Pattern: retrieve → generate → evaluate → refine. Steps:
1. Retrieve top-k nodes
2. Generate answer
3. Evaluate answer quality (faithfulness, completeness)
4. If insufficient: retrieve additional nodes, adjust query, or re-retrieve
5. Repeat until quality threshold met
LlamaIndex doesn't have this built-in but can be implemented via QueryPipeline with conditional branching.

**Q52: What is "multi-step query decomposition"?**
A: Breaks complex queries into steps that depend on each other:
```
Query: "What was the revenue growth rate last year?"
→ Step 1: "What was revenue last year?"
→ Step 2: "What was revenue the year before?"
→ Step 3: "Calculate growth rate: (rev_last - rev_previous) / rev_previous"
```
Each step can query different indexes or use different tools. Implemented via `MultiStepQueryEngine`.

**Q53: How do you handle retrieval from multiple data sources with different schemas?**
A: 
1. Create separate indexes per data source
2. Wrap each index as a QueryEngineTool
3. Use RouterQueryEngine or SubQuestionQueryEngine to route/decompose queries
4. Each tool's description tells the LLM what data it contains
5. Results from multiple tools are synthesized
This enables unified querying across PDFs, databases, APIs, and web pages.

**Q54: What is "BM25 retrieval" and when would you use it instead of vector search?**
A: BM25 is a keyword-based ranking function (TF-IDF variant). Better than vector search for: exact term matching, domain-specific jargon (where embeddings fail), proper names, code snippets. LlamaIndex provides `BM25Retriever` that indexes tokens for keyword search. Often combined with vector search in hybrid mode.

**Q55: How does the "auto-merging retriever" work?**
A: AutoMergingRetriever retrieves leaf nodes (small chunks) and automatically merges them with their parent nodes if enough children from the same parent are retrieved. Reduces context fragmentation. Implemented with HierarchicalNodeParser. Benefits: LLM gets coherent, larger context instead of scattered small chunks.

**Q56: What is "pydantic program" for structured extraction from retrieved data?**
A: PydanticProgram uses an LLM to extract structured data from retrieved nodes into a Pydantic model:
```python
class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str

program = PydanticProgram.from_defaults(PersonInfo, llm=llm)
result = program(query="Find person info", retrieved_nodes=nodes)
```
Powerful for: entity extraction, structured output from unstructured text, form filling from documents.

**Q57: How do you implement "contextual retrieval" (adding surrounding context before embedding)?**
A: 
1. Split documents into chunks
2. For each chunk, prepend a summary of the document/section it belongs to
3. Embed the enriched text
4. At query time, search by enriched embeddings
5. Return the original chunk content (without the prepended context)
Benefit: embedding captures context, not just isolated chunk. Implemented via custom node parser or transformation.

**Q58: What are "vector store filters" vs "metadata filters"?**
A: Vector store filters: passed directly to the vector DB as part of the search query (pre-filtering). Metadata filters: applied by LlamaIndex after retrieval (post-filtering). Pre-filtering is more efficient for selective filters; post-filtering can return fewer results if the filter is too restrictive. Most vector stores support pre-filtering natively.

**Q59: How does "Retriever" work with streaming?**
A: Retrievers don't stream (they return nodes synchronously). Streaming happens at the QueryEngine/LLM level. To stream in a RAG app:
1. Retrieve all nodes (blocking)
2. Stream LLM tokens as the response is generated
3. Use `query_engine.stream_query()` for end-to-end streaming
For full streaming (including retrieval progress): use events via callback manager to show "Retrieving..." status on frontend.

**Q60: What is the "zero-shot retrieval" capability?**
A: The ability to retrieve relevant information without any domain-specific fine-tuning of the embedding model. LlamaIndex achieves this via: strong pre-trained embeddings (BGE, E5, ada-002), good chunking strategies, and effective reranking. Zero-shot retrieval quality depends on: embedding model quality, chunk size/overlap strategy, and whether hybrid search is used.

## 4. Agents & Tool Use (Q61–Q75)

**Q61: How does LlamaIndex implement agents?**
A: LlamaIndex's agent system (separate from LangGraph) provides:
- `AgentRunner`: main agent loop, manages state, calls LLM, executes tools
- `AgentWorker`: defines agent behavior (ReAct, function calling, multi-step)
- `QueryTool`: wraps a query engine as a tool for the agent
- Tools: `QueryEngineTool`, `FunctionTool`, `QueryTool`, custom tools
- Supports: streaming, chat history, parallel tool execution

**Q62: What is the difference between LlamaIndex agents and LangChain/LangGraph agents?**
A: LlamaIndex agents are QueryEngine-centric — they naturally query indexes as tools. Strong integration with LlamaIndex's data/retrieval stack. LangChain/LangGraph agents are general-purpose — broader tool ecosystem. LlamaIndex agents are simpler to set up for RAG-focused agent tasks. For complex multi-agent orchestration, LangGraph is more powerful.

**Q63: How do you create an agent with QueryEngineTools?**
A: 
```python
from llama_index.core.agent import AgentRunner
from llama_index.core.tools import QueryEngineTool

tools = [
    QueryEngineTool.from_defaults(
        finance_engine,
        name="finance_tool",
        description="Useful for finance and revenue questions"
    ),
    QueryEngineTool.from_defaults(
        hr_engine,
        name="hr_tool",
        description="Useful for HR policy and employee questions"
    )
]
agent = AgentRunner.from_tools(tools, llm=llm, verbose=True)
response = agent.chat("What's the revenue for Q4 and the company holiday policy?")
```
The agent decides which tools to call and in what order.

**Q64: What is `FunctionTool` in LlamaIndex?**
A: FunctionTool wraps any Python function as a tool:
```python
from llama_index.core.tools import FunctionTool

def calculate_growth(current: float, previous: float) -> float:
    """Calculate growth rate between two values."""
    return (current - previous) / previous * 100

tool = FunctionTool.from_defaults(calculate_growth)
```
The docstring + parameter types become the tool description for the LLM.

**Q65: What agent types (workers) does LlamaIndex support?**
A: 
- `ReActAgentWorker`: ReAct pattern (thought → action → observation)
- `FunctionCallingAgentWorker`: for models with native tool calling (OpenAI, Anthropic, Gemini)
- `MultimodalAgentWorker`: for multi-modal LLMs (vision + text tools)
- `CustomAgentWorker`: extend for custom behavior
- `ParallelAgentWorker`: executes multiple tool calls in parallel
Configure via `AgentRunner.from_tools(worker_type=...)` or explicit worker construction.

**Q66: How does LlamaIndex handle tool call streaming?**
A: Agents support streaming:
```python
response = agent.stream_chat("Query here")
for chunk in response.response_gen:
    print(chunk, end="")
```
`stream_chat` returns a generator for response tokens. Tool calls in the middle are executed synchronously; streaming resumes after each tool call. For full streaming (including intermediate steps): use `agent.runner.stream_events()`.

**Q67: What is a "tool" vs "query tool" in LlamaIndex?**
A: Tool (`FunctionTool`): arbitrary function (calculator, API call, database query). QueryTool (`QueryEngineTool`): wraps a QueryEngine — the tool uses the engine's retrieval + synthesis to answer. QueryTool is the primary way to give agents access to indexed data.

**Q68: How does LlamaIndex handle agent state and memory?**
A: AgentRunner maintains chat history (messages list). Supports:
- `reset()`: clear history
- Prefix memory: add system messages
- Custom memory modules
- For persistent memory across sessions: store messages externally, rehydrate
Agent state is NOT as sophisticated as LangGraph — no checkpointing, no subgraph state isolation.

**Q69: What is a "multi-agent system" in LlamaIndex?**
A: Top-level agent delegates to sub-agents:
```python
from llama_index.core.agent import AgentRunner
from llama_index.core.tools import QueryEngineTool

writer_agent = AgentRunner.from_tools([write_tool])
reviewer_agent = AgentRunner.from_tools([review_tool])
supervisor = AgentRunner.from_tools([
    QueryEngineTool.from_defaults(writer_agent, name="writer"),
    QueryEngineTool.from_defaults(reviewer_agent, name="reviewer"),
])
```
Sub-agents are wrapped as QueryEngineTools. Simpler than LangGraph's multi-agent — no graph-based orchestration.

**Q70: How do you handle "agentic RAG" in LlamaIndex?**
A: An agent with RAG tools:
```python
rag_tool = QueryEngineTool.from_defaults(query_engine)
search_tool = FunctionTool.from_defaults(web_search)
calculator = FunctionTool.from_defaults(calculate)
agent = AgentRunner.from_tools([rag_tool, search_tool, calculator])
```
The agent decides: when to RAG, when to use other tools, how to combine results. More flexible than fixed RAG pipeline.

**Q71: What is "parallel tool execution" in LlamaIndex agents?**
A: If the LLM returns multiple tool_calls in one response (supported by OpenAI, Anthropic tool calling agents), LlamaIndex executes them concurrently. Implementation: `FunctionCallingAgentWorker` with `parallel_tool_calls=True` (default). Improves latency for independent sub-tasks.

**Q72: How do you handle agent errors (invalid tool calls, tool failures)?**
A: 
- Invalid tool call: agent receives error message as observation → retry or apologize
- Tool execution error: exception caught → error sent as observation
- Max iterations: `max_iterations` parameter (default 10)
- `verbose=True`: prints agent's reasoning for debugging
- For reliability: provide clear tool names, descriptions, and parameter schemas

**Q73: How does LlamaIndex integrate with LangChain/LangGraph?**
A: 
- LlamaIndex query engines can be wrapped as LangChain tools (and vice versa)
- Use `LlamaIndexTool` in LangChain to call LlamaIndex query engines from LangChain agents
- Use `LangChainTool` in LlamaIndex to call LangChain chains
- Best practice: LlamaIndex for data/retrieval, LangGraph for orchestration — both in the same app
- LlamaIndex's `QueryEngineTool` can be passed to LangGraph agents

**Q74: What are "workflow" agents in LlamaIndex?**
A: Workflow is LlamaIndex's graph-based orchestration (similar to LangGraph). A Workflow consists of `Steps` connected by events. Steps are functions decorated with `@step` that listen for events and emit events. Enables: cycles, branching, parallel steps, human-in-the-loop. State management via event passing. Supports: `ctx.send_event()`, `ctx.collect_events()`. Introduced in LlamaIndex v0.10+.

**Q75: Compare LlamaIndex Workflows vs LangGraph.**
A: LlamaIndex Workflows: event-driven, step orchestration, lighter weight, less mature. LangGraph: state machine with checkpointing, more production features (persistence, interrupts, time travel). Choose LangGraph for complex, stateful, production agent systems. Choose LlamaIndex Workflows for simpler agent workflows within the LlamaIndex ecosystem.

## 5. Advanced LlamaIndex Features (Q76–Q90)

**Q76: What is a "PropertyGraphIndex" in LlamaIndex?**
A: PropertyGraphIndex extracts entities and relationships from documents to build a knowledge graph. Nodes are entities (with properties), edges are relationships. Retrieval: traverse graph to find relevant entities and their relationships. Good for: multi-hop questions, relational reasoning, domain-specific knowledge that benefits from graph structure. Uses LLM to extract triples (subject-predicate-object).

**Q77: How does "knowledge graph indexing" differ from vector indexing?**
A: Vector index: documents → chunks → embeddings → similarity search. Knowledge graph: documents → entities + relationships → graph DB → traverse/query. Vector search finds "semantically similar" content. Graph search finds "related" content via explicit relationships. Best: both — vector for initial retrieval, graph for relationship-based expansion.

**Q78: What is "structured data extraction" in LlamaIndex?**
A: Using LLM to extract structured information from unstructured text:
```python
from llama_index.core.extractors import PydanticProgramExtractor
from llama_index.core.program import LLMTextCompletionProgram

class Invoice(BaseModel):
    invoice_number: str
    date: str
    total_amount: float
    vendor: str

program = LLMTextCompletionProgram.from_defaults(
    output_cls=Invoice,
    prompt=extraction_prompt,
    llm=llm
)
result = program(text=invoice_text)
```
Returns a Pydantic model with extracted fields.

**Q79: What is the "llama-index-experimental" package?**
A: Contains bleeding-edge features: `Guidance` integration, `StructuredGeneration` tools, experimental agents, and new index types. Not production-stable. Used for: evaluating new features before they graduate to core. Import: `from llama_index.experimental import ...`.

**Q80: What is "data agents" and how do they differ from regular agents?**
A: Data Agents (or "data agent tools") are agents specialized for data tasks: SQL queries, pandas analysis, Python REPL. LlamaIndex provides: `PandasQueryEngine`, `NLSQLTableQueryEngine`, `PythonTool`. These agents generate and execute code to answer data questions. More capable than simple retrieval for analytical queries.

**Q81: How does LlamaIndex support GraphRAG?**
A: GraphRAG combines knowledge graphs with RAG:
1. Build PropertyGraphIndex from documents
2. On query: retrieve relevant entities via embedding + graph traversal
3. Extract subgraph around those entities
4. Present subgraph as structured context to LLM
5. LLM uses relationships for multi-hop reasoning
LlamaIndex supports this via `PropertyGraphIndex` + `GraphRAGQueryEngine`. Better than naive RAG for relational queries.

**Q82: What is the "LLamaIndex Pydantic Program" for output structuring?**
A: Pydantic Program forces LLM to output structured data matching a Pydantic schema. Two modes:
- `LLMTextCompletionProgram`: textual prompt asking for structured output
- `LLMCompletionProgram`: for function-calling models (more reliable)
Used for: extraction, classification, structured generation, form filling.

**Q83: How do you implement "multi-modal RAG" in LlamaIndex?**
A: 
1. Use `MultiModalLLM` (GPT-4V, Gemini Pro Vision, Claude 3)
2. Index images + text in the same index
3. Use `MultiModalVectorIndex` to embed both modalities
4. Retrieve both text nodes and image nodes
5. Query engine returns text + image references
6. LLM sees both text context and images
Code: `index = MultiModalVectorIndex.from_documents(docs, embed_model=clip, llm=llm)`.

**Q84: What is "pandas query engine" in LlamaIndex?**
A: PandasQueryEngine converts natural language to pandas code:
```python
from llama_index.query_engine.pandas import PandasQueryEngine
engine = PandasQueryEngine(df=df, llm=llm)
response = engine.query("What is the average revenue by quarter?")
```
LLM generates pandas code, executes it, returns result. Great for data analysis over tabular data without writing SQL.

**Q85: How do you handle "time-sensitive retrieval" in LlamaIndex?**
A: 
- Metadata filtering: add timestamp to each node, filter by date range at query time
- Time-weighted decay: newer nodes get a relevance boost
- Time-aware splitting: split by time period for temporal queries
- Recency bias in retrieval: add recency score to similarity score
- LlamaIndex doesn't have built-in time decay, but can be implemented via custom retriever

**Q86: What is "evaluation" in LlamaIndex?**
A: LlamaIndex provides evaluation modules:
- `FaithfulnessEvaluator`: checks if response is supported by retrieved context
- `RelevancyEvaluator`: checks if retrieved context is relevant to query
- `CorrectnessEvaluator`: compares response to reference answer
- `SemanticSimilarityEvaluator`: embedding-based similarity between response and reference
- `PairwiseComparisonEvaluator`: compares two responses
- `BatchEvalRunner`: run multiple evaluators on a dataset

**Q87: How do you evaluate RAG quality with LlamaIndex?**
A: 
1. Create test dataset: queries + expected answers
2. Run your query engine against the dataset
3. Run evaluators (faithfulness, relevancy, correctness)
4. Aggregate scores
5. Compare against baselines (different chunk sizes, retrievers, models)
6. Use LlamaIndex's `Evaluate` module or integrate with LangSmith
Continuously monitor in production to catch degradation.

**Q88: What is "fine-tuning" in the context of LlamaIndex?**
A: LlamaIndex supports fine-tuning for:
- Embedding models: `SentenceTransformersFinetuneEngine` fine-tunes embeddings on your data for better retrieval
- LLMs: `OpenAIFineTuningEngine` fine-tunes LLM for response synthesis (domain adaptation)
- Rerankers: fine-tune cross-encoders on your relevance judgments
Fine-tuned embeddings can significantly improve retrieval quality for domain-specific data.

**Q89: What are "callback events" and how do you use them for monitoring?**
A: Callback events fire at each stage:
```
CBEventType. CHUNKING → NODE_PARSING → EMBEDDING → LLM → RETRIEVE → SYNTHESIS
```
Each event has: event_type, payload, start/end time. Use:
```python
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
cb_manager = CallbackManager([token_counter])
Settings.callback_manager = cb_manager
```
For production monitoring: integrate with LangSmith, Arize, or custom logging.

**Q90: What is the "Observability" integration in LlamaIndex?**
A: LlamaIndex integrates with:
- LangTracer: full trace visualization (suggested, by LlamaIndex team)
- LangSmith: LangChain's observability platform
- Arize AI: ML observability, drift detection
- Weights & Biases: experiment tracking
- OpenTelemetry: export traces to any backend
- Custom: subclass BaseCallbackHandler
Set via: `Settings.callback_manager = CallbackManager([handler])`

## 6. Production, Comparisons & Future (Q91–Q100)

**Q91: How do you deploy a LlamaIndex application to production?**
A: 
1. Package your index build + query engine as a service (FastAPI/Flask)
2. Pre-build the index at deployment time (build once, load from disk/vector DB)
3. Use vector store (Pinecone, Qdrant, Weaviate) — not in-memory
4. Ingestion pipeline for document updates
5. Monitoring via callbacks + LangTracer
6. Caching: response cache for frequent queries
7. Rate limiting, authentication
8. Horizontal scaling: stateless query engines, stateful ingestion

**Q92: How does LlamaIndex compare to Haystack for RAG?**
A: LlamaIndex: more retrieval strategies, better data ingestion, stronger agent integration. Haystack: simpler API, better pipeline visualization, more document store backends. Both are strong for RAG. LlamaIndex is better for complex retrieval + agentic RAG; Haystack is better for simpler, standardized RAG pipelines.

**Q93: How does LlamaIndex handle "prompt engineering" for RAG?**
A: Custom prompts for each stage:
```python
from llama_index.core import PromptTemplate
qa_prompt = PromptTemplate(
    "Context:\n{context}\n\nQuestion: {query}\n\nAnswer: "
)
query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
    refine_template=refine_prompt
)
```
Customize: system prompt, QA prompt, refinement prompt, summarization prompt. Each is a PromptTemplate with access to context, query, and chat history.

**Q94: What is the "cost optimization" strategy for LlamaIndex RAG?**
A: 
1. Cache responses for known queries
2. Use smaller/cheaper LLM for synthesis (e.g., GPT-4o-mini vs GPT-4o)
3. Reranking: reduces context size (top-20 → top-5, less LLM tokens)
4. Embedding caching: avoid re-embedding
5. Chunk size tuning: smaller chunks = more precise, fewer tokens per query
6. Batch processing: reuse LLM context for multiple queries
7. Use local models (Ollama, llama.cpp) for less critical tasks

**Q95: How do you handle PII and security in LlamaIndex?**
A: 
- Pre-processing: strip PII during ingestion (regex, Presidio)
- Metadata: don't store sensitive data in node metadata (used for retrieval)
- Access control: filter retrieval by document access-level metadata
- Output scanning: scan LLM responses for PII leakage
- Encryption: encrypt vector store connection, use TLS for API
- Audit: log all queries and retrievals for compliance

**Q96: What are the "token limits" considerations in LlamaIndex?**
A: 
- Context window: fit system prompt + context nodes + history + query
- Chunk size + k (retrieval count): chunk_size * k < context_window - overhead
- Overhead: prompt template (~500 tokens), system prompt (~500), chat history
- Strategy: if k=5, chunk_size=500, overhead=1000 → need 3500 context minimum
- For large context models (128K+): can use larger chunks or more chunks
- Fallback: if context exceeded, `compact` mode concat until full, then `refine` for overflow

**Q97: What is the "llama-index-vector-stores" integration ecosystem?**
A: LlamaIndex supports vector stores via integration packages:
- `llama-index-vector-stores-pinecone`
- `llama-index-vector-stores-qdrant`
- `llama-index-vector-stores-weaviate`
- `llama-index-vector-stores-milvus`
- `llama-index-vector-stores-chroma`
- `llama-index-vector-stores-faiss`
- `llama-index-vector-stores-postgres` (pgvector)
- `llama-index-vector-stores-elasticsearch`
Each implements `VectorStore` interface for plug-and-play.

**Q98: How do you migrate from LlamaIndex v0.9 to v0.10+?**
A: 
1. `ServiceContext` → `Settings`
2. Import paths change: `llama_index` → `llama_index.core` (core), `llama_index.llms.openai` (integrations)
3. `pip install llama-index-core` + specific integration packages
4. `Response` object API changes
5. Callback system migrated to dispatcher
6. Index persistence API changes (`.persist()` → `.storage_context.persist()`)
Migration guide in LlamaIndex docs. Major improvements justify the upgrade.

**Q99: What are the anti-patterns in LlamaIndex usage?**
A: 
1. Chunking too large: losing retrieval precision
2. No metadata filtering: retrieving irrelevant content
3. No reranking: top-k may miss the best results
4. Ignoring embedding model quality: poor retrieval = poor RAG
5. Using only vector search: missing keyword matches
6. Not evaluating: deploying without measuring recall/faithfulness
7. Over-indexing: indexing everything without considering what the LLM already knows
8. Stateful chat without context management: blowing up context window

**Q100: What emerging trends are shaping LlamaIndex in 2026?**
A: 
1. Agent-native RAG: agents that dynamically decide retrieval strategy per query
2. Multi-modal indexing: text + images + audio + video in unified indexes
3. GraphRAG maturation: knowledge graph + vector hybrid as default for complex queries
4. Streaming ingestion: real-time document processing pipelines
5. Evaluation-driven RAG: automated quality gates for retrieval pipelines
6. Fine-tuned mini-embeddings: domain-specific small models beating general large ones
7. On-device indexing: LlamaIndex running on mobile/edge with local models
8. Multi-turn retrieval agents: conversational data exploration with memory and context
