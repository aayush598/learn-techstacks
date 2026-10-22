# Part XVI — Specialized SaaS Error Scenarios

> **Chapters 42–44.** The previous parts teach universal mechanics — taxonomy, boundaries,
> retries, idempotency, async jobs. This part applies them to the three domains where SaaS
> products lose the most money and trust: **billing**, **file/media processing**, and **AI/LLM
> features**. Each domain has failure modes that generic guidance does not cover, and each
> punishes a different mistake: double charges, orphaned storage bills, runaway token spend.

## Learning objectives

By the end of Part XVI you will be able to:

1. Design **subscription state machines** and webhook appliers that tolerate duplicates,
   out-of-order delivery, and missed events without corrupting billing state.
2. Classify **payment provider errors** into retryable, action-required, and terminal buckets,
   and resolve **ambiguous payment outcomes** (timeout after the charge may have succeeded)
   without double-charging.
3. Enforce **quotas and entitlements** safely, including the fail-open/fail-closed decision when
   the entitlement store itself is down.
4. Build **upload and processing pipelines** that validate untrusted files, survive interrupted
   multipart uploads, and clean up the storage that failed jobs leave behind.
5. Handle **LLM provider failures** — rate limits, token/context overflow, invalid structured
   output, tool-call failures — behind a stable internal contract that survives swapping providers.
6. Prevent **duplicate side effects** from retried payments, retried agent steps, and replayed
   webhooks.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 42 | [Authentication, Billing, and Subscription Workflows](./42-auth-billing-and-subscription-workflows/README.md) | Account lifecycle, payments, refunds, subscription states, entitlements, invoices, financial retries |
| 43 | [File and Media Processing Errors](./43-file-and-media-processing-errors/README.md) | Upload validation, multipart/resume, transformation failures, malware scanning, temp URLs, batch processing |
| 44 | [AI, LLM, and Tool-Calling Application Errors](./44-ai-llm-and-tool-calling-application-errors/README.md) | Provider errors, rate/token limits, structured output, tool failures, agent topology, fallbacks, provider portability |

## How to study this part

- Read Chapter 42 even if you do not have a payment provider yet — subscription SaaS always
  gets one, and retrofitting idempotency onto live billing is the most expensive kind of rewrite.
- Chapter 43 is the most "infra" of the three; skim the concepts, then keep the reference tables
  (S3 multipart limits, presigned-URL rules) bookmarked.
- Chapter 44 assumes you have read Chapters 25–30 (third-party API errors, retries, circuit
  breakers); the AI-specific twist is *nondeterminism* and *side-effecting tools* on top of the
  usual provider problems.

## Key takeaways

- **Billing errors are money.** A retry policy that is fine for a read endpoint is a double
  charge on a payment endpoint. Financial operations need idempotency keys, an "unknown" state,
  and reconciliation — not just backoff.
- **The webhook is not the truth; the provider object is.** Local state is a projection.
  Duplicates, reordering, and missed events are normal operation, so every projection needs a
  reconciliation path back to the provider.
- **Untrusted files are attacker input.** Extension checks are not validation; incomplete
  multipart uploads are a real storage bill; cleanup is part of the feature, not an afterthought.
- **An LLM call is a third-party API call with a dice roll attached.** Classify provider vs
  application errors at the adapter, bound tokens/time/cost, validate structured output, and make
  every tool the agent calls idempotent.
- **Fallbacks must be honest.** A degraded invoice total, a truncated export, or a
  fallback-model summary presented as authoritative is worse than an explicit error.

## Related

- [Part XV — Advanced Distributed-System Failure Handling](../part-15-distributed-failures/README.md)
- [Part XVII — Error Handling in Architecture and Code Organization](../part-17-organization/README.md)
- [Glossary](../GLOSSARY.md)
