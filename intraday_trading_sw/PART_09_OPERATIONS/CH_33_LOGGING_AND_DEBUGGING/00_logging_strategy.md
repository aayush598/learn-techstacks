# 00 — Logging Strategy

## Purpose
Design logging that makes every decision reproducible and every incident
debuggable — structured, cheap, and complete where it matters.

## Logging principles
- **Structured**: one JSON per line (ts, level, module, event, fields). Grep-able,
  machine-readable, no parsing of prose.
- **Complete at the edges**: orders, fills, risk decisions, alerts, state changes
  are logged in full (audit-grade). Per-bar market data is NOT logged (volume).
- **Cheap in the core**: the hot loop (CH_27) logs async via a bounded queue —
  never blocks the signal path.
- **Levels**: DEBUG (dev), INFO (normal), WARN (anomaly, no action), ERROR
  (recoverable), CRITICAL (halt/breaker).

## Log events catalog (minimum)
- lifecycle: start/stop/restart of each service, with reason.
- data: validation rejects, gaps, backfills, feed reconnects (CH_06, CH_07).
- decision: every signal (with reasons), every risk approval/rejection (with rule
  names), every order event (CH_25/01), every fill.
- risk: limits hit, breakers, de-risking, halts (CH_20–CH_23).
- ops: health checks, deployments, model registry changes.

## Pseudo-code: structured log
```
log.info("order_placed", {oid, symbol, side, qty, type, ts, source, broker_id})
log.warn("risk_reject", {oid, reasons:[...], snapshot:{...}})
```

## Storage & rotation
- Local files, daily rotation + retention policy (e.g., 90 days live, longer
  for audit-grade order/risk logs) (CH_35 ties to backups).
- Optional: a searchable index for the journal (SQLite) — keep raw files too.

## Rules
- Never log secrets (mask credentials/tokens, CH_34/00).
- Log the same object once (no duplicated log lines from retries).
- A missing log line is itself a bug — traceability test in QA (CH_36).
