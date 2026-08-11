# 01 — Validation and Quality Checks

## Purpose
Automatically reject corrupt or suspicious data before it enters the store,
because garbage data silently poisons every downstream result.

## Validation suite (run on every batch/bar)
- **Schema**: required fields present, types correct (CH_07/00).
- **Range sanity**: price > 0, volume ≥ 0, finite numbers.
- **OHLC consistency**: low ≤ open ≤ high, low ≤ close ≤ high, low ≤ high.
- **Timestamps**: monotonic, aligned to period, within session, no duplicates.
- **Gap detector**: expected next ts; flag missing intervals (CH_06/02).
- **Cross-source spot check** (if available): compare recent closes vs second
  source within tolerance; mismatch → escalate.
- **Unusual data** (not necessarily error): extreme returns, zero-volume bars,
  price jumps > N×ATR — flag for review rather than auto-fix.

## Quality actions
| Check result | Action |
|---|---|
| Pass | accept into store |
| Fixable (e.g., ordering, duplicates) | fix deterministically, log |
| Non-fixable | reject + log; mark gap; never invent values |
| Suspicious | flag, quarantine for manual review |

## Pseudo-code: validation gate
```
def validate_bar(b):
    checks = [schema(b), ranges(b), ohlc_ok(b), ts_ok(b), dup_ok(b)]
    return all(c.pass for c in checks)   # log each failing check
```

## Quality metrics (monitor in CH_32)
- % bars passing, gap count, duplicate count, fixable-error count,
  cross-source mismatch count per source/day.

## Rules
- Rejection is the default; acceptance must be earned by passing all checks.
- Record every rejected/fixed record with reason (audit + tuning of checks).
- Never let the live engine consume unvalidated bars.
