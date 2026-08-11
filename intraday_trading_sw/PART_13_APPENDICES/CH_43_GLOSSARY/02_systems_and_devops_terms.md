# 02 — Systems and DevOps Terms Glossary

## Purpose
Define the engineering and operations terminology used across Parts 07–10.

## Architecture
- **Pipeline**: stages processing data/decisions in sequence.
- **Ingestion**: bringing data into the system.
- **Backfill**: fetching missed data to fill gaps.
- **Columnar storage**: data stored by column for fast scans (CH_08/01).
- **Journal**: append-only record of events (CH_25, CH_28).
- **Reconciliation**: aligning our records with the broker's (CH_25/02).
- **Single writer**: one owner for state, avoiding races (CH_28/01).

## Orders & execution
- **OMS**: order management system (CH_25).
- **Order state machine**: legal states/transitions of an order (CH_25/01).
- **Fill model**: how executions are simulated (CH_17/02).
- **TWAP/VWAP slicing**: splitting orders over time/volume (CH_26/01).
- **Kill switch**: immediate flatten-all control (CH_23/02).

## Reliability & ops
- **Liveness/readiness**: is the process alive / ready to serve (CH_32/01).
- **Watchdog**: heartbeat monitored by the process manager (CH_31/02).
- **Circuit breaker**: auto-halt on abnormal conditions (CH_23/00).
- **Incident**: an unplanned event needing review (CH_33/02).
- **Drift**: deviation of behavior from baseline (models or data, CH_16/03).
- **Replay**: re-running decisions on stored data (CH_33/01).
- **Fail-safe**: default to safe behavior on uncertainty (CH_20/00).

## Testing & quality
- **Unit test**: tests one function/module (CH_36/01).
- **Integration test**: tests module boundaries (CH_36/01).
- **Acceptance test**: proves product-level criteria (CH_36/02).
- **Paper trading / dry run**: simulated execution (CH_37).
- **Benchmark**: measured performance of an operation (CH_38/00).
- **Determinism**: same input → same output (CH_28).

## Security & compliance
- **Secrets**: credentials/tokens (CH_34/00).
- **Least privilege**: minimal access per role (CH_34/02).
- **Audit log**: append-only record of privileged actions (CH_34/02).
- **Disclosure**: the risk/legal statements (CH_40/01).
