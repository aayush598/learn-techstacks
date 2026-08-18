# User Feedback Loops for Recommendations

## Overview

User feedback loops are the mechanisms by which recommendation systems learn from user interactions to improve future recommendations. A well-designed feedback loop creates a virtuous cycle: better recommendations generate more engagement, which generates more data, which produces even better recommendations. This document covers feedback types, collection mechanisms, quality assessment, integration with model retraining, and the design of closed-loop ML systems.

---

## Feedback Types

### Implicit Feedback

Implicit feedback is inferred from user behavior without requiring explicit user action.

| Signal | Source | Reliability | Volume | Interpretation |
|--------|--------|-------------|--------|----------------|
| Clicks | Click logs | Moderate | Very high | Interest (but also clickbait) |
| Views (dwell time) | Event logs | High | Very high | Engagement depth |
| Purchases | Transaction logs | Very high | High | Strong preference signal |
| Add-to-cart | Event logs | High | Moderate | Purchase intent |
| Scroll depth | Event logs | Moderate | High | Content engagement |
| Skip/dismiss | Event logs | High | High | Negative signal |
| Search queries | Search logs | High | High | Active intent |
| Share | Event logs | Very high | Low | Strong endorsement |
| Replay/rewatch | Event logs | High | Moderate | Strong positive signal |

### Explicit Feedback

Explicit feedback requires deliberate user action.

| Signal | Source | Reliability | Volume | Interpretation |
|--------|--------|-------------|--------|----------------|
| Ratings (1-5 stars) | Rating form | High | Low-Moderate | Granular preference |
| Likes/dislikes | Button clicks | High | Moderate | Binary preference |
| Thumbs up/down | Button clicks | High | Moderate | Binary preference |
| Written reviews | Text input | Very high | Very low | Rich sentiment signal |
| "Not interested" | Dismissal button | Very high | Low | Strong negative signal |
| "Show me more" | Preference setting | Very high | Very low | Direct preference |
| Survey responses | Periodic survey | High | Very low | Meta-preference data |

### Feedback Quality Assessment

| Quality Dimension | Description | Measurement |
|------------------|-------------|-------------|
| Intentionality | Was the feedback deliberate? | Explicit > Implicit |
| Positivity | Is it a reliable positive signal? | Purchase > Click |
| Positivity bias | Are negative signals underreported? | Compare like/dislike ratios |
| Temporal relevance | How recent is the signal? | Decay-weighted engagement |
| Noise level | How much random variation? | Signal-to-noise ratio |
| Coverage | How many users provide it? | % of active users |

---

## Feedback Collection Architecture

### Event-Driven Collection

```
User Interaction
      ↓
Client-Side SDK (JavaScript, Mobile, Backend)
      ↓
Event Validation + Enrichment
      ↓
Event Stream (Kafka/Kinesis/Pub-Sub)
      ↓
┌─────────────┬──────────────────┬─────────────────┐
│ Real-time   │ Stream           │ Batch            │
│ Processing  │ Processing       │ Processing       │
│ (Flink)     │ (Spark Streaming)│ (Spark/Hive)     │
│             │                  │                   │
│ Feature     │ Session-level    │ User-level        │
│ updates     │ aggregation      │ aggregation       │
└─────────────┴──────────────────┴─────────────────┘
```

### Event Schema Design

```json
{
  "event_id": "uuid-v4",
  "user_id": "u_12345",
  "session_id": "s_67890",
  "timestamp": "2024-01-15T10:30:00.123Z",
  "event_type": "click",
  "item_id": "i_54321",
  "item_position": 3,
  "impression_id": "imp_11111",
  "context": {
    "device_type": "mobile_ios",
    "app_version": "3.2.1",
    "screen": "homepage",
    "referrer": "push_notification",
    "location_country": "US",
    "connection_type": "wifi"
  },
  "properties": {
    "dwell_time_ms": 4500,
    "scroll_depth": 0.85,
    "added_to_cart": false,
    "purchased": false
  },
  "experiment_info": {
    "experiment_id": "ranking_v3",
    "variant": "treatment"
  }
}
```

### Collection Best Practices

| Practice | Description | Why |
|----------|-------------|-----|
| Client-side dedup | Deduplicate events before sending | Prevent duplicate signals |
| Batch sending | Buffer events, send in batches | Reduce network overhead |
| Offline support | Queue events when offline, send when online | No data loss |
| Privacy compliance | Anonymize/aggregate per GDPR | Legal requirement |
| Sampling | Sample high-frequency events | Control data volume |
| Validation | Validate event schema at ingestion | Data quality |

---

## Implicit vs Explicit Signals: Handling Asymmetry

### The Positivity Bias Problem

Users are much more likely to click on items they like than to provide negative feedback. This creates a dataset biased toward positive interactions.

```
Typical signal distribution:
  Impressions (no click): 1,000,000  → Weak negative signal
  Clicks:                  50,000    → Moderate positive signal
  Purchases:                5,000    → Strong positive signal
  Explicit dislikes:           200   → Strong negative signal
  Explicit likes:            2,000   → Strong positive signal
```

### Addressing Asymmetry

| Strategy | Description | Implementation |
|----------|-------------|---------------|
| Negative sampling | Treat non-clicks as negative | Weighted negative sampling |
| Position debiasing | Account for position bias in clicks | Inverse propensity scoring |
| Exposure modeling | Model what users see vs what they skip | Counterfactual reasoning |
| Censored feedback | Users who don't click may not have seen the item | Treat missing as censored |
| Calibrated learning | Ensure predicted distribution matches observed | Calibration layer |

### Position Bias Correction

Users are more likely to click on items at the top of a list regardless of relevance:

```
Corrected CTR = Observed CTR / Position propensity

Position propensities (typical):
  Position 1: 3.0×  (highly inflated)
  Position 2: 1.8×
  Position 3: 1.2×
  Position 4: 1.0×  (baseline)
  Position 5: 0.8×
  ...
  Position 10: 0.4×
```

---

## Feedback in Model Retraining

### Online Learning

Update model parameters with each new feedback event:

```
For each event (user, item, clicked):
    features = extract_features(user, item, context)
    prediction = model.predict(features)
    loss = loss_fn(prediction, clicked)
    model.update(loss)  # Online gradient descent
```

**Pros:** Adapts immediately, no retraining lag
**Cons:** Noisy updates, can forget old patterns, difficult to debug

### Micro-batch Learning

Accumulate feedback for short periods, then update:

```
Every 1 hour:
    new_events = collect_events(since=last_update)
    if len(new_events) > threshold:
        update_model(new_events)
        last_update = now()
```

**Pros:** More stable than online, still fresh
**Cons:** Requires incremental training support

### Periodic Full Retraining

Retrain from scratch on accumulated data:

```
Daily/Weekly:
    full_dataset = all_historical_data + recent_feedback
    model = train(full_dataset)
    evaluate(model, test_set)
    if passes_quality_gate:
        deploy(model)
```

**Pros:** Most stable, easiest to debug, incorporates all data
**Cons:** Long latency, expensive, stale between retrains

### Hybrid Approach (Recommended)

```
Frequent micro-batch updates (hourly) for:
  - Feature statistics (trending items, popularity)
  - Embedding updates for active items
  - Bandit exploration parameters

Daily full retrain for:
  - Model weights (deep learning models)
  - Embedding tables
  - Feature importance weights

Weekly full retrain for:
  - Complete model architecture validation
  - Hyperparameter optimization
  - Feature engineering review
```

---

## Closed-Loop ML Systems

### Architecture

```
┌────────────────────────────────────────────────────┐
│                  Closed-Loop System                  │
│                                                     │
│  ┌─────────┐   ┌──────────┐   ┌───────────────┐   │
│  │ Model   │ → │ Serving  │ → │ User          │   │
│  │ Training│   │ Layer    │   │ Experience    │   │
│  └────▲────┘   └──────────┘   └───────┬───────┘   │
│       │                               │            │
│       │        ┌──────────────┐       │            │
│       └────────│ Feedback     │◄──────┘            │
│                │ Collection   │                    │
│                └──────────────┘                    │
│                                                     │
│  Monitoring → Alerts → Investigation → Fixes       │
└────────────────────────────────────────────────────┘
```

### Feedback Loop Health Metrics

| Metric | Description | Healthy Range | Alert Threshold |
|--------|-------------|---------------|-----------------|
| Feedback volume | Events per hour | Stable ± 20% | > 50% drop |
| Positive/negative ratio | Like/dislike ratio | 3:1 to 10:1 | > 20:1 (spam?) |
| Click-through rate | Engagement rate | Stable or increasing | > 10% drop |
| Return rate | Users returning within 7 days | > 30% | < 20% |
| Diversity over time | Intra-list diversity trend | Stable or increasing | > 20% drop |
| Freshness of recommendations | Age of recommended items | Appropriate for domain | Staleness increasing |
| Feedback coverage | % of users providing feedback | > 10% | < 5% |

### Feedback Loop Anti-Patterns

| Anti-Pattern | Description | Consequence | Prevention |
|-------------|-------------|-------------|------------|
| Filter bubble | System reinforces existing preferences | Reduced diversity, user fatigue | Exploration budget, diversity constraints |
| Popularity amplification | Popular items get more exposure → more popular | Long-tail items ignored | Exposure fairness constraints |
| Feedback echo | Model trains on its own biased output | Model drift, bias amplification | Hold-out validation, counterfactual evaluation |
| Silent degradation | Metrics slowly degrade without alerts | Gradual quality loss | Continuous monitoring, guardrail metrics |
| Target gaming | Users learn to manipulate recommendations | Noisy feedback | Anti-gaming detection, signal validation |

---

## Continuous Improvement Process

### Data Flywheel

```
Better Data → Better Models → Better Recommendations
    ↑                                      ↓
    └──── More User Engagement ←───────────┘
```

### Weekly Review Process

1. **Feedback quality review**: Check feedback volume, ratio, and quality metrics
2. **Model performance review**: Compare current metrics to historical baseline
3. **User complaint analysis**: Categorize and investigate user complaints
4. **A/B test results**: Incorporate winning experiment changes
5. **Feature importance analysis**: Identify which features drive the most lift
6. **Data gap identification**: Find areas with insufficient feedback data
7. **Retraining schedule review**: Ensure retraining is happening on schedule

### Monthly Strategic Review

1. **User satisfaction trends**: Survey results, NPS changes
2. **Long-term retention impact**: Are recommendations improving retention?
3. **Catalog health**: Are all items getting fair exposure?
4. **Competitive benchmarking**: How do our metrics compare to industry?
5. **Technology assessment**: New algorithms, frameworks, or approaches to evaluate

---

## Privacy and Ethical Considerations

### Privacy Requirements

| Requirement | Implementation | Regulation |
|------------|----------------|------------|
| Consent | Opt-in for tracking | GDPR, CCPA |
| Anonymization | Remove PII from feedback | GDPR |
| Right to deletion | Delete user's feedback on request | GDPR Art. 17 |
| Data minimization | Only collect necessary signals | GDPR Art. 5 |
| Purpose limitation | Use feedback only for recommendations | GDPR Art. 5 |

### Ethical Considerations

| Concern | Description | Mitigation |
|---------|-------------|------------|
| Filter bubbles | Reinforcing narrow interests | Diversity constraints, exploration |
| Echo chambers | Amplifying existing beliefs | Serendipity injection |
| Manipulation | Using feedback to manipulate behavior | Transparency, user control |
| Bias amplification | Feedback reinforces existing biases | Fairness constraints, monitoring |
| Surveillance | Excessive tracking of user behavior | Data minimization, anonymization |

### User Control

- Allow users to view their recommendation profile
- Provide "not interested" and "show more like this" controls
- Enable recommendation preference settings
- Allow data export and deletion
- Provide transparency about why items are recommended
