# Insertion and Deletion — Singly Linked List

These operations form the core of linked list manipulation. Master them and you'll handle any linked list problem.

---

## 1. Insert in Sorted Linked List

**Problem:** Insert a new node so the list remains sorted.

**Example:** List: `1 -> 3 -> 5 -> 7`, insert 4 → `1 -> 3 -> 4 -> 5 -> 7`

```java
public Node insertSorted(Node head, int data) {
    Node newNode = new Node(data);

    // Case 1: Empty list or insert before head
    if (head == null || head.data >= data) {
        newNode.next = head;
        return newNode;
    }

    // Case 2: Find the correct position
    Node current = head;
    while (current.next != null && current.next.data < data) {
        current = current.next;
    }

    newNode.next = current.next;
    current.next = newNode;

    return head;
}
```

**Why check `head == null`?** A common edge case. If the list is empty, the new node becomes both head and tail.

**Walkthrough: Insert 4 into `1 -> 3 -> 5 -> 7`**

| Step | current | current.next | current.next.data < 4? |
|------|---------|-------------|----------------------|
| start | 1 | 3 | yes (3 < 4) |
| step 1 | 3 | 5 | no (5 >= 4) |

Insert newNode (4) between 3 and 5 → `1 -> 3 -> 4 -> 5 -> 7` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 2. Delete First Occurrence of a Key

```java
public Node deleteFirstOccurrence(Node head, int key) {
    if (head == null) return null;

    // Case 1: Head holds the key
    if (head.data == key) {
        return head.next;
    }

    // Case 2: Search for the key
    Node current = head;
    while (current.next != null) {
        if (current.next.data == key) {
            current.next = current.next.next;
            return head;
        }
        current = current.next;
    }

    // Key not found
    return head;
}
```

### Walkthrough: Delete 3 from `1 -> 2 -> 3 -> 4 -> 5`

| Step | current | current.next.data | Match? |
|------|---------|-------------------|--------|
| start | 1 | 2 | no |
| step 1 | 2 | 3 | yes! |

Set `current.next = current.next.next` → `1 -> 2 -> 4 -> 5` ✓

---

## 3. Delete All Occurrences of a Key

```java
public Node deleteAllOccurrences(Node head, int key) {
    // Handle cases where head nodes match the key
    while (head != null && head.data == key) {
        head = head.next;
    }

    if (head == null) return null;

    Node current = head;
    while (current.next != null) {
        if (current.next.data == key) {
            current.next = current.next.next; // skip the matching node
            // Don't advance current — next node might also match
        } else {
            current = current.next;
        }
    }

    return head;
}
```

**Critical detail:** After skipping a node, we don't advance `current` because the new `current.next` might also be a match. This is a common bug — people forget this and skip consecutive duplicates.

### Walkthrough: Delete 3 from `3 -> 1 -> 3 -> 3 -> 2`

| Step | Action | List |
|------|--------|------|
| while loop | head.data = 3 = key, move head | `1 -> 3 -> 3 -> 2` |
| while loop | head.data = 1 ≠ key, stop | `1 -> 3 -> 3 -> 2` |
| traversal | current=1, next=3 matches, skip | `1 -> 3 -> 2` |
| traversal | current=1, next=3 matches, skip | `1 -> 2` |
| traversal | current=1, next=2 ≠ key, advance | `1 -> 2` |
| traversal | current=2, next=null, done | `1 -> 2` ✓ |

---

## 4. Remove Duplicates from Sorted List

**Problem:** Given a sorted linked list, remove all duplicate nodes (keep one of each value).

**Example:** `1 -> 1 -> 2 -> 3 -> 3 -> 3 -> 4` → `1 -> 2 -> 3 -> 4`

```java
public Node removeDuplicatesSorted(Node head) {
    Node current = head;

    while (current != null && current.next != null) {
        if (current.data == current.next.data) {
            // Skip the duplicate
            current.next = current.next.next;
        } else {
            // Move to next unique value
            current = current.next;
        }
    }

    return head;
}
```

**Walkthrough: `1 -> 1 -> 2 -> 3 -> 3`**

| Step | current | current.data | next.data | Action |
|------|---------|-------------|-----------|--------|
| 1 | 1 | 1 | 1 | skip, list: `1 -> 2 -> 3 -> 3` |
| 2 | 1 | 1 | 2 | advance |
| 3 | 2 | 2 | 3 | advance |
| 4 | 3 | 3 | 3 | skip, list: `1 -> 2 -> 3` |
| 5 | 3 | 3 | null | done |

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 5. Remove Duplicates from Unsorted List

**Problem:** Remove duplicates from an unsorted linked list.

**Example:** `3 -> 1 -> 3 -> 1 -> 2` → `3 -> 1 -> 2`

### Approach: HashSet + Previous Tracking

```java
public Node removeDuplicatesUnsorted(Node head) {
    Set<Integer> seen = new HashSet<>();
    Node current = head;
    Node prev = null;

    while (current != null) {
        if (seen.contains(current.data)) {
            // Duplicate found — skip it
            prev.next = current.next;
        } else {
            // First time seeing this value
            seen.add(current.data);
            prev = current;
        }
        current = current.next;
    }

    return head;
}
```

### Walkthrough: `3 -> 1 -> 3 -> 1 -> 2`

| Step | current | data | In set? | Action | Set |
|------|---------|------|---------|--------|-----|
| 1 | 3 | 3 | no | add to set, advance | {3} |
| 2 | 1 | 1 | no | add to set, advance | {3,1} |
| 3 | 3 | 3 | yes! | skip | {3,1} |
| 4 | 1 | 1 | yes! | skip | {3,1} |
| 5 | 2 | 2 | no | add to set | {3,1,2} |

Result: `3 -> 1 -> 2` ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n)  | (for the HashSet) |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Insert in sorted list
    Node sorted = buildList(new int[]{1, 3, 5, 7});
    sorted = insertSorted(sorted, 4);
    sorted = insertSorted(sorted, 0);
    sorted = insertSorted(sorted, 8);
    display(sorted); // 0 -> 1 -> 3 -> 4 -> 5 -> 7 -> 8

    // Test 2: Delete first occurrence
    Node list1 = buildList(new int[]{1, 2, 3, 4, 5});
    list1 = deleteFirstOccurrence(list1, 3);
    display(list1); // 1 -> 2 -> 4 -> 5

    // Test 3: Delete all occurrences
    Node list2 = buildList(new int[]{3, 1, 3, 3, 2, 3});
    list2 = deleteAllOccurrences(list2, 3);
    display(list2); // 1 -> 2

    // Test 4: Remove duplicates from sorted
    Node list3 = buildList(new int[]{1, 1, 2, 3, 3, 3, 4});
    list3 = removeDuplicatesSorted(list3);
    display(list3); // 1 -> 2 -> 3 -> 4

    // Test 5: Remove duplicates from unsorted
    Node list4 = buildList(new int[]{3, 1, 3, 1, 2});
    list4 = removeDuplicatesUnsorted(list4);
    display(list4); // 3 -> 1 -> 2

    // Edge cases
    System.out.println("Empty list:");
    Node empty = removeDuplicatesUnsorted(null);
    display(empty); // null

    System.out.println("Single node:");
    Node single = buildList(new int[]{5});
    single = removeDuplicatesUnsorted(single);
    display(single); // 5
}

// Helper methods
private static Node buildList(int[] arr) {
    if (arr.length == 0) return null;
    Node head = new Node(arr[0]);
    Node current = head;
    for (int i = 1; i < arr.length; i++) {
        current.next = new Node(arr[i]);
        current = current.next;
    }
    return head;
}

private static void display(Node head) {
    if (head == null) {
        System.out.println("null");
        return;
    }
    Node current = head;
    while (current != null) {
        System.out.print(current.data);
        if (current.next != null) System.out.print(" -> ");
        current = current.next;
    }
    System.out.println(" -> null");
}
```

---

## Common Pitfalls

1. **Not handling the head node** — always check if the head itself needs to be changed (insertion before head, deletion of head)
2. **Forgetting to advance `prev`** — in unsorted duplicate removal, only advance `prev` when you DON'T remove a node
3. **Skipping consecutive duplicates** — after removing a node, don't advance the current pointer until you've confirmed the next node isn't also a duplicate
4. **Null pointer exceptions** — always check `current.next != null` before accessing `current.next.data`
5. **Losing the head** — when modifying the head, return the new head from the function (don't modify in-place without returning)
