# Reducate.ai — 100 Full Stack Interview Q&A

> Based on Reducate.ai — Full Stack Development Internship (Next.js SSR/SSG, Redux, TypeScript, APIs, testing)  > Candidate: Aayush Gid (Next.js/React/TypeScript/FastAPI/MySQL/AI guardrails background)

---

## 1. Next.js: SSR, SSG & Rendering (Q1–Q14)

**Q1: What is the difference between SSR, SSG, and CSR in Next.js?**  
A: SSR (Server-Side Rendering) renders pages on each request (`getServerSideProps`), SSG (Static Site Generation) pre-renders at build time (`getStaticProps`), and CSR (Client-Side Rendering) renders in the browser. At Reducate.ai most marketing/content pages are SSG for speed, while dynamic user dashboards use SSR.

**Q2: When would you choose SSG over SSR?**  
A: Use SSG when data changes infrequently and SEO/first-paint speed matter (e.g., course landing pages). It ships static HTML and scales cheaply on Vercel — perfect for Reducate.ai's education content pages.

**Q3: Explain `getStaticProps` and `getStaticPaths`.**  
A: `getStaticProps` fetches data at build time for SSG; `getStaticPaths` defines which dynamic routes (e.g., `/course/[id]`) to pre-render.

```tsx
export async function getStaticPaths() {
  const courses = await getCourses();
  return { paths: courses.map(c => ({ params: { id: c.id } })), fallback: 'blocking' };
}
export async function getStaticProps({ params }) {
  return { props: { course: await getCourse(params.id) }, revalidate: 60 };
}
```

**Q4: What is Incremental Static Regeneration (ISR)?**  
A: ISR lets you update static pages after build using `revalidate`, so you get SSG performance with fresh data without a full rebuild. Great for course catalogs that update daily.

**Q5: What is the App Router vs Pages Router?**  
A: The App Router (`app/` directory) uses React Server Components, nested layouts, and `async` server components; the Pages Router (`pages/`) uses `getServerSideProps`/`getStaticProps`. Reducate.ai is moving to App Router for better data fetching.

**Q6: What are Server Components and Client Components?**  
A: Server Components run only on the server (no JS shipped, can access DB directly); Client Components run in the browser (`"use client"`). Use Server Components for data fetching and Client Components for interactivity.

**Q7: How do you fetch data in the App Router?**  
A: In a Server Component you `await` directly inside the component; for client fetching use SWR or React Query against API routes.

```tsx
export default async function Page() {
  const res = await fetch('https://api.reducate.ai/courses', { cache: 'no-store' });
  const courses = await res.json();
  return <CourseList courses={courses} />;
}
```

**Q8: How do you handle dynamic routes in the App Router?**  
A: Use a folder with brackets like `app/course/[id]/page.tsx` and read `params.id`. Add `generateStaticParams` for SSG.

**Q9: What is the purpose of `next/image`?**  
A: It optimizes images automatically (lazy loading, resizing, modern formats). I used it in the SaaS Video Editor to cut image payloads significantly.

**Q10: How do you optimize performance in a Next.js app?**  
A: Use SSG/ISR, `next/image`, code-splitting via dynamic imports, route-level `loading.tsx`, and avoid heavy client bundles. I applied these in GuardrailZ and the SaaS Video Editor.

**Q11: What is `next/font` and why use it?**  
A: `next/font` self-hosts fonts with zero layout shift and no extra network requests. It improves Core Web Vitals, important for Reducate.ai's public pages.

**Q12: How do you handle environment variables in Next.js?**  
A: Server-only vars go in `.env.local` (accessed server-side); prefix client-exposed vars with `NEXT_PUBLIC_`. Never leak secrets to the client bundle.

**Q13: What are layouts and how do they help?**  
A: A `layout.tsx` wraps nested routes and persists state/UI across navigations without remounting. Useful for shared nav/sidebar in Reducate.ai dashboards.

**Q14: How would you deploy a Next.js app at Reducate.ai?**  
A: Deploy on Vercel (I have Vercel experience from the SaaS Video Editor) with preview deploys per PR, environment variables per environment, and CI via GitHub Actions.

---

## 2. React Fundamentals & Components (Q15–Q28)

**Q15: What is the difference between a function component and a class component?**  
A: Function components are simpler, use hooks, and are the modern standard; class components use `this.state` and lifecycle methods. I only use function components with hooks.

**Q16: Explain the useState hook.**  
A: `useState` holds local component state and returns `[value, setValue]`.

```tsx
const [count, setCount] = useState(0);
```

**Q17: What are useEffect dependencies and cleanup?**  
A: The dependency array controls when the effect runs; returning a function cleans up (e.g., subscriptions). Empty array = run once on mount.

**Q18: What is the React component lifecycle in hooks?**  
A: Mount (`useEffect` with `[]`), update (deps change), unmount (cleanup). Hooks replaced the old class lifecycle methods.

**Q19: What are keys in lists and why do they matter?**  
A: Keys help React identify items across renders to optimize reconciliation. Use stable IDs, never array indexes for mutable lists.

**Q20: Controlled vs uncontrolled components?**  
A: Controlled inputs are driven by React state (`value` + `onChange`); uncontrolled use `ref` and the DOM. I prefer controlled for form validation in Reducate.ai forms.

**Q21: What is prop drilling and how do you avoid it?**  
A: Prop drilling is passing props through many layers; avoid with Context, Redux, or Zustand (my Workflow-Canvas used Zustand).

**Q22: What is React Context?**  
A: Context provides global state without prop drilling. Good for theme/auth, but overuse can hurt performance — pair with `useMemo`.

**Q23: How do you handle forms in React?**  
A: Controlled inputs with state, validation on submit/blur, and libraries like React Hook Form. I built auth forms in GuardrailZ with Clerk + controlled inputs.

**Q24: What are refs and when do you use them?**  
A: `useRef` accesses DOM nodes or mutable values without re-render. Use for focus, timers, or canvas (SaaS Video Editor used refs for video elements).

**Q25: What is reconciliation in React?**  
A: React's algorithm diffs the virtual DOM to update only changed real DOM nodes efficiently. Keys and component structure affect its performance.

**Q26: How do you optimize a slow React component?**  
A: Memoize with `React.memo`, `useMemo`, `useCallback`, split heavy work, and lazy-load with `React.lazy`/`Suspense`.

**Q27: What is the difference between `useMemo` and `useCallback`?**  
A: `useMemo` caches a computed value; `useCallback` caches a function reference. Both prevent unnecessary re-renders.

**Q28: How have you used React in real projects?**  
A: SaaS Video Editor (React + Framer Motion), Workflow-Canvas (React Flow), GuardrailZ (Next.js + React). I'm comfortable building production UIs.

---

## 3. Redux & State Management (Q29–Q42)

**Q29: What is Redux and why use it?**  
A: Redux is a predictable state container using a single store, actions, and reducers. Reducate.ai uses it for complex shared state across pages.

**Q30: Explain the Redux data flow.**  
A: UI dispatches an action → reducer returns new state → store updates → components re-render via selectors. Unidirectional and debuggable.

**Q31: What are actions, reducers, and the store?**  
A: Actions are plain objects with `type`; reducers are pure functions `(state, action) => newState`; the store holds the state and wires it together.

**Q32: What is Redux Toolkit (RTK) and why prefer it?**  
A: RTK reduces boilerplate with `createSlice`, `configureStore`, and built-in Immer. It's the modern standard Reducate.ai likely uses.

```ts
const slice = createSlice({ name: 'course', initialState, reducers: {
  setCourses: (s, a) => { s.list = a.payload; }
}});
```

**Q33: What is `createSlice`?**  
A: It generates action creators and a reducer from a single definition, removing manual switch statements.

**Q34: How do you handle async logic in Redux?**  
A: Use RTK `createAsyncThunk` or `redux-thunk` middleware to dispatch pending/fulfilled/rejected actions for API calls.

**Q35: What is a selector and why use `createSelector` (memoization)?**  
A: Selectors derive data from state; `createSelector` memoizes so expensive computations only re-run when inputs change.

**Q36: How does Redux compare to Zustand (which you've used)?**  
A: Zustand is lighter, hook-based, less boilerplate; Redux is more structured and scalable. My Workflow-Canvas used Zustand; I can map that knowledge directly to Redux patterns.

**Q37: What is the difference between Redux and React Context?**  
A: Redux has a global store with devtools/middleware and better performance at scale; Context is simpler but can cause re-render issues without memoization.

**Q38: How do you connect Redux to React?**  
A: With `react-redux`'s `Provider` and `useSelector`/`useDispatch` hooks (modern) rather than `connect`.

**Q39: What is middleware in Redux?**  
A: Middleware intercepts actions (e.g., `redux-thunk` for async, `redux-logger`). It's how side effects are handled.

**Q40: How do you debug Redux?**  
A: Use Redux DevTools to inspect actions, state diffs, and time-travel. I'd add it to track API state in Reducate.ai's dashboards.

**Q41: How would you structure Redux for a course platform?**  
A: Slices like `auth`, `courses`, `enrollments`, `ui`; async thunks for API; selectors for derived data. Keep reducers pure.

**Q42: What are common Redux mistakes?**  
A: Mutating state directly, putting non-serializable data (e.g., functions) in state, and over-fetching in selectors. Always return new state.

---

## 4. TypeScript (Q43–Q54)

**Q43: Why use TypeScript in a full-stack project?**  
A: It catches errors at compile time, improves refactoring, and documents APIs via types — valuable for Reducate.ai's shared frontend/backend contracts.

**Q44: What is the difference between `interface` and `type`?**  
A: Both describe shapes; `interface` supports declaration merging and is better for objects; `type` can represent unions, tuples, and primitives.

**Q45: Explain generics with an example.**  
A: Generics make functions/components reusable with type safety.

```ts
function first<T>(arr: T[]): T | undefined { return arr[0]; }
```

**Q46: What are union and intersection types?**  
A: Union `A | B` accepts either; intersection `A & B` requires both. I use unions for API response states (`Success | Error`).

**Q47: How do you type props in React with TS?**  
A: Define a `Props` type/interface and annotate the component.

```tsx
type Props = { title: string; onClose: () => void };
function Modal({ title, onClose }: Props) { ... }
```

**Q48: What are utility types (`Partial`, `Pick`, `Omit`)?**  
A: They transform existing types: `Partial<T>` makes all optional, `Pick` selects keys, `Omit` removes keys — handy for form/edit DTOs.

**Q49: What is `unknown` vs `any`?**  
A: `unknown` is type-safe (must narrow before use); `any` disables checking. Prefer `unknown` for untrusted input like API payloads.

**Q50: How do you handle nullable values (`null` vs `undefined`)?**  
A: Use strict mode; prefer `undefined` for absence, guard with optional chaining `?.` and nullish coalescing `??`.

**Q51: What is type narrowing?**  
A: TS infers a narrower type after checks like `typeof`, `in`, or type guards, enabling safe access.

**Q52: How do you type async API functions?**  
A: Annotate return types as `Promise<T>` and define request/response interfaces shared between client and server.

**Q53: What is `as const` and when to use it?**  
A: `as const` makes a value readonly and literal-typed — useful for action types or config constants.

**Q54: How have you used TypeScript in projects?**  
A: GuardrailZ, Workflow-Canvas, and Sim Studio OSS all used TypeScript; I'm confident with strict mode and typing React/Next.js apps.

---

## 5. APIs & Backend Integration (Q55–Q66)

**Q55: How do you consume a REST API from Next.js?**  
A: Server-side via `fetch` in Server Components/route handlers; client-side via SWR/React Query or `fetch` in effects. I built FastAPI backends consumed by React frontends.

**Q56: What is the difference between REST and GraphQL?**  
A: REST uses multiple resource endpoints; GraphQL uses a single endpoint with a query for exactly the data needed. Reducate.ai appears REST-based, which I know well.

**Q57: Explain JWT authentication flow.**  
A: User logs in → server returns a signed JWT → client stores it (httpOnly cookie preferred) → sends in `Authorization: Bearer` header → server verifies signature.

**Q58: What is OAuth and where is it used?**  
A: OAuth delegates auth to a provider (Google/GitHub). I used Clerk (which wraps OAuth) in GuardrailZ for social login.

**Q59: How do you handle API errors on the frontend?**  
A: Check `res.ok`, parse error bodies, surface user-friendly messages, and use error boundaries/state. I implement typed error unions.

**Q60: What status codes should an API return?**  
A: 200/201 success, 400 bad request, 401 unauthorized, 403 forbidden, 404 not found, 500 server error. Use them consistently.

**Q61: How do you secure an API (CORS, rate limiting)?**  
A: Set CORS allowlists, add rate limiting, validate input, use HTTPS, and sanitize. In Sim Studio OSS I added SSRF protection and localhost handling.

**Q62: What is caching and how have you used Redis?**  
A: Caching stores frequent responses to reduce DB load. I used Redis in the Agentic AI Intern role to cache FastAPI microservice responses.

**Q63: How would you integrate a FastAPI backend with a Next.js frontend?**  
A: Next.js calls FastAPI via `fetch`/SWR; deploy separately (Render/Vercel) or behind a gateway; share TS types via OpenAPI codegen.

**Q64: What is idempotency in APIs?**  
A: An operation producing the same result if called multiple times (e.g., retries on POST payments). Use idempotency keys.

**Q65: How do you version an API?**  
A: Via URL path (`/v1/`), header, or content negotiation. I version FastAPI routers to avoid breaking clients.

**Q66: How do you test API integration on the frontend?**  
A: Mock fetch with MSW or Jest mocks, and write Cypress e2e tests hitting a staging API. I've written Jest tests for API modules.

---

## 6. MySQL & Databases (Q67–Q76)

**Q67: What is the difference between SQL and NoSQL?**  
A: SQL (MySQL/PostgreSQL) is relational with schemas and joins; NoSQL (MongoDB) is flexible documents. Reducate.ai lists MySQL, which I've used alongside PostgreSQL.

**Q68: What are primary keys and foreign keys?**  
A: Primary key uniquely identifies a row; foreign key links to another table's primary key to enforce relationships.

**Q69: What are indexes and why are they important?**  
A: Indexes speed up lookups (B-tree) at the cost of write overhead. Add them to frequently queried columns like `user_id`.

**Q70: What is a JOIN? Give an example.**  
A: JOINs combine rows from tables. An INNER JOIN returns matching rows:

```sql
SELECT c.title, u.name
FROM courses c JOIN enrollments e ON c.id = e.course_id
JOIN users u ON e.user_id = u.id;
```

**Q71: What is the difference between INNER, LEFT, and RIGHT JOIN?**  
A: INNER returns matches in both; LEFT returns all left rows plus matches (nulls otherwise); RIGHT is the reverse.

**Q72: What are transactions and ACID?**  
A: A transaction groups operations atomically; ACID = Atomicity, Consistency, Isolation, Durability. Use for enrollments/payments.

**Q73: How do you prevent SQL injection?**  
A: Use parameterized queries/ORM, never string concatenation. I use SQLAlchemy/FastAPI's parameterized queries.

```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Q74: What is normalization (1NF–3NF)?**  
A: Normalization reduces redundancy: 1NF atomic values, 2NF no partial dependencies, 3NF no transitive dependencies.

**Q75: How do you optimize a slow MySQL query?**  
A: Use `EXPLAIN`, add indexes, avoid `SELECT *`, and denormalize selectively. I've tuned PostgreSQL queries similarly.

**Q76: You know PostgreSQL — how transferable is MySQL?**  
A: Very; both are relational with SQL, indexes, and transactions. Syntax differences (e.g., `AUTO_INCREMENT` vs `SERIAL`) are minor — I adapt quickly.

---

## 7. Testing (Jest & Cypress) (Q77–Q84)

**Q77: Why is testing important for an internship role?**  
A: It prevents regressions and documents behavior. Reducate.ai expects Jest unit/integration and Cypress e2e — I have Jest experience from Sim Studio OSS.

**Q78: What is the difference between unit, integration, and e2e tests?**  
A: Unit tests isolate a function/component; integration tests combine modules (API+DB); e2e (Cypress) tests the full user flow in a browser.

**Q79: How do you write a Jest unit test?**  
A: Use `describe`/`it` with `expect` assertions and mocks for dependencies.

```ts
test('adds course to cart', () => {
  expect(addToCart([], 1)).toEqual([1]);
});
```

**Q80: What is mocking and when do you use it?**  
A: Mocking replaces dependencies (API, DB) with controlled fakes to isolate the unit. Use `jest.mock` for fetch calls.

**Q81: How do you test a React component with Jest?**  
A: Use React Testing Library: render the component, query by role, fire events, and assert. I've tested components this way.

**Q82: What is Cypress and how does it differ from Jest?**  
A: Cypress runs real browser e2e tests interacting with the UI, while Jest runs fast in Node. Cypress validates critical Reducate.ai flows like login/enroll.

**Q83: How would you test an API integration?**  
A: Jest integration test hitting a test DB, or mock the client and assert request/response. Cypress for the full flow via UI.

**Q84: What testing practices would you bring from your experience?**  
A: I wrote tests in Sim Studio OSS (including SSRF/localhost handling) and Jest unit tests; I'd apply the same rigor to Reducate.ai's Next.js components and APIs.

---

## 8. Accessibility & Design Collaboration (Q85–Q90)

**Q85: What is web accessibility (a11y)?**  
A: Making sites usable by everyone, including screen-reader and keyboard users, per WCAG. Important for Reducate.ai's education reach.

**Q86: How do you make a form accessible?**  
A: Associate labels with inputs, use `aria-*` for errors, ensure focus management, and provide visible focus rings.

**Q87: What are ARIA attributes and when should you use them?**  
A: ARIA describes roles/states (e.g., `aria-live` for dynamic content) when HTML semantics aren't enough. Don't override native semantics unnecessarily.

**Q88: How do you ensure keyboard navigation?**  
A: Use semantic elements, manage focus traps in modals, and test tab order. I built accessible modals in GuardrailZ.

**Q89: How do you collaborate with designers?**  
A: Use their Figma specs, implement with Tailwind, match spacing/colors, and flag a11y issues early. I worked closely with design in the SaaS Video Editor.

**Q90: How do you handle responsive design?**  
A: Mobile-first with CSS flexbox/grid and Tailwind breakpoints; verify with devtools and real devices for Reducate.ai's learner base.

---

## 9. Golang Basics (Q91–Q95)

**Q91: You're strong in Python — how would you learn Golang quickly?**  
A: Go's syntax is C-like but simple; my Python/FastAPI backend experience maps to Go's `net/http` and structs-as-models. I'd ramp in weeks, not months.

**Q92: What are Go's key features?**  
A: Statically typed, compiled, goroutines for concurrency, and a simple standard library. It's fast and great for APIs Reducate.ai may use.

**Q93: How do you define a struct and function in Go?**  
A: Structs are like typed dicts/classes; functions use explicit return types.

```go
type User struct { ID int; Name string }
func (u User) Greet() string { return "Hi " + u.Name }
```

**Q94: What are goroutines and channels?**  
A: Goroutines are lightweight threads (`go func()`); channels pass data between them safely — Go's concurrency model differs from Python's asyncio but is intuitive.

**Q95: How would you build a simple REST API in Go?**  
A: Use `net/http` or Gin/Fiber, define handlers returning JSON, and route paths. Conceptually identical to my FastAPI services, just typed and compiled.

---

## 10. Behavioral & "Why Reducate.ai" (Q96–Q100)

**Q96: Why do you want to join Reducate.ai?**  
A: Reducate.ai blends education and AI — my guardrails/workflow projects align with its mission, and the Next.js/React/TypeScript stack matches my strengths exactly.

**Q97: You have a Python backend background but the role lists Golang — concern?**  
A: Not at all. My FastAPI/Flask/Express backend skills transfer directly to Go's API patterns, and I learn new languages fast (built Sim Studio OSS contributions quickly).

**Q98: Describe a challenging project and how you solved it.**  
A: GuardrailZ — I built LLM guardrails with Next.js, Clerk auth, and regex validation, shipping a secure product on Vercel. It shows I can own full-stack features end-to-end.

**Q99: How do you work in a remote, 5-days/week internship?**  
A: I'm disciplined with Git/GitHub, write clear PRs, and use CI (GitHub Actions) from prior roles. My Agentic AI Intern role was remote too.

**Q100: Where do you see yourself after this internship?**  
A: Growing into a full-stack engineer specializing in AI-powered education products at Reducate.ai, contributing to Coding Jr/Planto.ai and shipping reliable Next.js features.

---

