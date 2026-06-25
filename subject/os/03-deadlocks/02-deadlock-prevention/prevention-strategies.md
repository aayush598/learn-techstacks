# Deadlock Prevention

## Strategy: Break One of the 4 Conditions

### 1. Break Mutual Exclusion
- Make resources **sharable** whenever possible
- **Problem**: some resources are inherently non-sharable (printer, tape drive)
- **Limited applicability** — not always feasible

### 2. Break Hold & Wait
- Option A: Process requests **all resources at once** before execution
- Option B: Process releases all resources before requesting new ones
```c
// Before execution
request(R1, R2, R3);
// use resources
release(R1, R2, R3);
```
- **Problems**: low utilization, **starvation** (never gets all resources), inefficient

### 3. Break No Preemption
- If a process holding resources can't get a new one → it must **release all held resources**
- Resources added to list of things to request later
- **Problems**: expensive context saving/restoring, may not work for all resource types
```c
// Example: preempt CPU register state — very costly
```

### 4. Break Circular Wait — **Most Practical**
- Impose **total order** on all resource types
- Process can only request resources in **increasing order**
```c
// Order: R < S < T
// Correct:
request(R);
request(S);
request(T);
release(T);
release(S);
release(R);

// Wrong (could cause circular wait):
request(S);
request(R);  // requesting lower-numbered resource
```

### Proof of Correctness
- Suppose circular wait exists: P₀ → R₁ → P₁ → R₂ → ... → Rₖ → P₀
- Since P₀ waits for R₁ held by P₁, and P₁ waits for R₂...
- By ordering rule: R₁ < R₂ < ... < Rₖ < R₁ → contradiction
- Therefore circular wait cannot form

### Trade-off Summary
| Condition Broken | Pros | Cons |
|-----------------|------|------|
| Mutual Exclusion | Simple | Not always possible |
| Hold & Wait | Easy to implement | Low utilization, starvation |
| No Preemption | No starvation | Expensive, not always possible |
| Circular Wait | Practical, high utilization | Must know resource order |
