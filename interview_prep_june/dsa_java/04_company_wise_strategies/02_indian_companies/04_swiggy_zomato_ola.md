# Swiggy, Zomato & Ola — Product-Based Interview Strategy

> "These companies solve real-world logistics problems. Graph algorithms, optimization, and system design are their bread and butter."

---

## 1. Company Overview

### Swiggy
- **Focus:** Food delivery optimization, real-time logistics
- **Package:** ₹10-20 LPA (freshers)
- **Rounds:** Online Assessment → Technical (2-3 rounds) → System Design → HR
- **Key Topics:** Graphs (routing), DP (optimization), System Design (microservices)

### Zomato
- **Focus:** Restaurant search, recommendations, delivery
- **Package:** ₹10-20 LPA (freshers)
- **Rounds:** Online Assessment → Technical (2 rounds) → Hiring Manager → HR
- **Key Topics:** Strings (search), Hashing (recommendations), Graphs (delivery)

### Ola
- **Focus:** Ride-sharing, route optimization, scheduling
- **Package:** ₹10-18 LPA (freshers)
- **Rounds:** Online Assessment → Technical (2 rounds) → System Design → HR
- **Key Topics:** Graphs (Dijkstra), Greedy (scheduling), DP (optimization)

---

## 2. Most Asked Topics (Priority Order)

| Priority | Topic | Swiggy | Zomato | Ola |
|----------|-------|--------|--------|-----|
| 1 | Graphs (BFS/DFS/Dijkstra) | ★★★★★ | ★★★★ | ★★★★★ |
| 2 | Dynamic Programming | ★★★★ | ★★★★ | ★★★★ |
| 3 | Hashing | ★★★★ | ★★★★★ | ★★★ |
| 4 | Arrays/Sorting | ★★★ | ★★★★ | ★★★★ |
| 5 | Trees | ★★★ | ★★★ | ★★★ |
| 6 | Strings | ★★ | ★★★★ | ★★ |
| 7 | System Design | ★★★★★ | ★★★★ | ★★★★★ |

---

## 3. Graph Algorithms (The Core)

### Problem 1: Dijkstra's Shortest Path
**Pattern:** Priority Queue + Graph Traversal

```java
import java.util.*;

public class Dijkstra {
    
    static class Edge {
        int to, weight;
        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }
    
    static class Node implements Comparable<Node> {
        int vertex, distance;
        Node(int vertex, int distance) {
            this.vertex = vertex;
            this.distance = distance;
        }
        
        @Override
        public int compareTo(Node other) {
            return Integer.compare(this.distance, other.distance);
        }
    }
    
    // Find shortest path from source to all vertices
    public static int[] shortestPath(List<List<Edge>> graph, int source) {
        int n = graph.size();
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[source] = 0;
        
        PriorityQueue<Node> pq = new PriorityQueue<>();
        pq.offer(new Node(source, 0));
        
        while (!pq.isEmpty()) {
            Node current = pq.poll();
            int u = current.vertex;
            
            // Skip if we already found a shorter path
            if (current.distance > dist[u]) continue;
            
            for (Edge edge : graph.get(u)) {
                int v = edge.to;
                int newDist = dist[u] + edge.weight;
                
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                    pq.offer(new Node(v, newDist));
                }
            }
        }
        
        return dist;
    }
    
    public static void main(String[] args) {
        int n = 5;
        List<List<Edge>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
        
        // Add edges: from, to, weight
        graph.get(0).add(new Edge(1, 4));
        graph.get(0).add(new Edge(2, 1));
        graph.get(1).add(new Edge(3, 1));
        graph.get(2).add(new Edge(1, 2));
        graph.get(2).add(new Edge(3, 5));
        
        int[] dist = shortestPath(graph, 0);
        System.out.println("Shortest distances from node 0: " + Arrays.toString(dist));
        // [0, 3, 1, 4, Infinity]
    }
}
```

**Time:** O((V + E) log V) | **Space:** O(V)

---

### Problem 2: BFS on Grid (Nearest Exit)
**Pattern:** Multi-source BFS

```java
public class NearestExit {
    
    // Find shortest path from entrance to nearest exit in maze
    // '.' = walkable, '+' = wall
    
    static class Cell {
        int row, col, distance;
        Cell(int row, int col, int distance) {
            this.row = row;
            this.col = col;
            this.distance = distance;
        }
    }
    
    public static int nearestExit(char[][] maze, int[] entrance) {
        int rows = maze.length, cols = maze[0].length;
        int[][] directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        
        Queue<Cell> queue = new LinkedList<>();
        queue.offer(new Cell(entrance[0], entrance[1], 0));
        maze[entrance[0]][entrance[1]] = '+'; // Mark visited
        
        while (!queue.isEmpty()) {
            Cell current = queue.poll();
            
            for (int[] dir : directions) {
                int newRow = current.row + dir[0];
                int newCol = current.col + dir[1];
                
                // Check bounds and walkable
                if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols 
                    && maze[newRow][newCol] == '.') {
                    
                    // Check if it's an exit (on boundary)
                    if (newRow == 0 || newRow == rows - 1 || newCol == 0 || newCol == cols - 1) {
                        return current.distance + 1;
                    }
                    
                    maze[newRow][newCol] = '+'; // Mark visited
                    queue.offer(new Cell(newRow, newCol, current.distance + 1));
                }
            }
        }
        
        return -1; // No exit found
    }
    
    public static void main(String[] args) {
        char[][] maze = {
            {'+', '+', '+', '+'},
            {'+', '.', '.', '+'},
            {'+', '.', '+', '+'},
            {'+', '+', '.', '+'}
        };
        int[] entrance = {1, 2};
        System.out.println("Nearest exit: " + nearestExit(maze, entrance) + " steps"); // 2
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n)

---

### Problem 3: Topological Sort (Course Schedule)
**Pattern:** DFS/BFS + DAG

```java
public class CourseSchedule {
    
    // Can you finish all courses given prerequisites?
    // This is cycle detection in directed graph
    
    public static boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
        
        int[] inDegree = new int[numCourses];
        
        // Build graph
        for (int[] pre : prerequisites) {
            graph.get(pre[1]).add(pre[0]); // pre[1] → pre[0]
            inDegree[pre[0]]++;
        }
        
        // BFS (Kahn's algorithm)
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) queue.offer(i);
        }
        
        int completed = 0;
        while (!queue.isEmpty()) {
            int course = queue.poll();
            completed++;
            
            for (int next : graph.get(course)) {
                inDegree[next]--;
                if (inDegree[next] == 0) queue.offer(next);
            }
        }
        
        return completed == numCourses;
    }
    
    public static void main(String[] args) {
        int[][] prereqs1 = {{1, 0}, {2, 1}, {3, 2}};
        System.out.println("Can finish? " + canFinish(4, prereqs1)); // true
        
        int[][] prereqs2 = {{1, 0}, {0, 1}};
        System.out.println("Can finish? " + canFinish(2, prereqs2)); // false (cycle)
    }
}
```

**Time:** O(V + E) | **Space:** O(V + E)

---

## 4. Optimization Problems (Swiggy/Zomato Style)

### Problem 4: Minimum Platforms (Scheduling)
**Pattern:** Greedy + Sorting

```java
public class MinPlatforms {
    
    // Given arrival and departure times of trains, find minimum platforms needed
    
    public static int findMinPlatforms(int[] arrival, int[] departure) {
        Arrays.sort(arrival);
        Arrays.sort(departure);
        
        int platforms = 1; // At least 1 platform needed
        int maxPlatforms = 1;
        int i = 1, j = 0; // i for arrival, j for departure
        
        while (i < arrival.length && j < departure.length) {
            if (arrival[i] <= departure[j]) {
                // A train arrives before previous departs → need more platform
                platforms++;
                maxPlatforms = Math.max(maxPlatforms, platforms);
                i++;
            } else {
                // A train departs → free up platform
                platforms--;
                j++;
            }
        }
        
        return maxPlatforms;
    }
    
    public static void main(String[] args) {
        int[] arrival = {900, 940, 950, 1100, 1500, 1800};
        int[] departure = {910, 1200, 1120, 1130, 1900, 2000};
        System.out.println("Min platforms needed: " + findMinPlatforms(arrival, departure)); // 3
    }
}
```

**Time:** O(n log n) | **Space:** O(1)

---

### Problem 5: Job Scheduling with Deadlines
**Pattern:** Greedy + Union-Find

```java
public class JobScheduling {
    
    static class Job {
        char id;
        int deadline, profit;
        Job(char id, int deadline, int profit) {
            this.id = id;
            this.deadline = deadline;
            this.profit = profit;
        }
    }
    
    // Schedule jobs to maximize profit
    public static void scheduleJobs(Job[] jobs) {
        // Sort by profit (descending)
        Arrays.sort(jobs, (a, b) -> b.profit - a.profit);
        
        int maxDeadline = 0;
        for (Job job : jobs) {
            maxDeadline = Math.max(maxDeadline, job.deadline);
        }
        
        char[] result = new char[maxDeadline];
        boolean[] slot = new boolean[maxDeadline];
        
        for (Job job : jobs) {
            // Find a free slot before deadline
            for (int j = Math.min(maxDeadline - 1, job.deadline - 1); j >= 0; j--) {
                if (!slot[j]) {
                    slot[j] = true;
                    result[j] = job.id;
                    break;
                }
            }
        }
        
        System.out.print("Scheduled jobs: ");
        for (int i = 0; i < maxDeadline; i++) {
            if (slot[i]) System.out.print(result[i] + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        Job[] jobs = {
            new Job('A', 2, 100),
            new Job('B', 1, 19),
            new Job('C', 2, 27),
            new Job('D', 1, 25),
            new Job('E', 3, 15)
        };
        scheduleJobs(jobs); // Scheduled jobs: C A E
    }
}
```

**Time:** O(n²) | **Space:** O(n)

---

### Problem 6: Merge Intervals
**Pattern:** Sorting + Greedy

```java
public class MergeIntervals {
    
    public static int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        
        // Sort by start time
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        
        List<int[]> merged = new ArrayList<>();
        int[] current = intervals[0];
        
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= current[1]) {
                // Overlapping intervals, merge them
                current[1] = Math.max(current[1], intervals[i][1]);
            } else {
                // No overlap, add current to result
                merged.add(current);
                current = intervals[i];
            }
        }
        merged.add(current);
        
        return merged.toArray(new int[merged.size()][]);
    }
    
    public static void main(String[] args) {
        int[][] intervals1 = {{1,3}, {2,6}, {8,10}, {15,18}};
        int[][] result1 = merge(intervals1);
        System.out.println("Merged: " + java.util.Arrays.deepToString(result1));
        // [[1,6], [8,10], [15,18]]
        
        int[][] intervals2 = {{1,4}, {4,5}};
        int[][] result2 = merge(intervals2);
        System.out.println("Merged: " + java.util.Arrays.deepToString(result2));
        // [[1,5]]
    }
}
```

**Time:** O(n log n) | **Space:** O(n)

---

## 5. Hashing Problems (Zomato Focus)

### Problem 7: Group Anagrams
**Pattern:** HashMap with sorted key

```java
public class GroupAnagrams {
    
    public static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        
        for (String str : strs) {
            // Sort characters to create key
            char[] chars = str.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);
            
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(str);
        }
        
        return new ArrayList<>(map.values());
    }
    
    public static void main(String[] args) {
        String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        List<List<String>> groups = groupAnagrams(strs);
        System.out.println("Groups: " + groups);
        // [[eat, tea, ate], [tan, nat], [bat]]
    }
}
```

**Time:** O(n × k log k) where k = avg string length | **Space:** O(n × k)

---

### Problem 8: Two Sum (All Pairs)
**Pattern:** HashMap

```java
public class TwoSumVariants {
    
    // Find all unique pairs that sum to target
    public static List<List<Integer>> twoSumPairs(int[] nums, int target) {
        List<List<Integer>> result = new ArrayList<>();
        Set<Integer> seen = new HashSet<>();
        Set<Integer> used = new HashSet<>();
        
        for (int num : nums) {
            int complement = target - num;
            
            if (seen.contains(complement) && !used.contains(num)) {
                result.add(Arrays.asList(Math.min(num, complement), 
                                         Math.max(num, complement)));
                used.add(num);
                used.add(complement);
            }
            seen.add(num);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        int[] nums = {1, 5, 7, -1, 5};
        System.out.println("Pairs summing to 6: " + twoSumPairs(nums, 6));
        // [[1, 5]]
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

## 6. Delivery Route Problems (Swiggy/Ola Style)

### Problem 9: Shortest Path in Weighted Graph
**Real-world:** Find optimal delivery route

```java
public class DeliveryRoute {
    
    static class Edge {
        int to, weight;
        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }
    
    // Find shortest route visiting all restaurants and returning
    // (Simplified TSP using Dijkstra between all pairs)
    
    public static int shortestRoute(List<List<Edge>> graph, int source, 
                                     int[] restaurants, int n) {
        // First, find shortest paths from source to all restaurants
        int[][] dist = new int[n][n];
        
        for (int r : restaurants) {
            dist[r] = dijkstra(graph, r, n);
        }
        
        // Simple TSP: try all permutations of restaurants
        int minCost = Integer.MAX_VALUE;
        int[] perm = new int[restaurants.length];
        for (int i = 0; i < restaurants.length; i++) perm[i] = i;
        
        do {
            int cost = 0;
            int current = source;
            for (int idx : perm) {
                cost += dist[current][restaurants[idx]];
                current = restaurants[idx];
            }
            cost += dist[current][source]; // Return to start
            minCost = Math.min(minCost, cost);
        } while (nextPermutation(perm));
        
        return minCost;
    }
    
    private static int[] dijkstra(List<List<Edge>> graph, int source, int n) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[source] = 0;
        
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
        pq.offer(new int[]{source, 0});
        
        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int u = current[0];
            
            if (current[1] > dist[u]) continue;
            
            for (Edge edge : graph.get(u)) {
                int newDist = dist[u] + edge.weight;
                if (newDist < dist[edge.to]) {
                    dist[edge.to] = newDist;
                    pq.offer(new int[]{edge.to, newDist});
                }
            }
        }
        
        return dist;
    }
    
    private static boolean nextPermutation(int[] arr) {
        int i = arr.length - 2;
        while (i >= 0 && arr[i] >= arr[i + 1]) i--;
        if (i < 0) return false;
        
        int j = arr.length - 1;
        while (arr[j] <= arr[i]) j--;
        
        int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
        
        int left = i + 1, right = arr.length - 1;
        while (left < right) {
            temp = arr[left]; arr[left] = arr[right]; arr[right] = temp;
            left++; right--;
        }
        return true;
    }
    
    public static void main(String[] args) {
        int n = 5;
        List<List<Edge>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
        
        graph.get(0).add(new Edge(1, 2));
        graph.get(1).add(new Edge(2, 3));
        graph.get(2).add(new Edge(3, 1));
        graph.get(3).add(new Edge(4, 2));
        graph.get(0).add(new Edge(3, 5));
        
        int[] restaurants = {1, 3};
        System.out.println("Shortest route cost: " + shortestRoute(graph, 0, restaurants, n));
    }
}
```

---

## 7. Time-Based Problems

### Problem 10: Time-based Key-Value Store
```java
public class TimeMap {
    
    static class Entry {
        String value;
        int timestamp;
        Entry(String value, int timestamp) {
            this.value = value;
            this.timestamp = timestamp;
        }
    }
    
    Map<String, List<Entry>> map;
    
    public TimeMap() {
        map = new HashMap<>();
    }
    
    public void set(String key, String value, int timestamp) {
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(new Entry(value, timestamp));
    }
    
    public String get(String key, int timestamp) {
        if (!map.containsKey(key)) return "";
        
        List<Entry> entries = map.get(key);
        
        // Binary search for largest timestamp <= given timestamp
        int left = 0, right = entries.size() - 1;
        String result = "";
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (entries.get(mid).timestamp <= timestamp) {
                result = entries.get(mid).value;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TimeMap tm = new TimeMap();
        tm.set("foo", "bar", 1);
        System.out.println(tm.get("foo", 1)); // "bar"
        System.out.println(tm.get("foo", 3)); // "bar"
        tm.set("foo", "bar2", 4);
        System.out.println(tm.get("foo", 4)); // "bar2"
        System.out.println(tm.get("foo", 5)); // "bar2"
    }
}
```

**Time:** O(log n) for get, O(1) for set | **Space:** O(n)

---

## 8. Complete Problem List for Swiggy/Zomato/Ola (35 Problems)

### Graphs (15)
1. Dijkstra's Shortest Path ✓
2. BFS on Grid ✓
3. Topological Sort ✓
4. Number of Islands
5. Rotting Oranges
6. Word Ladder
7. Clone Graph
8. Detect Cycle in Undirected Graph
9. Detect Cycle in Directed Graph
10. Minimum Spanning Tree (Prim's/Kruskal's)
11. Bellman-Ford Algorithm
12. Floyd-Warshall Algorithm
13. Strongly Connected Components (Kosaraju's)
14. Bipartite Graph Check
15. Alien Dictionary

### DP (10)
16. Longest Increasing Subsequence
17. Coin Change
18. Edit Distance
19. Longest Common Subsequence
20. Minimum Path Sum
21. Unique Paths
22. House Robber
23. Burst Balloons
24. Egg Dropping
25. Knapsack Problem

### Hashing & Arrays (6)
26. Two Sum ✓
27. Group Anagrams ✓
28. Merge Intervals ✓
29. Top K Frequent Elements
30. Subarray Sum Equals K
31. Longest Consecutive Sequence

### Scheduling & Optimization (4)
32. Minimum Platforms ✓
33. Job Scheduling ✓
34. Meeting Rooms II
35. Task Scheduler

---

## 9. System Design for These Companies

### Swiggy/Zomato: Food Delivery System
```
Components:
├── User Service (authentication, profiles)
├── Restaurant Service (menu, availability)
├── Order Service (order management, tracking)
├── Delivery Service (driver assignment, routing)
├── Search Service (restaurant discovery)
├── Payment Service (transactions, refunds)
└── Notification Service (SMS, push notifications)

Key Design Decisions:
- Real-time tracking → WebSockets
- Route optimization → Dijkstra's + traffic data
- Scalability → Microservices + message queues
- Caching → Restaurant menus in Redis
```

### Ola: Ride-Sharing System
```
Components:
├── Rider Service (booking, trip history)
├── Driver Service (availability, ratings)
├── Matching Service (rider-driver pairing)
├── Route Service (ETA calculation, navigation)
├── Pricing Service (dynamic pricing, surge)
├── Payment Service (cash, digital)
└── Safety Service (SOS, ride sharing)

Key Design Decisions:
- Real-time location → WebSockets + geospatial DB
- Driver matching → Greedy + nearest driver
- Dynamic pricing → Demand-supply algorithm
- ETA calculation → Dijkstra's with real-time traffic
```

---

## 10. Preparation Tips

### For Swiggy
1. **Master Graph Algorithms** — they love routing problems
2. **Practice System Design** — microservices, scalability
3. **Know Real-time Systems** — WebSockets, event-driven architecture
4. **Focus on Optimization** — they care about efficiency

### For Zomato
1. **Strong on Hashing** — search, matching, recommendations
2. **String Algorithms** — KMP, Rabin-Karp for search
3. **Data Modeling** — how to design database schemas
4. **Caching Strategies** — Redis, memcached

### For Ola
1. **Geospatial Algorithms** — KD-trees, geohashing
2. **Graph Algorithms** — Dijkstra's, A* for navigation
3. **Scheduling** — greedy algorithms for driver allocation
4. **Real-time Systems** — location tracking, ETA

### Common for All
1. **Practice 35+ problems** from the list above
2. **Understand trade-offs** — time vs space, accuracy vs speed
3. **Mock system design** — explain architecture clearly
4. **Think about scalability** — what happens with 10M users?

---

> **Remember:** Swiggy, Zomato, and Ola solve practical logistics problems. They want engineers who can optimize real-world systems. Think about routing, scheduling, and user experience in your solutions.
