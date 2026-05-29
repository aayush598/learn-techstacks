# Section 03: Activation & Onboarding Metrics

## Activation Definition

Activation is the moment a new user realizes the core value of our platform. For our product, activation = **first successful AI-driven call completed**. This is the "Aha!" moment where the user hears their AI agent handle a real conversation.

```
Activation Journey
┌─────────────────────────────────────────────────────────────────────────┐
│ Step 1: Sign Up              Step 2: Create Agent                      │
│ ┌─────────────────────┐     ┌─────────────────────┐                   │
│ │ 60 seconds          │     │ 2-3 minutes          │                   │
│ │ Email/Google OAuth   │     │ Name, prompt, voice  │                   │
│ │ Verify email        │     │ Select template      │                   │
│ └─────────────────────┘     └─────────────────────┘                   │
│         │                          │                                   │
│         ▼                          ▼                                   │
│ Step 3: Connect Phone     Step 4: Test Call (CRITICAL)                 │
│ ┌─────────────────────┐     ┌─────────────────────┐                   │
│ │ 1-2 minutes          │     │ 2-5 minutes          │                   │
│ │ Twilio/Telnyx setup   │     │ Make first call      │                   │
│ │ Buy/connect DID      │     │ Hear AI response     │                   │
│ └─────────────────────┘     └─────────────────────┘                   │
│                                      │                                 │
│                                      ▼                                 │
│                              🎉 ACTIVATED!                             │
│                              "It works!"                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Activation Metrics

### Time-to-Value (TTV)
- **Target:** First successful call within 5 minutes of signup
- **Current baseline:** 8.4 minutes
- **Best-in-class:** <3 minutes (simplified onboarding)

### Onboarding Completion Rate
- **Step 1 → 2 (Agent created):** Target >85%
- **Step 2 → 3 (Phone connected):** Target >75%
- **Step 3 → 4 (Test call made):** Target >65%
- **Step 4 → Activated:** Target >60%

### Drop-off Analysis
- **Signup → No agent creation (15%):** Users got distracted, confused, or overwhelmed
- **Agent created → No phone setup (12%):** Users don't have a phone number ready
- **Phone setup → No test call (15%):** Users unsure how to test
- **Test call failed (8%):** Technical issues, poor voice quality, latency

## Onboarding Metrics Data Model

```typescript
interface OnboardingMetrics {
  signups: number;
  activated: number;
  activationRate: number;
  
  stepCompletion: {
    step1: number; // agent created
    step2: number; // phone connected
    step3: number; // test call attempted
    step4: number; // test call succeeded (activated)
  };
  
  timing: {
    medianTimeToStep2: number; // minutes
    medianTimeToStep3: number;
    medianTimeToActivation: number;
    averageStepsDuration: number;
  };
  
  quality: {
    firstCallSuccessRate: number;
    firstCallAvgDuration: number;
    firstCallCsat: number;
    firstCallFcr: number; // first call resolution
  };
  
  blockers: BlockerAnalysis[];
}

interface BlockerAnalysis {
  step: string;
  dropOffRate: number;
  topReasons: string[];
  suggestedFixes: string[];
}

function analyzeOnboardingFunnel(metrics: OnboardingMetrics): FunnelInsights {
  const biggestDropoff = metrics.blockers.reduce(
    (max, b) => b.dropOffRate > max.dropOffRate ? b : max
  );
  
  return {
    overallActivationRate: metrics.activated / metrics.signups,
    bottleneck: {
      step: biggestDropoff.step,
      rate: biggestDropoff.dropOffRate,
      reasons: biggestDropoff.topReasons,
    },
    improvement: estimateImprovementFromFix(biggestDropoff),
  };
}
```

## Onboarding Optimization Strategies

### Strategy 1: Pre-Built Templates
Use industry-specific templates so users don't start from scratch. "Dental Office Scheduling" template pre-fills prompt, voice, and settings.

### Strategy 2: Phone Number Provisioning
Pre-purchase phone numbers and assign on signup. Eliminate the "buy a phone number" step. User gets temporary number immediately.

### Strategy 3: Guided Test Call
Auto-initiate a test call after setup. "We're calling you right now — answer to hear your agent in action!" Reduces friction of dialing.

### Strategy 4: Progress Tracking
Visual step progress bar with clear next action. "Step 3 of 4: Configure your agent" with estimated time remaining.

## Activation Email Sequence

| Email | Timing | Content | Goal |
|-------|--------|---------|------|
| Welcome | Immediate | Quickstart guide, video link | Start onboarding |
| First call reminder | 2 hours | "Your agent is waiting" | Push to activation |
| Help | 24 hours | Common issues, support links | Overcome blockers |
| Personalized | 48 hours | "Here's what others in [industry] built" | Inspire and reactivate |
| Win-back | 7 days | Discount offer, case studies | Reactivate cold signups |
| Final | 30 days | Feedback survey, account cleanup | Close the loop |

## Activation Dashboard

```
Activation Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ Activation Rate: 57.2%    TTV (median): 6.8 min    Target: 60% / 5min │
│                                                                         │
│ Funnel (Last 30 Days)                                                   │
│ Signups: 4,892                                                          │
│ ├─ Created Agent: 4,108 (84.0%)                                        │
│ │  └─ Connected Phone: 3,659 (74.8% of signups)                        │
│ │     └─ Test Call Attempted: 3,114 (63.7%)                            │
│ │        └─ Activated: 2,798 (57.2%)                                   │
│                                                                         │
│ Biggest Drop-off: Phone Setup (-9.2%)                                  │
│ Top Reasons: "Don't have a number" (45%), "Confusing setup" (30%)     │
│ Recommended: Pre-provision numbers + one-click connect                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Activation Experiments

| Experiment | Hypothesis | Expected Impact | Status |
|------------|-----------|-----------------|--------|
| Pre-provisioned numbers | +8% activation | Remove biggest blocker | Planned |
| Template-first onboarding | +12% activation | Faster time-to-value | In test |
| Auto test call | +5% activation | Reduce friction | Building |
| Progress bar + estimates | +3% activation | Clarify expectations | Shipped |
| Industry-specific landing | +10% activation | Better targeting | GA |

## Tools & Resources

- **Onboarding analytics:** PostHog (step-by-step funnel), Amplitude
- **Guided tours:** Userflow, Appcues, Chameleon
- **Email automation:** Loops, Resend, Customer.io
- **Session recording:** Hotjar, FullStory, PostHog Recordings
- **Survey (post-onboarding):** Sprig, Userpilot
- **A/B testing:** GrowthBook, LaunchDarkly
