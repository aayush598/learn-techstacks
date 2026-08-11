# 00 — Test Pyramid

## Purpose
Structure testing so bugs are caught at the cheapest level first, and the live
trading path is covered end-to-end before it ever touches real money.

## Pyramid layers
1. **Unit tests** (many): math, indicators, features, rules, risk gates, state
   machine — pure logic, fast, deterministic.
2. **Integration tests**: module boundaries (data→features→signal→risk→OMS),
   storage round-trips, adapter vs simulator (CH_24/00).
3. **System/acceptance tests** (few): full pipeline on synthetic or replayed
   data (CH_37), end-to-end decision→order→fill→P&L.
4. **Drills**: recovery, breaker, reconnect (CH_32, CH_35) — scheduled, not just
   coded.

## Coverage priorities (what MUST be tested)
- Indicator correctness vs hand-computed values (CH_10/00).
- No-look-ahead canary (CH_17/03).
- Order state machine: all transitions (CH_25/01).
- Risk gates: limits enforced even with malicious input (CH_20).
- Determinism: same input → same output everywhere (CH_28).
- Secrets redaction in logs (CH_34/00).

## Pseudo-code: test runner concept
```
pytest-like:
  test_math/indicators/features/rules/risk/oms/...
  test_pipeline_e2e_replay...
  coverage gate: hot modules >= 90%
```

## Rules
- A feature is done only when its tests exist and pass (definition of done,
  CH_00/01).
- Tests run in CI before any deploy (CH_12/CH_41) — no skipping.
- Failing tests block deployment to staging and prod.
