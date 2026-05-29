# Section 08: SDK Maintenance & Versioning

## Overview

The Python SDK follows semantic versioning with a clear deprecation policy and changelog. Version bumps correspond to API compatibility levels: major for breaking changes, minor for new features, patch for bug fixes. Deprecated features emit warnings and are removed after two minor versions.

## Architecture

```
Versioning Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Semantic Versioning:
  voice-agent-sdk v2.3.1
                    │ │ │
                    │ │ └── Patch: bug fixes, no API changes
                    │ └──── Minor: new features, backward compatible
                    └────── Major: breaking changes

Version Alignment:
  SDK v2.x → API v2 (compatible)
  SDK v1.x → API v1 (legacy, deprecated)

Deprecation Policy:
  v2.0.0: Feature added, marked as "experimental"
  v2.1.0: Feature stable, no warnings
  v2.2.0: Feature deprecated, DeprecationWarning
  v2.3.0: Feature still available, warning continues
  v3.0.0: Feature removed

  Timeline: ~6 months from deprecation to removal

Changelog Format (Keep a Changelog):
  # Changelog

  ## [2.3.1] - 2025-06-01
  ### Fixed
  - Fixed connection pool leak on error responses
  - Fixed type hint for AgentConfig.greeting field

  ## [2.3.0] - 2025-05-15
  ### Added
  - Support for streaming transcription
  - New `client.stream_transcription()` method
  ### Deprecated
  - `client.calls.stream()` — use `client.stream_transcription()` instead
```

## Design Decisions

- **SemVer Strict**: Breaking changes require major version bump; no exceptions
- **Deprecation Warnings**: Python `warnings.warn()` with `DeprecationWarning` category
- **Changelog Automation**: `git-cliff` generates changelog from conventional commits
- **Backward Compatibility Guarantee**: Within a major version, all changes are backward compatible

## Implementation Approach

```python
# Deprecation handling
import warnings
import functools
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def deprecated(
    since: str,
    removal: str,
    alternative: str = "",
) -> Callable[[F], F]:
    """Decorator to mark a function as deprecated.

    Args:
        since: Version when deprecation was introduced.
        removal: Version when the feature will be removed.
        alternative: Suggested alternative.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = (
                f"{func.__name__} is deprecated since v{since} "
                f"and will be removed in v{removal}."
            )
            if alternative:
                message += f" Use {alternative} instead."

            warnings.warn(
                message,
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)
        return wrapper  # type: ignore
    return decorator


class AsyncCallsResource:
    @deprecated(since="2.3.0", removal="3.0.0", alternative="stream_transcription()")
    async def stream(self, call_id: str) -> None:
        """Deprecated: Use stream_transcription instead."""
        ...

    async def stream_transcription(self, call_id: str) -> AsyncIterator[TranscriptEvent]:
        """Stream real-time transcription for a call."""
        ...


# Version management
# voice_agent/_version.py
__version__ = "2.3.1"

# Version comparison utility
from packaging.version import Version


def check_sdk_compatibility(api_version: str) -> bool:
    """Check if SDK version is compatible with API version."""
    sdk_ver = Version(__version__)
    api_ver = Version(api_version)

    # Major version must match
    return sdk_ver.major == api_ver.major


# Changelog generation — git-cliff configuration
# cliff.toml
[changelog]
header = "# Changelog\n"
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }}
{%- endfor %}
{% endfor %}
"""

[git]
conventional_commits = true

# Pre-commit hook for version consistency
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: version-consistency
        name: Check version consistency
        entry: python scripts/check_version.py
        language: python
        files: ^voice_agent/_version\.py$


# Release workflow
# Makefile
.PHONY: release-patch release-minor release-major

release-patch:
	poetry version patch
	git add pyproject.toml voice_agent/_version.py
	git commit -m "chore: bump version to $(shell poetry version -s)"
	git tag v$(shell poetry version -s)
	git push && git push --tags

release-minor:
	poetry version minor
	git add pyproject.toml voice_agent/_version.py
	git commit -m "chore: bump version to $(shell poetry version -s)"
	git tag v$(shell poetry version -s)
	git push && git push --tags

release-major:
	poetry version major
	git add pyproject.toml voice_agent/_version.py
	git commit -m "chore: bump version to $(shell poetry version -s)"
	git tag v$(shell poetry version -s)
	git push && git push --tags
```

## Integration Points

- **PyPI**: Version published to PyPI; older versions remain available
- **Changelog**: Published to developer portal and GitHub Releases
- **CI/CD**: Automated release pipeline triggered by version tags

## Production Considerations

- **Version Pinning**: Users should pin SDK version in requirements.txt
- **Security Patches**: Backport critical security fixes to supported major versions
- **LTS Versions**: Major versions receive security patches for 12 months after successor release
- **Migration Guides**: Provide migration guides for each major version bump

## Open-Source Tools

- **git-cliff**: Changelog generation from conventional commits
- **packaging**: Version parsing and comparison
- **poetry**: Version management and publishing
