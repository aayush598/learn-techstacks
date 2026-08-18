# Data Flow Diagrams — Recommendation System

## 1. Context Diagram (Level -1)

The context diagram shows the recommendation system as a single process interacting with external entities.

### External Entities:
1. **End Users** — Interact with the system through web, mobile, and email interfaces
2. **Content Creators** — Upload and manage items (products, videos, songs, etc.)
3. **Administrators** — Configure system, manage experiments, monitor performance
4. **Third-party Systems** — External data providers, analytics platforms, advertising systems
5. **Payment Systems** — Transaction data for purchase-based recommendations

### Data Flows:
- User → System: Browsing behavior, searches, ratings, purchases, preferences
- System → User: Personalized recommendations, search results, notifications
- Content Creator → System: Item metadata, content, pricing
- Admin → System: Configuration, experiment setup, model deployment
- System → Admin: Performance dashboards, alerts, reports
- System → Third-party: Recommendation data, analytics events
- Third-party → System: External signals, trend data

---

## 2. Level 0 DFD — Major Processes

The Level 0 diagram breaks the system into major processing areas.

### Process 1.0: Data Ingestion and Storage
- **Inputs**: User events, item updates, external data
- **Outputs**: Stored raw data, validated events, enriched events
- **Data Stores**: Raw event log, validated event store, item catalog
- **Description**: Captures, validates, deduplicates, and stores all incoming data

### Process 2.0: Feature Engineering
- **Inputs**: Raw events, user profiles, item metadata
- **Outputs**: Computed features (user features, item features, interaction features)
- **Data Stores**: Feature store (offline + online), feature registry
- **Description**: Computes and serves features for model training and inference

### Process 3.0: Model Training and Management
- **Inputs**: Training data (features + labels), experiment configurations
- **Outputs**: Trained models, model metrics, model artifacts
- **Data Stores**: Model registry, experiment log, training data cache
- **Description**: Trains, validates, and manages recommendation models

### Process 4.0: Recommendation Serving
- **Inputs**: User request, user features, candidate items, model predictions
- **Outputs**: Personalized recommendation list
- **Data Stores**: Model cache, recommendation cache, pre-computed recommendations
- **Description**: Generates real-time personalized recommendations

### Process 5.0: Experimentation and Analytics
- **Inputs**: Recommendation events, user interactions, experiment configurations
- **Outputs**: Experiment results, analytics reports, performance dashboards
- **Data Stores**: Experiment results, analytics data warehouse
- **Description**: Manages A/B tests, calculates metrics, generates reports

### Process 6.0: Feedback Loop
- **Inputs**: User interactions with recommendations, outcome data
- **Outputs**: Updated training data, model retraining triggers, feature updates
- **Data Stores**: Feedback store, label store
- **Description**: Closes the loop from recommendation delivery to model improvement

---

## 3. Level 1 DFD — Detailed Process Breakdown

### 3.1 Process 1.0: Data Ingestion — Detailed

#### 1.1 Event Collection
- Collect events from client SDKs (web, mobile, email)
- Validate event schema against registered schemas
- Enrich events with server-side context (timestamp, IP geolocation, device detection)
- Assign correlation IDs for end-to-end tracing

#### 1.2 Event Validation and Cleaning
- Deduplicate events using event_id
- Validate required fields are present
- Detect and handle malformed events
- Route invalid events to dead letter queue

#### 1.3 Event Enrichment
- Join events with user profile data
- Join events with item metadata
- Add computed fields (time since last interaction, session position)
- Add contextual data (weather, trending topics)

#### 1.4 Event Storage
- Write raw events to data lake (Apache Iceberg on MinIO)
- Write processed events to Kafka topics for real-time consumption
- Write aggregated events to ClickHouse for analytics
- Update search index for item-related events

### 3.2 Process 2.0: Feature Engineering — Detailed

#### 2.1 Batch Feature Computation
- Trigger: Daily/hourly scheduled job
- Input: Historical events, user profiles, item metadata
- Processing: Spark jobs compute aggregate features
  - User features: category preference distribution, average rating, interaction frequency
  - Item features: popularity trend, quality score, content embeddings
  - Interaction features: user-item affinity scores, co-occurrence matrices
- Output: Materialized feature tables in feature store

#### 2.2 Streaming Feature Computation
- Trigger: Real-time event stream
- Input: Processed events from Kafka
- Processing: Flink jobs compute windowed features
  - Rolling averages (last 1 hour, 24 hours, 7 days)
  - Session-level features (current session behavior)
  - Real-time trending scores
- Output: Updated feature values in Redis

#### 2.3 Online Feature Computation
- Trigger: Recommendation request
- Input: User ID, context, candidate items
- Processing: On-demand feature computation
  - User-item interaction features
  - Real-time context features
  - Feature crosses and encoding
- Output: Feature vector for model inference

### 3.3 Process 3.0: Model Training — Detailed

#### 3.1 Training Data Assembly
- Trigger: Training pipeline scheduled or triggered
- Input: Feature store data, label data (user interactions as labels)
- Processing:
  - Point-in-time feature retrieval (no data leakage)
  - Negative sampling for implicit feedback
  - Train/validation/test splitting (temporal split)
  - Data quality validation
- Output: Training dataset in optimized format

#### 3.2 Model Training
- Trigger: Training data assembly complete
- Input: Training dataset, model configuration
- Processing:
  - Hyperparameter optimization (Optuna)
  - Distributed training (PyTorch DDP)
  - Training metrics logging (MLflow)
  - Checkpoint saving
- Output: Trained model artifacts

#### 3.3 Model Validation
- Trigger: Training complete
- Input: Trained model, validation dataset
- Processing:
  - Offline evaluation metrics (NDCG, Precision, Recall, MAP)
  - Latency benchmarking
  - Fairness and bias checks
  - Data validation checks
- Output: Validation report, pass/fail decision

#### 3.4 Model Deployment
- Trigger: Validation passed, approval received
- Input: Validated model, deployment configuration
- Processing:
  - Package model for serving (ONNX conversion if needed)
  - Deploy to staging environment
  - Run canary deployment (5% traffic)
  - Monitor quality metrics
  - Promote to full production
- Output: Model serving in production

### 3.4 Process 4.0: Recommendation Serving — Detailed

#### 4.1 Request Processing
- Receive recommendation request with user context
- Authenticate and authorize request
- Validate request parameters
- Check recommendation cache for recent results

#### 4.2 Candidate Generation
- Fetch user features from online feature store
- Execute multiple retrieval strategies in parallel:
  - Collaborative filtering candidates
  - Content-based candidates
  - Trending/popular candidates
  - Contextual candidates
- Merge and deduplicate candidates
- Apply hard filters (availability, language, content moderation)

#### 4.3 Ranking
- Fetch item features for all candidates
- Compute user-item interaction features
- Execute ranking model inference
- Score all candidates
- Apply multi-objective optimization weights

#### 4.4 Post-Ranking
- Apply diversity optimization
- Apply business rules (promotions, editorial)
- Apply freshness boosting
- Apply content moderation filters
- Deduplicate across recommendation surfaces

#### 4.5 Response Delivery
- Format recommendation response
- Log recommendation event (user, items, scores, context)
- Update real-time feature store with impression data
- Return response to client

### 3.5 Process 5.0: Experimentation — Detailed

#### 5.1 Experiment Setup
- Define experiment hypothesis and metrics
- Configure variants and traffic allocation
- Set up guardrail metrics and alerting
- Deploy experiment configuration to experiment service

#### 5.2 Traffic Assignment
- Assign users to experiment variants using consistent hashing
- Ensure consistent assignment across sessions
- Handle new user assignment
- Prevent cross-experiment interference

#### 5.3 Metric Collection
- Track impression, click, and conversion events per variant
- Apply metric definitions consistently across variants
- Handle edge cases (session boundaries, cross-device)
- Aggregate metrics at configured intervals

#### 5.4 Analysis and Reporting
- Calculate statistical significance (p-values, confidence intervals)
- Detect novelty effects and sample ratio mismatch
- Generate experiment reports with recommendations
- Archive experiment results for future reference

### 3.6 Process 6.0: Feedback Loop — Detailed

#### 6.1 Feedback Collection
- Capture user interactions with served recommendations
- Record outcome data (purchase, completion, rating)
- Track long-term engagement metrics
- Collect explicit feedback (surveys, reviews)

#### 6.2 Label Generation
- Convert interactions into training labels
- Apply attribution windows (e.g., purchase within 7 days)
- Handle delayed feedback (purchase days after view)
- Generate negative labels from non-interactions with confidence scores

#### 6.3 Retraining Triggers
- Schedule-based: Daily/weekly full retraining
- Performance-based: Retrain when metrics degrade
- Data-based: Retrain after significant data volume increase
- Event-based: Retrain after data distribution shift detected

---

## 4. Real-Time Data Flow Path

```
User Action (click/view/purchase)
  ↓ (50ms)
Client SDK sends event
  ↓ (10ms)
API Gateway receives event
  ↓ (5ms)
Event Validation Service
  ↓ (5ms)
Kafka Producer publishes to topic
  ↓ (1ms)
Kafka Topic (partitioned by user_id)
  ↓ (varies)
  ├── Flink Consumer → Streaming Feature Computation → Redis Update (2-5s)
  ├── ClickHouse Consumer → Analytics Aggregation (1-5min)
  └── Training Data Consumer → Label Store (batch)
```

Total latency from user action to feature update: **2-5 seconds**

---

## 5. Batch Data Flow Path

```
Scheduled Trigger (daily/hourly)
  ↓
Data Extraction from Data Lake
  ↓ (Spark job: 10-60min)
Feature Computation (batch features)
  ↓ (Spark job: 30-120min)
Feature Validation and Quality Check
  ↓ (5min)
Feature Store Materialization (offline → online)
  ↓ (10min)
Training Data Assembly
  ↓ (Spark job: 15-30min)
Model Training (GPU cluster: 1-24hrs)
  ↓
Model Validation
  ↓ (30min)
Model Registry (staging)
  ↓ (manual review / automated gate)
Model Deployment (canary → production)
```

Total latency from data availability to model production: **2-24 hours**

---

## 6. Cross-Service Data Flows

### 6.1 Service-to-Service Data Dependencies

| Source Service | Target Service | Data | Protocol | Latency |
|---|---|---|---|---|
| User Profile Service | Feature Store | User attributes | gRPC | <5ms |
| Item Profile Service | Feature Store | Item attributes | gRPC | <5ms |
| Feature Store | Candidate Generation | User features | Redis GET | <3ms |
| Candidate Generation | Ranking | Candidate items | gRPC | <10ms |
| Feature Store | Ranking | User+Item features | Redis GET | <5ms |
| Ranking | Re-ranking | Scored items | gRPC | <5ms |
| Feedback Service | Feature Store | Interaction events | Kafka | 2-5s |
| Model Management | All Serving Services | Model updates | gRPC stream | <100ms |
| Experiment Service | API Gateway | Experiment config | gRPC | <5ms |

### 6.2 Data Serialization Formats
- **gRPC communication**: Protocol Buffers (binary, compact, schema-evolved)
- **Kafka events**: Avro with Schema Registry (compact, evolved)
- **REST APIs**: JSON (human-readable, web-compatible)
- **Feature store**: Redis protocol (binary, fast)
- **Data lake storage**: Parquet (columnar, compressed, query-optimized)
- **Model artifacts**: ONNX / PyTorch state_dict (optimized for inference)
