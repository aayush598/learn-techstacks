# Combinational Circuits - Formulas

## Half Adder
```
Sum     = A ⊕ B
Carry   = A · B
Gates:  1 XOR + 1 AND = 2 gates
```

## Full Adder
```
Sum     = A ⊕ B ⊕ Cᵢₙ
Cₒᵤₜ   = AB + Cᵢₙ(A ⊕ B) = AB + BCᵢₙ + ACᵢₙ
Gates:  2 XOR + 2 AND + 1 OR = 5 gates

From Half Adders:
  HA1: S₁ = A⊕B,  C₁ = AB
  HA2: S = S₁⊕Cᵢₙ, C₂ = S₁·Cᵢₙ
  Cₒᵤₜ = C₁ + C₂
```

## Half Subtractor
```
Diff    = A ⊕ B
Borrow  = A'B
```

## Full Subtractor
```
Diff    = A ⊕ B ⊕ Bᵢₙ
Bₒᵤₜ   = A'B + A'Bᵢₙ + BBᵢₙ
```

## Adder-Subtractor (Mode M)
```
When M=0: Output = A + B  (addition, Cᵢₙ=0)
When M=1: Output = A - B  (subtraction, using 2's complement)
          = A + B' + 1    (B XOR M complements B when M=1)
```

---

## Magnitude Comparator (1-bit)
```
A > B  = AB'
A = B  = (A ⊕ B)' = A'B' + AB
A < B  = A'B
```

## Magnitude Comparator (4-bit, MSB first)
```
A > B: (A₃>B₃) + (A₃=B₃)(A₂>B₂) + (A₃=B₃)(A₂=B₂)(A₁>B₁) + ...
A < B: (A₃<B₃) + (A₃=B₃)(A₂<B₂) + (A₃=B₃)(A₂=B₂)(A₁<B₁) + ...
A = B: (A₃=B₃)(A₂=B₂)(A₁=B₁)(A₀=B₀)
```

---

## Parity Generator

### Even Parity (4-bit data)
```
P = A ⊕ B ⊕ C ⊕ D
Codeword: A B C D P (even number of 1s)
```

### Odd Parity (4-bit data)
```
P = (A ⊕ B ⊕ C ⊕ D)'
Codeword: A B C D P (odd number of 1s)
```

### Parity Checker
```
Error_out = A ⊕ B ⊕ C ⊕ D ⊕ P
For even parity: Error = 0 (correct), Error = 1 (error)
```

---

## Code Converters

### Binary to Gray (n-bit)
```
G[n-1] = B[n-1]
G[i]   = B[i+1] ⊕ B[i]   for i = n-2 to 0

Example (4-bit):
G₃ = B₃
G₂ = B₃ ⊕ B₂
G₁ = B₂ ⊕ B₁
G₀ = B₁ ⊕ B₀
```

### Gray to Binary (n-bit)
```
B[n-1] = G[n-1]
B[i]   = B[i+1] ⊕ G[i]   for i = n-2 to 0

Example (4-bit):
B₃ = G₃
B₂ = B₃ ⊕ G₂
B₁ = B₂ ⊕ G₁
B₀ = B₁ ⊕ G₀
```

### BCD to Excess-3
```
E₃ = B₃
E₂ = B₃ ⊕ B₂
E₁ = B₃ ⊕ B₁
E₀ = B₃ ⊕ B₀
(Only valid for BCD input 0-9)
```

---

## Priority Encoder (4-to-2)

### Expressions (I₃ highest priority)
```
Y₁ = I₃ + I₂'I₃' = I₃ + I₂
Y₀ = I₃ + I₂'I₁
V  = I₃ + I₂ + I₁ + I₀    (valid output)
```

### Cascading (expanding to 8-to-3)
```
Use two 4-to-2 PEs + OR gate for valid bit
Higher PE output overridden when lower PE has valid input
```

---

## BCD to 7-Segment Decoder

### Segment Equations (active HIGH)
```
a = B₃ + B₁ + B₂B₀ + B₂'B₀'
b = B₂'B₀' + B₂'B₁' + B₂B₁B₀' + B₂'B₁B₀ ... simplified:
b = B₂' + B₁B₀ + B₁'B₀'
c = B₂ + B₁'B₀' + B₁B₀
d = B₃ + B₂B₁' + B₂'B₁B₀ + B₂B₁B₀'
e = B₂B₁' + B₂B₁B₀' ... wait, let me provide simplified:
e = B₂B₁' + B₂B₁B₀'
f = B₃ + B₂'B₁ + B₂'B₀' + B₂B₁B₀'
g = B₃ + B₂B₁' + B₂'B₁ + B₂B₁B₀'
```

**Note:** For BCD (0-9), inputs 10-15 are don't cares — used to simplify logic.

---

## Binary Multiplier (2×2)
```
A₁A₀ × B₁B₀ = P₃P₂P₁P₀

P₀ = A₀B₀
P₁ = A₀B₁ ⊕ A₁B₀
C₁ = A₀B₁ · A₁B₀    (carry from P₁)
P₂ = A₁B₁ ⊕ C₁
P₃ = A₁B₁ · C₁
```

---

## N-Bit Ripple Carry Adder
```
Total delay = N × tₚₐₙₙₑₗ (carry must propagate through all stages)
For 4-bit: 4 gate delays
For 16-bit: 16 gate delays (too slow!)
```

---

## Propagation Delay in Combinational Circuits
```
t_pd(max) = longest path (critical path) from any input to any output
Critical path = maximum number of gates in series
```

### Delay Comparison
| Circuit | Delay (gate delays) |
|---------|-------------------|
| Half Adder | 1 (XOR path) |
| Full Adder | 2 (XOR + XOR) |
| 4-bit Ripple Carry | 8 (4 × 2) |
| 4-bit CLA | 3-4 (constant) |

---

## Gate Equivalents
| Circuit | Minimum Gate Equivalent |
|---------|------------------------|
| Half Adder | 5 NAND (or 5 NOR) |
| Full Adder | 9 NAND |
| 2:1 MUX | 4 NAND (or 4 NOR) |
| 4:1 MUX | 10 NAND |

---

## Quick Lookup Table
| Function | SOP | POS | XOR |
|----------|-----|-----|-----|
| Half Adder Sum | A'B + AB' | (A+B)(A'+B') | A⊕B |
| Half Adder Carry | AB | AB | N/A |
| Full Adder Sum | Σm(1,2,4,7) | ΠM(0,3,5,6) | A⊕B⊕C |
| Parity (4-bit) | Σm(1,2,4,7,8,11,13,14) | — | A⊕B⊕C⊕D |
