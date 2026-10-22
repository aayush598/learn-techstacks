# Chapter 49 — Error Contract Design and Versioning

> Part XIX · _Estimated reading time: 90–110 min_
> **Prerequisite:** [Chapter 8 — Error Codes and Error Registries](../part-03-error-models/08-error-codes-and-error-registries/README.md)

## One-sentence summary

An **error contract** is the set of promises a producer makes about the failures it emits; this
chapter defines where those contracts live, what stability each one carries, and exactly how to
change one without breaking a consumer.

## Why this chapter matters

Chapter 8 gave you a registry of codes. A registry is *vocabulary*, not *promise*. The moment
Acme SaaS ships a mobile app, a partner integration, and a public API, someone is branching on
those codes — and every change to them is a change to **their** code, not yours.

The failure mode is specific and expensive:

- A public code's **HTTP status changes** from `422` to `409` and a partner's retry logic
  silently starts retrying a permanent failure.
- A code is **renamed** in a refactor and an old dashboard reports "unknown error" for a week.
- A code is **repurposed** — same string, new meaning — and a client's `switch` now takes the
  wrong branch on a payment failure.
- An error's **message** is matched with `includes("timed out")` and stops matching the day
  someone improves the wording.

None of these are bugs in the error-handling code. They are **contract-management** bugs. This
chapter is the discipline that prevents them.

## Chapter map

The chapter has 16 sections grouped into eight files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-contract-surfaces-and-stability.md`](./01-concepts/01-contract-surfaces-and-stability.md) | 49.1–49.6 | Internal vs external, module/service/backend↔frontend/public surfaces, stability tiers |
| [`01-concepts/02-evolution-rules-and-compatibility.md`](./01-concepts/02-evolution-rules-and-compatibility.md) | 49.7–49.13 | Adding, deprecating, message and HTTP changes, backward/forward compatibility, unknown codes |
| [`01-concepts/03-ownership-documentation-and-message-independence.md`](./01-concepts/03-ownership-documentation-and-message-independence.md) | 49.14–49.16 | Contract ownership, documenting behaviour, why messages are never contract |
| [`02-deep-dive/01-deprecation-mechanics-and-windows.md`](./02-deep-dive/01-deprecation-mechanics-and-windows.md) | 49.8 | The deprecation state machine, window arithmetic, telemetry gates, sunset signalling |
| [`02-deep-dive/02-versioning-error-contracts.md`](./02-deep-dive/02-versioning-error-contracts.md) | 49.6, 49.11–49.12 | Independent contract versioning, semver mapping, version carriers and negotiation |
| [`02-deep-dive/03-durable-vs-ceremonial-rules.md`](./02-deep-dive/03-durable-vs-ceremonial-rules.md) | 49.6–49.7 | Which compatibility rules earn CI enforcement, which belong in review, which to delete |
| [`03-practical-examples/01-deprecation-workflow-introduce-dual-emit-sunset.md`](./03-practical-examples/01-deprecation-workflow-introduce-dual-emit-sunset.md) | 49.7–49.11 | A full introduce → dual-emit → measure → sunset → remove run |
| [`03-practical-examples/02-error-contract-spec-and-adr.md`](./03-practical-examples/02-error-contract-spec-and-adr.md) | 49.5–49.6, 49.14–49.15 | A public contract spec excerpt and the ADR that adopted it |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Versioning guide, change-classification tables, checklist, glossary |

## Learning objectives

By the end you can:

- Identify the five surfaces an error crosses and assign each a **stability tier**.
- Classify a proposed change as **additive** or **breaking** in under a minute, and pick the
  correct mechanism for it.
- Distinguish **backward compatibility** from **forward compatibility** and enforce both.
- Write a consumer that tolerates an **unknown code** without throwing.
- Run a deprecation to completion, gated on **consumption telemetry**.
- Version an error contract independently of the API version and the package version.
- Say, in one sentence, which parts of an error a consumer may rely on — and which it may not.

## Key takeaways

1. **The contract is the promise; the code is the vocabulary.** Codes without stability
   guarantees are just strings.
2. **Match stability to audience.** An internal helper function needs no contract; a public API
   needs a versioned one.
3. **Additive is safe; reductive is a migration.** Adding a code is free; renaming, repurposing,
   re-statusing, or removing one is not.
4. **Two compatibility directions, both required.** New consumers read old producers *and* old
   consumers survive new producers.
5. **Unknown is a normal state, not an error.** Consumers need a default branch from day one.
6. **Deprecate with evidence.** Zero consumption for 30 consecutive days, not a launch date.
7. **Messages are human-facing.** Machine logic branches on `code` and `type`.

## Exercises

1. Inventory every surface in your product that emits an error a *different team* consumes.
   Assign each a stability tier and an owner.
2. Take your five most-used public error codes. For each, write down what a consumer may rely
   on today (status, retryability, code stability) — and whether that is written down anywhere.
3. Audit one consumer for `message.includes(...)` or `message === ...` branching. Replace each
   hit with a code-based branch, or add a code if none exists.
4. Draft a one-paragraph deprecation policy: window length, telemetry gate, announcement
   channel, removal criteria.
5. Write the "stability guarantees" section of your public API error contract, then check it
   against the compatibility matrix in this chapter.

## Related

- [Chapter 50 — Error Handling as an Engineering Standard](../50-error-handling-as-an-engineering-standard/README.md)
- [Chapter 8 — Error Codes and Error Registries](../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 20 — Standardized API Error Responses](../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Chapter 38 — Full-Stack Error Contracts](../part-14-frontend-and-full-stack/38-full-stack-error-contracts/README.md)
