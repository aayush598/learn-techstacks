# Chapter 06: Credit System & Prepaid Billing

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Credit Balance Model](sec-01-credit-balance-model.md) | Credit ledger design, balance per tenant, pending vs settled credits, concurrent balance updates |
| 02 | [Credit Purchase Flow](sec-02-credit-purchase-flow.md) | Credit pack purchase, Stripe payment intent, immediate credit issuance, receipt generation |
| 03 | [Credit Consumption Tracking](sec-03-credit-consumption-tracking.md) | Usage deduction from balance, insufficient credit handling, partial consumption, refund scenarios |
| 04 | [Tiered Credit Packs](sec-04-tiered-credit-packs.md) | Volume discount tiers, credit pack pricing, bundle options (minutes + features), promotional packs |
| 05 | [Credit Expiry & Rollover](sec-05-credit-expiry-rollover.md) | Credit expiration policies, rollover to next period, use-it-or-lose-it vs rollover, automatic consumption order |
| 06 | [Promotional Credits](sec-06-promotional-credits.md) | Promo credit creation, campaign attribution, expiry configuration, usage restrictions |
| 07 | [Credit Refund Handling](sec-07-credit-refund-handling.md) | Refund scenarios, unused credit refund, partial refund, refund to original payment method |
| 08 | [Prepaid vs Postpaid Hybrid](sec-08-prepaid-postpaid-hybrid.md) | Prepaid balance first, then postpaid billing, hybrid consumption order, invoice integration |

---

## Credit Ledger

```
Transaction ID | Tenant   | Type        | Amount | Balance | Description
───────────────┼──────────┼─────────────┼────────┼─────────┼───────────────────
CR-001         | tenant_1 | purchase    | +5000  | 5000    | 5K Minutes Pack
CR-002         | tenant_1 | consumption | -150   | 4850    | Outbound Call
CR-003         | tenant_1 | consumption | -60    | 4790    | STT Processing
CR-004         | tenant_1 | promo       | +1000  | 5790    | Welcome Bonus
CR-005         | tenant_1 | expiry      | -500   | 5290    | Monthly expiry
```

---

## Learning Objectives

- Design credit ledger with concurrent-safe balance updates
- Implement credit purchase flow with immediate issuance
- Build credit consumption tracking with insufficient balance handling
- Create tiered credit packs with volume discounts
- Implement credit expiry and rollover policies
- Build promotional credit system with campaign tracking
- Handle credit refunds with payment method reconciliation
- Design prepaid/postpaid hybrid billing model
