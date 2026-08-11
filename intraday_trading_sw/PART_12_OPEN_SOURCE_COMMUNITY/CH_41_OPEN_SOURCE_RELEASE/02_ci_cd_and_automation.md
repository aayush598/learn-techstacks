# 02 — CI/CD and Automation

## Purpose
Automate build, test, and release so quality gates (CH_36, CH_19) are enforced
mechanically and releases are reproducible.

## CI pipeline (on every PR/commit)
1. **Lint + format** (consistent style).
2. **Unit + integration tests** (CH_36/01).
3. **Benchmarks vs budget** (CH_38/00).
4. **Docs/license/content checks** (CH_40/02, CH_41/00).
5. **Package build** (runtime + scripts) — reproducible artifact.
6. **Replay/smoke test** on a fixed fixture day (CH_36/02).

## CD/release pipeline (on tag)
1. Run full CI.
2. Build release artifact + versioned docs.
3. Run acceptance smoke on staging (CH_36/02).
4. Tag release (semver); publish changelog.
5. Deploy to prod only via the approval gate (CH_31, CH_34/02).

## Pseudo-code: pipeline definition
```
on push/pr:
  jobs: lint, test, bench, docs-check, build
on tag v*:
  jobs: ci, staging-acceptance, release-tag, changelog
deploy_to_prod: manual_approve(audit) -> run migrations -> deploy -> healthcheck
```

## Rules
- Nothing merges to main without green CI (no exceptions).
- Release artifacts are immutable and reproducible from the tag.
- Every prod deploy is logged in the audit log (CH_34/02) with before/after
  versions and rollback info (CH_35).
- CI runs the project's own tools (self-hosted runner or plain CI) — no
  proprietary dependency in the core path (CH_00/02).
