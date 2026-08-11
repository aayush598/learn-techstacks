# 02 — Dependency Minimization Philosophy

## Purpose
Explain the core principle that the system should be as self-contained and
self-hosted as possible, and how to achieve that without reinventing wheels
foolishly.

## Why minimize dependencies
- **Trust**: users can audit everything; no hidden third-party black boxes.
- **Portability**: runs anywhere (own server, VPS, even laptop) with few moving parts.
- **Resilience**: no vendor outage or API change can break the core system.
- **Security**: fewer packages = smaller attack surface.
- **Cost**: open-source + self-hosted = low operating cost.
- **Longevity**: core survives even if a dependency dies.

## What we still allow
- The **operating system** and its package manager.
- A **runtime** (e.g., a standard Python install — stdlib only for core).
- **Broker/exchange connectivity** is inherently external (you cannot self-host a
  broker); it is isolated behind one abstraction layer (CH_24).
- **Market data** must come from somewhere; preference for open/free sources,
  but stored locally forever once acquired.

## Implementation strategy
1. **Stdlib-first**: implement indicators, patterns, CSV/JSON handling, simple
   HTTP, WebSocket client, basic math/statistics with standard libraries.
2. **Write your own small libraries** where logic is simple and must be trusted:
   - `indicators.py` — MA, EMA, RSI, MACD, ATR, Bollinger, VWAP (CH_10)
   - `features.py` — returns, volatility, session features (CH_09)
   - `metrics.py` — sharpe, sortino, drawdown, expectancy (CH_18)
   - `risk.py` — sizing, limits, circuit breakers (PART_06)
   - `stats.py` — t-test, bootstrap, correlation (CH_18/CH_19)
3. **Optional, pluggable, strictly-isolated extras** (documented trade-offs):
   - An ML library (e.g., scikit-learn/lightgbm) only behind the model layer
     interface (CH_15), never leaking into other modules.
   - A numeric/array library only in the math layer, abstracted by functions.
   - A plotting library only in the UI module.
4. **Pin and audit**: when a third-party package is used, pin versions, document
   why, and keep its interface wrapped so it can be replaced.

## Decision table
| Need | Default choice | Alternative |
|---|---|---|
| CSV/JSON | stdlib `csv`/`json` | — |
| Arithmetic/stats | stdlib `math`/`statistics` | array lib (wrapped) |
| HTTP | stdlib `urllib`/`http` | own tiny client |
| WebSocket | stdlib `socket` hand-rolled or minimal lib | — |
| Storage | SQLite + Parquet (self-hosted) | own columnar writer |
| ML | hand-built trees/logreg first | wrapped ML lib |
| Scheduling | stdlib `sched`/OS cron | own scheduler |
| Charts | canvas/simple SVG renderer | wrapped plotting lib |

## Rules
- A dependency must justify its cost; if stdlib works, use stdlib.
- Every external dependency is isolated behind an interface and swappable.
- The system must be buildable and runnable from this repo + OS + runtime alone.
