# Practical — Context Allowlist for Errors

> Part XIII · Chapter 36 · Sections 36.7, 36.10–36.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [Deep Dive: Safe Serialization and Context Allowlists](../02-deep-dive/02-safe-serialization-and-context-allowlists.md)

## In one sentence

This file builds the **allowlist context builder + safe chain serializer** as one small module —
`buildContext` classifies fields at the source, `project` emits only sink-permitted keys, and
`serializeChain` walks nested causes with per-node sanitization and bounds.

## Why this matters in production

This module is the single artifact that makes "no sensitive data leaves" a reviewable property. Instead
of auditing forty catch blocks, you audit one builder, one allowlist table, and one chain serializer —
and a canary test proves all three together. It is deliberately small so it can be understood at a
glance and cannot rot into a leak.

## Module layout

```text
error-context.ts
├── FIELDS               // field → sensitivity, bounds
├── SINK_FIELDS          // sink → permitted keys
├── buildContext()       // classify at the source
├── project()            // allowlist projection for a sink
├── sanitizeText()       // control-char/length normalization
└── serializeChain()     // bounded, per-node sanitized cause walk
```

## Step 1 — The classification table

```ts
type Sink = "response" | "log" | "metric" | "tracker" | "dlq" | "support";

interface FieldSpec {
  sensitivity: "public" | "internal" | "tenant" | "sensitive" | "pii";
  maxLen?: number;
  sanitize?: boolean;
  fingerprint?: boolean; // store a non-reversible token instead of the value
}

export const FIELDS: Record<string, FieldSpec> = {
  code:      { sensitivity: "public" },
  message:   { sensitivity: "public", maxLen: 300, sanitize: true },
  requestId: { sensitivity: "public" },
  field:     { sensitivity: "public" },
  rule:      { sensitivity: "public" },
  class:     { sensitivity: "internal" },
  provider:  { sensitivity: "internal" },
  stack:     { sensitivity: "internal", maxLen: 8000, sanitize: true },
  tenantId:  { sensitivity: "sensitive" },
  userId:    { sensitivity: "sensitive" },
  userFp:    { sensitivity: "internal", fingerprint: true }, // pseudonym, not PII
};

export const SINK_FIELDS: Record<Sink, string[]> = {
  response: ["code", "message", "requestId", "field", "rule"],
  metric:   ["code", "provider"],
  log:      ["code", "message", "class", "provider", "requestId", "field", "rule", "userFp"],
  tracker:  ["code", "message", "class", "provider", "requestId", "tenantId", "userFp", "stack"],
  dlq:      ["code", "message", "class", "requestId", "tenantId"],
  support:  ["code", "message", "requestId", "tenantId"],
};
```

## Step 2 — Build context at the source

```ts
interface Principal { id: string; tenantId: string }

export function buildContext(
  req: { id: string },
  principal: Principal,
  extra: { class?: string; provider?: string; field?: string; rule?: string },
) {
  // Omit: req.body, req.query, raw provider payloads — never entered here.
  return {
    requestId: req.id,
    tenantId: principal.tenantId,
    userFp: fingerprint(principal.id), // pseudonym for correlation (salted hash)
    class: extra.class,
    provider: extra.provider,
    field: extra.field,
    rule: extra.rule,
  };
}
```

Note: the builder never receives the request body or query. If a field is needed, it is extracted and
passed explicitly through `extra`; everything else cannot leak because it was never collected.

## Step 3 — Project for a sink

```ts
export function project(ctx: Record<string, unknown>, sink: Sink): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const key of SINK_FIELDS[sink]) {
    const spec = FIELDS[key];
    const value = ctx[key];
    if (value === undefined || spec === undefined) continue; // unknown key => dropped

    if (typeof value === "string") {
      out[key] = spec.sanitize
        ? sanitizeText(value, spec.maxLen ?? 300)
        : spec.maxLen
          ? value.slice(0, spec.maxLen)
          : value;
    } else {
      out[key] = value;
    }
  }
  return out;
}
```

## Step 4 — Serialize the cause chain

```ts
const MAX_DEPTH = 6;
const MAX_NODES = 10;

export function serializeChain(
  err: unknown,
  sink: Sink,
  depth = 0,
  seen = new Set<unknown>(),
  budget = { nodes: 0 },
): unknown {
  if (depth > MAX_DEPTH || budget.nodes >= MAX_NODES) return "[truncated]";
  if (seen.has(err)) return "[cycle]";
  seen.add(err);
  budget.nodes++;

  if (!(err instanceof Error)) return "[non-error omitted]";

  const ctx = (err as any).context ?? {}; // app errors carry classified context
  const node: Record<string, unknown> = {
    code: (err as any).code ?? "UNKNOWN",
    ...project(ctx, sink),
  };

  // Native/non-app errors: tracker may see sanitized message only.
  if (!("code" in err)) {
    const safe = sink === "tracker" ? { code: "UNKNOWN", message: sanitizeText(err.message) } : "[omitted]";
    if ((err as any).cause) (safe as any).cause = serializeChain((err as any).cause, sink, depth + 1, seen, budget);
    return safe;
  }

  if ((err as any).cause !== undefined) {
    node.cause = serializeChain((err as any).cause, sink, depth + 1, seen, budget);
  }
  return node;
}
```

## Step 5 — Compose with the redaction backstop

```ts
import { redactDeep } from "./redact";

export function errorForSink(err: unknown, sink: Sink, ctx: Record<string, unknown>) {
  try {
    const base = { ...project(ctx, sink), ...(serializeChain(err, sink) as object) };
    return redactDeep(base); // backstop for third-party text
  } catch {
    return { code: "INTERNAL_ERROR", message: "Something went wrong." }; // fail-safe
  }
}
```

## Step 6 — The full test matrix

```ts
test("allowlist denies unknown fields everywhere", () => {
  const ctx = { code: "X", cardNumber: "4111111111111111", ssoSubject: "sub_canary" };
  for (const sink of Object.keys(SINK_FIELDS) as Sink[]) {
    const out = JSON.stringify(errorForSink(new Error("x"), sink, ctx));
    expect(out).not.toContain("4111111111111111");
    expect(out).not.toContain("sub_canary");
  }
});

test("chain serialization bounds depth and cycles", () => {
  const a: any = Object.assign(new Error("a"), { code: "A" });
  const b: any = Object.assign(new Error("b"), { code: "B", cause: a });
  a.cause = b; // cycle
  const out = JSON.stringify(serializeChain(b, "log"));
  expect(out).toContain("[cycle]");
});

test("serializer never throws", () => {
  expect(() => errorForSink({ weird: true }, "log", {})).not.toThrow();
});
```

## Key data / numbers

- **CWE-209** (info in messages), **CWE-532** (sensitive info in logs), **CWE-359** (private personal
  information), **CWE-502** (unsafe deserialization).
- **Bounds**: depth 6, nodes 10, message 300 chars, stack 8000 chars.
- **Deny-by-default**: any key absent from `FIELDS`/`SINK_FIELDS` is dropped.
- **Fail-safe**: `errorForSink` returns the generic public shape if anything throws.

## Real-world use case — Acme SaaS

Acme replaced its per-module error logging with this single `error-context` module across `Checkout`,
`WebhookIngest`, `ExportJob`, and `AgentRun`. The test matrix caught three unclassified fields during
migration (`ssoSubject`, `cardBrand`, and a `providerAccount`) — none reached a sink; each was either
classified to the tracker/support or dropped. Because `buildContext` never receives `req.body` or
`req.query`, the entire class of payload leaks became structurally impossible, and new endpoints
inherited the guarantee by construction. Code review of error context reduced to "is this field
classified?".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One module (builder + allowlist + chain) | Auditable, testable | Must classify needed fields | Default everywhere |
| Per-module logging | Local control | Inconsistent, leak-prone | Never |
| Raw serialization | Easy | Leaks everything | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Build context with an explicit classifier | Pass `req.body`/`req.query` |
| Drop unknown keys | Emit all keys |
| Sanitize + bound every string | Serialize unbounded |
| Bound and cycle-check chain walks | Walk causes freely |
| Fingerprint identifiers for correlation | Store raw identifiers |

## Common mistakes

- **Builder that accepts the whole request.** Reintroduces the leak.
- **Allowlist with a wildcard.** Deny unknown, always.
- **Unbounded chain walk.** Cycles/blowup.
- **Serializer that throws.** Fail-safe to generic.
- **No test matrix.** The guarantee is unverified.

## Checklist

- [ ] Does `buildContext` only accept classified, explicit fields?
- [ ] Are unknown keys dropped at every sink?
- [ ] Are strings sanitized and length-bounded?
- [ ] Is the cause chain bounded and cycle-checked?
- [ ] Is the serializer fail-safe (never throws)?
- [ ] Does the test matrix cover unknown fields, cycles, and hostile input?

## Related

- [Redacting PII and Secrets in Context](./01-redacting-pii-and-secrets-in-context.md)
- [Deep Dive: Safe Serialization and Context Allowlists](../02-deep-dive/02-safe-serialization-and-context-allowlists.md)
- [Deep Dive: Nested Causes and Leakage via Chains](../02-deep-dive/01-nested-causes-and-leakage-via-chains.md)
- [Chapter 34 — Error Sanitizer and Allowlist Serializer](../../34-security-principles-for-error-handling/03-practical-examples/01-error-sanitizer-allowlist-serializer.md)
- [Glossary](../../../GLOSSARY.md)
