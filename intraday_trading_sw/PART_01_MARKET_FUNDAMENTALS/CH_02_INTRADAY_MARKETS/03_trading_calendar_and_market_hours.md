# 03 — Trading Calendar and Market Hours

## Purpose
Own the trading calendar as first-class data: session hours, holidays,
half-days, and early closes — used by ingestion, backtesting, features, and the
live engine so nothing misaligns with real market structure.

## What the calendar must contain (per market)
- Session open/close times (local tz + UTC) per weekday.
- Holiday and half-day dates (with special hours), including days when the
  session doesn't occur (e.g., bank holidays).
- Early/late session variants (e.g., half-day close at 13:00).
- Expiry days and roll-over days for derivatives (CH_03/03, CH_07/04).
- Daylight-saving transitions affecting session offsets.

## How the calendar is used
- **Ingestion**: bars must align to actual sessions; never fabricate a session
  on a holiday (CH_04/00, CH_06).
- **Features**: session phase (CH_02/02) and time features depend on the real
  session bounds (CH_09/03).
- **Backtest**: exclude non-session days; simulate half-day behavior; avoid
  look-ahead across holidays (CH_17/03, CH_19/00).
- **Live engine**: scheduling, flatten-before-close, and pre-market routine all
  read the calendar (CH_28/00).
- **Reporting**: per-session metrics group by the real session id (CH_18/03).

## Data model (calendar record)
```
{ market, date, is_open, session_start_utc, session_end_utc,
  early_close: bool, special_note, source, version }
```

## Steps to integrate
1. Source the calendar (exchange/broker calendar feed, or a curated, versioned
   file — CH_05). Never hardcode dates in code.
2. Validate: every date the exchange is open must be present (spot-check
   against a second source or historical volume).
3. Derive session ids and store with every bar.
4. Backtest/live both load the *same* calendar artifact (reproducibility).

## Pseudo-code: session lookup
```
def session_for(date, market, calendar):
    if not calendar.is_open(date): return None
    return {start: calendar.start(date), end: calendar.end(date)}
```

## Rules
- The calendar is data, versioned and auditable like any dataset (CH_08).
- Bars never cross a session boundary (CH_04/00) — the calendar enforces this.
- A wrong calendar (missing holiday) silently poisons backtests — validate it
  and monitor calendar freshness (CH_32).
