# The Four Zones: Primitives, Domain, Infra Adapters, Transport

> Part XVII · Chapter 45 · Sections 45.3–45.6 · _Estimated reading time: 16 min_
> **Prerequisite:** [Shared Kernel vs App-Specific Code](./02-shared-kernel-vs-app-specific.md)

## In one sentence

Every error-handling module in the system falls into exactly one of **four zones** — core
primitives, domain definitions, infra adapters, transport handlers — and each zone has a fixed
vocabulary of responsibilities and a fixed set of things it must never do.

## Why this matters in production

Without named zones, "where do I put this?" is answered by whoever is shipping fastest, and the
answers conflict: the domain starts importing HTTP statuses, adapters start deciding business
outcomes, transport handlers start re-translating driver errors. Six months later, moving the
Checkout flow to a new payment vendor requires touching the domain — the exact coupling layered
architecture exists to prevent. Zones turn architecture from a diagram into **file-level rules
a linter could check**.

## Core concept: the zones and their contracts

```text
 ┌──────────── ZONE 1: TRANSPORT HANDLERS ────────────┐   serializes; speaks RFC 9457,
 │  http/error-handler · jobs/runner · webhooks/ack   │   job-failure, webhook status
 └───────────────────────▲─────────────────────────────┘
 ┌──────────── ZONE 3: INFRA ADAPTERS ────────────────┐   translates foreign → app;
 │  postgres/ · stripe/ · s3/ · redis/ · llm/        │   owns vendor types & retry hints
 └───────────────────────▲─────────────────────────────┘
 ┌──────────── ZONE 2: DOMAIN / APPLICATION ──────────┐   defines codes & outcomes;
 │  checkout/errors · export/errors · agent/errors   │   decides retryable semantics
 └───────────────────────▲─────────────────────────────┘
 ┌──────────── ZONE 1: CORE PRIMITIVES (kernel) ──────┐   AppError, Result, Category,
 │  errors-core: base types, redaction, guards       │   redaction — no policy
 └─────────────────────────────────────────────────────┘
```

| Zone | Owns | Imports from | Never does |
| ---- | ---- | ------------ | ---------- |
| **1. Core primitives** (45.3) | `AppError` base, `Result<T,E>`, `ErrorCategory`, `isAppError`, redaction helper, correlation context | (nothing internal) | Defines product codes; knows HTTP/SQL/Stripe; contains retry loops |
| **2. Domain definitions** (45.4) | Domain error classes & codes, business-rule failures, retryable *semantics* ("this condition is transient") | Zone 1 only | Imports driver/SDK types; picks HTTP status by branching; catches-and-recovers |
| **3. Infra adapters** (45.5) | Translation tables (SQLSTATE→code, Stripe→code), vendor error wrappers, connectivity error classes | Zones 1–2 | Decides business outcomes; serializes to clients; implements per-call-site retries |
| **4. Transport handlers** (45.6) | Global error middleware, RFC 9457 serialization, job failure reporting, webhook ack/nack mapping, header discipline (`Retry-After`) | Zones 1–2 (reads metadata) | Re-translates vendor errors; invents new codes; swallows errors |

## How it works (mechanics)

**Zone 1 — primitives.** Ship as a versioned package (`@acme/errors-core`). Contents are
structural, not semantic: a base class with `code`/`category`/`retryable`/`cause`, a `Result`
type if used, a `redact()` for context sanitization, and type guards. Test it like a library.

**Zone 2 — domain definitions.** One `errors.ts` per feature module (`checkout/`, `export/`,
`agent/`). Each file defines the codes the feature can *recognize* and stamps each with
retryable/recoverable semantics. Domain tests assert on these types directly — no mocks.

**Zone 3 — infra adapters.** One folder per dependency. Each adapter exposes a single public
translation function (`fromPgError`, `fromStripeError`) plus connectivity error types. The
adapter attaches the raw vendor error as `cause` so debuggability survives translation. This is
the *only* zone allowed to import vendor SDK types.

**Zone 4 — transport handlers.** One HTTP global handler, one job-runner wrapper, one webhook
ack mapper. They read `code`, `category`, `retryable`, and any `httpStatus` metadata off the
error and produce the external contract. They are the *only* zone that speaks to clients,
queues, or callers outside the process.

## Worked example

```ts
// ZONE 3 — infra/postgres/errors.ts: the only file that knows SQLSTATE.
import { AppError } from "@acme/errors-core";
import { ConflictError } from "../../features/project/errors";

export function fromPgError(err: unknown): AppError {
  const sqlstate = getSqlState(err); // vendor-specific extraction, local to this file
  switch (sqlstate) {
    case "23505": // unique_violation
      return new ConflictError("project_slug_taken", { cause: err });
    case "40001": // serialization_failure — transient, retryable at the transaction layer
      return new DependencyError("PG_SERIALIZATION_FAILURE", { retryable: true, cause: err });
    case "57014": // query_canceled (statement_timeout)
      return new DependencyError("PG_STATEMENT_TIMEOUT", { retryable: true, cause: err });
    default:
      return new DependencyError("PG_UNEXPECTED", { retryable: false, cause: err });
  }
}

// ZONE 2 — features/project/errors.ts: domain meaning, no vendor knowledge.
import { AppError } from "@acme/errors-core";

export class ConflictError extends AppError {
  readonly category = "conflict" as const;
  constructor(readonly conflictKind: string, opts?: { cause?: unknown }) {
    super(`Conflict: ${conflictKind}`, opts);
  }
  override get code() { return `PROJECT_${this.conflictKind.toUpperCase()}`; }
}

// ZONE 4 — http/error-handler.ts: the only file that produces RFC 9457 JSON.
export function toProblemDetails(err: AppError, req: Request) {
  return {
    type: `https://acme.dev/problems/${err.code.toLowerCase()}`, // stable, docs-hosted identifier
    title: err.category.replace("_", " "),
    status: statusFor(err),                 // from registry metadata, not a switch on class
    detail: err.message,                    // sanitized by kernel redact()
    instance: req.url,
    "request-id": req.ctx.correlationId,
  };
}
```

Translation happens once (Zone 3), meaning is set once (Zone 2), serialization happens once
(Zone 4). Nothing is repeated.

## Key data

- **Zone counts for a mid-size SaaS (Acme-scale):** 1 kernel package, 5–10 domain `errors.ts`
  files, 4–8 adapter folders with one translation function each, 3–4 transport handlers (HTTP,
  job runner, webhook ingest, CLI).
- **Import violations per zone are the review gate:** zero Zone-2→Zone-3 imports is a CI
  checkable property (dependency-cruiser, eslint `import/no-cycle` + boundary rules).
- **Translation tables should cover the SQLSTATEs you actually see:** `23505` unique_violation,
  `23503` foreign_key_violation, `23514` check_violation, `40001` serialization_failure,
  `40P01` deadlock_detected, `57014` query_canceled — six codes cover the overwhelming majority
  of production Postgres incidents.

## Real-world use case — Acme SaaS

When Acme built `AgentRun` (LLM tool-calling), the team initially called the LLM SDK directly
from the domain service and caught `RateLimitError` from the provider SDK inside business logic.
Two bugs followed: (1) a provider SDK upgrade renamed the class and the catch silently stopped
matching — a Zone-2 file depended on a Zone-3 type; (2) token-limit handling diverged between the
"summarize" feature and the agent feature because both translated independently. The refactor
created `infra/llm/errors.ts` as the single translation point (`fromProviderError` →
`LLM_RATE_LIMITED` retryable / `LLM_TOKEN_LIMIT` permanent / `LLM_INVALID_OUTPUT` retryable-once).
Domain services now catch only kernel types; the SDK rename cost one file. Incident recurrence
of "unclassified LLM error → whole AgentRun 500" dropped to zero over the following quarter.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Strict four zones | One-way deps; vendor swaps touch one folder; testable domain | More files; slight indirection | Default for any SaaS with external deps |
| Adapters merged into domain | Fewer files | Vendor types leak; swaps are cross-cutting | Prototypes with one dependency |
| Transport logic in domain | Fastest to first response | Unreusable across HTTP/CLI/worker; status drift | Never after the first second transport appears |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep exactly one translation function per dependency | Translate the same SQLSTATE in three repositories |
| Stamp retryable *semantics* in the domain, hints in the adapter | Let the adapter decide the business outcome |
| Let transport read metadata off errors | Have transport switch on concrete error classes |
| Give every zone a lint/import boundary | Rely on code review alone for zone discipline |

## Common mistakes

- **Transport re-translation.** The HTTP handler imports `fromPgError` "just for one case" —
  now every layer can reclassify, and status codes drift between endpoints.
- **Domain branching on HTTP status.** `if (err.httpStatus === 409)` inside a service couples
  business logic to one transport. Branch on `category` or the typed error instead.
- **Adapter mega-files.** One `integrations/errors.ts` handling Stripe + S3 + Postgres becomes
  unownable. One folder per dependency keeps CODEOWNERS honest.

## Checklist

- [ ] Each new dependency gets its own adapter folder with one public translation function.
- [ ] No file outside `infra/<vendor>/` imports that vendor's SDK error types.
- [ ] Domain error classes carry no HTTP framework imports.
- [ ] Transport handlers switch on metadata (`category`, registry), never on concrete classes.
- [ ] Import-boundary linting is enforced for all four zones in CI.

## Related

- [Supporting Modules: Registries, Mappings, Retries, Serialization](./04-supporting-modules-registries-mappings-retries-serialization.md)
- [Circular Dependency Avoidance](../02-deep-dive/01-circular-dependency-avoidance.md)
- [Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
