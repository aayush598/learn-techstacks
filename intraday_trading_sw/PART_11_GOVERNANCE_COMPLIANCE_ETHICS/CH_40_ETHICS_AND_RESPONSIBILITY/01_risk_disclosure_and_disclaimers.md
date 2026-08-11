# 01 — Risk Disclosure and Disclaimers

## Purpose
Provide the disclosure text and placement rules that keep users fully informed
of the risks — required, standardized, and impossible to miss.

## Standard disclaimer (base text — localize per jurisdiction, CH_39/01)
> Trading involves substantial risk of loss and is not suitable for every
> investor. Intraday trading is especially risky: most intraday traders lose
> money. Past performance — in backtests, paper trading, or live results — does
> not guarantee future results. This software is a decision-support tool; it is
> not financial, investment, or legal advice, and no promise of profit is made.
> Only trade with capital you can afford to lose, use the risk-management
> features, and consult a qualified professional before making financial
> decisions.

## Placement rules (enforced)
- README top (already present) and docs index.
- Before first live-trading enable (blocking confirmation).
- On every report/dashboard (banner, CH_40/00).
- In the app's "About/Legal" page and CLI setup output.

## What must always accompany any performance figure
- Period covered, costs included, engine type, data used (CH_18/03).
- A sentence that results may not be representative of future conditions.

## Pseudo-code: live enable gate
```
def enable_live(user):
    assert user.acknowledged(disclaimer_text)
    assert user.acknowledged(risk_basics)
    log("disclaimer_ack", user)
    # only then allow live mode config
```

## Rules
- Disclaimers are shown, not buried; consent is logged and auditable (CH_34/02).
- No version of the marketing/docs may promise returns.
- Keep a single source of truth for disclaimer text (CH_12 docs) so it never
  drifts.
