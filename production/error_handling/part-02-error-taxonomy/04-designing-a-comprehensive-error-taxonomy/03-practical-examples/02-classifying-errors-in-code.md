# Classifying Errors in Code

> Part II · Chapter 4 · Sections 4.3–4.15 (mechanics) · _Estimated reading time: 24 min_
> **Prerequisite:** [A Complete Taxonomy for Acme SaaS](./01-acme-error-taxonomy.md)

## In one sentence

Classification becomes real when **creating an error sets its primary category and tags once**,
and every downstream consumer reads them — never re-derives them.

## Why this matters in production

The taxonomy file is inert until the code populates it. The failure mode is subtle: an error is
created without classification, so each handler guesses, and guesses diverge. This file shows the
mechanics of attaching classification at creation, in TypeScript, Go, and Python.

## Core concept — classify at creation

```text
CREATE (throw/return) ──► error carries { category, code, tags, cause }
     │
     ├─► log layer reads category + tags (level, routing)
     ├─► HTTP edge reads category (status) + code (public body)
     ├─► retry engine reads tags (retryable, idempotent)
     └─► redactor reads tags (sensitive) before serialization
```

Nothing downstream calls `classify()` again. If it must, the error was created wrongly.

## Worked example — a typed, classified error (TypeScript)

```ts
// 01-classify.ts
export type Category =
  | "validation" | "request_parsing" | "authentication" | "authorization"
  | "business_rule" | "not_found" | "conflict" | "state_transition"
  | "rate_limit" | "quota" | "database" | "cache" | "file_storage"
  | "external_api" | "network" | "timeout" | "configuration"
  | "resource_exhaustion" | "internal_programming" | "unexpected_runtime"
  | "background_job" | "partial" | "compensation" | "ai_provider" | "ai_token_limit";

type Tag = "transient" | "sensitive" | "partial" | `dependency:${string}`;

interface AppError {
  category: Category;          // exactly one — routes
  code: string;                // stable, machine-readable
  http: number;                // DERIVED from category
  retryable: boolean;          // DERIVED from category + idempotency
  tags: Set<Tag>;              // descriptive axes
  cause?: unknown;             // preserved original
  context?: Record<string, unknown>; // safe metadata only
}

const POLICY: Record<Category, { http: number; retry: boolean; sensitive: boolean }> = {
  validation:           { http: 422, retry: false, sensitive: false },
  request_parsing:      { http: 400, retry: false, sensitive: false },
  authentication:       { http: 401, retry: false, sensitive: true  },
  authorization:        { http: 403, retry: false, sensitive: true  },
  business_rule:        { http: 422, retry: false, sensitive: false },
  not_found:            { http: 404, retry: false, sensitive: false },
  conflict:             { http: 409, retry: false, sensitive: false },
  state_transition:     { http: 409, retry: false, sensitive: false },
  rate_limit:           { http: 429, retry: true,  sensitive: false },
  quota:                { http: 429, retry: false, sensitive: false },
  database:             { http: 500, retry: true,  sensitive: true  },
  cache:                { http: 500, retry: false, sensitive: true  },
  file_storage:         { http: 502, retry: true,  sensitive: true  },
  external_api:         { http: 502, retry: true,  sensitive: true  },
  network:              { http: 503, retry: true,  sensitive: true  },
  timeout:              { http: 504, retry: true,  sensitive: false },
  configuration:        { http: 500, retry: false, sensitive: true  },
  resource_exhaustion:  { http: 503, retry: true,  sensitive: true  },
  internal_programming: { http: 500, retry: false, sensitive: true  },
  unexpected_runtime:   { http: 500, retry: false, sensitive: true  },
  background_job:       { http: 500, retry: true,  sensitive: false },
  partial:              { http: 500, retry: false, sensitive: false },
  compensation:         { http: 500, retry: false, sensitive: false },
  ai_provider:          { http: 502, retry: true,  sensitive: false },
  ai_token_limit:       { http: 422, retry: false, sensitive: false },
};

export function appError(
  category: Category,
  code: string,
  opts: { tags?: Tag[]; idempotent?: boolean; cause?: unknown; context?: Record<string, unknown> } = {},
): AppError {
  const p = POLICY[category];
  return {
    category,
    code,
    http: p.http,
    retryable: p.retry && (opts.idempotent ?? false),
    tags: new Set([...(p.sensitive ? (["sensitive"] as Tag[]) : []), ...(opts.tags ?? [])]),
    cause: opts.cause,
    context: opts.context,
  };
}
```

Usage at a call site — classification happens **once**:

```ts
if (!req.body.dateFrom) {
  throw appError("validation", "VALIDATION_REQUIRED_FIELD",
    { context: { field: "dateFrom" } });                 // 422, no retry, not sensitive
}

try {
  await queue.publish(job);
} catch (e) {
  throw appError("external_api", "DEPENDENCY_UNAVAILABLE",
    { tags: ["transient", "dependency:sqs"], idempotent: true, cause: e });
}
```

## The HTTP edge simply reads classification

```ts
// 02-edge.ts — no per-error branching
export function toResponse(err: AppError, reqId: string) {
  const body = {
    type: `https://acme.example/errors/${err.category}`,
    title: TITLES[err.category],
    status: err.http,
    code: err.code,
    instance: reqId,
    ...(err.tags.has("sensitive") ? {} : { detail: safeDetail(err) }),
  };
  return { status: err.http, headers: { "content-type": "application/problem+json" }, body };
}
```

## Same model in Go

```go
type Category string

type AppError struct {
    Category  Category
    Code      string
    HTTP      int
    Retryable bool
    Tags      []string
    Cause     error
}

func New(cat Category, code string, cause error, idempotent bool, tags ...string) *AppError {
    p := policy[cat] // same table
    return &AppError{cat, code, p.HTTP, p.Retry && idempotent, tags, cause}
}
```

And in Python:

```python
@dataclass(frozen=True)
class AppError(Exception):
    category: str
    code: str
    tags: frozenset[str] = frozenset()
    cause: BaseException | None = None
    # http/retryable derived via POLICY at serialization time
```

## Key data / numbers

- Classification adds **two fields** (`category`, `code`) and a small tag set — negligible cost.
- The policy table is ~25 rows; the HTTP edge has **zero** per-error branches.
- `retryable` must fold in `idempotent`; the same transient error is retryable for a keyed write
  and non-retryable for an unkeyed one.

## Real-world use case — Acme SaaS

Before classification-at-creation, Acme's export worker guessed statuses from messages. After the
change, the worker throws `appError(...)` and the API edge renders RFC 9457 responses with no
domain knowledge. The error taxonomy file and this helper are the *entire* contract between
worker, API, and frontend codegen.

## Trade-offs

| Placement | Pros | Cons |
| --------- | ---- | ---- |
| At creation (throw site) | Accurate, single source | Needs discipline |
| At boundary (edge) | Central | Loses original meaning |
| Never (message parsing) | None | Brittle, wrong |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive HTTP/retry from category | Set status codes at throw sites |
| Store `cause` + safe `context` | Attach raw request/PII |
| Classify for jobs/cache too | Only classify HTTP errors |
| Keep the policy table shared | Copy the table per service |

## Common mistakes

- **Reclassifying at the edge**, overriding the true category.
- **Deriving `retryable` without idempotency**.
- **Putting sensitive fields in `context`** — the redactor then has to save you.
- **A separate policy table per service** that drifts.

## Checklist

- [ ] Does every created error carry a category and code?
- [ ] Is HTTP/retry derived, never hand-set?
- [ ] Is `retryable` gated on idempotency?
- [ ] Does the edge render from classification without domain branches?

## Related

- [A Complete Taxonomy for Acme SaaS](./01-acme-error-taxonomy.md)
- [The Multi-Axis Classification Model](../02-deep-dive/01-multi-axis-classification-model.md)
- [Designing the Application's Error Model](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
