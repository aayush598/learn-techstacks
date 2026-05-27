# Part 04: Core Voice Engine

> **Duration:** Core Engine Phase (Weeks 4-8)  
> **Goal:** Build the real-time voice processing pipeline with STT, TTS, VAD, and audio processing capabilities.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Speech-to-Text (STT) Engine](ch-01-speech-to-text-engine/README.md) | Whisper integration, Deepgram API, real-time streaming, multi-language STT, custom vocabulary |
| 02 | [Text-to-Speech (TTS) Engine](ch-02-text-to-speech-engine/README.md) | Coqui TTS, Piper TTS, SSML support, voice cloning, emotion-aware TTS, streaming audio |
| 03 | [Voice Activity Detection (VAD)](ch-03-voice-activity-detection/README.md) | Silero VAD, WebRTC VAD, configurable sensitivity, endpoint detection, silence timeout |
| 04 | [Audio Processing Pipeline](ch-04-audio-processing-pipeline/README.md) | WebAudio API, audio codecs (Opus/PCM), sample rate conversion, resampling strategies |
| 05 | [Noise Cancellation & Echo Suppression](ch-05-noise-cancellation-echo-suppression/README.md) | RNNoise, WebRTC AEC, acoustic echo cancellation, background noise reduction |
| 06 | [Barge-In & Interruption Handling](ch-06-barge-in-interruption-handling/README.md) | Real-time interruption detection, graceful stop, context preservation, turn management |
| 07 | [Audio Streaming & Latency Optimization](ch-07-audio-streaming-latency-optimization/README.md) | WebSocket streaming, chunked transfer, adaptive bitrate, jitter buffer, latency budgeting |
| 08 | [DTMF Detection & Keypad Handling](ch-08-dtmf-detection-keypad-handling/README.md) | In-band DTMF detection, RFC 2833, SIP INFO, menu navigation via keypad |
| 09 | [Wake Word & Hotword Detection](ch-09-wake-word-hotword-detection/README.md) | Porcupine, Snowboy, custom wake word training, always-on listening, keyword spotting |
| 10 | [Audio Quality Monitoring](ch-10-audio-quality-monitoring/README.md) | MOS scoring, signal-to-noise ratio, clipping detection, bitrate monitoring, quality alerts |

---

## Voice Pipeline Architecture

```
Microphone → WebRTC → VAD → STT → LLM → TTS → Audio Out
                ↑         ↓                      ↓
           Noise Canc.   Barge-in Detect    Streaming Buffer
```

---

## Key Open-Source Tools

- **Whisper** (MIT) — Open-source STT (OpenAI)
- **Coqui TTS** (MIT) — Open-source TTS with voice cloning
- **Piper TTS** (MIT) — Fast neural TTS (Rhasspy)
- **Silero VAD** (MIT) — Production-grade VAD
- **RNNoise** (BSD) — Noise suppression library
- **WebRTC** (BSD) — Real-time communication
- **Porcupine** (Apache 2.0) — Wake word detection

---

## Learning Objectives

- Implement real-time STT with <200ms latency using streaming APIs
- Build a TTS system with natural prosody and emotion control
- Integrate VAD for accurate turn detection in conversations
- Create an audio processing pipeline with noise cancellation
- Handle interruptions and barge-in scenarios gracefully
- Optimize audio streaming for low-latency real-time communication
- Monitor and maintain audio quality across varying network conditions
