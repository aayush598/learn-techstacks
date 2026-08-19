# Everything About AI — 100 Full Stack Interview Q&A

> Based on Everything About AI — Full Stack Development Internship (React/Node/PostgreSQL+Supabase/MongoDB/Vercel/GenAI tools)  > Candidate: Aayush Gid (Next.js/React/Node/Express/PostgreSQL/MongoDB/Vercel/AI guardrails background)

---

## 1. Full-Stack Architecture & End-to-End Builds (Q1–Q12)

**Q1: How do you approach building an app from concept to production?**  
A: I start with requirements and a data model, then scaffold the frontend (React/Next.js) and backend (Node/Express or serverless), wire the DB (PostgreSQL/Supabase or MongoDB), integrate third-party APIs, and deploy on Vercel. My SaaS Video Editor went live this way: Next.js + React + Tailwind + Framer Motion deployed on Vercel in a few iterations.

**Q2: What is the difference between a monolith and a serverless architecture?**  
A: A monolith runs as one deployable process handling all routes; serverless splits logic into functions invoked on-demand (e.g., Vercel Functions). Serverless scales per-request and is cost-efficient for spiky traffic, like my FastAPI microservices behind AWS ECS, but adds cold-start and observability trade-offs.

**Q3: Explain the MVC pattern and where it fits in a full-stack app.**  
A: Model (data/DB schemas), View (React UI), Controller (request handlers in Express/Next API routes). In my Express + PostgreSQL projects, controllers validate input, call services, and return JSON the React frontend renders.

**Q4: How do you decide between a traditional SPA and a Next.js app?**  
A: Use a plain React SPA for simple dashboards; use Next.js for SSR/SSG, SEO, and built-in API routes + edge deployment. GuardrailZ and SaaS Video Editor use Next.js precisely for these benefits on Vercel.

**Q5: What is the role of an API gateway or BFF (Backend for Frontend)?**  
A: A BFF tailors backend responses for the frontend and aggregates microservices, reducing over-fetching. In my Agentic AI intern work, FastAPI services sat behind a gateway-like layer to keep the client simple.

**Q6: How do you keep a full-stack codebase maintainable as it grows?**  
A: Modular folder structure (features/components/services), shared types (TypeScript), env-based config, and linting. Workflow-Canvas used Zustand + ReactFlow with clear state boundaries to stay maintainable.

**Q7: Describe your experience with rapid prototyping tools like Lovable/Replit/V0.**  
A: I use V0 for component scaffolding, Replit for quick backends, and Lovable for full-app prototypes, then refine in Cursor/VSCode. These accelerate the "concept→production" loop the role emphasizes.

**Q8: How do you handle secrets and environment config in a full-stack app?**  
A: Store secrets in `.env` (never committed), use Vercel/Platform env vars in production, and inject via `process.env`. For Supabase/Mongo I keep connection strings out of source control and load them per environment.

**Q9: What is CORS and when do you need to configure it?**  
A: CORS controls which origins can call your API. Configure it on the Node/Express server or serverless function when the frontend and API are on different origins (e.g., Vercel frontend calling a separate API).

```js
app.use(cors({ origin: "https://myapp.vercel.app" }));
```

**Q10: How would you architect a real-time collaborative feature?**  
A: Use WebSockets (Socket.io) or Server-Sent Events, backed by a pub/sub (Redis) and a persistent store. Workflow-Canvas' node editing could be synced this way via Zustand + a WS channel.

**Q11: Explain the difference between client-side and server-side rendering.**  
A: Client-side rendering builds HTML in the browser (SPA); server-side rendering renders on the server per request (Next.js `getServerSideProps`/`app` router). SSR improves SEO and first paint, important for marketing pages on Vercel.

**Q12: How do you estimate and scope a feature before building?**  
A: Break it into user stories, identify data models and API endpoints, flag third-party dependencies (e.g., Cloudinary), and estimate in small tasks. I do this in GitHub Issues with checklists during internships.

---

## 2. Frontend: React, HTML5, CSS3, JavaScript (Q13–Q30)

**Q13: What are React hooks and which do you use most?**  
A: Hooks let function components use state/effects: `useState`, `useEffect`, `useContext`, `useMemo`, `useReducer`. I rely on `useState`/`useEffect` for UI state and `useMemo` for expensive ReactFlow computations in Workflow-Canvas.

**Q14: Explain the difference between props and state.**  
A: Props are passed in from a parent (read-only); state is internal and mutable via setters. Changing state re-renders the component; changing props re-renders when the parent passes new values.

**Q15: What is the React Virtual DOM and why does it matter?**  
A: React keeps a lightweight in-memory tree and diffs it against the real DOM, applying only minimal updates. This boosts performance versus manual DOM manipulation.

**Q16: How do you manage global state in React?**  
A: Context API for small apps, Zustand/Redux for larger ones. Workflow-Canvas used Zustand for node/edge state because it avoids boilerplate and re-render overhead.

**Q17: What are React keys and why are they important?**  
A: Keys help React identify list items across re-renders for efficient reconciliation. Use stable IDs, not array indices, to avoid bugs when lists reorder.

**Q18: Describe the CSS box model.**  
A: Content + padding + border + margin. `box-sizing: border-box` makes width include padding/border, which I set globally to simplify layouts.

**Q19: How do you make a layout responsive / mobile-first?**  
A: Write base styles for small screens, then use `min-width` media queries to enhance. Tailwind's `sm:`/`md:`/`lg:` prefixes do this declaratively; I used them in SaaS Video Editor.

**Q20: What is the difference between `let`, `const`, and `var`?**  
A: `var` is function-scoped and hoisted; `let`/`const` are block-scoped. `const` prevents reassignment (not deep immutability). I default to `const`.

**Q21: Explain ES6 features you use daily.**  
A: Arrow functions, template literals, destructuring, spread/rest, `Promise`/`async-await`, and modules. Example:

```js
const { id, ...rest } = user;
const updated = { ...rest, active: true };
```

**Q22: What are closures in JavaScript?**  
A: A closure is a function that retains access to its lexical scope even after the outer function returns. Useful for factories, memoization, and React event handlers.

**Q23: How do you prevent unnecessary re-renders in React?**  
A: Memoize with `React.memo`, `useMemo`, `useCallback`, and keep state local. Avoid inline objects/functions passed to memoized children.

**Q24: What is the difference between `useEffect` and `useLayoutEffect`?**  
A: `useEffect` runs after paint; `useLayoutEffect` runs synchronously before paint. Use layout effect for DOM measurements to avoid flicker, otherwise prefer `useEffect`.

**Q25: How do you handle forms in React?**  
A: Controlled inputs with `useState` or libraries like React Hook Form. Validate on submit and on blur; my GuardrailZ settings form uses controlled state with regex validation.

**Q26: What are semantic HTML5 elements and why use them?**  
A: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>` improve accessibility and SEO. I use them for structure and ARIA roles.

**Q27: Explain CSS Flexbox vs Grid.**  
A: Flexbox lays out items in one dimension (row/column); Grid is two-dimensional. I use Flexbox for navbars/toolbars and Grid for app dashboards.

**Q28: How do you optimize frontend performance?**  
A: Code-splitting (`next/dynamic`), lazy loading images (Cloudinary), memoization, debouncing, and minimizing bundle size. Vercel's analytics help spot slow routes.

**Q29: What is a Promise and how does async/await work?**  
A: A Promise represents an async result with `.then/.catch`; `async/await` is syntactic sugar over it for readable sequential code.

```js
const res = await fetch("/api/users");
const data = await res.json();
```

**Q30: How do you debug a React app?**  
A: React DevTools for component/state inspection, browser DevTools for network/console, and `console.log`/breakpoints. I also add error boundaries to catch render crashes.

---

## 3. Backend: Node.js, RESTful APIs, Serverless (Q31–Q48)

**Q31: How do you structure an Express.js application?**  
A: Routes → controllers → services → models, with middleware for auth/validation/error-handling. I separate concerns so each file has a single responsibility.

**Q32: What makes a RESTful API "RESTful"?**  
A: Resource-oriented URLs, HTTP verbs (GET/POST/PUT/DELETE), statelessness, and JSON payloads. Example: `GET /api/posts`, `POST /api/posts`, `DELETE /api/posts/:id`.

**Q33: How do you handle errors in a Node backend?**  
A: Centralized error middleware that maps exceptions to status codes and logs them, returning a consistent JSON error shape.

```js
app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ error: err.message });
});
```

**Q34: Explain middleware in Express.**  
A: Functions with `(req, res, next)` that run in sequence—logging, auth, validation, body parsing. They can short-circuit or call `next()` to continue.

**Q35: What is the difference between authentication and authorization?**  
A: Authentication verifies who you are (JWT/OAuth login); authorization checks what you can do (roles/permissions). GuardrailZ uses Clerk for auth and gated features by plan/role.

**Q36: How do you implement JWT authentication in Node?**  
A: Sign a token on login with a secret, send it in `Authorization: Bearer` header, and verify via middleware using `jsonwebtoken`.

```js
const token = jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: "1d" });
```

**Q37: What are serverless functions and how have you used them?**  
A: Single-purpose functions invoked on demand (Vercel/Netlify Functions, AWS Lambda). My Next.js API routes on Vercel are serverless; FastAPI endpoints also ran as containers behind ECS.

**Q38: How do you validate incoming API requests?**  
A: Use schema validators like Zod or Joi on the body/params. This prevents bad data reaching the DB and returns clear 400 errors.

```tsx
const Schema = z.object({ email: z.string().email() });
```

**Q39: Explain the event loop in Node.js.**  
A: Node runs a single-threaded event loop handling async I/O via callbacks/promises without blocking. CPU-heavy work should be offloaded to workers or external services.

**Q40: How do you rate-limit an API?**  
A: Use `express-rate-limit` or API gateway limits, keyed by IP or token, to prevent abuse. Useful for public endpoints like GuardrailZ' guardrail check API.

**Q41: What is idempotency and why does it matter for APIs?**  
A: Repeated identical requests produce the same result. Achieve via idempotency keys for payments/POSTs so retries don't double-create resources.

**Q42: How do you version a REST API?**  
A: URL prefix (`/api/v1/...`) or header versioning. I prefer URL versioning for clarity and easy deprecation.

**Q43: How would you upload files in a full-stack app?**  
A: Frontend sends `FormData`; backend stores to Cloudinary/S3 and saves the URL in DB. My projects use Cloudinary for images/video with signed uploads.

**Q44: What is the difference between SQL and NoSQL databases (conceptually)?**  
A: SQL (PostgreSQL) is relational with schemas and joins; NoSQL (MongoDB) is document-based and flexible. Choice depends on data relationships vs. schema velocity.

**Q45: How do you write a clean controller vs service layer?**  
A: Controllers parse requests and format responses; services contain business logic and DB calls. This keeps routes thin and testable.

**Q46: How do you test backend APIs?**  
A: Unit tests for services (Jest/Vitest) and integration tests hitting routes with Supertest. Sim Studio had pytest/unit tests I contributed to for SSRF handling.

**Q47: What are WebSockets and when vs REST?**  
A: WebSockets are persistent bidirectional channels for real-time; REST is request/response. Use WebSockets for chat/live cursors, REST for CRUD.

**Q48: How do you secure a Node API against common attacks?**  
A: Validate input, use helmet, sanitize, rate-limit, avoid SQL injection (parameterized queries), and prevent SSRF (whitelist URLs). I added localhost/SSRF protections in Sim Studio.

---

## 4. Databases: PostgreSQL, Supabase, MongoDB (Q49–Q66)

**Q49: When would you choose PostgreSQL over MongoDB?**  
A: When data is relational, needs transactions/ACID, and complex joins (users, orders, roles). Supabase (Postgres) fits the role's scalable DB requirement.

**Q50: What is a primary key and foreign key?**  
A: Primary key uniquely identifies a row; foreign key links to another table's primary key, enforcing relationships.

```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id)
);
```

**Q51: Explain indexes and when to use them.**  
A: Indexes speed up lookups on frequently queried columns but slow writes. Add them on FK and filter columns; avoid over-indexing.

**Q52: What are SQL joins? Give an example.**  
A: Joins combine rows from tables. `INNER JOIN` returns matching rows; `LEFT JOIN` includes unmatched left rows.

```sql
SELECT u.name, p.title
FROM users u JOIN posts p ON p.user_id = u.id;
```

**Q53: What is normalization?**  
A: Organizing tables to reduce redundancy (1NF–3NF) via separate related entities. Trade-off: too much normalization adds join cost; denormalize selectively for read-heavy paths.

**Q54: How do you handle migrations?**  
A: Use tools like Supabase migrations, Prisma, or Alembic (Python). Track schema changes in version control so they're reproducible across environments.

**Q55: What is Supabase and how is it different from raw Postgres?**  
A: Supabase is a hosted Postgres platform with auth, realtime, storage, and auto REST/GraphQL APIs. It speeds up full-stack builds with row-level security.

**Q56: Explain Row Level Security (RLS) in Supabase.**  
A: RLS policies enforce per-row access at the DB level, so users only see/edit their own data—critical for multi-tenant apps.

```sql
CREATE POLICY "own rows" ON posts
USING (auth.uid() = user_id);
```

**Q57: How do you model a many-to-many relationship?**  
A: A join table with two FKs. Example: `user_roles(user_id, role_id)` linking users to roles.

**Q58: What is a document in MongoDB?**  
A: A BSON object (like JSON) stored in a collection, schema-flexible. Good for evolving or hierarchical data like session logs.

**Q59: How do you query MongoDB?**  
A: Using the driver or Mongoose with filter objects:

```js
db.users.find({ active: true }, { name: 1 });
```

**Q60: When is MongoDB a better fit than Postgres?**  
A: For unstructured/semi-structured data, rapid schema changes, or document-centric models (e.g., chat messages, telemetry). I used MongoDB alongside Postgres depending on need.

**Q61: What is an aggregation pipeline in MongoDB?**  
A: A sequence of stages (`$match`, `$group`, `$project`) for transform/group data server-side.

```js
db.orders.aggregate([
  { $match: { status: "paid" } },
  { $group: { _id: "$userId", total: { $sum: "$amount" } } }
]);
```

**Q62: How do you prevent SQL injection?**  
A: Use parameterized queries / ORMs (Prisma, pg with placeholders), never string-concatenate SQL. This is non-negotiable for production apps.

**Q63: What is connection pooling?**  
A: Reusing a set of DB connections instead of opening new ones per request, improving throughput. Both Postgres clients and Mongo drivers pool by default.

**Q64: How do you back up and restore a database?**  
A: Postgres: `pg_dump`/`pg_restore` or Supabase snapshots; Mongo: `mongodump`/`mongorestore`. Automate backups and test restores.

**Q65: Explain transactions and ACID.**  
A: A transaction groups operations that must all succeed or all fail (Atomicity, Consistency, Isolation, Durability). Postgres supports them natively; Mongo supports multi-doc transactions.

**Q66: How do you design a scalable schema for a SaaS app?**  
A: Tenant isolation (e.g., `org_id` on rows + RLS), indexed FKs, soft deletes, and audit columns. Plan for read replicas and caching (Redis) on hot paths.

---

## 5. Cloud & Deployment: Vercel, Serverless, Edge, Performance (Q67–Q80)

**Q67: Why is Vercel a good fit for this role?**  
A: Vercel gives zero-config Next.js deploys, serverless/edge functions, preview deployments, and performance analytics—exactly the optimization-focused deployment the role wants. I've shipped multiple apps there.

**Q68: What is the difference between serverless and edge functions?**  
A: Serverless functions run in a Node runtime near a region; edge functions run globally at the CDN for low latency, ideal for auth/redirects/AB testing.

**Q69: How do you optimize a Next.js app for performance?**  
A: Use SSR/SSG where possible, `next/image` for optimized images, dynamic imports for heavy components, and minimize client JS. SaaS Video Editor benefits from these on Vercel.

**Q70: What are preview deployments and how do you use them?**  
A: Vercel creates a unique URL per PR for testing before merge. I review UI changes via previews and run checks before promoting to production.

**Q71: How do you set up CI/CD?**  
A: GitHub Actions run lint/test/build on PRs; Vercel auto-deploys on merge. My Agentic AI internship used GitHub Actions + Docker for CI/CD.

```bash
# .github/workflows/ci.yml
- run: npm ci && npm test && npm run build
```

**Q72: How do you manage environment variables across environments?**  
A: Local `.env.local`, Vercel project env for preview/production, and secrets in the platform. Never commit real secrets; use placeholders in docs.

**Q73: What is caching and where do you apply it?**  
A: Caching stores results to avoid recomputation—CDN caching, Redis for API responses, and React Query for client cache. I used Redis in the Agentic AI internship for hot data.

**Q74: How do you monitor a deployed app?**  
A: Vercel Analytics/Web Vitals, error tracking (Sentry), and logging. Set alerts on 5xx rates and slow p95 latency.

**Q75: What is lazy loading and code splitting?**  
A: Splitting bundles so code loads on demand (`next/dynamic`, `React.lazy`). Reduces initial load, improving LCP on mobile.

**Q76: How do you handle a production incident?**  
A: Check dashboards/logs, identify scope, roll back if needed (Vercel instant rollback), patch, and write a postmortem. Stay calm and communicate status.

**Q77: What are Web Vitals and why do they matter?**  
A: LCP, INP, CLS measure loading, interactivity, and visual stability. They directly affect UX and SEO; I optimize them via image/JS/CLS fixes.

**Q78: How do you secure a deployment?**  
A: HTTPS everywhere (Vercel default), secure headers (CSP, HSTS via `next.config`/middleware), secret management, and least-privilege DB access.

**Q79: Explain Docker's role in your workflow.**  
A: Docker containerizes apps for consistent dev/prod parity; I used it for FastAPI microservices in the Agentic AI internship and CI pipelines.

**Q80: How would you reduce cold-start latency on serverless?**  
A: Keep bundles small, minimize dependencies, use edge functions for light tasks, and warm critical paths. Avoid heavy init outside handlers.

---

## 6. AI-Assisted Dev Tools & GenAI/LLM Awareness (Q81–Q92)

**Q81: How do you use Cursor (GenAI IDE) to code faster?**  
A: I use Cmd-K for inline edits, Chat for scaffolding, and `@` context to reference files/repos. It accelerates boilerplate and refactoring while I review every diff for correctness.

**Q82: How have you used Lovable / Vercel V0 / Replit?**  
A: V0 for component drafts, Lovable for quick full-stack prototypes, Replit for throwaway backends. I then move generated code into a proper repo with tests and type-safety.

**Q83: What is GuardrailZ and what did you build?**  
A: GuardrailZ is an LLM guardrails tool (Next.js + Clerk + regex) deployed live. It filters/validates prompts and outputs using regex and policy rules—direct AI-safety experience relevant to an AI company.

**Q84: Explain prompt injection and how to mitigate it.**  
A: Attackers embed instructions to hijack an LLM. Mitigate by input sanitization, separating system/user content, output validation (like GuardrailZ), and least-privilege tool access.

**Q85: Describe your BERT/VADER chatbot experience.**  
A: In my Data Science internship I built a Python chatbot using BERT (transformers) and VADER for sentiment, with a Streamlit UI—showing I understand NLP and LLM-adjacent stacks.

**Q86: What SSRF protection did you add in Sim Studio?**  
A: I restricted outbound requests to safe hosts, blocked localhost/metadata endpoints, and added tests for localhost HTTP handling to prevent server-side request forgery in tool-calling agents.

**Q87: How would you integrate a third-party LLM API safely?**  
A: Keep API keys server-side (Vercel env), rate-limit, validate inputs/outputs, and add guardrails. Never expose keys to the client; proxy through a serverless function.

**Q88: What is retrieval-augmented generation (RAG)?**  
A: Augmenting an LLM with retrieved context from a vector store/DB to ground answers. Relevant if Everything About AI builds knowledge-based AI features.

**Q89: How do you evaluate or test AI/agent features?**  
A: Unit-test tool calls and guards (as in Sim Studio), add eval datasets for outputs, and log traces. Guardrails like regex give deterministic, testable checks.

**Q90: What are agentic workflows and have you built them?**  
A: Agents chain LLM calls with tools/state to accomplish goals. I built FastAPI-based AI agents with auth and tool use during internships, plus contributed to Sim Studio (agent orchestration OSS).

**Q91: How do you keep AI-generated code safe and correct?**  
A: Treat it like any code: review diffs, run lint/tests/typecheck, and verify security (no secrets, no unsafe URLs). AI speeds drafting; I own final correctness.

**Q92: Why is AI awareness valuable for a full-stack intern here?**  
A: Everything About AI builds AI products; my GuardrailZ, BERT/VADER, and Sim Studio work mean I can ship both the app and the AI safety/integration layer, not just CRUD.

---

## 7. Git, Collaboration, Code Reviews & Best Practices (Q93–Q99)

**Q93: What Git branching strategy do you use?**  
A: Feature branches off `main`, PRs with reviews, and squash/merge. I use `main`/`dev` plus short-lived `feature/*` branches.

**Q94: How do you resolve a merge conflict?**  
A: Pull latest, open the conflicted files, choose/keep correct changes (often both), test, then commit. I rely on the editor's 3-way merge view in Cursor/VSCode.

**Q95: What makes a good code review?**  
A: Check correctness, security, tests, naming, and DX; comment constructively and approve only when green. I both give and act on review feedback from internships.

**Q96: How do you write a good commit message?**  
A: Imperative, short subject + body explaining why. Example: `fix: block localhost URLs in tool caller (SSRF)`.

**Q97: How do you use GitHub Actions effectively?**  
A: Automate test/lint/build, cache deps, and gate merges on checks. I set this up for FastAPI services with Docker in CI.

**Q98: What is the difference between `git rebase` and `merge`?**  
A: `merge` creates a merge commit preserving history; `rebase` reapplies commits onto a new base for a linear history. I rebase feature branches before PR to keep history clean.

**Q99: How do you onboard to an existing codebase quickly?**  
A: Read README/architecture, run it locally via Docker, trace one feature end-to-end, and check open issues/PRs. I did this when contributing to Sim Studio OSS.

---

## 8. Behavioral & "Why Everything About AI" / Three Rounds Prep (Q100)

**Q100: Why do you want the Full Stack Development Internship at Everything About AI, and how do you prepare for the three technical rounds?**  
A: I want to build end-to-end AI products with modern stacks (Next.js/Node/Supabase/Vercel) and sharpen GenAI tooling skills—my GuardrailZ, SaaS Video Editor, and Sim Studio work already match the stack. For the three rounds I prep by: (1) revising React/Node/DB fundamentals with code snippets, (2) building a small full-stack demo on Vercel with Supabase + serverless functions, and (3) practicing system-design and live coding in Cursor while articulating trade-offs clearly.
