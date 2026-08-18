# Circuit Breaker Patterns for Recommendation Systems

## 1. Circuit Breaker State Machine

### 1.1 Three States

**Closed State (Normal)**:
- Requests flow normally to downstream service
- Failures are counted
- If failure count exceeds threshold, transitions to Open state
- All requests are allowed through

**Open State (Failing)**:
- All requests are immediately rejected/rejected with fallback
- No requests reach the downstream service
- After timeout period, transitions to Half-Open state
- Protects downstream service from overload
- Protects upstream service from waiting on failing calls

**Half-Open State (Testing)**:
- Limited number of requests are allowed through to test recovery
- If requests succeed, transitions back to Closed state
- If requests fail, transitions back to Open state
- Gradual recovery detection

### 1.2 State Transitions
```
Closed → Open: When consecutive failure count exceeds failure_threshold
Open → Half-Open: When timeout period expires
Half-Open → Closed: When success_count exceeds success_threshold
Half-Open → Open: When any request fails during test period
```

---

## 2. Configuration for Recommendation Services

### 2.1 Candidate Generation Circuit Breaker
```yaml
circuit_breaker:
  name: candidate_generation
  failure_threshold: 5
  failure_window: 60s
  timeout: 30s
  success_threshold: 3
  half_open_max_calls: 3
  fallback:
    strategy: cached_or_popular
    cache_ttl: 300s
    popular_items_count: 50
```

### 2.2 Ranking Service Circuit Breaker
```yaml
circuit_breaker:
  name: ranking_service
  failure_threshold: 3
  failure_window: 30s
  timeout: 60s
  success_threshold: 2
  half_open_max_calls: 2
  fallback:
    strategy: skip_ranking
    return_candidates_sorted_by_popularity: true
```

### 2.3 Feature Store Circuit Breaker
```yaml
circuit_breaker:
  name: feature_store
  failure_threshold: 3
  failure_window: 30s
  timeout: 10s
  success_threshold: 5
  half_open_max_calls: 5
  fallback:
    strategy: default_features
    use_cached_features: true
    cache_ttl: 600s
    default_feature_values: /config/default_features.yaml
```

---

## 3. Fallback Strategies

### 3.1 Graceful Degradation Levels
1. **Full Service**: All components healthy; full personalization
2. **Degraded Personalization**: Some components down; reduced personalization quality
3. **Popular Recommendations**: Model serving down; return popular/trending items
4. **Cached Recommendations**: All services down; return last cached recommendations
5. **Static Fallback**: Everything down; return editorially curated list

### 3.2 Fallback Response Design
```json
{
  "recommendations": [...],
  "metadata": {
    "personalized": false,
    "fallback_reason": "model_serving_unavailable",
    "fallback_level": "popular_items",
    "degradation_started_at": "2024-01-15T10:30:00Z"
  }
}
```

### 3.3 Fallback Quality Monitoring
- Track how often fallback is used per service
- Monitor recommendation quality during fallback mode
- Alert when fallback usage exceeds threshold
- Compare business metrics during normal vs fallback mode

---

## 4. Bulkhead Pattern

### 4.1 Resource Isolation
Isolate different recommendation components to prevent cascade failures:
- **Thread Pool Bulkhead**: Separate thread pools for different downstream services
- **Semaphore Bulkhead**: Limit concurrent calls to each service
- **Connection Pool Bulkhead**: Separate connection pools per service

### 4.2 Bulkhead Configuration
```yaml
bulkhead:
  candidate_generation:
    max_concurrent: 100
    max_wait: 5ms
  ranking_service:
    max_concurrent: 50
    max_wait: 10ms
  feature_store:
    max_concurrent: 200
    max_wait: 3ms
  model_serving:
    max_concurrent: 30
    max_wait: 20ms
```

### 4.3 Benefits
- Prevents one failing service from consuming all resources
- Ensures minimum capacity for each critical path
- Enables independent scaling of different components
- Prevents resource starvation during partial failures

---

## 5. Retry Strategies

### 5.1 Retry Configuration
```yaml
retry:
  max_attempts: 3
  initial_interval: 100ms
  max_interval: 2s
  multiplier: 2.0
  jitter: true
  retryable_status_codes: [408, 429, 500, 502, 503, 504]
  retryable_exceptions: [ConnectionError, TimeoutError]
```

### 5.2 Exponential Backoff with Jitter
- **Base Delay**: 100ms
- **Multiplier**: 2x (100ms, 200ms, 400ms, ...)
- **Jitter**: Random ±20% to prevent thundering herd
- **Max Delay**: 2 seconds
- **Total Budget**: Maximum retry time within latency budget

### 5.3 Recommendation-Specific Retry Logic
- **Feature Store**: Retry with shorter timeout; feature staleness is better than no recommendation
- **Model Serving**: Do NOT retry; model inference is expensive; use cached result instead
- **User Profile**: Retry once; profile data is cached and fast
- **Item Search**: Retry with different search strategy; try alternative retrieval channel

### 5.4 Idempotency Requirements
All retried operations must be idempotent:
- Feature retrieval: Idempotent (read-only)
- Model inference: Idempotent (deterministic for same input)
- Recommendation logging: Must use deduplication key
- User interaction recording: Must use event_id for deduplication

---

## 6. Time Limiter Pattern

### 6.1 Timeout Configuration
```yaml
timeouts:
  total_request: 200ms          # Total recommendation request timeout
  candidate_generation: 50ms    # Candidate generation timeout
  feature_retrieval: 15ms       # Feature store call timeout
  model_inference: 40ms         # Model serving timeout
  re_ranking: 10ms              # Re-ranking timeout
  network_buffer: 30ms          # Buffer for network variability
```

### 6.2 Timeout Propagation
- Set timeout at the start of request processing
- Propagate remaining timeout to downstream calls
- If downstream call exceeds timeout, use fallback
- Never wait longer than total request timeout

### 6.3 Timeout vs Retry Tradeoff
- Short timeouts: More retries, more overhead, faster failure detection
- Long timeouts: Fewer retries, higher latency during failures
- Recommendation: Set timeout at P99.9 of downstream service latency × 2

---

## 7. Cascading Failure Prevention

### 7.1 Common Cascade Scenarios in Recommendations
1. **Feature Store Slow → Ranking Backs Up → Candidate Gen Backs Up → API Gateway Overloads**
2. **Model Serving GPU Exhausted → Ranking Queues → Request Timeout → Client Retries → More Load**
3. **Kafka Lag → Feature Staleness → Poor Recommendations → User Complaints → Traffic Spike**

### 7.2 Prevention Strategies
- **Circuit Breakers**: Stop calling failing services
- **Bulkheads**: Isolate resource pools per service
- **Load Shedding**: Drop low-priority requests when under pressure
- **Rate Limiting**: Protect each service with its own rate limits
- **Timeout Propagation**: Don't wait for slow services
- **Graceful Degradation**: Return degraded but functional responses

### 7.3 Load Shedding Strategy
Priority levels for recommendation requests:
1. **P0 - Critical**: Real-time recommendations on main page
2. **P1 - High**: Similar item recommendations
3. **P2 - Medium**: "For you" feed recommendations
4. **P3 - Low**: Email recommendations (can be delayed)
5. **P4 - Background**: Batch pre-computation, model retraining

When under extreme load, shed P4 → P3 → P2 before affecting P0/P1.
