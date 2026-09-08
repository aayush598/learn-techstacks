# Number Systems and Codes - Concepts

## 1. Binary Number System

### Basic Representation
- Base-2 system using digits 0 and 1
- MSB (Most Significant Bit) is leftmost, LSB (Least Significant Bit) is rightmost
- Weight of each bit position = 2^n where n starts from 0 at LSB
- Example: (1011)₂ = 1×2³ + 0×2² + 1×2¹ + 1×2⁰ = 8+0+2+1 = 11

### Fractional Binary
- Binary point separates integer and fractional parts
- (101.11)₂ = 4+0+1+0.5+0.25 = 5.75
- Weights to the right: 2⁻¹, 2⁻², 2⁻³ ...

## 2. Octal Number System

- Base-8, digits 0-7
- 3 bits represent 1 octal digit (2³ = 8)
- Conversion from binary: Group bits in threes from LSB
- Example: (101110)₂ = (010)(111)(0) → (5)(6)₈ wait - (101)(110) = (5)(6)₈... Actually 101 110 = 56₈

## 3. Hexadecimal Number System

- Base-16, digits 0-9 and A-F (A=10, B=11, C=12, D=13, E=14, F=15)
- 4 bits represent 1 hex digit (2⁴ = 16)
- Conversion from binary: Group in fours from LSB
- Example: (1101 1010)₂ = (DA)₁₆ = 13×16 + 10 = 218

## 4. Decimal to Binary Conversion

### Integer Part - Double Dabble (Repeated Division by 2)
- Divide decimal by 2, record remainders
- Read remainders from bottom to top = binary
- Example: 13 ÷ 2 = 6 R1, 6 ÷ 2 = 3 R0, 3 ÷ 2 = 1 R1, 1 ÷ 2 = 0 R1
- (13)₁₀ = (1101)₂

### Fractional Part - Repeated Multiplication by 2
- Multiply fractional part by 2, extract integer
- Example: 0.625 × 2 = 1.25 (1), 0.25 × 2 = 0.5 (0), 0.5 × 2 = 1.0 (1)
- (0.625)₁₀ = (0.101)₂

## 5. Complement Systems

### 1's Complement
- Invert all bits (0→1, 1→0)
- Represents negative numbers in signed systems
- Two representations of zero: +0 and -0
- For n-bit number N, 1's complement of N = (2ⁿ - 1) - N
- Example: 1's complement of 1011 = 0100

### 2's Complement
- 1's complement + 1
- Unique representation of zero (no +0/-0 problem)
- Range: -2ⁿ⁻¹ to +(2ⁿ⁻¹ - 1) for n bits
- Most widely used representation for signed integers
- To negate: invert bits and add 1
- Example: 2's complement of 1011: invert=0100, add 1 = 0101

### 9's and 10's Complement (Decimal)
- 9's complement: subtract each digit from 9
- 10's complement: 9's complement + 1
- Used in decimal arithmetic circuits

## 6. Signed Number Representations

### Sign-Magnitude
- MSB = sign (0 for +, 1 for -), remaining bits = magnitude
- n bits → range: -(2ⁿ⁻¹ - 1) to +(2ⁿ⁻¹ - 1)
- Two zeros: +0 = 0000...0, -0 = 1000...0
- Simple but arithmetic is complex (need to handle signs separately)

### 1's Complement (Signed)
- Positive: same as unsigned
- Negative: 1's complement of positive number
- Range: -(2ⁿ⁻¹ - 1) to +(2ⁿ⁻¹ - 1)
- Two zeros exist

### 2's Complement (Signed) - Most Important
- Positive: same as unsigned
- Negative: 2's complement of positive number
- Range: -2ⁿ⁻¹ to +(2ⁿ⁻¹ - 1)
- Single zero representation
- Used in virtually all modern computers
- MSB has weight -2ⁿ⁻¹

### Comparison for 4-bit numbers:
| Representation | Range | # of Zeros |
|---|---|---|
| Unsigned | 0 to 15 | 1 |
| Sign-Magnitude | -7 to +7 | 2 |
| 1's Complement | -7 to +7 | 2 |
| 2's Complement | -8 to +7 | 1 |

## 7. Binary Arithmetic

### Binary Addition
- 0+0=0, 0+1=1, 1+0=1, 1+1=10 (carry), 1+1+1=11 (carry)

### Binary Subtraction
- 0-0=0, 1-0=1, 1-1=0, 0-1=1 (borrow)
- Using 2's complement: A-B = A + (2's complement of B)

### Binary Multiplication
- Same process as decimal long multiplication

## 8. BCD (Binary Coded Decimal)

### 8421 BCD
- Each decimal digit encoded as 4-bit binary
- Valid range per group: 0000 to 1001 (0-9)
- 1010-1111 are invalid/unused codes
- Example: (925)₁₀ = (1001 0010 0101)₈₄₂₁BCD

### Excess-3 Code
- Each digit = binary + 0011 (3)
- Non-weighted code
- Self-complementing: 1's complement of code = 9's complement of digit
- Example: 3→0110, 5→1000
- Useful for BCD arithmetic (carry propagation handled naturally)

### 2421 BCD
- Weighted code with weights 2, 4, 2, 1
- Also self-complementing
- Digits 0-4 have MSB=0, digits 5-9 have MSB=1

### BCD Addition
- Add as normal binary
- If sum > 1001 (9) or carry out of MSB, add 0110 (6) to correct
- This "excess-6" correction is key ISRO concept

## 9. Gray Code

- Also called reflected binary code
- Only one bit changes between consecutive codes
- Cyclic code (last to first also differs by 1 bit)
- n-bit Gray code: G = B ⊕ (B >> 1) (XOR each bit with bit to its right)
- Example: 3-bit Gray: 000, 001, 011, 010, 110, 111, 101, 100
- Applications: Karnaugh maps, rotary encoders, error detection in analog-to-digital conversion
- Advantage: eliminates spurious outputs during transitions

### Gray to Binary Conversion
- B(n-1) = G(n-1)
- B(i) = B(i+1) XOR G(i) for remaining bits

## 10. ASCII (American Standard Code for Information Interchange)

- 7-bit code (128 characters) or extended 8-bit (256 characters)
- Control characters: 0-31 and 127
- Printable: 32-126
- Digits '0'-'9': 48-57 (0x30-0x39)
- Uppercase 'A'-'Z': 65-90 (0x41-0x5A)
- Lowercase 'a'-'z': 97-122 (0x61-0x7A)
- Difference between upper and lowercase = 32 (bit 5)

## 11. Parity

### Even Parity
- Total number of 1s (including parity bit) is even
- Parity bit = XOR of all data bits
- Used for single-bit error detection

### Odd Parity
- Total number of 1s (including parity bit) is odd
- Parity bit = XOR of all data bits then inverted

### Limitations
- Can only detect odd number of bit errors
- Cannot detect even number of bit errors
- Cannot correct errors

## 12. Other Important Codes

### Biquinary Code
- 7-bit code: 5+2 format
- Error detecting capability (one of first 5 bits and one of last 2 bits must be 1)

### Excess-3 Gray Code
- Combination of excess-3 and Gray code properties

### Hamming Code
- SEC-DED (Single Error Correction, Double Error Detection)
- Parity bits at positions that are powers of 2
- Minimum distance = 3

### ISBN Check
- Uses weighted sum modulo 11

## 13. Key Conversion Strategies for ISRO

### Quick Binary-Decimal Patterns
- Memorize: 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024
- For large numbers, break into groups
- Binary to hex/octal is faster than binary to decimal

### Shortcut for 2's Complement Negation
- Keep all bits same from right until first '1' is found
- Then flip all remaining bits to the left
- Example: 1100 → find first 1 from right (position 0) → flip left bits: 0100

## 14. Number System Summary Table

| System | Base | Digits | Bits per digit |
|---|---|---|---|
| Binary | 2 | 0, 1 | 1 |
| Octal | 8 | 0-7 | 3 |
| Decimal | 10 | 0-9 | ~3.32 |
| Hexadecimal | 16 | 0-9, A-F | 4 |

## 15. ISRO Exam Key Points

- BCD addition correction: if sum > 9 or carry, add 0110
- Excess-3 is self-complementing (trick: 1's comp gives 9's comp)
- Gray code: only 1 bit changes (use XOR method G = B⊕(B>>1))
- 2's complement has unique zero and wider range than sign-magnitude
- Parity detects only ODD number of bit errors
- ASCII: 'A'=65, 'a'=97, '0'=48
