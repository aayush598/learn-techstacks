# Framework Independence and Outcome Mechanics Across Languages

> Part VII · Chapter 18 · Sections 18.11, 18.12, 18.17, 18.18 · _Estimated reading time: 22 min_
> **Prerequisite:** [Expected Outcomes, Alternative Outcomes, and Compatible Contracts](../01-concepts/05-outcome-modeling-and-contracts.md)

## In one sentence

The domain layer must compile **without** Spring/Django/Express types or HTTP status numbers, and
its denials must be expressible in each language's strongest available mechanism — `Result`
types, discriminated unions, typed exceptions, or sentinel-free error values — while the boundary
translates them into transport contracts **without losing codes, details, or cause**.

## Why this matters in production

Framework-coupled domain errors fail three real tests: swapping frameworks becomes a rewrite;
unit tests boot containers; and framework exception hierarchies (`DataAccessException`,
`Http404`, `IntegrityError`) *become* your public vocabulary, so a dependency upgrade silently
changes client-visible behavior. Meanwhile the mechanics of "how a denial travels" differ sharply
across languages — choosing the strongest available mechanism per language is what keeps the
exhaustiveness guarantees from 18.13 real.

## The purity contract (18.17)

A domain module may depend on: other domain modules, small ports (clock, id generator, pricing).
It may **not** depend on: web frameworks, ORM exception types, HTTP status constants, queue SDKs,
vendor clients, `Date.now()`/`new Date()` without a clock port, environment globals.

```text
 compile-time dependency rule (enforce with lint/arch tests):

   domain/          →  allowed: domain/**, ports/**
   application/     →  allowed: domain/**, ports/**
   adapters/http/   →  allowed: everything (translates domain → transport)
   adapters/db/     →  allowed: domain errors (translates SQLSTATE → domain)
```

```ts
// ❌ framework in the domain
import { HttpException } from "@nestjs/common";
throw new HttpException("quota", 402);

// ✅ domain error + registry mapping done at the adapter
export class SeatQuotaExceeded extends DomainError {
  readonly code = "SEAT_QUOTA_EXCEEDED" as const;
  readonly category = "QUOTA";
  constructor(readonly requested: number, readonly limit: number) { super(); }
}
// http adapter:  code registry → { status: 402, body: toProblem(err) }
```

CI greps that pay for themselves immediately:

```bash
# fail the build if domain imports infrastructure
rg -n "from ['\"](express|fastify|django|spring|@nestjs|pg|stripe)" domain/ && exit 1
rg -n "\b(4\d\d|5\d\d)\b" domain/ --type ts   # review any HTTP status literal in domain
```

## 18.11/18.12 — Outcome mechanics per language

Same design, four idiomatic encodings:

**TypeScript — discriminated union (strongest).**
```ts
type ChargeOutcome =
  | { kind: "charged"; paymentId: string }
  | { kind: "card_declined"; reason: string }
  | { kind: "insufficient_funds"; due: string };

function handle(o: ChargeOutcome) {
  switch (o.kind) {
    case "charged": return o.paymentId;
    case "card_declined": return promptNewCard(o.reason);
    case "insufficient_funds": return showPayDue(o.due);
  } // no default → new kind breaks the build ✅
}
```

**Go — error values with `errors.Is` sentinels (idiomatic result).**
```go
var ErrSeatQuota = errors.New("SEAT_QUOTA_EXCEEDED")

func Upgrade(t *Tenant, want int) error {
    if want > t.Plan.MaxSeats {
        return fmt.Errorf("%w: requested=%d limit=%d", ErrSeatQuota, want, t.Plan.MaxSeats)
    }
    return nil
}

// caller:
if errors.Is(err, ErrSeatQuota) {           // branch on the code, parse details from text/meta
    return mapQuotaProblem(err)             // boundary translation
}
```
Modern refinement: a `*DomainError` struct with `Code() string` + `Details() map` wrapped with
`%w` — sentinels alone lose structured details.

**Python — exceptions with typed classes *and* a registry (pragmatic).**
```python
class DomainError(Exception):
    code: str = "DOMAIN_ERROR"
    category: str = "INTERNAL"

class SeatQuotaExceeded(DomainError):
    code, category = "SEAT_QUOTA_EXCEEDED", "QUOTA"
    def __init__(self, requested: int, limit: int):
        super().__init__(self.code)
        self.details = {"requested": requested, "limit": limit}
```
Python has no checked exceptions — mitigate with an exhaustive registry test: every subclass is
registered, and the HTTP map is snapshot-tested. Consider `Result` libraries for core flows
where exhaustiveness matters most.

**Java/C# — checked/typed exceptions or sealed results.**
Prefer sealed interfaces (`sealed interface UpgradeResult`) in modern Java/C# for expected
denials; reserve the exception hierarchy for programming/infrastructure faults. If exceptions
carry denials, catch them by *specific type* at the boundary — never by the framework's
`RuntimeException` root.

| Language | Strongest denial mechanism | Fallback | Watch out |
| -------- | -------------------------- | -------- | --------- |
| TS | discriminated union | coded error class | `switch` without `default` hides new kinds |
| Go | wrapped `*DomainError` + `errors.Is` | sentinel errors | string-matching on `err.Error()` |
| Python | typed exception + registry | `Result` lib | accidental broad `except Exception` |
| Java/C# | sealed result types | typed exceptions | framework root-catch → 500 |

## 18.18 — Meaning-preserving translation at the boundary

The outbound hop (domain → transport) must carry **code, category, details, and cause**
(cause server-side only). The failure modes, revisited as mechanics:

```ts
// One mapper per API version; consults the registry — no per-handler guesses.
export function toTransport(err: DomainError, ctx: Ctx): Problem {
  const row = REGISTRY[err.code] ?? REGISTRY["INTERNAL_DOMAIN_ERROR"]; // unknown → safe generic + alert
  return {
    status: row.status,                                   // SEAT_QUOTA_EXCEEDED → 402
    body: {
      type: `https://errors.acme.example/${err.category.toLowerCase()}`,
      title: err.code,
      status: row.status,
      detail: row.defaultMessage,                          // replaceable; details carry data
      instance: ctx.path,
      requestId: ctx.requestId,
      details: err.details,                                // requested/limit/entitledPlans…
    },
    logMeta: { code: err.code, cause: err.cause },         // never serialized to the client
  };
}
```

Checklist per hop:

1. **Code unchanged** — the transport never invents or renames codes.
2. **Details copied wholesale** (allowlisted keys) — clients render from data, not prose.
3. **Category+code → status from the registry** — reordering a `switch` cannot change an API.
4. **Unknown code** → generic problem + alert (a domain code missing from the registry is a bug).
5. **Cause stays server-side**; stack traces never cross (Ch. 20/34).

## Key data / numbers

- Domain lint: zero framework imports in `domain/`; zero HTTP status literals.
- TS: unions without `default` → compile-time coverage of new outcome kinds.
- Go: `errors.Is`/`errors.As` for branching; never `strings.Contains(err.Error(), ...)`.
- Python: registry test asserting every `DomainError` subclass is registered.
- Unknown domain code at the boundary → `500 INTERNAL` + alert (never a silent `200`).

## Real-world use case — AgentRun

`AgentRun` (LLM tool-calling) mixed frameworks deep in the domain: tool handlers raised
`HttpException(400)` for bad tool args and a vendor SDK error type for provider failures. A
provider SDK upgrade renamed an error class; the `catch` stopped matching, and every provider
hiccup became an unhandled `500` instead of a coded `PROVIDER_UNAVAILABLE` (transient). The
cleanup: domain tool handlers return `ToolOutcome` unions (`ok` | `invalid_args` | `denied` |
`failed`); provider SDK types stay in the adapter; a registry test covers every outcome kind.
Afterward, swapping the provider required touching exactly one adapter file, and the exhaustiveness
compile error caught a newly added `context_exceeded` kind before it shipped as a raw 500.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Pure domain + adapter translation | Testable, portable, stable API | Indirection; mapping tables to maintain | ✅ Default |
| Framework exceptions as domain errors | Zero ceremony | Framework upgrade = contract change | Never for public contracts |
| Sealed results/unions | Exhaustive, documented | Type churn per addition | Core flows (18.13) |
| Typed exceptions (Python/Java) | Familiar | No compiler exhaustiveness | When registry tests exist |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Lint domain imports; block framework/HTTP types | Let `HttpException` escape a service |
| Use each language's strongest denial mechanism | Port TS union patterns into Go via string codes |
| Map code+category → status via registry | Map per-handler with inline `switch`es |
| Alert on unknown codes at the boundary | Default unknown domain errors to `200`/`404` |

## Common mistakes

- **`catch (e) { throw new DomainError(e) }` at the boundary** — erases cause and retry class
  (Ch. 16 anti-pattern).
- **Matching Go errors by string** — breaks on message rewording; use `errors.Is`/`As`.
- **Python `except Exception` around domain calls** — turns `402`-class denials into `500`s.
- **Status constants imported into the domain "just for tests"** — the dependency becomes real.

## Checklist

- [ ] Arch test: domain compiles with no framework/HTTP/ORM deps.
- [ ] Each language uses its strongest mechanism; weakest-pattern review items exist.
- [ ] One registry-driven mapper per API version; unknown codes alert.
- [ ] Details and cause handled per hop rules (details out, cause server-side).
- [ ] Provider/framework upgrades confined to adapters.

## Related

- [Domain Services, Aggregates, and DDD](./01-domain-services-aggregates-and-ddd.md)
- [Expected Outcomes, Alternative Outcomes, and Compatible Contracts](../01-concepts/05-outcome-modeling-and-contracts.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
- [Chapter 47 — Language-Level Error Semantics](../../../part-18-languages-and-frameworks/47-language-level-error-semantics/README.md)
