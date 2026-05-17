## 1. Next.js (1–40)

1. What problems does Next.js solve compared to React?
   Next.js solves several key problems: it provides server-side rendering for better SEO and faster initial page loads, file-based routing for simpler navigation, automatic code splitting, built-in image optimization, API routes for backend logic, and a full-stack framework with opinionated conventions.

2. Explain SSR, SSG, ISR, and CSR in Next.js.
   SSR (Server-Side Rendering) renders pages on each request. SSG (Static Site Generation) pre-builds pages at build time. ISR (Incremental Static Regeneration) updates static pages after build without full rebuild. CSR (Client-Side Rendering) renders entirely in the browser using JavaScript.

3. What is the App Router in Next.js?
   The App Router is the newer routing paradigm introduced in Next.js 13, built on React Server Components. It uses a file-system based router inside the `app` directory with support for layouts, nested routes, loading states, and error boundaries.

4. Difference between App Router and Pages Router?
   The Pages Router uses the `pages` directory with React components rendered client-side by default. The App Router uses the `app` directory with Server Components by default, supports nested layouts, streaming, and more advanced routing features like parallel and intercepting routes.

5. What are Server Components?
   Server Components are React components that render exclusively on the server, never send JavaScript to the client, and can directly access databases, file systems, and backend resources. They reduce bundle size and improve performance by keeping heavy dependencies server-side.

6. What are Client Components?
   Client Components are React components that render on both server and client, with interactivity and browser APIs. They are marked with `use client` directive and are hydrated in the browser for dynamic behavior like event handlers and hooks.

7. When should you use `use client`?
   Use `use client` when a component needs browser APIs, event handlers, useState, useEffect, or other interactive React hooks. Components that only render static content or fetch data should remain Server Components by default.

8. How does routing work in Next.js?
   Next.js uses file-system routing where folders define route segments and files define UI. The App Router uses `page.tsx` for public routes, `layout.tsx` for shared layouts, `loading.tsx` for loading states, and `error.tsx` for error boundaries.

9. What are dynamic routes?
   Dynamic routes allow parameterized URLs using folder names with square brackets like `[id]` or `[...slug]`. They enable pages like `/blog/123` where `123` is captured as a route parameter accessible via `params`.

10. What are route groups?
    Route groups are folders named in parentheses like `(marketing)` that organize routes without affecting the URL path. They group related routes together and allow different layouts for different sections of the app.

11. Explain nested layouts in Next.js.
    Nested layouts allow you to define layout files at any level in the route hierarchy. Each layout wraps its child pages and nested layouts, enabling persistent UI like headers and sidebars that won't re-render during navigation.

12. How does metadata handling work?
    Next.js supports both static and dynamic metadata via the `metadata` object or `generateMetadata` function exported from page or layout files. It automatically generates title, description, Open Graph, and other meta tags for SEO.

13. What is streaming in Next.js?
    Streaming allows the server to progressively send HTML to the client as it renders, enabling faster time-to-first-byte. Users see the page shell immediately while content loads asynchronously.

14. Explain Suspense boundaries.
    Suspense boundaries wrap components that depend on asynchronous data loading. They display fallback UI (like loading spinners) while the component is being fetched, enabling streaming and progressive rendering.

15. What are loading.tsx and error.tsx?
    `loading.tsx` defines the fallback UI shown while a route segment loads. `error.tsx` defines the error UI when rendering fails, with automatic error recovery and the ability to retry.

16. What are server actions?
    Server Actions are async functions that run on the server, invoked directly from client components via form actions or event handlers. They handle form submissions, data mutations, and revalidate cached data without creating explicit API routes.

17. How does caching work in Next.js?
    Next.js employs multiple caching layers: the Full Route Cache stores rendered pages, the Data Cache stores fetch results, and the Router Cache stores navigation payloads client-side. Each layer has configurable revalidation strategies.

18. Difference between fetch cache modes?
    The default `force-cache` stores data indefinitely until revalidated. `no-store` fetches fresh data on every request. `revalidate` sets a time-based revalidation. `{ next: { tags: [] } }` enables on-demand revalidation via tags.

19. What is ISR and how is revalidation handled?
    ISR (Incremental Static Regeneration) allows static pages to be updated after deployment without rebuilding the entire site. Revalidation can be time-based via `revalidate` in getStaticProps or on-demand via `revalidatePath` and `revalidateTag` APIs.

20. Explain middleware in Next.js.
    Middleware runs before every request, allowing you to redirect, rewrite, set headers, or check authentication. It executes at the edge for low latency and uses a single `middleware.ts` file at the project root.

21. How do you implement authentication in Next.js?
    Authentication is typically implemented using middleware for route protection, server actions or API routes for login/signup, and libraries like NextAuth.js for OAuth. Server Components check session state, while Client Components use context for UI changes.

22. Explain edge runtime.
    The Edge Runtime is a lightweight, fast runtime based on Web APIs that runs at CDN edge locations globally. It supports streaming, has lower latency than Node.js, and is ideal for middleware, authentication, and personalization.

23. Difference between edge and node runtimes?
    The Node.js runtime has full Node.js API support including file system, databases, and native modules. The Edge runtime is more limited but faster, supporting Web APIs like Request/Response, with no Node.js-specific modules.

24. How do image optimizations work?
    The `next/image` component automatically optimizes images by serving modern formats (WebP/AVIF), resizing to device dimensions, lazy loading, and preventing layout shift. Images are optimized on-demand at request time.

25. Explain code splitting in Next.js.
    Next.js automatically splits code by route segments, loading only the JavaScript needed for the current page. This reduces initial bundle size and improves performance through lazy loading of non-critical components.

26. How does bundling in Next.js work?
    Next.js uses Webpack (or Turbopack in dev) to bundle JavaScript and CSS. It automatically splits bundles by route, tree-shakes unused code, and optimizes production builds with minification, compression, and dead code elimination.

27. Explain partial prerendering.
    Partial Prerendering (PPR) combines static and dynamic content on the same page. The static shell is pre-rendered at build time, while dynamic components are streamed in as they resolve, giving SSG speed with SSR flexibility.

28. How do you handle SEO in Next.js?
    SEO is handled through metadata API for meta tags, server-side rendering for search engine crawlability, sitemap generation, robots.txt configuration, image optimization for Core Web Vitals, and structured data via JSON-LD.

29. What are API routes?
    API routes are serverless functions defined in the `pages/api` (or `app/api` with Route Handlers) directory. They handle backend logic like database queries, authentication, and third-party API integrations within the same project.

30. How do you deploy Next.js applications?
    Next.js apps deploy to Vercel (the recommended platform), AWS via Serverless Framework, Docker containers, or self-hosted Node.js servers. Deployment strategy depends on the rendering approach — static export for SSG, Node.js server for SSR.

31. Explain environment variables in Next.js.
    Environment variables are defined in `.env.local` files. Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser, while others remain server-only. Next.js inlines them at build time for the client bundle.

32. How do you secure secrets in Next.js?
    Secrets should never be prefixed with `NEXT_PUBLIC_` and should only be used in Server Components, API routes, or server actions. Use `.env.local` excluded from version control, and store production secrets in the deployment platform's secrets manager.

33. Explain data fetching patterns.
    Server Components fetch data directly using async/await. Client Components use hooks like useEffect, TanStack Query, or SWR. Static data is fetched at build time, dynamic data on request, and ISR for revalidated static content.

34. How do you optimize Core Web Vitals?
    Optimize by using the `next/image` component for CLS, lazy loading non-critical resources, minimizing JavaScript bundles, using streaming and Suspense for LCP, and optimizing fonts and third-party scripts.

35. Explain lazy loading in Next.js.
    Lazy loading is achieved via dynamic imports using `next/dynamic` for components or the `loading` prop for route segments. Components are loaded only when needed, reducing initial bundle size.

36. What are parallel routes?
    Parallel routes allow rendering multiple independent pages simultaneously within the same layout using named slots like `@modal` and `@feed`. Each slot renders separately, enabling features like dashboards and side panels.

37. Explain intercepting routes.
    Intercepting routes allow rendering a route from another part of the app within a modal while keeping the URL pointing to the intercepted page. They use `(..)` syntax similar to relative path traversal.

38. What is turbopack?
    Turbopack is an incremental bundler built by Vercel as a faster alternative to Webpack for development. It offers near-instant Hot Module Replacement and faster startup times using Rust-based incremental computation.

39. Explain hydration issues.
    Hydration issues occur when the server-rendered HTML and the client's first render differ, causing React to throw warnings or errors. Common causes include browser-only API usage, non-deterministic data, and timestamp or random value mismatches.

40. How do you debug production Next.js apps?
    Debug using `next/log` for server-side logging, the React DevTools and Next.js DevTools for client-side inspection, OpenTelemetry for tracing, and error monitoring tools like Sentry. Enable source maps for stack trace resolution.
