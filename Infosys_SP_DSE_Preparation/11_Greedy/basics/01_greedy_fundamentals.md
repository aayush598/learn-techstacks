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

### Core Principles

```python
# Greedy Algorithm Template
def greedy_algorithm(input):
    # 1. Sort/organize by greedy criterion
    sorted_input = sort_by_criterion(input)
    
    # 2. Initialize result
    result = initial_value
    
    # 3. Process items one by one
    for item in sorted_input:
        if can_add(item, result):
            result = update_result(item, result)
    
    return result
```

### Key Properties

1. **Greedy Choice Property**: A globally optimal solution can be arrived at by making locally optimal choices
2. **Optimal Substructure**: An optimal solution to the problem contains optimal solutions to subproblems

---

## 2. When to Use Greedy

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

| Pattern | Example |
|---------|---------|
| Sorting by criterion | Activity selection |
| Priority queue | Task scheduling |
| Two pointers | Two sum sorted |
| Mathematical proof | Fractional knapsack |

### Greedy Doesn't Work When

```python
# 1. Local optimum ≠ Global optimum
#    Example: 0/1 Knapsack (need DP)

# 2. Choices affect future choices
#    Example: Matrix chain multiplication

# 3. Need to consider all combinations
#    Example: Traveling salesman
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

---

## 4. Activity Selection Problem

**Problem**: Select maximum number of non-overlapping activities.

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

---

## Common Pitfalls

1. **Not proving greedy choice property** - always verify local optimum leads to global
2. **Greedy doesn't work for 0/1 knapsack** - need DP
3. **Coin change** - greedy fails for non-canonical coin systems
4. **Missing edge cases** - empty input, single element
5. **Off-by-one errors** - careful with boundary conditions
