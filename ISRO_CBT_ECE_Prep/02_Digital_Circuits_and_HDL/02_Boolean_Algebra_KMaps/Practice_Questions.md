# Boolean Algebra & K-Maps - Practice Questions (ISRO Style)

## Section A: Boolean Algebra Simplification

### Q1.
Simplify: **F = A'B'C' + A'BC' + AB'C' + ABC'**
- (a) C'
- (b) B'
- (c) A'
- (d) A'B'

**Answer:** (a) C'
**Explanation:** Group terms: A'C'(B'+B) + AC'(B'+B) = A'C' + AC' = C'(A'+A) = C'

---

### Q2.
Simplify: **F = AB + A'C + BC**
- (a) AB + A'C
- (b) AB + BC + AC
- (c) A'B + A'C
- (d) Cannot simplify further

**Answer:** (a) AB + A'C (Consensus Theorem: BC is redundant)

---

### Q3.
Which Boolean identity is used to eliminate redundant terms in combinational logic hazard-free design?
- (a) Absorption law
- (b) Consensus theorem
- (c) DeMorgan's theorem
- (d) Distributive law

**Answer:** (b) Consensus theorem — adding the consensus term eliminates static-1 hazards.

---

### Q4.
Apply DeMorgan's theorem: **(A + B'·C)'**
- (a) A'·(B + C')
- (b) A'·B'·C'
- (c) A'·(B' + C')
- (d) A' + B + C'

**Answer:** (c) A'·(B' + C')
**(A + B'C)' = A' · (B'C)' = A' · (B + C')**

---

### Q5.
The expression **A + A'B** simplifies to:
- (a) A + B
- (b) A'B
- (c) A
- (d) B

**Answer:** (a) A + B

---

## Section B: K-Map Problems

### Q6.
Simplify **F(A,B,C) = Σm(0,1,3,5)** using K-map:
- (a) A'C + B'C'
- (b) A'C + A'B' + AB'C
- (c) A'C + A'B'
- (d) B'C' + AC

**Answer:** (c) A'C + A'B'
```
K-map:          BC
              00  01  11  10
    A=0     | 1 | 1 | 1 | 0 |
    A=1     | 0 | 1 | 0 | 0 |

Group 1 (m0,m1): A'B'
Group 2 (m1,m3): A'C
```

---

### Q7.
Given **F(A,B,C,D) = Σm(0,1,2,5,8,9,10) + d(3,7,12,13)**, find minimum SOP:
- (a) A'B' + C'D' + B'D
- (b) A'B' + B'D + A'CD
- (c) A'D' + B'D + A'B'C
- (d) A'B' + C'D' + B'C

**Answer:** (a) A'B' + C'D' + B'D
Don't cares at 3,7,12,13 help form larger groups.

---

### Q8.
In a 4-variable K-map, cell **m₇** is adjacent to:
- (a) m₃, m₅, m₆, m₁₅
- (b) m₃, m₅, m₆, m₁₅
- (c) m₃, m₅, m₆, m₁₄
- (d) m₃, m₅, m₇, m₁₅

**Answer:** (a) m₃, m₅, m₆, m₁₅
m₇ (0111): adjacent cells differ by 1 bit → m₃(0011), m₅(0101), m₆(0110), m₁₅(1111)

---

### Q9.
In K-map simplification, don't care conditions:
- (a) Must always be included in groups
- (b) Must never be included in groups
- (c) Can be included or excluded to minimize the expression
- (d) Are always grouped with 1s

**Answer:** (c) — use them only when they simplify the result

---

### Q10.
The number of cells in a 5-variable K-map is:
- (a) 16
- (b) 32
- (c) 64
- (d) 25

**Answer:** (b) 32 (2⁵ = 32)

---

## Section C: Canonical Forms

### Q11.
The minterm expansion of **F = Σm(1,3,4,6)** for 3 variables is:
- (a) A'B'C + A'BC + AB'C' + ABC'
- (b) A'B'C + A'BC + AB'C' + ABC
- (c) A'BC + A'BC' + AB'C + ABC'
- (d) A'B'C + AB'C + AB'C' + ABC'

**Answer:** (a) A'B'C + A'BC + AB'C' + ABC'
m₁=001=A'B'C, m₃=011=A'BC, m₄=100=AB'C', m₆=110=ABC'

---

### Q12.
For 3-variable function **F = Σm(0,2,4,6)**, the POS form is:
- (a) (A+B+C)(A+B'+C)(A'+B+C)(A'+B'+C)
- (b) (A+B+C)(A'+B+C)(A+B'+C)(A'+B'+C)
- (c) (A+B)(A'+C)
- (d) (A+B'+C)(A'+B+C)

**Answer:** (c) (A+B)(A'+C)
0s at minterms 1,3,5,7. K-map shows groups forming (A+B) and (A'+C).

---

### Q13.
Number of literals in canonical SOP for 5 variables:
- (a) 5 per minterm
- (b) 4 per minterm
- (c) 3 per minterm
- (d) Variable

**Answer:** (a) 5 — canonical SOP always includes ALL variables in every term.

---

## Section D: Gate Implementations

### Q14.
Implement **F = AB + CD** using only NAND gates. Minimum number of NAND gates required:
- (a) 3
- (b) 4
- (c) 5
- (d) 6

**Answer:** (c) 5
AB → NAND(A,B) → NAND(NAND(A,B),NAND(A,B)) gives AB
CD → NAND(C,D) → NAND(NAND(C,D),NAND(C,D)) gives CD
AB+CD → NAND(NAND(AB,CD),NAND(AB,CD))
Actually: 2 for AB and CD, 2 for inversion, 1 for final = 5

---

### Q15.
Using DeMorgan's theorem, **(AB + CD)'** equals:
- (a) (A'+B')(C'+D')
- (b) A'B' + C'D'
- (c) A'B'C'D'
- (d) (A'+B')(C'+D') ... this is same as (a)

Wait — (AB+CD)' = (AB)'·(CD)' = (A'+B')·(C'+D')

**Answer:** (a) (A'+B')(C'+D')

---

## Section E: Advanced Concepts

### Q16.
A static-1 hazard occurs in:
- (a) SOP circuits during input transitions
- (b) POS circuits during input transitions
- (c) Both SOP and POS circuits
- (d) Sequential circuits only

**Answer:** (a) SOP circuits — when one input variable changes, the output momentarily goes to 0 before returning to 1.

---

### Q17.
The consensus term in **AB + A'C** is:
- (a) BC
- (b) A'B
- (c) AC
- (d) A'C

**Answer:** (a) BC — it's the product of the remaining literals from both terms.

---

### Q18.
How many prime implicants exist for **F(A,B,C) = Σm(0,1,2,4)**?
- (a) 2
- (b) 3
- (c) 4
- (d) 5

**Answer:** (b) 3
```
K-map:          BC
              00  01  11  10
    A=0     | 1 | 1 | 0 | 1 |
    A=1     | 1 | 0 | 0 | 0 |

PIs: A'B' (m0,m1), A'C' (m0,m2), B'C' (m0,m4)
```

---

### Q19.
**F = (A+B)(A+C)** in SOP form is:
- (a) A + BC
- (b) AB + AC
- (c) A + AC + BC
- (d) A + BC

**Answer:** (a) A + BC
Expand: AA + AC + BA + BC = A + AC + AB + BC = A(1+C+B) + BC = A + BC

---

### Q20.
For a function with 4 variables, the maximum possible number of minterms is:
- (a) 8
- (b) 12
- (c) 16
- (d) 32

**Answer:** (c) 16 = 2⁴

---

## Section F: VHDL Code Analysis (Boolean Context)

### Q21.
```vhdl
signal A, B, C, Y : std_logic;
Y <= A nand (B nand C);
```
This implements:
- (a) OR gate
- (b) AND gate
- (c) XOR gate
- (d) NOT-AND-OR

**Answer:** (a) OR gate
B nand C = (BC)' → A nand (BC)' = (A·(BC)')' = (A·A' + A·B' + A·C')' ... let's recalculate.
(A · (BC)')' = A' + (BC)' = A' + B' + C' ... no.
Actually: A nand X = (AX)' where X=(BC)'
So Y = (A·(BC)')' = A' + (BC)'' = A' + BC ... that's not OR.

Let me recalculate: Y = (A · (B nand C))' = (A · (BC)')' = A' + BC
This is not a standard gate. Let me fix the question.

**Corrected:**
```vhdl
Y <= (A nand A) nand (B nand B);
```
A nand A = A', B nand B = B'
Y = (A' · B')' = A + B → **OR gate**

**Answer:** (a) OR gate

---

### Q22.
```vhdl
signal A, B, Y : std_logic;
Y <= A xor (A nand B);
```
When A=1, B=0:
- (a) Y = 0
- (b) Y = 1
- (c) Y = Z
- (d) Y = X

**Answer:** (b) Y = 1
A nand B = (1·0)' = 1 → Y = 1 xor 1 = 0... let me recalculate.
A=1, B=0: A nand B = (1·0)' = 1' = 1
Y = 1 xor 1 = 0

Hmm, that gives 0. Let me check: A=1, B=1:
A nand B = (1·1)' = 0 → Y = 1 xor 0 = 1

Let me fix: When A=1, B=1:
- (a) Y = 0
- (b) Y = 1

**Answer:** (b) Y = 1
A nand B = 0 → Y = 1 xor 0 = 1

---

### Q23.
Using Shannon's expansion theorem, **F(A,B,C) = Σm(1,3,5,7)** expanded about variable A:
- (a) A·F(1,B,C) + A'·F(0,B,C) = A·C + A'·BC
- (b) A·F(1,B,C) + A'·F(0,B,C) = A·(B⊕C) + A'·(BC)
- (c) A·C + A'·BC
- (d) Both (a) and (c)

**Answer:** (d) — F(1,B,C) for minterms 5,7: C. F(0,B,C) for minterms 1,3: BC.

---

### Q24.
```vhdl
signal sel : std_logic_vector(1 downto 0);
signal out : std_logic;
with sel select
    out <= '1' when "00",
           '0' when "01",
           '1' when "10",
           '0' when others;
```
This circuit is equivalent to:
- (a) XOR gate
- (b) XNOR gate
- (c) NAND gate
- (d) OR gate

**Answer:** (b) XNOR gate
sel=00→1, sel=01→0, sel=10→1, sel=11→0
For sel={A,B}: out=1 when A=B → XNOR

---

### Q25.
The minimum number of 2-input NAND gates to implement **F = A ⊕ B**:
- (a) 3
- (b) 4
- (c) 5
- (d) 6

**Answer:** (b) 4
A ⊕ B = AB' + A'B. Requires 4 NAND gates.

---

## Section F: Numerical Problems

### Q26.
A Boolean function has 5 variables. What is the size of its K-map?
- (a) 16 cells
- (b) 32 cells
- (c) 64 cells
- (d) 128 cells

**Answer:** (b) 32 = 2⁵

---

### Q27.
For **F(A,B,C) = Σm(0,7)**, the minimum SOP is:
- (a) A'B'C' + ABC
- (b) (A ⊕ B ⊕ C)' ... wait, that's for m0,m3,m5,m6
- (c) A'B'C' + ABC (already minimum)
- (d) Both (a) and (c)

**Answer:** (c) A'B'C' + ABC — no further simplification possible since m0 and m7 are not adjacent.

---

### Q28.
How many essential prime implicants does **F(A,B,C) = Σm(0,1,4,5)** have?
- (a) 1
- (b) 2
- (c) 3
- (d) 4

**Answer:** (b) 2
```
K-map:
      BC
    00  01  11  10
A=0 | 1 | 1 | 0 | 0 |
A=1 | 1 | 1 | 0 | 0 |
```
Both PIs (A'B' and AB')... actually group m0,m1,m4,m5 = B' (1 essential PI)
Wait: m0=000, m1=001, m4=100, m5=101 → all have B'=1 and C varies
Group of 4: B'C' ... no. m0=000, m1=001, m4=100, m5=101
In K-map: cells 0,1 (row 0) and 4,5 (row 1) → column 00 and 01 → B' (B=0)
So F = B'. Only 1 essential PI.

**Answer:** (a) 1

---

### Q29.
**F = (A+B+C)(A+B+C')(A+B'+C)(A'+B+C)** in minterm notation:
- (a) ΠM(0,1,2,4)
- (b) Σm(3,5,6,7)
- (c) Σm(3,5,6,7) ... same as (b)
- (d) Σm(0,1,2,4)

**Answer:** (b) Σm(3,5,6,7)
M₀=(000)→(A+B+C), M₁=(001)→(A+B+C'), M₂=(010)→(A+B'+C), M₄=(100)→(A'+B+C)
Σm(0,1,2,4) are the zeros, so function = 1 at minterms 3,5,6,7.

---

### Q30.
The literal count in the minimized SOP **F = AB + A'CD + BC'D'** is:
- (a) 7
- (b) 8
- (c) 9
- (d) 10

**Answer:** (b) 8
AB=2, A'CD=3, BC'D'=3 → total = 2+3+3 = 8
