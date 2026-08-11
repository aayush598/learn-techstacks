# 02 — Parameter Optimization

## Purpose
Tune strategy/model parameters systematically while quantifying — and defending
against — the overfitting that tuning itself creates.

## Tuning protocol
1. **Define the search space explicitly** (small, rational): each parameter with
   a range of 3–10 candidate values (intraday strategies usually have few params).
2. **Grid or limited random search** on the validation window only.
3. **Early stop the search**: stop adding configs once gains plateau.
4. **Evaluate the finalists** on the held-out test exactly once (CH_19/00).
5. **Sensitivity check**: perturb each param ±20%; if performance collapses, the
   optimum is a spike, not a plateau — reject.

## Pseudo-code: sensitivity check
```
best = optimize(validate)
for p in best.params:
    for delta in (±20%):
        variant = best.with(p + delta)
        if metrics(variant, validate) << metrics(best): flag_fragile(best)
```

## Multiple-testing inflation (deflated Sharpe)
When you try N configs, the best of N is biased upward. Adjust the claim:
```
expected_best_sharpe ≈ sharpemean + sqrt(2*ln(N)) * std_sharpe   # approximation
if best_sharpe < expected_best_sharpe + margin: treat as noise
```
Better: report the *whole* search distribution, not just the winner.

## Practical rules
- Number of configs ≤ dozens for intraday (few parameters, small data).
- Never tune on the test set; never tune on the full dataset.
- Finalists must be validated by walk-forward (CH_19/01) and paper trading.
- Log every tried configuration with its result (reproducibility, CH_33).

## Rules
- A parameter that only works at one exact value is a bug, not a feature.
- Prefer plateaus: regions where neighboring params work too.
- Optimization without the costs model is meaningless (CH_17/02).
