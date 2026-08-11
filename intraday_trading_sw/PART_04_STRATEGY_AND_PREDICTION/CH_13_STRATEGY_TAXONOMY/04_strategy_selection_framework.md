# 04 — Strategy Selection Framework

## Purpose
Decide, at any moment, which strategy is allowed to act — and which is not —
based on regime, liquidity, volatility, session, and events.

## Selection inputs (all time-aware)
- **Regime** (CH_10/01): TRENDING_UP/DOWN → momentum family; RANGE → mean reversion.
- **Volatility percentile** (CH_10/03): extreme low/high → tighten or pause.
- **Liquidity** (CH_02/00): below threshold → no strategy.
- **Session phase** (CH_02/02): strategy manifest declares allowed phases.
- **Events** (CH_12/02): pause windows near high-impact releases.
- **Capital/state**: daily loss limit reached → all strategies halted (CH_23).

## Decision flow (pseudo)
```
def select_strategies(context):
    pool = []
    for s in enabled_strategies:
        if not s.regime_ok(context.regime): continue
        if not s.vol_ok(context.vol_perc): continue
        if not s.liquidity_ok(context.liquidity): continue
        if not s.phase_ok(context.phase): continue
        if not s.event_ok(context.calendar): continue
        pool.append(s)
    return risk_filter(pool)   # per-strategy limits, portfolio limits
```

## Portfolio-level coordination
- Cap total concurrent positions and gross exposure (CH_20).
- Correlation guard: don't stack correlated signals (same sector/theme) into
  one large bet.
- Diversity: prefer families with different edge sources so a regime shift
  doesn't kill everything at once.

## Pseudo-code: correlation guard
```
if new_signal.correlates_with(open_positions) and exposure_exceeds(limit):
    reject(signal, "correlated_exposure_limit")
```

## Rules
- Selection is re-evaluated every bar (context changes), never cached blindly.
- A strategy may be enabled but *not selected* — that is normal, not a bug.
- Log every selection/rejection reason (audit, CH_33) — this is how you tune.
