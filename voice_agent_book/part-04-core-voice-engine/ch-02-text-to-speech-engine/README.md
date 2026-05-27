# Chapter 02: Text-to-Speech (TTS) Engine

> **Part:** 04 - Core Voice Engine

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [TTS Architecture Overview](sec-01-tts-architecture-overview.md) | TTS pipeline: Text in → SSML processing → Voice selection → Synthesis → Audio out |
| 02 | [Coqui TTS Integration](sec-02-coqui-tts-integration.md) | Self-hosted Coqui TTS, model selection (YourTTS, VITS), fine-tuning, GPU optimization |
| 03 | [Piper TTS for Edge Deployment](sec-03-piper-tts-edge-deployment.md) | Piper model format, ultra-fast inference, edge deployment, voice quality vs speed |
| 04 | [Voice Cloning System](sec-04-voice-cloning-system.md) | Voice sample collection, model fine-tuning, voice verification, ethical considerations |
| 05 | [SSML Support & Advanced Controls](sec-05-ssml-support-advanced-controls.md) | SSML tags (prosody, emphasis, break, say-as), custom pronunciation lexicon, amazon/azure SSML |
| 06 | [Emotion-Aware TTS](sec-06-emotion-aware-tts.md) | Emotion tags, tone mapping, sentiment-driven voice modulation, excitement/calm/sympathy |
| 07 | [Streaming TTS Output](sec-07-streaming-tts-output.md) | Chunked synthesis, streaming playback, first-byte latency, buffer management |
| 08 | [Voice Library Management](sec-08-voice-library-management.md) | Voice catalog, preview, licensing, voice metadata, gender/demographics |

---

## TTS Pipeline

```
Text In → SSML Parser → Voice Selector → Synthesizer → Audio Stream → Playback
                                                ↓
                                         Emotion Controller
                                                ↓
                                         Custom Lexicon
```

---

## Key Takeaways

- Coqui TTS for primary synthesis with voice cloning capability
- Piper TTS for edge/low-latency scenarios (under 50ms first byte)
- SSML support for fine-grained control over prosody, emphasis, and pronunciation
- Emotion-aware TTS: tone changes based on conversation sentiment
- Streaming output: first audio byte in under 100ms for natural conversation
- Voice cloning for custom brand voices with ethical safeguards
- 100+ voice library covering multiple languages and accents
