# Profiles Module

The profiles module manages collections of guardrails organized for specific use cases. It follows a domain-driven design with built-in profiles, a compiler to normalize descriptors, a repository for persistence, and services for resolution.

---

## Architecture

```
profiles/
├── builtins/                  # 6 built-in profiles (no DB needed)
│   ├── index.ts               # Exports BUILTIN_PROFILES array
│   ├── default.profile.ts
│   ├── enterprise.profile.ts
│   ├── child-safety.profile.ts
│   ├── healthcare.profile.ts
│   ├── financial.profile.ts
│   └── minimal.profile.ts
├── compiler/
│   └── compile-profile.ts     # Normalizes raw descriptors → RuntimeProfile
├── domain/
│   ├── profile.ts             # Profile (DB model)
│   ├── profile-descriptor.ts  # ProfileDescriptor (config)
│   └── runtime-profile.ts     # RuntimeProfile (compiled)
├── repository/
│   └── profile.repository.ts  # Data access layer
├── service/
│   ├── profile-resolver.ts    # Resolves profile for execution
│   └── profile.service.ts     # Business logic
└── types/
    └── profile-ui.ts          # UI-facing type
```

---

## Domain Models

### Profile (DB Model)
```typescript
export interface Profile {
  id: string;
  userId: string;
  name: string;
  description?: string;
  isBuiltIn: boolean;
  inputGuardrails: unknown[];    // Raw descriptors
  outputGuardrails: unknown[];
  toolGuardrails: unknown[];
  createdAt: Date;
  updatedAt: Date;
}
```

Maps directly to the `profiles` DB table. Guardrails are stored as JSONB arrays of raw descriptors.

### ProfileDescriptor
```typescript
export interface ProfileDescriptor {
  name: string;
  description?: string;
  inputGuardrails: GuardrailDescriptor[];
  outputGuardrails: GuardrailDescriptor[];
  toolGuardrails: GuardrailDescriptor[];
}
```

Used for defining built-in profiles as constants. `GuardrailDescriptor` has `{ name: string, config?: unknown }`.

### RuntimeProfile (Compiled)
```typescript
export interface RuntimeProfile {
  id: string;
  name: string;
  input: GuardrailDescriptor[];
  output: GuardrailDescriptor[];
  tool: GuardrailDescriptor[];
  all: GuardrailDescriptor[];     // [ ...input, ...output, ...tool ]
}
```

Created by the compiler, this is what gets used at runtime.

---

## Compiler (`compile-profile.ts`)

```typescript
export function compileProfile(profile: {
  id: string; name: string;
  inputGuardrails: unknown[];
  outputGuardrails: unknown[];
  toolGuardrails: unknown[];
}): RuntimeProfile
```

**What it does:**
1. Takes raw guardrail descriptors from DB/builtins
2. Maps each through `normalizeDescriptor()` to get canonical form
3. Filters out nulls (invalid descriptors)
4. Combines all arrays into `all`
5. Returns a clean `RuntimeProfile`

**Why it exists:**
- DB stores descriptors as `unknown[]` (JSONB)
- The normalized form is what the executor expects
- Separates concerns (storage vs runtime format)

---

## Profile Resolver (`profile-resolver.ts`)

The critical function that resolves a profile name to actual guardrails:

```typescript
export async function resolveProfile(params: {
  userId: string;
  profileName: string;
}) {
```

**Resolution Order:**
1. **User-defined profile**: Query `profiles` table by `userId` + `name`
2. **Built-in fallback**: If no DB profile found, search `BUILTIN_PROFILES` array
3. **Error**: If neither found, throw "Profile not found"

Built-in profiles returned from resolver get synthetic IDs like `builtin:default`.

---

## Profile Service (`profile.service.ts`)

```typescript
export class ProfileService {
  async ensureBuiltIns(userId: string): Promise<void>
  async getRuntimeProfiles(userId: string): Promise<RuntimeProfile[]>
}
```

- `ensureBuiltIns()`: Copies all 6 built-in profiles to the user's DB account (only on first access)
- `getRuntimeProfiles()`: Fetches user's profiles and compiles them to RuntimeProfile

---

## Repository (`profile.repository.ts`)

Simple data access with 3 methods:
```typescript
findByUser(userId: string)         // All user profiles
findBuiltIn(userId: string)        // Built-in profiles for user
create(profile: any)               // Insert new profile
```

---

## 6 Built-in Profiles

### 1. Default Profile
```typescript
name: 'default'
inputGuardrails: [
  { name: 'SecretsInInput', config: { severity: 'critical' } },
  { name: 'InputSize', config: { maxChars: 50_000 } },
  { name: 'NSFWAdvanced', config: { ... } },
]
outputGuardrails: [{ name: 'OutputPIIRedaction' }]
```
**Use case**: General-purpose safety

### 2. Enterprise Security Profile
```typescript
name: 'enterprise_security'
inputGuardrails: [
  { name: 'SecretsInInput', config: { severity: 'critical' } },
  { name: 'InputSize', config: { maxChars: 25_000 } },
]
outputGuardrails: [{ name: 'OutputPIIRedaction' }]
```
**Use case**: Strict security, smaller input limits

### 3. Child Safety Profile
```typescript
name: 'child_safety'
inputGuardrails: [
  { name: 'SecretsInInput', config: { severity: 'critical' } },
  { name: 'InputSize', config: { maxChars: 30_000 } },
]
outputGuardrails: [{ name: 'OutputPIIRedaction' }]
```
**Use case**: Children's apps, educational platforms

### 4. Healthcare Profile (HIPAA-aligned)
```typescript
name: 'healthcare'
inputGuardrails: [
  { name: 'PHIAwareness' },
  { name: 'MedicalAdvice' },
  { name: 'SecretsInInput', config: { severity: 'critical' } },
  { name: 'InputSize', config: { maxChars: 40_000 } },
  { name: 'GDPRDataMinimization' },
  { name: 'UserConsentValidation' },
]
outputGuardrails: [
  { name: 'OutputPIIRedaction' },
  { name: 'Confidentiality' },
  { name: 'RetentionCheck' },
]
```
**Use case**: Healthcare/clinical AI systems requiring HIPAA compliance

### 5. Financial Profile
```typescript
name: 'financial'
inputGuardrails: [
  { name: 'SecretsInInput', config: { severity: 'critical' } },
  { name: 'InputSize', config: { maxChars: 35_000 } },
  { name: 'PHIAwareness' },
  { name: 'Defamation' },
  { name: 'GDPRDataMinimization' },
]
outputGuardrails: [
  { name: 'OutputPIIRedaction' },
  { name: 'Confidentiality' },
  { name: 'HallucinationRisk' },
]
toolGuardrails: [
  { name: 'IAMPermission' },
  { name: 'ApiRateLimit' },
]
```
**Use case**: Banking, fintech, and payments — only profile with tool guardrails

### 6. Minimal Profile
```typescript
name: 'minimal'
inputGuardrails: [
  { name: 'InputSize', config: { maxChars: 100_000 } },
]
outputGuardrails: []
```
**Use case**: Development, testing, internal experimentation

---

## Enhancements for Profiles

1. **Profile versioning**: Track changes to profiles over time
2. **Profile inheritance**: "extend" built-in profiles with custom additions
3. **Guardrail ordering**: Allow users to reorder guardrail execution
4. **A/B testing profiles**: Split traffic between profile configurations
5. **API-based profile sharing**: Import/export profiles between accounts
6. **Profile analytics**: Track which profiles are used most, their pass/fail rates
7. **Validation at creation**: Validate descriptor names against registry at profile creation time
8. **Merge capability**: Combine multiple profiles
9. **Scheduled profile switching**: Time-based profile activation
10. **Profile templates**: Marketplace for community-shared profiles
