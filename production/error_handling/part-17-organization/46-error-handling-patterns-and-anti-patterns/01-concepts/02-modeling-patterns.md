# Modeling Patterns: Result Type, Code Registry, Translation

> Part XVII · Chapter 46 · Sections 46.3, 46.4, 46.5 · _Estimated reading time: 15 min_
> **Prerequisite:** [Structural Patterns](./01-structural-patterns.md), [Chapter 8 — Error Codes and Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)

## In one sentence

Three **modeling patterns** decide *how* failures are represented and routed: the **result
type** for explicit success/failure returns, the **code registry** as the single source of
truth for code metadata, and **translation** for converting foreign errors into the app model
without losing the cause.

## Why this matters in production

Representation bugs are contract bugs. A result type used inconsistently (some functions throw,
some return `null`, some return `Result`) means every caller invents its own handling and some
invent none. An un-registryed code means the HTTP layer guesses the status — `500` for a card
decline, `400` for a rate limit — and clients cannot branch. Lost translation means the DLQ
shows `error: {}` or a vendor class name that support cannot act on. These three patterns fix
representation once so every consumer agrees.

## Pattern 46.3 — Result type

**What:** Functions that have *expected, frequent* failure modes return an explicit
`Result<T, E>` (or a language equivalent — Rust `Result`, Go `(T, error)`, TS discriminated
union) instead of throwing. Throwing remains for exceptional/unexpected conditions.

**Solves:** Callers cannot forget to handle known failures — the compiler forces the branch.
Hot-path validation and parsing stop paying exception-construction cost. Control flow is
visible in the signature.

**Must not:** Replace exceptions for truly exceptional paths, and must not be mixed
arbitrarily within one module. Pick per-layer convention (e.g. domain services return
`Result`; event handlers throw).

```ts
// TypeScript discriminated-union result — kernel-provided, no third-party dep needed.
export type Result<T, E extends AppError> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// features/export/parse.ts — expected failure (bad rows) as a result; bugs still throw.
export function parseCsvChunk(buf: Buffer): Result<Row[], ExportParseError> {
  const rows = tryParse(buf);
  if (rows === null) return { ok: false, error: new ExportParseError("malformed_csv") };
  return { ok: true, value: rows };
}

// caller must handle — the compiler rejects the forgetful version:
const r = parseCsvChunk(chunk);
if (!r.ok) return checkpoint.fail(r.error);   // no silent fallthrough possible
ingest(r.value);
```

## Pattern 46.4 — Code registry

**What:** A pure-data catalog mapping every public error code to its metadata: HTTP status,
retryable flag, public title, deprecation info. Exactly one entry per code; the transport,
docs pipeline, and client SDK all read it.

**Solves:** Status drift (two endpoints disagreeing on `CHECKOUT_CARD_DECLINED`'s status);
undocumented codes (CI fails if a code lacks an entry); docs drift (reference page generated
from the registry); SDK gaps (typed unions generated from the same data).

**Must not:** Contain behavior — no functions, no vendor imports, no message formatting.
Behavior on top of data belongs in the handlers and serializers that consume it.

```ts
// shared/registry/error-codes.ts — pure data; adding a code without an entry fails CI.
export const REGISTRY = {
  CHECKOUT_CARD_DECLINED:        { httpStatus: 402, retryable: false, publicTitle: "Card declined" },
  EXPORT_PARSE_MALFORMED_CSV:    { httpStatus: 422, retryable: false, publicTitle: "File could not be parsed" },
  DEP_LLM_RATE_LIMITED:          { httpStatus: 503, retryable: true,  publicTitle: "AI provider busy" },
  INTERNAL_UNEXPECTED:           { httpStatus: 500, retryable: false, publicTitle: "Unexpected error" },
} as const satisfies Record<string, { httpStatus: number; retryable: boolean; publicTitle: string }>;
```

## Pattern 46.5 — Translation

**What:** At each foreign boundary, convert the vendor/native error into the app model once,
attaching the original as `cause`, and carrying over the properties that matter (retryability,
permanence). The canonical direction is **foreign → domain**, never the reverse.

**Solves:** Vendor error shapes (`StripeError`, `PgError`, HTTP 5xx from an internal service)
stop leaking past the adapter; observability keeps the root cause via `cause`; retry decisions
read stable metadata (`retryable`) instead of vendor class names.

**Must not:** Overgeneralize (mapping *every* upstream 500 to one `DEPENDENCY_ERROR` destroys
routing) or lose permanence (a `404` from a provider is not the same as a `503`).

```ts
// infra/llm/errors.ts — AgentRun provider adapter: translation with preserved semantics.
export function fromProviderError(err: unknown): AppError {
  if (isRateLimit(err))    return new DependencyError("LLM_RATE_LIMITED",
    { retryable: true, cause: err });                 // 429 semantics survive
  if (isTokenLimit(err))   return new DependencyError("LLM_TOKEN_LIMIT",
    { retryable: false, cause: err });                // permanent for THIS request
  if (isTimeout(err))      return new DependencyError("LLM_TIMEOUT",
    { retryable: true, cause: err });
  return new DependencyError("LLM_PROVIDER_UNEXPECTED", { retryable: false, cause: err });
}
```

## Key data

- **Result-type sweet spot:** expected failure rates above ~1% of calls (validation, parsing,
  row-level import errors). Below that, exceptions-with-boundary are simpler and the language
  ecosystem already understands them.
- **Registry entry minimum:** `httpStatus`, `retryable`, `publicTitle`. Codes at Acme: 45
  entries; CI rejects a build when `grep` finds a `code = "..."` string absent from the
  registry.
- **Translation `cause` chain depth:** keep one adapter hop per dependency; a chain of three
  wrappers already makes support triage measurably slower (each hop risks losing fields).
- **SQLSTATE translation table minimum (Postgres):** `23505` unique → conflict, `23503` FK →
  conflict/dependency, `23514` check → validation/business, `40001` serialization → retryable
  dependency, `40P01` deadlock → retryable dependency, `57014` timeout → retryable dependency.

## Real-world use case — Acme SaaS

`ExportJob` parsed customer-uploaded CSVs with exceptions: every malformed row threw, and the
worker's boundary caught it as a job-level failure — so one bad row among 50,000 failed the
whole export, and customers re-uploaded repeatedly. After switching row parsing to a **result
type**, the job collected per-row failures, exported the valid rows, and attached a
`EXPORT_ROWS_SKIPPED` summary error (registered, 200-with-report semantics in the job result —
not in HTTP). Same underlying data, radically different support load: "export failed, try
again" tickets fell by roughly three-quarters the following quarter, because most failures were
now partial successes with a downloadable report instead of opaque job failures.

## Trade-offs

| Pattern | Buys | Costs | When |
| ------- | ---- | ----- | ----|
| Result type | Compiler-enforced handling; cheap hot path | Verbose callers; convention needed | Expected, frequent failures |
| Exceptions + boundary | Concise happy path; ecosystem default | Forgetting = runtime bug; cost on hot path | Exceptional failures |
| Registry as data | One source; codegen; CI-checkable | Discipline to update in-PR | Any public contract |
| Metadata on classes only | Colocation | Invisible to docs/SDK generators | Internal-only tools |
| Translation with cause | Debuggable; vendor-isolated | One adapter file per vendor | Every external dependency |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Choose result vs exception **per layer convention**, not per function | Mix `Result` and `throw` randomly in one module |
| Fail CI when a code lacks a registry entry | Let handlers hardcode statuses per route |
| Translate once at the adapter, preserve `cause` and `retryable` | Translate again in the controller or worker |
| Keep translations semantically specific (rate-limit ≠ timeout ≠ 404) | Map every upstream failure to one `DEPENDENCY_ERROR` |

## Common mistakes

- **Result without exhaustiveness.** `const r = f(); r.value` with a loose type erases the
  benefit. Use a discriminated union and let the compiler enforce the check.
- **Registry as a second code list.** Codes defined in features *and* copy-pasted into the
  registry drift. Generate one from the other, or CI-diff them.
- **Translation as classification loophole.** Adapters mapping "unknown" vendor errors to
  `retryable: true` by default cause retry storms on permanent failures. Default unknown →
  non-retryable (fail-safe for retries).

## Checklist

- [ ] A layer convention exists for result vs exception, and is followed in that layer.
- [ ] Every public code has exactly one registry entry; CI enforces it.
- [ ] Every vendor adapter exports exactly one `from<Vendor>Error` with `cause` preservation.
- [ ] Unknown vendor errors default to non-retryable.
- [ ] Docs/SDK generation (if any) reads the registry, not hand lists.

## Related

- [Resilience and Control-Flow Patterns](./03-resilience-and-control-flow-patterns.md)
- [Handling Anti-Patterns](./04-handling-anti-patterns.md)
- [Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
