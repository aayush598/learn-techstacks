# Java DSA Cheatsheet (Interview-Ready)

## Core Collections
| Structure | Use Case | Notes |
| :-- | :-- | :-- |
| `ArrayList<Integer>` | Dynamic arrays | Good for traversal |
| `int[]` | Fixed arrays | Fastest |
| `HashMap<K,V>` | Frequency, mapping, two-sum type | O(1) avg |
| `HashSet<T>` | Lookups, duplicates | O(1) avg |
| `LinkedList<T>`/`ArrayDeque<T>` | Stack/Queue/Deque | Prefer ArrayDeque |
| `Stack<T>` | LIFO (less preferred now) | Use ArrayDeque as stack |
| `PriorityQueue<T>` | Heap (min-heap by default) | Max-heap: `new PriorityQueue<>(Collections.reverseOrder())` |
| `TreeMap/TreeSet` | Sorted structure | O(log n) |
| `HashMap + LinkedHashMap` | LRU style | Know both |

## Common Snippets

### Fast I/O (if needed)
```java
import java.io.*;
import java.util.*;
public class Main {
    static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    static StringTokenizer st = new StringTokenizer(br.readLine());
    // ...
}
```

### Array Utilities
```java
Arrays.sort(arr);
Arrays.fill(arr, -1);
System.arraycopy or loop;
```

### StringBuilder
```java
StringBuilder sb = new StringBuilder();
sb.append(x).append(' ');
```

### Two Pointers
```java
int left=0,right=arr.length-1;
while(left<right){ ... left++; right--; }
```

### Sliding Window
```java
int left=0, res=0;
for(int right=0; right<n; right++){
  // expand
  while(windowInvalid){ // shrink; left++; }
  // update res
}
```

### Binary Search Template
```java
int left=0,right=n-1;
while(left<=right){
  int mid = left + (right-left)/2;
  if(arr[mid]==target) return mid;
  if(arr[mid]<target) left=mid+1;
  else right=mid-1;
}
return -1;
```

### BFS/DFS
```java
// BFS
Queue<Node> q = new ArrayDeque<>(); q.offer(start); visited.add(start);
while(!q.isEmpty()){ Node cur=q.poll(); for(nb: adj(cur)){ if(!visited){visited.add(nb); q.offer(nb);}}}

// DFS
void dfs(Node cur, Set<Node> vis){ if(vis.contains(cur)) return; vis.add(cur); for(nb: adj(cur)) dfs(nb,vis); }
```

### Trie Node (Template)
```java
static class TrieNode{
  TrieNode[] children = new TrieNode[26];
  boolean isEnd;
}
```

### Union-Find (Disjoint Set/DSU)
```java
static class DSU{
  int[] parent,size;
  int n;
  DSU(int n){ this.n=n; parent=new int[n]; size=new int[n]; for(int i=0;i<n;i++){parent[i]=i; size[i]=1;}}
  int find(int x){ if(parent[x]!=x) parent[x]=find(parent[x]); return parent[x];}
  void union(int x,int y){ int rx=find(x),ry=find(y); if(rx==ry)return; if(size[rx]<size[ry]){parent[rx]=ry; size[ry]+=size[rx];} else {parent[ry]=rx; size[rx]+=size[ry];}}
}
```

## Must-Know Java Tricks
- `Integer.MAX_VALUE / 2` to avoid overflow on sums
- Modulus only when explicitly asked
- Use `charAt`, `toCharArray()` wisely
- For max/min use `Math.max/min`
