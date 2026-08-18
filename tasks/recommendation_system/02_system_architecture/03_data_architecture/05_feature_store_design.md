# Feature Store Design for Recommendation Systems

## 1. Feature Store Architecture

### 1.1 Why Feature Store
A feature store is a centralized platform for managing, serving, and sharing ML features. It solves:
- **Feature Sharing**: Multiple models use same features without duplication
- **Consistency**: Training and serving use identical feature computation logic
- **Freshness**: Features updated in real-time and served at low latency
- **Discoverability**: Central registry of all available features
- **Reproducibility**: Point-in-time correctness for training data generation

### 1.2 Core Components

**Offline Store**:
- Storage: Apache Parquet files on data lake (MinIO/S3)
- Purpose: Training data generation, batch feature computation
- Access Pattern: Full table scans, joins, aggregations
- Latency: Minutes to hours
- Tools: Apache Spark, Feast offline store

**Online Store**:
- Storage: Redis Cluster, DynamoDB, or Cassandra
- Purpose: Low-latency feature serving for real-time inference
- Access Pattern: Point lookups by entity key
- Latency: <5ms p99
- Tools: Feast online store, custom Redis client

**Feature Registry**:
- Storage: PostgreSQL or metadata service
- Purpose: Catalog of all features with schema, owner, freshness, lineage
- Access Pattern: Search, browse, metadata queries
- Tools: Feast registry, custom metadata service

**Feature Computation Engine**:
- Batch: Apache Spark for daily/hourly feature computation
- Streaming: Apache Flink for real-time feature computation
- On-demand: Application code for request-time feature computation

---

## 2. Feature Types for Recommendations

### 2.1 User Features

**Static User Features** (computed infrequently):
- Demographics: age, gender, country, language
- Preferences: preferred categories, price range, brand preferences
- Account: registration date, subscription tier, lifetime value

**Dynamic User Features** (computed frequently):
- Behavioral aggregates: items viewed last 1h/24h/7d/30d
- Category preferences: category distribution over last 30 days
- Engagement metrics: avg session duration, sessions per week
- Purchase behavior: avg order value, purchase frequency

**Real-time User Features** (computed at request time):
- Session features: items in current session, session duration
- Contextual features: current device, time of day, location
- Recent interactions: last 5 items interacted with

### 2.2 Item Features

**Static Item Features**:
- Metadata: title, description, categories, tags, brand
- Attributes: price, weight, dimensions, color
- Content embeddings: text embedding, image embedding

**Dynamic Item Features**:
- Popularity: views/clicks/purchases in last 1h/24h/7d
- Trending score: rate of change in popularity
- Quality score: avg rating, review count, return rate

**Real-time Item Features**:
- Current trending status
- Real-time inventory/availability
- Live engagement metrics

### 2.3 Interaction Features

**User-Item Interaction Features**:
- Historical affinity score between user and item categories
- Number of times user has interacted with similar items
- User's rating behavior for items in same category

**Contextual Interaction Features**:
- Time since user last interacted with this category
- User's typical engagement pattern at this time of day
- Device-specific engagement patterns

---

## 3. Feature Computation Pipelines

### 3.1 Batch Feature Pipeline
```
Scheduled Trigger (daily/hourly)
  → Spark Job reads raw events from data lake
  → Computes aggregate features (windowed statistics)
  → Writes to feature store offline store (Parquet)
  → Materializes hot features to online store (Redis)
```

**Example Batch Features**:
- User's category preference distribution (last 30 days)
- Item's average rating (all time)
- User-item co-occurrence statistics

### 3.2 Streaming Feature Pipeline
```
Kafka Event → Flink Job
  → Windowed aggregation (tumbling, sliding, session windows)
  → State management for window state
  → Writes to online store (Redis)
  → Latency: 2-5 seconds from event to feature availability
```

**Example Streaming Features**:
- User's click count in last hour
- Item's trending score (last 15 minutes)
- User's session-level engagement

### 3.3 On-Demand Feature Pipeline
```
Recommendation Request
  → Fetch user features from online store
  → Fetch item features from online store
  → Compute interaction features on-the-fly
  → Assemble feature vector for model inference
  → Latency: <10ms
```

**Example On-Demand Features**:
- User-item cross features (user_age × item_price_bucket)
- Feature interactions (user_category_preference × item_category)
- Encoding transformations (hash encoding, target encoding)

---

## 4. Point-in-Time Correctness

### 4.1 The Problem
Training data must use features as they were at the time of each historical interaction, not as they are now. Using current features for historical data causes:
- **Data Leakage**: Using future information to predict past events
- **Biased Models**: Models trained on unrealizable feature values
- **Poor Generalization**: Models learn patterns that don't exist in real serving

### 4.2 Solution: Point-in-Time Joins
- Training data generation joins features at the event timestamp
- Each training example uses features as they existed at that point in time
- Feature store maintains historical snapshots for offline store
- Online store only serves current features (no historical lookup needed)

### 4.3 Implementation
```
For each training event (user_id, item_id, event_timestamp):
  1. Look up user features as of event_timestamp from offline store
  2. Look up item features as of event_timestamp from offline store
  3. Compute interaction features using features available at event_timestamp
  4. Label = outcome of the interaction
```

---

## 5. Open Source Feature Stores

### 5.1 Feast
- **Architecture**: Decoupled offline/online stores with registry
- **Offline Store**: Parquet on S3, BigQuery, Snowflake
- **Online Store**: Redis, DynamoDB, Cassandra
- **Registry**: PostgreSQL, file-based
- **Strengths**: Kubernetes-native, well-documented, active community
- **Integration**: Works with Spark, Flink, Python

### 5.2 Hopsworks
- **Architecture**: Full ML platform with integrated feature store
- **Features**: Feature store, model serving, experiment tracking
- **Strengths**: End-to-end ML platform, strong governance
- **Integration**: Jupyter, Spark, Python SDK

### 5.3 Tecton (Concept Reference)
- **Architecture**: Managed feature platform (reference for design)
- **Features**: Real-time feature computation, streaming features
- **Strengths**: Production-grade real-time features
- **Lessons**: Streaming feature architecture patterns worth emulating

---

## 6. Feature Monitoring

### 6.1 Feature Drift Detection
- **Distribution Monitoring**: Track feature distribution over time
- **Drift Metrics**: KL divergence, JS divergence, Population Stability Index (PSI)
- **Alert Thresholds**: Alert when drift exceeds configured thresholds
- **Root Cause Analysis**: Identify which features are drifting and why

### 6.2 Feature Quality Metrics
- **Missing Value Rate**: Percentage of null/missing values per feature
- **Freshness**: Time since last feature update
- **Cardinality**: Number of unique values per feature
- **Range Violations**: Values outside expected range
- **Schema Violations**: Feature type mismatches

### 6.3 Feature Impact Analysis
- **Feature Importance**: Track which features contribute most to model predictions
- **Feature Ablation**: Measure model performance impact of removing each feature
- **Feature Interaction**: Identify important feature interactions
- **Dead Features**: Identify features not used by any active model
