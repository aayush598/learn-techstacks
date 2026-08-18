# Microservices Overview — Recommendation System

## 1. Why Microservices for Recommendation Systems

### 1.1 The Case for Decomposition
Recommendation systems inherently involve multiple distinct concerns: data ingestion, feature computation, model training, model serving, API management, user profiling, and analytics. Each concern has different:
- **Scaling characteristics**: Model serving needs GPUs; feature computation needs CPUs; data ingestion needs high I/O
- **Update frequency**: Models update daily; APIs update weekly; infrastructure updates monthly
- **Team ownership**: ML engineers own models; data engineers own pipelines; backend engineers own APIs
- **Technology requirements**: Training uses Python/PyTorch; serving uses C++/ONNX; APIs use Go/Java

### 1.2 Benefits at Scale
- Independent deployment of services without coordinated releases
- Technology diversity — each service uses the best tool for its job
- Fault isolation — a failure in analytics does not affect recommendation serving
- Team autonomy — parallel development by multiple teams
- Granular scaling — scale model serving independently from API serving

---

## 2. Core Services — Detailed Specification

### 2.1 Candidate Generation Service

**Purpose**: Retrieve a broad set of potentially relevant items from the full catalog for a given user/context.

**Responsibilities**:
- Execute multiple retrieval strategies in parallel (collaborative, content-based, trending, contextual)
- Merge and deduplicate candidates from multiple channels
- Apply hard filters (availability, language, content moderation)
- Return top-N candidates to ranking service

**Inputs**: User ID, context (device, time, location), filters, number of candidates requested
**Outputs**: List of candidate item IDs with retrieval scores and channel source

**Scaling Characteristics**:
- CPU-intensive for ANN search; may benefit from GPU acceleration
- Requires low-latency access to item embeddings and user features
- High QPS — every recommendation request hits this service
- Scales horizontally; stateless design with distributed index shards

**Technology Choices**:
- FAISS or Milvus for vector similarity search
- Redis for user feature retrieval
- Elasticsearch for text-based retrieval and filtering

---

### 2.2 Ranking Service

**Purpose**: Score and sort candidate items by predicted relevance for the specific user.

**Responsibilities**:
- Fetch rich features for user-candidate pairs
- Execute ranking model inference
- Compute multi-objective scores (relevance, engagement, satisfaction, business value)
- Apply multi-task learning outputs for diverse optimization targets
- Return top-K ranked items

**Inputs**: Candidate item IDs, user ID, context, user features
**Outputs**: Ranked list of items with scores and explanation metadata

**Scaling Characteristics**:
- GPU-intensive for deep learning models
- Latency-critical — must complete within 20-100ms
- Batch inference — score multiple candidates in single forward pass
- Scales with GPU count; can use model parallelism for very large models

**Technology Choices**:
- Triton Inference Server for model serving
- ONNX Runtime for optimized CPU inference
- vLLM for large language model-based ranking

---

### 2.3 Re-ranking Service

**Purpose**: Apply post-ranking adjustments including diversity, business rules, and editorial overrides.

**Responsibilities**:
- Diversity optimization using Determinantal Point Processes (DPP) or Maximal Marginal Relevance (MMR)
- Business rule application (promotions, boosted items, blacklists)
- Content freshness adjustments
- Deduplication across recommendation surfaces
- Inject editorial/curated recommendations
- Apply content moderation filters

**Inputs**: Ranked item list, business rules, editorial configuration
**Outputs**: Final recommendation list with applied adjustments

---

### 2.4 User Profile Service

**Purpose**: Manage and serve comprehensive user profiles for personalization.

**Responsibilities**:
- Aggregate user attributes from multiple sources
- Compute and store user preference vectors
- Manage user interaction history
- Handle user preference updates in real-time
- Support user segmentation and clustering
- Privacy compliance (data deletion, anonymization)

**Data Stored**:
- Static attributes: demographics, preferences, subscription tier
- Computed attributes: preference vectors, embedding representations
- Aggregated statistics: interaction counts, category preferences, session metrics
- Privacy settings: consent preferences, data retention policies

**API Design**:
- `GET /users/{id}/profile` — Full user profile
- `GET /users/{id}/preferences` — User preference vector
- `GET /users/{id}/history` — Recent interaction history
- `PUT /users/{id}/preferences` — Update user preferences
- `DELETE /users/{id}/data` — GDPR data deletion

---

### 2.5 Item Profile Service

**Purpose**: Manage and serve item metadata, embeddings, and content understanding.

**Responsibilities**:
- Store and serve item metadata (title, description, categories, tags)
- Manage pre-computed item embeddings (text, image, audio)
- Handle item lifecycle (creation, update, deprecation, removal)
- Compute item popularity and trending scores
- Maintain item quality signals
- Support content-based similarity queries

**Data Stored**:
- Static metadata: title, description, categories, tags, attributes
- Computed embeddings: text embedding, image embedding, audio embedding
- Statistical metrics: popularity score, trending score, quality score
- Relationship data: related items, category hierarchy, brand information

---

### 2.6 Feature Computation Service

**Purpose**: Compute and serve features for model training and real-time inference.

**Responsibilities**:
- **Offline Feature Computation**: Daily Spark jobs for batch features (user historical aggregates, item statistics)
- **Near-line Feature Computation**: Flink/Kafka Streams for rolling window features (last hour activity, trending scores)
- **Online Feature Computation**: On-demand computation at serving time (real-time session features)
- **Feature Serving**: Low-latency retrieval from feature store
- **Feature Monitoring**: Track feature freshness, distribution, and quality

**Architecture**:
- Batch features flow: Spark -> Feature Store (offline) -> Materialized to Feature Store (online)
- Streaming features flow: Kafka -> Flink -> Feature Store (online)
- On-demand features flow: Request -> Compute -> Serve (no storage)

---

### 2.7 Model Management Service

**Purpose**: Manage the lifecycle of ML models from training to production.

**Responsibilities**:
- Model versioning and artifact storage
- Model stage management (development -> staging -> canary -> production)
- Automated quality gates before promotion
- Model rollback capabilities
- A/B test model assignment
- Model performance monitoring
- Model lineage and metadata tracking

**Key Concepts**:
- **Model Registry**: Central catalog of all model versions
- **Model Stages**: Development, Staging, Canary, Production, Archived
- **Quality Gates**: Automated checks (latency, accuracy, data validation) before promotion
- **Rollback**: Instant revert to previous model version on quality degradation
- **Model Lineage**: Complete audit trail from data to model to predictions

---

### 2.8 Experiment Service (A/B Testing)

**Purpose**: Manage experimentation infrastructure for testing recommendation strategies.

**Responsibilities**:
- User/traffic assignment to experiment variants
- Consistent hashing for deterministic assignment
- Experiment configuration management
- Metric collection and aggregation
- Statistical significance calculation
- Experiment lifecycle management (draft, running, concluded)
- Interference prevention between concurrent experiments

**Key Concepts**:
- **Experiment**: A hypothesis being tested (e.g., "new ranking model improves CTR")
- **Variant**: A specific configuration being tested (control, treatment A, treatment B)
- **Traffic Allocation**: Percentage of traffic assigned to each variant
- **Unit of Experimentation**: User-level, session-level, or request-level
- **Metric Guardrails**: Automated experiment termination if key metrics degrade

---

### 2.9 Feedback Collection Service

**Purpose**: Collect, process, and store user feedback signals for model improvement.

**Responsibilities**:
- Ingest implicit feedback: clicks, views, dwell time, scroll depth, purchases
- Ingest explicit feedback: ratings, likes, reviews, preferences
- Validate and deduplicate feedback events
- Aggregate feedback for model training data generation
- Feed real-time signals to streaming feature computation
- Support feedback for model evaluation

**Event Types**:
- `impression`: Item was shown to user
- `click`: User clicked on item
- `view`: User viewed item content
- `like`: User liked/favorited item
- `purchase`: User purchased item
- `rating`: User rated item
- `share`: User shared item
- `skip`: User skipped/dismissed item
- `report`: User reported item as inappropriate
- `search`: User searched for specific content

---

### 2.10 Search Service

**Purpose**: Provide search functionality that complements recommendation features.

**Responsibilities**:
- Full-text search across item catalog
- Faceted search with filters and sorting
- Search-as-you-type with autocomplete
- Query understanding and intent detection
- Hybrid search combining keyword and semantic search
- Search result ranking using the same ranking models
- Search personalization based on user profile

---

### 2.11 Notification Service

**Purpose**: Deliver personalized recommendations through non-real-time channels.

**Responsibilities**:
- Email recommendation digests (daily/weekly)
- Push notification recommendations
- In-app recommendation updates
- Notification scheduling and throttling
- User notification preferences management
- Delivery tracking and analytics

---

## 3. Service Communication Patterns

### 3.1 Synchronous Communication
- **Use When**: Low-latency response required; caller needs immediate result
- **Protocols**: gRPC (internal), REST (external), GraphQL (flexible clients)
- **Patterns**: Request-response, server streaming
- **Risk**: Cascading failures; mitigated with circuit breakers and timeouts

### 3.2 Asynchronous Communication
- **Use When**: Result not immediately needed; high throughput; eventual consistency acceptable
- **Protocols**: Kafka (event streaming), RabbitMQ (task queues), Redis Streams (lightweight)
- **Patterns**: Event-driven, pub/sub, task queue
- **Benefit**: Decoupling, resilience, natural load leveling

### 3.3 Communication Matrix

| From → To | Protocol | Pattern |
|---|---|---|
| API Gateway → Candidate Gen | gRPC | Request-response |
| API Gateway → Ranking | gRPC | Request-response |
| Candidate Gen → Ranking | gRPC | Request-response |
| Ranking → Re-ranking | gRPC | Request-response |
| All Services → Feature Store | gRPC/Redis | Request-response |
| User Actions → Feedback Service | Kafka | Event-driven |
| Feedback Service → Feature Service | Kafka | Event-driven |
| Model Mgmt → Serving Services | gRPC | Streaming (model updates) |
| Experiment Service → All | gRPC | Request-response |

---

## 4. Database Per Service Pattern

| Service | Database Type | Purpose |
|---|---|---|
| User Profile Service | PostgreSQL + Redis | User data + fast profile access |
| Item Profile Service | PostgreSQL + Elasticsearch | Item metadata + search index |
| Feature Store | Redis (online) + Parquet (offline) | Feature serving + training data |
| Feedback Service | Kafka + ClickHouse | Event storage + analytics |
| Experiment Service | PostgreSQL | Experiment configuration |
| Model Management | PostgreSQL + Object Storage | Registry + model artifacts |
| Search Service | Elasticsearch | Search indices |

---

## 5. Service Sizing Guidelines

### 5.1 When to Split a Service
- When a service has distinct scaling requirements from its neighbors
- When different parts of a service are owned by different teams
- When changes to one part of the service require testing the entire service
- When the service's database schema is becoming a catch-all
- When deployment of one feature requires deploying unrelated features

### 5.2 When to Merge Services
- When two services are always deployed together
- When the communication overhead between services exceeds the benefit
- When the services share most of their data
- When the operational complexity of running two services is not justified

---

## 6. Team Topology Alignment

| Team | Owned Services | Skills |
|---|---|---|
| ML Platform | Model Management, Feature Computation, Training Pipelines | ML Engineering, MLOps |
| Recommendation Backend | Candidate Gen, Ranking, Re-ranking | ML Engineering, Backend |
| User Platform | User Profile, Feedback Collection, Notifications | Backend Engineering |
| Content Platform | Item Profile, Search, Content Moderation | Backend Engineering |
| Data Engineering | Data pipelines, Data lake, ETL | Data Engineering |
| Experimentation | Experiment Service, Analytics | Data Science, ML Engineering |
| Platform/Infrastructure | Kubernetes, CI/CD, Monitoring, Security | DevOps, SRE |
| Product | Client applications, UI/UX | Frontend, Design |
