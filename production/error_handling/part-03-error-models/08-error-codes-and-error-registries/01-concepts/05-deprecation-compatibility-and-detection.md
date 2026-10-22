# Deprecating Codes, Compatibility, and Detecting Undocumented Codes

> Part III · Chapter 8 · Sections 8.15–8.16, 8.18 · _Estimated reading time: 16 min_
> **Prerequisite:** [Mapping Codes to Behavior](./04-mapping-codes-to-behavior.md)

## In one sentence

Codes are contracts, so you **deprecate rather than delete**, keep **backward compatibility** for
old clients, and **detect undocumented codes** automatically — because a code that exists only in a
`throw` statement is invisible until it breaks someone.

## Why this matters in production

Removing or repurposing a code breaks clients you do not control: a mobile app released last year,
a partner integration, an internal dashboard. Likewise, a code that engineers throw but never
register will have no HTTP mapping, no retry rule, and no user message — it will surface as a
generic `500` and an unactionable support ticket. Compatibility and detection are what keep the
registry honest over time.

## Deprecating codes (8.15)

Deprecation is a **staged lifecycle**, never a delete.

```text
1. ACTIVE      → in normal use
2. DEPRECATED  → marked; still produced and mapped; docs warn; replacement documented
3. RETIRED     → no longer produced; still recognized on input/mapping for old clients
4. REMOVED     → deleted only after telemetry shows zero producers and consumers
```

Registry entry during deprecation:

```ts
const REGISTRY = {
  USER_DOES_NOT_EXIST: {                    // the old code
    domain: "USER", category: "business", http: 404,
    retryable: false, visibility: "public",
    clientAction: "none", messageKey: "errors.user.notFound",
    description: "Deprecated alias of USER_NOT_FOUND.",
    deprecated: { since: "2026.03", replacedBy: "USER_NOT_FOUND", removeAfter: "2026.09" },
  },
  USER_NOT_FOUND: { /* canonical replacement */ },
} as const;
```

Rules:

- **Deprecate before removing.** Keep the old code working through at least one full release cycle
  (commonly 90 days for external clients).
- **Document the replacement** in the entry and the generated docs.
- **Keep producing the old code** during the deprecation window if consumers still expect it, or
  emit both via a compatibility alias.
- **Remove only with evidence** — telemetry showing no consumers.

## Backward compatibility (8.16)

Old clients must keep working. Strategies, from cheapest to most involved:

| Change | Compatibility strategy |
| ------ | ---------------------- |
| Add a new code | ✅ Safe; old clients fall back on unknown |
| Deprecate a code | Keep mapping + docs; announce; monitor |
| Rename a code | Emit old + new during a window, or alias old → new |
| Change a code's HTTP status | Never for a public code; introduce a new code |
| Change a code's meaning | Never; create a new code |
| Remove a code | Only after zero-consumer telemetry |

```ts
// Compatibility alias: accept an old code, respond with the canonical one.
const ALIASES: Record<string, ErrorCode> = {
  USER_DOES_NOT_EXIST: "USER_NOT_FOUND",
};

function canonicalize(raw: string): ErrorCode | undefined {
  return (REGISTRY as Record<string, unknown>)[raw] ? (raw as ErrorCode)
       : ALIASES[raw];
}
```

Client-side rule (forward compatibility): **unknown codes must degrade gracefully**, not crash.

```ts
function render(err: { code: string }): string {
  const known = MESSAGE_KEY[err.code as ErrorCode];
  return known ? t(known) : t("errors.internal.unexpected"); // safe fallback
}
```

> ⚠️ **Hazard.** A client that throws on an unrecognized code will break the day the server adds
> one. Unknown codes are inevitable in any system that evolves; handle them explicitly.

## Detecting undocumented codes (8.18)

A code is "undocumented" when it is produced somewhere but absent from the registry, or registered
but never produced (dead code). Both are detectable in CI.

| Detection | Method | Catches |
| --------- | ------ | ------- |
| Static: code literals vs registry | AST/lint scan of `code:` values | Thrown-but-unregistered codes |
| Runtime: unknown code at the boundary | Boundary logs/emits a metric | Codes from untyped/dynamic sources |
| Coverage: registry vs usage | Reverse scan | Registered-but-unused codes (dead) |
| Schema: emitted codes vs registry | Compare runtime analytics | Gaps between docs and reality |

```ts
// Static test: every literal code passed to AppError exists in the registry.
import { Project } from "ts-morph";

const sf = new Project().addSourceFilesAtPaths("src/**/*.ts");
const codes = sf.flatMap((f) => f.getDescendantsOfKind(SyntaxKind.StringLiteral))
  .map((s) => s.getLiteralValue())
  .filter((v) => /^[A-Z][A-Z0-9_]+$/.test(v));

const missing = codes.filter((c) => !(c in REGISTRY));
if (missing.length) throw new Error(`Undocumented codes: ${missing.join(", ")}`);
```

```ts
// Runtime boundary: count unknown codes as a metric.
function canonicalizeOrFallback(raw: unknown): ErrorCode {
  if (typeof raw === "string" && raw in REGISTRY) return raw as ErrorCode;
  metrics.increment("error.code.undocumented", 1);
  logger.warn({ unknownCode: raw }, "Unregistered error code observed");
  return "INTERNAL_UNEXPECTED";
}
```

A registry that is validated by static coverage, runtime telemetry, and schema comparison stays
accurate as the codebase grows.

## Worked example — retiring a code safely

```text
2026-03  Add USER_NOT_FOUND. Deprecate USER_DOES_NOT_EXIST (emit both in transitional code path).
2026-04  Monitor: telemetry shows USER_DOES_NOT_EXIST still consumed by mobile v3.2.
2026-06  Mobile v3.2 reaches < 0.1% of traffic. Stop producing USER_DOES_NOT_EXIST.
2026-09  Zero consumers in telemetry for 30 days. Mark RETIRED; keep alias mapping.
2027-01  REMOVED from registry; alias removed; docs updated.
```

Each step is reversible until the last; none surprises a client.

## Key data / numbers

- **Deprecation window:** ≥ one release cycle; commonly **90 days** for external clients,
  **30 days** for internal-only.
- **Alias retention:** keep old→new aliases until telemetry shows **zero** consumers for **30 days**.
- **Unknown-code metric:** emit `error.code.undocumented` on every unrecognized code seen at a
  boundary.
- **Coverage tables** make a missing mapping a compile error, so "registered but unmapped" cannot
  ship.

## Real-world use case — Acme SaaS

Acme renamed `USER_DOES_NOT_EXIST` to `USER_NOT_FOUND`. They shipped an alias, emitted both codes
for a release, watched telemetry, and only removed the old code after mobile v3.2 dropped below
0.1% of traffic. In parallel, a CI scan found six codes thrown in adapters that were never
registered — each had been silently mapping to `500`. Registering them added correct HTTP statuses,
retry rules, and messages, and the `error.code.undocumented` metric now catches new gaps within a
day. No client broke, and six latent bugs surfaced.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Emit old + new | Safe, explicit | Duplicate data briefly | Public/external codes |
| Alias old → new | Simple mapping | Old code persists in docs | Internal, low-risk |
| Hard cutover | Clean | Breaks old clients | Only with no external consumers |
| Never deprecate (keep forever) | Zero breakage | Registry grows unbounded | Small systems |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Deprecate before removing | Delete a public code outright |
| Keep aliases until zero-consumer telemetry | Assume old clients are gone |
| Handle unknown codes gracefully in clients | Throw on unknown codes |
| Scan for unregistered codes in CI | Rely on tests to notice |
| Emit an undocumented-code metric | Silently map unknown codes to `500` |

## Common mistakes

- **Hard deletion** of a public code.
- **Repurposing** a deprecated code instead of adding a new one.
- **Clients that crash** on unknown codes.
- **No static scan**, so thrown-but-unregistered codes persist.
- **No telemetry**, so you cannot know when removal is safe.

## Checklist

- [ ] Is every code that is produced also registered?
- [ ] Are deprecated codes kept working through a documented window?
- [ ] Do clients handle unknown codes with a safe fallback?
- [ ] Is there a static scan for unregistered codes?
- [ ] Is there a runtime metric for undocumented codes?
- [ ] Is removal gated on zero-consumer telemetry?

## Related

- [Mapping Codes to Behavior](./04-mapping-codes-to-behavior.md)
- [Registry-as-Code and Collision Testing](../02-deep-dive/01-registry-as-code-and-collision-testing.md)
- [Backward Compatibility and Deprecation Mechanics](../02-deep-dive/02-backward-compatibility-and-deprecation.md)
