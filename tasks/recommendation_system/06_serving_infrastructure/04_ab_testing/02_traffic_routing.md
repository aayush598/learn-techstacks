# Traffic Routing for A/B Testing

## Overview

Traffic routing determines which users see which model variant during A/B testing. Proper routing ensures statistical validity, prevents interference between experiments, and enables consistent user experiences. This covers consistent hashing, experiment levels, allocation strategies, and interference prevention.

---

## Consistent Hashing for Assignment

### Why Consistent Hashing

- Deterministic: same user always gets same assignment (given same experiment configuration)
- Balanced: uniform distribution across variants
- Stable: adding/removing variants doesn't completely reshuffle assignments
- Stateless: assignment computed from user ID and experiment config, no central state

### Implementation

```
hash_value = hash(user_id + experiment_id) % 10000
variant_index = hash_value / (10000 / num_variants)
```

### Hash Function Requirements

| Property | Requirement | Rationale |
|----------|-------------|-----------|
| Uniformity | Even distribution across variants | Balanced experiment groups |
| Determinism | Same input → same output | Consistent assignment |
| Stability | Minimal reshuffle on config change | Avoid crossover contamination |
| Speed | Fast computation (ns-level) | No serving latency impact |

### Seed-Based Hashing

- Use experiment-specific seed in hash function
- Changing seed re-randomizes assignments
- Enables reproducibility: same seed + same users = same assignment
- Store seed with experiment configuration

---

## Experiment Levels

### User-Level Experiments

- **Assignment unit**: Individual user
- **Consistency**: User always sees same variant within experiment
- **Use case**: Most recommendation experiments (model variants, UI changes)
- **Implementation**: Hash on user_id

### Session-Level Experiments

- **Assignment unit**: Individual session (new session = new assignment)
- **Consistency**: Same variant within session, may differ across sessions
- **Use case**: Session-dependent features, onboarding experiments
- **Implementation**: Hash on user_id + session_id

### Request-Level Experiments

- **Assignment unit**: Individual request
- **Consistency**: May see different variants on each request
- **Use case**: Latency experiments, caching experiments, exploration
- **Implementation**: Hash on user_id + request_id + timestamp

### Comparison

| Level | Consistency | Statistical Power | Use Case |
|-------|-------------|-------------------|----------|
| User | Highest | Highest | Model quality experiments |
| Session | Medium | Medium | Session-dependent features |
| Request | Lowest | Lowest | Infrastructure experiments |

---

## Traffic Allocation Strategies

### Fixed Allocation

Divide traffic into fixed percentages:

```
Variant A: 50% (control)
Variant B: 25% (treatment 1)
Variant C: 25% (treatment 2)
```

### Dynamic Allocation

Adjust allocation based on performance:

- Start with equal allocation (33/33/33 for 3 variants)
- After statistical significance, shift traffic to better variant
- Gradually phase out underperforming variants
- Maintain minimum traffic for each variant for ongoing validation

### Ramp-Up Strategy

1. **Canary**: 1% traffic to new variant (smoke test)
2. **Small test**: 5-10% traffic (statistical validation)
3. **Medium test**: 25-50% traffic (broader validation)
4. **Full rollout**: 100% traffic (production deployment)

### Allocation Requirements

| Experiment Type | Minimum Traffic | Duration | Rationale |
|----------------|----------------|----------|-----------|
| Model quality | 10% per variant | 7-14 days | Statistical significance |
| UI changes | 20% per variant | 3-7 days | Quick iteration |
| Infrastructure | 5% per variant | 3-5 days | Latency validation |
| Exploration | 5-10% per variant | Ongoing | Continuous learning |

---

## Interference Prevention

### Types of Interference

| Type | Description | Example |
|------|-------------|---------|
| User crossover | User sees multiple variants | User logged in on multiple devices |
| Network effects | Variant A affects users in variant B | Social recommendations influence friends |
| Position effects | Variant order affects comparison | First item always gets more clicks |
| Time effects | Different variants at different times | Morning vs evening behavior |

### Prevention Strategies

**User-level isolation**:
- Consistent hashing ensures same user sees same variant
- Account for multi-device: hash on user_id, not device_id
- Handle logged-out users: use device fingerprint or session ID

**Network effect isolation**:
- Cluster-based assignment for social features (assign entire friend group)
- Geographic assignment for location-dependent experiments
- Household-level assignment for shared device experiments

**Statistical isolation**:
- Use appropriate statistical tests that account for interference
- Consider switchback experiments for network effects
- Washout period between experiments on same user

### Crossover Detection

- Monitor for users appearing in multiple variants (should be 0%)
- Check assignment consistency across sessions
- Verify hash function produces expected distribution
- Audit experiment logs for assignment anomalies

---

## Implementation Architecture

### Assignment Service

```
Request → Assignment Service → {variant_id, config} → Model Serving → Response
              ↓
         Experiment DB (configs, assignments)
```

### Assignment Service Requirements

- **Latency**: < 1ms per assignment (typically hash computation)
- **Availability**: 99.99% (experiment failures should not affect production)
- **Consistency**: Deterministic across all serving instances
- **Scalability**: Handle peak QPS with room for growth

### Client-Side vs Server-Side Assignment

| Aspect | Client-Side | Server-Side |
|--------|------------|------------|
| Latency impact | None (local) | +1ms per request |
| Consistency | Device-dependent | User-level consistent |
| Implementation | Mobile SDK / web JS | API gateway / assignment service |
| Multi-device | May differ per device | Consistent across devices |

### Assignment Storage

- Store assignments in experiment database for analysis
- Keep assignment log for debugging and audit
- Use write-through caching for fast reads
- Retain assignment data for experiment duration + 30 days

---

## Monitoring Traffic Routing

### Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Assignment distribution | Actual vs expected % per variant | Within 1% of target |
| Crossover rate | Users in multiple variants | 0% |
| Assignment latency | Time to compute assignment | < 1ms |
| Assignment consistency | Same user gets same variant | 100% |

### Common Issues

- **Uneven distribution**: Hash function not uniform enough → change hash
- **Crossover**: Multi-device users not handled → use user_id not device_id
- **Drift**: Allocation percentages shift over time → monitor and rebalance
- **Stale assignments**: Old experiment config cached → implement proper TTL
