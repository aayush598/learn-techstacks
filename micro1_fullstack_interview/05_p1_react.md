# Priority 1 — React (Q176–Q215)

**Why these matter for micro1:** the role requires React + Next.js + TypeScript for the AI recruiter's frontend (chat UI, candidate dashboards). Expect component/hooks questions, then a drill on re-renders and performance.

---

## Q176: Tell me about your experience with React.

**Answer framework:**
1. **Years + types of apps:** "X years building SPAs and SSR apps with React — dashboards, chat UIs, forms-heavy tools, data tables."
2. **Modern React:** function components + hooks, TypeScript, TanStack Query, Next.js App Router.
3. **State:** local state, context, server-state caching (React Query), occasionally Zustand/Redux.
4. **Quality:** component testing (Testing Library), re-render/perf optimization (memoization, code splitting).
5. **Your project:** name the frontend you're proudest of; tie to the AI recruiter (chat interface, streaming messages, live dashboards).

> Follow-up prep: "how do you avoid unnecessary re-renders?", "how do you handle a large list?", "how do you structure state?"

---

## Q177: What is React?

A **JavaScript library for building user interfaces** — component-based, declarative, view-focused (a library, not a full framework like Angular).

- **Declarative:** you describe *what* the UI should look like for a given state; React updates the DOM for you.
- **Component-based:** small reusable pieces (functions returning JSX).
- **Virtual DOM + reconciliation** for efficient updates (Q569–572).
- **Unidirectional data flow:** parent → child via props; state changes trigger re-render.
- Runs on the client (SPA) or server (SSR via Next.js/Remix); can render to DOM, native (React Native), canvas, etc.

---

## Q178: Why use React?

1. **Developer velocity** — declarative components, huge ecosystem, fast iteration.
2. **Reusability & maintainability** — composable components; hooks extract shared logic.
3. **Performance** — virtual DOM diffing, memoization, code splitting.
4. **Ecosystem** — Next.js, React Query, Testing Library, component libraries, Tailwind.
5. **Team hiring & community** — massive talent pool, long-term support.
6. **Flexibility** — adopt as much/little as needed; works with CSR/SSR/SSG.
7. **TypeScript support** — excellent typing for components/hooks.
8. For micro1: chat interfaces (streaming LLM), dashboards, forms — all React strengths.

---

## Q179: What is a React component?

A function (or class) that returns **UI (JSX)** — the atomic building block of a React app.

```jsx
function UserCard({ user }) {
  return <div className="card"><h2>{user.name}</h2></div>;
}
```

- **Props in, UI out:** components are pure-ish — same props + state → same output.
- **Composition:** components nest (`<Layout><Sidebar/></Layout>`).
- Two kinds today: **function components** (with hooks) — the standard; class components (legacy, `this.state` + lifecycle).
- Server vs Client Components in Next.js (Q309–313) — a modern distinction.

---

## Q180: What is JSX?

JavaScript **syntax extension** that looks like HTML but compiles to React element calls.

```jsx
const el = <h1 className="title">Hello {name}</h1>;
// ≈ React.createElement('h1', { className: 'title' }, `Hello ${name}`)
```

- **Expressions in braces:** `{expr}` — variables, ternaries, function calls.
- Attributes use camelCase (`className`, `onClick`, `htmlFor`).
- **Not a string, not HTML** — it's JS producing objects; values are escaped by default (injection-safe; `dangerouslySetInnerHTML` opts out).
- Requires a compiler (Babel/SWC/esbuild).

---

## Q181: What are props?

**Properties** — read-only data passed from a parent to a child component.

```jsx
function Greeting({ name }) { return <p>Hello {name}</p>; }
<Greeting name="Ada" />
```

- **Immutable** — a component must never mutate its own props.
- Flow is **top-down** (unidirectional).
- `props.children` for nested content.
- New props from parent trigger re-render of the child.

---

## Q182: What is state?

**Mutable, component-owned data** that, when changed, causes the component to re-render.

```jsx
const [count, setCount] = useState(0);
```

- Local to the component (or lifted/hooked via context/store for sharing).
- Changing state **schedules a re-render**; the UI always reflects current state.
- `useState` holds one value; `useReducer` for complex transitions.
- Server state (API data) is not the same as client state (Q585) — handle separately.

---

## Q183: What is the difference between props and state?

| | **Props** | **State** |
|---|---|---|
| Owned by | Parent (passed down) | The component itself |
| Mutability | Immutable (read-only) | Mutable via setter |
| Triggers re-render | Yes, when parent re-renders/passes new value | Yes, when setter called |
| Purpose | Configuration/input | Internal, dynamic data |

```jsx
function Counter({ step }) {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + step)}>{count}</button>;
}
```

Rule of thumb: **props flow down, state is owned locally** (or lifted up when shared, Q210).

---

## Q184: How does state update work in React?

1. You call the setter (`setCount(5)` or `setCount(c => c + 1)`).
2. React **schedules** a re-render (updates are **batched** — multiple setState calls in one handler → one render).
3. On the next render, React computes the new UI, **diffes** (reconciliation) against the previous virtual DOM, and **commits** only the changed DOM nodes.
4. Functional updates (`c => c + 1`) are safest when the new value depends on the previous one.

```jsx
const [count, setCount] = useState(0);
setCount(count + 1); setCount(count + 1);  // still 1 — count not updated yet (batched)
setCount(c => c + 1); setCount(c => c + 1); // → 2 — correct
```

- State is a **snapshot at render time** — closures capture the render's value (Q574 stale closures).

---

## Q185: What causes a React component to re-render?

1. **Parent re-renders** — child re-renders unless memoized (Q209).
2. **Its own state changes** — setState/useReducer dispatch.
3. **Context value changes** — every consumer re-renders.
4. **Props change** — new props (different reference/values).
5. **Force render** — `forceUpdate()` (class), or changing a hook key.

Re-render ≠ DOM update: React re-runs the component function; only changed DOM nodes are committed. But re-rendering 10k rows still costs JS time → memoize, split components, virtualize.

---

## Q186: What is conditional rendering?

Showing different UI based on a condition — plain JS, no special syntax.

```jsx
{isLoading && <Spinner/>}
{error ? <ErrorView msg={error}/> : null}
{user ? <Dashboard user={user}/> : <LoginForm/>}
{role === "admin" && <AdminPanel/>}
```

- `&&` short-circuits (careful: `0 && x` renders `0` — coerce to boolean with `!!`).
- Ternary and early returns (`if (loading) return <Skeleton/>`) are common patterns.

---

## Q187: How do you render a list in React?

Use `.map()` returning elements with a **unique `key`**:

```jsx
<ul>
  {users.map(u => <li key={u.id}>{u.name}</li>)}
</ul>
```

- **Filter before map:** `users.filter(x => x.active).map(...)`.
- Empty state: `{users.length === 0 && <p>No users</p>}`.

---

## Q188: Why does React require keys when rendering lists?

**Keys tell React which list items changed**, so it can reconcile efficiently instead of re-creating everything.

- A stable key identifies each element across renders → React can **reorder, add, remove** items by *moving* DOM nodes instead of rebuilding them.
- Without keys, React matches by index → wrong DOM reuse, broken state (e.g., an input's local state follows the *position*, not the item).
- **Best practice:** use stable unique ids (`item.id`). Don't use the array index (Q189).

---

## Q189: What happens if you use an array index as a key?

- **Unstable identity:** when items are inserted/removed/reordered, indexes shift → React reuses the wrong component instances.
- Symptoms: **wrong local state, broken inputs, wrong animations** — e.g., item B's checkbox state moves to item C after a deletion.
- Also problematic: index keys make reconciliation a full rebuild (no reorder optimization).
- Acceptable **only** for a static, never-reordered list (or when items have no state).

---

## Q190: What is a controlled component?

A form input whose **value is controlled by React state** — the input's value comes from state and every change updates it via a handler.

```jsx
const [name, setName] = useState("");
<input value={name} onChange={e => setName(e.target.value)} />
```

- **Single source of truth** in React state → easy validation, disabling, formatting, two-way sync.
- Most React forms should be controlled (Q192).

---

## Q191: What is an uncontrolled component?

A form input that **manages its own value in the DOM**; React only reads it when needed (via `useRef`).

```jsx
function Form() {
  const inputRef = useRef(null);
  const submit = () => console.log(inputRef.current.value);  // read on demand
  return <input ref={inputRef} defaultValue="hi" />;
}
```

- `defaultValue` sets the initial value; the DOM owns the rest.
- Pros: less re-rendering per keystroke; simpler for one-off reads. Cons: no validation/instant sync.
- **Controlled vs uncontrolled** is the key tradeoff (Q573 in advanced).

---

## Q192: How do you handle forms in React?

**Controlled inputs** (state-driven) with validation + submission:

```jsx
function LoginForm({ onSubmit }) {
  const [values, setValues] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});

  const handleChange = (e) =>
    setValues({ ...values, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();                 // stop page reload
    if (!values.email.includes("@")) {
      setErrors({ email: "Invalid email" }); return;
    }
    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <input name="email" value={values.email} onChange={handleChange} />
      {errors.email && <span>{errors.email}</span>}
      <input name="password" type="password" value={values.password} onChange={handleChange} />
      <button type="submit">Login</button>
    </form>
  );
}
```

- Patterns: lift state up, validate on change + submit, disable submit while pending.
- Libraries: **React Hook Form** (+ Zod schema validation), Formik. Micro1 is more likely to ask about the fundamentals above.

---

## Q193: What is `useState()`?

A hook that adds **local state** to a function component. Returns `[value, setter]`.

```jsx
const [count, setCount] = useState(0);        // initial value 0
const [user, setUser] = useState<User | null>(null);

setCount(1);              // direct value
setCount(c => c + 1);     // functional update from previous
```

- Setter replaces the value (objects/dicts need spread to update fields).
- **Rules of hooks:** only call at top level (not in loops/if/callbacks), only in React components or custom hooks.
- State persists across renders (kept in the fiber node).

---

## Q194: What is `useEffect()`?

A hook for **side effects** — things outside the render (API calls, subscriptions, timers, DOM updates). Runs after render, coordinated with a **dependency array**.

```jsx
useEffect(() => {
  // effect (after render)
  return () => { /* cleanup — before next run / unmount */ };
}, [deps]);
```

- **Two parts:** the effect callback + the cleanup function it returns.
- No deps array → runs after **every** render. Empty `[]` → runs once (mount). With deps → re-runs when deps change.
- Used for data fetching (with async/abort), event listeners, timers, subscriptions.

---

## Q195: When does `useEffect()` run?

1. After the **initial render** (mount).
2. After every render where **any dependency changed** (strict comparison, `Object.is`).
3. Cleanup runs before the next effect run and on **unmount**.

```jsx
useEffect(() => {
  const id = setInterval(tick, 1000);      // runs on mount (+ when deps change)
  return () => clearInterval(id);          // cleanup
}, []);
```

- Effects are **asynchronous to rendering** — they never block paint.
- Strict mode (dev) double-invokes effects to surface bugs.
- **Note:** don't run state-updating logic synchronously in the render body — that belongs in effects or event handlers.

---

## Q196: What is the dependency array in `useEffect()`?

The list of values the effect depends on; React re-runs the effect when any of them **change reference/value** since the last render.

```jsx
useEffect(() => { fetchUser(userId); }, [userId]);   // re-fetch when userId changes
```

- **Empty `[]`** → runs once on mount (captures initial props/state).
- **No array** → runs after every render (usually a bug or intentional).
- Rules: include every value the effect reads; use `useCallback`/`useMemo` to stabilize functions/objects; ESLint `react-hooks/exhaustive-deps` catches mistakes.
- Gotcha: **referential identity** — passing an inline object/function as a dep changes every render → effect runs every render. Fix with `useMemo`/`useCallback` or by including primitive values.

---

## Q197: How can `useEffect()` cause an infinite loop?

When the effect **updates state that the dependency array depends on** → update → deps change → effect re-runs → update → ...

```jsx
const [data, setData] = useState([]);
useEffect(() => {
  setData(compute(data));        // data in deps → setData changes data → loop!
}, [data]);
```

Common causes:
1. Updating state that's a dependency (above).
2. **New object/array identity every render** in deps: `useEffect(fn, [obj])` where `obj` is recreated inline → changes each render → infinite.
3. Fetching inside an effect that sets fetched data which is a dep.

Fixes: remove the state from deps, use functional updates, stabilize with `useMemo`/`useCallback`, or fetch only on explicit triggers.

---

## Q198: How do you perform API calls from React?

Modern approach — **TanStack Query (React Query)** for server state (caching, retries, loading/error states):

```jsx
const { data, isLoading, isError, refetch } = useQuery({
  queryKey: ["users", page],
  queryFn: () => api.getUsers(page),
});
```

Manual approach with `useEffect` + `useState`:

```jsx
useEffect(() => {
  const ac = new AbortController();
  setLoading(true);
  fetch(`/api/users?page=${page}`, { signal: ac.signal })
    .then(r => r.json())
    .then(d => { setData(d); setLoading(false); })
    .catch(err => { if (err.name !== "AbortError") setError(err); setLoading(false); });
  return () => ac.abort();       // cancel on unmount / page change
}, [page]);
```

- Best practice: **abort on unmount** (Q577), handle loading + error states (Q199–200), avoid race conditions (Q576).

---

## Q199: How do you handle loading states?

1. **Track it:** `isLoading` from the fetch flow (or React Query's `isLoading/isFetching`).
2. **Render feedback:** skeleton screens, spinners, or "loading…" placeholders — never a blank flash.
3. **Skeletons > spinners** for lists/cards (reduces layout shift, feels faster).
4. **Defer/persist:** for refetches, keep showing stale data + a subtle indicator instead of clearing the UI.
5. **Avoid flicker:** don't flip to loading when you already have cached data (`isFetching` vs `isLoading` distinction in React Query).

```jsx
{isLoading ? <SkeletonList/> : <UserTable users={data}/>}
```

---

## Q200: How do you handle API errors in React?

1. **Capture the error** in state (or React Query's `isError`/`error`).
2. **User-friendly message** — generic text, retry button; log the detail.
3. **Different surfaces:** inline error on the component, error boundary for render errors (Q320), toast for background failures.
4. **Retry** — button or auto-retry (React Query default 3 retries with backoff).
5. **Partial data:** if some data loaded, show it + a warning banner rather than blanking.

```jsx
if (isError) return (
  <div role="alert">
    <p>Couldn't load users.</p>
    <button onClick={() => refetch()}>Try again</button>
  </div>
);
```

- Network errors vs business errors (HTTP status) → handle 401 (redirect to login), 403, 404 distinctly.

---

## Q201: What is `useMemo()`?

A hook that **memoizes a computed value** — recomputes only when its dependencies change.

```jsx
const total = useMemo(() => expensive(items), [items]);
```

- Returns the *previous* result if deps are unchanged → skips recomputation.
- Also **stabilizes object/array references** across renders (important for effect deps and memoized children).
- Only optimize real cost; measure first (Q207).

---

## Q202: What is `useCallback()`?

A hook that **memoizes a function** — returns the same function reference until deps change.

```jsx
const handleSave = useCallback(() => {
  save(values);
}, [values]);
```

- Prevents child re-renders (with `React.memo`) and keeps stable references for effect dependencies.
- `useCallback(fn, deps)` is equivalent to `useMemo(() => fn, deps)`.

---

## Q203: What is `useRef()`?

A hook for a **mutable value that persists across renders** without triggering re-renders.

```jsx
const inputRef = useRef(null);        // DOM ref
const countRef = useRef(0);           // arbitrary mutable value

inputRef.current.focus();
countRef.current += 1;
```

- `.current` is a mutable box; changing it does **not** cause re-render.
- Uses: focusing/manipulating DOM, storing previous values, holding timers/ids, avoiding stale closure values in effects/callbacks.

---

## Q204: What is `useContext()`?

A hook that **reads a Context value** provided higher in the tree — shared state without prop drilling.

```jsx
const ThemeContext = createContext("light");

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar/>
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);   // "dark"
  return <button className={theme}>...</button>;
}
```

- Provider passes a value; consumers re-render when it changes.
- Split contexts by concern to limit re-render scope (auth, theme, settings).
- For high-frequency updates, consider state libraries (Q213, Q583).

---

## Q205: What is the difference between `useMemo()` and `useCallback()`?

| | **`useMemo`** | **`useCallback`** |
|---|---|---|
| Returns | A memoized **value** (any type) | A memoized **function** |
| Purpose | Skip expensive recomputation; stabilize values/objects | Stabilize function references |
| Signature | `useMemo(() => compute(), deps)` | `useCallback(fn, deps)` |

```jsx
const sorted = useMemo(() => sort(items), [items]);      // value
const onSort = useCallback((dir) => sortItems(dir), []); // function
```

- Both exist to give stable references and avoid wasted work; neither makes React "faster" by itself.

---

## Q206: When should you use `useMemo()`?

1. The computation is **genuinely expensive** (measured — large arrays, heavy math, complex derived data).
2. You need a **stable reference** for a value passed to a memoized child (`React.memo`) or an effect dependency.
3. Derived data used by multiple consumers (selector-style).
4. Inside a render that runs frequently.

Example: sorting/filtering a 10k-row list based on search text.

```jsx
const visibleRows = useMemo(
  () => rows.filter(r => r.name.includes(query)),
  [rows, query]
);
```

---

## Q207: When should you avoid `useMemo()`?

1. **Trivial computations** — memoization overhead (allocating, comparing deps) exceeds the compute cost.
2. **Cheap comparisons** already fast.
3. When you don't have a perf problem — **premature optimization**.
4. As a rule on every value — it clutters code without benefit.
5. When the value changes often anyway (deps change every render → no benefit).

**Golden rule:** profile first (React DevTools Profiler), then optimize the actual hot paths.

---

## Q208: How do you prevent unnecessary React re-renders?

1. **`React.memo`** — memoize a component against prop changes (Q209).
2. **`useCallback`/`useMemo`** — stabilize props (functions/objects) so memoized children skip.
3. **Split state** — keep state close to where it's used; smaller components re-render less.
4. **Context slicing** — separate contexts so consumers only re-render for their slice.
5. **Avoid inline object/function props** to memoized components.
6. **Keys** — stable keys avoid remounts.
7. **Lift effects up / data fetching** into React Query — fewer manual setState storms.
8. **Virtualization** for long lists (only render visible rows).
9. **Don't put the whole app state in one component** — propagate only what changes.

Remember: re-render ≠ DOM update; focus on *wasted* work, measured.

---

## Q209: What is `React.memo()`?

A higher-order component that **memoizes a component**: it re-renders only when its **props change** (shallow compare), skipping re-renders when the parent re-renders with the same props.

```jsx
const ExpensiveRow = memo(function ExpensiveRow({ item, onSelect }) {
  return <li onClick={() => onSelect(item.id)}>{item.name}</li>;
});
```

- **Props must be referentially stable** to benefit → pair with `useCallback`/`useMemo` in the parent.
- Shallow compare only (primitive equality; object/function identity).
- Not for components whose props change every render; not needed for cheap renders.

---

## Q210: What is lifting state up?

Moving shared state from child components **up to a common parent**, passing values + setters down as props.

```jsx
function App() {
  const [tab, setTab] = useState("overview");   // shared state lives here
  return (<>
    <Tabs tab={tab} onChange={setTab} />
    <Panel tab={tab} />
  </>);
}
```

- Needed when **two or more components derive from the same state**.
- Tradeoff: more prop drilling (Q211). If too deep, use Context or a store.

---

## Q211: What is prop drilling?

Passing props through **many intermediate components** that don't use them, just to reach a deep consumer.

```jsx
<App user={u} />
  → <Header user={u} />        {/* doesn't use user */}
    → <Avatar user={u} />      {/* needs it */}
```

- Problems: verbose, couples middle components to data they don't need, re-render bloat.
- Solutions: **Context API** (Q213), state libraries, or component composition (pass the rendered child instead of data).

---

## Q212: How would you solve prop drilling?

1. **Context API** — provide near the top, consume where needed (Q213).
2. **Component composition** — pass `<Avatar user={u}/>` as children/JSX from the top instead of raw data.
3. **State management library** — Zustand/Redux/Jotai for cross-cutting or frequent state (Q583–585).
4. **Server state in React Query** — components fetch their own data by query key; no drilling.
5. Split components so data and its consumers live close together.

**Order of preference:** try composition → context → a store, adding complexity only as needed.

---

## Q213: What is Context API?

React's built-in mechanism to **share values across the component tree** without prop drilling.

```jsx
const AuthContext = createContext<{ user: User | null; login: () => void } | null>(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const login = useCallback(async () => { setUser(await api.login()); }, []);
  return <AuthContext.Provider value={{ user, login }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
```

- **Value + Provider + Consumer** (via `useContext`).
- Great for: auth, theme, locale, feature flags, current user — data read widely, updated rarely.
- **Caveat:** every consumer re-renders on *any* value change → split contexts, memoize values, or use selectors/Zustand for hot paths.

---

## Q214: How would you structure a large React application?

**Feature-first structure (Next.js App Router or Vite):**

```
src/
  app/                # routing / layout (Next.js) or pages/
  features/
    candidates/
      components/     # feature-specific components
      hooks/          # feature hooks
      api.ts          # feature API client + react-query hooks
      types.ts        # feature types
      components/ui/  # shared primitives (button, table)
  components/ui/      # global design system (Tailwind components)
  lib/                # api client, utils, auth
  stores/             # global state (zustand) slices
  styles/
```

**Principles to state out loud:**
1. **Feature colocation** — files that change together live together.
2. **Shared UI kit** (design system) separate from feature components.
3. **Server state via TanStack Query** — features declare queries, not fetch spaghetti.
4. **Minimal global state** — only genuinely global data (auth/settings); everything else local/feature.
5. **TypeScript end-to-end** — types shared with backend (Q242) or generated from OpenAPI.
6. **Code splitting** by route/feature (Q259), lazy loading heavy screens.
7. **Conventions:** one component per file, barrel exports, ESLint/Prettier, Storybook for UI.
8. **Testing colocated** — component tests next to components.

---

## Q215: How would you build a reusable component system?

1. **Design tokens first** — spacing, colors, radii, typography as CSS variables/Tailwind theme.
2. **Base primitives** — `Button`, `Input`, `Table`, `Modal`, `Tooltip` with consistent, typed APIs.
3. **Composition over config** — allow children and `as` props; avoid 30-boolean config monsters.
4. **Typed with TypeScript** — full prop types + variant types (`variant?: "primary" | "ghost"`).
5. **Forward refs** (`forwardRef`) and `className` passthrough for flexibility.
6. **Accessible** — keyboard nav, ARIA, focus management (or build on Radix UI/Headless UI for behavior, style yourself).
7. **Documentation + showcase** — Storybook; each component: props table, variants, usage.
8. **Versioned + tested** — component tests (Testing Library), consistent changelog.
9. **DRY vs over-abstraction** — extract when used 2–3 times; don't abstract prematurely.
10. **Themeable** — dark mode via tokens/CSS variables, Tailwind `dark:` variants.
