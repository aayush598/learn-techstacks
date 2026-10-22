# Uniqueness and Registry Structure

> Part III · Chapter 8 · Sections 8.6–8.9 · _Estimated reading time: 16 min_
> **Prerequisite:** [Code Naming and Scoping](./02-code-naming-and-scoping.md)

## In one sentence

A **registry** is the single source of truth that lists every code exactly once with its metadata,
and **uniqueness** — one meaning per code, enforced automatically — is what makes the registry
trustworthy.

## Why this matters in production

Without a registry, codes are scattered constants. Nobody knows the full set, duplicates appear
(`USER_NOT_FOUND` and `USER_DOES_NOT_EXIST`), and the same code gets different HTTP mappings in
different handlers. A registry fixes this by being the one place a code is declared, and by making
collisions and gaps detectable in CI rather than in production.

## Uniqueness (8.6)

The invariant is simple and absolute: **one code, one meaning, one row.** Uniqueness must hold in
two dimensions.

| Dimension | Meaning | Violated by |
| --------- | ------- | ----------- |
| **Value-unique** | No two rows share a code string | Copy-paste, merge conflicts |
| **Meaning-unique** | No two codes mean the same condition | `USER_NOT_FOUND` vs `USER_MISSING` |

Value-uniqueness is mechanical (a `Set` catches it). Meaning-uniqueness needs review — CI can flag
**near-duplicates** (edit distance, shared tokens) for a human to judge.

```ts
const codes = Object.keys(REGISTRY);
const unique = new Set(codes);
if (unique.size !== codes.length) throw new Error("Duplicate error code in registry");
```

## Preventing collisions (8.7)

Collisions come from three sources; each has a control.

| Source | Example | Control |
| ------ | ------- | ------- |
| Reserved-domain violation | `PAYMENT_STATUS` vs `BILLING_STATUS` | Enforce reserved domain prefixes |
| Case/format drift | `payment_declined` vs `PAYMENT_DECLINED` | Regex-validate format |
| Semantic overlap | `EXPORT_FAILED` vs `EXPORT_ERROR` | Near-duplicate CI lint + review |

```text
CI CHECKS (all must pass)
1. every code matches /^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/
2. prefix ∈ RESERVED_DOMAINS
3. no duplicate code strings
4. no code missing from a required mapping table
5. near-duplicate warnings surfaced for review
```

The goal is not to make collisions impossible by cleverness but to **make them fail the build**.

## Centralized registries (8.8)

A **centralized registry** is one module every code is declared in.

| Pros | Cons |
| ---- | ---- |
| One place to see every code | Merge conflicts on a large file |
| Easy to enforce uniqueness and coverage | Cross-team coupling |
| Simple tooling and docs generation | Central review bottleneck |
| Total mapping tables guaranteed | Big-bang edits |

```ts
// registry.ts — the single source of truth.
export const REGISTRY = {
  VALIDATION_REQUIRED_FIELD: {
    domain: "VALIDATION", category: "validation", http: 422,
    retryable: false, visibility: "public",
    message: "A required field is missing.",
  },
  PAYMENT_CARD_DECLINED: {
    domain: "PAYMENT", category: "payment", http: 402,
    retryable: false, visibility: "public",
    message: "Your card was declined.",
  },
  // ...
} as const satisfies Record<string, CodeEntry>;
```

Centralized works well up to a few hundred codes and a handful of teams. Past that, split by domain.

## Domain-owned registries (8.9)

A **domain-owned registry** lets each domain own its slice, with a thin central index enforcing
global rules.

```ts
// billing/codes.ts     → BILLING_* codes
// payments/codes.ts    → PAYMENT_* codes
// exports/codes.ts     → EXPORT_* codes
// registry/index.ts    → merges + validates + exports the union
```

| Pros | Cons |
| ---- | ---- |
| Teams own their codes, no bottleneck | Risk of drift between slices |
| Parallel development, fewer conflicts | Cross-slice collision possible |
| Clear ownership in CODEOWNERS | Requires a merge/validation step |

```ts
// registry/index.ts — merge and validate the union.
import { BILLING_CODES } from "../billing/codes";
import { PAYMENT_CODES } from "../payments/codes";
import { EXPORT_CODES } from "../exports/codes";

const SLICES = { ...BILLING_CODES, ...PAYMENT_CODES, ...EXPORT_CODES };
assertUnique(SLICES);
assertReservedDomains(SLICES);
export const REGISTRY = SLICES;
export type ErrorCode = keyof typeof REGISTRY;
```

Guidance:

- **Start centralized.** Split by domain only when the file becomes a bottleneck.
- **Keep the validation central.** Slices are owned by teams; the cross-slice invariants
  (uniqueness, reserved domains, coverage) are enforced in the merge.
- **Assign a CODEOWNER per slice** so a new code gets the right review.

## Worked example

```ts
interface CodeEntry {
  domain: string;
  category: ErrorCategory;
  http: number;
  retryable: boolean;
  visibility: "public" | "internal";
  publicAlias?: string;
  message: string;
}

function assertUnique(reg: Record<string, CodeEntry>): void {
  const seenMeaning = new Map<string, string>(); // category+http+message → code
  for (const [code, entry] of Object.entries(reg)) {
    if (!/^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/.test(code)) {
      throw new Error(`Bad code format: ${code}`);
    }
    if (!RESERVED_DOMAINS.has(entry.domain)) {
      throw new Error(`Unreserved domain '${entry.domain}' in ${code}`);
    }
    const meaning = `${entry.category}:${entry.http}`;
    const clash = seenMeaning.get(meaning);
    seenMeaning.set(meaning, code); // informational; near-dupes flagged for review
  }
}
```

## Key data / numbers

- **Practical size:** centralized registries stay manageable to ~**300–500 codes**; beyond that,
  split by domain.
- **Format regex:** `/^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/` — at least two segments, uppercase.
- **Reserved domains:** keep to **10–20**; every addition is a governance event.
- **Coverage tables:** HTTP status, retry policy, client action, user message — four tables, all
  `Record<ErrorCode, T>` so a missing entry is a build failure.

## Real-world use case — Acme SaaS

Acme's codes lived in a dozen files. Two teams both defined `WEBHOOK_FAILED` with different HTTP
mappings, and a third defined `WEBHOOK_ERROR` meaning the same thing. The centralized registry they
built enforced uniqueness at import time, and a near-duplicate lint flagged the overlap for review.
They later split into domain-owned slices (`billing/codes.ts`, `payments/codes.ts`, `exports/codes.ts`)
with a central merge that validates reserved domains and coverage. Merge conflicts on the registry
dropped to near zero while guarantees stayed centralized.

## Trade-offs

| Structure | Pros | Cons | When to use |
| --------- | ---- | ---- | ----------- |
| Centralized | Simple, total coverage | Bottleneck at scale | ≤ few hundred codes |
| Domain-owned | Parallel, clear ownership | Needs merge validation | Many teams/domains |
| No registry | None | Duplicates, drift | Never in production |
| Generated from decorators | Low friction | Magic, hard to audit | Only with strong tooling |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Declare each code exactly once | Re-declare codes in multiple modules |
| Enforce format + reserved domains in CI | Trust convention only |
| Flag near-duplicates for review | Auto-merge semantically similar codes |
| Keep validation central even if slices are owned | Let each slice define its own rules |
| Add a code via a reviewed registry change | Scatter constants across features |

## Common mistakes

- **Duplicate code strings** from copy-paste.
- **Semantic duplicates** (`_NOT_FOUND` vs `_MISSING`) that split analytics.
- **Unreserved prefixes** causing cross-team collisions.
- **Split registries without a central merge**, so global invariants vanish.
- **No coverage table**, so a code has no HTTP mapping.

## Checklist

- [ ] Is every code declared exactly once?
- [ ] Is format and domain validity enforced in CI?
- [ ] Are near-duplicates flagged for human review?
- [ ] Is there a central validation even with domain-owned slices?
- [ ] Does every code have all required mapping entries?
- [ ] Is there a CODEOWNER for each registry slice?

## Related

- [Preventing Collisions in CI](../02-deep-dive/01-registry-as-code-and-collision-testing.md)
- [Mapping Codes to Behavior](./04-mapping-codes-to-behavior.md)
- [The Sample Error Registry](../03-practical-examples/01-sample-error-registry.md)
