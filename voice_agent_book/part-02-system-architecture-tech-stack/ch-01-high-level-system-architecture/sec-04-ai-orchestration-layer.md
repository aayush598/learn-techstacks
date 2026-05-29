# Section 04: AI Orchestration Layer

## Orchestration Architecture

The AI Orchestration Layer is the **intelligence center** of the voice agent platform. It receives transcribed text from the voice pipeline, determines intent, retrieves relevant context, constructs prompts, executes tools, and generates responses. This layer coordinates multiple AI models and services to produce coherent, context-aware conversations.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       AI ORCHESTRATION LAYER                           │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                    INPUT PROCESSING                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │     │
│  │  │  Intent  │  │  Entity  │  │ Language │  │  Sentiment│      │     │
│  │  │  Router  │  │  Extract │  │  Detect  │  │  Analyze │       │     │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │     │
│  └───────┼──────────────┼──────────────┼──────────────┼───────────┘     │
│          │              │              │              │                 │
│  ┌───────┴──────────────┴──────────────┴──────────────┴───────────┐     │
│  │                    CONTEXT ASSEMBLY                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │     │
│  │  │  Agent   │  │  RAG     │  │  Memory  │  │  Call    │       │     │
│  │  │  Config  │  │  Engine  │  │  Manager │  │  Context │       │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                  │                                      │
│  ┌───────────────────────────────┴────────────────────────────────┐     │
│  │                    LLM ORCHESTRATION                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │     │
│  │  │  Prompt  │  │  Model   │  │  Tool    │  │ Response │       │     │
│  │  │  Builder │  │  Router  │  │  Executor│  │  Parser  │       │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                  │                                      │
│  ┌───────────────────────────────┴────────────────────────────────┐     │
│  │                    POST-PROCESSING                              │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │     │
│  │  │ Response │  │   TTS    │  │  Action  │  │  Event   │       │     │
│  │  │  Filter  │  │  Trigger │  │  Execute │  │  Emit    │       │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │     │
│  └────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Input Processing

```typescript
interface InputProcessor {
  intentRouter: IntentRouter
  entityExtractor: EntityExtractor
  languageDetector: LanguageDetector
  sentimentAnalyzer: SentimentAnalyzer
}

interface IntentRouter {
  classify(text: string, context: CallContext): Promise<IntentClassification>
}

interface IntentClassification {
  primaryIntent: 'greeting' | 'question' | 'complaint' | 'purchase' 
    | 'support' | 'transfer' | 'goodbye' | 'unknown'
  confidence: number
  subIntent?: string
  entities: ExtractedEntity[]
}

interface ExtractedEntity {
  type: 'product' | 'order_id' | 'date' | 'amount' | 'name' | 'email'
  value: string
  confidence: number
  span: { start: number, end: number }
}
```

### 2. RAG (Retrieval-Augmented Generation) Engine

The RAG engine retrieves relevant knowledge base documents to ground the AI's responses:

```typescript
interface RAGConfig {
  embeddingModel: 'text-embedding-3-small' | 'BAAI/bge-small-en-v1.5'
  chunkSize: 512
  chunkOverlap: 64
  topK: 5
  similarityThreshold: 0.7
  reranking: boolean
}

interface RAGEngine {
  embed(text: string): Promise<number[]>
  search(query: string, tenantId: string, topK?: number): Promise<KnowledgeDoc[]>
  rerank(query: string, docs: KnowledgeDoc[]): Promise<KnowledgeDoc[]>
}

interface KnowledgeDoc {
  id: string
  content: string
  metadata: {
    source: string
    chunkIndex: number
    pageNumber?: number
    docType: 'faq' | 'manual' | 'policy' | 'script'
  }
  score: number
  embedding: number[]  // pgvector
}
```

### 3. Memory Manager

The memory manager maintains conversation state across turns:

```typescript
interface MemoryManager {
  // Short-term memory (conversation context)
  currentTurn: {
    userInput: string
    aiResponse: string
    timestamp: number
  }

  // Working memory (call-level)
  workingMemory: {
    callId: string
    agentId: string
    callerInfo: {
      name?: string
      accountNumber?: string
      verifiedIdentity?: boolean
    }
    gatheredData: Record<string, unknown>
    pendingActions: Action[]
    state: CallState
  }

  // Long-term memory (cross-call, persisted)
  longTermMemory: {
    userId: string
    previousInteractions: Array<{
      date: string
      summary: string
      outcome: string
    }>
    preferences: Record<string, unknown>
    notes: string
  }
}
```

### 4. LLM Orchestration

The orchestrator manages which model to use and how to construct prompts:

```typescript
interface LLMOrchestrator {
  modelRouter: ModelRouter
  promptBuilder: PromptBuilder
  toolExecutor: ToolExecutor
  responseParser: ResponseParser
}

interface ModelRouter {
  selectModel(intent: string, complexity: number): ModelConfig
}

interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'openrouter' | 'local'
  model: string
  maxTokens: number
  temperature: number
  streaming: boolean
  costMultiplier: number
}

// Model routing decision tree
// Simple greeting → GPT-4o-mini (fast, cheap)
// Complex support → GPT-4o (accurate)
// Sensitive data → Local LLM (privacy)
// Escalation → Claude 3 Opus (nuanced)

interface PromptBuilder {
  build(context: OrchestrationContext): PromptTemplate
}

interface PromptTemplate {
  systemPrompt: string
  conversationHistory: Array<{ role: string; content: string }>
  contextDocuments: string[]
  tools: ToolDefinition[]
}

interface ToolDefinition {
  name: string
  description: string
  parameters: {
    type: 'object'
    properties: Record<string, unknown>
    required: string[]
  }
}
```

### 5. Tool Executor

Tools allow the AI to perform actions beyond conversation:

```typescript
interface ToolExecutor {
  availableTools: Map<string, Tool>
}

interface Tool {
  name: string
  description: string
  execute(params: Record<string, unknown>): Promise<ToolResult>
}

// Example tools
const tools: Tool[] = [
  {
    name: 'lookup_order',
    description: 'Look up order details by order ID',
    execute: async ({ orderId }) => {
      const order = await orderService.getOrder(orderId)
      return { success: true, data: order }
    }
  },
  {
    name: 'schedule_callback',
    description: 'Schedule a callback at a specific time',
    execute: async ({ phone, time, reason }) => {
      await campaignService.scheduleCallback(phone, time, reason)
      return { success: true }
    }
  },
  {
    name: 'transfer_to_human',
    description: 'Transfer call to human agent',
    execute: async ({ department, reason }) => {
      return { 
        success: true, 
        action: 'transfer',
        target: department,
        reason
      }
    }
  },
  {
    name: 'update_account',
    description: 'Update customer account information',
    execute: async ({ field, value }) => {
      // Requires verification first
      return { success: true, data: { field, value, updated: true } }
    }
  }
]
```

### 6. Response Parsing & Filtering

```typescript
interface ResponseParser {
  parse(rawResponse: string): ParsedResponse
}

interface ParsedResponse {
  text: string
  toolCalls?: Array<{
    name: string
    params: Record<string, unknown>
  }>
  stateTransition?: CallState
  emotions?: 'neutral' | 'empathetic' | 'urgent'
  suggestions?: string[]
}

interface ResponseFilter {
  // Content safety checks
  checkProfanity(text: string): boolean
  checkPII(text: string): boolean
  checkHallucination(text: string, sources: KnowledgeDoc[]): number
  formatResponse(text: string): string
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Model Provider | Multi-model (OpenAI + Anthropic + Local) | Cost optimization, privacy requirements |
| Embedding Model | text-embedding-3-small | Best quality/cost ratio for RAG |
| Vector Store | pgvector (PostgreSQL) | Reduces infrastructure complexity |
| Prompt Strategy | System prompt + few-shot examples | Consistent behavior, easy to modify |
| Tool Execution | Structured JSON mode | Reliable parsing vs free-form text |
| Streaming | Server-Sent Events for AI responses | Lower perceived latency |

## Integration Points

- **Part 05 (AI Conversation Intelligence)** — Deep dive into LLM orchestration
- **Part 13 (Knowledge Base)** — RAG engine integrates with knowledge base service
- **Part 04 (Core Voice Engine)** — AI layer consumes STT output, triggers TTS
- **Part 08 (Human Hand-off)** — Tool execution triggers escalation flow

## Production Considerations

- **Latency**: Target AI response generation under 500ms for streaming, 200ms for first token
- **Fallback**: If primary model fails, fall back to cheaper model. If all models fail, use scripted responses
- **Rate Limiting**: Per-tenant token limits to prevent cost abuse
- **Monitoring**: Track model latency, token usage, cost per call, hallucination scores
- **A/B Testing**: Ability to route calls to different model configurations for testing
- **Caching**: Common queries (greetings, FAQs) use cached responses to save cost
- **Cost Optimization**: Use smaller models for simple tasks, larger models for complex tasks
