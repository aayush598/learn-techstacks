# Combinational Logic Circuits

## 1. Introduction to Combinational Logic

Combinational logic circuits are digital circuits where the output depends only on the current inputs, not on any previous input states. Unlike sequential logic, there is no memory or feedback in combinational circuits.

### 1.1 Characteristics of Combinational Circuits

| Property | Description |
|----------|-------------|
| Memory | No memory elements (flip-flops/latches) |
| Feedback | No feedback paths from output to input |
| Timing | Output responds to input changes after propagation delay |
| State | No internal state; output is pure function of inputs |
| Examples | Adders, multiplexers, decoders, encoders |

### 1.2 General Model

```
Inputs (n bits) → [Combinational Logic] → Outputs (m bits)

Formal definition:
Y(t) = F(X(t))

Where:
- X(t) = input vector at time t
- Y(t) = output vector at time t
- F = Boolean function mapping
```

## 2. Basic Combinational Building Blocks

### 2.1 Binary Adders

#### Half Adder
```
Truth Table:
A | B | Sum | Carry
--|---|-----|------
0 | 0 |  0  |  0
0 | 1 |  1  |  0
1 | 0 |  1  |  0
1 | 1 |  0  |  1

Boolean Equations:
Sum   = A ⊕ B = A'B + AB'
Carry = A · B

Gate Implementation:
- Sum:   1 XOR gate (or 2 AND + 1 OR + 2 NOT)
- Carry: 1 AND gate
- Total: 5 gates minimum (NAND-NAND implementation)
```

#### Full Adder
```
Truth Table:
A | B | Cin | Sum | Cout
--|---|-----|-----|-----
0 | 0 |  0  |  0  |  0
0 | 0 |  1  |  1  |  0
0 | 1 |  0  |  1  |  0
0 | 1 |  1  |  0  |  1
1 | 0 |  0  |  1  |  0
1 | 0 |  1  |  0  |  1
1 | 1 |  0  |  0  |  1
1 | 1 |  1  |  1  |  1

Boolean Equations:
Sum   = A ⊕ B ⊕ Cin
Cout  = A·B + Cin·(A ⊕ B) = AB + ACin + BCin

Gate-Level Implementation:
Sum:  2 XOR gates, OR gate
Cout: 2 AND gates, 1 OR gate
Total: 9 gates, 28 transistors (static CMOS)
```

#### Ripple Carry Adder (RCA)
```
4-bit RCA Structure:
A3 B3      A2 B2      A1 B1      A0 B0
 |  |       |  |       |  |       |  |
[FA3]←C3←[FA2]←C2←[FA1]←C1←[FA0]←C0=0
 |         |         |         |
 S3        S2        S1        S0
              Cout

Critical Path Delay: O(n) where n = number of bits
For 4-bit: T = 4 × T_FA

Delay Analysis:
- T_XOR = 2 gate delays
- T_AND = 1 gate delay
- T_OR  = 1 gate delay
- T_FA  = 4 gate delays (critical path through XOR chain)
- Total 4-bit = 16 gate delays
```

#### Carry Lookahead Adder (CLA)
```
Generate and Propagate Terms:
Gi = Ai · Bi        (Generate)
Pi = Ai ⊕ Bi        (Propagate)

Carry Equations:
C1 = G0 + P0·C0
C2 = G1 + P1·G0 + P1·P0·C0
C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0
C4 = G3 + P3·G2 + P3·P2·G1 + P3·P2·P1·G0 + P3·P2·P1·P0·C0

Delay: O(log n) vs O(n) for RCA
Area: O(n·log n) vs O(n) for RCA
```

#### Carry Select Adder (CSA)
```
Structure for 8-bit CSA (using 4-bit blocks):

Block 1 (bits 3-0):         Block 2 (bits 7-4):
A[3:0], B[3:0]              A[7:4], B[7:4]
     ↓                           ↓
[4-bit RCA with C=0]        [4-bit RCA with C=0] → Sum_low
[4-bit RCA with C=1]        [4-bit RCA with C=1] → Sum_high
     ↓                           ↓
[MUX selected by C4]        [MUX selected by C8]

Delay: O(√n) with optimal block sizing
```

#### Adder Comparison

| Adder Type | Delay | Area | Power | Best Application |
|------------|-------|------|-------|------------------|
| Half Adder | 2 gate delays | 5 gates | Low | Single-bit addition |
| Full Adder | 4 gate delays | 9 gates | Low | Building block |
| Ripple Carry | 4n gate delays | 9n gates | Low | Small operands |
| Carry Lookahead | 2log₂(n)+2 | ~n·log₂(n) | High | High-speed |
| Carry Select | ~4√n | ~9n + MUX | Medium | Medium-speed |
| Kogge-Stone | 2log₂(n) | ~n·log₂(n) | Very High | Very high-speed |
| Brent-Kung | 2log₂(n) | ~2n | Medium | Balanced |

### 2.2 Binary Subtractors

#### Half Subtractor
```
Truth Table:
A | B | Diff | Bout
--|---|------|-----
0 | 0 |  0   |  0
0 | 1 |  1   |  1
1 | 0 |  1   |  0
1 | 1 |  0   |  0

Boolean Equations:
Diff = A ⊕ B
Bout = A' · B
```

#### Full Subtractor
```
Truth Table:
A | B | Bin | Diff | Bout
--|---|-----|------|-----
0 | 0 |  0  |  0   |  0
0 | 0 |  1  |  1   |  1
0 | 1 |  0  |  1   |  1
0 | 1 |  1  |  0   |  1
1 | 0 |  0  |  1   |  0
1 | 0 |  1  |  0   |  0
1 | 1 |  0  |  0   |  0
1 | 1 |  1  |  1   |  1

Boolean Equations:
Diff = A ⊕ B ⊕ Bin
Bout = A'·B + Bin·(A ⊕ B)'
```

#### Adder/Subtractor Unit
```
Shared Hardware using 2's Complement:
A - B = A + (-B) = A + B' + 1

Structure:
A[3:0] ──────→[+]
               |
B[3:0] →[XOR with Mode]→[+]
               |
Mode ─────────→Cin

When Mode=0: A + B (Addition)
When Mode=1: A + B' + 1 = A - B (Subtraction)
```

### 2.3 Comparators

#### Magnitude Comparator
```
Truth Table for 1-bit comparator:
A | B | A>B | A=B | A<B
--|---|-----|-----|----
0 | 0 |  0  |  1  |  0
0 | 1 |  0  |  0  |  1
1 | 0 |  1  |  0  |  0
1 | 1 |  0  |  1  |  0

Boolean Equations:
A > B = A · B'
A = B = A ⊙ B = AB + A'B'
A < B = A' · B

Cascading for n-bit comparison:
For A[3:0] vs B[3:0]:
EQ3 = A3⊙B3, GT3 = A3·B3', LT3 = A3'·B3
EQ2 = A2⊙B2, GT2 = A2·B2', LT2 = A2'·B2
EQ1 = A1⊙B1, GT1 = A1·B1', LT1 = A1'·B1
EQ0 = A0⊙B0, GT0 = A0·B0', LT0 = A0'·B0

A_eq_B = EQ3·EQ2·EQ1·EQ0
A_gt_B = GT3 + EQ3·GT2 + EQ3·EQ2·GT1 + EQ3·EQ2·EQ1·GT0
A_lt_B = LT3 + EQ3·LT2 + EQ3·EQ2·LT1 + EQ3·EQ2·EQ1·LT0
```

### 2.4 Multiplexers (MUX)

#### 2:1 Multiplexer
```
Truth Table:
S | A | B | Y
--|---|---|--
0 | 0 | 0 | 0
0 | 0 | 1 | 0
0 | 1 | 0 | 1
0 | 1 | 1 | 1
1 | 0 | 0 | 0
1 | 0 | 1 | 1
1 | 1 | 0 | 0
1 | 1 | 1 | 1

Boolean Equation: Y = S'A + SB

Implementation:
VDD           VDD
 |             |
[NMOS]--A--[NMOS]--B
 |             |
 +---Y----------+
 |             |
[NMOS]--S  [NMOS]--S'
 |             |
GND           GND

Or using transmission gates:
A ---[TG1]---+
              |--- Y
B ---[TG2]---+

TG1 controlled by S'
TG2 controlled by S
```

#### 4:1 Multiplexer
```
Truth Table:
S1 | S0 | Y
---|----|--
 0 |  0 | D0
 0 |  1 | D1
 1 |  0 | D2
 1 |  1 | D3

Boolean Equation:
Y = S1'S0'D0 + S1'S0D1 + S1S0'D2 + S1S0D3

Gate Implementation:
- 4 AND gates (3-input each)
- 1 OR gate (4-input)
- 2 NOT gates (for select lines)
- Total: 7 gates, 24 transistors

Hierarchical Implementation:
4:1 MUX = Two 2:1 MUXes + one 2:1 MUX
         = (S0'?D0 + S0·D1)·S1' + (S0'?D2 + S0·D3)·S1
```

#### 8:1 Multiplexer
```
Equation:
Y = Σ(S2'S1'S0'·D0, S2'S1'S0·D1, ..., S2S1S0·D7)

Hierarchical (tree of 2:1 MUXes):
Level 1: Four 2:1 MUXes (select S0)
Level 2: Two 2:1 MUXes (select S1)
Level 3: One 2:1 MUX (select S2)

Total 2:1 MUXes: 4 + 2 + 1 = 7
```

#### MUX as Universal Logic Element

```
Any n-variable function can be implemented with a 2^n:1 MUX:

Example: F(A,B,C) = Σm(1,3,5,7) = C

Implementation with 8:1 MUX:
D0=0, D1=1, D2=0, D3=1, D4=0, D5=1, D6=0, D7=1

Example: F(A,B,C) = Σm(0,1,6,7)

Implementation with 8:1 MUX:
D0=1, D1=1, D2=0, D3=0, D4=0, D5=0, D6=1, D7=1

Reduced MUX (4:1) with external logic:
Using A as select:
When A=0: F0(B,C) = Σm(0,1) = B'  → D0=B'
When A=1: F1(B,C) = Σm(2,3) = B   → D1=B
```

### 2.5 Demultiplexers (DEMUX)

#### 1:2 DEMUX
```
Truth Table:
S | Y0 | Y1
--|----|----
0 |  D |  0
1 |  0 |  D

Boolean Equations:
Y0 = S' · D
Y1 = S · D

Implementation:
D ---|\
     | >--- Y0
S ---|/

D ---|\
     | >--- Y1
S'--|/
```

#### 1:4 DEMUX
```
Truth Table:
S1 | S0 | Y0 | Y1 | Y2 | Y3
---|----|----|----|----|----
 0 |  0 |  D |  0 |  0 |  0
 0 |  1 |  0 |  D |  0 |  0
 1 |  0 |  0 |  0 |  D |  0
 1 |  1 |  0 |  0 |  0 |  D

Boolean Equations:
Y0 = S1'·S0'·D
Y1 = S1'·S0·D
Y2 = S1·S0'·D
Y3 = S1·S0·D
```

### 2.6 Encoders

#### 4:2 Priority Encoder
```
Truth Table (higher priority to I3):
I3 | I2 | I1 | I0 | Y1 | Y0 | V
---|----|----|----|----|----|--
 0 |  0 |  0 |  0 |  X |  X |  0
 0 |  0 |  0 |  1 |  0 |  0 |  1
 0 |  0 |  1 |  X |  0 |  1 |  1
 0 |  1 |  X |  X |  1 |  0 |  1
 1 |  X |  X |  X |  1 |  1 |  1

Boolean Equations:
Y1 = I3 + I2'I3'·I2 = I3 + I2
Y0 = I3 + I2'I1
V  = I3 + I2 + I1 + I0

Note: X = Don't Care condition
```

#### 8:3 Priority Encoder
```
Truth Table (abbreviated):
I7 | I6 | I5 | I4 | I3 | I2 | I1 | I0 | Y2 | Y1 | Y0 | V
---|----|----|----|----|----|----|----|----|----|----|--
 0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  X |  X |  X |  0
 0 |  0 |  0 |  0 |  0 |  0 |  0 |  1 |  0 |  0 |  0 |  1
 0 |  0 |  0 |  0 |  0 |  0 |  1 |  X |  0 |  0 |  1 |  1
 0 |  0 |  0 |  0 |  0 |  1 |  X |  X |  0 |  1 |  0 |  1
 0 |  0 |  0 |  0 |  1 |  X |  X |  X |  0 |  1 |  1 |  1
 0 |  0 |  0 |  1 |  X |  X |  X |  X |  1 |  0 |  0 |  1
 0 |  0 |  1 |  X |  X |  X |  X |  X |  1 |  0 |  1 |  1
 0 |  1 |  X |  X |  X |  X |  X |  X |  1 |  1 |  0 |  1
 1 |  X |  X |  X |  X |  X |  X |  X |  1 |  1 |  1 |  1

Equations:
Y2 = I7 + I6 + I5 + I4
Y1 = I7 + I6 + I5'I4'I3 + I5'I4'I2
Y0 = I7 + I5'I4'I3'I2'I1 + I5'I4'I3'I2'I0 + I6'I5'I4'I3 + I6'I5'I4'I1
V  = I7 + I6 + I5 + I4 + I3 + I2 + I1 + I0
```

### 2.7 Decoders

#### 2:4 Decoder
```
Truth Table:
S1 | S0 | Y0 | Y1 | Y2 | Y3
---|----|----|----|----|----
 0 |  0 |  1 |  0 |  0 |  0
 0 |  1 |  0 |  1 |  0 |  0
 1 |  0 |  0 |  0 |  1 |  0
 1 |  1 |  0 |  0 |  0 |  1

Boolean Equations:
Y0 = S1'·S0'
Y1 = S1'·S0
Y2 = S1·S0'
Y3 = S1·S0
```

#### 3:8 Decoder
```
Truth Table:
S2 | S1 | S0 | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | Y7
---|----|----|----|----|----|----|----|----|----|----
 0 |  0 |  0 |  1 |  0 |  0 |  0 |  0 |  0 |  0 |  0
 0 |  0 |  1 |  0 |  1 |  0 |  0 |  0 |  0 |  0 |  0
 0 |  1 |  0 |  0 |  0 |  1 |  0 |  0 |  0 |  0 |  0
 0 |  1 |  1 |  0 |  0 |  0 |  1 |  0 |  0 |  0 |  0
 1 |  0 |  0 |  0 |  0 |  0 |  0 |  1 |  0 |  0 |  0
 1 |  0 |  1 |  0 |  0 |  0 |  0 |  0 |  1 |  0 |  0
 1 |  1 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  1 |  0
 1 |  1 |  1 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  1

Decoder + OR gates = Any Boolean function
Example: F(A,B,C) = Σm(1,3,5,7) = C
Use 3:8 decoder outputs Y1,Y3,Y5,Y7 ORed together
```

## 3. Arithmetic Logic Unit (ALU)

### 3.1 ALU Block Diagram

```
            A[7:0]    B[7:0]
              |         |
              ↓         ↓
         ┌────────────────────┐
         │                    │
    S[2:0]→│    ALU Core      │
         │                    │
         └────────────────────┘
              |         |
              ↓         ↓
           Result[7:0]  Flags

ALU Operations (3-bit opcode):
000: A + B (ADD)
001: A - B (SUB)
010: A AND B
011: A OR B
100: A XOR B
101: NOT A
110: A << 1 (Shift Left)
111: A >> 1 (Shift Right)
```

### 3.2 Simple ALU Implementation

```verilog
module alu_8bit (
    input  wire [7:0] A, B,
    input  wire [2:0] ALU_Sel,
    output reg  [7:0] Result,
    output wire Zero, Overflow, Carry
);

    wire [8:0] temp_sum;
    wire [8:0] temp_diff;

    assign temp_sum = {1'b0, A} + {1'b0, B};
    assign temp_diff = {1'b0, A} - {1'b0, B};

    always @(*) begin
        case (ALU_Sel)
            3'b000: Result = temp_sum[7:0];    // ADD
            3'b001: Result = temp_diff[7:0];   // SUB
            3'b010: Result = A & B;            // AND
            3'b011: Result = A | B;            // OR
            3'b100: Result = A ^ B;            // XOR
            3'b101: Result = ~A;               // NOT
            3'b110: Result = A << 1;           // SHIFT LEFT
            3'b111: Result = A >> 1;           // SHIFT RIGHT
            default: Result = 8'b0;
        endcase
    end

    assign Zero = (Result == 8'b0);
    assign Overflow = (ALU_Sel == 3'b000) ? 
                      (A[7] == B[7] && Result[7] != A[7]) : 1'b0;
    assign Carry = (ALU_Sel == 3'b000) ? temp_sum[8] : 1'b0;

endmodule
```

## 4. Code Converters

### 4.1 Binary to BCD Converter

```
Algorithm (Double Dabble):
Input: 8-bit binary number
Output: 12-bit BCD (tens-hundreds, tens, ones)

Steps:
1. Initialize BCD register to 0
2. For each binary bit (MSB to LSB):
   a. If any BCD digit > 4, add 3 to that digit
   b. Shift BCD register left by 1, bringing in next binary bit
3. After 8 shifts, BCD result is complete

Example: Binary 11010101 (213 decimal)
Step  | Binary    | BCD (TH-T-O)
------|-----------|-------------
Init  | 11010101  | 0000-0000-0000
1     | 1010101_  | 0000-0000-0001
2     | 0101010_1 | 0000-0000-0011
3     | 101010_11 | 0000-0000-0111
4     | 01010_111 | 0000-0001-0111
5     | 1010_1111 | 0000-0011-0111
6     | 010_11111 | 0000-0111-0111
7     | 10_111111 | 0001-0010-0011
8     | 0_1111111 | 0010-0001-0011
```

### 4.2 BCD to Binary Converter

```
Algorithm:
Binary = BCD_hundreds × 100 + BCD_tens × 10 + BCD_ones

Implementation using shift-and-add:
× 10 = × 8 + × 2 = (N << 3) + (N << 1)

Example: BCD 213
Hundreds: 2 × 100 = 200
Tens:     1 × 10  =  10
Ones:     3 × 1   =   3
Total: 213 (binary: 11010101)
```

### 4.3 Gray Code Converter

```
Binary to Gray:
G[n] = B[n]
G[i] = B[i+1] ⊕ B[i] for i < n

Gray to Binary:
B[n] = G[n]
B[i] = B[i+1] ⊕ G[i] for i < n

Example: Binary 1101 → Gray
G3 = B3 = 1
G2 = B3 ⊕ B2 = 1 ⊕ 1 = 0
G1 = B2 ⊕ B1 = 1 ⊕ 0 = 1
G0 = B1 ⊕ B0 = 0 ⊕ 1 = 1
Result: 1011

4-bit Gray Code Sequence:
Dec | Bin  | Gray
----|------|-----
 0  | 0000 | 0000
 1  | 0001 | 0001
 2  | 0010 | 0011
 3  | 0011 | 0010
 4  | 0100 | 0110
 5  | 0101 | 0111
 6  | 0110 | 0101
 7  | 0111 | 0100
 8  | 1000 | 1100
 9  | 1001 | 1101
10  | 1010 | 1111
11  | 1011 | 1110
12  | 1100 | 1010
13  | 1101 | 1011
14  | 1110 | 1001
15  | 1111 | 1000
```

## 5. Parity Generators and Checkers

### 5.1 Even Parity

```
For 4-bit data (D3,D2,D1,D0):
Parity bit P = D3 ⊕ D2 ⊕ D1 ⊕ D0

Transmitted: (D3,D2,D1,D0,P)
Check: D3 ⊕ D2 ⊕ D1 ⊕ D0 ⊕ P = 0 (even parity)
       D3 ⊕ D2 ⊕ D1 ⊕ D0 ⊕ P = 1 (error detected)

Truth Table for 3-bit parity generator:
A | B | C | P_even | P_odd
--|---|---|--------|------
0 | 0 | 0 |   0    |   1
0 | 0 | 1 |   1    |   0
0 | 1 | 0 |   1    |   0
0 | 1 | 1 |   0    |   1
1 | 0 | 0 |   1    |   0
1 | 0 | 1 |   0    |   1
1 | 1 | 0 |   0    |   1
1 | 1 | 1 |   1    |   0
```

### 5.2 Parity Tree Implementation

```verilog
// 8-bit even parity generator
module parity_gen_8bit (
    input  wire [7:0] data,
    output wire parity
);

    assign parity = ^data;  // Reduction XOR

endmodule

// 8-bit parity checker
module parity_check_8bit (
    input  wire [7:0] data,
    input  wire parity_in,
    output wire error
);

    assign error = ^data ^ parity_in;

endmodule
```

## 6. Tri-State Buffers

### 6.1 Basic Tri-State Buffer

```
Truth Table:
EN | A | Y
--|---|--
0 | X | Z (High Impedance)
1 | 0 | 0
1 | 1 | 1

CMOS Implementation:
VDD
 |
[PMOS]---A'
 |
 +---EN'---+
 |         |
Y          |
 |         |
 +---EN----+
 |
[NMOS]---A
 |
GND
```

### 6.2 Bus Application

```
Tri-State Bus Architecture:
                    Data Bus
Device 1 ──[TSB]────────────────
Device 2 ──[TSB]────────────────
Device 3 ──[TSB]────────────────
                     │
                     ↓
Device 4 ←──[TSB]───────────────
Device 5 ←──[TSB]───────────────

TSB = Tri-State Buffer
Only one driver active at a time
```

## 7. Hazards and Glitches

### 7.1 Static Hazards

```
Static-1 Hazard:
Function: F = A·C + B'·C

When A changes from 0→1 (B=0, C=1):
Ideal: F stays at 1
Actual: Glitch to 0 due to delay in A vs B'

K-Map Analysis:
C
AB  0   1
0 | 0 | 1 | ← B'C
1 | 0 | 1 | ← AC

Hazard occurs at boundary between groups

Solution: Add consensus term
F = A·C + B'·C + A·B'·C'  (redundant term eliminates hazard)
```

### 7.2 Dynamic Hazards

```
Dynamic Hazard:
Function: F = (A + B)·(A' + C)·(B + C)

Multiple paths from input to output can cause
3 or more transitions (0→1→0→1)

Usually occurs in multilevel circuits
Can be eliminated by converting to two-level form
```

### 7.3 Hazard Prevention Methods

| Method | Description | Overhead |
|--------|-------------|----------|
| Consensus terms | Add redundant covering terms | Area increase |
| Redundant paths | Multiple parallel paths | Area and power |
| Filtering capacitors | Slow down transitions | Delay increase |
| Pipelining | Register stages | Latency increase |

## 8. Timing Analysis for Combinational Circuits

### 8.1 Propagation Delay

```
Key Timing Parameters:
- t_pd (propagation delay): Input to output delay
- t_cd (contamination delay): Minimum delay from input to output
- t_setup: Setup time (sequential circuits)
- t_hold: Hold time (sequential circuits)

For combinational circuits:
Maximum delay = Critical path delay
Minimum delay = Shortest path delay

Critical Path: Longest path through combinational logic
Determines maximum clock frequency: f_max = 1 / t_pd_critical
```

### 8.2 Timing Constraints

```
For a combinational path:
t_pd_logic ≥ t_setup (meeting setup time)
t_cd_logic ≥ t_hold (meeting hold time)

Setup constraint: T_clk ≥ t_pcq + t_pd_logic + t_setup
Hold constraint:  t_ccq + t_cd_logic ≥ t_hold

Where:
T_clk    = clock period
t_pcq    = clock-to-Q delay (flip-flop)
t_ccq    = contamination clock-to-Q delay
t_pd_logic = propagation delay of combinational logic
t_cd_logic = contamination delay of combinational logic
```

## 9. Applications in Medical Implants

### 9.1 Ultra-Low-Power Combinational Design

```
For implantable devices, power optimization is critical:

1. Gate Sizing:
   - Use minimum-size gates where speed not critical
   - Reduce capacitance: P = C·V²·f

2. Logic Style Selection:
   - Pass-transistor logic: fewer transistors, lower power
   - Transmission gate logic: better voltage swing
   - Dynamic logic: low standby power

3. Voltage Scaling:
   - Reduce V_DD from 1.8V to 0.8V
   - Power reduction: (0.8/1.8)² = 0.20 (80% savings!)
   - Requires threshold voltage adjustment

4. Activity Reduction:
   - Gray code counters (1-bit change)
   - Clock gating for unused blocks
   - Operand isolation
```

### 9.2 Fault-Tolerant Design

```
For critical medical functions:

1. Triple Modular Redundancy (TMR):
   ┌─[Logic A]─┐
   │            ├─→ [Voter] → Output
   ├─[Logic B]─┤
   │            │
   └─[Logic C]─┘

2. Error Detection and Correction:
   - Hamming codes: SEC-DED (Single Error Correct, Double Error Detect)
   - Parity: Simple error detection
   - CRC: Burst error detection

3. Watchdog Timers:
   - Monitor circuit operation
   - Reset system if stuck
```

## 10. Summary

| Component | Function | Typical Use |
|-----------|----------|-------------|
| Adder | Arithmetic addition | ALU, address generation |
| Subtractor | Arithmetic subtraction | ALU, comparison |
| Comparator | Magnitude comparison | Control logic, sorting |
| Multiplexer | Data selection | Registers, ALU, bus |
| Demultiplexer | Data distribution | Memory addressing |
| Encoder | Priority encoding | Interrupt handling |
| Decoder | Binary decoding | Memory selection, display |
| Parity Generator/Checker | Error detection | Reliable communication |
| Tri-State Buffer | Bus interfacing | Shared bus systems |
| ALU | Arithmetic and logic | Processor core |

## 11. Exercises

1. Design a 4-bit ripple carry adder and calculate worst-case delay
2. Implement a 16:1 MUX using 2:1 MUXes only
3. Design a BCD to 7-segment decoder
4. Create a 4-bit magnitude comparator with cascading capability
5. Implement an 8-bit ALU supporting ADD, SUB, AND, OR, XOR operations
6. Analyze and fix hazards in F = A'B'C + AB'C + ABC'
7. Design a parity generator/checker for 12-bit data
8. Compare power consumption of different adder architectures for implant applications
