# Merge K Sorted Lists/Arrays

## Problem: Merge K Sorted Linked Lists

```java
ListNode mergeKLists(ListNode[] lists) {
    if (lists == null || lists.length == 0) return null;
    
    PriorityQueue<ListNode> pq = new PriorityQueue<>(
        (a, b) -> a.val - b.val
    );
    
    // Add head of each list
    for (ListNode head : lists) {
        if (head != null) pq.offer(head);
    }
    
    ListNode dummy = new ListNode(0);
    ListNode curr = dummy;
    
    while (!pq.isEmpty()) {
        ListNode node = pq.poll();
        curr.next = node;
        curr = curr.next;
        
        if (node.next != null) pq.offer(node.next);
    }
    
    return dummy.next;
}
```
Time: O(N log K), Space: O(K) where N total nodes, K lists.

## Problem: Merge K Sorted Arrays

```java
class ArrayEntry {
    int value;
    int arrayIndex;
    int elementIndex;
    
    ArrayEntry(int v, int ai, int ei) {
        value = v; arrayIndex = ai; elementIndex = ei;
    }
}

int[] mergeKSortedArrays(int[][] arrays) {
    PriorityQueue<ArrayEntry> pq = new PriorityQueue<>(
        (a, b) -> a.value - b.value
    );
    
    int totalSize = 0;
    for (int i = 0; i < arrays.length; i++) {
        if (arrays[i].length > 0) {
            pq.offer(new ArrayEntry(arrays[i][0], i, 0));
            totalSize += arrays[i].length;
        }
    }
    
    int[] result = new int[totalSize];
    int idx = 0;
    
    while (!pq.isEmpty()) {
        ArrayEntry entry = pq.poll();
        result[idx++] = entry.value;
        
        if (entry.elementIndex + 1 < arrays[entry.arrayIndex].length) {
            pq.offer(new ArrayEntry(
                arrays[entry.arrayIndex][entry.elementIndex + 1],
                entry.arrayIndex,
                entry.elementIndex + 1
            ));
        }
    }
    
    return result;
}
```

## Problem: Smallest Range Covering Elements from K Lists

```java
int[] smallestRange(List<List<Integer>> nums) {
    PriorityQueue<ArrayEntry> pq = new PriorityQueue<>(
        (a, b) -> a.value - b.value
    );
    
    int max = Integer.MIN_VALUE;
    for (int i = 0; i < nums.size(); i++) {
        pq.offer(new ArrayEntry(nums.get(i).get(0), i, 0));
        max = Math.max(max, nums.get(i).get(0));
    }
    
    int rangeStart = 0, rangeEnd = Integer.MAX_VALUE;
    
    while (pq.size() == nums.size()) {
        ArrayEntry curr = pq.poll();
        int min = curr.value;
        
        if (max - min < rangeEnd - rangeStart) {
            rangeStart = min;
            rangeEnd = max;
        }
        
        if (curr.elementIndex + 1 < nums.get(curr.arrayIndex).size()) {
            int nextVal = nums.get(curr.arrayIndex).get(curr.elementIndex + 1);
            pq.offer(new ArrayEntry(nextVal, curr.arrayIndex, curr.elementIndex + 1));
            max = Math.max(max, nextVal);
        }
    }
    
    return new int[]{rangeStart, rangeEnd};
}
```
