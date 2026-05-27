# Chapter 03: Stripe Billing Integration

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Stripe Customer Management](sec-01-stripe-customer-management.md) | Customer creation on signup, metadata sync, customer portal, multi-account handling |
| 02 | [Subscription Lifecycle](sec-02-subscription-lifecycle.md) | Create/update/cancel subscription, plan change proration, trial handling, invoice lifecycle |
| 03 | [Price & Product Catalog Sync](sec-03-price-product-catalog-sync.md) | Internal plan → Stripe product sync, price ID mapping, tiered pricing, metered prices |
| 04 | [Stripe Webhook Handler](sec-04-stripe-webhook-handler.md) | Webhook endpoint setup, signature verification, event processing, idempotent handling |
| 05 | [Payment Method Management](sec-05-payment-method-management.md) | Card setup via Stripe Elements, payment method updates, default payment method, SEPA/ACH support |
| 06 | [Stripe Tax Integration](sec-06-stripe-tax-integration.md) | Automatic tax calculation, tax code mapping, jurisdiction handling, tax reporting |
| 07 | [Invoice Customization](sec-07-invoice-customization.md) | Invoice branding, custom fields, memo/description, invoice PDF customization, B2B invoice requirements |
| 08 | [Stripe Test Mode Strategy](sec-08-stripe-test-mode-strategy.md) | Test clock usage, test card numbers, webhook simulation, testing billing scenarios |

---

## Subscription Lifecycle

```
[Trial] ──→ [Active] ──→ [Past Due] ──→ [Unpaid] ──→ [Canceled]
   │            │            │
   │            ├──→ [Canceled] (at period end)
   │            └──→ [Canceled Immediately] (refund)
   │
   └──→ [Active] (conversion with payment method)
            │
            ├──→ [Active] (plan upgrade/downgrade)
            └──→ [Incomplete] (requires payment method)
```

---

## Learning Objectives

- Manage Stripe customer lifecycle with metadata sync
- Implement subscription lifecycle with plan change proration
- Sync internal plan catalog to Stripe products and prices
- Build Stripe webhook handler with signature verification
- Manage payment methods with Stripe Elements
- Integrate Stripe Tax for automated calculation
- Customize invoices for B2B branding requirements
- Use Stripe test mode for comprehensive billing testing
