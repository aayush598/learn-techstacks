# Section 01: Python SDK Architecture

## Overview

The Python SDK provides a clean, idiomatic interface for Python developers to interact with the Voice Agent API. The architecture follows a modular package structure with a client class, resource sub-clients, Pydantic models, and an adapter pattern for HTTP transport. The package supports both sync and async usage patterns.

## Architecture

```
Package Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

voice_agent/
├── __init__.py                 → Public exports
├── client.py                   → VoiceAgent client class
├── config.py                   → Configuration and settings
├── errors.py                   → Exception classes
├── models/
│   ├── __init__.py
│   ├── agent.py                → Agent models
│   ├── call.py                 → Call models
│   ├── campaign.py             → Campaign models
│   ├── common.py               → Shared models (pagination, etc.)
│   └── events.py               → Event models
├── resources/
│   ├── __init__.py
│   ├── base.py                 → Base resource client
│   ├── agents.py               → Agents API
│   ├── calls.py                → Calls API
│   ├── campaigns.py            → Campaigns API
│   └── webhooks.py             → Webhooks API
├── streaming/
│   ├── __init__.py
│   ├── websocket.py            → WebSocket client
│   └── events.py               → Event subscription
├── webhooks/
│   ├── __init__.py
│   └── verify.py               → Signature verification
└── utils/
    ├── __init__.py
    ├── retry.py                → Retry logic
    ├── pagination.py           → Pagination iterators
    └── http.py                 → HTTP client adapter

Usage:
  from voice_agent import VoiceAgent
  from voice_agent.models import Agent, AgentConfig

  client = VoiceAgent(api_key="va_live_abc")
  agents = client.agents.list(status="active")
  agent = client.agents.create(AgentConfig(name="Support Bot", ...))
```

## Design Decisions

- **Resource Sub-Clients**: `client.agents.list()`, `client.calls.get()` — same pattern as TypeScript SDK
- **Pydantic v2 Models**: Automatic serialization/deserialization, type validation, and IDE autocomplete
- **Adapter Pattern**: HTTP transport is swappable — can use httpx (async) or requests (sync)
- **Namespace Packages**: No circular dependencies between resource modules

## Implementation Approach

```python
"""voice_agent/client.py"""

from __future__ import annotations

import os
from typing import Optional
from .config import ClientConfig, Environment
from .resources.agents import AgentsResource
from .resources.calls import CallsResource
from .resources.campaigns import CampaignsResource
from .utils.http import HttpClient


class VoiceAgent:
    """Main client for the Voice Agent API."""

    def __init__(
        self,
        api_key: str,
        environment: Environment = "production",
        base_url: Optional[str] = None,
        timeout: int = 30,
        retry_max: int = 3,
    ) -> None:
        self.config = ClientConfig(
            api_key=api_key,
            environment=environment,
            base_url=base_url or self._get_default_url(environment),
            timeout=timeout,
            retry_max=retry_max,
        )
        self._http = HttpClient(self.config)

        # Initialize resource clients
        self.agents = AgentsResource(self._http)
        self.calls = CallsResource(self._http)
        self.campaigns = CampaignsResource(self._http)

    @staticmethod
    def _get_default_url(environment: Environment) -> str:
        urls = {
            "production": "https://api.voiceagent.com",
            "sandbox": "https://api.sandbox.voiceagent.com",
            "development": "http://localhost:3000",
        }
        return urls.get(environment, urls["production"])

    @classmethod
    def from_env(cls) -> VoiceAgent:
        """Create client from environment variables."""
        return cls(
            api_key=os.environ["VOICE_AGENT_API_KEY"],
            environment=os.environ.get("VOICE_AGENT_ENV", "production"),
        )


"""voice_agent/config.py"""

from typing import Literal

Environment = Literal["production", "sandbox", "development"]


class ClientConfig:
    def __init__(
        self,
        api_key: str,
        environment: Environment,
        base_url: str,
        timeout: int,
        retry_max: int,
    ) -> None:
        self.api_key = api_key
        self.environment = environment
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_max = retry_max


"""voice_agent/resources/base.py"""

from typing import TypeVar, Generic, Optional
from ..utils.http import HttpClient
from ..models.common import ListResponse

T = TypeVar("T")


class BaseResource(Generic[T]):
    """Base class for resource clients."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http


"""voice_agent/resources/agents.py"""

from typing import Optional
from .base import BaseResource
from ..models.agent import Agent, AgentConfig
from ..models.common import ListResponse


class AgentsResource(BaseResource[Agent]):
    """Agent API resource."""

    async def list(
        self,
        cursor: Optional[str] = None,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> ListResponse[Agent]:
        return await self._http.get("/v1/agents", params={
            "cursor": cursor,
            "limit": limit,
            "status": status,
        })

    async def get(self, agent_id: str) -> Agent:
        return await self._http.get(f"/v1/agents/{agent_id}")

    async def create(self, config: AgentConfig) -> Agent:
        return await self._http.post("/v1/agents", body=config.model_dump())

    async def update(self, agent_id: str, config: AgentConfig) -> Agent:
        return await self._http.patch(f"/v1/agents/{agent_id}", body=config.model_dump())

    async def delete(self, agent_id: str) -> None:
        await self._http.delete(f"/v1/agents/{agent_id}")
```

## Integration Points

- **PyPI Distribution**: Published as `voice-agent-sdk`
- **Type Hints**: Full type annotations for IDE autocomplete
- **Async Support**: Async/await throughout for modern Python applications

## Production Considerations

- **Connection Pooling**: httpx connection pool with keep-alive
- **Retry Handling**: Automatic retry on 429/5xx with exponential backoff
- **Timeout Configuration**: Configurable per-request timeout
- **Logging**: Structured logging integration with Python logging module

## Open-Source Tools

- **httpx**: Modern HTTP client with async support
- **Pydantic v2**: Data validation and settings management
- **poetry**: Dependency management and packaging
