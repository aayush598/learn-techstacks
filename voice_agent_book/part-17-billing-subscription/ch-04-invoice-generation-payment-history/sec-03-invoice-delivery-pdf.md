# Section 03: Invoice Delivery & PDF Generation

## PDF Generation

Invoice PDFs are generated automatically after invoice finalization. PDF generation uses pdfmake, an open-source library that builds PDFs from JavaScript objects. The PDF includes all invoice details, line items, tax breakdown, and branding.

```typescript
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

pdfMake.vfs = pdfFonts.pdfMake.vfs;

class InvoicePdfService {
  async generateInvoicePdf(invoice: Invoice): Promise<Buffer> {
    const tenant = await this.tenantService.getTenant(invoice.tenantId);
    const branding = tenant.branding;

    const docDefinition = {
      pageSize: 'A4',
      pageMargins: [40, 60, 40, 60],
      header: () => ({
        columns: [
          {
            image: branding?.logoUrl,
            width: 120,
            alignment: 'left',
          },
          {
            text: 'INVOICE',
            alignment: 'right',
            fontSize: 28,
            bold: true,
            color: branding?.primaryColor || '#635bff',
          },
        ],
        margin: [40, 20, 40, 10],
      }),
      content: [
        { text: '\n' },
        // Invoice details
        {
          columns: [
            {
              width: '50%',
              stack: [
                { text: 'From:', style: 'label' },
                { text: tenant.companyName, style: 'value' },
                { text: tenant.billingAddress?.line1 },
                { text: `${tenant.billingAddress?.city}, ${tenant.billingAddress?.state} ${tenant.billingAddress?.postalCode}` },
                { text: tenant.billingAddress?.country },
              ],
            },
            {
              width: '50%',
              alignment: 'right',
              stack: [
                { text: `Invoice #${invoice.number}`, style: 'value', bold: true },
                { text: `Issue Date: ${formatDate(invoice.issueDate)}` },
                { text: `Due Date: ${formatDate(invoice.dueDate)}` },
                { text: `Period: ${formatDate(invoice.periodStart)} — ${formatDate(invoice.periodEnd)}` },
              ],
            },
          ],
        },
        { text: '\n' },
        // Customer details
        {
          text: `Bill To: ${invoice.customerName || tenant.companyName}`,
          style: 'sectionHeader',
        },
        { text: '\n' },
        // Line items table
        {
          table: {
            headerRows: 1,
            widths: ['*', 'auto', 'auto', 'auto'],
            body: [
              [
                { text: 'Description', style: 'tableHeader' },
                { text: 'Qty', style: 'tableHeader', alignment: 'center' },
                { text: 'Unit Price', style: 'tableHeader', alignment: 'right' },
                { text: 'Amount', style: 'tableHeader', alignment: 'right' },
              ],
              ...invoice.lineItems.map(item => [
                item.description,
                { text: item.quantity.toString(), alignment: 'center' },
                { text: formatCurrency(item.unitPrice / 100), alignment: 'right' },
                { text: formatCurrency(item.amount / 100), alignment: 'right' },
              ]),
            ],
          },
          layout: {
            fillColor: (rowIndex: number) => rowIndex === 0 ? branding?.primaryColor || '#635bff' : null,
            hLineWidth: () => 0.5,
            vLineWidth: () => 0.5,
          },
        },
        { text: '\n' },
        // Totals
        {
          columns: [
            { width: '*', text: '' },
            {
              width: '40%',
              stack: [
                { columns: [{ text: 'Subtotal:', width: '50%' }, { text: formatCurrency(invoice.subtotal / 100), width: '50%', alignment: 'right' }] },
                ...invoice.taxBreakdown.map(tax => ({
                  columns: [
                    { text: `${tax.jurisdiction.state || tax.jurisdiction.country} Tax (${(tax.taxRate * 100).toFixed(2)}%):`, width: '50%' },
                    { text: formatCurrency(tax.taxAmount / 100), width: '50%', alignment: 'right' },
                  ],
                })),
                { columns: [{ text: 'Total:', bold: true, width: '50%', fontSize: 14 }, { text: formatCurrency(invoice.total / 100), bold: true, width: '50%', alignment: 'right', fontSize: 14 }] },
              ],
            },
          ],
        },
        { text: '\n\n' },
        // Payment terms
        {
          text: `Payment Terms: Due by ${formatDate(invoice.dueDate)}`,
          style: 'footer',
        },
        ...(invoice.notes ? [{ text: `Notes: ${invoice.notes}`, style: 'footer' }] : []),
      ],
      styles: {
        label: { fontSize: 10, color: '#666', bold: true },
        value: { fontSize: 11 },
        sectionHeader: { fontSize: 14, bold: true, color: branding?.primaryColor || '#635bff' },
        tableHeader: { fontSize: 10, bold: true, color: 'white', fillColor: branding?.primaryColor || '#635bff' },
        footer: { fontSize: 9, color: '#999', italics: true },
      },
    };

    return new Promise((resolve, reject) => {
      const pdfDoc = pdfMake.createPdf(docDefinition);
      pdfDoc.getBuffer((buffer: Buffer) => resolve(buffer));
    });
  }
}
```

## Email Delivery

Invoices are delivered via email with the PDF as an attachment. The delivery service formats the email body with invoice details and provides a link to the customer portal.

```typescript
class InvoiceDeliveryService {
  async deliverInvoice(invoice: Invoice): Promise<void> {
    const tenant = await this.tenantService.getTenant(invoice.tenantId);
    const pdfBuffer = await this.pdfService.generateInvoicePdf(invoice);

    // Upload PDF to storage
    const pdfUrl = await this.storageService.upload(
      `invoices/${invoice.tenantId}/${invoice.number}.pdf`,
      pdfBuffer,
      'application/pdf'
    );

    // Update invoice with PDF URL
    await this.db.invoices.updateOne(
      { id: invoice.id },
      { $set: { pdfUrl } }
    );

    // Send email
    await this.emailService.send({
      to: tenant.billingEmail || tenant.email,
      subject: `Invoice ${invoice.number} from Voice Agent Platform`,
      template: 'invoice_ready',
      data: {
        invoiceNumber: invoice.number,
        amount: formatCurrency(invoice.total / 100),
        dueDate: formatDate(invoice.dueDate),
        pdfUrl,
        portalUrl: `${APP_URL}/billing/invoices`,
      },
      attachments: [
        {
          filename: `${invoice.number}.pdf`,
          content: pdfBuffer.toString('base64'),
          contentType: 'application/pdf',
        },
      ],
    });

    // Schedule reminder
    await this.bullQueue.add('invoiceReminder', {
      invoiceId: invoice.id,
      remindDays: [3, 1], // Remind 3 days and 1 day before due
    });
  }
}
```

## Customer Portal Access

Invoices are available in the Stripe Customer Portal and on the app's billing page. The portal provides access to all invoices, payment history, and account settings.

```typescript
class InvoicePortalService {
  async listInvoices(
    tenantId: string,
    options: { limit?: number; offset?: number; status?: string }
  ): Promise<Invoice[]> {
    const query: any = { tenantId };

    if (options.status) {
      query.status = options.status;
    }

    return await this.db.invoices.find(query)
      .sort({ issueDate: -1 })
      .skip(options.offset || 0)
      .limit(options.limit || 20)
      .toArray();
  }

  async getInvoicePdf(tenantId: string, invoiceId: string): Promise<string> {
    const invoice = await this.db.invoices.findOne({ id: invoiceId, tenantId });
    if (!invoice) throw new Error('Invoice not found');

    if (invoice.pdfUrl) {
      return invoice.pdfUrl;
    }

    // Generate PDF on demand
    const pdfBuffer = await this.pdfService.generateInvoicePdf(invoice);
    const pdfUrl = await this.storageService.upload(
      `invoices/${tenantId}/${invoice.number}.pdf`,
      pdfBuffer,
      'application/pdf'
    );

    await this.db.invoices.updateOne(
      { id: invoiceId },
      { $set: { pdfUrl } }
    );

    return pdfUrl;
  }
}
```

## Archival

Invoices older than the retention period are archived to cold storage. Archival preserves accessibility while reducing active database size.

```typescript
interface InvoiceArchiveConfig {
  activeRetentionDays: number;    // 365 (1 year)
  warmRetentionDays: number;      // 2555 (7 years)
  coldStorageClass: string;       // 'glacier' for AWS S3
}

async function archiveInvoices(): Promise<void> {
  const archiveBefore = new Date();
  archiveBefore.setDate(archiveBefore.getDate() - 365);

  const oldInvoices = await db.invoices.find({
    issueDate: { $lt: archiveBefore.toISOString() },
    archived: { $ne: true },
  }).toArray();

  for (const invoice of oldInvoices) {
    // Move PDF to cold storage
    if (invoice.pdfUrl) {
      const coldUrl = await storageService.moveToColdStorage(invoice.pdfUrl);
      await db.invoices.updateOne(
        { id: invoice.id },
        {
          $set: {
            archived: true,
            archivedAt: new Date().toISOString(),
            pdfUrl: coldUrl,
          },
        }
      );
    }
  }
}
```

## Open-Source Tools

- **pdfmake** (MIT) — PDF generation from JavaScript
- **BullMQ** (MIT) — Schedule invoice delivery and reminders
- **Nodemailer** (MIT) — Email delivery for invoices
- **MinIO** (AGPL 3.0) — S3-compatible storage for invoice PDFs

## Integration Points

PDF generation integrates with the invoice service (invoice data), the tenant service (branding), the email service (delivery), and the storage service (PDF archival).

## Production Considerations

- Generate PDFs asynchronously after invoice finalization
- Cache generated PDFs to avoid regeneration
- Handle PDF generation failures with retry logic
- Ensure PDF accessibility (screen reader compatible)
- Compress PDFs to reduce storage and email size
- Monitor PDF generation latency and error rates

## Open-Source First Philosophy

pdfmake provides enterprise-grade PDF generation at zero licensing cost. MinIO replaces AWS S3 for PDF storage with an S3-compatible API. Nodemailer handles email delivery through any SMTP provider. This all-open-source stack replaces expensive document generation and delivery services while maintaining professional output quality.
