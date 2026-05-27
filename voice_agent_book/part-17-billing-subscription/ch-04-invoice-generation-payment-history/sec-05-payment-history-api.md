# Section 05: Payment History API

## Payment History Endpoint

The payment history API provides tenants with a complete view of all financial transactions: invoices, payments, refunds, credits, and adjustments. The API supports pagination, filtering, and sorting for efficient data retrieval.

```typescript
// API: GET /api/v1/billing/payments
interface PaymentHistoryQuery {
  page: number;
  limit: number;
  status?: PaymentStatus | 'all';
  type?: TransactionType;
  dateFrom?: string;
  dateTo?: string;
  sort?: 'date_desc' | 'date_asc' | 'amount_desc' | 'amount_asc';
}

interface PaymentHistoryResponse {
  data: PaymentTransaction[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
  summary: {
    totalPaid: number;
    totalRefunded: number;
    totalOpen: number;
    currency: string;
  };
}

type TransactionType = 'invoice' | 'payment' | 'refund' | 'credit' | 'adjustment';

interface PaymentTransaction {
  id: string;
  type: TransactionType;
  number?: string;           // Invoice or credit note number
  description: string;
  amount: number;            // In cents (positive for charges, negative for credits)
  currency: string;
  status: string;
  date: string;
  paymentMethod?: {
    brand: string;
    last4: string;
  };
  invoiceId?: string;
  receiptUrl?: string;
}

class PaymentHistoryController {
  async listPayments(
    tenantId: string,
    query: PaymentHistoryQuery
  ): Promise<PaymentHistoryResponse> {
    const filter: any = { tenantId };
    const page = query.page || 1;
    const limit = Math.min(query.limit || 20, 100);
    const skip = (page - 1) * limit;

    if (query.status && query.status !== 'all') {
      filter.paymentStatus = query.status;
    }

    if (query.dateFrom || query.dateTo) {
      filter.issueDate = {};
      if (query.dateFrom) filter.issueDate.$gte = query.dateFrom;
      if (query.dateTo) filter.issueDate.$lte = query.dateTo;
    }

    // Build sort
    let sort: any = { issueDate: -1 };
    switch (query.sort) {
      case 'date_asc': sort = { issueDate: 1 }; break;
      case 'amount_desc': sort = { total: -1 }; break;
      case 'amount_asc': sort = { total: 1 }; break;
    }

    // Fetch invoices
    const invoices = await this.db.invoices.find(filter)
      .sort(sort)
      .skip(skip)
      .limit(limit)
      .toArray();

    // Fetch credit notes
    const creditNotes = await this.db.creditNotes.find({
      tenantId,
      ...(query.dateFrom || query.dateTo ? {
        issuedAt: {
          ...(query.dateFrom ? { $gte: query.dateFrom } : {}),
          ...(query.dateTo ? { $lte: query.dateTo } : {}),
        },
      } : {}),
    }).sort({ issuedAt: -1 }).toArray();

    // Combine and sort by date
    const transactions: PaymentTransaction[] = [
      ...invoices.map(inv => this.invoiceToTransaction(inv)),
      ...creditNotes.map(cn => this.creditNoteToTransaction(cn)),
    ].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

    // Get totals
    const [totalPaid, totalOpen] = await Promise.all([
      this.db.invoices.aggregate([
        { $match: { tenantId, paymentStatus: PaymentStatus.PAID } },
        { $group: { _id: null, total: { $sum: '$total' } } },
      ]).toArray(),
      this.db.invoices.aggregate([
        { $match: { tenantId, paymentStatus: PaymentStatus.UNPAID } },
        { $group: { _id: null, total: { $sum: '$total' } } },
      ]).toArray(),
    ]);

    return {
      data: transactions.slice(skip, skip + limit),
      pagination: {
        page,
        limit,
        total: transactions.length,
        totalPages: Math.ceil(transactions.length / limit),
      },
      summary: {
        totalPaid: totalPaid[0]?.total || 0,
        totalRefunded: 0, // Calculate from credit notes
        totalOpen: totalOpen[0]?.total || 0,
        currency: 'usd',
      },
    };
  }

  private invoiceToTransaction(invoice: Invoice): PaymentTransaction {
    return {
      id: invoice.id,
      type: 'invoice',
      number: invoice.number,
      description: `Invoice for ${formatDate(invoice.periodStart)} — ${formatDate(invoice.periodEnd)}`,
      amount: invoice.total,
      currency: invoice.currency,
      status: invoice.paymentStatus,
      date: invoice.issueDate,
      paymentMethod: invoice.paymentMethod,
      receiptUrl: invoice.pdfUrl,
    };
  }
}
```

## Pagination and Filtering

The API supports cursor-based pagination for efficient retrieval of large datasets. Filters include date range, transaction type, status, and amount range.

```typescript
interface CursorPagination {
  cursor?: string;          // Opaque cursor for next page
  limit: number;
  previousCursor?: string;
}

async function listWithCursor(
  tenantId: string,
  cursor?: string,
  limit: number = 20
): Promise<{ data: any[]; nextCursor?: string; hasMore: boolean }> {
  const query: any = { tenantId };

  if (cursor) {
    const decoded = Buffer.from(cursor, 'base64').toString();
    const [timestamp, id] = decoded.split(':');
    query.$or = [
      { issueDate: { $lt: timestamp } },
      { issueDate: timestamp, id: { $lt: id } },
    ];
  }

  const invoices = await this.db.invoices.find(query)
    .sort({ issueDate: -1, id: -1 })
    .limit(limit + 1)
    .toArray();

  const hasMore = invoices.length > limit;
  const data = hasMore ? invoices.slice(0, limit) : invoices;

  let nextCursor: string | undefined;
  if (hasMore) {
    const last = data[data.length - 1];
    nextCursor = Buffer.from(`${last.issueDate}:${last.id}`).toString('base64');
  }

  return { data, nextCursor, hasMore };
}
```

## Transaction Types

The API covers all transaction types:

- **Invoice**: Standard billing charges
- **Payment**: Individual payment transactions
- **Refund**: Full or partial refunds
- **Credit Note**: Adjustments and credits
- **Adjustment**: Manual billing adjustments

## Export Endpoints

Export allows tenants to download payment history as CSV or JSON for accounting purposes.

```typescript
// API: GET /api/v1/billing/payments/export
class PaymentExportService {
  async exportToCsv(tenantId: string, query: PaymentHistoryQuery): Promise<string> {
    const payments = await this.paymentHistoryController.listPayments(tenantId, query);

    const headers = [
      'Date', 'Type', 'Number', 'Description',
      'Amount', 'Currency', 'Status', 'Payment Method',
    ];

    const rows = payments.data.map(tx => [
      tx.date,
      tx.type,
      tx.number || '',
      `"${tx.description.replace(/"/g, '""')}"`,
      (tx.amount / 100).toFixed(2),
      tx.currency,
      tx.status,
      tx.paymentMethod ? `${tx.paymentMethod.brand} ****${tx.paymentMethod.last4}` : '',
    ]);

    return [
      headers.join(','),
      ...rows.map(row => row.join(',')),
    ].join('\n');
  }

  async exportToJson(tenantId: string, query: PaymentHistoryQuery): Promise<string> {
    const payments = await this.paymentHistoryController.listPayments(tenantId, query);
    return JSON.stringify(payments.data, null, 2);
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Payment history storage
- **BullMQ** — Schedule export generation jobs
- **Metabase** (Apache 2.0) — Self-service payment analytics
- **csv-parse/serialize** (MIT) — CSV generation for exports

## Integration Points

The payment history API connects to the invoice service, credit note service, Stripe API (for payment method details), and the customer portal (Part 12).

## Production Considerations

- Cache payment history queries for frequently accessed pages
- Implement rate limiting on export endpoints
- Handle large datasets with streaming exports
- Mask sensitive payment method data (last 4 digits only)
- Ensure export data matches what's displayed in the UI

## Open-Source First Philosophy

The payment history API is built entirely on PostgreSQL with no proprietary database or API gateway. csv-parse (MIT) handles export generation. This keeps the billing infrastructure open and auditable while providing a comprehensive payment history interface for customers.
