# Serving Patterns for Recommendation Systems

## Overview

Recommendation serving patterns define how models are deployed, how requests are processed, and how recommendations are delivered to users. The choice of pattern impacts latency, freshness, cost, and complexity. Most production systems use hybrid approaches combining multiple patterns.

---

## Real-Time Synchronous Serving

### Architecture

```
Client Request → Load Balancer → Inference Server → Model → Response
```

### Characteristics

| Property | Value |
|----------|-------|
| Latency | 10-100 ms (SLA-dependent) |
| Freshness | Real-time (latest model and features) |
| Cost | High (GPU per request) |
| Complexity | Moderate |
| Scalability | Horizontal scaling |

### When to Use

- First page of recommendations (highest visibility)
- Personalized ranking after candidate generation
- User-facing features requiring immediate response
- A/B testing new models with real-time traffic

### Implementation Considerations

- Connection pooling for inference servers
- Request batching within SLA window
- Feature caching for repeated feature computation
- Fallback mechanisms for inference failures
- Timeout handling with graceful degradation

---

## Batch Pre-Computation

### Architecture

```
Scheduled Job → Feature Pipeline → Model Inference → Result Cache → Serving Layer
```

### Characteristics

| Property | Value |
|----------|-------|
| Latency | < 5 ms (cache lookup) |
| Freshness | Batch interval (hours to days) |
| Cost | Low (amortized batch GPU cost) |
| Complexity | Low-moderate |
| Scalability | High (cache-based) |

### When to Use

- Homepage recommendations (users visit infrequently)
- Email/push notification recommendations
- "Because you watched X" style recommendations
- Catalog-wide recommendations (for-you page)

### Batch Size and Frequency

| Recommendation Type | Batch Frequency | Items Scored |
|--------------------|----------------|--------------|
| Daily recommendations | Once daily | All active users |
| Weekly digest | Once weekly | All subscribers |
| Catalog reranking | Every 4-6 hours | Full catalog per user |
| Social recommendations | Every hour | User's social graph |

---

## Hybrid Serving (Pre-Compute + Real-Time Rank)

### Architecture

```
Offline: Candidate Generation → Pre-scored Candidates → Candidate Store
Online:  User Request → Real-Time Features → Re-ranking Model → Final Recommendations
```

### Two-Stage Pipeline

**Stage 1: Candidate Generation (Offline/Batch)**
- Generate 100-1000 candidate items per user
- Uses batch computation for efficiency
- Less sophisticated model, broader coverage
- Updated periodically (hours to days)

**Stage 2: Re-ranking (Real-Time)**
- Rank top-K candidates based on real-time context
- Uses latest features (session context, time of day, trending)
- More sophisticated model, higher accuracy
- Computed on-demand per request

### Benefits

- Balance between freshness and computational cost
- Candidate generation scales (batch), re-ranking stays fast (real-time)
- Different models optimized for each stage
- Easy to update re-ranking model without regenerating candidates

### Implementation Patterns

| Pattern | Candidate Source | Re-ranker | Latency |
|---------|-----------------|-----------|---------|
| Batch + Real-time rank | Pre-computed candidates | Real-time model | 20-50ms |
| Approximate NN + Rank | ANN index lookup | Light ranking model | 10-30ms |
| Rule-based + ML rank | Heuristic candidates | ML re-ranker | 5-20ms |

---

## Streaming Recommendations

### Architecture

```
Event Stream (Kafka) → Feature Update → Model Update → Recommendation Update
```

### Real-Time Feature Updates

- Process user interaction events in real-time
- Update user profiles and feature stores continuously
- Trigger recommendation refresh based on events
- Maintain sliding window features (last N interactions)

### Streaming Ranking

- Use online learning models that update incrementally
- Process feature updates as they arrive
- Maintain running user preference vectors
- Event-driven recommendation refresh

### When to Use

- Live shopping / real-time commerce
- News feeds with breaking content
- Live event recommendations
- Gaming recommendations during active sessions

---

## Edge Serving

### Architecture

```
Model → Edge Device (On-Device Inference)
```

### Characteristics

| Property | Value |
|----------|-------|
| Latency | < 5 ms (on-device) |
| Freshness | Last model sync (hours to days) |
| Cost | Zero marginal cost per request |
| Complexity | High (deployment, updates) |
| Scalability | Infinite (each device is a server) |

### When to Use

- Mobile app recommendations with offline capability
- Smart TV content recommendations
- IoT device recommendations
- Privacy-sensitive recommendations (data stays on device)

### Edge Model Requirements

- Small model size (< 50 MB)
- Fast inference (< 10 ms on target hardware)
- Quantized and optimized for edge hardware
- Offline-capable with periodic sync

---

## Pattern Selection Guide

| Factor | Real-Time | Batch | Hybrid | Streaming | Edge |
|--------|-----------|-------|--------|-----------|------|
| Latency requirement | < 100ms | Any | < 50ms | < 10ms | < 5ms |
| Freshness need | High | Low | Medium-High | Very High | Low-Medium |
| Cost budget | High | Low | Medium | Medium | Low |
| Infrastructure | GPU servers | Batch jobs | Both | Stream processing | Devices |
| Complexity | Low | Low | Medium | High | Very High |

---

## Combining Patterns in Production

### Multi-Channel Architecture

- **Web real-time**: Hybrid pattern (batch candidates + real-time rank)
- **Mobile push**: Batch pre-computation (daily recommendations)
- **Email**: Batch with personalization rules
- **Search**: Real-time synchronous (query-dependent)
- **Trending**: Streaming (real-time event-driven)

### Fallback Strategy

1. Try real-time inference (highest quality)
2. Fallback to pre-computed cache (if inference fails)
3. Fallback to popularity-based recommendations (if cache is empty)
4. Never return empty recommendations (always have a fallback)

### Monitoring Across Patterns

- Track latency, throughput, and error rate per pattern
- Monitor cache hit rates for hybrid and batch patterns
- A/B test across patterns when transitioning
- Cost tracking per pattern per request
