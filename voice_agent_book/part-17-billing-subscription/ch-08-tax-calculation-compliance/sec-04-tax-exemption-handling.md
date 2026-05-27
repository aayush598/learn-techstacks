# Section 04: Tax Exemption Handling

## Exemption Certificate Collection

Tax-exempt customers (non-profits, government entities, resellers) must submit valid exemption certificates. The system manages certificate collection, validation, and storage.

```typescript
interface ExemptionCertificate {
  id: string;
  tenantId: string;
  type: ExemptionType;
  jurisdiction: string;
  certificateNumber: string;
  issueDate: string;
  expirationDate?: string;
  status: 'pending' | 'active' | 'expired' | 'rejected';
  documentUrl?: string;
  validationNotes?: string;
  createdAt: string;
  updatedAt: string;
}

enum ExemptionType {
  NONPROFIT_501C3 = 'nonprofit_501c3',
  GOVERNMENT = 'government',
  RESELLER = 'reseller',
  EDUCATIONAL = 'educational',
  TRIBAL = 'tribal',
  CHARITABLE = 'charitable',
  RELIGIOUS = 'religious',
}

class ExemptionService {
  async submitCertificate(
    tenantId: string,
    certificate: Omit<ExemptionCertificate, 'id' | 'status' | 'createdAt' | 'updatedAt'>
  ): Promise<ExemptionCertificate> {
    // Upload document
    let documentUrl: string | undefined;
    if (certificate.documentUrl) {
      documentUrl = await this.storageService.storeFile(
        `exemptions/${tenantId}/${certificate.type}_${Date.now()}`,
        certificate.documentUrl
      );
    }

    const record: ExemptionCertificate = {
      id: `exc_${nanoid(16)}`,
      tenantId,
      ...certificate,
      documentUrl,
      status: 'pending',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    await this.db.exemptionCertificates.create(record);

    // Trigger validation
    await this.validateCertificate(record.id);

    return record;
  }

  async validateCertificate(certificateId: string): Promise<void> {
    const cert = await this.db.exemptionCertificates.findOne({ id: certificateId });

    let isValid = true;
    let notes: string[] = [];

    // Check expiration
    if (cert.expirationDate && new Date(cert.expirationDate) < new Date()) {
      isValid = false;
      notes.push('Certificate has expired');
    }

    // Validate format based on type
    switch (cert.type) {
      case 'nonprofit_501c3':
        // Validate format of 501(c)(3) determination letter
        const hasValidFormat = /^\d{2}-\d{7}$/.test(cert.certificateNumber);
        if (!hasValidFormat) {
          notes.push('Invalid EIN format for 501(c)(3)');
        }
        break;
      case 'reseller':
        // Validate reseller permit format (varies by state)
        const statePattern = /^[A-Z]{2}-\d{6,10}$/;
        if (!statePattern.test(cert.certificateNumber)) {
          notes.push('Invalid reseller certificate format');
        }
        break;
    }

    await this.db.exemptionCertificates.updateOne(
      { id: certificateId },
      {
        $set: {
          status: isValid ? 'active' : 'rejected',
          validationNotes: notes.join('; ') || undefined,
          updatedAt: new Date().toISOString(),
        },
      }
    );

    if (isValid) {
      // Apply exemption to customer
      await this.applyExemptionToCustomer(cert.tenantId, cert.jurisdiction, cert.id);
    }
  }

  async applyExemptionToCustomer(
    tenantId: string,
    jurisdiction: string,
    certificateId: string
  ): Promise<void> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    await stripe.customers.update(stripeCustomerId, {
      tax: {
        ip_address: null,
        location: null,
      },
      metadata: {
        [`exemption_${jurisdiction}`]: certificateId,
        exempt_jurisdictions: await this.getExemptJurisdictions(tenantId),
      },
    });

    await this.db.tenants.updateOne(
      { id: tenantId },
      {
        $set: {
          [`exemptions.${jurisdiction}`]: {
            certificateId,
            appliedAt: new Date().toISOString(),
          },
        },
      }
    );
  }
}
```

## Exemption Validation

Validation ensures certificates are legitimate and cover the appropriate jurisdictions and product types.

```typescript
interface ExemptionValidationRule {
  type: ExemptionType;
  acceptedJurisdictions: string[];
  acceptedProducts: string[];
  requiresDocument: boolean;
  documentFormats: string[];
  autoValidate: boolean;
  approvalRequired: boolean;
}

const VALIDATION_RULES: Record<ExemptionType, ExemptionValidationRule> = {
  nonprofit_501c3: {
    type: 'nonprofit_501c3',
    acceptedJurisdictions: ['US', 'US-*'],
    acceptedProducts: ['*'],
    requiresDocument: true,
    documentFormats: ['pdf', 'jpg', 'png'],
    autoValidate: true,
    approvalRequired: false,
  },
  government: {
    type: 'government',
    acceptedJurisdictions: ['US', 'US-*', 'CA', 'UK'],
    acceptedProducts: ['*'],
    requiresDocument: true,
    documentFormats: ['pdf'],
    autoValidate: true,
    approvalRequired: false,
  },
  reseller: {
    type: 'reseller',
    acceptedJurisdictions: ['US-*'],
    acceptedProducts: ['*'],
    requiresDocument: true,
    documentFormats: ['pdf'],
    autoValidate: false,
    approvalRequired: true,
  },
};
```

## Exempt vs Taxable Line Items

When an invoice includes both exempt and taxable items, each line item is marked with its tax status. The invoice total breaks down exempt and taxable amounts.

```typescript
function classifyLineItems(
  items: InvoiceLineItem[],
  exemptions: ExemptionCertificate[]
): LineItemTaxClassification[] {
  return items.map(item => {
    const relevantExemptions = exemptions.filter(e =>
      e.status === 'active'
      && (e.jurisdiction === '*' || e.jurisdiction === item.metadata?.jurisdiction)
    );

    return {
      lineItemId: item.id,
      description: item.description,
      amount: item.amount,
      exempt: relevantExemptions.length > 0,
      exemptionReferences: relevantExemptions.map(e => e.id),
      taxableAmount: relevantExemptions.length > 0 ? 0 : item.amount,
      exemptAmount: relevantExemptions.length > 0 ? item.amount : 0,
    };
  });
}
```

## Open-Source Tools

- **PostgreSQL** — Certificate storage and validation rules
- **MinIO** (AGPL 3.0) — Certificate document storage
- **BullMQ** — Schedule certificate expiry reminders
- **Nodemailer** (MIT) — Certificate status notifications

## Integration Points

Exemption handling connects to the tax engine (rate determination), the customer management system (exemption status), the invoice system (line item classification), and the notification service (expiry reminders).

## Production Considerations

- Send certificate expiry reminders 90, 60, and 30 days before
- Require admin approval for reseller exemptions
- Validate certificates against state databases where possible
- Maintain audit trail of all exemption applications
- Test exemption scenarios thoroughly for each jurisdiction

## Open-Source First Philosophy

PostgreSQL stores exemption certificates and validation rules. MinIO provides S3-compatible document storage. BullMQ manages expiry schedules. This open-source approach avoids proprietary tax exemption management systems while maintaining compliance with tax authority requirements.
