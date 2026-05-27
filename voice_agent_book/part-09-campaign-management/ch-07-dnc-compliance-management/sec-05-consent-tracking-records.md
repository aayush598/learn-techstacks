# Section 05: Consent Tracking & Records

## Overview

Consent tracking is the systematic capture, storage, and management of consumer permission to be called. Under TCPA and similar regulations worldwide, a business must have documented proof of consent before placing telemarketing calls. Consent can be explicit (written agreement, electronic signature, verbal confirmation) or implied (existing business relationship, inquiry within the last 3 months), and different consent types have different regulatory standing. The consent tracking system must record not just whether consent exists, but the full context: who gave consent, when, through what channel, what was agreed to, and any expiration conditions.

A robust consent management system is the first line of defense against TCPA litigation. Courts have awarded statutory damages of $500-$1,500 per violation (trebled for willful violations), making consent documentation a high-stakes compliance requirement. The system must maintain immutable consent records, support consent withdrawal (opt-out) with immediate effect, and provide audit-ready consent reports. Modern consent tracking integrates with CRM systems, web forms, IVR prompts, and SMS opt-in flows to capture consent at every touchpoint.

## Architecture

```
                   Consent Tracking & Records System

  +--------------+   +------------+   +-------------+   +-----------+
  | Web Form     |   | IVR Opt-In |   | SMS Keyword |   | API/CRM   |
  | Opt-In       |   | Recording  |   | (e.g. JOIN) |   | Import    |
  +------+-------+   +-----+------+   +------+------+   +-----+-----+
         |                 |                  |                 |
         v                 v                  v                 v
  +---------------------------------------------------------------+
  |                  Consent Capture Pipeline                      |
  |                                                                |
  |  1. Validate (phone, identity, consent type)                   |
  |  2. Record metadata (source, timestamp, IP, user agent)        |
  |  3. Store proof (recording, screenshot, signed doc)            |
  |  4. Create consent record (immutable, timestamped)             |
  |  5. Update DNC exception list (consent overrides DNC)          |
  |  6. Confirm to consumer (SMS, email, or in-call confirmation)  |
  +---------------------------+------------------------------------+
                              |
                              v
  +---------------------------------------------------------------+
  |                   Consent Database                             |
  |                                                                |
  |  consent_id | phone  | type   | source  | ts        | expires | 
  |  -----------+--------+--------+---------+-----------+---------|
  |  c001       | +1415  | explicit| web    | 2025-01-01| NULL    |
  |  c002       | +1416  | implied| ivr     | 2025-02-15| 2025-05-15|
  |  c003       | +1417  | written| api     | 2025-03-01| 2026-03-01|
  |  c004       | +1418  | withdrawn| sms   | 2025-03-10| NULL    |
  +---------------------------------------------------------------+
                              |
                              v
  +---------------------------------------------------------------+
  |              Consent Verification API                          |
  |                                                                |
  |  Pre-dial: check_consent(phone, campaign) →                   |
  |    {has_consent: bool, consent_type, expires_at, proof_ref}   |
  |                                                                |
  |  Post-dial: record_call_under_consent(phone, call_sid) →      |
  |    links call record to consent record for audit               |
  +---------------------------------------------------------------+
```

## Design Decisions

- **Immutable consent records with hash chaining:** Consent records use a blockchain-inspired hash chain where each record references the previous record's hash. Any tampering with historical records breaks the chain and is detectable. Trade-off: storage/indexing overhead vs. indisputable audit trail for litigation defense.

- **Consent proof storage in object storage:** Proof of consent (recordings, screenshots, signed documents) is stored in S3-compatible object storage with pre-signed URL access. The database stores proof references, not binary data. Trade-off: additional infrastructure dependency vs. database performance and cost optimization.

- **Consent type hierarchy with priority rules:** Explicit consent overrides implied consent; written consent overrides verbal consent. The priority system ensures the highest-validity consent type is always used for compliance decisions. Trade-off: rule complexity vs. clear consent authority for regulatory defense.

- **Consent withdrawal with propagation delay:** Opt-out requests take effect immediately in the consent database, with a propagation delay of up to 24 hours for third-party DNC lists. During the propagation window, the system adds an internal suppression entry to prevent calls immediately. Trade-off: immediate internal suppression vs. technical limitations of third-party list updates.

## Implementation Approach

```
interface ConsentRecord {
  id: string;
  phoneNumber: string;     // E.164 format
  consentType: ConsentType; // explicit | implied | written | withdrawn
  source: ConsentSource;    // web_form | ivr | sms | api | crm_import
  capturedAt: Date;
  expiresAt: Date | null;
  campaignId: string | null;
  brandId: string;
  proofReference: string;   // S3 object key
  metadata: Record<string, any>;
  previousHash: string;     // Hash chain linkage
  currentHash: string;
  signature: string;        // Digital signature for non-repudiation
}

enum ConsentType {
  EXPLICIT_WRITTEN,
  EXPLICIT_ELECTRONIC,
  EXPLICIT_VERBAL,
  IMPLIED_BUSINESS_RELATIONSHIP,
  IMPLIED_INQUIRY,
  WITHDRAWN,
  EXPIRED
}

enum ConsentSource {
  WEB_FORM,
  IVR_OPT_IN,
  SMS_KEYWORD,
  API_IMPORT,
  CRM_SYNC,
  MOBILE_APP,
  IN_CALL_CONFIRMATION
}

class ConsentTrackingService {
  constructor(storage, hashChain, dncService) {
    this.storage = storage; // S3-compatible object storage
    this.hashChain = hashChain;
    this.dncService = dncService;
    this.consentPriority = {
      [ConsentType.EXPLICIT_WRITTEN]: 10,
      [ConsentType.EXPLICIT_ELECTRONIC]: 9,
      [ConsentType.EXPLICIT_VERBAL]: 8,
      [ConsentType.IMPLIED_BUSINESS_RELATIONSHIP]: 5,
      [ConsentType.IMPLIED_INQUIRY]: 3
    };
  }

  async captureConsent(request) {
    const {
      phoneNumber,
      consentType,
      source,
      proofData,
      campaignId,
      metadata
    } = request;

    // 1. Validate the phone number
    const normalizedPhone = this.validatePhone(phoneNumber);

    // 2. Validate consent type against source
    this.validateConsentSource(consentType, source);

    // 3. Store proof of consent
    const proofRef = await this.storeProof(consentType, proofData);

    // 4. Create hash chain entry
    const lastHash = await this.hashChain.getLastHash(normalizedPhone);
    const currentHash = this.computeHash({
      phone: normalizedPhone,
      type: consentType,
      timestamp: new Date().toISOString(),
      previousHash: lastHash
    });

    // 5. Build consent record
    const record = {
      id: this.generateId(),
      phoneNumber: normalizedPhone,
      consentType,
      source,
      capturedAt: new Date(),
      expiresAt: this.computeExpiry(consentType, campaignId),
      campaignId,
      brandId: metadata?.brandId,
      proofReference: proofRef,
      metadata: {
        ...metadata,
        ipAddress: request.ipAddress,
        userAgent: request.userAgent,
        sessionId: request.sessionId
      },
      previousHash: lastHash,
      currentHash,
      signature: this.signRecord(currentHash)
    };

    // 6. Store consent record
    await this.storeConsent(record);

    // 7. If explicit consent, add DNC exception
    if (this.isExplicitConsent(consentType)) {
      await this.dncService.addException({
        phoneNumber: normalizedPhone,
        consentId: record.id,
        campaignId,
        expiresAt: record.expiresAt
      });
    }

    // 8. Send confirmation to consumer
    await this.sendConfirmation(normalizedPhone, consentType, source);

    return record;
  }

  async withdrawConsent(phoneNumber, reason, source) {
    const normalizedPhone = this.validatePhone(phoneNumber);

    // 1. Get current active consent
    const activeConsent = await this.getActiveConsent(normalizedPhone);

    if (!activeConsent) {
      throw new Error('No active consent found for this number');
    }

    // 2. Create withdrawal record
    const withdrawalRecord = {
      id: this.generateId(),
      phoneNumber: normalizedPhone,
      consentType: ConsentType.WITHDRAWN,
      source,
      capturedAt: new Date(),
      expiresAt: null,
      campaignId: activeConsent.campaignId,
      brandId: activeConsent.brandId,
      proofReference: null,
      metadata: {
        withdrawnConsentId: activeConsent.id,
        withdrawalReason: reason,
        originalConsentDate: activeConsent.capturedAt
      },
      previousHash: activeConsent.currentHash,
      currentHash: this.computeHash({
        phone: normalizedPhone,
        type: 'WITHDRAWN',
        timestamp: new Date().toISOString(),
        previousHash: activeConsent.currentHash
      }),
      signature: null
    };

    // 3. Store withdrawal
    await this.storeConsent(withdrawalRecord);

    // 4. Immediately add to DNC/internal suppression
    await this.dncService.addToSuppression({
      phoneNumber: normalizedPhone,
      reason: 'consent_withdrawn',
      source: `consent:${withdrawalRecord.id}`,
      expiresAt: null // Permanent unless consent re-given
    });

    // 5. Remove DNC exception
    await this.dncService.removeException(normalizedPhone);

    // 6. Send confirmation to consumer
    await this.sendWithdrawalConfirmation(normalizedPhone, source);

    return withdrawalRecord;
  }

  async checkConsent(phoneNumber, campaignId) {
    const normalizedPhone = this.validatePhone(phoneNumber);

    // 1. Get all consent records for this phone, sorted by recency
    const records = await this.getConsentHistory(normalizedPhone);

    // 2. Check for active consent
    const activeConsent = this.findActiveConsent(records, campaignId);

    if (!activeConsent) {
      return {
        hasConsent: false,
        consentType: null,
        expiresAt: null
      };
    }

    // 3. Check if consent is still valid
    if (activeConsent.expiresAt && activeConsent.expiresAt < new Date()) {
      return {
        hasConsent: false,
        consentType: activeConsent.consentType,
        expiresAt: activeConsent.expiresAt,
        expired: true
      };
    }

    return {
      hasConsent: true,
      consentId: activeConsent.id,
      consentType: activeConsent.consentType,
      source: activeConsent.source,
      capturedAt: activeConsent.capturedAt,
      expiresAt: activeConsent.expiresAt,
      proofReference: activeConsent.proofReference
    };
  }

  findActiveConsent(records, campaignId) {
    // Filter out withdrawn records
    const nonWithdrawn = records.filter(r => r.consentType !== ConsentType.WITHDRAWN && r.consentType !== ConsentType.EXPIRED);

    if (nonWithdrawn.length === 0) return null;

    // Group by type and pick highest priority
    const highestPriority = nonWithdrawn.reduce((best, current) => {
      const currentPriority = this.consentPriority[current.consentType] || 0;
      const bestPriority = this.consentPriority[best?.consentType] || 0;
      return currentPriority > bestPriority ? current : best;
    }, null);

    // Check if consent applies to this campaign
    if (highestPriority.campaignId && highestPriority.campaignId !== campaignId) {
      // Campaign-specific consent — check if there's a broader consent or campaign-specific one
      const campaignSpecific = nonWithdrawn.find(
        r => r.campaignId === campaignId
      );
      return campaignSpecific || highestPriority;
    }

    return highestPriority;
  }

  async storeProof(consentType, proofData) {
    if (!proofData) return null;

    const key = `consent-proofs/${this.generateId()}/${consentType}/${Date.now()}`;

    const proofContent = this.prepareProofContent(consentType, proofData);
    await this.storage.putObject(key, proofContent, {
      contentType: this.getProofContentType(consentType),
      metadata: {
        capturedAt: new Date().toISOString(),
        consentType
      }
    });

    return key;
  }

  prepareProofContent(consentType, proofData) {
    switch (consentType) {
      case ConsentType.EXPLICIT_VERBAL:
        return proofData.audioRecording; // Raw audio blob
      case ConsentType.EXPLICIT_WRITTEN:
        return proofData.signedDocument; // PDF or image
      case ConsentType.EXPLICIT_ELECTRONIC:
        return JSON.stringify({
          formData: proofData.formData,
          timestamp: proofData.timestamp,
          ipAddress: proofData.ipAddress,
          userAgent: proofData.userAgent,
          sessionRecording: proofData.sessionRecording
        });
      case ConsentSource.SMS_KEYWORD:
        return JSON.stringify({
          fromNumber: proofData.fromNumber,
          messageBody: proofData.messageBody,
          receivedAt: proofData.receivedAt,
          carrier: proofData.carrier
        });
      default:
        return JSON.stringify(proofData);
    }
  }

  computeExpiry(consentType, campaignId) {
    switch (consentType) {
      case ConsentType.EXPLICIT_WRITTEN:
        // Written consent typically valid for 5 years
        return this.addDuration({ years: 5 });
      case ConsentType.EXPLICIT_ELECTRONIC:
        // Electronic consent typically valid for 2 years
        return this.addDuration({ years: 2 });
      case ConsentType.EXPLICIT_VERBAL:
        // Verbal consent typically valid for 18 months
        return this.addDuration({ months: 18 });
      case ConsentType.IMPLIED_BUSINESS_RELATIONSHIP:
        // EBR valid for 18 months after last purchase/delivery
        return this.addDuration({ months: 18 });
      case ConsentType.IMPLIED_INQUIRY:
        // Inquiry valid for 3 months
        return this.addDuration({ months: 3 });
      default:
        return null; // No expiry
    }
  }

  computeHash(data) {
    const content = JSON.stringify(data);
    return crypto.createHash('sha256').update(content).digest('hex');
  }

  signRecord(hash) {
    // Digital signature for non-repudiation
    const sign = crypto.createSign('RSA-SHA256');
    sign.update(hash);
    return sign.sign(this.privateKey, 'base64');
  }

  async getConsentHistory(phoneNumber) {
    return this.db.consentRecord.findMany({
      where: { phoneNumber },
      orderBy: { capturedAt: 'desc' }
    });
  }

  async getActiveConsent(phoneNumber) {
    const records = await this.getConsentHistory(phoneNumber);
    return this.findActiveConsent(records, null);
  }

  async sendConfirmation(phoneNumber, consentType, source) {
    // Send SMS or email confirmation of consent capture
    const message = `You have opted in to receive calls from ${this.brandName}. Consent recorded via ${source}. Reply STOP to opt out at any time.`;
    await this.notificationService.send(phoneNumber, message);
  }

  async sendWithdrawalConfirmation(phoneNumber, source) {
    const message = `Your opt-out request has been received. You will no longer receive calls from ${this.brandName}. This may take up to 24 hours to take full effect.`;
    await this.notificationService.send(phoneNumber, message);
  }

  validatePhone(phone) {
    const normalized = phoneUtil.parse(phone, 'US');
    if (!phoneUtil.isValidNumber(normalized)) {
      throw new Error('Invalid phone number');
    }
    return phoneUtil.format(normalized, PhoneNumberFormat.E164);
  }

  validateConsentSource(consentType, source) {
    // Certain consent types cannot come from certain sources
    const invalidPairs = {
      [ConsentType.EXPLICIT_WRITTEN]: ['ivr', 'sms_keyword'],
      [ConsentType.EXPLICIT_VERBAL]: ['web_form', 'api_import']
    };

    const invalidSources = invalidPairs[consentType] || [];
    if (invalidSources.includes(source)) {
      throw new Error(`Invalid source ${source} for consent type ${consentType}`);
    }
  }
}
```

## Integration Points

- **DNC Engine (sec-02):** Consent records create DNC exceptions for pre-dial checks
- **Campaign Dialing (Ch 01):** Pre-dial consent verification before call placement
- **Call Recording (Part 12):** Verbal consent recordings linked to consent records for proof
- **Compliance Audit (sec-07):** Consent history exports for regulatory audit
- **CRM Integration (Part 10):** Consent records synced with CRM contact records
- **IVR System (Part 07):** IVR-based consent capture and recording
- **SMS/SIP Inbound:** SMS keyword opt-in processing for consent capture
- **Webhook API:** Third-party consent import via REST API
- **Analytics (Ch 09):** Consent rate and opt-out rate tracking by campaign

## Open-Source Tools

- **libphonenumber (Google):** Phone number validation and E.164 normalization
- **MinIO / localstack-s3:** S3-compatible object storage for consent proof
- **PostgreSQL (with hash index):** Consent record database with hash chain verification
- **BullMQ:** Asynchronous consent capture and confirmation notification queue
- **node:crypto:** Hash chain computation and digital signatures
- **Express / Fastify:** REST API for consent capture endpoints
- **OpenTelemetry:** Consent tracking audit logging and tracing

## Production Considerations

- Consent records are legal evidence — ensure immutability through hash chaining and append-only database patterns
- Proof of consent storage must be durable and backed up across regions — loss of proof is a compliance failure
- Consent verification must complete within 5ms to avoid adding latency to the dialing hot path
- Consumer consent withdrawal must be immediate — use in-memory cache invalidation + database write
- Expired consent should automatically re-add the phone number to DNC lists
- Verbal consent recordings require secure storage with access controls — they contain PII
- Consent type priority rules must be configurable per jurisdiction (e.g., some states require written consent only)
- Monitor consent-to-call conversion rates — low consent rates may indicate UX issues in consent capture flow
- Implement consent rate limiting to detect and prevent consent fraud or ballot stuffing
- Retain consent records for minimum of 4 years after expiration (FCC requirement under TCPA)
- Regular consent record audits (quarterly) should verify hash chain integrity and proof accessibility
- Consider blockchain-based consent registry for multi-tenant compliance across brands
- Consent confirmation messages (SMS/email) serve as secondary proof of consent — log delivery status
- GDPR right-to-erasure requests must handle consent records with anonymization, not deletion (to maintain audit trail)
