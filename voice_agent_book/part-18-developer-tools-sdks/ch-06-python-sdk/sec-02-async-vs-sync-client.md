# Section 02: Async vs Sync Client

## Overview

The Python SDK provides both async and sync clients to match different application patterns. The async client uses httpx with asyncio for concurrent operations, while the sync client provides a blocking interface for scripts and simple integrations. Both clients share the same interface and models.

## Architecture

```
Client Class Hierarchy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VoiceAgent (Abstract Base)
├── AsyncVoiceAgent (async/await)
│   Uses: httpx.AsyncClient
│   Import: from voice_agent import AsyncVoiceAgent
│   Usage: async with AsyncVoiceAgent(api_key) as client:
│              agents = await client.agents.list()
│
└── SyncVoiceAgent (blocking)
    Uses: httpx.Client
    Import: from voice_agent import SyncVoiceAgent
    Usage: with SyncVoiceAgent(api_key) as client:
               agents = client.agents.list()

Usage Comparison:
  # Async (recommended for web frameworks)
  async def handle_request():
      async with AsyncVoiceAgent(api_key="va_live") as client:
          agent = await client.agents.create(config)
          calls = await client.calls.list(agent_id=agent.id)

  # Sync (recommended for scripts)
  def main():
      with SyncVoiceAgent(api_key="va_live") as client:
          agent = client.agents.create(config)
          calls = client.calls.list(agent_id=agent.id)

  # Mixed — run sync in async context
  async def mixed_usage():
      sync_client = SyncVoiceAgent(api_key="va_live")
      # Run blocking call in thread pool
      agent = await asyncio.to_thread(
          sync_client.agents.create, config
      )
```

## Design Decisions

- **Separate Classes**: AsyncVoiceAgent and SyncVoiceAgent — clear API separation, no magic dispatching
- **Context Manager Support**: Both clients support `async with` / `with` for proper cleanup
- **Shared Models**: Same Pydantic models for both clients — no duplication
- **httpx Over aiohttp**: httpx provides both sync and async in one package; consistent API

## Implementation Approach

```python
"""voice_agent/client.py"""

from __future__ import annotations

import abc
from typing import Optional, TypeVar
import httpx
from .config import ClientConfig, Environment
from .resources.agents import AsyncAgentsResource, SyncAgentsResource
from .resources.calls import AsyncCallsResource, SyncCallsResource
from .errors import map_response_error

T = TypeVar("T")


class BaseVoiceAgent(abc.ABC):
    """Abstract base for VoiceAgent clients."""

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

    @staticmethod
    def _get_default_url(environment: Environment) -> str:
        urls = {
            "production": "https://api.voiceagent.com",
            "sandbox": "https://api.sandbox.voiceagent.com",
            "development": "http://localhost:3000",
        }
        return urls.get(environment, urls["production"])

    def _build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "voice-agent-sdk/1.0",
        }


class AsyncVoiceAgent(BaseVoiceAgent):
    """Async VoiceAgent client for use with asyncio."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._client: Optional[httpx.AsyncClient] = None
        self.agents: AsyncAgentsResource | None = None
        self.calls: AsyncCallsResource | None = None

    async def __aenter__(self) -> AsyncVoiceAgent:
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers=self._build_headers(),
            timeout=self.config.timeout,
        )
        self.agents = AsyncAgentsResource(self._client)
        self.calls = AsyncCallsResource(self._client)
        return self

    async def __aexit__(self, *args) -> None:
        if self._client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> dict:
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")

        response = await self._client.request(
            method=method,
            url=path,
            params=params,
            json=body,
        )

        if not response.is_success:
            raise map_response_error(response)

        return response.json()


class SyncVoiceAgent(BaseVoiceAgent):
    """Sync VoiceAgent client for scripts and blocking code."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._client: Optional[httpx.Client] = None
        self.agents: SyncAgentsResource | None = None
        self.calls: SyncCallsResource | None = None

    def __enter__(self) -> SyncVoiceAgent:
        self._client = httpx.Client(
            base_url=self.config.base_url,
            headers=self._build_headers(),
            timeout=self.config.timeout,
        )
        self.agents = SyncAgentsResource(self._client)
        self.calls = SyncCallsResource(self._client)
        return self

    def __exit__(self, *args) -> None:
        if self._client:
            self._client.close()

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> dict:
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'with' context manager.")

        response = self._client.request(
            method=method,
            url=path,
            params=params,
            json=body,
        )

        if not response.is_success:
            raise map_response_error(response)

        return response.json()


# Convenience: Sync client is default import
VoiceAgent = SyncVoiceAgent
```

## Integration Points

- **FastAPI/Starlette**: AsyncVoiceAgent integrates naturally with async web frameworks
- **Celery/Background Tasks**: SyncVoiceAgent for task workers
- **CLI Scripts**: SyncVoiceAgent for command-line tools

## Production Considerations

- **Connection Pool Size**: Configure httpx pool limits for high-concurrency scenarios
- **Timeout Configuration**: Default 30-second timeout; adjust for long-running operations
- **Error Handling**: Both clients raise the same exception types — consistent error handling
- **Thread Safety**: Sync client is not thread-safe; create per-thread instances

## Open-Source Tools

- **httpx**: HTTP client with sync and async support
- **asyncio**: Standard library async/await support
