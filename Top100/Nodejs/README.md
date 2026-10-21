# Node.js Interview Questions and Answers

## Q1: What is Node.js?
**A:** Node.js is an open-source, cross-platform JavaScript runtime environment built on Chrome's V8 engine that executes JavaScript code outside a web browser.

## Q2: Is Node.js a programming language?
**A:** No, Node.js is a runtime environment for executing JavaScript, not a programming language itself.

## Q3: What is the V8 engine?
**A:** V8 is Google's open-source high-performance JavaScript and WebAssembly engine, written in C++, that compiles JavaScript to native machine code.

## Q4: What is libuv?
**A:** libuv is a multi-platform C library that provides Node.js with asynchronous I/O, the event loop, thread pool, and other asynchronous capabilities.

## Q5: What does event-driven architecture mean in Node.js?
**A:** Node.js uses an event-driven architecture where actions trigger events, and event handlers (callbacks) are executed when those events occur, enabling non-blocking operations.

## Q6: What is non-blocking I/O?
**A:** Non-blocking I/O allows a program to initiate an I/O operation and continue executing other code without waiting for the operation to complete.

## Q7: How does the Node.js event loop work?
**A:** The event loop continuously checks the call stack and callback queues, executing pending callbacks in a specific order across multiple phases.

## Q8: What are the phases of the event loop?
**A:** The event loop phases are: timers, I/O callbacks, idle/prepare, poll, check, and close callbacks.

## Q9: What happens in the timers phase?
**A:** The timers phase executes callbacks scheduled by setTimeout and setInterval.

## Q10: What happens in the I/O callbacks phase?
**A:** The I/O callbacks phase executes callbacks for some system operations like TCP errors, deferred from the poll phase.

## Q11: What is the idle/prepare phase?
**A:** The idle/prepare phase is used internally by libuv for housekeeping and preparing before the poll phase.

## Q12: What happens in the poll phase?
**A:** The poll phase retrieves new I/O events, executes I/O callbacks, and blocks waiting for events when appropriate.

## Q13: What happens in the check phase?
**A:** The check phase executes setImmediate callbacks after the poll phase completes.

## Q14: What happens in the close callbacks phase?
**A:** The close callbacks phase executes close event callbacks, such as when a socket or handle is closed.

## Q15: What is the difference between process.nextTick and setImmediate?
**A:** process.nextTick fires before the next event loop phase begins, while setImmediate executes in the check phase after the poll phase.

## Q16: What is a microtask in Node.js?
**A:** Microtasks are callbacks from Promise resolutions and process.nextTick that are executed between each event loop phase, with nextTick having higher priority than Promise callbacks.

## Q17: What is CommonJS?
**A:** CommonJS is a module system used by default in Node.js that uses require() to import modules and module.exports to export them.

## Q18: What are ES modules?
**A:** ES modules (ESM) are the official JavaScript module system using import and export keywords, supported in Node.js with .mjs extension or type:module in package.json.

## Q19: What is the difference between require and import?
**A:** require is synchronous, loads modules at runtime, and is used in CommonJS. import is asynchronous, statically analyzed, and used in ES modules.

## Q20: How does Node.js module caching work?
**A:** Modules are cached after the first time they are loaded, meaning subsequent require calls return the same cached module instance.

## Q21: What is package.json?
**A:** package.json is a JSON file in the root of a project that defines metadata, dependencies, scripts, and configuration for a Node.js application.

## Q22: What is node_modules?
**A:** node_modules is the directory where npm installs project dependencies, following a nested dependency tree structure.

## Q23: What is npm?
**A:** npm (Node Package Manager) is the default package manager for Node.js, used to install, manage, and publish packages.

## Q24: What is the difference between npm and yarn?
**A:** Yarn uses a deterministic lockfile (yarn.lock), offers offline caching, and is generally faster, while npm uses package-lock.json and is bundled with Node.js.

## Q25: What is pnpm?
**A:** pnpm is a fast, disk-space-efficient package manager that uses hard links and symlinks to avoid duplicating packages across projects.

## Q26: What is a callback function?
**A:** A callback is a function passed as an argument to another function to be executed after an asynchronous operation completes.

## Q27: What is callback hell?
**A:** Callback hell is the nesting of multiple callback functions that creates deeply indented, unreadable, and hard-to-maintain code.

## Q28: What is a Promise?
**A:** A Promise is an object representing the eventual completion or failure of an asynchronous operation, with states: pending, fulfilled, or rejected.

## Q29: How does async/await work?
**A:** async/await is syntactic sugar over Promises where async functions return a Promise and await pauses execution until the Promise settles.

## Q30: What is the EventEmitter class?
**A:** EventEmitter is a Node.js class that enables objects to emit named events and register listener functions that are called when those events occur.

## Q31: What is a Stream?
**A:** A Stream is an abstract interface for working with streaming data in Node.js, enabling processing of data piece by piece without loading it all into memory.

## Q32: What are the types of streams in Node.js?
**A:** The four types are Readable, Writable, Duplex, and Transform streams.

## Q33: What is a Readable stream?
**A:** A Readable stream is a source of data that can be read, such as fs.createReadStream or HTTP response objects.

## Q34: What is a Writable stream?
**A:** A Writable stream is a destination for data that can be written to, such as fs.createWriteStream or HTTP request objects.

## Q35: What is a Duplex stream?
**A:** A Duplex stream is both Readable and Writable, like a TCP socket, where data can flow in both directions.

## Q36: What is a Transform stream?
**A:** A Transform stream is a Duplex stream that can modify or transform data as it passes through, like zlib compression.

## Q37: What is a Buffer in Node.js?
**A:** A Buffer is a built-in class for handling raw binary data, used when dealing with streams, file system operations, or network protocols.

## Q38: How do you read a file in Node.js?
**A:** Use fs.readFile for asynchronous reading or fs.readFileSync for synchronous reading, providing the file path and encoding.

## Q39: What does the fs module provide?
**A:** The fs (file system) module provides APIs for interacting with the file system, including reading, writing, deleting, and watching files.

## Q40: What does the path module do?
**A:** The path module provides utilities for working with file and directory paths, including joining, resolving, and normalizing paths.

## Q41: What does the HTTP module do?
**A:** The http module allows creating HTTP servers and clients, handling requests and responses for building web applications and APIs.

## Q42: What is the cluster module?
**A:** The cluster module enables a Node.js application to fork multiple worker processes sharing the same server port for better CPU utilization.

## Q43: What are worker threads?
**A:** Worker threads allow running JavaScript code in parallel on separate threads within the same process, useful for CPU-intensive tasks.

## Q44: What is the difference between worker threads and child processes?
**A:** Worker threads share memory within the same process and are lighter, while child processes are separate processes with their own memory and run independently.

## Q45: How do you create a child process in Node.js?
**A:** Use child_process.spawn, child_process.fork, child_process.exec, or child_process.execFile to create and manage child processes.

## Q46: What is the process object?
**A:** The process object is a global that provides information about the current Node.js process, including argv, env, exit, and cwd.

## Q47: What are global objects in Node.js?
**A:** Global objects like process, Buffer, console, and setTimeout are available in all modules without importing, accessible globally.

## Q48: What is __dirname?
**A:** __dirname is a string in CommonJS that represents the absolute directory path of the current module file.

## Q49: What is __filename?
**A:** __filename is a string in CommonJS that represents the absolute path of the current module file.

## Q50: How do you get __dirname and __filename in ES modules?
**A:** In ES modules, use import.meta.url with fileURLToPath from the url module to derive __dirname and __filename equivalents.

## Q51: What is the REPL?
**A:** REPL (Read-Eval-Print Loop) is an interactive shell in Node.js accessed by running the node command without arguments, useful for quick experimentation.

## Q52: What is NODE_ENV?
**A:** NODE_ENV is an environment variable commonly used to indicate the current environment (development, production, test) and influence application behavior.

## Q53: How do you handle errors in Node.js?
**A:** Errors are handled using try/catch blocks for synchronous code, .catch on Promises, or error-first callbacks in asynchronous patterns.

## Q54: What is the error-first callback pattern?
**A:** The error-first callback pattern passes an error as the first argument to a callback, followed by the result data, used extensively in older Node.js APIs.

## Q55: What is process.on uncaughtException?
**A:** process.on uncaughtException catches unhandled exceptions that bubble up to the event loop, but it should only be used for cleanup, not recovery.

## Q56: What is process.on unhandledRejection?
**A:** process.on unhandledRejection catches Promise rejections that are not handled with a .catch handler.

## Q57: What are domains in Node.js?
**A:** Domains are a deprecated API that grouped I/O operations to handle errors collectively; they are no longer recommended for use.

## Q58: How do you debug a Node.js application?
**A:** Use the --inspect flag to enable the Chrome DevTools debugger, or use the built-in node inspect command for command-line debugging.

## Q59: What is the --inspect flag?
**A:** The --inspect flag allows attaching Chrome DevTools or other debuggers to a running Node.js process for debugging.

## Q60: How do you monitor Node.js performance?
**A:** Use tools like the built-in perf hooks, process.hrtime, clinic.js, or APM solutions like New Relic, Datadog, or Sentry.

## Q61: What causes memory leaks in Node.js?
**A:** Memory leaks are caused by retaining references to unused objects, such as global variables, forgotten timers, closures, or unremoved event listeners.

## Q62: How do you identify memory leaks?
**A:** Use heap snapshots in Chrome DevTools, the --inspect flag, or the built-in v8 module's heap statistics to identify leaked objects.

## Q63: How does garbage collection work in Node.js?
**A:** Node.js uses V8's garbage collector, which employs generational collection, mark-and-sweep, and incremental marking to reclaim unused memory.

## Q64: What are environment variables in Node.js?
**A:** Environment variables are key-value pairs accessible via process.env, commonly used for configuration like database URLs and API keys.

## Q65: What is top-level await?
**A:** Top-level await allows using the await keyword at the top level of ES modules without wrapping in an async function.

## Q66: What is the package.json exports field?
**A:** The exports field maps subpath imports to files, controlling which parts of a package are accessible to consumers.

## Q67: What is the middleware pattern in Express?
**A:** Middleware are functions that have access to the request and response objects and the next function, executed sequentially in the request-response cycle.

## Q68: What is REST API design in Node.js?
**A:** REST API design involves creating stateless HTTP endpoints following resource-oriented principles, using GET, POST, PUT, PATCH, and DELETE methods.

## Q69: How do you handle file uploads in Node.js?
**A:** Use middleware like multer for Express or busboy directly to parse multipart/form-data and handle file uploads.

## Q70: How do you stream data in Node.js?
**A:** Use pipe or pipeline to connect readable streams to writable streams, efficiently transferring data without buffering everything in memory.

## Q71: What are WebSockets in Node.js?
**A:** WebSockets provide full-duplex communication channels over a single TCP connection, commonly implemented with libraries like socket.io or ws.

## Q72: What are Server-Sent Events?
**A:** Server-Sent Events (SSE) allow servers to push real-time updates to clients over HTTP using a single long-lived connection.

## Q73: How do you implement JWT authentication in Node.js?
**A:** Generate a signed JSON Web Token on login using jsonwebtoken, verify it on protected routes, and attach user data to the request.

## Q74: What is session-based authentication?
**A:** Session-based authentication stores session data server-side and sends a session ID cookie to the client for subsequent request verification.

## Q75: How do you test a Node.js application?
**A:** Use testing frameworks like Jest or Mocha with assertion libraries like Chai, along with supertest for HTTP endpoint testing.

## Q76: What is Jest?
**A:** Jest is a comprehensive testing framework by Meta that includes a test runner, assertions, mocking, and code coverage out of the box.

## Q77: What is Mocha?
**A:** Mocha is a flexible test framework that provides test structure and runner capabilities, typically paired with Chai for assertions and Sinon for mocking.

## Q78: Can you use TypeScript with Node.js?
**A:** Yes, TypeScript compiles to JavaScript and can be used with Node.js via ts-node, tsx, or compiling TypeScript to JavaScript before running.

## Q79: What is Express.js?
**A:** Express.js is a minimal and flexible web application framework for Node.js that provides routing, middleware, and HTTP utility methods.

## Q80: What is Fastify?
**A:** Fastify is a high-performance Node.js web framework inspired by Express, with JSON schema validation, logging, and plugin architecture baked in.

## Q81: What is Koa?
**A:** Koa is a lightweight web framework designed by the Express team that uses async/await natively and has a middleware onion model.

## Q82: How does Express differ from Fastify?
**A:** Fastify offers higher performance, built-in JSON schema validation, and automatic logging, while Express has a larger ecosystem and simpler API.

## Q83: How does Koa differ from Express?
**A:** Koa uses async/await natively and has an onion-style middleware model, while Express uses callback-based middleware with a linear flow.

## Q84: What is package-lock.json?
**A:** package-lock.json is an auto-generated file that locks exact dependency versions to ensure reproducible installs across environments.

## Q85: What is the difference between yarn.lock and package-lock.json?
**A:** Both lock dependency versions, but yarn.lock is generated by Yarn using a deterministic algorithm, while package-lock.json is generated by npm.

## Q86: What is npx?
**A:** npx is a tool bundled with npm that executes Node packages without installing them globally, useful for running one-off commands.

## Q87: What is the purpose of .npmrc?
**A:** .npmrc is the configuration file for npm that sets registry URLs, authentication tokens, and other package management settings.

## Q88: What are npm scripts?
**A:** npm scripts are custom commands defined in package.json scripts field that can be run with npm run scriptname for automation.

## Q89: How do you secure a Node.js application?
**A:** Validate input, use Helmet for HTTP headers, implement rate limiting, sanitize data, avoid eval, and keep dependencies updated.

## Q90: What is Helmet?
**A:** Helmet is a middleware that sets various HTTP security headers to protect against common web vulnerabilities like XSS and clickjacking.

## Q91: How do you implement rate limiting in Node.js?
**A:** Use express-rate-limit middleware or a reverse proxy like Nginx to limit the number of requests from a client within a time window.

## Q92: What is PM2?
**A:** PM2 is a production process manager for Node.js that provides clustering, load balancing, monitoring, and automatic restarts on failure.

## Q93: How do you deploy a Node.js app with Docker?
**A:** Create a Dockerfile that uses a Node base image, copies package.json, runs npm install, copies source code, and uses CMD or ENTRYPOINT to start the app.

## Q94: What is the difference between process.nextTick and Promise microtasks?
**A:** process.nextTick runs before Promise microtasks in the event loop, making nextTick higher priority than resolved Promise callbacks.

## Q95: What is the difference between readFile and createReadStream?
**A:** readFile loads the entire file into memory before returning, while createReadStream reads the file in chunks for better memory efficiency.

## Q96: What is the crypto module used for?
**A:** The crypto module provides cryptographic functionality including hashing, HMAC, encryption, decryption, and random number generation.

## Q97: What is the zlib module?
**A:** The zlib module provides compression and decompression using Gzip, Deflate, and Brotli algorithms, commonly used with streams.

## Q98: What is the os module?
**A:** The os module provides operating system-related utility methods for retrieving CPU, memory, network interfaces, and platform information.

## Q99: What is the net module?
**A:** The net module provides an asynchronous network API for creating TCP servers and clients, forming the foundation for higher-level protocols.

## Q100: What is the difference between fork and spawn?
**A:** fork is for spawning a new Node.js process with IPC communication built-in, while spawn is for running any system command with a general input/output interface.
