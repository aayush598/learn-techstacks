# Merge and Sort — Singly Linked List

These operations are where linked lists really shine. Merging sorted lists and sorting linked lists are classic interview problems.

---

## 1. Merge Two Sorted Linked Lists

**Problem:** Merge two sorted linked lists into one sorted list.

**Example:** `1 -> 3 -> 5` and `2 -> 4 -> 6` → `1 -> 2 -> 3 -> 4 -> 5 -> 6`

### Iterative Approach (Dummy Node)

```java
public Node mergeTwoSorted(Node l1, Node l2) {
    Node dummy = new Node(0); // sentinel to simplify edge cases
    Node current = dummy;

    while (l1 != null && l2 != null) {
        if (l1.data <= l2.data) {
            current.next = l1;
            l1 = l1.next;
        } else {
            current.next = l2;
            l2 = l2.next;
        }
        current = current.next;
    }

    // Attach remaining nodes
    current.next = (l1 != null) ? l1 : l2;

    return dummy.next; // skip the sentinel
}
```

**Why the dummy node?** Without it, we'd need a separate check for which list contributes the first node. The dummy node eliminates this special case entirely.

### Walkthrough

| Step | l1 | l2 | current.next | Action |
|------|-----|-----|-------------|--------|
| 1 | 1 | 2 | 1 (l1) | l1 advances |
| 2 | 3 | 2 | 2 (l2) | l2 advances |
| 3 | 3 | 4 | 3 (l1) | l1 advances |
| 4 | 5 | 4 | 4 (l2) | l2 advances |
| 5 | 5 | 6 | 5 (l1) | l1 advances |
| 6 | null | 6 | 6 (l2) | l2 exhausted |

Result: `dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> 6`

### Recursive Approach

```java
public Node mergeTwoSortedRecursive(Node l1, Node l2) {
    if (l1 == null) return l2;
    if (l2 == null) return l1;

    if (l1.data <= l2.data) {
        l1.next = mergeTwoSortedRecursive(l1.next, l2);
        return l1;
    } else {
        l2.next = mergeTwoSortedRecursive(l1, l2.next);
        return l2;
    }
}
```

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| Iterative | O(n + m) | O(1) |
| Recursive | O(n + m) | O(n + m) (stack) |

---

## 2. Merge K Sorted Lists

**Problem:** Merge k sorted linked lists into one sorted list.

**Example:** `[1->4->5, 1->3->4, 2->6]` → `1->1->2->3->4->4->5->6`

### Approach: PriorityQueue (Min-Heap)

```java
public Node mergeKLists(Node[] lists) {
    // Min-heap based on node value
    PriorityQueue<Node> pq = new PriorityQueue<>((a, b) -> a.data - b.data);

    // Add the head of each non-empty list
    for (Node node : lists) {
        if (node != null) {
            pq.offer(node);
        }
    }

    Node dummy = new Node(0);
    Node current = dummy;

    while (!pq.isEmpty()) {
        Node min = pq.poll();
        current.next = min;
        current = current.next;

        if (min.next != null) {
            pq.offer(min.next);
        }
    }

    return dummy.next;
}
```

**Walkthrough with `[1->4->5, 1->3->4, 2->6]`:**

| Step | PQ (min on left) | Poll | Add next |
|------|------------------|------|----------|
| start | [1, 1, 2] | — | — |
| 1 | [1, 2, 4] | 1 (list1) | 4 |
| 2 | [2, 4, 4] | 1 (list2) | 3 |
| 3 | [3, 4, 4] | 2 (list3) | 6 |
| 4 | [4, 4, 6] | 3 (list2) | 4 |
| 5 | [4, 4, 6] | 4 (list1) | 5 |
| 6 | [4, 5, 6] | 4 (list2) | null |
| 7 | [5, 6] | 5 (list1) | null |
| 8 | [6] | 6 (list3) | null |

Result: `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6` ✓

### Alternative: Divide and Conquer

```java
public Node mergeKListsDivideConquer(Node[] lists) {
    if (lists.length == 0) return null;
    return divide(lists, 0, lists.length - 1);
}

private Node divide(Node[] lists, int left, int right) {
    if (left == right) return lists[left];
    if (left > right) return null;

    int mid = left + (right - left) / 2;
    Node l = divide(lists, left, mid);
    Node r = divide(lists, mid + 1, right);
    return mergeTwoSorted(l, r);
}
```

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| PriorityQueue | O(N log k) | O(k) |
| Divide & Conquer | O(N log k) | O(log k) |

Where N = total nodes, k = number of lists.

---

## 3. Sort Linked List — Merge Sort

**Problem:** Sort a linked list in O(n log n) time.

**Why merge sort?** Unlike quicksort, merge sort doesn't need random access, making it ideal for linked lists.

```java
public Node sortList(Node head) {
    if (head == null || head.next == null) return head;

    // Step 1: Find the middle
    Node mid = getMid(head);

    // Step 2: Split into two halves
    Node rightHead = mid.next;
    mid.next = null; // break the list

    // Step 3: Recursively sort both halves
    Node left = sortList(head);
    Node right = sortList(rightHead);

    // Step 4: Merge sorted halves
    return mergeTwoSorted(left, right);
}

private Node getMid(Node head) {
    Node slow = head;
    Node fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n log n) |
| Space  | O(log n) | (recursion stack) |

---

## 4. Add Two Numbers

**Problem:** Each list represents a number in reverse order. Add them and return the sum as a linked list.

**Example:** `(2 -> 4 -> 3) + (5 -> 6 -> 4)` → `7 -> 0 -> 8` (342 + 465 = 807)

```java
public Node addTwoNumbers(Node l1, Node l2) {
    Node dummy = new Node(0);
    Node current = dummy;
    int carry = 0;

    while (l1 != null || l2 != null || carry != 0) {
        int sum = carry;

        if (l1 != null) {
            sum += l1.data;
            l1 = l1.next;
        }
        if (l2 != null) {
            sum += l2.data;
            l2 = l2.next;
        }

        carry = sum / 10;
        current.next = new Node(sum % 10);
        current = current.next;
    }

    return dummy.next;
}
```

**Walkthrough: `(2 -> 4 -> 3) + (5 -> 6 -> 4)`**

| Step | l1 | l2 | sum | carry | digit |
|------|-----|-----|-----|-------|-------|
| 1 | 2 | 5 | 7 | 0 | 7 |
| 2 | 4 | 6 | 10 | 1 | 0 |
| 3 | 3 | 4 | 8 | 0 | 8 |

Result: `7 -> 0 -> 8` ✓

**Key detail:** The loop continues while `carry != 0` even after both lists are exhausted. This handles cases like `(9 -> 9) + (1)` = `0 -> 0 -> 1`.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(max(n, m)) |
| Space  | O(max(n, m)) |

---

## 5. Intersection and Union of Two Lists

### Intersection (elements in both lists)

```java
public Node intersection(Node l1, Node l2) {
    Set<Integer> set = new HashSet<>();
    Node result = null;
    Node tail = null;

    // Add all elements of l1 to set
    Node curr = l1;
    while (curr != null) {
        set.add(curr.data);
        curr = curr.next;
    }

    // Check l2 elements against set
    curr = l2;
    while (curr != null) {
        if (set.contains(curr.data)) {
            Node newNode = new Node(curr.data);
            if (result == null) {
                result = tail = newNode;
            } else {
                tail.next = newNode;
                tail = newNode;
            }
            // Remove to avoid duplicates in result
            set.remove(curr.data);
        }
        curr = curr.next;
    }

    return result;
}
```

### Union (all unique elements from both lists)

```java
public Node union(Node l1, Node l2) {
    Set<Integer> set = new LinkedHashSet<>(); // preserves insertion order

    Node curr = l1;
    while (curr != null) {
        set.add(curr.data);
        curr = curr.next;
    }

    curr = l2;
    while (curr != null) {
        set.add(curr.data);
        curr = curr.next;
    }

    Node result = null;
    Node tail = null;
    for (int val : set) {
        Node newNode = new Node(val);
        if (result == null) {
            result = tail = newNode;
        } else {
            tail.next = newNode;
            tail = newNode;
        }
    }

    return result;
}
```

### Complexity (Intersection & Union)

| Metric | Value |
|--------|-------|
| Time   | O(n + m) |
| Space  | O(n) |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Merge two sorted lists
    Node l1 = buildList(new int[]{1, 3, 5});
    Node l2 = buildList(new int[]{2, 4, 6});
    display(mergeTwoSorted(l1, l2)); // 1 -> 2 -> 3 -> 4 -> 5 -> 6

    // Test 2: Merge K sorted lists
    Node[] lists = {
        buildList(new int[]{1, 4, 5}),
        buildList(new int[]{1, 3, 4}),
        buildList(new int[]{2, 6})
    };
    display(mergeKLists(lists)); // 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6

    // Test 3: Sort linked list
    Node unsorted = buildList(new int[]{4, 2, 1, 3});
    display(sortList(unsorted)); // 1 -> 2 -> 3 -> 4

    // Test 4: Add two numbers
    Node num1 = buildList(new int[]{2, 4, 3}); // represents 342
    Node num2 = buildList(new int[]{5, 6, 4}); // represents 465
    display(addTwoNumbers(num1, num2)); // 7 -> 0 -> 8 (represents 807)

    // Edge case: different lengths
    Node num3 = buildList(new int[]{9, 9}); // 99
    Node num4 = buildList(new int[]{1});    // 1
    display(addTwoNumbers(num3, num4)); // 0 -> 0 -> 1 (100)

    // Test 5: Intersection and Union
    Node a = buildList(new int[]{1, 2, 3, 4});
    Node b = buildList(new int[]{3, 4, 5, 6});
    System.out.print("Intersection: ");
    display(intersection(a, b)); // 3 -> 4
    System.out.print("Union: ");
    display(union(a, b)); // 1 -> 2 -> 3 -> 4 -> 5 -> 6
}
```

---

## When to Use What

| Problem | Best Approach | Why |
|---------|--------------|-----|
| Merge 2 sorted lists | Dummy node + compare | O(n+m) time, O(1) space |
| Merge K sorted lists | Min-heap or divide & conquer | O(N log k) time |
| Sort linked list | Merge sort | O(n log n), doesn't need random access |
| Add numbers | Carry + dummy node | Natural carry propagation |
| Intersection/Union | HashSet | O(n+m) time, handles duplicates |
