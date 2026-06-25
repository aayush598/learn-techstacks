# Page Replacement: Optimal (OPT/MIN)

## Algorithm

- **Replace the page that will not be used for the *longest* time in the future**
- Also called **Belady's Optimal Algorithm**, **MIN**
- Gives the **lowest possible page fault rate** for any reference string
- Serves as a **benchmark** for evaluating other algorithms

### Example

```
Reference string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0
Frames = 3

7    0    1    2    0    3    0    4    2    3    0
7    0    1    2    2    2    0    4    2    2    0
     7    0    1    1    1    2    0    4    2    3
          7    0    0    3    1    2    0    4    2

Faults: 7, 0, 1, 2, 3, 0, 4, 0 → 8 faults (with 3 frames)
```

Compare: FIFO gave 10 faults for same string → OPT is 20% better here

## How It Works

- At page fault time, examine all pages in memory
- Look forward in the reference string
- Pick the page whose **next reference is farthest in the future**
- If a page is **never referenced again** → optimal to evict it

## Properties

| Property | Value |
|---|---|
| **Belady's anomaly?** | No (has stack property) |
| **Stack property?** | Yes |
| **Implementable?** | No (needs future knowledge) |
| **Performance** | Best possible (theoretical maximum) |
| **Use case** | Benchmark for LRU, Clock, etc. |

## Practical Usage

- **Cannot be implemented** in real systems (OS cannot see into the future)
- Used in research and simulation to measure **optimal performance**
- The **gap** between an algorithm's performance and OPT = optimization opportunity
- LRU approximates OPT well in practice (uses past as predictor of future)

## Intuition

- OPT knows what program will do next → unfair advantage
- But it establishes a theoretical **lower bound** on page faults
- If LRU gives 10 faults and OPT gives 8 → LRU is 25% above optimal
- If Clock gives 14 faults → Clock has more room for improvement
