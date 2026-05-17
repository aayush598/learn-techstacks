## 50. Axios + Helmet.js Expert Topics (1331–1350)

1331. How do request interceptors chain execution?

   **Answer:** Axios request interceptors execute in reverse order of registration (LIFO) while response interceptors execute in registration order (FIFO). Each interceptor receives the config/response and can modify it, retry the request, or reject.

1332. Explain token refresh race conditions.

   **Answer:** Race conditions occur when multiple requests fail simultaneously due to expired tokens, each triggering a refresh attempt. Axios interceptors mitigate this with a queue that holds failed requests, performs a single refresh, and retries all queued requests.

1333. What are retry storm risks?

   **Answer:** Retry storms happen when many clients retry failed requests simultaneously, overwhelming the server. Mitigations include exponential backoff with jitter, circuit breakers, and maximum retry limits in axios-retry.

1334. Explain HTTP retry idempotency.

   **Answer:** Only idempotent methods (GET, PUT, DELETE, HEAD, OPTIONS, TRACE) should be automatically retried. POST and PATCH require manual idempotency keys to prevent duplicate side effects.

1335. How do secure cookies mitigate attacks?

   **Answer:** Secure cookies set the `Secure` flag (HTTPS-only), `HttpOnly` (inaccessible to JavaScript), `SameSite` (cross-origin restriction), and `__Host-` prefix for path binding, collectively preventing XSS, CSRF, and session theft.

1336. Explain session fixation attacks.

   **Answer:** Session fixation forces a user to use an attacker-known session ID before login. Mitigations include regenerating session IDs after authentication, enforcing short session TTLs, and using secure random session IDs.

1337. What are CSP bypass techniques?

   **Answer:** CSP bypass techniques include JSONP endpoints returning attacker-controlled callbacks, script gadgets in trusted libraries, and dangling markup injection. Nonces, strict-dynamic, and hash-based CSP mitigate these.

1338. Explain browser sandbox isolation.

   **Answer:** Browser sandbox isolation restricts what resources a page can access through iframe's `sandbox` attribute, limiting form submission, script execution, popups, and navigation. Enterprise apps use this for embedding untrusted content.

1339. How does strict transport security work?

   **Answer:** HSTS (`Strict-Transport-Security` header) forces browsers to use HTTPS for a specified `max-age`, preventing protocol downgrade attacks. `includeSubDomains` extends coverage and `preload` lists enable browser-level enforcement.

1340. Explain API gateway TLS termination.

   **Answer:** API gateways terminate TLS by decrypting incoming HTTPS traffic, forwarding plain HTTP to internal services. This offloads certificate management and encryption overhead, but internal traffic must be secured within the trusted network.

1341. What are cross-origin isolation headers?

   **Answer:** `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` enable high-performance APIs like SharedArrayBuffer by isolating the browsing context group from cross-origin pages.

1342. Explain secure iframe embedding.

   **Answer:** Secure iframe embedding uses sandbox attributes, `allow` permissions (microphone, camera), and `credentialless` for COEP. The embedding page should verify the iframe's origin via `postMessage` and enforce HTTPS.

1343. How do browser permissions policies work?

   **Answer:** `Permissions-Policy` headers control which browser APIs (geolocation, camera, notifications) a page and its iframes can use. This limits the attack surface of compromised pages by disabling unused powerful features.

1344. Explain origin-based security models.

   **Answer:** The Same-Origin Policy restricts how documents/scripts from one origin can interact with resources from another. Exceptions include CORS (controlled cross-origin access), CORP (cross-origin resource policy), and postMessage.

1345. What are browser trust boundaries?

   **Answer:** Trust boundaries separate privileged browser contexts (extension pages, devtools) from web content. Cross-origin iframes, service workers, and shared workers sit at different trust levels, and data crossing these boundaries needs validation.

1346. Explain layered API defense mechanisms.

   **Answer:** Layered defense includes rate limiting at the gateway, input validation in middleware, auth tokens in interceptors, output encoding in responses, and audit logging at every layer. Each layer catches failures from the layer before.

1347. How do anti-bot protections work?

   **Answer:** Anti-bot protections use CAPTCHA, rate limiting, behavior analysis (mouse movement, timing), device fingerprinting, and IP reputation scoring. Server-side validation of critical endpoints supplements client-side challenges.

1348. Explain DDoS mitigation strategies.

   **Answer:** DDoS mitigation uses edge-level traffic filtering (Cloudflare, AWS Shield), rate limiting, connection throttling, and auto-scaling infrastructure. At the application layer, caching absorbs static asset floods while computed endpoints collapse under load.

1349. What are advanced API hardening techniques?

   **Answer:** Advanced hardening includes request signing (HMAC), payload encryption at the application layer, API key rotation with grace periods, anomaly detection on traffic patterns, and penetration testing with automated fuzzing.

1350. How do enterprise systems enforce security policies?

   **Answer:** Enterprise systems enforce security through centralized policy engines that dictate TLS versions, cipher suites, token lifetimes, and rate limits. These policies are deployed as code (OPA, Kyverno) and validated in CI/CD pipelines.
