# 01 — Daily Limits and Halts

## Purpose
Enforce session-level discipline: bounded loss, bounded activity, and a forced
end-of-day — even when the system "feels" like trading more.

## Daily limit set (enforced by code)
- **Max daily loss** (e.g., 2% of equity) → flatten + halt for the day.
- **Max daily win / profit target** (optional) → stop trading after locking in
  a target (avoids giving it back).
- **Max trades/day** → caps overtrading and fee bleed.
- **Max consecutive losing trades** (e.g., 5) → pause + human review (CH_30).

## Halt behavior
- New entries disabled; existing positions flattened per policy.
- No "one more trade" override — the halt is in the risk layer, not the UI.
- Auto-resume next session, but reduced size if drawdown rules apply (CH_21/03).

## Pseudo-code: daily limits state
```
state.daily = { pnl, trades, consec_losses }
def on_trade_close(t):
    state.daily.pnl += t.pnl
    state.daily.trades += 1
    state.daily.consec_losses = consec(t.pnl)
    check_daily_limits(state.daily, policy)   # may trigger halt
```

## End-of-day procedure
- Flatten all by a configured time (e.g., 10–15 min before close).
- Generate EOD report (CH_18/03) and nightly batch (CH_32).
- Verify positions = 0 and equity reconciled before closing the session.

## Rules
- Daily limits live in risk_policy.yaml (CH_20/00) and are changed only between
  sessions, never mid-session.
- A halted day still runs monitoring/logging — data keeps flowing, orders don't.
- The trader cannot disable daily limits from the UI (authorization, CH_34).
