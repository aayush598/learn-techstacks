# Singly Linked List - Basics

## Node Class Definition
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Example: Creating a node
node = ListNode(1)
node.next = ListNode(2)
node.next.next = ListNode(3)
```

## Singly Linked List Creation
```python
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        return self.head is None
```

## Insertion Operations

### Insert at Head - O(1)
```python
def insert_at_head(self, val):
    new_node = ListNode(val)
    new_node.next = self.head
    self.head = new_node
    self.size += 1
```

### Insert at Tail - O(n)
```python
def insert_at_tail(self, val):
    new_node = ListNode(val)
    if not self.head:
        self.head = new_node
    else:
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    self.size += 1
```

### Insert at Position - O(n)
```python
def insert_at_position(self, val, position):
    if position < 0 or position > self.size:
        raise IndexError("Position out of bounds")
    
    if position == 0:
        self.insert_at_head(val)
        return
    
    new_node = ListNode(val)
    current = self.head
    for _ in range(position - 1):
        current = current.next
    
    new_node.next = current.next
    current.next = new_node
    self.size += 1
```

## Deletion Operations

### Delete from Head - O(1)
```python
def delete_from_head(self):
    if not self.head:
        raise IndexError("List is empty")
    
    val = self.head.val
    self.head = self.head.next
    self.size -= 1
    return val
```

### Delete from Tail - O(n)
```python
def delete_from_tail(self):
    if not self.head:
        raise IndexError("List is empty")
    
    if not self.head.next:
        val = self.head.val
        self.head = None
        self.size -= 1
        return val
    
    current = self.head
    while current.next.next:
        current = current.next
    
    val = current.next.val
    current.next = None
    self.size -= 1
    return val
```

### Delete by Value - O(n)
```python
def delete_by_value(self, val):
    if not self.head:
        raise IndexError("List is empty")
    
    if self.head.val == val:
        self.head = self.head.next
        self.size -= 1
        return True
    
    current = self.head
    while current.next:
        if current.next.val == val:
            current.next = current.next.next
            self.size -= 1
            return True
        current = current.next
    
    return False
```

### Delete at Position - O(n)
```python
def delete_at_position(self, position):
    if position < 0 or position >= self.size:
        raise IndexError("Position out of bounds")
    
    if position == 0:
        return self.delete_from_head()
    
    current = self.head
    for _ in range(position - 1):
        current = current.next
    
    val = current.next.val
    current.next = current.next.next
    self.size -= 1
    return val
```

## Search Element - O(n)
```python
def search(self, val):
    current = self.head
    position = 0
    
    while current:
        if current.val == val:
            return position
        current = current.next
        position += 1
    
    return -1  # Not found
```

## Length of List - O(n)
```python
def length(self):
    count = 0
    current = self.head
    
    while current:
        count += 1
        current = current.next
    
    return count
```

## Display/Print List - O(n)
```python
def display(self):
    elements = []
    current = self.head
    
    while current:
        elements.append(str(current.val))
        current = current.next
    
    return " -> ".join(elements) + " -> None"
```

## Reverse Linked List

### Iterative Approach - O(n) time, O(1) space
```python
def reverse_iterative(self):
    prev = None
    current = self.head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    self.head = prev
```

### Recursive Approach - O(n) time, O(n) space
```python
def reverse_recursive(self):
    def reverse_helper(node):
        if not node or not node.next:
            return node
        
        new_head = reverse_helper(node.next)
        node.next.next = node
        node.next = None
        
        return new_head
    
    self.head = reverse_helper(self.head)
```

## Find Middle Element (Slow/Fast Pointer) - O(n)
```python
def find_middle(self):
    if not self.head:
        return None
    
    slow = self.head
    fast = self.head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow.val
```

## Nth Node from End - O(n)
```python
def nth_from_end(self, n):
    if n <= 0:
        raise ValueError("n must be positive")
    
    fast = self.head
    slow = self.head
    
    # Move fast pointer n steps ahead
    for _ in range(n):
        if not fast:
            raise IndexError("n is larger than list size")
        fast = fast.next
    
    # Move both pointers until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    return slow.val
```

## Complete Example Usage
```python
# Create linked list
ll = LinkedList()

# Insert elements
ll.insert_at_tail(1)
ll.insert_at_tail(2)
ll.insert_at_tail(3)
ll.insert_at_head(0)

print(ll.display())  # 0 -> 1 -> 2 -> 3 -> None
print(f"Length: {len(ll)}")  # Length: 4
print(f"Middle: {ll.find_middle()}")  # Middle: 2
print(f"Search 2: {ll.search(2)}")  # Search 2: 2
print(f"2nd from end: {ll.nth_from_end(2)}")  # 2nd from end: 2

# Reverse the list
ll.reverse_iterative()
print(f"After reverse: {ll.display()}")  # 3 -> 2 -> 1 -> 0 -> None
```
