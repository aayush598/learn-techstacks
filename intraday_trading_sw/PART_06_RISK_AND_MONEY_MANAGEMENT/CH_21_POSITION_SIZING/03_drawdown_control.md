# 03 — Drawdown Control

## Purpose
Respond to drawdowns systematically so a losing streak shrinks risk instead of
feeding revenge trading.

## Drawdown awareness
- Track max drawdown (CH_18/00) continuously; know your historical worst.
- Rule of thumb: expect a drawdown of 2–3× your average, eventually. Plan for it.

## Progressive de-risking on drawdown
1. Normal: f = base fraction (e.g., 0.5%).
2. DD ≥ 5%: halve f.
3. DD ≥ 10%: quarter f and require strategy review before resuming normal.
4. DD ≥ hard limit (e.g., 15–20%): halt trading, flat, human review required.

## Pseudo-code: drawdown-based multiplier
```
dd = drawdown_from_peak(equity)
if   dd < 0.05: f_mult = 1.0
elif dd < 0.10: f_mult = 0.5
elif dd < 0.15: f_mult = 0.25
else:            halt = True
effective_f = base_f * f_mult
```

## Recovery behavior
- After a de-risk event, resume at the reduced size; scale back up only after
  N profitable days (never immediately — market may still be hostile).
- Log every de-risk decision (the risk journal, CH_33).

## Rules
- Drawdown control is automatic (code), not a suggestion to the trader.
- De-risking applies to all strategies simultaneously (portfolio level).
- A de-risk/halt event pages a human (CH_30) and is reviewed in daily ops (CH_32).
