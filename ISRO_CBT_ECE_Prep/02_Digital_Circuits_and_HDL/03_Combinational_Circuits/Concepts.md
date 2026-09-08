# Combinational Circuits - Concepts

## Fundamental Definitions

### Combinational vs Sequential
| Feature | Combinational | Sequential |
|---------|--------------|------------|
| Memory | No | Yes (flip-flops) |
| Output depends on | Current inputs only | Current inputs + past state |
| Examples | Adders, MUX, Decoders | Counters, Registers |
| Analysis | Truth table | State diagram/table |

### Building Blocks
All combinational circuits are built from:
- **Logic gates:** AND, OR, NOT, NAND, NOR, XOR, XNOR
- **No feedback loops** — output never feeds back to input
- **Propagation delay** is the only time consideration

---

## Half Adder

### Truth Table
| A | B | Sum | Carry |
|---|---|-----|-------|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

### Boolean Expressions
```
Sum = A ⊕ B = AB' + A'B
Carry = A · B
```

### Key Points
- Adds two single-bit binary numbers
- **Cannot** accept a carry input from previous stage
- Uses 1 XOR gate + 1 AND gate

---

## Full Adder

### Truth Table
| A | B | Cᵢₙ | Sum | Cₒᵤₜ |
|---|---|------|-----|-------|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

### Boolean Expressions
```
Sum = A ⊕ B ⊕ Cᵢₙ
Cₒᵤₜ = AB + BCᵢₙ + ACᵢₙ = AB + Cᵢₙ(A ⊕ B)
```

### Implementation from Half Adders
```
HA1: S₁ = A ⊕ B,    C₁ = AB
HA2: S  = S₁ ⊕ Cᵢₙ, C₂ = S₁·Cᵢₙ
Cₒᵤₜ = C₁ + C₂ = AB + (A⊕B)Cᵢₙ
```
- **2 Half Adders + 1 OR gate** = 1 Full Adder

### Gate Count
- Sum: 2 XOR gates
- Carry: 2 AND + 1 OR gate
- **Total: 5 gates** (2 XOR, 2 AND, 1 OR)

---

## Half Subtractor

### Truth Table
| A | B | Diff | Borrow |
|---|---|------|--------|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 |

### Expressions
```
Diff = A ⊕ B
Borrow = A'B
```

---

## Full Subtractor

### Truth Table
| A | B | Bᵢₙ | Diff | Bₒᵤₜ |
|---|---|------|------|-------|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |

### Expressions
```
Diff = A ⊕ B ⊕ Bᵢₙ
Bₒᵤₜ = A'B + A'Bᵢₙ + BBᵢₙ = A'B + Bᵢₙ(A⊕B)' ... wait
Actually: Bₒᵤₜ = A'B + A'Bᵢₙ + BBᵢₙ
```

---

## Adder-Subtractor (Unified Circuit)

### Using XOR for Mode Control
```
When M=0: Adds A+B (carry-in = 0)
When M=1: Subtracts A-B (B is complemented, carry-in = 1)
```

### Key Concept
```
B XOR M: When M=0, output = B; when M=1, output = B'
Carry-in = M (for 2's complement subtraction)
A - B = A + B' + 1 (2's complement)
```

---

## Magnitude Comparator

### 1-Bit Comparator
| A | B | A>B | A=B | A<B |
|---|---|-----|-----|-----|
| 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 |

### Expressions
```
A > B = AB'
A = B = A'B' + AB = (A ⊕ B)'
A < B = A'B
```

### 4-Bit Comparator (e.g., 7485)
Comparison proceeds MSB to LSB:
```
If A₃ > B₃ → A > B
If A₃ < B₃ → A < B
If A₃ = B₃ → check A₂ vs B₂
If A₂ = B₂ → check A₁ vs B₁
If A₁ = B₁ → check A₀ vs B₀
```

### Cascading
- Compare from MSB to LSB
- Use cascading inputs for multi-stage comparison
- 7485 IC: cascading inputs (I_{A>B}, I_{A=B}, I_{A<B})

---

## Parity Generator & Checker

### Even Parity
- Number of 1s in codeword (including parity bit) is EVEN
- Parity bit = XOR of all data bits

### Odd Parity
- Number of 1s in codeword (including parity bit) is ODD
- Parity bit = XOR of all data bits, then inverted

### 4-Bit Parity Generator
```
Even Parity Bit: P = A ⊕ B ⊕ C ⊕ D
Odd Parity Bit:  P = (A ⊕ B ⊕ C ⊕ D)'
```

### Parity Checker
```
Even: Error = A ⊕ B ⊕ C ⊕ D ⊕ P (should be 0)
Odd: Error = A ⊕ B ⊕ C ⊕ D ⊕ P (should be 1)
```

### Properties
- Detects single-bit errors
- Cannot detect 2-bit (or even number of) errors
- Simple and widely used in memory systems, UARTs

---

## Code Converters

### Binary to Gray Code
```
G₃ = B₃
G₂ = B₃ ⊕ B₂
G₁ = B₂ ⊕ B₁
G₀ = B₁ ⊕ B₀
```

### Gray to Binary
```
B₃ = G₃
B₂ = B₃ ⊕ G₂
B₁ = B₂ ⊕ G₁
B₀ = B₁ ⊕ G₀
```

### BCD to Excess-3
```
E₃ = A + BC
E₂ = B'C + B(D'+D') ... let me provide the standard:
E₃ = B₃ + B₂B₀ + B₂B₁
E₂ = B₂'B₁ + B₂B₁'B₀ + B₂B₁B₀' ... standard mapping
Actually simpler: E₃ = D₃, E₂ = D₃⊕D₂, E₁ = D₃⊕D₁, E₀ = D₃⊕D₀... no

Standard BCD to Excess-3:
Input: B₃B₂B₁B₀ (BCD: 0-9)
Output: E₃E₂E₁E₀ = B₃B₂B₁B₀ + 0011
```

---

## Priority Encoder

### Concept
- Resolves multiple simultaneous requests by priority
- Only the **highest-priority** active input is encoded

### 4-to-2 Priority Encoder
| I₃ | I₂ | I₁ | I₀ | Y₁ | Y₀ | V (valid) |
|----|----|----|----|----|----|-----------|
| 0 | 0 | 0 | 0 | X | X | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | X | 0 | 1 | 1 |
| 0 | 1 | X | X | 1 | 0 | 1 |
| 1 | X | X | X | 1 | 1 | 1 |

**I₃ has highest priority**

### Expressions
```
Y₁ = I₃ + I₂'I₃' + I₂I₃' = I₃ + I₂
Y₀ = I₃ + I₂'I₁
V = I₀ + I₁ + I₂ + I₃
```

---

## BCD to 7-Segment Decoder

### Segments
```
 _a_
|   |
f   b
|_g_|
|   |
e   c
|_d_|
```

### Truth Table (Partial)
| BCD | a | b | c | d | e | f | g |
|-----|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| 4 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |

### IC Examples
- **7447:** BCD to 7-segment (common anode, active LOW outputs)
- **7448:** BCD to 7-segment (common cathode, active HIGH outputs)

---

## Binary Multiplier

### 2×2 Multiplier
```
A₁A₀ × B₁B₀ = P₃P₂P₁P₀
P₀ = A₀B₀
P₁ = A₀B₁ + A₁B₀
P₂ = A₁B₁ + C (carry from P₁)
```
Uses AND gates for partial products, adders for summation

---

## Key ISRO Concepts
1. **Full Adder from Half Adders** — always asked
2. **Adder-Subtractor circuit** — XOR-based mode control
3. **Parity generation** — XOR cascade
4. **Priority encoder** — cascading for expansion
5. **Magnitude comparator** — MSB-first comparison logic
6. **BCD to 7-segment** — decode logic for display
