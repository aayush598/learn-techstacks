# Chapter 56 — Reference

> Part XXII · Chapter 56 · all sections · _Estimated reading time: 10 min_

Cheat sheets for choosing between competing error-handling approaches: the 18-pair decision
matrix, the abstraction cost table, the risk-tier policy table, and the decision-record
template.

## 1. The 18-pair decision matrix (56.1–56.18)

| # | Pair | Recommended default | Use the other side when | Tie-breaker |
| - | ---- | ------------------- | ----------------------- | ----------- |
| 56.1 | Exceptions vs results | Both, by layer | The caller can enumerate the failures | Can the caller branch exhaustively? |
| 56.2 | Centralized vs local | Central policy, local effect | The fallback differs per surface | Who owns the fallback? |
| 56.3 | Global vs domain classes | Global base + domain class | Error needs domain vocabulary | Does it need domain nouns? |
| 56.4 | Fail-fast vs degradation | By risk tier | The reduced answer is still true | Is a degraded answer useful *and true*? |
| 56.5 | Retry vs immediate failure | Retry transient + idempotent | The failure is permanent | Will attempt 2 differ from attempt 1? |
| 56.6 | Retry vs compensation | Depends on the effect | The effect already happened | Has the side effect occurred? |
| 56.7 | Throwing vs returning | Return in the domain | Failure is part of the contract | Is failure part of the API? |
| 56.8 | Wrapping vs preserving | Preserve, then add context | Adding domain meaning only | Can the original be reconstructed? |
| 56.9 | Generic vs specific | Specific, then collapse | Callers treat all instances the same | Do 3+ call sites branch on it? |
| 56.10 | Inheritance vs composition | Composition | One base for uniform catching | Will the hierarchy grow branches? |
| 56.11 | Universal vs bounded | Bounded per domain | < ~20 error classes total | Can each domain name its errors alone? |
| 56.12 | Shared vs feature-owned | Feature-owned | 3+ consumers, product-neutral | Is the concept product-neutral? |
| 56.13 | Strict vs permissive | Strict at untrusted boundaries | Vendor payload drift | Who owns the data? |
| 56.14 | Aggregation vs first-error | Aggregate independent failures | Ordered, dependent steps | Must the caller know all failures? |
| 56.15 | Sync vs deferred | Sync when the user waits | Long or background work | Is the caller blocked on the outcome? |
| 56.16 | Local recovery vs termination | Recover locally | Corruption, OOM, invariant | Is continued execution safe? |
| 56.17 | Abstraction vs indirection | Abstraction at 3+ consumers | One private helper | Does the layer remove a decision? |
| 56.18 | Policies by business risk | Tier by operation | Uniform risk codebase | What breaks if we are wrong? |

## 2. Risk-tier policy table (56.18)

| Tier | Meaning | Retry | Degrade | Compensate | Terminate | Alert |
| ---- | ------- | ----- | ------- | ---------- | --------- | ----- |
| **T0** | Cosmetic | 0 (cache instead) | Yes, marked | n/a | No | None |
| **T1** | Convenience | ≤ 2, idempotent | Yes, marked | Rarely | No | Dashboard |
| **T2** | Workflow | ≤ 3, idempotent | Yes, if still true | Yes, reverse order | No | Notify |
| **T3** | Financial | ≤ 3, **idempotency key required** | **No** | **Mandatory** | No | **Page** |
| **T4** | Integrity / security | **0** | **No** | **No** | **Yes** | **Page + incident** |

**Tier assignment questions**

1. Does a wrong outcome affect money, entitlement, contract, or stored data? → tier ≥ T2.
2. Can the effect be undone within 24 hours? → tier ≤ T3, else T4.
3. Would the user see a *wrong number* rather than a missing feature? → tier ≥ T3.
4. Does recovery need human judgement to be correct? → tier = T4.

## 3. Abstraction cost model (56.17, 56.12)

**Gate before arithmetic — all four must be true:**

1. The layer removes at least one decision from each caller.
2. There are ≥ 3 real consumers (production imports).
3. The concept is product-neutral (no product codes, no vendor types).
4. A new engineer can use it in ≤ 20 minutes without reading the source.

**Break-even table**

| Term | Formula | Example (9 call sites, 5 decisions each) |
| ---- | ------- | ---------------------------------------- |
| S1 duplication saved | `N × D` | 9 × 5 = 45 |
| S2 drift avoided | `N × P` | 9 × 0.25 ≈ 2.3 incidents/yr |
| S3 change amplification | `(N − 1) × C_change` | 8 × 0.5 h = 4 h/change |
| C1 setup + migration | one-time hours | 16 h + 6 h/release |
| C2 indirection | `N × A` per review cycle | 9 × 8 min ≈ 1.2 h/cycle |
| C3 cognitive + ownership | `readers × learn_time` | 12 × 25 min = 5 h, recurring |

Decision rule: **build only if savings ≥ 2 × costs**, because recurring costs compound and
one-off savings do not.

## 4. Translation preservation contract (56.8)

| Must survive | Example |
| ------------- | ------- |
| Original error object | `cause` |
| Vendor error code | `card_declined` |
| Vendor request ID | `req_9f2c…` |
| Retryability | explicit boolean |
| Operation / step | `charge` |
| Correlation ID | `req-7c11…` |

**Never** recover structure from `err.message`; never drop the `cause`.

## 5. Layer contract (what each layer may and may not know)

| Layer | May know | Must not know |
| ----- | -------- | ------------- |
| Transport | HTTP status, headers, RFC 9457 shape | Vendor error types; business rules |
| Application / domain | Business rules, tiers, compensations | HTTP status codes; SQLSTATE |
| Adapter | Vendor codes, timeouts, breakers | User-facing wording; business outcomes |
| Shared kernel | Primitives, classification, redaction | Product codes; vendor types |

## 6. Decision-record template (56.1–56.18)

```text
# ADR-NNN — <scope> error-handling approach

Status: proposed | accepted | superseded
Date: YYYY-MM-DD · Owners: @team

Context
  What is broken today, with a number (error rate, tickets, incidents).

Decisions
  1. <one line>          (56.x)
  2. <one line>          (56.x)

Consequences
  + <measurable improvement>
  − <cost accepted>

Revisit when
  - <trigger, e.g. "the union exceeds 12 variants">
```

## 7. Quick reference — numbers used in this chapter

| Item | Value |
| ---- | ----- |
| Union variants per domain result | 3–7 (split above 7, hard-split above 12) |
| Max reported field-level errors | 20 |
| Max collected failures in a bulk report | 25 (hard cap 100) |
| Max aggregation in a parallel operation | 10 |
| Error hierarchy depth | ≤ 2 |
| Max error classes per feature | 8 |
| Shared-abstraction consumers | ≥ 3 |
| Shared-package size | ≤ ~300 lines, ≤ 10 options |
| Error-path hops (call site → handler) | ≤ 3 |
| Retry attempts | T0:0, T1:2, T2:3, T3:3 (idempotent only), T4:0 |
| `Retry-After` emitted | ≥ 1 s, honored up to 60 s |
| Idempotency key TTL | 24 h |
| Compensation window | 24 h |
| `422` for semantic validation | yes; `400` for malformed syntax |

## 8. One-minute lookup

Given a new error path, answer in this order:

1. **What can fail here?** (taxonomy)
2. **What is the tier of the operation?** (56.18)
3. **Can the caller enumerate the failures?** (56.1, 56.7)
4. **Has the effect already happened?** (56.6)
5. **Who owns the fallback?** (56.2)
6. **What must survive to the handler?** (56.8)

If any answer is missing, the error path is not designed yet.

## Related

- [Chapter 56 README](../README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../57-error-handling-under-load-and-at-scale/README.md)
- [Checkout Decision Walkthrough](../03-practical-examples/01-checkout-decision-walkthrough.md)
- [Glossary](../../../GLOSSARY.md)
