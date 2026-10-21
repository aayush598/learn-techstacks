# Helmet.js Interview Questions and Answers

## Q1: What is Helmet.js?
**A:** Helmet.js is a middleware library for Express.js (and other Node.js frameworks) that helps secure HTTP headers by setting various security-related headers automatically.

## Q2: How do you install and use Helmet?
**A:** Install with `npm install helmet` and use with `app.use(helmet())` in an Express app to set secure HTTP headers.

## Q3: What version of Helmet is current as of 2025?
**A:** Helmet v7+ is the current major version, which simplified the API by removing deprecated options and making all middleware enabled by default.

## Q4: What security headers does Helmet set?
**A:** Helmet sets headers including Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security, X-XSS-Protection, Referrer-Policy, and Permissions-Policy.

## Q5: What is the Content-Security-Policy (CSP) header?
**A:** CSP is a security header that helps prevent cross-site scripting (XSS) and data injection attacks by controlling which resources the browser is allowed to load.

## Q6: How do you configure CSP with Helmet?
**A:** Pass a `contentSecurityPolicy` option object to `helmet()` with directives like `defaultSrc`, `scriptSrc`, and `styleSrc` to define allowed resource sources.

## Q7: What is the `default-src` CSP directive?
**A:** `default-src` serves as the fallback for all other CSP directives when they are not explicitly defined, setting the default policy for resource loading.

## Q8: What is the `script-src` CSP directive?
**A:** `script-src` controls which sources are allowed to execute JavaScript on the page, helping prevent XSS attacks.

## Q9: What is the `style-src` CSP directive?
**A:** `style-src` specifies allowed sources for stylesheets and inline styles on the page.

## Q10: What is the `img-src` CSP directive?
**A:** `img-src` defines which sources are permitted to load images on the page.

## Q11: What is the `connect-src` CSP directive?
**A:** `connect-src` restricts which URLs the page can connect to via fetch, XMLHttpRequest, WebSockets, and EventSource.

## Q12: What is the `font-src` CSP directive?
**A:** `font-src` controls which font sources are allowed to be loaded via `@font-face`.

## Q13: What is the `object-src` CSP directive?
**A:** `object-src` restricts the sources from which plugins like Flash and Java can be loaded using `<object>`, `<embed>`, or `<applet>`.

## Q14: What is the `frame-src` CSP directive?
**A:** `frame-src` specifies allowed sources for loading content in frames and iframes, replacing the deprecated `child-src` directive.

## Q15: What is the `base-uri` CSP directive?
**A:** `base-uri` restricts which URLs can be used in the `<base>` element, preventing attackers from redirecting relative URLs.

## Q16: What is the `form-action` CSP directive?
**A:** `form-action` specifies which endpoints are allowed as form submission targets, preventing clickjacking and redirection attacks.

## Q17: What is the `manifest-src` CSP directive?
**A:** `manifest-src` controls which sources can serve web app manifest files.

## Q18: What is the `media-src` CSP directive?
**A:** `media-src` defines allowed sources for media elements like `<audio>` and `<video>`.

## Q19: What is the `frame-ancestors` CSP directive?
**A:** `frame-ancestors` controls which parent pages can embed the current page in frames, preventing clickjacking.

## Q20: What is the `upgrade-insecure-requests` CSP directive?
**A:** This directive instructs browsers to upgrade all HTTP requests to HTTPS before making the request.

## Q21: How do you use CSP nonces with Helmet?
**A:** Pass a `nonce` function to the CSP config that generates a unique nonce per request, then reference it in your script and style tags.

## Q22: How do you use CSP hashes with Helmet?
**A:** Compute a SHA-256/384/512 hash of the inline script or style content and add it to the `scriptSrc` or `styleSrc` directive using `script-src sha256-...`.

## Q23: What is CSP report-only mode?
**A:** Report-only mode sends violations to a report endpoint without blocking resources, using the `Content-Security-Policy-Report-Only` header.

## Q24: How do you enable CSP report-only in Helmet?
**A:** Set `reportOnly: true` in the `contentSecurityPolicy` options and provide a `reportUri` endpoint to receive violation reports.

## Q25: What is a CSP report endpoint?
**A:** A server endpoint defined via `report-uri` or `report-to` that receives JSON reports of CSP violations for monitoring and debugging.

## Q26: What is the Strict-Transport-Security (HSTS) header?
**A:** HSTS instructs browsers to always connect via HTTPS for a specified duration, preventing SSL stripping attacks.

## Q27: How do you configure HSTS with Helmet?
**A:** Set `strictTransportSecurity` with `maxAge` (seconds), `includeSubDomains`, and `preload` options to control HSTS behavior.

## Q28: What does `includeSubDomains` do in HSTS?
**A:** It tells the browser to apply the HSTS policy to all subdomains of the current domain as well.

## Q29: What is the HSTS `preload` directive?
**A:** The `preload` flag allows the domain to be submitted to browser preload lists so HSTS is enforced even on the first visit.

## Q30: What is the X-Frame-Options header?
**A:** X-Frame-Options prevents clickjacking by controlling whether the page can be rendered in a frame or iframe.

## Q31: What values can X-Frame-Options take?
**A:** `DENY` (no framing allowed), `SAMEORIGIN` (framing allowed by same origin), and `ALLOW-FROM uri` (deprecated, use CSP `frame-ancestors` instead).

## Q32: What is the X-Content-Type-Options header?
**A:** X-Content-Type-Options with value `nosniff` prevents browsers from MIME-sniffing files away from the declared Content-Type.

## Q33: What is the X-XSS-Protection header?
**A:** X-XSS-Protection was a legacy header for Internet Explorer and older browsers that enabled the built-in XSS filter. Modern browsers have deprecated it.

## Q34: What is the Referrer-Policy header?
**A:** Referrer-Policy controls how much referrer information is included in requests, balancing privacy and functionality.

## Q35: What is the Permissions-Policy header?
**A:** Permissions-Policy (formerly Feature-Policy) allows controlling which browser APIs and features a page and its iframes can access.

## Q36: What is the `frameguard` middleware?
**A:** `frameguard` is Helmet's middleware that sets the X-Frame-Options header to prevent clickjacking attacks.

## Q37: What is the `hsts` middleware?
**A:** `hsts` is Helmet's middleware that sets the Strict-Transport-Security header for enforcing HTTPS connections.

## Q38: What is the `noSniff` middleware?
**A:** `noSniff` sets the X-Content-Type-Options header to `nosniff` to disable MIME type sniffing.

## Q39: What is the `xssFilter` middleware?
**A:** `xssFilter` sets the X-XSS-Protection header to enable the browser's reflective XSS filter (deprecated in modern browsers).

## Q40: What is the `referrerPolicy` middleware?
**A:** `referrerPolicy` sets the Referrer-Policy header to control referrer information sent with requests.

## Q41: What is the `permissionsPolicy` middleware?
**A:** `permissionsPolicy` sets the Permissions-Policy header to restrict browser API access like camera, microphone, and geolocation.

## Q42: What is the `dnsPrefetchControl` middleware?
**A:** `dnsPrefetchControl` sets the X-DNS-Prefetch-Control header to control browser DNS prefetching behavior.

## Q43: What is the `expectCt` middleware?
**A:** `expectCt` sets the Expect-CT header to enforce Certificate Transparency requirements (deprecated and removed in Helmet v7).

## Q44: What is the `crossOriginEmbedderPolicy` middleware?
**A:** It sets the Cross-Origin-Embedder-Policy header, requiring cross-origin resources to be loaded with explicit permission via CORS or CORP.

## Q45: What is the `crossOriginOpenerPolicy` middleware?
**A:** It sets the Cross-Origin-Opener-Policy header, controlling whether the page can share a browsing context group with cross-origin pages.

## Q46: What is the `crossOriginResourcePolicy` middleware?
**A:** It sets the Cross-Origin-Resource-Policy header, controlling which origins can read the response of this resource.

## Q47: What is the Origin-Agent-Cluster header?
**A:** Helmet sets Origin-Agent-Cluster to instruct browsers to isolate the origin in its own OS process for better security.

## Q48: How does Helmet handle CORS?
**A:** Helmet does not handle CORS directly; use the `cors` npm package alongside Helmet for Cross-Origin Resource Sharing configuration.

## Q49: Does Helmet protect against CSRF attacks?
**A:** No, Helmet does not protect against CSRF. Use dedicated CSRF protection like the `csrf` or `csurf` package or double-submit cookie patterns.

## Q50: How do you use Helmet with Express.js?
**A:** Require `helmet` and call `app.use(helmet())` at the top of your Express middleware stack to apply all security headers globally.

## Q51: How do you use Helmet with NestJS?
**A:** In NestJS, call `app.use(helmet())` in the `bootstrap()` function after creating the NestExpressApplication instance.

## Q52: How do you use Helmet with Fastify?
**A:** Helmet does not natively support Fastify; use `@fastify/helmet` which wraps Helmet for the Fastify plugin system.

## Q53: How do you disable a specific Helmet middleware?
**A:** Pass `false` for the specific middleware key in the config object, e.g., `helmet({ frameguard: false })`.

## Q54: How do you configure Helmet for development environments?
**A:** Conditionally disable strict policies like HSTS and CSP in development by passing different config objects based on `NODE_ENV`.

## Q55: What is the default CSP policy in Helmet?
**A:** Helmet's default CSP is fairly strict, set to `default-src: 'self'` which only allows resources from the same origin.

## Q56: Can Helmet be used with Express Router?
**A:** Yes, you can apply Helmet to specific routes by using `router.use(helmet())` instead of at the app level.

## Q57: Does Helmet affect performance?
**A:** The performance impact of Helmet is negligible as it simply sets response headers with minimal computation per request.

## Q58: What changed in Helmet v4?
**A:** Helmet v4 stopped setting the X-XSS-Protection header by default due to deprecation by modern browsers.

## Q59: What changed in Helmet v5?
**A:** Helmet v5 made `contentSecurityPolicy` more configurable and improved TypeScript definitions.

## Q60: What changed in Helmet v6?
**A:** Helmet v6 reordered middleware, made CSP enabled by default, and removed the deprecated `expectCt` middleware.

## Q61: What changed in Helmet v7?
**A:** Helmet v7 simplified the API by removing deprecated options, requiring explicit opt-in for loose CSP policies, and improving defaults.

## Q62: How do you set custom headers not covered by Helmet?
**A:** Use the `crossdomain` middleware in Helmet or set custom headers directly with `res.setHeader()` in your own middleware.

## Q63: Can Helmet be used with Koa?
**A:** Helmet is primarily designed for Express; use `koa-helmet` which provides a Koa-compatible wrapper around Helmet middleware.

## Q64: What is the `hidePoweredBy` middleware?
**A:** `hidePoweredBy` removes or renames the X-Powered-By header to obscure the server technology stack.

## Q65: What is the `ieNoOpen` middleware?
**A:** `ieNoOpen` sets the X-Download-Options header for Internet Explorer to prevent downloads from opening in the context of your application.

## Q66: What is the `xPermittedCrossDomainPolicies` middleware?
**A:** It sets the X-Permitted-Cross-Domain-Policies header to control which cross-domain requests Adobe plugins are allowed to make.

## Q67: How do you set Helmet for specific routes only?
**A:** Instead of `app.use(helmet())`, apply it to specific routes: `app.get('/api', helmet(), handler)`.

## Q68: What order should Helmet be applied in middleware?
**A:** Helmet should generally be one of the first middleware in the stack, applied before routes and body parsers.

## Q69: How do you update CSP dynamically per request?
**A:** Use a function for CSP directives instead of a static object, receiving `req` and `res` to generate dynamic policies per request.

## Q70: What is `report-uri` in CSP?
**A:** `report-uri` is a CSP directive that tells the browser to POST JSON violation reports to a specified URL when a policy is violated.

## Q71: What is `report-to` in CSP?
**A:** `report-to` is a newer CSP directive that uses the Reporting API to send violation reports, replacing the deprecated `report-uri`.

## Q72: What is the `block-all-mixed-content` CSP directive?
**A:** This directive blocks all mixed content (HTTP resources on HTTPS pages), preventing passive mixed content warnings.

## Q73: How does Helmet handle nonce generation?
**A:** You provide a function that returns a unique nonce per request; Helmet then adds it to both the CSP header and exposes it for use in templates.

## Q74: What is a CSP hash?
**A:** A CSP hash is a cryptographic hash (sha256, sha384, sha512) of an inline script or style that allows it to execute without a nonce.

## Q75: How do you use `strict-dynamic` in CSP?
**A:** `strict-dynamic` allows scripts loaded by already-trusted scripts to execute, simplifying CSP for sites that use JavaScript frameworks.

## Q76: What is `unsafe-inline` in CSP?
**A:** `unsafe-inline` allows all inline scripts and styles, which weakens CSP protection and should only be used during migration.

## Q77: What is `unsafe-eval` in CSP?
**A:** `unsafe-eval` allows the use of `eval()`, `setTimeout(string)`, and other dynamic code evaluation methods in JavaScript.

## Q78: What is the `self` keyword in CSP?
**A:** `self` refers to the origin of the document itself, allowing resources to be loaded from the same scheme, host, and port.

## Q79: What is the `none` keyword in CSP?
**A:** `none` means no sources are allowed for that directive, effectively blocking all resources of that type.

## Q80: Can Helmet be used in serverless environments?
**A:** Yes, Helmet works in serverless environments like AWS Lambda when used with Express-compatible frameworks via `serverless-http`.

## Q81: How do you test Helmet headers?
**A:** Use tools like `curl -I`, browser DevTools network tab, or security testing tools like OWASP ZAP to inspect response headers.

## Q82: What is HTTP Public Key Pinning (HPKP)?
**A:** HPKP was a security header that Helmet previously supported but it has been deprecated and removed due to security risks and browser removal.

## Q83: How do you configure CSP for Google Analytics?
**A:** Add `https://www.google-analytics.com` and `https://googletagmanager.com` to `scriptSrc` and `connectSrc` directives in your CSP config.

## Q84: How do you configure CSP for CDN resources?
**A:** Add the CDN domain (e.g., `https://cdn.example.com`) to the relevant directives like `scriptSrc`, `styleSrc`, or `imgSrc` as needed.

## Q85: What is a nonce-based CSP strategy?
**A:** A nonce-based strategy generates a unique random token per request for each trusted script tag, avoiding `unsafe-inline` while allowing dynamic scripts.

## Q86: What is a hash-based CSP strategy?
**A:** A hash-based strategy computes cryptographic hashes of known inline scripts and allows them explicitly, suitable for static inline content.

## Q87: How do you log CSP violations?
**A:** Set a `reportUri` endpoint in your CSP config, then parse the POSTed JSON violation reports and log them for analysis.

## Q88: What browsers support CSP?
**A:** All modern browsers including Chrome, Firefox, Safari, and Edge support CSP level 2 and most features of CSP level 3.

## Q89: What is the difference between CSP and CORS?
**A:** CSP controls which resources a page can load (restrictive), while CORS controls which origins can access a page's resources (permissive).

## Q90: How do you handle WebSocket connections with CSP?
**A:** Use the `connect-src` directive with `wss://your-domain.com` to allow WebSocket connections to specific origins.

## Q91: How do you handle multiple CSP directives?
**A:** Pass an object with each directive as a key to the `directives` option, with arrays of allowed sources as values.

## Q92: What is the `worker-src` CSP directive?
**A:** `worker-src` controls which sources are allowed for Web Workers, Service Workers, and Shared Workers.

## Q93: What is the `navigate-to` CSP directive?
**A:** `navigate-to` restricts which URLs the document can navigate to, limiting the destinations of links and form submissions.

## Q94: How do you apply Helmet conditionally in Express?
**A:** Use a custom middleware that checks conditions (like request path or environment) before calling `helmet()` with different configs.

## Q95: What are the security best practices for Helmet?
**A:** Place Helmet early in middleware stack, avoid `unsafe-inline` in CSP, use nonces or hashes for inline scripts, and enable HSTS with `includeSubDomains`.

## Q96: How does Helmet interact with reverse proxies?
**A:** If behind a reverse proxy like Nginx, ensure `trust proxy` is set in Express so Helmet reads the correct protocol and host values.

## Q97: Can you use multiple Helmet instances?
**A:** No, only the first `helmet()` call affects the response; subsequent calls are redundant since headers are already set.

## Q98: How do you disable the entire CSP in Helmet?
**A:** Pass `contentSecurityPolicy: false` to the `helmet()` options to disable CSP while keeping other Helmet middleware active.

## Q99: What is the `agentCluster` middleware in Helmet?
**A:** `agentCluster` sets the `Origin-Agent-Cluster` header to enable origin keying, isolating the origin in its own process.

## Q100: Why is Helmet important for production Node.js apps?
**A:** Helmet provides a simple, battle-tested way to set essential security headers that protect against common web vulnerabilities like XSS, clickjacking, and MIME sniffing.
