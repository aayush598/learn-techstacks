# Principles of Graceful Degradation

> Part XI · Chapter 30 · Sections 30.1–30.2 · _Estimated reading time: 17 min_
> **Prerequisite:** [Chapter 30 — Graceful Degradation and Fallbacks](../README.md)

## In one sentence

Graceful degradation means **pre-deciding what the system will give up, and what it will never give
up**, so that failure reduces the product instead of breaking it or corrupting it.

## Why this matters in production

Every system degrades under failure — the only question is whether it degrades *by design* or *by
accident*. Accidental degradation looks like empty dashboards, missing emails, blank recommendations,
and 500s on the checkout page all at once. Designed degradation looks like a search page that says
"personalized results unavailable," a checkout that still works while recommendations are hidden, and
a dashboard that serves cached data labelled with its age. The difference is a classification done
before the incident.

## 30.1 — Principles

### 1. Preserve correctness over completeness

A reduced but correct answer beats a complete but wrong one. If the price service is unavailable, do
not render an order total from a stale cache without labeling it; fail the checkout instead.

### 2. Degrade in proportion to criticality

Not every feature deserves the same protection. Ranking capabilities lets you spend scarce capacity on
what matters.

### 3. Make degradation visible

Every degraded response should be observable to the caller and to operators: a header, a field, a UI
banner, a metric. Silent degradation becomes silent inaccuracy.

### 4. Bound the fallback

A fallback must have its own timeout and budget. An unbounded fallback (e.g. "query the primary if the
cache fails") can turn a cache outage into a database outage.

### 5. Prefer reversible, low-risk fallbacks

Cached data, static templates, and disabled features are safer than writing partial state or
guessing. Prefer "omit" over "invent."

### 6. Test the degraded path

A fallback that has never run in staging will fail in production. Exercise it with fault injection.

### 7. Recovery is part of the design

Degradation must be reversible without a deploy, and the system must return to full behavior
automatically (or via a documented switch) when the dependency recovers.

## 30.2 — Required vs optional

Classify every capability on two axes: **can the user complete the core task without it?** and **can we
produce a correct result without it?**

```text
                    correct without dependency?
                         yes            no
core task    yes   |  OPTIONAL     |  IMPORTANT   |
needs it?    no    |  DECORATIVE   |  REQUIRED    |
```

| Class | Definition | Failure behavior |
| ----- | ---------- | ---------------- |
| **Required** | Core task impossible or incorrect | **Fail closed** with a clear error |
| **Important** | Task possible but meaningfully worse | Degrade with a visible notice |
| **Optional** | Nice-to-have enhancement | Hide/disable silently (log + metric) |
| **Decorative** | Cosmetic | Omit, no user notice |

### Acme's classification

| Capability | Class | Why | Mode |
| ---------- | ----- | --- | ---- |
| Payment authorization | Required | Cannot ship unpaid orders | Fail-closed |
| Auth / session validation | Required | Cannot trust identity | Fail-closed |
| Inventory reservation | Required | Oversell risk | Fail-closed |
| Order total calculation | Required | Wrong money | Fail-closed |
| Email receipt | Important | Order still valid | Queue and retry |
| Search results | Important | Core browse still works | Cached results, labelled |
| Recommendations | Optional | No effect on task | Hide |
| LLM summary (`AgentRun`) | Optional | Human can read source | Template fallback |
| Analytics events | Decorative | No user impact | Drop with counter |
| Avatar images | Decorative | Cosmetic | Placeholder |

### The classification is a product decision

Engineering can propose the class, but product must agree. "Recommendations are optional" is a
business statement. Write the classification in the same place as the dependency policy, and review it
when the product changes.

## Worked example — one request, three classes

```text
GET /checkout/summary
  ├─ session validation      REQUIRED   → fail 401/503 if unavailable
  ├─ cart items              REQUIRED   → fail 503 if unavailable
  ├─ order total             REQUIRED   → fail 503 if unavailable
  ├─ tax estimate            IMPORTANT  → cached estimate + "may change" flag
  ├─ shipping ETA            OPTIONAL   → omit if unavailable
  └─ product recommendations OPTIONAL   → omit if unavailable
```

The endpoint returns `200` with `Degraded: tax-estimate` when only the tax service is down. If the
cart service is down, it returns `503` — there is no correct reduced response.

## Key data / numbers

- Classification dimensions: **2** (core task, correctness).
- Typical split: **10–20%** required, **20–30%** important, rest optional/decorative.
- Fallback budget: ≤ **20%** of the user's total deadline.
- Degraded response should be labeled within **1 header + 1 body field**.
- Review classification at least **quarterly** and on major product changes.

## Real-world use case — Acme SaaS

Acme's dashboard originally treated every widget as required: one failed recommendations call turned
the whole page into an error. After classification, only account balance and invoice status remained
required. Recommendations, usage charts, and the LLM summary became optional with their own
fallbacks. During a provider incident the next quarter, the dashboard stayed up with three widgets
showing "temporarily unavailable," and support tickets about a "broken dashboard" dropped from
hundreds to a handful.

## Trade-offs

| Choice | Benefit | Cost |
| ------ | ------- | ---- |
| Many optional features | Resilience | More fallback paths to maintain |
| Few required features | Availability | Harder product decisions |
| Visible degradation | Trust, debuggability | Some user discomfort |
| Silent omission | Clean UI | Risk of unnoticed failure |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every capability | Treat all dependencies as critical |
| Let product own the classification | Decide criticality only in code |
| Preserve correctness over completeness | Serve wrong data to stay up |
| Make degradation visible | Silently omit required data |
| Bound every fallback | Let fallbacks run unbounded |
| Test degraded paths | Assume fallbacks work |

## Common mistakes

- **Classifying everything as required**, so one optional dependency takes down the page.
- **Classifying everything as optional**, so payments degrade into corruption.
- **No owner** for the classification, so it drifts from the product.
- **Never exercising fallbacks**, so they break silently.
- **Treating "available" as success** without checking correctness.

## Checklist

- [ ] Every dependency and capability has a class.
- [ ] Product has signed off on required vs optional.
- [ ] Required capabilities fail closed.
- [ ] Important/optional capabilities have bounded fallbacks.
- [ ] Degradation is observable (header, body, metric).
- [ ] Degraded paths are tested with fault injection.
- [ ] Classification is reviewed on product changes.

## Related

- [Fallback Responses and Cached Fallbacks](./02-fallback-responses-and-cached-fallbacks.md)
- [Fail-Open vs Fail-Closed](../02-deep-dive/02-fail-open-vs-closed.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
