# 03 — How to Use This Resource

## Purpose
Explain the reading order, conventions, and workflow so a newcomer can start
building immediately and consistently.

## Conventions used in every file
- **Parts** = major areas (folders `PART_NN_NAME`).
- **Chapters** = one topic (folders `CH_NN_TOPIC`).
- **Sections** = one sub-topic (files `NN_name.md`).
- Every file may contain: Purpose, Design Decisions, Steps, Pseudo-code,
  Rules/Checklist, References.
- Numbering is global and sequential (CH_00 … CH_44) so the reading order is
  strictly numeric.
- Pseudo-code is illustrative, not copy-paste-ready. It is language-agnostic.

## Recommended workflow
1. Read this README (you are here).
2. Read `PART_00` fully — the map and philosophy.
3. Build in this order, validating at each step:
   ```
   01 Market fundamentals (understand before coding)
   02 Data engineering     -> green: validated stored data
   03 Analysis engine      -> green: indicators/features tested
   04 Strategies + ML      -> green: signals produced
   05 Backtesting          -> green: honest evaluation
   06 Risk                 -> green: limits enforced
   07 Execution            -> green: paper orders reconcile
   08 Live platform        -> green: engine loop stable
   09 Operations           -> green: monitored & secure
   10 Quality & testing    -> gates for going live
   ```
4. Before real money: pass every gate in `PART_10/CH_37`.

## Golden loop for every feature
```
SPEC (what + why)
  -> DESIGN (steps)
  -> IMPLEMENT (pseudo-code to real code)
  -> TEST (unit + integration)
  -> VALIDATE (data/backtest realism)
  -> DOCUMENT (log, monitor, explain)
```

## How much time to expect
- MVP: realistic, careful build, ~3–6 months part-time for an experienced dev.
- Production hardening: another 3–6 months with paper trading.
- Expect to *reject* most strategies you build — that is normal and healthy.

## References
- `PART_13/CH_44/01_phased_development_plan.md`
- `PART_13/CH_43` glossary for unfamiliar terms.
