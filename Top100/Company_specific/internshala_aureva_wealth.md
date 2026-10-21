# Aureva Wealth Advisors — 100 Full Stack Interview Q&A

> Based on Aureva Wealth Advisors — Full Stack Development Internship (fintech mutual fund platform; Next.js/Node.js/PostgreSQL/OAuth2/KYC/payments)  > Candidate: Aayush Gid (Next.js/React/TypeScript/PostgreSQL/OAuth/Express/Docker background)

---

## 1. Fintech & Investment Platform Fundamentals (Q1–Q10)

**Q1: What is a mutual fund and how does a digital investment platform handle transactions?**  
A: A mutual fund pools investor money into a diversified portfolio managed by an AMC. A platform acts as a distributor: it collects user orders (purchase/SIP/step-up), routes them via BSE Star MF or CAMS APIs to the AMC, and reflects NAV-based allotment back to the user. Key states: pending → confirmed → allotted.

**Q2: What are the key regulatory requirements for a fintech wealth-tech platform in India?**  
A: SEBI ( Securities and Exchange Board of India ) regulates investment advisors and distributors. Requirements include KYC verification (via KRA/CDSL), AMFI registration for distribution, transaction audit trails, data encryption at rest and in transit, and compliance with RBI data localization norms. Non-compliance can result in license revocation.

**Q3: What is KYC and how would you implement it in a web app?**  
A: KYC (Know Your Customer) verifies user identity. Flow: user uploads PAN/Aadhaar → backend calls a KYC provider API (DigiLocker, NSDL eKYC, or OnGrid) → provider returns verified name/DOB/PAN status → backend stores verification status and expiry in the DB. Implement with a dedicated `kyc_verifications` table linked to `users`.

```sql
CREATE TABLE kyc_verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  provider TEXT NOT NULL,
  document_type TEXT NOT NULL, -- 'pan', 'aadhaar'
  status TEXT NOT NULL DEFAULT 'pending', -- pending, verified, rejected
  verified_data JSONB,
  verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

**Q4: What is a SIP and how does it differ from a lump-sum investment?**  
A: SIP (Systematic Investment Plan) auto-debits a fixed amount monthly and units are allotted at that day's NAV. Lump-sum is a one-time investment. The platform must schedule SIP mandates (via NACH/e-mandate), track installment dates, handle failures/retries, and show SIP vs one-time in the portfolio view.

**Q5: Explain the NAV cycle and why it matters for transaction processing.**  
A: NAV (Net Asset Value) is declared after market close at ~11 PM IST. Orders placed before 3 PM get that day's NAV; after 3 PM get next business day's NAV. The platform must clearly communicate cut-off times, store the expected NAV at order time, and reconcile after actual NAV is published.

**Q6: What is a folio and why does the platform need to track it?**  
A: A folio is a unique account number assigned by the AMC to track an investor's holdings in a specific fund. When a user first invests in a fund, a folio is created. Subsequent transactions are mapped to the same folio. The platform stores `folio_number` to link transactions and display accurate holdings.

**Q7: How would you design the transaction lifecycle for a mutual fund purchase?**  
A: States: `initiated` → `payment_pending` → `payment_confirmed` → `order_placed` (with AMC/BSE) → `allotted` (units + NAV received) → `reflected_in_portfolio`. Each state transition is recorded with timestamps for audit. Failed states: `payment_failed`, `order_rejected`, `reversed`.

**Q8: What is the role of BSE Star MF or KFintech in the transaction flow?**  
A: BSE Star MF and KFintech are transaction platforms that act as intermediaries between distributors (Aureva) and AMCs. They provide APIs for order placement, status tracking, NAV updates, and commission settlement. The platform integrates with one of these to execute real mutual fund transactions.

**Q9: Why is data integrity critical in a fintech platform and how do you ensure it?**  
A: Financial data errors (wrong balance, duplicate transaction, missing allotment) directly cause monetary loss and regulatory penalties. Ensure via: ACID transactions in PostgreSQL, unique constraints on transaction references, idempotency keys for API calls, reconciliation jobs, and optimistic locking on balance updates.

**Q10: What is the difference between a distributor and an investment advisor in the SEBI context?**  
A: A distributor (AMFI-registered) earns trail commissions and can facilitate transactions. An investment advisor (SEBI-registered RIA) provides fee-based advice and has fiduciary duties. Aureva as a distributor can offer platform-based investment execution but must clearly disclose commission structures and avoid advisory language without RIA registration.

---

## 2. Next.js & React Architecture (Q11–Q22)

**Q11: What are the App Router advantages over Pages Router for a fintech dashboard?**  
A: App Router (Next.js 13+) provides nested layouts (shared dashboard shell), React Server Components for server-rendered data fetching without client JS, streaming with `loading.tsx` for progressive page loads, and server actions for form handling. For fintech: RSCs reduce client bundle (faster load), layouts keep the sidebar/header persistent.

**Q12: How do you implement server-side data fetching for a portfolio dashboard in Next.js?**  
A: Use a Server Component that queries PostgreSQL directly via a typed client (e.g., `@neondatabase/serverless` or Drizzle ORM). The component runs on the server, fetches portfolio data, and passes it to client components for interactive charts.

```tsx
// app/dashboard/page.tsx (Server Component)
import { db } from '@/lib/db';
import { holdings } from '@/lib/schema';
import PortfolioChart from './PortfolioChart'; // client component

export default async function DashboardPage() {
  const data = await db.select().from(holdings).where(eq(holdings.userId, currentUser.id));
  return <PortfolioChart data={data} />;
}
```

**Q13: When would you use client components vs server components in a fintech app?**  
A: Server components for: initial data load, static content, SEO pages. Client components for: interactive charts (D3/Recharts), form inputs, modals, real-time price tickers, anything with `useState`/`useEffect`. Keep the boundary tight — only mark `"use client"` on components that need interactivity.

**Q14: How do you handle authentication state across a Next.js app?**  
A: Use middleware to check JWT/session on every request. The middleware reads the token from an HttpOnly cookie, validates it, and attaches the user ID to `req.headers` or a server context. Server components then read the current user without a client-side auth check. For client components, use a context provider that reads user from an API route on mount.

**Q15: What is React Server Components' impact on bundle size and how does it help a fintech dashboard?**  
A: RSCs run only on the server — their code (including dependencies like date-fns, validation libs) never ships to the client. This dramatically reduces bundle size. For a dashboard-heavy fintech app, this means faster initial load and less client JS for table rendering, calculations, and data formatting.

**Q16: How would you implement optimistic updates for a watchlist feature?**  
A: On click, immediately update local state (UI shows the change), then fire the API call. On success, do nothing (already reflected). On error, roll back the local state and show a toast. Use `useOptimistic` (React 19) or manual state management with a try/catch pattern.

```tsx
const [watchlist, setWatchlist] = useState(initialWatchlist);

const toggleWatchlist = async (fundId: string) => {
  setWatchlist(prev => prev.includes(fundId) ? prev.filter(id => id !== fundId) : [...prev, fundId]);
  try {
    await fetch('/api/watchlist', { method: 'POST', body: JSON.stringify({ fundId }) });
  } catch {
    setWatchlist(prev); // rollback
    toast.error('Failed to update watchlist');
  }
};
```

**Q17: How do you handle form validation in a Next.js registration/KYC flow?**  
A: Use Zod for schema validation on both client (with `react-hook-form` + `zodResolver`) and server (same Zod schema in the API route). This ensures consistent validation — client shows immediate feedback, server rejects invalid payloads regardless.

```ts
const kycSchema = z.object({
  pan: z.string().regex(/^[A-Z]{5}[0-9]{4}[A-Z]$/, 'Invalid PAN format'),
  aadhaar: z.string().regex(/^\d{12}$/, 'Aadhaar must be 12 digits'),
});
```

**Q18: What is ISR and when would you use it on a mutual fund factsheet page?**  
A: ISR (Incremental Static Regeneration) pre-renders a page at build time and revalidates after a set interval. Use for fund factsheet pages — they change daily (NAV, AUM) but don't need real-time freshness. Set `revalidate: 3600` to re-generate every hour, combining SEO-friendly static HTML with near-fresh data.

**Q19: How do you implement loading and error states for async data in Next.js?**  
A: Use `loading.tsx` files in the App Router for Suspense-based loading states. For error handling, use `error.tsx` boundary components. For data fetching in server components, wrap the query in try/catch and return a fallback component. For client components, use `use()` with Suspense or a loading state variable.

**Q20: How would you structure a fintech dashboard's component hierarchy?**  
A: `app/dashboard/layout.tsx` (sidebar + header), `page.tsx` (Server Component, fetches overview), `components/PortfolioSummary.tsx` (client, interactive), `components/HoldingsTable.tsx` (server for initial data, client for sorting/filtering), `components/TransactionHistory.tsx`, `components/PerformanceChart.tsx` (client, D3/Recharts).

**Q21: What are Server Actions and how could they simplify a SIP setup form?**  
A: Server Actions are async functions that run on the server, called directly from form `action` props. No manual API route needed. For SIP setup: the action validates input, checks balance, creates the SIP record in PostgreSQL, and returns success/error — all without a separate fetch call.

**Q22: How do you handle real-time portfolio value updates in a Next.js app?**  
A: Poll a `/api/portfolio-value` endpoint every 30-60 seconds using `setInterval` in a client component, or use Server-Sent Events (SSE) for push-based updates. For WebSocket (overkill for most cases), use a library like `socket.io`. Cache NAV data in Redis to avoid hitting the AMC API on every request.

---

## 3. Node.js & Express Backend (Q23–Q32)

**Q23: What is the role of Express.js in the Aureva stack?**  
A: Express.js serves as the API layer — it routes HTTP requests, applies middleware (auth, rate limiting, validation), and calls service/business logic functions that interact with PostgreSQL. It sits between the Next.js frontend (or external clients) and the database.

```ts
const app = express();
app.use(cors({ origin: process.env.NEXT_PUBLIC_APP_URL }));
app.use(express.json());
app.use('/api/v1', authenticateToken, apiRouter);
```

**Q24: How would you structure an Express.js backend for a fintech platform?**  
A: Layered architecture: `routes/` (define endpoints), `middleware/` (auth, validation, error handler), `controllers/` (request/response handling), `services/` (business logic — transaction processing, KYC, portfolio calculations), `models/` (DB schema), `utils/` (helpers, constants). This separation enables testing each layer independently.

**Q25: How do you implement centralized error handling in Express?**  
A: Use an error-handling middleware at the end of the middleware stack. Create a custom `AppError` class with status code and message. In controllers, call `next(new AppError('Invalid PAN', 400))`. The error middleware catches all, logs, and returns a standardized JSON response.

```ts
class AppError extends Error {
  constructor(public message: string, public statusCode: number) {
    super(message);
  }
}

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err.message });
  }
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});
```

**Q26: What is the purpose of middleware in Express and give fintech-relevant examples?**  
A: Middleware runs before the route handler. Examples: `authenticateToken` (JWT verification), `validateBody` (Zod schema check), `rateLimiter` (prevent abuse), `auditLogger` (log every financial action), `cors` (restrict origins), `helmet` (security headers), `requestId` (trace transactions across services).

**Q27: How do you implement rate limiting for financial API endpoints?**  
A: Use `express-rate-limit` with Redis store for distributed rate limiting. Apply stricter limits on sensitive endpoints (e.g., 5 requests/min for payment initiation, 30 requests/min for portfolio reads). For transaction endpoints, implement idempotency keys to prevent duplicate submissions even if rate limit is bypassed.

```ts
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

const paymentLimiter = rateLimit({
  store: new RedisStore({ sendCommand: (...args) => redis.call(...args) }),
  windowMs: 60 * 1000,
  max: 5,
  message: 'Too many payment requests',
});
```

**Q28: How do you design and implement idempotency for transaction APIs?**  
A: Client sends a unique `X-Idempotency-Key` header. Server checks if a transaction with that key already exists. If yes, return the stored response. If no, process the transaction, store the key-response pair, and return. Use a unique constraint on `(idempotency_key)` in the transactions table.

```sql
CREATE TABLE idempotency_keys (
  key TEXT PRIMARY KEY,
  response JSONB NOT NULL,
  status_code INT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

**Q29: How do you handle file uploads (KYC documents) in Express?**  
A: Use `multer` for multipart form handling. Store files in S3/R2 (not the server filesystem). Validate file type (PDF/JPEG only), enforce size limit (5MB), and scan for malware if available. Store the file URL in the `kyc_verifications` table, never expose raw S3 URLs publicly.

```ts
import multer from 'multer';

const upload = multer({
  storage: multerS3({ s3, bucket: 'aureva-kyc', key: (req, file, cb) => cb(null, `${uuid()}-${file.originalname}`) }),
  limits: { fileSize: 5 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowed = ['application/pdf', 'image/jpeg'];
    cb(null, allowed.includes(file.mimetype));
  },
});
```

**Q30: What is request validation and why is it non-negotiable in fintech?**  
A: Every incoming request must be validated against a strict schema before any business logic runs. In fintech, an unvalidated input could cause incorrect transaction amounts, unauthorized access, or SQL injection. Use Zod or Joi at the middleware layer, never trust the client.

**Q31: How do you implement request logging and audit trails in Express?**  
A: Use `pino` for structured JSON logging. Log every request with `requestId`, `userId`, `endpoint`, `method`, `statusCode`, `duration`. For financial actions (invest, redeem, KYC), write a separate audit record to an `audit_logs` table with before/after state for compliance.

**Q32: What is the difference between a monolithic Express app and splitting into services?**  
A: Start monolithic for the MVP — simpler deployment, faster iteration, easier debugging. Split into services when a component needs independent scaling (e.g., payment processing during month-end SIP runs) or a different tech stack. During the internship, a well-structured monolith with clear module boundaries is ideal.

---

## 4. PostgreSQL & Database Design (Q33–Q44)

**Q33: Why is PostgreSQL a strong choice for a fintech platform over MongoDB?**  
A: PostgreSQL provides ACID transactions (critical for financial data integrity), relational joins (user → portfolio → holdings → transactions), strict schema enforcement (prevents bad data), JSONB for flexible fields (KYC metadata), and mature tooling (migrations, backups, row-level security). MongoDB lacks multi-document ACID transactions by default.

**Q34: Design a database schema for a mutual fund platform's core entities.**  
A:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  phone TEXT UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLEfolios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  fund_id TEXT NOT NULL,
  folio_number TEXT NOT NULL,
  UNIQUE(user_id, fund_id)
);

CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  fund_id TEXT NOT NULL,
  folio_id UUID REFERENCES folios(id),
  type TEXT NOT NULL CHECK (type IN ('purchase', 'sip', 'redemption', 'switch')),
  amount NUMERIC(12,2) NOT NULL,
  units NUMERIC(12,4),
  nav NUMERIC(10,4),
  status TEXT NOT NULL DEFAULT 'initiated',
  idempotency_key TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE sips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  fund_id TEXT NOT NULL,
  amount NUMERIC(12,2) NOT NULL,
  frequency TEXT NOT NULL CHECK (frequency IN ('monthly', 'weekly')),
  start_date DATE NOT NULL,
  next_installment_date DATE,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT now()
);
```

**Q35: What is optimistic locking and how does it prevent double-spending?**  
A: Add a `version` column to the balance/holdings table. When updating, include `WHERE version = ?` in the UPDATE. If the row was modified by another transaction, the update affects 0 rows. Retry or fail. This prevents two concurrent transactions from both succeeding against the same balance.

```sql
-- Read
SELECT balance, version FROM user_balances WHERE user_id = 'u1';

-- Update (check version)
UPDATE user_balances SET balance = balance - 1000, version = version + 1
WHERE user_id = 'u1' AND version = 5;
-- If affected_rows = 0, someone else modified it → retry
```

**Q36: How do you handle database migrations in a fintech project?**  
A: Use a migration tool (Drizzle Kit, Prisma Migrate, or Knex). Every schema change is a versioned migration file. Never alter production DB manually. Run migrations in CI/CD before deploying the app. For zero-downtime deploys, use expand-and-contract: add new columns first, deploy code, then remove old columns.

**Q37: What are JSONB columns and when would you use them in a fintech DB?**  
A: JSONB stores indexed, queryable JSON. Use for semi-structured data: KYC provider responses (`verified_data`), transaction metadata (payment gateway response, AMFI order ID), fund metadata that varies by AMC. Avoid for core financial data (amounts, balances) — those must be typed columns with CHECK constraints.

```sql
ALTER TABLE kyc_verifications ADD COLUMN verified_data JSONB;
-- Query: SELECT verified_data->>'pan' FROM kyc_verifications WHERE user_id = ?;
```

**Q38: How do you design a portfolio holdings table that supports multiple funds?**  
A: A `holdings` table with composite unique key `(user_id, fund_id)` to ensure one holding per fund per user. Update on allotment: if holding exists, add units and recalculate average NAV. If not, insert new row. Use a transaction to ensure atomicity.

```sql
CREATE TABLE holdings (
  user_id UUID NOT NULL REFERENCES users(id),
  fund_id TEXT NOT NULL,
  units NUMERIC(12,4) NOT NULL DEFAULT 0,
  avg_nav NUMERIC(10,4) NOT NULL,
  invested_amount NUMERIC(14,2) NOT NULL DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (user_id, fund_id)
);
```

**Q39: What is row-level security in PostgreSQL and how does it apply to fintech?**  
A: RLS ensures users can only query their own data at the DB level, even if the application has a bug. Create policies: `CREATE POLICY user_isolation ON transactions USING (user_id = current_setting('app.current_user_id')::uuid)`. This prevents data leaks even if a developer forgets a WHERE clause in a query.

**Q40: How do you handle soft deletes vs hard deletes for financial records?**  
A: Financial records should never be hard-deleted (regulatory requirement). Use soft deletes: `deleted_at TIMESTAMPTZ` column. Queries filter `WHERE deleted_at IS NULL`. Physical deletion of financial data violates SEBI audit requirements. Only soft-delete non-critical records (user preferences, watchlists).

**Q41: Explain database indexing strategy for a transactions table.**  
A: Index on `user_id` (most queries filter by user), `(user_id, created_at DESC)` for paginated transaction history, `idempotency_key` UNIQUE index for idempotency checks, and `status` index for background job queries (e.g., find all `pending` transactions). Avoid over-indexing — each index slows writes.

```sql
CREATE INDEX idx_transactions_user_date ON transactions (user_id, created_at DESC);
CREATE UNIQUE INDEX idx_transactions_idempotency ON transactions (idempotency_key);
CREATE INDEX idx_transactions_status ON transactions (status) WHERE status IN ('initiated', 'pending');
```

**Q42: How do you handle data reconciliation between your DB and the AMC's records?**  
A: Run a nightly reconciliation job: pull all transactions from BSE Star MF API, compare against local `transactions` table by order reference. Flag mismatches (amount, status, units). Store reconciliation results in a separate table. Alert on discrepancies. This catches API failures, network issues, and data corruption.

**Q43: What is a materialized view and when would you use it for portfolio analytics?**  
A: A materialized view pre-computes and stores query results. Use for expensive aggregation queries like total portfolio value per user, asset allocation breakdown, or year-wise returns. Refresh on a schedule (every 5-10 minutes) rather than computing on every page load. Great for dashboard performance.

```sql
CREATE MATERIALIZED VIEW portfolio_summary AS
SELECT user_id, SUM(units * latest_nav) as total_value, SUM(invested_amount) as total_invested
FROM holdings JOIN latest_navs ON holdings.fund_id = latest_navs.fund_id
GROUP BY user_id;

-- Refresh every 5 minutes via cron or pg_cron
```

**Q44: How do you ensure data backup and disaster recovery for financial data?**  
A: Enable automated daily backups (pg_dump or managed provider snapshots). For managed Postgres (Neon, Supabase, AWS RDS), enable point-in-time recovery (WAL archiving). Test restore procedures monthly. For compliance, retain backups for 7+ years. Store backups in a different region from the primary DB.

---

## 5. Authentication, OAuth2 & Security (Q45–Q54)

**Q45: How would you implement OAuth2 authentication in a Next.js + Express stack?**  
A: Use NextAuth.js (Auth.js) with a custom Credentials provider + Google/GitHub OAuth providers. NextAuth handles the JWT session in Next.js. For the Express backend, verify the JWT from the `Authorization: Bearer <token>` header. Alternatively, use Clerk (which you've used in GuardrailZ) for a managed solution.

```ts
// Next.js: app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';

export default NextAuth({
  providers: [
    Google({ clientId: GOOGLE_ID, clientSecret: GOOGLE_SECRET }),
    Credentials({ authorize: async (credentials) => { /* validate */ } }),
  ],
});
```

**Q46: What is the difference between JWT and session-based authentication for fintech?**  
A: JWTs are stateless — the token carries user data, verified by signature. Sessions store state on the server (Redis/DB). For fintech: JWTs are fine for read operations but pair with server-side session revocation capability (blacklist in Redis) for logout and security incidents. HttpOnly cookies for JWT storage prevent XSS.

**Q47: How do you implement multi-factor authentication (MFA)?**  
A: After password verification, generate a TOTP secret, store it encrypted in the DB, and return a QR code for Google Authenticator. On login, verify the TOTP code against the stored secret. For SMS OTP, use a provider (Twilio/MSG91), send a 6-digit code with 5-minute expiry, verify server-side, and lock after 5 failed attempts.

```ts
import speakeasy from 'speakeasy';

// Setup
const secret = speakeasy.generateSecret({ name: `Aureva:${email}` });
// Store secret.base32 encrypted in DB

// Verify
const verified = speakeasy.totp.verify({
  secret: storedSecret, encoding: 'base32', token: userToken, window: 1,
});
```

**Q48: What security headers should a fintech web app set?**  
A: Use `helmet` in Express: `Content-Security-Policy` (restrict script sources), `Strict-Transport-Security` (force HTTPS), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (prevent clickjacking), `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (disable camera/mic). In Next.js, configure `headers()` in `next.config.js`.

**Q49: How do you protect against CSRF in a fintech app?**  
A: SameSite cookie attribute (Strict or Lax), CSRF tokens for state-changing POST requests, and verify the `Origin`/`Referer` headers server-side. For API-only backends with token auth, CSRF is less critical (tokens aren't auto-sent by browsers), but still implement for cookie-based sessions.

**Q50: What is OWASP and which top risks are most relevant to fintech?**  
A: OWASP Top 10 — most relevant: A01 (Broken Access Control — users accessing others' portfolios), A02 (Cryptographic Failures — storing PAN/Aadhaar in plaintext), A03 (Injection — SQL injection in transaction queries), A05 (Security Misconfiguration — exposed debug endpoints), A07 (Auth Failures — weak passwords, no MFA).

**Q51: How do you securely store sensitive financial data like PAN and Aadhaar?**  
A: Never store raw PAN/Aadhaar. Store a SHA-256 hash for lookup. Store only the last 4 characters for display. For KYC verification responses, store the verification status and provider reference, not the raw document data. Use envelope encryption for any encrypted data at rest (AWS KMS or similar).

```ts
import crypto from 'crypto';
const panHash = crypto.createHash('sha256').update(pan.toUpperCase()).digest('hex');
```

**Q52: How do you implement API authentication for partner integrations?**  
A: Use OAuth2 client credentials flow: partners get a `client_id` and `client_secret`, exchange them for an access token at `/oauth/token`, use the token in API calls. Rate limit per client. For simpler internal APIs, use API keys with HMAC-based request signing.

**Q53: What is Content Security Policy and why is it critical for fintech?**  
A: CSP whitelists allowed script sources, preventing XSS attacks from injecting malicious scripts. For fintech, an XSS attack could steal session tokens or display fake transaction amounts. Configure strict CSP: `script-src 'self' https://trusted-cdn.com; object-src 'none'; base-uri 'self'`.

**Q54: How do you handle security incidents and user data breaches in a fintech context?**  
A: 1) Contain (revoke compromised tokens, force password resets). 2) Assess scope (which users/data affected). 3) Notify SEBI and affected users within 72 hours (as per CERT-In guidelines). 4) Document root cause. 5) Patch vulnerability. 6) Post-mortem. Have an incident response runbook before launch.

---

## 6. Financial API Integration (Q55–Q62)

**Q55: How would you integrate a KYC verification API into the platform?**  
A: Create an API route `/api/kyc/verify` that accepts PAN/Aadhaar, calls the KYC provider's REST API (e.g., NSDL, DigiLocker, OnGrid), handles the async verification flow (some return immediately, some poll-based), stores the result in the `kyc_verifications` table, and updates the user's KYC status. Always validate input before calling external APIs.

```ts
// app/api/kyc/verify/route.ts
export async function POST(req: Request) {
  const { pan, aadhaar } = kycSchema.parse(await req.json());
  const result = await kyCProvider.verify({ pan, aadhaar });
  await db.insert(kycVerifications).values({ userId, provider: 'nsdl', status: result.status, verifiedData: result.data });
  return Response.json({ status: result.status });
}
```

**Q56: How do you handle external API failures gracefully?**  
A: Implement retry with exponential backoff (3 retries, 1s/2s/4s delays). Circuit breaker pattern: after N consecutive failures, stop calling for a cooldown period. Fallback to a degraded experience (show "KYC verification pending" instead of failing silently). Log failures with context for debugging. Set timeout on every external call (5-10 seconds).

**Q57: What is a payment gateway integration and how does it work for mutual fund purchases?**  
A: For lump-sum purchases: redirect user to payment gateway (Razorpay/PayU) → user completes payment → gateway sends webhook callback → platform verifies payment signature → marks transaction as `payment_confirmed` → places order with AMC. For SIPs: set up e-mandate (NACH) for auto-debit on each installment date.

**Q58: How do you verify payment gateway callbacks securely?**  
A: Every payment gateway sends a webhook with a signature. Verify it using the gateway's secret key and HMAC algorithm before processing. Never trust the callback payload alone — also query the gateway's API to confirm the payment status. This prevents forged callbacks that could trick the system into marking unpaid transactions as confirmed.

```ts
import crypto from 'crypto';

function verifyRazorpaySignature(orderId: string, paymentId: string, signature: string): boolean {
  const expected = crypto.createHmac('sha256', RAZORPAY_SECRET)
    .update(`${orderId}|${paymentId}`).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

**Q59: How do you handle payment failures and retries?**  
A: On payment failure: mark transaction as `payment_failed`, show clear error to user, allow retry. For SIP installments: implement retry logic (retry after 1 day, then 3 days, then mark as failed after 3 attempts). Track retry count in the `transactions` table. Notify the user via email/SMS on each failure.

**Q60: What is an e-mandate and how does it enable SIP auto-debit?**  
A: E-mandate (NACH) is an authorization from the user to auto-debit their bank account on scheduled dates. Flow: user sets up mandate via the platform → mandate is registered with NPCI → on each SIP date, the platform triggers a debit request → bank processes → if successful, order is placed with AMC. Use APIs from Razorpay or Cashfree for mandate management.

**Q61: How would you integrate a mutual fund data API for fund details and NAVs?**  
A: Use AMFI's NAV feed (daily CSV download) or a paid API (ValueResearch, Morningstar India, Kuvera API). Store fund metadata (name, category, benchmark, expense ratio) in a `funds` table. Store daily NAVs in a `nav_history` table with `(fund_id, date)` as composite key. Update daily via a cron job after market hours.

```sql
CREATE TABLE nav_history (
  fund_id TEXT NOT NULL,
  date DATE NOT NULL,
  nav NUMERIC(10,4) NOT NULL,
  PRIMARY KEY (fund_id, date)
);
```

**Q62: How do you handle API versioning when integrating multiple external services?**  
A: Use URL-based versioning (`/api/v1/...`) for your own APIs. For external APIs, pin to a specific version and monitor for deprecation notices. Abstract external API calls behind an adapter/service interface so swapping providers doesn't require changing business logic. Example: `KYCService` interface with `NSDLProvider` and `DigiLockerProvider` implementations.

---

## 7. TypeScript & Type Safety (Q63–Q70)

**Q63: Why is TypeScript essential for a fintech codebase?**  
A: TypeScript catches type errors at compile time — a wrong field name on a transaction object, a missing required parameter, or an incorrect return type are caught before runtime. In fintech, this prevents entire classes of bugs (passing `string` where `number` is expected for an amount). It also enables better IDE support and refactoring safety.

**Q64: How do you type API request/response objects in a Next.js + Express stack?**  
A: Define shared types in a `types/` package. Backend validates with Zod (which infers TypeScript types). Frontend uses the inferred types for API calls.

```ts
// shared/types/transaction.ts
import { z } from 'zod';

export const CreateTransactionSchema = z.object({
  fundId: z.string(),
  amount: z.number().positive().max(10000000),
  type: z.enum(['purchase', 'redemption']),
});

export type CreateTransaction = z.infer<typeof CreateTransactionSchema>;
```

**Q65: How do you type a PostgreSQL query result for use in React components?**  
A: Use Drizzle ORM or `pg` with explicit type annotations. With Drizzle, the schema definition generates types automatically. With raw `pg`, define interfaces matching the table structure.

```ts
import { pgTable, uuid, text, numeric } from 'drizzle-orm/pg-core';

export const holdings = pgTable('holdings', {
  userId: uuid('user_id').notNull(),
  fundId: text('fund_id').notNull(),
  units: numeric('units', { precision: 12, scale: 4 }).notNull(),
});

// Query result is automatically typed as { userId: string; fundId: string; units: string }[]
```

**Q66: What are discriminated unions and how are they useful in fintech state management?**  
A: Discriminated unions use a common literal property to narrow types. Useful for transaction states where each state has different data.

```ts
type TransactionState =
  | { status: 'initiated'; amount: number }
  | { status: 'payment_pending'; paymentUrl: string }
  | { status: 'allotted'; units: number; nav: number; folioNumber: string }
  | { status: 'failed'; errorCode: string; reason: string };

function renderTransaction(tx: TransactionState) {
  switch (tx.status) {
    case 'allotted': return <span>{tx.units} units at ₹{tx.nav}</span>;
    case 'failed': return <span>Error: {tx.reason}</span>;
    // TypeScript narrows tx correctly in each branch
  }
}
```

**Q67: How do you use TypeScript to prevent common financial calculation errors?**  
A: Create branded types for monetary values to prevent mixing up amounts, NAVs, and percentages.

```ts
type Amount = number & { readonly __brand: 'Amount' };
type NAV = number & { readonly __brand: 'NAV' };
type Percentage = number & { readonly __brand: 'Percentage' };

function calculateReturns(invested: Amount, current: Amount): Percentage {
  return ((current - invested) / invested * 100) as Percentage;
}
// Passing a NAV where Amount is expected would be a compile error
```

**Q68: How do you type environment variables safely in Next.js?**  
A: Create a `env.ts` file that validates env vars at startup using Zod. This catches missing env vars at build time rather than crashing at runtime.

```ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  RAZORPAY_KEY_ID: z.string().startsWith('rzp_'),
  RAZORPAY_KEY_SECRET: z.string(),
});

export const env = envSchema.parse(process.env);
```

**Q69: What are TypeScript utility types useful for in a fintech app?**  
A: `Pick<User, 'id' | 'email'>` for API responses that shouldn't expose all fields. `Partial<Transaction>` for update payloads. `Record<FundCategory, number>` for asset allocation. `Omit<Transaction, 'id' | 'createdAt'>` for creation payloads. `Required<SIPConfig>` to ensure all fields are provided.

**Q70: How do you handle API error typing in TypeScript?**  
A: Define a typed error response and use it consistently.

```ts
type ApiError = {
  error: string;
  code: string;
  details?: Record<string, string[]>;
};

// In API route
function errorResponse(message: string, status: number, code: string): Response {
  return Response.json({ error: message, code } satisfies ApiError, { status });
}

// In fetch wrapper
async function apiFetch<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw await res.json() as ApiError;
  return res.json() as Promise<T>;
}
```

---

## 8. MongoDB & NoSQL (Q71–Q74)

**Q71: When would you use MongoDB alongside PostgreSQL in a fintech platform?**  
A: Use PostgreSQL for all financial data (transactions, holdings, users, portfolios). Use MongoDB for non-critical, high-write data: chat conversations with support, user activity logs, temporary session data, or fund review/rating content. MongoDB's flexible schema suits unstructured data; PostgreSQL's ACID guarantees suit financial records.

**Q72: How would you model user activity analytics in MongoDB?**  
A: Use a time-series collection for efficient storage and querying of page views, feature usage, and session data.

```js
// MongoDB time-series collection
db.createCollection("user_events", {
  timeseries: { timeField: "timestamp", metaField: "userId", granularity: "hours" }
});
// Document
{ timestamp: new Date(), userId: "u1", event: "page_view", page: "/portfolio", duration: 4500 }
```

**Q73: What are the trade-offs of using MongoDB for transactional data?**  
A: MongoDB supports multi-document ACID transactions since v4.0, but they add overhead and aren't as mature as PostgreSQL's. For fintech: use MongoDB only if you need horizontal scaling of non-financial data. Financial records belong in PostgreSQL where constraints, foreign keys, and rollback are battle-tested.

**Q74: How do you handle data sync between PostgreSQL and MongoDB?**  
A: For non-critical sync (e.g., user profile changes reflected in analytics), use an event-driven approach: after a PostgreSQL write, emit an event (via internal pub/sub or a queue like BullMQ), and a consumer writes to MongoDB. For critical financial data, PostgreSQL is the single source of truth — no sync needed.

---

## 9. Docker, CI/CD & Deployment (Q75–Q82)

**Q75: How would you containerize a Next.js + Express + PostgreSQL stack?**  
A: Use Docker Compose with three services: `app` (Next.js frontend), `api` (Express backend), `db` (PostgreSQL). The Next.js app connects to Express API. Express connects to PostgreSQL. Use `.env` files for secrets. For production, use managed PostgreSQL (Neon, Supabase, RDS) and deploy frontend to Vercel, backend to Render/Railway.

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: aureva
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: [pgdata:/var/lib/postgresql/data]
  api:
    build: ./api
    depends_on: [db]
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/aureva
  app:
    build: ./frontend
    depends_on: [api]
```

**Q76: Write a Dockerfile for a Next.js fintech app.**  
A:

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

**Q77: What does a CI/CD pipeline for a fintech app look like?**  
A: GitHub Actions workflow: 1) On PR: lint, type-check, unit tests, build Docker image. 2) On merge to main: run integration tests against test DB, deploy to staging, run smoke tests. 3) Manual approval → deploy to production. 4) Post-deploy: health check, notification. Include secret scanning and dependency vulnerability scanning.

```yaml
# .github/workflows/deploy.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - run: npm run build
      - run: npm run db:migrate
      - run: # deploy to Vercel/Render
```

**Q78: How do you manage secrets and environment variables securely?**  
A: Never commit `.env` files. Use GitHub Secrets for CI/CD. For production: use Vercel/Render environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault). Rotate secrets quarterly. For database credentials, use connection pooling (PgBouncer) to limit exposure. Use different credentials for staging and production.

**Q79: How do you handle database migrations during deployment?**  
A: Run migrations as a separate step before the app starts. In CI/CD: `npm run db:migrate` → `npm run deploy`. Use transactional migrations (wrapped in BEGIN/COMMIT) so failures roll back cleanly. For zero-downtime: deploy the migration first, then deploy the code that uses the new schema (expand-contract pattern).

**Q80: What is the difference between deploying on Vercel vs a VPS for a fintech app?**  
A: Vercel handles Next.js deployment perfectly (edge functions, ISR, preview deploys) but you can't run a persistent Express server or background jobs. Options: Vercel for frontend + Render/Fly.io for Express API + managed PostgreSQL. Or a single VPS (DigitalOcean, AWS EC2) for everything if you need full control.

**Q81: How do you set up monitoring and alerting for a fintech platform?**  
A: Application: structured logging (Pino → stdout → log aggregator). Metrics: request latency, error rates, transaction success rate (Prometheus/Grafana). Alerting: PagerDuty/Slack on error rate spike, failed transaction threshold, DB connection pool exhaustion. Uptime: Health check endpoint `/health` monitored by UptimeRobot/BetterStack.

**Q82: How do you handle CORS for a fintech app with frontend on Vercel and backend on Render?**  
A: Set `Access-Control-Allow-Origin: https://aureva.vercel.app` in Express CORS config. Allow specific headers (`Authorization`, `Content-Type`). Allow `credentials: true` for cookie-based auth. Never use `*` origin in production. Also set CORS headers in Next.js config for any backend calls from server components.

---

## 10. MVP Development & Startup Mindset (Q83–Q88)

**Q83: How would you approach building the Aureva MVP in a 4-month internship?**  
A: Month 1: Core auth (JWT + OAuth), user registration, KYC flow, PostgreSQL schema. Month 2: Fund browsing, portfolio dashboard, transaction initiation. Month 3: Payment integration, SIP setup, AMC API integration. Month 4: Polish, testing, deployment, onboarding first users. Ship early, iterate based on founder feedback.

**Q84: How do you prioritize features when building an MVP with limited time?**  
A: Focus on the critical path: a user must be able to register → complete KYC → browse funds → invest → see portfolio. Defer nice-to-haves: advanced charts, notifications, multi-language. Use the MoSCoW method with the founder. Ship the smallest version of each feature, get feedback, then improve.

**Q85: How do you handle ambiguity and changing requirements in a startup?**  
A: Communicate proactively with the founder — clarify intent, not just the ask. Build modular code so changes don't cascade. Use feature flags to ship incrementally. Document decisions. Accept that startup scope shifts are normal; focus on building systems that adapt, not just features that ship.

**Q86: What does "strong ownership" mean in the context of this internship?**  
A: Taking responsibility for the full stack — not just coding, but debugging production issues, writing documentation, making deployment decisions, and following up when something breaks. If a user reports a transaction error at 10 PM, you investigate. It means treating the product as if it's yours.

**Q87: How would you onboard the first 10 users and incorporate feedback?**  
A: Deploy to a staging environment, invite users (friends/family or early adopters), provide a feedback form or WhatsApp group, watch session recordings (PostHog/Hotjar), fix critical bugs within 24 hours, add features based on user requests. Ship updates weekly. Treat every bug report as a priority.

**Q88: How do you balance speed and code quality in an MVP?**  
A: Don't skip: type safety (TypeScript), basic tests for critical paths (transaction flow), input validation, error handling. Defer: 100% test coverage, advanced caching, microservices architecture, comprehensive documentation. A well-typed codebase with validation and error boundaries prevents most production issues while moving fast.

---

## 11. D3.js & Financial Visualization (Q89–Q92)

**Q89: Why is D3.js beneficial for a fintech dashboard?**  
A: D3.js gives pixel-level control for custom financial charts: candlestick charts, portfolio allocation treemaps, SIP projection curves, and benchmark comparison line charts. React chart libraries (Recharts) are faster to implement but D3 excels when you need non-standard visualizations like interactive fund comparison or custom tooltips with NAV history.

**Q90: How would you implement a portfolio allocation pie chart with D3.js in React?**  
A: Use D3's `d3.arc()` and `d3.pie()` to compute arc paths, render as SVG in a React component. Pass data as props, use `useRef` for the SVG element, and `useEffect` to bind D3. For a simpler approach, use Recharts' `<PieChart>` with custom labels.

```tsx
'use client';
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function AllocationChart({ data }: { data: { label: string; value: number }[] }) {
  const svgRef = useRef<SVGSVGElement>(null);
  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const pie = d3.pie<{ label: string; value: number }>().value(d => d.value);
    const arc = d3.arc<d3.PieArcDatum<{ label: string; value: number }>>().innerRadius(60).outerRadius(120);
    svg.selectAll('path').data(pie(data)).join('path').attr('d', arc).attr('fill', (d, i) => d3.schemeCategory10[i]);
  }, [data]);
  return <svg ref={svgRef} width={260} height={260} />;
}
```

**Q91: How would you build an interactive NAV history line chart?**  
A: Use D3's `d3.line()` with `d3.scaleTime()` for x-axis and `d3.scaleLinear()` for y-axis. Add hover tooltips showing exact NAV and date. For React, consider `visx` (Airbnb's D3+React library) or `react-financial-charts` which provides pre-built OHLC/candlestick components.

**Q92: What are alternatives to D3.js for financial charting in a React app?**  
A: 1) Recharts — simple, declarative, good enough for basic line/bar/pie. 2) Lightweight Charts (TradingView) — free, optimized for financial time-series. 3) react-financial-charts — OHLC, volume, indicators. 4) visx — low-level D3 primitives for React. For MVP: start with Recharts/Lightweight Charts; switch to D3 only if custom visualization needs arise.

---

## 12. Behavioral & Culture Fit (Q93–Q100)

**Q93: Why are you interested in fintech and specifically Aureva Wealth?**  
A: Fintech combines complex engineering challenges with real financial impact. Aureva is building a platform from scratch — rare opportunity to shape architecture, make product decisions, and see direct impact on real users. My background in full-stack development with PostgreSQL and auth systems aligns directly with the role. Building investment tools for Indian users excites me.

**Q94: Describe a time you took ownership of a project end-to-end.**  
A: GuardrailZ — I identified a problem (LLM guardrails), designed the architecture (Next.js + Clerk + regex engine), built and deployed it solo on Vercel, iterated based on feedback, and presented it as a live product. Similar ownership is what this role demands — building Aureva's platform from zero to MVP with the founder.

**Q95: How do you handle working with a founder in a fast-paced startup?**  
A: I'd establish a weekly sync cadence for priorities, use async communication (Notion/Slack) for updates, ask clarifying questions early, and not wait for perfect specifications to start building. Ship a rough version, get feedback, iterate. My experience as an AI Agent Developer (building solo with API auth and database) demonstrates this self-directed work style.

**Q96: What would you do if you discovered a critical bug in production affecting user investments?**  
A: 1) Immediately assess severity — is it showing wrong data or causing actual financial loss? 2) If financial impact: take the affected endpoint down, notify the founder, and start rollback. 3) If display-only: hotfix within hours. 4) Document the root cause. 5) Add a test/regression to prevent recurrence. Never silently fix — always communicate.

**Q97: How do you learn a new technology stack quickly?**  
A: Build a small project. I learned FastAPI by building microservices during my Agentic AI internship, Next.js by building GuardrailZ, and PostgreSQL by designing schemas for multiple projects. Reading docs is necessary but building is how I retain. For this role, I'd start by cloning Aureva's codebase, understanding the schema, and shipping a small feature within the first week.

**Q98: How would you handle a disagreement with the founder on a technical decision?**  
A: Present data and trade-offs, not opinions. If the founder wants MongoDB for financial data, I'd show a quick comparison: "Here's why PostgreSQL gives us ACID and foreign keys for transaction integrity — and here's when we'd use MongoDB for activity logs." Recommend, then commit to the final decision even if I disagree.

**Q99: What does accountability mean to you in a development team?**  
A: If I say the KYC integration will be done by Friday, I deliver by Friday — or communicate proactively on Thursday if it'll slip. If my code causes a production issue, I own it, fix it, and document what went wrong. No blame-shifting. During my AI Agent Developer work, I built and maintained the entire backend solo — every bug was mine to fix.

**Q100: Where do you see this internship fitting into your career goals?**  
A: This internship is the intersection of everything I want to do: full-stack engineering at a startup, building a product from scratch with real users, and fintech domain knowledge. After 4 months, I expect to have shipped a production platform, gained deep PostgreSQL and OAuth experience, and contributed meaningfully to Aureva's growth. It also strengthens my foundation for a full-time SWE role in fintech.
