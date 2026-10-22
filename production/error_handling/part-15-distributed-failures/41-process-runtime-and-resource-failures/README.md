# Chapter 41 — Process, Runtime, and Resource Failures

> Part XV · _Estimated reading time: 75–100 min_
> **Prerequisite:** [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)

## One-sentence summary

Some failures are not about *your logic* but about *the process that runs it* — an uncaught
exception, an out-of-memory kill, an exhausted file-descriptor table, a pool with no connections —
and production-grade handling means knowing when the process can continue, when it must
**terminate cleanly**, and how to make **termination itself safe**.

## Why this chapter matters

A web request that throws a handled error is a 500 and a log line. A process that throws an
*uncaught* error is different: the runtime may print and exit, taking every in-flight request,
every open transaction, and every scheduled timer with it. A worker that hits `ENOMEM` or
`EMFILE` cannot necessarily recover in place — its invariants may be broken. Ignoring this class
produces the two worst outcomes: **crash loops that lose committed-looking work**, and **zombie
processes that keep "serving" with no file descriptors and no memory**. This chapter is about
catching what you can, terminating when you must, and shutting down in a way that the rest of the
system can reason about.

## Chapter map

The chapter has 18 sections grouped into ten files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-uncaught-and-unhandled-failures.md`](./01-concepts/01-uncaught-and-unhandled-failures.md) | 41.1, 41.2 | Last-resort handlers, why `uncaughtException` is a fatal signal, `unhandledRejection` |
| [`01-concepts/02-memory-stack-and-descriptor-exhaustion.md`](./01-concepts/02-memory-stack-and-descriptor-exhaustion.md) | 41.3–41.6 | OOM kills, `ENOMEM`, stack overflow, `EMFILE`/`ENFILE`, socket exhaustion |
| [`01-concepts/03-pool-queue-and-cpu-pressure.md`](./01-concepts/03-pool-queue-and-cpu-pressure.md) | 41.7–41.9 | Pool exhaustion, queue saturation, admission control, CPU/memory pressure |
| [`01-concepts/04-initialization-startup-and-shutdown.md`](./01-concepts/04-initialization-startup-and-shutdown.md) | 41.10–41.18 | Runtime init, module/config loading, startup, `SIGTERM` shutdown, termination, corruption |
| [`02-deep-dive/01-process-recovery-limits-and-termination.md`](./02-deep-dive/01-process-recovery-limits-and-termination.md) | 41.16–41.18 (mechanics) | Process invariants, restart safety, crash loops, when to terminate, corrupted state |
| [`02-deep-dive/02-graceful-shutdown-sequencing.md`](./02-deep-dive/02-graceful-shutdown-sequencing.md) | 41.14, 41.15 (mechanics) | The five shutdown phases, time budgets, escalation ladder, Node/Go/Python mechanics |
| [`03-practical-examples/01-node-uncaught-rejection-and-graceful-shutdown.md`](./03-practical-examples/01-node-uncaught-rejection-and-graceful-shutdown.md) | 41.1, 41.2, 41.14, 41.15 | A Node.js service: config validation, `uncaughtException`, `unhandledRejection`, phased `SIGTERM` drain |
| [`03-practical-examples/02-python-and-go-resource-limit-handling.md`](./03-practical-examples/02-python-and-go-resource-limit-handling.md) | 41.3, 41.5, 41.7, 41.16, 41.17 | `MemoryError`, `RecursionError`, `EMFILE`, `GOMEMLIMIT`, bounded pools, exit codes |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Process-failure rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Process-failure decision tables, signal/errno/exit-code maps, shutdown checklist |

## Learning objectives

By the end you can:

- Explain why an `uncaughtException` handler must **log and exit**, never resume serving.
- Distinguish errors the runtime can survive (`ENOMEM` on one allocation) from states it cannot
  (`EMFILE` on a hardened fd table, heap corruption).
- Read the pressure signals — RSS, open fds, pool waiters, queue depth — and act **before**
  exhaustion turns into an outage.
- Validate **config and dependencies at startup** so the process fails once at boot instead of
  per-request.
- Implement a **graceful shutdown** with drain, in-flight tracking, a hard deadline, and an
  idempotent exit.
- Decide, with a rule you can defend, **when termination is the correct recovery** and when it is
  the bug.

## Key takeaways

1. **`uncaughtException` is a post-mortem, not a recovery hook.** Node's own documentation says the
   process state is undefined; the correct handler logs, flushes, and exits non-zero.
2. **Resource exhaustion is a state, not a moment.** By the time `EMFILE` fires, some code path is
   already permanently broken for the rest of the process's life — restart, do not ration.
3. **Startup is the cheapest place to fail.** A bad config value or unreachable dependency should
   stop the process at boot, not produce 100 different per-request failures.
4. **Shutdown must be designed like an error path**: a deadline, in-flight tracking, cancellation,
   and an exit code that tells the orchestrator what happened.
5. **Terminate to recover; make termination safe.** Restart is a legitimate, cheap recovery — but
   only if in-flight work is idempotent, leased/fenced, and checkpoints exist.

## Exercises

1. Add `process.on("uncaughtException")` and `unhandledRejection` handlers that log, flush, and
   exit; verify with a deliberate throw in a timer that the process exits non-zero.
2. Run your service under a memory limit and watch RSS; identify the growth shape (leak vs
   sawtooth vs step) and the largest single allocation.
3. Kill your service with `SIGTERM` under load and measure: how long until it exits, how many
   requests were dropped, how many jobs were redelivered.
4. Inspect `ulimit -n` and your current open-fd count at steady state; compute headroom.
5. List the config values read at boot versus per-request; move the per-request ones that "cannot
   change" to boot-time validation.

## Related

- [Chapter 39 — Partial Failures and Multi-Step Operations](../39-partial-failures-and-multi-step-operations/README.md)
- [Chapter 40 — Consistency and Concurrency Failures](../40-consistency-and-concurrency-failures/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
- [Glossary](../../GLOSSARY.md)
