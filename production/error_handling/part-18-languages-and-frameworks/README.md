# Part XVIII — Error Handling Across Languages and Frameworks

> **Chapters 47–48.** Every principle in this book eventually lands in *some* language and *some*
> framework — and both change what is easy, what is forced, and what is silently forgotten. This
> part maps the error-handling concepts you already know onto ten mainstream languages and their
> web/queue frameworks, so you can carry one architecture across a polyglot codebase without
> letting any runtime's defaults quietly erode it.

## Learning objectives

By the end of Part XVIII you will be able to:

1. Compare the **error semantics of ten languages** — JS/TS, Node.js, Python, Java, Go, Rust,
   C#/.NET, PHP, Kotlin, Swift — and pick the idiom each one rewards (exceptions, explicit
   returns, or a hybrid of both).
2. Use each language's **native chaining and wrapping** APIs (`raise … from`, `%w` + `errors.Is`,
   `Error.cause`, `thiserror`/`anyhow`, `ExceptionDispatchInfo`, `Throwable` previous) without
   losing the original cause.
3. Choose the **type-safety level** your language gives you — exhaustive `match`, checked
   exceptions, `#[must_use]`, `errcheck` — and compensate where the compiler stays silent.
4. Handle **async error constructs** idiomatically: promises and `AbortSignal`, `asyncio` tasks,
   goroutines and `context`, coroutines and `CoroutineExceptionHandler`, `CompletableFuture`.
5. **Integrate with frameworks** — middleware, exception filters, ORM mappers, validation
   libraries, queue workers, startup/shutdown hooks — while keeping the error policy
   framework-independent and translating at the boundary.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 47 | [Language-Level Error Semantics](./47-language-level-error-semantics/README.md) | Exceptions vs returns; per-language idioms; async constructs; pitfalls; chaining/wrapping; type safety; translating to one architecture |
| 48 | [Framework and Runtime Integration](./48-framework-and-runtime-integration/README.md) | Framework hierarchies and handlers; HTTP middleware and request lifecycle; DI, ORM, and validation mapping; queue semantics; startup/shutdown; reusable adapters |

## How the chapters fit together

```text
                 one error-handling architecture (Parts I–XVII)
                              │
              ┌───────────────┴────────────────┐
              ▼                                ▼
   Chapter 47: the language layer     Chapter 48: the framework layer
   ┌───────────────────────────┐      ┌──────────────────────────────┐
   │ throw vs return Result    │      │ middleware / filters         │
   │ native wrapping APIs      │ ───▶ │ ORM + validation translation │
   │ type-safety guarantees    │      │ queue + lifecycle hooks      │
   │ async constructs          │      │ adapters over a stable core │
   └───────────────────────────┘      └──────────────────────────────┘
              │                                │
              └───────────────┬────────────────┘
                              ▼
        the same taxonomy, codes, and contracts in every service
```

- **Chapter 47** is the substrate: language semantics decide what a caller *must* notice, what
  can be silently ignored, and how causes survive propagation. Skip it and your "standard"
  becomes a lowest-common-denominator wrapper.
- **Chapter 48** is the integration layer: frameworks own the request boundary, the object graph,
  the persistence layer, and the worker loop. You either adopt their hooks deliberately or they
  adopt you by accident.

## The recurring cast in this part

| Cast member | Role in Part XVIII |
| ----------- | ------------------ |
| **Acme SaaS** | Polyglot platform (Go ingest, TS API, Java billing, Python AgentRun) sharing one error-code registry |
| **Checkout** | Payment workflow: card declines, idempotency conflicts, Stripe timeouts across languages |
| **ExportJob** | Background export: Go worker `if err != nil` paths, Rust `Result` pipelines, Celery/Sidekiq/BullMQ semantics |
| **WebhookIngest** | Inbound Stripe webhooks: signature failure translated through Express/FastAPI/Spring middleware |
| **AgentRun** | LLM tool-calling agent: parallel async failures in promises, asyncio, coroutines, goroutines |

## Key takeaways

- **Languages force different amounts of honesty.** Rust makes you handle or explicitly discard
  every `Result`; Go makes you receive every `error` but not check it; Java's checked exceptions
  make the compiler argue with you; JS/Python/C#/PHP trust you completely. Design your standard
  for the language you are in, then translate to a shared taxonomy.
- **Chaining is a native API, not a convention.** Every language has exactly one blessed way to
  preserve a cause (`raise … from`, `%w`, `Error.cause`, inner exceptions, `#[source]`). Use it;
  a re-thrown bare error is a lost root cause.
- **Async is where idioms diverge hardest.** A Go `errgroup`, a Python `TaskGroup`, a JS
  `Promise.allSettled`, and a Kotlin `supervisorScope` answer the same product question with
  different failure visibility — pick deliberately per operation.
- **Frameworks already made error decisions for you.** Express's 4-arg handler, Spring's
  resolver chain, FastAPI's 422, Sidekiq's 25 retries — preserve those defaults until you have
  a reason, and replace them at exactly one layer.
- **One architecture, many encodings.** Keep taxonomy, codes, classification, and contracts in a
  framework-free core; let each language and framework contribute a thin, replaceable adapter.

## Exercises

1. Take one domain error in your codebase (e.g. `PAYMENT_CARD_DECLINED`) and write how each of
   the ten languages in Chapter 47 would represent, chain, and surface it.
2. Pick one service and list every framework default that touches errors (handler, 4xx mapping,
   queue retries, startup checks). Mark each as *preserve* or *customize*, with a reason.
3. Choose one cross-language operation (e.g. `ExportJob`) and implement its failure contract in
   two languages with different semantics (e.g. Go and Rust); verify both preserve the cause.
4. Extract one reusable adapter from a framework-coupled service and prove the core policy has
   zero imports from the framework.

## Related

- [Part XVII — Error Handling in Architecture and Code Organization](../part-17-organization/README.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
- [Chapter 16 — Error Translation and Normalization](../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Glossary](../GLOSSARY.md)
