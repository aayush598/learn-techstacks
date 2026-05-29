# Section 08: Customer Persona Deep Dives

## Persona Deep Dive Methodology

Each persona is built from primary research (customer interviews, surveys) and secondary research (market reports, competitor analysis). Personas are living documents updated quarterly as we learn more.

```
Persona Research Sources
┌─────────────────────────────────────────────────────────────────────┐
│ Primary Research (60% of data)                                     │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
│ │ Customer     │ │ Win/Loss     │ │ User Testing │                │
│ │ Interviews   │ │ Analysis     │ │ Sessions     │                │
│ │ (47 total)   │ │ (25 deals)   │ │ (30 sessions)│                │
│ └──────────────┘ └──────────────┘ └──────────────┘                │
├─────────────────────────────────────────────────────────────────────┤
│ Secondary Research (40% of data)                                   │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
│ │ Gartner      │ │ Competitor   │ │ Market       │                │
│ │ Research     │ │ Reviews (G2) │ │ Reports      │                │
│ └──────────────┘ └──────────────┘ └──────────────┘                │
└─────────────────────────────────────────────────────────────────────┘
```

## Persona 1: Sarah — SMB Owner

**Demographics:** Female, 42, owns a dental practice with 2 locations (12 employees). Located in suburban Texas. Revenue: $2.5M. Tech comfort: 6/10 (uses practice management software, QuickBooks, Gmail).

**A Day in Her Life:** Arrives at 7:30 AM. First 30 minutes: returning voicemails from overnight (8-12 messages). Spends 2 hours on phone-related tasks (answering questions, scheduling, insurance verification). Receptionist handles the rest but needs lunch coverage. After-hours calls go to voicemail — 40% don't leave a message.

**Pain Points:** (1) "I hate playing phone tag with patients." (2) "Missed calls mean missed new patient revenue." (3) "Receptionist turnover is killing me — training takes 2 weeks." (4) "Insurance verification calls waste 30 minutes a day."

**Goals:** (1) Never miss a new patient call. (2) Reduce time spent on scheduling. (3) 24/7 coverage without overtime. (4) Professional phone experience that matches her brand.

**Buying Criteria:** (1) Must work out of box (<1 hour setup), (2) $50-100/month max, (3) Must sound natural, (4) Must integrate with her practice management software (Dentrix), (5) Must get positive reviews from peers.

**Decision Process:** (1) Google "AI phone system for dentists" → (2) Compares 3 options on G2 → (3) Signs up for free trial → (4) Tests with 10 calls → (5) Asks in dental Facebook group → (6) Buys on credit card.

**Emotions:** Stressed about time, skeptical about AI quality, hopeful about cost savings, anxious about patient experience.

## Persona 2: Mark — Contact Center Manager

**Demographics:** Male, 38, manages a 45-agent team for a regional insurance company (800 employees). Located in Ohio. Revenue: $350M. Tech comfort: 8/10 (uses Salesforce, Verint WFO, Five9).

**A Day in His Life:** Morning: Reviews yesterday's metrics (abandon rate, ASA, CSAT). Mid-day: Coaching sessions with bottom performers. Afternoon: Capacity planning, schedule optimization. Weekly: Leadership meeting on escalation trends.

**Pain Points:** (1) "35% of my agent's time is spent on simple password resets and balance inquiries." (2) "Hiring and training new agents costs $15K each and takes 6 weeks." (3) "CSAT drops 15% during peak seasons when we can't staff up." (4) "My agents burn out from repetitive calls."

**Goals:** (1) Reduce cost per call by 40%. (2) Improve CSAT from 4.0 to 4.5. (3) Reduce agent handle time by 20%. (4) Handle peak volume without overtime.

**Buying Criteria:** (1) Must integrate with Five9 (current dialer), (2) Must work with Verint QA, (3) SOC 2 compliance, (4) Analytics and reporting for his dashboard, (5) Agent augmentation (not replacement).

**Decision Process:** (1) Gartner report on voice AI → (2) Shortlists 3 vendors → (3) Attends product demos → (4) Runs 4-week POC with 5 agents → (5) Security review with IT → (6) Contracts/legal → (7) Board approval.

**Emotions:** Skeptical (heard AI promises before), pressured (efficiency targets), cautious (agent morale concerns), analytical (needs data).

## Persona 3: Dev — AI/ML Engineer

**Demographics:** Non-binary, 29, engineer at Series B SaaS company (200 employees). Located in San Francisco. Tech comfort: 10/10. Uses VSCode, Python, TypeScript, LangChain.

**A Day in Their Life:** Morning coffee while reviewing GitHub issues. Sprint planning standup. Build integration between LLM agent and internal APIs. Debug streaming audio pipeline. Afternoon: Write docs, review PR. End of day: Experiment with new Whisper model.

**Pain Points:** (1) "Closed APIs are black boxes — I can't figure out why it failed." (2) "Every platform has different pricing and limits." (3) "I want to BYO LLM but platforms force their models." (4) "Latency is unpredictable."

**Goals:** (1) Ship voice features fast (this sprint). (2) Full control over pipeline. (3) Cost transparency and optimization. (4) Good DX (types, docs, playground).

**Buying Criteria:** (1) Open-source (can inspect code), (2) TypeScript SDK with types, (3) Self-hosted option, (4) BYO LLM support, (5) Competitive price/perf.

## Persona Data Model

```typescript
interface Persona {
  id: string;
  name: string;
  role: string;
  demographics: {
    age: number;
    gender: string;
    location: string;
    income: string;
  };
  psychographics: {
    motivations: string[];
    fears: string[];
    values: string[];
    communicationStyle: string;
  };
  dayInLife: {
    morningRoutine: string;
    keyActivities: string[];
    endOfWork: string;
  };
  decisionJourney: {
    trigger: string;
    researchSources: string[];
    evaluationCriteria: string[];
    stakeholders: string[];
    timeline: string;
  };
  relationship: {
    acquisitionChannel: string;
    onboardingNeeds: string[];
    supportChannels: ('chat' | 'email' | 'phone' | 'docs')[];
    expansionTriggers: string[];
    churnRisks: string[];
  };
}
```

## Persona Communication Preferences

| Persona | Channel | Tone | Frequency | Content |
|---------|---------|------|-----------|---------|
| Sarah (SMB) | Email + SMS | Simple, encouraging | Weekly | Tips, results, new templates |
| Mark (CC Mgr) | Email + LinkedIn | Analytical, results | Bi-weekly | Case studies, benchmarks, new features |
| Dev | GitHub + Discord | Technical, honest | Ongoing | Changelogs, RFCs, API updates |
| CTO | Email + Phone | Formal, ROI | Monthly | Security updates, compliance, case studies |
| Agency | Dashboard + Email | Partner-focused | Weekly | Revenue reports, new marketplace items |

## Persona Evolution & Validation

**Update cadence:** Quarterly review based on: customer feedback, usage analytics, win/loss data, market changes. **Validation methods:** Surveys (annual NPS/segmentation survey), behavioral analytics (PostHog cohorts), customer development interviews (2 per persona per quarter), sales feedback (weekly deal review).

## Tools & Resources

- **Persona templates:** Miro, Figma, Notion
- **Interview tools:** User Interviews, Respondent, Calendly
- **Survey tools:** Typeform, SurveyMonkey, Sprig
- **Analytics:** PostHog, Amplitude (segment by persona)
- **CRM segmentation:** HubSpot, Salesforce (persona-based lead scoring)
- **Feedback collection:** Canny, Intercom, ProductBoard
