# Section 08: Security & Compliance

## Overview

Webhook security protects both the platform and consumers from attacks. HTTPS enforcement, IP allowlisting, payload encryption, and comprehensive audit logging ensure compliance with security standards and regulations.

## Architecture

```
Security Layers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Event] → [Encryption] → [Transport] → [AuthN/Z] → [Consumer]
    │           │              │             │            │
Raw payload   AES-256-GCM   HTTPS/TLS    Signature      Receive
              encrypt       enforce      verification   + decrypt
              at rest       only          + IP allowlist

Security Controls:
  ┌──────────────────────┬─────────────────────────────┐
  │ Control              │ Implementation               │
  ├──────────────────────┼─────────────────────────────┤
  │ HTTPS Enforcement    │ Reject non-TLS endpoints     │
  │ IP Allowlisting      │ Optional consumer IP filter   │
  │ Payload Encryption   │ AES-256-GCM per-event key    │
  │ Audit Logging        │ All operations logged        │
  │ Data Retention       │ 90-day log retention         │
  │ Access Control       │ Tenant-scoped endpoint access │
  │ Rate Limiting        │ Per-endpoint rate limits      │
  │ Secret Rotation      │ Automated quarterly rotation  │
  └──────────────────────┴─────────────────────────────┘

Compliance Requirements:
  - SOC 2: Access controls, audit trails
  - GDPR: Data retention, deletion capabilities
  - HIPAA: Payload encryption (if handling PHI)
  - PCI DSS: Encryption of sensitive data
  - ISO 27001: Security controls documentation
```

## Design Decisions

- **Default-Deny IP Policy**: Allowlist required for sensitive data
- **Per-Event Encryption Keys**: Each payload encrypted with unique key
- **Immutable Audit Logs**: Write-once, read-many log storage
- **Automated Compliance Reports**: Generated monthly for audit

## Implementation Approach

```typescript
interface SecurityConfig {
  enforceHttps: boolean;
  ipAllowlist?: string[];
  payloadEncryption: boolean;
  encryptionAlgorithm: 'aes-256-gcm';
  auditLogRetentionDays: number;
  maxSecretsPerEndpoint: number;
  allowedSourceIps?: string[];
  requireClientCertificate?: boolean;
}

interface AuditEntry {
  id: string;
  action: 'create' | 'update' | 'delete' | 'rotate' | 'deliver' | 'test' | 'retry';
  resourceId: string;
  resourceType: 'endpoint' | 'secret' | 'event';
  tenantId: string;
  userId?: string;
  metadata: Record<string, unknown>;
  ipAddress: string;
  userAgent?: string;
  timestamp: Date;
}

class WebhookSecurityService {
  async encryptPayload(
    payload: Record<string, unknown>,
    key: Buffer,
  ): Promise<{ encrypted: Buffer; iv: Buffer; authTag: Buffer }> {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

    const json = JSON.stringify(payload);
    const encrypted = Buffer.concat([cipher.update(json, 'utf-8'), cipher.final()]);
    const authTag = cipher.getAuthTag();

    return { encrypted, iv, authTag };
  }

  async decryptPayload(
    encrypted: Buffer,
    key: Buffer,
    iv: Buffer,
    authTag: Buffer,
  ): Promise<Record<string, unknown>> {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);

    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
    return JSON.parse(decrypted.toString('utf-8'));
  }

  validateEndpoint(endpoint: WebhookEndpoint, config: SecurityConfig): ValidationResult {
    const errors: string[] = [];

    // HTTPS enforcement
    if (config.enforceHttps && !endpoint.url.startsWith('https://')) {
      errors.push('URL must use HTTPS protocol');
    }

    // IP Allowlisting
    if (config.ipAllowlist && config.ipAllowlist.length > 0) {
      // In production, extract IP from resolved endpoint URL
      const endpointHost = new URL(endpoint.url).hostname;
      const resolvedIps = this.resolveHostname(endpointHost);

      const allowed = resolvedIps.some(ip =>
        config.ipAllowlist!.some(allowed => this.ipInRange(ip, allowed))
      );

      if (!allowed) {
        errors.push(`Endpoint IP not in allowlist: ${resolvedIps.join(', ')}`);
      }
    }

    // URL scheme validation
    try {
      const parsed = new URL(endpoint.url);
      if (!['http:', 'https:'].includes(parsed.protocol)) {
        errors.push('Unsupported URL protocol');
      }
    } catch {
      errors.push('Invalid URL');
    }

    return { valid: errors.length === 0, errors };
  }

  private resolveHostname(hostname: string): string[] {
    // Use DNS resolution to get IP addresses
    // In production, use dns.resolve4 and dns.resolve6
    return [];
  }

  private ipInRange(ip: string, cidr: string): boolean {
    const [range, bits = '32'] = cidr.split('/');
    const mask = ~(2 ** (32 - parseInt(bits)) - 1);
    const ipNum = this.ipToNumber(ip);
    const rangeNum = this.ipToNumber(range);
    return (ipNum & mask) === (rangeNum & mask);
  }

  private ipToNumber(ip: string): number {
    return ip.split('.').reduce((acc, octet) => (acc << 8) + parseInt(octet), 0) >>> 0;
  }
}

class AuditLogger {
  private logStream: WriteStream;

  async log(action: AuditEntry): Promise<void> {
    const entry = {
      ...action,
      timestamp: new Date().toISOString(),
    };

    // Write to immutable log store (e.g., AWS CloudWatch, S3)
    await this.writeToImmutableStore(entry);

    // Also store in queryable database for dashboard
    await this.db.insert('audit_logs', entry);
  }

  private async writeToImmutableStore(entry: AuditEntry): Promise<void> {
    const logLine = JSON.stringify(entry) + '\n';
    // Append to write-once log file or stream
    this.logStream.write(logLine);
  }

  async queryAuditLogs(filters: AuditQuery): Promise<AuditEntry[]> {
    const query: any = {};
    if (filters.tenantId) query.tenantId = filters.tenantId;
    if (filters.action) query.action = filters.action;
    if (filters.resourceId) query.resourceId = filters.resourceId;
    if (filters.startDate || filters.endDate) {
      query.timestamp = {};
      if (filters.startDate) query.timestamp.$gte = new Date(filters.startDate);
      if (filters.endDate) query.timestamp.$lte = new Date(filters.endDate);
    }

    return this.db.find('audit_logs', query, {
      sort: { timestamp: -1 },
      limit: filters.limit || 100,
    });
  }

  async generateComplianceReport(startDate: Date, endDate: Date): Promise<ComplianceReport> {
    const logs = await this.queryAuditLogs({
      startDate: startDate.toISOString(),
      endDate: endDate.toISOString(),
      limit: 10000,
    });

    return {
      period: { start: startDate, end: endDate },
      totalEvents: logs.length,
      actionsByType: this.groupBy(logs, 'action'),
      uniqueEndpointsModified: [...new Set(logs.map(l => l.resourceId))].length,
      secretRotations: logs.filter(l => l.action === 'rotate').length,
      failedDeliveries: logs.filter(l => l.action === 'deliver' && l.metadata.status === 'failed').length,
      generatedAt: new Date(),
    };
  }
}
```

## Integration Points

- **Secret Store**: HashiCorp Vault or AWS KMS for key management
- **SIEM Integration**: Audit logs forwarded to security monitoring
- **Compliance Dashboard**: Automated report generation for auditors

## Production Considerations

- **Encryption Key Rotation**: Rotate encryption keys monthly
- **Audit Log Immutability**: Use append-only storage (e.g., S3 Object Lock)
- **Data Deletion**: GDPR compliance with per-tenant data deletion workflows
- **Penetration Testing**: Regular security testing of webhook infrastructure

## Open-Source Tools

- **Node.js crypto**: AES-256-GCM encryption
- **HashiCorp Vault**: Secret management and encryption keys
- **Winston**: Structured audit logging
