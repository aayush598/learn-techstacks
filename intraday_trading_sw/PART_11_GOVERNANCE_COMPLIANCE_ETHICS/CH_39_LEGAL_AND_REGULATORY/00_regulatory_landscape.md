# 00 — Regulatory Landscape

## Purpose
Make developers aware that automated trading and financial software are
regulated in most jurisdictions, and that compliance obligations depend on
where the software and its users are.

## Key regulatory themes (informational, not legal advice)
- **Brokerage/execution**: routing live orders usually requires the user to hold
  an account with a licensed broker; the software operates *on top of* that
  account.
- **Investment advice**: "advice" is heavily regulated; label the product as a
  *decision-support tool*, never as advice (CH_40).
- **Robo-advisory / investment management**: discretionary, unsupervised
  auto-trading on behalf of others may constitute regulated activity.
- **Market abuse**: manipulative behavior (spoofing, layering, wash trading,
  pump-and-dump) is illegal everywhere. The software must actively refuse it
  (CH_40/00).
- **Algorithmic trading rules**: some regulators impose testing, kill-switch,
  and notification obligations on algo traders (kill switch: CH_23/02).

## What this means for the open-source project
- The software is a **tool**; each *user* is responsible for their own compliance
  in their own jurisdiction.
- The project must provide documentation and disclaimers (CH_40/01) and must
  never include features that could facilitate market abuse.
- Redistribution of market data has its own license constraints (CH_05, CH_12).

## Pseudo-code: compliance posture
```
product = "decision_support_tool"     # not advice, not robo-advisor
requires = { broker_account: true }   # execution through licensed venues
prohibited = [spoofing, wash_trading, market_manipulation]   # enforced (CH_40)
```

## Rules
- The repo ships with a compliance section (this part) and disclaimers — but
  legal counsel per jurisdiction is each user's responsibility.
- Never design features whose primary purpose could be market manipulation.
- Keep data licenses and attribution files current (CH_12).
