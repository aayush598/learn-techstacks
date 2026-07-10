# Circular Linked List — Full Implementation

A circular linked list is where the last node points back to the first node, forming a loop. This is useful for applications that cycle through a list repeatedly (e.g., round-robin scheduling, music playlists, Josephus problem).

---

## Design Decision: Head or Tail?

| Design | Pros | Cons |
|--------|------|------|
| Head pointer only | Simple traversal start | Adding to end requires traversal to find tail (O(n)) |
| Tail pointer only | O(1) add to end, O(1) access to head (tail.next) | Slightly less intuitive |
| Head and Tail | O(1) addFirst and addLast | Extra pointer to maintain |

**We'll use tail pointer only** — it's the most efficient design for circular lists. `tail.next` is always the head.

---

## Node Class

We can reuse the same Node class as singly linked list:

```java
public class Node {
    int data;
    Node next;

    public Node(int data) {
        this.data = data;
        this.next = null;
    }

    @Override
    public String toString() {
        return data + "";
    }
}
```

---

## CircularLinkedList Class

```java
public class CircularLinkedList {
    Node tail;  // tail.next = head
    int size;

    public CircularLinkedList() {
        this.tail = null;
        this.size = 0;
    }

    public boolean isEmpty() {
        return tail == null;
    }

    public int size() {
        return size;
    }
}
```

**Key insight:** We only need `tail` because:
- `tail.next` gives us access to `head`
- When we have `tail`, we can add to the end in O(1)
- When we have `tail.next` (head), we can add to the front in O(1)

---

## Insertion Operations

### insertFirst — O(1)

```java
public void insertFirst(int data) {
    Node newNode = new Node(data);

    if (isEmpty()) {
        newNode.next = newNode; // points to itself — the only node
        tail = newNode;
    } else {
        newNode.next = tail.next; // new node points to old head
        tail.next = newNode;      // tail (last node) points to new head
    }

    size++;
}
```

**Walkthrough: Insert 1, then 2 into empty list**

After `insertFirst(1)`:
```
tail -> [1] -> [1]   (single node points to itself)
```

After `insertFirst(2)`:
```
tail -> [1] -> [2] -> [1]
```
tail still points to node 1, but node 1 now points to node 2, which points back to node 1.

### insertLast — O(1)

```java
public void insertLast(int data) {
    Node newNode = new Node(data);

    if (isEmpty()) {
        newNode.next = newNode;
        tail = newNode;
    } else {
        newNode.next = tail.next; // new node points to head
        tail.next = newNode;      // old tail points to new node
        tail = newNode;           // update tail to new node
    }

    size++;
}
```

**Walkthrough: `insertLast(3)` on `2 -> 1 -> 2` (tail=1)**

```
Before:  tail(1) -> 2 -> 1 -> ...
Step 1:  newNode(3).next = tail.next = 2
Step 2:  tail(1).next = newNode(3)
Step 3:  tail = newNode(3)

After:   2 -> 1 -> 3 -> 2 -> ...  (tail=3)
```

Result: `2 -> 1 -> 3` (circular: 3 → 2)

---

## Deletion Operations

### deleteFirst — O(1)

```java
public int deleteFirst() {
    if (isEmpty()) {
        throw new RuntimeException("List is empty");
    }

    Node head = tail.next;
    int data = head.data;

    if (tail == head) {
        // Only one node
        tail = null;
    } else {
        tail.next = head.next; // skip the head node
    }

    size--;
    return data;
}
```

### deleteLast — O(n)

```java
public int deleteLast() {
    if (isEmpty()) {
        throw new RuntimeException("List is empty");
    }

    Node head = tail.next;

    if (tail == head) {
        // Only one node
        tail = null;
        size--;
        return head.data;
    }

    // Find the second-to-last node
    Node current = head;
    while (current.next != tail) {
        current = current.next;
    }

    int data = tail.data;
    current.next = head; // second-to-last becomes new tail
    tail = current;

    size--;
    return data;
}
```

**Why O(n)?** In a singly circular linked list, we can't go backward from tail. We must traverse from head to find the node before tail.

---

## Traversal

### Using do-while Loop

```java
public void display() {
    if (isEmpty()) {
        System.out.println("List is empty");
        return;
    }

    Node head = tail.next; // head is tail's next
    Node current = head;

    do {
        System.out.print(current.data + " -> ");
        current = current.next;
    } while (current != head);

    System.out.println("(back to " + head.data + ")");
}
```

**Why do-while?** A regular `while` loop would need a separate check for the first iteration. `do-while` guarantees we process at least one node and naturally stops when we circle back to head.

### Display with Tail Reference

```java
public void displayCircular() {
    if (isEmpty()) return;

    Node current = tail.next; // start from head
    StringBuilder sb = new StringBuilder();

    do {
        sb.append(current.data);
        current = current.next;
        if (current != tail.next) sb.append(" -> ");
    } while (current != tail.next);

    sb.append(" -> ").append(tail.next.data); // show it loops back
    System.out.println(sb.toString());
}
```

Output for `1 -> 2 -> 3`: `1 -> 2 -> 3 -> 1`

### Display from Tail

```java
public void displayFromTail() {
    if (isEmpty()) return;

    Node current = tail;
    StringBuilder sb = new StringBuilder();

    do {
        sb.append(current.data);
        current = current.next;
        if (current != tail) sb.append(" -> ");
    } while (current != tail);

    sb.append(" -> ").append(tail.data);
    System.out.println(sb.toString());
}
```

---

## Search in Circular Linked List

```java
public boolean contains(int target) {
    if (isEmpty()) return false;

    Node current = tail.next; // start from head

    do {
        if (current.data == target) return true;
        current = current.next;
    } while (current != tail.next);

    return false;
}

public int indexOf(int target) {
    if (isEmpty()) return -1;

    Node current = tail.next;
    int index = 0;

    do {
        if (current.data == target) return index;
        current = current.next;
        index++;
    } while (current != tail.next);

    return -1;
}
```

---

## Complete Working Example

```java
public class Main {
    public static void main(String[] args) {
        CircularLinkedList cll = new CircularLinkedList();

        // Insertions
        cll.insertLast(10);
        cll.insertLast(20);
        cll.insertLast(30);
        cll.insertFirst(5);
        cll.display();       // 5 -> 10 -> 20 -> 30 -> (back to 5)

        // Search
        System.out.println("Contains 20: " + cll.contains(20));  // true
        System.out.println("Contains 99: " + cll.contains(99));  // false
        System.out.println("Index of 30: " + cll.indexOf(30));   // 3

        // Deletions
        System.out.println("Delete first: " + cll.deleteFirst()); // 5
        System.out.println("Delete last: " + cll.deleteLast());   // 30
        cll.display();       // 10 -> 20 -> (back to 10)

        System.out.println("Size: " + cll.size());  // 2

        // Empty the list
        cll.deleteFirst();
        cll.deleteFirst();
        System.out.println("Empty: " + cll.isEmpty());  // true
    }
}
```

---

## Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| insertFirst | O(1) | O(1) |
| insertLast | O(1) | O(1) |
| deleteFirst | O(1) | O(1) |
| deleteLast | O(n) | O(1) |
| display | O(n) | O(1) |
| search | O(n) | O(1) |
| isEmpty | O(1) | O(1) |
| size | O(1) | O(1) |

---

## Common Pitfalls

1. **Infinite loops** — Always use a `do-while` loop with a clear stop condition (e.g., `current != head`). A `while(true)` without a break is a bug.
2. **Forgetting the single-node case** — When deleting, check if the list will become empty. A single-node circular list points to itself.
3. **Lost references** — When updating `tail.next`, make sure you've saved the old head reference first, or you'll lose access to the rest of the list.
4. **Not updating tail** — After `insertLast`, the new node becomes the tail. After `deleteLast`, the second-to-last node becomes the tail.
