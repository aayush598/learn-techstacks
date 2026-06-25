# AI/ML, LangChain & RAG - 300+ Interview Q&A
## For YC Startups & Top Tech Companies

## Machine Learning Fundamentals (Q1-Q35)
### Q1: What is Machine Learning? How does it differ from traditional programming?
**Answer:** ML: system learns patterns from data without explicit rules. Traditional: programmer writes rules (if-else). ML: model learns from examples. Types: Supervised (labeled data), Unsupervised (unlabeled), Reinforcement (reward-based). ML excels at tasks too complex for hand-coded rules (image recognition, NLP, recommendations).

### Q2: Explain Supervised, Unsupervised, and Reinforcement Learning.
**Answer:** Supervised: X→Y mapping, labeled data. Tasks: regression (predict price), classification (spam detection). Unsupervised: find hidden patterns in unlabeled data. Tasks: clustering (customer segments), dimensionality reduction (PCA), anomaly detection. Reinforcement: agent learns by interacting with environment, maximizing rewards. Used in: game playing (AlphaGo), robotics.

### Q3: Overfitting vs Underfitting - causes and solutions.
**Answer:** Overfitting: learns noise, memorizes training data. High variance, low bias. Symptoms: great train metrics, poor test metrics. Solutions: more data, regularization, simpler model, dropout, early stopping, cross-validation. Underfitting: too simple, misses patterns. High bias, low variance. Symptoms: poor on both train and test. Solutions: more complex model, better features, fewer constraints, longer training.

### Q4: Explain the bias-variance tradeoff.
**Answer:** Total error = bias² + variance + irreducible error. Bias: error from wrong assumptions (underfitting). Variance: error from sensitivity to training data (overfitting). As model complexity increases, bias decreases but variance increases. Goal: find optimal complexity that minimizes total error.

### Q5: What is cross-validation? Describe k-fold.
**Answer:** Technique to assess model generalization. k-fold: split data into k equal folds, train on k-1, validate on 1, repeat k times. Report average ± std. k=5 or 10 common. Stratified k-fold: preserves class proportions in each fold. Leave-one-out: k=N (expensive but unbiased).

### Q6: L1 vs L2 regularization?
**Answer:** L1 (Lasso): adds Σ|wᵢ| to loss. Produces sparse solutions (many weights become 0) - feature selection. L2 (Ridge): adds Σwᵢ² to loss. Shrinks weights but doesn't zero them. ElasticNet: combines both. L1 for feature selection, L2 when all features potentially relevant.

### Q7: Precision, Recall, F1 Score explained.
**Answer:** Precision = TP/(TP+FP) - "of predicted positives, how many are correct?" Recall = TP/(TP+FN) - "of actual positives, how many did we find?" F1 = 2*P*R/(P+R) - harmonic mean. Use precision when FP costly (spam), recall when FN costly (cancer screening), F1 when balance needed.

### Q8: ROC curve and AUC explained.
**Answer:** ROC: plots TPR (recall) vs FPR (fall-out) at various thresholds. AUC = probability model ranks random positive higher than random negative. AUC 0.5=random, 0.7-0.8=fair, 0.8-0.9=good, 0.9+=excellent. For imbalanced datasets, use PR-AUC instead.

### Q9: Gradient Descent variants?
**Answer:** Batch GD: gradient computed on entire dataset. Accurate but slow, can't handle large data. SGD: gradient on one sample. Fast, noisy, can escape local minima. Mini-batch GD: gradient on small batch (32-256). Best of both - stable, efficient, vectorized. Adam: adaptive learning rates + momentum. Most commonly used optimizer.

### Q10: Decision Trees - how do they work?
**Answer:** Recursive partitioning of feature space. At each node, split on feature that maximizes information gain (classification: entropy/Gini, regression: variance reduction). Leaves make predictions. Prone to overfitting - use max_depth, min_samples_split, or ensemble methods (Random Forest, Gradient Boosting).

### Q11: Random Forest explained.
**Answer:** Ensemble of decision trees trained with bagging (bootstrap aggregation) + random feature selection. Each tree trained on random sample with replacement. At each split, only random subset of features considered. Predict by averaging (regression) or majority vote (classification). Reduces variance without increasing bias. Robust to overfitting.

### Q12: Gradient Boosting (XGBoost, LightGBM) explained.
**Answer:** Sequentially add trees, each correcting errors of previous. Each new tree predicts residuals (gradient of loss). XGBoost: regularized, handles missing values, parallelized. LightGBM: leaf-wise growth (faster, uses less memory). CatBoost: handles categorical features natively. Best for tabular data (structured data).

### Q13: Feature engineering techniques?
**Answer:** Numerical: scaling (Standard/MinMax/Robust), binning (equal width/frequency), polynomial features, log/Box-Cox transforms. Categorical: one-hot encoding, label encoding, target encoding, frequency encoding. Temporal: day/month/year, dayofweek, is_weekend, elapsed time. Text: TF-IDF, count vectorizer, embeddings.

### Q14: Handling imbalanced datasets?
**Answer:** Resampling: oversample minority (SMOTE creates synthetic samples), undersample majority. Algorithm-level: class weights, focal loss, anomaly detection approaches. Evaluation: use precision/recall/F1, PR-AUC, not accuracy. Ensemble: balanced Random Forest, EasyEnsemble.

## Deep Learning (Q36-Q65)
### Q15: Neural network basics - perceptron, activation functions.
**Answer:** Perceptron: y = σ(w·x + b). Single layer, linear decision boundary. Activation functions: sigmoid (0-1, vanishing gradient), tanh (-1-1, still vanishing), ReLU (max(0,x), most common, dying ReLU problem), Leaky ReLU (0.01x for x<0), GELU (smooth, used in transformers), Swish. Output: linear (regression), sigmoid (binary), softmax (multi-class).

### Q16: Backpropagation explained.
**Answer:** Chain rule applied to compute gradients of loss w.r.t. all weights. Forward pass: compute predictions. Backward pass: compute error at output, propagate backwards through layers. Update weights via gradient descent. Key equations: δ_output = (ŷ - y) * σ'(z), δ_hidden = (W·δ_next) * σ'(z).

### Q17: What is a Transformer? Key components?
**Answer:** "Attention is All You Need" (Vaswani 2017). Key: self-attention replaces recurrence. Components: multi-head attention, feed-forward network, positional encoding, layer norm, residual connections. Scaled dot-product attention: Attention(Q,K,V) = softmax(QK^T/√d_k)V. Encoder processes input, decoder generates output. Foundation for BERT, GPT, T5.

### Q18: BERT vs GPT - key differences?
**Answer:** BERT: encoder-only, bidirectional attention, masked language modeling, good for understanding tasks (classification, QA, NER). GPT: decoder-only, unidirectional (causal) attention, autoregressive, good for generation. BERT sees both left and right context, GPT sees only left context. BERT fine-tuned, GPT prompted.

### Q19: What is Transfer Learning?
**Answer:** Take pre-trained model (trained on large dataset like ImageNet, Wikipedia), adapt to specific task with less data. Approaches: feature extraction (freeze base, train new head), fine-tuning (unfreeze some/all layers, train with low learning rate). Benefits: requires less data, faster training, better performance.

### Q20: Dropout - what is it and why does it work?
**Answer:** Randomly deactivates neurons during training (typical rate 0.1-0.5). Effect: prevents co-adaptation of neurons, creates ensemble effect (different architectures each batch), reduces overfitting. At inference, all neurons active but weights scaled by keep probability.

### Q21: Batch Normalization vs Layer Normalization?
**Answer:** Batch Norm: normalize across batch dimension. Requires batch size, behaves differently at train/test. Used in CNNs. Layer Norm: normalize across feature dimension. Independent of batch size, same at train/test. Used in RNNs/Transformers. Modern LLMs use Layer Norm (RMSNorm variant).

### Q22: Optimizers - SGD vs Adam vs AdamW?
**Answer:** SGD: basic gradient descent, may need manual learning rate scheduling. Adam: adaptive learning rates per parameter + momentum. Fast convergence, less tuning. AdamW: Adam with decoupled weight decay (corrects Adam's regularization issue). Preferred for transformer training.

## LLMs (Q66-Q120)
### Q23: What is an LLM? How does text generation work?
**Answer:** Large Language Model - neural network (transformer) trained on massive text. Autoregressive generation: predict next token given previous. P(next_token | context). Decoding: greedy (highest prob), beam search (top-k paths), sampling (temperature, top-k, top-p/nucleus). Temperature: 0=deterministic, 1=creative. Top-p: sample from smallest set with cumulative probability > p.

### Q24: Tokenization - BPE, WordPiece, SentencePiece?
**Answer:** Maps text to tokens (subwords). BPE (GPT): iteratively merges most frequent byte pairs. WordPiece (BERT): merges pairs that maximize likelihood. SentencePiece (T5): treats input as raw bytes, doesn't require pre-tokenization (handles all languages). Vocabulary sizes: 32k-100k tokens.

### Q25: What is in-context learning?
**Answer:** LLM learns from examples in prompt without gradient updates. Zero-shot: no examples ("Translate to French: Hello"). Few-shot: 2-5 examples. Capability emerges at model scale (>10B parameters). Contrasts with fine-tuning (weight updates).

### Q26: What is hallucination in LLMs? How to mitigate?
**Answer:** LLM generates plausible but incorrect information. Causes: model learns statistical patterns, not facts; training data has inaccuracies; over-optimization for fluency. Mitigation: RAG (retrieve ground truth), chain-of-thought (verify reasoning), output validation, temperature reduction, fine-tuning on factual data, prompt engineering ("say 'I don't know' if unsure").

### Q27: Fine-tuning vs RAG - when to use which?
**Answer:** RAG: external knowledge, no training needed, easy to update, factual grounding, cite sources. Use for: knowledge base QA, customer support (docs). Fine-tuning: teach model new behavior/style/task, improve performance on specific format. Use for: writing in specific style, following specific formats, domain adaptation. Often combined (fine-tune for style, RAG for facts).

### Q28: What is LoRA? How does it work?
**Answer:** Low-Rank Adaptation. Freezes pre-trained weights, adds trainable low-rank matrices (A×B). Rank r << d (typically 8-64). Reduces trainable parameters by 10,000x. Applied to attention projection matrices. QLoRA: quantizes base model to 4-bit, adds LoRA adapters. Enables fine-tuning on single GPU.

### Q29: Model quantization - GPTQ, GGUF, AWQ?
**Answer:** Reduces model precision (32-bit→4-bit/8-bit). GPTQ: post-training quantization, GPU-optimized, layer-wise. GGUF: CPU-friendly, for llama.cpp. AWQ: activation-aware, better quality than GPTQ at same bit-width. Benefits: 4x memory reduction, faster inference. Quality degradation usually minimal.

## LangChain (Q121-Q200)
### Q30: What is LangChain? Core components?
**Answer:** Framework for LLM applications. Components: (1) Models - wrappers for LLM providers (OpenAI, Anthropic, etc). (2) Prompts - templates, few-shot, messages. (3) Chains - compose components sequentially (LLMChain, SequentialChain). (4) Agents - LLM decides actions using tools. (5) Memory - conversation history. (6) Retrieval - RAG pipeline (document loaders, splitters, vector stores, retrievers).

### Q31: What is LCEL (LangChain Expression Language)?
**Answer:** Declarative composability using `|` operator. Example: `chain = prompt | model | StrOutputParser`. Benefits: streaming, batching, async, parallel execution, tracing. Replace legacy Chain classes with LCEL.

### Q32: LangChain agents - how do they work?
**Answer:** ReAct pattern loop: (1) LLM receives prompt + tool descriptions + conversation. (2) LLM outputs "Thought: I need to search for X" + "Action: search_tool[query]". (3) System executes tool, returns observation. (4) Repeat until LLM outputs "Final Answer: ...". Agent types: OpenAI Tools, ReAct, Structured Chat, XML.

### Q33: LangChain memory types?
**Answer:** ConversationBufferMemory: stores raw messages. ConversationBufferWindowMemory: last k messages. ConversationSummaryMemory: LLM summarizes conversation. ConversationSummaryBufferMemory: summarize when token limit reached. VectorStoreRetrieverMemory: semantic retrieval from history. Combine types for complex needs.

### Q34: LangChain retrievers - types?
**Answer:** VectorStoreRetriever: similarity search against vector DB. ContextualCompressionRetriever: compress/rerank retrieved docs. EnsembleRetriever: combine multiple retrievers with weights. MultiQueryRetriever: generate multiple query variants. ParentDocumentRetriever: retrieve small chunks, return parent docs. TimeWeightedVectorStoreRetriever: recency-weighted.

### Q35: What is a vector database?
**Answer:** Stores and searches embeddings using vector similarity (cosine, dot product, L2). Index types: IVF (inverted file), HNSW (hierarchical navigable small world), DiskANN. Examples: Pinecone (managed), Weaviate, Milvus, Qdrant, Chroma (embedded). CRUD + metadata filtering + hybrid search.

### Q36: LangChain document loaders and text splitters?
**Answer:** Loaders: TextLoader, PyPDFLoader, WebBaseLoader, CSVLoader, S3FileLoader, etc. Splitters: RecursiveCharacterTextSplitter (recommended - split by `\n\n`, `\n`, `.`, character), CharacterTextSplitter (fixed size), TokenTextSplitter (token-aware), MarkdownHeaderTextSplitter, SemanticChunker (embedding-based).

## RAG (Q201-Q280)
### Q37: What is RAG? Full pipeline.
**Answer:** Retrieval-Augmented Generation. (1) Indexing: documents → chunk → embed → store in vector DB. (2) Retrieval: query → embed → similarity search → retrieve top-k chunks. (3) Generation: augment prompt with retrieved chunks → LLM generates grounded answer. Benefits: factual accuracy, cites sources, up-to-date, reduce hallucination.

### Q38: Chunking strategies for RAG?
**Answer:** Fixed-size (n tokens) - simple but can split content mid-sentence. RecursiveCharacterTextSplitter - splits at natural boundaries, best general choice. Semantic chunking - split when embedding similarity drops, better quality but slower. Agentic chunking - LLM decides chunk boundaries. Optimal depends on content type and use case.

### Q39: Hybrid search - how does it work?
**Answer:** Combines dense (vector similarity) + sparse (keyword BM25) retrieval. Dense finds semantically related, sparse finds exact matches. Fusion algorithms: Reciprocal Rank Fusion (RRF) - rank-based, simple. Weighted sum of scores. Results more robust than either alone. Supported by Milvus, Weaviate, Pinecone.

### Q40: Re-ranking in RAG?
**Answer:** Two-stage: (1) fast retrieval (bi-encoder) of top-k (100). (2) expensive re-ranking (cross-encoder) of top-k' (10). Cross-encoder jointly encodes query + document pair for relevance score. Slower but more accurate. Improves RAG quality significantly. You contributed Milvus reranking to Agno framework.

### Q41: RAG evaluation - how to measure quality?
**Answer:** RAGAS framework metrics: (1) Context precision - are retrieved chunks relevant? (2) Context recall - enough information in chunks? (3) Faithfulness - answer grounded in context? (4) Answer relevancy - answer addresses query? (5) Answer correctness - factual accuracy. Also: hit rate, MRR (Mean Reciprocal Rank), NDCG for retrieval.

### Q42: Advanced RAG techniques?
**Answer:** (1) RAPTOR: build hierarchical summary tree over documents. (2) CRAG: correct retrieval with web fallback. (3) Self-RAG: LLM reflects on retrieved docs (relevant/supported/not). (4) RAG-Fusion: multi-query generation + reciprocal rank fusion. (5) Agentic RAG: agent decides retrieval strategy dynamically.

## Agno Framework (Q281-Q300)
### Q43: What is Agno? How is it different from LangChain?
**Answer:** Agno is a lightweight framework for building multi-modal AI agents. Key differences: agent-first design (not chain-focused), simpler API, built-in multi-modal support (text, images, audio), native function calling, Milvus integration (with your reranking contribution), proxy support (your contribution). More Pythonic, less abstraction layers than LangChain.

### Q44: Agno agents - how do they work?
**Answer:** Define agent with model, tools, memory, knowledge base. Agent = Agent(model=OpenAIChat(), tools=[search_web, calculator], knowledge=KnowledgeBase(vector_db=MilvusStore()), memory=Memory()). Agent processes input, decides actions using tools, maintains conversation memory. Supports streaming, tool calls, multi-modal inputs.

### Q45: Your contributions to Agno?
**Answer:** (1) Milvus reranking - added cross-encoder reranking after vector search to improve RAG quality. (2) JSON filter parsing fix - corrected filter parsing for metadata filtering in Milvus. (3) Proxy configuration for Crawl4AI toolkit - enabled network proxy support for Crawl4AI in Agno. All PRs merged.

## LLM Applications (Q301-Q320)
### Q46: Building a chatbot - architecture considerations?
**Answer:** (1) Conversation memory (buffer, summary, vector store). (2) Context window management (truncate/summarize old messages). (3) Streaming response for UX. (4) Rate limiting and cost control. (5) Safety guardrails (your GuardrailZ project). (6) Fallback responses. (7) Multi-turn coherence. (8) User identification and persistent history.

### Q47: What is prompt engineering? Key techniques?
**Answer:** Designing prompts to get desired LLM output. Techniques: role assignment ("You are an expert..."), clear instructions, specific format requirements, few-shot examples, chain-of-thought, delimiter usage (###), negative instructions ("Do not..."), output structure specification (JSON schema), persona context, temperature/sampling control.
