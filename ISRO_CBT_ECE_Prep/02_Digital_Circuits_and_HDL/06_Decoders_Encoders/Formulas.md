# Decoders and Encoders - Formulas

## 2-to-4 Decoder (outputs)
```
Y0 = A' B'
Y1 = A' B
Y2 = A  B'
Y3 = A  B
(Enable low: Y = enable' AND term)
```

## 3-to-8 Decoder minterms
```
Y0=m0=A'B'C', Y1=m1=A'B'C, ..., Y7=m7=ABC
Each output = a minterm
```

## 4-to-2 Encoder
```
A = D1 + D3
B = D2 + D3
(only one input high assumed)
```

## 4-to-2 Priority (D3 highest)
```
V = D0+D1+D2+D3
A = D2 D3' + D3 = D3 + D2
B = D1 D3' + D2 D3' = D3' (D1+D2)... 
  More precisely:
  A = D3 + D2 D3'  -> D3 + D2 (since D2D3' + D3 = D2+D3)
  B = D3 + D1 D2' D3'? 
Standard: 
  A = D3 + D2
  B = D3 + D1 D2'
Wait with priority D3>D2>D1>D0:
  A = D3 + D2 D3' ... = D3 + D2 (D2 above D3? D3 highest so D2 only if D3=0)
```
For priority D3>D2>D1>D0:
```
A = D3 + D2
B = D3 + (~D3)*D1 = D3 + D1 (D2 is bit A only)
V = D0+D1+D2+D3
(Check: D3=1->11, D2=1->10, D1=1->01, D0=1->00)
```

## Decoder-based function synthesis
```
F(A,B,C) = sum of minterms:
  Connect decoder outputs corresponding to minterms of F
  to an OR gate
  F = OR(mi for i where F=1)
```

## Cascading decoders
```
To make 4-to-16 from 2x 3-to-8:
  Use MSB to select which decoder via enable
  Higher address bit controls enable
```

## Quick Reference
| Device | Inputs | Outputs |
|--------|--------|---------|
| Decoder 2x4 | 2 | 4 |
| Decoder 3x8 | 3 | 8 |
| Decoder 4x16 | 4 | 16 |
| Encoder 4x2 | 4 | 2 |
| Encoder 8x3 | 8 | 3 |
| Priority enc | 2^n | n + V |
