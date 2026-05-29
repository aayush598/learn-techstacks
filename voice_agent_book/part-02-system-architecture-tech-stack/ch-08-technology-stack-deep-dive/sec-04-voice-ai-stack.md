# Section 04: Voice & AI Stack

## Technology Overview

The voice and AI stack combines **Whisper** (speech-to-text), **Coqui TTS** (text-to-speech), **Silero VAD** (voice activity detection), **Vercel AI SDK** (LLM orchestration), and **LangChain** (agentic workflows) with **pgvector** for retrieval-augmented generation (RAG).

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VOICE & AI TECHNOLOGY STACK                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    VOICE PIPELINE                            │   │
│  │                                                              │   │
│  │  Audio Input                                                 │   │
│  │      │                                                       │   │
│  │      ▼                                                       │   │
│  │  ┌──────────────┐   ┌────────────────────────────────────┐  │   │
│  │  │  Silero VAD  │──→│  Voice Activity Detection         │  │   │
│  │  │  (ONNX)      │   │  • Speech/non-speech detection    │  │   │
│  │  │              │   │  • Start/end of speech             │  │   │
│  │  └──────────────┘   │  • Silence trimming                │  │   │
│  │         │           └────────────────────────────────────┘  │   │
│  │         ▼                                                   │   │
│  │  ┌──────────────┐   ┌────────────────────────────────────┐  │   │
│  │  │   Whisper    │──→│  Speech-to-Text (STT)             │  │   │
│  │  │  (faster-    │   │  • English: base.en (244MB)       │  │   │
│  │  │   whisper)   │   │  • Multilingual: small (769MB)    │  │   │
│  │  │              │   │  • Real-time: distil-large-v3     │  │   │
│  │  └──────────────┘   │  • Word-level timestamps          │  │   │
│  │         │           └────────────────────────────────────┘  │   │
│  │         ▼                                                   │   │
│  │  ┌──────────────┐   ┌────────────────────────────────────┐  │   │
│  │  │  AI Service   │──→│  LLM Orchestration               │  │   │
│  │  │  (Vercel AI   │   │  • Streaming text generation     │  │   │
│  │  │   SDK +       │   │  • Function calling              │  │   │
│  │  │   LangChain)  │   │  • RAG via pgvector              │  │   │
│  │  │              │   │  • Multi-turn conversation        │  │   │
│  │  └──────────────┘   │  • Agentic workflows              │  │   │
│  │         │           └────────────────────────────────────┘  │   │
│  │         ▼                                                   │   │
│  │  ┌──────────────┐   ┌────────────────────────────────────┐  │   │
│  │  │  Coqui TTS   │──→│  Text-to-Speech (TTS)             │  │   │
│  │  │  (XTTS v2)   │   │  • Voice cloning (5s sample)     │  │   │
│  │  │              │   │  • 17+ languages                   │  │   │
│  │  │              │   │  • Streaming audio output          │  │   │
│  │  └──────────────┘   │  • Emotion/style control           │  │   │
│  │                      └────────────────────────────────────┘  │   │
│  │         │                                                   │   │
│  │         ▼                                                   │   │
│  │  ┌──────────────┐                                           │   │
│  │  │  Audio Output│                                           │   │
│  │  └──────────────┘                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Model Serving:                                              │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Local GPU   │ │   API        │ │   Edge TPU       │    │   │
│  │  │  (NVIDIA     │ │  (OpenAI,    │ │   (Serverless    │    │   │
│  │  │   A10G/T4)   │ │   Anthropic) │ │   Inference)     │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## VAD Integration (Silero)

```typescript
import * as ort from 'onnxruntime-node';
import { SileroVAD } from 'silero-vad';

// VAD configuration
const vad = new SileroVAD({
  modelPath: '/models/silero_vad.onnx',
  sampleRate: 16000,
  windowSize: 512,       // 32ms at 16kHz
  threshold: 0.5,        // Speech probability threshold
  minSilenceMs: 500,     // Minimum silence to consider speech end
  speechPadMs: 300,      // Padding at speech boundaries
});

// Real-time VAD processing
async function processAudioChunk(chunk: Float32Array): Promise<VadResult> {
  const result = await vad.process(chunk);

  if (result.isSpeech) {
    return {
      isSpeech: true,
      confidence: result.confidence,
      startTime: result.timestamp,
    };
  }

  return { isSpeech: false, confidence: result.confidence };
}
```

## Whisper STT

```typescript
import { WhisperModel } from 'faster-whisper';

// Model initialization
const whisperModel = new WhisperModel('/models/whisper-base.en', {
  device: 'cuda',
  computeType: 'float16',
  numWorkers: 2,
});

// Transcription with word-level timestamps
interface TranscriptionResult {
  text: string;
  segments: {
    start: number;    // seconds
    end: number;
    text: string;
    confidence: number;
    words: { word: string; start: number; end: number; probability: number }[];
  }[];
  language: string;
}

async function transcribe(audioPath: string): Promise<TranscriptionResult> {
  const segments = await whisperModel.transcribe(audioPath, {
    language: 'en',
    task: 'transcribe',
    wordTimestamps: true,
    vadFilter: true,
    beamSize: 5,
  });

  return {
    text: segments.map(s => s.text).join(' '),
    segments: segments.map(s => ({
      start: s.start,
      end: s.end,
      text: s.text,
      confidence: s.avgLogprob,
      words: s.words.map(w => ({
        word: w.word,
        start: w.start,
        end: w.end,
        probability: w.probability,
      })),
    })),
    language: 'en',
  };
}
```

## LLM Orchestration (Vercel AI SDK + LangChain)

```typescript
import { openai } from '@ai-sdk/openai';
import { streamText, tool } from 'ai';
import { z } from 'zod';
import { RetrievalQAChain } from 'langchain/chains';
import { pgvectorStore } from '@/lib/vector-store';

// AI agent with tool calling
async function handleConversation(messages: Message[], context: ConversationContext) {
  const result = streamText({
    model: openai('gpt-4o-mini'),
    system: `You are a voice agent assistant. Current context:
      - Agent: ${context.agentName}
      - Tenant: ${context.tenantName}
      - Tools available: transfer call, lookup customer, check order status

      Keep responses concise and natural for voice.`,
    messages,
    tools: {
      transferCall: tool({
        description: 'Transfer call to a human agent',
        parameters: z.object({
          reason: z.string(),
          department: z.enum(['support', 'sales', 'billing']),
        }),
        execute: async ({ reason, department }) => {
          return await callService.transferToHuman(context.callId, department, reason);
        },
      }),
      lookupCustomer: tool({
        description: 'Look up customer by phone or account number',
        parameters: z.object({
          identifier: z.string(),
          type: z.enum(['phone', 'account']),
        }),
        execute: async ({ identifier, type }) => {
          const customer = await customerService.lookup(identifier, type);
          return customer ? JSON.stringify(customer) : 'Customer not found';
        },
      }),
    },
    maxSteps: 5,  // Allow multi-step tool calls
  });

  return result.toDataStreamResponse();
}
```

## RAG with pgvector

```typescript
import { OpenAIEmbeddings } from '@langchain/openai';
import { PGVectorStore } from '@langchain/community/vectorstores/pgvector';

const embeddings = new OpenAIEmbeddings({
  model: 'text-embedding-3-small',
  dimensions: 1536,
});

const vectorStore = await PGVectorStore.initialize(embeddings, {
  postgresConnectionOptions: {
    connectionString: process.env.DATABASE_URL,
  },
  tableName: 'agent_knowledge',
  columns: {
    idColumnName: 'id',
    contentColumnName: 'content',
    metadataColumnName: 'metadata',
  },
});

// Semantic search for RAG
async function queryKnowledgeBase(query: string, tenantId: string) {
  const results = await vectorStore.similaritySearch(query, 5, {
    tenantId,
  });
  return results.map(r => r.pageContent);
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| STT model | Whisper (faster-whisper) | Best accuracy, open-weight, C++ inference (fast) |
| TTS model | Coqui XTTS v2 | Voice cloning, multiple languages, open-source |
| VAD model | Silero VAD | Real-time, lightweight ONNX, high accuracy |
| LLM SDK | Vercel AI SDK | Streaming-first, tool calling, edge-compatible |
| Agent framework | LangChain | RAG chains, tool integration, memory management |
| Vector database | pgvector | No separate infrastructure, transactional consistency |

## Integration Points

- **Ch 01 (System Architecture)** — Voice pipeline integration with media server
- **Ch 03 (Database)** — pgvector schema for embeddings
- **Ch 04 (Real-Time)** — Streaming transcription via WebSocket
- **Ch 09 (Data Flow)** — Event-driven processing of transcription results

## Production Considerations

- **GPU Requirements**: Whisper base.en: 1GB VRAM; Coqui XTTS: 2GB VRAM; both run on NVIDIA T4/A10G
- **Latency Budget**: VAD < 10ms, STT < 500ms (real-time), LLM first token < 1s, TTS < 300ms
- **Batch Processing**: Transcription jobs batched every 30 seconds for cost efficiency
- **Model Caching**: Models loaded once at worker startup, shared across inference requests
- **Fallbacks**: If local GPU unavailable, fall back to OpenAI Whisper API / Google TTS
- **Audio Formats**: Input: PCM 16kHz mono, Opus; Output: PCM 16kHz mono, Mulaw
