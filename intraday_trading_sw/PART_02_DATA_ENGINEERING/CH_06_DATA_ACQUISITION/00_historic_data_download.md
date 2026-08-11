# 00 — Historic Data Download

## Purpose
Acquire long, clean history for backtesting and model training, in a scriptable,
auditable, resumeable way.

## Download jobs (design)
- A download job = (source, symbols[], timeframe, date range).
- Jobs are defined in a manifest (yaml) and executed by a CLI tool.
- Each job produces versioned raw files; nothing is written directly into the
  main store until validated (CH_07).

## Steps
1. Parse job manifest → split into per-symbol tasks.
2. For each symbol: discover available range; fetch in date windows
   (respecting source pagination/limits).
3. Apply source-specific normalization (timezone, symbol case, field names).
4. Write raw frames to `raw/<source>/<symbol>/...` (partitioned by year).
5. Run validation suite (CH_07); write only passing batches to the store.
6. Record job metadata: source, version, start/end, rows, validation result.

## Rate-limit client (pseudo)
```
class RateLimiter:
    def acquire(self):
        if now() < next_slot: sleep(next_slot - now())
        next_slot = now() + period/capacity
        # token bucket: capacity tokens per period, refill
```

## Resumeability
- Store per-symbol "last fetched until" checkpoint in a small sqlite table.
- On restart, continue from checkpoint (do not refetch everything).

## Rules
- Always store raw data exactly as received (auditability) *in addition to*
  cleaned copies.
- Never let a fetch crash mid-write corrupt a file: write temp then atomic rename.
- Prefer one-time bulk downloads stored forever over repeated re-downloading.
