# Section 06: Streaming Response Handling

## Overview

The Python SDK supports streaming responses for real-time transcription, SSE event streams, and large response bodies. Streaming uses async generators for efficient memory usage and real-time processing. Backpressure handling ensures the SDK doesn't buffer excessive data in memory.

## Architecture

```
Streaming Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SSE Stream (Real-time Transcription):
  [Client] → GET /v1/calls/{id}/transcription/stream
       │
  [HTTP Connection — Transfer-Encoding: chunked]
       │
  data: {"type":"transcript","speaker":"agent","text":"Hello..."}
  data: {"type":"transcript","speaker":"caller","text":"Hi..."}
  data: {"type":"transcript","speaker":"agent","text":"How can I help?"}
       │
  [Async Generator:
    async for event in client.stream_transcription(call_id):
        print(f"[{event.speaker}] {event.text}")
  ]

Async Generator Pattern:
  async def stream_transcription(self, call_id: str) -> AsyncIterator[TranscriptEvent]:
      async with self._client.stream("GET", f"/v1/calls/{call_id}/transcription/stream") as response:
          async for line in response.aiter_lines():
              if line.startswith("data: "):
                  yield TranscriptEvent.model_validate_json(line[6:])

Event Stream (WebSocket Fallback):
  async for event in client.events.subscribe("call:call_123"):
      if event.type == "call.status_changed":
          print(f"Call status: {event.data.current_status}")
```

## Design Decisions

- **Async Generators**: Memory-efficient — processes events as they arrive, no buffering
- **Context Manager for Streams**: Ensures proper cleanup of streaming connections
- **Backpressure via asyncio**: Slow consumer naturally applies backpressure through the event loop
- **Automatic Reconnection**: SSE/event streams auto-reconnect with backoff

## Implementation Approach

```python
"""voice_agent/streaming/events.py"""

from __future__ import annotations

from typing import AsyncIterator, Optional, Callable, Awaitable
from datetime import datetime
import json
import asyncio
import httpx
from pydantic import BaseModel
from ..errors import ApiError


class EventEnvelope(BaseModel):
    type: str
    version: int
    id: str
    timestamp: datetime
    channel: str
    data: dict


class TranscriptSegment(BaseModel):
    speaker: str
    text: str
    start_time: float
    end_time: float
    confidence: float


class TranscriptEvent(BaseModel):
    type: str
    call_id: str
    segment: TranscriptSegment


class StreamClient:
    """Client for streaming API responses."""

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http = http_client

    async def stream_transcription(
        self,
        call_id: str,
    ) -> AsyncIterator[TranscriptEvent]:
        """Stream real-time transcription for a call."""
        url = f"/v1/calls/{call_id}/transcription/stream"

        async with self._http.stream("GET", url) as response:
            if not response.is_success:
                raise self._map_stream_error(response)

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])
                        yield TranscriptEvent.model_validate(data)
                    except (json.JSONDecodeError, ValueError):
                        continue  # Skip malformed events

    async def subscribe(
        self,
        channel: str,
        handler: Optional[Callable[[EventEnvelope], Awaitable[None]]] = None,
    ) -> AsyncIterator[EventEnvelope]:
        """Subscribe to events via SSE."""
        url = f"/v1/events/stream?channel={channel}"

        while True:
            try:
                async with self._http.stream("GET", url) as response:
                    if not response.is_success:
                        await asyncio.sleep(5)
                        continue

                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                event = EventEnvelope.model_validate_json(line[6:])
                                if handler:
                                    await handler(event)
                                yield event
                            except (json.JSONDecodeError, ValueError):
                                continue

            except (httpx.TransportError, httpx.TimeoutException):
                # Connection lost — reconnect with backoff
                await asyncio.sleep(1)

    async def stream_response(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
    ) -> AsyncIterator[bytes]:
        """Stream raw response body for large payloads."""
        async with self._http.stream(method, path, params=params) as response:
            if not response.is_success:
                raise self._map_stream_error(response)

            async for chunk in response.aiter_bytes():
                yield chunk

    def _map_stream_error(self, response: httpx.Response) -> ApiError:
        """Map streaming error responses to exceptions."""
        body = response.json() if response.content else {}
        error = body.get("error", {})
        code = error.get("code", "STREAM_ERROR")
        message = error.get("message", f"Stream failed with status {response.status_code}")

        from ..errors import map_status_code
        error_class = map_status_code(response.status_code)
        return error_class(
            message=message,
            code=code,
            status_code=response.status_code,
        )


# Usage examples
async def transcribe_call(call_id: str) -> None:
    client = StreamClient(http_client)

    async for event in client.stream_transcription(call_id):
        speaker = event.segment.speaker
        text = event.segment.text
        print(f"[{speaker}] {text}")


async def monitor_calls() -> None:
    async for event in client.subscribe("call:*"):
        if event.type == "call.status_changed":
            call_id = event.data["call_id"]
            status = event.data["current_status"]
            print(f"Call {call_id}: {status}")


# Backpressure example — slow consumer
async def slow_consumer() -> None:
    async for event in client.subscribe("call:*"):
        await process_event(event)  # Slow processing naturally applies backpressure
```

## Integration Points

- **httpx Streaming**: Uses httpx async streaming via `aiter_lines()` and `aiter_bytes()`
- **asyncio**: Backpressure managed by the event loop
- **SDK Event Handlers**: Stream events dispatched to registered handlers

## Production Considerations

- **Memory Management**: Streaming prevents loading entire responses into memory
- **Reconnection**: SSE streams auto-reconnect on connection loss with backoff
- **Cancellation**: Streams respect CancelledError for graceful shutdown
- **Timeout Configuration**: Stream timeout separate from request timeout; configure for long-lived streams

## Open-Source Tools

- **httpx**: Async HTTP client with streaming support
- **asyncio**: Standard library for async/await patterns
