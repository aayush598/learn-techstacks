# Section 07: Python SDK Documentation

## Overview

The Python SDK documentation is generated from docstrings and published to the developer portal. MkDocs with the Material theme provides a clean, searchable documentation site. Documentation includes API reference (auto-generated), getting started guide, usage examples (Jupyter notebooks), and migration guides.

## Architecture

```
Documentation Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Source Code] → [Docstrings] → [MkDocs + mkdocstrings]
      │                              │
      │                              ├── Auto-generated API Reference
      │                              │   - All public modules
      │                              │   - All public classes/functions
      │                              │   - Type signatures
      │                              │   - Docstring descriptions
      │                              │
      │                              ├── Manual Pages (markdown)
      │                              │   - Getting started
      │                              │   - Authentication
      │                              │   - Usage examples
      │                              │   - Migration guides
      │                              │
      │                              └── Jupyter Notebooks
      │                                  - Interactive examples
      │                                  - Run in browser via Colab
      │
      └── [Type Hints] → [IDE Tooltips]
                             ├── VSCode hover: types, docstrings
                             └── PyCharm: inline documentation

Documentation Site Structure:
  docs/
  ├── index.md                    → Home page
  ├── getting-started.md          → Quickstart guide
  ├── authentication.md           → API key and OAuth2 setup
  ├── guides/
  │   ├── creating-agents.md      → Agent management
  │   ├── managing-calls.md       → Call lifecycle
  │   ├── streaming.md            → Real-time transcription
  │   └── webhooks.md             → Webhook handling
  ├── api-reference/
  │   ├── client.md               → VoiceAgent client
  │   ├── agents.md               → Agents resource
  │   ├── calls.md                → Calls resource
  │   └── models.md               → Pydantic models
  ├── migration.md                → Version migration guide
  └── notebooks/
      └── quickstart.ipynb        → Interactive notebook
```

## Design Decisions

- **mkdocstrings**: Auto-generates API reference from Google-style docstrings
- **Jupyter Notebooks**: Interactive examples that users can run locally or in Colab
- **Docstring Convention**: Google-style docstrings with types, Args, Returns, Raises sections
- **Versioned Documentation**: Multiple SDK versions documented; version selector in site

## Implementation Approach

```python
# Docstring style (Google)
from typing import Optional


class AgentsResource:
    """Client for Agent API operations.

    This resource provides methods to create, read, update, delete,
    and deploy AI voice agents.

    Usage:
        async with AsyncVoiceAgent(api_key) as client:
            agent = await client.agents.get("ag_123")
    """

    async def list(
        self,
        cursor: Optional[str] = None,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> ListResponse[Agent]:
        """List all agents for the authenticated tenant.

        Args:
            cursor: Pagination cursor from previous response.
            limit: Maximum number of agents to return (1-100).
            status: Filter by agent status.

        Returns:
            A paginated list of agents.

        Raises:
            AuthenticationError: If the API key is invalid.
            RateLimitError: If rate limit is exceeded.

        Example:
            async with AsyncVoiceAgent(api_key) as client:
                result = await client.agents.list(status="active")
                for agent in result.data:
                    print(agent.name)
        """
        ...


# mkdocs.yml
site_name: Voice Agent Python SDK
site_description: Python SDK for the Voice Agent API
repo_url: https://github.com/voiceagent/voice-agent-python

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - content.code.copy

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [voice_agent]
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Authentication: authentication.md
  - Guides:
      - Creating Agents: guides/creating-agents.md
      - Managing Calls: guides/managing-calls.md
      - Real-time Streaming: guides/streaming.md
      - Webhooks: guides/webhooks.md
  - API Reference:
      - Client: api-reference/client.md
      - Agents: api-reference/agents.md
      - Calls: api-reference/calls.md
      - Models: api-reference/models.md
  - Migration Guide: migration.md
  - Notebooks:
      - Quickstart: notebooks/quickstart.ipynb


# Generating API reference docs — mkdocstrings auto-generates from source
# api-reference/client.md
::: voice_agent.client.AsyncVoiceAgent
    handler: python

::: voice_agent.client.SyncVoiceAgent
    handler: python
```

## Integration Points

- **Developer Portal**: Documentation deployed alongside OpenAPI reference
- **CI/CD**: Doc build runs on every PR; deploy to GitHub Pages or docs.voiceagent.com
- **IDE Integration**: Docstrings provide inline documentation in VSCode/PyCharm

## Production Considerations

- **Documentation Testing**: Run code examples as doctests to verify they work
- **Broken Link Checking**: CI checks for broken links in documentation
- **API Reference Generation**: Auto-generate on every release to match SDK version
- **Search Functionality**: MkDocs Material includes client-side search

## Open-Source Tools

- **MkDocs**: Static site generator for documentation
- **MkDocs Material**: Clean, responsive theme
- **mkdocstrings**: Auto-generate API reference from docstrings
- **mkdocs-jupyter**: Embed Jupyter notebooks in documentation
