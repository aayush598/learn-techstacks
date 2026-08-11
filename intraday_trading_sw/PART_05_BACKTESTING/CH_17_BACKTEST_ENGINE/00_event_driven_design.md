# 00 — Event-Driven Backtest Design

## Purpose
Design a backtester that processes data bar-by-bar (event-driven), applying
fills, costs, and risk exactly as live trading would.

## Why event-driven (not just vectorized)
- Matches live behavior: orders take effect at their *next possible* bar.
- Naturally enforces no-look-ahead (you only see data up to the current bar).
- Handles stateful logic: position, open orders, trailing stops, multiple
  concurrent positions.
- Slower than vectorized but the *honest* reference implementation.

## Core loop
```
def backtest(strategy, bars, costs):
    state = PortfolioState()
    for bar in bars:
        ctx = build_context(bar, state)          # features, indicators, positions
        decision = strategy.decide(ctx)          # CH_14/03 (pure)
        orders = translate_to_orders(decision, costs)   # fills at next bar open
        state.process_executions(bar, orders)    # apply fills + costs
        state.update_mark(bar)                   # mark positions to market
        record_trade_events(state, bar)
    return report(state, bars)                   # CH_18
```

## Order execution timing (the no-look-ahead rule)
- Signal decided on bar t close → order simulated for **bar t+1 open** (or a
  trigger/stop intra-bar), with slippage (CH_17/02).
- Never fill at bar t close when the signal used bar t close.

## State components
- Cash, open positions, pending orders, realized/unrealized P&L, trade log,
  equity curve.

## Pseudo-code: portfolio state
```
class PortfolioState:
    cash, positions{symbol: qty}, orders[], equity_curve[]
    def process_executions(bar, orders):
        for o in orders: fill(o, bar.open + slippage); cash -= gross+cost
    def update_mark(bar): equity = cash + Σ qty*bar.close
```

## Rules
- Event-driven backtest is the *canonical* evaluation; vectorized (CH_17/01)
  is for fast screening only.
- Backtest must be deterministic (same seed/data → identical results).
- A backtest that passes every gate here is a *candidate*, not a promise (CH_19).
