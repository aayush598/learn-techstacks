# Agno Interview Questions and Answers - Part 2

## Q1: How do you implement a custom tool in Agno that maintains state across multiple invocations within the same agent run?
**A:** Use a class-based tool that stores state in `self`. The class instance persists across tool calls during a single agent run cycle. Implement `__init__` for initial state, and ensure state is reset when the agent is re-initialized:

```python
class CounterTool:
    def __init__(self):
        self.count = 0
    def increment(self) -> str:
        self.count += 1
        return f"Count: {self.count}"
    def get_count(self) -> str:
        return str(self.count)
```

## Q2: How do you implement Agno knowledge bases with custom vector store backends (e.g., SingleStore, Redis Stack, Elasticsearch)?
**A:** Implement the `VectorDB` interface with methods for `upsert`, `search`, `delete`, and `create_collection`. Agno's vector store abstraction allows plugging any backend by implementing these core operations. Register the custom vector store via the knowledge base constructor:

```python
class SingleStoreDB(VectorDB):
    def search(self, query: str, limit: int = 10) -> list[Document]:
        # Implement ANN search via SingleStore's vector functions
        pass
```

## Q3: How do you implement Agno agent memory with session persistence and semantic retrieval over past conversations?
**A:** Use `VectorMemory` that stores conversation embeddings in a vector database. Each session is identified by a unique ID. On new messages, the agent retrieves semantically similar past interactions and injects them as context. Configure memory with `memory=VectorMemory(vector_db=ChromaDB(), session_id="user_123")`.

## Q4: How do you implement multi-modal agents in Agno that can process images, audio, and video inputs simultaneously?
**A:** Pass multiple media types in the same request using the `Image`, `Audio`, and `Video` media classes. The agent uses a capable multi-modal model (GPT-4V, Gemini, Claude 3) that processes all inputs:

```python
response = agent.run(
    "Analyze this meeting recording and the slide deck",
    images=[Image(url="slide1.png"), Image(url="slide2.png")],
    audio=[Audio(filepath="meeting.mp3")]
)
```

## Q5: How do you implement Agno agents that use structured outputs with nested Pydantic models and validation?
**A:** Define nested Pydantic models and pass the root model as `response_model`. Agno ensures the LLM returns valid JSON matching the schema, including nested structures, lists, and optional fields:

```python
class Address(BaseModel):
    street: str; city: str; zip: str

class Person(BaseModel):
    name: str; age: int; address: Address; tags: list[str]

response: Person = agent.run("Extract info", response_model=Person)
```

## Q6: How do you implement Agno agent teams with specialized roles and dynamic task delegation?
**A:** Create a Team with a coordinator agent that analyzes the task, breaks it into subtasks, and delegates to specialized member agents (researcher, writer, reviewer, coder). The coordinator synthesizes results. Configure member agent capabilities via their tool sets and instructions.

## Q7: How do you implement Agno agents with streaming and real-time tool call visualization?
**A:** Use `agent.run_stream(prompt)` which yields `RunEvent` objects. Track tool calls via `on_tool_call` events. The streaming iterator yields both text chunks and structured events for tool calls, results, and errors, enabling real-time UI updates:

```python
for event in agent.run_stream("Research AI trends"):
    if event.type == "tool_call": print(f"Calling: {event.name}")
    elif event.type == "text": print(event.text, end="")
```

## Q8: How do you implement custom Agno model providers for proprietary or self-hosted LLM APIs?
**A:** Implement the `Model` abstract class: `invoke(messages, **kwargs)`, `invoke_stream(messages, **kwargs)` (async generator), and `parse_response(response)`. Handle authentication, request formatting, streaming parsing, and error mapping. Register and use via `agent = Agent(model=MyCustomModel())`.

## Q9: How do you implement Agno workflows with conditional branching, parallel execution, and human-in-the-loop steps?
**A:** Use the `Workflow` class with decorated steps. Steps can return `NextStep` (continue), `EndWorkflow` (stop), or conditionally route. Parallel execution uses async step execution. Human-in-the-loop pauses and waits for external input:

```python
class MyWorkflow(Workflow):
    @step
    async def review(self, c) -> StepResult:
        result = await c.run_agent(reviewer_agent, c.input)
        if result.quality > 0.8: return EndWorkflow()
        return NextStep(result)
```

## Q10: How do you implement Agno agents with context management strategies (sliding window, summary, token-aware truncation)?
**A:** Configure `context=agent.Context(strategy="sliding_window", max_messages=20)` or `strategy="summary"` (summarize old messages) or `strategy="token_aware"` (truncate when approaching model's token limit). Combine strategies: summarize messages beyond the sliding window.

## Q11: How do you implement Agno agents that dynamically select which tools to use based on the task description?
**A:** Use a tool selection agent that analyzes the task and returns a subset of available tools. Then create a new agent with only the selected tools. Alternatively, implement a meta-tool that routes to sub-agents with different tool sets based on task classification.

## Q12: How do you implement Agno RAG with hybrid search (dense + sparse) and reciprocal rank fusion?
**A:** Configure a knowledge base with both dense (embedding) and sparse (BM25) retrievers. Use `HybridRetriever` that combines results using RRF:

```python
knowledge_base = KnowledgeBase(
    vector_db=ChromaDB(),
    retriever=HybridRetriever(
        dense_retriever=EmbeddingRetriever(),
        sparse_retriever=BM25Retriever(),
        fusion=ReciprocalRankFusion(k=60)
    )
)
```

## Q13: How do you implement Agno agents with guardrails that validate inputs and outputs against custom rules?
**A:** Create guardrail functions that raise `GuardrailError` or return modified content. Register via `agent = Agent(guardrails=[input_guardrail, output_guardrail])`:

```python
def pii_guardrail(text: str) -> str:
    if re.search(r'\b\d{3}-\d{2}-\d{4}\b', text):
        raise GuardrailError("SSN detected and blocked")
    return text
```

## Q14: How do you implement Agno agents with function calling that supports parallel tool execution (calling multiple tools simultaneously)?
**A:** Agno supports OpenAI-style parallel tool calling natively. When the LLM returns multiple tool calls in one response, Agno executes them concurrently using `asyncio.gather`. Results are collected and returned to the LLM in the same turn, reducing latency for independent tool calls.

## Q15: How do you implement Agno agents with custom error recovery and self-correction loops?
**A:** Configure `max_retries` and use the `on_tool_error` hook. The agent can analyze tool errors and adjust its approach:

```python
agent = Agent(
    tools=[my_tool],
    max_retries=3,
    on_tool_error=lambda e, ctx: ctx.add_message(f"Error: {e}. Try a different approach.")
)
```

## Q16: How do you implement Agno knowledge base with incremental updates and document versioning?
**A:** Use `knowledge_base.add_documents()` for incremental updates. The knowledge base checks document hashes to deduplicate. For versioning, store document metadata including version number. Implement custom `VersionedVectorDB` that filters by version during retrieval.

## Q17: How do you implement Agno agents with monitoring and observability via OpenTelemetry?
**A:** Enable OpenTelemetry instrumentation in Agno. Configure exporters for traces (Jaeger, Datadog). Each agent run creates a trace with spans for LLM calls, tool executions, and reasoning steps. Custom attributes (session ID, agent name, token count) enrich observability.

## Q18: How do you implement Agno agents with response model fallback (try structured output, fall back to unstructured parsing)?
**A:** Implement a wrapper that first attempts `response_model`. If parsing fails (JSON decode, validation error), fall back to extracting structured data from free text using regex or a secondary prompt:

```python
try:
    result = agent.run(prompt, response_model=MyModel)
except ValidationError:
    result = agent.run(f"Extract as JSON: {prompt}")
    result = parse_json(result.content)
```

## Q19: How do you implement Agno agents with session-based conversation history stored in PostgreSQL?
**A:** Use `SessionManager` with `PostgresSessionStore`. Configure the connection string and table name. Sessions are created per conversation, storing all messages with metadata. On agent initialization, pass `session_id=existing_id` to resume:

```python
agent = Agent(session_manager=PostgresSessionStore(conn_string="postgresql://..."))
```

## Q20: How do you implement Agno agent chaining where the output of one agent becomes the input of another?
**A:** Use the `Workflow` pattern or compose manually:

```python
result1 = agent1.run("Research quantum computing")
result2 = agent2.run(f"Write a summary based on: {result1.content}")
result3 = agent3.run(f"Review this summary: {result2.content}")
```

## Q21: How do you implement Agno agents with sub-agents that have access to different knowledge bases?
**A:** Create specialized agents with domain-specific knowledge bases, then use a Team or a router agent that directs queries to the appropriate sub-agent based on the topic:

```python
legal_agent = Agent(knowledge=legal_kb, instructions=["Answer legal questions"])
medical_agent = Agent(knowledge=medical_kb, instructions=["Answer medical questions"])
team = Team(leader=router_agent, members=[legal_agent, medical_agent])
```

## Q22: How do you implement Agno agents with automatic prompt optimization based on task performance feedback?
**A:** Track task success metrics per prompt template. When performance drops, use a meta-agent to analyze failures and suggest prompt improvements. Apply successful improvements as new prompt versions. This creates a feedback loop for continuous prompt refinement.

## Q23: How do you implement Agno agents with vision capabilities that analyze multiple images and generate structured reports?
**A:** Pass multiple `Image` objects to a single agent call. The model processes all images together. For structured reports, use `response_model` with fields for findings per image:

```python
class ImageFinding(BaseModel):
    image_index: int; objects: list[str]; description: str

class Report(BaseModel):
    findings: list[ImageFinding]; summary: str

report: Report = agent.run("Analyze these images", images=[img1, img2], response_model=Report)
```

## Q24: How do you implement Agno agents with the ReAct pattern modified to include verification steps?
**A:** Override the default run loop to add a verification step after each action. Before proceeding, the agent verifies the tool result makes sense. If verification fails, the agent retries the action or tries an alternative:

```python
class VerifiedAgent(Agent):
    async def _run_loop(self, messages):
        # Standard ReAct loop with verification
        for step in super()._run_loop(messages):
            if step.type == "tool_result" and not self._verify(step):
                yield self._retry_action(step)
            else:
                yield step
```

## Q25: How do you implement Agno knowledge base with multi-modal document indexing (text + images + tables)?
**A:** Use a multi-modal document loader that extracts text, images, and tables. Store text in a vector DB for semantic search, images in an image embedding DB (CLIP), and tables in a structured format. The retriever combines results from all sources.

## Q26: How do you implement Agno agents with caching strategies for LLM responses to reduce cost and latency?
**A:** Configure `agent.cache = Cache(backend=RedisCache(), ttl=3600)`. Cache keys are computed from (model, prompt, temperature). Implement `SemanticCache` that finds semantically similar cached responses using embedding similarity with a configurable threshold.

## Q27: How do you implement Agno agents with delayed tool execution (deferring expensive tool calls until needed)?
**A:** Use lazy tool definitions where the tool function returns a thunk/coroutine. The agent can decide to execute or skip based on intermediate reasoning. Implement a `LazyTool` wrapper that reports availability but defers computation.

## Q28: How do you implement Agno agents with automatic language detection and multilingual support?
**A:** Use a detection tool that identifies the input language, then configure the agent to respond in the detected language. Knowledge bases can store documents in multiple languages with language metadata tags, and the retriever filters by detected language.

## Q29: How do you implement Agno workflow with scheduled periodic execution using cron expressions?
**A:** Wrap the workflow in a script that uses a scheduler (APScheduler, Celery Beat). The scheduler triggers `workflow.run(input_data)` at specified intervals. Use session persistence for stateful workflows that run across invocations.

## Q30: How do you implement Agno agents with tool call batching where multiple related tool calls are combined?
**A:** Create a composite tool that accepts batch parameters. For example, instead of calling `get_weather(city)` multiple times, implement `get_weather_batch(cities: list[str])`. The agent can call the batch tool once with all cities, reducing round trips.

## Q31: How do you implement Agno agents with automatic API key rotation and credential management?
**A:** Create a credential manager that stores multiple API keys and rotates them on rate-limit errors. The custom model provider or tool wrapper checks current key, detects rate-limit responses, switches to the next key, and retries the request.

## Q32: How do you implement Agno agents that respect rate limits by implementing token bucket or sliding window algorithms?
**A:** Create a rate-limited tool wrapper that uses a token bucket algorithm. Each tool call consumes tokens. When the bucket is empty, the wrapper queues the request or returns a "retry after" message. Configure per-tool limits independently.

## Q33: How do you implement Agno agents with response streaming that updates a UI with intermediate reasoning and tool progress?
**A:** Use `run_stream` and forward events to the UI via WebSocket. Each event type triggers different UI updates: text chunks append to output, tool calls show spinners, tool results expandable details, and errors show inline:

```python
for event in agent.run_stream("Research"):
    if event.type == "text": await ws.send_json({"type": "token", "data": event.text})
    elif event.type == "tool_call": await ws.send_json({"type": "tool_start", "name": event.name})
```

## Q34: How do you implement Agno agents with structured outputs that include confidence scores and citations?
**A:** Design the response model with confidence and citation fields:

```python
class CitedResponse(BaseModel):
    answer: str; confidence: float; citations: list[Citation]

class Citation(BaseModel):
    text: str; source: str; relevance_score: float
```

## Q35: How do you implement Agno agents with custom knowledge base retrieval that uses query rewriting and HyDE?
**A:** Override the knowledge base's `retrieve` method. Implement query rewriting using an LLM call, generate a hypothetical document (HyDE), embed it, and retrieve based on the hypothetical document's embedding:

```python
class HyDEKnowledgeBase(KnowledgeBase):
    async def retrieve(self, query: str) -> list[Document]:
        hypothetical = await self.llm.generate(f"Write a document answering: {query}")
        return await self.vector_db.search(embed(hypothetical), limit=5)
```

## Q36: How do you implement Agno agents that detect and handle hallucinations by cross-referencing tool results?
**A:** After the agent responds, run a verification step that checks each factual claim against tool results or knowledge base. Claims not supported by any source are flagged as potential hallucinations. Configure action on detection: warn, remove, or re-generate.

## Q37: How do you implement Agno agents with asynchronous parallel execution of multiple independent agents?
**A:** Use `asyncio.gather` to run multiple agents concurrently:

```python
tasks = [
    agent1.arun("Research topic A"),
    agent2.arun("Research topic B"),
    agent3.arun("Research topic C"),
]
results = await asyncio.gather(*tasks)
```

## Q38: How do you implement Agno agents with custom run loop hooks for logging, metrics, and auditing?
**A:** Use the agent's event system: attach handlers to `on_start`, `on_tool_call`, `on_message`, `on_error`, `on_end`:

```python
agent.on("on_tool_call", lambda event: logger.info(f"Tool called: {event.name}"))
agent.on("on_error", lambda event: metrics.increment("agent_errors"))
```

## Q39: How do you implement Agno agents with tool discovery where the agent can list and learn about new tools at runtime?
**A:** Pass a `ToolRegistry` as a tool itself. The agent can call `list_tools()` to discover available tools, then `get_tool_schema(tool_name)` to learn about parameters. This enables dynamic tool selection without pre-configuring all tools.

## Q40: How do you implement Agno agents with cost-aware model selection that chooses the cheapest model sufficient for the task?
**A:** Use a model selector that evaluates task complexity (input length, required capabilities) and selects the most cost-effective model. Simple tasks use cheaper models (GPT-4o-mini, Claude Haiku), complex tasks use premium models (GPT-4o, Claude Opus):

```python
agent = Agent(model=CostAwareSelector(models=[cheap, medium, expensive]))
```

## Q41: How do you implement Agno agents that use vector memory to recall and learn from past mistakes?
**A:** Store errors and corrections in vector memory. Before each action, the agent retrieves similar past situations and their resolutions. This creates a feedback loop where the agent improves over time without explicit retraining.

## Q42: How do you implement Agno agents with response model that supports Union/Discriminated types for variable output shapes?
**A:** Use Pydantic's discriminated unions. The response model can vary based on content:

```python
class WeatherResponse(BaseModel): type: Literal["weather"]; temperature: float
class NewsResponse(BaseModel): type: Literal["news"]; headlines: list[str]
class GeneralResponse(BaseModel): type: Literal["general"]; text: str

Response = Union[WeatherResponse, NewsResponse, GeneralResponse]
```

## Q43: How do you implement Agno agents with knowledge base that supports multi-hop reasoning across documents?
**A:** Implement iterative retrieval: first retrieve documents, ask the agent what's missing, formulate a follow-up query, retrieve again, and combine. Configure `agent.knowledge.multi_hop = True` or implement custom logic in the workflow:

```python
class MultiHopAgent(Agent):
    async def run(self, prompt):
        docs = await self.knowledge.retrieve(prompt)
        gaps = await self.identify_gaps(prompt, docs)
        for gap in gaps: docs.extend(await self.knowledge.retrieve(gap))
        return await self.generate(prompt, docs)
```

## Q44: How do you implement Agno agents with structured output that enforces business rules and cross-field validation?
**A:** Add Pydantic validators to the response model:

```python
class OrderItem(BaseModel):
    product_id: str; quantity: int; unit_price: float

    @field_validator('quantity')
    def validate_quantity(cls, v): assert v > 0 and v < 1000; return v

    @model_validator(mode='after')
    def validate_total(self): assert self.quantity * self.unit_price < 10000; return self
```

## Q45: How do you implement Agno agents with automatic conversation summarization for long-running sessions?
**A:** Configure `context=SummaryContext(max_tokens=4000)`. When approaching the token limit, the agent automatically summarizes the oldest messages into a condensed summary, preserving key facts and decisions while discarding verbatim chat history.

## Q46: How do you implement Agno agents that use external knowledge bases (Wikipedia, company wikis) via API tools?
**A:** Create API tools that query external knowledge sources:

```python
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    import wikipedia; return wikipedia.summary(query, sentences=5)

agent = Agent(tools=[search_wikipedia])
```

## Q47: How do you implement Agno agents with tool dependency resolution where one tool's output feeds another?
**A:** The LLM naturally chains tools by reasoning: it calls tool A, receives the result, and then calls tool B with A's output. For complex dependency chains, use a workflow that explicitly orders tool calls with data passing between them.

## Q48: How do you implement Agno agents with custom embedding models (e.g., voyage-2, jina-embeddings) for specialized domains?
**A:** Implement the `Embedding` interface:

```python
class VoyageEmbedding(Embedding):
    def __init__(self, model="voyage-2"): self.client = voyageai.Client()
    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed(texts, model=self.model).embeddings
```

## Q49: How do you implement Agno agents with automatic retry on tool failure with exponential backoff and jitter?
**A:** Configure the tool's execution wrapper. Agno's tool executor supports `retry_count` and `retry_delay`. For custom control:

```python
import asyncio, random
async def resilient_tool_call(tool, args, max_retries=3):
    for attempt in range(max_retries):
        try: return await tool(**args)
        except Exception:
            if attempt == max_retries - 1: raise
            await asyncio.sleep(2 ** attempt + random.uniform(0, 1))
```

## Q50: How do you implement Agno agents that use the model's native tool calling vs. forcing tool use via prompt?
**A:** Set `use_tools="auto"` (model decides), `use_tools="force"` (model must use a tool), or `use_tools="none"` (no tools). For forced tool use, set `tool_choice="required"` or `tool_choice={"type": "function", "function": {"name": "my_tool"}}`.

## Q51: How do you implement Agno agents with conversation branching (multiple alternative responses evaluated and ranked)?
**A:** Run the agent multiple times with different temperature settings or prompts, collect all responses, and use a ranking agent to select the best one. This is similar to tree-of-thought:

```python
responses = await asyncio.gather(*[
    agent.arun(prompt, temperature=t) for t in [0.3, 0.7, 1.0]
])
best = await ranker_agent.arun(f"Which response is best? {responses}")
```

## Q52: How do you implement Agno agents with custom knowledge base chunking strategies (semantic, agentic, LLM-based)?
**A:** Implement a custom `TextSplitter`. Semantic chunking uses embedding similarity to detect topic shifts. Agentic chunking uses an LLM to identify logical breakpoints. LLM-based splitting asks the model to identify section boundaries:

```python
class SemanticSplitter(TextSplitter):
    def split(self, text):
        sentences = sent_tokenize(text)
        chunks, current = [], []
        for s in sentences:
            current.append(s)
            if len(' '.join(current)) > 500 or self._topic_shift(current):
                chunks.append(' '.join(current)); current = []
        return chunks
```

## Q53: How do you implement Agno agents with real-time data ingestion where the knowledge base updates mid-conversation?
**A:** Add documents to the knowledge base while the agent is running using `knowledge_base.add_documents()`. The agent can retrieve newly added documents on subsequent queries. Use a background task that monitors data sources and updates the vector store.

## Q54: How do you implement Agno agents that use adversarial prompting to test their own robustness?
**A:** Create a red-team agent that generates adversarial inputs (prompt injections, jailbreak attempts, edge cases). Run these against the primary agent and evaluate responses for safety violations. Log failures for guardrail improvement:

```python
def adversarial_test(agent, red_team_agent):
    attacks = red_team_agent.run("Generate 10 prompt injection attempts").attacks
    for attack in attacks:
        response = agent.run(attack)
        if not safety_check(response): failures.append(attack)
```

## Q55: How do you implement Agno agents with multi-tenant session isolation in a shared database?
**A:** Prefix session IDs with tenant ID (e.g., `tenant_123:session_456`). Configure the session store to filter by tenant prefix. The agent's session manager retrieves only sessions belonging to the current tenant, ensuring data isolation.

## Q56: How do you implement Agno agents that use a two-stage retrieval: coarse (fast, cheap) then fine-grained (slow, accurate)?
**A:** Implement a cascading retriever. First, use BM25 or lightweight embeddings for fast candidate selection (top-100). Then, use a cross-encoder to re-rank candidates (top-5). The agent receives only the top-ranked documents:

```python
class CascadeRetriever(Retriever):
    async def retrieve(self, query, limit=5):
        candidates = await self.fast_retriever.search(query, 100)
        return await self.reranker.rerank(query, candidates)[:limit]
```

## Q57: How do you implement Agno agents with automated testing using deterministic LLM mocks?
**A:** Use Agno's testing utilities or create a mock model provider that returns predefined responses based on input matching:

```python
class MockModel(Model):
    def __init__(self, responses: dict):
        self.responses = responses
    def invoke(self, messages, **kwargs):
        key = messages[-1]["content"]
        return Message(content=self.responses.get(key, "Mock response"))
```

## Q58: How do you implement Agno agents with tool-specific error messages that help the agent self-correct?
**A:** Design tools to return structured error responses with hints:

```python
def query_database(sql: str) -> str:
    try: return str(execute(sql))
    except Exception as e:
        return f"SQL Error: {e}. Hint: Check table name or use valid syntax."
```

## Q59: How do you implement Agno agents with automatic prompt compression using LLMLingua or similar techniques?
**A:** Compress the prompt before sending to the LLM. Strip irrelevant whitespace, remove redundant instructions, and compress retrieved context using a prompt compressor:

```python
from llmlingua import PromptCompressor
compressor = PromptCompressor()
compressed = compressor.compress(prompt, rate=0.5)
response = agent.run(compressed['compressed_prompt'])
```

## Q60: How do you implement Agno agents with structured outputs that include a chain-of-thought reasoning field?
**A:** Include a `reasoning` field in the response model:

```python
class AnalyzedResponse(BaseModel):
    reasoning: str  # chain-of-thought
    conclusion: str
    confidence: float
```

## Q61: How do you implement Agno agents with fine-grained tool access control (certain tools only available for certain users)?
**A:** Create a tool factory that filters tools based on user role/permissions. Use a session context that includes user attributes, and conditionally include tools when creating the agent:

```python
def create_agent(user_role: str):
    tools = [basic_tools]
    if user_role == "admin": tools.append(admin_tool)
    return Agent(tools=tools)
```

## Q62: How do you implement Agno agents with active learning where the agent identifies gaps in its knowledge base and requests new documents?
**A:** When the agent's confidence is low or it cannot find relevant information, it generates a "knowledge gap" report. This report is submitted to a document ingestion pipeline that sources and indexes new documents to fill the gap.

## Q63: How do you implement Agno agents with streaming that separates tool call progress from text output in the UI?
**A:** The streaming events include type information. The UI renders text tokens inline while showing tool calls as separate visual elements (cards, spinners with results). This creates a clear visual distinction between "thinking" and "doing."

## Q64: How do you implement Agno agents with custom response formatting (markdown, HTML, code blocks, diagrams)?
**A:** Instruct the agent in the system prompt to return specific formatting. For code, include language tags. For diagrams, use Mermaid syntax. The response can be rendered based on content type:

```python
agent = Agent(instructions=["Use Mermaid for diagrams", "Format code with language tags"])
```

## Q65: How do you implement Agno agents with a self-consistency decoding strategy (multiple runs, majority vote)?
**A:** Run the agent N times with the same input but higher temperature. Collect all structured responses, decode to final answers, and select the most common (majority voting). This improves reliability for factual tasks:

```python
responses = await asyncio.gather(*[agent.arun(question, temperature=0.7) for _ in range(5)])
answers = [extract_answer(r) for r in responses]
final = max(set(answers), key=answers.count)
```

## Q66: How do you implement Agno agents that consume streaming data from Kafka and act on it in real-time?
**A:** Create a consumer loop that reads Kafka messages and passes each to the agent:

```python
async for msg in consumer:
    response = await agent.arun(f"Process this event: {msg.value}")
    await producer.send("processed-events", response.content)
```

## Q67: How do you implement Agno agents with tool composition where a meta-tool calls multiple sub-tools?
**A:** Create a composite tool that orchestrates sub-tools internally:

```python
def research_topic(topic: str) -> str:
    """Research a topic comprehensively."""
    search_results = search_web(topic)
    summaries = [summarize_page(url) for url in search_results[:3]]
    return synthesize(summaries)
```

## Q68: How do you implement Agno agents with context-aware tool suggestions (suggesting relevant tools based on conversation)?
**A:** Before each LLM call, prepend a dynamic "available tools" section that excludes irrelevant tools based on conversation context. This reduces the prompt size and helps the model focus on appropriate tools.

## Q69: How do you implement Agno agents with model fallback where different providers handle different parts of the task?
**A:** Route subtasks to the optimal model: use a cheap model for classification/ routing, a specialized model for code generation, a vision model for image analysis. The Team pattern enables this with specialized member agents.

## Q70: How do you implement Agno agents with automatic response evaluation using LLM-as-judge?
**A:** After the agent responds, pass the query, response, and context to an evaluator agent. The evaluator scores: correctness, completeness, helpfulness, and safety. Low-scoring responses trigger re-generation:

```python
evaluation = await evaluator.arun(f"Query: {q}\nResponse: {r}\nRate 1-10")
if evaluation.score < 7: response = await agent.arun(q)  # retry
```

## Q71: How do you implement Agno agents with memory that persists across different agent instances (shared memory pool)?
**A:** Use a shared vector database as memory backend. Multiple agent instances read/write to the same memory store, tagged with session IDs and user IDs. Implement access controls to prevent cross-user leakage.

## Q72: How do you implement Agno agents with rationalization (explaining why specific tools were called)?
**A:** Include in the system prompt: "After each tool call, explain why you chose that tool and what you expect to learn." The response includes reasoning text before/after tool calls, providing transparency into the agent's decision process.

## Q73: How do you implement Agno agents with adaptive chunk size for knowledge retrieval (larger chunks for simple queries, smaller for precise)?
**A:** Implement a dynamic chunk selector. Analyze query complexity (length, specificity). Simple/general queries use larger chunks for broader context. Specific/ factoid queries use smaller chunks for precise information. Adjust chunk size per retrieval.

## Q74: How do you implement Agno agents with automatic database schema discovery for NL2SQL tools?
**A:** Create a tool that introspects the database schema (tables, columns, types, relationships) and caches it. The agent references this schema when generating SQL queries. Schema is refreshed periodically or on demand.

## Q75: How do you implement Agno agents with conversation decompression (expanding summaries back to detailed responses)?
**A:** Store full context alongside summaries. When a user asks about a past topic, the agent retrieves the full conversation from vector memory rather than relying only on the compressed summary, providing detailed recall.

## Q76: How do you implement Agno agents that use a scratchpad for intermediate computation and reasoning?
**A:** The agent's run loop naturally maintains reasoning in the conversation. For explicit scratchpad, add a tool that writes/reads to a temporary buffer:

```python
scratchpad = {}
def write_note(key: str, value: str) -> str: scratchpad[key] = value; return "Saved"
def read_note(key: str) -> str: return scratchpad.get(key, "Not found")
```

## Q77: How do you implement Agno agents with intent classification before tool execution to validate user requests?
**A:** Use a pre-processing step that classifies user intent (question, command, chitchat, sensitive request). Based on intent, the agent adjusts its behavior: allows tool use for commands and questions, restricts for sensitive topics, or redirects chitchat.

## Q78: How do you implement Agno agents with continuous learning from user feedback (reinforcement from human feedback)?
**A:** Collect user feedback (thumbs up/down, ratings) per response. Store feedback with conversation context. Periodically analyze patterns: which tools led to positive outcomes, which response styles work best. Use insights to update agent prompts and tool configurations.

## Q79: How do you implement Agno agents with automatic tool execution timeout for slow operations?
**A:** Configure tool-level timeout:

```python
@tool(timeout=10.0)  # seconds
def slow_api_call(query: str) -> str:
    return requests.get(f"https://slow-api.com/search?q={query}", timeout=10).text
```

## Q80: How do you implement Agno agents with retrieval that respects document-level access control?
**A:** Tag documents with access levels (public, internal, confidential). The retriever filters based on the user's clearance level. Agent instructions include: "Only use information the user has access to. Do not reveal confidential data."

## Q81: How do you implement Agno agents with response model that includes source attribution for each claim?
**A:** Design the response model to include citations inline:

```python
class Claim(BaseModel): text: str; source: str; page: int
class Response(BaseModel): claims: list[Claim]; summary: str
```

## Q82: How do you implement Agno agents with dynamic system prompt construction based on user profile and context?
**A:** Build the system prompt at runtime by composing sections: base instructions + user-specific instructions + session context + tool descriptions. This personalizes the agent's behavior without separate agent instances.

## Q83: How do you implement Agno agents with automatic language detection and response in kind?
**A:** Add a pre-processing tool that detects the query language and sets a `language` context variable. The system prompt includes: "Respond in the language of the user's query." The agent adapts its response language naturally.

## Q84: How do you implement Agno agents with tool usage analytics (which tools are called most, success rates, latencies)?
**A:** Wrap the agent's run loop with instrumentation. Record each tool call event with duration, success/failure, and token cost. Export to a time-series database for dashboarding. Analyze patterns to optimize tool selection and configuration.

## Q85: How do you implement Agno agents with concurrent knowledge base updates during active queries (read-write isolation)?
**A:** Use versioned vectors or database snapshots. When a retrieval occurs, it reads from the current snapshot. Writes create new versions. Readers are not blocked by writers. This ensures consistent retrieval results during a single query.

## Q86: How do you implement Agno agents with feedback loops where the agent critiques its own output before responding?
**A:** After generating a response, pass it through a self-critique step. The agent reviews its response for errors, omissions, and improvements. If issues are found, the agent regenerates. Configure max self-correction iterations:

```python
class SelfCritiquingAgent(Agent):
    async def run(self, prompt):
        response = await super().run(prompt)
        critique = await self.critique_agent.arun(f"Critique this response: {response.content}")
        if critique.needs_improvement:
            return await super().run(f"{prompt}\nPrevious attempt had issues: {critique.issues}")
        return response
```

## Q87: How do you implement Agno agents with graceful degradation when knowledge base is unavailable?
**A:** Configure fallback behavior: if vector DB is unreachable, try BM25, then fall back to LLM's parametric knowledge. The agent's system prompt includes: "If you cannot retrieve documents, answer based on your knowledge but state when doing so."

## Q88: How do you implement Agno agents with interactive data visualization tool (generate charts from data)?
**A:** Create a visualization tool that accepts data and chart type, generates the chart using matplotlib/plotly, and returns the image or HTML:

```python
def create_chart(data: str, chart_type: str) -> str:
    """Create a chart from CSV data. Returns HTML."""
    df = pd.read_csv(StringIO(data))
    fig = df.plot(kind=chart_type).get_figure()
    return fig_to_base64(fig)
```

## Q89: How do you implement Agno agents with role-based system prompts (customer support vs. internal analyst)?
**A:** Define prompt templates per role. When creating the agent, select the template based on the deployment context. Each template defines tone, constraints, tool availability, and response format:

```python
AGENT_ROLES = {
    "support": Agent(instructions=["Be helpful and patient", "Never speculate", "Escalate if unsure"]),
    "analyst": Agent(tools=[sql_tool, chart_tool], instructions=["Provide data-driven answers"]),
}
```

## Q90: How do you implement Agno agents with automatic PII redaction in conversation logs?
**A:** Configure post-processing hook that scans all messages for PII patterns (email, phone, SSN, credit card) using regex or NER. Redact detected PII with `[REDACTED]` before storing in session history:

```python
def redact_pii(message: Message) -> Message:
    message.content = re.sub(r'\b\d{16}\b', '[REDACTED]', message.content)
    return message
agent = Agent(post_processors=[redact_pii])
```

## Q91: How do you implement Agno agents that switch between models mid-conversation based on task difficulty?
**A:** Monitor conversation complexity (message length, tools used, domain). When complexity exceeds a threshold, upgrade to a more capable model. When simpler, downgrade to save costs. The agent is re-initialized with the new model but preserves session state.

## Q92: How do you implement Agno agents with encrypted session storage for sensitive conversations?
**A:** Implement a custom `SessionStore` that encrypts messages before writing to the database and decrypts on read. Use AES-GCM encryption with per-session keys stored in a secure key management service.

## Q93: How do you implement Agno agents with automatic detection of insufficient context and proactive retrieval?
**A:** Before responding, the agent evaluates if it has enough information. If not, it automatically formulates a retrieval query and fetches additional context. This is implemented as a pre-generation step in a custom agent run loop.

## Q94: How do you implement Agno agents that generate and execute code in a sandboxed environment?
**A:** Create a code execution tool that sends code to a sandbox (Docker container, Pyodide, or cloud function). The tool returns stdout, stderr, and execution time. The agent can iterate on code based on results:

```python
def run_python(code: str) -> str:
    """Execute Python code in a sandbox and return output."""
    result = subprocess.run(["docker", "run", "--rm", "python:3.11", "python", "-c", code],
                          capture_output=True, text=True, timeout=30)
    return result.stdout or result.stderr
```

## Q95: How do you implement Agno agents with citation verification (checking that citations actually support the claims)?
**A:** After the agent generates a response with citations, run a verification step. For each citation, extract the claim and the cited document. Verify that the document actually supports the claim using an LLM or NLI model. Flag unsupported citations.

## Q96: How do you implement Agno agents with persona persistence across sessions (consistent personality and knowledge)?
**A:** Store persona configuration (name, traits, expertise, conversation style) in the session metadata. On each session start, load the persona into the system prompt. Store "memories" about user preferences across sessions in vector memory.

## Q97: How do you implement Agno agents with tool usage quota tracking (max N calls per day per user)?
**A:** Implement a quota tracker as a tool wrapper. Before executing a tool, check the user's daily usage count. If exceeded, return a quota exceeded message. Reset counters daily. Store quotas in Redis for distributed consistency.

## Q98: How do you implement Agno agents with response model that supports streaming structured output (partial JSON parsing)?
**A:** Use partial JSON parsing to display structured data as it streams. For example, if the response model has an array of items, each item can be displayed as it's generated. Use `parse_partial_json` to handle incomplete JSON:

```python
for chunk in agent.run_stream(prompt, response_model=ItemList):
    if chunk.type == "text":
        partial = parse_partial_json(chunk.text)
        if partial and "items" in partial:
            for item in partial["items"]:
                ui.render_item(item)
```

## Q99: How do you implement Agno agents with multi-step reasoning using the ReAct pattern but with explicit checkpoints for verification?
**A:** Add verification steps at configurable intervals. After every N reasoning cycles, the agent must pass a verification checkpoint: summarize progress, confirm the plan is still valid, and adjust if needed. This prevents the agent from going down rabbit holes:

```python
class CheckpointAgent(Agent):
    async def _run_loop(self, messages, context):
        steps_since_check = 0
        for event in super()._run_loop(messages, context):
            yield event
            if event.type == "tool_result":
                steps_since_check += 1
                if steps_since_check >= 3:
                    verify = await self._verify_progress(context)
                    if not verify.on_track: yield self._correct_course(verify)
                    steps_since_check = 0
```

## Q100: How do you implement Agno agents with BDI (Belief-Desire-Intention) architecture for more human-like reasoning?
**A:** Model the agent's state with beliefs (knowledge about the world), desires (current goals), and intentions (action plan). The run loop updates beliefs based on tool results, re-evaluates desires, and adjusts intentions accordingly:

```python
class BDIAgent(Agent):
    def __init__(self):
        self.beliefs = {}; self.desires = []; self.intentions = []

    async def run(self, prompt):
        self.desires = self._extract_goals(prompt)
        while self.desires:
            intention = self._form_intention(self.desires[0], self.beliefs)
            result = await self._execute_intention(intention)
            self.beliefs.update(result)
            if self._goal_achieved(self.desires[0], result):
                self.desires.pop(0)
        return self._synthesize_response()
```
