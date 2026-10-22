# The Abstraction Cost Model: When a Shared Layer Pays for Itself

> Part XXII · Chapter 56 · Sections 56.17, 56.2, 56.11, 56.12 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 53 — Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)

## In one sentence

An error-handling abstraction is worth its cost when it **removes a decision from N callers**
for a cost proportional to N; if it removes no decision, or if only one caller exists, it is
**indirection you pay for forever**.

## Why this matters in production

Error handling attracts abstractions faster than any other part of a codebase, because errors
feel like they need a *framework*. The result is a package that:

- has 12 configuration options and a plugin system,
- must be versioned independently of the app,
- is understood by nobody outside the team that wrote it,
- and still leaves every call site writing `try { ... } catch (e) { throw new Wrapper(e) }`.

The team's belief is "we will reuse this across services". The reality is that reuse across
services requires the abstraction to be *stable*, and stability requires it to be *small*, and
smallness is exactly what a framework is not.

This deep dive gives you a **cost model** so the decision can be made with numbers instead of
taste.

## The cost model

An abstraction layer costs you three things and saves you two.

```text
  SAVES                                   COSTS
  ┌───────────────────────────────┐       ┌───────────────────────────────┐
  │ S1 Decision duplication       │       │ C1 Setup / migration cost     │
  │    N callers × D decisions    │       │    one-time, high              │
  │                               │       │                               │
  │ S2 Consistency drift risk     │       │ C2 Indirection cost           │
  │    N callers × P drift prob.  │       │    per call site, forever      │
  │                               │       │                               │
  │ S3 Change amplification       │       │ C3 Cognitive + ownership cost │
  │    1 change instead of N      │       │    per reader, forever        │
  └───────────────────────────────┘       └───────────────────────────────┘
```

The break-even test is simply **S > C**, with the weighting below.

### Quantifying each term

| Term | How to estimate | Example (Acme: a shared retry helper) |
| ---- | --------------- | ------------------------------------ |
| S1 | `N` callers × `D` duplicated decisions each | 8 call sites × 2 decisions (attempts, backoff) = 16 |
| S2 | `N` × `P` probability of a drift per year | 8 × 0.25 = 2 incidents/year |
| S3 | `(N − 1) × C_change` hours saved per policy change | 7 × 0.5 h = 3.5 h per change |
| C1 | Hours to build, document, and migrate | 16 h |
| C2 | `N` × `A` extra hops/complexity per call site (in reviewer-minutes) | 8 × 6 min ≈ 0.8 h per review cycle |
| C3 | Minutes for a new engineer to learn the layer; multiplied by readers | 20 min × 12 engineers = 4 h |

Break-even for the retry helper: savings ≈ 16 + 2 + 3.5 = **21.5 units**; costs ≈ 16 + 0.8 +
4 = **20.8 units**. Break-even — but the margin is thin, and the helper must then be *kept
correct*, forever. That thin margin is the signal: **this is a "maybe", not a "yes"**.

### The four-question gate

Apply these before the arithmetic, because a "no" on any of them ends the discussion:

1. **Does the layer hide a decision?** If the caller still chooses the timeout, the retry
   count, and the error mapping, the layer is decoration.
2. **Are there 3+ real consumers?** One consumer is a private helper.
3. **Is the concept product-neutral?** No product codes, no vendor types, no business nouns.
4. **Can a new engineer use it without reading the source?** ≤ 10 options, obvious names.

## How it works (mechanics)

### The indirection tax, measured

Each layer in the error path costs something concrete at every call site. Here is the
accounting for a request that goes through a generic HTTP wrapper, a retry helper, a
translator, and a global handler:

```text
  Call site                     Cost                          Who notices
  ─────────────────────────────────────────────────────────────────────────
  await httpGet(url)            +1 stack frame, unknown        reviewer
  await retry(() => ...)        +1 frame, closure alloc,       reviewer,
                                 policy lookup                 on-call
  throw translate(err)          +1 frame, try/catch noise      reviewer
  app.use(errorHandler)         invisible here                 —
```

Four hops for a request that performs one HTTP call. The overhead is not the runtime cost
(microseconds) — it is that **every reader of the call site must now hold four policies in
their head** to answer "what happens if this fails?".

The mitigation is not "remove all layers". It is:

> **Every layer must remove a decision, and the layer must be visible at the call site.**

```ts
// ❌ Four policies hidden behind one call.
const data = await client.get("/projects");

// ✅ The policy is visible: the caller knows the deadline, the retry shape, and the failure.
const data = await stripeClient.charges.list({ limit: 20 }, {
  timeoutMs: 2_000,
  retry: stripeRetryPolicy,        // named, documented, owned
});
```

### When a shared layer is the wrong answer

| Situation | Why sharing hurts |
| --------- | ----------------- |
| The concept encodes one team's assumption | Becomes everyone's constraint; first dissenter forks it |
| The callers need *different* policies | The layer grows a mode flag per caller |
| The layer's API changes faster than its consumers | Version churn across repositories |
| Only one service needs it now | A package boundary with no benefit |
| It hides the vendor's semantics | You lose the ability to special-case the vendor |

### The bounded-hierarchy variant

The alternative to a universal hierarchy is a **bounded hierarchy**: one small tree per domain
sharing a global base. The cost model favors it because:

- The base is genuinely shared and genuinely neutral (it earns the 3-consumer threshold).
- Domain classes stay feature-owned, so no shared package has to change when a domain changes.
- New teams copy a 40-line template instead of depending on a 40-page framework.

```text
  packages/errors-core/          (shared: 1 file, ~120 lines, 0 product codes)
    AppError · Result · classify · redact · registry types

  features/checkout/errors.ts    (owned by the Checkout team, ~80 lines)
    CheckoutError = { code: CheckoutCode; step: CheckoutStep; ... }
```

The shared surface is small enough to stay stable for years, which is exactly what a
cross-repository dependency needs.

### A worked break-even for the two common candidates

**Candidate A — a shared retry framework.**

- Consumers today: 9 call sites across 3 features → passes the 3-consumer gate.
- Decisions removed: attempts, backoff shape, jitter, deadline, retryable check → 5 decisions
  removed per call site.
- Neutrality: yes (no vendor, no product).
- Verdict: **extract**, but as a *named policy table* plus a 30-line function — not a
  framework with pluggable backoff strategies.

**Candidate B — a shared error serialization framework.**

- Consumers today: 2 (one HTTP app, one worker) → fails the 3-consumer gate.
- Decisions removed: RFC 9457 shape, redaction, status lookup → 3 decisions.
- Neutrality: partially — "the shape of an API error" is product-adjacent.
- Verdict: **do not extract**. Duplicate 30 lines in two places; revisit at 3 consumers.

## Key data / numbers

| Metric | Threshold | Notes |
| ------ | --------- | ----- |
| Real consumers for a shared abstraction | ≥ 3 | Counted from production imports |
| Decisions removed by the layer | ≥ 1 | A layer that removes none is indirection |
| Configuration options in a shared layer | ≤ 10 | Above that, it is a framework |
| Error-path hops from call site to handler | ≤ 3 | More than 3 means policies are hidden |
| Max lines in a shared error package | ~300 | Past that, it needs to be split |
| Product codes in a shared package | 0 | Any product code makes it feature-owned |
| Shared package release cadence | ≤ 1 per quarter | Faster means the abstraction is not stable |
| Break-even margin required | ≥ 2× savings | Thin margins do not survive maintenance |
| New-engineer onboarding time for the layer | ≤ 20 min | Above that it needs to be smaller |

## Real-world use case — Acme SaaS

Acme started with `packages/error-handler` (a framework) because three teams were writing
HTTP error responses. It grew to 1,400 lines and 14 options, and it was on the critical path
of every release: changing the response shape meant releasing the package and bumping three
apps.

The team ran the cost model:

| Term | Value |
| ---- | ----- |
| S1 decision duplication | 3 apps × 4 decisions = 12 |
| S2 drift risk | 3 apps × 0.3 = ~1 incident/year |
| S3 change amplification | 2 × 1 h = 2 h per shape change |
| C1 setup + migration | 40 h (initial) + 6 h per release cycle |
| C2 indirection | 3 apps × 8 min per review cycle |
| C3 cognitive + ownership | 25 min × 9 engineers = 3.75 h, recurring |

Savings ≈ 15 units; costs ≈ 50+ units, and the costs were **recurring** while the savings
were one-off. The verdict was unambiguous: **the abstraction cost more than it saved.**

The replacement was deliberately boring:

- `packages/errors-core` (≈ 300 lines): `AppError`, `Result`, `classify`, `redact`, and the
  registry *types*. No product codes, no HTTP knowledge.
- `src/shared/registry/error-codes.ts`: pure data, one entry per code, generated docs.
- `src/transports/http/serialize-problem.ts`: 60 lines per transport, owned by the API team.
- `src/transports/jobs/serialize-failure.ts`: 40 lines, owned by the worker team.

The duplication that was "eliminated" turned out to be 100 lines of transport-specific
serialization — which *should* differ, because an HTTP problem and a job failure record are
different shapes.

Measured outcome after two quarters: response-shape changes went from 3 days (package release
+ 3 app bumps) to 40 minutes; the number of "which layer owns this?" questions in code review
dropped to near zero; and the framework's 14 configuration options became 3 registry fields.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Full shared framework | Maximum uniformity | High setup cost, recurring cognitive cost, version churn | Never in a multi-team SaaS |
| Small shared core + local policy | Low cost, high clarity | Some duplication in transports | **Default** |
| Purely local (no shared layer) | Zero indirection | Inconsistent shapes; duplicated redaction | Small services only |
| Bounded hierarchies + shared base | Vocabulary stays local, base is shared | Slight duplication at the base | **Default for medium/large codebases** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Gate every proposed abstraction on the four questions | Extract on first use |
| Measure S vs C before building | Assume "DRY" is free |
| Keep the shared package under ~300 lines and 10 options | Let it grow configuration options |
| Make the policy visible at the call site (`retryPolicy`) | Hide four policies behind `client.get()` |
| Keep product codes out of shared packages | Put `CHECKOUT_*` in the core package |
| Revisit a "no" when the 3-consumer threshold is met | Force a shared layer to justify itself repeatedly |

## Common mistakes

- **Extracting during an incident.** A framework built at 2 a.m. to fix one bug will be
  designed around that bug and will outlive the incident by years.
- **Confusing "used by 3 teams" with "3 consumers of the concept".** Three teams can use the
  same package for three different reasons and still need different policies.
- **Counting theoretical consumers.** "The platform team will also use it" is not a consumer.
- **Letting the abstraction absorb business decisions.** The moment the shared layer knows
  about `CHECKOUT_CARD_DECLINED`, it is not shared any more — it is Acme's checkout code with
  extra steps.
- **Never deleting it.** The classic end state: two ways to do everything, and nobody knows
  which is canonical.

## Checklist

- [ ] Every proposed shared abstraction passes the four-question gate.
- [ ] The break-even arithmetic is written down (S vs C) before building.
- [ ] The layer removes at least one decision from each caller.
- [ ] The shared package has 0 product codes and ≤ 10 options.
- [ ] The error path from call site to handler is ≤ 3 hops.
- [ ] The policy is visible at the call site.
- [ ] A named owner and a removal/deprecation plan exist for every shared layer.

## Related

- [Fidelity and Risk (56.8, 56.13, 56.17, 56.18)](./01-concepts/04-fidelity-and-risk.md)
- [Structure and Ownership (56.2, 56.3, 56.9–56.12)](../01-concepts/02-structure-and-ownership.md)
- [Chapter 54 — Reusable Error-Handling Infrastructure](../../../part-21-maintainability/54-reusable-error-handling-infrastructure/README.md)
- [Chapter 53 — Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
