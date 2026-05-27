# Section 07: Compliance Reporting & Audit

## Overview

Compliance Reporting & Audit provides the documentation infrastructure that demonstrates regulatory adherence to TCPA, FDCPA, GDPR, and other telemarketing regulations. In the event of a regulatory investigation or consumer lawsuit, the compliance report is the first document regulators and plaintiffs' attorneys request. A well-structured compliance report can demonstrate good-faith efforts and mitigate penalties, while a missing or incomplete report is prima facie evidence of non-compliance. The reporting system must capture every step of the dialing process: consent verification, DNC checking, time-of-day compliance, call outcome, and the audit trail of all compliance decisions.

Beyond regulatory defense, compliance reports serve internal governance needs: compliance teams review reports to identify violations before they become lawsuits, operations teams use metrics to improve compliance rates, and business development teams use compliance documentation to win enterprise clients. The system must support real-time compliance dashboards, scheduled regulatory filings, and ad-hoc audit report generation with chain-of-custody documentation. Reports must be tamper-evident, cryptographically signed, and exportable to formats accepted by regulators and courts.

## Architecture

```
               Compliance Reporting & Audit System

  +-----------+  +-----------+  +-----------+  +-----------+
  | DNC       |  | Consent   |  | Call Log  |  | Campaign  |
  | Check Log |  | Records   |  | (Part 12) |  | Config    |
  +-----+-----+  +-----+-----+  +-----+-----+  +-----+-----+
        |              |              |              |
        v              v              v              v
  +-------------------------------------------------------+
  |             Compliance Data Lake                       |
  |                                                        |
  |  Append-only event store:                              |
  |  timestamp | event_type | entity_id | payload | hash   |
  | -----------+------------+-----------+---------+--------|
  | T1         | dnc_check  | call-001  | {...}   | h1     |
  | T2         | consent_ver | call-001 | {...}   | h2     |
  | T3         | dial_attempt| call-001 | {...}   | h3     |
  | T4         | call_outcome| call-001 | {...}   | h4     |
  +---------------------------+---------------------------+
                              |
                              v
  +-------------------------------------------------------+
  |            Report Generation Engine                     |
  |                                                        |
  |  - TCPA Compliance Report                              |
  |  - DNC Refresh Report                                  |
  |  - Calling Hours Compliance                            |
  |  - Consent Audit Trail                                 |
  |  - Violation Detection & Alerts                        |
  |  - Regulatory Filing Export                            |
  +---------------------------+---------------------------+
                              |
          +-------------------+-------------------+
          |                                       |
          v                                       v
  +------------------+                  +------------------+
  | Real-Time        |                  | Scheduled        |
  | Dashboard        |                  | Reports          |
  | (Grafana)        |                  | (PDF, CSV, JSON) |
  +------------------+                  +------------------+
```

## Design Decisions

- **Append-only event store with hash chaining:** All compliance events are stored in an append-only database table with cryptographic hash chaining. Each event includes the hash of the previous event, making post-hoc tampering detectable. Trade-off: storage growth (never deleted) vs. indisputable audit trail integrity.

- **Separate compliance data lake from operational database:** Compliance data is replicated from operational systems into a separate compliance data store with strict access controls. This prevents operational data cleanup from affecting regulatory records. Trade-off: data duplication and ETL overhead vs. data integrity and access control separation.

- **Automated violation detection with alerting:** The system continuously scans compliance events for violations: calls to DNC numbers, calls outside permitted hours, calls without consent, excessive retry counts. Violations trigger immediate alerts to compliance officers. Trade-off: false positive alert noise vs. early violation detection.

- **Report templates certified by compliance counsel:** Report templates are designed and certified by legal counsel to meet regulatory requirements. Templates include all required fields, disclaimers, and attestation statements. Trade-off: template rigidity vs. regulatory acceptance guarantee.

## Implementation Approach

```
interface ComplianceEvent {
  id: string;
  timestamp: Date;
  eventType: string;
  entityId: string;     // call_id, campaign_id, contact_id
  payload: Record<string, any>;
  previousHash: string;
  currentHash: string;
  signature: string;
}

class ComplianceAuditService {
  constructor(eventStore, hashChain, reportGenerator) {
    this.eventStore = eventStore; // Append-only database
    this.hashChain = hashChain;
    this.reportGenerator = reportGenerator;
  }

  async recordEvent(eventType, entityId, payload) {
    const lastHash = await this.hashChain.getLastHash();

    const event = {
      id: this.generateId(),
      timestamp: new Date(),
      eventType,
      entityId,
      payload: this.sanitizePayload(payload),
      previousHash: lastHash,
      currentHash: this.computeHash({
        eventType,
        entityId,
        payload,
        previousHash: lastHash
      })
    };

    event.signature = this.signEvent(event.currentHash);

    // Store in append-only event store
    await this.eventStore.append(event);

    // Update hash chain
    await this.hashChain.setLastHash(event.currentHash);

    // Check for violations (async)
    await this.checkViolations(event);

    return event;
  }

  async generateComplianceReport(options) {
    const {
      startDate,
      endDate,
      campaignId,
      format = 'pdf',
      reportType = 'tcpa_full'
    } = options;

    // 1. Gather raw data
    const events = await this.eventStore.query({
      timestamp: { gte: startDate, lte: endDate },
      ...(campaignId ? { 'payload.campaignId': campaignId } : {})
    });

    // 2. Verify hash chain integrity
    const chainValid = await this.verifyHashChain(events);
    if (!chainValid) {
      throw new Error('Hash chain integrity check FAILED — data may have been tampered with');
    }

    // 3. Build report data
    const reportData = await this.buildReportData(events, options);

    // 4. Generate report
    const report = await this.reportGenerator.generate(reportType, reportData, format);

    // 5. Sign report
    const reportSignature = this.signReport(report);

    return {
      report,
      signature: reportSignature,
      generatedAt: new Date(),
      hashChainValid: chainValid,
      eventCount: events.length,
      dateRange: { startDate, endDate }
    };
  }

  async buildReportData(events, options) {
    return {
      summary: this.buildSummary(events),
      dncChecks: this.extractEvents(events, 'dnc_check'),
      consentVerifications: this.extractEvents(events, 'consent_verification'),
      dialAttempts: this.extractEvents(events, 'dial_attempt'),
      callOutcomes: this.extractEvents(events, 'call_outcome'),
      optOuts: this.extractEvents(events, 'opt_out'),
      violations: this.detectViolations(events),
      campaignInfo: await this.getCampaignInfo(options.campaignId),
      hashChainVerified: true,
      generatedAt: new Date()
    };
  }

  buildSummary(events) {
    const totalCalls = events.filter(e => e.eventType === 'dial_attempt').length;
    const dncBlocked = events.filter(e => 
      e.eventType === 'dnc_check' && e.payload.matched === true
    ).length;
    const optOuts = events.filter(e => e.eventType === 'opt_out').length;
    const consentVerified = events.filter(e =>
      e.eventType === 'consent_verification' && e.payload.hasConsent === true
    ).length;

    return {
      totalCalls,
      dncBlocked,
      optOuts,
      consentVerified,
      complianceRate: totalCalls > 0 
        ? ((totalCalls - this.countViolations(events)) / totalCalls * 100).toFixed(2)
        : 100,
      periodCovered: this.formatPeriod(events[0]?.timestamp, events[events.length - 1]?.timestamp),
      hashChainIntegrity: 'verified'
    };
  }

  async verifyHashChain(events) {
    // Verify that each event's hash matches and chain is unbroken
    if (events.length === 0) return true;

    events.sort((a, b) => a.timestamp - b.timestamp);

    for (let i = 0; i < events.length; i++) {
      const event = events[i];

      // Verify current hash
      const computedHash = this.computeHash({
        eventType: event.eventType,
        entityId: event.entityId,
        payload: event.payload,
        previousHash: event.previousHash
      });

      if (computedHash !== event.currentHash) {
        console.error(`Hash mismatch at event ${event.id}`);
        return false;
      }

      // Verify chain linkage
      if (i > 0) {
        if (event.previousHash !== events[i - 1].currentHash) {
          console.error(`Chain break between event ${events[i-1].id} and ${event.id}`);
          return false;
        }
      }

      // Verify signature
      const signatureValid = this.verifySignature(event.currentHash, event.signature);
      if (!signatureValid) {
        console.error(`Invalid signature at event ${event.id}`);
        return false;
      }
    }

    return true;
  }

  async checkViolations(event) {
    const violations = [];

    switch (event.eventType) {
      case 'dial_attempt':
        // Check if call was made to DNC-listed number
        if (event.payload.dncMatched === true && !event.payload.hasConsent) {
          violations.push({
            type: 'DNC_VIOLATION',
            severity: 'critical',
            description: `Call placed to DNC-listed number ${event.payload.phone}`,
            eventId: event.id
          });
        }

        // Check calling hours
        if (!this.isWithinCallingHours(event.timestamp, event.payload.timezone)) {
          violations.push({
            type: 'CALLING_HOURS_VIOLATION',
            severity: 'high',
            description: `Call placed outside permitted hours at ${event.timestamp}`,
            eventId: event.id
          });
        }

        // Check retry limits
        if (event.payload.retryCount > event.payload.maxRetries) {
          violations.push({
            type: 'EXCESSIVE_RETRY',
            severity: 'medium',
            description: `Excessive retries for ${event.payload.phone}: ${event.payload.retryCount}`,
            eventId: event.id
          });
        }
        break;

      case 'opt_out':
        // Check if call was made after opt-out
        const subsequentCalls = await this.eventStore.query({
          eventType: 'dial_attempt',
          'payload.phone': event.payload.phone,
          timestamp: { gt: event.timestamp }
        });
        if (subsequentCalls.length > 0) {
          violations.push({
            type: 'POST_OPTOUT_CALL',
            severity: 'critical',
            description: `${subsequentCalls.length} call(s) made after opt-out for ${event.payload.phone}`,
            eventId: event.id
          });
        }
        break;
    }

    // Log violations
    if (violations.length > 0) {
      for (const v of violations) {
        await this.recordEvent('compliance_violation', event.entityId, v);
      }
      await this.alertViolations(violations);
    }

    return violations;
  }

  async alertViolations(violations) {
    const criticalViolations = violations.filter(v => v.severity === 'critical');

    if (criticalViolations.length > 0) {
      // Immediate alert to compliance team
      await this.notificationService.send({
        channel: ['email', 'sms', 'slack'],
        priority: 'urgent',
        subject: `CRITICAL: ${criticalViolations.length} compliance violations detected`,
        body: this.formatViolationAlert(criticalViolations)
      });
    }

    // Log to monitoring
    for (const v of violations) {
      this.metrics.increment('compliance.violation', {
        type: v.type,
        severity: v.severity
      });
    }
  }

  async generateTcpReport(startDate, endDate) {
    // TCPA-specific report required by FCC
    return this.generateComplianceReport({
      startDate,
      endDate,
      reportType: 'tcpa_full',
      format: 'pdf',
      includeFields: [
        'total_calls',
        'dnc_checks_completed',
        'dnc_matches_found',
        'consent_verified_count',
        'consent_missing_count',
        'opt_out_count',
        'calling_hours_compliance',
        'violation_summary',
        'scrub_api_calls',
        'list_refresh_dates',
        'consent_records_sample',
        'hash_chain_verification',
        'attestation_statement'
      ]
    });
  }

  async exportForRegulator(reportId) {
    const report = await this.complianceReport.findUnique({
      where: { id: reportId }
    });

    if (!report) throw new Error('Report not found');

    // Package report with supporting evidence
    const exportPackage = {
      report: report.data,
      hashChain: await this.exportHashChain(report.dateRange),
      eventSamples: await this.getEventSamples(report.dateRange),
      attestation: this.generateAttestation(report),
      metadata: {
        exportedAt: new Date().toISOString(),
        exportedBy: 'system',
        reportId: report.id,
        dataIntegrity: 'hash_chain_verified'
      }
    };

    // Sign the export package
    const packageSignature = this.signReport(JSON.stringify(exportPackage));
    exportPackage.signature = packageSignature;

    return exportPackage;
  }

  generateAttestation(report) {
    return {
      statement: `I hereby attest that the compliance data contained in this report is accurate, complete, and has been verified through cryptographic hash chain integrity checks. The compliance systems described herein were operational and properly configured during the reporting period.`,
      signedBy: 'Compliance Reporting System',
      signedAt: new Date().toISOString(),
      reportId: report.id,
      reportPeriod: report.dateRange,
      signature: this.signReport(JSON.stringify(report.dateRange))
    };
  }

  computeHash(data) {
    return crypto.createHash('sha256')
      .update(JSON.stringify(data, Object.keys(data).sort()))
      .digest('hex');
  }

  signEvent(hash) {
    const sign = crypto.createSign('RSA-SHA256');
    sign.update(hash);
    return sign.sign(this.privateKey, 'base64');
  }

  verifySignature(hash, signature) {
    const verify = crypto.createVerify('RSA-SHA256');
    verify.update(hash);
    return verify.verify(this.publicKey, signature, 'base64');
  }
}
```

## Integration Points

- **DNC Engine (sec-02):** DNC check results feed into compliance event store
- **Consent Tracking (sec-05):** Consent verification and opt-out events for audit trail
- **Campaign Scheduling (Ch 03):** Calling hours enforcement generates compliance events
- **Call Logging (Part 12):** Call outcome records linked to compliance events
- **Scrub API (sec-06):** Scrub results included in compliance reporting
- **Campaign Config (Ch 01):** Per-campaign compliance rule configuration
- **Retry Logic (Ch 04):** Retry count compliance validation
- **Analytics (Ch 09):** Compliance dashboard metrics and trend tracking

## Open-Source Tools

- **PostgreSQL (with append-only trigger):** Append-only compliance event store
- **node:crypto:** Hash chain computation, digital signatures, and verification
- **Grafana:** Real-time compliance monitoring dashboards
- **BullMQ:** Scheduled report generation and violation alert queues
- **Puppeteer / Playwright:** PDF report generation from HTML templates
- **Prometheus + Alertmanager:** Compliance violation alerting and metrics
- **OpenTelemetry:** Distributed compliance event tracing
- **csv-writer / exceljs:** CSV and Excel report export for regulators

## Production Considerations

- Compliance reports must be generated within 24 hours of a regulatory request (FCC requirement)
- Hash chain verification is mandatory before submitting any compliance report as legal evidence
- Violation detection should run in near real-time (<1 minute delay) for critical violations
- Compliance data retention: minimum 4 years for TCPA, 5 years for FDCPA, indefinite for litigation holds
- Access to compliance data must be logged and restricted to authorized compliance personnel only
- Compliance report templates must be version-controlled and any changes approved by legal counsel
- Automated report distribution to compliance team on scheduled cadence (daily, weekly, monthly)
- False positive violations should have a review workflow with documented disposition
- Compliance scorecard: track compliance rate by campaign, agent, and carrier for continuous improvement
- Third-party auditor access: provide read-only access to compliance data with full audit trail
- Regulatory filing formats vary by agency — support PDF, CSV, JSON, and XML exports
- Anomaly detection on compliance metrics: sudden drops in compliance rate may indicate system issues
- Compliance data lake storage costs are significant at scale — implement tiered storage (hot/warm/cold)
- Regular compliance report drills: simulate regulatory audit to verify report accuracy and timeliness
- Chain-of-custody documentation for compliance data: who accessed what data when and why
