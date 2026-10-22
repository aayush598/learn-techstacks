# Chapter 47 — Language-Level Error Semantics

> Part XVIII · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 7 — Error Classes, Types, and Structured Results](../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)

## One-sentence summary

Every language encodes failure differently — **exceptions, explicit returns, or a hybrid** — and
each encoding decides what the compiler forces you to notice, how causes survive propagation, and
which bugs become runtime surprises; your architecture must be translated into each language's
native idiom rather than wrapped around it.

## Why this chapter matters

A team that ships Acme SaaS in Go, TypeScript, Java, Python, and Rust will otherwise end up with
five incompatible error cultures: a Go service that silently ignores an `error`, a Java service
that funnels business rules through checked exceptions, a TypeScript service whose promises reject
into the void, a Rust service that `unwrap()`s in production, and a Python service whose bare
`except:` turns cancellation into corruption. This chapter gives you the per-language semantics,
the native chaining APIs, the type-safety guarantees, and the translation pattern that let one
error taxonomy survive all five runtimes.

## Chapter map

The chapter has 16 sections grouped into ten files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-exceptions-vs-returns.md`](./01-concepts/01-exceptions-vs-returns.md) | 47.1 | The two families of error signaling; what each forces and hides; hybrids |
| [`01-concepts/02-language-comparison-at-a-glance.md`](./01-concepts/02-language-comparison-at-a-glance.md) | 47.2–47.11 | One comparison table plus a survey card for each of the ten languages |
| [`01-concepts/03-exception-first-languages.md`](./01-concepts/03-exception-first-languages.md) | 47.2–47.5, 47.8–47.9 | JS/TS, Node.js, Python, Java, C#/.NET, PHP idioms in depth |
| [`01-concepts/04-result-first-languages.md`](./01-concepts/04-result-first-languages.md) | 47.6–47.7, 47.10–47.11 | Go, Rust, Kotlin, Swift idioms in depth |
| [`01-concepts/05-async-constructs-and-pitfalls.md`](./01-concepts/05-async-constructs-and-pitfalls.md) | 47.12–47.13 | Async error constructs per language; the pitfalls each one is famous for |
| [`02-deep-dive/01-native-chaining-and-wrapping-capabilities.md`](./02-deep-dive/01-native-chaining-and-wrapping-capabilities.md) | 47.14 | Exact chaining APIs: `raise … from`, `%w`, `Error.cause`, `#[source]`, inner exceptions |
| [`02-deep-dive/02-type-safe-handling-and-common-architecture.md`](./02-deep-dive/02-type-safe-handling-and-common-architecture.md) | 47.15–47.16 | The compile-time honesty spectrum; Result patterns; mapping one taxonomy onto every language |
| [`03-practical-examples/01-same-error-across-languages.md`](./03-practical-examples/01-same-error-across-languages.md) | 47.2, 47.4–47.9, 47.14–47.16 (applied) | One provider timeout handled in Go, Rust, Python, TypeScript, Java, C# |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules per language family; the pitfall catalog (swallowed exceptions, bare `except:`, floating promises, Go typed-nil, Rust `unwrap`) |
| [`05-reference/README.md`](./05-reference/README.md) | all | Language matrix, chaining cheat sheet, lint gates, cancellation table, glossary |

## Learning objectives

By the end you can:

- Explain why **Go returns errors, Rust encodes them in types, and Java argued about checked
  exceptions for 30 years** — and what each choice costs you at the call site.
- Use each language's blessed chaining API so the root cause survives three layers of wrapping.
- State exactly which compile-time guarantees your language gives you for errors, and which
  linter or pattern compensates for the rest.
- Write the same `Checkout` failure in five languages so a polyglot team shares one vocabulary.
- Choose the right async construct per language for aggregation, cancellation, and terminal
  handling of concurrent failures.

## Key takeaways

1. **Exceptions are out-of-band; results are in-band.** Exceptions hide the failure from the
   signature; results put it in the signature. Neither is universally better — but mixing both
   freely in one codebase is universally worse.
2. **Chaining has exactly one native API per language.** Use `raise … from` (Python), `%w` +
   `errors.Is/As` (Go), `Error.cause` (ES2022), `#[source]`/`anyhow` (Rust), inner exceptions
   (C#/PHP), cause constructors (`addSuppressed` in Java). Re-`throw new Error(message)` is a
   root-cause deletion.
3. **The compiler's honesty varies by an order of magnitude.** Rust forces handling of every
   `Result`; Go forces receipt but not checking of every `error`; Java forces checked exceptions
   but not runtime ones; JS/TS, Python, C#, PHP, and Kotlin force nothing. Compensate with
   linting (`errcheck`) and types (discriminated unions, sealed classes).
4. **Async is the idiom gap.** The same product question — "fail fast or collect all?" — is
   `Promise.all` vs `allSettled` in JS, `gather(return_exceptions=True)` vs `TaskGroup` in
   Python, `errgroup` in Go, `supervisorScope` vs `coroutineScope` in Kotlin.
5. **One architecture, ten encodings.** Taxonomy, codes, retryability, and the error envelope
   stay identical; only the encoding changes. Generate per-language types from one registry
   (see [47.16](./02-deep-dive/02-type-safe-handling-and-common-architecture.md)).

## Exercises

1. Pick the last three errors your service produced. For each, write the representation,
   chaining call, and boundary translation in Go *and* Rust (or your two primary languages).
2. Find one place in your codebase where an error is re-thrown without its cause. Fix it using
   the native chaining API and show the improved log line.
3. List every `unwrap()`/`try!`/`async void`/bare `except:` in one service. Classify each as
   genuinely unrecoverable or a latent production crash; fix the second class.
4. Take your error-code registry and sketch the generated types for two languages with
   different semantics (e.g. TypeScript union vs Rust enum).

## Related

- [Chapter 48 — Framework and Runtime Integration](../48-framework-and-runtime-integration/README.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [Chapter 31 — Asynchronous Error Handling](../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
- [Glossary](../../GLOSSARY.md)
