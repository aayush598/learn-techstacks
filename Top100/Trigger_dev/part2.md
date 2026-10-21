# Trigger.dev Interview Questions and Answers - Part 2

## Q1: What are the key architectural differences between Trigger.dev v2 and v3?
**A:** Trigger.dev v2 used a poll-based worker model where workers polled the API server for jobs. v3 uses a push-based model with a persistent WebSocket connection between workers and the platform, reducing latency from seconds to milliseconds. v3 also introduces: (1) `io.runTask` for granular task tracking, (2) improved TypeScript inference, (3) local development with `trigger.dev dev`, (4) built-in idempotency, (5) Zod-based payload validation.

## Q2: How do you implement a webhook trigger pattern that handles Stripe webhooks with proper signature verification?
**A:** Define a webhook job with `webhookTrigger({ endpoint: '/stripe-webhook' })`. Inside the job, verify the Stripe signature using `stripe.webhooks.constructEvent(payload, signature, secret)`. If verification fails, return 400. Use `io.sendResponse()` to acknowledge receipt immediately, then process the event asynchronously. The webhook trigger exposes an endpoint that Stripe can call, and Trigger.dev handles the HTTP lifecycle.

## Q3: How does Trigger.dev handle idempotency for retried job executions and how do you ensure exactly-once processing?
**A:** Each event can include an `idempotencyKey`. Trigger.dev deduplicates events with the same key within a configurable time window (default 24h). For retries within a job, use idempotent operations in `io.runTask`: check if the task already completed successfully (by external ID) before re-executing. Combine with database-level unique constraints on idempotency keys for defense in depth.

## Q4: How do you implement a complex event-driven workflow where Job A emits multiple events that trigger different downstream jobs?
**A:** Use `io.sendEvent()` within Job A to emit multiple events. Each event has a distinct name and payload. Different jobs subscribe to different event names. Example: `io.sendEvent({ name: 'order.placed', payload: { orderId } })` triggers OrderProcessing job, `io.sendEvent({ name: 'notification.send', payload: { userId, message } })` triggers Notification job. This decouples jobs while enabling complex workflows.

## Q5: How do you integrate Trigger.dev with Next.js App Router for server actions that queue background jobs?
**A:** Create a Trigger.dev client in a shared file. In server actions, call `client.sendEvent()` to trigger jobs. For route handlers, use the same pattern. Ensure the Trigger.dev client is initialized with the correct API key for the environment. Example: in `app/actions/order.ts`, import the client and call `await client.sendEvent({ name: 'order.process', payload: formData })` after validation.

## Q6: How do you use Trigger.dev with Express.js to handle long-running API requests as background jobs?
**A:** In the Express route handler, validate the request and call `client.sendEvent()` to trigger a job. Return immediately with `202 Accepted`. The job processes the request asynchronously. For status updates, the job can update a database record that the client polls via GET endpoint. Use the job's run ID as a reference for status tracking.

## Q7: How do you build a custom integration for Trigger.dev (e.g., a custom API wrapper)?
**A:** Create a class that wraps the external API with typed methods. Each method calls `io.runTask()` internally so API calls appear as tracked tasks in the dashboard. Example: `class MyAPI { constructor(private io: IO) {} async getData(params) { return this.io.runTask('get-data', async () => { /* API call */ }, { retry: { maxAttempts: 3 } }); } }`. Register the integration with the Trigger.dev client.

## Q8: How do you implement priority queues in Trigger.dev to ensure critical jobs skip ahead of batch jobs?
**A:** Use the `priority` option in job definition: `defineJob({ ..., priority: { type: 'job-priority', value: 10 } })`. Higher values = higher priority. Default is 0. Critical jobs (e.g., payment processing) get high priority (10), batch jobs (e.g., report generation) get low priority (-10). The queue dequeues higher priority jobs first, preempting lower priority ones.

## Q9: How do you implement concurrency limits per customer to prevent one customer from consuming all workers?
**A:** Use `concurrencyLimit` with a dynamic key based on customer ID: `concurrencyLimit: { max: 5, key: payload.customerId }`. This limits each customer to 5 concurrent runs. Other customers' jobs continue unaffected. Combine with global concurrency limits to cap total parallel execution. This is essential for multi-tenant SaaS applications.

## Q10: How do you handle rate limiting when a Trigger.dev job calls an external API that has per-second limits?
**A:** Use Trigger.dev's `rateLimit` on the job: `rateLimit: { limit: 10, period: '1s' }`. If the external API has per-endpoint limits, use `io.runTask` with retry handling for 429 responses. In the retry handler, parse the `Retry-After` header and wait accordingly. For fine-grained control, implement a token bucket within the job using `io.wait` for delays.

## Q11: What is the error handling hierarchy in Trigger.dev (task level vs. job level vs. integration level)?
**A:** Three levels: (1) Task level: `io.runTask` catches errors, applies task retry policy, and on exhaustion marks the task as FAILED. (2) Job level: if any task fails and no retry remains, the entire run is marked FAILED. (3) Integration level: API wrapper methods can have their own retry logic within a task. This layered approach allows granular error recovery (retry just the failed API call) without restarting the entire job.

## Q12: How do you implement custom alerting for Trigger.dev job failures using webhooks?
**A:** In the Trigger.dev Dashboard, configure a "Failure Webhook" that POSTs to your endpoint on job failures. The payload includes: run ID, job ID, error message, task ID (if failed at task level). Process the webhook to: send Slack notification, create PagerDuty incident, log to error tracking (Sentry), or trigger remediation flows. For self-hosted, implement custom alerting via event listeners.

## Q13: How do you secure Trigger.dev webhook endpoints from replay attacks?
**A:** Implement: (1) Timestamp verification: check that the webhook request timestamp is within 5 minutes of current time. (2) Signature verification: use HMAC-SHA256 with the shared secret to sign the payload, verify on receipt. (3) Nonce tracking: reject requests with already-used nonces. (4) IP whitelisting: restrict incoming webhook IPs to the provider's published ranges. Trigger.dev webhook triggers support signature verification natively.

## Q14: How does payload validation work in Trigger.dev jobs using Zod schemas?
**A:** Define a Zod schema for the event payload: `const OrderSchema = z.object({ orderId: z.string().uuid(), amount: z.number().positive(), email: z.string().email() })`. Use `eventTrigger({ name: 'order.created', schema: OrderSchema })`. Trigger.dev validates incoming events against the schema. Invalid events are rejected with a descriptive error. Within the job, the payload is strongly typed from the inferred Zod type.

## Q15: How do you implement scheduled (cron) jobs in Trigger.dev with timezone-aware execution?
**A:** Use `cronTrigger({ cron: '0 9 * * 1-5', timezone: 'America/New_York' })`. Trigger.dev handles DST transitions automatically. For complex schedules (e.g., "last day of month"), use `scheduleTrigger` with advanced options. For one-time future schedules, trigger a job with `io.wait` for the desired delay, or use a scheduled event.

## Q16: How do you test Trigger.dev jobs locally with a real database?
**A:** Run `npx trigger.dev dev` which starts a local dev server. Define jobs with database connections (e.g., Prisma, Drizzle). Send test events: `npx trigger.dev run my-job --payload '{"key":"value"}'`. The job runs locally against your local database. Use test database instances to avoid corrupting production data. The CLI watches files and hot-reloads job definitions.

## Q17: How do you deploy Trigger.dev jobs to production with environment-specific configurations?
**A:** Use Trigger.dev's environment management: (1) development (local), (2) staging, (3) production. Each environment has separate API keys, environment variables, and job versions. Deploy with `npx trigger.dev deploy --env production`. Promote versions between environments via the dashboard. Use `.env.production` for production secrets and `.env.staging` for staging.

## Q18: Trigger.dev vs. BullMQ vs. Inngest vs. Temporal - what are the precise technical differences?
**A:** BullMQ: Redis-based, self-managed, no dashboard, requires Redis ops, lower level. Trigger.dev: managed + open-source, built-in dashboard, TypeScript SDK, retries, rate limiting, webhooks, cron. Inngest: managed only (not self-hostable), event-driven, step-based workflow, similar to Trigger.dev. Temporal: durable execution, long-running workflows (days/months), stateful, multi-language, complex setup, microservice-oriented. Choose BullMQ for simplicity, Trigger.dev/Inngest for managed workflows, Temporal for complex orchestration.

## Q19: How do you implement a job that processes items in batches with progress tracking?
**A:** Define a job that receives an array of items. Use `io.runTask` per batch of items. Track progress: `io.logger.info('Processing batch', { batch: currentBatch, total: totalBatches })`. Use `io.heartbeat()` periodically for long processing. On completion, the run tracks all task statuses. For very large batches, consider fanning out to sub-jobs per batch and using `io.waitForEvent` to collect results.

## Q20: How do you implement webhook verification for Shopify/Twitter/GitHub webhooks in Trigger.dev?
**A:** For Shopify: verify HMAC from the `X-Shopify-Hmac-Sha256` header. For GitHub: verify with the webhook secret using `crypto.timingSafeEqual`. For generic webhooks: use a shared secret in the webhook trigger definition. The webhook trigger exposes the raw request (headers, body, signature) to your validation logic before processing.

## Q21: How do you implement a Trigger.dev job that sends an email via SendGrid/Resend with retries?
**A:** Use the SendGrid or Resend integration: `await resend.emails.send({ from: '...', to: payload.email, subject: '...', html: '...' }, { id: 'send-email' })`. The integration wraps the API call in a task with automatic retry and logging. Configure retry: `retry: { maxAttempts: 3, minTimeoutInMs: 1000 }`. Handle specific failures (invalid email) by marking the task as failed without retry.

## Q22: How do you implement a Trigger.dev job that runs a long-running data sync with checkpoint/resume?
**A:** Process data in pages. After each page, save checkpoint (last processed ID) to a database. On job restart (after crash), read the checkpoint and resume from there. Use `io.wait()` if rate limits require delays between pages. For very long syncs, use `io.heartbeat()` to prevent timeout. Only the failed task is retried, not the entire sync.

## Q23: How do you implement dynamic task creation in Trigger.dev where the number of tasks is unknown at job start?
**A:** Use a loop with `io.runTask` inside. Each iteration creates a new tracked task: `for (const item of items) { await io.runTask(\`process-${item.id}\`, async () => { ... }); }`. Each task is independently tracked, retried, and logged in the dashboard. The job's task list grows dynamically based on the input data.

## Q24: How do you implement a Trigger.dev job that calls OpenAI and handles streaming responses?
**A:** Use the OpenAI integration with streaming: `const stream = await openai.chat.completions.create({ model: 'gpt-4', messages, stream: true }, { id: 'ai-stream' })`. Process the stream in a task, collecting chunks. For very long streams, use `io.heartbeat()` to keep the job alive. Store the final response and any intermediate results in the job state.

## Q25: How do you implement database transactions within a Trigger.dev job to ensure data consistency?
**A:** Use the database client's transaction support within task: `await io.runTask('update-order', async () => { await prisma.$transaction([prisma.order.update(...), prisma.inventory.update(...)]); })`. If the task fails, the transaction rolls back. For cross-service consistency, implement the Saga pattern: compensating actions in subsequent tasks or using a transaction outbox pattern.

## Q26: How do you implement Trigger.dev job chaining with data passing between jobs?
**A:** Job A completes and calls `io.sendEvent({ name: 'job.b.complete', payload: { resultId, data } })`. Job B subscribes to this event. Job B receives the payload in its run function. For complex data, pass a reference ID and have Job B fetch the full data from a database. This keeps event payloads small and avoids duplication.

## Q27: How do you implement a Trigger.dev job that depends on external API availability (circuit breaker)?
**A:** Wrap external API calls in a task with retry. If the API returns 503 repeatedly, mark the task as failed after retries. At the job level, implement a circuit breaker: check a Redis key for "api-down" before making the call. If tripped, either wait (`io.wait`) or fail early. The circuit resets after a timeout and allows test calls.

## Q28: How do you implement fine-grained logging in Trigger.dev jobs with structured data?
**A:** Use `io.logger.info('Processing order', { orderId: payload.orderId, amount: payload.amount, customerTier })`. Log at key milestones: start, each task, errors, completion. Use `io.logger.warn` for recoverable issues, `io.logger.error` for failures. Logs are searchable in the Dashboard with filters by run ID, task ID, level, and custom fields.

## Q29: How do you implement a Trigger.dev job that handles file uploads from S3/webhooks?
**A:** The trigger receives a file reference (URL or S3 key). In the job, download the file using a task: `await io.runTask('download-file', async () => { const file = await fetch(fileUrl); return file; })`. Process the file content. For large files, stream processing to avoid memory issues. Store results back to S3 and pass the output reference to downstream jobs.

## Q30: How do you implement a Trigger.dev job that sends Slack notifications with rich formatting?
**A:** Use the Slack integration: `await slack.chat.postMessage({ channel: payload.channelId, text: '*Order Processed*\nOrder #: ' + payload.orderId, blocks: [...] }, { id: 'slack-notify' })`. The integration handles API calls, retries, and logging. For complex messages, use Slack's Block Kit builder and include the blocks array in the payload.

## Q31: How do you implement conditional branching in Trigger.dev jobs (if-else logic)?
**A:** Use JavaScript control flow within the run function: `if (payload.amount > 1000) { await approveOrder(); } else { await processOrder(); }`. Each branch can have its own tasks. For complex branching, use event-driven approach: Job A emits different events based on conditions, and different downstream jobs subscribe to each event.

## Q32: How do you implement a Trigger.dev job that delays execution until a specific time?
**A:** Use `io.wait` with a computed delay: `const delayMs = new Date(payload.scheduledAt).getTime() - Date.now(); await io.wait('wait-for-schedule', { milliseconds: Math.max(0, delayMs) })`. For recurring schedules, use `cronTrigger`. For one-time future execution, you can also schedule the event with a future timestamp: `client.sendEvent({ name: 'delayed.job', payload, ts: futureTimestamp })`.

## Q33: How do you implement middleware/logging wrapper for all Trigger.dev jobs?
**A:** Create a higher-order function that wraps the run handler: `function withLogging(job) { const originalRun = job._run; job._run = async (payload, io, ctx) => { io.logger.info('Job started', { jobId: ctx.run.id }); const result = await originalRun(payload, io, ctx); io.logger.info('Job completed', { jobId: ctx.run.id, duration: ... }); return result; }; return job; }`. Apply to all job definitions. For self-hosted, implement as a global plugin.

## Q34: How do you implement a Trigger.dev job that processes large CSV files row by row?
**A:** Read the CSV in a streaming fashion. For each row (or batch of rows), use `io.runTask` to process it. Track progress: processed count, error count. For error rows, log and continue (don't fail the entire job). For very large CSVs (millions of rows), consider splitting into multiple sub-jobs per chunk.

## Q35: How do you implement Trigger.dev job versioning and rollback?
**A:** Each job definition has a `version` field (semver). When you deploy a new version, the old version remains active until promoted. Via the Dashboard or API, you can: (1) rollback to a previous version, (2) run A/B tests between versions, (3) promote a specific version to handle all new events. Version pinning is at the environment level.

## Q36: How do you implement a Trigger.dev job that performs a database migration with verification?
**A:** The job: (1) runs the migration SQL in a task, (2) verifies the migration with data checks (row counts, sample queries), (3) if verification fails, runs a rollback migration in a compensating task. Use `io.runTask` for each migration step with independent retry policies. Log all SQL executed and verification results for audit.

## Q37: How do you implement a Trigger.dev job that integrates with Kubernetes for container orchestration?
**A:** Use the `@trigger.dev/sdk` with custom tasks that call the Kubernetes API. Example task: `await io.runTask('deploy-to-k8s', async () => { const k8s = new K8s({ kubeconfig }); await k8s.createDeployment({ ... }); })`. Use `io.waitForEvent` to wait for deployment readiness. For long-running deployments, use `io.heartbeat()`.

## Q38: How do you implement a Trigger.dev job with fan-out/fan-in pattern (parallel processing with results aggregation)?
**A:** Fan-out: iterate over items and call `io.sendEvent` for each sub-job. Fan-in: the main job waits for all sub-job results using `io.waitForEvent` with a timeout. Collect results and aggregate. Alternatively, use a shared database where sub-jobs write results, and the main job reads them after all sub-jobs complete.

## Q39: How do you implement Trigger.dev job concurrency with "discard new" behavior when queue is full?
**A:** Use `concurrencyLimit` with `mode: 'discard-new'`. When at max concurrency, new events are silently dropped instead of queued. Useful for: periodic sync jobs where skipping one cycle is acceptable, webhook handlers where the source will retry, and real-time notifications where freshness matters more than reliability.

## Q40: How do you implement a Trigger.dev job that generates PDF reports with data from multiple sources?
**A:** The job: (1) fetches data from multiple sources in parallel tasks, (2) merges data in a processing task, (3) generates PDF using a library (Puppeteer, PDFKit), (4) stores PDF to S3/cloud storage, (5) sends notification with download link. Each step is a tracked task with independent error handling.

## Q41: How do you implement Trigger.dev job cancellation from within the job itself?
**A:** Call `io.fail({ message: 'Cancelling due to condition', data: { reason: 'data_invalid' } })` to mark the run as FAILED and stop execution. For graceful cancellation, use conditional checks between tasks: `if (shouldStop) { await io.fail({ ... }); }`. The job can also check an external cancellation flag (Redis, database) between tasks.

## Q42: How do you implement a Trigger.dev job that polls an external API until a condition is met?
**A:** Use a loop with `io.wait` between polls: `while (true) { const status = await checkStatus(); if (status === 'complete') break; await io.wait('wait-for-completion', { seconds: 10 }); }`. Set a maximum number of polls to avoid infinite loops. Use `io.heartbeat()` to prevent timeout during long polling. Each poll iteration is a task.

## Q43: How do you implement a Trigger.dev job with environment-specific behavior (dev vs prod)?
**A:** Check `ctx.environment` in the job: `if (ctx.environment === 'production') { /* send real emails */ } else { /* log only */ }`. Use environment variables for sensitive data (API keys, database URLs). Separate Trigger.dev projects for dev/staging/prod with different API keys. This prevents accidental production mutations from development runs.

## Q44: How do you implement a Trigger.dev job that reads from and writes to Redis for real-time cache updates?
**A:** Use the `ioredis` library within tasks: `await io.runTask('update-cache', async () => { await redis.set(`user:${payload.userId}`, JSON.stringify(data), 'EX', 3600); })`. For cache invalidation patterns: the job updates the database then invalidates the cache. For pub/sub: publish cache invalidation events that other services subscribe to.

## Q45: How do you implement Trigger.dev jobs as webhook endpoints for multiple external services on a single endpoint?
**A:** Use a single webhook trigger with a wildcard path, then route based on the request path or headers: `webhookTrigger({ endpoint: '/webhooks/:source' })`. Inside the job, switch on `payload.source` or `event.path`. Each source has its own verification logic (Stripe, GitHub, SendGrid). This simplifies deployment while maintaining separate verification per source.

## Q46: How do you implement a Trigger.dev job that handles idempotent webhook processing for Stripe events?
**A:** Use Stripe's `idempotency_key` from the request headers as the Trigger.dev idempotency key. Also use the Stripe event ID as a unique constraint in the database. The job: (1) checks if event ID was already processed, (2) if yes, skips, (3) if no, processes and records event ID. This prevents duplicate processing even if Stripe sends the same event twice.

## Q47: How do you implement a Trigger.dev job with graceful timeout handling for slow external APIs?
**A:** Set `timeoutInSeconds` on the job and use `io.heartbeat()` for long-running tasks. For individual API calls, set a timeout in the HTTP client: `fetch(url, { signal: AbortSignal.timeout(10000) })`. On timeout: catch the error, log, and decide whether to retry or fail the task. Use `io.wait` before retry to give the API time to recover.

## Q48: How do you implement Trigger.dev job payload encryption for sensitive data?
**A:** Before calling `client.sendEvent()`, encrypt sensitive fields: `payload.ssn = encrypt(payload.ssn, encryptionKey)`. In the job, decrypt in the first task: `const ssn = decrypt(payload.ssn, encryptionKey)`. Ensure the encryption key is stored as a Trigger.dev environment variable. This protects sensitive data at rest and in transit beyond TLS.

## Q49: How do you implement a Trigger.dev job that syncs data between two databases (source -> target)?
**A:** The job: (1) reads batch from source database (with cursor/pagination), (2) transforms data as needed, (3) writes to target database, (4) updates the cursor, (5) if more data, loops. Use tasks per batch for granular error handling. For large syncs, use `io.wait()` between batches for rate limiting.

## Q50: How do you implement Trigger.dev job orchestration with concurrent task execution within a single job?
**A:** Use `Promise.all` with `io.runTask` calls: `const [result1, result2] = await Promise.all([io.runTask('task1', async () => { ... }), io.runTask('task2', async () => { ... })]);`. Both tasks run in parallel. Each is independently tracked. On failure of either, the Promise.all rejects and the job handles error recovery. For partial success, use `Promise.allSettled`.

## Q51: How do you implement a Trigger.dev job that sends SMS via Twilio with delivery confirmation?
**A:** Use the Twilio SDK in a task: `await io.runTask('send-sms', async () => { const msg = await twilio.messages.create({ body, from, to }); return msg.sid; })`. For delivery confirmation: poll the message status via Twilio API or handle Twilio's status callback webhook in a separate job.

## Q52: How do you implement Trigger.dev job with "poison message" handling (messages that repeatedly fail)?
**A:** Check `ctx.attempt.number` in the job. If a message has failed N times (e.g., 3), route it to a dead letter queue (DLQ): send to a separate "dlq" event that stores the failed message for manual review. Don't attempt further retries. Alert on DLQ messages for operations team investigation.

## Q53: How do you implement a Trigger.dev job that generates and serves dynamic images (OG images)?
**A:** The job: (1) receives image generation parameters, (2) uses Puppeteer/Playwright to render an HTML page to screenshot, (3) optimizes the image (sharp), (4) uploads to S3/CDN, (5) returns the URL. Use `io.runTask` per step. For high volume, pre-warm browser instances to reduce cold start latency.

## Q54: How do you implement Trigger.dev job configuration using environment variables with defaults?
**A:** Use: `const MAX_RETRIES = parseInt(process.env.MAX_RETRIES || '3')`. Define all configurable parameters as env vars with sensible defaults in the job definition. Document expected env vars in the README. For secret values, use Trigger.dev's encrypted environment variables in the Dashboard.

## Q55: How do you implement a Trigger.dev job that handles webhook batch delivery (multiple events in one request)?
**A:** Some services send webhooks in batches. The webhook trigger receives all events in one request. Use `io.runTask` per event: `for (const event of payload.events) { await io.runTask(\`process-${event.id}\`, async () => { ... }); }`. Each event is tracked separately. If one fails, others continue. Acknowledge the batch only after all events are processed.

## Q56: How do you implement a Trigger.dev job that uses a queue for sequential processing of ordered events?
**A:** Use `orderingKey` in `client.sendEvent()`: `client.sendEvent({ name: 'order.event', payload, orderingKey: payload.orderId })`. All events with the same orderingKey are processed sequentially (FIFO). Different orderIds are processed in parallel. This is critical for event sourcing and state machine patterns where event order matters.

## Q57: How do you implement a Trigger.dev job that triggers based on database changes (CDC - Change Data Capture)?
**A:** Use a database trigger or CDC tool (Supabase Realtime, Debezium, pg_notify) to detect changes. On change, emit a Trigger.dev event: `client.sendEvent({ name: 'record.updated', payload: { table, id, changes } })`. The job processes the change asynchronously. For PostgreSQL, use `LISTEN/NOTIFY` or logical replication.

## Q58: How do you implement a Trigger.dev job with exponential backoff for external API calls within a task?
**A:** Custom retry within a task: `async function callWithBackoff(fn, maxRetries = 3) { for (let i = 0; i < maxRetries; i++) { try { return await fn(); } catch (e) { if (i === maxRetries - 1) throw e; await io.wait(\`retry-\${i}\`, { seconds: Math.pow(2, i) }); } } }`. This is for API-specific retries within a task, separate from Trigger.dev's built-in task retry.

## Q59: How do you implement a Trigger.dev job that processes image uploads with multiple transformations?
**A:** The job: (1) downloads the original image, (2) creates multiple variants (thumbnail, medium, large) using sharp, (3) uploads each variant to cloud storage (S3, Cloudinary), (4) updates the database with URLs. Use `Promise.all` for parallel variant generation. Each variant upload is a sub-task for independent error tracking.

## Q60: How do you implement Trigger.dev job monitoring with custom business metrics?
**A:** Within jobs, emit custom metrics via `io.logger.info('metric', { metric: 'order_value', value: payload.amount, currency: 'USD' })`. Send metrics to your observability platform (Datadog, Prometheus) via a webhook integration. The Trigger.dev Dashboard shows run-level metrics; business-level metrics require external aggregation.

## Q61: How do you implement a Trigger.dev job that uses a webhook trigger with IP whitelisting?
**A:** Inside the job, check the source IP from the request metadata: `const clientIp = payload.request.headers['x-forwarded-for'] || payload.request.ip`. Validate against a whitelist: `if (!whitelistedIps.includes(clientIp)) { await io.sendResponse({ status: 403 }); return; }`. For self-hosted, configure IP whitelisting at the reverse proxy level.

## Q62: How do you implement Trigger.dev job deduplication for webhook events with natural idempotency?
**A:** Extract a natural idempotency key from the payload (e.g., Stripe event ID, GitHub delivery ID). Use it as the Trigger.dev event idempotency key: `client.sendEvent({ name: 'webhook.received', idempotencyKey: stripeEventId })`. Trigger.dev deduplicates within the time window. Also implement database-level unique constraints for defense in depth.

## Q63: How do you implement a Trigger.dev job that uses the `waitForEvent` pattern for human approval flows?
**A:** The job pauses at an approval step: `await io.waitForEvent('await-approval', { event: 'order.approved', filter: { orderId: payload.orderId }, timeout: '1h' })`. A separate API endpoint (or human interface) emits the approval event. If approval is received, the job continues. If timeout, the job handles the rejection path (cancel order, notify user).

## Q64: How do you implement a Trigger.dev job that handles rate-limited API calls with queue management?
**A:** Use a global rate limiter (Redis-based) within the job: `await io.runTask('api-call', async () => { await rateLimiter.wait(); return apiCall(); })`. The rate limiter manages concurrency across all job instances. For per-instance limits, use Trigger.dev's built-in `rateLimit`. For external API rate limits, parse response headers and adjust dynamically.

## Q65: How do you implement Trigger.dev job testing with mocked dependencies (unit tests)?
**A:** Create test fixtures that mock the `io` object: `const mockIo = { runTask: vi.fn((id, fn) => fn()), logger: { info: vi.fn(), error: vi.fn() }, wait: vi.fn() }`. Test the run function by calling it directly with the mock io and test payload. This enables fast unit tests without Trigger.dev infrastructure.

## Q66: How do you implement a Trigger.dev job that processes WebSocket events/messages?
**A:** The trigger receives WebSocket messages (via the application server). Each message is sent as a Trigger.dev event: `client.sendEvent({ name: 'ws.message', payload: { connectionId, data } })`. The job processes the message asynchronously (AI processing, data enrichment, broadcast preparation). Use orderingKey per connection for sequential processing per user.

## Q67: How do you implement Trigger.dev job with S3 event notifications as triggers?
**A:** Configure S3 bucket to send events to an SQS queue or directly to an HTTP endpoint. If using the Trigger.dev webhook trigger, set up S3 event notification to POST to the webhook URL. The job receives the S3 event payload (bucket, key, size) and processes the uploaded file. Use idempotency based on S3 event ID.

## Q68: How do you implement a Trigger.dev job that includes a maintenance window (no execution during certain hours)?
**A:** At the start of the job, check the current time: `const now = new Date(); const hour = now.getHours(); if (hour >= 2 && hour < 4) { await io.wait('wait-outside-maintenance', { milliseconds: (4 - hour) * 3600000 }); }`. For scheduled jobs, use `scheduleTrigger` with exclusion periods to avoid running during maintenance windows entirely.

## Q69: How do you implement a Trigger.dev job that enriches data by calling multiple external APIs in parallel?
**A:** Use `Promise.all` with `io.runTask` per API: `const [geo, weather, reviews] = await Promise.all([io.runTask('get-geo', geoApi), io.runTask('get-weather', weatherApi), io.runTask('get-reviews', reviewsApi)]);`. Each API call is tracked independently. On partial failure (one API down), use `Promise.allSettled` and handle missing data gracefully.

## Q70: How do you implement a Trigger.dev job that handles file expiration/deletion after a retention period?
**A:** Use a scheduled (cron) job that runs daily. Query expired records from the database. For each expired file: `await io.runTask(\`delete-${fileId}\`, async () => { await storage.delete(fileKey); await db.update({ deleted: true }); })`. Use batching with concurrency limits to avoid overwhelming storage API. Log all deletions for audit.

## Q71: How do you implement Trigger.dev integration with Auth0/Okta for user management workflows?
**A:** Subscribe to Auth0/Okta webhook events (user.signup, user.delete, user.update). In the Trigger.dev job: create user in your database, send welcome email, set up default resources. For user deletion: clean up user data, revoke tokens, archive records. Use idempotency keys from the identity provider's event IDs.

## Q72: How do you implement a Trigger.dev job that dynamically creates child jobs based on runtime data?
**A:** At runtime, iterate over items and call `io.sendEvent` for each child: `for (const item of payload.items) { await io.sendEvent({ name: 'process.item', payload: item }); }`. Each child job is independent with its own retries and tracking. The parent job completes after spawning all children. Use `io.waitForEvent` if the parent needs to collect results.

## Q73: How do you implement a Trigger.dev job with conditional webhook response (success vs error)?
**A:** Use `io.sendResponse()` to set the HTTP response before the job completes. For validation errors: `await io.sendResponse({ status: 400, body: { error: 'Invalid payload' } })`. For successful receipt: `await io.sendResponse({ status: 200, body: { received: true } })`. The response is sent immediately; the job continues processing in the background.

## Q74: How do you implement a Trigger.dev job that uses remote caching (Redis) to avoid redundant API calls?
**A:** Before calling an external API, check a Redis cache: `const cached = await redis.get(cacheKey); if (cached) return JSON.parse(cached);`. After fetching, store: `await redis.set(cacheKey, JSON.stringify(result), 'EX', ttl)`. Use the cache key based on API endpoint + parameters. Task-level caching prevents redundant API calls even across different job runs.

## Q75: How do you implement a Trigger.dev job that processes streaming data from Kafka?
**A:** A consumer job reads from Kafka topics: `await io.runTask('consume-kafka', async () => { const messages = await consumer.consume({ topic: 'orders', maxMessages: 100 }); for (const msg of messages) { await io.sendEvent({ name: 'order.event', payload: JSON.parse(msg.value) }); } })`. Each Kafka message triggers a separate Trigger.dev job. Use consumer groups for horizontal scaling.

## Q76: How do you implement a Trigger.dev job with a "dry run" mode for testing?
**A:** Check a `dryRun` flag in payload: `if (payload.dryRun) { io.logger.info('DRY RUN - would process', { orderId }); return { dryRun: true, wouldDo: '...' }; }`. In dry run mode, skip actual mutations (DB writes, API calls) but log all actions. Useful for testing before enabling in production. The flag is set when triggering the event.

## Q77: How do you implement a Trigger.dev job that handles OAuth token refresh automatically?
**A:** Before making API calls with an access token, check if expired. If expired, refresh: `if (isTokenExpired(token)) { const newToken = await refreshToken(refreshToken); await db.updateToken(newToken); token = newToken; }`. Store token metadata (expiry, refresh token) in the database. The refresh logic can be a shared utility task.

## Q78: How do you implement Trigger.dev job result aggregation for batch processing (MapReduce pattern)?
**A:** Map phase: fan-out to many sub-jobs via `io.sendEvent` (one per data shard). Reduce phase: a result aggregation job that waits for all sub-jobs to report via `io.waitForEvent`. Use a unique batch ID passed to all sub-jobs. The reducer collects results until all complete or timeout, then produces the final output.

## Q79: How do you implement a Trigger.dev job that uses WebSockets to push real-time progress to clients?
**A:** Use `io.runTask` for progress steps. After each step, emit a progress event: `io.sendEvent({ name: 'job.progress', payload: { runId: ctx.run.id, step: 'processing', progress: 50 } })`. A separate WebSocket server subscribes to these events and pushes to connected clients using the runId for routing.

## Q80: How do you implement a Trigger.dev job with integration testing against a staging environment?
**A:** Deploy jobs to staging environment. Use a test suite that: (1) sends events with known test data, (2) polls for run completion (via API), (3) asserts run status is SUCCESS, (4) verifies side effects (database state, API calls). Use staging credentials and test databases. Run integration tests in CI before production deployment.

## Q81: How do you implement a Trigger.dev job that uses the `io.sendEvent` with a delay for scheduled notifications?
**A:** Use a future timestamp: `io.sendEvent({ name: 'notification.send', payload, ts: new Date(Date.now() + 3600000).toISOString() })`. The event is queued and delivered at the specified timestamp. This schedules one-time notifications without a cron job. For recurring notifications, the job itself re-emits with the next schedule time.

## Q82: How do you implement a Trigger.dev job that handles API pagination for large result sets?
**A:** In a loop: fetch a page, process, advance cursor: `let cursor = null; do { const result = await api.list({ cursor }); await io.runTask(\`process-page-\${cursor}\`, async () => { /* process results */ }); cursor = result.nextCursor; } while (cursor);`. Each page is a tracked task. Use `io.wait()` between pages for rate limiting.

## Q83: How do you implement Trigger.dev job with environment variable validation at startup?
**A:** At the top of the job file, validate required env vars: `function validateEnv() { const required = ['DATABASE_URL', 'API_KEY']; for (const key of required) { if (!process.env[key]) throw new Error(`Missing required env var: ${key}`); } }`. Call `validateEnv()` at module load time. The job fails immediately if configuration is missing, providing clear error messages.

## Q84: How do you implement a Trigger.dev job that processes webhook events with idempotent deduplication across multiple webhook sources?
**A:** Create a generic deduplication task: `await io.runTask('deduplicate', async () => { const key = `${payload.source}:${payload.eventId}`; const exists = await redis.setnx(`dedup:${key}`, '1'); if (!exists) { await io.fail({ message: 'Duplicate event' }); } })`. Use Redis SETNX for atomic dedup check. Set TTL on the dedup key (e.g., 24h).

## Q85: How do you implement a Trigger.dev job that uses a custom Docker worker for specific runtime requirements?
**A:** For self-hosted: run Trigger.dev workers in custom Docker containers with specific dependencies (Python, ffmpeg, Chrome). The worker connects to the Trigger.dev platform or self-hosted instance. Define the Dockerfile with your runtime and the Trigger.dev worker binary. Jobs run in this environment with access to all installed tools.

## Q86: How do you implement a Trigger.dev job with Circuit Breaker pattern for external service calls?
**A:** Implement a circuit breaker class: `const breaker = new CircuitBreaker({ threshold: 5, resetTimeout: 30000 });`. Before API call: `if (!breaker.isAllowed()) { await io.wait('circuit-open', { seconds: 30 }); }`. After call: `breaker.recordSuccess()` or `breaker.recordFailure()`. The circuit prevents cascading failures when an external service is down.

## Q87: How do you implement a Trigger.dev job that handles user data export (GDPR compliance)?
**A:** The job receives a user ID. It: (1) collects data from all tables/databases related to the user, (2) compiles into a structured format (JSON, CSV), (3) packages into a ZIP file, (4) uploads to secure storage, (5) sends download link to the user with expiration. Each data source query is a tracked task. Verify data completeness before packaging.

## Q88: How do you implement a Trigger.dev job with dynamic webhook header forwarding?
**A:** In the webhook trigger, forward specific headers to the job payload: `webhookTrigger({ endpoint: '/webhook', headers: ['x-request-id', 'x-source'] })`. The forwarded headers are available in `payload.request.headers`. Use this for: traceability (forward tracing headers), source identification, and custom routing logic.

## Q89: How do you implement a Trigger.dev job that uses file locking to prevent concurrent processing of the same resource?
**A:** Use a distributed lock (Redis Redlock pattern): `const lock = await redis.lock(`resource:${payload.resourceId}`, 30000); if (!lock) { await io.fail({ message: 'Resource locked, skipping' }); }`. The lock prevents two jobs from processing the same order/file simultaneously. Release the lock in a finally block: `await lock.unlock()`.

## Q90: How do you implement a Trigger.dev job that periodically cleans up stale data with batched deletions?
**A:** Scheduled job runs daily. Queries for stale records: `const stale = await db.findMany({ where: { updatedAt: { lt: daysAgo(90) } }, take: 1000 })`. For each batch: `await io.runTask(\`cleanup-batch\`, async () => { await db.deleteMany({ where: { id: { in: staleIds } } }); })`. Loop until no more stale records. Log deletion counts and duration.

## Q91: How do you implement a Trigger.dev job that generates webhook events for downstream systems?
**A:** After processing, the job calls an external system via webhook: `await io.runTask('notify-downstream', async () => { await fetch('https://downstream.example.com/webhook', { method: 'POST', headers: { 'X-Signature': sign(payload, secret) }, body: JSON.stringify(payload) }); })`. Use retry for delivery failures. This makes Trigger.dev act as an event producer.

## Q92: How do you implement a Trigger.dev job that handles concurrent requests for the same resource with queuing?
**A:** Use `orderingKey` for FIFO per resource: `client.sendEvent({ name: 'update.resource', orderingKey: payload.resourceId })`. Events for the same resourceId process sequentially. Different resources process in parallel. This ensures: no concurrent modifications, correct ordering of updates, and no lost updates.

## Q93: How do you implement a Trigger.dev job with dynamic rate limiting based on API response headers?
**A:** Parse rate limit headers from API responses: `const remaining = parseInt(response.headers.get('X-RateLimit-Remaining')); const reset = parseInt(response.headers.get('X-RateLimit-Reset'));`. If remaining is low, calculate wait time: `const waitMs = Math.max(0, reset * 1000 - Date.now() + 1000)`. Use `io.wait('rate-limit', { milliseconds: waitMs })` before the next call.

## Q94: How do you implement a Trigger.dev job that performs A/B testing of job configurations?
**A:** Define two job versions with different configurations (e.g., different retry strategies, different API endpoints). Route events to version A or B based on payload hash: `const version = payload.userId % 2 === 0 ? 'A' : 'B';`. Compare metrics: success rate, duration, cost. Promote the winning version based on statistical significance.

## Q95: How do you implement a Trigger.dev job that handles multi-tenant isolation (data separation per tenant)?
**A:** Pass tenant ID in every event payload. In the job, scope all queries by tenant: `WHERE tenantId = payload.tenantId`. Use `concurrencyLimit` per tenant: `concurrencyLimit: { max: 5, key: payload.tenantId }`. Log tenant ID in all log entries. Use separate database schemas (per-tenant) or row-level security based on tenant ID.

## Q96: How do you implement a Trigger.dev job that uses serverless Redis (Upstash) for caching and rate limiting?
**A:** Use Upstash Redis REST API (HTTP-based, no persistent connection, works in serverless): `const redis = new Redis({ url: process.env.UPSTASH_REDIS_REST_URL, token: process.env.UPSTASH_REDIS_TOKEN })`. Use it for: rate limiting checks, caching, distributed locking. Since Trigger.dev jobs run on workers (not serverless), you can also use `ioredis` for persistent connections.

## Q97: How do you implement a Trigger.dev job that sends event notifications to an external queue (SQS, RabbitMQ)?
**A:** After processing, send a message to SQS/RabbitMQ: `await io.runTask('queue-notification', async () => { await sqs.sendMessage({ QueueUrl: queueUrl, MessageBody: JSON.stringify({ event: 'order.processed', data: result }) }); })`. This bridges Trigger.dev with other queue-based systems. The external system processes the notification independently.

## Q98: How do you implement a Trigger.dev job that processes events in strict order per entity?
**A:** Use `orderingKey` on `client.sendEvent()`: `client.sendEvent({ name: 'entity.update', payload, orderingKey: payload.entityId })`. Trigger.dev processes events with the same orderingKey sequentially. This guarantees: no concurrent processing of the same entity, correct event ordering, and avoidance of race conditions. Different entityIds process in parallel.

## Q99: How do you implement a Trigger.dev job that generates and sends monthly invoices?
**A:** Scheduled job runs on the 1st of each month. It: (1) queries customers with monthly billing, (2) for each customer: calculates invoice, creates invoice record, calls Stripe API, (3) sends invoice email. Use `Promise.all` with concurrency limit for parallel processing. Use `io.runTask` per customer for granular tracking. Log failures per customer without failing the entire batch.

## Q100: How do you implement a Trigger.dev job that uses webhook triggers with HMAC signature verification for security?
**A:** In the webhook job, extract the signature from headers, compute HMAC with the shared secret, and compare: `const computed = crypto.createHmac('sha256', secret).update(JSON.stringify(payload.request.body)).digest('hex'); const received = payload.request.headers['x-signature']; if (!crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(received))) { await io.sendResponse({ status: 401, body: 'Invalid signature' }); return; }`. Always use timing-safe comparison to prevent timing attacks.
