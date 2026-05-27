# Section 04: Setup Wizard Implementation

## Overview

The setup wizard guides new tenants through their first-time configuration after signup and provisioning. It bridges the gap between "account created" and "first successful call placed," reducing time-to-value and increasing activation rates. A well-designed wizard progressively reveals complexity, asking only for information needed at each stage, and allowing users to skip non-essential configuration and return to it later.

The wizard typically includes: company profile (name, industry, timezone), team member invitations, phone number setup (purchase or bring your own), agent creation (or selecting from templates), voice selection (trying different voices), knowledge base setup (uploading documents or connecting sources), integration connections (CRM, calendar), and a first test call. Each step saves progress to the database, allowing the user to leave and resume.

Progress is shown as a step indicator with completion status. Jumps between steps are allowed for non-dependent configuration. A "Getting Started" checklist in the dashboard shows remaining setup items for users who skip steps.

## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface WizardStep {
  id: string;
  title: string;
  description: string;
  required: boolean;
  component: React.ComponentType<WizardStepProps>;
  validate: (data: any) => ValidationResult;
  onSave: (tenantId: string, data: any) => Promise<void>;
}

class SetupWizardService {
  private steps: WizardStep[] = [
    {
      id: 'company_profile',
      title: 'Company Profile',
      description: 'Tell us about your business',
      required: true,
      component: CompanyProfileStep,
      validate: (data) => data.name?.length > 0 ? { valid: true } : { valid: false, error: 'Company name required' },
      onSave: async (tenantId, data) => {
        await db.query('UPDATE tenants SET name = $1, industry = $2, timezone = $3 WHERE id = $4',
          [data.name, data.industry, data.timezone, tenantId]);
      },
    },
    {
      id: 'phone_number',
      title: 'Phone Number',
      description: 'Get a voice agent number or bring your own',
      required: true,
      component: PhoneNumberStep,
      validate: (data) => data.phoneNumber ? { valid: true } : { valid: false, error: 'Phone number required' },
      onSave: async (tenantId, data) => {
        if (data.purchaseNew) {
          await phoneNumberService.provisionNumber(tenantId, data.areaCode);
        } else {
          await phoneNumberService.verifyAndImport(tenantId, data.existingNumber);
        }
      },
    },
  ];

  async getWizardProgress(tenantId: string): Promise<WizardProgress> {
    const completed = await this.getCompletedSteps(tenantId);
    const currentStep = this.getCurrentStep(completed);
    
    return {
      totalSteps: this.steps.length,
      completedSteps: completed.length,
      currentStep: currentStep?.id,
      completedStepIds: completed.map(s => s.id),
      percentage: Math.round((completed.length / this.steps.length) * 100),
    };
  }

  async completeStep(tenantId: string, stepId: string, data: any): Promise<void> {
    const step = this.steps.find(s => s.id === stepId);
    if (!step) throw new Error(`Unknown step: ${stepId}`);
    
    const validation = step.validate(data);
    if (!validation.valid) throw new ValidationError(validation.error);
    
    await step.onSave(tenantId, data);
    await this.markStepCompleted(tenantId, stepId);
  }

  private getCurrentStep(completed: WizardStep[]): WizardStep | null {
    const completedIds = new Set(completed.map(s => s.id));
    return this.steps.find(s => !completedIds.has(s.id)) || null;
  }
}

// Step persistence
async function saveWizardState(tenantId: string, stepId: string, data: any): Promise<void> {
  await redis.setex(
    `wizard:${tenantId}:${stepId}`,
    86400, // 24h TTL
    JSON.stringify(data)
  );
  await redis.sadd(`wizard:${tenantId}:completed`, stepId);
}

async function getWizardState(tenantId: string): Promise<Record<string, any>> {
  const completedStepIds = await redis.smembers(`wizard:${tenantId}:completed`);
  const states: Record<string, any> = {};
  
  for (const stepId of completedStepIds) {
    const data = await redis.get(`wizard:${tenantId}:${stepId}`);
    if (data) states[stepId] = JSON.parse(data);
  }
  
  return states;
}
```

## Integration Points

- **Dashboard UI:** Step indicator component and Getting Started checklist
- **Phone Number Service:** Provisioning and verification of numbers
- **Agent Builder (Part 06):** Agent creation step integrates with agent configuration
- **Knowledge Base (Part 13):** Document upload step for RAG setup
- **Integrations (Part 10):** CRM and calendar connection step

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Progress Persistence:** Store wizard state in Redis with a 24-48 hour TTL. After the wizard is completed, clear the state.
- **Analytics Tracking:** Track each step completion, time spent per step, and abandonment point. Use this data to optimize the wizard funnel.
- **Skipped Steps Handling:** Configurations that are skipped should have reasonable defaults applied. The Getting Started checklist in the dashboard should prompt completion.
- **Mobile Responsiveness:** The wizard must work on mobile devices. Use responsive layouts and mobile-optimized form inputs (especially phone number entry with country codes).
- **A/B Testing:** Test different wizard flows: linear vs choose-your-own-adventure, video vs text instructions, number of steps. Measure impact on activation rate.
- **Multi-Language:** Support wizard steps in the tenant's configured language. Use i18n for all step content, validation messages, and help text.
