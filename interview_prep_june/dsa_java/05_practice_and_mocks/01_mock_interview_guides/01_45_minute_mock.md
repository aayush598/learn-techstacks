# 45-Minute Mock Interview Guide

## Format

Standard onsite round (virtual or in-person):
- 1 hard problem or 2 medium problems
- 45 minutes

## Time Breakdown

| Phase | Time | Activity |
|-------|------|----------|
| Clarify | 3-5 min | Restate, ask questions, edge cases |
| Examples | 2-3 min | Walk through examples |
| Brute Force | 5 min | Propose and analyze brute force |
| Optimize | 10 min | Brainstorm improvements, arrive at optimal |
| Code | 15 min | Write clean code with good structure |
| Test | 5 min | Trace examples, edge cases, fix bugs |
| Analyze | 2-5 min | Time/space, trade-offs, follow-ups |

## Optimal Strategy

### Phase 1: Clarify (3-5 min)
- Restate the problem in your own words
- Ask about: input size, data types, duplicates, negatives
- Ask about: time/space priorities

### Phase 2: Brute Force to Optimal (15 min)
- Start with simple solution
- Identify bottlenecks
- Walk through optimization steps
- Explain WHY the optimal approach works

### Phase 3: Code (15 min)
- **Write clean code**: meaningful variable names, helper methods
- Write incrementally, not all at once
- Handle edge cases inline
- Talk through while writing

### Phase 4: Test & Analyze (10 min)
- Trace the example step by step
- Test edge cases: empty, single, duplicates
- Analyze: O(time), O(space)
- Discuss trade-offs if any

## Example: "Longest Substring Without Repeating Characters"

**Clarify**: Only lowercase? ASCII? Characters or bytes? Case-sensitive?

**Brute Force**: Check every substring O(n³)
```
for(i=0..n) for(j=i..n) checkUnique(s,i,j) → O(n²) × O(n) = O(n³)
```

**Optimize**: Sliding window with HashSet
```
Left=0, right expands, when duplicate found shrink left.
Optimize further: HashMap stores last position → jump left directly.
O(n) time, O(min(m,n)) space.
```

**Code**: Write clean implementation

**Test**: "abcabcbb" → 3, "bbbbb" → 1, " " → 1, "" → 0
