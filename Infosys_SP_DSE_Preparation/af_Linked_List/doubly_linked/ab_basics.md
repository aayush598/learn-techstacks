# Doubly Linked List - Basics

## Doubly Linked List Node Class
```python
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

## Doubly Linked List Implementation
```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
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
    new_node = DoublyListNode(val)
    
    if self.is_empty():
        self.head = new_node
        self.tail = new_node
    else:
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
    
    self.size += 1
```

### Insert at Tail - O(1)
```python
def insert_at_tail(self, val):
    new_node = DoublyListNode(val)
    
    if self.is_empty():
        self.head = new_node
        self.tail = new_node
    else:
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
    
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
    
    if position == self.size:
        self.insert_at_tail(val)
        return
    
    new_node = DoublyListNode(val)
    current = self.head
    
    for _ in range(position):
        current = current.next
    
    # Insert before current
    new_node.prev = current.prev
    new_node.next = current
    current.prev.next = new_node
    current.prev = new_node
    
    self.size += 1
```

## Deletion Operations

### Delete from Head - O(1)
```python
def delete_from_head(self):
    if self.is_empty():
        raise IndexError("List is empty")
    
    val = self.head.val
    
    if self.head == self.tail:
        self.head = None
        self.tail = None
    else:
        self.head = self.head.next
        self.head.prev = None
    
    self.size -= 1
    return val
```

### Delete from Tail - O(1)
```python
def delete_from_tail(self):
    if self.is_empty():
        raise IndexError("List is empty")
    
    val = self.tail.val
    
    if self.head == self.tail:
        self.head = None
        self.tail = None
    else:
        self.tail = self.tail.prev
        self.tail.next = None
    
    self.size -= 1
    return val
```

### Delete by Value - O(n)
```python
def delete_by_value(self, val):
    if self.is_empty():
        return False
    
    current = self.head
    
    while current:
        if current.val == val:
            if current == self.head:
                self.delete_from_head()
            elif current == self.tail:
                self.delete_from_tail()
            else:
                current.prev.next = current.next
                current.next.prev = current.prev
                self.size -= 1
            return True
        current = current.next
    
    return False
```

## Display List - O(n)
```python
def display_forward(self):
    elements = []
    current = self.head
    
    while current:
        elements.append(str(current.val))
        current = current.next
    
    return "None <-> " + " <-> ".join(elements) + " <-> None"

def display_backward(self):
    elements = []
    current = self.tail
    
    while current:
        elements.append(str(current.val))
        current = current.prev
    
    return "None <-> " + " <-> ".join(elements) + " <-> None"
```

## LRU Cache Implementation using DLL + HashMap - O(1) for get/put
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = DoublyListNode(0)
        self.tail = DoublyListNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        new_node = DoublyListNode(value)
        new_node.val = value
        self.cache[key] = new_node
        self._add_to_front(new_node)
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.val]

# Alternative cleaner LRU Cache
class LRUCacheClean:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = DoublyListNode(0)
        self.tail = DoublyListNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_head(node)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove_node(self.cache[key])
        
        node = DoublyListNode(value)
        self.cache[key] = node
        self._add_to_head(node)
        
        if len(self.cache) > self.capacity:
            lru_node = self.tail.prev
            self._remove_node(lru_node)
            del self.cache[lru_node.val]
```

## Flatten a Multilevel Linked List - O(n)
```python
class MultiLevelNode:
    def __init__(self, val=0, next=None, child=None):
        self.val = val
        self.next = next
        self.child = child

def flatten_multilevel(head):
    if not head:
        return head
    
    current = head
    
    while current:
        if current.child:
            # Flatten the child list
            child_head = flatten_multilevel(current.child)
            
            # Save next pointer
            next_node = current.next
            
            # Connect current to child
            current.next = child_head
            child_head.prev = current
            
            # Find tail of child list
            tail = child_head
            while tail.next:
                tail = tail.next
            
            # Connect tail to saved next
            tail.next = next_node
            if next_node:
                next_node.prev = tail
            
            # Remove child pointer
            current.child = None
        
        current = current.next
    
    return head
```

## Complete Example Usage
```python
# Create doubly linked list
dll = DoublyLinkedList()

# Insert elements
dll.insert_at_tail(1)
dll.insert_at_tail(2)
dll.insert_at_tail(3)
dll.insert_at_head(0)

print(dll.display_forward())   # None <-> 0 <-> 1 <-> 2 <-> 3 <-> None
print(dll.display_backward())  # None <-> 3 <-> 2 <-> 1 <-> 0 <-> None

# Delete operations
dll.delete_from_head()
print(f"After delete head: {dll.display_forward()}")  # 1 <-> 2 <-> 3

dll.delete_from_tail()
print(f"After delete tail: {dll.display_forward()}")  # 1 <-> 2

# LRU Cache example
cache = LRUCacheClean(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # Returns 1
cache.put(3, 3)      # Evicts key 2
print(cache.get(2))  # Returns -1 (not found)
```
