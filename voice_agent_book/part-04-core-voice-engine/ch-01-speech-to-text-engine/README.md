# Chapter 01: Speech-to-Text (STT) Engine

> **Part:** 04 - Core Voice Engine

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [STT Architecture Overview](sec-01-stt-architecture-overview.md) | STT pipeline: Audio capture → Preprocessing → ASR → Post-processing → Output |
| 02 | [Whisper Integration](sec-02-whisper-integration.md) | OpenAI Whisper API, Whisper.cpp for self-hosting, model selection (base/large), GPU optimization |
| 03 | [Deepgram API Integration](sec-03-deepgram-api-integration.md) | Deepgram streaming API, Nova-2 model, real-time transcription, custom vocabulary |
| 04 | [Real-Time Streaming STT](sec-04-real-time-streaming-stt.md) | WebSocket streaming, interim results, utterance detection, end-of-speech detection |
| 05 | [Multi-Language STT](sec-05-multi-language-stt.md) | Language detection, per-call language config, language fallback, accent adaptation |
| 06 | [Custom Vocabulary & Named Entities](sec-06-custom-vocabulary-named-entities.md) | Brand names, technical terms, proper nouns, hotwords, phrase boosting |
| 07 | [STT Post-Processing](sec-07-stt-post-processing.md) | Punctuation restoration, capitalization, formatting, profanity filtering, correction |
| 08 | [STT Performance & Latency](sec-08-stt-performance-latency.md) | Sub-200ms target, model quantization, batching, edge inference, GPU vs CPU |

---

## STT Pipeline

```
Audio In → VAD Gate → Audio Buffer → Codec → Whisper/Deepgram → Post-Process → Text Out
                                          ↓
                                    Custom Vocab
                                          ↓
                                    Punctuation
```

---

## Key Takeaways

- Whisper for self-hosted (cost control), Deepgram for best accuracy (pay per use)
- Target: real-time transcription under 200ms end-to-end
- Interim results streamed for real-time display and interruption detection
- Custom vocabulary for brand names, technical terms, and industry jargon
- Post-processing: punctuation, capitalization, profanity filtering
- Fallback chain: Deepgram → Whisper → Web Speech API (graceful degradation)
