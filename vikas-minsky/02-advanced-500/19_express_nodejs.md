## 38. Express.js + Node.js Advanced (976–1000)

976. Explain libuv architecture.
   libuv is a C library providing Node.js's event loop and async I/O. It handles file system, DNS, network, and thread pool operations via epoll/kqueue/IOCP, exposing callback-based APIs.

977. How does the event queue operate?
   The event loop processes phases in order: timers, pending callbacks, idle/prepare, poll (I/O), check (setImmediate), and close callbacks. Each phase has a FIFO queue; the loop blocks in the poll phase waiting for I/O.

978. Explain microtasks vs macrotasks.
   Microtasks (Promise callbacks, `queueMicrotask`) execute after each macrotask phase before the next phase. Macrotasks (setTimeout, setInterval, I/O) run in their respective phases. Microtasks have higher priority.

979. What causes event loop starvation?
   Starvation occurs when microtasks (e.g., recursive Promises) or synchronous CPU-heavy operations block the event loop indefinitely. Long-running tasks should be offloaded to worker threads or split with `setImmediate`.

980. Explain async_hooks usage.
   `async_hooks` tracks async resource lifetimes via `init`, `before`, `after`, and `destroy` hooks. It enables context propagation (AsyncLocalStorage), diagnostics, and correlation IDs across async chains.

981. How do streams handle backpressure?
   Streams manage backpressure via `highWaterMark` and `drain` events. When the writable buffer exceeds the threshold, `write()` returns `false`; the reader should pause until `drain` fires.

982. Explain TCP connection lifecycle.
   TCP lifecycle: client `connect()` → SYN/SYN-ACK handshake → established → data transfer → `close()` → FIN/FIN-ACK termination. Express abstracts this but `server.close()` ensures graceful shutdown.

983. What are HTTP keep-alive optimizations?
   Keep-alive reuses TCP connections for multiple HTTP requests, reducing handshake overhead. Configure `keepAliveTimeout` and `maxKeepAliveRequests` in `http.createServer` for optimal resource use.

984. Explain websocket handshake internals.
   The WebSocket handshake upgrades an HTTP GET with `Upgrade: websocket` and `Sec-WebSocket-Key`. The server responds with `101 Switching Protocols` and a computed `Sec-WebSocket-Accept` hash.

985. How does clustering distribute load?
   `cluster` forks worker processes sharing the same server port. The OS round-robins incoming connections (or uses `SO_REUSEPORT`) across workers, utilizing multi-core CPUs.

986. Explain sticky sessions.
   Sticky sessions route requests from the same client to the same worker, preserving in-memory state. Implemented via a cookie (e.g., `server-id`) configured on the load balancer.

987. What are worker pool bottlenecks?
   Worker threads share the libuv thread pool (default 4). CPU-intensive or blocking operations can exhaust it, starving other async operations. Increase `UV_THREADPOOL_SIZE` or isolate workloads.

988. Explain V8 garbage collection.
   V8 uses generational GC: young generation (new space) collected frequently via Scavenge, old generation (old space) collected via Mark-Sweep-Compact. GC pauses can spike latency; monitor with `--trace-gc`.

989. What causes heap out-of-memory errors?
   OOM errors stem from memory leaks (unreleased references), large buffers, unclosed streams, unbounded caches, or V8 memory limits (~1.4GB default). Profile with `--inspect` memory snapshots.

990. Explain memory profiling techniques.
   Use Chrome DevTools Memory tab (heap snapshots, allocation timeline), `process.memoryUsage()`, `clinic.js` heap profiler, and `--heapsnapshot-signal` for production snapshots.

991. What are Node.js security hardening techniques?
   Hardening includes input validation, Helmet for headers, rate limiting, `--disallow-code-generation-from-strings`, sandboxed `vm` modules, dependency scanning, and principle of least privilege.

992. Explain event emitter leak warnings.
   Leak warnings appear when >10 listeners are attached to an emitter (`MaxListenersExceededWarning`). Increase limit with `emitter.setMaxListeners(n)` or find the source of excessive subscriptions.

993. What are async context propagation patterns?
   `AsyncLocalStorage` propagates context (user, request ID) across async operations without explicit passing. Middleware creates a store per request, accessible anywhere in the async chain.

994. Explain graceful degradation strategies.
   Graceful degradation maintains partial functionality during failures. Strategies include circuit breakers, fallback responses, caching degraded data, feature degradation (disable non-critical features), and clear user messaging.

995. How do circuit breakers protect services?
   Circuit breakers monitor failure rates; on threshold breach, they open (blocking calls) for a cooldown period, then half-open (testing) before closing on success. Libraries like `opossum` implement this.

996. Explain distributed queue architectures.
   Distributed queues (Redis Streams, Bull, RabbitMQ, Kafka) decouple producers and consumers. Queues provide buffering, backpressure, retries, DLQs, and fan-out for reliable async processing.

997. What are high-throughput Node.js design patterns?
   Patterns include stream processing (backpressure-aware), worker threads for CPU tasks, clustering for multi-core, connection pooling, async iteration with `for await`, and backoff-based retry.

998. Explain realtime scaling architectures.
   Realtime scaling uses WebSocket gateways with pub/sub (Redis) for horizontal scaling. Each server broadcasts to its connected clients; `socket.io` with Redis adapter handles cross-server events.

999. How do you debug production Node.js incidents?
   Debug with structured logs (correlation IDs), `--inspect` with port forwarding (secure), heap snapshots on OOM, CPU profiling with `clinic.js`, distributed tracing, and monitoring dashboards.

1000. Design a globally scalable SaaS platform using Next.js, NestJS, PostgreSQL, Redis, Docker, CI/CD, tRPC, and Node.js.
    Use Next.js (edge-rendered, regions) for the frontend, NestJS microservices for business logic, tRPC for type-safe frontend-backend communication, PostgreSQL (read replicas + Citus sharding) for persistence, Redis for caching/queues/pub-sub, Docker + Kubernetes for orchestration, CI/CD with GitHub Actions + ArgoCD, global CDN (Cloudflare) for static assets, and OpenTelemetry for observability.

---

# Additional 500 Expert-Level Interview Questions (Unique Set)
