# 02 — Statistical Significance

## Purpose
Determine whether a backtest edge is real or a lucky draw — before risking money
on it.

## Why significance matters
Few trades + high volatility ⇒ apparent edges are noise. Significance testing
quantifies "what fraction of that result could be luck".

## Methods (all must pass, in order)
1. **Sample size sanity**: minimum ~30–100 trades (per strategy) before any claim.
2. **Bootstrap confidence intervals**: resample trades/days with replacement;
   report 90% CI of net P&L, Sharpe, expectancy. If CI includes ≤ 0 → not proven.
3. **Deflated Sharpe / multiple-testing adjustment**: when scanning many variants,
   expected best Sharpe inflates; adjust for the number of trials (CH_19/02).
4. **Permutation test on labels**: shuffle buy/sell outcomes; how often does
   random beat your strategy? p < 0.05 (with enough trades) is evidence.
5. **Out-of-time replication**: confirm on a later period that wasn't used.

## Pseudo-code: bootstrap CI of expectancy
```
samples = []
for i in range(2000):
    resample = np.random.choice(trades, len(trades), replace=True)
    samples.append(expectancy(resample))
lo, hi = quantile(samples, 0.05), quantile(samples, 0.95)
pass = lo > 0
```

## Pseudo-code: permutation test (simplified)
```
stat0 = expectancy(trades)
for i in range(1000):
    shuffled = permute(signs, len(trades))      # random wins/losses same counts
    perm_stats.append(expectancy(shuffled))
p = fraction(perm_stats >= stat0)
```

## Decision rule
- Strategy passes for **live candidate** only if: expectancy CI excludes 0,
  permutation p < 0.05, and it survives walk-forward (CH_19) and paper trading.

## Rules
- Significance results are part of every strategy report (CH_18/03).
- Adjust for multiple testing whenever you ran a parameter scan.
- A non-significant result is not failure — it's the system working (CH_00/02).
