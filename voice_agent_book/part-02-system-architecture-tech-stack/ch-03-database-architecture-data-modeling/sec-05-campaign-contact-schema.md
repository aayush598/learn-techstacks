# Section 05: Campaign & Contact Schema

## Outbound Campaign Data Model

Campaigns manage outbound calling operations — from contact lists through dialing to result tracking. This schema supports preview, power, and predictive dialing modes with full compliance (DNC lists, time zone respect).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAMPAIGN & CONTACT SCHEMA                           │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         CAMPAIGN                                │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  id: uuid    │  │  name:       │  │  type:       │          │    │
│  │  │  tenant_id   │  │  "Summer Sale│  │  outbound    │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  status:     │  │  mode:       │  │  config:     │          │    │
│  │  │  "active"    │  │  "predictive"│  │  {maxConcurr │          │    │
│  │  │              │  │              │  │   ent: 50,   │          │    │
│  │  │              │  │              │  │   maxAttempts│          │    │
│  │  │              │  │              │  │   : 3, ...}  │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────┬───────────────────────────────────────┘    │
│                            │                                            │
│                            ▼                                            │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │  ┌──────────────────┐    ┌──────────────────┐                   │     │
│  │  │  Contact List    │    │  Contact List    │                   │     │
│  │  │  "Hot Leads"     │    │  "Follow-ups"    │                   │     │
│  │  │  500 contacts    │    │  1200 contacts   │                   │     │
│  │  └────────┬─────────┘    └────────┬─────────┘                   │     │
│  │           │                       │                             │     │
│  │           ▼                       ▼                             │     │
│  │  ┌─────────────────────────────────────────────────────────┐    │     │
│  │  │                    CONTACTS                              │    │     │
│  │  │  ┌─────────┬──────────┬──────────┬──────────┬────────┐  │    │     │
│  │  │  │ id      │ phone    │ email    │ first_name│ status │  │    │     │
│  │  │  ├─────────┼──────────┼──────────┼──────────┼────────┤  │    │     │
│  │  │  │ c1      │ +1415... │ alice@   │ Alice    │ active  │  │    │     │
│  │  │  │ c2      │ +1510... │ bob@     │ Bob      │ opt_out │  │    │     │
│  │  │  │ c3      │ +1312... │ carol@   │ Carol    │ active  │  │    │     │
│  │  │  └─────────┴──────────┴──────────┴──────────┴────────┘  │    │     │
│  │  └──────────────────────────────────────────────────────────┘    │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                    CALL ATTEMPTS                                  │     │
│  │                                                                   │     │
│  │  ┌─────────┬──────────┬──────────┬──────────┬──────────┬───────┐  │     │
│  │  │ id      │contact_id│ campaign │ attempt  │ status   │ result│  │     │
│  │  ├─────────┼──────────┼──────────┼──────────┼──────────┼───────┤  │     │
│  │  │ ca1     │ c1       │ camp_1   │ 1        │ completed│ answered│  │     │
│  │  │ ca2     │ c1       │ camp_1   │ 2        │ completed│ no_answer│  │     │
│  │  │ ca3     │ c1       │ camp_1   │ 3        │ scheduled│ pending │  │     │
│  │  └─────────┴──────────┴──────────┴──────────┴──────────┴───────┘  │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                     DNC (DO NOT CALL) LIST                        │     │
│  │                                                                   │     │
│  │  ┌─────────┬──────────┬──────────┬──────────┬──────────┬───────┐  │     │
│  │  │ id      │ tenant_id│ phone    │ source   │ expires_at│ reason│  │     │
│  │  ├─────────┼──────────┼──────────┼──────────┼──────────┼───────┤  │     │
│  │  │ dnc1    │ t_acme   │ +1415555 │ internal │ 2026-01-01│ optout│  │     │
│  │  │ dnc2    │ t_acme   │ +1510555 │ national │ 2025-06-01│ reg   │  │     │
│  │  └─────────┴──────────┴──────────┴──────────┴──────────┴───────┘  │     │
│  └──────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prisma Schema

```prisma
// Campaign model
model Campaign {
  id          String         @id @default(uuid()) @db.Uuid
  tenantId    String         @map("tenant_id") @db.Uuid
  agentId     String         @map("agent_id") @db.Uuid
  name        String         @db.VarChar(255)
  description String?        @db.Text
  type        CampaignType   @default(outbound)
  mode        CampaignMode   @default(predictive)
  status      CampaignStatus @default(draft)
  schedule    Json           @default("{}")    // Calling hours, timezone, start/end dates
  config      Json           @default("{}")    // Pacing, retry, compliance settings
  startedAt   DateTime?      @map("started_at")
  completedAt DateTime?      @map("completed_at")
  createdBy   String         @map("created_by") @db.Uuid
  createdAt   DateTime       @default(now()) @map("created_at")
  updatedAt   DateTime       @updatedAt @map("updated_at")

  tenant      Tenant        @relation(fields: [tenantId], references: [id])
  agent       Agent         @relation(fields: [agentId], references: [id])
  creator     User          @relation("CampaignCreator", fields: [createdBy], references: [id])
  contactLists ContactList[]
  callAttempts CallAttempt[]
  calls       Call[]

  @@index([tenantId, status])
  @@index([tenantId, createdAt])
  @@index([agentId])
  @@map("campaigns")
}

enum CampaignType {
  outbound
  inbound
  blended
}

enum CampaignMode {
  preview     // Agent reviews before call
  power       // Auto-dial next after call ends
  progressive // Auto-dial with concurrency limit
  predictive  // Algorithm-based pacing
}

enum CampaignStatus {
  draft
  scheduled
  running
  paused
  completed
  canceled
  archived
}

// Campaign config type
// {
//   "dialing": {
//     "maxConcurrent": 50,
//     "maxAttemptsPerContact": 3,
//     "attemptIntervalMinutes": 1440,  // 24 hours between attempts
//     "maxAttemptsPerDay": 1,
//     "abandonRate": 3,               // Max abandon rate % (predictive)
//     "dialTimeout": 30               // Seconds before marking no-answer
//   },
//   "schedule": {
//     "timezone": "America/New_York",
//     "callingHours": {
//       "monday": { "start": "09:00", "end": "21:00" },
//       "tuesday": { "start": "09:00", "end": "21:00" },
//       ...
//       "saturday": { "start": "10:00", "end": "17:00" },
//       "sunday": null                // No Sunday calling
//     },
//     "respectDst": true,
//     "holidays": ["2025-01-01", "2025-12-25"]
//   },
//   "compliance": {
//     "checkDnc": true,
//     "dncSources": ["internal", "national"],
//     "maxDailyAttempts": 3,
//     "abideByTimeZone": true,
//     "recordingConsent": "optional"  // required | optional | none
//   },
//   "pacing": {
//     "targetConnectedPerMin": 5,
//     "agentUtilizationTarget": 85,   // %
//     "adjustmentInterval": 60        // Seconds between pace adjustments
//   },
//   "callback": {
//     "enabled": true,
//     "maxCallbackAttempts": 2,
//     "callbackWindowHours": 48
//   }
// }

model ContactList {
  id          String   @id @default(uuid()) @db.Uuid
  tenantId    String   @map("tenant_id") @db.Uuid
  campaignId  String?  @map("campaign_id") @db.Uuid
  name        String   @db.VarChar(255)
  description String?  @db.Text
  contactCount Int     @default(0) @map("contact_count")
  createdBy   String   @map("created_by") @db.Uuid
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  tenant   Tenant   @relation(fields: [tenantId], references: [id])
  campaign Campaign? @relation(fields: [campaignId], references: [id])
  contacts Contact[]

  @@index([tenantId])
  @@index([campaignId])
  @@map("contact_lists")
}

model Contact {
  id            String        @id @default(uuid()) @db.Uuid
  contactListId String        @map("contact_list_id") @db.Uuid
  phone         String        @db.VarChar(20)
  email         String?       @db.VarChar(255)
  firstName     String?       @map("first_name") @db.VarChar(100)
  lastName      String?       @map("last_name") @db.VarChar(100)
  company       String?       @db.VarChar(255)
  title         String?       @db.VarChar(255)
  timezone      String?       @db.VarChar(50)
  metadata      Json          @default("{}")
  status        ContactStatus @default(active)
  createdAt     DateTime      @default(now()) @map("created_at")
  updatedAt     DateTime      @updatedAt @map("updated_at")

  contactList  ContactList  @relation(fields: [contactListId], references: [id], onDelete: Cascade)
  callAttempts CallAttempt[]

  @@index([contactListId, status])
  @@index([phone])
  @@map("contacts")
}

enum ContactStatus {
  active
  opt_out
  bounced
  duplicate
  blocked
}

// Contact metadata shape
// {
//   "custom_fields": {
//     "account_number": "ACC-12345",
//     "tier": "premium",
//     "last_purchase_date": "2025-01-15"
//   },
//   "tags": ["high-value", "renewal-due"],
//   "notes": "Prefers afternoon calls",
//   "external_ids": {
//     "crm": "crm_contact_67890",
//     "hubspot": "hs_contact_12345"
//   }
// }

model CallAttempt {
  id          String          @id @default(uuid()) @db.Uuid
  contactId   String          @map("contact_id") @db.Uuid
  campaignId  String          @map("campaign_id") @db.Uuid
  callId      String?         @map("call_id") @db.Uuid
  attemptNumber Int           @default(1) @map("attempt_number")
  status      CallAttemptStatus
  result      CallAttemptResult?
  scheduledAt DateTime?       @map("scheduled_at")
  dialedAt    DateTime?       @map("dialed_at")
  duration    Int?            // seconds
  notes       String?         @db.Text
  createdAt   DateTime        @default(now()) @map("created_at")
  updatedAt   DateTime        @updatedAt @map("updated_at")

  contact  Contact   @relation(fields: [contactId], references: [id])
  campaign Campaign  @relation(fields: [campaignId], references: [id])
  call     Call?     @relation(fields: [callId], references: [id])

  @@index([contactId, attemptNumber])
  @@index([campaignId, status])
  @@index([scheduledAt])
  @@map("call_attempts")
}

enum CallAttemptStatus {
  pending
  scheduled
  dialing
  ringing
  connected
  completed
  failed
  skipped
}

enum CallAttemptResult {
  answered
  no_answer
  busy
  disconnected
  voicemail
  invalid_number
  dnc_hit
  callback_requested
  not_interested
  opted_out
  error
}

// DNC (Do Not Call) numbers
model DncNumber {
  id        String   @id @default(uuid()) @db.Uuid
  tenantId  String   @map("tenant_id") @db.Uuid
  phone     String   @db.VarChar(20)
  source    DncSource
  reason    String?  @db.Text
  expiresAt DateTime? @map("expires_at")
  createdAt DateTime @default(now()) @map("created_at")

  @@unique([tenantId, phone])
  @@index([tenantId, phone])
  @@map("dnc_numbers")
}

enum DncSource {
  internal      // Manual opt-out
  national      // National DNC registry
  state         // State-level DNC
  complaint     // Reported as spam
  litigation    // Legal restrictions
}
```

## Compliance Checking

```typescript
// lib/compliance/dnc-check.ts
import { prisma } from '@/lib/db'

export async function checkDncCompliance(
  tenantId: string,
  phone: string
): Promise<{
  allowed: boolean
  reasons: string[]
}> {
  const reasons: string[] = []

  // 1. Check internal DNC
  const internalDnc = await prisma.dncNumber.findUnique({
    where: { tenantId_phone: { tenantId, phone } }
  })
  if (internalDnc && (!internalDnc.expiresAt || internalDnc.expiresAt > new Date())) {
    reasons.push(`Internal DNC: ${internalDnc.reason ?? 'Opted out'}`)
  }

  // 2. Check national DNC (via external API)
  const nationalDnc = await checkNationalDNC(phone)
  if (nationalDnc.blocked) {
    reasons.push('National DNC registry')
  }

  // 3. Check time zone compliance
  const contact = await prisma.contact.findFirst({
    where: { phone, contactList: { tenantId } }
  })
  if (contact?.timezone) {
    const now = new Date()
    const localHour = new Date(now.toLocaleString('en-US', { timeZone: contact.timezone })).getHours()
    if (localHour < 8 || localHour >= 21) {
      reasons.push(`Outside calling hours (${contact.timezone} local time: ${localHour}:00)`)
    }
  }

  // 4. Check daily attempt limit
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const attemptsToday = await prisma.callAttempt.count({
    where: {
      contact: { phone },
      campaign: { tenantId },
      createdAt: { gte: today }
    }
  })
  if (attemptsToday >= 3) {
    reasons.push('Exceeded daily attempt limit (3)')
  }

  return {
    allowed: reasons.length === 0,
    reasons
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Contact List | Separate model from campaign | Reusable lists across campaigns |
| Call Attempt | Detailed status/result tracking | Analytics, compliance, billing |
| DNC | Internal + national registry | Legal compliance across jurisdictions |
| Contact Status | opt_out, bounced, etc. | Respect user preferences, reduce cost |
| Campaign Mode | Configurable per campaign | Different use cases need different dialing |

## Integration Points

- **Part 09 (Campaign Management)** — Full campaign management implementation
- **Part 04 (Core Voice)** — Campaign drives outbound call initiation
- **Part 07 (Telephony)** — Dialer engine uses campaign config
- **Part 11 (Analytics)** — Campaign performance metrics

## Production Considerations

- **DNC Compliance**: Check DNC before every outbound call attempt; log all checks for audit
- **Scaling**: Predictive dialer uses machine learning to optimally pace calls
- **Rate Limiting**: Max 1000 contacts per batch upload; validate phone format
- **Contact Deduplication**: Check existing contacts by phone+tenant before import
- **Data Retention**: Campaign results retained for 2 years; contact lists retained until campaign archived
- **Compliance Logging**: All compliance checks logged with timestamp, result, and reason
