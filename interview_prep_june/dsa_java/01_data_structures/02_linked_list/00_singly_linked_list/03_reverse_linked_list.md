# Reverse Linked List

Reversing a linked list is one of the most fundamental operations. There are multiple approaches, each with different trade-offs.

---

## 1. Iterative Reverse

**The Classic Approach — O(n) time, O(1) space**

We maintain three pointers: `prev`, `curr`, and `next`. At each step, we reverse the current node's pointer.

```java
public Node reverseIterative(Node head) {
    Node prev = null;
    Node curr = head;

    while (curr != null) {
        Node next = curr.next; // save next before we break the link
        curr.next = prev;      // reverse the pointer
        prev = curr;           // advance prev
        curr = next;           // advance curr
    }

    return prev; // prev is the new head
}
```

### Step-by-Step Walkthrough: `1 -> 2 -> 3 -> null`

| Step | prev | curr | next | Action | List State |
|------|------|------|------|--------|------------|
| start | null | 1 | 2 | | `1 -> 2 -> 3` |
| 1 | null | 1 | 2 | 1.next = null | `1 -> null`, `2 -> 3` |
| 2 | 1 | 2 | 3 | 2.next = 1 | `2 -> 1 -> null`, `3` |
| 3 | 2 | 3 | null | 3.next = 2 | `3 -> 2 -> 1 -> null` |
| end | 3 | null | — | curr is null, return prev | `3 -> 2 -> 1 -> null` ✓ |

### Visualizing the Three Pointers

```
Start:    null    1 -> 2 -> 3 -> null
          prev  curr

Step 1:   null <- 1    2 -> 3 -> null
                prev curr

Step 2:   null <- 1 <- 2    3 -> null
                     prev curr

Step 3:   null <- 1 <- 2 <- 3    null
                          prev  curr (null → stop)
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 2. Recursive Reverse

Elegant, but uses O(n) stack space.

```java
public Node reverseRecursive(Node head) {
    // Base case: empty list or single node
    if (head == null || head.next == null) {
        return head;
    }

    // Recurse to the end
    Node newHead = reverseRecursive(head.next);

    // Reverse the link: make the next node point back to us
    head.next.next = head;
    head.next = null; // cut the old forward link

    return newHead; // always return the same newHead (the original last node)
}
```

### Walkthrough: `1 -> 2 -> 3 -> null`

**Reaching the base case:**
```
reverse(1) → reverse(2) → reverse(3) → returns 3 (base case)
```

**Unwinding the stack:**

| Call returns to | head | head.next | head.next.next | Action | List state |
|----------------|------|-----------|----------------|--------|------------|
| reverse(2) | 2 | 3 | — | 3.next = 2, 2.next = null | `1 -> 2 <- 3` |
| reverse(1) | 1 | 2 | — | 2.next = 1, 1.next = null | `1 <- 2 <- 3` |

Result: `3 -> 2 -> 1 -> null` ✓

### Why does this work?

1. We recurse all the way to the last node — this becomes the new head
2. On the way back, each node makes its `next` node point back to itself
3. Each node then severs its own forward link (`head.next = null`)
4. The new head is passed back through all recursive calls

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n)  | (recursion stack) |

---

## 3. Reverse in Groups of K

**Problem:** Reverse every k nodes in the list. If the remaining nodes are fewer than k, reverse them too.

**Example:** `1 -> 2 -> 3 -> 4 -> 5`, k=2 → `2 -> 1 -> 4 -> 3 -> 5`

```java
public Node reverseInGroups(Node head, int k) {
    // Check if we have at least k nodes to reverse
    Node check = head;
    for (int i = 0; i < k; i++) {
        if (check == null) return head; // fewer than k remaining, keep as-is
        check = check.next;
    }

    // Reverse k nodes
    Node prev = null;
    Node curr = head;
    for (int i = 0; i < k; i++) {
        Node next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }

    // head is now the tail of this reversed group
    // curr is the start of the next group
    head.next = reverseInGroups(curr, k);

    return prev; // new head of this group
}
```

### Walkthrough: `1 -> 2 -> 3 -> 4 -> 5`, k=2

**First group:**
- Reverse `1 -> 2` → `2 -> 1`
- `head` (1) is now the tail, connect to result of reversing rest

**Second group:**
- Reverse `3 -> 4` → `4 -> 3`
- `head` (3) is now the tail, connect to result

**Third group:**
- Only `5` remains (less than k=2), return as-is

Result: `2 -> 1 -> 4 -> 3 -> 5` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n/k) | (recursion depth = number of groups) |

---

## 4. Reverse Between Positions m and n

**Problem:** Reverse nodes from position m to position n (1-indexed). Do it in one pass.

**Example:** `1 -> 2 -> 3 -> 4 -> 5`, m=2, n=4 → `1 -> 4 -> 3 -> 2 -> 5`

```java
public Node reverseBetween(Node head, int m, int n) {
    if (head == null || m == n) return head;

    Node dummy = new Node(0);
    dummy.next = head;
    Node prev = dummy;

    // Move prev to the node just before position m
    for (int i = 1; i < m; i++) {
        prev = prev.next;
    }

    // curr is at position m
    Node curr = prev.next;

    // Standard reversal, but only n - m + 1 times
    for (int i = 0; i < n - m; i++) {
        Node next = curr.next;
        curr.next = next.next;
        next.next = prev.next;
        prev.next = next;
    }

    return dummy.next;
}
```

### Walkthrough: `1 -> 2 -> 3 -> 4 -> 5`, m=2, n=4

**Setup:** prev = dummy (before 1), curr = 1

After loop `for (int i = 1; i < 2; i++)`: prev = node 1, curr = node 2

**Reversal steps (i = 0 to 2):**

| i | next | Action |
|---|------|--------|
| 0 | 3 | Move 3 to front: `1 -> 3 -> 2 -> 4 -> 5` |
| 1 | 4 | Move 4 to front: `1 -> 4 -> 3 -> 2 -> 5` |

Result: `1 -> 4 -> 3 -> 2 -> 5` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 5. Check if Linked List is Palindrome

**Problem:** Determine if a linked list is a palindrome.

**Example:** `1 -> 2 -> 2 -> 1` → true, `1 -> 2 -> 3 -> 1` → false

### Approach: Fast/Slow to Middle, Reverse Second Half, Compare

```java
public boolean isPalindrome(Node head) {
    if (head == null || head.next == null) return true;

    // Step 1: Find the middle using slow/fast pointers
    Node slow = head;
    Node fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    // Step 2: Reverse the second half
    Node secondHalf = reverseIterative(slow.next);
    slow.next = null; // break the list at middle

    // Step 3: Compare both halves
    Node firstHalf = head;
    Node secondPtr = secondHalf;
    boolean isPalin = true;

    while (secondPtr != null) {
        if (firstHalf.data != secondPtr.data) {
            isPalin = false;
            break;
        }
        firstHalf = firstHalf.next;
        secondPtr = secondPtr.next;
    }

    // Step 4: Restore the list (optional but good practice)
    slow.next = reverseIterative(secondHalf);

    return isPalin;
}
```

### Walkthrough: `1 -> 2 -> 3 -> 2 -> 1`

| Step | Action | State |
|------|--------|-------|
| 1 | Find middle | slow at 3 |
| 2 | Reverse after middle | `1 -> 2 -> 3` and `1 -> 2` (reversed) |
| 3 | Compare | 1==1 ✓, 2==2 ✓ → palindrome! |
| 4 | Restore | `1 -> 2 -> 3 -> 2 -> 1` |

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  | (in-place, no extra data structures) |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Iterative reverse
    Node list1 = buildList(new int[]{1, 2, 3, 4, 5});
    list1 = reverseIterative(list1);
    display(list1); // 5 -> 4 -> 3 -> 2 -> 1

    // Test 2: Recursive reverse
    Node list2 = buildList(new int[]{1, 2, 3});
    list2 = reverseRecursive(list2);
    display(list2); // 3 -> 2 -> 1

    // Test 3: Reverse in groups of K
    Node list3 = buildList(new int[]{1, 2, 3, 4, 5});
    list3 = reverseInGroups(list3, 2);
    display(list3); // 2 -> 1 -> 4 -> 3 -> 5

    Node list3b = buildList(new int[]{1, 2, 3, 4, 5, 6, 7});
    list3b = reverseInGroups(list3b, 3);
    display(list3b); // 3 -> 2 -> 1 -> 6 -> 5 -> 4 -> 7

    // Test 4: Reverse between m and n
    Node list4 = buildList(new int[]{1, 2, 3, 4, 5});
    list4 = reverseBetween(list4, 2, 4);
    display(list4); // 1 -> 4 -> 3 -> 2 -> 5

    // Test 5: Palindrome check
    System.out.println(isPalindrome(buildList(new int[]{1, 2, 2, 1}))); // true
    System.out.println(isPalindrome(buildList(new int[]{1, 2, 3, 2, 1}))); // true
    System.out.println(isPalindrome(buildList(new int[]{1, 2, 3}))); // false
    System.out.println(isPalindrome(buildList(new int[]{1}))); // true
    System.out.println(isPalindrome(null)); // true
}
```

---

## Summary

| Variant | Time | Space | Key Insight |
|---------|------|-------|-------------|
| Iterative reverse | O(n) | O(1) | Three pointers: prev, curr, next |
| Recursive reverse | O(n) | O(n) | `head.next.next = head; head.next = null` |
| Reverse in groups of K | O(n) | O(n/k) | Reverse k nodes, recurse on rest |
| Reverse between m and n | O(n) | O(1) | Dummy head + standard reversal |
| Palindrome check | O(n) | O(1) | Reverse second half in-place |
