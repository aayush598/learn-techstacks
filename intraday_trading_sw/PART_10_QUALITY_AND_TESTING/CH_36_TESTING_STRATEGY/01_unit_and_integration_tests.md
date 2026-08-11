# 01 — Unit and Integration Tests

## Purpose
Define the concrete unit and integration test suites that give confidence in
every module before it meets the live system.

## Unit test essentials
- **Indicators**: RSI/EMA/MACD/ATR/ADX/BB vs hand-computed tables; warmup NaN
  policy; batch == incremental equivalence (CH_10/00).
- **Features**: formulas exact; session bucket behavior; no-future leak per
  feature (CH_09).
- **Rules/evaluator**: every manifest construct; precedence; invalid manifest
  rejection (CH_14/00).
- **Risk**: per-trade/portfolio/daily limits with boundary values (exactly at
  limit = reject), breaker triggers (CH_20–CH_23).
- **OMS state machine**: exhaustive legal transitions + illegal ones raise/halt
  (CH_25/01).
- **Sizing**: fixed-fractional, ATR, drawdown de-risking, fractional Kelly caps
  (CH_21).
- **Cost/fill model**: spread+slippage math, asymmetric stop fills (CH_17/02).

## Integration test essentials
- Data → store round-trip: write→read→identical (CH_08).
- Ingest → validate → feature → signal on a replayed day (CH_06, CH_09, CH_14).
- Strategy → risk gate → OMS → simulator fills → positions/P&L (CH_24/00).
- Reconciliation: induced OMS/broker mismatch is detected and adopted (CH_25/02).
- Calendar/event gates: paused windows honored (CH_12/02).
- Secrets redaction: logs never contain credential substrings (CH_34/00).

## Pseudo-code: integration scenario
```
def test_full_day_replay():
    bars = load_replay_day("2026-03-04")           # fixture
    engine = Engine(simulator_broker())            # CH_24/00
    for bar in bars: engine.on_bar(bar)
    assert engine.daily_pnl == expected_pnl
    assert positions_flat_by_close()
```

## Rules
- Every test is deterministic (fixed seeds/fixtures, no network in unit tests).
- The simulator broker is used for integration — never a real account.
- New bug = new failing test first (regression discipline), then fix.
