# Webhook Signature Verification — Mechanics

> Part XII · Chapter 33 · Section 33.10 (mechanics) · _Estimated reading time: 15 min_
> **Prerequisite:** [Webhook Signatures, Retries, and Timeouts](../01-concepts/04-webhook-signatures-retries-timeouts.md)

## In one sentence

Verification is **HMAC over `timestamp + "." + raw body` compared in constant time, within a
timestamp tolerance** — every deviation (parsed body, naive compare, no timestamp check) opens either
a forgery or a replay hole.

## Why this matters in production

A webhook endpoint is a public, unauthenticated POST. Without verification, an attacker can send
`{"type":"invoice.paid","data":{"tenantId":"ten_victim"}}` and grant a free subscription. With a
naive implementation, an attacker can also replay a previously valid signed request indefinitely, or
infer the expected signature byte-by-byte through timing. This is a security boundary, so the
mechanics must be exact.

## The signed payload

Providers sign a **string composed of a timestamp and the raw body**, not just the body, so a captured
signature cannot be reused with a different timestamp:

```text
signed_payload = "{timestamp}.{raw_body}"
signature      = HMAC_SHA256(signing_secret, signed_payload)
header         = "t={timestamp},v1={hex_signature}"
```

```text
Stripe-Signature: t=1729502520,v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
                   │            │
                   │            └─ HMAC-SHA256 hex
                   └─ Unix seconds
```

Multiple `v1` values may appear during secret rotation; accept if **any** matches.

## The five failure modes

| # | Mistake | Consequence | Fix |
| - | ------- | ----------- | --- |
| 1 | Parse JSON before verifying | HMAC over re-serialized bytes differs | Verify on raw body |
| 2 | `===` comparison | Timing side channel | `timingSafeEqual` |
| 3 | No timestamp check | Replay forever | Tolerance window |
| 4 | `JSON.parse` fallback on failure | Processing unsigned input | Reject |
| 5 | Trusting the client's clock | Skew breaks valid webhooks | Server time, allow skew |

## Raw body handling per framework

The body must be captured as bytes **before** any JSON middleware mutates it.

### Express

```ts
// Route-specific raw parser; do NOT use express.json() on this route.
app.post("/webhooks/stripe", express.raw({ type: "application/json", limit: "1mb" }), handler);
```

If a global `express.json()` runs first, `req.body` is an object and the raw bytes are gone. Options:
mount the webhook route before the JSON middleware, or use `verify: (req, _res, buf) => { req.rawBody = buf }`.

### Fastify

```ts
fastify.addContentTypeParser(
  "application/json",
  { parseAs: "buffer" },
  (req, body, done) => done(null, body), // keep Buffer; parse after verification
);
```

### Go

```go
body, err := io.ReadAll(io.LimitReader(r.Body, 1<<20))
if err != nil { http.Error(w, "bad body", http.StatusBadRequest); return }
// verify(body) before json.Unmarshal
```

## Constant-time comparison

```ts
import crypto from "node:crypto";

function safeEqualHex(a: string, b: string): boolean {
  const ba = Buffer.from(a, "hex");
  const bb = Buffer.from(b, "hex");
  if (ba.length !== bb.length) return false;       // lengths must match first
  return crypto.timingSafeEqual(ba, bb);
}
```

`timingSafeEqual` requires equal lengths and throws otherwise. A plain `===` short-circuits on the
first differing byte, leaking information to an attacker who can time responses.

## Timestamp tolerance

```ts
const toleranceSec = 300; // Stripe default
const now = Math.floor(Date.now() / 1000);
if (Math.abs(now - timestamp) > toleranceSec) return false;
```

Why this matters: a valid signature captured today can be replayed tomorrow. The timestamp binds the
signature to a time window. Use the **server's** clock, not the sender's. Allow a small skew (a few
minutes) because clocks drift.

> ⚠️ **Hazard.** A tolerance measured in hours (or omitted) turns a leaked webhook body into a
> permanent replay credential.

## Key rotation

Providers rotate signing secrets. Support **two active secrets** during rotation:

```ts
const secrets = [process.env.STRIPE_SECRET_CURRENT!, process.env.STRIPE_SECRET_PREVIOUS!].filter(Boolean);

function verifyWithRotation(rawBody: Buffer, header: string): boolean {
  return secrets.some((secret) => verifyStripe(rawBody, header, secret));
}
```

If the header includes a key id, select the secret by id; otherwise try each. Log which secret matched
(an indicator) without logging the secret.

## Full verifier

```ts
export function verifyStripe(rawBody: Buffer, header: string | undefined, secrets: string[], toleranceSec = 300): boolean {
  if (!header) return false;
  const fields = header.split(",").map((p) => p.split("="));
  const timestamp = Number(fields.find(([k]) => k === "t")?.[1]);
  if (!Number.isFinite(timestamp)) return false;
  if (Math.abs(Date.now() / 1000 - timestamp) > toleranceSec) return false;

  const provided = fields.filter(([k]) => k === "v1").map(([, v]) => v);
  if (provided.length === 0) return false;

  return secrets.some((secret) => {
    const expected = crypto.createHmac("sha256", secret).update(`${timestamp}.${rawBody.toString("utf8")}`).digest("hex");
    return provided.some((sig) => sig.length === expected.length && crypto.timingSafeEqual(Buffer.from(sig, "hex"), Buffer.from(expected, "hex")));
  });
}
```

## Test vectors

Always test with a fixed secret and body:

```ts
const secret = "whsec_test_secret";
const t = 1729502520;
const body = Buffer.from('{"id":"evt_1","type":"invoice.paid"}');
const sig = crypto.createHmac("sha256", secret).update(`${t}.${body.toString("utf8")}`).digest("hex");

expect(verifyStripe(body, `t=${t},v1=${sig}`, [secret])).toBe(true);
expect(verifyStripe(body, `t=${t},v1=${sig}`, ["wrong"])).toBe(false);
expect(verifyStripe(body, `t=${t - 400},v1=${sig}`, [secret])).toBe(false); // stale
```

Add a case where the body is valid but the signature is for a different body, and a case with a
tampered timestamp.

## Worked example — WebhookIngest rejection

```ts
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), (req, res) => {
  const ok = verifyStripe(req.body, req.get("Stripe-Signature"), [SECRET]);
  if (!ok) {
    metrics.increment("webhook_signature_rejected");
    return res.status(400).json({ error: "invalid_signature" });
  }
  const event = JSON.parse(req.body.toString("utf8"));
  void enqueue(event);
  res.status(200).json({ received: true });
});
```

A forged request is rejected **before** it reaches the queue, and a replayed valid request outside the
tolerance window is rejected the same way.

## Key data / numbers

- Stripe header: `Stripe-Signature`; format `t=<unix>,v1=<hex>`; HMAC-SHA256.
- Stripe default tolerance: **300 s**.
- GitHub header: `X-Hub-Signature-256` (`sha256=<hex>` over the raw body, no timestamp).
- HMAC output: 32 bytes / 64 hex characters for SHA-256.
- `crypto.timingSafeEqual` requires equal-length buffers.
- Body size limit: enforce one (e.g. 1 MiB) to avoid memory exhaustion.

## Real-world use case — Acme SaaS

Acme's handler used `express.json()`, then `JSON.stringify(req.body)` for the HMAC. It worked for
months because Stripe's JSON happened to serialize identically — until a payload contained a Unicode
escape that re-serialized differently, and every webhook began failing signature checks. Billing
stopped for 20 minutes. They switched to `express.raw()` on the webhook route, added a fixed test
vector to CI, and added an alert on signature-rejection rate. No failures since.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| HMAC + timestamp | Prevents forgery and replay | Shared secret management | Default |
| HMAC only | Simpler | Replay possible | Idempotent, low-risk events |
| Mutual TLS | Strong identity | Cert management | B2B integrations |
| IP allowlist | Simple | Spoofable, brittle | Defense in depth only |
| No verification | None | Full forgery | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify on raw bytes | Verify on parsed/re-serialized JSON |
| Use constant-time compare | Use `===` |
| Enforce a timestamp tolerance | Accept old signatures |
| Support two secrets during rotation | Replace secrets atomically |
| Reject before parsing business data | Process then verify |
| Test with fixed vectors | Rely on live traffic |

## Common mistakes

- **Global JSON middleware** — raw body unavailable.
- **`JSON.stringify` for HMAC** — key order/whitespace changes the digest.
- **Comparing hex as strings** — timing leak.
- **No length check before `timingSafeEqual`** — throws and becomes a 500.
- **Tolerance in hours** — replay window too large.

## Checklist

- [ ] Is the webhook route using a raw-body parser?
- [ ] Is verification done before JSON parsing?
- [ ] Is the signature compared in constant time?
- [ ] Is there a timestamp tolerance using server time?
- [ ] Are multiple v1 signatures accepted during rotation?
- [ ] Are rejection reasons measured (without leaking secrets)?
- [ ] Are there fixed test vectors in CI?
- [ ] Is there a body-size limit?

## Related

- [Webhook Signatures, Retries, and Timeouts](../01-concepts/04-webhook-signatures-retries-timeouts.md)
- [WebhookIngest Dedupe and Signature](../03-practical-examples/01-webhookingest-dedupe-and-signature.md)
- [Webhook Signatures, Retries, and Timeouts](../01-concepts/04-webhook-signatures-retries-timeouts.md)
- [Chapter 33 — Event Do's and Don'ts](../04-dos-and-donts/README.md)
