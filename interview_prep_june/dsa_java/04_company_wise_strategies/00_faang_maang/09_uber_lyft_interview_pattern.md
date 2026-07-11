# Uber / Lyft Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Uber/Lyft Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Focus on practical problem-solving experience
- Discussion of past projects involving scale

### Technical Phone Screen (45-60 min)
- 1-2 coding problems (Medium to Hard)
- Often includes **practical, real-world scenarios**
- May ask system design even for mid-level roles
- Focus on scalable, production-ready solutions

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (2): DSA with practical flavor
- **System Design** (1): Scalable systems (ride matching, real-time tracking)
- **Hiring Manager / Behavioral** (1): Team fit, project deep-dive
- **Bar Raiser** (1): Cross-cutting technical assessment

### Key Differences from Other FAANG
- **Practical problems** — Uber/Lyft love real-world scenarios
- **Graph problems** are very common (maps, routes, matching)
- **System design** is emphasized even for mid-level
- **Scalability** discussions are expected
- They value **end-to-end thinking** — from algorithm to deployment

---

## 2. Most Asked Topics

### Priority Matrix

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Graphs | 85% | Shortest path, matching, connectivity |
| 2 | Arrays | 80% | Sliding window, two pointers, sorting |
| 3 | HashMaps | 75% | Frequency, grouping, caching |
| 4 | System Design | 70% | Scalable, real-time systems |
| 5 | Trees | 60% | BST, binary tree |
| 6 | DP | 55% | Optimization, path problems |
| 7 | Strings | 50% | Pattern matching, parsing |

### Topic Frequency Graph
```
Graphs:     ████████████████████
Arrays:     ██████████████████
HashMaps:   █████████████████
Sys Design: ██████████████
Trees:      ████████████
DP:         ███████████
Strings:    ██████████
```

### What Makes Uber/Lyft Different
- **Graph problems** are king — they're a ride-sharing company
- **Real-world scenarios** — "design the matching algorithm"
- **Geospatial problems** — distance, proximity, grid-based
- **System design** is weighted heavily
- **Scalability** is always part of the discussion
- They want engineers who think about **production systems**

---

## 3. Uber/Lyft Culture

### Core Values

| Value | Meaning | Interview Impact |
|-------|---------|-----------------|
| **Do the Right Thing** | Ethical engineering | Discuss trade-offs honestly |
| **We Care** | User safety and experience | User-centric thinking |
| **Embrace the Action** | Bias for action | Quick prototyping, iteration |
| **Go Deep** | Deep technical expertise | Technical depth in discussions |
| **Build Together** | Collaboration | Team-oriented solutions |

### What Uber/Lyft Look For
1. **Practical problem-solving** — Not just algorithms, but real systems
2. **Scalability thinking** — How does this work at 1M+ requests?
3. **Graph theory knowledge** — Core to their business
4. **System design skills** — End-to-end system thinking
5. **User empathy** — How does this affect the user experience?

### Behavioral Questions
- "Tell me about a time you built a system that handled high traffic"
- "Describe a complex debugging experience"
- "How do you approach designing a new feature?"
- "Tell me about a time you had to make a trade-off between speed and quality"

---

## 4. Types of Problems

### Graph Problems (Uber/Lyft Specialty)
- Shortest path in weighted graph (Dijkstra's)
- Minimum spanning tree
- Network connectivity
- Ride matching algorithms
- Grid-based shortest path (BFS)

### Practical Scenarios
- Find nearest driver to a rider
- Calculate ETA using graph traversal
- Detect fraud in transaction graphs
- Optimize route for multiple pickups
- Find available time slots

### Array/HashMap Problems
- Two sum and variants
- Sliding window problems
- Frequency counting
- Prefix sums
- Merge intervals

### Design Problems
- Design ride-sharing system
- Design real-time tracking
- Design surge pricing
- Design driver-rider matching
- Design trip history system

---

## 5. Example Problems

### Problem 1: Shortest Path in Binary Matrix
**Problem:** Find the shortest path from top-left to bottom-right in a binary grid.

**Approach:** BFS — level by level exploration ensures shortest path.

```java
import java.util.*;

public class ShortestPathBinaryMatrix {

    // APPROACH: BFS on grid
    // Each level of BFS = one step further from start
    // 8-directional movement allowed
    
    public static int shortestPathBinaryMatrix(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        
        int[][] dirs = {{-1,-1},{-1,0},{-1,1},{0,-1},
                        {0,1},{1,-1},{1,0},{1,1}};
        
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0});
        grid[0][0] = 1; // Mark as visited
        
        int steps = 1;
        
        while (!queue.isEmpty()) {
            int size = queue.size();
            
            for (int i = 0; i < size; i++) {
                int[] cell = queue.poll();
                int row = cell[0], col = cell[1];
                
                if (row == n - 1 && col == n - 1) return steps;
                
                for (int[] dir : dirs) {
                    int newRow = row + dir[0];
                    int newCol = col + dir[1];
                    
                    if (newRow >= 0 && newRow < n && newCol >= 0 
                        && newCol < n && grid[newRow][newCol] == 0) {
                        grid[newRow][newCol] = 1; // Mark visited
                        queue.offer(new int[]{newRow, newCol});
                    }
                }
            }
            
            steps++;
        }
        
        return -1;
    }

    public static void main(String[] args) {
        int[][] grid1 = {{0,1},{1,0}};
        System.out.println(shortestPathBinaryMatrix(grid1)); // 2
        
        int[][] grid2 = {{0,0,0},{1,1,0},{1,1,0}};
        System.out.println(shortestPathBinaryMatrix(grid2)); // 4
    }
}
```

**Time:** O(n²) | **Space:** O(n²)

---

### Problem 2: Clone Graph
**Problem:** Given a reference to a node in a connected undirected graph, return a deep copy.

**Approach:** BFS/DFS with HashMap to track cloned nodes.

```java
import java.util.*;

public class CloneGraph {

    static class Node {
        int val;
        List<Node> neighbors;
        Node(int val) {
            this.val = val;
            this.neighbors = new ArrayList<>();
        }
    }

    // APPROACH: BFS with HashMap
    // Map original node → cloned node
    // For each neighbor, create clone if not exists, add to neighbors list
    
    public static Node cloneGraph(Node node) {
        if (node == null) return null;
        
        Map<Node, Node> map = new HashMap<>();
        Queue<Node> queue = new LinkedList<>();
        
        Node clone = new Node(node.val);
        map.put(node, clone);
        queue.offer(node);
        
        while (!queue.isEmpty()) {
            Node current = queue.poll();
            
            for (Node neighbor : current.neighbors) {
                if (!map.containsKey(neighbor)) {
                    map.put(neighbor, new Node(neighbor.val));
                    queue.offer(neighbor);
                }
                map.get(current).neighbors.add(map.get(neighbor));
            }
        }
        
        return clone;
    }

    // DFS APPROACH
    public static Node cloneGraphDFS(Node node) {
        if (node == null) return null;
        return dfs(node, new HashMap<>());
    }
    
    private static Node dfs(Node node, Map<Node, Node> map) {
        if (map.containsKey(node)) return map.get(node);
        
        Node clone = new Node(node.val);
        map.put(node, clone);
        
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(dfs(neighbor, map));
        }
        
        return clone;
    }

    public static void main(String[] args) {
        Node node1 = new Node(1);
        Node node2 = new Node(2);
        Node node3 = new Node(3);
        Node node4 = new Node(4);
        
        node1.neighbors.addAll(Arrays.asList(node2, node4));
        node2.neighbors.addAll(Arrays.asList(node1, node3));
        node3.neighbors.addAll(Arrays.asList(node2, node4));
        node4.neighbors.addAll(Arrays.asList(node1, node3));
        
        Node cloned = cloneGraph(node1);
        System.out.println("Cloned graph root: " + cloned.val); // 1
        System.out.println("Cloned neighbors: " + cloned.neighbors.size()); // 2
    }
}
```

**Time:** O(V + E) | **Space:** O(V)

---

### Problem 3: Find Median from Data Stream
**Problem:** Design a data structure that supports addNum and findMedian.

**Approach:** Two heaps — max-heap for lower half, min-heap for upper half.

```java
import java.util.*;

public class MedianFinder {

    // APPROACH: Two heaps
    // Max-heap: stores smaller half of numbers
    // Min-heap: stores larger half of numbers
    // Invariant: maxHeap.size() >= minHeap.size()
    
    private PriorityQueue<Integer> maxHeap; // Lower half (max at top)
    private PriorityQueue<Integer> minHeap; // Upper half (min at top)
    
    public MedianFinder() {
        maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        minHeap = new PriorityQueue<>();
    }
    
    public void addNum(int num) {
        maxHeap.offer(num);
        
        // Balance: move max from lower half to upper half
        minHeap.offer(maxHeap.poll());
        
        // Maintain invariant: maxHeap can be at most 1 larger
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.offer(minHeap.poll());
        }
    }
    
    public double findMedian() {
        if (maxHeap.size() > minHeap.size()) {
            return maxHeap.peek();
        }
        return (maxHeap.peek() + minHeap.peek()) / 2.0;
    }

    public static void main(String[] args) {
        MedianFinder mf = new MedianFinder();
        mf.addNum(1);
        mf.addNum(2);
        System.out.println(mf.findMedian()); // 1.5
        
        mf.addNum(3);
        System.out.println(mf.findMedian()); // 2.0
        
        mf.addNum(4);
        mf.addNum(5);
        System.out.println(mf.findMedian()); // 3.0
    }
}
```

**Time:** O(log n) for addNum, O(1) for findMedian | **Space:** O(n)

---

### Problem 4: Merge Intervals
**Problem:** Merge all overlapping intervals.

**Approach:** Sort by start time, then merge overlapping intervals.

```java
import java.util.*;

public class MergeIntervals {

    // APPROACH: Sort by start, then merge
    // If current interval overlaps with previous, merge them
    
    public static int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        
        // Sort by start time
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);
        
        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            int[] current = intervals[i];
            
            if (current[0] <= last[1]) {
                // Overlapping — merge by extending end
                last[1] = Math.max(last[1], current[1]);
            } else {
                // Non-overlapping — add new interval
                merged.add(current);
            }
        }
        
        return merged.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        int[][] intervals1 = {{1,3},{2,6},{8,10},{15,18}};
        int[][] result1 = merge(intervals1);
        for (int[] interval : result1) {
            System.out.print(Arrays.toString(interval) + " ");
        }
        // [[1,6], [8,10], [15,18]]
        
        int[][] intervals2 = {{1,4},{4,5}};
        int[][] result2 = merge(intervals2);
        for (int[] interval : result2) {
            System.out.print(Arrays.toString(interval) + " ");
        }
        // [[1,5]]
    }
}
```

**Time:** O(n log n) | **Space:** O(n)

---

### Problem 5: LRU Cache
**Problem:** Implement an LRU cache with O(1) get and put operations.

**Approach:** HashMap + Doubly Linked List.

```java
import java.util.*;

public class LRUCache {

    private class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
    
    private int capacity;
    private Map<Integer, Node> map;
    private Node head, tail; // Dummy nodes
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void moveToHead(Node node) {
        removeNode(node);
        addToFront(node);
    }
    
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToHead(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            moveToHead(node);
        } else {
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addToFront(newNode);
            
            if (map.size() > capacity) {
                Node lru = tail.prev;
                removeNode(lru);
                map.remove(lru.key);
            }
        }
    }

    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println(cache.get(1)); // 1
        cache.put(3, 3); // Evicts key 2
        System.out.println(cache.get(2)); // -1
    }
}
```

**Time:** O(1) for both | **Space:** O(capacity)

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Graph Algorithms
- [ ] BFS, DFS on graphs (10 problems)
- [ ] Shortest path: Dijkstra's, Bellman-Ford (5 problems)
- [ ] Minimum spanning tree (5 problems)
- [ ] Grid-based problems (10 problems)
- [ ] Practice: 20 problems

#### Week 2: Arrays and HashMaps
- [ ] Sliding window problems (10 problems)
- [ ] Two pointer technique (10 problems)
- [ ] HashMap patterns (10 problems)
- [ ] Merge intervals variants (5 problems)
- [ ] Practice: 20 problems

#### Week 3: Trees and DP
- [ ] BST operations (10 problems)
- [ ] Binary tree traversals (10 problems)
- [ ] 1D DP patterns (10 problems)
- [ ] 2D DP patterns (5 problems)
- [ ] Practice: 20 problems

#### Week 4: System Design and Mocks
- [ ] Ride-sharing system design
- [ ] Real-time tracking system
- [ ] Scalability concepts
- [ ] Mock interviews (3-5 sessions)
- [ ] Review weak areas

### Uber/Lyft-Specific Tips
1. **Master graph algorithms** — They're the core of ride-sharing
2. **Think about scale** — Always discuss how your solution scales
3. **Practice geospatial problems** — Grid, distance, proximity
4. **Know Dijkstra's** — Shortest path is bread and butter
5. **System design matters** — Even for coding rounds
6. **Real-world context** — Frame algorithms in ride-sharing context
7. **Be practical** — Uber/Lyft value working systems over clever algorithms
8. **Discuss trade-offs** — "This is faster but harder to maintain"

### Common Follow-up Questions
- "How would this work at scale (millions of rides)?"
- "What if the graph doesn't fit in memory?"
- "How would you handle real-time updates?"
- "What's the latency requirement?"
- "How would you test this system?"

### Resources
- LeetCode Graph problems tag
- "Algorithm Design Manual" for graph algorithms
- System design for real-time systems
- Dijkstra's and A* algorithm implementations

---

> **Remember:** Uber/Lyft value practical, scalable solutions. Always frame your algorithm in the context of real-world problems. Show that you can think about production systems, not just theoretical algorithms.
