# Boolean Algebra and Logic Gates

## 1. Introduction to Boolean Algebra

Boolean algebra is the mathematical foundation of digital logic design. Developed by George Boole in 1854 and later applied to circuit design by Claude Shannon in 1937, it provides the formal framework for analyzing and designing binary digital systems.

### 1.1 Boolean Variables and Constants

In Boolean algebra, variables can take only two values:

| Symbol | Meaning |
|--------|---------|
| 0 | Logic FALSE, Low, Off |
| 1 | Logic TRUE, High, On |

### 1.2 Fundamental Operations

The three fundamental Boolean operations are:

#### AND Operation (Conjunction)
```
A · B = Y

Truth Table:
A | B | Y
--|---|--
0 | 0 | 0
0 | 1 | 0
1 | 0 | 0
1 | 1 | 1
```

Mathematical notation: `A ∧ B` or `A · B` or `AB`

#### OR Operation (Disjunction)
```
A + B = Y

Truth Table:
A | B | Y
--|---|--
0 | 0 | 0
0 | 1 | 1
1 | 0 | 1
1 | 1 | 1
```

Mathematical notation: `A ∨ B` or `A + B`

#### NOT Operation (Complement)
```
Ā = Y

Truth Table:
A | Y
--|--
0 | 1
1 | 0
```

Mathematical notation: `¬A` or `A'` or `Ā` or `!A`

## 2. Boolean Algebra Laws

### 2.1 Basic Laws

| Law | AND Form | OR Form |
|-----|----------|---------|
| Identity | A · 1 = A | A + 0 = A |
| Null/Annihilator | A · 0 = 0 | A + 1 = 1 |
| Idempotent | A · A = A | A + A = A |
| Inverse/Complement | A · Ā = 0 | A + Ā = 1 |
| Commutative | A · B = B · A | A + B = B + A |
| Associative | (A · B) · C = A · (B · C) | (A + B) + C = A + (B + C) |
| Distributive | A · (B + C) = A·B + A·C | A + (B · C) = (A+B) · (A+C) |

### 2.2 De Morgan's Theorems

De Morgan's theorems are crucial for logic optimization and gate-level transformations:

```
Theorem 1:  (A · B)' = A' + B'
Theorem 2:  (A + B)' = A' · B'
```

**Generalized form:**
```
(A₁ · A₂ · ... · Aₙ)' = A₁' + A₂' + ... + Aₙ'
(A₁ + A₂ + ... + Aₙ)' = A₁' · A₂' · ... · Aₙ'
```

### 2.3 Boolean Algebra Theorems

#### Absorption Theorems
```
A + A·B = A
A · (A + B) = A
```

#### Simplification Theorems
```
A + Ā·B = A + B
A · (Ā + B) = A · B
```

#### Consensus Theorem
```
A·B + Ā·C + B·C = A·B + Ā·C
```

## 3. Logic Gate Implementations

### 3.1 Basic Gates

#### Buffer
```
Symbol: A ---[>o--- Y
Function: Y = A

CMOS Implementation:
- 1 PMOS transistor (VDD to output)
- 1 NMOS transistor (output to GND)
- Actually implemented as two inverters in series
```

#### Inverter (NOT Gate)
```
Symbol: A ---|>o--- Y
Function: Y = A'

CMOS Implementation:
- 1 PMOS transistor (VDD to output, gate = A)
- 1 NMOS transistor (output to GND, gate = A)

VDD
 |
[PMOS] --- A
 |
 Y --- Output
 |
[NMOS] --- A
 |
GND
```

#### NAND Gate
```
Symbol:
A ---|\
     | >o--- Y
B ---|/

Function: Y = (A · B)'

Truth Table:
A | B | Y
--|---|--
0 | 0 | 1
0 | 1 | 1
1 | 0 | 1
1 | 1 | 0

CMOS Implementation (4 transistors):
VDD    VDD
 |      |
[PMOS]-A [PMOS]-B
 |      |
 +--Y---+
 |
[NMOS]-A
 |
[NMOS]-B
 |
GND
```

#### NOR Gate
```
Symbol:
A ---|\
     | >o--- Y
B ---|/

Function: Y = (A + B)'

Truth Table:
A | B | Y
--|---|--
0 | 0 | 1
0 | 1 | 0
1 | 0 | 0
1 | 1 | 0

CMOS Implementation (4 transistors):
VDD
 |
[NMOS]-A
 |
[NMOS]-B
 |
 +--Y---+
 |      |
[PMOS]-A [PMOS]-B
 |      |
GND    GND
```

### 3.2 Compound Gates

#### AND Gate (NAND + Inverter)
```
Function: Y = A · B
Implementation: NAND gate followed by inverter
Transistor Count: 6

A ---|\
     | >o---|>o--- Y
B ---|/
```

#### OR Gate (NOR + Inverter)
```
Function: Y = A + B
Implementation: NOR gate followed by inverter
Transistor Count: 6

A ---|\
     | >o---|>o--- Y
B ---|/
```

#### XOR Gate
```
Function: Y = A ⊕ B = A'B + AB'

Truth Table:
A | B | Y
--|---|--
0 | 0 | 0
0 | 1 | 1
1 | 0 | 1
1 | 1 | 0

CMOS Implementation Options:
1. Static CMOS: 8-12 transistors
2. Transmission gate: 4-6 transistors
3. Pass transistor logic: 4 transistors

Implementation using NAND gates:
Y = (A · (A⊕B)') · (B · (A⊕B)')'

Or using the identity:
A ⊕ B = (A + B) · (AB)'
```

#### XNOR Gate
```
Function: Y = A ⊙ B = AB + A'B'

Truth Table:
A | B | Y
--|---|--
0 | 0 | 1
0 | 1 | 0
1 | 0 | 0
1 | 1 | 1

CMOS Implementation: 8-12 transistors
```

### 3.3 Gate Equivalency Table

| Gate | NAND | NOR | AND | OR | NOT | XOR | XNOR |
|------|------|-----|-----|----|-----|-----|------|
| NAND | 1 | 2+INV | 1+INV | 2·NAND+INV | 1 | Complex | Complex |
| NOR | 2+INV | 1 | 2·NOR+INV | 1+INV | 1 | Complex | Complex |
| AND | 1+INV | 2+INV | 1 | 2+INV | - | Complex | Complex |
| OR | 2+INV | 1+INV | 2+INV | 1 | - | Complex | Complex |

## 4. Boolean Function Representation

### 4.1 Sum of Products (SOP)

A Boolean function can be expressed as an OR of AND terms:

```
F(A,B,C) = Σm(1,3,5,7)

SOP Form: F = A'B'C + A'BC + AB'C + ABC
Minimized: F = C

K-Map for F(A,B,C):
BC
A   00  01  11  10
0 |  0   1   1   0
1 |  0   1   1   0

Grouping: Column where B=1, C=1 → F = C
```

### 4.2 Product of Sums (POS)

A Boolean function can be expressed as an AND of OR terms:

```
F(A,B,C) = ΠM(0,2,4,6)

POS Form: F = (A+B+C) · (A+B'+C) · (A'+B+C) · (A'+B'+C)
Minimized: F = C

K-Map for F(A,B,C):
BC
A   00  01  11  10
0 |  0   1   1   0
1 |  0   1   1   0

Grouping: Column where C=1 → F = C
```

### 4.3 Canonical Forms Comparison

| Property | SOP (Sum of Products) | POS (Product of Sums) |
|----------|----------------------|----------------------|
| Structure | OR of AND terms | AND of OR terms |
| Implementation | AND-OR network | OR-AND network |
| Optimization target | Minimize product terms | Minimize sum terms |
| Default output | 1 | 0 |
| Best for | Sparse 1s in truth table | Sparse 0s in truth table |

## 5. Karnaugh Maps (K-Maps)

### 5.1 2-Variable K-Map

```
Variables: A, B
F(A,B) = Σm(0,1,3)

K-Map:
B
A   0   1
0 | 1 | 1 |
1 | 0 | 1 |

Groups:
- Group 1: (0,1) → A' (covers m0, m1)
- Group 2: (1,3) → B (covers m1, m3)

F = A' + B
```

### 5.2 3-Variable K-Map

```
Variables: A, B, C
F(A,B,C) = Σm(0,1,2,5,6,7)

K-Map:
BC
A   00  01  11  10
0 | 1 | 1 | 0 | 1 |
1 | 0 | 1 | 1 | 1 |

Groups:
- Group 1: (0,2,4,6) → C' (corners)
- Group 2: (1,5) → B'C
- Group 3: (6,7) → AB

F = C' + B'C + AB
```

### 5.3 4-Variable K-Map

```
Variables: A, B, C, D
F(A,B,C,D) = Σm(0,1,2,4,5,6,8,9,12,13)

K-Map:
CD
AB  00  01  11  10
00 | 1 | 1 | 0 | 1 |
01 | 1 | 1 | 0 | 1 |
11 | 0 | 0 | 0 | 0 |
10 | 1 | 1 | 0 | 0 |

Groups:
- Group 1: (0,1,4,5,8,9,12,13) → D' (large group)
- Group 2: (0,2,4,6) → A'C' (corners)
- Group 3: (0,1,2) → A'B'D' or simplified

Final: F = D' + A'C'
```

### 5.4 Don't Care Conditions

```
F(A,B,C,D) = Σm(1,3,5,7,9) + Σd(0,2,4,6,8,10)

K-Map:
CD
AB  00  01  11  10
00 | X | 1 | 1 | X |
01 | X | 1 | 1 | 0 |
11 | 0 | 0 | 0 | 0 |
10 | X | 1 | 0 | X |

Using don't cares (X) for optimization:
- Group 1: (0,1,2,3,4,5) → A' (all don't cares used)
- Group 2: (1,3,5,7) → A'D or CD'

F = A' + CD
```

## 6. Quine-McCluskey Algorithm

### 6.1 Tabular Method

For functions with many variables, the Quine-McCluskey algorithm provides a systematic approach:

```
Step 1: Group minterms by number of 1s
Step 2: Combine terms that differ by one bit
Step 3: Repeat until no more combinations possible
Step 4: Create Prime Implicant chart
Step 5: Select Essential Prime Implicants

Example: F(A,B,C,D) = Σm(0,1,2,5,6,7,8,9,10,14)

Step 1 - Grouping:
Group 0: 0000 (0)
Group 1: 0001 (1), 0010 (2), 1000 (8)
Group 2: 0101 (5), 0110 (6), 1001 (9), 1010 (10)
Group 3: 0111 (7), 1110 (14)

Step 2 - Combining:
(0,1) = 000-
(0,2) = 00-0
(1,5) = 0-01
(2,6) = 0-10
(2,10) = -010
(8,9) = 100-
(8,10) = 10-0
(5,7) = 01-1
(6,7) = 011-
(6,14) = -110
(10,14) = 101-

Step 3 - Further combining:
(0,1,8,9) = -00-
(0,2,8,10) = -0-0
(2,6,10,14) = --10

Step 4 - Prime Implicants:
PI1: -00- (covers 0,1,8,9)
PI2: -0-0 (covers 0,2,8,10)
PI3: --10 (covers 2,6,10,14)
PI4: 01-1 (covers 5,7)

Step 5 - Selection:
Essential: PI1, PI3, PI4
F = B'C' + CD' + A'BD
```

## 7. Multi-Level Logic Optimization

### 7.1 Common Subexpression Elimination

```
Before:
F = ABC + ABD + AB'C + AB'D

After CSE:
T1 = AB
F = T1·C + T1·D + T1·B'·C + T1·B'·D
F = T1·(C + D + B'·C + B'·D)
F = T1·(C + D)·(1 + B')
F = AB·(C + D)
```

### 7.2 Factorization

```
Before:
F = ABC + ABD + ABE

After Factoring:
F = AB·(C + D + E)
```

### 7.3 Functional Decomposition

```
Before:
F(A,B,C,D) = ABCD + AB'CD' + A'BCD' + A'B'CD

Decomposed:
G(A,B) = AB + A'B'
H(C,D) = CD + CD'
F = G(A,B) · H(C,D) + G'(A,B) · H'(C,D)
```

## 8. Logic Synthesis Concepts

### 8.1 Technology Mapping

```
Generic Netlist:
F = A·B + C·D

Mapped to NAND-NAND:
F = (A·B)' · (C·D)' '
F = NAND(NAND(A,B), NAND(C,D))

Mapped to NOR-NOR:
F = ((A·B)'+(C·D)')'
F = NOR(NOR(A·B)', NOR(C·D)')
F = NOR(NOR(NAND(A,B)), NOR(NAND(C,D)))
```

### 8.2 Standard Cell Libraries

| Cell Type | Transistor Count | Delay (typical) | Power |
|-----------|-----------------|-----------------|-------|
| INV | 2 | 1x | Low |
| NAND2 | 4 | 1.5x | Low |
| NOR2 | 4 | 1.5x | Low |
| AND2 | 6 | 2x | Medium |
| OR2 | 6 | 2x | Medium |
| XOR2 | 8-12 | 3x | High |
| MUX2 | 8-12 | 2.5x | Medium |
| DFF | 20-28 | 4x | High |

## 9. Verilog Implementation

### 9.1 Gate-Level Modeling

```verilog
// Basic gate implementations
module logic_gates (
    input  wire A, B,
    output wire Y_AND, Y_OR, Y_NAND, Y_NOR, Y_XOR, Y_XNOR
);

    and  gate1 (Y_AND,  A, B);
    or   gate2 (Y_OR,   A, B);
    nand gate3 (Y_NAND, A, B);
    nor  gate4 (Y_NOR,  A, B);
    xor  gate5 (Y_XOR,  A, B);
    xnor gate6 (Y_XNOR, A, B);

endmodule
```

### 9.2 Dataflow Modeling

```verilog
// Dataflow descriptions
module logic_dataflow (
    input  wire A, B,
    output wire Y_AND, Y_OR, Y_NAND, Y_NOR, Y_XOR, Y_XNOR
);

    assign Y_AND  = A & B;
    assign Y_OR   = A | B;
    assign Y_NAND = ~(A & B);
    assign Y_NOR  = ~(A | B);
    assign Y_XOR  = A ^ B;
    assign Y_XNOR = ~(A ^ B);

endmodule
```

### 9.3 Behavioral Modeling

```verilog
// Behavioral descriptions using always blocks
module logic_behavioral (
    input  wire A, B,
    output reg  Y_AND, Y_OR, Y_NAND, Y_NOR, Y_XOR, Y_XNOR
);

    always @(*) begin
        Y_AND  = A & B;
        Y_OR   = A | B;
        Y_NAND = ~(A & B);
        Y_NOR  = ~(A | B);
        Y_XOR  = A ^ B;
        Y_XNOR = ~(A ^ B);
    end

endmodule
```

### 9.4 Boolean Equation Implementation

```verilog
// Implementing complex Boolean functions
module boolean_functions (
    input  wire A, B, C, D,
    output wire F1, F2, F3
);

    // F1 = A'B + AB' (XOR)
    assign F1 = (~A & B) | (A & ~B);

    // F2 = (A + B)(C + D) (Product of Sums)
    assign F2 = (A | B) & (C | D);

    // F3 = AB + AC + BC (Majority function)
    assign F3 = (A & B) | (A & C) | (B & C);

endmodule
```

### 9.5 Testbench

```verilog
// Testbench for logic gates
module tb_logic_gates;

    reg  A, B;
    wire Y_AND, Y_OR, Y_NAND, Y_NOR, Y_XOR, Y_XNOR;

    // Instantiate DUT
    logic_gates dut (
        .A(A), .B(B),
        .Y_AND(Y_AND), .Y_OR(Y_OR),
        .Y_NAND(Y_NAND), .Y_NOR(Y_NOR),
        .Y_XOR(Y_XOR), .Y_XNOR(Y_XNOR)
    );

    // Stimulus
    initial begin
        $monitor("A=%b B=%b AND=%b OR=%b NAND=%b NOR=%b XOR=%b XNOR=%b",
                 A, B, Y_AND, Y_OR, Y_NAND, Y_NOR, Y_XOR, Y_XNOR);

        A = 0; B = 0; #10;
        A = 0; B = 1; #10;
        A = 1; B = 0; #10;
        A = 1; B = 1; #10;

        $finish;
    end

    // Optional: Generate VCD for waveform viewing
    initial begin
        $dumpfile("logic_gates.vcd");
        $dumpvars(0, tb_logic_gates);
    end

endmodule
```

## 10. Applications in Medical Implant Design

### 10.1 Low-Power Logic Design Considerations

For medical implant electronics, Boolean algebra optimization directly impacts:

```
Power Consumption: P = α · C_L · V_DD² · f

Where:
- α = switching activity factor
- C_L = load capacitance
- V_DD = supply voltage
- f = clock frequency

Optimization Strategies:
1. Reduce logic depth → lower delay → lower V_DD possible
2. Minimize switching activity → lower α
3. Reduce gate count → lower C_L
4. Gate sizing → optimize power-delay product
```

### 10.2 Reliability Considerations

```
Critical Logic Requirements for Implants:
- Error detection: Parity, CRC
- Redundancy: Triple Modular Redundancy (TMR)
- Self-checking circuits: Totally Self-Checking (TSC)

Example - TMR for critical control:
F = MAJORITY(F1, F2, F3)
F = F1·F2 + F2·F3 + F1·F3

Where F1, F2, F3 are identical logic implementations
```

## 11. Summary

| Concept | Key Points |
|---------|------------|
| Boolean Algebra | Mathematical foundation for digital logic |
| Logic Gates | Physical implementation of Boolean operations |
| K-Maps | Graphical method for minimization (up to 6 variables) |
| Quine-McCluskey | Algorithmic method for minimization |
| Logic Synthesis | Automated translation to gate-level netlists |
| Optimization | Reduces area, power, and delay |
| Medical Implants | Requires ultra-low-power, high-reliability design |

## 12. Exercises

1. Minimize F(A,B,C,D) = Σm(0,1,2,5,8,9,10) using K-Maps
2. Prove De Morgan's theorem using truth tables
3. Implement F = A⊕B using only NAND gates
4. Convert the following to POS form: F = A'B + AC
5. Design a 4-input majority function using minimal gates
6. Verify the consensus theorem: AB + A'C + BC = AB + A'C
7. Implement a 2:1 multiplexer using Boolean equations and verify with Verilog
8. Optimize for power: Compare static CMOS vs pass-transistor XOR implementations
