# 02 — Exit Rule Design

## Purpose
Design the exit side — where most of a strategy's risk is controlled. Exits
must be mechanical and enforced before any entry.

## Exit types
- **Stop-loss** (CH_22): maximum acceptable loss in ATR units; hard protection.
- **Take-profit / target**: level where the thesis is complete (structure, POC,
  fixed R multiple).
- **Time stop**: exit after N bars regardless of P&L (mean reversion essential).
- **Trailing stop**: ratchet the stop behind the favorable move (let winners run).
- **Regime/invalidation exit**: thesis broken (e.g., breakout fails, regime flips).

## Exit priority (each exit competes; first to trigger wins)
1. Hard stop-loss (broker-level too, CH_03/01).
2. Time stop.
3. Thesis invalidation.
4. Trailing stop / target.

## Pseudo-code: exit controller per bar
```
for pos in open_positions:
    if bar.price <= pos.hard_stop:        exit(MARKET, "stop_loss")
    elif bar.t - pos.entry_ts >= time_stop: exit(MARKET, "time_stop")
    elif invalidation(pos):               exit(MARKET, "invalidation")
    elif target_hit(pos):                 exit(LIMIT, "target")
    else: update_trailing(pos, bar)       # ratchet, no exit yet
```

## Design guidance
- Exits are decided *at entry time* (values computed then, recorded in the
  trade plan). Late decisions invite emotion and look-ahead.
- Stops/targets are placed at the broker when live (defense in depth).
- Expect asymmetric realism: stops slip (fast markets), targets fill more
  predictably. Backtest with worst-case fills (CH_17).

## Rules
- A trade without a precomputed stop/target/time-stop is never submitted.
- Every exit event is logged with its reason (audit + tuning, CH_33).
- Evaluate exits every bar; never "wait and see" — the engine has no feelings.
