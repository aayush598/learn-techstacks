# Anti-Pattern Compounding and Remediation

> Part XVII · Chapter 46 · Sections 46.13–46.25 (remediation) · _Estimated reading time: 15 min_
> **Prerequisite:** [Handling Anti-Patterns](../01-concepts/04-handling-anti-patterns.md), [Design Anti-Patterns](../01-concepts/05-design-anti-patterns.md)

## In one sentence

Anti-patterns rarely cause incidents alone — they **compound** in predictable chains (swallow →
success-shaped → retry-blind), so remediation must be ordered by the chain, not by the individual
line, or you will fix the leaf and keep the tree.

## Why this matters in production

A code-review culture that flags individual lines under-fixes: the empty catch gets deleted, and
the swallow-and-continue underneath it remains because "at least we log now." Incident reviews
that blame one file miss the *chain* that turned a vendor 429 into a customer-visible outage.
This file gives you the known chains, the compounding math, and a remediation order that
dismantles the chain rather than its latest link.

## The five compounding chains

```text
CHAIN A — The silent-success chain (data corruption)
  46.14 empty catch / 46.21 catch-log-no-rethrow
      └▶ 46.15 swallow-and-continue (state invalid, flow continues)
           └▶ 46.22 success-shaped failure (contract tells clients it worked)
                └▶ dashboards green, incident discovered by customer/auditor

CHAIN B — The amplification chain (outage spread)
  46.23 retry-all (no classification)
       └▶ 46.20 repeated/nested retry loops (attempts multiply)
            └▶ provider incident → your traffic spike → your pool exhaustion
                 └▶ 46.13 catch-all flattens the exhaustion into generic 500s
                      └▶ no classification → more retries (loop closes)

CHAIN C — The double-side-effect chain (money)
  ambiguous failure (timeout after remote commit)
       └▶ 46.24 retry non-idempotent operation
            └▶ duplicate charge / duplicate invite / duplicate row
                 └▶ 46.18 generic message hides which op duplicated
                      └▶ support refund loop, audit finding

CHAIN D — The debuggability collapse chain (MTTR blow-up)
  46.19 deep wrappers per layer
       └▶ cause chain lost / truncated in DLQ serialization
            └▶ 46.18 generic messages at the outermost wrapper
                 └▶ 46.13 catch-all returns one generic 500
                      └▶ MTTR measured in hours, not minutes

CHAIN E — The abstraction death-spiral (delivery freeze)
  46.17 excessive classes (nominal taxonomy)
       └▶ teams unsure which class/code to use → invent 46.17 again
            └▶ 46.25 overengineering response: more framework to "standardize"
                 └▶ every new error needs framework PR → error changes stop
                      └▶ 46.21/46.15 return as the path of least resistance
```

## Compounding math (why chains beat individual lines)

Two illustrative models, both seen in the field:

- **Attempt multiplication (Chain B).** Caller loop 3 attempts × adapter-internal loop 2
  attempts × provider SDK default 2 retries = **up to 12 provider calls per logical
  operation**. Under a provider incident with 1,000 logical ops/minute, that is 12,000 calls/
  minute against a dependency that is already failing — your retry layer is now the outage.
- **Visibility loss (Chain D).** Each wrapper hop that re-creates the error without `cause`
  drops one segment of stack/context. Three hops + a generic message = the DLQ entry
  `Error: An error occurred` with zero fields: the failure exists in the system but not in any
  human's model of it. Time-to-identify shifts from minutes (code + correlation id) to hours
  (repro + archaeology).

## The remediation playbook (ordered)

Order matters: **contract first, then classification, then amplification, then structure.**

| Order | Step | Targets | Why first/later |
| ----- | ---- | ------- | --------------- |
| 1 | **Fix the contract.** Eliminate success-shaped failures (46.22) and generic 500 flattening (46.13) at transports. | Chains A, D, B (observability) | If the outside world lies, nothing downstream can be trusted or measured |
| 2 | **Restore classification.** Wire registry + adapter translation; default unknown → non-retryable (46.23). | Chains B, C | Retries and alerts need honest metadata before you touch loops |
| 3 | **Kill amplification.** Collapse repeated/nested retries into named policies; enforce idempotency keys or AMBIGUOUS_OUTCOME (46.20, 46.24). | Chains B, C | Highest incident-severity reduction per line changed |
| 4 | **Close the swallows.** Every catch: rethrow / recover / documented-optional (46.14, 46.21, 46.15). | Chain A | Now safe: surfacing failures produces *classified* failures, not noise |
| 5 | **Simplify the type graph.** Collapse behavior-less classes; strip deep wrappers to translation-only (46.17, 46.19). | Chains D, E | Pure refactors; safest after the contract is stable |
| 6 | **Prune speculative machinery.** Delete mechanisms without justification; reinstate on measured need (46.25). | Chain E | Last: deletion is only safe when the surrounding contracts are honest |

Each step is a shippable PR series; do not batch 1+3 or the review becomes unreviewable.

## Worked example — executing step 3 on Chain C

```ts
// BEFORE — Chain C live in one function: ambiguous failure + non-idempotent retry + generic msg.
async function captureV1(checkoutId: string, amount: number) {
  for (let i = 0; i < 3; i++) {
    try { return await stripe.charges.create({ amount, currency: "usd" }); }
    catch { await sleep(1000); }               // 46.23 + 46.24
  }
  throw new Error("Payment failed");           // 46.18
}

// AFTER — step 3 executed: key makes retry legal; ambiguous outcomes surface; code is typed.
async function captureV2(checkoutId: string, amount: number) {
  return withRetry("stripeHttp", () =>
    stripe.charges.create(
      { amount, currency: "usd" },
      { idempotencyKey: checkoutId },          // retries now safe by construction
    ).catch((err) => {
      // timeout/reset AFTER request sent, key unknown state → do not blind-retry:
      if (isAmbiguousNetworkFailure(err)) {
        throw new PaymentAmbiguousOutcomeError(checkoutId, { cause: err }); // non-retryable
      }
      throw fromStripeError(err);              // classified; policy decides the rest
    }));
}
```

The reconciliation queue consumes `PAYMENT_AMBIGUOUS_OUTCOME` and resolves via
balance-transaction lookup — the ambiguity is *handled*, not *retried into a duplicate*.

## Key data

- **Remediation sequencing at Acme:** six weeks, steps 1→3 in weeks 1–3 (three PRs), steps 4–5
  in weeks 4–5 (eleven PRs, mostly mechanical), step 6 in week 6 (deleted one unused breaker
  and a 1,100-line "universal error pipeline" module).
- **Severity proxy per chain (field judgment):** Chain C (money) and Chain A (silent data
  corruption) rank highest — customer-auditable harm; Chain B next (shared-outage amplifier);
  Chains D and E are efficiency/MTTR costs that *raise* the cost of everything else.
- **Re-audit yield:** after the ordered remediation, the same grep suite that found 41 instances
  found 4 (all new, in feature code merged during the weeks — i.e. the guardrails from steps
  1–3 caught most new occurrences at review time).
- **Catch-site census used in step 4:** each catch must end in exactly one of three forms —
  `throw` (rethrow/translate), `return <recovery>`, or `catch` + explicit `// OPTIONAL:` comment
  with degradation. Anything else fails review.

## Real-world use case — Acme SaaS

`ExportJob` exhibited Chain A end-to-end: per-row parse failures were swallowed with a warn log
(46.21), the job record was written with `status: "succeeded"` regardless (46.22 at the job
contract), and the customer saw a green "Export complete" with missing rows — discovered only
when their finance team flagged it. Remediation followed the order: (1) job result became
`succeeded | succeeded_with_warnings | failed` with warnings serialized via the job serializer
(contract first); (2) parse failures typed and registered (`EXPORT_ROWS_SKIPPED`);
(4) swallows removed — each row failure now lands in the warnings list or fails the job if
above threshold. Customer-visible outcome: honest partial-success reports; support category
"export missing data" tickets went to zero over the next quarter, and the two that would have
been filed were self-served from the report.

## Trade-offs

| Approach | Pros | Cons | When |
| ---------- | ---- | ---- | ---- |
| Ordered chain remediation (recommended) | Incidents drop stepwise; each step measurable | Six-week programs feel slow vs "fix the line" | Any live product with ≥ 1 compounded chain |
| Per-line cleanup sprints | Fast visible wins | Chains re-form at the next link | Toy repos only |
| Big-bang rewrite of error handling | One review | No intermediate value; high regression risk | Never on a live system |
| Fix only the incident's leaf | Closes the ticket | Chain survives; next incident in months | Explicitly reject this in postmortems |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the chain in the postmortem, not just the file | Blame the last `catch` in the stack |
| Execute remediation in the six-step order | Start with the "interesting" refactor (step 5/6) |
| Make each catch end in throw/recover/document-optional | Accept "we log it now" as step 4 completion |
| Re-run the grep suite after remediation | Assume the program finished when the PRs merged |

## Common mistakes

- **Step 4 before step 1.** Surfacing swallowed errors into an unclassified 500-world produces
  alert floods and rollbacks the program. Contract and classification first.
- **Skipping step 2 for speed.** Killing nested retries without a classification-driven
  `retryOn` leaves retry-all live in the shared module — quieter, same amplification.
- **Postmortems that name files, not patterns.** Without pattern names, the same chain
  reappears in the next feature because nothing diffused into review culture.

## Checklist

- [ ] Postmortems classify error-handling defects by anti-pattern ID.
- [ ] Remediation programs follow the six-step order; each step has exit greps.
- [ ] Every catch site ends in throw / recovery / documented-optional.
- [ ] The grep suite from the initial audit runs in CI (empty catches, log-only catches,
      success:false, numeric attempts).
- [ ] Step 6 (prune) is scheduled, not skipped.

## Related

- [Handling Anti-Patterns](../01-concepts/04-handling-anti-patterns.md)
- [Design Anti-Patterns](../01-concepts/05-design-anti-patterns.md)
- [Before/After Anti-Pattern Refactors](../03-practical-examples/02-before-after-anti-pattern-refactors.md)
