# Feature Store for Recommendation Systems

## 1. Feature Store Architecture

### 1.1 Core Components

**Offline Store**:
- Storage: Parquet files on MinIO/S3 via Apache Iceberg
- Purpose: Training data generation, batch feature computation
- Access Pattern: Full scans, joins, aggregations
- Latency: Minutes to hours
- Use Cases: Model training, batch scoring, backfills

**Online Store**:
- Storage: Redis Cluster
- Purpose: Low-latency feature serving for real-time inference
- Access Pattern: Point lookups by entity key
- Latency: <5ms p99
- Use Cases: Real-time recommendation serving

**Feature Registry**:
- Storage: PostgreSQL
- Purpose: Catalog of all features with metadata
- Access Pattern: Search, browse, metadata queries
- Use Cases: Feature discovery, lineage tracking, governance

**Feature Server**:
- Purpose: Unified API for feature access (online + offline)
- Protocol: gRPC for internal, REST for external
- Use Cases: Feature retrieval for training and serving

---

## 2. Feature Types in Feature Store

### 2.1 Entity-Based Features
- **User Features**: `user:123:click_count_24h = 45`
- **Item Features**: `item:456:ctr_7d = 0.12`
- **User-Item Features**: `user:123:item:456:affinity = 0.85`

### 2.2 Feature Groups
- **Behavioral Features**: Interaction counts, engagement metrics
- **Preference Features**: Category preferences, brand affinity
- **Contextual Features**: Time, device, location features
- **Content Features**: Text embeddings, image embeddings
- **Statistical Features**: Aggregates, distributions, trends

### 2.3 Feature Freshness Requirements
| Feature Type | Freshness Requirement | Update Frequency |
|---|---|---|
| Real-time session | <5 seconds | Every event |
| Streaming aggregate | <5 minutes | Continuous |
| Hourly aggregate | <1 hour | Hourly |
| Daily aggregate | <24 hours | Daily |
| Static metadata | <7 days | On change |
| Model-based | <24 hours | After retraining |

---

## 3. Feature Materialization

### 3.1 Offline Materialization
```
Feature Computation (Spark) → Parquet on S3 → Hive Metastore
```
- Used for training data generation
- Point-in-time joins for historical features
- Large batch reads for model training

### 3.2 Online Materialization
```
Feature Computation (Spark/Flink) → Redis Cluster
```
- Used for real-time serving
- Low-latency point lookups
- TTL-based expiration for stale features

### 3.3 Materialization Strategies
- **Full Refresh**: Recompute all feature values daily
- **Incremental Update**: Only compute changed features
- **Streaming Update**: Update features in real-time as events arrive
- **On-Demand**: Compute features at request time (no pre-materialization)

---

## 4. Feature Monitoring

### 4.1 Feature Drift Detection
- **Statistical Tests**: KS test, Chi-squared test for distribution changes
- **Drift Metrics**: PSI (Population Stability Index), KL divergence
- **Alert Thresholds**: Alert when drift exceeds configured thresholds
- **Root Cause Analysis**: Identify which features are drifting and why

### 4.2 Feature Quality Metrics
- **Missing Value Rate**: Percentage of null/missing values
- **Freshness**: Time since last feature update
- **Cardinality**: Number of unique values
- **Range Violations**: Values outside expected range
- **Correlation Changes**: Unexpected correlation shifts

### 4.3 Feature Impact Analysis
- **Feature Importance**: Track which features contribute most to predictions
- **Ablation Studies**: Measure model performance impact of removing features
- **Dead Feature Detection**: Identify features not used by any active model

---

## 5. Open Source Feature Store Comparison

### 5.1 Feast
- **Architecture**: Decoupled offline/online stores with registry
- **Strengths**: Kubernetes-native, well-documented, active community
- **Offline Store**: Parquet, BigQuery, Snowflake
- **Online Store**: Redis, DynamoDB, Cassandra
- **Integration**: Spark, Flink, Python SDK

### 5.2 Hopsworks
- **Architecture**: Full ML platform with integrated feature store
- **Strengths**: End-to-end ML platform, strong governance
- **Features**: Feature store, model serving, experiment tracking, monitoring

### 5.3 Custom Feature Store
- **When to Build**: Unique requirements not met by existing tools
- **Components**: Redis (online), Parquet (offline), PostgreSQL (registry)
- **Trade-off**: More control but more maintenance burden
