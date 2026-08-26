# MCP (Model Context Protocol) — 100 Interview Q&A

---

## Q1: What is MCP?
**A:** Model Context Protocol (MCP) is an open standard protocol created by Anthropic (announced November 2024) that defines a universal, standardized way for AI models to connect to external data sources, tools, and services. It provides a single interface that replaces the need to build custom integrations for every provider.

## Q2: Who created MCP and when?
**A:** MCP was created by Anthropic and publicly announced in November 2024. It was open-sourced to encourage broad adoption across the AI ecosystem.

## Q3: What problem does MCP solve?
**A:** MCP solves the N×M integration problem. Without MCP, every AI application (N) needs a custom integration for every tool or data source (M), resulting in N×M bespoke connectors. MCP reduces this to N+M by providing a single universal protocol.

## Q4: What is the N×M integration problem?
**A:** If there are N AI applications and M external services, without a standard protocol you need N×M unique integrations. MCP introduces a universal interface so each application and service only needs one implementation, reducing complexity to N+M.

## Q5: What is the architecture of MCP?
**A:** MCP follows a client-server architecture with three core roles: the Host (the AI application like Claude Desktop or an IDE), the Client (a protocol client that maintains a 1:1 connection with a server), and the Server (a lightweight program that exposes tools, resources, and prompts to the AI model).

## Q6: What is the Host in MCP architecture?
**A:** The Host is the AI-powered application that the end user interacts with, such as Claude Desktop, VS Code with an AI extension, or a custom chat application. The Host manages one or more Client instances and controls permissions and user consent.

## Q7: What is the Client in MCP architecture?
**A:** The Client is a protocol-level component created by the Host that maintains a 1:1 stateful connection with a single MCP Server. It handles protocol negotiation, message routing, and capability discovery with its paired server.

## Q8: What is the Server in MCP architecture?
**A:** The Server is a lightweight program that exposes specific capabilities — tools, resources, and prompts — to the AI model via the MCP protocol. Servers are modular and each one focuses on a specific domain like a database, filesystem, or API.

## Q9: What are the three primitives in MCP?
**A:** The three primitives are Tools (actions the model can perform), Resources (data the model can read), and Prompts (reusable templates for AI interactions). Each serves a distinct purpose in connecting models to external capabilities.

## Q10: What are Tools in MCP?
**A:** Tools are actions that a model can request to execute on the server side, such as querying a database, sending an email, or calling an API. They are model-controlled — the model decides when to invoke them — and they require user consent before execution.

## Q11: What are Resources in MCP?
**A:** Resources represent data that the model can access, such as file contents, database records, or API responses. They are application-controlled — the host application decides how and when to provide resources to the model, often via context injection.

## Q12: What are Prompts in MCP?
**A:** Prompts are reusable templates that guide AI interactions. They are user-controlled — the end user selects which prompt to use — and they define structured input/output patterns for common tasks like code review, summarization, or data extraction.

## Q13: How does MCP differ from function calling?
**A:** Function calling is a vendor-specific mechanism (e.g., OpenAI's function calling) where tool definitions are sent with each API request. MCP is a vendor-neutral, stateful protocol with a standardized lifecycle, capability negotiation, and support for resources and prompts — not just tools. MCP also persists connections across requests.

## Q14: How does MCP differ from REST APIs?
**A:** REST APIs are stateless HTTP interfaces with no built-in concept of AI interaction. MCP is a stateful, bidirectional protocol specifically designed for AI model communication, with structured message passing, capability negotiation, and support for streaming and server-initiated messages.

## Q15: What is the difference between MCP and A2A (Agent-to-Agent)?
**A:** MCP defines how an AI agent communicates with tools and data sources (client-server). A2A (Google's Agent-to-Agent protocol) defines how multiple AI agents communicate with each other peer-to-peer. They are complementary — an agent can use MCP for tool access and A2A for inter-agent communication.

## Q16: How does MCP compare to LangChain tools?
**A:** LangChain tools are a Python framework-specific abstraction. MCP is a language-agnostic, cross-application protocol standard. MCP servers can be consumed by LangChain apps, but MCP is broader — it works across frameworks, languages, and host applications.

## Q17: How does MCP compare to OpenAPI/Swagger?
**A:** OpenAPI describes REST API interfaces for humans and code generation. MCP is a real-time bidirectional communication protocol. An MCP server can wrap an OpenAPI-described API, but MCP adds state management, streaming, capability negotiation, and AI-specific semantics that OpenAPI lacks.

## Q18: How does MCP compare to OpenAI plugins?
**A:** OpenAI plugins were vendor-specific and tightly coupled to ChatGPT. MCP is open-standard and vendor-neutral, working with any AI model or host application. MCP also supports resources and prompts, not just tool invocation, and provides a richer lifecycle and capability negotiation system.

## Q19: What transport protocols does MCP support?
**A:** MCP supports two main transports: stdio (standard input/output) for local processes where the host launches the server as a subprocess, and HTTP with Server-Sent Events (SSE) for remote servers over a network. Both use JSON-RPC 2.0 as the message format.

## Q20: What is stdio transport in MCP?
**A:** In stdio transport, the host launches the MCP server as a child process. Communication happens via standard input (stdin) and standard output (stdout) using newline-delimited JSON-RPC messages. This is ideal for local tool integrations and desktop applications.

## Q21: What is HTTP+SSE transport in MCP?
**A:** HTTP+SSE transport enables remote MCP servers. The client connects to an HTTP endpoint and uses Server-Sent Events (SSE) for server-to-client streaming, while client-to-server messages are sent via HTTP POST. This allows cloud-hosted, scalable MCP servers.

## Q22: What is JSON-RPC 2.0 in the context of MCP?
**A:** JSON-RPC 2.0 is the wire format MCP uses for all messages between client and server. It provides a simple request-response and notification structure with fields like method, params, and id. MCP builds its protocol semantics on top of this standard.

## Q23: How does capability negotiation work in MCP?
**A:** During the initialization handshake, the client and server exchange their supported capabilities (e.g., which tools, resources, or features they support). Both sides declare what they can do, and the connection proceeds with only mutually supported capabilities enabled.

## Q24: What is the MCP lifecycle?
**A:** The MCP lifecycle has three phases: Initialization (version handshake, capability negotiation), Operation (normal message exchange — tool calls, resource reads, prompt requests), and Shutdown (graceful termination of the connection).

## Q25: What happens during MCP initialization?
**A:** The client sends an `initialize` request with its protocol version and capabilities. The server responds with its own capabilities. The client then sends an `initialized` notification. After this handshake, normal operation begins.

## Q26: How does the model decide to call a tool in MCP?
**A:** The model receives tool definitions as part of its context. When it determines a tool would help answer the user's request, it generates a tool call request. The client routes this to the appropriate MCP server, executes it, and returns the result to the model.

## Q27: What does a minimal MCP server look like in Python?
**A:** A minimal Python MCP server uses the `mcp` package with a `FastMCP` server instance, registers a function with the `@server.tool` decorator, and runs the server via stdio transport. The decorator handles protocol compliance automatically.

## Q28: What Python package is used to build MCP servers?
**A:** The `mcp` Python package (installable via `pip install mcp`) provides the `FastMCP` class and decorators like `@server.tool`, `@server.resource`, and `@server.prompt` for building MCP servers quickly.

## Q29: How do you build an MCP server in TypeScript?
**A:** TypeScript MCP servers use the `@modelcontextprotocol/sdk` package. You create a `McpServer` instance, register tools with `server.tool()`, and connect via stdio or HTTP transport. The SDK handles JSON-RPC 2.0 protocol details.

## Q30: What SDKs are available for MCP?
**A:** Official MCP SDKs exist for Python (`mcp`), TypeScript (`@modelcontextprotocol/sdk`), Java (`io.modelcontextprotocol:sdk`), Kotlin, and C#/.NET. Community SDKs also exist for Go, Rust, and other languages.

## Q31: How do you register a tool in a Python MCP server?
**A:** Use the `@server.tool` decorator on an async or sync function. The function's name becomes the tool name, docstring becomes the description, and type hints are used to generate JSON Schema for input parameters automatically.

## Q32: How do you expose a resource in an MCP server?
**A:** Use the `@server.resource` decorator with a URI template (e.g., `file:///{path}`). The decorated function returns the resource content. Resources can be static or dynamic and support different MIME types.

## Q33: What are resource templates in MCP?
**A:** Resource templates use URI templates (RFC 6570) to define parameterized resource paths, like `postgres:///{table_name}`. This allows clients to request specific resources dynamically based on the URI parameters provided.

## Q34: What are resource subscriptions in MCP?
**A:** Resource subscriptions allow a client to subscribe to change notifications for a specific resource. When the resource changes on the server, the server sends a notification to the client, enabling reactive updates.

## Q35: What is the sampling feature in MCP?
**A:** Sampling allows an MCP server to request LLM completions from the client. The server sends a completion request through the client to the host's LLM, enabling agentic patterns where the server can leverage AI reasoning during tool execution.

## Q36: How does user consent work in MCP?
**A:** The Host application is responsible for obtaining user consent before executing tools or providing resources. MCP requires that users approve actions, especially destructive ones, before the client sends execution requests to the server.

## Q37: What security considerations apply to MCP?
**A:** Key security concerns include: user consent for tool execution, authentication between client and server, secrets management (not hardcoding API keys), input validation on server-side, output sanitization, and protection against prompt injection attacks.

## Q38: What authentication methods does MCP support?
**A:** MCP supports multiple authentication methods depending on transport: API keys for simple integrations, OAuth 2.0 for remote servers (especially HTTP transport), and mutual TLS (mTLS) for enterprise environments. The protocol is transport-agnostic regarding auth.

## Q39: How do you handle secrets in MCP servers?
**A:** Never hardcode secrets. Use environment variables, secrets managers (e.g., HashiCorp Vault, AWS Secrets Manager), or the host application's credential injection. MCP servers should receive secrets through secure channels, not protocol messages.

## Q40: How do you defend against prompt injection in MCP?
**A:** Defenses include: validating and sanitizing all tool outputs before injecting into LLM context, using structured output schemas, treating server responses as untrusted data, implementing output length limits, and never passing raw user-controlled data directly into prompts.

## Q41: What is MCP Inspector?
**A:** MCP Inspector is an interactive debugging tool provided by Anthropic that lets developers connect to an MCP server, inspect its capabilities, test tool calls, view resources, and debug protocol messages in real time. It is invaluable during development.

## Q42: How do you test an MCP server?
**A:** Use MCP Inspector for interactive testing, write unit tests for individual tool/resource functions, use the MCP SDK's test utilities to simulate client-server communication, and test error handling with invalid inputs and edge cases.

## Q43: How do you deploy MCP servers in production with Docker?
**A:** Package the MCP server in a Docker container with all dependencies, configure environment variables for secrets, use multi-stage builds for smaller images, set health checks, and for remote servers expose the HTTP+SSE transport endpoint behind a load balancer.

## Q44: How do you deploy MCP servers on Kubernetes?
**A:** Create Kubernetes Deployments for the MCP server containers, use ConfigMaps and Secrets for configuration, expose via Services or Ingress for HTTP transport, set resource limits, configure health probes (liveness/readiness), and use Horizontal Pod Autoscaler for scaling.

## Q45: How do you implement rate limiting in MCP servers?
**A:** Implement rate limiting at the server level using token bucket or sliding window algorithms, track requests per client/session, return appropriate JSON-RPC error responses when limits are exceeded, and consider using API gateways for centralized rate limiting.

## Q46: How do you monitor MCP servers in production?
**A:** Collect metrics (request counts, latency, error rates) using Prometheus or similar, log protocol events and errors with structured logging, set up alerts on error rate spikes, trace requests across distributed systems with OpenTelemetry, and monitor resource usage.

## Q47: How do you implement health checks for MCP servers?
**A:** For HTTP transport, expose a `/health` endpoint that verifies server connectivity and dependency health. For stdio transport, implement process-level health monitoring. In Kubernetes, configure liveness and readiness probes that check the health endpoint.

## Q48: Can an MCP server handle multiple concurrent tool calls?
**A:** Yes. MCP servers can handle multiple concurrent requests from clients. The JSON-RPC 2.0 protocol uses request IDs to match responses with requests, allowing concurrent in-flight operations. Servers should be designed to be thread-safe or use async processing.

## Q49: What is server chaining in MCP?
**A:** Server chaining occurs when one MCP server acts as a client to another MCP server, creating a pipeline of capabilities. This allows composing multiple specialized servers into more complex workflows, with each server adding its own domain-specific tools and resources.

## Q50: Can MCP servers be stateful?
**A:** Yes. MCP servers can maintain state across requests within a session, such as database connections, cached data, or user-specific context. The stateful nature of MCP connections enables this, but servers should handle reconnection gracefully.

## Q51: How does MCP handle multi-tenancy?
**A:** Multi-tenant MCP servers can isolate tenant data through session-level context, database row-level security, or separate server instances per tenant. The server should validate tenant identity from authentication context and enforce data isolation boundaries.

## Q52: How does error handling work in MCP?
**A:** MCP uses standard JSON-RPC 2.0 error codes plus MCP-specific error types. Servers return error responses with code, message, and optional data. Common errors include `MethodNotFound`, `InvalidParams`, `InternalError`, and `ToolExecutionError`.

## Q53: What MCP-specific error codes exist?
**A:** MCP defines errors like `-32601` (Method Not Found), `-32602` (Invalid Params), `-32603` (Internal Error), and application-level errors for tool execution failures, resource not found, and capability mismatches.

## Q54: How does versioning work in MCP?
**A:** During initialization, client and server exchange protocol version strings. If versions are incompatible, the handshake fails. The protocol version follows semantic versioning, with minor versions being backward-compatible and major versions indicating breaking changes.

## Q55: How does MCP handle backward compatibility?
**A:** MCP uses capability negotiation so that newer servers can support older clients and vice versa. Features that a client or server doesn't declare in capabilities are not used. Minor protocol versions add optional features without breaking existing functionality.

## Q56: How does MCP integrate with LangChain?
**A:** LangChain provides an `MCPServerAdapter` or MCP tool wrapper that can connect to MCP servers and expose their tools as LangChain-compatible tools. This allows LangChain agents and chains to use MCP server capabilities natively.

## Q57: How does MCP integrate with CrewAI?
**A:** CrewAI can wrap MCP servers as tools for its agents. By connecting to an MCP server, CrewAI agents gain access to the server's tools and resources, enabling multi-agent systems to leverage MCP's broad ecosystem of integrations.

## Q58: How does MCP integrate with LlamaIndex?
**A:** LlamaIndex can use MCP servers as tool sources for its RAG pipelines and agents. MCP tools can be converted to LlamaIndex tool objects, allowing queries that combine retrieved context with MCP-powered actions.

## Q59: How does MCP work with Ollama and local LLMs?
**A:** Ollama and local LLMs can be used with MCP by configuring the host application to use a local model for completions while connecting to MCP servers for tool execution. The host handles the translation between local model outputs and MCP protocol messages.

## Q60: What is the MCP server registry?
**A:** The MCP server registry is a community-maintained collection of available MCP servers. Anthropic maintains an official reference at `modelcontextprotocol/servers` on GitHub, and registries like Smithery and Glama provide searchable indexes of hundreds of servers.

## Q61: What MCP servers are commonly available?
**A:** Common MCP servers include filesystem access, PostgreSQL/SQLite databases, Git operations, GitHub/GitLab integration, Brave Search, Puppeteer browser automation, Google Drive, Slack, email (SMTP), Docker, Kubernetes, and many more.

## Q62: How do you build a database MCP server?
**A:** Create an MCP server that exposes tools for querying the database (SELECT, INSERT, UPDATE), resources for table schemas and data, and connection pooling. Use parameterized queries to prevent SQL injection and validate all inputs.

## Q63: How do you build a filesystem MCP server?
**A:** A filesystem MCP server exposes tools for reading, writing, listing, and searching files. It should enforce path restrictions to sandbox access, validate file types, handle permissions, and support both local and remote filesystems.

## Q64: What is the `call_tool` message in MCP?
**A:** `call_tool` is a request message sent from the client to the server to execute a specific tool with given arguments. The server processes the request and returns a result or error. This is the primary mechanism for model-driven actions.

## Q65: What is the `list_tools` message in MCP?
**A:** `list_tools` is a request that retrieves the list of available tools from the server. Each tool includes its name, description, and JSON Schema for input parameters. The client uses this during initialization or when refreshing capabilities.

## Q66: What is the `list_resources` message in MCP?
**A:** `list_resources` retrieves available resources from the server. Each resource has a URI, name, description, and MIME type. The client uses this to understand what data the server can provide.

## Q67: What is the `read_resource` message in MCP?
**A:** `read_resource` requests the content of a specific resource by URI. The server returns the resource content (text or binary) along with its MIME type. This is how the host provides data context to the model.

## Q68: What is the `list_prompts` message in MCP?
**A:** `list_prompts` retrieves available prompt templates from the server. Each prompt includes a name, description, and argument schema. Users can then select a prompt and provide arguments to generate structured interactions.

## Q69: What is the `get_prompt` message in MCP?
**A:** `get_prompt` requests a specific prompt template with arguments. The server processes the template with the provided arguments and returns a structured prompt (typically a list of messages) ready for use with the AI model.

## Q70: How do you handle large data in MCP?
**A:** For large data, use chunked resource reading, paginated tool responses, streaming via SSE, or reference-based access where resources return URIs instead of inline data. Avoid returning massive payloads in single messages to prevent context overflow.

## Q71: How do you handle file uploads with MCP?
**A:** File uploads can be handled by tools that accept file paths or URIs, binary resource content, or multipart data. For large files, use streaming uploads, resumable protocols, or upload to cloud storage and pass the resulting URI to the MCP tool.

## Q72: How do you implement streaming in MCP?
**A:** MCP supports streaming through Server-Sent Events (SSE) for HTTP transport. Servers can send partial results or progress updates. The `notifications/progress` message type allows servers to report long-running operation progress to clients.

## Q73: What is the progress notification in MCP?
**A:** Progress notifications allow servers to report the status of long-running operations. The server sends `notifications/progress` messages with a progress token, current progress, and optional total, enabling the client to show progress to the user.

## Q74: How do you implement logging in MCP servers?
**A:** MCP provides a `logging/setLevel` message that allows clients to configure log levels on servers. Servers can send `notifications/message` log messages back to the client. Use structured logging internally for debugging and observability.

## Q75: How do you implement cancellation in MCP?
**A:** Clients can send `notifications/cancelled` with a request ID to cancel an in-flight request. Servers should check for cancellation and clean up resources. This is important for long-running operations that may become irrelevant.

## Q76: What are roots in MCP?
**A:** Roots define the boundaries of what an MCP server can access. They are URI-based filesystem or resource roots that the client provides to the server, restricting the server's scope to specific directories or resource namespaces for security.

## Q77: What is the `notifications/roots/list_changed` message?
**A:** This notification is sent from the client to the server when the set of available roots changes (e.g., the user opens a new project folder). The server can then update its understanding of accessible resources.

## Q78: How do you build an MCP server for a REST API?
**A:** Create an MCP server that wraps each REST endpoint as a tool, maps request/response schemas to JSON Schema, handles authentication, manages rate limiting, and translates REST errors into MCP error responses. Use async HTTP clients for performance.

## Q79: How do you handle authentication in remote MCP servers?
**A:** For remote MCP servers over HTTP transport, implement OAuth 2.0 flows (authorization code, client credentials), validate tokens on each request, support token refresh, and use HTTPS for transport security. The server should reject unauthenticated requests.

## Q80: What is the difference between server-initiated and client-initiated messages in MCP?
**A:** Client-initiated messages are requests and notifications sent from the client to the server (e.g., `call_tool`, `read_resource`). Server-initiated messages include responses to client requests and notifications sent from the server to the client (e.g., progress updates, resource change notifications, log messages).

## Q81: How do you handle concurrent MCP server connections?
**A:** A host application can maintain multiple Client instances, each connected to a different server. Each connection is independent with its own capability negotiation and state. The host manages routing requests to the correct client/server pair.

## Q82: What is the model in the context of MCP?
**A:** The model is the AI/LLM that processes user inputs and decides when to use tools, resources, or prompts. The model itself doesn't communicate directly with MCP servers — the host and client handle protocol communication on the model's behalf.

## Q83: How do you debug MCP server issues?
**A:** Use MCP Inspector for interactive debugging, enable verbose logging, inspect JSON-RPC messages with network proxies for HTTP transport, use stdio redirection for local servers, and check server process exit codes for crash diagnostics.

## Q84: What are common MCP development mistakes?
**A:** Common mistakes include: not implementing capability negotiation correctly, hardcoding secrets, not validating inputs, returning overly large responses, ignoring cancellation requests, not handling reconnection, and failing to implement proper error responses.

## Q85: How do you ensure MCP server reliability?
**A:** Implement proper error handling and fallbacks, add health checks and auto-recovery, use connection pooling and retry logic, implement circuit breakers for dependent services, monitor error rates, and test failure scenarios thoroughly.

## Q86: Can MCP servers call other MCP servers?
**A:** Yes, through server chaining or by having a server act as both a client and server. A meta-server can aggregate capabilities from multiple backend MCP servers, presenting a unified interface while delegating to specialized servers.

## Q87: How do you version MCP server APIs?
**A:** Version tools and resources by including version in names (e.g., `search_v2`), use separate tool namespaces per API version, maintain backward-compatible changes, and leverage the protocol version negotiation for breaking changes.

## Q88: What is the role of JSON Schema in MCP?
**A:** JSON Schema defines the input and output structures for tools, resources, and prompts. Tools use JSON Schema to describe their parameters, enabling the model to generate correct arguments. The MCP SDKs auto-generate schemas from type hints.

## Q89: How do you implement output sanitization in MCP?
**A:** Sanitize tool outputs by removing or escaping sensitive data, limiting response sizes, validating output formats, stripping HTML/scripts if injecting into prompts, and filtering PII. Treat all server outputs as potentially untrusted before model consumption.

## Q90: How does MCP handle binary data?
**A:** MCP supports binary data through base64 encoding in JSON-RPC messages or through resource reads with binary MIME types. For large binary data, streaming or file-based transfer is recommended over inline base64 encoding.

## Q91: What are the best practices for MCP server design?
**A:** Best practices include: single responsibility per server, clear tool/resource naming, comprehensive JSON Schema definitions, proper error messages, input validation, output sanitization, documentation via descriptions, and implementing all relevant lifecycle phases.

## Q92: How do you handle timeouts in MCP?
**A:** Implement timeouts on both client and server sides. Clients should set reasonable timeouts for tool calls and handle timeout errors gracefully. Servers should complete operations within expected timeframes and use progress notifications for long-running tasks.

## Q93: Can MCP work with edge computing or IoT?
**A:** Yes. The stdio transport works well for local agents on edge devices. For remote scenarios, lightweight HTTP+SSE servers can run on constrained environments. MCP's modular design allows deploying only needed capabilities on resource-limited devices.

## Q94: How does MCP handle idempotency?
**A:** MCP itself doesn't enforce idempotency, but servers should implement it for critical operations. The client can retry failed requests using the same request ID. Servers should handle duplicate requests gracefully, especially for write operations.

## Q95: What analytics can you track with MCP servers?
**A:** Track tool invocation counts, resource access patterns, error rates, response times, request/response sizes, user consent decisions, concurrent connection counts, and prompt usage. This data helps optimize server performance and understand usage patterns.

## Q96: What is the future of MCP?
**A:** MCP is rapidly becoming the de facto standard for AI-tool connectivity. Expected developments include broader SDK support, more server implementations, enterprise features, standardized auth patterns, integration with major cloud platforms, and potential IETF/RFC standardization.

## Q97: How many MCP servers exist in the ecosystem?
**A:** The MCP ecosystem has grown to hundreds of community and official servers covering databases, version control, cloud services, productivity tools, browsers, file systems, and more. The registry at GitHub's `modelcontextprotocol/servers` and third-party indexes like Smithery track available servers.

## Q98: What companies have adopted MCP?
**A:** Beyond Anthropic, companies like Microsoft (VS Code/Copilot), OpenAI, Google (Workspace integrations), Replit, Sourcegraph, and many startups have adopted or announced MCP support, making it a cross-industry standard for AI tool connectivity.

## Q99: How do you contribute to the MCP ecosystem?
**A:** Contribute by building MCP servers for new services, improving existing SDKs, writing documentation, reporting issues, participating in the specification discussions on GitHub, and sharing servers in community registries.

## Q100: What are the key takeaways about MCP?
**A:** MCP is an open, vendor-neutral protocol that standardizes AI-to-tool connectivity, solving the N×M integration problem. It provides a clean architecture (Host/Client/Server), three powerful primitives (Tools/Resources/Prompts), flexible transports (stdio/HTTP), robust security patterns, and a growing ecosystem — making it essential knowledge for anyone building AI-powered applications.
