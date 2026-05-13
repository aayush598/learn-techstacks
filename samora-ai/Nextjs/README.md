# Next.js Interview Questions and Answers

## Q1: What is Next.js?
**A:** Next.js is a React framework for building full-stack web applications. It provides features like server-side rendering (SSR), static site generation (SSG), API routes, file-based routing, automatic code splitting, middleware, and more. It is developed by Vercel.

## Q2: What are the main rendering strategies in Next.js?
**A:** Static Site Generation (SSG) — HTML generated at build time; Server-Side Rendering (SSR) — HTML generated per request; Incremental Static Regeneration (ISR) — static regeneration after build at runtime; Client-Side Rendering (CSR) — data fetching on the client; and Partial Pre-rendering (PPR) — hybrid approach in Next.js 14+.

## Q3: What is the difference between Next.js and plain React?
**A:** Next.js is a framework built on top of React that adds routing (file-based), server-side rendering, static generation, API routes, image optimization, middleware, and built-in performance optimizations. Plain React is a library for building UIs and requires additional tools for routing, SSR, etc.

## Q4: What is the App Router in Next.js 13+?
**A:** The App Router is a new routing paradigm introduced in Next.js 13 that uses the `app/` directory, supports React Server Components by default, nested layouts, loading states, error boundaries, and parallel routes. It replaces the Pages Router.

## Q5: What are React Server Components (RSC) in Next.js?
**A:** React Server Components are components that run and render on the server, reducing the JavaScript bundle sent to the client. In Next.js 13+, all components in the App Router are Server Components by default. They can directly access databases, file systems, and backend resources.

## Q6: How do you create a client component in Next.js App Router?
**A:** By adding `'use client'` directive at the top of the file. This marks the component as a Client Component, which runs on both server (for initial HTML) and client (for interactivity), and has access to hooks like `useState`, `useEffect`, and browser APIs.

## Q7: What is file-based routing in Next.js?
**A:** File-based routing means the file structure inside the `pages/` or `app/` directory defines the routes. For example, `pages/about.js` maps to `/about`, `pages/blog/[slug].js` maps to `/blog/:slug`. The App Router uses folders with `page.js` files.

## Q8: What are layouts in Next.js App Router?
**A:** Layouts are wrapper components defined in `layout.js` files that persist across route changes and maintain state. They wrap child pages and can be nested. A root layout is required in the App Router and wraps all pages.

## Q9: What is `getStaticProps` and when would you use it?
**A:** `getStaticProps` (Pages Router) is a function that fetches data at build time and passes it as props to the page component. Used for SSG — ideal for content that doesn't change frequently, like blog posts, documentation, or marketing pages.

## Q10: What is `getServerSideProps`?
**A:** `getServerSideProps` (Pages Router) is a function that fetches data on each request at server-side. Used for SSR — ideal for pages with frequently changing data or user-specific content. It receives the request context (req, res, params, query).

## Q11: What is `getStaticPaths`?
**A:** `getStaticPaths` (Pages Router) is used with dynamic routes to specify which paths should be pre-rendered at build time. It returns an object with `paths` (array of parameter objects) and `fallback` behavior (false, true, or 'blocking').

## Q12: What is Incremental Static Regeneration (ISR)?
**A:** ISR allows updating static pages after build time without rebuilding the entire site. Using `revalidate` in `getStaticProps`, Next.js re-renders the page in the background when a request comes in after the revalidation period. The stale page is served while the new one is generated.

## Q13: How do you fetch data in the App Router?
**A:** In the App Router, Server Components can fetch data directly using `async` functions or libraries. For example: `async function Page() { const data = await fetch('https://api.example.com/data'); return <div>...</div> }`. No special functions like getStaticProps are needed.

## Q14: What is the difference between `fetch` in App Router and Pages Router?
**A:** In the App Router, `fetch` is extended with automatic caching and revalidation (using `next: { revalidate }` and `next: { tags }` options). In the Pages Router, data fetching uses specialized functions like `getStaticProps` and `getServerSideProps`.

## Q15: What are API routes in Next.js?
**A:** API routes allow creating backend API endpoints within a Next.js application. In the Pages Router, they are files inside `pages/api/`. In the App Router, they are `route.js` files inside the `app/` directory. They run server-side only.

## Q16: How do you create API routes in the App Router?
**A:** Create a `route.js` or `route.ts` file in the `app/` directory. Export functions named after HTTP methods: `export async function GET(request) { ... }`, `POST(req)`, `PUT(req)`, `DELETE(req)`, etc. The file path determines the URL.

## Q17: What is middleware in Next.js?
**A:** Middleware is a function that runs before a request is completed, allowing you to modify the response, redirect, rewrite, or set headers. Defined in a `middleware.ts` file at the project root. It runs on the Edge Runtime for low latency.

## Q18: What is Next.js Image component and its benefits?
**A:** The `next/image` component (Image) provides automatic image optimization, lazy loading, responsive images with srcset, placeholder blur, and WebP/AVIF format support. It requires explicit width/height (or fill) to prevent layout shift.

## Q19: What is the `next/link` component?
**A:** The `Link` component enables client-side navigation between pages. It prefetches linked pages in the background (when in viewport), supports shallow routing, and provides faster navigation compared to traditional anchor tags.

## Q20: How does Next.js handle code splitting?
**A:** Next.js automatically code-splits by route/page. Each page only loads its own JavaScript and dependencies. The framework also supports dynamic imports for further splitting of components that aren't needed immediately.

## Q21: What is dynamic import in Next.js?
**A:** `next/dynamic` is a function that lazy-loads components. It's useful for loading large components or third-party libraries on demand: `const MyComponent = dynamic(() => import('./MyComponent'), { loading: () => <p>Loading...</p> })`.

## Q22: What is the `_app.js` file in the Pages Router?
**A:** `pages/_app.js` is a custom App component that initializes pages. It's used to persist layouts between route changes, keep state, inject global styles, and pass data to all pages using props.

## Q23: What is the `_document.js` file in the Pages Router?
**A:** `pages/_document.js` customizes the HTML document structure (html, head, body tags). It runs server-side only and is used for adding fonts, meta tags, and other elements that should be in the HTML shell.

## Q24: How does Next.js handle CSS and styling?
**A:** Next.js supports CSS Modules (`*.module.css`), global CSS (imported in `_app.js` or root layout), CSS-in-JS libraries (styled-components, emotion), Tailwind CSS, Sass/SCSS (with `.scss` files), and CSS imports from node_modules.

## Q25: What is `next/head` and what does it do?
**A:** The `Head` component from `next/head` allows setting HTML head elements (title, meta, link, script) for each page. In the App Router, use the `metadata` API instead for better performance and SEO.

## Q26: What is the Metadata API in Next.js App Router?
**A:** The Metadata API allows defining SEO metadata (title, description, open graph, etc.) by exporting a `metadata` object or `generateMetadata` function from layout or page files. It's the preferred way over <Head> in the App Router.

## Q27: How do you configure Next.js with `next.config.js`?
**A:** `next.config.js` exports a configuration object for customizing Next.js behavior. Options include: `images` (remote patterns), `redirects`, `rewrites`, `headers`, `env`, `basePath`, `output` (standalone), `experimental` features, and more.

## Q28: What are environment variables in Next.js?
**A:** Next.js supports `.env.local`, `.env.development`, `.env.production` files. Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Others are only available on the server. Access via `process.env.VARIABLE_NAME`.

## Q29: What is the `public/` directory in Next.js?
**A:** The `public/` directory serves static assets (images, fonts, robots.txt) directly without processing. Files are served from the root URL. For example, `public/favicon.ico` is served at `/favicon.ico`.

## Q30: How do you implement authentication in Next.js?
**A:** Common approaches: NextAuth.js (Auth.js) for easy integration with multiple providers, Clerk for auth as a service, Lucia for flexible auth, or custom JWT-based auth. Middleware can protect routes, and Server Components check auth status.

## Q31: What is NextAuth.js (Auth.js)?
**A:** NextAuth.js is an authentication library for Next.js that supports OAuth (Google, GitHub, etc.), email/password, credentials, and database sessions. It provides APIs, middleware, and React hooks for authentication flows.

## Q32: How do you handle redirects in Next.js?
**A:** In the Pages Router, use `getServerSideProps` with a redirect return object or use `next.config.js` redirects. In the App Router, use `redirect()` function from `next/navigation` in Server Components or middleware.

## Q33: What is the `useRouter` hook?
**A:** `useRouter` (from `next/router` in Pages Router, `next/navigation` in App Router) provides access to the router object with properties like `pathname`, `query`, `asPath`, and methods like `push()`, `replace()`, and `back()` for programmatic navigation.

## Q34: What is the difference between `useRouter` from `next/router` and `next/navigation`?
**A:** `next/router` is used in the Pages Router (classic). `next/navigation` is used in the App Router and provides `useRouter()`, `usePathname()`, `useSearchParams()`, and `redirect()` — designed for Server and Client Components.

## Q35: What is `rewrites` in `next.config.js`?
**A:** Rewrites map an incoming request path to a different destination URL without changing the browser URL. They are useful for proxying API requests, implementing A/B testing, or rewriting legacy URLs.

## Q36: What is `redirects` in `next.config.js`?
**A:** Redirects map an incoming request path to a different destination URL and change the browser URL (HTTP redirect with 307/308 status codes). Used for URL structure changes, permanent redirects (301), or temporary ones (302).

## Q37: How does Next.js handle SEO?
**A:** Next.js provides SSR/SSG for search engine crawlers, the Metadata API for meta tags, sitemap generation (built-in via `sitemap.ts`), robots.txt (via `public/` or config), Open Graph images, and structured data (JSON-LD).

## Q38: What is the `generateStaticParams` function?
**A:** `generateStaticParams` (App Router) is the replacement for `getStaticPaths`. It returns an array of route parameter objects for dynamic routes to pre-render at build time, enabling ISR or SSG for dynamic pages.

## Q39: How do you create a sitemap in Next.js?
**A:** In the App Router, create `app/sitemap.ts` that exports a `generateSitemap` function returning an array of URL entries with `url`, `lastModified`, `changeFrequency`, and `priority`. Next.js automatically generates `/sitemap.xml`.

## Q40: What is `generateMetadata`?
**A:** `generateMetadata` is an async function exported from page or layout files that dynamically generates metadata (title, description, OG tags) based on route parameters, fetched data, or other context. It replaces custom `<Head>` usage.

## Q41: How do you implement i18n (internationalization) in Next.js?
**A:** Options include: built-in i18n routing (Pages Router via `next.config.js`), `next-intl` or `next-i18next` libraries for translations, and middleware-based routing for the App Router. Built-in i18n provides locale detection and URL-based locale prefixes.

## Q42: What is the difference between `next build` and `next start`?
**A:** `next build` compiles the application for production, generating optimized bundles, static pages, and server code. `next start` starts the production server using the built output from the `.next/` directory.

## Q43: What is `next dev`?
**A:** `next dev` starts the development server with hot module replacement (HMR), fast refresh for React components, helpful error overlay, and development-specific warnings. Not suitable for production.

## Q44: How does Next.js handle TypeScript?
**A:** Next.js has built-in TypeScript support. Create a `tsconfig.json` or rename files to `.tsx`/`.ts`, and Next.js auto-configures TypeScript. Zero-config setup with strict mode, path aliases, and type checking during build.

## Q45: What is `next/script`?
**A:** The `Script` component from `next/script` optimizes third-party script loading with strategies: `beforeInteractive` (load before page is interactive), `afterInteractive` (default — load after hydration), `lazyOnload` (load when idle), and `worker` (offload to Web Worker).

## Q46: What is `next/font`?
**A:** `next/font` automatically optimizes and self-hosts Google Fonts (and custom fonts), eliminating external requests and improving privacy. It supports `variable` fonts, subsets for smaller bundles, and CSS `size-adjust` to prevent layout shift.

## Q47: How do you create a 404 page in Next.js?
**A:** Create `pages/404.js` (Pages Router) or `app/not-found.js` (App Router). Next.js automatically serves this custom page for 404 errors. You can also return `notFound()` from a Server Component for conditional 404s.

## Q48: What is the `error.js` file in the App Router?
**A:** `error.js` defines an error boundary component that catches errors in the page and its children. It receives `error` and `reset` props. The `reset` function attempts to re-render the segment, providing a recovery mechanism.

## Q49: What is the `loading.js` file in the App Router?
**A:** `loading.js` creates a loading UI (suspense boundary) that is shown immediately when navigating to a route while the page content is being rendered server-side. It improves perceived performance with instant loading states.

## Q50: What are parallel routes in Next.js?
**A:** Parallel routes allow rendering multiple pages in the same layout simultaneously. Defined using slots (folders prefixed with `@`), like `@analytics` and `@team` inside a layout. Each slot renders independently, useful for dashboards.

## Q51: What are intercepting routes in Next.js?
**A:** Intercepting routes allow loading a route from another part of the app within the current layout context. Defined with `(.)` prefix for same level, `(..)` for parent level, `(..)(..)` for grandparent, or `(...)` for root level. Useful for modals.

## Q52: What is the `route groups` feature?
**A:** Route groups (folders named in parentheses like `(marketing)`) organize routes without affecting the URL structure. They allow using different layouts for different sections without nesting URL paths.

## Q53: How do you handle forms in Next.js?
**A:** In the App Router, use Server Actions (functions defined with `'use server'`) to handle form submissions directly on the server without creating API endpoints. Client forms can use controlled components, react-hook-form, or Formik.

## Q54: What are Server Actions in Next.js?
**A:** Server Actions are async functions marked with `'use server'` that run on the server. They can be called from Client Components or forms, enabling direct server-side data mutations without creating separate API routes.

## Q55: How do you handle file uploads in Next.js?
**A:** File uploads can be handled via Server Actions (receiving FormData), traditional API routes, or libraries like `uploadthing`, `Vercel Blob`, or `AWS S3` directly from the server. Client components use file inputs and FormData.

## Q56: What is the Edge Runtime in Next.js?
**A:** The Edge Runtime is a lightweight runtime based on Web APIs that runs at the edge (CDN nodes). Middleware runs on Edge Runtime by default. It's faster but has limitations (no Node.js APIs like fs, limited execution time).

## Q57: What is the difference between Edge Runtime and Node.js Runtime?
**A:** Node.js Runtime has full access to Node.js APIs (fs, path, process), supports any library, and has no timeout limits. Edge Runtime is lightweight, globally distributed, faster cold starts, but limited to Web APIs and has a 30s timeout.

## Q58: How do you deploy a Next.js application?
**A:** Next.js can be deployed to: Vercel (optimized platform by Next.js creators), Node.js servers (via `next start`), Docker containers, serverless platforms (AWS Lambda, Netlify), or static export (`output: 'export'` for fully static sites).

## Q59: What is the `output: 'standalone'` configuration?
**A:** When `output: 'standalone'` is set in `next.config.js`, Next.js creates a minimal standalone `/.next/standalone/` directory with only necessary files for production, reducing deployment size significantly. Optimized for Docker.

## Q60: How do you set up ESLint in Next.js?
**A:** Next.js comes with built-in ESLint. Run `next lint` to set up ESLint. The base config extends `next/core-web-vitals` or `next/typescript`. Custom rules can be added in `.eslintrc.json` or `eslint.config.js`.

## Q61: What are Next.js bundle analyzer tools?
**A:** `@next/bundle-analyzer` is a plugin that generates visual reports of JavaScript bundle sizes. Configure in `next.config.js` with `withBundleAnalyzer` to identify large dependencies and optimize bundle splits.

## Q62: How does Next.js handle image caching and optimization?
**A:** The Image component optimizes images on-the-fly using Sharp (server) or Squoosh (fallback). Optimized images are cached with Cache-Control headers. Remote images must be allowed via `images.remotePatterns` in config.

## Q63: What is the `onClick` behavior with `next/link`?
**A:** The `Link` component supports the `onClick` event. When a user clicks a link, Next.js performs client-side navigation (preventing full page reload), prefetches the target page, and updates the URL via the History API.

## Q64: How do you pass data between pages in Next.js?
**A:** Methods include: query parameters (in URL), `useRouter` with query (Pages Router), context/state management (React Context, Zustand, Redux), URL path parameters, cookies, or server-side data passing through getServerSideProps.

## Q65: What is `shallow routing` in Next.js?
**A:** Shallow routing (Pages Router) updates the URL without triggering data fetching (`getServerSideProps` or `getStaticProps` again). Useful for updating search params or filters without re-fetching page data.

## Q66: How do you handle SEO for client-rendered content?
**A:** Use the Metadata API for static SEO basics, dynamic metadata via `generateMetadata` for data-driven pages, and consider SSR or ISR for critical SEO pages. For highly dynamic content, ensure meta tags are set before rendering.

## Q67: What is the `useSearchParams` hook?
**A:** `useSearchParams` (from `next/navigation`) provides access to URL query parameters in the App Router. It returns a `URLSearchParams` instance, is read-only, and can be used in Client Components. It's the replacement for `useRouter().query`.

## Q68: What is the `useParams` hook?
**A:** `useParams` (from `next/navigation`) returns the dynamic route parameters for the current route. For route `/blog/[slug]`, `useParams()` returns `{ slug: 'value' }`. Works in both Server and Client Components in the App Router.

## Q69: How do you implement route handlers (API routes) with streaming?
**A:** Route handlers can stream responses by returning a `ReadableStream` or using `TextEncoder` encoding. Useful for real-time data, large file generation, or progressive responses. Edge Runtime supports Web Streams API.

## Q70: What is `next/og` for Open Graph images?
**A:** `next/og` (Vercel OG) dynamically generates Open Graph images using JSX and CSS. Create a route handler that returns an image with `ImageResponse`. Commonly used for auto-generating social share images per page.

## Q71: What is the Turbopack bundler and how does it relate to Next.js?
**A:** Turbopack is an incremental bundler written in Rust, developed by Vercel. It is the successor to Webpack for Next.js (available in Next.js 13+). It provides significantly faster module resolution, bundling, and Hot Module Replacement in development.

## Q72: How do you optimize fonts in Next.js?
**A:** Using `next/font/google` for Google Fonts (self-hosted, no external requests) or `next/font/local` for custom fonts. Fonts are automatically subsetted, preloaded with `link rel="preload"`, and CSS `size-adjust` prevents layout shift.

## Q73: What is the `amp` support in Next.js?
**A:** Next.js supports AMP (Accelerated Mobile Pages) through hybrid AMP (pages served as both AMP and HTML) or AMP-first mode. Configured per page or globally. Note: AMP is being phased out in favor of core web vitals.

## Q74: How do you implement custom server in Next.js?
**A:** Create a server file (e.g., `server.js`) that uses `next({ dev })` to create a Next.js app, `app.getRequestHandler()` to handle requests, and a custom HTTP/HTTPS server. This provides full control but loses automatic optimizations.

## Q75: What is `getInitialProps` in Next.js?
**A:** `getInitialProps` is the legacy data fetching method in the Pages Router. It runs on server for initial page load and client for subsequent navigations. It has been superseded by `getStaticProps` and `getServerSideProps`.

## Q76: How do you handle multiple layouts in Next.js?
**A:** In the App Router, layouts can be nested by creating multiple `layout.js` files in the route hierarchy. Route groups (`(group)`) allow different layouts for different sections without affecting URLs.

## Q77: What is `next/dynamic` vs regular import?
**A:** Regular imports are bundled eagerly. `next/dynamic` enables lazy loading — the component is loaded only when rendered. It supports SSR disabling (`ssr: false`), loading placeholders, and custom loading components.

## Q78: How do you handle cookies in Next.js?
**A:** In the App Router, Server Components and Route Handlers can use `cookies()` from `next/headers`. Client components use `document.cookie`. The `cookies()` function returns a `RequestCookies` object with get/set/delete methods.

## Q79: How do you handle headers in Next.js route handlers?
**A:** Route handlers receive a `NextRequest` object with `headers`. Server Components can use `headers()` from `next/headers`. To set response headers, return a `NextResponse` with headers or use middleware.

## Q80: What is the `NextResponse` object?
**A:** `NextResponse` extends the Web Response API with Next.js-specific methods: `NextResponse.next()` (continue), `NextResponse.redirect(url)` (redirect), `NextResponse.rewrite(url)` (rewrite). Used in middleware and route handlers.

## Q81: How do you handle errors in Server Components?
**A:** Use `error.js` files for error boundaries, `not-found.js` for 404s, `global-error.js` for root-level errors. In Server Components, throw or return errors; they propagate to the nearest error boundary. Use `try/catch` for expected errors.

## Q82: What is `revalidatePath` and `revalidateTag`?
**A:** `revalidatePath` and `revalidateTag` (from `next/cache`) are used for on-demand ISR. They allow purging cached data for specific paths or cache tags at runtime, enabling instant content updates without redeployment.

## Q83: What is `unstable_noStore` (now `connection`) in Next.js?
**A:** In Next.js 14+, `connection()` from `next/server` indicates that a page should not be cached (dynamic rendering). It was previously `unstable_noStore` and tells Next.js to skip static optimization for that page.

## Q84: What is the `export` function for static HTML export?
**A:** Setting `output: 'export'` in `next.config.js` generates a fully static site with HTML/CSS/JS files. No Node.js server is needed. Features like ISR, SSR, API routes, and middleware are not available in static export.

## Q85: How does Next.js handle React Strict Mode?
**A:** Strict Mode is enabled by default in `next dev` (since Next.js 13.5). It helps detect potential problems by double-invoking certain functions (like useEffect). Set `reactStrictMode: false` in `next.config.js` to disable.

## Q86: What is `Link` passHref prop?
**A:** The `passHref` prop on `Link` (Pages Router) forces the Link to pass its `href` to the child component. Useful when the child is a custom component that needs the href for accessibility or styling.

## Q87: How do you implement search functionality in Next.js?
**A:** Options include: client-side search (filtering loaded data), server-side search (API route or Server Action querying a database), Algolia or Meilisearch integration, or ISR-based static search indexes.

## Q88: What is `next/amp` for AMP pages?
**A:** `next/amp` provides the `useAmp` hook to detect if the page is served as AMP, and `withAmp` HOC to configure AMP behavior per page. AMP pages have strict HTML/CSS/JS constraints.

## Q89: How do you handle websockets in Next.js?
**A:** Next.js doesn't have built-in WebSocket support. Use a custom server with `ws` library, or deploy WebSocket server separately (e.g., Socket.io on a Node.js server, or a third-party service like Pusher).

## Q90: What is the `useEvent` hook (deprecated)?
**A:** `useEvent` was an experimental hook for wrapping callbacks with stable references. It was deprecated in favor of React's built-in patterns. It prevented unnecessary re-renders when passing callbacks to optimized components.

## Q91: How do you debug Next.js server-side code?
**A:** Use `NODE_OPTIONS='--inspect' next dev` and Chrome DevTools for Node.js debugging. Use `console.log` (output shows in server terminal), or VS Code debugger with a Node.js launch configuration.

## Q92: How do you handle environment-specific configurations?
**A:** Using `.env.development`, `.env.production`, and `.env.local` files. The `.env.local` overrides others and is not committed to git. Access in `next.config.js` via environment variables.

## Q93: What is `optimizeFonts` in `next.config.js`?
**A:** `optimizeFonts: true` (default) enables automatic font optimization using `next/font`. When disabled, fonts are handled manually. This optimization reduces bundle size and improves load performance.

## Q94: How do you create a PWA with Next.js?
**A:** Use `next-pwa` or `@serwist/next` packages. Add a service worker, manifest file, and configure caching strategies. The packages integrate with Next.js's build process to generate the service worker.

## Q95: What is the `trailingSlash` configuration?
**A:** `trailingSlash: true` in `next.config.js` appends a trailing slash to URLs (e.g., `/about/`). When false (default), URLs do not have trailing slashes. Affects routing and static export paths.

## Q96: How do you handle CORS in Next.js API routes?
**A:** In API routes or route handlers, set CORS headers manually (`Access-Control-Allow-Origin`, etc.) in the response. Use middleware for global CORS configuration, or the `cors` npm package.

## Q97: What is the `next start` port configuration?
**A:** Use the `-p` flag: `next start -p 3000`. Or set the `PORT` environment variable. The default port is 3000. For `next dev`, use `next dev -p 3001`.

## Q98: What is the React `cache` function in Next.js?
**A:** The `cache` function from `react` is used in Server Components to memoize data fetching results across renders within a single request. It prevents duplicate requests for the same data within a render pass.

## Q99: How do you handle deep linking in Next.js?
**A:** Deep linking works naturally with Next.js's file-based routing. Dynamic routes (`[id]`) map to specific URLs. On page load, the server renders the content based on the route params. Client-side navigation preserves this behavior.

## Q100: What are some common performance optimizations in Next.js?
**A:** Use Image component for images, next/font for fonts, dynamic imports for large components, ISR for semi-dynamic content, streaming (loading.js) for slow data, route prefetching, proper caching headers, bundle analysis, and static export when possible.
