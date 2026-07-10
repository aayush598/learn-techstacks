# Doubly Linked List — Full Implementation

A doubly linked list gives you a `prev` pointer on each node, enabling O(1) operations that singly linked lists can't do efficiently.

---

## Node Class

```java
public class DNode {
    int data;
    DNode prev;
    DNode next;

    public DNode(int data) {
        this.data = data;
        this.prev = null;
        this.next = null;
    }

    @Override
    public String toString() {
        return data + "";
    }
}
```

**Key difference from singly linked list:** The `prev` pointer allows traversal in both directions and O(1) deletion when you already have a reference to the node.

---

## DoublyLinkedList Class — Fields

```java
public class DoublyLinkedList {
    DNode head;
    DNode tail;
    int size;

    public DoublyLinkedList() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
}
```

---

## Insertion Operations

### addFirst — O(1)

```java
public void addFirst(int data) {
    DNode newNode = new DNode(data);

    if (isEmpty()) {
        head = tail = newNode;
    } else {
        newNode.next = head;
        head.prev = newNode;
        head = newNode;
    }
    size++;
}
```

**Key:** We must set both `newNode.next = head` AND `head.prev = newNode`. Forgetting the `prev` link is the #1 bug here.

### addLast — O(1)

```java
public void addLast(int data) {
    DNode newNode = new DNode(data);

    if (isEmpty()) {
        head = tail = newNode;
    } else {
        tail.next = newNode;
        newNode.prev = tail;
        tail = newNode;
    }
    size++;
}
```

### addAtIndex — O(n)

```java
public void addAtIndex(int index, int data) {
    if (index < 0 || index > size) {
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
    }

    if (index == 0) {
        addFirst(data);
        return;
    }
    if (index == size) {
        addLast(data);
        return;
    }

    DNode newNode = new DNode(data);
    DNode current = getNode(index);

    // Insert newNode before current
    newNode.prev = current.prev;
    newNode.next = current;
    current.prev.next = newNode;
    current.prev = newNode;

    size++;
}
```

**The four pointer assignments for middle insertion:**
```
newNode.prev = current.prev;   // 1. new node points back to previous
newNode.next = current;        // 2. new node points forward to current
current.prev.next = newNode;   // 3. previous node points forward to new
current.prev = newNode;        // 4. current points back to new
```

---

## Deletion Operations

### removeFirst — O(1)

```java
public int removeFirst() {
    if (isEmpty()) {
        throw new RuntimeException("List is empty");
    }

    int data = head.data;

    if (head == tail) {
        head = tail = null;
    } else {
        head = head.next;
        head.prev = null;
    }

    size--;
    return data;
}
```

### removeLast — O(1)

This is where DLL beats SLL. O(1) instead of O(n)!

```java
public int removeLast() {
    if (isEmpty()) {
        throw new RuntimeException("List is empty");
    }

    int data = tail.data;

    if (head == tail) {
        head = tail = null;
    } else {
        tail = tail.prev;
        tail.next = null;
    }

    size--;
    return data;
}
```

### removeAtIndex — O(n)

```java
public int removeAtIndex(int index) {
    if (index < 0 || index >= size) {
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
    }

    if (index == 0) return removeFirst();
    if (index == size - 1) return removeLast();

    DNode current = getNode(index);

    // Bypass current node
    current.prev.next = current.next;
    current.next.prev = current.prev;

    size--;
    return current.data;
}
```

**O(1) deletion if you have the node reference:**

```java
public void removeNode(DNode node) {
    if (node == head) {
        removeFirst();
        return;
    }
    if (node == tail) {
        removeLast();
        return;
    }

    node.prev.next = node.next;
    node.next.prev = node.prev;
    size--;
}
```

**This is the big DLL advantage:** If someone hands you a reference to the node (not its index), you can delete it in O(1) by wiring around it. In SLL, you'd need to traverse to find the previous node.

---

## Display Operations

### Forward Display

```java
public void displayForward() {
    DNode current = head;
    StringBuilder sb = new StringBuilder();
    sb.append("null <-> ");

    while (current != null) {
        sb.append(current.data).append(" <-> ");
        current = current.next;
    }

    sb.append("null");
    System.out.println(sb.toString());
}
```

Output: `null <-> 1 <-> 2 <-> 3 <-> null`

### Backward Display

```java
public void displayBackward() {
    DNode current = tail;
    StringBuilder sb = new StringBuilder();
    sb.append("null <-> ");

    while (current != null) {
        sb.append(current.data).append(" <-> ");
        current = current.prev;
    }

    sb.append("null");
    System.out.println(sb.toString());
}
```

Output: `null <-> 3 <-> 2 <-> 1 <-> null`

---

## Reverse Doubly Linked List

```java
public void reverse() {
    DNode current = head;
    DNode temp;

    while (current != null) {
        // Swap prev and next
        temp = current.prev;
        current.prev = current.next;
        current.next = temp;

        // Move to the next node (which is now prev because we swapped)
        current = current.prev;
    }

    // Swap head and tail
    temp = head;
    head = tail;
    tail = temp;
}
```

**Why does this work?** After swapping `prev` and `next`, the "next" node in the original order is now in `current.prev`. So we advance `current = current.prev`.

### Walkthrough: `1 <-> 2 <-> 3`

| Step | current | Before swap | After swap | current = |
|------|---------|-------------|------------|-----------|
| 1 | 1 | prev=null, next=2 | prev=2, next=null | 2 |
| 2 | 2 | prev=1, next=3 | prev=3, next=1 | 3 |
| 3 | 3 | prev=2, next=null | prev=null, next=2 | null |

After loop: swap head(1) and tail(3) → head=3, tail=1

Result: `3 <-> 2 <-> 1` ✓

### Recursive Reverse

```java
public DNode reverseRecursive(DNode node) {
    if (node == null || node.next == null) {
        head = node;
        return node;
    }

    DNode newHead = reverseRecursive(node.next);

    node.next.next = node;
    node.next.prev = node;
    node.prev = null;

    return newHead;
}
```

---

## Helper: getNode

```java
private DNode getNode(int index) {
    if (index < 0 || index >= size) {
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
    }

    DNode current;
    if (index < size / 2) {
        // Search from head
        current = head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
    } else {
        // Search from tail (this is faster for DLL!)
        current = tail;
        for (int i = size - 1; i > index; i--) {
            current = current.prev;
        }
    }

    return current;
}
```

**Optimization:** We choose direction based on whether the index is in the first or second half. This cuts average traversal time in half.

---

## Complete Working Example

```java
public class Main {
    public static void main(String[] args) {
        DoublyLinkedList dll = new DoublyLinkedList();

        dll.addLast(10);
        dll.addLast(20);
        dll.addLast(30);
        dll.addFirst(5);
        dll.addAtIndex(2, 15);

        dll.displayForward();  // null <-> 5 <-> 10 <-> 15 <-> 20 <-> 30 <-> null
        dll.displayBackward(); // null <-> 30 <-> 20 <-> 15 <-> 10 <-> 5 <-> null

        System.out.println("Size: " + dll.size());  // 5

        dll.removeFirst();
        dll.removeLast();
        dll.displayForward();  // null <-> 10 <-> 15 <-> 20 <-> null

        dll.reverse();
        dll.displayForward();  // null <-> 20 <-> 15 <-> 10 <-> null
    }
}
```

---

## Complexity Comparison: SLL vs DLL

| Operation | SLL | DLL |
|-----------|-----|-----|
| addFirst | O(1) | O(1) |
| addLast | O(1)* | O(1) |
| addAtIndex | O(n) | O(n) |
| removeFirst | O(1) | O(1) |
| removeLast | O(n) | **O(1)** |
| removeAtIndex | O(n) | O(n) |
| remove(node ref) | O(n) to find prev | **O(1)** |
| getNode(index) | O(n) | **O(n/2)** (search from nearest end) |
| reverse | O(n) | O(n) |
| backward traversal | O(n) | **O(n)** (native) |

*With tail pointer

**DLL uses more memory** per node (one extra pointer), but gains O(1) tail removal and O(1) node removal when you have a reference.
