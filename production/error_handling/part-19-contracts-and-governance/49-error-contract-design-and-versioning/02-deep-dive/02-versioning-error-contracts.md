# Versioning Error Contracts

> Part XIX · Chapter 49 · Sections 49.6, 49.11–49.12 · _Estimated reading time: 20 min_
> **Prerequisite:** [Contract Surfaces and Stability Guarantees](../01-concepts/01-contract-surfaces-and-stability.md)

## In one sentence

An error contract gets its **own version**, independent of the API version and the package
version, and semver applies to it by blast radius: **MAJOR** for removals and meaning changes,
**MINOR** for additions, **PATCH** for wording.

## Why this matters in production

Teams usually try to hang the error contract off something that already exists — the API
version, the package version, the deploy. Each of those is wrong for a different reason:

- **Hanging it off the API version** means an error-only change forces an API version bump,
  which means clients migrate for something they do not use. In practice teams then *stop
  bumping* and the error contract silently stops being versioned at all.
- **Hanging it off the package version** couples the contract to the release cadence of the
  code. A `PATCH` release that renames a code becomes a breaking change by accident.
- **Hanging it off the deploy** means there is no durable reference for "which contract was
  live on 3 March", so a support investigation cannot be answered.

The contract version answers exactly one question: **which set of guarantees was in force?**
That is the question asked during an incident, in a partner escalation, and in a code review.

## Why a separate version

```text
API version        → which endpoints and payload schemas exist
Package version    → which library implementation you installed
Error contract ver → which failure guarantees the producer makes
```

These three move at different speeds, so they need different numbers:

| What changed | API version | Package version | Error contract version |
| ------------ | ----------- | --------------- | --------------------- |
| New endpoint | MINOR | any | unchanged |
| New error code | unchanged | MINOR | MINOR |
| Error message reworded | unchanged | PATCH | PATCH |
| Error code removed | unchanged | MAJOR | **MAJOR** |
| Internal refactor of the error layer | unchanged | PATCH | unchanged |

## The semver mapping

This is the table to memorise. The test for each row is: *could a reasonable consumer break?*

| Change | Contract bump | Rationale |
| ------ | ------------- | --------- |
| Add an error code | **MINOR** | Old consumers must tolerate unknown codes |
| Add an optional field to the error body | **MINOR** | Additive |
| Add a new `type` URI | **MINOR** | New problem class, existing classes untouched |
| Reword `title` or `detail` | **PATCH** | Prose is not contract |
| Change a description in the catalogue | **PATCH** | Documentation |
| Add a `clientAction` value | **MAJOR** | Clients with exhaustive `switch`es break |
| Remove or rename a code | **MAJOR** | Old consumers' branches stop matching |
| Change a code's HTTP status | **MAJOR** | Changes retry/branch behaviour |
| Change a code's meaning | **MAJOR** | Old consumers take the wrong branch |
| Change a code's retryability | **MAJOR** | Changes automated behaviour |
| Remove or retype a body field | **MAJOR** | Parsing breaks |
| Make a field required | **MAJOR** | Older producers no longer produce a valid body |

> ⚠️ **Hazard.** "We only added a new `clientAction` value" is a MAJOR change. Every consumer
> with an exhaustive `switch` on `clientAction` now has a branch that throws or returns
> `undefined`. Enumerations are part of the contract even when they look like implementation
> detail.

## Version carriers

A contract version must be discoverable in at least two places: **in the registry** (for
producers) and **on the wire** (for consumers).

```yaml
# 1. Registry — the authoritative record
contract:
  surface: public-api
  version: "1.4.0"
  since: "2025-09-01"
  typeUriBase: "/problems"
```

```http
# 2. On the wire — every error response announces the contract it follows
HTTP/1.1 409 Conflict
Content-Type: application/problem+json
Error-Contract-Version: 1.4.0
```

```ts
// 3. In code — the type URIs are generated from the registry, not hand-written
const TYPE_BY_CODE: Record<ErrorCode, string> = buildTypeUris(REGISTRY);
```

A version that only exists in a document is a version nobody can check. `Error-Contract-Version`
is a private header (not standardised), which is fine — but it must be **emitted on every error
response** and **readable by your SDK**, so a consumer can assert "the server is still on a
contract I understand".

### Versioning `type` URIs

`type` is a URI reference identifying the problem class. Two approaches:

| Approach | Example | Pros | Cons |
| -------- | ------- | ---- | ---- |
| **Versionless `type`** | `/problems/validation-error` | Survives contract versions; docs stay stable | Cannot express "the meaning of this type changed" |
| **Versioned `type`** | `/problems/v1/validation-error` | Meaning is pinned | Every contract version needs a new URI set; docs multiply |

Recommended default: **versionless `type` URIs**, plus a contract version header. If a problem
class genuinely changes meaning — rare, and it should be treated as a new class — give it a
**new** URI rather than versioning the old one:

```text
/problems/validation-error            ← unchanged meaning across 1.x and 2.x
/problems/payment-declined-v2          ← new class, new URI (avoid renaming the old one)
```

The rule "one `type` per problem class, and a changed meaning is a new class" keeps `type`
stable, which is what makes it usable as a durable identifier.

## Negotiation

Two modes are worth supporting, and only two:

### Passive (recommended default)

The server always answers with its **current** contract. The client compares the returned
`Error-Contract-Version` against what it knows and decides what to do.

```ts
const serverVersion = res.headers.get("error-contract-version"); // "1.4.0"
if (serverVersion && major(serverVersion) > major(SUPPORTED_CONTRACT)) {
  log.warn({ serverVersion }, "server contract newer than client support");
  // keep working: unknown codes degrade gracefully
}
```

### Active (for long-lived clients)

The client declares the contract it supports, and the server may answer in that contract.

```http
GET /v2/projects HTTP/1.1
Accept-Error-Contract: 1.x
```

```text
Server answers with contract 1.4.0 while 1.x is supported;
once only 2.x is supported, a 1.x-only client receives a 400 with
code=ERROR_CONTRACT_VERSION_UNSUPPORTED and a Sunset header.
```

Active negotiation is worth it only when you have clients that **must** keep an exact
guarantee (contractual SLAs, regulated partners). For everything else, passive is enough and
far cheaper to operate.

### Version pinning in the registry

Every code records when it entered and (optionally) when it leaves:

```ts
USER_NOT_FOUND: {
  // ...
  since: "2026-03",          // contract version 1.3.0
  removedIn: undefined,      // still present
},
USER_DOES_NOT_EXIST: {
  // ...
  since: "2024-11",          // contract version 1.0.0
  removedIn: "2.0.0",        // scheduled for removal
},
```

This turns "when did this code exist?" from an archaeology exercise into a lookup, which is
exactly the question an incident review asks.

## Worked example — Acme bumps the public error contract from 1.4.0 to 2.0.0

```text
Contract 1.4.0 (current)
  codes: 42 public, 180 internal
  type URIs: /problems/... (versionless)
  clientAction values: retry | reauthenticate | fix_input | choose_alternative
                       | contact_support | none
```

**Why a MAJOR is needed.** Three changes accumulate, any one of which is breaking:

```text
1. USER_DOES_NOT_EXIST is removed (consumption 0 for 45 days).        → removal
2. PAYMENT_CARD_EXPIRED moves 422 → 409 via a new code.                → status/meaning
3. clientAction gains "schedule" (for "come back at 09:00").           → enum extension
```

**The release.**

```text
2026-08-01  Contract 1.5.0 — MINOR. New code EXPORT_SCHEDULED added with
            clientAction="schedule". Wait: adding an enum value is a MAJOR.
            Corrected: 1.5.0 ships the new CODE only, using the existing
            action "none"; the new action value is deferred to 2.0.0.
```

This is the discipline paying off: a reviewer caught the enum extension and deferred it, which
kept the release MINOR and non-breaking.

```text
2026-09-15  Contract 2.0.0 — MAJOR. Ships together:
              - USER_DOES_NOT_EXIST removed (alias removed)
              - PAYMENT_CARD_EXPIRED deprecated → PAYMENT_CARD_EXPIRED_AT_CHECKOUT (409)
              - clientAction gains "schedule"
            All responses now carry Error-Contract-Version: 2.0.0.
            1.x clients keep working against the deprecated endpoints for 90 days.
            Sunset headers announce the 1.x end-of-life on those endpoints.
```

## Key data / numbers

- **Three independent versions:** API version · package version · error contract version.
- **Semver mapping:** add code/optional field/`type` → MINOR; wording/docs → PATCH; remove,
  rename, re-status, re-meaning, enum extension, required field → MAJOR.
- **Version carrier:** `Error-Contract-Version` header on every error response; `contract.version`
  in the registry; `since` / `removedIn` per code.
- **`type` URI convention:** one URI per problem class, **versionless** by default, root-relative
  (`/problems/<slug>`); `about:blank` only for untyped problems. A changed meaning gets a **new
  URI**, not a versioned one.
- **Negotiation:** passive (server returns current, client compares majors) by default; active
  (`Accept-Error-Contract`) only for contractual consumers.
- **Contract version lifetime:** 1.x supported for **≥ 90 days** after a 2.0.0 release; 2.x
  becomes the default **30 days** after 1.x reaches end-of-life.
- **Changelog:** one entry per contract version, listing added / changed / removed codes.

## Real-world use case — Acme SaaS public API

Acme's public API originally returned bare `{"error": "..."}` strings, and the error catalogue
was a wiki page nobody updated. When they launched v2, they kept the same code names but
re-mapped `PAYMENT_CARD_DECLINED` from `402` to `409`, because the new billing engine reported
card declines as state conflicts.

Two partner integrations broke within a day: one retried `409` forever (it treated 4xx as
retryable) and one switched from "try another card" to "contact support" because its copy keyed
on `409`.

The repair took one quarter and shaped the standard:

1. **A contract version, separate from the API version.** `Error-Contract-Version: 1.0.0` on
   every error response. The API is now v3; the error contract is still 1.x.
2. **`type` URIs, versionless**, so `/problems/payment-declined` remains the identifier even
   after the API moves to v4.
3. **The offending mapping reverted** to `402`, and the `409` behaviour was introduced as
   `PAYMENT_CARD_DECLINED_AT_CHECKOUT` in contract **2.0.0** with a 90-day dual-emit window.
4. **A public catalogue generated from the registry**, so it can no longer lag behind the code.
5. **A compatibility test suite** that replays old client expectations against the current
   contract and fails CI when a published guarantee is broken.

The lesson Acme took from a two-day partner incident: **the error contract is a published
artifact and needs its own version, its own changelog, and its own tests.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Separate contract version | Precise, decoupled | One more version to track | Any surface with external consumers |
| Fold into API version | One version to track | Error-only changes force API migrations | Small products, single client |
| Fold into package version | Zero extra work | Breaks on unrelated releases | Internal modules only |
| Versionless `type` URIs | Durable identifiers | Cannot express changed meaning | Default choice |
| Versioned `type` URIs | Meaning pinned | URI explosion, doc churn | When a class truly changes meaning |
| Active negotiation | Exact guarantees | Server complexity, client complexity | Contractual/regulated consumers |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give the error contract its own version | Hang it off the API or package version |
| Announce the contract version on every error response | Keep the version only in a document |
| Use versionless `type` URIs by default | Version every `type` URI |
| Treat enum extensions as MAJOR | Add enum values in a MINOR release |
| Pin code lifetimes with `since` / `removedIn` | Guess a code's age from the changelog |
| Support passive negotiation by default | Build active negotiation nobody asked for |
| Test published guarantees in CI | Assume the contract matches the implementation |

## Common mistakes

- **The implicit version.** No contract version exists, so "which guarantees were live?" is
  unanswerable.
- **The accidental MAJOR.** A MINOR release adds an enum value and breaks exhaustive switches.
- **The accidental MINOR.** A "cleanup" renames a code inside a patch release.
- **The versioned `type` URI.** `/problems/v2/validation-error` for every contract version.
- **The contract that only exists in the registry.** Consumers cannot see the version they got.

## Checklist

- [ ] The error contract has its own version, stored in the registry.
- [ ] Every error response carries the contract version.
- [ ] Every code records `since` and, when scheduled, `removedIn`.
- [ ] The semver mapping table is applied to every proposed change.
- [ ] `type` URIs are versionless, root-relative, and one per problem class.
- [ ] Clients compare contract versions passively and degrade gracefully.
- [ ] A CI test replays published contract expectations against the current implementation.

## Related

- [Contract Surfaces and Stability Guarantees](../01-concepts/01-contract-surfaces-and-stability.md)
- [Deprecation Mechanics and Windows](./01-deprecation-mechanics-and-windows.md)
- [Durable vs Ceremonial Rules](./03-durable-vs-ceremonial-rules.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
