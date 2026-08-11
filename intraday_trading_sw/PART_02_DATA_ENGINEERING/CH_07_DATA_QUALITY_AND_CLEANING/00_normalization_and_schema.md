# 00 — Normalization and Schema

## Purpose
Define one canonical schema and one set of normalization rules so every module
reads identical, consistent data regardless of source.

## Canonical bar schema (single source of truth)
| Field | Type | Meaning |
|---|---|---|
| symbol | str | canonical symbol id |
| ts | int64 | bar start time, UTC, microseconds |
| interval | str | "1m", "5m", "D", … |
| open/high/low/close | float | prices (normalized currency unit) |
| volume | float/int | traded volume |
| trades | int | trade count (optional) |
| vwap | float | volume-weighted price (optional) |
| source | str | source id (lineage) |
| quality | str | ok / gap / corrected / estimated |
| ingest_ts | int64 | when ingested (audit) |

## Normalization rules
- All timestamps → UTC micro-since-epoch; local session time derived at display.
- Prices → one canonical unit (e.g., instrument's own units; never mix).
- Symbol names → canonical mapping table (aliases resolved once at ingest).
- Volume → native lots unless a documented multiplier applies.
- Strings lowercased, whitespace trimmed, enums validated.

## Canonical tick/quote schema
- trade: `ts, symbol, price, size, side(+1/-1/0), seq, source`
- quote: `ts, symbol, bid, bid_size, ask, ask_size, seq, source`

## Schema enforcement
- A single `schema.py`-style validator owns field types and constraints.
- Every writer must pass data through the validator; invalid records are
  rejected with a logged reason (never silently coerced).

## Pseudo-code: normalizer
```
def to_canonical_bar(raw, source):
    row = {}
    row.symbol  = canonical_symbol(raw.symbol)
    row.ts      = to_utc_micros(raw.time, source.tz)
    row.open    = float(raw.open); ... (high, low, close, volume)
    row.interval = raw.interval.lower()
    row.source  = source.id; row.quality = "ok"; row.ingest_ts = now_micros()
    validate(row)             # raises/records if out of bounds
    return row
```

## Rules
- Exactly one canonical schema; adapters do the translating.
- Schema changes are migrations with version numbers, never silent.
