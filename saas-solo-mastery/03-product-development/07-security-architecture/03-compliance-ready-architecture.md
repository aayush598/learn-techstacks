# Building Compliance-Ready Architecture

## Compliance for Solo Founders

Compliance certifications (SOC 2, HIPAA, GDPR) are often required to sell to enterprise customers. But they're expensive and time-consuming to obtain. The key insight is that you can build your architecture to be "compliance-ready" — designed so that achieving certification later is a paperwork exercise, not a re-architecture project.

This guide covers how to design your SaaS architecture to meet SOC 2, HIPAA, and GDPR requirements from day one, with specific implementation patterns for each.

## The Compliance-Ready Philosophy

### What "Compliance-Ready" Means

```markdown
Compliance-ready ≠ Compliant

Compliance-ready means:
  - Your architecture supports the controls needed for compliance
  - You have the data and processes to prove compliance
  - You can pass an audit with minimal rework
  - You're not blocking enterprise deals due to compliance gaps

Compliance-ready does NOT mean:
  - You are certified (certification costs money and time)
  - You have implemented every control perfectly
  - You're ready for a federal audit

Build compliance-ready architecture from day 1.
Pursue certification when customers demand it.
```

### The Compliance Maturity Model

```markdown
Stage 1: None (MVP)
  - Basic security practices
  - No formal compliance
  - Sales to: Small businesses, individuals

Stage 2: Compliance-Ready (Growth)
  - Architecture supports compliance
  - Basic documentation
  - Self-assessment done
  - Sales to: Mid-market, startups with compliance needs

Stage 3: Self-Attestation (Scale)
  - SOC 2 Type I completed
  - GDPR compliant
  - Security questionnaire responses prepared
  - Sales to: Enterprises with basic compliance needs

Stage 4: Certified (Enterprise)
  - SOC 2 Type II
  - HIPAA (if needed)
  - ISO 27001 (if needed)
  - Sales to: Regulated industries, large enterprises
```

## SOC 2 Compliance

### What SOC 2 Requires

SOC 2 is based on five Trust Service Criteria:

```markdown
1. Security (Required)
   - Protected against unauthorized access
   - This is the only required criterion

2. Availability (Optional)
   - System is available for operation and use
   - Monitoring, incident response, disaster recovery

3. Processing Integrity (Optional)
   - Processing is complete, valid, accurate
   - Data validation, error handling

4. Confidentiality (Optional)
   - Information designated as confidential is protected
   - Encryption, access controls, data classification

5. Privacy (Optional)
   - Personal information is collected, used, retained, disclosed in accordance with commitments
   - Privacy notice, consent, access, correction

Most SaaS companies pursue Security + Confidentiality (Type II).
```

### SOC 2 Architecture Controls

```markdown
### Control Area 1: Logical & Physical Access
[ ] Authentication: MFA required for all system access
[ ] Authorization: Role-based access control (RBAC)
[ ] Password policy: 8+ chars, complexity, rotation
[ ] Session management: timeout, termination
[ ] API authentication: API keys with scoped permissions
[ ] Physical security: cloud provider SOC 2 (inherited)
[ ] Network security: firewalls, WAF, segmentation

Implementation:
  - Use Auth0/Clerk with MFA
  - Implement RBAC (already done in schema design)
  - Enforce password policies
  - Cloud provider inherits physical controls (AWS/GCP/Cloudflare SOC 2 reports)
```

```markdown
### Control Area 2: System Operations
[ ] Monitoring: 24/7 system monitoring
[ ] Incident response: documented process
[ ] Change management: documented change process
[ ] Backup & recovery: automated, tested
[ ] Capacity planning: monitored and documented

Implementation:
  - Sentry + Better Uptime for monitoring
  - Document your change process (even as solo founder)
  - Automated backups (already covered)
  - Quarterly restore testing
```

```markdown
### Control Area 3: Change Management
[ ] Code review: all changes reviewed
[ ] Testing: automated tests required for changes
[ ] Approval: changes approved before production
[ ] Deployment: automated, auditable
[ ] Emergency changes: documented process
[ ] Configuration management: documented

Implementation:
  - GitHub PRs (even if you self-review)
  - CI/CD pipeline (already covered)
  - Deployment tags/versions
  - Emergency change documentation template
```

```markdown
### Control Area 4: Risk Management
[ ] Risk assessment: annually
[ ] Vendor management: assess third-party risks
[ ] Security incident response: documented plan
[ ] Business continuity: documented plan
[ ] Disaster recovery: documented plan

Implementation:
  - Annual self-risk assessment
  - Vendor security assessment (check their SOC 2 reports)
  - Incident response runbook (covered in DevOps section)
  - Backup & restore procedure documented
```

### SOC 2 Evidence Collection

```typescript
// lib/compliance/soc2.ts
// Collect evidence for SOC 2 audits

class Soc2EvidenceCollector {
  async collectEvidence(period: { start: Date; end: Date }) {
    return {
      // 1. Access reviews
      accessReviews: await this.getAccessReviews(period),

      // 2. Change management
      changes: await this.getCodeChanges(period),
      deployments: await this.getDeployments(period),

      // 3. Monitoring
      incidents: await this.getIncidents(period),
      uptimeReports: await this.getUptimeReports(period),

      // 4. Backups
      backupVerifications: await this.getBackupVerifications(period),

      // 5. Security training
      trainingRecords: await this.getTrainingRecords(period),

      // 6. Vendor reviews
      vendorAssessments: await this.getVendorAssessments(period),
    };
  }

  private async getAccessReviews(period: { start: Date; end: Date }) {
    return db.query(
      `SELECT * FROM access_reviews
       WHERE review_date BETWEEN $1 AND $2
       ORDER BY review_date DESC`,
      [period.start, period.end]
    );
  }

  private async getCodeChanges(period: { start: Date; end: Date }) {
    // GitHub API: get all PRs merged in period
    const response = await fetch(
      `https://api.github.com/repos/${process.env.GITHUB_REPO}/pulls?state=closed&sort=updated&direction=desc`,
      {
        headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` },
      }
    );
    const pulls = await response.json();
    return pulls
      .filter((p: any) => p.merged_at && new Date(p.merged_at) >= period.start)
      .map((p: any) => ({
        id: p.number,
        title: p.title,
        author: p.user.login,
        mergedAt: p.merged_at,
        url: p.html_url,
        reviewers: p.requested_reviewers.map((r: any) => r.login),
      }));
  }

  private async getDeployments(period: { start: Date; end: Date }) {
    return db.query(
      `SELECT * FROM deployment_logs
       WHERE deployed_at BETWEEN $1 AND $2
       ORDER BY deployed_at DESC`,
      [period.start, period.end]
    );
  }

  private async getIncidents(period: { start: Date; end: Date }) {
    return db.query(
      `SELECT * FROM incidents
       WHERE created_at BETWEEN $1 AND $2
       ORDER BY created_at DESC`,
      [period.start, period.end]
    );
  }

  private async getBackupVerifications(period: { start: Date; end: Date }) {
    return db.query(
      `SELECT * FROM backup_verifications
       WHERE verified_at BETWEEN $1 AND $2
       ORDER BY verified_at DESC`,
      [period.start, period.end]
    );
  }
}
```

## HIPAA Compliance

### What HIPAA Requires

```markdown
HIPAA applies if you handle Protected Health Information (PHI).

Requirements:
1. Administrative Safeguards
   - Risk analysis
   - Risk management
   - Sanction policy
   - Information system activity review

2. Physical Safeguards (if applicable)
   - Facility access controls
   - Workstation security

3. Technical Safeguards
   - Access control (unique user IDs, emergency access, automatic logoff)
   - Audit controls (record and examine activity)
   - Integrity controls (PHI not improperly altered)
   - Person or entity authentication
   - Transmission security

4. Policies & Procedures
   - Documentation
   - Retention (6 years)
```

### HIPAA Architecture Requirements

```markdown
## Technical Safeguards Implementation

### 1. Access Control
[ ] Unique user identification: every user has unique ID
[ ] Emergency access: break-glass procedure
[ ] Automatic logoff: 15 minutes of inactivity
[ ] Encryption and decryption: AES-256 for PHI

### 2. Audit Controls
[ ] Log all access to PHI
[ ] Log all modifications to PHI
[ ] Log all deletions of PHI
[ ] Audit logs are immutable
[ ] Audit logs retained for 6 years

### 3. Integrity Controls
[ ] PHI is encrypted at rest and in transit
[ ] Electronic signatures for modifications
[ ] Checksums/ hashes for data integrity
[ ] Version history for PHI records

### 4. Transmission Security
[ ] TLS 1.2+ for all data in transit
[ ] VPN for internal access (if self-hosted)
[ ] Message integrity checks
```

### HIPAA-Compliant Audit Logging

```sql
-- HIPAA requires detailed, immutable audit logs
-- Use append-only table design

CREATE TABLE hipaa_audit_log (
  id BIGSERIAL PRIMARY KEY,
  event_type VARCHAR(50) NOT NULL,
  -- created, read, updated, deleted, exported, viewed
  user_id UUID NOT NULL,
  user_role VARCHAR(50),
  ip_address INET NOT NULL,
  user_agent TEXT,
  resource_type VARCHAR(100) NOT NULL, -- 'patient_record', 'prescription'
  resource_id UUID NOT NULL,
  phi_accessed BOOLEAN NOT NULL DEFAULT false,
  fields_accessed TEXT[], -- Which PHI fields were accessed
  changes JSONB, -- For modifications: what changed
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Immutable record
  record_hash VARCHAR(64) NOT NULL, -- SHA-256 of this record
  previous_record_hash VARCHAR(64), -- Chain for integrity
  CONSTRAINT fk_previous_hash FOREIGN KEY (previous_record_hash) REFERENCES hipaa_audit_log(record_hash)
);
```

```typescript
// lib/compliance/hipaa-audit.ts

import { createHash } from 'crypto';

class HipaaAuditLogger {
  private previousHash: string | null = null;

  async logAccess(params: {
    userId: string;
    userRole: string;
    ip: string;
    userAgent?: string;
    resourceType: string;
    resourceId: string;
    phiAccessed: boolean;
    fieldsAccessed?: string[];
    changes?: Record<string, any>;
  }) {
    const record = {
      event_type: 'access',
      user_id: params.userId,
      user_role: params.userRole,
      ip_address: params.ip,
      user_agent: params.userAgent,
      resource_type: params.resourceType,
      resource_id: params.resourceId,
      phi_accessed: params.phiAccessed,
      fields_accessed: params.fieldsAccessed,
      changes: params.changes,
      timestamp: new Date().toISOString(),
      previous_record_hash: this.previousHash,
    };

    // Generate hash for this record
    const recordString = JSON.stringify(record);
    record.record_hash = createHash('sha256')
      .update(recordString)
      .digest('hex');

    // Store in database (INSERT only, no UPDATE or DELETE)
    await db.query(
      `INSERT INTO hipaa_audit_log
       (event_type, user_id, user_role, ip_address, user_agent,
        resource_type, resource_id, phi_accessed, fields_accessed,
        changes, record_hash, previous_record_hash)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)`,
      [record.event_type, record.user_id, record.user_role,
       record.ip_address, record.user_agent, record.resource_type,
       record.resource_id, record.phi_accessed, record.fields_accessed,
       JSON.stringify(record.changes || {}),
       record.record_hash, record.previous_record_hash]
    );

    this.previousHash = record.record_hash;
  }

  async verifyIntegrity(): Promise<{
    valid: boolean;
    brokenChains: number;
  }> {
    const records = await db.query(
      'SELECT * FROM hipaa_audit_log ORDER BY id ASC'
    );

    let brokenChains = 0;
    let expectedHash: string | null = null;

    for (const record of records.rows) {
      // Verify hash
      const recordData = { ...record };
      const storedHash = recordData.record_hash;
      delete recordData.record_hash;

      const computedHash = createHash('sha256')
        .update(JSON.stringify(recordData))
        .digest('hex');

      if (computedHash !== storedHash) {
        brokenChains++;
      }

      // Verify chain
      if (recordData.previous_record_hash !== expectedHash) {
        brokenChains++;
      }

      expectedHash = storedHash;
    }

    return {
      valid: brokenChains === 0,
      brokenChains,
    };
  }
}

export const hipaaAudit = new HipaaAuditLogger();
```

### HIPAA BAAs (Business Associate Agreements)

```typescript
// lib/compliance/hipaa-baa.ts
// Track Business Associate Agreements

interface BusinessAssociate {
  name: string;
  service: string;
  hasBAA: boolean;
  baASignedDate?: Date;
  baaExpiryDate?: Date;
  phiShared: string[]; // What PHI do they access
}

const businessAssociates: BusinessAssociate[] = [
  {
    name: 'AWS',
    service: 'Cloud Infrastructure',
    hasBAA: true,
    baASignedDate: new Date('2024-01-01'),
    phiShared: ['Storage', 'Database Hosting'],
  },
  {
    name: 'Sentry',
    service: 'Error Monitoring',
    hasBAA: false,
    phiShared: ['None - error data only'],
  },
  // ...
];

function checkBAAs() {
  const missingBAA = businessAssociates.filter(ba => !ba.hasBAA);
  const expiredBAA = businessAssociates.filter(
    ba => ba.baaExpiryDate && ba.baaExpiryDate < new Date()
  );

  if (missingBAA.length > 0) {
    console.log('⚠️  Missing BAAs:', missingBAA.map(b => b.name));
  }

  if (expiredBAA.length > 0) {
    console.log('⚠️  Expired BAAs:', expiredBAA.map(b => b.name));
  }
}
```

### HIPAA-Capable Infrastructure

```markdown
Cloud providers with HIPAA eligibility:

1. AWS (BAA available)
   - Services: EC2, RDS, S3, CloudFront
   - Requires: PHI only in HIPAA-eligible services
   - BAA: Included in AWS Artifact

2. Google Cloud (BAA available)
   - Services: Compute Engine, Cloud SQL, Cloud Storage
   - BAA: Included in Google Cloud compliance

3. Azure (BAA available)
   - Services: VMs, SQL Database, Blob Storage
   - BAA: Included in Azure compliance

4. Cloudflare (BAA not available for all services)
   - CDN, DNS, DDoS protection — no PHI stored here

5. Supabase (BAA available on Team plan)
   - Database hosting with PHI
   - Required: self-host or use their HIPAA plan
```

## GDPR Compliance

### What GDPR Requires

```markdown
### Key Principles
1. Lawfulness, fairness, and transparency
2. Purpose limitation
3. Data minimization
4. Accuracy
5. Storage limitation
6. Integrity and confidentiality (security)
7. Accountability

### Data Subject Rights
- Right to be informed
- Right of access
- Right to rectification
- Right to erasure (right to be forgotten)
- Right to restrict processing
- Right to data portability
- Right to object
- Rights related to automated decision-making

### GDPR Applies If:
- You offer goods/services to EU residents
- You monitor behavior of EU residents
- Even if you're based outside the EU
```

### GDPR Architecture Requirements

```markdown
## Technical Implementation

### 1. Consent Management
[ ] Clear opt-in for all data collection
[ ] Granular consent categories
[ ] Consent records stored with timestamps
[ ] Easy withdrawal of consent
[ ] No pre-ticked boxes
```

```sql
-- Consent tracking
CREATE TABLE consent_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  consent_type VARCHAR(100) NOT NULL, -- 'marketing', 'analytics', 'cookies'
  status VARCHAR(20) NOT NULL, -- 'granted', 'withdrawn'
  ip_address INET,
  user_agent TEXT,
  granted_at TIMESTAMPTZ DEFAULT NOW(),
  withdrawn_at TIMESTAMPTZ
);

CREATE TABLE consent_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  is_required BOOLEAN DEFAULT false, -- Required for service delivery
  sort_order INTEGER DEFAULT 0
);
```

```typescript
// lib/compliance/gdpr-consent.ts

class GDPRConsentService {
  async recordConsent(params: {
    userId: string;
    consentType: string;
    granted: boolean;
    ip: string;
    userAgent?: string;
  }) {
    if (params.granted) {
      await db.query(
        `INSERT INTO consent_records (user_id, consent_type, status, ip_address, user_agent)
         VALUES ($1, $2, 'granted', $3, $4)`,
        [params.userId, params.consentType, params.ip, params.userAgent]
      );
    } else {
      await db.query(
        `UPDATE consent_records
         SET status = 'withdrawn', withdrawn_at = NOW()
         WHERE user_id = $1 AND consent_type = $2 AND status = 'granted'`,
        [params.userId, params.consentType]
      );
    }
  }

  async getConsentStatus(userId: string, consentType: string) {
    const result = await db.query(
      `SELECT status FROM consent_records
       WHERE user_id = $1 AND consent_type = $2
       ORDER BY granted_at DESC
       LIMIT 1`,
      [userId, consentType]
    );

    return result.rows[0]?.status || 'not_collected';
  }

  async hasConsent(userId: string, consentType: string): Promise<boolean> {
    const status = await this.getConsentStatus(userId, consentType);
    return status === 'granted';
  }
}

export const gdprConsent = new GDPRConsentService();
```

```markdown
### 2. Right to Erasure (Right to be Forgotten)

Implementation:
[ ] Anonymize or delete all personal data
[ ] Maintain audit trail (anonymized)
[ ] Cascade deletes to third-party services
[ ] 30-day response window
[ ] Verification of identity before processing
```

```typescript
// lib/compliance/gdpr-erasure.ts

class GDPRDataErasure {
  async deleteUserData(userId: string): Promise<void> {
    const client = await pool.connect();

    try {
      await client.query('BEGIN');

      // 1. Anonymize user record (keep for audit, but remove identity)
      await client.query(
        `UPDATE users SET
           email = 'deleted-' || id || '@deleted.com',
           name = 'Deleted User',
           password_hash = NULL,
           avatar_url = NULL,
           metadata = '{}'::jsonb,
           deleted_at = NOW()
         WHERE id = $1`,
        [userId]
      );

      // 2. Delete personal data from all tables
      const tables = [
        'profiles', 'sessions', 'api_keys',
        'consent_records', 'support_tickets',
      ];

      for (const table of tables) {
        await client.query(
          `DELETE FROM ${table} WHERE user_id = $1`,
          [userId]
        );
      }

      // 3. Anonymize but keep analytics data
      await client.query(
        `UPDATE analytics_events SET
           user_id = 'deleted',
           metadata = '{}'::jsonb
         WHERE user_id = $1`,
        [userId]
      );

      // 4. Log the erasure request (audit trail)
      await client.query(
        `INSERT INTO data_erasure_log
         (user_id, requested_at, completed_at)
         VALUES ($1, NOW(), NOW())`,
        [userId]
      );

      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }

    // 5. Notify third-party services
    await this.notifyThirdParties(userId);

    // 6. Send confirmation to user
    await sendEmail({
      to: 'deleted@deleted.com', // Can't email after erasure
      // Actually, the email is already anonymized.
      // Log the erasure, user doesn't get email confirmation.
    });
  }

  private async notifyThirdParties(userId: string) {
    // Stripe: can't delete customer with transactions
    // Instead, update email to deleted@
    // await stripe.customers.update(customerId, { email: 'deleted@deleted.com' });

    // Email service: remove from lists
    // await resend.contacts.remove({ email: oldEmail });

    // Analytics: anonymize
    // await posthog.personDelete(userId);
  }
}
```

```markdown
### 3. Data Portability

[ ] Export user data in machine-readable format (JSON)
[ ] Include all personal data
[ ] Include all user-generated content
[ ] Download available without authentication (secure link)
[ ] 30-day response window
```

```typescript
// lib/compliance/gdpr-portability.ts

class GDPRDataPortability {
  async exportUserData(userId: string): Promise<{
    profile: any;
    content: any;
    activity: any;
    billing: any;
  }> {
    const [profile, content, activity, billing] = await Promise.all([
      // 1. Profile data
      db.query(
        `SELECT email, name, created_at
         FROM users WHERE id = $1`,
        [userId]
      ),

      // 2. User content
      db.query(
        `SELECT id, title, content, created_at
         FROM projects WHERE user_id = $1`,
        [userId]
      ),

      // 3. Activity data
      db.query(
        `SELECT action, resource_type, created_at
         FROM audit_logs WHERE actor_id = $1
         ORDER BY created_at DESC
         LIMIT 1000`,
        [userId]
      ),

      // 4. Billing data
      db.query(
        `SELECT amount_cents, currency, status, created_at
         FROM invoices WHERE user_id = $1
         ORDER BY created_at DESC`,
        [userId]
      ),
    ]);

    return {
      exported_at: new Date().toISOString(),
      profile: profile.rows[0],
      content: content.rows,
      activity: activity.rows,
      billing: billing.rows,
    };
  }

  async createDownloadLink(
    userId: string,
    data: any
  ): Promise<string> {
    // Generate a secure, time-limited download link
    const token = crypto.randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 days

    await db.query(
      `INSERT INTO data_export_tokens
       (user_id, token, data, expires_at)
       VALUES ($1, $2, $3, $4)`,
      [userId, token, JSON.stringify(data), expiresAt]
    );

    return `${process.env.APP_URL}/api/export/download?token=${token}`;
  }
}
```

```markdown
### 4. Data Processing Records

[ ] Maintain record of all data processing activities
[ ] Document: purpose, categories, recipients, retention
[ ] Review and update regularly
[ ] Available for regulatory inspection
```

```sql
-- Data processing activity records
CREATE TABLE data_processing_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  activity_name VARCHAR(255) NOT NULL,
  purpose TEXT NOT NULL,
  data_categories TEXT[] NOT NULL,
  legal_basis VARCHAR(100) NOT NULL,
  -- 'consent', 'contract', 'legal_obligation', 'vital_interests', 'public_task', 'legitimate_interests'
  data_subjects TEXT[] NOT NULL, -- 'customers', 'employees', etc.
  retention_period VARCHAR(100),
  recipients TEXT[], -- Third parties who receive this data
  transfer_mechanisms TEXT[], -- For international transfers
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Universal Compliance Controls

### Controls That Apply to All Frameworks

```markdown
These controls are required by SOC 2, HIPAA, and GDPR:

### 1. Access Control
[ ] Unique user IDs
[ ] Role-based access
[ ] Principle of least privilege
[ ] Access review (quarterly)
[ ] Termination of access on departure

### 2. Audit Logging
[ ] Log all access to sensitive data
[ ] Log all changes to sensitive data
[ ] Immutable logs
[ ] Log monitoring and alerting
[ ] Log retention (6 years for HIPAA, 3 for SOC 2)

### 3. Encryption
[ ] Data in transit: TLS 1.2+
[ ] Data at rest: AES-256
[ ] Key management: cloud KMS or environment vars
[ ] Encryption of backups

### 4. Incident Response
[ ] Documented incident response plan
[ ] Defined severity levels
[ ] Notification procedures
[ ] Post-incident review
[ ] Regular testing of incident response

### 5. Business Continuity
[ ] Documented backup procedures
[ ] Regular backup testing (quarterly)
[ ] Disaster recovery plan
[ ] RPO/RTO defined
[ ] Plan testing annually

### 6. Vendor Management
[ ] Inventory of all vendors
[ ] Security assessment of vendors
[ ] Contracts with security requirements
[ ] BAAs where required (HIPAA)
[ ] Regular vendor review (annually)
```

## Compliance Documentation Templates

### Data Flow Diagram

```markdown
# Data Flow Diagram: User Registration

## Data Collected:
- Email address
- Name
- Password (hashed)
- IP address
- Browser user agent

## Data Flow:
1. User submits registration form
2. Frontend sends to API (TLS encrypted)
3. API validates and creates user record
4. Password hashed with bcrypt before storage
5. User record stored in PostgreSQL (encrypted at rest)
6. Welcome email sent via Resend (TLS encrypted)
7. Audit log entry created
8. Analytics event sent to PostHog (anonymized)

## Data Storage:
- Primary: PostgreSQL database (AWS RDS, encrypted at rest)
- Cache: Redis (transient, no PII)
- Logs: Axiom (structured logs, PII excluded)
- Email: Resend (transactional only, deleted after 90 days)

## Data Access:
- Application servers: via database connection (encrypted)
- Admin (you): via database client (authenticated, audited)
- Third parties: None have direct database access

## Data Retention:
- User accounts: until deletion request
- Audit logs: 6 years
- Analytics: 26 months (rolling window)
- Email logs: 90 days
```

### Security Policy Template

```markdown
# Security Policy
Version: 1.0
Date: [Date]

## 1. Purpose
This document outlines the security policies for [Product Name].

## 2. Scope
This policy applies to all systems, data, and personnel
associated with [Product Name].

## 3. Access Control
3.1 All users must have unique credentials
3.2 Access is granted on principle of least privilege
3.3 Access reviews are conducted quarterly
3.4 MFA is required for administrative access
3.5 Access is revoked immediately upon termination

## 4. Data Classification
4.1 Public: Marketing materials, blog posts
4.2 Internal: Business plans, internal communications
4.3 Confidential: Customer data, API keys, credentials
4.4 Restricted: Payment data, PHI (if applicable)

## 5. Data Protection
5.1 All data in transit encrypted with TLS 1.2+
5.2 All data at rest encrypted with AES-256
5.3 Encryption keys stored separately from data
5.4 Backups encrypted and stored in separate location

## 6. Incident Response
6.1 Incidents categorized as Critical, High, Medium, Low
6.2 Critical incidents: response within 15 minutes
6.3 High incidents: response within 1 hour
6.4 Medium incidents: response within 24 hours
6.5 Low incidents: response within 72 hours

## 7. Change Management
7.1 All code changes require pull request
7.2 All changes must pass automated tests
7.3 Production deployments require CI/CD pipeline
7.4 Emergency changes documented within 24 hours

## 8. Vendor Management
8.1 All vendors assessed for security posture
8.2 SOC 2 reports reviewed for critical vendors
8.3 BAAs in place for PHI (HIPAA only)
8.4 Vendor contracts include security requirements

## 9. Compliance
9.1 Security controls reviewed quarterly
9.2 Penetration testing conducted annually
9.3 Risk assessment conducted annually
9.4 Security awareness training completed annually

## 10. Enforcement
Violations of this policy may result in:
- Revocation of access
- Termination of employment (if applicable)
- Legal action (if warranted)
```

## Compliance Automation

### Compliance Dashboard

```typescript
// lib/compliance/dashboard.ts

interface ComplianceStatus {
  framework: string;
  status: 'compliant' | 'partial' | 'non_compliant';
  controls: {
    total: number;
    passed: number;
    failed: number;
    not_applicable: number;
  };
  lastAssessment: Date;
  nextAssessment: Date;
}

class ComplianceDashboard {
  async getStatus(): Promise<ComplianceStatus[]> {
    const frameworks = [
      { name: 'SOC 2', controlsFile: './controls/soc2.json' },
      { name: 'HIPAA', controlsFile: './controls/hipaa.json' },
      { name: 'GDPR', controlsFile: './controls/gdpr.json' },
    ];

    const statuses: ComplianceStatus[] = [];

    for (const framework of frameworks) {
      const controls = await this.loadControls(framework.controlsFile);
      const results = await this.evaluateControls(controls);

      statuses.push({
        framework: framework.name,
        status: this.overallStatus(results),
        controls: {
          total: controls.length,
          passed: results.filter(r => r.passed).length,
          failed: results.filter(r => !r.passed).length,
          not_applicable: controls.filter(c => !c.applicable).length,
        },
        lastAssessment: await this.getLastAssessment(framework.name),
        nextAssessment: await this.getNextAssessment(framework.name),
      });
    }

    return statuses;
  }

  private async evaluateControls(controls: Control[]) {
    return Promise.all(
      controls.map(async (control) => {
        if (!control.applicable) {
          return { control: control.id, passed: true, skipped: true };
        }

        const passed = await this.evaluateControl(control);
        return { control: control.id, passed };
      })
    );
  }

  private async evaluateControl(control: Control): Promise<boolean> {
    switch (control.type) {
      case 'header':
        return this.checkHeader(control.value);
      case 'config':
        return this.checkConfig(control.value);
      case 'log':
        return this.checkLogExists(control.value);
      case 'process':
        return this.checkDocumentExists(control.value);
      default:
        return false;
    }
  }

  private overallStatus(results: Array<{ passed: boolean }>): 'compliant' | 'partial' | 'non_compliant' {
    const passed = results.filter(r => r.passed).length;
    const total = results.length;

    if (passed === total) return 'compliant';
    if (passed >= total * 0.7) return 'partial';
    return 'non_compliant';
  }
}
```

## Compliance Timeline for Solo Founders

```markdown
### Month 1-3: Foundation
[ ] Implement security headers and HTTPS
[ ] Set up audit logging (basic)
[ ] Implement RBAC
[ ] Data encryption at rest and in transit
[ ] Password hashing with bcrypt
[ ] Document architecture and data flows

### Month 4-6: Compliance-Ready Architecture
[ ] Consent management (GDPR)
[ ] Data deletion functionality (right to erasure)
[ ] Data export functionality (data portability)
[ ] Comprehensive audit logging
[ ] Session management with timeout
[ ] Rate limiting on all endpoints

### Month 7-12: Documentation
[ ] Incident response plan
[ ] Change management process
[ ] Backup and recovery procedures
[ ] Vendor management program
[ ] Security policies
[ ] Risk assessment

### Year 2: Self-Attestation (if needed)
[ ] SOC 2 Type I readiness assessment
[ ] Address gaps from readiness assessment
[ ] Complete security questionnaires
[ ] Prepare evidence collection

### Year 3+: Certification (if needed)
[ ] Engage SOC 2 auditor ($10-30k)
[ ] Engage HIPAA compliance consultant (if needed)
[ ] Formal penetration test ($5-15k)
[ ] Implement remaining controls
[ ] Certification audit
```

## Compliance Cost Estimate

```markdown
| Phase               | Cost               | Time               | When              |
|---------------------|--------------------|--------------------|--------------------|
| Compliance-Ready    | $0-500 (tools)    | 20-40 hours        | Month 1-6         |
| Self-Assessment     | $0                | 10-20 hours        | Year 1            |
| SOC 2 Type I        | $10-30k           | 3-6 months         | Year 2+           |
| SOC 2 Type II       | $15-40k           | 6-12 months        | Year 2-3+         |
| HIPAA Assessment    | $5-20k            | 2-4 months         | If handling PHI   |
| Penetration Test    | $5-15k            | 2-4 weeks          | Before audit      |
| Compliance Software | $0-5k/year        | Ongoing            | Ongoing           |
| Legal Review        | $2-10k            | 1-2 weeks          | GDPR readiness    |
```

## Summary

Building a compliance-ready architecture is about making smart choices today that prevent expensive rework tomorrow. Key principles:

1. **Start with security fundamentals** — Most compliance requirements are just good security practices
2. **Design for audit from day one** — Log everything, document processes, maintain evidence
3. **Use cloud provider compliance** — Inherit their SOC 2/HIPAA compliance (AWS, GCP)
4. **Be privacy-conscious by default** — Data minimization, consent, right to deletion
5. **Document as you go** — Write policies when you implement controls, not during the audit
6. **Don't certify too early** — Self-attestation is often sufficient for mid-market deals
7. **Use managed services with compliance** — Clerk, Stripe, Sentry all have compliance certifications
8. **Automate compliance checks** — Use your CI/CD pipeline to verify controls
9. **Think about data retention** — Delete data you don't need (applies to all frameworks)
10. **Compliance is a journey** — You don't need to be certified on day 1, but you should be building toward it

The goal is to make certification a documentation exercise, not a re-architecture crisis. Build with compliance in mind, certify when customers demand it, and use your compliance-ready architecture as a competitive advantage in sales.
