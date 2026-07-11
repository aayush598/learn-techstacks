# SQRT Decomposition

## Overview

Divide array into blocks of size √n. Precompute information per block. Trade-off between update and query.

## Implementation: Range Sum + Point Update

```java
class SqrtDecomposition {
    private int[] arr;
    private long[] blockSums;
    private int blockSize;
    
    SqrtDecomposition(int[] nums) {
        arr = nums;
        int n = nums.length;
        blockSize = (int) Math.sqrt(n);
        int blockCount = (n + blockSize - 1) / blockSize;
        blockSums = new long[blockCount];
        
        for (int i = 0; i < n; i++) {
            blockSums[i / blockSize] += nums[i];
        }
    }
    
    void update(int idx, int val) {
        int block = idx / blockSize;
        blockSums[block] += val - arr[idx];
        arr[idx] = val;
    }
    
    long query(int l, int r) {
        int leftBlock = l / blockSize;
        int rightBlock = r / blockSize;
        long sum = 0;
        
        if (leftBlock == rightBlock) {
            // Same block: iterate directly
            for (int i = l; i <= r; i++) sum += arr[i];
        } else {
            // Left partial block
            for (int i = l; i < (leftBlock + 1) * blockSize; i++) sum += arr[i];
            
            // Complete blocks
            for (int b = leftBlock + 1; b < rightBlock; b++) sum += blockSums[b];
            
            // Right partial block
            for (int i = rightBlock * blockSize; i <= r; i++) sum += arr[i];
        }
        
        return sum;
    }
}
```

## Complexity

| Operation | Time |
|-----------|------|
| Build | O(n) |
| Point Update | O(1) |
| Range Query | O(√n) |

## When to Use

- **Simpler** than segment tree
- Good for **moderate constraints** (n ≤ 10⁵, q ≤ 10⁵)
- When √n queries are acceptable
- Basis for **Mo's algorithm**
