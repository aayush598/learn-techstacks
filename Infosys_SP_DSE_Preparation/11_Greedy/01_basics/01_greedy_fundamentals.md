# Greedy Fundamentals - Complete Guide

## Table of Contents
1. [What is Greedy Algorithm](#1-what-is-greedy-algorithm)
2. [When to Use Greedy](#2-when-to-use-greedy)
3. [Greedy vs DP](#3-greedy-vs-dp)
4. [Activity Selection Problem](#4-activity-selection-problem)
5. [Fractional Knapsack](#5-fractional-knapsack)
6. [Minimum Number of Coins](#6-minimum-number-of-coins)
7. [Assign Cookies](#7-assign-cookies)
8. [Lemonade Change](#8-lemonade-change)

---

## 1. What is Greedy Algorithm

A **greedy algorithm** builds a solution piece by piece, always choosing the **locally optimal** option at each step with the hope of finding a **global optimum**.

### The Intuition

Imagine you are at a buffet and want to fill your plate to maximize deliciousness.
A greedy approach: at each step, pick the tastiest item available right now.
You never go back to swap — you just keep picking the best you see.

```
  BUFFET TABLE (items with values)
  ┌──────────────────────────────────────────────────┐
  │  [Cake=9]  [Pizza=7]  [Pasta=5]  [Salad=2]      │
  │     1          2          3          4            │
  └──────────────────────────────────────────────────┘

  GREEDY PICK ORDER:  Cake(9) -> Pizza(7) -> Pasta(5) -> Salad(2)
  At each step, pick the HIGHEST value item remaining.
```

### Core Principles

```python
# Greedy Algorithm Template
def greedy_algorithm(input):
    # STEP 1: Sort/organize by greedy criterion
    #         (earliest deadline? highest value? best ratio?)
    sorted_input = sort_by_criterion(input)
    
    # STEP 2: Initialize result
    result = initial_value
    
    # STEP 3: Process items one by one
    for item in sorted_input:
        # STEP 4: Check if this item fits / is valid
        if can_add(item, result):
            # STEP 5: Make the greedy choice (never reconsider)
            result = update_result(item, result)
    
    return result
```

### Step-by-Step Walkthrough: Simple Greedy

```
  Problem: Pick maximum non-overlapping intervals
  
  Intervals sorted by finish time:
  ──────────────────────────────────────────────
  Time:  0  1  2  3  4  5  6  7  8  9  10
         │──A──│                     A finishes at 4
              │──────B──────│        B finishes at 6
                     │──C──│        C finishes at 8
                            │──D──│  D finishes at 10
  ──────────────────────────────────────────────
  
  Step 1: Pick A (finishes earliest at t=4) ✓
          last_finish = 4
  
  Step 2: B starts at 3, but 3 < 4 → OVERLAP → SKIP B
  
  Step 3: C starts at 5, and 5 >= 4 → PICK C ✓
          last_finish = 8
  
  Step 4: D starts at 9, and 9 >= 8 → PICK D ✓
          last_finish = 10
  
  RESULT: [A, C, D] — 3 activities selected
```

### Key Properties

1. **Greedy Choice Property**: A globally optimal solution can be arrived at by making locally optimal choices
2. **Optimal Substructure**: An optimal solution to the problem contains optimal solutions to subproblems

```
  ╔═══════════════════════════════════════════════════════╗
  ║           GREEDY CHOICE PROPERTY (visual)            ║
  ╠═══════════════════════════════════════════════════════╣
  ║                                                       ║
  ║   Global Optimal Solution                             ║
  ║   ┌─────┬─────┬─────┬─────┐                         ║
  ║   │ g₁  │ g₂  │ g₃  │ g₄  │                         ║
  ║   └──┬──┴─────┴─────┴─────┘                         ║
  ║      │                                                ║
  ║      ▼                                                ║
  ║   First choice g₁ is locally optimal                 ║
  ║   Remaining g₂..g₄ is also optimal for subproblem    ║
  ║                                                       ║
  ╚═══════════════════════════════════════════════════════╝
```

## 2. When to Use Greedy

### Decision Flowchart: Should I Use Greedy?

```
                    ┌─────────────────────────┐
                    │  Can I make a locally   │
                    │  optimal choice at each  │
                    │        step?             │
                    └────────┬────────────────┘
                             │
                    ┌────────▼────────┐
               YES  │                 │  NO
                    │                 ├──────────────► Use DP / Brute Force
                    ▼                 │
          ┌─────────────────────┐     │
          │ Does this local     │     │
          │ choice guarantee a  │     │
          │ global optimum?     │     │
          └────────┬────────────┘     │
                   │                  │
          ┌────────▼────────┐         │
     YES  │                 │  NO     │
          │                 ├─────────┘
          ▼                 │
    ┌───────────┐           │
    │ USE GREEDY│           │
    └───────────┘           │
```

### Greedy Works When

```python
# 1. Greedy Choice Property exists
#    Making the locally optimal choice leads to global optimum

# 2. Optimal Substructure
#    Optimal solution contains optimal solutions to subproblems

# 3. No backtracking needed
#    Once a choice is made, it's never undone
```

### Common Greedy Patterns

| Pattern | Key Idea | Example Problems |
|---------|----------|-----------------|
| **Sorting by criterion** | Order items by greedy metric | Activity selection, Interval merging |
| **Priority queue** | Always process "most important" first | Task scheduling, Huffman coding |
| **Two pointers** | Match from both ends of sorted array | Assign Cookies, Two Sum sorted |
| **Mathematical proof** | Prove local = global via exchange argument | Fractional knapsack |
| **Exchange argument** | Show swapping with greedy improves it | Minimum spanning tree |

### Greedy Fails: 0/1 Knapsack Example

```
  Capacity = 50
  ┌────────┬────────┬────────┬──────────────────────────┐
  │  Item  │ Weight │ Value  │ Value/Weight Ratio       │
  ├────────┼────────┼────────┼──────────────────────────┤
  │   A    │   10   │   60   │  6.0  ◄── greedy picks  │
  │   B    │   20   │  100   │  5.0                      │
  │   C    │   30   │  120   │  4.0                      │
  └────────┴────────┴────────┴──────────────────────────┘

  Greedy by ratio:  A + B = weight 30, value 160
  Optimal (DP):     B + C = weight 50, value 220  ← BETTER!

  Why greedy fails: it picks A (ratio 6.0) but that leaves
  only 40 capacity, and B+C (weight 50) doesn't fit.
  The globally optimal choice is B+C without A.
```

---

## 3. Greedy vs DP

```python
# Greedy: O(n log n) or O(n)
# DP: O(n * capacity) or O(n²)

# When to use which:

# GREEDY:
# - Fractional knapsack
# - Activity selection
# - Huffman coding
# - Minimum spanning tree

# DP:
# - 0/1 Knapsack
# - Longest common subsequence
# - Edit distance
# - Matrix chain multiplication
```

### Comparison Table

| Aspect | Greedy | DP |
|--------|--------|-----|
| Approach | Local optimum | All subproblems |
| Time | Usually faster | Usually slower |
| Space | Usually O(1) | Usually O(n) |
| Correctness | Needs proof | Always correct |
| Backtracking | No | Yes |

### Visual Comparison

```
  GREEDY APPROACH:                    DP APPROACH:
  ────────────────                    ────────────
  Make one choice, never undo         Explore all choices
  
  Start                               Start
    │                                   │
    ▼                                   ├──── Choose A ────┐
  Pick BEST option now                  │                   │
    │                                   ├──── Choose B ────┤
    ▼                                   │                   │
  Pick BEST option now                  ├──── Choose C ────┤
    │                                   │                   │
    ▼                                   ▼                   ▼
  DONE (one path)                   Compare all paths,
                                    pick the best
  
  Time: O(n) to O(n log n)          Time: O(2^n) to O(n*w)
  Space: O(1)                       Space: O(n) to O(n*w)
```

---

## 4. Activity Selection Problem

**Problem**: Select maximum number of non-overlapping activities.

### Visual Explanation

```
  All activities on a timeline:
  
  Time: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
        │──A──│                                          A=(1,4)
           │────B────│                                   B=(3,5)
        │────────C────────│                              C=(0,6)
                          │──D──│                        D=(5,7)
              │──────────────E──────────────│            E=(3,9)
                    │────────F────────│                  F=(5,9)
                       │────────G────────│              G=(6,10)
                                  │──H──│               H=(8,11)
                                  │────────I────────│   I=(8,12)
        │──────────────J──────────────│                  J=(2,14)
                                                │──K──│ K=(12,16)

  SORTED BY FINISH TIME:
  ┌─────┬───────┬────────┐
  │ Act │ Start │ Finish │
  ├─────┼───────┼────────┤
  │  A  │   1   │    4   │ ◄── Pick first (earliest finish)
  │  B  │   3   │    5   │     3 < 4 → SKIP
  │  C  │   0   │    6   │     0 < 4 → SKIP
  │  D  │   5   │    7   │     5 >= 4 → PICK ✓
  │  E  │   3   │    9   │     3 < 7 → SKIP
  │  F  │   5   │    9   │     5 < 7 → SKIP
  │  G  │   6   │   10   │     6 < 7 → SKIP
  │  H  │   8   │   11   │     8 >= 7 → PICK ✓
  │  I  │   8   │   12   │     8 < 11 → SKIP
  │  J  │   2   │   14   │     2 < 11 → SKIP
  │  K  │  12   │   16   │    12 >= 11 → PICK ✓
  └─────┴───────┴────────┘

  RESULT: [A, D, H, K] → 4 activities
```

```python
def activity_selection(activities):
    """
    Select maximum number of non-overlapping activities.
    activities: list of (start, finish) times
    """
    # Sort by finish time
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_finish = activities[0][1]
    
    for i in range(1, len(activities)):
        start, finish = activities[i]
        
        # If activity starts after last selected finishes
        if start >= last_finish:
            selected.append(activities[i])
            last_finish = finish
    
    return selected

# Example
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
selected = activity_selection(activities)
print(f"Selected activities: {selected}")
print(f"Maximum activities: {len(selected)}")
# Output: [(1, 4), (5, 7), (8, 11), (12, 16)]
# Maximum activities: 4
```

### Proof of Correctness

```python
def activity_selection_with_proof(activities):
    """Activity selection with proof of optimality."""
    # Sort by finish time (greedy choice)
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_finish = activities[0][1]
    
    for i in range(1, len(activities)):
        start, finish = activities[i]
        
        if start >= last_finish:
            selected.append(activities[i])
            last_finish = finish
    
    print("Proof of optimality:")
    print("1. Greedy choice: Always pick activity with earliest finish time")
    print("2. This leaves maximum time for remaining activities")
    print("3. Optimal substructure: After picking activity i,")
    print("   solve remaining problem optimally")
    
    return selected
```

---

## 5. Fractional Knapsack

**Problem**: Given weights and values, fill knapsack to maximize value (can take fractions).

### Visual Explanation

```
  ITEMS:                          KNAPSACK (capacity = 50):
  ┌───────┬────────┬───────┬──────────────┐
  │ Item  │ Weight │ Value │ Value/Weight │     ┌────────────────────────┐
  ├───────┼────────┼───────┼──────────────┤     │                        │
  │   1   │   10   │   60  │    6.0       │     │  [10kg][20kg][20/30kg] │
  │   2   │   20   │  100  │    5.0       │     │  =========  =========  │
  │   3   │   30   │  120  │    4.0       │     │  Item 1   Item 2  ⅓ of │
  └───────┴────────┴───────┴──────────────┘     │  (full)  (full) Item 3│
                                                │                        │
  Sort by ratio (descending):                   └────────────────────────┘
  1. Item 1: ratio 6.0  → take all   (10kg)     Used: 10+20 = 30 kg
  2. Item 2: ratio 5.0  → take all   (20kg)     Remaining: 20 kg
  3. Item 3: ratio 4.0  → take ⅓     (10kg)     Used: 10 kg
  
  Total value = 60 + 100 + (120 × ⅓) = 60 + 100 + 40 = 200

  KEY INSIGHT: In fractional knapsack, always pick the item
  with the HIGHEST value-to-weight ratio first!
```

```python
def fractional_knapsack(weights, values, capacity):
    """
    Fractional knapsack - can take fractions of items.
    Returns maximum value achievable.
    """
    n = len(weights)
    
    # Calculate value-to-weight ratio
    items = [(values[i] / weights[i], weights[i], values[i]) for i in range(n)]
    
    # Sort by ratio in descending order
    items.sort(reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    
    for ratio, weight, value in items:
        if weight <= remaining_capacity:
            # Take whole item
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction of item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            break
    
    return total_value

# Example
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
print(fractional_knapsack(weights, values, capacity))
# Output: 240.0 (take all of item 1, all of item 2, and 2/3 of item 3)
```

### With Item Selection Details

```python
def fractional_knapsack_detailed(weights, values, capacity):
    """Fractional knapsack with detailed item selection."""
    n = len(weights)
    
    # Calculate value-to-weight ratio
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    
    # Sort by ratio in descending order
    items.sort(reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    selected = []
    
    for ratio, weight, value, idx in items:
        if weight <= remaining_capacity:
            selected.append((idx, weight, value, 1.0))
            total_value += value
            remaining_capacity -= weight
        else:
            fraction = remaining_capacity / weight
            selected.append((idx, remaining_capacity, value * fraction, fraction))
            total_value += value * fraction
            break
    
    print("Items selected:")
    for idx, wt, val, frac in selected:
        print(f"  Item {idx}: weight={wt:.1f}, value={val:.1f}, fraction={frac:.2f}")
    print(f"Total value: {total_value:.1f}")
    
    return total_value, selected

# Example
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
fractional_knapsack_detailed(weights, values, capacity)
```

---

## 6. Minimum Number of Coins

**Problem**: Find minimum number of coins to make a given amount.

### Visual Walkthrough (US Coins)

```
  Coins available: [25, 10, 5, 1]
  Amount to make: 41
  
  GREEDY APPROACH (pick largest coin that fits):
  ┌─────────────────────────────────────────────────────┐
  │  Amount = 41                                        │
  │                                                     │
  │  Step 1: 41 >= 25 → Pick $25   Remaining: 41-25=16 │
  │  Step 2: 16 >= 10 → Pick $10   Remaining: 16-10=6  │
  │  Step 3:  6 >= 5  → Pick $5    Remaining: 6-5=1    │
  │  Step 4:  1 >= 1  → Pick $1    Remaining: 1-1=0    │
  │                                                     │
  │  Coins used: [25, 10, 5, 1] = 4 coins              │
  └─────────────────────────────────────────────────────┘

  When greedy FAILS:
  ┌─────────────────────────────────────────────────────┐
  │  Coins: [1, 3, 4],  Amount: 6                       │
  │                                                     │
  │  Greedy: 4 + 1 + 1 = 3 coins                       │
  │  Optimal: 3 + 3 = 2 coins   ← BETTER!              │
  │                                                     │
  │  Greedy fails because coin system [1,3,4] is NOT    │
  │  canonical. US coins [1,5,10,25] ARE canonical.     │
  └─────────────────────────────────────────────────────┘
```

```python
def min_coins(coins, amount):
    """
    Find minimum coins to make amount.
    Note: Greedy works for US coins, not for all coin systems.
    """
    # Sort coins in descending order
    coins.sort(reverse=True)
    
    count = 0
    result = []
    
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
            result.append(coin)
    
    return count, result if amount == 0 else -1

# Example - works for standard US coins
coins = [25, 10, 5, 1]
amount = 41
count, result = min_coins(coins, amount)
print(f"Minimum coins: {count}")
print(f"Coins used: {result}")
# Output: Minimum coins: 4
# Coins used: [25, 10, 5, 1]
```

### DP Solution (Works for All Coin Systems)

```python
def min_coins_dp(coins, amount):
    """DP solution that works for all coin systems."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Example
coins = [1, 3, 4]
amount = 6
print(min_coins_dp(coins, amount))  # 2 (3 + 3, not 4 + 1 + 1)
# Note: Greedy would give 3 coins (4 + 1 + 1)
```

### Proof: When Greedy Works

```python
def greedy_works_for_coins(coins):
    """
    Check if greedy works for given coin system.
    Greedy works if coin system has the "canonical" property.
    """
    # Sort coins in descending order
    coins.sort(reverse=True)
    
    # For each amount, check if greedy gives optimal
    for amount in range(1, 100):
        # Greedy solution
        greedy_count = 0
        temp = amount
        for coin in coins:
            while temp >= coin:
                temp -= coin
                greedy_count += 1
        
        # DP solution
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        
        if greedy_count != dp[amount]:
            return False, amount
    
    return True, None

# Test with US coins
print(greedy_works_for_coins([25, 10, 5, 1]))  # (True, None)

# Test with non-canonical system
print(greedy_works_for_coins([1, 3, 4]))  # (False, 6)
```

---

## 7. Assign Cookies

**Problem**: Each child i has greed factor g[i], each cookie j has size s[j]. Maximize content children.

### Visual Explanation

```
  Children (sorted): [1, 2, 3]
  Cookies (sorted):  [1, 1]
  
  TWO-POINTER APPROACH:
  ┌────────────────────────────────────────────────────┐
  │  Child:  1   2   3                                 │
  │          ▲   ▲   ▲                                 │
  │          │   │   │                                 │
  │  Cookie: 1   1                                     │
  │          ▲   ▲                                     │
  │          │   │                                     │
  │  Step 1: Cookie[0]=1 >= Child[0]=1 → MATCH! ✓     │
  │          Both pointers advance                     │
  │  Step 2: Cookie[1]=1 < Child[1]=2 → Cookie too    │
  │          small, advance cookie pointer             │
  │  Step 3: No more cookies                           │
  │                                                    │
  │  Content children: 1                               │
  └────────────────────────────────────────────────────┘

  GREEDY INSIGHT: Always give the smallest cookie that
  satisfies a child. This preserves larger cookies for
  harder-to-please children.
```

```python
def find_content_children(children, cookies):
    """
    Find maximum content children.
    A child is content if cookie size >= greed factor.
    """
    children.sort()
    cookies.sort()
    
    child_idx = 0
    cookie_idx = 0
    content_children = 0
    
    while child_idx < len(children) and cookie_idx < len(cookies):
        if cookies[cookie_idx] >= children[child_idx]:
            # Child is content
            content_children += 1
            child_idx += 1
            cookie_idx += 1
        else:
            # Cookie too small, try next
            cookie_idx += 1
    
    return content_children

# Example
children = [1, 2, 3]
cookies = [1, 1]
print(find_content_children(children, cookies))  # 1

children = [1, 2]
cookies = [1, 2, 3]
print(find_content_children(children, cookies))  # 2
```

### Detailed Version

```python
def find_content_children_detailed(children, cookies):
    """Detailed version showing matching."""
    children_sorted = sorted(enumerate(children), key=lambda x: x[1])
    cookies_sorted = sorted(enumerate(cookies), key=lambda x: x[1])
    
    child_idx = 0
    cookie_idx = 0
    matches = []
    
    while child_idx < len(children) and cookie_idx < len(cookies):
        child_id, child_greed = children_sorted[child_idx]
        cookie_id, cookie_size = cookies_sorted[cookie_idx]
        
        if cookie_size >= child_greed:
            matches.append((child_id, cookie_id, cookie_size))
            child_idx += 1
            cookie_idx += 1
        else:
            cookie_idx += 1
    
    print("Matches:")
    for child_id, cookie_id, size in matches:
        print(f"  Child {child_id} (greed={children[child_id]}) <- Cookie {cookie_id} (size={size})")
    print(f"Content children: {len(matches)}")
    
    return len(matches)

# Example
children = [1, 2, 3, 4]
cookies = [1, 2, 3, 5]
find_content_children_detailed(children, cookies)
```

---

## 8. Lemonade Change

**Problem**: Customers pay with $5, $10, $20 bills. Start with no change. Can you give change to all customers?

### Visual Walkthrough

```
  Lemonade costs $5. Customers pay with $5, $10, $20.
  Start with empty register.

  bills = [5, 5, 5, 10, 20]

  ┌──────────┬────────┬───────────────┬──────────────────────┐
  │ Customer │  Bill  │ Change Given  │ Register After       │
  ├──────────┼────────┼───────────────┼──────────────────────┤
  │    1     │   $5   │ None          │ {$5: 1}              │
  │    2     │   $5   │ None          │ {$5: 2}              │
  │    3     │   $5   │ None          │ {$5: 3}              │
  │    4     │  $10   │ Give $5       │ {$5: 2, $10: 1}     │
  │    5     │  $20   │ Give $10 + $5 │ {$5: 1, $10: 0}     │
  └──────────┴────────┴───────────────┴──────────────────────┘

  GREEDY STRATEGY for $20 bill change:
  Prefer to give $10 + $5 (preserves more $5 bills)
  If not possible, give $5 + $5 + $5
  If neither possible, return False

  Why prefer $10+$5 over $5+$5+$5?
  Because $10 bills are LESS useful for change ($10 can only
  give change for $10 payments, while $5 bills are needed
  for both $10 and $20 change).
```

```python
def lemonade_change(bills):
    """
    Determine if you can give change to all customers.
    Each lemonade costs $5.
    """
    five = 0
    ten = 0
    
    for bill in bills:
        if bill == 5:
            five += 1
        elif bill == 10:
            if five == 0:
                return False
            five -= 1
            ten += 1
        else:  # bill == 20
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    
    return True

# Example
bills = [5, 5, 5, 10, 20]
print(lemonade_change(bills))  # True

bills = [5, 5, 10, 10, 20]
print(lemonade_change(bills))  # False
```

### Detailed Version

```python
def lemonade_change_detailed(bills):
    """Detailed version showing change given."""
    five = 0
    ten = 0
    change_history = []
    
    for i, bill in enumerate(bills):
        change_given = []
        
        if bill == 5:
            five += 1
            change_given.append("No change needed")
        elif bill == 10:
            if five == 0:
                print(f"Cannot give change for customer {i+1} (bill=$10)")
                return False, []
            five -= 1
            ten += 1
            change_given.append("Give $5")
        else:  # bill == 20
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
                change_given.append("Give $10 + $5")
            elif five >= 3:
                five -= 3
                change_given.append("Give $5 + $5 + $5")
            else:
                print(f"Cannot give change for customer {i+1} (bill=$20)")
                return False, []
        
        change_history.append({
            'customer': i + 1,
            'bill': bill,
            'change': change_given,
            'balance': {'$5': five, '$10': ten}
        })
    
    print("Transaction history:")
    for record in change_history:
        print(f"  Customer {record['customer']}: Paid ${record['bill']}, "
              f"{' -> '.join(record['change'])}, "
              f"Balance: {record['balance']}")
    
    return True, change_history

# Example
bills = [5, 5, 5, 10, 20]
success, history = lemonade_change_detailed(bills)
print(f"Success: {success}")
```

---

## Quick Reference: Greedy Patterns

| Pattern | Key Idea | Example |
|---------|----------|---------|
| Sort by criterion | Choose best at each step | Activity selection |
| Priority queue | Process most important first | Task scheduling |
| Two pointers | Match from both ends | Assign cookies |
| Mathematical | Prove local = global | Fractional knapsack |

### When to Use Each Pattern (Visual Guide)

```
  ┌─────────────────────────────────────────────────────────────┐
  │              GREEDY PATTERN DECISION GUIDE                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  Problem has intervals/times?                               │
  │    YES → Sort by finish time (Activity Selection)           │
  │                                                             │
  │  Problem has items with ratios?                             │
  │    YES → Sort by ratio (Fractional Knapsack)                │
  │                                                             │
  │  Problem has two sorted sequences to match?                 │
  │    YES → Two pointers (Assign Cookies)                      │
  │                                                             │
  │  Problem needs "best item at each step"?                    │
  │    YES → Priority queue (Task Scheduling, Huffman)          │
  │                                                             │
  │  Problem needs minimum coins/change?                        │
  │    YES → Pick largest denomination (Coin Change)            │
  │    WARNING: Only works for canonical coin systems!          │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

---

## Common Pitfalls

```
  ╔══════════════════════════════════════════════════════════════╗
  ║                  TOP 5 GREEDY MISTAKES                       ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                              ║
  ║  1. NOT PROVING GREEDY CHOICE PROPERTY                       ║
  ║     → Always verify: does local optimum = global optimum?    ║
  ║     → Use exchange argument if unsure                        ║
  ║                                                              ║
  ║  2. USING GREEDY FOR 0/1 KNAPSACK                            ║
  ║     → Greedy by ratio gives suboptimal result                ║
  ║     → Use DP for 0/1 knapsack instead                        ║
  ║                                                              ║
  ║  3. COIN CHANGE WITH NON-CANONICAL SYSTEMS                   ║
  ║     → Greedy works for [1,5,10,25] but not [1,3,4]          ║
  ║     → When in doubt, use DP for coin change                  ║
  ║                                                              ║
  ║  4. OFF-BY-ONE ERRORS                                        ║
  ║     → Careful with >= vs > in overlap checks                 ║
  ║     → Activity: start >= last_finish (not >)                 ║
  ║                                                              ║
  ║  5. NOT HANDLING EDGE CASES                                  ║
  ║     → Empty input, single element, all same values           ║
  ║     → Always check: if not activities: return []             ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝
```

---

## Complexity Analysis

| Problem | Time | Space | Sorting Step |
|---------|------|-------|-------------|
| Activity Selection | O(n log n) | O(1) | Sort by finish time |
| Fractional Knapsack | O(n log n) | O(1) | Sort by value/weight ratio |
| Min Coins (Greedy) | O(n × amount) | O(1) | Sort coins descending |
| Assign Cookies | O(n log n) | O(1) | Sort both arrays |
| Lemonade Change | O(n) | O(1) | No sorting needed |
