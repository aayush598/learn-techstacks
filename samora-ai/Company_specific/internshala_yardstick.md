# Yardstick — 100 Full Stack Interview Q&A

> Based on Yardstick — Full Stack Development Internship (MERN/Next.js, AWS, AI integration)  > Candidate: Aayush Gid (Python/FastAPI/Next.js/React/MongoDB/AI guardrails background)

---

## 1. Full Stack & MERN/Next.js Fundamentals (Q1–Q14)

**Q1: What does the MERN stack consist of, and how do the pieces fit together?**  
A: MERN stands for MongoDB, Express.js, React, and Node.js. MongoDB stores JSON-like documents, Express + Node serve the REST API, and React renders the UI — all using JavaScript end-to-end, which reduces context switching.

**Q2: How does Next.js differ from a plain React SPA?**  
A: Next.js adds file-based routing, server-side rendering (SSR), static site generation (SSG), and API routes in one framework. This improves SEO and initial load time versus a client-only SPA that fetches everything in the browser.

**Q3: What are the different rendering strategies in Next.js (SSR, SSG, ISR, CSR)?**  
A: SSR renders on each request (`getServerSideProps`/`dynamic` with `ssr:false`), SSG pre-renders at build time (`getStaticProps`), ISR revalidates static pages on a schedule (`revalidate`), and CSR is client-rendered. Choose based on data freshness vs. performance needs.

**Q4: Explain the full lifecycle of a feature you built at Yardstick-style work, from idea to production.**  
A: I'd clarify requirements, design the API/DB schema, implement backend (FastAPI/Express) and frontend (React/Next), write tests, containerize with Docker, set up CI/CD (GitHub Actions), deploy (Vercel/AWS), then monitor and document via README/Notion.

**Q5: What is the difference between a monolith and microservices, and when would you pick each?**  
A: A monolith is one deployable unit (simpler, faster to start). Microservices split by domain (scalable, resilient, more ops overhead). For an internship-scale AI product, I'd start monolithic (Next.js + API) and split only when a service needs independent scaling.

**Q6: What is a REST API and its core constraints?**  
A: REST uses HTTP verbs (GET/POST/PUT/DELETE), statelessness, resource-oriented URLs, and representational data (JSON). Statelessness means each request carries all needed info — no server session, which aids scalability.

**Q7: GET vs POST — when do you use each?**  
A: GET retrieves data (idempotent, cacheable, params in URL). POST creates/ submits data (not cached, body payload). Use GET for fetches, POST for mutations like login or uploads.

**Q8: What is the difference between SQL and NoSQL databases?**  
A: SQL (PostgreSQL/MySQL) is relational with schemas and joins; NoSQL (MongoDB) is document-based, schema-flexible, horizontally scalable. I pick MongoDB for rapidly evolving AI app data and PostgreSQL when relational integrity matters.

**Q9: What is npm, and what is the difference between dependencies and devDependencies?**  
A: npm is the Node package manager. `dependencies` ship to production (React, Express); `devDependencies` are build/test tools (Jest, ESLint) excluded from prod bundles.

**Q10: What is package.json and what key fields does it hold?**  
A: It defines project metadata, `scripts` (start/build/test), `dependencies`, and `devDependencies`. Example:
```json
{ "name": "app", "scripts": { "dev": "next dev" }, "dependencies": { "next": "^14" } }
```

**Q11: What is CORS and how have you handled it?**  
A: CORS controls which origins can call your API. I enable it via Express `cors` middleware or Next.js config, restricting `origin` to the frontend domain rather than `*`.

**Q12: What are environment variables and why keep secrets out of code?**  
A: They externalize config (DB URLs, API keys). I use `.env` (gitignored) and Vercel/AWS Secrets, never committing keys — a lesson reinforced by security work on Sim Studio.

**Q13: What is the difference between `let`, `const`, and `var` in JavaScript?**  
A: `var` is function-scoped and hoisted; `let`/`const` are block-scoped. `const` prevents reassignment (not deep immutability). I default to `const`, then `let`.

**Q14: How do you keep code clean and maintainable on a team?**  
A: Consistent linting/formatting (ESLint/Prettier), small PRs, clear naming, typed interfaces (TypeScript), and up-to-date docs. I practiced this across GuardrailZ and Sim Studio OSS contributions.

---

## 2. React & TypeScript (Q15–Q30)

**Q15: What are React hooks, and name the most common ones?**  
A: Hooks let function components use state/lifecycle: `useState`, `useEffect`, `useContext`, `useRef`, `useMemo`, `useReducer`. They replaced class components for most logic.

**Q16: Explain `useEffect` and its dependency array.**  
A: It runs side effects after render. `[]` runs once, `[dep]` on change, no array runs every render. Missing deps cause stale closures:
```js
useEffect(() => { fetchUser(id) }, [id]);
```

**Q17: What is the difference between Controlled and Uncontrolled components?**  
A: Controlled inputs derive value from React state (`value={state}`); uncontrolled use `ref` and the DOM. I use controlled for validation-heavy forms (e.g., GuardrailZ settings).

**Q18: How does React state update and why is it async?**  
A: `setState` is batched and asynchronous for performance. Don't read state immediately after setting it — use the updater form for dependent updates: `setCount(c => c + 1)`.

**Q19: What are keys in React lists and why do they matter?**  
A: Keys identify elements across renders so React can reconcile efficiently. Use stable unique IDs, not array indexes, to avoid bugs when reordering.

**Q20: What is prop drilling and how do you avoid it?**  
A: Passing props through many layers. Avoid with Context API, Zustand (used in Workflow-Canvas), or a state manager. Zustand kept my canvas state clean without boilerplate.

**Q21: What is the Context API and when would you use it?**  
A: It shares state (theme, auth user) without prop drilling. Use sparingly — overusing causes re-renders. I pair it with `useReducer` for auth state.

**Q22: Explain TypeScript generics with a short example.**  
A: Generics make functions/types reusable over types:
```ts
function identity<T>(v: T): T { return v; }
const x = identity<string>("hi");
```
I use them for typed API responses in Next.js.

**Q23: What is the difference between `interface` and `type` in TypeScript?**  
A: Both describe shapes. `interface` supports declaration merging and is ideal for objects/contracts; `type` can model unions, tuples, and primitives. I use `interface` for API DTOs.

**Q24: How do you handle forms and validation in React?**  
A: Controlled inputs + local validation, or libraries like React Hook Form + Zod. Zod gives typed schemas I reuse on client and server (e.g., GuardrailZ rule config).

**Q25: What are React Server Components (RSC)?**  
A: RSC run only on the server, sending minimal JS to the client — great for data fetching and reducing bundle size in Next.js App Router. They can't use browser-only hooks.

**Q26: What is the difference between Client and Server Components in Next.js App Router?**  
A: Server Components (default) execute on the server with direct DB/API access; Client Components (`"use client"`) run in the browser for interactivity. I keep data-fetching server-side and mark only interactive bits as client.

**Q27: How do you optimize React performance?**  
A: Memoization (`useMemo`/`React.memo`), code-splitting (`next/dynamic`), lazy loading, avoiding unnecessary re-renders, and virtualization for long lists.

**Q28: What is a custom hook and give an example use?**  
A: A reusable function starting with `use` that encapsulates logic:
```ts
function useLocalStorage(key: string) {
  const [v, setV] = useState(() => localStorage.getItem(key));
  // ...sync on change
  return [v, setV] as const;
}
```

**Q29: How have you used Zustand or similar state management?**  
A: In Workflow-Canvas I used Zustand to manage nodes/edges from ReactFlow — lightweight, no providers, and selectors prevented unnecessary re-renders versus Redux boilerplate.

**Q30: What is Framer Motion and where have you used it?**  
A: A React animation library. I used it in the SaaS Video Editor for smooth transitions and drag interactions, improving perceived performance with declarative `motion.div` components.

---

## 3. Node.js, Express & REST APIs (Q31–Q46)

**Q31: What is Node.js and how does its event loop work?**  
A: Node is a JS runtime built on V8 with a non-blocking, event-driven loop. Async I/O (callbacks/Promises) lets one thread handle many requests — ideal for scalable APIs.

**Q32: What is the difference between `process.nextTick`, `setImmediate`, and `setTimeout`?**  
A: `process.nextTick` runs after current op, before I/O; `setImmediate` runs after I/O; `setTimeout` after a delay. They affect task ordering in the event loop phases.

**Q33: How do you structure an Express.js app?**  
A: Routes → controllers → services → models, with middleware for auth/logging/error handling. I keep routes thin and put logic in services for testability.

**Q34: What is middleware in Express?**  
A: Functions with `(req, res, next)` that run before handlers — for auth, CORS, logging, validation. Order matters; call `next()` to continue:
```js
app.use((req, res, next) => { console.log(req.method); next(); });
```

**Q35: How do you handle errors centrally in Express?**  
A: An error-handling middleware with four args `(err, req, res, next)` that formats responses and logs. Throw in async handlers via `try/catch` or `express-async-errors`.

**Q36: What is the difference between `==` and `===` in JS?**  
A: `==` does type coercion (`"1" == 1` is true); `===` is strict (no coercion). Always use `===` to avoid subtle bugs.

**Q37: Explain Promises and `async/await`.**  
A: A Promise represents future value with `.then/.catch`; `async/await` is syntactic sugar for readability:
```js
const data = await fetch(url).then(r => r.json());
```

**Q38: How would you design a scalable REST API for an AI feature?**  
A: Versioned routes (`/api/v1`), pagination, rate limiting, async job queues for heavy inference, caching (Redis), and clear typed contracts (OpenAPI/Zod).

**Q39: What is rate limiting and how have you implemented it?**  
A: Caps requests per IP to prevent abuse. In Express I use `express-rate-limit`; for AI endpoints I combine it with Redis counters for distributed limits.

**Q40: How do you validate incoming request data?**  
A: Schema validation with Joi/Zod on the server (never trust client). Example with Zod:
```ts
const schema = z.object({ prompt: z.string().min(1) });
```

**Q41: What is the difference between `PUT` and `PATCH`?**  
A: `PUT` replaces the whole resource; `PATCH` partially updates it. Use PATCH for editing one field of a user profile.

**Q42: How do you version your APIs?**  
A: URL versioning (`/api/v1/users`), header versioning, or content negotiation. URL versioning is simplest and most explicit for AI product iterations.

**Q43: What is idempotency and why does it matter for APIs?**  
A: An idempotent operation yields the same result on repeated calls (GET, PUT, DELETE). Critical for retries on payment/AI job submission to avoid double-charging or duplicate jobs.

**Q44: How do you handle file uploads in Node?**  
A: Multipart parsing via `multer` (Express) or streaming to Cloudinary/S3. I used Cloudinary for image uploads in SaaS projects with signed presets.

**Q45: What are WebSockets and when would you use them?**  
A: Full-duplex persistent connections for real-time (chat, live AI token streaming). In Node I use `socket.io` or native `ws`; useful for streaming LLM responses.

**Q46: How do you test Node/Express APIs?**  
A: Unit (Jest/Vitest) for services, integration (Supertest) hitting routes, and contract tests. I added Supertest coverage in Sim Studio to guard SSRF logic.

---

## 4. MongoDB & Databases (Q47–Q58)

**Q47: What is MongoDB and why choose it over SQL?**  
A: A document NoSQL DB storing BSON with flexible schemas — great for evolving AI app data (varied prompt/response shapes) and horizontal scaling via sharding.

**Q48: What is a document and a collection in MongoDB?**  
A: A collection holds documents (JSON-like objects with `_id`). Unlike tables/rows, documents in a collection can have different fields, enabling schema evolution.

**Q49: How do you model relationships in MongoDB — embedding vs referencing?**  
A: Embed for one-to-few, frequently-read-together data; reference (ObjectId) for one-to-many/large data. I embed user profile in a session doc but reference posts by ID.

**Q50: What is an index and why is it important?**  
A: Indexes speed queries by avoiding full scans. I add indexes on queried fields (`createIndex({ email: 1 })`), but avoid over-indexing writes. Compound indexes help filtered sorts.

**Q51: What is the aggregation pipeline?**  
A: A chain of stages (`$match`, `$group`, `$project`) for analytics:
```js
db.orders.aggregate([{ $match: { status: "paid" } }, { $group: { _id: "$user", total: { $sum: "$amt" } } }]);
```

**Q52: How do you prevent NoSQL injection?**  
A: Validate/sanitize inputs and avoid passing raw user objects into queries. Use typed schemas (Mongoose/Zod) and parameterize filters rather than string-built queries.

**Q53: What is the Mongoose ODM?**  
A: An abstraction over MongoDB providing schemas, validation, and middleware. I define models with typed fields and pre-save hooks for hashing passwords.

**Q54: How do you handle transactions in MongoDB?**  
A: Use replica-set transactions via `startSession()` + `withTransaction()` for multi-document atomicity. Needed when updating wallet + order together.

**Q55: What is the difference between `find()` and `findOne()`?**  
A: `find()` returns a cursor/array of matches; `findOne()` returns the first match or null. Use `findOne` for unique lookups like login.

**Q56: How do you paginate MongoDB results?**  
A: `skip()`/`limit()` for small sets, or cursor-based (`_id` range) for large/social feeds to avoid deep-skip slowdown:
```js
db.posts.find({ _id: { $gt: lastId } }).limit(20);
```

**Q57: When would you choose PostgreSQL over MongoDB (given your experience)?**  
A: When I need ACID guarantees, relational joins, or complex reporting. I used PostgreSQL/MySQL in earlier internships and MongoDB for flexible AI payloads.

**Q58: How do you back up and monitor a MongoDB database?**  
A: `mongodump` snapshots, managed backups on Atlas, and monitoring slow queries via the profiler. For prod I'd use Atlas auto-backups plus alerting.

---

## 5. Python, FastAPI & Backend (Q59–Q70)

**Q59: Why FastAPI and how does it compare to Flask?**  
A: FastAPI is async-native, auto-generates OpenAPI docs, and uses Pydantic for validation — faster and more typed than Flask. I built GuardrailZ and agent microservices on it.

**Q60: What is Pydantic and how do you use it?**  
A: A data validation library using Python type hints. FastAPI uses it for request/response models:
```python
class User(BaseModel):
    id: int
    name: str
```

**Q61: How do you define a route in FastAPI?**  
A:
```python
@app.post("/items")
async def create(item: Item):
    return {"ok": True}
```
Path/query params and body are typed and auto-validated.

**Q62: What is the difference between sync and async in FastAPI?**  
A: `async def` handles concurrent I/O (DB/HTTP calls) efficiently; use plain `def` for CPU-bound or blocking libs. I use async for external API calls to AI models.

**Q63: How do you structure a FastAPI microservice?**  
A: Routers (per domain), `schemas` (Pydantic), `services` (logic), `models` (ORM), `dependencies` (auth/DB), and a `main.py` assembling the app — the pattern I used in the Agentic AI internship.

**Q64: How do you handle auth in FastAPI?**  
A: OAuth2 password flow with JWT via `python-jose` + `passlib`, using `Depends` for protected routes. I implemented API-key and JWT auth in agent services.

**Q65: What is dependency injection in FastAPI?**  
A: `Depends()` provides reusable, testable components (DB sessions, current user). It keeps route handlers clean and centralizes cross-cutting logic.

**Q66: How did you use Redis in your backend projects?**  
A: For caching AI responses, rate-limit counters, and job queues (Celery/RQ). It cut latency on repeated prompts and shared state across ECS containers.

**Q67: Explain your BERT/VADER chatbot from the Data Science internship.**  
A: I built a sentiment-aware chatbot: VADER for fast lexicon sentiment, BERT (`transformers`) for deeper context, served via Streamlit + a Python API. It routed responses by detected emotion.

**Q68: How do you containerize a FastAPI app with Docker?**  
A:
```dockerfile
FROM python:3.11-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```
I built these for ECS deployment with multi-stage builds to shrink images.

**Q69: How do you run CI/CD for Python services?**  
A: GitHub Actions: lint (ruff/flake8), test (pytest), build image, push to registry, deploy to AWS ECS. This is exactly the pipeline I set up in the Agentic AI role.

**Q70: What is the GIL in Python and does it affect your APIs?**  
A: The Global Interpreter Lock limits true parallelism for CPU tasks in CPython. For I/O-bound FastAPI apps it's fine; for heavy CPU (model inference) I offload to worker processes or use async.

---

## 6. AWS, Docker & DevOps/CI-CD (Q71–Q82)

**Q71: Which AWS services has the role listed, and which have you used?**  
A: Role lists EC2, Lambda, DynamoDB. I have hands-on AWS ECS (from Agentic AI internship) plus Vercel/Render. I'm ready to apply that to EC2/Lambda/DynamoDB quickly.

**Q72: What is EC2 and when would you use it?**  
A: Elastic Compute Cloud — virtual servers for long-running apps (e.g., a Node/FastAPI API). Use it when you need full control vs. serverless for sporadic workloads.

**Q73: What is AWS Lambda and its trade-offs?**  
A: Serverless functions that scale to zero, billed per invocation — great for AI webhooks or image processing. Trade-offs: cold starts and 15-min timeout; not ideal for long training jobs.

**Q74: What is DynamoDB and how does it differ from MongoDB?**  
A: A managed NoSQL key-value/wide-column store with single-digit-ms latency and seamless scaling. Unlike MongoDB it requires careful partition-key design; I'd use it for high-throughput session/event data.

**Q75: How would you deploy a Next.js app on AWS?**  
A: Via Amplify, S3+CloudFront (static export), or EC2/Container behind ALB. Given my Vercel experience, I'd mirror that with CloudFront for caching and ACM for HTTPS.

**Q76: What is Docker and why use it?**  
A: Containers package app + deps for consistent environments across dev/prod. I used Docker for FastAPI microservices to eliminate "works on my machine" issues.

**Q77: What is the difference between an image and a container?**  
A: An image is an immutable blueprint; a container is a running instance of it. You build once, run many — like class vs object.

**Q78: Explain a GitHub Actions CI/CD pipeline you built.**  
A: On push/PR: checkout → setup Python/Node → lint → test → build Docker image → push to ECR → deploy to ECS. This automated my Agentic AI service releases.

**Q79: What is the difference between CI and CD?**  
A: CI integrates/tests code continuously; CD delivers (deploys) automatically after passing. I configured both so merges to main ship to staging.

**Q80: How do you manage secrets in CI/CD?**  
A: Store in GitHub Actions Secrets / AWS Secrets Manager, inject as env vars at runtime — never in code or logs. This kept API keys safe across my projects.

**Q81: What is infrastructure as code, and have you used it?**  
A: Defining infra in code (Terraform/CDK/CloudFormation) for reproducibility. While my IaC is light, I've used Docker Compose and GitHub workflows as code; I'd adopt Terraform for Yardstick's AWS.

**Q82: How do you monitor and log a deployed app?**  
A: Centralized logs (CloudWatch), metrics/alerts, and error tracking (Sentry). On ECS I used CloudWatch logs; for Next I'd add Sentry for frontend errors.

---

## 7. AI/LLM Integration & Guardrails (Q83–Q93)

**Q83: How have you integrated LLMs into full-stack apps?**  
A: Via provider SDKs/REST (OpenAI/Anthropic) behind a FastAPI/Next API route, streaming tokens over SSE/WebSocket, with Redis caching of common responses. GuardrailZ added a safety layer.

**Q84: What is GuardrailZ and what problem does it solve?**  
A: A project that adds LLM guardrails — validating/redacting prompts and responses using regex and rule engines, with Next.js + Clerk auth. It prevents prompt injection and unsafe outputs.

**Q85: How would you detect and prevent prompt injection?**  
A: Input validation, system-prompt isolation, regex/semantic checks for instruction patterns, and output filtering. GuardrailZ uses layered regex rules plus allow/deny lists.

**Q86: Explain the SSRF protection work you did in Sim Studio.**  
A: I blocked server-side request forgery by validating URLs (scheme/host), denying private/localhost ranges, and safely handling localhost HTTP requests with tests proving the fix.

**Q87: How would you build a safe localhost/URL fetcher for an AI tool?**  
A: Resolve the host, reject `file://`, `169.254.*`, `127.*`, `10.*`, `192.168.*`, and only allow `http(s)`. Combine with a timeout and size caps to avoid resource exhaustion.

**Q88: What is fine-tuning vs. RAG, and when to use each?**  
A: Fine-tuning adapts model weights to a style/task; RAG retrieves external docs at inference for grounded answers. I'd use RAG for Yardstick's analytics to keep answers current without retraining.

**Q89: How do you evaluate an AI model's output quality?**  
A: Automated metrics (BLEU/ROUGE for text, latency/cost), plus human review and guardrail pass-rate. In the BERT/VADER chatbot I tracked sentiment accuracy and response relevance.

**Q90: What is token streaming and how do you implement it?**  
A: Sending model output incrementally for UX. In Next.js:
```ts
const res = await fetch("/api/chat", { method: "POST", body });
const reader = res.body!.getReader();
```
Forward chunks via `ReadableStream` to the client.

**Q91: How do you keep AI API costs down?**  
A: Caching (Redis), smaller models for simple tasks, prompt trimming, batching, and rate limits. I cached repeated prompts in the Agentic AI services.

**Q92: What are embeddings and a vector store use case?**  
A: Embeddings map text to vectors for semantic search. Pair with a vector DB (or DynamoDB + cosine) for RAG retrieval — relevant to Yardstick's analytics/search features.

**Q93: How do you keep up with latest AI techniques/models?**  
A: Following papers/arXiv, provider changelogs, and OSS (I contributed to Sim Studio). I prototype new models quickly in FastAPI sandboxes before productizing.

---

## 8. Authentication, Security & Best Practices (Q94–Q99)

**Q94: How does JWT authentication work?**  
A: Server issues a signed token (header.payload.signature) after login; client sends it in `Authorization: Bearer`. Stateless and scalable — I implemented it in FastAPI and Next.js middleware.

**Q95: What is the difference between JWT and OAuth2?**  
A: JWT is a token format; OAuth2 is an authorization framework (delegated access via providers like Google). I've used both — OAuth via Clerk in GuardrailZ and JWT in FastAPI agents.

**Q96: How do you securely store passwords?**  
A: Never plaintext — hash with bcrypt/argon2 + salt. In Mongoose/FastAPI I use `passlib` with bcrypt and a pre-save hook.

**Q97: What are common web vulnerabilities and how do you mitigate them?**  
A: XSS (sanitize output, CSP), SQL/NoSQL injection (validation), CSRF (tokens), SSRF (URL validation — my Sim Studio fix). I apply least-privilege and input validation throughout.

**Q98: How do you write maintainable, tested code?**  
A: Type safety (TypeScript/Pydantic), small pure functions, 80% test coverage, linting, and docs. I treat tests as a safety net, evidenced by Sim Studio's SSRF tests.

**Q99: Why is documentation important and how do you maintain it?**  
A: Docs enable onboarding and reduce support load. I keep README, API docs (FastAPI auto-OpenAPI, Postman), and inline references updated with each PR as part of the dev lifecycle.

---

## 9. Behavioral & "Why Yardstick" (Q100)

**Q100: Why do you want this Full Stack internship at Yardstick, and what makes you a fit?**  
A: Yardstick's AI-integration focus matches my FastAPI/Next.js/guardrails experience (GuardrailZ, Sim Studio, BERT chatbot). I bring MERN/Next + AWS ECS + Docker/CI-CD skills and a habit of shipping clean, documented, secure code — exactly what this role needs for 6 months of WFH product work.
