# Section 07: Usage Audits for Enterprise

## Usage Verification Reports

Enterprise customers require verified usage reports to reconcile invoices against actual consumption.

```
[Usage Data Collected]
    ├── Real-time metering
    ├── Hourly/daily aggregation
    └── Stored in data warehouse
    ↓
[Audit Period Defined]
    ├── Monthly, quarterly, or annual
    ├── Aligned with contract terms
    └── Customer-specified date range
    ↓
[Generate Audit Report]
    ├── Usage by product/category
    ├── Daily/weekly breakdown
    ├── Comparison to commitment
    └── Usage trend analysis
    ↓
[Verify and Certify]
    ├── Data integrity check
    ├── System of record verification
    ├── Certificate generation
    └── Digital signature
    ↓
[Deliver to Customer]
    ├── PDF report
    ├── Raw data export (CSV/JSON)
    ├── API access to audit data
    └── Portal dashboard
```

```typescript
interface UsageAuditReport {
  id: string;
  tenantId: string;
  contractId: string;
  period: { start: string; end: string };
  type: 'monthly' | 'quarterly' | 'annual' | 'custom';
  generatedAt: string;
  status: 'generating' | 'ready' | 'delivered' | 'verified';
  summary: UsageAuditSummary;
  categories: UsageCategory[];
  dailyBreakdown: DailyUsage[];
  commitmentComparison: CommitmentComparison;
  dataIntegrity: DataIntegrityCheck;
  certificateUrl?: string;
}

interface UsageAuditSummary {
  totalUnits: number;
  totalAmount: number;
  averageDailyUsage: number;
  peakDailyUsage: number;
  daysWithData: number;
  dataPoints: number;
}

interface UsageCategory {
  name: string;
  productId: string;
  totalUnits: number;
  totalAmount: number;
  percentageOfTotal: number;
  trend: 'increasing' | 'stable' | 'decreasing';
}

interface DailyUsage {
  date: string;
  units: number;
  amount: number;
  category: string;
  source: string;
}

interface CommitmentComparison {
  committedUnits: number;
  actualUnits: number;
  variance: number;
  variancePercent: number;
  shortfallAmount?: number;
  overageAmount?: number;
  status: 'met' | 'shortfall' | 'overage';
}

class UsageAuditService {
  async generateAuditReport(
    tenantId: string,
    contractId: string,
    period: { start: string; end: string }
  ): Promise<UsageAuditReport> {
    // Collect all usage data for the period
    const usageData = await this.collectUsageData(tenantId, period);

    // Get contract commitment
    const commitment = await this.getContractCommitment(contractId);

    // Calculate daily breakdown
    const dailyBreakdown = this.calculateDailyBreakdown(usageData);

    // Calculate summary
    const summary: UsageAuditSummary = {
      totalUnits: usageData.reduce((s, d) => s + d.units, 0),
      totalAmount: usageData.reduce((s, d) => s + d.amount, 0),
      averageDailyUsage: 0,
      peakDailyUsage: Math.max(...dailyBreakdown.map(d => d.units)),
      daysWithData: dailyBreakdown.length,
      dataPoints: usageData.length,
    };
    summary.averageDailyUsage = summary.daysWithData > 0
      ? summary.totalUnits / summary.daysWithData
      : 0;

    // Calculate categories
    const categories = this.calculateCategories(usageData);

    // Calculate commitment comparison
    const commitmentComparison: CommitmentComparison = {
      committedUnits: commitment?.minimumUnits || 0,
      actualUnits: summary.totalUnits,
      variance: summary.totalUnits - (commitment?.minimumUnits || 0),
      variancePercent: commitment?.minimumUnits
        ? ((summary.totalUnits - commitment.minimumUnits) / commitment.minimumUnits) * 100
        : 0,
      status: this.determineStatus(summary.totalUnits, commitment),
    };

    // Perform data integrity check
    const dataIntegrity = await this.performIntegrityCheck(tenantId, period);

    const report: UsageAuditReport = {
      id: generateId('audit'),
      tenantId,
      contractId,
      period,
      type: this.determineReportType(period),
      generatedAt: new Date().toISOString(),
      status: 'generating',
      summary,
      categories,
      dailyBreakdown,
      commitmentComparison,
      dataIntegrity,
    };

    // Generate certificate
    report.certificateUrl = await this.generateAuditCertificate(report);

    report.status = 'ready';

    await this.storeAuditReport(report);

    return report;
  }

  private async performIntegrityCheck(
    tenantId: string,
    period: { start: string; end: string }
  ): Promise<DataIntegrityCheck> {
    // Check for gaps in data
    const gaps = await this.findDataGaps(tenantId, period);

    // Verify source data consistency
    const sourceChecks = await this.verifySourceConsistency(tenantId, period);

    // Calculate checksums
    const checksum = await this.calculateDataChecksum(tenantId, period);

    return {
      passed: gaps.length === 0 && sourceChecks.every(c => c.passed),
      gaps,
      sourceChecks,
      checksum,
      verifiedAt: new Date().toISOString(),
    };
  }
}
```

## Overage vs Commitment Reconciliation

```typescript
interface OverageReconciliation {
  contractId: string;
  period: { start: string; end: string };
  commitmentAmount: number;
  usageAmount: number;
  overageAmount: number;
  overageRate: number;
  overageCharge: number;
  shortfallAmount: number;
  shortfallRate: number;
  shortfallCharge: number;
  netAmount: number;
  priorCredits: number;
  totalDue: number;
}

class OverageReconciliationService {
  async reconcile(
    contractId: string,
    period: { start: string; end: string }
  ): Promise<OverageReconciliation> {
    const commitment = await this.getCommitment(contractId);
    const usage = await this.getUsageForPeriod(contractId, period);

    const usageAmount = usage.totalAmount;
    const commitmentAmount = commitment.minimumAmount;

    const overageAmount = Math.max(0, usageAmount - commitmentAmount);
    const shortfallAmount = Math.max(0, commitmentAmount - usageAmount);

    const overageCharge = overageAmount * commitment.overageRate;
    const shortfallCharge = shortfallAmount * commitment.shortfallRate;

    // Get any prior credits (carry-forward overage)
    const priorCredits = await this.getPriorCredits(contractId);

    const netAmount = (overageCharge - shortfallCharge) - priorCredits;
    const totalDue = Math.max(0, netAmount);

    return {
      contractId,
      period,
      commitmentAmount,
      usageAmount,
      overageAmount,
      overageRate: commitment.overageRate,
      overageCharge,
      shortfallAmount,
      shortfallRate: commitment.shortfallRate,
      shortfallCharge,
      netAmount,
      priorCredits,
      totalDue,
    };
  }
}
```

## Audit Certificate Generation

```typescript
interface AuditCertificate {
  reportId: string;
  certNumber: string;
  tenantId: string;
  contractId: string;
  period: { start: string; end: string };
  issuedAt: string;
  expiresAt?: string;
  signedBy: string;
  signature: string;             // Digital signature
  sealUrl?: string;              // Trust seal image
  verificationUrl: string;       // URL to verify certificate
  dataHash: string;              // SHA-256 of the report data
}

class AuditCertificateService {
  async generateCertificate(report: UsageAuditReport): Promise<string> {
    const certData = {
      reportId: report.id,
      tenantId: report.tenantId,
      contractId: report.contractId,
      period: report.period,
      summary: report.summary,
      commitmentComparison: report.commitmentComparison,
      dataIntegrity: report.dataIntegrity,
    };

    // Create certificate hash
    const certHash = crypto
      .createHash('sha256')
      .update(JSON.stringify(certData))
      .digest('hex');

    const certificate: AuditCertificate = {
      reportId: report.id,
      certNumber: `AUD-${report.tenantId}-${Date.now()}`,
      tenantId: report.tenantId,
      contractId: report.contractId,
      period: report.period,
      issuedAt: new Date().toISOString(),
      signedBy: 'system',
      signature: certHash,
      verificationUrl: `${APP_URL}/audit/verify/${certHash}`,
      dataHash: certHash,
    };

    // Store certificate
    await this.storeCertificate(certificate);

    // Generate audit PDF with certificate
    const pdfUrl = await this.generateAuditPDF(report, certificate);

    return pdfUrl;
  }

  async verifyCertificate(certHash: string): Promise<VerificationResult> {
    const cert = await this.getCertificateByHash(certHash);
    if (!cert) {
      return { valid: false, reason: 'Certificate not found' };
    }

    // Verify the data hash matches
    const report = await this.getAuditReport(cert.reportId);
    const computedHash = crypto
      .createHash('sha256')
      .update(JSON.stringify({
        reportId: report.id,
        tenantId: report.tenantId,
        contractId: report.contractId,
        period: report.period,
        summary: report.summary,
        commitmentComparison: report.commitmentComparison,
        dataIntegrity: report.dataIntegrity,
      }))
      .digest('hex');

    if (computedHash !== cert.dataHash) {
      return { valid: false, reason: 'Data integrity check failed — report has been modified' };
    }

    return {
      valid: true,
      certificate: cert,
      report,
      verifiedAt: new Date().toISOString(),
    };
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Usage data warehouse for audit queries
- **BullMQ** — Scheduled audit report generation
- **pdfmake** (MIT) — Audit report PDF generation
- **MinIO** (AGPL v3) — Audit report and certificate storage
- **Metabase** (Apache 2.0) — Self-serve usage audit dashboards
- **OpenTelemetry** — Audit data lineage tracing
- **Apache Calcite** (Apache 2.0) — SQL-based audit data queries

## Integration Points

Usage audits integrate with the usage metering system (data source), contract management (commitment comparison), invoice system (reconciliation), customer portal (report delivery), and compliance (certificate generation).

## Production Considerations

- Provide raw data exports in multiple formats (CSV, JSON, Parquet)
- Support ad-hoc audit queries for enterprise customers
- Maintain data lineage from meter to invoice
- Implement data retention aligned with contract terms
- Allow customers to schedule recurring audit reports
- Generate data integrity proofs (checksums, hashes)
- Support third-party audit tool integration via API
- Provide API-based audit data access for automated reconciliation

## Open-Source First Philosophy

PostgreSQL with TimescaleDB stores the complete usage data warehouse for arbitrary audit queries. pdfmake generates professional audit reports with certificate pages. MinIO provides cost-effective long-term audit storage. Metabase enables self-serve usage dashboards for enterprise customers. This open-source stack replaces proprietary audit and reconciliation tools while providing complete transparency and data access.
