# 01 — Containerization and Services

## Purpose
Package the system into small, reproducible services so it is easy to deploy,
update, and run long-term.

## Service layout (single host, MVP)
| Service | Responsibility |
|---|---|
| `ingest` | feeds → validated bars (CH_06) |
| `engine` | strategies/decisions/risk (CH_28) |
| `oms` | order lifecycle (CH_25) |
| `ui` | dashboard/charts (CH_29) |
| `monitor` | metrics/health/alerts (CH_32) |
| `notify` | alert delivery (CH_30/01) |
| `research` | offline backtest/training (on-demand, not always running) |

## Packaging options (dependency-minimized)
- **Option A (default)**: plain OS services (systemd units) — no containers
  needed; simplest to audit and debug.
- **Option B**: containers (image per service) for reproducibility — only if the
  ops complexity is justified.
Rule: choose A for MVP; B only when moving hosts or teams demands it.

## Container approach (if used)
- Small base images; runtime image built from pinned runtime.
- Config injected via env/config files; volumes for `data/` and `logs/`.
- Healthchecks per service (CH_32/01).
- Images built by CI (CH_12/CH_41) from the tagged repo.

## Pseudo-code: compose of services (concept)
```
services:
  ingest:  { run: ingest,  depends: [db] }
  engine:  { run: engine,  depends: [ingest] }
  oms:     { run: oms,     depends: [engine] }
  ui:      { run: ui,      depends: [engine, oms] }
```

## Rules
- One process per responsibility; the engine and OMS are the only ones touching
  live orders (single writer, CH_28/01).
- Service restarts must not lose journal data (CH_28/02).
- Version tags on images/artifacts tie to git (CH_12/CH_41).
