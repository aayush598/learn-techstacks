# Before/After Anti-Pattern Refactors

> Part XVII · Chapter 46 · Sections 46.13–46.25 (applied) · _Estimated reading time: 20 min_
> **Prerequisite:** [Handling Anti-Patterns](../01-concepts/04-handling-anti-patterns.md), [Design Anti-Patterns](../01-concepts/05-design-anti-patterns.md)

## In one sentence

Six real refactors, taken from Acme's audit backlog, each showing the anti-patterned code as
found, the refactor as shipped, and the one metric that proved the fix — one per major
anti-pattern family, sized so you can copy the diff shape into your own PRs.

## Why this matters in production

Anti-pattern write-ups age poorly; *diffs* age well. Each pair below is deliberately small —
the kind of change that fits one review — because the bottleneck in real remediation is not
understanding the rule, it is producing the unobjectionable PR that implements it under
delivery pressure. Copy the shape; keep the accompanying registry/policy discipline from
Chapter 45 or the fix will rot.

## Refactor 1 — Empty catch → explicit optional degradation (46.14)

```ts
// BEFORE — cache write failure invisible; stale dashboards, no signal.
async function saveDashboard(tenantId: string, data: Dashboard) {
  await db.dashboards.update(tenantId, data);
  try { await redis.set(dash:`dash:${tenantId}`, JSON.stringify(data)); } catch {}
}

// AFTER — optional by policy, documented at the site, measured.
async function saveDashboard(tenantId: string, data: Dashboard) {
  await db.dashboards.update(tenantId, data);          // required: failure fails the request
  // OPTIONAL: cache is best-effort; degrade = serve older cache or compute from db.
  try {
    await redis.set(dash:`dash:${tenantId}`, JSON(data), { px: CACHE_TTL_MS });
  } catch (err) {
    log.debug({ err, tenantId }, "dashboard cache write skipped");  // still optional
    metrics.increment("cache.write.skipped");
  }
}
```

**Metric:** cache-write failures went from invisible to a Grafana counter; one Redis incident
was diagnosed from the counter instead of from customer "stale data" reports.

## Refactor 2 — Catch-log-without-rethrow → classify and propagate (46.21 + 46.13)

```ts
// BEFORE — controller flattens everything; log-only catch upstream lies to the caller.
try { res.json(await projects.create(req.body, ctx)); }
catch (err) { log.error(err); res.status(500).json({ error: "Something went wrong" }); }

// BEFORE service — the log-only catch that made the 500 "fine":
try { await db.insert(project); }
catch (err) { log.error({ err }, "insert failed"); }     // swallowed; returns undefined!

// AFTER service — translation + rethrow of typed errors; no local serialization.
export async function create(input: ProjectInput, ctx: Ctx): Promise<Project> {
  try {
    return await repo.insert(input, ctx.tenantId);
  } catch (err) {
    throw fromPgError(err);   // 23505 → ProjectSlugTaken (409 via registry); cause kept
  }
}

// AFTER controller — no local catch at all; 46.1 global handler owns the exit.
router.post("/projects", async (req, res) => {
  res.status(201).json(await projects.create(req.body, req.ctx));
});
```

**Metric:** slug-conflict responses moved from generic 500 to registry-driven 409; the client
SDK's duplicate-submit branch (previously dead code) began working; "unexpected 500" rate on
this endpoint fell by ~70% (the remainder were true bugs, now correctly 500s).

## Refactor 3 — Success-shaped failure → honest status (46.22)

```ts
// BEFORE — declined card returns 200; every status-based consumer is wrong.
res.status(200).json({ success: false, error: { code: "CHECKOUT_CARD_DECLINED", message } });

// AFTER — registry mapping; the SDK, the gateway, and the dashboards agree again.
const result = await checkout.capture(id, ctx);          // throws typed errors
// global handler: REGISTRY["CHECKOUT_CARD_DECLINED"].httpStatus → 402 + RFC 9457 body.
```

**Metric:** the API gateway's retry policy (which retried only 5xx) stopped retrying declines;
client-side "payment failed" handling switched from parsing 200-bodies to status codes; the
billing-sync job stopped marking declined invoices as paid (its precondition had been
`response.ok`).

## Refactor 4 — Retry-all + repeated loops → one classified policy (46.23 + 46.20)

```ts
// BEFORE — three call sites, three loops, no classification, no jitter.
// worker:
for (let i = 0; i < 5; i++) { try { return await stripeRefund(id); } catch { await sleep(1000); } }
// api client:
for (let i = 0; i < 3; i++) { try { return await stripeRefund(id); } catch { await sleep(500); } }
// adapter (yes, really):
try { return await stripe.refunds.create(...); } catch { return await stripe.refunds.create(...); }

// AFTER — one policy; adapter translates only; callers reference the name.
// shared/resilience/retry-policies.ts
stripeHttp: { attempts: 3, baseDelayMs: 200, multiplier: 2, jitter: "full",
              retryOn: (e) => e.retryable && !e.code.endsWith("_AMBIGUOUS") },
// worker & api client:
const refund = await withRetry("stripeHttp", () => stripeRefund(id));
// adapter: fromStripeError only — no internal loop.
```

**Metric:** per logical refund, worst-case Stripe calls 30 (5×3×2) → 3. During the next
provider incident, Acme-originated refund calls dropped ~90% versus the previous incident of
similar vendor severity.

## Refactor 5 — Retry non-idempotent → key or surface ambiguity (46.24)

```ts
// BEFORE — capture re-run after timeout can double-charge.
try { return await stripe.charges.create({ amount }); }
catch { return await stripe.charges.create({ amount }); }   // blind second charge

// AFTER — idempotency key by construction; ambiguous outcomes are typed, not retried.
try {
  return await withRetry("stripeHttp", () =>
    stripe.charges.create({ amount }, { idempotencyKey: checkoutId }));
} catch (err) {
  if (isAmbiguousNetworkFailure(err)) {
    throw new PaymentAmbiguousOutcomeError(checkoutId, { cause: err });  // non-retryable
    // → reconciliation queue resolves via balance-transaction lookup
  }
  throw err;
}
```

**Metric:** duplicate-capture incidents: 1 in the trailing 12 months before → 0 in the 9
months after; ambiguous outcomes resolved by reconciliation in ≤ 2 hours median.

## Refactor 6 — Overengineering + class sprawl → behavior types + codes (46.17 + 46.25)

```ts
// BEFORE — 61 subclasses + a 1,100-line "error pipeline" framework with middleware hooks.
class StripeCardDeclined402Error extends AppError {}
class StripeCardInsufficientFunds402Error extends AppError {}
class StripeRateLimited503RetryableError extends AppError {}
// …58 more… plus registerHook("beforeClassify", fn) pipelines at every call site.

// AFTER — 14 behavior types; specificity in code + details; pipeline module deleted.
export class DependencyError extends AppError {
  readonly category = "dependency" as const;
  constructor(code: string, opts: { retryable: boolean; cause?: unknown }) {
    super(code, opts); this.retryable = opts.retryable;
  }
}
// adapter: new DependencyError("DEP_STRIPE_RATE_LIMITED", { retryable: true, cause: err })
// routing reads e.code / e.retryable / registry — no instanceof ladders.
```

**Metric:** lines of error-handling framework −85%; median time to add a new error code: 2
days (framework PR + review) → same-day single-module PR; no routing behavior changes were
needed because routing had always been metadata-driven after the Chapter 45 migration.

## Key data

- **Audit → backlog shape:** initial sweep found 41 instances across the six families; the
  twelve PRs implementing these six refactors closed 37 of them; the remaining 4 were inside
  a deprecated service on a deletion ticket.
- **Review sizes:** each refactor PR ≤ ~150 changed lines excluding tests; none required a
  flag-day; refactors 2 and 3 shipped in the same week because they touch the same boundary.
- **Sequencing:** refactors 2→4→5 (contract → classification → amplification) preceded 1 and 6,
  matching the remediation order from the deep-dive.

## Real-world use case — Acme SaaS

Refactor 5 was born from the double-charge escalation (design anti-patterns file). The customer
impact review forced the sequencing: idempotency keys first (day 1, payments on-call), ambiguous
typing second (day 3), reconciliation queue third (week 2). While keys landed, Refactor 4's
shared policy had to *exclude* non-keyed captures temporarily (`retryOn` false for captures) —
a deliberate conservative window where users saw slower refunds but zero duplicate risk. That
"temporarily less available, never twice-charged" trade is the fail-safe principle applied to
release sequencing, and it is the pattern to copy when your fix cannot land atomically.

## Trade-offs

| Refactor | Shortcut rejected | Why |
| -------- | ----------------- | --- |
| 1 | Deleting the try/catch entirely | The write is optional *by policy*; explicit optional > accidental required |
| 2 | Keeping a local catch that maps to one code | Registry + global handler already do it; local catch = second source of truth |
| 3 | Returning 200 for "soft declines" | Contract lies compound through every consumer |
| 4 | Keeping "just our loop" per team | Divergent loops are the anti-pattern; policy naming is cheaper than coordination |
| 5 | Retrying with "the same" charge | Without a key, "the same" is an assumption about a remote system you cannot verify |
| 6 | Renaming classes instead of collapsing | Renames preserve the nominal-taxonomy disease |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ship contract fixes (2, 3) before classification fixes | Start remediation at the "interesting" class collapse |
| Keep each PR ≤ one anti-pattern family | Bundle six refactors into one unreviewable PR |
| Pair every retry change with a policy-module edit | Fix one loop and leave five |
| Record the metric that motivated each fix | Refactor by taste without a measurement |

## Common mistakes

- **Refactor 3 without SDK coordination.** Changing 200→402/409/503 can break clients that
  parse only 200-bodies. Ship a contract changelog entry and, if needed, a versioned
  compatibility window at the serializer.
- **Refactor 4 while nested loops still exist in the vendor SDK.** Disable SDK-internal retries
  explicitly (`maxRetries: 0` in Stripe's SDK) or your "3 attempts" is fiction.
- **Refactor 6's half-collapse.** Collapsing classes while leaving `instanceof` switches in
  place just moves the sprawl into string comparisons with no registry backing.

## Checklist

- [ ] Each refactor family has a before/after in your own repo's PR history.
- [ ] Retry fixes touched the policy module, not only the call site.
- [ ] Contract changes shipped with client-communication and compatibility planning.
- [ ] The motivating metric is recorded in the PR description.
- [ ] CI greps for the fixed anti-patterns are enabled so they stay dead.

## Related

- [Acme Patterns Wired In](./01-acme-patterns-wired-in.md)
- [Anti-Pattern Compounding and Remediation](../02-deep-dive/02-anti-pattern-compounding-and-remediation.md)
- [Reference: Pattern Selection & Anti-Pattern Catalog](../05-reference/README.md)
