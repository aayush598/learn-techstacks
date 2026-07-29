# Managing LLM API Costs: Caching Strategies, Prompt Optimization, Model Selection, Batching

## Why LLM Cost Management Matters for Solo Founders

LLM API costs are the single biggest operational risk for AI-powered SaaS. Unlike traditional cloud costs (compute, storage, bandwidth), LLM costs:

- Scale with user engagement (more success = higher costs)
- Have unpredictable variance (different queries use different tokens)
- Are growing rapidly (AI usage increases as models improve)
- Can outpace revenue if not managed (especially during free trials)

A solo founder cannot absorb runaway costs. You need systems to keep AI costs under control from day one.

## The Solo Founder's AI Cost Framework

```
Total AI Cost = (Number of Queries) × (Tokens per Query) × (Cost per Token)

You need to control ALL THREE variables:

1. Number of queries → Caching, rate limits, user behavior
2. Tokens per query → Prompt optimization, model selection
3. Cost per token → Model tier, provider, batch processing
```

## Phase 1: Measuring Your Current AI Costs

### Cost Tracking Infrastructure

Before you can optimize costs, you need to measure them.

```javascript
// AI Cost Tracking Service
class AICostTracker {
  constructor() {
    this.dailyLogs = []
  }

  logQuery({ userId, feature, model, promptTokens, completionTokens, latency }) {
    const query = {
      userId,
      feature,
      model,
      inputTokens: promptTokens,
      outputTokens: completionTokens,
      totalTokens: promptTokens + completionTokens,
      cost: this.calculateCost(promptTokens, completionTokens, model),
      latency,
      timestamp: new Date()
    }
    
    this.dailyLogs.push(query)
    
    // Store for analysis
    this.persist(query)
  }

  calculateCost(promptTokens, completionTokens, model) {
    const pricing = {
      'gpt-4o': { input: 0.0000025, output: 0.00001 },
      'gpt-4o-mini': { input: 0.00000015, output: 0.0000006 },
      'claude-3-haiku': { input: 0.00000025, output: 0.00000125 },
      'claude-3-sonnet': { input: 0.000003, output: 0.000015 }
    }
    
    const modelPricing = pricing[model] || pricing['gpt-4o-mini']
    
    const inputCost = promptTokens * modelPricing.input
    const outputCost = completionTokens * modelPricing.output
    
    return inputCost + outputCost
  }

  async getDailyCost() {
    const today = this.dailyLogs.filter(log => {
      return log.timestamp.toDateString() === new Date().toDateString()
    })
    return {
      totalCost: today.reduce((sum, log) => sum + log.cost, 0),
      totalQueries: today.length,
      byFeature: this.groupByFeature(today),
      byUser: this.groupByUser(today)
    }
  }

  groupByFeature(logs) {
    const groups = {}
    logs.forEach(log => {
      groups[log.feature] = groups[log.feature] || { queries: 0, cost: 0, tokens: 0 }
      groups[log.feature].queries++
      groups[log.feature].cost += log.cost
      groups[log.feature].tokens += log.totalTokens
    })
    return groups
  }

  groupByUser(logs) {
    const groups = {}
    logs.forEach(log => {
      groups[log.userId] = groups[log.userId] || { queries: 0, cost: 0 }
      groups[log.userId].queries++
      groups[log.userId].cost += log.cost
    })
    return groups
  }
}
```

### Cost Dashboard

Monitor these metrics daily:

```
AI Cost Dashboard:

Daily AI Cost: $___
MTD AI Cost: $___
Avg Cost Per Query: $___
Cost Per User (active): $___
Cost Per User (all users): $___
Cost Per Feature:
  - Feature A: $___ (___ queries)
  - Feature B: $___ (___ queries)
  - Feature C: $___ (___ queries)

AI Cost as % of Revenue: __%

Top 5 Costliest Users:
  1. User X: $___
  2. User Y: $___
  3. User Z: $___

Alert: Single user cost > $10/day? ___ (Yes/No)
```

### Setting Cost Alerts

```javascript
// Cost alert thresholds for solo founders

async function checkCostAlerts() {
  const today = await costTracker.getDailyCost()
  const alerts = []

  // Daily budget check
  if (today.totalCost > DAILY_BUDGET) {
    alerts.push(`Daily cost $${today.totalCost} exceeds budget of $${DAILY_BUDGET}`)
  }

  // Per-user check (prevent abuse)
  Object.entries(today.byUser).forEach(([userId, { cost, queries }]) => {
    if (cost > 10) {
      alerts.push(`User ${userId} spent $${cost} today (${queries} queries)`)
    }
    if (queries > 1000) {
      alerts.push(`User ${userId} made ${queries} queries today — possible abuse`)
    }
  })

  // Cost growth check
  const yesterdayCost = await getYesterdayCost()
  const growth = (today.totalCost - yesterdayCost) / yesterdayCost * 100
  if (growth > 50) {
    alerts.push(`Daily cost grew ${growth.toFixed(0)}% vs yesterday`)
  }

  // Feature-level anomaly
  Object.entries(today.byFeature).forEach(([feature, { cost }]) => {
    const featureAverage = featureAverages[feature] || cost
    if (cost > featureAverage * 3) {
      alerts.push(`Feature "${feature}" cost ($ ${cost}) is 3x above average`)
    }
  })

  return alerts
}
```

## Phase 2: Caching Strategies (Highest ROI)

Caching is the single most effective cost reduction strategy. A well-designed cache reduces LLM costs by 30-60%.

### Cache Level 1: Exact Query Cache

```javascript
// Cache identical queries
class ExactQueryCache {
  constructor(redis) {
    this.redis = redis
    this.ttl = 60 * 60 * 24 // 24 hours
  }

  generateCacheKey(user, query, context) {
    // Hash the exact query + relevant context
    const data = JSON.stringify({
      model: query.model,
      messages: query.messages,
      temperature: query.temperature,
      contextHash: this.hashContext(context)
    })
    return `ai:exact:${this.hash(data)}`
  }

  hashContext(context) {
    // Hash only the relevant context keys
    const relevantKeys = ['userId', 'feature', 'productType']
    const filtered = {}
    relevantKeys.forEach(key => {
      if (context[key]) filtered[key] = context[key]
    })
    return this.hash(JSON.stringify(filtered))
  }

  hash(str) {
    // Simple hash function
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash
    }
    return `cache_${Math.abs(hash).toString(36)}`
  }

  async getOrCompute(key, computeFn) {
    // Try cache first
    const cached = await this.redis.get(key)
    if (cached) {
      return { data: JSON.parse(cached), fromCache: true }
    }

    // Compute if not cached
    const result = await computeFn()
    
    // Cache the result
    await this.redis.setex(key, this.ttl, JSON.stringify(result))
    
    return { data: result, fromCache: false }
  }
}
```

### Cache Level 2: Semantic Cache (Advanced)

For queries that are semantically similar but not identical:

```javascript
// Semantic cache using embeddings
class SemanticCache {
  constructor(redis, embedder) {
    this.redis = redis
    this.embedder = embedder  // OpenAI embedding API
    this.similarityThreshold = 0.95
  }

  async findSimilar(query) {
    // Get query embedding
    const queryEmbedding = await this.embedder.embed(query)
    
    // Search cache by embedding similarity
    const cachedQueries = await this.redis.smembers('ai:semantic:keys')
    
    let bestMatch = null
    let bestSimilarity = 0
    
    for (const cachedKey of cachedQueries) {
      const cachedEmbedding = await this.redis.get(`ai:semantic:emb:${cachedKey}`)
      if (!cachedEmbedding) continue
      
      const similarity = this.cosineSimilarity(queryEmbedding, JSON.parse(cachedEmbedding))
      
      if (similarity > bestSimilarity) {
        bestSimilarity = similarity
        bestMatch = cachedKey
      }
    }

    if (bestSimilarity >= this.similarityThreshold) {
      const result = await this.redis.get(`ai:semantic:result:${bestMatch}`)
      if (result) {
        return { data: JSON.parse(result), fromCache: true }
      }
    }
    
    return null
  }

  cosineSimilarity(a, b) {
    let dotProduct = 0
    let normA = 0
    let normB = 0
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i]
      normA += a[i] * a[i]
      normB += b[i] * b[i]
    }
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB))
  }
}
```

### Cache Level 3: User-Specific Cache

Many users ask similar questions:

```javascript
// Per-user cache for repetitive queries
class UserQueryCache {
  constructor(redis) {
    this.redis = redis
    this.maxEntriesPerUser = 50
  }

  async getOrCompute(userId, queryKey, computeFn, ttl = 3600) {
    const key = `ai:user:${userId}:${this.hash(queryKey)}`
    
    const cached = await this.redis.get(key)
    if (cached) {
      // Extend TTL on access
      await this.redis.expire(key, ttl)
      return JSON.parse(cached)
    }

    const result = await computeFn()
    await this.redis.setex(key, ttl, JSON.stringify(result))
    
    // Maintain LRU-like limit
    await this.pruneUserCache(userId)
    
    return result
  }

  async pruneUserCache(userId) {
    const pattern = `ai:user:${userId}:*`
    const keys = await this.redis.keys(pattern)
    
    if (keys.length > this.maxEntriesPerUser) {
      // Sort by TTL (remaining time) and remove oldest
      const keysWithTtl = await Promise.all(
        keys.map(async key => ({
          key,
          ttl: await this.redis.ttl(key)
        }))
      )
      
      keysWithTtl
        .sort((a, b) => a.ttl - b.ttl)
        .slice(0, keys.length - this.maxEntriesPerUser)
        .forEach(({ key }) => this.redis.del(key))
    }
  }
}
```

## Phase 3: Prompt Optimization (Moderate ROI)

Reducing prompt token usage by 20-50% is achievable without quality loss.

### Prompt Compression Techniques

```javascript
// 1. Remove unnecessary context
// BAD: Provide everything
const badPrompt = `
You are a helpful assistant for our SaaS product [Product Name].
We help teams manage projects, tasks, and deadlines.
Our features include: Gantt charts, Kanban boards, time tracking,
resource management, budget tracking, reporting, integrations
with Slack, Jira, GitHub, and 50+ other tools.
We have pricing tiers: Free ($0), Pro ($12/user/month), and
Enterprise (custom).
Our users include marketing agencies, software teams, and
consulting firms.
[Plus 500 more words of background context]

User question: How do I create a task?
`

// GOOD: Only provide relevant context
const goodPrompt = `
[Product Name] is a project management tool.
The user is asking about task creation.

User question: How do I create a task?

Context: Users can create tasks from the project view,
dashboard, or via email. Tasks support:
- Title, description, assignee, due date
- Labels, priority, status
- Subtasks and dependencies

Keep your answer concise (under 100 words).
`
```

### System Prompt Optimization

```
Optimization Checklist:

1. Remove boilerplate
   "You are a helpful AI assistant" → "You help users analyze data"
   Every word should serve a purpose

2. Use shorthand for common patterns
   Instead of: "Provide a response that is concise, direct, 
   and actionable, with no more than 3 sentences"
   Write: "Respond in ≤3 sentences. Be direct. Be actionable."

3. Combine system and user messages
   System messages are processed as tokens too
   Move non-sensitive system context to user messages if it helps

4. Remove redundant instructions
   If a rule is never violated, remove it
   If a behavior is already in the model, don't restate it

5. Use format constraints
   "Respond as: { summary: string, action_items: string[] }"
   Structured outputs reduce verbose output
```

### Prompt Template Management

```javascript
// Systematic prompt template system
const PROMPT_TEMPLATES = {
  // Version your prompts — you can track which versions are cheapest
  v1: {
    system: 'You help with data analysis. Keep responses under 50 words.',
    template: 'Data: {data}\nQuestion: {question}\nAnswer:'
  },
  v2: {
    system: 'Analyze and summarize. Max 30 words.',
    template: '{question}\nBased on: {data}\nResult:'
  },
  v3: {
    // Optimized version after measuring token usage
    system: 'Concise data analyst. 20 words max.',
    template: '{question} → data: {data} →',
    estimatedTokens: { system: 8, template: 15 }
  }
}

// A/B test prompt versions for cost vs. quality
async function comparePromptVersions() {
  const results = []
  
  for (const [version, config] of Object.entries(PROMPT_TEMPLATES)) {
    const { text, usage } = await generateText({
      model: openai('gpt-4o-mini'),
      system: config.system,
      prompt: config.template
    })
    
    results.push({
      version,
      inputTokens: usage.promptTokens,
      outputTokens: usage.completionTokens,
      totalTokens: usage.promptTokens + usage.completionTokens,
      cost: usage.promptTokens * 0.00000015 + usage.completionTokens * 0.0000006,
      qualityScore: await rateResponseQuality(text) // Human or LLM rating
    })
  }
  
  return results.sort((a, b) => a.cost - b.cost)
}
```

## Phase 4: Model Selection (High ROI)

### The Model Tier System

Not every query needs GPT-4. Create a model routing system:

```javascript
class ModelRouter {
  constructor() {
    this.models = {
      'cheap': {
        model: 'gpt-4o-mini',
        costPerQuery: 0.001,  // Estimated
        capabilities: ['simple_qa', 'summarization', 'classification']
      },
      'medium': {
        model: 'claude-3-haiku',
        costPerQuery: 0.003,
        capabilities: ['data_analysis', 'code_generation', 'reasoning']
      },
      'premium': {
        model: 'gpt-4o',
        costPerQuery: 0.03,
        capabilities: ['complex_reasoning', 'creative_writing', 'edge_cases']
      }
    }
  }

  selectModel(feature, complexity, userTier) {
    // Simple features get cheap model
    if (['autocomplete', 'title_generation', 'tag_classification'].includes(feature)) {
      return this.models.cheap
    }

    // Free tier users get cheaper models
    if (userTier === 'free') {
      return this.models.cheap
    }

    // Complex features for paid users get premium
    if (complexity === 'high' && userTier === 'premium') {
      return this.models.premium
    }

    // Default to medium
    return this.models.medium
  }

  async generateWithRouter(feature, query, userTier) {
    const selectedModel = this.selectModel(feature, query.complexity, userTier)
    
    const startTime = Date.now()
    const result = await this.generate(selectedModel.model, query)
    const latency = Date.now() - startTime
    
    return {
      ...result,
      model: selectedModel.model,
      cost: selectedModel.costPerQuery,
      latency
    }
  }
}
```

### Model Selection Decision Tree

```
Is this a real-time feature (user waiting)?
├── Yes →
│   Is accuracy critical?
│   ├── Yes → GPT-4o or Claude 3.5 Sonnet
│   └── No → GPT-4o-mini or Claude 3 Haiku
└── No (batch/async) →
    → Cheapest model that meets quality threshold
    → Consider open-source (self-hosted Llama, Mistral)

Does this require reasoning or creativity?
├── Yes → Higher tier model (GPT-4o, Claude Sonnet)
└── No → Lower tier (GPT-4o-mini, Haiku)

Is this a free user or paid user?
├── Free → Cheapest tier (GPT-4o-mini)
├── Pro → Medium tier (Claude Haiku)
└── Enterprise → Premium tier (GPT-4o, Claude Sonnet)
```

## Phase 5: Batching and Queueing

### Batch Processing

Combine multiple independent AI tasks into one API call:

```javascript
class AIService {
  // Batch multiple classification tasks
  async batchClassify(items) {
    // Instead of N separate calls, make 1 call
    const prompt = `
    Classify each item into: [Category A, Category B, Category C]
    
    Items:
    ${items.map((item, i) => `${i + 1}. "${item.text}"`).join('\n')}
    
    Respond as JSON:
    { "classifications": [{ "index": 1, "category": "..." }, ...] }
    `
    
    const { text } = await generateText({
      model: openai('gpt-4o-mini'),
      prompt
    })
    
    return JSON.parse(text).classifications
  }
}
```

### Request Queueing for Async Tasks

```javascript
class AIQueryQueue {
  constructor() {
    this.queue = []
    this.processing = false
    this.batchSize = 10
    this.maxWaitMs = 5000
  }

  async enqueue(task) {
    return new Promise((resolve, reject) => {
      this.queue.push({ task, resolve, reject, enqueuedAt: Date.now() })
      this.processBatch()
    })
  }

  async processBatch() {
    if (this.processing) return
    this.processing = true

    while (this.queue.length > 0) {
      // Collect batch (either batchSize items or after maxWait)
      const batch = []
      const waitPromise = new Promise(resolve => setTimeout(resolve, this.maxWaitMs))
      
      while (batch.length < this.batchSize && this.queue.length > 0) {
        batch.push(this.queue.shift())
      }

      // Process batch
      const results = await Promise.allSettled(
        batch.map(item => item.task())
      )

      // Resolve individual promises
      results.forEach((result, i) => {
        if (result.status === 'fulfilled') {
          batch[i].resolve(result.value)
        } else {
          batch[i].reject(result.reason)
        }
      })
    }

    this.processing = false
  }
}
```

## Phase 6: User-Level Cost Controls

### Rate Limiting by Tier

```javascript
class AICostLimiter {
  constructor(redis) {
    this.redis = redis
    this.limits = {
      free: { queriesPerDay: 20, queriesPerHour: 5, maxCostPerDay: 0.05 },
      pro: { queriesPerDay: 500, queriesPerHour: 100, maxCostPerDay: 1.00 },
      enterprise: { queriesPerDay: 10000, queriesPerHour: 1000, maxCostPerDay: 20.00 }
    }
  }

  async checkLimit(userId, userTier) {
    const tier = userTier || 'free'
    const limits = this.limits[tier]
    
    // Check daily limit
    const dailyKey = `ai:limit:daily:${userId}:${this.getDate()}`
    const dailyCount = await this.redis.get(dailyKey) || 0
    if (parseInt(dailyCount) >= limits.queriesPerDay) {
      return { allowed: false, reason: 'daily_limit' }
    }
    
    // Check hourly limit
    const hourlyKey = `ai:limit:hourly:${userId}:${this.getHour()}`
    const hourlyCount = await this.redis.get(hourlyKey) || 0
    if (parseInt(hourlyCount) >= limits.queriesPerHour) {
      return { allowed: false, reason: 'hourly_limit' }
    }
    
    // Check cost limit (track cumulative cost)
    const costKey = `ai:limit:cost:${userId}:${this.getDate()}`
    const dailyCost = parseFloat(await this.redis.get(costKey) || '0')
    if (dailyCost >= limits.maxCostPerDay) {
      return { allowed: false, reason: 'cost_limit' }
    }

    return { allowed: true, remaining: {
      daily: limits.queriesPerDay - parseInt(dailyCount),
      hourly: limits.queriesPerHour - parseInt(hourlyCount),
      cost: limits.maxCostPerDay - dailyCost
    }}
  }

  recordQuery(userId, userTier, cost) {
    const keys = [
      `ai:limit:daily:${userId}:${this.getDate()}`,
      `ai:limit:hourly:${userId}:${this.getHour()}`,
      `ai:limit:cost:${userId}:${this.getDate()}`
    ]
    
    // Increment all counters
    keys.forEach(key => {
      this.redis.incr(key)
      if (key.includes('cost')) {
        this.redis.incrbyfloat(key, cost)
      }
    })
  }

  getDate() {
    return new Date().toISOString().split('T')[0]
  }

  getHour() {
    return `${this.getDate()}:${new Date().getHours()}`
  }
}
```

### Usage Dashboard for Users

Show users their AI usage to encourage conservation:

```javascript
// User-facing AI usage component
function AIUsageDashboard({ userId, tier }) {
  const [usage, setUsage] = useState(null)
  
  useEffect(() => {
    fetch(`/api/ai/usage/${userId}`)
      .then(res => res.json())
      .then(setUsage)
  }, [userId])

  if (!usage) return <Loading />

  const limits = {
    free: { queries: 20, cost: '$0.05' },
    pro: { queries: 500, cost: '$1.00' },
    enterprise: { queries: 10000, cost: '$20.00' }
  }

  const tierLimits = limits[tier]

  return (
    <div className="ai-usage-card">
      <h3>AI Usage Today</h3>
      <div className="usage-bar">
        <div 
          className="usage-fill" 
          style={{ width: `${(usage.queries / tierLimits.queries) * 100}%` }}
        />
      </div>
      <div className="usage-stats">
        <span>{usage.queries} / {tierLimits.queries} queries</span>
        <span>${usage.cost.toFixed(3)} / {tierLimits.cost}</span>
      </div>
      {usage.queries / tierLimits.queries > 0.8 && (
        <div className="usage-warning">
          You're approaching your daily AI limit. Upgrade for more.
        </div>
      )}
    </div>
  )
}
```

## Phase 7: Provider Optimization

### Multi-Provider Strategy

Different providers offer different pricing for similar quality:

```javascript
class AIProviderRouter {
  constructor() {
    this.providers = {
      openai: {
        models: {
          'gpt-4o-mini': { input: 0.00000015, output: 0.0000006 },
          'gpt-4o': { input: 0.0000025, output: 0.00001 }
        }
      },
      anthropic: {
        models: {
          'claude-3-haiku': { input: 0.00000025, output: 0.00000125 },
          'claude-3-sonnet': { input: 0.000003, output: 0.000015 }
        }
      },
      groq: {
        models: {
          'llama-3-8b': { input: 0.00000005, output: 0.00000008 },
          'llama-3-70b': { input: 0.00000059, output: 0.00000079 }
        }
      }
    }
  }

  getCheapestForTask(task, quality) {
    const candidates = []
    
    for (const [provider, config] of Object.entries(this.providers)) {
      for (const [model, pricing] of Object.entries(config.models)) {
        if (this.meetsQuality(model, quality)) {
          candidates.push({
            provider,
            model,
            inputCost: pricing.input,
            outputCost: pricing.output,
            estimatedTotal: (pricing.input + pricing.output) * 1.5 // estimate
          })
        }
      }
    }
    
    return candidates.sort((a, b) => a.estimatedTotal - b.estimatedTotal)[0]
  }

  meetsQuality(model, quality) {
    if (quality === 'high') {
      return ['gpt-4o', 'claude-3-sonnet'].includes(model)
    }
    if (quality === 'medium') {
      return ['gpt-4o-mini', 'claude-3-haiku', 'llama-3-70b'].includes(model)
    }
    // Low quality — any model works
    return true
  }
}
```

### Fallback Chains for Reliability and Cost

```javascript
async function generateWithFallback(task) {
  const routes = [
    { provider: 'groq', model: 'llama-3-70b', cost: 0.001 },
    { provider: 'openai', model: 'gpt-4o-mini', cost: 0.002 },
    { provider: 'anthropic', model: 'claude-3-haiku', cost: 0.003 },
  ]

  for (const route of routes) {
    try {
      const result = await callProvider(route.provider, route.model, task)
      trackCost(route.cost)
      return result
    } catch (error) {
      logFailure(route, error)
      continue // Try next provider
    }
  }

  throw new Error('All AI providers failed')
}
```

## Phase 8: Long-Term Cost Optimization

### Fine-Tuning: Lower Cost, Better Quality

Fine-tuned small models can match GPT-4 quality at GPT-4o-mini prices:

```
Cost comparison for 1M queries/month:

GPT-4o: $2,500/month (at ~$0.0025/query)
GPT-4o-mini: $150/month (at ~$0.00015/query)
Fine-tuned Llama 3 (8B): $50/month (at ~$0.00005/query)

Fine-tuning initial cost: ~$100-500
Payback period: 1-2 months vs. GPT-4o
```

**When to fine-tune:**
- You have 1,000+ high-quality examples
- Your task is well-defined (classification, extraction, structured output)
- You're making 10K+ queries/month on the task
- Quality with base model is good but not great

### Self-Hosting Economics

For high-volume features, self-hosting can be cheaper:

```
Break-even analysis:

API cost: $0.00015/query (GPT-4o-mini)
Self-hosted cost: ~$0.00002/query (Llama 3 8B on own GPU)

At 500K queries/month:
- API: $75/month
- Self-hosted: ~$10/month + $500-1000/month GPU rental
Break-even: ~3-6M queries/month

Self-hosted makes sense when:
- 100K+ queries/day
- Predictable traffic patterns
- You have DevOps expertise
- Latency requirements are flexible
```

### Monitoring Provider Pricing Changes

LLM pricing changes frequently (dropping 50-80%/year). Automate monitoring:

```javascript
// Weekly cost optimization report
async function generateCostReport() {
  const currentCosts = await getCurrentCostBreakdown()
  const alternativeCosts = await getAlternativeProviderCosts()

  const savingsOpportunities = []
  
  for (const [feature, { currentCost, queries, provider }] of Object.entries(currentCosts)) {
    for (const [altProvider, altCost] of Object.entries(alternativeCosts[feature] || {})) {
      if (altCost < currentCost && await testQuality(feature, altProvider)) {
        const monthlySavings = (currentCost - altCost) * queries * 30
        savingsOpportunities.push({
          feature,
          from: provider,
          to: altProvider,
          monthlySavings,
          qualityTest: 'passed'
        })
      }
    }
  }

  return {
    currentMonthlyCost: Object.values(currentCosts).reduce((s, f) => s + f.currentCost, 0),
    potentialMonthlyCost: currentMonthlyCost - savingsOpportunities.reduce((s, o) => s + o.monthlySavings, 0),
    savingsOpportunities: savingsOpportunities.sort((a, b) => b.monthlySavings - a.monthlySavings)
  }
}
```

## Cost Management Cheat Sheet

```
DAILY CHECKLIST:

[ ] Check daily AI spend (target: under $__)
[ ] Verify cache hit rate > 30%
[ ] Check for cost anomalies (single user > $10)
[ ] Review prompt token counts (trending down?)
[ ] Check model distribution (80%+ on cheap models?)

WEEKLY CHECKLIST:

[ ] Analyze cost by feature (focus on most expensive)
[ ] Review and update prompt templates
[ ] Check provider pricing changes
[ ] A/B test cheaper model alternatives
[ ] Identify users approaching rate limits

MONTHLY CHECKLIST:

[ ] Calculate AI cost as % of revenue (target: < 10%)
[ ] Review fine-tuning opportunities
[ ] Evaluate self-hosting for high-volume features
[ ] Update cost dashboard and alerts
[ ] Plan model migrations (as pricing changes)

EMERGENCY PROCEDURES:

If daily cost exceeds 2x budget:
1. Reduce free tier limits immediately
2. Route all traffic to cheapest model
3. Enable aggressive caching
4. Investigate top cost users
5. Consider temporarily disabling expensive features
```

## The Solo Founder's LLM Cost Strategy

1. **Start with GPT-4o-mini for everything.** It handles 80% of tasks at 10% of the cost of GPT-4o.

2. **Cache aggressively from day one.** Before writing any AI feature, write the cache layer. It's the highest ROI optimization.

3. **Track costs before they track you.** Set up cost monitoring before launch. Know your cost per user, per feature, per query.

4. **Set hard limits.** Free tier: 20 queries/day. Pro: 500 queries/day. These limits protect you while you learn actual usage patterns.

5. **Optimize prompts and then optimize again.** The cheapest optimization is removing unnecessary tokens. Every word in your prompt costs money.

6. **Use the right model for the right task.** Simple tasks on cheap models. Complex tasks on premium models. Route intelligently.

7. **Batch when you can.** Combine multiple simple AI tasks into one call. Queue async tasks for batch processing.

8. **Monitor and adjust daily.** AI costs can triple overnight if something changes (model update, user behavior, abuse). Never go more than a day without checking.

9. **Fine-tune when it makes economic sense.** If you spend $500+/month on a specific task, fine-tuning will probably pay for itself in 1-2 months.

10. **Plan for declining costs.** Model prices drop 50-80%/year. Features that aren't economical today will be in 6 months. Don't over-optimize for current pricing.

Your AI features should be profitable from day one. Cost management is not an afterthought — it's a core feature of your AI strategy. Build it in from the start.
