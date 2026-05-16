# Output Guardrails (13 Guards)

Output guardrails validate model responses before they reach the user. They prevent data leakage, ensure quality, and enforce formatting constraints.

---

## SO-1. OutputPIIRedactionGuardrail
**Registered Name**: `OutputPIIRedaction`  
**File**: `modules/guardrails/guards/output/pii-redaction.guardrail.ts`

### Purpose
Redacts personally identifiable information from model output.

### Redaction Patterns
| PII Type | Pattern | Replacement |
|----------|---------|-------------|
| Email | `user@domain.com` | `[EMAIL_REDACTED]` |
| Phone | `123-456-7890` | `[PHONE_REDACTED]` |
| SSN | `123-45-6789` | `[SSN_REDACTED]` |
| Credit Card | `4111-1111-1111-1111` | `[CARD_REDACTED]` |
| IPv4 | `192.168.1.1` | `[IP_REDACTED]` |

### Behavior
- If any PII found → returns `MODIFY` action with `redactedText`
- No config needed (works out of box)
- Always ALLOWs (never blocks) — redaction is the corrective action

### Enhancement Ideas
- Add more PII types (passport numbers, driver's license, MRN)
- Use NER-based detection for better accuracy
- Add differential privacy noise for aggregate data
- Support custom replacement templates

---

## SO-2. SecretLeakOutputGuardrail
**Registered Name**: `SecretLeakOutput`  
**File**: `modules/guardrails/guards/output/secret-leak-output.guardrail.ts`

### Purpose
Prevents secrets and credentials from appearing in model outputs.

### Detection Patterns
| Secret Type | Pattern |
|-------------|---------|
| OpenAI API Key | `sk-...` (20+ chars) |
| AWS Access Key | `AKIA...` (16 chars) |
| GitHub Token | `ghp_...` (36 chars) |
| Stripe Secret | `sk_live_...` (24+ chars) |
| JWT | `eyJ...` (3-part base64) |
| Private Key | `-----BEGIN...PRIVATE KEY-----` |
| Password Assignment | `password = "..."` |

### Config
```typescript
interface SecretLeakOutputConfig {
  blockOnDetection?: boolean;  // BLOCK instead of MODIFY
  redactWith?: string;         // replacement string
  minEntropyLength?: number;
}
```

---

## SO-3. InternalDataLeakGuardrail
**Registered Name**: `InternalDataLeak`  
**File**: `modules/guardrails/guards/output/internal-data-leak.guardrail.ts`

### Purpose
Blocks exposure of internal or proprietary information in outputs.

### Detection Targets
- Internal domains (`.internal`, `.corp`, `.local`, `.intranet`, or custom)
- Private IP addresses (10.x.x.x, 192.168.x.x, 172.16-31.x.x)
- File system paths (`/etc/...`, `/var/...`, `C:\...`)

### Config
```typescript
interface InternalDataLeakConfig {
  internalDomains?: string[];
  warnOnly?: boolean;
  detectFilePaths?: boolean;  // default: true
}
```

---

## SO-4. HallucinationRiskGuardrail
**Registered Name**: `HallucinationRisk`  
**File**: `modules/guardrails/guards/output/hallucination-risk.guardrail.ts`

### Purpose
Assesses likelihood of hallucinated or fabricated responses.

### Signal Detection
1. **Unverified research claims**: "studies show", "research indicates" without citation
2. **Precise dates without citation**: `2024` with no source reference
3. **Overconfident language**: "always", "never", "guaranteed", "proven"
4. **Hedging conflict**: "I think... definitely" (contradictory certainty)
5. **Missing citations** (if `requireCitations` is enabled)

### Scoring
```typescript
const weights = {
  unverified_research_claim: 0.3,
  precise_date_without_citation: 0.2,
  overconfident_language: 0.2,
  hedging_conflict: 0.2,
  missing_citations: 0.3,
};
// Sum of matched weights, capped at 1.0
```

### Config
```typescript
interface HallucinationRiskConfig {
  warnThreshold?: number;    // default: 0.4
  blockThreshold?: number;   // default: 0.75
  requireCitations?: boolean;
}
```

### Enhancement Ideas
- Add factual grounding via external knowledge base lookup
- Add contradiction detection against known facts
- Integrate with retrieval-augmented generation (RAG) pipeline
- Add confidence scoring per sentence

---

## SO-5. ConfidentialityGuardrail
**Registered Name**: `Confidentiality`  
**File**: `modules/guardrails/guards/output/confidentiality.guardrail.ts`

### Purpose
Ensures confidential or restricted data is not disclosed in outputs.

### Detection Signals
1. **Keywords**: "internal use only", "confidential", "restricted", "do not share", "proprietary"
2. **Environment variables**: `process.env`, `AWS_SECRET`, `API_KEY`, `SECRET_KEY`
3. **Internal IPs**: private ranges
4. **Stack traces**: `at Function (file:line:col)` pattern

### Config
```typescript
interface ConfidentialityGuardrailConfig {
  redact?: boolean;            // MODIFY instead of BLOCK
  keywords?: string[];         // custom keywords
  allowedProfiles?: string[];  // profile-based bypass
}
```

### Profile-Based Access Control
If the request's `profileId` is in the `allowedProfiles` list, confidential data is ALLOW'd instead of blocked.

---

## SO-6. OutputSchemaValidationGuardrail
**Registered Name**: `OutputSchemaValidation`  
**File**: `modules/guardrails/guards/output/output-schema-validation.guardrail.ts`

### Purpose
Validates model output against a required JSON or structured schema using AJV (JSON Schema validator).

### Config
```typescript
interface OutputSchemaValidationConfig {
  schema: Record<string, unknown>;   // REQUIRED
  warnOnly?: boolean;                 // default: false
  allowNonJson?: boolean;             // default: false
}
```

### How It Works
1. Attempts to `JSON.parse(text)`
2. If not valid JSON and `allowNonJson` → ALLOW
3. If not valid JSON and not `allowNonJson` → BLOCK
4. Validates parsed object against JSON Schema via AJV
5. Returns detailed schema errors in metadata

### Enhancement Ideas
- Support multiple schema formats (YAML, XML)
- Add partial validation for streaming outputs
- Support OpenAPI/Swagger schema validation

---

## SO-7. CitationRequiredGuardrail
**Registered Name**: `CitationRequired`  
**File**: `modules/guardrails/guards/output/citation-required.guardrail.ts`

### Purpose
Requires citations or sources for factual claims in outputs.

### Factual Claim Detection (Heuristic)
- "X is 10" pattern (verb + number)
- "according to", "studies show", "research indicates"
- "founded in", "the capital of", "was born in"

### Citation Extraction
- URLs, `[1]` style brackets, markdown links `[text](url)`
- "source:", "according to:" keywords

### Config
```typescript
interface CitationRequiredConfig {
  requireCitations?: boolean;  // BLOCK if missing (default: WARN)
  minCitations?: number;       // default: 1
  enabled?: boolean;           // disable entirely
}
```

### Enhancement Ideas
- Add DOI/PubMed ID validation
- Add link rot detection (dead links)
- Cross-reference with knowledge base

---

## SO-8. SandboxedOutputGuardrail
**Registered Name**: `SandboxedOutput`  
**File**: `modules/guardrails/guards/output/sandboxed-output.guardrail.ts`

### Purpose
Restricts executable or actionable output to prevent command execution.

### Detection Patterns
- Shell commands: `rm`, `sudo`, `chmod`, `chown`, `curl`, `wget`
- Execution environments: `bash`, `sh`, `powershell`
- Dangerous paths: `/etc`, `/usr`, `/bin`
- Code execution: `run()`, `execute()`, `eval()`, `spawn()`
- Script shebangs: `#!/usr/bin/`
- PowerShell: `Invoke-Expression`

### Config
```typescript
interface SandboxedOutputConfig {
  mode?: 'BLOCK' | 'MODIFY';       // default: BLOCK
  extraPatterns?: RegExp[];
}
```

---

## SO-9. QualityThresholdGuardrail
**Registered Name**: `QualityThreshold`  
**File**: `modules/guardrails/guards/output/quality-threshold.guardrail.ts`

### Purpose
Enforces minimum response quality thresholds.

### Metrics Computed
- **Length**: minimum character count (default: 30)
- **Repetition Ratio**: most frequent word / total words (max: 0.4)
- **Unique Word Ratio**: unique words / total words (min: 0.4)

### Config
```typescript
interface QualityThresholdConfig {
  minLength?: number;              // default: 30
  maxRepetitionRatio?: number;     // default: 0.4
  minUniqueWordRatio?: number;     // default: 0.4
  hardFail?: boolean;              // BLOCK instead of WARN
}
```

### Enhancement Ideas
- Add readability score (Flesch-Kincaid)
- Add response coherence metrics
- Add instruction-following assessment
- BERTScore or semantic similarity to expected output

---

## SO-10. EnvVarLeakGuardrail
**Registered Name**: `EnvVarLeak`  
**File**: `modules/guardrails/guards/output/env-var-leak.guardrail.ts`

### Purpose
Prevents leakage of environment variable names and values in outputs.

### Detection
```typescript
const defaultVars = [
  'AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID', 'DATABASE_URL',
  'OPENAI_API_KEY', 'JWT_SECRET', 'API_KEY', 'TOKEN', 'SECRET', 'NODE_ENV',
];
```
Detects both `process.env.SECRET` and `$SECRET` / `${SECRET}` syntax.

### Config
```typescript
interface EnvVarLeakGuardrailConfig {
  redact?: boolean;              // MODIFY instead of BLOCK
  sensitiveVars?: string[];      // custom var names
}
```

---

## SO-11. InternalEndpointLeakGuardrail
**Registered Name**: `InternalEndpointLeak`  
**File**: `modules/guardrails/guards/output/internal-endpoint.guardrail.ts`

### Purpose
Prevents exposure of internal service endpoints.

### Detection Patterns
- `localhost`, `127.0.0.1`, `0.0.0.0`
- Private IPv4 ranges (10.x, 192.168.x, 172.16-31.x)
- Cloud metadata IP: `169.254.169.254`
- Internal DNS: `*.internal`, `*.svc.cluster.local`
- Internal ports: 2375, 2376, 3306, 5432, 6379, 9200, 27017

### Config
```typescript
interface InternalEndpointGuardrailConfig {
  redact?: boolean;                 // MODIFY instead of BLOCK
  additionalPatterns?: RegExp[];
}
```

---

## SO-12. SecretsInLogsGuardrail
**Registered Name**: `SecretsInLogs`  
**File**: `modules/guardrails/guards/output/secrets-in-logs.guardrail.ts`

### Purpose
Detects secrets and credentials before content is logged.

### Detection Patterns
- AWS Access/Secret Keys
- JWT Tokens
- Private Keys (PEM blocks)
- API Keys/Tokens (key: value patterns)
- High-entropy tokens (32+ alphanumeric chars)

### Config
```typescript
interface SecretsInLogsConfig {
  action?: 'BLOCK' | 'REDACT';       // default: BLOCK
  minEntropyLength?: number;         // default: 32
  enableGenericEntropyDetection?: boolean;
}
```

### Enhancement Ideas
- Add context-aware entropy analysis (Shannon entropy)
- Whitelist known safe tokens
- Integration with log management systems (e.g., DataDog, Splunk)

---

## SO-13. CommandInjectionOutputGuardrail
**Registered Name**: `CommandInjectionOutput`  
**File**: `modules/guardrails/guards/output/command-injection.guardrail.ts`

### Purpose
Prevents generation of executable or shell-injection commands.

### Detection Patterns
- Shell execution: `rm -rf`, `sudo`, `chmod +x`
- Pipe to shell: `curl ... | sh`, `wget ... | bash`
- Command chaining: `&&`, `||`, `;`
- Subshell: `$(...)`, backticks
- Redirection: `> /file`, `< /file`
- SQL/system hybrids: `drop table`, `shutdown -h`

### Config
```typescript
interface CommandInjectionGuardrailConfig {
  warnOnly?: boolean;
  extraPatterns?: RegExp[];
}
```
