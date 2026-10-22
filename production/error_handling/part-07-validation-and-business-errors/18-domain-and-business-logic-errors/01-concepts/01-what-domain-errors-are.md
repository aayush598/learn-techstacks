# What Domain Errors Are — and How They Differ from Infrastructure

> Part VII · Chapter 18 · Sections 18.1, 18.11, 18.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 18 overview](../README.md)

## In one sentence

A **domain error** is a named, coded outcome saying a *well-formed* operation is unacceptable
under the *business's current state* — distinct from **validation errors** (bad input) and
**infrastructure errors** (broken machinery) — and it must keep that business meaning intact as it
crosses every layer to the client.

## Why this matters in production

If "the trial has not ended yet", "this project belongs to another workspace", and "the database
connection pool is exhausted" all leave your service as the same untyped `Exception`, three
catastrophes follow: the API maps all three to `500`; clients cannot distinguish "act
differently" from "retry later"; and support cannot triage without reading stack traces. Domain
errors are how the *meaning of the business* survives to the edge — the whole point of the
taxonomy (Part II) and translation (Ch. 16) machinery.

## 18.1 — The definition

A domain error has four properties:

| Property | Meaning | Example (`Checkout`) |
| -------- | ------- | -------------------- |
| **Business meaning** | A rule of the product was evaluated and said no | Seat quota rule said no |
| **Expected** | Documented behavior, not a defect | Clients branch on it |
| **Coded** | Stable machine identifier + category | `SEAT_QUOTA_EXCEEDED`, `BILLING` |
| **Stateful** | Depends on data/time/other systems | Needs subscription + seat count |

Contrast with the other two families:

```text
 VALIDATION (Ch. 17)        DOMAIN (this chapter)        INFRASTRUCTURE (Ch. 22+)
 ───────────────────        ────────────────────         ────────────────────────
 "your payload is wrong"    "the world says no"          "our machinery failed"
 needs: the request         needs: state, time, tenant   needs: nothing from you
 owner: DTO/schema          owner: domain service        owner: platform/ops
 example: seats="five"      example: quota reached       example: DB pool timeout
 status: 422                status: 409/403/402/…        status: 500/503/504
 retry: never helps         retry: sometimes helps       retry: usually helps
```

> ⚠️ **Hazard.** The dangerous middle case: an infrastructure error *disguised* as a domain error
> (mapping `SQLSTATE 23514` check-violation to `422 BUSINESS_RULE` when the rule lives in a DB
> `CHECK` you forgot to enforce in the domain) — and the reverse, a domain error laundered into
> `500` because nobody translated it.

## Naming the taxonomy (a starter vocabulary)

Group codes by *what the caller must do differently*:

| Category | Codes (examples) | Caller action |
| -------- | ---------------- | ------------- |
| CONFLICT | `ALREADY_EXISTS`, `STATE_CONFLICT`, `CONCURRENT_MODIFICATION` | Refresh; do not blind-retry |
| FORBIDDEN | `NOT_OWNER`, `INSUFFICIENT_ROLE`, `ENTITLEMENT_MISSING` | Different account/plan, or stop |
| NOT_FOUND | `RESOURCE_NOT_FOUND`, `PARENT_NOT_FOUND` | Fix reference |
| PAYMENT/BILLING | `INSUFFICIENT_FUNDS`, `INVOICE_OPEN`, `PAYMENT_METHOD_REQUIRED` | Pay / update method |
| QUOTA | `SEAT_QUOTA_EXCEEDED`, `STORAGE_QUOTA_EXCEEDED` | Upgrade or free capacity |
| PRECONDITION | `TRIAL_NOT_ENDED`, `VERIFICATION_REQUIRED`, `DEPENDENCY_PENDING` | Complete the pre-step |
| LIFECYCLE | `INVALID_TRANSITION`, `ALREADY_CANCELED`, `JOB_ALREADY_RUNNING` | Re-read state |

(These categories are the same ones Ch. 4/8 registered; extend, don't fork.)

## 18.11 — Domain vs infrastructure

The test is **"did the business say no, or did the machinery fail?"**

| Question | Domain | Infrastructure |
| -------- | ------ | -------------- |
| Would it still happen with a healthy DB/provider? | Yes | No |
| Does a product manager recognize it? | Yes ("that's by design") | No |
| Is retrying the same request the fix? | Rarely/never | Often |
| Who is on call when it spikes? | Nobody — it's product behavior | The owning team |
| HTTP mapping | 4xx | 5xx (mostly) |

Concrete confusions and their resolutions:

```text
Unique email already registered     → domain? both! → see 18.7: the *rule* is domain,
                                        the *detection* is a DB 23505 translated at the
                                        repository boundary (Ch. 16)
"Cannot cancel: another payment in flight" → domain (LIFECYCLE/CONFLICT)
"Payment provider timed out"        → infrastructure (DEPENDENCY, transient)
"Plan does not include audit log"   → domain (ENTITLEMENT_MISSING)
"Feature flag service unreachable"  → infrastructure; degrade (Ch. 30)
```

Ownership follows the classification: domain errors are owned by the **domain team** and appear in
the **error registry**; infrastructure errors are owned by **platform/integration** code and
appear in the **translation tables**.

## 18.18 — Preserving domain meaning

Meaning dies in translation unless you fight for it. Three loss patterns:

| Loss | Example | Fix |
| ---- | ------- | --- |
| **Collapse** | Every 409 becomes `CONFLICT` with no code | Keep specific codes; category is metadata, not identity |
| **Genericization** | `INSUFFICIENT_FUNDS` → `CHECKOUT_FAILED` | Map to the precise code; details carry amounts |
| **Infra laundering** | Domain error caught by a global `catch → 500` | Register the code → status map; global handler consults it |

The preservation contract for every hop:

```ts
// Domain code (no HTTP anywhere):
class InsufficientSeats extends DomainError {
  readonly code = "INSUFFICIENT_FUNDS" as const;   // typo-proof: literal type
  readonly category = "PAYMENT";
  constructor(readonly requested: number, readonly available: number, cause?: unknown) {
    super(cause);
  }
}

// Boundary translation (Ch. 16/19): category + registry decide 402, body carries details.
// { "code": "INSUFFICIENT_FUNDS", "status": 402,
//   "detail": "This change requires 30 seats; 12 are available.",
//   "requested": 30, "available": 12 }
```

Rules:

- **The code travels with the cause**, never replaces it (debuggability).
- **Structured details travel with the code** (`requested`, `available`) so clients can render
  "30 needed, 12 available" without parsing prose.
- **The domain never learns the status number** — the registry maps category+code → HTTP/gRPC.

## Key data / numbers

- Typical domain-error HTTP mappings (full table in the [reference](../05-reference/README.md)):
  `CONFLICT→409`, `NOT_FOUND→404`, `FORBIDDEN→403`, `PAYMENT→402`, `QUOTA→409 or 429` (pick one
  policy per family), `PRECONDITION→409 or 422`, `LIFECYCLE→409`.
- gRPC counterparts: `ALREADY_EXISTS=6`, `FAILED_PRECONDITION=9`, `PERMISSION_DENIED=7`,
  `NOT_FOUND=5`, `RESOURCE_EXHAUSTED=8`, `ABORTED=10`.
- Retry classification: **domain errors are permanent for the identical request** — the caller
  must change something (state, plan, payload) first.

## Real-world use case — Checkout

`Checkout`'s upgrade path threw `new Exception("upgrade failed")` for three distinct realities:
seat quota exceeded, plan not entitled to SSO, and a concurrent upgrade already running. All
became `500`s; the client showed "something went wrong" and support escalated all three to
engineering. After modeling three coded domain errors (`SEAT_QUOTA_EXCEEDED` → `402` with
`requested`/`available`; `ENTITLEMENT_MISSING` → `403`; `CONCURRENT_MODIFICATION` → `409`), the
client rendered an upgrade prompt, an upsell page, and an automatic single retry respectively.
Engineering escalation for these paths fell to zero — the errors were *supposed* to happen.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Typed domain error classes | Exhaustive handling, structured details | Class count grows | ✅ Core flows |
| Code + data map (`code`, `details`) | Compact, serializable | Weaker compile-time checks | High-volume, uniform errors |
| Exceptions for all denials | Familiar | Loses "expected" framing; retry misuse | Never for documented outcomes |
| Result/union types for denials | Forces handling | Noise for rare paths | Combinatorial outcomes (18.13) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every denial a code, category, and details | Throw bare strings for business outcomes |
| Classify domain vs infrastructure before mapping | Map pool exhaustion to a business code |
| Carry structured details (`requested`/`available`) | Encode data in the message sentence |
| Keep HTTP status numbers out of domain code | `throw new DomainError(409)` |

## Common mistakes

- **`NOT_FOUND` for permission denials** without a deliberate existence-hiding policy (see 18.5).
- **One `CONFLICT` code for everything 409** — clients can't branch; support can't triage.
- **Catching domain errors in infrastructure middleware and defaulting to `500`** because the
  code wasn't in the registry.
- **Encoding tenant/plan names in the code** (`PLAN_PRO_MISSING`) — codes identify rules, not
  values; values go in `details`.

## Checklist

- [ ] Every "no" in your domain maps to a registered code + category.
- [ ] Domain vs infrastructure classification is documented per code.
- [ ] Structured details accompany codes; messages stay replaceable.
- [ ] No HTTP/gRPC numbers in domain modules (CI grep).
- [ ] Registry maps each code to exactly one status per API version.

## Related

- [Invariants and Business Rules](./02-invariants-and-business-rules.md)
- [Outcome Modeling and Contracts](./05-outcome-modeling-and-contracts.md)
- [Value Object and Domain Error Examples](../03-practical-examples/01-value-object-money-and-domain-errors.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
