# Adders and Subtractors - Formulas

## Half Adder
```
Sum = A XOR B
Carry = A AND B
```

## Full Adder
```
Sum = A XOR B XOR Cin
Cout = AB + Cin(A XOR B) = AB + BCin + ACin (any two 1s)
= majority(A,B,Cin)
```

## N-bit Ripple Carry
```
Delay = N * t_carrier (worst case)
Area: N full adders
```

## Carry Lookahead
```
Generate: Gi = Ai Bi
Propagate: Pi = Ai XOR Bi (or Ai OR Bi)
Carry: Ci+1 = Gi + Pi Ci
Sum: Si = Pi XOR Ci
```

## 4-bit CLA carries
```
C1 = G0 + P0 C0
C2 = G1 + P1 G0 + P1 P0 C0
C3 = G2 + P2 G1 + P2 P1 G0 + P2 P1 P0 C0
C4 = G3 + P3 G2 + P3 P2 G1 + P3 P2 P1 G0 + P3 P2 P1 P0 C0
Sum: S0=P0^C0, S1=P1^C1, S2=P2^C2, S3=P3^C3
```

## Half Subtractor
```
D = A XOR B
Borrow = A' B  (A AND NOT B) when A<B
```

## Full Subtractor
```
D = A XOR B XOR Bin
Borrow = A'B + A' Bin + B Bin ... (2 of (A' ,B,Bin))
= A'B + Bin(A' XOR B)?
```

## Two's Complement subtractor (A-B)
```
Result = A + B' + 1
B' = bitwise NOT B
Design: use adder with control:
  B_c = B XOR S, Cin = S
  S=0 -> A+B, S=1 -> A-B (A+B'+1)
```

## Adder Counts
```
Half adder: 1 XOR + 1 AND
Full adder: 2 half adders + 1 OR
  5 gates total (2 XOR, 2 AND, 1 OR)
CLA: alot but fast
```

## Quick Reference
| Signal | Expression |
|--------|-----------|
| HA Sum | A^B |
| HA Carry | AB |
| FA Sum | A^B^Cin |
| FA Carry | AB+ACin+BCin |
| G | Ai Bi |
| P | Ai^Bi |
| Carry next | G + P C |
| D (sub) | A^B^Bin |
| Borrow | A'B + ... |
