# 01 — Phased Development Plan

## Purpose
Turn the resource into an ordered build sequence with milestones, so progress
is measurable and every stage is validated before the next.

## Phase map (build order = chapter order)
| Phase | Builds | Gate to pass before moving on |
|---|---|---|
| P0 Foundations | CH_00, CH_01, CH_02, CH_03 | concepts understood; decisions recorded |
| P1 Data | CH_05–CH_08 | validated store; data KPI ≥ 99% |
| P2 Features/Analysis | CH_09–CH_12 | feature catalog + tested indicators |
| P3 Strategy | CH_13–CH_16 (rules first) | signals deterministic; no leakage |
| P4 Backtest | CH_17–CH_19 | honest reports; overfitting gate |
| P5 Risk | CH_20–CH_23 | limits enforced in tests |
| P6 Execution | CH_24–CH_27 | OMS + simulator reconcile cleanly |
| P7 Live Platform | CH_28–CH_30 | engine loop stable; dashboards live |
| P8 Operations | CH_31–CH_35 | monitored, secured, backed up, recoverable |
| P9 QA/Paper | CH_36–CH_38 | acceptance + dry-run green |
| P10 Governance | CH_39–CH_40 | disclaimers + policy live |
| P11 Release | CH_41–CH_42 | open-sourced, docs, CI |
| P12 Scale | CH_43–CH_44 + live ladder | graduated live (CH_37/02) |

## Time-boxing guidance
- P0–P3: 4–8 weeks (experienced developer).
- P4–P6: 4–8 weeks.
- P7–P8: 4–8 weeks.
- P9: 4–12 weeks of paper trading (unhurried — this is where trust is earned).
- Total realistic MVP-to-paper: ~6–9 months; live graduation after that.

## Iteration rule
- Do not start a phase until the previous gate passes (CH_36/02 acceptance).
- Each phase ends with: tests, docs, and a written review.

## Pseudo-code: phase runner
```
for phase in PLAN:
    implement(phase)
    if not gate(phase): block(); review; return
    review_and_doc(phase)
```

## Rules
- Milestones are defined by gates, not by calendar promises.
- A gate failure is a reason to rework, never to skip.
- Revisit the plan quarterly; markets and needs change (CH_42/02).
