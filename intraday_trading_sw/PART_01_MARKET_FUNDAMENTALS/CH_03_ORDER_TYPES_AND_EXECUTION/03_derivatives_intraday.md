# 03 — Intraday Derivatives (Futures & Options)

## Purpose
Extend the system's understanding to derivatives: futures and options have
their own microstructure, margin, pricing, and expiry behavior that must be
modeled correctly before any intraday strategy touches them.

## Futures specifics
- **Contract specs**: tick size, tick value, lot/contract size, margin per
  contract, settlement, and expiry months — per symbol, per exchange.
- **Margin & leverage**: positions are margined; leverage is high; per-trade
  risk math (CH_21) must use margin and worst-case loss correctly.
- **Expiry/roll**: near-month expires; positions and data must roll (CH_07/04).
  Roll weeks have volume/tracking effects.
- **Calendar spreads**: intraday basis between months — a relative-value
  strategy (CH_13/03) with its own risks.
- **Intraday margin calls**: price spikes can trigger margin shortfalls — the
  risk layer must account for worst-case (gap) exposure (CH_20/01).

## Options specifics
- **Greeks** (computed from a pricing model — implementable from scratch,
  CH_00/02):
  - **Delta**: sensitivity to underlying price.
  - **Gamma**: rate of change of delta (position convexity).
  - **Theta**: time decay (options bleed value toward expiry).
  - **Vega**: sensitivity to implied volatility.
  - **Rho**: sensitivity to interest rates (minor intraday).
- **Implied volatility (IV)**: derived from market prices (invert a pricing
  model); IV surfaces and skew are tradable signals themselves.
- **Expiry decay**: theta accelerates near expiry; strategies must account for
  it (an option's "value" falls even if the underlying doesn't move).
- **Open interest & volume**: liquidity and positioning clues per strike/series.
- **Exercise/settlement risk**: avoid holding to expiry; flatten by intraday
  close or defined window (CH_23/01).

## Data requirements (add to the catalog, CH_05)
- Underlying spot data aligned in time to the option/future series.
- Option chains: strikes, expiries, bids/asks, IV, OI (if the feed provides).
- Contract spec tables (versioned).

## Pseudo-code: Black-Scholes delta (reference math)
```
def normal_cdf(x):  # standard normal CDF (implementable via erf/approximation)
def delta_call(S, K, T, r, sigma):
    d1 = (ln(S/K) + (r + sigma^2/2)*T) / (sigma*sqrt(T))
    return normal_cdf(d1)
```
(Used only if the broker/feed doesn't provide Greeks.)

## Rules
- Never treat options P&L as linear: position P&L must be mark-to-model (Greeks
  + underlying) or feed-derived.
- Derivatives strategies declare contract specs and margin in their manifest
  (CH_13/00); risk gates verify margin sufficiency (CH_20/01).
- Roll/expiry handling is mandatory before any futures/options go live
  (CH_07/04) — do not start with derivatives in the MVP (CH_44/00).
