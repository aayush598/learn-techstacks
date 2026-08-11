# 01 — Trailing and Time Stops

## Purpose
Use trailing stops to let winners run while protecting gains, and time stops to
exit trades that "go nowhere" (opportunity cost + noise risk).

## Trailing stop variants
- **ATR trail**: stop = max(stop_prev, price − k×ATR) for longs (ratchet up
  only). Adapts to volatility; k tuned per strategy.
- **Structure trail**: ratchet to below each new higher-low (CH_11/01).
- **Parabolic/chandelier**: trail from the highest close/ATR since entry.
- **Fixed % trail**: simple, but breaks in volatile names (noise-bait).

## Pseudo-code: ATR trail (long)
```
def update_trail(pos, bar, k):
    new_stop = bar.price - k * bar.atr
    if new_stop > pos.trail_stop:
        pos.trail_stop = new_stop          # ratchet only up
        if pos.broker_stop: modify_stop(pos.broker_stop, new_stop)
```

## Time stops
- Mean reversion: exit after max N bars regardless of P&L (reversion thesis has
  a shelf life).
- Intraday universal rule: **no positions past the session close** — time stop
  at a fixed minutes-before-close (e.g., flatten 10–15 min before).
- Optional: "time stop if no progress" — exit if after N bars the trade is
  within M×ATR of entry (dead trade).

## Rules
- The tightest rule wins: whichever of hard stop / time stop / trail / target
  triggers first (CH_14/02 priority).
- Trailing stops are updated only when they tighten (never loosen) in live code.
- Broker-side trail is preferred when the broker supports it; else software
  trail with frequent re-quoting (CH_25).
