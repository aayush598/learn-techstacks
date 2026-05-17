## 39. Next.js Expert Topics (1001–1040)

1001. How does React selective hydration work in Next.js?
   Selective hydration allows React to hydrate components incrementally as their data becomes available, rather than waiting for the entire page to load. Next.js uses this to prioritize hydrating interactive content first, improving Time to Interactive.

1002. Explain edge-side rendering.
   Edge-side rendering executes server logic at CDN edge nodes close to the user, reducing latency by eliminating round trips to a central origin server. Next.js supports this via edge runtime functions that run on platforms like Vercel Edge or Cloudflare Workers.

1003. What are cache tags in Next.js?
   Cache tags are labels attached to cached responses that allow fine-grained invalidation of specific data segments. When a revalidation request targets a tag, all tagged cache entries are purged, enabling precise control over stale content.

1004. Explain on-demand revalidation.
   On-demand revalidation triggers cache refreshes through explicit API calls or webhooks instead of waiting for time-based expiry. This ensures users see fresh content immediately after data changes, commonly used with headless CMS webhooks.

1005. How does static optimization detection work?
   Next.js statically analyzes each page to determine if it can be pre-rendered into static HTML. Pages without dynamic data or blocking APIs are automatically marked as static, reducing server load and improving response times.

1006. Explain navigation cache behavior.
   Next.js caches rendered route segments in memory during client-side navigation, enabling instant back/forward navigation without re-fetching data. The cache uses a Least Recently Used eviction policy and is invalidated on full page reloads.

1007. What are server boundaries?
   Server boundaries are code boundaries in React's component tree that separate server-executed from client-executed code. Components below a boundary run exclusively on the server and are never sent to the browser.

1008. Explain route preloading internals.
   Next.js preloads route chunks when a link enters the viewport, using IntersectionObserver to fetch both the component JavaScript and initial data. This makes navigations feel instant by parallelizing network requests with user reading time.

1009. How do streaming responses improve UX?
   Streaming responses send HTML chunks progressively as they render on the server, allowing the browser to display content before the full response is ready. This reduces First Contentful Paint and perceived load time.

1010. Explain browser hydration priorities.
   React prioritizes hydrating components that the user is likely to interact with first, using scheduling heuristics based on viewport position and interaction cues. This ensures critical interactivity is available before off-screen content.

1011. What are async server component limitations?
   Async server components cannot use hooks, event handlers, or browser APIs since they execute solely on the server. They also cannot be directly imported by client components without being passed as children.

1012. Explain middleware matcher patterns.
   Middleware matchers use glob patterns to define which routes trigger middleware execution, allowing efficient filtering before the request reaches the page handler. Complex patterns can combine inclusive and exclusive rules for precise control.

1013. How do dynamic imports impact TTI?
   Dynamic imports split code into smaller chunks loaded on demand, reducing initial bundle size and improving Time to Interactive. However, excessive splitting can create network waterfalls that delay interactivity for critical features.

1014. Explain image CDN optimization.
   Next.js Image Optimization integrates with CDNs to automatically serve images in modern formats like WebP and AVIF, resize them to the device viewport, and apply quality compression. This reduces bandwidth while maintaining visual fidelity.

1015. What are asset prefix configurations?
   Asset prefixes allow deploying static assets to a separate CDN domain by prepending a URL prefix to all asset references. This enables independent scaling of asset delivery and avoids cookie overhead on static requests.

1016. Explain custom webpack configurations.
   Custom webpack configs in `next.config.js` extend Next.js's internal bundling pipeline, allowing modifications to loaders, plugins, and resolve aliases. Overriding core rules can break optimizations and requires careful alignment with Next.js conventions.

1017. How does Next.js optimize fonts automatically?
   Next.js self-hosts Google Fonts and other external fonts during build time, eliminating external network requests and reducing layout shift. It also applies size-adjust and fallback metrics to minimize Cumulative Layout Shift.

1018. Explain script loading strategies.
   Next.js provides `beforeInteractive`, `afterInteractive`, and `lazyOnload` strategies that control when external scripts execute relative to page hydration, ensuring critical scripts don't block rendering while non-essential ones load asynchronously.

1019. What are server actions serialization rules?
   Server actions accept and return only serializable data—plain objects, arrays, primitives, Dates, Maps, and Sets—and reject functions, symbols, or class instances. This constraint ensures data can be safely transmitted over the network boundary.

1020. Explain React cache deduplication.
   React's native `cache` function deduplicates identical fetch requests made across multiple components during a single render pass, ensuring that the same data is fetched only once even if ten components request it concurrently.

1021. How do edge functions access headers?
   Edge functions receive incoming request headers through the standard `Request` API parameter, enabling header inspection for authentication, geolocation, and A/B testing without round-tripping to origin servers.

1022. Explain request coalescing.
   Request coalescing merges concurrent requests for the same resource into a single upstream call, broadcasting the result to all pending consumers. This prevents thundering herd problems in serverless environments.

1023. What are rendering priority heuristics?
   Rendering priority heuristics determine which components render first based on viewport visibility, user interaction likelihood, and data dependency depth. React uses these to optimize perceived performance through suspense boundaries.

1024. Explain hydration race conditions.
   Hydration race conditions occur when server-rendered DOM differs from the initial client render due to dynamic data or browser-specific APIs, causing React to discard the server HTML and re-render from scratch, hurting performance.

1025. How does Next.js handle redirects at scale?
   Next.js handles redirects at the edge before requests reach the server, using configuration-based rules in `next.config.js` that map source paths to destinations with status codes. This avoids server-side computation for common redirect patterns.

1026. Explain partial static generation.
   Partial static generation pre-renders static parts of a page at build time while deferring dynamic content to runtime streaming or client-side fetching. This combines the speed of static delivery with the freshness of dynamic data.

1027. What are CDN invalidation strategies?
   CDN invalidation strategies include tag-based purging, path-based purging, and surrogate-key purging that remove stale content from edge caches. On-demand revalidation is preferred over time-based TTLs for frequently changing content.

1028. Explain navigation transitions.
   Navigation transitions coordinate loading states, layout shifts, and component mounting during client-side route changes. Next.js uses the App Router's loading.js, error.js, and template components to provide smooth transition feedback.

1029. How does Next.js support observability?
   Next.js supports observability through OpenTelemetry integration, request logging, and custom metric reporting. Built-in instrumentation hooks allow capturing server timing, data fetch durations, and error rates.

1030. Explain OpenTelemetry in Next.js.
   OpenTelemetry integration in Next.js automatically instruments server components, API routes, and middleware with distributed tracing spans. This enables correlation of frontend performance with backend service calls.

1031. What are middleware cold starts?
   Middleware cold starts occur when an edge function spins up from idle, incurring latency for the first request. Mitigations include keeping functions warm with periodic pings and minimizing middleware bundle size.

1032. Explain edge region selection.
   Edge region selection routes requests to the geographically closest edge node based on the user's IP location. This minimizes latency for global audiences and is configured through deployment platform settings.

1033. How do you reduce JavaScript payload size?
   Payload reduction techniques include tree-shaking unused exports, code splitting by routes, dynamic imports for heavy libraries, and optimizing dependencies to use ES modules. Next.js's automatic bundling handles most of this.

1034. Explain advanced SEO rendering concerns.
   Advanced SEO concerns include ensuring critical content renders in the initial HTML (not requiring JavaScript), managing canonical URLs, handling pagination with rel=next/prev, and avoiding duplicate content from dynamic parameters.

1035. What are dynamic segment collisions?
   Dynamic segment collisions happen when multiple route patterns match the same URL path, causing ambiguous routing. Next.js resolves this by prioritizing more specific patterns over less specific ones in the route definition order.

1036. Explain React suspense waterfalls.
   Suspense waterfalls occur when nested suspense boundaries each wait for their parent's data to resolve before fetching their own, creating sequential loading delays. Parallel data fetching and lifting suspense boundaries higher mitigate this.

1037. How does Next.js integrate with serverless platforms?
   Next.js compiles application routes into standalone serverless functions that platforms like Vercel, AWS Lambda, and Netlify deploy individually. Each function handles a specific route, enabling independent scaling and isolation.

1038. Explain frontend error boundary strategies.
   Error boundary strategies include granular boundaries per feature section, fallback UI that preserves surrounding functionality, and error recovery mechanisms that allow retrying failed operations without full page reloads.

1039. What are advanced bundle splitting techniques?
   Advanced bundle splitting includes splitting by route, by component visibility, by device type, and by user interaction patterns. Module federation and granular chunking allow teams to deploy independently.

1040. How do enterprise teams structure Next.js apps?
   Enterprise teams structure Next.js apps with domain-driven folder organization, shared component libraries, feature-flag systems for gradual rollouts, and monorepo tooling for cross-team collaboration. They also implement strict code ownership and code review standards.
