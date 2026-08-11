# 00 — Alert Rule Engine

## Purpose
Define when the system must reach out to a human — configurable rules evaluated
continuously, self-hosted, deterministic.

## Alert categories
1. **Risk**: breaker tripped, daily limit hit, exposure cap, position mismatch.
2. **Data**: feed down, gaps, validation rejections, source health (CH_07, CH_06).
3. **Execution**: OMS errors, illegal state transitions, rejections spike,
   auth failure, reconciliation differences (CH_24, CH_25).
4. **System**: stage over budget, crash/restart, disk space, process health
   (CH_27, CH_31, CH_32).
5. **Model**: drift alarm, retraining completed/failed, deployment (CH_16/03).

## Rule format
```
alert_rules.yaml:
  - id: daily_loss_hit
    severity: CRITICAL
    when: risk.daily_loss_pct >= policy.max_daily_loss
    channels: [email, telegram, push]
  - id: feed_down
    severity: CRITICAL
    when: feed.lag_sec > 10 and feed.down_sec > 30
    channels: [email, telegram]
  - id: reject_rate_high
    severity: HIGH
    when: oms.reject_rate > 0.05 over 10 min
    channels: [email]
```

## Evaluation
- Rules evaluated on a short tick (e.g., every 5–10 s) against the metrics
  state (CH_32) — pure function `(rule, state) -> fired?`.
- **Deduplication**: same rule fires at most once per N minutes (no alert spam).
- **Recovery**: optional auto-notify on condition clearing (state transition).

## Pseudo-code
```
def evaluate_alerts():
    for rule in rules:
        if rule.when(metrics_state) and not in_cooldown(rule):
            notify(rule); mark_cooldown(rule)
        elif cleared(rule): notify_recovered(rule)
```

## Rules
- Alerting must not depend on the trading path (separate process/channel).
- Critical alerts route through multiple channels (CH_30/01).
- Every alert is logged with the state snapshot that triggered it (CH_33).
