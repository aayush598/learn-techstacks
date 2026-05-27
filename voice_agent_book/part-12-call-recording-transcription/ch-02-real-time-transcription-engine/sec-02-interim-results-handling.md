# Section: Interim Results Handling

Interim Results Handling is a core component of the real-time transcription engine. This section covers design, implementation, and operational patterns.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Real-Time Transcription Engine              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Audio In ──▶  Preprocessor ──▶  STT Engine ──▶  Out  │
│                    │                    │          │     │
│              ┌─────▼─────┐       ┌──────▼───────┐  │     │
│              │  VAD      │       │  Whisper/    │  │     │
│              │  AGC      │       │  Deepgram    │  │     │
│              │  Denoise  │       │  Provider    │  │     │
│              └───────────┘       └──────────────┘  │     │
│                                                     │     │
│              ┌──────────────────────────────────────┘     │
│              │  Stream Manager (WebSocket)               │
│              └───────────────────────────────────────────┘
```

## Design Considerations

**Low-latency streaming.** The engine processes audio in 100ms frames with 500ms hop size. Interim results are emitted every 300ms, with final results after endpoint detection.

**Provider abstraction.** Multiple STT providers are supported through a common interface. The provider selector routes based on language, cost, and latency requirements.

## Pseudo-code

```python
class TranscriptionEngine:
    def __init__(self):
        self.preprocessor = AudioPreprocessor(vad_threshold=0.3)
        self.provider = STTProviderSelector().select()
        self.stream = StreamManager()

    async def transcribe(self, audio_stream):
        async for chunk in audio_stream:
            processed = self.preprocessor.process(chunk)
            result = await self.provider.transcribe(processed)
            await self.stream.send(result)
```

## Open-Source Tools

- **Whisper** (MIT) — Open-source speech-to-text
- **WebRTC VAD** (BSD) — Voice activity detection
- **Triton Inference Server** (BSD) — GPU model serving

## Integration Points

The engine receives audio from the recording pipeline and produces text for the live transcript, keyword spotter, diarization system, and transcript storage.

## Production Considerations

- GPU resource management with dynamic model loading
- Latency SLAs: p50 < 500ms, p99 < 2s
- Fallback chain: primary → secondary → batch
- Connection pooling for WebSocket connections
- Audio quality monitoring and quality scoring
