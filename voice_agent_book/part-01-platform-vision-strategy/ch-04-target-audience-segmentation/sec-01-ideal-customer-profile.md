# Section 01: Ideal Customer Profile (ICP)

## ICP Definition

Our Ideal Customer Profile (ICP) is the customer type most likely to buy, succeed with, and expand on our platform. ICP informs product prioritization, marketing channels, sales targeting, and customer success playbooks.

```
ICP Targeting Framework
                      High Value
                         ▲
            ┌────────────┼────────────┐
            │  Mid-Market│ Enterprise │
            │  Service   │ Contact    │
            │  Businesses│ Centers    │
            │  ⭐ ICP    │            │
            ├────────────┼────────────┤
            │  SMB       │ Developer  │
            │  Local     │ & Agency   │
            │  Businesses│            │
            └────────────┼────────────┘
                         │
                    Low Complexity
        Low Revenue ◄────────────────► High Revenue
```

## ICP Profile: Mid-Market Service Businesses

**Company size:** 50-500 employees. **Revenue:** $5M-$100M annual revenue. **Industry:** B2C service businesses (healthcare, real estate, financial services, e-commerce, hospitality). **Geography:** United States (primary), UK/EU (secondary).

**Characteristics:** (1) High inbound call volume (100+ calls/day), (2) Customer service is core to their business, (3) Currently using human agents or basic IVR, (4) Have a CRM (Salesforce, HubSpot), (5) Tech-savvy enough to adopt AI but no dedicated ML team.

**Pain points:** Missed calls = lost revenue, high agent costs ($35K-$55K/year per agent), inconsistent customer experience, long hold times, inability to scale during peak seasons.

## ICP Qualification Criteria

```typescript
interface ICPProfile {
  firmographic: {
    employeeCount: { min: number; max: number; ideal: number };
    revenueRange: { min: number; max: number; ideal: number };
    industry: string[];
    geography: string[];
  };
  behavioral: {
    monthlyCallVolume: { min: number; ideal: number };
    currentTechStack: string[];
    digitalMaturity: 1 | 2 | 3 | 4 | 5;
    buyingProcess: 'individual' | 'team' | 'executive';
  };
  needs: {
    primaryUseCase: string;
    complianceRequirements: string[];
    integrationNeeded: string[];
    supportLevel: 'self-serve' | 'guided' | 'full-service';
  };
  fitScore: number; // 0-100 composite score
}

function scoreICPLead(lead: LeadCandidate): number {
  let score = 0;
  
  // Firmographic fit (40 points max)
  if (lead.employeeCount >= 50 && lead.employeeCount <= 500) score += 20;
  if (lead.revenue >= 5_000_000 && lead.revenue <= 100_000_000) score += 15;
  if (ICP_INDUSTRIES.includes(lead.industry)) score += 5;
  
  // Behavioral fit (35 points max)
  if (lead.monthlyCallVolume >= 2000) score += 15;
  if (lead.currentTechStack.some(t => CRM_PLATFORMS.includes(t))) score += 10;
  if (lead.digitalMaturity >= 3) score += 10;
  
  // Need fit (25 points max)
  if (lead.primaryUseCase === 'customer_service') score += 10;
  if (lead.complianceRequirements.includes('hipaa') || lead.complianceRequirements.includes('soc2')) score += 8;
  if (lead.integrationNeeded.length > 0) score += 7;
  
  return score;
}
```

## ICP vs. Anti-ICP

**ICP:** Mid-market service businesses with 50-500 employees. These companies have the call volume to justify AI, the budget to pay, and the complexity to value our enterprise features.

**Anti-ICP:** (1) Solopreneurs (too small, high churn, low revenue), (2) Large enterprises with 5000+ employees (too complex, 12+ month sales cycle, need 24-month feature set), (3) Non-English-only markets initially (too early), (4) Government agencies (too slow, procurement complexity).

## ICP by Vertical

| Vertical | ICP Sub-Type | Companies | Key Trigger Event |
|----------|-------------|-----------|-------------------|
| Healthcare | Multi-location clinics | Dental chains, urgent care, specialist groups | Opening new location |
| Real Estate | Regional brokerages | Residential agencies, property managers | High lead volume season |
| E-commerce | Direct-to-consumer brands | Mid-market online retailers | Customer service scaling pain |
| Financial | Regional banks/credit unions | Insurance agencies, mortgage brokers | Compliance audit |
| Travel | Boutique hotel groups | Travel agencies, rental companies | Seasonal volume spikes |

## Consumer Demographics for Voice Agent End-Users

While buyers are business decision-makers, the end-users (callers) also shape ICP. Our voice agents serve: **Age:** 25-65. **Tech comfort:** Moderate (comfortable with automated phone systems). **Preferred resolution speed:** <3 minutes. **Language:** Primarily English (Year 1-2), expanding to Spanish and other languages in Year 3.

## ICP Evolution Over Time

**Year 1:** Narrow ICP — US-based, English-speaking, mid-market service businesses, high call volume. **Year 2:** Expanded ICP — Include EU, agencies, developers. Add vertical-specific offerings. **Year 3:** Broad ICP — Include Enterprise, white-label partners, international markets (APAC).

## ICP Validation Metrics

- % of new signups matching ICP: Target >60%
- Activation rate: ICP vs non-ICP (Target: ICP 2x higher)
- 90-day retention: ICP vs non-ICP (Target: ICP 3x higher)
- Expansion revenue: ICP vs non-ICP (Target: ICP 2x higher)
- NPS: ICP vs non-ICP (Target: ICP +10 points higher)

## Tools & Resources

- **ICP research:** ZoomInfo, Clearbit, LinkedIn Sales Navigator
- **Lead scoring:** HubSpot, Salesforce, Marketo
- **Firmographic data:** Dun & Bradstreet, Crunchbase, Owler
- **Survey tools:** Typeform, SurveyMonkey, User Interviews
- **Analytics:** PostHog (track ICP vs non-ICP metrics)
