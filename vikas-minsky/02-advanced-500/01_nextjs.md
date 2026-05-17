## 20. Next.js Advanced (501–540)

501. How does React Server Components reduce bundle size?
   RSCs execute on the server and never send their code to the client. This eliminates the need to bundle React components, reducing JavaScript payload and improving initial load performance.

502. Explain request memoization in Next.js.
   Next.js automatically deduplicates fetch requests within a single render pass using the `fetch` cache. Multiple components requesting the same data share the same promise, preventing redundant network calls.

503. What are static exports in Next.js?
   Static exports generate a fully static HTML/CSS/JS output via `next export`. The app runs without a Node.js server, suitable for CDN hosting but sacrificing SSR, API routes, and middleware.

504. How do route handlers differ from API routes?
   Route handlers (App Router) use `route.ts` files inside directories and support streaming, while API routes (Pages Router) use `api/` files. Route handlers are more tightly integrated with RSCs and middleware.

505. Explain edge caching strategies.
   Edge caching stores responses at CDN nodes close to users. Strategies include static caching for immutable assets, stale-while-revalidate for dynamic content, and caching based on headers like `Cache-Control` and `CDN-Cache-Control`.

506. What are server-only modules?
   Server-only modules are files marked with `server-only` package or placed in the `lib/` directory. They can only execute on the server, safely containing secrets, database queries, and filesystem operations.

507. How does React Flight work?
   React Flight is the wire protocol for RSCs. It serializes server component output into a compact format that the client uses to reconstruct the component tree without executing the component code on the client.

508. Explain hydration mismatch debugging.
   Hydration mismatches occur when server HTML differs from client render. Debug by checking browser console warnings, using `suppressHydrationWarning` for intentional differences, and ensuring deterministic data sources.

509. What are nested Suspense boundaries used for?
   Nested Suspense boundaries allow granular streaming of independent UI sections. Each boundary can show its own fallback, enabling progressive rendering where fast data loads appear before slow ones.

510. Explain incremental adoption in Next.js.
   Incremental adoption lets you migrate from Pages Router to App Router incrementally. Both routers can coexist, allowing per-page migration using the `app/` directory alongside existing `pages/`.

511. How do cookies work in Server Components?
   Cookies in RSCs are accessed via server-only APIs like `cookies()` from `next/headers`. They are read on the server and sent as part of the initial response; mutations require Server Actions or Route Handlers.

512. Explain draft mode in Next.js.
   Draft mode bypasses static generation caching, rendering pages dynamically with draft content from a headless CMS. It uses a cookie-based toggle, typically activated via a secret URL.

513. What is dynamic rendering?
   Dynamic rendering generates HTML per request instead of at build time. It enables real-time data, cookies, and headers but increases server load. Used for personalized or frequently changing content.

514. Explain rendering waterfalls.
   Rendering waterfalls occur when parent components fetch data before children start their fetches sequentially. This increases load time; parallel data fetching with Promise.all or Suspense boundaries helps avoid it.

515. How do you reduce TTFB in Next.js?
   Reduce TTFB by using edge functions for low-latency execution, static generation for content, ISR for semi-dynamic pages, optimizing database queries, and enabling streaming to send HTML early.

516. Explain prefetching strategies.
   Next.js prefetches route segments on link hover using `<Link>` with `prefetch={true}`. Strategies include static prefetch for SSG pages, dynamic prefetch for SSR, and disabling prefetch for rarely visited routes.

517. What is bundle analysis?
   Bundle analysis visualizes the size of JavaScript bundles using tools like `@next/bundle-analyzer`. It helps identify large dependencies, code splitting gaps, and tree-shaking opportunities.

518. Explain tree shaking in Next.js.
   Tree shaking removes unused exports via static analysis. Next.js uses Webpack/Turbopack's tree shaker, and RSCs inherently shake better by eliminating client bundles entirely for server-only code.

519. How does middleware rewriting work?
   Middleware rewriting modifies incoming request URLs before routing using `NextResponse.rewrite()`. It enables A/B testing, localization, and feature flags without changing the URL the user sees.

520. Explain redirects vs rewrites.
   Redirects return a 3xx status to the browser, changing the URL bar. Rewrites serve content from a different path internally while the URL stays the same, useful for masked routing.

521. How do you secure middleware logic?
   Secure middleware by avoiding secrets inline (use env variables), validating user tokens at the edge, limiting middleware to necessary routes via config matchers, and avoiding heavy computation.

522. Explain server action security risks.
   Server Actions expose endpoints that could be abused. Risks include CSRF (mitigated with `useActionState`), unauthorized invocation (add auth checks), and data leakage (validate all inputs with Zod).

523. What are route segment configs?
   Route segment configs are exported `const` objects in layout or page files that control rendering behavior: `dynamic`, `revalidate`, `fetchCache`, `runtime`, and `preferredRegion` for fine-grained per-route control.

524. Explain dynamic metadata generation.
   Dynamic metadata uses the `generateMetadata` async function in layout/page files to produce SEO metadata based on params, searchParams, or fetched data, supporting Open Graph, Twitter cards, and JSON-LD.

525. How does font optimization work?
   Next.js automatically downloads and self-hosts Google Fonts via `next/font`, eliminating external requests. It applies CSS `size-adjust` to prevent layout shift and supports variable fonts and subsets.

526. Explain partial hydration concepts.
   Partial hydration hydrates only interactive client components on the page while server components remain static. This reduces JavaScript execution, improving time-to-interactive for content-heavy pages.

527. What are React cache boundaries?
   Cache boundaries isolate fetch deduplication scopes. Wrapping a segment with `<CacheBoundary>` or using `react.cache()` creates a new cache context, preventing stale data sharing across concurrent renders.

528. Explain stale-while-revalidate behavior.
   Stale-while-revalidate serves cached (stale) content immediately while triggering a background refresh. Next.js ISR uses this pattern: returning static HTML and regenerating it in the background.

529. How do you optimize large Next.js apps?
   Optimize large apps with modular routing, lazy loading heavy components via `next/dynamic`, parallel data fetching, selective RSC usage, bundle analysis, proper caching headers, and partial prerendering.

530. Explain monorepo support in Next.js.
   Next.js supports monorepos natively with Turbopack, allowing shared UI components, utilities, and types across packages. Workspaces in npm/pnpm/yarn enable single `npm install` and unified builds.

531. How does turborepo integrate with Next.js?
   Turborepo integrates with Next.js via the `next` task definition in `turbo.json`, enabling parallel build execution, remote caching of `.next` artifacts, and dependency-aware task orchestration.

532. Explain server timing headers.
   Server Timing (`Server-Timing`) headers expose backend performance metrics to browser DevTools. Next.js can emit custom timing data for route generation, data fetching, and rendering phases.

533. How do you profile rendering performance?
   Profile rendering using `React.Profiler`, Chrome DevTools flame charts, Next.js `instrumentation.ts` for server-side profiling, and the built-in `next dev --profile` flag to capture rendering logs.

534. Explain React compiler implications.
   The React Compiler (forget) automatically memoizes components and hooks, reducing manual `useMemo` and `useCallback`. In Next.js this means fewer re-renders, smaller bundles, and simpler code.

535. What are edge function limitations?
   Edge functions have limited APIs (no Node.js `fs`, `crypto`, or `child_process`), max execution time (30s on Vercel), smaller memory limits (128MB), and no direct database connections without connection pooling.

536. Explain deployment cold starts.
   Cold starts happen when serverless functions spin up from idle, adding latency (500ms–2s). Mitigate with keep-alive pings, provisioned concurrency, edge functions for low-latency routes, and warm startup strategies.

537. How do you implement feature flags?
   Feature flags use middleware or route handlers to evaluate flag values from services like LaunchDarkly or Flagsmith. Include the flag check in layout data, apply via rewrites, or use client-side hooks.

538. Explain locale-based routing.
   Locale-based routing serves content per locale using `next.config` i18n or `middleware.ts` with path detection. It supports sub-path (`/en/`), domain-based routing, and automatic language detection.

539. How do you implement A/B testing?
   A/B testing uses middleware to assign variants via cookies/headers, rewrites to serve different pages, and analytics to track conversions. Variants can be server-rendered or client-resolved with feature flags.

540. Explain enterprise-grade Next.js architecture.
   Enterprise architecture includes modular monorepo structure, RSC-first design, edge API routes for globality, centralized auth middleware, feature-flag-driven deploys, ISR for content, and full observability with OpenTelemetry.
