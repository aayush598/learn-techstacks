# Traversal and Search — Singly Linked List

Mastering traversal patterns is essential. Most linked list problems are solved by walking the list in clever ways.

---

## 1. Iterative Traversal

The fundamental pattern. You'll use this in almost every linked list problem.

```java
public void traverse(Node head) {
    Node current = head;
    while (current != null) {
        System.out.print(current.data + " ");
        current = current.next;
    }
    System.out.println();
}
```

**Key invariant:** The loop terminates when `current` becomes `null`, meaning we've reached the end.

### Collecting to a List

```java
public List<Integer> toList(Node head) {
    List<Integer> result = new ArrayList<>();
    Node current = head;
    while (current != null) {
        result.add(current.data);
        current = current.next;
    }
    return result;
}
```

---

## 2. Recursive Traversal

Elegant but uses O(n) stack space. Use when the problem naturally decomposes recursively.

```java
public void traverseRecursive(Node node) {
    if (node == null) return;

    System.out.print(node.data + " "); // process before recursion
    traverseRecursive(node.next);
}
```

### Print in Reverse (Recursive)

```java
public void traverseReverse(Node node) {
    if (node == null) return;

    traverseReverse(node.next);      // go to end first
    System.out.print(node.data + " "); // process after recursion (on the way back)
}
```

**How the stack unwinds:**
```
traverseReverse(1 -> 2 -> 3 -> null)
  calls traverseReverse(2 -> 3 -> null)
    calls traverseReverse(3 -> null)
      calls traverseReverse(null) → returns
    prints 3
  prints 2
prints 1
Output: 3 2 1
```

### Recursive Display with Arrows

```java
public void displayRecursive(Node node) {
    if (node == null) {
        System.out.println("null");
        return;
    }
    System.out.print(node.data + " -> ");
    displayRecursive(node.next);
}
```

---

## 3. Iterative Search

```java
public boolean search(Node head, int target) {
    Node current = head;
    while (current != null) {
        if (current.data == target) return true;
        current = current.next;
    }
    return false;
}

public int indexOf(Node head, int target) {
    Node current = head;
    int index = 0;
    while (current != null) {
        if (current.data == target) return index;
        current = current.next;
        index++;
    }
    return -1;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 4. Recursive Search

```java
public boolean searchRecursive(Node node, int target) {
    if (node == null) return false;
    if (node.data == target) return true;
    return searchRecursive(node.next, target);
}

public int indexOfRecursive(Node node, int target, int index) {
    if (node == null) return -1;
    if (node.data == target) return index;
    return indexOfRecursive(node.next, target, index + 1);
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n)  | (recursion stack) |

---

## 5. Find Middle of Linked List (Fast & Slow Pointers)

**Problem:** Find the middle node. If two middle nodes, return the second one.

**Example:** `1 -> 2 -> 3 -> 4 -> 5` → node with value 3

```java
public Node findMiddle(Node head) {
    Node slow = head;
    Node fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    return slow;
}
```

**How it works:**
- `slow` moves 1 step at a time
- `fast` moves 2 steps at a time
- When `fast` reaches the end, `slow` is at the middle

**Walkthrough: `1 -> 2 -> 3 -> 4 -> 5`**

| Step | slow | fast |
|------|------|------|
| start | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | 5 |

`fast.next` is null → loop ends → `slow` is at 3 ✓

### Variant: First Middle (for even-length lists)

```java
public Node findFirstMiddle(Node head) {
    Node slow = head;
    Node fast = head;

    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    return slow;
}
```

For `1 -> 2 -> 3 -> 4`: returns node 2 (first middle) vs the original which returns node 3 (second middle).

---

## 6. Find Nth Node from End

**Problem:** Find the nth node from the end of the list. n=1 is the last node.

**Example:** `1 -> 2 -> 3 -> 4 -> 5`, n=2 → node with value 4

### Approach 1: Two Pointers with Gap

```java
public Node nthFromEnd(Node head, int n) {
    Node fast = head;
    Node slow = head;

    // Move fast pointer n steps ahead
    for (int i = 0; i < n; i++) {
        if (fast == null) throw new IllegalArgumentException("n is larger than list size");
        fast = fast.next;
    }

    // Move both until fast reaches the end
    while (fast != null) {
        slow = slow.next;
        fast = fast.next;
    }

    return slow;
}
```

**Walkthrough: `1 -> 2 -> 3 -> 4 -> 5`, n=2**

| Step | slow | fast |
|------|------|------|
| after gap | 1 | 3 |
| 1 | 2 | 4 |
| 2 | 3 | 5 |
| 3 | 4 | null |

Result: node 4 ✓

### Approach 2: Length - n

```java
public Node nthFromEndLength(Node head, int n) {
    // First pass: count length
    int length = 0;
    Node current = head;
    while (current != null) {
        length++;
        current = current.next;
    }

    // Second pass: go to (length - n)th node
    current = head;
    for (int i = 0; i < length - n; i++) {
        current = current.next;
    }

    return current;
}
```

**Comparison:** Two-pointer approach is one pass, length approach is two passes. The two-pointer approach is the interview favorite.

---

## 7. Count Occurrences of a Value

```java
public int countOccurrences(Node head, int target) {
    int count = 0;
    Node current = head;
    while (current != null) {
        if (current.data == target) count++;
        current = current.next;
    }
    return count;
}
```

### Recursive Version

```java
public int countOccurrencesRecursive(Node node, int target) {
    if (node == null) return 0;
    int match = (node.data == target) ? 1 : 0;
    return match + countOccurrencesRecursive(node.next, target);
}
```

---

## Test Cases

```java
public static void main(String[] args) {
    // Build list: 1 -> 2 -> 3 -> 4 -> 5
    Node head = new Node(1);
    head.next = new Node(2);
    head.next.next = new Node(3);
    head.next.next.next = new Node(4);
    head.next.next.next.next = new Node(5);

    // Traversal
    System.out.print("Iterative: ");
    traverse(head);           // 1 2 3 4 5

    System.out.print("Reverse: ");
    traverseReverse(head);    // 5 4 3 2 1

    // Search
    System.out.println("Search 3: " + search(head, 3));  // true
    System.out.println("Search 9: " + search(head, 9));  // false
    System.out.println("Index of 4: " + indexOf(head, 4)); // 3

    // Middle
    System.out.println("Middle: " + findMiddle(head).data); // 3

    // Nth from end
    System.out.println("2nd from end: " + nthFromEnd(head, 2).data); // 4
    System.out.println("1st from end: " + nthFromEnd(head, 1).data); // 5

    // Count occurrences
    Node list2 = new Node(1);
    list2.next = new Node(2);
    list2.next.next = new Node(1);
    list2.next.next.next = new Node(1);
    System.out.println("Count 1s: " + countOccurrences(list2, 1)); // 3
}
```

---

## Key Patterns to Remember

| Pattern | When to Use |
|---------|-------------|
| Fast & slow pointers | Find middle, detect cycles |
| Two pointers with gap | Find nth from end |
| Recursive traversal | Print in reverse, tree-like decomposition |
| Single pointer + prev | Most insertion/deletion problems |
| Count length first | When you need size before processing |
