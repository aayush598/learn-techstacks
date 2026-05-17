## 31. Axios + Helmet.js Advanced (831–850)

831. How do Axios adapters work?
   Axios adapters are functions that handle the actual request execution. The default adapter uses `XMLHttpRequest` in browsers and `http`/`https` in Node.js. Custom adapters can mock requests or use fetch APIs.

832. Explain request queueing.
   Request queueing enqueues requests when the connection pool is saturated. Axios doesn't queue natively; implement with an interceptor that uses a semaphore or use libraries like `axios-queue` for controlled concurrency.

833. What are interceptor memory leaks?
   Interceptors hold references to closures, preventing garbage collection. Leaks occur when interceptors are added repeatedly without being ejected via `axios.interceptors.request.eject(id)`.

834. Explain duplicate request prevention.
   Prevent duplicates by tracking in-flight request keys (e.g., `method + url + params`). Before sending, check if an identical request is pending and return its promise instead of creating a new one.

835. How do exponential backoffs work?
   Exponential backoff retries failed requests with increasing delays (e.g., 1s, 2s, 4s, 8s). Axios-retry or custom interceptors implement this with jitter (random offset) to prevent thundering herd.

836. Explain HTTP keep-alive.
   Keep-alive (`Connection: keep-alive`) reuses TCP connections for multiple requests, avoiding TCP handshake overhead. In Axios Node.js, set `http.Agent` with `keepAlive: true` in the config.

837. What are connection pools?
   Connection pools manage a set of reusable TCP connections per host. Axios uses `http.Agent` with `maxSockets` to limit concurrent connections, preventing resource exhaustion.

838. Explain CSRF attack prevention.
   CSRF attacks trick users into submitting malicious requests. Helmet's `crossOriginRequestCounter` or using SameSite cookies, CSRF tokens, and custom headers (e.g., `X-CSRF-Token`) prevent cross-origin requests.

839. What are SameSite cookies?
   SameSite cookies (`Strict`, `Lax`, `None`) control when cookies are sent cross-origin. `Strict` blocks all cross-site requests, `Lax` allows top-level GET, and `None` requires Secure context.

840. Explain CSP reporting.
   Content Security Policy reporting sends violation reports to a specified endpoint via `report-uri` or `report-to` directives. Reports detail the violated directive and source, enabling policy refinement.

841. How do nonce headers improve security?
   Nonces are one-time-use random strings added to `<script>` and `<style>` tags. CSP with `'nonce-{random}'` allows specific inline scripts while blocking all others, defeating XSS injection.

842. Explain subresource integrity.
   SRI (`integrity="sha256-..."`) ensures fetched resources (CDN scripts/styles) haven't been tampered with. The browser computes the resource hash and blocks it if it doesn't match the declared integrity value.

843. What are MIME sniffing attacks?
   MIME sniffing allows browsers to interpret resources as different types than declared, enabling script injection via image uploads. Helmet sets `X-Content-Type-Options: nosniff` to disable sniffing.

844. Explain Referrer-Policy headers.
   Referrer-Policy controls how much referrer information is sent in requests. `strict-origin-when-cross-origin` (default) sends full URL for same-origin, origin-only for cross-origin, improving privacy.

845. What are browser isolation headers?
   Isolation headers include `Cross-Origin-Embedder-Policy: require-corp`, `Cross-Origin-Opener-Policy: same-origin`, and `Cross-Origin-Resource-Policy`. They enable high-security features like `SharedArrayBuffer`.

846. Explain secure session management.
   Secure sessions use HTTP-only, secure, SameSite cookies with signed/encrypted values. Sessions expire after inactivity, regenerate IDs on privilege escalation, and store minimal data with server-side validation.

847. How does HTTPS termination work?
   HTTPS termination decrypts TLS traffic at a load balancer/reverse proxy, forwarding plain HTTP to internal services. This offloads encryption overhead from application servers and centralizes certificate management.

848. Explain TLS handshake basics.
   The TLS handshake begins with ClientHello and ServerHello exchanging cipher suites. Certificates authenticate the server, key exchange establishes a shared secret, and encrypted data flows after the Finished message.

849. What are common API attack vectors?
   Common vectors include injection (SQL, NoSQL, command), authentication bypass, excessive data exposure, mass assignment, rate limit abuse, path traversal, SSRF, and deserialization attacks.

850. Explain defense-in-depth architecture.
   Defense-in-depth layers security at every level: WAF (web app firewall), TLS termination, API gateway auth, request validation (Zod), output encoding, CSP headers, rate limiting, audit logging, and least-privilege DB access.
