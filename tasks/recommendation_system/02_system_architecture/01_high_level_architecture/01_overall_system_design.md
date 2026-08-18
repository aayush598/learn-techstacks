# Overall System Design — Recommendation System Architecture

## 1. Executive Overview

A production-grade recommendation system is one of the most complex distributed systems in modern software engineering. It spans data engineering, machine learning, real-time serving, and user experience — all operating at scale with strict latency and availability requirements. This document covers the complete end-to-end architecture that mirrors what top-tier companies like Netflix, Spotify, Amazon, and YouTube operate in production.

---

## 2. Core Architectural Principles

### 2.1 Design Principles
- **Separation of Concerns**: Each layer handles a distinct responsibility — data ingestion, feature computation, model training, serving, and presentation
- **Loose Coupling**: Services communicate through well-defined interfaces; changes in one layer do not cascade failures
- **High Cohesion**: Related functionality is grouped within the same service boundary
- **Scalability First**: Every component is designed to scale independently based on its specific bottleneck
- **Fault Tolerance**: No single point of failure; graceful degradation at every layer
- **Observability**: Every component emits metrics, logs, and traces for debugging and monitoring
- **Idempotency**: Recommendation requests are idempotent — retries do not produce duplicate side effects
- **Data Locality**: Computation is moved closer to data to minimize network overhead

### 2.2 Architectural Tradeoffs
- **Consistency vs Availability**: Recommendation systems favor availability; eventual consistency is acceptable for most recommendation features
- **Latency vs Accuracy**: Two-stage architecture (candidate generation + ranking) balances both
- **Freshness vs Compute Cost**: Real-time features improve quality but increase infrastructure cost
- **Complexity vs Performance**: Simple models with excellent features often outperform complex models with poor features

---

## 3. System Layers — Detailed Breakdown

### 3.1 Data Layer

The data layer is the foundation of the entire recommendation system. It handles ingestion, storage, and initial processing of all data.

#### 3.1.1 Data Sources
- **User Interaction Data**: Clicks, views, purchases, ratings, likes, shares, bookmarks, time spent, scroll depth, search queries
- **User Profile Data**: Demographics, preferences, device information, location, registration date, subscription tier
- **Item Data**: Metadata (title, description, categories, tags), content embeddings (text, image, audio), pricing, availability, freshness
- **Contextual Data**: Time of day, day of week, season, device type, geographic location, network conditions
- **External Data**: Trends, social signals, competitor data, market conditions

#### 3.1.2 Data Ingestion
- **Real-time Ingestion**: Apache Kafka for streaming user events with sub-millisecond latency; schema registry for event schema management
- **Batch Ingestion**: Apache Airflow orchestrated ETL pipelines for daily/hourly data loads from databases and data warehouses
- **Change Data Capture (CDC)**: Debezium for capturing database changes in real-time for user profile and item metadata updates
- **Event Schema**: Avro or Protobuf schemas registered in Confluent Schema Registry or Apicurio for schema evolution

#### 3.1.3 Data Storage
- **Data Lake**: Apache Iceberg on MinIO/S3 for raw and processed data at petabyte scale
- **Data Warehouse**: Apache ClickHouse or Apache Druid for real-time analytics and dashboard queries
- **Operational Database**: PostgreSQL for transactional data (user accounts, orders, configurations)
- **Cache Layer**: Redis Cluster for hot data (recent interactions, active user features, frequent recommendations)

#### 3.1.4 Data Processing
- **Batch Processing**: Apache Spark for large-scale data transformations, feature computation, and model training data preparation
- **Stream Processing**: Apache Flink or Apache Kafka Streams for real-time feature computation and event aggregation
- **Query Engine**: Apache Trino for federated queries across multiple data stores

---

### 3.2 Feature Layer

The feature layer bridges raw data and machine learning models. It is arguably the most critical layer for recommendation quality.

#### 3.2.1 Feature Types
- **User Features**: Historical interaction aggregates, preference vectors, demographic embeddings, session-level behavioral features
- **Item Features**: Content embeddings, popularity metrics, freshness scores, category distributions, quality signals
- **Interaction Features**: Cross features between user and item, historical affinity scores, co-occurrence statistics
- **Contextual Features**: Time-based features, device features, location features, weather features
- **Graph Features**: Social network embeddings, community detection scores, influence metrics

#### 3.2.2 Feature Computation
- **Offline Features**: Computed in batch (Spark jobs) — historical aggregates, trained embeddings, statistical features; stored in feature store offline store
- **Near-line Features**: Computed on streaming data (Flink/Kafka Streams) — rolling window aggregates, real-time popularity; stored with minutes of latency
- **Online Features**: Computed on-demand at serving time — user's last N interactions, real-time session features; computed in milliseconds
- **On-Demand Features**: Computed at inference time from raw input — feature crosses, encoding transformations

#### 3.2.3 Feature Store
- **Offline Store**: Parquet files on data lake for training data generation with point-in-time correctness
- **Online Store**: Redis or DynamoDB-compatible store for low-latency feature retrieval during serving (< 5ms p99)
- **Feature Registry**: Centralized catalog of all features with schema, owner, freshness SLA, and lineage
- **Point-in-time Correctness**: Training data uses features as they were at the time of each historical interaction, preventing data leakage
- **Feature Versioning**: All feature transformations are versioned for reproducibility
- **Feature Monitoring**: Automated detection of feature drift, missing values, and distribution changes

---

### 3.3 Training Layer

The training layer transforms data and features into recommendation models.

#### 3.3.1 Training Infrastructure
- **Distributed Training**: PyTorch Distributed Data Parallel (DDP) or DeepSpeed for training large models across multiple GPUs
- **Training Clusters**: Kubernetes with GPU node pools (NVIDIA A100/H100) for training workloads
- **Experiment Tracking**: MLflow for tracking experiments, parameters, metrics, and artifacts
- **Model Registry**: MLflow Model Registry or ML Server for versioned model storage with stage transitions
- **Resource Management**: Kubernetes resource quotas and priority classes to manage training vs serving resources

#### 3.3.2 Training Pipelines
- **Full Retraining**: Complete model retraining on full dataset — typically daily or weekly
- **Incremental Training**: Fine-tuning existing model on new data — can run hourly
- **Online Learning**: Continuous model updates from real-time feedback — runs continuously
- **Multi-stage Training**: Pre-training on large data, fine-tuning on domain-specific data, calibration on recent data

#### 3.3.3 Training Data Generation
- **Negative Sampling**: Strategic sampling of items a user did not interact with for implicit feedback models
- **Position Debiasing**: Correcting for position bias in training data where higher-positioned items get more clicks
- **Time Decay**: Weighting recent interactions more heavily than older ones
- **Data Augmentation**: Creating synthetic training examples from existing data
- **Train/Validation/Test Splitting**: Temporal splitting to prevent future data leakage

---

### 3.4 Model Store

The model store manages trained models through their lifecycle.

#### 3.4.1 Model Registry
- **Model Versioning**: Semantic versioning for all model artifacts
- **Stage Transitions**: Staging -> Production -> Archived lifecycle
- **Model Metadata**: Training data version, hyperparameters, metrics, dependencies
- **Model Lineage**: Which data, code, and configuration produced each model version
- **Model Comparison**: Side-by-side comparison of model versions across metrics
- **Rollback Capability**: Instant rollback to previous model version if issues detected

#### 3.4.2 Model Artifacts
- **Model Weights**: Serialized model parameters (PyTorch state_dict, ONNX format)
- **Embeddings**: Pre-computed user and item embedding tables
- **Vocabulary/Encoder**: Tokenizers, label encoders, normalizers
- **Configuration**: Model architecture configuration, feature config, serving config
- **Validation Reports**: Automated quality gate results before production deployment

---

### 3.5 Serving Layer

The serving layer is where real-time recommendation requests are processed and responses returned.

#### 3.5.1 Two-Stage Architecture

This is the industry-standard architecture used by YouTube, Amazon, and TikTok:

**Stage 1 — Candidate Generation:**
- Purpose: Narrow down millions of items to hundreds of candidates
- Techniques: Collaborative filtering, approximate nearest neighbor (ANN) search, graph-based retrieval
- Latency budget: 10-50ms
- Scale: Must search through millions of items efficiently
- Tools: FAISS, ScaNN, Milvus for vector search; Elasticsearch for text-based retrieval
- Multiple retrieval channels: collaborative, content-based, trending, contextual, editorial

**Stage 2 — Ranking:**
- Purpose: Score and sort hundreds of candidates by relevance
- Techniques: Deep neural networks, gradient boosted trees, ensemble models
- Latency budget: 20-100ms
- Richer features available since scoring is done on a small candidate set
- Multi-objective optimization: relevance, diversity, freshness, business value
- Multiple ranking models for different surfaces (home page, detail page, email)

**Stage 3 — Re-ranking (Post-ranking):**
- Purpose: Apply business rules, diversity constraints, and final adjustments
- Techniques: Determinantal Point Processes (DPP) for diversity, business rule filters
- Deduplication across recommendation surfaces
- freshness boosting, content moderation filters
- Editorial overrides and promoted content injection

#### 3.5.2 Inference Pipeline
1. Parse and validate request (user ID, context, filters)
2. Fetch user features from feature store (online store)
3. Fetch candidate items from retrieval services (ANN search + business rules)
4. Compute interaction features between user and candidates
5. Score candidates using ranking model
6. Apply re-ranking logic (diversity, business rules, freshness)
7. Format response with recommendation metadata
8. Log request and response for feedback loop
9. Return response to client

#### 3.5.3 Serving Patterns
- **Synchronous Serving**: Request-response for real-time recommendations on web/mobile
- **Batch Pre-computation**: Pre-compute recommendations for all users periodically (e.g., daily email recommendations)
- **Hybrid Serving**: Pre-compute candidates online, rank in real-time (most common production pattern)
- **Streaming Serving**: Continuous recommendation updates pushed to client via WebSocket

---

### 3.6 API Layer

The API layer exposes recommendation capabilities to clients and external systems.

#### 3.6.1 API Types
- **REST API**: For web and mobile clients; JSON payloads; HTTP/2 support
- **gRPC API**: For internal service-to-service communication; Protocol Buffers; bidirectional streaming
- **GraphQL API**: For flexible client-driven queries; single endpoint; schema introspection
- **WebSocket API**: For real-time recommendation streams; push-based updates

#### 3.6.2 API Endpoints
- `GET /v1/recommendations/home` — Home page personalized recommendations
- `GET /v1/recommendations/similar/{item_id}` — Similar item recommendations
- `GET /v1/recommendations/for-you` — "For You" personalized feed
- `GET /v1/recommendations/trending` — Trending/popular items
- `POST /v1/interactions` — Record user interaction (implicit feedback)
- `POST /v1/ratings` — Submit user rating (explicit feedback)
- `GET /v1/users/{user_id}/preferences` — User preference profile
- `GET /v1/items/{item_id}/recommendations` — Item-level recommendations (e.g., "customers also bought")

#### 3.6.3 Cross-Cutting Concerns
- **Authentication**: JWT token validation, API key verification
- **Rate Limiting**: Per-user, per-API-key, per-endpoint rate limits
- **Caching**: Response caching at gateway and CDN levels
- **Compression**: gzip/Brotli for response compression
- **Circuit Breaking**: Fallback to cached/default recommendations on failure
- **Request Logging**: Full request/response logging for debugging

---

### 3.7 Client Layer

The client layer is where recommendations are presented to users.

#### 3.7.1 Client Surfaces
- **Web Application**: React/Vue SPA with server-side rendering for SEO
- **Mobile Applications**: Native iOS/Android with push notification support
- **Email Recommendations**: Pre-generated recommendation emails (daily/weekly digests)
- **Push Notifications**: Real-time recommendation alerts
- **Third-party Integrations**: API-based recommendation delivery to partners

#### 3.7.2 Client-Side Patterns
- **Skeleton Loading**: Show placeholder UI while recommendations load
- **Progressive Loading**: Load initial recommendations fast, then enhance with more data
- **Offline Support**: Cache last recommendations for offline viewing
- **A/B Test SDK**: Client-side experiment assignment and tracking
- **Analytics SDK**: Track user interactions with recommendations
- **Personalization Signals**: Client-side signals (scroll depth, hover time, dwell time)

---

## 4. Architecture Patterns

### 4.1 Lambda Architecture
- **Batch Layer**: Process all historical data in batch for comprehensive recommendations
- **Speed Layer**: Process recent data in real-time for freshness
- **Serving Layer**: Merge batch and real-time views for serving
- **Pros**: Handles both completeness and freshness
- **Cons**: Maintaining two code paths (batch + stream) increases complexity

### 4.2 Kappa Architecture
- **Single Stream Layer**: All data processing through a single stream processing system
- **Replay Capability**: Reprocess by replaying from event log
- **Pros**: Simpler architecture, single codebase
- **Cons**: Stream processing may not handle all batch use cases efficiently

### 4.3 Recommendation-Specific Pattern
Most production recommendation systems use a **hybrid** approach:
- **Batch**: Model training, offline feature computation, batch recommendation pre-computation
- **Stream**: Real-time feature computation, online model updates, live event processing
- **Request-Driven**: Real-time inference at serving time with online features

---

## 5. Latency Budget Breakdown

For a recommendation request with a 200ms total latency budget:

| Component | Latency Budget | Percentage |
|---|---|---|
| Network (Client → API) | 20ms | 10% |
| API Gateway Processing | 5ms | 2.5% |
| Authentication/Authorization | 5ms | 2.5% |
| User Feature Retrieval | 15ms | 7.5% |
| Candidate Generation (ANN Search) | 30ms | 15% |
| Item Feature Retrieval | 15ms | 7.5% |
| Interaction Feature Computation | 10ms | 5% |
| Model Inference (Ranking) | 40ms | 20% |
| Re-ranking / Business Rules | 10ms | 5% |
| Response Serialization | 5ms | 2.5% |
| Network (API → Client) | 20ms | 10% |
| Buffer / Safety Margin | 25ms | 12.5% |
| **Total** | **200ms** | **100%** |

---

## 6. Open Source Technology Stack

### 6.1 Data Layer
| Component | Technology | Purpose |
|---|---|---|
| Event Streaming | Apache Kafka | Real-time event ingestion and processing |
| Stream Processing | Apache Flink | Real-time feature computation |
| Batch Processing | Apache Spark | Large-scale data transformations |
| Data Lake | Apache Iceberg + MinIO | Petabyte-scale data storage |
| OLAP Database | Apache ClickHouse | Real-time analytics |
| Operational DB | PostgreSQL | Transactional data |
| Cache | Redis Cluster | Hot data caching |

### 6.2 Feature Layer
| Component | Technology | Purpose |
|---|---|---|
| Feature Store | Feast | Feature serving and management |
| Feature Computation | Apache Spark + Flink | Batch and stream feature computation |
| Feature Registry | Feast + custom metadata | Feature catalog and lineage |

### 6.3 Training Layer
| Component | Technology | Purpose |
|---|---|---|
| ML Framework | PyTorch | Model development |
| Distributed Training | PyTorch DDP / DeepSpeed | Multi-GPU training |
| Experiment Tracking | MLflow | Experiment management |
| Model Registry | MLflow Model Registry | Model versioning |
| Hyperparameter Tuning | Optuna | Hyperparameter optimization |
| Orchestration | Apache Airflow / Kubeflow Pipelines | Pipeline orchestration |

### 6.4 Serving Layer
| Component | Technology | Purpose |
|---|---|---|
| Model Serving | Triton Inference Server / vLLM | High-performance model serving |
| Vector Search | FAISS / Milvus | Approximate nearest neighbor search |
| Serving Framework | FastAPI / gRPC | API serving |
| Model Optimization | ONNX Runtime | Inference optimization |

### 6.5 Infrastructure
| Component | Technology | Purpose |
|---|---|---|
| Container Orchestration | Kubernetes | Container management |
| Service Mesh | Istio / Linkerd | Service communication |
| API Gateway | Kong / Traefik | API routing and security |
| Monitoring | Prometheus + Grafana | Metrics and dashboards |
| Logging | ELK Stack (Elasticsearch, Logstash, Kibana) | Log aggregation |
| Tracing | Jaeger / OpenTelemetry | Distributed tracing |
| CI/CD | GitHub Actions / GitLab CI | Continuous integration |
| IaC | Terraform / Pulumi | Infrastructure management |

---

## 7. Scalability Characteristics

### 7.1 Scale Dimensions
- **Users**: 1K → 1M → 100M → 1B users
- **Items**: 10K → 1M → 100M → 1B items
- **Interactions**: 10K/day → 10M/day → 1B/day
- **Requests**: 10 QPS → 10K QPS → 1M QPS
- **Features**: 100 features → 10K features → 1M features
- **Models**: 1 model → 10 models → 100+ concurrent A/B tests

### 7.2 Scaling Strategies by Component
- **API Layer**: Horizontal scaling with load balancers; stateless design
- **Feature Store**: Redis Cluster with consistent hashing; read replicas
- **Model Serving**: GPU scaling with auto-scaling; model sharding for large models
- **Vector Search**: Sharded FAISS indices; hierarchical navigable small world (HNSW) graphs
- **Data Pipeline**: Spark dynamic allocation; Flink reactive scaling
- **Database**: Read replicas, connection pooling, query optimization, sharding

---

## 8. Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Feature store down | Cannot serve personalized recommendations | Fallback to popular/trending items; cached features |
| Model serving failure | No recommendations generated | Fallback to previous model version; pre-computed cache |
| Kafka lag spike | Features become stale | Monitor consumer lag; scale consumers; alert on thresholds |
| Database overload | Slow or failed queries | Connection pooling; read replicas; query caching |
| GPU exhaustion | Model inference delays | GPU auto-scaling; CPU fallback models; request queuing |
| Network partition | Services cannot communicate | Circuit breakers; local fallback logic; retry with backoff |
| Data corruption | Incorrect recommendations | Data validation gates; model quality checks; rollback capability |

---

## 9. Key Design Decisions

1. **Two-stage retrieval**: Candidate generation + ranking is the standard for good reason — it allows using cheap retrieval for scale and expensive models for quality
2. **Feature store as central component**: Separating feature computation from model serving enables feature reuse, consistency, and independent scaling
3. **Event sourcing for interactions**: Storing all user interactions as immutable events enables replay, debugging, and flexible feature computation
4. **Model registry with staged deployment**: Models go through staging, canary, and production stages with automated quality gates
5. **Multi-model serving**: Different models for different surfaces, user segments, and objectives; enables experimentation and specialization
6. **Graceful degradation**: The system should always return something (popular items, cached recommendations) even when components fail
7. **Observability first**: Every component must emit metrics, logs, and traces — you cannot improve what you cannot measure
