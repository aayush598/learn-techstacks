# 02 — Escalation Policy

## Purpose
Define what happens when an alert is not acknowledged within a time window —
so problems never go unnoticed during market hours.

## Severity levels
| Level | Meaning | Ack SLA | Escalate after |
|---|---|---|---|
| CRITICAL | Capital/system risk (breaker, OMS desync, feed down) | 5 min | 5 min |
| HIGH | Degraded (rejections, data gaps, drift) | 15 min | 15 min |
| MEDIUM | Operational (report failed, disk) | 60 min | 60 min |
| LOW | Informational (retraining done) | — | — |

## Escalation ladder
1. First channel(s) fired (CH_30/01).
2. No ack within SLA → escalate to next channel/contact (e.g., phone/push #2).
3. Still no ack and CRITICAL → the system's *automatic protective behavior*
   is the real backstop: it already halted/flattened (CH_23). Escalation is for
   review, not for safety (safety never waits on humans).

## Pseudo-code
```
def on_alert(a):
    notify(a)
    schedule_check(a, sla(a)):
        if not a.acked: escalate(a, next_step)      # paging, extra channels
```

## Auto-action vs human decision
- Safety-critical actions (flatten, halt) are **automatic** — they never wait
  for acknowledgment.
- Human decisions (re-enable trading, deploy new model) require explicit,
  authorized, audited actions (CH_34/02).

## Rules
- Escalation schedules are config, documented and tested (CH_36).
- Every escalation is logged (who was paged, when, ack status).
- After-hours: batch alerts into a morning digest (no noise at night), except
  CRITICAL infrastructure alarms.
