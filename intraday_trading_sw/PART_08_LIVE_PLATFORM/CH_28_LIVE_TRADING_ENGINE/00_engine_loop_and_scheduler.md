# 00 — Engine Loop and Scheduler

## Purpose
Define the live engine: a deterministic, wall-clock-driven loop that consumes
bars, produces decisions, and submits approved orders — the heartbeat of the
platform.

## Engine phases per session
1. **Pre-market**: connect, authenticate (CH_24/01), load state, reconcile
   (CH_25/02), warm features/indicators, load strategy manifests.
2. **Trading**: the main loop below.
3. **Post-close**: flatten check, EOD report (CH_18/03), nightly jobs, disconnect.

## Main loop (pseudo)
```
while in_session(now()):
    bar = next_validated_bar()                  # from ingestion (CH_06/01)
    if bar is None: handle_missed_bar(bar_ts); continue
    ctx = engine_context(bar)                   # features, indicators, state, calendar
    decisions = [s.decide(ctx) for s in selected_strategies(ctx)]   # CH_14/03
    for d in decisions:
        if risk_gate.approve(d):                # CH_20 (hard gate)
            oms.submit(d.order)                 # CH_25
    manage_open_positions(ctx)                  # exits/trails (CH_14/02)
    publish_ui_updates(ctx)
    metrics.observe(bar_ts, now())
```

## Scheduling (time-aware)
- Bar cadence derived from the calendar (session map, CH_02/02).
- Scheduled jobs: reconcile (periodic), trail refresh, EOD flatten
  (minutes-before-close), report generation — via a simple scheduler.
- All scheduling uses the same wall clock as the calendar (NTP-synced, CH_27/02).

## Pseudo-code: missed bar handling
```
def handle_missed_bar(ts):
    gap = detect_gap(ts)
    metrics.gaps += 1
    if gap and risk_policy.halt_on_data_gap: risk.halt_strategies(symbol)
    schedule_backfill(ts)                       # CH_06/02
```

## Rules
- The engine is the only writer of strategy state (single owner).
- Engine decisions are synchronous with the current bar — no stale decisions.
- On any exception in the loop: log, alert, and go fail-safe (halt/flatten per
  CH_23/00), never skip silently.
