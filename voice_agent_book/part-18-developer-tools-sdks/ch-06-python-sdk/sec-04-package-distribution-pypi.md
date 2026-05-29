# Section 04: Package Distribution (PyPI)

## Overview

The Python SDK is distributed as a package on PyPI under the name `voice-agent-sdk`. The build system uses `pyproject.toml` with Poetry for dependency management, versioning, and publishing. CI/CD pipelines automate testing, building, and publishing to PyPI for every release.

## Architecture

```
Build & Distribution Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Development:
  [Developer] → [git commit] → [GitHub] → [CI Pipeline]
                                              │
                                     ┌────────┴────────┐
                                     │ PR (pre-release)│
                                     │   Run tests     │
                                     │   Build check   │
                                     │   Lint check    │
                                     └────────┬────────┘
                                              │
                                     ┌────────┴────────┐
                                     │ Main (release)  │
                                     │   Run tests     │
                                     │   Build package │
                                     │   Publish to    │
                                     │   Test PyPI     │
                                     └────────┬────────┘
                                              │
                                     ┌────────┴────────┐
                                     │ Tag v*          │
                                     │   Publish to    │
                                     │   PyPI          │
                                     └─────────────────┘

pyproject.toml Structure:
  [build-system]
  requires = ["poetry-core"]
  build-backend = "poetry.core.masonry.api"

  [tool.poetry]
  name = "voice-agent-sdk"
  version = "1.0.0"
  description = "Python SDK for the Voice Agent API"
  authors = ["Voice Agent Team <devs@voiceagent.com>"]
  license = "MIT"
  readme = "README.md"
  repository = "https://github.com/voiceagent/python-sdk"

  [tool.poetry.dependencies]
  python = "^3.9"
  httpx = "^0.27.0"
  pydantic = "^2.0.0"

  [tool.poetry.group.dev.dependencies]
  pytest = "^8.0"
  pytest-asyncio = "^0.23.0"
  mypy = "^1.8.0"
  ruff = "^0.3.0"
```

## Design Decisions

- **Poetry Over pip/setuptools**: Dependency resolution, lock files, and build system in one tool
- **Python 3.9+**: Minimum Python version — covers 95% of active Python installations
- **Minimal Dependencies**: Only httpx and Pydantic — no unnecessary transitive dependencies
- **Semantic Versioning**: Major.Minor.Patch — breaking changes, features, fixes

## Implementation Approach

```python
# pyproject.toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "voice-agent-sdk"
version = "1.0.0"
description = "Python SDK for the Voice Agent API"
authors = ["Voice Agent Team <devs@voiceagent.com>"]
license = "MIT"
readme = "README.md"
repository = "https://github.com/voiceagent/voice-agent-python"
homepage = "https://docs.voiceagent.com/sdks/python"
documentation = "https://docs.voiceagent.com/sdks/python/api"

[tool.poetry.dependencies]
python = "^3.9"
httpx = "^0.27.0"
pydantic = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-asyncio = "^0.23.0"
pytest-httpx = "^0.30.0"
mypy = "^1.8.0"
ruff = "^0.3.0"
pre-commit = "^3.6.0"

[tool.poetry.urls]
"Bug Tracker" = "https://github.com/voiceagent/voice-agent-python/issues"

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.mypy]
python_version = "3.9"
strict = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

```python
# Version management — single source of truth
# voice_agent/_version.py
__version__ = "1.0.0"


# Makefile for common operations
.PHONY: install test build publish

install:
	poetry install

test:
	poetry run pytest --cov=voice_agent --cov-report=term

lint:
	poetry run ruff check voice_agent tests
	poetry run mypy voice_agent

build:
	poetry build

publish:
	poetry publish

publish-test:
	poetry publish --repository test-pypi


# GitHub Actions CI workflow
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - uses: snok/install-poetry@v1
      - run: poetry install
      - run: poetry run pytest
      - run: poetry run ruff check voice_agent
      - run: poetry run mypy voice_agent

  publish:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: snok/install-poetry@v1
      - run: poetry install
      - run: poetry build
      - run: poetry publish --username __token__ --password ${{ secrets.PYPI_TOKEN }}
```

## Integration Points

- **PyPI**: Public package repository
- **Test PyPI**: Pre-release validation
- **Security Scanning**: Dependencies scanned for vulnerabilities via Dependabot

## Production Considerations

- **Two-Factor Auth**: PyPI requires 2FA for publishing
- **Trusted Publishing**: Use OIDC-based trusted publishing instead of API tokens
- **Release Notes**: Auto-generated changelog from conventional commits
- **Version Pinning**: Lock files committed to repository for reproducible builds

## Open-Source Tools

- **Poetry**: Python packaging and dependency management
- **PyPI**: Python Package Index
- **Trusted Publishers**: OIDC-based deployment to PyPI from GitHub Actions
