# Section 08: Voice Survey Adapter

## Overview

The voice survey adapter is the unified integration layer that abstracts away the differences between multiple survey platform providers (Twilio Studio, Amazon Connect Voice ID, Genesys Cloud CX Surveys, custom IVR systems) behind a consistent interface. It enables the survey framework to deliver surveys, collect responses, and manage survey flows without being coupled to any specific provider. The adapter pattern allows adding new survey providers with minimal changes to the core survey orchestrator.

The adapter sits at the boundary between the survey orchestrator and the telephony/IVR layer. It handles provider-specific protocol differences: Twilio uses TwiML verbs for DTMF collection, Amazon Connect uses Lambda-backed contact flows, and Genesys uses Architect flows. The adapter normalizes these differences into a common `VoiceSurveyProvider` interface that exposes methods for `startSurvey`, `collectResponse`, `endSurvey`, and `handleError`. It also manages provider-specific state serialization for long-running surveys.

## Architecture

```
                Voice Survey Adapter Architecture

   Survey Orchestrator → Voice Survey Adapter
                                |
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
             Twilio        Amazon       Genesys
             Provider      Connect      Cloud
                    |           |           |
                    ▼           ▼           ▼
             TwiML App   Lambda      Architect
                          Function    Flow
                    |           |           |
                    └───────────┼───────────┘
                                ▼
                        Provider Registry
                        (tenant → provider
                         mapping)
```

## Design Decisions

- **Provider adapter with registry pattern over hard-coded provider logic:** The adapter maintains a provider registry mapping each tenant to their configured survey provider. The orchestrator only references the `VoiceSurveyProvider` interface; provider selection happens through a factory method. Adding a new provider requires implementing the interface and registering it, with zero changes to the orchestrator. Trade-off: the interface abstraction may not perfectly capture all provider-specific features (e.g., Twilio's `<Gather>` verb has different timeout semantics than Amazon Connect's "Get customer input" block), requiring feature detection or polyfill logic.

- **State serialization for long-running surveys over in-memory sessions:** Voice surveys can last 2-5 minutes with multiple questions. The adapter serializes session state (current question index, accumulated responses, provider-specific context) to Redis after each question. If the voice server restarts or the call is transferred, the session can be reconstructed. Trade-off: serialization adds 5-10 ms per question transition and requires careful handling of concurrent modifier requests during the survey.

- **Provider-agnostic error handling with tenant-specific fallback over blanket retry:** Each provider has different error modes (Twilio rate limits, Amazon Connect throttling, Genesys session timeouts). The adapter implements a provider-specific error classification that maps to a common error taxonomy (`TRANSIENT`, `CONFIGURATION`, `QUOTA_EXCEEDED`, `PROVIDER_UNAVAILABLE`). Transient errors trigger automatic retry with exponential backoff; configuration errors trigger tenant admin alerts; provider unavailability triggers a fallback to the secondary provider for the tenant. Trade-off: mapping 40+ provider-specific error codes to 4 categories requires ongoing maintenance as providers add new error types.

## Implementation Approach

```typescript
interface VoiceSurveyProvider {
  name: string;
  startSurvey(params: StartSurveyParams): Promise<SurveySession>;
  collectResponse(session: SurveySession, prompt: string, options: CollectOptions): Promise<CollectResult>;
  endSurvey(session: SurveySession): Promise<void>;
  handleError(error: ProviderError): Promise<ErrorAction>;
  serializeSession(session: SurveySession): string;
  deserializeSession(data: string): SurveySession;
}

interface StartSurveyParams {
  callSid: string;
  tenantId: string;
  phoneNumber: string;
  surveyType: string;
  language: string;
  providerConfig: Record<string, unknown>;
}

interface SurveySession {
  id: string;
  provider: string;
  callSid: string;
  tenantId: string;
  providerSessionId: string;
  state: Record<string, unknown>;
  currentStep: number;
  createdAt: number;
}

interface CollectOptions {
  inputType: 'dtmf' | 'speech' | 'hybrid';
  maxDigits: number;
  timeout: number;
  retries: number;
  speechHintKeywords?: string[];
}

interface CollectResult {
  success: boolean;
  input: string;
  confidence: number;
  inputType: 'dtmf' | 'speech';
  durationMs: number;
  error?: ProviderError;
}

class VoiceSurveyAdapter {
  private providers: Map<string, VoiceSurveyProvider> = new Map();
  private tenantProviderRegistry: Map<string, string> = new Map();
  private sessionStore: RedisClient;

  constructor() {
    this.registerProvider('twilio', new TwilioVoiceSurveyProvider());
    this.registerProvider('amazon_connect', new AmazonConnectVoiceSurveyProvider());
    this.registerProvider('genesys', new GenesysVoiceSurveyProvider());
  }

  registerProvider(name: string, provider: VoiceSurveyProvider): void {
    this.providers.set(name, provider);
  }

  configureTenantProvider(tenantId: string, providerName: string): void {
    if (!this.providers.has(providerName)) {
      throw new Error(`Unknown provider: ${providerName}`);
    }
    this.tenantProviderRegistry.set(tenantId, providerName);
  }

  async startSurvey(params: StartSurveyParams): Promise<SurveySession> {
    const provider = this.getProviderForTenant(params.tenantId);
    return provider.startSurvey(params);
  }

  async collectResponse(
    sessionId: string,
    prompt: string,
    options: CollectOptions
  ): Promise<CollectResult> {
    const session = await this.getSession(sessionId);
    const provider = this.getProvider(session.provider);

    try {
      const result = await provider.collectResponse(session, prompt, options);
      // Persist updated session state
      await this.saveSession(session);
      return result;
    } catch (error) {
      const errorAction = await provider.handleError(error as ProviderError);
      switch (errorAction.type) {
        case 'retry':
          return this.collectResponse(sessionId, prompt, options);
        case 'failover': {
          // Switch to secondary provider
          const secondaryProvider = this.findSecondaryProvider(
            session.tenantId,
            session.provider
          );
          if (secondaryProvider) {
            const newSession = await secondaryProvider.startSurvey({
              callSid: session.callSid,
              tenantId: session.tenantId,
              phoneNumber: session.state.phoneNumber as string,
              surveyType: session.state.surveyType as string,
              language: session.state.language as string,
              providerConfig: {},
            });
            await this.saveSession(newSession);
            return secondaryProvider.collectResponse(newSession, prompt, options);
          }
          throw error;
        }
        case 'abort':
          throw error;
        default:
          throw error;
      }
    }
  }

  async endSurvey(sessionId: string): Promise<void> {
    const session = await this.getSession(sessionId);
    const provider = this.getProvider(session.provider);
    await provider.endSurvey(session);
    await this.sessionStore.del(`survey:session:${sessionId}`);
  }

  private getProviderForTenant(tenantId: string): VoiceSurveyProvider {
    const providerName = this.tenantProviderRegistry.get(tenantId);
    if (!providerName) {
      throw new Error(`No provider configured for tenant: ${tenantId}`);
    }
    return this.getProvider(providerName);
  }

  private getProvider(name: string): VoiceSurveyProvider {
    const provider = this.providers.get(name);
    if (!provider) {
      throw new Error(`Provider not registered: ${name}`);
    }
    return provider;
  }

  private async getSession(sessionId: string): Promise<SurveySession> {
    const data = await this.sessionStore.get(`survey:session:${sessionId}`);
    if (!data) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    const parsed = JSON.parse(data);
    const provider = this.getProvider(parsed.provider);
    return provider.deserializeSession(data);
  }

  private async saveSession(session: SurveySession): Promise<void> {
    const provider = this.getProvider(session.provider);
    const serialized = provider.serializeSession(session);
    await this.sessionStore.set(`survey:session:${session.id}`, serialized, 'EX', 3600);
  }

  private findSecondaryProvider(
    tenantId: string,
    currentProvider: string
  ): VoiceSurveyProvider | null {
    // Check tenant-level provider priority list
    for (const [name] of this.providers) {
      if (name !== currentProvider) {
        return this.getProvider(name);
      }
    }
    return null;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Twilio SDK (Apache 2.0) | Server | Twilio voice survey provider |
| AWS SDK (Apache 2.0) | Server | Amazon Connect voice survey provider |
| Redis (RSAL) | Server | Session state persistence |
| Winston (MIT) | Server | Provider operation logging |

## Production Considerations

**Scaling:** Each provider maintains its own connection pool. The Twilio provider uses keep-alive HTTP connections to Twilio's API (pool size: 50 per node). The Amazon Connect provider uses the AWS SDK's built-in retry mechanism with a max of 3 attempts. Session data in Redis is TTL-based (1 hour) — abandoned surveys are automatically cleaned up. For high-throughput tenants, provision dedicated provider-specific worker pools to avoid one provider's throttling affecting other tenants.

**Security:** Provider credentials (API keys, AWS IAM roles, client secrets) are stored in a secrets manager and injected at adapter initialization, never serialized into session state. Provider API calls use tenant-scoped API keys where supported. Session state does not contain PII; the adapter stores provider session IDs rather than phone numbers or customer names in the session blob.

**Monitoring:** Track per-provider survey delivery latency, per-provider error rate and error distribution, failover frequency (percentage of surveys using secondary provider), and session recovery rate. Alert if any provider's error rate exceeds 5%, if failover rate exceeds 2% of total surveys, or if session store get/set latency exceeds 50 ms at p99.
