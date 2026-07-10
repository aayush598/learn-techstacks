# Doubly Linked List — Operations

With the full implementation in place, let's explore classic DLL operations that frequently appear in interviews.

---

## 1. Insert in Sorted Doubly Linked List

**Problem:** Insert a value into a sorted DLL while maintaining sorted order.

**Example:** List: `1 <-> 3 <-> 5 <-> 7`, insert 4 → `1 <-> 3 <-> 4 <-> 5 <-> 7`

```java
public void insertSorted(DNode head, DNode tail, int data) {
    DNode newNode = new DNode(data);

    // Case 1: Empty list
    if (head == null) {
        head = tail = newNode;
        return;
    }

    // Case 2: Insert before head
    if (data <= head.data) {
        newNode.next = head;
        head.prev = newNode;
        head = newNode;
        return;
    }

    // Case 3: Insert after tail
    if (data >= tail.data) {
        tail.next = newNode;
        newNode.prev = tail;
        tail = newNode;
        return;
    }

    // Case 4: Insert in middle — find position
    DNode current = head;
    while (current.next != null && current.next.data < data) {
        current = current.next;
    }

    // Insert newNode after current
    newNode.next = current.next;
    newNode.prev = current;
    current.next.prev = newNode;
    current.next = newNode;
}
```

### Walkthrough: Insert 4 into `1 <-> 3 <-> 5 <-> 7`

| Step | current | current.next.data < 4? |
|------|---------|----------------------|
| start | 1 | yes (3 < 4) |
| step 1 | 3 | no (5 >= 4) |

Insert after 3: set `newNode(4).next = 5`, `newNode(4).prev = 3`, then wire `3.next = 4` and `5.prev = 4`.

Result: `1 <-> 3 <-> 4 <-> 5 <-> 7` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 2. Delete Node with Given Reference

**Problem:** Delete a node from a DLL when given a direct reference to the node (not its value or index).

**Why this is O(1) in DLL:** The `prev` pointer lets us access the previous node without traversal.

```java
public DNode deleteNode(DNode head, DNode tail, DNode node) {
    if (node == null) return head;

    // Case 1: Only node
    if (head == tail) {
        return null; // list becomes empty
    }

    // Case 2: Deleting head
    if (node == head) {
        head = head.next;
        head.prev = null;
        return head;
    }

    // Case 3: Deleting tail
    if (node == tail) {
        tail = tail.prev;
        tail.next = null;
        return head;
    }

    // Case 4: Deleting middle node
    node.prev.next = node.next;
    node.next.prev = node.prev;

    return head;
}
```

### Walkthrough: Delete node 3 from `1 <-> 2 <-> 3 <-> 4 <-> 5`

```
Before: 2 <-> 3 <-> 4
         ↑     ↑
       prev   node (target)

Step 1: node.prev.next = node.next  →  2.next = 4
Step 2: node.next.prev = node.prev  →  4.prev = 2

After: 2 <-> 4  (3 is orphaned and garbage collected)
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(1)  |
| Space  | O(1)  |

---

## 3. Find Pairs with Given Sum K

**Problem:** Find all pairs of nodes whose values sum to K.

**Example:** List: `1 <-> 2 <-> 3 <-> 4 <-> 5`, K=5 → pairs: (1,4), (2,3)

### Approach: Two Pointers (Head and Tail)

```java
public void findPairsWithSum(DNode head, DNode tail, int targetSum) {
    if (head == null) return;

    DNode left = head;
    DNode right = tail;
    boolean found = false;

    while (left != right && left.prev != right) {
        int currentSum = left.data + right.data;

        if (currentSum == targetSum) {
            System.out.println("(" + left.data + ", " + right.data + ")");
            found = true;
            left = left.next;
            right = right.prev;
        } else if (currentSum < targetSum) {
            left = left.next;    // need a bigger sum
        } else {
            right = right.prev;  // need a smaller sum
        }
    }

    if (!found) {
        System.out.println("No pairs found");
    }
}
```

**Why this works in DLL:** We can walk inward from both ends simultaneously. If the sum is too small, we move the left pointer forward. If too large, we move the right pointer backward.

### Walkthrough: List `1 <-> 2 <-> 3 <-> 4 <-> 5`, K=5

| Step | left | right | sum | sum < 5? | Action |
|------|------|-------|-----|----------|--------|
| 1 | 1 | 5 | 6 | no | right-- |
| 2 | 1 | 4 | 5 | equal! | print (1,4), both advance |
| 3 | 2 | 3 | 5 | equal! | print (2,3), both advance |
| 4 | 3 | 2 | — | left == right, stop |

Result: `(1, 4)` and `(2, 3)` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 4. Rotate Doubly Linked List by N Positions

**Problem:** Rotate the DLL to the right by N positions.

**Example:** `1 <-> 2 <-> 3 <-> 4 <-> 5`, N=2 → `4 <-> 5 <-> 1 <-> 2 <-> 3`

### Approach: Break and Reconnect

```java
public DNode rotateByN(DNode head, DNode tail, int n) {
    if (head == null || head == tail || n == 0) return head;

    int size = 0;
    DNode current = head;
    while (current != null) {
        size++;
        current = current.next;
    }

    n = n % size; // normalize
    if (n == 0) return head;

    // Find the new tail: (size - n - 1)th node
    // That's the same as finding the (size - n)th node and going back one
    current = head;
    for (int i = 1; i < size - n; i++) {
        current = current.next;
    }

    DNode newTail = current;
    DNode newHead = current.next;

    // Break the connection between newTail and newHead
    newTail.next = null;
    newHead.prev = null;

    // Connect old tail to old head
    tail.next = head;
    head.prev = tail;

    // Update head and tail
    head = newHead;
    tail = newTail;

    return head;
}
```

### Walkthrough: `1 <-> 2 <-> 3 <-> 4 <-> 5`, N=2

size=5, n=2, so we need to find the (5-2)th node = 3rd node

| Step | current |
|------|---------|
| start | 1 |
| 1 | 2 |
| 2 | 3 |

newTail = 3, newHead = 4

**Actions:**
1. Break: `3.next = null`, `4.prev = null`
2. Connect: `5.next = 1`, `1.prev = 5`
3. Update: head = 4, tail = 3

Result: `4 <-> 5 <-> 1 <-> 2 <-> 3` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 5. Remove Duplicates from Sorted DLL

```java
public DNode removeDuplicatesSorted(DNode head) {
    DNode current = head;

    while (current != null && current.next != null) {
        if (current.data == current.next.data) {
            DNode duplicate = current.next;
            current.next = duplicate.next;

            if (duplicate.next != null) {
                duplicate.next.prev = current;
            }

            // duplicate is now orphaned → garbage collected
        } else {
            current = current.next;
        }
    }

    return head;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Insert in sorted DLL
    DoublyLinkedList dll = new DoublyLinkedList();
    dll.addLast(1);
    dll.addLast(3);
    dll.addLast(5);
    dll.addLast(7);
    dll.displayForward(); // 1 <-> 3 <-> 5 <-> 7

    dll.insertSorted(4);
    dll.displayForward(); // 1 <-> 3 <-> 4 <-> 5 <-> 7

    dll.insertSorted(0);
    dll.displayForward(); // 0 <-> 1 <-> 3 <-> 4 <-> 5 <-> 7

    dll.insertSorted(8);
    dll.displayForward(); // 0 <-> 1 <-> 3 <-> 4 <-> 5 <-> 7 <-> 8

    // Test 2: Delete node with reference
    DoublyLinkedList dll2 = new DoublyLinkedList();
    dll2.addLast(1);
    DNode node2 = new DNode(2);
    dll2.addLast(2);
    DNode node3 = new DNode(3);
    dll2.addLast(3);
    dll2.addLast(4);
    dll2.addLast(5);
    dll2.displayForward(); // 1 <-> 2 <-> 3 <-> 4 <-> 5

    dll2.head = dll2.deleteNode(dll2.head, dll2.tail, node3);
    dll2.displayForward(); // 1 <-> 2 <-> 4 <-> 5

    // Test 3: Pairs with sum
    System.out.println("Pairs with sum 5:");
    DoublyLinkedList dll3 = new DoublyLinkedList();
    dll3.addLast(1);
    dll3.addLast(2);
    dll3.addLast(3);
    dll3.addLast(4);
    dll3.addLast(5);
    dll3.findPairsWithSum(dll3.head, dll3.tail, 5);
    // (1, 4)
    // (2, 3)

    System.out.println("Pairs with sum 6:");
    dll3.findPairsWithSum(dll3.head, dll3.tail, 6);
    // (1, 5)
    // (2, 4)

    // Test 4: Rotate by N
    DoublyLinkedList dll4 = new DoublyLinkedList();
    dll4.addLast(1);
    dll4.addLast(2);
    dll4.addLast(3);
    dll4.addLast(4);
    dll4.addLast(5);
    dll4.head = dll4.rotateByN(dll4.head, dll4.tail, 2);
    dll4.displayForward(); // 4 <-> 5 <-> 1 <-> 2 <-> 3

    // Test 5: Remove duplicates from sorted
    DoublyLinkedList dll5 = new DoublyLinkedList();
    dll5.addLast(1);
    dll5.addLast(1);
    dll5.addLast(2);
    dll5.addLast(3);
    dll5.addLast(3);
    dll5.addLast(3);
    dll5.addLast(4);
    dll5.displayForward(); // 1 <-> 1 <-> 2 <-> 3 <-> 3 <-> 3 <-> 4

    dll5.head = dll5.removeDuplicatesSorted(dll5.head);
    dll5.displayForward(); // 1 <-> 2 <-> 3 <-> 4
}
```

---

## Quick Reference

| Operation | Time | Space | DLL Advantage |
|-----------|------|-------|---------------|
| Insert in sorted | O(n) | O(1) | No advantage |
| Delete by reference | **O(1)** | O(1) | SLL needs O(n) to find prev |
| Pairs with sum K | O(n) | O(1) | Two pointers from both ends |
| Rotate by N | O(n) | O(1) | No advantage |
| Remove duplicates (sorted) | O(n) | O(1) | No advantage |
