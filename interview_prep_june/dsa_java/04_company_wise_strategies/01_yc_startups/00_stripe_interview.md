# Stripe Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Stripe Engineering Culture
4. Types of Problems
5. Example Problems with Approaches
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background discussion
- Role expectations
- Stripe culture overview

### Technical Screen (60 min)
- 1-2 coding problems on CoderPad
- Stripe uses a shared editor — you'll write actual working code
- Expect practical, real-world problems

### On-site (4-5 rounds, 45-60 min each)
- **Coding** (2 rounds): Practical programming, API design, algorithms
- **System Design** (1): For senior roles
- **Debugging** (1): Find and fix issues in existing code
- **Behavioral / Stripe-yness** (1): Culture fit

### Key Differences
- Stripe focuses on practical, real-world problems
- API design is a significant component
- They value writing clean, maintainable, testable code
- Strong emphasis on developer experience
- Questions often relate to payments, money, financial systems

---

## 2. Most Asked Topics

| Topic | Frequency | Why Stripe Asks It |
|-------|-----------|-------------------|
| Arrays & Strings | High | Transaction processing |
| HashMaps | High | Payment lookup, reconciliation |
| API Design | Very High | Stripe's core product |
| Concurrency | Medium | Payment race conditions |
| Trees | Medium | Category hierarchies, tax |
| Design Patterns | Medium | Extensible payment systems |
| Debugging | Medium | Production issue resolution |
| SQL / Data | Low-Medium | Reporting, analytics |

### Topic Frequency Graph
```
API Design: ████████████████████
Arrays:     ████████████████
Hash:       ████████████████
Concurr:    ████████
Trees:      ██████
Debugging:  ██████
SQL:        ████
```

---

## 3. Stripe Engineering Culture

### Key Values
- **Write idiomatic code** — Follow language conventions
- **Make it work, then make it beautiful** — Correctness first, then refactor
- **API design mindset** — Every function is an API; design it thoughtfully
- **Incremental progress** — Ship small changes frequently
- **Developer empathy** — Code should be easy to understand and use
- **Ownership** — You build it, you run it

### Stripe Interview Focus
- Can you write production-quality code?
- Do you think about edge cases and error states?
- Can you design clean APIs?
- Do you understand idempotency, transactions, race conditions?

---

## 4. Types of Problems

### API Design
- Design a payment API
- Design a webhook delivery system
- Design an API for transferring money between accounts
- Rate limiting API design
- API versioning strategy

### Practical Algorithms
- **Balance checking / reconciliation** — Arrays, HashMaps
- **Transaction validation** — State machines, rules
- **Currency conversion** — Graph of rates, shortest path
- **Fraud detection** — Frequency counting, sliding window

### Concurrency and Race Conditions
- Idempotency keys — preventing duplicate charges
- Concurrent payment processing — locking strategies
- Distributed transactions — 2PC, Saga pattern

### Debugging
- Given a buggy implementation, identify and fix issues
- Race condition identification
- Memory leak detection
- Performance bottleneck analysis

---

## 5. Example Problems with Approaches

### Problem 1: Design a Money Transfer API
**Problem:** Design an API to transfer money between accounts.

**API Design:**
```
POST /v1/transfers
Request: {
  "amount": 1000,
  "currency": "usd",
  "source": "acct_123",
  "destination": "acct_456",
  "idempotency_key": "unique_key_123"
}
Response: {
  "id": "tr_789",
  "status": "succeeded",
  "amount": 1000,
  "created": 1620000000
}
```

**Considerations:**
- **Idempotency** — Same request can be retried safely
- **Atomicity** — Both accounts must be updated or neither
- **Concurrency** — Prevent double-spending
- **Currency support** — Handle different currencies, conversion
- **Error handling** — Insufficient funds, invalid accounts, network errors

### Problem 2: Validate Balanced Brackets (But with Money)
**Problem:** Given a string of transactions with parentheses, validate they are properly balanced.

**Approach:** Stack-based bracket matching.
```java
public boolean isValid(String s) {
    Stack<Character> stack = new Stack<>();
    for (char c : s.toCharArray()) {
        if (c == '(') stack.push(')');
        else if (c == '{') stack.push('}');
        else if (c == '[') stack.push(']');
        else if (stack.isEmpty() || stack.pop() != c) return false;
    }
    return stack.isEmpty();
}
```

### Problem 3: Design a Rate Limiter (Token Bucket)
**Problem:** Design a rate limiter for API endpoints.

**Approach:** Token bucket or sliding window log.
```java
class RateLimiter {
    private final long maxTokens;
    private final long refillRate; // tokens per second
    private double tokens;
    private long lastRefillTime;

    public RateLimiter(long maxTokens, long refillRate) {
        this.maxTokens = maxTokens;
        this.refillRate = refillRate;
        this.tokens = maxTokens;
        this.lastRefillTime = System.currentTimeMillis();
    }

    public synchronized boolean allow() {
        refill();
        if (tokens > 0) {
            tokens--;
            return true;
        }
        return false;
    }

    private void refill() {
        long now = System.currentTimeMillis();
        double elapsed = (now - lastRefillTime) / 1000.0;
        tokens = Math.min(maxTokens, tokens + elapsed * refillRate);
        lastRefillTime = now;
    }
}
```

### Problem 4: Currency Conversion (Graph)
**Problem:** Given exchange rates between currencies, convert amount from one to another.

**Approach:** Build graph of rates, BFS/DFS with multiplication.
```java
public double convert(String from, String to, double amount,
                      Map<String, Map<String, Double>> rates) {
    if (!rates.containsKey(from)) return -1;
    Queue<Pair> queue = new LinkedList<>();
    Set<String> visited = new HashSet<>();
    queue.offer(new Pair(from, amount));
    visited.add(from);
    while (!queue.isEmpty()) {
        Pair cur = queue.poll();
        if (cur.currency.equals(to)) return cur.amount;
        Map<String, Double> neighbors = rates.get(cur.currency);
        if (neighbors != null) {
            for (Map.Entry<String, Double> e : neighbors.entrySet()) {
                if (!visited.contains(e.getKey())) {
                    visited.add(e.getKey());
                    queue.offer(new Pair(e.getKey(), cur.amount * e.getValue()));
                }
            }
        }
    }
    return -1;
}
```

---

## 6. Preparation Strategy

### Focus Areas

1. **Practical Coding (50%)**
   - Arrays, strings, HashMaps — the bread and butter
   - Write clean, production-quality code
   - Practice with Python or Ruby (Stripe uses these extensively)

2. **API Design (30%)**
   - RESTful API design principles
   - Request/response format
   - Error handling and status codes
   - Rate limiting, pagination, idempotency

3. **System Design / Concurrency (20%)**
   - Distributed transactions
   - Race conditions and locking
   - Event-driven architecture
   - Database consistency models

### Stripe-Specific Tips
1. **Write clean code** — Stripe values developer experience
2. **Think about errors** — What happens when things go wrong?
3. **Consider idempotency** — It's central to payment systems
4. **Test your code** — Mentally run through test cases
5. **Know your payment basics** — Understand how money moves
6. **Show API mindset** — Every method signature is an API contract
7. **Be thorough with edge cases** — Stripe engineers are meticulous
