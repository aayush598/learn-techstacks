# Amazon Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Amazon Values (Leadership Principles)
4. Types of Problems
5. Example Problems with Approaches
6. Bar Raiser Round
7. Preparation Strategy

---

## 1. Interview Format

### Online Assessment (OA)
- 2-3 coding problems (60-90 min)
- Usually medium difficulty
- Workstyle assessment (personality test)
- Must pass OA to proceed

### Phone Screen (45-60 min)
- 1 coding problem on shared editor
- Some Leadership Principles (LPs) discussion
- Review of OA solution

### On-site (5-6 rounds, 45-60 min each)
- **Coding problems** (2-3): Data structures, algorithms
- **System Design** (1): For SDE II and above
- **OOP Design** (1): Object-oriented design problems
- **Bar Raiser** (1): Most important round — harder problems, LP deep dive
- All rounds include **Leadership Principles** questions

### Key Differences
- Amazon has the most rounds among FAANG
- Leadership Principles are the MOST important — even DSA rounds evaluate LP
- Bar Raiser has veto power — they ensure the hire raises the bar
- OOP Design round tests your ability to design extensible systems

---

## 2. Most Asked Topics

| Topic | Frequency | Why Amazon Asks It |
|-------|-----------|-------------------|
| Arrays | Very High | Product data, inventory management |
| Strings | Very High | Search, product descriptions |
| Trees | High | Category hierarchy, recommendations |
| Hashing | High | Caching, fast lookup |
| Heaps | High | Top K products, best sellers |
| Graphs | Medium | Logistics, delivery optimization |
| DP | Medium | Pricing optimization, resource allocation |
| Design (OOP) | Very High | Extensible system design |
| Recursion | Medium | Tree problems, file system |

### Topic Frequency Graph
```
Arrays:  ████████████████████
Strings: ████████████████████
Trees:   ████████████████
Hash:    ████████████████
Heap:    ██████████████
Design:  ██████████████
Graphs:  ████████
DP:      ██████
```

---

## 3. Amazon Values — Leadership Principles (LPs)

You MUST prepare stories for each LP. Every behavioral question is tied to one.

### The 16 Leadership Principles

| LP | What They Want to Hear | Story Template |
|----|----------------------|----------------|
| **Customer Obsession** | Customer-first decisions | "The customer needed X, so I..." |
| **Ownership** | Taking responsibility beyond role | "I saw a problem and fixed it even though it wasn't my job" |
| **Invent and Simplify** | Creative solutions, simple designs | "I found a simpler way to do Y" |
| **Are Right, A Lot** | Good judgment, learning from mistakes | "I was wrong about Z, but here's what I learned" |
| **Learn and Be Curious** | Continuous learning | "I learned a new technology for this project" |
| **Hire and Develop the Best** | Mentoring, raising standards | "I mentored a junior engineer" |
| **Insist on the Highest Standards** | Quality, not cutting corners | "I found a bug that no one noticed and fixed it" |
| **Think Big** | Vision beyond current scope | "I proposed a feature that would scale 10x" |
| **Bias for Action** | Speed, calculated risks | "I made a quick decision without waiting for approval" |
| **Frugality** | Resource optimization | "I found a way to save costs on infrastructure" |
| **Earn Trust** | Integrity, transparency | "I was honest about a mistake/limitation" |
| **Dive Deep** | Getting into details | "I investigated a problem at the code level" |
| **Have Backbone; Disagree and Commit** | Disagree respectfully, commit to decisions | "I disagreed with the approach but committed once decided" |
| **Deliver Results** | Consistent output | "I shipped feature X on time despite obstacles" |
| **Strive to be Earth's Best Employer** | Team culture, safety | "I improved team processes/onboarding" |
| **Success and Scale Bring Broad Responsibility** | Social responsibility | "I considered the broader impact of my work" |

### The STAR Method for LP Stories
- **S**ituation: What was the context?
- **T**ask: What was your responsibility?
- **A**ction: What did YOU do? (Use "I", not "we")
- **R**esult: What was the outcome? (Quantify if possible)

---

## 4. Types of Problems

### Top K Problems (Amazon LOVES these)
- Top K frequent elements
- K closest points to origin
- Kth largest element in array
- Top K frequent words
- Find K pairs with smallest sums

### Two Sum Variants
- Two Sum (sorted, BST, with input constraints)
- Two Sum — less than K, closest
- Two Sum — data structure design
- Two Sum — unique pairs

### BST Operations
- Validate BST
- Lowest common ancestor in BST
- Convert sorted array to BST
- BST iterator
- Delete node in BST

### OOP Design
- Design a parking lot
- Design Amazon Locker
- Design a restaurant reservation system
- Design a vending machine
- Design a file system

### LRU Cache
Amazon asks this or LFU cache in almost every interview cycle.

---

## 5. Example Problems with Approaches

### Problem 1: Top K Frequent Elements
**Problem:** Return k most frequent elements.

**Approach (0):** HashMap for frequency + Min Heap of size K (O(n log k))
**Approach (1):** Bucket sort using frequency array (O(n)) — preferred for interviews

```java
public int[] topKFrequent(int[] nums, int k) {
    // Frequency count
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

    // Bucket sort by frequency
    List<Integer>[] buckets = new List[nums.length + 1];
    for (int key : freq.keySet()) {
        int f = freq.get(key);
        if (buckets[f] == null) buckets[f] = new ArrayList<>();
        buckets[f].add(key);
    }

    // Gather top K
    int[] result = new int[k];
    int idx = 0;
    for (int f = buckets.length - 1; f >= 0 && idx < k; f--) {
        if (buckets[f] != null) {
            for (int n : buckets[f]) {
                result[idx++] = n;
                if (idx == k) break;
            }
        }
    }
    return result;
}
```

### Problem 2: Product of Array Except Self
**Problem:** Return array where result[i] = product of all elements except nums[i]. Without division.

**Approach:** Left pass (products of left elements), Right pass (multiply by products of right elements).

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    result[0] = 1;
    for (int i = 1; i < n; i++) result[i] = result[i-1] * nums[i-1];
    int right = 1;
    for (int i = n-1; i >= 0; i--) {
        result[i] *= right;
        right *= nums[i];
    }
    return result;
}
```

### Problem 3: Copy List with Random Pointer
**Problem:** Deep copy a linked list where each node has a random pointer.

**Approach:** Three passes: (1) interleave copies, (2) set random pointers, (3) separate lists.
```java
public Node copyRandomList(Node head) {
    if (head == null) return null;
    // Pass 1: Create interleaved copies
    Node curr = head;
    while (curr != null) {
        Node copy = new Node(curr.val);
        copy.next = curr.next;
        curr.next = copy;
        curr = copy.next;
    }
    // Pass 2: Set random pointers for copies
    curr = head;
    while (curr != null) {
        if (curr.random != null) curr.next.random = curr.random.next;
        curr = curr.next.next;
    }
    // Pass 3: Separate lists
    curr = head;
    Node dummy = new Node(0), copyCurr = dummy;
    while (curr != null) {
        copyCurr.next = curr.next;
        copyCurr = copyCurr.next;
        curr.next = curr.next.next;
        curr = curr.next;
    }
    return dummy.next;
}
```

### Problem 4: Number of Islands
**Problem:** Count islands in a binary matrix.

**Approach:** DFS/BFS on each '1', mark visited by setting to '0'.
```java
public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++)
        for (int j = 0; j < grid[0].length; j++)
            if (grid[i][j] == '1') { count++; dfs(grid, i, j); }
    return count;
}
void dfs(char[][] grid, int i, int j) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] == '0') return;
    grid[i][j] = '0';
    dfs(grid, i+1, j); dfs(grid, i-1, j);
    dfs(grid, i, j+1); dfs(grid, i, j-1);
}
```

---

## 6. Bar Raiser Round

### What is the Bar Raiser?
- The Bar Raiser is an experienced interviewer from outside the hiring team
- Their role: ensure the candidate meets Amazon's hiring bar
- They have VETO power — can reject even if all others say yes
- Usually the most challenging round

### What to Expect
- **Harder coding problem** than other rounds
- **Deep LP probing** (every answer gets follow-ups)
- They will challenge your answers — they want to see how you handle pushback
- Often a system design or OOP design question
- "Why Amazon?" and "Why should we hire you?" are common

### How to Prepare
- Have 3-4 strong STAR stories that cover multiple LPs
- Practice explaining design trade-offs clearly
- Show "Amazon-ness": customer focus, ownership, high standards
- Be humble but confident about your achievements
- Quantify everything: "Improved X by Y%"

---

## 7. Preparation Strategy

### Timeline: 8-10 weeks

**Weeks 1-3: Fundamentals + LP Stories**
- Review all data structures
- Write 12-15 STAR stories covering 8-10 LPs
- Practice 2-3 LeetCode easy/medium daily

**Weeks 4-6: Amazon Patterns**
- Focus on arrays, strings, trees, heaps
- Solve Amazon-tagged problems (last 6 months)
- Practice OOP design (parking lot, vending machine, etc.)
- 3-4 problems daily

**Weeks 7-8: System Design**
- Design Uber, Amazon, Twitter, TinyURL
- Review scalability concepts (sharding, caching, CDN, etc.)
- Practice explaining trade-offs

**Weeks 9-10: Mocks + LP Integration**
- Full mock interviews with LP integration
- Practice answering LP questions using STAR
- Review weakest topics
- 2-3 complete mock rounds

### Must-Solve Amazon Problems
- Two Sum (all variants)
- Top K Frequent Elements
- LRU Cache
- Number of Islands
- Product of Array Except Self
- Copy List with Random Pointer
- Merge Two Sorted Lists
- Binary Tree Zigzag Level Order
- Most Common Word
- Critical Connections in a Network

### Common Amazon LP Questions
- "Tell me about a time you went above and beyond"
- "Describe a conflict with a team member"
- "Tell me about a time you failed"
- "Describe a time you had to make a decision with incomplete data"
- "Tell me about a time you innovated"
- "Give an example of when you disagreed with a decision"
