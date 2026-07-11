# Binary Heap Implementation

## What is a Binary Heap?

A **complete binary tree** stored in an array with the **heap property**:
- **Max-Heap**: parent >= children (root is max)
- **Min-Heap**: parent <= children (root is min)

## Array Representation

For node at index `i`:
```
left child  = 2*i + 1
right child = 2*i + 2
parent      = (i-1) / 2
```

## MaxHeap Implementation

```java
class MaxHeap {
    private int[] heap;
    private int size;
    private int capacity;
    
    MaxHeap(int capacity) {
        this.capacity = capacity;
        this.size = 0;
        this.heap = new int[capacity];
    }
    
    private int parent(int i) { return (i - 1) / 2; }
    private int left(int i) { return 2 * i + 1; }
    private int right(int i) { return 2 * i + 2; }
    
    // Insert: add at end, bubble up
    void insert(int val) {
        if (size == capacity) throw new IllegalStateException("Heap full");
        heap[size] = val;
        int i = size;
        size++;
        
        // Bubble up: while parent is smaller, swap
        while (i > 0 && heap[parent(i)] < heap[i]) {
            swap(i, parent(i));
            i = parent(i);
        }
    }
    
    // Extract max: swap root with last, remove last, bubble down
    int extractMax() {
        if (size == 0) throw new NoSuchElementException("Heap empty");
        int max = heap[0];
        heap[0] = heap[size - 1];
        size--;
        bubbleDown(0);
        return max;
    }
    
    void bubbleDown(int i) {
        int largest = i;
        int l = left(i), r = right(i);
        
        if (l < size && heap[l] > heap[largest]) largest = l;
        if (r < size && heap[r] > heap[largest]) largest = r;
        
        if (largest != i) {
            swap(i, largest);
            bubbleDown(largest);
        }
    }
    
    int peek() { return heap[0]; }
    
    private void swap(int i, int j) {
        int temp = heap[i]; heap[i] = heap[j]; heap[j] = temp;
    }
}
```

## MinHeap Implementation

Same as MaxHeap but reverse comparison:
```java
// In insert: while (i > 0 && heap[parent(i)] > heap[i]) swap
// In bubbleDown: if (l < size && heap[l] < heap[smallest]) smallest = l;
```

## Complexity

| Operation | Time |
|-----------|------|
| Insert | O(log n) |
| Extract | O(log n) |
| Peek | O(1) |
| Heapify (build) | O(n) |
