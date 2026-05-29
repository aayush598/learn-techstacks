# Section 03: Agent Configuration Schema

## Agent Data Model

AI Agents are the core configurable entity in the platform. Each agent has a voice, prompt, version history, and configuration that determines how it interacts with callers.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       AGENT CONFIGURATION SCHEMA                       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                          AGENT                                   │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  id: uuid    │  │  name:       │  │  description │          │    │
│  │  │  tenant_id   │  │  "Sales Rep" │  │  "Handles... │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  language:   │  │  status:     │  │  config:     │          │    │
│  │  │  "en-US"     │  │  "active"    │  │  {temperature│          │    │
│  │  └──────────────┘  └──────────────┘  │   : 0.7,    │          │    │
│  │                                      │   bargeIn:   │          │    │
│  │                                      │   true,...}  │          │    │
│  │                                      └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌──────────────────────┬──────────────────────┬──────────────────────┐ │
│  │          ▼           │          ▼           │          ▼           │ │
│  │  ┌──────────────┐    │  ┌──────────────┐    │  ┌──────────────┐    │ │
│  │  │    Voice     │    │  │   Prompt     │    │  │  Knowledge   │    │ │
│  │  │              │    │  │              │    │  │  Base        │    │ │
│  │  │  • provider  │    │  │  • content   │    │  │              │    │ │
│  │  │  • voice_id  │    │  │  • variables │    │  │  • documents │    │ │
│  │  │  • gender    │    │  │  • version   │    │  │  • chunks    │    │ │
│  │  │  • language  │    │  └──────────────┘    │  │  • embeddings│    │ │
│  │  └──────────────┘    │                       │  └──────────────┘    │ │
│  │                      └──────────────────────┘                      │ │
│  │                                                                     │ │
│  │  ┌────────────────────────────────────────────────────────────┐    │ │
│  │  │                    Agent Versions                          │    │ │
│  │  │  ┌───────┬───────┬───────┬───────┬───────┬──────────┐     │    │ │
│  │  │  │ v1    │ v2    │ v3    │ v4    │ v5    │ (active) │     │    │ │
│  │  │  │ (draft)│(draft)│(deploy)│(draft)│       │  v3      │     │    │ │
│  │  │  └───────┴───────┴───────┴───────┴───────┴──────────┘     │    │ │
│  │  └────────────────────────────────────────────────────────────┘    │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prisma Schema

```prisma
// Agent model
model Agent {
  id          String       @id @default(uuid()) @db.Uuid
  tenantId    String       @map("tenant_id") @db.Uuid
  name        String       @db.VarChar(255)
  description String?      @db.Text
  voiceId     String       @map("voice_id") @db.Uuid
  promptId    String       @map("prompt_id") @db.Uuid
  language    String       @default("en-US") @db.VarChar(10)
  status      AgentStatus  @default(draft)
  config      Json         @default("{}")
  createdBy   String       @map("created_by") @db.Uuid
  deployedAt  DateTime?    @map("deployed_at")
  createdAt   DateTime     @default(now()) @map("created_at")
  updatedAt   DateTime     @updatedAt @map("updated_at")

  tenant        Tenant        @relation(fields: [tenantId], references: [id])
  voice         Voice         @relation(fields: [voiceId], references: [id])
  prompt        Prompt        @relation(fields: [promptId], references: [id])
  createdByUser User          @relation("AgentCreator", fields: [createdBy], references: [id])
  versions      AgentVersion[]
  calls         Call[]
  campaigns     Campaign[]
  knowledgeBases KnowledgeBase[]

  @@index([tenantId, status])
  @@index([tenantId, createdAt])
  @@map("agents")
}

enum AgentStatus {
  draft
  testing
  active
  paused
  archived
  deleted
}

// Agent configuration type
// {
//   "temperature": 0.7,           // LLM creativity (0-2)
//   "maxTokens": 1024,            // Max response tokens
//   "bargeIn": true,              // Allow caller to interrupt
//   "endCallAfterSilence": 10,   // Seconds of silence before ending
//   "endCallMaxDuration": 1800,  // Max call duration in seconds
//   "sttLanguage": "en-US",      // Speech-to-text language
//   "sttModel": "whisper-large-v3",
//   "ttsSpeed": 1.0,             // Speech speed (0.5-2.0)
//   "ttsPitch": 0,               // Pitch adjustment
//   "noInputTimeout": 5,         // Seconds before "no input" prompt
//   "fallbackMessage": "I didn't understand. Could you repeat that?",
//   "maxRetriesOnError": 2,
//   "endBehavior": {
//     "type": "hangup",           // hangup | transfer | callback
//     "target": null,
//     "message": "Goodbye!"
//   },
//   "transferRules": [
//     {
//       "condition": "intent == 'escalate' || sentiment < 0.3",
//       "target": "support-team",
//       "message": "Let me transfer you to a specialist."
//     }
//   ]
// }

// Agent version history
model AgentVersion {
  id          String   @id @default(uuid()) @db.Uuid
  agentId     String   @map("agent_id") @db.Uuid
  version     Int
  config      Json     @default("{}")
  voiceId     String?  @map("voice_id") @db.Uuid
  promptId    String?  @map("prompt_id") @db.Uuid
  publishNote String?  @map("publish_note") @db.Text
  createdBy   String   @map("created_by") @db.Uuid
  createdAt   DateTime @default(now()) @map("created_at")
  isActive    Boolean  @default(false) @map("is_active")

  agent   Agent  @relation(fields: [agentId], references: [id])
  voice   Voice? @relation("VersionVoice", fields: [voiceId], references: [id])
  prompt  Prompt? @relation("VersionPrompt", fields: [promptId], references: [id])

  @@unique([agentId, version])
  @@index([agentId, isActive])
  @@map("agent_versions")
}

// Voice configuration
model Voice {
  id         String   @id @default(uuid()) @db.Uuid
  tenantId   String   @map("tenant_id") @db.Uuid
  name       String   @db.VarChar(255)
  provider   VoiceProvider
  voiceId    String   @map("voice_id") @db.VarChar(100)
  language   String   @default("en-US") @db.VarChar(10)
  gender     VoiceGender @default(neutral)
  previewUrl String?  @map("preview_url") @db.VarChar(500)
  isDefault  Boolean  @default(false) @map("is_default")
  config     Json     @default("{}")
  createdAt  DateTime @default(now()) @map("created_at")
  updatedAt  DateTime @updatedAt @map("updated_at")

  tenant         Tenant         @relation(fields: [tenantId], references: [id])
  agents         Agent[]
  agentVersions  AgentVersion[] @relation("VersionVoice")

  @@unique([tenantId, name])
  @@index([tenantId, provider])
  @@map("voices")
}

enum VoiceProvider {
  coqui_tts
  elevenlabs
  azure
  google
  amazon_polly
  custom
}

enum VoiceGender {
  male
  female
  neutral
}

// Voice config example
// {
//   "coqui_tts": {
//     "model": "tts_models/en/ljspeech/tacotron2-DDC",
//     "speaker_id": null
//   },
//   "elevenlabs": {
//     "model": "eleven_multilingual_v2",
//     "stability": 0.5,
//     "similarity_boost": 0.75,
//     "style": 0.0,
//     "use_speaker_boost": true
//   }
// }

// Prompt configuration
model Prompt {
  id        String   @id @default(uuid()) @db.Uuid
  tenantId  String   @map("tenant_id") @db.Uuid
  name      String   @db.VarChar(255)
  content   String   @db.Text          // System prompt / template
  variables Json?    @default("[]")    // Template variables
  version   Int      @default(1)
  createdBy String   @map("created_by") @db.Uuid
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  tenant         Tenant         @relation(fields: [tenantId], references: [id])
  agents         Agent[]
  agentVersions  AgentVersion[] @relation("VersionPrompt")

  @@unique([tenantId, name])
  @@index([tenantId])
  @@map("prompts")
}

// Knowledge base for RAG
model KnowledgeBase {
  id         String           @id @default(uuid()) @db.Uuid
  tenantId   String           @map("tenant_id") @db.Uuid
  agentId    String?          @map("agent_id") @db.Uuid
  name       String           @db.VarChar(255)
  type       KnowledgeBaseType
  config     Json             @default("{}")
  chunkCount Int              @default(0) @map("chunk_count")
  status     KnowledgeBaseStatus @default(processing)
  createdBy  String           @map("created_by") @db.Uuid
  createdAt  DateTime         @default(now()) @map("created_at")
  updatedAt  DateTime         @updatedAt @map("updated_at")

  tenant Tenant @relation(fields: [tenantId], references: [id])
  agent  Agent? @relation(fields: [agentId], references: [id])

  @@index([tenantId, agentId])
  @@map("knowledge_bases")
}

enum KnowledgeBaseType {
  document
  website
  faq
  csv
  api
  manual
}

enum KnowledgeBaseStatus {
  processing
  ready
  failed
  disabled
}
```

## Agent Builder Workflow

```typescript
// Agent creation and deployment flow
import { prisma } from '@/lib/db'
import { kafka } from '@/lib/kafka'

export async function createAgent(data: CreateAgentInput, userId: string) {
  // 1. Create agent
  const agent = await prisma.agent.create({
    data: {
      tenantId: data.tenantId,
      name: data.name,
      description: data.description,
      voiceId: data.voiceId,
      promptId: data.promptId,
      language: data.language,
      config: data.config,
      status: 'draft',
      createdBy: userId
    }
  })

  // 2. Create initial version (v1)
  await prisma.agentVersion.create({
    data: {
      agentId: agent.id,
      version: 1,
      config: data.config,
      voiceId: data.voiceId,
      promptId: data.promptId,
      createdBy: userId,
      isActive: false
    }
  })

  return agent
}

export async function deployAgent(agentId: string, userId: string, note?: string) {
  const agent = await prisma.agent.findUnique({
    where: { id: agentId },
    include: { versions: { orderBy: { version: 'desc' }, take: 1 } }
  })

  if (!agent) throw new Error('Agent not found')
  if (agent.status === 'deleted') throw new Error('Agent is deleted')

  const latestVersion = await prisma.agentVersion.create({
    data: {
      agentId: agent.id,
      version: (agent.versions[0]?.version ?? 0) + 1,
      config: agent.config,
      voiceId: agent.voiceId,
      promptId: agent.promptId,
      createdBy: userId,
      publishNote: note,
      isActive: true
    }
  })

  // Deactivate other versions
  await prisma.agentVersion.updateMany({
    where: { agentId: agent.id, id: { not: latestVersion.id } },
    data: { isActive: false }
  })

  // Update agent status
  await prisma.agent.update({
    where: { id: agentId },
    data: { status: 'active', deployedAt: new Date() }
  })

  // Notify voice service of config change
  await kafka.produce('agent.deployed', {
    agentId: agent.id,
    version: latestVersion.version,
    tenantId: agent.tenantId,
    timestamp: new Date().toISOString()
  })

  return latestVersion
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent Versioning | Optimistic (new version on deploy) | Simple, no merge conflicts |
| Config Storage | JSON column in PostgreSQL | Flexible schema, no migration per field |
| Voice/Prompt Reference | Foreign key (immutable reference) | Integrity, can't delete used voice |
| Knowledge Base | Separate model with 1:N to agent | Can be shared across agents |
| Agent Status | State machine (draft→testing→active→paused→archived) | Controlled lifecycle, audit trail |

## Integration Points

- **Part 04 (Core Voice)** — Agent config drives voice pipeline behavior
- **Part 05 (AI Conversation)** — Prompt and KB used by AI orchestrator
- **Part 06 (Agent Builder)** — UI surface for creating/managing agents
- **Part 13 (Knowledge Base)** — RAG integration with KB documents

## Production Considerations

- **Config Validation**: Zod schemas validate agent config before DB write
- **Version Limit**: Max 100 versions per agent; older versions archived
- **Caching**: Active agent config cached in Redis (TTL: 5 minutes)
- **Deployment Hook**: Agent deployment triggers cache invalidation in voice service
- **Prompt Templates**: Use Handlebars/Mustache syntax for variable interpolation
- **A/B Testing**: Deploy two versions to different call percentages for testing
