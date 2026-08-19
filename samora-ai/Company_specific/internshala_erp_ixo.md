# ERP IXO — 100 Full Stack Interview Q&A

> Based on ERP IXO — Full Stack Development Internship (AI-driven ERP; AngularJS/React/Node.js/MongoDB/Python)  > Candidate: Aayush Gid (React/Next.js/Node/Express/Python FastAPI/MongoDB/AI guardrails background)

---

## 1. Full-Stack & ERP Fundamentals (Q1–Q10)

**Q1: What does a full-stack developer do on an ERP product, and how do you see the role?**  
A: A full-stack developer builds and maintains both the front-end (UI for inventory, dashboards) and back-end (APIs, business logic, data) of the ERP. At ERP IXO this means shipping features end-to-end — from a React screen down to a Node/Mongo service — while keeping the system fast and reliable.

**Q2: What is ERP and what are its core modules?**  
A: ERP (Enterprise Resource Planning) integrates business processes into one system. Core modules include inventory, procurement, sales, finance, HR, and manufacturing. ERP IXO adds AI layers like demand prediction and anomaly detection on top of these.

**Q3: Why is an ERP system different from a normal web app?**  
A: ERPs handle complex, interdependent business workflows, transactional consistency, role-based access, and large relational/operational data. They demand careful state management, audits, and scalability more than a typical CRUD app.

**Q4: Explain the request-response lifecycle of a typical ERP feature you'd build.**  
A: The browser (React) sends a request to a Node/Express REST endpoint, which validates input, runs business logic, queries MongoDB (or another store), and returns JSON. The UI then updates state and re-renders the relevant view.

```ts
// React -> fetch -> Express -> Mongo -> JSON
const res = await fetch("/api/inventory?sku=ABC");
const data = await res.json();
```

**Q5: What is a RESTful API and why is it used in ERP integration?**  
A: REST uses HTTP verbs (GET/POST/PUT/DELETE) with resource URLs and stateless requests. ERPs rely on REST to integrate modules and third-party systems cleanly and predictably.

**Q6: How do you keep front-end and back-end in sync during development?**  
A: Use a shared API contract (OpenAPI/Swagger), typed models (TypeScript interfaces shared or generated), and environment configs. I often define request/response types in TS and mirror them in FastAPI/Express schemas.

**Q7: What does "optimize for speed and scalability" mean for an ERP?**  
A: It means reducing latency (caching, indexing, pagination), minimizing payloads, and designing services that scale horizontally. For ERP IXO, that includes Redis caching of heavy analytics and indexed Mongo queries.

**Q8: Describe a feature you built end-to-end. How did you approach it?**  
A: For Workflow-Canvas I built a React/ReactFlow UI backed by a state store (Zustand) and persisted graphs via an API. I scoped the data model first, built the backend endpoints, then wired the UI, testing both together.

**Q9: How would you handle a bug reported in production ERP?**  
A: Reproduce it locally with the same data/inputs, check logs and stack traces, isolate the layer (UI/API/DB), add a failing test, fix, and verify before deploying. I use structured logging and Redis/DB inspection when needed.

**Q10: Why are code reviews important on a small internship team?**  
A: They catch bugs early, spread knowledge, and keep code consistent. As an intern I'd both request reviews on my PRs and give constructive feedback on others', which ERP IXO explicitly values.

---

## 2. HTML, CSS & JavaScript (ES6+) (Q11–Q22)

**Q11: What are semantic HTML tags and why use them?**  
A: Tags like `<header>`, `<main>`, `<table>` describe meaning, improving accessibility and SEO. ERP dashboards benefit from semantic tables and landmarks for screen readers.

**Q12: How do you make an ERP UI responsive with CSS?**  
A: Use flexbox/grid, media queries, and relative units. I prefer CSS modules or Tailwind (used in my SaaS Video Editor) for consistent, responsive layouts.

```css
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
```

**Q13: Difference between `let`, `const`, and `var`?**  
A: `var` is function-scoped and hoisted; `let` and `const` are block-scoped, with `const` preventing reassignment. I default to `const` and use `let` only when rebinding.

**Q14: What are arrow functions and how do they differ in `this` binding?**  
A: Arrow functions inherit `this` from their enclosing scope and are concise. Regular functions have their own `this`, which matters in event handlers and class methods.

```js
const add = (a, b) => a + b;
```

**Q15: Explain `map`, `filter`, and `reduce` with an example for ERP data.**  
A: They transform arrays declaratively. Use `filter` for rows meeting a threshold, `map` to project fields, and `reduce` to aggregate totals.

```js
const lowStock = items.filter(i => i.qty < i.reorderLevel)
  .map(i => i.sku);
const revenue = orders.reduce((s, o) => s + o.total, 0);
```

**Q16: What is the event loop in JavaScript?**  
A: JS runs single-threaded; the event loop processes the call stack then the callback/task queues (macrotasks, microtasks like Promises). Understanding it prevents blocking the UI in data-heavy ERP screens.

**Q17: How do `Promise` and `async/await` help with API calls?**  
A: They flatten asynchronous code. `async/await` makes fetch calls readable and lets me use `try/catch` for error handling instead of callback pyramids.

**Q18: What is the difference between `==` and `===`?**  
A: `==` does type coercion; `===` checks value and type strictly. I always use `===` to avoid surprising coercion bugs.

**Q19: How do you prevent layout thrashing in a data grid?**  
A: Batch DOM reads/writes, virtualize long lists, and avoid forced reflows in loops. Libraries like React Window help render only visible ERP rows.

**Q20: What are CSS variables and where are they useful?**  
A: Custom properties (`--primary`) enable theming and consistent design tokens. I use them for ERP theme switching (light/dark) without recompiling.

**Q21: Explain debouncing and where you'd use it in an ERP.**  
A: Debouncing delays a function until activity stops, reducing excessive calls. I use it on search/filter inputs hitting the API to avoid a request per keystroke.

```js
function debounce(fn, ms){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms);};}
```

**Q22: What is the difference between `localStorage` and `sessionStorage`?**  
A: `localStorage` persists until cleared; `sessionStorage` clears when the tab closes. I store non-sensitive UI prefs (filters) locally, never tokens — those go to httpOnly cookies.

---

## 3. React.js (Q23–Q40)

**Q23: What is React and why is it a strong fit for ERP front-ends?**  
A: React is a component-based UI library with a virtual DOM for efficient updates. Its declarative model suits complex ERP dashboards with lots of interactive, stateful widgets.

**Q24: Functional components vs class components — which do you use?**  
A: I use functional components with hooks; they're simpler and the modern standard. Class components are legacy, though I can read/maintain them.

**Q25: Explain `useState` and `useEffect`.**  
A: `useState` holds local component state; `useEffect` runs side effects (fetching, subscriptions) after render with dependency control. I guard effects to avoid infinite loops.

```jsx
const [rows, setRows] = useState([]);
useEffect(() => { fetch("/api/orders").then(r=>r.json()).then(setRows); }, []);
```

**Q26: What is the dependency array in `useEffect`?**  
A: It controls when the effect re-runs: `[]` once, `[dep]` on change, omitted every render. Wrong deps cause stale data or loops — a common ERP bug.

**Q27: How do you manage global state in React?**  
A: For small apps, Context; for complex ERP state, Zustand or Redux. I used Zustand in Workflow-Canvas for graph/node state — lightweight and performant.

**Q28: What are React keys and why do they matter in lists?**  
A: Keys help React identify items across renders for efficient diffing. Use stable IDs (not array index) to avoid UI bugs when rows reorder or filter.

**Q29: How do you optimize a slow React dashboard?**  
A: Memoize with `useMemo`/`React.memo`, virtualize long lists, paginate server-side, and debounce inputs. At ERP IXO I'd also cache responses in Redis behind the API.

**Q30: Explain prop drilling and how to avoid it.**  
A: Prop drilling passes data through many intermediate components. Avoid with Context or a state library (Zustand) so ERP modules share data without messy chains.

**Q31: What is React Router and how do you structure an ERP app's routes?**  
A: It handles client-side navigation. I structure routes by module (`/inventory`, `/analytics`) with lazy loading and protected routes for auth.

**Q32: How do you handle forms in React?**  
A: Controlled components with state, or libraries like React Hook Form for performance and validation. I validate on submit and on blur for good UX.

**Q33: What are hooks rules and why do they matter?**  
A: Call hooks at the top level (not in loops/conditions) and only in React functions. Breaking them causes unpredictable state — I lint with eslint-plugin-react-hooks.

**Q34: Explain `useContext` with an example.**  
A: It consumes a Context value without prop drilling. I use it for theme, auth user, and selected-tenant in multi-org ERP views.

```jsx
const user = useContext(AuthContext);
```

**Q35: How do you do error handling in React?**  
A: Use error boundaries for render errors and try/catch in async effects, showing fallback UI. I surface API errors via toast notifications.

**Q36: What is code-splitting and why use it?**  
A: It loads only needed JS per route via `React.lazy` + `Suspense`, speeding initial load. Important for large ERP bundles deployed on Vercel.

**Q37: Describe your Workflow-Canvas project and React skills shown.**  
A: Workflow-Canvas is a React + ReactFlow + Zustand visual editor where users build node graphs. It shows my ability with complex state, custom nodes, and performant canvas rendering — directly transferable to ERP flow builders.

**Q38: How would you build a real-time analytics widget in React?**  
A: Poll or use WebSockets/SSE from a Node service, update state with the latest metrics, and memoize charts. ERP IXO's real-time analytics fit this pattern.

**Q39: What is the Virtual DOM and how does React use it?**  
A: React keeps a lightweight in-memory DOM copy and diffs it to apply minimal real DOM changes. This makes frequent ERP data updates efficient.

**Q40: How do you test React components?**  
A: With React Testing Library + Jest/Vitest for behavior, and occasionally Playwright for E2E. I test user interactions, not implementation details.

---

## 4. AngularJS & React Native Basics (Transferable from React/TS) (Q41–Q52)

**Q41: I know React, not AngularJS — how transferable is my experience?**  
A: Very. Both are component-based, use one-way data flow concepts, and rely on services/modules. My React/TypeScript background maps to AngularJS controllers/services with a short learning curve.

**Q42: What is the basic structure of an AngularJS app?**  
A: It uses modules (`angular.module`), controllers, directives, and services, with two-way binding via `ng-model`. I'd adapt my React state mental model to its digest cycle.

```js
angular.module("erp", []).controller("InvCtrl", function($scope, $http){
  $http.get("/api/inventory").then(r => $scope.rows = r.data);
});
```

**Q43: How does two-way binding in AngularJS differ from React's one-way flow?**  
A: AngularJS auto-syncs view↔model via `$scope` digest; React is explicit (state → props → view). I'd note React's model is more predictable, which helps debugging ERP state.

**Q44: What are AngularJS directives?**  
A: They extend HTML with `ng-` attributes (`ng-repeat`, `ng-if`). Comparable to React components/JSX — I'd map `ng-repeat` to `.map()` rendering.

**Q45: What is a service/factory in AngularJS and why use it?**  
A: Singletons for shared logic/API calls, like React custom hooks or context providers. I'd use them for ERP data access and auth.

**Q46: How would you migrate an AngularJS view to React?**  
A: Replace templates with JSX, controllers with hooks, and services with API modules/hooks. I've done similar React↔Next transitions (GuardrailZ, SaaS Editor).

**Q47: What is React Native and how is it related to React?**  
A: React Native uses React's component model to build mobile apps with native UI via JavaScript. Same JSX/state/hooks knowledge transfers directly.

**Q48: How would you build an ERP mobile screen in React Native?**  
A: Use `View`/`Text`/`FlatList` components and fetch from the same Node REST APIs. My React skills cover 90% — mainly learning native components and navigation.

```jsx
<FlatList data={items} keyExtractor={i=>i.id}
  renderItem={({item}) => <Text>{item.sku}</Text>} />
```

**Q49: Difference between React (web) and React Native rendering?**  
A: Web renders DOM elements; RN renders native iOS/Android components. Logic, hooks, and API code are shared — only the view layer differs.

**Q50: What is Expo in React Native?**  
A: A framework/toolchain that simplifies RN development (builds, OTA updates). I'd use it to prototype ERP mobile features quickly.

**Q51: How do you handle navigation in React Native?**  
A: With React Navigation, defining stack/tab navigators. The concept mirrors React Router I already know.

**Q52: Given you lack AngularJS/RN experience, how will you ramp up fast?**  
A: I'll lean on my React/TypeScript fundamentals, read ERP IXO's existing code, build a small practice component, and pair in code reviews. My fast learning is proven by SIH finals and rapid OSS contributions (Sim Studio).

---

## 5. Node.js, Express & REST APIs (Q53–Q66)

**Q53: What is Node.js and why use it for ERP back-ends?**  
A: Node.js runs JavaScript server-side on an event loop, great for I/O-heavy APIs. With Express I can build fast REST services that share types with the React front-end.

**Q54: How do you structure an Express app?**  
A: Routes → controllers → services → data layer, with middleware for auth/logging/error handling. I follow this in my FastAPI/Express work.

```js
app.get("/api/inventory", auth, async (req, res, next) => {
  try { res.json(await Inventory.list(req.query)); }
  catch (e) { next(e); }
});
```

**Q55: What is middleware in Express?**  
A: Functions that run before handlers (auth, CORS, logging, error handling). I use them for JWT verification and request validation.

**Q56: How do you handle errors centrally in Express?**  
A: An error-handling middleware with `(err, req, res, next)` that formats a consistent JSON error and logs it. Avoids leaking stack traces to clients.

**Q57: Explain JWT authentication.**  
A: The server signs a token (header.payload.signature) the client sends in `Authorization: Bearer`. I verify it in middleware; for ERP I'd prefer httpOnly cookies + refresh tokens.

**Q58: How do you validate incoming API requests?**  
A: With schema libraries (Joi/Zod on Node, Pydantic on FastAPI). I validate at the boundary to protect the DB and return clear 400 errors.

**Q59: What are the differences between REST and GraphQL?**  
A: REST exposes fixed resources; GraphQL lets clients query exactly the fields they need. For ERP, REST is simpler; GraphQL helps complex dashboards reduce round-trips.

**Q60: How do you implement pagination for large ERP tables?**  
A: Cursor or offset/limit with total counts. I return `{ data, page, total }` and the UI shows paginated grids.

```js
const page = +req.query.page || 1, limit = 20;
const data = await Inventory.find().skip((page-1)*limit).limit(limit);
```

**Q61: How would you rate-limit an API?**  
A: Use `express-rate-limit` (or API gateway) keyed by IP/user to prevent abuse. Important for public ERP endpoints.

**Q62: How do you secure secrets in a Node app?**  
A: Store in `.env` (never committed), load via `dotenv`, and use a secrets manager in prod. I never hardcode DB URIs or JWT secrets.

**Q63: What is CORS and how do you configure it?**  
A: CORS controls which origins can call your API. I set allowed origins explicitly (the ERP front-end domain), not `*`, especially with credentials.

**Q64: How do you handle async errors in Node without crashing?**  
A: Wrap handlers in try/catch, use `await` properly, and a process-level `uncaughtException`/`unhandledRejection` handler plus a supervisor (Docker/PM2).

**Q65: Describe your FastAPI/Express backend experience relevant here.**  
A: At my Agentic AI internship I built FastAPI microservices with Docker, Redis caching, and JWT auth on AWS ECS. In another role I built FastAPI + SQLite with API auth. This transfers to ERP IXO's Node/Express + Mongo stack.

**Q66: How would you design a REST endpoint for "predict demand" in ERP?**  
A: `POST /api/forecast/demand` with `{ sku, horizon }`, the service calls the ML model and returns predictions with confidence. I'd cache results in Redis for repeat queries.

---

## 6. MongoDB (Q67–Q78)

**Q67: Why is MongoDB a good fit for ERP data?**  
A: Its flexible documents suit evolving ERP schemas, and it scales horizontally. I've used MongoDB alongside Postgres/MySQL, so I know when to choose each.

**Q68: What is a document in MongoDB and how does it compare to SQL rows?**  
A: A BSON document is a flexible JSON-like record vs a fixed SQL row. Related data can be embedded or referenced depending on access patterns.

**Q69: How do you model one-to-many relationships in Mongo?**  
A: Embed arrays for small, always-fetched data; reference IDs for large/sub-collections. For orders→line items I'd likely embed line items in the order doc.

**Q70: Write a basic Mongo query to find low-stock items.**  
A:

```js
db.inventory.find({ qty: { $lt: "$reorderLevel" } });
// or with aggregation comparing two fields
db.inventory.aggregate([
  { $match: { $expr: { $lt: ["$qty", "$reorderLevel"] } } }
]);
```

**Q71: What are indexes and why are they critical for ERP?**  
A: Indexes speed up queries on filtered/sorted fields. I'd index `sku`, `createdAt`, and frequently queried fields to keep dashboards fast.

**Q72: How do you perform aggregations in MongoDB?**  
A: Using the aggregation pipeline (`$match`, `$group`, `$sort`). Great for ERP reports like total sales per region.

```js
db.orders.aggregate([
  { $group: { _id: "$region", total: { $sum: "$amount" } } }
]);
```

**Q73: What is the MongoDB Node driver vs Mongoose?**  
A: The native driver is lightweight; Mongoose adds schemas, validation, and middleware (ODM). I've used both; Mongoose speeds development with validation.

**Q74: How do you ensure data consistency without transactions in Mongo?**  
A: Use MongoDB transactions for multi-document updates when needed (it supports them on replica sets). For single docs, atomic updates suffice.

**Q75: How would you back up a MongoDB ERP database?**  
A: Use `mongodump`/Atlas snapshots and scheduled backups, plus oplog for point-in-time recovery. Critical for financial ERP data.

```bash
mongodump --uri="$MONGO_URI" --out=/backup/$(date +%F)
```

**Q76: What is the aggregation `$lookup` and when do you use it?**  
A: It's a left outer join between collections. I'd use it to join orders with customer details for reporting without embedding everything.

**Q77: How do you handle schema changes in MongoDB over time?**  
A: Write migration scripts (or use Mongoose versioning) and make reads tolerant of missing fields. Flexible schema still needs disciplined migrations in ERP.

**Q78: How would you optimize a slow Mongo query in an ERP report?**  
A: Add/check indexes with `explain()`, project only needed fields, paginate, and cache results in Redis. Avoid full-collection scans on large tables.

---

## 7. Python & FastAPI (Q79–Q89)

**Q79: ERP IXO lists Python — how does your FastAPI experience transfer to their Node stack?**  
A: FastAPI and Express share REST concepts: routing, middleware, dependency injection, validation (Pydantic ≈ Zod), and async. I can contribute Python services (e.g., ML/analytics) and ramp on Node quickly.

**Q80: What is FastAPI and why do you like it?**  
A: FastAPI is a modern Python async web framework with auto OpenAPI docs and Pydantic validation. I built multiple production services with it (GuardrailZ, agent backends).

```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
async def health(): return {"status": "ok"}
```

**Q81: How do you do auth in FastAPI?**  
A: With `OAuth2PasswordBearer` + JWT (or Clerk on Next.js). I've implemented JWT/OAuth in both FastAPI and Node, so the pattern is familiar.

**Q82: How would you build an anomaly-detection endpoint in Python for ERP?**  
A: Load a trained model (scikit-learn/PyTorch), accept metrics, return anomaly score/flag. My BERT/VADER and face-mask ML work shows I can own this pipeline.

**Q83: Explain Pydantic and its role.**  
A: Pydantic validates and types request/response models at runtime. It's the Python equivalent of Zod — I rely on it to enforce ERP API contracts.

**Q84: How do you structure a FastAPI project?**  
A: Routers (per module), dependencies (DB/auth), schemas (Pydantic), services, and a main app. Mirrors my Express layering.

**Q85: What Python libraries have you used for data/ML?**  
A: Pandas, scikit-learn, transformers (BERT), VADER, NumPy. I built a BERT/VADER chatbot and a face-mask detection model (IEEE-published).

**Q86: How do you call a Python ML service from a Node ERP backend?**  
A: Via HTTP (the Python service exposes a REST API) or a message queue. I'd keep ML in a separate FastAPI service and have Node consume its predictions.

**Q87: How do you test Python services?**  
A: Pytest with fixtures, plus `httpx`/`TestClient` for API tests. I added tests in Sim Studio OSS, including SSRF/security cases.

**Q88: Describe the GuardrailZ project and its relevance to ERP IXO's AI focus.**  
A: GuardrailZ is a live LLM guardrails system (Next.js + Clerk + regex rules) that filters unsafe model output. It shows I can build AI-safety features — relevant to ERP IXO's trustworthy AI (anomaly flagging, safe automation).

**Q89: How would you containerize a Python service with Docker?**  
A: A multi-stage Dockerfile with a slim Python base, `pip install` from requirements, and a non-root user; I used this in my Agentic AI internship CI/CD.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0"]
```

---

## 8. AI/ML & Analytics for ERP (Q90–Q96)

**Q90: ERP IXO is AI-driven — what AI features would you build for an ERP?**  
A: Demand forecasting, anomaly flagging (e.g., unusual spend), and process automation. My ML background (BERT, VADER, forecasting) maps directly to these.

**Q91: How would you approach inventory demand prediction?**  
A: Collect historical sales/seasonality, engineer features, train a time-series or gradient-boosted model, and serve predictions via an API with confidence intervals. Cache to avoid recompute.

**Q92: What is anomaly detection and how would you flag ERP anomalies?**  
A: It identifies outliers from expected patterns (statistical thresholds or ML). I'd compute z-scores or use isolation forests on metrics like transaction volume and alert when breached.

**Q93: How do you keep AI predictions trustworthy in a business system?**  
A: Version models, log inputs/outputs, show confidence, and allow human override — exactly the guardrail thinking from GuardrailZ.

**Q94: Explain the difference between rules-based and ML-based automation.**  
A: Rules are explicit `if-then` logic (simple, explainable); ML learns patterns from data (handles complexity). ERP often blends both — rules for hard constraints, ML for predictions.

**Q95: How would you visualize real-time analytics in an ERP?**  
A: Stream metrics via WebSocket/SSE into React charts, debounced and memoized. I built real-time-style dashboards and can extend them with ERP data.

**Q96: What role does data quality play in ERP AI?**  
A: Garbage-in-garbage-out — dirty data ruins forecasts. I'd enforce validation at ingestion (Pydantic/Zod) and monitor drift, reflecting my data-science discipline.

---

## 9. Testing, Deployment, DevOps & Code Reviews (Q97–Q99)

**Q97: How do you test a full-stack ERP feature before deploy?**  
A: Unit tests for logic, API tests (Vitest/Pytest), and E2E (Playwright) for critical flows, plus manual checks on staging. I added tests in Sim Studio including security cases.

**Q98: Describe your CI/CD and deployment experience.**  
A: I use GitHub Actions for CI (lint, test, build) and deploy to Vercel/Render/Docker. At my internship I containerized FastAPI services and shipped via GitHub Actions — directly useful for ERP IXO's deploy pipeline.

```bash
# GitHub Actions snippet
- run: npm ci && npm test
- run: docker build -t erp-api . && docker push ...
```

**Q99: What do you look for when reviewing a teammate's code?**  
A: Correctness, security (auth/secrets/input validation), performance (N+1 queries, missing indexes), tests, and readability. I give specific, kind feedback and appreciate the same on mine.

---

## 10. Behavioral — Why ERP IXO & Remote Readiness (Q100)

**Q100: Why ERP IXO and how ready are you for WFH, 6 days/week, and possible late-night remote meetings?**  
A: ERP IXO combines full-stack work with AI — exactly my stack (React/Node/Python/Mongo) and interest (GuardrailZ, ML). I've worked remotely across time zones (Agentic AI internship, AWS ECS deployments) and am disciplined with async updates, so late-night meetings and a 6-day week are manageable.
