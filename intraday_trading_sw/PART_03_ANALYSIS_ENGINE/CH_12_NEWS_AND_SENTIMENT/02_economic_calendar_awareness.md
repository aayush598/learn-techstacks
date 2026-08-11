# 02 — Economic Calendar Awareness

## Purpose
Use scheduled events as first-class inputs: avoid dangerous illiquid moments,
pause around releases, and (optionally) trade the expected volatility.

## Calendar features per bar
- minutes_to_next_event (and its category/importance)
- is_high_impact_minutes (binary, e.g., within ±N min of a major release)
- event_spike_risk (expected vol multiplier from calendar metadata)
- today_has_expiry/rollover (F&O: expiry/roll affects price action and volume)

## Strategy-level effects (configurable per strategy)
- **Pause mode**: no new entries within ±X minutes of a high-impact event.
- **Reduce mode**: halve position size near events.
- **Widen mode**: widen stops (vol spike) or flatten before events.
Each strategy declares its policy; the risk layer enforces it (PART_06).

## Pseudo-code: event risk gate
```
def allow_entry(bar, calendar):
    d = minutes_to_next(bar.t, calendar)
    if d < pause_window and event.importance >= HIGH:
        return False, "high_impact_event"
    return True, None
```

## Calendar data (self-hosted)
- Curated YAML/CSV of known events: `{date, time, tz, region, symbol_tags,
  importance, actual_type}`.
- Versioned and auditable; sources documented (CH_05).
- Never guess event times; an error here can be costly.

## Rules
- Event awareness is data, delivered through features; decisions stay in strategy.
- Test behavior around events with replayed days that contain releases (CH_37).
- Pause/alter rules must be enforceable by the risk layer, not just convention.
