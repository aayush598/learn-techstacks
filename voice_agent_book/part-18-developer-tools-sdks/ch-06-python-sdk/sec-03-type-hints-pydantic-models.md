# Section 03: Type Hints & Pydantic Models

## Overview

Pydantic v2 models define request and response shapes for the Python SDK. Models provide automatic validation, serialization/deserialization, and IDE autocomplete. Type hints are used throughout the SDK for function signatures, enabling static type checking with mypy and Pyright.

## Architecture

```
Model Hierarchy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BaseModel (Pydantic)
├── Agent
│   ├── name: str
│   ├── status: AgentStatus
│   ├── voice: VoiceConfig
│   ├── model: ModelConfig
│   └── created_at: datetime
├── AgentConfig (request)
│   ├── name: str
│   ├── voice: VoiceConfig
│   └── model: ModelConfig
├── Call
│   ├── id: str
│   ├── agent_id: str
│   ├── status: CallStatus
│   └── duration_seconds: int
├── PaginationMeta
│   ├── cursor: str | None
│   ├── has_more: bool
│   └── total: int | None
└── ListResponse[T]
    ├── data: list[T]
    └── pagination: PaginationMeta

Type Checking:
  # IDE shows types on hover
  agent: Agent = await client.agents.get("ag_123")
  agent.name  # → str
  agent.status  # → AgentStatus (enum)

  # Invalid data caught at deserialization
  agent = Agent(**{"id": "ag_1", "status": "invalid_status"})
  # → ValidationError: Input should be 'draft', 'active', 'paused' or 'archived'
```

## Design Decisions

- **Pydantic v2 Over dataclasses**: Built-in validation, serialization, JSON Schema generation, discriminated unions
- **Separate Request/Response Models**: Request models may have optional fields; response models always return all fields
- **Enums for Status Fields**: Type-safe status transitions; IDE autocomplete for valid values
- **datetime Parsing**: ISO 8601 strings auto-parsed to datetime objects

## Implementation Approach

```python
"""voice_agent/models/common.py"""

from __future__ import annotations

from datetime import datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class PaginationMeta(BaseModel):
    cursor: Optional[str] = None
    has_more: bool = Field(alias="hasMore")
    total: Optional[int] = None


class ListResponse(BaseModel, Generic[T]):
    data: list[T]
    pagination: PaginationMeta


"""voice_agent/models/agent.py"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class VoiceProvider(str, Enum):
    ELEVENLABS = "elevenlabs"
    AZURE = "azure"
    GOOGLE = "google"
    AMAZON = "amazon"


class VoiceConfig(BaseModel):
    provider: VoiceProvider
    voice_id: str = Field(alias="voiceId")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class ModelConfig(BaseModel):
    provider: ModelProvider
    model: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, alias="maxTokens", ge=1, le=16384)


class Agent(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=100)
    status: AgentStatus
    voice: VoiceConfig
    model: ModelConfig
    greeting: Optional[str] = None
    timezone: str = "UTC"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True


class AgentConfig(BaseModel):
    """Request model for creating/updating an agent."""
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    voice: VoiceConfig
    model: ModelConfig
    greeting: Optional[str] = Field(default=None, max_length=1000)
    timezone: str = "UTC"


"""voice_agent/resources/agents.py"""

from typing import Optional
from ..models.agent import Agent, AgentConfig
from ..models.common import ListResponse


class AsyncAgentsResource:
    """Async agent resource client."""

    def __init__(self, client):
        self._client = client

    async def list(
        self,
        cursor: Optional[str] = None,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> ListResponse[Agent]:
        data = await self._client.request(
            "GET", "/v1/agents",
            params={"cursor": cursor, "limit": limit, "status": status},
        )
        return ListResponse[Agent].model_validate(data)

    async def get(self, agent_id: str) -> Agent:
        data = await self._client.request("GET", f"/v1/agents/{agent_id}")
        return Agent.model_validate(data)

    async def create(self, config: AgentConfig) -> Agent:
        data = await self._client.request(
            "POST", "/v1/agents",
            body=config.model_dump(by_alias=True),
        )
        return Agent.model_validate(data)

    async def update(self, agent_id: str, config: AgentConfig) -> Agent:
        data = await self._client.request(
            "PATCH", f"/v1/agents/{agent_id}",
            body=config.model_dump(by_alias=True, exclude_unset=True),
        )
        return Agent.model_validate(data)


# Type checking example — mypy validates this
def process_agent(agent: Agent) -> str:
    return f"Agent {agent.name} is {agent.status.value}"
```

## Integration Points

- **OpenAPI Compatibility**: Pydantic models generate JSON Schema matching the OpenAPI spec
- **IDE Support**: VSCode Pyright, PyCharm — full type hints and autocomplete
- **Serialization**: `model_dump()` for request bodies; `model_validate()` from response JSON

## Production Considerations

- **Model Versioning**: Models are versioned with the SDK; breaking changes require major version bump
- **Validation Performance**: Pydantic v2 is written in Rust — validation is fast (~5μs per model)
- **Forward Compatibility**: Models ignore unknown fields by default; new API fields don't break old SDKs
- **Alias Handling**: `by_alias=True` for camelCase → snake_case mapping

## Open-Source Tools

- **Pydantic v2**: Data validation and settings management
- **mypy / pyright**: Static type checking
