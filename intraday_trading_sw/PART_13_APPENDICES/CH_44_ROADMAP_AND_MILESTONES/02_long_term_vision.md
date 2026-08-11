# 02 — Long-Term Vision

## Purpose
Describe where the project can grow — while keeping the core principles (risk
first, honest, self-hosted, open) intact.

## Long-term directions
- **More markets & instruments**: equities → futures/options/FX/crypto with the
  same architecture (data/adapters/config, CH_05, CH_24).
- **Strategy breadth**: curated community strategy library with mandatory
  backtest + checklist per contribution (CH_42/00).
- **Models**: validated ML layer (CH_15) with model registry, drift monitoring,
  and calibration — always behind the honesty gates (CH_16, CH_40).
- **Advanced execution**: multi-venue routing, better impact models (CH_26).
- **Deeper microstructure**: L2/tape strategies for those with the data (CH_11/02).
- **Ecosystem tooling**: browser-based strategy editor, packaged docs site,
  one-command deployment (CH_31).
- **Research collaboration**: shared, licensed datasets contributed by the
  community (CH_39/02).

## What will NOT change (non-negotiables)
- No profit guarantees; disclaimers always visible (CH_40/02).
- Risk limits un-removable and enforced in code (CH_20/00).
- No manipulation features, ever (CH_39/00).
- No proprietary black boxes in core modules (CH_00/02).
- Backtest honesty: costs, assumptions, and significance in every report
  (CH_18).

## Vision statement
> A trustworthy, self-hosted, open-source intraday trading platform that anyone
> can inspect, run, and extend — engineered to protect capital first, validated
> honestly before every step, and never promising what markets cannot guarantee.

## Pseudo-code: vision guard
```
def future_ok(feature):
    return (respects_risk_first() and is_honest() and is_open()
            and no_manipulation() and self_hostable())
```

## Rules
- Every roadmap item passes `future_ok()` (CH_42/02 roadmap sharing).
- Growth happens by *validated* increments, not by feature sprawl.
- The community's trust is the product; guard it above all (CH_00/02).
