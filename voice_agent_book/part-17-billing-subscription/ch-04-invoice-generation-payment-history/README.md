# Chapter 04: Invoice Generation & Payment History

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Invoice Data Model](sec-01-invoice-data-model.md) | Invoice schema, line items, tax breakdown, totals, invoice statuses, credit notes |
| 02 | [Automated Invoice Generation](sec-02-automated-invoice-generation.md) | Invoice generation trigger, period-end processing, proration calculations, consolidated invoices |
| 03 | [Invoice Delivery & PDF Generation](sec-03-invoice-delivery-pdf.md) | PDF generation (Puppeteer/ wkhtmltopdf), email delivery, customer portal access, archival |
| 04 | [Payment Reconciliation](sec-04-payment-reconciliation.md) | Stripe payment intents to invoice matching, payment status tracking, bank reconciliation |
| 05 | [Payment History API](sec-05-payment-history-api.md) | Payment history endpoint, pagination, filtering, transaction types, export endpoints |
| 06 | [Credit Notes & Adjustments](sec-06-credit-notes-adjustments.md) | Credit note creation, application to future invoices, refund processing, adjustment audit trail |
| 07 | [Invoice Tax Breakdown](sec-07-invoice-tax-breakdown.md) | Per-line-item tax, jurisdiction breakdown, tax rate display, exempt status indicators |
| 08 | [Invoice Dispute Handling](sec-08-invoice-dispute-handling.md) | Dispute intake, evidence submission, dispute resolution, chargeback prevention, representment |

---

## Invoice Data Model

```json
{
  "id": "inv_abc123",
  "number": "INV-2025-06-001",
  "tenant_id": "tenant_xyz",
  "customer_id": "cus_stripe_id",
  "status": "paid",
  "currency": "usd",
  "period_start": "2025-06-01T00:00:00Z",
  "period_end": "2025-06-30T23:59:59Z",
  "subtotal": 19900,
  "tax_total": 3980,
  "total": 23880,
  "amount_paid": 23880,
  "amount_due": 0,
  "amount_remaining": 0,
  "line_items": [
    { "description": "Growth Plan - Monthly", "amount": 19900, "quantity": 1 },
    { "description": "Additional Minutes (1,200 over)", "amount": 0, "quantity": 0 }
  ],
  "tax_breakdown": [
    { "jurisdiction": "US-CA", "rate": 0.0875, "amount": 1741.25 },
    { "jurisdiction": "US-NY", "rate": 0.04, "amount": 796 }
  ],
  "paid_at": "2025-07-01T01:00:00Z",
  "pdf_url": "https://invoices.example.com/inv_abc123.pdf"
}
```

---

## Learning Objectives

- Design comprehensive invoice data model with line items
- Implement automated invoice generation at period end
- Build PDF invoice generation and delivery pipeline
- Create payment reconciliation between Stripe and internal records
- Develop payment history API with filtering and export
- Implement credit notes and account adjustments
- Show detailed tax breakdown on invoices
- Handle invoice disputes and chargeback representment
