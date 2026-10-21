# DFDSOFT / DogFoodDev — AI Coding & Agent Development Specialist — INTERVIEW CHEAT SHEET

> Role: AI Coding & Agent Development Specialist (Remote, Full-time, US overlap 8:30 PM–5:30 AM IST)
> Candidate: Aayush Gid | Last-minute revision sheet — study this before the interview

---

## YOUR 2-MINUTE PITCH ("Tell me about yourself")

> "I'm Aayush, a final-year B.Tech E&C student from Indore with deep hands-on experience in AI agent development and Python backend engineering. Over the past year, I've completed three AI-focused internships — at Krip AI building LLM-powered automation workflows with FastAPI and Docker, at Clone Futura developing REST API automations for Google Drive, and at NullClass building a BERT-based sentiment analysis chatbot. I've also built and shipped several AI projects: MigratorGen, a code migration tool using LibCST and OpenAI; ScriptVector, an AI content generator using Agno agents and Gemini; and a Marketing AI Agent that integrates Gmail, Twitter, and YouTube APIs. I'm an active open-source contributor to the Agno framework — I've merged PRs for Milvus reranking and JSON filter parsing. I'm passionate about building AI agents and automation tools, and I love the startup energy of turning rough ideas into working software fast. That's exactly what this role is about, which is why I'm excited about DFDSOFT."

---

## YOUR 30-SECOND ELEVATOR PITCH

> "AI developer with 3 internships and multiple shipped AI agent projects. I build with Python, FastAPI, LangChain, CrewAI, and Agno. I've contributed open-source PRs to the Agno framework. I'm comfortable with ambiguity, fast iteration, and turning founder ideas into working tools."

---

## KEY RESUME NUMBERS TO REMEMBER

| Metric | Value |
|--------|-------|
| Internships | 3 (all AI-focused, remote) |
| AI projects shipped | 3 (MigratorGen, ScriptVector, Marketing AI Agent) |
| Open-source PRs merged | 3+ (Agno framework — Milvus reranking, JSON filter, Crawl4AI proxy) |
| Hackathon result | SIH 2024 Finalist (500 teams) |
| Coding competition | IIT Bombay Techfest Top 5 (500+ participants) |
| Publication | IEEE — Real-Time Face Mask Detection (2024) |
| Tech stack | Python, JavaScript, FastAPI, Flask, LangChain, CrewAI, Agno, OpenAI API, TensorFlow, Keras, Docker, GitHub Actions, PostgreSQL, SQLite, Milvus, FAISS, pytest |

---

## JOB REQUIREMENTS → YOUR EVIDENCE MAP

| Job Requirement | Your Evidence |
|-----------------|---------------|
| Claude, Codex, Cursor, Copilot experience | Frame: used OpenAI API extensively (MigratorGen LLM parser, Marketing Agent Gemini/Groq); have used Cursor for development; familiar with AI-assisted coding workflows |
| Build/configure/test/improve AI agents | Agno agents (ScriptVector), CrewAI knowledge, LangChain experience, LangGraph familiarity |
| Python, JavaScript, TypeScript | Python (primary — all 3 internships + all projects), JavaScript (all projects use JS frameworks), TypeScript (GuardrailZ/Workflow-Canvas from resume) |
| APIs, JSON, webhooks, GitHub, CLI | REST APIs (all internships), JSON parsing (MigratorGen), GitHub (active contributor), CLI (MigratorGen CLI tool) |
| Software architecture understanding | FastAPI microservices (Krip AI), containerized with Docker, CI/CD pipelines |
| English communication | Open-source PRs with international maintainers, technical documentation, IEEE publication |
| Startup ambiguity / quick pivots | 3 startup internships, hackathon finalist, "ship fast" projects |
| RAG, vector DBs, embeddings | Milvus (open-source reranking PR), FAISS, embeddings knowledge |
| Ongoing support / maintenance | CI/CD pipelines at Krip AI, monitoring agents in production |

---

## TOP 10 QUESTIONS YOU WILL DEFINITELY BE ASKED

### 1. "How would you build an AI agent from scratch?"
> Start with: Define the agent's goal → choose LLM (Claude/GPT-4o) → define tools (function calling with JSON Schema) → implement agent loop (ReAct: observe → think → act → observe) → add memory (conversation buffer + vector store for long-term) → add guardrails (input validation, output filtering) → test with evals → deploy with monitoring.

### 2. "What's the difference between ReAct and plan-and-execute agents?"
> ReAct: interleaves reasoning and acting in a single loop — thinks step-by-step, takes one action, observes result, repeats. Plan-and-execute: first creates a full plan, then executes steps sequentially. ReAct is better for dynamic tasks where each step depends on previous results. Plan-and-execute is better for complex multi-step tasks where you can plan upfront.

### 3. "How does RAG work? Walk me through the pipeline."
> 1) Ingest documents → 2) Chunk text (fixed-size/semantic/recursive) → 3) Generate embeddings (OpenAI ada/sentence-transformers) → 4) Store in vector DB (Milvus/FAISS) with metadata → 5) At query time: embed the query → 6) Retrieve top-k similar chunks → 7) Optionally rerank (cross-encoder) → 8) Assemble context + query into prompt → 9) Generate answer with LLM → 10) Evaluate faithfulness and relevance.

### 4. "Tell me about a time you dealt with ambiguity."
> STAR: At Clone Futura, the founder had a vague idea about "automating Google Drive workflows." There was no spec. I asked clarifying questions, defined the scope myself (which files, what triggers, what output), built a FastAPI service with SQLite storage, integrated the Google Drive API, and delivered a working automation in 4 weeks — all with minimal supervision.

### 5. "How do you review AI-generated code?"
> Check: 1) Correctness — does it solve the actual problem? 2) Security — no hardcoded secrets, proper input validation, no SQL injection. 3) Error handling — does it handle edge cases and failures gracefully? 4) Performance — any unnecessary allocations or N+1 queries? 5) Readability — naming, structure, comments where needed. 6) Tests — are there tests for the generated code? 7) Dependencies — are all imports necessary and available?

### 6. "How do you handle working US hours (8:30 PM–5:30 AM IST)?"
> "I'm a night owl by nature and have done late-night coding sessions for hackathons and deadlines. I'm comfortable with this schedule and see it as an advantage — fewer distractions during deep work hours, and direct overlap with the team for real-time collaboration when they need me most."

### 7. "What's your experience with Claude / Anthropic's API?"
> "I've primarily used OpenAI and Gemini APIs in my projects, but I'm deeply familiar with the LLM API paradigm — system prompts, user/assistant messages, tool use, temperature control, token limits. Claude's API follows similar patterns to OpenAI's with some differences: tool_use content blocks instead of function_call, thinking tokens for extended reasoning, and prompt caching. I've been exploring Claude's capabilities and am ready to work with it on day one."

### 8. "How would you build an automation workflow for a founder's idea?"
> 1) Listen to the idea, ask clarifying questions (what triggers it, what data, what output). 2) Break into steps (trigger → process → action). 3) Choose tools (APIs, scripts, AI models). 4) Build a prototype fast (vibe code it). 5) Test with real data. 6) Add error handling and logging. 7) Deploy. 8) Monitor and iterate based on feedback. "I did exactly this at Clone Futura and with the Marketing AI Agent."

### 9. "What's the most challenging AI project you've built?"
> MigratorGen: Building an LLM-based parser that extracts structured migration steps from unstructured Markdown changelogs was hard. The LLM sometimes hallucinated steps or missed edge cases. I solved it by: designing strict JSON schemas for output, few-shot prompting with real changelog examples, adding validation with Pydantic, and building a pytest suite with 50+ test cases covering edge cases. The result was a reliable CLI tool that automates library upgrades.

### 10. "Why DFDSOFT / DogFoodDev?"
> "I'm drawn to the startup energy and the mission of building AI-powered tools for product builders. The role perfectly matches my strengths — I build AI agents, I ship fast, and I'm comfortable with ambiguity. The California entrepreneur culture resonates with how I work: big ideas, fast experiments, shipping today. And the technical stack aligns exactly with what I do daily."

---

## TECHNICAL CONCEPTS — QUICK DEFINITIONS

| Concept | One-Line Definition |
|---------|-------------------|
| **ReAct Agent** | Agent that interleaves reasoning (thinking) and acting (tool calls) in a loop |
| **Function Calling** | LLM outputs structured JSON to call predefined tools/functions instead of free text |
| **RAG** | Retrieval-Augmented Generation — retrieve relevant docs from vector store, inject into LLM context |
| **Embedding** | Dense vector representation of text (e.g., 1536-dim) capturing semantic meaning |
| **HNSW** | Hierarchical Navigable Small World — fast ANN algorithm for vector similarity search |
| **LangChain** | Python framework for building LLM-powered apps with chains, agents, tools, memory |
| **LangGraph** | LangChain's framework for building stateful, multi-step agent workflows as graphs |
| **CrewAI** | Multi-agent framework where agents have roles, goals, and backstories, working as a crew |
| **Agno** | Lightweight agent framework the candidate contributed to (Milvus reranking, tool configs) |
| **Cosine Similarity** | Measures angle between two vectors — primary metric for embedding similarity (0 to 1) |
| **Chunking** | Splitting documents into smaller pieces for embedding and retrieval in RAG pipelines |
| **HMAC Signature** | Hash-based message authentication — used to verify webhook payloads are authentic |
| **Circuit Breaker** | Pattern that stops calling a failing service after N errors, preventing cascade failures |
| **Exponential Backoff** | Retry strategy where wait time doubles after each failure (1s, 2s, 4s, 8s...) |
| **MVP** | Minimum Viable Product — simplest version that delivers core value, built fast for validation |
| **Prompt Injection** | Attack where user input tricks the LLM into ignoring system instructions or performing unauthorized actions |
| **Grounding** | Connecting LLM outputs to factual sources (RAG, citations) to reduce hallucination |
| **Evals** | Systematic evaluation of AI model/agent performance using test cases and metrics |
| **Guardrails** | Input/output validation rules that prevent AI from generating harmful/inaccurate content |
| **Tool Use vs Function Calling** | Same concept — LLM calls external functions via structured JSON output (Anthropic calls it "tool use", OpenAI "function calling") |

---

## AGNO FRAMEWORK — KNOW THIS COLD (YOUR OPEN-SOURCE CONTRIBUTION)

**What is Agno?**
Lightweight Python framework for building AI agents. Agents have tools, memory, and can work in teams.

**Your PRs:**
1. **Milvus Reranking**: Added reranking support to Milvus vector store integration — improved search relevance by re-ordering initial results using a cross-encoder model
2. **JSON Filter Parsing**: Fixed a bug where complex JSON filters weren't parsed correctly — improved filter handling for metadata-based vector searches
3. **Crawl4AI Proxy Configuration**: Added proxy support to the Crawl4AI toolkit — enabled agents to scrape web content through proxy servers for privacy/rate-limiting

**Why this matters for the role:** Shows you can contribute to production AI frameworks, understand agent architectures deeply, and work with vector databases — exactly what DFDSOFT needs.

---

## PROJECT TALKING POINTS

### MigratorGen (Code Migration Platform)
- **Problem**: Library upgrades are manual, tedious, error-prone
- **Solution**: CLI tool that parses changelogs (JSON/Markdown), uses LLM to extract migration steps, generates code transforms using LibCST (Python AST library)
- **Tech**: Python, LibCST (Python source code transformation), OpenAI API, pytest
- **Key insight**: LLMs are great at understanding unstructured changelogs but need strict JSON schema enforcement to output structured data
- **Testing**: 50+ pytest cases, including edge cases (malformed changelogs, missing versions, breaking changes)

### ScriptVector (Hindi Manhwa Content Generator)
- **Problem**: Generating long-form Hindi content with contextual continuity
- **Solution**: AI pipeline using Agno agents + Gemini API with SQLite for memory/context storage
- **Tech**: Python, Gemini API, Agno agents, SQLite
- **Key insight**: Long-form content needs context memory — SQLite stores previous chapter context so the AI maintains story continuity

### Marketing AI Agent
- **Problem**: Managing social media and Google Drive manually is time-consuming
- **Solution**: AI agent that automates Gmail, Twitter, YouTube, Google Drive tasks
- **Tech**: Python, Flask, Streamlit, Gemini API, HuggingFace, Groq (fast inference)
- **Key insight**: Multi-API integration requires careful auth management (OAuth2 tokens, API keys) and error handling for rate limits

---

## QUESTIONS TO ASK THEM

1. "What does the current AI agent stack look like at DFDSOFT? Are you using LangChain, CrewAI, or custom frameworks?"
2. "What's the typical workflow when a founder comes with a new idea? From concept to deployed agent — what's the timeline?"
3. "How do you currently handle agent evaluation and monitoring in production?"
4. "What are the most common types of AI agents you're building — customer-facing chatbots, internal automation tools, or data processing agents?"
5. "How does the team handle the US time zone overlap? What does a typical day look like?"
6. "What's the biggest technical challenge the team is currently facing?"

---

## FINAL CHECKLIST BEFORE THE INTERVIEW

- [ ] You can explain ReAct, plan-and-execute, and tool calling clearly
- [ ] You know RAG pipeline end-to-end (chunking → embedding → retrieval → generation)
- [ ] You can walk through any project in 2 minutes using STAR/problem-solution-result
- [ ] You know the difference between LangChain, LangGraph, CrewAI, and Agno
- [ ] You can explain prompt injection and how to defend against it
- [ ] You know what function calling / tool use is and can describe JSON Schema for tools
- [ ] You have a clear "tell me about yourself" answer (2 minutes)
- [ ] You know why you want this role specifically (startup energy + AI agents + US exposure)
- [ ] You're comfortable explaining your Agno open-source contributions technically
- [ ] You have 6 questions ready to ask them
- [ ] You've tested your audio/video/connection for the call
- [ ] You're ready for the US time zone (8:30 PM–5:30 AM IST)

---

*Good luck, Aayush. You've got this.*
