# Building API-First SaaS: Developer Experience, Documentation, SDK, Pricing, Rate Limiting

## Why API-First as a Solo Founder

Building an API-first SaaS means your primary product is an API. Developers integrate your API into their own applications. This model offers unique advantages for solo founders:

- **No user interface to build** — Focus on the API, not pixel-perfect UIs
- **Developer distribution** — Developers find you through API docs, not ads
- **Usage-based revenue** — Revenue scales with API usage, not seats
- **Sticky integrations** — Once developers integrate your API, switching costs are high
- **Global reach** — APIs serve customers worldwide without localization complexity

Successful API-first companies include Stripe, Twilio, Algolia, Plaid, and SendGrid — many started with small teams.

## Phase 1: API Design Principles

### Developer Experience (DX) is Your Product

For API-first SaaS, developer experience IS your product. A bad API with great marketing fails. A great API with no marketing succeeds.

```
API Design Principles:

1. Consistency
   - Same patterns across all endpoints
   - Predictable error formats
   - Consistent naming conventions

2. Simplicity
   - Minimal endpoints that do one thing well
   - Sensible defaults (over 80% of users don't override)
   - Clear, readable request/response formats

3. Predictability
   - RESTful or clearly documented conventions
   - Idempotent mutations (same request = same result)
   - No surprises in behavior

4. Discoverability
   - Endpoints follow logical hierarchy
   - Responses include links to related resources
   - Error messages point to documentation

5. Forgiveness
   - Accept flexible input formats
   - Ignore unknown fields (don't error)
   - Smart type coercion
```

### REST API Design Template

```typescript
// Consistent REST API patterns

// List resources
GET /api/v1/resources?page=1&per_page=20&sort=created_at:desc
// Response: { data: [...], meta: { page, per_page, total, total_pages } }

// Get single resource
GET /api/v1/resources/:id
// Response: { data: { id, attributes, relationships } }

// Create resource
POST /api/v1/resources
Body: { type: "resource", attributes: { ... } }
// Response: 201 { data: { id, attributes, ... } }

// Update resource
PATCH /api/v1/resources/:id
Body: { attributes: { ... } }
// Response: 200 { data: { id, attributes, ... } }

// Delete resource
DELETE /api/v1/resources/:id
// Response: 204 (no content)

// Nested resources
GET /api/v1/resources/:id/children
POST /api/v1/resources/:id/children

// Actions (non-CRUD operations)
POST /api/v1/resources/:id/action-name
Body: { ... parameters ... }
```

### Error Response Format

```typescript
// Consistent error responses for every API

interface ApiError {
  error: {
    type: string           // Machine-readable error code
    message: string        // Human-readable description
    code: string           // Specific error code
    detail?: string        // Additional context
    docs?: string          // Link to documentation
    request_id?: string    // For debugging
  }
}

// Examples:

// 400 - Bad Request
{ "error": { 
    "type": "validation_error",
    "message": "Email is required",
    "code": "missing_field",
    "detail": "The 'email' field must be provided",
    "docs": "https://docs.api.com/errors#missing_field"
}}

// 401 - Unauthorized
{ "error": {
    "type": "authentication_error",
    "message": "Invalid API key",
    "code": "invalid_api_key",
    "docs": "https://docs.api.com/errors#authentication"
}}

// 404 - Not Found
{ "error": {
    "type": "not_found",
    "message": "Resource not found",
    "code": "resource_not_found",
    "request_id": "req_abc123"
}}

// 429 - Rate Limited
{ "error": {
    "type": "rate_limit_error",
    "message": "Rate limit exceeded. Try again in 30 seconds.",
    "code": "rate_limited",
    "retry_after": 30
}}

// 500 - Server Error
{ "error": {
    "type": "server_error",
    "message": "An unexpected error occurred",
    "code": "internal_error",
    "request_id": "req_def456",
    "docs": "https://status.api.com"
}}
```

## Phase 2: Authentication and Security

### API Key Authentication (Minimum Viable)

```typescript
// Simple API key authentication for solo founder API

import { createHash, randomBytes } from 'crypto'

class APIKeyAuth {
  generateAPIKey(userId: string): { key: string; prefix: string } {
    const raw = `api_${randomBytes(32).toString('hex')}`
    const prefix = raw.substring(0, 8) // "api_abc1"
    const hash = createHash('sha256').update(raw).digest('hex')
    
    // Store hash, never store raw key
    await db.apiKeys.create({
      userId,
      keyPrefix: prefix,
      keyHash: hash,
      createdAt: new Date()
    })
    
    // Return raw key ONCE to the user
    return { key: raw, prefix }
  }

  async authenticate(request: Request): Promise<User | null> {
    const authHeader = request.headers.get('authorization')
    if (!authHeader) return null
    
    // Support both "Bearer sk_..." and "sk_..." directly
    const key = authHeader.replace('Bearer ', '')
    const hash = createHash('sha256').update(key).digest('hex')
    
    const apiKey = await db.apiKeys.findUnique({
      where: { keyHash: hash },
      include: { user: true }
    })
    
    if (!apiKey || apiKey.revokedAt) return null
    
    // Update last used
    await db.apiKeys.update({
      where: { id: apiKey.id },
      data: { lastUsedAt: new Date() }
    })
    
    return apiKey.user
  }
}
```

### Rate Limiting

```typescript
// Sliding window rate limiter

class RateLimiter {
  constructor(private redis: Redis) {}

  async checkRateLimit(apiKey: string, endpoint: string): Promise<{
    allowed: boolean;
    remaining: number;
    resetAt: number;
  }> {
    const limits = await this.getLimitsForKey(apiKey)
    
    // Check each limit tier
    for (const limit of limits) {
      const key = `ratelimit:${apiKey}:${limit.window}`
      
      const current = await this.redis.incr(key)
      
      if (current === 1) {
        // First request in this window — set expiry
        await this.redis.expire(key, limit.windowSeconds)
      }
      
      const ttl = await this.redis.ttl(key)
      
      if (current > limit.maxRequests) {
        return {
          allowed: false,
          remaining: 0,
          resetAt: Date.now() + (ttl * 1000)
        }
      }
    }
    
    // Calculate remaining from the most restrictive limit
    const remaining = await this.calculateRemaining(apiKey, limits)
    const maxTtl = await this.getMaxTtl(apiKey, limits)
    
    return {
      allowed: true,
      remaining,
      resetAt: Date.now() + (maxTtl * 1000)
    }
  }

  async getLimitsForKey(apiKey: string) {
    const key = await db.apiKeys.findUnique({
      where: { keyHash: apiKey },
      include: { plan: true }
    })
    
    return key.plan.rateLimits || [
      { window: 'second', windowSeconds: 1, maxRequests: 10 },
      { window: 'minute', windowSeconds: 60, maxRequests: 100 },
      { window: 'hour', windowSeconds: 3600, maxRequests: 1000 },
      { window: 'day', windowSeconds: 86400, maxRequests: 10000 },
    ]
  }

  async calculateRemaining(apiKey: string, limits: any[]) {
    const remaining = await Promise.all(
      limits.map(async (limit) => {
        const key = `ratelimit:${apiKey}:${limit.window}`
        const current = await this.redis.get(key)
        return limit.maxRequests - (parseInt(current || '0'))
      })
    )
    return Math.min(...remaining)
  }
}
```

## Phase 3: Documentation and Developer Experience

### Documentation is Your Marketing

For API-first products, documentation is the #1 marketing channel. Developers find you through search, read your docs, and decide whether to integrate.

```
Documentation that converts:

1. Quickstart
   - "Get started in 5 minutes"
   - Copy-paste code that works
   - Clear expectations: what will happen

2. Core concepts
   - Explain your data model
   - Diagrams > text
   - Examples for every concept

3. API Reference
   - Every endpoint documented
   - Request/response examples
   - Error codes and what they mean
   - Code samples in multiple languages

4. Guides
   - Common integration patterns
   - Best practices
   - Migration guides

5. SDK documentation
   - Installation
   - Basic usage
   - Advanced usage

6. Changelog
   - What's new
   - Breaking changes
   - Deprecation timeline

7. Status page
   - Current status
   - Incident history
   - Maintenance calendar
```

### The Solo Founder's Documentation Stack

```
Documentation Tools:

Primary: Next.js + MDX (custom docs site)
  - Full control, SEO-friendly
  - Time to build: 1-2 weeks

Alternative: GitBook (hosted, fast to launch)
  - Free tier available
  - Time to set up: 1 day

Code Examples: 
  - Runable snippets (CodeSandbox, Replit)
  - Copy-paste examples for curl, Node.js, Python, Ruby, PHP

API Testing:
  - Rapidoc or Swagger UI for interactive API docs
  - "Try it" button on every endpoint

Analytics:
  - Track doc page views, search queries
  - Identify which pages cause the most support tickets
```

### The Developer Onboarding Flow

```typescript
// Track developer onboarding progress

class DeveloperOnboarding {
  async trackOnboarding(developerId: string) {
    const steps = [
      { name: 'viewed_docs', weight: 10 },
      { name: 'generated_api_key', weight: 20 },
      { name: 'made_first_request', weight: 30 },
      { name: 'completed_quickstart', weight: 20 },
      { name: 'built_integration', weight: 20 }
    ]
    
    const completed = await db.developerProgress.findMany({
      where: { developerId, completed: true }
    })
    
    const totalScore = completed.reduce(
      (sum, step) => sum + steps.find(s => s.name === step.stepName)?.weight || 0,
      0
    )
    
    return {
      score: totalScore,
      maxScore: steps.reduce((sum, s) => sum + s.weight, 0),
      percentage: Math.round((totalScore / 100) * 100),
      nextStep: steps.find(
        s => !completed.find(c => c.stepName === s.name)
      )
    }
  }
}
```

## Phase 4: SDK Development

### Why SDKs Matter

SDKs are your distribution. Developers choose APIs with good SDKs over APIs with better functionality but no SDK.

```
SDK Priority Order:

1. Node.js/TypeScript (if you're a JS developer)
   - Your first SDK. Eat your own dog food.
   
2. Python
   - Largest developer community for data/ML/AI
   - Second most common for API integrations

3. Curl examples (always include)
   - Every developer can read curl
   - Useful for debugging and testing

4. Additional languages (when demand justifies)
   - Go (infrastructure developers)
   - Ruby (Rails developers)
   - PHP (WordPress/web developers)
   - Java/.NET (enterprise developers)
```

### SDK Template (TypeScript/Node.js)

```typescript
// Consistent SDK pattern for all languages

class ApiClient {
  private baseUrl: string
  private apiKey: string
  private maxRetries: number

  constructor(config: {
    apiKey: string
    baseUrl?: string
    maxRetries?: number
  }) {
    this.apiKey = config.apiKey
    this.baseUrl = config.baseUrl || 'https://api.example.com/v1'
    this.maxRetries = config.maxRetries || 3
  }

  // Resources
  async get<T>(path: string, params?: Record<string, any>): Promise<T> {
    return this.request('GET', path, { params })
  }

  async post<T>(path: string, body?: any): Promise<T> {
    return this.request('POST', path, { body })
  }

  async patch<T>(path: string, body?: any): Promise<T> {
    return this.request('PATCH', path, { body })
  }

  async delete<T>(path: string): Promise<T> {
    return this.request('DELETE', path)
  }

  // Core request handler with retries
  private async request<T>(
    method: string,
    path: string,
    options?: { params?: any; body?: any }
  ): Promise<T> {
    let lastError: Error | null = null
    
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const url = new URL(`${this.baseUrl}${path}`)
        if (options?.params) {
          Object.entries(options.params).forEach(([k, v]) => {
            url.searchParams.set(k, String(v))
          })
        }

        const response = await fetch(url.toString(), {
          method,
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
            'User-Agent': 'api-client/1.0'
          },
          body: options?.body ? JSON.stringify(options.body) : undefined
        })

        // Handle rate limiting
        if (response.status === 429) {
          const retryAfter = parseInt(
            response.headers.get('Retry-After') || '1'
          )
          await this.sleep(retryAfter * 1000)
          continue
        }

        if (!response.ok) {
          throw new ApiError(
            response.status,
            await response.json()
          )
        }

        return response.json()
      } catch (error) {
        lastError = error as Error
        if (attempt < this.maxRetries) {
          await this.sleep(Math.pow(2, attempt) * 1000) // Exponential backoff
        }
      }
    }

    throw lastError || new Error('Request failed')
  }

  private sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// Usage
const client = new ApiClient({ apiKey: 'sk_...' })

const users = await client.get('/users', { page: 1, limit: 20 })
const user = await client.post('/users', { name: 'Alice', email: 'alice@example.com' })
```

## Phase 5: API Pricing Models

### Common API Pricing Models

```
1. Usage-Based Pricing
   Pay per API call or per unit consumed
   Example: Twilio ($0.0079/SMS), Stripe (2.9% + $0.30)
   Pros: Scales with customer success
   Cons: Revenue is unpredictable

2. Tiered Pricing
   Fixed price for X API calls/month
   Example: $20/month for 10K calls, $100/month for 100K calls
   Pros: Predictable revenue
   Cons: Undercharged power users, overcharged small users

3. Freemium + Usage
   Free tier with limits, paid for more
   Example: 1K free calls/month, then $0.001/call
   Pros: Low barrier to try, converts naturally
   Cons: Free tier costs you money

4. Enterprise Licensing
   Custom pricing for large customers
   Example: $10K+/month with dedicated support
   Pros: High revenue per customer
   Cons: Requires sales process

5. Feature-Based
   Pay for specific features/capabilities
   Example: Basic (REST API), Premium (Webhooks + Real-time)
   Pros: Clear upgrade path
   Cons: More complex pricing page
```

### Recommended Pricing for Solo Founder API

```
Phase 1: Simple usage-based pricing
  - Free tier: 1,000 calls/month (no credit card)
  - Pay-as-you-go: $0.01/call after free tier
  - No tiers, no complexity

Phase 2: Tiered pricing (after 100+ paying customers)
  - Free: 1K calls/month
  - Starter: $20/month for 10K calls
  - Pro: $100/month for 100K calls
  - Enterprise: Custom (contact us)
  - Overage: $0.01/call above tier

Phase 3: Optimize based on data
  - What's the average usage per customer?
  - What usage level triggers upgrades?
  - What price maximizes LTV?
  - A/B test pricing pages
```

### API Pricing Implementation

```typescript
class APIBilling {
  async getPricingPlan(usageCalls: number) {
    const plans = [
      {
        name: 'Free',
        price: 0,
        includedCalls: 1000,
        overageRate: null, // Block instead of overage
        features: ['REST API', 'Basic docs']
      },
      {
        name: 'Starter',
        price: 20,
        includedCalls: 10000,
        overageRate: 0.002, // $0.002 per call
        features: ['REST API', 'SDKs', 'Email support']
      },
      {
        name: 'Pro',
        price: 100,
        includedCalls: 100000,
        overageRate: 0.001, // $0.001 per call
        features: ['REST API', 'SDKs', 'Webhooks', 'Priority support']
      },
      {
        name: 'Enterprise',
        price: 'Custom',
        includedCalls: 'Custom',
        overageRate: 'Custom',
        features: ['All features', 'SLA', 'Dedicated support', 'Custom integrations']
      }
    ]
    
    // Find the best plan for this usage
    const plan = plans.find(p => p.includedCalls >= usageCalls)
      || plans[plans.length - 1]
    
    return plan
  }

  async calculateMonthlyBill(apiKey: string) {
    const usage = await db.apiUsage.aggregate({
      where: {
        apiKey,
        month: new Date().getMonth()
      },
      _sum: { calls: true }
    })

    const totalCalls = usage._sum.calls || 0
    const plan = await this.getActivePlan(apiKey)
    
    if (totalCalls <= plan.includedCalls) {
      return { amount: plan.price, calls: totalCalls, included: plan.includedCalls }
    }

    const overage = totalCalls - plan.includedCalls
    const overageCost = overage * plan.overageRate

    return {
      amount: plan.price + overageCost,
      calls: totalCalls,
      included: plan.includedCalls,
      overage,
      overageCost
    }
  }
}
```

## Phase 6: API Monitoring and Observability

### What to Monitor

```typescript
class APIMonitoring {
  trackRequest(request: {
    method: string
    path: string
    statusCode: number
    latency: number
    apiKey: string
    error?: string
  }) {
    // Log to analytics
    this.logToAnalytics(request)
    
    // Track latency percentiles
    this.trackLatency(request.latency)
    
    // Track error rate
    if (request.statusCode >= 500) {
      this.incrementErrorCount()
      this.alertIfHighErrorRate()
    }
    
    // Track usage for billing
    this.incrementUsage(request.apiKey)
    
    // Track endpoint popularity
    this.trackEndpointUsage(request.path, request.method)
  }

  async getAPIDashboard() {
    const now = Date.now()
    const lastHour = now - 3600000
    
    return {
      requests: {
        total: await this.countRequests(lastHour),
        byEndpoint: await this.getRequestsByEndpoint(lastHour),
        byStatusCode: await this.getRequestsByStatus(lastHour)
      },
      performance: {
        p50Latency: await this.getLatencyPercentile(50, lastHour),
        p95Latency: await this.getLatencyPercentile(95, lastHour),
        p99Latency: await this.getLatencyPercentile(99, lastHour)
      },
      errors: {
        rate: await this.getErrorRate(lastHour),
        byEndpoint: await this.getErrorsByEndpoint(lastHour)
      },
      usage: {
        byCustomer: await this.getUsageByCustomer(lastHour),
        rateLimited: await this.getRateLimitedCount(lastHour)
      }
    }
  }
}
```

## Phase 7: Developer Marketing for APIs

### How Developers Find APIs

| Source | Priority | Strategy |
|--------|----------|----------|
| Google Search | #1 | SEO for "how to [solve problem]" + your product |
| GitHub | #2 | Open source SDKs, examples, community |
| Documentation | #3 | API docs that rank for technical queries |
| Word of mouth | #4 | Happy developers tell other developers |
| API directories | #5 | RapidAPI, ProgrammableWeb, GitHub topics |
| Content marketing | #6 | Technical blog posts, tutorials, videos |

### Developer Marketing Content

```
Content Types That Work:

1. Tutorials
   "How to build [useful thing] with [Your API]"
   Step-by-step, copy-paste code
   Published on your blog + dev.to + Medium

2. Comparison posts
   "Your API vs. Competitor: Which should you use?"
   Honest, balanced comparison
   Highlights your strengths without trashing competitors

3. Built-with case studies
   "[Company] built [product] using [Your API]"
   "How we [achieved result] with [Your API]"
   Technical deep-dive with code

4. Open source examples
   GitHub repos with real integration examples
   Starter templates for popular frameworks
   Sample apps that showcase your API

5. Technical talks
   Conference talks and meetup presentations
   "How we scaled [Your API] to handle [scale]"
   Share technical learnings (builds developer trust)
```

### The Developer Onboarding Funnel

```
API Developer Funnel:

Awareness:
  Google search → Docs site
  GitHub → SDK repo
  Twitter → Blog post
  Friend → Word of mouth

Evaluation:
  → Reads quickstart (5 min)
  → Generates API key (1 min)
  → Makes first API request (2 min)
  → "This works as advertised"

Integration:
  → Reads integration guide
  → Implements in their app
  → Tests with their data
  → Deploys to production

Advocacy:
  → Success with your API
  → Tells other developers
  → Contributes to community
  → Writes about their experience
```

## The Solo Founder's API Launch Timeline

### Month 1: Foundation
- [ ] Design API (endpoints, authentication, error formats)
- [ ] Build core API functionality
- [ ] Write quickstart guide
- [ ] Generate first API key

### Month 2: Developer Experience
- [ ] Build API reference docs
- [ ] Create Node.js SDK
- [ ] Add curl examples everywhere
- [ ] Set up Stripe billing integration
- [ ] Implement rate limiting

### Month 3: Polish
- [ ] Write 3-5 integration guides
- [ ] Build status page
- [ ] Set up monitoring and alerts
- [ ] Write changelog
- [ ] Create API testing dashboard

### Month 4: Launch
- [ ] Publish documentation site
- [ ] Launch on Product Hunt (API tools category)
- [ ] Post on Hacker News (Show HN)
- [ ] Write launch blog post
- [ ] Submit to API directories

### Month 5-6: Growth
- [ ] Publish 2-3 technical tutorials
- [ ] Create open source example apps
- [ ] Build Python SDK
- [ ] Start developer newsletter
- [ ] Respond to every developer inquiry personally

## Final Thoughts

- **Your API is your product.** Every design decision, every error message, every latency millisecond matters.

- **Documentation is your marketing.** A great API with bad docs fails. A decent API with great docs succeeds.

- **Developer experience is your moat.** Developers who love your API will build with it, advocate for it, and stay with it through competitors.

- **SDKs are your distribution.** The easier you make it to integrate, the more integrations you'll get. Start with the languages your target developers use.

- **Pricing should be simple.** Developers hate complex pricing. Usage-based pricing with a free tier is the standard for API-first products.

- **Monitor everything.** Every API call is data about your product's health, your customers' usage, and your business's performance.

- **Be the developer you're serving.** Use your own API. Feel your own pain. Fix it. Your developers will thank you.

Building an API-first SaaS as a solo founder means competing with companies 10x your size on quality alone. That's an advantage — when you have fewer constraints, you can obsess over developer experience in ways larger companies can't.
