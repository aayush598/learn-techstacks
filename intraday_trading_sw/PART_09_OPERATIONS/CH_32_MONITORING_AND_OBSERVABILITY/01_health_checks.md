# 01 — Health Checks

## Purpose
Define explicit, executable checks that prove each service is alive, up to
date, and able to trade safely.

## Per-service health checks
| Service | Check |
|---|---|
| ingest | receiving bars within X s for subscribed symbols; no sustained gaps |
| engine | processing bars within budget; watchdog heartbeat fresh (CH_31/02) |
| oms | order callbacks flowing; reconciliation clean; no UNKNOWN orders |
| ui | serving snapshots; websocket clients connected |
| monitor | itself collecting and flushing metrics |
| broker adapter | connected, authenticated, subscriptions active (CH_24) |

## Check protocol
- **Liveness**: process alive + watchdog reset.
- **Readiness**: dependencies reachable (db, feed, broker).
- **Depth**: functional probes — e.g., place a simulator order and verify state
  transitions (paper mode only), ping feed, check calendar is today's.

## Pseudo-code: health endpoint
```
def health(svc):
    checks = [alive(svc), ready(svc), depth(svc)]
    return { svc: svc, status: all_ok, details: [c.name: c.ok] }
```
`/health` per service; `monitor` aggregates into one status board (CH_29/00).

## Behavior
- Liveness failure → process manager restart (CH_31/02).
- Readiness/depth failure → alert + risk halt for affected symbols (CH_30/00).
- All checks run on a short interval during market hours; lighter after hours.

## Rules
- Health checks are part of the deploy gate: a service with failed checks is
  not "up" even if the process runs.
- Health results feed dashboards and alerting (CH_29, CH_30) automatically.
- Depth probes never place real orders (simulator only) — enforced by config.
