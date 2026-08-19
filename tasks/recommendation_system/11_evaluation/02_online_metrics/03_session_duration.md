# Session Metrics

## Overview

Session metrics evaluate how recommendations perform within and across user sessions. A session represents a continuous period of user activity on a platform—from the moment they arrive until they leave. Session-level analysis captures recommendation quality from the user's perspective: how deeply they engage, how many items they explore, and whether the session leads to a meaningful outcome.

## Session Duration

### Definition

```
Session Duration = Timestamp(last_action) - Timestamp(first_action)
```

### Types of Session Duration

| Type | Definition | Use Case |
|------|-----------|----------|
| **Wall-clock duration** | Real elapsed time | Overall engagement measurement |
| **Active duration** | Time excluding idle periods | True engagement measurement |
| **Interaction duration** | Time between first and last interaction | Recommendation-driven engagement |

### Idle Timeout Threshold
Sessions must be defined with an idle timeout—the maximum gap between consecutive actions before a new session begins:

| Platform | Typical Timeout | Rationale |
|----------|----------------|-----------|
| E-commerce | 30 minutes | Shopping sessions are deliberate |
| Social media | 15 minutes | Fast-paced content consumption |
| News/media | 20 minutes | Reading breaks are common |
| SaaS tools | 60 minutes | Work sessions are long |
| Mobile apps | 5 minutes | Quick interactions |

### Session Duration and Recommendations
- **Longer sessions** may indicate the recommendation system is effectively engaging users
- **Shorter sessions** may indicate poor recommendations or efficient task completion
- **Caution**: Duration alone is ambiguous—long sessions could mean confusion, not engagement

### Normalized Session Duration

```
Norm_Duration = Session_Duration / Expected_Duration(user_type)
```

Where expected duration is computed from historical sessions of similar user types.

## Items Per Session

### Definition

```
Items_Per_Session = |{unique items interacted with in session}| / Session_Count
```

### Metrics

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| Average items per session | Σ items(s) / Σ sessions | Overall engagement depth |
| Median items per session | Median of items(s) distribution | Robust to outliers |
| Items per session by source | Items(s) / sessions(s) for each traffic source | Source quality comparison |

### Items Per Session and Recommendation Quality

| Pattern | Interpretation | Action |
|---------|---------------|--------|
| Increasing over time | Recommendations are improving engagement | Maintain strategy |
| Decreasing over time | Users may be fatigued or recommendations declining | Investigate |
| High variance | Inconsistent recommendation quality | Improve consistency |
| Low for new users | Cold-start problem | Improve onboarding recommendations |

## Session Depth

### Definition

Session depth measures how far into the recommendation list or catalog a user explores within a session.

### Depth Metrics

```
Average Depth = mean(position of last interacted item)
Normalized Depth = Average Depth / Total Items Shown
```

### Depth Distribution

| Depth Range | User Behavior | Recommendation Implication |
|-------------|--------------|---------------------------|
| Position 1–3 | Shallow exploration | Top recommendations must be excellent |
| Position 4–10 | Moderate exploration | Good list quality needed |
| Position 11–20 | Deep exploration | User is actively searching |
| Position 20+ | Very deep exploration | User is determined; tail items matter |

### Depth by Recommendation Section

On a homepage with multiple recommendation sections:
- **Hero section**: How many users engage with the primary recommendation?
- **Row-level sections**: Do users scroll through secondary recommendations?
- **Infinite scroll**: How far do users scroll before exiting?

## Session Frequency

### Definition

```
Session_Frequency = Total_Sessions(user) / Time_Window(user)
```

### Frequency Segments

| Segment | Definition | Typical Behavior |
|---------|-----------|-----------------|
| Daily active | ≥ 1 session/day | Power users; habit-driven |
| Weekly active | 1–6 sessions/week | Regular users |
| Monthly active | 1–4 sessions/month | Casual users |
| Lapsed | No sessions in 30+ days | At-risk users |

### Frequency and Recommendation Impact
- **Increasing frequency**: Recommendations are creating habit loops
- **Decreasing frequency**: Users are losing interest or finding alternatives
- **Frequency by acquisition channel**: Organic users may be more frequent than paid users

## Session-Based Recommendation Quality

### Real-Time Quality Signals

| Signal | What It Indicates | How to Measure |
|--------|------------------|---------------|
| Click-through within session | Initial recommendation relevance | CTR per session |
| Items explored per session | Engagement depth | Items per session |
| Recommendation diversity consumed | List diversity effectiveness | Unique categories per session |
| Time to first click | Recommendation attractiveness | Time from session start to first click |
| Scroll depth past recommendations | Recommendation visibility | Scroll position analysis |

### Session-Level NDCG

Compute NDCG for each session's interaction sequence:

```
Session_NDCG(s) = NDCG(interactions(s), recommendations(s))
Average_Session_NDCG = mean(Session_NDCG(s) for all sessions s)
```

### Session Precision

```
Session_Precision(s) = |{relevant items clicked}| / |{recommended items shown}|
```

## Session Conversion

### Definition

```
Session_Conversion_Rate = |{sessions with at least one conversion}| / |{all sessions}|
```

### Session Conversion vs User Conversion

| Metric | Definition | When to Use |
|--------|-----------|------------|
| User conversion rate | Users who converted / all users | Overall business metric |
| Session conversion rate | Sessions with conversion / all sessions | Per-session recommendation quality |
| Multi-session conversion | Conversion within N sessions of exposure | Understanding delayed conversion |

### Session Conversion Attribution

Within a session, determine which recommendation section or item led to conversion:
- **Last-interacted**: The conversion is attributed to the last recommendation item the user interacted with
- **First-interacted**: Attribution to the first interaction
- **View-through**: Attribution to any recommendation that was shown (even if not clicked)

## Session Abandonment Rate

### Definition

```
Abandonment_Rate = |{sessions with zero meaningful actions}| / |{all sessions}|
```

Where "meaningful actions" is defined per product (e.g., at least one item view, one click, or one add-to-cart).

### Abandonment Signals

| Signal | Threshold | Severity |
|--------|----------|----------|
| Bounce (single page, no interaction) | Session depth = 1 | High |
| Immediate exit (< 5 seconds) | Duration < 5s | Very high |
| No scroll past first screen | Scroll depth = 0% | Medium |
| No click on any recommendation | CTR = 0 | Medium |

### Diagnosing Abandonment

1. **New users with abandonment**: Likely a cold-start or onboarding problem
2. **Returning users with increased abandonment**: Recommendation quality may have degraded
3. **Abandonment by device**: Mobile abandonment may indicate UX issues, not recommendation issues
4. **Abandonment by source**: High-bounce traffic sources may have low intent

### Abandonment Funnel

```
Session Start → Recommendation View → First Interaction → Deep Engagement → Conversion
    100%              85%                   60%                30%              5%
```

Each stage drop-off should be investigated separately.

## Comprehensive Session Dashboard

| Category | Metric | Target |
|----------|--------|--------|
| Duration | Average session duration | Increasing trend |
| Duration | Active time ratio | > 60% |
| Depth | Average items per session | > 5 |
| Depth | Scroll depth past recommendations | > 70% |
| Frequency | Sessions per user per week | > 3 |
| Frequency | Returning user rate | > 40% |
| Quality | Session-level NDCG | > 0.4 |
| Quality | First-click latency | < 10 seconds |
| Conversion | Session conversion rate | > 3% |
| Conversion | Multi-session conversion rate | > 10% |
| Abandonment | Bounce rate | < 40% |
| Abandonment | Immediate exit rate | < 15% |

## Implementation Considerations

### Session Definition Challenges
- **Cross-device sessions**: A user on mobile then desktop—same session or two?
- **Background/foreground transitions**: App switching mid-session
- **Bot traffic**: Automated crawlers inflate session counts
- **Authenticated vs anonymous**: Sessions without login are harder to track

### Statistical Considerations
- Session metrics are highly non-normal (long-tailed distributions)
- Use bootstrapping for confidence intervals
- Account for within-user correlation (a user's sessions are not independent)
- Report median alongside mean for duration and items-per-session metrics
