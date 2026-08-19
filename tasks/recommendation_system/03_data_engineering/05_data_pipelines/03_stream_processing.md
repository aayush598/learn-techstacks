# Apache Flink Deep Dive for Stream Processing

## Overview

Apache Flink is a distributed stream processing framework designed for stateful computations over unbounded data streams. Unlike micro-batch systems (Spark Streaming), Flink processes events one at a time with true streaming semantics, making it the preferred choice for recommendation systems requiring low-latency feature computation, exactly-once guarantees, and complex event-driven logic.

This document covers Flink's core concepts—windows, state, watermarks, time semantics, CEP, Flink SQL, and exactly-once guarantees—at the depth required for production recommendation pipelines.

---

## Windowing in Flink

Windows are the fundamental mechanism for converting infinite streams into finite computations. Flink provides four built-in window types, each with distinct semantics and use cases.

### Tumbling Windows

Tumbling windows partition the stream into non-overlapping, fixed-size segments. Each event belongs to exactly one window.

**Semantics**: For a 5-minute tumbling window, events at `T+0:00` through `T+4:59` belong to window `[T, T+5min)`. The window emits results when the last event arrives (or on a watermark update).

**Recommendation use cases**:
- User click counts per fixed interval
- Item view aggregations per hour
- Purchase rate computation per 15-minute bucket

**Key parameters**:
- `size`: The window duration (e.g., `Time.minutes(5)`).
- **Alignment**: Windows are aligned to the Unix epoch by default. Use `TimeWindow.getJoinOffset()` for custom alignment (e.g., align to business hours).

### Sliding Windows

Sliding windows overlap and are defined by both a window size and a slide interval. Each event may belong to multiple windows.

**Semantics**: For a 1-hour window sliding every 5 minutes, each event appears in 12 windows (`60 / 5 = 12`). Results are emitted every 5 minutes, each reflecting the last hour of data.

**Recommendation use cases**:
- Moving average of click-through rates
- Trending item detection with smoothed scores
- Session-level features with rolling lookback

**Performance consideration**: The number of windows per event is `window_size / slide_interval`. Large ratios (e.g., 24-hour window sliding every minute = 1440 windows per event) create significant state overhead. Consider reducing slide frequency or using custom trigger logic.

### Session Windows

Session windows group events by activity periods, with a configurable gap timeout defining session boundaries.

**Semantics**: If no events arrive for a user within the gap period (e.g., 30 minutes), the session window closes and emits results. New events after the gap start a new session. Adjacent windows within the gap are automatically merged.

**Recommendation use cases**:
- Session-level features: items viewed per session, session conversion rate
- User engagement metrics: session duration, bounce rate
- Real-time personalization: features computed within the current session context

**Session window merging**: When two session windows for the same key are within the gap period, Flink merges them into a single window. This is transparent to the user but affects state management—merged windows accumulate state from both inputs.

### Global Windows

Global windows assign all events with the same key to a single window. They never naturally close—results are emitted only when a custom trigger fires.

**Recommendation use cases**:
- Emitting cumulative aggregates on event count thresholds (e.g., every 100 clicks)
- Custom logic that doesn't fit time-based windows
- Deduplication: accumulate events and emit only unique ones

### Window Triggers and Evictors

**Triggers** determine when a window's results are computed and emitted:

| Trigger | Behavior |
|---|---|
| `EventTimeTrigger` | Fires when the watermark passes the window's end time |
| `ProcessingTimeTrigger` | Fires when the processing time clock reaches the window's end |
| `CountTrigger` | Fires after N events in the window |
| `PurgingTrigger` | Wraps another trigger and clears window state after firing |
| `ContinuousEventTimeTrigger` | Fires periodically based on event time progress |

**Evictors** remove events from windows before or after computation:

- `CountEvictor`: Keeps only the N most recent events.
- `TimeEvictor`: Removes events older than a time threshold.
- `DeltaEvictor`: Removes events based on a delta condition on the event timestamp or value.

---

## Keyed State

Keyed state is state that is scoped to a key and managed by Flink. It is automatically partitioned across the cluster, ensuring all state for a given key resides on a single task manager.

### State Types

| State Type | Data Structure | Use Case |
|---|---|---|
| `ValueState<T>` | Single value | Counters, flags, latest value |
| `ListState<T>` | List of values | Event history, collection aggregation |
| `MapState<K,V>` | Key-value map | Per-key sub-counters, feature vectors |
| `ReducingState<T>` | Aggregated value | Running sum, min, max |
| `AggregatingState<I,O>` | Aggregated with input/output types | Complex aggregations with type transformation |

### State Access Patterns

- **Read-modify-write**: The most common pattern. Read the current state, compute the new value, write it back. Example: incrementing a click counter requires reading the count, adding one, and writing the result.
- **Append-only**: Use `ListState.add()` to accumulate events without reading previous state. Suitable for event history that is periodically processed.
- **Conditional update**: Read state, evaluate a condition, and update only if the condition is met. Example: updating a "last purchase timestamp" only if the new timestamp is greater than the current one.

### State TTL

State TTL automatically expires state entries after a configurable duration. In Flink, TTL is configured at the state descriptor level:

- **Update type**: `OnCreateAndWrite` (default) or `OnReadAndWrite`. The former only resets TTL on state writes; the latter also resets on reads.
- **State visibility**: `NeverReturnExpired` (default) or `ReturnExpiredIfNotCleanedUp`. The former guarantees expired state is never returned; the latter may return stale data before background cleanup runs.
- **Background cleanup**: Flink can periodically scan and remove expired state entries. Cleanup strategies include incremental cleanup (check N entries per access) and full snapshot cleanup (during checkpointing).

### Managed vs. Raw State

- **Managed state**: Flink controls the serialization and storage. Supports all state types, TTL, and efficient serialization. Always use managed state.
- **Raw state**: The user manages serialization. Only supported as `OperatorState` or in custom serializers. Avoid in new code.

---

## Watermarks

Watermarks are Flink's mechanism for tracking event-time progress and determining when windows are complete. A watermark with timestamp `T` signifies that no events with timestamp less than `T` are expected to arrive (with some bounded delay).

### Watermark Generation Strategies

**Periodic watermarks**: Generated at a fixed interval (default: every 200ms). The watermark is typically based on the maximum observed event timestamp minus a configured out-of-orderness bound.

**Punctuated watermarks**: Generated after each event (or each event that meets a condition). More responsive but more computationally expensive.

### Out-of-Orderness Handling

Events may arrive out of order due to network delays, client-side buffering, or reprocessing. The watermark delay (out-of-orderness bound) determines how long Flink waits before considering a window complete:

- **Too short**: Late events are dropped or assigned to side outputs.
- **Too long**: Windows take longer to close, increasing latency.
- **Typical values**: 1–5 seconds for recommendation events, up to 30 seconds for mobile events with unreliable delivery.

### Side Outputs for Late Events

When events arrive after their window has been closed (watermark has passed the window end), Flink can route them to a side output for separate handling:

- **Late event counting**: Monitor the volume of late events to detect system issues.
- **Late event processing**: Recompute window results with late events included (expensive).
- **Late event logging**: Store late events for debugging and audit purposes.

### Watermark Propagation

Watermarks propagate forward through the processing graph. When a window operator receives a watermark, it triggers evaluation of all windows whose end time is <= the watermark. In multi-input operators (e.g., joins), the watermark is the minimum of all input watermarks—the operator cannot proceed until all inputs have progressed.

---

## Event Time vs. Processing Time

Flink supports three time semantics:

| Semantics | Description | Use Case |
|---|---|---|
| **Event Time** | Time when the event was generated at the source | Correct windowed aggregations, reproducibility |
| **Processing Time** | Time when the event is processed by Flink | Low-latency, approximate computations |
| **Ingestion Time** | Time when the event entered Flink | Compromise between correctness and latency |

### Event Time Processing

Event time ensures that windowed computations are deterministic regardless of processing speed or delays. The same input events always produce the same output, enabling:

- **Reproducibility**: Replay the same stream and get identical results.
- **Correctness**: Late events are properly accounted for within the watermark delay.
- **Backfill compatibility**: Use the same pipeline for both real-time and batch reprocessing.

**Tradeoff**: Event time processing requires watermarks, which introduce latency (the watermark delay). For recommendation systems, this latency is typically 1–5 seconds, which is acceptable for most feature computation.

### Processing Time Processing

Processing time uses the local clock of each task manager. It is the simplest and lowest-latency option but provides no guarantees about correctness:

- **Non-deterministic**: Replaying the same input may produce different results.
- **No late event handling**: Events are assigned to windows based on processing time, not their actual occurrence.
- **Use case**: Approximate computations where speed is more important than correctness (e.g., approximate trending item detection).

### Ingestion Time

Ingestion time assigns timestamps when events enter Flink, before any processing. It provides a middle ground:

- **Deterministic**: Same as event time for well-ordered streams.
- **Simpler than event time**: No need for watermarks at the source.
- **Limitation**: Cannot distinguish between events that were generated at different times but arrived simultaneously.

---

## Complex Event Processing (CEP)

Flink CEP enables pattern detection over streams of events. It is useful in recommendation systems for detecting sequences of user actions that indicate specific intents or behaviors.

### Pattern Specification

Patterns are defined as sequences of conditions applied to events:

- **Simple patterns**: Match a single event (e.g., "user clicked on an item").
- **Composite patterns**: Chain multiple conditions with temporal constraints (e.g., "user searched, then clicked within 5 minutes, then purchased within 30 minutes").
- **Quantifiers**: Specify how many times a pattern must occur (once, one or more, exactly N, between M and N).

### Sequence Detection Use Cases

| Pattern | Business Value |
|---|---|
| Search → Click → Purchase (within 30 min) | High-intent conversion funnel |
| View → Add to Cart → Remove (within 1 hour) | Cart abandonment signal |
| 3+ clicks on same category (within 5 min) | Category affinity signal |
| Login → No action for 10 min → Exit | Bounce detection |
| Click → Scroll to bottom → Back → Click different item | Comparison shopping signal |

### CEP Performance Considerations

- **Pattern complexity**: More complex patterns require more state and CPU. Limit the number of patterns and their nesting depth.
- **Timeout handling**: Use `within()` to bound pattern detection time. Without timeouts, partial matches accumulate state indefinitely.
- **Pattern sharing**: Flink optimizes multiple patterns by sharing state for common prefixes. Structure patterns to maximize prefix sharing.

---

## Flink SQL

Flink SQL provides a declarative interface for stream processing, enabling analysts and engineers to write transformations without writing Java/Scala code.

### Core Constructs

- **Table**: An unbounded stream of rows. Defined by a schema (column names and types) and optionally a time attribute.
- **Time attributes**: Declare event time or processing time columns for windowed operations. Event time attributes use `WATERMARK` clauses.
- **Windowed aggregations**: `TUMBLE`, `HOP`, `SESSION` functions for tumbling, sliding, and session windows.
- **Joins**: Inner joins, temporal joins (for versioned dimension tables), and interval joins (for two-stream joins within a time range).
- **Over aggregations**: Window functions for running aggregates (e.g., `SUM(...) OVER (PARTITION BY user_id ORDER BY event_time ROWS BETWEEN 100 PRECEDING AND CURRENT ROW)`).

### Flink SQL for Recommendation Features

| Feature | Flink SQL Pattern |
|---|---|
| Click count per 5 min | `SELECT user_id, COUNT(*) FROM events GROUP BY user_id, TUMBLE(event_time, INTERVAL '5' MINUTE)` |
| Last 10 items viewed | `SELECT user_id, LISTAGG(item_id, ',') WITHIN GROUP (ORDER BY event_time) FROM events GROUP BY user_id` |
| Session duration | `SELECT user_id, SESSION_START(event_time, INTERVAL '30' MINUTE), SESSION_END(event_time, INTERVAL '30' MINUTE) FROM events GROUP BY user_id, SESSION(event_time, INTERVAL '30' MINUTE)` |
| Item popularity (last hour) | `SELECT item_id, COUNT(*) as views FROM events WHERE event_type = 'view' GROUP BY item_id, TUMBLE(event_time, INTERVAL '1' HOUR)` |

### Flink SQL Performance

- **State backend**: Flink SQL operators use keyed state. Ensure RocksDB is configured for large state.
- **State cleanup**: Use `STATE_TTL` hints to expire state for completed sessions or stale aggregations.
- **Query optimization**: Flink's query planner optimizes SQL queries. Use EXPLAIN to verify the execution plan and identify bottlenecks.

---

## Exactly-Once Semantics

Flink achieves exactly-once semantics through distributed snapshots based on the Chandy-Lamport algorithm. Here is how the three phases work:

### Checkpointing Mechanism

1. **Barrier injection**: The checkpoint coordinator sends a barrier (control message) into each source stream at a specific offset.
2. **Barrier propagation**: Barriers flow through the DAG, aligned at operators with multiple inputs. Each operator snapshots its state when it receives barriers from all inputs.
3. **State snapshot**: The operator writes its state to the configured state backend (RocksDB, filesystem, or S3).
4. **Checkpoint completion**: When all operators have reported successful snapshots, the checkpoint is marked complete.

### Checkpoint Configuration

| Parameter | Recommended Value | Rationale |
|---|---|---|
| `checkpointing.interval` | 30–60 seconds | Balance between recovery time and overhead |
| `checkpointing.timeout` | 10 minutes | Allow large checkpoints to complete |
| `min-pause-between-checkpoints` | 30 seconds | Prevent checkpoint overlap |
| `max-concurrent-checkpoints` | 1 | Prevent resource contention |
| `checkpointing.mode` | EXACTLY_ONCE | Required for feature correctness |
| `externalized-checkpoint` | RETAIN_ON_CANCELLATION | Enable recovery after job cancellation |

### Recovery from Failures

On failure, Flink:

1. Cancels all running tasks.
2. Restores state from the latest completed checkpoint.
3. Replays source records from the checkpointed offsets.
4. Resumes processing from the checkpoint state.

The recovery time depends on state size (RocksDB restoration speed) and replay speed (Kafka consumer lag at checkpoint time).

### End-to-End Exactly-Once

True end-to-end exactly-once requires transactional sinks:

- **Two-phase commit sinks**: Flink implements the two-phase commit protocol for Kafka transactions, enabling exactly-once delivery to Kafka topics.
- **Idempotent writes**: Write feature values with version numbers. The sink ignores writes with older versions, ensuring the latest value wins.
- **Semantic sinks**: Some databases support upsert semantics (INSERT or UPDATE), which effectively provide idempotency for single-row writes.

---

## Flink in Production: Operational Considerations

### Job Management

- **Savepoints**: Manual checkpoints used for upgrades, migrations, and scaling. Trigger savepoints before deploying new versions. Use savepoints to migrate jobs between Flink versions or to different clusters.
- **Parallelism changes**: Flink can rescale state when changing parallelism during a savepoint restore. Redistribute keyed state using rescaling or rebalancing modes.
- **State evolution**: When changing the state schema, use Flink's state migration or custom serializers with backward compatibility.

### Performance Tuning

- **Network buffer size**: Increase `taskmanager.network.memory.segment-size` for high-throughput workloads (default: 32KB, recommended: 64KB–128KB).
- **RocksDB tuning**: Enable bloom filters, use prefix seek for keyed state, and tune the block cache size based on working set.
- **SerDe optimization**: Use Flink's native serialization for POJOs. Avoid Kryo for production workloads—slower and uses more memory.
- **Operator chaining**: Enable chaining for operators with similar parallelism and resource needs. Disable for operators that benefit from independent scaling.

### Monitoring

- **Flink Web UI**: Monitor job status, checkpoint history, backpressure, and task metrics.
- **Metrics integration**: Export Flink metrics to Prometheus/Grafana via the `prometheus` reporter.
- **Key metrics**: `checkpointDuration`, `checkpointSize`, `numLateRecordsDropped`, `watermarkLag`, `busyTimeMsPerSecond`.
