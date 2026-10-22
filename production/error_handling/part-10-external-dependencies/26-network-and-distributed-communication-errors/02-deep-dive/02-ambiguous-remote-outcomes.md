# Ambiguous Remote Outcomes

> Part X · Chapter 26 · Sections 26.13–26.16 · _Estimated reading time: 16 min_

## In one sentence

**The fundamental ambiguity is: after sending a request, a timeout/reset means you don't know if the remote side executed it** — this must be modeled explicitly and resolved with idempotency, status checks, or reconciliation.

## Why this matters in production

**Checkout** sends `capture` to payment gateway. Read timeout occurs. If gateway already captured, retrying creates double charge. If it didn't, retrying is needed. There is no local signal — only uncertainty. This is the "two generals" flavor in practice.

## Core concept

Ambiguity arises when:
- **Full request sent** (write complete), then **read timeout** or **connection reset** before response.
- **Partial write** then failure — usually safe to assume not fully processed.
- **Connect timeout** — request never sent, no ambiguity.
- **Lost response after success** — remote succeeded, client lost response.

Handling strategies:
1. **Idempotency keys** — server deduplicates retries.
2. **State verification** — query to see actual state.
3. **Design operations to be queryable/verifiable**.
4. **For financial/non-idempotent, never blindly retry**; resolve via reconciliation.
5. **Mark as `uncertain`** and handle via compensation path.

## How it works

### Decision tree
```text
Did request start sending? 
  No (connect failure) → no ambiguity, retry if idempotent-safe class
  Yes (wrote at least partially)
    Was full write complete?
      No → likely not processed → retry may be safe only if idempotent
      Yes → sent complete request; response lost → AMBIGUOUS (remote may have succeeded)
        Action: do NOT blindly retry non-idempotent; use idempotency + status check
```

### Idempotency requirement
- Mutating operations must accept idempotency key.
- On retry with same key, server returns previous result or consistent outcome.
- Without this, ambiguous case cannot be safely retried.

## Worked example

```ts
interface NetErr {
  ambiguous: boolean;
  phase: "connect"|"write"|"read";
  requestSent: boolean; // full request sent?
  idempotentOnly: boolean;
}

async function safeCapture(id: string) {
  const idem = `capture:${id}`;
  try {
    return await pay.capture(id, idem);
  } catch (e: NetErr) {
    if (e.ambiguous && e.phase === "read" && e.requestSent) {
      // Check status
      const s = await pay.getStatus(id);
      if (s.captured) return { ok: true, deduped: true };
      if (s.requiresCapture) return await pay.capture(id, idem); // retry safe
      throw e;
    }
    throw e;
  }
}
```

**Key data:**
- **Ambiguity window** is between write completion and response receipt.
- **Financial systems** often require reconciliation jobs for uncertain outcomes.

## Real-world use case

**Checkout at Acme SaaS:** Gateway captures payment but response lost due to LB idle timeout (read timeout). Without handling, we would retry → potential double capture or fail order. With status check after ambiguous timeout, we detect "captured" and mark order paid correctly.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Assume failed** | Safe from double-charge | Leaves revenue unrecognized | Conservative, bad UX |
| **Assume succeeded** | Consistent if true | Double-charge risk | **Never** |
| **Idem + status lookup** | Safe | Requires provider support for status | **Recommended** for critical |
| **Reconciliation** | Handles provider that can't query well | Delayed resolution | When status lookup impossible |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Detect ambiguity explicitly | Treat read timeout as simple failure |
| Require idempotency for mutations | Retry non-idempotent blindly |
| Implement status check for critical ops | Guess without verification |
| Record uncertainty | Lose the fact it was ambiguous |
| Use reconciliation as fallback | Assume immediate certainty |

## Common mistakes

- **Blind retry on read timeout** — major source of duplicates.
- **No idempotency keys** — can't safely retry even with them.
- **No query endpoint** — hard to resolve ambiguity.

## Checklist

- [ ] Ambiguity detected by phase + requestSent.
- [ ] Mutations support idempotency keys.
- [ ] Critical ops have status lookup or reconciliation.
- [ ] Uncertain outcomes logged and tracked.

## Related

- [Lost Responses and Retries Safely](../03-practical-examples/02-handling-lost-responses-and-retries-safely.md)
- [Ambiguous Outcomes and Service Boundaries](../01-concepts/04-ambiguous-outcomes-and-service-boundaries.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../../GLOSSARY.md)
