# Input Guardrails (23 Guards)

Input guardrails validate user prompts before they reach the LLM. They protect against prompt injection, sensitive data leakage, content policy violations, and abuse.

---

## SI-1. InputSizeGuardrail
**Registered Name**: `InputSize`  
**File**: `modules/guardrails/guards/input/input-size.guardrail.ts`

### Purpose
Protects infrastructure from oversized payloads, controls LLM cost & latency, detects abuse via size heuristics.

### Config
```typescript
interface InputSizeConfig {
  maxChars?: number;           // default: 50,000
  maxBytes?: number;           // default: 200,000
  warnThresholdRatio?: number;  // default: 0.8 (80%)
  truncateOnSoftLimit?: boolean; // default: false
  truncateToChars?: number;     // default: maxChars
  abuseSignal?: boolean;        // default: true
}
```

### Execution Logic
1. Count characters and UTF-8 bytes
2. **HARD BLOCK** if `charCount > maxChars` OR `byteCount > maxBytes` → sets `excessiveFailures` security signal
3. **SOFT LIMIT WARN** if `charCount >= warnThreshold` (e.g., 40K chars out of 50K max)
4. **MODIFY** (truncate) if `truncateOnSoftLimit` is enabled
5. **ALLOW** if all within limits

### Enhancement Ideas
- Add token counting (tiktoken) for LLM-specific limits
- Add streaming-aware size tracking
- Support model-specific limits (e.g., GPT-4 has 8K vs Claude has 100K)

---

## SI-2. SecretsInInputGuardrail
**Registered Name**: `SecretsInInput`  
**File**: `modules/guardrails/guards/input/secrets.guardrail.ts`

### Purpose
Detects API keys, tokens, and credentials in user input to prevent accidental leakage.

### Detected Secret Types
- AWS Access Keys (`AKIA...`)
- GitHub Tokens (`ghp_...`)
- OpenAI API Keys (`sk-...`)
- Stripe API Keys (`sk_test_...` / `sk_live_...`)
- Generic API Keys (`api_key: ...`)
- Bearer Tokens
- Private Key Blocks (`-----BEGIN PRIVATE KEY-----`)
- JWT Tokens

### Config
```typescript
interface SecretsInInputGuardrailConfig {
  allowlist?: string[];  // specific secret types to check
  warnOnly?: boolean;    // WARN instead of BLOCK
}
```

### Key Feature
Uses `mask()` to partially redact secrets in metadata logs (shows first 4 + last 4 chars).

### Enhancement Ideas
- Add entropy-based detection for unknown token patterns
- Integrate with a secrets scanner API (e.g., GitLeaks, TruffleHog)
- Add support for more cloud provider keys (GCP, Azure)
- Context-aware detection to reduce false positives

---

## SI-3. NSFWAdvancedGuardrail
**Registered Name**: `NSFWAdvanced`  
**File**: `modules/guardrails/guards/input/nsfw.guardrail.ts`

### Purpose
Multi-layer, multi-signal NSFW content detection. The most complex input guardrail (424 lines).

### Architecture
```
Input Text
    │
    ├── 1. Blocklist check (custom terms)
    ├── 2. Pattern tiers (Level 3 → 2 → 1)
    │       ├── Level 3: Explicit sexual acts (BLOCK)
    │       ├── Level 2: Contextual sexual themes (WARN/BLOCK)
    │       └── Level 1: Mature references (ALLOW)
    ├── 3. Obfuscation detection (character separation, misspellings)
    ├── 4. Context analysis (medical/educational, erotic, roleplay)
    ├── 5. Medical/Educational exemption (reduces modifier by 70%)
    └── 6. Ensemble decision engine
```

### Severity Levels
```typescript
enum NSFWSeverityLevel {
  LEVEL_0_ALLOWED = 0,    // Safe - ALLOW
  LEVEL_1_RESTRICTED = 1, // Mature themes - ALLOW
  LEVEL_2_CONTEXTUAL = 2, // Mature content - WARN or BLOCK (age-gated)
  LEVEL_3_CRITICAL = 3,   // Explicit - BLOCK
}
```

### Config
```typescript
interface NSFWGuardrailConfig {
  severityThreshold?: NSFWSeverityLevel;
  enableContextAnalysis?: boolean;
  requireAgeVerification?: boolean;
  allowMedicalEducational?: boolean;
  enableObfuscationDetection?: boolean;
  customBlocklist?: string[];
  customAllowlist?: string[];
  minConfidence?: number;  // default: 0.7
}
```

### Decision Logic
The `makeDecision()` function implements an ensemble approach:
1. Level 3 signals → BLOCK (regardless of confidence)
2. Level 2 signals above `minConfidence`:
   - If `requireAgeVerification` and age not verified → BLOCK
   - Otherwise → WARN
3. Level 1 signals → ALLOW
4. No signals → ALLOW

### Enhancement Ideas
- Add image-based NSFW detection (vision API)
- Implement ML classifier as alternative to regex
- Add more obfuscation patterns (emoji, zero-width chars, Unicode normalization attacks)
- Expose telemetry for dashboard analytics

---

## SI-4. PHIAwarenessGuardrail
**Registered Name**: `PHIAwareness`  
**File**: `modules/guardrails/guards/input/phi-awareness.guardrail.ts`

### Purpose
Detects Protected Health Information (PHI) for HIPAA compliance.

### Detection Categories
- **Medical Terms**: diagnosed with, diabetes, cancer, HIV, blood pressure, etc.
- **Personal Identifiers**: SSN, phone numbers, emails, addresses, patient names

### Config
```typescript
interface PHIAwarenessConfig {
  mode?: 'warn' | 'block';       // default: 'warn'
  allowDeidentified?: boolean;    // default: true
}
```

### Logic
- Medical terms WITHOUT identifiers → ALLOW (de-identified)
- Medical terms WITH identifiers → WARN or BLOCK based on mode
- No medical terms → ALLOW

### Enhancement Ideas
- Add HIPAA-specific identifier patterns (MRN, health plan IDs)
- Add NER-based detection for better accuracy
- Add redaction capability for de-identified output
- More comprehensive medical term dictionary (ICD-10 codes)

---

## SI-5. UrlFileBlockerGuardrail
**Registered Name**: `UrlFileBlocker`  
**File**: `modules/guardrails/guards/input/url-file-blocker.guardrail.ts`

### Purpose
Blocks URLs, file paths, and external references in user input.

### Detection Targets
- HTTP/HTTPS URLs
- FTP URLs
- IPv4 addresses
- File:// URLs
- Windows paths (`C:\...`)
- Unix paths (`/etc/...`)
- Blocked file extensions (`.env`, `.pem`, `.key`, `.crt`, `.sqlite`, `.db`, `.bak`)

### Config
```typescript
interface UrlFileBlockerConfig {
  allowLocalhost?: boolean;
  allowRelativePaths?: boolean;
  blockedExtensions?: string[];
}
```

### Enhancement Ideas
- Add domain allowlist/blocklist
- URL reputation checking (e.g., Google Safe Browsing)
- IP address geolocation checks
- Data URI detection enhancement

---

## SI-6. BinaryAttachmentGuardrail
**Registered Name**: `BinaryAttachment`  
**File**: `modules/guardrails/guards/input/binary-attachment.guardrail.ts`

### Purpose
Prevents binary blobs, base64 payloads, and high-entropy encoded data.

### Detection Methods
1. **Data URLs**: `data:image/png;base64,...`
2. **Base64 Payloads**: long base64 strings with length % 4 == 0
3. **Binary/High-Entropy**: checks for >15% non-printable characters

### Config
```typescript
interface BinaryAttachmentGuardrailConfig {
  minPayloadLength?: number;  // default: 256
  allowBase64?: boolean;
  allowDataUrls?: boolean;
}
```

### Enhancement Ideas
- Add magic number/byte signature detection for file types
- Compressibility check (high entropy = low compressibility)
- Integration with antivirus/file scanning APIs

---

## SI-7. EncodingObfuscationGuardrail
**Registered Name**: `EncodingObfuscation`  
**File**: `modules/guardrails/guards/input/encoding-obfuscation.guardrail.ts`

### Purpose
Detects obfuscated text using base64 encoding, hex encoding, or leetspeak/homoglyphs.

### Detection Capabilities
1. **Base64**: checks if text is likely base64, attempts decode, checks decoded content for sensitive keywords
2. **Hex**: detects long hex strings
3. **Leetspeak**: normalizes `0→o, 1→i, 3→e, 4→a, 5→s, 7→t, @→a, $→s`

### Config
```typescript
interface EncodingObfuscationConfig {
  blockOnDecode?: boolean;      // default: true
  minEncodedLength?: number;    // default: 16
  confidenceThreshold?: number;  // default: 0.7
}
```

### Enhancement Ideas
- Add Unicode normalization (NFKC) for homoglyph attacks
- Add URL encoding detection (%XX sequences)
- Add quoted-printable, uuencode detection
- Add binary-to-text encoding detection (base32, base58)

---

## SI-8. DangerousPatternsGuardrail
**Registered Name**: `DangerousPatterns`  
**File**: `modules/guardrails/guards/input/dangerous-patterns.guardrail.ts`

### Purpose
Blocks malware, exploit, fraud, and weaponization patterns in prompts.

### Pattern Categories
1. **malware**: ransomware, keylogger, trojan, spyware, backdoor, botnet, DDoS
2. **exploit**: SQL injection, XSS payload, buffer overflow, RCE, privilege escalation
3. **command_injection**: `rm -rf /`, `curl | sh`, `wget | bash`, PowerShell -enc
4. **fraud**: credit card generator, OTP bypass, account takeover, phishing templates
5. **weaponization**: bomb making, improvised explosive, weaponize chemical

### Config
```typescript
interface DangerousPatternsConfig {
  strictMode?: boolean;      // BLOCK medium-risk too
  customPatterns?: RegExp[];
}
```

### Logic
- High-risk categories (malware, weaponization, command_injection) → BLOCK
- Low-risk (exploit, fraud) → WARN (or BLOCK if strictMode)
- Always BLOCK if high risk

---

## SI-9. LanguageRestrictionGuardrail
**Registered Name**: `LanguageRestriction`  
**File**: `modules/guardrails/guards/input/language-restriction.guardrail.ts`

### Purpose
Restricts input to approved Unicode scripts/languages.

### Supported Scripts
latin, cyrillic, arabic, devanagari, han, hiragana, katakana, hangul

### Config
```typescript
interface LanguageRestrictionConfig {
  allowedScripts?: [...];       // default: ['latin']
  minAllowedRatio?: number;     // default: 0.95
  maxDisallowedChars?: number;  // default: 2
  warnOnly?: boolean;
}
```

### How It Works
- Iterates over Unicode characters, testing each letter character against allowed scripts
- Ignores whitespace, digits, punctuation, emojis
- Passes if `allowedChars/totalChars >= ratio` OR `disallowed <= maxDisallowedChars`
- Fails with BLOCK/WARN based on `warnOnly`

### Enhancement Ideas
- Add CJK-specific handling (Japanese has 4 scripts mixed)
- Add language detection (not just script detection)
- Support for locale-based restrictions

---

## SI-10. PromptInjectionSignatureGuardrail
**Registered Name**: `PromptInjectionSignature`  
**File**: `modules/guardrails/guards/input/prompt-injection.guardrail.ts`

### Purpose
Detects known prompt injection patterns using regex signatures.

### Pattern Categories
1. **override**: "ignore all instructions", "do not follow rules"
2. **role_escalation**: "you are now system/developer/admin"
3. **jailbreak_templates**: "DAN", "no restrictions"
4. **safety_bypass**: "disable safety filter", "uncensored"

### Config
```typescript
interface PromptInjectionConfig {
  blockThreshold?: number;  // minimum matched patterns to block (default: 1)
  enabled?: boolean;        // disable guardrail entirely
}
```

### Logic
- Counts matching pattern categories
- `matches >= blockThreshold` → BLOCK
- `matches > 0` but below threshold → WARN

---

## SI-11. SystemPromptLeakGuardrail
**Registered Name**: `SystemPromptLeak`  
**File**: `modules/guardrails/guards/input/system-prompt-leak.guardrail.ts`

### Purpose
Prevents attempts to extract system or developer prompts.

### Detection Patterns
- Direct requests: "show system prompt", "reveal hidden prompt"
- Instruction override: "ignore previous instructions"
- Introspection: "what are your instructions", "how are you configured"
- Security probing: "internal policy", "confidential prompt"

### Config
```typescript
interface SystemPromptLeakConfig {
  allowBenignContext?: boolean;  // downgrade BLOCK→WARN
}
```

---

## SI-12. JailbreakPatternGuardrail
**Registered Name**: `JailbreakPattern`  
**File**: `modules/guardrails/guards/input/jailbreak-pattern.guardrail.ts`

### Purpose
Detects common jailbreak templates like DAN-style prompts.

### Patterns
- DAN-style: "do anything now", "DAN mode"
- Instruction override: "ignore previous instructions"
- System prompt override: "system prompt ignore"
- Role reassignment: "you are now an assistant", "pretend to be"
- Safety removal: "no rules", "unfiltered", "uncensored"
- Multi-persona: "two responses", "dual mode"

### Config
```typescript
interface JailbreakPatternConfig {
  warnOnly?: boolean;
  customPatterns?: RegExp[];
}
```

---

## SI-13. CrossContextManipulationGuardrail
**Registered Name**: `CrossContextManipulation`  
**File**: `modules/guardrails/guards/input/cross-context-manipulation.guardrail.ts`

### Purpose
Blocks references to prior conversations or hidden context that attackers use for context injection.

### Patterns
- Prior conversation references: "as we discussed", "from earlier sessions"
- Hidden prompt probing: "what is your system prompt"
- Context persistence abuse: "remember what I said"
- Instruction override: "ignore previous instructions"

### Config
```typescript
interface CrossContextManipulationConfig {
  enforcementMode?: 'block' | 'warn';
  additionalPatterns?: RegExp[];
}
```

---

## SI-14. OverrideInstructionGuardrail
**Registered Name**: `OverrideInstruction`  
**File**: `modules/guardrails/guards/input/override-instruction.guardrail.ts`

### Purpose
Blocks attempts to override system or developer instructions.

### Patterns
- Direct override: "ignore instructions", "bypass system"
- Instruction hierarchy: "system prompt", "developer message"
- Persona/jailbreak: "act as unrestricted", "act as developer"
- Safety disabling: "no rules", "remove safety"

### Config
```typescript
interface OverrideInstructionConfig {
  warnOnly?: boolean;
  customPatterns?: RegExp[];
}
```

---

## SI-15. RoleplayInjectionGuardrail
**Registered Name**: `RoleplayInjection`  
**File**: `modules/guardrails/guards/input/roleplay-injection.guardrail.ts`

### Purpose
Prevents roleplay-based attempts to bypass safety controls.

### Patterns
- Persona switching: "act as", "pretend to be", "you are now"
- Jailbreak framing: "unrestricted AI", "no rules apply"
- Roleplay framing: "this is a roleplay"
- DAN/jailbreak personas

### Config
```typescript
interface RoleplayInjectionConfig {
  allowFictionalRoleplay?: boolean;  // WARN instead of BLOCK
  action?: GuardrailAction;
  severity?: GuardrailSeverity;
}
```

---

## SI-16. RightToErasureGuardrail
**Registered Name**: `RightToErasure`  
**File**: `modules/guardrails/guards/input/right-to-erasure.guardrail.ts`

### Purpose
Detects and routes GDPR "Right to Erasure" (Article 17) requests.

### Signal Categories
1. **Explicit**: "delete my data", "right to be forgotten" (confidence 0.95)
2. **Regulatory**: "GDPR", "Article 17", "data subject request" (confidence 0.9)
3. **Implicit**: "remove everything", "delete profile" (confidence 0.7)

### Config
```typescript
interface RightToErasureConfig {
  minConfidence?: number;           // default: 0.75
  includeLegalBasis?: boolean;      // include GDPR Article 17 reference
}
```

**Note**: This guardrail always returns WARN (never BLOCKS), since erasure requests must be handled, not blocked.

---

## SI-17. UserConsentValidationGuardrail
**Registered Name**: `UserConsentValidation`  
**File**: `modules/guardrails/guards/input/user-consent.guardrail.ts`

### Purpose
Ensures user consent is present before processing personal data (GDPR compliance).

### How It Works
Reads `userConsent` from context:
- No consent object → BLOCK
- Consent not given → check if legal basis exception applies, else BLOCK
- Scopes check: if `requiredScopes` configured, validates all present
- All checks pass → ALLOW

### Config
```typescript
interface UserConsentGuardrailConfig {
  warnOnly?: boolean;
  allowedLegalBases?: string[];  // e.g., ['legal', 'contract']
  requiredScopes?: string[];     // e.g., ['profile', 'analytics']
}
```

---

## SI-18. GDPRDataMinimizationGuardrail
**Registered Name**: `GDPRDataMinimization`  
**File**: `modules/guardrails/guards/input/gdpr-data-minimization.guardrail.ts`

### Purpose
Ensures only necessary personal data is processed (GDPR principle).

### Detection
- Regex-based PII detection (email, phone, SSN, credit card)
- Compares against allowed fields
- Counts excessive items

### Config
```typescript
interface GDPRDataMinimizationConfig {
  allowedFields?: string[];        // default: ['email', 'name', ...]
  maxPersonalDataItems?: number;   // default: 2
  warnOnly?: boolean;
  enablePIIDetection?: boolean;
}
```

---

## SI-19. PoliticalPersuasionGuardrail
**Registered Name**: `PoliticalPersuasion`  
**File**: `modules/guardrails/guards/input/political-persuasion.guardrail.ts`

### Purpose
Prevents targeted political persuasion and election interference.

### Detection Levels
1. **Election interference** (highest): "rig an election", "fake ballots", "suppress votes" → BLOCK
2. **Targeted persuasion**: demographic targeting + political action → BLOCK
3. **Generic persuasion**: "vote for", "support this party" → WARN

### Config
```typescript
interface PoliticalPersuasionConfig {
  strictMode?: boolean;          // BLOCK generic persuasion too
  blockElectionInterference?: boolean;  // default: true
}
```

---

## SI-20. SelfHarmGuardrail
**Registered Name**: `SelfHarm`  
**File**: `modules/guardrails/guards/input/self-harm.guardrail.ts`

### Purpose
Detects suicide ideation, self-harm intent, and related content.

### Severity Levels
1. **Imminent**: "I am going to kill myself", "I plan to kill myself" → BLOCK (0.95 confidence)
2. **Active**: "I want to die", "I don't want to live" → BLOCK (0.85)
3. **Passive**: "suicide", "self-harm" → WARN or BLOCK if strictMode

### Config
```typescript
interface SelfHarmGuardrailConfig {
  strictMode?: boolean;         // BLOCK passive references
  minConfidence?: number;
}
```

---

## SI-21. HateSpeechGuardrail
**Registered Name**: `HateSpeech`  
**File**: `modules/guardrails/guards/input/hate-speech.guardrail.ts`

### Purpose
Blocks hateful or abusive content targeting protected classes.

### Protected Classes
race, religion, ethnicity, nationality, gender, sexual orientation, disability, caste, immigration status

### Detection
- Slur matching (configurable list)
- Violence patterns combined with slurs → CRITICAL
- Slurs alone → BLOCK (or WARN if moderate severity)
- Quoted context → ALLOW (reporting)

### Config
```typescript
interface HateSpeechGuardrailConfig {
  blockSeverity?: 'strict' | 'moderate';
  customSlurs?: string[];
  allowQuotedContext?: boolean;
}
```

---

## SI-22. RegexFilterGuardrail
**Registered Name**: `RegexFilter`  
**File**: `modules/guardrails/guards/input/regex-filter.guardrail.ts`

### Purpose
User-configurable regex-based filtering for custom policies.

### Config
```typescript
interface RegexFilterRule {
  pattern: string;        // regex pattern string
  flags?: string;         // regex flags (e.g., 'gi')
  action: GuardrailAction; // ALLOW | WARN | BLOCK
  message?: string;
}

interface RegexFilterConfig {
  rules: RegexFilterRule[];
  defaultAction?: GuardrailAction;  // default: ALLOW
}
```

### How It Works
- Compiles all rules at construction time
- First matching rule wins (priority order)
- No match → `defaultAction`
- Validates regex at compile time

---

## SI-23. LLMClassifierInjectionGuardrail
**Registered Name**: `LLMClassifierInjection`  
**File**: `modules/guardrails/guards/input/llm-classifier-injection.guardrail.ts`

### Purpose
ML-style ensemble detection of sophisticated prompt injection attempts.

### Signal Types & Weights
| Signal | Weight | High Risk |
|--------|--------|-----------|
| override_instruction | 0.6 | Yes |
| system_prompt_reference | 0.7 | Yes |
| role_change | 0.35 | No |
| jailbreak_keyword | 0.6 | Yes |
| instruction_hierarchy | 0.5 | No |
| meta_prompting | 0.3 | No |

### Scoring Formula
```typescript
// Cumulative weighted scoring:
score += signal.weight * (1 - score)
```
This is a cumulative probability formula, capping at 1.0.

### Special Rule
If BOTH `override_instruction` AND `system_prompt_reference` are detected → immediate BLOCK at score 1.0

### Config
```typescript
interface LLMClassifierInjectionConfig {
  blockThreshold?: number;     // default: 0.8
  warnThreshold?: number;      // default: 0.25
  enableExplainability?: boolean;
}
```
