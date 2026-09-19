# Infosys SP DSE — 100 Data Science / AI Interview Q&A

> Based on Infosys Specialist Programmer (SP) & Digital Specialist Engineer (DSE) interview experiences (HackWithInfy / on-campus / off-campus — GeeksforGeeks, Medium, LinkedIn, Reddit, DevBrainiac)
> Candidate: Aayush Gid — B.Tech E&C | Agentic AI / AI Agent / Data Science Internships | MigratorGen, ScriptVector, OpenRTL.ai, Agno Open-Source PRs | IEEE Publication (2024)
> Scope: Resume deep-dive + AI/ML/DL/NLP/GenAI/RAG/Agentic + Data Science fundamentals + Model evaluation & production. DSA, SQL/tech-stack, and HR questions are covered in separate sheets.
> Interview pattern observed: panel jumps straight into resume → deep-dives your ML/DL/GenAI/RAG projects → follows up with core ML concepts, NLP, model evaluation, prompt/RAG architecture and how you'd build/deploy AI at enterprise scale. Every line of your resume is fair game.

---

## 1. Resume Deep Dive & Projects (Q1–Q30)

**Q1: Walk me through your resume. What makes you a fit for the SP DSE role?**
A: I'm a final-year B.Tech Electronics & Communication student who has spent the last 18 months building production AI systems. I've done three AI internships — Agentic AI at Krip AI (FastAPI + LLMs + Docker + CI/CD), AI Agent Developer at Clone Futura (REST API automations + SQLite), and Data Science at NullClass (BERT/VADER chatbot). I've shipped three AI projects: MigratorGen (LLM-based code migration), ScriptVector (Agno agent content generator), and OpenRTL.ai (LLM-driven Verilog generation). I've contributed merged PRs to the Agno framework (Milvus reranking, JSON filter fix, Crawl4AI proxy), published an IEEE paper on real-time face mask detection, and was an SIH 2024 finalist. This maps directly to the DSE role: Python, GenAI/RAG/agents, data pipelines, and enterprise-grade engineering.

**Q2: Tell me about MigratorGen — what problem does it solve?**
A: When a library releases a new major version, downstream developers must manually read changelogs and rewrite import/call sites. MigratorGen automates this by parsing the library's JSON/Markdown changelog, extracting structured migration steps with an LLM parser, and generating a "migrator package" (codemod) that uses LibCST to rewrite the user's code safely — supporting both upgrades and downgrades from the CLI.

**Q3: How does the LLM-based parser work? Why do you need an LLM to parse changelogs?**
A: Changelogs are unstructured prose — "the `foo` parameter is deprecated, use `bar` instead" — with no standard schema, so regex/rules always miss edge cases. I prompt the LLM with a strict JSON output schema (change type: rename/remove/new parameter/behavior change; old API; new API; migration snippet; applies-to version range). Pydantic validates the structured output, and I used few-shot prompting with real changelog examples. The LLM handles paraphrase variability that a parser cannot.

**Q4: Why LibCST instead of Python's built-in AST module or regex?**
A: The built-in `ast` module cannot round-trip: it loses comments, formatting, and string quotes, so rewriting with it corrupts the user's file. LibCST preserves full fidelity — the syntax tree is immutable and position-aware, so what I don't change stays byte-for-byte identical. Regex is brittle for nested/balanced constructs like function signatures. Migration tools must be non-destructive, so lossless CST editing is the right tool.

**Q5: How does LibCST differ from the ast module?**
A: LibCST produces a concrete syntax tree that keeps every token, whitespace, and comment, and supports `CSTTransformer.leave_*` to rewrite nodes and re-serialize losslessly. Python's `ast` produces an abstract syntax tree that drops most source-level detail and cannot be reliably written back. LibCST is the standard for codemods (used by Instagram/OpenRewrite-style tools) precisely because it round-trips.

**Q6: What does a "migrator package" contain and how is it generated?**
A: It's a self-contained codemod module: (1) the target library + version range, (2) a list of structured migration rules from the LLM parser (old→new import path, renamed function, changed signature, moved module), (3) a LibCST transformer implementing each rule, and (4) a test file with before/after fixtures. The generator scaffolds these from the parsed changelog so one library update produces a reusable, testable migrator.

**Q7: How did you ensure migrated code is correct? How did you test MigratorGen?**
A: Three layers: (1) unit tests — pytest over each rule type (rename, remove param, add param, move import, 50+ cases including nested calls and edge cases), (2) round-trip verification — the output re-parses with LibCST and `ast.parse` without error, and (3) integration tests — migrating a real small codebase and running its test suite to confirm behavior is unchanged. I also snapshot-compare "old file → migrated file" fixtures.

**Q8: What were the hardest challenges in code migration?**
A: (1) LLM hallucinating migration steps — fixed with strict JSON schema, Pydantic validation and few-shot examples. (2) Version-conditioned rules — a change in v3 vs v4 must apply only to the right range. (3) Nested/ambiguous call sites — `foo(a, b=c)` where `b` is renamed needs argument-name matching, not position. (4) Pathological code (decorators, nested imports, stringified code) — needs targeted transformer rules. (5) Losing formatting — solved by LibCST's fidelity.

**Q9: Why did you combine LLM extraction with a deterministic engine instead of pure AI rewriting?**
A: Deterministic, testable transformations on the CST guarantee correctness and reproducibility (no surprises per-run); the LLM is used only where ambiguity lives — understanding human changelog prose. This hybrid (LLM for parsing, rules for rewriting) is far safer in production than letting the model rewrite source directly, which risks silent corruption.

**Q10: Tell me about ScriptVector — the Hindi Manhwa Content Generator. How is it architected?**
A: It's an AI content-generation system that produces long-form Hindi manhwa content. Pipeline: an Agno agent (using Gemini API) generates the narrative; automation pipelines produce chapters/segments in sequence; every generated chunk is stored in SQLite with metadata (chapter index, character state, plot context) so later generations stay contextually consistent. It's built as Python services, not a one-shot script.

**Q11: How do you use Agno agents in ScriptVector?**
A: I model the content pipeline as agents with tools: a planner agent that decides the next narrative arc, a writer agent that generates the actual Hindi prose with Gemini, and a continuity agent that reads the SQLite context store before each chapter. Agno gives me structured agents + tools + memory without the heavy orchestration boilerplate of other frameworks. Because I contribute to it, I know the internals well.

**Q12: How do you maintain contextual continuity in AI outputs using SQLite?**
A: LLMs are stateless per call. I persist a "state store" in SQLite: table of characters, locations, plot events, and a summary of each prior chapter. Before generating the next chapter, the system embeds the relevant state into the prompt (retrieving recent events/characters), so the new chapter references earlier ones. This is essentially long-term memory — like RAG over the story's own history. SQLite is the right fit: single-writer, zero-config, embedded.

**Q13: Why Gemini API here instead of OpenAI? What made you choose it?**
A: I picked Gemini mainly for stronger multilingual/Hindi generation quality and a generous free tier for prototyping, plus its long context window for feeding previous-chapter summaries. I've also used the OpenAI API (MigratorGen's parser). I discuss selection honestly: for generic long-form Hindi content, Gemini performed better out-of-the-box; cost and context were the deciding factors — I compare both APIs on real samples before choosing.

**Q14: How does your long-form content automation pipeline work?**
A: It's a scheduling/state pipeline: a controller runs the generation loop — fetch next pending chapter + context → planner agent → writer agent → validate (length, no dangling references, language check) → write to SQLite → update state → proceed. It runs unattended for many chapters, with retries, and appends to a log. This is the same "automation workflow" pattern I used at Clone Futura (Python + REST APIs + DB).

**Q15: What breaks in autonomous long-form generation, and how did you handle it?**
A: (1) Plot drift — characters/events forgotten; fixed with the SQLite continuity state. (2) Repetitive/Hallucinated content — temperature tuning + validation rules. (3) Length/format drift — post-generation checks that reject and regenerate. (4) Inconsistency of names across languages — a normalization map. (5) Cost blowup — every generation is audited and cached. This mirrors how you'd design any production LLM pipeline.

**Q16: Tell me about OpenRTL.ai — an RTL project generator.**
A: OpenRTL.ai automates the "write → verify → analyze" flow for digital design. The user describes a module in natural language; Gemini generates Verilog; then open-source tools run the checks: Verilator lints, Yosys synthesizes, and netlistsvg renders a schematic. A Streamlit UI gives folder setup, RTL metrics (module hierarchy, line counts, port counts), and visualization. It's a strong demonstration of integrating LLMs with deterministic industry tools.

**Q17: What exactly is the LLM's role in Verilog generation, and how do you keep output valid?**
A: The LLM produces the Verilog module from a prompt (spec + port conventions + style guide); the tricky part is that LLM Verilog is frequently syntactically wrong or unsynthesizable. So I wrap it: post-generation I run Verilator lint; failures are fed back to the LLM as error messages for repair iterations (self-correction loop). Only code that lints clean proceeds to synthesis. Deterministic tools are the ground truth, the LLM is the generator+fixer.

**Q18: How do Yosys and Verilator fit into the pipeline? What do they do?**
A: Verilator is a fast simulator/linter: it compiles Verilog to C++/SystemVerilog for simulation and flags lint errors, so I use it as the first correctness gate. Yosys performs logic synthesis: it maps RTL to a netlist (technology-independent first, then to a target library), letting me report metrics like gate count and confirm the design is synthesizable. Together they give verify + synthesize in one flow.

**Q19: What is netlistsvg and how do you produce the schematic visualization?**
A: netlistsvg converts a synthesized netlist (JSON format) into an SVG schematic diagram of the logic — gates, wires, ports. In OpenRTL.ai, after Yosys synthesis I extract the netlist JSON and feed it to netlistsvg to render, so the user sees both the Verilog and the actual hardware structure. This closes the loop between generated code and visual hardware representation.

**Q20: What RTL metrics do you compute and why are they useful?**
A: Module hierarchy depth, number of modules/instances, port and wire counts, line counts per module, and basic combinational/logic gate estimates post-synthesis. These give a developer a quick health check — is the generated architecture flat (bad) or hierarchical (good), how big is the design, where is complexity concentrated. Metrics make the AI output explainable and comparable.

**Q21: Tell me about your open-source contributions to Agno. What was the Milvus reranking PR?**
A: I contributed three merged PRs to the Agno framework. The Milvus PR added reranking support to the Milvus vector-store integration: after retrieving top-k candidates by vector similarity, the results are re-scored with a reranker (e.g., cross-encoder) to improve relevance precision before returning. This is the standard "retrieve broadly, rerank precisely" pattern in production RAG.

**Q22: What is reranking and why is it needed in RAG?**
A: A bi-encoder embedding model retrieves candidates by approximate cosine similarity — fast but coarse. A reranker (cross-encoder) scores query–document pairs jointly and is far more accurate, so the pipeline retrieves top 50 by vector search, then reranks to the best top 5. It trades a little latency for a large precision gain and is the highest-leverage improvement in most RAG systems. My Milvus PR enabled exactly this inside Agno's store.

**Q23: What was the JSON filter parsing bug you fixed, and how did you debug it?**
A: Agno's vector store supports metadata filters passed as JSON (e.g., `{"field": "category", "operator": "eq", "value": "docs"}`). Nested or compound filters (multiple conditions / operators like `in`, `not_eq`, `and/or` trees) were parsed incorrectly, silently dropping or misapplying conditions. I reproduced with a failing test, fixed the parser to walk the JSON tree correctly and map each condition to the store's filter syntax, and added regression tests covering nested filters.

**Q24: What is the Crawl4AI proxy configuration PR you merged?**
A: I added proxy configuration support to Agno's Crawl4AI toolkit. Crawl4AI is the web-scraping-tool agent integration; without proxy support, agents scraping from restricted environments (corporate networks, geo-limited sites, rate-limited sources) would fail. The PR exposes proxy settings so agent web scraping goes through a configured proxy — enabling privacy and IP rotation.

**Q25: What did you learn from contributing to a framework like Agno?**
A: (1) Reading a real codebase's abstractions before coding — matching their style and extension points. (2) Writing tests that a maintainer will actually merge — every PR included regression tests and docs. (3) Asynchronous, maintainer-driven review — iterating on feedback, rebasing, keeping PRs small and focused. (4) Deepening my RAG/vector-store fundamentals, which directly powered my project work. It's also a strong interview story: my code runs in a widely used framework.

**Q26: Walk me through your Krip AI intern work. What was the stack?**
A: At Krip AI I built Python AI applications on LLM APIs, exposed them as FastAPI backend services, and wired them into automation workflows. I implemented CI/CD with GitHub Actions (lint → test → build Docker image → push to registry → deploy) and containerized the services with Docker, so every endpoint had reproducible builds and automated deployment. This is where I internalized production engineering around AI.

**Q27: How did you design a FastAPI backend around an LLM at Clone Futura?**
A: I built backend services where authenticated endpoints wrap third-party API automation workflows and persist state in SQLite. Request flow: `/auth` with token-based or API-key auth (secure headers), a service layer that calls the third-party REST API, result stored in SQLite with status tracking, then responses returned as JSON. Auth, validation, error handling and idempotency were the focus because automation runs unattended.

**Q28: Explain the NullClass chatbot: BERT + VADER. How do the two models work together?**
A: VADER is the fast, lexicon-based sentiment scorer (intensity of positive/negative/neutral); BERT (fine-tuned for classification) captures nuanced, syntax-aware sentiment. The chatbot classifies intent and sentiment: VADER gives a lightweight first-pass score, BERT handles ambiguous, sarcastic, or domain text, and results feed the response logic and a Streamlit dashboard for real-time analytics of user sentiment.

**Q29: What did your IEEE "Real-Time Face Mask Detection" paper actually solve?**
A: It's a distributed ML system for enterprise healthcare — detecting whether people are wearing masks, in real time. I focused on a CNN (transfer-learned from a pretrained model) with advanced preprocessing — augmentation, lighting normalization, and optimized data pipelines — and tuned the model for low-latency inference suitable for real-time surveillance/cameras. The paper documents the distributed training and optimization approach.

**Q30: How would you defend the performance/evaluation methodology of your models?**
A: For every model I keep the full evidence: the dataset split (train/val/test), the metric chosen and why (e.g., F1 for imbalanced classes, per-class precision/recall for the mask classes), confusion matrix, and ablation (with/without preprocessing/augmentation). For the LLM projects, evaluation is different — fixture-based goldens and human review. I can always justify why a metric fits the business problem rather than quoting a number.

---

## 2. Data Science & Machine Learning Fundamentals (Q31–Q55)

**Q31: What is the difference between AI, ML, DL, and Generative AI?**
A: AI is the broad field of machines mimicking intelligence. ML (a subset of AI) learns patterns from data instead of being explicitly programmed. DL (subset of ML) uses multi-layer neural networks to learn representations automatically. GenAI (subset of DL) generates new content (text, images, code) from learned distributions — LLMs like Gemini/GPT are GenAI. My work spans ML (mask detection, sentiment) and GenAI (RAG, agents, content generation).

**Q32: Walk me through the full data science lifecycle (CRISP-DM).**
A: (1) Business understanding — define the problem and success metric. (2) Data understanding — EDA: distributions, missing values, outliers, correlations. (3) Data preparation — cleaning, feature engineering, encoding, split. (4) Modeling — baseline → candidate models → tuning. (5) Evaluation — metrics vs business goal, error analysis. (6) Deployment & monitoring — API, drift tracking, retraining. In interviews they often ask you to draw this with ETL specifics — know each stage's concrete deliverables.

**Q33: What is ETL and how is it different from ELT?**
A: ETL = Extract, Transform, Load: you extract from sources, transform/clean in a staging layer, then load into the warehouse — good when transformations need to happen before storage and storage is expensive. ELT = Extract, Load, Transform: you load raw data into the warehouse first, transform in place with warehouse compute (dbt, Spark) — the modern pattern because cloud warehouses are cheap and powerful. For DS work the practical difference is where/when you clean, dedupe, type-cast, and join.

**Q34: What is the difference between structured, unstructured, and semi-structured data?**
A: Structured = rows/columns with fixed schema (SQL tables, match my PostgreSQL/SQLite work). Unstructured = no fixed schema (text, images, audio, video). Semi-structured = has tags/keys but no rigid schema (JSON, XML, Markdown changelogs). My projects cross all three: changelog Markdown (semi/unstructured) parsed into structured migration rules, content stored in SQLite, Verilog (text).

**Q35: Supervised vs unsupervised vs reinforcement learning — explain with examples.**
A: Supervised learns labeled input→output mappings (face mask classification, sentiment analysis, churn prediction). Unsupervised finds structure in unlabeled data (customer segmentation via K-Means, association rules). Reinforcement learning learns by reward/punishment from action feedback (AlphaGo, robotics). Real systems often combine them (unsupervised clustering as a feature for a supervised model).

**Q36: Regression vs classification — how do you decide, and what overlaps?**
A: Regression predicts a continuous value (house price, revenue forecast); classification predicts a discrete class (fraud/not-fraud, sentiment positive/negative/neutral). You decide by the business answer you need. Overlap: both need the same preprocessing pipeline; logistic regression is a classifier despite the name; you can bin a regression target to classify (and the reverse). 

**Q37: What is overfitting and underfitting? How do you detect and fix both?**
A: Overfitting = model memorizes training data, low train error, high validation error (high variance). Underfitting = model too simple, high error on both train and validation (high bias). Detection: gap between training and validation metrics, learning-curve analysis. Fixes for overfitting: more data, regularization (L1/L2), dropout, early stopping, simpler model, cross-validation. Fixes for underfitting: more features/complexity, more epochs, stronger model. Every modeling question should mention the train/val gap signal.

**Q38: Explain the bias-variance tradeoff.**
A: Bias = error from oversimplifying assumptions (model can't capture the pattern). Variance = error from sensitivity to training-data fluctuations (model chases noise). Total error = bias² + variance + irreducible noise. Simple models = high bias/low variance; complex models = low bias/high variance. The goal is the sweet spot of minimum total error — why we use regularization, ensembles, and proper validation to tune complexity.

**Q39: Why do you split data into train, validation, and test sets?**
A: So you can select and honestly evaluate. Train sets model weights; validation tunes hyperparameters and detects overfitting during development; test gives an unbiased estimate of real-world performance, used only once at the end. Without a held-out test set, tuning on the same data the model saw leaks information and your reported accuracy is optimistic. Time-based splits matter for time-series data.

**Q40: What is k-fold cross-validation and when do you use it?**
A: Split data into k folds; train on k−1, validate on the remaining fold, rotate k times, average the metric. It uses all data for both training and validation, giving a more stable estimate with small datasets. Use it to tune hyperparameters or compare models, then retrain on the full data with best params. Leave-one-out is k-fold with k=N. I'd use it for the mask-detection/sentiment training to be robust to dataset division.

**Q41: L1 vs L2 regularization — how do they differ?**
A: Both add a penalty to the loss to shrink weights. L2 (Ridge, sum of weight²) shrinks weights toward zero smoothly — good when all features carry some signal. L1 (Lasso, sum of |weight|) drives some weights to exactly zero — feature selection, sparse models. Elastic Net combines both. In Keras you add them via `kernel_regularizer`; with enough features both reduce overfitting, L1 helps interpretability.

**Q42: Feature engineering vs feature selection vs feature extraction — what's the difference?**
A: Feature engineering = creating new informative features from raw data (from my paper: lighting normalization, region-based inputs). Feature selection = choosing a subset of existing features (filter methods, wrapper, embedded like L1/Lasso — also used in the SIH/attrition project with ANOVA/chi-square style selection). Feature extraction = transforming to a lower-dimension space (PCA, embeddings, TF-IDF). All three combat the curse of dimensionality and improve model quality.

**Q43: Standardization vs normalization — when do you use each?**
A: Standardization (z-score) shifts to mean 0, std 1 — needed for distance-based and gradient-based models (SVM, KNN, neural networks, linear models). Normalization (Min-Max) scales to [0,1] or [-1,1] — useful when bounded inputs matter or for some image data. Tree-based models don't care about scaling. Decide by model type; keep the scaler fit on train only and apply to test (avoid leakage).

**Q44: How do you handle missing data?**
A: First understand why it's missing (MCAR/MAR/MNAR) — that decides everything. Options: (1) drop rows (ok if few, but loses data), (2) drop columns (if >50–60% missing), (3) impute — mean/median (median is robust to outliers), mode for categorical, KNN imputation, model-based imputation, or a constant + flag column, (4) for time series, forward-fill/backward-fill/interpolation. Always compare against a baseline. In my mask-detection pipeline I used augmentation + preprocessing to reduce data sensitivity rather than naive deletion.

**Q45: Your dataset is imbalanced (e.g., fraud is 1% of rows). What do you do?**
A: Don't use plain accuracy — use precision/recall/F1/ROC-AUC. Level-1 handling: (1) resampling — SMOTE to over-sample minority, undersample majority; (2) class weights in the loss (Keras `class_weight`, sklearn `class_weight`); (3) threshold tuning — adjust the decision threshold on validation; (4) ensemble/bagging minority views; (5) framing as anomaly detection for extremes. Also collect more minority data. For production, the business metric (cost of a missed fraud vs a false alarm) sets the threshold.

**Q46: Which classification metrics do you use and why?**
A: Accuracy (overall correctness — misleading with imbalance), Precision (of predicted positives, how many were right), Recall/Sensitivity (of actual positives, how many caught), F1 (harmonic mean of precision+recall — balances both), ROC-AUC (ranking quality across thresholds, good for model comparison), PR-AUC (better than ROC for imbalanced data), plus the confusion matrix for error patterns. Choose by cost: for fraud, recall-favored thresholds; for spam that blocks mail, precision matters more.

**Q47: Explain the confusion matrix and each of its cells.**
A: Rows = actual, columns = predicted. TP = predicted positive, actually positive. FP = predicted positive, actually negative (type-1 error). FN = predicted negative, actually positive (type-2 error). TN = predicted negative, actually negative. Everything else derives: Accuracy = (TP+TN)/total; Precision = TP/(TP+FP); Recall = TP/(TP+FN); F1 = 2PR/(P+R); Specificity = TN/(TN+FP). I use the matrix for the fine-grained error analysis of the mask-detection and sentiment models.

**Q48: Regression metrics — MSE, RMSE, MAE, R² — when do you use which?**
A: MSE squares errors — penalizes large errors heavily, differentiable, gradient-friendly, but interpretable only in squared units. RMSE is MSE sqrt'd (same units as target) — standard for error magnitude. MAE is the average absolute error — robust to outliers (no squaring), interpretable. R² = variance explained (0–1), best for explaining goodness-of-fit across models. With outliers, prefer MAE over MSE/RMSE; when big errors are disproportionately bad (finance), RMSE.

**Q49: Explain gradient descent, learning rate, and the optimizers you've used.**
A: Gradient descent updates weights in the direction that reduces loss: w ← w − lr·∇L. Learning rate controls step size — too high diverges, too low trains slowly/sticks in a saddle. Variants: batch GD (all data), mini-batch SGD (batches), SGD with momentum; Adam combines momentum + adaptive per-parameter learning rates and is my default in Keras. Related: learning-rate schedules/decay, warm-up, and that loss curves tell you whether lr is wrong.

**Q50: Decision trees, Random Forest, and Gradient Boosting (XGBoost) — how do they relate?**
A: Decision tree = simple hierarchical if-else learner, high variance, prone to overfitting. Random Forest = bagging trees with feature randomness — reduces variance by averaging many decorrelated trees. Gradient boosting = sequential trees, each correcting the previous tree's residual errors — reduces bias, very strong on tabular data; XGBoost/LightGBM add regularization, pruning, and speed. Rule of thumb: boosting for best tabular accuracy, RF for robustness/noisy data.

**Q51: Explain K-Means and how you choose k.**
A: K-Means partitions data into k clusters minimizing within-cluster squared distances: initialize centroids → assign each point to nearest centroid → recompute centroids as cluster means → repeat until convergence. Choosing k: elbow method (inertia vs k), silhouette score (higher better), gap statistic, or business constraint. Sensitive to initialization (k-means++) and scale (standardize first). Use for segmentation/unsupervised exploratory analysis.

**Q52: What is EDA, and what key steps do you take?**
A: EDA is investigating data before modeling to spot problems and hypotheses: (1) shape, dtypes, head of data, (2) missing values and duplicates, (3) univariate stats — distributions, outliers (boxplots, IQR), (4) bivariate — correlations (heatmap), relationship of features to target, (5) categorical feature frequency, (6) sanity checks (negative prices, impossible dates). Output: a documented data profile that guides cleaning and feature engineering. At NullClass I built the Streamlit dashboard to make this visible in real time.

**Q53: How do you detect and handle outliers? Why do they matter?**
A: Detection: IQR (points beyond 1.5·IQR), z-score (|z|>3), boxplots, isolation forests, domain rules. Impact: distance-based models (linear regression, KNN, NN) are skewed by outliers; tree models are more robust. Handling: investigate first (is it a data error or a genuine rare case?), then winsorize/cap, transform (log), or remove if erroneous. Never remove without understanding why the value exists.

**Q54: What is multicollinearity, and does it matter?**
A: When independent variables are highly correlated (e.g., two features both encoding the same thing). It inflates coefficient variance in linear models — unstable/uninterpretable coefficients — and can confuse feature-importance. Detection: correlation matrix, VIF (>5–10). Handling: drop one of the pair, combine into one feature, or use regularization/PCA. Tree and bagging models tolerate it fine; linear/interpretable models care.

**Q55: Data drift vs concept drift — what's the difference and what do you do?**
A: Data drift: the input distribution changes (new customers, different traffic patterns) — P(X) changes. Concept drift: the relationship between input and target changes (same signals no longer predict churn) — P(Y|X) changes. Detection: monitoring feature distributions (PSI/KS), retrain/refresh model, monitor predictions. This is why a deployed model needs monitoring — the model valid at deploy time degrades silently as the world changes.

---

## 3. NLP & Text Analytics (Q56–Q68)

**Q56: What is NLP, and where does it appear in your projects?**
A: NLP is giving computers the ability to understand and generate human language. It spans text preprocessing, classification, sentiment, NER, embeddings, and generation. It's everywhere in my resume: sentiment analysis with BERT/VADER at NullClass, the LLM parser on changelogs in MigratorGen, and multilingual Hindi content generation in ScriptVector.

**Q57: What does a text preprocessing pipeline look like?**
A: Raw text → lowercase → remove noise (URLs, HTML, emojis, special chars) → tokenization (split into tokens; sub-word tokenization for BERT) → remove stop words (heuristic, careful not to strip meaning in tasks like sentiment) → stemming (crude — "playing"→"play") or lemmatization (dictionary-aware — "better"→"good") → handle negation ("not good" ≠ "good"). The exact steps depend on the task and model; modern DL models often skip heavy preprocessing because sub-word tokenization handles morphology.

**Q58: Bag-of-Words vs TF-IDF — differences and limitations?**
A: BoW counts word frequency in a sparse vector — simple, but ignores importance and counts stop words heavily. TF-IDF weights each term by frequency weighted against how common it is across documents (term frequency × inverse document frequency) — so rare, informative words get high weight. Limitations of both: no word order/semantics, huge sparse vectors, no out-of-vocabulary handling. Embeddings/transformer models fix these — which is why BERT and embedding-based models came next.

**Q59: What is a word embedding, and why is it central to NLP/AI now?**
A: An embedding maps tokens to dense vectors where semantic similarity ≈ vector distance (king − man + woman ≈ queen). Unlike BoW, they capture meaning. Embeddings power everything today: text embeddings for RAG/vector search (Milvus), token embeddings inside transformers, and multilingual embeddings that map Hindi and English near each other. Why it matters for my projects: RAG relies entirely on embedding similarity for retrieval.

**Q60: Explain BERT. Why is it bidirectional?**
A: BERT (Bidirectional Encoder Representations from Transformers) is a transformer encoder pretrained on masked-language modeling (predict masked tokens using both left and right context) and next-sentence prediction. Bidirectionality means each token attends to all other tokens on both sides — so "bank" is disambiguated by the whole sentence ("river bank" vs "bank loan"). For sentiment classification, the [CLS] token's final representation is fed to a classifier head, fine-tuned on labeled data.

**Q61: How does BERT represent input text?**
A: WordPiece sub-word tokenization (unknown words split into known subwords — key for OOV). Each token gets: (1) token embedding, (2) segment embedding (sentence A/B), (3) position embedding. Special tokens: [CLS] at start, [SEP] between/after sentences. Input includes attention masks (1 for real tokens, 0 for padding). Output: hidden states per token + pooled [CLS] vector, used for classification, NER, QA.

**Q62: How do you fine-tune BERT for a downstream task like sentiment?**
A: Start from pretrained BERT (Keras/HuggingFace), replace the head with a small task-specific classifier over the [CLS] representation, and train with a small learning rate (2e-5–5e-5) for few epochs on labeled data. Only the head and top layers change much; lower layers keep general language knowledge. Use a validation set for early stopping. This is transfer learning — I did exactly this class of fine-tuning for the NullClass chatbot.

**Q63: What is VADER and when is it appropriate to use?**
A: VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon + rule-based sentiment model: a curated dictionary of words with polarity scores plus rules for intensifiers, negations ("not good" flips polarity), emoticons, ALL-CAPS, and punctuation. Pros: fast (no training/inference cost), works out-of-the-box on short informal text and social media. Limits: no deep context, sarcasm, or domain nuance. Right tool when you need cheap, transparent, real-time scoring on short text — I used it as the lightweight path in the NullClass chatbot.

**Q64: VADER vs BERT for sentiment — how do you choose?**
A: VADER: no training, instant, great for short informal text, but shallow — fails on sarcasm, negation-heavy long text, domain slang. BERT (or any transformer): deep contextual understanding, handles syntax and nuance, domain-adaptable by fine-tuning — but needs labeled data, compute, and slower inference. In the NullClass chatbot I used both: VADER as a fast first-pass filter and BERT for the ambiguous cases — a classic tiered design that balances cost and accuracy.

**Q65: What are the hardest challenges in sentiment analysis?**
A: (1) Sarcasm/irony — the literal words say the opposite of intent. (2) Negation and scope — "not bad" vs "not very good". (3) Domain/context — "sick" is negative in health, positive in slang. (4) Product-aspect vs overall sentiment — "the movie was boring but the songs were great" needs aspect-level. (5) Code-mixing and informal language. (6) Label subjectivity and annotation noise — two human annotators often disagree, so evaluate on agreement-based labels.

**Q66: Besides classification, what other NLP tasks matter?**
A: NER (named-entity recognition — people, orgs, dates; used to extract migration targets or customer entities), part-of-speech tagging, dependency parsing, question answering, text summarization, machine translation, language modeling, text generation, topic modeling (LDA), and slot filling/entity extraction for conversational AI (my chatbot had to extract intents/entities). Enterprise DS work is full of these — entity extraction powers RAG metadata and automation rules.

**Q67: How do you evaluate a text classification / NLP model?**
A: Same core metrics as any classifier — for sentiment: per-class precision/recall/F1, macro vs weighted F1, confusion matrix to see which classes (e.g., neutral) are confused. Plus: cross-fold stability, a held-out test set never tuned on, and error analysis on misclassified examples to find systematic failures. For generative/NLU components, different evals: intent accuracy, entity extraction F1, and end-to-end task success — not just token accuracy.

**Q68: How do you handle multilingual / code-mixed text like Hindi-English?**
A: Challenges: Devanagari vs Latin script, code-switching mid-sentence (Hinglish), transliteration variance (same word spelled differently). Approaches: (1) use multilingual models (mBERT, multilingual embeddings, Gemini/GPT) that map languages into shared space, (2) transliterate everything to a common script (Indic transliteration), (3) per-language preprocessing and normalization maps (my ScriptVector uses a name/spelling normalization map), (4) prompt the model to follow the user's language, (5) evaluate per language separately. This was a real, recurring problem in the Hindi manhwa generator.

---

## 4. Deep Learning (Q69–Q78)

**Q69: Explain how a neural network learns, from a single neuron up.**
A: A neuron computes z = W·x + b and applies an activation. Stacking layers with non-linear activations lets a network represent complex functions. Learning = forward pass (predictions) → compute loss → backpropagate gradients → update weights with an optimizer. Depth matters: hidden layers learn progressively abstract features (edges→shapes→objects in CNN image tasks). This is the foundation behind every Keras/TensorFlow model I trained.

**Q70: Which activation functions do you use and when?**
A: ReLU (default for hidden layers — cheap, avoids vanishing gradient, but "dying ReLU" risk), LeakyReLU (fixes dying ReLU), sigmoid (output for binary classification, squashes to 0–1), tanh (zero-centered, good in RNN gates for some cases), softmax (output for multi-class — turns logits into a probability distribution summing to 1). Hidden activations must be non-linear or stacked layers collapse into one linear function.

**Q71: How do you choose a loss function?**
A: Match it to the task: binary cross-entropy for two classes (sigmoid output); categorical cross-entropy for multi-class (softmax output); sparse categorical CE when labels are integers; mean squared error for regression; contrastive/margin losses for embeddings. For RAG relevance you optimize retrieval metrics, not CE. In Keras you pass `loss=` on `compile()`. My face-mask model used categorical CE (Mask/NoMask/Incorrect classes); sentiment used categorical CE too.

**Q72: Explain backpropagation intuitively.**
A: Backpropagation computes, via the chain rule, how much each weight contributed to the error, then updates so the network reduces loss. Forward pass computes predictions; backward pass propagates the gradient of the loss from output back to weights through every layer; optimizer applies w −= lr·grad. That's why activation derivatives and stable gradients matter — saturated sigmoids kill gradients (why we use ReLU, BatchNorm, and skip connections).

**Q73: Explain CNNs — convolution, pooling, and why they work for images.**
A: A CNN treats an image as a 2D grid. Convolution applies small learnable filters (kernels) that slide over the image extracting local patterns — edges, then shapes, then object parts — via shared weights (translation invariance, far fewer parameters than a fully connected net). Pooling (max/avg) downsamples and adds translation robustness. Early layers learn low-level features, later layers combine them into semantic features. That's exactly why I used a CNN for face-mask detection.

**Q74: Why use a CNN instead of a plain feedforward network for images?**
A: A fully-connected net flattens a 224×224 image to ~150k inputs, exploding parameters, and ignores spatial locality — a pixel 100px away matters as much as the neighbor. CNNs exploit spatial structure: shared convolution weights (few parameters), local receptive fields, pooling for scale invariance, and learnable hierarchical features. They generalize far better on images with far less data.

**Q75: Explain RNNs and LSTMs. Why do sequence models have trouble with long sequences?**
A: RNNs process sequences step-by-step carrying a hidden state — but naive RNNs suffer the vanishing-gradient problem: gradients shrink over many steps, so long-range dependencies (the start of the sentence changing the meaning at the end) are forgotten. LSTM adds gated memory: input gate, forget gate, output gate, and a cell state that can carry information across many steps with an additive path (gradients flow more easily) — so it remembers long-term context. That's why LSTM-based sequence models are used for temporal signals.

**Q76: What is transfer learning, and how did you use it in your projects?**
A: Transfer learning = take a model pretrained on a large generic dataset and adapt it to your smaller task: keep the learned feature extractor, replace the head, fine-tune with a low learning rate. Benefits: needs less data, trains faster, higher accuracy. I used it in the face-mask detection paper (pretrained CNN backbone → mask classifier) and in BERT-style fine-tuning for sentiment. This is the standard way to get good results with limited domain data.

**Q77: Walk me through a Keras/TensorFlow training workflow and the key hyperparameters.**
A: Data preprocessing (resize, normalize, augment, train/val split) → build `Sequential`/`Functional` model → `compile(loss=..., optimizer=Adam, metrics=[...])` → `fit` with `epochs`, `batch_size`, `validation_data`, callbacks (`EarlyStopping` on val loss, `ModelCheckpoint` for best weights, `ReduceLROnPlateau`) → evaluate on the held-out test set → export (SavedModel/TFLite). Key knobs: learning rate, batch size, epochs, number of layers/units, dropout, regularization, data augmentation.

**Q78: What is data augmentation and why is it effective?**
A: Data augmentation generates new training samples by applying realistic transformations to existing ones — rotation, flipping, scaling, brightness/contrast shifts for images; synonym replacement, back-translation, noise injection for text. It improves generalization by teaching the model invariance (a rotated face is still a face) and reduces overfitting when data is scarce. In the mask-detection paper I combined augmentation with normalization preprocessing to make the distributed model robust across camera/lighting conditions.

---

## 5. GenAI, LLMs, RAG & AI Agents (Q79–Q92)

**Q79: Explain how an LLM works at a high level.**
A: LLMs are transformer-based neural networks trained to predict the next token given previous tokens, over enormous text corpora. The transformer uses self-attention — every token computes how relevant every other token is (Q/K/V) — giving deep bidirectional context. At inference you prompt it and it autoregressively generates tokens one by one. Scale + data gave the emergent abilities (reasoning, few-shot learning). Fine-tuning/instruction-tuning (RLHF) makes outputs follow instructions. That's the machinery behind Gemini/GPT I use in my projects.

**Q80: What is tokenization, and why does token count matter?**
A: Tokenization converts text into token IDs the model consumes, using algorithms like BPE/WordPiece (sub-word units). It matters for three reasons: (1) cost — APIs bill per token, (2) latency — more tokens = longer generation, (3) context limits — every token counts against the window. Some languages (including Hindi/Devanagari) split into more tokens than English for the same meaning, a practical consideration in ScriptVector's pipeline and budget.

**Q81: What are the key generation parameters you control?**
A: Temperature — randomness (low = focused/deterministic for factual tasks, high = creative; I keep 0.1–0.3 for extraction). top_p — nucleus sampling: only sample from the most probable tokens cumulatively reaching p. max_tokens — caps output length. presence/frequency_penalty — reduces repetition (used in long-form ScriptVector generation). stop sequences — end generation at markers. structured output/schema — force JSON. Choosing these per task is real engineering — they directly shaped MigratorGen's consistent JSON and ScriptVector's non-repetitive prose.

**Q82: What are zero-shot, few-shot, and chain-of-thought prompting?**
A: Zero-shot — no examples, just instructions ("extract migration steps as JSON"). Few-shot — include a handful of labeled examples in the prompt to show format/behavior (I used few-shot with real changelogs in MigratorGen). Chain-of-thought — ask the model to reason step-by-step before answering, improving accuracy on multi-step tasks at the cost of tokens/latency. Also relevant: self-consistency (sample multiple CoT paths, vote), and role/system prompts.

**Q83: What is RAG? Walk me through the complete pipeline.**
A: RAG (Retrieval-Augmented Generation) grounds the LLM in external data to answer from facts instead of memory. Pipeline: (1) Ingestion — load docs, parse (Markdown changelogs, PDFs, mixed content), (2) Chunking — split into retrieval-sized pieces with overlap/metadata, (3) Embedding — encode chunks into vectors, (4) Index — store in vector DB (Milvus) with an ANN index like HNSW, (5) Retrieval — embed the query, top-k similarity search, optionally rerank with a cross-encoder (my Agno PR!), (6) Generation — put retrieved context + query in the prompt, LLM synthesizes the grounded answer. It fixes hallucination staleness (live updates) and private data access.

**Q84: What is a vector database, and why Milvus? How does vector search work?**
A: A vector DB stores embeddings and answers "which vectors are most similar to this one?" using approximate nearest-neighbor (ANN) indexing — HNSW (graph-based, fast/accurate), IVF (inverted file clustering), or flat exact scan. I picked Milvus for Agno because it's open-source, scales horizontally, supports metadata filtering (relevant to my JSON-filter PR) and reranking, and integrates with LangChain-style tooling. Search quality is measured by recall@k vs cost, and I evaluate embedding model + index together.

**Q85: How do you choose a chunking strategy?**
A: Depends on document structure. Fixed-size chunks (simple, uniform, can split sentences mid-thought); overlapping chunks (avoid losing boundary context); recursive/semantic chunking (split on natural boundaries — Markdown headers, paragraphs, sentences); document-aware chunking for tables/code (my changelog/Markdown case!). Best chunk size balances retrieval precision (too big = diluted embeddings) vs context (too small = missing surrounding context). The practical approach is empirical — evaluate retrieval hit-rate, not intuition. Reranking is a strong fix for imperfect chunking, which is part of why I implemented it in Agno.

**Q86: What is "lost in the middle" and how do you handle it?**
A: LLMs use the beginning and end of a long context best; information buried in the middle is often ignored — so RAG retrieval that packs 20 chunks in the middle fails on answers found mid-context. Mitigations: put the most relevant chunk first, limit/rerank context to the top 5 truly relevant chunks (breadth→precision), restructure the prompt to front-load answers, or use maps/reduce or summary trees for long docs.

**Q87: How do you evaluate a RAG system?**
A: Separate retrieval from generation. Retrieval: retrievability — can the answer be found at all — then precision@k/recall@k, hit-rate, and MRR over a labeled query→passage set. Generation: faithfulness (is the answer grounded in retrieved context — LLM-as-judge or token overlap), answer relevancy, and correctness vs gold answers. Frameworks like RAGAS give these as standard metrics (faithfulness, answer relevancy, context precision/recall). Plus end-to-end task completion.

**Q88: What is hallucination, and how do you prevent it?**
A: Hallucination is the model confidently generating content not grounded in the data. Mitigations: (1) RAG grounding with citations, (2) prompt constraints — "answer only from the context; say 'I don't know' otherwise", (3) low temperature, (4) structured output + validation (Pydantic), (5) self-checking/verification by a second pass, (6) reranking so irrelevant context never reaches the model, (7) guardrails and human review for high-risk outputs, (8) fine-tuning for fixed domains. In MigratorGen I added schema validation specifically to stop the parser inventing migration rules.

**Q89: RAG vs fine-tuning — when do you use which?**
A: RAG for: knowledge that changes often, private/large corpora, needs citations/traceability, no training infra — it's the default for factual grounding. Fine-tuning for: fixed style/format/behavior, latency/cost reduction on repeated patterns, domain tone — but doesn't add new knowledge and needs labeled data + infra. They're complementary: fine-tune for how to respond (style/format), RAG for what to answer (facts). Model fine-tuning (LoRA) would be the lever if ScriptVector needed a consistent voice.

**Q90: What is an AI agent? How does it differ from a plain LLM call?**
A: An LLM call is one-shot text→text. An agent wraps an LLM in a loop with tools, memory, and autonomy: it reasons, decides to call tools (function calling) — search, APIs, DB, code execution — observes the tool result, and iterates until the goal completes (ReAct pattern). Agents can plan, use external systems, and self-correct. My ScriptVector "agents" (planner/writer/continuity) and the Agno contributions (tool configs for Crawl4AI) are exactly this pattern — LLM + tools + state, not a single prompt call.

**Q91: Agno vs LangChain — what did you use and why?**
A: I chose Agno (and contributed to it) because it's minimal and model-agnostic — agents, tools, memory without the deep abstraction/chain complexity of LangChain, making the agent loop readable and debuggable. I know LangChain's ecosystem too, but for my agent-heavy projects Agno's design (tools as callables, explicit agent loop) was clearer and lighter. In an interview I describe the trade-offs honestly: LangChain wins on breadth/ecosystem, Agno wins on simplicity — and I have production code in both worlds plus merged PRs in Agno.

**Q92: What is function calling / structured output, and how do you secure tool use?**
A: Function calling = the model outputs a structured request (JSON) naming a function + arguments instead of free text — you execute it and return the result. Structured output = the model is constrained to produce JSON matching a schema (OpenAI structured outputs, Pydantic models). Security: validate schema, whitelist tools the model can invoke, sandbox any code execution, verify args against business rules (never trust a model's numbers blindly), rate-limit, log all calls, and use input/output guardrails to block prompt injection. In MigratorGen the migration rules go through Pydantic validation before any rewrite runs.

---

## 6. Model Evaluation, Testing & Productionizing ML (Q93–Q100)

**Q93: How do you evaluate an ML model after deployment?**
A: You evaluate pre-deployment (held-out test metrics, cross-validation) and then monitor post-deployment continuously: (1) performance drift — retest on a labeled rolling sample, (2) feature/data drift — distribution monitoring (KS, PSI), (3) business metrics — did churn drop / resolution improve, (4) latency/throughput/cost, (5) feedback loop — collect production outcomes as labels for retraining. A model is a product living in production, not a notebook artifact — my internships always ended with a deployed, monitored service.

**Q94: What is good A/B testing for ML/AI systems?**
A: Randomly split traffic (or sessions) between control (old model/flow) and treatment (new one), holding everything else constant, measure the same business + quality metrics, and decide with statistical significance (sample size planning, fixed horizon or sequential testing), then gradual rollout with rollback. Guard against: leakage between groups, novelty effects, peeking at results mid-test. For LLM features, evaluate both task success and cost/latency deltas.

**Q95: How do you test AI code — especially things that call LLM APIs?**
A: Same engineering discipline as any code, plus mocking: (1) unit tests for pure logic (parsers, transformers, rules) with fixtures — MigratorGen's 50+ pytest cases, (2) mock the LLM API/network layer so tests are fast, deterministic, and free, (3) golden/regression tests — fixed expected outputs for canonical inputs, (4) integration tests for the DB/service wiring (FastAPI TestClient, SQLite), (5) property/edge-case tests (empty input, huge input). Never let CI depend on live API calls or real networks.

**Q96: How do you evaluate an LLM application (not just its components)?**
A: Layered evals: (1) golden test set — prompts with expected answers, assertions on structure/containment, (2) LLM-as-judge — a strong model scores faithfulness, relevance, tone (calibrate the judge first), (3) human review on a sample — the ground truth for outliers, (4) end-to-end task metrics — did the user's goal complete, resolution rate, error rate, (5) safety/guardrail tests — prompt-injection, off-topic, hallucinated claims, (6) soft metrics — latency, token cost, retry rates. I'd build this kind of eval suite for every GenAI feature before merge.

**Q97: How does CI/CD apply to ML/GenAI projects?**
A: The standard software loop plus model-specific stages: lint/typecheck → unit + integration tests (with mocked LLMs) → data/schema validation → train/validate a candidate model (or validate prompt/embedding changes) → build & push Docker image → deploy → smoke/health checks → monitor drift/latency. At Krip AI I ran exactly this on GitHub Actions (lint → pytest → Docker build → push → deploy). For GenAI, prompt/config changes go through the same review-and-rollback pipeline, with A/B routing for prompt variants.

**Q98: What is data leakage, and why is it dangerous?**
A: Leakage = information from the test/future reaching the model during training, inflating metrics that collapse in production. Examples: scaling/encoding fit on the full dataset (including test), target-derived features, dedup/random split on time-series so future leaks into the past, test data used for tuning. Consequences: great validation scores, bad real-world results. Prevention: fit transformers only on train, strict chronological splits, and never let test data touch training decisions.

**Q99: When and how do you retrain a model?**
A: Retrain when: data drift/concept drift is detected, business conditions changed, new data with known labels is available, or the current/reference model's offline+online metrics degrade. Approaches: periodic scheduled retraining (daily/weekly), threshold-triggered retraining on drift alarms, or online/continuous learning. Always: version models, evaluate new vs current on a frozen holdout (A/B), and roll back safely. "Train once and forget" is how models rot.

**Q100: Design an end-to-end sentiment analysis system in production.**
A: (1) Data — labeled review/social data, annotation guidelines, stratified train/val/test. (2) Pipelines (ETL) — ingest, clean (dedupe, language detect), preprocess (normalize, handle code-mix), store raw + processed (SQLite/Postgres, object storage for raw). (3) Modeling — start with VADER as the cheap baseline, compare with a fine-tuned BERT; pick by latency/cost/accuracy, threshold-tune on the business cost matrix (that's my NullClass work scaled up). (4) Serving — FastAPI service with input validation, model versioning, batching, and caching. (5) Evaluation & monitoring — A/B the models, live accuracy on a labeled sample, per-label F1, sentiment distribution drift alerts, retraining trigger when drift/accuracy degrades. (6) Ops — Docker + GitHub Actions CI/CD (Krip AI pattern), logging, and a dashboard (my Streamlit experience) for stakeholders. This ties every project line on the resume into one senior-level answer.

---

> **Quick revision checklist before the interview:**
> 1. Be able to deep-dive EACH project for 15+ minutes — architecture, why-this-tool, trade-offs, failures, and the metrics.
> 2. Memorize the Agno PRs (Milvus reranking, JSON filter fix, Crawl4AI proxy) — these are the top resume hooks.
> 3. Know BERT, VADER, RAG pipeline, reranking, vector DBs, function calling/agents cold — the most-asked GenAI areas for SP DSE.
> 4. Keep your self-story tight: ML/DS foundation (NullClass, IEEE) → Engineering (Krip AI, Clone Futura) → GenAI/Agents (ScriptVector, OpenRTL.ai, Agno PRs).
> 5. Every number you state (accuracy, PRs, teams) must be defensible.