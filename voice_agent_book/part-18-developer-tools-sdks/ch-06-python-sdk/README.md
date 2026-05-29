# Chapter 06: Python SDK

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Python SDK Architecture](sec-01-python-sdk-architecture.md) | Package structure, client class, configuration, module organization, adapter pattern |
| 02 | [Async vs Sync Client](sec-02-async-vs-sync-client.md) | httpx vs requests, asyncio support, async context managers, mixed sync/async usage |
| 03 | [Type Hints & Pydantic Models](sec-03-type-hints-pydantic-models.md) | Pydantic v2 models, request/response validation, serialization/deserialization, IDE autocomplete |
| 04 | [Package Distribution (PyPI)](sec-04-package-distribution-pypi.md) | pyproject.toml configuration, versioning, publishing workflow, CI/CD for PyPI releases |
| 05 | [Authentication & Session](sec-05-authentication-session.md) | API key management, connection pooling, retry session, token refresh for OAuth |
| 06 | [Streaming Response Handling](sec-06-streaming-response-handling.md) | SSE/event stream parsing, async generators, real-time transcription streams, backpressure |
| 07 | [Python SDK Documentation](sec-07-python-sdk-documentation.md) | Docstrings, Sphinx/ MkDocs, auto-generated API reference, notebook examples |
| 08 | [SDK Maintenance & Versioning](sec-08-sdk-maintenance-versioning.md) | Semantic versioning, deprecation policy, changelog generation, backward compatibility |

---

## Python SDK Usage

```python
from voice_agent import VoiceAgent
from voice_agent.models import AgentConfig, VoiceConfig

# Initialize client
client = VoiceAgent(
    api_key="va_live_...",
    environment="sandbox"  # or "production"
)

# List agents
agents = client.agents.list(status="active", limit=20)
for agent in agents:
    print(f"{agent.id}: {agent.name}")

# Create agent
agent = client.agents.create(
    AgentConfig(
        name="Customer Support Bot",
        voice=VoiceConfig(provider="elevenlabs", voice_id="21m00Tcm4TlvDq8ikWAM"),
        model=ModelConfig(provider="openai", model="gpt-4o"),
    )
)

# Stream transcription (async)
async for event in client.calls.stream_transcription("call_id_123"):
    if event.type == "transcript":
        print(f"[{event.speaker}] {event.text}")
```

---

## Learning Objectives

- Design Python SDK with clean package structure
- Implement both sync and async clients
- Use Pydantic models for request/response validation
- Publish package to PyPI with CI/CD
- Implement authentication with connection pooling
- Handle streaming responses with async generators
- Generate documentation with MkDocs
- Maintain SDK with semantic versioning
