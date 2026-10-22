# Chapter 45 — Do / Don't

> Part XVII · Chapter 45 · all sections · _Estimated reading time: 6 min_

The consolidated rules for organizing error-handling modules. Use the tables as a PR checklist;
the review questions at the bottom are the ones worth arguing about.

## Placement rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Define an error where the condition is **detected** (45.1) | Define codes in a global `errors.ts` "for now" |
| Handle an error where the **fallback** is owned (45.1) | Catch-and-handle at every layer "to be safe" |
| Give every code exactly one **owning module** (45.16) | Let codes live where no team's CODEOWNERS applies |
| Keep retry/serialization decisions at their boundary owner | Branch on HTTP status inside domain services |

## Kernel and sharing rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the kernel to primitives: base, result, guards, redaction (45.3) | Put product codes or vendor helpers in the kernel |
| Promote to shared only after **3 evidenced consumers** (45.15) | Extract on first use "for consistency" |
| Version the kernel as a real package with semver (45.18) | Let features vendor silent copies of kernel code |
| Keep shared abstractions usable in a 5-line test | Ship a DSL engineers must learn to throw an error |

## Zone and dependency rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enforce zone imports with CI graph rules (45.12) | Trust code review alone to catch cycles |
| Let adapters **translate only**; attach vendor error as `cause` | Let adapters retry, decide outcomes, or serialize |
| Wire adapters at the composition root | Let domain services import `infra/**` |
| Make the registry **pure data** | Add functions to the registry that import transports |

## Module inventory rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| One named retry policy per dependency class, referenced by name (45.9) | Inline `attempts: 5` at call sites |
| One error serializer per transport (45.11) | Let each controller invent its error JSON |
| Colocate compensations with their saga steps (45.10) | Build a global `CompensationService` |
| One mapping function per vendor adapter (45.8) | Map the same SQLSTATE in three repositories |

## Structure and navigability rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Prefix every code with its owning feature (`CHECKOUT_*`) (45.19) | Use owner-less prefixes (`ERR_`, `E1002`) |
| Keep one `errors.ts` per feature folder | Scatter error classes across service files |
| Grow into the standard tree's slots on demand (45.20) | Copy the full 20+ file tree into a 2-person MVP |
| Export feature errors only via the feature's `index.ts` | Re-export everything from a global barrel |

## God-module and duplication rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Freeze a god module before extracting; delete it after (45.13) | Keep accepting "just one more helper" |
| Extract a duplicated policy at **3 copies, and delete the copies** (45.14) | Add a shared helper beside the originals |
| Assign CODEOWNERS to every extracted module | Extract into another unowned shared folder |
| Watch the top-conflicted-files report for `errors`-named files | Wait for an incident to split the file |

## Review questions worth arguing about

1. **Ownership.** For the codes in this PR: which module owns each, and does the owner's team
   review it?
2. **Zone.** Does any import cross a zone boundary it shouldn't (domain → infra, kernel →
   feature)? Show the import list, not the diagram.
3. **Singularity.** Does this PR add a second serializer, a second retry constant block, or a
   second translation of something that already has a home?
4. **Metadata.** Is the registry updated in the same PR, and does the transport still produce
   the right status without a code change?
5. **Deletion.** If this PR introduces a shim or a "temporary" global, where is the dated
   removal ticket?

## Escalation criteria

Stop the PR and redesign when you see any of:

- A new shared error package with more than one product code in its first release.
- A domain file importing from `infra/` "for convenience."
- A retry loop with numeric constants outside `shared/resilience/retry-policies.ts`.
- A second `catch` that formats RFC 9457 JSON outside `transports/http/serialize-problem.ts`.
- An error file with internal import fan-in ≥ 8.

## Related

- [Chapter 45 README](../README.md)
- [Reference: Directory Structure & Placement Tables](../05-reference/README.md)
- [Chapter 46 — Patterns and Anti-Patterns](../../46-error-handling-patterns-and-anti-patterns/README.md)
