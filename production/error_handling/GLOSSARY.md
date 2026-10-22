# Glossary — Production-Grade Error Handling

Shared vocabulary used across the entire resource. When a chapter introduces a new term, it
should be defined here too. Definitions are deliberately short; the linked chapter holds the
full explanation.

| Term | Definition | Deep dive |
| ---- | ---------- | --------- |
| **Error** | A condition in which the software's result departs from its specification. A signal. | Ch. 1 |
| **Fault** | The defect/root cause (a bug or misconfiguration) that can produce an error. | Ch. 1 |
| **Failure** | The externally observable deviation from required behavior — the error became visible. | Ch. 1 |
| **Exception** | A language mechanism for signaling and propagating an error out-of-band from the normal return path. | Ch. 1, 12 |
| **Error taxonomy** | A structured classification of errors along multiple axes (origin, severity, recoverability…). | Ch. 4 |
| **Error model** | The internal data structure every error is represented as inside the application. | Ch. 6 |
| **Error code** | A stable, machine-readable identifier for a specific error condition (e.g. `PAYMENT_CARD_DECLINED`). | Ch. 8 |
| **Error registry** | A single source of truth listing every error code, its category, HTTP mapping, and retry policy. | Ch. 8 |
| **Error boundary** | A deliberate architectural line where errors are caught, translated, or contained rather than propagated. | Ch. 15 |
| **Error translation** | Converting an error from one representation (e.g. a driver exception) into another (e.g. a domain error) without losing the cause. | Ch. 16 |
| **Error normalization** | Reducing many vendor/format-specific errors into a consistent internal shape. | Ch. 16 |
| **Error envelope** | The outer JSON/document wrapper of an API error response (see RFC 9457 Problem Details). | Ch. 20 |
| **Error lifecycle** | The ordered stages an error passes through: originate → detect → classify → enrich → propagate → translate → recover/terminate. | Ch. 11 |
| **Fail-fast** | Abort the current operation immediately on an error rather than continuing with invalid state. | Ch. 2 |
| **Fail-safe** | Keep the system in a safe state when something goes wrong (often by denying/blocking) even at the cost of availability. | Ch. 2 |
| **Fail-closed / fail-open** | A security/availability choice: on failure, deny access (closed) or allow (open). | Ch. 30 |
| **Graceful degradation** | Continue providing reduced functionality when a non-critical dependency fails. | Ch. 30 |
| **Fallback** | A substitute value/behavior used when the primary path fails. | Ch. 30 |
| **Transient error** | A failure likely to succeed on retry (timeout, deadlock, 503). | Ch. 1, 27 |
| **Permanent error** | A failure that will not succeed on retry (validation, 404, auth). | Ch. 1, 27 |
| **Retry** | Re-executing a failed operation, ideally only if it is transient and idempotent. | Ch. 27 |
| **Backoff** | Increasing delay between retries (exponential, with jitter). | Ch. 27 |
| **Retry budget** | A cap on retries as a fraction of total requests, to prevent retry storms. | Ch. 27 |
| **Idempotency** | The property that performing an operation N times has the same effect as once. | Ch. 28 |
| **Idempotency key** | A client-supplied unique token letting the server detect and collapse duplicate requests. | Ch. 28 |
| **Circuit breaker** | A state machine (closed/open/half-open) that stops calling a failing dependency to let it recover. | Ch. 29 |
| **Bulkhead** | Isolating resources (pools, workers) per dependency/tenant so one failure cannot exhaust all. | Ch. 29 |
| **Timeout / deadline** | The maximum time an operation may take before it is aborted. | Ch. 29 |
| **Deadline propagation** | Passing the remaining time budget to downstream calls. | Ch. 29 |
| **Partial failure** | Some steps/items of an operation succeeded while others failed. | Ch. 39 |
| **Saga** | A sequence of local transactions with compensating actions instead of a distributed transaction. | Ch. 39 |
| **Compensation** | An action that logically undoes a previously completed step (e.g. refund, release reservation). | Ch. 39 |
| **Dead-letter queue (DLQ)** | A destination for messages/jobs that exhausted retries, kept for inspection/replay. | Ch. 32 |
| **Poison message** | A message that always fails processing and would block a queue forever without a DLQ. | Ch. 32 |
| **At-least-once / at-most-once / exactly-once** | Delivery guarantees. Exactly-once is achieved via at-least-once + idempotency. | Ch. 33 |
| **Correlation ID** | An identifier shared across all logs/errors for one request or workflow. | Ch. 6 |
| **Problem Details** | The RFC 9457 JSON shape for HTTP API errors (`type`, `title`, `status`, `detail`, `instance`). | Ch. 20 |
| **Result type** | A return value that encodes success or failure explicitly (e.g. `Result<T, E>`), instead of throwing. | Ch. 7 |
| **Error boundary (UI)** | A framework mechanism (e.g. React error boundary) that contains render errors to a subtree. | Ch. 37 |
| **Failover** | Switching to a standby resource (replica, region) after a failure. | Ch. 22 |
| **Optimistic concurrency** | Detecting conflicting writes via a version number/timestamp and rejecting stale writes. | Ch. 40 |
| **Fencing token** | A monotonically increasing token that invalidates a stale lock holder's writes. | Ch. 40 |
| **Compensating transaction** | Synonym for compensation; a business-level undo. | Ch. 39 |
| **Fail-operational** | The system continues operating (possibly degraded) despite component failures. | Ch. 30 |
| **Error budget** | (SRE) The allowed unreliability; used to decide how aggressively to fail vs degrade. | Ch. 3, 61 |

> **Note on terminology.** "Fault" (cause), "error" (state), and "failure" (observable effect) are
> often used interchangeably in casual speech. This book distinguishes them precisely in
> Chapter 1 because the distinction drives where you fix things: prevent faults, detect errors,
> contain failures.
