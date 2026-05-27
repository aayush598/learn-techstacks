# Section 01: Invoice Data Model

## Invoice Schema

The invoice data model captures all financial details of a billing transaction. It must support multiple line items, tax breakdowns, discounts, credits, and various payment states. The schema is designed for both display (customer-facing invoices) and audit (financial records).

```typescript
interface Invoice {
  id: string;
  number: string;                // Human-readable invoice number (e.g., INV-2025-06-001)
  tenantId: string;
  subscriptionId: string;
  stripeInvoiceId?: string;

  // Period
  periodStart: string;
  periodEnd: string;
  issueDate: string;
  dueDate: string;
  paidAt?: string;

  // Financial totals (in cents)
  subtotal: number;
  discountTotal: number;
  taxTotal: number;
  total: number;
  amountPaid: number;
  amountDue: number;
  amountRemaining: number;
  currency: string;

  // Status
  status: InvoiceStatus;
  paymentStatus: PaymentStatus;

  // Line items
  lineItems: InvoiceLineItem[];

  // Tax breakdown
  taxBreakdown: TaxBreakdown[];

  // Discounts
  discounts: InvoiceDiscount[];

  // Metadata
  notes?: string;
  footer?: string;
  customFields?: InvoiceCustomField[];
  metadata: Record<string, string>;

  // Audit
  createdAt: string;
  updatedAt: string;
  voidedAt?: string;
  voidReason?: string;
}

enum InvoiceStatus {
  DRAFT = 'draft',
  OPEN = 'open',             // Issued but not yet paid
  PAID = 'paid',
  UNCOLLECTIBLE = 'uncollectible',
  VOID = 'void',
  DELETED = 'deleted',       // Administrative deletion
}

enum PaymentStatus {
  UNPAID = 'unpaid',
  PAID = 'paid',
  PARTIALLY_PAID = 'partially_paid',
  OVERPAID = 'overpaid',
  REFUNDED = 'refunded',
  PARTIALLY_REFUNDED = 'partially_refunded',
}

interface InvoiceLineItem {
  id: string;
  description: string;
  type: LineItemType;
  quantity: number;
  unitPrice: number;         // Per-unit price in cents
  amount: number;            // Total = quantity × unitPrice
  taxAmount: number;
  discountAmount: number;
  taxRate?: number;
  metadata?: Record<string, string>;
}

enum LineItemType {
  PLAN = 'plan',               // Subscription plan charge
  PRORATION = 'proration',     // Plan change adjustment
  USAGE = 'usage',             // Metered usage overage
  ADDON = 'addon',             // Add-on feature
  CREDIT = 'credit',           // Credit note application
  DISCOUNT = 'discount',       // Coupon or discount
  TAX = 'tax',                 // Tax line item
  FEE = 'fee',                 // Other fee
}
```

## Tax Breakdown

Taxes are broken down by jurisdiction for compliance and reporting. Each line item can have multiple tax jurisdictions applied.

```typescript
interface TaxBreakdown {
  jurisdiction: {
    country: string;
    state?: string;
    county?: string;
    city?: string;
  };
  taxType: 'vat' | 'sales_tax' | 'gst' | 'hst' | 'pst' | 'digital_service';
  taxRate: number;             // As decimal (e.g., 0.0875 for 8.75%)
  taxableAmount: number;
  taxAmount: number;
  taxCode: string;             // Stripe tax code or internal code
  exemptionReference?: string; // Exemption certificate reference
}

interface InvoiceDiscount {
  couponId?: string;
  name: string;
  type: 'percentage' | 'fixed';
  amount: number;              // In cents
  percentage?: number;         // If percentage discount
  description?: string;
}
```

## Credit Notes

Credit notes are negative invoices issued to correct errors, provide refunds, or adjust charges. They follow the same structure as invoices but with negative amounts.

```typescript
interface CreditNote {
  id: string;
  number: string;              // CN-2025-06-001
  invoiceId: string;           // Original invoice
  tenantId: string;
  reason: CreditNoteReason;
  total: number;               // Negative amount in cents
  taxTotal: number;
  lineItems: CreditNoteLineItem[];
  status: 'issued' | 'applied' | 'voided';
  appliedToInvoiceId?: string; // If applied to a specific invoice
  issuedAt: string;
  appliedAt?: string;
}

enum CreditNoteReason {
  DUPLICATE = 'duplicate',
  FRAUDULENT = 'fraudulent',
  ORDER_CHANGE = 'order_change',
  PRODUCT_UNSATISFACTORY = 'product_unsatisfactory',
  SUBSCRIPTION_CHANGE = 'subscription_change',
  OTHER = 'other',
}

interface CreditNoteLineItem {
  originalLineItemId: string;
  amount: number;
  taxAmount: number;
  reason: string;
}
```

## Invoice Status State Machine

Invoices transition through a defined set of states. Understanding the state machine is critical for correct billing logic.

```
Invoice Status Flow:
┌───────┐    generate    ┌───────┐    payment    ┌───────┐
│ Draft │───────────────→│  Open  │──────────────→│  Paid │
└───────┘                └───┬───┘                └───────┘
                            │                         │
                      failed │                    partial
                            ▼                         ▼
                     ┌──────────────┐          ┌──────────────┐
                     │ Uncollectible│          │   Partially  │
                     └──────────────┘          │    Paid      │
                                                └──────┬───────┘
                                                       │
                                                  full payment
                                                       │
                                                       ▼
                                                  ┌──────────┐
                                                  │   Paid   │
                                                  └──────────┘
```

## Open-Source Tools

- **PostgreSQL** — Invoice data storage with JSONB for flexible line items
- **BullMQ** — Schedule invoice generation and delivery jobs
- **pdfmake** (MIT) — PDF generation for invoice documents
- **Stripe API** — Invoice creation, finalization, and payment

## Integration Points

The invoice data model connects to the subscription service (for period and plan data), the usage metering system (for usage-based line items), the tax service (for jurisdiction breakdown), and the payment reconciliation system (for payment status tracking).

## Production Considerations

- Make invoice numbers sequential and gap-free for audit compliance
- Store invoice data redundantly (don't rely solely on Stripe)
- Implement invoice archiving policy (active ↔ archived after 3 years)
- Handle invoice data migration carefully (schema changes are difficult)
- Ensure timezone consistency for invoice dates

## Open-Source First Philosophy

The invoice data model is stored in PostgreSQL with JSONB for flexible line item storage, avoiding proprietary invoice management systems. pdfmake generates PDF invoices locally without external API calls. This open-source approach eliminates recurring costs for document generation and storage while maintaining complete data ownership.
