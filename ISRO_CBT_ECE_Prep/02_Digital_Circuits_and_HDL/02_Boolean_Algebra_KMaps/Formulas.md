# Boolean Algebra and K-Maps - Formulas

## De Morgan's Laws
```
(A + B)' = A' . B'
(A . B)' = A' + B'
Extended: (A+B+C+...)' = A' . B' . C' . ...
Extended: (A.B.C...)' = A' + B' + C' + ...
```

## Boolean Algebra Identities
```
A + 0 = A          A . 0 = 0
A + 1 = 1          A . 1 = A
A + A = A          A . A = A
A + A' = 1         A . A' = 0
(A')' = A
A + AB = A         A(A+B) = A (Absorption)
A + A'B = A + B    A(A'+B) = AB
```

## Consensus Theorem
```
AB + A'C + BC = AB + A'C
(BC is the consensus term - redundant)
Dual: (A+B)(A'+C)(B+C) = (A+B)(A'+C)
```

## Shannon's Expansion Theorem
```
f(A,B,C,...) = A . f(1,B,C,...) + A' . f(0,B,C,...)
```

## Minterm and Maxterm Relationships
```
f(A,B,C) = Sigma m(0,1,3,5,7) = Pi M(2,4,6)
Complement: f' = Sigma m(remaining) = Pi M(included)
```

## K-Map Simplification Rules
```
Number of variables = n
Number of cells = 2^n
Group sizes: 1, 2, 4, 8, 16, ... (powers of 2)
Eliminated variables per group of size 2^k: k variables eliminated

Example: Group of 8 in 4-variable K-map eliminates 3 variables
```

## Quick Conversion (SOP to POS)
```
SOP: f = Sigma m(0,1,3,5,7)
POS: f = Pi M(2,4,6) [remaining minterms become maxterms]
```

## NAND/NOR Implementation
```
Any SOP can be implemented with 2-level NAND gates
Any POS can be implemented with 2-level NOR gates
Double negation: A = ((A')') 
```
