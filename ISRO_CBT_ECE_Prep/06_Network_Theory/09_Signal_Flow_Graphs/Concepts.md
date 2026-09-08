# Signal Flow Graphs and Mason's Gain - Concepts

## Signal Flow Graph (SFG)
- Graphical representation of linear system equations
- Nodes represent variables
- Directed branches represent transfer (gain)
- Arrows show signal flow direction

## Basic Elements
- **Node**: variable (e.g., V1)
- **Branch**: line with gain, direction arrow
- **Source node**: only outgoing branches
- **Sink node**: only incoming branches
- **Path**: continuous sequence of branches in direction
- **Loop**: path that returns to starting node (no node repeated)
- **Forward path**: from source to sink, no node repeated
- **Loop gain**: product of branch gains in a loop

## Terms
| Term | Meaning |
|------|---------|
| Forward path | Source->sink path |
| Forward path gain | product of its branch gains |
| Loop | closed path |
| Loop gain | product of gains in loop |
| Non-touching loops | share no node |
| Non-touching loop & path | share no node |
| Nontouching definitions matter for Mason's |

## Mason's Gain Formula
```
T = (Sum over forward paths Pk * Delta_k) / Delta

Delta = 1 - Sum(L1) + Sum(L2) - Sum(L3) + ...
  L1 = all individual loop gains
  L2 = product of gains of 2 NON-TOUCHING loops
  L3 = product of 3 non-touching loops
  ...signs alternate

Delta_k = Delta with all loops touching forward path Pk removed
```

## Application
- Transfer function of feedback control systems
- Electronic networks
- Relates to block diagram reduction

## Key Steps
1. Identify forward paths and their gains
2. Identify all loops and their gains
3. Compute Delta (alternating sums of non-touching loop products)
4. For each forward path, compute Delta_k (exclude touching loops)
5. Apply formula

---

## ISRO Key Points
- Delta = 1 - Sum(loops) + Sum(2 nontouch) - Sum(3 nontouch) + ...
- Delta_k: remove loops touching forward path k
- Mason's computes transfer function of SFG
- Non-touching means no common node
