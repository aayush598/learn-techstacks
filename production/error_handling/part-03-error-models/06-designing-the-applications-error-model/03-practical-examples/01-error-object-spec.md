# Practical: A Complete Error Object Specification

> Part III · Chapter 6 · Sections 6.1–6.20 · _Estimated reading time: 25 min_
> **Prerequisite:** [Model Invariants](../02-deep-dive/01-model-invariants.md)

## In one sentence

This file is a **copy-ready specification**: the TypeScript interface, the JSON wire shape at each
boundary, the constructor that enforces invariants, and the serializer/deserializer pair — one
concrete answer to "what should our error object actually be?"

## Why this matters in production

Most teams debate the error shape forever and ship three inconsistent versions. This file gives you
a defensible default. Copy it, rename the category set to match your taxonomy, and wire every error
path through the factory. The value is not the exact field list — it is that there is **exactly
one** of them.

## The TypeScript interface

```ts
// Category is the closed routing bucket from your taxonomy (Part II).
type ErrorCategory =
  | "validation" | "auth"     | "business" | "payment"
  | "database"   | "external" | "resource" | "unexpected";

type Severity = "info" | "warning" | "error" | "critical";

interface FieldError {
  field: string;                          // JSON pointer or dotted path
  code: string;                           // REQUIRED | INVALID_FORMAT | OUT_OF_RANGE | ...
  message: string;                        // human-readable, localizable
  meta?: Readonly<Record<string, unknown>>; // { min, max, ... }
}

interface AppErrorInit {
  code: string;
  message: string;
  category: ErrorCategory;
  severity?: Severity;
  recoverable?: boolean;
  retryable?: boolean;
  details?: FieldError[];
  cause?: unknown;
  metadata?: Record<string, unknown>;
  correlationId?: string;
  operation?: string;
}

interface AppError {
  readonly name: string;
  readonly code: string;
  readonly category: ErrorCategory;
  readonly severity: Severity;
  readonly recoverable: boolean;
  readonly retryable: boolean;
  readonly message: string;
  readonly details?: readonly FieldError[];
  readonly metadata: Readonly<Record<string, unknown>>;
  readonly correlationId?: string;
  readonly operation?: string;
  readonly timestamp: string;             // ISO-8601 UTC
  readonly cause?: unknown;
  readonly stackTrace: string;            // internal only
}
```

## Field reference

| Field | Required | Contract? | Serialized to client? | Notes |
| ----- | -------- | --------- | --------------------- | ----- |
| `name` | Yes | No | No | Class name for humans/stacks |
| `code` | Yes | **Yes** | Yes | Stable machine identifier |
| `category` | Yes | Yes | Optional | Closed set; drives policy |
| `severity` | Yes | No | No | Drives log level/alerting |
| `recoverable` | Yes | No | No | Continue vs abort |
| `retryable` | Yes | Yes | Yes | Retry eligibility |
| `message` | Yes | No | Public variant only | Single line, secret-free |
| `details` | No | Yes | Yes | Field-level validation |
| `metadata` | Yes | No | Allowlisted subset | Safe, scalar values |
| `correlationId` | No | Yes | Yes | Cross-service trace key |
| `operation` | No | No | No | Which phase failed |
| `timestamp` | Yes | No | No | ISO-8601 UTC |
| `cause` | No | No | No | Original error, preserved |
| `stackTrace` | Yes | No | **Never** | Logs only |

## The constructor (invariant-enforcing)

```ts
const CATEGORY_DEFAULTS: Record<ErrorCategory, Pick<AppErrorInit, "severity" | "retryable" | "recoverable">> = {
  validation: { severity: "info",    retryable: false, recoverable: true  },
  auth:       { severity: "warning", retryable: false, recoverable: true  },
  business:   { severity: "info",    retryable: false, recoverable: true  },
  payment:    { severity: "warning", retryable: false, recoverable: true  },
  database:   { severity: "error",   retryable: true,  recoverable: true  },
  external:   { severity: "warning", retryable: true,  recoverable: true  },
  resource:   { severity: "warning", retryable: true,  recoverable: true  },
  unexpected: { severity: "error",   retryable: false, recoverable: false },
};

const SENSITIVE_KEY = /password|token|secret|authorization|cookie|card[_-]?number|ssn|cvv/i;
const MAX_MESSAGE_BYTES = 2048;

class AppErrorClass extends Error implements AppError {
  readonly code: string;
  readonly category: ErrorCategory;
  readonly severity: Severity;
  readonly recoverable: boolean;
  readonly retryable: boolean;
  readonly details?: readonly FieldError[];
  readonly metadata: Readonly<Record<string, unknown>>;
  readonly correlationId?: string;
  readonly operation?: string;
  readonly timestamp: string;
  readonly stackTrace: string;

  constructor(init: AppErrorInit) {
    if (!init.code) throw new Error("AppError: code is required");
    const msg = sanitizeMessage(init.message);
    super(msg, init.cause !== undefined ? { cause: init.cause } : undefined);
    this.name = new.target.name;
    this.code = init.code;
    this.category = init.category;

    const d = CATEGORY_DEFAULTS[init.category];
    if (!d) throw new Error(`AppError: unknown category '${init.category}'`);
    this.severity = init.severity ?? d.severity;
    this.recoverable = init.recoverable ?? d.recoverable;
    this.retryable = init.retryable ?? d.retryable;

    this.details = init.details ? Object.freeze(validateDetails(init.details)) : undefined;
    this.metadata = Object.freeze(assertSafeMetadata(init.metadata ?? {}));
    this.correlationId = init.correlationId;
    this.operation = init.operation;
    this.timestamp = new Date().toISOString();
    this.stackTrace = this.stack ?? "";
    Object.freeze(this);
  }
}

function sanitizeMessage(message: string): string {
  const oneLine = (message ?? "").replace(/\s+/g, " ").trim();
  const safe = oneLine.length ? oneLine : "An error occurred";
  return safe.length > MAX_MESSAGE_BYTES ? safe.slice(0, MAX_MESSAGE_BYTES) : safe;
}

// assertSafeMetadata(meta): drop keys matching SENSITIVE_KEY; keep scalars/small arrays only.
// validateDetails(details): drop empties and de-duplicate by `field:code`.
// Both are defined in full in Chapter 6, Concepts 05 — they enforce the model invariants.
```

## The factory and native wrap

```ts
function toErrorObject(err: unknown, ctx?: Partial<AppErrorInit>): AppErrorClass {
  if (err instanceof AppErrorClass) return err;
  if (err instanceof Error) {
    return new AppErrorClass({
      code: "INTERNAL_UNEXPECTED",
      message: err.message || "Unexpected error",
      category: "unexpected",
      cause: err,
      ...ctx,
    });
  }
  return new AppErrorClass({
    code: "INTERNAL_UNEXPECTED",
    message: "An unexpected error occurred",
    category: "unexpected",
    metadata: { rawType: typeof err },
    ...ctx,
  });
}
```

## The wire shapes

### Internal log JSON (full fidelity)

```json
{
  "name": "PaymentError",
  "code": "PAYMENT_PROVIDER_TIMEOUT",
  "category": "payment",
  "severity": "warning",
  "recoverable": true,
  "retryable": true,
  "message": "Stripe capture timed out for order ord_123",
  "metadata": { "tenantId": "t_acme", "orderId": "ord_123", "provider": "stripe" },
  "correlationId": "01HQ8Z3K2M9Q4R7T1V6W8X0Y2Z",
  "operation": "checkout.capture",
  "timestamp": "2026-03-01T10:22:01.482Z",
  "cause": { "name": "FetchError", "message": "ETIMEDOUT" }
}
```

### Client JSON (safe projection)

The client shape is produced by `toClientJSON` below — same `code`, a public message, `details`
when present, `retryable`, and the `correlationId`, and nothing else:

```json
{
  "code": "PAYMENT_PROVIDER_TIMEOUT",
  "message": "We couldn't reach the payment provider. Please try again.",
  "retryable": true,
  "correlationId": "01HQ8Z3K2M9Q4R7T1V6W8X0Y2Z"
}
```

## The serializers

```ts
export function toLogJSON(e: AppErrorClass): Record<string, unknown> {
  return {
    name: e.name, code: e.code, category: e.category, severity: e.severity,
    recoverable: e.recoverable, retryable: e.retryable, message: e.message,
    details: e.details, metadata: e.metadata, correlationId: e.correlationId,
    operation: e.operation, timestamp: e.timestamp, stack: e.stackTrace,
    cause: e.cause instanceof Error
      ? { name: (e.cause as Error).name, message: (e.cause as Error).message }
      : undefined,
  };
}

export function toClientJSON(e: AppErrorClass): Record<string, unknown> {
  return {
    code: e.code,
    message: publicMessageFor(e.code),
    retryable: e.retryable,
    details: e.details?.map(({ field, code, message, meta }) => ({ field, code, message, meta })),
    correlationId: e.correlationId,
  };
}
```

## Worked example — Checkout capture

```ts
async function capture(order: Order, ctx: RequestContext): Promise<void> {
  try {
    await stripe.charges.create({ amount: order.total, currency: order.currency });
  } catch (native) {
    const appErr = toErrorObject(native, {
      code: classifyStripeError(native),     // e.g. PAYMENT_PROVIDER_TIMEOUT
      message: `Stripe capture failed for order ${order.id}`,
      category: "payment",
      metadata: { tenantId: ctx.tenantId, orderId: order.id, provider: "stripe" },
      correlationId: ctx.correlationId,
      operation: "checkout.capture",
    });
    throw appErr;
  }
}
```

## Key data / numbers

- **Payload budgets:** client error JSON ≤ 4 KB; log error JSON ≤ 8 KB; message ≤ 2 KB.
- **`details` cap:** 100 entries, with `truncated: true` when exceeded.
- **Cause depth cap:** 20.
- **Correlation ID:** 26-char ULID or 32-char hex; `schemaVersion` integer at durable boundaries.
- **Standard mapping anchors:** RFC 9457 (`type`/`title`/`status`/`detail`/`instance`), RFC 6901
  (JSON Pointer), W3C Trace Context (`traceparent`).

## Real-world use case — Acme SaaS

Acme adopted this spec across four services and a browser client. The `code` became the single
contract: the frontend maps `code → localized message` and `code → UI action`, the API layer maps
`code → HTTP status`, and the retry engine reads `retryable`. When a new `AGENT_TOKEN_LIMIT` code
was added by `AgentRun`, no consumer needed a code change — unknown codes fall back to a generic
message and a `500`/`400` default. Adding the code was a one-line registry edit plus a test.

## Trade-offs

| Choice | Pros | Cons | Recommendation |
| ------ | ---- | ---- | -------------- |
| Class vs plain object | Methods, `instanceof`, stacks | Slightly heavier | Use class internally, serialize to plain |
| Freeze vs mutable | Safety | Slight cost, no partial enrich | Freeze; wrap to enrich |
| Drop unsafe metadata | Never leaks | Silent loss | Log a dev warning when dropping |
| Allowlist vs blocklist keys | Safer | More upkeep | Allowlist where feasible |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Route every error through one factory | Construct ad-hoc error literals |
| Ship a client projection, not `JSON.stringify` | Send the full internal object |
| Keep `code` stable, messages changeable | Key UI/HTTP mapping on message text |
| Store IDs in metadata | Store `req`/`res`/user objects |

## Common mistakes

- **Two shapes** (a class and a literal) that drift apart.
- **`JSON.stringify(error)`** leaking or dropping `message`.
- **Client sees `stack`, `cause`, or raw metadata.**
- **Unbounded `details`/metadata** breaking log budgets.
- **Category typo** silently disabling category defaults.

## Checklist

- [ ] Is the interface the single source of truth for the shape?
- [ ] Does the constructor enforce all invariants?
- [ ] Are there distinct log and client serializers?
- [ ] Is the client output a safe projection?
- [ ] Are payload, detail, and cause-depth budgets enforced?
- [ ] Does every error path use the factory?

## Related

- [Model Invariants](../02-deep-dive/01-model-invariants.md)
- [Versioning the Internal Contract](../02-deep-dive/02-versioning-the-internal-contract.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../../07-error-classes-types-and-structured-results/README.md)
