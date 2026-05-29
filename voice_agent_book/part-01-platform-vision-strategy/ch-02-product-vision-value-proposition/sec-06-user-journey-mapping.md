# Section 06: User Journey Mapping

## Journey Overview

The user journey spans from initial discovery through mature platform usage. We map six stages with defined actions, emotions, touchpoints, and success metrics for each persona.

```
Full User Journey Funnel
Discovery → Signup → Onboarding → First Call → Growth → Advocacy
    │          │          │           │           │          │
    ▼          ▼          ▼           ▼           ▼          ▼
  Find      Create    Configure   Make 1st   Scale to   Refer,
  Platform  Account  Agent       Call      100/day    Share, Win
```

## Stage 1: Discovery

**User actions:** Search "voice AI agent", "AI phone agent", "automated phone system" on Google. Read comparison blog posts. Visit G2, Capterra. See GitHub project. See Twitter/LinkedIn post.

**Touchpoints:** Google Ads (branded + unbranded), SEO content (comparisons, "best voice AI" posts), GitHub README, social media (Twitter/X, LinkedIn), Hacker News, Product Hunt.

**Emotions:** Curious (What's possible?), skeptical (Will it work?), overwhelmed (Too many options).

**Key metric:** Traffic by source → signup conversion rate.

**Design decisions:** Landing page shows ROI calculator immediately. 60-second demo video. Social proof (customer logos, testimonials). No signup required for docs/GitHub.

## Stage 2: Signup

**User actions:** Click CTA ("Start Free", "Try Free"). Fill form (email, name, company, use case). Verify email. Land in dashboard.

**Touchpoints:** Signup form, email verification, welcome email (Drip 1), in-app onboarding tour.

**Emotions:** Excited (Ready to try), impatient (Wants to see value NOW), cautious (What data do they need?).

**Key metric:** Signup completion rate, email verification rate.

**Design decisions:** Google OAuth for frictionless signup. Minimal form (email + password only). No credit card required. Use case dropdown to personalize onboarding.

## Stage 3: Onboarding

**User actions:** Welcome tour. Connect phone number (Twilio/Telnyx). Configure first agent. Set up knowledge base. Make test call.

**Touchpoints:** In-app wizard, interactive tutorials, knowledge base articles, support chat, onboarding email sequence (Days 1-7).

**Emotions:** Confident (Following the guide), confused (What is SIP trunking?), frustrated (Why isn't it working?), delighted (It works!).

**Key metric:** Time to first call, onboarding completion rate.

## Stage 4: First Call

**User actions:** Receive first live call. Review transcript. Check sentiment analysis. Adjust agent behavior. Make second call.

**Touchpoints:** Dashboard (live call feed), call analytics page, agent builder edit mode, support (if issues).

**Emotions:** Excited (It's real!), surprised (It sounds natural), critical (No, it should handle this differently), proud (My AI agent is live!).

**Key metric:** First call success rate (call completed, no error), first call within 5 minutes of signup (target).

## Stage 5: Growth

**User actions:** Increase call volume. Add more agents. Configure advanced flows. Set up integrations (CRM). Invite team members. Upgrade plan.

**Touchpoints:** Dashboard (usage analytics), billing page, integrations page, team management, success manager (manual outreach).

**Emotions:** Confident (This works), ambitious (Let's scale), analytical (How do we optimize?), concerned (Cost at scale?).

**Key metric:** DAU/MAU, call volume growth, upgrade rate, NPS.

## Stage 6: Advocacy

**User actions:** Leave G2 review. Refer colleagues. Contribute to GitHub. Attend community events. Become case study.

**Touchpoints:** Review request email, referral program page, GitHub issues/PRs, community Discord, case study interview.

**Emotions:** Proud (Part of something), generous (Want to help others succeed), invested (Want platform to improve).

**Key metric:** Referral conversion, NPS promoter score, community contributions.

## User Journey Data Model

```typescript
interface UserJourney {
  userId: string;
  persona: string;
  currentStage: JourneyStage;
  stages: JourneyStageData[];
  conversions: Conversion[];
  timeInProduct: number; // days
}

interface JourneyStageData {
  stage: JourneyStage;
  enteredAt: Date;
  completedAt?: Date;
  steps: JourneyStep[];
  blockers: Blocker[];
  satisfaction: 1 | 2 | 3 | 4 | 5;
}

interface JourneyStep {
  name: string;
  action: string;
  duration: number; // seconds
  success: boolean;
  error?: string;
}

type JourneyStage = 'discovery' | 'signup' | 'onboarding' | 'first_call' | 'growth' | 'advocacy';

function analyzeJourneyFunnel(journeys: UserJourney[]): FunnelAnalysis {
  const stages: JourneyStage[] = ['discovery', 'signup', 'onboarding', 'first_call', 'growth', 'advocacy'];
  const funnel: StageMetrics[] = [];
  
  for (let i = 0; i < stages.length; i++) {
    const entered = journeys.filter(j => j.stages.find(s => s.stage === stages[i]));
    const completed = journeys.filter(j => {
      const stage = j.stages.find(s => s.stage === stages[i]);
      return stage?.completedAt;
    });
    
    funnel.push({
      stage: stages[i],
      enteredCount: entered.length,
      completedCount: completed.length,
      conversionRate: entered.length > 0 ? completed.length / entered.length : 0,
      dropOff: entered.length - completed.length,
    });
  }
  
  return {
    stages: funnel,
    overallConversion: funnel[stages.length - 1]?.completedCount / funnel[0]?.enteredCount || 0,
    biggestDropoff: funnel.reduce((max, curr) => 
      curr.dropOff > max.dropOff ? curr : max
    ),
  };
}
```

## Persona-Specific Journey Variations

| Stage | Sarah (SMB) | Dev | Mark (CC Mgr) | CTO |
|-------|-------------|-----|---------------|-----|
| Discovery | Google search | GitHub/HN | Analyst report | Gartner/peers |
| Signup | Google OAuth | GitHub OAuth | SSO (SAML) | SSO (SAML) |
| Onboarding | Visual wizard | API docs | Integration | Compliance review |
| First Call | Test call via UI | API call | Pilot with 5 agents | Security audit |
| Growth | Upgrade plan | Build custom app | Full deployment | Enterprise eval |
| Advocacy | Tell friends | Contribute code | Case study | Reference call |

## Tools & Resources

- **Journey mapping:** Miro, FigJam, UXPressia
- **Analytics:** PostHog, Amplitude, Mixpanel (track each stage)
- **Session recording:** Hotjar, FullStory, LogRocket
- **Surveys:** Sprig, Userpilot, Chameleon
- **Email automation:** Loops, Resend, Customer.io
- **Feature adoption:** Pendo, Appcues, Userflow
