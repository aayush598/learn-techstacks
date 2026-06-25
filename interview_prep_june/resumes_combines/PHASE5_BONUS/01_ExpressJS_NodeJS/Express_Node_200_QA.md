# Express.js & Node.js Backend - 200+ Interview Q&A

## Express.js (Q1-Q90)
### Q1: What is Express.js? How does middleware work?
**Answer:** Express is a minimal Node.js web framework. Middleware are functions that access req, res, next. Each middleware can: modify req/res, end response, call next() to pass control. `app.use(middleware)` for all paths, `app.get('/path', middleware)` for specific routes. Order matters - middleware executes in registration order. Error middleware: `(err, req, res, next)` with 4 params.

### Q2: Express error handling middleware?
**Answer:** Define with 4 parameters: `app.use((err, req, res, next) => { ... })`. Catch async errors by wrapping: `const asyncHandler = fn => (req,res,next) => Promise.resolve(fn(req,res,next)).catch(next)`. Send proper HTTP status codes and structured error responses.

### Q3: Express vs FastAPI - which to choose?
**Answer:** Express: JavaScript/Node ecosystem, async via callbacks/promises, larger community/middleware ecosystem. FastAPI: Python, native async/await, automatic OpenAPI docs, Pydantic validation, dependency injection, type safety. Choose based on team expertise, ecosystem needs (Node libraries vs Python/AI libraries), and performance reqs.

## Node.js Core (Q91-Q180)
### Q4: Node.js event loop phases?
**Answer:** (1) timers: setTimeout, setInterval callbacks. (2) pending callbacks: I/O callbacks deferred to next iteration. (3) idle/prepare: internal use. (4) poll: retrieve new I/O events, execute I/O callbacks. (5) check: setImmediate callbacks. (6) close callbacks: socket close, etc. Microtasks: process.nextTick runs after each phase (highest priority!), Promise callbacks run after each microtask batch.

### Q5: process.nextTick vs setImmediate vs setTimeout?
**Answer:** nextTick: runs before next phase (highest priority). setImmediate: runs in check phase (after poll). setTimeout: runs in timers phase. nextTick can starve I/O if used recursively. setImmediate is safer for deferring work. Order: nextTick → timer → I/O → check → close.

### Q6: Streams in Node.js - types and use cases?
**Answer:** Readable: source of data (file read, HTTP request). Writable: destination (file write, HTTP response). Duplex: both (TCP socket). Transform: modify data (compression, encryption). events: 'data', 'end', 'error', 'finish'. pipe() handles backpressure automatically. Use streams for large files, HTTP bodies, real-time data processing.

### Q7: Cluster module - how does it work?
**Answer:** `cluster.fork()` creates worker processes sharing same server port. Master distributes connections (round-robin on Linux, OS-dependent on Windows). Workers are separate Node processes (separate memory, event loops). Benefits: utilize multi-core CPUs. Downside: each worker has own memory (not shared). Alternatives: PM2 cluster mode.

### Q8: Child process methods - spawn vs exec vs fork?
**Answer:** spawn: streams I/O, no max buffer, for long-running processes. exec: buffers output, maxBuffer (default 200KB), for short commands. execFile: like exec but directly executes file (no shell). fork: spawns new Node process, with IPC channel, for CPU-intensive tasks.

### Q9: CommonJS vs ES Modules - differences?
**Answer:** CJS: require()/module.exports, synchronous, runtime resolution, can use __dirname/__filename. ESM: import/export, static analysis (enables tree-shaking), async, top-level await, no __dirname by default. package.json: "type": "module" for ESM, or .mjs/.cjs extensions. CJS require() in ESM via createRequire().

### Q10: EventEmitter pattern?
**Answer:** Core Node pattern: `emitter.on('event', handler)`, `emitter.emit('event', data)`. Used throughout Node (HTTP server, streams, file system). Max listeners: 10 by default (warnings >10, set via setMaxListeners). Once: `emitter.once()` (auto-removes after first emit). RemoveListener to clean up (prevent memory leaks).

## Package Management & Tools (Q181-Q200)
### Q11: package-lock.json - purpose?
**Answer:** Locks exact dependency versions (including transitive dependencies) for reproducible builds. Contains integrity hashes for security. Should be committed to git. npm ci uses lockfile only (faster, stricter). package.json specifies version ranges (^1.0.0 allows minor/patch), lockfile pins exact versions.

### Q12: npx vs npm?
**Answer:** npm: install and manage packages. npx: execute node packages without installing globally. Useful for one-off commands (npx create-react-app), running specific package versions, executing from local node_modules (npx jest). Falls back to downloading if not installed locally.
