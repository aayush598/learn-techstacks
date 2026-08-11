# 01 — Entry Rule Design

## Purpose
Design entry conditions that are precise, minimal, and statistically honest —
the bar where the decision is made must be well-defined.

## Entry design principles
1. **One trigger, few confirmations**: 1 trigger + 1–2 confirmations beats 8
   conditions (overfitting risk grows with every added rule, CH_19).
2. **Price precision**: entry is defined on a specific reference (close of bar t,
   breakout level, stop order). Never "somewhere around".
3. **Confirmations are independent**: relative volume + regime + phase measure
   different things; don't add three flavors of the same signal.
4. **Tradeability**: the entry must be executable at realistic fills (limit at
   level, market on confirmation close) — backtest must use the same (CH_17).

## Template: breakout entry
- **Reference**: bar t close (signal bar). Entry executed at t+1 open/stop with
  slippage (never at the same close price — that's look-ahead).
- **Trigger**: close beyond level + buffer.
- **Confirm**: rel_volume ≥ 1.5 and ADX regime trending.
- **Exclusion**: skip if within event window, vol percentile extreme, or
  correlated exposure at limit.

## Pseudo-code: entry evaluation at bar t
```
if not base_filters(ctx): return None
if trigger(ctx) and confirms(ctx):
    return Entry(price=reference(ctx), side=side(ctx),
                 stop=stop(ctx), target=target(ctx),
                 ts=bar.t, reasons=[...])
```

## Timing convention (critical)
- Signal at bar t close → execution modeled at t+1 (next bar open or triggered
  stop), with slippage. This single convention removes most look-ahead bugs.

## Rules
- Every condition must be expressible in the signal language (CH_14/00).
- Document what each condition *should* protect against (regime, noise, news).
- The number of entry rules is a risk factor: fewer is better, always.
