# Signal Flow Graphs - Formulas

## Mason's Gain Formula
```
T(s) = Sum[k] (Pk * Delta_k) / Delta

Delta = 1 - Sum La + Sum Lb Lc - Sum Ld Le Lf + ...
  (single loops)  (2 nontouching)  (3 nontouching)
  signs alternate: -, +, -, ...

Delta_k = Delta with loops touching forward path k eliminated
```

## Example
```
Loop gains: L1=G1H1, L2=G2H2, L3=G1G2H3 (for illustration)
  Actually compute individual loops.
  
Consider 2 non-touching loops L1, L2:
  Delta = 1 - (L1+L2) + (L1*L2)
Forward path P1 touches L1 and L2:
  Delta_1 = 1
Forward path P2 touches only L1:
  Delta_2 = 1 - L2
T = (P1*1 + P2*(1-L2)) / (1 - L1 - L2 + L1L2)
```

## Common Structures
```
Unity feedback: C/R = G/(1+GH)
  G = forward (controller+plant)
  H = feedback gain
  GH = loop gain
Closed loop = forward gain/(1 + loop gain) [for negative feedback]
```

## Reduction Rules (block diagram)
```
Cascade: G1*G2
Parallel: G1+G2
Feedback: G/(1+GH)
Shifting branch points / summing points
```

## Quick Reference
| Symbol | Meaning |
|--------|---------|
| Pk | forward path gain k |
| Delta | 1 - sum(L1) + sum(L2) - ... |
| Delta_k | Delta minus touching loops |
| L1 | individual loop gains |
| L2 | products of 2 nontouching |
| T | transfer function |

## Non-Touching Check
```
Two loops are non-touching if they share NO NODE
A loop touches a forward path if they share any node
```
