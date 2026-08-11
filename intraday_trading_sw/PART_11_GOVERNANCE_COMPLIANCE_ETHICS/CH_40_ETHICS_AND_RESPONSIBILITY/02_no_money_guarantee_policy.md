# 02 — No-Money-Guarantee Policy

## Purpose
Make it legally and ethically impossible to read this project as a guarantee of
earnings — the single most important trust guard for a financial tool.

## Policy statements (adopted by the project)
1. **No guarantees, express or implied**: the software, its authors, and
   contributors do not guarantee profit, income, or any financial outcome.
2. **Results vary**: markets are unpredictable; strategies can and do lose money
   even after rigorous validation.
3. **User responsibility**: users decide how (and whether) to use the software
   and bear full responsibility for their trades and their compliance (CH_39).
4. **No performance promises in marketing**: no testimonial or screenshot may
   imply future earnings.
5. **Backtest ≠ future**: any historical performance is presented with its
   assumptions and disclaimers (CH_40/01).

## Enforcement in the codebase
- `docs/policy/no-money-guarantee.md` exists (single source).
- Dashboard/reports include the banner (CH_40/00).
- Live-enable gate requires acknowledgment (CH_40/01).
- CI check: marketing/docs pages must contain the disclaimer (CH_12/CH_41).

## Pseudo-code: CI content check
```
def check_docs():
    for page in [readme, index, dashboard_about, signup]:
        assert disclaimer in page
    assert "guarantee" not in any_implied_profit_phrase(page)
```

## Rules
- Any contributor adding content that implies guaranteed returns → rejected by
  the content policy (CH_42/00).
- The policy applies to the project itself, forks, and derived works.
- If a user asks "will this make me money?", the honest answer is always:
  it might lose money; no one can guarantee trading profits.
