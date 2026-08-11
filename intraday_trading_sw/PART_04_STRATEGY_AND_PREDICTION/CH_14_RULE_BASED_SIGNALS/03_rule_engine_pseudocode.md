# 03 — Rule Engine Pseudo-code

## Purpose
Give a complete, walkable reference implementation sketch of the rule engine so
it can be re-implemented correctly in any language.

## Core pieces
1. `Manifest` — strategy definition (CH_14/00).
2. `Context` — immutable snapshot of everything available at bar t
   (features, indicators, structure events, calendar, state).
3. `RuleTree` — compiled manifest (validated at load).
4. `Evaluator` — pure function manifest→decision.

## Pseudo-code: full decision cycle
```
def decide(manifest, ctx) -> Decision | None:
    # 1. Base gates
    for g in manifest.base_gates:             # regime, vol, liquidity, phase, events
        if not g.ok(ctx): return None

    # 2. Entry
    if no_open_position(ctx):
        if trigger(ctx) and confirms(ctx):
            plan = build_plan(manifest, ctx)  # stop/target/time computed here
            return Decision.ENTRY(plan)
        return None

    # 3. Exit management (only if a position exists)
    return Decision.EXITS(plan, ctx)          # CH_14/02 controller
```

## Pseudo-code: build_plan (entry-time values only)
```
def build_plan(m, ctx):
    entry_px = reference_price(ctx)           # close of signal bar, or level
    atr      = ctx.atr
    return {
      entry:  entry_px,
      stop:   entry_px - side*m.exit.stop_atr*atr,
      target: entry_px + side*m.exit.target_atr*atr,
      time_stop: m.exit.time_stop_min,
      trail:  m.exit.trail_atr,
      max_risk_pct: m.risk.max_risk_pct,      # sizing input (CH_21)
    }
```

## Determinism & purity
- `decide()` must return identical output for identical (manifest, ctx).
- No clock reads, no randomness, no I/O inside decide().
- All I/O (order placement, logging) happens outside, after decide returns.

## Concurrency
- The engine calls decide() on one thread per symbol (or a single sequential
  loop). No shared mutable state inside decide().

## Rules
- Keep decide() dependency-free: pass everything via ctx.
- Version manifests; decide() logs the manifest version in each signal (repro).
