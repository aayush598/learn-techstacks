# Versioning the Internal Error Contract

> Part III · Chapter 6 · Section 6.20 · _Estimated reading time: 16 min_
> **Prerequisite:** [Model Invariants](./01-model-invariants.md)

## In one sentence

Your error model is a **contract with every consumer** — handlers, log pipelines, UI clients,
support tools — so you evolve it with the same discipline as a public API: add optional fields,
never repurpose meaning, and version when a change cannot be made compatible.

## Why this matters in production

The error model is consumed by more systems than any other internal type: the API layer reads
`code`, the logger reads `metadata`, the retry engine reads `retryable`, the UI reads `details`,
and an on-call dashboard reads `category`. A casual rename of `severity` to `level` silently breaks
all of them at once, usually in production. Versioning discipline keeps the model useful as the
product (and the model) grows.

## What "the contract" covers

| Consumer | Reads | Breakage if changed |
| -------- | ----- | ------------------- |
| Internal handlers | `code`, `category`, `retryable` | Wrong routing/retry |
| Log/trace pipeline | `metadata`, `severity`, `timestamp` | Broken dashboards/alerts |
| HTTP boundary | `code`, `details` | Wrong status, broken client |
| Frontend | `code`, `details` | Broken field mapping, bad UX |
| Queues/DLQ | serialized error shape | Replay/inspection breaks |
| Support tooling | `code`, `correlationId` | Lost traceability |

The contract is not just the TypeScript interface; it is the **serialized shape** consumers depend
on.

## Compatibility rules

| Change | Compatible? | Rule |
| ------ | ----------- | ---- |
| Add an optional field | ✅ Yes | Consumers ignore unknown fields |
| Add a new code | ✅ Yes | New value, old consumers see a default path |
| Add an enum value to `category` | ⚠️ Conditional | Requires all total functions updated and consumers with a `default` branch |
| Rename a field | ❌ No | Add the new field, deprecate the old, migrate, then remove |
| Change a field's type | ❌ No | Add a new field, or version the model |
| Change a code's meaning | ❌ No | Never; introduce a new code (Chapter 8, §8.15) |
| Remove a field | ⚠️ Only after deprecation | Two-phase removal across a release cycle |
| Change `message` text | ✅ Yes | Messages are not contract (codes are) |

> ⚠️ **Hazard.** Changing the *meaning* of an existing code or field is worse than removing it:
> consumers keep compiling and running, but now act on the wrong semantics. Treat meaning as
> immutable.

## Versioning strategies

### 1. Additive-only (default, no version field)

Most changes are additive. If every consumer ignores unknown fields, you never need a version
number for additions.

```ts
interface AppError {
  code: string;
  category: ErrorCategory;
  // ... stable set ...
  helpUrl?: string;   // added later — optional, safe
}
```

### 2. Versioned serialized shape (for external/queue boundaries)

When the error crosses a durable boundary (DLQ, webhook, cross-service), stamp a schema version.

```json
{
  "schemaVersion": 2,
  "code": "EXPORT_UPLOAD_FAILED",
  "category": "external",
  "retryable": true,
  "message": "S3 upload failed",
  "metadata": { "tenantId": "t_acme", "shard": "shard_7" },
  "correlationId": "01HQ8...",
  "timestamp": "2026-03-01T10:22:01.482Z"
}
```

```ts
type SerializedErrorV2 = { schemaVersion: 2 } & SerializedErrorV1;

function deserialize(raw: unknown): AppError {
  const obj = raw as { schemaVersion?: number };
  switch (obj.schemaVersion) {
    case 1: return migrateV1toV2(obj as SerializedErrorV1);
    case 2: return fromSerialized(obj as SerializedErrorV2);
    default: return toErrorObject(raw); // forward-compatible fallback
  }
}
```

The `default` branch is what makes old consumers survive **new** versions they have never seen.

### 3. Namespaced extension bags

For per-domain fields, avoid widening the core set. Use a namespaced bag that core code ignores.

```ts
metadata: {
  "payment.provider": "stripe",
  "payment.declineCode": "card_declined",
  "agent.model": "gpt-4.1-mini",
  "agent.tokens": 1823,
}
```

Core consumers read `code` and `category`; domain consumers parse their namespace. The core contract
stays small.

## Worked example — migrating a rename

Renaming `retryable` → `isRetryable` without breaking consumers:

```ts
interface AppError {
  code: string;
  retryable: boolean;                 // legacy, still populated
  isRetryable?: boolean;              // new, canonical
}

function normalizedRetryable(err: AppError): boolean {
  return err.isRetryable ?? err.retryable; // prefer new, fall back to old
}
```

Release sequence:

1. **Add** `isRetryable` and populate both.
2. **Migrate** all readers to `isRetryable` (with fallback).
3. **Stop writing** `retryable` in a later release.
4. **Remove** `retryable` only after telemetry shows zero readers.

## Key data / numbers

- **Schema version** is an integer that increments on any non-additive change (commonly
  `schemaVersion` or `v`).
- **Deprecation window:** keep deprecated fields/codes for **at least one full release cycle**, or
  90 days for externally consumable shapes.
- **Unknown-field policy:** consumers MUST ignore unknown fields (Postel-style robustness) to keep
  additive changes compatible.
- **Forward-compat fallback:** unknown `schemaVersion` deserializes to the generic
  `toErrorObject` path rather than throwing.

## Real-world use case — ExportJob DLQ

Acme serialized failed `ExportJob` errors into a dead-letter queue. When they added
`metadata.primaryShard`, an old replay tool that did `JSON.parse` and destructured a fixed set of
keys kept working — because the addition was optional and the tool ignored unknowns. Later they
did a rename (`provider` → `dependency`) that *did* break the replay tool and forced a support
incident. They adopted additive-only changes plus a `schemaVersion` and a migration map; since
then, evolving the error shape has never required touching the replay tooling.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Additive-only | No versions, simplest | Cannot express removals/renames | Default for internal models |
| Versioned schema | Explicit, safe across services | Migration code per version | Durable/external boundaries |
| Namespaced bags | Core stays tiny | Less discoverable | Domain-specific fields |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Add optional fields freely | Rename/remove fields without a deprecation cycle |
| Treat code semantics as immutable | Repurpose an existing code |
| Ignore unknown fields in consumers | Throw on unknown fields from a newer producer |
| Stamp `schemaVersion` at durable boundaries | Rely on shape shape-matching |

## Common mistakes

- **Silent rename** that compiles internally but breaks log dashboards.
- **Repurposed code** — same string, new meaning; consumers act on stale semantics.
- **Non-forward-compatible deserializer** that throws on an unknown `schemaVersion`.
- **No deprecation telemetry**, so you cannot tell when it is safe to remove a field.
- **Versioning everything**, including internal-only additive changes that never needed it.

## Checklist

- [ ] Are all structural changes additive or explicitly versioned?
- [ ] Is code meaning treated as immutable?
- [ ] Do all consumers ignore unknown fields?
- [ ] Is there a `schemaVersion` on durable/external error shapes?
- [ ] Is there a migration map for older versions?
- [ ] Is deprecation removal gated on telemetry?

## Related

- [Model Invariants](./01-model-invariants.md)
- [Chapter 8 — Error Codes and Error Registries](../../08-error-codes-and-error-registries/README.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
