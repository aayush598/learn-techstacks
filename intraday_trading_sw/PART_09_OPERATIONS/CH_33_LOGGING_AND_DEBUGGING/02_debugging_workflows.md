# 02 — Debugging Workflows

## Purpose
Define standard procedures for diagnosing problems in a live trading system —
fast, safe, and evidence-based.

## Golden rules of live debugging
1. **Protect first**: if the anomaly touches orders/positions, halt/flatten the
   affected scope (CH_23) *before* investigating. Trading safety is not debuggable.
2. **Read the chain**: start from the decision_id / timestamp and follow the
   journal (CH_33/01) — never guess from memory.
3. **Replay, don't reason**: reproduce the decision locally from stored data.
4. **Change one thing**: one fix, then verify with tests + replay, then deploy
   through the gate (CH_12/CH_41 CI).

## Common symptom → first check
| Symptom | First check |
|---|---|
| No signals | strategy selected? gates/regime? data gap? (CH_13/04, CH_06) |
| Signals but no orders | risk rejection reasons in journal (CH_20) |
| Order stuck | OMS state machine / reconciliation (CH_25) |
| Slippage worse than modeled | fill vs mid, impact, spread at time (CH_26) |
| Backtest differs from live | cost model, timing convention, data version (CH_17) |
| Model degrading | drift metrics, retrain recency (CH_16/03) |

## Pseudo-code: debug checklist
```
def debug_issue(incident):
    scope = identify_scope(incident)        # symbols/strategies/orders
    protect(scope)                          # halt if needed
    chain = trace(incident.decision_id)     # journal walk
    replay = replay_decision(chain)
    hypothesis = diff(actual, expected)
    fix_verify_deploy(hypothesis)           # test -> deploy -> monitor
```

## Tooling
- Log viewer, dashboard, replay harness, backtest re-run — all runnable from the
  repo (CH_12/CH_41) — no external SaaS needed.

## Rules
- Every incident ends with a written review (what/when/why/fix/prevention)
  stored with the repo (CH_32/02 incident flow).
- No code changes during market hours except for protection fixes, and those go
  through the emergency deploy path (CH_12/CH_41).
