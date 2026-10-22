# Chapter 45 — Reference

> Part XVII · Chapter 45 · all sections · _Estimated reading time: 8 min_

Cheat sheets for organizing error-handling modules: the standard directory structure, a
placement decision table, the legal dependency edges, and an ownership template.

## 1. Standard directory structure (45.20)

```text
src/
├── kernel/ or packages/errors-core/     # primitives only
│   ├── app-error.ts · result.ts · guards.ts · redact.ts
├── shared/
│   ├── registry/error-codes.ts          # pure data
│   └── resilience/retry-policies.ts     # named policies
├── features/<feature>/
│   ├── errors.ts                        # codes with <FEATURE>_ prefix
│   ├── <feature>.service.ts | .job.ts
│   └── index.ts                         # public surface (incl. error types)
├── infra/<vendor>/
│   └── errors.ts                        # from<Vendor>Error(): translate only
├── transports/
│   ├── http/     error-handler.ts · serialize-problem.ts
│   ├── jobs/     runner.ts · serialize-failure.ts
│   └── webhooks/ ack.ts
└── workflows/<saga>/
    ├── steps.ts · compensations.ts
```

**Sizing:** MVP ≈ 3 files (kernel + 1 feature + 1 transport). Startup ≈ 8–12. Full Acme scale
≈ 22. Grow into slots; never invent extra top-level folders for error code.

## 2. Module placement decision table

| You are adding… | Put it in | Owner | Never in |
| --------------- | --------- | ----- | -------- |
| A base class / type guard / redaction helper | `kernel/` | Platform team | feature folders |
| A new domain code (`EXPORT_*`) | `features/export/errors.ts` | Export team | kernel, shared barrel |
| SQLSTATE → app error mapping | `infra/postgres/errors.ts` | Infra/data team | domain, controllers |
| Stripe/vendor → app error mapping | `infra/<vendor>/errors.ts` | Integrations team | domain, HTTP handler |
| HTTP status + public title for a code | `shared/registry/error-codes.ts` (data entry) | Owning feature (PR) | handler switch statements |
| Retry attempts/backoff/budget | `shared/resilience/retry-policies.ts` | Platform team | call sites |
| Fallback / degraded response choice | The boundary that owns the fallback | Boundary owner | adapters |
| Saga compensation (refund, release) | `workflows/<saga>/compensations.ts` | Workflow owner | global recovery lib |
| RFC 9457 serialization | `transports/http/serialize-problem.ts` | API platform | controllers |
| DLQ failure payload | `transports/jobs/serialize-failure.ts` | Worker platform | job bodies |
| Webhook ack/nack status | `transports/webhooks/ack.ts` | Integrations | event handlers inline |

## 3. Legal dependency edges (45.12)

```text
transports  →  features, shared, kernel        (reads metadata; never translates vendors)
infra       →  features, kernel                (translates toward the domain)
features    →  kernel                          (and shared/registry data, read-only)
shared/registry → ∅                            (pure data)
workflows   →  features, kernel
```

Any edge outside this set is a review finding. Enforce with dependency-cruiser / eslint
boundary rules in CI; do not rely on review alone.

## 4. Zone fan-in thresholds (45.13 guardrail)

| Zone file | Expected internal imports | Red flag |
| --------- | ------------------------- | -------- |
| kernel | 0 | any internal import |
| `features/*/errors.ts` | 1 (kernel) | ≥ 3 |
| `infra/*/errors.ts` | 2 (kernel + feature codes) | ≥ 5 |
| `shared/registry` | 0 | any |
| transport handler | ≤ 3 | ≥ 6 |
| any error file | — | fan-in ≥ 8 or size ≥ ~300 lines |

## 5. Ownership template (45.16)

```text
# CODEOWNERS excerpt — every error zone gets a named owner
/packages/errors-core/            @acme/platform
/src/shared/registry/             @acme/platform   # mechanical; entries proposed by feature teams
/src/shared/resilience/           @acme/platform
/src/features/checkout/           @acme/payments
/src/features/export/             @acme/data
/src/features/webhooks/           @acme/integrations
/src/features/agent/              @acme/ai
/src/infra/postgres/              @acme/data
/src/infra/stripe/                @acme/integrations
/src/infra/llm/                   @acme/ai
/src/transports/http/             @acme/api-platform
/src/transports/jobs/             @acme/worker-platform
/src/workflows/checkout-saga/     @acme/payments
```

Per-code ownership is implied by prefix ↔ folder mapping (45.19): `CHECKOUT_*` can only be
defined under `features/checkout/`. A lint rule matching prefix to path makes this mechanical.

## 6. Promotion checklist — does this belong in the kernel? (45.2, 45.15)

- [ ] It has **no** product/vendor meaning (no `code` string, no SDK types).
- [ ] It changed at most once this quarter (or its change rate is explainable as a major).
- [ ] At least **3** independent modules consume it today (not "will consume someday").
- [ ] It is usable in a 5-line test with no other kernel imports.
- [ ] A new engineer can understand it without knowing Acme's product.

Fewer than 5 checkmarks = keep it local; revisit in a quarter.

## 7. Extraction playbook (god module → zones) (45.13, 45.14)

1. **Freeze** the god file (no new exports).
2. **Inventory** every export → assign a target zone.
3. **Move** behavior-preservingly; add one-release re-export shims with dated deletion.
4. **Registry entries** land in the same PR as each move.
5. **Kill barrels**; switch consumers to owning modules.
6. **Delete shims** on the scheduled date (CI grep enforces).
7. **Guard** with import-boundary lint; assign CODEOWNERS.

## 8. One-minute lookup test (45.19)

Pick a production log line with an error code. From the code string alone:

1. `grep` the prefix → finds the owning `errors.ts` in ≤ 1 hop.
2. Registry entry → status, retryable, public title.
3. Transport serializer → the single file that formats it externally.

If any hop takes > 1 minute for an engineer outside the owning team, fix naming/structure
before adding codes.

## Related

- [Chapter 45 README](../README.md)
- [Acme SaaS Error Module Tree](../03-practical-examples/01-acme-error-module-tree.md)
- [Circular Dependency Avoidance](../02-deep-dive/01-circular-dependency-avoidance.md)
- [Glossary](../../../GLOSSARY.md)
