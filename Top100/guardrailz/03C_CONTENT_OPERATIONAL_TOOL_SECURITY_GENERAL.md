# Content, Operational, Tool, Security & General Guardrails

---

## C. CONTENT / POLICY GUARDRAILS (3 Guards)

### C-1. DefamationGuardrail
**Registered Name**: `Defamation`  
**File**: `modules/guardrails/guards/content/defamation.guardrail.ts`

**Purpose**: Detects and blocks defamatory claims about individuals or organizations.

**Detection**:
- Wrongdoing terms: fraud, scam, criminal, thief, corrupt, embezzlement, money laundering, sexual assault, rape, abuse, bribery, terrorist (configurable)
- Allegation qualifiers: "allegedly", "reportedly", "according to", "claimed that" (downgrade to WARN)

**Config**:
```typescript
interface DefamationGuardrailConfig {
  allowAllegations?: boolean;    // WARN instead of BLOCK with qualifier
  wrongdoingTerms?: string[];    // custom terms
}
```

**Logic**:
- No wrongdoing → ALLOW
- Wrongdoing + qualifier + allowAllegations → WARN
- Wrongdoing + no qualifier → BLOCK

---

### C-2. MedicalAdviceGuardrail
**Registered Name**: `MedicalAdvice`  
**File**: `modules/guardrails/guards/content/medical-advice.guardrail.ts`

**Purpose**: Restricts medical diagnosis or treatment advice.

**Detection Categories**:
1. **Diagnosis**: "you have diabetes", "diagnosed with"
2. **Treatment**: "you should take", "I recommend", "try to rest"
3. **Prescription**: "take 10mg", "increase dosage"

**Config**:
```typescript
interface MedicalAdviceGuardrailConfig {
  strictMode?: boolean;         // BLOCK soft advice too
  allowFirstAid?: boolean;      // default: true
  customBlocklist?: string[];
}
```

**Logic**:
- Custom blocklist → BLOCK
- First aid info → ALLOW
- Diagnosis/prescription → BLOCK
- Treatment advice → WARN (or BLOCK if strictMode)
- Disclaimer presence noted in metadata

---

### C-3. ViolenceGuardrail
**Registered Name**: `Violence`  
**File**: `modules/guardrails/guards/content/violence.guardrail.ts`

**Purpose**: Detects and blocks graphic or extreme violent content.

**Severity Levels**:
1. **EXTREME**: dismemberment, decapitation, gore, burning alive → BLOCK (critical)
2. **GRAPHIC**: blood splatter, stabbing, torture → BLOCK (error)
3. **NON_GRAPHIC**: kill, murder, fight, war, threat → WARN (configurable)
4. **NONE**: no violence → ALLOW

**Config**:
```typescript
interface ViolenceGuardrailConfig {
  warnOnNonGraphic?: boolean;    // default: true
  escalateThreats?: boolean;     // default: true
}
```

---

## O. OPERATIONAL GUARDRAILS (4 Guards)

### O-1. RateLimitGuardrail
**Registered Name**: `RateLimit`  
**File**: `modules/guardrails/guards/operational/rate-limit.guardrail.ts`

**Purpose**: Enforces request rate limits using in-memory sliding window.

**IMPORTANT**: This is an in-memory guardrail (separate from the DB-based rate limiter in `lib/rate-limit.ts`). Uses a `Map<string, { count, resetAt }>` store.

**Config**:
```typescript
interface RateLimitGuardrailConfig {
  limit: number;                  // max requests
  windowMs: number;               // window in ms
  warnThreshold?: number;         // remaining count to warn at
}
```

**Defaults**: 100 requests per 60 seconds.

**Key Feature**: `__clearStore()` static method for testing.

---

### O-2. CostThresholdGuardrail
**Registered Name**: `CostThreshold`  
**File**: `modules/guardrails/guards/operational/cost-threshold.guardrail.ts`

**Purpose**: Blocks or warns when usage exceeds configured cost limits.

**Modes**:
- `request`: uses `estimatedCostUsd` (per-request cost)
- `daily`: uses `dailyCostUsd`
- `monthly`: uses `monthlyCostUsd`

**Config** (REQUIRED):
```typescript
interface CostThresholdConfig {
  maxCostUsd: number;             // REQUIRED
  warnCostUsd?: number;           // default: 80% of maxCostUsd
  mode?: 'request' | 'daily' | 'monthly';
  includeTelemetry?: boolean;
}
```

---

### O-3. ModelVersionPinGuardrail
**Registered Name**: `ModelVersionPin`  
**File**: `modules/guardrails/guards/operational/model-version-pin.guardrail.ts`

**Purpose**: Prevents unintended model version changes by enforcing explicit version pins.

**Config** (REQUIRED):
```typescript
interface ModelVersionPinConfig {
  allowedModels: string[];          // REQUIRED - e.g., ['gpt-4.1-2024-11-20']
  requireExplicitVersion?: boolean; // default: true
  strict?: boolean;                 // default: true
}
```

**Validation**:
- Checks for version suffix pattern: `-YYYY-MM-DD`
- Unknown models → BLOCK (strict) or WARN (non-strict)
- Empty `allowedModels` throws error at construction

---

### O-4. TelemetryEnforcementGuardrail
**Registered Name**: `TelemetryEnforcement`  
**File**: `modules/guardrails/guards/operational/telemetry-enforcement.guardrail.ts`

**Purpose**: Ensures telemetry and audit logging are enabled.

**Config**:
```typescript
interface TelemetryEnforcementConfig {
  requireTelemetry?: boolean;       // default: true
  requireAuditLogging?: boolean;    // default: false
  warnOnly?: boolean;
}
```

**Logic**:
- No telemetry context → BLOCK (or WARN if warnOnly)
- Telemetry disabled → BLOCK
- Audit required but missing → BLOCK (or WARN if warnOnly)
- All checks pass → ALLOW

---

## T. TOOL GUARDRAILS (5 Guards)

### T-1. ToolAccessControlGuardrail
**Registered Name**: `ToolAccess`  
**File**: `modules/guardrails/guards/tool/tool-access.guardrail.ts`

**Purpose**: Advanced, zero-trust tool access control for LLM agents. The most sophisticated guardrail (401 lines).

**Key Components**:

1. **AgentIdentity**: agentId, type (human/agent/service/guest), role (task_only/assistant/orchestrator/admin), identity strength (unverified → KYC_verified), attestation signature
2. **CapabilityToken**: cryptographically signed token using SHA-256 HMAC, containing tool name, allowed actions, constraints, expiry
3. **RuntimeContext**: session ID, environment, geolocation, recent tool calls, risk score
4. **ToolAccessPolicy**: sensitivity-based policy engine with role checks, identity strength requirements, approval requirements, rate limiting
5. **ApprovalSystem**: human-in-the-loop approval workflow
6. **AuditLogger**: immutable audit logging

**Policy Decisions**:
```
ALLOW | DENY | REQUIRE_APPROVAL | ALLOW_WITH_SANITIZATION | AUDIT_ONLY | QUARANTINE
```

**Tool Sensitivity Levels**:
```
PUBLIC_READ → INTERNAL_READ → INTERNAL_WRITE → SENSITIVE_WRITE → PRIVILEGED_ADMIN → EXTERNAL_CREDENTIAL
```

**Config**:
```typescript
interface ToolAccessGuardrailConfig {
  policy: ToolAccessPolicy;
  signingKey: string;
}
```

---

### T-2. IAMPermissionGuardrail
**Registered Name**: `IAMPermission`  
**File**: `modules/guardrails/guards/tool/iam-permission.guardrail.ts`

**Purpose**: Enforces least-privilege IAM permissions for tool invocations.

**Logic**:
- No tool invocation → ALLOW
- Wildcard (`*`) permission found + not allowed → BLOCK (critical)
- Wildcard explicitly allowed → ALLOW (with warning)
- Missing required permissions → BLOCK
- All permissions present → ALLOW

**Config**:
```typescript
interface IAMPermissionGuardrailConfig {
  allowWildcards?: boolean;  // default: false (secure by default)
}
```

---

### T-3. DestructiveToolCallGuardrail
**Registered Name**: `DestructiveToolCall`  
**File**: `modules/guardrails/guards/tool/destructive-tool-call.guardrail.ts`

**Purpose**: Blocks high-risk or destructive tool invocations.

**Patterns Checked**:
- Filesystem: `rm -rf`, `delete file`, `unlink`
- Database: `drop database`, `drop table`, `truncate table`
- Infrastructure: `terraform destroy`, `kubectl delete`, `helm uninstall`
- OS: `eval`, `sudo`
- Wildcard patterns

**Config**:
```typescript
interface DestructiveToolCallConfig {
  allowlist?: string[];     // explicitly allowed tools
  warnOnly?: boolean;
}
```

---

### T-4. FileWriteRestrictionGuardrail
**Registered Name**: `FileWriteRestriction`  
**File**: `modules/guardrails/guards/tool/file-write-restriction.guardrail.ts`

**Purpose**: Restricts file system write access by tools or agents using path validation.

**Checks**:
1. Identifies file write tools by name pattern (`file`, `fs`, `write`)
2. Resolves absolute vs relative paths
3. Blocks hidden files (`.env`, `.git/config`)
4. Checks blocked directories (e.g., `/etc`, `/root`)
5. Enforces allowed directories whitelist
6. Validates file size limits

**Config**:
```typescript
interface FileWriteRestrictionConfig {
  allowedWriteDirs?: string[];
  blockedWriteDirs?: string[];
  allowRelativePaths?: boolean;     // default: false
  maxFileSizeBytes?: number;
  blockHiddenFiles?: boolean;       // default: true
}
```

---

### T-5. ApiRateLimitGuardrail
**Registered Name**: `ApiRateLimit` (Tool-level)  
**File**: `modules/guardrails/guards/tool/api-rate-limit.guardrail.ts`

**Purpose**: Prevents excessive API usage and abuse at the tool level.

**Config** (REQUIRED):
```typescript
interface ApiRateLimitConfig {
  maxRequests: number;           // REQUIRED
  windowMs: number;              // REQUIRED
  keyBy?: 'apiKeyId' | 'userId' | 'profileId' | 'ip';
  mode?: 'BLOCK' | 'WARN';
}
```

**Key Feature**: In-memory sliding window bucket per identifier.

---

## G. GENERAL GUARDRAILS (1 Guard)

### G-1. RetentionCheckGuardrail
**Registered Name**: `RetentionCheck`  
**File**: `modules/guardrails/guards/general/retention-check.guardrail.ts`

**Purpose**: Validates data retention policies and expiration rules.

**Config**:
```typescript
interface RetentionCheckConfig {
  blockOnExpiry?: boolean;    // default: true
  allowLegalHold?: boolean;   // default: true
  clockSkewMs?: number;       // default: 5 min
}
```

**Logic**:
- No retention metadata → ALLOW
- Legal hold active → ALLOW (bypass)
- Invalid timestamp → BLOCK
- Expired → BLOCK (or WARN if blockOnExpiry false)
- Valid → ALLOW

---

## S. SECURITY GUARDRAILS (1 Guard)

### S-1. ApiKeyRotationTriggerGuardrail
**Registered Name**: `ApiKeyRotationTrigger`  
**File**: `modules/guardrails/guards/security/api-key-rotation.guardrail.ts`

**Purpose**: Triggers key rotation on suspected API key compromise.

**Signals Monitored**:
- `apiKeyLeak`: key detected in input/output
- `unusualGeoAccess`: access from unusual location
- `excessiveFailures`: too many auth failures
- `compromisedBy`: external compromise indicators

**Config**:
```typescript
interface ApiKeyRotationConfig {
  signalThreshold?: number;    // min signals to trigger (default: 1)
  blockOnTrigger?: boolean;    // block until rotation (default: false)
  enableTelemetry?: boolean;
}
```

---

## Summary: All 50 Guardrails

| # | Registered Name | Stage | File Location |
|---|----------------|-------|--------------|
| 1 | InputSize | input | input/input-size.guardrail.ts |
| 2 | SecretsInInput | input | input/secrets.guardrail.ts |
| 3 | NSFWAdvanced | input | input/nsfw.guardrail.ts |
| 4 | PHIAwareness | input | input/phi-awareness.guardrail.ts |
| 5 | UrlFileBlocker | input | input/url-file-blocker.guardrail.ts |
| 6 | BinaryAttachment | input | input/binary-attachment.guardrail.ts |
| 7 | EncodingObfuscation | input | input/encoding-obfuscation.guardrail.ts |
| 8 | DangerousPatterns | input | input/dangerous-patterns.guardrail.ts |
| 9 | LanguageRestriction | input | input/language-restriction.guardrail.ts |
| 10 | PromptInjectionSignature | input | input/prompt-injection.guardrail.ts |
| 11 | SystemPromptLeak | input | input/system-prompt-leak.guardrail.ts |
| 12 | JailbreakPattern | input | input/jailbreak-pattern.guardrail.ts |
| 13 | CrossContextManipulation | input | input/cross-context-manipulation.guardrail.ts |
| 14 | OverrideInstruction | input | input/override-instruction.guardrail.ts |
| 15 | RoleplayInjection | input | input/roleplay-injection.guardrail.ts |
| 16 | RightToErasure | input | input/right-to-erasure.guardrail.ts |
| 17 | UserConsentValidation | input | input/user-consent.guardrail.ts |
| 18 | GDPRDataMinimization | input | input/gdpr-data-minimization.guardrail.ts |
| 19 | PoliticalPersuasion | input | input/political-persuasion.guardrail.ts |
| 20 | SelfHarm | input | input/self-harm.guardrail.ts |
| 21 | HateSpeech | input | input/hate-speech.guardrail.ts |
| 22 | RegexFilter | input | input/regex-filter.guardrail.ts |
| 23 | LLMClassifierInjection | input | input/llm-classifier-injection.guardrail.ts |
| 24 | OutputPIIRedaction | output | output/pii-redaction.guardrail.ts |
| 25 | SecretLeakOutput | output | output/secret-leak-output.guardrail.ts |
| 26 | InternalDataLeak | output | output/internal-data-leak.guardrail.ts |
| 27 | HallucinationRisk | output | output/hallucination-risk.guardrail.ts |
| 28 | Confidentiality | output | output/confidentiality.guardrail.ts |
| 29 | OutputSchemaValidation | output | output/output-schema-validation.guardrail.ts |
| 30 | CitationRequired | output | output/citation-required.guardrail.ts |
| 31 | SandboxedOutput | output | output/sandboxed-output.guardrail.ts |
| 32 | QualityThreshold | output | output/quality-threshold.guardrail.ts |
| 33 | EnvVarLeak | output | output/env-var-leak.guardrail.ts |
| 34 | InternalEndpointLeak | output | output/internal-endpoint.guardrail.ts |
| 35 | CommandInjectionOutput | output | output/command-injection.guardrail.ts |
| 36 | SecretsInLogs | output | output/secrets-in-logs.guardrail.ts |
| 37 | Defamation | content | content/defamation.guardrail.ts |
| 38 | MedicalAdvice | content | content/medical-advice.guardrail.ts |
| 39 | Violence | content | content/violence.guardrail.ts |
| 40 | RateLimit | operational | operational/rate-limit.guardrail.ts |
| 41 | CostThreshold | operational | operational/cost-threshold.guardrail.ts |
| 42 | ModelVersionPin | operational | operational/model-version-pin.guardrail.ts |
| 43 | TelemetryEnforcement | operational | operational/telemetry-enforcement.guardrail.ts |
| 44 | ToolAccess | tool | tool/tool-access.guardrail.ts |
| 45 | IAMPermission | tool | tool/iam-permission.guardrail.ts |
| 46 | DestructiveToolCall | tool | tool/destructive-tool-call.guardrail.ts |
| 47 | FileWriteRestriction | tool | tool/file-write-restriction.guardrail.ts |
| 48 | ApiRateLimit | tool | tool/api-rate-limit.guardrail.ts |
| 49 | RetentionCheck | general | general/retention-check.guardrail.ts |
| 50 | ApiKeyRotationTrigger | security | security/api-key-rotation.guardrail.ts |

*(Some guardrails like Defamation, Violence, etc. exist in both the code registry AND the hub catalog)*
