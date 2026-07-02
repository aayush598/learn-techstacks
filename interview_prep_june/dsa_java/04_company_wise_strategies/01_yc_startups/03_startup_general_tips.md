# General Tips for YC Startup Interviews

## Table of Contents
1. How Startup Interviews Differ
2. What Startups Look For
3. Most Common DSA Topics
4. Practical Strategies
5. Common Mistakes
6. Company-Specific Notes

---

## 1. How Startup Interviews Differ from Big Tech

| Aspect | Big Tech (FAANG) | Startups (YC) |
|--------|-----------------|---------------|
| **Interview Rounds** | 5-7 rounds | 3-4 rounds |
| **System Design** | Heavy for senior | Lightweight or skipped |
| **LeetCode Style** | Algorithm-focused | Practical, project-based |
| **Behavioral** | Standardized | Founder-driven, culture fit |
| **Timeline** | 2-3 months | 1-3 weeks |
| **Coding Environment** | Shared editor | Often real codebase or project |
| **Take-home Projects** | Rare | Common (esp. early-stage) |

### Why Startups Interview Differently
- Startups need engineers who can ship quickly
- Generalists who can work across the stack
- Pragmatists who make trade-offs, not perfectionists
- Self-starters who thrive with less structure

---

## 2. What Startups Look For

### Top Qualities

| Quality | Why Important | How to Demonstrate |
|---------|--------------|-------------------|
| **Speed of execution** | Startups need results fast | Solve problems quickly, not perfectly |
| **Pragmatism** | Trade-offs > perfection | Discuss when O(n²) is OK |
| **Full-stack mindset** | Everyone does everything | Mention frontend, backend, infra experience |
| **Communication** | Small teams, high alignment | Clear explanations, whiteboarding |
| **Product sense** | Engineers contribute to roadmap | Ask about users and value |
| **Ownership** | No one else to pick up slack | Take full responsibility for deliverables |

### What Matters MORE Than Algorithms
1. **Can you ship?** — Have you built and deployed things?
2. **Do you understand the product?** — Do you care about what they're building?
3. **Can you grow?** — Early employees become leaders as company scales
4. **Are you low-ego?** — No room for politics in small teams

---

## 3. Most Common DSA Topics

### Core Topics (90% of startup interviews)
| Topic | Why Still Asked | Difficulty |
|-------|----------------|------------|
| Arrays | Universal | Easy-Medium |
| Strings | Practical, common | Easy-Medium |
| HashMaps | O(1) lookup, frequency | Easy |
| Trees (DFS/BFS) | Real-world data | Medium |
| Basic DP | Optimization | Medium |
| Sorting | Foundation | Easy |
| Two Pointers | Sliding window | Medium |

### Advanced Topics (Rare in startups)
| Topic | When Asked | Skip For |
|-------|-----------|----------|
| Tries | Autocomplete features | Most interviews |
| Segment Trees | Range queries | 95% of startups |
| Bitmask DP | Optimization (rare) | Early-stage |
| KMP | String matching | Almost never |
| Union-Find | Connectivity | Late-stage only |

### Important Caveat
Don't skip DSA entirely — startups still do coding rounds. But they're more pragmatic about it. A working O(n²) solution with clean code often beats a buggy O(n) solution.

---

## 4. Practical Strategies

### Before the Interview
1. **Research the company deeply**
   - What do they build? (YC company page, Crunchbase)
   - What tech stack do they use?
   - Who are their competitors?
   - What stage are they at? (Seed? Series A? B?)

2. **Align your experience**
   - Highlight relevant projects
   - Show interest in their domain
   - Mention how you'd add value specifically

3. **Prepare the "Why this startup?" answer**
   - Generic "I love your product" is weak
   - Be specific about what you'd want to work on

### During the Interview

1. **Be pragmatic with algorithms**
   - Start with a working solution, then optimize
   - If stuck, a simpler correct solution is better than nothing
   - Explain trade-offs: "This is O(n²) but for our input size it's fine"

2. **Show full-stack awareness**
   - "This algorithm goes on the backend, but I'd cache it in Redis"
   - "We'd need to consider database query patterns here"
   - "API latency vs batch processing trade-off"

3. **Ask smart questions**
   - "How does this feature impact the user experience?"
   - "What's the scale we're designing for?"
   - "Is this handling real-time or batch data?"

### Take-Home Projects

Many YC startups give take-home projects. Tips:
- **Prioritize functionality** — Make it work first
- **Write clean code** — They WILL read your code
- **Include tests** — Shows engineering discipline
- **Add a README** — Explain your design decisions
- **Don't over-engineer** — Simple solutions score higher
- **Send on time** — Late submissions look bad
- **Be prepared to discuss** — They'll want to know why you made certain choices

---

## 5. Common Mistakes

| Mistake | Why It Hurts | Better Approach |
|---------|-------------|-----------------|
| Ignoring the product | Looks like you don't care | Ask product questions |
| Over-engineering | Slow, unnecessary complexity | Ship simple, working code |
| LeetCode grinding without context | Can't explain trade-offs | Focus on practical reasoning |
| Not asking questions | Seems disinterested | Ask about challenges, scale, users |
| Being too academic | Unrealistic for startup pace | Discuss real-world practicalities |
| Not preparing for behavioral | "Fit" matters more in small teams | Prepare stories showing ownership |
| Not showing growth mindset | Startups need adaptable people | Talk about learning new things |
| Focusing only on algorithms | Missing the bigger picture | Show you think about the system |

---

## 6. Company-Specific Notes

### By Stage

**Seed Stage (1-10 employees):**
- Founder will interview you directly
- Focus on: Can you build things independently?
- DSA: Lightweight, more practical
- Might ask: "Build a simple web app that does X"
- What matters: Versatility, speed, low ego

**Series A (10-50 employees):**
- Still founder-heavy interviews
- Focus on: Ownership + technical depth
- DSA: Medium difficulty
- Might ask: System design for 10x scale
- What matters: Reliability, growth potential

**Series B+ (50+ employees):**
- More structured process
- Focus on: Team fit + scalability thinking
- DSA: Medium-Hard, similar to FAANG lite
- Might ask: Full loop with 3-4 rounds
- What matters: Leadership, mentoring, scaling

### Example YC Startup Prep Notes

| Company Type | Focus Topics | Key Questions |
|-------------|-------------|---------------|
| **B2B SaaS** | APIs, data processing, access control | Design an API, handle multi-tenancy |
| **Marketplace** | Search, matching, ranking | Paginate results, match buyers/sellers |
| **Fintech** | Transactions, reconciliation, fraud | Handle idempotency, detect fraud patterns |
| **DevTools** | CLI tools, parsing, automation | Parse config files, build a CLI |
| **Healthcare** | Data validation, HIPAA compliance | Validate records, handle PII |
| **AI/ML** | Data pipelines, feature engineering | Process training data, feature extraction |
