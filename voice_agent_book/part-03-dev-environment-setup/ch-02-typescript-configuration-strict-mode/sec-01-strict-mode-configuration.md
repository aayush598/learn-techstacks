# Section 01: Strict Mode Configuration

## Overview

TypeScript strict mode is the foundation of our type safety strategy. By enabling the full set of strict checks, we catch entire categories of bugs at compile time that would otherwise manifest as runtime errors in production voice calls — where a crash means a dropped call or a failed transcription.

## Strict Mode Flags

TypeScript's strict mode is a meta-flag that enables several individual checks. Here's each flag and what it protects against in the context of a voice agent platform:

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "useUnknownInCatchVariables": true
  }
}
```

```text
┌────────────────────────────────────────────────────────────┐
│              TypeScript Strict Mode Flags                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ strict: true (enables all below)                     │   │
│  │                                                      │   │
│  │ ├── strictNullChecks        ● Prevent null/undefined │   │
│  │ ├── strictFunctionTypes     ● Variance checking      │   │
│  │ ├── strictBindCallApply     ● Correct function calls │   │
│  │ ├── strictPropertyInit      ● Class property init    │   │
│  │ ├── noImplicitAny           ● Explicit types         │   │
│  │ ├── noImplicitReturns       ● All paths return       │   │
│  │ ├── noUncheckedIndexAccess  ● Safe array/object access│   │
│  │ ├── noImplicitOverride      ● Explicit override       │   │
│  │ ├── exactOptionalProperty   ● Optional ≠ undefined    │   │
│  │ ├── noPropertyAccessFromIdx ● No dot access on index  │   │
│  │ └── useUnknownInCatch       ● Safe catch typing       │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

## Flag-by-Flag Analysis

### strictNullChecks

The most impactful flag. Without it, `null` and `undefined` are assignable to any type.

```typescript
// Without strictNullChecks — this compiles fine
const agentName: string = agent?.name; // Might be undefined at runtime

// With strictNullChecks — this is a compile error
const agentName: string = agent?.name;
// Error: Type 'string | undefined' is not assignable to type 'string'

// Correct approach
const agentName: string | undefined = agent?.name;

// Or provide a default
const agentName: string = agent?.name ?? "Unnamed Agent";
```

**Impact on voice platform**: An agent's `voiceId` could be null in the database. Without strict null checks, we might pass `null` to the TTS provider, causing an unhandled crash mid-call.

### noUncheckedIndexedAccess

Array and object access returns `T | undefined` instead of `T`:

```typescript
// Without noUncheckedIndexedAccess
const agents: Agent[] = await getAgents();
const first = agents[0]; // Type: Agent (but might be undefined!)

// With noUncheckedIndexedAccess
const agents: Agent[] = await getAgents();
const first = agents[0]; // Type: Agent | undefined

// Safe access
if (first !== undefined) {
  processAgent(first); // TypeScript knows first is Agent here
}
```

### exactOptionalPropertyTypes

This flag prevents assigning `undefined` to an optional property that wasn't explicitly declared as `| undefined`:

```typescript
interface AgentConfig {
  name: string;
  description?: string; // Optional, but not explicitly undefined
}

const config: AgentConfig = {
  name: "Support Agent",
  description: undefined, // Error with exactOptionalPropertyTypes
};

// Correct:
const config: AgentConfig = {
  name: "Support Agent",
};
// description is simply absent, not undefined
```

### noPropertyAccessFromIndexSignature

Prevents accessing properties via dot notation when the type uses an index signature:

```typescript
interface CallMetadata {
  [key: string]: unknown;
  duration: number;
}

const metadata: CallMetadata = getCallMetadata();
metadata.duration; // OK — explicitly declared
metadata.customField; // Error with noPropertyAccessFromIndexSignature
metadata["customField"]; // OK — bracket notation for index signature
```

### noImplicitOverride

Ensures subclass methods explicitly mark overrides:

```typescript
class VoiceProvider {
  async synthesize(text: string): Promise<AudioBuffer> {
    // Base implementation
  }
}

class ElevenLabsProvider extends VoiceProvider {
  // Error: Missing 'override' keyword
  async synthesize(text: string): Promise<AudioBuffer> {
    // Custom implementation
  }
}

// Correct:
class ElevenLabsProvider extends VoiceProvider {
  override async synthesize(text: string): Promise<AudioBuffer> {
    return this.callElevenLabsAPI(text);
  }
}
```

### useUnknownInCatchVariables

Forces catch clauses to type the error as `unknown` instead of `any`:

```typescript
// Without the flag
try {
  await processCall(callId);
} catch (error) {
  // error is 'any' — can access anything unsafely
  console.log(error.message); // Might crash if error is not an Error
}

// With the flag
try {
  await processCall(callId);
} catch (error) {
  // error is 'unknown' — must narrow first
  if (error instanceof Error) {
    console.log(error.message); // Safe
    logError(error);
  } else {
    console.error("Unknown error:", error);
  }
}
```

## Base TypeScript Configuration

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  }
}
```

## Strict Mode Configuration by Package Type

### Library Package (e.g., @voice-agent/db)

```jsonc
{
  "extends": "@voice-agent/config-typescript/base.json",
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

### Next.js Application

```jsonc
{
  "extends": "@voice-agent/config-typescript/nextjs.json",
  "compilerOptions": {
    "jsx": "preserve",
    "plugins": [{ "name": "next" }]
  }
}
```

## Trade-offs and Mitigations

### Development Velocity Impact

Strict mode surfaces more errors, which can slow initial development. However, the time spent fixing compile errors is significantly less than debugging production crashes:

```text
Without strict mode:
  Write code (fast) → Runtime error (slow debug) → Fix → Deploy
  Average: 2 hours per null-related bug

With strict mode:
  Write code (slower) → Compile error (instant fix) → Deploy
  Average: 5 minutes per null-related prevention
```

### Migration Path for Legacy Code

If strict mode is being added to an existing project, use incremental adoption:

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "exactOptionalPropertyTypes": false, // Opt out initially
    "noPropertyAccessFromIndexSignature": false // Opt out initially
  }
}
```

Alternatively, use `// @ts-expect-error` comments with a tracking ticket to gradually fix violations.

## Integration Points

- **tsconfig.json**: Applied at the root and per-package
- **CI pipeline**: `turbo typecheck` verifies all packages compile
- **Editor**: VS Code uses the same tsconfig for IntelliSense
- **Pre-commit hook**: Type checking runs on staged files

## Production Considerations

1. **never type**: When strictNullChecks is enabled, some edge cases produce `never`. Understand type narrowing to work with, not against, the type system
2. **Generic constraints**: Strict mode may require additional generic constraints. For example, `T extends Record<string, unknown>` instead of `T extends object`
3. **Third-party types**: `skipLibCheck: true` prevents type errors from node_modules from blocking your build, but periodically run `turbo typecheck --no-skipLibCheck` to audit external type quality
4. **Performance**: Strict mode can slow type checking on very large projects. Use TypeScript's incremental builds (`tsc --incremental`) and project references to mitigate
5. **Version upgrades**: When upgrading TypeScript, new strict flags may be added. Review the changelog and adopt new flags deliberately, not blindly
