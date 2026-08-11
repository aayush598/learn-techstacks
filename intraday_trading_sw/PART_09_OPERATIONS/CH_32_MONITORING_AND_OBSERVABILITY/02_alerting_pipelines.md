# 02 — Alerting Pipelines

## Purpose
Turn monitored signals into the right alert at the right severity, reliably
and without noise.

## Pipeline
```
Metrics (CH_32/00) -> Rules (CH_30/00) -> Dedup/cooldown -> Notify (CH_30/01)
                                    -> Escalation (CH_30/02) -> Dead-letter log
```

## Alert health itself is monitored
- Alert queue backlog, notifier failures, dead-letter queue size — all metrics.
- A failed alert pipeline is a CRITICAL alert on its own (the "watcher watched").

## Pseudo-code: alert pipeline loop
```
while True:
    state = metrics_snapshot()
    for rule in rules: maybe_fire(rule, state)   # cooldown-aware (CH_30/00)
    check_notifier_health()
    sleep(interval)
```

## Anti-noise rules
- Cooldowns per rule (CH_30/00); aggregated digests for LOW/MEDIUM.
- Severity is set by impact on capital, not by technical drama.
- Alerts carry context: state snapshot, links to logs/dashboard (CH_33).

## Incident flow (for CRITICAL)
1. Alert fires → paging (CH_30/02).
2. The system already auto-protected (flatten/halt where applicable, CH_23).
3. Post-incident: a written review is generated (what, why, effect, fix) —
   see CH_33 traceability.

## Rules
- Safety actions never wait for alerting (CH_30/02) — alerting informs humans;
  protection is automatic.
- Every fired alert is recorded with the triggering snapshot (reproducibility).
- Weekly alert review: tune thresholds to keep signal, remove noise.
