# DFDSOFT / DogFoodDev — AI Agents & LLM Architecture (100 Q&A)

> Role: AI Coding & Agent Development Specialist  |  Candidate: Aayush Gid (LangChain/CrewAI/Agno/OpenAI API/RAG/embeddings/Milvus/FAISS background)

---

## 1. Agent Fundamentals & Taxonomy (Q1–Q12)

**Q1: What is an AI agent, and how does it differ from a chatbot or copilot?**
A: An AI agent is an autonomous system that perceives its environment, reasons about goals, and takes actions — often via tool calls — to achieve objectives with minimal human intervention. A chatbot is reactive (responds to user turns), a copilot augments human work in-loop, while an agent operates autonomously across multi-step workflows with its own control flow, memory, and tool access. The key distinction is agency: agents decide *what* to do next, not just how to respond.

**Q2: Describe the core agent loop (perception → reasoning → action → observation).**
A: The agent loop is: (1) **Perceive** — receive input from environment (user message, tool output, sensor data); (2) **Reason** — LLM processes context + goals to decide the next step; (3) **Act** — execute an action (call a tool, write code, send a message); (4) **Observe** — receive the result/feedback; then loop back. This is the OODA loop (Observe-Orient-Decide-Act) adapted for LLM agents.

```python
while agent.has_goal():
    observation = agent.perceive()
    decision = agent.llm.reason(observation, agent.memory)
    result = agent.act(decision)
    agent.memory.update(observation, decision, result)
```

**Q3: What are reactive agents vs. deliberative agents? Give examples.**
A: **Reactive agents** map perceptions directly to actions without internal state or planning (e.g., a reflex-based agent that classifies an email and auto-routes it). **Deliberative agents** maintain an internal model of the world, plan ahead, and reason about consequences (e.g., a planning agent that decomposes a software project into tasks before coding). Most LLM agents are deliberative because the LLM provides explicit reasoning traces.

**Q4: What is a learning agent, and how do LLM agents differ from traditional reinforcement-learning agents?**
A: A learning agent improves its behavior over time from experience. Traditional RL agents update a policy via reward signals (gradient descent, Q-learning). LLM agents "learn" via in-context learning (few-shot examples in prompts), RAG retrieval of past experiences, fine-tuning, or memory consolidation — but their core weights don't change at inference. Agno agents, for instance, can persist and retrieve memories across sessions rather than updating model weights.

**Q5: What is a multi-agent system, and when is it preferable to a single-agent design?**
A: A multi-agent system (MAS) has multiple specialized agents collaborating. Prefer MAS when: tasks are complex with distinct sub-domains (research vs. coding vs. review), parallelism improves throughput, or debate/verification reduces errors. CrewAI and Agno both support multi-agent teams. A single agent suffices for simple, tightly-scoped tasks where the overhead of inter-agent communication isn't justified.

**Q6: Explain the difference between an agent loop and a chain.**
A: A **chain** is a fixed, acyclic sequence of steps (Prompt → LLM → Output). An **agent loop** is cyclic: the agent can loop, branch, retry, or invoke different tools based on observations. Chains are DAGs; agent loops have cycles. LangChain `AgentExecutor` implements this loop — it repeatedly calls the LLM with tool outputs until the agent decides it's done.

**Q7: What makes an agent "agentic" vs. just prompt-chaining?**
A: True agenticity requires: (1) **autonomy** — the agent decides its own next steps; (2) **tool use** — it can act on the external world; (3) **memory** — it retains context across steps/sessions; (4) **goal-directedness** — it works toward an objective, not just completing a single prompt. Simple prompt chains are deterministic DAGs; agentic systems have dynamic control flow.

**Q8: What are tool-use agents? How do they differ from function-calling LLMs?**
A: Tool-use agents are systems where an LLM selects and invokes external tools (APIs, databases, code interpreters) during reasoning. Function calling is the *mechanism* (e.g., OpenAI's `tools` parameter) that lets the LLM emit structured tool invocations. The agent framework wraps this mechanism in a loop: call LLM → parse tool call → execute tool → feed result back → repeat.

**Q9: Explain the concept of an agent's "state" vs. its "memory."**
A: **State** is the current working context: the active task, current step in a plan, intermediate variables. It's ephemeral within a run. **Memory** is persisted information across runs: conversation history, past tool outputs, learned facts. State lives in the agent's execution frame (e.g., LangGraph's `State` object); memory lives in vector stores, databases, or files. Both are critical — state drives the current loop, memory provides long-term context.

**Q10: What are reflex agents in the context of Wooldridge's agent typology?**
A: Reflex agents select actions based only on current perceptions, ignoring history. They use condition-action rules: `if <perception> then <action>`. LLM equivalents are single-turn classifiers or routers. They're fast and simple but cannot handle multi-step or context-dependent tasks. Example: an LLM that reads an incoming Slack message and routes it to the right channel based purely on keywords.

**Q11: What is the role of an "executor" in agent frameworks like LangChain?**
A: The executor is the runtime loop that orchestrates the agent-LLM-tool cycle. LangChain's `AgentExecutor` receives user input, calls the agent's LLM to get a decision (which tool to call or final answer), executes the tool, appends the result to the message history, and repeats until the agent produces a final answer or hits a max-iteration limit. It also handles error recovery, timeouts, and early stopping.

**Q12: What is an agent sandbox, and why is it critical for agentic coding?**
A: A sandbox is an isolated execution environment (container, VM, or process) where an agent can run code or execute tools without risking the host system. For agentic coding (AI writing and running code), sandboxes prevent malicious or buggy code from affecting production. Cloudflare Sandbox SDK, Docker containers, and E2B are common solutions. Every production-grade agentic coding tool must have sandboxing.

---

## 2. LLM Foundations (Q13–Q25)

**Q13: Explain the Transformer architecture's self-attention mechanism.**
A: Self-attention computes, for each token, a weighted sum of all other tokens where weights are derived from Query-Key dot products (scaled by √d_k) passed through softmax. This lets every token attend to every other token in O(1) layers (but O(n²) in sequence length). Multi-head attention runs this in parallel across h heads with different learned projections, capturing diverse relational patterns.

```python
# Simplified self-attention
Q, K, V = x @ W_q, x @ W_k, x @ W_v
attn_weights = softmax(Q @ K.T / sqrt(d_k))
output = attn_weights @ V
```

**Q14: What is positional encoding, and why do Transformers need it?**
A: Transformers process all tokens in parallel with no inherent notion of order. Positional encoding injects sequence position information so the model knows token order. Original Transformers used sinusoidal functions; modern LLMs use learned embeddings or rotary positional embeddings (RoPE). Without positional encoding, "dog bites man" and "man bites dog" would be indistinguishable.

**Q15: How does tokenization work (BPE, SentencePiece)?**
A: Byte-Pair Encoding (BPE) iteratively merges the most frequent character pairs in the training corpus to build a vocabulary of subword tokens. SentencePiece is similar but works on raw text without pre-tokenization. This allows LLMs to handle rare words, misspellings, and multiple languages efficiently. A 7B-token vocabulary might have ~32K tokens. Token count determines cost and context-window consumption.

**Q16: What is the context window, and what happens when you exceed it?**
A: The context window is the maximum number of tokens an LLM can process in a single forward pass (e.g., 128K for GPT-4o, 200K for Claude). Exceeding it causes truncation — earlier tokens are dropped, which can lose critical context. Mitigations: sliding window summarization, RAG to fetch relevant context, or using models with larger windows. This is a core constraint driving RAG and memory system design.

**Q17: Explain temperature, top_p, and top_k in LLM sampling.**
A: **Temperature** scales logits before softmax — low (0.0–0.3) makes output deterministic/focused; high (0.7–1.5) makes it creative/random. **Top_p (nucleus sampling)** truncates the token distribution to the smallest set whose cumulative probability exceeds p (e.g., 0.9). **Top_k** keeps only the k highest-probability tokens. In practice, you use temperature OR top_p, not both. For agents/tool-calling, temperature=0 or 0.1 is typical for deterministic outputs.

**Q18: What causes LLM hallucination, and how can it be mitigated?**
A: Hallucination stems from: training data gaps, ambiguity in prompts, the model's tendency to produce plausible-sounding text, and lack of grounding in real-time data. Mitigations: **RAG** (ground responses in retrieved documents), **chain-of-thought reasoning** (force explicit reasoning), **self-consistency** (sample multiple outputs, majority-vote), **grounding against APIs/databases**, **retrieval-first prompting**, and **post-generation fact-checking** with an LLM-as-judge.

**Q19: What is grounding in the context of LLMs?**
A: Grounding means anchoring LLM outputs in verifiable, external information rather than relying solely on parametric memory. Techniques: RAG (retrieve documents before generating), tool-use (call APIs for real-time data), citations (reference source documents), and human-in-the-loop verification. Grounding is essential for factual accuracy in production agents — without it, confident-sounding but wrong outputs are common.

**Q20: Explain the difference between GPT-style decoder-only and encoder-decoder Transformers.**
A: **Decoder-only** (GPT, LLaMA, Claude): autoregressive, generates tokens left-to-right, each token attends to all previous tokens. Used for most modern LLMs. **Encoder-decoder** (T5, BART): encoder processes the full input bidirectionally, decoder generates output autoregessively with cross-attention to encoder. Better for seq2seq tasks (translation, summarization). Most agent-focused LLMs are decoder-only because conversational/generation is the primary use case.

**Q21: What is KV-cache, and why does it matter for agent loops?**
A: In autoregressive generation, previously computed Key and Value matrices are cached so they don't need recomputation for each new token. For agent loops with long histories (many tool calls), KV-cache grows linearly with context length, consuming GPU memory. This is why long conversations or multi-step agent runs are expensive — and why context compression and summarization matter.

**Q22: What are system prompts, and how do they differ from user prompts?**
A: System prompts set the model's persona, constraints, and instructions. They're prepended to the conversation and typically have higher "authority" — the model treats them as developer instructions. User prompts are the actual task input. In OpenAI's API, the system message sets behavior; in Anthropic's, it's the `system` parameter. For agents, system prompts define the agent's role, available tools, and behavioral rules.

**Q23: What is chain-of-thought (CoT) prompting, and why is it powerful for agents?**
A: CoT prompting instructs the model to show its reasoning step-by-step before producing a final answer. This improves performance on complex tasks by decomposing reasoning. For agents, CoT is critical because the reasoning trace becomes the agent's "thought" — it lets the agent evaluate intermediate steps, catch errors, and decide the next tool to call. ReAct prompting formalizes this as Thought → Action → Observation loops.

**Q24: What are the trade-offs between larger and smaller LLMs for agent systems?**
A: Larger models (GPT-4o, Claude) have stronger reasoning, better tool-use accuracy, and fewer hallucinations but are slower and more expensive. Smaller models (GPT-4o-mini, Llama 3 8B) are faster and cheaper but less reliable at complex multi-step reasoning. In agent systems, a common pattern is: large model for planning/complex decisions, small model for classification/routing/simple tasks — a hierarchical approach that optimizes cost and latency.

**Q25: What is structured output, and why do agents depend on it?**
A: Structured output means the LLM returns JSON (or another schema) instead of free-form text. Agents depend on this because tool calls, action decisions, and state updates all require parseable, machine-readable formats. OpenAI's `response_format` and function calling enforce structure. Without structured output, agents would need fragile regex parsing to extract tool names and arguments from free text.

---

## 3. Agent Architectures & Reasoning Patterns (Q26–Q38)

**Q26: Explain the ReAct (Reasoning + Acting) pattern.**
A: ReAct interleaves reasoning traces ("Thought") with actions ("Action") and observations ("Observation") in a loop:
```
Thought: I need to find the population of California.
Action: search("population of California")
Observation: California has ~39 million people.
Thought: Now I can answer the question.
Action: finish("39 million")
```
This grounds reasoning in real observations and prevents the LLM from hallucinating actions. It's the foundation of most tool-use agent frameworks including LangChain's `AgentExecutor`.

**Q27: What is the plan-and-execute pattern?**
A: The agent first creates a full plan (list of steps) before executing any of them. Step 1: LLM generates a plan with numbered subtasks. Step 2: Each subtask is executed sequentially or in parallel. Step 3: Results are aggregated, and optionally the plan is replanned based on intermediate results. This is better than ReAct for complex tasks because it produces coherent, globally-optimal plans rather than myopic step-by-step decisions. LangGraph supports this via its state graph.

**Q28: What is the reflection pattern in agent architectures?**
A: After producing output, the agent (or a separate evaluator agent) reviews and critiques it, then the original agent revises. The loop is: Generate → Critique → Revise → Critique → ... until satisfactory. This self-correction mechanism catches hallucinations, logical errors, and quality issues. Reflexion and LATS (Language Agent Tree Search) formalize this. In CrewAI, a reviewer agent can critique another agent's output before passing it downstream.

**Q29: Explain Tree of Thought (ToT) and its application to agents.**
A: ToT explores multiple reasoning branches simultaneously rather than following a single chain. At each decision point, the LLM generates multiple candidate "thoughts" (partial solutions), evaluates each, and prunes low-quality branches. This is like beam search in reasoning space. It excels at planning, puzzle-solving, and strategic tasks where the optimal path isn't obvious. LATS combines ToT with Monte Carlo Tree Search for more principled exploration.

**Q30: What is MRKL (Modular Reasoning, Knowledge and Language)?**
A: MRKL is an architecture that combines an LLM (language/reasoning module) with external expert modules (tools, databases, code interpreters). The LLM acts as a router that selects which expert module to invoke based on the query. This is the theoretical foundation for tool-use agents — the LLM doesn't need to know everything; it dispatches to specialized modules. Every modern agent framework implements a version of MRKL.

**Q31: Compare ReAct, plan-and-execute, and reflection architectures. When would you use each?**
A: **ReAct**: Best for straightforward multi-step tasks where the next step depends on the previous result (web search → read → answer). **Plan-and-execute**: Best for complex tasks requiring global planning before action (project scaffolding, multi-file refactoring). **Reflection**: Best for quality-critical outputs where correctness matters (code generation, document writing). In practice, combine them: plan-and-execute with reflection at each step, or ReAct with periodic reflection checkpoints.

**Q32: What is a state machine in the context of agent architecture (LangGraph)?**
A: A state machine (or state graph) defines nodes (functions/agents) and edges (transitions between them) with an explicit shared state object. In LangGraph, you define: `State` (typed dict with message history, intermediate results), nodes (functions that read/write state), and edges (conditional or direct transitions). This gives fine-grained control over agent behavior — you can implement loops, branches, parallel execution, and human-in-the-loop gates deterministically.

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)
graph.add_node("reason", reason_node)
graph.add_node("act", action_node)
graph.add_edge("reason", "act")
graph.add_conditional_edges("act", should_continue, {True: "reason", False: END})
```

**Q33: What is LATS (Language Agent Tree Search)?**
A: LATS combines tree search algorithms (like MCTS) with LLM agents. At each step, the LLM generates multiple candidate actions (branching), evaluates them (scoring via self-critique or value function), and backpropagates scores. It explores the most promising branches first. This is more thorough than ReAct (single path) but more expensive. It's ideal for tasks with high branching factors where greedy search fails — e.g., complex debugging or strategic planning.

**Q34: Explain the concept of an "action space" for agents.**
A: The action space is the set of all possible actions an agent can take — every tool, API call, or operation it can perform. Defining the action space is critical: too narrow and the agent can't solve tasks; too large and the LLM struggles to choose the right action (decision noise). Best practice: group tools logically, use tool descriptions with clear examples, and implement tool selection hierarchies (router agent → specialist agents).

**Q35: What is self-correction in agent systems, and how is it implemented?**
A: Self-correction is when an agent detects and fixes its own errors before or during execution. Implementations: (1) Output validation — check tool outputs for errors, retry with modified inputs; (2) Reflection — generate critique of own output, then revise; (3) Consistency checking — compare multiple reasoning paths; (4) Test execution — for code agents, run tests and fix failures. LangGraph supports this via conditional edges that loop back to error-recovery nodes.

**Q36: What is hierarchical agent architecture?**
A: A meta-agent (supervisor) delegates to specialist sub-agents. The supervisor decomposes the task, assigns subtasks to appropriate specialists, monitors progress, and aggregates results. This mirrors human organizational structure. In CrewAI, this is the "manager" crew pattern. In LangGraph, you can model this as a graph where a supervisor node routes to different sub-graphs. Benefits: specialization, parallelism, separation of concerns.

**Q37: What is the difference between open-loop and closed-loop agent control?**
A: **Open-loop**: The agent executes a pre-determined sequence of actions without observing intermediate results (like a script). **Closed-loop**: The agent observes the result of each action and adapts its plan accordingly. LLM agents are inherently closed-loop — they process tool outputs before deciding the next step. Open-loop is faster but brittle; closed-loop is adaptive but more expensive (more LLM calls).

**Q38: Explain "agentic coding" — how agents write and debug code.**
A: Agentic coding is when an LLM agent generates code, executes it, observes results (errors, test failures, output), and iterates until the code works. The loop: read task → generate code → run in sandbox → parse errors → fix → repeat. Systems like Devin, OpenHands, and SWE-Agent implement this. Key challenges: sandboxing, test generation, understanding large codebases (context window limits), and distinguishing between code that "looks right" and code that "works."

---

## 4. Tool Calling & Function Calling (Q39–Q50)

**Q39: How does OpenAI function calling work?**
A: You define tools as JSON Schema objects in the API request. The LLM, when it determines a tool is needed, returns a structured `tool_calls` object (not text) with the function name and parsed arguments. Your code executes the function, then sends the result back as a `tool` message. The LLM incorporates the result into its reasoning. This is the standard mechanism for all OpenAI-based agent frameworks.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
}]
```

**Q40: How does Anthropic's `tool_use` differ from OpenAI's function calling?**
A: Conceptually identical but API-level differences: Anthropic uses `tools` parameter with `input_schema`, returns tool use as content blocks (type `"tool_use"`) rather than a separate `tool_calls` field, and you respond with `tool_result` content blocks. Anthropic also supports `tool_choice` to force specific tool usage. The underlying pattern is the same: define schema → LLM emits structured call → execute → return result.

**Q41: What is a JSON Schema, and why is it important for tool definitions?**
A: JSON Schema defines the structure, types, required fields, and constraints of a tool's input parameters. It's critical because: (1) The LLM uses it to generate correctly-structured arguments; (2) It enables automatic validation before execution; (3) It generates tool documentation for the model. Well-written schemas with descriptions and enums dramatically improve tool-call accuracy. Bad schemas are the #1 cause of tool-calling failures.

**Q42: How should you handle tool-call errors in agent systems?**
A: Strategies: (1) **Return the error as the tool result** — the LLM sees the error and can retry with corrected arguments; (2) **Retry with exponential backoff** for transient errors (API rate limits, network timeouts); (3) **Implement fallback tools** — if primary tool fails, try an alternative; (4) **Error classification** — distinguish retryable errors from permanent failures; (5) **Circuit breaker** — stop calling a failing tool after N failures. Never let unhandled tool errors crash the agent loop.

```python
def safe_tool_call(tool_func, *args, **kwargs):
    try:
        return tool_func(*args, **kwargs)
    except RateLimitError:
        time.sleep(exponential_backoff())
        return tool_func(*args, **kwargs)
    except Exception as e:
        return f"Error: {str(e)}. Please try a different approach."
```

**Q43: What are parallel tool calls, and when should you use them?**
A: Parallel tool calls let the LLM request multiple independent tool invocations in a single response (OpenAI supports this natively). Use when: (1) Multiple independent lookups are needed (get weather for 3 cities simultaneously); (2) Task decomposition produces independent subtasks; (3) Reducing round-trips improves latency. Sequential calls are needed when step B depends on step A's result.

**Q44: How do you decide which tools to give an agent?**
A: Principles: (1) **Relevance** — only provide tools relevant to the agent's task scope; (2) **Minimalism** — fewer tools = better selection accuracy (LLMs confuse similar tools); (3) **Clear descriptions** — each tool needs unambiguous naming and documentation; (4) **Composability** — prefer composable atomic tools over monolithic ones; (5) **Testability** — tools should have deterministic outputs for testing. Start with minimum viable toolset, expand based on failure analysis.

**Q45: What is tool orchestration, and how do you implement it?**
A: Tool orchestration is managing the flow of tool calls — deciding execution order, handling dependencies, managing concurrency, and aggregating results. Implementations: (1) **Sequential pipeline** — tools run in order; (2) **Parallel fan-out** — independent tools run simultaneously; (3) **DAG-based** — model tool dependencies as a directed acyclic graph; (4) **Agent-driven** — LLM decides order dynamically (ReAct). LangGraph excels at explicit orchestration; ReAct-style agents use dynamic orchestration.

**Q46: Explain the concept of a "tool description" and why it matters for accuracy.**
A: The tool description is the natural-language explanation the LLM uses to decide when and how to call the tool. It's the single most important factor in tool-selection accuracy. Best practices: describe *what* the tool does (not how), specify when to use it vs. alternatives, note edge cases, and include parameter descriptions with examples. A vague description leads to wrong tool selection; a precise one enables correct routing even with many tools.

**Q47: What is a tool router, and when do you need one?**
A: A tool router is a lightweight classifier or LLM call that pre-selects which tools to expose to the main agent based on the query. Use when: (1) You have 20+ tools (LLMs struggle with >15-20 tools); (2) Tools belong to distinct domains; (3) Cost optimization (don't load all tool schemas for simple queries). Router can be a small LLM call: "Given this query, which tools are relevant?" → filter tool list → pass to main agent.

**Q48: How do you test tool implementations in agent systems?**
A: (1) **Unit tests** — test each tool function independently with known inputs/outputs; (2) **Mock external APIs** — don't call real services in tests; (3) **Schema validation** — verify tool output matches expected schema; (4) **Integration tests** — test tool + LLM interaction with recorded LLM responses; (5) **End-to-end tests** — full agent loop with deterministic inputs; (6) **Regression tests** — track tool-call accuracy over time. Use fixtures for deterministic LLM responses.

**Q49: What is structured output mode, and how does it relate to tool calling?**
A: Structured output mode (`response_format: { type: "json_object" }` or `strict: true` in tool definitions) forces the LLM to produce valid JSON matching a schema. For tool calling, `strict: true` ensures every tool call matches the exact schema, eliminating parsing errors. The trade-off is slightly higher latency and potentially less flexible outputs. For agents, always use strict mode for tool calls.

**Q50: How do you handle situations where the LLM hallucinates a tool that doesn't exist?**
A: When the LLM calls a non-existent tool: (1) Return an error message listing available tools; (2) Log the hallucinated tool name for prompt improvement; (3) Update the system prompt to explicitly list available tools; (4) Reduce temperature to prevent creative tool invention; (5) Fine-tune with examples of correct tool usage. Some frameworks handle this automatically by validating tool names against the registered tool list before execution.

---

## 5. Memory Systems (Q51–Q62)

**Q51: What are the different types of memory in agent systems?**
A: (1) **Working/short-term** — current conversation buffer (last N messages); (2) **Long-term** — persisted facts extracted and stored in a vector DB; (3) **Episodic** — memories of specific past interactions/experiences; (4) **Semantic** — generalized knowledge derived from multiple episodes; (5) **Procedural** — learned action sequences (e.g., "when user says X, do Y"). Most production agents implement short-term + long-term memory; episodic/semantic require more sophisticated extraction.

**Q52: Explain the conversation buffer memory strategy.**
A: Store the last N messages (or N tokens) in the conversation history. Simple, fast, and preserves recent context perfectly. Limitation: loses early context. Variant: **token-limited buffer** keeps messages until token count exceeds a threshold, then drops oldest. This is what most chat applications implement. The `ConversationBufferWindowMemory` in LangChain wraps this pattern.

**Q53: What is summary memory, and when should you use it?**
A: Instead of storing all messages, periodically summarize the conversation history and replace older messages with the summary. Use when: conversations are very long (100+ turns), context window is limited, or early conversation context is important but full detail isn't. The trade-off: you lose specific details but retain thematic understanding. Implementation: after every K turns, LLM summarizes the full history into a condensed form.

**Q54: How does vector-store-based long-term memory work?**
A: Each interaction is embedded into a vector and stored in a vector database (Milvus, FAISS). When the agent starts a new session, relevant past memories are retrieved via similarity search and injected into the context. This mimics human associative memory — retrieving relevant past experiences based on the current situation. Agno implements this pattern with built-in memory search. Key decisions: what to embed (full messages? extracted facts?), when to store, and retrieval threshold.

```python
# Store memory
embedding = embed(current_interaction)
vector_store.insert(embedding, metadata={"topic": topic, "timestamp": now})

# Retrieve memory
relevant_memories = vector_store.search(embed(current_query), top_k=5)
agent_context = format_memories(relevant_memories)
```

**Q55: What is episodic memory, and how does it differ from semantic memory?**
A: **Episodic memory** stores specific past experiences with context (time, place, outcome). Example: "On March 5, user asked about deploying to AWS and the deployment failed due to IAM permissions." **Semantic memory** stores generalized knowledge extracted from episodes. Example: "User prefers AWS over GCP." Episodic is detailed but specific; semantic is abstracted but broadly applicable. Both can be implemented via vector stores with different extraction strategies.

**Q56: What is memory consolidation in agent systems?**
A: Memory consolidation is the process of transforming raw episodic memories into refined semantic knowledge over time — analogous to how the human brain consolidates memories during sleep. Implementation: periodically batch-process stored interactions, extract key facts, merge duplicates, resolve contradictions, and update the long-term memory store. This prevents memory bloat and improves retrieval quality. It's typically a background task that runs after interactions.

**Q57: Explain sliding window memory and its limitations.**
A: Sliding window keeps the most recent N messages and discards everything older. It's the simplest memory strategy — fast, predictable, and memory-efficient. Limitations: (1) No retention of important early context; (2) Window size is a fixed hyperparameter; (3) Doesn't distinguish important from unimportant messages. It works for simple chat but fails for long-running agents that need context from distant past interactions.

**Q58: What are memory retrieval strategies beyond simple similarity search?**
A: (1) **Recency weighting** — score by similarity × recency decay; (2) **Importance weighting** — score by similarity × importance score (LLM-judged); (3) **Hybrid** — combine recency, importance, and relevance; (4) **Metadata filtering** — filter by topic, user, or time range before similarity search; (5) **Re-ranking** — retrieve top-K candidates, then re-rank with a cross-encoder; (6) **Query expansion** — expand the query with LLM-generated variations for better recall.

**Q59: How do you prevent memory poisoning or injection in agents?**
A: Memory poisoning is when adversarial content in stored memories influences future agent behavior. Defenses: (1) **Sanitize before storage** — validate and clean data before embedding; (2) **Provenance tracking** — tag each memory with its source and trust level; (3) **Separation** — don't let user-generated content directly modify agent instructions; (4) **Memory review** — periodically audit stored memories; (5) **Privilege separation** — separate "user memories" from "system instructions" in retrieval.

**Q60: What is a memory graph, and when is it preferable to a flat vector store?**
A: A memory graph stores memories as nodes with explicit relationships (edges) between them — e.g., "Project X → uses → Milvus" and "Milvus → isSimilarTo → FAISS". Prefer a graph when: relationships between memories matter (traversal paths, causal chains), you need structured queries (find all memories related to topic A that happened after event B), or the domain is inherently relational. Graphs are more complex but enable richer retrieval than flat vector similarity.

**Q61: How does Agno handle agent memory?**
A: Agno provides built-in session and memory management: agents persist state across invocations, store conversation history, and can be configured with vector-store-backed memory for long-term fact retention. Agno agents support `memory` parameter that auto-manages storing and retrieving past interactions. This is one of Agno's strengths over raw LangChain — memory is a first-class concern rather than an add-on.

**Q62: What is the "lost in the middle" problem, and how does it affect memory retrieval?**
A: Research shows LLMs pay less attention to information in the middle of long contexts — they focus on the beginning and end. This means retrieved memories placed in the middle of the prompt may be ignored. Mitigations: (1) Place most critical retrieved context at the beginning or end; (2) Use fewer, higher-quality retrieved chunks; (3) Re-rank to ensure the most important information is at the top; (4) Summarize retrieved context instead of passing raw chunks.

---

## 6. RAG — Retrieval-Augmented Generation (Q63–Q75)

**Q63: Describe a complete RAG indexing pipeline.**
A: (1) **Document ingestion** — load PDFs, HTML, code, databases; (2) **Chunking** — split documents into overlapping segments (512–2048 tokens); (3) **Embedding** — convert each chunk to a vector using an embedding model (OpenAI ada-002, BGE, E5); (4) **Storage** — insert vectors + metadata into a vector store (Milvus, FAISS); (5) **Indexing** — build ANN index (HNSW, IVF) for fast retrieval. Quality of the indexing pipeline directly determines RAG quality.

**Q64: What are the main chunking strategies, and when do you use each?**
A: (1) **Fixed-size** (e.g., 512 tokens, 50-token overlap) — simple, works for uniform text; (2) **Recursive character splitting** — splits on paragraph/sentence/word boundaries (LangChain default); (3) **Semantic chunking** — split when embedding similarity drops (preserves topic boundaries); (4) **Document-structure-aware** — split on headers, sections, code blocks; (5) **Agentic chunking** — LLM decides chunk boundaries. Semantic chunking generally outperforms fixed-size but is more expensive. For code, split on functions/classes.

**Q65: How do you choose an embedding model for RAG?**
A: Factors: (1) **Dimension** — higher dimensions capture more nuance but cost more storage/compute; (2) **Domain performance** — evaluate on your domain-specific retrieval benchmark; (3) **Multilingual support** — needed if content is multi-language; (4) **Speed vs. accuracy** — `text-embedding-3-small` is fast/cheap; `text-embedding-3-large` is more accurate; (5) **Licensing** — some models are open-source (BGE, E5), others have API costs. Always benchmark on your data — no universal winner.

**Q66: Compare Milvus and FAISS as vector stores.**
A: **FAISS** (Meta): library, not a database. In-process, extremely fast for single-node, no persistence built-in (you manage saving/loading), no filtering, no distributed support. Best for prototyping and when you control the runtime. **Milvus**: full database with persistence, filtering, metadata, distributed scaling, hybrid search (vector + scalar), and production-grade reliability. Best for production RAG systems. I've used both — FAISS for quick experiments, Milvus for production workloads needing filtering and persistence.

**Q67: What is hybrid search, and why is it better than pure vector search?**
A: Hybrid search combines **semantic** (vector similarity) and **keyword** (BM25/TF-IDF) search, merging results via reciprocal rank fusion (RRF) or weighted scoring. Pure vector search misses exact keyword matches ("error code E-4021"); pure keyword search misses semantic similarity ("problems connecting to database"). Hybrid captures both. Milvus supports hybrid search natively. Elasticsearch + vector search is another common hybrid stack.

**Q68: What is re-ranking in RAG, and why is it necessary?**
A: Re-ranking takes the top-K results from an initial retrieval (vector + keyword) and re-scores them using a more precise but expensive model (cross-encoder). The initial retrieval is fast but approximate; re-ranking is slow but accurate. Typically: retrieve top 20–50 candidates → re-rank to top 3–5 → pass to LLM. This dramatically improves precision. Cross-encoder models like `bge-reranker` or Cohere Rerank are common. Without re-ranking, irrelevant chunks in the top-K dilute the context.

**Q69: Explain query transformation techniques in RAG.**
A: (1) **Query rewriting** — LLM rephrases the user's query for better retrieval; (2) **Query decomposition** — break complex questions into sub-queries, retrieve for each, aggregate; (3) **HyDE** (Hypothetical Document Embeddings) — LLM generates a hypothetical answer, embeds that, retrieves similar documents; (4) **Step-back prompting** — generate a higher-level question, retrieve broader context; (5) **Query expansion** — generate multiple query variations. These improve recall, especially for ambiguous or complex queries.

**Q70: What is faithfulness in RAG evaluation?**
A: Faithfulness measures whether the generated answer is actually supported by the retrieved context — i.e., the model isn't hallucinating information not present in the source documents. Metrics: (1) **LLM-as-judge** — ask an LLM to verify each claim against the context; (2) **NLI-based** — use a natural language inference model to check entailment; (3) **Citation accuracy** — verify each cited fact exists in the context. High faithfulness is the #1 quality requirement for production RAG.

**Q71: How do you evaluate RAG system quality end-to-end?**
A: (1) **Retrieval metrics** — recall@K, precision@K, MRR (Mean Reciprocal Rank), NDCG; (2) **Answer quality** — faithfulness, relevance, correctness (LLM-as-judge or human evaluation); (3) **End-to-end metrics** — answer accuracy on a benchmark Q&A dataset; (4) **Latency** — time from query to answer; (5) **Cost** — embedding + retrieval + LLM call costs per query. Use frameworks like RAGAS or DeepEval for systematic evaluation. Build a golden test set of 50–100 representative queries with ground-truth answers.

**Q72: What are common RAG failure modes, and how do you fix them?**
A: (1) **Wrong chunks retrieved** — improve chunking, try semantic chunking, add metadata; (2) **Right chunks, wrong answer** — improve prompting, add context ordering, reduce context noise; (3) **No relevant chunks** — expand index, improve embeddings, try hybrid search; (4) **Contradictory chunks** — add de-duplication, prioritize authoritative sources; (5) **Answer exceeds retrieved context** — add hallucination guards, restrict to "answer only from context"; (6) **Query-chunk mismatch** — add query transformation. Diagnose first: is it a retrieval problem or a generation problem?

**Q73: What is Contextual Retrieval, and how does it improve RAG?**
A: Contextual Retrieval (Anthropic's approach) prepends context to each chunk before embedding — the chunk is "This chunk is from section X of document Y about topic Z: [original chunk]". This gives the embedding model more information about where the chunk fits, dramatically improving retrieval accuracy because the embedding captures context, not just local content. It also helps with ambiguous chunks that could match many queries.

**Q74: How do you handle multi-modal RAG (text + images + tables)?**
A: (1) **Image understanding** — use multimodal embeddings (CLIP) or extract text from images via OCR/vision models; (2) **Table extraction** — parse tables into structured format, store as text or JSON; (3) **Cross-modal retrieval** — embed all modalities into the same vector space, or use separate indices with late fusion; (4) **Late-interaction models** — ColBERT-style models that handle multi-modal content at the token level. Most production RAG is text-only; multi-modal adds significant complexity.

**Q75: What is a vector database index (HNSW, IVF), and how does it affect retrieval?**
A: ANN (Approximate Nearest Neighbor) indexes trade exactness for speed. **HNSW** (Hierarchical Navigable Small World): graph-based, excellent recall/speed trade-off, good for <10M vectors, higher memory usage. **IVF** (Inverted File Index): partitions vectors into clusters, searches only nearby clusters — faster for very large datasets, slightly lower recall. For most RAG use cases (1K–1M vectors), HNSW is ideal. For billions of vectors, IVF or hybrid approaches are needed.

---

## 7. Agent Frameworks (Q76–Q85)

**Q76: What are LangChain's core abstractions?**
A: (1) **LLMs/Chat Models** — wrappers around API providers (OpenAI, Anthropic); (2) **Prompts** — templated message structures; (3) **Chains** — sequential pipelines (LLMChain, RetrievalQA); (4) **Agents** — dynamic tool-using loops (AgentExecutor); (5) **Tools** — functions the agent can call; (6) **Memory** — conversation history management; (7) **Retrievers** — interfaces to vector stores. LangChain provides the building blocks; LangGraph provides the execution engine for complex agent workflows.

**Q77: What is LangGraph, and how does it differ from LangChain agents?**
A: LangGraph is a framework for building stateful, multi-step agent workflows as graphs. While LangChain agents use a simple loop (AgentExecutor), LangGraph gives you explicit control: define state, nodes (functions), edges (transitions), and conditional logic. Benefits: deterministic control flow, support for cycles and branches, human-in-the-loop checkpoints, parallel execution, persistence. It's the successor to AgentExecutor for production agents.

```python
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    messages: list
    next_step: str

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_conditional_edges("agent", should_use_tool, {"yes": "tools", "no": END})
graph.add_edge("tools", "agent")
app = graph.compile()
```

**Q78: Explain CrewAI's role-task-crew hierarchy.**
A: **Role**: defines an agent's expertise and behavior (e.g., "Senior Python Developer" with a backstory and goal). **Task**: a specific assignment given to an agent with expected output format. **Crew**: a team of agents with a process (sequential, hierarchical, or parallel) that orchestrates task execution. CrewAI's strength is its intuitive, high-level API — you describe roles in natural language and let the framework handle the agent loop, delegation, and result aggregation.

```python
researcher = Agent(role="Research Analyst", goal="Find accurate data", backstory="...")
writer = Agent(role="Technical Writer", goal="Write clear documentation", backstory="...")

research_task = Task(description="Research AI agent architectures", agent=researcher)
write_task = Task(description="Write a report", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task], process=Process.sequential)
result = crew.kickoff()
```

**Q79: How does Agno compare to LangChain and CrewAI?**
A: Agno focuses on simplicity, performance, and first-class memory/teams. Key differences: (1) **Simpler API** — less boilerplate than LangChain; (2) **Built-in memory** — session persistence and long-term memory are native; (3) **Teams** — multi-agent collaboration is a core primitive; (4) **Performance** — optimized for low latency; (5) **Fewer abstractions** — closer to raw LLM calls, less "framework magic." CrewAI is more opinionated about role-based task execution; LangChain offers the most flexibility and ecosystem; Agno balances simplicity with power.

**Q80: When would you choose LangGraph over CrewAI?**
A: Choose LangGraph when: (1) You need fine-grained control over agent flow (specific branches, loops, conditions); (2) The workflow is a state machine, not just "assign tasks to roles"; (3) You need human-in-the-loop gates (approve before executing); (4) You need checkpointing and state persistence; (5) The workflow involves parallel execution with synchronization. CrewAI is better for straightforward multi-agent task execution where the process is simple (sequential or hierarchical) and you want rapid prototyping.

**Q81: What is the LangChain `RetrievalQA` chain, and when do you use it?**
A: `RetrievalQA` is a chain that combines a retriever with an LLM for question answering. It retrieves relevant documents and generates an answer from them. Use it for simple Q&A over documents when you don't need an agent loop — just retrieve + generate. For complex workflows (multi-step reasoning, tool use, conversation), use agents instead. It's the simplest RAG pattern in LangChain.

**Q82: How do you implement state management in LangGraph?**
A: Define a `TypedDict` or Pydantic model as your state schema. Each node function receives the current state and returns a partial update (dict with keys to modify). LangGraph handles merging updates. Use `Annotated[list, operator.add]` for append-only fields (like messages). State is the single source of truth — all nodes read from and write to it. You can serialize state to a database for persistence across restarts.

**Q83: What are LangGraph's persistence and checkpointing features?**
A: LangGraph supports `SqliteSaver` or `PostgresSaver` for persistent checkpoints. After each step, the full state is saved. This enables: (1) **Resumability** — restart from last checkpoint on failure; (2) **Human-in-the-loop** — pause execution, persist state, resume after human approval; (3) **Time-travel debugging** — inspect state at any past step; (4) **Session persistence** — maintain state across application restarts. Critical for production agents that must handle failures gracefully.

**Q84: How do you build a custom agent framework vs. using existing ones?**
A: Build custom when: (1) Existing frameworks don't support your specific control flow; (2) You need extreme performance optimization; (3) The framework overhead is unnecessary for your use case; (4) You need deep integration with proprietary systems. The minimum viable custom agent: a while loop, an LLM call with tool definitions, a tool registry, a message history list, and error handling. Start with LangChain/LangGraph — only go custom when you've outgrown them.

**Q85: What are "runnables" in LangChain's LCEL (LangChain Expression Language)?**
A: Runnables are composable units in LCEL that chain together with the `|` pipe operator. Every component (prompt template, LLM, parser, retriever, tool) is a Runnable. `prompt | llm | parser` creates a pipeline. Benefits: streaming support, async support, batch processing, and automatic tracing. LCEL replaced the older `Chain` classes with a more composable, functional API. For agents, LangGraph handles the complex loops; LCEL handles the linear pipeline segments within nodes.

---

## 8. Multi-Agent Systems (Q86–Q92)

**Q86: What is the supervisor pattern in multi-agent systems?**
A: A supervisor agent monitors other agents, delegates tasks, and aggregates results. It acts as an orchestrator: receives the high-level goal, breaks it into subtasks, assigns each to the most appropriate specialist agent, monitors execution, handles failures, and synthesizes the final output. In LangGraph, this is modeled as a supervisor node that routes to different agent sub-graphs. In CrewAI, this is the hierarchical process.

**Q87: Explain agent-to-agent communication patterns.**
A: (1) **Direct messaging** — agents send messages to each other (Agno teams); (2) **Shared state** — agents read/write to a common state object (LangGraph); (3) **Pub/sub** — agents publish events, others subscribe (event-driven architectures); (4) **Blackboard** — shared workspace where agents post and read information; (5) **Hierarchical** — all communication goes through a central supervisor. Shared state (LangGraph) is the most common pattern in LLM agent systems because it's simple and deterministic.

**Q88: What is the difference between orchestration and choreography in multi-agent systems?**
A: **Orchestration**: A central coordinator (supervisor) controls the workflow, assigns tasks, and manages sequencing. Simple to understand and debug. **Choreography**: Agents react to events from other agents without a central coordinator. More scalable and resilient but harder to debug. Most LLM multi-agent systems use orchestration because LLM agents benefit from explicit coordination. Choreography works better for event-driven microservices.

**Q89: How do you handle agent disagreement in multi-agent systems?**
A: (1) **Majority voting** — multiple agents answer independently, majority wins; (2) **Debate** — agents argue for their positions, a judge resolves; (3) **Confidence weighting** — weight each agent's output by its self-assessed confidence; (4) **Supervisor arbitration** — a supervisor agent evaluates and selects; (5) **Verification agent** — a separate agent checks others' work. Debate patterns (like in CrewAI) improve accuracy for subjective tasks by surfacing alternative viewpoints.

**Q90: How do you prevent infinite loops in multi-agent systems?**
A: (1) **Max iteration limits** — cap the total number of steps/LLM calls; (2) **Max agent turns** — limit how many times agents can communicate; (3) **Timeout** — set wall-clock time limits; (4) **Convergence detection** — stop when agent outputs stabilize (low change between iterations); (5) **Circuit breakers** — stop when error rates exceed threshold; (6) **Explicit termination conditions** — define clear "done" criteria. Always implement at least 2 of these — production agents without loop guards will eventually hang.

**Q91: What is "agent specialization," and why does it matter?**
A: Specialization means each agent has a narrow focus — a specific role, domain expertise, and tool set. A "research agent" has search tools and is prompted for information gathering; a "coding agent" has code execution tools and is prompted for development. Benefits: better performance (focused prompts are more accurate), cost efficiency (smaller models for simpler tasks), and maintainability (each agent is testable independently). CrewAI's role-based design encourages this naturally.

**Q92: How do you evaluate multi-agent system performance?**
A: Metrics: (1) **Task completion rate** — did the system achieve the goal?; (2) **Quality** — LLM-as-judge scoring of output quality; (3) **Latency** — end-to-end time; (4) **Cost** — total LLM API calls × cost per call; (5) **Agent utilization** — which agents were used, how often; (6) **Error rate** — how many steps required retries; (7) **Communication overhead** — inter-agent message count. Compare against single-agent baselines — multi-agent is only justified if it meaningfully outperforms simpler approaches.

---

## 9. Evals, Guardrails & Safety (Q93–Q98)

**Q93: How do you evaluate agent task completion?**
A: (1) **Binary success** — did the agent achieve the objective? (define clear success criteria); (2) **Partial credit** — score on a rubric (0–5 scale for completeness, accuracy, style); (3) **Tool-call accuracy** — did the agent call the right tools with correct arguments?; (4) **Step efficiency** — how many steps to reach the goal? (fewer is better); (5) **LLM-as-judge** — use a separate LLM to evaluate output against criteria; (6) **Human evaluation** — gold standard but doesn't scale. Build a test suite of 50+ representative tasks with expected outcomes.

**Q94: What is LLM-as-judge, and what are its pitfalls?**
A: LLM-as-judge uses a (usually stronger) LLM to evaluate agent outputs against criteria. Pitfalls: (1) **Position bias** — LLMs prefer outputs presented first; (2) **Verbosity bias** — longer answers rated higher; (3) **Self-preference** — LLMs rate their own outputs higher; (4) **Inconsistency** — same input, different scores across runs; (5) **Criterion interpretation** — LLM may misinterpret evaluation criteria. Mitigations: use a different LLM than the one being evaluated, randomize presentation order, use structured rubrics, average across multiple evaluations.

**Q95: What are guardrails in agent systems?**
A: Guardrails are safety mechanisms that validate inputs and outputs. Input guardrails: prompt injection detection, topic filtering, PII detection, rate limiting. Output guardrails: content safety filtering, hallucination detection, format validation, sensitive data redaction, tool-call validation. Implementation: pre/post processing middleware around the agent loop. LangGraph supports guardrails as nodes that can halt execution on violations. Every production agent needs both input and output guardrails.

**Q96: How do you defend against prompt injection in agent systems?**
A: (1) **Input sanitization** — strip or escape suspicious patterns; (2) **Instruction hierarchy** — system message > user message (enforce via prompt structure); (3) **Separation** — don't mix user data with system instructions; (4) **Input validation** — classify inputs as safe/unsafe before processing; (5) **Canary tokens** — embed unique tokens in system prompts to detect if they've been leaked; (6) **Least-privilege tools** — agents only have tools they need; (7) **Output monitoring** — detect if the agent is acting outside expected behavior. Prompt injection is the top security risk for agent systems.

**Q97: What is output validation, and how do you implement it?**
A: Output validation checks agent outputs against expected schemas, content policies, and quality criteria before returning to the user. Implementations: (1) **Schema validation** — Pydantic models or JSON Schema to verify structured outputs; (2) **Content filtering** — check for harmful, biased, or off-topic content; (3) **Hallucination checking** — verify claims against source documents; (4) **Format enforcement** — ensure code blocks, citations, and formatting are correct; (5) **Retry on failure** — if validation fails, ask the agent to regenerate. Implement as middleware in the agent loop.

**Q98: How do you measure the cost-effectiveness of an agent system?**
A: Track: (1) **Tokens per task** — input + output tokens × price per token; (2) **LLM calls per task** — more calls = higher cost; (3) **Tool call costs** — external API calls have their own pricing; (4) **Latency** — time = money (compute costs); (5) **Task success rate** — failed tasks = wasted cost; (6) **Cost per successful task** — total cost / tasks completed. Optimize by: using smaller models for simple subtasks, caching common queries, reducing unnecessary tool calls, and batching. Always benchmark cost against a simpler alternative.

---

## 10. Advanced Topics (Q99–Q100)

**Q99: What is the current frontier of agentic AI, and what are the unsolved problems?**
A: Frontiers: (1) **Long-horizon autonomy** — agents that work reliably for hours/days, not minutes; (2) **Agentic coding maturity** — agents that handle full software projects, not just snippets; (3) **Multi-modal agents** — combining vision, audio, and code execution; (4) **Self-improving agents** — agents that learn from their failures without retraining; (5) **Agent-to-agent internet** — standardized protocols for agent communication (MCP, A2A). Unsolved: reliability at scale, cost efficiency, safe autonomy, evaluation methodology, and the exploration-exploitation trade-off in open-ended tasks.

**Q100: Design an AI agent system for a California startup that automates customer support — describe architecture, tools, memory, and evals.**
A: **Architecture**: Hierarchical multi-agent system with LangGraph for orchestration. **Supervisor agent** classifies incoming tickets (routing node). **Specialist agents**: (1) FAQ agent — RAG over knowledge base (Milvus + contextual embeddings); (2) Code/technical agent — debugs issues, runs diagnostic tools; (3) Escalation agent — handles complex cases requiring human review. **Memory**: conversation buffer (current session) + vector-store long-term memory (customer history, past resolutions). **Tools**: knowledge base search, CRM lookup, ticket creation, Slack notification, code log retrieval. **Guardrails**: PII redaction on inputs, content safety filter on outputs, prompt injection detection, max 10 LLM calls per ticket. **Evals**: golden test set of 100 support scenarios, LLM-as-judge for answer quality, track first-contact resolution rate, average handling time, and cost per ticket. Monthly review of escalation reasons to identify gaps in the knowledge base.
