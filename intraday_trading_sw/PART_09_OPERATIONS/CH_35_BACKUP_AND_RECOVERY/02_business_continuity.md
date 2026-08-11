# 02 — Business Continuity

## Purpose
Ensure the trading operation can survive scheduled and unscheduled absences and
continue to protect capital automatically.

## Continuous protection principle
- **Protective orders live at the broker** (stops/brackets, CH_03/01) — they
  survive even if every local process dies. This is the ultimate continuity
  backstop for open risk.
- Flat-by-close policy (CH_23/01) means no overnight positions to manage — the
  biggest continuity simplification for intraday.

## Coverage scenarios
- **Operator away**: system runs unattended under risk limits + alerting
  (CH_30); degraded mode = automatic halt-on-alert (CH_23/00). Someone returns
  to review incidents, not to babysit.
- **Scheduled maintenance**: EOD/weekend windows; nightly jobs can re-run after.
- **Long absence**: reduce auto-trading aggressiveness (config) and rely on
  monitoring + escalation (CH_30/02).

## Runbook (documented, in-repo)
- One page per scenario: symptom → automated behavior → human actions →
  recovery steps. E.g., "feed down 10+ min", "breaker tripped", "broker outage",
  "machine loss" (CH_35/01).

## Pseudo-code: continuity checklist (pre-session)
```
pre_session():
    check(calendar_ok); check(feed_ok); check(broker_ok)
    check(reconciliation_clean); check(backup_fresh); check(drills_recent)
    log("session_start", ok=all)
```

## Rules
- If humans are unavailable, the system's default is *more conservative*, never
  more aggressive (fail-safe, CH_20/00).
- The runbook lives with the repo and is tested in drills (CH_35/01, CH_37).
- Continuity decisions (who can reduce limits, etc.) follow access control
  (CH_34/02) — no "post-it password" backdoors.
