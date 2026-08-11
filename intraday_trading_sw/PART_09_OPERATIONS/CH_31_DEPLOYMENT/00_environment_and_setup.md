# 00 — Environment and Setup

## Purpose
Define a reproducible, boring, documented environment so the system runs the
same everywhere and anyone can audit the setup.

## Environment blueprint
- **OS**: a mainstream stable Linux distribution (documented version).
- **Runtime**: the chosen runtime (e.g., a Python version) — pinned exactly.
- **Repo**: the open-source codebase (CH_12) with pinned dependencies
  (CH_00/02 philosophy: mostly stdlib).
- **Config**: all settings via config files (YAML/JSON) + env-injected secrets
  (CH_34/00) — nothing hardcoded.
- **Data layout**: as defined in CH_08/00.

## Setup automation
- A single `setup.sh` / `install` script: install OS packages, create user,
  directories, permissions, cron/systemd units (CH_31/02), and a
  `doctor` command that verifies the environment (network, disk, clock, ports).
- `doctor` checks: time sync (NTP), broker reachability, disk space, read/write
  on data dirs, runtime version match, config validity.

## Pseudo-code: doctor checks
```
doctor():
    check(ntp_synced())
    check(runtime_version == PINNED)
    check(can_write(data_dir))
    check(disk_free > min_gb)
    check(broker_endpoint_reachable(timeout=2s))
    check(config_valid(config))
    report all results (pass/warn/fail)
```

## Environments
- **dev** (local): simulator broker (CH_24/00), small symbol set.
- **staging**: broker sandbox/paper, full symbol set, full monitoring.
- **prod**: live, gated by QA/paper sign-off (CH_37).

## Rules
- The repo builds and runs from a clean OS following only the documented steps.
- Environment differences are configuration, never code.
- `doctor` runs before any live start and reports to logs (CH_32).
