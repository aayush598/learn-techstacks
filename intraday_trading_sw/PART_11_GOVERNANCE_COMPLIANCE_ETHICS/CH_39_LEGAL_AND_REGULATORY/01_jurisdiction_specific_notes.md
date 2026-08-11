# 01 — Jurisdiction-Specific Notes

## Purpose
Provide a framework for assessing the rules that apply per jurisdiction, since
one codebase may serve users worldwide.

## Assessment dimensions
1. **User's residence**: where the person using the software lives.
2. **Broker's location/license**: where the executing broker is regulated.
3. **Instrument type**: stocks, futures, options, FX, crypto — each has distinct
   regimes (margin rules, CFDs, leverage caps, day-trading rules).
4. **Software's role**: decision-support (lighter touch) vs discretionary
   management (heavier, often needs licensing).

## Common obligations to check per jurisdiction
- **Day-trading minimums / pattern-day-trader** style rules (some markets).
- **Leverage/margin caps** on retail accounts.
- **Reporting/tax** on profits (user-level).
- **Data licensing** for redistribution.
- **Advertising/marketing** restrictions for anything financial.

## Template for a jurisdiction profile (docs/legal/<region>.md)
```
region: <Name>
residence_rules: summary + sources
broker_rules: summary + sources
instrument_notes: summary
software_role_note: decision-support framing
data_license_notes: redistribution constraints
disclaimer_text: required phrasing (CH_40/01)
```

## What the codebase should do
- Configurable leverage/notional caps per account (CH_20/CH_21) to honor local
  retail limits.
- Region-aware labels and disclaimer text at signup/docs.
- Never silently bypass broker-imposed limits.

## Rules
- The project ships templates and checklists, not legal opinions.
- Each deployment documents which jurisdiction profile(s) apply (in-repo).
- When in doubt, the conservative interpretation wins (fail-safe, CH_20/00).
