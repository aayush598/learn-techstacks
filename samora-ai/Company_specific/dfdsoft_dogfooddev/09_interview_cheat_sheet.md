# DFDSOFT / DogFoodDev — Interview Cheat Sheet: Top 100 Must-Know Q&A

> Role: AI Coding & Agent Development Specialist (Remote, Full-time, US overlap 8:30 PM–5:30 AM IST)
> Candidate: Aayush Gid — quick-reference interview prep, study this last

---

## 1. Your Pitch & Behavioral (Q1–Q15)

**Q1: Tell me about yourself.**  
A: "I'm Aayush, a final-year B.Tech E&C student from Indore with deep hands-on experience in AI agent development and Python backend engineering. Over the past year, I've completed three AI-focused internships — at Krip AI building LLM-powered automation workflows with FastAPI and Docker, at Clone Futura developing REST API automations for Google Drive, and at NullClass building a BERT-based sentiment analysis chatbot. I've also built and shipped several AI projects: MigratorGen, a code migration tool using LibCST and OpenAI; ScriptVector, an AI content generator using Agno agents and Gemini; and a Marketing AI Agent integrating Gmail, Twitter, and YouTube APIs. I'm an active open-source contributor to the Agno framework with merged PRs. I'm passionate about building AI agents and automation tools, and I love the startup energy of turning rough ideas into working software fast — which is exactly what this role is about."

**Q2: Give me your 30-second elevator pitch.**  
A: "AI developer with 3 internships and multiple shipped AI agent projects. I build with Python, FastAPI, LangChain, CrewAI, and Agno. I've contributed open-source PRs to the Agno framework. I'm comfortable with ambiguity, fast iteration, and turning founder ideas into working tools."

**Q3: Why do you want to work at DFDSOFT / DogFoodDev?**  
A: "I'm drawn to the startup energy and the mission of building AI-powered tools for product builders. The role perfectly matches my strengths — I build AI agents, I ship fast, and I'm comfortable with ambiguity. The California entrepreneur culture resonates with how I work: big ideas, fast experiments, shipping today. And the technical stack aligns exactly with what I do daily — Python, LLM APIs, agent frameworks, and automation."

**Q4: Why this role over other AI engineering roles?**  
A: "Most AI engineering roles are narrowly focused on model training or MLOps. This role is unique because it's about the full lifecycle — from understanding a founder's idea, to building an agent with Claude/Codex, to supporting it after launch. I love that breadth. My experience across all three internships has been exactly this: translating business needs into working AI tools and maintaining them."

**Q5: How do you handle working US hours (8:30 PM–5:30 AM IST)?**  
A: "I'm a night owl by nature and have done late-night coding sessions for hackathons and deadlines. I'm comfortable with this schedule and see it as an advantage — fewer distractions during deep work hours, and direct overlap with the team for real-time collaboration when they need me most."

**Q6: Describe a time you dealt with ambiguity.**  
A: "At Clone Futura, the founder had a vague idea about 'automating Google Drive workflows.' There was no spec. I asked clarifying questions, defined the scope myself — which files, what triggers, what output — built a FastAPI service with SQLite storage, integrated the Google Drive API, and delivered a working automation in 4 weeks with minimal supervision."

**Q7: Describe a time you had to pivot quickly.**  
A: "During SIH 2024, our team built a security-focused encryption system. Midway through, we discovered our initial approach was too slow for real-time use. We pivoted to a hybrid encryption model within 48 hours, re-architected the core module, and still made it to the finals among 500 teams."

**Q8: What's your biggest strength?**  
A: "Speed of execution combined with technical depth. I can take a vague idea, prototype it in a day, and have a working tool within a week — but I also write tests, handle edge cases, and document it properly. My MigratorGen project went from idea to a fully tested CLI tool with 50+ pytest cases in under two weeks."

**Q9: What's your biggest weakness?**  
A: "I sometimes over-engineer early on. I've learned to catch myself — now I follow the MVP approach: build the simplest version first, get feedback, then iterate. At Krip AI, I learned to ship a working prototype before polishing, which aligned well with the startup pace."

**Q10: How do you handle criticism of your code?**  
A: "I welcome it. During my Agno open-source contributions, maintainers requested significant changes to my Milvus reranking PR. I iterated through 3 review cycles, learned their coding standards, and the PR was eventually merged. Code review is how the whole team improves."

**Q11: Tell me about a project you're most proud of.**  
A: "MigratorGen. It solves a real problem — library upgrades are manual and error-prone. I built a CLI tool that parses changelogs using an LLM, extracts structured migration steps, and generates code transforms with LibCST. The hardest part was making the LLM output reliable — I enforced strict JSON schemas, added Pydantic validation, and built 50+ test cases. It's a tool I actually use myself."

**Q12: How do you prioritize when everything feels urgent?**  
A: "I ask: what blocks other people? If a teammate is waiting on my output, that goes first. If it's a founder-facing issue, that's priority. Otherwise, I focus on the task with the highest impact-to-effort ratio. At Krip AI, I balanced CI/CD pipeline fixes with new feature development by always unblocking the team first."

**Q13: How do you stay updated on AI developments?**  
A: "I follow AI Twitter/X, read arXiv papers on agents and RAG, experiment with new APIs as they launch (I was early to try Gemini, Groq, and Agno), and contribute to open source which keeps me connected to what's actually being built in production."

**Q14: Where do you see yourself in 2 years?**  
A: "Building and leading AI agent systems at a fast-growing startup. I want to go deep on agentic AI — multi-agent orchestration, enterprise-grade agent deployments, and the tooling around agent reliability. This role is the perfect next step toward that."

**Q15: What questions do you have for us?**  
A: "1) What does the current AI agent stack look like? LangChain, CrewAI, or custom? 2) What's the typical workflow from founder idea to deployed agent? 3) How do you handle agent evaluation and monitoring? 4) What's the biggest technical challenge right now? 5) What does a typical day look like with the US overlap?"

---

## 2. AI Agents & Architecture (Q16–Q35)

**Q16: What is an AI agent?**  
A: An AI agent is an autonomous system that perceives its environment (via inputs/tools), reasons about what to do (using an LLM), and takes actions (tool calls, API requests, code execution) to achieve a goal. Unlike a simple chatbot, an agent can plan, use tools, remember context, and iterate until the task is complete.

**Q17: What are the main types of AI agents?**  
A: Reactive agents (respond to stimuli without memory), deliberative agents (plan before acting), learning agents (improve from experience), and multi-agent systems (multiple agents collaborating). In practice, most LLM-based agents are deliberative with tool use — they reason about what to do, call a tool, observe the result, and repeat.

**Q18: What is the ReAct pattern?**  
A: ReAct (Reasoning + Acting) is an agent architecture where the LLM alternates between reasoning (thinking about what to do next) and acting (calling a tool). The loop is: Thought → Action → Observation → Thought → Action → Observation → ... until the task is complete. It's the most common pattern for LLM agents because it's simple, debuggable, and effective.

**Q19: What is the difference between ReAct and plan-and-execute?**  
A: ReAct interleaves reasoning and acting in a single loop — it thinks step-by-step and takes one action at a time. Plan-and-execute first creates a complete plan (list of steps), then executes each step sequentially. ReAct is better for dynamic tasks where each step depends on the previous result. Plan-and-execute is better for complex tasks where you can map out the full approach upfront.

**Q20: What is tool calling / function calling?**  
A: Tool calling is when an LLM outputs a structured JSON request to call a predefined function instead of generating free-text. The developer defines tools with names, descriptions, and JSON Schema parameters. The LLM selects the appropriate tool and generates the correct arguments. The system executes the function and returns the result to the LLM. OpenAI calls this "function calling"; Anthropic calls it "tool use."

**Q21: How does an LLM decide which tool to call?**  
A: The LLM receives the tool definitions (name, description, parameter schema) as part of the system prompt. When processing a user request, it evaluates which tool's description best matches the task and generates a structured JSON call with the appropriate arguments. The model is trained to select tools based on semantic matching between the request and tool descriptions.

**Q22: What is a multi-agent system?**  
A: A system where multiple AI agents collaborate to solve a task. Common patterns: supervisor (one agent delegates to others), debate (agents argue and converge), and assembly line (each agent handles a step). CrewAI implements this with roles like Researcher, Writer, Reviewer. The key challenge is coordination — who does what, and how do agents share information.

**Q23: What is LangChain?**  
A: LangChain is a Python framework for building LLM-powered applications. It provides abstractions for chains (sequences of operations), agents (tool-using LLMs), tools (functions agents can call), memory (conversation history), and retrieval (RAG). It includes LangChain Core (LCEL — LangChain Expression Language for composable chains) and integrations for hundreds of LLMs, vector stores, and tools.

**Q24: What is LangGraph?**  
A: LangGraph is LangChain's framework for building stateful, multi-step agent workflows as directed graphs. Nodes are functions that do work; edges define the flow; state is passed between nodes. It supports cycles (for agent loops), human-in-the-loop, persistence, and streaming. It's more explicit and controllable than LangChain's AgentExecutor.

**Q25: What is CrewAI?**  
A: CrewAI is a multi-agent framework where agents have defined roles (e.g., Researcher, Writer, Analyst), goals, and backstories. You create a "crew" of agents and assign tasks. Agents collaborate by delegating work to each other. It's higher-level than LangGraph and great for task decomposition — e.g., one agent researches, another writes, another reviews.

**Q26: What is Agno?**  
A: Agno is a lightweight Python framework for building AI agents. Agents have tools, memory, and can work in teams. It's minimal and fast — focused on simplicity. I've contributed to it: adding Milvus reranking support, fixing JSON filter parsing, and implementing proxy configuration for the Crawl4AI toolkit.

**Q27: What is the difference between an agent and a chain?**  
A: A chain is a fixed sequence of operations (input → step 1 → step 2 → output). An agent is dynamic — it decides at each step what to do next based on the current state. Chains are deterministic; agents are adaptive. Use chains for predictable workflows; use agents when the path to the solution varies based on the input.

**Q28: What is memory in an AI agent?**  
A: Memory allows agents to retain information across interactions. Types: short-term (conversation buffer — recent messages), long-term (vector store — semantically searchable past interactions), episodic (specific past experiences), and semantic (facts and knowledge). Most agents use a combination: recent conversation in the context window + vector store for long-term retrieval.

**Q29: What is RAG?**  
A: Retrieval-Augmented Generation. Instead of relying solely on the LLM's training data, RAG retrieves relevant documents from an external knowledge base (vector store) and injects them into the prompt. Pipeline: chunk documents → embed → store in vector DB → at query time: embed query → retrieve similar chunks → assemble context → generate answer. This grounds the LLM in factual, up-to-date information.

**Q30: What is prompt injection and how do you defend against it?**  
A: Prompt injection is when a user's input tricks the LLM into ignoring system instructions or performing unauthorized actions. Defenses: 1) Separate system/user messages clearly, 2) Input sanitization (strip special instructions from user input), 3) Output validation (check if the output matches expected format), 4) Use guardrails/content filters, 5) Canary tokens in system prompts to detect overrides, 6) Never put sensitive data in prompts.

**Q31: What are guardrails for AI agents?**  
A: Guardrails are rules and validations that ensure agent behavior stays within acceptable bounds. Input guardrails: validate/filter user input (PII detection, content safety, prompt injection detection). Output guardrails: validate agent responses (factuality checks, format validation, content filtering). Runtime guardrails: limit tool access, set token budgets, enforce rate limits. My GuardrailZ project implemented 50+ such rules.

**Q32: What are evals and why do they matter?**  
A: Evals are systematic evaluations of AI agent/model performance. They measure: task completion rate, accuracy, latency, cost, and safety. Types: unit evals (single tool call correctness), integration evals (full task completion), and human evals (subjective quality). Without evals, you're flying blind — you can't improve what you can't measure. Tools: promptfoo, LangSmith, custom pytest suites.

**Q33: What is the difference between an AI agent and a copilot?**  
A: A copilot assists a human — it suggests code, answers questions, or helps with tasks, but the human drives. An agent is autonomous — it takes a goal, plans, executes, and delivers results with minimal human intervention. GitHub Copilot is a copilot; a customer service agent that handles tickets end-to-end is an agent.

**Q34: What is hallucination and how do you mitigate it?**  
A: Hallucination is when an LLM generates plausible-sounding but factually incorrect information. Mitigation: 1) RAG (ground in real documents), 2) Temperature reduction (more deterministic), 3) Structured outputs (JSON schema enforcement), 4) Chain-of-thought prompting (force reasoning), 5) Self-consistency (generate multiple answers, take majority), 6) Post-generation fact-checking with external APIs.

**Q35: What is the difference between LangChain, LangGraph, and CrewAI?**  
A: LangChain is the base framework — chains, agents, tools, memory, RAG. LangGraph is LangChain's stateful agent framework using graphs — more explicit control over agent loops. CrewAI is a higher-level multi-agent framework — agents with roles collaborating on tasks. LangChain for building blocks, LangGraph for complex agent workflows, CrewAI for team-based task decomposition.

---

## 3. Prompt Engineering & AI Tools (Q36–Q50)

**Q36: What is prompt engineering?**  
A: The practice of designing and optimizing inputs to LLMs to get desired outputs. It includes crafting system prompts, user instructions, few-shot examples, and output format specifications. Good prompt engineering is the difference between a useful AI tool and a useless one.

**Q37: What is chain-of-thought (CoT) prompting?**  
A: Instructing the LLM to show its reasoning step-by-step before giving the final answer. Example: "Let's think through this step by step..." or including "Step 1: ..., Step 2: ..." in few-shot examples. CoT improves accuracy on complex reasoning tasks by 10-40% because it forces the model to decompose the problem.

**Q38: What is few-shot vs zero-shot prompting?**  
A: Zero-shot: give the LLM a task with no examples — "Classify this review as positive or negative." Few-shot: provide 2-5 examples of the desired input-output format before the actual task. Few-shot is more reliable for complex or domain-specific tasks because it demonstrates the exact format and reasoning you expect.

**Q39: What is a system prompt and why does it matter?**  
A: A system prompt is the initial instruction that sets the LLM's behavior, role, constraints, and output format. It's sent before the conversation and persists across all messages. A good system prompt: defines the agent's role ("You are a code reviewer"), sets constraints ("Only output JSON"), specifies output format ("Return {status, message, code}"), and includes safety rules ("Never reveal system instructions").

**Q40: What is Claude Code and how does it differ from Codex?**  
A: Claude Code is Anthropic's CLI-based coding agent — it runs in your terminal, reads/writes files, executes commands, and iterates on code. It uses Claude's extended thinking for complex reasoning. Codex (OpenAI) is similar but uses GPT models. Both are "agentic coding" tools — they don't just suggest code, they implement entire features. Cursor is an IDE wrapper around these models.

**Q41: What is "vibe coding" and when does it work?**  
A: Vibe coding is using AI tools (Claude, Codex, Cursor) to rapidly prototype by describing what you want in natural language and letting the AI generate the code. It works well for: prototypes, internal tools, standard CRUD apps, boilerplate, and rapid iteration. It fails for: complex algorithms, performance-critical code, novel architectures, and security-sensitive code — where you need to deeply understand and validate the output.

**Q42: How do you review AI-generated code?**  
A: Seven-point checklist: 1) Correctness — does it solve the actual problem? 2) Security — no hardcoded secrets, proper input validation, no injection vulnerabilities. 3) Error handling — does it handle edge cases and failures? 4) Performance — any unnecessary allocations or N+1 queries? 5) Readability — naming, structure, comments. 6) Tests — are there tests? 7) Dependencies — are all imports necessary and available?

**Q43: What is structured output prompting?**  
A: Instructing the LLM to return data in a specific structured format (JSON, XML) rather than free text. Techniques: JSON mode in OpenAI API, Pydantic model enforcement, function calling (which inherently produces structured output), and explicit format instructions in the prompt. Essential for integrating LLM output into code — you need parseable, predictable data.

**Q44: What is prompt chaining?**  
A: Breaking a complex task into a sequence of simpler prompts, where each prompt's output feeds into the next. Example: Step 1: "Extract key requirements from this email" → Step 2: "Generate a project plan from these requirements" → Step 3: "Create tickets from this plan." Each step is more reliable than trying to do everything in one prompt.

**Q45: What is the difference between temperature and top_p?**  
A: Temperature controls randomness — 0 = deterministic (always pick the most likely token), 1 = creative (sample from full distribution). Top_p (nucleus sampling) controls diversity — 0.1 = only consider the top 10% most likely tokens, 1.0 = consider all tokens. For coding tasks, use low temperature (0-0.2). For creative writing, use higher (0.7-1.0). They can be used together or separately.

**Q46: What is a canary token in prompt security?**  
A: A unique, predictable string inserted into the system prompt that shouldn't appear in normal output. If the canary appears in the LLM's response, it indicates prompt injection (the system prompt was overridden). Example: "System ID: abc123" in the system prompt — if the output contains "abc123", the prompt was likely injected.

**Q47: How do you test prompts?**  
A: Create a test dataset of inputs with expected outputs. Run each input through the prompt and compare actual vs expected. Metrics: accuracy (correct classifications), format compliance (valid JSON), consistency (same input → same output across runs), and latency. Use pytest for automated prompt testing. Tools: promptfoo, LangSmith, OpenAI Evals.

**Q48: What is constitutional AI prompting?**  
A: A technique where the LLM is given a set of principles ("constitution") and asked to self-critique and revise its outputs against those principles. Example: "Review your response: Does it contain harmful content? Is it truthful? Revise if needed." This improves safety and quality without requiring a separate classifier model.

**Q49: What is meta-prompting?**  
A: Using an LLM to generate or improve prompts. Example: "Here is my current prompt for a code reviewer. Suggest improvements to make it more accurate and consistent." Useful for iteratively optimizing prompts when you're not sure what phrasing works best.

**Q50: How do you handle LLM output that doesn't match expected format?**  
A: 1) Retry with explicit format instructions ("You MUST output valid JSON"). 2) Use structured output APIs (OpenAI's response_format, Anthropic's tool_use). 3) Add a Pydantic validator and retry on validation failure. 4) Use a fallback — extract data from free text with regex. 5) Log failures and improve the prompt based on common failure patterns.

---

## 4. Python & Backend (Q51–Q65)

**Q51: What is the difference between a list and a tuple in Python?**  
A: Lists are mutable (can be changed after creation) and use `[]`. Tuples are immutable and use `()`. Tuples are slightly faster, hashable (can be dict keys), and signal "fixed collection." Use tuples for config/records, lists for dynamic collections.

**Q52: What are decorators in Python?**  
A: Functions that wrap other functions to add behavior without modifying the original. Example: `@timer` that prints execution time, `@auth_required` that checks JWT tokens. Decorators are syntactic sugar for `func = decorator(func)`. They're used extensively in FastAPI (`@app.get`, `@app.post`).

**Q53: What is async/await in Python?**  
A: Async/await enables concurrent I/O operations without threads. `async def` defines a coroutine; `await` pauses execution until a result is ready, allowing other tasks to run. Essential for FastAPI (handles thousands of concurrent requests) and API calls to external services. `asyncio.gather()` runs multiple async tasks concurrently.

**Q54: What is FastAPI and why is it popular?**  
A: FastAPI is a modern Python web framework built on Starlette and Pydantic. It's popular because: automatic API docs (OpenAPI/Swagger), type-safe request/response validation via Pydantic, native async support, dependency injection, and performance comparable to Node.js/Go. It's the standard for AI/ML backends because of its speed and developer experience.

**Q55: What is Pydantic and why does FastAPI use it?**  
A: Pydantic is a data validation library using Python type hints. It validates data at runtime, serializes/deserializes JSON, and generates JSON Schema. FastAPI uses Pydantic models for request bodies, query parameters, and response models — giving you automatic validation, serialization, and documentation for free.

**Q56: What is the difference between synchronous and asynchronous FastAPI?**  
A: Sync FastAPI (`def endpoint()`) runs in a thread pool — fine for CPU-bound or blocking I/O tasks. Async FastAPI (`async def endpoint()`) runs on the event loop — essential for I/O-bound tasks (API calls, database queries, file operations) because it allows handling thousands of concurrent requests without blocking.

**Q57: What is dependency injection in FastAPI?**  
A: A pattern where FastAPI automatically provides dependencies (database connections, auth, config) to your endpoint functions. Example: `def get_db(): yield SessionLocal()` then `def read_users(db: Session = Depends(get_db))`. FastAPI manages the lifecycle — creating, injecting, and cleaning up dependencies.

**Q58: How do you handle errors in FastAPI?**  
A: Raise HTTP exceptions: `raise HTTPException(status_code=404, detail="Not found")`. For custom errors, create exception handlers: `@app.exception_handler(CustomError)`. Use try/except in endpoints. FastAPI automatically returns JSON error responses with proper status codes. For validation errors, Pydantic raises `422 Unprocessable Entity` automatically.

**Q59: What is pytest and how do you use it?**  
A: pytest is Python's most popular testing framework. Use: `assert result == expected`, fixtures (`@pytest.fixture`), parametrize (`@pytest.mark.parametrize`), markers (`@pytest.mark.slow`), and conftest.py for shared fixtures. Example: `def test_add(): assert add(1, 2) == 3`. It's used for unit tests, integration tests, and AI model evaluation.

**Q60: What is the difference between unit, integration, and end-to-end tests?**  
A: Unit tests: test individual functions in isolation (fast, many). Integration tests: test how components work together (API + database). End-to-end tests: test the full system from user input to final output (slowest, fewest). For AI agents: unit test tool functions, integration test agent loops, E2E test full task completion.

**Q61: What is a generator in Python?**  
A: A function that uses `yield` instead of `return` — it produces values lazily, one at a time. Generators are memory-efficient for large datasets because they don't load everything into memory. Example: `def read_large_file(): for line in file: yield line`. Used in streaming responses and data processing pipelines.

**Q62: What are Python context managers?**  
A: Objects that define `__enter__` and `__exit__` methods for resource management (file handles, database connections, locks). Used with `with` statement: `with open('file.txt') as f: ...`. Ensures cleanup happens even if exceptions occur. Create custom ones with `@contextmanager` decorator.

**Q63: What is the GIL and does it affect FastAPI?**  
A: The Global Interpreter Lock (GIL) allows only one thread to execute Python bytecode at a time. It limits CPU-bound parallelism in threads but NOT I/O-bound concurrency. FastAPI is I/O-bound (waiting for database, API calls), so the GIL doesn't significantly affect it. For CPU-bound work, use `multiprocessing` or `asyncio.to_thread()`.

**Q64: How do you structure a Python project?**  
A: `src/` layout with package, `tests/` directory, `pyproject.toml` for config, `README.md`, `.env` for secrets, `.gitignore`. Inside the package: separate by feature or layer (routes/, models/, services/, utils/). Use `__init__.py` for exports. Follow PEP 8, use type hints, run `ruff` for linting.

**Q65: What is the difference between `*args` and `**kwargs`?**  
A: `*args` captures positional arguments as a tuple. `**kwargs` captures keyword arguments as a dict. Example: `def func(*args, **kwargs): print(args, kwargs)`. `func(1, 2, a=3)` → `(1, 2)` and `{'a': 3}`. Used for flexible function signatures and decorators.

---

## 5. APIs, Webhooks & Integrations (Q66–Q80)

**Q66: What is the difference between polling and webhooks?**  
A: Polling: client repeatedly asks the server "is there new data?" (wasteful, high latency). Webhooks: server pushes data to a client URL when an event occurs (efficient, real-time). Webhooks are event-driven — you register a URL, and the server POSTs data to it when something happens. Essential for GitHub, Stripe, Slack integrations.

**Q67: How do you secure a webhook endpoint?**  
A: 1) Verify HMAC signature — the sender signs the payload with a shared secret; you verify the signature matches. 2) Use HTTPS only. 3) Validate the source IP (if the service provides a whitelist). 4) Check timestamp to reject replay attacks. 5) Return 200 quickly and process asynchronously (to avoid timeouts). 6) Implement idempotency (same event delivered twice shouldn't cause duplicate side effects).

**Q68: What is OAuth2 and how does it work?**  
A: OAuth2 is an authorization framework that allows third-party apps to access user data without sharing passwords. Flow: 1) App redirects user to provider (Google, GitHub), 2) User authorizes, 3) Provider returns an authorization code, 4) App exchanges code for access token, 5) App uses token to access APIs. Types: authorization code (most secure), client credentials (server-to-server), PKCE (public clients).

**Q69: What is the difference between authentication and authorization?**  
A: Authentication: "Who are you?" (verify identity — login, JWT, API key). Authorization: "What can you do?" (check permissions — roles, scopes, ACLs). Authentication comes first; authorization checks what the authenticated user is allowed to access. JWTs can encode both: identity (sub) and permissions (roles, scopes).

**Q70: What is a REST API and what makes it RESTful?**  
A: REST (Representational State Transfer) is an API architecture using HTTP methods on resources (URLs). RESTful properties: stateless (no server-side session), resource-based (each URL is a resource), uses HTTP verbs (GET/POST/PUT/DELETE), returns standard status codes (200, 201, 404, 500), and supports HATEOAS (hypermedia links).

**Q71: What are common HTTP status codes?**  
A: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized (not authenticated), 403 Forbidden (not authorized), 404 Not Found, 409 Conflict, 422 Unprocessable Entity (validation error), 429 Too Many Requests (rate limit), 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable.

**Q72: What is rate limiting and how do you implement it?**  
A: Limiting how many requests a client can make in a time window. Algorithms: fixed window (100 req/min), sliding window (rolling 60s), token bucket (burst + sustained). Implementation: FastAPI middleware with Redis backend (count requests per API key). Return 429 with `Retry-After` header when exceeded. Protects against abuse and ensures fair usage.

**Q73: What is a webhook receiver endpoint?**  
A: A server endpoint that accepts incoming webhook POST requests from external services. Example: `@app.post("/webhooks/stripe")` receives payment events. Must: verify signature, parse JSON payload, return 200 quickly, queue for async processing. Don't do heavy computation in the handler — enqueue and process in background.

**Q74: What is idempotency and why does it matter for webhooks?**  
A: Idempotency means processing the same request multiple times produces the same result. Webhooks can be delivered multiple times (retries, network issues). Without idempotency, duplicate processing causes bugs (double charges, duplicate records). Implement with idempotency keys (store processed event IDs) or database upserts instead of inserts.

**Q75: What is exponential backoff?**  
A: A retry strategy where wait time doubles after each failure: 1s, 2s, 4s, 8s, 16s... Prevents overwhelming a failing service (thundering herd). Add jitter (random offset) to prevent synchronized retries. Use with circuit breaker: after N failures, stop retrying and fail fast. Python: `time.sleep(min(base * 2**attempt + random(), max_delay))`.

**Q76: What is the difference between a circuit breaker and rate limiting?**  
A: Rate limiting: limits requests from YOUR client to a service (outbound). Circuit breaker: stops calling a service that's failing (protects you from cascade failures). Rate limiting protects the service; circuit breaker protects your system. Both are essential for reliable integrations.

**Q77: How do you handle API versioning?**  
A: URL path versioning (`/api/v1/users`) — most common, explicit. Header versioning (`Accept: application/vnd.api.v1+json`) — cleaner URLs. Query param (`/api/users?version=1`) — easy but messy. For webhooks, include version in payload. Always maintain backward compatibility for at least one version.

**Q78: What is a dead letter queue (DLQ)?**  
A: A queue where messages go when they can't be processed after maximum retries. Instead of losing failed messages or blocking the queue, they're stored for inspection and manual reprocessing. Essential for webhooks, event-driven systems, and any async processing where failures need investigation.

**Q79: How would you integrate with the Gmail API?**  
A: 1) Set up Google Cloud project and enable Gmail API. 2) Create OAuth2 credentials (or service account). 3) Implement OAuth flow to get access token. 4) Use token to call Gmail API endpoints: `GET /messages` (list), `GET /messages/{id}` (read), `POST /messages/send` (send). 5) Handle token refresh. I did this in my Marketing AI Agent project for email automation.

**Q80: What is a webhook vs an event-driven architecture?**  
A: Webhooks are a specific implementation of event-driven architecture — one system notifying another via HTTP POST. Event-driven architecture is broader: includes message queues (RabbitMQ, Kafka), pub/sub patterns, and event sourcing. Webhooks are synchronous (HTTP); event queues are asynchronous. For simple integrations, webhooks; for complex systems, message queues.

---

## 6. Databases & Vector Stores (Q81–Q90)

**Q81: What is the difference between SQL and NoSQL?**  
A: SQL (PostgreSQL, MySQL): structured schemas, tables with rows/columns, JOINs, ACID transactions, vertical scaling. NoSQL (MongoDB, Redis): flexible schemas, documents/key-values, eventual consistency, horizontal scaling. Use SQL for relational data with complex queries; NoSQL for flexible schemas, high write throughput, or horizontal scaling.

**Q82: What is an embedding and why does it matter for AI?**  
A: An embedding is a dense vector representation of text (or images) that captures semantic meaning. Similar texts have similar vectors. Example: "dog" and "puppy" are close in embedding space. Used for: semantic search, RAG (retrieve relevant documents), deduplication, and clustering. Models: OpenAI text-embedding-3-small (1536-dim), sentence-transformers, BGE.

**Q83: What is a vector database?**  
A: A database optimized for storing and querying high-dimensional vectors. It supports approximate nearest neighbor (ANN) search — finding the most similar vectors to a query vector. Examples: Milvus, FAISS, Pinecone, Chroma, Weaviate. Essential for RAG — you store document embeddings and retrieve the most relevant chunks for a query.

**Q84: What is the difference between FAISS and Milvus?**  
A: FAISS (Facebook): library, runs locally/in-process, great for prototyping, supports GPU, no server needed. Milvus: distributed database, production-grade, supports metadata filtering, multi-vector search, horizontal scaling, and reranking. FAISS for quick experiments; Milvus for production deployments. I've contributed to Agno's Milvus reranking integration.

**Q85: What is cosine similarity?**  
A: A metric measuring the angle between two vectors (0 = identical direction, 90° = unrelated, 180° = opposite). Formula: cos(θ) = (A·B) / (||A|| × ||B||). Used as the primary similarity metric for embedding search — higher cosine similarity means more semantically similar. Range: -1 to 1 (usually 0 to 1 for normalized embeddings).

**Q86: What is chunking in RAG?**  
A: Splitting documents into smaller pieces before embedding. Why: LLMs have context limits, and embedding short texts is more accurate than embedding entire documents. Strategies: fixed-size (512 tokens), semantic (split at paragraph/topic boundaries), recursive (split by paragraph → sentence → word), and overlap (include surrounding context in each chunk).

**Q87: What is reranking in RAG?**  
A: After initial vector search returns top-k results, reranking re-orders them using a more accurate (but slower) model. Initial search: fast but approximate (cosine similarity). Reranking: slower but more accurate (cross-encoder that reads query + document together). Example: Cohere Rerank, cross-encoder/ms-marco. Improves retrieval quality significantly.

**Q88: What is hybrid search?**  
A: Combining dense vector search (semantic similarity) with sparse search (keyword/BM25 matching). Vector search finds semantically similar documents even if words don't match. Sparse search finds exact keyword matches. Hybrid search combines both scores, giving you the best of both worlds. Essential for production RAG — some queries need exact matches.

**Q89: What is PostgreSQL and when should you use it?**  
A: PostgreSQL is a powerful open-source relational database. Use for: structured data with relationships, complex queries (JOINs, window functions, CTEs), ACID transactions, JSONB for semi-structured data, full-text search (tsvector), and geospatial queries (PostGIS). It's the standard for production backends — reliable, extensible, and performant.

**Q90: What is SQLite and when should you use it?**  
A: SQLite is a serverless, file-based relational database. Use for: embedded applications, prototyping, testing, mobile apps, and single-user tools. It's a single file, zero-config, and fast for read-heavy workloads. Don't use for: high-concurrency write-heavy production systems. I used it in Clone Futura and ScriptVector for lightweight, portable storage.

---

## 7. DevOps, Docker & Deployment (Q91–Q95)

**Q91: What is Docker and why do you use it?**  
A: Docker packages applications into containers — lightweight, portable environments with all dependencies. Benefits: "works on my machine" eliminated, consistent dev/prod environments, easy scaling, isolation between services. Dockerfile defines the container; docker-compose defines multi-service stacks. I containerized FastAPI services at Krip AI for deployment on AWS ECS.

**Q92: What is CI/CD and how do you set it up?**  
A: Continuous Integration: automatically run tests/linting on every push. Continuous Delivery: automatically build and stage for deployment. Continuous Deployment: automatically deploy to production. Setup: GitHub Actions workflow → trigger on push/PR → checkout code → install deps → run tests → build Docker image → push to registry → deploy. I built CI/CD pipelines at Krip AI using GitHub Actions.

**Q93: What is the difference between a container and a virtual machine?**  
A: Containers share the host OS kernel (lightweight, fast startup, smaller). VMs have their own OS (full isolation, heavier, slower startup). Containers are ideal for microservices and CI/CD. VMs are better for running different OS or strong isolation requirements. Docker containers start in seconds; VMs take minutes.

**Q94: What is Linux and why is it essential for DevOps?**  
A: Linux is the operating system running most servers, containers, and cloud infrastructure. Essential commands: `ls`, `cd`, `grep`, `find`, `curl`, `ssh`, `docker`, `git`, `ps`, `top`, `chmod`, `chown`. Understanding Linux basics (file system, permissions, processes, networking) is critical for deploying and debugging applications in production.

**Q95: How do you debug a production issue?**  
A: 1) Check logs (application logs, system logs, Docker logs). 2) Check metrics (CPU, memory, request latency, error rate). 3) Reproduce locally if possible. 4) Add targeted logging to narrow down the issue. 5) Check recent deployments (did a change cause this?). 6) Check dependencies (database, external APIs, network). 7) Fix, test, deploy, monitor. Use Sentry for error tracking, Grafana for metrics.

---

## 8. Open Source & Technical Depth (Q96–Q100)

**Q96: Tell me about your Agno framework contributions.**  
A: "I've contributed three merged PRs to the Agno framework. First, I added Milvus reranking support — this allows Agno agents to re-order vector search results using a cross-encoder model for better retrieval relevance. Second, I fixed a JSON filter parsing bug where complex nested filters weren't handled correctly. Third, I implemented proxy configuration for the Crawl4AI toolkit, enabling agents to scrape web content through proxy servers. All three PRs required understanding Agno's agent architecture, writing tests, and following the maintainers' code review process."

**Q97: How does Milvus reranking work in your Agno contribution?**  
A: "Initial vector search in Milvus uses approximate nearest neighbor (ANN) — fast but not perfectly accurate. Reranking takes the top-k results and re-scores them using a cross-encoder model that reads the query and document together. This is slower but more accurate because it captures fine-grained relevance that cosine similarity misses. My PR integrated Cohere rerank and cross-encoder models into Agno's Milvus wrapper, with configurable top-k reranking."

**Q98: Explain your MigratorGen project technically.**  
A: "MigratorGen automates library upgrades. It has three components: 1) A changelog parser that ingests JSON or Markdown release notes and extracts breaking changes, deprecations, and migration steps. 2) An LLM-based extractor using OpenAI that converts unstructured Markdown into structured JSON using Pydantic models. 3) A code transform engine using LibCST (a Python AST library) that applies the migration steps to actual source code — renaming functions, updating imports, replacing deprecated APIs. The CLI takes a library name, current version, and target version, then generates a migration package. Tested with 50+ pytest cases."

**Q99: How do you handle API authentication in your projects?**  
A: "I've implemented multiple auth patterns: JWT-based auth in FastAPI (token generation, validation middleware, refresh tokens), API key authentication for internal services, and OAuth2 flows for third-party integrations (Google Drive API at Clone Futura, Gmail/Twitter/YouTube APIs in Marketing AI Agent). I understand the tradeoffs: JWT for stateless auth, API keys for simple service-to-service, OAuth2 for user-delegated access."

**Q100: What makes you the right fit for this role?**  
A: "Three things: 1) I build AI agents — not just theoretically, but shipped products using LangChain, CrewAI, Agno, and OpenAI/Gemini APIs. I understand the full agent lifecycle from prompt design to deployment. 2) I ship fast — three internships, three projects, and open-source contributions in under a year. I thrive in ambiguous, fast-paced environments. 3) I'm reliable — I write tests, handle edge cases, document my work, and provide ongoing support. I don't just build and disappear. That's exactly what you need: someone who brings the vibe coding energy but also the reliability to keep software useful, stable, and improving."
