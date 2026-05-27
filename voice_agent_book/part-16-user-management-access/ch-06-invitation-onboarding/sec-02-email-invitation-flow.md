# Email Invitation Flow

## Overview

The email invitation flow sends branded transactional emails with invitation links, tracks delivery status, handles bounces, and supports click tracking. Integration with email providers (Resend, SES, SendGrid) ensures reliable delivery.

## Email Template

```typescript
interface InvitationEmailData {
  inviterName: string;
  inviterEmail: string;
  tenantName: string;
  roleName: string;
  teamName?: string;
  inviteLink: string;
  expiresInDays: number;
  companyLogoUrl?: string;
}

function renderInvitationEmail(data: InvitationEmailData): string {
  return `
    <div style="max-width: 560px; margin: 0 auto; font-family: sans-serif;">
      ${data.companyLogoUrl ? `<img src="${data.companyLogoUrl}" height="40" />` : ''}
      <h2>You're invited to join ${data.tenantName}</h2>
      <p>${data.inviterName} (${data.inviterEmail}) has invited you to join <strong>${data.tenantName}</strong> as <strong>${data.roleName}</strong>.</p>
      ${data.teamName ? `<p>Team: ${data.teamName}</p>` : ''}
      <a href="${data.inviteLink}" style="display: inline-block; padding: 12px 24px; background: #6366f1; color: white; text-decoration: none; border-radius: 6px;">
        Accept Invitation
      </a>
      <p style="color: #666; font-size: 12px;">This link expires in ${data.expiresInDays} days.</p>
    </div>
  `;
}
```

## Delivery Service

```typescript
class InvitationEmailService {
  async sendInvitation(inviteId: string, email: string, data: InvitationEmailData): Promise<void> {
    const html = renderInvitationEmail(data);
    const text = `You're invited to join ${data.tenantName}. Click here to accept: ${data.inviteLink}`;

    const result = await this.emailProvider.send({
      to: email,
      subject: `You're invited to join ${data.tenantName}`,
      html,
      text,
      tags: { type: 'invitation', inviteId },
      trackClicks: true,
      trackOpens: true,
    });

    await this.db.insert('invitation_emails', {
      inviteId,
      email,
      messageId: result.messageId,
      status: 'sent',
      sentAt: new Date(),
    });
  }

  async handleBounce(messageId: string): Promise<void> {
    await this.db.update('invitation_emails', { messageId }, {
      status: 'bounced',
      bouncedAt: new Date(),
    });

    // Notify inviter
    const emailRec = await this.db.findOne('invitation_emails', { messageId });
    if (emailRec) {
      await this.notificationService.notify({
        type: 'invitation_bounced',
        recipients: [emailRec.inviteId], // Inviter
        data: { email: emailRec.email },
      });
    }
  }
}
```

## Flow

```
Admin creates invitation → Token generated → Email queued
    → Email sent via Resend/SES → Delivery tracked
    → User clicks link → Token validated → Registration page
    → On completion → Token consumed → Welcome email sent
```

## Open-Source Tools

- **Resend** (MIT) — Transactional email API
- **nodemailer** (MIT) — SMTP email library
- **@sendgrid/mail** (MIT) — SendGrid email client

## Production Considerations

- Queue email sending via BullMQ to handle delivery failures and retries
- Track bounce rate per tenant; alert if >5% bounce rate
- Support custom sender domain (SPF, DKIM, DMARC configured per tenant)
- Provide in-app resend with 60-second cooldown
- Include unsubscribe link in footer per CAN-SPAM compliance
