# Tech Stack for AI-Powered SaaS

## The AI SaaS Landscape

Building an AI-powered SaaS is fundamentally different from building a traditional SaaS. Your stack needs to handle LLM API calls, vector storage, prompt management, streaming responses, and token cost optimization — all while maintaining the reliability users expect from a SaaS product.

This guide covers the complete tech stack for AI SaaS, from LLM providers to prompt management to deployment, with concrete patterns and code examples.

## The AI SaaS Architecture

### High-Level Architecture

```
[Browser] → [Frontend (Next.js/React)]
                ↓
         [API Gateway / Backend]
            ↓           ↓           ↓
     [LLM Service]  [Auth]    [Payment]
            ↓
     [Prompt Manager]
            ↓
     [Vector DB] ← → [Document Store]
            ↓
     [LLM Provider(s)]
            ↓
     [Cache Layer]
```

### Component Diagram

```
┌─────────────────────────────────────────────┐
│              Frontend (Next.js)              │
│  - UI Components                            │
│  - Streaming Response Display               │
│  - Real-time Updates                        │
│  - Auth Integration (Clerk/Auth0)          │
└─────────────────┬───────────────────────────┘
                  │ HTTP / WebSocket
┌─────────────────▼───────────────────────────┐
│           API Backend (Node.js/Python)       │
│                                             │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Auth Service │  │  LLM Orchestrator   │  │
│  └─────────────┘  │  - Rate Limiting     │  │
│                   │  - Cost Tracking     │  │
│  ┌─────────────┐  │  - Fallback Logic    │  │
│  │ Billing     │  │  - Prompt Assembly   │  │
│  └─────────────┘  └──────────┬──────────┘  │
│                              │              │
│  ┌─────────────┐             │              │
│  │ Usage       │             │              │
│  │ Analytics   │             │              │
│  └─────────────┘             │              │
└──────────────────────────────┼──────────────┘
                               │
    ┌──────────────────────────┼──────────────────────┐
    │                          │                      │
┌───▼──────┐          ┌───────▼───────┐    ┌─────────▼──┐
│ LLM API  │          │ Vector Store  │    │  Cache     │
│ (OpenAI, │          │ (Pinecone,    │    │  (Redis,   │
│ Anthropic,│          │  Supabase/pgvector) │  Upstash) │
│ Cohere)  │          │               │    │            │
└──────────┘          └───────────────┘    └────────────┘
```

## LLM Provider Selection

### Provider Comparison

```
| Provider    | Models                      | Pricing            | Best For                     |
|-------------|-----------------------------|--------------------|------------------------------|
| OpenAI      | GPT-4o, GPT-4o-mini, o1    | $2.50-10/M tokens  | General purpose, high quality|
| Anthropic   | Claude 3.5 Sonnet, Haiku    | $3-15/M tokens     | Code, analysis, safety       |
| Google      | Gemini 1.5 Pro, Flash       | $1.25-5/M tokens   | Long context, multimodal     |
| Mistral AI  | Mistral Large, Small        | $2-8/M tokens      | European hosting, open models|
| Cohere      | Command R+, Command R       | $2.50-5/M tokens   | RAG, embedding, enterprise   |
| AWS Bedrock | Various models              | Per-model pricing  | AWS integration, compliance  |
| Azure OpenAI| OpenAI models               | Per-model pricing  | Enterprise, Microsoft shop   |
| Together    | Open models (Llama, etc)    | $0.10-2.40/M tokens| Open source models, low cost |
| Groq        | Llama, Mixtral (fast)       | $0.27-0.79/M tokens| Fast inference, low cost     |
```

### Provider Strategy

```
Primary + Fallback Strategy:

Strategy 1: Single Provider (Simplest)
  - Only use OpenAI (GPT-4o-mini for cost, GPT-4o for quality)
  - Best for: MVP, simple use cases
  - Risk: Provider outage = product outage

Strategy 2: Primary + Fallback
  - Primary: OpenAI GPT-4o (high quality, most capable)
  - Fallback: Anthropic Claude (when OpenAI is down)
  - Best for: Production reliability

Strategy 3: Tiered Model Access
  - Cheap model: GPT-4o-mini or Claude Haiku (simple queries)
  - Medium model: GPT-4o or Claude Sonnet (default)
  - Premium model: o1 or Claude Opus (complex reasoning)
  - Best for: Cost optimization, quality differentiation

Strategy 4: Open Source + API Fallback
  - Primary: Self-hosted Llama 3 or Mistral (lower cost)
  - Fallback: OpenAI API (when open source isn't good enough)
  - Best for: High volume, data privacy requirements
```

### Multi-Provider Client Example

```typescript
// lib/llm/client.ts
// Abstraction over multiple LLM providers

interface LLMRequest {
  model: string;
  messages: Array<{ role: 'system' | 'user' | 'assistant'; content: string }>;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
}

interface LLMResponse {
  content: string;
  model: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  latency: number;
}

interface LLMProvider {
  name: string;
  generate(req: LLMRequest): Promise<LLMResponse>;
  generateStream(req: LLMRequest): AsyncIterable<string>;
}

class OpenAIProvider implements LLMProvider {
  name = 'openai';
  private client: OpenAI;

  constructor() {
    this.client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }

  async generate(req: LLMRequest): Promise<LLMResponse> {
    const start = Date.now();
    const response = await this.client.chat.completions.create({
      model: req.model,
      messages: req.messages,
      temperature: req.temperature ?? 0.7,
      max_tokens: req.maxTokens,
    });
    return {
      content: response.choices[0]?.message?.content || '',
      model: response.model,
      usage: {
        promptTokens: response.usage?.prompt_tokens || 0,
        completionTokens: response.usage?.completion_tokens || 0,
        totalTokens: response.usage?.total_tokens || 0,
      },
      latency: Date.now() - start,
    };
  }
}

class AnthropicProvider implements LLMProvider {
  name = 'anthropic';
  private client: Anthropic;

  constructor() {
    this.client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }

  async generate(req: LLMRequest): Promise<LLMResponse> {
    const start = Date.now();
    const response = await this.client.messages.create({
      model: req.model,
      messages: req.messages.filter(m => m.role !== 'system'),
      system: req.messages.find(m => m.role === 'system')?.content,
      max_tokens: req.maxTokens ?? 4096,
      temperature: req.temperature ?? 0.7,
    });
    return {
      content: response.content[0]?.text || '',
      model: response.model,
      usage: {
        promptTokens: response.usage?.input_tokens || 0,
        completionTokens: response.usage?.output_tokens || 0,
        totalTokens: (response.usage?.input_tokens || 0) + (response.usage?.output_tokens || 0),
      },
      latency: Date.now() - start,
    };
  }
}

class LLMClient {
  private providers: Map<string, LLMProvider>;
  private fallbackOrder: string[];

  constructor(config: {
    primary: string;
    fallbacks?: string[];
  }) {
    this.providers = new Map();
    this.fallbackOrder = [config.primary, ...(config.fallbacks || [])];

    this.registerProvider('openai', new OpenAIProvider());
    this.registerProvider('anthropic', new AnthropicProvider());
  }

  registerProvider(name: string, provider: LLMProvider) {
    this.providers.set(name, provider);
  }

  async generate(req: LLMRequest): Promise<LLMResponse & { provider: string }> {
    let lastError: Error | null = null;

    for (const providerName of this.fallbackOrder) {
      const provider = this.providers.get(providerName);
      if (!provider) continue;

      try {
        const response = await provider.generate(req);
        return { ...response, provider: providerName };
      } catch (error) {
        lastError = error as Error;
        console.warn(`Provider ${providerName} failed:`, error);
        // Continue to next provider
      }
    }

    throw new Error(`All providers failed. Last error: ${lastError?.message}`);
  }
}

export const llmClient = new LLMClient({
  primary: 'openai',
  fallbacks: ['anthropic'],
});
```

## Vector Database Selection

### Options Comparison

```markdown
| Solution       | Type           | Cost Start    | Best For                  |
|----------------|----------------|---------------|---------------------------|
| pgvector       | Postgres exten | $0 (existing) | Simplicity, one less DB   |
| Pinecone       | Managed        | $70/mo        | Scale, performance        |
| Supabase       | Managed pvec   | $0 (free tier)| Simplicity, all-in-one    |
| Weaviate       | Self-hosted    | $0            | Flexibility, open source  |
| Qdrant         | Self-hosted    | $0            | Performance, filtering    |
| Chroma         | Embedded       | $0            | Development, small scale  |
| Milvus         | Self-hosted    | $0            | Large scale, complex needs|
| Redis Stack    | With Redis     | $0 (existing) | Caching + vectors         |
| LanceDB        | Embedded       | $0            | Columnar, multi-modal     |
```

### The pgvector Approach (Recommended for Solo Founders)

Use pgvector unless you have specific reasons not to. It keeps your stack simple — one database instead of two.

```sql
-- Enable the extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create an embeddings table
CREATE TABLE document_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  embedding vector(1536), -- OpenAI embeddings are 1536 dimensions
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX idx_document_embeddings_embedding
  ON document_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- For better performance at larger scale, use HNSW index:
-- CREATE INDEX idx_document_embeddings_hnsw
--   ON document_embeddings
--   USING hnsw (embedding vector_cosine_ops);
```

```typescript
// lib/rag/vector-store.ts
// Vector store abstraction using pgvector

import { Pool } from 'pg';

export class VectorStore {
  constructor(private pool: Pool) {}

  async storeEmbedding(params: {
    documentId: string;
    content: string;
    embedding: number[];
    metadata?: Record<string, any>;
  }) {
    await this.pool.query(
      `INSERT INTO document_embeddings
       (document_id, content, embedding, metadata)
       VALUES ($1, $2, $3::vector, $4)`,
      [
        params.documentId,
        params.content,
        JSON.stringify(params.embedding),
        JSON.stringify(params.metadata || {}),
      ]
    );
  }

  async searchSimilar(params: {
    embedding: number[];
    limit?: number;
    threshold?: number;
    filter?: Record<string, any>;
  }): Promise<Array<{
    documentId: string;
    content: string;
    similarity: number;
    metadata: Record<string, any>;
  }>> {
    const { embedding, limit = 10, threshold = 0.7, filter } = params;

    // Build filter conditions
    let filterClause = '';
    const values: any[] = [JSON.stringify(embedding), limit];

    if (filter) {
      const conditions = Object.entries(filter).map(([key, value], i) => {
        values.push(value);
        return `metadata->>'${key}' = $${values.length}`;
      });
      if (conditions.length > 0) {
        filterClause = `AND ${conditions.join(' AND ')}`;
      }
    }

    const result = await this.pool.query(
      `SELECT
         document_id, content,
         1 - (embedding <=> $1::vector) AS similarity,
         metadata
       FROM document_embeddings
       WHERE 1 - (embedding <=> $1::vector) > $${values.length + 1}
       ${filterClause}
       ORDER BY embedding <=> $1::vector
       LIMIT $2`,
      [...values, threshold]
    );

    return result.rows.map(row => ({
      documentId: row.document_id,
      content: row.content,
      similarity: row.similarity,
      metadata: row.metadata,
    }));
  }

  async deleteByDocumentId(documentId: string) {
    await this.pool.query(
      'DELETE FROM document_embeddings WHERE document_id = $1',
      [documentId]
    );
  }
}
```

## Embedding Generation

```typescript
// lib/rag/embeddings.ts
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small', // 1536 dimensions, $0.02/1M tokens
    input: text,
  });
  return response.data[0].embedding;
}

// For batch processing (much cheaper and faster)
export async function generateEmbeddings(texts: string[]): Promise<number[][]> {
  // Batch up to 2048 texts per request
  const batches = [];
  for (let i = 0; i < texts.length; i += 100) {
    batches.push(texts.slice(i, i + 100));
  }

  const results: number[][] = [];
  for (const batch of batches) {
    const response = await openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: batch,
    });
    results.push(...response.data.map(d => d.embedding));
  }

  return results;
}
```

## RAG (Retrieval-Augmented Generation) Implementation

```typescript
// lib/rag/rag-pipeline.ts
// Complete RAG pipeline: retrieve context, assemble prompt, generate response

import { VectorStore } from './vector-store';
import { generateEmbedding } from './embeddings';
import { llmClient } from '@/lib/llm/client';

interface RAGRequest {
  query: string;
  userId: string;
  documentIds?: string[]; // Filter to specific documents
  maxContextLength?: number; // Max characters of context to include
}

interface RAGResponse {
  answer: string;
  sources: Array<{
    documentId: string;
    content: string;
    similarity: number;
  }>;
  usage: {
    totalTokens: number;
    cost: number;
  };
}

export class RAGPipeline {
  constructor(
    private vectorStore: VectorStore,
    private systemPrompt: string = `You are a helpful assistant. Answer the user's question
      based on the provided context. If the context doesn't contain enough information,
      say so clearly. Always cite your sources by referencing the document content.`
  ) {}

  async query(request: RAGRequest): Promise<RAGResponse> {
    // 1. Generate embedding for the query
    const queryEmbedding = await generateEmbedding(request.query);

    // 2. Retrieve relevant context
    const results = await this.vectorStore.searchSimilar({
      embedding: queryEmbedding,
      limit: 5,
      threshold: 0.7,
      filter: request.documentIds
        ? { document_id: request.documentIds } // Will need array handling
        : undefined,
    });

    // 3. Assemble context
    const context = results
      .map(r => r.content)
      .join('\n\n---\n\n')
      .slice(0, request.maxContextLength || 4000);

    // 4. Generate response with context
    const response = await llmClient.generate({
      model: 'gpt-4o-mini', // Cost-effective for RAG
      messages: [
        { role: 'system', content: this.systemPrompt },
        { role: 'user', content: `Context:\n${context}\n\nQuestion: ${request.query}` },
      ],
      temperature: 0.3, // Lower temperature for factual answers
    });

    // 5. Calculate cost
    const cost = this.calculateCost(response.usage);

    return {
      answer: response.content,
      sources: results.map(r => ({
        documentId: r.documentId,
        content: r.content.slice(0, 200), // Truncate for response
        similarity: r.similarity,
      })),
      usage: {
        totalTokens: response.usage.totalTokens,
        cost,
      },
    };
  }

  private calculateCost(usage: { promptTokens: number; completionTokens: number; totalTokens: number }): number {
    // GPT-4o-mini pricing: $0.15/1M input tokens, $0.60/1M output tokens
    const inputCost = (usage.promptTokens / 1_000_000) * 0.15;
    const outputCost = (usage.completionTokens / 1_000_000) * 0.60;
    return inputCost + outputCost;
  }
}
```

## Prompt Management

### Prompt Templates

```typescript
// lib/prompts/templates.ts
// Centralized prompt management

export const promptTemplates = {
  summarize: {
    system: `You are a summarization assistant. Summarize the following text
      in a clear, concise manner. Maintain key facts and figures.
      Length: {length}`,
    user: `Text to summarize:\n{text}`,
  },

  extract: {
    system: `Extract structured information from the text.
      Return the information as a JSON object with the following fields:
      {schema}`,
    user: `Text:\n{text}`,
  },

  chat: {
    system: `You are an AI assistant for {product_name}.
      Context about the user: {user_context}
      Previous messages: {history}
      Knowledge base: {knowledge_base}

      Guidelines:
      - Be concise and helpful
      - Use the provided context to answer questions
      - If you don't know something, say so
      - {additional_guidelines}`,
    user: `{message}`,
  },

  generate: {
    system: `Generate {content_type} based on the following requirements.
      Tone: {tone}
      Length: {length}
      Target audience: {audience}
      Style guidelines: {style_guidelines}`,
    user: `Requirements:\n{requirements}`,
  },
};

type PromptTemplate = keyof typeof promptTemplates;

export function renderPrompt<T extends PromptTemplate>(
  template: T,
  variables: Record<string, string>
): { system: string; user: string } {
  const tmpl = promptTemplates[template];

  const system = tmpl.system.replace(
    /{(\w+)}/g,
    (_, key) => variables[key] || `{${key}}`
  );

  const user = tmpl.user.replace(
    /{(\w+)}/g,
    (_, key) => variables[key] || `{${key}}`
  );

  return { system, user };
}
```

### Prompt Versioning

```typescript
// lib/prompts/versioning.ts
// Track prompt versions for A/B testing and rollback

interface PromptVersion {
  id: string;
  name: string;
  version: number;
  systemPrompt: string;
  userPrompt: string;
  model: string;
  temperature: number;
  maxTokens: number;
  createdAt: Date;
  isActive: boolean;
}

class PromptManager {
  private versions: Map<string, PromptVersion[]> = new Map();
  private activeVersions: Map<string, PromptVersion> = new Map();

  async createVersion(params: {
    name: string;
    systemPrompt: string;
    userPrompt: string;
    model: string;
    temperature?: number;
    maxTokens?: number;
  }): Promise<PromptVersion> {
    const existing = this.activeVersions.get(params.name);
    const version: PromptVersion = {
      id: crypto.randomUUID(),
      name: params.name,
      version: (existing?.version || 0) + 1,
      systemPrompt: params.systemPrompt,
      userPrompt: params.userPrompt,
      model: params.model,
      temperature: params.temperature ?? 0.7,
      maxTokens: params.maxTokens ?? 2048,
      createdAt: new Date(),
      isActive: true,
    };

    // Deactivate previous version
    if (existing) {
      existing.isActive = false;
    }

    // Store version
    if (!this.versions.has(params.name)) {
      this.versions.set(params.name, []);
    }
    this.versions.get(params.name)!.push(version);
    this.activeVersions.set(params.name, version);

    // Persist to database
    await this.persistVersion(version);

    return version;
  }

  getActiveVersion(name: string): PromptVersion | undefined {
    return this.activeVersions.get(name);
  }

  async rollback(name: string, targetVersion: number): Promise<PromptVersion> {
    const versions = this.versions.get(name) || [];
    const target = versions.find(v => v.version === targetVersion);
    if (!target) throw new Error(`Version ${targetVersion} not found`);

    // Deactivate current
    const current = this.activeVersions.get(name);
    if (current) {
      current.isActive = false;
      await this.persistVersion(current);
    }

    // Reactivate target
    target.isActive = true;
    this.activeVersions.set(name, target);
    await this.persistVersion(target);

    return target;
  }

  private async persistVersion(version: PromptVersion) {
    // Store in database for persistence
    await db.query(
      `INSERT INTO prompt_versions (id, name, version, system_prompt,
        user_prompt, model, temperature, max_tokens, is_active)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
       ON CONFLICT (id) DO UPDATE SET is_active = $9`,
      [version.id, version.name, version.version,
       version.systemPrompt, version.userPrompt, version.model,
       version.temperature, version.maxTokens, version.isActive]
    );
  }
}

export const promptManager = new PromptManager();
```

## Streaming Responses

```typescript
// app/api/chat/stream/route.ts (Next.js App Router)
// Stream LLM responses to the client

import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST(req: Request) {
  const { messages } = await req.json();

  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    stream: true,
    messages: [
      {
        role: 'system',
        content: 'You are a helpful assistant for a SaaS product.',
      },
      ...messages,
    ],
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
```

```typescript
// Client-side streaming consumption
// app/chat/page.tsx

'use client';

import { useChat } from 'ai/react';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat/stream',
  });

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          <strong>{m.role}:</strong> {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## Cost Tracking and Rate Limiting

### Token Usage Tracking

```typescript
// lib/llm/cost-tracker.ts

interface UsageRecord {
  userId: string;
  requestId: string;
  provider: string;
  model: string;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  cost: number;
  timestamp: Date;
}

class CostTracker {
  private readonly COST_PER_TOKEN: Record<string, { input: number; output: number }> = {
    'gpt-4o': { input: 5.0 / 1_000_000, output: 15.0 / 1_000_000 },
    'gpt-4o-mini': { input: 0.15 / 1_000_000, output: 0.60 / 1_000_000 },
    'gpt-4': { input: 30.0 / 1_000_000, output: 60.0 / 1_000_000 },
    'claude-3-5-sonnet': { input: 3.0 / 1_000_000, output: 15.0 / 1_000_000 },
    'claude-3-haiku': { input: 0.25 / 1_000_000, output: 1.25 / 1_000_000 },
    'text-embedding-3-small': { input: 0.02 / 1_000_000, output: 0.02 / 1_000_000 },
  };

  calculateCost(model: string, promptTokens: number, completionTokens: number): number {
    const pricing = this.COST_PER_TOKEN[model];
    if (!pricing) return 0;

    const inputCost = (promptTokens * pricing.input);
    const outputCost = (completionTokens * pricing.output);
    return inputCost + outputCost;
  }

  async recordUsage(record: UsageRecord) {
    await db.query(
      `INSERT INTO llm_usage
       (user_id, request_id, provider, model,
        prompt_tokens, completion_tokens, total_tokens, cost)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
      [record.userId, record.requestId, record.provider,
       record.model, record.promptTokens, record.completionTokens,
       record.totalTokens, record.cost]
    );
  }

  async getUserUsage(userId: string, period: 'day' | 'month'): Promise<{
    totalTokens: number;
    totalCost: number;
    requestCount: number;
  }> {
    const interval = period === 'day' ? '24 hours' : '30 days';

    const result = await db.query(
      `SELECT
         COALESCE(SUM(total_tokens), 0) as total_tokens,
         COALESCE(SUM(cost), 0) as total_cost,
         COUNT(*) as request_count
       FROM llm_usage
       WHERE user_id = $1
         AND timestamp > NOW() - INTERVAL '${interval}'`,
      [userId]
    );

    return {
      totalTokens: parseInt(result.rows[0].total_tokens),
      totalCost: parseFloat(result.rows[0].total_cost),
      requestCount: parseInt(result.rows[0].request_count),
    };
  }
}

export const costTracker = new CostTracker();
```

### Rate Limiting

```typescript
// lib/llm/rate-limiter.ts

interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
  maxTokensPerRequest?: number;
}

class LLMRateLimiter {
  private limits: Map<string, RateLimitConfig> = new Map();

  constructor() {
    // Default limits per user tier
    this.limits.set('free', {
      maxRequests: 20,
      windowMs: 60 * 60 * 1000, // 1 hour
      maxTokensPerRequest: 2000,
    });
    this.limits.set('pro', {
      maxRequests: 500,
      windowMs: 60 * 60 * 1000,
      maxTokensPerRequest: 8000,
    });
    this.limits.set('enterprise', {
      maxRequests: 5000,
      windowMs: 60 * 60 * 1000,
      maxTokensPerRequest: 16000,
    });
  }

  async checkLimit(userId: string, tier: string): Promise<{
    allowed: boolean;
    remaining: number;
    resetTime: Date;
  }> {
    const config = this.limits.get(tier) || this.limits.get('free')!;

    const result = await db.query(
      `SELECT
         COUNT(*) as request_count,
         MAX(timestamp) as last_request
       FROM llm_usage
       WHERE user_id = $1
         AND timestamp > NOW() - ($2 || ' milliseconds')::interval`,
      [userId, config.windowMs]
    );

    const currentCount = parseInt(result.rows[0].request_count);
    const remaining = Math.max(0, config.maxRequests - currentCount);
    const resetTime = new Date(Date.now() + config.windowMs);

    return {
      allowed: remaining > 0,
      remaining,
      resetTime,
    };
  }
}

export const rateLimiter = new LLMRateLimiter();
```

## Caching LLM Responses

```typescript
// lib/llm/cache.ts
// Cache identical requests to reduce costs and latency

import { createHash } from 'crypto';

class LLMCache {
  constructor(private ttlMs: number = 3600_000) {} // 1 hour default

  private generateKey(request: {
    model: string;
    messages: Array<{ role: string; content: string }>;
    temperature?: number;
  }): string {
    const hash = createHash('sha256');
    hash.update(JSON.stringify(request));
    return `llm:${hash.digest('hex')}`;
  }

  async get(
    request: Parameters<LLMCache['generateKey']>[0]
  ): Promise<string | null> {
    const key = this.generateKey(request);
    const cached = await redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }

  async set(
    request: Parameters<LLMCache['generateKey']>[0],
    response: string
  ): Promise<void> {
    const key = this.generateKey(request);
    await redis.set(key, JSON.stringify(response), 'PX', this.ttlMs);
  }
}

export const llmCache = new LLMCache();

// Usage in generation flow
async function generateWithCache(request: LLMRequest): Promise<LLMResponse> {
  // Check cache first
  const cached = await llmCache.get({
    model: request.model,
    messages: request.messages,
    temperature: request.temperature,
  });

  if (cached) {
    return {
      content: cached,
      model: request.model,
      usage: { promptTokens: 0, completionTokens: 0, totalTokens: 0 },
      latency: 0,
    };
  }

  // Generate fresh response
  const response = await llmClient.generate(request);

  // Cache if it's a cacheable request (no streaming, low temperature)
  if (!request.stream && (request.temperature || 0.7) < 0.5) {
    await llmCache.set(
      {
        model: request.model,
        messages: request.messages,
        temperature: request.temperature,
      },
      response.content
    );
  }

  return response;
}
```

## Document Processing Pipeline

```typescript
// lib/rag/document-processor.ts
// Process documents for RAG: chunk, embed, store

interface Document {
  id: string;
  userId: string;
  title: string;
  content: string;
  metadata?: Record<string, any>;
}

class DocumentProcessor {
  constructor(
    private vectorStore: VectorStore,
    private chunkSize: number = 500,
    private chunkOverlap: number = 50
  ) {}

  async processDocument(document: Document): Promise<void> {
    // 1. Split document into chunks
    const chunks = this.chunkDocument(document.content);

    // 2. Generate embeddings for each chunk
    const embeddings = await generateEmbeddings(chunks.map(c => c.text));

    // 3. Store embeddings in vector database
    for (let i = 0; i < chunks.length; i++) {
      await this.vectorStore.storeEmbedding({
        documentId: document.id,
        content: chunks[i].text,
        embedding: embeddings[i],
        metadata: {
          ...document.metadata,
          chunkIndex: i,
          totalChunks: chunks.length,
          title: document.title,
        },
      });
    }

    // 4. Store document metadata
    await this.storeDocumentMetadata(document, chunks.length);
  }

  private chunkDocument(text: string): Array<{ index: number; text: string }> {
    const chunks: Array<{ index: number; text: string }> = [];
    let start = 0;

    while (start < text.length) {
      let end = start + this.chunkSize;

      // Try to break at a sentence boundary
      if (end < text.length) {
        const searchEnd = Math.min(end + 100, text.length);
        const sentenceEnd = text.lastIndexOf('.', searchEnd);
        if (sentenceEnd > end - 50) {
          end = sentenceEnd + 1;
        }
      }

      chunks.push({
        index: chunks.length,
        text: text.slice(start, end).trim(),
      });

      start = end - this.chunkOverlap;
    }

    return chunks;
  }

  private async storeDocumentMetadata(
    document: Document,
    chunkCount: number
  ) {
    await db.query(
      `INSERT INTO documents (id, user_id, title, content, chunk_count, metadata)
       VALUES ($1, $2, $3, $4, $5, $6)
       ON CONFLICT (id) DO UPDATE SET
         title = $3, content = $4, chunk_count = $5, metadata = $6`,
      [document.id, document.userId, document.title,
       document.content, chunkCount, JSON.stringify(document.metadata || {})]
    );
  }

  async deleteDocument(documentId: string): Promise<void> {
    await this.vectorStore.deleteByDocumentId(documentId);
    await db.query('DELETE FROM documents WHERE id = $1', [documentId]);
  }
}

export const documentProcessor = new DocumentProcessor(vectorStore);
```

## AI SaaS Database Schema

```sql
-- Core tables for AI SaaS

-- Documents (source material for RAG)
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  title VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  content_type VARCHAR(50) DEFAULT 'text',
  chunk_count INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_documents_user ON documents(user_id);

-- LLM Usage Tracking
CREATE TABLE llm_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  request_id UUID NOT NULL,
  provider VARCHAR(50) NOT NULL,
  model VARCHAR(100) NOT NULL,
  prompt_tokens INTEGER NOT NULL,
  completion_tokens INTEGER NOT NULL,
  total_tokens INTEGER NOT NULL,
  cost DECIMAL(10,6) NOT NULL,
  latency_ms INTEGER,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_llm_usage_user ON llm_usage(user_id, timestamp);
CREATE INDEX idx_llm_usage_date ON llm_usage(timestamp);

-- Prompt Versions
CREATE TABLE prompt_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  version INTEGER NOT NULL,
  system_prompt TEXT NOT NULL,
  user_prompt TEXT,
  model VARCHAR(100) NOT NULL,
  temperature DECIMAL(4,2) DEFAULT 0.7,
  max_tokens INTEGER DEFAULT 2048,
  is_active BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(name, version)
);

-- Chat History
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  session_id UUID NOT NULL,
  role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
  content TEXT NOT NULL,
  model VARCHAR(100),
  tokens_used INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chat_session ON chat_messages(session_id, created_at);

-- User AI Settings
CREATE TABLE user_ai_settings (
  user_id UUID PRIMARY KEY REFERENCES users(id),
  default_model VARCHAR(100) DEFAULT 'gpt-4o-mini',
  temperature DECIMAL(4,2) DEFAULT 0.7,
  max_tokens INTEGER DEFAULT 2048,
  system_prompt TEXT,
  daily_usage_limit INTEGER DEFAULT 100,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Cost Optimization Strategies

```markdown
1. Model Tiering
   Use smaller/cheaper models for simple tasks:
   - Summarization: GPT-4o-mini ($0.60/M output tokens)
   - Classification: GPT-4o-mini
   - Complex reasoning: GPT-4o ($15/M output tokens)
   - Embeddings: text-embedding-3-small ($0.02/M tokens)

2. Caching
   - Cache identical requests (same prompt + parameters)
   - Cache embeddings (same text = same embedding)
   - Cache common queries with short TTL
   - Typical savings: 30-50%

3. Prompt Optimization
   - Shorter prompts = fewer tokens = lower cost
   - Use system prompts efficiently
   - Trim conversation history
   - Remove unnecessary context
   - Typical savings: 20-40%

4. Batch Processing
   - Batch embedding requests (100 texts per API call)
   - Batch similar LLM requests
   - Use async processing for non-real-time tasks
   - Typical savings: 30-60%

5. Rate Limiting by Tier
   - Free: 20 requests/hour, GPT-4o-mini only
   - Pro: 500 requests/hour, GPT-4o available
   - Enterprise: 5000 requests/hour, all models
   - Prevents cost explosion from heavy users

6. Prompt Caching (New)
   - OpenAI/Anthropic support prompt caching
   - Cache system prompts and large context
   - 50% discount on cached tokens
   - Enable automatically for repeating prompts
```

## AI SaaS Monitoring

```typescript
// lib/monitoring/ai-monitoring.ts

interface AIMonitoringEvent {
  userId: string;
  model: string;
  promptTokens: number;
  completionTokens: number;
  latency: number;
  success: boolean;
  error?: string;
}

class AIMonitoring {
  async trackLLMCall(event: AIMonitoringEvent) {
    // Send to your monitoring service
    await Promise.all([
      // 1. Track in database for usage analytics
      costTracker.recordUsage({
        userId: event.userId,
        requestId: crypto.randomUUID(),
        provider: event.model.split('-')[0],
        model: event.model,
        promptTokens: event.promptTokens,
        completionTokens: event.completionTokens,
        totalTokens: event.promptTokens + event.completionTokens,
        cost: costTracker.calculateCost(
          event.model,
          event.promptTokens,
          event.completionTokens
        ),
        timestamp: new Date(),
      }),

      // 2. Track in monitoring (Datadog, Grafana, etc.)
      // await metrics.increment('llm.requests.total');
      // await metrics.histogram('llm.latency', event.latency);
      // await metrics.histogram('llm.tokens', event.promptTokens + event.completionTokens);

      // 3. Log for debugging
      console.log('LLM Call:', {
        model: event.model,
        tokens: event.promptTokens + event.completionTokens,
        latency: `${event.latency}ms`,
        success: event.success,
      }),
    ]);
  }

  async getLLMAlerts(): Promise<Array<{
    type: string;
    severity: 'low' | 'medium' | 'high';
    message: string;
  }>> {
    const alerts = [];

    // Check for cost anomalies
    const todayCost = await db.query(
      `SELECT COALESCE(SUM(cost), 0) as total_cost
       FROM llm_usage WHERE timestamp > NOW() - INTERVAL '1 day'`
    );

    if (parseFloat(todayCost.rows[0].total_cost) > 50) {
      alerts.push({
        type: 'cost_anomaly',
        severity: 'high',
        message: `Daily LLM cost exceeded $50: $${todayCost.rows[0].total_cost}`,
      });
    }

    // Check for high error rates
    const errorRate = await db.query(
      `SELECT
         COUNT(*) FILTER (WHERE success = false) * 100.0 / COUNT(*) as error_rate
       FROM llm_usage
       WHERE timestamp > NOW() - INTERVAL '1 hour'`
    );

    if (parseFloat(errorRate.rows[0].error_rate) > 10) {
      alerts.push({
        type: 'high_error_rate',
        severity: 'high',
        message: `LLM error rate: ${errorRate.rows[0].error_rate}%`,
      });
    }

    return alerts;
  }
}

export const aiMonitoring = new AIMonitoring();
```

## Building AI Features: Common Patterns

### Pattern 1: AI-Powered Search

```typescript
// lib/ai/ai-search.ts
// Combine traditional search with semantic search

async function hybridSearch(query: string, userId: string) {
  const [vectorResults, textResults] = await Promise.all([
    // Semantic search (vector)
    vectorStore.searchSimilar({
      embedding: await generateEmbedding(query),
      limit: 10,
    }),
    // Text search (PostgreSQL full-text)
    db.query(
      `SELECT id, title, content,
        ts_rank(to_tsvector('english', title || ' ' || content),
                plainto_tsquery('english', $1)) as rank
       FROM documents
       WHERE user_id = $2
         AND to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', $1)
       ORDER BY rank DESC
       LIMIT 10`,
      [query, userId]
    ),
  ]);

  // Merge results with reciprocal rank fusion (RRF)
  const merged = mergeResults(vectorResults, textResults.rows);
  return merged;
}
```

### Pattern 2: AI Content Generation

```typescript
// lib/ai/content-generator.ts
class ContentGenerator {
  async generate(params: {
    contentType: 'blog' | 'social' | 'email' | 'code';
    topic: string;
    tone: string;
    length: 'short' | 'medium' | 'long';
  }): Promise<{ content: string; usage: UsageInfo }> {
    const templates: Record<string, { system: string; length: number }> = {
      blog: {
        system: 'You are a professional blog writer.',
        length: 1000,
      },
      social: {
        system: 'You are a social media content creator.',
        length: 200,
      },
    };

    const tmpl = templates[params.contentType];
    const response = await llmClient.generate({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: tmpl.system },
        { role: 'user', content: `Write a ${params.length} ${params.contentType}
          about ${params.topic} in a ${params.tone} tone.` },
      ],
      maxTokens: tmpl.length,
    });

    return { content: response.content, usage: response.usage };
  }
}
```

### Pattern 3: AI Classification

```typescript
// lib/ai/classifier.ts
class AIClassifier {
  async classify(params: {
    text: string;
    categories: string[];
  }): Promise<{ category: string; confidence: number }> {
    const response = await llmClient.generate({
      model: 'gpt-4o-mini', // Cheap model for simple tasks
      messages: [
        {
          role: 'system',
          content: `Classify the following text into exactly one of these categories:
            ${params.categories.join(', ')}.
            Respond with ONLY the category name and confidence score as JSON:
            {"category": "...", "confidence": 0.0-1.0}`,
        },
        { role: 'user', content: params.text },
      ],
      temperature: 0.1, // Low temperature for deterministic output
    });

    return JSON.parse(response.content);
  }
}
```

## AI SaaS Security Considerations

```markdown
1. Prompt Injection Protection
   - Validate user input for prompt injection attempts
   - Use delimiter-based separation of user content
   - Implement input/output guardrails
   - Rate limit per user to prevent abuse
   - Consider using OpenAI's moderation endpoint

2. Data Privacy
   - Ensure no customer data leaks in prompts to other customers
   - Strip PII from prompts before sending to LLM providers
   - Consider using Azure/AWS providers for data residency
   - Implement data retention policies for stored prompts
   - Encrypt stored embeddings and documents

3. Cost Abuse Prevention
   - Hard rate limits per user/API key
   - Usage alerts when approaching thresholds
   - Automatic suspension for anomalous usage
   - Per-request cost tracking
   - Monthly budget caps per customer

4. Model Hallucination Mitigation
   - Always provide context for RAG
   - Include confidence scores where possible
   - Allow users to flag incorrect responses
   - Consider using smaller models with prompt engineering
   - Implement citation verification
```

## Recommended AI SaaS Starter Stack

```markdown
Frontend:
  Next.js 14+ (React, TypeScript, Server Components)
  Tailwind CSS + shadcn/ui (rapid UI development)
  Vercel AI SDK (streaming, useChat, useCompletion)

Backend:
  Next.js API routes (can also use Python FastAPI for heavy AI work)
  Prisma or Drizzle ORM (type-safe database access)
  Supabase or Neon for PostgreSQL

AI Services:
  OpenAI API (GPT-4o-mini for cost, GPT-4o for quality)
  Anthropic API (Claude 3.5 Sonnet as fallback)
  text-embedding-3-small for embeddings

Vector Storage:
  pgvector (on existing PostgreSQL — simplest setup)
  Pinecone (when you need scale beyond PostgreSQL)

Caching:
  Upstash Redis (serverless, $0.45/GB month)
  Or in-memory cache for MVP

Monitoring:
  Helicone (LLM observability, free tier available)
  Langfuse (open source LLM tracing)
  Sentry (error tracking)

Payment:
  Stripe (usage-based billing for API tokens)
  Lemon Squeezy (simpler, handles VAT)

Auth:
  Clerk or Supabase Auth
```

## Summary

Building an AI SaaS requires careful consideration of the LLM stack, cost management, and prompt engineering. The key decisions are:

1. **LLM Provider**: Start with OpenAI, add Anthropic as fallback
2. **Vector Store**: Use pgvector on your existing PostgreSQL
3. **Prompt Management**: Version and track prompts from day one
4. **Cost Tracking**: Track every token and set rate limits
5. **Caching**: Cache identical requests to save 30-50%
6. **Streaming**: Stream responses for better UX
7. **Security**: Prevent prompt injection and abuse
8. **Monitoring**: Track usage, cost, and errors from day one

The biggest difference from traditional SaaS is cost management — LLM APIs are expensive and costs can spiral. Monitor aggressively, cache aggressively, and always set limits.
