# 01 — Documentation and README

## Purpose
Ship documentation good enough that a stranger can build, run, and safely
evaluate the software — the real test of open-source quality.

## Required docs (in-repo)
- `README.md` — what it is, quick start, architecture map, disclaimers.
- `docs/getting-started.md` — environment setup (CH_31/00), doctor, first run.
- `docs/architecture.md` — system anatomy and data flow (CH_00, CH_01).
- `docs/usage.md` — configuration, manifests, dashboards, kill switch.
- `docs/backtesting.md` — how results are produced and how to read them (CH_18/03).
- `docs/risk-policy.md` — how to configure limits safely (CH_20).
- `docs/paper-trading.md` — how to validate before live (CH_37).
- `docs/legal/` — disclaimers, jurisdiction profiles (CH_39, CH_40).
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` (CH_42, CH_41).

## Doc quality rules
- Every doc links to the relevant chapters of this resource (CH references).
- Every config change is documented with an example (config files are code).
- Docs are versioned with releases (no doc/repo drift).

## Pseudo-code: quick-start doc checklist
```
- [ ] prereqs (OS, runtime) with exact versions
- [ ] clone + install + doctor steps
- [ ] load example data (or connect a feed)
- [ ] run in paper mode with a sample strategy
- [ ] view dashboard + a sample report
- [ ] how to configure risk limits
- [ ] how to report issues / security (CH_42)
```

## Rules
- No feature ships without its doc entry (definition of done, CH_00/01).
- Docs are reviewed in PRs like code (CH_42/01).
- The disclaimer banner lives in the README and docs index (CH_40/01).
