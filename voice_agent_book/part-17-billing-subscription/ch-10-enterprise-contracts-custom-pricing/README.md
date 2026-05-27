# Chapter 10: Enterprise Contracts & Custom Pricing

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Custom Pricing Data Model](sec-01-custom-pricing-data-model.md) | Custom price definitions, overrideable plan prices, volume discounts, committed usage discounts |
| 02 | [Contract Term Management](sec-02-contract-term-management.md) | Annual/ multi-year contracts, contract start/end dates, auto-renewal, early termination fees |
| 03 | [Minimum Commitment (MTD)](sec-03-minimum-commitment-mtd.md) | Monthly minimum spend, true-up at period end, shortfall billing, commitment tracking |
| 04 | [Custom Invoice Workflow](sec-04-custom-invoice-workflow.md) | Manual invoice generation, PO number requirements, Net-30/60 terms, custom invoice fields |
| 05 | [Enterprise Approval Flows](sec-05-enterprise-approval-flows.md) | Quote generation, internal approval routing, discount approval limits, contract signing |
| 06 | [Contract Renewal Automation](sec-06-contract-renewal-automation.md) | Renewal notification, price escalation calculation, renewal negotiation tracking, automated renewal |
| 07 | [Usage Audits for Enterprise](sec-07-usage-audits-enterprise.md) | Usage verification reports, overage vs commitment reconciliation, audit certificate generation |
| 08 | [Enterprise Sales Portal](sec-08-enterprise-sales-portal.md) | Quote generation tool, contract library, customer health dashboard, renewal pipeline view |

---

## Custom Pricing Override Model

```json
{
  "tenant_id": "enterprise_tenant",
  "contract_id": "cont_abc_123",
  "plan_override": {
    "base_plan": "enterprise",
    "price_monthly": 500000,
    "price_annual": 5000000,
    "currency": "usd",
    "commitment": {
      "type": "monthly_minimum",
      "amount": 400000,
      "true_up": "quarterly"
    },
    "discounts": [
      { "type": "volume", "threshold": 100000, "rate": 0.15 },
      { "type": "term", "years": 2, "rate": 0.10 }
    ],
    "features": [
      { "id": "premium_support", "enabled": true },
      { "id": "dedicated_infrastructure", "enabled": true },
      { "id": "custom_sla", "value": "99.99%" }
    ]
  },
  "term": {
    "start": "2025-01-01",
    "end": "2025-12-31",
    "auto_renew": true,
    "renewal_notice_days": 90
  }
}
```

---

## Learning Objectives

- Design custom pricing data model with overrides
- Manage contract terms with auto-renewal and termination
- Implement minimum commitment tracking with true-up
- Build custom invoice workflow with PO numbers
- Create enterprise approval flows for quotes and discounts
- Automate contract renewal with escalation
- Build usage audit reports for enterprise customers
- Develop enterprise sales portal with quote generation
