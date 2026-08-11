# 00 — Strategy Classification

## Purpose
Give every strategy a typed identity (regime, horizon, edge source) so the
system can select, gate, and evaluate strategies coherently.

## Classification axes
1. **Regime** — mean-reversion | momentum/breakout | arbitrage | market-making | event.
2. **Edge source** — behavioral flows, structural (calendar/settlement), statistical
   (short-horizon autocorrelation), information asymmetry.
3. **Timeframe of decision** — which bars drive entry vs exit (context vs trigger).
4. **Risk profile** — expected win rate, payoff ratio, holding period, capital demand.
5. **Dependence** — data-only vs needs L2/tape vs needs news/calendar.

## Strategy manifest (required per strategy)
```
name, version, regime, instruments[], timeframe(trigger/context),
entry_conditions[], exit_conditions[], stop/target rules,
filters (liquidity, vol percentile, session phase, events),
sizing policy ref, position limit, data needs, params[],
expected behavior: win_rate_range, payoff_ratio, holding_bars
```

## Strategy families (detailed in sibling files)
- Mean reversion (CH_13/01) — fade extremes in range.
- Momentum/breakout (CH_13/02) — ride follow-through after structure breaks.
- Arbitrage/spread (CH_13/03) — relative-value between related instruments.
- Market-making (optional, infra-heavy) — earn spread, inventory risk.

## Selection framework (CH_13/04) — which strategy to run when
Regime classifier (CH_10/01) picks the family; liquidity/vol filters gate it.

## Pseudo-code: strategy registry
```
registry = { "meanrev_1m": MeanRevStrategy, "breakout_15m": BreakoutStrategy, ... }
def get_strategy(name):
    s = registry[name](manifest=MANIFESTS[name])
    return s   # strategies are stateless; state lives in the engine
```

## Rules
- Strategies are **pure logic** (decide); the engine holds state and risk.
- A strategy must declare its data needs so the platform verifies availability.
- No strategy runs without a manifest, backtest record, and risk approval.
