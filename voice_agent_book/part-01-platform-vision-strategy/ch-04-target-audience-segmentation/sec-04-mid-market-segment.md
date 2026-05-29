# Section 04: Mid-Market Segment

## Mid-Market Overview

Mid-market companies (50-500 employees, $20M-$500M revenue) are our primary ICP. They have the call volume, budget, and complexity to justify a sophisticated voice AI platform but lack the internal resources to build custom solutions.

```
Mid-Market by Vertical
┌────────────────────────────────────────────────────────────────────────┐
│ Vertical         │ 50-150 emp  │ 150-300 emp │ 300-500 emp │ Total    │
├────────────────────────────────────────────────────────────────────────┤
│ Healthcare       │ 2,400       │ 1,200       │ 400         │ 4,000    │
│ Financial Svcs   │ 1,800       │ 900         │ 300         │ 3,000    │
│ E-commerce       │ 3,200       │ 1,100       │ 200         │ 4,500    │
│ Real Estate      │ 1,500       │ 600         │ 200         │ 2,300    │
│ Insurance        │ 1,200       │ 800         │ 300         │ 2,300    │
│ Travel/Hospital  │ 900         │ 400         │ 100         │ 1,400    │
│ Total            │ 11,000      │ 5,000       │ 1,500       │ 17,500   │
└────────────────────────────────────────────────────────────────────────┘
```

## Mid-Market Needs Assessment

Mid-market companies face a unique challenge: they have outgrown basic IVR and SMB tools but cannot afford enterprise platforms like Retell AI (min $5K/mo) or Twilio Flex (complex, requires implementation partners).

### Primary Needs
**Need 1: Integration with existing tech stack.** They have Salesforce/HubSpot, a WFO platform (Calabrio, Verint), possibly an existing telephony system. The platform must integrate. **Solution:** Native CRM integrations, no-code integration builder.

**Need 2: Compliance ready.** Many have SOC 2 requirements from their own customers. Healthcare mid-market needs HIPAA. **Solution:** SOC 2 Type II, HIPAA available, compliance dashboard.

**Need 3: Agent augmentation, not replacement.** Human agents aren't going away. Mid-market needs AI + human hybrid model. **Solution:** AI handles Tier 1, warm transfer to humans, agent assist mode.

## Mid-Market Buyer Persona

**Name:** Mark (from persona). **Role:** Contact Center Manager / Director of Customer Experience. **Reports to:** VP of Operations or CCO. **Team:** 5-50 agents. **Budget authority:** Up to $50K annually (above needs VP approval). **Buying process:** Research (2-4 weeks) → Demo (2-3 vendors) → POC (4-8 weeks) → Decision. **Key decision factors:** Integration compatibility, compliance, agent experience, analytics depth.

## Mid-Market Deal Economics

| Deal Component | Typical Value | Notes |
|---------------|--------------|-------|
| Annual contract value | $12K-60K | $1K-5K/month |
| Initial term | 12 months | Annual preferred |
| Implementation | 4-8 weeks | Includes integration setup |
| Pilot size | 5-10 agents | Expand after 30-day success |
| Expansion trigger | 70% usage of pilot | Auto-scaling to full team |
| Implementation fee | $5K-15K | One-time, sometimes waived |
| Training | 2-4 hours | On-site or virtual |

## Mid-Market Sales Process

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Mid-Market Sales Cycle                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ Stage 1:   Research & Education (1-2 weeks)                             │
│            → Content marketing, analyst reports, case studies           │
│ Stage 2:   Discovery Call (Week 2-3)                                    │
│            → Needs assessment, qualification, ROI estimate              │
│ Stage 3:   Product Demo (Week 3-4)                                      │
│            → Tailored to use case, integration walkthrough              │
│ Stage 4:   Technical POC (Week 4-8)                                     │
│            → 5-10 agent pilot, integration testing                     │
│ Stage 5:   Security/Compliance Review (Week 6-8)                        │
│            → SOC 2 report, BAAs (if HIPAA), data processing agreement  │
│ Stage 6:   Contract & Negotiation (Week 8-10)                           │
│            → Pricing, terms, SLA, implementation timeline               │
│ Stage 7:   Onboarding (Week 10-14)                                       │
│            → Integration, agent configuration, team training            │
│ Stage 8:   Go Live & Expansion (Week 14+)                               │
│            → Rollout, optimization, expansion to more teams             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Mid-Market Product Requirements

```typescript
interface MidMarketRequirements {
  integrations: {
    crm: ('salesforce' | 'hubspot' | 'zoho' | 'dynamics')[];
    workforce: ('calabrio' | 'verint' | 'nice')[];
    telephony: ('twilio' | 'amazon_connect' | 'genesys' | 'five9')[];
    analytics: ('tableau' | 'powerbi' | 'looker')[];
  };
  compliance: {
    certsRequired: ('soc2_type2' | 'hipaa' | 'gdpr')[];
    auditLogLevel: 'basic' | 'advanced' | 'real-time';
    dataResidency: string[];
  };
  admin: {
    rbac: boolean;
    sso: ('saml' | 'oidc' | 'scim')[];
    teams: boolean;
    usageReporting: boolean;
  };
  support: {
    sla: number; // hours
    channels: ('email' | 'chat' | 'phone' | 'dedicated_contact')[];
    onboardingIncluded: boolean;
  };
}
```

## Competitive Position in Mid-Market

| Factor | Us | Retell AI | RingCentral | Aircall |
|--------|-----|-----------|-------------|---------|
| Starting price | $199/mo | $5K/mo | $30/user/mo | $40/user/mo |
| AI-native | ✅ | ✅ | ❌ | ❌ |
| CRM integration | Native | API | Native | Native |
| Agent augmentation | ✅ | ✅ | Basic | Basic |
| Analytics | Advanced | Enterprise | Basic | Basic |
| Ease of setup | <1 day | 1-2 weeks | 1-2 days | 1 day |
| Compliance features | SOC 2 + HIPAA | HIPAA | SOC 2 | SOC 2 |

## Mid-Market Case Studies (Projected)

**Case: Regional Insurance Agency (200 employees, 40 agents).** Before: 15,000 calls/month, 18% call abandonment, CSAT 3.8/5. After: AI handles policy inquiries, billing questions, claims intake. Results: Abandonment down to 4%, CSAT 4.5/5, agent capacity increased 60%.

**Case: E-commerce Retailer ($80M revenue, 15 customer service agents).** Before: Order status calls consume 35% of agent time. After: AI handles 85% of order inquiries. Results: Agents focus on complex issues, resolution time drops 40%.

## Tools & Resources

- **Mid-market CRM:** Salesforce, HubSpot Enterprise
- **Sales engagement:** Outreach, SalesLoft, Gong
- **Lead generation:** ZoomInfo, Clearbit, LinkedIn Sales Navigator
- **POC infrastructure:** Dedicated tenant with guided setup
- **Competitive intelligence:** Klue, Crayon (track mid-market competitor moves)
- **Analyst relations:** Gartner Peer Insights, G2 (mid-market segment)
