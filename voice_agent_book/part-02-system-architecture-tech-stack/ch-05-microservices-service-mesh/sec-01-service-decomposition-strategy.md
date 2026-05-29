# Section 01: Service Decomposition Strategy

## Domain-Driven Service Boundaries

The platform follows **Domain-Driven Design (DDD)** principles to decompose functionality into independently deployable microservices. Each service owns its domain logic and data store, communicates via well-defined APIs, and can be scaled independently.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MICROSERVICES DECOMPOSITION MAP                     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     CORE DOMAIN SERVICES                        │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │  Agent   │  │  Call    │  │  Voice   │  │   AI     │        │    │
│  │  │  Service │  │  Service │  │  Service │  │  Service │        │    │
│  │  │          │  │          │  │          │  │          │        │    │
│  │  │ • Agents │  │ • Calls  │  │ • STT    │  │ • LLM    │        │    │
│  │  │ • Config │  │ • State  │  │ • TTS    │  │ • RAG    │        │    │
│  │  │ • Vers.  │  │ • Events │  │ • VAD    │  │ • Memory │        │    │
│  │  │ • Prompts│  │ • Rec.   │  │ • Audio  │  │ • Tools  │        │    │
│  │  │ • Voices │  │          │  │          │  │          │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  │                                                                  │    │
│  │  PostgreSQL    │  PostgreSQL   │  Ephemeral    │  PostgreSQL    │    │
│  │  (primary)     │  (primary)    │  + GPU        │  + pgvector    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    SUPPORTING SERVICES                          │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ Campaign │  │  Billing │  │   Auth   │  │Notificat.│        │    │
│  │  │ Service  │  │  Service │  │  Service │  │ Service  │        │    │
│  │  │          │  │          │  │          │  │          │        │    │
│  │  │ • Campgns│  │ • Subsc. │  │ • Users  │  • Emails   │        │    │
│  │  │ • Contac │  │ • Usage  │  │ • Roles  │  • Webhooks │        │    │
│  │  │ • DNC    │  │ • Inv.   │  │ • OAuth  │  • SMS     │        │    │
│  │  │ • Dialer │  │ • Paymnts│  │ • MFA    │  • Push    │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    INFRASTRUCTURE SERVICES                      │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │  Media   │  │ WebSocket│  │  API     │  │  File    │        │    │
│  │  │  Server  │  │  Server  │  │  Gateway │  │  Service │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Service Definitions

### Core Domain Services

```typescript
// Agent Service — manages AI agent configuration
interface AgentService {
  // Domain: Agent lifecycle
  createAgent(config: CreateAgentInput): Promise<Agent>
  updateAgent(id: string, config: UpdateAgentInput): Promise<Agent>
  deleteAgent(id: string): Promise<void>
  deployAgent(id: string): Promise<AgentVersion>
  getAgent(id: string): Promise<Agent>
  listAgents(filter: AgentFilter): Promise<PaginatedResult<Agent>>
  
  // Domain: Agent configuration
  getAgentConfig(id: string): Promise<AgentConfig>
  updateAgentConfig(id: string, config: AgentConfig): Promise<void>
  
  // Domain: Prompt management
  createPrompt(prompt: CreatePromptInput): Promise<Prompt>
  updatePrompt(id: string, prompt: Prompt): Promise<Prompt>
  
  // Domain: Voice management
  listVoices(filter: VoiceFilter): Promise<Voice[]>
  createVoice(voice: CreateVoiceInput): Promise<Voice>
  
  // Events emitted
  events: {
    'agent.created': AgentCreatedEvent
    'agent.updated': AgentUpdatedEvent
    'agent.deployed': AgentDeployedEvent
    'agent.deleted': AgentDeletedEvent
  }
  
  // Data store: PostgreSQL (agents, agent_versions, prompts, voices)
  // Cache: Redis (active agent configs)
}

// Call Service — manages call lifecycle
interface CallService {
  // Domain: Call lifecycle
  initiateCall(input: InitiateCallInput): Promise<Call>
  answerCall(callId: string): Promise<Call>
  endCall(callId: string): Promise<Call>
  transferCall(callId: string, target: TransferTarget): Promise<Call>
  
  // Domain: Call state
  getCall(callId: string): Promise<Call>
  getCallState(callId: string): Promise<CallState>
  updateCallState(callId: string, state: Partial<CallState>): Promise<void>
  
  // Domain: Call events
  getCallEvents(callId: string): Promise<CallEvent[]>
  addCallEvent(callId: string, event: CallEvent): Promise<void>
  
  // Domain: Recording
  startRecording(callId: string): Promise<void>
  stopRecording(callId: string): Promise<RecordingMetadata>
  
  // Events emitted
  events: {
    'call.initiated': CallInitiatedEvent
    'call.answered': CallAnsweredEvent
    'call.ended': CallEndedEvent
    'call.transferred': CallTransferredEvent
    'call.recording.started': RecordingStartedEvent
    'call.recording.completed': RecordingCompletedEvent
  }
  
  // Data store: PostgreSQL (calls, call_events, recordings)
  // Partitioned: calls by month, call_events by month
}

// Voice Service — handles audio processing
interface VoiceService {
  // Domain: Speech-to-text
  transcribeAudio(audio: AudioChunk, options: STTOptions): Promise<STTResult>
  startStreamingSTT(sessionId: string): Promise<STTStream>
  stopStreamingSTT(sessionId: string): Promise<void>
  
  // Domain: Text-to-speech
  synthesizeSpeech(text: string, voice: VoiceConfig): Promise<AudioBuffer>
  startStreamingTTS(sessionId: string): Promise<TTSStream>
  
  // Domain: Voice activity detection
  detectVoiceActivity(audio: AudioChunk): Promise<VADResult>
  
  // Domain: Audio processing
  mixAudio(streams: AudioStream[], options: MixOptions): Promise<AudioBuffer>
  transcodeAudio(audio: AudioBuffer, targetCodec: string): Promise<AudioBuffer>
  
  // Data store: Ephemeral (in-memory streams)
  // GPU: NVIDIA T4/A10G for STT/TTS inference
}

// AI Service — LLM orchestration
interface AIService {
  // Domain: Conversation
  processTurn(input: ConversationInput): Promise<ConversationOutput>
  generateResponse(context: ConversationContext): Promise<AIResponse>
  
  // Domain: RAG
  searchKnowledgeBase(query: string, kbId: string): Promise<KnowledgeResult[]>
  addToKnowledgeBase(documents: Document[]): Promise<void>
  
  // Domain: Memory
  getConversationMemory(conversationId: string): Promise<Memory>
  updateConversationMemory(conversationId: string, memory: Partial<Memory>): Promise<void>
  
  // Domain: Tools
  executeTool(name: string, params: Record<string, unknown>): Promise<ToolResult>
  
  // Data store: PostgreSQL + pgvector (embeddings, memory)
  // Model: OpenAI/Anthropic/Local via model router
}
```

### Supporting Services

```typescript
// Campaign Service — outbound dialing campaigns
interface CampaignService {
  createCampaign(input: CreateCampaignInput): Promise<Campaign>
  startCampaign(id: string): Promise<void>
  pauseCampaign(id: string): Promise<void>
  completeCampaign(id: string): Promise<void>
  getCampaignMetrics(id: string): Promise<CampaignMetrics>
  
  // Contact management
  importContacts(campaignId: string, contacts: Contact[]): Promise<ImportResult>
  getNextContact(campaignId: string): Promise<Contact | null>
  recordAttempt(attempt: CallAttempt): Promise<void>
  
  // DNC management
  checkDNC(phone: string): Promise<DNCStatus>
  addToDNC(phone: string, reason: string): Promise<void>
  
  // Data store: PostgreSQL (campaigns, contacts, call_attempts, dnc_numbers)
}

// Billing Service — subscription and usage
interface BillingService {
  // Subscriptions
  getSubscription(tenantId: string): Promise<Subscription>
  changePlan(tenantId: string, planId: string): Promise<Subscription>
  cancelSubscription(tenantId: string): Promise<void>
  
  // Usage metering
  recordUsage(tenantId: string, metric: string, amount: number): Promise<void>
  getCurrentUsage(tenantId: string, metric?: string): Promise<UsageBreakdown>
  checkUsageLimit(tenantId: string, metric: string): Promise<LimitCheck>
  
  // Invoicing
  generateInvoice(tenantId: string, period: DateRange): Promise<Invoice>
  getInvoice(invoiceId: string): Promise<Invoice>
  
  // Data store: PostgreSQL + Redis (rate limit counters)
}

// Auth Service — authentication and authorization
interface AuthService {
  // Authentication
  authenticate(credentials: Credentials): Promise<AuthResult>
  validateSession(token: string): Promise<Session>
  refreshSession(token: string): Promise<AuthResult>
  invalidateSession(token: string): Promise<void>
  
  // OAuth
  initiateOAuth(provider: string): Promise<OAuthURL>
  handleOAuthCallback(provider: string, code: string): Promise<AuthResult>
  
  // MFA
  setupMFA(userId: string): Promise<MFASetup>
  verifyMFA(userId: string, code: string): Promise<boolean>
  
  // API Keys
  createApiKey(tenantId: string, name: string): Promise<ApiKey>
  validateApiKey(key: string): Promise<ApiKeyValidation>
  revokeApiKey(id: string): Promise<void>
  
  // Data store: PostgreSQL (users, sessions, api_keys)
}

// Notification Service — alerts and messages
interface NotificationService {
  // Email
  sendEmail(to: string, template: string, data: Record<string, unknown>): Promise<void>
  
  // Webhook
  sendWebhook(endpointId: string, event: string, payload: unknown): Promise<void>
  retryWebhook(deliveryId: string): Promise<void>
  
  // SMS
  sendSMS(to: string, message: string): Promise<void>
  
  // In-app notification
  sendInApp(userId: string, notification: Notification): Promise<void>
  
  // Data store: PostgreSQL (webhook_endpoints, delivery_logs)
  // Queue: Redis/BullMQ (webhook delivery, email sending)
}
```

## Service Dependency Graph

```
                    ┌──────────┐
                    │  Auth    │
                    │  Service │
                    └────┬─────┘
                         │
  ┌──────────────────────┼──────────────────────┐
  │                      │                      │
  ▼                      ▼                      ▼
┌──────────┐      ┌──────────┐      ┌──────────────┐
│  Agent   │      │  Call    │      │  Campaign    │
│  Service │◄─────│  Service │◄─────│  Service     │
└────┬─────┘      └────┬─────┘      └──────────────┘
     │                  │
     ▼                  ▼
┌──────────┐      ┌──────────┐
│   AI     │      │  Voice   │
│  Service │◄─────│  Service │
└──────────┘      └──────────┘
     │
     ▼
┌──────────┐
│  Billing │
│  Service │
└──────────┘
     │
     ▼
┌──────────────┐
│ Notification │
│  Service     │
└──────────────┘
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Service Count | 7 core + 3 infra | Manageable team ownership; each service owned by 2-3 devs |
| Data Ownership | Database-per-service | Clear ownership, independent schema evolution |
| Communication | Async (Kafka) > Sync (gRPC/REST) | Loose coupling, resilience, audit trail |
| Service Size | Bounded context (DDD) | Each service has focused, non-overlapping responsibility |
| Deployment | Independent per service | Can deploy without coordinating other services |

## Integration Points

- **Part 05 (Microservices)** — This is the foundation chapter for microservices
- **Part 03 (Database)** — Each service owns its database schema
- **Part 23 (DevOps)** — Independent deployment per service
- **Part 24 (Scaling)** — Each service scales independently based on load

## Production Considerations

- **Service Ownership**: Each service has a named owner and on-call rotation
- **SLAs by Service**: Core services (Call, Voice) have 99.99% SLA; supporting (Notifications) 99.9%
- **Circuit Breakers**: Each service has circuit breakers for downstream dependencies
- **Bulkheads**: Services run in separate Kubernetes deployments with resource limits
- **Versioning**: Services maintain backward-compatible APIs for at least 2 major versions
- **Monitoring**: Service-level dashboards for latency, error rate, throughput, saturation
