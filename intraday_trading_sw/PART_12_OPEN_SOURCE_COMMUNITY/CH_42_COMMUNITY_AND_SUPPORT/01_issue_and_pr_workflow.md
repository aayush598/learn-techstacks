# 01 — Issue and PR Workflow

## Purpose
Run a transparent, responsive issue/PR process that builds trust and improves
the software.

## Issue triage
- **Labels**: bug / security / enhancement / strategy / docs / question /
  incident-review.
- **Bug reports require**: version, logs, expected vs actual, whether paper or
  live mode, correlation id if available (CH_33/01).
- **Security reports**: private channel (SECURITY.md) — never public before fix
  (CH_41/02).
- **SLAs (community)**: triage within N days; security issues highest priority.

## PR workflow
- CI must pass (CH_41/02) before review.
- Two reviews for risk/execution code; one for docs.
- Review = reason about correctness + risk impact (CH_40), not style only.
- Merge types: squash for clean history; releases from tags (CH_41/02).

## Incident review issues
- Post-incident: a template issue/PR records what/when/why/fix/prevention
  (CH_33/02) — open process, no blame.

## Pseudo-code: triage loop
```
on issue:
    apply labels; route owner
    if security: private + priority
    if bug: request reproduction info (template)
    if strategy: request backtest + checklist (CH_42/00)
```

## Rules
- Every closed issue records its resolution (fix/duplicate/wontfix + reason).
- Maintainers respond within SLA; community help is welcomed and credited.
- Decisions about the project (roadmap, license, ethics) happen in the open.
