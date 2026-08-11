# Priority 2 — Next.js (Q306–Q324)

**Why these matter for micro1:** the role explicitly lists React, Next.js, TypeScript for building Zara's frontend. Expect App Router / Server vs Client Components / data fetching / SSR, and how it connects to FastAPI.

---

## Q306: What is Next.js?

A **React framework** providing a full-stack foundation on top of React:

- **Rendering:** SSR, SSG/static, ISR, and client-side — per route/page.
- **Routing:** file-based (`app/` App Router since v13; `pages/` legacy).
- **Data fetching:** Server Components, `fetch` caching, Server Actions, route handlers.
- **Performance:** automatic code splitting, image/font optimization, streaming, `next/link` prefetching.
- **DX:** HMR, TypeScript out of the box, middleware, API routes/route handlers.
- **Deployment:** works as a full-stack app (Node) or static export; Vercel/AWS hosting.

For micro1: the AI recruiter's chat UI + dashboards, SSR for SEO/public pages, fast interactive chat.

---

## Q307: Why use Next.js instead of plain React?

| | **Plain React (SPA)** | **Next.js** |
|---|---|---|
| Rendering | Client-side only | SSR/SSG/ISR/CSR mix |
| SEO | Poor (empty HTML) | Great (server HTML) |
| First paint | JS-bundle dependent | Fast (server-rendered HTML) |
| Routing | External lib (react-router) | Built-in file routing |
| Data fetching | useEffect/query libs | Server Components, RSC, Server Actions |
| Code splitting | Manual | Automatic per route |
| Backend | Separate server | Route handlers + Server Actions |
| Images/fonts | Manual | Built-in `next/image`, `next/font` |

**Answer:** "Next.js gives SSR for SEO + performance, built-in routing and code-splitting, and lets the React app talk to the backend (or be the backend via route handlers) — the standard choice for production React apps, especially for micro1's public-ish recruiting product."

---

## Q308: What is the Next.js App Router?

The **modern routing system** (Next 13+) based on the `app/` directory, built on React Server Components and file-system conventions:

```
app/
  layout.tsx        # shared layout for children
  page.tsx          # route page ("/")
  loading.tsx       # loading UI (Suspense)
  error.tsx         # error UI (error boundary)
  not-found.tsx
  dashboard/
    layout.tsx
    page.tsx        # /dashboard
    [id]/page.tsx   # /dashboard/:id  (dynamic segment)
    loading.tsx
  api/
    route.ts        # route handler (API endpoint)
```

- **Conventions over config:** files define routes, layouts, loading/error boundaries, APIs.
- Features: nested layouts, parallel routes, intercepting routes, server + client components, streaming.
- Replaces the older `pages/` router (which still works in Next 13–14; removed in 15+).

---

## Q309: What are Server Components?

**React Server Components (RSC)** — components that render **on the server only**, shipping **zero JavaScript** to the client.

- Can be `async`, directly `await` DB/fetch/API calls, access secrets.
- Output is serialized HTML + a special payload; no client JS.
- **Cannot** use hooks (`useState`/`useEffect`), event handlers, or browser APIs.
- Default in the App Router — components are server unless marked.

```tsx
// server component (default in app/)
export default async function Page() {
  const jobs = await db.jobs.findMany();   // direct DB access!
  return <ul>{jobs.map(j => <li key={j.id}>{j.title}</li>)}</ul>;
}
```

**Benefits:** less JS, faster loads, better security (secrets stay server-side), and simpler data fetching.

---

## Q310: What are Client Components?

Components that render (and hydrate) **in the browser** — interactive UI with state/effects/events.

- Marked with `"use client"` at the top of the file.
- Still server-rendered for initial HTML in App Router (SSR), then hydrated client-side.
- Can use hooks, event handlers, browser APIs.
- **Cannot** directly access DB/secrets.

```tsx
"use client";
export function ChatInput({ onSend }: { onSend: (m: string) => void }) {
  const [text, setText] = useState("");
  return <input value={text} onChange={e => setText(e.target.value)}
               onKeyDown={e => e.key === "Enter" && onSend(text)} />;
}
```

---

## Q311: What does `"use client"` mean?

A directive at the top of a file marking it (and its imports) as **Client Components** — they execute in the browser and participate in interactivity.

- Server components are the default; `"use client"` opts *this module* into the client bundle.
- A client component can **import** server components? No — client components can't import server components (but can receive them as `children`/props from a server parent).
- Everything imported by a client component becomes client-side code.

**Answer:** "It's an opt-in boundary: it says 'this component (and its children that aren't themselves server components) runs in the browser,' enabling hooks and events."

---

## Q312: When should a component be a Client Component?

1. **Interactive:** buttons, inputs, forms, toggles, chat input, modals.
2. **Uses hooks:** `useState`, `useEffect`, `useRef`, `useContext`.
3. **Event handlers:** `onClick`, `onChange`.
4. **Browser APIs:** localStorage, geolocation, `window`/`document`, media.
5. **Third-party interactive libs:** charts, editors, carousels.

---

## Q313: When should a component be a Server Component?

1. **Static/content rendering** — headers, cards, lists of data fetched server-side.
2. **Data fetching** — direct DB/API access without exposing secrets; use `async` components.
3. **SEO-critical pages** — public content, candidate-facing pages.
4. **Large dependency, minimal interactivity** — keep heavy libs server-side (no client JS).
5. **Anything that doesn't need state/effects** — default to server; add `"use client"` only when needed.

**Golden rule:** **default to server components**; push interactivity to the smallest client islands.

---

## Q314: What is server-side rendering (SSR)?

Generating the **full HTML for a request on the server** and sending it to the browser; the client then **hydrates** (attaches React state/handlers to the existing markup).

- **Per-request** — fresh HTML for each request (dynamic).
- Benefits: fast first paint, SEO, works without JS initially.
- Costs: server compute per request; slower TTFB vs static.
- Next.js App Router: Server Components give you SSR automatically for dynamic pages; also `dynamic = "force-dynamic"` / `revalidate`.

```tsx
export const dynamic = "force-dynamic";   // SSR per request
```

- RSC + SSR combination: HTML from server components, minimal JS for client islands.

---

## Q315: What is static rendering?

Pre-generating HTML **at build time** and serving it as static files (also called SSG — static site generation).

- Fastest delivery (CDN-cacheable, no per-request compute).
- Content must be known ahead of time (blogs, docs, marketing).
- Next.js: pages without dynamic APIs are static by default; combine with **ISR** (`revalidate`) to refresh periodically.

```tsx
export const revalidate = 3600;   // ISR — regenerate at most every hour
```

- Tradeoff: staleness vs speed.

---

## Q316: What is dynamic rendering?

Rendering on the **server per request** using live data — needed for personalized/customized content (auth-gated dashboards, chat, candidate data).

- Next.js decides static vs dynamic: using `cookies()`, `headers()`, `searchParams`, or a dynamic API forces dynamic.
- Force it: `export const dynamic = "force-dynamic"`.
- **Streaming** lets dynamic pages send HTML progressively (skeleton + data as ready) — great UX for chat/dashboards.

**For Zara:** the recruiter's dashboard/chat is inherently dynamic; public marketing pages can be static/ISR.

---

## Q317: What are Next.js layouts?

Layout components that **wrap** pages and **persist across navigation** (they don't re-render/remount when switching child pages).

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>{children}</main>
    </div>
  );
}
```

- **Nested layouts** (root layout → segment layouts) compose naturally.
- State persists across route changes inside a layout → no refetch of shared UI.
- Layouts can be server or client; root layout is required (wraps `<html>`/`<body>`).

---

## Q318: How does routing work in Next.js?

**File-system routing.** Files in `app/` map to URL paths:

| File | URL |
|---|---|
| `app/page.tsx` | `/` |
| `app/dashboard/page.tsx` | `/dashboard` |
| `app/dashboard/[id]/page.tsx` | `/dashboard/:id` |
| `app/dashboard/[...slug]/page.tsx` | `/dashboard/a/b/c` (catch-all) |
| `app/(marketing)/about/page.tsx` | `/about` (route group, no URL segment) |

- **Dynamic segments** in brackets `[id]` → `params.id` in the page.
- Navigation with `next/link` (`<Link href="/dashboard">`) — client-side, prefetch.
- `usePathname()`, `useSearchParams()` (client) / `searchParams` prop (server) for query strings.
- Parallel routes (`@slot`) and intercepting routes (`(.)`) for advanced patterns.

---

## Q319: How do you handle loading states in Next.js?

**Built-in Suspense conventions:**
- `app/dashboard/loading.tsx` — automatically shown while a route's server component is pending (wraps the page in Suspense).
- `<Suspense fallback={<Skeleton/>}>` around individual async components/segments → **streaming**: HTML with placeholders arrives, data fills in.

```tsx
// app/dashboard/page.tsx
export default function Page() {
  return (
    <Suspense fallback={<SkeletonList />}>
      <CandidateTable />     {/* async server component */}
    </Suspense>
  );
}
```

- For client data fetching: React Query's `isLoading` + skeletons (Q199).
- `loading.tsx` per segment gives progressive streaming down the tree.

---

## Q320: How do you handle errors in Next.js?

- **`app/error.tsx`** — per-segment **error boundary** UI (catches render errors in client components; must be a client component, receives `error` + `reset`).

```tsx
"use client";
export default function ErrorBoundary({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

- **`app/global-error.tsx`** — root-level error boundary.
- **`app/not-found.tsx`** — 404 page; `notFound()` throws to render it.
- **Route handlers / API errors** — return proper `Response`/JSON with status codes.
- **Data errors in server components** — catch and render friendly UI (or throw → error.tsx).
- **Logging** — log to your monitoring stack (Q628–635).

---

## Q321: How do you fetch data in Next.js?

**In Server Components (recommended):** just `await` — direct DB or API calls, no client state.

```tsx
export default async function Jobs() {
  const res = await fetch(`${API}/jobs`, { next: { revalidate: 60 } });
  const jobs = await res.json();
  return <JobList jobs={jobs} />;
}
```

- **Client-side** (for interactivity/caching): TanStack Query (React Query) in client components.
- **`fetch` caching** — default cached (static); `{ next: { revalidate } }` for ISR; `{ cache: "no-store" }` for dynamic.
- **Route Handlers** (`app/api/route.ts`) — build API endpoints that proxies to FastAPI (Q322, Q324).
- **Server Actions** — mutations directly from forms/buttons (call backend, revalidate).
- **Best practice for Zara:** server components for page data; React Query for chat/interactive data; route handlers or direct fetch to FastAPI.

---

## Q322: What are route handlers?

API endpoints defined as **files** in the App Router — a way to write backend logic in Next.js without a separate server.

```ts
// app/api/chat/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = await req.json();
  const reply = await callFastAPI(body);
  return NextResponse.json(reply);
}

export async function GET() { ... }
```

- Each HTTP method is an exported function (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`).
- Support streaming responses (`new Response(stream)`) — used for proxying LLM/SSE streams (Q399).
- Useful for: auth cookie helpers, BFF (backend-for-frontend) proxying to FastAPI, webhooks.
- **They run on the server** — secrets stay server-side.

---

## Q323: How do you optimize performance in Next.js?

1. **Server Components by default** — ship less JS.
2. **Code splitting** — automatic per-route; lazy-load client islands only where interactive.
3. **Streaming + Suspense** — fast first paint (loading.tsx, `<Suspense>`).
4. **Caching strategy** — static/ISR where possible; `revalidate` for semi-dynamic; dynamic only when needed (Q314–316).
5. **`next/image`** — automatic optimization, lazy loading, proper sizing.
6. **`next/font`** — self-hosted, no layout shift.
7. **Link prefetching** — `<Link>` prefetches visible routes.
8. **Middleware/edge** — run lightweight logic at the edge (redirects, geolocation).
9. **Avoid client-heavy libs** on server pages; React Query caching for client data.
10. **Measure** — Lighthouse/Web Vitals (LCP/INP/CLS), bundle analyzer; optimize what's measured.

---

## Q324: How would you integrate a Next.js frontend with FastAPI?

**Clean separation via HTTP + API client:**

1. **Backend (FastAPI):** owns data + business logic + auth; CORS configured for the Next.js origin (Q66).

```python
app.add_middleware(CORSMiddleware, allow_origins=["https://app.micro1.ai"], allow_credentials=True, ...)
```

2. **Frontend API layer:** a typed client (OpenAPI-generated types, Q242) using `fetch`/axios with auth headers.

```ts
// lib/api.ts
const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL, timeout: 30_000 });
api.interceptors.request.use(cfg => { cfg.headers.Authorization = `Bearer ${getToken()}`; return cfg; });
```

3. **Fetch patterns:**
   - **Server Components** → `await fetch(API_URL + "/candidates")` server-side (SSR) with revalidate.
   - **Client interactive (chat)** → TanStack Query in client components, or fetch in event handlers.
   - **Route Handlers (BFF)** → Next.js proxies/adapts to FastAPI when you need to add server-only logic (token injection, transformation, streaming proxy) (Q322).
4. **Auth:** FastAPI issues JWT (Q62); Next.js stores/uses it (HTTP-only cookie for SSR, or Authorization header client-side) (Q408–411).
5. **Streaming:** FastAPI SSE → Next.js Route Handler or direct `fetch` with `ReadableStream` → chat UI (Q399).
6. **Deploy:** FastAPI (ECS/Lambda/EKS, Q364) + Next.js (Vercel/ECS/CloudFront, Q365) — separate domains or same via reverse proxy.
7. **Env config:** `NEXT_PUBLIC_API_URL`, API secrets only in server env (Q69–70).
