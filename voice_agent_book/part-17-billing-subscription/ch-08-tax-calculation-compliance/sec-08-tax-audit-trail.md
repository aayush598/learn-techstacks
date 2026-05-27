# Section 08: Tax Audit Trail

## Per-Transaction Tax Records

Every taxable transaction must maintain a complete tax audit trail that captures the full state of tax determination at the time of the transaction.

```
[Invoice Generated]
    ↓
[Snap Tax State]
    ├── Tax rate (snapshotted)
    ├── Product taxability rules
    ├── Customer exemption status
    └── Jurisdiction details
    ↓
[Calculate Tax]
    ↓
[Record Audit Record]
    ├── tax_calculation_id (UUID)
    ├── invoice_id
    ├── tenant_id
    ├── tax_line_items[]
    ├── rate_snapshot
    ├── exemption_reference
    └── calculation_metadata
    ↓
[Archive to Audit Store]
    ├── Immutable record
    ├── Timestamped
    └── Checksummed
```

## Rate Snapshot at Time of Transaction

Tax rates change over time. The system must capture the exact rate used at the transaction moment.

```typescript
interface TaxRateSnapshot {
  rateId: string;
  jurisdiction: string;
  jurisdictionType: 'country' | 'state' | 'county' | 'city' | 'special';
  baseRate: number;
  breakdown: TaxRateComponent[];
  effectiveDate: string;
  snapshotDate: string;           // When this rate was captured
  rateVersion: number;
  supersededBy?: string;          // If rate has changed since
}

interface TaxRateComponent {
  name: string;
  type: 'state' | 'county' | 'city' | 'special_district';
  rate: number;
  authority: string;
}

interface TaxCalculationRecord {
  id: string;
  invoiceId: string;
  tenantId: string;
  transactionDate: string;
  lineItems: TaxLineItemRecord[];
  totalTaxAmount: number;
  currency: string;
  calculationMethod: 'unit' | 'percentage' | 'compound';
  roundingMethod: 'per_line' | 'per_transaction';
  metadata: Record<string, string>;
  createdAt: string;
  checksum: string;
}

interface TaxLineItemRecord {
  lineItemId: string;
  productId: string;
  productType: string;
  quantity: number;
  unitPrice: number;
  subtotal: number;
  taxAmount: number;
  taxRate: number;
  rateSnapshotId: string;
  jurisdictionPath: string[];
  exemptionReason?: string;
  taxability: 'taxable' | 'exempt' | 'partially_exempt';
  exemptAmount?: number;
}

class TaxAuditService {
  private readonly auditStore: TaxAuditStore;

  async recordTaxCalculation(
    calculation: TaxCalculation
  ): Promise<TaxCalculationRecord> {
    // Build immutable audit record
    const record: TaxCalculationRecord = {
      id: generateId('tax_calc'),
      invoiceId: calculation.invoiceId,
      tenantId: calculation.tenantId,
      transactionDate: new Date().toISOString(),
      lineItems: calculation.lineItems.map(item => ({
        lineItemId: item.id,
        productId: item.productId,
        productType: item.productType,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        subtotal: item.subtotal,
        taxAmount: item.taxAmount,
        taxRate: item.taxRate,
        rateSnapshotId: item.rateSnapshotId,
        jurisdictionPath: item.jurisdictionPath,
        exemptionReason: item.exemptionReason,
        taxability: item.taxability,
        exemptAmount: item.exemptAmount,
      })),
      totalTaxAmount: calculation.totalTaxAmount,
      currency: calculation.currency,
      calculationMethod: calculation.calculationMethod,
      roundingMethod: calculation.roundingMethod,
      metadata: calculation.metadata,
      createdAt: new Date().toISOString(),
      checksum: this.computeChecksum(calculation),
    };

    await this.auditStore.append(record);
    return record;
  }

  private computeChecksum(data: any): string {
    const serialized = JSON.stringify(data, Object.keys(data).sort());
    return crypto.createHash('sha256').update(serialized).digest('hex');
  }
}
```

## Tax Code Mappings

Tax codes map products to their tax treatment across jurisdictions.

```typescript
interface TaxCodeMapping {
  taxCode: string;
  description: string;
  jurisdictionMappings: TaxCodeJurisdictionMapping[];
}

interface TaxCodeJurisdictionMapping {
  jurisdiction: string;
  taxability: 'taxable' | 'exempt' | 'reduced_rate';
  rate?: number;
  category: string;
  subcategory?: string;
  nexusRequired: boolean;
}

const TAX_CODE_MAPPINGS: TaxCodeMapping[] = [
  {
    taxCode: 'voice_services',
    description: 'Voice communication services',
    jurisdictionMappings: [
      {
        jurisdiction: 'US',
        taxability: 'taxable',
        category: 'Communications',
        subcategory: 'Voice',
        nexusRequired: true,
      },
      {
        jurisdiction: 'EU',
        taxability: 'taxable',
        rate: 0.20,
        category: 'Telecommunications',
        nexusRequired: false,
      },
      {
        jurisdiction: 'UK',
        taxability: 'taxable',
        rate: 0.20,
        category: 'Telecommunications',
        nexusRequired: false,
      },
    ],
  },
  {
    taxCode: 'ai_processing',
    description: 'AI voice processing services',
    jurisdictionMappings: [
      {
        jurisdiction: 'US',
        taxability: 'exempt',
        category: 'Digital Services',
        subcategory: 'AI Processing',
        nexusRequired: false,
      },
      {
        jurisdiction: 'EU',
        taxability: 'taxable',
        rate: 0.20,
        category: 'Digital Services',
        subcategory: 'Automated',
        nexusRequired: false,
      },
    ],
  },
];

class TaxCodeService {
  async resolveTaxCode(
    product: Product,
    jurisdiction: string
  ): Promise<TaxCodeResolution> {
    // Find the mapping for this product
    const mapping = await this.getMapping(product.taxCode, jurisdiction);
    if (!mapping) {
      return { taxCode: product.taxCode, taxability: 'unknown', rate: null };
    }

    return {
      taxCode: product.taxCode,
      taxability: mapping.taxability,
      rate: mapping.rate,
      category: mapping.category,
      subcategory: mapping.subcategory,
    };
  }
}
```

## Exemption Records

Exemption certificates and their association with transactions must be stored for audit.

```typescript
interface ExemptionAuditRecord {
  exemptionId: string;
  customerId: string;
  tenantId: string;
  certificateType: 'resale' | 'exempt_entity' | 'government' | 'charity' | 'other';
  jurisdiction: string;
  certificateNumber: string;
  issueDate: string;
  expirationDate: string;
  status: 'active' | 'expired' | 'revoked' | 'pending_review';
  transactions: ExemptTransaction[];
  documentUrl?: string;
  reviewedBy?: string;
  reviewDate?: string;
}

interface ExemptTransaction {
  invoiceId: string;
  transactionDate: string;
  amount: number;
  exemptAmount: number;
  taxSaved: number;
  exemptionReason: string;
}

class ExemptionAuditService {
  async recordExemptTransaction(
    exemptionId: string,
    invoice: Invoice,
    exemptionResult: ExemptionResult
  ): Promise<void> {
    const record: ExemptTransaction = {
      invoiceId: invoice.id,
      transactionDate: invoice.createdAt,
      amount: invoice.total,
      exemptAmount: exemptionResult.exemptAmount,
      taxSaved: exemptionResult.taxSaved,
      exemptionReason: exemptionResult.reason,
    };

    await this.appendExemptTransaction(exemptionId, record);
  }

  async generateExemptionReport(
    customerId: string,
    startDate: string,
    endDate: string
  ): Promise<ExemptionReport> {
    const exemptions = await this.getCustomerExemptions(customerId);

    const report: ExemptionReport = {
      customerId,
      reportPeriod: { start: startDate, end: endDate },
      exemptions: exemptions.map(ex => ({
        exemptionId: ex.exemptionId,
        certificateType: ex.certificateType,
        jurisdiction: ex.jurisdiction,
        totalExemptTransactions: ex.transactions.length,
        totalExemptAmount: ex.transactions.reduce((s, t) => s + t.exemptAmount, 0),
        totalTaxSaved: ex.transactions.reduce((s, t) => s + t.taxSaved, 0),
      })),
      summary: {
        totalExemptAmount: 0,
        totalTaxSaved: 0,
      },
    };

    report.summary.totalExemptAmount = report.exemptions.reduce(
      (s, e) => s + e.totalExemptAmount, 0
    );
    report.summary.totalTaxSaved = report.exemptions.reduce(
      (s, e) => s + e.totalTaxSaved, 0
    );

    return report;
  }
}
```

## Audit Trail Storage

```typescript
interface TaxAuditStore {
  append(record: TaxCalculationRecord): Promise<void>;
  findByInvoiceId(invoiceId: string): Promise<TaxCalculationRecord>;
  findByTenantAndDateRange(
    tenantId: string,
    startDate: string,
    endDate: string
  ): Promise<TaxCalculationRecord[]>;
  findByTransactionId(transactionId: string): Promise<TaxCalculationRecord>;
}

// PostgreSQL implementation with immutable append-only pattern
class PostgresTaxAuditStore implements TaxAuditStore {
  private readonly pool: Pool;
  private readonly archiveTable = 'tax_calculation_archive';

  async append(record: TaxCalculationRecord): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');

      // Write to archive table (append-only, no updates)
      await client.query(
        `INSERT INTO ${this.archiveTable} (
          id, invoice_id, tenant_id, transaction_date,
          line_items, total_tax_amount, currency,
          calculation_method, rounding_method, metadata,
          created_at, checksum
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
        [
          record.id, record.invoiceId, record.tenantId,
          record.transactionDate, JSON.stringify(record.lineItems),
          record.totalTaxAmount, record.currency,
          record.calculationMethod, record.roundingMethod,
          JSON.stringify(record.metadata), record.createdAt, record.checksum,
        ]
      );

      // Update current state (mutable for performance)
      await client.query(
        `INSERT INTO tax_calculation_current (
          id, invoice_id, tenant_id, transaction_date,
          line_items, total_tax_amount, checksum
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (invoice_id) DO UPDATE SET
          line_items = EXCLUDED.line_items,
          total_tax_amount = EXCLUDED.total_tax_amount,
          checksum = EXCLUDED.checksum`,
        [
          record.id, record.invoiceId, record.tenantId,
          record.transactionDate, JSON.stringify(record.lineItems),
          record.totalTaxAmount, record.checksum,
        ]
      );

      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async findByInvoiceId(invoiceId: string): Promise<TaxCalculationRecord> {
    const result = await this.pool.query(
      `SELECT * FROM ${this.archiveTable} WHERE invoice_id = $1`,
      [invoiceId]
    );
    return this.mapToRecord(result.rows[0]);
  }

  async findByTenantAndDateRange(
    tenantId: string,
    startDate: string,
    endDate: string
  ): Promise<TaxCalculationRecord[]> {
    const result = await this.pool.query(
      `SELECT * FROM ${this.archiveTable}
       WHERE tenant_id = $1
       AND transaction_date >= $2
       AND transaction_date <= $3
       ORDER BY transaction_date ASC`,
      [tenantId, startDate, endDate]
    );
    return result.rows.map(this.mapToRecord);
  }

  private mapToRecord(row: any): TaxCalculationRecord {
    return {
      ...row,
      lineItems: typeof row.line_items === 'string'
        ? JSON.parse(row.line_items)
        : row.line_items,
      metadata: typeof row.metadata === 'string'
        ? JSON.parse(row.metadata)
        : row.metadata,
    };
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Append-only audit trail with checksums
- **BullMQ** — Schedule audit log maintenance and retention
- **Stripe Tax** — Tax calculation source of truth
- **Metabase** (Apache 2.0) — Audit trail queries and reports
- **MinIO** (AGPL v3) — Long-term audit archive storage
- **OpenTelemetry** — Audit trail tracing and monitoring

## Integration Points

Tax audit trail integrates with the tax engine (records all calculations), the invoice system (per-invoice tax records), the exemption service (exemption certificates linked to transactions), and the reporting system (audit query interface).

## Production Considerations

- Implement append-only storage with cryptographic checksums for immutability
- Retain records for the maximum statute of limitations (typically 7 years)
- Compress and archive records older than 90 days to cold storage
- Provide an admin query interface for auditors
- Generate checksums for each record to detect tampering
- Implement data retention policies per jurisdiction
- Support export formats (CSV, JSON, PDF) for auditor requests

## Open-Source First Philosophy

PostgreSQL's append-only tables and cryptographic functions provide a tamper-evident audit trail. MinIO stores archived records at low cost. Metabase delivers self-serve audit queries for tax and finance teams. This open-source stack replaces proprietary audit management systems while meeting Sarbanes-Oxley and GDPR audit requirements.
