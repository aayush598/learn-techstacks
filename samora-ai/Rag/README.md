# RAG Interview Questions and Answers

## Q1: What is RAG (Retrieval Augmented Generation)?
**A:** RAG is an AI framework that combines information retrieval with text generation. It retrieves relevant documents from a knowledge base and provides them as context to an LLM, enabling the model to generate accurate, grounded responses based on actual data rather than relying solely on parametric knowledge.

## Q2: Why is RAG important?
**A:** RAG addresses key limitations of LLMs: it provides access to current information (solving knowledge cutoff), reduces hallucinations by grounding responses in retrieved data, enables domain-specific knowledge without retraining, and allows citation of sources for verifiability.

## Q3: What are the main components of a RAG system?
**A:** The main components are: 1) Document Ingestion Pipeline (load, split, embed, store), 2) Vector Database (stores embeddings for similarity search), 3) Retriever (finds relevant documents), 4) LLM (generates responses using retrieved context), and 5) Prompt Template (structures the LLM input with context and query).

## Q4: How does a basic RAG pipeline work?
**A:** 1) User submits a query, 2) Query is embedded into a vector, 3) Vector database performs similarity search to find relevant documents, 4) Retrieved documents are added to a prompt as context, 5) LLM generates a response grounded in the provided context, 6) Response with citations is returned to the user.

## Q5: What is the difference between RAG and fine-tuning?
**A:** RAG provides external knowledge at inference time without modifying the model. Fine-tuning updates model weights to incorporate new knowledge. RAG is better for frequently changing data and access control. Fine-tuning is better for learning new skills or styles. They are complementary and can be combined.

## Q6: What types of RAG architectures exist?
**A:** Types include: Naive RAG (retrieve-then-generate), Advanced RAG (with pre/post-retrieval optimizations), Modular RAG (composable modules), Agentic RAG (agents decide retrieval strategy), Corrective RAG (self-correcting retrieval), and Speculative RAG (hypothesis-driven retrieval).

## Q7: What is Naive RAG?
**A:** Naive RAG is the simplest form: index documents, retrieve relevant chunks, augment prompt, generate response. It is straightforward but suffers from retrieval quality issues, lack of query understanding, and limited context utilization.

## Q8: What is Advanced RAG?
**A:** Advanced RAG adds pre-retrieval (query rewriting, expansion, decomposition) and post-retrieval (reranking, filtering, compression) optimizations. It improves retrieval accuracy and context quality through techniques like HyDE, query transformation, and multi-step retrieval.

## Q9: What is Modular RAG?
**A:** Modular RAG decomposes the RAG pipeline into interchangeable modules (search, filtering, reranking, memory, fusion, etc.) that can be composed flexibly. This enables custom RAG patterns like search-rerank-generate or multi-query fusion.

## Q10: What is Agentic RAG?
**A:** Agentic RAG uses an AI agent that autonomously decides when and how to retrieve information. The agent can decide whether retrieval is needed, choose which tools/databases to query, perform multi-step research, refine queries, and synthesize results from multiple sources.

## Q11: What is a vector database?
**A:** A vector database stores and indexes high-dimensional vector embeddings for fast similarity search. It supports operations like ANN (Approximate Nearest Neighbor) search, metadata filtering, and hybrid search. Examples include Pinecone, Weaviate, Qdrant, Chroma, and Milvus.

## Q12: How does similarity search work in vector databases?
**A:** Vector databases index embeddings using algorithms like HNSW (Hierarchical Navigable Small Worlds), IVF (Inverted File Index), or PQ (Product Quantization). Given a query vector, they find nearest neighbors using distance metrics like cosine similarity, Euclidean distance, or dot product.

## Q13: What are embeddings in RAG?
**A:** Embeddings are dense vector representations of text (or other data) that capture semantic meaning. In RAG, both documents and queries are embedded into the same vector space. Semantic similarity is measured by distance between vectors.

## Q14: What embedding models are commonly used for RAG?
**A:** Popular embedding models include: OpenAI text-embedding-3-small/large, Cohere embed-english-v3.0, Google text-embedding-004, Sentence Transformers (all-MiniLM-L6-v2, BAAI/bge-large-en-v1.5), and open-source models from Mistral, Voyage AI, and Jina AI.

## Q15: What is chunking in RAG?
**A:** Chunking splits documents into smaller, coherent pieces before embedding and indexing. Good chunking preserves semantic boundaries, respects content structure, and creates chunks of appropriate size for retrieval. Strategies include fixed-size, recursive, semantic, and document-aware chunking.

## Q16: What chunking strategies are there?
**A:** Strategies include: Fixed-size (N characters with overlap), Recursive (split on separators like paragraphs and sentences), Semantic (based on embedding similarity changes), Document-aware (respecting Markdown/HTML structure), and Sentence-based (NLTK/spaCy sentence splitting).

## Q17: What is the optimal chunk size for RAG?
**A:** Optimal chunk size depends on the use case and LLM context window. Typical sizes range from 256-1024 tokens. Smaller chunks provide precise retrieval but may lack context. Larger chunks provide more context but may introduce noise. Experimentation is key.

## Q18: What is chunk overlap?
**A:** Chunk overlap adds a sliding window of N characters/tokens between consecutive chunks. This prevents information loss at chunk boundaries. Common overlap is 10-20% of chunk size. Overlap increases storage but improves retrieval completeness.

## Q19: What is a retriever in RAG?
**A:** A retriever takes a user query and returns relevant documents from the knowledge base. Retrievers can be sparse (BM25, TF-IDF), dense (embedding-based), hybrid (combining sparse and dense), or multi-modal.

## Q20: What is dense retrieval?
**A:** Dense retrieval uses neural embeddings to represent queries and documents as dense vectors, then finds nearest neighbors in embedding space. It captures semantic similarity beyond keyword matching but requires good embedding models.

## Q21: What is sparse retrieval (BM25)?
**A:** BM25 is a keyword-based retrieval algorithm that ranks documents by term frequency and inverse document frequency. It is fast, does not require embeddings, excels at exact keyword matching, and is often used as a baseline or in hybrid retrieval systems.

## Q22: What is hybrid retrieval?
**A:** Hybrid retrieval combines dense (semantic) and sparse (keyword) retrieval results, typically using weighted fusion (RRF, weighted sum, or learning to rank). This leverages the strengths of both approaches: semantic understanding from dense and exact matching from sparse.

## Q23: What is Reciprocal Rank Fusion (RRF)?
**A:** RRF combines multiple ranked lists by scoring each document as the sum of reciprocal ranks: score = sum of 1/(k + rank_i(d)). It is parameter-free and effective for fusing results from different retrieval methods without training.

## Q24: What is query rewriting in RAG?
**A:** Query rewriting transforms the user's original query to improve retrieval quality. Examples include expanding acronyms, correcting spelling, adding synonyms, decomposing complex queries, and converting conversational queries into standalone search queries.

## Q25: What is HyDE (Hypothetical Document Embeddings)?
**A:** HyDE generates a hypothetical ideal document that would answer the query, embeds that instead of the query, and retrieves documents similar to the hypothesis. This bridges the vocabulary gap between short queries and long documents.

## Q26: What is query expansion?
**A:** Query expansion adds related terms, synonyms, or generated variations to the original query before retrieval. This broadens the search to capture more relevant documents. Techniques include synonym expansion, LLM-generated expansions, and relevance feedback-based expansion.

## Q27: What is query decomposition?
**A:** Query decomposition breaks a complex question into simpler sub-questions, retrieves documents for each sub-question, and synthesizes the results. For example, comparing the economies of France and Japan becomes separate queries for each country.

## Q28: What is multi-hop RAG?
**A:** Multi-hop RAG requires multiple rounds of retrieval, where information from one retrieval informs the next query. This is needed for questions that require connecting information across multiple documents.

## Q29: What is iterative retrieval?
**A:** Iterative retrieval performs multiple rounds of retrieval, using results from previous rounds to refine the query. Each iteration can use the LLM's assessment of missing information to formulate better follow-up queries.

## Q30: What is RAPTOR?
**A:** RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) builds a hierarchical tree of document summaries. Documents are chunked, embedded, clustered, and summarized recursively. Retrieval navigates this tree at appropriate levels of abstraction.

## Q31: What is Reranking in RAG?
**A:** Reranking takes the initial retrieval results (top-k from fast retrieval) and re-evaluates them using a more accurate but slower model (cross-encoder). This improves precision by reordering results based on deeper relevance assessment.

## Q32: What are cross-encoders for reranking?
**A:** Cross-encoders jointly process query-document pairs through a transformer, producing a relevance score. They are more accurate than bi-encoders but slower since each pair must be processed together.

## Q33: What is the difference between bi-encoders and cross-encoders?
**A:** Bi-encoders encode query and document independently into fixed vectors (fast, scalable for retrieval). Cross-encoders process query-document pairs together (slow but accurate). Bi-encoders are used for initial retrieval; cross-encoders for reranking.

## Q34: What is Cohere Rerank?
**A:** Cohere Rerank is a hosted reranking API that uses a cross-encoder model to score query-document relevance. It takes a query and a list of documents, returns relevance scores, and improves RAG quality by filtering out irrelevant documents.

## Q35: What is the Lost-in-the-Middle problem?
**A:** The Lost-in-the-Middle problem refers to LLMs ignoring information in the middle of long contexts. When multiple retrieved documents are provided, those in the middle receive less attention. Solutions include placing the most relevant documents first and last.

## Q36: How does context window size affect RAG?
**A:** Larger context windows allow more retrieved documents and longer documents. However, they do not solve the Lost-in-the-Middle problem and increase computational cost. Typical strategies include limiting to top-k documents and compressing context.

## Q37: What is context compression in RAG?
**A:** Context compression reduces retrieved documents to only the most relevant parts before feeding them to the LLM. Techniques include extractive compression (select relevant sentences), abstractive compression (LLM summarizes), and selective retrieval.

## Q38: What is the RAG prompt template?
**A:** A RAG prompt template structures the LLM input with system instructions, retrieved context (with source references), and user query. Example: "Answer the question based on the context. If the context does not contain the answer, say so."

## Q39: How do you structure RAG prompts for best results?
**A:** Place context before the question, clearly separate context from instruction, include source attribution, ask the model to cite sources, instruct the model to say "I don't know" if the answer is not in context, and handle cases with no retrieved documents.

## Q40: What is RAG evaluation?
**A:** RAG evaluation measures retrieval quality (precision, recall, MRR, NDCG), generation quality (faithfulness, answer relevance, completeness), and end-to-end metrics. Frameworks like RAGAS, TruLens, and ARES provide comprehensive evaluation.

## Q41: What is RAGAS?
**A:** RAGAS (RAG Assessment) is a framework for evaluating RAG systems. It measures Faithfulness (is the answer grounded in context?), Answer Relevance (does the answer address the question?), Context Precision (are retrieved documents relevant?), and Context Recall (are all relevant documents retrieved?).

## Q42: What is faithfulness in RAG evaluation?
**A:** Faithfulness measures whether the generated answer is supported by the retrieved context. It checks for hallucinations or claims not present in the context. High faithfulness means the model does not add unsupported information.

## Q43: What is answer relevance in RAG?
**A:** Answer relevance measures how well the generated answer addresses the user's question. Irrelevant details or overly generic responses score low. It is typically measured by computing similarity between the answer and the question.

## Q44: What is context precision?
**A:** Context precision measures whether the retrieved documents are relevant to the question. It penalizes retrieval of irrelevant documents. High precision means most retrieved chunks contain information useful for answering the query.

## Q45: What is context recall?
**A:** Context recall measures whether all necessary information to answer the question was retrieved. It penalizes missing relevant information. Low recall means the LLM lacks sufficient context and may hallucinate or fail to answer.

## Q46: How do you handle cases where no relevant documents are retrieved?
**A:** Strategies include: instruct the LLM to say "I don't have enough information", fall back to general knowledge (optionally flagged), try alternative retrieval (different embedding model, BM25), expand the query, or use rephrased queries.

## Q47: What is self-RAG?
**A:** Self-RAG (by Asai et al.) is a framework where the LLM decides when to retrieve, generates reflections on retrieved passages (is it relevant, supporting, or refuting), and uses special tokens to control retrieval and generation steps.

## Q48: What is Corrective RAG (CRAG)?
**A:** CRAG evaluates the relevance of retrieved documents and takes corrective action: if documents are relevant it generates; if some are relevant it filters and keeps only relevant ones; if none are relevant it falls back to web search or LLM knowledge.

## Q49: What is Speculative RAG?
**A:** Speculative RAG generates multiple possible answers from different document subsets (speculations), then evaluates them against the full set of retrieved documents. It improves both speed and accuracy.

## Q50: What is Graph RAG?
**A:** Graph RAG uses knowledge graphs instead of (or alongside) vector databases for retrieval. It captures entities, relationships, and community structure. Queries traverse the graph to find relevant information. Developed by Microsoft.

## Q51: How does Graph RAG work?
**A:** 1) Build a knowledge graph from documents (extract entities and relationships), 2) Detect communities using graph algorithms (Leiden clustering), 3) Generate summaries for communities, 4) For a query, find relevant communities and entities, 5) Retrieve connected information from the graph, 6) Augment the LLM with structured graph context.

## Q52: What is Agentic RAG vs Simple RAG?
**A:** Simple RAG retrieves once and generates. Agentic RAG uses an AI agent that decides if retrieval is needed, chooses which sources to query, writes its own search queries, performs multi-step research, and synthesizes answers from multiple sources.

## Q53: What is Multi-Modal RAG?
**A:** Multi-Modal RAG retrieves and generates across multiple data types: text, images, tables, audio, and video. It uses multi-modal embeddings (CLIP, SigLIP) for cross-modal retrieval and multi-modal LLMs (GPT-4V, Gemini) for generation.

## Q54: What is Multi-Vector RAG?
**A:** Multi-Vector RAG creates multiple embeddings per document (chunk, summary, keywords, hypothetical questions). At retrieval time, it can match against different representations, improving coverage. The full document is provided as context.

## Q55: What is Parent Document Retrieval?
**A:** Parent Document Retrieval stores chunks at two levels: small child chunks (for precise retrieval) and larger parent chunks (for full context). It retrieves the most relevant child chunk but provides the parent chunk as context.

## Q56: What is Sentence Window Retrieval?
**A:** Sentence Window Retrieval embeds individual sentences for precise retrieval but provides surrounding sentences (a window) as context. This ensures the LLM gets sufficient context while maintaining precise retrieval.

## Q57: What are metadata filters in RAG?
**A:** Metadata filters restrict retrieval to documents with specific metadata attributes such as date range, author, category, source, or document type. This improves precision by narrowing the search space before similarity search.

## Q58: What is time-weighted retrieval?
**A:** Time-weighted retrieval biases results toward more recent documents by combining relevance scores with recency weights. It is useful for domains where information freshness matters such as news and finance.

## Q59: What is the Curse of Dimensionality in vector search?
**A:** The Curse of Dimensionality refers to distances between points becoming less meaningful in high-dimensional spaces. For very high dimensional embeddings (e.g., 4096d), nearest neighbor search becomes less effective, requiring dimensionality reduction or quantization.

## Q60: How do you scale RAG systems?
**A:** Scaling strategies include sharding vector databases across nodes, using ANN indexes, implementing caching for frequent queries, batch document ingestion, distributed processing, and optimizing embedding generation with batching.

## Q61: What is incremental indexing in RAG?
**A:** Incremental indexing adds new documents to the vector database without re-indexing existing ones. New documents are embedded and upserted into the index. This enables real-time updates and requires vector DB support for dynamic updates.

## Q62: What is the difference between ANN and KNN search?
**A:** KNN (k-Nearest Neighbors) finds exact nearest neighbors by comparing against all vectors (accurate but slow). ANN (Approximate Nearest Neighbor) uses indexes like HNSW to find approximate neighbors quickly (faster, slightly less accurate).

## Q63: What are the different ANN algorithms?
**A:** Common ANN algorithms: HNSW (best for high recall), IVF (memory efficient), PQ (Product Quantization - memory efficient), DiskANN (for SSD-based indexes), and LSH (Locality-Sensitive Hashing).

## Q64: What is HNSW?
**A:** HNSW (Hierarchical Navigable Small World) is a graph-based ANN algorithm. It builds a multi-layer graph where upper layers have fewer nodes with long-range connections and lower layers have more nodes with short-range connections. Search traverses from top to bottom.

## Q65: What is IVF (Inverted File Index)?
**A:** IVF partitions the vector space into Voronoi cells using k-means clustering. At search time, it searches only the closest cells to the query. IVF is memory-efficient but slower than HNSW for very high recall requirements.

## Q66: What is Product Quantization (PQ)?
**A:** PQ compresses vectors by splitting them into sub-vectors and quantizing each sub-vector separately with a codebook. This dramatically reduces memory (16x-64x compression) at the cost of some accuracy. Often used with IVF.

## Q67: What is the role of a Parser in document ingestion?
**A:** A parser extracts text and structure from raw documents. Different parsers handle different formats: PDF (PyMuPDF, Unstructured), HTML (BeautifulSoup), Markdown, DOCX, and images (OCR with Tesseract).

## Q68: How do you handle PDFs in RAG?
**A:** PDF handling challenges include mixed content (text, images, tables), multi-column layouts, headers/footers extracting incorrectly, and scanned documents. Solutions include using specialized PDF parsers (PyMuPDF, marker, docling) and OCR for scanned PDFs.

## Q69: What is table extraction in RAG?
**A:** Table extraction identifies and preserves tabular data from documents. Approaches include rule-based (regex, layout analysis), ML-based (Table Transformer), and LLM-based (prompted extraction). Preserved tables can be linearized into text.

## Q70: What is the difference between structured and unstructured data in RAG?
**A:** Structured data is organized (SQL tables, CSV, JSON, knowledge graphs). Unstructured data is free-form (text, PDF, images). RAG traditionally handles unstructured data via chunking and embeddings. Structured data requires text-to-SQL or graph traversal approaches.

## Q71: What is Text-to-SQL in RAG?
**A:** Text-to-SQL converts natural language questions into SQL queries, retrieves results from databases, and uses those results as context for the LLM. This enables RAG over structured databases.

## Q72: What is a RAG agent?
**A:** A RAG agent is an AI agent that uses retrieval as a tool. It decides whether to retrieve, what to search for, which sources to query, when to stop searching, and how to synthesize information. Agents enable adaptive retrieval strategies.

## Q73: How do you handle real-time data in RAG?
**A:** For real-time data: use web search tools, continuously ingest streaming data, implement incremental indexing, use time-decayed relevance scoring, maintain a hot cache for frequent queries, and set up data pipelines for document ingestion.

## Q74: What is data freshness in RAG?
**A:** Data freshness measures how up-to-date the knowledge base is. Strategies include timestamping documents, using time-weighted retrieval, scheduling re-indexing jobs, implementing incremental updates, and integrating real-time data sources.

## Q75: How do you handle duplicate documents in RAG?
**A:** Deduplication techniques include exact hash matching (MD5, SHA), near-duplicate detection (MinHash, SimHash), embedding similarity thresholding, and content-based deduplication. Deduplication reduces storage and prevents redundant retrieval.

## Q76: What is a RAG cache?
**A:** A RAG cache stores frequently retrieved results and generated responses. Levels include query cache (same query to cached response), embedding cache (same query to cached embedding), document cache (frequently retrieved docs), and partial cache.

## Q77: What is streaming in RAG?
**A:** Streaming in RAG sends the response token-by-token as the LLM generates it. The UI can show retrieved documents first, then stream the generated answer. This improves perceived latency and user experience.

## Q78: What are citations in RAG?
**A:** Citations reference the specific source passages used to generate each part of the response. They enable fact-checking and build trust. Implementation includes source IDs in retrieved context and instructing the LLM to cite sources inline.

## Q79: How do you implement citations in RAG?
**A:** Assign unique IDs to each retrieved chunk, include IDs in the prompt context, instruct the model to reference IDs, and post-process to extract citations. Verify that cited content actually supports the associated claims.

## Q80: What is RAG with conversational memory?
**A:** Conversational RAG maintains conversation history and uses it for context-aware retrieval. The system may reformulate follow-up questions using history, retrieve based on conversation context, and use previous retrievals to inform current retrieval.

## Q81: How do you handle follow-up questions in RAG?
**A:** Use conversation history to contextualize follow-up queries. Techniques include rewriting the query incorporating context, retrieving based on the full conversation, and filtering results using session context.

## Q82: What are common failure modes in RAG?
**A:** Common failures include irrelevant retrieval (returning unrelated documents), incomplete retrieval (missing necessary information), lost in the middle (LLM ignores relevant context), hallucination (LLM ignores context), and citation errors.

## Q83: How do you debug a RAG system?
**A:** Debug by examining each component: inspect retrieved documents for relevance, check embedding quality, evaluate prompt construction, analyze LLM response for context usage, and test with known-answer queries.

## Q84: What tools and frameworks are available for building RAG systems?
**A:** Popular frameworks include LangChain, LlamaIndex, Haystack, RAGatouille, and Canopy (by Pinecone). They provide document loaders, splitters, embedding integrations, vector store connectors, and retrieval pipelines.

## Q85: What is LangChain's role in RAG?
**A:** LangChain provides document loaders (50+ formats), text splitters, embedding wrappers, vector store integrations, retrieval chains (stuff, map-reduce, refine), and LCEL for composing RAG pipelines.

## Q86: What is LlamaIndex's role in RAG?
**A:** LlamaIndex specializes in data indexing and retrieval for RAG. It provides data connectors (160+ sources), advanced indexing strategies (tree, keyword, vector, hybrid), query engines, and routing.

## Q87: What is Haystack in RAG?
**A:** Haystack is an open-source framework for RAG pipelines. It provides components (Embedder, Retriever, Reader/Generator), document stores (Elasticsearch, Weaviate, Pinecone), and pipeline orchestration.

## Q88: What is the difference between RAG and search engines?
**A:** Search engines return ranked lists of documents. RAG retrieves documents AND generates a synthesized answer. RAG provides direct answers with citations; search engines require users to browse results.

## Q89: How do you choose between RAG and fine-tuning?
**A:** Choose RAG when: data changes frequently, you need source citations, or you need access control. Choose fine-tuning when: you need to teach new skills/formats, you have stable data patterns, or latency is critical.

## Q90: Can RAG and fine-tuning be combined?
**A:** Yes. Fine-tune an LLM on domain-specific instructions, then use RAG to provide current knowledge. The fine-tuned model better understands how to use retrieved context. This hybrid approach often outperforms either method alone.

## Q91: What is RAG for code generation?
**A:** Code RAG retrieves relevant code snippets, documentation, and examples from a codebase to augment code generation. It is used for repository-level code completion, API usage generation, and code Q&A.

## Q92: What is RAG for enterprise search?
**A:** Enterprise RAG indexes internal documents (policies, wikis, product docs, emails) and provides a natural language interface. It must handle access control, data privacy, diverse formats, and high accuracy.

## Q93: How do you handle access control in RAG?
**A:** Implement access control by tagging documents with permissions, filtering retrieved results by user roles, using metadata-based ACLs, and ensuring the LLM never exposes unauthorized information.

## Q94: What is the cost of operating a RAG system?
**A:** Costs include embedding generation, vector database hosting, LLM inference (token costs), document processing, and monitoring. Optimization strategies include caching, smaller embedding models, and efficient indexing.

## Q95: What are emerging trends in RAG?
**A:** Trends include Agentic RAG (autonomous retrieval agents), Long-context RAG (models with 1M+ context windows), Graph RAG (knowledge graph integration), Multi-modal RAG, and Self-RAG.

## Q96: How does long-context affect RAG?
**A:** Very long context windows (Gemini 1.5 Pro, Claude 3.5, GPT-4-128k) allow processing more retrieved documents. This changes RAG design with less need for chunking but still faces lost-in-the-middle and cost challenges.

## Q97: What is RAG quality assurance?
**A:** QA involves: testing with diverse queries, measuring retrieval metrics (precision, recall, MRR), evaluating generation quality (faithfulness, relevance), monitoring for drift, and setting up human evaluation pipelines.

## Q98: How do you optimize RAG latency?
**A:** Optimize by: using ANN indexes for fast retrieval, caching frequent queries, streaming responses, pre-computing embeddings, using smaller embedding models, parallelizing retrieval, and optimizing LLM inference with quantization or smaller models.

## Q99: What is the RAG document pipeline?
**A:** The document pipeline includes: document loading (from various sources), cleaning (remove noise, normalize text), chunking (split into appropriate pieces), embedding (convert to vectors), and indexing (store in vector database with metadata).

## Q100: What is the future of RAG?
**A:** Future directions include: Agentic RAG with autonomous research capabilities, native long-context integration, multi-modal retrieval across text/image/video, self-improving RAG with feedback loops, and standardized RAG evaluation benchmarks.
