# Registry-as-Code and Collision Testing

> Part III · Chapter 8 · Sections 8.6–8.8, 8.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Uniqueness and Registry Structure](../01-concepts/03-uniqueness-and-registry-structure.md)

## In one sentence

Turn the registry into **executable code with CI checks** so uniqueness, reserved domains, complete
mappings, and production coverage are **verified on every commit** instead of discovered in
production.

## Why this matters in production

A registry in a wiki or a spreadsheet is stale the moment someone throws a code without updating it.
A registry **as code** — a typed module plus a test suite — makes the invariants mechanical. The
build fails on a duplicate, an unreserved prefix, a missing mapping, or a thrown-but-unregistered
code. This file shows the complete enforcement suite.

## The typed registry module

```ts
// registry/registry.ts
export type ErrorCategory =
  | "validation" | "auth" | "business" | "payment"
  | "database" | "external" | "resource" | "unexpected";

export type Visibility = "public" | "internal";
export type ClientAction =
  | "retry" | "reauthenticate" | "fix_input"
  | "choose_alternative" | "contact_support" | "none";

export interface CodeEntry {
  domain: string;                 // must be in RESERVED_DOMAINS
  category: ErrorCategory;
  http: number;
  retryable: boolean;
  visibility: Visibility;
  publicAlias?: string;           // required when visibility: "internal"
  clientAction: ClientAction;
  messageKey: string;             // i18n key, not raw text
  description: string;            // engineer-facing
  owner: string;
  since: string;                  // e.g. "2026.03"
  deprecated?: { since: string; replacedBy: string; removeAfter: string };
}

export const RESERVED_DOMAINS = new Set([
  "VALIDATION", "AUTH", "USER", "BILLING", "PAYMENT",
  "DB", "EXPORT", "WEBHOOK", "AGENT", "RATE", "SYSTEM", "INTERNAL",
]);

export const REGISTRY = {
  VALIDATION_REQUIRED_FIELD: {
    domain: "VALIDATION", category: "validation", http: 422, retryable: false,
    visibility: "public", clientAction: "fix_input",
    messageKey: "errors.validation.required",
    description: "A required field was missing.", owner: "platform", since: "2026.01",
  },
  PAYMENT_CARD_DECLINED: {
    domain: "PAYMENT", category: "payment", http: 402, retryable: false,
    visibility: "public", clientAction: "choose_alternative",
    messageKey: "errors.payment.cardDeclined",
    description: "The card issuer declined the charge.", owner: "payments", since: "2026.01",
  },
  PAYMENT_PROVIDER_TIMEOUT: {
    domain: "PAYMENT", category: "external", http: 503, retryable: true,
    visibility: "internal", publicAlias: "SERVICE_UNAVAILABLE",
    clientAction: "retry", messageKey: "errors.payment.providerTimeout",
    description: "The PSP did not respond before the deadline.", owner: "payments", since: "2026.02",
  },
  DB_UNIQUE_VIOLATION: {
    domain: "DB", category: "database", http: 409, retryable: false,
    visibility: "internal", publicAlias: "CONFLICT",
    clientAction: "fix_input", messageKey: "errors.db.conflict",
    description: "A unique constraint was violated.", owner: "platform", since: "2026.01",
  },
  INTERNAL_UNEXPECTED: {
    domain: "INTERNAL", category: "unexpected", http: 500, retryable: false,
    visibility: "internal", publicAlias: "SERVICE_UNAVAILABLE",
    clientAction: "contact_support", messageKey: "errors.internal.unexpected",
    description: "An unclassified error reached the boundary.", owner: "platform", since: "2026.01",
  },
} as const satisfies Record<string, CodeEntry>;

export type ErrorCode = keyof typeof REGISTRY;
```

`satisfies Record<string, CodeEntry>` validates every entry against the interface at compile time
without widening the literal types — so `ErrorCode` stays a precise union.

## The enforcement suite

```ts
// registry/registry.test.ts
import { describe, it, expect } from "vitest";
import { REGISTRY, RESERVED_DOMAINS } from "./registry";

const CODE_RE = /^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/;
const entries = Object.entries(REGISTRY);

describe("registry invariants", () => {
  it("has no duplicate codes", () => {
    const keys = Object.keys(REGISTRY);
    expect(new Set(keys).size).toBe(keys.length);
  });

  it("uses valid code format and reserved domains", () => {
    for (const [code, e] of entries) {
      expect(code).toMatch(CODE_RE);
      expect(RESERVED_DOMAINS.has(e.domain)).toBe(true);
      expect(code.startsWith(e.domain)).toBe(true);      // prefix matches domain
    }
  });

  it("maps internal codes to a public alias", () => {
    for (const [code, e] of entries) {
      if (e.visibility === "internal") {
        expect(e.publicAlias, `${code} needs publicAlias`).toBeTruthy();
      }
    }
  });

  it("has a message key and owner for every code", () => {
    for (const [code, e] of entries) {
      expect(e.messageKey, `${code} messageKey`).toBeTruthy();
      expect(e.owner, `${code} owner`).toBeTruthy();
    }
  });

  it("deprecated codes declare a replacement", () => {
    for (const [code, e] of entries) {
      if (e.deprecated) {
        expect(e.deprecated.replacedBy in REGISTRY).toBe(true);
      }
    }
  });
});
```

## Detecting thrown-but-unregistered codes (static scan)

```ts
// registry/coverage.test.ts — scan source for code literals not in the registry.
import { Project, SyntaxKind } from "ts-morph";
import { REGISTRY } from "./registry";

it("every quoted code literal exists in the registry", () => {
  const project = new Project({ tsConfigFilePath: "tsconfig.json" });
  project.addSourceFilesAtPaths(["src/**/*.ts", "!src/**/*.test.ts"]);

  const KNOWN = new Set(Object.keys(REGISTRY));
  const offenders: string[] = [];

  for (const file of project.getSourceFiles()) {
    for (const lit of file.getDescendantsOfKind(SyntaxKind.StringLiteral)) {
      const v = lit.getLiteralValue();
      // Heuristic: SCREAMING_SNAKE likely a code. Tighten with a `code:` property check.
      if (/^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/.test(v) && !KNOWN.has(v) && !RESERVED_DOMAINS.has(v)) {
        offenders.push(`${v} @ ${file.getBaseName()}:${lit.getStartLineNumber()}`);
      }
    }
  }
  expect(offenders).toEqual([]);
});
```

For precision, match the AST shape `new AppError({ code: "<literal>" })` rather than every string.
The heuristic above is a starting point that catches most accidental codes.

## Reverse coverage — registered but unused

```ts
it("reports registered codes with no production usage", () => {
  const used = new Set<string>(); // populated by the same AST scan over `code:` literals
  const unused = Object.keys(REGISTRY).filter((c) => !used.has(c));
  // Unused codes are a warning, not a failure (may be produced dynamically).
  expect(unused.length).toBeLessThan(Object.keys(REGISTRY).length);
});
```

## Generating derived tables from the registry

Because the registry is data, the mapping tables and docs are **derived**, never hand-maintained.

```ts
export const HTTP: Record<ErrorCode, number> =
  Object.fromEntries(Object.entries(REGISTRY).map(([c, e]) => [c, e.http])) as Record<ErrorCode, number>;

export const RETRYABLE: Record<ErrorCode, boolean> =
  Object.fromEntries(Object.entries(REGISTRY).map(([c, e]) => [c, e.retryable])) as Record<ErrorCode, boolean>;

export function publicCodeOf(code: ErrorCode): string {
  const e = REGISTRY[code];
  return e.visibility === "public" ? code : (e.publicAlias ?? "SERVICE_UNAVAILABLE");
}
```

A missing entry is impossible because `Object.fromEntries` is driven by the registry itself; the
`Record<ErrorCode, T>` annotation guarantees total coverage at compile time.

## Runtime guards for dynamic boundaries

```ts
import { REGISTRY, ErrorCode } from "./registry";

const KNOWN = new Set(Object.keys(REGISTRY));

export function isKnownCode(v: unknown): v is ErrorCode {
  return typeof v === "string" && KNOWN.has(v);
}

export function canonicalize(v: unknown, metrics: Metrics, log: Logger): ErrorCode {
  if (isKnownCode(v)) return v;
  metrics.increment("error.code.undocumented");
  log.warn({ unknownCode: v }, "Unregistered error code observed");
  return "INTERNAL_UNEXPECTED";
}
```

## Worked example — CI pipeline

```yaml
# .github/workflows/registry.yml (illustrative)
- run: pnpm test registry/registry.test.ts
- run: pnpm test registry/coverage.test.ts
- run: pnpm tsx registry/generate-docs.ts --check   # docs in sync with registry
```

Any failing step blocks the merge. A duplicate code, an unreserved prefix, a missing alias, a
thrown-but-unregistered code, or stale generated docs all stop the build.

## Key data / numbers

- **Format regex:** `/^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/`.
- **Reserved domains:** 10–20 entries; every entry validated.
- **Coverage tables:** HTTP, retry, client action, message key — all derived, all total.
- **`satisfies`** (TypeScript 4.9+) validates entries while preserving literal types.
- **ts-morph** is the common AST library for TS static scans; alternatives include ESLint custom
  rules and `tsc` APIs.

## Real-world use case — Acme SaaS

Acme's registry test suite caught a merge that introduced a duplicate `WEBHOOK_FAILED` with a
different HTTP status, blocked a PR that added `PAYMENT_STATUS` (unreserved prefix), and flagged six
unregistered codes in adapters. Generated HTTP/retry/message tables meant no handler maintained its
own mapping. The static scan ran in ~8 seconds on CI and has since blocked every attempted drift.
The registry moved from a doc to a build artifact.

## Trade-offs

| Enforcement | Catches | Cost | Failure timing |
| ----------- | ------- | ---- | -------------- |
| Type `satisfies` | Missing/extra entry fields | Compile | Fastest |
| Unit tests | Duplicates, domains, aliases | Test runtime | PR |
| Static AST scan | Thrown-but-unregistered | Scan runtime | PR |
| Runtime metric | Dynamic/unknown codes | Negligible | Production |
| Generated docs check | Doc drift | Generation | PR |

Layer them: compile-time first, tests next, runtime for the inevitable dynamic cases.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make the registry a typed module | Keep it in a wiki/spreadsheet |
| Derive mapping tables from it | Hand-maintain parallel tables |
| Enforce uniqueness/domains in tests | Trust reviewers to notice |
| Maintain a runtime undocumented-code metric | Assume static coverage is complete |
| Check generated docs in CI | Let docs drift |

## Common mistakes

- **Registry in docs only** — drifts immediately.
- **No AST scan** — thrown-but-unregistered codes persist.
- **Hand-maintained mapping tables** that disagree with the registry.
- **Static-only** coverage that misses dynamically constructed codes.
- **No docs generation check**, so the catalog lies.

## Checklist

- [ ] Is the registry a typed, version-controlled module?
- [ ] Are uniqueness, format, and reserved domains tested?
- [ ] Are internal codes required to declare a public alias?
- [ ] Is there a static scan for unregistered codes?
- [ ] Are mapping tables generated from the registry?
- [ ] Is there a runtime metric for unknown codes?

## Related

- [Uniqueness and Registry Structure](../01-concepts/03-uniqueness-and-registry-structure.md)
- [Backward Compatibility and Deprecation Mechanics](./02-backward-compatibility-and-deprecation.md)
- [The Sample Error Registry](../03-practical-examples/01-sample-error-registry.md)
