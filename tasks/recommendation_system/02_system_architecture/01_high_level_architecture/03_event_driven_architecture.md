# Event-Driven Architecture for Recommendation Systems

## 1. Why Event-Driven Architecture

### 1.1 The Nature of Recommendation Data
Recommendation systems are fundamentally event-driven:
- **User actions generate events**: Every click, view, purchase, rating, search is an event
- **Item changes generate events**: New items, updated metadata, removed items are events
- **Model changes generate events**: New model deployment, configuration changes are events
- **Feature changes generate events**: Feature computation completion, feature drift alerts are events

### 1.2 Benefits for Recommendation Systems
- **Natural data flow**: User actions → events → features → model updates → recommendations
- **Temporal ordering**: Events maintain chronological order for sequence-aware recommendations
- **Replay capability**: Replay historical events for model retraining and debugging
- **Decoupling**: Producers and consumers evolve independently
- **Scalability**: Event streams scale independently of request processing
- **Auditability**: Complete audit trail of all system activities

---

## 2. Event Types and Taxonomy

### 2.1 User Interaction Events
```
Event: UserActionEvent
  - event_id: UUID
  - user_id: string
  - item_id: string
  - action_type: enum (view, click, purchase, like, share, bookmark, rate, skip, report, search)
  - timestamp: timestamp
  - context:
    - device_type: string
    - platform: string (web, ios, android)
    - session_id: string
    - page_location: string
    - referrer: string
  - metadata:
    - dwell_time_ms: integer
    - scroll_depth: float
    - position_in_list: integer
    - search_query: string (for search actions)
    - rating_value: float (for rating actions)
```

### 2.2 Item Lifecycle Events
```
Event: ItemEvent
  - event_id: UUID
  - item_id: string
  - event_type: enum (created, updated, removed, deprecated, availability_changed)
  - timestamp: timestamp
  - changes: map of field_name -> {old_value, new_value}
```

### 2.3 Model Events
```
Event: ModelEvent
  - event_id: UUID
  - model_id: string
  - model_version: string
  - event_type: enum (trained, validated, deployed, promoted, rolled_back, archived)
  - timestamp: timestamp
  - metrics: map of metric_name -> value
  - configuration: map of param_name -> value
```

### 2.4 Feature Events
```
Event: FeatureEvent
  - event_id: UUID
  - feature_group: string
  - event_type: enum (computed, updated, stale, error)
  - timestamp: timestamp
  - feature_count: integer
  - freshness_ms: integer
```

### 2.5 System Events
```
Event: SystemEvent
  - event_id: UUID
  - event_type: enum (health_check, alert, config_change, deployment)
  - component: string
  - severity: enum (info, warning, error, critical)
  - timestamp: timestamp
  - details: map
```

---

## 3. Event Schema Design

### 3.1 Schema Evolution Strategies
- **Backward Compatibility**: New schema can read old events
- **Forward Compatibility**: Old schema can read new events (ignoring unknown fields)
- **Full Compatibility**: Both backward and forward compatible
- **Breaking Changes**: Require versioned topics or new topics

### 3.2 Schema Evolution Rules
1. Never remove a field — mark it as deprecated instead
2. Never change the type of an existing field
3. Always provide default values for new optional fields
4. Use namespace prefixes for event types
5. Include a schema version in every event envelope
6. Test schema changes with compatibility mode before deployment

### 3.3 Event Envelope Pattern
Every event should be wrapped in a standard envelope:
```
Envelope:
  - schema_version: string
  - event_type: string
  - event_id: UUID
  - timestamp: timestamp
  - source: string (service name)
  - correlation_id: UUID (for request tracing)
  - payload: bytes (serialized event)
```

---

## 4. Apache Kafka as Event Backbone

### 4.1 Topic Design for Recommendations

| Topic | Partitions | Retention | Purpose |
|---|---|---|---|
| user.interactions.raw | 128 | 30 days | Raw user interaction events |
| user.interactions.processed | 128 | 7 days | Validated and enriched interactions |
| items.events | 32 | 90 days | Item lifecycle events |
| features.computed.batch | 16 | 7 days | Batch feature computation results |
| features.computed.streaming | 64 | 3 days | Streaming feature computation results |
| models.events | 8 | 365 days | Model lifecycle events |
| recommendations.served | 64 | 7 days | Recommendations served to users |
| recommendations.feedback | 64 | 30 days | Recommendation outcome events |

### 4.2 Partitioning Strategy
- **User interaction topics**: Partition by user_id for ordering guarantees per user
- **Item event topics**: Partition by item_id for ordering guarantees per item
- **Feature topics**: Partition by entity_id (user or item depending on feature group)
- **Model topics**: Partition by model_id for ordering per model

### 4.3 Consumer Group Design
- **Feature computation consumers**: One group per feature pipeline
- **Model training consumers**: One group for training data assembly
- **Analytics consumers**: One group for real-time dashboards
- **Search index consumers**: One group for index updates

---

## 5. CQRS Pattern for Recommendations

### 5.1 Command Side (Write Model)
- **Purpose**: Process user actions, update profiles, manage configurations
- **Database**: PostgreSQL with optimized write schema
- **Events Generated**: UserActionEvent, ProfileUpdateEvent, ConfigChangeEvent
- **Consistency**: Strong consistency within the command model
- **Optimistic Concurrency**: Version fields for conflict detection

### 5.2 Query Side (Read Model)
- **Purpose**: Serve recommendation queries, analytics dashboards, search results
- **Database**: Redis (hot data), ClickHouse (analytics), Elasticsearch (search)
- **Events Consumed**: All events from the event log
- **Consistency**: Eventual consistency — reads may lag writes by seconds to minutes
- **Materialized Views**: Pre-computed views optimized for specific query patterns

### 5.3 Synchronization
- **Event Store**: Kafka serves as the single source of truth
- **Projections**: Event handlers build read models from event stream
- **Catch-up**: Read models can be rebuilt from event log for debugging
- **Real-time**: Kafka Connect for low-latency synchronization to read stores

---

## 6. Event Replay and Recovery

### 6.1 Replay Use Cases
- **Model Retraining**: Replay historical interactions to generate training data
- **Feature Recomputation**: Replay events to recompute features with updated logic
- **Debugging**: Replay events to reproduce and diagnose issues
- **New Consumer Onboarding**: Replay historical events to bootstrap new data stores
- **Bug Recovery**: Replay events to fix corrupted data stores

### 6.2 Replay Architecture
- **Event Retention**: Kafka retains events for configurable periods (7-90 days)
- **Compacted Topics**: For entity state topics, compaction keeps only latest state
- **Snapshots**: Periodic snapshots to avoid replaying entire history
- **Checkpointed Replay**: Consumers track offset for resumable replay
- **Parallel Replay**: Partition-level parallelism for fast replay

### 6.3 Recovery Procedures
1. Identify affected consumers and their last good offset
2. Stop affected consumers
3. Reset consumer offsets to recovery point
4. Restart consumers and monitor catch-up progress
5. Verify data consistency after catch-up completes

---

## 7. Exactly-Once Semantics

### 7.1 The Challenge
- Recommendation systems need accurate event processing — duplicate events cause incorrect feature computation and model training data contamination
- At-least-once delivery can cause duplicate processing
- Exactly-once delivery requires coordination between producer, broker, and consumer

### 7.2 Implementation Strategies
- **Idempotent Producers**: Kafka producer retries with same sequence number
- **Transactional Producers**: Kafka transactions for atomic multi-topic writes
- **Idempotent Consumers**: Deduplication using event_id in consumer logic
- **Outbox Pattern**: Write event to database and outbox atomically, then publish from outbox

### 7.3 Recommendation-Specific Considerations
- **Impression events**: Duplicates cause inflated impression counts — deduplication critical
- **Click events**: Duplicates cause incorrect CTR calculations — deduplication critical
- **Feature computation**: Idempotent aggregation functions handle duplicates gracefully
- **Model training**: Duplicate events in training data cause biased models — deduplication before training

---

## 8. Dead Letter Queues and Error Handling

### 8.1 Error Categories
- **Transient Errors**: Network timeouts, temporary resource exhaustion — retry with backoff
- **Permanent Errors**: Schema validation failure, data corruption — route to DLQ
- **Poison Messages**: Events that cause consumer crashes — route to DLQ after max retries

### 8.2 DLQ Architecture
- **DLQ Topic**: Separate Kafka topic for failed events (e.g., `user.interactions.dlq`)
- **DLQ Metadata**: Include original topic, partition, offset, error reason, retry count
- **DLQ Processing**: Separate consumer to analyze and reprocess failed events
- **DLQ Monitoring**: Alert on DLQ depth; track error rates by topic and consumer
- **DLQ Retention**: Longer retention than main topics for debugging

### 8.3 Retry Strategies
- **Exponential Backoff**: Increase delay between retries (1s, 2s, 4s, 8s, ...)
- **Dead Letter after N Retries**: After max retries, route to DLQ
- **Rate-limited Retries**: Limit retry throughput to prevent overwhelming downstream
- **Circuit Breaker**: Stop retries when downstream service is degraded

---

## 9. Event Ordering and Consistency

### 9.1 Ordering Guarantees
- **Per-Partition Ordering**: Kafka guarantees order within a partition
- **Per-User Ordering**: Partition by user_id ensures events for the same user are ordered
- **Cross-User Ordering**: Not guaranteed and typically not needed
- **Global Ordering**: Impractical at scale; not required for most recommendation use cases

### 9.2 When Ordering Matters
- **Session reconstruction**: Events within a session must be ordered by timestamp
- **Sequence models**: Training data for sequence models requires temporal ordering
- **Feature computation**: Some features depend on event order (e.g., "time since last click")
- **State management**: State updates must be processed in order

### 9.3 Out-of-Order Event Handling
- **Event Time vs Processing Time**: Use event timestamps, not processing timestamps
- **Watermarks**: Flink watermarks for handling late-arriving events
- **Grace Period**: Allow events to arrive within a grace period before finalizing window computations
- **Late Event Handling**: Option to update previously computed results or discard late events

---

## 10. Event-Driven Feature Computation

### 10.1 Streaming Feature Pipeline
1. User interaction event published to Kafka
2. Flink consumer processes event in real-time
3. Computes rolling window aggregates (e.g., user's last 10 clicks, items interacted with in last hour)
4. Updates feature store (Redis) with latest feature values
5. Feature available for next recommendation request within seconds

### 10.2 Advantages Over Batch Features
- **Freshness**: Features update within seconds vs hours for batch
- **Responsiveness**: System adapts to user behavior changes immediately
- **Session Awareness**: Capture within-session behavior for better recommendations

### 10.3 Challenges
- **State Management**: Maintaining windowed state across many users requires careful memory management
- **Exactly-Once**: Ensuring each event is processed exactly once for accurate aggregates
- **Late Events**: Handling events that arrive after window closure
- **Resource Management**: Streaming jobs run continuously and require careful resource allocation

---

## 11. Event Monitoring and Observability

### 11.1 Key Metrics
- **Producer Metrics**: Events produced/sec, error rate, latency, serialization errors
- **Broker Metrics**: Partition count, under-replicated partitions, disk usage, request latency
- **Consumer Metrics**: Consumer lag, events consumed/sec, processing latency, error rate
- **Event Quality**: Schema validation errors, duplicate events, late events

### 11.2 Consumer Lag Monitoring
- **Critical Lag Threshold**: Alert when consumer lag exceeds time-based threshold (e.g., 5 minutes)
- **Growing Lag Alert**: Alert when lag is monotonically increasing for N minutes
- **Lag Dashboard**: Real-time visualization of lag across all consumer groups
- **Impact Assessment**: Map consumer lag to downstream feature freshness and recommendation quality

### 11.3 Event Flow Visualization
- **End-to-End Tracing**: Correlation ID through entire event flow
- **Dependency Mapping**: Visualize event flow between services
- **Bottleneck Detection**: Identify slow consumers and overwhelmed topics
- **Anomaly Detection**: Alert on unusual event volume patterns
