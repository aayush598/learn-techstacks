## 35. Trigger.dev Advanced (921–930)

921. How do durable executions work?
   Durable executions persist workflow state as checkpoints after each step. If a worker crashes, the workflow resumes from the last checkpoint rather than restarting, ensuring at-least-once execution guarantees.

922. Explain workflow retries with backoff.
   Trigger.dev retries failed steps with configurable exponential backoff and jitter. Retries respect `maxAttempts`, backoff multipliers, and can be customized per step with `{ retry: { maxAttempts: 3 } }`.

923. What are saga compensations?
   Saga compensations define rollback steps for each workflow action. If a later step fails, Trigger.dev executes compensating actions to undo previous side effects, maintaining data consistency.

924. Explain event sourcing basics.
   Event sourcing stores state changes as an append-only event log. Trigger.dev workflows can emit and react to events, enabling audit trails, time travel, and rebuilding state from event history.

925. How do distributed workflows coordinate?
   Distributed workflows coordinate via message passing between Trigger.dev workers. Steps can fan-out to parallel workers and fan-in with joins, using the orchestration engine to manage concurrency.

926. Explain workflow idempotency patterns.
   Idempotency uses unique workflow IDs or deduplication keys. If a workflow is triggered multiple times with the same ID, it only executes once, preventing duplicate processing.

927. What are workflow deadlocks?
   Workflow deadlocks occur when parallel branches wait for each other indefinitely, or when a step crashes without advancing. Trigger.dev detects stalled workflows with timeouts and notifies on deadlock.

928. Explain queue throughput optimization.
   Optimize throughput by adjusting concurrency limits, batch sizes, worker count, and polling intervals. Trigger.dev's queue processes jobs in parallel within configurable rate limits.

929. How do delayed retries improve reliability?
   Delayed retries space out repeated attempts, giving transient failures (e.g., DB connection timeout) time to resolve. Exponential backoff prevents thundering herd on downstream services.

930. Explain workflow observability dashboards.
   Dashboards show workflow status (running, failed, completed), execution timelines, step-level logs, retry counts, latency histograms, and error breakdowns. Trigger.dev provides a hosted dashboard and API for custom monitoring.
