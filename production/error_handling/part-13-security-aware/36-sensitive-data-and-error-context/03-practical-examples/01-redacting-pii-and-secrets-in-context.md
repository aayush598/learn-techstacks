# Practical — Redacting PII and Secrets in Error Context

> Part XIII · Chapter 36 · Sections 36.2–36.6, 36.8 · _Estimated reading time: 20 min_
> **Prerequisite:** [Redaction, Omission, Sanitization, and Allowlists](../01-concepts/05-redaction-omission-sanitization-and-allowlists.md)

## In one sentence

This file builds a **redaction pass** that runs on top of the allowlist serializer as a backstop —
stripping PII, secrets, payment values, and query tokens from any string or value that survives the
allowlist (usually unavoidable third-party text), with a canary test that proves it works.

## Why this matters in production

The allowlist is the primary control: it prevents *your* fields from leaking. But two sources bypass it:

1. **Third-party text** — a provider message you must store for debugging.
2. **Values nested inside an allowlisted string** — a `provider` or `message` that a library filled with
   the request (including its URL, headers, or body).

Redaction is the backstop for exactly these. It is not a substitute for the allowlist; it is the second
layer that catches text your code did not author.

## Step 1 — Redaction patterns

```ts
interface RedactionRule {
  name: string;
  re: RegExp;
  replace: string;
}

const RULES: RedactionRule[] = [
  // Credentials / tokens
  { name: "bearer",   re: /(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+/g, replace: "Bearer [REDACTED]" },
  { name: "stripe",   re: /\b(sk|rk)_(live|test)_[A-Za-z0-9]+/g,  replace: "[REDACTED_KEY]" },
  { name: "aws",      re: /\bAKIA[0-9A-Z]{16}\b/g,                replace: "[REDACTED_AWS_KEY]" },
  { name: "jwt",      re: /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g,
                       replace: "[REDACTED_JWT]" },
  { name: "pem",      re: /-----BEGIN[^-]+KEY-----[\s\S]+?-----END[^-]+KEY-----/g,
                       replace: "[REDACTED_PEM]" },
  { name: "basicAuth",re: /(?i)\b(authorization|cookie)\s*[:=]\s*[^\s,;]+/g,
                       replace: "$1: [REDACTED]" },
];

const PII_RULES: RedactionRule[] = [
  { name: "email", re: /\b[\w.+-]+@[\w-]+\.[\w.-]+\b/g, replace: "[REDACTED_EMAIL]" },
  { name: "pan",   re: /\b(?:\d[ -]?){13,19}\b/g,       replace: "[REDACTED_PAN]" },
  { name: "ssn",   re: /\b\d{3}-\d{2}-\d{4}\b/g,        replace: "[REDACTED_SSN]" },
  { name: "phone", re: /\b\+?\d{1,3}[-. ]?\d{3}[-. ]?\d{3,4}[-. ]?\d{3,4}\b/g,
                   replace: "[REDACTED_PHONE]" },
];

const QUERY_RULES: RedactionRule[] = [
  { name: "querySecret",
    re: /([?&](?:token|key|api_key|apikey|password|code|secret)=)[^&#\s]+/gi,
    replace: "$1[REDACTED]" },
];
```

> ⚠️ **Hazard.** Regexes over-match and mis-match: the PAN pattern can hit timestamps and order sizes.
> Treat redaction as a **backstop**, keep patterns conservative, and prefer omission/allowlist for
> values you control. Test against a corpus of real samples to tune false positives.

## Step 2 — Apply redaction to strings and deep values

```ts
function redactString(input: string): string {
  let out = input;
  for (const rule of [...RULES, ...PII_RULES, ...QUERY_RULES]) {
    out = out.replace(rule.re, rule.replace);
  }
  return out;
}

function redactDeep<T>(value: T, depth = 0): T {
  if (depth > 6) return value;
  if (typeof value === "string") return redactString(value) as T;
  if (Array.isArray(value)) return value.map((v) => redactDeep(v, depth + 1)) as T;
  if (value && typeof value === "object") {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out[k] = redactDeep(v, depth + 1);
    }
    return out as T;
  }
  return value;
}
```

`redactDeep` handles nested structures (including the cause chain nodes) with a depth bound.

## Step 3 — Wire it as a backstop after the allowlist

```ts
function serializeForSink(err: unknown, ctx: Record<string, unknown>, sink: Sink) {
  const allowed = safeSerialize(err, ctx, { sink }); // primary: allowlist
  return redactDeep(allowed);                         // backstop: redact survivors
}
```

Order matters: **allowlist first, redact second.** The allowlist removes fields you should not emit;
redaction cleans the third-party text that legitimately remains.

## Step 4 — Prove it with a canary corpus

```ts
const CANARIES = {
  stripeKey: "sk_live_CANARY0000000000",
  jwt: "eyJhbGciOiJIUzI1NiJ9.CANARY.SIGNATURE",
  email: "canary@example.com",
  pan: "4111111111111111",
  queryToken: "?token=CANARY_SECRET",
};

test("no canary survives a sink", () => {
  const hostile = Object.assign(new Error("upstream failed"), {
    code: "UPSTREAM_ERROR",
    message: `call failed: GET /d${CANARIES.queryToken} Bearer ${CANARIES.stripeKey}`,
    provider: `Stripe sk_live_CANARY0000000000, user ${CANARIES.email}, card ${CANARIES.pan}`,
    cause: new Error(`jwt ${CANARIES.jwt}`),
  });
  const ctx = { code: "UPSTREAM_ERROR", message: hostile.message, provider: hostile.provider };

  for (const sink of ["response", "log", "metric", "dlq", "tracker"] as const) {
    const out = JSON.stringify(serializeForSink(hostile, ctx, sink));
    for (const [name, value] of Object.entries(CANARIES)) {
      expect(out, `${sink} leaked ${name}`).not.toContain(value);
    }
  }
});
```

Run this in CI; it is the guarantee that both layers hold together.

## Step 5 — Handling hash-and-range backstops

For values you must correlate but not show, replace rather than mask:

```ts
{ name: "correlateEmail", re: /\b[\w.+-]+@[\w-]+\.[\w.-]+\b/g,
  replace: (m) => `[email:${fingerprint(m)}]` } // per-concept fingerprint
```

This keeps debugging useful without storing PII.

## Key data / numbers

- **CWE-532** (sensitive info in logs), **CWE-311/CWE-312** (missing/cleartext protection), **CWE-359**
  (private personal information).
- **PCI DSS Req 3.3/10.3**: PAN never logged; card data excluded from logs.
- **GDPR Art. 32/33**: minimization/pseudonymization; breach notification within 72 hours.
- **Bounds**: depth 6, and keep patterns conservative to limit false positives.

## Real-world use case — Acme SaaS

Acme's LLM adapter stored the raw provider error text in the `AgentRun` tracker. The text occasionally
included the prompt (customer content) and, in one provider's format, the API key. Acme added the
redaction backstop after the allowlist, so provider text is now scanned for keys, JWTs, emails, and card
numbers even when it is stored. The canary corpus above runs in CI across all sinks. A follow-up review
found the LLM adapter could instead map the provider error to a stable code, so the raw text was removed
entirely (omission) — the strongest fix — and redaction remained as the backstop for the remaining
integrations.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Allowlist + redaction backstop | Defense in depth | Regex tuning/false positives | Any third-party text |
| Allowlist only | Clean, no false positives | Provider text may contain secrets | If you omit provider text |
| Redaction only | Catches unknowns | Misses new shapes | Never as primary |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Run allowlist first, redaction second | Redact the whole object as the only control |
| Keep patterns conservative | Use a greedy PAN regex everywhere |
| Redact deep (arrays, causes) with a bound | Redact only the top-level string |
| Fingerprint for correlation | Store the raw value |
| Run a canary corpus in CI | Assume redaction works |

## Common mistakes

- **Redaction as the primary control.** Misses new shapes.
- **Over-broad patterns.** Corrupt legitimate values.
- **Redacting only strings, not nested objects.** Nested values leak.
- **No canary test.** The guarantee is unverified.
- **Forgetting query strings.** Tokens ride in URLs.

## Checklist

- [ ] Does redaction run **after** the allowlist as a backstop?
- [ ] Are nested arrays and cause nodes redacted with a depth bound?
- [ ] Are query-string secrets handled?
- [ ] Are patterns conservative and tested for false positives?
- [ ] Does a canary corpus cover every sink in CI?
- [ ] Are values that need correlation fingerprinted, not stored?

## Related

- [Context Allowlist for Errors](./02-context-allowlist-for-errors.md)
- [Secrets and Tokens](../01-concepts/02-secrets-and-tokens.md)
- [Payment, Financial, Query, and Third-Party Context](../01-concepts/04-payment-financial-query-and-third-party.md)
- [Chapter 34 — Redaction Strategy](../../34-security-principles-for-error-handling/02-deep-dive/03-redaction-strategy.md)
- [Glossary](../../../GLOSSARY.md)
