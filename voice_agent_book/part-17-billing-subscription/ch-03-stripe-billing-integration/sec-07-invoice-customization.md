# Section 07: Invoice Customization

## Invoice Branding

Stripe invoices can be customized with the company's branding — logo, colors, and company information. Branded invoices present a professional image to customers and reinforce brand identity.

```typescript
class InvoiceBrandingService {
  async setInvoiceBranding(tenantId: string): Promise<void> {
    const tenant = await this.tenantService.getTenant(tenantId);
    const account = await stripe.accounts.retrieve(); // Platform account

    // Set branding settings on the Stripe account
    await stripe.accounts.update(account.id, {
      branding: {
        icon: tenant.branding?.logoUrl
          ? await this.uploadImageToStripe(tenant.branding.logoUrl)
          : undefined,
        logo: tenant.branding?.invoiceLogoUrl
          ? await this.uploadImageToStripe(tenant.branding.invoiceLogoUrl)
          : undefined,
        primary_color: tenant.branding?.primaryColor || '#635bff',
        secondary_color: tenant.branding?.secondaryColor || '#0a2540',
      },
      settings: {
        branding: {
          icon: tenant.branding?.iconUrl
            ? await this.uploadImageToStripe(tenant.branding.iconUrl)
            : undefined,
        },
      },
    });
  }

  async customizeInvoiceDefaults(tenantId: string): Promise<void> {
    const tenant = await this.tenantService.getTenant(tenantId);

    await stripe.invoiceSettings.update({
      default_settings: {
        footer: tenant.branding?.invoiceFooter,
        rendering_options: {
          amount_tax_display: 'include_inclusive_tax',
        },
      },
    });
  }

  private async uploadImageToStripe(imageUrl: string): Promise<Stripe.File> {
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = await imageResponse.buffer();

    return await stripe.files.create({
      purpose: 'business_icon',
      file: {
        data: imageBuffer,
        name: 'branding_image.png',
        type: 'image/png',
      },
    });
  }
}
```

## Custom Fields

Stripe supports custom fields on invoices for B2B requirements like PO numbers, department codes, and cost center references. Custom fields are displayed on the invoice PDF and in the customer portal.

```typescript
interface InvoiceCustomField {
  name: string;
  value: string;
}

async function createInvoiceWithCustomFields(
  subscriptionId: string,
  customFields: InvoiceCustomField[]
): Promise<Stripe.Invoice> {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);

  // Generate invoice manually with custom fields
  const invoice = await stripe.invoices.create({
    customer: subscription.customer,
    subscription: subscriptionId,
    custom_fields: customFields.map(f => ({
      name: f.name,
      value: f.value,
    })),
    pending_invoice_items_behavior: 'include',
  });

  return invoice;
}

async function setCustomerInvoiceSettings(
  tenantId: string,
  settings: {
    customFields?: InvoiceCustomField[];
    defaultPaymentMethod?: string;
    footer?: string;
  }
): Promise<void> {
  const stripeCustomerId = await getStripeCustomerId(tenantId);

  await stripe.customers.update(stripeCustomerId, {
    invoice_settings: {
      custom_fields: settings.customFields?.map(f => ({
        name: f.name,
        value: f.value,
      })),
      default_payment_method: settings.defaultPaymentMethod,
      footer: settings.footer,
    },
  });
}
```

## Memo/Description

Invoice descriptions and memos provide context for the charges. They explain what services were rendered, the billing period, and any special terms.

```typescript
function generateInvoiceDescription(
  periodStart: string,
  periodEnd: string,
  planName: string,
  usageSummary?: UsageSummary
): string {
  const parts = [
    `${planName} — ${formatDate(periodStart)} to ${formatDate(periodEnd)}`,
  ];

  if (usageSummary) {
    parts.push(`Included minutes: ${usageSummary.includedMinutes}`);
    if (usageSummary.overageMinutes > 0) {
      parts.push(`Overage minutes: ${usageSummary.overageMinutes}`);
    }
  }

  return parts.join('\n');
}
```

## PDF Customization

Invoice PDFs can be customized through Stripe's rendering options or by generating custom PDFs using pdfmake (open-source).

```typescript
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

pdfMake.vfs = pdfFonts.pdfMake ? pdfFonts.pdfMake.vfs : pdfFonts.vfs;

class CustomPdfGenerator {
  async generateInvoicePdf(invoice: Invoice): Promise<Buffer> {
    const docDefinition = {
      content: [
        {
          text: 'INVOICE',
          style: 'header',
        },
        {
          text: invoice.number,
          style: 'subheader',
        },
        {
          columns: [
            {
              width: '50%',
              text: [
                { text: 'From:\n', bold: true },
                'Voice Agent SaaS\n',
                '123 Tech Street\n',
                'San Francisco, CA 94105\n',
                'US\n',
              ],
            },
            {
              width: '50%',
              text: [
                { text: 'To:\n', bold: true },
                `${invoice.customerName}\n`,
                `${invoice.customerAddress}\n`,
              ],
            },
          ],
        },
        { text: '\n' },
        {
          table: {
            headerRows: 1,
            widths: ['*', 'auto', 'auto', 'auto'],
            body: [
              [
                { text: 'Description', style: 'tableHeader' },
                { text: 'Qty', style: 'tableHeader' },
                { text: 'Rate', style: 'tableHeader' },
                { text: 'Amount', style: 'tableHeader' },
              ],
              ...invoice.lineItems.map(item => [
                item.description,
                item.quantity.toString(),
                formatCurrency(item.unitPrice),
                formatCurrency(item.total),
              ]),
              [
                { text: '', colSpan: 3, border: [false, true, false, false] },
                {},
                {},
                { text: `Subtotal: ${formatCurrency(invoice.subtotal)}`, bold: true },
              ],
              [
                { text: '', colSpan: 3, border: [false, false, false, false] },
                {},
                {},
                { text: `Tax: ${formatCurrency(invoice.taxTotal)}` },
              ],
              [
                { text: '', colSpan: 3, border: [false, true, false, false] },
                {},
                {},
                { text: `Total: ${formatCurrency(invoice.total)}`, bold: true, fontSize: 14 },
              ],
            ],
          },
        },
        { text: '\n\n' },
        {
          text: `Payment Terms: Due upon receipt`,
          style: 'footer',
        },
        {
          text: invoice.footer || '',
          style: 'footer',
        },
      ],
      styles: {
        header: { fontSize: 24, bold: true, margin: [0, 0, 0, 10] },
        subheader: { fontSize: 16, margin: [0, 0, 0, 20] },
        tableHeader: { bold: true, fontSize: 12, color: 'white', fillColor: '#635bff' },
        footer: { fontSize: 10, italics: true, color: '#666' },
      },
      defaultStyle: {
        fontSize: 11,
      },
    };

    return new Promise((resolve, reject) => {
      const pdfDoc = pdfMake.createPdf(docDefinition);
      pdfDoc.getBuffer((buffer: Buffer) => resolve(buffer));
    });
  }
}
```

## Open-Source Tools

- **pdfmake** (MIT) — PDF invoice generation library
- **Stripe API** — Invoice settings customization
- **Sharp** (Apache 2.0) — Image processing for branding uploads
- **PostgreSQL** — Invoice branding settings storage

## Integration Points

Invoice customization integrates with the tenant settings service, the invoice generation service (Chapter 4 Section 2), and the customer portal.

## Production Considerations

- Validate uploaded branding images (dimensions, file size, format)
- Cache branding settings to avoid repeated Stripe API calls
- Test PDF rendering across different invoice scenarios
- Handle custom fonts in pdfmake for internationalization
- Preview invoice PDF before sending to customer

## Open-Source First Philosophy

pdfmake (MIT) provides full-featured PDF generation for invoices without licensing costs. Combined with Stripe's native invoice customization, this eliminates the need for enterprise document generation platforms. The entire invoicing pipeline uses open-source tools with Stripe providing the payment infrastructure.
