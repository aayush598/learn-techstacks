# Expected Outcomes, Alternative Outcomes, and Compatible Contracts

> Part VII · Chapter 18 · Sections 18.12, 18.13, 18.20 · _Estimated reading time: 20 min_
> **Prerequisite:** [Ownership, Duplicates, Quota, and Entitlements](./04-access-duplicates-quota-entitlements.md)

## In one sentence

Most domain denials are **expected outcomes, not exceptions** — so you choose deliberately between
throwing and returning, model the full set of alternatives with **typed results/unions**, and
version the resulting vocabulary so **adding outcomes never breaks existing clients**.

## Why this matters in production

An exception-shaped denial forces every caller to wrap the call, loses exhaustiveness (the
compiler cannot list the ways a call can fail), and encourages the global-handler-to-`500`
failure mode. A result-shaped denial forces callers to *see* the alternatives — which is exactly
what you want when "already subscribed", "trial active", and "payment required" are all normal
answers. And because clients code against these outcomes forever, the contract must evolve
without breakage: a renamed outcome is a production incident with a release-note alibi.

## 18.12 — Expected outcomes vs exceptions

The decision table — use it per operation, not per language fashion:

| Criterion | Expected outcome (return) | Exception (throw) |
| --------- | ------------------------- | ----------------- |
| Documented in the API contract? | Yes | No |
| Caller can plausibly hit it in normal use? | Yes | No (it means *something is wrong*) |
| Examples | not found, duplicate, quota, entitlement, transition | invariant breach, missing config, translator bug |
| Retry semantics | Caller decides per code | Usually infra/policy layer |
| Language fit | Result/union/`Outcome` | throw/raise/`?` |

```ts
// Expected: visible in the signature — impossible to ignore.
type UpgradeOutcome =
  | { kind: "upgraded";           subscriptionId: string; effectiveAt: Instant }
  | { kind: "quota_exceeded";     requested: number; limit: number }
  | { kind: "payment_required";   invoiceId: string;     amountDue: Money }
  | { kind: "entitlement_missing"; capability: string;   entitledPlans: string[] }
  | { kind: "in_flight";          operationId: string;   retryAfterMs: number };

// Unexpected: throw — a bug or broken machinery, handled by boundaries (Ch. 10/15).
throw new InvariantViolation("seat_range", { seats: -1 });
```

Honest hybrid, because real code has both: **domain denials return; broken invariants and
infrastructure failures throw.** If your language has no `Result` (Java, older TS patterns),
either adopt a small `Outcome` type or throw *typed domain errors* — but then (a) register every
one, (b) never let them hit a global `catch → 500`, and (c) document them exhaustively. The
important property is **the caller can enumerate the denials**, by type or by registry.

## 18.13 — Modeling alternative outcomes

Three patterns, ascending in strength:

| Pattern | Shape | Exhaustiveness | Note |
| ------- | ----- | -------------- | ---- |
| **Coded error object** | `{code, category, details}` | Registry/docs only | Most flexible; weakest checks |
| **Union of outcomes** | `kind` discriminant | ✅ Compiler `switch` | ✅ Recommended for core flows |
| **Enum + payload map** | `OutcomeCode` + typed details | Partial | Compact RPC-friendly |

```ts
// Discriminated union: the compiler finds every missing branch in review, not in prod.
export function handleUpgrade(o: UpgradeOutcome): ReactNode | Action {
  switch (o.kind) {
    case "upgraded":           return showSuccess(o.effectiveAt);
    case "quota_exceeded":     return promptUpgrade(o.requested, o.limit);
    case "payment_required":   return redirectToBilling(o.invoiceId, o.amountDue);
    case "entitlement_missing":return upsell(o.capability, o.entitledPlans);
    case "in_flight":          return scheduleRetry(o.retryAfterMs);
    // no default: adding a new outcome breaks the build — that is the feature
  }
}
```

Design rules for alternatives:

1. **One outcome per distinct caller action.** If two branches render the same UI with the same
   action, they are one outcome with a detail flag.
2. **Details are typed per outcome**, not a generic bag — `quota_exceeded` always has
   `requested`/`limit`; a missing field is a compile error, not a support ticket.
3. **Transport mapping is per outcome-kind**, declared next to the union (registry: kind → code →
   status), so the domain file is self-documenting.
4. **Don't model infrastructure in the union** — `network_error` as an `UpgradeOutcome` member
   lies about the domain; that's the transport's retry layer (Ch. 27–29).

## 18.20 — Backward-compatible domain contracts

The vocabulary (`code`s, outcome kinds, statuses, detail fields) is a **public contract** equal in
stability to your endpoints:

| Change | Client effect | Policy |
| ------ | ------------- | ------ |
| Add new outcome kind / code | Old clients hit unknown kind | ✅ Allowed — clients must treat unknown as generic (see below) |
| Add optional detail field | None | ✅ Allowed |
| Remove/rename kind or code | Branch stops matching | ❌ Deprecate → dual-emit → sunset |
| Change status of an existing code | Client status logic breaks | ❌ Breaking; version the API instead |
| Split one code into two | Old clients conflate | ⚠️ Only with old code still emitted as alias |

Unknown-outcome tolerance on the client (write this into your SDK):

```ts
default:
  // Unknown outcome kind (server newer than client): degrade, don't crash.
  return showGenericError(o as { code?: string });
```

Registry mechanics that make this real:

```sql
-- one row per public outcome; tombstones are forever
INSERT INTO domain_codes(code, category, http_status, added_in, deprecated_at)
VALUES ('SEAT_QUOTA_EXCEEDED', 'QUOTA', 402, 'v3.2', NULL);
-- snapshot test: current API's emitted code set == registry's active set
```

Versioning discipline:

- **Semver the vocabulary with the API.** New code = minor. Meaning change = major (and usually
  you just add a new code instead — meaning changes are almost never necessary).
- **Codes are forever.** Retire with `deprecated_at`, keep emitting during the window, then stop
  emitting — never reuse.
- **Message text is not the contract** (17.20 applies domain-side too): reword freely; never
  rename the code "to match the new wording".
- **Contract tests** in CI: golden responses per outcome kind, plus "every outcome kind the
  domain can produce has a registry row and a test".

## Key data / numbers

- Union pattern: discriminant member (`kind`/`code`) required; `default` branch must degrade
  gracefully.
- Registry: `code` PK, `category`, `http_status`, `added_in`, `deprecated_at` (tombstone rows
  kept).
- Compatibility: add ✅ · rename ❌ · status change ❌ (major) · detail-add ✅.
- Unknown outcome on old clients → generic fallback UI + log the code; never a crash.

## Real-world use case — Acme SaaS

Acme's upgrade endpoint threw typed exceptions that the global handler rendered as `500` until
each was individually registered — a process that missed `IN_FLIGHT`, whose `500`s looked like
outages during every billing run. The conversion to a discriminated `UpgradeOutcome` union made
the missing case a **compile error** in the exhaustive `switch`, and the transport map gained the
`in_flight → 409 + retryAfterMs` row. Three releases later the team added `TRIAL_CONVERSION_QUEUED`
as a new kind: old SDKs (which had the documented unknown-kind fallback) showed the generic
message with the code, new SDKs rendered the specific spinner, and nobody cut an emergency
mobile release — exactly what an additive contract is for.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Typed unions/results | Exhaustiveness, self-documenting | Type churn on additions | ✅ Core flows with many branches |
| Coded error objects only | Flexible, RPC-friendly | No compiler help | Simple/low-variety denials |
| Exceptions for denials | Familiar | Hides alternatives; global-500 risk | Only when registry+handler discipline is absolute |
| Status/code registry with tombstones | Evolvable, auditable | Small governance cost | ✅ All public vocabularies |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return documented denials; throw only bugs/broken machinery | Throw for "already subscribed" |
| Use discriminated unions for core multi-outcome flows | Use one `BusinessException` for all denials |
| Give clients an unknown-kind fallback | `switch` without `default` in client SDKs |
| Tombstone codes; add instead of rename | Reuse a retired code for a new meaning |
| Version status/code changes as breaking | Silently move `402` → `409` in a patch |

## Common mistakes

- **"Generic BusinessException" base used as the actual catch** — all specificity lost at the
  first `catch (e: BusinessException)`.
- **Union with a `generic_error` member that everyone throws** — the union becomes decorative.
- **Renaming a code to match new UI copy** — breaks every branch; reword `message` instead.
- **Assuming clients read `details`** — old mobile clients may only know `code`; keep it stable
  and sufficient.

## Checklist

- [ ] Per-operation decision recorded: which denials return, which bugs throw.
- [ ] Core flows use typed outcomes; every branch has a compile-checked `switch`.
- [ ] Each kind maps to one registry row → one status.
- [ ] Client SDKs degrade gracefully on unknown kinds.
- [ ] Tombstones and deprecation windows enforced; CI snapshots the active code set.

## Related

- [Domain Services, Aggregates, and DDD](../02-deep-dive/01-domain-services-aggregates-and-ddd.md)
- [Framework Independence and Outcome Mechanics](../02-deep-dive/02-framework-independence-and-outcome-mechanics.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
