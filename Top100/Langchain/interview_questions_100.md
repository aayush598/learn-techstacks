# LangChain — 100 Interview Q&A
> Based on real-world LLM application development, RAG pipelines, agent architectures, and production deployment patterns using LangChain v0.3+.

---

## 1. Core Concepts & Architecture (Q1–Q20)

**Q1: What is LangChain and what problem does it solve?**
A: LangChain is a framework for building LLM-powered applications. It solves: 1) abstracting LLM provider APIs (OpenAI, Anthropic, local models), 2) composing multiple LLM calls via chains, 3) integrating external data (RAG), 4) building agents with tool use, and 5) managing prompts, memory, and output parsing. It provides a unified interface for pattern composition.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# One unified interface over many providers (OpenAI, Anthropic, Ollama...)
model = ChatOpenAI(model="gpt-4o-mini")
reply = model.invoke([HumanMessage(content="What is LangChain?")])
print(reply.content)
```

**Q2: Explain the core abstractions in LangChain: Model, Prompt, Output Parser, Chain, and Agent.**
A: 
- Model: wrapper around LLM providers (ChatOpenAI, Anthropic, Ollama)
- Prompt: template for constructing LLM inputs (PromptTemplate, ChatPromptTemplate)
- Output Parser: structures LLM output (StrOutputParser, PydanticOutputParser, JsonOutputParser)
- Chain: sequence of steps (LLM + prompt + parser or multiple LLMs piped together)
- Agent: LLM that decides which tools to call, loops until task complete

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4o-mini")                      # Model
prompt = ChatPromptTemplate.from_messages([("human", "{input}")])  # Prompt
parser = StrOutputParser()                                    # Output Parser
chain = prompt | model | parser                               # Chain (LCEL)
print(chain.invoke({"input": "Hello!"}))                      # Agent would add tools/memory
```

**Q3: What is LCEL (LangChain Expression Language) and why is it important?**
A: LCEL is a declarative syntax (using `|` pipe operator) to compose LangChain components into chains. It provides built-in streaming, async support, batch, parallel execution, retries, and LangSmith tracing. Example: `chain = prompt | model | parser`. LCEL is the recommended way to build chains in LangChain v0.2+.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = (ChatPromptTemplate.from_messages([("human", "Tell a joke about {topic}")])
         | ChatOpenAI(model="gpt-4o-mini")
         | StrOutputParser())
for chunk in chain.stream({"topic": "anything"}):   # built-in streaming
    print(chunk, end="", flush=True)
```

**Q4: Explain the difference between ChatModels and LLMs (completion models) in LangChain.**
A: ChatModels (ChatOpenAI, ChatAnthropic) exchange messages (SystemMessage, HumanMessage, AIMessage) — they use chat-based APIs. LLMs (OpenAI, Anthropic) accept string input and return string output — completion APIs. LangChain v0.3+ focuses on ChatModels. Use ChatModels unless you need legacy completion endpoints.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

chat = ChatOpenAI(model="gpt-4o-mini")  # ChatModel: message-based API
response = chat.invoke([
    SystemMessage(content="You are a concise assistant."),
    HumanMessage(content="Say hi in one word"),
])
print(type(response).__name__)   # AIMessage, not a plain string
print(response.content)
```

**Q5: What is the concept of "Runnable" in LangChain?**
A: Runnable is the base interface that all LCEL components implement. Provides: `invoke()` (sync call), `ainvoke()` (async), `stream()`, `batch()`, `abatch()`. Runnables can be combined with `|` (pipe), composed with `RunnableSequence`, branched with `RunnableParallel`, and configured with `.configurable_fields()`. Everything in LCEL is a Runnable.

**Code:**
```python
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: x * 2)   # wraps a function as a Runnable
print(runnable.invoke(21))                    # 42
print(runnable.batch([1, 2, 3]))              # [2, 4, 6]
async for chunk in runnable.astream([5]):
    print(chunk)                              # 10 (streaming/async)
```

**Q6: What is a RunnableSequence and how does it differ from a RunnableParallel?**
A: RunnableSequence runs steps sequentially — output of step i feeds into step i+1. Built with `|` operator. RunnableParallel runs steps concurrently on the same input — outputs are merged into a dict. Example: `chain = {"context": retriever, "question": lambda x: x} | prompt | model` — retriever runs in parallel with identity passthrough.

**Code:**
```python
from langchain_core.runnables import RunnableLambda, RunnableParallel

add_one = RunnableLambda(lambda x: x + 1)
double = RunnableLambda(lambda x: x * 2)
seq = add_one | double                        # sequence: (x+1)*2
print(seq.invoke(5))                          # 12

parallel = RunnableParallel(a=add_one, b=double)  # both on same input
print(parallel.invoke(5))                     # {'a': 6, 'b': 10}
```

**Q7: What is a RunnableLambda and when would you use it?**
A: RunnableLambda wraps an arbitrary Python function as a Runnable, making it composable in LCEL. Used for: custom preprocessing/postprocessing, calling external APIs, formatting outputs, adding business logic. Example: `RunnableLambda(lambda x: x["key"].upper())`. Avoid putting heavy logic here — use as glue between LCEL components.

**Code:**
```python
from langchain_core.runnables import RunnableLambda

def enrich(query: str) -> dict:
    return {"question": query, "ts": "2026-01-01T00:00:00Z"}

chain = RunnableLambda(enrich) | RunnableLambda(lambda d: d["question"].upper())
print(chain.invoke("what is langchain"))   # WHAT IS LANGCHAIN
```

**Q8: Explain RunnablePassthrough and RunnableBranch.**
A: RunnablePassthrough: passes input through unchanged (identity) or passes specific keys. Used to forward context in parallel chains. RunnableBranch: conditional chain routing — like if-elif-else in LCEL. Each branch is a (predicate, runnable) pair. Example: route short queries to fast model, long queries to powerful model.

**Code:**
```python
from langchain_core.runnables import RunnablePassthrough, RunnableBranch, RunnableLambda

fast = RunnableLambda(lambda q: f"short: {q}")
deep = RunnableLambda(lambda q: f"deep: {q}")
branch = RunnableBranch((lambda q: len(q) < 10, fast), deep)
print(branch.invoke("short query"))              # short: short query
print(branch.invoke("a much longer detailed query that needs deep model"))
print(RunnablePassthrough().invoke("untouched"))
```

**Q9: How does LangChain handle streaming with LCEL?**
A: Any LCEL chain supports `.stream()` if all components support streaming. Token-by-token for LLMs + parsed output streaming for parsers. Implemented via Runnable's `stream()` method which yields chunks. For final output parsing, LangChain buffers tokens and emits parsed chunks. Async streaming with `astream()`.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = (ChatPromptTemplate.from_messages([("human", "{input}")])
         | ChatOpenAI(model="gpt-4o-mini")
         | StrOutputParser())
for token in chain.stream({"input": "Say the alphabet"}):
    print(token, end="", flush=True)          # token-by-token
import asyncio
async def main():
    async for token in chain.astream({"input": "Hi"}):
        print(token, end="", flush=True)
asyncio.run(main())
```

**Q10: What is LangSmith and how does it integrate with LangChain?**
A: LangSmith is LangChain's observability platform for LLM apps. It traces every run (LLM calls, retrievals, chains), logs inputs/outputs, measures latency/token usage, and supports evaluation/testing. Integrated via `LANGCHAIN_TRACING_V2=true` environment variable. Essential for debugging complex chains and monitoring production.

**Code:**
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_yourapikey"
os.environ["LANGCHAIN_PROJECT"] = "my-rag"

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

model = ChatOpenAI(model="gpt-4o-mini")
result = model.invoke([HumanMessage(content="Trace this call")])
print(result.content)   # every invocation is now logged in LangSmith
```

**Q11: What is LangServe and when would you use it?**
A: LangServe deploys LangChain chains as REST APIs with auto-generated FastAPI endpoints. Provides: `/invoke`, `/stream`, `/batch` endpoints, auto-generated OpenAPI/Swagger docs, input/output schemas, and client SDK generation. Used to expose chains as microservices. Deploy via `langchain serve` or programmatically with FastAPI.

**Code:**
```python
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

app = FastAPI(title="My Chain")
chain = (ChatPromptTemplate.from_messages([("human", "{question}")])
         | ChatOpenAI(model="gpt-4o-mini")
         | StrOutputParser())
add_routes(app, chain, path="/qa")   # -> /qa/invoke, /qa/stream, /qa/batch

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Q12: Explain the different types of prompt templates in LangChain.**
A: 
- PromptTemplate: for string-based LLMs `"Tell me about {topic}"`
- ChatPromptTemplate: for chat models, composed of message templates
- MessagesPlaceholder: inserts variable-length messages (history, tool results)
- FewShotPromptTemplate: few-shot examples with example selector
- PipelinePromptTemplate: combine multiple templates
- DynamicPrompt: templates that change based on input

**Code:**
```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

string_t = PromptTemplate.from_template("Tell me about {topic}")
chat_t = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])
print(string_t.format(topic="RAG"))
print(chat_t.format(role="teacher", chat_history=[], question="What is RAG?"))
```

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

**Code:**
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
messages = prompt.invoke({
    "role": "helpful",
    "chat_history": [HumanMessage(content="Hi"), AIMessage(content="Hello!")],
    "input": "What is LCEL?",
}).to_messages()
print(messages)   # system + 2 history turns + human
```

**Q14: How does LangChain handle tool calling with LLMs?**
A: LangChain defines tools via `@tool` decorator, Tool class, or BaseTool subclass. Tools have: name, description, args_schema (JSONSchema), and a `_run` method. LLMs that support tool calling (OpenAI, Anthropic, Gemini) receive tools in the API call. The LLM returns tool_calls in AIMessage, which LangChain dispatches to tools.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

model = ChatOpenAI(model="gpt-4o-mini").bind_tools([add])
resp = model.invoke("What is 2 + 3?")
print(resp.tool_calls)   # [{'name': 'add', 'args': {'a': 2, 'b': 3}, ...}]
```

**Q15: What is a @tool decorator and what are its key parameters?**
A: `@tool` decorates a function as a LangChain tool:
```python
@tool
def search(query: str) -> str: ...
```
Key params: `name`, `description` (used by LLM to choose tool), `return_direct` (return tool output to user without LLM), `args_schema` (pydantic model for parameter validation), `response_format` ("content" or "content_and_artifact").

**Code:**
```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class SearchArgs(BaseModel):
    query: str = Field(description="the search term")

@tool("web_search", args_schema=SearchArgs, return_direct=False)
def search(query: str) -> str:
    """Search the web for {query}."""
    return f"results for: {query}"

print(search.name, search.description, search.args_schema)
print(search.invoke({"query": "langchain"}))
```

**Q16: What is the ToolMessage type and when is it used?**
A: ToolMessage represents the result of a tool call, sent back to the LLM. Contains: content (result string), tool_call_id (matches the tool_call that triggered it), name, and optional artifact. In agent loops, after tool execution, ToolMessage is appended to history and fed to the LLM for continuation.

**Code:**
```python
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage

call_id = "call_9fgh123"
tool_resp = ToolMessage(content="21 C, sunny", tool_call_id=call_id)
history = [
    HumanMessage(content="weather in Paris?"),
    AIMessage(content="", tool_calls=[{"name": "get_weather",
                                       "args": {"city": "Paris"}, "id": call_id}]),
    tool_resp,   # result sent back to the LLM to continue
]
print(tool_resp.tool_call_id, tool_resp.content)
```

**Q17: Explain the concept of "bind" in LangChain tools.**
A: `bind()` attaches runtime arguments to a Runnable without changing its signature. Example: `model.bind_tools(tools)` injects tool definitions to the model call. `model.bind(stop=["\n"])` sets stop tokens. `chain.bind(input_key="value")` provides constant values. Useful for configuring components at chain creation time.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"sunny in {city}"

model = ChatOpenAI(model="gpt-4o-mini")
bound = model.bind_tools([get_weather])          # inject tool schema
stopped = model.bind(stop=["\n"])                # bind stop tokens
resp = bound.invoke("What is the weather in Lyon?")
print(resp.tool_calls)
```

**Q18: What is the difference between "invoke" and "batch" in LangChain?**
A: `invoke`: single input → single output. `batch`: list of inputs → list of outputs, with configurable parallelism via `RunnableConfig(max_concurrency=N)`. Both support streaming (via `stream` / `batch` returns all at once). Batch is more efficient for independent requests.

**Code:**
```python
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig

fn = RunnableLambda(lambda x: x.upper())
print(fn.invoke("hello"))                    # HELLO
print(fn.batch(["a", "b", "c"],
               config=RunnableConfig(max_concurrency=3)))  # ['A','B','C']
```

**Q19: How does LangChain's callback system work?**
A: Callbacks provide hooks into chain execution. BaseCallbackHandler has methods: on_llm_start/end, on_chain_start/end, on_tool_start/end, on_retriever_start/end, etc. Used for logging, monitoring, streaming UI updates. Configured via CallbackManager or passed in RunnableConfig. LangSmithHandler is the primary production callback.

**Code:**
```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class LogHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM start: {prompts}")
    def on_llm_end(self, response, **kwargs):
        print(f"LLM end: {response}")

model = ChatOpenAI(model="gpt-4o-mini", callbacks=[LogHandler()])
model.invoke([HumanMessage(content="hi")])
```

**Q20: What is the role of RunnableConfig in LangChain?**
A: RunnableConfig carries runtime configuration: callbacks, metadata (run name, tags), max_concurrency, recursion_limit, and run_id. Passed through every Runnable invocation. Enables tracing, cancellation, and configuration override without changing the chain definition.

**Code:**
```python
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig

chain = RunnableLambda(lambda x: x * 2)
result = chain.batch(
    [1, 2, 3],
    config=RunnableConfig(
        tags=["api"], metadata={"user_id": 42}, max_concurrency=3,
    ),
)
print(result)
```

## 2. Chains & Composability (Q21–Q35)

**Q21: What is a "chain" in LangChain and how do you build one?**
A: A chain is a sequence of steps (LLM calls, retrievals, transforms) combined to accomplish a task. Built via LCEL with `|` operator. Example: `chain = prompt | model | parser`. Each step must be a Runnable. LangChain also offers legacy Chain classes (LLMChain, SimpleSequentialChain) but LCEL is preferred.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = (ChatPromptTemplate.from_messages([("human", "Translate to {lang}: {text}")])
         | ChatOpenAI(model="gpt-4o-mini")
         | StrOutputParser())
print(chain.invoke({"lang": "French", "text": "Hello"}))
```

**Q22: Explain the difference between a sequential chain and a parallel chain.**
A: Sequential chain (`|`): steps execute one after another, output of each is input to next. Parallel chain (`RunnableParallel`): steps execute concurrently on the same input, results merge into a dict. Combined: `{"step1": chain1, "step2": chain2} | combine | model`.

**Code:**
```python
from langchain_core.runnables import RunnableLambda, RunnableParallel

add_one = RunnableLambda(lambda x: x + 1)
cube = RunnableLambda(lambda x: x ** 3)
sequential = add_one | cube                 # (x+1)^3
print(sequential.invoke(2))                 # 27

parallel = RunnableParallel(plus1=add_one, cube=cube)
print(parallel.invoke(2))                   # {'plus1': 3, 'cube': 8}
```

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

**Code:**
```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

short = RunnableLambda(lambda q: f"quick: {q}")
medium = RunnableLambda(lambda q: f"medium: {q}")
long = RunnableLambda(lambda q: f"long: {q}")

chain = RunnableBranch(
    (lambda q: len(q) < 10, short),
    (lambda q: len(q) < 50, medium),
    long,
)
print(chain.invoke("hi"))
```

**Q24: What is a "RunnableMap" (RunnableParallel) and give a use case.**
A: RunnableParallel runs multiple runnables on same input, returns dict of results. Use case: RAG where retriever and query processing run concurrently:
```python
chain = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
}) | prompt | model | parser
```
Retriever fetches docs while question passes through, then both feed into prompt.

**Code:**
```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

retriever = RunnableLambda(lambda q: [f"doc about {q}"])
chain = (RunnableParallel(
             {"context": retriever, "question": RunnablePassthrough()})
         | ChatPromptTemplate.from_messages(
             [("human", "Answer using {context}:\n{question}")])
         | ChatOpenAI(model="gpt-4o-mini")
         | StrOutputParser())
print(chain.invoke("LangChain"))
```

**Q25: How do you handle errors in LCEL chains?**
A: 
- `.with_retry()` — auto-retry on failure with exponential backoff
- `.with_fallbacks()` — fallback chain if primary fails
- Try/except in RunnableLambda — catch and handle errors
- `Runnable.with_retry(stop_after_attempt=3)` for transient errors (rate limits, timeouts)
- Use callbacks for error logging and monitoring

**Code:**
```python
from langchain_core.runnables import RunnableLambda

def flaky(x):
    if x == "boom":
        raise ValueError("temporary failure")
    return x.upper()

primary = RunnableLambda(flaky).with_retry(stop_after_attempt=3)
chain = primary.with_fallbacks([RunnableLambda(lambda x: "fallback")])
print(chain.invoke("ok"))            # OK
print(chain.invoke("boom"))          # fallback after retries
```

**Q26: What is the purpose of `.configurable_fields()` and `.configurable_alternatives()`?**
A: 
- `.configurable_fields()`: expose specific component params as runtime config (e.g., change model temperature)
- `.configurable_alternatives()`: swap entire components (e.g., use different LLM providers or retrieval strategies)
- Configured at invoke time via `RunnableConfig`. Enables A/B testing, per-user customization.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

model = ChatOpenAI(model="gpt-4o-mini").configurable_fields(
    temperature=ConfigurableField(id="llm_temperature", default=0.0),
)
response = model.invoke("hi", config={"configurable": {"llm_temperature": 0.9}})
print(response.content)
```

**Q27: How does LangChain handle stateful chains (conversation memory)?**
A: Via `BaseChatMemory` implementations:
- ConversationBufferMemory: stores all messages
- ConversationSummaryMemory: summarizes older messages
- ConversationBufferWindowMemory: keeps last k turns
- VectorStoreRetrieverMemory: retrieves relevant history
- Used with Chains or agents to maintain conversation context

**Code:**
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
memory.chat_memory.add_user_message("My name is Ada")
memory.chat_memory.add_ai_message("Nice to meet you!")
print(memory.load_memory_variables({}))
```

**Q28: What is StringOutputParser vs PydanticOutputParser vs JsonOutputParser?**
A: 
- StringOutputParser: returns raw string — simplest, identity for strings
- StrOutputParser: handles string/bytes conversion from LLM output
- PydanticOutputParser: parse into a Pydantic model using structured output
- JsonOutputParser: parse JSON object from LLM output
- Composable: pipe parsers or use with structured LLM output features

**Code:**
```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(description="movie title")
    year: int = Field(description="release year")

print(StrOutputParser().invoke("plain text"))
print(JsonOutputParser().invoke('{"title": "Inception"}'))
print(PydanticOutputParser(pydantic_object=Movie).parse(
    '{"title": "Inception", "year": 2010}'))
```

**Q29: How do you implement custom output parsers in LangChain?**
A: Subclass `BaseOutputParser[T]` and implement:
- `parse(text: str) -> T`: core parsing logic
- (optional) `get_format_instructions() -> str`: instructions for LLM on output format
- (optional) `parse_with_prompt(text, prompt)`: with prompt context
Register with `@chain` decorator or use RunnableLambda for simple cases.

**Code:**
```python
from langchain_core.output_parsers import BaseOutputParser

class CommaSeparated(BaseOutputParser[list[str]]):
    def parse(self, text: str) -> list[str]:
        return [item.strip() for item in text.split(",")]
    def get_format_instructions(self) -> str:
        return "Return items separated by commas."

parser = CommaSeparated()
print(parser.invoke("a, b, c"))            # ['a', 'b', 'c']
print(parser.get_format_instructions())
```

**Q30: What is the difference between RunnableSequence and SequentialChain?**
A: RunnableSequence (LCEL): modern, supports streaming/async/batch/tracing, type-safe, composable. SequentialChain: legacy class, verbose, no streaming, deprecated. Always use LCEL (RunnableSequence) for new chains.

**Code:**
```python
from langchain_core.runnables import RunnableLambda

# RunnableSequence (LCEL): streaming, async, composable
seq = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 10)
print(seq.invoke(1))       # 20
async for chunk in seq.astream([1]):
    print(chunk)           # 20 (async streaming works out of the box)
```

**Q31: How do you add memory to an LLM chain in LangChain?**
A: In LCEL: use `RunnableWithMessageHistory` which wraps a chain and manages message history persistence. Provide `get_session_history` to load/save by session_id. Under the hood, it prepends history to prompt via MessagesPlaceholder. Supports ChatMessageHistory backends: InMemory, SQL, Redis, etc.

**Code:**
```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
store = {}
def get_history(session_id: str):
    return store.setdefault(session_id, InMemoryChatMessageHistory())

chain = (prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser())
with_mem = RunnableWithMessageHistory(
    chain,
    get_session_history=get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
cfg = {"configurable": {"session_id": "s1"}}
print(with_mem.invoke({"input": "My name is Ada"}, config=cfg))
print(with_mem.invoke({"input": "What is my name?"}, config=cfg))
```

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

**Code:**
```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "Helpful assistant."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
sessions = {}
def get_session(sid):
    return sessions.setdefault(sid, InMemoryChatMessageHistory())

chain = RunnableWithMessageHistory(
    prompt | ChatOpenAI(model="gpt-4o-mini"),
    get_session_history=get_session,
    input_messages_key="input",
    history_messages_key="chat_history",
)
out = chain.invoke(
    {"input": "Hi!"},
    config={"configurable": {"session_id": "abc"}},
)
print(out.content)
```

**Q33: How does LangChain handle large documents in summarization chains?**
A: Two strategies:
- Stuff: fit entire doc in one prompt — simple but hits context limits
- Map-Reduce: split doc → summarize each chunk (map) → combine summaries (reduce)
- Refine: sequential, each chunk refines previous summary
- In LCEL: compose with RunnableParallel for map step, reduce with another LLM call
- LangChain provides `load_summarize_chain` with these modes

**Code:**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4o-mini")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text("Long article text. " * 100)

map_chain = (ChatPromptTemplate.from_messages([("human", "Summarize: {text}")])
             | model | StrOutputParser())
reduce_prompt = ChatPromptTemplate.from_messages(
    [("human", "Combine these summaries into one:\n{summaries}")])

summaries = [map_chain.invoke({"text": c}) for c in chunks]      # map
final = (reduce_prompt | model | StrOutputParser()).invoke(
    {"summaries": "\n".join(summaries)})                          # reduce
print(final)
```

**Q34: What is the "hub" in LangChain Hub?**
A: LangChain Hub is a central repository of prompts, chains, and agents. `langchain hub pull` downloads shared components. `langchain hub push` uploads your own. Used for prompt sharing, versioning, and community collaboration. Accessible via `langchain/hub` package.

**Code:**
```python
from langchain import hub
from langchain_openai import ChatOpenAI

prompt = hub.pull("rlm/rag-prompt")      # shared, versioned prompt
print(prompt.input_variables)
chain = prompt | ChatOpenAI(model="gpt-4o-mini")
print(chain.invoke({"context": "LangChain is a framework.",
                    "question": "What is LangChain?"}).content)
```

**Q35: How do you version and manage prompts in LangChain?**
A: Via LangChain Hub: pull prompts by tag/version. In code: pin to specific commit hash. For local management: store prompts as YAML or templates in git. Use `.configurable_alternatives()` to switch between prompt versions at runtime for A/B testing.

**Code:**
```python
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

prompt = hub.pull("rlm/rag-prompt")
versioned = (prompt | ChatOpenAI(model="gpt-4o-mini")).configurable_alternatives(
    ConfigurableField(id="prompt_version"),
    v2=hub.pull("rlm/rag-prompt:v2"),
)
out = versioned.invoke({"context": "LCEL composes chains.",
                        "question": "What is LCEL?"},
                       config={"configurable": {"prompt_version": "v2"}})
print(out.content)
```

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

**Code:**
```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

texts = ["LangChain is a framework for LLM apps.",
         "RAG means retrieval augmented generation."]
vectorstore = FAISS.from_texts(texts, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using only: {context}"),
    ("human", "{question}"),
])
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)
print(rag_chain.invoke("What is RAG?"))
```

**Q37: What is a retriever in LangChain and how does it differ from a vector store?**
A: VectorStore: stores and searches vectors (similarity_search, delete, add). Retriever: higher-level abstraction over vector store — implements `get_relevant_documents(query)` and integrates with LCEL. Created via `vectorstore.as_retriever(search_kwargs={"k": 5})`. Retriever is a Runnable; VectorStore is not.

**Code:**
```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_texts(
    ["LangChain is a framework.", "RAG improves answers."],
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
print([d.page_content for d in retriever.invoke("framework")])
print([d.page_content for d in vectorstore.similarity_search("framework", k=1)])
```

**Q38: Explain the different retrieval strategies in LangChain.**
A: 
- Basic similarity search: k nearest vectors
- MMR (Maximum Marginal Relevance): diversify results
- Similarity score threshold: only return docs above certain score
- Ensemble retriever: combine multiple retrievers with weighting
- Parent document retriever: retrieve smaller chunks, return parent docs
- Multi-query retriever: generate multiple query variants, search each, merge results

**Code:**
```python
retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k": 3},
)
mmr = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 0.7},
)
threshold = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.5},
)
print([d.page_content for d in mmr.invoke("LangChain")])
```

**Q39: What is the EnsembleRetriever and when would you use it?**
A: EnsembleRetriever combines results from multiple retrievers (e.g., keyword BM25 + vector similarity) with weighted scoring and reciprocal rank fusion. Use when: no single retrieval method is sufficient, need both lexical and semantic matching, improving recall at cost of some precision.

**Code:**
```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

texts = ["LangChain is a framework.", "Graph DBs store relationships."]
bm25 = BM25Retriever.from_texts(texts, k=1)
vector = FAISS.from_texts(
    texts, OpenAIEmbeddings()).as_retriever(search_kwargs={"k": 1})

ensemble = EnsembleRetriever(retrievers=[bm25, vector], weights=[0.5, 0.5])
print([d.page_content for d in ensemble.invoke("framework")])
```

**Q40: How does LangChain handle document chunking for RAG?**
A: Via TextSplitter classes:
- RecursiveCharacterTextSplitter: splits on separators recursively (most common)
- CharacterTextSplitter: fixed-size character chunks
- TokenTextSplitter: splits by token count (respects LLM token limits)
- SemanticChunker: splits by semantic similarity of sentences
- MarkdownHeaderTextSplitter: splits by markdown structure
- Configure: chunk_size (e.g., 1000 tokens), chunk_overlap (e.g., 200)

**Code:**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_text("This is one sentence. " * 20)
print(len(chunks), chunks[0])
```

**Q41: Explain the concept of "Parent Document Retriever" in LangChain.**
A: 
1. Split documents into small child chunks (for precise retrieval) and larger parent chunks (for context)
2. Embed and index only child chunks
3. On query: retrieve child chunks by similarity
4. Return the parent chunks containing matched children
5. Benefit: precise retrieval with rich context. Implemented via `ParentDocumentRetriever`.

**Code:**
```python
from langchain.retrievers import ParentDocumentRetriever
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

retriever = ParentDocumentRetriever(
    vectorstore=Chroma(embedding_function=OpenAIEmbeddings()),
    docstore=InMemoryStore(),
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=100),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=1000),
)
retriever.add_texts(["A long parent document with lots of context. " * 10])
docs = retriever.invoke("context")
print(len(docs[0].page_content))   # returns the big parent chunk
```

**Q42: What is the MultiQueryRetriever and how does it improve retrieval?**
A: MultiQueryRetriever uses an LLM to generate multiple paraphrased versions of the user's query, runs all through the retriever, deduplicates, and returns the combined results. Improves recall by covering different phrasings. Useful for ambiguous or complex queries.

**Code:**
```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(model="gpt-4o-mini"),
)
docs = retriever.invoke("How does LangChain work?")
print([d.page_content for d in docs])
```

**Q43: How does contextual compression work in LangChain RAG?**
A: ContextualCompressionRetriever wraps a base retriever and compresses retrieved docs:
- LLMChainExtractor: LLM extracts only relevant parts from each doc
- LLMChainFilter: LLM filters out irrelevant docs entirely
- EmbeddingsFilter: keeps only semantically relevant docs (by threshold)
- Reduces token usage and removes noise from retrieved context

**Code:**
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI

compressor = LLMChainExtractor.from_llm(ChatOpenAI(model="gpt-4o-mini"))
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
)
docs = compression_retriever.invoke("What does LangChain do?")
print([d.page_content for d in docs])
```

**Q44: What is the SelfQueryRetriever?**
A: SelfQueryRetriever lets the LLM extract both a search term AND metadata filters from a natural language query. For example: "Find articles about AI from 2024" → query="AI", filter=year>=2024. Requires the vector store to support metadata filtering. Useful for structured + semantic search.

**Code:**
```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_openai import ChatOpenAI

metadata_fields = [
    AttributeInfo(name="year", description="The year of the article", type="integer"),
]
retriever = SelfQueryRetriever.from_llm(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    vectorstore=vectorstore,
    document_contents="tech articles about AI",
    metadata_field_info=metadata_fields,
)
docs = retriever.invoke("Articles about AI from 2024")
print([d.page_content for d in docs])
```

**Q45: How do you handle RAG with multiple data sources in LangChain?**
A: 
- MultiRetrievalQAChain: route questions to appropriate retriever based on content
- Using RunnableBranch to route to different RAG chains
- Merge results from multiple retrievers with EnsembleRetriever
- Router retriever: LLM decides which data source to query
- LangChain's MultiSourceRetriever

**Code:**
```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

sql_chain = RunnableLambda(lambda q: f"SQL answer for: {q}")
pdf_chain = RunnableLambda(lambda q: f"PDF answer for: {q}")
router = RunnableBranch(
    (lambda q: "sql" in q.lower(), sql_chain),
    pdf_chain,   # default
)
print(router.invoke("run a SQL query to get users"))
```

**Q46: What is the difference between simple RAG and advanced RAG patterns in LangChain?**
A: Simple RAG: embed → retrieve → generate. Advanced RAG adds: query rewriting, multi-step retrieval, re-ranking, contextual compression, Hyde (generate hypothetical doc then search), step-back prompting, iterative retrieval, fusion retrieval (keyword + vector). LangChain supports all via composable runnables.

**Code:**
```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("human", "Answer using context.\n{context}\nQ: {question}")
])
model = ChatOpenAI(model="gpt-4o-mini")

# Simple RAG: embed -> retrieve -> generate
simple = (
    {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
    | prompt | model | StrOutputParser()
)

# Advanced: rewrite the query first, then retrieve + answer
rewrite = (ChatPromptTemplate.from_messages(
    [("human", "Rewrite into a clear question: {question}")])
    | model | StrOutputParser())
advanced = rewrite | RunnablePassthrough.assign(
    context=lambda q: vectorstore.as_retriever().invoke(q)) | prompt | model | StrOutputParser()
print(advanced.invoke("What is RAG?"))
```

**Q47: What is Hyde (Hypothetical Document Embeddings) in LangChain?**
A: Hyde: use an LLM to generate a hypothetical ideal document for the query, then embed and search with THAT hypothetical doc instead of the query. The idea: the hypothetical doc is closer to target docs in embedding space than the raw query, improving retrieval quality. Implemented via `HyDEQueryTransform`.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

hyde_prompt = ChatPromptTemplate.from_messages([
    ("human", "Write a hypothetical document that would answer: {question}")
])
hyde = hyde_prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

hypothetical_doc = hyde.invoke({"question": "How does RAG work?"})
docs = vectorstore.similarity_search(hypothetical_doc, k=2)  # embed the doc, not the query
print([d.page_content for d in docs])
```

**Q48: How do you implement RAG with conversation history (follow-up questions)?**
A: 
1. Use RunnableWithMessageHistory to maintain conversation
2. Before retrieval, use a "condense question" step: create a standalone query from {history + new question}
3. Retrieve using the standalone query
4. Generate answer with full context + history + retrieved docs
LangChain provides `create_history_aware_retriever` for this pattern.

**Code:**
```python
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

condense_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("chat_history"),
    ("human", "Standalone version of: {input}"),
])
history_retriever = create_history_aware_retriever(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=vectorstore.as_retriever(),
    prompt=condense_prompt,
)
result = history_retriever.invoke({
    "input": "What does it say about agents?",
    "chat_history": [("human", "Show me LangChain docs on memory")],
})
print([d.page_content for d in result])
```

**Q49: What is the role of Document transformers in LangChain RAG?**
A: Document transformers preprocess retrieved docs before sending to LLM:
- `LongContextReorder`: reorder docs to avoid lost-in-the-middle
- `EmbeddingsClusteringFilter`: cluster and select diverse docs
- `MetaDataTagger`: add metadata to docs
- Compressors: extract/filter relevant content
- Applied via `create_documents_transformer` or as RunnableLambda in chain

**Code:**
```python
from langchain_community.document_transformers import LongContextReorder
from langchain_core.documents import Document

reorderer = LongContextReorder()
docs = [Document(page_content=f"chunk {i}") for i in range(8)]
reordered = reorderer.transform_documents(docs)
print([d.page_content for d in reordered])
```

**Q50: How does LangChain handle multi-modal RAG (text + images)?**
A: 
- Use multi-modal embeddings (CLIP) to embed both text and images in same vector space
- Store both in vector store with metadata
- Retrieve relevant images + text chunks
- Feed as context to multi-modal LLM (GPT-4V, Gemini)
- LangChain supports via `MultiVectorRetriever` and multi-modal prompt templates

**Code:**
```python
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

message = HumanMessage(content=[
    {"type": "text", "text": "Describe this diagram."},
    {"type": "image_url", "image_url": {"url": "https://example.com/diagram.png"}},
])
model = ChatOpenAI(model="gpt-4o-mini")
print(model.invoke([message]).content)
```

**Q51: Explain the difference between "retrieval" and "reranking" in RAG.**
A: Retrieval: fast, approximate — fetches top-k (e.g., 20) from vector store. Reranking: slower, more accurate — applies cross-encoder to score and reorder the retrieved candidates, selecting the top-n (e.g., 5). This two-stage approach combines speed of ANN with accuracy of cross-encoders. LangChain integrates with CohereRerank, CrossEncoderReranker.

**Code:**
```python
from langchain_community.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

reranker = CrossEncoderReranker(
    model=HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base"),
    top_n=3,
)
docs = vectorstore.as_retriever(search_kwargs={"k": 10}).invoke("how do chains work")
filtered = reranker.compress_documents(docs, "how do chains work")
print([d.page_content for d in filtered])
```

**Q52: How do you evaluate RAG quality in LangChain?**
A: 
- LangSmith evaluation: define evaluators (correctness, faithfulness, relevance, hallucination)
- Use `LangChainStringEvaluator` or custom evaluators
- Metrics: context precision, context recall, answer relevancy, faithfulness
- RAGA (RAG Assessment) library integration
- A/B test with different retrievers/chunking strategies via LangSmith datasets

**Code:**
```python
from langsmith.evaluation import evaluate, LangChainStringEvaluator

quality = LangChainStringEvaluator("cot_qa")   # correctness evaluator

evaluate(
    lambda inputs: rag_chain.invoke({"question": inputs["question"]}),
    data="my-rag-dataset",                    # answers + contexts in LangSmith
    evaluators=[quality],
)
print("evaluation results written back to LangSmith")
```

**Q53: What is a "tool" in the context of RAG agents?**
A: A RAG tool wraps a retrieval chain as a callable tool that an agent can invoke. E.g., `@tool` that runs retriever.get_relevant_documents and returns formatted context. The agent decides when to use RAG vs other tools (calculator, search, etc.). Enables complex multi-step reasoning with retrieval.

**Code:**
```python
from langchain_core.tools import tool

@tool
def search_knowledge_base(query: str) -> str:
    """Retrieve up-to-date answers from our internal docs."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join(d.page_content for d in docs)

answer = search_knowledge_base.invoke({"query": "what is an agent?"})
print(answer)
```

**Q54: How does LangChain handle query routing in a multi-RAG system?**
A: 
- RouterChain: LLM chooses which RAG chain to invoke based on query
- RunnableBranch: route by keyword matching
- Semantic routing: embed query, compare to route descriptions
- LangChain's `RouterChain` and `MultiPromptChain` (legacy)
- Modern approach: agent-based routing with tool descriptions

**Code:**
```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

finance = RunnableLambda(lambda q: f"finance answer: {q}")
legal = RunnableLambda(lambda q: f"legal answer: {q}")
router = RunnableBranch(
    (lambda q: "invoice" in q.lower(), finance),
    (lambda q: "contract" in q.lower(), legal),
    RunnableLambda(lambda q: f"general answer: {q}"),
)
print(router.invoke("Invoice #42 status?"))
```

**Q55: What is the "corrective RAG" pattern and how to implement it in LangChain?**
A: Corrective RAG:
1. Retrieve docs
2. LLM evaluates if retrieved docs are relevant (using `LLMChainExtractor` or custom evaluator)
3. If relevant → generate answer
4. If irrelevant → rewrite query and re-retrieve (or use web search fallback)
5. If partially relevant → filter and proceed
Implemented via RunnableBranch with relevance check gate. Self-RAG is a related pattern.

**Code:**
```python
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_openai import ChatOpenAI

grader = ChatOpenAI(model="gpt-4o-mini")

def check_relevance(docs):
    verdict = grader.invoke(
        f"Relevant to the question? {docs[0].page_content}").content
    return "yes" in verdict.lower()

def rewrite_retrieve(q):
    new_q = f"improved query for: {q}"
    return vectorstore.similarity_search(new_q, k=2)

corrective = RunnableBranch(
    (check_relevance, lambda docs: [d.page_content for d in docs]),   # keep
    RunnableLambda(rewrite_retrieve),                                  # re-retrieve
)
print(corrective.invoke(vectorstore.similarity_search("rag", k=1)))
```

## 4. Agents & Tool Use (Q56–Q75)

**Q56: What is an agent in LangChain and what differentiates it from a chain?**
A: An agent is an LLM that repeatedly decides which action to take (tool call), observes the result, and continues until the task is complete. A chain is a fixed sequence of steps. Agents are dynamic — the path depends on intermediate results. LangChain provides AgentExecutor to run this loop.

**Code:**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
agent = create_tool_calling_agent(
    ChatOpenAI(model="gpt-4o-mini"), [multiply], prompt,
)
executor = AgentExecutor(agent=agent, tools=[multiply])
result = executor.invoke({"input": "What is 6 * 7?"})
print(result["output"])
```

**Q57: Explain the ReAct (Reasoning + Acting) agent framework.**
A: ReAct interleaves reasoning traces (thought) with tool calls (action). Pattern:
1. Thought: reason about what to do next
2. Action: call a tool (with input)
3. Observation: tool output
4. Repeat until answer found → Final Answer
LangChain's `create_react_agent` implements this with explicit prompt templates.

**Code:**
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

@tool
def square(x: float) -> float:
    """Return the square of a number."""
    return x * x

prompt = PromptTemplate.from_template(
    "Answer the question using tools.\nQuestion: {input}\n{agent_scratchpad}"
)
agent = create_react_agent(ChatOpenAI(model="gpt-4o-mini"), [square], prompt)
executor = AgentExecutor(agent=agent, tools=[square])
print(executor.invoke({"input": "What is the square of 9?"})["output"])
```

**Q58: What are the different agent types in LangChain?**
A: LangChain v0.3+ simplified to:
- `create_react_agent`: ReAct framework with tools
- `create_openai_tools_agent`: for models supporting tool calling (OpenAI, Anthropic, Gemini)
- `create_structured_chat_agent`: structured output for action/observation
- `create_tool_calling_agent`: generic tool calling (recommended)
- `create_xml_agent`: for XML-prompted models (e.g., Claude via Bedrock)
Legacy: zero-shot-react-description, conversational-react-description, etc.

**Code:**
```python
from langchain.agents import (
    create_react_agent, create_tool_calling_agent,
    create_structured_chat_agent, create_xml_agent,
)

# Recommended: native tool calling where the model supports it
agent = create_tool_calling_agent(model, tools, chat_prompt_with_scratchpad)
react = create_react_agent(model, tools, react_prompt)
structured = create_structured_chat_agent(model, tools, structured_prompt)
xml_agent = create_xml_agent(model, tools, xml_prompt)
```

**Q59: What is AgentExecutor and how does it manage the agent loop?**
A: AgentExecutor runs the iterative agent loop:
1. Call LLM with prompt + tools + history
2. Parse response — is it a final answer or tool call?
3. If tool call: execute tool, append tool result to history, loop
4. If final answer: return
5. Configurable: max_iterations, early_stopping_method, handle_parsing_errors
Handles edge cases: invalid tool calls, tool errors, iteration limits.

**Code:**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def get_length(s: str) -> int:
    """Return the length of a string."""
    return len(s)

agent = create_tool_calling_agent(model, [get_length], prompt)
executor = AgentExecutor(
    agent=agent,
    tools=[get_length],
    max_iterations=10,                       # cap the loop
    early_stopping_method="generate",        # ask LLM for final answer when stopping
    handle_parsing_errors=True,
)
print(executor.invoke({"input": "length of 'abcdef'?"})["output"])
```

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

**Code:**
```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class WeatherArgs(BaseModel):
    location: str = Field(description="city name, e.g. London")

@tool("weather_api", args_schema=WeatherArgs)
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"sunny, 21C in {location}"

print(get_weather.name, get_weather.description)
print(get_weather.invoke({"location": "London"}))
```

**Q61: What is the difference between "tool" and "toolkit" in LangChain?**
A: Tool: a single function an agent can call. Toolkit: a collection of related tools (e.g., SQLDatabaseToolkit with list_tables, execute_query, check_query). Toolkits provide cohesive functionality. LangChain has toolkits for: SQL, GitHub, Gmail, FileSystem, JSON, etc.

**Code:**
```python
from langchain_core.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

@tool
def single_tool(x: int) -> int:     # one standalone tool
    """Return x + 1."""
    return x + 1

db = SQLDatabase.from_uri("sqlite:///mydb.db")
toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(model="gpt-4o-mini"))
print([t.name for t in toolkit.get_tools()])   # a bundled set of tools
```

**Q62: How does LangChain handle tool calling in parallel?**
A: If the LLM returns multiple tool_calls in one response (supported by OpenAI, Gemini, Anthropic), LangChain dispatches them concurrently. The AgentExecutor runs tool executions in parallel, then collects all observations and sends them back to the LLM in a single turn. Improves efficiency for independent sub-tasks.

**Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def weather(city: str) -> str:
    """Get the weather for a city."""
    return f"weather in {city}: 20C"

model = ChatOpenAI(model="gpt-4o-mini")
augmented = model.bind_tools([weather])
resp = augmented.invoke("Weather in Paris and Tokyo")
print(resp.tool_calls)   # may contain BOTH calls -> executed in parallel
```

**Q63: What is "tool message" history and why is it important?**
A: After tool execution, ToolMessage (with tool_call_id) is appended to message history. The LLM uses this history to continue reasoning — it sees what it did and what the result was. Without proper tool message history, the LLM loses context and may repeat actions or produce incorrect final answers.

**Code:**
```python
from langchain_core.messages import AIMessage, ToolMessage

tool_call = {"name": "get_weather", "args": {"city": "Rome"},
             "id": "call_123", "type": "tool_call"}

history = [
    AIMessage(content="", tool_calls=[tool_call]),
    ToolMessage(content="21C sunny", tool_call_id="call_123", name="get_weather"),
]
last = history[-1]
print(last.type, last.content, last.tool_call_id)
```

**Q64: How do you manage agent state across multiple turns?**
A: 
- Messages are accumulated in the agent's message history
- History includes: HumanMessage, AIMessage (with tool_calls), ToolMessage
- RunnableWithMessageHistory persists history per session
- For long-running agents: use summarization to trim history (trim_messages utility)
- LangGraph provides more sophisticated state management for complex agents

**Code:**
```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, trim_messages

history = InMemoryChatMessageHistory()
history.add_messages([
    HumanMessage("hello"),
    AIMessage("hi, how can I help?"),
    HumanMessage("what is 5+5?"),
])
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

# Persist per session_id and trim when too long
def get_history(sid: str):
    return history

chat = RunnableWithMessageHistory(
    ChatOpenAI(model="gpt-4o-mini"),
    get_session_history=get_history,
    input_messages_key="input",
)
print(chat.invoke({"input": "Add 10 to it"}, config={"configurable": {"session_id": "u1"}}).content)
```

**Q65: Explain the concept of "agentic RAG" (RAG agents).**
A: Agentic RAG combines agents with retrieval — the agent decides when and how to retrieve. Instead of fixed RAG pipeline, the agent can: rewrite queries, retrieve multiple times, choose different data sources, combine retrieval with other tools, and reflect on retrieval results before answering. More flexible than naive RAG chains.

**Code:**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def rag_search(query: str) -> str:
    """Search our internal knowledge base."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join(d.page_content for d in docs)

@tool
def refute(claim: str) -> str:
    """Check additional sources for a claim."""
    return "No contradicting sources found."

agent = create_tool_calling_agent(
    ChatOpenAI(model="gpt-4o-mini"), [rag_search, refute],
    prompt_template_with_scratchpad,
)
executor = AgentExecutor(agent=agent, tools=[rag_search, refute])
print(executor.invoke({"input": "Summarize Q3 revenue with sources"})["output"])
```

**Q66: What is a "multi-agent" system in LangChain?**
A: A system where multiple agents collaborate:
- Router agent: distributes tasks to specialized agents
- Sequential: agents execute in sequence, passing results
- Supervisor: an agent coordinates other agents
- Debate: agents discuss to reach consensus
- Implemented via AgentExecutor + message passing between agents
- LangGraph provides better support for complex multi-agent systems

**Code:**
```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

def researcher(q): return f"research: {q}"
def writer(q): return f"written: {q}"

researcher_agent = RunnableLambda(researcher)
writer_agent = RunnableLambda(writer)
supervisor = RunnableBranch(
    (lambda q: "research" in q.lower(), researcher_agent),
    writer_agent,
)
print(supervisor.invoke("please research the topic"))
print(supervisor.invoke("now write an article"))
```

**Q67: How do you handle tool errors gracefully in agents?**
A: 
- AgentExecutor's handle_parsing_errors=True: catch malformed tool calls
- Tool's `handle_tool_error=True`: sends error message back as observation
- Fallback tools: if primary tool fails, try alternative
- Max retries per tool call
- If tool fails repeatedly, agent should apologize and stop (configure early_stopping_method="force")

**Code:**
```python
from langchain_core.tools import tool

@tool(handle_tool_error=True, handle_validation_error=True)
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b

print(divide.invoke({"a": 1, "b": 0}))   # returns error text, not a crash
```

**Q68: What is the "stop" sequence in agent prompts?**
A: Agent prompts include stop tokens that signal the LLM to stop generating (e.g., `<|eot_id|>`, `Observation:`). The model generates until it hits the stop token, then LangChain parses the output. For ReAct, `Observation:` is the stop string — the model writes Thought/Action/Action Input, then stops, waiting for the observation.

**Code:**
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", stop=["Observation:"])
resp = model.invoke("Thought: I need the weather.\nAction: get_weather\nAction Input: London")
print(resp.content)   # generation stops before "Observation:"
```

**Q69: How does LangChain implement function/tool calling for non-OpenAI models?**
A: LangChain normalizes tool calling across providers:
- OpenAI: native function calling
- Anthropic: tool use API
- Google: function declaration
- Ollama/Llama.cpp: tool calling via chat templates
- For models without native support: prompt-based tool calling with structured parsing
- `bind_tools()` abstracts this — LangChain handles the conversion per provider

**Code:**
```python
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

@tool
def get_time(city: str) -> str:
    """Get the current time in a city."""
    return f"12:30 in {city}"

for model in (ChatAnthropic(model="claude-3-5-sonnet"),
              ChatGoogleGenerativeAI(model="gemini-1.5-pro")):
    augmented = model.bind_tools([get_time])     # same API, provider-specific
    print(augmented.invoke("what time in Berlin?").tool_calls)
```

**Q70: What is the difference between `create_react_agent` and `create_tool_calling_agent`?**
A: 
- create_react_agent: uses ReAct prompt format (Thought/Action/Action Input/Observation). Works with ANY LLM (including non-tool-calling). Parses text output for tool calls.
- create_tool_calling_agent: uses model's native tool calling API. Only for models that support function calling. More reliable, supports parallel tool calls.
- Recommendation: use create_tool_calling_agent when possible; fall back to ReAct for other models.

**Code:**
```python
from langchain.agents import create_react_agent, create_tool_calling_agent
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# ReAct: works with any LLM, parses text markers
react_agent = create_react_agent(
    model, tools,
    PromptTemplate.from_template("Question: {input}\n{agent_scratchpad}"),
)

# Tool-calling: needs native support, more reliable + parallel
native_agent = create_tool_calling_agent(
    model, tools,
    ChatPromptTemplate.from_messages([
        ("human", "{input}"), MessagesPlaceholder("agent_scratchpad"),
    ]),
)
print(type(native_agent).__name__)
```

**Q71: How do you limit agent execution time or iterations?**
A: AgentExecutor config:
- `max_iterations`: max thought-action cycles (default 15)
- `max_execution_time`: wall-clock time limit
- `early_stopping_method`: "force" (return partial) or "generate" (ask LLM for final answer)
- Tool timeout: per-tool execution timeout
- Without limits, agents can loop infinitely or cost excessive tokens.

**Code:**
```python
from langchain.agents import AgentExecutor

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=5,                  # hard cap on thought-action loops
    max_execution_time=60,             # seconds wall-clock limit
    early_stopping_method="force",     # stop and return partial output
)
result = executor.invoke({"input": "Keep going forever"})
print(result["output"])
```

**Q72: What is a "stoppable agent" pattern?**
A: An agent that can be interrupted mid-execution. Implemented via:
- `astream_events()` for frontend cancellation
- Checkpointing agent state for resumability
- Human-in-the-loop approval gates (LangGraph)
- Python's asyncio cancellation with async agent execution
- Useful when an agent requires user confirmation before proceeding

**Code:**
```python
import asyncio
from langchain_core.runnables.config import RunnableConfig

async def run():
    async for event in executor.astream_events(
        {"input": "do research"},
        config=RunnableConfig(run_name="stoppable"),
        version="v2",
    ):
        if event["event"] == "on_tool_start":
            print("tool starting:", event["name"])
        if event["event"] == "on_chain_end":
            print("done:", event.get("data", {}).get("output"))
asyncio.run(run())
```

**Q73: How do you share state between agents in a multi-agent system?**
A: 
- Shared memory: agents write to a common message store
- Agent communication: agents send messages to each other (human-like)
- Shared tool access: tools that write to a shared database
- LangGraph: shared StateGraph with typed state that all nodes (agents) read/write
- Best practice: define a schema for inter-agent messages and shared state

**Code:**
```python
from typing import Annotated
from langchain_core.runnables import RunnableLambda
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: list  # shared across agents

def agent_a(state: AgentState) -> AgentState:
    return {"messages": state["messages"] + ["from agent_a"]}

def agent_b(state: AgentState) -> AgentState:
    return {"messages": state["messages"] + ["from agent_b"]}

pipeline = RunnableLambda(agent_a) | RunnableLambda(agent_b)
print(pipeline.invoke({"messages": []})["messages"])
```

**Q74: What is a "conversational agent" and how is it different from a standard agent?**
A: Conversational agent maintains dialogue history and uses memory to answer follow-up questions. Differs from standard agent by:
- Using ChatPromptTemplate with MessagesPlaceholder for history
- RunnableWithMessageHistory for persistence
- A "condense" step to extract standalone queries from multi-turn context
- Personality/system prompt awareness across turns
- `create_react_agent` with chat history support

**Code:**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

convo_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with a friendly personality."),
    MessagesPlaceholder("chat_history"),           # prior turns injected here
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
agent = create_tool_calling_agent(
    model, tools, convo_prompt,
)
conv_executor = AgentExecutor(agent=agent, tools=tools)
out = conv_executor.invoke({
    "input": "Hi! remember I like blue",
    "chat_history": [],
})
print(out["output"])
```

**Q75: How do you test and evaluate agents in LangChain?**
A: 
- LangSmith evaluation: run agent against test datasets, measure success rate
- Unit test individual tools
- Simulate tool responses for deterministic testing
- Evaluate: task completion rate, steps taken, token efficiency, hallucination rate
- LangSmith's `aevaluate` for LLM-as-judge evaluation
- Regression testing with known edge cases

**Code:**
```python
from langsmith.evaluation import evaluate

def run_agent(inputs):
    result = executor.invoke({"input": inputs["question"]})
    return {"output": result["output"]}

evaluate(
    run_agent,
    data="agent-eval-dataset",        # expected answers in LangSmith
    evaluators=["qa", "criteria"],    # correctness + rubric judges
)
print("agent benchmark complete")
```

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

**Code:**
```python
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationTokenBufferMemory,
)
from langchain_openai import ChatOpenAI

buffer = ConversationBufferMemory(return_messages=True)
window = ConversationBufferWindowMemory(k=5, return_messages=True)
token_budget = ConversationTokenBufferMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"), max_token_limit=500,
)
print(window.k)                       # keeps only last 5 turns
```

**Q77: How does ConversationSummaryMemory work and when is it useful?**
A: It maintains a running summary of the conversation. At each turn, the LLM updates the summary with new context. On query, the summary + recent messages are injected. Useful for long conversations where full history exceeds context window. More token-efficient than buffer but loses detail.

**Code:**
```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

memory = ConversationSummaryMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"), return_messages=True,
)
memory.save_context({"input": "I love LangChain"},
                    {"output": "Great, what about it?"})
memory.save_context({"input": "Agents!"},
                    {"output": "Let's discuss agents."})
print(memory.load_memory_variables({})["history"])  # running summary
```

**Q78: What is the role of Document objects in LangChain?**
A: Document is the core unit for unstructured data: `Document(page_content="...", metadata={"source": "...", "page": 1})`. Used throughout indexing and retrieval. Documents flow from: loaders → splitters → embedding → vector store → retriever → chain. Metadata enables filtering and provenance tracking.

**Code:**
```python
from langchain_core.documents import Document

doc = Document(
    page_content="LangChain makes building LLM apps easy.",
    metadata={"source": "docs/intro.md", "page": 1},
)
print(doc.page_content, doc.metadata)     # a self-contained data unit
```

**Q79: How does LangChain integrate with document loaders?**
A: Document loaders load from various sources:
- PDF: PyPDFLoader, PDFMinerLoader
- Web: WebBaseLoader, SitemapLoader, AsyncHtmlLoader
- Database: SQLLoader, MongoDBLoader
- Code: PythonLoader, TextLoader
- Cloud: S3FileLoader, GCSFileLoader
- Each implements `load()` → List[Document] or `alazy_load()` for streaming

**Code:**
```python
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader

pdf_docs = PyPDFLoader("manual.pdf").load()          # -> List[Document]
txt_docs = TextLoader("notes.txt").load()
web_docs = WebBaseLoader("https://example.com/docs").load()
print(len(pdf_docs), len(txt_docs), len(web_docs))
```

**Q80: What is the difference between lazy_load and load in document loaders?**
A: `load()` loads all documents into memory at once — simple but can OOM for large datasets. `lazy_load()` returns an iterator — documents are loaded on-demand, processing as you iterate. Use `lazy_load()` with `RecursiveCharacterTextSplitter` to pipeline large-scale ingestion.

**Code:**
```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("big_book.txt")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for doc in loader.lazy_load():                      # one document at a time
    for chunk in splitter.split_text(doc.page_content):
        print(len(chunk))                            # stream chunks, low memory
```

**Q81: How do you process large-scale document ingestion in LangChain?**
A: 
1. Use lazy loaders + streaming splitters
2. Batch embeddings (avoid OOM on GPU/API)
3. Use vector store's `add_documents` with batching
4. Use LangChain's `index` API for incremental indexing (avoid re-indexing unchanged docs)
5. Consider parallel processing with RunnableParallel or multiprocessing
6. Monitor API rate limits with `with_retry`

**Code:**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
all_chunks = []
for doc in TextLoader("large.txt").lazy_load():
    all_chunks += splitter.split_documents([doc])

vectorstore = FAISS.from_documents(
    all_chunks, OpenAIEmbeddings(),   # embeddings called in internal batches
)
for batch in range(0, len(all_chunks), 100):
    vectorstore.add_documents(all_chunks[batch:batch + 100])
print(f"ingested {len(all_chunks)} chunks")
```

**Q82: Explain the LangChain "index" API for document management.**
A: `langchain.indexes.VectorStoreIndexWrap` maps documents to vector stores with id tracking:
- Tracks document hashes
- Only embeds changes (new/modified docs)
- Deletes stale documents
- Prevents duplicate vectors
- Essential for production RAG document pipelines

**Code:**
```python
from langchain.indexes import SQLRecordManager, index
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

record_manager = SQLRecordManager(
    namespace="my_docs", db_url="sqlite:///index_records.sqlite",
)
record_manager.create_schema()
vectorstore = FAISS.from_documents(
    docs, OpenAIEmbeddings(),   # freshly built store
)
result = index(
    docs, record_manager, vectorstore,
    cleanup="incremental",
    source_id_key="source",
)
print(result)   # {'num_added': ..., 'num_updated': ..., 'num_deleted': ...}
```

**Q83: What is the SQLRecordManager in LangChain?**
A: SQLRecordManager tracks document writes in a SQLite/Postgres database. Used with the Indexing API to record which documents have been written. On re-index: compares current docs vs records, only processes differences. Supports clean/upsert modes. Records document ID + source hash + write timestamp.

**Code:**
```python
from langchain.indexes import SQLRecordManager, index

manager = SQLRecordManager(namespace="prod_docs", db_url="sqlite:///records.db")
manager.create_schema()
print(manager.get_time())                       # current write timestamp
result = index(
    [doc1, doc2], manager, vectorstore,
    cleanup="incremental", source_id_key="source",
)
manager.list_keys()                             # only changed/new docs remain
```

**Q84: How does LangChain handle document deduplication?**
A: 
- Via the Indexing API with `VectorStoreIndexWrap(record_manager, ...)`
- Document hashing: content hash determines uniqueness
- Cleanup modes: incremental (delete removed docs), full (rebuild)
- Custom dedup: compare metadata / content before adding
- For vector dedup: search for near-duplicates before inserting

**Code:**
```python
from langchain.indexes import SQLRecordManager, index
from langchain_core.documents import Document

manager = SQLRecordManager(namespace="dedup", db_url="sqlite:///dedup.db")
manager.create_schema()

same_doc = [Document(page_content="identical content", metadata={"source": "a.txt"})] * 5
first = index(same_doc, manager, vectorstore, cleanup="incremental",
              source_id_key="source")
second = index(same_doc, manager, vectorstore, cleanup="incremental",
               source_id_key="source")
print(first["num_added"], second["num_added"])   # second run adds 0
```

**Q85: What are the different embedding model integrations in LangChain?**
A: LangChain provides `Embeddings` interface for: OpenAI, Anthropic, Cohere, HuggingFace (sentence-transformers), Ollama (nomic-embed-text, mxbai-embed), Google VertexAI, AWS Bedrock, Together AI, Mistral AI, Jina AI, and local models via HuggingFaceEmbeddings.

**Code:**
```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vec = embeddings.embed_query("LangChain embeddings")
print(len(vec))                                     # 1536-dim vector

local = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print(local.embed_documents(["a", "b"])[0][:3])     # local, offline capable
```

**Q86: How do you switch between embedding models without re-indexing?**
A: You CANNOT — changing the embedding model changes the vector space, making old vectors incompatible. To migrate: create a new collection with new embeddings, re-index all documents, then swap the collection pointer. Some apps run dual embedding during migration.

**Code:**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

old_store = FAISS.from_texts(
    ["your documents"],
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)

# 1) build a fresh index with the new model
new_store = FAISS.from_texts(
    ["your documents"],
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
)
# 2) swap the pointer at runtime
active_store = new_store
print(active_store.similarity_search("migrated from old model"))
```

**Q87: What is the CacheBackedEmbeddings and when should you use it?**
A: CacheBackedEmbeddings wraps an Embeddings instance with a cache (disk/Redis). First time a text is embedded: compute and cache. Subsequent identical texts: return cached vector. Reduces API costs and latency for repeated texts. Useful for ingesting data with duplicate chunks or queries.

**Code:**
```python
from langchain.storage import LocalFileStore
from langchain_community.embeddings import CacheBackedEmbeddings
from langchain_openai import OpenAIEmbeddings

store = LocalFileStore("./cache")
embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    document_embedding_cache=store,
    namespace="embeddings",
)
v1 = embeddings.embed_query("repeated text")
v2 = embeddings.embed_query("repeated text")   # served from cache
print(v1 == v2)
```

**Q88: How does LangChain handle token counting and cost estimation?**
A: 
- `get_openai_callback()` context manager: tracks tokens used, cost
- `OpenAICallbackHandler`: callback for token tracking
- Token counting via tiktoken for OpenAI models
- For other models: approximate via model-specific tokenizers
- Integrates with LangSmith for cost tracking across runs

**Code:**
```python
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
with get_openai_callback() as cb:
    model.invoke("Summarize token usage for me")
    model.invoke("Once more")

print(cb.total_tokens)          # combined across all calls
print(cb.prompt_tokens, cb.completion_tokens)
print(cb.total_cost)            # estimated USD cost
```

**Q89: What is the difference between batch and async ingestion in LangChain?**
A: Batch ingestion (`vectorstore.add_documents(docs)`) processes documents sequentially or in parallel threads. Async ingestion (`await vectorstore.aadd_documents(docs)`) uses asyncio — better for I/O-bound workloads (API-based embeddings). For large datasets: use `batch_size` parameter to control concurrency and rate limiting.

**Code:**
```python
import asyncio
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())

# sync batch ingestion
vectorstore.add_documents(docs[0:50])

# async ingestion for I/O-heavy API workloads
async def ingest():
    await vectorstore.aadd_documents(docs[50:100])
asyncio.run(ingest())
```

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

**Code:**
```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = WebBaseLoader(["https://docs.example.com/page"])
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

for doc in loader.lazy_load():                 # streamed, not loaded at once
    for chunk in splitter.split_documents([doc]):
        print(chunk.page_content[:30])
```

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

**Code:**
```python
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="LangChain API")
chain = (ChatPromptTemplate.from_messages([("human", "{question}")])
         | ChatOpenAI(model="gpt-4o-mini"))

add_routes(app, chain, path="/chat", enable_feedback_endpoint=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Q92: How does LangChain handle rate limiting with LLM providers?**
A: 
- `with_retry()`: exponential backoff + jitter
- Custom rate limiter middleware via callbacks
- `max_concurrency` in RunnableConfig for batch calls
- Token bucket or sliding window rate limiter
- Async for non-blocking I/O
- Queue-based processing with controlled throughput

**Code:**
```python
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig

flaky = RunnableLambda(lambda x: f"ok: {x}") .with_retry(
    stop_after_attempt=3,                        # backoff + retries on failure
    retry_if_exception_type=(TimeoutError,),
)
results = flaky.batch(
    list(range(20)),
    config=RunnableConfig(max_concurrency=2),    # throttles concurrency
)
print(len(results))
```

**Q93: What is the role of "filters" in LangChain retrievers?**
A: Filters restrict retrieval by document metadata: `vectorstore.as_retriever(search_kwargs={"filter": {"year": 2024}})`. Supported by most vector stores. Enables: date range filtering, category filtering, source filtering, access control. Different vector stores have different filter syntaxes — LangChain normalizes via `RunnableLambda`.

**Code:**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["Q3 report", "Q4 report"],
    embedding=OpenAIEmbeddings(),
    metadatas=[{"year": 2024}, {"year": 2025}],
)
filtered = vectorstore.as_retriever(
    search_kwargs={"k": 1, "filter": {"year": 2024}},
)
print([d.page_content for d in filtered.invoke("report")])
```

**Q94: How does LangChain handle PII (Personally Identifiable Information) in chains?**
A: 
- Presidio integration for PII detection and redaction
- `PresidioReversibleAnonymizer`: anonymizes PII before LLM, de-anonymizes response
- Custom callbacks to scan inputs/outputs
- LangChain's `OpenAIModerationChain` for content filtering
- Best practice: detect + redact before any external API call

**Code:**
```python
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer

anonymizer = PresidioReversibleAnonymizer()
text = "My email is ada@example.com and I live in Paris."

masked = anonymizer.anonymize(text)
print(masked)                                  # PII replaced with placeholders
print(anonymizer.deanonymize(masked))          # restore before showing user
```

**Q95: What is the difference between LangChain and LlamaIndex?**
A: LangChain: broader framework — chains, agents, tools, memory, ecosystem integrations. LlamaIndex: specialized for data indexing and retrieval (RAG). LangChain is better for complex agent workflows; LlamaIndex is better for advanced data ingestion and retrieval. They complement each other — many production apps use both.

**Code:**
```python
# LangChain: general LLM app framework
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

chain = (ChatPromptTemplate.from_messages([("human", "{input}")])
         | ChatOpenAI(model="gpt-4o-mini"))

# LlamaIndex: focused document indexing + retrieval
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
print(query_engine.query("What does the doc say?"))
```

**Q96: How does LangChain handle Structured Output vs JSON mode?**
A: Two approaches:
1. Bind model to a Pydantic schema: `model.with_structured_output(SchemaClass)` — uses model's native structured output (tool calling internally)
2. PydanticOutputParser: instruct the LLM via prompt to output JSON, then parse it
3. JsonOutputParser: simpler JSON parsing
4. with_structured_output is preferred — more reliable, avoids prompt injection issues

**Code:**
```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(description="the title")
    year: int = Field(description="publish year")

model = ChatOpenAI(model="gpt-4o-mini")
structured = model.with_structured_output(Book)          # native tool calling
book = structured.invoke("Inception, released 2010")
print(book.title, book.year)
```

**Q97: What is the "RunnableGenerator" pattern?**
A: RunnableGenerator yields multiple outputs from a single input — like a generator function wrapped as a Runnable. Used for: stream processing, map operations, incremental processing. Example: yield chunks of a transformed document. Less common than RunnableLambda for most use cases.

**Code:**
```python
from langchain_core.runnables import RunnableGenerator

def split_into_chunks(text: str):
    for line in text.splitlines():
        yield line.strip()

chain = RunnableGenerator(split_into_chunks)
for chunk in chain.stream("line one\nline two"):
    print(chunk)               # "line one", "line two"
```

**Q98: How do you handle user feedback in LangChain RAG systems?**
A: 
- Collect: thumbs up/down, explicit ratings, implicit signals (clicks, dwell time)
- Store feedback in LangSmith: `runs.feedback.create()` linked to trace run_id
- Use feedback to: fine-tune reranker, adjust chunking strategy, improve prompt
- Active learning: low-confidence queries → human label → improve retrieval
- LangSmith datasets for continuous evaluation

**Code:**
```python
from langsmith import Client

client = Client()
run_id = "input_run_id_after_trace"       # captured from the chain run

client.create_feedback(
    run_id=run_id,
    key="user_score",
    score=1.0,                             # thumbs up / down
    comment="answer was exactly right",
)
print("feedback recorded for", run_id)
```

**Q99: What are the major breaking changes in LangChain v0.3?**
A: 
- Legacy chains (LLMChain, SimpleSequentialChain) removed
- LangChain community packages separated (langchain-community)
- Standardized on ChatModels over LLM abstractions
- LCEL as the only recommended composition method
- Agent types simplified to tool-calling
- Model I/O streamlined with BaseMessage
- Import paths reorganized

**Code:**
```python
# v0.3 style: ChatModels + LCEL
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = (ChatPromptTemplate.from_messages([("human", "{input}")])
         | ChatOpenAI(model="gpt-4o-mini")
         | StrOutputParser())
print(chain.invoke({"input": "v0.3 migrated"}))
```

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

**Code:**
```python
from langchain_ollama import ChatOllama   # on-device, locally hosted
from langchain_core.messages import HumanMessage

local_model = ChatOllama(model="llama3.2")
for chunk in local_model.stream([HumanMessage(content="Count 1 to 3")]):
    print(chunk.content, end="", flush=True)   # streaming-first UX
```