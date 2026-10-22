# Part V — Exception Handling Mechanics

> **Chapters 12–14.** Parts I–IV decide *what* an error is, how to model it, and where it belongs
> architecturally. This part is about the *mechanics* of moving that error through running code:
> how control flow unwinds, how you catch and recover, and how you release resources without
> leaking — in every case, including when things fail mid-flight.

## Learning objectives

By the end of Part V you will be able to:

1. Trace how an exception (or error value) travels through synchronous calls, asynchronous
   continuations, callbacks, event handlers, and concurrent work — and explain the exact point at
   which it is caught, wrapped, or lost.
2. Choose the **correct level to catch** and decide deliberately between **catch, wrap, rethrow,
   translate, or terminate**.
3. Write catch blocks that recover without corrupting state, without suppressing failures, and
   without recursion.
4. Guarantee cleanup with `try/finally`, `using` / try-with-resources, `defer`, and context
   managers — preserving the **primary error** when cleanup itself fails.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 12 | [Exception Propagation and Control Flow](./12-exception-propagation-and-control-flow/README.md) | How errors move through the call stack, async boundaries, and concurrent work |
| 13 | [Catch Blocks and Recovery Logic](./13-catch-blocks-and-recovery-logic/README.md) | When and how to catch; recovery that is safe and non-recursive |
| 14 | [Resource Cleanup and Failure-Safe Execution](./14-resource-cleanup-and-failure-safe-execution/README.md) | Guaranteed release of connections, files, locks, and temp resources |

## The three questions this part answers

1. **Where does the error go if I do nothing?** (propagation)
2. **Should I intercept it, and if so, what is the safe outcome?** (catch and recovery)
3. **What must be released no matter what happens?** (cleanup)

## How to study this part

- Read Chapter 12 first and draw the call/continuation path for one real request in your system.
- For Chapter 13, take every `catch` block in one module and label it: recover / translate /
  rethrow / bug.
- For Chapter 14, list every resource you acquire (connection, file, lock, temp file) and confirm
  it has exactly one owner that releases it on every path.

## Key takeaways

- **Propagation is the default.** You only catch when the fallback is *meaningfully different*
  from letting the error continue. Every catch is an architectural decision (Ch. 13).
- **Async boundaries are where causes go to die.** A promise rejection, a dropped callback, or a
  detached goroutine loses the stack unless you explicitly carry the cause forward (Ch. 12).
- **Never convert a failure into a success.** If you cannot complete the operation, the caller
  must be able to tell (Ch. 13).
- **Cleanup must be structural, not habitual.** `finally` / `using` / `defer` run on the failure
  path too; manual release at the end of the happy path leaks (Ch. 14).
- **Preserve the primary error.** When cleanup throws, the original failure is the one the caller
  cares about; attach the cleanup failure as suppressed/secondary (Ch. 14).

## Related

- **Prerequisite:** [Part IV — Error-Handling Architecture and System Boundaries](../part-04-architecture/README.md)
- **Next:** [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md)
- **Deep-dive support:** [Part IX — Database, Persistence, and Transaction Errors](../part-09-database-and-transactions/README.md), [Part XII — Asynchronous Processing and Background Jobs](../part-12-async-and-background-jobs/README.md)
- [Glossary](../GLOSSARY.md)
