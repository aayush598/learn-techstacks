# 00 — Contribution Guidelines

## Purpose
Define how others can contribute safely and consistently to a financial
open-source project.

## Contribution types
- Code (features, fixes, tests).
- Strategies (manifests + backtests — must include honest results, CH_19).
- Docs, translations, disclaimers review.
- Data-source adapters (with documented licensing, CH_05).
- Bug reports and incident reviews (CH_33).

## Contribution rules
1. **Create an issue first** for any non-trivial change (discuss before build).
2. **Fork → branch → PR** with a clear description and test evidence.
3. **Follow the test discipline**: new logic ships with tests (CH_36).
4. **No strategy claims**: a PR adding a strategy must include its full backtest
   report with costs (CH_18/03) and pass the overfitting checklist (CH_19/03).
5. **No guaranteed-profit content** — rejected by policy (CH_40/02).
6. **DCO / sign-off**: contributors certify their contribution (license
   compliance, CH_41/00).

## Review checklist (maintainers)
```
- [ ] tests included and passing
- [ ] docs updated
- [ ] no secrets/deps introduced casually (CH_34, CH_00/02)
- [ ] risk/ethics reviewed (CH_40)
- [ ] data licensing documented if new sources (CH_05)
```

## Pseudo-code: strategy PR template
```
Strategy: <name>
Manifest: link
Backtest: report link (costs included, CH_18/03)
Overfitting checklist: link (CH_19/03)
Paper results: link (CH_37/01)
```

## Rules
- Contributing is code review, not just merge — quality gates are mandatory.
- Maintainers have the final word on risk/ethics-sensitive changes.
- A Code of Conduct is adopted and enforced (community health, CH_42/02).
