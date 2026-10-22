# Deep Dive — Safe Serialization and Context Allowlists

> Part XIII · Chapter 36 · Sections 36.9–36.11 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Redaction, Omission, Sanitization, and Allowlists](../01-concepts/05-redaction-omission-sanitization-and-allowlists.md)

## In one sentence

**Safe serialization** means the error context is emitted through a **per-sink allowlist** with bounded
size and depth, where unclassified fields are denied, strings from untrusted sources are sanitized, and
the serializer itself can never throw — so a leak is a structural impossibility rather than a
discipline.

## Why this matters in production

Serialization is where all the classification and redaction work either holds or collapses. A single
`JSON.stringify(err)` re-opens every leak the rest of the design closed. This file specifies the
mechanics: the allowlist data structure, the string sanitizer, the size/depth bounds, the fail-safe
wrapper, and the tests that keep them honest.

## The allowlist data structure

Model each sink as a set of permitted **keys**, not a set of forbidden patterns:

```ts
type Sink = "response" | "log" | "metric" | "tracker" | "dlq" | "support";

interface FieldSpec {
  key: string;
  sensitivity: "public" | "internal" | "tenant" | "sensitive" | "pii";
  maxLen?: number;      // bound string length
  sanitize?: boolean;   // strip control chars, untrusted source
}

const FIELDS: Record<string, FieldSpec> = {
  code:       { key: "code", sensitivity: "public" },
  message:    { key: "message", sensitivity: "public", maxLen: 300, sanitize: true },
  requestId:  { key: "requestId", sensitivity: "public" },
  class:      { key: "class", sensitivity: "internal" },
  provider:   { key: "provider", sensitivity: "internal" },
  tenantId:   { key: "tenantId", sensitivity: "sensitive" },
  userId:     { key: "userId", sensitivity: "sensitive" },
  stack:      { key: "stack", sensitivity: "internal", maxLen: 8000, sanitize: true },
  field:      { key: "field", sensitivity: "public" },
  rule:       { key: "rule", sensitivity: "public" },
};

const SINK_FIELDS: Record<Sink, string[]> = {
  response: ["code", "message", "requestId", "field", "rule"],
  metric:   ["code", "provider"],
  log:      ["code", "message", "class", "provider", "requestId", "field", "rule"],
  tracker:  ["code", "message", "class", "provider", "requestId", "tenantId", "userId", "stack"],
  dlq:      ["code", "message", "class", "requestId", "tenantId"],
  support:  ["code", "message", "requestId", "tenantId"],
};
```

Two properties follow automatically:

- **New field → denied everywhere** until added to a sink list. (`cardNumber` cannot leak.)
- **Sensitivity lives in one table**, so policy changes are one edit, not a hunt.

## The string sanitizer

Untrusted strings (provider messages, native error text) need sanitization before they enter any sink:

```ts
export function sanitizeText(input: string, maxLen = 300): string {
  if (typeof input !== "string") return "";
  return input
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "") // control chars
    .replace(/[\r\n\t]+/g, " ")                                       // newlines/tabs
    .replace(/\s{2,}/g, " ")
    .slice(0, maxLen)
    .trim();
}
```

For HTML sinks, additionally escape `<`, `>`, `&`, `"`, `'`. For header sinks, strip CR/LF entirely.

## The serializer

```ts
interface SerializeOptions {
  sink: Sink;
  maxDepth?: number; // default 6
}

export function safeSerialize(
  err: unknown,
  ctx: Record<string, unknown>,
  opts: SerializeOptions,
): Record<string, unknown> {
  try {
    const allowedKeys = SINK_FIELDS[opts.sink];
    const out: Record<string, unknown> = {};

    for (const key of allowedKeys) {
      const spec = FIELDS[key];
      const raw = ctx[key];
      if (raw === undefined || spec === undefined) continue;

      let value = raw;
      if (typeof value === "string") {
        if (spec.maxLen) value = value.slice(0, spec.maxLen);
        if (spec.sanitize) value = sanitizeText(value as string, spec.maxLen ?? 300);
      }
      out[key] = value;
    }

    // Cause chain handled by serializeChain (bounded, per-node sanitized).
    if (err instanceof Error && "cause" in err) {
      out.cause = serializeChain((err as any).cause, opts.sink, 1);
    }
    return out;
  } catch {
    // The serializer must never throw; fail to the generic public shape.
    return { code: "INTERNAL_ERROR", message: "Something went wrong." };
  }
}
```

The `try/catch` is mandatory: a serializer that throws turns a handled error into an unhandled one.

## Bounds

| Bound | Default | Purpose |
| ----- | ------- | ------- |
| String length | 300 (message), 8000 (stack) | Prevent bulk payloads |
| Cause depth | 6 | Prevent cycles/unbounded chains |
| Chain node count | 10 | Prevent aggregate blowup |
| Total serialized size | a few KB | Prevent response/record bloat |

## Context builder pattern

Pair the serializer with a builder that classifies at the source:

```ts
function buildContext(req: Request, principal: Principal, extra: Record<string, unknown>) {
  return {
    requestId: req.id,
    tenantId: principal.tenantId,
    class: extra.class,
    provider: extra.provider,
    field: extra.field,
    rule: extra.rule,
    // never: req.body, req.query, raw provider payload
  };
}
```

`req.body` and `req.query` never enter the context; if a field is needed, it is extracted and classified.

## Testing

```ts
test("new unclassified field never reaches any sink", () => {
  const ctx = { code: "X", cardNumber: "4111111111111111" }; // not in FIELDS
  for (const sink of Object.keys(SINK_FIELDS) as Sink[]) {
    const out = JSON.stringify(safeSerialize(new Error("x"), ctx, { sink }));
    expect(out).not.toContain("4111111111111111");
  }
});

test("serializer never throws on hostile input", () => {
  const cyc: any = { code: "X" };
  cyc.self = cyc;
  expect(() => safeSerialize(cyc, cyc, { sink: "log" })).not.toThrow();
});
```

## Key data / numbers

- **CWE-209 / CWE-532 / CWE-502**: info in messages, sensitive info in logs, unsafe deserialization.
- **Allowlist principle**: deny unknown fields; the property that makes new fields safe by default.
- **Bounds**: depth 6, chain nodes 10, message 300 chars, stack 8000 chars, total a few KB.
- **Fail-safe**: serializer wrapped in `try/catch`, always returns the generic public shape on failure.

## Real-world use case — Acme SaaS

Acme's shared `safeSerialize` replaced `JSON.stringify(err)` in the global handler, the logger, and the
DLQ writer. On rollout, the "new unclassified field" test failed because `support` tooling depended on a
`resolvedAt` timestamp that was not in `FIELDS`; the fix was to classify it `internal` and add it to
`support` — a deliberate decision recorded in review rather than an accidental leak. The serializer's
`try/catch` also caught a cyclic context object in `AgentRun` that had previously thrown inside the
global handler and produced a double response. Both were caught by the standard tests.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Per-sink key allowlist | New fields denied | Must classify needed fields | Default |
| Sensitivity-tagged fields | Policy in one table | Slightly more setup | Multi-sink systems |
| Raw `JSON.stringify` | Zero effort | Leaks everything, can throw | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Emit only allowlisted keys | Emit the whole context object |
| Bound strings, depth, and chain size | Serialize unbounded |
| Sanitize untrusted strings | Store raw provider text |
| Wrap the serializer in `try/catch` | Let it throw |
| Classify needed fields deliberately | Add fields ad hoc |

## Common mistakes

- **`JSON.stringify(err)`.** The anti-pattern this replaces.
- **Serializer that throws.** Turns handled into unhandled.
- **No length/depth bounds.** Bulk payloads and cycles.
- **Sanitizing only the top-level string.** Nested values leak.
- **Denylist.** New fields leak.

## Checklist

- [ ] Is serialization driven by a per-sink key allowlist?
- [ ] Are sensitivity, max length, and sanitize flags in one table?
- [ ] Are strings, depth, and chain size bounded?
- [ ] Can the serializer never throw?
- [ ] Does a test prove a new unclassified field is denied everywhere?
- [ ] Is `JSON.stringify(err)` absent from all error paths?

## Related

- [Nested Causes and Leakage via Chains](./01-nested-causes-and-leakage-via-chains.md)
- [Redaction, Omission, Sanitization, and Allowlists](../01-concepts/05-redaction-omission-sanitization-and-allowlists.md)
- [Practical: Context Allowlist for Errors](../03-practical-examples/02-context-allowlist-for-errors.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Glossary](../../../GLOSSARY.md)
