# 00 — Responsible Financial Software

## Purpose
Articulate the ethical design principles that keep the software honest,
non-exploitative, and safe for the people who trust it.

## Ethical commitments
1. **No profit promises**: the software never claims, implies, or sells the idea
   that it guarantees earnings. (Enforced in docs/UI, CH_40/01–02.)
2. **Honest uncertainty**: every prediction carries probability/confidence and a
   clear statement that markets are uncertain (CH_00/02).
3. **No dark patterns**: no "act now" pressure, no deceptive backtest charts,
   no hiding losses in dashboards (CH_18/03, CH_29).
4. **Fail-safe by default**: on doubt, the system does less, not more (CH_20/00).
5. **No manipulation**: hard-refuse features for spoofing, layering, wash
   trading, cornering, or misleading others (CH_39/00). These are illegal and
   destroy markets and users.
6. **Protection over profit**: risk limits are un-removable by design
   (CH_23/02) even if a user asks for more leverage than is safe.

## Software-level enforcement (examples)
- A "backtest is not a promise" banner on every report/dashboard.
- Probability outputs always shown with calibration/uncertainty.
- Daily/risk limits configurable *within* safe bounds enforced by policy caps.
- Explicit confirmation before enabling live trading, linking to CH_40 docs.

## Pseudo-code: honesty guardrails
```
def present_result(r):
    r.banner = "Past results do not guarantee future outcomes"
    assert r.has_costs; assert r.has_period; assert r.has_assumptions
```

## Rules
- Ethics are enforced in code and docs, not just written down.
- If a feature increases risk without a compensating safety control, it ships
  disabled or not at all.
- Review prompts: "would this harm a typical user?" — block if yes.
