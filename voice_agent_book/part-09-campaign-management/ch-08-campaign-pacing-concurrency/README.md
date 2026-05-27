# Chapter 08: Campaign Pacing & Concurrency

> **Part:** 09 - Campaign Management

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Concurrency Limit Fundamentals](sec-01-concurrency-limit-fundamentals.md) | Per-campaign, per-agent, global concurrency limits — resource-based and rule-based limits |
| 02 | [Dialing Ratio Strategies](sec-02-dialing-ratio-strategies.md) | Predictive dialing ratio — answer rate calculation, ratio adjustment, abandonment rate control |
| 03 | [Agent Utilization Optimization](sec-03-agent-utilization-optimization.md) | Agent availability tracking, utilization targets, idle time minimization, skill-based routing |
| 04 | [Campaign Throttling Mechanisms](sec-04-campaign-throttling-mechanisms.md) | Rate limiting, token bucket algorithm, leaky bucket, campaign-level throttles |
| 05 | [Real-Time Pacing Adjustment](sec-05-real-time-pacing-adjustment.md) | Dynamic pacing — answer rate feedback loop, abandonment rate monitoring, automatic ratio tuning |
| 06 | [Pacing Algorithm Design](sec-06-pacing-algorithm-design.md) | Algorithm comparison — predictive, adaptive, fixed ratio, machine learning-based pacing |
| 07 | [Burst Protection & Overload Control](sec-07-burst-protection-overload-control.md) | Burst detection, circuit breaker, overload shedding, graceful degradation |
| 08 | [Pacing Metrics & Monitoring](sec-08-pacing-metrics-monitoring.md) | Key pacing metrics — answered rate, abandonment rate, agent utilization, service level, dashboards |

---

## Key Takeaways

- Concurrency limits must be enforceable at campaign, agent, and global levels
- Predictive dialing ratio requires real-time answer rate tracking and adjustment
- Agent utilization optimization directly impacts campaign ROI and contact center efficiency
- Pacing algorithms must balance dialing volume with agent availability to prevent abandonment
- Burst protection prevents carrier throttling and compliance violations
