# Translation Tables and Policies

> Part VI · Chapter 16 · Section 16.16 · _Estimated reading time: 20 min_
> **Prerequisite:** [Vendor Codes, Tables, and Versioning](../01-concepts/05-vendor-codes-tables-and-versioning.md)

## In one sentence

A **translation table** is a declarative, data-driven mapping from a source error signature to a
target error spec plus **policy** (retry, alert, degrade, redaction) — and making it data rather
than code is what lets you audit, test, and extend translations safely.

## Why this matters in production

Inline `switch` statements hide the mapping inside control flow: you cannot enumerate "all the
errors we know," you cannot test coverage, and adding a provider means editing several functions.
A table turns translation into a **configuration** with a schema, a test suite, and a single place
to change. This is the single highest-leverage refactor for teams with more than two providers.

## Table schema

Define the schema once; every entry conforms to it.

```ts
type SourceKind = "postgres" | "stripe" | "s3" | "openai" | "os" | "grpc";

interface Match {
  source: SourceKind;
  code?: string;          // exact vendor/SQLSTATE/errno code
  codePrefix?: string;    // e.g. SQLSTATE class "08" (connection exceptions)
  http?: number;          // HTTP status when no structured code exists
}

interface Target {
  code: string;           // stable application code
  category: Category;     // VALIDATION | AUTH | CONFLICT | DEPENDENCY | BUSINESS | INTERNAL | RESOURCE
  transient: boolean;     // retry eligibility
  httpStatus?: number;    // transport mapping
  safeMessage: string;    // user-safe, curated
  alert?: boolean;        // should this page a human?
  degrade?: boolean;      // is this an optional dependency that can be isolated?
  redact?: string[];      // fields in the source error that must not be copied
  details?: (src: any) => Record<string, unknown>; // derive safe, structured details
}

interface Rule { match: Match; to: Target; }
```

Every field earns its place:

| Field | Consumer |
| ----- | -------- |
| `code` | clients, logging, registry |
| `category` | HTTP mapping, dashboards |
| `transient` | retry engine |
| `httpStatus` | request boundary |
| `safeMessage` | API response |
| `alert` | observability |
| `degrade` | fallback decisions |
| `redact` | security |
| `details` | validation UX |

## Precedence and matching order

When multiple rules can match, order matters. Resolve with explicit precedence:

1. **Exact `code`** beats `codePrefix` beats `http`.
2. **More specific `source`** beats a generic one.
3. **First match wins** within the same specificity — so keep specific rules above generic ones.

```ts
function findRule(source: SourceKind, err: any): Rule | undefined {
  const code = extractCode(source, err);
  return (
    RULES.find((r) => r.match.source === source && r.match.code === code) ??
    RULES.find((r) => r.match.source === source && r.match.codePrefix &&
                     code?.startsWith(r.match.codePrefix)) ??
    RULES.find((r) => r.match.source === source && r.match.http === statusOf(err))
  );
}
```

> ⚠️ **Hazard.** Table order is load-bearing. A `codePrefix: "08"` rule above a `code: "08006"`
> rule would swallow the more specific case. Put specific rules first and test the ordering.

## Policy composition

Keep **mapping** and **policy** co-located, but resolve policy in one place so it is consistent.
Typical policy decisions derived from the table:

```text
transient = true      → eligible for retry (respect retryAfterMs)
alert = true          → emit an alert (e.g. SCHEMA_ERROR, INTERNAL_ERROR)
degrade = true        → optional dependency; isolate at the feature boundary
non-transient + 5xx   → dependency failure the caller must surface
```

```ts
function toAppError(rule: Rule, src: any): AppError {
  return {
    code: rule.to.code,
    category: rule.to.category,
    transient: rule.to.transient,
    httpStatus: rule.to.httpStatus,
    safeMessage: rule.to.safeMessage,
    details: rule.to.details?.(src) ?? {},
    meta: { alert: !!rule.to.alert, degrade: !!rule.to.degrade },
    cause: redactCause(src, rule.to.redact), // strip sensitive fields from the cause copy
  };
}
```

## Redaction as part of the table

Some vendor errors echo secrets (a pre-signed URL, an API key fragment). The table's `redact` list
tells the translator which fields to scrub **from the cause copy** before it is logged.

```ts
function redactCause(src: any, fields?: string[]): any {
  if (!fields?.length || !src || typeof src !== "object") return src;
  const copy = { ...src };
  for (const f of fields) if (f in copy) copy[f] = "[REDACTED]";
  return copy;
}
```

## Testing strategy for a table

Four test layers, each cheap:

| Test | Asserts |
| ---- | ------- |
| **Entry test** | Each rule maps its sample source error to the expected `code`/`transient`/status |
| **Coverage test** | Every known vendor code (from a fixture list) has a rule — no accidental fall-through |
| **Ordering test** | Specific rules win over prefix/generic rules |
| **Unknown test** | An unlisted code hits the safe unknown branch, `transient = status ≥ 500` |

```ts
test("every known Stripe code is mapped", () => {
  for (const code of KNOWN_STRIPE_CODES) {
    const err = { type: "invalid_request_error", code };
    const app = translate("stripe", err);
    expect(app.code).not.toBe("PROVIDER_ERROR"); // would indicate a coverage gap
  }
});
```

The coverage test is what turns provider drift from a production incident into a red CI job.

## Extending the table (recipes)

| New thing | Steps |
| --------- | ----- |
| **New provider** | Write an adapter that extracts `code`; add rules; add a coverage fixture list |
| **New vendor code** | Add one rule (or one fixture entry); no consumer changes |
| **New internal category** | Add to `Category`; update HTTP mapping; document |
| **Tighten redaction** | Add field names to `redact`; add a test asserting scrubbing |
| **Change a status** | Treat as a contract change (Ch. 49); version it |

## Anti-patterns

- **Logic in the table.** Rules should be declarative; if a rule needs branching, use `details`
  functions sparingly and keep them pure.
- **A god table.** Split by source (`postgres.rules.ts`, `stripe.rules.ts`) so ownership matches
  the adapter.
- **Silent fall-through.** A missing rule must be loud (coverage test), not a vague `PROVIDER_ERROR`.
- **Duplicated mappings.** Two rules for the same code with different targets — last-wins surprises.

## Key data / numbers

- Precedence: exact `code` > `codePrefix` > `http`; specific before generic; first match wins.
- `transient` default false; unknown `5xx` → transient, unknown `4xx` → permanent.
- Redaction is applied to the **cause copy**; the live cause is untouched server-side.
- Coverage fixture lists should mirror each provider's documented error codes.

## Real-world use case — Acme SaaS

Acme's payment, storage, and LLM adapters each had their own `switch`. The team consolidated into
one table split by source. Adding a second payment provider meant a new adapter + a new
`adyen.rules.ts`; the retry engine, HTTP mapper, and clients were untouched. A coverage test
immediately caught two AWS codes that had been silently falling through to `PROVIDER_ERROR`,
explaining a class of incorrect `500`s.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make the mapping declarative and testable | Bury mappings in control flow |
| Co-locate policy with the mapping | Recompute retry/alert rules ad hoc |
| Test coverage against a provider code fixture | Let unknowns fall through silently |
| Put specific rules before generic ones | Rely on incidental ordering |
| Redact sensitive fields from the cause copy | Log vendor payloads verbatim |

## Common mistakes

- **Last-match-wins surprise** from unordered rules.
- **A generic rule above a specific one**, shadowing it.
- **No coverage test**, so a new provider code becomes a vague error.
- **Redacting the live cause** instead of the logged copy, breaking debugging.

## Checklist

- [ ] The table has a documented schema and precedence.
- [ ] Mapping and policy are co-located, resolved in one place.
- [ ] Entry, coverage, ordering, and unknown tests all exist.
- [ ] Redaction runs on the logged cause copy.
- [ ] Tables are split by source and owned by the adapter team.

## Related

- [Vendor Codes, Tables, and Versioning](../01-concepts/05-vendor-codes-tables-and-versioning.md)
- [Preserving Cause and Circular Chains](./02-preserving-cause-and-circular-chains.md)
- [Part VIII — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
