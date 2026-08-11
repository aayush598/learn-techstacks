# 00 — Signal Definition Language

## Purpose
Define a declarative, versioned language for expressing strategy rules so
strategies are data, testable, auditable — not scattered imperative code.

## Signal model
A signal is a typed event: `{ts, symbol, direction(LONG/SHORT/FLAT), confidence,
reason[], ref_bar, model_scores{}, meta}`. Confidence is mandatory (0–1) so risk
can scale by conviction.

## Rule expression format (YAML/JSON, declarative)
```
signal: breakout_open_range
enabled: true
regime: { adx_min: 22, allow: [TRENDING_UP, TRENDING_DOWN] }
filters:
  rel_volume_min: 1.5
  vol_percentile: [15, 95]
  session_phases: [OPEN, AFTERNOON, CLOSE]
entry:
  trigger: close > open_range_high + 0.3*atr
  confirm: [ rel_volume >= 1.5, flow_imbalance >= 0.2 ]
exit:
  stop: "entry - 1.5*atr"
  target: "entry + 2.0*atr"
  time_stop_min: 45
  trail: atr_mult(1.2)
```

## Rule atoms (operators available)
- Comparisons on features: `feature >= value`, `==`, `!=`, `in [...]
- Logical: `and`, `or`, `not`, sequence conditions (A then B within N bars).
- Event atoms: `event(level_touch)`, `event(breakout_up)`.
- Aggregates: `crossed_above(x,y)`, `max/min over window`, `zscore(x,w)`.

## Parser/evaluator contract
```
parse(manifest) -> RuleTree
evaluate(rule, context) -> (bool, reasons[], confidence)
```
- Pure function of (manifest, context at t). No hidden state, no time travel.

## Pseudo-code: evaluator
```
def evaluate(spec, ctx):
    if not all(spec.filters.ok(ctx)): return NO_SIGNAL
    trig = eval_expr(spec.entry.trigger, ctx)
    conf  = all(eval_expr(c, ctx) for c in spec.entry.confirm)
    if trig and conf:
        return SIGNAL(long/short, confidence=calc(spec, ctx))
    return NO_SIGNAL
```

## Rules
- Every rule expression is validated at load time (typos fail fast).
- Signals carry reasons so humans can inspect every decision.
- Rule language version is embedded in the manifest (schema evolution).
