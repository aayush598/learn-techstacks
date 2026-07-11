# Heapify & Complexity

## Building a Heap from Array

Two approaches:

### 1. Sequential Insert O(n log n)
```java
for (int x : arr) heap.insert(x);
```
Each insert = O(log n), total = O(n log n)

### 2. Heapify (Floyd's Algorithm) O(n)
```java
void buildHeap(int[] arr) {
    // Start from last non-leaf node, bubble down
    for (int i = arr.length/2 - 1; i >= 0; i--) {
        heapify(arr, i, arr.length);
    }
}

void heapify(int[] arr, int i, int n) {
    int largest = i;
    int left = 2*i + 1, right = 2*i + 2;
    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;
    if (largest != i) {
        swap(arr, i, largest);
        heapify(arr, largest, n);
    }
}
```

## Proof that Heapify is O(n)

Number of nodes at height h: ceil(n / 2^(h+1))
Time per node at height h: O(h)
Total: sum(h * ceil(n / 2^(h+1))) for h = 0 to log n
This sum converges to O(n). Specifically, sum(h/2^h) = 2.

## Heap Sort O(n log n)

```java
void heapSort(int[] arr) {
    int n = arr.length;
    // Build heap O(n)
    for (int i = n/2 - 1; i >= 0; i--) heapify(arr, i, n);
    // Extract one by one O(n log n)
    for (int i = n - 1; i > 0; i--) {
        swap(arr, 0, i);
        heapify(arr, 0, i);
    }
}
```

## Complexity Comparison

| Operation | Insert Each | Heapify |
|-----------|-------------|---------|
| Build heap | O(n log n) | O(n) |
| Insert one | O(log n) | O(log n) |
| Extract | O(log n) | O(log n) |
| Peek | O(1) | O(1) |

**Use heapify** when you have all elements upfront (faster).
**Use sequential insert** when elements arrive one at a time (same cost).
