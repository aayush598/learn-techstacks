# Core Guardrail Engine

The guardrail engine is the heart of the platform. It provides an extensible framework for defining, registering, and executing guardrails.

---

## 1. Types (`modules/guardrails/engine/types.ts`)

```typescript
export type GuardrailStage = 'input' | 'output' | 'content' | 'tool' | 'operational' | 'security' | 'general';
export type GuardrailAction = 'ALLOW' | 'WARN' | 'BLOCK' | 'MODIFY';
export type GuardrailSeverity = 'info' | 'warning' | 'error' | 'critical';

export interface GuardrailResult {
  passed: boolean;           // Did the guardrail pass?
  guardrailName: string;     // Name of the guardrail
  action: GuardrailAction;   // What action to take
  severity: GuardrailSeverity;
  message?: string;          // Human-readable message
  redactedText?: string;     // Modified text (for MODIFY action)
  metadata?: Record<string, unknown>; // Additional context
}
```

- **GuardrailStage**: categorizes where a guardrail runs
- **GuardrailAction**: 4 possible outcomes. The executor uses `BLOCK` as short-circuit
- **GuardrailSeverity**: severity level for logging/monitoring
- **GuardrailResult**: every guardrail returns this from its `execute()` method

---

## 2. BaseGuardrail (`modules/guardrails/engine/base.guardrails.ts`)

```typescript
export abstract class BaseGuardrail<Config = unknown> {
  readonly name: string;
  readonly stage: GuardrailStage;
  protected readonly config: Config;

  constructor(name: string, stage: GuardrailStage, config: Config) { ... }

  abstract execute(text: string, context: GuardrailContext): Promise<GuardrailResult> | GuardrailResult;

  protected result(partial: Omit<GuardrailResult, 'guardrailName'>): GuardrailResult {
    return {
      guardrailName: this.name,
      ...partial,
    };
  }
}
```

**Key design decisions:**
- **Abstract class** (not interface): provides `result()` helper and stores common properties
- **Generic Config**: each guardrail defines its own config type, inferred at runtime
- **`execute()` can be sync or async**: some guardrails are purely regex-based (sync), others might call external APIs (async)
- **`result()` helper**: automatically fills `guardrailName` from the class property

---

## 3. Context (`modules/guardrails/engine/context.ts`)

The `GuardrailContext` carries runtime information for guardrail execution:

```typescript
export interface GuardrailContext {
  // Request identity
  validationType?: 'input' | 'output';
  userId?: string;
  apiKeyId?: string;
  profileId?: string;
  ip?: string;

  // Behavioral / risk signals
  ageVerified?: boolean;
  priorViolations?: number;

  // Tool execution
  tool?: BaseToolContext;
  toolAccess?: IAMToolAccessContext;

  // Operational / policy context
  model?: string;
  telemetry?: TelemetryContext;
  usage?: UsageContext;
  retention?: RetentionContext;

  // Security signals
  securitySignals?: SecuritySignals;
}
```

**Sub-contexts:**
- `BaseToolContext`: `{ toolName, toolArgs? }` — identifies a tool invocation
- `IAMToolAccessContext`: extends Base with `{ requiredPermissions, grantedPermissions }`
- `SecuritySignals`: `{ apiKeyLeak?, unusualGeoAccess?, excessiveFailures?, compromisedBy? }`
- `TelemetryContext`: `{ enabled?, auditLogging?, destination? }`
- `UsageContext`: `{ estimatedCostUsd?, dailyCostUsd?, monthlyCostUsd? }`
- `ModelContext`: `{ model? }`
- `RetentionContext`: `{ createdAt, retentionDays, policyId?, legalHold? }`

---

## 4. Registry (`modules/guardrails/engine/registry.ts`)

The registry is a **singleton** `Map<string, GuardrailFactory>` that maps guardrail names to factory functions:

```typescript
export type GuardrailFactory = (config?: unknown) => BaseGuardrail;

export class GuardrailRegistry {
  private readonly registry = new Map<string, GuardrailFactory>();

  register(name: string, factory: GuardrailFactory): void
  create(name: string, config?: unknown): BaseGuardrail
  has(name: string): boolean
  list(): string[]
}

export const guardrailRegistry = new GuardrailRegistry();
```

**Key behaviors:**
- `register()` throws if duplicate name
- `create()` constructs a new instance with optional config
- Singleton export ensures global access
- Deterministic registration order (important since executor runs guardrails sequentially)

**Registry Bootstrap** (`modules/guardrails/registry/index.ts`):
This file, imported at process startup, loads all sub-registries which each register their guardrails:

```
index.ts
├── input.registry.ts       → 17 input guardrails (23 implementations exist)
├── output.registry.ts      → 10 output guardrails (13 implementations exist)
├── tool.registry.ts        → 5 tool guardrails
├── content.registry.ts     → 3 content guardrails
├── operational.registry.ts → 4 operational guardrails
├── general.registry.ts     → 1 general guardrail
└── security.registry.ts    → 1 security guardrail
```

**Total: 41 registered guardrails.** The additional ~9 implementations (6 input + 3 output) exist as code but are not registered in the engine registry — they may be available in the hub catalog or as extensions.

---

## 5. Executor (`modules/guardrails/engine/executor.ts`)

```typescript
export async function executeGuardrails(
  guardrails: BaseGuardrail[],
  text: string,
  context: GuardrailContext = {},
) {
  const results: GuardrailResult[] = [];

  for (const guardrail of guardrails) {
    const result = await guardrail.execute(text, context);
    results.push(result);
    if (result.action === 'BLOCK') break; // Short-circuit!
  }

  return {
    passed: results.every(r => r.passed),
    results,
    executionTimeMs: Date.now() - start,
    summary: {
      total: results.length,
      passed: results.filter(r => r.passed).length,
      failed: results.filter(r => !r.passed).length,
    },
  };
}
```

**Critical design decisions:**
- **Sequential execution**: guardrails run one-by-one in registration order
- **Short-circuit on BLOCK**: if any guardrail blocks, remaining guardrails in the same batch are skipped
- **Execution timing**: total time tracked via `Date.now()` diff
- **Error handling**: if a guardrail throws, it's caught and converted to a BLOCK result with severity `error`

---

## 6. Errors (`modules/guardrails/engine/errors.ts`)

```typescript
export class GuardrailExecutionError extends Error {
  constructor(public readonly guardrail: string, message: string) {
    super(message);
    this.name = 'GuardrailExecutionError';
  }
}
```

Simple custom error class containing the guardrail name that failed.

---

## 7. Descriptors (`modules/guardrails/descriptors/`)

### Types
```typescript
export interface GuardrailDescriptor {
  name: string;
  config?: unknown;
}
```

### Normalizer
Converts various formats → canonical `GuardrailDescriptor`:
```typescript
normalizeDescriptor(raw: unknown): GuardrailDescriptor | null
```

Supports 3 formats:
1. **Canonical**: `{ name: 'InputSize', config: { maxChars: 50000 } }`
2. **Legacy**: `{ class: 'InputSizeGuardrail', config: { ... } }` — strips "Guardrail" suffix
3. **String shorthand**: `'InputSize'` — no config

Returns `null` for invalid input.

---

## 8. Service Layer

### `runGuardrails()` (`modules/guardrails/service/run-guardrails.ts`)
The main execution entry point:
```typescript
export async function runGuardrails(rawDescriptors: unknown[], text: string, context: GuardrailContext)
```
1. Imports the registry bootstrap (side-effect import)
2. Maps each descriptor through `normalizeDescriptor`
3. Creates instances via `guardrailRegistry.create()`
4. Calls `executeGuardrails()` with the instances

### `validateRequest()` (`modules/guardrails/service/validate-request.ts`)
The production validation workflow:
```typescript
export async function validateRequest(input: {
  apiKey: string;
  text: string;
  profileName: string;
  validationType: 'input' | 'output' | 'both';
})
```

**Step-by-step flow:**
1. **Authenticate**: Look up API key in DB, check active status
2. **Rate Limit**: Check per-minute AND per-day limits (API key level + user account level)
3. **Resolve Profile**: Look up user-defined profile, fallback to built-in
4. **Select Guardrails**: Based on `validationType`:
   - `input` → `profile.inputGuardrails`
   - `output` → `profile.outputGuardrails`
   - `both` → `[...inputGuardrails, ...outputGuardrails]`
5. **Execute**: `runGuardrails()` with resolved descriptors
6. **Log**: Insert execution record into `guardrail_executions` table
7. **Return**: Response with results, summary, profile info, rate limits

---

## 9. Contracts (`modules/guardrails/contracts/validate.ts`)

Zod validation schema for the `/api/validate` endpoint:
```typescript
export const ValidateRequestSchema = z.object({
  text: z.string().min(1, 'Text is required'),
  profileName: z.string(),
  validationType: z.enum(['input', 'output', 'both']).default('input'),
});

export interface ValidateResponse {
  passed: boolean;
  profile: { id: string; name: string };
  validationType: 'input' | 'output' | 'both';
  results: GuardrailResult[];
  summary: { total: number; failed: number };
  executionTimeMs: number;
  rateLimits?: unknown;
}
```

---

## 10. Selectable Guardrail Type (`modules/guardrails/types/selectable-guardrail.ts`)

```typescript
export interface SelectableGuardrail {
  name: string;
  enabled: boolean;
}
```

Used in the UI for enabling/disabling guardrails within a profile.
