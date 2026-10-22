# Chapter 7 — Error Classes, Types, and Structured Results

> Part III · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Chapter 6 — Designing the Application's Error Model](../06-designing-the-applications-error-model/README.md)

## One-sentence summary

Once you have an error **shape**, you must decide how it is **expressed in code** — native
exceptions, custom classes, tagged unions, or `Result` values — and this chapter chooses a
consistent, type-safe convention so failure paths are explicit rather than accidental.

## Why this chapter matters

Chapter 6 defines the data. This chapter defines the **control flow and type system** around it.
The wrong choice is expensive: a deep class hierarchy becomes unmaintainable; a `Result` used only
in some modules forces two dialects; untyped errors defeat exhaustiveness so a handler forgets a
case and silently mishandles it. A consistent approach means the compiler helps you handle every
failure — and catches the ones you forgot.

## Chapter map

The chapter has 20 sections. They are grouped into nine files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-native-vs-custom-exceptions.md`](./01-concepts/01-native-vs-custom-exceptions.md) | 7.1–7.6 | When to use native errors vs custom classes; domain/infra/app/framework layers |
| [`01-concepts/02-typed-vs-untyped-and-unions.md`](./01-concepts/02-typed-vs-untyped-and-unions.md) | 7.7, 7.10 | Typed vs untyped errors; union types for known failures |
| [`01-concepts/03-result-types-and-adts.md`](./01-concepts/03-result-types-and-adts.md) | 7.8–7.9 | Algebraic data types and success/failure `Result` |
| [`01-concepts/04-exception-vs-result-control-flow.md`](./01-concepts/04-exception-vs-result-control-flow.md) | 7.11–7.13 | Exception vs result control flow; choosing; hybrid approaches |
| [`01-concepts/05-hierarchies-composition-and-naming.md`](./01-concepts/05-hierarchies-composition-and-naming.md) | 7.14–7.17 | Inheritance vs composition; shallow hierarchies; catch-alls; names |
| [`02-deep-dive/01-exhaustiveness-and-compiler-assistance.md`](./02-deep-dive/01-exhaustiveness-and-compiler-assistance.md) | 7.18 | Discriminated unions, `never`, and making the compiler check |
| [`02-deep-dive/02-type-safety-across-async-boundaries.md`](./02-deep-dive/02-type-safety-across-async-boundaries.md) | 7.19–7.20 | Async/`Promise`, serialization typing, reusable error primitives |
| [`03-practical-examples/01-result-type-and-union-errors.md`](./03-practical-examples/01-result-type-and-union-errors.md) | 7.8–7.13 | A runnable `Result<T, E>` implementation with unions |
| [`03-practical-examples/02-custom-error-class-design.md`](./03-practical-examples/02-custom-error-class-design.md) | 7.1–7.6, 7.14–7.17 | A small, flat custom class set in practice |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Cheat sheet, decision tables, glossary |

## Learning objectives

By the end you can:

- Decide per layer whether an error is a thrown class, a union member, or a `Result`.
- Build a `Result<T, E>` and use typed unions to make known failures exhaustive.
- Avoid deep hierarchies, catch-all types, and ambiguous names.
- Get compiler help across `async`/`await` boundaries and serialization.

## Key takeaways

1. **One convention per boundary.** Pick exceptions or results and state where each is allowed.
2. **Types are the exhaustiveness engine.** Discriminated unions + `never` make missed cases a
   compile error.
3. **Flat, composable error types beat deep hierarchies.** Use small primitives, not a tree.
4. **Async does not change the contract** — but it does change where errors can escape.

## Exercises

1. List every error class in your codebase. How deep is the hierarchy? Could it be flat?
2. Convert one `throw`-based function to `Result<T, E>` and note what becomes explicit.
3. Add an exhaustive `switch` over your error categories with a `never` guard. What breaks?

## Related

- [Chapter 6 — Designing the Application's Error Model](../06-designing-the-applications-error-model/README.md)
- [Chapter 8 — Error Codes and Error Registries](../08-error-codes-and-error-registries/README.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
