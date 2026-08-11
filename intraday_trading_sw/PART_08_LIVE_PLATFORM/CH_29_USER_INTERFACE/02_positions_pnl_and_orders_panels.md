# 02 — Positions, P&L, and Orders Panels

## Purpose
Present the trader with an accurate, live, and unambiguous view of what the
system is doing — and what risk it carries right now.

## Positions panel (per position)
- symbol, side, qty, entry price, current price, unrealized P&L (abs and %),
  stop/target (from the trade plan, CH_14/02), open duration, strategy id.

## P&L panel
- today's realized, unrealized, net (after costs); equity curve (session);
  % vs daily limits (CH_23/01); drawdown from peak (CH_21/03).
- per-strategy P&L breakdown (for review, CH_32).

## Orders panel (recent)
- id, symbol, side, type, qty, price/stop, state (CH_25/01), timestamp, reason
  (source), rejection reason when rejected.
- Live/unfilled orders highlighted; bracket links visible (CH_03/01).

## Pseudo-code: positions view
```
def positions_view():
    for pos in oms.positions():
        yield {
          symbol, side, qty, entry, last=mark(pos),
          upnl=pnl(pos), stop=pos.plan.stop, target=pos.plan.target,
          strategy=pos.plan.strategy, age=age(pos)
        }
```

## Consistency rules
- All panels derive from one engine snapshot (CH_29/00) — no mixed-state reads.
- Unrealized P&L uses the last validated close/mid, with its timestamp shown.
- Position counts must match the risk layer's exposure view (CH_20/02) —
  a mismatch is a visible alarm.

## Rules
- Panels show *state*, not advice — no "suggested" actions beyond the audited
  commands the system itself already made.
- Rejected orders are shown with their risk reason (education + trust, CH_23/02).
- Timeouts/staleness are shown on the panel, never hidden.
