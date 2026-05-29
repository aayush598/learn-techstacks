# LangChain — 100 Interview Q&A
> Based on real-world LLM application development, RAG pipelines, agent architectures, and production deployment patterns using LangChain v0.3+.

---

## 1. Core Concepts & Architecture (Q1–Q20)

**Q1: What is LangChain and what problem does it solve?**
A: LangChain is a framework for building LLM-powered applications. It solves: 1) abstracting LLM provider APIs (OpenAI, Anthropic, local models), 2) composing multiple LLM calls via chains, 3) integrating external data (RAG), 4) building agents with tool use, and 5) managing prompts, memory, and output parsing. It provides a unified interface for pattern composition.

**Q2: Explain the core abstractions in LangChain: Model, Prompt, Output Parser, Chain, and Agent.**
A: 
- Model: wrapper around LLM providers (ChatOpenAI, Anthropic, Ollama)
- Prompt: template for constructing LLM inputs (PromptTemplate, ChatPromptTemplate)
- Output Parser: structures LLM output (StrOutputParser, PydanticOutputParser, JsonOutputParser)
- Chain: sequence of steps (LLM + prompt + parser or multiple LLMs piped together)
- Agent: LLM that decides which tools to call, loops until task complete

**Q3: What is LCEL (LangChain Expression Language) and why is it important?**
A: LCEL is a declarative syntax (using `|` pipe operator) to compose LangChain components into chains. It provides built-in streaming, async support, batch, parallel execution, retries, and LangSmith tracing. Example: `chain = prompt | model | parser`. LCEL is the recommended way to build chains in LangChain v0.2+.

**Q4: Explain the difference between ChatModels and LLMs (completion models) in LangChain.**
A: ChatModels (ChatOpenAI, ChatAnthropic) exchange messages (SystemMessage, HumanMessage, AIMessage) — they use chat-based APIs. LLMs (OpenAI, Anthropic) accept string input and return string output — completion APIs. LangChain v0.3+ focuses on ChatModels. Use ChatModels unless you need legacy completion endpoints.

**Q5: What is the concept of "Runnable" in LangChain?**
A: Runnable is the base interface that all LCEL components implement. Provides: `invoke()` (sync call), `ainvoke()` (async), `stream()`, `batch()`, `abatch()`. Runnables can be combined with `|` (pipe), composed with `RunnableSequence`, branched with `RunnableParallel`, and configured with `.configurable_fields()`. Everything in LCEL is a Runnable.

**Q6: What is a RunnableSequence and how does it differ from a RunnableParallel?**
A: RunnableSequence runs steps sequentially — output of step i feeds into step i+1. Built with `|` operator. RunnableParallel runs steps concurrently on the same input — outputs are merged into a dict. Example: `chain = {"context": retriever, "question": lambda x: x} | prompt | model` — retriever runs in parallel with identity passthrough.

**Q7: What is a RunnableLambda and when would you use it?**
A: RunnableLambda wraps an arbitrary Python function as a Runnable, making it composable in LCEL. Used for: custom preprocessing/postprocessing, calling external APIs, formatting outputs, adding business logic. Example: `RunnableLambda(lambda x: x["key"].upper())`. Avoid putting heavy logic here — use as glue between LCEL components.

**Q8: Explain RunnablePassthrough and RunnableBranch.**
A: RunnablePassthrough: passes input through unchanged (identity) or passes specific keys. Used to forward context in parallel chains. RunnableBranch: conditional chain routing — like if-elif-else in LCEL. Each branch is a (predicate, runnable) pair. Example: route short queries to fast model, long queries to powerful model.

**Q9: How does LangChain handle streaming with LCEL?**
A: Any LCEL chain supports `.stream()` if all components support streaming. Token-by-token for LLMs + parsed output streaming for parsers. Implemented via Runnable's `stream()` method which yields chunks. For final output parsing, LangChain buffers tokens and emits parsed chunks. Async streaming with `astream()`.

**Q10: What is LangSmith and how does it integrate with LangChain?**
A: LangSmith is LangChain's observability platform for LLM apps. It traces every run (LLM calls, retrievals, chains), logs inputs/outputs, measures latency/token usage, and supports evaluation/testing. Integrated via `LANGCHAIN_TRACING_V2=true` environment variable. Essential for debugging complex chains and monitoring production.

**Q11: What is LangServe and when would you use it?**
A: LangServe deploys LangChain chains as REST APIs with auto-generated FastAPI endpoints. Provides: `/invoke`, `/stream`, `/batch` endpoints, auto-generated OpenAPI/Swagger docs, input/output schemas, and client SDK generation. Used to expose chains as microservices. Deploy via `langchain serve` or programmatically with FastAPI.

**Q12: Explain the different types of prompt templates in LangChain.**
A: 
- PromptTemplate: for string-based LLMs `"Tell me about {topic}"`
- ChatPromptTemplate: for chat models, composed of message templates
- MessagesPlaceholder: inserts variable-length messages (history, tool results)
- FewShotPromptTemplate: few-shot examples with example selector
- PipelinePromptTemplate: combine multiple templates
- DynamicPrompt: templates that change based on input

**Q13: What is a ChatPromptTemplate and how do you compose multi-turn prompts?**
A: ChatPromptTemplate builds a list of chat messages from templates. Example:
```python
ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])
```
MessagesPlaceholder injects previous conversation turns. Supports SystemMessage, HumanMessage, AIMessage, ToolMessage types.

**Q14: How does LangChain handle tool calling with LLMs?**
A: LangChain defines tools via `@tool` decorator, Tool class, or BaseTool subclass. Tools have: name, description, args_schema (JSONSchema), and a `_run` method. LLMs that support tool calling (OpenAI, Anthropic, Gemini) receive tools in the API call. The LLM returns tool_calls in AIMessage, which LangChain dispatches to tools.

**Q15: What is a @tool decorator and what are its key parameters?**
A: `@tool` decorates a function as a LangChain tool:
```python
@tool
def search(query: str) -> str: ...
```
Key params: `name`, `description` (used by LLM to choose tool), `return_direct` (return tool output to user without LLM), `args_schema` (pydantic model for parameter validation), `response_format` ("content" or "content_and_artifact").

**Q16: What is the ToolMessage type and when is it used?**
A: ToolMessage represents the result of a tool call, sent back to the LLM. Contains: content (result string), tool_call_id (matches the tool_call that triggered it), name, and optional artifact. In agent loops, after tool execution, ToolMessage is appended to history and fed to the LLM for continuation.

**Q17: Explain the concept of "bind" in LangChain tools.**
A: `bind()` attaches runtime arguments to a Runnable without changing its signature. Example: `model.bind_tools(tools)` injects tool definitions to the model call. `model.bind(stop=["\n"])` sets stop tokens. `chain.bind(input_key="value")` provides constant values. Useful for configuring components at chain creation time.

**Q18: What is the difference between "invoke" and "batch" in LangChain?**
A: `invoke`: single input → single output. `batch`: list of inputs → list of outputs, with configurable parallelism via `RunnableConfig(max_concurrency=N)`. Both support streaming (via `stream` / `batch` returns all at once). Batch is more efficient for independent requests.

**Q19: How does LangChain's callback system work?**
A: Callbacks provide hooks into chain execution. BaseCallbackHandler has methods: on_llm_start/end, on_chain_start/end, on_tool_start/end, on_retriever_start/end, etc. Used for logging, monitoring, streaming UI updates. Configured via CallbackManager or passed in RunnableConfig. LangSmithHandler is the primary production callback.

**Q20: What is the role of RunnableConfig in LangChain?**
A: RunnableConfig carries runtime configuration: callbacks, metadata (run name, tags), max_concurrency, recursion_limit, and run_id. Passed through every Runnable invocation. Enables tracing, cancellation, and configuration override without changing the chain definition.

## 2. Chains & Composability (Q21–Q35)

**Q21: What is a "chain" in LangChain and how do you build one?**
A: A chain is a sequence of steps (LLM calls, retrievals, transforms) combined to accomplish a task. Built via LCEL with `|` operator. Example: `chain = prompt | model | parser`. Each step must be a Runnable. LangChain also offers legacy Chain classes (LLMChain, SimpleSequentialChain) but LCEL is preferred.

**Q22: Explain the difference between a sequential chain and a parallel chain.**
A: Sequential chain (`|`): steps execute one after another, output of each is input to next. Parallel chain (`RunnableParallel`): steps execute concurrently on the same input, results merge into a dict. Combined: `{"step1": chain1, "step2": chain2} | combine | model`.

**Q23: How do you implement branching logic in LCEL chains (conditionals)?**
A: Using `RunnableBranch`:
```python
chain = RunnableBranch(
    (lambda x: len(x) < 100, short_chain),
    (lambda x: len(x) < 1000, medium_chain),
    long_chain  # default
)
```
Each branch is (predicate_fn, runnable). First matching predicate executes. For simple routing, use `RunnableLambda` with `if/else`.

**Q24: What is a "RunnableMap" (RunnableParallel) and give a use case.**
A: RunnableParallel runs multiple runnables on same input, returns dict of results. Use case: RAG where retriever and query processing run concurrently:
```python
chain = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
}) | prompt | model | parser
```
Retriever fetches docs while question passes through, then both feed into prompt.

**Q25: How do you handle errors in LCEL chains?**
A: 
- `.with_retry()` — auto-retry on failure with exponential backoff
- `.with_fallbacks()` — fallback chain if primary fails
- Try/except in RunnableLambda — catch and handle errors
- `Runnable.with_retry(stop_after_attempt=3)` for transient errors (rate limits, timeouts)
- Use callbacks for error logging and monitoring

**Q26: What is the purpose of `.configurable_fields()` and `.configurable_alternatives()`?**
A: 
- `.configurable_fields()`: expose specific component params as runtime config (e.g., change model temperature)
- `.configurable_alternatives()`: swap entire components (e.g., use different LLM providers or retrieval strategies)
- Configured at invoke time via `RunnableConfig`. Enables A/B testing, per-user customization.

**Q27: How does LangChain handle stateful chains (conversation memory)?**
A: Via `BaseChatMemory` implementations:
- ConversationBufferMemory: stores all messages
- ConversationSummaryMemory: summarizes older messages
- ConversationBufferWindowMemory: keeps last k turns
- VectorStoreRetrieverMemory: retrieves relevant history
- Used with Chains or agents to maintain conversation context

**Q28: What is StringOutputParser vs PydanticOutputParser vs JsonOutputParser?**
A: 
- StringOutputParser: returns raw string — simplest, identity for strings
- StrOutputParser: handles string/bytes conversion from LLM output
- PydanticOutputParser: parse into a Pydantic model using structured output
- JsonOutputParser: parse JSON object from LLM output
- Composable: pipe parsers or use with structured LLM output features

**Q29: How do you implement custom output parsers in LangChain?**
A: Subclass `BaseOutputParser[T]` and implement:
- `parse(text: str) -> T`: core parsing logic
- (optional) `get_format_instructions() -> str`: instructions for LLM on output format
- (optional) `parse_with_prompt(text, prompt)`: with prompt context
Register with `@chain` decorator or use RunnableLambda for simple cases.

**Q30: What is the difference between RunnableSequence and SequentialChain?**
A: RunnableSequence (LCEL): modern, supports streaming/async/batch/tracing, type-safe, composable. SequentialChain: legacy class, verbose, no streaming, deprecated. Always use LCEL (RunnableSequence) for new chains.

**Q31: How do you add memory to an LLM chain in LangChain?**
A: In LCEL: use `RunnableWithMessageHistory` which wraps a chain and manages message history persistence. Provide `get_session_history` to load/save by session_id. Under the hood, it prepends history to prompt via MessagesPlaceholder. Supports ChatMessageHistory backends: InMemory, SQL, Redis, etc.

**Q32: What is RunnableWithMessageHistory and how do you configure it?**
A: Wraps another Runnable, maintains message history per session_id:
```python
chain = prompt | model | parser
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda sid: SQLChatMessageHistory(sid, "sqlite:///history.db"),
    input_messages_key="input",
    history_messages_key="chat_history"
)
```
At invoke time, pass `configurable={"session_id": "abc"}`.

**Q33: How does LangChain handle large documents in summarization chains?**
A: Two strategies:
- Stuff: fit entire doc in one prompt — simple but hits context limits
- Map-Reduce: split doc → summarize each chunk (map) → combine summaries (reduce)
- Refine: sequential, each chunk refines previous summary
- In LCEL: compose with RunnableParallel for map step, reduce with another LLM call
- LangChain provides `load_summarize_chain` with these modes

**Q34: What is the "hub" in LangChain Hub?**
A: LangChain Hub is a central repository of prompts, chains, and agents. `langchain hub pull` downloads shared components. `langchain hub push` uploads your own. Used for prompt sharing, versioning, and community collaboration. Accessible via `langchain/hub` package.

**Q35: How do you version and manage prompts in LangChain?**
A: Via LangChain Hub: pull prompts by tag/version. In code: pin to specific commit hash. For local management: store prompts as YAML or templates in git. Use `.configurable_alternatives()` to switch between prompt versions at runtime for A/B testing.

## 3. RAG (Retrieval-Augmented Generation) (Q36–Q55)

**Q36: What is the default RAG pattern in LangChain?**
A: The standard RAG chain:
```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)
```
retriever fetches relevant docs, format_docs converts to string, combined with question, fed to LLM.

**Q37: What is a retriever in LangChain and how does it differ from a vector store?**
A: VectorStore: stores and searches vectors (similarity_search, delete, add). Retriever: higher-level abstraction over vector store — implements `get_relevant_documents(query)` and integrates with LCEL. Created via `vectorstore.as_retriever(search_kwargs={"k": 5})`. Retriever is a Runnable; VectorStore is not.

**Q38: Explain the different retrieval strategies in LangChain.**
A: 
- Basic similarity search: k nearest vectors
- MMR (Maximum Marginal Relevance): diversify results
- Similarity score threshold: only return docs above certain score
- Ensemble retriever: combine multiple retrievers with weighting
- Parent document retriever: retrieve smaller chunks, return parent docs
- Multi-query retriever: generate multiple query variants, search each, merge results

**Q39: What is the EnsembleRetriever and when would you use it?**
A: EnsembleRetriever combines results from multiple retrievers (e.g., keyword BM25 + vector similarity) with weighted scoring and reciprocal rank fusion. Use when: no single retrieval method is sufficient, need both lexical and semantic matching, improving recall at cost of some precision.

**Q40: How does LangChain handle document chunking for RAG?**
A: Via TextSplitter classes:
- RecursiveCharacterTextSplitter: splits on separators recursively (most common)
- CharacterTextSplitter: fixed-size character chunks
- TokenTextSplitter: splits by token count (respects LLM token limits)
- SemanticChunker: splits by semantic similarity of sentences
- MarkdownHeaderTextSplitter: splits by markdown structure
- Configure: chunk_size (e.g., 1000 tokens), chunk_overlap (e.g., 200)

**Q41: Explain the concept of "Parent Document Retriever" in LangChain.**
A: 
1. Split documents into small child chunks (for precise retrieval) and larger parent chunks (for context)
2. Embed and index only child chunks
3. On query: retrieve child chunks by similarity
4. Return the parent chunks containing matched children
5. Benefit: precise retrieval with rich context. Implemented via `ParentDocumentRetriever`.

**Q42: What is the MultiQueryRetriever and how does it improve retrieval?**
A: MultiQueryRetriever uses an LLM to generate multiple paraphrased versions of the user's query, runs all through the retriever, deduplicates, and returns the combined results. Improves recall by covering different phrasings. Useful for ambiguous or complex queries.

**Q43: How does contextual compression work in LangChain RAG?**
A: ContextualCompressionRetriever wraps a base retriever and compresses retrieved docs:
- LLMChainExtractor: LLM extracts only relevant parts from each doc
- LLMChainFilter: LLM filters out irrelevant docs entirely
- EmbeddingsFilter: keeps only semantically relevant docs (by threshold)
- Reduces token usage and removes noise from retrieved context

**Q44: What is the SelfQueryRetriever?**
A: SelfQueryRetriever lets the LLM extract both a search term AND metadata filters from a natural language query. For example: "Find articles about AI from 2024" → query="AI", filter=year>=2024. Requires the vector store to support metadata filtering. Useful for structured + semantic search.

**Q45: How do you handle RAG with multiple data sources in LangChain?**
A: 
- MultiRetrievalQAChain: route questions to appropriate retriever based on content
- Using RunnableBranch to route to different RAG chains
- Merge results from multiple retrievers with EnsembleRetriever
- Router retriever: LLM decides which data source to query
- LangChain's MultiSourceRetriever

**Q46: What is the difference between simple RAG and advanced RAG patterns in LangChain?**
A: Simple RAG: embed → retrieve → generate. Advanced RAG adds: query rewriting, multi-step retrieval, re-ranking, contextual compression, Hyde (generate hypothetical doc then search), step-back prompting, iterative retrieval, fusion retrieval (keyword + vector). LangChain supports all via composable runnables.

**Q47: What is Hyde (Hypothetical Document Embeddings) in LangChain?**
A: Hyde: use an LLM to generate a hypothetical ideal document for the query, then embed and search with THAT hypothetical doc instead of the query. The idea: the hypothetical doc is closer to target docs in embedding space than the raw query, improving retrieval quality. Implemented via `HyDEQueryTransform`.

**Q48: How do you implement RAG with conversation history (follow-up questions)?**
A: 
1. Use RunnableWithMessageHistory to maintain conversation
2. Before retrieval, use a "condense question" step: create a standalone query from {history + new question}
3. Retrieve using the standalone query
4. Generate answer with full context + history + retrieved docs
LangChain provides `create_history_aware_retriever` for this pattern.

**Q49: What is the role of Document transformers in LangChain RAG?**
A: Document transformers preprocess retrieved docs before sending to LLM:
- `LongContextReorder`: reorder docs to avoid lost-in-the-middle
- `EmbeddingsClusteringFilter`: cluster and select diverse docs
- `MetaDataTagger`: add metadata to docs
- Compressors: extract/filter relevant content
- Applied via `create_documents_transformer` or as RunnableLambda in chain

**Q50: How does LangChain handle multi-modal RAG (text + images)?**
A: 
- Use multi-modal embeddings (CLIP) to embed both text and images in same vector space
- Store both in vector store with metadata
- Retrieve relevant images + text chunks
- Feed as context to multi-modal LLM (GPT-4V, Gemini)
- LangChain supports via `MultiVectorRetriever` and multi-modal prompt templates

**Q51: Explain the difference between "retrieval" and "reranking" in RAG.**
A: Retrieval: fast, approximate — fetches top-k (e.g., 20) from vector store. Reranking: slower, more accurate — applies cross-encoder to score and reorder the retrieved candidates, selecting the top-n (e.g., 5). This two-stage approach combines speed of ANN with accuracy of cross-encoders. LangChain integrates with CohereRerank, CrossEncoderReranker.

**Q52: How do you evaluate RAG quality in LangChain?**
A: 
- LangSmith evaluation: define evaluators (correctness, faithfulness, relevance, hallucination)
- Use `LangChainStringEvaluator` or custom evaluators
- Metrics: context precision, context recall, answer relevancy, faithfulness
- RAGA (RAG Assessment) library integration
- A/B test with different retrievers/chunking strategies via LangSmith datasets

**Q53: What is a "tool" in the context of RAG agents?**
A: A RAG tool wraps a retrieval chain as a callable tool that an agent can invoke. E.g., `@tool` that runs retriever.get_relevant_documents and returns formatted context. The agent decides when to use RAG vs other tools (calculator, search, etc.). Enables complex multi-step reasoning with retrieval.

**Q54: How does LangChain handle query routing in a multi-RAG system?**
A: 
- RouterChain: LLM chooses which RAG chain to invoke based on query
- RunnableBranch: route by keyword matching
- Semantic routing: embed query, compare to route descriptions
- LangChain's `RouterChain` and `MultiPromptChain` (legacy)
- Modern approach: agent-based routing with tool descriptions

**Q55: What is the "corrective RAG" pattern and how to implement it in LangChain?**
A: Corrective RAG:
1. Retrieve docs
2. LLM evaluates if retrieved docs are relevant (using `LLMChainExtractor` or custom evaluator)
3. If relevant → generate answer
4. If irrelevant → rewrite query and re-retrieve (or use web search fallback)
5. If partially relevant → filter and proceed
Implemented via RunnableBranch with relevance check gate. Self-RAG is a related pattern.

## 4. Agents & Tool Use (Q56–Q75)

**Q56: What is an agent in LangChain and what differentiates it from a chain?**
A: An agent is an LLM that repeatedly decides which action to take (tool call), observes the result, and continues until the task is complete. A chain is a fixed sequence of steps. Agents are dynamic — the path depends on intermediate results. LangChain provides AgentExecutor to run this loop.

**Q57: Explain the ReAct (Reasoning + Acting) agent framework.**
A: ReAct interleaves reasoning traces (thought) with tool calls (action). Pattern:
1. Thought: reason about what to do next
2. Action: call a tool (with input)
3. Observation: tool output
4. Repeat until answer found → Final Answer
LangChain's `create_react_agent` implements this with explicit prompt templates.

**Q58: What are the different agent types in LangChain?**
A: LangChain v0.3+ simplified to:
- `create_react_agent`: ReAct framework with tools
- `create_openai_tools_agent`: for models supporting tool calling (OpenAI, Anthropic, Gemini)
- `create_structured_chat_agent`: structured output for action/observation
- `create_tool_calling_agent`: generic tool calling (recommended)
- `create_xml_agent`: for XML-prompted models (e.g., Claude via Bedrock)
Legacy: zero-shot-react-description, conversational-react-description, etc.

**Q59: What is AgentExecutor and how does it manage the agent loop?**
A: AgentExecutor runs the iterative agent loop:
1. Call LLM with prompt + tools + history
2. Parse response — is it a final answer or tool call?
3. If tool call: execute tool, append tool result to history, loop
4. If final answer: return
5. Configurable: max_iterations, early_stopping_method, handle_parsing_errors
Handles edge cases: invalid tool calls, tool errors, iteration limits.

**Q60: How do you create a custom tool for a LangChain agent?**
A:
```python
@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get current weather for a location."""
    response = requests.get(f"https://api.weather.com/{location}")
    return response.text
```
Key: descriptive name, clear docstring (used as tool description by LLM), typed parameters. For complex tools, subclass BaseTool with custom `_run` and `_arun`.

**Q61: What is the difference between "tool" and "toolkit" in LangChain?**
A: Tool: a single function an agent can call. Toolkit: a collection of related tools (e.g., SQLDatabaseToolkit with list_tables, execute_query, check_query). Toolkits provide cohesive functionality. LangChain has toolkits for: SQL, GitHub, Gmail, FileSystem, JSON, etc.

**Q62: How does LangChain handle tool calling in parallel?**
A: If the LLM returns multiple tool_calls in one response (supported by OpenAI, Gemini, Anthropic), LangChain dispatches them concurrently. The AgentExecutor runs tool executions in parallel, then collects all observations and sends them back to the LLM in a single turn. Improves efficiency for independent sub-tasks.

**Q63: What is "tool message" history and why is it important?**
A: After tool execution, ToolMessage (with tool_call_id) is appended to message history. The LLM uses this history to continue reasoning — it sees what it did and what the result was. Without proper tool message history, the LLM loses context and may repeat actions or produce incorrect final answers.

**Q64: How do you manage agent state across multiple turns?**
A: 
- Messages are accumulated in the agent's message history
- History includes: HumanMessage, AIMessage (with tool_calls), ToolMessage
- RunnableWithMessageHistory persists history per session
- For long-running agents: use summarization to trim history (trim_messages utility)
- LangGraph provides more sophisticated state management for complex agents

**Q65: Explain the concept of "agentic RAG" (RAG agents).**
A: Agentic RAG combines agents with retrieval — the agent decides when and how to retrieve. Instead of fixed RAG pipeline, the agent can: rewrite queries, retrieve multiple times, choose different data sources, combine retrieval with other tools, and reflect on retrieval results before answering. More flexible than naive RAG chains.

**Q66: What is a "multi-agent" system in LangChain?**
A: A system where multiple agents collaborate:
- Router agent: distributes tasks to specialized agents
- Sequential: agents execute in sequence, passing results
- Supervisor: an agent coordinates other agents
- Debate: agents discuss to reach consensus
- Implemented via AgentExecutor + message passing between agents
- LangGraph provides better support for complex multi-agent systems

**Q67: How do you handle tool errors gracefully in agents?**
A: 
- AgentExecutor's handle_parsing_errors=True: catch malformed tool calls
- Tool's `handle_tool_error=True`: sends error message back as observation
- Fallback tools: if primary tool fails, try alternative
- Max retries per tool call
- If tool fails repeatedly, agent should apologize and stop (configure early_stopping_method="force")

**Q68: What is the "stop" sequence in agent prompts?**
A: Agent prompts include stop tokens that signal the LLM to stop generating (e.g., `<|eot_id|>`, `Observation:`). The model generates until it hits the stop token, then LangChain parses the output. For ReAct, `Observation:` is the stop string — the model writes Thought/Action/Action Input, then stops, waiting for the observation.

**Q69: How does LangChain implement function/tool calling for non-OpenAI models?**
A: LangChain normalizes tool calling across providers:
- OpenAI: native function calling
- Anthropic: tool use API
- Google: function declaration
- Ollama/Llama.cpp: tool calling via chat templates
- For models without native support: prompt-based tool calling with structured parsing
- `bind_tools()` abstracts this — LangChain handles the conversion per provider

**Q70: What is the difference between `create_react_agent` and `create_tool_calling_agent`?**
A: 
- create_react_agent: uses ReAct prompt format (Thought/Action/Action Input/Observation). Works with ANY LLM (including non-tool-calling). Parses text output for tool calls.
- create_tool_calling_agent: uses model's native tool calling API. Only for models that support function calling. More reliable, supports parallel tool calls.
- Recommendation: use create_tool_calling_agent when possible; fall back to ReAct for other models.

**Q71: How do you limit agent execution time or iterations?**
A: AgentExecutor config:
- `max_iterations`: max thought-action cycles (default 15)
- `max_execution_time`: wall-clock time limit
- `early_stopping_method`: "force" (return partial) or "generate" (ask LLM for final answer)
- Tool timeout: per-tool execution timeout
- Without limits, agents can loop infinitely or cost excessive tokens.

**Q72: What is a "stoppable agent" pattern?**
A: An agent that can be interrupted mid-execution. Implemented via:
- `astream_events()` for frontend cancellation
- Checkpointing agent state for resumability
- Human-in-the-loop approval gates (LangGraph)
- Python's asyncio cancellation with async agent execution
- Useful when an agent requires user confirmation before proceeding

**Q73: How do you share state between agents in a multi-agent system?**
A: 
- Shared memory: agents write to a common message store
- Agent communication: agents send messages to each other (human-like)
- Shared tool access: tools that write to a shared database
- LangGraph: shared StateGraph with typed state that all nodes (agents) read/write
- Best practice: define a schema for inter-agent messages and shared state

**Q74: What is a "conversational agent" and how is it different from a standard agent?**
A: Conversational agent maintains dialogue history and uses memory to answer follow-up questions. Differs from standard agent by:
- Using ChatPromptTemplate with MessagesPlaceholder for history
- RunnableWithMessageHistory for persistence
- A "condense" step to extract standalone queries from multi-turn context
- Personality/system prompt awareness across turns
- `create_react_agent` with chat history support

**Q75: How do you test and evaluate agents in LangChain?**
A: 
- LangSmith evaluation: run agent against test datasets, measure success rate
- Unit test individual tools
- Simulate tool responses for deterministic testing
- Evaluate: task completion rate, steps taken, token efficiency, hallucination rate
- LangSmith's `aevaluate` for LLM-as-judge evaluation
- Regression testing with known edge cases

## 5. Memory, Documents & Data Handling (Q76–Q90)

**Q76: What are the different memory types in LangChain?**
A: 
- ConversationBufferMemory: stores all messages verbatim
- ConversationBufferWindowMemory: keeps last k turns
- ConversationSummaryMemory: summarizes old messages
- ConversationTokenBufferMemory: truncates by token count
- VectorStoreRetrieverMemory: retrieves relevant history by similarity
- ZepMemory, RedisChatMessageHistory: production backends
- RunnableWithMessageHistory is the current recommended approach

**Q77: How does ConversationSummaryMemory work and when is it useful?**
A: It maintains a running summary of the conversation. At each turn, the LLM updates the summary with new context. On query, the summary + recent messages are injected. Useful for long conversations where full history exceeds context window. More token-efficient than buffer but loses detail.

**Q78: What is the role of Document objects in LangChain?**
A: Document is the core unit for unstructured data: `Document(page_content="...", metadata={"source": "...", "page": 1})`. Used throughout indexing and retrieval. Documents flow from: loaders → splitters → embedding → vector store → retriever → chain. Metadata enables filtering and provenance tracking.

**Q79: How does LangChain integrate with document loaders?**
A: Document loaders load from various sources:
- PDF: PyPDFLoader, PDFMinerLoader
- Web: WebBaseLoader, SitemapLoader, AsyncHtmlLoader
- Database: SQLLoader, MongoDBLoader
- Code: PythonLoader, TextLoader
- Cloud: S3FileLoader, GCSFileLoader
- Each implements `load()` → List[Document] or `alazy_load()` for streaming

**Q80: What is the difference between lazy_load and load in document loaders?**
A: `load()` loads all documents into memory at once — simple but can OOM for large datasets. `lazy_load()` returns an iterator — documents are loaded on-demand, processing as you iterate. Use `lazy_load()` with `RecursiveCharacterTextSplitter` to pipeline large-scale ingestion.

**Q81: How do you process large-scale document ingestion in LangChain?**
A: 
1. Use lazy loaders + streaming splitters
2. Batch embeddings (avoid OOM on GPU/API)
3. Use vector store's `add_documents` with batching
4. Use LangChain's `index` API for incremental indexing (avoid re-indexing unchanged docs)
5. Consider parallel processing with RunnableParallel or multiprocessing
6. Monitor API rate limits with `with_retry`

**Q82: Explain the LangChain "index" API for document management.**
A: `langchain.indexes.VectorStoreIndexWrap` maps documents to vector stores with id tracking:
- Tracks document hashes
- Only embeds changes (new/modified docs)
- Deletes stale documents
- Prevents duplicate vectors
- Essential for production RAG document pipelines

**Q83: What is the SQLRecordManager in LangChain?**
A: SQLRecordManager tracks document writes in a SQLite/Postgres database. Used with the Indexing API to record which documents have been written. On re-index: compares current docs vs records, only processes differences. Supports clean/upsert modes. Records document ID + source hash + write timestamp.

**Q84: How does LangChain handle document deduplication?**
A: 
- Via the Indexing API with `VectorStoreIndexWrap(record_manager, ...)`
- Document hashing: content hash determines uniqueness
- Cleanup modes: incremental (delete removed docs), full (rebuild)
- Custom dedup: compare metadata / content before adding
- For vector dedup: search for near-duplicates before inserting

**Q85: What are the different embedding model integrations in LangChain?**
A: LangChain provides `Embeddings` interface for: OpenAI, Anthropic, Cohere, HuggingFace (sentence-transformers), Ollama (nomic-embed-text, mxbai-embed), Google VertexAI, AWS Bedrock, Together AI, Mistral AI, Jina AI, and local models via HuggingFaceEmbeddings.

**Q86: How do you switch between embedding models without re-indexing?**
A: You CANNOT — changing the embedding model changes the vector space, making old vectors incompatible. To migrate: create a new collection with new embeddings, re-index all documents, then swap the collection pointer. Some apps run dual embedding during migration.

**Q87: What is the CacheBackedEmbeddings and when should you use it?**
A: CacheBackedEmbeddings wraps an Embeddings instance with a cache (disk/Redis). First time a text is embedded: compute and cache. Subsequent identical texts: return cached vector. Reduces API costs and latency for repeated texts. Useful for ingesting data with duplicate chunks or queries.

**Q88: How does LangChain handle token counting and cost estimation?**
A: 
- `get_openai_callback()` context manager: tracks tokens used, cost
- `OpenAICallbackHandler`: callback for token tracking
- Token counting via tiktoken for OpenAI models
- For other models: approximate via model-specific tokenizers
- Integrates with LangSmith for cost tracking across runs

**Q89: What is the difference between batch and async ingestion in LangChain?**
A: Batch ingestion (`vectorstore.add_documents(docs)`) processes documents sequentially or in parallel threads. Async ingestion (`await vectorstore.aadd_documents(docs)`) uses asyncio — better for I/O-bound workloads (API-based embeddings). For large datasets: use `batch_size` parameter to control concurrency and rate limiting.

**Q90: How do you handle streaming with document loading and splitting in LangChain?**
A: Use lazy loaders with streaming splitters:
```python
loader = WebBaseLoader(urls)
splitters = RecursiveCharacterTextSplitter(chunk_size=1000)
for doc in loader.lazy_load():
    for chunk in splitter.split_text(doc.page_content):
        process(chunk)
```
This avoids loading entire dataset into memory. Combine with async for concurrent processing.

## 6. Advanced Topics, Production & Ecosystem (Q91–Q100)

**Q91: How do you deploy a LangChain application to production?**
A: 
1. LangServe: deploy chain as FastAPI endpoint
2. Dockerize the application
3. Use LangSmith for monitoring
4. Implement caching (Redis for LLM responses, embedding cache)
5. Rate limiting with middleware
6. Horizontal scaling behind a load balancer
7. A/B test chain configurations with `.configurable_alternatives()`
8. Monitor: latency, token usage, error rate, user feedback

**Q92: How does LangChain handle rate limiting with LLM providers?**
A: 
- `with_retry()`: exponential backoff + jitter
- Custom rate limiter middleware via callbacks
- `max_concurrency` in RunnableConfig for batch calls
- Token bucket or sliding window rate limiter
- Async for non-blocking I/O
- Queue-based processing with controlled throughput

**Q93: What is the role of "filters" in LangChain retrievers?**
A: Filters restrict retrieval by document metadata: `vectorstore.as_retriever(search_kwargs={"filter": {"year": 2024}})`. Supported by most vector stores. Enables: date range filtering, category filtering, source filtering, access control. Different vector stores have different filter syntaxes — LangChain normalizes via `RunnableLambda`.

**Q94: How does LangChain handle PII (Personally Identifiable Information) in chains?**
A: 
- Presidio integration for PII detection and redaction
- `PresidioReversibleAnonymizer`: anonymizes PII before LLM, de-anonymizes response
- Custom callbacks to scan inputs/outputs
- LangChain's `OpenAIModerationChain` for content filtering
- Best practice: detect + redact before any external API call

**Q95: What is the difference between LangChain and LlamaIndex?**
A: LangChain: broader framework — chains, agents, tools, memory, ecosystem integrations. LlamaIndex: specialized for data indexing and retrieval (RAG). LangChain is better for complex agent workflows; LlamaIndex is better for advanced data ingestion and retrieval. They complement each other — many production apps use both.

**Q96: How does LangChain handle Structured Output vs JSON mode?**
A: Two approaches:
1. Bind model to a Pydantic schema: `model.with_structured_output(SchemaClass)` — uses model's native structured output (tool calling internally)
2. PydanticOutputParser: instruct the LLM via prompt to output JSON, then parse it
3. JsonOutputParser: simpler JSON parsing
4. with_structured_output is preferred — more reliable, avoids prompt injection issues

**Q97: What is the "RunnableGenerator" pattern?**
A: RunnableGenerator yields multiple outputs from a single input — like a generator function wrapped as a Runnable. Used for: stream processing, map operations, incremental processing. Example: yield chunks of a transformed document. Less common than RunnableLambda for most use cases.

**Q98: How do you handle user feedback in LangChain RAG systems?**
A: 
- Collect: thumbs up/down, explicit ratings, implicit signals (clicks, dwell time)
- Store feedback in LangSmith: `runs.feedback.create()` linked to trace run_id
- Use feedback to: fine-tune reranker, adjust chunking strategy, improve prompt
- Active learning: low-confidence queries → human label → improve retrieval
- LangSmith datasets for continuous evaluation

**Q99: What are the major breaking changes in LangChain v0.3?**
A: 
- Legacy chains (LLMChain, SimpleSequentialChain) removed
- LangChain community packages separated (langchain-community)
- Standardized on ChatModels over LLM abstractions
- LCEL as the only recommended composition method
- Agent types simplified to tool-calling
- Model I/O streamlined with BaseMessage
- Import paths reorganized

**Q100: What emerging patterns are shaping LangChain development in 2026?**
A: 
1. Agent-native apps: LangGraph + LangChain as the standard stack
2. Streaming-first UX: every component supports streaming
3. Multi-modal chains (vision, audio, text combined)
4. Evaluation-driven development: LangSmith + CI for LLM pipelines
5. On-device LangChain (Ollama, MLX, llama.cpp integration)
6. Agent observability: fine-grained tracing and debugging
7. Caching-first architecture for cost efficiency
8. Declarative agent workflows via LangGraph state machines
