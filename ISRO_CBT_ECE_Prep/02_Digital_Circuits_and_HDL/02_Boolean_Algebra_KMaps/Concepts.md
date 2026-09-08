# Boolean Algebra and K-Maps - Concepts

## Boolean Algebra Fundamentals

### Basic Operations
- **AND (.)**: Output 1 only if both inputs are 1
- **OR (+)**: Output 1 if at least one input is 1
- **NOT (')**: Complement of input

### Boolean Theorems (Single Variable)
```
A + 0 = A        A . 0 = 0
A + 1 = 1        A . 1 = A
A + A = A        A . A = A
A + A' = 1       A . A' = 0
(A')' = A
```

### De Morgan's Laws (CRITICAL for ISRO)
```
(A + B)' = A' . B'    "NOR = bubbled AND"
(A . B)' = A' + B'    "NAND = bubbled OR"
```

### Consensus Theorem
```
AB + A'C + BC = AB + A'C
(Remove the consensus term BC)
```

---

## Karnaugh Maps (K-Maps)

### 2-Variable K-Map
```
    B=0  B=1
A=0 | m0 | m1 |
A=1 | m2 | m3 |
```

### 3-Variable K-Map (Gray Code ordering)
```
      BC=00  BC=01  BC=11  BC=10
A=0  | m0  | m1  | m3  | m2  |
A=1  | m4  | m5  | m7  | m6  |
```

### 4-Variable K-Map
```
        CD=00  CD=01  CD=11  CD=10
AB=00  | m0  | m1  | m3  | m2  |
AB=01  | m4  | m5  | m7  | m6  |
AB=11  | m12 | m13 | m15 | m14 |
AB=10  | m8  | m9  | m11 | m10 |
```

### K-Map Grouping Rules
1. Group 1s (for SOP) or 0s (for POS)
2. Groups must be powers of 2: 1, 2, 4, 8, 16
3. Groups must be rectangular
4. Groups can wrap around edges
5. Groups can overlap
6. Make groups as large as possible
7. Every 1 must be in at least one group
8. Use minimum number of groups

### Don't Care Conditions (X)
- Can be treated as 0 or 1 (whichever gives simpler expression)
- Circle only if they help make larger groups

---

## Sum of Products (SOP) vs Product of Sums (POS)
- **SOP**: OR of AND terms (standard form: Y = AB + CD)
- **POS**: AND of OR terms (standard form: Y = (A+B)(C+D))
- **Canonical SOP**: Every term contains ALL variables (minterms)
- **Canonical POS**: Every term contains ALL variables (maxterms)
- Minterm: Product term with all variables (e.g., A'B'C)
- Maxterm: Sum term with all variables (e.g., A+B+C')

---

## ISRO Key Points
- De Morgan's laws are the most tested concept
- K-map with don't cares can dramatically simplify
- Gray code ordering ensures adjacent cells differ by one bit
- SOP from 1s, POS from 0s
- Consensus theorem shortcut: remove redundant term
