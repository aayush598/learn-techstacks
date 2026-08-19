# Feature Computation Pipelines for Recommendation Systems

## 1. Computation Latency Tiers

### 1.1 Tier Definitions

| Tier | Latency | Use Case | Examples |
|---|---|---|---|
| Batch | Hours–Days | Training data, offline analytics | Daily user aggregates, item popularity |
| Micro-Batch | Minutes | Near-real-time updates | Sliding window counts, trending scores |
| Streaming | Seconds | Real-time features | Session features, click counts, context |
| On-Demand | Milliseconds | Request-time computation | User-item similarity, context features |

### 1.2 Tier Selection Criteria
- **Freshness Requirement**: Session features <5s; user aggregates <5min; preferences <24h
- **Computation Cost**: Streaming is more expensive than batch
- **Accuracy**: Batch uses full data; streaming may miss late events
- **Infrastructure Complexity**: Streaming pipelines are harder to maintain

---

## 2. Batch Feature Computation

### 2.1 Daily Batch Pipeline
```
Event Logs → ETL (Spark) → Feature Aggregation → Feature Store (Offline) → Training Data
```
- **Schedule**: Nightly (2:00–6:00 AM UTC); SLA: complete within 4-hour window
- **Input**: Full day's event logs from Kafka/S3
- **Output**: Feature tables in Parquet on S3 / Hive tables

### 2.2 Common Batch Features
- **User Features**: Interaction counts per category (1d/7d/30d/90d), preference distributions, purchase frequency, AOV, embeddings (retrained weekly)
- **Item Features**: View/click/purchase counts, Bayesian-smoothed CTR/CVR, average rating, trending score, embeddings
- **Cross Features**: User-item affinity, user-category preference, co-occurrence counts

### 2.3 Pipeline Architecture
- **Orchestration**: Apache Airflow / Dagster — DAG definitions with retry, alerting, SLA monitoring
- **Processing**: Apache Spark — date-partitioned incremental processing, broadcast small dimension tables, checkpointing
- **Storage**: Apache Iceberg on S3 — schema evolution, time-travel queries for point-in-time training data

### 2.4 Backfill Pipeline
- **Trigger**: Computation logic changes or new features added
- **Strategy**: Incremental backfill — recompute only affected feature groups
- **Validation**: Compare backfilled vs production features for overlap period

---

## 3. Real-Time Feature Computation

### 3.1 Streaming Architecture
```
Kafka Events → Flink/Spark Streaming → Feature Aggregation → Redis (Online Store)
```
- **Latency**: <5 seconds from event to feature availability
- **State Management**: Exactly-once semantics via checkpointing

### 3.2 Aggregation Patterns
- **Sliding Window Count**: Events in last N minutes (Flink `SlidingEventTimeWindows`)
- **Session Window**: Aggregate within session (30-min inactivity timeout)
- **Tumbling Window**: Fixed non-overlapping buckets (e.g., 5-minute) for rate computation
- **Exponential Moving Average**: `ema_new = α × current + (1-α) × ema_old` — smooths noisy signals

### 3.3 Real-Time Feature Examples
- **Session Features**: Items viewed, dwell time, category focus, cart changes, search queries
- **Recent Activity**: Clicks in last 1h, purchases in last 24h, time since last interaction, velocity
- **Item Popularity**: Views in last 5 min, click rate vs 7-day average, purchase velocity

### 3.4 Flink State Management
- **ValueState**: Single value per key (running count)
- **ListState**: List per key (recent item IDs)
- **MapState**: Key-value map per key (category counts)
- **State TTL**: Auto-expire stale state; RocksDB backend for large state

---

## 4. Near-Real-Time (Micro-Batch)

### 4.1 Architecture
```
Kafka Events → Micro-Batch Accumulator (1-5 min) → Aggregation → Feature Store
```
- **Processing**: Spark Structured Streaming with trigger interval
- **Advantage**: Simpler than true streaming; sufficient for most features

### 4.2 Change Data Capture (CDC)
- **Database CDC**: Debezium captures PostgreSQL/MySQL changes → Kafka → feature store
- **Feature Value CDC**: Only update online store when value actually changes (reduces write amplification)
- **Schema Registry**: Confluent Schema Registry for feature schema evolution

### 4.3 Micro-Batch Examples
- User preference recompute every 5 min; item CTR with Bayesian smoothing; trending score; co-occurrence matrix updates

---

## 5. Feature Transformation

### 5.1 Normalization
- **Min-Max Scaling**: `(x - min) / (max - min)` → [0,1]; sensitive to outliers
- **Z-Score**: `(x - mean) / std` → mean=0, std=1; standard for most ML models
- **Log Transform**: `log(1 + x)` for skewed count features (views, clicks, purchases)
- **Power Transform**: Box-Cox (`x^λ`) or Yeo-Johnson (handles negatives) for Gaussian output
- **Quantile Transform**: Map to uniform/normal distribution; robust to outliers

### 5.2 Encoding
- **One-Hot**: Binary indicator per value; use for low-cardinality (<20 values)
- **Target Encoding**: Replace with mean target value; smoothing prevents overfitting for rare categories
  - `encoding = (count × category_mean + smoothing × global_mean) / (count + smoothing)`
  - Must use out-of-fold estimates during training to prevent leakage
- **Frequency Encoding**: `category_count / total_count` — captures popularity signal
- **Hash Encoding**: `hash(category) % n_buckets` — handles high-cardinality; collision risk
- **Embedding Encoding**: Learned dense vector — most expressive; needs sufficient data per category

### 5.3 Bucketing
- **Equal-Width**: Divide range into N buckets; simple but imbalanced for skewed data
- **Equal-Frequency**: Each bucket has ~same sample count; handles skewed distributions
- **Custom**: Domain-specific (e.g., price: $0–10, $10–50, $50–200, $200+)
- **Tree-Based**: Decision tree finds optimal split points maximizing target separation

### 5.4 Feature Crossing
- **Polynomial**: `x₁ × x₂` for multiplicative interactions; quadratic explosion limits to important pairs
- **Categorical Crosses**: `user_preference × item_category` — critical for linear models
- **Temporal Crosses**: `time_of_day × day_of_week` — captures "weekday mornings" vs "weekend evenings"

---

## 6. Feature Aggregation

### 6.1 User-Level
- Per-user statistics (mean, sum, count, min, max)
- Per-user-category and per-user-window (1h/24h/7d/30d) statistics
- Distribution features: entropy, skewness, kurtosis
- Trend features: linear regression slope of metric over time

### 6.2 Item-Level
- Per-item aggregates over all interacting users
- Per-item-user-segment (new vs returning) and per-item-location/device statistics

### 6.3 Global
- Category-level averages, global baselines (avg CTR/CVR/rating), trending aggregates

### 6.4 Anti-Patterns
- **Data Leakage**: Always use point-in-time joins — aggregate only from events before prediction time
- **Selection Bias**: CTR over shown items biases against unseen items
- **Sparse Aggregation**: Require minimum count threshold; fall back to category/global statistics

---

## 7. Computation Frameworks

### 7.1 Apache Beam
- Unified batch + streaming model; runs on Flink, Spark, or Dataflow
- Excellent windowing API (fixed, sliding, session, custom triggers)
- **Use Case**: Feature computation running in both batch and streaming modes

### 7.2 Apache Flink
- True streaming (not micro-batch); event-time processing with watermarks
- Exactly-once semantics; large state via RocksDB backend
- **Use Case**: Real-time features with complex state logic

### 7.3 Spark Structured Streaming
- Micro-batch processing; same API as batch Spark
- **Limitations**: ~100ms+ latency per micro-batch
- **Use Case**: Near-real-time features (5-minute update frequency)

| Feature | Beam | Flink | Spark Streaming |
|---|---|---|---|
| Latency | Runner-dependent | <100ms | ~100ms–1s |
| State Management | Runner-dependent | Excellent | Good |
| Exactly-Once | Runner-dependent | Yes | Yes |
| Ecosystem | Growing | Mature | Very Mature |

---

## 8. Feature Serving

### 8.1 Pre-Computed Features
- Computed offline; stored in Redis (online) or Parquet (offline)
- **Latency**: <5ms for online lookup
- **Trade-off**: Stale by computation interval; fast and predictable

### 8.2 On-the-Fly Computation
- Computed at request time; must complete within serving budget (<20ms)
- **Use Case**: Context features, user-item similarity
- **Optimization**: Cache frequently computed values; parallelize independent computations

### 8.3 Hybrid Serving (Recommended)
1. Fetch pre-computed user/item features from Redis (<5ms)
2. Compute context features at request time (<1ms)
3. Compute user-item interaction features at request time (<5ms)
4. Concatenate all features for model input

### 8.4 Serving Optimization
- **Feature Batching**: Single Redis pipeline call for all lookups (N round trips → 1)
- **Feature Prefetching**: Pre-fetch features for likely candidates during session
- **TTL-Based Caching**: User features 5-min TTL; item features 1-hour TTL; context no cache

---

## 9. Feature Caching Strategies

### 9.1 Invalidation Policies
- **TTL-Based**: Simple; guarantees maximum staleness; set proportional to update frequency
- **Event-Based**: Precise; requires Kafka → cache invalidator infrastructure
- **Hybrid**: TTL as fallback; event-based for critical features (recommended)

### 9.2 Multi-Level Cache Architecture
- **L1 (In-Process)**: <1ms; HashMap for global stats and category-level features
- **L2 (Redis Cluster)**: <5ms; terabytes for user and item features
- **L3 (Feature Store)**: <10ms; source of truth for all features

### 9.3 Performance Metrics
- **Cache Hit Rate**: Target >95% for L1+L2 combined
- **Cache Staleness**: Monitor average and p99 age of cached values
- **Cache Write Latency**: Target <50ms for streaming updates
- **Eviction**: LRU policy for most use cases

### 9.4 Cache Warming
- Pre-populate on new feature deployment or failure recovery
- Background refresh before TTL expiry for popular entities
- Graceful degradation: serve stale cache if backend unavailable

---

## 10. Feature Freshness Management

### 10.1 Freshness SLAs

| Feature Type | Max Staleness | Update Mechanism |
|---|---|---|
| Session state | 0 seconds | Streaming |
| User recent activity | 5 minutes | Streaming |
| Item real-time popularity | 5 minutes | Streaming |
| User/item daily aggregates | 24 hours | Batch |
| User preferences | 24 hours | Batch |
| Embeddings | 7 days | Batch (retrain) |
| Static metadata | 30 days | On-change |

### 10.2 Monitoring
- Track computation timestamp per feature value
- Alert on p50/p95/p99 staleness exceeding SLA
- Freshness dashboard for pipeline health visualization

### 10.3 Freshness vs Accuracy Trade-off
- More frequent updates = better freshness but higher cost
- Determine optimal interval via A/B testing (1-min vs 5-min vs 15-min vs 1-hour)
- Choose least frequent update maintaining metric parity

### 10.4 Late Event Handling
- **Watermarks**: Flink defines when window is "complete"
- **Grace Period**: Extend window to accept late arrivals
- **Side Outputs**: Capture late events for separate processing
