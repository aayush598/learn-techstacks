# Section 05: Enterprise Approval Flows

## Quote Generation

Enterprise sales require formal quote generation with approval workflows for discounts, custom pricing, and contract terms.

```
[Sales Rep Creates Quote]
    ├── Select customer
    ├── Choose products/plans
    ├── Apply discounts
    └── Set custom terms
    ↓
[Discount > Threshold?]
    ├── Yes → Route for approval
    │   ├── < 10%: Sales manager
    │   ├── 10-25%: Director
    │   └── > 25%: VP / CRO
    └── No → Auto-approved
    ↓
[Approval Request Sent]
    ├── Notification to approver
    ├── Quote details included
    └── Approval/Rejection link
    ↓
[Approved → Generate Quote PDF]
    ├── Official quote document
    ├── Valid until date
    └── Send to customer
```

```typescript
interface Quote {
  id: string;
  quoteNumber: string;
  tenantId: string;
  customerId: string;
  salesRepId: string;
  status: QuoteStatus;
  lineItems: QuoteLineItem[];
  discounts: DiscountApplication[];
  totalBeforeDiscount: number;
  totalAfterDiscount: number;
  currency: string;
  paymentTerms: PaymentTerm;
  validUntil: string;
  approvalStatus: ApprovalStatus;
  approvalChain: ApprovalChain;
  notes: string;
  createdAt: string;
  updatedAt: string;
}

type QuoteStatus = 'draft' | 'pending_approval' | 'approved' | 'rejected' | 'sent' | 'accepted' | 'expired' | 'cancelled';

interface QuoteLineItem {
  productId: string;
  productName: string;
  description: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  billingPeriod: BillingPeriod;
  discountPercent?: number;
  discountAmount?: number;
}

interface DiscountApplication {
  type: 'percentage' | 'fixed_amount' | 'volume' | 'promotional';
  value: number;
  reason: string;
  approvedBy?: string;
  approvedAt?: string;
}

class QuoteService {
  async createQuote(quoteData: Partial<Quote>): Promise<Quote> {
    const quote: Quote = {
      id: generateId('quote'),
      quoteNumber: this.generateQuoteNumber(),
      tenantId: quoteData.tenantId!,
      customerId: quoteData.customerId!,
      salesRepId: quoteData.salesRepId!,
      status: 'draft',
      lineItems: quoteData.lineItems || [],
      discounts: quoteData.discounts || [],
      totalBeforeDiscount: this.calculateTotal(quoteData.lineItems || []),
      totalAfterDiscount: 0,
      currency: quoteData.currency || 'usd',
      paymentTerms: quoteData.paymentTerms || 'net_30',
      validUntil: this.calculateValidUntil(30),
      approvalStatus: 'not_required',
      approvalChain: [],
      notes: quoteData.notes || '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    // Calculate discounts
    quote.totalAfterDiscount = this.applyDiscounts(
      quote.totalBeforeDiscount,
      quote.discounts
    );

    // Determine approval requirements
    quote.approvalChain = await this.determineApprovalChain(quote);
    quote.approvalStatus = quote.approvalChain.length > 0
      ? 'pending'
      : 'not_required';

    await this.storeQuote(quote);

    // Start approval flow if needed
    if (quote.approvalChain.length > 0) {
      await this.startApprovalFlow(quote);
    }

    return quote;
  }

  private async determineApprovalChain(quote: Quote): Promise<ApprovalChain> {
    const totalDiscount = quote.totalBeforeDiscount - quote.totalAfterDiscount;
    const discountPercent = (totalDiscount / quote.totalBeforeDiscount) * 100;

    const chain: ApprovalChain = [];

    if (quote.totalAfterDiscount > 100000) {
      // High-value quote
      chain.push({ level: 1, role: 'sales_manager', required: true });
      chain.push({ level: 2, role: 'director', required: true });
      chain.push({ level: 3, role: 'vp_sales', required: true });
    } else if (discountPercent > 25) {
      chain.push({ level: 1, role: 'sales_manager', required: true });
      chain.push({ level: 2, role: 'director', required: true });
      chain.push({ level: 3, role: 'vp_sales', required: true });
    } else if (discountPercent > 10) {
      chain.push({ level: 1, role: 'sales_manager', required: true });
      chain.push({ level: 2, role: 'director', required: false });
    } else if (discountPercent > 5) {
      chain.push({ level: 1, role: 'sales_manager', required: true });
    }

    return chain;
  }
}
```

## Internal Approval Routing

```typescript
interface ApprovalChain {
  approvals: ApprovalStep[];
}

interface ApprovalStep {
  level: number;
  role: string;
  required: boolean;
  status: 'pending' | 'approved' | 'rejected' | 'skipped';
  approverId?: string;
  approverName?: string;
  approvedAt?: string;
  comments?: string;
}

class ApprovalFlowService {
  async startApprovalFlow(quote: Quote): Promise<void> {
    for (const step of quote.approvalChain) {
      // Create approval task
      await this.createApprovalTask(quote, step);

      // Send notification to approver
      await this.notifyApprover(quote, step);
    }
  }

  async processApproval(
    quoteId: string,
    approverId: string,
    decision: 'approved' | 'rejected',
    comments?: string
  ): Promise<Quote> {
    const quote = await this.getQuote(quoteId);
    const step = quote.approvalChain.find(
      s => s.status === 'pending' && s.role === this.getApproverRole(approverId)
    );

    if (!step) {
      throw new Error('No pending approval step for this approver');
    }

    step.status = decision;
    step.approverId = approverId;
    step.approverName = await this.getUserName(approverId);
    step.approvedAt = new Date().toISOString();
    step.comments = comments;

    if (decision === 'rejected') {
      quote.approvalStatus = 'rejected';
      quote.status = 'rejected';
      await this.notifySalesRep(quote, 'rejected', comments);
    } else {
      // Check if all approvals are complete
      const allApproved = quote.approvalChain.every(
        s => s.status === 'approved' || (s.status === 'pending' && !s.required)
      );

      if (allApproved) {
        quote.approvalStatus = 'approved';
        quote.status = 'approved';
        await this.onQuoteApproved(quote);
      }
    }

    quote.updatedAt = new Date().toISOString();
    await this.updateQuote(quote);

    return quote;
  }

  private async onQuoteApproved(quote: Quote): Promise<void> {
    // Generate official quote PDF
    await this.generateQuotePDF(quote);

    // Send to customer
    await this.sendQuoteToCustomer(quote);

    // Create quote acceptance deadline
    await this.scheduleQuoteExpiry(quote);
  }

  private async notifyApprover(quote: Quote, step: ApprovalStep): Promise<void> {
    await this.notificationService.send({
      userId: step.role,          // Resolved to actual user(s)
      type: 'approval_required',
      title: `Quote ${quote.quoteNumber} requires your approval`,
      body: `Total: $${quote.totalAfterDiscount.toLocaleString()} | Discount: ${this.calculateDiscountPercent(quote)}%`,
      actionUrl: `/admin/quotes/${quote.id}/approve`,
      priority: 'high',
    });
  }
}
```

## Discount Approval Limits

```typescript
interface DiscountApprovalLimit {
  role: string;
  maxDiscountPercent: number;
  maxDiscountAmount: number;
  canOverridePaymentTerms: boolean;
  canModifyContractLength: boolean;
}

const DISCOUNT_LIMITS: DiscountApprovalLimit[] = [
  { role: 'sales_rep', maxDiscountPercent: 5, maxDiscountAmount: 1000, canOverridePaymentTerms: false, canModifyContractLength: false },
  { role: 'sales_manager', maxDiscountPercent: 15, maxDiscountAmount: 10000, canOverridePaymentTerms: true, canModifyContractLength: false },
  { role: 'director', maxDiscountPercent: 25, maxDiscountAmount: 50000, canOverridePaymentTerms: true, canModifyContractLength: true },
  { role: 'vp_sales', maxDiscountPercent: 50, maxDiscountAmount: 200000, canOverridePaymentTerms: true, canModifyContractLength: true },
  { role: 'ceo', maxDiscountPercent: 100, maxDiscountAmount: Infinity, canOverridePaymentTerms: true, canModifyContractLength: true },
];

class DiscountAuthorizationService {
  async authorizeDiscount(
    discountPercent: number,
    discountAmount: number,
    userRole: string,
    quote: Quote
  ): Promise<AuthorizationResult> {
    const limit = DISCOUNT_LIMITS.find(l => l.role === userRole);
    if (!limit) {
      return { authorized: false, reason: 'Role not authorized for discounts' };
    }

    if (discountPercent > limit.maxDiscountPercent) {
      return {
        authorized: false,
        reason: `Discount ${discountPercent}% exceeds max ${limit.maxDiscountPercent}% for ${userRole}`,
        requiresEscalation: true,
        escalateTo: this.getNextRole(userRole),
      };
    }

    if (discountAmount > limit.maxDiscountAmount) {
      return {
        authorized: false,
        reason: `Discount amount $${discountAmount} exceeds max $${limit.maxDiscountAmount} for ${userRole}`,
        requiresEscalation: true,
        escalateTo: this.getNextRole(userRole),
      };
    }

    return {
      authorized: true,
      discountPercent,
      discountAmount,
      authorizedBy: userRole,
    };
  }

  private getNextRole(currentRole: string): string | undefined {
    const roles = ['sales_rep', 'sales_manager', 'director', 'vp_sales', 'ceo'];
    const currentIndex = roles.indexOf(currentRole);
    return currentIndex < roles.length - 1 ? roles[currentIndex + 1] : undefined;
  }
}
```

## Contract Signing

```typescript
interface ContractSigningFlow {
  quoteId: string;
  contractId: string;
  signingMethod: 'electronic' | 'wet_signature' | 'internal';
  status: 'pending' | 'sent' | 'viewed' | 'signed' | 'expired';
  signingProvider?: 'docuseal';
  signingUrl?: string;
  signedAt?: string;
  signatureImageUrl?: string;
}

class ContractSigningService {
  async initiateSigning(
    quote: Quote,
    contract: Contract
  ): Promise<ContractSigningFlow> {
    // Generate contract document from quote
    const contractDoc = await this.generateContractDocument(quote, contract);

    // Create signing request via DocuSeal
    const signingRequest = await this.docuseal.createSubmission({
      template_id: contractDoc.templateId,
      send_email: true,
      signers: [
        {
          email: quote.customerEmail,
          name: quote.customerName,
          role: 'customer',
        },
        {
          email: quote.salesRepEmail,
          name: quote.salesRepName,
          role: 'provider',
        },
      ],
      metadata: {
        quote_id: quote.id,
        contract_id: contract.id,
      },
    });

    const flow: ContractSigningFlow = {
      quoteId: quote.id,
      contractId: contract.id,
      signingMethod: 'electronic',
      status: 'sent',
      signingProvider: 'docuseal',
      signingUrl: signingRequest.url,
    };

    await this.storeSigningFlow(flow);

    return flow;
  }

  async handleSigningWebhook(event: any): Promise<void> {
    if (event.type === 'submission.completed') {
      const { quote_id, contract_id } = event.metadata;

      // Update contract status
      await this.contractService.activateContract(contract_id);

      // Update quote status
      await this.quoteService.updateQuoteStatus(quote_id, 'accepted');

      // Create subscription from accepted quote
      await this.createSubscriptionFromQuote(quote_id);
    }
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Quote and approval state
- **BullMQ** — Approval notification scheduling
- **DocuSeal** (AGPL v3) — Contract e-signing
- **pdfmake** (MIT) — Quote PDF generation
- **Handlebars** (MIT) — Approval email templates
- **Metabase** (Apache 2.0) — Sales pipeline dashboards
- **OpenTelemetry** — Approval flow tracing

## Integration Points

Approval flows integrate with the quote system (approval triggers), contract system (post-approval contract creation), customer portal (quote acceptance), CRM (sales pipeline updates), and notification service (approver alerts).

## Production Considerations

- Support approval delegation and out-of-office handling
- Implement approval escalation on timeout (auto-escalate after 48 hours)
- Track approval cycle time as a sales metric
- Allow quote revision and re-submission after rejection
- Maintain full approval audit trail
- Support partial approvals (conditional approval with modifications)
- Provide mobile-friendly approval interface
- Implement quote versioning for approval history

## Open-Source First Philosophy

PostgreSQL stores the complete approval chain with audit history. BullMQ sends approval reminders and handles escalation timing. DocuSeal provides self-hosted contract signing. pdfmake generates professional quote PDFs. This open-source stack replaces Salesforce CPQ and DocuSign while maintaining full control over the quote-to-cash approval workflow.
