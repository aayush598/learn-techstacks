# 02 — Market Impact Minimization

## Purpose
Estimate and reduce how much your own trading moves price — the hidden cost
that grows with order size and aggressiveness.

## Impact model (estimate)
```
impact_bp ≈ k_impact × (order_qty / participant_volume)^0.5
```
where participant_volume = available depth/typical volume in the period.
Parameter k_impact is calibrated per symbol (from fills history or defaults).

## Pseudo-code: impact check
```
def impact_estimate(order, ctx):
    share = order.qty / ctx.recent_volume
    return k_impact[order.symbol] * sqrt(share)     # in bp
```

## Practical minimization rules
1. **Participation cap**: never exceed X% of recent volume per interval
   (e.g., 10% of a bar's volume → else slice, CH_26/01).
2. **Limit not market**: cross the spread only when required (CH_26/00).
3. **Avoid the moment**: delay when spread wide / book thin (liquidity check).
4. **Avoid the crowd**: don't pile into the same opening-minute spike.
5. **Reduce frequency**: fewer, larger child orders vs many tiny ones (fee + latency).

## Sizing feedback
- If estimated impact > strategy edge → the trade is too big for the liquidity;
  risk layer should reduce qty or reject (CH_20/01).

## Pseudo-code: participation gate
```
if order.qty > max_participation_pct * ctx.recent_volume:
    if slicing_enabled: return slice_plan(order)     # CH_26/01
    else: reject(order, "participation_cap")
```

## Rules
- Measure realized impact (fill vs pre-trade mid) and feed it back to k_impact.
- Never assume zero impact; backtests assume a conservative floor (CH_17/02).
- Impact grows non-linearly — respect the √share rule of thumb.
