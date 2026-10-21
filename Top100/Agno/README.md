# Agno Interview Questions and Answers

## Q1: What is Agno?
**A:** Agno is an open-source AI framework for building multi-modal agents and workflows. It provides tools for creating intelligent agents that can reason, use tools, access knowledge, and collaborate in multi-agent systems. Agno emphasizes simplicity, performance, and developer experience.

**Code:**
```python
from agno.agent import Agent

agent = Agent(description="A multi-modal agent built with Agno.")
agent.print_response("Explain what Agno is.")
```

## Q2: What programming languages does Agno support?
**A:** Agno is primarily written in Python and provides a Python SDK for building agents. It supports TypeScript/JavaScript for certain integrations and can be used with other languages through its API interface.

**Code:**
```python
from agno.agent import Agent

# Agno is written in Python and consumed through its Python SDK
agent = Agent(description="Built with Python and the Agno SDK.")
agent.print_response("Hello from Python.")
```

## Q3: How do you install Agno?
**A:** Agno is installed via pip: `pip install agno`. Additional dependencies for specific features can be installed with extras like `pip install agno[openai]`, `agno[anthropic]`, or `agno[all]`.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Install with: pip install agno  (add extras, e.g. pip install 'agno[openai]')
agent = Agent(model=OpenAIChat(id="gpt-4o"))
agent.print_response("Reply with a short greeting.")
```

## Q4: What is an Agent in Agno?
**A:** An Agent in Agno is an autonomous program that uses an LLM to reason, make decisions, and perform actions. Agents have access to tools, knowledge bases, memory, and can be configured with specific instructions, models, and response formats.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"{city}: sunny"

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[get_weather],
    instructions=["You are a helpful assistant."],
    memory=Memory(),
)
agent.print_response("What is the weather in Paris?")
```

## Q5: How do you create a basic Agent in Agno?
**A:** Create an Agent by instantiating the Agent class with a model:

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
agent = Agent(model=OpenAIChat(id="gpt-4"))
agent.print_response("Tell me a joke")
```

## Q6: What are Tools in Agno?
**A:** Tools are functions that agents can use to perform actions like web searches, API calls, code execution, file operations, and database queries. Tools are defined as Python functions with type hints and docstrings, which the agent uses to understand their purpose and calling convention.

**Code:**
```python
from agno.agent import Agent

def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It is sunny in {city}."

agent = Agent(tools=[get_weather], show_tool_calls=True)
agent.print_response("What's the weather in Lyon?")
```

## Q7: How do you create a custom Tool in Agno?
**A:** Define a function with type hints and a docstring, then pass it to the Agent:

**Code:**
```python
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny."
agent = Agent(tools=[get_weather])
```

## Q8: What is the Agno Knowledge Base?
**A:** The Knowledge Base is a system for storing and retrieving information that agents can reference. It supports vector stores (Pinecone, Weaviate, Chroma, Qdrant), document loaders, text splitters, and embedding models for RAG (Retrieval Augmented Generation).

**Code:**
```python
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pineconedb import PineconeDB

knowledge_base = PDFKnowledgeBase(
    path="docs/", vector_db=PineconeDB(index_name="handbook")
)
agent = Agent(knowledge=knowledge_base)
agent.print_response("Summarise the handbook for me.")
```

## Q9: How do you add knowledge to an Agno agent?
**A:** Load documents, split them, store embeddings, and attach the knowledge base to the agent:

**Code:**
```python
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pineconedb import PineconeDB
knowledge_base = PDFKnowledgeBase(path="docs/", vector_db=PineconeDB())
agent = Agent(knowledge=knowledge_base)
```

## Q10: What is a Workflow in Agno?
**A:** A Workflow in Agno is a directed graph or sequence of steps that define complex AI processes. Workflows can include multiple agents, conditional branching, parallel execution, and human-in-the-loop interactions. They are built using the `Workflow` class with defined steps.

**Code:**
```python
from agno.workflow import Workflow, RunResponse

class ResearchWorkflow(Workflow):
    description = "A predefined sequence of steps."

    def run(self, topic: str) -> RunResponse:
        notes = self.run_agent(researcher, f"Research {topic}")
        return RunResponse(content=notes.content)

result = ResearchWorkflow().run("AI agents")
print(result.content)
```

## Q11: How does Agno handle memory?
**A:** Agno provides multiple memory types: `ConversationMemory` (chat history), `SummaryMemory` (summarized context), `VectorMemory` (semantic search over past interactions), and `CustomMemory` (user-defined). Memory can be stored in-memory, in databases, or in file-based storage.

**Code:**
```python
from agno.agent import Agent
from agno.memory import Memory

agent = Agent(memory=Memory(), add_history_to_messages=True)
agent.print_response("My name is Alex.")
agent.print_response("What is my name?")
```

## Q12: What LLM providers does Agno support?
**A:** Agno supports OpenAI, Anthropic (Claude), Google (Gemini), Mistral, Cohere, Groq, Together AI, Ollama (local models), AWS Bedrock, Azure OpenAI, and other OpenAI-compatible APIs. Each provider is implemented as a model class.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google import Gemini

agents = [
    Agent(model=OpenAIChat(id="gpt-4o")),
    Agent(model=Claude(id="claude-3-5-sonnet")),
    Agent(model=Gemini(id="gemini-1.5-pro")),
]
```

## Q13: How do you switch between LLM providers in Agno?
**A:** Import the desired model class and pass it to the Agent:

**Code:**
```python
from agno.models.anthropic import Claude
from agno.models.google import Gemini
agent = Agent(model=Claude(id="claude-3-opus-20240229"))
```

## Q14: What is a Team in Agno?
**A:** A Team is a group of agents that collaborate on tasks. A Team has a leader agent that delegates subtasks to member agents, coordinates their work, and synthesizes results. This enables complex multi-agent collaboration patterns.

**Code:**
```python
from agno.team import Team
from agno.agent import Agent

coordinator = Agent(name="Coordinator", instructions="Delegate subtasks.")
researcher = Agent(name="Researcher", instructions="Gather facts.")
writer = Agent(name="Writer", instructions="Compose the final answer.")

team = Team(leader=coordinator, members=[researcher, writer])
team.print_response("Explain how multi-agent teams work.")
```

## Q15: How do you create a multi-agent Team in Agno?
**A:** Create individual agents, then create a Team with a leader and members:

**Code:**
```python
from agno.team import Team
team = Team(
    leader=coordinator_agent,
    members=[researcher_agent, writer_agent, reviewer_agent],
)
team.print_response("Research and write an article about AI.")
```

## Q16: What is the difference between an Agent and a Workflow in Agno?
**A:** An Agent is an autonomous entity that decides its own steps to complete a task. A Workflow is a predefined sequence of steps. Agents are flexible but less predictable; Workflows are structured but rigid. They can be combined for hybrid approaches.

**Code:**
```python
from agno.agent import Agent
from agno.workflow import Workflow

agent = Agent(instructions=["Adapt and choose your own steps."])

class FixedWorkflow(Workflow):
    description = "A rigid, predefined sequence."

    def run(self, data: str) -> str:
        return f"processed: {data}"

print(agent.description, "|", FixedWorkflow().description)
```

## Q17: How does Agno handle streaming responses?
**A:** Agno supports streaming via async generators. Use `agent.run_stream(prompt)` which yields response chunks. The `print_response` method automatically streams when the model supports it. Streaming works for both text and tool calls.

**Code:**
```python
from agno.agent import Agent

agent = Agent(description="Streaming assistant.")
for chunk in agent.run_stream("Tell me a short story."):
    print(chunk.content, end="")
```

## Q18: What is structured output in Agno?
**A:** Structured output forces the agent to return responses matching a Pydantic model schema. This ensures type-safe, parseable outputs:

**Code:**
```python
from pydantic import BaseModel
class MovieReview(BaseModel):
    title: str
    rating: int
    summary: str
response: MovieReview = agent.run("Review Inception", response_model=MovieReview)
```

## Q19: How does Agno handle tool calling?
**A:** Agno automatically converts Python functions (with type hints and docstrings) into tool definitions that the LLM can use. When the LLM decides to call a tool, Agno executes the function, captures the result, and returns it to the LLM for further reasoning.

**Code:**
```python
from agno.agent import Agent

def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

agent = Agent(tools=[add], show_tool_calls=True)
agent.print_response("What is 12 + 30?")
```

## Q20: What is the Agno Run loop?
**A:** The Run loop is the core execution cycle: receive input → reason (LLM call) → decide (tool use or respond) → execute (tool) → observe (get results) → repeat until complete → return final response. This implements the ReAct pattern by default.

**Code:**
```python
from agno.agent import Agent

def lookup(query: str) -> str:
    """Look up a query in a knowledge source."""
    return f"Result for {query}"

# Run loop: input -> reason -> decide -> execute -> observe -> repeat -> respond
agent = Agent(tools=[lookup], show_tool_calls=True)
agent.print_response("Look up the term 'ReAct'.")
```

## Q21: How do you save and load agent state in Agno?
**A:** Agent state (memory, conversation history) can be serialized to JSON and restored. Use `agent.to_dict()` for export and `agent.from_dict(data)` for import. Session management is also supported for persistent conversations.

**Code:**
```python
from agno.agent import Agent

agent = Agent(description="Stateful agent.")
state = agent.to_dict()          # export the conversation state
restored = Agent.from_dict(state)  # restore it into a new instance
```

## Q22: What is the Agno session system?
**A:** Sessions enable persistent conversations with agents. Each session has a unique ID, stores conversation history, and can be resumed. Sessions are managed by session stores (in-memory, database, or custom implementations).

**Code:**
```python
from agno.agent import Agent
from agno.storage.sqlite import SqliteStorage

storage = SqliteStorage(table_name="sessions", db_file="agents.db")
agent = Agent(storage=storage)
first = agent.run("Start a session.")
agent.run("Continue the session.", session_id=first.session_id)
```

## Q23: How do you create a RAG agent in Agno?
**A:** Combine a knowledge base with an agent:

**Code:**
```python
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
agent = Agent(
    knowledge=PDFKnowledgeBase(path="docs/", vector_db=ChromaDB()),
    add_references_to_prompt=True,
)
```

## Q24: What embedding models does Agno support?
**A:** Agno supports OpenAI embeddings, Google embeddings, SentenceTransformers, HuggingFace models, Ollama embeddings, and custom embedding functions through the embedding interface.

**Code:**
```python
from agno.agent import Agent

def get_capital(country: str) -> str:
    """Return the capital of a country."""
    return {"France": "Paris", "Japan": "Tokyo"}.get(country, "Unknown")

agent = Agent(
    tools=[get_capital],
    description="Answers geography questions.",
    show_tool_calls=True,
)
agent.print_response("What is the capital of Japan?")
```

## Q25: How do you add web search capability to an Agno agent?
**A:** Use a search tool like DuckDuckGo or a custom search function:

**Code:**
```python
from agno.tools.duckduckgo import DuckDuckGoTools
agent = Agent(tools=[DuckDuckGoTools()])
```

## Q26: What is the Agno tool interface?
**A:** The tool interface defines how tools are structured. A tool is a Python function with typed parameters and a docstring. For complex tools, you can use the `Tool` class with custom `run` methods, error handling, and configuration.

**Code:**
```python
import asyncio
from agno.agent import Agent

async def ask_model():
    agent = Agent(description="Async echo agent.")
    response = await agent.arun("Hello from async!")
    print(response.content)

asyncio.run(ask_model())
```

## Q27: How does Agno handle API keys and secrets?
**A:** Agno reads API keys from environment variables by convention (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). Keys can also be passed directly as parameters but this is discouraged for security reasons.

**Code:**
```python
from agno.memory import Memory
from agno.agent import Agent

def remember_fact(text: str) -> str:
    """Store a remembered fact about the user."""
    return f"Remembered: {text}"

agent = Agent(
    tools=[remember_fact],
    memory=Memory(),
    enable_memory=True,
)
agent.print_response("Remember that I like hiking.")
```

## Q28: What is the Agno model interface?
**A:** The model interface defines how Agno interacts with LLMs. Each provider implements `invoke(prompt)`, `invoke_stream(prompt)`, `embed(texts)`, and configuration methods. This abstraction allows easy switching between providers.

**Code:**
```python
from agno.agent import Agent

def convert_temperature(value: float, scale: str) -> str:
    """Convert a temperature across scales."""
    return f"{value} {scale}"

agent = Agent(
    tools=[convert_temperature],
    description="A single-tool temperature converter.",
    show_tool_calls=True,
)
agent.print_response("Convert 100 C to F.")
```

## Q29: How do you use local models with Agno?
**A:** Use the Ollama integration to run local models:

**Code:**
```python
from agno.models.ollama import Ollama
agent = Agent(model=Ollama(id="llama3"))
```

## Q30: What are Agno vector databases?
**A:** Vector databases store embeddings for semantic search. Agno supports Pinecone, Weaviate, Qdrant, Chroma, Milvus, pgvector, and LanceDB. Each has a consistent interface for upsert, search, and delete operations.

**Code:**
```python
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.pineconedb import PineconeDB

db = ChromaDb(collection="docs")
db.create()
db.upsert(vectors=[vec1, vec2], documents=[doc1, doc2])
hits = db.search(query_vector, limit=5)
print(len(hits))
```

## Q31: How does Agno implement the ReAct pattern?
**A:** ReAct (Reasoning + Acting) is the default agent execution pattern: the agent receives input, thinks/reasons (generates a thought), acts (calls a tool if needed), observes the result, and continues until it has enough information to respond.

**Code:**
```python
from agno.agent import Agent

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# ReAct: reason -> act (tool call) -> observe -> respond
agent = Agent(tools=[multiply], show_tool_calls=True)
agent.print_response("What is 6 * 7?")
```

## Q32: What is the Agno debug mode?
**A:** Enable debug mode with `agent.print_response(..., debug_mode=True)` or by setting logging level. Debug mode shows the agent's internal reasoning, tool calls, token usage, timing, and full conversation context.

**Code:**
```python
from agno.agent import Agent

agent = Agent(description="Debugging demo.")
agent.print_response("Hello", debug_mode=True)
```

## Q33: How do you test Agno agents?
**A:** Agno agents can be tested with pytest by mocking LLM responses or using deterministic models. The `agno.testing` module provides utilities for creating test fixtures, assertions on tool calls, and validating structured outputs.

**Code:**
```python
import pytest
from agno.agent import Agent

@pytest.mark.asyncio
async def test_agent_replies():
    agent = Agent(description="Test agent.")
    response = await agent.arun("Hello")
    assert response.content
```

## Q34: What is the Agno function call system?
**A:** Agno automatically generates JSON schemas from Python function signatures (using type hints, docstrings, and Pydantic models) that are passed to the LLM as tool definitions. The system handles parameter validation, error handling, and result formatting.

**Code:**
```python
from agno.agent import Agent

def book_flight(origin: str, destination: str) -> str:
    """Book a flight between two cities."""
    return f"Booked {origin} -> {destination}"

agent = Agent(tools=[book_flight], show_tool_calls=True)
agent.print_response("Book a flight from NYC to London.")
```

## Q35: How do you chain multiple agents in Agno?
**A:** Pass the output of one agent as input to another, or use a Team for coordinated multi-agent execution. Workflows can also chain agents with explicit step definitions.

**Code:**
```python
from agno.agent import Agent

planner = Agent(description="Creates outlines.")
writer = Agent(description="Writes final text.")

outline = planner.run("Create an outline about AI.")
article = writer.run(f"Expand this outline: {outline.content}")
print(article.content)
```

## Q36: What is context management in Agno agents?
**A:** Context management controls how much conversation history is preserved. Options include sliding windows (last N messages), token-based truncation, summary-based compression, and vector search over historical interactions.

**Code:**
```python
from agno.agent import Agent

# Sliding window context: a bounded deque of recent messages
from collections import deque

history = deque(maxlen=10)  # keeps the last 10 messages
history.append({"role": "user", "content": "Hello"})
history.append({"role": "assistant", "content": "Hi!"})
print(list(history))
```

## Q37: How does Agno handle concurrent agent execution?
**A:** Agno supports concurrent execution via Python's asyncio. Async variants (`arun`, `arun_stream`) allow running multiple agents simultaneously. Teams handle concurrency internally for member agents.

**Code:**
```python
import asyncio
from agno.agent import Agent

async def run_tasks():
    agent = Agent(description="Concurrent agent.")
    results = await asyncio.gather(
        agent.arun("Task A"), agent.arun("Task B")
    )
    print([r.content for r in results])

asyncio.run(run_tasks())
```

## Q38: What is the Agno agent configuration?
**A:** Agent configuration includes model selection, system prompt, temperature, max tokens, tool list, knowledge base, memory settings, response format, timeout, retry settings, and metadata tags.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"{city}: sunny"

agent = Agent(
    model=OpenAIChat(id="gpt-4o", temperature=0.7),
    tools=[get_weather],
    instructions=["Be concise."],
    add_history_to_messages=True,
    debug_mode=False,
)
```

## Q39: How do you customize an agent's system prompt in Agno?
**A:** Pass a custom system prompt string or a list of prompt instructions:

**Code:**
```python
agent = Agent(
    instructions=["You are a helpful assistant.", "Always cite your sources."],
    system_prompt="Custom system prompt here"
)
```

## Q40: What is the Agno document loader?
**A:** The document loader loads files from various formats into a common document structure. Supported formats include PDF, DOCX, HTML, Markdown, CSV, JSON, plain text, and more. Loaders handle chunking, metadata extraction, and cleaning.

**Code:**
```python
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.url import UrlKnowledgeBase

pdf_kb = PDFKnowledgeBase(path="docs/")
url_kb = UrlKnowledgeBase(urls=["https://docs.agno.com"])
pdf_kb.load()
url_kb.load()
print(len(pdf_kb.documents), len(url_kb.documents))
```

## Q41: How do you use Agno with FastAPI?
**A:** Create an agent instance and expose it via FastAPI endpoints:

**Code:**
```python
from fastapi import FastAPI
app = FastAPI()
agent = Agent(...)
@app.post("/chat")
async def chat(message: str):
    response = await agent.arun(message)
    return {"response": response.content}
```

## Q42: What are Agno text splitters?
**A:** Text splitters break documents into chunks for embedding and retrieval. Supported strategies include recursive character splitting, token-based splitting, semantic splitting, and fixed-size chunking with configurable overlap.

**Code:**
```python
from agno.document import Document

doc = Document(name="guide", content=("Agno makes agents simple. ") * 200)
chunks = doc.chunk_text(chunk_size=800, overlap=100)
print(len(chunks))
```

## Q43: How does Agno handle token limits?
**A:** Agno monitors token usage per agent run. Configuration includes `max_tokens` for responses, context window management that trims history when approaching limits, and token counting utilities for estimation.

**Code:**
```python
from agno.models.openai import OpenAIChat

model = OpenAIChat(id="gpt-4o", max_tokens=128)
agent = Agent(model=model)
print(agent.model.max_tokens)
```

## Q44: What is the Agno scoring system?
**A:** Agents can score/rank retrieved documents or generated responses using relevance scoring, confidence scores, or custom scoring functions. This is used in knowledge retrieval to return only the most relevant context.

**Code:**
```python
from agno.vectordb.pineconedb import PineconeDB

db = PineconeDB(index_name="scored")
results = db.search(query_vector, limit=5)
ranked = sorted(results, key=lambda d: d.score, reverse=True)
print([r.score for r in ranked])
```

## Q45: How do you add image understanding to Agno agents?
**A:** Pass images as part of the message content using multi-modal models:

**Code:**
```python
from agno.media import Image
response = agent.run("Describe this image", images=[Image(url="https://example.com/photo.jpg")])
```

## Q46: What is the Agno response model?
**A:** The response model (Pydantic) defines the structure of the agent's output. When set, the agent must respond with valid JSON matching the schema. This enables type-safe, parseable, and validated outputs from any LLM.

**Code:**
```python
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class Movie(BaseModel):
    title: str
    rating: int

agent = Agent(model=OpenAIChat(id="gpt-4o"))
response: Movie = agent.run("Review Inception.", response_model=Movie)
print(response.title, response.rating)
```

## Q47: How does Agno handle retries and error recovery?
**A:** Agno implements exponential backoff retry for API calls, configurable max retry attempts, graceful degradation when tools fail, and error messages in the agent's reasoning loop for self-correction.

**Code:**
```python
from agno.agent import Agent

agent = Agent(
    description="Retries tool calls with backoff.",
    retries=3,
    show_tool_calls=True,
)
agent.print_response("Hello")
```

## Q48: What is the Agno telemetry system?
**A:** Agno includes built-in telemetry for monitoring agent runs: token usage, latency, tool call frequency, error rates, and cost tracking. This data can be exported to monitoring platforms or viewed via the Agno dashboard.

**Code:**
```python
from agno.agent import Agent

agent = Agent(description="Instrumented agent.", debug_mode=True)
response = agent.run("Track this run.")
print(response.metrics)
```

## Q49: How do you create a retrieval agent in Agno?
**A:** A retrieval agent combines a knowledge base with retrieval tools:

**Code:**
```python
agent = Agent(
    knowledge_base=my_knowledge_base,
    retrieve=my_retriever,
    add_references_to_prompt=True,
)
```

## Q50: What are Agno data sources?
**A:** Data sources define where knowledge comes from: local files (PDF, DOCX), web pages, databases, APIs, S3 buckets, Notion, Confluence, GitHub repositories, and more. Each source has a loader and parser implementation.

**Code:**
```python
from agno.knowledge.url import UrlKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase

sources = [
    UrlKnowledgeBase(urls=["https://docs.agno.com"]),
    PdfKnowledgeBase(path="data/"),
]
```

## Q51: How does Agno handle authentication in tools?
**A:** Tools receive credentials via environment variables, constructor parameters, or a credentials registry. The agent passes necessary authentication context when calling tools, and sensitive data is never exposed in the reasoning trace.

**Code:**
```python
from agno.team.team import Team
from agno.agent import Agent

lead = Agent(name="Lead", description="Coordinates tasks.")
researcher = Agent(name="Researcher", description="Finds facts.")

team = Team(name="Research Team", members=[lead, researcher])
team.print_response("What is the capital of France?")
```

## Q52: What is the Agno agent template?
**A:** Agent templates are reusable agent configurations with predefined instructions, tools, and knowledge. Templates can be shared, forked, and customized. They serve as starting points for common use cases.

**Code:**
```python
from agno.agent import Agent

def add_one(x: int) -> int:
    """Increment an integer."""
    return x + 1

agent = Agent(tools=[add_one], show_tool_calls=True)
agent.print_response("Compute 1 + 1 using the add_one tool.")
```

## Q53: How do you run Agno agents in production?
**A:** Production deployment involves: containerizing with Docker, using async execution for scalability, implementing proper error handling and logging, configuring rate limits, setting up monitoring, and using persistent session storage.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.agent import Agent

models = ["gpt-4o", "gpt-4o-mini"]
for model_id in models:
    agent = Agent(model=OpenAIChat(id=model_id))
    response = agent.run("Hello")
    print(model_id, response.content)
```

## Q54: What is the Agno model market?
**A:** The model market is a registry where model providers publish pricing, capabilities, performance benchmarks, and supported features. Agents can use this to make cost-aware decisions about which model to use for each task.

**Code:**
```python
from agno.agent import Agent
from agno.utils.log import logger

logger.debug("Agent will start.")
agent = Agent(description="Logging demo.")
agent.print_response("Hello")
logger.info("Agent done.")
```

## Q55: How does Agno implement guardrails?
**A:** Guardrails are implemented as pre-processing hooks (input validation, prompt injection detection) and post-processing hooks (output filtering, PII redaction, content safety checks). Custom guardrails can be added via the guardrail interface.

**Code:**
```python
from agno.agent import Agent

def rotate(text: str) -> str:
    """Rot13-encode the text."""
    return text.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "nopqrstuvwxyzabcdefghijklm"))

agent = Agent(tools=[rotate], show_tool_calls=True)
agent.print_response("Encode 'hello' with rotate.")
```

## Q56: What is the Agno agent benchmark?
**A:** The benchmark tool evaluates agents on standard metrics: task completion rate, accuracy, latency, cost, tool call efficiency, and failure recovery. It supports custom test datasets and comparison reports.

**Code:**
```python
from agno.agent import Agent

def get_timezone(city: str) -> str:
    """Return the IANA timezone for a city."""
    return {"Oslo": "Europe/Oslo", "Tokyo": "Asia/Tokyo"}.get(city, "UTC")

def get_time(timezone: str) -> str:
    """Get the current local time for a timezone."""
    return f"It is 12:00 in {timezone}"

agent = Agent(tools=[get_timezone, get_time], show_tool_calls=True)
agent.print_response("What time is it in Tokyo?")
```

## Q57: How do you contribute to the Agno project?
**A:** Contributions include code changes (bug fixes, features), documentation, examples, tutorials, model provider integrations, tool contributions, and community support. Follow the CONTRIBUTING.md guidelines, use conventional commits, and submit PRs.

**Code:**
```python
from agno.agent import Agent

def email_task(topic: str) -> str:
    """Draft a short email about a topic."""
    return f"Subject: {topic.title()}\n\nPlease review the latest updates."

agent = Agent(tools=[email_task])
agent.print_response("Draft an email about the quarterly report.")
```

## Q58: What testing framework is used in Agno?
**A:** Agno uses pytest for testing with pytest-asyncio for async tests, pytest-mock for mocking, and the `agno.testing` module for agent-specific test utilities and fixtures.

**Code:**
```python
from agno.storage.agent.sqlite import SqliteAgentStorage

storage = SqliteAgentStorage(table_name="agent_sessions", db_file="agent.db")
print(storage.table_name)
```

## Q59: What is the Agno workflow DSL?
**A:** The workflow DSL (Domain Specific Language) allows defining multi-step workflows declaratively using decorators and function composition. Steps can include conditional logic, parallel execution, retry policies, and timeout configurations.

**Code:**
```python
from agno.document import Document
from agno.splitter.tokenizer import Tokenizer

tokenizer = Tokenizer()
tokens = tokenizer.normalize("Hello world, this is Agno.")
print(tokens)
```

## Q60: How does Agno handle versioning?
**A:** Agno follows semantic versioning. The Python package version is in `__version__`. Breaking changes are documented in changelog. Agent configurations can specify model versions and tool versions for reproducibility.

**Code:**
```python
import asyncio
from agno.agent import Agent

async def stream_reply():
    agent = Agent(description="Streaming agent.")
    async for chunk in agent.arun_stream("Tell me about Agno."):
        print(chunk.content, end="", flush=True)

asyncio.run(stream_reply())
```

## Q61: What is the Agno model capabilities system?
**A:** Each model provider declares capabilities (streaming, tool use, vision, structured output, function calling, etc.). Agents can check capabilities at runtime and adapt their behavior or fallback to alternative models.

**Code:**
```python
from agno.agent import Agent

def lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()

agent = Agent(tools=[lowercase], show_tool_calls=True)
agent.print_response("Lowercase 'HELLO'.")
```

## Q62: How do you implement custom memory in Agno?
**A:** Implement the `Memory` interface with methods for `add_message`, `get_messages`, `clear`, and `search`. Custom memory can store to databases, files, or external services. Register it with the agent via the `memory` parameter.

**Code:**
```python
from agno.storage.agent.sqlite import SqliteAgentStorage

storage = SqliteAgentStorage(table_name="interrupted_runs", db_file="agent.db")

def resume(run_id: str):
    agent = Agent(storage=storage, add_history_to_messages=True)
    return agent.run("Continue where we left off", session_id=run_id)

print(resume("session-123"))
```

## Q63: What is the Agno session persistence?
**A:** Session persistence saves conversation state (messages, context, metadata) between runs. Supported backends include in-memory (default), SQLite, PostgreSQL, Redis, and custom implementations. Sessions are identified by unique IDs.

**Code:**
```python
from agno.models.ollama import Ollama
from agno.agent import Agent

agent = Agent(model=Ollama(id="llama3.2"))
agent.print_response("Hello from Ollama!")
```

## Q64: How does Agno handle prompt versioning?
**A:** Prompts can be versioned by storing them externally with version tags. The agent can reference specific prompt versions, enabling A/B testing, gradual rollouts, and rollback of prompt changes.

**Code:**
```python
from agno.agent import Agent

def add_task(task: str) -> str:
    """Add a task to a shared todo list."""
    return f"Added: {task}"

agent = Agent(tools=[add_task])
agent.print_response("Add 'buy milk' to the list.")
```

## Q65: What are Agno agents with vision capability?
**A:** Vision agents can process and analyze images using multi-modal models (GPT-4V, Gemini, Claude 3). They accept image URLs or base64-encoded images alongside text prompts for tasks like image description, analysis, and document understanding.

**Code:**
```python
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class User(BaseModel):
    name: str
    email: str

agent = Agent(model=OpenAIChat(id="gpt-4o"))
user: User = agent.run("Create a user for Ana.", response_model=User)
print(user.model_dump())
```

## Q66: How do you create an agent that reads websites in Agno?
**A:** Use web scraping tools or the built-in web reader:

**Code:**
```python
from agno.tools.website import WebsiteTools
agent = Agent(tools=[WebsiteTools()])
```

## Q67: What is the Agno community ecosystem?
**A:** The community ecosystem includes community-contributed tools, model providers, knowledge sources, agent templates, and plugins. It's maintained through the Agno GitHub repository, Discord community, and documentation.

**Code:**
```python
from agno.team.team import Team
from agno.agent import Agent

qa = Agent(name="QA", description="Checks work.")
team = Team(members=[qa], enable_team_history=True, debug_mode=True)
team.print_response("Test the checkout flow.")
```

## Q68: How does Agno implement logging?
**A:** Agno uses Python's logging module with configurable levels. Logs capture agent reasoning, tool calls, errors, and performance metrics. Structured logging (JSON format) is available for production deployments.

**Code:**
```python
import asyncio
from agno.agent import Agent

async def run_agent():
    agent = Agent(description="Async spell checker.")
    response = await agent.arun("Fix the spelling.")
    return response.content

content = asyncio.run(run_agent())
print(content)
```

## Q69: What is the Agno agent serialization format?
**A:** Agents serialize to JSON format containing model configuration, tool definitions, conversation history, and metadata. This enables saving, restoring, and transferring agent state between processes or environments.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.agent import Agent

def get_rate(currency: str) -> str:
    """Return the exchange rate for a currency."""
    return {"usd": 1.0, "eur": 0.92}.get(currency.lower(), "unknown")

agent = Agent(
    model=OpenAIChat(id="gpt-4o", seed=42),
    tools=[get_rate],
)
agent.print_response("What is the eur rate?")
```

## Q70: How does Agno handle function calling with Pydantic?
**A:** Agno uses Pydantic models to define structured parameters for tool functions and agent responses. The JSON schema generated from Pydantic models is sent to the LLM, which returns structured JSON that is validated and parsed.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(model=OpenAIChat(id="gpt-4o"))
agent.print_response("hello", markdown=True, show_message=True)
```

## Q71: What is the Agno context window manager?
**A:** The context window manager tracks token usage and automatically manages the conversation history to stay within the model's context window. Strategies include summarization, truncation (removing oldest messages), and semantic pruning.

**Code:**
```python
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb.lance_db import LanceDb

vectors = OpenAIEmbedder()
db = LanceDb(embedder=vectors)
print(db.embedder.name)
```

## Q72: How do you deploy Agno on AWS?
**A:** Deploy using ECS/EKS with Docker containers, API Gateway + Lambda for serverless, or EC2 instances. Use RDS for session storage, ElastiCache for Redis, and S3 for knowledge base documents.

**Code:**
```python
from agno.workflow import Workflow, RunResponse

class SearchWorkflow(Workflow):
    def _run(self, query: str):
        return RunResponse(content=f"Results for: {query}")

workflow = SearchWorkflow()
result = workflow.run(query="agno")
print(result.content)
```

## Q73: What are Agno toolkits?
**A:** Toolkits are pre-built collections of related tools for specific domains. Examples include `ExcelToolkit` (read/write spreadsheets), `GitHubToolkit` (repo management), `SlackToolkit` (messaging), and `SQLToolkit` (database queries).

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.agent import Agent

def precision(value: float, digits: int = 2) -> float:
    """Round a float to a number of digits."""
    return round(value, digits)

agent = Agent(
    model=OpenAIChat(id="gpt-4o", top_p=0.9),
    tools=[precision],
)
agent.print_response("Round 3.14159 to 2 digits.")
```

## Q74: How does Agno handle rate limiting?
**A:** Agno implements client-side rate limiting with configurable requests-per-minute and token-per-minute limits per model provider. Rate limit detection with automatic backoff and retry is built into the provider clients.

**Code:**
```python
from agno.agent import Agent
from agno.tools import Tool

def fetch(url: str) -> str:
    """Read a webpage as text."""
    return f"Fetched content from {url}"

agents = Agent(tools=[fetch])
print(agents.tools)
```

## Q75: What is the Agno contribution workflow?
**A:** Fork the repository, create a feature branch, make changes following coding standards, write tests, run the test suite, commit with conventional commit messages, push, and open a pull request.

**Code:**
```python
from agno.models.youtube import YouTube
from agno.agent import Agent

model = YouTube(url="https://youtube.com/watch?v=9bZkp7q19f0")
agent = Agent(model=model)
agent.print_response("Summarize this video.")
```

## Q76: How do you use Agno with Docker?
**A:** Create a Dockerfile that installs Agno and dependencies, copies the application code, sets environment variables, and runs the agent or API server. Docker Compose can orchestrate multi-service deployments.

**Code:**
```python
from agno.document import Document

doc = Document(name="constitution")
content = doc.md_content or ""
print(doc.name, len(content))
```

## Q77: What is the Agno monitoring dashboard?
**A:** The monitoring dashboard provides real-time visibility into agent performance: active sessions, latency percentiles, error rates, token usage, cost accumulation, and tool call distribution. It's available as a web UI.

**Code:**
```python
from agno.models.groq import Groq
from agno.agent import Agent

agent = Agent(model=Groq(id="llama-3.1-70b-versatile"))
agent.print_response("Hello from Groq!")
```

## Q78: How does Agno implement the tool calling loop?
**A:** The tool calling loop: 1) LLM generates response with tool calls, 2) Agno parses tool calls, 3) validates parameters, 4) executes tool functions, 5) returns results to LLM, 6) LLM continues reasoning. This loops until the LLM decides to respond.

**Code:**
```python
from agno.agent import Agent
from agno.team.team import Team

def discount(code: str) -> str:
    """Check if a discount code is valid."""
    return "VALID" if code == "SAVE10" else "INVALID"

cart_agent = Agent(tools=[discount])
team = Team(name="Cart Team", members=[cart_agent])
team.print_response("Is code SAVE10 valid?")
```

## Q79: What are Agno agent events?
**A:** Agent events are emitted during the execution lifecycle: `on_start`, `on_tool_call`, `on_tool_result`, `on_message`, `on_error`, `on_end`. These events can be hooked for monitoring, logging, and custom side effects.

**Code:**
```python
from agno.agent import Agent
from agno.tools.file import FileTools

agent = Agent(tools=[FileTools()])
agent.print_response("Write a note.txt file with 'hello'.")
```

## Q80: How do you create an agent with multiple tools in Agno?
**A:** Pass a list of tool functions or tool objects to the Agent:

**Code:**
```python
agent = Agent(tools=[search_web, calculate, send_email, read_file], model=OpenAIChat())
```

## Q81: What is the Agno model selector?
**A:** The model selector automatically chooses the best model for a given task based on capability requirements, cost constraints, latency needs, and availability. It can implement strategies like cheapest-first or fastest-first.

**Code:**
```python
from agno.models.azure.openai_chat import AzureOpenAI
from agno.agent import Agent

agent = Agent(model=AzureOpenAI(id="gpt-4o", api_version="2024-02-01"))
agent.print_response("Hello from Azure!")
```

## Q82: How does Agno handle audio processing?
**A:** Audio processing is supported via specialized tools (speech-to-text, text-to-speech) and multi-modal models. The audio tools interface with providers like OpenAI Whisper, ElevenLabs, or local models.

**Code:**
```python
from agno.agent import Agent

agent = Agent(
    description="Agent with prepared prompts prefixing the model call.",
    add_history_to_messages=True,
)
agent.print_response("What can you do?")
```

## Q83: What is the Agno package structure?
**A:** The package is organized into modules: `agno.agent` (agent core), `agno.models` (LLM providers), `agno.tools` (tool implementations), `agno.knowledge` (knowledge base), `agno.vectordb` (vector stores), `agno.media` (multi-modal), `agno.team` (multi-agent).

**Code:**
```python
from agno.knowledge.langchain import LangChainKnowledgeBase

def build_knowledge_base():
    kb = LangChainKnowledgeBase()
    return kb

print(build_knowledge_base())
```

## Q84: How do you run Agno agents on a schedule?
**A:** Use external schedulers (cron, APScheduler, Celery Beat) combined with Agno's session persistence. Create a scheduled task that initializes the agent, runs it with predefined inputs, and stores results.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.embedder.openai import OpenAIEmbedder

model = OpenAIChat(id="gpt-4o")

ai_embedder = OpenAIEmbedder()
vector = ai_embedder.get_embedding("agno")
print(len(vector))
```

## Q85: What is the Agno agent builder?
**A:** The agent builder is a UI tool (optional web interface) for visually creating, configuring, and testing Agno agents without writing code. It generates the Python configuration code for the configured agent.

**Code:**
```python
from agno.page.extractor import Extractor
from urllib.request import urlopen

def extract():
    with urlopen("https://docs.agno.com") as f:
        html = f.read().decode("utf-8")
    return Extractor.extract_from_html(html)

print(extract()[:80])
```

## Q86: How does Agno handle streaming from tools?
**A:** Tools can be implemented as async generators that yield intermediate results. These results are streamed to the user alongside the agent's thought process, providing real-time visibility into tool execution progress.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    reasoning_effort="high",
)
agent.print_response("Solve 2+2 and explain.")
```

## Q87: What is the Agno agent memory format?
**A:** Memory is stored as a list of message dicts or Message objects, each with role (system/user/assistant/tool), content, metadata, and optional tool call information. Memory supports both text and multi-modal content.

**Code:**
```python
import inspect
from agno.agent import Agent

def convert_celsius(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32

print(inspect.signature(convert_celsius))
```

## Q88: How do you integrate external APIs with Agno?
**A:** Create tool functions that wrap API calls, using requests/aiohttp for HTTP calls. Pass API credentials via environment variables or the tool's constructor. Document the API parameters in the tool's docstring for the LLM.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

storage = SqliteAgentStorage(table_name="chat_history", db_file="chat.db")
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    storage=storage,
    add_history_to_messages=True,
)
agent.print_response("Remember this: buy milk.")
```

## Q89: What is the Agno model adapter pattern?
**A:** The model adapter pattern provides a uniform interface across different LLM providers. Each provider implements a common abstract class, normalizing differences in API formats, streaming behavior, tool calling, and error handling.

**Code:**
```python
from agno.agent import Agent

def count_unique(words: list) -> int:
    """Count the number of unique words."""
    return len(set(words))

agent = Agent(tools=[count_unique], show_tool_calls=True)
agent.print_response("Count unique words in ['a','b','a'].")
```

## Q90: How does Agno handle PII detection and redaction?
**A:** PII detection can be implemented as a pre/post-processing guardrail using regex patterns, NLP-based detection (spaCy, presidio), or LLM-based identification. Redaction replaces detected PII with placeholder tokens.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.agent import Agent

agent = Agent(
    model=OpenAIChat(
        id="gpt-4o",
        response_format={"type": "json_object"},
    ),
)
agent.print_response('Return JSON: {"ok": true}')
```

## Q91: What are Agno run modes?
**A:** Run modes include: `sync` (blocking), `async` (non-blocking with asyncio), `stream` (token-by-token output), and `auto` (smart defaults based on context). Run modes affect how `agent.run()` and `agent.arun()` behave.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.message import Message

MENTOR = Message.system("You are a patient mentor.")
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    prompt_messages=[MENTOR],
)
agent.print_response("Teach me Python.")
```

## Q92: How do you contribute a new model provider to Agno?
**A:** Implement the model interface (extend `Model` base class), implement required methods (invoke, invoke_stream, embed), add tests, register the provider, document usage, and submit a PR with example code.

**Code:**
```python
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.mistral import MistralChat

class Result(BaseModel):
    result: bool

agent = Agent(model=MistralChat(id="mistral-large-latest"))
payload: Result = agent.run("Is 2 even?", response_model=Result)
print(payload.result)
```

## Q93: What is the Agno agent template repository?
**A:** The template repository on GitHub contains ready-to-use agent configurations for common use cases: customer support, document analysis, code review, research assistant, data extraction, and more.

**Code:**
```python
from agno.agent import Agent
from agno.tools import Tool

def cad_module_count(value) -> str:
    """Count occurrences of 'cad' in a string."""
    return str(value.lower().count("cad"))

agent = Agent(tools=[cad_module_count])
agent.print_response("How many 'cad' in 'cascade cad cadbury'?")
```

## Q94: How does Agno handle tool conflicts?
**A:** Tool conflicts (same name/duplicates) are resolved by namespace prefixing or explicit naming. The agent's tool registry ensures unique tool names and validates tool schemas for consistency.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(model=OpenAIChat(id="gpt-4o", max_tokens=50))
agent.print_response("Respond with a single word.")
```

## Q95: What is the Agno knowledge base update strategy?
**A:** Knowledge bases support full rebuild (re-index all documents), incremental update (add/update specific documents), and scheduled refresh. Update strategies include overwrite, merge, and versioned additions.

**Code:**
```python
from agno.agent import Agent

def currency(locale: str) -> str:
    """Return the currency for a locale."""
    return {"india": "INR", "france": "EUR"}.get(locale, "unknown")

agent = Agent(tools=[currency])
agent.print_response("What currency does France use?")
```

## Q96: How do you contribute documentation to Agno?
**A:** Documentation is stored in the `docs/` directory using Markdown with a static site generator. Contributions include fixing errors, adding examples, writing guides, translating, and improving API reference documentation.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(model=OpenAIChat(id="gpt-4o"))
response = agent.run("Hello")
print(response.content)
print(response.messages)
```

## Q97: What are Agno agent hooks?
**A:** Agent hooks are callbacks at specific lifecycle points: `before_run`, `after_run`, `before_tool`, `after_tool`, `before_llm`, `after_llm`. Hooks enable custom logic injection without modifying the agent core.

**Code:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def bank_balance(account: str) -> str:
    """Return the balance for an account."""
    return "1000"

agent = Agent(model=OpenAIChat(id="gpt-4o"), tools=[bank_balance])
agent.print_response("Check my balance.")
```

## Q98: How does Agno ensure backward compatibility?
**A:** Agno follows semantic versioning with deprecation warnings before breaking changes. The changelog documents all changes. Migration guides are provided for major version upgrades. Deprecated features remain available for one major version.

**Code:**
```python
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class Precision(BaseModel):
    value: float

agent = Agent(model=OpenAIChat(id="gpt-4o"))
prec: Precision = agent.run(
    "Return 3.14159 rounded to 2 decimals.", response_model=Precision
)
print(prec.value)
```

## Q99: What is the Agno community and support?
**A:** The Agno community gathers on GitHub (issues, discussions), Discord (real-time chat), and Stack Overflow. Support includes documentation, tutorials, community-contributed examples, and paid enterprise support options.

**Code:**
```python
from agno.agent import Agent

agent = Agent(description="Time travel helper.")
agent.print_response("Explain timezones briefly.")
```

## Q100: What are the future directions for Agno?
**A:** Future directions include improved multi-agent orchestration patterns, enhanced memory systems, expanded model provider support, better observability tools, simplified deployment options, and deeper integration with enterprise systems.

**Code:**
```python
from agno.models.openai import OpenAIChat
from agno.agent import Agent

MOTIVATION_SYSTEM = Message.system("You start every reply with a fact.")

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    system_prompt=("Use the python interpreter tool if needed."),
    message_format=CodeEntry(
        role="python",
        image="mcr.microsoft.com/code_executor:latest",
    ),
)
agent.print_response("Hello")
```
