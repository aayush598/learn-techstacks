# Adders and Subtractors - Concepts

## Binary Adder
- Adds binary digits
- Half adder: 2 inputs (A,B), 2 outputs (Sum, Carry)
- Full adder: 3 inputs (A,B,Cin), 2 outputs (Sum, Carry out)

## Half Adder
```
Sum = A XOR B
Carry = A AND B
Truth: 0+0=0, 0+1=1, 1+1=10 (carry)
2 gates: 1 XOR + 1 AND
```

## Full Adder
```
Sum = A XOR B XOR Cin
Cout = AB + Cin(A XOR B) = AB + Cin(A+B)  (majority)
Built from 2 half adders + OR
Truth: sum = odd parity, Cout = majority of 3
```

## Ripple Carry Adder (RCA)
- Cascade N full adders
- Carry propagates serially through stages
- Simple but SLOW (delay = N * carry delay)
- Delay approx proportional to number of bits

## Carry Lookahead Adder (CLA)
```
Uses generate (G) and propagate (P):
  Gi = Ai Bi       (generate carry)
  Pi = Ai XOR Bi   (propagate carry)
  Ci+1 = Gi + Pi Ci
Computes carries in parallel -> fast
Delay O(log N), much faster than ripple for large N
```

## Carry Lookahead Equations (4-bit)
```
C1 = G0 + P0 C0
C2 = G1 + P1 G0 + P1 P0 C0
C3 = G2 + P2 G1 + P2 P1 G0 + P2P1P0 C0
C4 = G3 + P3 G2 + P3P2 G1 + P3P2P1 G0 + P3P2P1P0 C0
```

## Subtractors
- Half subtractor: Difference, Borrow (D = A-B)
- Full subtractor: 3 bits (A, B, Bin) -> D, Bout
- Alternatively: subtraction via two's complement addition (A + (~B) + 1)

## Half Subtractor
```
D = A XOR B
Borrow = (NOT A) AND B
```

## Full Subtractor
```
D = A XOR B XOR Bin
Borrow = (NOT A)B + Bin(NOT A XOR B) ...
```

## Adder/Subtractor Unit
```
Using two's complement:
  Control S: 0=add, 1=subtract
  B2 = B XOR S  (invert if subtract)
  Cin = S
  Sum = A + (B XOR S) + S
```

## Serial vs Parallel Adder
- Serial: 1 bit at a time, shift register, slow (N clocks)
- Parallel: all bits at once, faster but more hardware

## Applications
- Arithmetic (ALU)
- Address calculation
- Binary counters (actually incrementers)
- DSP (MAC units)

---

## ISRO Key Points
- Full adder: Sum=A^B^Cin, Cout=majority
- Half adder: 2 outputs
- CLA: G, P faster than ripple
- Ripple delay = N*t_carrier
- Subtraction: two's complement add
- G=A&B, P=A^B
