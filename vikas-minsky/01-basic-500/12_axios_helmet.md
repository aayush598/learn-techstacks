## 12. Axios + Helmet.js (331–350)

331. What is Axios?
     A**Answer:** Axios is a promise-based HTTP client for browser and Node.js. It provides features like request/response interceptors, automatic JSON parsing, request cancellation, timeout handling, and progress tracking that the native Fetch API lacks.

332. Difference between fetch and Axios?
     A**Answer:** Axios automatically parses JSON responses, supports request cancellation natively, provides interceptors for global request/response handling, has built-in CSRF protection, and offers a cleaner API for setting headers and timeouts. Fetch is native but requires more manual handling.

333. Explain Axios interceptors.
     I**Answer:** Interceptors are functions that run before a request is sent or after a response is received. Request interceptors add auth tokens, transform data, or log requests. Response interceptors handle errors globally, refresh expired tokens, or transform response data.

334. How do you handle retries?
     R**Answer:** Retries are handled with `axios-retry` interceptor or manual retry logic. The interceptor automatically retries failed requests with configurable retry count, delay strategy (exponential backoff), and condition (which status codes to retry).

335. Explain request cancellation.
     R**Answer:** Requests are cancelled using `AbortController` (or Axios's built-in `CancelToken`). Create a controller, pass its signal to the request config, and call `controller.abort()` to cancel. Useful for aborting stale requests when components unmount.

336. What are Axios instances?
     A**Answer:** Axios instances are custom configurations created with `axios.create()`. They have their own base URL, headers, interceptors, and defaults — enabling different API configurations for different services without global mutation.

337. Explain token refresh flows.
     T**Answer:** Token refresh uses a response interceptor that detects 401 errors, refreshes the token using a refresh token, retries the original request with the new token, and queues concurrent failed requests to avoid parallel refresh calls.

338. How do you handle errors globally?
     G**Answer:** Global error handling uses a response interceptor that catches errors, normalizes them, and either shows notifications, redirects to login, or logs them. The interceptor distinguishes between network errors, timeout errors, and server errors.

339. Explain timeout handling.
     T**Answer:** Timeouts are set via `timeout` in the request config (milliseconds). When exceeded, Axios throws a timeout error. Interceptors catch these errors for retries or user notification. Different endpoints may need different timeout values.

340. What are request transformers?
     R**Answer:** Request transformers modify request data before sending, via the `transformRequest` config option. They can serialize data, add wrappers, encrypt payloads, or format dates. Similarly, `transformResponse` transforms response data after receiving.

341. What is Helmet.js?
     H**Answer:** Helmet.js is an Express middleware that secures apps by setting various HTTP security headers. It helps prevent common web vulnerabilities by configuring headers like Content-Security-Policy, X-Content-Type-Options, and Strict-Transport-Security.

342. Why are security headers important?
     S**Answer:** Security headers instruct browsers to enforce security policies that prevent attacks like XSS, clickjacking, MIME-type sniffing, and protocol downgrade. They add defense layers that protect users even if application code has vulnerabilities.

343. Explain CSP headers.
     C**Answer:** CSP (Content-Security-Policy) restricts which resources (scripts, styles, images, fonts) can be loaded and from which origins. It prevents XSS by blocking inline scripts and unauthorized external resources, significantly reducing attack surface.

344. What is clickjacking?
     C**Answer:** Clickjacking tricks users into clicking hidden UI elements by overlaying transparent iframes on legitimate pages. Helmet's `X-Frame-Options: DENY` or `frame-ancestors` CSP directive prevents your site from being embedded in iframes.

345. Explain XSS protection.
     X**Answer:** XSS (Cross-Site Scripting) occurs when attackers inject malicious scripts into web pages. Helmet sets `X-XSS-Protection` and CSP headers to block reflected XSS, but proper output encoding, input validation, and CSP are the primary defenses.

346. What is HSTS?
     H**Answer:** HSTS (HTTP Strict Transport Security) forces browsers to always use HTTPS connections to your site, preventing protocol downgrade attacks. It's set via `Strict-Transport-Security` header with a `max-age` directive and optional `includeSubDomains`.

347. Explain CORS security.
     C**Answer:** CORS security controls which origins can access your resources. Restrict `Access-Control-Allow-Origin` to specific domains, limit allowed methods and headers, avoid wildcard credentials, and validate the Origin header server-side.

348. What are nonce-based CSPs?
     N**Answer:** Nonce-based CSPs use cryptographically random values (`nonce`) generated per request to allow specific inline scripts. Scripts with matching `nonce` attribute execute while blocking all other inline scripts, balancing security with legitimate inline code.

349. Explain secure cookie settings.
     S**Answer:** Secure cookies use `HttpOnly` (inaccessible to JavaScript, prevents XSS token theft), `Secure` (only over HTTPS), `SameSite` (Strict/Lax/None controls cross-site requests), and `__Host-` prefix for path/domain restrictions.

350. How do you secure Express/Nest apps?
     S**Answer:** Secure by applying Helmet middleware, CORS configuration, rate limiting, input validation, authentication (JWT with httpOnly cookies), CSRF protection, HTTPS enforcement, encrypted environment variables, SQL injection prevention (parameterized queries), and security audit tools.
