# Priority 4 — Advanced React (Q569–Q588)

**Why these matter for micro1:** deeper React questions show up in senior full-stack rounds. Expect reconciliation, stale closures, hooks pitfalls, race conditions, memoization, and state management philosophy.

---

## Q569: What is reconciliation in React?

**Reconciliation** = the algorithm React uses to **diff the virtual DOM** against the previous one and figure out the minimal set of DOM operations to apply.

**How it works:**
1. React builds a **virtual DOM** (plain JS objects) from components each render.
2. On state/props change, it builds a new tree and diffs it against the previous tree.
3. **Diffing rules (heuristics — React is NOT a general tree-diff, it's O(n) by assumption):**
   - **Same element type + same position** → update in place (re-render that component).
   - **Different element type** → unmount old subtree, mount new (state is lost).
   - **Keys** on lists identify which items changed/moved (Q572).
4. Result is a list of DOM updates applied in the **commit phase** (Q570).

**Why it matters:** understanding reconciliation explains *why* state resets when types change, *why* keys matter, and *why* inline objects cause re-renders.

---

## Q570: What is the React Fiber architecture?

**Fiber** (React 16+) — the **reconciler rewrite** that makes rendering *interruptible* and *prioritizable*.

**Core ideas:**
- **Unit of work = a Fiber node** — a JS object per component/instance with the component, props, state, and links to parent/sibling/child (a linked tree, not a recursive call stack).
- **Two phases:**
  - **Render phase** — builds the work tree, is **interruptible** (can yield to the browser → better perceived performance, time-slicing).
  - **Commit phase** — applies DOM mutations, **not interruptible** (must be atomic).
- **Priorities:** urgent updates (input, click) can preempt low-priority ones (list rendering, async data).
- Enables **Concurrent Features**: `startTransition`, `useDeferredValue`, `Suspense` — keep the UI responsive during big updates.
- **Effects** (useEffect/useLayoutEffect) are scheduled in Fiber; `useLayoutEffect` runs synchronously after DOM mutations, `useEffect` async after paint.

**Interview answer:** "Fiber is React's incremental reconciler — a tree of fibers processed in interruptible chunks, with a two-phase (render/commit) model that enables time-slicing and concurrent features."

---

## Q571: Why does React need keys? What happens without them?

**Keys** tell reconciliation *which items in a list correspond to which* — enabling correct reordering, reuse, and state preservation (Q569, Q572).

```jsx
{candidates.map(c => <CandidateCard key={c.id} candidate={c} />)}
```

**Without (good) keys:**
- React matches items **by index/position** → when the list reorders/inserts, components get **wrong props** and **state leaks across items** (an expanded card, a draft input, scroll position moves to the wrong item).
- **Incorrect DOM reuse** → visual bugs and wasted re-renders.

**Key rules:**
- Use a **stable unique id** from data (`candidate.id`) — never `index` for dynamic lists, never random values (they change every render → remount everything).
- Keys only need to be unique among **siblings**.
- The key must be a **string/number**; an object breaks reconciliation (stringifies to `[object Object]`).

---

## Q572: How do you avoid unnecessary re-renders?

1. **Memoize the right things:**
   - `React.memo(Component)` — skip re-render when props are shallow-equal.
   - `useMemo` — expensive computed values; keep references stable.
   - `useCallback` — stable function references so memoized children don't re-render.
2. **Stable props:** don't pass new inline objects/arrays/functions each render (`{...}` → new ref every time defeats memo).
3. **State colocation:** keep state as close as possible to where it's used; don't lift everything to the top (Q201).
4. **Context wisely:** context changes re-render *all* consumers — split contexts, memo provider values.
5. **Avoid the "anonymous function in JSX" pitfall** where it matters (not always — modern React handles inline props okay, but memoized children care).
6. **`useDeferredValue`/`startTransition`** for expensive derived UI (search-as-you-type) to keep typing responsive.
7. **Don't over-memoize:** React's diff is fast; memo has a cost. Profile (React DevTools Profiler) before wrapping everything.

**The golden rule:** keep *references* stable and *state* local; memoize children that are expensive to render or frequently re-rendered.

---

## Q573: What is a stale closure? How do you avoid it?

**Stale closure** = a function (effect callback, event handler, `setTimeout`) that "remembers" an **old snapshot** of state/props because it was created in an earlier render.

```jsx
function Chat() {
  const [messages, setMessages] = useState([]);
  useEffect(() => {
    const id = setInterval(() => {
      console.log(messages.length);      // ❌ always 0 — this closure captured the first render's value
    }, 1000);
    return () => clearInterval(id);
  }, []);                                 // deps: [] → effect never re-runs
}
```

**Fixes:**
1. **Add the dependency** to the effect array (`[messages]`) — re-create the effect when it changes.
2. **Functional updates** — `setMessages(m => [...m, next])` reads the latest state without depending on it.
3. **`useRef`** — hold the latest value in a ref and read `.current` inside callbacks.
4. **`useReducer`** if multiple state values must stay in sync.

**Diagnosis skill:** if a timer/websocket/handler "always sees the first value", it's a stale closure — the closure was created once, before the value changed. Grep for `[]` deps + callbacks reading state.

---

## Q574: What is a race condition in React? How do you handle it?

**Race condition** = a slower earlier request overwrites the result of a faster later one — classic with async fetches in effects.

```jsx
// ❌ user types "a" → request A, then "ab" → request B
// B returns first; then A returns → UI shows stale result for "a"
useEffect(() => {
  let cancelled = false;
  fetch(`/search?q=${query}`).then(r => r.json())
    .then(data => { if (!cancelled) setResults(data); });   // guard
  return () => { cancelled = true; };                        // cleanup on unmount/re-run
}, [query]);
```

**Patterns:**
1. **Cancellation flag in cleanup** (above) — the standard effect-safe pattern.
2. **AbortController** — actually cancel the fetch (`controller.abort()` in cleanup) — saves bandwidth too.
3. **Sequence token / "latest wins"** — keep a ref of the latest request id; ignore stale responses.
4. For custom async (React Query), the library handles it — use `useQuery` with query keys (cancel/stale-invalidation built in).

**Apply to your app:** the AI chat — user sends a message while the previous turn is still streaming → guard the stream handler, or the UI mixes turns (Q441-style client-side sequencing).

---

## Q575: What is the difference between `useEffect`, `useLayoutEffect`, and `useInsertionEffect`?

- **`useEffect`** — runs **after** the browser paints (async). Default choice for side effects (data fetching, subscriptions, timers). Doesn't block paint.
- **`useLayoutEffect`** — runs **synchronously after DOM mutations but before paint**. Use when you must measure/read the DOM and mutate it before the user sees it (avoid flicker): measuring layout, positioning tooltips, scroll restoration. Blocks paint (avoid unless needed).
- **`useInsertionEffect`** (React 18+) — runs **before** any DOM mutation. For **CSS-in-JS** libraries injecting styles; never read DOM here. Almost never used directly in app code.

**Decision:** network/IO → `useEffect`; DOM-measure-then-adjust that would flicker → `useLayoutEffect`; style injection → `useInsertionEffect`. On SSR, `useLayoutEffect` warns — guard with a mounted check if needed.

---

## Q576: How does React batching work?

**Batching** = React groups multiple state updates into **one re-render**.

- **Legacy:** updates inside React events (onClick) are batched; async contexts (promises, setTimeout, native events) were **not** batched.
- **React 18+:** **automatic batching everywhere** — inside promises, timeouts, native handlers, and async callbacks, updates are batched. `setA(1); setB(2);` → one render.

```jsx
function handleClick() {
  setLoading(true);      // batched → single re-render with both changes
  setError(null);
}
```

**Why it matters:**
- Predictable renders, fewer wasted re-renders, less flicker.
- If you ever need the *latest* state *between* updates, use a functional update or `flushSync` (rare — and `flushSync` disables batching, so use sparingly).
- With `useState`, consecutive `setCount(c => c+1)` functional updates each get the latest value — batching doesn't lose updates, it just renders once.

---

## Q577: What are controlled vs uncontrolled components?

- **Controlled:** the input's value **comes from React state**; every change flows through `onChange` → `setState` → re-render. React is the single source of truth.
```jsx
<input value={title} onChange={e => setTitle(e.target.value)} />
```
- **Uncontrolled:** the input **owns its value in the DOM**; read it imperatively via `ref`.
```jsx
const ref = useRef(null);
<input ref={ref} defaultValue="hi" />   // ref.current.value
```

**Rules:**
- **Controlled** for anything you validate, transform, or need the value of (almost everything — forms in your app).
- **Uncontrolled** for performance-sensitive, ephemeral fields, or integrating non-React libraries; or file inputs (`<input type="file">` is effectively uncontrolled).
- **Golden rule:** never mix — a component should be either fully controlled or fully uncontrolled (error: "changing an uncontrolled input").

---

## Q578: What is the React Context API, and what are its limitations?

**Context** provides values to a whole subtree **without prop drilling**: `createContext` → `<Provider value>` → `useContext`.

```jsx
const AuthCtx = createContext(null);
<AuthCtx.Provider value={{ user, login, logout }}>
  <App />
</AuthCtx.Provider>
// deep child:
const { user } = useContext(AuthCtx);
```

**Limitations:**
1. **Performance:** when the value changes, **every consumer** re-renders — even those not using the changed field. Fix: split contexts, memo the provider value (`useMemo`), or accept the granular re-render.
2. **Not for high-frequency updates** — live timers/counters in context = constant subtree re-render. Use local state or a store.
3. **No selectors/optimization built in** — `useContext` gives the whole value, not a slice (React 19's `use` still exposes the whole context).
4. **Hard to test/debug** — consumers need a provider wrapper.

**When to use:** auth/session, theme, i18n, feature flags — low-churn, read-heavy, subtree-wide values. When to not: frequently changing values, complex interdependent state (→ a store, Q582).

---

## Q579: What is `useMemo` vs `useCallback` vs `memo`?

- **`useMemo`** — caches a **computed value** between renders (`useMemo(() => expensive(a,b), [a,b])`).
- **`useCallback`** — caches a **function reference** (`useCallback(() => doThing(x), [x])`) — `useMemo(() => fn, deps)` sugar.
- **`React.memo(Comp)`** — **component-level**: skips re-rendering `Comp` if props are shallow-equal.

```jsx
const memoizedScore = useMemo(() => computeScore(cand, job), [cand, job]);
const onShortlist = useCallback((id) => shortlist(id), []);
const MemoCard = React.memo(CandidateCard);
```

**When each matters:**
- `useMemo` — expensive derived data (parsing, filtering 10k items).
- `useCallback` — passing handlers to **memoized** children (otherwise the new function ref defeats `memo` every render).
- `memo` — components that re-render often with unchanged props (list rows).

**Anti-patterns to name:** over-memoizing (cost > benefit); stale deps (missing deps → stale closure, Q573); using `useMemo` as a premature optimization without profiling.

---

## Q580: What is a `key` when using React Router / mapping? (Bonus: reconciliation with keys)

Already covered in Q571 — key extras for the interview:

- **Router:** using `key` on routed components resets their state when the path/param changes: `<CandidateDetail key={id} id={id} />` forces a remount (clears local state) when navigating candidate → candidate. Useful when the param changes but the component type doesn't.
- **Lists:** keys also enable **animation/transition** libs and correct `React.memo` reuse.

---

## Q581: How do you manage forms in React (large/complex)?

**Options, in order of complexity:**
1. **Controlled inputs + local state** — fine for small forms (Q577).
2. **A forms library (react-hook-form)** — recommended for real forms:
   - **Uncontrolled-ish internals** → less re-rendering per keystroke (perf win).
   - **Built-in validation** (zod resolvers) with minimal code.
   - **Dirty/touched/submitting state**, arrays of fields, dynamic fields.
   - Easy **default values** + **reset** on submit.
3. **Formik** — heavier, fully controlled, more boilerplate; older alternative.

**Your app:** the candidate application form + recruiter job form → react-hook-form + zod schema shared with the FastAPI Pydantic model (single source of truth for validation!).

**Best practices:** disable submit while submitting (double-submit, Q396), optimistic UI optional, persist draft to state/DOM before navigation.

---

## Q582: React state management: when to use Context vs a store (Redux/Zustand/Jotai)?

| | **Context** | **Store (Zustand/Redux/Jotai)** |
|---|---|---|
| Frequency | Low-churn, subtree-wide | Any frequency |
| Re-render scope | Whole subtree on change | Only subscribed selectors |
| Middleware/time-travel/devtools | Manual | Built-in (Redux DevTools) |
| Boilerplate | None | Redux: high; Zustand/Jotai: low |
| Testability | Provider wrapper needed | Standalone store |

**Decision guide:**
- Auth, theme, i18n, flags → **Context** (Q578).
- Frequently-changing, complex, cross-cutting state (chat messages, connection status, many components subscribe) → **store**. **Zustand** (minimal, selector-based, easy) is a great default; Redux when you want strict discipline + DevTools; Jotai for atomic/derived state.
- **Server state ≠ client state:** use **TanStack Query** for API data (caching, refetch, invalidate) — most "state management" in a real app is server data, and Query solves it better than any client store (Q251).

---

## Q583: What is React Server Components (RSC)? How do they work in Next.js?

**RSC** — components that run **on the server only** and render to a **special RSC payload** (not HTML) streamed to the client, which can be composed with client components.

**Key properties (App Router, Q307):**
- **Server Components:** async, can `await` the DB/API directly, **zero JS shipped** to the client, **no hooks/state** (render-only), no browser APIs. Rendered per-request (or cached — Next.js caching Q312).
- **Client Components** (`"use client"`): run in the browser, have state/effects/handlers. They're still SSR'd for initial HTML.
- **Composition rule:** server components can render client components; client components **can't import server components** — pass server data as **props** or via **children/slots**.

```tsx
// page.tsx (server) — direct DB access, no API layer needed for reads
export default async function JobPage({ params }) {
  const job = await db.getJob(params.id);       // runs on server
  return <JobCard job={job}><Comments jobId={job.id} /></JobCard>;
}
```

**Tradeoffs:** great for SEO/perf and data-fetching simplicity; but you must respect the server/client boundary, manage what serializes over the wire (props must be serializable), and know the caching semantics (Q312).

---

## Q584: How does SSR work? CSR vs SSR vs SSG?

- **CSR:** browser downloads JS bundle → renders on the client. Fast interactions after load; bad initial paint/SEO.
- **SSR:** server renders HTML per request → sends HTML + hydration; good SEO/first paint, slower TTFB, server cost per request.
- **SSG:** pre-render at **build time** to static HTML/CDN; fastest, but stale unless ISR (incremental static regeneration, Q314).

**SSR flow (Next.js):** request → server runs the React tree → HTML streamed to client → JS loads → **hydration** (React attaches event handlers/state to the existing HTML, making it interactive).

**Hydration pitfalls (deep answer):** mismatched server/client HTML (e.g., `Date.now()`, `Math.random()` differ) → React discards/re-renders → flicker + console warnings; use `suppressHydrationWarning` or defer to a mounted effect.

**Choice:** marketing/SEO pages → SSG/ISR; user dashboards with fresh data → SSR or CSR+loading; your recruiter dashboard → SSR for initial HTML + client-side fetch for live updates (Q312–315).

---

## Q585: What is Suspense and how does it work?

**Suspense** lets a component **"wait"** for async data with a **fallback UI**, without blocking the rest of the tree.

```jsx
<Suspense fallback={<Spinner />}>
  <ScreeningResults candidateId={id} />   {/* suspends until data loads */}
</Suspense>
```

**How it works:**
- A component that **suspends** (throws a promise — typically via a framework like TanStack Query/SWR, or Next.js with async server components) tells React "I'm not ready."
- React unwinds to the nearest `<Suspense>` boundary and renders its **fallback**.
- When the promise resolves, React **retries** the suspended part.
- **Multiple boundaries** = independent loading states; nested Suspense = progressive rendering (headers/pages stream in as their data resolves).

**Streaming SSR (Next.js):** with `loading.tsx`/`Suspense`, the server streams HTML shell first, then each suspended section as data arrives — your AI chat could stream "thinking..." states. **Error handling:** combine with error boundaries for per-section fallbacks.

---

## Q586: What are hooks rules? What happens when you break them?

**Rules of Hooks (from React docs):**
1. **Only call hooks at the top level** — not inside loops, conditions, or nested functions.
2. **Only call hooks from React functions** — components or custom hooks (not plain JS, not event handlers... actually callbacks are fine as *calls*, but hooks themselves can't be inside).

**Why (the deep answer):** React matches a hook call to a state slot **by order of calls** within a component (a linked list of hook nodes stored on the Fiber, Q570). If a hook is called conditionally, the order shifts on re-render → React pairs the wrong state → **bugs, `Rendered fewer hooks than expected`, or crash**.

```jsx
if (cond) { const [x] = useState(0); }   // ❌ hook order changes between renders
```

**Custom hooks:** must call real hooks at their top level; name them `useX` so lint rules catch violations. ESLint `react-hooks/rules-of-hooks` + `exhaustive-deps` are non-negotiable on real projects.

---

## Q587: What is a custom hook? Give an example relevant to your app.

**Custom hook** = a function (starts with `use`) that **reuses stateful logic** by composing built-in hooks.

```tsx
function useStreamingChat(interviewId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [status, setStatus] = useState<"idle"|"streaming"|"done">("idle");

  const send = useCallback(async (text: string) => {
    setStatus("streaming");
    const res = await fetch(`/api/interviews/${interviewId}/stream`, {
      method: "POST", body: JSON.stringify({ text }),
    });
    const reader = res.body!.getReader();          // parse SSE chunks
    const decoder = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      setMessages(m => [...m, decoder.decode(value)]);   // incremental append
    }
    setStatus("done");
  }, [interviewId]);

  return { messages, status, send };
}
```

**Why they matter:** abstraction + testability — extract timers, subscriptions, async flows, DOM/lifecycle logic into hooks; test with `renderHook` (Q461). Custom hooks are the modern React "utility belt."

---

## Q588: How do you optimize a React app for performance? (full answer)

1. **Measure first:** React DevTools **Profiler** — find the expensive commits; Lighthouse/Web-Vitals for real metrics (LCP/INP/CLS).
2. **Reduce renders:** state colocation (Q572), memoized children/values (Q579), stable references.
3. **Code-splitting + lazy loading:** `next/dynamic` / `React.lazy` for routes and heavy components (charts, markdown renderers) → smaller initial bundles.
4. **Bundle analysis:** `next build --analyze` / source-map-explorer — kill duplicate/oversized deps; tree-shaking.
5. **Images/assets:** CDN, `next/image` optimization, lazy loading, correct sizes (Q247).
6. **Lists:** virtualization (`react-window`/`tanstack-virtual`) for 1000s of rows (candidate lists).
7. **Avoid blocking main thread:** `useDeferredValue`/`startTransition` for expensive derived UI; defer non-critical effects.
8. **Server-side wins:** RSC/SSR to ship less JS (Q583); caching strategy (Q312).
9. **Network:** reduce round trips (React Query caching, batching endpoints, `@tanstack/react-query` prefetching).
10. **Cache-control/CDN** for static assets; streaming for long payloads (SSE, Q399).

**Answer structure:** "Profile → then target: render count, bundle size, images, lists, blocking work, then the server/caching side — in that order."
