## 16. Trigger.dev (421–430)

421. What is Trigger.dev?
     Trigger.dev is an open-source background job and workflow platform for TypeScript developers. It allows you to write long-running, event-driven workflows as TypeScript functions with built-in retries, scheduling, observability, and error handling.

422. Explain background jobs.
     Background jobs are tasks that run asynchronously outside the request-response cycle. They handle operations like sending emails, processing uploads, generating reports, and webhook handling — keeping API responses fast and users unblocked.

423. What are event-driven workflows?
     Event-driven workflows react to events (webhooks, cron schedules, queue messages) and execute a sequence of steps. Each step can wait for conditions, call external APIs, or trigger other events, enabling complex business logic without polling.

424. Explain retries in Trigger.dev.
     Retries in Trigger.dev are configurable per job or step, with exponential backoff. Failed steps are automatically retried with controlled delays, and the system provides visibility into retry attempts, failures, and recovery.

425. How does scheduling work?
     Scheduling uses cron expressions or interval-based triggers to run jobs at specific times. Trigger.dev's crontab-like scheduling supports timezone handling and one-time scheduled runs for delayed job execution.

426. Explain long-running tasks.
     Long-running tasks are jobs that execute over minutes or hours, like data processing pipelines or multi-step API integrations. Trigger.dev handles them by persisting state between steps, allowing resumption after server restarts.

427. What are idempotent jobs?
     Idempotent jobs produce the same result regardless of how many times they're executed. They use unique IDs and `idempotencyKey` to prevent duplicate processing — if a job is triggered multiple times, it only runs once.

428. Explain observability in workflows.
     Workflow observability provides real-time visibility into job status, execution logs, failure causes, retry history, and performance metrics. Trigger.dev's dashboard shows workflow runs, step-level timing, and error details.

429. How does Trigger.dev integrate with Next.js?
     Trigger.dev integrates with Next.js via the `@trigger.dev/nextjs` package, enabling background jobs defined as API routes or server actions. Jobs run in the Trigger.dev cloud or self-hosted workers, keeping serverless functions fast.

430. Explain workflow orchestration.
     Workflow orchestration coordinates multiple steps, services, and conditions into a reliable execution flow. It handles step ordering, parallel execution, error recovery, timeouts, and state persistence — ensuring complex processes complete correctly.
