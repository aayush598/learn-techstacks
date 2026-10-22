# Contract Surfaces and Stability Guarantees

> Part XIX · Chapter 49 · Sections 49.1–49.6 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)

## In one sentence

An **error contract** is the set of promises a producer makes about the failures it emits, and
each contract lives on a **surface** — internal, module, service, backend↔frontend, or public
API — whose **stability tier** decides how freely you may change it.

## Why this matters in production

Most teams have exactly one error-handling style and apply it everywhere: a `try/catch` around a
helper in the same process, and a public API response, get the same treatment. That is a
category error. A helper's error message can change every Tuesday; a public API's error code
cannot change without a migration plan for people you have never met.

The cost of ignoring the distinction is not "we broke a client". It is:

- **Over-engineering** internal code paths with versioning machinery nobody asked for.
- **Under-engineering** public surfaces, where a breaking change ships on a Friday and a partner
  integration silently degrades.
- **No shared vocabulary** between teams, so each invents its own code names for the same
  condition — the exact problem the registry solved, reintroduced at the contract level.

## Core concept — what an error contract actually contains

A contract is not the code list. It is **four promises**:

| Promise | Question it answers | Example |
| ------- | ------------------- | ------- |
| **Vocabulary** | What conditions exist and under which code? | `PAYMENT_CARD_DECLINED` means "issuer declined the card" |
| **Shape** | What fields are present and what are their types? | `code`, `status`, `detail`, `instance`, `errors[]` |
| **Semantics** | What does a given code *mean* for retry, idempotency, and user action? | `retryable: true`, `clientAction: "retry"` |
| **Stability** | Which of those may change, and how? | "Codes are append-only; removing one needs a 90-day window" |

A product with a registry but no stability promise has a vocabulary, not a contract. Consumers
still have to guess what they may rely on.

## The five surfaces (49.1–49.5)

### 49.1 — Internal vs external

**Internal** errors never cross a process boundary. **External** errors do. The dividing line
is not "is it user-facing" — it is **"is there a consumer I do not control?"**

| Surface | Who consumes it | Do they control the version? | Contract needed? |
| ------- | --------------- | --------------------------- | ---------------- |
| Internal (same process) | Your own code | Yes — you deploy both sides | No, but keep it typed |
| Module / package | Other teams, maybe external users | Via semver, not directly | Yes, at package level |
| Service (internal HTTP/gRPC) | Another team in your org | Sometimes (independent deploys) | Yes, informal is fine |
| Backend ↔ frontend | Your web/mobile app | No — the app outlives the deploy | Yes, versioned |
| Public API | External developers, partners | No | Yes, published + versioned |

> ⚠️ **Hazard.** "Internal" and "public" are not binary, and "our own frontend" is not
> internal. A mobile app v3.0, installed on a customer's phone, is a **public** consumer with a
> 12-month support tail. Design the frontend contract as if it were public, because it is.

### 49.2 — Module contracts

A published package (`@acme/errors`) exposes error classes, codes, and types to consuming
teams. Its contract is governed by **semver**:

- **MAJOR** — a code is removed or repurposed; an error class's hierarchy changes such that
  `instanceof` checks break; a required field is added.
- **MINOR** — new codes, new error classes, new optional fields.
- **PATCH** — message wording, documentation, internal implementation of a formatter.

The practical rule for modules: **export the vocabulary, not the implementation**. Consumers
should depend on `ErrorCode` (a union of string literals), not on a class hierarchy that
rearranges itself.

```ts
// Module contract: the union type is the contract.
export type ErrorCode =
  | "PAYMENT_CARD_DECLINED"
  | "PAYMENT_CARD_EXPIRED"
  | "EXPORT_STORAGE_UNAVAILABLE"
  | "INTERNAL_UNEXPECTED";

// Consumers branch on the union, so a new code is a compile error they must handle —
// which is exactly the signal you want for a MAJOR change.
export class AcmeError extends Error {
  constructor(
    readonly code: ErrorCode,
    readonly status: number,
    options?: { cause?: unknown },
  ) {
    super(code, options);
  }
}
```

### 49.3 — Service contracts

An internal service (HTTP, gRPC, or an event schema) emits errors that another team's service
consumes. Two rules make this tractable:

- **Translate at the boundary, then hold the contract.** The service maps its internal
  `DB_UNIQUE_VIOLATION` to a domain code (`PLAN_ALREADY_EXISTS`) and that domain code is the
  contract. The consumer never sees the database layer.
- **Version the service, not each error.** A service on API v2 may change its error mapping
  freely because the whole v2 surface is versioned; carving out per-error versions inside one
  service version is how contracts become unmanageable.

```text
Service v1  →  409 + code PLAN_ALREADY_EXISTS   (frozen; v1 lives)
Service v2  →  409 + code SUBSCRIPTION_ALREADY_ACTIVE
               consumers migrate at the service-version level, not per error
```

### 49.4 — Backend ↔ frontend contracts

The first-party web and mobile clients are the most common unowned contract surface. They
consume the HTTP error envelope and branch on `code`.

The rules that keep this surface stable:

- **Codes are the branch key.** The frontend never branches on `title` or `detail`.
- **Unknown codes degrade to a generic state**, never an exception. The frontend must render
  something for a code released after its build.
- **New fields are additive.** A new optional field in the error body is safe; removing or
  retyping one is a breaking change.
- **The frontend owns its fallback.** The backend must not assume the frontend knows the code.

### 49.5 — Public API contracts

This is the surface with the longest tail. A public API's error contract is **published,
versioned, and supported**.

| Obligation | Why it exists |
| ---------- | ------------- |
| A published error catalogue | Developers must be able to read what can go wrong |
| A stated stability policy | Developers must know what they may rely on |
| A deprecation policy with windows | Developers must know how much notice they get |
| A sunset/announcement mechanism | Developers must be able to plan |
| An "unknown code" guarantee | Developers must know a new code will not break them |

A public API's error contract is usually a separate document from the endpoint reference,
because it has a different lifecycle: endpoints are added and removed per release, but the
error contract changes only on **major** boundaries.

## 49.6 — Stability guarantees

Assign each surface a tier. The tier determines the change process, not the code style.

| Tier | Surfaces | Guarantee | Change requires |
| ---- | -------- | --------- | --------------- |
| **T0 — Unstable** | Internal helpers, internal-only scripts | Nothing is guaranteed; any change is allowed | Nothing |
| **T1 — Internal-stable** | Service contracts, shared modules within the org | Codes are append-only within a service version | Team review |
| **T2 — Consumer-stable** | Backend ↔ frontend, first-party mobile apps | Codes append-only; status and semantics frozen; 90-day deprecation window | Contract owner approval |
| **T3 — Public** | Public API, partner integrations | Semver-guaranteed; breaking change = new major contract version + published migration note | Contract owner + review + changelog |

### How it works — assigning a tier

```text
Who consumes this error?
  ├─ only this process          → T0  (keep it typed; don't write a contract)
  ├─ another team in our org    → T1  (append-only codes; service-versioned)
  ├─ our own web/mobile client  → T2  (append-only + 90-day window + owner)
  └─ external developer/partner → T3  (semver + published catalogue + major versions)
```

When in doubt, **choose the higher tier**. The cost of over-promising stability is a stale
guarantee nobody reads; the cost of under-promising is a surprise break.

## Worked example — Acme SaaS surface inventory

```text
SURFACE                          CONSUMER                TIER  OWNER            CONTRACT ARTIFACT
────────────────────────────────────────────────────────────────────────────────────────────────
internal service helpers         same process            T0    platform team    none (typed only)
@acme/errors package             other Acme teams       T1    platform team    semver + CHANGELOG
Billing service (HTTP)           Checkout team          T1    billing team     service API spec
Acme web app  ↔  Acme API        our frontend (mobile!) T2    product team    error-contract.yaml
Public REST API                  partners + developers  T3    API team        published catalogue
Stripe webhooks (WebhookIngest)  partner backends       T3    billing team    webhook error doc
```

Note the asymmetry that bit Acme: the **webhook error contract** (T3, owned by billing) and the
**public API error contract** (T3, owned by the API team) are *different contracts* even though
both are "Acme errors going outward". They evolve on separate schedules and have separate
consumers.

## Key data / numbers

- **Five surfaces**: internal · module · service · backend↔frontend · public API.
- **Four stability tiers**: T0 unstable · T1 internal-stable · T2 consumer-stable · T3 public.
- **Semver for module contracts:** MAJOR = removal/repurposing/hierarchy change; MINOR = new
  code or optional field; PATCH = wording and docs.
- **RFC 9457 `type` URIs:** one `type` per problem class, root-relative by default
  (`/problems/validation-error`), version-independent unless the problem class itself is
  versioned. `about:blank` only for genuinely untyped problems.
- **Deprecation windows by tier:** T0 none · T1 30 days · T2 90 days · T3 90 days minimum,
  longer for regulated or long-support clients.
- **Telemetry gate before removal:** zero consumption for **30 consecutive days**.

## Real-world use case — Checkout

Acme's `Checkout` flow lives behind three surfaces at once. The **billing service** (T1) throws
`PAYMENT_CARD_DECLINED`; the **public API** (T3) returns `402` with
`type: "/problems/payment-declined"` and code `PAYMENT_CARD_DECLINED`; the **mobile app**
(T2) maps that code to "Try another card".

Acme's first mistake was treating the billing service's internal code as the public code. When
they later needed to distinguish *insufficient funds* from *card expired* for analytics, they
repurposed `PAYMENT_CARD_DECLINED` — the public meaning changed with no new code, and a partner
whose logic said "declined → suggest another card" started showing "your card expired" on
renewals, which users reported as a billing bug.

The fix started with an **ownership and tier** decision: the public code became
`PAYMENT_CARD_DECLINED` (meaning preserved), and two **new** codes
(`PAYMENT_CARD_INSUFFICIENT_FUNDS`, `PAYMENT_CARD_EXPIRED`) were added alongside it, with the
original code deprecated over a 90-day window on the T3 surface. The billing service kept its
internal code; the translation layer mapped all three.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One global error contract for everything | Simple to explain | Over-constrains internals; under-constrains publics | Very small products, single team |
| Tiered surfaces (T0–T3) | Matches real blast radius | Needs a decision the first time | Most products with >1 consumer |
| Versioned per-error contracts | Maximum precision | Unmanageable; consumers juggle versions | Rare; large partner ecosystems only |
| Publish everything as T3 | Maximum trust | High support cost; slow change | Regulated or partner-heavy products |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign a tier and owner per surface | Assume "internal" means "nobody depends on it" |
| Keep a module's exported vocabulary stable | Export class hierarchies as contract |
| Version a service, not individual errors inside it | Carve per-error versions inside one service version |
| Publish a public error catalogue | Ship public codes undocumented |
| Choose the higher tier when unsure | Under-promise stability to avoid work |
| Treat a mobile app as a public consumer | Assume the frontend is always up to date |

## Common mistakes

- **One-size-fits-all.** The same stability promise for an internal helper and a public API.
- **Unowned public surface.** Nobody is allowed to approve a breaking change because nobody
  owns the contract.
- **Mobile treated as first-party-and-therefore-safe.** Cached app versions live for years.
- **Per-error versioning inside a service.** Consumers end up tracking four versions at once.
- **No catalogue.** Developers guess, and their guesses become your support load.
- **Tier chosen by optimism.** "We will never change this" is not a stability tier.

## Checklist

- [ ] Every surface that crosses a boundary is listed, with a tier and an owner.
- [ ] Every tier has a written stability promise.
- [ ] Module contracts export a vocabulary (union of codes), not a fragile class shape.
- [ ] Services translate to domain codes at the boundary and version at the service level.
- [ ] The frontend and mobile client degrade gracefully on unknown codes.
- [ ] The public API has a published error catalogue and a deprecation policy.
- [ ] RFC 9457 `type` URIs are root-relative, one per problem class, and documented.

## Related

- [Evolution Rules and Compatibility](./02-evolution-rules-and-compatibility.md)
- [Ownership, Documentation, and Message Independence](./03-ownership-documentation-and-message-independence.md)
- [Versioning Error Contracts](../02-deep-dive/02-versioning-error-contracts.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 38 — Full-Stack Error Contracts](../../../part-14-frontend-and-full-stack/38-full-stack-error-contracts/README.md)
