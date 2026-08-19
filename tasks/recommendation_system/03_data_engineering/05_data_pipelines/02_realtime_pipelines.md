# Real-Time Data Pipelines for Recommendations

## Overview

Real-time data pipelines are the circulatory system of modern recommendation engines. They ingest user interactions (clicks, views, purchases, searches), enrich them with contextual metadata, compute features on-the-fly, and deliver signals to serving systems with sub-second latency. The canonical architecture follows the pattern: **Kafka → Stream Processor (Flink/Spark Streaming) → Feature Store → Model Serving**.

Unlike batch pipelines that operate on hour- or day-level latency, real-time pipelines must guarantee delivery, maintain exactly-once semantics, handle out-of-order events, and scale to millions of events per second—all while maintaining strict freshness SLAs for downstream features.

---

## Architecture: Kafka → Flink → Feature Store

### Kafka as the Ingestion Layer

Apache Kafka serves as the durable, distributed commit log that decouples event producers from consumers. In a recommendation system, Kafka topics typically correspond to distinct event streams:

| Topic Pattern | Example | Retention | Partitions |
|---|---|---|---|
| `events.{domain}.{type}` | `events.ecommerce.click` | 7 days | 128 |
| `events.{domain}.{type}` | `events.ecommerce.purchase` | 30 days | 64 |
| `events.{domain}.{type}` | `events.ecommerce.search` | 7 days | 128 |
| `features.{domain}.realtime` | `features.ecommerce.user` | 24 hours | 64 |
| `model.{domain}.predictions` | `model.ecommerce.ranker` | 1 hour | 32 |

**Key design decisions for Kafka in recsys pipelines:**

- **Partitioning strategy**: Partition by `user_id` or `item_id` to ensure co-location of related events for stateful processing. Hash-based partitioning on `user_id` guarantees all events for a user land in the same partition, enabling correct windowed aggregations without cross-partition coordination.
- **Topic compaction**: Use compacted topics for materialized views of user profiles or item catalogs where only the latest state matters. This reduces storage and simplifies downstream consumers.
- **Multi-topic consumption**: Flink jobs typically consume from multiple topics simultaneously (clicks, purchases, views) using union operators or side outputs to handle different event types within a single processing topology.
- **Schema evolution**: Use Avro or Protobuf with a Schema Registry to enforce forward/backward compatibility. Breaking schema changes in event streams can silently corrupt downstream feature computations.

### Flink as the Stream Processor

Apache Flink provides the processing backbone with true event-time semantics, exactly-once guarantees via distributed snapshots, and native support for stateful computation at scale. The Flink job reads from Kafka, performs windowed aggregations, computes real-time features, and writes results to the feature store.

### Feature Store as the Serving Layer

The feature store (Feast, Tecton, Hopsworks) materializes computed features into a low-latency serving store (Redis, DynamoDB, Cassandra) for real-time model inference. The pipeline writes features with explicit TTLs—user-level features might persist for 24 hours while session-level features expire after 30 minutes.

---

## Stream Processing Patterns

### Windowing Strategies

Windowing defines how infinite streams are divided into finite chunks for computation. The choice of windowing strategy directly impacts feature freshness, computational cost, and correctness.

| Window Type | Use Case | Example | Latency |
|---|---|---|---|
| **Tumbling** | Fixed-interval aggregations | Click count per 5-min interval | Window size |
| **Sliding** | Moving averages, trend detection | Average purchase velocity over 1-hour, updated every 5 min | Slide interval |
| **Session** | User activity periods | Features for an active user session | Variable |
| **Global** | Cumulative aggregations | Lifetime item view count | Unbounded |

**Tumbling windows** partition the stream into non-overlapping fixed-size segments. For a 5-minute tumbling window computing user click counts, events in `[00:00, 05:00)` form one window, `[05:00, 10:00)` another. This is the simplest and most common pattern for real-time feature computation.

**Sliding windows** overlap and are defined by both a window size and a slide interval. A 1-hour sliding window with a 5-minute slide produces 12 overlapping windows per hour, each computing features over the full hour lookback. This provides smoother feature values but increases computational cost proportionally to `window_size / slide_interval`.

**Session windows** group events by user activity, with a gap timeout defining session boundaries. If a user is inactive for more than the gap threshold (e.g., 30 minutes), the session closes and a new one begins. Session windows are critical for computing session-level features like "number of items viewed in current session" or "session purchase probability."

**Global windows** accumulate all events and are rarely used in isolation. They are useful with custom triggers—for example, emitting a cumulative count every N events rather than on a time basis.

### State Management

Stateful stream processing requires careful management of operator state and keyed state. Flink provides several state backends:

- **HashMapStateBackend**: Stores state in JVM heap. Fast but limited by memory and not fault-tolerant without checkpointing. Suitable for low-latency, small-state workloads.
- **EmbeddedRocksDBStateBackend**: Stores state in RocksDB (on-disk). Handles state larger than memory with acceptable performance degradation. The default choice for production recommendation pipelines.
- **Incremental checkpointing**: Enabled by default with RocksDB. Only checkpoints state diffs since the last checkpoint, reducing checkpoint overhead from minutes to seconds for large state.

**State TTL (Time-To-Live)** is essential for recommendation pipelines to prevent unbounded state growth. User interaction state should expire after a reasonable period—typically 24–72 hours for click history, longer for purchase history. Flink's State TTL feature automatically cleans up expired state entries during access or background cleanup.

**Keyed state** in Flink is partitioned by key (e.g., `user_id`), ensuring all state operations for a given key are co-located on a single task manager. This eliminates the need for distributed transactions but requires careful key design to avoid data skew.

### Exactly-Once Semantics

Exactly-once processing means each input event affects the output exactly once, despite potential failures, retries, or replays. Achieving this requires coordination between three components:

1. **Source (Kafka)**: Track consumer offsets as part of the checkpoint. On recovery, rewind to the last committed checkpoint offset.
2. **Processing (Flink)**: Use distributed snapshots (Chandy-Lamport algorithm) to capture consistent state across all operators. Flink's checkpoint coordinator periodically triggers barriers that propagate through the DAG.
3. **Sink (Feature Store)**: Use idempotent writes. Each feature update includes a monotonically increasing event timestamp, and the sink ignores stale updates. Alternatively, use two-phase commit sinks (e.g., KafkaTransactionalProducer) for transactional delivery.

**Common pitfalls breaking exactly-once:**

- **Non-idempotent sinks**: Writing to a database that doesn't handle duplicate writes will produce incorrect feature values on recovery.
- **External system calls**: Calling external APIs during processing that have side effects (sending emails, charging credit cards) cannot be made exactly-once. Use idempotency keys or at-least-once with deduplication.
- **Checkpoint timeout**: If checkpointing takes longer than the checkpoint interval, checkpoints overlap and processing stalls. Monitor checkpoint duration and tune accordingly.

---

## Real-Time Feature Computation

### Feature Types and Latency Requirements

| Feature Category | Example | Latency Requirement | Refresh Rate |
|---|---|---|---|
| User interaction aggregates | Click count (last 1h) | < 1 minute | Continuous |
| Item popularity | Views in last 24h | < 5 minutes | Every 5 min |
| User-item affinity | Co-occurrence score | < 10 minutes | Every 10 min |
| Contextual features | Time of day, device | < 1 second | Real-time |
| Cross-session features | Purchase frequency (30d) | < 1 hour | Batch refresh |
| Model predictions | CTR prediction | < 50ms | On-request |

### Real-Time Aggregation Patterns

**Counting**: Maintain running counts of user actions within time windows. A Flink `KeyedProcessFunction` with timer-based state cleanup computes counts efficiently. For example, "number of searches in last 30 minutes" uses a list state of timestamps, with a timer set for the oldest event's expiry.

**Sessionization**: Group consecutive user events into sessions using session windows with a gap timeout. Compute session-level features like session duration, items viewed per session, and session conversion rate. Session windows in Flink automatically merge adjacent windows when events arrive within the gap.

**Rate of change**: Compute the derivative of cumulative metrics—for example, "click rate acceleration" as the difference in click rate between the current and previous time window. This requires maintaining two tumbling windows simultaneously and computing the difference on each emission.

**Top-K maintenance**: Track the most popular items, most active users, or trending topics in real-time using Flink's `TopK` operator or custom priority queue state. Useful for computing trending features and popular item lists.

### Real-Time Event Enrichment

Raw events typically lack the context needed for feature computation. Enrichment joins events with dimension data:

- **User enrichment**: Add user demographics, preferences, membership tier to click events. This is typically a broadcast join with a small lookup table (user profile) stored in Flink's broadcast state.
- **Item enrichment**: Add item category, price, seller, popularity tier. Use a regular join with an item dimension table, or cache item metadata in state for frequently accessed items.
- **Contextual enrichment**: Add weather data, holiday flags, device information, geographic context. These are often time-varying and require periodic refresh of the lookup tables.

**Enrichment latency considerations:**

- Broadcast state joins: O(1) lookup, best for small reference datasets (< 1GB).
- Interval joins: Join two streams within a time window, useful when both sides are streaming.
- Temporal table joins: Join with a versioned dimension table at the event's timestamp, providing point-in-time correctness.

---

## Latency Requirements

Recommendation system pipelines have tiered latency requirements based on the feature's role in the serving path:

| Tier | Latency | Features | Pipeline |
|---|---|---|---|
| **Hot path** | < 100ms | Real-time features for model serving | Kafka → Flink → Redis |
| **Warm path** | < 5 minutes | Near-real-time aggregations | Kafka → Flink → Feature Store |
| **Cold path** | < 1 hour | Batch-computed features | Kafka → Spark → Data Lake → Feature Store |
| **Frozen path** | Daily | Complex batch features | Airflow → Spark → Feature Store |

The hot path is the most challenging—features must be available in the feature store within 100ms of the triggering event. This requires:

- **Pre-computation**: Instead of computing features on-demand, pre-compute and store all possible feature values. Trade storage for latency.
- **Write-through caching**: Write to both the feature store and a hot cache (Redis) simultaneously. The serving layer reads from the hot cache.
- **Predictive prefetching**: Based on user navigation patterns, prefetch likely-needed features before they are requested.

---

## Scaling Streaming Workloads

### Horizontal Scaling

- **Kafka partitioning**: Scale ingestion by adding partitions. Each partition is consumed by exactly one Flink task. The number of Kafka partitions should be a multiple of the Flink parallelism.
- **Flink parallelism**: Each operator's parallelism can be configured independently. CPU-intensive operators (feature computation) may need higher parallelism than I/O-intensive operators (Kafka source).
- **State backend scaling**: RocksDB state can be distributed across multiple disks and task managers. Use Flink's rescaling to redistribute state when scaling up/down.

### Backpressure Management

Backpressure occurs when a downstream operator cannot keep up with the upstream's emission rate. Flink detects backpressure via latency markers and automatically slows down source operators. Key mitigation strategies:

- **Asynchronous I/O**: Use Flink's async I/O operator for external lookups (enrichment joins) to avoid blocking on network calls.
- **Buffer timeout tuning**: Reduce `buffer-timeout` for lower latency at the cost of throughput, or increase it for higher throughput.
- **Operator chaining**: Disable chaining for operators with different processing characteristics to allow independent scaling.

### Resource Management

| Resource | Recommendation | Rationale |
|---|---|---|
| CPU | 4–8 cores per task slot | Feature computation is CPU-bound |
| Memory | 8–16 GB per task slot | RocksDB needs memory for block cache |
| Network | 10 Gbps+ | High throughput for shuffle operations |
| Disk | NVMe SSD | RocksDB performance depends on disk I/O |
| Heap | 2–4 GB | JVM overhead, serialization buffers |

### Monitoring and Alerting

Critical metrics to monitor in real-time pipelines:

- **End-to-end latency**: Time from event creation to feature availability. Alert if p99 > SLA threshold.
- **Kafka consumer lag**: Number of unconsumed events per partition. Alert if lag exceeds 10,000 events or 5 minutes of backlog.
- **Checkpoint duration and size**: Increasing checkpoint size indicates state growth. Alert if checkpoint duration exceeds checkpoint interval.
- **Feature freshness**: Timestamp of the latest feature update per user/item. Alert if freshness degrades beyond the feature's SLA.
- **Throughput**: Events processed per second per operator. Sudden drops indicate processing bottlenecks.
- **Error rate**: Failed processing attempts. Even 0.1% errors can corrupt feature values for millions of users.

---

## Operational Best Practices

1. **Idempotent writes**: Design every sink operation to be safely replayable. Use event timestamps or sequence numbers as version identifiers.
2. **Graceful degradation**: When real-time features are unavailable (pipeline failure), fall back to the most recent batch-computed features rather than failing the recommendation request.
3. **Schema evolution**: Always use schema registries with compatibility checks. Never remove or rename fields in existing event schemas without a migration period.
4. **Dead letter queues**: Route failed events to a dead letter queue for investigation rather than dropping them. Monitor DLQ depth as a pipeline health indicator.
5. **Canary deployments**: Roll out pipeline changes to a subset of partitions first. Monitor feature quality metrics before full rollout.
6. **Chaos engineering**: Periodically kill Flink task managers, partition Kafka brokers, and inject network latency to validate pipeline resilience.
