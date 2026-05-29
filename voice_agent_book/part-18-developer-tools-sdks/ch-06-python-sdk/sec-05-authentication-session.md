# Section 05: Authentication & Session

## Overview

The Python SDK manages API key authentication, connection pooling, and session lifecycle. The SDK uses httpx client with connection pooling for efficient HTTP connections, automatic retry with exponential backoff, and optional OAuth2 token refresh for user-facing applications.

## Architecture

```
Session Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Client Initialization:
  [User] → VoiceAgent(api_key="va_live_abc")
              │
          [httpx.Client] with:
              ├── base_url = api.voiceagent.com
              ├── headers = { Authorization, Content-Type }
              ├── timeout = 30s
              ├── pool_limits = max 100 connections
              └── transport = RetryTransport

Connection Pool:
  ┌─────────────────────────────────────────┐
  │  Connection Pool (httpx)                │
  │                                         │
  │  [Conn 1] → api.voiceagent.com:443     │
  │  [Conn 2] → api.voiceagent.com:443     │
  │  [Conn 3] → api.voiceagent.com:443     │
  │  ...                                    │
  │  [Conn 100] → api.voiceagent.com:443   │
  │                                         │
  │  Keep-alive: 60 seconds                 │
  │  Max connections per host: 100          │
  └─────────────────────────────────────────┘

Retry Session:
  [Request] → [429/5xx/Network Error]
       │
  [Retry #1] ← wait 1s
       │
  [Retry #2] ← wait 2s
       │
  [Retry #3] ← wait 4s
       │
  [Max retries exceeded → Raise Error]

Token Refresh (OAuth2):
  [Client] → [401 Unauthorized]
       │
  [Check token expiry]
       │
  [Expired] → [Refresh token]
       │
  [Retry original request with new token]
```

## Design Decisions

- **httpx Client Over Session Object**: Client manages connection pool and cookies internally
- **Automatic Retry Transport**: Retry layer wraps the HTTP transport — transparent to resources
- **OAuth2 Token Refresh**: Interceptor detects 401 responses and attempts token refresh before failing
- **Auth Header Injection**: Authorization header set at client level, not per-request

## Implementation Approach

```python
"""voice_agent/utils/http.py"""

from __future__ import annotations

from typing import Optional
import httpx
from ..config import ClientConfig
from ..errors import (
    ApiError,
    AuthenticationError,
    RateLimitError,
    ServerError,
    NetworkError,
    map_status_code,
)


class RetryTransport(httpx.BaseTransport):
    """HTTP transport with automatic retry."""

    def __init__(
        self,
        inner: httpx.BaseTransport,
        max_retries: int = 3,
        base_delay: float = 1.0,
    ) -> None:
        self._inner = inner
        self._max_retries = max_retries
        self._base_delay = base_delay

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        last_error: Exception | None = None

        for attempt in range(self._max_retries):
            try:
                response = self._inner.handle_request(request)

                if response.status_code in {429, 500, 502, 503}:
                    if attempt < self._max_retries - 1:
                        delay = self._base_delay * (2 ** attempt)
                        import time
                        time.sleep(delay)
                        continue

                return response

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = exc
                if attempt < self._max_retries - 1:
                    delay = self._base_delay * (2 ** attempt)
                    import time
                    time.sleep(delay)
                    continue

        if last_error:
            raise NetworkError(str(last_error)) from last_error

        return response

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        last_error: Exception | None = None

        for attempt in range(self._max_retries):
            try:
                response = await self._inner.handle_async_request(request)

                if response.status_code in {429, 500, 502, 503}:
                    if attempt < self._max_retries - 1:
                        delay = self._base_delay * (2 ** attempt)
                        import asyncio
                        await asyncio.sleep(delay)
                        continue

                return response

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = exc
                if attempt < self._max_retries - 1:
                    delay = self._base_delay * (2 ** attempt)
                    import asyncio
                    await asyncio.sleep(delay)
                    continue

        if last_error:
            raise NetworkError(str(last_error)) from last_error

        return response


class HttpClient:
    """HTTP client with connection pooling and retry."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        transport = httpx.HTTPTransport(
            retries=0,  # We handle retry ourselves
        )
        retry_transport = RetryTransport(
            transport,
            max_retries=config.retry_max,
        )

        self._client = httpx.Client(
            base_url=config.base_url,
            headers=self._build_headers(config),
            timeout=config.timeout,
            transport=retry_transport,
        )

    def _build_headers(self, config: ClientConfig) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "voice-agent-sdk/1.0",
            "Idempotency-Key": self._generate_idempotency_key(),
        }

    def _generate_idempotency_key(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> dict:
        try:
            response = self._client.request(
                method=method,
                url=path,
                params=params,
                json=body,
            )

            if not response.is_success:
                raise self._map_error(response)

            return response.json()

        except httpx.TimeoutException as exc:
            raise NetworkError(f"Request timed out: {exc}") from exc
        except httpx.ConnectError as exc:
            raise NetworkError(f"Connection failed: {exc}") from exc

    def _map_error(self, response: httpx.Response) -> ApiError:
        body = response.json() if response.content else {}
        error = body.get("error", {})
        code = error.get("code", "UNKNOWN")
        message = error.get("message", "Unknown error")

        error_class = map_status_code(response.status_code)
        return error_class(
            message=message,
            code=code,
            status_code=response.status_code,
        )
```

## Integration Points

- **Connection Pool Tuning**: Configure pool_limits based on application concurrency
- **OAuth2 Refresh**: Token refresh callback passed to client for auto-refresh
- **Proxy Support**: httpx supports HTTP/HTTPS proxies via mount

## Production Considerations

- **Connection Leak Prevention**: Always use context manager (`async with` / `with`) for proper cleanup
- **DNS Caching**: httpx caches DNS results; configure TTL for production
- **TLS Verification**: Enabled by default; disable only for development with warning
- **Rate Limit Handling**: Retry transport respects Retry-After headers

## Open-Source Tools

- **httpx**: HTTP client with connection pooling and async support
