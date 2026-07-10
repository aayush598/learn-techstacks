# Fast & Slow Pointers (Floyd's Algorithm)

The two-pointer technique is the Swiss Army knife of linked list problems. Learn these patterns and you'll solve most linked list challenges.

---

## 1. Floyd's Cycle Detection — Has Cycle

**Problem:** Determine if a linked list has a cycle.

**How it works:** A "tortoise and hare" approach. If there's a cycle, the fast pointer will eventually meet the slow pointer inside the cycle.

```java
public boolean hasCycle(Node head) {
    Node slow = head;
    Node fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;          // moves 1 step
        fast = fast.next.next;     // moves 2 steps

        if (slow == fast) {        // they met — cycle exists!
            return true;
        }
    }

    return false; // fast reached end — no cycle
}
```

**Why does this work?**
- If no cycle: `fast` reaches `null` in at most n/2 steps
- If cycle: once both pointers enter the cycle, `fast` closes the gap by 1 node per step. They must meet within at most `cycle_length` steps after both enter the cycle.

### Walkthrough: `1 -> 2 -> 3 -> 4 -> 2` (cycle back to 2)

| Step | slow | fast |
|------|------|------|
| start | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | 2 |
| 3 | 4 | 4 |
| 4 | 2 | 2 | → slow == fast → cycle! |

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 2. Find the Cycle Start Node

**Problem:** If a cycle exists, find the node where it begins.

**Example:** `1 -> 2 -> 3 -> 4 -> 2` → cycle starts at node 2

### Approach: Head + Meet Point

After slow and fast meet, reset one pointer to head and move both at the same speed. They meet at the cycle start.

```java
public Node detectCycleStart(Node head) {
    Node slow = head;
    Node fast = head;

    // Phase 1: Detect if cycle exists
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;

        if (slow == fast) {
            // Phase 2: Find the start
            Node start = head;
            while (start != slow) {
                start = start.next;
                slow = slow.next;
            }
            return start; // both meet at cycle start
        }
    }

    return null; // no cycle
}
```

### Mathematical Proof

Let:
- `F` = distance from head to cycle start
- `a` = distance from cycle start to meeting point
- `c` = cycle length

When they meet:
- Slow traveled: `F + a`
- Fast traveled: `F + a + n*c` (fast has gone around n times)

Since fast moves twice as fast: `2(F + a) = F + a + n*c`
→ `F + a = n*c`
→ `F = n*c - a`
→ `F = (n-1)*c + (c - a)`

So walking `F` steps from head = same as walking `c - a` steps from meeting point (which wraps around the cycle to the start).

### Walkthrough: `1 -> 2 -> 3 -> 4 -> 2`

- F = 1 (head to node 2)
- a = 2 (node 2 to meeting point node 4)
- c = 3 (cycle: 2 → 3 → 4 → 2)

After meeting at node 4:
- start at head (node 1), slow at node 4
- Step 1: start → node 2, slow → node 2 → MATCH! ✓

---

## 3. Remove the Cycle

**Problem:** Detect and remove the cycle, restoring the list to a linear structure.

```java
public Node removeCycle(Node head) {
    Node slow = head;
    Node fast = head;

    // Phase 1: Detect cycle
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;

        if (slow == fast) {
            // Phase 2: Find the start
            Node start = head;
            while (start != slow.next) {
                start = start.next;
                slow = slow.next;
            }
            // Break the cycle
            slow.next = null;
            return head;
        }
    }

    return head; // no cycle
}
```

**Key difference from finding start:** We stop one step earlier. Instead of comparing `start != slow`, we compare `start != slow.next`. When they meet, `slow` is the last node in the cycle, and we set `slow.next = null`.

---

## 4. Find Middle of Linked List

Already covered in traversal, but here's the pattern reinforced:

```java
public Node findMiddle(Node head) {
    Node slow = head;
    Node fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    return slow; // for even-length, returns the second middle
}
```

**Why this works:** `fast` covers distance twice as fast as `slow`. When `fast` reaches the end, `slow` is exactly at the midpoint.

| List Length | Middle Position (slow) |
|-------------|----------------------|
| 1 | node 1 |
| 3 | node 2 |
| 5 | node 3 |
| 7 | node 4 |
| 2 | node 2 (second middle) |
| 4 | node 3 (second middle) |

---

## 5. Happy Number

**Problem:** Determine if a number is happy. A happy number eventually reaches 1 when replaced by the sum of squares of its digits. Non-happy numbers enter a cycle.

**Example:** 19 → 1²+9² = 82 → 8²+2² = 68 → ... → 1 (happy!)

**Key insight:** This is a linked list cycle problem in disguise! The sequence of numbers forms a linked list, and we need to detect a cycle.

```java
public boolean isHappy(int n) {
    int slow = n;
    int fast = n;

    do {
        slow = squareSum(slow);          // move 1 step
        fast = squareSum(squareSum(fast)); // move 2 steps
    } while (slow != fast);

    return slow == 1; // if they meet at 1, it's happy
}

private int squareSum(int n) {
    int sum = 0;
    while (n > 0) {
        int digit = n % 10;
        sum += digit * digit;
        n /= 10;
    }
    return sum;
}
```

**Walkthrough for n=19:**

| Step | slow | fast |
|------|------|------|
| start | 19 | 19 |
| 1 | 82 | 68 |
| 2 | 68 | 89 |
| 3 | 100 | 145 |
| 4 | 1 | 42 |
| 5 | 1 | 4 | → slow == fast → return slow == 1 → true ✓ |

**Walkthrough for n=2 (unhappy):**

The sequence 2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle!). They'll meet at some point in the cycle, and the value won't be 1.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(log n) per step (digit count) |
| Space  | O(1) |

---

## 6. Intersection of Two Linked Lists

**Problem:** Find the node where two linked lists intersect. If they don't intersect, return null.

**Example:**
```
A1 -> a2 -> c1 -> c2 -> c3
B1 -> b2 -> b3 -> c1 -> c2 -> c3
```
Intersection at node c1.

### Approach 1: Count Difference + Align

```java
public Node getIntersectionNode(Node headA, Node headB) {
    int lenA = length(headA);
    int lenB = length(headB);

    // Advance the longer list by the difference
    while (lenA > lenB) {
        headA = headA.next;
        lenA--;
    }
    while (lenB > lenA) {
        headB = headB.next;
        lenB--;
    }

    // Move both until they meet
    while (headA != headB) {
        headA = headA.next;
        headB = headB.next;
    }

    return headA; // null if no intersection
}

private int length(Node head) {
    int len = 0;
    while (head != null) {
        len++;
        head = head.next;
    }
    return len;
}
```

**Walkthrough:**
- lenA = 5, lenB = 6 → advance B by 1 → B at b2
- Both walk: A at a2, B at b3 → A at c1, B at c1 → intersection!

### Approach 2: Two Pointers (No Length Calculation)

```java
public Node getIntersectionNodeTwoPointer(Node headA, Node headB) {
    Node a = headA;
    Node b = headB;

    while (a != b) {
        a = (a == null) ? headB : a.next;
        b = (b == null) ? headA : b.next;
    }

    return a;
}
```

**Why this works:**
- Both pointers travel `lenA + lenB` total distance
- If there's an intersection, they meet at the intersection node
- If there's no intersection, they both become `null` at the same time

**Proof:** Pointer A travels `lenA` then switches to list B and travels `lenB`. Pointer B travels `lenB` then switches to list A and travels `lenA`. Both travel the same total distance, so if they meet, it must be at the intersection.

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Cycle detection — no cycle
    Node list1 = buildList(new int[]{1, 2, 3, 4, 5});
    System.out.println(hasCycle(list1)); // false

    // Test 2: Cycle detection — has cycle
    Node list2 = buildList(new int[]{1, 2, 3, 4, 5});
    list2.next.next.next.next.next = list2.next; // 5 -> 2
    System.out.println(hasCycle(list2)); // true

    // Test 3: Find cycle start
    System.out.println(detectCycleStart(list2).data); // 2

    // Test 4: Remove cycle
    removeCycle(list2);
    System.out.println(hasCycle(list2)); // false
    display(list2); // 1 -> 2 -> 3 -> 4 -> 5

    // Test 5: Middle
    System.out.println(findMiddle(buildList(new int[]{1, 2, 3, 4, 5})).data); // 3
    System.out.println(findMiddle(buildList(new int[]{1, 2, 3, 4})).data);    // 3

    // Test 6: Happy number
    System.out.println(isHappy(19));  // true
    System.out.println(isHappy(2));   // false
    System.out.println(isHappy(7));   // true

    // Test 7: Intersection
    Node common = new Node(8);
    common.next = new Node(4);
    common.next.next = new Node(5);

    Node headA = new Node(4);
    headA.next = new Node(1);
    headA.next.next = common;

    Node headB = new Node(5);
    headB.next = new Node(6);
    headB.next.next = new Node(1);
    headB.next.next.next = common;

    Node intersection = getIntersectionNode(headA, headB);
    System.out.println(intersection != null ? intersection.data : "No intersection"); // 8
}
```

---

## Pattern Summary

| Pattern | Problem Type | Key Insight |
|---------|-------------|-------------|
| Slow/Fast meet | Cycle detection | Fast catches slow in cycle |
| Head + Meet point | Cycle start | F = n*c - a (math proof) |
| Slow/Fast at 2x speed | Middle | Fast reaches end → slow at middle |
| Value as next pointer | Happy number | Cycle in number sequence |
| Length difference | Intersection | Align, then walk together |
| Two pointers swap heads | Intersection | Both travel lenA + lenB total |

---

## When to Use Fast/Slow Pointers

- Detect cycles in linked lists
- Find the middle of a linked list
- Problems that involve "repeated" states (like Happy Number)
- Finding intersection points
- Any problem where you need to know if a structure has a loop

**Advantage over HashSet:** O(1) space instead of O(n). The trade-off is that it only finds YES/NO cycle existence — if you need to find all nodes in the cycle, use a HashSet.
