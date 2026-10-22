# The Full Category Catalog in Code

> Part II · Chapter 5 · Sections 5.1–5.35 · _Estimated reading time: 26 min_
> **Prerequisite:** [The Classification Decision Tree](../02-deep-dive/02-classification-decision-tree.md)

## In one sentence

A single **catalog table** (35 categories) plus a **pure classifier** is all the code you need to
turn any failure into a category, an HTTP status, a retry verdict, and a stable code.

## Why this matters in production

The taxonomy is only real when it exists as importable data. This file gives the complete catalog
as code and a classifier you can unit-test. Every service imports the same table, so behavior
cannot drift.

## The catalog (all 35 categories)

```ts
// error-catalog.ts
type Category =
  // 5.1–5.9  input / auth / business
  | "validation" | "request_parsing" | "authentication" | "authorization"
  | "business_rule" | "not_found" | "conflict" | "duplicate_operation" | "state_transition"
  // 5.10–5.15, 5.28  limits / concurrency / data
  | "rate_limit" | "quota" | "concurrency" | "database" | "cache" | "file_storage" | "data_integrity"
  // 5.16–5.21, 5.32  external / network / config
  | "external_api" | "network" | "timeout" | "serialization" | "configuration"
  | "dependency_initialization" | "third_party"
  // 5.22, 5.25–5.27, 5.31  runtime / resources / lifecycle
  | "resource_exhaustion" | "internal_programming" | "unexpected_runtime"
  | "cancellation" | "shutdown_lifecycle"
  // 5.23, 5.24, 5.29, 5.30, 5.33–5.35  async / partial / specialized
  | "background_job" | "scheduled_task" | "partial" | "compensation"
  | "ai_provider" | "ai_tool" | "ai_token_limit" | "webhook" | "file_processing";

interface Policy { http: number; retry: boolean; alert: "none"|"warn"|"page"; sensitive: boolean; }

export const CATALOG: Record<Category, Policy> = {
  // input / auth / business
  validation:               { http: 422, retry: false, alert: "none", sensitive: false },
  request_parsing:          { http: 400, retry: false, alert: "none", sensitive: false },
  authentication:           { http: 401, retry: false, alert: "warn", sensitive: true  },
  authorization:            { http: 403, retry: false, alert: "warn", sensitive: true  },
  business_rule:            { http: 422, retry: false, alert: "none", sensitive: false },
  not_found:                { http: 404, retry: false, alert: "none", sensitive: false },
  conflict:                 { http: 409, retry: false, alert: "none", sensitive: false },
  duplicate_operation:      { http: 200, retry: false, alert: "none", sensitive: false }, // replay
  state_transition:         { http: 409, retry: false, alert: "none", sensitive: false },
  // limits / concurrency / data
  rate_limit:               { http: 429, retry: true,  alert: "warn", sensitive: false },
  quota:                    { http: 429, retry: false, alert: "warn", sensitive: false },
  concurrency:              { http: 409, retry: true,  alert: "warn", sensitive: true  },
  database:                 { http: 503, retry: true,  alert: "page", sensitive: true  },
  cache:                    { http: 500, retry: false, alert: "warn", sensitive: true  },
  file_storage:             { http: 502, retry: true,  alert: "warn", sensitive: true  },
  data_integrity:           { http: 500, retry: false, alert: "page", sensitive: true  },
  // external / network / config
  external_api:             { http: 502, retry: true,  alert: "warn", sensitive: true  },
  network:                  { http: 503, retry: true,  alert: "warn", sensitive: true  },
  timeout:                  { http: 504, retry: true,  alert: "warn", sensitive: false },
  serialization:            { http: 400, retry: false, alert: "warn", sensitive: false },
  configuration:            { http: 500, retry: false, alert: "page", sensitive: true  },
  dependency_initialization:{ http: 500, retry: false, alert: "page", sensitive: true  },
  third_party:              { http: 502, retry: true,  alert: "warn", sensitive: true  },
  // runtime / resources / lifecycle
  resource_exhaustion:      { http: 503, retry: true,  alert: "page", sensitive: true  },
  internal_programming:     { http: 500, retry: false, alert: "page", sensitive: true  },
  unexpected_runtime:       { http: 500, retry: false, alert: "page", sensitive: true  },
  cancellation:             { http: 499, retry: false, alert: "none", sensitive: false },
  shutdown_lifecycle:       { http: 503, retry: true,  alert: "warn", sensitive: false },
  // async / partial / specialized
  background_job:           { http: 500, retry: true,  alert: "warn", sensitive: false },
  scheduled_task:           { http: 500, retry: true,  alert: "warn", sensitive: false },
  partial:                  { http: 500, retry: false, alert: "page", sensitive: false },
  compensation:             { http: 500, retry: true,  alert: "page", sensitive: false },
  ai_provider:              { http: 502, retry: true,  alert: "warn", sensitive: false },
  ai_tool:                  { http: 502, retry: true,  alert: "warn", sensitive: false },
  ai_token_limit:           { http: 422, retry: false, alert: "none", sensitive: false },
  webhook:                  { http: 400, retry: false, alert: "warn", sensitive: true  },
  file_processing:          { http: 422, retry: false, alert: "warn", sensitive: false },
};
```

## The classifier (pure, testable)

```ts
// classify.ts
interface RawFailure {
  message: string;
  httpStatus?: number;       // from a provider, if any
  errno?: string;            // e.g. "ECONNRESET"
  sqlstate?: string;         // e.g. "40001"
  source: "input" | "db" | "cache" | "storage" | "remote" | "runtime" | "async" | "ai";
  cancelledByCaller?: boolean;
  jobContext?: boolean;
}

const TRANSIENT_SQLSTATE = new Set(["40001", "40P01", "08000", "08006", "53300", "57014"]);
const NETWORK_ERRNO = new Set(["ECONNREFUSED", "ECONNRESET", "ENOTFOUND", "ETIMEDOUT"]);

export function classify(f: RawFailure): Category {
  // gate 1 — cancellation
  if (f.cancelledByCaller) return "cancellation";            // 5.27

  // gate 2 — configuration
  if (/missing (env|config|secret)|invalid config/i.test(f.message)) return "configuration"; // 5.20

  // gate 3 — own-code defects
  if (f.source === "runtime" && /TypeError|is not a function|undefined/.test(f.message))
    return "internal_programming";                            // 5.25

  // gate 4 — input/contract
  if (f.source === "input") {
    if (/malformed json|unexpected token/i.test(f.message)) return "request_parsing"; // 5.2
    return "validation";                                      // 5.1
  }

  // gate 5 — limits
  if (f.source === "db" && f.sqlstate && TRANSIENT_SQLSTATE.has(f.sqlstate))
    return "concurrency";                                     // 5.12
  if (f.httpStatus === 429) return "rate_limit";              // 5.10 (override with code for quota)

  // gate 6 — data/store
  if (f.source === "db") {
    if (f.sqlstate === "23505") return "duplicate_operation"; // 5.8
    if (f.sqlstate === "23503" || f.sqlstate === "23514") return "conflict"; // 5.7
    return "database";                                        // 5.13
  }
  if (f.source === "cache") return "cache";                   // 5.14
  if (f.source === "storage") return "file_storage";          // 5.15

  // gate 7 — external/remote
  if (f.source === "ai") {
    if (/context_length_exceeded|finish_reason=length/.test(f.message)) return "ai_token_limit"; // 5.33
    if (/tool/.test(f.message)) return "ai_tool";
    return "ai_provider";
  }
  if (f.source === "remote") {
    if (/timeout|deadline/i.test(f.message)) return "timeout"; // 5.18
    if (f.errno && NETWORK_ERRNO.has(f.errno)) return "network"; // 5.17
    return "external_api";                                     // 5.16
  }

  // gate 8 — async
  if (f.jobContext) return "background_job";                   // 5.23

  // default
  return "unexpected_runtime";                                 // 5.26
}
```

## Classify, then derive policy

```ts
export function policyFor(c: Category, opts: { idempotent?: boolean; partial?: boolean } = {}) {
  const p = CATALOG[c];
  return {
    http: p.http,
    retryable: p.retry && (opts.idempotent ?? false),
    alert: p.alert,
    redact: p.sensitive,
    partial: opts.partial ?? false,
  };
}
```

## Unit tests (classification bugs become test failures)

```ts
test("40001 is concurrency and retryable", () => {
  const c = classify({ message: "could not serialize", sqlstate: "40001", source: "db" });
  expect(c).toBe("concurrency");
  expect(policyFor(c, { idempotent: true }).retryable).toBe(true);
});

test("23505 is duplicate, not database", () => {
  expect(classify({ message: "dup key", sqlstate: "23505", source: "db" }))
    .toBe("duplicate_operation");
});

test("token limit is permanent", () => {
  const c = classify({ message: "context_length_exceeded", source: "ai" });
  expect(c).toBe("ai_token_limit");
  expect(policyFor(c).retryable).toBe(false);
});
```

## Key data / numbers

- **35 categories**, one table, ~40 lines of classifier gates.
- `duplicate_operation` maps to HTTP **`200`** on replay — the only category whose "error" is a
  success to the caller.
- `cancellation` maps to `499` (nginx convention), logged at `info`.
- Transient SQLSTATE set: `40001`, `40P01`, `08000`, `08006`, `53300`, `57014`.

## Real-world use case — Acme SaaS

Acme replaced ~2,000 lines of per-endpoint `if (err.message…)` with this 35-row catalog and an
80-line classifier. New providers now require a new **code**, not new branching. When the LLM
provider changed its token-limit wording, one regex changed and every agent picked up the correct
`ai_token_limit` policy on deploy.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| Pure classifier + table | Deterministic, testable, shared | Needs maintenance |
| Regex on messages | Quick | Brittle, drifts |
| Per-endpoint branching | Local control | Inconsistent, huge |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Encode the tree as a pure function | Scatter classification in handlers |
| Unit-test each category | Trust regexes untested |
| Keep the catalog shared | Duplicate the table per service |
| Default to `unexpected_runtime` | Leave uncategorized errors |

## Common mistakes

- **Ordering gates wrong** — matching `unexpected_runtime` too early.
- **Regex-only classification** without structured signals (`sqlstate`, `errno`).
- **Forgetting to fold idempotency** into `retryable`.
- **Letting the HTTP layer reclassify**.

## Checklist

- [ ] Is there one shared catalog of all categories?
- [ ] Is the classifier pure and unit-tested?
- [ ] Are structured signals (`sqlstate`, `errno`) preferred over message text?
- [ ] Does `retryable` consult idempotency?

## Related

- [The Classification Decision Tree](../02-deep-dive/02-classification-decision-tree.md)
- [Scenario Classification Drills](./02-scenario-classification-drills.md)
- [Classifying Errors in Code (Ch. 4)](../../04-designing-a-comprehensive-error-taxonomy/03-practical-examples/02-classifying-errors-in-code.md)
