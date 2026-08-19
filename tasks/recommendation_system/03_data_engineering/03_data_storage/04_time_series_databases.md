# Time-Series Databases — Recommendation System Metrics and Monitoring

## 1. Why Time-Series Databases for Recommendation Systems

### 1.1 Use Cases

| Use Case | Data Characteristics | Query Pattern | Retention |
|----------|---------------------|---------------|-----------|
| **Real-Time Dashboards** | Metrics per second/minute | Last 1h/24h/7d aggregations | 90 days |
| **Model Monitoring** | Prediction latency, error rates, feature drift | Rolling windows, anomaly detection | 1 year |
| **Business KPI Tracking** | CTR, conversion, revenue per hour/day | Daily/weekly/monthly trends | Indefinite |
| **A/B Test Metrics** | Experiment arm metrics per hour | Comparison across time windows | Experiment lifetime + 6 months |
| **Infrastructure Metrics** | CPU, memory, QPS per second | Real-time alerting, historical analysis | 30 days (hot), 1 year (cold) |
| **User Behavior Analytics** | Aggregated interaction patterns | Cohort analysis, trend detection | 1 year |

### 1.2 Why Not Use PostgreSQL for Time-Series Data

- **Write Amplification**: PostgreSQL's MVCC creates multiple row versions, which is wasteful for append-only time-series data.
- **No Native Retention**: PostgreSQL does not automatically expire old data; manual partition dropping is required.
- **Aggregation Performance**: Time-window aggregations (1-minute, 5-minute, 1-hour rollups) are slower in PostgreSQL than in purpose-built time-series databases.
- **Storage Efficiency**: Time-series databases use columnar compression that achieves 10–50× compression ratios on timestamp-metric data, far exceeding PostgreSQL's row-storage efficiency.

---

## 2. InfluxDB

### 2.1 Architecture Overview

InfluxDB is a purpose-built time-series database using a custom storage engine (TSM — Time-Structured Merge Tree) optimized for time-stamped data.

- **Data Model**: Measurements (tables) → Tags (indexed metadata) → Fields (values) → Timestamps.
- **Storage Engine**: LSM-tree variant with automatic compaction and compression.
- **Query Language**: InfluxQL (SQL-like) or Flux (functional, pipeline-based).

### 2.2 InfluxDB Schema for Recommendation Metrics

```sql
-- Measurement: recommendation serving metrics
-- Tags (indexed, low cardinality): service, endpoint, model_version, experiment_id
-- Fields (high cardinality, not indexed): latency_ms, qps, error_rate, cache_hit_ratio
-- Timestamp: nanosecond precision

-- Write point example
insert recommendation_metrics,
  service="ranking",
  endpoint="/recommendations/home",
  model_version="v2.3.1",
  experiment_id="exp_42"
  latency_ms=45.2,
  qps=12500.0,
  error_rate=0.001,
  cache_hit_ratio=0.72,
  candidate_count=150.0,
  feature_retrieval_ms=8.3,
  model_inference_ms=12.1
  1692432000000000000

-- Measurement: model performance metrics
insert model_metrics,
  model_name="deep_ranking",
  model_version="v2.3.1",
  dataset="production",
  metric_type="hourly"
  auc=0.847,
  ndcg_10=0.723,
  coverage=0.156,
  novelty=0.342,
  diversity=0.618,
  ctr=0.042,
  conversion_rate=0.008
  1692432000000000000

-- Measurement: business metrics
insert business_metrics,
  source="recommendation_engine",
  dimension="overall"
  total_impressions=50000000.0,
  total_clicks=2100000.0,
  total_purchases=400000.0,
  revenue_attributed=12500000.0,
  unique_users=8000000.0
  1692432000000000000
```

### 2.3 InfluxQL Query Examples

```sql
-- Average recommendation latency by endpoint over last 24 hours
SELECT mean(latency_ms), percentile(latency_ms, 95), percentile(latency_ms, 99)
FROM recommendation_metrics
WHERE time > now() - 24h
GROUP BY endpoint, time(5m)

-- Hourly CTR trend for the last 7 days
SELECT mean(ctr) / mean(qps) as hourly_ctr
FROM business_metrics
WHERE time > now() - 7d
GROUP BY time(1h)

-- Model performance comparison between two versions
SELECT mean(auc), mean(ndcg_10)
FROM model_metrics
WHERE model_version =~ /v2.3\.(0|1)/
  AND time > now() - 7d
GROUP BY model_version, time(1d)

-- Anomaly detection: QPS deviation from hourly average
SELECT mean(qps) - percentile(qps, 50) as deviation
FROM recommendation_metrics
WHERE service = "ranking" AND time > now() - 1h
GROUP BY time(1m)
```

### 2.4 InfluxDB Retention Policies

```sql
-- Create retention policies for different data tiers
CREATE RETENTION POLICY "hot_data" ON "recsys" DURATION 7d REPLICATION 1;
CREATE RETENTION POLICY "warm_data" ON "recsys" DURATION 90d REPLICATION 1;
CREATE RETENTION POLICY "cold_data" ON "recsys" DURATION 365d REPLICATION 1;

-- Continuous query for downsampling (1-minute → 1-hour aggregation)
CREATE CONTINUOUS QUERY "cq_hourly_latency" ON "recsys"
BEGIN
  SELECT mean(latency_ms) as avg_latency,
         percentile(latency_ms, 95) as p95_latency,
         percentile(latency_ms, 99) as p99_latency,
         mean(qps) as avg_qps,
         mean(error_rate) as avg_error_rate
  INTO "downsampled"."recommendation_metrics_hourly"
  FROM "recommendation_metrics"
  GROUP BY time(1h), endpoint, model_version
END;
```

---

## 3. TimescaleDB

### 3.1 Why TimescaleDB for Recommendation Metrics

TimescaleDB is a PostgreSQL extension that adds time-series optimizations while retaining full SQL compatibility.

- **Full SQL Support**: Use standard PostgreSQL queries, joins, and functions — no new query language to learn.
- **Automatic Partitioning**: Data is automatically partitioned into hypertables (time-based chunks) without manual partition management.
- **Columnar Compression**: Achieves 10–20× compression on time-series data with automatic compression policies.
- **Continuous Aggregates**: Materialized views that automatically update as new data arrives, enabling fast pre-aggregated queries.
- **Retention Policies**: Automatic data expiry with configurable retention periods.

### 3.2 TimescaleDB Schema for Recommendation Metrics

```sql
-- Create hypertable for recommendation metrics
CREATE TABLE rec_metrics (
    time        TIMESTAMPTZ NOT NULL,
    service     TEXT NOT NULL,
    endpoint    TEXT NOT NULL,
    model_version TEXT,
    latency_ms  DOUBLE PRECISION,
    qps         DOUBLE PRECISION,
    error_rate  DOUBLE PRECISION,
    cache_hit_ratio DOUBLE PRECISION,
    candidate_count INTEGER,
    feature_latency_ms DOUBLE PRECISION,
    inference_latency_ms DOUBLE PRECISION
);

SELECT create_hypertable('rec_metrics', 'time');

-- Create indexes for common query patterns
CREATE INDEX idx_rec_metrics_service_time ON rec_metrics(service, time DESC);
CREATE INDEX idx_rec_metrics_endpoint_time ON rec_metrics(endpoint, time DESC);
CREATE INDEX idx_rec_metrics_model_version ON rec_metrics(model_version, time DESC);

-- Add compression policy (compress data older than 2 days)
ALTER TABLE rec_metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'service, endpoint',
    timescaledb.compress_orderby = 'time DESC'
);
SELECT add_compression_policy('rec_metrics', INTERVAL '2 days');

-- Add retention policy (drop data older than 90 days)
SELECT add_retention_policy('rec_metrics', INTERVAL '90 days');
```

### 3.3 Continuous Aggregates

```sql
-- Create continuous aggregate for hourly metrics
CREATE MATERIALIZED VIEW rec_metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    service,
    endpoint,
    model_version,
    AVG(latency_ms) AS avg_latency_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) AS p95_latency_ms,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) AS p99_latency_ms,
    AVG(qps) AS avg_qps,
    AVG(error_rate) AS avg_error_rate,
    AVG(cache_hit_ratio) AS avg_cache_hit_ratio,
    COUNT(*) AS sample_count
FROM rec_metrics
GROUP BY bucket, service, endpoint, model_version;

-- Add refresh policy (refresh every 5 minutes)
SELECT add_continuous_aggregate_policy('rec_metrics_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '5 minutes',
    schedule_interval => INTERVAL '5 minutes'
);
```

### 3.4 TimescaleDB vs InfluxDB Comparison

| Aspect | TimescaleDB | InfluxDB |
|--------|------------|---------|
| Query Language | Standard SQL | InfluxQL / Flux |
| Compression | Columnar (10–20×) | TSM compression (10–50×) |
| Joins | Full SQL joins | Limited ( Flux supports some joins) |
| ACID Transactions | Yes | No |
| Continuous Aggregates | Materialized views with auto-refresh | Continuous queries |
| Horizontal Scaling | Multi-node (TimescaleDB 2.0+) | Single-node (Enterprise for clustering) |
| Ecosystem | PostgreSQL extensions, pgAdmin, pg_dump | InfluxDB UI, Telegraf, Kapacitor |
| Best For | Teams familiar with SQL; need joins + time-series | Pure time-series workloads; maximum compression |

---

## 4. Real-Time Dashboards

### 4.1 Dashboard Architecture

```
Recommendation Service
    ↓ (emit metrics via StatsD/Prometheus client)
Metrics Collector (Telegraf / Prometheus)
    ↓
Time-Series Database (InfluxDB / TimescaleDB / Prometheus)
    ↓
Visualization (Grafana)
    ↓
Dashboards:
├── Real-Time Serving Dashboard (last 1h, refresh every 10s)
├── Model Performance Dashboard (last 7d, refresh every 5m)
├── Business KPI Dashboard (last 30d, refresh every 1h)
├── Experiment Dashboard (experiment lifetime, refresh every 1h)
└── Infrastructure Dashboard (last 24h, refresh every 30s)
```

### 4.2 Key Dashboard Panels

**Real-Time Serving Dashboard**:
| Panel | Metric | Visualization | Alert Threshold |
|-------|--------|--------------|-----------------|
| Request Rate | QPS by endpoint | Time-series line chart | Drop > 50% from baseline |
| Latency Distribution | P50, P95, P99 by endpoint | Time-series with bands | P99 > 500ms |
| Error Rate | 5xx rate by service | Time-series line chart | > 0.1% |
| Cache Hit Ratio | Hit rate by cache layer | Time-series line chart | < 50% |
| Active Experiments | Count by status | Status panel | Experiment paused unexpectedly |
| Model Version Distribution | Traffic split | Stacked area chart | N/A (informational) |

### 4.3 Alert Configuration

| Alert | Condition | Duration | Severity | Action |
|-------|-----------|----------|----------|--------|
| High Latency | P99 > 500ms | 5 min | SEV-2 | Page on-call |
| High Error Rate | 5xx > 0.5% | 3 min | SEV-1 | Page on-call |
| Low Cache Hit | Cache hit < 30% | 10 min | SEV-3 | Ticket for investigation |
| Model Drift | AUC drop > 5% from baseline | 1 hour | SEV-2 | Page ML engineer |
| Anomaly Detection | > 3σ deviation from hourly average | 5 min | SEV-2 | Auto-investigate |

---

## 5. Retention Policies and Data Lifecycle

### 5.1 Data Retention Tiers

| Data Type | Hot (In-Memory/SSD) | Warm (SSD) | Cold (Object Storage) | Archive |
|-----------|---------------------|------------|----------------------|---------|
| Raw metrics (per-second) | 24 hours | 7 days | — | — |
| Aggregated metrics (per-minute) | 7 days | 30 days | 1 year | — |
| Aggregated metrics (per-hour) | 30 days | 1 year | 5 years | Indefinite |
| Model performance metrics | 30 days | 1 year | 5 years | Indefinite |
| Business KPIs (daily) | 1 year | 5 years | Indefinite | Indefinite |
| A/B test results | Experiment + 6 months | Experiment + 2 years | Indefinite | Indefinite |

### 5.2 Downsampling Strategy

Downsampling reduces storage costs and query latency by aggregating high-frequency data into lower-frequency summaries:

```
Raw (per-second) → 1-minute aggregates (retain 7 days)
                 → 5-minute aggregates (retain 30 days)
                 → 1-hour aggregates (retain 1 year)
                 → 1-day aggregates (retain indefinitely)
```

- **Rollup Pipeline**: A streaming pipeline (Flink, Kafka Streams) or batch job performs the downsampling.
- **Aggregation Functions**: Mean, median, P95, P99, count, sum — depending on the metric.
- **Query Routing**: Queries automatically route to the appropriate granularity based on the time range requested (last 1 hour → raw data; last 30 days → 5-minute aggregates; last year → hourly aggregates).
