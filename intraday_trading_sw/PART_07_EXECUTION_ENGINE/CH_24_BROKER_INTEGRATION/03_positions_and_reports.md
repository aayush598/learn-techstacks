# 03 — Positions and Reports

## Purpose
Keep an accurate, continuously reconciled view of positions, balances, and
executions — the ground truth the risk layer and UI depend on.

## Position model
- Derived from executions + corporate actions, never assumed from memory.
- Fields: symbol, side, qty, avg_entry, realized_pnl, unrealized_pnl, open_ts.
- Intraday rule: positions flatten by session close (CH_23/01).

## Sources of truth and order
1. **Broker authoritative state** (get_positions/get_orders) — final.
2. **OMS execution journal** (our records) — first-level.
3. **Trades/executions feed** — streaming updates.

## Pseudo-code: reconciliation
```
def reconcile():
    broker_pos = broker.get_positions()
    oms_pos    = oms.journal_positions()
    diffs = compare(broker_pos, oms_pos, tolerance=lot_size)
    if diffs:
        alert("position_mismatch", diffs)
        adopt(broker_pos, diffs)     # broker is authoritative
    else:
        status = RECONCILED
```
Run: on startup, after every fill, on reconnect, and at EOD.

## Reports (daily & intraday)
- P&L by symbol/strategy; executed orders; rejected orders with reasons;
  risk events (halts, limits hit); slippage stats (CH_17/02 model vs real).
- EOD report integrates with CH_18/03 reporting (live vs paper vs backtest).

## Rules
- Positions are always reconciled before any risk decision that depends on
  exposure (CH_20/02).
- A mismatch is a top-severity alert and halts new entries until resolved.
- Execution journal is append-only; corrections are new entries (audit, CH_33).
