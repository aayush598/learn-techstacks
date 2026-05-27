# Section 05: Tax Report Generation

## Monthly/Quarterly Tax Reports

Tax reports aggregate transaction-level tax data for filing. Reports are generated monthly or quarterly, depending on the jurisdiction's filing frequency.

```typescript
interface TaxReport {
  id: string;
  period: string;              // '2025-Q2' or '2025-06'
  reportType: 'monthly' | 'quarterly' | 'annual';
  jurisdiction: TaxJurisdictionSummary;
  taxableSales: TaxAmountSummary;
  taxCollected: TaxAmountSummary;
  transactionCount: number;
  lines: TaxReportLine[];
  generatedAt: string;
  status: 'draft' | 'final' | 'filed';
}

interface TaxReportLine {
  jurisdiction: string;
  taxRate: number;
  taxableAmount: number;
  taxAmount: number;
  currency: string;
  transactionCount: number;
  productTaxCode: string;
}

class TaxReportService {
  async generateTaxReport(
    periodStart: string,
    periodEnd: string,
    jurisdiction?: string
  ): Promise<TaxReport> {
    // Query tax data from transactions
    const match: any = {
      createdAt: { $gte: periodStart, $lte: periodEnd },
      taxTotal: { $gt: 0 },
    };
    if (jurisdiction) match['taxBreakdown.jurisdiction'] = jurisdiction;

    const transactions = await this.db.invoices.find(match).toArray();

    // Aggregate by jurisdiction
    const byJurisdiction = new Map<string, TaxReportLine>();

    for (const tx of transactions) {
      for (const tax of tx.taxBreakdown || []) {
        const key = `${tax.jurisdiction.country}-${tax.jurisdiction.state || ''}`;
        const existing = byJurisdiction.get(key) || {
          jurisdiction: key,
          taxRate: tax.taxRate,
          taxableAmount: 0,
          taxAmount: 0,
          currency: tx.currency,
          transactionCount: 0,
          productTaxCode: tax.taxCode || '',
        };

        existing.taxableAmount += tax.taxableAmount;
        existing.taxAmount += tax.taxAmount;
        existing.transactionCount++;

        byJurisdiction.set(key, existing);
      }
    }

    const lines = Array.from(byJurisdiction.values());
    const totalTaxable = lines.reduce((s, l) => s + l.taxableAmount, 0);
    const totalTax = lines.reduce((s, l) => s + l.taxAmount, 0);

    return {
      id: `tax_report_${nanoid(16)}`,
      period: this.formatPeriod(periodStart),
      reportType: this.determineReportType(periodStart, periodEnd),
      jurisdiction: {
        totalJurisdictions: lines.length,
      },
      taxableSales: { total: totalTaxable, currency: 'USD' },
      taxCollected: { total: totalTax, currency: 'USD' },
      transactionCount: transactions.length,
      lines,
      generatedAt: new Date().toISOString(),
      status: 'draft',
    };
  }

  private formatPeriod(dateStr: string): string {
    const date = new Date(dateStr);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
  }

  private determineReportType(start: string, end: string): 'monthly' | 'quarterly' | 'annual' {
    const startDate = new Date(start);
    const endDate = new Date(end);
    const diffMonths = (endDate.getFullYear() - startDate.getFullYear()) * 12
      + endDate.getMonth() - startDate.getMonth();

    if (diffMonths >= 12) return 'annual';
    if (diffMonths >= 3) return 'quarterly';
    return 'monthly';
  }
}
```

## Jurisdiction Summaries

Reports include summaries by jurisdiction, showing the tax rate, taxable sales, tax collected, and transaction count for each.

```
Tax Report — Jurisdiction Summary:
┌──────────────────────────────────────────────────────────────────┐
│ Jurisdiction    │ Taxable Sales │ Tax Collected │ Txns │ Rate   │
├─────────────────┼───────────────┼───────────────┼──────┼────────┤
│ US-CA           │ $45,230.50    │ $3,957.67     │ 342   │ 8.75%  │
│ US-NY           │ $23,100.00    │ $1,848.00     │ 156   │ 8.00%  │
│ US-TX           │ $18,750.25    │ $1,406.27     │ 128   │ 7.50%  │
│ US-FL           │ $12,400.00    │ $868.00       │ 89    │ 7.00%  │
│ EU-DE           │ €9,800.00     │ €1,960.00     │ 67    │ 19.00% │
│ EU-FR           │ €7,200.00     │ €1,440.00     │ 52    │ 20.00% │
│ EU-NL           │ €3,100.00     │ €651.00       │ 23    │ 21.00% │
├─────────────────┼───────────────┼───────────────┼──────┼────────┤
│ Total           │ $110,380.75   │ $10,130.94    │ 857   │        │
└──────────────────────────────────────────────────────────────────┘
```

## Marketplace Facilitator Reports

Marketplace facilitator rules shift tax responsibility to the marketplace platform. Reports must distinguish between marketplace and direct sales.

```typescript
interface MarketplaceSellerReport {
  sellerId: string;
  sellerName: string;
  period: string;
  totalSales: number;
  taxableSales: number;
  taxCollected: number;
  commissions: number;
  transactions: number;
}

async function generateMarketplaceReport(
  periodStart: string,
  periodEnd: string
): Promise<MarketplaceFacilitatorReport> {
  // Aggregate sales by seller
  const sellers = await this.db.invoices.aggregate([
    {
      $match: {
        createdAt: { $gte: periodStart, $lte: periodEnd },
        'metadata.marketplace_sale': 'true',
      },
    },
    {
      $group: {
        _id: '$metadata.seller_id',
        sellerName: { $first: '$metadata.seller_name' },
        totalSales: { $sum: '$total' },
        taxableSales: { $sum: '$subtotal' },
        taxCollected: { $sum: '$taxTotal' },
        transactions: { $sum: 1 },
      },
    },
  ]).toArray();

  return {
    period: `${periodStart} — ${periodEnd}`,
    totalSellers: sellers.length,
    totalTaxCollected: sellers.reduce((s, sl) => s + sl.taxCollected, 0),
    sellers: sellers.map(s => ({
      sellerId: s._id,
      sellerName: s.sellerName,
      totalSales: s.totalSales,
      taxableSales: s.taxableSales,
      taxCollected: s.taxCollected,
      transactions: s.transactions,
    })),
    generatedAt: new Date().toISOString(),
  };
}
```

## VAT Return Data

VAT returns require specific data formats that match each country's tax authority requirements.

```typescript
interface VATReturn {
  period: string;
  countryCode: string;
  vatNumber: string;
  scheme: 'oss' | 'normal';
  totalSales: number;
  vatDue: number;
  deductions: number;
  netVatPayable: number;
  breakdown: Array<{
    rate: string;
    netSales: number;
    vatRate: number;
    vatAmount: number;
  }>;
}

async function generateVATReturn(
  countryCode: string,
  period: string
): Promise<VATReturn> {
  const salesByRate = await this.db.invoices.aggregate([
    {
      $match: {
        'taxBreakdown.jurisdiction.country': countryCode,
        createdAt: { $regex: period },
      },
    },
    {
      $unwind: '$taxBreakdown',
    },
    {
      $group: {
        _id: { rate: '$taxBreakdown.taxRate' },
        netSales: { $sum: '$taxBreakdown.taxableAmount' },
        vatAmount: { $sum: '$taxBreakdown.taxAmount' },
      },
    },
  ]).toArray();

  return {
    period,
    countryCode,
    vatNumber: await this.getVATNumber(countryCode),
    scheme: 'oss',
    totalSales: salesByRate.reduce((s, r) => s + r.netSales, 0),
    vatDue: salesByRate.reduce((s, r) => s + r.vatAmount, 0),
    deductions: 0,
    netVatPayable: salesByRate.reduce((s, r) => s + r.vatAmount, 0),
    breakdown: salesByRate.map(r => ({
      rate: r._id.rate,
      netSales: r.netSales,
      vatRate: r._id.rate,
      vatAmount: r.vatAmount,
    })),
  };
}
```

## Open-Source Tools

- **PostgreSQL** — Report data aggregation
- **BullMQ** (MIT) — Schedule report generation
- **Metabase** (Apache 2.0) — Self-service tax dashboards
- **pdfmake** (MIT) — Report PDF generation
- **Nodemailer** (MIT) — Report delivery to finance team

## Integration Points

Tax report generation connects to the invoice database (transaction data), the tax engine (rate information), the exemption system (exempt amounts), and the notification service (report delivery).

## Production Considerations

- Schedule report generation to run after period close
- Validate report totals against general ledger
- Maintain historical reports for audit (7+ years)
- Support multi-currency reporting (USD, EUR, GBP, etc.)
- Allow manual adjustments for corrections

## Open-Source First Philosophy

Tax reports are generated from PostgreSQL data using aggregation queries. BullMQ schedules report generation. Metabase provides self-service dashboards for the finance team. pdfmake generates formatted PDF reports. This all-open-source stack replaces expensive tax reporting software while providing comprehensive filing data.
