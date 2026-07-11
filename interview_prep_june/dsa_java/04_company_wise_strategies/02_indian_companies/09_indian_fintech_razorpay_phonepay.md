# Indian Fintech — Razorpay, PhonePe, CRED, Groww

> "Indian fintech companies test practical problem-solving with real-world scenarios. They focus on payment systems, transaction processing, and system design. Known for medium-difficulty problems with practical context."

---

## 1. Company Overview

### Razorpay
- **Package:** ₹15-35 LPA (freshers)
- **Focus:** Payment gateway, financial infrastructure
- **Known for:** Clean engineering, fast-paced environment

### PhonePe
- **Package:** ₹12-30 LPA (freshers)
- **Focus:** UPI payments, financial services
- **Known for:** Scale (millions of daily transactions)

### CRED
- **Package:** ₹15-35 LPA (freshers)
- **Focus:** Credit payments, rewards platform
- **Known for:** Elegant engineering, product focus

### Groww
- **Package:** ₹12-25 LPA (freshers)
- **Focus:** Investment platform, mutual funds
- **Known for:** Clean code, product thinking

### Common Pattern
- **Rounds:** Online Test → Technical (2-3 rounds) → HR
- **Focus:** DSA, System Design, Practical Problem-Solving
- **Difficulty:** Medium (not as hard as FAANG, but practical)

---

## 2. Most Asked Topics

### Topic Priority (All Fintech)

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 85% | Sliding window, two pointers |
| 2 | HashMaps | 80% | Frequency, grouping, caching |
| 3 | DP | 65% | Medium DP, optimization |
| 4 | System Design | 60% | Payment systems, scalability |
| 5 | Trees | 55% | BST basics, traversals |
| 6 | Strings | 50% | Parsing, validation |
| 7 | Concurrency | 40% | Thread safety, locks |

### Fintech-Specific Topics
- **Transaction matching** — Pair debits and credits
- **Payment splitting** — Divide amounts among multiple parties
- **Fraud detection** — Pattern recognition in transactions
- **Rate limiting** — Throttle API requests
- **Idempotency** — Handle duplicate transactions safely

---

## 3. Company-Specific Focus

### Razorpay
- **Heavy DSA** — Medium-Hard problems
- **System design** — Payment gateway architecture
- **Concurrency** — Thread-safe payment processing
- **Go/Rust preferred** — But Java also accepted

### PhonePe
- **Scale-focused** — How to handle millions of transactions
- **System design** — UPI architecture, real-time processing
- **DP problems** — Optimization for financial calculations
- **SQL** — Database queries for transaction data

### CRED
- **Product thinking** — How features affect user experience
- **Clean code** — Elegant, maintainable solutions
- **Medium difficulty** — Focus on correctness
- **OOP design** — Design patterns in financial context

### Groww
- **Practical problems** — Real-world financial scenarios
- **System design** — Investment platform architecture
- **Data structures** — Efficient data management
- **Clean engineering** — Production-ready code

---

## 4. Example Problems

### Problem 1: Two Sum (Transaction Matching)
**Why fintech asks this:** Finding matching transaction pairs.

```java
import java.util.*;

public class TransactionMatching {

    // APPROACH: HashMap — find two transactions that sum to target
    // Real-world: Match a debit of X with a credit of Y
    
    public static int[] findMatchingPair(int[] transactions, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < transactions.length; i++) {
            int complement = target - transactions[i];
            
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            
            map.put(transactions[i], i);
        }
        
        return new int[]{-1, -1};
    }

    // VARIANT: Split bill among friends
    // Given amounts each person paid, find who owes whom
    public static void splitBill(int[] amounts) {
        int total = 0;
        for (int amount : amounts) total += amount;
        
        int avg = total / amounts.length;
        List<int[]> transfers = new ArrayList<>();
        
        for (int i = 0; i < amounts.length; i++) {
            int diff = amounts[i] - avg;
            if (diff > 0) {
                // This person overpaid — others owe them
                System.out.println("Person " + i + " is owed " + diff);
            } else if (diff < 0) {
                // This person underpaid — they owe others
                System.out.println("Person " + i + " owes " + (-diff));
            }
        }
    }

    public static void main(String[] args) {
        int[] transactions = {100, 200, 300, 400, 500};
        int[] result = findMatchingPair(transactions, 500);
        System.out.println("Match: " + result[0] + ", " + result[1]); // 0, 3
        
        int[] amounts = {40, 20, 40, 60};
        splitBill(amounts);
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 2: Rate Limiter (Sliding Window)
**Why fintech asks this:** Rate limiting is critical for payment APIs.

```java
import java.util.*;

public class RateLimiter {

    // APPROACH: Sliding window with TreeMap
    // Track timestamps of requests
    // Remove old timestamps outside the window
    // Allow if count < limit
    
    private int maxRequests;
    private int windowSizeMs;
    private TreeMap<Long, Integer> timestamps;
    
    public RateLimiter(int maxRequests, int windowSizeMs) {
        this.maxRequests = maxRequests;
        this.windowSizeMs = windowSizeMs;
        this.timestamps = new TreeMap<>();
    }
    
    public synchronized boolean allowRequest(long timestampMs) {
        // Remove timestamps outside the window
        long windowStart = timestampMs - windowSizeMs;
        timestamps.headMap(windowStart, true).clear();
        
        // Count requests in current window
        int totalRequests = 0;
        for (int count : timestamps.values()) {
            totalRequests += count;
        }
        
        if (totalRequests < maxRequests) {
            timestamps.merge(timestampMs, 1, Integer::sum);
            return true;
        }
        
        return false;
    }

    public static void main(String[] args) {
        RateLimiter limiter = new RateLimiter(3, 1000); // 3 requests per second
        
        System.out.println(limiter.allowRequest(1000)); // true
        System.out.println(limiter.allowRequest(1100)); // true
        System.out.println(limiter.allowRequest(1200)); // true
        System.out.println(limiter.allowRequest(1300)); // false (over limit)
        System.out.println(limiter.allowRequest(2001)); // true (new window)
    }
}
```

**Time:** O(log n) per request | **Space:** O(n)

---

### Problem 3: Longest Increasing Subsequence (Portfolio Growth)
**Why fintech asks this:** Finding longest growth streak in stock prices.

```java
import java.util.*;

public class LIS {

    // O(n log n) Binary Search approach
    public static int lengthOfLIS(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        
        for (int num : nums) {
            int pos = Collections.binarySearch(tails, num);
            if (pos < 0) pos = -(pos + 1);
            
            if (pos == tails.size()) {
                tails.add(num);
            } else {
                tails.set(pos, num);
            }
        }
        
        return tails.size();
    }

    public static void main(String[] args) {
        int[] prices = {10, 9, 2, 5, 3, 7, 101, 18};
        System.out.println(lengthOfLIS(prices)); // 4
    }
}
```

**Time:** O(n log n) | **Space:** O(n)

---

### Problem 4: Maximum Subarray Sum (Daily Transaction Totals)
```java
public class MaxSubarraySum {

    public static int maxSubarraySum(int[] nums) {
        int maxSum = nums[0];
        int currentSum = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        
        return maxSum;
    }

    public static void main(String[] args) {
        int[] transactions = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println(maxSubarraySum(transactions)); // 6
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 5: Coin Change (Payment Denominations)
```java
import java.util.Arrays;

public class CoinChange {
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] > amount ? -1 : dp[amount];
    }
    
    public static void main(String[] args) {
        int[] denominations = {1, 5, 10, 25};
        System.out.println(coinChange(denominations, 30)); // 2
    }
}
```

---

## 5. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Arrays and HashMaps
- [ ] Sliding window problems (10 problems)
- [ ] Two pointer technique (10 problems)
- [ ] HashMap patterns (10 problems)
- [ ] Prefix sums (5 problems)
- [ ] Practice: 25 problems

#### Week 2: DP and Trees
- [ ] 1D DP (10 problems)
- [ ] 2D DP (5 problems)
- [ ] BST basics (10 problems)
- [ ] Binary tree traversals (5 problems)
- [ ] Practice: 20 problems

#### Week 3: System Design and Concurrency
- [ ] Payment system design
- [ ] Rate limiter implementation
- [ ] Thread-safe data structures
- [ ] Idempotency patterns
- [ ] Practice: 5 system designs + 10 coding problems

#### Week 4: Fintech-Specific + Mocks
- [ ] Transaction matching problems
- [ ] Split bill algorithms
- [ ] Fraud detection patterns
- [ ] Mock interviews (3-5 sessions)
- [ ] Review and consolidate

### Fintech-Specific Tips
1. **Practical context** — Frame problems in payment/financial context
2. **System design** — Payment gateway, rate limiting, idempotency
3. **Concurrency** — Thread-safe payment processing
4. **Scale thinking** — How to handle millions of daily transactions
5. **Edge cases** — Failed transactions, duplicates, race conditions
6. **Clean code** — Financial code must be maintainable
7. **Medium problems are enough** — Focus on correctness
8. **SQL basics** — Transaction queries, data analysis

### Common Follow-up Questions
- "How would you handle a failed payment?"
- "What if two payments arrive simultaneously?"
- "How would you ensure idempotency?"
- "How would this scale to 10M daily transactions?"
- "How would you handle currency conversion?"

---

> **Remember:** Indian fintech values practical problem-solving. Frame your algorithms in the context of payments and transactions. Show that you can build reliable, scalable financial systems.
