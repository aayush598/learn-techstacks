# Section 04: Call & Conversation Schema

## Call Lifecycle Data Model

The call and conversation tables capture every detail of a voice interaction — from the initial connection through each turn of dialogue to the final outcome. This data powers analytics, compliance, quality assurance, and the event-sourced call state machine.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CALL & CONVERSATION SCHEMA                          │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                            CALL                                  │    │
│  │                                                                  │    │
│  │  ┌─────────────────────┐  ┌─────────────────────┐              │    │
│  │  │  Connection Phase   │  │  Conversation Phase  │              │    │
│  │  │                     │  │                      │              │    │
│  │  │  • caller_number    │  │  • duration          │              │    │
│  │  │  • called_number    │  │  • status            │              │    │
│  │  │  • direction        │  │  • sentiment_score   │              │    │
│  │  │  • started_at       │  │  • cost_micro_us     │              │    │
│  │  │  • answered_at      │  │  • turn_count        │              │    │
│  │  │  • ended_at         │  │  • word_count        │              │    │
│  │  └─────────────────────┘  └─────────────────────┘              │    │
│  │                                                                  │    │
│  │  ┌─────────────────────┐  ┌─────────────────────┐              │    │
│  │  │  Performance        │  │  References          │              │    │
│  │  │                     │  │                      │              │    │
│  │  │  • stt_latency_ms   │  │  • agent_id          │              │    │
│  │  │  • ai_latency_ms    │  │  • campaign_id       │              │    │
│  │  │  • tts_latency_ms   │  │  • recording_url     │              │    │
│  │  │  • avg_jitter_ms    │  │  • transcript_url    │              │    │
│  │  │  • packet_loss_pct  │  │  • tenant_id         │              │    │
│  │  └─────────────────────┘  └─────────────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        CONVERSATION EVENTS                      │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Type:        │  │  Type:        │  │  Type:        │          │    │
│  │  │  "utterance"  │  │  "sentiment"  │  │  "system"    │          │    │
│  │  │              │  │              │  │              │          │    │
│  │  │  • speaker    │  │  • score     │  │  • event     │          │    │
│  │  │  • text       │  │  • label     │  │  • metadata  │          │    │
│  │  │  • start_time │  │  • timestamp │  │  • timestamp │          │    │
│  │  │  • end_time   │  │              │  │              │          │    │
│  │  |  • confidence  |  |              |  |              |          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │                                                                  │    │
│  │  Timeline: ──── U1 ──── U2 ── S1 ──── U3 ── U4 ── S2 ── T1 ──► │    │
│  │             (User  ) (Agent) (Sent) (User) (Agent)(Sent) (Transfer) │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      TRANSCRIPT CHUNKS                          │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Chunk 1     │  │  Chunk 2     │  │  Chunk 3     │          │    │
│  │  │  "Hello, I   │  │  "I need help│  │  "My order   │          │    │
│  │  │  need help"  │  │  with..."    │  │  number is"  │          │    │
│  │  │              │  │              │  │              │          │    │
│  │  │  offset: 0   │  │  offset: 512 │  │  offset: 1024│          │    │
│  │  │  conf: 0.95  │  │  conf: 0.88  │  │  conf: 0.91  │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prisma Schema

```prisma
// Call record — core transactional entity
model Call {
  id             String       @id @default(uuid()) @db.Uuid
  tenantId       String       @map("tenant_id") @db.Uuid
  agentId        String       @map("agent_id") @db.Uuid
  campaignId     String?      @map("campaign_id") @db.Uuid
  callerNumber   String       @map("caller_number") @db.VarChar(20)
  calledNumber   String       @map("called_number") @db.VarChar(20)
  direction      CallDirection
  status         CallStatus
  duration       Int          @default(0)      // seconds
  costMicroUs    BigInt       @default(0) @map("cost_micro_us")
  sttLatencyMs   Int?         @map("stt_latency_ms")
  aiLatencyMs    Int?         @map("ai_latency_ms")
  ttsLatencyMs   Int?         @map("tts_latency_ms")
  sentimentScore Float?       @map("sentiment_score")
  turnCount      Int          @default(0) @map("turn_count")
  wordCount      Int          @default(0) @map("word_count")
  recordingUrl   String?      @map("recording_url") @db.VarChar(1000)
  transcriptUrl  String?      @map("transcript_url") @db.VarChar(1000)
  errorCode      String?      @map("error_code") @db.VarChar(50)
  errorMessage   String?      @map("error_message") @db.Text
  startedAt      DateTime?    @map("started_at")
  answeredAt     DateTime?    @map("answered_at")
  endedAt        DateTime?    @map("ended_at")
  createdAt      DateTime     @default(now()) @map("created_at")
  updatedAt      DateTime     @updatedAt @map("updated_at")

  tenant       Tenant            @relation(fields: [tenantId], references: [id])
  agent        Agent             @relation(fields: [agentId], references: [id])
  campaign     Campaign?         @relation(fields: [campaignId], references: [id])
  events       ConversationEvent[]
  transcriptChunks TranscriptChunk[]
  recording    CallRecording?
  escalation   CallEscalation?

  @@index([tenantId, status, createdAt])
  @@index([tenantId, agentId, createdAt])
  @@index([tenantId, callerNumber])
  @@index([tenantId, createdAt])
  @@index([campaignId])
  @@map("calls")
}

enum CallDirection {
  inbound
  outbound
}

enum CallStatus {
  queued
  ringing
  connecting
  in_progress
  paused
  transferring
  transferring_media
  completed
  failed
  no_answer
  busy
  voicemail
  canceled
  error
}

// Conversation events — append-only log of everything that happened
model ConversationEvent {
  id        String              @id @default(uuid()) @db.Uuid
  callId    String              @map("call_id") @db.Uuid
  type      ConversationEventType
  speaker   String?             @db.VarChar(10)   // "user" | "agent" | "system"
  text      String?             @db.Text
  payload   Json                @default("{}")
  startTime Int?                @map("start_time")  // ms from call start
  endTime   Int?                @map("end_time")
  confidence Float?             // 0.0 - 1.0
  timestamp DateTime            @default(now())
  createdAt DateTime            @default(now()) @map("created_at")

  call Call @relation(fields: [callId], references: [id])

  @@index([callId, timestamp])
  @@index([callId, type])
  @@map("conversation_events")
}

enum ConversationEventType {
  utterance           // User or agent speech
  sentiment_snapshot  // Periodic sentiment score
  system_event        // State transitions, errors
  tool_call           // AI tool execution
  tool_result         // Tool execution result
  escalation          // Human hand-off
  transfer            // Call transfer
  dtmf               // DTMF digit received
  silence             // Silence detected
  barge_in           // Caller interrupted
}

// Transcript chunks — incremental STT output
model TranscriptChunk {
  id          String   @id @default(uuid()) @db.Uuid
  callId      String   @map("call_id") @db.Uuid
  text        String   @db.Text
  offset      Int                  // Character offset in full transcript
  confidence  Float
  isFinal     Boolean  @default(false) @map("is_final")
  createdAt   DateTime @default(now()) @map("created_at")

  call Call @relation(fields: [callId], references: [id])

  @@index([callId, offset])
  @@map("transcript_chunks")
}

// Call recording metadata
model CallRecording {
  id             String           @id @default(uuid()) @db.Uuid
  callId         String           @unique @map("call_id") @db.Uuid
  format         String           @default("wav")  // wav, mp3, ogg, opus
  sampleRate     Int              @default(16000) @map("sample_rate")
  duration       Int              // seconds
  fileSize       BigInt           @map("file_size")  // bytes
  storagePath    String           @map("storage_path") @db.VarChar(1000)
  storageBucket  String           @map("storage_bucket") @db.VarChar(100)
  hasMonoAgent   Boolean          @default(false) @map("has_mono_agent")
  hasMonoCaller  Boolean          @default(false) @map("has_mono_caller")
  stereoUrl      String?          @map("stereo_url") @db.VarChar(1000)
  agentUrl       String?          @map("agent_url") @db.VarChar(1000)
  callerUrl      String?          @map("caller_url") @db.VarChar(1000)
  createdAt      DateTime         @default(now()) @map("created_at")

  call Call @relation(fields: [callId], references: [id], onDelete: Cascade)

  @@map("call_recordings")
}

// Escalation records
model CallEscalation {
  id          String     @id @default(uuid()) @db.Uuid
  callId      String     @unique @map("call_id") @db.Uuid
  reason      EscalationReason
  triggeredBy EscalationTrigger
  summary     String?    @db.Text
  agentNote   String?    @map("agent_note") @db.Text
  assignedTo  String?    @map("assigned_to") @db.VarChar(255)
  status      EscalationStatus @default(pending)
  resolvedAt  DateTime?  @map("resolved_at")
  createdAt   DateTime   @default(now()) @map("created_at")
  updatedAt   DateTime   @updatedAt @map("updated_at")

  call Call @relation(fields: [callId], references: [id], onDelete: Cascade)

  @@map("call_escalations")
}

enum EscalationReason {
  agent_requested
  sentiment_too_low
  multiple_failures
  complex_query
  compliance_required
  user_requested
  payment_processing
  legal_concern
}

enum EscalationTrigger {
  ai_detected
  user_requested
  rule_based
  manual
}

enum EscalationStatus {
  pending
  accepted
  in_progress
  resolved
  closed
}
```

## Key Query Patterns

```typescript
// Call queries — heavily indexed, optimized for common access patterns

// Recent calls for a tenant (dashboard)
const recentCalls = await prisma.call.findMany({
  where: {
    tenantId: session.tenantId,
    createdAt: { gte: subDays(new Date(), 7) }
  },
  orderBy: { createdAt: 'desc' },
  take: 50,
  include: {
    agent: { select: { name: true } },
    recording: { select: { duration: true } }
  }
})

// Active calls (real-time monitoring)
const activeCalls = await prisma.call.findMany({
  where: {
    tenantId: session.tenantId,
    status: { in: ['in_progress', 'ringing', 'connecting', 'paused'] }
  },
  include: {
    agent: { select: { name: true, voice: { select: { name: true } } } },
    events: {
      where: { type: 'sentiment_snapshot' },
      orderBy: { timestamp: 'desc' },
      take: 1
    }
  }
})

// Call detail with full conversation
const callDetail = await prisma.call.findUnique({
  where: { id: callId },
  include: {
    agent: true,
    events: { orderBy: { timestamp: 'asc' } },
    recording: true,
    escalation: true
  }
})

// Call performance analytics (aggregate)
const performance = await prisma.call.aggregate({
  where: {
    tenantId: session.tenantId,
    createdAt: { gte: startDate, lte: endDate }
  },
  _avg: {
    sttLatencyMs: true,
    aiLatencyMs: true,
    ttsLatencyMs: true,
    duration: true
  },
  _count: true
})
```

## Partitioning Strategy

```sql
-- Calls table partitioned by month for performance
CREATE TABLE calls (
  id UUID DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL,
  -- ... other columns
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE calls_2025_01 PARTITION OF calls
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE calls_2025_02 PARTITION OF calls
  FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
-- ... auto-created by pg_partman

-- Conversation events — even higher volume, partitioned by month too
CREATE TABLE conversation_events (
  -- ...
  created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY RANGE (created_at);
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event Storage | Separate table (not JSON array) | Queryable, indexable, scalable |
| Transcript Storage | Chunks + full URL | Searchable chunks + downloadable full transcript |
| Cost Storage | Micro-cents (BigInt) | Avoid floating point precision issues |
| Timestamps | Milliseconds from call start | Precise alignment for audio playback |
| Partitioning | Monthly by created_at | Manageable partition size, easy archival |

## Integration Points

- **Part 04 (Core Voice)** — Call records created during voice pipeline execution
- **Part 11 (Analytics)** — Aggregations on call data for reporting
- **Part 12 (Recording)** — Recording metadata linked to call
- **Part 08 (Human Handoff)** — Escalation records linked to call

## Production Considerations

- **Data Volume**: ~1KB per call record, ~100MB per 100K calls; partition monthly
- **Archival**: Calls older than 90 days moved to warm storage (ClickHouse), only metadata retained in PostgreSQL
- **Cleanup**: Conversation events older than 30 days archived to MinIO as JSON
- **Monitoring**: Track call volume, average duration, error rate by agent
- **Compliance**: Call recordings retained per regulatory requirements (typically 12-84 months)
- **PII Handling**: Caller number stored with deterministic encryption; access controlled by RLS
