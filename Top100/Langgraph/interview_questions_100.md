# LangGraph — 100 Interview Q&A
> Based on production agent orchestration, state machines, multi-agent systems, and human-in-the-loop workflows using LangGraph v0.2+.

---

## 1. Core Concepts & Architecture (Q1–Q20)

**Q1: What is LangGraph and how does it differ from LangChain?**
A: LangGraph is a framework for building stateful, multi-actor agent applications as graphs. LangChain is for linear chain composition; LangGraph enables cycles, branching, state persistence, human-in-the-loop, and complex agent orchestration. LangGraph treats agent workflows as state machines — nodes perform computation, edges control flow, and state persists across steps.

**Q2: Explain the core primitives of LangGraph: StateGraph, Node, Edge, and State.**
A: 
- StateGraph: the graph definition, parameterized by a State type
- State: a TypedDict or Pydantic model defining the schema for data passed between nodes
- Node: a function (or Runnable) that takes State and returns partial State updates
- Edge: defines flow between nodes — can be conditional (function-based routing) or normal (always go to next node)
- The graph is compiled into a Runnable with checkpointing, streaming, and human-in-the-loop support

**Q3: What is the difference between StateGraph and MessageGraph?**
A: MessageGraph (deprecated in newer versions) was a simplified graph that assumed state is a list of messages. StateGraph is the general version — you define your own state schema (TypedDict). StateGraph is more flexible; MessageGraph was convenient for chat. Current recommendation: always use StateGraph with explicit state schema.

**Q4: How do you define state in LangGraph?**
A: State is a TypedDict (or Pydantic BaseModel) annotated with `add_messages`, `operator.add`, or custom reducers:
```python
from typing import Annotated, TypedDict
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str
    input: str
    intermediate_steps: list
```
Reducers (like `add_messages`) handle how state is merged from multiple nodes — append, replace, or custom logic.

**Q5: What is a "reducer" in LangGraph state?**
A: A reducer defines how state keys are updated when multiple nodes write to the same key. Default: last write wins. `add_messages`: appends new messages to the list. `operator.add`: merges lists. Custom reducers: any function (old_value, new_value) → merged_value. Reducers are critical for node parallelism — without them, parallel node updates to the same key would conflict.

**Q6: What is a "node" in LangGraph and what can it do?**
A: A node is a function that processes state and returns updates. Signature: `NodeFunction(state: State) -> dict`. Nodes can: call LLMs, execute tools, run subgraphs, invoke RAG, perform business logic. Nodes are added to the graph via `graph.add_node("node_name", node_function)`. They receive the full state and return a partial state update (dict).

**Q7: Explain the difference between "normal edges" and "conditional edges".**
A: Normal edges (`graph.add_edge("node_a", "node_b")`): always go from A to B. Conditional edges (`graph.add_conditional_edges("node_a", router_fn, {True: "node_b", False: "node_c"})`): the router function decides which node to go to next based on state. Conditional edges are the primary mechanism for branching, looping, and routing in LangGraph.

**Q8: What is the "entry point" and "finish point" of a LangGraph graph?**
A: Entry point: the first node executed when the graph starts — set via `graph.set_entry_point("node_name")` or `graph.set_conditional_entry_point(router_fn)`. Finish point: when the graph reaches a node that is set as the finish point (`graph.set_finish_point("node_name")`), or when a special `END` edge is reached — `graph.add_edge("node_name", END)`. Multiple finish points are allowed.

**Q9: What does "compiling" a graph do?**
A: `graph.compile()` transforms the graph definition into a runnable object (a Runnable). During compilation, LangGraph: validates the graph structure (no orphan nodes), checks for cycles, prepares checkpointing, and creates the execution engine. The compiled graph supports `invoke`, `ainvoke`, `stream`, `astream`, and event streaming.

**Q10: What is a "checkpointer" in LangGraph?**
A: A checkpointer saves the state of the graph at each step (superstep). Enables: pause/resume, human-in-the-loop (interrupt and wait for input), error recovery (restart from checkpoint), replay, and time travel debugging. Checkpointer backends: MemorySaver (in-memory, dev), SqliteSaver, PostgresSaver, and custom implementations.

**Q11: How does LangGraph handle graph execution — synchronous vs async?**
A: Compiled graph is a Runnable — supports both sync (`invoke`, `stream`) and async (`ainvoke`, `astream`, `astream_events`). Nodes can be sync or async functions. If any node is async, invoke the graph asynchronously. LangGraph handles the concurrency model automatically — you don't need to manage event loops.

**Q12: What is a "superstep" in LangGraph execution?**
A: A superstep is one iteration of the node execution loop. In each superstep, all nodes that have incoming edges from the current set of completed nodes execute in parallel (fan-out). After all parallel nodes complete, state is merged via reducers, and the next superstep begins. Supersteps enable parallel agent execution.

**Q13: How does LangGraph enable cyclic graphs (loops)?**
A: Unlike LangChain (which is a DAG), LangGraph supports cycles by design. A cycle is created by adding a conditional edge that routes back to a previous node. Without cycles, you can't have agent loops (thought → action → observation → thought). The recursive limit (`recursion_limit` in config) prevents infinite loops.

**Q14: Explain the concept of "interrupt" in LangGraph.**
A: Interrupts pause graph execution at a specific node, persist the state, and wait for external input. Used for human-in-the-loop: the agent asks for approval, waits for human response, then continues. Implemented via `NodeInterrupt` exception or `graph.interrupt()` function. The checkpoint stores the state; resume by invoking with `Command(resume="user input")`.

**Q15: What is Command in LangGraph?**
A: Command is a special return type from nodes that allows a node to: 1) update state AND 2) control the next edge (override the graph's edge definition). `Command(goto="next_node", update={"key": "value"})`. Useful for dynamic routing decisions directly from node logic. Available in LangGraph v0.2+.

**Q16: How does LangGraph handle "fan-out" (parallel execution)?**
A: When multiple nodes are all reachable from the current node (via normal edges or different conditional branches), they execute in parallel in the same superstep. Each gets the current state. Writes are merged via reducers after all complete. For map operations: use `Send()` API to fan-out to the same node with different arguments.

**Q17: What is the Send() API in LangGraph?**
A: Send() allows dynamic fan-out to the SAME node with different arguments:
```python
def router(state):
    return [Send("process_item", {"item": item}) for item in state["items"]]
```
Each Send creates a separate execution branch with the given state subset. Results are merged via reducers. Used for map-reduce patterns, parallel tool execution, batch processing.

**Q18: How does streaming work in LangGraph?**
A: Compiled graph supports multiple streaming modes:
- `stream()`: yields state updates per superstep
- `astream_events()`: yields fine-grained events (node start/end, LLM token streaming, tool calls)
- Event types: on_chain_start, on_chat_model_stream, on_tool_end, etc.
- Use `astream_events` with `version="v2"` for production-grade streaming to frontends

**Q19: What are "subgraphs" in LangGraph and why use them?**
A: Subgraphs are StateGraph instances used as nodes in a parent graph. Benefits:
- Encapsulation: complex logic isolated in a subgraph
- Reusability: same subgraph used in multiple parent graphs
- Hierarchical state: subgraph has its own state, can communicate with parent
- Testing: subgraphs tested independently
- Example: a "research" subgraph that searches, reads, and summarizes

**Q20: Explain the difference between LangGraph and other agent frameworks (AutoGen, CrewAI).**
A: LangGraph: graph-based, fine-grained state control, human-in-the-loop, checkpointing, LangChain ecosystem integration. AutoGen: conversation-based, agent chat, Microsoft ecosystem. CrewAI: role-based agents, simpler API, less state control. LangGraph is best for: complex stateful workflows, production-grade reliability, custom agent architectures.

## 2. State Management & Persistence (Q21–Q35)

**Q21: How do you persist graph state across sessions in LangGraph?**
A: Via checkpointer:
```python
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
graph = builder.compile(checkpointer=checkpointer)
```
Now every invocation saves state. Resume by passing the same `thread_id` in config. Supported: SqliteSaver, PostgresSaver, MemorySaver. For production: PostgresSaver (durable, concurrent).

**Q22: What is a "thread_id" in LangGraph and how is it used?**
A: thread_id uniquely identifies a conversation/execution session. Passed in config:
```python
config = {"configurable": {"thread_id": "user-123-conversation-1"}}
```
State is persisted per thread_id. To resume: invoke with the same thread_id. To start fresh: use a new thread_id. Enables multi-tenant persistence.

**Q23: How does LangGraph handle concurrent access to the same thread?**
A: Checkpointers can be configured to lock threads. PostgresSaver supports advisory locks. Without locking, concurrent writes to the same thread could corrupt state. Best practice: one thread per user session, avoid concurrent writes. Queue requests per thread_id.

**Q24: What is the difference between "state" and "config" in LangGraph?**
A: State: data passed between nodes (messages, intermediate results, business data). Persisted by checkpointer. Config: runtime parameters (thread_id, recursion_limit, metadata, callbacks). NOT persisted. Config controls execution but isn't part of the graph's state schema.

**Q25: How do you implement "time travel" (rewind/replay) in LangGraph?**
A: Checkpointer stores every state. To time travel:
1. `graph.get_state_history(config)`: list all checkpoints
2. Select a checkpoint's `parent_config`
3. `graph.invoke(None, parent_config)`: replay from that point
4. Continue with new input — creates a fork
Used for: debugging, undo, scenario exploration.

**Q26: What is the "state update" mechanism when a node returns None?**
A: If a node returns `None` (or nothing), no state update occurs for that superstep. The state passes through unchanged. This is valid — used for nodes that only have side effects (logging, monitoring, sending events) or nodes that read state without modifying it.

**Q27: How do you handle large state objects (e.g., thousands of messages)?**
A: 
- Summarize: compress old messages into a summary (LangGraph's `add_messages` doesn't automatically summarize)
- Trim: use `RemoveMessage` to drop old messages
- External storage: store large data outside state (file paths, DB references)
- Lazy loading: load data on demand in nodes rather than storing in state
- Use Pydantic models with validators to control state size

**Q28: What is the "private state" concept in LangGraph?**
A: Private state is state local to a subgraph — not visible to the parent graph. Each subgraph has its own state schema. Communication with parent: parent updates are passed via inputs; results are returned as outputs. Encapsulation prevents state pollution between components.

**Q29: How do you merge state from parallel branches correctly?**
A: Reducers define merge behavior:
- Messages: `add_messages` appends chronologically by timestamp
- Lists: `operator.add` concatenates
- Dicts: keys from both branches merge (last write per key)
- Custom reducers: implement your own merge logic
- Branch-specific keys: each branch writes to different state keys to avoid conflict

**Q30: What happens when two parallel nodes write to the same state key without a reducer?**
A: Default behavior: last write wins (overwrite). Since parallel execution is concurrent, the final value is non-deterministic (race condition). Always use a reducer (add_messages, operator.add, custom) for keys written by multiple parallel nodes.

**Q31: How does LangGraph handle state serialization for checkpointing?**
A: State is serialized via the checkpointer's serialization format. Default: JSON serialization (for TypedDicts). For Pydantic models: uses model_dump_json. Custom serializers can be provided. Messages are serialized using LangChain's BaseMessage serialization. Binary/opaque data is not supported — serialize to string first.

**Q32: What is the "recursion limit" and how does it affect state?**
A: recursion_limit caps total supersteps (default 25). When hit: raises `GraphRecursionError`. State is preserved in the checkpoint. Protects against infinite loops and runaway token costs. Increase for complex agent workflows: `config["recursion_limit"] = 100`. Monitor actual superstep count in production.

**Q33: How do you implement transactional state updates?**
A: LangGraph checkpoints are atomic per superstep. If a node fails: the state is rolled back to the last checkpoint (not to the current superstep's partial state). For multi-node transactions: group related state updates in the same node, or use a dedicated "commit" node at the end.

**Q34: What is the difference between "astream" and "astream_events"?**
A: `astream`: yields state updates (the full state after each superstep). Coarse-grained. `astream_events`: yields individual events (LLM token, node start/end, tool call/result). Fine-grained. For frontend streaming (typing indicators, token-by-token output): use `astream_events` with `version="v2"`. For backend monitoring: use `astream`.

**Q35: How do you reset or clear state for a thread?**
A: No built-in reset. To clear:
- Delete checkpoint: `checkpointer.put(thread_id, None)` — checkpointer-specific
- Start new thread: use a new thread_id
- For explicit reset: implement a "reset" node that clears state keys and routes to start
- PostgresSaver: `DELETE FROM checkpoints WHERE thread_id = ?`

## 3. Agent Patterns & Orchestration (Q36–Q60)

**Q36: What is the standard "ReAct agent" pattern in LangGraph?**
A: The ReAct agent as a graph:
- Nodes: `call_model` (LLM with tools), `call_tool` (execute tool)
- Edges: conditional — if model returns tool_calls → call_tool → call_model (loop); if final answer → END
- State: messages list (system prompt, human, AI responses, tool results)
- This creates the thought-action-observation loop naturally via graph cycles

**Q37: How do you implement a "supervisor agent" in LangGraph?**
A: Supervisor agent delegates tasks to specialized sub-agents:
- Supervisor node: receives task, decides which agent to route to
- Sub-agent nodes: each is a subgraph (or node) handling a domain
- Supervisor re-invoked after each sub-agent: decide if done or need more
- State includes: task, history of sub-agent outputs, final answer
- Conditional edge from supervisor routes to sub-agents or END

**Q38: Explain the "hierarchical agent" pattern.**
A: A top-level agent (supervisor) manages mid-level agents that manage low-level agents. Each level has its own state. Benefits: delegation, specialization, scope control. Implemented via nested subgraphs. Example: CEO agent → Manager agents (Research, Coding, Review) → Worker agents (Search, Write, Execute, Lint).

**Q39: How do you implement "human-in-the-loop" in LangGraph?**
A: 
1. Add a node that raises `NodeInterrupt` or returns `Command(resume="awaiting_approval")`
2. Checkpointer saves state at that point
3. Frontend detects interrupt via `astream_events`
4. Human provides input (approve, modify, reject)
5. Resume with `graph.invoke(Command(resume="approved"), config_with_same_thread_id)`
6. Graph continues from the interrupt point with human input

**Q40: What is a "dynamic agent" pattern?**
A: A graph where agents (nodes) are created dynamically at runtime. Example:
- A "planner" node generates a plan (list of steps)
- Each step is executed by dynamically created nodes via Send()
- Results are merged and sent to a "summarizer" node
- The number and type of agents aren't known at graph definition time

**Q41: How do you implement a "reflection" pattern in LangGraph?**
A: Reflection: the agent generates an output, then critiques it, then improves it.
- Nodes: `generator`, `critic`, `improver`
- Conditional edge: if critic approves → END; if not → improver → generator
- State includes: current draft, critique history, iteration count
- Self-reflection loop improves output quality at cost of multiple LLM calls

**Q42: Explain the "tool-calling agent" implementation in LangGraph.**
A: 
State: messages (with tool messages)
Nodes:
- `call_model`: bind tools, invoke LLM, append AI message to state
- `execute_tools`: for each tool_call in AI message, execute tool, append ToolMessage
Edges: 
- After call_model: if tool_calls exist → execute_tools
- After execute_tools: → call_model (loop)
- If no tool_calls → END
This handles parallel tool calls, tool errors, and multi-turn tool use.

**Q43: How do you implement a "plan-and-execute" agent pattern?**
A: 
1. Planner node: LLM generates a multi-step plan from the user query
2. Executor node: executes steps sequentially (sends each step to a sub-agent)
3. Tracker node: checks plan status, marks completed steps
4. Updater node: adjusts plan based on execution results
5. Loop until all steps complete
State: plan (list of steps), completed_steps, results, current_step_index

**Q44: What is the "multi-agent debate" pattern?**
A: Multiple agents with different perspectives debate a topic:
- One agent per perspective (e.g., pro, con, neutral)
- Each agent reads the debate history and responds
- Loop for N rounds
- Final judge agent synthesizes conclusion
- State: debate_rounds, agent_responses[pro], agent_responses[con], etc.

**Q45: How do you handle tool errors in a LangGraph agent?**
A: 
- Tool node catches exceptions and returns ToolMessage with error content
- LLM receives the error as observation — can retry with different args or apologize
- `handle_tool_error=True` in tool decorator automatically formats errors
- Max retry logic in the graph: track tool_failures in state; if > threshold → escalate or END
- Node-level try/except for non-transient failures

**Q46: What is the "agent supervisor" pattern and how do agents communicate?**
A: Supervisor receives all agent outputs and decides the next action. Agent communication:
- All agents share the same message list (via state)
- Supervisor reads all messages and responds
- OR each agent has its own state channel, supervisor composes
- Use `add_messages` reducer so all messages are visible in chronological order

**Q47: How do you implement timeout for individual agent steps?**
A: 
- Tool-level timeout: pass timeout to tool execution function
- Node-level timeout: wrap node logic with `asyncio.wait_for`
- Graph-level timeout: `config["recursion_limit"]` + wall clock tracking in state
- Use `astream_events` with asyncio.timeout on the frontend
- Fallback: if a node times out, route to a timeout handler node

**Q48: How do you implement a "guardrails" agent that validates outputs?**
A: 
1. After main agent generates output, route to guardrails node
2. Guardrails node: validates output against rules (PII, toxicity, factual correctness, format)
3. If passes → END (or deliver to user)
4. If fails → route back to agent with feedback, or route to fallback response
State: guardrails_result, validation_errors, correction_attempts

**Q49: What is the "orchestrator-worker" pattern in LangGraph?**
A: 
1. Orchestrator node: analyzes task, creates a plan with subtasks
2. Send() fan-out to Worker nodes, each with a subtask
3. Workers execute in parallel (each is a subgraph or node)
4. Aggregator node: collects all worker results, merges, produces final output
State: plan, subtasks, worker_results (list), final_output
Benefits: parallelism, specialized workers, clean separation of concerns.

**Q50: How do you implement a "router" agent that categorizes queries?**
A: 
1. Router node: LLM classifies query into categories (tech support, sales, billing)
2. Conditional edge: routes to the appropriate handler agent based on category
3. Each handler agent is a subgraph specialized for that domain
4. A default handler for unclassified queries
State: query, category, confidence_score

**Q51: How do you handle agent handoff in LangGraph?**
A: Agent handoff: one agent pauses while another executes. Implemented via:
- Subgraphs: agent A is a subgraph; after it completes, agent B starts
- Supervisor pattern: supervisor decides when to switch agents
- Tool-based handoff: agent A calls a "transfer_to_agent_B" tool that updates state and routes to agent B node
- The state carries context across the handoff

**Q52: What is the "retry with backoff" pattern for agent tools?**
A: 
```python
@tool(handle_tool_error=True)
def fragile_api(input: str) -> str:
    try:
        return call_api_with_retry(input, max_retries=3, backoff=2.0)
    except Exception as e:
        return f"Error after retries: {str(e)}"
```
In graph: track `tool_failures` in state. If a tool fails repeatedly, the LLM should try a different approach or ask for help.

**Q53: How do you implement a "conversational" agent with memory in LangGraph?**
A: 
- State includes messages list with add_messages reducer
- System prompt node: injects system message at start (if new thread) or maintains chat style
- Conversation loop: user input → LLM → tool calls → LLM → response
- RunnableWithMessageHistory NOT needed — LangGraph handles history via checkpointer
- Trim messages when exceeding context window using RemoveMessage

**Q54: What is "agent observability" in LangGraph?**
A: Tracking agent behavior:
- LangSmith tracing: each superstep is a trace with inputs/outputs
- `astream_events`: real-time visibility into agent decisions
- State inspection: read any checkpoint's state to understand agent state
- Metrics: steps taken, tools called, tokens consumed, latency per node
- Debugging: time travel to replay any checkpoint

**Q55: How do you limit agent context window (e.g., for long conversations)?**
A: 
- Trim messages: use `trim_messages` utility to keep last N messages + summary
- Summarize: call LLM to compress old messages into a summary
- RemoveMessage: mark messages for deletion from state
- Done in a "preprocessing" node before call_model
- Example: keep system + summary + last 20 messages

**Q56: What is the "map-reduce" pattern in LangGraph?**
A: 
1. Map: use Send() to fan-out to a processing node with different inputs
2. Process: each branch executes independently, returns partial results
3. Reduce: after all Send branches complete, a reduction node merges results
4. State: results list populated by parallel branches
Used for: summarizing multiple documents, parallel research, batch code review.

**Q57: How do you implement a "quality gate" before final output?**
A: 
1. After generation, add a "quality_check" node
2. Node evaluates: completeness, correctness, safety, format compliance
3. Conditional edge: if quality passes → output; if fails → regenerate or route to human review
4. Track quality metrics in state for monitoring
Enables self-improving agents that catch their own mistakes.

**Q58: What is the "sticky agent" pattern (stay with same agent until done)?**
A: Once a specialized agent starts handling a task, keep routing to it until it signals completion. Implemented via:
- Agent node sets a `current_handler` key in state
- Router conditional edge: if current_handler is set, route to it
- Agent clears current_handler when done → router re-evaluates
Prevents thrashing between agents.

**Q59: How do you handle context injection (documents, user profile) in agent state?**
A: 
- Initial state: populate with user profile, retrieved documents, prior conversation
- "context_injection" node: runs before the first agent to fetch and inject context
- Dynamic injection: agents can call RAG tools to fetch context as needed
- State stores: context_documents, user_info, session_data
- For large context: store references (doc IDs) not full content

**Q60: What is the "bounded agent" pattern?**
A: An agent constrained to a specific scope:
- Its state only contains variables relevant to its domain
- Its tools are limited to that domain
- Its system prompt defines boundaries (what it can/cannot do)
- A supervisor agent routes only appropriate tasks to it
Prevents agents from exceeding their authority or hallucinating about unrelated topics.

## 4. Human-in-the-Loop & Interaction (Q61–Q75)

**Q61: How does `interrupt` work in detail in LangGraph?**
A: The graph encounters `NodeInterrupt` (raised by node or from `Command(interrupt="...")`). The checkpointer persists the current state. The graph pauses execution and returns control to the caller. The checkpoint contains the full state + interrupt metadata. Resuming: call `invoke` with `Command(resume=value)` — the interrupted node receives `resume` as `state["resume"]`.

**Q62: What is the "approval gate" pattern for human-in-the-loop?**
A: 
1. Agent generates a plan or action
2. "approval_request" node: sets state with proposed action, raises interrupt
3. Human views proposed action (via frontend)
4. Human approves: resume with `Command(resume="approved")` → node proceeds
5. Human rejects: resume with `Command(resume="rejected")` → node routes to revision or abort
6. Human modifies: resume with modified action as the value

**Q63: How do you design a frontend that communicates with LangGraph?**
A: 
- Backend: LangGraph server (LangServe or custom FastAPI) wrapping the compiled graph
- Endpoints: `POST /invoke` (start/resume), `POST /stream` (SSE streaming)
- Frontend (React/Next.js): EventSource or fetch for SSE, display token stream
- On interrupt: frontend detects via event, shows approval UI, sends user response as resume command
- LangGraph SDK provides JS/TS client libraries

**Q64: How do you handle partial human input in the middle of agent execution?**
A: 
1. Agent pauses at interrupt with a question/state
2. Human provides answer, correction, or additional context
3. Agent continues with the human input incorporated
4. The human input is passed via `Command(resume=...)` and stored in state
Useful for: disambiguation, clarifying questions, data correction, permission grants.

**Q65: What is the "dynamic interrupt" pattern?**
A: The agent decides WHEN to ask for human input (not a fixed interrupt point). Implemented via:
- After tool execution, LLM decides if it needs human input (confidence low, ambiguous result)
- If yes: sets a flag in state → routes to "interrupt_node" → human input
- If no: continues autonomously
More natural UX — agent only bothers human when necessary.

**Q66: How do you implement approval for sensitive tool calls (e.g., sending emails)?**
A: 
1. Before the "send_email" tool, add a "review_action" node
2. Review node: copies the action details to a "pending_approval" state key
3. Interrupt: pause for human approval
4. If approved: proceed to send_email node
5. If rejected: route to "cancel_action" node
6. State tracks pending actions and their approval status

**Q67: How do you communicate interrupt state to the frontend?**
A: `astream_events` yields `on_custom_event` for interrupts:
```python
async for event in graph.astream_events(input, version="v2"):
    if event["event"] == "on_custom_event" and event["name"] == "interrupt":
        # send interrupt data to frontend
        yield event["data"]
```
Frontend receives the interrupt, displays the prompt, collects user input, and sends resume command.

**Q68: What is the "email a human" fallback pattern?**
A: When the agent cannot resolve an issue, it:
1. Drafts an email to a human expert with context + proposed approach
2. Stores the email in state
3. Interrupts or continues (async email send)
4. A human expert reviews, responds via email/custom tool
5. Agent picks up the response and continues
State: escalation_request, human_response

**Q69: How do you resume a graph from a different process/machine?**
A: Since checkpoints are persisted in a database (PostgresSaver), you can resume from any process that can access the DB:
```python
checkpointer = PostgresSaver.from_conn_string("postgresql://...")
graph = builder.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "existing_thread"}}
# This resumes from the last checkpoint
result = graph.invoke(None, config)
```
Enables: serverless agents (pause → resume on new instance), distributed execution.

**Q70: What is the "timeout for human response" pattern?**
A: After interrupt:
1. Start a timer (via asyncio or external scheduler)
2. If human responds before timeout → resume normally
3. If timeout → automatically resume with a default/fallback action
4. State includes: interrupt_timestamp, timeout_duration
Implementation: wrap the graph invoke with asyncio.wait_for, or use a scheduler to auto-resume.

**Q71: How do you handle multiple human inputs during a single graph run?**
A: Multiple interrupts can occur in one run. Each interrupt is a separate pause. After each resume, the graph continues until the next interrupt or END. State tracks the interrupt history. Example: agent asks for clarification, then later asks for approval — both are separate interrupt/resume cycles.

**Q72: What is the "human takeover" pattern?**
A: 
1. Agent works autonomously
2. On error or low confidence: agent signals for human takeover
3. Human takes control: provides direct instructions or takes over specific tool actions
4. Agent resumes with the human-provided guidance
5. State: takeover_requested, human_guidance
Important for safety-critical applications.

**Q73: How do you present agent reasoning to the user for review?**
A: 
- Store "thought_process" in state — the LLM's chain-of-thought
- Before executing tools, present the plan + reasoning to user
- User can: approve, modify the plan, or reject
- Uses interrupt after the reasoning step
- Frontend shows: "I plan to: 1. Search for X, 2. Analyze Y, 3. Compile result" → [Approve] [Modify]

**Q74: How do you implement asynchronous human approval (Slack/email)?**
A: 1. Graph hits interrupt, checkpointer saves state
2. Backend sends Slack message/email to human with approval request
3. Human responds via Slack/email button
4. Backend receives webhook, calls `graph.invoke(Command(resume=...))` with thread_id
5. Graph continues from checkpoint
Requires: external webhook endpoint, thread_id mapping in the notification.

**Q75: What security considerations exist for human-in-the-loop patterns?**
A: 
- Validate human input: don't trust raw resume values
- Authentication: verify who is responding (JWT, session)
- Authorization: ensure the human has permission to approve the action
- Audit trail: log all interrupts, resumes, approvals
- Rate limit resumes to prevent abuse
- Timeout: expire pending interrupts after a set duration

## 5. Advanced LangGraph Patterns (Q76–Q90)

**Q76: What is "concurrent agent execution" and how does LangGraph support it?**
A: Multiple agents executing in parallel within the same graph. Achieved via:
- Fan-out: multiple nodes executing in the same superstep
- Send(): dynamic fan-out to same node with different state subsets
- Subgraphs: independent subgraphs running in parallel
- State merging: reducers combine results from parallel branches
Useful for: parallel research, simultaneous API calls, multi-perspective analysis.

**Q77: How does LangGraph integrate with LangChain's tools and retrievers?**
A: Seamlessly — nodes can use any LangChain component:
```python
def agent_node(state):
    result = chain.invoke(state["messages"])  # Any LCEL chain
    return {"messages": [result]}
```
Tools, retrievers, prompts, and parsers all work inside LangGraph nodes. LangGraph extends LangChain; it's not a replacement.

**Q78: How do you implement "streaming tokens from the agent"?**
A: Use `astream_events` with event filtering:
```python
async for event in graph.astream_events(input, version="v2"):
    if event["event"] == "on_chat_model_stream":
        yield event["data"]["chunk"].content
```
For frontend SSE: yield token content as Server-Sent Events. Each LLM call within the graph produces its own stream events identified by the run ID.

**Q79: What is the "persistent agent memory" pattern?**
A: Long-term memory across sessions:
- Store summaries/embeddings in a vector store
- At session start: retrieve relevant memories → inject into system prompt
- At session end: summarize conversation → store in long-term memory
- Uses a dedicated "memory_store" node
- LangGraph's state persists per thread; long-term memory persists across threads

**Q80: How do you implement "dynamic tool creation" for agents?**
A: Tools created at runtime based on state:
- Agent generates Python code defining the tool
- Tool is compiled and bound to the LLM
- Agent uses the dynamically created tool
- Security: sandbox execution (subprocess, container)
- Used for: data analysis (generate pandas query), database query, custom computation

**Q81: What is the "graph as a tool" pattern?**
A: A compiled LangGraph used as a tool in another LangGraph:
```python
research_subgraph = research_graph.compile()
@tool
def research_topic(topic: str) -> str:
    """Deep research a topic using multi-agent graph."""
    return research_subgraph.invoke({"topic": topic})["final_report"]
```
Enables hierarchical composition — complex capabilities wrapped as reusable tools.

**Q82: How do you implement "self-correction" in LangGraph agents?**
A: 
1. Generate output
2. Check: does output meet criteria? (LLM-as-judge, validation functions)
3. If not: feed the error + output back to the model for correction
4. Track correction count; if > max → fallback
State: correction_attempts, last_error, final_output
Self-correction loops significantly improve reliability.

**Q83: What is "parallel tool execution" in a single agent step?**
A: When the LLM returns multiple tool_calls in one response:
- LangGraph executes each tool concurrently in the same superstep
- Each tool call gets its own branch (via implicit fan-out)
- Results are collected as separate ToolMessage objects
- All tool results are passed back to the LLM in the next step
Improves speed for independent parallel actions.

**Q84: How do you integrate external APIs as graph nodes?**
A: Directly in node functions:
```python
def fetch_weather(state):
    response = requests.get(f"https://api.weather.com/{state['location']}")
    return {"weather_data": response.json()}
```
For rate-limited APIs: add retry logic, circuit breakers, and exponential backoff inside the node. For webhooks: call from the node or use astream to process results.

**Q85: What is "subgraph state isolation"?**
A: A subgraph's internal state is not visible to the parent graph. The subgraph receives input from the parent, executes with its own state schema, and returns output to the parent. This prevents: state key collisions, accidental overwrites, and coupling between components.

**Q86: How do you implement "graph versioning" in production?**
A: 
- Version your graph definition (git tag/commit)
- Store graph version in state metadata
- Run multiple graph versions behind a router (canary, stable)
- LangSmith traces include graph version for debugging
- Use `.configurable_alternatives()` for graph-level A/B testing
- Blue-green deployment: run v2 alongside v1, gradually shift traffic

**Q87: How do you handle "rate limiting" in LangGraph agents?**
A: 
- Per-tool rate limiting: use token bucket or sliding window in tool implementation
- Per-node rate limiting: wrap node with rate limiter
- LangChain's `with_retry` for API-level limits
- Queue: use asyncio.Queue with controlled consumer concurrency
- State tracking: track API call timestamps in state, enforce minimum intervals

**Q88: What is "graph compilation caching"?**
A: Graph compilation can be expensive (validating, preparing checkpointing). Cache the compiled graph:
```python
@lru_cache
def get_compiled_graph():
    builder = StateGraph(State)
    # ... define graph ...
    return builder.compile(checkpointer=checkpointer)
```
In serverless environments: compile once at cold start, reuse across invocations.

**Q89: How do you test LangGraph graphs?**
A: 
- Unit test individual nodes (pure functions)
- Integration test subgraphs in isolation
- End-to-end test: compile graph, invoke with test inputs, assert state changes
- Snapshot testing: compare checkpoints against expected values
- LangSmith datasets: run graph against test cases, measure success rate
- Property-based testing: random inputs, assert invariants (no crash, finite steps)

**Q90: What are the production considerations for LangGraph deployment?**
A: 
- Checkpointer: PostgresSaver for durability, not MemorySaver
- Concurrency: handle multiple thread_ids, lock to prevent race conditions
- Monitoring: LangSmith tracing + custom metrics (steps per run, error rate)
- Recursion limit: set appropriate cap (25-100 depending on complexity)
- Memory: monitor state size, implement trimming for long-running agents
- Graceful shutdown: save checkpoint on SIGTERM
- Scaling: horizontal with shared checkpoint DB; stateful agents stick to one thread

## 6. Ecosystem, Comparisons & Future (Q91–Q100)

**Q91: How does LangGraph compare to LangChain's AgentExecutor?**
A: AgentExecutor is simpler — linear loop (LLM → tool → LLM → tool → ...). LangGraph is more flexible — arbitrary graph structures, cycles, parallel execution, human-in-the-loop, checkpointing. LangGraph is the evolution of AgentExecutor. For complex agents: always use LangGraph. For simple tools: AgentExecutor or LangGraph both work.

**Q92: Can you use LangGraph without LangChain?**
A: LangGraph depends on LangChain's message types (BaseMessage, AIMessage, ToolMessage) and optionally on LangChain models/tools. You CAN use LangGraph with plain functions and custom state — you don't HAVE to use LangChain models. However, the ecosystem integration (tools, retrievers, models) is a major benefit.

**Q93: How does LangGraph compare to other state machine / workflow frameworks?**
A: 
- Temporal: long-running workflow orchestration, durable execution — different scale (microservices vs agent)
- Prefect: data pipeline orchestration — not LLM-aware
- AWS Step Functions: cloud-native — no LLM primitives
- AutoGen: conversation-based multi-agent — less state control than LangGraph
- LangGraph is uniquely designed for LLM agent workflows with state management, checkpointing, and human-in-the-loop

**Q94: What is the relationship between LangGraph and Pregel?**
A: LangGraph's execution engine is inspired by Google's Pregel (bulk synchronous parallel) model. Each superstep is a "step" where nodes execute in parallel, then state is synchronized. LangGraph extends Pregel with: dynamic routing, conditional edges, checkpointing, and streaming.

**Q95: How does LangGraph handle state schema evolution (adding/removing keys)?**
A: 
- State schema is defined at graph creation time
- Adding keys: deploy new graph version, old checkpoints lack the key → handle with `.get(key, default)` in nodes
- Removing keys: old checkpoints still have the key → nodes should ignore unknown keys or use migration
- Best practice: use optional keys with defaults for forward compatibility
- For major changes: new thread_id (new sessions use new schema)

**Q96: What is the LangGraph Cloud / LangGraph Platform?**
A: LangGraph Cloud is a managed platform for deploying LangGraph agents:
- Serverless graph execution
- Managed checkpointing (Postgres)
- Built-in streaming API
- Concurrency management
- Monitoring and debugging
- API key authentication
Alternative to self-hosting with FastAPI + PostgresSaver.

**Q97: What are common LangGraph anti-patterns?**
A: 
1. Too much state: storing huge documents in state — use references
2. No recursion limit: infinite loops, runaway costs
3. Forgetting reducers for parallel branches: race conditions
4. Over-engineering: using a complex graph where a simple chain would suffice
5. Ignoring checkpointing: losing state on crash
6. Tight coupling: nodes that depend on internal state of other nodes

**Q98: How do you migrate from AgentExecutor to LangGraph?**
A: 
1. Identify the agent loop (model → tools → model → ...)
2. Convert to a two-node graph (call_model, execute_tools) with conditional edge
3. Add state schema (messages list with add_messages)
4. Add checkpointer for persistence
5. Add LangSmith tracing
6. Incrementally add features: parallel tools, human-in-the-loop, subgraphs
Migration path is straightforward — the core logic remains similar.

**Q99: What are the LLMOps considerations specific to LangGraph?**
A: 
- Cost tracking: trace token usage per node per run
- Latency: measure time per node, identify bottlenecks (retrieval, LLM calls)
- Failures: categorize (rate limit, tool error, parsing error, timeout)
- Quality: track agent success rate, human intervention rate, iterations per task
- Versioning: graph version → LangSmith traces → compare quality across versions
- A/B testing: `.configurable_alternatives()` for graph variants

**Q100: What emerging trends are shaping LangGraph in 2026?**
A: 
1. Agent-as-API: LangGraph agents deployed as managed microservices
2. Multi-modal agents: vision, audio, text nodes in the same graph
3. Agent-to-agent protocols: standardized communication between LangGraph agents and external agent systems
4. Streaming-native UX: every graph output streams by default
5. Self-evolving agents: agents that modify their own graph structure
6. Federated agents: graphs spanning organizational boundaries
7. On-device LangGraph: lightweight graphs on mobile/edge
8. Formal verification: proving agent behavior before deployment
