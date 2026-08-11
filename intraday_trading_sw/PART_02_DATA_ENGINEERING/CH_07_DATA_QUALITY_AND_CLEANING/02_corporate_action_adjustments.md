# 02 — Corporate Action Adjustments

## Purpose
Handle splits, dividends, and mergers so historical prices are comparable and
returns are computed correctly (backtests and models must not be distorted).

## Common actions and their effect
- **Stock split** (e.g., 2:1): price halves, share count doubles. Historical
  prices must be divided; volume multiplied.
- **Reverse split**: opposite direction.
- **Cash dividend**: price drops on ex-date by ~dividend amount; total-return
  models add it back; price-only models adjust for the drop to avoid a fake loss.
- **Mergers/delistings**: series end/transform; mark symbol change or remove.
- **New listings**: series start mid-history; ensure consistent start.

## Adjustment policy (pick and document)
- **Adjusted prices**: all history restated in today's terms (best for models).
- **Unadjusted prices**: raw market prints (needed for fill simulation realism).
- Keep **both**; mark which is which. Signals use adjusted; execution/backtest
  fills use raw.

## Steps
1. Maintain a corporate-action calendar (exchange/broker source or curated file).
2. Apply action on ex-date; recompute only the affected series' adjusted fields.
3. Validate: adjusted series must not jump on the ex-date (except real news).
4. Version the series (adjustment re-run = new version, never in-place mutation).

## Pseudo-code: apply split
```
for bar in history_before(ex_date):
    bar.adj_open   = bar.open / ratio
    bar.adj_high   = bar.high / ratio
    bar.adj_low    = bar.low  / ratio
    bar.adj_close  = bar.close/ ratio
    bar.adj_volume = bar.volume * ratio
```

## Rules
- Never mix adjusted and unadjusted series in one calculation.
- A return computed across an ex-date must use adjusted prices (or the dividend).
- Record the corporate-action version in every dataset artifact.
