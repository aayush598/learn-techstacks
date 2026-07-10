# Singly Linked List — Full Implementation

Let's build a complete singly linked list from scratch. This is the foundation for every linked list problem you'll encounter.

---

## Node Class

Every linked list starts with a node. Each node holds a value and a reference to the next node.

```java
public class Node {
    int data;
    Node next;

    public Node(int data) {
        this.data = data;
        this.next = null;
    }

    public Node(int data, Node next) {
        this.data = data;
        this.next = next;
    }

    @Override
    public String toString() {
        return data + "";
    }
}
```

---

## LinkedList Class — Fields

```java
public class LinkedList {
    Node head;
    Node tail;
    int size;

    public LinkedList() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
}
```

**Why track both head and tail?**
- `head` → needed for traversal from the beginning and `removeFirst()`
- `tail` → needed for O(1) `addLast()` without traversing the entire list
- `size` → O(1) size queries and index bounds checking

---

## Insertion Operations

### addFirst — O(1)

```java
public void addFirst(int data) {
    Node newNode = new Node(data);
    if (isEmpty()) {
        head = tail = newNode;
    } else {
        newNode.next = head;
        head = newNode;
    }
    size++;
}
```

### addLast — O(1)

```java
public void addLast(int data) {
    Node newNode = new Node(data);
    if (isEmpty()) {
        head = tail = newNode;
    } else {
        tail.next = newNode;
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

    Node newNode = new Node(data);
    Node prev = getNode(index - 1);
    newNode.next = prev.next;
    prev.next = newNode;
    size++;
}
```

**Helper: getNode(index)**

```java
private Node getNode(int index) {
    Node current = head;
    for (int i = 0; i < index; i++) {
        current = current.next;
    }
    return current;
}
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
    }

    size--;
    return data;
}
```

### removeLast — O(n)

```java
public int removeLast() {
    if (isEmpty()) {
        throw new RuntimeException("List is empty");
    }

    int data = tail.data;

    if (head == tail) {
        head = tail = null;
    } else {
        Node current = head;
        while (current.next != tail) {
            current = current.next;
        }
        current.next = null;
        tail = current;
    }

    size--;
    return data;
}
```

**Why O(n)?** To remove the last node, we need to update the second-to-last node's `next` to `null` and move `tail` back. There's no `prev` pointer in a singly linked list, so we must traverse.

### removeAtIndex — O(n)

```java
public int removeAtIndex(int index) {
    if (index < 0 || index >= size) {
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
    }

    if (index == 0) return removeFirst();
    if (index == size - 1) return removeLast();

    Node prev = getNode(index - 1);
    int data = prev.next.data;
    prev.next = prev.next.next;
    size--;
    return data;
}
```

---

## Search & Access Operations

### get — O(n)

```java
public int get(int index) {
    if (index < 0 || index >= size) {
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
    }
    return getNode(index).data;
}
```

### set — O(n)

```java
public int set(int index, int data) {
    if (index < 0 || index >= size) {
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
    }
    Node node = getNode(index);
    int old = node.data;
    node.data = data;
    return old;
}
```

### indexOf — O(n)

```java
public int indexOf(int data) {
    Node current = head;
    int index = 0;
    while (current != null) {
        if (current.data == data) return index;
        current = current.next;
        index++;
    }
    return -1;
}
```

### contains — O(n)

```java
public boolean contains(int data) {
    return indexOf(data) != -1;
}
```

---

## Utility Operations

### size and isEmpty

```java
public int size() {
    return size;
}

public boolean isEmpty() {
    return size == 0;
}
```

### clear — O(1)

```java
public void clear() {
    head = tail = null;
    size = 0;
}
```

We don't need to null out each node's `next` — once we lose the references to head and tail, the garbage collector handles the rest.

### display

```java
public void display() {
    Node current = head;
    StringBuilder sb = new StringBuilder();
    while (current != null) {
        sb.append(current.data);
        if (current.next != null) sb.append(" -> ");
        current = current.next;
    }
    sb.append(" -> null");
    System.out.println(sb.toString());
}
```

---

## Complete Working Example

```java
public class Main {
    public static void main(String[] args) {
        LinkedList list = new LinkedList();

        // Insertions
        list.addLast(10);
        list.addLast(20);
        list.addLast(30);
        list.addFirst(5);
        list.addAtIndex(2, 15);

        list.display();  // 5 -> 10 -> 15 -> 20 -> 30 -> null

        // Access
        System.out.println("Get index 2: " + list.get(2));        // 15
        System.out.println("Index of 20: " + list.indexOf(20));   // 3
        System.out.println("Contains 30: " + list.contains(30));  // true

        // Deletion
        System.out.println("Remove first: " + list.removeFirst()); // 5
        System.out.println("Remove last: " + list.removeLast());   // 30
        list.display();  // 10 -> 15 -> 20 -> null

        // Size
        System.out.println("Size: " + list.size());  // 3
    }
}
```

---

## Complexity Cheat Sheet

| Operation | Time | Notes |
|-----------|------|-------|
| addFirst | O(1) | |
| addLast | O(1) | with tail pointer |
| addAtIndex | O(n) | must traverse to position |
| removeFirst | O(1) | |
| removeLast | O(n) | no prev pointer in singly LL |
| removeAtIndex | O(n) | must traverse to position |
| get(index) | O(n) | no random access |
| set(index) | O(n) | must traverse to position |
| indexOf | O(n) | linear search |
| contains | O(n) | delegates to indexOf |
| size | O(1) | tracked field |
| isEmpty | O(1) | tracked field |
| clear | O(1) | null out references |

---

## Why Linked Lists Over Arrays?

| Feature | Array | Linked List |
|---------|-------|-------------|
| Access by index | O(1) | O(n) |
| Insert at beginning | O(n) (shift) | O(1) |
| Insert at end | O(1) amortized | O(1) with tail |
| Delete at beginning | O(n) (shift) | O(1) |
| Delete at end | O(1) | O(n) without doubly linked |
| Memory | Contiguous, cache-friendly | Scattered, pointer overhead |
| Size | Fixed or costly resize | Dynamic, no resize |

**Use linked lists when:** You need frequent insertions/deletions at the beginning or middle, and don't need random access by index.
