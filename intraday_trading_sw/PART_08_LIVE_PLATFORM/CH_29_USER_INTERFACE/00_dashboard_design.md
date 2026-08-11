# 00 — Dashboard Design

## Purpose
Design a self-hosted web dashboard that shows the live state of the system —
data health, signals, positions, risk, and P&L — without requiring cloud services.

## Layout (priority order)
1. **Risk/health header**: circuit-breaker status, daily loss/gain vs limits,
   equity vs drawdown band, data-feed health, OMS status. (Seen always.)
2. **Live P&L**: today's realized + unrealized P&L, equity curve (session).
3. **Positions panel**: open positions, entry, stop, target, unrealized P&L
   (CH_29/02).
4. **Orders panel**: recent orders + states (CH_25/01), rejects with reasons.
5. **Signals feed**: latest signals per strategy with confidence and reasons.
6. **Charts**: selected symbol candle + indicators + levels (CH_29/01).

## Design principles
- **Read-only by default**: the dashboard displays; all control flows through
  audited actions (risk policy changes, kill switch) with authorization (CH_34/02).
- **Freshness**: every panel carries a last-updated timestamp; stale panels are
  visually flagged.
- **Slow-render safe**: live updates via a single WebSocket or SSE channel
  (polling is a fallback only).

## Pseudo-code: dashboard data source
```
def ui_snapshot():
    return {
      health: monitor.summary(),                 # CH_32
      risk:   risk_state(),                      # limits, breakers, halted flags
      pnl:    pnl_daily(), equity_curve(),
      positions: oms.positions(), orders: oms.recent_orders(),
      signals: engine.recent_signals(),
    }
```

## Rules
- The dashboard never writes to the journal directly; every action is an
  audited command through the engine (CH_28).
- Dashboard availability must not affect trading (engine keeps running if UI dies).
- Refresh state is consistent: panels render from one snapshot, not mixed reads.
