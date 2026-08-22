# A2A (Agent-to-Agent Protocol) — 100 Interview Q&A

---

## Q1: What is the A2A (Agent-to-Agent) protocol?
**A:** A2A is an open protocol developed by Google that enables AI agents built on different frameworks or by different vendors to communicate, collaborate, and delegate tasks to each other over standard web protocols (HTTP/SSE). It acts as a universal translation layer so heterogeneous agents can interoperate.

## Q2: Who created the A2A protocol and why?
**A:** Google introduced A2A in April 2025. The motivation was that enterprises use agents from multiple vendors (Google, Microsoft, Salesforce, custom-built), and these agents cannot talk to each other natively. A2A provides a vendor-neutral standard for cross-agent communication.

## Q3: What problem does A2A solve?
**A:** It solves agent fragmentation — the problem where agents built with different frameworks (LangChain, CrewAI, AutoGen, custom) cannot discover or delegate work to each other. Before A2A, integrating multi-vendor agent systems required custom point-to-point integrations.

## Q4: How does A2A differ from MCP (Model Context Protocol)?
**A:** MCP connects agents to tools and data sources (agent ↔ tool). A2A connects agents to other agents (agent ↔ agent). MCP is about capability exposure; A2A is about task delegation and collaboration between peer agents.

## Q5: What are the core components of the A2A architecture?
**A:** Two roles: the Client Agent (initiates a task, needs something done) and the Remote Agent (receives the task, has capabilities to complete it). Communication happens via HTTP with Server-Sent Events (SSE) for streaming.

## Q6: What is an Agent Card in A2A?
**A:** An Agent Card is a JSON document (at `/.well-known/agent.json`) that an agent publishes to describe its identity, capabilities, supported input/output types, authentication requirements, and endpoint URL. It's like a business card that other agents can discover.

## Q7: What information does an Agent Card contain?
**A:** Agent name, version, description, URL endpoint, authentication method (API key, OAuth2, etc.), supported input MIME types, supported output MIME types, a list of skills/capabilities the agent offers, and optional pricing or rate-limit information.

## Q8: How do agents discover each other in A2A?
**A:** A client agent fetches the Agent Card from a known URL (e.g., `https://agent.example.com/.well-known/agent.json`). This is the discovery mechanism — the card tells the client what the remote agent can do and how to call it.

## Q9: What is a task in A2A?
**A:** A task is the fundamental unit of work in A2A. The client sends a task request with a message (text, files, structured data), and the remote agent processes it, updating the task through states (submitted → working → completed/failed/canceled).

## Q10: What are the task states in A2A?
**A:** `submitted` (task received), `working` (agent is processing), `input-required` (agent needs more info from client), `completed` (task done), `failed` (task failed), `canceled` (task was canceled by client).

## Q11: How does an agent request more information in A2A?
**A:** The remote agent sets the task state to `input-required` and includes a message specifying what additional information it needs. The client then sends a follow-up message to provide the missing input. This supports multi-turn conversations within a single task.

## Q12: What streaming options does A2A support?
**A:** A2A supports Server-Sent Events (SSE) for real-time task updates. The client can subscribe to task status changes, receive intermediate results as they're produced, and track progress without polling.

## Q13: Can A2A agents send files to each other?
**A:** Yes. A2A supports multi-part messages that can include text, files (inline base65 or via URI reference), and structured JSON data. This allows agents to exchange documents, images, code, or any binary data.

## Q14: What is the push notification feature in A2A?
**A:** A client can register a webhook URL with the remote agent. When the task completes or has an update, the remote agent pushes the result to the client's webhook. This is useful for long-running tasks where polling is impractical.

## Q15: How does authentication work in A2A?
**A:** Authentication is defined in the Agent Card. Common methods include API keys (passed in headers), OAuth2 flows (client credentials or authorization code), and mTLS. The protocol itself is auth-agnostic — the Agent Card specifies the scheme, and the client follows it.

## Q16: What is the difference between A2A and function calling?
**A:** Function calling is intra-agent — an LLM within a single agent decides to call a tool. A2A is inter-agent — one autonomous agent delegates a task to another autonomous agent that has its own LLM, tools, and reasoning loop.

## Q17: Can A2A agents be built with any framework?
**A:** Yes. The protocol is framework-agnostic. You can build A2A-compatible agents with LangChain, CrewAI, AutoGen, Agno, Google ADK, or even raw Python. As long as the agent publishes an Agent Card and implements the task endpoints, it's A2A-compliant.

## Q18: What transport protocol does A2A use?
**A:** HTTP/HTTPS with JSON-RPC 2.0 as the message format. SSE is used for streaming task updates. This ensures wide compatibility — any system that can make HTTP requests can participate.

## Q19: What is the role of JSON-RPC 2.0 in A2A?
**A:** JSON-RPC 2.0 provides the standard request/response format for task creation, message sending, and task status queries. It defines methods like `tasks/send`, `tasks/get`, `tasks/cancel`, and `tasks/pushNotification/set`.

## Q20: How does A2A handle long-running tasks?
**A:** Tasks can be asynchronous. The remote agent acknowledges receipt (state: `submitted`), processes in the background (state: `working`), and notifies the client via SSE or push notification when complete. The client can check task status at any time via `tasks/get`.

## Q21: Can multiple agents collaborate on a single task?
**A:** Yes. A client agent can delegate subtasks to multiple remote agents in parallel. Each remote agent works independently, and the client agent aggregates results. This enables multi-agent workflows where different agents handle different specialties.

## Q22: What is the difference between A2A and a message queue (RabbitMQ, Kafka)?
**A:** Message queues are infrastructure-level pub/sub systems. A2A is an application-level protocol specifically for AI agent collaboration. A2A includes agent discovery (Agent Cards), structured task management, and multi-turn conversations — none of which message queues provide natively.

## Q23: How does A2A handle errors?
**A:** If a remote agent fails, it sets the task state to `failed` and includes an error message describing what went wrong. The client agent can then retry, delegate to a different agent, or handle the failure gracefully.

## Q24: What is a skill in A2A?
**A:** A skill is a specific capability an agent advertises in its Agent Card (e.g., "summarize documents," "generate images," "translate languages"). Skills help client agents decide which remote agent to delegate a task to.

## Q25: Can A2A agents negotiate task parameters?
**A:** Yes, through multi-turn conversation. The remote agent can set state to `input-required` and ask for clarification, and the client can refine its request. This enables iterative task refinement.

## Q26: How does A2A relate to Google's Agent Development Kit (ADK)?
**A:** Google ADK is a framework for building agents. It has built-in support for publishing Agent Cards and implementing A2A endpoints, making it easy to build A2A-compatible agents. However, A2A works with any framework.

## Q27: What are the use cases for A2A?
**A:** Multi-vendor agent orchestration, enterprise agent interoperability (e.g., Salesforce agent + internal agent), specialized agent delegation (research agent delegates to calculation agent), and building agent marketplaces where agents discover and hire each other.

## Q28: Can A2A agents handle multimodal content?
**A:** Yes. A2A messages support multiple MIME types including text/plain, text/markdown, application/json, image/png, application/pdf, and custom types. Agents can exchange images, documents, code, and structured data.

## Q29: What is the `tasks/resubscribe` endpoint in A2A?
**A:** If a client loses its SSE connection, it can call `tasks/resubscribe` to reconnect and receive any events it missed. This ensures reliable streaming even over unstable networks.

## Q30: How do you implement an A2A server in Python?
**A:** Use the `a2a-sdk` Python package (or the reference implementation from Google). Define your agent's logic, create an Agent Card, and expose the JSON-RPC endpoints (`/` or `/a2a`). The SDK handles protocol details — you focus on agent logic.

## Q31: Can A2A work over local networks (intranet)?
**A:** Yes. A2A uses standard HTTP, so it works over any network — public internet, private VPC, or localhost. For local development, you can run agents on different ports on the same machine.

## Q32: What is the difference between A2A and REST APIs?
**A:** REST APIs are static — a developer defines endpoints, and clients call them. A2A is dynamic — agents discover capabilities at runtime via Agent Cards, and the task workflow (submit → work → complete with possible multi-turn) is standardized. A2A adds intelligence and autonomy on top of HTTP.

## Q33: How does A2A handle concurrency?
**A:** Multiple clients can send tasks to the same remote agent simultaneously. The remote agent handles each task independently. A2A doesn't define a concurrency model — that's implementation-dependent.

## Q34: What is the `tasks/cancel` method?
**A:** A client can cancel a submitted or working task. The remote agent stops processing and sets the state to `canceled`. This is useful for long-running tasks the client no longer needs.

## Q35: Can an A2A agent refuse a task?
**A:** Yes. The remote agent can immediately set the task to `failed` with a reason (e.g., "outside my skill set," "authentication required," "rate limit exceeded"). The client can then try a different agent.

## Q36: What happens if an A2A remote agent goes offline?
**A:** The client's request will fail with a connection error. The client should implement retries with backoff, fallback to alternative agents, or queue the task for later. The A2A protocol doesn't handle agent availability — that's the client's responsibility.

## Q37: How do you test A2A agents?
**A:** Unit test your agent's core logic independently. Integration test the A2A endpoints by sending mock task requests and verifying responses. Use the A2A SDK's test utilities. End-to-end tests involve running two agents and verifying task delegation works.

## Q38: What is the relationship between A2A and OpenAPI?
**A:** Agent Cards are separate from OpenAPI specs, but they can complement each other. OpenAPI describes HTTP endpoints; Agent Cards describe agent capabilities, skills, and communication protocols. A2A Agent Cards are simpler and agent-specific.

## Q39: Can A2A agents have memory or state?
**A:** The protocol itself is stateless (HTTP). However, agents can maintain internal state (conversation history, task context, learned preferences) across tasks. Task state is tracked by the remote agent and accessible via `tasks/get`.

## Q40: How does A2A handle security?
**A:** A2A delegates security to the transport layer (HTTPS) and authentication (defined in Agent Cards). It supports standard web security practices: OAuth2, API keys, mTLS. The protocol doesn't add its own encryption — it relies on TLS.

## Q41: What are the limitations of A2A?
**A:** Still early stage (2025). Limited tooling and SDKs. No standard for agent trust/reputation. No built-in payment or SLA mechanisms. Discovery is manual (you need to know the Agent Card URL). Performance overhead from HTTP/JSON serialization vs. direct in-process calls.

## Q42: How does A2A compare to Microsoft's AutoGen?
**A:** AutoGen is a framework for building multi-agent systems within a single application. A2A is a protocol for cross-application, cross-vendor agent communication. AutoGen agents run in the same process; A2A agents can be anywhere on the network. They can complement each other — an AutoGen multi-agent system could expose itself as an A2A endpoint.

## Q43: Can A2A be used for agent marketplaces?
**A:** Yes, conceptually. Agents publish Agent Cards, and a marketplace could index them. Clients could search for agents by skill, compare capabilities, and delegate tasks. The Agent Card is the foundation for such a marketplace.

## Q44: What MIME types does A2A support natively?
**A:** `text/plain`, `text/markdown`, `application/json`, `image/png`, `image/jpeg`, `application/pdf`, `audio/wav`, `video/mp4`, and any custom MIME type. The Agent Card declares which types the agent accepts.

## Q45: How do you version A2A APIs?
**A:** Include a version field in the Agent Card. The protocol supports backward-compatible evolution — new fields can be added without breaking existing clients. Breaking changes require a new Agent Card URL or version identifier.

## Q46: What is the `tasks/get` method?
**A:** A client calls `tasks/get` with a task ID to retrieve the current state of a task, including its status, latest message, and any artifacts (results). Useful for polling long-running tasks or reconnecting after a disconnect.

## Q47: Can A2A agents send intermediate progress updates?
**A:** Yes. While working, the remote agent can send progress updates via SSE, including percentage complete, intermediate results, or status messages. The client receives these in real-time without polling.

## Q48: What is an artifact in A2A?
**A:** Artifacts are the outputs produced by a remote agent during a task — generated files, code, analysis results, images, etc. They're part of the task response and can be retrieved by the client.

## Q49: How do you handle agent trust in A2A?
**A:** A2A itself doesn't define trust mechanisms. Trust is handled at the application level: API keys, OAuth scopes, rate limiting, reputation systems, or manual allowlists. The Agent Card can declare authentication requirements, but trust decisions are up to the client.

## Q50: Can A2A agents delegate tasks to other A2A agents (chained delegation)?
**A:** Yes. Agent A delegates to Agent B, which in turn delegates to Agent C. This creates an agent chain. The challenge is tracking state across the chain and handling failures at any point. Implementation must handle timeouts and error propagation.

## Q51: What is the difference between A2A and webhooks?
**A:** Webhooks are simple HTTP callbacks triggered by events. A2A is a structured protocol with agent discovery, task lifecycle management, multi-turn conversations, and streaming. Webhooks are a building block; A2A is a complete agent collaboration framework.

## Q52: How does A2A handle different LLMs behind agents?
**A:** A2A is LLM-agnostic. Agent A might use GPT-4, Agent B might use Claude, Agent C might use Gemini. The protocol doesn't care what LLM powers the agent — it only defines how agents communicate. This is a key feature for vendor neutrality.

## Q53: Can you build A2A agents without any SDK?
**A:** Yes. A2A is just HTTP + JSON. You can implement it from scratch: serve an Agent Card at `/.well-known/agent.json`, accept JSON-RPC requests at a POST endpoint, manage task state internally, and return JSON responses. SDKs just make this easier.

## Q54: What is the `tasks/pushNotification/set` method?
**A:** Registers a webhook URL with the remote agent for a specific task. When the task completes or has an update, the agent POSTs the result to the registered URL. This enables asynchronous, event-driven task completion.

## Q55: How does A2A handle task timeouts?
**A:** A2A doesn't define a standard timeout mechanism. Timeout handling is implementation-dependent. The client can set its own timeout, cancel the task if it takes too long, or the remote agent can fail the task if it exceeds internal limits.

## Q56: Can A2A agents share context or conversation history?
**A:** Through the task itself. A client can include conversation history in messages, and the remote agent can reference previous exchanges within the same task. There's no shared memory between agents — context is passed explicitly.

## Q57: What is the difference between A2A and LLM function calling?
**A:** Function calling: LLM within one agent decides to call a tool (intra-agent). A2A: one agent delegates a task to another agent over the network (inter-agent). Function calling is synchronous and local; A2A is asynchronous and distributed.

## Q58: How does A2A support enterprise compliance?
**A:** Through standard web security (TLS, OAuth2, API keys) and the ability to run on private networks. Enterprise features like audit logging, access control, and data residency are implementation-dependent, not protocol-defined.

## Q59: Can A2A agents communicate with non-AI systems?
**A:** A2A is designed for agent-to-agent communication. To integrate with non-AI systems, you'd build a wrapper agent that exposes the legacy system's capabilities via A2A. The agent acts as a bridge between the A2A world and the legacy API.

## Q60: What is the future roadmap for A2A?
**A:** As of 2025: broader adoption, more SDKs, agent marketplace standards, trust/reputation protocols, payment integration, and enterprise features. Google is pushing it as an open standard with community governance.

## Q61: How do you debug A2A communication issues?
**A:** Check HTTP logs for request/response payloads. Verify the Agent Card is accessible and correctly formatted. Use `tasks/get` to inspect task state. Enable verbose logging in the A2A SDK. Test with curl/Postman before using the SDK.

## Q62: Can A2A handle batch task submissions?
**A:** Yes. A client can send multiple task requests to a remote agent. The agent processes them independently. The protocol doesn't define batch semantics — it's up to the implementation to handle multiple concurrent tasks efficiently.

## Q63: How does A2A relate to Kubernetes and microservices?
**A:** A2A agents can be deployed as microservices (e.g., in Kubernetes pods). Each agent is an independent service with its own endpoint. Kubernetes handles scaling, networking, and service discovery; A2A handles agent-level communication.

## Q64: What programming languages support A2A?
**A:** Python (primary, with the official SDK), TypeScript/JavaScript, Go, Java, and any language that can serve HTTP endpoints and handle JSON. The protocol is language-agnostic.

## Q65: Can A2A agents have different security clearances?
**A:** Yes, but it's implementation-dependent. Different Agent Cards can declare different authentication requirements. A classified-data agent might require mTLS + API key, while a public-info agent might accept anonymous requests.

## Q66: How do you implement retry logic in A2A?
**A:** The client catches connection errors or task failures and retries with exponential backoff. Use `tasks/get` to check if a previous attempt actually succeeded before retrying (idempotency). A2A doesn't define retry semantics — it's the client's responsibility.

## Q67: What is the relationship between A2A and GraphQL?
**A:** They solve different problems. GraphQL is a query language for APIs (client specifies what data it needs). A2A is an agent collaboration protocol. You could use GraphQL for the underlying API layer, but A2A's JSON-RPC format is the standard.

## Q68: Can A2A agents have billing or metering?
**A:** The Agent Card can include pricing information (e.g., cost per task), but A2A doesn't define a payment protocol. Billing would need to be handled externally (e.g., API key usage tracking, OAuth scopes with quotas).

## Q69: How does A2A handle agent versioning?
**A:** Agent Cards include a version field. Different versions can coexist at different URLs. Clients check the version to ensure compatibility. Breaking changes should result in a new URL or major version bump.

## Q70: Can A2A work in air-gapped environments?
**A:** Yes, as long as agents can reach each other over the network (even an isolated one). A2A uses standard HTTP, so it works on any IP network without internet access.

## Q71: What is the difference between A2A and a service mesh (Istio, Linkerd)?
**A:** Service meshes handle infrastructure concerns: load balancing, retries, mTLS between microservices. A2A handles application-level agent semantics: discovery, task delegation, multi-turn conversations. A2A can run on top of a service mesh.

## Q72: Can A2A agents publish events (pub/sub)?
**A:** A2A is primarily request-response (task delegation). For pub/sub patterns, you'd combine A2A with a messaging system (Kafka, Redis Streams). The push notification feature provides some event-like behavior for task completions.

## Q73: How do you migrate existing agents to A2A?
**A:** Wrap existing agents with an A2A-compatible server. Implement the JSON-RPC endpoints, publish an Agent Card, and map existing functionality to A2A task semantics. The core agent logic doesn't need to change — only the communication layer.

## Q74: Can A2A agents have SLAs (Service Level Agreements)?
**A:** The Agent Card can declare expected response times or availability, but A2A doesn't enforce SLAs. SLA enforcement is handled through monitoring, alerting, and contract-level agreements between parties.

## Q75: How does A2A handle large payloads (GB-scale data)?
**A:** A2A supports file references (URI-based) instead of inline data. For large files, the agent can host the file and provide a URL. The client downloads it separately. A2A messages should be small; large data transfers use external storage.

## Q76: What testing frameworks support A2A?
**A:** The A2A Python SDK includes test utilities. You can also use standard HTTP testing tools (pytest + httpx, curl, Postman). Mock remote agents for integration tests. The A2A GitHub repo includes reference test suites.

## Q77: Can A2A agents have rate limits?
**A:** Yes. The Agent Card can declare rate limits (e.g., "100 requests/minute"). The remote agent enforces them and returns appropriate error responses (HTTP 429) when exceeded.

## Q78: How does A2A handle agent discovery at scale?
**A:** The current model is manual discovery (known URLs). For scale, you'd need a registry/index service that catalogs Agent Cards. This is an active area of development — agent registries and marketplaces are emerging.

## Q79: Can A2A agents run serverless (AWS Lambda, Cloudflare Workers)?
**A:** Yes. A2A agents are just HTTP endpoints. They can run anywhere — containers, VMs, serverless functions. Serverless is a good fit for lightweight agents that don't need persistent connections.

## Q80: What is the difference between A2A and MCP's "resources" concept?
**A:** MCP resources expose data to an agent (agent reads files, databases). A2A tasks delegate work to another agent (agent sends a task, receives a result). Resources are passive data access; A2A is active task collaboration.

## Q81: How do you handle authentication token refresh in A2A?
**A:** The client manages token refresh independently (standard OAuth2 refresh flow). When making A2A requests, the client attaches the current valid token. The remote agent validates it on each request. Token refresh is orthogonal to A2A.

## Q82: Can A2A agents negotiate protocols or formats?
**A:** Not natively. The Agent Card declares what the agent supports, and the client must comply. If there's a mismatch, the remote agent fails the task with an appropriate error. Future versions may add negotiation.

## Q83: How does A2A handle agent downtime gracefully?
**A:** Clients should implement retries, timeouts, and fallback agents. If a remote agent is down, the client can try an alternative agent with similar skills. The protocol itself doesn't handle availability — it's an application concern.

## Q84: Can A2A support voice or real-time audio agents?
**A:** A2A supports audio MIME types (audio/wav), but it's not designed for real-time streaming audio (like phone calls). For real-time voice, you'd use WebRTC or similar protocols, with A2A for task delegation.

## Q85: What is the relationship between A2A and OpenAI's Agents API?
**A:** OpenAI's Agents API defines how to build agents within OpenAI's ecosystem. A2A is a cross-vendor protocol. An OpenAI agent could expose itself as an A2A endpoint, allowing agents from other frameworks to delegate tasks to it.

## Q86: How do you monitor A2A agent performance?
**A:** Log task completion rates, latency, error rates, and token usage per task. Use APM tools (Datadog, Prometheus) on the HTTP endpoints. AgentOps and similar tools can track LLM-specific metrics within each agent.

## Q87: Can A2A agents have preferences or learned behavior?
**A:** The protocol doesn't define learning. However, agents can maintain internal state across tasks — tracking which approaches work best, which client preferences exist, or which strategies yield better results. This is implementation-specific.

## Q88: How does A2A handle graceful degradation?
**A:** If a remote agent can't fully complete a task, it can return partial results (state: `completed` with partial artifacts) or fail with a descriptive error. The client decides how to handle partial success — use what it got, try another agent, or escalate.

## Q89: What is the most common A2A use case in 2025?
**A:** Multi-agent workflows where a supervisor/orchestrator agent delegates specialized subtasks to expert agents (research, code generation, data analysis, content creation). This is the "agent team" pattern — each agent is an A2A endpoint.

## Q90: Can A2A agents implement circuit breaker patterns?
**A:** Yes, at the client level. If a remote agent fails repeatedly, the client can stop sending tasks (circuit open), periodically test if it's back (half-open), and resume when healthy (closed). This prevents cascade failures.

## Q91: How do you secure A2A endpoints in production?
**A:** HTTPS everywhere, OAuth2 or mTLS authentication, rate limiting, input validation, least-privilege API keys, network-level access controls (VPC, firewall rules), and audit logging. Treat A2A endpoints like any other production API.

## Q92: Can A2A agents support human-in-the-loop?
**A:** Yes. An agent can set state to `input-required` and ask the human (via the client) for approval or input. The client relays the human's response back. This enables workflows where agents draft and humans approve.

## Q93: What is the latency overhead of A2A vs. direct function calls?
**A:** A2A adds network latency (HTTP round-trip) plus JSON serialization/deserialization. For local agents, this is 1-10ms. For remote agents, it's 50-500ms+. Direct function calls are nanoseconds-microseconds. A2A trades latency for flexibility and decoupling.

## Q94: Can A2A agents have different model sizes (small vs. large LLMs)?
**A:** Yes. Each agent chooses its own LLM. A classification agent might use a small, fast model (GPT-4o-mini), while a complex reasoning agent uses a large model (Claude Opus). The A2A protocol is model-agnostic.

## Q95: How does A2A handle agent capability evolution?
**A:** Update the Agent Card when capabilities change. Clients re-fetch the card periodically or check at startup. Version numbers in the card indicate changes. Old clients using cached cards may not see new capabilities.

## Q96: Can A2A agents process tasks in different languages?
**A:** Yes. Agents can be language-specific (a French translation agent) or multilingual. The Agent Card can declare supported languages. Clients choose agents based on language requirements.

## Q97: What are the best practices for designing A2A agent skills?
**A:** Make skills specific and well-documented (not "does everything"). Define clear input/output schemas. Provide example tasks. Keep skills composable — small, focused skills that can be combined. Decline tasks outside your skill set rather than producing poor results.

## Q98: How does A2A relate to the broader agentic AI ecosystem?
**A:** A2A is a foundational protocol for the multi-agent future. As agents proliferate, they need to communicate. A2A provides the plumbing — like HTTP did for the web, A2A does for agent-to-agent communication. It enables agent networks, marketplaces, and ecosystems.

## Q99: What should you build first when adopting A2A?
**A:** Start with a simple agent that exposes 1-2 skills via A2A. Publish the Agent Card. Build a client that discovers and delegates tasks to it. Once that works, add more agents, implement multi-agent workflows, and layer on security and monitoring.

## Q100: What are the key A2A interview topics to master?
**A:** Agent Cards, task lifecycle (states and transitions), SSE streaming, push notifications, multi-turn conversations, authentication patterns, differences from MCP and function calling, protocol design decisions, and real-world multi-agent orchestration patterns.
