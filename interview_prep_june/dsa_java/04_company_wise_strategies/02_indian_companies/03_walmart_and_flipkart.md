# Walmart & Flipkart — Product-Based Interview Strategy

> "Walmart and Flipkart are India's top product-based companies. They test deep algorithmic thinking, system design, and optimization. Prepare for Medium-Hard problems."

---

## 1. Company Overview

### Walmart Global Tech India
- **Package:** ₹15-30 LPA (freshers)
- **Hiring:** Campus + Off-campus
- **Rounds:** Online Assessment → Technical (2-3 rounds) → Managerial → HR
- **Focus:** Data structures, algorithms, system design, optimization
- **Key Differentiator:** Strong emphasis on **scalability** and **efficiency**

### Flipkart
- **Package:** ₹12-25 LPA (freshers)
- **Hiring:** Campus + Off-campus + Hackathons
- **Rounds:** Online Assessment → Machine Coding → Technical (2 rounds) → HR
- **Focus:** DSA, system design, machine coding (design-focused)
- **Key Differentiator:** **Machine coding round** — design a system in code

---

## 2. Difficulty Level Comparison

| Aspect | Walmart | Flipkart |
|--------|---------|----------|
| Coding Difficulty | Medium-Hard | Medium-Hard |
| System Design | Yes (senior) | Yes (Machine Coding) |
| Focus Areas | Trees, Graphs, DP | String Algorithms, DP, Hashing |
| Time Pressure | Moderate | High (Machine Coding) |
| Expectation | Optimal solutions | Working system + clean code |

---

## 3. Most Asked Topics

### Walmart Priority
| Priority | Topic | Frequency |
|----------|-------|-----------|
| 1 | Trees (BST, Binary Tree) | 80% |
| 2 | Graphs (BFS, DFS, Dijkstra) | 75% |
| 3 | Dynamic Programming | 70% |
| 4 | Arrays (Advanced) | 60% |
| 5 | Hashing | 50% |
| 6 | Strings | 40% |
| 7 | Greedy | 30% |

### Flipkart Priority
| Priority | Topic | Frequency |
|----------|-------|-----------|
| 1 | Strings (Advanced) | 85% |
| 2 | Dynamic Programming | 80% |
| 3 | Hashing | 75% |
| 4 | Trees | 60% |
| 5 | Arrays | 55% |
| 6 | Graphs | 40% |
| 7 | Design Problems | 35% |

---

## 4. Core Problems with Solutions

### Problem 1: Two Sum (HashMap Approach)
**Pattern:** Hashing — O(n) solution

```java
import java.util.*;

public class TwoSum {
    
    // Store seen numbers and their indices
    // For each number, check if complement exists in map
    
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            
            map.put(nums[i], i);
        }
        
        return new int[]{-1, -1}; // Not found
    }
    
    // VARIANT: Return all pairs (not just first)
    public static List<List<Integer>> twoSumAllPairs(int[] nums, int target) {
        List<List<Integer>> result = new ArrayList<>();
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            if (map.containsKey(complement)) {
                // Add all pairs with complement
                for (int j = 0; j < map.get(complement); j++) {
                    result.add(Arrays.asList(complement, nums[i]));
                }
            }
            
            map.merge(nums[i], 1, Integer::sum);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] result = twoSum(nums, 9);
        System.out.println("Indices: " + result[0] + ", " + result[1]); // 0, 1
        
        int[] nums2 = {3, 3, 3, 3};
        System.out.println("All pairs: " + twoSumAllPairs(nums2, 6));
        // [[3, 3], [3, 3], [3, 3]]
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 2: Top K Frequent Elements
**Pattern:** HashMap + MinHeap (PriorityQueue)

```java
public class TopKFrequent {
    
    // APPROACH: Count frequencies → use MinHeap of size k
    // Why MinHeap? We want to keep the k most frequent
    // When heap size > k, remove the least frequent (root of min heap)
    
    public static int[] topKFrequent(int[] nums, int k) {
        // Step 1: Count frequencies
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.merge(num, 1, Integer::sum);
        }
        
        // Step 2: MinHeap based on frequency
        PriorityQueue<Map.Entry<Integer, Integer>> minHeap = 
            new PriorityQueue<>((a, b) -> a.getValue() - b.getValue());
        
        for (Map.Entry<Integer, Integer> entry : freqMap.entrySet()) {
            minHeap.offer(entry);
            if (minHeap.size() > k) {
                minHeap.poll(); // Remove least frequent
            }
        }
        
        // Step 3: Extract results
        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = minHeap.poll().getKey();
        }
        
        return result;
    }
    
    // ALTERNATIVE: Bucket Sort — O(n) time
    public static int[] topKFrequentBucket(int[] nums, int k) {
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.merge(num, 1, Integer::sum);
        }
        
        // Bucket sort: index = frequency, value = list of numbers
        List<Integer>[] buckets = new List[nums.length + 1];
        for (int i = 0; i <= nums.length; i++) {
            buckets[i] = new ArrayList<>();
        }
        
        for (Map.Entry<Integer, Integer> entry : freqMap.entrySet()) {
            buckets[entry.getValue()].add(entry.getKey());
        }
        
        // Collect top k from highest frequency bucket
        int[] result = new int[k];
        int index = 0;
        for (int i = buckets.length - 1; i >= 0 && index < k; i--) {
            for (int num : buckets[i]) {
                if (index < k) {
                    result[index++] = num;
                }
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        int[] nums = {1, 1, 1, 2, 2, 3};
        int[] result = topKFrequent(nums, 2);
        System.out.println("Top 2 frequent: " + Arrays.toString(result)); // [1, 2]
    }
}
```

**Time:** O(n log k) for heap, O(n) for bucket sort | **Space:** O(n)

---

### Problem 3: LRU Cache
**Pattern:** HashMap + Doubly Linked List

```java
public class LRUCache {
    
    // DESIGN: O(1) get and put operations
    // HashMap: key → Node in linked list
    // Doubly Linked List: maintains order (most recent at tail)
    
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
    private Node head, tail; // Dummy nodes for easier edge case handling
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0); // Dummy head
        tail = new Node(0, 0); // Dummy tail
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
        moveToHead(node); // Mark as recently used
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
                // Remove least recently used (node before tail)
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
        System.out.println(cache.get(2)); // -1 (not found)
    }
}
```

**Time:** O(1) for both get and put | **Space:** O(capacity)

---

### Problem 4: Serialize and Deserialize Binary Tree
**Pattern:** BFS/DFS + String Manipulation

```java
public class SerializeDeserializeTree {
    
    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }
    
    // SERIALIZE: Convert tree to string using preorder with null markers
    // "1,2,#,#,3,4,#,#,5,#,#"
    public static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        serializeHelper(root, sb);
        return sb.toString();
    }
    
    private static void serializeHelper(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append("#,");
            return;
        }
        sb.append(node.val).append(",");
        serializeHelper(node.left, sb);
        serializeHelper(node.right, sb);
    }
    
    // DESERIALIZE: Reconstruct tree from string
    public static TreeNode deserialize(String data) {
        Queue<String> queue = new LinkedList<>(Arrays.asList(data.split(",")));
        return deserializeHelper(queue);
    }
    
    private static TreeNode deserializeHelper(Queue<String> queue) {
        String val = queue.poll();
        if (val.equals("#")) return null;
        
        TreeNode node = new TreeNode(Integer.parseInt(val));
        node.left = deserializeHelper(queue);
        node.right = deserializeHelper(queue);
        return node;
    }
    
    // Test helper: print tree inorder
    static void inorder(TreeNode root) {
        if (root == null) return;
        inorder(root.left);
        System.out.print(root.val + " ");
        inorder(root.right);
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.right.left = new TreeNode(4);
        root.right.right = new TreeNode(5);
        
        String serialized = serialize(root);
        System.out.println("Serialized: " + serialized);
        
        TreeNode deserialized = deserialize(serialized);
        System.out.print("Inorder: ");
        inorder(deserialized); // 2 1 4 3 5
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 5: Word Break
**Pattern:** DP — similar to coin change

```java
public class WordBreak {
    
    // dp[i] = true if substring(0, i) can be segmented using dictionary
    // dp[i] = dp[j] && wordDict.contains(substring(j, i)) for all j < i
    
    public static boolean wordBreak(String s, List<String> wordDict) {
        Set<String> wordSet = new HashSet<>(wordDict);
        boolean[] dp = new boolean[s.length() + 1];
        dp[0] = true; // Empty string can always be segmented
        
        for (int i = 1; i <= s.length(); i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && wordSet.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break; // Found a valid segmentation
                }
            }
        }
        
        return dp[s.length()];
    }
    
    public static void main(String[] args) {
        List<String> dict1 = Arrays.asList("apple", "pen");
        System.out.println(wordBreak("applepenapple", dict1)); // true
        
        List<String> dict2 = Arrays.asList("cats", "dog", "sand", "and", "cat");
        System.out.println(wordBreak("catsandog", dict2)); // false
    }
}
```

**Time:** O(n² × k) where k = avg word length | **Space:** O(n)

---

### Problem 6: Edit Distance
**Pattern:** 2D DP

```java
public class EditDistance {
    
    // dp[i][j] = min operations to convert word1[0..i] to word2[0..j]
    // Operations: Insert, Delete, Replace
    
    public static int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Base cases: converting to/from empty string
        for (int i = 0; i <= m; i++) dp[i][0] = i; // Delete all
        for (int j = 0; j <= n; j++) dp[0][j] = j; // Insert all
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1]; // Characters match, no operation
                } else {
                    dp[i][j] = 1 + Math.min(
                        dp[i - 1][j],     // Delete
                        Math.min(
                            dp[i][j - 1],  // Insert
                            dp[i - 1][j - 1] // Replace
                        )
                    );
                }
            }
        }
        
        return dp[m][n];
    }
    
    public static void main(String[] args) {
        System.out.println(minDistance("horse", "ros"));   // 3
        System.out.println(minDistance("intention", "execution")); // 5
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n), can optimize to O(min(m,n))

---

### Problem 7: N-Queens
**Pattern:** Backtracking

```java
import java.util.*;

public class NQueens {
    
    public static List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        char[][] board = new char[n][n];
        
        // Initialize board with dots
        for (char[] row : board) Arrays.fill(row, '.');
        
        backtrack(board, 0, result);
        return result;
    }
    
    private static void backtrack(char[][] board, int row, List<List<String>> result) {
        if (row == board.length) {
            // Convert board to list of strings
            List<String> solution = new ArrayList<>();
            for (char[] r : board) {
                solution.add(new String(r));
            }
            result.add(solution);
            return;
        }
        
        for (int col = 0; col < board.length; col++) {
            if (isSafe(board, row, col)) {
                board[row][col] = 'Q';       // Place queen
                backtrack(board, row + 1, result); // Recurse
                board[row][col] = '.';       // Remove queen (backtrack)
            }
        }
    }
    
    private static boolean isSafe(char[][] board, int row, int col) {
        int n = board.length;
        
        // Check column
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') return false;
        }
        
        // Check upper-left diagonal
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') return false;
        }
        
        // Check upper-right diagonal
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
            if (board[i][j] == 'Q') return false;
        }
        
        return true;
    }
    
    public static void main(String[] args) {
        List<List<String>> solutions = solveNQueens(4);
        System.out.println("Number of solutions for 4-Queens: " + solutions.size());
        for (List<String> solution : solutions) {
            for (String row : solution) {
                System.out.println(row);
            }
            System.out.println();
        }
    }
}
```

**Time:** O(n!) | **Space:** O(n²)

---

### Problem 8: Number of Islands
**Pattern:** BFS/DFS on Grid

```java
public class NumberOfIslands {
    
    // Count connected components of '1's in a grid
    // Use DFS to mark all connected land cells as visited
    
    public static int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        
        int count = 0;
        int rows = grid.length, cols = grid[0].length;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        
        return count;
    }
    
    private static void dfs(char[][] grid, int row, int col) {
        int rows = grid.length, cols = grid[0].length;
        
        // Boundary and visited check
        if (row < 0 || row >= rows || col < 0 || col >= cols || grid[row][col] == '0') {
            return;
        }
        
        grid[row][col] = '0'; // Mark as visited
        
        // Visit all 4 neighbors
        dfs(grid, row + 1, col);
        dfs(grid, row - 1, col);
        dfs(grid, row, col + 1);
        dfs(grid, row, col - 1);
    }
    
    public static void main(String[] args) {
        char[][] grid = {
            {'1', '1', '0', '0', '0'},
            {'1', '1', '0', '0', '0'},
            {'0', '0', '1', '0', '0'},
            {'0', '0', '0', '1', '1'}
        };
        System.out.println("Number of islands: " + numIslands(grid)); // 3
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n) for recursion stack

---

## 5. Flipkart Machine Coding Round

### What is Machine Coding?
- Design and implement a working system in code (1-2 hours)
- Examples: Parking Lot, Splitwise, Vending Machine, Elevator
- Tests: OOP design, clean code, problem decomposition

### Parking Lot System (Simplified)

```java
import java.util.*;

public class ParkingLot {
    
    enum VehicleType { TWO_WHEELER, CAR, TRUCK }
    enum SpotStatus { AVAILABLE, OCCUPIED }
    
    static class Vehicle {
        String licensePlate;
        VehicleType type;
        
        Vehicle(String licensePlate, VehicleType type) {
            this.licensePlate = licensePlate;
            this.type = type;
        }
    }
    
    static class ParkingSpot {
        int id;
        VehicleType supportedType;
        SpotStatus status;
        Vehicle parkedVehicle;
        
        ParkingSpot(int id, VehicleType type) {
            this.id = id;
            this.supportedType = type;
            this.status = SpotStatus.AVAILABLE;
        }
        
        boolean canPark(VehicleType type) {
            return status == SpotStatus.AVAILABLE && supportedType == type;
        }
    }
    
    private Map<Integer, ParkingSpot> spots;
    private int nextSpotId;
    
    public ParkingLot(int twoWheelerSpots, int carSpots, int truckSpots) {
        spots = new HashMap<>();
        nextSpotId = 1;
        
        for (int i = 0; i < twoWheelerSpots; i++) {
            spots.put(nextSpotId, new ParkingSpot(nextSpotId++, VehicleType.TWO_WHEELER));
        }
        for (int i = 0; i < carSpots; i++) {
            spots.put(nextSpotId, new ParkingSpot(nextSpotId++, VehicleType.CAR));
        }
        for (int i = 0; i < truckSpots; i++) {
            spots.put(nextSpotId, new ParkingSpot(nextSpotId++, VehicleType.TRUCK));
        }
    }
    
    public int parkVehicle(Vehicle vehicle) {
        for (ParkingSpot spot : spots.values()) {
            if (spot.canPark(vehicle.type)) {
                spot.status = SpotStatus.OCCUPIED;
                spot.parkedVehicle = vehicle;
                return spot.id;
            }
        }
        return -1; // No spot available
    }
    
    public void removeVehicle(int spotId) {
        ParkingSpot spot = spots.get(spotId);
        if (spot != null && spot.status == SpotStatus.OCCUPIED) {
            spot.parkedVehicle = null;
            spot.status = SpotStatus.AVAILABLE;
        }
    }
    
    public int getAvailableSpots(VehicleType type) {
        int count = 0;
        for (ParkingSpot spot : spots.values()) {
            if (spot.supportedType == type && spot.status == SpotStatus.AVAILABLE) {
                count++;
            }
        }
        return count;
    }
    
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot(5, 10, 3);
        
        Vehicle car1 = new Vehicle("KA-01-1234", VehicleType.CAR);
        Vehicle car2 = new Vehicle("KA-02-5678", VehicleType.CAR);
        
        int spot1 = lot.parkVehicle(car1);
        System.out.println("Car 1 parked at spot: " + spot1);
        
        int spot2 = lot.parkVehicle(car2);
        System.out.println("Car 2 parked at spot: " + spot2);
        
        System.out.println("Available car spots: " + lot.getAvailableSpots(VehicleType.CAR)); // 8
        
        lot.removeVehicle(spot1);
        System.out.println("Available car spots: " + lot.getAvailableSpots(VehicleType.CAR)); // 9
    }
}
```

---

## 6. Common Walmart Problems (Top 20)

### Trees & BST
1. Validate BST
2. Lowest Common Ancestor
3. Binary Tree Level Order Traversal
4. Maximum Depth of Binary Tree
5. Serialize/Deserialize Binary Tree ✓
6. Inorder Successor in BST
7. Kth Smallest Element in BST

### Graphs
8. Number of Islands ✓
9. Clone Graph
10. Course Schedule (Topological Sort)
11. Alien Dictionary
12. Word Ladder
13. Dijkstra's Shortest Path

### Dynamic Programming
14. Longest Increasing Subsequence
15. Coin Change ✓
16. Word Break ✓
17. Edit Distance ✓
18. Unique Paths in Grid
19. Longest Common Subsequence

### Other
20. LRU Cache ✓

---

## 7. Common Flipkart Problems (Top 20)

### Strings & Hashing
1. Group Anagrams
2. Longest Substring Without Repeating Characters
3. Minimum Window Substring
4. Anagram Substring Search
5. Word Pattern

### Dynamic Programming
6. Word Break ✓
7. Edit Distance ✓
8. Longest Palindromic Subsequence
9. Burst Balloons
10. Egg Dropping Problem

### Trees & Graphs
11. Serialize/Deserialize Binary Tree ✓
12. Binary Tree from Preorder and Inorder
13. Top K Frequent Elements ✓
14. Find Median from Data Stream

### Design Problems
15. Design Parking Lot ✓
16. Design Splitwise
17. Design Vending Machine
18. Design URL Shortener

---

## 8. System Design Basics (Brief)

### For Senior Roles
```
Interview Round: System Design (45-60 min)
Topics: Scalability, Caching, Load Balancing, Database Design
Examples: Design Flipkart's product search, Design Walmart's inventory system
```

### Key Concepts
- **Horizontal Scaling:** Add more servers vs. vertical (bigger server)
- **Caching:** Redis/Memcached for frequent reads
- **Load Balancer:** Distribute traffic across servers
- **Database:** SQL vs. NoSQL, sharding, replication
- **Message Queue:** Kafka, RabbitMQ for async processing

---

## 9. Preparation Timeline (4 Weeks)

### Week 1: Trees & BST
- [ ] Binary Tree traversals (inorder, preorder, postorder)
- [ ] BST operations (insert, delete, search)
- [ ] LCA, diameter, path sum problems
- [ ] Practice: 15 tree problems

### Week 2: Graphs
- [ ] BFS, DFS, Topological Sort
- [ ] Dijkstra's, Bellman-Ford
- [ ] Union-Find, Minimum Spanning Tree
- [ ] Practice: 15 graph problems

### Week 3: DP Patterns
- [ ] 1D DP (climbing stairs, house robber)
- [ ] 2D DP (edit distance, LCS)
- [ ] Knapsack variants
- [ ] Practice: 15 DP problems

### Week 4: System Design + Mocks
- [ ] Machine coding practice (Parking Lot, Vending Machine)
- [ ] System design basics
- [ ] Full mock interviews
- [ ] Company-specific problem sets

---

## 10. Final Tips

### Walmart
1. **Focus on Trees and Graphs** — they love these topics
2. **Practice optimization** — always discuss time/space complexity
3. **Know system design** — for senior roles, this is crucial
4. **Be thorough** — explain your approach before coding

### Flipkart
1. **Master Machine Coding** — this round is unique to Flipkart
2. **Practice String algorithms** — KMP, Rabin-Karp, Z-algorithm
3. **Work on speed** — machine coding has tight deadlines
4. **Clean code matters** — naming conventions, modularity

### Common for Both
1. **Always discuss trade-offs** — "This approach is O(n) but uses O(n) space"
2. **Handle edge cases** — empty inputs, single elements, large inputs
3. **Practice 50+ problems** per topic
4. **Mock interviews** — get comfortable with whiteboard coding

---

> **Remember:** Walmart and Flipkart test not just coding ability, but problem-solving depth. They want to see HOW you think, not just the final answer. Think out loud, explain your approach, and always discuss alternatives.
