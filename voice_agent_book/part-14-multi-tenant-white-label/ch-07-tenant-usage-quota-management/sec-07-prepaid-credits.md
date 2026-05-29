# Section 07: Prepaid Credits & Consumption

Prepaid credits allow tenants to purchase usage credits upfront at a discount, then consume them over time. Credits are stored as a balance in the tenant's account and deducted as usage occurs. The system supports both monetary credits ($1 = $1 of usage) and unit credits (10,000 API calls, 1,000 call minutes).

The credit system architecture: credit purchase (Stripe payment creates credit balance), credit deduction (usage events decrement balance), balance tracking (real-time Redis counter, PostgreSQL for persistence), expiration (credits expire after 12 months), and rollover (unused credits at month end carry forward). Credits are consumed in FIFO order.

Credit deduction logic checks the prepaid balance first, then falls back to postpaid billing. If credits exist, usage is deducted from the credit balance. If credits are exhausted, usage is billed normally. The billing system generates invoices that show credit usage vs billed usage separately.
