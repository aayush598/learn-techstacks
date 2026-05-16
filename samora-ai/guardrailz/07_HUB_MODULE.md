# Hub Module

The hub module powers the **GuardrailZ Hub** — a marketplace/catalog for discovering guardrails and profiles.

---

## Directory Structure

```
modules/hub/
├── data/
│   ├── guardrails.catalog.ts    # 41 hub guardrail entries
│   ├── profiles.catalog.ts      # Hub profile entries
│   └── index.ts
├── domain/
│   ├── hub-category.ts          # Category taxonomy
│   ├── hub-filter.ts            # Filter model
│   ├── hub-guardrails.ts        # HubGuardrail type
│   ├── hub-item.ts              # HubItem (base type)
│   ├── hub-profile.ts           # HubProfile type
│   ├── hub-sort.ts              # Sort model
│   ├── hub-stage.ts             # Development stage enum
│   ├── hub-stats.ts             # View/like/share stats
│   └── hub-tags.ts              # Tag system
├── service/
│   ├── hub-query.service.ts     # Search/filter service
│   └── hub-stats.service.ts     # Stats aggregation
└── ui/
    ├── HubCard.tsx              # Card component
    ├── HubClient.tsx            # Main client component
    ├── HubEmptyState.tsx        # Empty state
    ├── HubGrid.tsx              # Grid layout
    ├── HubSidebar.tsx           # Sidebar with filters
    └── HubTopbar.tsx            # Search bar
```

---

## Domain Models

### HubGuardrail
```typescript
interface HubGuardrail {
  id: string;
  slug: string;
  name: string;
  description: string;
  category: string;
  tags: string[];
  stage: 'development' | 'completed';
  icon: string;
  stats: { views: number; likes: number; shares: number };
}
```

### HubItem
```typescript
interface HubItem extends HubGuardrail {
  type: 'guardrail' | 'profile';
}
```

---

## Catalog Data (`guardrails.catalog.ts`)

Contains guardrail entries organized by category:
- **Input Validation** (9): PII Detection, PHI Awareness, URL/File Blocker, Binary Attachment, Secrets Detection, Encoding Obfuscation, Input Size, Dangerous Patterns, Regex Filter, Language Restriction
- **Prompt Security** (6): Prompt Injection, LLM Classifier, System Prompt Leak, Cross-Context, Jailbreak, Roleplay Injection, Override Instruction
- **Output Safety** (9): PII Redaction, Secret Leak, Internal Data Leak, Hallucination Risk, Confidentiality, Schema Validation, Citation Required, Sandboxed Output, Quality Threshold, Env Var Leak, Internal Endpoint Leak, Command Injection Output, Secrets in Logs
- **Content Safety** (7): NSFW, Hate Speech, Self-Harm, Violence, Political Persuasion, Medical Advice, Defamation
- **Tooling & Security** (5): Tool Access Control, Command Injection, Destructive Tool Call, API Rate Limit, File Write Restriction
- **Privacy & Compliance** (4): GDPR Data Minimization, User Consent, Retention Check, Right to Erasure
- **Operational** (5): Rate Limit, Cost Threshold, Model Version Pin, Quality Threshold, Telemetry Enforcement
- **Security** (3): Secrets in Logs, API Key Rotation, IAM Permission

Each has static `stats` (views, likes, shares) and a `stage` indicator.

---

## Frontend Routes

```
/hub                    → HubClient (all guardrails)
/hub/guardrails/[slug]  → Individual guardrail detail page
/hub/profiles/[slug]    → Individual profile detail page
```

The hub uses client-side filtering via the sidebar (category, tags, stage) and search via the top bar.
