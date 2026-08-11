# 00 — Simulation Environment

## Purpose
Build a realistic paper-trading environment: the simulator broker (CH_24/00)
plus live-market execution paths, so every feature is validated exactly as it
will run — without risking money.

## Components
1. **Simulator broker** (adapter): fills orders against the live feed/order book
   with the same cost model as backtests (CH_17/02). Supports: market, limit,
   stop, bracket, cancel, modify, partial fills, rejects (configurable).
2. **Paper engine**: the real engine (CH_28) running in "paper mode" (risk
   limits as configured, real manifests).
3. **Replay mode**: the same engine replaying a stored day — used for tests and
   for tuning (CH_36/02).
4. **Cost realism**: fills use mid/spread + slippage from the cost model; track
   realized vs theoretical slippage.

## Simulator fill logic (pseudo)
```
def fill(sim_order, market_state):
    if sim_order.type == MARKET:
        fill_px = market_state.ask/bid + slip(sim_order)    # adverse side
    elif LIMIT:
        fill if market trades through limit ± buffer
    apply_commission(sim_order); emit fill; update position
```

## Configuration
- Paper mode: same risk policy, same symbols, same strategies as planned live.
- Differentiator: capital is virtual; broker adapter is `simulator`.

## Rules
- Paper trading uses the *same* code path as live except for the broker adapter.
- Paper results are honest evidence: same costs, same timing, same risk.
- Run every feature in paper before enabling it live (CH_37/02).
