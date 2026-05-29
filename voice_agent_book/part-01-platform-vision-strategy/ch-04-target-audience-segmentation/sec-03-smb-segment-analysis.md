# Section 03: SMB Segment Analysis

## SMB Market Overview

Small and medium businesses (1-50 employees) represent the largest addressable market by count but smallest by individual deal size. However, the aggregate opportunity is significant, and SMBs are underserved by current voice AI platforms.

```
SMB Market Segmentation
┌─────────────────────────────────────────────────────────────────────┐
│ Sub-Segment    │ Employee │ Revenue     │ Voice AI Spend │ Units    │
├─────────────────────────────────────────────────────────────────────┤
│ Micro-biz      │ 1-5      │ <$500K      │ $0-50/mo       │ 5M       │
│ Small business │ 5-20     │ $500K-$5M   │ $50-200/mo     │ 2M       │
│ Medium-small   │ 20-50    │ $5M-$20M    │ $200-500/mo    │ 500K     │
└─────────────────────────────────────────────────────────────────────┘
```

## SMB Voice AI Needs Assessment

### Common Pain Points
**Pain 1: Missed calls = lost revenue.** SMBs miss 15-25% of calls. Each missed call = $15-50 lost revenue. For a dental practice missing 40 calls/week: $31K-$104K/year lost.

**Pain 2: Staff hate phone duty.** Front desk staff spend 30-40% of time on phone. High turnover in reception roles. Cost of hiring/training receptionist: $5-8K.

**Pain 3: Inconsistent phone etiquette.** No script adherence. Different staff members handle calls differently. Customer experience varies widely.

**Pain 4: No after-hours coverage.** 23% of calls come outside business hours. Most SMBs simply don't answer. Competitors with 24/7 service win those customers.

## SMB Buyer Persona Deep Dive

**Name:** Sarah (from sec-02 persona). **Role:** Owner/operator. **Decision style:** Quick, pragmatic, price-conscious. **Info sources:** Google search, industry groups, Yelp/Google reviews, word of mouth. **Buying window:** 1-3 weeks from awareness to purchase. **Budget:** $50-200/month. **Deal breaker:** Must work immediately, no long implementation.

## SMB Pricing Sensitivity

```
Pricing Sensitivity by SMB Sub-Segment
┌───────────────────────────────────────────────────────────────────────┐
│ Monthly Price │ Micro-Biz   │ Small Biz    │ Med-Small    │           │
├───────────────────────────────────────────────────────────────────────┤
│ $0 (Free)     │ Very likely │ Somewhat     │ Unlikely     │           │
│ $29           │ Likely      │ Very likely  │ Somewhat     │           │
│ $49           │ Somewhat    │ Likely       │ Likely       │           │
│ $99           │ Unlikely    │ Somewhat     │ Likely       │           │
│ $199          │ Very unlike │ Unlikely     │ Somewhat     │           │
│ $499          │ No          │ Very unlike  │ Unlikely     │           │
└───────────────────────────────────────────────────────────────────────┘
```

## SMB Segment Data Model

```typescript
interface SMBSegment {
  subSegment: 'micro' | 'small' | 'med-small';
  employeeRange: [number, number];
  revenueRange: [number, number];
  monthlyCallVolume: number;
  currentPhoneSetup: 'cell' | 'basic_ivr' | 'pbx' | 'voip';
  techStack: string[];
  voiceAIReadiness: 1 | 2 | 3 | 4 | 5;
  priceSensitivity: 'high' | 'medium' | 'low';
  churnRisk: 'high' | 'medium' | 'low';
  
  // Marketing channels that work
  effectiveChannels: ('google' | 'facebook' | 'referral' | 'local_events' | 'industry_assoc')[];
}

function scoreSMBActivation(smb: SMBSegment): ActivationScore {
  const callVolumeScore = Math.min(smb.monthlyCallVolume / 100, 10);
  const techReadinessScore = smb.voiceAIReadiness * 2;
  const painScore = smb.currentPhoneSetup === 'cell' ? 10 : 
                    smb.currentPhoneSetup === 'basic_ivr' ? 7 : 
                    smb.currentPhoneSetup === 'pbx' ? 4 : 3;
  
  return {
    total: (callVolumeScore + techReadinessScore + painScore) / 3,
    callVolume: callVolumeScore,
    techReadiness: techReadinessScore,
    painLevel: painScore,
    recommendedPlan: callVolumeScore > 7 ? 'Starter' : 'Free',
  };
}
```

## SMB Acquisition Channels

**Channel 1: Google Ads (Highest converting).** Keywords: "AI phone system", "virtual receptionist", "auto attendant for small business", "AI answer phone". Avg CPC: $3-8. Conversion rate: 5-8%.

**Channel 2: Local SEO.** Optimize for "[city] + voice AI", "[industry] + phone system". Google Business Profile optimization. Local backlinks from business associations.

**Channel 3: Partnerships.** Chamber of commerce, industry associations (ADA for dentists, NAR for real estate), franchise networks.

**Channel 4: Content.** "How to automate your small business phone" guides, ROI calculators, comparison pages.

## SMB Retention & Expansion

**Churn drivers:** Price sensitivity (36%), insufficient call volume (22%), feature gaps (18%), poor reliability (14%), other (10%).

**Retention strategies:**
- **Onboarding call:** 15-minute setup call with each new SMB customer (included)
- **Monthly usage report:** "You handled X calls, saved $Y, missed Z less calls"
- **Seasonal check-in:** "Busy season coming? Here's how to prepare"
- **Feature discovery:** Monthly email highlighting one feature they haven't tried
- **Loyalty pricing:** 10% discount after 12 continuous months

## SMB Competitive Positioning

| Feature | Us | Bland AI | Vapi | Dialpad | 
|---------|-----|-----------|------|---------|
| Free tier | 100 min | 30 min | 5 min | None |
| SMB pricing | $49/mo | $29/mo | Pay-as-you-go | $23/user/mo |
| Ease of setup | Very easy | Easy | Moderate | Moderate |
| No-code builder | ✅ | ✅ | ❌ | ✅ |
| Industry templates | ✅ | ✅ | ❌ | ❌ |
| 24/7 support | Email | Chatbot | Email | Phone |
| Minutes included | 1,000 | 2,000 | None | Unlimited (per user) |

## SMB Case Studies (Projected)

**Case: Dental Practice (Dr. Smith, 3 locations).** Before: Missed 35 calls/day, 1 receptionist overwhelmed ($38K/yr). After: AI handles scheduling, follow-ups, insurance verification. Results: 0 missed calls, 40% increase in booked appointments, $28K saved annually.

**Case: Real Estate Agency (Acme Realty, 12 agents).** Before: Admin team spends 60% of time qualifying leads. After: AI qualifies leads 24/7, books tours automatically. Results: 3x more qualified leads, 50% faster tour booking.

## Tools & Resources

- **SMB directories:** Yelp, Google Business, Nextdoor
- **SMB advertising:** Google Ads, Facebook Ads, Nextdoor Ads
- **SMB analytics:** PostHog (track SMB-specific funnel)
- **SMB support:** Intercom, Crisp, Tidio (chat + knowledge base)
- **SMB onboarding:** Userflow, Appcues (guided tours)
- **SMB email automation:** Loops, Resend, Mailchimp
