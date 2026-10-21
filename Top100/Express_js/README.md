# Express.js Interview Questions and Answers

## Q1: What is Express.js?
**A:** Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for building web and mobile applications. It is designed for building single-page, multi-page, and hybrid web applications and APIs. It is the de facto standard server framework for Node.js.

## Q2: What are the core features of Express.js?
**A:** Core features include: middleware system for request/response handling, routing (URL-based and HTTP method-based), template engine integration, static file serving, error handling, sub-app mounting (express.Router), content negotiation, and environment-based configuration.

## Q3: How do you create a basic Express.js server?
**A:** By importing express, calling `express()` to create an app instance, defining routes with `app.get()`, and calling `app.listen()` to start the server on a specified port.

## Q4: What is middleware in Express.js?
**A:** Middleware are functions that have access to the request object (`req`), the response object (`res`), and the `next` function in the application's request-response cycle. They can execute code, modify req/res, end the request-response cycle, or call the next middleware.

## Q5: What are the different types of middleware in Express.js?
**A:** Application-level middleware (bound to `app` with `app.use()`), Router-level middleware (bound to `express.Router()`), Error-handling middleware (four arguments: err, req, res, next), Built-in middleware (express.static, express.json, express.urlencoded), Third-party middleware (like morgan, cors, helmet), and Custom middleware.

## Q6: How do you handle errors in Express.js?
**A:** Error-handling middleware is defined with four parameters: `(err, req, res, next)`. Errors from synchronous code are caught automatically; async errors need explicit forwarding via `next(err)` or using a wrapper like `express-async-errors`.

## Q7: What is the difference between `app.use()` and `app.get()`?
**A:** `app.use()` mounts middleware for all HTTP methods and matches any path starting with the specified path prefix. `app.get()` only matches GET requests to an exact path (by default). `app.use()` is for middleware, `app.get()` is for route definitions.

## Q8: How does routing work in Express.js?
**A:** Routing maps HTTP methods (GET, POST, PUT, DELETE, etc.) and URL patterns to handler functions. Routes are defined using methods like `app.get('/path', handler)`. Route parameters (`:param`), query strings, and regular expressions are supported.

## Q9: What are route parameters in Express.js?
**A:** Route parameters are named URL segments used to capture values at specific positions in the URL. Defined with a colon prefix (`:userId`), accessed via `req.params.userId`. They can be made optional with a `?` suffix and can have regex constraints.

## Q10: What is `express.Router()`?
**A:** `express.Router()` creates modular, mountable route handlers. It acts as a mini-application capable only of performing middleware and routing functions. It allows grouping related routes and mounting them at a common path prefix.

## Q11: How do you serve static files in Express.js?
**A:** Using the built-in `express.static` middleware. Example: `app.use(express.static('public'))` serves files from the 'public' directory. Multiple directories can be used, and a virtual path prefix can be added.

## Q12: What is `res.json()` and how is it different from `res.send()`?
**A:** `res.json()` sends a JSON response with the correct Content-Type header (`application/json`) and automatically converts objects/arrays to JSON. `res.send()` is more general — it can send buffers, strings, objects, or JSON, and auto-detects the content type.

## Q13: How do you parse request bodies in Express.js?
**A:** Using built-in middleware: `express.json()` parses JSON bodies, `express.urlencoded({ extended: true })` parses URL-encoded bodies. For file uploads, third-party middleware like `multer` is used.

## Q14: What is `next()` and why is it important?
**A:** `next()` is a callback function passed to middleware that passes control to the next middleware function in the stack. Without calling `next()`, the request will hang and never complete. It can be called with `'route'` to skip to the next route, or with an error to jump to error-handling middleware.

## Q15: How does CORS work in Express.js?
**A:** CORS (Cross-Origin Resource Sharing) is handled using the `cors` npm package. `cors()` as middleware enables all CORS requests; options like `origin`, `methods`, and `credentials` configure specific policies.

## Q16: What is the purpose of `app.set()` and `app.get()` (the config version)?
**A:** `app.set('key', value)` sets application-level settings (like view engine, port, trust proxy). `app.get('key')` retrieves those settings. These are not to be confused with route-handling `app.get()`.

## Q17: How do you handle 404 errors in Express.js?
**A:** By placing a catch-all middleware at the end of the middleware stack that creates a 404 error using `app.use((req, res) => res.status(404).send('Not Found'))` or forwarding to an error handler.

## Q18: What is template engine integration in Express.js?
**A:** Express can integrate with template engines like Pug, EJS, Handlebars, and Mustache. Set the view engine with `app.set('view engine', 'pug')` and use `res.render('templateName', data)` to render templates.

## Q19: What are query parameters and how do you access them?
**A:** Query parameters appear after `?` in a URL (e.g., `/search?q=hello&page=2`). They are accessed via `req.query` as an object: `req.query.q`, `req.query.page`.

## Q20: What is `res.status()` used for?
**A:** `res.status(code)` sets the HTTP response status code. It returns the response object for chaining, e.g., `res.status(404).json({ error: 'Not found' })`.

## Q21: How does Express.js handle asynchronous code?
**A:** In Express 4, errors from async middleware must be caught and forwarded via `next(err)`. Express 5 (experimental/alpha) natively handles rejected promises from async route handlers. Patterns like `express-async-errors` or custom wrappers are used in Express 4.

## Q22: What is the difference between `req.params` and `req.query`?
**A:** `req.params` contains route parameters extracted from the URL path (e.g., `/users/:id` gives `req.params.id`). `req.query` contains parsed query string parameters from the URL after `?`. Both are objects.

## Q23: What is helmet and why use it?
**A:** Helmet is a collection of middleware that sets various HTTP security headers to protect against common web vulnerabilities like XSS, clickjacking, MIME sniffing, etc. It's a security best practice for Express apps.

## Q24: How do you implement logging in Express.js?
**A:** Using the `morgan` middleware library. `app.use(morgan('combined'))` logs requests in Apache combined format. Custom formats and logging to files are also supported.

## Q25: What is rate limiting and how is it implemented?
**A:** Rate limiting restricts the number of requests a client can make in a time window. Implemented via `express-rate-limit` package: `const limiter = rateLimit({ windowMs: 15*60*1000, max: 100 })`.

## Q26: How do you create a RESTful API with Express.js?
**A:** By defining routes that correspond to CRUD operations: `GET /resource` (list), `GET /resource/:id` (read), `POST /resource` (create), `PUT/PATCH /resource/:id` (update), `DELETE /resource/:id` (delete), with proper status codes and JSON responses.

## Q27: What is `app.all()` used for?
**A:** `app.all('/path', handler)` matches a path for all HTTP methods (GET, POST, PUT, DELETE, etc.). It's useful for loading middleware or logic that applies regardless of the HTTP method.

## Q28: How do you structure a large Express.js application?
**A:** Common patterns include: separating routes into modules using `express.Router()`, organizing by feature/module rather than by type, using a dedicated controllers layer, services layer, middleware folder, config files, and separate utility functions.

## Q29: What is the difference between `res.redirect()` and `res.render()`?
**A:** `res.redirect()` sends a 302 (or other) redirect response, telling the client to navigate to a different URL. `res.render()` processes a template file with provided data and sends the rendered HTML as the response.

## Q30: How do you handle file uploads in Express.js?
**A:** Using the `multer` middleware. Configure multer with storage options (disk or memory), define file size limits, and access uploaded files via `req.file` (single) or `req.files` (multiple).

## Q31: What is `cookie-parser` and how does it work?
**A:** `cookie-parser` parses the `Cookie` header in incoming requests and populates `req.cookies` with an object keyed by cookie names. It also supports signed cookies and secret-based verification.

## Q32: How do you implement authentication in Express.js?
**A:** Common approaches: session-based auth with `express-session`, JWT-based auth with `jsonwebtoken`, or using Passport.js middleware which supports many strategies (local, OAuth, SAML, etc.).

## Q33: What is `express-session`?
**A:** `express-session` is middleware that creates session objects stored server-side (in memory, database, or Redis). It sets a cookie with a session ID on the client and populates `req.session` on subsequent requests.

## Q34: How do you handle environment variables in Express.js?
**A:** Using the `dotenv` package. Create a `.env` file with key-value pairs, call `require('dotenv').config()` early in the app, and access variables via `process.env.VAR_NAME`.

## Q35: What is `app.locals`?
**A:** `app.locals` is an object that stores application-level variables that are accessible in all templates rendered by the application. It persists throughout the application's lifetime.

## Q36: What is `res.locals`?
**A:** `res.locals` is an object that contains response-local variables scoped to the current request. It's useful for passing data through middleware to route handlers and templates.

## Q37: How does Express.js compare to Koa.js?
**A:** Express is more mature with a larger ecosystem but uses callback-based middleware. Koa was built by the same team but uses async/await natively, has a lighter core, and uses a context object instead of separate req/res objects.

## Q38: What are the advantages of using Express.js?
**A:** Minimal and unopinionated, large ecosystem of middleware, excellent performance, easy to learn, extensive community support, flexible routing, and seamless Node.js integration.

## Q39: How do you implement HTTPS in Express.js?
**A:** By using Node's `https` module instead of `http`, providing SSL certificate and key files: `https.createServer({ key, cert }, app).listen(443)`.

## Q40: What is compression middleware and when to use it?
**A:** `compression` middleware compresses response bodies using gzip/deflate. Use it for production apps to reduce bandwidth, but avoid for pre-compressed assets or when behind a reverse proxy that handles compression.

## Q41: How do you create a health check endpoint?
**A:** Define a GET route (e.g., `/health` or `/api/health`) that returns a 200 status with health status information like server uptime, database connectivity, and memory usage.

## Q42: What is the `req.ip` property?
**A:** `req.ip` contains the IP address of the client. With `app.set('trust proxy', true)`, it uses the `X-Forwarded-For` header to get the original client IP when behind a proxy.

## Q43: How do you validate request data in Express.js?
**A:** Using libraries like `joi`, `express-validator`, or `zod`. Define validation schemas for request bodies, query parameters, and route parameters, and run validation as middleware.

## Q44: What is `express-validator`?
**A:** A set of express.js middleware that wraps `validator.js` for validating and sanitizing request data. Provides `body()`, `param()`, `query()` functions and a `validationResult` function to check for errors.

## Q45: How do you handle database connections in Express.js?
**A:** Typically by creating a connection pool (for SQL databases) or connecting once at startup (for MongoDB), then making the connection accessible via middleware, modules, or dependency injection.

## Q46: What is the purpose of `app.disable()` and `app.enable()`?
**A:** These toggle boolean application settings. `app.enable('trust proxy')` is equivalent to `app.set('trust proxy', true)`. `app.disable()` sets to false.

## Q47: How do you mount sub-applications in Express.js?
**A:** Using `app.use('/prefix', subApp)` where `subApp` is another Express application instance. This allows composing applications and splitting large apps into manageable pieces.

## Q48: What are chainable route handlers?
**A:** Express allows chaining HTTP method handlers on a single path using `app.route('/path').get(handler).post(handler).put(handler)`, reducing redundancy and improving organization.

## Q49: How do you set response headers in Express.js?
**A:** Using `res.set('Header-Name', 'value')` or `res.header('Header-Name', 'value')`. Multiple headers can be set with `res.set({ 'Header1': 'val1', 'Header2': 'val2' })`.

## Q50: What is `res.append()`?
**A:** `res.append()` appends a value to an existing response header or creates it if it doesn't exist. Useful for headers like `Set-Cookie` or `Link` that can appear multiple times.

## Q51: How does content negotiation work in Express.js?
**A:** Express uses the `Accept` request header to determine the best response format. `res.format()` can define different responses for different content types (JSON, HTML, XML, etc.).

## Q52: What is `req.accepts()`?
**A:** `req.accepts(types)` checks if the specified content types are acceptable based on the request's Accept header. Returns the best matching type or false if none match.

## Q53: How do you handle file downloads in Express.js?
**A:** `res.download('/path/to/file')` prompts the browser to download the file. `res.sendFile('/path/to/file')` sends the file for inline display. Both handle appropriate headers automatically.

## Q54: What is `res.attachment()`?
**A:** `res.attachment('/path/to/file')` sets the Content-Disposition header to "attachment", optionally setting the Content-Type based on the filename extension. The file is not sent; use with `res.sendFile()` or `res.download()`.

## Q55: How do you set and get cookies in Express.js?
**A:** Set cookies with `res.cookie('name', 'value', options)` with options like maxAge, httpOnly, secure, signed. Read cookies with `req.cookies` (if using cookie-parser). Clear with `res.clearCookie('name')`.

## Q56: What are signed cookies?
**A:** Signed cookies are cookies whose value is signed with a secret using HMAC. They prevent tampering on the client side. Configured with `cookieParser('secret')`, written with `res.cookie('name', 'val', { signed: true })`, read from `req.signedCookies`.

## Q57: What is the `trust proxy` setting?
**A:** `app.set('trust proxy', 1)` (or true) indicates the app is behind a reverse proxy. It changes the behavior of `req.ip`, `req.protocol`, `req.hostname`, and `req.secure` to use proxy headers (X-Forwarded-*).

## Q58: How do you implement pagination in an Express API?
**A:** By accepting `page` and `limit` query parameters, calculating offset (`(page - 1) * limit`), querying the database with LIMIT and OFFSET, and returning pagination metadata (total, page, totalPages) alongside the data.

## Q59: What is a route prefix and how do you set it?
**A:** A route prefix is a common path segment prepended to all routes in a router. Set it when mounting the router: `app.use('/api/users', userRouter)` makes all routes in `userRouter` available under `/api/users`.

## Q60: How do you handle CORS preflight requests?
**A:** CORS preflight (OPTIONS request) is automatically handled by the `cors` middleware. For custom configurations, set `optionsSuccessStatus: 204` and ensure the OPTIONS method is not blocked by authentication middleware.

## Q61: What is rate limiting bypass and how to prevent it?
**A:** Rate limiting can be bypassed by rotating IPs (via proxies) or by exploiting X-Forwarded-For headers. Prevent by using trust proxy settings, rate limiting by user ID/token instead of IP, or using API keys with quotas.

## Q62: How do you implement WebSocket support in Express.js?
**A:** Using `socket.io` or `ws` library alongside the Express server. The HTTP server is created first and passed to the WebSocket library: `const server = http.createServer(app); const io = new Server(server);`.

## Q63: What is the `case sensitive routing` setting?
**A:** `app.set('case sensitive routing', true)` enables case-sensitive route matching. With the default (undefined/false), `/Users` and `/users` are treated the same. When enabled, they are distinct.

## Q64: What is the `strict routing` setting?
**A:** `app.set('strict routing', true)` treats trailing slashes as significant. With strict routing, `/user` and `/user/` are different routes. Default is false (trailing slash is optional/ignored).

## Q65: How do you implement server-sent events (SSE) in Express.js?
**A:** Set headers `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive`. Write data with `res.write(`data: ${JSON.stringify(data)}\n\n`)`. Handle `req.on('close')` to clean up.

## Q66: What is `req.range()`?
**A:** `req.range(size)` parses the `Range` header and returns an array of ranges for partial content requests. Used for implementing video/audio streaming and resumable downloads.

## Q67: How do you handle concurrent requests in Express.js?
**A:** Express/Node.js handles concurrency via its event loop and asynchronous I/O. For CPU-bound tasks, use worker threads or child processes. For database, use connection pooling. For rate limiting, use appropriate middleware.

## Q68: What is the `res.vary()` method?
**A:** `res.vary('header-name')` sets the `Vary` response header, indicating that the response varies based on the specified request header. Important for proper caching behavior with content negotiation.

## Q69: How do you implement CSRF protection in Express.js?
**A:** Using the `csurf` package (though it's deprecated, alternatives exist). The general approach: generate a CSRF token, include it in forms/ajax requests, and validate it server-side against the session.

## Q70: What is the `res.type()` method?
**A:** `res.type('extension')` sets the Content-Type header based on the MIME type associated with the file extension. For example, `res.type('json')` sets `application/json`.

## Q71: How do you test Express.js applications?
**A:** Using testing frameworks like Jest or Mocha with Supertest (HTTP assertion library). Supertest allows programmatically making requests to the Express app and asserting on responses without needing a running server.

## Q72: What is `req.subdomains`?
**A:** `req.subdomains` is an array of subdomains in the domain name of the request. For `api.example.com`, `req.subdomains` would be `['api']`. The `trust proxy` setting affects this value.

## Q73: How do you implement API versioning in Express.js?
**A:** Common strategies: URL-based versioning (`/v1/users`, `/v2/users`), header-based versioning (`Accept: application/vnd.api.v1+json`), or query parameter versioning. URL-based is most common with Express routers.

## Q74: What is `app.engine()` used for?
**A:** `app.engine('ext', callback)` registers a template engine for rendering files with the given extension. This is used when the template engine doesn't integrate out-of-the-box with Express.

## Q75: How does error handling middleware differ from regular middleware?
**A:** Error-handling middleware has four parameters `(err, req, res, next)` instead of three `(req, res, next)`. Express identifies it by the number of parameters. It only runs when an error is passed to `next()`.

## Q76: What happens if you don't handle an error in Express.js?
**A:** If no error-handling middleware is defined and an error occurs, Express returns a default HTML error response with the status code and a basic stack trace (in development mode). In production, the error may result in a 500 response with minimal info.

## Q77: How do you properly handle unhandled promise rejections in Express.js?
**A:** Register a global process handler: `process.on('unhandledRejection', (reason, promise) => { /* log and exit gracefully */ })`. Or use `express-async-errors` to automatically catch async errors and forward them to error middleware.

## Q78: What is the `res.format()` method?
**A:** `res.format(object)` performs content negotiation using the Accept header. It maps content types to response handlers: `res.format({ 'text/html': () => res.send('html'), 'application/json': () => res.json(data) })`.

## Q79: How do you limit request body size in Express.js?
**A:** Pass options to `express.json({ limit: '10kb' })` or `express.urlencoded({ limit: '10kb' })`. For file uploads, set limits in multer: `multer({ limits: { fileSize: 5 * 1024 * 1024 } })`.

## Q80: What is a reverse proxy and how does it relate to Express.js?
**A:** A reverse proxy (like Nginx, HAProxy) sits in front of the Express server and handles SSL termination, load balancing, caching, and static file serving. Express apps are typically deployed behind a reverse proxy in production.

## Q81: How do you optimize Express.js for production?
**A:** Use compression, set NODE_ENV=production (improves caching and error output), enable trust proxy, use a reverse proxy for static files, implement caching (Redis), use cluster mode or PM2, enable HTTP/2, and add monitoring/logging.

## Q82: What is the `req.acceptsLanguages()` method?
**A:** `req.acceptsLanguages()` checks which languages are acceptable based on the `Accept-Language` header. Returns the best matching language or false.

## Q83: How do you implement a proxy in Express.js?
**A:** Using `http-proxy-middleware`. It forwards requests to another server: `app.use('/api', createProxyMiddleware({ target: 'http://localhost:3001', changeOrigin: true }))`.

## Q84: What is the difference between `app.use` and `router.use`?
**A:** `app.use` applies middleware to the entire application. `router.use` applies middleware only to routes handled by that specific router instance. Both can take an optional path prefix.

## Q85: How do you handle circular redirects?
**A:** Detect by counting redirects or checking against a maximum redirect limit. Use 301/302 for proper semantics. Implement redirect middleware that tracks redirect count in session or request.

## Q86: What is `req.stale` and `req.fresh`?
**A:** These properties check if the response is "fresh" or "stale" based on the request's `If-None-Match` and `If-Modified-Since` headers. Used for HTTP caching and conditional requests.

## Q87: How do you implement HTTP caching in Express.js?
**A:** Set caching headers like `Cache-Control`, `ETag`, and `Last-Modified` on responses. Express's `res.sendFile()` and `res.json()` can auto-generate ETags. Use middleware like `apicache` or `express-cache-controller`.

## Q88: What is `app.path()`?
**A:** `app.path()` returns the canonical path of the Express application, which is useful when mounting sub-applications. For the main app, it returns `''`. For sub-apps mounted at `/admin`, it returns `/admin`.

## Q89: How do you get the full URL of a request in Express.js?
**A:** Use `req.protocol + '://' + req.get('host') + req.originalUrl`. Alternatively, many libraries provide helpers. The `trust proxy` setting affects `req.protocol`.

## Q90: What is the `req.route` object?
**A:** `req.route` contains information about the currently matched route, including the path pattern, HTTP methods, and any regular expression or parameter details. It's populated after a successful route match.

## Q91: How do you implement database transactions in Express.js?
**A:** Transactions depend on the database driver/ORM. For example, with Sequelize: `sequelize.transaction(async (t) => { await Model.create(data, { transaction: t }) })`. For Knex: `knex.transaction(trx => { ... })`.

## Q92: What are some common security best practices for Express.js?
**A:** Use Helmet for headers, validate/sanitize input, use parameterized queries (prevent SQL injection), implement rate limiting, use HTTPS, set secure/httpOnly cookies, avoid stack traces in production, keep dependencies updated, and use CORS restrictively.

## Q93: How do you implement logging with different levels in Express.js?
**A:** Using libraries like `winston` or `pino`. Configure transports (console, file, external service) and levels (error, warn, info, debug). Create a middleware that logs request details with appropriate level.

## Q94: What is `res.links()`?
**A:** `res.links(links)` sets the `Link` response header, which is useful for pagination (providing `first`, `prev`, `next`, `last` links) and other relational link data in REST APIs.

## Q95: How do you handle graceful shutdown in Express.js?
**A:** Listen for `SIGTERM` and `SIGINT` signals, stop accepting new requests, close database connections, release resources, and call `server.close()` to allow in-flight requests to complete before exiting.

## Q96: What is the `query parser` setting in Express?
**A:** `app.set('query parser', 'simple' | 'extended' | function)` controls how query strings are parsed. 'simple' uses Node's built-in querystring module. 'extended' (default) uses the qs library, which supports nested objects and arrays.

## Q97: How do you implement a request timeout in Express.js?
**A:** Using the `connect-timeout` middleware or setting a timeout on the `http.Server`: `server.timeout = 30000` (30 seconds). Custom middleware can also track and abort slow requests.

## Q98: What is `res.cookie()` options object?
**A:** Options include: `domain` (cookie domain), `expires` (expiration date), `httpOnly` (not accessible to JS), `maxAge` (milliseconds from now), `path` (URL path), `secure` (HTTPS only), `signed` (sign the cookie), `sameSite` (SameSite policy).

## Q99: How do you debug an Express.js application?
**A:** Set the `DEBUG` environment variable: `DEBUG=express:*` for Express internals. Use `node --inspect` for Chrome DevTools, `console.log` strategically, or dedicated debugging middleware. For production, use structured logging with correlation IDs.

## Q100: What's new in Express 5?
**A:** Express 5 (alpha) introduces native async/await error handling (rejected promises automatically go to error handler), improved routing with path-to-regexp v8 (changes route parameter syntax), `req.query` always returns an object, `res.json()` no longer supports JSONP callback, removed deprecated methods (`app.del()` replaced by `app.delete()`), and `app.param()` changes for async support.
