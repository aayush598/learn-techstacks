# Agentic AI, LangGraph & CrewAI - 200+ Interview Q&A
## For YC Startups & Top Tech Companies

## AI Agent Fundamentals (Q1-Q40)
### Q1: What is an AI Agent?
**Answer:** An AI agent is an autonomous system powered by an LLM that can perceive its environment, reason about goals, and take actions using tools. Key components: model (LLM for decision-making), tools (functions agent can call), memory (conversation history, learned info), planning (task decomposition). Agents operate in a loop: observe→think→act→observe→...

### Q2: What is the ReAct pattern?
**Answer:** Reasoning + Acting. Iterative loop: (1) Thought - "I need to find the weather in Tokyo" (2) Action - call weather API tool with query. (3) Observation - API returns "25°C, sunny". (4) Thought - "I have the weather, now I can answer". (5) Final Answer - "The weather in Tokyo is 25°C and sunny." This pattern allows LLMs to interact with external systems and reason about results.

### Q3: Tools in AI agents - how are they defined?
**Answer:** Tools are functions the agent can call. Each tool has: name (unique identifier), description (when to use this tool), parameters (JSON schema describing inputs), function (actual implementation). Example: `def search_web(query: str) -> str: ...`. The LLM receives tool descriptions in the system prompt and decides when to call which tool.

### Q4: What is function calling in LLMs?
**Answer:** API feature (OpenAI, Anthropic, etc) where LLM outputs structured JSON to call a function instead of generating text. Model receives tool schemas. Outputs: `{"name": "search_web", "arguments": {"query": "weather Tokyo"}}`. Developer executes function and passes result back. More reliable than text-parsing approaches for tool use.

### Q5: Agent memory - types and use cases?
**Answer:** (1) Short-term (episodic): current conversation, stored in context window. (2) Long-term: persisted to vector DB for retrieval across sessions. (3) Working: scratchpad for current task decomposition. (4) Procedural: learned patterns/strategies. Implementation: summarize conversation → store embedding → retrieve relevant past on new session.

## LangGraph (Q41-Q100)
### Q6: What is LangGraph? How does it differ from LangChain agents?
**Answer:** LangGraph is a framework for building stateful, multi-actor LLM applications as graphs. Differences from LangChain agents: LangGraph gives explicit control over graph structure, persistent state, cycles, conditional branching, parallel execution, human-in-the-loop. LangChain agents are simpler but limited (straight loop). LangGraph is for complex workflows.

### Q7: LangGraph key concepts?
**Answer:** StateGraph: defines the graph. State: shared state passed between nodes. Nodes: compute functions (LLM calls, tool execution, data processing). Edges: connect nodes. Conditional edges: routing based on state. Persistence: save/load state at any point. Interrupts: pause execution for human approval.

### Q8: LangGraph state management?
**Answer:** State is a TypedDict. Updated by each node. Nodes receive previous state, return state updates. Edges read state to decide routing. Supports reducer functions (add_messages for appending, overwrite for replacement). Checkpointing saves state at each step for resumability.

### Q9: LangGraph persistence and human-in-the-loop?
**Answer:** Checkpointers (SqliteSaver, MemorySaver) save state at each step. Enable: (1) Resumability - continue after failure. (2) Human-in-the-loop - pause before certain actions, wait for human approval/rejection. (3) Time travel - rerun from any checkpoint. Crucial for production agent systems.

### Q10: Multi-agent orchestration in LangGraph?
**Answer:** Define sub-graphs per agent, compose into super-graph. Agents communicate through shared state. Supervisor agent routes tasks to specialist agents. Patterns: supervisor (manager delegates), sequential (A→B→C), parallel (agents work independently, results merged), debate (agents discuss to consensus).

## CrewAI (Q101-Q160)
### Q11: What is CrewAI?
**Answer:** Framework for orchestrating role-based AI agents as a crew. Each agent has role, goal, backstory, tools. Agents collaborate on tasks. Supports sequential processes, hierarchical management, task delegation, custom tools. Python-native, integrates with LangChain tools. Good for structured multi-agent workflows.

### Q12: CrewAI agent structure?
**Answer:** Agent definition: role="Researcher", goal="Find latest AI developments", backstory="Senior AI researcher", tools=[search_tool, scrape_tool], allow_delegation=True, max_iter=15, verbose=True. Each agent has clear responsibility and personality. Tasks assigned to specific agents.

### Q13: CrewAI tasks and processes?
**Answer:** Task: description, expected_output, agent assignment, tools. Process types: sequential (tasks executed in order), hierarchical (manager agent assigns tasks, reviews results). Tools shared across agents or task-specific. Crew executes tasks and returns results.

### Q14: CrewAI vs LangChain/LangGraph?
**Answer:** CrewAI is higher-level - focuses on role-based agent teams with structured task assignments. LangChain agents are simpler single agents. LangGraph is lower-level - full control over graph execution. CrewAI: "we need a team of specialists working together". LangGraph: "we need precise control over a complex workflow".

### Q15: Marketing AI Agent project (from your resume)?
**Answer:** Built AI agent integrating Gemini, HuggingFace, Groq APIs with Flask + Streamlit. Agent automates: Google Drive management, social media posting (Gmail, Twitter, YouTube APIs), content generation. Deployed as Streamlit dashboard. Multi-model architecture allows choosing provider per task. Secure env config for API keys.

## Multi-Agent Systems (Q161-Q200)
### Q16: Multi-agent patterns?
**Answer:** (1) Supervisor/Orchestrator: central agent delegates to worker agents. (2) Sequential pipeline: Agent A → Agent B → Agent C. (3) Parallel: agents work simultaneously, results merged. (4) Debate: agents discuss to improve reasoning. (5) Auction: agents bid for tasks based on capability. (6) Swarm: many simple agents, emergent behavior.

### Q17: Agent communication patterns?
**Answer:** Direct messages (agent to agent), broadcast (one-to-many), shared memory/state, structured outputs (agents output parseable data for other agents). In LangGraph: shared state. In CrewAI: task outputs passed as context to next tasks.

### Q18: Agent evaluation - how to test?
**Answer:** (1) Task completion rate - does agent achieve goal? (2) Tool call accuracy - does it use right tools with right params? (3) Efficiency - how many steps/tokens? (4) Safety - does it take unwanted actions? (5) Edge cases - malformed inputs, missing info, ambiguity. (6) Human evaluation of final outputs.

### Q19: Productionizing agents - challenges?
**Answer:** (1) Latency - tool calls + LLM reasoning takes seconds. (2) Cost - token usage per run. (3) Reliability - LLM may fail to use tools correctly. (4) Error handling - malformed tool output, API failures. (5) Observability - tracing agent decisions (LangSmith). (6) Rate limits - tool APIs have limits. (7) Safety - prevent unintended tool usage. (8) Memory management - context window limits.

### Q20: What is the future of AI agents?
**Answer:** Trends: (1) Multi-modal agents (text+images+audio+code). (2) Long-running autonomous agents with persistent memory. (3) Agent-to-agent communication protocols (A2A by Google). (4) Specialized agent marketplaces. (5) Improved reliability via better models + structured outputs. (6) Agent-native operating systems and browsers.
