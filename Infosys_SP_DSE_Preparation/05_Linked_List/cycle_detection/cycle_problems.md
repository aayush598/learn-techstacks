# Linked List Cycle Detection Problems

## Floyd's Cycle Detection (Tortoise and Hare) - O(n)
**Key Insight**: If there's a cycle, slow and fast pointers will eventually meet.

```python
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    
    return True

# Alternative: Start both at head
def has_cycle_v2(head):
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False
```

## Find Start of Cycle - O(n)
**Key Insight**: After detecting cycle, move one pointer to head and advance both at same speed. They meet at cycle start.

```python
def detect_cycle_start(head):
    if not head or not head.next:
        return None
    
    # Phase 1: Detect cycle
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Phase 2: Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow

# Mathematical proof:
# Let meeting point be M, cycle start be S
# Distance from head to S = a
# Distance from S to M = b
# Distance from M to S (remaining cycle) = c
# Total cycle length = b + c
# 
# When they meet: slow traveled a + b, fast traveled a + b + c + b
# Fast travels twice: 2(a + b) = a + b + c + b
# Simplify: a = c
# So head to S distance = M to S distance
```

## Detect Cycle in Directed Graph Using This Concept - O(V + E)
```python
def has_cycle_in_graph(graph):
    """
    graph: dict where graph[node] = list of neighbors
    Uses DFS with state tracking (white, gray, black)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Cycle found
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    
    return False

# Example usage
graph = {
    1: [2],
    2: [3],
    3: [1],  # Cycle: 1 -> 2 -> 3 -> 1
    4: [5],
    5: []
}
print(has_cycle_in_graph(graph))  # True
```

## Happy Number Using Cycle Detection - O(log n)
```python
def is_happy(n):
    """
    A happy number eventually reaches 1 when replaced by sum of squares of digits.
    If not happy, it enters a cycle.
    """
    def get_next(num):
        total_sum = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total_sum += digit * digit
        return total_sum
    
    slow = n
    fast = get_next(n)
    
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))
    
    return fast == 1

# Mathematical insight: Unhappy numbers enter cycle containing 4
def is_happy_optimized(n):
    def get_next(num):
        total_sum = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total_sum += digit * digit
        return total_sum
    
    while n != 1 and n != 4:
        n = get_next(n)
    
    return n == 1
```

## Palindrome Linked List Using Cycle Detection - O(n) time, O(1) space
```python
def is_palindrome(head):
    """
    1. Find middle using slow/fast
    2. Reverse second half
    3. Compare first half with reversed second half
    4. Restore the list
    """
    if not head or not head.next:
        return True
    
    # Find middle
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    current = slow.next
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = current.next
    
    # Compare
    first = head
    second = prev
    result = True
    
    while second:
        if first.val != second.val:
            result = False
            break
        first = first.next
        second = second.next
    
    # Restore the list (optional)
    prev = None
    current = prev
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    slow.next = prev
    
    return result
```

## Remove Cycle from Linked List - O(n)
```python
def remove_cycle(head):
    if not head:
        return
    
    # Detect cycle
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return  # No cycle
    
    # Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    # Find end of cycle
    while fast.next != slow:
        fast = fast.next
    
    # Remove cycle
    fast.next = None
```

## Middle of Linked List Using Fast/Slow - O(n)
```python
def find_middle(head):
    """
    Slow pointer moves 1 step, fast moves 2 steps
    When fast reaches end, slow is at middle
    """
    if not head:
        return None
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow

# For even length, this returns the second middle
# For [1,2,3,4], returns 3
# For [1,2,3,4,5], returns 3

def find_middle_v2(head):
    """
    Returns first middle for even length
    For [1,2,3,4], returns 2
    """
    if not head:
        return None
    
    slow = head
    fast = head
    
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

## Complete Example Usage
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def create_cycle_list(values, cycle_pos):
    if not values:
        return None
    
    head = ListNode(values[0])
    nodes = [head]
    
    for val in values[1:]:
        nodes.append(ListNode(val))
        nodes[-2].next = nodes[-1]
    
    if cycle_pos >= 0:
        nodes[-1].next = nodes[cycle_pos]
    
    return head

# Test cycle detection
head = create_cycle_list([3, 2, 0, -4], 1)
print(f"Has cycle: {has_cycle(head)}")  # True
print(f"Cycle starts at: {detect_cycle_start(head).val}")  # 2

# Test happy number
print(f"19 is happy: {is_happy(19)}")  # True
print(f"2 is happy: {is_happy(2)}")  # False

# Test palindrome
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(2)
head.next.next.next = ListNode(1)
print(f"Is palindrome: {is_palindrome(head)}")  # True
```
