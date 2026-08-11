# 02 — Kelly Criterion and Growth Criteria

## Purpose
Understand growth-optimal sizing — and why full Kelly is dangerous in practice.

## Kelly formula (simplified, single-bet)
```
f* = edge / odds = (p×b − q) / b
p = win probability, q = 1−p, b = payoff ratio (avg win/avg loss)
```

## Pseudo-code
```
def kelly(p, b):
    return max(0.0, (p*b - (1-p)) / b)   # f* as fraction of equity
```

## Why fractional Kelly
- Kelly assumes known, stationary probabilities — markets violate this.
- Full Kelly = huge drawdowns (risk of ruin from estimation error + fat tails).
- Standard practice: **quarter-Kelly to half-Kelly** (0.25–0.5× f*) and a hard
  cap (e.g., 2% per trade) from the policy (CH_20/01).

## Pseudo-code: fractional Kelly sizing
```
k = kelly(p_est, b_est)
k_safe = min(0.5 * k, policy.max_fraction)     # half-Kelly, capped
risk_amount = equity * k_safe
qty = floor(risk_amount / stop_distance)
```

## Estimation honesty
- p and b must come from out-of-sample validation (CH_19), never in-sample.
- Re-estimate on rolling windows; if estimates are unstable, distrust them.
- Kelly with a coin-flip p of 0.52 and b=1 yields f*=4% — that's why intraday
  traders rarely use pure Kelly: their edges are small and noisy.

## Rules
- Kelly output is *always* multiplied by a fraction ≤ 0.5 and capped by policy.
- Never let Kelly-style growth bets push per-trade risk above the global cap.
- Report the Kelly estimate as a metric, not as an instruction.
