# User Onboarding Checklist

## Overview

The onboarding checklist guides new users through essential setup tasks after first login. Progress is tracked per-user, with optional completion requirements before accessing certain features.

## Checklist Definition

```typescript
interface OnboardingChecklist {
  id: string;
  tenantId: string;
  name: string;
  steps: OnboardingStep[];
  isDefault: boolean;
  requiredForAccess: boolean;     // Must complete before using platform
  applicableRoles: string[];      // Which roles see this checklist
}

interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  action: string;                 // Route or API call to verify completion
  type: 'setup' | 'learn' | 'configure' | 'verify';
  optional: boolean;
  order: number;
  estimatedMinutes: number;
  dependsOn?: string[];           // Step IDs that must be completed first
}
```

## Progress Tracking

```typescript
interface UserOnboardingProgress {
  userId: string;
  checklistId: string;
  completedSteps: string[];
  startedAt: Date;
  completedAt?: Date;
  skippedSteps: string[];
}

class OnboardingService {
  async getChecklist(userId: string): Promise<OnboardingChecklist> {
    const user = await this.userService.getUser(userId);
    const checklists = await this.db.find('onboarding_checklists', {
      tenantId: user.tenantId,
      applicableRoles: { $in: user.roles },
      isDefault: true,
    });
    return checklists[0];
  }

  async completeStep(userId: string, stepId: string): Promise<void> {
    let progress = await this.db.findOne('onboarding_progress', { userId });

    if (!progress) {
      progress = { userId, completedSteps: [], startedAt: new Date(), skippedSteps: [] };
    }

    if (!progress.completedSteps.includes(stepId)) {
      progress.completedSteps.push(stepId);
    }

    // Check if all required steps completed
    const checklist = await this.getChecklist(userId);
    const requiredSteps = checklist.steps.filter(s => !s.optional);
    const allRequiredComplete = requiredSteps.every(s =>
      progress.completedSteps.includes(s.id)
    );

    if (allRequiredComplete && !progress.completedAt) {
      progress.completedAt = new Date();
    }

    await this.db.upsert('onboarding_progress', { userId }, progress);
  }
}
```

## Sample Steps

```
├── ✅ Connect phone number (5 min)
├── ✅ Configure welcome message (10 min)
├── ⬜ Create first agent (15 min)
├── ⬜ Set up business hours (5 min)
├── ⬜ Invite team members (10 min)
└── ⬜ Complete training module (20 min) [optional]
```

## Open-Source Tools

- **React Joyride** (MIT) — Product tour/onboarding UI
- **Shepherd.js** (MIT) — Guided tour library

## Production Considerations

- Show progress as percentage in user menu
- Allow admin to customize checklist per role
- Send reminder emails for incomplete checklists (24h, 72h, 7d)
- Support checklist templates per tenant industry
- Track drop-off analytics per step to improve UX
