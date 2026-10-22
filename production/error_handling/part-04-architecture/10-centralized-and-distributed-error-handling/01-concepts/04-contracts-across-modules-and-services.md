# Error Contracts Across Modules and Services

> Part IV · Chapter 10 · Sections 10.14–10.17 · _Estimated reading time: 20 min_
> **Prerequisite:** [Limits of the Global Handler](./03-limits-of-a-global-handler.md)

## In one sentence

Whether your components live in **one deployable (modular monolith)** or **many (microservices)**,
what must stay uniform is the **error contract** — codes, envelope, correlation, and
compatibility rules — while implementations stay owned by each module or service.

## Why this matters in production

Error handling drifts along your deployment boundaries:

- In a **modular monolith (10.14)**, modules share a process but not a standard: `billing`
  throws `InvoiceError`, `projects` returns `{ ok: false }`, and the HTTP layer maps both with
  `instanceof` chains that grow per module.
- In **microservices (10.15)**, each service deploys independently, so a shared *library* is not
  enough — last month's deployed consumer still speaks yesterday's contract. A new code becomes
  an unhandled `500` on the caller, or worse, a silently swallowed one.
- Across **independently deployed components (10.16)** the failure mode is temporal: producer and
  consumer versions always differ somewhere.

The defense is to separate the **contract** (versioned, boring, tolerant) from the
**implementation** (owned locally, evolving freely) — and to demand **consistent contracts
(10.17)** on every hop.

## Core concept — the two deployment worlds

```text
 MODULAR MONOLITH (10.14)                  MICROSERVICES (10.15)
 ┌───────────────────────────┐            ┌─────────┐   ┌─────────┐
 │ module: billing           │            │ Checkout│──▶│ Billing │
 │ module: projects          │   HTTP/    │   API   │   │ service │
 │ module: webhooks          │  message   └────┬────┘   └────┬────┘
 │   ▲         ▲             │                 │             │
 │   └── shared error kernel ┘        same contract, deployed SEPARATELY
 │   one process, one registry        one registry artifact, N implementations
 └───────────────────────────┘        version tolerance is mandatory
```

| Concern | Modular monolith (10.14) | Microservices (10.15) |
| ------- | ------------------------ | --------------------- |
| Distribution of codes | one shared package/version | published registry artifact; services lag |
| Coupling risk | compile-time (good) but import spaghetti (bad) | runtime drift (worst) |
| Serialization | in-process objects | wire formats (HTTP envelope, message schema) |
| Tolerance required | low | high — unknown codes are normal |
| Governance | lint + code review | contract tests + deprecation windows |

## Modular monoliths (10.14)

The monolith's advantage is that the contract can be *compile-time*. Use it:

- **One error kernel package** (`@acme/errors`): the `AppError` type, the registry, `toProblem`,
  redaction. Modules depend on the kernel; the kernel depends on nothing.
- **Module-owned codes**: `billing` registers `INVOICE_FINALIZED`; nobody else may emit it.
  Registration is code (Chapter 8), reviewed by the owning module's team.
- **Cross-module calls speak the contract, not the classes** — a module raises/consumes
  registered codes, avoiding `instanceof` chains that couple internals.

## Microservices and independently deployed components (10.15–10.16)

Now the contract lives on the wire. Three rules make it survivable:

1. **Envelope stability.** Every service emits the same RFC 9457-shaped body plus a namespaced
   app code: `{ "type": ".../errors/PAYMENT_CARD_DECLINED", "status": 402, "code":
   "PAYMENT_CARD_DECLINED", "request-id": "..." }`. Field *additions* are non-breaking; field
   *removals* and semantic changes of existing codes are breaking (Chapter 49).
2. **Tolerant consumers.** A consumer must treat an **unknown code as its generic class**:
   `5xx`/`retryable` → retry policy; `4xx` → surface as-is; never crash, never `200`-swallow.
   ```ts
   const known = REGISTRY[e.code];
   if (!known) return classifyByStatus(e.status);   // unknown ≠ fatal
   ```
3. **Versioned identity for codes.** Codes are API surface: deprecate, don't delete; keep the
   old code answering with the same class (Chapter 8 deprecation, Chapter 49 contracts).

Message-based hops (queues, webhooks) add a fourth rule: **the failure of a hop is itself a
contract** — ack/retry/DLQ semantics must be documented per queue, not left to consumer defaults
(Chapter 33).

## Consistency across services (10.17) — the checklist that makes it true

| Property | Requirement |
| -------- | ----------- |
| Envelope | one schema, published, with compatibility rules |
| Code namespace | domain-prefixed, globally unique, registry-owned (`BILLING_*`, `CHECKOUT_*`) |
| Status mapping | identical code → status table everywhere (share the table, not the code) |
| Correlation | one ID propagates across every hop (headers + message attributes) |
| Retry semantics | retryable classes defined once per code; consumers honor `Retry-After` |
| Redaction | central policy applied at every producer; no service invents its own |
| Unknown codes | classified by status class, logged with producer name, never fatal by default |

## Key data / numbers

- RFC 9457 fixed members: `type`, `title`, `status`, `detail`, `instance` — the safe common
  denominator on the wire; app codes ride as an extension member.
- Compatibility heuristics: **adding** a response field or a new code = non-breaking;
  **removing/renaming** a code or changing its status = breaking (semver the contract, not just
  the client SDK).
- Recommendation: publish the registry as a **versioned artifact** (npm/PyPI package or a JSON
  schema with a version) and let services upgrade independently — assume **N-1 and N-2** versions
  coexist during any rollout.
- Correlation: `traceparent`/`trace-id` on HTTP, `correlationId` attribute on queue messages —
  pick one name per transport and never vary it.

## Real-world use case — Acme SaaS splits billing

Acme extracted `billing` from the monolith into a service. Month one: the new service returned
code `BILLING_PROVIDER_DEGRADED` (`503`) during a Stripe incident; the old monolith caller knew
only `BILLING_ERROR` and treated unknown codes as `500` **without retry** — so Stripe's
transient incident became a permanent-looking failure for customers.

The fix was contractual, not code-y: (1) the consumer was changed to classify unknown codes by
status class (`5xx` → its retry policy, honoring `Retry-After`); (2) the registry artifact gained
a deprecation path mapping old codes to their successors; (3) a contract test in CI replayed a
recorded set of error bodies against each consumer. Two weeks later the same provider incident
passed through with automatic retries and zero customer-visible failures.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Shared kernel + tolerant wire contract (recommended) | Local evolution, uniform behavior | Requires registry discipline | Any multi-module or multi-service system |
| Copy-paste error helpers per service | Zero coordination cost | Drift within months | Never beyond a spike |
| Shared *library* that must deploy in lockstep | Perfect consistency in theory | One team blocks all releases | Only inside a monolith |
| Full contract-first (schemas gate everything) | Strong guarantees | Slow iteration | Financial/regulated hops |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Publish one registry artifact with versions | Let each service invent its own codes |
| Make consumers tolerate unknown codes | Assume the producer upgraded first |
| Namespace codes by owning domain | Use generic `ERROR_500` across services |
| Propagate one correlation ID across hops | Generate a fresh ID per service |

## Common mistakes

- **Treating internal codes as free** — every code on a wire is public API; unregistered codes
  are incidents waiting for a version skew.
- **Consumers switching on message text** — text changes freely; codes are the contract.
- **"We'll version the whole envelope later"** — versioning that is not exercised is fiction;
  run the N-1 compatibility test in CI from day one.

## Checklist

- [ ] One published registry artifact; services consume versions, not copies.
- [ ] Unknown codes classify by status class on every consumer.
- [ ] Correlation ID crosses every hop unchanged.
- [ ] Deprecation keeps old codes answerable for at least one release window.
- [ ] A CI contract test replays representative error bodies against each consumer.

## Related

- [Limits of the Global Handler](./03-limits-of-a-global-handler.md)
- [Consistent Contracts Across Three Services](../03-practical-examples/02-consistent-contracts-across-services.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
