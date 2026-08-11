# 04 — Futures Rolls and Continuous Contracts

## Purpose
Handle futures expiry/roll correctly so data, features, backtests, and live
trading stay consistent across contract months — preventing price "jumps" from
being mistaken for market moves.

## The roll problem
When the near month expires, the front contract changes. Switching symbols
creates a synthetic price jump from rollover (institutional carry), which
corrupts features and backtests if unhandled.

## Terminology
- **Front (near) month**: contract closest to expiry; usually the reference.
- **Back month**: later-dated contract.
- **Roll window**: the period during which volume shifts from front to back.
- **Continuous contract**: a synthetic series joining multiple contract months.

## Roll policy options
1. **Calendar/volume rule**: roll when the back month's volume/price exceeds the
   front (or on a fixed day before expiry). Simple and robust.
2. **Day-of-month rule**: roll on a fixed day (e.g., 5 sessions before expiry).
   Deterministic, easy to backtest, but may leave the series illiquid.

## Adjusting the continuous series
- **Unadjusted**: raw prices, easy to understand; jumps remain — must be
   handled by the strategy (detect & exclude).
- **Ratio-adjusted**: multiply historical prices by a roll ratio so series is
   continuous; preserves return ratios, distorts absolute levels.
- **Difference-adjusted**: add a roll spread; preserves levels poorly.
Pick one, document it, and apply identically in backtest and live.

## Pseudo-code: ratio-adjusted continuous price
```
def continuous_price(series, roll_dates):
    adj = 1.0; out = []
    for i, bar in enumerate(series):
        if bar.date in roll_dates and i > 0:
            ratio = prev_close / bar_open_of_new_contract
            adj *= ratio
        out.append(bar.close * adj)
    return out
```

## Steps to implement
1. Maintain a contract-spec + roll-date table (versioned, CH_08).
2. Decide roll rule (volume-based preferred over fixed-day).
3. Build the continuous series for backtesting; note roll dates in metadata.
4. Live: track the front contract, roll positions/data on the policy date
   (flatten or carry with roll accounting — CH_23/01).
5. Validate: no synthetic jumps survive in returns on roll dates.

## Rules
- Backtest and live must use the **same** roll policy and adjustment method.
- Roll dates are part of the trading calendar (CH_02/03).
- Report rolls in the backtest report (CH_18/03) so reviewers see them.
- Never mix adjusted and unadjusted series within one feature pipeline (CH_09).
