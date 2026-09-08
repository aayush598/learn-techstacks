# Number Systems and Codes - Formulas

## 1. Base Conversion Formulas

### Binary to Decimal
```
Value = Σ (bᵢ × 2ⁱ) for i = 0 to n-1
Where bᵢ is the bit at position i (0 = LSB)
```

### Decimal to Binary (Integer)
```
Repeated Division: quotient ÷ 2, remainder is bit
Read remainders from last to first (bottom-up)
```

### Decimal to Binary (Fraction)
```
Repeated Multiplication: fraction × 2, integer part is bit
Read integers from first to last (top-down)
```

### Binary to Octal
```
Group bits in 3s from LSB → convert each group to octal digit
```

### Binary to Hexadecimal
```
Group bits in 4s from LSB → convert each group to hex digit
```

### Octal/Hex to Decimal
```
Direct positional weight evaluation (base = 8 or 16)
```

## 2. Complement Formulas

### 1's Complement
```
For n-bit number:
1's Comp(N) = (2ⁿ - 1) - N

Shortcut: Flip all bits
Example: 1's Comp(10110) = 01001
```

### 2's Complement
```
For n-bit number:
2's Comp(N) = 2ⁿ - N = 1's Comp(N) + 1

Shortcut: Flip all bits after rightmost 1, keep that 1 and everything right unchanged
Example: 2's Comp(1100) = 0100
  1100 → rightmost 1 at position 2
  Keep bits 0-1: 00
  Flip bits 2-3: 01
  Result: 0100
```

### 9's Complement (Decimal)
```
9's Comp(N) = (10ⁿ - 1) - N
Each digit d → (9 - d)
```

### 10's Complement (Decimal)
```
10's Comp(N) = 10ⁿ - N = 9's Comp(N) + 1
```

## 3. Signed Number Range Formulas

### Sign-Magnitude (n bits)
```
Range: -(2ⁿ⁻¹ - 1) to +(2ⁿ⁻¹ - 1)
Number of values: 2ⁿ
Two zeros: +0 and -0
```

### 1's Complement (n bits)
```
Range: -(2ⁿ⁻¹ - 1) to +(2ⁿ⁻¹ - 1)
Number of values: 2ⁿ
Two zeros
```

### 2's Complement (n bits)
```
Range: -2ⁿ⁻¹ to +(2ⁿ⁻¹ - 1)
Number of values: 2ⁿ
Single zero
MSB weight: -2ⁿ⁻¹
```

### Quick Reference (n=8):
```
Unsigned: 0 to 255
Sign-Mag: -127 to +127
1's Comp: -127 to +127
2's Comp: -128 to +127
```

## 4. BCD Formulas

### 8421 BCD Addition
```
Step 1: Add both BCD numbers as binary
Step 2: If result > 1001 (9) OR carry from MSB:
         Add 0110 (6) to the result
Step 3: The corrected sum is the BCD result

Formula: IF (Sum > 9) OR (Carry = 1) THEN Corrected = Sum + 0110
```

### Excess-3 Addition
```
Sum = A + B
Each digit: Sumdigit = Binary(A) + Binary(B) + 0011
If carry from any nibble, add 0011 to that nibble
(Excess-3 carry = natural carry + 3)
```

### BCD to Binary Conversion
```
For 2-digit BCD: Binary = 10 × (tens digit) + (units digit)
D = (D₃×10) + D₂ where D₃=tens, D₂=units in BCD
```

## 5. Gray Code Conversion Formulas

### Binary to Gray
```
G(n-1) = B(n-1)          [MSB same]
G(i) = B(i+1) XOR B(i)   [for i = n-2 to 0]

Example (4-bit): B = 1011
G₃ = B₃ = 1
G₂ = B₃ ⊕ B₂ = 1⊕0 = 1
G₁ = B₂ ⊕ B₁ = 0⊕1 = 1
G₀ = B₁ ⊕ B₀ = 1⊕1 = 0
Gray = 1110
```

### Gray to Binary
```
B(n-1) = G(n-1)           [MSB same]
B(i) = B(i+1) XOR G(i)    [for i = n-2 to 0]

Example: G = 1110
B₃ = G₃ = 1
B₂ = B₃ ⊕ G₂ = 1⊕1 = 0
B₁ = B₂ ⊕ G₁ = 0⊕1 = 1
B₀ = B₁ ⊕ G₀ = 1⊕0 = 1
Binary = 1011
```

### n-bit Gray Code Count
```
Total Gray codes = 2ⁿ
Cyclic property: last code differs from first by 1 bit
```

## 6. Parity Formulas

### Even Parity Bit
```
P = D₀ ⊕ D₁ ⊕ D₂ ⊕ ... ⊕ Dₙ₋₁

Total 1s including P must be even
```

### Odd Parity Bit
```
P = D₀ ⊕ D₁ ⊕ D₂ ⊕ ... ⊕ Dₙ₋₁ ⊕ 1

Total 1s including P must be odd
```

### Parity Check
```
Received word → compute parity of all bits
If even parity: result should be 0
If odd parity: result should be 1
Non-zero result = error detected
```

## 7. ASCII Quick Reference Formulas

### Character to ASCII
```
'0'-'9':  ASCII = 48 + digit = 0x30 + digit
'A'-'Z': ASCII = 65 + position = 0x41 + position
'a'-'z': ASCII = 97 + position = 0x61 + position
```

### Case Conversion
```
Lowercase to Uppercase: ASCII - 32 (clear bit 5)
Uppercase to Lowercase: ASCII + 32 (set bit 5)
```

### Digit Extraction
```
ASCII digit to value: ASCII AND 0x0F (or ASCII - 48)
Value to ASCII digit: value OR 0x30 (or value + 48)
```

## 8. Hamming Code Formulas

### Number of Parity Bits
```
2ᵖ ≥ m + p + 1
Where m = data bits, p = parity bits

Example: 4 data bits → 2ᵖ ≥ 4+p+1
p=3: 8 ≥ 8 ✓ (minimum parity bits = 3)
```

### Parity Bit Positions
```
Parity bits at positions: 2⁰=1, 2¹=2, 2²=4, 2³=8, ...
Each parity bit covers positions where bit position has '1' in that bit

P1 (pos 1): covers positions with LSB=1: 1,3,5,7,9,11,...
P2 (pos 2): covers positions with bit1=1: 2,3,6,7,10,11,...
P4 (pos 4): covers positions with bit2=1: 4,5,6,7,12,13,...
```

### Error Detection
```
Syndrome = P1_check ⊕ P2_check ⊕ P4_check ⊕ ...
Syndrome = 0 → No error
Syndrome ≠ 0 → Error at position = syndrome value
```

## 9. Biquinary Code Formula

```
Format: 5 + 2 = 7 bits
First 5 bits: exactly one '1' (position indicates value range 0-4 or 5-9)
Last 2 bits: exactly one '1' (01 for 0-4, 10 for 5-9)

Value = (position of 1 in first 5) + (5 if second group = 10)
Example: 10000 01 → value = 0
         00001 10 → value = 9
```

## 10. Excess-3 Code Formulas

```
Excess-3(d) = d + 3 (in binary)
9's complement of d = Excess-3((9-d)) = NOT(Excess-3(d))

For self-complementing property:
If digit d has code C, then digit (9-d) has code C' (bitwise NOT of C)

Example: d=3 → Excess-3 = 0110
         d=6 → Excess-3 = 1001 = NOT(0110) ✓
```

## 11. Useful Bit Manipulation Formulas

### Power of 2 Check
```
n is power of 2 iff (n & (n-1)) == 0 and n > 0
```

### Set/Clear/Toggle Bit
```
Set bit k:     result = n | (1 << k)
Clear bit k:   result = n & ~(1 << k)
Toggle bit k:  result = n ^ (1 << k)
```

### Extract Bit
```
Bit k of n:    (n >> k) & 1
```

### Sign Extension (n-bit to m-bit, m>n)
```
Sign-extend: copy MSB to all new upper bits
For 2's complement: (x << (m-n)) >> (m-n) [arithmetic shift right]
```

## 12. Number of Bits Required

```
For unsigned integer N: bits = ⌈log₂(N+1)⌉
For signed integer N: bits = ⌈log₂(|N|+1)⌉ + 1 [extra sign bit]

Quick estimate: 10 bits ≈ 1K, 20 bits ≈ 1M, 30 bits ≈ 1G
```

## 13. ISRO Quick Reference Card

```
┌─────────────────────────────────────────────┐
│  2⁰=1  2¹=2  2²=4  2³=8  2⁴=16            │
│  2⁵=32 2⁶=64 2⁷=128 2⁸=256 2⁹=512         │
│  2¹⁰=1024                                  │
├─────────────────────────────────────────────┤
│  '0'=48  'A'=65  'a'=97                    │
│  ASCII case diff = 32 (bit 5)              │
├─────────────────────────────────────────────┤
│  BCD add: sum>9 or carry → +0110           │
│  2's comp: flip bits after rightmost 1     │
│  Gray: G = B ⊕ (B >> 1)                   │
├─────────────────────────────────────────────┤
│  Parity detects ODD errors only            │
│  Excess-3: self-complementing              │
│  Gray: single-bit change property          │
└─────────────────────────────────────────────┘
```
