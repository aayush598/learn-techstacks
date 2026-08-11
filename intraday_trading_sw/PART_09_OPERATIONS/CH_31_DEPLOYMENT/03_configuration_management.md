# 03 — Configuration Management

## Purpose
Define how the system's configuration is structured, validated, versioned, and
released — so every environment (research, paper, live) is reproducible and
secrets never leak (CH_31/00, CH_34).

## Config sources (layered, explicit precedence)
1. **Defaults** (baked into code).
2. **Environment-specific files** (`config/live.yaml`, `config/paper.yaml`).
3. **Environment variables / secrets** (API keys, tokens — never in files).
4. **Override layer** (rare, e.g., a documented maintenance flag).

## What belongs in config
- Strategy manifests (CH_13/00), risk policy (CH_20/01), sources catalog
  (CH_05/02), alert rules (CH_30/00), calendar artifact (CH_02/03).
- Session schedule, universe snapshot id, symbol mappings, timezone/UTC.

## What never belongs in config
- Secrets (API keys, DB passwords) — secrets live in a secret manager
  (CH_34/00) and are injected at runtime (CH_31/00).

## Requirements
- **Schema-validated**: every config file validates on load (JSON Schema or
  equivalent); an invalid config fails fast with a clear message.
- **Versioned**: configs live in the same repo/versioning as code; every
  run/backtest records the config hash for reproducibility (CH_16/01).
- **No silent fallbacks**: missing values error loudly; never auto-pick a
  "safer" default that changes behavior (CH_19/01).
- **Atomic & audited**: config changes are reviewable (PR/diff) and rollback is
  a revert of the file, not a manual tweak.

## Pseudo-code: config load
```
def load_config(env):
    base = parse(env + ".yaml")          # fails on missing/invalid schema
    merged = defaults.deep_merge(base)
    merged.override_from_env("TRADING__RISK__MAX_POSITION")  # explicit keys
    assert validate_schema(merged)
    record_config_hash(merged)           # attach to run/backtest (CH_16/01)
    return merged
```

## Rules
- One source of truth: derived values are computed, not duplicated in multiple
  configs (CH_20/01 owns risk limits).
- Config changes that alter behavior require a full backtest, not just a
  restart (CH_17, CH_37).
- Runtime hot-reload only for safe flags (alerts, logging); risk and strategy
  config require a restart after validation (CH_28/00).
