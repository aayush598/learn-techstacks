# Mo's Algorithm

## Overview

Offline algorithm for answering range queries. Reorders queries to minimize pointer movement. O((N+Q)√N).

```java
class MoAlgorithm {
    int[] arr, freq;
    int currentAnswer;
    
    MoAlgorithm(int[] nums) {
        arr = nums;
        freq = new int[1000001];  // adjust based on range
        currentAnswer = 0;
    }
    
    void add(int i) {
        int val = arr[i];
        freq[val]++;
        if (freq[val] == 1) currentAnswer++;  // distinct count
    }
    
    void remove(int i) {
        int val = arr[i];
        freq[val]--;
        if (freq[val] == 0) currentAnswer--;
    }
    
    class Query {
        int l, r, idx;
        Query(int l, int r, int idx) { this.l = l; this.r = r; this.idx = idx; }
    }
    
    int[] processQueries(Query[] queries) {
        int n = arr.length;
        int blockSize = (int) Math.sqrt(n);
        
        // Sort queries
        Arrays.sort(queries, (a, b) -> {
            int blockA = a.l / blockSize;
            int blockB = b.l / blockSize;
            if (blockA != blockB) return blockA - blockB;
            return (blockA % 2 == 0) ? a.r - b.r : b.r - a.r;  // Hilbert sort optimization
        });
        
        int[] result = new int[queries.length];
        int curL = 0, curR = -1;
        
        for (Query q : queries) {
            while (curL > q.l) add(--curL);
            while (curR < q.r) add(++curR);
            while (curL < q.l) remove(curL++);
            while (curR > q.r) remove(curR--);
            
            result[q.idx] = currentAnswer;
        }
        
        return result;
    }
}
```

## Complexity

- Each add/remove: O(1)
- Total pointer moves: O((N+Q)√N)
- Good for constraints up to 10⁵

## When to Use

- Offline queries (all queries known in advance)
- Range queries where add/remove can be done in O(1)
- No updates to the array
