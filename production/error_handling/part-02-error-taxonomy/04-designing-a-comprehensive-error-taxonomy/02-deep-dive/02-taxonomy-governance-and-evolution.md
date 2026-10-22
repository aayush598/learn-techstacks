# Taxonomy Governance and Evolution

> Part II · Chapter 4 · Sections 4.17–4.18 · _Estimated read time: 20 min_
> **Prerequisite:** [Mutual Exclusivity, Growth, and Governance](../01-concepts/04-mutual-exclusivity-growth-governance.md)

## In one sentence

A taxonomy that cannot change safely becomes a tax; **governance is the mechanism that lets the
taxonomy evolve without breaking existing handlers, clients, or dashboards.**

## Why this matters in production

Taxonomies rot in predictable ways: categories duplicate, names drift, codes get renamed (breaking
dashboards), and removed categories leave dangling references. Governance prevents all four. The
goal is not bureaucracy — it is **safe, low-friction change**.

## Core concept — three change classes

Classify every proposed change by blast radius, then apply the matching process:

| Change | Example | Blast radius | Process |
| ------ | ------- | ------------ | ------- |
| **Add a code** | `INVOICE_ALREADY_PAID` | None (additive) | Fast path: PR to registry |
| **Add a category** | new `webhook` family | Handler routing tables | Review gate + owner |
| **Rename/remove** | `deadline` → `timeout` | Clients, dashboards, stored codes | Deprecation + alias period |

Most changes are additive and should be frictionless. Reserve ceremony for renames and removals.

## How it works — safe evolution

```text
ADD:      new code, new category (append-only) — old behavior unchanged
ALIAS:    new name points to old; both accepted for a deprecation window
DEPRECATE: mark old; log usage; keep mapping for a minimum of one release cycle
REMOVE:   only after usage hits zero and clients have migrated
```

Deprecation example with aliases:

```json
{
  "TIMEOUT_DEADLINE_EXCEEDED": { "deprecated": true, "alias_of": "TIMEOUT_OPERATION" },
  "TIMEOUT_OPERATION":         { "http": 504, "retryable": true }
}
```

Handlers and clients keep working; the registry logs when the deprecated code is still emitted so
you know when removal is safe.

## Versioning the taxonomy

- **Additive-only within a major version.** New codes/Categories are safe; renames are not.
- **Store the taxonomy version** on the error object (Chapter 6) so a handler knows which shape
  it is reading.
- **Public codes are contracts** (Chapter 49). Never silently repurpose a public code.
- **Internal categories may change faster** than public codes, but translations must preserve
  meaning (Chapter 16).

## Ownership model

| Role | Responsibility |
| ---- | -------------- |
| **Category owner** (domain team) | Definition, policy, examples |
| **Taxonomy maintainer** (platform) | Consistency, hierarchy, precedence |
| **Review gate** (architecture) | New families, renames, removals |
| **Consumers** (all teams) | Report gaps, propose changes |

A single maintainer with clear rules beats a committee. The maintainer's job is to say "that's a
code, not a category" quickly and consistently.

## Worked example — renaming a code safely

Acme has `STORAGE_WRITE_FAILED` used by uploads and exports. Usage audit shows two distinct
meanings. Rather than rename (breaking clients), Acme:

1. Adds `FILE_STORAGE_WRITE_FAILED` and `EXPORT_STORAGE_WRITE_FAILED` (fast path).
2. Aliases the old code to `FILE_STORAGE_WRITE_FAILED` for 90 days.
3. Migrates emit sites over two sprints.
4. Removes the old code once logs show zero occurrences.

No client changes, no dashboard breakage, one weekend of platform work.

## Migration patterns

When the taxonomy changes, code and stored records must move too. Three patterns cover most
cases:

| Pattern | When | How |
| ------- | ---- | --- |
| **Alias-on-read** | Rename a code | Registry maps old → new at serialization; no client change |
| **Dual-write** | New field/axis added | Emit both shapes for one release, then drop the old |
| **Backfill** | Category split | Re-classify stored records in a migration, verify counts |

```sql
-- Backfill example: split a legacy generic code into two specific ones.
UPDATE error_events
SET code = CASE
  WHEN context->>'source' = 'upload' THEN 'FILE_STORAGE_WRITE_FAILED'
  ELSE 'EXPORT_STORAGE_WRITE_FAILED'
END
WHERE code = 'STORAGE_WRITE_FAILED';
```

> ⚠️ **Hazard.** Never split a code without a **mapping table** from old → new. During the
> transition, both may be queried by dashboards, and an unmapped legacy value becomes an
> invisible gap in your metrics.

## Key data / numbers

- Deprecation windows in practice: **one minor release or 60–90 days**, whichever is longer.
- A registry that logs deprecated-code usage can tell you exactly when removal is safe.
- Keep the number of **public** codes far smaller than internal ones (public = contract surface).

## Real-world use case — Acme SaaS

After a reorg, two teams independently added `not_found` and `resource_missing`. The maintainer
merged them by aliasing `resource_missing → not_found`, updated the two emit sites, and added the
merged code to the public docs. Because the taxonomy had an owner, the duplication lived for days,
not quarters.

## Trade-offs

| Governance | Pros | Cons |
| ---------- | ---- | ---- |
| No process | Fast now | Sprawl, breaks later |
| Additive fast path + gate for renames | Balanced | One maintainer's time |
| Freeze everything | Consistent | Stagnation, bypass |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Prefer additive changes | Rename public codes in place |
| Alias during deprecation | Remove a code the same day |
| Version the taxonomy | Assume one global shape forever |
| Log deprecated usage | Retire blind |

## Common mistakes

- **Deleting a code without an alias.** Breaks clients and stored records.
- **Renaming internal categories** without updating the precedence tree.
- **No version on the error object** — handlers guess the shape.
- **Governance only for additions**, none for removals — the list only grows.

## Checklist

- [ ] Is there an explicit deprecation policy with a minimum window?
- [ ] Does the registry track usage of deprecated codes?
- [ ] Is the taxonomy versioned and carried on errors?
- [ ] Does one maintainer own consistency and precedence?

## Related

- [The Multi-Axis Classification Model](./01-multi-axis-classification-model.md)
- [Mutual Exclusivity, Growth, and Governance](../01-concepts/04-mutual-exclusivity-growth-governance.md)
- [Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
