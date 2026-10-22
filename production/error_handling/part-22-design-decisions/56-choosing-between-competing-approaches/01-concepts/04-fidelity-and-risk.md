# Fidelity and Risk: Wrapping vs Preserving, Strict vs Permissive, Abstraction vs Indirection

> Part XXII · Chapter 56 · Sections 56.8, 56.13, 56.17, 56.18 · _Estimated reading time: 24 min_
> **Prerequisite:** [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md), [Chapter 3 — Error-Handling Requirements for a SaaS Product](../../../part-01-foundations/03-error-handling-requirements-for-saas/README.md)

## In one sentence

**Preserve before you improve, validate strictly where you do not own the data, and scale your
engineering effort to the blast radius** — because a wrong page title costs nothing and a
wrong payment costs a customer.

## Why this matters in production

These four subsections share one theme: **fidelity**. How much of the original failure survives
your handling, how much of the input you accept, and how much engineering you spend.

Each has a characteristic production failure:

- **Unfaithful wrapping.** The wrapper is fine; the *cause* was dropped. At 3 a.m. you have a
  `500` and a request ID and nothing else — and the vendor's own request ID, which was the
  only way to find the attempt in the Stripe dashboard, is gone.
- **Permissive input.** You accepted a malformed `amount` because the field was "usually
  fine", and a `NaN` became `0` and a `0` became a free subscription.
- **Abstraction without evidence.** A shared "error framework" now has 12 configuration
  options, and the on-call engineer spends 30 minutes configuring it during an incident.
- **Uniform effort.** A `404` for a missing avatar and a `500` for a corrupted ledger get the
  same (or the same lack of) attention. One of them costs real money.

## Core concept

### 56.8 — Wrapping vs preserving

"Wrapping" means catching a low-level error and re-throwing a higher-level one. It is the
right instinct — but the difference between *wrapping* and *replacing* is the whole game.

```text
  ❌ Replacing (destroys the original)      ✅ Wrapping (preserves the original)
  new Error("Payment failed")               new CheckoutError({
                                              code: "PAYMENT_PROVIDER_UNAVAILABLE",
                                              step: "charge",
                                              cause: originalError,     ← the original
                                            })
  Original stack: gone                       Original stack: cause.stack
  Vendor code: gone                          Vendor code: cause.vendorCode
  Request ID: gone                           Request ID: cause.requestId
  Retryable?: unknown                        Retryable?: carried explicitly
```

**The preservation contract.** When you translate or wrap, these six things must survive:

| Field | Why it matters | Where it lives |
| ----- | --------------- | -------------- |
| Original error object | Stack trace, vendor detail | `cause` |
| Vendor error code | Only the vendor knows the precise meaning | `cause.vendorCode` / `vendorCode` |
| Vendor request ID | The only handle for support/sales inquiries | `vendorRequestId` |
| Retryability | Decides the whole recovery policy | explicit field, not inferred later |
| Operation / step | Which part of the operation failed | explicit field |
| Correlation ID | Ties the failure to the request | inherited, never regenerated |

The anti-pattern: the wrapper adds a nice message and *reconstructs* the vendor code by
string-matching the message:

```ts
// ❌ Parsing a message to recover information that was available in the original.
if (err.message.includes("card was declined")) return new PaymentError("declined");
```

This is fragile (vendor wording changes), lossy (no request ID), and slow (regex on every
failure). Read the structured fields instead.

**When to wrap at all.** Wrap when you are **adding domain meaning**. Do not wrap when you are
only adding a human message — that can be done at the boundary, once.

### 56.13 — Strict vs permissive

| | Strict | Permissive |
| - | ------ | ---------- |
| Unknown field | Reject (`422`) | Ignore |
| Wrong type | Reject | Coerce |
| Out-of-range value | Reject | Clamp |
| Missing optional field | Default | Reject |
| Extra nesting depth | Reject | Accept |

The rule that resolves nearly every case:

> **Be strict at trust boundaries where you do not own the data; be permissive at internal
> boundaries where you do.**

Concretely:

- **HTTP request bodies** → strict. You do not own the client. Unknown fields are rejected
  (or ignored but *recorded*), types are checked, ranges are enforced. Answer `422` with a
  field-level list.
- **Rows from your own Postgres** → permissive about *shape evolution* (a nullable column that
  became nullable), strict about *semantics* (an amount that must be positive).
- **Vendor API responses** → strict about structure (missing required field → treat as an
  upstream error, not as `undefined`), permissive about extra fields (ignore them).
- **Your own internal config** → strict at boot: a missing required value should crash the
  process at startup, not at first use.

The failure mode to avoid is **permissive parsing that silently changes semantics**. `Number("")`
is `0`; `Number(" 12 ")` is `12`; `parseInt("12abc")` is `12`. A monetary amount that becomes
`0` because the string was empty is a free product.

### 56.17 — Abstraction vs indirection

An abstraction is a layer that **hides variation behind a stable concept**. An indirection is a
layer that **only moves work around**. The difference is whether the layer removes decisions
from the caller or adds steps to the caller.

| | Abstraction | Indirection |
| - | ----------- | ----------- |
| The caller writes | `payments.charge(...)` | `httpClient.request(...)` + 40 lines of plumbing |
| The layer decides | Something meaningful (retry, timeout, translation) | Something trivial (URL building) |
| Value | Removes a decision | Hides a name |
| Symptom | "I don't need to know how this works" | "I have to know how this works anyway" |

The four-question test:

1. **Does the layer hide a decision?** If the caller still has to decide timeouts, retries,
   and error mapping, the layer is not doing the job.
2. **Are there 3+ real consumers?** One consumer is a private helper, not an abstraction.
3. **Is the concept product-neutral?** If it embeds one team's assumptions, it becomes
   everyone's constraint.
4. **Can a new engineer use it without reading it?** If it has 12 options, they cannot.

The cost model is developed in
[`02-deep-dive/01-abstraction-vs-indirection-cost.md`](../02-deep-dive/01-abstraction-vs-indirection-cost.md).

### 56.18 — Policies by business risk

This is where the whole chapter pays out. **The error-handling policy of an operation is a
function of the blast radius of getting it wrong**, not of the technical category of the error.

Risk tiers used at Acme SaaS:

| Tier | Meaning | Examples | Policy |
| ---- | ------- | -------- | ------ |
| **T0 — Cosmetic** | The user notices briefly; no state changes | Avatar load fails | Degrade; no retry (cache it instead); no alert |
| **T1 — Convenience** | Feature unusable; no data loss | AI summary unavailable; export preview fails | Degrade or retry (bounded); alert only on sustained rate |
| **T2 — Workflow** | A user's work is blocked but recoverable | Export job fails; webhook processing fails | Retry with backoff; then DLQ; notify the owner |
| **T3 — Financial** | Money, entitlement, or contract is affected | Payment capture; subscription activation; refund | Fail fast unless idempotent-retryable; compensate; page on failure |
| **T4 — Integrity / security** | Data correctness or trust is at stake | Ledger mismatch; cross-tenant read; audit log gap | Terminate or quarantine; always alert; never auto-recover |

Every error code should carry its tier, and the tier drives:

- **Retry**: allowed from T0–T2; only with idempotency from T3; never from T4.
- **Fallback**: allowed from T0–T1; only with an explicit marker; never silently from T3+.
- **Compensation**: mandatory for T3 side effects; forbidden for T4 (compensating an integrity
  failure can hide it).
- **Termination**: only T4.
- **Alerting**: T0 → no alert; T1 → dashboard; T2 → ticket/notification; T3 → page; T4 → page
  + incident.

> ⚠️ **Hazard.** The most common tiering error is putting a **financial** operation in T1
> because "the retry usually works". A retry that doubles a charge is not a degraded feature;
> it is a T3 incident.

## How it works (mechanics)

### A lossless translation

```ts
// ✅ Adapter: vendor error -> domain error, nothing lost.
export function fromStripeError(err: unknown, ctx: StripeContext): CheckoutError {
  if (!isStripeError(err)) {
    // Unknown shape: keep it as the cause, classify conservatively.
    return new CheckoutError({
      code: "PAYMENT_PROVIDER_UNAVAILABLE",
      category: "dependency",
      retryable: true,
      step: ctx.step,
      correlationId: ctx.correlationId,
      safeContext: { provider: "stripe" },
      cause: err,                                   // 56.8: original preserved
    });
  }

  switch (err.type) {
    case "card_error":
      return new CheckoutError({
        code: err.decline_code === "insufficient_funds"
          ? "PAYMENT_INSUFFICIENT_FUNDS"
          : "PAYMENT_CARD_DECLINED",
        category: "business",
        retryable: false,
        step: ctx.step,
        correlationId: ctx.correlationId,
        safeContext: { provider: "stripe" },
        vendorCode: err.code,                        // e.g. "card_declined"
        vendorRequestId: err.request_id,             // search Stripe by this
        cause: err,                                  // stack preserved
      });
    case "rate_limit_error":
      return new CheckoutError({
        code: "PAYMENT_PROVIDER_RATE_LIMITED",
        category: "dependency",
        retryable: true,
        step: ctx.step,
        correlationId: ctx.correlationId,
        retryAfterSeconds: Number(err.retry_after ?? 1),
        vendorCode: err.code,
        vendorRequestId: err.request_id,
        cause: err,
      });
    default:
      return new CheckoutError({
        code: "PAYMENT_PROVIDER_UNAVAILABLE",
        category: "dependency",
        retryable: true,
        step: ctx.step,
        correlationId: ctx.correlationId,
        safeContext: { provider: "stripe" },
        vendorCode: err.code,
        vendorRequestId: err.request_id,
        cause: err,
      });
  }
}
```

Note what is **not** here: no message parsing, no `err.message.includes(...)`, no dropped
request ID, no `retryable` guessed from a string.

### Strict input validation with a field-level report

```ts
// ✅ Strict at the trust boundary; one error per field, capped.
const MAX_FIELD_ERRORS = 20;

export function parseCheckoutRequest(body: unknown): Result<CheckoutInput, FieldError[]> {
  const issues: FieldError[] = [];

  const raw = asRecord(body);
  if (!raw) return err([{ field: "", code: "BODY_MUST_BE_OBJECT" }]);

  const planId = asString(raw.planId);
  if (!planId) issues.push({ field: "planId", code: "REQUIRED" });
  else if (!PLAN_ID_PATTERN.test(planId)) issues.push({ field: "planId", code: "INVALID_FORMAT" });

  const seats = asInteger(raw.seats);
  if (seats === undefined) issues.push({ field: "seats", code: "REQUIRED" });
  else if (seats < 1 || seats > 500) issues.push({ field: "seats", code: "OUT_OF_RANGE" });

  const amount = asMoneyMinor(raw.amountMinor);
  if (amount === undefined) issues.push({ field: "amountMinor", code: "INVALID" });

  if (issues.length > 0) return err(issues.slice(0, MAX_FIELD_ERRORS));
  return ok({ planId: planId!, seats: seats!, amountMinor: amount! });
}
```

The HTTP layer turns this into `422 Unprocessable Entity` with an `errors` array — and the
transport is the only place that knows that.

### Risk tier as registry data

```ts
// ✅ The tier travels with the code, so policies can be derived from it.
export type RiskTier = "T0" | "T1" | "T2" | "T3" | "T4";

export type RegistryEntry = {
  code: string;
  httpStatus: number;
  retryable: boolean;
  riskTier: RiskTier;
  publicTitle: string;
  degradeAllowed: boolean;
  alert: "none" | "dashboard" | "notify" | "page";
};
```

With that in place, a policy function can be derived rather than hand-written per call site:

```ts
export function maxAttempts(entry: RegistryEntry): number {
  if (!entry.retryable) return 0;
  switch (entry.riskTier) {
    case "T0": return 1;
    case "T1": return 2;
    case "T2": return 3;
    case "T3": return 3;   // only when the operation is idempotent
    case "T4": return 0;
  }
}
```

## Worked example — `AgentRun` (Acme SaaS)

`AgentRun` executes an LLM tool-calling loop. Three decisions from this group decide its
behavior under provider trouble.

**56.8 — preserving.** The LLM provider returns a body like
`{"error":{"message":"Rate limit reached","type":"rate_limit_error","request_id":"req_9f2"}}`.
Acme's first adapter did:

```ts
// ❌ The request_id — the only handle for support — is gone.
throw new Error(`LLM call failed: ${res.body.error.message}`);
```

After the fix, the provider's `request_id` and `type` are carried into
`AGENT_PROVIDER_RATE_LIMITED` as `vendorRequestId` and `vendorCode`, and the original response
body is the `cause` (redacted for PII before it is stored — Chapter 36).

**56.13 — strict.** The model may return a tool call with missing arguments. Acme validates
the tool arguments against the tool schema and rejects the call as
`AGENT_TOOL_ARGS_INVALID` (permanent, never retried — the model will produce the same thing
again). The permissive alternative — calling the tool with `undefined` arguments — produced
tool calls that silently deleted records.

**56.18 — tiering.** The loop has three operations with different tiers:

| Operation | Tier | Policy |
| --------- | ---- | ------ |
| Summarize a task description | T1 | Degrade (no summary card); retry once on `429` honoring `Retry-After` |
| Call a tool that writes to the DB | T3 | Fail the run; compensate the partial write; page on failure |
| Refresh the provider OAuth token | T2 | Retry with backoff; the run resumes from the last checkpoint |

The result: during a provider rate-limit incident, Acme's runs *slowed down* instead of
collapsing, and the tool writes that failed were rolled back rather than left half-applied.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Fields that must survive a translation | 6 | cause, vendor code, vendor request ID, retryable, operation, correlation ID |
| Max wrappers between origin and handler | 2 | Each wrapper is a place to drop a field |
| Max field-level validation errors in a response | 20 | Cap the array; summarize the rest |
| Validation status | `422` | `400` only for malformed syntax |
| Error-detail length | ≤ 200 chars | Long details belong in logs |
| Risk tiers | 5 (T0–T4) | Fewer merges distinct policies; more adds ceremony |
| Max retry attempts by tier | T0:1, T1:2, T2:3, T3:3 (idempotent only), T4:0 | Derived, not hand-written |
| Alerting by tier | T0 none, T1 dashboard, T2 notify, T3 page, T4 page+incident | Tier drives the alert, not the category |
| Abstraction promotion threshold | 3 real consumers | See 56.12 and the deep dive |
| Config options in a shared error abstraction | ≤ 10 | Above that, it is a framework |
| `Retry-After` on a `429` from your own API | seconds (integer) | Also accept HTTP-date per RFC 9110 |

## Real-world use case — `WebhookIngest` (Acme SaaS)

`WebhookIngest` receives Stripe webhooks and must be strict about security, tolerant of
version drift, and precise about the risk of each failure.

**Strict where Acme owns the contract.** The signature header must be present and within
Stripe's tolerance window; the event type must be one Acme handles; the payload must satisfy
the event schema. A missing `Stripe-Signature` header → `400` with `WEBHOOK_SIGNATURE_MISSING`
(permanent, never retried). A payload field of the wrong type → `422` with field details.

**Permissive where Acme does not own the data.** Stripe adds new fields to events
constantly. Acme's parser accepts unknown fields and ignores them — but records the unknown
field names so a schema-drift alert can fire if a *known* field changes type. This is the
"permissive in the shape, strict in the semantics" rule from 56.13.

**Preserving.** When a webhook fails inside Acme's processing, the error carries the
`Stripe-Event-Id` as the `vendorRequestId`, the event type, and the Acme `correlationId`.
Support can find the exact event in Stripe's dashboard by ID — which was impossible when the
original implementation flattened the error to a string.

**Tiering.** The tier of a webhook error depends on what the webhook *does*:

| Event | Effect | Tier | Policy |
| ----- | ------ | ---- | ------ |
| `invoice.payment_succeeded` | Financial | T3 | Fail fast; no retry of Acme's own processing; but ack only after commit |
| `customer.subscription.updated` | Entitlement | T3 | Idempotent upsert; safe to retry |
| `invoice.created` | Informational | T1 | Degrade (no invoice email); ack and drop |

The dangerous case was `invoice.payment_succeeded`: Acme's original code caught the processing
error and still returned `200`, so Stripe never retried — and the subscription was never
activated. The fix was to acknowledge **only after the effect is durable**, and to return
`500` (so Stripe retries) when the effect is not durable. Since Stripe retries for up to
**3 days** on non-2xx, and Acme's handler is idempotent, this is safe.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Wrapping with context | Domain meaning, readable logs | Extra layers can drop fields | When adding domain meaning |
| Preserving the raw error | Nothing lost | Leaks vendor internals into logs | Always, as `cause` (redacted) |
| Strict validation | Catches errors early | More client breakage on version drift | Trust boundaries you do not own |
| Permissive validation | Tolerates drift | Silently wrong semantics | Vendor payloads, internal config |
| Abstraction with 3+ consumers | Real reuse, one place to change | Costs a package boundary | Once the threshold is met |
| Indirection layer | Organizes code | Adds a name and a hop | Only if it hides a decision |
| Risk-tiered policies | Spends effort where it matters | Requires classifying every code | Every codebase with a tiered customer base |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve `cause`, vendor code, and vendor request ID | Rebuild the vendor code from the message |
| Wrap only to add domain meaning | Wrap at every layer for readability |
| Validate strictly at untrusted boundaries | Accept `Number(body.amount)` without checking |
| Ignore unknown vendor fields but record their names | Reject a Stripe event because it gained a field |
| Give every code a risk tier | Apply one retry policy to all errors |
| Derive retry/fallback/alert rules from the tier | Hand-write a policy per call site |
| Promote an abstraction at 3 real consumers | Abstract the first use |

## Common mistakes

- **String-matching to recover structure.** `err.message.includes("declined")` breaks when the
  vendor changes wording, and it drops the request ID even while it works.
- **Permissive coercion of money and identifiers.** `Number("")` is `0`; `parseInt("12abc")`
  is `12`. Coerce with validation, not with `Number`.
- **Uniform effort across tiers.** Treating a payment failure like a missing avatar means
  either noisy pages or missed incidents.
- **Abstraction by extraction.** Moving one function into a `packages/` folder is not reuse;
  it is a new module with a versioning obligation.
- **Degrading without a marker.** The user cannot tell that the number on the screen is
  stale, and neither can the operator counting degraded responses.

## Checklist

- [ ] Every translation preserves cause, vendor code, vendor request ID, retryability,
      operation, and correlation ID.
- [ ] No classification reads `err.message`.
- [ ] Validation at trust boundaries returns `422` with a capped field-level list.
- [ ] Coercion never silently changes semantics (money, IDs, timestamps).
- [ ] Every error code has a risk tier, and retry/fallback/alert rules derive from it.
- [ ] Shared abstractions have 3+ real consumers and ≤ 10 configuration options.
- [ ] Degraded responses are explicitly marked.

## Related

- [Structure and Ownership (56.2, 56.3, 56.9–56.12)](./02-structure-and-ownership.md)
- [The Abstraction Cost Model](../02-deep-dive/01-abstraction-vs-indirection-cost.md)
- [Risk-Based Policy Selection](../02-deep-dive/02-risk-based-policy-selection.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
