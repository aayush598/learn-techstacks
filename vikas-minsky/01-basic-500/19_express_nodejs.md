## 19. Express.js + Node.js (476–500)

476. What is Node.js?
     Node.js is a JavaScript runtime built on Chrome's V8 engine for building server-side applications. It uses an event-driven, non-blocking I/O model, making it efficient for high-throughput, I/O-heavy applications like APIs, real-time services, and microservices.

477. Explain event loop in Node.js.
     The event loop processes asynchronous callbacks in phases: timers (setTimeout/setInterval), pending callbacks (I/O), idle/prepare, poll (I/O events), check (setImmediate), and close callbacks. It enables non-blocking concurrency on a single thread.

478. What are worker threads?
     Worker threads run JavaScript in parallel on separate CPU cores, enabling CPU-intensive operations (crypto, compression, image processing) without blocking the event loop. They communicate with the main thread via message passing.

479. Difference between blocking and non-blocking I/O?
     Blocking I/O (synchronous) pauses execution until the operation completes. Non-blocking I/O (asynchronous) initiates the operation and continues execution, with a callback invoked on completion. Node.js excels at non-blocking I/O for scalable servers.

480. Explain streams in Node.js.
     Streams process data piece-by-piece instead of loading entire datasets into memory. Types include Readable (read data), Writable (write data), Duplex (both), and Transform (modify data). Streams handle large files, network data, and real-time processing efficiently.

481. What are buffers?
     Buffers are fixed-size memory allocations for handling raw binary data in Node.js. They work with streams, file I/O, and network operations where data arrives in chunks before encoding to strings.

482. Explain middleware in Express.js.
     Middleware functions have access to `req`, `res`, and `next`. They execute code, modify request/response objects, end responses, or call the next middleware. Express uses middleware for parsing, logging, authentication, error handling, and routing.

483. What is req-res lifecycle?
     The request-response lifecycle starts when a request arrives, passes through middleware in order, reaches the route handler, sets response properties, and sends the response. Middleware runs sequentially; `next()` passes control to the next handler.

484. Explain error handling middleware.
     Error handling middleware has four parameters `(err, req, res, next)`. It catches errors passed via `next(err)` from previous middleware or route handlers, logs them, and sends appropriate error responses with status codes.

485. What are async handlers?
     Async handlers wrap async route handlers to catch promise rejections automatically. Without them, unhandled promise rejections crash the server. Libraries like `express-async-errors` or wrapper functions forward errors to error middleware.

486. Explain clustering in Node.js.
     Clustering forks the main process into multiple worker processes sharing the same port, utilizing all CPU cores. The master process distributes incoming connections across workers using round-robin, enabling horizontal scaling on a single machine.

487. What is backpressure?
     Backpressure occurs when data is produced faster than it can be consumed. In streams, backpressure pauses the readable stream when the writable buffer is full, preventing memory overflow. Proper backpressure handling ensures memory-efficient streaming.

488. Explain Node.js memory leaks.
     Memory leaks happen when objects are retained longer than needed, often from: global variables, uncleared timers/intervals, closure references, event listeners not removed, and cached data without size limits. Detected via heap snapshots and monitoring.

489. What are child processes?
     Child processes (`child_process` module) spawn separate OS processes for running system commands, scripts, or CPU-intensive work. Types include `spawn` (streaming), `exec` (buffered), `fork` (IPC communication), and `execFile` (direct binary execution).

490. Explain authentication in Express.
     Authentication in Express uses session-based (cookie storing session ID, server stores session data) or JWT-based (self-contained token) approaches. Middleware checks auth before protected routes, with Passport.js providing strategy-based authentication.

491. What are common Express security risks?
     Risks include: XSS (cross-site scripting), CSRF (cross-site request forgery), SQL injection, insecure direct object references, mass assignment, path traversal in file serving, and Server-Side Template Injection. Mitigated by validation, sanitization, and security middleware.

492. Explain rate limiting.
     Rate limiting restricts requests per IP or user within a time window using `express-rate-limit` middleware. It prevents brute force attacks, DDoS amplification, and API abuse. Limits are communicated via rate limit headers and 429 status code.

493. What is event-driven architecture?
     Event-driven architecture uses events for communication between services. Components emit events when state changes, and listeners react asynchronously. Node.js's EventEmitter, message queues (RabbitMQ, Kafka), and pub/sub systems enable loose coupling.

494. Explain queues in Node.js.
     Queues manage asynchronous work by storing tasks for later processing. Libraries like Bull (Redis-backed) handle job scheduling, retries, rate limiting, and concurrency control. Queues decouple request processing from background work.

495. What are microservices?
     Microservices decompose applications into small, independent services, each owning its data and domain. They communicate via REST, gRPC, or message queues, deploy independently, and scale individually — improving team autonomy and fault isolation.

496. Explain horizontal scaling.
     Horizontal scaling adds more server instances behind a load balancer to handle increased traffic. Stateless applications (no server-side session) scale easily. Stateful services require distributed caching (Redis), sticky sessions, or database replication.

497. What are Node.js performance bottlenecks?
     Bottlenecks include: synchronous CPU-intensive operations blocking the event loop, memory leaks, inefficient database queries (N+1), lack of connection pooling, large JSON payloads, unoptimized loops, and garbage collection pauses.

498. Explain graceful shutdown.
     Graceful shutdown stops the server without dropping active connections. It stops accepting new requests, drains existing connections (with timeout), closes database connections, completes background jobs, and finally exits. Implemented via `process.on('SIGTERM')`.

499. What monitoring tools do you use for Node.js?
     Tools include: PM2 for process management and metrics, Prometheus + Grafana for metrics dashboards, Sentry/Datadog for error tracking, Winston/Pino for structured logging, clinic.js for performance profiling, and OpenTelemetry for distributed tracing.

500. Design a scalable startup architecture using Node.js, PostgreSQL, Redis, Docker, CI/CD, and Next.js.
     A scalable startup architecture uses Next.js (frontend + SSR + API routes), Node.js/NestJS microservices for backend logic, PostgreSQL for persistent data with read replicas, Redis for caching and session management, Docker containers with Docker Compose for local dev and Kubernetes for production, CI/CD via GitHub Actions (lint → test → build → deploy to staging/production), and horizontal scaling via load balancers. This stack handles rapid growth with caching, connection pooling, background job queues, and blue-green or canary deployments for zero-downtime updates.

# Startup-Level System Design & Practical Rounds

In top startups, interviews also heavily focus on practical engineering decisions. Prepare these additional themes deeply:

- Authentication architecture
- RBAC and permissions
- Multi-tenant SaaS design
- Notification systems
- Queue systems
- Realtime collaboration
- WebSocket scaling
- API gateway design
- Caching architecture
- Database sharding
- Search systems
- AI workflow integrations
- Feature flags
- Billing systems
- Audit logs
- Observability stack
- Error tracking
- Distributed tracing
- Monorepo architecture
- Turborepo setup
- Nx architecture
- Serverless tradeoffs
- Edge computing
- CDN optimization
- Performance profiling
- Web security fundamentals
- OWASP Top 10
- Infrastructure cost optimization
- Event-driven architecture
- Kafka basics
- Message queues
- Data consistency strategies
- CAP theorem
- Idempotency strategies
- Retry patterns
- Rate limiting
- Feature rollout systems
- CI/CD rollback handling
- Database migration safety
- High availability architecture
- Zero downtime deployment
- API schema evolution
- Testing pyramid
- Contract testing
- SRE fundamentals
- Incident management
- Production debugging
- Memory optimization
- Large-scale frontend architecture
- Accessibility standards
- SEO optimization
- Frontend rendering strategies
- Graph rendering optimization
- Workflow engine design
- AI-powered product integrations

# Final Preparation Strategy

1. Prepare answers with practical production examples.
2. Be able to explain tradeoffs.
3. Practice system design daily.
4. Build at least 2 production-grade projects.
5. Learn deployment deeply.
6. Practice debugging discussions.
7. Prepare behavioral stories using STAR format.
8. Focus on scalability, performance, and security.
9. Prepare architecture diagrams.
10. Practice coding rounds with TypeScript.

---

# Additional 500 Advanced Interview Questions (Unique Set)
