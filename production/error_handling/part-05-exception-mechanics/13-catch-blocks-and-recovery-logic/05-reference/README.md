# Chapter 13 — Reference

> Part V · Chapter 13 · Cheat sheet, decision tree, and chapter glossary.

## Catch-vs-propagate decision tree

```text
error reaches this frame
  │
  ├─ Can I complete the operation safely via recovery?  ──yes─▶ CATCH + recover
  │
  ├─ Am I at a boundary that maps to a contract?         ──yes─▶ CATCH + translate
  │
  ├─ Can I add meaningful context only?                  ──yes─▶ WRAP + rethrow
  │
  ├─ Do I only need to release a resource?                        USE finally/defer/using
  │
  └─ Otherwise                                       ──▶      PROPAGATE (no catch)
```

## Recovery decision tree (inside a catch)

```text
caught error
  │
  ├─ transient? ─no─▶ permanent
  │                  ├─ at boundary? ─▶ translate (domain result / status)
  │                  └─ else         ─▶ rethrow
  │
  └─ yes
      ├─ idempotent (or keyed)? ─no─▶ do NOT retry; translate "outcome unknown"
      ├─ resource alive & state consistent? ─no─▶ reset/rollback; if impossible → terminate
      ├─ budget left (attempts & deadline)? ─no─▶ rethrow final error
      └─ all yes ─▶ recover; on failure attach as suppressed, rethrow primary
```

## Cheat sheet — specific-first catch order

```text
NotFound → Conflict → Transient → Invalid → Auth → Unknown(log+rethrow) → (bare: ❌)
```

## Cheat sheet — the five catch defects

| Defect | Signature | Fix |
| ------ | --------- | --- |
| Empty catch | `catch {}` | Delete or justify harmlessness + log |
| Broad suppression | `catch (Exception)` | Specific types + rethrowing unknown |
| Repeated catch/rethrow | log+throw per layer | Wrap; log once at boundary |
| Recovery error overwrites | recovery throws over primary | Wrap recovery; attach suppressed |
| Recursive recovery | retry calls itself | Bounded loop with deadline |

## Cheat sheet — preserving the primary

| Language | Attach secondary |
| -------- | ---------------- |
| Java | `primary.addSuppressed(secondary)` |
| Go | `errors.Join(primary, secondary)` |
| Python | implicit `__context__` / explicit `from` |
| TypeScript | explicit `suppressed` field on the error |

## Decision table — recovery outcome

| Condition | Outcome |
| --------- | ------- |
| Alternative path completes the op | Full recovery → success |
| One step redone/undone, op still fails | Partial recovery → rethrow |
| Recovered enough to classify | Translate → domain result |
| State unknown/untrusted | Terminate → fail-fast, alert |
| Non-idempotent + ambiguous remote outcome | Translate "outcome unknown", reconcile |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Recovery | Completing the operation after a failure |
| Partial recovery | Some work redone/undone; operation still failed |
| Precondition | A condition that must hold for recovery to be safe |
| Idempotency | Re-running has the same effect as once |
| Suppressed error | A secondary failure attached to the primary |
| Discrimination | Telling error kinds apart inside a catch |
| Category | A group of errors sharing a policy |
| Unknown branch | Handler for unmodeled errors; logs + rethrows |
| Recursive recovery | Retry that re-enters the failing call unbounded |
| Termination | Aborting because state cannot be trusted |

## Signposts

- Propagation mechanics → [Ch. 12](../../12-exception-propagation-and-control-flow/README.md)
- Cleanup on failure → [Ch. 14](../../14-resource-cleanup-and-failure-safe-execution/README.md)
- Boundaries → [Ch. 15 Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- Retry ownership → [Ch. 27 Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)

## Related

- [Chapter 13 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 13 README](../README.md)
- [Part V Index](../../README.md)
