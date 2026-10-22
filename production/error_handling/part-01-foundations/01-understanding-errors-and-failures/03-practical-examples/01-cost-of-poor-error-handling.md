# The Cost of Poor Error Handling

> Part I · Chapter 1 · Section 1.17 · _Estimated reading time: 15 min_

## In one sentence

Poor error handling is not a style issue — it converts recoverable blips into outages, silent
corruption, security incidents, and support costs that compound as you scale.

## Why this matters in production

This file exists so that "we should improve error handling" becomes a business argument, not an
aesthetic one. The costs below are the reasons error handling is a first-class architectural
concern.

## The five cost centers

| Cost center | Mechanism | Example symptom |
| ----------- | --------- | --------------- |
| **Availability** | Unhandled failure cascades | One dependency's timeout 500s the whole site |
| **Data integrity** | Silent swallow / partial failure | Duplicate rows, double charges, stuck state |
| **Security** | Over-disclosure in errors | Stack traces / SQL / secrets leaked to users |
| **Engineering velocity** | Inconsistent, duplicated handling | Every new feature reinvents recovery |
| **Support & trust** | Unclear, unactionable messages | "Error 500" tickets, churn, churn-driven refunds |

## Availability: the cascade

A single un-timed-out call to a slow dependency ties up workers. Workers fill, the request queue
backs up, health checks fail, the load balancer removes instances, and a partial dependency
degradation becomes a full outage.

```text
Slow dep → no timeout → requests pile up → pool exhausted → 503s → LB drains → outage
```

The fix is not "handle errors"; it is a **classification + policy** chain: timeout (transient),
bulkhead (isolate), breaker (stop calling), fallback (degrade). Every link is an error-handling
decision.

### Quantified

- A 30-minute outage on a SaaS with a 99.9% SLA can incur contractual SLA credits.
- Retry storms can *extend* an outage indefinitely by re-loading a recovering dependency.
- Cascading retries without jitter create synchronized load spikes every backoff interval.

## Data integrity: the silent corruption

The most expensive failures are the quiet ones.

```ts
// Anti-pattern: swallow and continue
try {
  await db.insert(order);
} catch (e) {
  // ignore
}
await chargeCard(order); // now running on an order that may not exist
```

Outcomes: a charge with no order, a fulfilled order with no charge, a job marked "done" that did
nothing. These are not just bugs; they are **audit findings** and, in finance, compliance
liabilities.

## Security: the disclosure channel

Error messages are a classic data-exfiltration channel:

- A raw SQL error reveals table/column names (schema leakage).
- A stack trace reveals file paths, library versions, internal hostnames.
- A "user not found" vs "wrong password" difference enables **user enumeration**.
- A serialized error object can leak tokens in `cause` chains.

Chapter 34 covers this in depth; here, note that the *cost* is breaches and fines, not just
embarrassment.

## Engineering velocity: the tax

Without a standard:

- Every developer invents their own error classes and messages.
- Bugs appear because one handler treats a transient error as permanent and another does the
  reverse.
- Onboarding takes weeks because error behavior is tribal knowledge.
- Adding one new provider requires touching many unrelated files.

A reusable standard (Chapters 54, 59) removes this tax. The whole point of this book is to make
that tax near-zero.

## Support and trust: the human cost

- "Something went wrong" forces users to file tickets, which humans must triage.
- A support ticket costs real money; thousands of avoidable ones are a line item.
- Unpredictable error behavior erodes trust, which shows up as churn and lower expansion.

## A worked micro-cost model

For a mid-size SaaS:

| Factor | Poor handling | Production-grade |
| ------ | ------------- | ---------------- |
| Avoidable downtime / quarter | 4 h | 0.5 h |
| Support tickets / 1k users / mo | 40 | 8 |
| Data-integrity incidents / yr | 3 | 0.2 |
| New-provider integration effort | 3 days | 4 hours |

The direction is always the same: **the cost is paid either up front (design) or repeatedly
(incidents).** Production-grade handling is an investment with compounding returns.

## Real-world use case — Checkout

A startup's checkout swallowed a `capture` failure "to avoid blocking the user," then marked the
order paid. Customers received goods without being charged; the bug ran undetected for weeks
because it produced *no error signal*. The eventual fix — fail-fast on capture, mark order
`pending`, retry idempotently — eliminated both the revenue leak and the audit exposure.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat error handling as an investment | Defer it "until after launch" |
| Measure incidents, tickets, integrity events | Argue only about code style |
| Make the cost visible to non-engineers | Assume correctness is obvious |

## Common mistakes

- **Optimizing for "never show an error"** instead of "fail correctly."
- **Ignoring silent failures** because they produce no alert.
- **Treating disclosure as harmless** because "it's just a stack trace."

## Checklist

- [ ] Can you name your top three error-related costs?
- [ ] Do you have a metric for silent/partial failures?
- [ ] Are public errors free of internals?
- [ ] Does adding a provider touch only one adapter?

## Related

- [Failure Domains and Fault Boundaries](../02-deep-dive/01-failure-domains-and-fault-boundaries.md)
- [Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [Part XXI — Maintainability](../../../part-21-maintainability/README.md)
