# MFA Compliance Requirements

## Overview

Multi-factor authentication is mandated by major compliance frameworks (SOC 2, HIPAA, PCI DSS) for accessing sensitive systems and data. This section maps MFA requirements across standards and provides implementation guidance for each.

## Compliance Framework Comparison

```
│ Requirement                │ SOC 2     │ HIPAA     │ PCI DSS   │ SOX       │
├────────────────────────────┼───────────┼───────────┼───────────┼───────────┤
│ MFA for Admin Access       │ Required  │ Required  │ Required  │ Required  │
│ MFA for All Users          │ Recommended│ Addressable│ N/A      │ N/A       │
│ MFA for Remote Access      │ Required  │ Required  │ Required  │ Required  │
│ Automated Enforcement      │ Required  │ Addressable│ Required  │ Recommended│
│ Regular Review of Access   │ Required  │ Required  │ Required  │ Required  │
│ MFA Audit Logging          │ Required  │ Required  │ Required  │ Required  │
│ Backup/Recovery MFA        │ Recommended│ Recommended│ Required  │ Recommended│
│ Hardware Token Support     │ N/A       │ N/A       │ Optional  │ N/A       │
```

## SOC 2 MFA Requirements

```typescript
interface Soc2ComplianceCheck {
  checkMfaForAdminAccess(): Promise<ComplianceResult> {
    // CC6.1: Logical and physical access controls
    const adminUsers = await this.userService.getUsersByRole('admin');
    const violations: string[] = [];

    for (const user of adminUsers) {
      const mfaState = await this.mfaService.getEnrollmentState(user.id);
      if (mfaState.enrollmentStatus !== 'completed') {
        violations.push(`Admin user ${user.email} has no MFA enrolled`);
      }
    }

    return {
      compliant: violations.length === 0,
      violations,
      standard: 'SOC 2 CC6.1',
      remediation: 'Enforce MFA for all administrative users',
    };
  }

  async checkMfaForRemoteAccess(): Promise<ComplianceResult> {
    // CC6.6: Remote access controls
    const remoteSessions = await this.sessionService.getActiveSessions({ isRemote: true });
    const violations: string[] = [];

    for (const session of remoteSessions) {
      if (!session.mfaVerified) {
        violations.push(`Remote session ${session.id} from ${session.ipAddress} lacks MFA`);
      }
    }

    return {
      compliant: violations.length === 0,
      violations,
      standard: 'SOC 2 CC6.6',
      remediation: 'Require MFA for all remote access sessions',
    };
  }
}
```

## HIPAA Technical Safeguards

```typescript
interface HipaaCompliance {
  // §164.312(d) - Person or Entity Authentication
  async checkHipaaMFA(): Promise<ComplianceResult[]> {
    return [
      await this.checkUniqueUserIdentification(),
      await this.checkEmergencyAccess(),
      await this.checkAutomaticLogoff(),
      await this.checkEncryptionAndDecryption(),
    ];
  }

  private async checkUniqueUserIdentification(): Promise<ComplianceResult> {
    // §164.312(a)(1) - Unique User Identification
    const usersWithoutMFA = await this.db.find('users', {
      mfaEnrolled: false,
      status: 'active',
    });

    return {
      compliant: usersWithoutMFA.length === 0,
      violations: usersWithoutMFA.map(u => `User ${u.id} missing unique identification via MFA`),
      standard: '45 CFR §164.312(a)(1)',
      remediation: 'Assign unique user IDs with MFA for all system users',
    };
  }

  private async checkEmergencyAccess(): Promise<ComplianceResult> {
    // §164.312(a)(2) - Emergency Access Procedure
    const emergencyProcedures = await this.getEmergencyAccessProcedures();

    return {
      compliant: emergencyProcedures.mfaBypassRequiresApproval,
      violations: emergencyProcedures.mfaBypassRequiresApproval ? [] : ['Emergency MFA bypass lacks approval workflow'],
      standard: '45 CFR §164.312(a)(2)',
      remediation: 'Implement emergency access procedure with post-event MFA verification',
    };
  }

  private async checkAutomaticLogoff(): Promise<ComplianceResult> {
    // §164.312(a)(3) - Automatic Logoff
    const sessionsWithoutTimeout = await this.sessionService.getSessionsExceedingIdleTime(15);

    return {
      compliant: sessionsWithoutTimeout.length === 0,
      violations: sessionsWithoutTimeout.map(s => `Session ${s.id} exceeds 15-minute idle timeout`),
      standard: '45 CFR §164.312(a)(3)',
      remediation: 'Implement 15-minute inactivity timeout for ePHI access',
    };
  }
}
```

## PCI DSS MFA Requirements

```typescript
interface PciCompliance {
  // Requirement 8.3: MFA for all non-console admin access
  async checkPciRequirement_8_3_1(): Promise<ComplianceResult> {
    // 8.3.1: MFA for administrative access to cardholder data environment
    const adminAccesses = await this.auditLog.search({
      action: 'admin_access',
      resource_type: 'cardholder_data',
      dateRange: { last: '30d' },
    });

    const noMfaAccesses = adminAccesses.filter(a => !a.mfaVerified);
    return {
      compliant: noMfaAccesses.length === 0,
      violations: noMfaAccesses.map(a => `Admin access ${a.id} without MFA`),
      standard: 'PCI DSS 8.3.1',
      severity: 'critical',
    };
  }

  // Requirement 8.3.2: MFA for remote network access
  async checkPciRequirement_8_3_2(): Promise<ComplianceResult> {
    const remoteAccesses = await this.sessionService.getSessions({ isRemote: true, last24h: true });
    const noMfaRemote = remoteAccesses.filter(s => !s.mfaVerified);

    return {
      compliant: noMfaRemote.length === 0,
      violations: noMfaRemote.map(s => `Remote access ${s.id} without MFA`),
      standard: 'PCI DSS 8.3.2',
      severity: 'critical',
    };
  }

  // Requirement 8.3.3: MFA for all access from untrusted networks
  async checkPciRequirement_8_3_3(): Promise<ComplianceResult> {
    const untrustedNetworks = await this.getUntrustedNetworkAccesses();
    const nonCompliant = untrustedNetworks.filter(a => !a.mfaVerified);

    return {
      compliant: nonCompliant.length === 0,
      violations: nonCompliant.map(a => `Access from untrusted network ${a.networkId} without MFA`),
      standard: 'PCI DSS 8.3.3',
      severity: 'critical',
    };
  }
}
```

## Compliance Monitoring Dashboard

```typescript
interface ComplianceDashboardData {
  overallScore: number;           // 0-100
  frameworkScores: {
    soc2: number;
    hipaa: number;
    pci: number;
  };
  violationsBySeverity: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  recentViolations: ComplianceViolation[];
  mfaAdoptionRate: number;        // Percentage of users enrolled
  mfaEnforcementRate: number;     // Percentage of sessions with MFA
  adminMfaCoverage: number;       // Admin users with MFA
  remoteAccessMfaRate: number;    // Remote sessions with MFA
}
```

## Automated Compliance Reporting

```typescript
class ComplianceReportGenerator {
  async generateMfaComplianceReport(tenantId: string, framework: string): Promise<Report> {
    const checks: ComplianceResult[] = [];

    switch (framework) {
      case 'soc2':
        checks.push(await this.soc2.checkMfaForAdminAccess());
        checks.push(await this.soc2.checkMfaForRemoteAccess());
        break;
      case 'hipaa':
        checks.push(...await this.hipaa.checkHipaaMFA());
        break;
      case 'pci':
        checks.push(await this.pci.checkPciRequirement_8_3_1());
        checks.push(await this.pci.checkPciRequirement_8_3_2());
        checks.push(await this.pci.checkPciRequirement_8_3_3());
        break;
    }

    const compliant = checks.every(c => c.compliant);
    const violations = checks.flatMap(c => c.violations);

    return {
      tenantId,
      framework,
      timestamp: new Date(),
      compliant,
      totalChecks: checks.length,
      passedChecks: checks.filter(c => c.compliant).length,
      failedChecks: checks.filter(c => !c.compliant).length,
      violations,
      remediations: checks
        .filter(c => !c.compliant)
        .map(c => ({ standard: c.standard, remediation: c.remediation })),
    };
  }
}
```

## Open-Source Tools

- **OpenSCAP** — Security compliance scanning
- **Wazuh** — Security monitoring and compliance

## Production Considerations

- Run compliance checks daily on a schedule and alert on violations
- Maintain audit trail of compliance check results for auditor review
- Allow configurable compliance requirements per tenant (multi-tenant SaaS)
- Generate compliance reports in PDF format for auditor submission
- Implement auto-remediation for common violations (e.g., force MFA enrollment)
- Track compliance drift over time with trend dashboards
- Store compliance check history for minimum of 3 years (per most frameworks)
