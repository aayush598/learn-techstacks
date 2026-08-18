# Batch Inference for Recommendations

## Overview

Batch inference pre-computes recommendation results for large user populations on a scheduled basis, storing results for fast retrieval at serving time. Unlike real-time inference which computes predictions on-demand, batch inference trades freshness for throughput and cost efficiency. This document covers batch scoring architectures, scheduling strategies, incremental scoring, and the tradeoffs between batch and real-time approaches.

---

## When Batch Inference Makes Sense

### Use Cases

| Use Case | Freshness Requirement | Volume | Why Batch |
|----------|----------------------|--------|-----------|
| Email recommendations | Daily (send at 8am) | Millions | Massive parallelism, low latency at send time |
| "Because you watched" | Hourly | Millions | Pre-compute similarity-based recs |
| Push notification triggers | Hourly-Daily | Hundreds of thousands | Event-driven, not latency-sensitive |
| User profile recommendations | Daily | Full user base | Compute once, serve from cache |
| Catalog-wide re-ranking | Weekly | Full catalog | Expensive ranking model |
| Social feed recommendations | Hourly | Millions | Feed doesn't change per-request |
| Offline evaluation | On-demand | Test set | Evaluation doesn't require real-time |

### Cost Comparison

| Approach | Cost per 1M predictions | Latency at serve time |
|----------|------------------------|----------------------|
| Real-time inference | $5-50 (GPU compute) | 1-50ms |
| Batch inference | $0.5-5 (distributed compute) | < 1ms (cache lookup) |
| Pre-computed + cache | $0.1-1 (storage) | < 1ms |

---

## Batch Scoring Pipeline Architecture

### End-to-End Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Data Source  │ →   │  Feature     │ →   │  Model       │
│  (Events,    │     │  Engineering │     │  Inference   │
│   Catalog)   │     │  (Spark)     │     │  (Distributed)│
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
┌──────────────┐     ┌──────────────┐     ┌──────┴───────┐
│  Serving      │ ←   │  Filtering   │ ←   │  Candidate   │
│  (Redis/KV)  │     │  & Ranking   │     │  Generation   │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Pipeline Stages

#### Stage 1: Data Collection and Preprocessing

```
Raw Interaction Logs (Kafka → S3/Data Lake)
      ↓
Spark ETL Job:
  - Deduplicate events
  - Filter bot traffic
  - Compute session boundaries
  - Join with item metadata
      ↓
Processed Training/Feature Data
```

#### Stage 2: Feature Engineering

```
Feature Pipeline (Spark/Feature Store):
  - User historical features (aggregated preferences)
  - Item content features (embeddings, attributes)
  - Contextual features (time-based, trending)
  - Cross features (user × item interactions)
      ↓
Feature Matrix (user × feature dimensions)
```

#### Stage 3: Model Inference

```
Model Inference Options:
  - Spark MLlib (distributed scoring)
  - Spark + Pandas UDF (vectorized inference)
  - Ray (distributed Python inference)
  - Dask (parallel computing)
  - Native batch API (framework-specific)
      ↓
Raw Scores (user × item × score)
```

#### Stage 4: Post-processing and Ranking

```
Post-processing:
  - Apply business rules (exclude purchased, blacklisted)
  - Diversity re-ranking (MMR or DPP)
  - Slot allocation (mix of categories)
  - Boost new/trending items
      ↓
Final Recommendations (user → [item₁, item₂, ..., itemₖ])
```

#### Stage 5: Storage and Serving

```
Storage Options:
  - Redis/Memcached (sub-ms latency)
  - DynamoDB/Cassandra (managed, scalable)
  - Feature Store (integrated with feature pipeline)
  - Object Storage (S3 + CDN for non-real-time)
      ↓
Serving Layer:
  - API reads from cache on user request
  - No model inference needed (pre-computed)
```

---

## Spark-Based Batch Inference

### PySpark with Pandas UDF

```python
import pyspark.sql.functions as F
from pyspark.sql.types import *
import pandas as pd

# Define UDF for batch inference
@F.pandas_udf(ArrayType(FloatType()))
def batch_predict(user_ids: pd.Series, item_features: pd.DataFrame) -> pd.Series:
    model = load_model()  # Load model once per partition
    scores = model.predict(user_ids, item_features)
    return pd.Series(scores.tolist())

# Apply across Spark DataFrame
results = user_item_pairs.withColumn(
    "scores",
    batch_predict("user_id", "item_features")
)
```

### Spark MLlib Distributed Scoring

```python
from pyspark.ml.recommendation import ALS

# Load trained model
als_model = ALS.load("hdfs:///models/als_model")

# Generate recommendations for all users
recommendations = als_model.recommendForAllUsers(50)

# Save results
recommendations.write.parquet("hdfs:///recommendations/daily/")
```

### Performance Optimization

| Technique | Description | Speedup |
|-----------|-------------|---------|
| Partition by user | Each partition processes one user's recommendations | 2-5× |
| Broadcast model | Send model to all executors | Avoids shuffle |
| Cache features | Reuse feature computation across iterations | 3-10× |
| Adaptive query execution | Spark dynamically optimizes queries | 1.5-2× |
| Columnar storage | Use Parquet/ORC for feature data | 2-5× I/O |

### Handling Large-Scale Scoring

```
Total items: 10M
Total users: 100M
User-item pairs to score: 10M × 100M = 10¹⁵ (impossible to score all)

Solution: Two-phase approach
  Phase 1: Candidate generation (reduce to 1000 items per user)
    - Collaborative filtering, ANN search, popular items
    - Scoring: 100M × 1000 = 10¹¹ (feasible with Spark)
  
  Phase 2: Ranking (score all candidates per user)
    - Deep model ranking on candidates
    - Scoring: 100M × 1000 = 10¹¹ (parallel across cluster)
```

---

## Incremental Scoring

### Motivation

Full recomputation of all recommendations is expensive. Incremental scoring updates only the recommendations affected by new data.

### Incremental Strategies

#### User-Level Incremental

```
When: New interaction event for user U
What: Recompute recommendations for user U only
How:
  1. Detect user has new events (Kafka trigger)
  2. Fetch user's updated feature vector
  3. Run model inference for user U
  4. Update stored recommendations for user U
```

#### Item-Level Incremental

```
When: New item added or item metadata updated
What: Update recommendations for users who might like the new item
How:
  1. Identify affected users (similarity-based or category-based)
  2. Score new item against affected users
  3. Insert into affected users' recommendation lists
  4. Re-rank and trim to top-K
```

#### Time-Window Incremental

```
Maintain two recommendation sets:
  - Stable set: Computed weekly (full retraining)
  - Fresh set: Computed hourly (recent interactions only)

At serve time:
  - Merge stable and fresh sets
  - Weight by recency and confidence
  - Deduplicate and re-rank
```

### Incremental vs Full Recomputation

| Aspect | Incremental | Full Recomputation |
|--------|------------|-------------------|
| Compute cost | Lower (per update) | Higher (batch) |
| Freshness | Higher (near real-time) | Lower (periodic) |
| Consistency | Eventual consistency | Strong consistency |
| Implementation | More complex | Simpler |
| Data drift handling | Automatic | Requires retraining |
| Coverage | May miss long-term patterns | Complete |

---

## Result Caching

### Cache Architecture

```
┌──────────────────────────────────────┐
│            Cache Layers              │
├──────────┬──────────┬───────────────┤
│ L1: App  │ L2: Redis│ L3: Feature  │
│ Cache    │ Cluster  │ Store        │
│ (1MB)    │ (100GB)  │ (10TB)       │
│ <0.01ms  │ <1ms     │ <5ms         │
└──────────┴──────────┴───────────────┘
```

### Cache Design

| Aspect | Recommendation | Rationale |
|--------|---------------|-----------|
| Key design | `rec:{user_id}:{version}` | Version for cache invalidation |
| Value format | Serialized list of item_ids + scores | Compact representation |
| TTL | 1-24 hours based on use case | Balance freshness vs cost |
| Invalidation | Event-driven (new interaction) or TTL | Immediate for important events |
| Replication | 3+ replicas per shard | High availability |
| Sharding | Consistent hashing on user_id | Even distribution |

### Cache Hit Optimization

| Strategy | Description | Cache Hit Rate |
|----------|-------------|---------------|
| Popularity-based caching | Cache recs for active users | 60-80% |
| Pre-compute all | Compute for every user | 95-100% |
| Tiered caching | Hot users in fast cache, cold in slow | 80-95% |
| Predictive caching | Pre-compute before user request | 70-90% |

---

## Batch vs Real-Time Tradeoffs

### Decision Matrix

| Factor | Favor Batch | Favor Real-Time |
|--------|------------|-----------------|
| Freshness needs | Minutes to hours acceptable | Milliseconds required |
| User interaction frequency | Infrequent visitors | Frequent, session-based |
| Compute budget | Limited GPU budget | Sufficient GPU budget |
| Personalization depth | Shallow (population-level) | Deep (per-interaction) |
| Infrastructure maturity | Basic data pipeline | Advanced streaming |
| Cost sensitivity | Cost is primary concern | Latency is primary concern |

### Hybrid Architecture (Production Standard)

```
┌─────────────────────────────────────────┐
│           Serving Layer                  │
│                                          │
│  ┌────────────────┐  ┌────────────────┐ │
│  │ Batch Layer     │  │ Real-Time Layer│ │
│  │ (Redis cache)   │  │ (GPU inference)│ │
│  │ Pre-computed    │  │ On-demand      │ │
│  │ recommendations │  │ predictions    │ │
│  └───────┬────────┘  └───────┬────────┘ │
│          │                   │           │
│          └───────┬───────────┘           │
│                  ↓                       │
│         Merge + Re-rank                  │
│         (combines both sources)          │
└─────────────────────────────────────────┘
```

### Merge Strategy

```
Final score = α × batch_score + (1 - α) × real_time_score

Where:
  α = f(user_activity, item_recency, compute_budget)
  
For active users: Higher α (batch provides good baseline)
For new users: Lower α (real-time adapts faster)
For new items: Real-time only (no batch data yet)
```

---

## Scheduling and Orchestration

### Airflow DAG for Batch Scoring

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

with DAG("daily_recommendations", schedule_interval="0 2 * * *") as dag:
    
    extract_events = PythonOperator(
        task_id="extract_events",
        python_callable=extract_recent_events
    )
    
    compute_features = PythonOperator(
        task_id="compute_features",
        python_callable=compute_user_item_features
    )
    
    generate_candidates = BashOperator(
        task_id="generate_candidates",
        command="spark-submit --master yarn candidate_generation.py"
    )
    
    rank_candidates = BashOperator(
        task_id="rank_candidates",
        command="spark-submit --master yarn ranking_model.py"
    )
    
    apply_business_rules = PythonOperator(
        task_id="apply_rules",
        python_callable=apply_filtering_and_diversity
    )
    
    load_to_cache = PythonOperator(
        task_id="load_cache",
        python_callable=write_to_redis
    )
    
    extract_events >> compute_features >> generate_candidates
    generate_candidates >> rank_candidates >> apply_business_rules
    apply_business_rules >> load_to_cache
```

### Scheduling Patterns

| Pattern | Schedule | Use Case |
|---------|----------|----------|
| Daily full recompute | 2am daily | Email recs, daily digest |
| Hourly incremental | Every hour | Trending items, session updates |
| Event-driven | On new event | User cold start, new items |
| Weekly deep scoring | Sunday 3am | Full catalog re-ranking |
| On-demand | Triggered by API | A/B test evaluation |

### SLA Management

| Metric | SLA Target | Monitoring |
|--------|-----------|------------|
| Pipeline completion | < 4 hours (daily job) | Airflow monitoring |
| Data freshness | < 24 hours | Timestamp on last update |
| Coverage | > 95% of active users | Coverage report |
| Cache hit rate | > 80% | Redis metrics |
| Quality degradation | < 1% vs real-time | Weekly A/B comparison |

---

## Quality Assurance for Batch Results

### Validation Checks

| Check | Description | Action on Failure |
|-------|-------------|-------------------|
| Coverage | % of users with recommendations | Alert, extend batch window |
| Null/empty check | Users with empty recommendation lists | Fallback to popularity-based |
| Duplicate check | Repeated items in recommendation lists | Deduplicate |
| Freshness | Age of items in recommendations | Boost newer items |
| Diversity | Intra-list diversity metric | Apply diversity re-ranking |
| Score distribution | Expected score ranges | Investigate model output |
| Staleness | Time since last batch update | Trigger re-scoring |

### A/B Testing Batch Results

```
Control: Current batch recommendations (daily update)
Treatment: New batch recommendations (new model/features)

Metrics:
  - CTR lift
  - Conversion rate
  - User engagement time
  - Recommendation diversity
  - Coverage improvement

Duration: 1-2 weeks (batch cycles)
Statistical test: Two-proportion z-test for CTR
```

---

## Cost Optimization

### Compute Cost Reduction

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Spot/preemptible instances | 60-80% | Job may be interrupted |
| Right-sizing | 20-40% | Must profile accurately |
| Incremental scoring | 50-70% | Implementation complexity |
| Model distillation | 30-50% | Slight quality loss |
| Caching intermediate results | 20-40% | Storage cost |

### Storage Cost Reduction

| Strategy | Savings | Notes |
|----------|---------|-------|
| Compressed serialization | 50-70% | Use protobuf, msgpack |
| Tiered storage | 30-50% | Hot in Redis, cold in S3 |
| TTL-based deletion | Variable | Delete stale recommendations |
| Delta encoding | 60-80% | Store only changes between versions |
