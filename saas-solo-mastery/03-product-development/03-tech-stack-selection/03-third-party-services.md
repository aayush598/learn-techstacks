# Essential Third-Party Services for Solo SaaS

## The Service Selection Philosophy

As a solo founder, your time is your most scarce resource. Every service you use should either (a) save you significant development time or (b) provide reliability you can't achieve on your own. The goal is to buy commodity functionality so you can focus on your differentiator.

This guide covers every category of third-party service a SaaS needs, with specific recommendations for solo founders at different stages, pricing, and integration patterns.

## The Solo Founder's Service Stack

### MVP Phase (0-50 customers, $0-100/mo total spend)

```markdown
Auth:            Clerk / Supabase Auth ($0)
Database:        Supabase or Neon ($0)
Payments:        Stripe or Lemon Squeezy ($0 + fees)
Email:           Resend ($0)
Monitoring:      Sentry ($0) + Better Uptime ($0)
Hosting:         Vercel + Supabase ($0)
Domain:          Cloudflare ($0 for DNS)
Analytics:       Plausible or Umami ($0)
Support:         Intercom or Crisp ($0)
File Storage:    Uploadthing or Tigris ($0)
CDN:             Cloudflare ($0)
Backups:         Built-in DB backups ($0)
```

### Growth Phase (50-1000 customers, $100-500/mo total spend)

```markdown
Auth:            Clerk ($25/mo) or Auth0 ($23/mo)
Database:        Supabase Pro ($25/mo) or RDS ($15/mo)
Payments:        Stripe + Paddle for EU VAT ($0 + fees)
Email:           Resend ($20/mo) or SendGrid ($20/mo)
Monitoring:      Sentry ($26/mo) + Datadog ($15/mo)
Hosting:         Vercel Pro ($20/mo) or Railway ($20/mo)
Analytics:       Plausible ($9/mo) or PostHog ($0)
Support:         Intercom ($39/mo) or Crisp ($25/mo)
File Storage:    AWS S3 ($5/mo)
CDN:             Cloudflare Pro ($20/mo) or Bunny ($10/mo)
Backups:         pg_dump to S3 (cron job, $0)
```

### Scale Phase (1000+ customers, $500+/mo total spend)

```markdown
Auth:            Clerk ($100/mo) or Auth0 Enterprise
Database:        RDS or Cloud SQL ($50-200/mo)
Payments:        Stripe + Paddle + Invoicing
Email:           AWS SES + Resend/SendGrid for marketing
Monitoring:      Datadog ($100+/mo) or Grafana stack
Hosting:         Self-hosted on VPS or k8s ($50-200/mo)
Analytics:       PostHog self-hosted or Mixpanel
Support:         Intercom Pro or Zendesk
CDN:             Cloudflare Business or Bunny
Backups:         Automated, cross-region
```

## Authentication Services

### Comparison

```markdown
| Service      | Free Tier          | Paid Start | Best For                       |
|--------------|--------------------|------------|--------------------------------|
| Clerk        | 10k users          | $25/mo     | Best DX, Next.js-friendly      |
| Supabase Auth| 50k users          | $25/mo     | All-in-one with DB             |
| NextAuth     | Free (open source) | $0         | Next.js only, self-hosted      |
| Auth0        | 7k users           | $23/mo     | Enterprise features            |
| Firebase Auth| Free (limits)      | $25/mo     | Google ecosystem               |
| Lucia        | Free (open source) | $0         | DIY auth, full control         |
| WorkOS       | 1m users           | $99/mo     | Enterprise SSO, directory sync |
```

### Recommendation: Clerk

Clerk is the best auth option for solo founders building modern SaaS. It provides:

- Multiple auth methods (email, Google, GitHub, magic links)
- User management dashboard
- Organization/team support
- Webhook integration
- Built-in components for React/Next.js

```typescript
// app/layout.tsx - Clerk provider setup
import { ClerkProvider, SignedIn, SignedOut, UserButton } from '@clerk/nextjs';

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html>
        <body>
          <SignedIn>
            <UserButton />
          </SignedIn>
          <SignedOut>
            <SignInButton />
          </SignedOut>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

### Integration Pattern: Auth Webhook

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';

export async function POST(req: Request) {
  const headerPayload = headers();
  const svixId = headerPayload.get('svix-id');
  const svixTimestamp = headerPayload.get('svix-timestamp');
  const svixSignature = headerPayload.get('svix-signature');

  if (!svixId || !svixTimestamp || !svixSignature) {
    return new Response('Missing svix headers', { status: 400 });
  }

  const payload = await req.json();
  const body = JSON.stringify(payload);

  const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET!);
  let event: { type: string; data: any };

  try {
    event = wh.verify(body, {
      'svix-id': svixId,
      'svix-timestamp': svixTimestamp,
      'svix-signature': svixSignature,
    }) as any;
  } catch (err) {
    return new Response('Invalid signature', { status: 400 });
  }

  switch (event.type) {
    case 'user.created':
      await createUserInDatabase(event.data);
      break;
    case 'user.updated':
      await updateUserInDatabase(event.data);
      break;
    case 'user.deleted':
      await deleteUserFromDatabase(event.data);
      break;
    case 'organization.created':
      await createTeamInDatabase(event.data);
      break;
  }

  return new Response('OK', { status: 200 });
}
```

## Payment Processing

### Comparison

```markdown
| Service         | Fees            | Payouts         | Best For                      |
|-----------------|-----------------|-----------------|-------------------------------|
| Stripe          | 2.9% + $0.30   | 2 business days | Global, developer-friendly    |
| Lemon Squeezy   | 5% + $0.50     | 7-14 days       | Handles EU VAT, simpler       |
| Paddle          | 5% + $0.50     | 7 days          | Enterprise, compliance        |
| Chargebee       | N/A            | N/A             | Subscription management (addon)|
| Recurly         | N/A            | N/A             | Subscription management       |
| RevenueCat      | Free tier      | Varies          | In-app purchases, mobile      |
| Braintree       | 2.9% + $0.30  | 2 business days | PayPal integration            |
| Polar.sh        | 5%             | Varies          | Open source friendly          |
```

### Recommendation: Stripe (Primary) + Lemon Squeezy (EU Backup)

Stripe is the standard for online payments. For solo founders, their API and documentation are unmatched.

```typescript
// lib/stripe/client.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
});

// lib/stripe/checkout.ts
export async function createCheckoutSession(params: {
  userId: string;
  priceId: string;
  mode: 'payment' | 'subscription';
  successUrl: string;
  cancelUrl: string;
}) {
  const session = await stripe.checkout.sessions.create({
    mode: params.mode,
    line_items: [{ price: params.priceId, quantity: 1 }],
    success_url: params.successUrl,
    cancel_url: params.cancelUrl,
    client_reference_id: params.userId,
    metadata: { userId: params.userId },
  });

  return session;
}
```

### Stripe Webhook Handling

```typescript
// app/api/webhooks/stripe/route.ts
import { stripe } from '@/lib/stripe/client';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Invalid signature', { status: 400 });
  }

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object;
      await activateSubscription(
        session.client_reference_id!,
        session.subscription as string
      );
      break;
    }
    case 'customer.subscription.updated': {
      const subscription = event.data.object;
      await syncSubscriptionStatus(subscription);
      break;
    }
    case 'customer.subscription.deleted': {
      const subscription = event.data.object;
      await cancelSubscription(subscription.id);
      break;
    }
    case 'invoice.paid': {
      const invoice = event.data.object;
      await recordPayment(invoice);
      break;
    }
    case 'invoice.payment_failed': {
      const invoice = event.data.object;
      await handleFailedPayment(invoice);
      break;
    }
  }

  return new Response('OK', { status: 200 });
}
```

### Lemon Squeezy (Alternative for EU Simplification)

```typescript
// lib/lemonsqueezy/client.ts
import { LemonSqueezy } from '@lemonsqueezy/lemonjs';

const ls = new LemonSqueezy(process.env.LEMONSQUEEZY_API_KEY!);

export async function createCheckout(params: {
  variantId: string;
  userId: string;
  email: string;
}) {
  const checkout = await ls.createCheckout({
    productVariantId: params.variantId,
    email: params.email,
    custom: { userId: params.userId },
    redirectUrl: `${process.env.NEXT_PUBLIC_URL}/dashboard`,
  });

  return checkout;
}
```

## Email Services

### Comparison

```markdown
| Service    | Free Tier          | Paid Start  | Best For                    |
|------------|--------------------|-------------|-----------------------------|
| Resend     | 100/day            | $20/mo      | Developer-friendly, modern  |
| SendGrid   | 100/day            | $20/mo      | Reliable, established       |
| AWS SES    | 62k/month          | $0.10/1k    | Cheap at scale              |
| Mailgun    | 5k/month           | $35/mo      | Developers, APIs            |
| Postmark   | None               | $15/mo      | Transactional, deliverability|
| Loops      | 500/month          | $30/mo      | Marketing + transactional   |
| ConvertKit | 1k subscribers     | $29/mo      | Newsletter/creator          |
| MailerLite | 1k subscribers     | $10/mo      | Email marketing             |
```

### Recommendation: Resend (Transactional) + Loops (Marketing)

Resend provides the best developer experience for transactional emails. Loops combines marketing and transactional in one platform.

```typescript
// lib/email/resend.ts
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY!);

const emailTemplates = {
  welcome: {
    subject: 'Welcome to {product_name}!',
    html: (vars: Record<string, string>) => `
      <h1>Welcome to ${vars.product_name}!</h1>
      <p>Hi ${vars.name},</p>
      <p>We're excited to have you on board. Here's how to get started:</p>
      <ol>
        <li><a href="${vars.dashboard_url}">Visit your dashboard</a></li>
        <li>Create your first project</li>
        <li>Invite your team</li>
      </ol>
      <p>If you have any questions, just reply to this email.</p>
    `,
  },
  invoice: {
    subject: 'Your {product_name} invoice is ready',
    html: (vars: Record<string, string>) => `
      <h1>Invoice #${vars.invoice_number}</h1>
      <p>Amount: $${vars.amount}</p>
      <p>Date: ${vars.date}</p>
      <p><a href="${vars.invoice_url}">View invoice</a></p>
    `,
  },
  reset_password: {
    subject: 'Reset your password',
    html: (vars: Record<string, string>) => `
      <p>Click <a href="${vars.reset_url}">here</a> to reset your password.</p>
      <p>This link expires in 1 hour.</p>
    `,
  },
};

export async function sendEmail(params: {
  to: string;
  template: keyof typeof emailTemplates;
  variables: Record<string, string>;
}) {
  const template = emailTemplates[params.template];

  await resend.emails.send({
    from: `${process.env.PRODUCT_NAME} <noreply@${process.env.DOMAIN}>`,
    to: params.to,
    subject: template.subject.replace(/{(\w+)}/g, (_, k) => params.variables[k]),
    html: template.html(params.variables),
  });
}
```

## Error Monitoring

### Comparison

```markdown
| Service    | Free Tier          | Paid Start | Best For                    |
|------------|--------------------|------------|-----------------------------|
| Sentry     | 5k events/mo       | $26/mo     | Best overall error tracking |
| Bugsnag    | 7.5k events/mo     | $29/mo     | Stability scores            |
| Rollbar    | 5k events/mo       | $22/mo     | AI-assisted debugging       |
| Raygun     | 10k events/mo      | $25/mo     | APM + error tracking        |
| Highlight  | Free (open source) | $0         | Self-hostable               |
| LogRocket  | 1k sessions/mo     | $40/mo     | Session replay + errors     |
```

### Recommendation: Sentry

```typescript
// lib/monitoring/sentry.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1, // Sample 10% of transactions
  profilesSampleRate: 0.1,

  // Capture more context
  beforeSend(event) {
    // Remove sensitive data
    if (event.request?.headers) {
      delete event.request.headers['Authorization'];
      delete event.request.headers['Cookie'];
    }
    return event;
  },
});

// Usage in API routes
export async function someHandler() {
  try {
    // risky operation
  } catch (error) {
    Sentry.captureException(error, {
      tags: { feature: 'payment', priority: 'high' },
      extra: { userId: currentUser.id },
    });
    throw error; // Re-throw for API error response
  }
}

// User feedback widget
export function useReportFeedback() {
  return {
    showReportDialog: (errorId: string) => {
      Sentry.showReportDialog({ eventId: errorId });
    },
  };
}
```

## Uptime Monitoring

### Comparison

```markdown
| Service       | Free Tier    | Paid Start | Best For                    |
|---------------|--------------|------------|-----------------------------|
| Better Uptime | 1 monitor    | $20/mo     | Status pages + monitoring   |
| UptimeRobot   | 5 monitors   | $7/mo      | Simple, cheap               |
| Checkly       | 5 checks     | $30/mo     | Browser checks, API checks  |
| Cronitor      | 5 monitors   | $10/mo     | Cron job monitoring         |
| Pulsetic      | 3 monitors   | $9/mo      | Status pages                |
| Instatus      | Free         | $20/mo     | Status pages only           |
```

### Recommendation: Better Uptime

Better Uptime provides monitoring, status pages, and on-call scheduling in one product.

```typescript
// lib/monitoring/uptime.ts
// Endpoint for Better Uptime to ping
export async function GET(req: Request) {
  // Check critical services
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
    checkLLMAvailability(),
  ]);

  const allHealthy = checks.every(
    c => c.status === 'fulfilled' && c.value === true
  );

  return Response.json(
    { status: allHealthy ? 'up' : 'degraded' },
    { status: allHealthy ? 200 : 503 }
  );
}
```

## Hosting Platforms

### Comparison

```markdown
| Platform     | Free Tier         | Paid Start | Best For                    |
|--------------|-------------------|------------|-----------------------------|
| Vercel       | Generous free     | $20/mo     | Next.js, frontend-heavy     |
| Railway      | $5 credit         | $5/mo      | Any stack, simple deploys   |
| Fly.io       | Free tier         | $19/mo     | Global deployment           |
| Render       | Free tier         | $7/mo      | Any stack, simple           |
| DigitalOcean | None              | $6/mo      | VPS, full control           |
| Hetzner      | None              | $4/mo      | Cheap VPS, EU               |
| AWS EC2      | 1 year free tier  | $8.50/mo   | Full control, complex       |
| Google Cloud | $300 credit       | Varies     | GCP ecosystem               |
| Netlify      | Generous free     | $19/mo     | Static sites, functions     |
| Cloudflare   | Free tier         | $25/mo     | Workers, Pages, global      |
```

### Recommendation: Vercel + Supabase (MVP) moving to Hetzner VPS (Scale)

```typescript
// vercel.json
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "crons": [
    {
      "path": "/api/crons/billing",
      "schedule": "0 0 * * *"
    }
  ]
}
```

## Database Hosting

### Comparison

```markdown
| Service    | Free Tier          | Paid Start  | Best For                    |
|------------|--------------------|-------------|-----------------------------|
| Supabase   | 500MB DB           | $25/mo      | All-in-one backend          |
| Neon       | 0.5GB DB           | $19/mo      | Serverless Postgres         |
| Railway    | $5 credit          | $5/mo       | Simple, integrated          |
| Render     | 256MB RAM          | $7/mo       | Managed Postgres            |
| AWS RDS    | Free tier (1yr)    | $15/mo      | Reliable, scalable          |
| DigitalOcean| None              | $12/mo      | Managed, simple             |
| PlanetScale | 1GB storage        | $29/mo      | MySQL, branching flows      |
| CockroachDB| Free tier          | $25/mo      | Distributed SQL, serverless |
| TiDB       | Free tier          | $20/mo      | MySQL-compatible, serverless|
```

### Recommendation: Supabase (MVP) → Neon (Scale) → RDS (Enterprise)

## File and Asset Storage

### Comparison

```markdown
| Service        | Free Tier         | Paid Start | Best For                    |
|----------------|-------------------|------------|-----------------------------|
| AWS S3         | 5GB free          | $0.023/GB  | Standard, reliable          |
| Cloudflare R2  | 10GB free         | $0.015/GB  | No egress fees, global      |
| Uploadthing    | 2GB               | $10/mo     | Developer-friendly uploads  |
| Tigris         | 5GB free          | $0.02/GB   | S3-compatible, global       |
| Supabase Storage| 1GB               | $10/mo     | Integrated with Supabase    |
| Backblaze B2   | 10GB free         | $0.006/GB  | Cheapest storage            |
| Bunny Storage  | None              | $0.005/GB  | CDN + storage, global       |
```

### Recommendation: Cloudflare R2 (no egress fees, global, cheap)

```typescript
// lib/storage/r2.ts
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';

const r2 = new S3Client({
  region: 'auto',
  endpoint: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY!,
    secretAccessKey: process.env.R2_SECRET_KEY!,
  },
});

export async function uploadFile(params: {
  key: string;
  body: Buffer | ReadableStream;
  contentType: string;
}) {
  await r2.send(new PutObjectCommand({
    Bucket: process.env.R2_BUCKET!,
    Key: params.key,
    Body: params.body,
    ContentType: params.contentType,
  }));

  return {
    url: `https://${process.env.R2_PUBLIC_URL}/${params.key}`,
    key: params.key,
  };
}
```

## Analytics

### Comparison

```markdown
| Service    | Free Tier          | Paid Start | Best For                    |
|------------|--------------------|------------|-----------------------------|
| Plausible  | None              | $9/mo      | Privacy-first, simple       |
| Umami      | Self-host free    | $0         | Open source, own data       |
| PostHog    | 1m events/mo      | $0         | Product analytics + feature flags |
| Mixpanel   | 20M events        | $25/mo     | Advanced analytics          |
| Amplitude  | 10M events/mo     | $0         | Product analytics           |
| Google Analytics| Free          | $0         | Free, widely used           |
| Heap       | 5k sessions       | $0         | Auto-capture, no tracking   |
| Fathom     | None              | $14/mo     | Privacy-first, simple       |
| Pirsch     | None              | €9/mo      | Privacy-first, EU-hosted    |
```

### Recommendation: PostHog (product analytics) + Plausible (traffic analytics)

PostHog provides product analytics, session recording, feature flags, and A/B testing in one platform. Plausible is a lightweight, privacy-friendly alternative for basic traffic data.

```typescript
// lib/analytics/posthog.ts
import { PostHog } from 'posthog-node';

export const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST,
});

export function trackEvent(userId: string, event: string, properties?: Record<string, any>) {
  posthog.capture({
    distinctId: userId,
    event,
    properties,
  });
}

export function identifyUser(userId: string, traits: Record<string, any>) {
  posthog.identify({
    distinctId: userId,
    properties: traits,
  });
}
```

## Customer Support

### Comparison

```markdown
| Service     | Free Tier         | Paid Start | Best For                    |
|-------------|-------------------|------------|-----------------------------|
| Intercom    | None             | $39/mo     | Best overall, expensive     |
| Crisp       | Free             | $25/mo     | Chat + email + knowledge base|
| Help Scout  | None             | $25/mo     | Email-only, simple          |
| Freshdesk   | Free             | $15/mo     | Full help desk              |
| Zendesk     | None             | $55/mo     | Enterprise, expensive       |
| Canny       | Free             | $25/mo     | Feature requests + changelog|
| Livestorm   | Free             | $55/mo     | Video support               |
| Stonly      | Free             | $29/mo     | Interactive guides          |
| Tawk.to     | Free             | $0         | Free live chat (branded)    |
```

### Recommendation: Crisp (Free for MVP, $25/mo for growth)

Crisp provides live chat, email ticketing, knowledge base, and chatbot in one platform at a reasonable price.

## Feature Flags

### Comparison

```markdown
| Service     | Free Tier          | Paid Start  | Best For                    |
|-------------|--------------------|-------------|-----------------------------|
| LaunchDarkly| 5 seats            | $80/mo      | Best, expensive             |
| PostHog     | 1m events/mo       | $0          | Built-in with PostHog       |
| Flagsmith   | Free (self-host)   | $0          | Open source                 |
| Unleash     | Free (self-host)   | $0          | Open source, simple         |
| GrowthBook  | Free (self-host)   | $0          | Open source, A/B testing    |
| ConfigCat   | Free (10 flags)    | $0          | Simple, cheap at scale      |
| Split       | Free (3 users)     | $0          | Developer-focused           |
```

### Recommendation: PostHog Feature Flags (if using PostHog) or a simple DB-backed system for MVP

```typescript
// lib/features/index.ts
// Simple feature flag system for MVP
const features = {
  new_dashboard: process.env.ENABLE_NEW_DASHBOARD === 'true',
  ai_autocomplete: process.env.ENABLE_AI_AUTOCOMPLETE === 'true',
  beta_api_v2: process.env.ENABLE_BETA_API_V2 === 'true',
};

export function isEnabled(feature: keyof typeof features): boolean {
  return features[feature];
}

// For more sophisticated flags, use PostHog
export async function isFeatureEnabled(
  userId: string,
  feature: string
): Promise<boolean> {
  const isEnabled = await posthog.isFeatureEnabled(feature, userId);
  return isEnabled ?? false;
}
```

## Background Jobs

### Comparison

```markdown
| Service     | Free Tier          | Paid Start  | Best For                    |
|-------------|--------------------|-------------|-----------------------------|
| Inngest     | Free tier          | $0          | Serverless jobs, great DX   |
| Trigger.dev | Free tier          | $0          | Open source, JS-only        |
| QStash      | 10k req/month      | $0          | HTTP-based queues           |
| Redis Queue | Self-hosted        | $0          | Requires Redis              |
| Sidekiq     | Self-hosted        | $0          | Ruby-only, mature           |
| Celery      | Self-hosted        | $0          | Python-only, mature         |
| AWS SQS     | 1m req/month       | $0.40/m     | Standard queue service      |
| GCP Pub/Sub | 10GB/month         | $0          | Google Cloud                |
```

### Recommendation: Inngest (serverless, great free tier) or database-backed queue (MVP)

```typescript
// lib/jobs/inngest.ts
import { Inngest } from 'inngest';

export const inngest = new Inngest({ id: 'my-saas' });

// Define a job
export const processPayment = inngest.createFunction(
  { id: 'process-payment' },
  { event: 'payment/created' },
  async ({ event, step }) => {
    const { userId, amount, currency } = event.data;

    // Step 1: Charge customer
    const charge = await step.run('charge-customer', async () => {
      return stripe.charges.create({ amount, currency, customer: userId });
    });

    // Step 2: Update database
    await step.run('update-database', async () => {
      await db.query('UPDATE users SET balance = balance - $1 WHERE id = $2', [amount, userId]);
    });

    // Step 3: Send receipt
    await step.run('send-receipt', async () => {
      await sendEmail({ to: event.data.email, template: 'receipt', variables: { amount } });
    });

    return { success: true, chargeId: charge.id };
  }
);
```

## Form/Data Collection

### Comparison

```markdown
| Service     | Free Tier          | Paid Start | Best For                    |
|-------------|--------------------|------------|-----------------------------|
| Typeform    | 10 responses/mo    | $25/mo     | Beautiful forms             |
| Tally       | Free              | $29/mo     | No-code forms, unlimited    |
| Fillout     | 1k responses/mo   | $20/mo     | Powerful, embeddable        |
| Jotform     | 100 submissions/mo| $34/mo     | Complex forms               |
| Formbricks  | Self-host free    | $0         | Open source, surveys        |
| Paperform   | 3 forms           | $22/mo     | Beautiful, payment forms    |
```

### Recommendation: Tally (free, beautiful, unlimited forms for MVP)

## Logging

### Comparison

```markdown
| Service    | Free Tier          | Paid Start  | Best For                    |
|------------|--------------------|-------------|-----------------------------|
| Logtail    | 1GB/mo             | $17/mo      | Modern, fast                |
| Better Stack| 1GB/mo            | $20/mo      | Logs + status pages         |
| Logz.io    | 1GB/day            | $0          | ELK stack as a service      |
| Axiom      | 5TB/mo             | $0          | Unlimited retention, cheap  |
| Datadog    | 1GB/day            | $15/mo      | Full observability          |
| Grafana    | Self-host free     | $0          | Self-hosted, powerful       |
| Seq        | Free (4GB/day)     | $0          | .NET-focused                |
```

### Recommendation: Axiom (insanely cheap, unlimited retention on free tier)

```typescript
// lib/logging/axiom.ts
import { createLogger } from '@axiomhq/axiom';

const logger = createLogger({
  token: process.env.AXIOM_TOKEN!,
  dataset: process.env.AXIOM_DATASET!,
});

// Structured logging
export function log(level: string, message: string, meta?: Record<string, any>) {
  logger.log({
    level,
    message,
    service: 'my-saas',
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString(),
    ...meta,
  });
}
```

## SEO and Marketing

### Comparison

```markdown
| Service     | Free Tier          | Paid Start | Best For                    |
|-------------|--------------------|------------|-----------------------------|
| Ahrefs      | None              | $29/mo     | Best SEO toolset            |
| Semrush     | Free (limited)    | $35/mo     | SEO + content marketing     |
| Google Search Console| Free   | $0         | Essential, free             |
| Ubersuggest | Free (limited)    | $12/mo     | Keyword research            |
| Screaming Frog| Free (500 URLs) | $0         | Technical SEO               |
| Plausible   | None              | $9/mo      | Privacy-first analytics     |
| Hotjar      | 35 sessions/day   | $0         | Session recording, heatmaps |
| Microsoft Clarity| Free        | $0         | Free session recordings     |
```

### Recommendation: Google Search Console (free) + Plausible ($9/mo) + Microsoft Clarity (free)

## CI/CD

### Comparison

```markdown
| Service         | Free Tier          | Paid Start  | Best For                    |
|-----------------|--------------------|-------------|-----------------------------|
| GitHub Actions  | 2k min/mo          | $0          | Best for GitHub repos       |
| GitLab CI/CD    | 400 min/mo         | $0          | Best for GitLab repos       |
| CircleCI        | 6k min/mo          | $0          | Fast, Docker-native         |
| Railway         | $5 credit          | $0          | Deploy from GitHub          |
| Vercel          | Unlimited          | $0          | Automatic deploys for Next.js|
| Netlify         | 300 min/mo         | $0          | Automatic deploys           |
| Render          | Free               | $0          | Automatic deploys           |
| Cloudflare Pages| Unlimited          | $0          | Fast, global                |
```

### Recommendation: GitHub Actions + Vercel/Railway for deploys

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
```

## Monitoring Stack Summary

### MVP Phase Stack (Total: $0/mo)

```markdown
Errors:          Sentry (free tier)
Uptime:          Better Uptime (1 monitor free)
Logs:            Axiom (free tier, generous)
Analytics:       PostHog (free tier or self-host)
Performance:     Vercel Analytics (free with Vercel)
```

### Growth Phase Stack (Total: ~$60/mo)

```markdown
Errors:          Sentry ($26/mo)
Uptime:          Better Uptime ($20/mo)
Logs:            Axiom ($17/mo)
Analytics:       PostHog (paid tier, ~$30/mo)
Performance:     Grafana or Datadog ($15/mo)
```

## Service Selection Decision Framework

For each service category, use this framework:

```
1. Can I build this myself in < 1 day?
   YES → Consider building (simple feature flag, basic logging)
   NO → Buy a service

2. Is this a core differentiator for my product?
   YES → Build it yourself (unique value)
   NO → Buy a service

3. Is there a free tier that meets my needs?
   YES → Use it. Upgrade when forced to.
   NO → Is the paid price < $50/mo?
       YES → Buy it
       NO → Can I survive without it?
           YES → Skip for now
           NO → Find a cheaper alternative

4. How hard is it to switch later?
   Easy → Use the best tool regardless of lock-in
   Hard → Choose carefully, prefer standards-based solutions
```

## Avoiding Service Sprawl

Too many services create management overhead. For MVP, aim for:

```
Maximum 5-7 external services:
1. Auth (Clerk or Supabase)
2. Database (Supabase or Neon)
3. Payments (Stripe)
4. Email (Resend)
5. Hosting (Vercel)
6. Monitoring (Sentry)
7. DNS (Cloudflare)

Every additional service should require strong justification.
```

## Summary

As a solo founder, every service you use should save you more time than it costs to manage. The key is to buy commodity functionality and build only your core differentiator.

**MVP Service Stack (Total: $0/mo):**
- Auth: Clerk (free up to 10k users)
- Database: Supabase (free 500MB)
- Payments: Stripe (pay as you go)
- Email: Resend (100 free/day)
- Hosting: Vercel + Supabase (both free)
- Monitoring: Sentry + Better Uptime (both free)
- DNS: Cloudflare (free)
- Analytics: PostHog (free tier)

**Key principle:** Start with the cheapest/free options that work. Upgrade only when the free tier becomes a bottleneck. Most free tiers support 1k-10k users, which is well beyond the point where you should have revenue to pay for services.
