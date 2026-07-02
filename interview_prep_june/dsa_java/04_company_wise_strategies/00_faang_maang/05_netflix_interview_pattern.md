# Netflix Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Netflix Culture (Freedom and Responsibility)
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Culture fit discussion
- Background and experience review
- Determine leveling (IC4-IC7)

### Technical Phone Screen (45-60 min)
- 1-2 coding problems
- Usually algorithm/data structure focused
- May include system design for senior roles

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (1-2): DSA problems
- **System Design** (1): Usually for senior+ roles
- **Behavioral / Culture** (1): Deep dive into Netflix culture fit
- **Hiring Manager** (1): Overview, team fit, projects

### Key Differences
- Netflix has the most senior-heavy engineering team (mostly IC4+)
- Culture fit is EXTREMELY important — they reject strong engineers who don't fit
- No standard framework — they expect you to be autonomous
- Compensation is all cash (base salary, no RSUs)
- They hire for specific teams, not general headcount

---

## 2. Most Asked Topics

| Topic | Frequency | Notes |
|-------|-----------|-------|
| System Design | Very High | Streaming, CDN, recommendation |
| Arrays & Strings | High | General DSA foundation |
| HashMaps | Medium | Lookup optimization |
| Trees | Medium | Content hierarchy, metadata |
| Graphs | Medium | Content delivery, routing |
| DP / Greedy | Low-Medium | Optimization, scheduling |
| Concurrency | Medium | High-volume streaming |

### Topic Frequency Graph
```
Sys Design: ████████████████████
Arrays:     ██████████████
Hash:       ██████████
Trees:      ██████████
Graphs:     ██████████
DP:         ██████
Concurr:    ██████
```

### Why Less DSA than Other FAANG?
- Netflix values pragmatic engineering judgment over algorithmic trivia
- They'd rather discuss trade-offs and design than optimal binary search
- But they still ask DSA — just fewer rounds than Google or Amazon

---

## 3. Netflix Culture (Freedom and Responsibility)

### Key Principles

| Principle | Meaning | Interview Impact |
|-----------|---------|-----------------|
| **Freedom and Responsibility** | You're given autonomy, but expected to deliver | Show self-direction, decision-making |
| **Context, not Control** | Leaders provide context, not micromanagement | Show you can work independently |
| **Highly Aligned, Loosely Coupled** | Aligned on goals, independent execution | Show collaboration + ownership |
| **Curious, Not Judgmental** | Learn from mistakes, no blame culture | Show growth mindset |
| **Communicate Clearly** | Speak your mind, say what you think | Be direct and honest in interviews |
| **Strong Opinions, Weakly Held** | Have opinions but be open to being wrong | Show confidence + humility |
| **Inclusion** | Diverse perspectives make better products | Show respect for different views |

### Culture Fit Questions
- "Tell me about a time you disagreed with your manager"
- "Describe a project where you had complete ownership"
- "What would you do if you saw a teammate making a mistake?"
- "How do you handle ambiguity?"
- "Tell me about a time you gave direct feedback to someone"

---

## 4. Types of Problems

### System Design (Heavy)
- Design Netflix (content delivery, recommendation)
- Design a video streaming platform
- Design a content recommendation engine
- Design a global CDN
- Design a billing/usage tracking system

### Algorithm Problems
- **Arrays/strings** — parsing, searching, sorting
- **HashMaps** — data aggregation, frequency analysis
- **Interval problems** — scheduling, overlap detection
- **Top K / Frequency** — trending content, popularity

### Practical Engineering
- "How would you debug a production issue with video buffering?"
- "How would you A/B test a new recommendation algorithm?"
- "How would you monitor system health across regions?"

---

## 5. Example Problems

### Problem 1: Design a Content Recommendation API
**Problem:** Design an API that returns recommended content for a user.

**Approach discussion:**
- Data sources: user history, ratings, demographics, trending
- ML model integration (collaborative filtering, content-based)
- Caching strategy: precompute top-N for each user segment
- Serving: latency < 100ms, handle 100K QPS
- Fallback: trending content when user data is sparse

### Problem 2: Top K Frequently Watched Shows
**Problem:** Find top K shows in the last hour from streaming logs.

**Approach:** HashMap + Min-Heap or Count-Min Sketch for approximate.
```java
public List<String> topKShows(String[] stream, int k) {
    Map<String, Integer> freq = new HashMap<>();
    for (String show : stream) freq.put(show, freq.getOrDefault(show, 0) + 1);
    PriorityQueue<Map.Entry<String, Integer>> pq = new PriorityQueue<>(
        (a, b) -> a.getValue() - b.getValue()
    );
    for (Map.Entry<String, Integer> e : freq.entrySet()) {
        pq.offer(e);
        if (pq.size() > k) pq.poll();
    }
    List<String> result = new ArrayList<>();
    while (!pq.isEmpty()) result.add(pq.poll().getKey());
    Collections.reverse(result);
    return result;
}
```

### Problem 3: Longest Consecutive Sequence in Ratings
**Problem:** Given unsorted array of ratings, find longest consecutive sequence.

**Approach:** HashSet for O(1) lookup.
```java
public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int n : nums) set.add(n);
    int longest = 0;
    for (int n : set) {
        if (!set.contains(n - 1)) { // start of a sequence
            int len = 1;
            while (set.contains(n + len)) len++;
            longest = Math.max(longest, len);
        }
    }
    return longest;
}
```

---

## 6. Preparation Strategy

### Focus Areas

1. **System Design (60% of prep time)**
   - Streaming systems, CDN, load balancing
   - Caching strategies (CDN, edge, local)
   - Data pipelines (Kafka, Spark)
   - Recommendation systems (collaborative filtering)

2. **DSA Fundamentals (30% of prep time)**
   - Arrays, strings, hash tables
   - Trees and graph basics
   - Custom data structure design
   - Algorithm complexity analysis

3. **Culture / Behavioral (10% of prep time)**
   - Prepare stories showing ownership and autonomy
   - Practice giving honest, constructive feedback examples
   - Show curiosity and learning mindset

### Netflix-Specific Tips
1. **Emphasize engineering judgment** — Not just "what" but "why" and "trade-offs"
2. **Be candid** — Say what you actually think, not what you think they want to hear
3. **Show ownership** — Example of taking complete responsibility for a project
4. **Prepare for ambiguity** — They don't spoon-feed requirements; expect vague problems
5. **No LeetCode grinding** — Focus on real-world engineering problems
6. **Read the culture memo** — Netflix's culture deck is famous; reference it naturally
