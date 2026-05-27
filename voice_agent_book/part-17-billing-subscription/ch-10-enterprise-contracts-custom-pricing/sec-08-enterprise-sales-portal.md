# Section 08: Enterprise Sales Portal

## Quote Generation Tool

The enterprise sales portal provides a comprehensive tool for generating quotes with custom pricing, discounts, and contract terms.

```
[Sales Portal Dashboard]
    ├── Quote Generation
    ├── Contract Library
    ├── Customer Health
    └── Renewal Pipeline
    ↓
[Create New Quote]
    ├── Select customer
    ├── Choose products/add-ons
    ├── Set quantities
    ├── Apply discounts
    └── Configure terms
    ↓
[Quote Preview]
    ├── Real-time price calculation
    ├── Discount visualizations
    ├── Term comparison
    └── PDF preview
    ↓
[Submit for Approval]
    ├── Auto-routing based on discount
    ├── Approval chain tracking
    └── Notification to approvers
```

```typescript
interface SalesPortalQuoteRequest {
  customerId: string;
  salesRepId: string;
  products: QuoteProductSelection[];
  discounts: DiscountApplication[];
  paymentTerms: PaymentTerm;
  contractLength: number;        // Months
  startDate: string;
  notes: string;
}

interface QuoteProductSelection {
  productId: string;
  productName: string;
  quantity: number;
  unitPrice: number;
  billingPeriod: BillingPeriod;
  features: string[];
}

interface QuotePreview {
  lineItems: QuotePreviewLine[];
  subtotal: number;
  discountTotal: number;
  total: number;
  monthlyEquivalent: number;
  termSavings: number;            // Savings vs month-to-month
  priceValidityDate: string;
}

class SalesPortalQuoteEngine {
  async previewQuote(request: SalesPortalQuoteRequest): Promise<QuotePreview> {
    const lineItems: QuotePreviewLine[] = [];

    for (const product of request.products) {
      // Check for customer-specific pricing
      const effectivePrice = await this.priceResolver.resolvePrice(
        request.customerId,
        product.productId,
        product.quantity
      );

      const lineTotal = effectivePrice * product.quantity;
      const monthlyTotal = request.contractLength >= 12
        ? (lineTotal / request.contractLength)
        : lineTotal;

      lineItems.push({
        productId: product.productId,
        productName: product.productName,
        quantity: product.quantity,
        unitPrice: effectivePrice,
        lineTotal,
        monthlyEquivalent: monthlyTotal,
        discountApplied: product.unitPrice - effectivePrice,
      });
    }

    const subtotal = lineItems.reduce((s, i) => s + i.lineTotal, 0);

    // Apply additional discounts
    let discountTotal = 0;
    for (const discount of request.discounts) {
      if (discount.type === 'percentage') {
        discountTotal += subtotal * (discount.value / 100);
      } else if (discount.type === 'fixed_amount') {
        discountTotal += discount.value;
      }
    }

    // Calculate term savings
    const monthlyTotal = lineItems.reduce((s, i) => s + i.monthlyEquivalent, 0);
    const termSavings = request.contractLength >= 12
      ? (monthlyTotal * request.contractLength) * 0.1 // 10% annual discount
      : 0;

    return {
      lineItems,
      subtotal,
      discountTotal,
      total: subtotal - discountTotal - termSavings,
      monthlyEquivalent: (subtotal - discountTotal - termSavings) / request.contractLength,
      termSavings,
      priceValidityDate: this.addDays(new Date(), 30).toISOString(),
    };
  }

  async generateQuote(request: SalesPortalQuoteRequest): Promise<Quote> {
    const preview = await this.previewQuote(request);

    const quote: Quote = {
      id: generateId('quote'),
      quoteNumber: this.generateQuoteNumber(),
      tenantId: request.customerId,
      customerId: request.customerId,
      salesRepId: request.salesRepId,
      status: 'draft',
      lineItems: request.products.map(p => ({
        productId: p.productId,
        productName: p.productName,
        description: `${p.productName} x${p.quantity}`,
        quantity: p.quantity,
        unitPrice: p.unitPrice,
        totalPrice: p.unitPrice * p.quantity,
        billingPeriod: p.billingPeriod,
      })),
      discounts: request.discounts,
      totalBeforeDiscount: preview.subtotal,
      totalAfterDiscount: preview.total,
      currency: 'usd',
      paymentTerms: request.paymentTerms,
      validUntil: preview.priceValidityDate,
      approvalStatus: 'not_required',
      approvalChain: [],
      notes: request.notes,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    return this.quoteService.createQuote(quote);
  }
}
```

## Contract Library

The contract library provides searchable access to all enterprise contracts with version history.

```typescript
interface ContractLibraryEntry {
  contractId: string;
  customerName: string;
  contractNumber: string;
  type: 'standard' | 'custom' | 'amendment';
  status: ContractStatus;
  startDate: string;
  endDate: string;
  value: number;
  currency: string;
  accountManager: string;
  documents: ContractDocument[];
  amendments: ContractAmendment[];
  version: number;
}

interface ContractDocument {
  id: string;
  type: 'contract' | 'amendment' | 'sow' | 'addendum';
  title: string;
  url: string;
  uploadedAt: string;
  uploadedBy: string;
  signedAt?: string;
  version: number;
}

class ContractLibraryService {
  async searchContracts(query: ContractSearchQuery): Promise<ContractLibraryEntry[]> {
    const sql = this.buildSearchQuery(query);
    const results = await this.db.query(sql, query.parameters);

    return results.rows.map(this.mapToEntry);
  }

  private buildSearchQuery(query: ContractSearchQuery): string {
    const conditions: string[] = ['1=1'];

    if (query.customerName) {
      conditions.push(`customer_name ILIKE '%' || $1 || '%'`);
    }
    if (query.status) {
      conditions.push(`status = $2`);
    }
    if (query.dateRange) {
      conditions.push(`(start_date >= $3 AND end_date <= $4)`);
    }
    if (query.accountManager) {
      conditions.push(`account_manager_id = $5`);
    }
    if (query.minValue) {
      conditions.push(`total_value >= $6`);
    }

    return `
      SELECT c.*, array_agg(d.*) as documents
      FROM contracts c
      LEFT JOIN contract_documents d ON d.contract_id = c.id
      WHERE ${conditions.join(' AND ')}
      GROUP BY c.id
      ORDER BY c.end_date ASC
    `;
  }

  async getContractTimeline(contractId: string): Promise<ContractTimelineEvent[]> {
    const contract = await this.getContract(contractId);
    const events: ContractTimelineEvent[] = [];

    events.push({ date: contract.createdAt, type: 'created', description: 'Contract created' });
    events.push({ date: contract.signedAt, type: 'signed', description: 'Contract signed' });
    events.push({ date: contract.term.startDate, type: 'activated', description: 'Contract activated' });

    // Add amendment events
    for (const amendment of contract.amendments) {
      events.push({
        date: amendment.effectiveDate,
        type: 'amended',
        description: `Amendment: ${amendment.description}`,
      });
    }

    // Add status change events
    for (const statusChange of contract.statusHistory) {
      events.push({
        date: statusChange.changedAt,
        type: 'status_change',
        description: `Status changed to ${statusChange.newStatus}`,
      });
    }

    return events.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
  }
}
```

## Customer Health Dashboard

Real-time dashboard showing customer health metrics, usage trends, and risk indicators.

```typescript
interface CustomerHealthScore {
  customerId: string;
  customerName: string;
  overallScore: number;           // 0-100
  metrics: {
    usageTrend: number;           // Positive = growing
    paymentReliability: number;   // 0-100
    supportTickets: number;       // Open tickets
    npsScore?: number;
    contractCompliance: number;   // 0-100
    daysSinceLastLogin: number;
  };
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  alerts: CustomerAlert[];
  lastUpdated: string;
}

interface CustomerAlert {
  type: 'usage_drop' | 'payment_failure' | 'support_spike' | 'login_decline' | 'contract_expiring';
  severity: 'info' | 'warning' | 'critical';
  message: string;
  timestamp: string;
  actionUrl?: string;
}

class CustomerHealthCalculator {
  async calculateHealthScore(customerId: string): Promise<CustomerHealthScore> {
    const [usage, payments, support, contract] = await Promise.all([
      this.getUsageTrend(customerId),
      this.getPaymentHistory(customerId),
      this.getSupportMetrics(customerId),
      this.getContractInfo(customerId),
    ]);

    // Calculate individual scores (0-100)
    const usageScore = this.scoreUsageTrend(usage);
    const paymentScore = this.scorePaymentReliability(payments);
    const supportScore = this.scoreSupportActivity(support);
    const contractScore = this.scoreContractHealth(contract);

    // Weighted overall score
    const overallScore = Math.round(
      usageScore * 0.30 +
      paymentScore * 0.35 +
      supportScore * 0.15 +
      contractScore * 0.20
    );

    // Determine risk level
    const riskLevel = this.determineRiskLevel(overallScore, {
      daysSinceLastLogin: usage.daysSinceLastLogin,
      paymentFailures: payments.recentFailures,
      openTickets: support.openTickets,
      contractEnding: contract.daysUntilEnd < 90,
    });

    // Generate alerts
    const alerts = this.generateAlerts(customerId, {
      usage,
      payments,
      support,
      contract,
    });

    return {
      customerId,
      customerName: customer.name,
      overallScore,
      metrics: {
        usageTrend: usage.monthOverMonthChange,
        paymentReliability: paymentScore,
        supportTickets: support.openTickets,
        contractCompliance: contractScore,
        daysSinceLastLogin: usage.daysSinceLastLogin,
      },
      riskLevel,
      alerts,
      lastUpdated: new Date().toISOString(),
    };
  }

  private determineRiskLevel(
    score: number,
    factors: {
      daysSinceLastLogin: number;
      paymentFailures: number;
      openTickets: number;
      contractEnding: boolean;
    }
  ): 'low' | 'medium' | 'high' | 'critical' {
    if (factors.contractEnding && score < 50) return 'critical';
    if (factors.paymentFailures > 3) return 'critical';
    if (score < 40) return 'high';
    if (score < 70) return 'medium';
    return 'low';
  }

  private generateAlerts(customerId: string, data: any): CustomerAlert[] {
    const alerts: CustomerAlert[] = [];

    if (data.usage.monthOverMonthChange < -20) {
      alerts.push({ type: 'usage_drop', severity: 'warning', message: 'Usage dropped more than 20% this month', timestamp: new Date().toISOString() });
    }

    if (data.payments.recentFailures > 0) {
      alerts.push({ type: 'payment_failure', severity: 'warning', message: `${data.payments.recentFailures} recent payment failures`, timestamp: new Date().toISOString(), actionUrl: `${APP_URL}/admin/billing/${customerId}` });
    }

    if (data.support.openTickets > 5) {
      alerts.push({ type: 'support_spike', severity: 'info', message: `${data.support.openTickets} open support tickets`, timestamp: new Date().toISOString() });
    }

    if (data.contract.daysUntilEnd < 90 && data.contract.daysUntilEnd >= 0) {
      alerts.push({ type: 'contract_expiring', severity: 'critical', message: `Contract expires in ${data.contract.daysUntilEnd} days`, timestamp: new Date().toISOString(), actionUrl: `${APP_URL}/admin/contracts/${customerId}/renew` });
    }

    return alerts;
  }
}
```

## Renewal Pipeline View

```typescript
interface RenewalPipelineEntry {
  contractId: string;
  customerName: string;
  contractValue: number;
  renewalDate: string;
  daysUntilRenewal: number;
  probability: number;            // 0-100
  expectedValue: number;          // contractValue * probability
  stage: 'not_started' | 'contacted' | 'negotiating' | 'proposal_sent' | 'verbal_commit' | 'closed_won' | 'closed_lost';
  accountManager: string;
  lastActivity: string;
  riskLevel: 'low' | 'medium' | 'high';
}

class RenewalPipelineService {
  async getPipeline(
    dateRange: { start: string; end: string }
  ): Promise<RenewalPipelineEntry[]> {
    const contracts = await this.getContractsExpiringInRange(dateRange);
    const entries: RenewalPipelineEntry[] = [];

    for (const contract of contracts) {
      const negotiation = await this.negotiationTracker.getNegotiation(contract.id);
      const health = await this.healthCalculator.calculateHealthScore(contract.tenantId);

      entries.push({
        contractId: contract.id,
        customerName: contract.customerName,
        contractValue: contract.pricing.monthlyPrice * 12,
        renewalDate: contract.term.endDate,
        daysUntilRenewal: Math.ceil(
          (new Date(contract.term.endDate).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
        ),
        probability: negotiation?.probability || health.overallScore / 100 * 80,
        expectedValue: 0,         // Calculated below
        stage: this.determinePipelineStage(contract, negotiation),
        accountManager: contract.accountManagerName,
        lastActivity: negotiation?.negotiationHistory[negotiation.negotiationHistory.length - 1]?.date || contract.updatedAt,
        riskLevel: health.riskLevel === 'critical' ? 'high' : health.riskLevel === 'high' ? 'high' : 'medium',
      });
    }

    // Calculate expected values
    for (const entry of entries) {
      entry.expectedValue = Math.round(entry.contractValue * (entry.probability / 100));
    }

    return entries;
  }

  private determinePipelineStage(
    contract: Contract,
    negotiation?: RenewalNegotiation
  ): RenewalPipelineEntry['stage'] {
    if (!negotiation || negotiation.status === 'not_started') return 'not_started';
    if (negotiation.status === 'in_progress') return 'negotiating';
    if (negotiation.status === 'agreed') return 'closed_won';
    if (negotiation.status === 'lost') return 'closed_lost';
    return 'contacted';
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Sales portal data model
- **Redis** — Real-time customer health score caching
- **BullMQ** — Scheduled health score recalculation
- **Metabase** (Apache 2.0) — Embedded analytics dashboards
- **pdfmake** (MIT) — Quote PDF generation
- **DocuSeal** (AGPL v3) — Contract signing integration
- **Node.js/React** — Frontend portal framework
- **OpenTelemetry** — Portal usage tracking and performance monitoring

## Integration Points

Enterprise sales portal integrates with the quote system (quote generation), contract management (contract library), usage metering (customer health), CRM (pipeline data), notification service (alerts), and document storage (contract documents).

## Production Considerations

- Implement role-based access control for sensitive contract data
- Provide real-time price calculations during quote creation
- Cache customer health scores with periodic recalculation
- Support multi-currency and multi-region enterprise customers
- Track portal usage analytics for sales team optimization
- Implement rate limiting on quote generation API
- Provide mobile-responsive interface for field sales
- Support integrations with external CRM (Salesforce, HubSpot)
- Export pipeline data for executive reporting

## Open-Source First Philosophy

The entire enterprise sales portal is built on open-source components: React frontend, Node.js API, PostgreSQL database, Redis caching, Metabase analytics, pdfmake for documents, and DocuSeal for signing. This stack replaces proprietary sales tools like Salesforce CPQ, DocuSign, and Tableau while providing a unified, customizable portal for enterprise sales operations with complete data ownership.
