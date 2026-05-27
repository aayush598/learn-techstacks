# Section 04: White-Label Email Templates

## Overview

White-label email templates ensure that all transactional emails sent on behalf of a tenant (welcome emails, password resets, notifications, reports) carry the tenant's branding rather than the platform's. This is essential for resellers and enterprise customers who want their end users to see a seamless brand experience. Email templates inherit brand colors, logo, fonts, and custom footer content from the tenant's branding configuration.

The email template system uses a template inheritance model: base templates define the email structure (header, body, footer) with platform defaults, and tenant branding overlays replace colors, logos, and contact information. Templates are rendered server-side (using MJML for responsive email design) and sent through the tenant's configured sending domain for better deliverability.

For a voice agent platform, typical branded emails include: welcome/onboarding, call summaries and transcripts, campaign reports, billing invoices, usage alerts, and security notifications. Each email type has a branded and unbranded version.

## Design Decisions

**Decision 1: MJML for responsive email templates.** MJML compiles to responsive HTML email that works across all email clients (Outlook, Gmail, Apple Mail). It's the industry standard for transactional email design.

**Decision 2: Template inheritance with brand variables.** Base templates contain `{{brand.logo}}`, `{{brand.primaryColor}}`, `{{brand.companyName}}` placeholders that are replaced with tenant-specific values at render time.

**Decision 3: Custom sending domain per tenant.** For white-label resellers, emails should come from the tenant's domain (noreply@acmecorp.com) rather than the platform's domain. This requires SPF/DKIM configuration per tenant.

## Implementation Approach

```typescript
class WhiteLabelEmailService {
  private templates: Map<string, string>;

  async renderEmail(
    templateName: string,
    tenantId: string,
    data: Record<string, any>
  ): Promise<{ html: string; text: string }> {
    const [branding, template] = await Promise.all([
      this.getTenantBranding(tenantId),
      this.getTemplate(templateName),
    ]);

    // Apply branding variables to template
    const brandedTemplate = this.applyBranding(template, branding, data);

    // Render MJML to HTML
    const html = mjml2html(brandedTemplate, { minify: true });

    // Generate plain text version
    const text = this.htmlToText(html.html);

    return { html: html.html, text };
  }

  async sendBrandedEmail(
    tenantId: string,
    to: string,
    templateName: string,
    data: Record<string, any>
  ): Promise<void> {
    const { html, text } = await this.renderEmail(templateName, tenantId, data);
    const branding = await this.getTenantBranding(tenantId);

    await this.emailClient.send({
      from: {
        email: branding.fromEmail || 'noreply@voiceagent.com',
        name: branding.companyName || 'Voice Agent',
      },
      to,
      subject: this.renderSubject(templateName, data, branding),
      html,
      text,
      headers: {
        'X-Tenant-ID': tenantId,
        'List-Unsubscribe': branding.unsubscribeUrl,
      },
    });
  }

  private applyBranding(
    template: string,
    branding: TenantBranding,
    data: Record<string, any>
  ): string {
    return template
      .replace(/\{\{brand\.logo\}\}/g, branding.logoUrl)
      .replace(/\{\{brand\.primaryColor\}\}/g, branding.primaryColor)
      .replace(/\{\{brand\.companyName\}\}/g, branding.companyName)
      .replace(/\{\{brand\.companyAddress\}\}/g, branding.address || '')
      .replace(/\{\{brand\.supportEmail\}\}/g, branding.supportEmail)
      .replace(/\{\{brand\.unsubscribeUrl\}\}/g, branding.unsubscribeUrl)
      .replace(/\{\{brand\.footerText\}\}/g, branding.footerText || '');
  }

  async configureSendingDomain(tenantId: string, domain: string): Promise<void> {
    // Configure SPF, DKIM, DMARC for tenant's sending domain
    const dkimKeys = await this.emailClient.addDomain(domain);
    
    await this.db.query(
      `UPDATE tenant_branding 
       SET sending_domain = $1, dkim_config = $2 
       WHERE tenant_id = $3`,
      [domain, JSON.stringify(dkimKeys), tenantId]
    );

    // Return DNS records that tenant must add
    return dkimKeys.dnsRecords;
  }
}
```

## Open-Source Tools

- **MJML** — Responsive email framework
- **React Email** — Build email templates with React components
- **html-to-text** — Plain text email generation
- **SendGrid / Resend** — Transactional email API with DKIM support
- **Postmark** — Email delivery with white-label support

## Production Considerations

- **Email Deliverability:** Branded emails from tenant domains requires proper email authentication (SPF, DKIM, DMARC). Guide tenants through DNS setup for their sending domain.
- **Template Testing:** Test branded emails in all major email clients (Gmail, Outlook, Apple Mail). Use Litmus or Email on Acid for pre-deployment testing.
- **Footer Compliance:** Include required legal footers (unsubscribe link, physical address) in all branded emails. These are required by CAN-SPAM and GDPR.
- **Preview Mode:** Allow tenants to preview their branded emails before sending. Show how each email type will appear with their branding.
- **Custom Templates:** Advanced tenants may want complete control over email template HTML. Offer a custom template option with version control and rollback.
