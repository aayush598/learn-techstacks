# Streaming Inference for Recommendation Systems

## Overview

Streaming inference processes data in real-time as events arrive, updating recommendations continuously rather than in batch cycles. For recommendation systems, this enables immediate response to user behavior changes, trending content, and real-time context. This covers real-time feature updates, online model updates, streaming ranking, and event-driven inference.

---

## Real-Time Feature Updates

### Feature Store Architecture

```
Event Stream → Stream Processor → Feature Store → Inference Engine
                (Flink/Spark)     (Redis/DynamoDB)
```

### Feature Update Patterns

| Pattern | Latency | Use Case |
|---------|---------|----------|
| Synchronous update | 1-5 ms | Real-time session features |
| Micro-batch update | 100-500 ms | Near-real-time features |
| Window-based update | 1-60 s | Aggregated features (click rate) |
| Event-driven update | 1-10 ms | Triggered features (recent view) |

### Real-Time Feature Categories

**User Session Features**:
- Current session click sequence
- Time since last interaction
- Session-level engagement metrics
- Device and context information

**Item Trending Features**:
- Last-hour interaction count
- Velocity (interaction rate change)
- Geographic trending signals
- Social sharing velocity

**Cross-Feature Real-Time Signals**:
- User-item affinity score (last N interactions)
- User-category interest (sliding window)
- Time-decayed interaction weights

### Feature Store Requirements

- Sub-millisecond read latency for inference
- Write latency < 100 ms for feature updates
- High availability (99.99%+ uptime)
- Consistency model: eventual consistency acceptable for most features
- TTL management for time-windowed features

---

## Online Model Updates

### Incremental Learning Approaches

| Approach | Update Frequency | Complexity | Freshness |
|----------|-----------------|-----------|-----------|
| Full retrain | Hours-Days | Low | Low |
| Incremental fine-tune | Minutes-Hours | Medium | Medium |
| Online gradient descent | Per-event | High | Very high |
| Embarrassingly parallel online | Per-event | Medium | Very high |

### Online Gradient Descent

Update model weights with each incoming interaction:
```
w_t+1 = w_t - η × ∇L(interaction_t, w_t)
```

**Challenges**:
- Catastrophic forgetting: new data overrides old patterns
- Concept drift: user preferences change over time
- Stability-plasticity tradeoff: balance learning new patterns vs retaining old ones
- Noisy gradients: individual interactions may be outliers

### Mitigation Strategies

- **Learning rate decay**: Reduce update magnitude over time
- **Elastic weight consolidation**: Protect important weights from large updates
- **Experience replay**: Mix new interactions with sampled historical data
- **Ensemble updates**: Maintain multiple model versions and average predictions

---

## Streaming Ranking

### Event-Driven Recommendation Refresh

1. User performs action (click, purchase, search)
2. Event is published to stream (Kafka, Kinesis)
3. Stream processor updates user features
4. Trigger recommendation refresh
5. Updated recommendations pushed to client

### Streaming Ranking Architecture

```
User Event → Kafka → Flink Job → Feature Update → Model Inference → Recommendation Store
                              ↓
                        User Profile Update → Redis
```

### Real-Time Re-Ranking

- Maintain base recommendations (pre-computed)
- Apply real-time re-ranking based on latest context
- Consider recently seen items (avoid repetition)
- Boost trending items matching user interests
- Apply business rules (diversity, freshness, fairness)

---

## Incremental Recommendations

### Sliding Window Recommendations

- Maintain recommendations based on last N interactions
- Update incrementally as new interactions arrive
- Evict old interactions from the window
- Recompute affected recommendations only

### Differential Updates

- When a single feature changes, recompute only affected scores
- Cache intermediate computations for incremental updates
- Use dependency graphs to identify affected recommendations
- Minimize redundant computation across users

### Event-Time vs Processing-Time

| Aspect | Event-Time | Processing-Time |
|--------|-----------|----------------|
| Ordering | Based on when event occurred | Based on when event is processed |
| Latency | Higher (may wait for late events) | Lower (process immediately) |
| Accuracy | More accurate (correct ordering) | May process out-of-order events |
| Complexity | Requires watermarking | Simple implementation |

---

## Event-Driven Inference

### Architecture Components

- **Event bus**: Kafka, Kinesis, Pub/Sub for event ingestion
- **Stream processor**: Flink, Spark Streaming, Kafka Streams
- **Feature store**: Redis, DynamoDB for real-time feature access
- **Inference service**: Model serving endpoint for real-time scoring
- **Recommendation store**: Cache of current recommendations per user

### Event Types and Handlers

| Event Type | Handler | Action |
|-----------|---------|--------|
| User click | Feature updater + re-ranker | Update user profile, refresh recommendations |
| Item published | Candidate generator | Add item to candidate pools |
| Trending signal | Trending scorer | Update trending scores for items |
| Model update | Model loader | Reload model from registry |
| Feedback signal | Label generator | Generate training labels for online learning |

### Scaling Event-Driven Systems

- Partition events by user ID for ordered processing per user
- Scale stream processors horizontally (more partitions = more parallelism)
- Use backpressure handling for traffic spikes
- Implement circuit breakers for downstream service failures
- Monitor event processing lag and alert on delays

---

## Operational Considerations

### Monitoring

- **Event processing lag**: Time from event creation to processing
- **Feature freshness**: Age of features used for inference
- **Recommendation latency**: End-to-end time from event to updated recommendation
- **Update throughput**: Events processed per second
- **Model freshness**: Time since model weights were last updated

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Feature store down | Stale features used | Fallback to default features |
| Stream processor lag | Delayed recommendations | Scale processor, accept staleness |
| Model service down | No real-time scoring | Fallback to pre-computed results |
| Event loss | Missing feature updates | Event replay from log |

### Best Practices

1. Design for eventual consistency; avoid strong consistency requirements
2. Implement graceful degradation when components fail
3. Monitor end-to-end freshness, not just component health
4. Test with production-like event volumes and patterns
5. Maintain batch fallback for all streaming features
