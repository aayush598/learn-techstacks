# Deadlock Detection Algorithms

## Single Instance per Resource — Wait-For Graph

### RAG → WFG Conversion
- Remove resource nodes
- Edge P₁ → P₂ if P₁ is waiting for a resource held by P₂

```
RAG:  P₁ → R₁ → P₂ → R₂ → P₁
WFG:  P₁ → P₂ → P₁  (cycle → deadlock)
```

### Cycle Detection
- **DFS** from each node: O(n²) where n = number of processes
- Maintain 3 states: **White** (unvisited), **Gray** (in current DFS stack), **Black** (finished)
- If we find a **Gray** node → cycle detected
- **Optimization**: Tarjan's algorithm O(V+E)

## Multiple Instances — Detection Algorithm
```
Work[m] = Available[m]
Finish[n] = FALSE for all processes
For i where Allocation[i] != 0: Finish[i] = FALSE
For i where Allocation[i] == 0: Finish[i] = TRUE

Find i where Finish[i] == FALSE && Request[i] <= Work
If found: Work += Allocation[i]; Finish[i] = TRUE; repeat
If any Finish[i] == FALSE → deadlocked
```

### Example
```
Available = (0, 0, 0)
          Allocation    Request
          A  B  C     A  B  C
P0        0  1  0     0  0  0
P1        2  0  0     2  0  2
P2        3  0  3     0  0  0
P3        2  1  1     1  0  0
P4        0  0  2     0  0  2
```
- P0: Request=(0,0,0) → Work=(0,1,0); Finish[0]=TRUE
- P2: Request=(0,0,0) → Work=(3,1,3); Finish[2]=TRUE
- P3: Request=(1,0,0) ≤ Work(3,1,3) → Work=(5,2,4); Finish[3]=TRUE
- P1 and P4 remain unfinished → **deadlocked** {P1, P4}

## How Often to Detect
| Approach | Pros | Cons |
|----------|------|------|
| **On every request** | Instant detection | High overhead |
| **Periodic** (e.g., every hour) | Low overhead | Deadlock may persist unnoticed |
| **On CPU usage drop** | Detects process starvation | False positives |
