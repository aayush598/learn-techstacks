# Section 04: Custom Invoice Workflow

## Manual Invoice Generation

Enterprise customers often require manually generated invoices with custom fields, PO numbers, and specific billing terms.

```
[Invoice Request]
    ├── Customer requests custom invoice
    └── System or admin triggers generation
    ↓
[Collect Invoice Data]
    ├── Customer details
    ├── Line items (manual or from usage)
    ├── PO number
    ├── Billing address
    └── Tax information
    ↓
[Apply Customizations]
    ├── Custom invoice number format
    ├── Custom fields
    ├── Payment terms (Net-30, Net-60)
    ├── Currency
    └── Tax handling
    ↓
[Generate Invoice]
    ├── Create in Stripe (or direct)
    ├── Generate PDF
    ├── Store in document system
    └── Send to customer
    ↓
[Post-Generation]
    ├── Update invoice status
    ├── Schedule payment reminder
    └── Track in ERP system
```

```typescript
interface CustomInvoiceRequest {
  tenantId: string;
  customerId: string;
  contractId?: string;
  lineItems: CustomInvoiceLineItem[];
  poNumber?: string;
  paymentTerms: PaymentTerm;
  currency: string;
  invoiceDate: string;
  dueDate: string;
  memo?: string;
  customFields: Record<string, string>;
  taxSettings?: TaxSettings;
  deliveryMethod: 'email' | 'portal' | 'edi' | 'manual_download';
  additionalRecipients: string[];
}

interface CustomInvoiceLineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  type: 'usage' | 'subscription' | 'one_time' | 'credit' | 'adjustment';
  reference?: string;            // PO line number, contract reference
  taxCode?: string;
  metadata?: Record<string, string>;
}

type PaymentTerm = 'due_on_receipt' | 'net_15' | 'net_30' | 'net_45' | 'net_60' | 'custom';

interface CustomInvoiceResult {
  id: string;
  invoiceNumber: string;
  pdfUrl: string;
  status: 'draft' | 'open' | 'paid' | 'overdue' | 'cancelled';
  total: number;
  stripeInvoiceId?: string;
}

class CustomInvoiceService {
  async generateCustomInvoice(
    request: CustomInvoiceRequest
  ): Promise<CustomInvoiceResult> {
    // Create invoice in Stripe with custom fields
    const stripeInvoice = await this.createStripeInvoice(request);

    // Generate PDF with custom template
    const pdfUrl = await this.generateInvoicePDF(stripeInvoice, request);

    // Store invoice record
    const invoice: CustomInvoiceResult = {
      id: generateId('inv'),
      invoiceNumber: this.generateInvoiceNumber(request.tenantId),
      pdfUrl,
      status: 'open',
      total: request.lineItems.reduce((s, i) => s + i.amount, 0),
      stripeInvoiceId: stripeInvoice.id,
    };

    await this.storeInvoice(invoice);

    // Deliver invoice
    await this.deliverInvoice(invoice, request);

    return invoice;
  }

  private async createStripeInvoice(
    request: CustomInvoiceRequest
  ): Promise<Stripe.Invoice> {
    // Create invoice items
    for (const item of request.lineItems) {
      await stripe.invoiceItems.create({
        customer: request.customerId,
        amount: Math.round(item.amount * 100), // Convert to cents
        currency: request.currency,
        description: item.description,
        quantity: item.quantity,
        metadata: {
          type: item.type,
          reference: item.reference || '',
          ...item.metadata,
        },
      });
    }

    // Create invoice
    const invoice = await stripe.invoices.create({
      customer: request.customerId,
      collection_method: 'send_invoice',
      days_until_due: this.getDaysUntilDue(request.paymentTerms),
      auto_advance: true,
      metadata: {
        po_number: request.poNumber || '',
        contract_id: request.contractId || '',
        invoice_type: 'custom',
        ...request.customFields,
      },
      custom_fields: Object.entries(request.customFields).map(([name, value]) => ({
        name,
        value,
      })),
    });

    // Finalize invoice
    await stripe.invoices.finalizeInvoice(invoice.id);

    return stripe.invoices.retrieve(invoice.id);
  }

  private async generateInvoicePDF(
    stripeInvoice: Stripe.Invoice,
    request: CustomInvoiceRequest
  ): Promise<string> {
    // Use pdfmake to generate custom invoice PDF
    const docDefinition = {
      content: [
        { text: 'INVOICE', style: 'header' },
        { text: `Invoice #${stripeInvoice.number}`, style: 'subheader' },
        { text: `Date: ${new Date(stripeInvoice.created * 1000).toLocaleDateString()}` },
        { text: `Due Date: ${new Date(stripeInvoice.due_date * 1000).toLocaleDateString()}` },
        { text: `PO Number: ${request.poNumber || 'N/A'}` },
        { text: '\nBill To:', style: 'section' },
        { text: `${stripeInvoice.customer_name}\n${stripeInvoice.customer_address?.line1}\n${stripeInvoice.customer_address?.city}, ${stripeInvoice.customer_address?.state} ${stripeInvoice.customer_address?.postal_code}` },
        { text: '\nLine Items', style: 'section' },
        {
          table: {
            headers: ['Description', 'Qty', 'Unit Price', 'Amount'],
            body: request.lineItems.map(item => [
              item.description,
              item.quantity.toString(),
              `$${item.unitPrice.toFixed(2)}`,
              `$${item.amount.toFixed(2)}`,
            ]),
          },
        },
        { text: `\nTotal: $${(stripeInvoice.total / 100).toFixed(2)}`, style: 'total' },
        { text: `\nPayment Terms: ${request.paymentTerms}` },
        { text: `\n${request.memo || ''}` },
      ],
      styles: {
        header: { fontSize: 24, bold: true },
        subheader: { fontSize: 16, margin: [0, 10, 0, 5] },
        section: { fontSize: 14, bold: true, margin: [0, 10, 0, 5] },
        total: { fontSize: 18, bold: true, margin: [0, 10, 0, 5] },
      },
    };

    // Generate and store PDF
    const pdfBuffer = await pdfmake.createPdf(docDefinition).getBuffer();
    const pdfUrl = await this.storageService.storeFile(
      `invoices/${stripeInvoice.id}.pdf`,
      pdfBuffer,
      'application/pdf'
    );

    return pdfUrl;
  }

  private generateInvoiceNumber(tenantId: string): string {
    const prefix = 'INV';
    const timestamp = Date.now().toString(36).toUpperCase();
    const random = Math.random().toString(36).substring(2, 6).toUpperCase();
    return `${prefix}-${timestamp}-${random}`;
  }

  private getDaysUntilDue(term: PaymentTerm): number {
    switch (term) {
      case 'due_on_receipt': return 0;
      case 'net_15': return 15;
      case 'net_30': return 30;
      case 'net_45': return 45;
      case 'net_60': return 60;
      default: return 30;
    }
  }
}
```

## PO Number Requirements

```typescript
interface PORequirement {
  required: boolean;
  validation?: {
    pattern: string;
    example: string;
    minLength?: number;
    maxLength?: number;
  };
  autoGenerate?: boolean;
  autoGeneratePattern?: string;
}

class POValidationService {
  async validatePO(
    poNumber: string,
    customerId: string
  ): Promise<POValidationResult> {
    const requirement = await this.getPORequirement(customerId);

    if (!requirement.required && !poNumber) {
      return { valid: true };
    }

    if (requirement.required && !poNumber) {
      return { valid: false, error: 'PO number is required' };
    }

    if (requirement.validation) {
      const { pattern, minLength, maxLength } = requirement.validation;
      if (minLength && poNumber.length < minLength) {
        return { valid: false, error: `PO number must be at least ${minLength} characters` };
      }
      if (maxLength && poNumber.length > maxLength) {
        return { valid: false, error: `PO number must be at most ${maxLength} characters` };
      }
      if (pattern && !new RegExp(pattern).test(poNumber)) {
        return { valid: false, error: `PO number must match pattern: ${pattern}` };
      }
    }

    // Check for duplicate PO numbers
    const existing = await this.findInvoiceByPONumber(poNumber, customerId);
    if (existing) {
      return { valid: false, error: 'PO number already used for another invoice' };
    }

    return { valid: true };
  }
}
```

## Net-30/60 Terms

```typescript
interface PaymentTermConfig {
  term: PaymentTerm;
  dueDays: number;
  discount?: {
    percent: number;
    days: number;                // e.g., 2% if paid within 10 days
  };
  lateFee: {
    rate: number;                // Monthly percentage
    graceDays: number;
    maxFee: number;
  };
}

const PAYMENT_TERMS: Record<PaymentTerm, PaymentTermConfig> = {
  due_on_receipt: {
    term: 'due_on_receipt',
    dueDays: 0,
    lateFee: { rate: 0.015, graceDays: 0, maxFee: 100 },
  },
  net_30: {
    term: 'net_30',
    dueDays: 30,
    discount: { percent: 2, days: 10 },
    lateFee: { rate: 0.015, graceDays: 5, maxFee: 50 },
  },
  net_60: {
    term: 'net_60',
    dueDays: 60,
    discount: { percent: 2, days: 15 },
    lateFee: { rate: 0.015, graceDays: 5, maxFee: 100 },
  },
};

class PaymentTermService {
  calculateDueDate(term: PaymentTerm, invoiceDate: string): string {
    const config = PAYMENT_TERMS[term];
    const date = new Date(invoiceDate);
    date.setDate(date.getDate() + config.dueDays);
    return date.toISOString();
  }

  calculateLateFee(invoice: Invoice, currentDate: string): number {
    const config = PAYMENT_TERMS[invoice.paymentTerms];
    const dueDate = new Date(invoice.dueDate);
    const now = new Date(currentDate);

    const daysOverdue = Math.floor((now.getTime() - dueDate.getTime()) / (1000 * 60 * 60 * 24));
    if (daysOverdue <= config.lateFee.graceDays) return 0;

    const monthsOverdue = Math.ceil(daysOverdue / 30);
    const fee = Math.min(
      invoice.total * config.lateFee.rate * monthsOverdue,
      config.lateFee.maxFee
    );

    return Math.round(fee * 100) / 100;
  }
}
```

## Open-Source Tools

- **Stripe** — Invoice object and payment processing
- **pdfmake** (MIT) — Custom invoice PDF generation
- **BullMQ** — Invoice delivery and reminder scheduling
- **PostgreSQL** — Invoice records and tracking
- **MinIO** (AGPL v3) — Invoice PDF storage
- **Nodemailer** (MIT) — Invoice email delivery
- **Handlebars** (MIT) — Invoice email templates

## Integration Points

Custom invoice workflow integrates with the contract system (invoice terms), usage metering (line items), tax engine (tax calculation), document storage (PDF archival), and payment gateway (payment collection).

## Production Considerations

- Support bulk invoice generation for enterprise customers
- Implement invoice number uniqueness across tenant
- Validate PO numbers against customer requirements
- Track invoice delivery status (sent, viewed, downloaded)
- Support invoice memos and custom fields
- Handle invoice corrections and credit notes
- Implement late fee calculation and application
- Provide invoice portal for self-service download

## Open-Source First Philosophy

pdfmake generates professional custom invoice PDFs with full layout control. MinIO stores invoice PDFs with configurable retention policies. Nodemailer handles delivery through any SMTP provider. BullMQ schedules payment reminders and late fee processing. This open-source stack replaces proprietary billing platforms while providing complete control over invoice presentation and delivery workflows.
